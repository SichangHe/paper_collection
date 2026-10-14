                                                        Agentic Neurosymbolic Collaboration for
                                                                Mathematical Discovery:
                                                         A Case Study in Combinatorial Design
                                                 Hai Xia∗         Carla P. Gomes†             Bart Selman†         Stefan Szeider∗


                                                                                       Abstract
                                                    We study mathematical discovery through the lens of neurosymbolic reasoning,
                                                where an AI agent powered by a large language model (LLM), coupled with symbolic
                                                computation tools, and human strategic direction, jointly produced a new result in
                                                combinatorial design theory. The main result of our human-AI collaboration is a tight
arXiv:2603.08322v2 [cs.AI] 13 Aug 2026




                                                lower bound on the imbalance of Latin squares for the difficult case n ≡ 1 (mod 3).
                                                Analyzing the logs of multiple sessions and multiple days, we can identify the contri-
                                                butions of different components in the framework. On one hand, the AI agent can
                                                uncover hidden structures and generate hypotheses. On the other hand, the symbolic
                                                components, including computer algebra, constraint solvers, and simulated annealing
                                                algorithms, can provide rigorous verification and exhaustive enumeration. Importantly,
                                                the human can make the important decision, shifting the dead-end research question to
                                                another promising one. Our analysis reveals that multi-model reviews among frontier
                                                LLMs proved reliable for criticism and error detection but unreliable for constructive
                                                claims. In the end, the resulting human-AI mathematical contribution, a tight lower
                                                bound of 4n(n−1)/9, is achieved via a new class of near-perfect permutations. The
                                                bound was also formally verified in Lean, showing that our neurosymbolic systems can
                                                indeed produce genuine discoveries in pure mathematics.


                                         1      Introduction
                                         There is increasing attention to mathematical discoveries with the help of neurosymbolic
                                         frameworks [d’Avila Garcez and Lamb, 2023], from program search with large language
                                         models finding new extremal constructions [Romera-Paredes et al., 2024], AI-guided conjec-
                                         tures in knot theory and representation theory [Davies et al., 2021], and automated geometry
                                         proving [Trinh et al., 2024]. All these kinds of frameworks use similar paradigms, using the
                                         neural side for generating conjectures or candidates and using symbolic tools for verifica-
                                         tion and refinement. The neurosymbolic general idea is quite promising for mathematical
                                         discovery, as LLMs can have creative intuitions regarding proofs and conjectures, and the
                                         symbolic tools can do effective and rigorous verification and computation. However, in each
                                         of these cases the objective is fixed from the outset: proving a stated conjecture, optimizing
                                         a known quantity, or search within a predefined space. In contrast, our case study involves
                                         open-ended exploration where the hypothesis itself was not given in advance or the objec-
                                         tive is shifted according to the exploration results emerged from the interaction with the AI
                                         agent.
                                             ∗ Algorithms and Complexity Group, TU Wien, Vienna, Austria
                                             † Department of Computer Science, Cornell University, USA
    In general, how each component contributes to the final mathematical discovery is am-
biguous, like the sequence of dead ends, pivots, and insights leading from an open question
to some novel results. Even though the post-hoc description can be traced back, it is not
clear how distinct contributions are made by neural reasoning, symbolic computation, and
human judgments, separately or collaboratively. Without the detailed process analysis, it
is challenging to reproduce discovery workflows, not to mention designing more efficient
workflows in a principled methodology.
    In this paper, we present a detailed case study that addresses this gap. From the inter-
action logs spanning several days and multiple sessions, we reconstruct the discovery of a
tight lower bound on the imbalance of Latin squares, a fundamental problem in combinato-
rial design theory with applications in experimental design [Jones et al., 2015, van Es and
van Es, 1993]. Our result settles an open question for the imbalance of the Latin squares
case n ≡ 1 (mod 3). The discovery process involved an AI agent, an interactive LLM-based
assistant with access to different symbolic tools (computer algebra systems and constraint
solvers) and human strategic direction. Through the analysis of contributions from different
components of the framework, we found the agent’s primary strength was uncovering hidden
structure. For example, in our setting, the agent discovered a parity constraint from the
numerical data that had been produced by the symbolic solvers in the exhaustive search.
For the verification of some conjectures from the LLM, the symbolic tools can work on
the rigorous search by scaling and verifying the instances across different orders. Human
steering contributed to the critical research pivot: changing the question from “find objects
with zero imbalance” to “characterize the minimum positive imbalance.” We also find that
multi-model review among frontier LLMs was reliable for criticism.
    More specifically, our main contributions are as follows.
    (1) An agentic neurosymbolic collaboration framework: We propose an agentic
neurosymbolic collaborative framework for mathematical discovery in which an LLM-based
agent orchestrates symbolic computation tools, parallel multi-model review, and a two-tier
persistent memory system that enables multi-session research continuity, while a human
researcher provides strategic direction. (2) Mathematical discovery in combinatorial
design: We demonstrate the effectiveness of our framework on an open problem in com-
binatorial design theory. In particular, our framework led to a new research direction and
a concrete mathematical discovery in combinatorial design comprising: (i) the introduc-
tion of the concept of near-perfect permutations for Latin squares; (ii) a theorem stating a
tight lower bound of 4n(n−1)/9 on the imbalance of Latin squares for n ≡ 1 (mod 3) for
near-perfect permutations that achieve this bound, and (iii) empirical verification of their
existence up to n = 52. (3) Asymmetry in multi-model review: We show that multi-
model review among frontier LLMs is reliable for criticism and error detection but unreliable
for constructive mathematical claims, an asymmetry with implications for neurosymbolic
system design. (4) Process-level analysis of discovery: We provide a fine-grained
process-level analysis of the discovery, reconstructed from interaction logs, that identifies
the distinct contributions of neural pattern recognition, symbolic computation, and human
strategic judgment across five phases, showing all three components are required.

  1. An agentic neurosymbolic collaboration framework. We propose a framework for math-
     ematical discovery in which an LLM-based agent orchestrates symbolic computation
     tools, parallel multi-model review, and a two-tier persistent memory system that en-
     ables multi-session research continuity without updating model weights, while a human
     researcher provides strategic direction.
  2. Mathematical discovery in combinatorial design. We demonstrate the effectiveness of
     our framework on an open problem in combinatorial design theory. Our framework
     led to a new research direction and a concrete mathematical discovery comprising:


                                             2
       (i) the introduction of the concept of near-perfect permutations for Latin squares;
       (ii) a theorem stating a tight lower bound of 4n(n−1)/9 on the imbalance of Latin
       squares for n ≡ 1 (mod 3), with near-perfect permutations that achieve this bound;
       and (iii) empirical verification of their existence up to n = 52.
    3. Asymmetry in multi-model review. We show that multi-model review among frontier
       LLMs is reliable for criticism and error detection but unreliable for constructive math-
       ematical claims, an asymmetry with implications for neurosymbolic system design.
    4. Process-level analysis of discovery. We provide a fine-grained process-level analysis
       of the discovery, reconstructed from interaction logs, that identifies the distinct con-
       tributions of neural pattern recognition, symbolic computation, and human strategic
       judgment across five phases. A counterfactual analysis shows that the discovery re-
       quired all three components.


2      Problem Setting
An n × n Latin square L is an array filled with n different symbols such that each symbol
occurs exactly once in each row and each column. Latin squares are fundamental objects
in combinatorics, with applications in many fields of experimental design, where spatial
balance among treatments is important [Jones et al., 2015, van Es and van Es, 1993].
    We denote rows, columns, and symbols by Zn = {0, . . . , n−1}. For a row r and symbol s,
we write pos(r, Ps) for the column containing s in row r. The distance between rows r1 and r2
is d(r1 , r2 ) = s∈Zn |pos(r1 , s) − pos(r2 , s)|, and the imbalance of L [Dı́az et al., 2017] is

                                    1       X
                           I(L) =                   |3 · d(r1 , r2 ) − n(n+1)|.              (1)
                                    3
                                        0≤r1 <r2 ≤n−1

A Latin square is spatially balanced (an SBLS) [Gomes and Sellmann, 2004] when I(L) = 0.
This requires 3 | n(n+1), i.e., n ̸≡ 1 (mod 3) [Zheng and Cao, 2022]. For n ≡ 1 (mod 3), the
ideal distance n(n+1)/3 is not an integer, so perfect balance is impossible. The imbalance
of Latin squares has been studied computationally by Smith et al. [2005], Dı́az et al. [2017],
Ramaswamy and Szeider [2023], Voboril et al. [2025], Zheng and Cao [2022]. However, the
minimum achievable imbalance for n ≡ 1 (mod 3) had remained open.
    Our human-AI contribution is a tight lower bound on this Latin square imbalance. The
discovery process was based on an AI agent, an interactive assistant powered by Anthropic’s
Claude Opus 4.5 large language model, which operated in a terminal environment with full
access to a file system, shell commands, and external tools. The agent used the following
symbolic tools: (i) a computer algebra system (using SageMath through the Model Context
Protocol, MCP server1 ) for algebraic analysis; (ii) a custom high-performance solver written
in Rust for exhaustive enumeration of combinatorial objects; and (iii) simulated annealing
search implemented in Python with JIT compilation. The human researcher interacted with
the agent through natural-language dialogue, steering the research direction.


3      The Discovery Process
We describe the discovery from interaction logs spanning five days and approximately fifteen
sessions. The process consists of five phases as summarized below. The general collaboration
follows the architecture shown in Figure 1, where the human researcher sets strategic goals
    1 https://pypi.org/project/mcp-sage/




                                                        3
                                                               Human Researcher


                                                 Research directions,                      Hypotheses,
                                                  quality judgments                     conjectures, proofs

                       Proof drafts, claims                                                                   Handover updates, new topics
      Multi-model Review                                                                                                            Persistent Memory
                                                                    LLM Agent                                                          Project state file,
      Parallel frontier LLM
          consultation                                              Claude Opus 4.5
                                                                                                                                    knowledge base, handover
                      Criticism, error reports                                                          Project state, dead ends, knowledge


                                   Generated code,                                                     Results, data,
                                 scripts, parameters                                                  counterexamples




                                 Rust Solver                            SageMath                                SA Search
                              Exhaustive enumeration                    Exact algebra                    Stochastic optimization




Figure 1: Collaboration architecture and data flow. Rounded boxes represent actors (hu-
man, agent, symbolic tools); italic labels on arrows show the data exchanged. Solid arrows
indicate instructions or programs. Dashed arrows indicate results or feedback. The AI
agent manages all interactions between different components. It dispatches proofs to mul-
tiple frontier LLMs for critical reviews (left). Meanwhile, it maintains a three-component
persistent memory system (right), consisting of a project state file, a searchable knowledge
base, and a session handover protocol.


and decides when to change direction, and the AI agent translates these goals into executable
code for running the symbolic tools, and synthesizing results into conjectures and proofs. On
one hand, the data flows downward as generated code and parameters. On the other hand,
they flow upward as results, counterexamples, and verification results. For supporting the
long-persistent runs among multiple sessions where the new sessions begin at the previous
ends, a three-component persistent memory system (Section 3.6) is designed to carry project
state, documented dead ends, and a searchable knowledge base.
    We have five phases illustrating different facets of the discovery loop: Phase 1 (Sec-
tion 3.1) does algebraic exploration, ending with a documented dead end; Phase 2 (Sec-
tion 3.2) is a human-initiated research pivot, shifting from the previous goal to a more
promising research direction; Phase 3 (Section 3.3) indicates how the agent discovers the
parity constraint from numerical data and then drafts an elementary proof; Phase 4 (Sec-
tion 3.4) uses multiple-model consultation to catch errors in the proof during the review;
and Phase 5 (Section 3.5) extends the computational verification by scaling up the orders
of the near-perfect permutations.

3.1      Dead End: Algebraic Reverse-Engineering
Our original goal was to find algebraic constructions
                                              P         for perfect permutations, permuta-
tions σ of Zn whose shift correlation fσ (δ) = j |σ(j+δ) − σ(j)| equals n(n+1)/3 for every
shift δ. Such permutations can result in spatially balanced Latin squares by circulant con-
structions [Zheng and Cao, 2022, LeBras et al., 2012].
    By calling the Rust solver, the agent enumerated all perfect permutations for n = 12.
Then the agent did the algebraic analysis with SageMath. But all the analyses showed
there is no algebraic construction for multiple n except n = 3 and 5, in the range from 3
to 17. For all n ≥ 6, perfect permutations end up structureless in the symmetric group Sn .
Accordingly, we concluded the algebraic approach could not get perfect permutations for all
orders.




                                                                                4
3.2    The Research Pivot
Even though we have negative results for the initial goal, constructing the solutions, we
have two observations inspiring a change of research direction. The first observation is that
the exhaustive solver hit a combinatorial wall at n = 18: even with symmetry breaking and
multi-core parallelism, no perfect permutation could be found within a one-hour timeout.
Meanwhile, no perfectly balanced solutions can exist for n ≡ 1 (mod 3). Second, the alge-
braic analysis of Section 3.1 showed that even known perfect permutations resist closed-form
description.
    The human researcher made the critical decision about changing the research question
entirely. The initial goal was to search for objects with zero imbalance. However, the new
conceptualized question is about the minimum positive imbalance for different orders n
with n ≡ 1 (mod 3). Retrospectively, this switch of the research question was decisive in
the discovery loop, reframing the search problem as an optimization problem and opening
a new thread of questions.

3.3    Parity from Data Anomaly
With the new question in hand, the agent computed a naive lower bound for n = 13. Since
n(n+1)/3 = 60.67 . . . is not an integer, each distance d(r1 , r2 ) must deviate from it by at
least 1/3 after the scaling in (1), giving a naive lower bound of I ≥ n(n−1)/6 = 26.
    However, when the agent ran the simulated annealing algorithm, the best found imbal-
ance was 69.3. That is more than two times above the naive bound. This huge gap in the
imbalance triggered a necessary explanation about the theoretical minimum.
    To this end, the agent investigated by examining the shift correlations fσ (δ) for the
best permutation found. The observation: fσ (δ) was even for every shift δ. A check
confirmed that all permutations exhibit this parity constraint, which was not specific to the
particular permutation. The proof also came together:
                                                                                P
   1. Since |a − b| ≡ a + b (mod 2) for all integers, the distance d(r1 , r2 ) ≡ s (pos(r1 , s) +
      pos(r2 , s)) ≡ n(n−1) ≡ 0 (mod 2).
   2. If every distance is even and the ideal value n(n+1)/3 is non-integer, then the minimum
      deviation per pair is not 1 but 2, doubling the lower bound.
                                                                   d = n2 (n2 −1)/6, this yields
                                                                P
   3. Using a careful case analysis with the sum constraint
      I ≥ 4n(n−1)/9.
The agent did the verification by comparing the minimum imbalance over all 576 Latin
squares of order 4 with the new bound. The results matched exactly, so the new bound is
confirmed.
    The total time from posing the question to a verified proof was less than one session,
approximately one hour. This was the shortest and most consequential session of the project.
    By computing the shift correlations for many permutations, the agent could recognize
the pattern (all values even) that a human is unlikely to discover without special focus. The
proof itself is not complex (four lines of modular arithmetic); however, finding it required the
structure-discovery step that came from inspecting numerical data and preliminary lemmas
(like Lemma 1).

3.4    Formalization and Multi-Model Review
To guarantee the correctness of the proof, we tried to get the formal proof. However, the
formalization exposed two errors that the initial discovery session had missed.




                                               5
The circulant trap. The first proof draft was actually based on the properties specific
to circulant Latin squares (the shift correlation function fσ ). However, Opus 4.5 claimed it
holds for all Latin squares. This error was found by calling multiple-model reviews, where
four frontier LLMs were consulted in parallel, and one of them correctly identified that the
generality of the proof does not hold for all Latin squares. Therefore, the proof was fixed
by proving the bound purely from the Parity Lemma and the sum constraint, instead of the
circulant structure property.

The σ/σ −1 mismatch. The circulant construction L[i][j] = (i + σ(j)) mod n has row
distances determined by σ −1 , not by σ. This subtle error was caught during formalization
and resolved by redefining the construction with τ = σ −1 .

Multi-model reliability. The same multi-model review that caught the circulant trap
also confidently claimed that the modular inversion map σ(j) = j −1 mod p would achieve
O(n5/2 ) imbalance. Our experiments showed this claim was wrong: inversion scales as
Θ(n3.6 ). This pattern recurred throughout the project: multi-model review proved reliable
for criticism but unreliable for constructive claims.

3.5    Computational Extension
To match the lower bound, the agent did a minimum relaxation of the perfect permutations
that is compatible with the parity and divisibility constraints. The relaxation is introduced
as near-perfect permutations: permutations σ with fσ (δ) ∈ {a, a+2} for all δ, where a =
(n(n+1)−2)/3.
    A simulated annealing search found near-perfect permutations for all n ≡ 1 (mod 3) up
to n = 52, each achieving exactly I = 4n(n−1)/9. In contrast, the prior computational
work did not reach the optimum even at n = 10 as the results show in the recent paper [Ra-
maswamy and Szeider, 2023]. Furthermore, the agent also investigated whether algebraic
constructions could produce near-perfect permutations for large n. Its analysis of charac-
ter sums over finite fields could show a fundamental barrier, proving the perfect imbalance
cannot be closed by algebraic methods at all.

3.6    Persistent Learning Across Sessions
We equipped the agent with a structured persistent memory organized in two tiers following
a progressive disclosure design. The first tier is a project instruction file that the agent
reads at the start of every session. This file records accomplished goals, open questions, key
formulas, tool usage patterns, and, critically, documented dead ends. At the end of each
session, a handover protocol updates this file with new results, failed approaches, and next
steps. The second tier consists of a collection of topic files, each tagged with keywords and a
short context description. At session start, the agent receives only a compact index of these
files; the full content of any topic file is retrieved on demand through keyword search. This
two-tier design makes the context window of the agent relatively small at the beginning.
Meanwhile, it provides access to the entire accumulated knowledge base when a specific
topic becomes relevant.
     This memory mechanism played a concrete role in the discovery. When the agent began
the pivotal session (Section 3.3), it had access to a detailed record of the algebraic dead
end: which constructions had been tried, why they failed, and the explicit instruction “do
not retry.” This prevented the agent from revisiting unproductive directions and focused its
effort on the new research question. Similarly, the memory of all 672 perfect permutations
for n = 12, the Rust solver’s performance characteristics, and the exact formulas used in


                                              6
prior sessions provided the agent with accumulated context that no single session could have
built from scratch.
    From a neurosymbolic perspective, this persistent memory is a form of external symbolic
state that compensates for the agent’s lack of long-term memory. Each session, the LLM
begins with a fresh context window; the memory system augments sessions by externalizing
knowledge into structured, human-readable files that both the agent and the researcher
can inspect and modify. This design gives rise to a form of incremental learning that is
purely symbolic (no model weights are updated) yet provides the continuity essential for
multi-session research projects.


4     The Mathematical Result
We now state the mathematical result precisely. For a self-contained presentation, we include
full proofs of the main theorem; the construction that achieves the bound appears as a
corollary.

4.1    The Lower Bound
The argument is only based on the two properties of row-pair distances that hold for every
n × n Latin square.
Lemma 1 (Fixed sum). For every n × n Latin square L, r1 <r2 d(r1 , r2 ) = n2 (n2 − 1)/6.
                                                         P

Proof.  For each symbol s, the positions pos(r, s) form a permutation of Zn , so
                                          2
P
  r1 <r2 |pos(r1 , s) − pos(r2 , s)| = n(n −1)/6. Summing over all n symbols gives the re-
sult.
Lemma 2 (Parity). For every n × n Latin square L and every pair of rows r1 , r2 , the
distance d(r1 , r2 ) is even.
                                                                                 Pn−1
Proof. Since |a−b| ≡ a+b (mod 2) for all integers a, b, we have d(r1 , r2 ) ≡ s=0 (pos(r1 , s)+
pos(r2 , s)) P
             (mod 2). For each row r, the values pos(r, 0), . . . , pos(r, n−1) form a permutation
of Zn , so    s pos(r, s) = n(n−1)/2. Therefore d(r1 , r2 ) ≡ 2 · n(n−1)/2 = n(n−1) ≡ 0
(mod 2).

Theorem 3. For n ≡ 1 (mod 3), every n × n Latin square L satisfies I(L) ≥ 4n(n−1)/9.
Proof. Let N = n2 and a = (n(n+1)−2)/3. Writing n = 3k+1, one verifies that a =
                  

3k(k+1) is a nonnegative even integer and N/3 = k(3k+1)/2 is an integer.
   By Lemma 2,Peach distance is even, so we write d(r1 , r2 ) = a + 2xr1 ,r2 for integers xr1 ,r2 .
Lemma 1 gives r1 <r2 d(r1 , r2 ) = N · n(n+1)/3 = N (a + 2/3), hence
                                   P
                                     r1 <r2 xr1 ,r2 = N/3.                                    (2)

Since 3a = n(n+1) − 2, the deviation for each pair is 3 d − n(n+1) = −2 + 6x. We claim
the pointwise inequality

                           |−2 + 6x| ≥ 2 + 2x       for every integer x.                       (3)

Indeed: for x ≥ 1, 6x − 2 ≥ 2 + 2x since 4x ≥ 4; for x = 0, both sides equal 2; for x ≤ −1,
the left side is 2 − 6x ≥ 8 while 2 + 2x ≤ 0.               P
   Summing (3) over all row pairs and applying (2) yields r1 <r2 |3d − n(n+1)| ≥ 2N +
2N/3 = 8N/3. Therefore I(L) ≥ 8N/(3 · 3) = 8N/9 = 4n(n−1)/9.


                                                7
4.2       The Matching Construction
                                                                          P
The shift correlation of a permutation σ : Zn → Zn at shift δ is fσ (δ) = j∈Zn |σ(j+δ) −
σ(j)|. For the circulant Latin square L[i][j] = (i + σ −1 (j)) mod n, the distance between
rows at offset δ equals fσ (δ).
Definition 4. A permutation σ of Zn is a near-perfect permutation (near-PP) if n ≡ 1
(mod 3) and fσ (δ) ∈ {a, a+2} for every δ ∈ {1, . . . , n−1}, where a = (n(n+1) − 2)/3.

Proposition 5. If σ is a near-PP of order n, then the circulant Latin square L[i][j] =
(i + σ −1 (j)) mod n has I(L) = 4n(n−1)/9.
Proof. Since fσ (δ) ∈ {a, a+2}, every row-pair distance satisfies d = a + 2x with x ∈ {0, 1}.
For both values, equality holds in (3): |−2+6·0| = 2 = 2+2·0 and |−2+6·1| = 4 = 2+2·1.
Hence the lower bound I(L) ≥ 4n(n−1)/9 from Theorem 3 is attained with equality.

Theorem 6. Near-perfect permutations exist for every n ≡ 1 (mod 3) with 4 ≤ n ≤ 52.
   Table 1 summarizes the computational results. Each entry was found by simulated
annealing and independently verified.


Table 1: Near-PP existence for n ≡ 1 (mod 3), 4 ≤ n ≤ 52. Each achieves the optimal
imbalance I ∗ = 4n(n−1)/9. Times are in seconds obtained on the machine equipped with
CPU i7-1260P and 32 GB RAM under the operating system Ubuntu 24.04.3 LTS.
n          I∗   Time (s)     n        I∗    Time (s)       n       I∗   Time (s)   n       I∗   Time (s)
 4      16/3          <1    19      152           1    34      1496/3         5 49     3136/3        54
 7      56/3          <1    22    616/3           2    37         592         5 52     3536/3        32
10        40          <1    25    800/3           2    40      2080/3        74
13     208/3          <1    28      336           2    43      2408/3       139
16     320/3           1    31   1240/3           4    46         920        31



4.3       Formal Verification in Lean 4
We formally verified the lower bound (Theorem 3) in the Lean 4 proof assistant [de Moura
and Ullrich, 2021] with the Mathlib library, using the LeanBack MCP server2 . The for-
malization includes the definition for Latin squares as a function Fin n → Fin n → Fin n
with row and column bijectivity, the two lemmas (the Parity Lemma and the Fixed Sum
Lemma), and the main inequality property. It is around 340 lines of Lean formalization
code, and here is the key theorem statement where we use imbalance3 = 3 · I(L) to avoid
rational arithmetic in the formalization.

theorem LatinSquare.imbalance_lower_bound
    (L : LatinSquare n) (hn : n % 3 = 1) :
    3 * L.imbalance3 >= 4 * ↑n * (↑n - 1)
     2 https://pypi.org/project/leanback/




                                                       8
5     Analysis of the Discovery Process
5.1    Role Taxonomy
Table 2 maps each phase of the discovery to its primary function and the components.
Briefly, the agent uncovered hidden structure (the all-even parity pattern) from the numer-
ical data of permutations and then generated hypotheses. Meanwhile, the critical reviews
from multiple models can catch errors. The symbolic components, including the Rust
solver, SageMath, and simulated annealing, provided exhaustive enumeration and algebraic
analysis, confirming conjectures from the LLM. The human made a key decision for the
research question, shifting the current goal to a more promising direction.


Table 2: Contributions by component across discovery phases. A = agent, S = symbolic
(solvers, CAS), H = human.

          Phase / Step                      Function                        Role
          Enumerate PPs (n ≤ 17)            Exhaustive search                S
          Algebraic analysis                Pattern search (negative)        S
          Confirm dead end                  Rigorous verification            S
          Change research question          Strategic reframing              H
          Compute naive bound               Numerical reasoning              A
          Notice f (δ) always even          Uncovering hidden structure      A
          Formulate the parity hypothesis   Abductive reasoning              A
          Prove Parity Lemma                Proof construction              A+S
          Prove a lower bound               Proof construction              A+S
          Catch a circulant trap            Critical review                  A
          Fix σ/σ −1 error                  Formal debugging                A+S
          Find near-PPs (n ≤ 52)            Stochastic search                S
          Weil bound analysis               Theoretical reasoning            A



5.2    Counterfactual Analysis
Without the agent, the parity observation would have been unlikely discovered. As the pat-
tern emerges only from systematic numerical exploration across many orders (dimensions).
In the meanwhile, symbolic tools are the key for verifying the observation and checking
proofs contained errors that only formal checking exposed. Without human steering, the
research would have remained in the algebraic dead end because the agent did not propose
the pivot resulting in the final discoveries.


6     Related Work
Recent work on AI for mathematical discovery includes AI-guided conjectures [Davies et al.,
2021], LLM-based program search [Romera-Paredes et al., 2024], automated geometry prov-
ing [Trinh et al., 2024], conjecture generation on fundamental constants [Raayoni et al.,
2021], and LLM-assisted formal proving [Yang et al., 2023]. We focus on the process rather
than on the end result; the central role of human steering sets our work apart. d’Avila
Garcez and Lamb [2023] articulate the neurosymbolic vision of integrating neural and sym-
bolic reasoning. Evaluations of LLM mathematical capabilities [Frieder et al., 2023] are


                                            9
consistent with our findings. LLMs excel at pattern recognition but struggle with rigor and
strategic planning.


7    Conclusion
We have presented an agentic neurosymbolic collaboration framework for a genuine mathe-
matical discovery, a tight lower bound on Latin square imbalance together with a new class
of near-perfect permutations. Our analysis reveals that the discovery required all three
components: neural recognition to notice the parity constraint, symbolic computation to
verify and extend the result, and human judgment to redirect the research when the initial
approach stalled.
    The failure modes are equally instructive. Multi-model review among frontier LLMs
proved reliable for criticism (catching errors in proofs) but unreliable for constructive claims.
The most important contribution of the human was recognizing the degree of promise of the
research question itself and making the decisive shift from the current research question to
another promising one.
    We see several possibilities for improving neurosymbolic discovery systems. First, in-
tegrating systematic verification into the agent’s reasoning loop could catch errors like the
circulant trap earlier. Second, developing meta-cognitive capabilities, the ability to recog-
nize unproductive research directions, could reduce dependence on human steering. Third,
there are close ties between criticism and construction in multi-model review and this asym-
metry deserves further study. Understanding why LLM-based agents are better critics than
constructors has implications for both system design and training objectives.

Supplementary material. The interaction-log excerpts and the full session timeline
are also provided as standalone supplementary files at https://doi.org/10.5281/zenodo.
20530914.

Acknowledgements
This project is partially supported by an AI2050 Senior Fellowship, a Schmidt Sciences
program, the National Science Foundation, the National Institute of Food and Agriculture
and the Air Force Office of Scientific Research.
        This project is also partially supported by the European Union’s Horizon 2020
        research and innovation programme under the Marie Sklodowska-Curie grant agree-
        ment No. 101034440, and by the Austrian Science Fund (FWF) within the Cluster
of Excellence Bilateral Artificial Intelligence (10.55776/COE12) and 10.55776/P36420. This
research is supported by the Marshall Plan Foundation as part of the Marshall Plan Schol-
arship.


References
A. Davies, P. Velickovic, L. Buesing, S. Blackwell, D. Zheng, N. Tomasev, R. Tanburn, P. W.
  Battaglia, C. Blundell, A. Juhász, M. Lackenby, G. Williamson, D. Hassabis, and P. Kohli.
  Advancing mathematics by guiding human intuition with AI. Nat., 600(7887):70–74, 2021.
  doi: 10.1038/S41586-021-04086-X. URL https://doi.org/10.1038/s41586-021-04086-x.
A. d’Avila Garcez and L. C. Lamb. Neurosymbolic AI: the 3rd wave. Artif. Intell. Rev.,
  56(11):12387–12406, 2023. doi: 10.1007/S10462-023-10448-W. URL https://doi.org/10.
  1007/s10462-023-10448-w.


                                               10
L. de Moura and S. Ullrich. The lean 4 theorem prover and programming language. In
  A. Platzer and G. Sutcliffe, editors, Automated Deduction - CADE 28 - 28th International
  Conference on Automated Deduction, Virtual Event, July 12-15, 2021, Proceedings, vol-
  ume 12699 of Lecture Notes in Computer Science, pages 625–635. Springer, 2021. doi:
  10.1007/978-3-030-79876-5\ 37. URL https://doi.org/10.1007/978-3-030-79876-5 37.

M. Dı́az, R. L. Bras, and C. P. Gomes. In search of balance: The challenge of generat-
 ing balanced latin rectangles. In D. Salvagnin and M. Lombardi, editors, Integration
 of AI and OR Techniques in Constraint Programming - 14th International Conference,
 CPAIOR 2017, Padua, Italy, June 5-8, 2017, Proceedings, volume 10335 of Lecture Notes
 in Computer Science, pages 68–76. Springer, 2017. doi: 10.1007/978-3-319-59776-8\ 6.
 URL https://doi.org/10.1007/978-3-319-59776-8 6.

S. Frieder, L. Pinchetti, A. Chevalier, R. Griffiths, T. Salvatori, T. Lukasiewicz, P. Pe-
  tersen, and J. Berner. Mathematical capabilities of chatgpt. In A. Oh, T. Nau-
  mann, A. Globerson, K. Saenko, M. Hardt, and S. Levine, editors, Advances in
  Neural Information Processing Systems 36: Annual Conference on Neural Infor-
  mation Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, Decem-
  ber 10 - 16, 2023, 2023. URL http://papers.nips.cc/paper files/paper/2023/hash/
  58168e8a92994655d6da3939e7cc0918-Abstract-Datasets and Benchmarks.html.
C. P. Gomes and M. Sellmann. Streamlined constraint reasoning. In M. Wallace, edi-
  tor, Principles and Practice of Constraint Programming - CP 2004, 10th International
  Conference, CP 2004, Toronto, Canada, September 27 - October 1, 2004, Proceedings,
  volume 3258 of Lecture Notes in Computer Science, pages 274–289. Springer, 2004. doi:
  10.1007/978-3-540-30201-8\ 22. URL https://doi.org/10.1007/978-3-540-30201-8 22.
M. Jones, R. Woodward, and J. Stoller. Increasing precision in agronomic field trials using
 Latin square designs. Agronomy Journal, 107(1):20–24, 2015. doi: 10.2134/agronj14.0232.
R. LeBras, C. P. Gomes, and B. Selman. From streamlined combinatorial search to effi-
  cient constructive procedures. In J. Hoffmann and B. Selman, editors, Proceedings of the
  Twenty-Sixth AAAI Conference on Artificial Intelligence, July 22-26, 2012, Toronto, On-
  tario, Canada, pages 499–506. AAAI Press, 2012. doi: 10.1609/AAAI.V26I1.8147. URL
  https://doi.org/10.1609/aaai.v26i1.8147.
G. Raayoni, S. Gottlieb, Y. Manor, G. Pisha, Y. Harris, U. Mendlovic, D. Haviv, Y. Hadad,
  and I. Kaminer. Generating conjectures on fundamental constants with the ramanujan
  machine. Nat., 590(7844):67–73, 2021. doi: 10.1038/S41586-021-03229-4. URL https:
  //doi.org/10.1038/s41586-021-03229-4.
V. P. Ramaswamy and S. Szeider. Proven optimally-balanced latin rectangles with SAT
  (short paper). In R. H. C. Yap, editor, 29th International Conference on Principles and
  Practice of Constraint Programming, CP 2023, Toronto, Canada, August 27-31, 2023,
  volume 280 of LIPIcs, pages 48:1–48:10. Schloss Dagstuhl - Leibniz-Zentrum für Infor-
  matik, 2023. doi: 10.4230/LIPICS.CP.2023.48. URL https://doi.org/10.4230/LIPIcs.CP.
  2023.48.
B. Romera-Paredes, M. Barekatain, A. Novikov, M. Balog, M. P. Kumar, E. Dupont, F. J. R.
  Ruiz, J. S. Ellenberg, P. Wang, O. Fawzi, P. Kohli, and A. Fawzi. Mathematical discoveries
  from program search with large language models. Nat., 625(7995):468–475, 2024. doi:
  10.1038/S41586-023-06924-6. URL https://doi.org/10.1038/s41586-023-06924-6.




                                            11
C. Smith, C. P. Gomes, and C. Fernández. Streamlining local search for spatially balanced
  latin squares. In L. P. Kaelbling and A. Saffiotti, editors, IJCAI-05, Proceedings of the
  Nineteenth International Joint Conference on Artificial Intelligence, Edinburgh, Scotland,
  UK, July 30 - August 5, 2005, pages 1539–1540. Professional Book Center, 2005. URL
  http://ijcai.org/Proceedings/05/Papers/post-0460.pdf.

T. H. Trinh, Y. Wu, Q. V. Le, H. He, and T. Luong. Solving olympiad geometry without
  human demonstrations. Nat., 625(7995):476–482, 2024. doi: 10.1038/S41586-023-06747-5.
  URL https://doi.org/10.1038/s41586-023-06747-5.
H. M. van Es and C. L. van Es. Spatial nature of randomization and its effect on the outcome
  of field experiments. Agronomy Journal, 85(2):420–428, 1993. doi: 10.2134/agronj1993.
  00021962008500020046x.
F. Voboril, V. P. Ramaswamy, and S. Szeider. Balancing latin rectangles with LLM-
  generated streamliners. In M. G. de la Banda, editor, 31st International Confer-
  ence on Principles and Practice of Constraint Programming, CP 2025, Glasgow, Scot-
  land, August 10-15, 2025, volume 340 of LIPIcs, pages 36:1–36:17. Schloss Dagstuhl -
  Leibniz-Zentrum für Informatik, 2025. doi: 10.4230/LIPICS.CP.2025.36. URL https:
  //doi.org/10.4230/LIPIcs.CP.2025.36.
K. Yang, A. M. Swope, A. Gu, R. Chalamala, P. Song, S. Yu, S. Godil, R. J. Prenger,
  and A. Anandkumar. Leandojo: Theorem proving with retrieval-augmented language
  models. In A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt, and S. Levine,
  editors, Advances in Neural Information Processing Systems 36: Annual Conference on
  Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA,
  December 10 - 16, 2023, 2023. URL http://papers.nips.cc/paper files/paper/2023/hash/
  4441469427094f8873d0fecb0c4e1cee-Abstract-Datasets and Benchmarks.html.
H. Zheng and H. T. Cao. Perfect permutations and spatially balanced Latin squares. Acta
  Mathematica Sinica, Chinese Series, 65(5):939–950, 2022. doi: 10.12386/A20210055.




                                            12
