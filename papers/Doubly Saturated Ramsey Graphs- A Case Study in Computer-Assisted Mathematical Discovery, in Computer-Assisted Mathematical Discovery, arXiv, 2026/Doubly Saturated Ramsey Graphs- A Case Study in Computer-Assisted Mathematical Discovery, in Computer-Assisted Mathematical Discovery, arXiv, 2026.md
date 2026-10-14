                                           Doubly Saturated Ramsey Graphs: A Case Study
                                            in Computer-Assisted Mathematical Discovery

                                                              Benjamin Przybocki , John Mackey ,
                                                        Marijn J. H. Heule , and Bernardo Subercaseaux

                                                             Carnegie Mellon University, Pittsburgh, USA
arXiv:2604.21187v1 [math.CO] 23 Apr 2026




                                                        {bprzyboc,jmackey,mheule,bsuberca}@andrew.cmu.edu



                                                 Abstract. Ramsey-good graphs are graphs that contain neither a clique
                                                 of size s nor an independent set of size t. We study doubly saturated
                                                 Ramsey-good graphs, defined as Ramsey-good graphs in which the ad-
                                                 dition or removal of any edge necessarily creates an s-clique or a t-
                                                 independent set. We present a method combining SAT solving with be-
                                                 spoke LLM-generated code to discover infinite families of such graphs,
                                                 answering a question of Grinstead and Roberts from 1982. In addition,
                                                 we use LLMs to generate and formalize correctness proofs in Lean. This
                                                 case study highlights the potential of integrating automated reasoning,
                                                 large language models, and formal verification to accelerate mathemat-
                                                 ical discovery. We argue that such tool-driven workflows will play an
                                                 increasingly central role in experimental mathematics.

                                                 Keywords: Ramsey theory · experimental mathematics · artificial in-
                                                 telligence


                                           1   Introduction
                                           In 2000, the mathematician Timothy Gowers presciently predicted that “during
                                           the next century computers will become sufficiently good at proving theorems
                                           that the practice of pure mathematical research will be completely revolution-
                                           ized” [22]. He looked forward to a “golden age” of mathematics, where comput-
                                           ers can be helpful research assistants while still leaving room for humans to
                                           contribute deep insights. We believe that we are now entering this golden age,
                                           thanks to the combination of several technologies:
                                            – Mature and efficient symbolic reasoning: SAT solvers and computer
                                              algebra systems have evolved tremendously, and are currently able to reliably
                                              handle large computations.
                                            – LLMs capable of producing mathematical arguments: Frontier mod-
                                              els have demonstrated remarkable mathematical capabilities [48], ranging
                                              from competition problems [29] to research-level questions and open prob-
                                              lems [7, 18, 46].
                                            – Autoformalization: Relying on proof assistants like Lean [36], with large
                                              mathematical libraries [13], LLMs can now formalize proofs for mathematical
                                              arguments of increasing complexity [44, 45].
2       Przybocki et al.

In this paper, we give a glimpse of what this golden age looks like, and how these
different technologies coalesce for accelerating mathematical research. Specifi-
cally, we show how our investigations into a natural problem in Ramsey theory
were drastically assisted by the above technologies. Indeed, our theorems would
have been very difficult to discover without computer assistance, and essentially
all of the tedious work that inevitably arises in the course of research was fully
automated.


1.1   Problem and results

A graph is R(s, t)-good if it contains neither a clique of size s nor an independent
set of size t. Ramsey’s celebrated theorem states that for each s and t, there are
only finitely many R(s, t)-good graphs [39]. This theorem has been revisited and
generalized many times and gave birth to a vast area of combinatorics called
Ramsey theory [23]. In this paper, we revisit the topic once again. Let us say
that a graph G is doubly saturated R(s, t)-good if it is R(s, t)-good, but adding
or removing any edge from G yields a graph that is not R(s, t)-good, and neither
G nor G is the complete graph.1 In other words, doubly saturated R(s, t)-good
graphs are R(s, t)-good graphs that are edge-maximal and edge-minimal, ex-
cluding complete and empty graphs. What makes these graphs interesting is
that they “just barely” avoid s-cliques and t-independent sets, so their construc-
tion involves a delicate balancing act. More broadly, our goal in understand-
ing doubly saturated R(s, t)-good graphs is to understand better the space of
R(s, t)-good graphs; as Angeltveit and McKay stated [3]: “The improvements in
the upper bound for R(5, 5) are intimately connected to our understanding of
[the set of R(4, 5)-good graphs on n vertices] for n large”. One way of under-
standing the space of R(s, t)-good graphs is to consider the partial ordering in
which G1 ≺ G2 if G2 can be obtained from G1 by adding edges. As illustrated
in Figure 1, graphs can then be partitioned into weakly connected components
of this ordering; doubly saturated graphs are precisely those that make up their
entire connected component.
    According to Grinstead and Roberts [24], Albertson and Berman asked in
1980 whether there are any doubly saturated R(s, t)-good graphs other than
C5 .2 Grinstead and Roberts were able to find three others, all of which were
circulant graphs, and they asked whether there were any others. Unfortunately,
this natural problem has lain dormant since Grinstead and Roberts’ paper.
    With computer assistance, we prove that there are infinitely many circulant
doubly saturated graphs:

Theorem 1. For all t ≥ 4, there is a doubly saturated R(4, t)-good graph on
6t − 11 vertices.
1
  The final condition ensures that it is possible to add and remove edges, which rules
  out, e.g., considering a graph on 1 vertex as doubly saturated for all s and t.
2
  Grinstead and Roberts called these graphs bicritical, but we avoid this terminology,
  since it is also used with a different meaning [33].
                                          Doubly Saturated Ramsey Graphs           3

                             570                        24   20 12    6   6    1   1
          55
# edges   54
          53
          52
          51
          50


Fig. 1: Hasse diagram for all 640 R(4, 4)-good graphs on 15 vertices, including 2
doubly saturated graphs. The size of each component is given above it.



   In fact, on the basis of experimental evidence, we conjecture that there are
doubly saturated R(s, t)-good graphs for almost all choices of parameters:



Conjecture 1. Let s, t ≥ 3 with s ≤ t and (s, t) ∈
                                                 / {(3, 4), (3, 6)}. Then, there is
a doubly saturated R(s, t)-good graph.


In Section 4, we provide some evidence for this conjecture by verifying it for
small choices of s and t. Specifically, in Section 4.1, we verify the conjecture for
s = 3 and t ≤ 10, and we propose a construction of an infinite family of graphs
that we conjecture are doubly saturated R(3, t)-good. Then, in Section 4.2, we
use Paley graphs to show that there is a doubly saturated R(s, s)-good graph
for all s ∈ [3, 20].
    A simple computer search shows that there are no doubly saturated R(3, 4)-
or R(3, 6)-good graphs.3 However, obtaining experimental data for larger choices
of s and t requires efficient combinatorial optimization tooling. We use SAT
solvers for this purpose, which allows us to prove for instance that the smallest
doubly saturated R(3, 7)-good graph has 20 vertices, and the smallest doubly
saturated R(4, 5)-good graph has 19 vertices. This relies on a compact SAT
encoding with only O(n4 ) clauses for the double saturation constraint as well as
symmetry-breaking constraints; we present this encoding in Section 2. In tandem
with LLMs, we use these and similar computations to discover constructions of
infinite families of doubly saturated graphs, including the one used to prove
Theorem 1. This methodology is detailed in the next subsection.
    Conjecture 1 asks about the existence of doubly saturated R(s, t)-good graphs,
but we can also ask more fine-grained questions about the set of doubly satu-
rated R(s, t)-good graphs. One question that strikes us as particularly natural is
how small a doubly saturated R(s, t)-good graph can be. In Section 5, we present
an LLM-discovered proof that every doubly saturated R(s, t)-good graph has at
least 2s + 2t − 7 vertices.
4         Przybocki et al.

    1                                     3       Formulate                          5
         Formulate                                                                       Formalize proof
                                                  conjecture
        math problem                                                                 (via autoformalization system)
                                              (in tandem with LLMs)




                  2                                           4
                          Generate
                                                                  Prove conjecture
                         small-n data
                                                                      (using LLMs)
                       (e.g., via SAT solvers)



             Fig. 2: Computer-assisted mathematics research paradigm


1.2      Our computer-assisted methodology
In this paper, we describe not only our mathematical results but also the method-
ology by which we discovered them, since we believe that workflows like ours will
rapidly become the norm in experimental mathematics and will be a boon to
the field. Our computer-assisted research paradigm is illustrated in Figure 2.
Of course, these steps (except perhaps formalization) are part of the research
process of almost every math problem, although it is only thanks to recent ad-
vances in AI and formal methods that multiple stages of this pipeline can be
automated. Specifically, for step 2 of the process, we used SAT solvers to look
for doubly saturated Ramsey-good graphs; in some cases, SAT solvers are not
well suited to the problem, in which case we used bespoke LLM-generated code
as a substitute. For about a decade now, it has been recognized that SAT solvers
have tremendous potential for solving small cases of hard combinatorial prob-
lems [6, 26, 27, 32, 42]. However, a common criticism of such proofs is that they
do not scale to proving general results, partly because “mere computations” can-
not provide the conceptual understanding that would be required for a general
proof (see the discussion in [4]). But this criticism is unwarranted in general:
SAT solving (and computational experiments more generally) should be seen
as an initial stage of the discovery process, not the end goal. This motivates
step 3, where we studied the doubly saturated graphs found computationally,
searched for patterns, and conjectured a general construction. We conjectured
Theorem 1 in the course of a dialogue with ChatGPT. This dialogue felt like a
productive collaboration with a research partner, which was expedited by the
fact that ChatGPT can autonomously run computational experiments to quickly
assess hypotheses and analyze data. The role of the human in this dialogue was
to guide ChatGPT toward promising strategies.
    For step 4, we used LLMs to generate a proof of Theorem 1 with essen-
tially no human guidance. It is well known that LLMs have achieved remarkable
performance on benchmarks and math competitions, but they are also starting
to become useful for proving theorems arising in the course of actual research.
Unfortunately, LLMs are notorious for producing proofs with fiendishly subtle
3
    This can easily be checked using Brendan McKay’s enumeration of Ramsey-good
    graphs: https://users.cecs.anu.edu.au/~bdm/data/ramsey.html.
                                         Doubly Saturated Ramsey Graphs         5

errors. Thus, formalizing proofs in a proof assistant like Lean has become more
important than ever. The primary barrier to the mainstream adoption of proof
assistants has historically been their steep learning curve, together with the la-
borious nature of formalizing nontrivial mathematics. But here too, advances in
AI and formal methods have changed the game. In our case, using an informal
proof generated by Gemini, Harmonic’s autoformalization system called Aristo-
tle [1] was able to autonomously write over 1000 lines of Lean code to formally
verify Theorem 1.


1.3   Related work

Mathematical related work. Saturation problems in graph theory have been stud-
ied since Erdős, Hajnal, and Moon’s classic paper [17], which studied graphs for
which the addition of any edge creates a k-clique. Specifically, they determined
the minimum number of edges in an n-vertex graph avoiding k-cliques such that
the addition of any edge creates a k-clique. These graphs were further stud-
ied by Hajnal [25], and we use one of Hajnal’s theorems in Section 5. Similar
saturation problems have been studied with respect to subgraphs other than
cliques [14, 31] and with respect to induced subgraphs [34]. Damásdi et al. [15]
studied Ramsey-good graphs that are vertex-saturated, meaning that adding a
vertex and connecting it to any subset of the existing vertices always yields a
graph that is not Ramsey-good. The same paper also proved saturation results
for other problems in Ramsey theory. More broadly, our work falls under the
umbrella of studying objects that avoid some pattern but no longer do so after
a small perturbation. The first author studied a problem in this vein in combi-
natorics on words, constructing words avoiding certain types of repetitions such
that changing any letter creates such a repetition [38].


AI related work. As mentioned above, SAT solvers have become an essential
tool for computer-assisted mathematics, particularly for combinatorial prob-
lems [6,26,27,32,42]. Most applications of SAT to mathematics focus on solving
particular cases of open problems (step 2 from Figure 2), but some work has
gone further and used data generated from SAT experiments to discover gen-
eral theorems. For example, Subercaseaux et al. [43] applied SAT to pentagon
minimization in planar point sets and discovered a general construction, whose
correctness they were able to prove by hand. Aside from SAT, using LLMs to
assist with mathematical research has recently become a hot topic [8, 19, 46].
However, to the best of our knowledge, there are no case studies on the interplay
between SAT and LLMs in spurring mathematical discovery, which is a signif-
icant gap given the recognized potential of neuro-symbolic AI [28]. The closest
work to ours is by Xia et al. [47], which also uses a neuro-symbolic pipeline for
a combinatorial design problem, integrating LLMs and Lean autoformalization.
Their work does not include SAT solvers, instead using a custom Rust solver as
well as computer algebra systems.
6        Przybocki et al.

1.4     Preliminaries

All graphs in this paper are simple and finite. The complete graph on n vertices
is denoted Kn , and the empty graph on n vertices is denoted In . Given a graph
G, its clique number, denoted ω(G), is the largest n such that G contains Kn as
a subgraph; its independence number, denoted α(G), is the largest n such that
G contains In as an induced subgraph. The minimum (respectively, maximum)
degree of vertices in G is denoted δ(G) (respectively, ∆(G)).
    Given x ∈ Z/nZ, let ∥x∥ := min(x mod n, n − (x mod n)). Then, a circulant
graph on n vertices with distances S ⊆ [⌊n/2⌋] is the graph with vertex set Z/nZ
such that x and y are adjacent if and only if ∥x − y∥ ∈ S.


2     A SAT encoding of double saturation

In this section, we describe how to compactly encode the double saturation
condition as a CNF formula that can be fed to a SAT solver. Given s, t, and n,
we construct a CNF formula that is satisfiable if and only if there is a doubly
saturated R(s, t)-good graph on n vertices. Naturally, we have edge variables
e{i,j} for each {i, j} ∈ [n]
                             
                          2 , which indicate whether the graph contains the edge
{i, j}. To encode that the graph contains no s-clique, we use the following clauses:
                                                      
                               ^  _
                                                 e{i,j}  .
                                                        
                                      
                              S∈([n]
                                  s )
                                       {i,j}∈(S
                                              2)



The absence of t-independent sets is  encoded  similarly. Note that this direct
encoding of R(s, t)-goodness uses ns + nt clauses.4 To enforce that the
                                          
                                                                       W graph
is neither
     W     the complete graph nor the empty graph, we  add the clauses  i,j e{i,j}
and i,j e{i,j} .
    It remains to encode the double saturation condition, which amounts to en-
forcing:

      (Maximality) every non-edge {i, j} is part of a Ks \ {{i, j}}
      (Minimality) and every edge {i, j} is part of an It ∪ {{i, j}}.

A naive encoding of these constraints would use O(ns + nt ) clauses for a fixed
s and t. Perhaps surprisingly, we show that the double saturation condition
can be encoded using only O(n4 ) clauses. Let us describe the encoding for the
maximality property, since minimality is analogous. For each {i, j} ∈ [n]
                                                                                
                                                                              2   and
each k ∈ [n] \ {i, j}, we introduce an auxiliary variable p{i,j},k , which intuitively
represents that vertex k belongs to the Ks \ {{i, j}} certifying maximality in
4
    An encoding with asymptotically fewer clauses using fast matrix multiplication is
    possible but unlikely to be practical [16].
                                                       Doubly Saturated Ramsey Graphs                   7

case {i, j} is a non-edge. Our encoding includes the following clauses:
          ^           ^                                                               
                               e{i,j} ∨ p{i,j},k ∨ e{i,k} ∧ e{i,j} ∨ p{i,j},k ∨ e{j,k}
      {i,j}∈([n]
              2 )
                  k∈[n]\{i,j}
          ^              ^                                                     
    ∧                                 e{i,j} ∨ p{i,j},k ∨ p{i,j},k′ ∨ e{k,k′ }
      {i,j}∈([n]
              2 ) {k,k }∈(
                      ′   [n]\{i,j}
                              2     )
          ^
    ∧             AtLeasts−2 ({p{i,j},k | k ∈ [n] \ {i, j}}).
      {i,j}∈([n]
              2 )


These constraints enforce that for every non-edge {i, j}, there are at least s − 2
vertices that are all pairwise adjacent and adjacent to both i and j, which is to
say that {i, j} is part of a Ks \ {{i, j}}. An illustration is presented in Figure 3.
We encode AtLeasts−2 ({p{i,j},k | k ∈ [n] \ {i, j}}) with O(ns) clauses using
Sinz’s sequential counter encoding [41]; we use the implementation of cardinality
constraints provided by PySAT [30]. Therefore, the number of clauses is O(n4 ).


                                                                            k1
                                                                                          k2

                                                                   i
              i                  k1
                                                                                                   k3

                                                                  j
                                                                                          k4
              j                  k2                                         k5

                   (a) s = 4                                                 (b) s = 7

Fig. 3: Illustration of the encoding for maximality. If edge {i, j} is not present,
there must be vertices k1 , . . . , ks−2 such that adding edge {i, j} would introduce
a Ks .


   To make the SAT encoding performant, we also introduce lexicographic
symmetry-breaking constraints [12, Definition 8]. Namely, we enforce for each
i < j that

         (e{i,1} , . . . , e{i,i−1} , e{i,i+1} , . . . , e{i,j−1} , e{i,j+1} , . . . , e{i,n} ) ⪯lex
         (e{j,1} , . . . , e{j,i−1} , e{j,i+1} , . . . , e{j,j−1} , e{j,j+1} , . . . , e{j,n} ).

We encode the ⪯lex constraint between two sequences (a1 , . . . , an ), (b1 , . . . , bn )
of propositional variables via the following recursion. First, we add a clause
(a1 ∨ b1 ), then introduce an auxiliary variable y, and add 4 clauses to enforce
that y ↔ (a1 ↔ b1 ). Finally, we recursively encode (a2 , . . . , an ) ⪯lex (b2 , . . . , bn )
into a formula λn−1 , and add clauses (y ∨ C) for every C ∈ λn−1 .
8      Przybocki et al.

3   Doubly saturated R(4, t)-good graphs
Since there is a complete enumeration of R(4, 4)-good graphs, it is a simple
computation to check that there are six doubly saturated R(4, 4)-good graphs:
one on 13 vertices, two on 15 vertices, two on 16 vertices, and one on 17 vertices.
The doubly saturated R(4, 4)-good graph on 13 vertices is the Paley graph of
order 13, which is the circulant graph with distances {1, 3, 4}.
    Following these observations, we turned to looking for doubly saturated
R(4, 5)-good graphs. There are far too many R(4, 5)-good graphs for a complete
enumeration (the estimate of Angeltveit and McKay is about 2.93 · 1019 [3, Ap-
pendix A]), so we applied SAT to the problem using the encoding from Section 2.
We found that there are no doubly saturated R(4, 5)-good graphs on 18 or fewer
vertices. On the other hand, for 19 vertices, a SAT solver (CaDiCaL [5]) does
not terminate after a day on a single core. Thus, we made an ansatz that a so-
lution would be circulant, as suggested by some of the R(4, 4) results. We found
that there is a circulant doubly saturated R(4, 5)-good graph on 19 vertices with
distances {4, 5, 6, 8}. Later, we applied Mallob [40] to our SAT encoding, and it
found a solution isomorphic to this circulant graph, which suggests that it may
be the unique doubly saturated R(4, 5)-good graph on 19 vertices.
    At this point, we asked ChatGPT-5.1 Pro to look for circulant doubly satu-
rated R(4, t)-good graphs for t ∈ [6, 12]. For large values of t, the SAT encoding
becomes unwieldy because there are too many clauses required to enforce the ab-
sence of t-independent sets, but bespoke code generated by the LLM succeeded
in finding circulant constructions for each t ∈ [6, 12].
    Having found nine constructions, we asked ChatGPT to extrapolate from
these to find a general construction that works for all t ≥ 4. ChatGPT quickly
recognized that every construction so far had n := 6t−11 vertices, so it remained
to find the patterns in the distance sets. ChatGPT tried several approaches,
which varied in how promising they seemed to us. For example, analyzing the
spectral properties of the graphs did not seem to us to be as fruitful as studying
the additive-combinatorial properties of the distance sets. Accordingly, we en-
couraged ChatGPT to look deeper into the more promising strategies. Besides
this minimal shepherding, the discovery process was almost entirely LLM-driven.
ChatGPT realized that when specifying a circulant graph, there are many dis-
tance sets that result in isomorphic graphs. Motivated by this observation, Chat-
GPT tried rewriting each of the nine distance sets into a canonical form from
which patterns would become clearer. After a few iterations of this, it discovered
the following construction for the distance sets, which agreed with all nine of
our constructions up to isomorphism: {1} ∪ {m ∈ [⌊n/2⌋] | m ≡ 3, 4 (mod 6)}.
At the time, ChatGPT was unable to prove that the construction works.
    With the release of ChatGPT-5.4 Pro, we revisited the problem. This time,
ChatGPT not only managed to produce a proof but also showed that the con-
jectured construction has a simpler isomorphic description. Specifically, letting
m = t − 2 and n = 6t − 11, the above construction is isomorphic to the circu-
lant graph on n vertices with distances {m} ∪ [2m + 1, 3m]. See Figure 4 for a
depiction of the construction for t = 4 and t = 5.
                                               Doubly Saturated Ramsey Graphs                9

    We next set our sights on obtaining a formal proof that the construction
works. We believe that this is important when using LLMs to prove theorems,
because LLM-generated proofs are notorious for containing subtle errors, and
formalization eliminates any worries about correctness. Moreover, autoformal-
ization avoids wasting mathematicians’ time on checking flawed LLM-generated
proofs, and can be further used to refine proof attempts on a loop based on errors
that the formalization process reveals. To autoformalize a proof, it is important
to start with an informal proof that is sufficiently detailed. We prompted Gemini
3 Deep Think5 to “write a proof that is very detailed and formal so that it can
readily be formalized in Lean.” We fed this proof into Aristotle, which generated
a complete formal proof in Lean after two attempts.6
    Below, we present an informal proof that the construction works. The proof
has been human-edited for clarity and concision, particularly because the LLM-
generated proof had some needless case distinctions. Since the formal proof con-
tains all of the details, we write the informal proof somewhat tersely.

Theorem 1. For all t ≥ 4, there is a doubly saturated R(4, t)-good graph on
6t − 11 vertices.

Proof. Let m = t − 2, meaning the number of vertices is n = 6m + 1 = 6t − 11.
Let G be the circulant graph on n vertices with distances {m} ∪ [2m + 1, 3m].
Thus, u and v are adjacent if and only if u − v ∈ {m, 5m + 1} ∪ [2m + 1, 4m].
    To show G is doubly saturated R(4, t)-good, we must establish four proper-
ties: ω(G) < 4, α(G) < t, adding any edge creates a K4 , and removing any edge
creates an It .
    Part 1: ω(G) < 4. Assume for contradiction that a clique of 4 vertices exists.
The forward cyclic differences (gaps) g1 , g2 , g3 , g4 between adjacent vertices must
satisfy g1 + g2 + g3 + g4 = n = 6m + 1. At least three gaps must equal m,
otherwise g1 + g2 + g3 + g4 ≥ 2m + 2 · (2m + 1) > 6m + 1 = n. Thus, there
is some i ∈ [4] for which we have gi = gi+1 = m (where g5 = g1 ). But then,
gi + gi+1 = 2m ∈   / {m, 5m + 1} ∪ [2m + 1, 4m], a contradiction.
    Part 2: α(G) < t. Assume for contradiction that an independent set of
t = m + 2 vertices exists. Let the vertices be v1 , . . . , vt . Then, ∥vi − vj ∥ ∈
[0, m − 1] ∪ [m + 1, 2m] for all i, j ∈ [t]. Since ∥vi − vj ∥ ≤ 2m < n/3, we can
cyclically shift the vertices so that v1 = 0 and vi ∈ [1, m − 1] ∪ [m + 1, 2m] for all
i ∈ [2, t]. But since {v2 , . . . , vt } is a subset of [1, m − 1] ∪ [m + 1, 2m] of size m + 1,
there must be some pair vi and vj such that ∥vi − vj ∥ = m, a contradiction.
    Part 3: Adding any edge creates a K4 . Suppose we add an edge (0, d)
where d ∈ [1, m − 1] ∪ [m + 1, 2m]. First, if d ∈ [1, m − 1], then {0, d, 2m + d +
1, 3m + d + 1} is a K4 . Second, if d ∈ [m + 1, 2m], then {0, d, m + d, 5m + 1} is
a K4 .
    Part 4: Removing any edge creates an It . Suppose we remove an edge
(0, d) where d ∈ S. First, if d = m, then [−1, m − 2] ∪ {m, 2m − 1} is an It .
5
  Switching to Gemini from ChatGPT was simply because each of us prefers a different
  LLM, not because we had any reason to expect Gemini to be better at this task.
6
  The formalization is available at https://github.com/bprzybocki/doubly-saturated.
10      Przybocki et al.

Second, if d ∈ [2m + 1, 3m − 1], then {0, 2m, d} ∪ ([d − 2m, d − m − 1] \ {m}) is
an It . Third, if d = 3m, then [−2m, −m − 1] ∪ {0, 3m} is an It .




Fig. 4: Illustration of the construction for t = 4 and t = 5 (13 and 19 vertices
respectively). Dashed red edges are not part of the construction, and adding them
introduces the K4 subgraph given by the green vertices and already present thick
edges.


    An interesting lingering question is whether the construction in Theorem 1
is as small as possible. Our SAT experiments demonstrate this for t ≤ 5.

Question 1. For each t ≥ 4, is the smallest doubly saturated R(4, t)-good graph
of size 6t − 11?

   We remark that the largest R(4, t)-good graphs are known to be of size
 e 3 ) [2, 35], so the doubly saturated R(4, t)-good graphs constructed in Theo-
Θ(t
rem 1 are much smaller than the largest R(4, t)-good graphs.


4     Other families of doubly saturated Ramsey graphs
4.1   Doubly saturated R(3, t)-good graphs
We have some experimental results regarding doubly saturated R(3, t)-good
graphs, including a conjectural infinite family. First, we present experimental
observations for small values of t:
 – There is a unique doubly saturated R(3, 3)-good graph, namely C5 .
 – There are no doubly saturated R(3, 4)-good graphs.
 – There is a unique doubly saturated R(3, 5)-good graph, namely the circulant
   graph on 13 vertices with distances {1, 5}.
                                       Doubly Saturated Ramsey Graphs        11

 – There are no doubly saturated R(3, 6)-good graphs.
 – Using our SAT encoding, we found that there is a doubly saturated R(3, 7)-
   good graph on 20 vertices, and there are none with fewer than 20 vertices. We
   found 18 satisfying assignments that were all isomorphic, which suggests that
   the solution may be unique. Interestingly, the graph is 5-regular and vertex-
   transitive, although it is not circulant. We asked ChatGPT whether it was
   possible to decompose the graph into various patterned substructures, and
   with its help, we eventually discovered that it can be partitioned into four
   disjoint 5-cycles with a matching between each pair of cycles (see Figure 5).
   This pattern might form the basis of a general construction.
 – Using our SAT encoding, we have found two non-isomorphic doubly satu-
   rated R(3, 8)-good graphs on 25 vertices. There may be more than two such
   graphs, and we do not know if they are minimal, although we do know that
   there are none on 21 or fewer vertices.
 – There is a unique R(3, 9)-good graph on 35 vertices [21], and it is therefore
   doubly saturated. It is also a circulant graph.
 – We have found over 100 doubly saturated R(3, 10)-good graphs on 39 vertices
   by searching through the known R(3, 10)-good graphs on 39 vertices.




         Fig. 5: A doubly saturated R(3, 7)-good graph on 20 vertices


   Using a similar workflow as described in Section 3, we collaborated with
ChatGPT-5.1 Pro to find circulant constructions for doubly saturated R(3, t)-
good graphs. After much experimentation, we conjecture the following:
12                   Przybocki et al.

Conjecture 2. For every odd t ≥ 17, the following graph is doubly saturated
R(3, t)-good: the circulant graph on 5t − 10 vertices with distances [t − 4, t − 3] ∪
[t + 1, (3t − 9)/2] ∪ {(3t − 5)/2} ∪ {2t − 4}.
We have not yet managed to prove this conjecture, although we have checked
it for t ≤ 63. We expect that in the near future, it will be feasible for LLMs to
both prove Conjecture 2 and formally verify it as was done for Theorem 1.

4.2                Doubly saturated R(s, s)-good graphs
The question of whether there is a doubly saturated R(s, s)-good graph is per-
haps the most interesting case of Conjecture 1. We have verified this claim for
s ≤ 20 using Paley graphs of prime order. Since Paley graphs are symmetric and
self-complementary, to check whether a Paley graph is doubly saturated, we only
need to add an arbitrary edge and check if the clique number increases. We use
Cliquer [37] to compute clique numbers of these graphs. Table 1 shows, for each
s ∈ [3, 20], the smallest prime p such that the Paley graph of order p is doubly
saturated R(s, s)-good.



Table 1: The smallest prime p such that the Paley graph on p vertices is a doubly
saturated R(s, s)-good graph
     s             3 4 5 6 7      8     9   10 11 12 13       14   15    16   17      18   19     20
     p             5 13 29 53 97 137 173 317 577 541 613 1301 1373 1481 2389 3001 4861 3169



   As depicted in Figure 6, our experimental results show that approximately
75% of prime-order Paley graphs are doubly saturated. On the basis of these
results, we strongly expect that there is a doubly saturated R(s, s)-good Paley
graph for each s ≥ 3, although this seems difficult to prove.
 Cum. proportion




                      1



                   0.75

                    0.6
                                  50         100        150        200          250         300
                                            nth prime congruent to 1 modulo 4

Fig. 6: Cumulative proportion of prime-order Paley graphs that are doubly sat-
urated
                                         Doubly Saturated Ramsey Graphs        13

5   A lower bound for the double saturation number

We define the double saturation number of s and t as follows:

DS(s, t) := inf{n | there is a doubly saturated R(s, t)-good graph on n vertices}.

Question 1 asks whether DS(4, t) = 6t − 11 for all t ≥ 4. More generally, it
is natural to ask for bounds on DS(s, t). We asked Gemini 3.1 Deep Think to
prove a lower bound on DS(s, t), and it proved that DS(s, t) ≥ 2s + 2t − 7
with an elegant argument. To present the argument, we need a theorem due to
Hajnal [25]. We say that a graph G is k-saturated if it does not contain a Kk+1
subgraph, but adding any edge to G yields a graph containing a Kk+1 . Hajnal
proved the following:

Theorem 2 ([25, Theorem 1]). If G is k-saturated, then either G has a
vertex adjacent to every other vertex or δ(G) ≥ 2(k − 1).

Now, we can prove our lower bound on DS(s, t):

Theorem 3. For all s, t ≥ 3, we have DS(s, t) ≥ 2s + 2t − 7.

Proof. Suppose that G is a doubly saturated R(s, t)-good graph. First, we claim
that G does not have a vertex adjacent to every other vertex. Indeed, suppose for
the sake of contradiction that v ∈ V (G) is adjacent to every vertex in V (G)\{v}.
Let w ∈ V (G) \ {v} be an arbitrary vertex, and let G′ be the graph obtained
from G by removing the edge {v, w}. Then, G′ contains an It involving v. Since
v is adjacent to every other vertex except w in G′ , the largest independent set
involving v is {v, w}, which contradicts our assumption that t ≥ 3. Thus, G
does not have a vertex adjacent to every other vertex. By symmetry, the same
property holds for G.
    Now, by Theorem 2, we have δ(G) ≥ 2(s − 2) and δ(G) ≥ 2(t − 2). Thus,
∆(G) = n − 1 − δ(G) ≤ n − 1 − 2(t − 2) = n − 2t + 3. Since δ(G) ≤ ∆(G), we
have 2(s − 2) ≤ n − 2t + 3, so n ≥ 2s + 2t − 7.


6   Conclusion

We used SAT solvers and LLMs to study doubly saturated Ramsey-good graphs.
Our work suggests several further directions related to these graphs:

 – Conjecture 1 is the main open problem raised by our work. Finding new
   infinite families of doubly saturated Ramsey-good graphs would constitute
   partial progress toward proving this conjecture and has the potential to
   uncover intriguing families of graphs. Indeed, there is reason to expect such
   graphs to have nice combinatorial or algebraic properties, as illustrated by
   the infinite families from Theorem 1 and Conjecture 2, the graph depicted
   in Figure 5, and the Paley graphs discussed in Section 4.2.
14      Przybocki et al.

 – Another further direction is to better understand the behavior DS(s, t). In
   Question 1, we asked whether DS(4, t) = 6t − 11. We are also interested
   in whether, for each fixed s ≥ 3, the growth of DS(s, t) is linear; that is, is
   DS(s, t) = Os (t)? Theorem 1 and Conjecture 2 provide some limited evidence
   in favor of this hypothesis. It would also be interesting to understand the
   asymptotics of DS(s, s). As a concrete question, is DS(s, s) = sO(1) ?
 – Given arbitrary graphs H1 and H2 , one can consider graphs G such that
   (i) G does not contain H1 as a subgraph, (ii) G does not contain H2 as a
   subgraph, (iii) adding any edge to G yields a graph that contains H1 as a
   subgraph, and (iv) adding any edge to G yields a graph that contains H2
   as a subgraph. Taking H1 = Ks and H2 = Kt yields the doubly saturated
   R(s, t)-good graphs that we have been studying, although other choices of
   graphs may be equally interesting. The study of graphs satisfying conditions
   (i) and (ii) is a central topic in Ramsey theory [9–11, 20].
   More generally, our work creates an impetus to find other types of mathe-
matical problems to which our computer-assisted methodology can be fruitfully
applied. The features that made this problem amenable to computer-assistance
were the following:
 – Data for small cases are very helpful for understanding the problem while
   being hard to compute by hand, which makes SAT solvers and other com-
   putational experiments useful.
 – There is a vast array of techniques that might be applicable to the problem,
   which makes leveraging the encyclopedic knowledge of LLMs powerful.
 – Proofs are likely to involve relatively elementary combinatorial arguments,
   which allows them to be discovered and formalized by LLMs.
With the mathematical abilities of LLMs rapidly advancing, we expect that the
last feature will become increasingly unnecessary.

Acknowledgments. This research is supported by the DARPA expMath program
through the DARPA CMO contract number HR0011262E028. Przybocki was addi-
tionally supported by the NSF Graduate Research Fellowship Program under Grant
No. DGE-2140739.

Disclosure of Interests. The authors have no competing interests to declare that
are relevant to the content of this article.


References
 1. Achim, T., Best, A., Bietti, A., Der, K., Fédérico, M., Gukov, S., Halpern-Leistner,
    D., Henningsgard, K., Kudryashov, Y., Meiburg, A., Michelsen, M., Patterson,
    R., Rodriguez, E., Scharff, L., Shanker, V., Sicca, V., Sowrirajan, H., Swope, A.,
    Tamas, M., Tenev, V., Thomm, J., Williams, H., Wu, L.: Aristotle: IMO-level
    automated theorem proving (2025), https://arxiv.org/abs/2510.01346
 2. Ajtai, M., Komlós, J., Szemerédi, E.: A note on Ramsey numbers. J. Combin. The-
    ory Ser. A 29(3), 354–360 (1980). https://doi.org/10.1016/0097-3165(80)90030-8
                                             Doubly Saturated Ramsey Graphs             15

 3. Angeltveit, V., McKay, B.D.: R(5, 5) ≤ 46. J. Graph Theory (2026). https://doi.
    org/10.1002/jgt.70029
 4. Avigad, J.: Varieties of mathematical understanding. Bull. Amer. Math. Soc. (N.S.)
    59(1), 99–117 (2022). https://doi.org/10.1090/bull/1726
 5. Biere, A., Faller, T., Fazekas, K., Fleury, M., Froleyks, N., Pollitt, F.: CaDiCaL 2.0.
    In: Gurfinkel, A., Ganesh, V. (eds.) Computer Aided Verification - 36th Interna-
    tional Conference, CAV 2024, Montreal, QC, Canada, July 24-27, 2024, Proceed-
    ings, Part I. Lecture Notes in Computer Science, vol. 14681, pp. 133–152. Springer
    (2024). https://doi.org/10.1007/978-3-031-65627-9_7
 6. Brakensiek, J., Heule, M., Mackey, J., Narváez, D.E.: The resolution of Keller’s
    conjecture. J. Autom. Reason. 66(3), 277–300 (2022), https://doi.org/10.1007/
    s10817-022-09623-5
 7. Brenner, M.P., Cohen-Addad, V., Woodruff, D.: Solving an open problem in the-
    oretical physics using AI-assisted discovery (2026), https://arxiv.org/abs/2603.
    04735
 8. Bubeck, S., Coester, C., Eldan, R., Gowers, T., Lee, Y.T., Lupsasca, A., Sawh-
    ney, M., Scherrer, R., Sellke, M., Spears, B.K., Unutmaz, D., Weil, K., Yin,
    S., Zhivotovskiy, N.: Early science acceleration experiments with GPT-5 (2025),
    https://arxiv.org/abs/2511.16072
 9. Chvátal, V., Harary, F.: Generalized Ramsey theory for graphs. I. Diagonal
    numbers. Period. Math. Hungar. 3, 115–124 (1973). https://doi.org/10.1007/
    BF02018466, collection of articles dedicated to the memory of Alfred Renyi, II
10. Chvátal, V., Harary, F.: Generalized Ramsey theory for graphs. II. Small diagonal
    numbers. Proc. Amer. Math. Soc. 32, 389–394 (1972). https://doi.org/10.2307/
    2037824
11. Chvátal, V., Harary, F.: Generalized Ramsey theory for graphs. III. Small off-
    diagonal numbers. Pacific J. Math. 41, 335–345 (1972), http://projecteuclid.org/
    euclid.pjm/1102968279
12. Codish, M., Miller, A., Prosser, P., Stuckey, P.J.: Constraints for symmetry break-
    ing in graph representation. Constraints 24(1), 1–24 (Jan 2019). https://doi.org/
    10.1007/s10601-018-9294-5
13. mathlib Community, T.: The Lean Mathematical Library. In: Proceedings of the
    9th ACM SIGPLAN International Conference on Certified Programs and Proofs.
    CPP ’20, ACM (January 2020). https://doi.org/10.1145/3372885.3373824
14. Currie, B.L., Faudree, J.R., Faudree, R.J., Schmitt, J.R.: A survey of mini-
    mum saturated graphs. The Electronic Journal of Combinatorics Dynamic Sur-
    veys, #DS19: Oct 11, 2021 (Jul 2011). https://doi.org/10.37236/41, https://www.
    combinatorics.org/ojs/index.php/eljc/article/view/DS19
15. Damásdi, G., Keszegh, B., Malec, D., Tompkins, C., Wang, Z., Zamora, O.: Satu-
    ration problems in the Ramsey theory of graphs, posets and point sets. European
    J. Combin. 95, Paper No. 103321, 21 (2021). https://doi.org/10.1016/j.ejc.2021.
    103321
16. Eisenbrand, F., Grandoni, F.: On the complexity of fixed parameter clique and
    dominating set. Theor. Comput. Sci. 326(1-3), 57–67 (2004). https://doi.org/10.
    1016/J.TCS.2004.05.009
17. Erdős, P., Hajnal, A., Moon, J.W.: A problem in graph theory. Amer. Math.
    Monthly 71, 1107–1110 (1964). https://doi.org/10.2307/2311408
18. Feng, T., Trinh, T., Bingham, G., Kang, J., Zhang, S., hyun Kim, S., Barreto, K.,
    Schildkraut, C., Jung, J., Seo, J., Pagano, C., Chervonyi, Y., Hwang, D., Hou, K.,
    Gukov, S., Tsai, C.C., Choi, H., Jin, Y., Li, W.Y., Wu, H.A., Shiu, R.A., Shih,
16      Przybocki et al.

    Y.S., Le, Q.V., Luong, T.: Semi-autonomous mathematics discovery with Gemini:
    A case study on the Erdős problems (2026), https://arxiv.org/abs/2601.22401
19. Feng, T., Trinh, T.H., Bingham, G., Hwang, D., Chervonyi, Y., Jung, J., Lee, J.,
    Pagano, C., hyun Kim, S., Pasqualotto, F., Gukov, S., Lee, J.N., Kim, J., Hou,
    K., Ghiasi, G., Tay, Y., Li, Y., Kuang, C., Liu, Y., Lin, H., Liu, E.Z., Nayakanti,
    N., Yang, X., Cheng, H.T., Hassabis, D., Kavukcuoglu, K., Le, Q.V., Luong, T.:
    Towards autonomous mathematics research (2026), https://arxiv.org/abs/2602.
    10177
20. Gerencsér, L., Gyárfás, A.: On Ramsey-type problems. Ann. Univ. Sci. Budapest.
    Eötvös Sect. Math. 10, 167–170 (1967)
21. Goedgebeur, J., Radziszowski, S.P.: New computational upper bounds for Ramsey
    numbers R(3, k). Electron. J. Combin. 20(1), Paper 30, 22 (2013). https://doi.org/
    10.37236/2824
22. Gowers, W.T.: Rough structure and classification. pp. 79–117 (2000). https://doi.
    org/10.1007/978-3-0346-0422-2_4, GAFA 2000 (Tel Aviv, 1999)
23. Graham, R.L., Rothschild, B.L., Spencer, J.H.: Ramsey theory. Wiley-Interscience
    Series in Discrete Mathematics and Optimization, John Wiley & Sons, Inc., New
    York, second edn. (1990), a Wiley-Interscience Publication
24. Grinstead, C.M., Roberts, S.M.: On the Ramsey numbers R(3, 8) and R(3, 9).
    J. Combin. Theory Ser. B 33(1), 27–51 (1982). https://doi.org/10.1016/
    0095-8956(82)90055-7
25. Hajnal, A.: A theorem on k-saturated graphs. Canadian J. Math. 17, 720–724
    (1965). https://doi.org/10.4153/CJM-1965-072-1
26. Heule, M.J.H.: Schur number five. In: McIlraith, S.A., Weinberger, K.Q. (eds.) Pro-
    ceedings of the Thirty-Second AAAI Conference on Artificial Intelligence, (AAAI-
    18), the 30th innovative Applications of Artificial Intelligence (IAAI-18), and the
    8th AAAI Symposium on Educational Advances in Artificial Intelligence (EAAI-
    18), New Orleans, Louisiana, USA, February 2-7, 2018. pp. 6598–6606. AAAI Press
    (2018), https://doi.org/10.1609/aaai.v32i1.12209
27. Heule, M.J.H., Kullmann, O., Marek, V.W.: Solving and verifying the Boolean
    Pythagorean triples problem via cube-and-conquer. In: Creignou, N., Berre, D.L.
    (eds.) Theory and Applications of Satisfiability Testing - SAT 2016 - 19th Interna-
    tional Conference, Bordeaux, France, July 5-8, 2016, Proceedings. Lecture Notes
    in Computer Science, vol. 9710, pp. 228–245. Springer (2016), https://doi.org/10.
    1007/978-3-319-40970-2_15
28. Hitzler, P., Eberhart, A., Ebrahimi, M., Sarker, M.K., Zhou, L.: Neuro-symbolic
    approaches in artificial intelligence. National Science Review 9(6), nwac035 (03
    2022). https://doi.org/10.1093/nsr/nwac035
29. Hubert, T., Mehta, R., Sartran, L., Horváth, M.Z., Žužić, G., Wieser, E., Huang,
    A., Schrittwieser, J., Schroecker, Y., Masoom, H., Bertolli, O., Zahavy, T., Mand-
    hane, A., Yung, J., Beloshapka, I., Ibarz, B., Veeriah, V., Yu, L., Nash, O., Lezeau,
    P., Mercuri, S., Sönne, C., Mehta, B., Davies, A., Zheng, D., Pedregosa, F., Li,
    Y., von Glehn, I., Rowland, M., Albanie, S., Velingker, A., Schmitt, S., Lockhart,
    E., Hughes, E., Michalewski, H., Sonnerat, N., Hassabis, D., Kohli, P., Silver, D.:
    Olympiad-level formal mathematical reasoning with reinforcement learning. Nature
    651(8106), 607–613 (Mar 2026). https://doi.org/10.1038/s41586-025-09833-y
30. Ignatiev, A., Morgado, A., Marques-Silva, J.: PySAT: A Python toolkit for pro-
    totyping with SAT oracles. In: SAT. pp. 428–437 (2018). https://doi.org/10.1007/
    978-3-319-94144-8_26, https://doi.org/10.1007/978-3-319-94144-8_26
31. Kászonyi, L., Tuza, Z.: Saturated graphs with minimal number of edges. J. Graph
    Theory 10(2), 203–210 (1986). https://doi.org/10.1002/jgt.3190100209
                                           Doubly Saturated Ramsey Graphs           17

32. Konev, B., Lisitsa, A.: A SAT attack on the Erdős discrepancy conjecture. In:
    Sinz, C., Egly, U. (eds.) Theory and Applications of Satisfiability Testing - SAT
    2014 - 17th International Conference, Held as Part of the Vienna Summer of Logic,
    VSL 2014, Vienna, Austria, July 14-17, 2014. Proceedings. Lecture Notes in Com-
    puter Science, vol. 8561, pp. 219–226. Springer (2014), https://doi.org/10.1007/
    978-3-319-09284-3_17
33. Lovász, L., Plummer, M.D.: On a family of planar bicritical graphs. Proc. London
    Math. Soc. (3) 30, 160–176 (1975). https://doi.org/10.1112/plms/s3-30.2.160
34. Martin, R.R., Smith, J.J.: Induced saturation number. Discrete Math. 312(21),
    3096–3106 (2012). https://doi.org/10.1016/j.disc.2012.06.015
35. Mattheus, S., Verstraete, J.: The asymptotics of r(4, t). Ann. of Math. (2) 199(2),
    919–941 (2024). https://doi.org/10.4007/annals.2024.199.2.8
36. de Moura, L., Ullrich, S.: The Lean 4 theorem prover and programming lan-
    guage. In: Automated Deduction – CADE 28: 28th International Conference
    on Automated Deduction, Virtual Event, July 12–15, 2021, Proceedings. p.
    625–635. Springer-Verlag, Berlin, Heidelberg (2021). https://doi.org/10.1007/
    978-3-030-79876-5_37
37. Niskanen, S., Östergård, P.R.J.: Cliquer user’s guide, version 1.0. Tech. Rep. T48,
    Communications Laboratory, Helsinki University of Technology, Espoo, Finland
    (2003)
38. Przybocki, B.: Lengths of irreducible and delicate words. Electron. J. Combin.
    29(3), Paper No. 3.7, 12 (2022). https://doi.org/10.37236/10669
39. Ramsey, F.P.: On a problem of formal logic. Proc. London Math. Soc. (2) 30(4),
    264–286 (1929). https://doi.org/10.1112/plms/s2-30.1.264
40. Schreiber, D., Sanders, P.: MallobSat: Scalable SAT solving by clause sharing.
    Journal of Artificial Intelligence Research (JAIR) 80, 1437–1495 (2024). https:
    //doi.org/10.1613/jair.1.15827
41. Sinz, C.: Towards an optimal CNF encoding of boolean cardinality constraints.
    In: van Beek, P. (ed.) Principles and Practice of Constraint Programming - CP.
    Lecture Notes in Computer Science, vol. 3709, pp. 827–831. Springer (2005). https:
    //doi.org/10.1007/11564751_73
42. Subercaseaux, B., Heule, M.J.H.: The packing chromatic number of the infinite
    square grid is 15. In: Sankaranarayanan, S., Sharygina, N. (eds.) Tools and Algo-
    rithms for the Construction and Analysis of Systems - 29th International Confer-
    ence, TACAS 2023, Held as Part of the European Joint Conferences on Theory
    and Practice of Software, ETAPS 2022, Paris, France, April 22-27, 2023, Proceed-
    ings, Part I. Lecture Notes in Computer Science, vol. 13993, pp. 389–406. Springer
    (2023), https://doi.org/10.1007/978-3-031-30823-9_20
43. Subercaseaux, B., Mackey, J., Heule, M.J.H., Martins, R.: Automated mathemat-
    ical discovery and verification: Minimizing pentagons in the plane. In: Kohlhase,
    A., Kovács, L. (eds.) Intelligent Computer Mathematics - 17th International Con-
    ference, CICM 2024, Montréal, QC, Canada, August 5-9, 2024, Proceedings. pp.
    21–41. Lecture Notes in Computer Science, Springer (2024). https://doi.org/10.
    1007/978-3-031-66997-2_2
44. Urban, J.: 130k lines of formal topology in two weeks: Simple and cheap autofor-
    malization for everyone? (2026), https://arxiv.org/abs/2601.03298
45. Weng, K., Du, L., Li, S., Lu, W., Sun, H., Liu, H., Zhang, T.: Autoformalization
    in the era of large language models: A survey (2025), https://arxiv.org/abs/2505.
    23486
18      Przybocki et al.

46. Woodruff, D.P., Cohen-Addad, V., Jain, L., Mao, J., Zuo, S., Bateni, M., Branzei,
    S., Brenner, M.P., Chen, L., Feng, Y., Fortnow, L., Fu, G., Guan, Z., Hadizadeh,
    Z., Hajiaghayi, M.T., JafariRaviz, M., Javanmard, A., C. S., K., Kawarabayashi,
    K., Kumar, R., Lattanzi, S., Lee, E., Li, Y., Panageas, I., Paparas, D., Przy-
    bocki, B., Subercaseaux, B., Svensson, O., Taherijam, S., Wu, X., Yogev, E.,
    Zadimoghaddam, M., Zhou, S., Matias, Y., Manyika, J., Mirrokni, V.: Acceler-
    ating scientific research with Gemini: Case studies and common techniques (2026),
    https://arxiv.org/abs/2602.03837
47. Xia, H., Gomes, C.P., Selman, B., Szeider, S.: Agentic neurosymbolic collaboration
    for mathematical discovery: A case study in combinatorial design (2026), https:
    //arxiv.org/abs/2603.08322
48. Yan, Y., Su, J., He, J., Fu, F., Zheng, X., Lyu, Y., Wang, K., Wang, S., Wen, Q.,
    Hu, X.: A survey of mathematical reasoning in the era of multimodal large language
    model: Benchmark, method & challenges. In: Che, W., Nabende, J., Shutova, E.,
    Pilehvar, M.T. (eds.) Findings of the Association for Computational Linguistics,
    ACL 2025, Vienna, Austria, July 27 - August 1, 2025. pp. 11798–11827. Findings
    of ACL, Association for Computational Linguistics (2025), https://aclanthology.
    org/2025.findings-acl.614/
