                                         Automated Repair of Unrealisable LTL Specifications Guided by
                                                               Model Counting
                                                             Matías Brizzio                                                 Maxime Cordy                                  Mike Papadakis
                                                   IMDEA Software Institute                                       SnT, University of Luxembourg                    SnT, University of Luxembourg
                                                Universidad Politécnica de Madrid                                          Luxembourg                                       Luxembourg
                                                             Spain

                                                             César Sánchez                                               Nazareno Aguirre                               Renzo Degiovanni
                                                      IMDEA Software Institute                                Universidad Nacional de Río Cuarto                   SnT, University of Luxembourg
arXiv:2105.12595v2 [cs.SE] 14 Apr 2023




                                                              Spain                                                       CONICET                                           Luxembourg
                                                                                                                          Argentina

                                         ABSTRACT                                                                                        1   INTRODUCTION
                                         The reactive synthesis problem consists of automatically produc-                                Reactive synthesis is the problem of automatically generating a
                                         ing correct-by-construction operational models of systems from                                  correct-by-construction implementation for a reactive system, from
                                         high-level formal specifications of their behaviours. However, spec-                            a given specification of the expected behaviour [7, 9, 12, 24, 40, 46].
                                         ifications are often unrealisable, meaning that no system can be                                The specification comprises the list of the variables controlled by the
                                         synthesised from the specification. To deal with this problem, we                               environment and system (i.e., inputs and outputs), respectively, and
                                         present AuRUS, a search-based approach to repair unrealisable                                   a declarative description of the expected properties of the system,
                                         Linear-Time Temporal Logic (LTL) specifications. AuRUS aims at                                  i.e., the goals. Based on these, reactive synthesis produces a model
                                         generating solutions that are similar to the original specifications by                         for the system, usually referred to as controller, which interacts
                                         using the notions of syntactic and semantic similarities. Intuitively,                          with the environment, and guarantees the specified goals [46].
                                         the syntactic similarity measures the text similarity between the                                   Temporal logic is widely considered the standard formalism for
                                         specifications, while the semantic similarity measures the num-                                 expressing the expected goals of reactive systems [38]. Reactive
                                         ber of behaviours preserved/removed by the candidate repair. We                                 specifications are usually expressed as assume-guarantee assertions,
                                         propose a new heuristic based on model counting to approximate                                  i.e., 𝐴 ⇒ 𝐺, where 𝐴 captures assumptions on the behaviour of
                                         semantic similarity. We empirically assess AuRUS on many unre-                                  the environment, and 𝐺 expresses the goals the system must fulfill,
                                         alisable specifications taken from different benchmarks and show                                provided that the assumptions are met. Since the specifications are
                                         that it can successfully repair all of them. Also, compared to re-                              the central element in the synthesis, their quality is crucial for a
                                         lated techniques, AuRUS can produce many unique solutions while                                 successful process.
                                         showing more scalability.                                                                           Reactive specifications often contain imperfections that make
                                                                                                                                         them unrealisable, i.e., no controller can be synthesised. Common is-
                                         CCS CONCEPTS                                                                                    sues leading to unrealisability are (1) inconsistencies between goals
                                         • Software and its engineering → Requirements analysis; For-                                    making them unsatisfiable (and therefore unrealisable); (2) inade-
                                         mal methods; Search-based software engineering.                                                 quate assumptions and guarantees, which allow the environment
                                                                                                                                         to satisfy the assumptions and prevent the system from comply-
                                         KEYWORDS                                                                                        ing with the guarantees. Therefore, arriving at a consistent and
                                                                                                                                         realisable specification is not straightforward and demands com-
                                         Search-based Software Engineering, Model Counting, LTL-Synthesis
                                                                                                                                         prehensive elicitation activities to prevent these common issues.
                                         ACM Reference Format:                                                                               Previous attempts have made significant efforts to provide auto-
                                         Matías Brizzio, Maxime Cordy, Mike Papadakis, César Sánchez, Nazareno                           mated mechanisms to assist engineers in identifying and resolving
                                         Aguirre, and Renzo Degiovanni. 2023. Automated Repair of Unrealisable                           sources of unrealisability in temporal logic specifications. Some
                                         LTL Specifications Guided by Model Counting. In Genetic and Evolutionary                        concentrate on diagnosing the cause of synthesis impossibility, e.g.,
                                         Computation Conference (GECCO ’23), July 15–19, 2023, Lisbon, Portugal.                         by computing a core of assertions that make the specification unre-
                                         ACM, New York, NY, USA, 9 pages. https://doi.org/10.1145/3583131.3590454
                                                                                                                                         alisable [16, 29, 48]. Some generate counter-strategies that evidence
                                                                                                                                         how the environment prevents the controller from satisfying the
                                         Permission to make digital or hard copies of all or part of this work for personal or
                                         classroom use is granted without fee provided that copies are not made or distributed           goals [47]. Related to our work, many approaches to repair unreal-
                                         for profit or commercial advantage and that copies bear this notice and the full citation       isable specifications have been presented [8, 13, 14, 37, 41]. These
                                         on the first page. Copyrights for components of this work owned by others than the
                                         author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or
                                                                                                                                         techniques attempt to repair the specifications just by adding as-
                                         republish, to post on servers or to redistribute to lists, requires prior specific permission   sumptions that are built from the information extracted from the
                                         and/or a fee. Request permissions from permissions@acm.org.                                     generated counter-strategies, and the current specification. This
                                         GECCO ’23, July 15–19, 2023, Lisbon, Portugal
                                                                                                                                         is a significant limitation because they do not consider that unre-
                                         © 2023 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                         ACM ISBN 979-8-4007-0119-1/23/07. . . $15.00                                                    alisability might be caused by failures in the current assumptions
                                         https://doi.org/10.1145/3583131.3590454
GECCO ’23, July 15–19, 2023, Lisbon, Portugal                                                                                              Brizzio et al.


and guarantees. These techniques also impose syntactical restric-            𝜑 : 𝐴 → 𝐺 [46], defined over a set of variables V = X ∪ Y, where
tions on how specifications are written, limiting their application          X and Y are the variables controlled by the environment, and
to particular patterns (e.g., GR(1), a subset of LTL).                       system, respectively. A strategy for 𝜑 is a function 𝜎 : (2 X ) + → 2 Y
    In this paper, we present AuRUS, a search-based approach to              that maps finite sequences of subsets of X into subsets of Y. For
repair unrealisable specifications, which applies to LTL [38] spec-          an infinite sequence 𝑋 = 𝑋 1, 𝑋 2, . . . ∈ (2 X )𝜔 , the play induced
ifications and generates candidate repairs by changing both, as-             by strategy 𝜎 is the infinite sequence 𝜌𝜎,𝑋 = (𝑋 1 ∪ 𝜎 (𝑋 1 )) (𝑋 2 ∪
sumptions and guarantees. AuRUS consists of a genetic algorithm              𝜎 (𝑋 2 ))) . . .). A play 𝜌 is winning if 𝜌 |= 𝜑. A strategy is winning
(GA) that, given an unrealisable LTL specification, attempts to gen-         when 𝜌𝜎,𝑋 |= 𝜑 for all 𝑋 ∈ (2 X )𝜔 .
erate a realisable variant of it, which is as close as possible to the          Realisability is the problem of deciding whether a specification
original one. The algorithm iteratively explores candidate repairs           has a winning strategy, and synthesis is the problem of computing
of the original specification, seeking to find a realisable variant          one. The Unrealisability of a specification means that no winning
that is both syntactically and semantically similar to the original          strategy exists for the system. This implies that the environment can
one. The syntactic similarity is measured by using the number of             always falsify the specification, no matter which strategy the system
sub-formulas that belong to both the original and the mutated spec-          chooses. AuRUS performs syntactic changes in the specification to
ification. On the other hand, semantic similarity is measured by             remove the flaw that makes it unrealisable. AuRUS delegates the
calculating the number of behaviours from the original specification         realisability check to Strix [43], one of the most efficient synthesis
that were maintained in the candidate repair. These behaviours are           tools presented at the annual synthesis competition [3].
computed by using model counting. Since all existing model count-
ing approaches for LTL do not scale well, we develop an alternative
approach to approximate the LTL model counting problem which
                                                                             2.3      Genetic Algorithms
considerably improves scalability. We empirically assess AuRUS               Genetic algorithms [27, 30, 44] are heuristic search algorithms,
and show that it is effective at repairing unrealisable specifications       inspired by natural evolution. Candidate solutions are called indi-
not handled by previous techniques, while also producing more                viduals or chromosomes, and are often represented as sequences
unique repairs not computed by related approaches.                           of genes (characteristics) that capture their features. Genetic algo-
                                                                             rithms maintain a population of candidate solutions, rather than a
2 PRELIMINARIES                                                              single “current” candidate, as in traditional search. They are largely
                                                                             driven by random decisions, e.g., in the generation of the initial pop-
2.1 Linear-Time Temporal Logic (LTL)                                         ulation, and how the new candidate solutions are generated from
LTL is a logical formalism widely employed to specify reactive sys-          existing ones. To produce new individuals, it exploits information
tems [38]. Given a set 𝐴𝑃 of propositional variables, LTL formulas           in the current population, combining their characteristics (called
are inductively defined using the standard logical connectives, and          crossover), or randomly altering the information in specific indi-
the temporal operators ⃝ (next) and U (until), as follows: (i) every         viduals (called mutation). The effectiveness of this general search
𝑝 ∈ 𝐴𝑃 is an LTL formula, and (ii) if 𝜑 and 𝜓 are LTL formulas, then         process is guided by a heuristic function, called fitness function.
so are ¬𝜑, 𝜑 ∨ 𝜓 , ⃝𝜑 and 𝜑U𝜓 . Other connectives and operators,             Intuitively, this function measures how “fit” a particular individual
such as ∧, 2 (always), 3 (eventually), and W (weak-until), can be            is, i.e., how close it is to being a real solution to the search problem
defined in terms of the basic ones. LTL formulas are interpreted             under consideration. This evolution process is usually performed
over infinite traces of the form 𝜎 = 𝑠 0 𝑠 1 . . ., where each 𝑠𝑖 is a       until some termination criterion is met, e.g., a defined number of
propositional valuation on 2𝐴𝑃 . Formulas with no temporal opera-            iterations (known as generations of the population). AuRUS em-
tor are evaluated in the first state of the trace. Formula ⃝𝜑 is true in     ploys genetic algorithms to search for realisable repairs, close to
𝜎 iff 𝜑 is true in 𝜎 [1..], i.e., the trace obtained by removing the first   the unrealisable specification given as input. Individuals in our
state from 𝜎. Formula 𝜑U𝜓 is true in 𝜎 iff there exists a position 𝑖 in      case will represent LTL specifications, the genetic operators will
the trace, such that, 𝜓 is true in 𝜎 [𝑖..] and for every 0 ≤ 𝑘 < 𝑖, 𝜑 is     produce new specifications from others, and the fitness function
true in 𝜎 [𝑘..]. An LTL formula 𝜑 is satisfiable (SAT) iff at least one      will attempt to evaluate how “close” a candidate repair is to be
trace satisfies 𝜑. The model counting problem consists of calculating        realisable, as well as how close is to the original (unrealisable) one.
the number of models satisfying 𝜑. In the case of LTL, if a formula
is unsatisfiable, the number of models is zero. Otherwise, it has an
                                                                             3     A MOTIVATING EXAMPLE
infinite number of models. Therefore, LTL model-counting is re-
stricted to bounded models [25], i.e., it computes how many models           Let us present a running example to illustrate the main ideas behind
                                                                             AuRUS. Consider the problem of synchronising the access to a
up to 𝑘 states exist for 𝜑 and a bound 𝑘. AuRUS uses bounded model
                                                                             shared resource, via an arbiter [31]. Two processes request access
counting to guide the search by measuring the semantic impact of             to the resource via signals 𝑟 1 and 𝑟 2 , respectively. An extra signal 𝑎
syntactic changes on candidate repairs, in terms of the number of            indicates when the resource can be accessed. The arbiter indicates
preserved and removed behaviors from the original specification.             which process has been granted access by means of respective
                                                                             signals 𝑔1 and 𝑔2 . Signals 𝑟 1, 𝑟 2 and 𝑎 thus constitute the inputs,
2.2     Reactive LTL Synthesis                                               while signals 𝑔1 and 𝑔2 are the outputs. The following guarantees
Reactive LTL synthesis is the problem of automatically constructing          are elicited in [31] for this problem:
a reactive module that reacts to the environment with the objective
of realizing a given LTL specification of the form assume-guarantee,             𝐺 1 : 2(𝑟 1 → 3𝑔1 ) 𝐺 2 : 2(𝑟 2 → 3𝑔2 ) 𝐺 3 : 2(¬𝑎 → (¬𝑔1 ∧ ¬𝑔2 ))
Automated Repair of Unrealisable LTL Specifications Guided by Model Counting                                    GECCO ’23, July 15–19, 2023, Lisbon, Portugal


 Intuitively, 𝐺 1 states that if the first process requests access to the      by a sub-formula of 𝑆 2 . For instance, if both 𝑆 1 and 𝑆 2 are exactly the
resource, the arbiter will eventually grant it. Guarantee 𝐺 2 states           same specification 𝐺 1 ∧𝐺 2 ∧𝐺 3 , the crossover operator can produce
the same but for the second process. While guarantee 𝐺 3 states that           a new specification 𝑆 3 = 𝐺 1 ∧𝐺 2′ ∧𝐺 3 , where 𝐺 2′ = 2(𝑟 2 → 3𝑔1 ) is
if the resource cannot be accessed, no process is granted permission.          obtained by replacing sub-formula 𝑔2 in 𝐺 2 , by the sub-formula 𝑔1
No assumptions were identified for this specification. Hence, the              extracted from 𝐺 1 in 𝑆 2 . On the other hand, the mutation operator
specification 𝑆 = 𝐺 1 ∧ 𝐺 2 ∧ 𝐺 3 is unrealisable.                             will create a new specification by applying a syntactic mutation to
    A cause of unrealisability is that the environment is allowed to           some sub-formula of the specification. For instance, mutating gener-
set the input signal 𝑎 to false continuously, preventing the arbiter           ated specification 𝑆 3 , the algorithm can produce a new specification
from granting access to the resource (see 𝐺 3 ). Therefore, if any             𝑆 4 = 𝐺 1′ ∧ 𝐺 2′ ∧ 𝐺 3 in which 𝐺 1′ = 2(𝑟 1 → ⃝𝑔1 ) is obtained by
of the processes requests access to the resource in such a situa-              changing the operator 3 by ⃝ in 𝐺 1 . Going back to the arbiter so-
tion, no implementation would satisfy the guarantees 𝐺 1 and 𝐺 2 .             lutions, to obtain the realisable version 𝐺 1 ∧𝐺 2 ∧𝐺 3′ , two mutations
In [31], authors propose different alternatives for “fixing” these             to the original guarantee 𝐺 3 are necessary: first, a replacement of
issues. One option is to add an environment assumption to ensure               the sub-formula 𝑎 by false leading to 2(¬𝑔1 ∧ ¬𝑔2 ); and then the re-
that the resource is allowed to be accessed infinitely often; indeed,          placement of operator ∧ by ∨, obtaining the formula 2(¬𝑔1 ∨ ¬𝑔2 )
by adding the assumption 𝐴1 = 23𝑎, the resulting specification                 which is equivalent to 𝐺 3′ . AuRUS may produce other realisable
becomes realisable. Another option explored in [31] is to indicate             specifications that can also be considered as candidate repairs. The
that the arbiter will enforce mutual exclusion in accessing the re-            fitness function plays a crucial role in guiding the search. Intuitively,
source. This is done by replacing 𝐺 3 by an alternative guarantee              the fitness function is the oracle that is used to assess the quality
𝐺 3′ = 2(¬(𝑔1 ∧ 𝑔2 )). The resulting specification 𝑆 ′ = 𝐺 1 ∧ 𝐺 2 ∧ 𝐺 3′      of the candidate solutions, giving higher scores to “better” individ-
is also realisable. The overall intuition we get from this example is          uals, i.e., those closer to sought solutions. AuRUS implements a
that, in cases of unrealisability, it can sometimes be fixed by making         multi-objective fitness function that assesses three key properties
small changes to the original specification. But, even when the                of the candidate solutions: (1) it checks whether the specification is
repairs were generated automatically, a domain expert would need               realisable or not; (2) it then computes the syntactic similarity with
to review them, and decide which of them is an acceptable solution.            respect to the original specification; and finally (3) it computes the
For instance, the repairs introducing a new assumption would need              semantic similarity with respect to the original specification (i.e.,
to be analysed to check if such an assumption is reasonable to ex-             the number of behaviours preserved and removed by the formula
pect from the environment. Thus, to help the domain expert and                 modifications). We show in Section 6 the importance of each fitness
make easier this validation activity, we would like to maintain as             factor to guide the search toward adequate solutions, i.e., solutions
much as possible from the original specification in the generated              that are very alike to the original.
repairs, and simply modify what is necessary to make it realisable.
In this paper, we propose AuRUS, a genetic algorithm that performs
syntactic modifications to an unrealisable specification, with the             4     AURUS APPROACH
aim of producing a set of realisable candidate repairs. The candidate          AuRUS takes as input an unrealisable specification 𝑆, and by the
repairs are searched for in the “vicinity” of the original specification,      successive application of genetic operations, it aims at producing a
in the sense that they aim at being slight syntactic and especially            specification 𝑆 ′ that is realisable, and minimizes the syntactic and
semantic, modifications of the original one. AuRUS has the chal-               semantic changes with respect to 𝑆.
lenge of dealing with a very large search space of LTL specifications
that are obtained by performing syntactic changes to the original
one. It also needs to objectively quantify the semantic impact of              4.1    Search Space and Initial Population
each change. AuRUS is guided by a multi-objective fitness function             Individuals in our search space are LTL specifications 𝑆 = (𝐴, 𝐺)
that attempts to minimise syntactic and semantic changes, while                over V, consisting of assumptions and guarantees. Genetic opera-
at the same time attempting to achieve realisability. Let us provide           tors are used to produce new individuals with syntactic changes to
some intuition on how AuRUS works, and how it can produce some                 both assumptions and guarantees, with equal probability. AuRUS
solutions presented in [31].                                                   begins by creating assumptions based on patterns commonly found
    AuRUS starts by generating an initial population that represents           in reactive specifications [23] to form the initial population. These
samples of candidate solutions. These are generated by introducing             new assumptions are generated from the original specification 𝑆, re-
new assumptions based on patterns commonly found in reactivity                 sulting in 𝑆 0 = (𝐴 ∪ 𝑎 0, 𝐺), where 𝑎 0 follows the patterns: (1) 23𝑥𝑖 ,
specifications [23]. For example, assumptions stating that input               (2)2¬(𝑥 0 ∧ . . . ∧ 𝑥𝑛 ), and (3) 23(𝑥 0 ∧ . . . ∧ 𝑥𝑛 ), for 𝑥𝑖 ∈ X. These
events occur infinitely often (23𝑟 1 , 23𝑟 2 , 23𝑎), and that differ-          patterns respectively express that the input 𝑥𝑖 holds infinitely many
ent input events cannot simultaneously occur (2¬(𝑟 1 ∧ 𝑟 2 ∧ 𝑎)),              times, that all input events cannot happen at the same time, and that
will be considered. In our running example, the initial population             all input events hold at the same time, infinitely many times. We
already contains one of the realisable solutions proposed in [31].             only include input variables in the assumptions to prevent trivial
Other candidate solutions can be obtained by the successive appli-             solutions. Adding assumptions like 2𝑦, 𝑦 ∈ Y would result in a
cation of genetic operators to some selected specifications. AuRUS             specification that can easily be satisfied by setting 𝑦 to false, making
implements the two most common genetic operators, crossover and                it trivially realisable. AuRUS avoids anomalous solutions [22] in the
mutation. Given two specifications 𝑆 1 and 𝑆 2 , the crossover operator        initial population and checks for unsatisfiable assumptions during
will produce a new specification 𝑆 3 by replacing a sub-formula of 𝑆 1 ,       the search to prevent trivially realisable repairs.
GECCO ’23, July 15–19, 2023, Lisbon, Portugal                                                                                                      Brizzio et al.


4.2     Genetic Operators                                                    were maintained in the candidate. Basically, let 𝑆 be the unrealisable
AuRUS implements the two most common genetic operators such                  specification given as input, the fitness value for a candidate repair
as, crossover and mutation, adapted to LTL. Let 𝑆𝐹 (𝜑) be the list           𝑆 ′ is computed by the following function 𝑓 :
of sub-formulas of 𝜑, e.g., 𝑆𝐹 (2¬𝑝) = [2¬𝑝, ¬𝑝, 𝑝]. We denote                    𝑓 (𝑆 ′ ) = 𝛼 ∗ 𝑠𝑡𝑎𝑡𝑢𝑠 (𝑆 ′ ) + 𝛽 ∗ 𝑠𝑦𝑛𝑆𝑖𝑚(𝑆, 𝑆 ′ ) + 𝛾 ∗ 𝑠𝑒𝑚𝑆𝑖𝑚(𝑆, 𝑆 ′ )
by 𝜑 [𝜙\𝜓 ] the formula that is obtained by replacing occurrences            where 𝑠𝑡𝑎𝑡𝑢𝑠 (𝑆 ′ ) focuses on checking if 𝑆 ′ is satisfiable and realis-
of 𝜙 in 𝜑, by 𝜓 . For instance, 2(¬𝑝) [¬𝑝\𝑟 ] returns 2(𝑟 ). Given           able; while, 𝑠𝑦𝑛𝑆𝑖𝑚(𝑆, 𝑆 ′ ) and 𝑠𝑒𝑚𝑆𝑖𝑚(𝑆, 𝑆 ′ ) compute the syntactic
two formulas 𝜑 and 𝜑 ′ , we define: replaceSub(𝜑, 𝜑 ′ ) = 𝜑 [𝜙\𝜓 ] and       and semantic similarities between 𝑆 and 𝑆 ′ , respectively. Constants
combineSub(𝜑, 𝜑 ′ ) = 𝜑 [𝜙\𝜙 • 𝜓 ], s.t. 𝜙 ∈ 𝑆𝐹 (𝜑), 𝜓 ∈ 𝑆𝐹 (𝜑 ′ ), and      𝛼, 𝛽 and 𝛾 are the factors that assign different weights to the three
• ∈ {∨, ∧, U, R, W}. Intuitively, replaceSub(𝜑, 𝜑 ′ ) returns a new          properties of interest in the candidate repair 𝑆 ′ .
formula that consists of replacing a sub-formula of 𝜑 with a sub-                Let 𝑆 ′ = (𝐴 ′, 𝐺 ′ ) be a candidate solution, we define 𝑠𝑡𝑎𝑡𝑢𝑠 (𝑆 ′ )
                                                                             as follows:
formula of 𝜑 ′ ; while combineSub(𝜑, 𝜑 ′ ) takes a sub-formula from                          1     if 𝐴′ ∧ 𝐺 ′ is satisfiable and 𝐴′ → 𝐺 ′ realisable;
𝜑 and combines it with another from 𝜑 ′ , using a binary operator.
                                                                                            
                                                                                            
                                                                                            
                                                                                             0.5   if 𝐴′ ∧ 𝐺 ′ is satisfiable, but 𝐴′ → 𝐺 ′ unrealisable;
                                                                                            
    The crossover operator combines two LTL specifications, namely
                                                                                            
                                                                                            
                                                                              status(𝑆 ′ ) = 0.2
                                                                                            
                                                                                            
𝑆 1 = (𝐴1, 𝐺 1 ) and 𝑆 2 = (𝐴2, 𝐺 2 ), to create a new specification                                if 𝐴′ ∧ 𝐺 ′ is unsatisfiable, but 𝐴′ /𝐺 ′ are satisfiable;
                                                                                            
                                                                                              0.1   if 𝐴′ is satisfiable, but not 𝐺 ′ ;
                                                                                            
𝑆 3 = (𝐴3, 𝐺 3 ). This is achieved by merging the assumptions and
                                                                                            
                                                                                            
                                                                                            
                                                                                            
                                                                                            0      if 𝐴′ is unsatisfiable.
                                                                                            
guarantees of the original specifications.                                                  
    Particularly, every assumption in 𝐴3 is taken from 𝐴1 or 𝐴2 ,
or is generated by replacing (𝑟𝑒𝑝𝑙𝑎𝑐𝑒𝑆𝑢𝑏 (𝑎 1, 𝑎 2 )) or combining            𝑠𝑡𝑎𝑡𝑢𝑠 (𝑆 ′ ) will return 1 iff 𝑆 ′ is both, satisfiable and realisable.
(𝑐𝑜𝑚𝑏𝑖𝑛𝑒𝑆𝑢𝑏 (𝑎 1, 𝑎 2 )) sub-formulas from 𝐴1 and 𝐴2 , where 𝑎𝑖 ∈ 𝐴𝑖 .       When the candidate 𝑆 ′ is satisfiable, but still unrealisable, 𝑠𝑡𝑎𝑡𝑢𝑠 (𝑆 ′ )
To produce 𝐺 3 , the crossover operator performs the same choices            will return 0.5. Whether assumptions/guarantees are unsatisfiable,
but it takes guarantees from 𝐺 1 and 𝐺 2 instead.                            it will return values closer to 0.
    The mutation operator takes a specification and applies syntactic           𝑠𝑦𝑛𝑆𝑖𝑚(𝑆, 𝑆 ′ ) computes the syntactic similarity between specifi-
modifications to produce a new one. Given a specification 𝑆 =                cations 𝑆 and 𝑆 ′ , measured in terms of the number of sub-formulas
(𝐴, 𝐺), the algorithm randomly selects one assumption/guarantee              that belong to both the original 𝑆 and the candidate 𝑆 ′ :
to which the mutation will be applied. Let 𝑚𝑢𝑡𝑎𝑡𝑒 (𝜑) = 𝜑 ′ be
                                                                                                        #(𝑆𝐹 (𝑆) ∩ 𝑆𝐹 (𝑆 ′ )) #(𝑆𝐹 (𝑆) ∩ 𝑆𝐹 (𝑆 ′ ))
                                                                                                                                                     
the function that takes a formula and produces a mutation of it.              𝑠𝑦𝑛𝑆𝑖𝑚(𝑆, 𝑆 ′ ) = 0.5 ∗                         +
                                                                                                              #𝑆𝐹 (𝑆)                 #𝑆𝐹 (𝑆 ′ )
When the mutation operator is applied to some assumption 𝑎 ∈ 𝐴, it
returns a new specification 𝑆 ′ = (𝐴 ′, 𝐺), where 𝐴 ′ = (𝐴\{𝑎})∪{𝑎 ′ }
and 𝑎 ′ = 𝑚𝑢𝑡𝑎𝑡𝑒 (𝑎). The same applies when some guarantee 𝑔 ∈ 𝐺                Small values for 𝑠𝑦𝑛𝑆𝑖𝑚(𝑆, 𝑆 ′ ) indicate that 𝑆 ′ is syntactically
is mutated. 𝑚𝑢𝑡𝑎𝑡𝑒 is defined as follows:                                    very different from 𝑆, while values closer to 1 indicate that both
                                                                             specifications are very similar. The fitness function uses this value
(1) if 𝜙 = 𝑏 or 𝜙 = 𝑝, where 𝑏 ∈ {true, false} and 𝑝 ∈ 𝐴𝑃, then:
                                                                             to quantify the syntactic changes produced by the genetic operators.
   (a) 𝜙 ′ = 𝑏 ′ , s.t. 𝑏 ′ ∈ {true, false} and 𝑏 ≠ 𝑏 ′ .
                                                                                Small changes in the syntax of a specification may result in
  (b) 𝜙 ′ = 𝑞, s.t. 𝑞 ∈ 𝐴𝑃 and 𝑝 ≠ 𝑞.
                                                                             significant changes in its semantics. For example, a mutation that
   (c) 𝜙 ′ = 𝑜 1𝜙 where 𝑜 1 ∈ {2, 3, ⃝, ¬}.
                                                                             negates a formula may appear as a single syntactic change, but it
(2) if 𝜙 = 𝑜 1𝜙 1 , where 𝑜 1 ∈ {¬, ⃝, 3, 2}, then:
                                                                             can completely reverse the behaviors described by the original for-
   (a) 𝜙 ′ = 𝑚𝑢𝑡𝑎𝑡𝑒 (𝜙 1 ).
                                                                             mula. The function 𝑠𝑒𝑚𝑆𝑖𝑚(𝑆, 𝑆 ′ ) computes the semantic similarity
  (b) 𝜙 ′ = 𝑜 1′ 𝑚𝑢𝑡𝑎𝑡𝑒 (𝜙 1 ), s.t. 𝑜 1′ ∈ {¬, ⃝, 3, 2}.
                                                                             between specifications 𝑆 and 𝑆 ′ , measured in terms of the number
   (c) 𝜙 ′ = 𝑜 1′ 𝑜 1𝑚𝑢𝑡𝑎𝑡𝑒 (𝜙 1 ) where 𝑜 1′ ∈ {¬, ⃝, 3, 2}.
                                                                             of behaviours from the original specification still in the candidate
   (d) 𝜙 ′ = 𝑝 𝑜 2′ 𝑜 1′ (𝑚𝑢𝑡𝑎𝑡𝑒 (𝜙 1 )), s.t. 𝑝 ∈ 𝐴𝑃,
                                                                             repair. To automatically compute this value, we rely on LTL model
              𝑜 2′ ∈ {U, W, ∧, ∨} and 𝑜 1′ ∈ {¬, ⃝, 3, 2}.
                                                                             counting. Given a specification 𝑆 and a bound 𝑘, let us denote by
(3) if 𝜙 = 𝜙 1𝑜 2𝜙 2 , where 𝑜 2 ∈ {∨, ∧, U, R, W}, then:
                                                                             #(𝑆, 𝑘) the number of models up to 𝑘 states satisfying 𝑆. We define
   (a) 𝜙 ′ = 𝑚𝑢𝑡𝑎𝑡𝑒 (𝜓𝑖 ), s.t. 𝜓𝑖 ∈ {𝜙 1, 𝜙 2 }
                                                                             𝑠𝑒𝑚𝑆𝑖𝑚(𝑆, 𝑆 ′ ) as follows:
  (b) 𝜙 ′ = 𝑚𝑢𝑡𝑎𝑡𝑒 (𝜙 1 ) 𝑜 2′ 𝑚𝑢𝑡𝑎𝑡𝑒 (𝜙 2 ), s.t. 𝑜 2′ ∈ {∨, ∧, U, R, W}.                                     
                                                                                                                 #(𝑆 ∧ 𝑆 ′, 𝑘) #(𝑆 ∧ 𝑆 ′, 𝑘)
                                                                                                                                             
   (c) 𝜙 ′ = 𝑜 1′ (𝑚𝑢𝑡𝑎𝑡𝑒 (𝜙 1 ) 𝑜 2′ 𝑚𝑢𝑡𝑎𝑡𝑒 (𝜙 2 )),                                  𝑠𝑒𝑚𝑆𝑖𝑚(𝑆, 𝑆 ′ ) = 0.5 ∗                +
                                                                                                                    #(𝑆, 𝑘)        #(𝑆 ′, 𝑘)
           s.t. 𝑜 1′ ∈ {¬, ⃝, 3, 2} and 𝑜 2′ ∈ {∨, ∧, U, R, W}.                 Notice that small values for 𝑠𝑒𝑚𝑆𝑖𝑚(𝑆, 𝑆 ′ ) indicate that the be-
                                                                             haviours described by 𝑆 are very different from the ones described
4.3     Fitness Function                                                     by 𝑆 ′ . In particular, when 𝑆 ∧ 𝑆 ′ is unsatisfiable, 𝑠𝑒𝑚𝑆𝑖𝑚(𝑆, 𝑆 ′ ) is 0.
AuRUS is guided by a multi-objective fitness function that aims at           As this value gets closer to 1, both specifications characterise an
generating a realisable variant, as close as possible, to the unrealis-      increasingly large number of common behaviours. Since the compu-
able specification given as input. This function focuses on checking         tation of 𝑠𝑒𝑚𝑆𝑖𝑚(𝑆, 𝑆 ′ ) requires calculating several model counting
three key properties of the candidate solutions, with the objective          instances, it is crucial for AuRUS to perform model counting ef-
of finding one that is realisable, and that minimises the syntactic and      ficiently. Thus, later in Section 5, we develop an automata-based
semantic changes with respect to the original specification. Syntac-         estimation for LTL model counting, that scales much better than
tic similarity is measured in terms of the number of sub-formulas            exact LTL model counting algorithms. The user can select different
shared by the original specification and the candidate. Semantic             values for the different parameters that might affect the fitness
similarity is measured in terms of the number of behaviours that             function, e.g., 𝛼, 𝛽, 𝛾, and the bound 𝑘. We tested AuRUS in various
                                                        {p}     {p,q}        {q}             {p}            {p}       {p,q}               {q}               {p}



                                                           {}         {p,q}              {p,q}
                                                                                                                                          s0         s1         s2
                                                                       {p}
                                                                s0                 s1                                         s0          0           2          2

                                                          {q}          {q}                                                    s1          0           1          1

                                                                                                               s0             s
                                                                                                                             s1 2         0si         2    sk    2                 s0        s0     si         sk

Automated Repair of Unrealisable LTL Specifications Guided by Model Counting                                  {p}       {p,q}         {q}                 {p}
                                                                                                                                                                             GECCO
                                                                                                                                                                               {p}  ’23, July
                                                                                                                                                                                   {p,q}   {q}15–19,
                                                                                                                                                                                                 {p} 2023, Lisbon, Portugal

                                                                                             {p,q}
                                                                                                                 {}               {p,q}
                                                                                                                                     {p}              {p,q}
                                                                      {p}                                      {q}
complex specifications, selecting the best-performing configuration
                                                                 s   {p,q}               1                      {}                  {p,q}
                                                                                                                                    {p}
                                                                                                                                                                {p,q}         s0        s1   s2
                                                                                                                                                                                                               s0     s1
                                                                                                                        s0                      s1
                                                                                                                                                                        s0     0        2    2
and comparing its effectiveness to previous techniquess in Section
                                                            {q}  0
                                                                   6. {p}                                               s0                            s1                                                 s0     2     2
                                                                                              {p,q}               {q}               {q}                                 s1     0        1    1

                                                                      {}                s2                                           {q}                                s2     0        2    2           s1     1     1
4.4     Selection                                                    {q}                       {}
                                                                                                                                                          {p,q}
                                                                                              {q}
The fittest individuals are chosen for the next generation using the                                                 {p}
                                                                                                          Figure 1: Finite automaton.
                                                                                                                           s
                                                                                                                                      {q}
                                                                                                                                       Figure  2: Transfer
                                                                                                                                            {p,q}   {p,q}
                                                                                                                                                      1    matrix.
                                                                                                                                                                                                  {p}
                                                                                                                    {p,q}              {}
traditional “best selector” operator, sorting individuals by fitness                                                    s0            {q}                   {p}
                                                                                                                                                           {p,q}                             s0           s1
and selecting the best until maximum population size.
                                                                                                                                                     s2
                                                                                                      multiplying 𝑘 times matrix{}
                                                                                                                               {q}
                                                                                                                                {}   𝑇𝜑 ; and 𝐹 is a{q}column vector codifying
                                                                                                                               {q}
4.5     Soundness, and (In)completeness                                                               the final (accepting) states of 𝐴𝜑 . For example, Fig. 1 and Fig. 2 show
                                                                                                      the automaton and the transfer matrix, generated by our approach
AuRUS guarantees satisfiability and realisability of its generated
                                                                                                      from the formula 𝜓 = 2(𝑝 → ⃝𝑞). Considering 𝑘 = 4, our model
repairs, checked using Polsat [35] and Strix [43], respectively. While
                                                                                                      counting approach answers that there are 108 models, computed
AuRUS uses a non-exhaustive search and may not consider all
                                                                                                      by the following matrices multiplication:
possible repairs, its genetic operators are complete, allowing the                                                                4
production of 𝜑 ′ from 𝜑 via crossover and mutation.
                                                                                                                                                                
                                                                                                                           2 2                            54 54      1
                                                                                                       𝐼 × 𝑇𝜑4 × 𝐹 = 𝐼 ×
                                                                                                                                                 
                                                                                                                                     ×𝐹 = 1 0 ×                  ×      = 108
                                                                                                                           1 1                            27 27      1
5     LTL MODEL COUNTING APPROXIMATION                                                                 Actually, there are exactly 351 lasso traces of length 4 for 𝜓 but
AuRUS proposes to use LTL model counting to compute the se-                                           our approach reports 108 (i.e., the approximate number of prefixes
mantic similarity 𝑠𝑒𝑚𝑆𝑖𝑚(𝑆, 𝑆 ′ ). Unfortunately, exact LTL model                                     for these traces). However, we show in Section 6.5 that it provides
counting techniques quickly reach their scalability limits [25]. As a                                 a good estimation of the exact model counting. Meaning that, if
consequence, the work presented in [19] attempts to deal with the                                     it computes that formula 𝜑 has more prefixes of length 𝑘 than
scalability issues. It presents a translation from LTL formulas to                                    formula 𝜓 , then it is almost sure that the number of lasso traces of
regular expressions, such that, each string recognized by the regular                                 𝜑 of length 𝑘 is greater than the number of lasso traces for 𝜓 .
expression is a prefix of some trace satisfying the formula. Then, a
string model counter (ABC [10]) is used to compute the number of                                      6     EXPERIMENTAL EVALUATION
strings that, up to a certain length, satisfy the regular expression.                                 We evaluate AuRUS around the following research questions:
Though effective, this approach works on specific examples but
                                                                                                        RQ1 How effective and efficient is AuRUS?
fails to scale overall (failing in 22/26 specifications, see Section 6).
                                                                                                        RQ2 How does it compare with random generation?
   Thus, we develop a new technique to efficiently estimate the LTL
                                                                                                        RQ3 Does AuRUS generate unique solutions?
model counting problem. Intuitively, we aim at counting the number
                                                                                                        RQ4 How does each objective of the fitness function contribute to
of prefixes satisfying an LTL formula and use that number as a proxy
                                                                                                             AuRUS’ effectiveness?
for the number of models of the formula. To improve scalability,
                                                                                                        RQ5 What is the precision of our model counting method?
we employ matrices multiplication for this task (as ABC [10]).
   Basically, our approach operates in two steps. First, we rely on                                   We answer RQ1-RQ4 using unrealisable specifications from the
established algorithms to generate an automaton 𝐴𝜑 that recog-                                        literature and benchmarks, and RQ5 using randomly picked LTL
nises all the traces satisfying a given formula 𝜑. Recall that LTL                                    formulas from an LTL SAT solving benchmark.
formulas are interpreted on infinite traces (c.f. Section 2.1). This                                      Specifications. We consider 26 unrealisable specifications in our
means that every trace satisfying 𝜑, has a path in automaton 𝐴𝜑 , in                                  evaluation. Table 1 summarises for each specification the number
which some accepting state is visited infinitely many times (i.e., a                                  of input/output variables, assumptions (A), and guarantees (G). We
loop). Notice that, every finite path reaching some accepting state                                   consider 5 cases from the literature, 13 from SYNTCOMP [4], and 8
of 𝐴𝜑 , is potentially a prefix of some trace recognised by 𝐴𝜑 . Then,                                specifications created by students and reported in SYNTECH15 [41].
we can have an estimation of the number of traces accepted by
                                                                                                                               Table 1: Unrealisable Specifications.
𝐴𝜑 , by counting the number of finite paths of 𝐴𝜑 that reach some                                           Literature (5)                      #In-Out              #A-#G               SYNTCOMP (13)              #In-Out   #A-#G
accepting state (this can be thought as if we interpreted accepting                                            Arbiter                              3-2                 0-3                    Detector                 2-1    0-4
                                                                                                             MinePump                               2-1                 1-2                  Full Arbiter               3-3    0-16
states as final states). Notice that, it may happen that our approach
                                                                                                                 RG1                                2-2                 1-4                      Lily02                 3-1    0-3
overestimates the number of models for 𝜑. For instance, when some                                                RG2                                2-1                 0-2                      Lily11                 2-2    0-1
reachable accepting state does not loop. Conversely, the accepting                                               Lift                               3-3                7-12                      Lily15                 2-2    0-5
                                                                                                                                                                                                 Lily16                 3-3    0-9
state may be part of multiple loops; in this case, the prefix accepted                                     SYNTECH15 (8)                        #In-Out              #A-#G                 Load Balancer                3-2    3-8
by 𝐴𝜑 corresponds to multiple traces, which leads to underestimat-                                          Humanoid458                            3-10                0-11                  ltl2dba_R_2                2-1    0-1
ing the number of models for 𝜑. These are the reasons why our                                               Humanoid503                            6-11                1-17               ltl2dba_theta_2               4-1    0-1
                                                                                                            Humanoid531                            1-11                2-17                    ltl2dba27                1-1    0-1
approach only approximates the number of models.                                                            Humanoid741                            4-14                5-21             Prioritized Arbiter             4-4    1-10
   Then, we encode automaton 𝐴𝜑 into a 𝑁 × 𝑁 transfer matrix 𝑇𝜑 ,                                           Humanoid742                            1-14                2-26                 Round-Robin                 2-2    2-4
                                                                                                              GyroV1                                3-3                 6-7                Simple Arbiter               2-2    0-4
where 𝑁 is the number of states in 𝐴𝜑 , such that the value of each                                           GyroV2                                3-3                 7-7
𝑇𝜑 [𝑖, 𝑗] denotes the number of transitions from states 𝑖 to 𝑗 in 𝐴𝜑 .                                       PCarV2-888                             3-9                4-21
The number of finite paths, of length 𝑘, reaching some accepting
state of 𝐴𝜑 , can be computed by solving 𝐼 ×𝑇𝜑𝑘 × 𝐹 , where 𝐼 is a row                                  Implementation. AuRUS uses OWL [32] to manipulate LTL
vector codifying the initial states; 𝑇𝜑𝑘 is the matrix resulting from                                 specifications. Apache Commons Math [2] to manipulate matrices
GECCO ’23, July 15–19, 2023, Lisbon, Portugal                                                                                                                 Brizzio et al.


for model counting. AuRUS also integrates Polsat [35], a portfolio            by the algorithm to finally find realisable solutions. In particular,
that runs 4 LTL solvers in parallel. Moreover, AuRUS uses Strix [43]          the first 2 cases are part of the synthesis competition and were
to check realisability. The experiments in this section were con-             made artificially unrealisable (by adding assertions contradicting
ducted on a cluster with Xeon 2.6GHz, with 16Gb of RAM, running               the existing ones) to use them for assessing the efficiency of the
GNU/Linux. The tool, case studies, and a description of how to                tools participating in the competition.
reproduce the experiments can be found in the replication pack-
age https://sites.google.com/site/unrealrepair/.                                     Table 2: Comparison between AuRUS and random.
                                                                                     Literature     Tech.   #Sol.   Time      SYNTCOMP             Tech.   #Sol.   Time
   Experimental Setup. As AuRUS is driven by random decisions,                        Arbiter      AuRUS     467     921        Detector          AuRUS     522    1799
for each experiment, we run it 10 times. Precisely, in our experi-                                Random      11     404                         Random      21    1592
                                                                                     Minepump      AuRUS     481     897      Full Arbiter        AuRUS       4    3805
mentation AuRUS is configured as follows: the population size is                                  Random      31     678                         Random       6    1003
100, the model-counter bound 𝑘 is 20, best selector, the crossover                     RG1         AuRUS     380     905         Lily02           AuRUS     387    2656
                                                                                                  Random      15     529                         Random       4     427
operator is applied to 10% of the individuals, and the mutation oper-                  RG2         AuRUS     459     935         Lily11           AuRUS     623     834
ator is applied to each individual, to which each gene (sub-formula)                              Random      27     406                         Random      35     350
                                                                                        Lift       AuRUS     303    3170         Lily15           AuRUS     424    1643
is mutated with a probability of 1/𝑁 (where 𝑁 is the size of the                                  Random       0     930                         Random       4    1248
                                                                                                                                 Lily16           AuRUS     385    1756
formula). The termination criterion is reached either when 1000                     SYNTECH15       Tech.   #Sol.   Time                         Random       6     984
individuals are generated or after 2hrs of execution time.                            GyroV1       AuRUS     530    1574     Load Balancer        AuRUS     532    1619
                                                                                                  Random       7     724                         Random      29     801
   Notice that, our fitness function (Sec. 4.3) focuses on three as-                  GyroV2       AuRUS     618    1388      ltl2dba_R_2         AuRUS     623    1442
pects of the candidate solution (the status (𝛼), the syntactic (𝛽) and                            Random      40     771                         Random      42    1451
                                                                                    Humanoid458    AuRUS     582    2307    ltl2dba_theta_2       AuRUS     660    1453
semantic (𝛾) similarities). We assess the performance of AuRUS                                    Random      26     738                         Random      32    1493
under many configurations, by considering values for 𝛼, 𝛽, and                      Humanoid503    AuRUS       3    7400       ltl2dba27          AuRUS     582    1473
                                                                                                  Random       1     616                         Random      46    1048
𝛾, such that 𝛼 + 𝛽 + 𝛾 = 1 (i.e., the sum of weights is 100%). We                   Humanoid531    AuRUS      86    7400   Prioritized Arbiter    AuRUS      13    4205
                                                                                                  Random      19     239                         Random      24    5680
organise our unrealisable specifications into two disjoint sets: the                Humanoid741    AuRUS      80    7400     Round-Robin          AuRUS     678    1713
development set, and the evaluation set. We randomly selected 6                                   Random      11     756                         Random      76     904
                                                                                    Humanoid742    AuRUS      99    7400    Simple Arbiter        AuRUS     504    1012
cases to be part of the development set (2 from the literature, 2                                 Random      21     705                         Random      17     404
from SYNTECH15, and 2 from SYNTCOMP) and the remaining 20                           PCarV2-888     AuRUS       3    7400
                                                                                                  Random       4     174
cases as part of the evaluation set. The development set is meant to
support us in setting the parameters of our algorithm, with the hope
                                                                              6.2      Comparison with Random Generation
that the best-performing configuration for the development set, will
generalise to the evaluation set. To find the best-performing con-            Random starts by producing 1000 syntactic variants of each unre-
figuration, for each experiment we measure the number of repairs              alisable specification and then checks which one is satisfiable and
generated by AuRUS, as well as, the syntactic and semantic similari-          realisable. The random approach uses the same mutation opera-
ties of the found solutions. Then, for each case, we can compare the          tor as AuRUS to produce syntactic modifications to the original
performance of two configurations by using the Vargha-Delaney                 specifications, with the additional requirement that at least one
A (𝐴ˆ12 ) measure [53], to determine which configuration obtained             sub-formula (assumption/guarantee) has been modified. We repeat
better performance for that particular subject. This will allow us to         this experiment 10 times and report all results in Table 2. Notice
analyse which configuration generalises more and better to all the            that, unsurprisingly, the time required by random is considerably
case studies. Particularly, realisability checking is crucial for qual-       smaller than the required by AuRUS in most cases, except for cases
ity and quantity of solutions. Also, better performance is reached            ltl2dba_R_2, ltl2dba_theta_2 and Prioritized Arbiter. However, ran-
when the weight assigned to the semantic similarity is greater or             dom effectiveness is relatively low compared to AuRUS, producing
equal to the one assigned to the syntactic similarity. For instance,          on average 23 times less repairs than AuRUS. We also compute,
configurations (𝛼 = .7, 𝛽 = .1, 𝛾 = .2), (𝛼 = .8, 𝛽 = .07, 𝛾 = .13), or       for each case study, the 𝐴ˆ12 measure to compare the number of
(𝛼 = .9, 𝛽 = .05, 𝛾 = .05) typically reach better performance.                repairs obtained in the 10 runs of our best-performing configu-
                                                                              ration and random. 𝐴ˆ12 results to be 100% for almost every case
                                                                              study, indicating that AuRUS obtains more repairs than random
6.1     Effectiveness and Efficiency Evaluation                               in every run. There are only 3 exceptions where random produces
Table 2 summarises the average results, out of the 10 runs, obtained          more realisable solutions: in Full Arbiter (𝐴ˆ12 of 33.3%), Prioritized
with the best-performing configuration for each case study. We                Arbiter (𝐴ˆ12 of 10.5%) and PCarV2-888 (𝐴ˆ12 of 33.3%). Fig. 3 shows
report the average number of repairs and time (in seconds) per case           further details regarding random performance.
required by AuRUS to explore the 1000 individuals. Noticeable, Au-
RUS succeeds in generating satisfiable and realisable repairs in 100%         6.3      Comparison with Related Approaches
of the runs. As expected, it required more time to analyse the more           We study to what extent AuRUS’s repairs are unique or related to
complex specifications such as the Lift, full arbiter, and Humanoid           the repairs produced by other approaches. Precisely, we analyse
cases in which the 2 hours timeout was reached. Particularly, there           if AuRUS is able to produce some equivalent, weaker, or stronger
are four cases for which the algorithm could find just a few repairs:         repair. We say that a formula 𝐵 is weaker than 𝐴, if 𝐴 → 𝐵 holds
on average, 4 repairs for the full arbiter, 13 for the prioritized arbiter,   (i.e. if 𝐴 ∧ ¬𝐵 is unsatisfiable). Typically, weaker specifications are
and 3 repairs for Humanoid503 and PCarV2-888. This is because                 thought of as more general solutions, while stronger ones corre-
these cases contain several guarantees that require many changes              spond to more localised solutions. Our intention is twofold: we
Automated Repair of Unrealisable LTL Specifications Guided by Model Counting                                                                          GECCO ’23, July 15–19, 2023, Lisbon, Portugal


want to show that AuRUS can produce repairs that are close to the              techniques, and provide a rich set of variants to the engineer to
ones obtained by other approaches, and also that it can generate               resolve the source of unrealisability.
unique solutions that cannot be computed by existing techniques.
   Manually reported solutions. AuRUS can generate equivalent so-              6.4         Importance of the three properties
lutions to some manual repairs, reported in the literature, for the            We first study AuRUS’ effectiveness, when some properties are
Arbiter, MinePump, RG2, and Lift cases. Additionally, it produces              deactivated from the fitness function. We run it under six extra
some weaker/stronger solutions, compared to the manual ones, as                configurations (see Fig. 3). In configurations (Syn, Sem, Syn+Sem)
well as many unique solutions, giving further choices to the engi-             we deactivate the status checking, being AuRUS only guided by the
neer in how to refine the specifications to get a realisable one.              syntactic and/or semantic similarity (realisability is only checked
   Automatically generated solutions. We consider the work pre-                at the end of the execution, to check which candidate is a solu-
sented by Maoz et al. [41], limited to GR(1). They present two sym-            tion). In configurations (Real, Real+Syn, Real+Sem) we deactivate
bolic techniques for learning missing assumptions: JVTS-Repair,                the syntactic and/or semantic similarity computation from the fit-
which generates new assumptions from the counter-strategies built              ness function. Configuration Real+Syn+Sem denotes that AuRUS is
as proofs of unrealisability; and GLASS, that computes safety, jus-            guided by the three properties. Fig. 3 reports, for each configuration,
tice, and initial assumptions to ensure the corresponding safety,              the average percentage of repairs found per case study, with respect
justice, and initial guarantees of the unrealisable specification. Also,       to the best performance previously discussed (with the three factors
[41] re-implements the algorithm presented in [8](AMT13), which                activated). Precisely, for the orange plots (repairs produced), the
also generates missing assumptions from counter-strategies. Notice             y-axis represents the relative difference between configuration runs
that, while GLASS generates only 1 candidate repair, JVTS-Repair               and the best result for this metric across all configuration runs. For
and AMT13 may generate many candidates (because they try to                    instance, the configuration Real+Syn+Sem produced on average 467
remove the counter-strategies generated). To perform this compari-             repairs while the highest number across all configurations is 531
son we took specifications from SYNTECH15 and others expressed                 in the arbiter example. In the red and green plots, the similarity
in GR(1) such as RG1, RG2, and Lift (see Table 1).                             is measured relative to the original specification. Notice that, by
                                                                               removing the realisability checking, AuRUS behaves pretty similar,
                    Table 3: Repairs Overlapping                               or even worse, than random, affecting drastically its effectiveness
                 Case      AuRUS     GLASS   JVTS-Repair     AMT13
                 RG1       379 / 1     1/0         46 / 0     98 / 1           in finding repairs. On the other hand, configurations that use re-
                 RG2       453 / 6     0/1         11 / 1     20 / 4           alisability checking considerably improve AuRUS’ effectiveness,
                 Lift      302 / 1     1/0        145 / 0      1/1             being able to find more solutions. In fact, we compute 𝐴ˆ12 values
               GyroV1      529 / 1     1/0          7/0       22 / 1
               GyroV2      617 / 1     1/0          9/0       13 / 1           to compare different configurations for each case, and we can en-
             Humanoid458   582 / 0     1/0          1/0        1/0             sure that if AuRUS is guided by the 3 properties (Real+Syn+Sem), it
             Humanoid503     3/0       1/0      Timeout     Timeout
             Humanoid531    86 / 0     1/0      Timeout     Timeout
                                                                               obtains more repairs than the configurations that remove some of
             Humanoid741    80 / 0     1/0      Timeout     Timeout            the properties.
             Humanoid742    99 / 0     1/0          3/0     Timeout               We also analyse the quality of the best 10 ranked repairs, mea-
              PCarV2-888     3/0       1/0        289 / 0   Timeout
                                                                               sured in terms of the syntactic (red) and semantic (green) similarity,
                                                                               that can be presented to the engineer for analysis and validation. It
   Table 3 summarises, for each case, the number of unique solu-               is almost always the case that our best-performing configuration
tions (left) produced by AuRUS, i.e., the number of solutions not              (Real+Syn+Sem) obtains better syntactic and semantic similarities
generated by other techniques, and the number of equivalent so-                than the other configurations. Only in a few cases where random
lutions to one produced by other approaches (right). Notice that               found more repairs than AuRUS, outperforms us in syntactical and
the comparison is always in between AuRUS and the related tech-                semantic similarities. Two exceptions occur in Humanoid741/742,
niques, but we do not compare the related approaches against each              where the solutions found by configuration Real+Sem have better
other (i.e., we do not compare GLASS vs JVTS-Repair vs AMT13).                 semantic similarities than the repairs found by Real+Syn+Sem. The
   We observe that in most of the cases, AuRUS and GLASS com-                  outliers in Fig. 3 correspond to the mentioned cases.
plement each other, with the only exception for case RG2, where
AuRUS produces an equivalent solution to the one proposed by                          1



GLASS. Moreover, for all considered cases, AuRUS generates many
                                                                                     0.8

weaker/stronger repairs (between 2 and 80) than the one provided
by GLASS, and the remaining are unique. When analysing AMT13                         0.6



repairs, we observe that AuRUS generates, for all cases in which
                                                                                     0.4
the bound of 10 minutes was not reached (same timeout of [41]) ex-
cept for Humanoid458, between 1 to 4 equivalent solutions, and the                   0.2


remaining In the case of JVTS-Repair, AuRUS only generates 1 equiv-
                                                                                      0
alent solution for the case RG2. In all case studies, many solutions                       random               Syn             Sem               Syn+Sem           Real             Real+Syn      Real+Sem   Real+Syn+Sem




generated by AuRUS maintains some relation (i.e., weaker/stronger)                         Percentage of Solutions    Syntactic Similarity (10 top ranked)   Semantic Similarity (10 top ranked)




to the ones generated by JVTS-Repair and AMT13, but the majority
are unique. The results evidence that the overlapping between the                           Figure 3: Impact of each factor of the fitness.
solutions is low, indicating that AuRUS can complement existing
GECCO ’23, July 15–19, 2023, Lisbon, Portugal                                                                                             Brizzio et al.


6.5     Evaluating our Model Counting Approach                                 [11], and model-based testing [26]. Detecting and finding flaws in
To evaluate the precision and scalability of our model counting                specifications have been the focus on many studies [20, 21, 52] Re-
approach, we compare it with two related approaches. Firstly, we               cent works present different techniques to automatically repair the
re-implemented an established exact model counting approach,                   system’s specification [6, 15, 18]. Unlike these approaches, which
that will be used as a baseline in the comparison. We basically en-            target the behavioural model, AuRUS aims to repair the declara-
code LTL formulas as propositional formulas, such that, for a given            tive specification from which the synthesis tool will later generate
bound 𝑘, each satisfying valuation of the encoding corresponds to              an adequate model. LTL-Reactive synthesis has been studied for
a lasso-trace of 𝑘 states of the formula [33]. Then, we can use a              many years [7, 9, 24, 40, 45, 46]. Many approaches have focused on
propositional model counter [28, 49, 50] to indirectly solve the LTL           diagnosing the cause of unsynthesisability by computing a core of
(bounded) model counting. The propositional encoding explodes ex-              assertions that makes the specification unreal [48] or by generating
ponentially as the bound is incremented, thus it can only be applied           a counter-strategy showing how the environment can prevent the
to small values of 𝑘. For the comparison, we additionally consider             controller from satisfying the guarantees [47]. Other approaches
the approach that served us as motivation, presented in [19]. It also          focus on undesirable properties of realisable specifications that
attempts to approximate LTL model counting, by generating a regex              affect the controllers’ quality [22]. AuRUS guarantees to produce
from a formula, then fed to the string model counter ABC [10] to               satisfiable and realisable repairs, and the mentioned techniques can
estimate the number of models. Encoding our reactive specifica-                complement the analysis to assess and improve our repairs’ quality.
tions into propositional constraints can quickly produce formulas                 Recent approaches focus on inferring missing assumptions from
beyond what exact model counters can analyse. Therefore, we gen-               unrealisable specifications [8, 13, 14, 37, 41]. Their limitations are
erate ten sets, 𝑆 0, . . . , 𝑆 9 , with 50 random LTL formulas, feasible for   twofold: they work on LTL fragments, e.g., GR(1), and only attempt
all approaches, taken from a well-established benchmark [1], used              to solve unrealisability, adding assumptions, not considering that
for assessing LTL SAT solvers [36]. For each formula in each set,              existing ones/guarantees might be incorrect, which is often the
we compute the number of models, for 𝑘 ∈ [6..10], using the Exact              case [5, 51, 52]. We show in Section 6.3 that AuRUS complements
Model-Counting, the approach of [19] (RE), and our Approximate                 these techniques by being able to analyse general LTL specifica-
Model-Counting (ApMC). Then, we rank the formulas in ascending                 tions, changing both assumptions and guarantees, and providing
order w.r.t. the number of models obtained with each technique.                more variants to repair unrealisability. Program repair tools, like
We compare these rankings to verify if the techniques preserve the             GenProg [34] and DirectFix [42], use evolutionary algorithms to ex-
ranking of the exact MC.                                                       plore syntactical variants of the buggy program. These algorithms
                                                                               also aim to guide the search toward repairs similar to the input
                   Table 4: Model Counting results.                            program. AuRUS uses LTL model counting to measure the seman-
                   Time     Time             Diff   Time          Diff
                                                                               tic distance of the candidates concerning the initial specification.
             Set   Exact   ApMC    Exact - ApMC       RE   Exact - RE
             𝑆0     3685       2               0     102           11          We show that existing LTL model counting tools [19, 25] quickly
             𝑆1     8815       2               2     102            9          reach their scalability limits. Thus, we developed an approach to
             𝑆2     5757       2               0     101            7
                                                                               approximate it, proving that it is more efficient than the mentioned
             𝑆3     5299       2               0     101            6
             𝑆4     5844       2               0     102            5          methods.
             𝑆5     5665       2               0     102            6
             𝑆6     5130       2               0     103           10          8   CONCLUSION
             𝑆7     5929       2               0     103            8
             𝑆8     8800       2               0     101           10          This paper presents AuRUS, a search-based approach to repair unre-
                    6172       2               0     103            7
             𝑆9
                                                                               alisable specifications. Compared to previous methods that typically
                                                                               focus their analyses on identifying missing assumptions, AuRUS
   Table 4 shows the results of the comparison only for bound                  aims to modify assumptions and guarantees. The key aim is to gen-
𝑘 = 10 (other bounds are in the tool’s site). It reports the execution         erate realisable versions close to the given unrealisable ones. We
time in seconds and the difference between rankings provided by                defined syntactic and semantic similarity notions, essentials in guid-
ApMC and RE w.r.t. the ranking of the Exact model counter. The                 ing the algorithm towards quality solutions. AuRUS succeeded in
results show that ApMC, in 9/10 sets, produces the same ranking                repairing several case studies from the literature, established bench-
as Exact. In only 1 set it misclassified 2/50 formulas. Contrary, RE           marks, and managed to generate solutions in line with manual and
misclassified 8 formulas per set on average. Exact required 470                automated fixes.
seconds, for a bound of 6, to 6000 seconds, for a bound of 10, to
analyze each set on average. RE required more than 100 seconds                 ACKNOWLEDGMENT
per set, while ApMC required only 2 seconds per set. We assess
                                                                               This work is made possible by the support of the Luxembourg
scalability by testing approaches on 26 Table 1 specifications. Exact
                                                                               National Research Funds (FNR) through the CORE project grant
quickly becomes infeasible, while RE failed on 22/26 specifications,
                                                                               C19/IS/13646587/RASoRS, the PRODIGY Project (TED2021-132464B-
but ApMC succeeded on all, even with large bounds.
                                                                               I00) funded by MCIN/AEI/10.13039/501100011033/ and the Euro-
7     RELATED WORK                                                             pean Union NextGenerationEU/PRTR, as well as a research grant
                                                                               from Nomadic Labs and the Tezos Foundation.
In reactive modeling, the system’s expected properties are captured
in temporal logics [38, 39], this is a typical setting in many essen-
tial activities, such as model checking [17], property monitoring
Automated Repair of Unrealisable LTL Specifications Guided by Model Counting                                                           GECCO ’23, July 15–19, 2023, Lisbon, Portugal


REFERENCES                                                                                     [28] Roberto J. Bayardo Jr. and Robert Schrag. Using CSP look-back techniques to solve
 [1] Aalta benchmark. https://www.lab301.cn/aalta/node3.html.                                       real-world SAT instances. In Proceedings of the Fourteenth National Conference
 [2] Commons math: The apache commons mathematics library. https://commons.                         on Artificial Intelligence and Ninth Innovative Applications of Artificial Intelligence
     apache.org/proper/commons-math/.                                                               Conference, AAAI 97, IAAI 97, July 27-31, 1997, Providence, Rhode Island., pages
 [3] The reactive synthesis competition. www.syntcomp.org.                                          203–208, 1997.
 [4] Synthesis competition repository. https://bitbucket.org/swenjacobs/syntcomp/.             [29] Robert Könighofer, Georg Hofferek, and Roderick Bloem. Debugging formal
 [5] Dalal Alrajeh, Antoine Cailliau, and Axel van Lamsweerde. Adapting require-                    specifications: a practical approach using model-based diagnosis and counter-
     ments models to varying environments. In Proceedings of the ACM/IEEE 42nd                      strategies. Int. J. Softw. Tools Technol. Transf., 15(5-6):563–583, 2013.
     International Conference on Software Engineering, ICSE ’20, page 50–61, New York,         [30] John R. Koza. Genetic Programming: On the Programming of Computers by Means
     NY, USA, 2020. Association for Computing Machinery.                                            of Natural Selection. MIT Press, Cambridge, MA, USA, 1992.
 [6] Dalal Alrajeh and Robert Craven. Automated error-detection and repair for                 [31] Hadas Kress-Gazit and Hazem Torfah. The challenges in specifying and ex-
     compositional software specifications. In Dimitra Giannakopoulou and Gwen                      plaining synthesized implementations of reactive systems. In Bernd Finkbeiner
     Salaün, editors, Software Engineering and Formal Methods, pages 111–127, Cham,                 and Samantha Kleinberg, editors, Proceedings 3rd Workshop on formal reason-
     2014. Springer International Publishing.                                                       ing about Causation, Responsibility, and Explanations in Science and Technology,
 [7] R. Alur and S. La Torre. Deterministic generators and games for LTL fragments.                 Thessaloniki, Greece, 21st April 2018, volume 286 of Electronic Proceedings in
     In Proceedings 16th Annual IEEE Symposium on Logic in Computer Science, pages                  Theoretical Computer Science, pages 50–64. Open Publishing Association, 2019.
     291–300, June 2001.                                                                       [32] Jan Kretínský, Tobias Meggendorfer, and Salomon Sickert. Owl: A library for 𝜔 -
 [8] Rajeev Alur, Salar Moarref, and Ufuk Topcu. Counter-strategy guided refinement                 words, automata, and LTL. In Automated Technology for Verification and Analysis
     of GR(1) temporal logic specifications. In Formal Methods in Computer-Aided                    - 16th International Symposium, ATVA 2018, Los Angeles, CA, USA, October 7-10,
     Design, FMCAD 2013, Portland, OR, USA, October 20-23, 2013, pages 26–33, 2013.                 2018, Proceedings, pages 543–550, 2018.
 [9] Eugene Asarin, Oded Maler, Amir Pnueli, and Joseph Sifakis. Controller synthesis          [33] Timo Latvala, Armin Biere, Keijo Heljanko, and Tommi A. Junttila. Simple
     for timed automata. IFAC Proceedings Volumes, 31(18):447 – 452, 1998. 5th IFAC                 bounded LTL model checking. In Formal Methods in Computer-Aided Design, 5th
     Conference on System Structure and Control 1998 (SSC’98), Nantes, France.                      International Conference, FMCAD 2004, Austin, Texas, USA, November 15-17, 2004,
[10] Abdulbaki Aydin, Lucas Bang, and Tevfik Bultan. Automata-based model count-                    Proceedings, pages 186–200, 2004.
     ing for string constraints. In Computer Aided Verification - 27th International           [34] Claire Le Goues, ThanhVu Nguyen, Stephanie Forrest, and Westley Weimer.
     Conference, CAV 2015, San Francisco, CA, USA, July 18-24, 2015, Proceedings, Part              Genprog: A generic method for automatic software repair. IEEE Trans. Softw.
     I, pages 255–272, 2015.                                                                        Eng., 38(1):54–72, January 2012.
[11] Andreas Bauer, Martin Leucker, and Christian Schallhart. Runtime verification             [35] Jianwen Li, Geguang Pu, Lijun Zhang, Yinbo Yao, Moshe Y. Vardi, and Jifeng He.
     for LTL and TLTL. ACM Trans. Softw. Eng. Methodol., 20(4):14:1–14:64, 2011.                    Polsat: A portfolio LTL satisfiability solver. CoRR, abs/1311.1602, 2013.
[12] Roderick Bloem, Barbara Jobstmann, Nir Piterman, Amir Pnueli, and Yaniv Sa’ar.            [36] Jianwen Li, Shufang Zhu, Geguang Pu, and Moshe Y Vardi. SAT-based explicit
     Synthesis of reactive(1) designs. J. Comput. Syst. Sci., 78(3):911–938, 2012.                  LTL reasoning. In Haifa Verification Conference, pages 209–224. Springer, 2015.
[13] Davide G Cavezza and Dalal Alrajeh. Interpolation-based GR(1) assumptions re-             [37] Wenchao Li, Lili Dworkin, and Sanjit A Seshia. Mining assumptions for synthesis.
     finement. In International Conference on Tools and Algorithms for the Construction             In Ninth ACM/IEEE International Conference on Formal Methods and Models for
     and Analysis of Systems, pages 281–297. Springer, 2017.                                        Codesign (MEMPCODE2011), pages 43–50. IEEE, 2011.
[14] Krishnendu Chatterjee, Thomas A. Henzinger, and Barbara Jobstmann. Environ-               [38] Zohar Manna and Amir Pnueli. The Temporal Logic of Reactive and Concurrent
     ment assumptions for synthesis. In Franck van Breugel and Marsha Chechik,                      Systems. Springer-Verlag New York, Inc., New York, NY, USA, 1992.
     editors, CONCUR 2008 - Concurrency Theory, pages 147–161, Berlin, Heidelberg,             [39] Zohar Manna and Amir Pnueli. Temporal verification of reactive systems: safety.
     2008. Springer Berlin Heidelberg.                                                              Springer-Verlag New York, Inc., New York, NY, USA, 1995.
[15] George Chatzieleftheriou, Borzoo Bonakdarpour, Panagiotis Katsaros, and Scott A.          [40] Zohar Manna and Pierre Wolper. Synthesis of communicating processes from
     Smolka. Abstract model repair. Log. Methods Comput. Sci., 11(3), 2015.                         temporal logic specifications. ACM Trans. Program. Lang. Syst., 6(1):68–93, 1984.
[16] A. Cimatti, M. Roveri, V. Schuppan, and A. Tchaltsev. Diagnostic information              [41] Shahar Maoz, Jan Oliver Ringert, and Rafi Shalom. Symbolic repairs for GR(1)
     for realizability. In Proc. of the 9th Intl. Conf. on Verification, Model Checking, and        specifications. In Proceedings of the 41st International Conference on Software
     Abstract Interpretation, pages 52–67, 2008.                                                    Engineering, ICSE 2019, Montreal, QC, Canada, pages 1016–1026, 2019.
[17] Edmund M. Clarke, Orna Grumberg, and Doron Peled. Model checking. MIT                     [42] S. Mechtaev, J. Yi, and A. Roychoudhury. Directfix: Looking for simple pro-
     Press, 2001.                                                                                   gram repairs. In 2015 IEEE/ACM 37th IEEE International Conference on Software
[18] Renzo Degiovanni, Dalal Alrajeh, Nazareno Aguirre, and Sebastián Uchitel. Au-                  Engineering, volume 1, pages 448–458, 2015.
     tomated goal operationalisation based on interpolation and sat solving. In ICSE,          [43] Philipp J. Meyer, Salomon Sickert, and Michael Luttenberger. Strix: Explicit
     pages 129–139, 2014.                                                                           reactive synthesis strikes back! In Computer Aided Verification - 30th International
[19] Renzo Degiovanni, Pablo F. Castro, Marcelo Arroyo, Marcelo Ruiz, Nazareno                      Conference, CAV 2018, Held as Part of the Federated Logic Conference, FloC 2018,
     Aguirre, and Marcelo F. Frias. Goal-conflict likelihood assessment based on                    Oxford, UK, July 14-17, 2018, Proceedings, Part I, pages 578–586, 2018.
     model counting. In Proceedings of the 40th International Conference on Software           [44] Z. Michalewicz. Genetic Algorithms + Data Structures = Evolution Programs.
     Engineering, ICSE 2018, Gothenburg, Sweden, pages 1125–1135, 2018.                             Springer, 1996.
[20] Renzo Degiovanni, Facundo Molina, Germán Regis, and Nazareno Aguirre. A                   [45] Nir Piterman, Amir Pnueli, and Yaniv Sa’ar. Synthesis of reactive(1) designs. In
     genetic algorithm for goal-conflict identification. In Proceedings of the 33rd                 VMCAI, pages 364–380, 2006.
     ACM/IEEE International Conference on Automated Software Engineering, ASE 2018,            [46] A. Pnueli and R. Rosner. On the synthesis of a reactive module. In Proceedings
     Montpellier, France, September 3-7, 2018, pages 520–531, 2018.                                 of the 16th ACM SIGPLAN-SIGACT Symposium on Principles of Programming
[21] Renzo Degiovanni, Nicolás Ricci, Dalal Alrajeh, Pablo F. Castro, and Nazareno                  Languages, POPL ’89, pages 179–190, New York, NY, USA, 1989. ACM.
     Aguirre. Goal-conflict detection based on temporal satisfiability checking. In            [47] Vasumathi Raman and Hadas Kress-Gazit. Explaining impossible high-level robot
     Proceedings of the 31st IEEE/ACM International Conference on Automated Software                behaviors. Trans. Rob., 29(1):94–104, February 2013.
     Engineering, ASE 2016, Singapore, September 3-7, 2016, pages 507–518, 2016.               [48] Viktor Schuppan. Towards a notion of unsatisfiable cores for LTL. In Farhad
[22] Nicolás D’Ippolito, Víctor A. Braberman, Nir Piterman, and Sebastián Uchitel.                  Arbab and Marjan Sirjani, editors, Fundamentals of Software Engineering, pages
     Synthesizing nonanomalous event-based controllers for liveness goals. ACM                      129–145, Berlin, Heidelberg, 2010. Springer Berlin Heidelberg.
     Trans. Softw. Eng. Methodol., 22(1):9, 2013.                                              [49] Shubham Sharma, Subhajit Roy, Mate Soos, and Kuldeep S. Meel. Ganak: A
[23] Matthew B. Dwyer, George S. Avrunin, and James C. Corbett. Patterns in property                scalable probabilistic exact model counter. In Proceedings of the Twenty-Eighth
     specifications for finite-state verification. In ICSE, pages 411–420, 1999.                    International Joint Conference on Artificial Intelligence, IJCAI-19, pages 1169–1176.
[24] E. Allen Emerson and Edmund M. Clarke. Using branching time temporal logic                     International Joint Conferences on Artificial Intelligence Organization, 7 2019.
     to synthesize synchronization skeletons. Sci. Comput. Program., 2(3):241–266,             [50] Marc Thurley. sharpsat - counting models with advanced component caching
     1982.                                                                                          and implicit BCP. In Theory and Applications of Satisfiability Testing - SAT 2006,
[25] Bernd Finkbeiner and Hazem Torfah. Counting models of linear-time temporal                     9th International Conference, Seattle, WA, USA, August 12-15, 2006, Proceedings,
     logic. In Adrian Horia Dediu, Carlos Martín-Vide, José Luis Sierra-Rodríguez,                  pages 424–429, 2006.
     and Bianca Truthe, editors, Language and Automata Theory and Applications - 8th           [51] Axel van Lamsweerde. Requirements Engineering - From System Goals to UML
     International Conference, LATA 2014, Madrid, Spain, March 10-14, 2014. Proceedings,            Models to Software Specifications. Wiley, 2009.
     volume 8370 of Lecture Notes in Computer Science, pages 360–371. Springer, 2014.          [52] Axel van Lamsweerde and Emmanuel Letier. Handling obstacles in goal-oriented
[26] Gordon Fraser, Franz Wotawa, and Paul Ammann. Testing with model checkers:                     requirements engineering. IEEE Trans. Softw. Eng., 26(10):978–1005, October
     a survey. Softw. Test., Verif. Reliab., 19(3):215–261, 2009.                                   2000.
[27] D. Goldberg. Genetic Algorithms in Search, Optimization and Machine Learning.             [53] András Vargha and Harold D. Delaney. A Critique and Improvement of the
     Addison-Wesley, 1989.                                                                          "CL" Common Language Effect Size Statistics of McGraw and Wong. Journal of
                                                                                                    Educational and Behavioral Statistics, 25(2):101–132, 2000.
