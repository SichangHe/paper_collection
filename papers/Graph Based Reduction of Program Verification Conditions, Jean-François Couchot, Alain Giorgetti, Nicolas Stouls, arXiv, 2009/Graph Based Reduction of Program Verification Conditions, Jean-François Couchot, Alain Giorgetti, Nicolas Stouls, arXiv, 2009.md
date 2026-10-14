                                       Graph-based Reduction of Program Verification Conditions

                                                         J.-F. Couchot                           A. Giorgetti                        N. Stouls
                                                              LIFC                         INRIA CASSIS / LIFC               AMAZONES INRIA / CITI
                                                  University of Franche-Comté           University of Franche-Comté                INSA Lyon
                                                      F-25030 Besançon                      F-25030 Besançon                  F-69621 Villeurbanne
                                                     couchot@lifc.univ-                   alain.giorgetti@univ-              Nicolas.Stouls@insa-
                                                         fcomte.fr                              fcomte.fr                           lyon.fr
arXiv:0907.1357v1 [cs.LO] 8 Jul 2009




                                       ABSTRACT                                                          verification conditions (VCs) that, when proved, establish
                                       Increasing the automaticity of proofs in deductive verifica-      that the program satisfies its assertions. In the KeY sys-
                                       tion of C programs is a challenging task. When applied            tem [2] a special purpose logic and calculus are used to prove
                                       to industrial C programs known heuristics to generate sim-        these verification conditions. The drawback of this approach
                                       pler verification conditions are not efficient enough. This       is has it is specific to a programming language and a target
                                       is mainly due to their size and a high number of irrelevant       prover. In contrast, a multi-prover approach is followed by
                                       hypotheses.                                                       effective tools such as ESC/Java [10] for Java programs an-
                                                                                                         notated using the Java Modeling Language [4], Boogie [1]
                                       This work presents a strategy to reduce program verification      for the C# programming language, and Caduceus/Why [12]
                                       conditions by selecting their relevant hypotheses. The rele-      for C programs. The latter also offers Java as input pro-
                                       vance of a hypothesis is determined by the combination of a       gramming language.
                                       syntactic analysis and two graph traversals. The first graph
                                       is labeled by constants and the second one by the predicates      A theorem prover is invoked to establish the validity of each
                                       in the axioms. The approach is applied on a benchmark             verification condition. One of the challenges in deductive
                                       arising in industrial program verification.                       software verification is to automatically discharge as many
                                                                                                         verification conditions as possible. A key issue is that the
                                       Categories and Subject Descriptors                                whole context of a verification condition is a huge set of
                                       D.2.4 [Software Engineering]: Software/Program Verifi-            axioms modelling not only the property and the program
                                       cation                                                            under verification, but also many features of the program-
                                                                                                         ming language. Simply passing this large context to an auto-
                                                                                                         mated prover induces a combinatorial explosion, preventing
                                       General Terms                                                     the prover from terminating in reasonable time.
                                       Verification, Experimentation
                                                                                                         Possible solutions to reduce the VC size and complexity are
                                       Keywords                                                          to optimize the memory model (e.g. by introducing sepa-
                                       Proof, hypothesis selection                                       rations of zones of pointers [16]), to improve the weakest
                                                                                                         precondition calculus [17] and to apply strategies for simpli-
                                       1.   INTRODUCTION                                                 fying VCs [14, 8, 18]. This work focuses on the latter. We
                                       Deductive software verification aims at verifying program         suggest heuristics to select axioms to feed automated theo-
                                       properties with the help of theorem provers. It has gained        rem provers (ATPs). Instead of blindly invoking ATPs with
                                       more interest with the increased use of software embedded         a large VC, we present reduction strategies that significantly
                                       in, for instance, airplanes commands, cars or smart cards,        prune their search space. The idea behind these strategies is
                                       requiring a high-level of confidence.                             quite natural: an axiom is relevant if a prover applies it suc-
                                                                                                         cessfully, i.e. without diverging, to establish the conclusion.
                                       In the Hoare logic framework, program properties are ex-          Relevance criteria are computed by the combined traver-
                                       pressed by first-order logical assertions on program variables    sal of two graphs representing symbol dependencies within
                                       (preconditions, postconditions, invariants, . . . ). The deduc-   axioms. In the graph of constants edges represent the con-
                                       tive verification method consists in transforming a program,      joint presence of two constants in some ground axiom. In
                                       annotated with sufficiently many assertions, into so-called       the graph of predicates arcs represent logical dependencies
                                                                                                         between predicates occuring in the same axiom.

                                                                                                         In former work [5], selection was limited to ground hypothe-
                                                                                                         ses and comparison predicates were not taken into account.
                                                                                                         This led to unsatisfactory results, for instance when the con-
                                                                                                         clusion is some equality between terms. The present work
                                                                                                         extends selection to context axioms, comparison predicates
                                                                                                         and hypotheses with quantifiers. We propose new heuristics
                                                                                                         that increase the number of automatically discharged VCs.
The plan of the article is as follows. Section 2 presents the                                              Goal
                                                                                      z                     }|                 {
industrial C example that has motivated this work. This
case study is a part of the Oslo [3] secure bootloader an-            Context    ⇒        Hypotheses        ⇒     Conclusion
notated with a safety property. Section 3 presents the gen-
eral structure of a verification condition. Section 4 shows           |            {z                  }
how dependencies are stored in graphs. The selection strat-                      Axioms
egy of hypotheses is presented in Section 5. These last two
sections are the first contribution. The second contribu-
                                                                     Figure 1: Structure of verification conditions
tion is the implementation of this strategy as a module of
Caduceus/Why [12]. Section 6 presents experimentation
results. Section 7 discusses related work, concludes and
presents future work.
                                                                  types or a memory model, enriched to allow the specification
2.   TRUSTED PLATFORM CASE STUDY                                  of, e.g. separated pointer regions. For instance, a typical VC
Some new challenges for axiom filtering are posed by the          produced by Caduceus/Why has a context with more than
context of the PFC project on Trusted Computing (TC).             80 axioms.
PFC (meaning trusted platforms in French) is one of the
SYSTEM@TIC Paris Region French cluster projects. The              VCs are generated in the input format of many first-order
main idea of the TC approach is to gain some confidence           ATPs, among which Simplify [9] and SMT solvers [6]. The
about the execution context of a program. This confidence         Simplify automatic prover has a specific input language.
is obtained by construction, by using a trusted chain. A          SMT solvers such as Alt-Ergo and Yices have a common
trusted chain is a chain of executions where each launched        input language. Alt-Ergo is however addressed in the Why
program is previously registered with a tamperproof compo-        input language for more efficiency. For SMT solvers, the
nent, such as the Trusted Platform Module (TPM) hardware          context is presented as a base theory, usually a combination
chipset. In this context of TC, we focus on the Oslo [3] se-      of equality with uninterpreted function symbols and linear
cure loader. This program is the first step of a trusted chain.   arithmetic, extended with a large set of specific axioms.
It uses some hardware functionalities of recent CPUs (AMD-
V or Intel-TET technologies) to initialize the chain and to       The goal depends on the program and on the property under
launch the first program of the chain.                            verification. When this property is an assertion about a
                                                                  given program control point, the goal is generated by the
The main trusted chain properties are temporal, but some          weakest precondition (wp) calculus of Dijkstra [11] at that
recent works [13, 15] propose a method to translate a tem-        control point. The goal is considered as a conclusion implied
poral property into first-order logic annotations in the code.    by hypotheses that encode the program execution up to the
This method is systematic and generates a large amount of         control point.
VCs, including quantifications and arrays with many links
between them. Therefore, this approach is a good gener-
ator for VCs with a medium or low level of automaticity.
Table 1 gives some factual information about the studied          Running example. Consider the following function:
part of Oslo. The VCs of this benchmark are publicly avail-
able [24].

 Oslo program and specification
 Code          ≈ 1500 lines                                       struct p {
 Specification ≈ 1500 lines (functional)                           int x;
 Number of VCs ≈ 7300 VCs                                         } p;
 Observed part of Oslo
 Observed code = 218 lines                                        struct t {
 Specification ≈ 1400 lines (functional and generated)             struct p v[2];
 Number of VCs = 771 VCs                                          } t;
  Table 1: Some Metrics about the Oslo Program                    /*@ requires \valid(a) &&
                                                                    @ (\forall int i; 0<=i<=1 => \valid(a->v[i]))
3.   VERIFICATION CONDITIONS                                        @ assigns a->v[0].x */
The verification conditions (VC) we consider are first order      void f(struct t *a) {
formulae whose validity implies that a piece of annotated          a->v[0].x = 2;
source code satisfies some property. This section describes       }
the general structure of VCs generated by Caduceus/Why.
A VC is composed of a context and a goal. This structure is
illustrated in Fig. 1.

The context depends on the programming language. It is            The requires annotation specifies a precondition and the
a first-order axiomatization of the language features used        assigns annotation means that function f modifies no other
in the program under verification. Typical features are data      location than a->v[0].x. The hypotheses of the generated
VC are                                                                  and c when c is tj if tj is a constant and when c is the fresh
     valid(a),                                                          constant created for tj if tj is a compound term (1 ≤ j ≤ n).
     (∀i : int . 0 ≤ i ≤ 1 ⇒ valid(a, shift(acc(mv , a), i)) ∧          Running example. An excerpt of the graph representing
       valid acc(mpPM )),                                               the VC presented in Section 3 is given in Fig. 2. The vertices
     valid acc range(mv , 2),                                           shift 6 and acc 7 come from the second hypothesis and the
     separation1 range(mv , 2),                                         other vertices come from the conclusion (C).
     valid acc(mv ),
     r = acc(mv , a),
     r0 = shift(r, 0), and                                                                       upd 1
     mx 0 = upd(mx , r0 , 2).
The conclusion is
         not assigns(mx , mx 0, singleton(acc(mv , a))).                      singleton 4                  shift 2          shift 6
                                                  PSfrag replacements
The meaning of these formulae is as follows. mpPM is the
                                                                  m
pointer (P ) memory (M ) for the structures of type p. valid - pP M
acc(m) means that the memory m is initialized, i.e. that acc 6                 acc 5          mx              acc 3          acc 7
this memory is accessible from any valid pointer in the al-
location table. The first two hypotheses correspond to the
precondition. In the next two hypotheses the predicates
valid acc range(mv , 2) and separation1 range(mv , 2) respec-
                                                                                                                mv
tively mean that any access to the memory mv returns an ar-
ray t such that pointers t[0] and t[1] are valid and t[0] 6= t[1].
The last three hypotheses come from a flattening-like decom-
position of the statement a->v[0].x = 2 performed by the
VC generator. The function shift(t, i) allows access to the                                                a
index i in the array t. The conclusion translates the assigns
annotation into a relation between two memory values. mx
is the value of memory x before execution of f and mx 0 is
                                                                     Figure 2: Example of Constant Dependency Graph
its value after execution of f. The third parameter is the
representation of a->v[0]. Our preprocessor eliminates the
last three hypotheses and the intermediary constants that            4.2 Predicate Dependency
they introduce by considering that the conclusion is                 A weighted directed graph is constructed to represent im-
                                                                     plication relations between predicates in an efficient way.
     not assigns(mx , upd(mx , shift(acc(mv , a), 0), 2),
                                                             (C)     Intuitively, each graph vertex represents a predicate name
        singleton(acc(mv , a))).
                                                                     and an arc from a vertex p to a vertex q means that p may
                                                                     imply q. What follows are details on how to compute this
4. GRAPH-BASED DEPENDENCY                                            graph of predicates, named GP . This section describes the
Basically, a conclusion is a propositional combination of po-        general approach. The next section adds a special treatment
tentially quantified predicates over some terms. Dependen-           for comparison predicates.
cies between axioms and the conclusion can then arise from
terms and predicates. Terms in the goal may either come              First, each context axiom is decomposed into a conjunctive
from the annotated program (from statements or assertions)           normal form (CNF). It is done in a straightforward way (in
or may result from a weakest precondition calculus applied           contrast to optimised CNF decomposition [19]): axioms are
to the program and its assertions. The term dependency just          of short size and their transformation into CNF does not
transcribes that parts of the goal (in particular, hypotheses        yield a combinatorial explosion. The resulting clauses are
and conclusion) share common terms. It is presented in               called axiom clauses. Each graph vertex is labeled with a
Section 4.1. Two predicates are dependent if there is a de-          predicate symbol that appears in at least one literal of the
ductive path leading from one to the other. The predicate            context. If a predicate p appears negated (as ¬p) in an
dependency is presented in Section 4.2. Finally, Section 4.3         axiom clause, it is represented by a vertex labeled with p.
presents a special dependency analysis for comparison pred-          A clause is considered as a set of literals. For each axiom
icates.                                                              clause Cl and each pair (l, l′ ) ∈ Cl × Cl of distinct literals in
                                                                        this clause, there is an arc in GP depending on the polarity
4.1 Term Dependency                                                     of l and l′ . There are three distinct cases modulo symmetry
In order to describe how hypotheses connect terms together              to consider. They are enumerated in Table 2, where p and
and according to previous work [5], an undirected connected             q are two distinct predicates. To reduce the graph size, the
graph Gc is constructed by syntactic analysis of term occur-            contraposite of each implication is not represented as an arc
rences in each hypothesis of a VC. The graph vertices are la-           in the graph but is considered when traversing it, as detailed
beled with the constants occurring in the goal and with new             in Section 5.2.
constants resulting from the following flattening-like process.
A fresh constant f i where i is some unique integer is cre-             The intended meaning of an arc weight is that the lower the
ated for each term f (t1 , . . . , tn ) in the goal. There is a graph   weight is, the higher the probability to establish q from p
edge between the two vertices labeled with the constants f i            is. Therefore, the arc introduced for the pair (p, q) along
                          Value of the (l, l′ ) pair                 Arcs
                                  (¬p, q)                          {p −→ q}                                      x≤y∧y ≤x ⇒ x=y                                  (1)
                                   (p, q)                          {p −→ q}                                          x=y ⇒ x≥y                                   (2)
                                 (¬p, ¬q)                          {p −→ q}                                          x=y ⇒ y≥x                                   (3)
                                                                                                                          x>y     ⇒ x≥y                          (4)
                 Table 2: Translating Pairs of Literals into Arcs.                                                        x≥y     ⇒ x>y∨x=y                      (5)


                                                     valid                                         Figure 4: Some Axioms Relating Comparison Pred-
                                                                                                   icates
                                             1         2
                          2                                    1        3

                                         valid acc                                                 support of types and the exploitation of some causalities
                                                                                                   between comparison predicates.
                                1                                  not assigns
                                         1       2                                                 4.3.1 Typed comparisons
                                                                    3           1         3        Each comparison predicate ◦ is written ◦t where ◦ is =, 6=,
g replacements      valid acc                                                                      ≤, <, ≥ or > and t is the type of the ◦ operands. For
                                     2                         not in pset                         simplicity, the focus is on the types t where ≤t and ≥t are
                                1                          3                                       total orders, >t and <t are their respective reverse orders,
                                         valid                                                     and ≤t is the union of <t and =t . A typical example is the
                                                                                                   type int of integers.
                                         3                                  not in pset
                                                 1                                                 Each comparison t1 ◦t t2 present in at least one axiom is
                                                                    1
                                                                            3                      represented by two nodes respectively labeled with ◦t and
                                      not assigns                                                  ◦t , where =t , 6=t , ≤t , <t , ≥t , and >t respectively are 6=t ,
                                                                                                   =t , >t , ≥t , <t , and ≤t . For instance, the two nodes ≤int
                                                                                                   and >int represent a total order on integers and its negation.
             Figure 3: Example of Predicate Dependency Graph                                       These labels are called the typed comparison predicates.

                                                                                                   Apart from this difference in the definition of ◦t , the arcs
                                                                                                   connected to typed comparison predicates are constructed
             Table 2 is labeled with the number of predicates minus one                            following the general rules described in Table 2.
             (card(Cl) − 1) in the clause Cl under consideration. For
             instance, a large clause with many negative literals, with
             ¬p among them, and with many consequents, with q among                                4.3.2 Causalities between comparison predicates
             them, is less useful for a deduction step leading to q than the                       Verification conditions are expressed as SMT problems in
             smaller clause {¬p, q}. Finally, two weighted arcs p −→
                                                                       w1
                                                                           q                       AUFLIA logics [22]. Since the comparison predicates be-
                     w                                                              min(w1 ,w2 )   tween integers are interpreted in AUFLIA, no context ax-
                    2
             and p −→ q are replaced with the weighted arc p −−−−−−→                               iom contributes to their definition. Figure 4 suggests such a
             q.                                                                                    list of axioms. To lighten the figure, the predicates are not
                                                                                                   indexed with int.
             Running example. Figure 3 represents the dependency
             graph corresponding to the definition of predicates valid,
                                                                                                   Adding these axioms to the context would be counterpro-
             not assigns and valid acc. It is an excerpt of the graph rep-
                                                                                                   ductive. We propose instead to analyze them to enrich the
             resenting the memory model of Caduceus/Why.
                                                                                                   predicate graph as if they were in the context. Since the
                                                                                                   algorithm of axiom selection does not take loops into ac-
             4.3 Handling Comparison Predicates                                                    count, the sole arcs of interest in the predicate graph are
             In a former work [5], equalities and inequalities were ig-                            between distinct nodes. It is then impossible to proceed so
             nored when memorizing predicate dependencies. This leads                              on internal properties like reflexivity, irreflexivity, symmetry
             to unsatisfactory results when (in)equality is central for de-                        or transitivity. This is the reason why Figure 4 is limited
             duction, e.g. when the conclusion is some equality between                            to axioms between distinct predicates. The symmetric ax-
             terms. If we handle equality as the other predicates, the                             ioms where ≤ and < respectively replace ≥ and > are also
             process of Section 4.2 connects too many vertices with the                            treated but are not reproduced. The arcs resulting from the
             vertex labeled =. We have experienced that this reduction                             application of the rules of Table 2 to those ten axioms are
             of the graph diameter has a negative impact on the quality                            added to the graph of predicates.
             of selection.

             More generally the present section suggests a special con-                            5. AXIOM SELECTION
             struction of graph vertices and edges for comparison predi-                           Relevant axioms remain to be selected. Intuitively, an axiom
             cates. A comparison predicate is an equality =, an inequal-                           is relevant with respect to a conclusion if a proof that needs
             ity 6=, a (reflexive) order relation (≤ or ≥) or an irreflexive                       this axiom can be found. Variables and predicates included
             pre-order (> or <). The keys of this construction are the                             in a relevant axiom are also called relevant.
Section 5.1 shows how to select relevant constants in, Sec-       predicates are
tion 5.2 how to select relevant predicates and Section 5.3
                                                                         L0   =    {not assigns},
how to combine these results to select relevant axioms. A
selection strategy is presented as an algorithm in Section 5.4.          L1   =    L 0 ∪ {valid, not in pset, =},
                                                                         L2   =    L 1 ∪ {<int , valid acc, ≤int },
                                                                         L3   =    L 2 ∪ {valid acc, >int , 6=int , ≥int } and
5.1 Relevant Constants                                                   L4   =    L 3 ∪ {=, not in pset, valid, ≤int , =int }.
A node in the graph of constants Gc is identified with its
labeling constant. Let n be the diameter of the graph of          5.3 Selection of Relevant Axioms
constants Gc . Starting from the set C0 of constants in the       In this section, we present the main principles of the axiom
conclusion, a breadth-first search algorithm computes the         selection combining predicate and constant selection. A first
sets Ci of constants in Gc that are reachable from C0 with at     part describes hypothesis selection and a second one extends
most i steps (1 ≤ i ≤ n). Finally, `unreachable
                                       ´         constants are    the approach to axioms from the context.
added to the limit of the sequence Cn n∈N for completeness.                         ` ´
Let C∞ be the resulting set.                                      Let (L n )n∈N and Cn n∈N respectively be the sequences of
                                                                  relevant predicate and constant sets. Let i be a counter
To introduce more granularity in the computation of reach-        which represents the depth of predicate selection. Similarly,
able constants, we propose as a heuristic to insert nodes that    let j be a counter corresponding to the depth of constant
are linked several times before nodes that are just linked        selection.
once. Semantically it gives priority to constants which are
closer to the conclusion. Notice that, in this case, the index    5.3.1 Hypothesis Selection
i of Ci does not correspond to a path length anymore.             Let Cl be a clause from a hypothesis. Let V be the set
                                                                  of constants of Cl augmented with constants resulting from
Running example. The sequence of reachable constants              flattening (see Section 4.1). Let P be the set of predicates of
sets associated to the graph in Fig. 2 is:                        Cl. The clause Cl should be selected if it includes constants
                                                                  or predicates that are relevant according to the conclusion.
            C0    =   {mx , mv , a},
                                                                  Different criteria can be used to verify this according to its
            C1    =   C0 ∪ {acc 3, acc 5, acc 7},
                                                                  sets P and V . Possible choices are, in increasing order of
            C2    =   C1 ∪ {singleton 4, shift 2},
                                                                  selectivity
            C3    =   C2 ∪ {shift 6},
            C4    =   C3 ∪ {upd 1} and
            C∞    =   C4 .                                          1. the clause includes at least one relevant constant or
                                                                       one relevant predicate:
                                                                                  V ∩ Cj 6= ∅ ∨ P ∩ L i 6= ∅
5.2 Relevant Predicates
A predicate p is identified with the vertex labeled p and its        2. the clause includes more than a threshold tv of rele-
negation with the vertex labeled p in the graph of predicates           vant constants or more than a threshold tp of relevant
GP . A predicate symbol p is relevant w.r.t. a predicate sym-           predicates:
bol q if there is a path from p to q in GP , or dually from q      card(V ∩ Cj )/card(Cj ) ≥ tv ∨ card(P ∩ L i )/card(L i ) ≥ tp
to p. Intuitively, the weaker the path weight is, the higher
the probability of p to establish q is. Relevant predicates         3. all the clause constants and clause predicates are rele-
extracted from GP are stored into an increasing sequence               vant:
(L n )n∈N of sets. The natural number n is the maximal                                 V ⊆ Cj ∧ P ⊆ L i
weight of paths considered in the graph of predicates.

We now present how L n is computed. The conclusion is             Our experiments on these criteria have shown that a too
assumed to be a single clause. L 0 gathers the predicates         weak criterion does not accomplish what it is designed for:
from the conclusion. For each predicate symbol p that is          too many clauses are selected for few iterations, making the
not in L 0 , a graph traversal computes the paths with the        prover quickly diverge. Thus, we only consider the strongest
minimal weight w from p to some predicate in L 0 .                criterion (3).

Furthermore, contraposition of each implication is consid-        We have also often observed the case where only a conjunc-
ered: let p1 and p2 be two node labels, corresponding either      tive part of a universally quantified hypothesis is relevant. In
                                                     w
to a positive or a negative literal. If the arc p1 −→ p2 is       that case, we split the conjunctive hypothesis into its parts
taken into account, its couterpart p2 −→ p1 is too, with the      and the filtering criterion is applied to the resulting predi-
convention that p is p. Let n be the minimal distance from        cates. A particular case is considered if a whole splittable
L 0 to the deepest reachable predicate. For 1 ≤ i ≤ n, L i is     hypothesis is relevant according to the criterion. Indeed, we
the set of vertices of GP whoseS distance to L 0 is less than     then consider the original formula, in order to preserve its
or equal to i. L ∞ is the limit i≥0 L i augmented with the        structure, which can be exploited by provers.
vertices from which L 0 is not reachable.
                                                                  5.3.2 Context Axioms
Running example. From the predicate graph of the run-             Consider now the case of selecting relevant axioms from the
ning example, depicted in Fig. 3 without the comparison           context. Intuitively, an axiom of the context has to be se-
predicates for lack of space, the first five sets of reachable    lected if one of the predicate relations it defines is relevant
 Parameters : VC, Prover, TO                                          2. If the formula is declared to be satisfiable, we may have
 6 // Prover call without VC reduction                                   omitted some axioms; we are then left to increment
 6
 6 Res := Prover(VC, T O)                                                either i or j, i.e. to enlarge either the set of selected
 6                                                                       predicates or the set of selected constants.
 6 if
 6 6  Res = timeout then
 6 6  i   := 1 + Min depth giving reachable preds (VC)                   However, allowing predicates has a more critical im-
 6 6 jmax := 1 + Min depth giving reachable vars (VC)
   6
 6 6 max                                                                 pact than allowing new constants, since constants do
 6 6
 6 6
 6 6 i := 0;                                                             not appear in context axioms. Therefore we recom-
 6 6 j := 0;
 6 6                                                                     mend to first increment j, increasing Cj until even-
 6 6 While Res 6= unsat ∧ i ≤ imax do                                    tually C∞ , before considering incrementing i. In this
 6 6 6
 6 6 6 // Prover call after VC reduction                                 later case, j resets to 0.
 6 6 6
 6 6 6 Res := Prover(selection(VC, i, j), T O)
 6 6 6 j := j + 1;
 6 6 6
                                                                      3. If the formula is not discharged in less than a given
 6 4 4 — j > jmax then
 6 6 6 if
 6         i := i + 1;                                                   time, after having iteratively incremented i and j, then
 4         j := 0;                                                       the algorithm terminates.
    return Res;
                                                                    6. EXPERIMENTS
Figure 5: General Algorithm Discharging a VC with                   The proposed approach is included in a global context of an-
Axiom Selection                                                     notated C program certification. A separation analysis that
                                                                    strongly simplifies the verification conditions generated by
                                                                    a weakest precondition calculus, and thus greatly helps to
for one hypothesis, i.e. the corresponding arc is used in the       prove programs with pointers has been proposed by T. Hu-
computation of L i . Practically, for each arc that is passed       bert and C. Marché [16]. Their approach is supported by
through while generating L i , we keep all the axioms of the        the Why tool. The pruning heuristics presented here are
context that have generated this arc.                               developed as a post-process of this tool.

5.4 Selection Strategy                                              Section 6.1 gives some implementation and experimentation
The selection strategy experimented in this work is described       details. Section 6.2 presents experimental results on an in-
in Fig. 5. The algorithm takes three parameters in input:           dustrial case study for trusted computing. This case study
                                                                    raises new challenges associated to the certification of C pro-
                                                                    grams annotated with a temporal logic formula. Section 6.3
   • a VC whose satisfiability has to be checked,                   finally gives results obtained on a public benchmark.
   • a satisfiability solver Prover, and
   • a maximal amount of time T O given by the user to the
                                                                    6.1 Methodology
                                                                    All the strategies presented in this work are implemented in
     satisfiability solver to discharge the VC.
                                                                    OCaml as modules in the Why [12] tool in less than 1700
                                                                    lines of code. Since these criteria are heuristics, their use
The algorithm starts with a first attempt to discharge the          is optional, and Why has command line arguments which
VC without axiom selection. It stops if this first result is        allow a user to enable or disable their use. In the current
unsatisfiable or satisfiable. Notice that in the latter case, re-   version, several others heuristics have been developed, which
moving axioms cannot modify the result. Otherwise, Prover           are not considered because their impact on the performance
is called following an incremental constant-first selection.        of Why seems to be less obvious. In order to use the pre-
                                                                    sented algorithms, the arguments to include in the Why call
The two natural numbers imax and jmax are depth bounds              are:
for L i and Cj computed during predicate graph and con-                - -prune-with-comp - -prune-context - -prune-coarse-pred-comp
stant graph traversals. Since we want to reach L ∞ and C∞ ,                              - -prune-vars-filter CNF
imax and jmax are initially computed by the tool as one plus
the minimal depth to obtain all reachable predicates and            The first parameter includes comparison predicates in the
constants. This is interpreted by the tool as the ∞ depth,          predicate dependency graph. The second one requires filter-
according to Sec. 5.2 and 5.1 (all predicates and constants         ing not only hypotheses but also axioms from the context.
of the graphs).                                                     The third one requires to ignore arc weights. This option
                                                                    gives better execution times on the Oslo benchmark. Fi-
The selection function implements the selection of axioms           nally, the fourth argument requires for rewriting hypotheses
(from context or hypotheses) according to the strongest cri-        into CNF before filtering.
terion (3). Discharging the resulting reduced VC into a
prover can yield three outcomes: satisfiable, unsatisfiable         The whole experiment is done on an Intel T8300@2.4GHz
or timeout.                                                         with 4Gb of memory, under a x86 64 Ubuntu Linux.


  1. If the formula is declared to be unsatisfiable, the pro-       6.2 Results of Oslo Verification
     cedure ends. Adding more axioms cannot make the                First of all, among the 771 generated VCs, 741 are directly
     problem satisfiable.                                           discharged, without any axiom selection. Next, the ap-
                                                                    proach developed in [5] increases the result to 752 VCs.
Among the remaining unproved VCs, some rely on quanti-           we have combined two separate dependency analyses based
fied hypotheses and others need comparison predicates that       on graph computation and graph traversal. Moreover, we
are not handled in the previous work [5]. They have moti-        have given some heuristics to analyse the graphs with a suf-
vated the present extensions, namely CNF reduction, com-         ficient granularity. Finally we have shown the relevance of
parison handling and context reduction. Thanks to these          this approach with a benchmark issued from a real industrial
improvements, 10 more VCs are automatically proved by us-        code.
ing the algorithm described in Fig. 5 with the three provers
Simplify, Alt-Ergo 0.8 and Yices 1.0.20 with a timeout T O       Strategies to simplify the prover’s task have been widely
of 10 seconds.                                                   studied since automated provers exist [28], mainly to pro-
                                                                 pose more efficient deductive systems [28, 27, 26]. The
The imax and jmax limits depend on the VCs. Their observed       KeY deductive system [2] is an extreme case. It is com-
values do not go beyond imax = 6 and jmax = 7. These limits      posed of a large list of special purpose rules dedicated to
express the number of versions in which the VCs have been        JML-annotated JavaCard programs. These rules make un-
cut. If edge weights are considered, then imax grows up to       necessary an explicit axiomatization of data types, memory
imax = 18 and the execution time is twice as long. Figure 6      model, and program execution. Priorities between deduc-
sums up these results.                                           tion rules help in effective reasoning. Beyond this, choosing
                                                                 rules in that framework requires as much effort as choosing
                                                                 axioms when targeting general purpose theorem provers.

                                                                 The present work can be compared with the set of support
                                                                 (sos) selection strategy [28, 20]. This approach starts with
                                                                 asking the user to provide an initial sos: it is classically the
                                                                 conclusion negation and a subset of hypotheses. It is then
                                                                 restricted to only apply inferences with at least one clause
                                                                 in the sos, consequences being added next into the sos. Our
                                                                 work can also be viewed as an automatic guess of the ini-
                                                                 tial sos guided by the formula to prove. In this sense, it is
                                                                 close to [18] where initial relevant clauses are selected ac-
                                                                 cording to syntactical criteria, i.e. counting matching rates
                                                                 between symbols of any clause and symbols of clauses issued
                                                                 from the conclusion. By considering syntactical filtering on
Figure 6: Result Comparison on Oslo Benchmark                    clauses issued from axioms and hypotheses, this latter work
(771 VCs)                                                        does not consider the relation between hypotheses, formal-
                                                                 ized by axioms of the theory: it provides a reduced forward
                                                                 proof. In contrast, by analyzing dependency graphs, we sim-
6.3 Public Why Benchmark                                         ulate natural deduction and are not far from backward proof
Our approach is developed in the Why tool, which trans-          search. By focusing on the predicative part of the verifica-
lates Why syntax into the input syntax of several proof assis-   tion condition, our objectives are dual to those developed
tants (Coq, HOL 4, HOL Light, Isabelle/HOL, Mizar, PVS)          in [14]: this work concerns boolean verification conditions
and automated theorem provers (Alt-Ergo, CVC3, Simplify,         with any boolean structure whereas we treat predicative for-
Yices, Z3). This section shows some experimental results on      mulae whose symbols are axiomatized in a quantified theory.
the Why public benchmark1 .                                      Even in a large set of context axioms, most of the time, each
                                                                 verification condition only requires a tiny portion of this con-
The Why benchmark is a public collection of VCs gener-           text. In [23, 7] a strategy to select relevant context axioms
ated by Caduceus or Krakatoa. These tools generate VCs           is presented, but it needs a preliminary manual task classi-
respectively from C and Java programs, according to CSL          fying axioms. Our predicate graph computation makes this
and JML specifications. Hence, it partially matches to our       axiom classification automatic. Recent advances have been
requirements, since our work is focusing on the verification     made in the direction of semantic selection of axioms [25,
of VCs generated by these tools. The only limitation is          21]. Briefly speaking, at each iteration, the selection of each
that our method is focusing on VCs with a large amount of        axiom depends on the fact whether a computed valuation is
hypotheses, in contrast to the ones presented in this bench-     a model of the axiom or not. By comparison, our syntactical
mark.                                                            axiom selection is more efficient, indeed linear in the size of
                                                                 the input formula.
This benchmark is provided in two versions corresponding
to two different pre-processes. Our results are similar with     In a near future we plan to apply the strategy to other case
both versions. Alt-Ergo discharges 1260 VCs directly and         studies. We also plan to investigate the impact on execution
1297 VCs with axiom selection, while axiom selection adds        time of various strategies discharging the same list of verifi-
3 VCs to the 1310 VCs directly discharged by Simplify.           cation conditions. We want to confirm or infirm with other
                                                                 benchmarks that weighting predicate dependencies with a
7.     RELATED WORK AND CONCLUSION                               formula length has no positive impact on automaticity but
We have presented a new strategy to select relevant hypothe-     has a significant negative impact on the execution time. We
ses in formulae coming from program verification. To do so,      also plan to integrate selection strategies in the Why tool or
1                                                                in a target automated theorem prover.
    http://proval.lri.fr/why-benchmarks/
8.   ACKNOWLEDGMENTS                                                 Lecture Notes in Computer Science, pages 173–177.
This work is partially funded by the French Ministry of Re-          Springer, 2007.
search, thanks to the CAT (C Analysis Toolbox) RNTL             [13] A. Giorgetti and J. Groslambert. JAG: JML
(Reseau National des Technologies Logicielles), by the SYS-          Annotation Generation for Verifying Temporal
TEM@TIC Paris Region French cluster, thanks to the PFC               Properties. In Luciano Baresi and Reiko Heckel,
project (Plateforme de Confiance, trusted platforms), and            editors, Fundamental Approaches to Software
by the INRIA, thanks to the CASSIS project and the Ce-               Engineering, 9th International Conference, FASE
ProMi ARC. The authors also want to thank Christophe                 2006, volume 3922 of Lecture Notes in Computer
Ringeissen and the four anonymous referees for their insight-        Science, pages 373–376. Springer, 2006.
ful comments.                                                   [14] E. P. Gribomont. Simplification of boolean verification
                                                                     conditions. Theoretical Computer Science,
9.   REFERENCES                                                      239(1):165–185, 2000.
 [1] M. Barnett, K. R. M. Leino, and W. Schulte. The            [15] J. Groslambert and N. Stouls. Vérification de
     Spec# Programming System: An Overview. In                       propriétés LTL sur des programmes C par génération
     Construction and Analysis of Safe, Secure, and                  d’annotations. In AFADL’09, 2009. Short paper.
     Interoperable Smart Devices (CASSIS’04), volume            [16] T. Hubert and C. Marché. Separation analysis for
     3362 of Lecture Notes in Computer Science, pages                deductive verification. In Heap Analysis and
     49–69. Springer, 2004.                                          Verification (HAV’07), Braga, Portugal, Mar. 2007.
 [2] B. Beckert, R. Hähnle, and P. H. Schmitt, editors.        [17] K. R. M. Leino. Efficient weakest preconditions.
     Verification of Object-Oriented Software: The KeY               Information Processing Letters, 93(6):281–288, 2005.
     Approach. LNCS 4334. Springer-Verlag, 2007.                [18] J. Meng and L. Paulson. Lightweight relevance
 [3] Bernhard Kauer. OSLO: Improving the security of                 filtering for machine-generated resolution problems. In
     Trusted Computing. In 16th USENIX Security                      ESCoR: Empirically Successful Computerized
     Symposium, August 6-10, 2007, Boston, MA, USA,                  Reasoning, 2006.
     2007.                                                      [19] A. Nonnengart and C. Weidenbach. Computing Small
 [4] L. Burdy, Y. Cheon, D. Cok, M. Ernst, J. Kiniry,                Clause Normal Forms. In A. Robinson and
     G. T. Leavens, K. R. M. Leino, and E. Poll. An                  A. Voronkov, editors, Handbook of Automated
     overview of JML tools and applications. Technical               Reasoning, volume I, chapter 6, pages 335–367.
     Report NIII-R0309, Dept. of Computer Science,                   Elsevier Science, 2001.
     University of Nijmegen, 2003.                              [20] D. A. Plaisted and A. H. Yahya. A relevance
 [5] J.-F. Couchot and T. Hubert. A Graph-based Strategy             restriction strategy for automated deduction. Artificial
     for the Selection of Hypotheses. In FTP 2007 -                  Intelligence, 144(1-2):59–93, 2003.
     International Workshop on First-Order Theorem              [21] P. Pudlak. Semantic selection of premisses for
     Proving, Liverpool, UK, Sept. 2007.                             automated theorem proving. In G. Sutcliffe, J. Urban,
 [6] L. M. de Moura, B. Dutertre, and N. Shankar. A                  and S. Schulz, editors, CEUR Workshop Proceedings,
     tutorial on satisfiability modulo theories. In W. Damm          volume 257, pages 27–44, 2007.
     and H. Hermanns, editors, CAV, volume 4590 of              [22] S. Ranise and C. Tinelli. The Satisfiability Modulo
     Lecture Notes in Computer Science, pages 20–36.                 Theories Library (SMT-LIB).
     Springer, 2007.                                                 http://www.SMT-LIB.org, 2006.
 [7] D. Deharbe and S. Ranise. Satisfiability Solving for       [23] W. Reif and G. Schellhorn. Theorem proving in large
     Software Verification. Submitted in 2006. See http:             theories. In M. P. Bonacina and U. Furbach, editors,
     //www.loria.fr/~ranise/pubs/sttt-submitted.pdf.                 Int. Workshop on First-Order Theorem Proving,
 [8] E. Denney, B. Fischer, and J. Schumann. An empirical            FTP’97, pages 119–124. Johannes Kepler Universität,
     evaluation of automated theorem provers in software             Linz (Austria), 1997.
     certification. International Journal on Artificial         [24] N. Stouls. Hypotheses selection applied to trusted
     Intelligence Tools, 15(1):81–108, 2006.                         computing. http:
 [9] D. Detlefs, G. Nelson, and J. B. Saxe. Simplify: a              //perso.citi.insa-lyon.fr/nstouls/tools/oslo/.
     theorem prover for program checking. J. ACM,               [25] G. Sutcliffe and Y. Puzis. Srass - a semantic relevance
     52(3):365–473, 2005.                                            axiom selection system. In Springer, editor, Automated
[10] D. L. Detlefs, K. R. M. Leino, G. Nelson, and J. B.             Deduction - CADE-21, 21st International Conference
     Saxe. Extended static checking. Technical Report 159,           on Automated Deduction, Bremen, Germany, July
     Compaq Systems Research Center, Dec. 1998.                      17-20, 2007, Proceedings, volume 4603 of Lecture
     Available at http://www.hpl.hp.com/techreports/                 Notes in Computer Science, pages 295–310, 2007.
     Compaq-DEC/SRC-RR-159.html.                                [26] L. Wos. Conquering the meredith single axiom.
[11] E. W. Dijkstra. A discipline of programming. Series in          Journal of Automated Reasoning, 27(2):175–199, 2001.
     Automatic Computation. Prentice Hall Int., 1976.           [27] L. Wos and G. W. Pieper. The hot list strategy.
[12] J.-C. Filliâtre and C. Marché. The                            Journal of Automated Reasoning, 22(1):1–44, 1999.
     Why/Krakatoa/Caduceus platform for deductive               [28] L. Wos, G. A. Robinson, and D. F. Carson. Efficiency
     program verification. In 19th International Conference          and completeness of the set of support strategy in
     on Computer Aided Verification, volume 4590 of                  theorem proving. J. ACM, 12(4):536–541, 1965.
