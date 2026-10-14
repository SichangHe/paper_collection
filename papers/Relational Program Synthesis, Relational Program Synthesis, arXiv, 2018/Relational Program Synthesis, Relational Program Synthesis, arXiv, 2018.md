                                                                                                                                                                  1

                                         Relational Program Synthesis

                                         YUEPENG WANG, University of Texas at Austin, USA
                                         XINYU WANG, University of Texas at Austin, USA
                                         ISIL DILLIG, University of Texas at Austin, USA
arXiv:1809.02283v2 [cs.PL] 11 Sep 2018




                                         This paper proposes relational program synthesis, a new problem that concerns synthesizing one or more
                                         programs that collectively satisfy a relational specification. As a dual of relational program verification,
                                         relational program synthesis is an important problem that has many practical applications, such as automated
                                         program inversion and automatic generation of comparators. However, this relational synthesis problem
                                         introduces new challenges over its non-relational counterpart due to the combinatorially larger search space.
                                         As a first step towards solving this problem, this paper presents a synthesis technique that combines the
                                         counterexample-guided inductive synthesis framework with a novel inductive synthesis algorithm that is
                                         based on relational version space learning. We have implemented the proposed technique in a framework called
                                         Relish, which can be instantiated to different application domains by providing a suitable domain-specific
                                         language and the relevant relational specification. We have used the Relish framework to build relational
                                         synthesizers to automatically generate string encoders/decoders as well as comparators, and we evaluate our
                                         tool on several benchmarks taken from prior work and online forums. Our experimental results show that the
                                         proposed technique can solve almost all of these benchmarks and that it significantly outperforms EUSolver,
                                         a generic synthesis framework that won the general track of the most recent SyGuS competition.
                                         CCS Concepts: • Software and its engineering → Programming by example; Automatic program-
                                         ming; • Theory of computation → Formal languages and automata theory;
                                         Additional Key Words and Phrases: Relational Program Synthesis, Version Space Learning, Counterexample
                                         Guided Inductive Synthesis.
                                         ACM Reference Format:
                                         Yuepeng Wang, Xinyu Wang, and Isil Dillig. 2018. Relational Program Synthesis. Proc. ACM Program. Lang. 1,
                                         CONF, Article 1 (January 2018), 33 pages.

                                         1   INTRODUCTION
                                         Relational properties describe requirements on the interaction between multiple programs or differ-
                                         ent runs of the same program. Examples of relational properties include the following:
                                             • Equivalence: Are two programs P 1 , P2 observationally equivalent? (i.e., ∀®            x . P1 (®
                                                                                                                                               x) = P 2 (®
                                                                                                                                                         x))
                                             • Inversion: Given two programs P1 , P2 , are they inverses of each other? (i.e., ∀x . P2 (P1 (x)) = x)
                                             • Non-interference: Given a program P with two types of inputs, namely low (public) input l®
                                                and high (secret) input h,® does P produce the same output when run on the same low input l®
                                                but two different high inputs h®1 , h®2 ? (i.e., ∀l,
                                                                                                  ® h®1 , h®2 . P(l,
                                                                                                                  ® h®1 ) = P(l,
                                                                                                                              ® h®2 ))
                                             • Transitivity: Given a program P that returns a boolean value, does P obey transitivity? (i.e.,
                                                ∀x, y, z. P(x, y) ∧ P(y, z) ⇒ P(x, z))
                                         Observe that the first two properties listed above relate different programs, while the latter two
                                         relate multiple runs of the same program.
                                            Due to their importance in a wide range of application domains, relational properties have
                                         received significant attention from the program verification community. For example, prior papers
                                         propose novel program logics for verifying relational properties [Barthe et al. 2012b; Benton 2004;
                                         Authors’ addresses: Yuepeng Wang, University of Texas at Austin, USA, ypwang@cs.utexas.edu; Xinyu Wang, University of
                                         Texas at Austin, USA, xwang@cs.utexas.edu; Isil Dillig, University of Texas at Austin, USA, isil@cs.utexas.edu.

                                         2018. 2475-1421/2018/1-ART1 $15.00
                                         https://doi.org/


                                                                         Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:2                                                              Yuepeng Wang, Xinyu Wang, and Isil Dillig

Chen et al. 2017; Sousa and Dillig 2016; Yang 2007] or transform the relational verification problem
to standard safety by constructing so-called product programs [Barthe et al. 2011, 2013, 2016].
   In this paper, we consider the dual synthesis problem of relational verification. That is, given
a relational specification Ψ relating runs of n programs P1 , . . . , Pn , our goal is to automatically
synthesize n programs that satisfy Ψ. This relational synthesis problem has a broad range of practical
applications. For example, we can use relational synthesis to automatically generate comparators
that provably satisfy certain correctness requirements such as transitivity and anti-symmetry. As
another example, we can use relational synthesis to solve the program inversion problem where the
goal is to generate a program P ′ that is an inverse of another program P [Hu and D’Antoni 2017;
Srivastava et al. 2011]. Furthermore, since many automated repair techniques rely on program
synthesis [Jobstmann et al. 2005; Nguyen et al. 2013], we believe that relational synthesis could
also be useful for repairing programs that violate a relational property like non-interference.
   Solving the relational synthesis problem introduces new challenges over its non-relational
counterpart due to the combinatorially larger search space. In particular, a naive algorithm that
simply enumerates combinations of programs and then checks their correctness with respect to the
relational specification is unlikely to scale. Instead, we need to design novel relational synthesis
algorithms to efficiently search for tuples of programs that collectively satisfy the given specification.
   We solve this challenge by introducing a novel synthesis algorithm that learns relational version
spaces (RVS), a generalization of the notion of version space utilized in prior work [Gulwani 2011; Lau
et al. 2003; Wang et al. 2017]. Similar to other synthesis algorithms based on counterexample-guided
inductive synthesis (CEGIS) [Solar-Lezama 2008], our method also alternates between inductive
synthesis and verification; but the counterexamples returned by the verifier are relational in nature.
Specifically, given a set of relational counterexamples, such as f (1) = д(1) or f (д(1), д(2)) = f (3),
our inductive synthesizer compactly represents tuples of programs and efficiently searches for their
implementations that satisfy all relational counterexamples.
   In more detail, our relational version space learning algorithm is based on the novel concept
of hierarchical finite tree automata (HFTA). Specifically, an HFTA is a hierarchical collection of
finite tree automata (FTAs), where each individual FTA represents possible implementations of the
different functions to be synthesized. Because relational counterexamples can refer to compositions
of functions (e.g., f (д(1), д(2))), the HFTA representation allows us to compose different FTAs
according to the hierarchical structure of subterms in the relational counterexamples. Furthermore,
our method constructs the HFTA in such a way that tuples of programs that do not satisfy the
examples are rejected and therefore excluded from the search space. Thus, the HFTA representation
allows us to compactly represent those programs that are consistent with the relational examples.
   We have implemented the proposed relational synthesis algorithm in a tool called Relish 1 and
evaluate it in the context of two different relational properties. First, we use Relish to automatically
synthesize encoder-decoder pairs that are provably inverses of each other. Second, we use Relish
to automatically generate comparators, which must satisfy three different relational properties,
namely, anti-symmetry, transitivity, and totality. Our evaluation shows that Relish can efficiently
solve interesting benchmarks taken from previous literature and online forums. Our evaluation
also shows that Relish significantly outperforms EUSolver, a general-purpose synthesis tool that
won the General Track of the most recent SyGuS competition for syntax-guided synthesis.
   To summarize, this paper makes the following key contributions:
     • We introduce the relational synthesis problem and take a first step towards solving it.
     • We describe a relational version space learning algorithm based on the concept of hierarchical
        finite tree automata (HFTA).
1 Relish stands for RELatIonal SyntHesis.



Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Relational Program Synthesis                                                                                       1:3

                         Property                      Relational specification
                        Equivalence                            ∀®x . f 1 (®
                                                                          x) = f 2 (®
                                                                                    x)
                       Commutativity                     ∀x . f 1 (f 2 (x)) = f 2 (f 1 (x))
                        Distributivity       ∀x, y, z. f 2 (f 1 (x, y), z) = f 1 (f 2 (x, z), f 2 (y, z))
                        Associativity             ∀x, y, z. f (f (x, y), z) = f (x, f (y, z))
                       Anti-symmetry       ∀x, y. (f (x, y) = true ∧ x , y) ⇒ f (y, x) = false
                   Fig. 1. Examples of relational specifications for five relational properties.

      • We show how to construct HFTAs from relational examples expressed as ground formulas
        and describe an algorithm for finding the desired accepting runs.
      • We experimentally evaluate our approach in two different application domains and demon-
        strate the advantages of our relational version space learning approach over a state-of-the-art
        synthesizer based on enumerative search.

2     OVERVIEW
In this section, we define the relational synthesis problem and give a few motivating examples.

2.1    Problem Statement
The input to our synthesis algorithm is a relational specification defined as follows:
   Definition 2.1 (Relational specification). A relational specification with functions f 1 , . . . , fn
is a first-order sentence Ψ = ∀®
                               x . ϕ(®
                                     x), where ϕ(®
                                                 x) is a quantifier-free formula with uninterpreted
functions f 1 , . . . , fn .
  Fig. 1 shows some familiar relational properties like distributivity and associativity as well as their
corresponding specifications. Even though we refer to Definition 2.1 as a relational specification,
observe that it allows us to express combinations of both relational and non-relational properties.
For instance, the specification ∀x . (f (x) ≥ 0 ∧ f (x) + д(x) = 0) imposes both a non-relational
property on f (namely, that all of its outputs must be non-negative) as well as the relational property
that the outputs of f and д must always add up to zero.
   Definition 2.2 (Relational program synthesis). Given a set of n function symbols F = { f 1 , . . . , fn },
their corresponding domain-specific languages {L 1 , . . . , Ln }, and a relational specification Ψ, the
relational program synthesis problem is to find an interpretation I for F such that:
    (1) For every function symbol fi ∈ F , I(fi ) is a program in fi ’s DSL Li (i.e., I(fi ) ∈ Li ).
    (2) The interpretation I satisfies the relational specification Ψ (i.e., I(f 1 ), . . . , I(fn ) |= Ψ).

2.2    Motivating Examples
We now illustrate the practical relevance of the relational program synthesis problem through
several real-world programming scenarios.
   Example 2.3 (String encoders and decoders). Consider a programmer who needs to implement
a Base64 encoder encode(x) and its corresponding decoder decoder(x) for any Unicode string x.
For example, according to Wikipedia 2 , the encoder should transform the string “Man” into “TWFu”,
“Ma” into “TWE=”, and “M” to “TQ==”. In addition, applying the decoder to the encoded string should
yield the original string. Implementing this encoder/decoder pair is a relational synthesis problem

2 https://en.wikipedia.org/wiki/Base64



                                 Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:4                                                              Yuepeng Wang, Xinyu Wang, and Isil Dillig

in which the relational specification is the following:
      encode(“Man”) = “TWFu” ∧ encode(“Ma”) = “TWE=” ∧ encode(“M”) = “TQ==”                 (input-output examples)
 ∧    ∀x . decode(encode(x)) = x                                                            (inversion)
Here, the first part (i.e., the first line) of the specification gives three input-output examples
for encode, and the second part states that decode must be the inverse of encode. Relish can
automatically synthesize the correct Base64 encoder and decoder from this specification using a
DSL targeted for this domain (see Section 6.2).
   Example 2.4 (Comparators). Consider a programmer who needs to implement a comparator
for sorting an array of integers according to the number of occurrences of the number 5 3 . Specifi-
cally, compare(x,y) should return -1 (resp. 1) if x (resp. y) contains less 5’s than y (resp. x), and
ties should be broken based on the actual values of the integers. For instance, sorting the array
[“24”,“15”,“55”,“101”,“555”] using this comparator should yield array [“24”,“101”,“15”,“55”,“555”].
Furthermore, since the comparator must define a total order, its implementation should satisfy
reflexivity, anti-symmetry, transitivity, and totality. The problem of generating a suitable compare
method is again a relational synthesis problem and can be defined using the following specification:
       compare(“24”, “15”) = -1 ∧ compare(“101”, “24”) = 1 ∧ . . .                       (input-output examples)
  ∧    ∀x . compare(x, x) = 0                                                            (reflexivity)
  ∧    ∀x, y. sgn(compare(x, y)) = −sgn(compare(y, x))                                   (anti-symmetry)
  ∧    ∀x, y, z. compare(x, y) > 0 ∧ compare(y, z) > 0 ⇒ compare(x, z) > 0               (transitivity)
  ∧    ∀x, y, z. compare(x, y) = 0 ⇒ sgn(compare(x, z)) = sgn(compare(y, z))             (totality)
   A solution to this problem is given by the following implementation of compare:
                    let a = intCompare (countChar x '5') (countChar y '5') in
                        if a != 0 then a else intCompare (toInt x) (toInt y)
where countChar function returns the number of occurrences of a character in the input string,
and intCompare is the standard comparator on integers.
   Example 2.5 (Equals and hashcode). A common programming task is to implement equals and
hashcode methods for a given class. These functions are closely related because equals(x,y)=true
implies that the hash codes of x and y must be the same. Relational synthesis can be used to
simultaneously generate implementations of equals and hashcode. For example, consider an
ExperimentResults class that internally maintains an array of numbers where negative integers
indicate an anomaly (i.e., failed experiment) and should be ignored when comparing the results
of two experiments. For instance, the results [23.5,-1,34.7] and [23.5,34.7] should be equal
whereas [23.5,34.7] and [34.7,23.5] should not. The programmer can use a relational synthe-
sizer to generate equals and hashcode implementations by providing the following specification:
                 equals([23.5,-1,34.7], [23.5,34.7]) = true                      (input-output examples)
            ∧    equals([23.5,34.7], [34.7,23.5]) = false ∧ . . .
            ∧    ∀x, y. equals(x, y) ⇒ (hashcode(x) = hashcode(y))               (equals-hashcode)
   A possible solution consists of the following pair of implementations of equals and hashcode:
                  equals(x,y) : (filter (>= 0) x) == (filter (>= 0) y)
                  hashcode(x) : foldl (\u.\v. 31 * (u + v)) 0 (filter (>= 0) x)

  Example 2.6 (Reducers). MapReduce is a software framework for writing applications that
process large datasets in parallel. Users of this framework need to implement both a mapper that
maps input key/value pairs to intermediate ones as well as a reducer which transforms intermediate
3 https://stackoverflow.com/questions/19231727/sort-array-based-on-number-of-character-occurrences



Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Relational Program Synthesis                                                                                        1:5

values that share a key to a smaller set of values. An important requirement in the MapReduce
framework is that the reduce function must be associative. Now, consider the task of using the
MapReduce framework to sum up sensor measurements obtained from an experiment. In particular,
each sensor value is either a real number or None, and the final result should be None if any sensor
value is None. In order to implement this functionality, the user needs to write a reducer that takes
sensor values x, y and returns their sum if neither of them is None, or returns None otherwise. We
can express this problem using the following relational specification:
             reduce(1, 2) = 3 ∧ reduce(1, None) = None                                   (input-output examples)
         ∧   ∀x, y, z. reduce(reduce(x, y), z) = reduce(x, reduce(y, z))                 (associativity)
The first part of the specification gives input-output examples to illustrate the desired functionality,
and the latter part expresses the associativity requirement on reduce. A possible solution to this
relational synthesis problem is given by the following implementation:
                                reduce(x,y) : if x == None then None
                                              else if y == None then None
                                              else x + y

3     PRELIMINARIES
Since the rest of this paper requires knowledge of finite tree automata and their use in program
synthesis, we first briefly review some background material.

3.1    Finite Tree Automata
A tree automaton is a type of state machine that recognizes trees rather than strings. More formally,
a (bottom-up) finite tree automaton (FTA) is a tuple A = (Q, Σ, Q f , ∆), where
      • Q is a finite set of states.
      • Σ is an alphabet.
      • Q f ⊆ Q is a set of final states.
      • ∆ ⊆ Q ∗ × Σ × Q is a set of transitions (or rewrite rules).
    Intuitively, a tree automaton A recognizes a term (i.e., tree) t if we can rewrite t into a final state
q ∈ Q f using the rewrite rules given by ∆.
    More formally, suppose we have a tree t = (V , E, vr ) where V is a set of nodes labeled with
σ ∈ Σ, E ⊆ V × V is a set of edges, and vr ∈ V is the root node. A run of an FTA A = (Q, Σ, Q f , ∆)
on t is a mapping π : V → Q compatible with ∆ (i.e., given node v with label σ and children
v 1 , . . . , vn in the tree, the run π can only map v, v 1 , . . . , vn to q, q 1 , . . . , qn if there is a transition
σ (q 1 , . . . , qn ) → q in ∆). Run π is said to be accepting if it maps the root node of t to a final state,
and a tree t is accepted by an FTA A if there exists an accepting run of A on t. The language L(A)
recognized by A is the set of all those trees that are accepted by A.
   Example 3.1. Consider a finite tree automaton A = (Q, Σ, Q f , ∆) with states Q = {q 0 , q 1 },
alphabet Σ = {0, 1, ¬, ∧}, final states Q f = {q 1 }, and transitions ∆:
                          1 → q1          0 → q0          ∧(q 0 , q 0 ) → q 0   ∧(q 0 , q 1 ) → q 0
                          ¬(q 0 ) → q 1   ¬(q 1 ) → q 0   ∧(q 1 , q 0 ) → q 0   ∧(q 1 , q 1 ) → q 1
   Intuitively, the states of this FTA correspond to boolean constants (i.e., q 0 , q 1 represent false and
true respectively), and the transitions define the semantics of the boolean connectives ¬ and ∧.
Since the final state is q 1 , the FTA accepts all boolean formulas (containing only ∧ and ¬) that
evaluate to true. For example, 1 ∧ ¬0 is accepted by A, and the corresponding tree and its accepting
run are shown in Fig. 2.

                                 Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:6                                                                        Yuepeng Wang, Xinyu Wang, and Isil Dillig

                   ein = (e 1 , . . . , en )
                                                 (Input)                                                               (Output)
             G, e ⊢ q xeii ∈ Q, x i → q xeii ∈ ∆                                      G, e ⊢ qse0out ∈ Q f

              (s → σ (s 1 , . . . , sn )) ∈ P   G, e ⊢ qsc11 ∈ Q, . . . , qscnn ∈ Q     c = Jσ (c 1 , . . . , c n )K
                                                                      c1            cn                                   (Prod)
                        G = (T , N , P, s 0 ), e ⊢     qsc ∈ Q,   σ (qs1 , . . . , qsn ) → qsc ∈ ∆
Fig. 3. Rules for constructing FTA A = (Q, Σ, Q f , ∆) given example e = (e in , e out ) and grammar G =
(T , N , P, s 0 ). The alphabet Σ of the FTA is exactly the terminals T of G.


3.2    Example-based Synthesis using FTAs
Since our relational synthesis algorithm leverages prior
work on example-based synthesis using FTAs [Wang                              tree
                                                                                      ∧
                                                                                             run
                                                                                                   q1
et al. 2017, 2018a], we briefly review how FTAs can be
used for program synthesis.                                                     1       ¬     q1        q1

   At a high-level, the idea is to build an FTA that ac-
cepts exactly the ASTs of those DSL programs that are                                   0               q0

consistent with the given input-output examples. The
states of this FTA correspond to concrete values, and Fig. 2. Tree for 1 ∧ ¬0 and its accepting run.
the transitions are constructed using the DSL’s seman-
tics. In particular, the FTA states correspond to output values of DSL programs on the input
examples, and the final states of the FTA are determined by the given output examples. Once this
FTA is constructed, the synthesis task boils down to finding an accepting run of the FTA. A key
advantage of using FTAs for synthesis is to enable search space reduction by allowing sharing
between programs that have the same input-output behavior.
   In more detail, suppose we are given a set of input-output examples e® and a context-free grammar
G describing the target domain-specific language. We assume that G is of the form (T , N , P, s 0 )
where T and N are the terminal and non-terminal symbols respectively, P is a set of productions of
the form s → σ (s 1 , · · · , sn ), and s 0 ∈ N is the topmost non-terminal (start symbol) in G. We also
assume that the program to be synthesized takes arguments x 1 , . . . , x n .
   Fig. 3 reviews the construction rules for a single example e = (e in , e out ) [Wang et al. 2018a]. In
particular, the Input rule creates n initial states q xe11 , . . . , q xenn for input example e in = (e 1 , . . . , en ).
We then iteratively use the Prod rule to generate new states and transitions using the productions
in grammar G and the concrete semantics of the DSL constructs associated with the production.
Finally, according to the Output rule, the only final state is qsc0 where s 0 is the start symbol and c
is the output example e out . Observe that we can build an FTA for a set of input-output examples
by constructing the FTA for each example individually and then taking their intersection using
standard techniques [Comon 1997].
Remark. Since the rules in Fig. 3 may generate an infinite
                                                                                 qx1 id qe1       +    qe2
set of states and transitions, the FTA is constructed by                            1
                                                                                                  +
applying the Prod rule a finite number of times. The
number of applications of the Prod rule is determined by                                               qe4
a bound on the AST depth of the synthesized program.                                              +

                                                                                              qx3     id q3                +      qe6
                                                                                                 2        e
  Example 3.2. Consider a very simple DSL specified by
the following CFG, where the notation s → s ′ is short-
hand for s → id(s ′) for a unary identity function id:                                Fig. 4. FTA for input-output (1, 3) → 4.

                        e → x1 | x2 | e + e

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Relational Program Synthesis                                                                                                 1:7

Suppose we want to find a program (of size at most 3) that is consistent with the input-output
example (1, 3) → 4. Using the rules from Fig. 3, we can construct A = (Q, Σ, Q f , ∆) with states Q =
{q x1 1 , q x3 2 , qe1 , qe2 , qe3 , qe4 , qe6 }, alphabet Σ = {x 1 , x 2 , id, +}, final states Q f = {qe4 }, and transitions ∆:

                       x 1 → q x1 1          x 2 → q x3 2          id(q x1 1 ) → qe1     id(q x3 2 ) → qe3
                       +(qe1 , qe1 ) → qe2   +(qe1 , qe3 ) → qe4   +(qe3 , qe1 ) → qe4   +(qe3 , qe3 ) → qe6

For example, the FTA contains the transition +(qe3 , qe1 ) → qe4 because the grammar contains a
production e → e + e and we have 3 + 1 = 4. Since it is sometimes convenient to visualize FTAs
as hypergraphs, Fig. 4 shows a hypergraph representation of this FTA, using circles to indicate
states, double circles to indicate final states, and labeled (hyper-)edges to represent transitions. The
transitions of nullary alphabet symbols (i.e. x 1 → q x1 1 , x 2 → q x3 2 ) are omitted in the hypergraph for
brevity. Note that the only two programs that are accepted by this FTA are x 1 + x 2 and x 2 + x 1 .

4    HIERARCHICAL FINITE TREE AUTOMATA
As mentioned in Section 1, our relational synthesis technique uses a version space learning algorithm
that is based on the novel concept of hierarchical finite tree automata (HFTA). Thus, we first introduce
HFTAs in this section before describing our relational synthesis algorithm.
   A hierarchical finite tree automaton (HFTA) is a tree in which each node is annotated with a
finite tree automaton (FTA). More formally, an HFTA is a tuple H = (V , Ω, vr , Λ) where
     • V is a finite set of nodes.
     • Ω is a mapping that maps each node v ∈ V to a finite tree automaton.
     • vr ∈ V is the root node.
     • Λ ⊆ States(Range(Ω)) × States(Range(Ω)) is a set of inter-FTA transitions.
   Intuitively, an HFTA is a tree-structured (or hierarchical) collection of FTAs, where Λ corresponds
to the edges of the tree and specifies how to transition from a state of a child FTA to a state of its
parent. For instance, the left-hand side of Fig. 5 shows an HFTA, where the inter-FTA transitions
Λ (indicated by dashed lines) correspond to the edges (v 3 , v 1 ) and (v 3 , v 2 ) in the tree.
   Just as FTAs accept trees, HFTAs accept hierarchical trees. Intuitively, as depicted in the right-hand
side of Fig. 5, a hierarchical tree organizes a collection of trees in a tree-structured (i.e., hierarchical)
manner. More formally, a hierarchical tree is of the form T = (V , ϒ, vr , E), where:
     • V is a finite set of nodes.
     • ϒ is a mapping that maps each node v ∈ V to a tree.
     • vr ∈ V is the root node.
     • E ⊆ V × V is a set of edges.
    We now define what it means for an HFTA to accept a hierarchical tree:

    Definition 4.1. A hierarchical tree T = (V , ϒ, vr , E) is accepted by an HFTA H = (V , Ω, vr , Λ) iff:
     • For any node v ∈ V , the tree ϒ(v) is accepted by FTA Ω(v).
     • For any edge (v, v ′) ∈ E, there is an accepting run π of FTA Ω(v) on tree ϒ(v) and an accepting
       run π ′ of Ω(v ′) on ϒ(v ′) such that there exists a unique leaf node l ∈ ϒ(v) where we have
       π ′ Root(ϒ(v ′)) → π (l) ∈ Λ.

   In other words, a hierarchical tree T is accepted by an HFTA H if the tree at each node v of T is
accepted by the corresponding FTA Ω(v) of H , and the runs of the individual FTAs can be “stitched”
together according to the inter-FTA transitions of H . The language of an HFTA H , denoted L(H ),
is the set of all hierarchical trees accepted by H .

                                    Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:8                                                                                          Yuepeng Wang, Xinyu Wang, and Isil Dillig

    v3        s⊤           s⊥
                                                     v3                                       v3                                        v3
          =        =   =        =                             =                                         S⊤                                       =
     u5       u6           w5       w6                  x1         x2                             u5          w5                           x1         x2

    v1                 v2
     q5       q6         r5         r6       v1                   v2                  v1     q5
                                                                                                             v2    r5           v1                   v2
                                                    +                   +                                                              +                   x
     +        x            +        x
                                               2          2
                                                          3        3          2         q2        q3          r3        r2       2           2
                                                                                                                                             3        3        2
     q2       q3           r3       r2

                   HFTA                           Hierarchical Tree T1                             FTA Runs                          Hierarchical Tree T2

Fig. 5. Example HFTA and hierarchical trees. Left-hand side shows HFTA H = (V , Ω, v 3 , Λ), where nodes
V = {v 1 , v 2 , v 3 } are represented by rectangles, and annotated FTAs are represented as hypergraphs inside
the corresponding rectangles. Specifically, circles in the hypergraph correspond to FTA states, double circles
indicate final states, and labeled (hyper-)edges correspond to transitions. Inter-FTA transitions Λ are repre-
sented as dashed lines. An example hierarchical tree T1 = (V , ϒ, v 3 , E) that is accepted by H is shown in the
middle, where nodes V = {v 1 , v 2 , v 3 } are represented by rectangles, the tree annotation ϒ(vi ) is depicted
inside the corresponding rectangle vi , and edges are E = {(v 3 , v 1 ), (v 3 , v 2 )}. “FTA runs” shows the runs of the
FTAs for each vi in H on the corresponding tree in T1 . On the right-hand side, we show another example of a
hierarchical tree T2 that is not accepted by H .

  Example 4.2. Consider the HFTA H = (V , Ω, v 3 , Λ) shown on the left-hand side of Fig. 5. This
HFTA has nodes V = {v 1 , v 2 , v 3 } annotated with FTAs as follows:
                                                   Ω = {v 1 7→ A1 , v 2 7→ A3 , v 3 7→ A3 }
where:
  A1 = ({q 2 , q 3 , q 5 , q 6 }, {2, 3, +, ×}, {q 5 , q 6 }, ∆1 ) with transitions ∆1 :
                                           2 → q2         3 → q3        +(q 2 , q 3 ) → q 5            ×(q 2 , q 3 ) → q 6
    A2 = ({r 2 , r 3 , r 5 , r 6 }, {2, 3, +, ×}, {r 5 , r 6 }, ∆2 ) with transitions ∆2 :
                                            2 → r2        3 → r3            +(r 3 , r 2 ) → r 5        ×(r 3 , r 2 ) → r 6
    A3 = ({u 5 , u 6 , w 5 , w 6 , s ⊤ , s ⊥ }, {x 1 , x 2 , =}, {s ⊤ }, ∆3 ) with transitions ∆3 :
                                         x1 → u5     x1 → u6            = (u 5 , w 5 ) → s ⊤             = (u 6 , w 5 ) → s ⊥
                                         x2 → w5     x2 → w6            = (u 5 , w 6 ) → s ⊥             = (u 6 , w 6 ) → s ⊤
Finally, Λ includes the following four transitions:
                                           q5 → u5            q6 → u6                  r5 → w5                     r6 → w6
    Intuitively, this HFTA accepts ground first-order formulas of the form t 1 = t 2 where t 1 (resp. t 2 )
is a ground term accepted by A1 (resp. A2 ) such that t 1 and t 2 are equal. For example, t 1 = 2 + 3
and t 2 = 3 + 2 are collectively accepted. However, t 1 = 2 + 3 and t 2 = 3 × 2 are not accepted because
t 1 is not equal to t 2 . Fig. 5 shows a hierarchical tree T1 that is accepted by H and another one T2
that is rejected by H .

5        RELATIONAL PROGRAM SYNTHESIS USING HFTA
In this section, we describe the high-level structure of our relational synthesis algorithm and explain
its sub-procedures in the following subsections.
   Our top-level synthesis algorithm is shown in Algorithm 1. The procedure Synthesize takes
as input a tuple of function symbols F = (f 1 , . . . , fn ), their corresponding context-free grammars
G = (G 1 , . . . , G n ), and a relational specification Ψ = ∀®x . ϕ(®
                                                                     x). The output is a mapping P from
each function symbol fi to a program in grammar G i such that these programs collectively satisfy
the given relational specification Ψ, or null if no such solution exists.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Relational Program Synthesis                                                                                        1:9

Algorithm 1 Top-level algorithm for inductive relational program synthesis.
 1: procedure Synthesize(F , G, Ψ)
    input: Function symbols F = (f 1 , . . . , fn ), grammars G = (G 1 , . . . , G n ), and specification Ψ = ∀®
                                                                                                               x . ϕ(®
                                                                                                                     x).
    output: Mapping P that maps function symbols in F to programs.
 2:    P ← Prandom ;
 3:    Φ ← true;
 4:    while true do
 5:        if P = null then return null;
 6:        if Verify(P, Ψ) then return P;
 7:        Φ ← Φ ∧ GetRelationalCounterexample(P, Ψ);
 8:        (Φ ′, M) ← Relax(Φ, F );
 9:        H ← BuildHFTA(Φ ′, G, M);
10:        P⊥ ← { f 1 7→ ⊥, . . . , fn 7→ ⊥};
11:        P ← FindProgs(H, P⊥ , M);


   As mentioned in Section 1, our synthesis algorithm is based on the framework of counterexample-
guided inductive synthesis (CEGIS) [Solar-Lezama 2008]. Specifically, given candidate programs P,
the verifier checks whether these programs satisfy the relational specification Ψ. If so, the CEGIS
loop terminates with P as a solution (line 6). Otherwise, we obtain a relational counterexample in
the form of a ground formula and use it to strengthen the current ground relational specification Φ
(line 7). In particular, a relational counterexample can be obtained by instantiating the quantified
variables in the relational specification Ψ with concrete inputs that violate Ψ. Then, in the inductive
synthesis phase, the algorithm finds candidates P that satisfy the new ground relational specification
Φ (lines 8-11) and repeats the aforementioned process. Initially, the candidate programs P are
chosen at random, and the ground relational specification Φ is true.
   Since the verification procedure is not a contribution of this paper, the rest of this section focuses
on the inductive synthesis phase which proceeds in three steps:
(1) Relaxation: Rather than directly taking Φ as the inductive specification, our algorithm first
    constructs a relaxation Φ′ of Φ (line 8) by replacing each occurrence of function fi in Φ with
    a fresh symbol (e.g., f 1 (f 1 (1)) = 1 is converted to f 1,1 (f 1,2 (1)) = 1). This strategy relaxes the
    requirement that different occurrences of a function symbol must have the same implementation
    and allows us to construct our relational version space in a compositional way.
(2) HFTA construction: Given the relaxed specification Φ′, the next step is to construct an HFTA
    whose language consists of exactly those programs that satisfy Φ′ (line 9). Our HFTA construc-
    tion follows the recursive decomposition of Φ′ and allows us to compose the individual version
    spaces of each subterm in a way that the final HFTA is consistent with Φ′.
(3) Enforcing functional consistency: Since Φ′ relaxes the original ground relational specifica-
    tion Φ, the programs for different occurrences of the same function symbol in Φ that are accepted
    by the HFTA from Step (2) may be different. Thus, in order to guarantee functional consistency,
    our algorithm looks for programs that are accepted by the HFTA where all occurrences of the
    same function symbol correspond to the same program (lines 10-11).
  The following subsections discuss each of these three steps in more detail.

5.1   Specification Relaxation
Given a ground relational specification Φ and a set of functions F to be synthesized, the Relax
procedure generates a relaxed specification Φ′ as well as a mapping M from each function f ∈ F

                                Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:10                                                                    Yuepeng Wang, Xinyu Wang, and Isil Dillig


                                         f ∈F         f ′ is fresh       F ⊢ ti ,→ (ti′, Mi )          i = 1, . . . , m
                        (Const)                                                                                             (Func)
   F ⊢ c ,→ (c, ∅)                                                                         ′ ), ⋓m M ⋓ { f 7→ { f ′ }})
                                        F ⊢ f (t 1 , . . . , tm ) ,→ (f ′ (t 1′ , . . . , tm     i=1 i


         F ⊢ ψ 1 ,→ (ψ 1′, M1 )     F ⊢ ψ 2 ,→ (ψ 2′, M2 )                                 F ⊢ Φ ,→ (Φ ′, M)
                                                                     (Logical)                                            (Neg)
            F ⊢ ψ 1 op ψ 2 ,→ (ψ 1 op ψ 2′, M1 ⋓ M2 )
                                 ′
                                                                                         F ⊢ ¬Φ ,→ (¬Φ ′, M)

Fig. 6. Inference rules for relaxing inductive relational specification Φ to Φ ′ . M maps each function symbol
in Φ to its occurrences in Φ ′ . ⋓ is a special union operator for M and ψ denotes either a term or a formula.


to a set of fresh function symbols that represent different occurrences of f in Φ. As mentioned
earlier, this relaxation strategy allows us to build a relational version space in a compositional way
by composing the individual version spaces for each subterm. In particular, constructing an FTA for
a function symbol f ∈ F requires knowledge about the possible values of its arguments, which can
introduce circular dependencies if we have multiple occurrences of f (e.g., f (f (1))). The relaxed
specification, however, eliminates such circular dependencies and allows us to build a relational
version space in a compositional way.
     We present our specification relaxation procedure, Relax, in the form of inference rules shown
in Fig. 6. Specifically, Fig. 6 uses judgments of the form F ⊢ Φ ,→ (Φ′, M), meaning that ground
specification Φ is transformed into Φ′ and M gives the mapping between the function symbols
used in Φ and Φ′. In particular, a mapping f 7→ { f 1 , . . . , fn } in M indicates that function symbols
f 1 , . . . , fn in Φ′ all correspond to the same function f in Φ. It is worthwhile to point out that there
are no inference rules for variables in Fig. 6 because specification Φ is a ground formula that does
not contain any variables.
     Since the relaxation procedure is pretty straightforward, we do not explain the rules in Fig. 6
in detail. At a high level, we recursively transform all subterms and combine the results using a
special union operator ⋓ defined as follows:
                                              ∅                      if f < dom(M1 ) and f < dom(M2 )
                                       (
                 (M1 ⋓ M2 )(f ) =             Mi (f )                if f ∈ dom(Mi ) and f < dom(M j )
                                              M1 (f ) ∪ M2 (f )      otherwise
    In the remainder of this paper, we also use the notation M −1 to denote the inverse of M. That
is, M −1 maps each function symbol in the relaxed specification Φ′ to a unique function symbol in
the original specification Φ (i.e., f = M −1 (fi ) ⇔ fi ∈ M(f )).

5.2    HFTA Construction
We now turn our attention to the relational version space learning algorithm using hierarchical
finite tree automata. Given a relaxed relational specification Φ, our algorithm builds an HFTA H
that recognizes exactly those programs that satisfy Φ. Specifically, each node in H corresponds
to a subterm (or subformula) in Φ. For instance, consider the subterm f (д(1)) where f and д are
functions to be synthesized. In this case, the HFTA contains a node v 1 for f (д(1)) whose child
v 2 represents the subterm д(1). The inter-FTA transitions represent data flow from the children
subterms to the parent term, and the FTA for each node v is constructed according to the grammar
of the top-level constructor of the subterm represented by v.
   Fig. 7 describes HFTA construction in more detail using the judgment G, M ⊢ Φ ↠ H where G
describes the DSL for each function symbol 4 and M is the mapping constructed in Section 5.1. The
4 If there is an interpreted function in the relational specification, we assume that a trivial grammar with a single production

for that function is added to G by default.


Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Relational Program Synthesis                                                                                          1:11

meaning of this judgment is that, under CFGs G and mapping M, HFTA H represents exactly those
programs that are consistent with Φ. In addition to the judgment G, M ⊢ Φ ↠ H , Fig. 7 also uses
an auxiliary judgment of the form G, M ⊢ Φ { H to construct the HFTAs for the subformulas
and subterms in the specification Φ.
     Let us now consider the HFTA construction rules from Fig. 7 in more detail. The first rule, called
Const, is the base case of our algorithm and builds an HFTA node for a constant c. Specifically, we
introduce a fresh node vc and construct a trivial FTA A that accepts only constant c.
     The next rule, Func, shows how to build an HFTA for a function term f (t 1 , . . . , tm ). In this rule,
we first recursively build the HFTAs Hi = (V i , Ωi , vr i , Λi ) for each subterm ti . Next, we use a
procedure called BuildFTA to build an FTA A for the function symbol f that takes m arguments
x 1 , · · · , xm . The BuildFTA procedure is shown in Fig. 8 and is a slight adaptation of the example-
guided FTA construction technique described in Section 3.2: Instead of assigning the input example
to each argument x i , our BuildFTA procedure assigns possible values that x i may take based on
the HFTA Hi for subterm ti . Specifically, let Q fi denote the final states of the FTA Afi associated
with the root node of Hi . If there is a final state qsc in Q fi , this indicates that argument x i of f may
take value c; thus our BuildFTA procedure adds a state qcx i in the FTA A for f (see the Input rule
in Fig. 8). The transitions and new states are built exactly as described in Section 3.2 (see the Prod
rule of Fig. 8), and we mark every state qsc0 as a final state if s 0 is the start symbol in f ’s grammar.
To avoid getting an FTA of infinite size, we impose a predefined bound on how many times the
Prod rule can be applied when building the FTA. Using this FTA A for f and the HFTAs Hi for
f ’s subterms, we now construct a bigger HFTA H as follows: First, we introduce a new node v f
for function f and annotate it with A. Second, we add appropriate inter-FTA transitions in Λ to
account for the binding of formal to actual parameters. Specifically, if qsc is a final state of Afi , we
add a transition qsc → qcx i to Λ. Observe that our HFTA is compositional in that there is a separate
node for every subterm, and the inter-FTA transitions account for the flow of information from
each subterm to its parent.
     The next rule, called Logical, shows how to build an HFTA for a subterm ψ 1 op ψ 2 where op is
either a relation constant (e.g., =, ≤) or a binary logical connective (e.g., ∧, ↔). As in the previous
rule, we first recursively construct the HFTAs Hi = (V i , Ωi , vr i , Λi ) for the subterms ψ 1 and ψ 2 .
Next, we introduce a fresh HFTA node v op for the subterm “ψ 1 op ψ 2 ” and construct its corresponding
FTA A using op’s semantics. The inter-FTA transitions between A and the FTAs annotating the
root nodes of H1 and H2 are constructed in the same way as in the previous rule. 5 Since the Neg
rule for negation is quite similar to the Logical rule, we elide its description in the interest of space.
     The last rule, Final, in Fig. 7 simply assigns the final states of the constructed HFTA. Specifically,
given specification Φ, we first use the auxiliary judgment { to construct the HFTA H for Φ.
However, since we want to accept only those programs that satisfy Φ, we change the final states of
the FTA that annotates the root node of H to be {qs⊤0 } rather than {qs⊤0 , qs⊥0 }.
  Example 5.1. Consider the relational specification Φ : f (2) = д(f (1)), where the DSL for f is
e → x | e + 1 and the DSL for д is t → y | t × 2 (Here, x, y denote the inputs of f and д respectively).
We now explain HFTA construction for this specification.
                                              the specification Φ to a relaxed version Φ : f 1 (2) =′
• First, the relaxation procedure transforms                                                 ′

  д1 (f 2 (1)) and produces a mapping M = f 7→ { f 1 , f 2 }, д 7→ {д1 } relating the symbols in Φ, Φ .
• Fig. 9 shows the HFTA H constructed for Φ′ where we view +1 and ×2 as unary functions for
  ease of illustration. Specifically, by the Const rule of Fig. 7, we build two nodes v 1 and v 2 that
  correspond to two FTAs that only accept constants 1 and 2, respectively. This sets up the initial
5 In fact, the Logical and Neg rules could be viewed as special cases of the Func rule where op and ¬ have a trivial grammar

with a single production. However, we separate these rules for clarity of presentation.


                                  Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:12                                                                      Yuepeng Wang, Xinyu Wang, and Isil Dillig

                                         Jc K     Jc K    Jc K
                 V = {vc }         A = ( qc , {c}, qc , c → qc )                            Ω = {vc 7→ A}
                                                                                                                      (Const)
                                               G, M ⊢ c { (V , Ω, vc , ∅)

               G, M ⊢ ti { (Vi , Ωi , vr i , Λi )     Ωi (vr i ) = (Q i , Σi , Q fi , ∆i )     i = 1, . . . , m
                    Ω= m  i=1 ΩiÐ ∪ v f 7→ BuildFTA              G(M −1 (f )), [Q f1 , . . . , Q fm ]
                         Ð                                                                            
                                     m               c      c      c
                            Λ = i=1 Λi ∪ qs → q x i qs ∈ Q fi , i ∈ [1, m]
                                                   
                                                                                                                        (Func)
                          G, M ⊢ f (t 1 , . . . , tm ) { ( m    i=1 Vi ∪ {v f }, Ω, v f , Λ)
                                                            Ð


                         G, M ⊢ ψi { (Vi , Ωi , vr i , Λi ) Ωi (vr i ) = (Q i , Σi , Q fi , ∆i ) i = 1, 2
          Q = qs⊥0 , qs⊤0 ∪ qcxii qscii ∈ Q fi , i = 1, 2   ∆ = op(qcx11 ,qcx22 ) → qsc0 c = JopK(c 1 , c 2 )
              

 Ω = Ω1 ∪Ω2 ∪ v op 7→ (Q, {x 1 , x 2 , op}, qs⊥0 , qs⊤0 , ∆) Λ = Λ1 ∪Λ2 ∪ qsci → qcx i qsci ∈ Q fi , i = 1, 2
                                                                                                                                 (Logical)
                                G, M ⊢ ψ 1 op ψ 2 { (V1 ∪ V2 ∪ {v op }, Ω, v op , Λ)

                             G, M ⊢ Φ { (V , Ω, vr , Λ)                  Ω(vr )= (Q, Σ, Q f , ∆)
                                Q ′ = q x⊥1 , q x⊤1 , qs⊥0 , qs⊤0       ∆ ′ = ¬(qx⊥1 ) → qs⊤0 , ¬(q x⊤1 ) → qs⊥0
           Ω ′ = Ω ∪ v ¬ 7→ Q ′, {x 1 , ¬}, qs⊤0 , qs⊥0 , ∆ ′             Λ ′ = Λ ∪ qsc → qcx 1 qsc ∈ Q f
                    
                                                                                                                             (Neg)
                                         G, M ⊢ ¬Φ { (V ∪ {v ¬ }, Ω ′, v ¬ , Λ ′ )

                               G, M ⊢ Φ { (V , Ω,
                                                 vr , Λ)   Ω(v
                                                             r ) = (Q, Σ, Q f , ∆)
                                        Ω ′ = Ω vr 7→ (Q, Σ, qs⊤0 , ∆)
                                                                                                          (Final)
                                               G, M ⊢ Φ ↠ (V , Ω ′, vr , Λ)

Fig. 7. Rules for constructing HFTA H = (V , Ω, vr , Λ) for ground relational specification Φ from grammars G,
and function symbol mapping M. Every node v is a fresh node. ψ denotes either a term or a formula. Every
variable x i in function f is assumed to be annotated by f to enforce its global uniqueness.


                                    qsc ∈ Q i                                    G, Q® ⊢ qsc0 ∈ Q
                                                          (Input)                                        (Output)
                   G, Q® ⊢     q x i ∈ Q, x i → qcx i ∈ ∆
                                 c                                             G, Q® ⊢ qsc0 ∈ Q f

               s → σ (s 1 , . . . , sn ) ∈ P   G, Q® ⊢ qsc11 ∈ Q, . . . , qscnn ∈ Q  c = Jσ (c 1 , . . . , c n )K
                                        

                                                                   c1            cn
                                                                                                                    (Prod)
                        G = (T , N , P, s 0 ), Q® ⊢     c
                                                       qs ∈ Q, σ (qs1 , . . . , qsn ) → qsc ∈ ∆

Fig. 8. Auxiliary BuildFTA procedure to construct an FTA A = (Q, Σ, Q f , ∆) for function f that takes m
arguments x 1 , . . . , xm . G is a context-free grammar of function f . Q® = (Q 1 , . . . , Qm ) is a vector where Q i
represents the initial state set for argument x i .



  state set of FTAs corresponding to f 2 and f 1 , which results in two HFTA nodes v f2 and v f1 and
  their corresponding FTAs Ω(v f2 ) and Ω(v f1 ) constructed according to the Func rule. (Note that
  we build the FTAs using only two applications of the Prod rule.) Similarly, we build a node vд1
  and FTA Ω(vд1 ) by taking the final states of Ω(v f2 ) as the initial state set of Ω(vд1 ). Finally, the
  node v = along with its FTA Ω(v = ) is built by the Logical rule.
• Fig. 9 also shows two hierarchical trees, T1 and T2 , that are accepted by the HFTA H constructed
  above. However, note that only T1 corresponds to a valid solution to the original synthesis
  problem because (1) in T1 both f 1 and f 2 refer to the program f = λx . x, and (2) in T2 these two
  occurrences (i.e., f 1 and f 2 ) of f correspond to different programs.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Relational Program Synthesis                                                                                            1:13

                                                                                            v=
                  HFTA H          vf1                                                                        =
                                              q2e                                           qx21                 qs⊤0
                                         id    +1
                                                                                                             =
                  v2                                                                        qx31
                        q22        q2x        q3e
                                                                                                             =
                                                              v g1
                                                                     id
                                                                                q1t         qx22
                                                                                                             =
                                  vf2         q1e                                 x2
                                                               q1y                                           =
                                                                                q2t         qx12                 qs⊥0
                                         id    +1                    id
                  v1                                                              x2                         =
                        q11        q1x        q2e              q2y              q4t         qx42



                   Hierarchical Tree T1
                    v2             vf1                                                             v=
                              2           x         id                                                  x1

                                                                                                                 =
                    v1             vf2                        v g1
                                          x         id               y            id   x2               x2
                              1



                   Hierarchical Tree T2
                   v2              vf1                                                             v=
                          2               x         id                                                  x1

                                                                                                                 =
                   v1              vf2                                   v g1
                                          x         id   +1                       y    id               x2
                          1


Fig. 9. HFTA H = (V , Ω, v = , Λ) for specification f 1 (2) = д1 (f 2 (1)). FTAs are represented as hypergraphs, where
circles correspond to FTA states, double circles indicate final states, and labeled (hyper-)edges correspond to
transitions. Inter-FTA transitions Λ are represented as dashed lines. Hierarchical trees T1 and T2 are both
accepted by H .

  Theorem 5.2. (HFTA Soundness) Suppose G, M ⊢ Φ ↠ H according to the rules from Fig 7,
and let f 1 , . . . , fn be the function symbols used in the relaxed specification Φ. Given a hierarchical tree
T = (V , ϒ, vr , E) that is accepted by H , we have:
  (1) ϒ(v fi ) is a program that conforms to grammar G(M −1 (fi ))
  (2) ϒ(v f1 ), . . . , ϒ(v fn ) satisfy Φ, i.e. ϒ(v f1 ), . . . , ϒ(v fn ) |= Φ
  Proof. See Appendix A.                                                                                                  □
     Theorem 5.3. (HFTA Completeness) Let Φ be a ground formula where every function symbol
f 1 , . . . , fn occurs exactly once, and suppose we have G, M ⊢ Φ ↠ H . If there are implementations
Pi of fi such that P1 , . . . , Pn |= Φ, where Pi conforms to grammar G(M −1 (fi )), then there exists a
hierarchical tree T = (V , ϒ, vr , E) accepted by H such that ϒ(v fi ) = Pi for all i ∈ [1, n].
  Proof. See Appendix A.                                                                                                  □

5.3   Enforcing Functional Consistency
As stated by Theorems 5.2 and 5.3, the HFTA method discussed in the previous subsection gives
a sound and complete synthesis procedure with respect to the relaxed specification where each
function symbol occurs exactly once. However, a hierarchical tree T that is accepted by the HFTA
might still violate functional consistency by assigning different programs to the same function f

                                  Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:14                                                               Yuepeng Wang, Xinyu Wang, and Isil Dillig

Algorithm 2 Algorithm for enforcing functional consistency.
 1: procedure FindProgs(H, P, M)
       Input: HFTA H = (V , Ω, vr , Λ), mapping P that maps a function symbol to a program, and mapping M
       that maps a function symbol to its occurrences.
       Output: Mapping Pres that maps each function symbol to a program.
 2:       f ← ChooseUnassigned(P);
 3:       if f = null then return P;
 4:       fi ← ChooseOccurrence(M,       f );
          for each p ∈ ϒ(v fi ) (V , ϒ, vr , E) ∈ L(H ), v fi ∈ V do
                         
 5:
 6:           H ′ ← Propagate(H, p, f , M);
 7:           if L(H ′ ) = ∅ then continue;
 8:           P ′ ← P[f 7→ p];
 9:           Pres ← FindProgs(H ′, P ′, M);
10:           if Pres , null then return Pres ;
11:       return null;



used in the original specification. In this section, we describe an algorithm for finding hierarchical
trees that (a) are accepted by the HFTA and (b) conform to the functional consistency requirement.
   Algorithm 2 describes our technique for finding accepting programs that obey functional consis-
tency. Given an HFTA H and a mapping M from function symbols in the original specification
to those in the relaxed specification, the FindProgs procedure finds a mapping Pres from each
function symbol fi in the domain of M to a program pi such that p1 , . . . , pn are accepted by H .
Since the resulting mapping Pres maps each function symbol in the original specification to a single
program, the solution returned by FindProgs is guaranteed to be a valid solution for the original
relational synthesis problem.
   We now explain how Algorithm 2 works in more detail. At a high level, FindProgs is a recursive
procedure that, in each invocation, updates the current mapping P by finding a program for a
currently unassigned function symbol f . In particular, we say that a function symbol f is unassigned
if P maps f to ⊥. Initially, all function symbols are unassigned, but FindProgs iteratively makes
assignments to each function symbol in the domain of P. Eventually, if all function symbols
have been assigned, this means that P is a valid solution; thus, Algorithm 2 returns P at line 3 if
ChooseUnassigned yields null.
   Given a function symbol f that is currently unassigned, FindProgs first chooses some occurrence
fi of f in the relaxed specification (i.e., fi ∈ M(f )) and finds a program p for fi . In particular, given
a hierarchical tree T accepted by H 6 , we find the program p that corresponds to fi in T (line 5).
Now, since every occurrence of f must correspond to the same program, we use a procedure called
Propagate that propagates p to all other occurrences of f (line 6). The procedure Propagate is
shown in Algorithm 3 and returns a modified HFTA H ′ that enforces that all occurrences of f
are consistent with p. (We will discuss the Propagate procedure in more detail after finishing the
discussion of FindProgs).
   The loop in lines 5–10 of Algorithm 2 performs backtracking search. In particular, if the language
of H ′ becomes empty after the call to Propagate, this means that p is not a suitable implementation
of f — i.e., given the current mapping P, there is no extension of P where p is assigned to f . Thus,
the algorithm backtracks at line 7 by moving on to the next program for f .

6 Section 6 describes a strategy for lazily enumerating hierarchical trees accepted by a given HFTA.



Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Relational Program Synthesis                                                                                         1:15

Algorithm 3 Auxilary procedure for propagating a program in HFTA.
 1: procedure Propagate(H, p, f , M)
      Input: HFTA H = (V , Ω, vr , Λ), program p, function symbol f , M maps function symbols to occurrences
      Output: An updated HFTA H ′ = (V , Ω ′, vr , Λ ′ )
 2:      Ω ′ ← Ω, Λ ′ ← Λ;
 3:      for each v ∈ {v fi | fi ∈ M(f ), v fi ∈ V } do
 4:          (Q, Σ, Q f , ∆) ← Ω(v);
 5:          Q f′ ← ReachableFinalStates(Ω(v), p);                                   ▷ remove unreachable final states
 6:          Ω ′ ← Ω ′ [v 7→ (Q, Σ, Q f′ , ∆)];
 7:          Λ ′ ← Λ ′ \ ∪q ∈Q f \Q ′ {q → q ′ | q → q ′ ∈ Λ ′ };                        ▷ remove spurious transitions
                                        f

 8:      return (V , Ω ′, vr , Λ ′ );




   On the other hand, assuming that the call to Propagate does not result in a contradiction (i.e.,
L(H ′) , ∅), we try to find an implementation of the remaining function symbols via the recursive
call to FindProgs at line 9. If the recursive call does not yield null, we have found a set of programs
that both satisfy the relational specification and obey functional consistency; thus, we return Pres
at line 10. Otherwise, we again backtrack and look for a different implementation of f .

    Propagate subroutine. We now discuss the Propagate subroutine for enforcing that different
occurrences of a function have the same implementation. Given an HFTA H and a function symbol
f with candidate implementation p, Propagate returns a new HFTA H ′ such that the FTAs for all
occurrences of f only accept programs that have the same input-output behavior as p.
    In more detail, the loop in lines 3–7 of Algorithm 3 iterates over all HFTA nodes v that correspond
to some occurrence of f . Since we want to make sure that the FTA for v only accepts those programs
that have the same input-output behavior as p, we first compute all final states Q f′ that can be
reached by successful runs of the FTA on program p (line 5) and change the final states of Ω(v) to
Q f′ (line 6). Since some of the inter-FTA transitions become spurious as a result of this modification,
we also remove inter-FTA transitions q → q ′ where q is no longer a final state of its corresponding
FTA (line 7). These modifications ensure that the FTAs for different occurrences of f only accept
programs that have the same behavior as p.

   Example 5.4. We now illustrate how FindProgs extracts programs from the HFTA in Example 5.1.
Suppose we first choose occurrence f 2 of function f and its implementation f 2 = λx . x + 1. Since f 1
and f 2 must have the same implementation, the call to Propagate results in the modified HFTA H2
shown in Fig. 10. However, observe that L(H2 ) is empty because the final state qs⊤0 in FTA Ω(v = )
is only reachable via state q x2 1 , but q x2 1 no longer has incoming transitions. Thus, the algorithm
backtracks to the only other implementation choice for f 2 , namely λx .x, and Propagate now
yields the HFTA H3 from Fig. 10. This time, L(H3 ) is not empty; hence, the algorithm moves on
to function symbol д. Since the only hierarchical tree in L(H3 ) is T1 from Fig. 9, we are forced to
choose the implementation д = λy. y × 2. Thus, the FindProgs procedure successfully returns
P = { f 7→ λx .x, д 7→ λy. y × 2}.

5.4    Properties of the Synthesis Algorithm
The following theorems state the soundness and completeness of the synthesis algorithm.

                                    Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:16                                                               Yuepeng Wang, Xinyu Wang, and Isil Dillig

                                                                                v=
                HFTA H2         vf1                                                      =
                                            q2e                                  qx21        qs⊤0
                                       id    +1
                                                                                         =
                v2                                                               qx31
                     q22         q2x        q3e
                                                                                         =
                                                       v g1
                                                              id
                                                                   q1t           qx22
                                                                                         =
                                vf2         q1e                      x2
                                                        q1y                              =
                                                                   q2t           qx12        qs⊥0
                                       id    +1               id
                v1                                                   x2                  =
                     q11         q1x        q2e         q2y        q4t           qx42



                                                                                v=
                HFTA H3         vf1                                                      =
                                            q2e                                  qx21        qs⊤0
                                       id    +1
                                                                                         =
                v2                                                               qx31
                     q22         q2x        q3e
                                                                                         =
                                                       v g1
                                                              id
                                                                   q1t           qx22
                                                                                         =
                                vf2         q1e                      x2
                                                        q1y                              =
                                                                   q2t           qx12        qs⊥0
                                       id    +1               id
                v1                                                   x2                  =
                     q11         q1x        q2e         q2y        q4t           qx42


Fig. 10. HFTAs after propagation. H2 is obtained by propagating f 1 = f 2 = λx . x +1 on HFTA H in Example 5.1
(shown in Fig. 9). H3 is obtained by propagating f 1 = f 2 = λx . x on HFTA H .

   Theorem 5.5. (Soundness) Assuming the soundness of the Verify procedure invoked by Algo-
rithm 1, then the set of programs P returned by Synthesize are guaranteed to satisfy the relational
specification Ψ, and program Pi of function fi conforms to grammar G(fi ).
    Proof. See Appendix A.                                                                                  □
   Theorem 5.6. (Completeness) If there is a set of programs that (a) satisfy Ψ and (b) can be
implemented using the DSLs given by G, then Algorithm 1 will eventually terminate with programs P
satisfying Ψ.
    Proof. See Appendix A.                                                                                  □

6     IMPLEMENTATION
We have implemented the proposed relational program synthesis approach in a framework called
Relish. To demonstrate the capabilities of the Relish framework, we instantiate it on the first two
domains from Section 2.2, namely string encoders/decoders, and comparators. In this section, we
describe our implementation of Relish and its instantiations.

6.1    Implementation of Relish Framework
While the implementation of the Relish framework closely follows the algorithm described in
Section 5, it performs several important optimizations that we discuss next.
  Lazy enumeration. Recall that Algorithm 2 needs to (lazily) enumerate all hierarchical trees
accepted by a given HFTA. Furthermore, since we want to find a program with the greatest
generalization power, our algorithm should enumerate more promising programs first. Based on

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Relational Program Synthesis                                                                                     1:17


      EncodedText     E    :=      M | padToMultiple(E, num, char ) | header(E)
      Mapper          M    :=      enc16(B) | enc32(B) | enc32Hex(B) | enc64(B) | enc64XML(B) | encUU(B)
      ByteArray       B    :=      x | reshape(B, num) | encUTF8(I ) | encUTF16(I ) | encUTF32(I )
      IntArray        I    :=      codePoint(x)
                    x ∈ Variable            num ∈ {1, 2, . . . , 8}        char ∈ {‘=’, ‘´’, . . .}
                                     (a) Context-free grammar for encoders.
      DecodedData     D    :=      B | asUnicode(I )
      IntArray        I    :=      decUTF8(B) | decUTF16(B) | decUTF32(B)
      ByteArray       B    :=      M | invReshape(B, num)
      Mapper          M    :=      dec16(C) | dec32(C) | dec32Hex(C) | dec64(C) | dec64XML(C) | decUU(C)
      CharArray       C    :=      x | removePad(C, char ) | substr(C, num)
                    x ∈ Variable            num ∈ {1, 2, . . . , 8}        char ∈ {‘=’, ‘´’, . . .}
                                     (b) Context-free grammar for decoders.
                Fig. 11. Context-free grammars for Unicode string encoders and decoders.
these criteria, we need a mechanism for predicting the generalization power of a hierarchical tree
using some heuristic cost metric. In our implementation, we associate a non-negative cost with
every DSL construct and compute the cost of a given hierarchical tree by summing up the costs
of all its nodes. Because hierarchical trees with lower cost are likely to have better generalization
power, our algorithm lazily enumerates hierarchical trees according to their cost.
   In our implementation, we reduce the problem of enumerating hierarchical trees accepted by
an HFTA to the task of enumerating B-paths in a hypergraph [Gallo et al. 1993]. In particular,
we first flatten the HFTA into a standard FTA by combining the individual tree automata at each
node via the inter-FTA transitions. We then represent the resulting flattened FTA as a hypergraph
where the FTA states correspond to nodes and a transition σ (q 1 , . . . , qn ) → q corresponds to a
B-edge ({q 1 , . . . , qn }, q) with weight cost(σ ). Given this representation, the problem of finding the
lowest-cost hierarchical tree accepted by an HFTA becomes equivalent to the task of finding a
minimum weighted B-path in a hypergraph, and our implementation leverages known algorithms
for solving this problem [Gallo et al. 1993].
   Verification. Because our overall approach is based on the CEGIS paradigm, we need a sep-
arate verification step to both check the correctness of the programs returned by the inductive
synthesizer and find counterexamples if necessary. However, because heavy-weight verification
can add considerable overhead to the CEGIS loop, we test the program against a large set of inputs
rather than performing full-fledged verification in each iteration. Specifically, we generate a set of
validation inputs by computing all possible permutations of a finite set up to a bounded length k
and check the correctness of the candidate program against this validation set. In our experiments,
we use over a million test cases in each iteration, and resort to full verification only when the
synthesized program passes all of these test cases.

6.2   Instantiation for String Encoders and Decoders
While Relish is a generic framework that can be used in various application domains, one needs to
construct suitable DSLs and write relational specifications for each different domain. In this section,
we discuss our instantiation of Relish for synthesizing string encoders and decoders. Since we
have already explained the relational property of interest in Section 2.2, we discuss two simple
DSLs, presented in Fig. 11, for implementing encoders and decoders respectively.
  DSL for encoders. We designed a DSL for string encoders by reviewing several different en-
coding mechanisms and identifying their common building blocks. Specifically, this DSL allows

                                Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:18                                                             Yuepeng Wang, Xinyu Wang, and Isil Dillig

transforming a Unicode string (or binary data) to a sequence of restricted ASCII characters (e.g.,
to fulfill various requirements of text-based network transmission protocols). At a high-level,
programs in this DSL first transform the input string to an integer array and then to a byte array.
The encoded text is obtained by applying various kinds of mappers to the byte array, padding it,
and attaching length information. In what follows, we informally describe the semantics of the
constructs used in the encoder DSL.
• Code point representation: The codePoint function converts string s to an integer array I where
  I [j] corresponds to the Unicode code point for s[j].
• Mappers: The encUTF8/16/32 functions transform the code point array to a byte array according
  to the corresponding standards of UTF-8, UTF-16, UTF-32, respectively. The other mappers
  encX can further transform the byte array into a sequence of restricted ASCII characters based
  on different criteria. For example, the enc16 function is a simple hexadecimal mapper that can
  convert binary data 0x6E to the string “6E”.
• Padding: The padToMultiple function takes an existing character array E and pads it with a
  sequence of extra char characters to ensure that the length of the padded sequence is evenly
  divisible by num.
• Header: The header(E) function prepends the ASCII representation of the length of the text to E.
• Reshaping: The function reshape(B, num) first concatenates all bytes in B, then regroups them
  such that each group only contains num bits (instead of 8), and finally generates a new byte array
  where each byte is equal to the value of corresponding group. For example, reshape([0xFF],4)
  = [0x0F,0x0F] and reshape([0xFE],2) = [0x03,0x03,0x03,0x02].
   DSL for decoders. The decoder DSL is quite similar to the encoder one and is structured as
follows: Given an input string x, programs in this DSL first process x by removing the header
and/or padding characters and then transform it to a byte array using a set of pre-defined mappers.
The decoded data can be either the resulting byte array or a Unicode string obtained by converting
the byte array to an integer Unicode code point array. In more detail, the decoder DSL supports the
following built-in operators:
• Unicode conversion: The asUnicode function converts an integer array I to a string s, where s[j]
  corresponds to the Unicode symbol of code point I [j].
• Mappers: The decUTF8/16/32 functions transform a byte array to a code point array based on
  standards of UTF-8, UTF-16, UTF-32, respectively. The other mappers decX transform a sequence
  of ASCII characters to byte arrays according to their standard transformation rules.
• Character removal: The removePad function removes all trailing characters char from a given
  string C. The substr function takes a string C and an index num, and returns the sub-string of C
  from index num to the end.
• Reshaping: The invReshape function takes a byte array B, collects num bits from the least
  significant end of each byte, concatenates the bit sequence and regroups every eight bits to
  generate a new byte array. For instance, invReshape([0x0E,0x0F],4) = [0xEF].
  Example 6.1. The desired encode/decode functions from Example 2.3 can be implemented in
our DSL as follows:
       encode(x) : padToMultiple (enc64 (reshape (encUTF8 (codePoint (x)), 6)), 4, '=')
       decode(x) : asUnicode (decUTF8 (invReshape (dec64 (removePad (x, '=')), 6)))

6.3     Instantiation for Comparators
We have also instantiated the Relish framework to enable automatic generation of custom string
comparators. As described in Section 2.2, this domain is an interesting ground for relational program
synthesis because comparators must satisfy three different relational properties (i.e., anti-symmetry,

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Relational Program Synthesis                                                                                      1:19


                            Comparator   C    :=    B | chain(B, C)
                            Basic        B    :=    intCompare(I 1 , I 2 ) | strCompare(S 1 , S 2 )
                            Integer      I    :=    countChar(S, c) | length(S) | toInt(S)
                            String       S    :=    substr(v, P 1 , P 2 )
                            Position     P    :=    pos(v, t, k, d) | constPos(k)
             v ∈ { x, y }      c ∈ Characters       t ∈ Tokens         k ∈ Integers        d ∈ { Start, End }
                                 Fig. 12. Context-free grammar for comparators.
transitivity, and totality). In what follows, we describe the DSL from Fig. 12 that Relish uses to
synthesize these comparators.
   In more detail, programs in our comparator DSL take as input a pair of strings x, y, and return -1,
0, or 1 indicating that x precedes, is equal to, or succeeds y respectively. Specifically, a program is
either a basic comparator B or a comparator chain of the form chain(B 1 , . . . , Bn ) which returns the
result of the first comparator that does not evaluate to zero. The DSL allows two basic comparators,
namely intCompare and strCompare. The integer or string inputs to these basic comparators can be
obtained using the following functions:
• Substring extraction: The substring function is used to extract substrings of the input string. In
   particular, for a string v and positions P1 , P 2 , it returns the substring of v that starts at index P1
   and ends at index P2 .
• Position identifiers: A position P can either be a constant index (constPos(k)) or the (start or
   end) index of the k’th occurrence of the match of token t in the input string (pos(v, t, k, d)). 7 For
   example, we have pos(“12ab”, Number, 1, Start) = 0 and pos(“12ab”, Number, 1, End) = 2 where
   Number is a token indicating a sequence of digits.
• Numeric string features: The DSL allows extracting various numeric features of a given string
   S. In particular, countChar yields the number of occurrences of a given character c in string S,
   length yields string length, and toInt converts a string representing an integer to an actual integer
   (i.e., toInt(“123”) = 123 but toInt(“abc") throws an exception).
   Example 6.2. Consider Example 2.4 where the user wants to sort integers based on the number
of occurrences of the number 5, and, in the case of a tie, sort them based on the actual integer
values. This functionality can be implemented by the following simple program in our DSL:
                   chain (intCompare (countChar (x, '5'), countChar (y, '5')),
                          intCompare (toInt (x), toInt (y)) )

7   EVALUATION
We evaluate Relish by using it to automatically synthesize (1) string encoders and decoders
for program inversion tasks collected from prior work [Hu and D’Antoni 2017] and (2) string
comparators to solve sorting problems posted on StackOverflow. The goal of our evaluation is to
answer the following questions:
    • How does Relish perform on various relational synthesis tasks from two domains?
    • What is the benefit of using HFTAs for relational program synthesis?
  Experimental setup. To evaluate the benefit of our approach over a base-line, we compare our
method against EUSolver [Alur et al. 2017], an enumeration-based synthesizer that won the General
Track of the most recent SyGuS competition [Alur et al. 2013]. Since EUSolver only supports
synthesis tasks in linear integer arithmetic, bitvectors, and basic string manipulations by default,
we extend it to encoder/decoders and comparators by implementing the same DSLs described in
7 Tokens are chosen from a predefined universe of regular expressions.



                                 Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:20                                                              Yuepeng Wang, Xinyu Wang, and Isil Dillig

                   Table 1. Experimental results on Unicode string encoders and decoders.
                 Enc     Dec                       Relish                            EUSolver
 Benchmark                                                                                                Speedup
                 Size    Size   Iters   Total(s)     Synth(s)   Mem(MB)      Iters   Total(s) Synth(s)
   Base16         6       6       3       16.2         10.4       551          3      494.2     489.3      30.4x
   Base32         9       8       5       21.0         14.6       458          -       T/O      T/O          -
  Base32hex       9       8       5       22.9         15.6       468          -       T/O      T/O          -
   Base64         9       8       5       16.4         8.8        916          -       T/O      T/O          -
  Base64xml       9       8       6       23.4         15.5       1843         -       T/O      T/O          -
     UU           10      10      5       23.3         15.2       843          -       T/O      T/O          -
    UTF-8         6       6       4       17.7         11.9       916          4      536.4     531.8      30.2x
   UTF-16         6       6       2       11.5         5.4        285          4      1265.2   1259.9      110.4x
   UTF-32         6       6       2       11.6         4.8        284          3      771.1     765.1      66.4x
    UTF-7         6       6       3       14.8         9.2        285          3      475.2     470.1      32.1x
   Average        7.6    7.2     4.0      17.9         11.1        685        3.4        708.4    703.2    46.5x

Section 6. Additionally, we implement the same CEGIS loop used in Relish for EUSolver and use
the same bounded verifier in our evaluation. All experiments are conducted on a machine with
Intel Xeon(R) E5-1620 v3 CPU and 32GB of physical memory, running the Ubuntu 14.04 operating
system. Due to finite computational resources, we set a time limit of 24 hours for each benchmark.

7.1    Results for String Encoders and Decoders
In our first experiment, we evaluate Relish by using it to simultaneously synthesize Unicode string
encoders and decoders, which are required to be inverses of each other.
   Benchmarks. We collect a total of ten encoder/decoder benchmarks, seven of which are taken
from a prior paper on program inversion [Hu and D’Antoni 2017]. Since the 14 benchmarks from
prior paper [Hu and D’Antoni 2017] are essentially seven pairs of encoders and decoders, we
have covered all their encoder/decoder benchmarks. The remaining three benchmarks, namely,
Base32hex, UTF-32, and UTF-7, are also well-known encodings. Unlike previous work on program
inversion, our goal is to solve the considerably more difficult problem of simultaneously synthesizing
the encoder and decoder from input-output examples rather than inverting an existing function.
For each benchmark, we use 2-3 input-output examples taken from the documentation of the
corresponding encoders. We also specify the relational property ∀x . decode(encode(x))=x and
use the encoder/decoder DSLs presented in Section 6.2.
   Main results. Our main experimental results are summarized in Table 1, where the first two
columns (namely, “Enc Size” and “Dec Size”) describe the size of the target program in terms of the
number of AST nodes. 8 The next three columns under Relish summarize the results obtained
by running Relish on each of these benchmarks, and the three columns under EUSolver report
the same results for EUSolver. Specifically, the column labeled “Iters” shows the total number of
iterations inside the CEGIS loop, “Total” shows the total synthesis time in seconds, and “Synth”
indicates the time (in seconds) taken by the inductive synthesizer (i.e., excluding verification). If a
tool fails to solve the desired task within the 24 hour time limit, we write T/O to indicate a time-out.
Finally, the last column labeled “Speed-up” shows the speed-up of Relish over EUSolver for those
benchmarks where neither tool times out.
   As shown in Table 1, Relish can correctly solve all of these benchmarks 9 and takes an average
of 17.9 seconds per benchmark. In contrast, EUSolver solves half of the benchmarks within the 24
hour time limit and takes an average of approximately 12 minutes per benchmark that it is able to
8 We obtain this information by manually writing a simplest DSL program for achieving the desired task.
9 We manually inspected the synthesized solutions and confirmed their correctness.



Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Relational Program Synthesis                                                                                      1:21

solve. For the five benchmarks that can be solved by both tools, the average speed-up of Relish
over EUSolver is 46.5x. 10 These statistics clearly demonstrate the advantages of our HFTA-based
approach compared to enumerative search: Even though both tools use the same DSLs, verifier,
and CEGIS architecture, Relish unequivocally outperforms EUSolver across all benchmarks.
   Next, we compare Relish and EUSolver in terms of the number of CEGIS iterations for the five
benchmarks that can be solved by both tools. As we can see from Table 1, Relish takes 2.8 CEGIS
iterations on average, whereas EUSolver needs an average of 3.4 attempts to find the correct
program. This discrepancy suggests that our HFTA-based method might have better generalization
power compared to enumerative search. In particular, our method first generates a version space
that contains all tuples of programs that satisfy the relational specification and then searches for
the best program in this version space. In contrast, EUSolver returns the first program that satisfies
the current set of counterexamples; however, this program may not be the best (i.e., lowest-cost)
one in Relish’s version space.
   Finally, we compare Relish against EUSolver in terms of synthesis time per CEGIS iteration:
Relish takes an average of 4.5 seconds per iteration, whereas EUSolver takes 208.4 seconds on
average across the five benchmarks that it is able to solve. To summarize, these results clearly
indicate the advantages of our approach compared to enumerative search when synthesizing string
encoders and decoders.
   Memory usage. We now investigate the memory usage of Relish on the encoder/decoder
benchmarks (see column labeled Mem in Table 1). Here, the memory usage varies between 284MB
and 1843MB, with the average being 685MB. As we can see from Table 1, the memory usage mainly
depends on (1) the number of CEGIS iterations and (2) the size of programs to be synthesized.
Specifically, as the CEGIS loop progresses, the number of function occurrences in the ground
relational specification increases, which results in larger HFTAs. For example, the impact of the
number of CEGIS iterations on memory usage becomes apparent by comparing the “Base64xml” and
“UTF-32” benchmarks, which take 6 and 2 iterations and consume 1843 MB and 284 MB respectively.
In addition to the number of CEGIS iterations, the size of the target program also has an impact on
memory usage. Intuitively, the larger the synthesized programs, the larger the size of the individual
FTAs; thus, memory usage tends to increase with program size. For example, the impact of program
size on memory usage is illustrated by the difference between the “UU” and “Base32” benchmarks.

7.2   Results for String Comparators
In our second experiment, we evaluate Relish by using it to synthesize string comparators for
sorting problems obtained from StackOverflow. Even though our goal is to synthesize a single
compare function, this problem is still a relational synthesis task because the generated program
must obey two 2-safety properties (i.e., anti-symmetry and totality) and one 3-safety property (i.e.,
transitivity). Thus, we believe that comparator synthesis is also an interesting and relevant test-bed
for evaluating relational synthesizers.
  Benchmarks. To perform our evaluation, we collected 20 benchmarks from StackOverflow
using the following methodology: First, we searched StackOverflow for the keywords “Java string
comparator”. Then, we manually inspected each of these posts and retained exactly those that
satisfy the following criteria:
    • The question in the post should involve writing a compare function for sorting strings.
    • The post should contain a list of sample strings that are sorted in the desired way.
    • The post should contain a natural language description of the desired sorting task.
10 Here, we use geometric mean to compute the average since the arithmetic mean is not meaningful for ratios.



                                 Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:22                                                             Yuepeng Wang, Xinyu Wang, and Isil Dillig

                                    Table 2. Experimental results on comparators.
                                                 Relish                           EUSolver
    Benchmark        Size                                                                             Speedup
                            Iters     Total(s)    Synth(s)   Mem(MB)      Iters   Total(s) Synth(s)
    comparator-1      5       2         2.0          0.1        12          2       2.6       0.7       1.3x
    comparator-2      13      5         3.4          0.2       1375         5       5.5       2.5       1.6x
    comparator-3      13      5         4.1          0.5       385          6       21.5     18.5       5.3x
    comparator-4      23      6         7.7          1.4       1401         10     299.7     291.9     38.8x
    comparator-5      21      7         8.8          1.2       548          10     650.9     643.3     74.1x
    comparator-6      23      4         9.1          0.2        30          11      57.3     52.5       6.3x
    comparator-7      25      7         9.8          0.6       1386         9      640.8     632.5     65.1x
    comparator-8      23      6         9.9          1.6       117          7       50.7     45.2       5.1x
    comparator-9      41      10        25.5        12.7       2146          -      T/O      T/O          -
   comparator-10      21      11        40.7        32.4       1454         12     1301.9   1295.3     32.0x
   comparator-11      41      9         42.9         7.4       4507         13    13966.0   13952.7    325.2x
   comparator-12      17      10        75.2        66.7       1045         15     9171.0   9161.4     122.0x
   comparator-13      27      10        85.0        60.1       3834         13    10742.8   10736.3    126.3x
   comparator-14      25      8        102.5        93.2       2022          -      T/O      T/O          -
   comparator-15      17      9        116.7        112.3      1622         16    26443.4   26434.6    226.5x
   comparator-16      19      7        130.1        124.2      1383          -      T/O      T/O          -
   comparator-17      43      11       196.2        183.4      4460          -      T/O      T/O          -
   comparator-18      41      10       406.5        351.0     18184          -      T/O      T/O          -
   comparator-19      65      9        523.9        485.7     18367          -      T/O      T/O          -
   comparator-20       -       -        T/O         T/O          -           -      T/O      T/O          -
       Average       26.5    7.7        94.7        80.8       3382        9.9     4873.4   4866.7     26.0x
   The relational specification Ψ for each benchmark consists of the following three parts:
    • Universally-quantified formulas reflecting the three relational properties that compare has
      to satisfy (i.e., anti-symmetry, transitivity, and totality).
    • Another quantified formula that stipulates reflexivity (i.e., ∀x . compare(x, x) = 0)
    • Quantifier-free formulas that correspond to the input-output examples from the StackOver-
      flow post. In particular, given a sorted list l, if string x appears before string y in l, we add
      the examples compare(x,y) = -1 and compare(y,x) = 1.
   Among these benchmarks, the number of examples range from 2 to 30, with an average of 16.
   Main results. Our main results are summarized in Table 2, which is structured in the same way
as Table 1. The main take-away message from this experiment is that Relish can successfully solve
95% of the benchmarks within the 24 hour time limit. Among these 19 benchmarks, Relish takes
an average of 94.7 seconds per benchmark, and it solves 55% of the benchmarks within 1 minute
and 75% of the benchmarks within 2 minutes.
   In contrast to Relish, EUSolver solves considerably fewer benchmarks within the 24 hour time-
limit. In particular, Relish solves 46% more benchmarks than EUSolver (19 vs. 13) and outperforms
EUSolver by 26x (in terms of running time) on the common benchmarks that can be solved by
both techniques. Furthermore, similar to the previous experiment, we also observe that Relish
requires fewer CEGIS iterations (7.0 vs. 9.9 on average), again confirming the hypothesis that the
HFTA-based approach might have better generalization power. Finally, we note that Relish is also
more efficient than EUSolver per CEGIS iteration (12 seconds vs. 492 seconds).
   Memory usage. We also investigate the memory usage of Relish on the comparator benchmarks.
As shown in the Mem column of Table 2, memory usage varies between 12 MB and 18367MB, with
an average memory consumption of 3382MB. Comparing these statistics with Table 1, we see that
memory usage is higher for comparators than the encoder/decoder benchmarks. We believe this
difference can be attributed to the following three factors: First, as shown in Table 2, the size of the

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Relational Program Synthesis                                                                                 1:23

synthesized programs is larger for the comparator domain. Second, the relational specification for
comparators is more complex and involves multiple properties such as reflexivity, anti-symmetry,
totality, and transitivity. Finally, most benchmarks in the comparator domain require more CEGIS
iterations to solve and therefore result in larger HFTAs.
   Analysis of failed benchmarks. We manually inspected the benchmark “comparator-20” that
Relish failed to synthesize within the 24 hour time limit. In particular, we found this benchmark
is not expressible in our current DSL because it requires comparing integers that are obtained by
concatenating all substrings that represent integers in the input strings.
    Summary. In summary, this experiment demonstrates that Relish can successfully synthesize
non-trivial string comparators that arise in real-world scenarios. This experiment also demonstrates
the advantages of our new relational synthesis approach compared to an existing state-of-the-art
solver. While the comparator synthesis task involves synthesizing a single function, the enumeration-
based approach performs considerably worse than Relish because it does not use the relational
(i.e., k-safety) specification to prune its search space.

8   RELATED WORK
In this section, we survey prior work that is most closely related to relational program synthesis.
   Relational Program Verification. There is a large body of work on verifying relational prop-
erties about programs [Barthe et al. 2011; Benton 2004; Sousa and Dillig 2016; Sousa et al. 2018;
Wang et al. 2018b; Yang 2007]. Existing work on relational verification can be generally categorized
into three classes, namely relational program logics, product programs, and Constrained Horn Clause
(CHC) solving. The first category includes Benton’s Relational Hoare Logic [Benton 2004] and its
variants [Barthe et al. 2012a,b; Yang 2007] as well as Cartesian Hoare Logic [Chen et al. 2017; Sousa
and Dillig 2016] for verifying k-safety properties. In contrast to these approaches that provide a
dedicated program logic for reasoning about relational properties, an alternative approach is to
build a so-called product program that captures the simultaneous execution of multiple programs
or different runs of the same program [Barthe et al. 2011, 2013, 2004]. In the simplest case, this
approach sequentially composes different programs (or copies of the same program) [Barthe et al.
2004], but more sophisticated product construction methods perform various transformations such
as loop fusion and unrolling to make invariant generation easier [Barthe et al. 2011, 2013; Sousa
et al. 2014; Zaks and Pnueli 2008]. A common theme underlying all these product construction
techniques is to reduce the relational verification problem to a standard safety checking problem.
Another alternative approach that has been explored in prior work is to reduce the relational
verification problem to solving a (recursive) set of Constrained Horn Clauses (CHC) and apply
transformations that make the problem easier to solve [De Angelis et al. 2016; Mordvinov and
Fedyukovich 2017]. To the best of our knowledge, this paper is the first one to address the dual
synthesis variant of the relational verification problem.
   Program Synthesis. This paper is related to a long line of work on program synthesis dating
back to the 1960s [Green 1969]. Generally speaking, program synthesis techniques can be classified
into two classes depending on whether they perform deductive or inductive reasoning. In particular,
deductive synthesizers generate correct-by-construction programs by applying refinement and
transformation rules [Delaware et al. 2015; Kneuss et al. 2013; Manna and Waldinger 1986; Morgan
1994; Polikarpova et al. 2016]. In contrast, inductive synthesizers learn programs from input-
output examples using techniques such as constraint solving [So and Oh 2017; Solar-Lezama 2009],
enumerative search [Alur et al. 2017; Feser et al. 2015], version space learning [Polozov and Gulwani
2015], stochastic search [Heule et al. 2016; Schkufza et al. 2013], and statistical models and machine

                            Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:24                                                             Yuepeng Wang, Xinyu Wang, and Isil Dillig

learning [Raychev et al. 2016, 2015]. Similar to most recent work in this area [Gulwani 2012; Polozov
and Gulwani 2015; Solar-Lezama 2009; Wang et al. 2018a], our proposed method also uses inductive
synthesis. However, a key difference is that we use relational examples in the form of ground
formulas rather than the more standard input-output examples.
   Counterexample-guided Inductive Synthesis. The method proposed in this paper follows
the popular counterexample-guided inductive synthesis (CEGIS) methodology [Alur et al. 2013;
Solar-Lezama 2009; Solar-Lezama et al. 2006]. In the CEGIS paradigm, an inductive synthesizer
generates a candidate program P that is consistent with a set of examples, and the verifier checks
the correctness of P and provides counterexamples when P does not meet the user-provided
specification. Compared to other synthesis algorithms that follow the CEGIS paradigm, the key
differences of our method are (a) the use of relational counterexamples and (b) a new inductive
synthesis algorithm that utilizes relational specifications.
   Version Space Learning. As mentioned earlier, the inductive synthesizer used in this work can
be viewed as a generalization of version space learning to the relational setting. The notion of version
space was originally introduced in the 1980s as a supervised learning framework [Mitchell 1982]
and has found numerous applications within the field of program synthesis [Gulwani 2011; Lau
et al. 2003; Polozov and Gulwani 2015; Wang et al. 2017, 2016; Yaghmazadeh et al. 2018]. Generally
speaking, synthesis algorithms based on version space learning construct some sort of data structure
that represents all programs that are consistent with the examples. While existing version space
learning algorithms only work with input-output examples, the method proposed here works with
arbitrary ground formulas representing relational counterexamples and uses hierarchical finite tree
automata to compose the version spaces of individual functions.
   Program Inversion. Prior work has addressed the program inversion problem, where the goal
is to automatically generate the inverse of a given program [Chen and Udding 1990; Dijkstra
1982; Hu and D’Antoni 2017; Ross 1997; Srivastava et al. 2011]. Among these, the PINS tool uses
inductive synthesis to semi-automate the inversion process based on templates provided by the
user [Srivastava et al. 2011]. More recent work describes a fully automated technique, based on
symbolic transducers, to generate the inverse of a given program [Hu and D’Antoni 2017]. While
program inversion is one of the applications that we consider in this paper, relational synthesis is
applicable to many problems beyond program inversion. Furthermore, our approach can be used to
synthesize the program and its inverse simultaneously rather than requiring the user to provide
one of these functions.

9    LIMITATIONS
While we have successfully used the proposed relational synthesis method to synthesize encoder-
decoder pairs and comparators, our current approach has some limitations that we plan to address
in future work. First, our method only works with simple DSLs without recursion, loops, or let
bindings. That is, the programs that can be currently synthesized by Relish are compositions of
built-in functions provided by the DSL. Second, we only allow relational specifications of the form
∀®x .ϕ(®
       x) where ϕ is quantifier-free. Thus, our method does not handle more complex relational
specifications with quantifier alternation (e.g., ∀x .∃y.f (x, y) = д(y, x)).

10     CONCLUSION
In this paper, we have introduced relational program synthesis —the problem of synthesizing one
or more programs that collectively satisfy a relational specification— and described its numerous
applications in real-world programming scenarios. We have also taken a first step towards solving
this problem by presenting a CEGIS-based approach with a novel inductive synthesis component.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Relational Program Synthesis                                                                                          1:25

In particular, the key idea is to construct a relational version space (in the form of a hierarchical
finite tree automaton) that encodes all tuples of programs that satisfy the original specification.
   We have implemented this technique in a relational synthesis framework called Relish which
can be instantiated in different application domains by providing a suitable domain-specific lan-
guage as well as the relevant relational specifications. Our evaluation in two different application
domains (namely, encoders/decoders and comparators) demonstrate that Relish can effectively
synthesize pairs of closely related programs (i.e., inverses) as well as individual programs that must
obey non-trivial k-safety specifications (e.g., transitivity). Our evaluation also shows that Relish
significantly outperforms EUSolver, both in terms of the efficiency of inductive synthesis as well
as its generalization power per CEGIS iteration.

ACKNOWLEDGMENTS
We would like to thank Yu Feng, Kostas Ferles, Jiayi Wei, Greg Anderson, and the anonymous
OOPSLA’18 reviewers for their thorough and helpful comments on an earlier version of this paper.
This material is based on research sponsored by NSF Awards #1712067, #1811865, #1646522, and
AFRL Award #8750-14-2-0270. The views and conclusions contained herein are those of the authors
and should not be interpreted as necessarily representing the official policies or endorsements,
either expressed or implied, of the U.S. Government.

REFERENCES
Rajeev Alur, Rastislav Bodik, Garvit Juniwal, Milo MK Martin, Mukund Raghothaman, Sanjit A Seshia, Rishabh Singh,
    Armando Solar-Lezama, Emina Torlak, and Abhishek Udupa. 2013. Syntax-guided synthesis. In Proc. of FMCAD. 1–8.
Rajeev Alur, Arjun Radhakrishna, and Abhishek Udupa. 2017. Scaling Enumerative Program Synthesis via Divide and
    Conquer. In Proc. of TACAS. 319–336.
Gilles Barthe, Juan Manuel Crespo, and César Kunz. 2011. Relational verification using product programs. In Proc. of FM.
    Springer, 200–214.
Gilles Barthe, Juan Manuel Crespo, and César Kunz. 2013. Beyond 2-safety: Asymmetric product programs for relational
    program verification. In Proc. of LFCS. Springer, 29–43.
Gilles Barthe, Juan Manuel Crespo, and César Kunz. 2016. Product programs and relational program logics. Journal of
    Logical and Algebraic Methods in Programming 85, 5 (2016), 847–859.
Gilles Barthe, Pedro R D’Argenio, and Tamara Rezk. 2004. Secure information flow by self-composition. In Proc. of CSF.
    100–114.
Gilles Barthe, Benjamin Grégoire, and Santiago Zanella Béguelin. 2012a. Probabilistic relational Hoare logics for computer-
    aided security proofs. In International Conference on Mathematics of Program Construction. Springer, 1–6.
Gilles Barthe, Boris Köpf, Federico Olmedo, and Santiago Zanella Béguelin. 2012b. Probabilistic relational reasoning for
    differential privacy. In Proc. of POPL, Vol. 47. 97–110.
Nick Benton. 2004. Simple relational correctness proofs for static analyses and program transformations. In Proc. of POPL,
    Vol. 39. 14–25.
Jia Chen, Yu Feng, and Isil Dillig. 2017. Precise Detection of Side-Channel Vulnerabilities using Quantitative Cartesian
    Hoare Logic. In Proc. of CCS. 875–890.
Wei Chen and Jan Tijmen Udding. 1990. Program inversion: More than fun! Science of Comp. Prog. 15, 1 (1990), 1–13.
Hubert Comon. 1997. Tree automata techniques and applications. http://www. grappa. univ-lille3. fr/tata (1997).
Emanuele De Angelis, Fabio Fioravanti, Alberto Pettorossi, and Maurizio Proietti. 2016. Relational verification through horn
    clause transformation. In Proc. of SAS. Springer, 147–169.
Benjamin Delaware, Clément Pit-Claudel, Jason Gross, and Adam Chlipala. 2015. Fiat: Deductive synthesis of abstract data
    types in a proof assistant. In Proc. of POPL, Vol. 50. 689–700.
Edsger W Dijkstra. 1982. Program inversion. In Selected Writings on Computing: A Personal Perspective. Springer, 351–354.
John K. Feser, Swarat Chaudhuri, and Isil Dillig. 2015. Synthesizing data structure transformations from input-output
    examples. In Proc. of PLDI. 229–239.
Giorgio Gallo, Giustino Longo, Stefano Pallottino, and Sang Nguyen. 1993. Directed hypergraphs and applications. Discrete
    applied mathematics 42, 2-3 (1993), 177–201.
Cordell Green. 1969. Application of theorem proving to problem solving. In Proc. of IJCAI. 219–239.
Sumit Gulwani. 2011. Automating string processing in spreadsheets using input-output examples. In Proc. of POPL. 317–330.


                                  Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:26                                                                Yuepeng Wang, Xinyu Wang, and Isil Dillig

Sumit Gulwani. 2012. Synthesis from examples: Interaction models and algorithms. In Symbolic and Numeric Algorithms for
   Scientific Computing (SYNASC). 8–14.
Stefan Heule, Eric Schkufza, Rahul Sharma, and Alex Aiken. 2016. Stratified synthesis: automatically learning the x86-64
   instruction set. In Proc. of PLDI. 237–250.
Qinheping Hu and Loris D’Antoni. 2017. Automatic program inversion using symbolic transducers. In Proc. of PLDI. 376–389.
Barbara Jobstmann, Andreas Griesmayer, and Roderick Bloem. 2005. Program repair as a game. In Proc. of CAV. 226–238.
Etienne Kneuss, Ivan Kuraj, Viktor Kuncak, and Philippe Suter. 2013. Synthesis modulo recursive functions. Proc. of OOPSLA
   48, 10 (2013), 407–426.
Tessa Lau, Steven A. Wolfman, Pedro Domingos, and Daniel S. Weld. 2003. Programming by Demonstration Using Version
   Space Algebra. Machine Learning 53, 1-2 (2003), 111–156.
Zohar Manna and Richard Waldinger. 1986. A deductive approach to program synthesis. In Readings in artificial intelligence
   and software engineering. Elsevier, 3–34.
Tom M Mitchell. 1982. Generalization as search. Artificial intelligence 18, 2 (1982), 203–226.
Dmitry Mordvinov and Grigory Fedyukovich. 2017. Synchronizing constrained Horn clauses. LPAR, EPiC Series in Computing
   (2017).
Carroll Morgan. 1994. Programming from specifications. Prentice Hall.
Hoang Duong Thien Nguyen, Dawei Qi, Abhik Roychoudhury, and Satish Chandra. 2013. Semfix: Program repair via
   semantic analysis. In Proc. of ICSE. 772–781.
Nadia Polikarpova, Ivan Kuraj, and Armando Solar-Lezama. 2016. Program synthesis from polymorphic refinement types.
   In Proc. of PLDI. 522–538.
Oleksandr Polozov and Sumit Gulwani. 2015. FlashMeta: A framework for inductive program synthesis. In Proc. of OOPSLA,
   Vol. 50. 107–126.
Veselin Raychev, Pavol Bielik, Martin T. Vechev, and Andreas Krause. 2016. Learning programs from noisy data. In Proc. of
   POPL. 761–774.
Veselin Raychev, Martin T. Vechev, and Andreas Krause. 2015. Predicting Program Properties from "Big Code". In Proc. of
   POPL. 111–124.
Brian J Ross. 1997. Running programs backwards: the logical inversion of imperative computation. Formal Aspects of
   Computing 9, 3 (1997), 331–348.
Eric Schkufza, Rahul Sharma, and Alex Aiken. 2013. Stochastic superoptimization. In Proc. of ASPLOS. 305–316.
Sunbeom So and Hakjoo Oh. 2017. Synthesizing Imperative Programs from Examples Guided by Static Analysis. In Proc. of
   SAS. 364–381.
Armando Solar-Lezama. 2008. Program synthesis by sketching. University of California, Berkeley.
Armando Solar-Lezama. 2009. The sketching approach to program synthesis. In Proc. of APLAS. Springer, 4–13.
Armando Solar-Lezama, Liviu Tancau, Rastislav Bodik, Sanjit Seshia, and Vijay Saraswat. 2006. Combinatorial sketching for
   finite programs. Proc. of ASPLOS 41, 11 (2006), 404–415.
Marcelo Sousa and Isil Dillig. 2016. Cartesian hoare logic for verifying k-safety properties. In Proc. of PLDI. 57–69.
Marcelo Sousa, Isil Dillig, and Shuvendu K. Lahiri. 2018. Verified Three-Way Program Merge. PACMPL OOPSLA (2018).
Marcelo Sousa, Isil Dillig, Dimitrios Vytiniotis, Thomas Dillig, and Christos Gkantsidis. 2014. Consolidation of queries with
   user-defined functions. In Proc. of PLDI, Vol. 49. 554–564.
Saurabh Srivastava, Sumit Gulwani, Swarat Chaudhuri, and Jeffrey S Foster. 2011. Path-based inductive synthesis for
   program inversion. In Proc. of PLDI, Vol. 46. 492–503.
Xinyu Wang, Isil Dillig, and Rishabh Singh. 2017. Synthesis of data completion scripts using finite tree automata. PACMPL
   1, OOPSLA (2017), 62:1–62:26.
Xinyu Wang, Isil Dillig, and Rishabh Singh. 2018a. Program synthesis using abstraction refinement. PACMPL 2, POPL (2018),
   63:1–63:30.
Xinyu Wang, Sumit Gulwani, and Rishabh Singh. 2016. FIDEX: filtering spreadsheet data using examples. In Proc. of OOPSLA.
   195–213.
Yuepeng Wang, Isil Dillig, Shuvendu K. Lahiri, and William R. Cook. 2018b. Verifying equivalence of database-driven
   applications. PACMPL 2, POPL (2018), 56:1–56:29.
Navid Yaghmazadeh, Xinyu Wang, and Isil Dillig. 2018. Automated Migration of Hierarchical Data to Relational Tables
   using Programming-by-Example. Proc. of VLDB 11, 5 (2018), 580–593.
Hongseok Yang. 2007. Relational separation logic. Theoretical Computer Science 375, 1-3 (2007), 308–334.
Anna Zaks and Amir Pnueli. 2008. Covac: Compiler validation by program analysis of the cross-product. In Proc. of FM.
   Springer, 35–51.




Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Relational Program Synthesis                                                                                      1:27

A    PROOF OF THEOREMS
  Lemma A.1. Suppose FTA A = (Q, Σ, Q f , ∆) is built with grammar G and initial states [Q 1 , . . . , Qm ]
using rules from Figure 8. Given a tree t(x 1 , . . . , xm ) that is accepted by A, we have
  (1) t conforms to grammar G.
  (2) The accepting run of t with x i = c i , where qcxii ∈ Q i , is rooted with final state qsc and c =
      Jt(c 1 , . . . , cm )K.
   Proof. To prove by induction on height of t, we first strengthen (2) to: the run of t with x i = c i
is rooted with state qsc and c = Jt(c 1 , . . . , cm )K.
     • Base case: height is 1. In this case, t only has one variable x, and qsc is passed as an input.
       Consider the Input rule in Figure 8, we know qcx ∈ Q and x → qcx ∈ ∆. Given t is accepted
       by A, qcx is a final state, so x conforms to grammar G. The run has only one node qcx , and
       c = Jt(c)K.
     • Inductive case: Suppose the lemma is correct for term with height no larger than h, and the
       goal is to prove it is correct for term t of height h + 1. Without loss of generality, assume
       t = σ (t 1 , . . . , tn ) is of height h + 1, so the height of terms t 1 , . . . , tn is at most h. By inductive
       hypothesis, ti conforms to grammar G for i ∈ [1, n]. Furthermore, the run of ti is rooted
       with state qsaii where ai = Jti K on environment {x j 7→ c j | j ∈ [1, m]}. Based on the Prod
       rule in Figure 8, we know the transition σ (qsa11 , . . . , qsann ) → qsc is only added to ∆ if there is
       production σ (s 1 , . . . , sn ) → s in grammar G and c = Jσ (a 1 , . . . , an )K. Therefore, t conforms
       to grammar G and the run of t with x i = c i is rooted with state qsc and c = Jt(c 1 , . . . , cm )K.
Since term t is accepted by A, we know qsc is a final state, which concludes the proof.                               □

   Lemma A.2. Suppose G, M ⊢ t { H according to the rules from Figure 7, where t is a term, and
let f 1 , . . . , fn be the function symbols used in t. Given a hierarchical tree T = (V , ϒ, vr , E) that is
accepted by H , we have:
   (1) ϒ(v fi ) is a program that conforms to grammar G(M −1 (fi ))
                                                                 Jt K
   (2) The run of ϒ(vr ) on Ω(vr ) is rooted with final state qs .
    Proof. Prove by structural induction on t.
     • Base case: t = c. According to the Const rule in Figure 7, the HFTA H from t contains only a
       single node vc , so the root node is also vc . The FTA Ω(vc ) is
                                        Jc K         Jc K      Jc K
                                 A = ( qc , {c}, qc , c → qc )
       Given T = (V , ϒ, vr , E) accepted by H , we know tree ϒ(vc ) is accepted by FTA Ω(vc ) by
                                                                  Jc K
       Definition 4.1. The run of ϒ(vc ) is a single node qc .
     • Inductive case: t = f (t 1 , . . . , tm ). Suppose G, M ⊢ ti { Hi = (Vi , Ωi , vr i , Λi ) for i ∈
       [1, m]. Given a hierarchical tree T = (V , ϒ, vr , E) accepted by H , we denote its ti part as
       Ti = (Vi , ϒi , vr i , Ei ). On one hand, V = ∪m                            m
                                                         i=1Vi ∪ {v f }. E = ∪i=1 E i ∪ {(v f , v r i ) | i ∈ [1, m]}.
       ϒi (v) = ϒ(v) for all v ∈ Vi . On the other hand,we have Ωi (v) = Ω(v) for all v ∈ Vi based on
       the Func rule in Figure 7. Also, Λ = ∪m                  c       c      c
                                                    i=1 Λi ∪ q s i → q x i | q s i ∈ Q f i , i ∈ [1, m] where Q f i is
       the final state set of Ω(vr i ).
           According to the acceptance condition of Definition 4.1, we know Ti is accepted by Hi for all
       i ∈ [1, m]. By inductive hypothesis, we have ϒi (v fi ) conforms to grammar G(M −1 (fi )) for all
       v fi ∈ Vi . Moreover, we have proved ϒ(v f ) conforms to grammar G(M −1 (f )) in Lemma A.1.
       Therefore, any function symbol fi in t conforms to its grammar G(M −1 (fi )). Again, by
                                                                                                              Jt K
       inductive hypothesis, we have the run of ϒi (vr i ) on Ωi (vr i ) is rooted with final state qsi i for

                                 Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:28                                                              Yuepeng Wang, Xinyu Wang, and Isil Dillig

      i ∈ [1, m]. Based on Lemma A.1, the run of ϒ(v f ) on Ω(v f ) is rooted with final state qsc where
      c = Jt(Jti K, . . . , Jtm K)K = JtK. Hence, the lemma is proved for t = f (t 1 , . . . , tm ).
By principle of structural induction, we have proved the lemma.                                       □
   Lemma A.3. Suppose G, M ⊢ Φ { H according to the rules from Figure 7, where Φ is a ground
formula, and let f 1 , . . . , fn be the function symbols used in Φ. Given a hierarchical tree T = (V , ϒ, vr , E)
that is accepted by H , we have:
   (1) ϒ(v fi ) is a program that conforms to grammar G(M −1 (fi ))
   (2) If the run of ϒ(vr ) on Ω(vr ) is rooted with final state qs⊤0 , then ϒ(v f1 ), . . . , ϒ(v fn ) |= Φ
   (3) If the run of ϒ(vr ) on Ω(vr ) is rooted with final state qs⊥0 , then ϒ(v f1 ), . . . , ϒ(v fn ) ̸ |= Φ
   Proof. Prove by structural induction on Φ.
    • Base case: Φ = t 1 op t 2 . Suppose G, M ⊢ t 1 { H1 = (V1 , Ω1 , vr 1 , Λ1 ) and G, M ⊢ t 2 { H2 =
      (V2 , Ω2 , vr 2 , Λ2 ). Given a hierarchical tree T = (V , ϒ, vr , E) accepted by H , we denote its
      t 1 part as T1 = (V1 , ϒ1 , vr 1 , E 1 ) and denote the t 2 part as T2 = (V2 , ϒ2 , vr 2 , E 2 ). On one hand,
      V = V1 ∪ V2 ∪ {vop }. E = E 1 ∪ E 2 ∪ {(vop , vr 1 ), (vop , vr 2 )}. ϒi (v) = ϒ(v) for all v ∈ Vi where
      i = 1, 2. On the other hand, we have Ωi (v) =Ω(v) for all v ∈ Vi where i = 1, 2 based on the
      Logical rule in Figure 7. Also, Λ = Λ1 ∪ Λ2 ∪ qsci → qcx i | qsci ∈ Q fi , i = 1, 2 where Q fi is the
      final state set of Ω(vr i ).
          According to the acceptance condition of Definition 4.1, we know T1 is accepted by H1
      and T2 is accepted by H2 . By Lemma A.2, we have ϒi (v f ) conforms to grammar G(M −1 (f ))
      for all v f ∈ Vi where i = 1, 2. Therefore, any function symbol fi in Φ conforms to its
      grammar G(M −1 (fi )). Also by Lemma A.2, we have the run of ϒi (vr i ) on Ωi (vr i ) is rooted
                              Jt K
      with    final state qsi i for i = 1, 2. In addition, consider that Logical rule will add transitions
              c1 c2
        op(q x 1 , q x 2 ) → qsc0 | c = JopK(c 1 , c 2 ) to Ω(vr ), the run will reach state qs⊤0 if t 1 op t 2 evaluates
      

      to true and reach state qs⊥0 otherwise. Hence, the lemma is proved for Φ = t 1 op t 2 .
    • Inductive case: Φ = Φ1 ⊙ Φ2 (⊙ = ∧, ∨). Suppose G, M ⊢ Φ1 { H1 = (V1 , Ω1 , vr 1 , Λ1 ) and
      G, M ⊢ Φ2 { H2 = (V2 , Ω2 , vr 2 , Λ2 ). Given a hierarchical tree T = (V , ϒ, vr , E) accepted by
      H , we denote its Φ1 part as T1 = (V1 , ϒ1 , vr 1 , E 1 ) and denote the Φ2 part as T2 = (V2 , ϒ2 , vr 2 , E 2 ).
      On one hand, V = V1 ∪ V2 ∪ {v ⊙ }. E = E 1 ∪ E 2 ∪ {(v ⊙ , vr 1 ), (v ⊙ , vr 2 )}. ϒi (v) = ϒ(v) for all
      v ∈ Vi where i = 1, 2. On the other hand, we have Ωi (v) = Ω(v)               for all v ∈ Vi where i = 1, 2
      based on the Logical rule in Figure 7. Also, Λ = Λ1 ∪ Λ2 ∪ qsci → qcx i | qsci ∈ Q fi , i = 1, 2
      where Q fi is the final state set of Ω(vr i ).
          According to the acceptance condition of Definition 4.1, we know T1 is accepted by H1
      and T2 is accepted by H2 . By inductive hypothesis, we have ϒi (v f ) conforms to grammar
      G(M −1 (f )) for all v f ∈ Vi where i = 1, 2. Therefore, any function symbol fi in Φ conforms to
      its grammar G(M −1 (fi )). Also by inductive hypothesis, we know that if the run of ϒi (vr i ) on
      Ωi (vr i ) is rooted with final state qs⊤i then ϒi (v fi ), v fi ∈ Vi collectively satisfy Φi for i = 1, 2. In
      addition, the Logical rule is essentially building an FTA that accepts programs with boolean
      input value JΦ1 K and JΦ2 K. The run is rooted with qs⊤0 if JΦ1 K⊙JΦ2 K evaluates to true; otherwise,
      the run is rooted with qs⊥0 . Hence, the lemma is proved for Φ = Φ1 ⊙ Φ2 .
    • Inductive case: Φ = ¬Φ1 . Suppose G, M ⊢ Φ1 { H1 = (V1 , Ω1 , vr 1 , Λ1 ). Given a hierarchical
      tree T = (V , ϒ, vr , E) accepted by H , we denote its Φ1 part as T1 = (V1 , ϒ1 , vr 1 , E 1 ). On one
      hand, V = V1 ∪ {v ¬ }. E = E 1 ∪ {(v ¬ , vr 1 )}. ϒ1 (v) = ϒ(v) for all v ∈ V1 . On the other hand,          we
      have Ω1 (v) = Ω(v) for all v ∈ V1 based on the Neg rule in Figure 7. Also, Λ = Λ1 ∪ qsc →
      qcx 1 | qsc ∈ Q f1 where Q f1 is the final state set of Ω(vr 1 ).
          According to the acceptance condition of Definition 4.1, we know T1 is accepted by H1 .
      By inductive hypothesis, we have ϒ1 (v f ) conforms to grammar G(M −1 (f )) for all v f ∈

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Relational Program Synthesis                                                                                              1:29

      V1 . Therefore, any function symbol fi in Φ conforms to its grammar G(M −1 (fi )). Also by
                                                                                                    Jt K
      inductive hypothesis, we have the run of ϒ1 (vr 1 ) on Ω1 (vr 1 ) is rooted with final state qs1 1 . In
      addition, the Neg rule is building an FTA that accepts programs with boolean input value
      JΦ1 K. The run is rooted with qs⊤0 if ¬JΦ1 K evaluates to true; otherwise, the run is rooted with
      qs⊥0 . Hence, the lemma is proved for Φ = ¬Φ1 .
By principle of structural induction, we have proved the lemma.                                             □
   Proof of Theorem 5.2. Suppose G, M ⊢ Φ ↠ H and H = (V , Ω, vr , Λ), we know G, M ⊢ Φ {
H ′ with H ′ = (V , Ω ′, vr , Λ) according to the Final rule in Figure 7. The only difference between
Ω and Ω ′ is that Ω(vr ) = (Q, Σ, {qs⊤0 }, ∆) but Ω ′(vr ) = (Q, Σ, {qs⊤0 , qs⊥0 }, ∆). By Definition 4.1, we
know L(H ) ⊆ L(H ′). Thus, if hierarchical tree T is accepted by H , then T is also accepted by
H ′. According to Lemma A.3, we have ϒ(v fi ) conforms to grammar G(M −1 (fi )). In addition, we
have ϒ(v f1 ), . . . , ϒ(v fn ) |= Φ if the run of ϒ(vr ) is rooted with final state qs⊤0 . Since H only has one
final state qs⊤0 in Ω(vr ), we know the accepting run of ϒ(vr ) on Ω(vr ) must be rooted with qs⊤0 . Thus,
ϒ(v f1 ), . . . , ϒ(v fn ) |= Φ.                                                                               □
   Lemma A.4. Suppose FTA A = (Q, Σ, Q f , ∆) is built with grammar G and initial states [Q 1 , . . . , Qm ]
using rules from Figure 8. If there is a program P that conforms to grammar G such that JPK(a 1 , . . . , am ) =
a where qsaii ∈ Q i for i ∈ [1, m], then there exists a tree accepted by A and the run is rooted with final
state qsa from initial states q xa11 , . . . , q xam
                                                   m
                                                     .
   Proof. To prove by induction on height of P’s AST, we first strengthen the lemma to: the run of
tree t is rooted with state qsa from initial states q xa11 , . . . , q xam     m
                                                                                  where a = JtK(a 1 , . . . , am ).
    • Base case: height is 1. In this case, P only has one variable x, and qsc is passed as an input.
       Consider the Input rule in Figure 8, we know qcx ∈ Q and x → qcx ∈ ∆. Then x is accepted by
       A, and the run is rooted with final state qcx .
    • Inductive case: Suppose the lemma is correct for AST with height no larger than h, and the
       goal is to prove it is correct for AST of height h + 1. Without loss of generality, assume
       P = σ (P 1 , . . . , Pn ) is of height h + 1, so the height of partial programs P 1 , . . . , Pn is at most h.
       By inductive hypothesis, there exists trees t 1 , . . . , tn whose runs are rooted with state qscii form
       initial states q xa11 , . . . , q xam
                                           m
                                             , and Jti K = c i for all i ∈ [1, n]. According to the Prod rule in Figure 8,
       we know the run of t = σ (t 1 , . . . , tn ) is rooted with state Jσ (Jt 1 K, . . . , Jtn K)K = Jσ (c 1 , . . . , c n )K.
       Hence, the inductive case is proved.
Consider P is a program (not partial program), if the run of tree t is rooted with state qsa , then s
must be a starting symbol. By the Output rule in Figure 8, qsa is a final state. Therefore, tree t is
accepted by A, and we have proved the lemma.                                                                                 □
   Lemma A.5. Let t be a term where every function symbol f 1 , . . . , fn occurs exactly once, and suppose
we have G, M ⊢ t { H . If there are implementations Pi of fi such that JtK = a, where Pi conforms
to grammar G(M −1 (fi )), then there exists a hierarchical tree T = (V , ϒ, vr , E) accepted by H such
that ϒ(v fi ) = Pi for all i ∈ [1, n], and the run of ϒ(vr ) on Ω(vr ) is rooted with final state qsa .
   Proof. Prove by structural induction on t.
    • Base case: t = c. Suppose the HFTA built from Const rule in Figure 7 is H = ({vc }, Ω, vc , Λ)
      and Ω(vc ) is
                                      Jc K       Jc K         Jc K
                               A = ( qc , {c}, qc , c → qc )
      Consider the hierarchical tree T = ({vc }, ϒ, vc , ∅) where ϒ(vc ) is a tree that only contains a
      single node c. By Definition 4.1, T is accepted by H and the run of ϒ(vc ) on Ω(vc ) is rooted
                        Jc K
      with final state qc .

                                   Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:30                                                             Yuepeng Wang, Xinyu Wang, and Isil Dillig

    • Inductive case: t = f (t 1 , . . . , tm ). Given G, M ⊢ t { H = (V , Ω, v f , Λ), we denote its ti part
      as Hi = (Vi , Ωi , vr i , Λi ) for i ∈ [1, m]. In addition, we have Vi (vi ) = V (vi ) and Ωi (vi ) = V (vi )
      for all node vi ∈ Vi . Λi ⊂ Λ. Note that the ti part is recognized by inter-FTA transition
      qsc → qcx i ∈ Λ where qsc is a state in Ωi (vr i ) and qcx i is a state in Ω(v f ). According to the Func
      rule in Figure 7, we have G, M ⊢ ti { Hi for i ∈ [1, m]. By inductive hypothesis, we know
      there exists a hierarchical tree Ti = (Vi , ϒi , vr i , Ei ) accepted by Hi and the run of ϒi (vr i ) on
                                                  Jt K
      Ωi (vr i ) is rooted with final state qsi i for all i ∈ [1, m]. Moreover, by Lemma A.4, we know
      there exists a tree Tf accepted by Ω(v f ) and the run is rooted with final state qsa from initial
                 Jt K         Jt K
      states qs1 1 , . . . , qsmm , where a = Jf (Jt 1 K, . . . , Jtm K)K. Now consider the hierarchical tree
                 T = (∪m                m                             m
                       i=1Vi ∪ {v f }, ∪i=1 ϒi ∪ {v f 7→ Tf }, v f , ∪i=1 (E i ∪ {(v f , v r i )}))
      By acceptance condition of HFTA in Defintion 4.1, T is accepted by H . Thus, the lemma is
      proved for t = f (t 1 , . . . , tm ) case.
By principle of structural induction, we have proved the lemma.                              □
  Lemma A.6. Let Φ be a ground formula where every function symbol f 1 , . . . , fn occurs exactly once,
and suppose we have G, M ⊢ Φ { H . If there are implementations Pi of fi where Pi conforms to
grammar G(M −1 (fi )), then there exists a hierarchical tree T = (V , ϒ, vr , E) accepted by H such that
ϒ(v fi ) = Pi for all i ∈ [1, n], and
  (1) If P1 , . . . , Pn |= Φ, the run of ϒ(vr ) on Ω(vr ) is rooted with final state qs⊤0 .
  (2) If P1 , . . . , Pn ̸ |= Φ, the run of ϒ(vr ) on Ω(vr ) is rooted with final state qs⊥0 .
   Proof. Prove by structural induction on Φ.
    • Base case: Φ = t 1 op t 2 . Given G, M ⊢ t { H = (V , Ω, vop , Λ), we denote its ti part as
      Hi = (Vi , Ωi , vr i , Λi ) for i = 1, 2. In addition, we have Vi (vi ) = V (vi ) and Ωi (vi ) = V (vi )
      for all node vi ∈ Vi . Λi ⊂ Λ. Note that the ti part is recognized by inter-FTA transition
      qsc → qcx i ∈ Λ where qsc is a state in Ωi (vr i ) and qcx i is a state in Ω(vop ). According to the
      Logical rule in Figure 7, we have G, M ⊢ ti { Hi for i = 1, 2. By Lemma A.5, we know
      there exists a hierarchical tree Ti = (Vi , ϒi , vr i , Ei ) accepted by Hi and the run of ϒi (vr i ) on
                                                 Jt K
      Ωi (vr i ) is rooted with final state qsi i for i = 1, 2. Moreover, based on the Logical rule, we
      know there exists a tree Top = op(x 1 , x 2 ) accepted by Ω(vop ). The run is rooted with qs⊤0 if
      Jt 1 K op Jt 2 K evaluates to true (i.e., P 1 , . . . , Pn |= t 1 opt 2 ); the run is rooted with qs⊥0 otherwise.
      Now consider the hierarchical tree
       T = (V1 ∪ V2 ∪ {vop }, ϒ1 ∪ ϒ2 ∪ {vop 7→ Top }, vop , E 1 ∪ E 2 ∪ {(vop , vr 1 ), (vop , vr 2 )}))
      By acceptance condition of HFTA in Defintion 4.1, T is accepted by H . Thus, the lemma is
      proved for Φ = t 1 op t 2 .
    • Inductive case: Φ = Φ1 ⊙ Φ2 (⊙ = ∧, ∨). Given G, M ⊢ t { H = (V , Ω, v ⊙ , Λ), we denote
      its Φi part as Hi = (Vi , Ωi , vr i , Λi ) for i = 1, 2. In addition, we have Vi (vi ) = V (vi ) and
      Ωi (vi ) = V (vi ) for all node vi ∈ Vi . Λi ⊂ Λ. Note that the Φi part is recognized by inter-FTA
      transition qsc → qcx i ∈ Λ where qsc is a state in Ωi (vr i ) and qcx i is a state in Ω(v ⊙ ). According
      to the Logical rule in Figure 7, we have G, M ⊢ Φi { Hi for i = 1, 2. By inductive hypothesis,
      we know there exists a hierarchical tree Ti = (Vi , ϒi , vr i , Ei ) accepted by Hi and the run
      of ϒi (vr i ) on Ωi (vr i ) is rooted with final state qs⊤0 if Φi is satisfied; the run is rooted with
      final state qs⊤0 otherwise. Moreover, based on the Logical rule, we know there exists a tree
      T ⊙ = ⊙(x 1 , x 2 ) accepted by Ω(v ⊙ ). The run is rooted with qs⊤0 if JΦ1 K ⊙ JΦ2 K evaluates to true,
      but rooted with qs⊥0 otherwise. Now consider the hierarchical tree
          T = (V1 ∪ V2 ∪ {v ⊙ }, ϒ1 ∪ ϒ2 ∪ {v ⊙ 7→ T ⊙ }, v ⊙ , E 1 ∪ E 2 ∪ {(v ⊙ , vr 1 ), (v ⊙ , vr 2 )})

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Relational Program Synthesis                                                                                     1:31

      By acceptance condition of HFTA in Defintion 4.1, T is accepted by H . Thus, the lemma is
      proved for Φ = Φ1 ⊙ Φ2 .
   • Inductive case: Φ = ¬Φ1 . Given G, M ⊢ t { H = (V , Ω, v ¬ , Λ), we denote its Φ1 part as
      H1 = (V1 , Ω1 , vr 1 , Λ1 ). In addition, we have V1 (v 1 ) = V (v 1 ), Ω1 (v 1 ) = V (v 1 ), and Λ1 ⊂ Λ.
      Note that the Φ1 part is recognized by inter-FTA transition qsc → qcx 1 ∈ Λ where qsc is
      a state in Ω1 (vr 1 ) and qcx 1 is a state in Ω(v ¬ ). According to the Neg rule in Figure 7, we
      have G, M ⊢ Φ1 { H1 . By inductive hypothesis, we know there exists a hierarchical tree
      T1 = (V1 , ϒ1 , vr 1 , E 1 ) accepted by H1 and the run of ϒ1 (vr 1 ) on Ω1 (vr 1 ) is rooted with final state
      qs⊤0 if Φ1 is satisfied; the run is rooted with final state qs⊤0 otherwise. Moreover, based on the
      Neg rule, we know there exists a tree T¬ = ¬(x 1 ) accepted by Ω(v ¬ ). The run is rooted with
      qs⊤0 if ¬JΦ1 K evaluates to true, but rooted with qs⊥0 otherwise. Now consider the hierarchical
      tree
                           T = (V1 ∪ {v ¬ }, ϒ1 ∪ {v ¬ 7→ T¬ }, v ¬ , E 1 ∪ {(v ¬ , vr 1 )})
      By acceptance condition of HFTA in Defintion 4.1, T is accepted by H . Thus, the lemma is
      proved for Φ = ¬Φ1 .
By principle of structural induction, we have proved the lemma.                                                   □
   Proof of Theorem 5.3. Suppose G, M ⊢ Φ ↠ H and H = (V , Ω, vr , Λ), we have G, M ⊢ Φ {
H ′ with H ′ = (V , Ω ′, vr , Λ) according to the Final rule in Figure 7. The only difference between
Ω and Ω ′ is that Ω(vr ) = (Q, Σ, {qs⊤0 }, ∆) but Ω ′(vr ) = (Q, Σ, {qs⊤0 , qs⊥0 }, ∆). By Lemma A.6, we
know there exists a hierarchical tree T = (V , ϒ, vr , E) accepted by H ′ such that ϒ(v fi ) = Pi for all
i ∈ [1, n]. Furthermore, since P1 , . . . , Pn |= Φ, we know the run of ϒ(vr ) on Ω(vr ) is rooted with
final state qs⊤0 . Since qs⊤0 is also a final state in Ω ′(vr ), the run of ϒ(vr ) on FTA Ω(vr ) is the same as
the run of ϒ(vr ) on FTA Ω ′(vr ). According to the HFTA accepting condition in Definition 4.1, T is
also accepted by H .                                                                                         □
  Lemma A.7. Suppose we have a ground relational specification Φ, its relaxation Φ′ with symbol
mapping M, and an HFTA H built from Φ′, M and grammars G. If the FindProgs procedure returns
programs P (not null) given input H and M, then P satisfy Φ, and program Pi for function fi
conforms to the grammar G(fi ).
   Proof. If FindProgs actually returns programs P, then there must be a hierarchical tree T =
(V , ϒ, vr , E) accepted by H . Otherwise, it will skip the for loop and directly return null. For ease
of illustration, we assign H0 = H and assign T0 = T = (V , ϒ0 , vr , E). Observe that the FindProgs
procedure assigns one program to a function symbol at a time, and terminates when all function
symbols are successfully assigned. Without loss of generality, we assume the function symbols are
assigned in the order of f 1 , . . . , fn . We denote by Ti = (V , ϒi , vr , E) the hierarchical tree and ϒi is
obtained by substituting all ϒi−1 (v fi′ ) in Ti−1 with program tree Pi , where fi′ is a symbol in M(fi ).
We also denote the HFTA of invoking Propagate(Hi−1 , Pi , fi , M) by Hi .
   To prove programs P 1 , . . . , Pn in P satisfy Φ and program Pi for function fi conforms to grammar
G(fi ), consider the following invariant: For any integer i ∈ [0, n],
   (1) L(Hi ) ⊆ L(H ).
   (2) For all k ≤ i, function symbol fk in original ground specification Φ is consistently assigned
        to program Pk , i.e. Pk = ϒi (v fk′ ) for all fk′ ∈ M(fk ).
First, let us prove it is indeed an invariant.
    • Base case: i = 0. Given H0 = H , we have L(H0 ) ⊆ L(H ). (2) trivially holds because no
        program has been assigned for i = 0.
    • Inductive case: Suppose (1)(2) hold for i = j, the goal is to prove they also hold for i = j + 1.

                                Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:32                                                             Yuepeng Wang, Xinyu Wang, and Isil Dillig

     (1) Since Propagate will only remove final states and inter-FTA transitions from Hj , we know
          L(Hj+1 ) ⊆ L(Hj ) by acceptance condition in Definition 4.1. Since L(Hj ) ⊆ L(H ) by
          inductive hypothesis, we have L(Hj+1 ) ⊆ L(H ).
     (2) By definition of Tj+1 , ϒj+1 (v f j′+1 ) = P j+1 holds for all f j+1
                                                                           ′  ∈ M(f j+1 ). Also by inductive
          hypothesis, we know for all k ≤ j, Pk = ϒk (v fk′ ). Thus, for all k ≤ j +1, we have Pk = ϒk (v fk′ )
          for all fk′ ∈ M(fk ).
   After assigning programs to all function symbols, we have
   (1) L(Hn ) ⊆ L(H ).
   (2) For all function symbol fi in Φ, function occurrences fi′ are consistently assigned to program
        Pi for all fi′ ∈ M(fi ).
   Since the programs P are accepted by the last HFTA Hn , i.e. Tn ∈ L(Hn ) (otherwise Propagate
would return null due to the recurrent failure of emptiness check on Hn , we have Tn ∈ L(H ).
By Theorem 5.2, we have ϒ(v fi′ ) conforms to grammar G(M −1 (fi )) and ϒ(v f1′ ), . . . , ϒ(v fn′ ) |= Φ′.
Consider the fact that fi = M −1 (fi′) ⇔ fi′ ∈ M(fi ) and the only difference between Φ and Φ′
is captured by M, we have proved P1 , . . . , Pn |= Φ and Pi for function fi conforms to grammar
G(fi ).                                                                                                     □
   Proof of Theorem 5.5. Observe the Synthesize procedure shown in Algorithm 1 can only
return a set of programs P after it invokes the Verify procedure and successfully verifies P indeed
satisfy the relational specification Ψ. Thus, the programs P returned by Synthesize are guaranteed
to satisfy Ψ. In addition, observe that Algorithm 1 only has two ways to generate candidate programs
that may be potentially returned after verification.
   (1) Randomly generate programs Prandom that conform to context-free grammars G in the
       initialization phase.
   (2) Generate programs Pres by the FindProgs procedure. According to Lemma A.7, for program
       Pi of function fi in Pres , program Pi conforms to the grammar G(fi ).
Put two cases together, we have program Pi of function symbol fi conforms to grammar G(fi ). □
  Lemma A.8. Suppose we have a ground relational specification Φ, its relaxation Φ′ with symbol
mapping M, and an HFTA H built from Φ′, M, and grammars G. If there exist a set of programs
that (a) satisfy Φ and (b) can be implemented using the DSLs given by G, then invoking FindProgs on
H and M will eventually return programs P satisfying Φ.
  Proof. Suppose there exist a set of programs that satisfy Φ and can be implemented using the
DSLs given by G, we denote the program for function fi by Pi . Given that the relationship between
Φ and Φ′ is captured by mapping M, and fi = M −1 (fi′) ⇔ fi′ ∈ M(fi ), we know that assigning
program Pi for all fi′ if fi′ ∈ M(fi ) would satisfy Φ′, and Pi conforms to grammar G(M −1 (fi′). By
Theorem 5.3, we know there exists a hierarchical tree T = (V , ϒ, vr , E) accepted by H such that
ϒ(v fi′ ) = Pi for any i ∈ [1, n]. Observe that the FindProgs procedure essentially employs standard
backtrack search and may potentially enumerate all possible hierarchical trees accepted by H , it
will eventually find T and thus return the program set P.                                          □
   Proof of Theorem 5.6. Suppose the ground relational specification obtained by i-th loop itera-
tion of Algorithm 1 is denoted by Φi , and Φ0 = ⊤, let us first prove that Ψ ⇒ Φi for any natural
number i by induction on i.
    • Base case: i = 0. Ψ ⇒ ⊤ holds obviously.
    • Inductive case: Suppose Ψ ⇒ Φi−1 holds, we would like to prove Ψ ⇒ Φi . Given Φi = Φi−1 ∧
      GetRelationalCounterexample(P, Ψ), and consider that Ψ ⇒ GetRelationalCounterexample(P, Ψ)

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Relational Program Synthesis                                                                                  1:33

       because the counterexamples are obtained by instantiating the universal quantifiers in Ψ, we
       have Ψ ⇒ Φi .
According to the principle of induction, Ψ ⇒ Φi holds for any natural number i. If there exist
programs P that satisfy Ψ and P can be implemented using the DSLs given by G, then programs
P also satisfy Φi for any i. By Lemma A.8, we know the FindProgs procedure will always return
programs satisfying Φi . Since the Algorithm 1 will not terminate until it finds a set of programs that
satisfy Ψ or the FindProgs procedure fails to find any programs, and we have proved FindProgs
will never return failure, we can conclude that Algorithm 1 will eventually terminate with programs
satisfying Ψ.                                                                                        □

B   COMPLEXITY ANALYSIS
The complexity of our inductive synthesis algorithm is parametrized by 1) the number of functions
to synthesize, 2) the size of ground relational specification, 3) the size of largest FTA in the HFTA,
and 4) the bound of AST size for programs under consideration. Specifically, the ground relational
specification can be relaxed in linear time O(k), where k is the size of ground relational specification.
Since the HFTA may contain at most k FTAs, it can be constructed in O(km) time, where m is the
size of largest FTA in the HFTA. In particular, m = Σδ ∈∆ |δ | where |δ | = w + 1 for a transition δ of
the form σ (q 1 , . . . , qw ) → q. Observe that FindProgs is a backtracking search procedure, its worst
case complexity is O(mbn ) where n is the number of functions to synthesize, and b is the bound of
AST size for all programs under consideration. Therefore, the overall complexity is O(km + mbn ).




                             Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
