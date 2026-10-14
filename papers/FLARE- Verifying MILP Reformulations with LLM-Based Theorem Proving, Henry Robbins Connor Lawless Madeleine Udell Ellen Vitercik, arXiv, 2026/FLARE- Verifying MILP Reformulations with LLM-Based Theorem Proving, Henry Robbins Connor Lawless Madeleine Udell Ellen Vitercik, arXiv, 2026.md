                                                    FLARE: V ERIFYING MILP R EFORMULATIONS WITH
                                                                     LLM-BASED T HEOREM P ROVING


                                              Henry Robbins                 Connor Lawless                Madeleine Udell                Ellen Vitercik
                                             Stanford University           Stanford University           Stanford University           Stanford University
                                             hwr@stanford.edu          lawlessc@stanford.edu           udell@stanford.edu          vitercik@stanford.edu
arXiv:2608.25220v1 [cs.AI] 25 Aug 2026




                                                                                              A BSTRACT
                                                    Mixed-Integer Linear Programming (MILP) is a fundamental tool for combinatorial optimization with
                                                    extensive real-world applications. A central challenge is designing computationally efficient MILP
                                                    formulations. Large Language Models (LLMs) offer new opportunities to automate the modeling
                                                    process, from deriving formulations to strengthening them. Reliable automation requires robust
                                                    methods for verifying that proposed formulations preserve the underlying optimization problem.
                                                    However, existing approaches evaluate formulations numerically and fail to reason about general
                                                    problem instances. We resolve this limitation by introducing a constructive definition of MILP
                                                    reformulation that can be formalized in Lean and machine-checked. We develop FLARE1 (Formulation-
                                                    Level Automated Reformulation Evaluation), a method that uses an LLM-based agent and the Lean
                                                    proof assistant to verify proposed reformulations against a reference formulation. To evaluate
                                                    our approach, we introduce FormulationBench2 , a challenging dataset of 20 problems and 109
                                                    formulations. FLARE outperforms existing methods, with 100% accuracy on the NP-hard subset
                                                    of FormulationBench. Furthermore, FLARE produces a machine-checkable certificate for every
                                                    reformulation it accepts. For cases where formal guarantees are not necessary, we introduce FLARE-NL,
                                                    a fast and cheap LLM proxy that matches FLARE’s accuracy but produces no certificate.3 These
                                                    methods enable reliable verification in automated optimization modeling.

                                         Keywords Mixed Integer Linear Programming · Automated Theorem Proving · Large Language Models

                                         1       Introduction
                                         Mixed-Integer Linear Programming (MILP) is a fundamental tool for combinatorial optimization with applications
                                         in scheduling [17, 32], planning [48], energy [31, 45], and chip design [53]. A central challenge in MILP is problem
                                         formulation: translating a real-world scenario into a concrete mathematical model. Historically, problem formulation
                                         has required significant technical expertise. However, recent work has highlighted the ability of LLMs to translate
                                         natural-language problem descriptions into MILP formulations [1, 3, 9, 25, 63]. The primary objective is to generate
                                         MILP formulations that faithfully represent the underlying optimization problem.
                                         Developing a faithful formulation is just the first stage in the modeling process. The same problem can often be expressed
                                         by multiple formulations that can lead to dramatically different solve times. In practice, experts use techniques like
                                         reformulation [56], decomposition [61], and cutting planes [43] to obtain efficient MILP formulations. LLMs offer the
                                         potential to automate this process [16, 66]. More generally, we can view optimization modeling as a special case of
                                         algorithm design, where the chosen model dictates the algorithm’s runtime. In this broader context, LLMs have recently
                                         been used to iteratively evolve efficient algorithms through generation and evaluation [41, 47, 52, 67]. This approach
                                         has led to advances in mathematical discovery [22], vehicle routing [24, 64], and system design [23].
                                         Key Challenges. A central challenge in automated algorithm design, particularly acute in the context of optimization
                                         modeling, is to ensure that an AI-generated formulation faithfully represents the original problem. Existing approaches
                                         rely heavily on heuristics, most commonly comparing optimal objective values on a single instance [1, 25, 37]. However,
                                             1
                                               FLARE is implemented in the milp-flare Python package; see https://flare.henryrobbins.com.
                                             2
                                               Download via the formulation-bench Python package; see https://formulation-bench.henryrobbins.com.
                                             3
                                               All experimental code is available at https://github.com/henryrobbins/flare.
                       FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



 A                                                                 B
        A                                                                           import Common


        {}
                                                                                    import A.Formulation
                       Formulation A Lean Formalization                             import B.Formulation

                         def formulation : MILPFormulation where                    def Reformulation :
                           Params := Params                                            MILPReformulation A.formulation B.formulation where
                 >_        Vars     := Vars
                           feasible := Feasible
                                                                                      ...

                           obj      := obj


                                                                   ... and then iteratively

                        The agent harness translates the
                        templated LaTeX description and code of
                                                                   constructs the reformulation
                                                                   proof with feedback from the
                                                                   Lean-LSP-MCP.
                                                                                                            >_                               Lean Process
                                                                                                                             Lean-LSP-MCP
                        both formulations to Lean, ...

        B
        {}             Formulation B Lean Formalization                             def Reformulation :
                                                                                       MILPReformulation A.formulation B.formulation where
                                                                                      paramMap    := paramMap
                         def formulation : MILPFormulation where
                           Params := Params                                           fwd         := fwd
                 >_        Vars     := Vars
                           feasible := Feasible
                                                                                      bwd
                                                                                      fwd_feas
                                                                                                  := bwd
                                                                                                  := fwd_feas
                           obj      := obj                                            bwd_feas    := bwd_feas
                                                                                      objMap      := id
                                                                                      objMap_mono := strictMono_id
                                                                                      fwd_obj _ _ _ := rfl
                                                                                      bwd_obj _ _ _ := rfl




Figure 1: The FLARE workflow. (a) An agent is given templated LATEX and Python representations of a pair of MILP formulations and
their parameter mapping, and is instructed to formalize them in Lean. Combined with our Lean formalization of MILP reformulation,
these outputs yield a formal claim that formulation B is a reformulation of A under the fixed parameter map. (b) The agent then
attempts to construct a Lean proof of that claim. The Lean-LSP-MCP allows the agent to obtain detailed feedback from the Lean
process as it develops the proof.



such checks are unreliable and can fail under simple transformations such as adding cutting planes or rescaling an
objective (see [68] for a discussion).
Inspired by Karp reductions in complexity theory, Zhai et al. [68] introduced EquivaMap, which uses LLMs to discover
how solutions map between formulations. However, EquivaMap still operates at the instance level. It validates a
reformulation for a specific instance (e.g., a particular set of jobs to schedule) but not in general (e.g., any possible
set of jobs to schedule). Such instance-level checks can miss formulation inconsistencies that arise on other problem
instances. For example, we identify several cutting planes proposed by an LLM-based modeling framework called
EvoCut [66] that pass instance-level validation but remove optimal solutions for some instances. To mitigate this risk,
we seek formulation-level guarantees that hold for every problem instance. Such guarantees require reasoning over all
instances, rather than computationally evaluating a small subset of instances.
Our Contributions. This paper introduces FLARE, an automated framework for validating reformulations at the
formulation level. FLARE uses formal verification to make universal claims over problem instances machine-checkable,
leveraging recent advances in automated theorem proving (ATP) to generate reformulation proofs automatically [42].
Classic notions of reformulation require reasoning about optimal solution sets and are not well-suited to ATP. To address
this challenge, we introduce and formalize a constructive definition of reformulation that requires explicit mappings
between parameter spaces, feasible regions, and objective values. FLARE instantiates this definition with autoformalized
MILP formulations to obtain a formal statement that can be certified with ATP. Provided the formalizations are faithful,
a certificate proves a reformulation is valid for all problem instances. If ATP fails to produce a certificate, FLARE
does not certify the reformulation as valid. FLARE is the first automated approach to produce verifiable reformulation
certificates, enabling trustworthy optimization modeling with LLMs.
We also introduce FLARE-NL, a fast and cheap proxy that prompts a frontier reasoning model with the same definition.
The two methods serve different regimes. A FLARE certificate on faithful formalizations admits no false positives; this
property is critical in settings with zero tolerance for error (e.g., energy [31]). FLARE-NL is faster and cheaper but offers
no such guarantee, making it the natural choice in non-critical settings or as a screening heuristic prior to FLARE.
Our contributions can be summarized as follows:

     • Constructive definition of MILP reformulation. We introduce a constructive definition of MILP reformulation
       that is amenable to formal verification and ATP, enabling the first automated method for certifying reformulations
       at the formulation level.
     • AI for formulation verification. We develop FLARE, a framework that combines LLM-based autoformalization
       with ATP to generate machine-checkable reformulation certificates, and FLARE-NL, an LLM proxy that trades
       formal guarantees for improved speed and cost.


                                                                       2
                         FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



    • Realistic benchmark for reformulation. We introduce FormulationBench, a benchmark dataset of 20 problems
      and 109 formulations capturing realistic modeling transformations. Empirically, we show both FLARE and
      FLARE-NL outperform existing methods, achieving 100% accuracy on the NP-hard subset of FormulationBench.
    • Demonstrated need for formal proofs. We apply FLARE to prior AI-driven MILP transformations, revealing 5
      invalid cutting planes proposed by EvoCut [66] and 4 reformulations proposed in Ferchtandiker et al. [16]: these
      “equivalent” formulations are wrong or omit necessary assumptions (Appendix F).

2       Related Work
An efficient MILP formulation can decrease the solve time by orders of magnitude [11]. To improve solve time,
experts apply transformations such as lifting [6], change of variables [61], and cutting planes [55] that strengthen
the formulation while preserving optimal solutions (see [38] for a broader discussion). We study the complementary
problem of verifying such reformulations, particularly in emerging settings where formulations are generated or modified
by LLMs. This perspective connects three lines of research: (i) LLM-based systems that generate and refine MILP
formulations, (ii) methods for verifying reformulations, and (iii) autoformalization and automated theorem proving.
LLMs for MILP Modeling. A growing body of work has applied LLMs to automate the translation of natural
language problem descriptions into MILP formulations. Early efforts focused on natural language processing (NLP)
pipelines for structured extraction [49], while more recent optimization copilots use LLM-based multi-agent systems
[1–3, 15, 37, 46, 63] or fine-tuning [25, 28] to handle complex, multi-constraint problems. These capabilities have been
applied across domains including supply chain management [36], diagnosing infeasible models [8, 9], and scheduling
[33]. Beyond formulating a correct model, recent work has also explored the use of LLMs to generate stronger MILP
formulations via cutting planes [66], reformulations [16], or better solver configuration [34]. However, these approaches
rely on instance-level validation. We demonstrate examples where this limitation leads to invalid cutting planes and
reformulations.
Automatic Reformulation Checking Methods. Determining whether one formulation is a reformulation of another is
central to evaluating LLM-generated MILP formulations. Existing approaches largely operate at the instance level.
Canonical accuracy checks for a direct mapping between declarations (i.e., constraints and objectives) [49], while
execution accuracy compares optimal objective values after solving both formulations [1, 25, 37]. More recently,
EquivaMap [68] used LLMs to infer variable mappings between formulations and validate them by mapping optimal
solutions on a specific instance. Structural approaches represent MILPs as bipartite graphs and measure similarity
via graph isomorphism or edit distance [54, 59, 60, 65], avoiding the need to solve the optimization problem directly.
Unlike existing approaches, FLARE verifies reformulations at the formulation-level by producing machine-checkable
certificates that hold across all problem instances.
Autoformalization and Automated Theorem Proving. Autoformalization translates natural language into formal
representations [20, 27, 40, 58, 62], while automated theorem proving (ATP) generates machine-checkable proofs for
formal statements [5, 10, 26, 39, 42, 50, 51, 57]. Recent advances in LLMs have significantly improved both tasks,
with agentic frameworks combining (fine-tuned) language models and proof assistants (e.g., Lean) to formalize and
solve complex mathematical problems. Most recently, simple agentic harnesses have been shown to be competitive ATP
methods [42, 51]. We adopt an LLM-based agent as the ATP method in FLARE and introduce a constructive definition
of reformulation to make proving reformulations tractable.

3       Formalizing Formulations
We begin by formally defining a MILP formulation. In particular, we distinguish between a formulation and the
parameter (or data) values that specify a particular instance of the problem [18]. Take the traveling salesman problem
(TSP) as an example. A TSP formulation is defined on an abstract set of cities. A TSP instance is one such set of cities.
Instantiating the formulation with an instance yields a concrete MILP to be solved.
Definition 3.1. A MILP formulation M is a tuple M = (P, F , f0 ) with parameter space P, feasible region F(p) ⊆
Rn(p) , and objective function f0 . For instance p ∈ P, the feasible region F(p) is defined by m(p) linear constraints,
fi (·; p) : Rn(p) → R for all i ∈ [m(p)]. The first k(p) ≤ n(p) variables are integers. The feasible region is
                           F(p) = {x ∈ Zk(p) × Rn(p)−k(p) | fi (x; p) ≤ 0 ∀i ∈ [m(p)]}.
When the instance p is clear from context, we use n, m, and k instead of the parameterized forms. The objective is
to minimize1 the linear function f0 (·; p) : Rn(p) → R. A formulation M is instantiated with an instance p ∈ P. We
denote an instantiated formulation as M(p) = (F (p), f0 (p)).
    1
        We write all formulations as minimization problems; maximization objectives can be converted by negating the objective.


                                                                  3
                                  FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



Running Example. The traveling salesman problem (TSP) aims to find the shortest tour in a graph that visits every
node exactly once. A TSP instance is a weighted fully-connected graph G = (V, E, w) on n = |V | ≥ 2 nodes with
edge weights wij . We write PTSP for the set of all such graphs. Two common MILP formulations for the TSP are the
Dantzig-Fulkerson-Johnson (DFJ) [12] and Miller-Tucker-Zemlin (MTZ) [44] formulations:
               X                                                                     X
    min                wij xij                                             min               wij xij
             (i,j)∈E                                                               (i,j)∈E
               X                                                                     X
      s.t.              xij = 1        ∀i ∈ V                               s.t.              xij = 1        ∀i ∈ V
             j∈V \{i}                                                              j∈V \{i}
               X
                        xij = 1        ∀j ∈ V                  (DFJ)                 X
                                                                                              xij = 1        ∀j ∈ V                    (MTZ)
             i∈V \{j}                                                              i∈V \{j}
             XX
                       xij ≤ |S| − 1   ∀S ⊂ V, 2 ≤ |S| ≤ n−1                       ui − uj + n xij ≤ n − 1   ∀i, j ∈ V \ {1}, i ̸= j
             i∈S j∈S                                                               u1 = 1
             xij ∈ {0, 1}              ∀(i, j) ∈ E                                 2 ≤ ui ≤ n                ∀i ∈ V \ {1}
                                                                                   xij ∈ {0, 1}              ∀(i, j) ∈ E

Both formulations define decision variables xij ∈ {0, 1} to indicate if the edge (i, j) is used in the tour. To prevent
subtours, (DFJ) uses an exponential family of subtour-elimination constraints, while (MTZ) uses a polynomial family
of constraints with auxiliary position variables ui ∈ R for each node. We denote these formulations as MDFJ and
MMTZ , respectively. Both formulations faithfully represent the TSP, but have notable differences that affect solve times.
MDFJ is a stronger formulation than MMTZ in that it admits fewer fractional solutions in the linear relaxation. Despite
the exponential size of MDFJ , it can be solved efficiently with constraint generation.
With this formal definition established, we now consider multiple notions of MILP reformulation and introduce a
constructive definition amenable to formalization and ATP.

4       Formalizing Reformulations
Until now, we have used the term reformulation informally. It has an intuitive operational meaning: M′ is a reformula-
tion of M if one can map an instance M(p) to an instance M′ (p′ ), solve M′ (p′ ), and efficiently recover an optimal
solution to M(p). Importantly, this is a formulation-level claim: the construction must work for all problem instances
p ∈ P.
In Section 4.1, we review an existing notion of reformulation capturing this intuition and discuss why this definition
is difficult to verify computationally. This limitation has led to proxies for reformulation that are easier to check
computationally but lack formulation-level guarantees (Section 4.2). Our key idea is to utilize tools from formal
verification to make formulation-level claims machine-checkable. To this end, we propose a constructive definition of
reformulation that is amenable to formalization and tractable for ATP (Section 4.3).

4.1          Existing Definition

Audet et al. [4] capture our intuitive notion of reformulation with a complexity-theoretic definition inspired by
polynomial-time Turing reductions [21].
Definition 4.1 (Audet Reformulation [4]). Let M and M′ be two formulations with parameter spaces P and P ′ . M′
is an Audet reformulation of M if there exists a mapping Φp : P → P ′ such that, for any instance p ∈ P: if M(p) has
an optimal solution, then M′ (Φp (p)) also has an optimal solution, and every optimal solution to M′ (Φp (p)) can be
mapped back to an optimal solution of M(p) in polynomial time.
Remark 4.2. To avoid trivial or vacuous cases, we focus on settings in which solving each formulation is NP-hard and
each formulation has at least one feasible instance. The polynomial-time restriction on the optimal-solution mapping
excludes trivial mappings that solve M(p) directly.
TSP Example. The formulation MMTZ is an Audet reformulation of MDFJ . The mapping Φp is the identity as both
formulations use the same parameter space PTSP . Given any optimal solution of MMTZ (Φp (p)), we can obtain an
optimal solution to MDFJ (p) by mapping xij to itself and dropping the position variables ui , a linear time operation.
This definition captures a formulation-level notion of reformulation as desired. However, it is difficult to verify
computationally since it quantifies over all instances p ∈ P. Furthermore, ATP must identify a mapping that sends
every optimal solution of M′ (Φp (p)) to an optimal solution of M(p). Our constructive definition of reformulation in
Section 4.3 is designed to lighten the demands on ATP.


                                                                       4
                            FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



4.2        Proxy Definitions and Limitations

Because formulation-level verification is difficult, existing methods use instance-level proxies. For a fixed pair of
instances, a proxy checks whether M′ (p′ ) is a reformulation of M(p). The simplest proxy solves M(p) and M′ (p′ ) and
compares the optimal objective values [1, 25, 37]. Zhai et al. [68] propose a stronger proxy, Quasi-Karp equivalence1 ,
inspired by Karp reductions [30] in complexity theory.
Definition 4.3 (Quasi-Karp Equivalence [68]). Let M(p) and M′ (p′ ) be two instantiated formulations. We say M′ (p′ )
is Quasi-Karp equivalent to M(p) if there exists an algorithm A(M(p), M′ (p′ )) that produces a mapping f such that:
   • If x∗ is an optimal solution to M′ (p′ ), then f (x∗ ) is an optimal solution to M(p),
   • f can be computed in polynomial time, and
   • A(M(p), M′ (p′ )) runs in polynomial time for all p ∈ P and p′ ∈ P ′ .

Quasi-Karp equivalence is an instance-level analogue of Audet reformulation. Zhai et al. [68] implement this idea in
EquivaMap, where an LLM proposes a mapping f , which is then validated on the particular solved instance. This
mapping-based view is more expressive than comparing the objective values alone, allowing EquivaMap to handle some
objective transformations and solution mappings on a fixed instance. However, it still does not certify at the formulation
level (across all instances), and its effectiveness depends on the class of candidate mappings 2 for f and the LLM’s
ability to find the map.
Pitfalls of Instance-Level Verification. The distinction between instance- and formulation-level verification is critical
in automated optimization modeling. A generated formulation is meant to be reused on unseen problem data. An
instance-level check can validate a reformulation that is invalid at the formulation level, resulting in errors on unseen
instances. For example, EvoCut [66] uses LLMs to propose cutting planes (cuts) for MILP formulations (Appendix
F.1). A valid cut for formulation M may remove feasible points in the linear relaxation of M while retaining all
integer-feasible points. The EvoCut method validates candidate cuts with a simple execution-based proxy. As such, the
proposed cuts may be invalid on unseen instances. The proposed cut (v1-EC3) illustrates this risk (Proposition F.1).
This cut eliminates triangles involving the first node. This is acceptable for an instance with n > 3 nodes. However,
consider the 3-node instance depicted in Figure 2a with feasible tour 1 → 2 → 3 → 1. The only feasible tour is
eliminated by the cut.

                    A           1
                                                  B



                        2                   3


                            1       2   3


                            0       1   0

                            0       0   1

                            1       0   0



Figure 2: (a) A feasible tour 1 → 2 → 3 → 1 on a 3-node TSP instance with the MTZ variables xij and ui . (b) A graphical
depiction of the reformulation construction Φ(M, M′ ). The parameter mapping Φp yields a pair of feasible regions F (p) and
F ′ (p′ ) related by the forward and backward maps such that objective ordering is preserved.


4.3        Constructive Definition

To overcome the limitations of instance-level reformulation proxies, we use formal verification to machine-check
reformulations at the formulation level. Audet reformulation can be formalized and machine-checked, but it requires
      1
          Note that this definition is directional despite the equivalence terminology.
      2
          To ensure f is computable in polynomial time, EquivaMap restricts f to be linear.


                                                                    5
                       FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



ATP to identify a mapping that sends every optimal solution of M′ (Φp (p)) to an optimal solution of M(p). To
ease the burden on ATP, we propose a stronger, constructive definition of reformulation that requires explicit forward
and backward mappings between feasible regions that preserve objective ordering, together with a strictly increasing
objective map (see Figure 2b). These conditions satisfy the Audet reformulation (Proposition 4.6) but do not require
ATP to certify the optimality of solutions in the image of the solution mapping.
Definition 4.4 (Constructive Reformulation). Let M = (P, F , f0 ) and M′ = (P ′ , F ′ , f0′ ) be formulations. A
reformulation construction from M to M′ is a tuple Φ(M, M′ ) = (Φp , Φfwd , Φbwd , Φobj ) consisting of:
    • a parameter mapping Φp : P → P ′ ,
                                                      ′
    • a forward mapping Φfwd (·; p) : Rn(p) → Rn (Φp (p)) ,
                                              ′
    • a backward mapping Φbwd (·; p) : Rn (Φp (p)) → Rn(p) computable in polynomial time, 1 and
    • an objective mapping Φobj : R → R.
M′ is a constructive reformulation of M if there exists a reformulation construction satisfying the following conditions
for every instance p ∈ P, with p′ = Φp (p):
    • Forward feasibility. For all x ∈ F (p): Φfwd (x; p) ∈ F ′ (p′ ).
    • Backward feasibility. For all x′ ∈ F ′ (p′ ): Φbwd (x′ ; p) ∈ F(p).
    • Strictly monotone objective mapping. Φobj is strictly monotonically increasing.
    • Objective preservation. (1) For all x ∈ F(p), f0′ (Φfwd (x; p); p′ ) = Φobj (f0 (x; p)), and (2) for all x′ ∈ F ′ (p′ ),
      f0′ (x′ ; p′ ) = Φobj (f0 (Φbwd (x′ ; p); p)).
We say M′ (p′ ) is a constructive reformulation of M(p) if the conditions hold for p ∈ P and p′ ∈ P ′ .
Remark 4.5. Like Audet reformulation, we use this definition for settings in which solving each formulation is NP-hard
and each formulation has at least one feasible instance.
This definition is designed to capture common MILP transformations (e.g., lifting, rescaling, and substitution) and
modeling choices (e.g., exponential constraints like the TSP (DFJ) formulation). A related definition by Sherali
requires a much stronger order-preserving bijective mapping between the two feasible regions that excludes common
transformations (e.g., lifting) [38].
We next relate constructive reformulation to the two notions above. We prove that a constructive reformulation is
an Audet reformulation and, as an immediate corollary at the instance level, constructive reformulation also implies
Quasi-Karp equivalence. We defer the proof to Appendix A.
Proposition 4.6. Let M and M′ be formulations. If M′ is a constructive reformulation of M, then M′ is an Audet
reformulation of M. Furthermore, for any instance p ∈ P with p′ = Φp (p), if M′ (p′ ) is a constructive reformulation
of M(p), then M′ (p′ ) is Quasi-Karp equivalent to M(p).

Our definition is stronger than Audet’s because it requires mappings for all feasible points, not only optima. This
stronger notion of reformulation provides a more structured claim that reduces the proof burden on ATP while remaining
satisfied by common MILP transformations. For the remainder of the paper, we use reformulation to mean constructive
reformulation.

5    Methodology
This section operationalizes our reformulation definition into an automated verification pipeline. We first formalize our
definition in Lean and then introduce FLARE, which uses ATP to generate machine-checkable certificates. Finally, we
introduce FLARE-NL, a fast and cheap LLM proxy that reasons about reformulations using only natural language rather
than Lean.
Formalization. Our reformulation definition is a formulation-level claim quantified over every instance p ∈ P. To
make it machine-checkable, we encode the claim in Lean, which reasons symbolically over arbitrary instances rather
than testing concrete data. We formalize our definition in Lean [13], chosen for its mature Mathlib library and extensive
ATP tooling (see Appendix C). We provide Lean formalizations of formulation (Definition 3.1) and reformulation
(Definition 4.4) in Appendix B. We assume the input formulations are well-formed MILPs (i.e., have linear constraints
    1
      Polynomial time is measured under fixed binary encodings of parameters and rational/integer assignments: Φbwd is polynomial-
time computable if a single deterministic algorithm, given p, Φp (p), and x′ , outputs Φbwd (x′ ; p) in time polynomial in the total
input bit length. Supplying Φp (p) as input means this condition does not impose a polynomial-time requirement on Φp .


                                                                 6
                        FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



and objective, and are defined over real-valued decision variables). Accordingly, our Lean formalization does not
explicitly encode these conditions. The only part of Definition 4.4 we omit from the Lean proof obligation is the
polynomial-time requirement on Φbwd . Formalizing computational complexity in Lean would add substantial proof
burden, and in our experiments, the backward map in each construction was always computable in polynomial time.
FLARE. FLARE determines if M′ is a reformulation of M under a fixed parameter mapping Φp in the following stages:
(1) autoformalize M, M′ , and Φp into Lean, (2) attempt to prove M′ is a reformulation of M under Φp using ATP,
and (3) check if a reformulation certificate was successfully generated by ATP. In the first two stages, we utilize the
Claude Code1 agent harness for autoformalization and ATP. Existing ATP methods, like the Numina-Lean-Agent [42],
demonstrate the use of Claude Code as a competitive ATP method when combined with the Lean-LSP-MCP [7, 29, 42].
We further augment Claude Code with custom agent skills for handling MILP formulations in Lean. In the final stage,
we check if a proof was generated and ensure it compiles without using sorry2 and without introducing new axioms.
This workflow is summarized in Figure 1 and additional implementation details can be found in Appendix C.
Limitations. FLARE’s guarantee is conditional on faithful formalization. If the formulations and parameter mapping
are formalized correctly, then a Lean-verified certificate proves the reformulation claim under our definition. However,
failure to generate a certificate is inconclusive. We highlight three limitations.
• No certificate of invalidity. If M′ is not a reformulation of M under Φp , FLARE does not prove invalidity; the
  ATP component simply refuses to certify validity of the reformulation. Moreover, invalidity is scoped to the fixed
  mapping: it is not evidence that no parameter mapping makes M′ a reformulation of M.
• Dependence on faithful formalization. If the formalizations are unfaithful to M, M′ , or Φp , FLARE may certify
  a statement that differs from the intended claim. We conduct a human audit of our dataset (Section 6.1) and an
  LLM-as-a-judge audit of every formalization produced during our main FLARE experiment. A selection of FLARE
  formalizations were human-reviewed to check the correctness of the LLM judge. Both audits observe no instance
  of this failure mode. Furthermore, this concern can be eliminated by deterministically translating from a modeling
  standard such as AMPL [18] or MathOptInterface [35] to Lean.
• False negatives from theorem proving. If the LLM is unable to identify an appropriate reformulation construction
  or the proof requires extensive work in Lean to formalize, the agent may exit early, producing a false negative.
  Ongoing efforts to formalize computer science foundations in Lean with CSLib may reduce this burden on ATP.
FLARE-NL. Generating a reformulation certificate using FLARE can take 5-10 minutes. As a fast and cheap proxy,
FLARE-NL prompts a frontier reasoning model with templated LATEX descriptions of two formulations, M and M′ ,
along with the parameter mapping Φp , and asks if M′ is a reformulation of M under Φp (see Appendix D for full
prompt). FLARE-NL differs from the naive-LLM baseline of Zhai et al. [68] in three ways: (1) the prompt includes our
definition of reformulation, (2) the prompt explicitly states all formulation assumptions and instructs not to introduce
new ones, and (3) we utilize reasoning and structured output. Unlike FLARE, FLARE-NL lacks any verifiable guarantees
on its output. It can serve as a screening heuristic before FLARE, but it is not a proof method.

6         Experiments
To evaluate if formulation-level verification catches failures missed by instance-level proxies, we introduce Formulation-
Bench, an extension of the EquivaFormulation dataset [68] containing more challenging formulation-level cases. We
evaluate FLARE and FLARE-NL against established baselines and conduct an ablation study on FLARE-NL.3 Additional
experimental details are provided in Appendix G.

6.1       FormulationBench

We introduce FormulationBench, a benchmark designed to test formulation-level reformulation reasoning. Formula-
tionBench extends EquivaFormulation [68] with candidate cuts proposed by EvoCut [66] and a collection of eight
MILP formulation pairs from Ferchtandiker et al. [16]. These formulation pairs are more challenging than those in
EquivaFormulation, requiring reasoning about general cutting plane families and meaningfully different modeling
techniques. The dataset contains 20 problems, 109 formulations, and 89 formulation pairs with 63 positive and 26
negative examples (Appendix E). Following Remark 4.5, we restrict our evaluation to the subset of 16 NP-hard problems
containing 54 formulation pairs. FormulationBench is available via the formulation-bench Python package.4
      1
        Alternative agent harnesses are considered in Appendix H.
      2
        The sorry tactic can be used in Lean proofs to skip a proof obligation. Any proof relying on sorry is hence incomplete.
      3
        All experimental code is available at https://github.com/henryrobbins/flare.
      4
        Documentation is available at https://formulation-bench.henryrobbins.com


                                                                  7
                        FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



FormulationBench is organized similarly to the NLP4LP dataset [1]; JSON files contain formulation descriptions and
problem instance data. Relative to NLP4LP, FormulationBench introduces two notable extensions. First, we explicitly
record implicit assumptions necessary to prove reformulation validity. We flag assumptions implicit in the source
dataset to facilitate our ablation study in Section 6.3. Second, we formalize each formulation in Lean (see Appendix B)
and include ground-truth reformulation certificates for each valid reformulation pair. The nine TSP formulations were
formalized by hand and used as reference examples when autoformalizing the remainder with Claude Code. All 109
Lean formalizations were then reviewed line-by-line by a PhD student specializing in operations research, who found
no autoformalization errors. While preparing this dataset, we verified prior AI-generated MILP reformulations and
found 5 invalid cutting planes proposed by EvoCut [66] and 4 invalid reformulations proposed in Ferchtandiker et al.
[16] (see Appendix F).

6.2   Baseline Comparison

We compare FLARE and FLARE-NL against the baselines evaluated by Zhai et al. [68]. We exclude graph-related methods
due to their poor performance on non-trivial transformations [68]. To ensure comparability, every LLM-based method
receives the same list of all explicit and implicit assumptions from the problem statement.
   • Execution [1]. Solves both formulations on a fixed problem instance and compares their optimal objective values.
   • EquivaMap [68]. We re-implement EquivaMap to allow for mappings over non-scalar variables. The original
     mapping prompt is unmodified. We use Opus 5 as the mapping LLM.
Performance. Table 1 summarizes performance on the 54-pair NP-hard subset of FormulationBench. Our methods
outperform both existing baselines. FLARE achieves 100% accuracy and is the only method that generates machine-
checkable reformulation certificates. FLARE-NL also achieves 100% accuracy. Although it produces no certificate,
FLARE-NL is 30x faster and 25x cheaper than FLARE. Both execution and EquivaMap’s errors reflect limitations of
instance-level validation; see Table 2 for a systematic breakdown.

Table 1: Accuracy of automated reformulation checking methods on the FormulationBench dataset. Bold indicates the best method
on a metric and underlined indicates the second best. Metric cells report mean ± std. dev. across 3 runs; TP/FP/TN/FN reports totals.
All LLM-based methods use Opus 5 with reasoning and medium effort level. Due to the high cost, we only do a single run of FLARE.
FLARE and FLARE-NL outperform existing methods and FLARE is the only method that generates a machine-checkable certificate.
†
  79.7% of FLARE’s wall time is LLM inference; the remaining 20.3% is file IO and querying the Lean LSP.
      Method         Model Certificate Runs   TP    FP   TN   FN        Precision         Recall       Accuracy   Avg. Time    Avg. Cost
      Execution [1]  —         ✗        3     120   21   15    6    85.1%±0.0%       95.2%±0.0%     83.3%±0.0%          2.1s         —
      EquivaMap [68] Opus 5    ✗        3     111   15   21   15    88.1%±0.0%       88.1%±0.0%     81.5%±0.0%          6.1s     $0.026
                                                                                                                    †
      FLARE          Opus 5    ✓        1      42    0   12    0         100.0%           100.0%         100.0%       410.6s     $1.180
      FLARE-NL       Opus 5    ✗        3     126    0   36    0   100.0%±0.0%      100.0%±0.0%    100.0%±0.0%         13.9s     $0.048


Failure Modes of Instance-Level Validation. Table 2 summarizes errors by transformation type. Existing instance-
level methods fail to catch formulation-level modeling errors, such as transformations (1) and (2), where a transformation
can appear valid on the tested instance while failing as a general reformulation. EquivaMap’s solution-mapping approach
handles transformations (3) and (4), showing its advantage over the execution heuristic, but fails on category (5), where
valid reformulations require nonlinear solution mappings. In contrast, FLARE’s formulation-level guarantees eliminate
these false positives.
Limits of ATP. For a valid pair of formulations, failure to produce a Lean proof results in a false negative. We do not
observe this failure mode in our main experiments with Opus 5. However, we run additional experiments with GPT 5.6
Sol and DeepSeek V4 Pro (see Table 6). Both models produce false negatives attributed to ATP failure. The limits of
ATP are especially prominent in DeepSeek with 79.6% accuracy. Although Opus 5 achieves 100% accuracy, the cost
scales with the proof difficulty due to ATP. The cost standard deviation is $1.22 and the max is $8.02. Many problems
rely on standard combinatorial results that are unavailable in Lean’s standard libraries (e.g., flow decomposition). As
Lean libraries improve (e.g., CSLib), FLARE can reduce cost by simply invoking such results rather than reproving them.

6.3 FLARE-NL Ablation Study

In Table 3, we evaluate ablations of the FLARE-NL prompt to measure the importance of the reformulation definition
and assumption handling across three LLMs. The Baseline uses the full prompt; No Definition omits the definition of
reformulation; and Allow Implicit removes implicit assumptions from the prompt and permits the model to introduce
reasonable assumptions. See Appendix D for prompt variants and Appendix G for additional details.


                                                                    8
                          FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving




Table 2: Accuracy of automated reformulation checking methods segmented by challenging transformation types in the Formulation-
Bench dataset. The Valid column indicates if the listed transformation results in a valid reformulation. The Pairs column gives the
number of formulation pairs in each category. Worst Case reports the minimum accuracy over the transformation categories listed
above. FLARE and FLARE-NL are the only methods with 100% accuracy in the worst case.
               Transformation                                  Valid    Pairs       Execution [1]    EquivaMap [68]          FLARE      FLARE-NL

               1. Base-10 Representation                        ✗           2           0%                    0%             100%            100%
               2. Addition of Invalid Cutting Planes            ✗           3           0%                    0%             100%            100%
               3. Rescaled Objective                            ✓           2           0%                   100%            100%            100%
               4. Different Formulation (Same Objective)        ✗           2           0%                   100%            100%            100%
               5. Non-Linear Solution Maps                      ✓           5          100%                   0%             100%            100%
               Worst Case                                                               0%                   0%              100%            100%




Explicit Definitions and Assumptions. The full FLARE-NL prompt performs the best across all model families,
indicating that reformulation verification relies on explicit definitions and assumptions. Removing the reformulation
definition consistently reduces accuracy, and allowing the model to reason about implicit assumptions causes the largest
degradation for every model family. Verifying reformulations requires explicit criteria and assumptions, rather than
model-inferred assumptions.
Frontier Model Reasoning. FLARE-NL is most effective when paired with strong frontier reasoning models (also see
Appendix H). Under the full prompt, Opus 5, GPT-5.6 Sol, and DeepSeek V4 Pro all achieve high accuracy, with
Opus 5 correct on every pair of every run.

Table 3: Ablation study of FLARE-NL across LLM model and prompt variations. No Definition omits the reformulation definition
from the prompt and Allow Implicit removes implicit assumptions from the prompt and permits the model to introduce reasonable
assumptions. Metric cells report mean ± std. dev. across 3 runs; TP/FP/TN/FN reports totals. All models have reasoning enabled
and the reasoning effort level is shown following the model name.
            Model (Effort)      Variant          TP    FP      TN      FN       Precision           Recall        Accuracy    Avg Time        Avg Cost
                                Baseline         126       0    36      0   100.0±0.0%       100.0±0.0%       100.0±0.0%             13.9s      $0.048
            Opus 5
                                No Definition    120       0    36      6   100.0±0.0%        95.2±0.0%        96.3±0.0%             12.0s      $0.039
            (medium)
                                Allow Implicit   121       6    30      5    95.3±0.1%        96.0±1.4%        93.2±1.1%             18.4s      $0.052
                                Baseline         120       0    36      6   100.0±0.0%        95.2±0.0%        96.3±0.0%             14.6s      $0.034
            GPT-5.6 Sol
                                No Definition    120       0    36      6   100.0±0.0%        95.2±0.0%        96.3±0.0%             12.3s      $0.027
            (medium)
                                Allow Implicit    93       6    30     33    93.9±0.0%        73.8±0.0%        75.9±0.0%             20.7s      $0.040
                                Baseline         118       0    36      8   100.0±0.0%        93.7±1.4%        95.1±1.1%             60.1s      $0.005
            DeepSeek V4 Pro
                                No Definition    113       0    36     13   100.0±0.0%        89.7±1.4%        92.0±1.1%             56.9s      $0.004
            (high)
                                Allow Implicit   100       5    31     26    95.3±1.5%        79.4±3.6%        80.9±2.1%             71.2s      $0.005




7    Conclusion
LLMs are increasingly used for optimization modeling but lack formal guarantees, motivating methods to automatically
verify LLM-generated formulations. We develop FLARE, the first automated approach for producing machine-checkable
reformulation certificates. FLARE combines a constructive definition of reformulation and ATP to verify reformulation
claims at the formulation level, while existing methods only operate at the instance level. Furthermore, we introduce
FLARE-NL, an LLM proxy that trades formal guarantees for improved speed and cost. Both methods outperform existing
baselines and achieve 100% accuracy on the NP-hard subset of FormulationBench.
Limitations and Future Work. Several limitations motivate future work on formally verified AI-driven optimization
modeling.
    • Deterministic formalization. The FLARE reformulation certificate requires faithful formalization. Deterministi-
      cally translating accepted MILP modeling standards into Lean eliminates formalization as a source of error.
    • Certificates of invalidity. FLARE currently searches only for certificates of validity. Future work could develop
      methods for proving that no reformulation construction exists under a fixed parameter map. For current ATP
      systems, proving this type of non-existence guarantee will likely be substantially more difficult than proving
      existence by exhibiting an explicit construction.
    • Alternative formulation relations. Our constructive definition requires forward and backward maps over the
      entire feasible region. Thus, it may reject a reformulation that removes non-optimal feasible points while preserving
      the optimal feasible points. Future work could formalize weaker, optimality-preserving notions of reformulation.


                                                                                9
                      FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



     It could also formalize formulation strength as a well-defined relation (e.g., by proving containment between the
     projected linear relaxations of two formulations).
   • Real-world formulations. The formulations of FormulationBench are drawn from academic benchmarks. Future
     work should extend FormulationBench to demonstrate that FLARE and ATP can scale to larger, more complex
     industrial MILP formulations.
   • Verification for automated modeling. Our results raise questions about how to integrate verification into
     LLM-driven modeling and automated algorithm design pipelines (e.g., EvoCut [66]). A natural design is to use
     FLARE-NL for rapid screening and FLARE for final certification.


Acknowledgements
We thank the anonymous referees for thoughtful feedback that significantly improved the clarity of the paper. We
also thank Nichie Supatgiat for her contributions to FormulationBench and helpful discussions. We thank Refine.ink
for detailed manuscript feedback. MU gratefully acknowledges support from the Office of Naval Research under
award N000142412306, Air Force Office of Scientific Research under award FA9550-26-1-0012, the Alfred P. Sloan
Foundation, the Stanford Institute for Human-Centered Artificial Intelligence (HAI), and from IBM Research as a
founding member of Stanford Institute for Human-centered Artificial Intelligence. EV gratefully acknowledges support
from the National Science Foundation under award CCF-2338226 and the AI2050 program at Schmidt Sciences. Any
opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not
necessarily reflect the views of these funders.

References
 [1] Ali AhmadiTeshnizi, Wenzhi Gao, and Madeleine Udell. OptiMUS: Scalable optimization modeling with (MI)LP solvers and
     large language models. In Proceedings of the 41st International Conference on Machine Learning, ICML’24. JMLR.org, 2024.
 [2] Ali AhmadiTeshnizi, Wenzhi Gao, Herman Brunborg, Shayan Talaei, Connor Lawless, and Madeleine Udell. OptiMUS-0.3:
     Using Large Language Models to Model and Solve Optimization Problems at Scale. arXiv preprint arXiv:2407.19633, 2025.
 [3] Nicolas Astorg, Tennison Liu, Yuanzhang Xiao, and Mihaela van der Schaar. Autoformulation of mathematical optimization
     models using LLMs. Proceedings of Machine Learning Research, 2025.
 [4] C. Audet, P. Hansen, B. Jaumard, and G. Savard. Links Between Linear Bilevel and Mixed 0–1 Programming Problems. Journal
     of Optimization Theory and Applications, 93(2):273–300, May 1997. ISSN 1573-2878. doi: 10.1023/A:1022645805569.
 [5] Axiom. From Seeing Why to Checking Everything, 2026.
 [6] Egon Balas. Disjunctive programming. Annals of discrete mathematics, 5:3–51, 1979.
 [7] Benjamin Breen, Marco Del Tredici, Jacob McCarran, Javier Aspuru Mijares, Weichen Winston Yin, Kfir Sulimany, Jacob M.
     Taylor, Frank H. L. Koppens, and Dirk Englund. Ax-Prover: A Deep Reasoning Agentic Framework for Theorem Proving in
     Mathematics and Quantum Physics. arXiv preprint arXiv:2510.12787, 2025.
 [8] Hao Chen, Gonzalo E Constante-Flores, and Can Li. Diagnosing infeasible optimization problems using large language models.
     INFOR: Information Systems and Operational Research, 62(4):573–587, 2024.
 [9] Hao Chen, Gonzalo Esteban Constante-Flores, Krishna Sri Ipsit Mantri, Sai Madhukiran Kompalli, Akshdeep Singh Ahluwalia,
     and Can Li. OptiChat: Bridging optimization models and practitioners with large language models. INFORMS Journal on
     Data Science, 2025.
[10] Jiangjie Chen, Wenxiang Chen, Jiacheng Du, Jinyi Hu, Zhicheng Jiang, Allan Jie, Xiaoran Jin, Xing Jin, Chenggang Li, Wenlei
     Shi, Zhihong Wang, Mingxuan Wang, Chenrui Wei, Shufa Wei, Huajian Xin, Fan Yang, Weihao Gao, Zheng Yuan, Tianyang
     Zhan, Zeyu Zheng, Tianxi Zhou, and Thomas Hanwen Zhu. Seed-Prover 1.5: Mastering Undergraduate-Level Theorem
     Proving via Learning from Experience. arXiv preprint arXiv:2512.17260, 2025.
[11] Michele Conforti, Gérard Cornuéjols, and Giacomo Zambelli. Integer programming models. In Integer Programming, pages
     45–84. Springer, 2014.
[12] G. Dantzig, R. Fulkerson, and S. Johnson. Solution of a Large-Scale Traveling-Salesman Problem. Journal of the Operations
     Research Society of America, 2(4):393–410, 1954. ISSN 0096-3984.
[13] Leonardo de Moura and Sebastian Ullrich. The Lean 4 Theorem Prover and Programming Language. In André Platzer and
     Geoff Sutcliffe, editors, Automated Deduction – CADE 28, pages 625–635, Cham, 2021. Springer International Publishing.
     ISBN 978-3-030-79876-5. doi: 10.1007/978-3-030-79876-5_37.
[14] Oliver Dressler. Lean LSP MCP: Tools for agentic interaction with the lean theorem prover, March 2025.
[15] Joshua Drossman, Alexandre Jacquillat, and Sébastien Martin. Let’s have a conversation: Designing and evaluating LLM
     agents for interactive optimization. arXiv preprint arXiv:2604.02666, 2026.


                                                              10
                       FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



[16] Nathan Ferchtandiker, Dick den Hertog, Madeleine Udell, and Segev Wasserkrug. Finding efficient MILO
     formulations with LLMs.      Working paper, 2025.      URL https://github.com/nathan-ferchtandiker/
     LLMs-For-Optimization-Reformulations.
[17] Christodoulos A. Floudas and Xiaoxia Lin. Mixed Integer Linear Programming in Process Scheduling: Modeling, Algorithms,
     and Applications. Annals of Operations Research, 139(1):131–162, October 2005. ISSN 1572-9338. doi: 10.1007/
     s10479-005-3446-x.
[18] Robert Fourer, David M. Gay, and Brian W. Kernighan. AMPL: A Modeling Language for Mathematical Programming.
     Thomson/Brooks/Cole, Pacific Grove, CA, 2nd ed edition, 2003. ISBN 978-0-534-38809-6.
[19] Cameron Freer. Lean 4 Skills: Theorem proving skill and workflow pack for AI coding agents, October 2025.
[20] Guoxiong Gao, Yutong Wang, Jiedong Jiang, Qi Gao, Zihan Qin, Tianyi Xu, and Bin Dong. Herald: A natural language
     annotated Lean 4 dataset. In The Thirteenth International Conference on Learning Representations, 2025.
[21] Michael R. Garey and David S. Johnson. Computers and Intractability: A Guide to the Theory of NP-completeness. A
     Series of Books in the Mathematical Sciences. Freeman, New York [u.a], 27. print edition, 2009. ISBN 978-0-7167-1044-8
     978-0-7167-1045-5.
[22] Bogdan Georgiev, Javier Gómez-Serrano, Terence Tao, and Adam Zsolt Wagner. Mathematical exploration and discovery at
     scale. arXiv preprint arXiv:2511.02864, 2025.
[23] Pouya Hamadanian, Pantea Karimi, Arash Nasr-Esfahany, Kimia Noorbakhsh, Joseph Chandler, Ali ParandehGheibi, Moham-
     mad Alizadeh, and Hari Balakrishnan. Glia: A Human-Inspired AI for Automated Systems Design and Optimization. arXiv
     preprint arXiv:2510.27176, 2025.
[24] André Hottung, Federico Berto, Chuanbo Hua, Nayeli Gast Zepeda, Daniel Wetzel, Michael Römer, Haoran Ye, Davide Zago,
     Michael Poli, Stefano Massaroli, Jinkyoo Park, and Kevin Tierney. VRPAgent: LLM-Driven Discovery of Heuristic Operators
     for Vehicle Routing Problems. arXiv preprint arXiv:2510.07073, 2025.
[25] Chenyu Huang, Zhengyang Tang, Shixi Hu, Ruoqing Jiang, Xin Zheng, Dongdong Ge, Benyou Wang, and Zizhuo Wang.
     ORLM: A customizable framework in training large models for automated optimization modeling. Operations Research, 73(6):
     2986–3009, 2025.
[26] Logical Intelligence. Aleph Prover: State-of-the-Art Formal Theorem Prover, January 2026.
[27] Prithwish Jana, Kaan Kale, Ahmet Ege Tanriverdi, Cruise Song, Sriram Vishwanath, and Vijay Ganesh. ProofBridge: Auto-
     formalization of natural language proofs in lean via joint embeddings. In The Fourteenth International Conference on Learning
     Representations, 2026.
[28] Caigao JIANG, Xiang Shu, Hong Qian, Xingyu Lu, JUN ZHOU, Aimin Zhou, and Yang Yu. LLMOPT: Learning to define and
     solve general optimization problems from scratch. In The Thirteenth International Conference on Learning Representations,
     2025.
[29] Haocheng Ju, Guoxiong Gao, Jiedong Jiang, Bin Wu, Zeming Sun, Leheng Chen, Yutong Wang, Yuefeng Wang, Zichen Wang,
     Wanyi He, Peihao Wu, Liang Xiao, Ruochuan Liu, Bryan Dai, and Bin Dong. Automated Conjecture Resolution with Formal
     Verification. arXiv preprint arXiv:2604.03789, 2026.
[30] Richard M. Karp. Reducibility among Combinatorial Problems. In Raymond E. Miller, James W. Thatcher, and Jean D.
     Bohlinger, editors, Complexity of Computer Computations: Proceedings of a Symposium on the Complexity of Computer
     Computations, Held March 20–22, 1972, at the IBM Thomas J. Watson Research Center, Yorktown Heights, New York, and
     Sponsored by the Office of Naval Research, Mathematics Program, IBM World Trade Corporation, and the IBM Research
     Mathematical Sciences Department, pages 85–103. Springer US, Boston, MA, 1972. ISBN 978-1-4684-2001-2. doi:
     10.1007/978-1-4684-2001-2_9.
[31] Bernard Knueven, James Ostrowski, and Jean-Paul Watson. On Mixed-Integer Programming Formulations for the Unit
     Commitment Problem. INFORMS Journal on Computing, 32(4):857–876, October 2020. ISSN 1091-9856. doi: 10.1287/ijoc.
     2019.0944.
[32] Wen-Yang Ku and J. Christopher Beck. Mixed Integer Programming models for job shop scheduling: A computational analysis.
     Computers & Operations Research, 73:165–173, September 2016. ISSN 0305-0548. doi: 10.1016/j.cor.2016.04.006.
[33] Connor Lawless, Jakob Schoeffer, Lindy Le, Kael Rowan, Shilad Sen, Cristina St. Hill, Jina Suh, and Bahareh Sarrafzadeh. “I
     Want It That Way”: Enabling interactive decision support using large language models and constraint programming. ACM
     Transactions on Interactive Intelligent Systems, 14(3):1–33, 2024.
[34] Connor Lawless, Yingxi Li, Anders Wikum, Madeleine Udell, and Ellen Vitercik. LLMs for cold-start cutting plane separator
     configuration. In International Conference on the Integration of Constraint Programming, Artificial Intelligence, and Operations
     Research, pages 51–69. Springer, 2025.
[35] Benoît Legat, Oscar Dowson, Joaquim Dias Garcia, and Miles Lubin. MathOptInterface: A data structure for mathematical
     optimization problems. INFORMS Journal on Computing, 2021. doi: 10.1287/ijoc.2021.1067.
[36] Beibin Li, Konstantina Mellou, Bo Zhang, Jeevan Pathuri, and Ishai Menache. Large Language Models for Supply Chain
     Optimization. arXiv preprint arXiv:2307.03875, 2023.


                                                                11
                      FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



[37] Kuo Liang, Yuhang Lu, Jianming Mao, Shuyi Sun, Chunwei Yang, Congcong Zeng, Xiao Jin, Hanzhang Qin, Ruihao Zhu, and
     Chung-Piaw Teo. LLM for large-scale optimization model auto-formulation: A lightweight few-shot learning approach. arXiv
     preprint arXiv:2601.09635, 2026.
[38] Leo Liberti. Reformulations in Mathematical Programming: Definitions and Systematics. RAIRO - Operations Research, 43
     (1):55–85, January 2009. ISSN 0399-0559, 1290-3868. doi: 10.1051/ro/2009005.
[39] Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu, Hongzhou Lin, Kaiyu Yang, Jia LI, Mengzhou Xia, Danqi Chen, Sanjeev
     Arora, and Chi Jin. Goedel-Prover: A frontier model for open-source automated theorem proving. In Second Conference on
     Language Modeling, 2025.
[40] Fan Liu, Zhe-Rui Yang, Cancheng Liu, Tianrui SONG, Xiaofeng Gao, and Hao Liu. MM-Agent: LLM as agents for real-world
     mathematical modeling problem. In The Thirty-ninth Annual Conference on Neural Information Processing Systems, 2025.
[41] Fei Liu, Xialiang Tong, Mingxuan Yuan, Xi Lin, Fu Luo, Zhenkun Wang, Zhichao Lu, and Qingfu Zhang. Evolution of
     Heuristics: Towards efficient automatic algorithm design using large language model. In Proceedings of the 41st International
     Conference on Machine Learning, ICML’24. JMLR.org, 2024.
[42] Junqi Liu, Zihao Zhou, Zekai Zhu, Marco Dos Santos, Weikun He, Jiawei Liu, Ran Wang, Yunzhou Xie, Junqiao Zhao, Qiufeng
     Wang, Lihong Zhi, Jia Li, and Wenda Li. Numina-Lean-Agent: An Open and General Agentic Reasoning System for Formal
     Mathematics. arXiv preprint arXiv:2601.14027, 2026.
[43] Hugues Marchand, Alexander Martin, Robert Weismantel, and Laurence Wolsey. Cutting planes in integer and mixed
     integer programming. Discrete Applied Mathematics, 123(1):397–446, November 2002. ISSN 0166-218X. doi: 10.1016/
     S0166-218X(01)00348-1.
[44] C. E. Miller, A. W. Tucker, and R. A. Zemlin. Integer Programming Formulation of Traveling Salesman Problems. J. ACM, 7
     (4):326–329, October 1960. ISSN 0004-5411. doi: 10.1145/321043.321046.
[45] Hugo Morais, Péter Kádár, Pedro Faria, Zita A. Vale, and H. M. Khodr. Optimal scheduling of a renewable micro-grid in an
     isolated load area using mixed-integer linear programming. Renewable Energy, 35(1):151–156, January 2010. ISSN 0960-1481.
     doi: 10.1016/j.renene.2009.02.031.
[46] Mahdi Mostajabdaveh, Timothy T Yu, Rindranirina Ramamonjison, Giuseppe Carenini, Zirui Zhou, and Yong Zhang. Opti-
     mization modeling and verification from problem specifications using a multi-agent multi-stage LLM framework. INFOR:
     Information Systems and Operational Research, 62(4):599–617, 2024.
[47] Alexander Novikov, Ngân Vũ, Marvin Eisenberger, Emilien Dupont, Po-Sen Huang, Adam Zsolt Wagner, Sergey Shirobokov,
     Borislav Kozlovskii, Francisco J. R. Ruiz, Abbas Mehrabian, M. Pawan Kumar, Abigail See, Swarat Chaudhuri, George
     Holland, Alex Davies, Sebastian Nowozin, Pushmeet Kohli, and Matej Balog. AlphaEvolve: A coding agent for scientific and
     algorithmic discovery. arXiv preprint arXiv:2506.13131, 2025.
[48] Yves Pochet and Laurence A Wolsey. Production Planning by Mixed Integer Programming. Springer, 2006.
[49] Rindranirina Ramamonjison, Timothy Yu, Raymond Li, Haley Li, Giuseppe Carenini, Bissan Ghaddar, Shiqi He, Mahdi
     Mostajabdaveh, Amin Banitalebi-Dehkordi, Zirui Zhou, et al. NL4Opt competition: Formulating optimization problems based
     on their natural language descriptions. In NeurIPS 2022 Competition Track, pages 189–203. PMLR, 2023.
[50] Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin, Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe Fu, Qihao Zhu,
     Dejian Yang, Z. F. Wu, Zhibin Gou, Shirong Ma, Hongxuan Tang, Yuxuan Liu, Wenjun Gao, Daya Guo, and Chong Ruan.
     DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition.
     arXiv preprint arXiv:2504.21801, 2025.
[51] Borja Requena, Austin Letson, Krystian Nowakowski, Izan Beltran Ferreiro, and Leopoldo Sarra. A Minimal Agent for
     Automated Theorem Proving. arXiv preprint arXiv:2602.24273, 2026.
[52] Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog, M. Pawan Kumar, Emilien
     Dupont, Francisco J. R. Ruiz, Jordan S. Ellenberg, Pengming Wang, Omar Fawzi, Pushmeet Kohli, and Alhussein Fawzi.
     Mathematical discoveries from program search with large language models. Nature, 625(7995):468–475, January 2024. ISSN
     0028-0836, 1476-4687. doi: 10.1038/s41586-023-06924-6.
[53] K. Srinivasan, K.S. Chatha, and G. Konjevod. Linear-programming-based techniques for synthesis of network-on-chip
     architectures. IEEE Transactions on Very Large Scale Integration (VLSI) Systems, 14(4):407–420, April 2006. ISSN 1557-9999.
     doi: 10.1109/TVLSI.2006.871762.
[54] Zachary Steever, Kyle Hunt, Mark Karwan, Junsong Yuan, and Chase C Murray. A graph-based approach for relating integer
     programs. INFORMS Journal on Computing, 36(6):1715–1736, 2024.
[55] Tony J Van Roy and Laurence A Wolsey. Solving mixed integer programming problems using automatic reformulation.
     Operations Research, 35(1):45–57, 1987.
[56] François Vanderbeck and Laurence A. Wolsey. Reformulation and Decomposition of Integer Programs. In Michael Jünger,
     Thomas M. Liebling, Denis Naddef, George L. Nemhauser, William R. Pulleyblank, Gerhard Reinelt, Giovanni Rinaldi, and
     Laurence A. Wolsey, editors, 50 Years of Integer Programming 1958-2008, pages 431–502. Springer Berlin Heidelberg, Berlin,
     Heidelberg, 2010. ISBN 978-3-540-68274-5 978-3-540-68279-0. doi: 10.1007/978-3-540-68279-0_13.


                                                               12
                      FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



[57] Sumanth Varambally, Thomas Voice, Yanchao Sun, Zhifeng Chen, Rose Yu, and Ke Ye. Hilbert: Recursively building formal
     proofs with informal reasoning. In The Fourteenth International Conference on Learning Representations, 2026.
[58] Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas Baksys, Junqi Liu, Marco Dos Santos, Flood Sung, Marina Vinyes, Zhenzhe
     Ying, Zekai Zhu, Jianqiao Lu, Hugues de Saxcé, Bolton Bailey, Chendong Song, Chenjun Xiao, Dehao Zhang, Ebony Zhang,
     Frederick Pu, Han Zhu, Jiawei Liu, Jonas Bayer, Julien Michel, Longhui Yu, Léo Dreyfus-Schmidt, Lewis Tunstall, Luigi
     Pagani, Moreira Machado, Pauline Bourigault, Ran Wang, Stanislas Polu, Thibaut Barroyer, Wen-Ding Li, Yazhe Niu, Yann
     Fleureau, Yangyang Hu, Zhouliang Yu, Zihan Wang, Zhilin Yang, Zhengying Liu, and Jia Li. Kimina-Prover Preview: Towards
     Large Formal Reasoning Models with Reinforcement Learning. arXiv preprint arXiv:2504.11354, 2025.
[59] Zhuohan Wang, Ziwei Zhu, Yizhou Han, Yufeng Lin, Zhihang Lin, Ruoyu Sun, and Tian Ding. OptiBench: Benchmarking
     large language models in optimization modeling with equivalence-detection evaluation, 2024.
[60] Zhuohan Wang, Ziwei Zhu, Ziniu Li, Congliang Chen, Yizhou Han, Yufeng Lin, Zhihang Lin, Angyang Gu, Xinglin Hu, Ruoyu
     Sun, et al. ORGEval: Graph-theoretic evaluation of LLMs in optimization modeling. arXiv preprint arXiv:2510.27610, 2025.
[61] Laurence A Wolsey. Integer Programming. John Wiley & Sons, 2020.
[62] Yuhuai Wu, Albert Q. Jiang, Wenda Li, Markus N. Rabe, Charles Staats, Mateja Jamnik, and Christian Szegedy. Autoformal-
     ization with large language models. In Proceedings of the 36th International Conference on Neural Information Processing
     Systems, NIPS ’22, Red Hook, NY, USA, 2022. Curran Associates Inc. ISBN 9781713871088.
[63] Ziyang Xiao, Dongxiang Zhang, Yangjun Wu, Lilin Xu, Yuan Jessica Wang, Xiongwei Han, Xiaojin Fu, Tao Zhong, Jia Zeng,
     Mingli Song, and Gang Chen. Chain-of-Experts: When LLMs Meet Complex Operations Research Problems. In The Twelfth
     International Conference on Learning Representations, 2024.
[64] Zhuoliang Xie, Fei Liu, Zhenkun Wang, and Qingfu Zhang. Enhancing CVRP Solver through LLM-driven Automatic Heuristic
     Design. arXiv preprint arXiv:2602.23092, 2026.
[65] Linzi Xing, Xinglu Wang, Yuxi Feng, Zhenan Fan, Jing Xiong, Zhijiang Guo, Xiaojin Fu, Rindra Ramamonjison, Mahdi
     Mostajabdaveh, Xiongwei Han, Zirui Zhou, and Yong Zhang. Towards Human-aligned Evaluation for Linear Programming
     Word Problems. In Nicoletta Calzolari, Min-Yen Kan, Veronique Hoste, Alessandro Lenci, Sakriani Sakti, and Nianwen
     Xue, editors, Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and
     Evaluation (LREC-COLING 2024), pages 16550–16556, Torino, Italia, May 2024. ELRA and ICCL.
[66] Milad Yazdani, Mahdi Mostajabdaveh, Samin Aref, and Zirui Zhou. EvoCut: Strengthening Integer Programs via Evolution-
     Guided Language Models. arXiv preprint arXiv:2508.11850, 2025.
[67] Haoran Ye, Jiarui Wang, Zhiguang Cao, Federico Berto, Chuanbo Hua, Haeyeon Kim, Jinkyoo Park, and Guojie Song. ReEvo:
     Large language models as hyper-heuristics with reflective evolution. In The Thirty-eighth Annual Conference on Neural
     Information Processing Systems, 2024.
[68] Haotian Zhai, Connor Lawless, Ellen Vitercik, and Liu Leqi. EquivaMap: Leveraging LLMs for automatic equivalence
     checking of optimization formulations. In Forty-second International Conference on Machine Learning, 2025.




                                                             13
                      FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



A     Proof of Proposition 4.6
Proposition 4.6. Let M and M′ be formulations. If M′ is a constructive reformulation of M, then M′ is an Audet
reformulation of M. Furthermore, for any instance p ∈ P with p′ = Φp (p), if M′ (p′ ) is a constructive reformulation
of M(p), then M′ (p′ ) is Quasi-Karp equivalent to M(p).

Proof. Let M = (P, F , f0 ) and M′ = (P ′ , F ′ , f0′ ) be formulations. Assume M′ is a constructive reformulation
of M. By definition, there exists a reformulation construction Φ(M, M′ ) = (Φp , Φfwd , Φbwd , Φobj ) such that the
conditions of Definition 4.4 hold. Fix an instance p ∈ P and let p′ = Φp (p).
We first show that if M(p) has an optimal solution, then M′ (p′ ) also has an optimal solution. Let x∗ ∈ F(p) be
optimal for M(p). By forward feasibility, x′ = Φfwd (x∗ ; p) ∈ F ′ (p′ ). We now claim that x′ is optimal for M′ (p′ ).
Suppose this was not true. There must exist an x̂′ ∈ F ′ (p′ ) such that f0′ (x̂′ ) < f0′ (x′ ). By backward feasibility,
x̂ = Φbwd (x̂′ ; p) ∈ F (p). By objective preservation:
                           f0′ (x̂′ ; p′ ) = Φobj (f0 (x̂; p))   and   f0′ (x′ ; p′ ) = Φobj (f0 (x∗ ; p)).
Thus,
                                            Φobj (f0 (x̂; p)) < Φobj (f0 (x∗ ; p)).
Since Φobj is strictly increasing, this implies f0 (x̂; p) < f0 (x∗ ; p) which contradicts the optimality of x∗ . Using an
identical argument by contradiction, we can show that every optimal solution of M′ (p′ ) is mapped to an optimal solution
of M(p) by the backward mapping Φbwd (·; p). Definition 4.4 requires Φbwd (·; p) to be computable in polynomial time.
Therefore, given any optimal solution of M′ (p′ ), an optimal solution of M(p) can be recovered in polynomial time.
Hence M′ is an Audet reformulation of M.
For the instantiated claim, fix p and p′ = Φp (p). Definition 4.3 requires a mapping-producing algorithm A. Let
A(M(p), M′ (p′ )) output the backward mapping Φbwd with p bound as a constant, representing the mapping
                                                      f (x′ ) = Φbwd (x′ ; p).
This only copies p into a fixed-size algorithm, so A runs in polynomial time for all p ∈ P and p′ ∈ P ′ . By Definition 4.4,
f is polynomial-time computable, and the argument above shows f maps every optimal solution of M′ (p′ ) to an
optimal solution of M(p). Thus M′ (p′ ) is Quasi-Karp equivalent to M(p).

B     Lean Formalization
We now formalize the formulation (Definition 3.1) and reformulation (Definition 4.4) definitions in Lean. For both
definitions, we utilize a Lean structure. A structure is a collection of named fields and their types. See Listing 1
for the MILPFormulation and MILPReformulation structures. In the following sections, we provide details on how
each definition is formalized.

B.1     Formulation

A formulation M = (P, F , f0 ) is represented by the MILPFormulation structure. The Params field encodes the
parameter space P. Next, the Vars and feasible fields together encode the feasible region F. Lastly, obj encodes
the objective function f0 . Notice that both feasible and obj are functions of Params and Vars. See Listing 2 for an
example Lean formalization of the TSP MTZ formulation.
Discrepancies. This definition does not restrict Vars to Rn nor does it assert linearity conditions on either feasible
or obj. This additional typing would add modeling complexity to Vars, reduce legibility, and place unnecessary burden
on ATP. Our primary motivation is not to prove if a MILP formulation is well-formed. Hence, we make the practical
decision to exclude this typing.

B.2     Reformulation

We formalize reformulation with the MILPReformulation structure. This defines the reformulation construction
Φ(M, M′ ) = (Φp , Φfwd , Φbwd , Φobj ) along with the four conditions specified in Definition 4.4. The fields paramMap,
fwd, bwd, and obj encode Φp , Φfwd , Φbwd , and Φobj respectively. The fields fwd_feas and bwd_feas encode the
forward and backward feasibility conditions. The two objective mapping conditions are encoded by fwd_obj and
bwd_obj. Lastly, objMap_mono encodes the strict monotonicity objective condition. A formulation G is proven to
be a reformulation of F by declaring a definition of type MILPReformulation F G. This structure encodes both the


                                                                  14
                      FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



witnessing reformulation construction and proves it obeys the necessary conditions. Proving G is not a reformulation of
F requires proving the type MILPReformulation F G is uninhabited (i.e., no construction satisfying the conditions
exists).
Discrepancies. The Lean formalization does not enforce that the backward mapping Φbwd is computable in polynomial
time. Formalizing computational complexity in Lean is non-trivial and adds substantial proof burden to ATP. In our
experiments, we observe no examples of LLMs producing non-polynomial-time backward maps, so we om it the
condition from the Lean proof obligation.


                     Listing 1: Lean formalizations: MILPFormulation and MILPReformulation.
 import Mathlib.Tactic
 import Mathlib.Data.Real.Basic
 import Mathlib.Order.Basic

 structure MILPFormulation where
   Params   : Type                                       -- Parameter space
   Vars     : Params → Type                              -- Variables
   feasible : (p : Params) → Vars p → Prop               -- Feasible region
   obj      : (p : Params) → Vars p → R                   -- Objective function

 structure MILPReformulation (F G : MILPFormulation) where
   paramMap    : F.Params → G.Params                     -- Parameter mapping
   fwd         : (p : F.Params) → F.Vars p →             -- Forward mapping
                   G.Vars (paramMap p)
   bwd         : (p : F.Params) → G.Vars (paramMap p) → -- Backward mapping
                   F.Vars p
      _
   fwd feas    : ∀ p x, F.feasible p x →                 -- Forward feasibility condition
                   G.feasible (paramMap p) (fwd p x)
      _
   bwd feas    : ∀ p x', G.feasible (paramMap p) x' →    -- Backward feasibility condition
                   F.feasible p (bwd p x')
   objMap      : R → R                                     -- Objective mapping
   objMap_mono : StrictMono objMap                      -- Objective monotonicity
      _
   fwd obj     : ∀ p x, F.feasible p x →                 -- Forward objective condition
                   G.obj (paramMap p) (fwd p x) = objMap (F.obj p x)
      _
   bwd obj     : ∀ p x', G.feasible (paramMap p) x' →    -- Backward objective condition
                   G.obj (paramMap p) x' = objMap (F.obj p (bwd p x'))




                        Listing 2: An example Lean formalization of the TSP MTZ formulation.
 structure Params where
   n : N                           -- number of cities
   c : Fin n → Fin n → R           -- arc cost
   hn : 2 ≤ n

 structure Vars (p : Params) where
   x : Fin p.n → Fin p.n → Z       -- arc indicator
   u : Fin p.n → R                 -- position

 structure Feasible (p : Params) (v : Vars p) : Prop where
   -- Each city has exactly
                         P one outgoing arc
   hout : ∀ i : Fin p.n,     j : Fin p.n, v.x i j = 1
   -- Each city has exactly
                        P one incoming arc
   hin : ∀ j : Fin p.n,     i : Fin p.n, v.x i j = 1
   -- MTZ subtour elimination
   hmtz : ∀ (i : Fin p.n) (j : Fin p.n), i.val ̸= 0 → j.val ̸= 0 → i ̸= j →
     v.u i - v.u j + (p.n : R) * (v.x i j : R) ≤ (p.n : R) - 1
   -- Depot position fixed to 1
   hu_depot : haveI : NeZero p.n := <by have := p.hn; omega>; v.u 0 = 1
   hx_bin : ∀ (i j : Fin p.n), v.x i j = 0 ∨ v.x i j = 1
   -- u ∈ [2, n] for non-depot cities
   hu_lo : ∀ i : Fin p.n, i.val ̸= 0 → 2 ≤ v.u i
   hu_hi : ∀ i : Fin p.n, v.u i ≤ (p.n : R)
   -- No self-loops
   hx_no_self : ∀ i : Fin p.n, v.x i i = 0

 -- Minimize total arc cost
   Pobj (p : Params)
 def               P (v : Vars p) : R :=
      i : Fin p.n,     j : Fin p.n, p.c i j * (v.x i j : R)




                                                               15
                      FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



C FLARE Implementation Details
This section outlines the implementation details for every component of FLARE (Figure 1).1 We use a general-purpose
coding agent harness (Claude Code, Codex, and OpenCode) for both autoformalizing MILP formulations and ATP. This
design decision was inspired by recent work achieving competitive ATP performance with Claude Code [42]. In Section
C.1, we describe the agent harness prompt, working directory, and sandbox. To enable the agent to effectively compose
Lean proofs, we use the Lean-LSP-MCP (Section C.2) and two custom agent skills (Section C.3). After the agent exits,
FLARE does a final verification to check if a reformulation certificate was successfully generated (Section C.4).

C.1     Agent Harness

We programmatically initialize the agent harness in a headless mode using the CLI. The agent is given instructions and
provided with a working directory containing the necessary context. To isolate the agent’s working directory and avoid
duplicating the Lean environment (the Mathlib library is over 5GB), we run FLARE inside a Docker container.
Agent Prompt. In the agent prompt (Listing 3), we provide the agent with instructions to (1) formalize both MILP for-
mulations as MILPFormulation structures A and B and (2) attempt to declare a definition of type MILPReformulation
A B where paramMap formalizes the fixed parameter map.
Working Directory Files. The working directory is initialized with the following context:
   • templated LATEXdescriptions of both MILP formulations (Listing 5) and the parameter map (Listing 6),
   • Gurobi Python implementations for both MILP formulations and the parameter mapping, and
   • a Lean file Common.lean with MILPFormulation and MILPReformulation definitions.
Both the templated LATEX descriptions and Gurobi Python implementations are populated by the FormulationBench
JSON files. The formulation-bench Python package provides utilities to construct Gurobi Python implementations
from the JSON file code snippets. See Appendix E for additional details on the FormulationBench dataset structure.
Docker. We pre-build a Docker image called flare-agent with every agent CLI (Claude Code, Codex, and OpenCode),
the Lean-LSP-MCP, and a Lake-built Lean environment with Mathlib pre-compiled. When FLARE is invoked, it creates
a working directory on the host with all the necessary files. It then creates a Docker container from this image and
copies the working directory into the container. To use the pre-built Lean environment, we symlink .lake from the
pre-built location into the agent’s working directory. This configuration prevents duplication of the Lean environment
while ensuring FLARE can run in parallel without agents impacting each other’s Lean environment. Previously, we
attempted to isolate agents with the permissions and sandboxing mechanisms provided by each agent harness. We
found the implementations to be immature; Docker was the only reliable way to ensure the agent couldn’t access files
outside its working directory.

C.2     Lean-LSP-MCP

Lean-LSP-MCP [14]2 is a Model Context Protocol (MCP) server providing MCP Tools for Lean theorem proving. It
enables the agent to efficiently generate, debug, and compile Lean proofs and has been utilized by numerous Lean ATP
methods [7, 29, 42]. The Lean Language Server Protocol (LSP) traditionally allows editors like VS Code to get rich,
interactive feedback from a running Lean process. The Lean-LSP-MCP allows the agent to communicate directly with
this LSP and obtain feedback like a human theorem prover. It offers a broad range of tools including:
   • lean_goal. Get the proof goal at a specific location in the file. This allows the agent to observe precisely what
     sub-goal must be proved to continue making progress.
   • lean_diagnostic_messages. Retrieve all the diagnostic messages for a Lean file. This allows the agent to verify
     if the file is compiling and, if not, where fixes are necessary.
   • lean_verify. Verify the soundness of a proof. There are two conditions where a proof compiles, but is actually
     unsound: (1) a new axiom was added or (2) the sorry tactic is used to complete a goal (see Appendix C.4 for a
     further discussion). This tool allows the agent to verify that neither condition holds.
   • lean_multi_attempt. Attempt multiple tactics at a proof position and return the new goal state for each. This
     allows the agent to explore strategies for making progress in parallel.
   • lean_hover_info. Retrieve documentation for symbols, terms, and expressions. This allows the agent to view
     underlying definitions and reduces hallucination.
   1
       FLARE is implemented in the milp-flare Python package; see https://flare.henryrobbins.com.
   2
       https://github.com/oOo0oOo/lean-lsp-mcp


                                                          16
                       FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



C.3     Agent Skills

Agent skills are an “open format for extending AI agent capabilities with specialized knowledge and workflows.” They
are simply a directory containing context, scripts, or other resources related to a specific task. The directory contains
a SKILL.md file which tells the agent the skill’s name and provides instructions on when to use it. Skills allow for
progressive disclosure where the agent loads additional task-specific context as needed.
We define two custom agent skills, lean-milp-formulation and lean-milp-reformulation, for autoformalizing
MILP formulations and proving reformulations respectively. The agent prompt explicitly instructs the agent to invoke
these skills. Both skills contain instructions along with a template Lean file containing detailed comments about Lean
modeling choices and file structure. In addition to our custom skills, we use the general-purpose Lean 4 skills [19].1

C.4     Final Verification

After the agent exits, we inspect the working directory. First, we verify the presence of A/Formulation.lean,
B/Formulation.lean, and Reformulation.lean. If all of these files are present and compile, we then check that
Reformulation.lean contains a MILPReformulation A B definition. Finally, we guard against two conditions
where a proof compiles but is unsound: use of the sorry tactic and the introduction of non-standard axioms. The sorry
tactic can skip any proof obligation and indicates the proof has yet to be formally verified. We emit #print axioms
for the MILPReformulation A B definition, which reports its transitive axiom dependencies; a sorry surfaces here as
sorryAx. We require that the proof depend only on Lean’s three standard axioms (propext, Classical.choice, and
Quot.sound). If all files compile and the MILPReformulation A B definition is sorry-free and introduces no new
axioms, formulation B is deemed a reformulation of A under the fixed parameter mapping.




   1
       https://github.com/cameronfreer/lean4-skills


                                                           17
                     FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



D   Prompts

                                              Listing 3: FLARE Agent Prompt
You are a mixed-integer linear programming (MILP) and Lean 4 expert. You have been tasked with formalizing two MILP
      formulations in Lean 4 and then proving that formulation B is a reformulation of formulation A.

## Working Directory Structure

The working directory will be initialized with the following structure:

‘‘‘
  +-- A
  |   +-- Formulation.lean    # Write the Lean 4 formalization of Formulation A here
  |   +-- formulation.md      # Natural language description of Formulation A
  |   \-- solve.py            # Python script that solves Formulation A
  +-- B
  |   +-- Formulation.lean    # Write the Lean 4 formalization of Formulation B here
  |   +-- formulation.md      # Natural language description of Formulation B
  |   \-- solve.py            # Python script that solves Formulation B
  +-- Common.lean             # Definition of ‘MILPFormulation‘ and ‘MILPReformulation‘
  +-- Reformulation.lean      # Write the reformulation proof here
  +-- map.md                  # The parameter mapping from Formulation A to Formulation B
  +-- map.py                  # Python script computing B’s parameters from A’s
  +-- lake-manifest.json      # DO NOT EDIT!
  +-- lakefile.toml           # DO NOT EDIT!
  \-- lean-toolchain          # DO NOT EDIT!
‘‘‘

## Parameter Map
The parameter mapping of the reformulation construction is *given*, not something you search for. ‘map.md‘ states, for each
      parameter of Formulation B, how it is computed from the parameters of Formulation A; ‘map.py‘ is the same mapping as an
      executable Python script. Read ‘map.md‘ before writing either ‘Formulation.lean‘ file.

## Workflow
1. Read ‘map.md‘ (and ‘map.py‘ where the LaTeX is ambiguous) to understand the given parameter mapping.
2. Utilize the ‘lean-milp-formulation‘ skill to generate both ‘Formulation.lean‘ files.
3. Validate each ‘Formulation.lean‘ file with ‘mcp__lean-lsp__lean_diagnostic_messages‘. Fix any issues that arise and repeat
      until both files compile cleanly.
4. Run ‘Bash(lake build A.Formulation B.Formulation)‘ to materialize their oleans.
5. Determine whether formulation B is a mathematical reformulation of formulation A *under the given parameter mapping*.
6. If B is a reformulation of A, use the ‘lean-milp-reformulation‘ skill to generate a compiled ‘MILPReformulation‘ proof in ‘
      Reformulation.lean‘, with its ‘paramMap‘ field implementing the mapping in ‘map.md‘.
7. Validate ‘Reformulation.lean‘ with ‘mcp__lean-lsp__lean_verify‘ to ensure there are no stubs. Fix any issues that arise and
      repeat until both files compile cleanly.

## Rules
- IMPORTANT: Only read/write files that exist in *this* working directory. Do not navigate outside of it for any reason.
- The ‘paramMap‘ field of your ‘MILPReformulation‘ MUST implement the mapping given in ‘map.md‘. Do not substitute a different
      parameter mapping, even if another one would make the proof easier. If B is not a reformulation of A under *this* mapping,
       that is a negative result -- report it as described below rather than switching mappings.
- ‘map.md‘ also constrains how you formalize each ‘Formulation.lean‘: B’s ‘Params‘ structure must have exactly the parameters
      that ‘map.md‘ computes, and A’s ‘Params‘ must have the parameters ‘map.md‘ computes them from. If you cannot express the
      mapping as a total function ‘A.Params -> B.Params‘, the mismatch is in your formalization -- fix the ‘Params‘ structures
      rather than adapting the mapping.
- DO NOT EDIT ‘map.md‘ or ‘map.py‘.
- The Lean project root is the current directory. Use ‘import A.Formulation‘ and ‘import B.Formulation‘.
- You MUST use the lean-lsp MCP tools (mcp__lean-lsp__*) to check compilation as you work. Before doing anything else, verify
      the server is available by calling ‘mcp__lean-lsp__lean_diagnostic_messages‘ on ‘Common.lean‘. If the first probe reports
      the tool as unregistered or still connecting, that is expected -- probe again until it answers, up to 3 attempts. If the *
      same* server-level failure (e.g. "Failed to start Lean language server", tool not registered) persists, conclude the
      environment is unusable: write ‘MCP_UNAVAILABLE: <error>‘ to Reformulation.lean and exit. Do not fall back to ‘lake env
      lean‘ to perform compilation.
- If ‘lake build‘ fails, treat the error message as a real signal -- read it, fix the cause (typically a typo, missing import,
      or stale olean), and retry. Only after the *same* failure persists across two clean retries should you write ‘
      LAKE_BUILD_FAILED: <error>‘ to Reformulation.lean and exit. Persistent toolchain-level failures (e.g. elan/toolchain
      missing) are the exit case; ordinary compile errors are not.
- Generate both Formulation.lean files before attempting the reformulation proof.
- Confirm the final reformulation proof with ‘mcp__lean-lsp__lean_verify‘ on the ‘MILPReformulation‘ definition. The returned
      axioms must NOT contain ‘sorryAx‘ -- if it does, the proof has a stub and you must finish it.
- You are expected to iterate on the proof until it compiles and ‘lean_verify‘ reports no ‘sorryAx‘. A non-trivial
      reformulation proof typically runs 100+ lines with many manual ‘refine‘/‘rcases‘/‘simp‘ steps and multiple rounds of
      compile-error fixing. You should only exit before this point if there is concrete evidence that B is *not* a reformulation
       of A under the given assumptions.

## Common Mistakes
- Interpret ‘lean_diagnostic_messages‘ carefully: ‘success:true, items:[]‘ means the file compiles cleanly. ‘success:false,
      items:[]‘ typically means imports aren’t built yet -- build them, don’t assume the file is broken. Real errors come back
      as ‘items‘ with severity/message fields.




                                                              18
                            FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



     - If there issues with the Lean environment or MCP tools, it is imperative to handle them as described in the rules above.
           Report and exit.
     - If you are stuck proving the reformulation due missing assumptions in the ‘Formulation.lean‘ files, first verify that the
           assumptions specified in ‘formulation.md‘ are all present in the corresponding ‘Formulation.lean‘. If any assumptions are
           missing, add them. Otherwise, DO NOT ADD ASSUMPTIONS YOURSELF. Instead, report the missing necessary assumptions as an
           issue preventing the reformulation proof in ‘Reformulation.lean‘ and exit.

     ## Available Tools
     **Filesystem:** ‘Bash(ls ./*)‘, ‘Bash(find ./*)‘,
     **Read:** ‘Read(./*)‘, ‘Bash(cat ./*)‘, ‘Bash(head ./*)‘, ‘Bash(tail ./*)‘, ‘Bash(less ./*)‘, ‘Bash(more ./*)‘, ‘Bash(bat ./*)‘
     **Edit:** ‘Edit(./*)‘
     **Write:** ‘Write(./*)‘
     **Skills:** ‘lean4:lean4‘, ‘lean-milp-formulation‘, ‘lean-milp-reformulation‘
     **MCP Tools:** ‘mcp__lean-lsp__*‘
     **Lake:** ‘Bash(lake env lean:*)‘, ‘Bash(lake build:*)‘



Listing 4: FLARE-NL Prompt. The No Definition variant omits L9-27 and drops the Φp symbol from L31. The Allow
Implicit variant omits L38 as well as implicit assumptions and constraints from the formulation descriptions. The
formulation descriptions are populated by Listing 5 and the parameter mapping is populated by Listing 6.
1     You are given the following two Mixed-Integer Linear Programming (MILP) formulations. You are tasked with deciding if
            formulation B is a reformulation of formulation A.
2
3     ## Formulations
4
5     {{ formulation_a }}
6
7     {{ formulation_b }}
8
9     ## Definitions
10
11    Use the following definition of formulation and reformulation to guide your reasoning.
12
13    **Formulation.** A MILP *formulation* $A$ is a tuple ${A = (P, F, f_0)}$ with parameter space $P$, feasible region $F(p) \
            subseteq R^{n(p)}$, and objective function $f_0$. For instance $p \in P$, the feasible region $F(p)$ is defined by $m(p)
            $ linear constraints, $f_i(\cdot ; p) : R^{n(p)} \to R$ for all $i \in [m(p)]$. The first $k(p) \leq n(p)$ variables are
             integers. The feasible region is
14    $$F(p) = \{x \in \mathbb{Z}^{k(p)} \times R^{n(p)-k(p)}~|~f_i(x;p) \leq 0 ~\forall i\in[m(p)]\}.$$
15    The objective is to minimize the linear function $f_0(\cdot ; p) : R^{n(p)} \to R$. A formulation $A$ is *instantiated* with
            an *instance* $p \in P$. We denote an instantiated formulation as ${A(p) = (F(p), f_0(p))}$.
16
17    **Reformulation.** Let $A = (P, F, f_0)$ and $B = (P’, F’, f’_0)$ be formulations. A *reformulation construction* from $A$ to
             $B$ is a tuple $\Phi(A, B) = (\Phi_{p},\, \Phi_{fwd},\, \Phi_{bwd},\, \Phi_{\text{obj}})$ consisting of:
18    - a parameter mapping $\Phi_{p} : P \to P’$,
19    - a forward mapping $\Phi_{fwd}(\cdot;p) : R^{n(p)} \to R^{n’(\Phi_{p}(p))}$,
20    - a backward mapping $\Phi_{bwd}(\cdot;p) : R^{n’(\Phi_{p}(p))} \to R^{n(p)}$ computable in polynomial time, and
21    - an objective mapping $\Phi_{\text{obj}} : R \to R$.
22
23    $B$ is a *reformulation* of $A$ if there exists a reformulation construction satisfying the following conditions for every
            instance $p \in P$, with $p’ = \Phi_{p}(p)$:
24    - **Forward feasibility.** For all feasible points $x \in F(p)$, the forward mapping maps to a feasible point $x’ = \Phi_{fwd
            }(x;p) \in F’(\Phi_{p}(p))$.
25    - **Backward feasibility.** For all feasible points $x’ \in F’(p’)$, the backward mapping maps to a feasible point $x = \Phi_{
            bwd}(x’;p) \in F(p)$.
26    - **Objective mapping.** The forward and backward mappings induce an objective mapping. The following two conditions must
            hold. (1) For all feasible points ${x \in F(p)}$, the forward mapped point $x’ = \Phi_{fwd}(x;p)$ has objective value
            $f_0’(x’;p’) = \Phi_{\text{obj}}(f_0(x;p))$. (2) For all feasible points ${x’ \in F’(p’)}$, the backward mapped point is
             $x = \Phi_{bwd}(x’;p)$ and $f_0’(x’;p’) = \Phi_{\text{obj}}(f_0(x;p))$.
27    - **Strictly monotone.** The objective mapping $\Phi_{\text{obj}}$ is strictly monotonically increasing.
28
29    ## Parameter Mapping
30
31    The parameter mapping $\Phi_{p}$ is *given*. It computes each parameter of formulation B from the parameters of formulation A.

32
33    {{ parameter_map }}
34
35    ## Instructions
36
37    - Decide whether B is a reformulation of A under *this* parameter mapping. Do not substitute a different one, even if another
             mapping would make B a reformulation of A.
38    - Do NOT make any assumptions about the formulation or parameter space that are not explicitly stated in the formulation
            descriptions.
39    - When uncertain, state that formulation B is *not* a reformulation of A.
40    - Provide a short summary of your conclusion (at most 2,500 characters) and a final determination of whether B is a
            reformulation of A (true or false).




                                                                   19
                        FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



Listing 5: Formulation Prompt Template. Rendered as formulation.md for FLARE and {{ formulation_(a|b) }}
in the FLARE-NL prompt.
 # {{ problem_name }}

 ## Problem Description

 {{ problem_description }}

 ## Formulation

 ### Parameters

 {% for name, p in parameters.items() %}
 - **{{ name }}** (type: {{ p.type.value }}, shape: ‘{{ p.shape }}‘): {{ p.description }}
 {% endfor %}

 {% if assumptions %}

 ### Assumptions

 {% for a in assumptions %}
 - {{ a.description }}
 $${{ a.formulation }}$$
 {% endfor %}
 {% endif %}

 {% if definitions %}

 ### Definitions

 {% for name, d in definitions.items() %}
 - **{{ name }}**: {{ d.description }}
 $${{ d.formulation }}$$
 {% endfor %}
 {% endif %}

 ### Variables

 {% for name, v in variables.items() %}
 - **{{ name }}** (type: {{ v.type.value }}, shape: ‘{{ v.shape }}‘): {{ v.description }}
 {% endfor %}

 ### Constraints

 {% for c in constraints %}
 - {{ c.description }}
 $${{ c.formulation }}$$
 {% endfor %}

 ### Objective

 {{ objective.description }}
 $${{ objective.formulation }}$$




Listing 6: Parameter Map Template. Rendered as map.md for FLARE and {{ parameter_map }} in the FLARE-NL
prompt.
 # Parameter Map

 {% for note in notes %}
 {{ note }}

 {% endfor %}
 {% if definitions %}
 ## Definitions

 {% for name, d in definitions.items() %}
 - **{{ name }}**
 $${{ d.formulation }}$$
 {% endfor %}

 {% endif %}
 ## Parameters

 {% for name, d in parameters.items() %}
 - **{{ name }}**
 $${{ d.formulation }}$$
 {% endfor %}




                                                               20
                      FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



E       FormulationBench Details
The FormulationBench dataset is a collection of 20 optimization problems, 109 MILP formulations, and 89 reformulation
pairs (Table 4). The dataset can be downloaded via the formulation-bench Python package. The documentation1
provides user guides, detailed problem and formulation descriptions, the dataset schema, and the package API reference.
We provide a concise summary here. The dataset is comprised of three sources:
    • EquivaFormulation [68]. The five EquivaFormulation problems were sampled at random. These are simple
      optimization problems with a few scalar variables and constraints. Each one contains an original formulation and
      10 transformations. These are enumerated in Table 1 of [68]. We make the following modifications.
         – The Add Valid Inequalities transformation is instance-specific. Because we are interested in formulation-level
            reformulation, we omit this transformation type.
         – We change the label on the Replace by Base-10 Representation. This formulation replaces each integer
            variable with a base-10 decimal expansion. It relies on using enough digit variables to support the size of the
            test instance data. Hence, this transformation is not valid under our formulation-level notion of reformulation.
    • EvoCut [66]. They define 7 optimization problems for which their method EvoCut proposes numerous cutting
      planes. We construct reformulation pairs by pairing the original MILP formulation with one augmented by the cut.
      A cutting plane valid for all instances is a valid reformulation.
    • Ferchtandiker et al. [16]. They define 8 real-world optimization problems, each admitting an efficient and
      inefficient formulation. We add each as a pair to FormulationBench.

Table 4: The 20 optimization problems in the FormulationBench dataset with their source. The NP-hard column indicates if the
problem is NP-hard. We only use the 16 NP-hard problems in our experiments.
            Problem   Name                                                 Source                        NP-hard
            p1        EquivaFormulation Instance 47                        EquivaFormulation [68]           ✗
            p2        EquivaFormulation Instance 74                        EquivaFormulation [68]           ✓
            p3        EquivaFormulation Instance 92                        EquivaFormulation [68]           ✓
            p4        EquivaFormulation Instance 183                       EquivaFormulation [68]           ✗
            p5        EquivaFormulation Instance 217                       EquivaFormulation [68]           ✗
            p6        Capacitated Warehouse Location (CWLP)                EvoCut [66]                      ✓
            p7        Rectangular Tiling (IMO6)                            EvoCut [66]                      ✗
            p8        Job Shop Scheduling (JSSP)                           EvoCut [66]                      ✓
            p9        Multi-Commodity Network Design (MCND)                EvoCut [66]                      ✓
            p10       Pickup and Delivery with Time Windows (PDPTW)        EvoCut [66]                      ✓
            p11       Sub-Hour Unit Commitment (SHUC)                      EvoCut [66]                      ✓
            p12       Traveling Salesman Problem (TSP)                     EvoCut [66]                      ✓
            p13       Air Traffic Flow Management                          Ferchtandiker et al. [16]        ✓
            p14       Blood Bank Netherlands                               Ferchtandiker et al. [16]        ✓
            p15       Dutch Housing Problem                                Ferchtandiker et al. [16]        ✓
            p16       Park and Bike Hub Location (Mobian)                  Ferchtandiker et al. [16]        ✓
            p17       Open-Pit Mine Production Scheduling                  Ferchtandiker et al. [16]        ✓
            p18       Timor-Leste Hospital Location                        Ferchtandiker et al. [16]        ✓
            p19       UN Humanitarian Disaster Response Hub (UNHDR)        Ferchtandiker et al. [16]        ✓
            p20       World Food Program Food Distribution                 Ferchtandiker et al. [16]        ✓

Dataset Structure. Each problem contains (1) a Markdown problem description file, (2) a JSON information file,
and (3) JSON files with instance data and the corresponding optimal solution. Each problem contains at least two
formulations. Each formulation contains (1) a JSON information file, (2) a Python script to transform raw problem
data into the formulation’s parameter space, and (3) a ground-truth MILPFormulation Lean formalization. The JSON
information file format is an extension of the format introduce by the NLP4LP dataset [1]. We add assumptions (see
Section 6.1 for a discussion) and definitions fields. Lastly, each formulation is flagged as valid if it is faithful to the
underlying optimization problem.
Reformulation Test Set. FormulationBench contains 89 pairs of formulations (M, M′ ) containing 63 positive
examples where M′ is a constructive reformulation of M and 26 negative examples. Our experiments use the 54 pairs
(42 positive, 12 negative) belonging to the 16 NP-hard problems. Each reformulation pair additionally contains a JSON
file specifying the parameter mapping Φp from P to P ′ . For every valid reformulation, we provide a ground-truth
MILPReformulation proof.
    1
        https://formulation-bench.henryrobbins.com


                                                            21
                     FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



F     Invalid Reformulations
While preparing the FormulationBench dataset, we verified prior LLM-generated MILP reformulations: cutting planes
proposed by EvoCut [66] and reformulation pairs proposed by Ferchtandiker et al. [16]. In the process, FLARE failed to
produce reformulation certificates for 5 cutting planes and 4 formulations that were confirmed invalid upon manual
inspection. In this section, we provide proofs of invalidity.

F.1     EvoCut Cutting Planes

Yazdani et al. [66] recently proposed the EvoCut framework to automatically generate acceleration cuts for MILP
formulations using an LLM-based evolutionary search. Acceleration cuts are constraints added to a MILP formulation
with the aim of reducing solve time. Importantly, such cuts are not guaranteed to be valid cutting planes or even
optimality preserving. This pragmatic choice to consider acceleration cuts enables automation by reducing the
computational burden required to verify candidate cuts. A cut is considered an acceleration cut if it does not change the
optimal objective value on a small verification set of problem instances.
In the FormulationBench dataset, we constructed a reformulation from a cutting plane by adding the cut to the base
formulation. A formulation constructed from a valid cutting plane trivially satisfies Definition 4.4. Using FLARE, we
identified that 5 of the 43 acceleration cuts proposed by EvoCut are invalid cutting planes. These cuts span the TSP and
a rectangle tiling problem. In the case of TSP, all three invalid cutting plane families are only invalid on TSP instances
of size n ≤ 3. While these counter-examples are not practically meaningful, they illustrate the importance of explicitly
stating all assumptions of the problem data. In the case of rectangle tiling, the cuts meaningfully change the set of
optimal solutions (see Figure 3). This motivates the importance of formally verifying reformulations, especially for
non-standard optimization problems where an LLM is more likely to have an error in reasoning.

F.1.1    Traveling Salesman Problem (TSP)
For the TSP, EvoCut generates acceleration cuts for the Miller–Tucker–Zemlin (MTZ) formulation defined in Section 3.
Between v1 and v2 of the arXiv preprint, there are 8 acceleration cuts proposed. FLARE identifies the following three
as invalid cutting planes. Both cuts v1-EC3 and v2-EC2 eliminate triangles including the depot node and cut v2-EC1
eliminates all two-city subtours.
            xj1 + xji + (uj − ui − 1) ≤ (n − 1)(2 − x1i − xij )              ∀i, j ∈ V \ {1}, i ̸= j            (v1-EC3)
            xij + xji ≤ 1                                                    ∀i, j ∈ V, i < j                   (v2-EC1)
            x1i + xi1 + x1j + xj1 + xij + xji ≤ 2                            ∀i, j ∈ V \ {1}, i < j             (v2-EC2)

Proposition F.1. The cut v1-EC3 is not a valid cutting plane for the MTZ TSP formulation.

Proof. Consider the 3-node TSP instance depicted in Figure 2a with feasible tour 1 → 2 → 3 → 1. Letting i = 2 and
j = 3, the cut v1-EC3 reduces to 1 ≤ 0, which does not hold. Hence, there exists a feasible integer point that is not
satisfied by the cut. Therefore, the cut is invalid.
Proposition F.2. The cut v2-EC1 is not a valid cutting plane for the MTZ TSP formulation.

Proof. Consider the 2-node TSP instance with the unique feasible tour 1 → 2 → 1. The MTZ formulation permits
x12 = x21 = 1, corresponding to traversing both arcs of this tour. Setting i = 1 and j = 2, the cut v2-EC1 reduces to
2 ≤ 1, which does not hold. Hence, there exists a feasible integer point that is not satisfied by the cut. Therefore, the
cut is invalid.
Proposition F.3. The cut v2-EC2 is not a valid cutting plane for the MTZ TSP formulation.

Proof. Consider the 3-node TSP instance depicted in Figure 2a with feasible tour 1 → 2 → 3 → 1. Setting i = 2 and
j = 3, the cut v2-EC2 reduces to 3 ≤ 2, which does not hold. Hence, there exists a feasible integer point that is not
satisfied by the cut. Therefore, the cut is invalid.

F.1.2    Rectangular Tiling with One Hole per Row and Column (IMO6)
This problem is inspired by IMO 2025 Problem 6. Given an N × N grid of unit squares, one must place rectangular
tiles (of various sizes) such that each row and column of the grid contain exactly one uncovered square (a hole). The
objective is to minimize the number of tiles used. Yazdani et al. [66] introduce the following notation and formulation.


                                                           22
                       FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



Notation.
   • R = {1, . . . , N } rows and C = {1, . . . , N } columns
   • I = {(a, b) ∈ C 2 | a ≤ b} contiguous column-intervals
   • hij ∈ {0, 1} hole indicator
   • xab
      i ∈ {0, 1} indicates if columns a through b on row i are covered by the same tile
      ab ab
   • si , ti ∈ {0, 1} indicate if a tile spanning columns a to b begins on row i or ends on row i, respectively
Formulation.                           X X
                               min                      sab
                                                         i
                                       i∈R (a,b)∈I
                                       X
                                s.t.         hij = 1                       ∀i ∈ R
                                       j∈C
                                       X
                                             hij = 1                       ∀j ∈ C
                                       i∈R
                                        X
                                                 xab
                                                  i + hij = 1              ∀i ∈ R, ∀j ∈ C                                     (IMO6)
                                       (a,b)∈I
                                       a≤j≤b

                                       xab   ab
                                        1 − s1 = 0                         ∀(a, b) ∈ I
                                       xab   ab     ab   ab
                                        i − xi−1 − si + ti−1 = 0           ∀i = 2, . . . , N, ∀(a, b) ∈ I
                                       xab   ab
                                        N − tN = 0                         ∀(a, b) ∈ I
                                       hij ∈ {0, 1}                        ∀i ∈ R, ∀j ∈ C
                                       xab   ab ab
                                        i , si , ti ∈ {0, 1}               ∀i ∈ R, ∀(a, b) ∈ I

Between v1 and v2 of the arXiv preprint, there are 8 acceleration cuts proposed. FLARE identifies the following two as
invalid cutting planes. The cut v1-EC1 enforces that a tile end (bottom-right corner) must be immediately to the left of
any hole, and the cut v1-EC2 enforces that a tile start (top-left corner) must be immediately to the right of any hole.

                                       X
                            hij ≤             tab
                                               i                                ∀i ∈ R, ∀j ∈ {2, . . . , N }                 (v1-EC1)
                                    (a,b)∈I
                                    b=j−1
                                       X
                            hij ≤             sab
                                               i                                ∀i ∈ R, ∀j ∈ {1, . . . , N − 1}              (v1-EC2)
                                    (a,b)∈I
                                    a=j+1




Proposition F.4. The cut v1-EC1 is not a valid cutting plane for the IMO6 formulation.

Proof. Consider the N = 3 counterexample depicted in Figure 3. Let i = j = 2. The inequality reduces to h22 ≤ t11      2 .
Substituting yields 1 ≤ 0, which does not hold. Hence, there exists a feasible integer point that is not satisfied by the
cut. Therefore, the cut is invalid.



                                                    1         0   0         0        1     1            0      1   0

                                                    0         1   0         1        0     0            0      0   1

                                                    0         0   1         0        1     0            1      1   0


                    3x3 Tiling

Figure 3: A feasible rectangular tiling for the N = 3 instance of IMO 2025 Problem 6. Decision variable values for the hole
indicator hij , start flag sjj              jj                                                             ab     ab
                            i and end flag ti are depicted in the grids. Note the figure does not specify si and ti for a < b. However,
since all tiles have unit width, these variables all have value 0.


                                                                      23
                                  FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



Proposition F.5. The cut v1-EC2 is not a valid cutting plane for the IMO6 formulation.

Proof. Consider the N = 3 counterexample depicted in Figure 3. Let i = 2 and j = 2. The inequality reduces to
h22 ≤ s332 . Substituting yields 1 ≤ 0, which does not hold. Hence, there exists a feasible integer point that is not
satisfied by the cut. Therefore, the cut is invalid.

F.2        Ferchtandiker Formulation Pairs

Ferchtandiker et al. [16] introduces a dataset1 containing an efficient and inefficient MILP formulation for 8 optimization
problems. The dataset includes both LATEX and GurobiPy code for each formulation. In the process of incorporating
these reformulations in to the FormulationBench dataset, FLARE identified 4 invalid reformulations.
We prove the Air Traffic Management (ATM) and UN Humanitarian Disaster Response (UNHDR) reformulation pairs
are not related by a constructive reformulation in either direction under the identity parameter mapping. We do not
provide proofs for the World Food Program (WFP) since both formulations are polynomially-solvable linear programs,
and our constructive reformulation definition is only meaningful on NP-hard formulations (Remark 4.5). The Open
Pit Mining reformulation is intentionally a relaxation. It is expected to violate our definition and we omit any further
discussion.
In FormulationBench, we modify the ATM, UNHDR, and WFP formulations to make them valid constructive reformu-
lations, and we modify WFP to be NP-hard. See the documentation2 for detailed descriptions of these modifications.

F.2.1        Air Traffic Management (ATM)
This problem consists of assigning each plane in an airline’s fleet to a location (airport or airspace sector) over a
sequence of time periods. The assignment must respect each location’s capacity over time and the network’s adjacency
structure. Planes can only travel to locations that are a single time unit away. The objective is to maximize the total
reward accrued for visiting locations. Ferchtandiker et al. [16] introduces the following formulations of this problem.
Notation.
   • P : set of vehicles (planes).
   • A: set of locations (airports and airspace sectors).
   • T : set of time periods.
   • capa,t : capacity of location a ∈ A at time t ∈ T .
   • τa,a′ : travel time from location a to location a′ .
   • ra,t : reward for being at location a ∈ A at time t ∈ T .
Formulations. Both formulations share the binary departure variable xp,a,a′ ,t ∈ {0, 1}, which indicates whether
plane p departs from a to a′ at time t.3 The Efficient formulation is purely event-based. The Inefficient formulation
additionally tracks plane locations via yp,a,t ∈ {0, 1}, which indicates whether plane p is at location a at time t.
            X X X                                                                                    X X X
max                          ra,t yp,a,t                                                    max                     ra,t
           p∈P a∈A t∈T                                                                              p∈P a∈A t∈T
            X                                                                                                                             
  s.t.           yp,a,t = 1                         ∀p ∈ P, t ∈ T
                                                                                                       X            X                       
           a∈A                                                                                                                  xp,a′ ,a,t′ 
                                                                                                                                            
                                                                                                          a′ ∈A t′ :t′ +τ ′ =t
            X
                 yp,a,t ≤ capa,t                    ∀a ∈ A, t ∈ T                                                        a ,a
           p∈P                                                                                       X      X    X
                                                                                             s.t.                    xp,a,a′ ,t ≥ 1              ∀p ∈ P
           yp,a,t = yp,a,t−1 +                                                                      a∈A a′ ∈A t∈T
              X         X
                                      xp,a′ ,a,t′
                                                                                                     X      X
                                                                                                                xp,a,a′ ,t ≤ capa,t              ∀a ∈ A, t ∈ T
             a′ ∈A t′ :t′ +τ ′ =t                                                                   p∈P a′ ∈A
                            a ,a
                  X                                                                                                                                           ′
             −           xp,a,a′ ,t                 ∀p ∈ P, a ∈ A, t > 0                            xp,a,a′ ,t ∈ {0, 1}                          ∀p ∈ P, a, a ∈ A, t ∈ T
                 a′ ∈A                                                                                                                                            (Efficient)
           yp,a,t ∈ {0, 1}                          ∀p ∈ P, a ∈ A, t ∈ T
                                                                 ′
           xp,a,a′ ,t ∈ {0, 1}                      ∀p ∈ P, a, a ∈ A, t ∈ T
                                                                       (Inefficient)

      1
          The dataset is available at https://github.com/nathan-ferchtandiker/LLMs-For-Optimization-Reformulations
      2
          https://formulation-bench.henryrobbins.com/en/latest/problems
      3
          In the dataset, this variable is denoted zp,a,a′ ,t in the inefficient formulation. We use xp,a,a′ ,t for both formulations.


                                                                                       24
                          FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving


                                                                                                      P
The two formulations have misaligned objectives semantics. In the inefficient formulation, the reward p,a,t ra,t yp,a,t
            P time period a plane is present at a location, so a plane that remains at a for k consecutive time periods
accrues at every
contributes t ra,t over those k periods. In the efficient formulation, the reward only accrues on arrivals, so the same
solution contributes only the single reward ra,t at the arrival time.
First, we establish a useful obstruction that asserts the existence of a bijection between the objective value sets of
constructive reformulations.
Lemma F.6 (Objective-level bijection). Let Φ = (Φp , Φfwd , Φbwd , Φobj ) be a reformulation construction (Definition
4.4) from M to M′ , and let p ∈ P with p′ = Φp (p). Write V (p) = {f0 (x; p) : x ∈ F (p)} and V ′ (p′ ) = {f0′ (x′ ; p′ ) :
x′ ∈ F ′ (p′ )} for the attained objective-value sets. Then Φobj is a bijection from V (p) onto V ′ (p′ ); in particular
|V (p)| = |V ′ (p′ )|.

Proof. We first show Φobj (V (p)) ⊆ V ′ (p′ ). For v = f0 (x; p) ∈ V (p) with x ∈ F(p), the point Φfwd (x; p) lies in
F ′ (p′ ) by forward feasibility and has objective value Φobj (v) by objective preservation. Hence Φobj (v) ∈ V ′ (p′ ).
We now show the reverse inclusion V ′ (p′ ) ⊆ Φobj (V (p)). For v ′ = f0′ (x′ ; p′ ) ∈ V ′ (p′ ) with x′ ∈ F ′ (p′ ), the point
x = Φbwd (x′ ; p) lies in F(p) by backward feasibility and satisfies v ′ = Φobj (f0 (x; p)) by objective preservation.
Hence v ′ ∈ Φobj (V (p)). Both inclusions yield Φobj (V (p)) = V ′ (p′ ). Since Φobj is strictly monotonically increasing,
it is injective, so this surjection is a bijection and |V (p)| = |V ′ (p′ )|.
Proposition F.7. The Inefficient and Efficient formulations of ATM are not related by a constructive reformulation
(Definition 4.4) in either direction under the identity parameter mapping Φp .

Proof. Consider a single-plane, single-location instance p. Let P = {1}, A = {a}, and T = {0, 1} with τa,a = 1,
capa,0 = capa,1 = 1, and ra,0 = ra,1 = 1. Write xt := x1,a,a,t and yt := y1,a,t . Let Veff (p) and Vineff (p) denote the
objective values attained on p by the Efficient and Inefficient formulations respectively.
In the Efficient formulation, the constraints reduce to x0 + x1 ≥ 1 and xt ≤ capa,t = 1, so the feasible set is
{(1, 0), (0, 1), (1, 1)}. A departure at time t arrives at time t + τa,a = t + 1, so a departure at t = 1 arrives at t = 2 ∈
                                                                                                                           /T
and contributes nothing; the objective equals ra,1 x0 = x0 . Hence Veff (p) = {0, 1}.
                                   P
In the Inefficient formulation, a∈A y1,a,t = 1 with |A| = 1 forces y0 = y1 = 1 at every feasible point. The
point y0 = y1 = 1, x0 = x1 = 0 satisfies the transition constraint, so the feasible set is nonempty. Its objective is
y0 ra,0 + y1 ra,1 = 2, giving Vineff (p) = {2}.
Suppose that a constructive reformulation between the two formulations with Φp the identity exists. By Lemma
F.6, |Veff (p)| = |Vineff (p)| regardless of which formulation is the source. But |Veff (p)| = 2 ̸= 1 = |Vineff (p)|, a
contradiction.

F.2.2      UN Humanitarian Disaster Response Hub (UNHDR)
This problem consists of selecting a fixed number of response hubs to service a set of disaster regions. The selection
must satisfy demand and response time constraints. The objective is to minimize transportation cost. Ferchtandiker
et al. [16] introduces the following formulations of this problem.
Notation.
   • H: set of candidate hubs.
   • H f ⊆ H: set of hubs that must be open (fixed hubs).
   • C: set of disaster regions.
   • ac : number of people affected in region c ∈ C.
   • Chc : cost per person from hub h to region c.
   • thc : travel time from hub h to region c.
   • T : maximum allowed (weighted) travel time per region.
   • n: maximum number of hubs that can be opened.
   • M : sufficiently large constant (used in big-M constraints).
Formulations. The Inefficient formulation introduces a binary indicator variable yh to indicate if hub h ∈ H is opened
and binary indicator zhc to indicate if hub h ∈ H is assigned to serve region c ∈ C. Lastly, xhc is the fraction of region
c’s demand that is served by hub h.1 The Efficient formulation drops the hub indicator zhc variables.
    1
        In the dataset, this variable is denoted qhc . We use xhc for consistency with the efficient formulation.


                                                                     25
                               FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving


                 X X                                                                   X X
        min               ac Chc xhc                                          min               ac Chc xhc
                h∈H c∈C                                                               h∈H c∈C
                                                                                      X
         s.t.   xhc ≤ M zhc            ∀h ∈ H, c ∈ C                           s.t.         xhc ≤ |C|yh      ∀h ∈ H
                 X                                                                    c∈C
                     zhc = 1           ∀c ∈ C                                          X
                h∈H                                                                         xhc = 1          ∀c ∈ C
                X                                                                     h∈H
                      zhc ≤ |C|yh      ∀h ∈ H                                          X
                c∈C                                                                         yh ≤ n                              (Efficient)
                 X                                                                    h∈H
                      xhc = 1          ∀c ∈ C
                                                                                                                      f
                h∈H                                      (Inefficient)                yh = 1                 ∀h ∈ H
                 X
                      yh ≤ n
                                                                                       X
                                                                                           thc xhc ≤ T       ∀c ∈ C
                h∈H                                                                   h∈H
                                                f
                yh = 1                 ∀h ∈ H                                         xhc ≥ 0                ∀h ∈ H, c ∈ C
                                                                                      yh ∈ {0, 1}            ∀h ∈ H
                 X
                     thc xhc ≤ T       ∀c ∈ C
                h∈H

                xhc ≥ 0                ∀h ∈ H, c ∈ C
                zhc ∈ {0, 1}           ∀h ∈ H, c ∈ C
                yh ∈ {0, 1}            ∀h ∈ H

The two formulations
            P          differ in how the demand of a region may be met. In the Inefficient formulation, the assignment
constraint h∈H zhc = 1 together with the big-M constraint xhc ≤ M zhc forces each region c ∈ C to be served in
full by a single hub. The Efficient formulation has no such restriction; a region can be supplied by a combination of
multiple hubs simultaneously.
Proposition F.8. The Inefficient and Efficient formulations of UNHDR are not related by a constructive reformulation
(Definition 4.4) in either direction under the identity parameter mapping Φp .


Proof. Consider the instance p with H = {1, 2}, H f = ∅, C = {c}, ac = 1, n = 2, costs C1c = 0, C2c = 1, travel
times t1c = 2, t2c = 0, response time limit T = 1, and any M ≥ 1. Let Veff (p) and Vineff (p) denote the objective values
attained on p by the Efficient and Inefficient formulations respectively.
In the Efficient formulation, open both hubs (y1 = y2 = 1). The point x1c = λ, x2c = 1 − λ is feasible for every
λ ∈ [0, 21 ] (the response time constraint reads 2λ ≤ 1) and attains objective value 1 − λ. Hence Veff (p) ⊇ [ 12 , 1] is
uncountable.
In the Inefficient formulation, assigning region c to hub 1 (z1c = 1) forces x1c = 1 and violates the response time
constraint t1c x1c = 2 > 1 = T . Hence the only feasible assignment is z2c = 1, which forces x2c = 1 and y2 = 1,
attaining objective value 1. Thus Vineff (p) = {1}.
Suppose that a constructive reformulation between the two formulations with Φp the identity exists. By Lemma F.6,
|Veff (p)| = |Vineff (p)| regardless of which formulation is the source. But Veff (p) is uncountable while |Vineff (p)| = 1, a
contradiction.


F.2.3     World Food Program (WFP)
This problem consists of designing a food distribution plan for the World Food Program (WFP) to deliver commodities
from suppliers, through transshipment points, to beneficiary camps in crisis-affected regions. The plan must satisfy each
camp’s ration demand and meet per-person nutritional requirements across all nutrients. The objective is to minimize
the total procurement and transportation cost. Ferchtandiker et al. [16] introduces the following formulations of this
problem.
Notation.
   • K: set of commodities.
   • L: set of nutrients.
   • pck is the procurement cost per kg of commodity k.1
   • nutvalkℓ : nutrient-ℓ content (per kg) of commodity k ∈ K.
   • nutreqℓ : per-person requirement for nutrient ℓ ∈ L.
   • demj : number of beneficiaries at camp j.
   • Rk ≥ 0: ration size (kg per person) of commodity k ∈ K.
   1
       In the dataset, the variable qk is used for procurement cost in the inefficient formulation. We use pck for both formulations.


                                                                         26
                               FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



Formulations. The Efficient formulation is node-based: N is the set of nodes, partitioned into suppliers NS , transship-
ment points NT , and beneficiary camps NB . Eij ∈ {0, 1} indicates whether an edge from i to j exists and we have a
transportation cost tcijk ≥ 0 per kg of commodity k on edge (i, j). Edges run only from suppliers to transshipment
points, between transshipment points, and from transshipment points to beneficiary camps; that is, Eij = 1 only if
                                        (i, j) ∈ (NS × NT ) ∪ (NT × NT ) ∪ (NT × NB ).
The decision variable Fijk ≥ 0 encodes the amount of commodity k shipped from i to j. The Inefficient formulation is
path-based: P is the set of all simple paths from a supplier to a beneficiary camp. The indicator ejp ∈ {0, 1} indicates
whether path p ends at camp j and cpk is the cost of shipping one kg of commodity k along path p. The decision
variable xpk ≥ 0 is the amount of commodity k shipped along path p.
                                                                                                                  
          X             X                                                               X             X
  min           pck          xpk  +                                          min           pck          demj Rk  +
          k∈K           p∈P                                                            k∈K        j∈NB
            X X                                                                           X       X
                        cpk xpk                                                                       tcijk Fijk
           p∈P k∈K                                                                       i,j∈N k∈K
          X                                                                            X                  X
   s.t.         ejp xpk ≥ demj Rk       ∀j ∈ NB , k ∈ K   (Inefficient)         s.t.         Eij Fijk =         Eji Fjik   ∀j ∈ NT , k ∈ K
          p∈P                                                                          i∈N                i∈N
                                                                                                                                              (Efficient)
          X                                                                            X
                nutvalkℓ Rk ≥ nutreqℓ   ∀ℓ ∈ L                                               Eij Fijk ≥ demj Rk            ∀j ∈ NB , k ∈ K
          k∈K                                                                          i∈N

          xpk ≥ 0                       ∀p ∈ P, k ∈ K
                                                                                        X
                                                                                             nutvalkℓ Rk ≥ nutreqℓ         ∀ℓ ∈ L
          Rk ≥ 0                        ∀k ∈ K                                         k∈K

                                                                                       Fijk ≥ 0                            ∀i, j ∈ N, k ∈ K
                                                                                       Rk ≥ 0                              ∀k ∈ K

Both WFP formulations are polynomially-solvable linear programs, but our constructive reformulation definition is only
meaningful on NP-hard formulations (Remark 4.5). Despite this, FLARE still identified two inconsistencies between the
pair of WFP formulations.
                                                                                         P        P
   • Misaligned objectives. In the Efficient formulation, the procurement cost term k pck j∈NB demj Rk de-
                                                                        P
     pends only on the ration size Rk , while the demand constraint i Eij Fijk ≥ demj Rk permits shipping in
     excess ofPdemj Rk without additional procurement penalty. In the Inefficient formulation, the procurement cost
     P
        k pck    p xpk instead depends on the total amount shipped, so any slack in the demand constraint is charged.
   • Cycles. In the Efficient formulation, we have flow variables Fijk . A feasible point could have positive flow on
     a cycle of transshipment points. However, in the Inefficient formulation, P is the set of all simple paths from a
     supplier to a beneficiary camp. A feasible point necessarily has acyclic flow on each commodity.
Notably, these inconsistencies are only realized on sub-optimal feasible points. An optimal point will not ship
excess demand nor send flow on a cycle. While the Efficient formulation is an Audet reformulation of the Inefficient
formulation, our stricter constructive reformulation definition imposes conditions across the entire feasible region.
We modify WFP to resolve these inconsistencies for inclusion in FormulationBench and make the problem NP-hard by
restricting to integral flows and adding transhipment throughput capacities.




                                                                          27
                        FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



G       Experiment Details
Dataset. All experiments were run on v0.5.0 of the formulation-bench Python package which pins the dataset to
v0.4.0. See Appendix E and the package documentation for details.
FLARE agent harness. Experiments were conducted on a MacBook Pro (Apple M3 Pro, 12-core CPU, 18 GB unified
memory) running macOS 15.7.1. We evaluate FLARE on the following agent harnesses:

          • Claude Code. Version 2.1.197 with Claude Code Max subscription ($100/month)
          • Codex. Version 0.147.0 with ChatGPT Pro subscription ($100/month)
          • OpenCode. Version 1.18.15 (open-source)

We used Claude Code and ChatGPT subscriptions in order to avoid higher API costs. The FLARE experiments can be
run within the weekly usage limits but must be batched in order to avoid the 5 hour Claude Code session limit.
FLARE compute. FLARE runs in a Docker container with a 30 minute time limit. The image is built on Ubuntu 24.04
with Python 3.12 and Node 20. It contains the three agent CLIs above, the Lean toolchain (elan 4.2.3 and Lean 4.28.0,
with mathlib pinned to v4.28.0), and the lean-lsp-mcp 0.29.0 MCP server. To allow for increased parallelization,
we run each FLARE in its own Modal1 Sandbox. Each Sandbox is allocated a guaranteed floor of 2 CPU cores (it may
burst higher) and 4 GiB of memory. Modal compute costs are excluded from the reported average costs. The compute
costs of the FLARE experiments falls below the $30/month compute provided for free.

Table 5: Standard API rates (USD per million tokens) used to compute the reported average costs. Input is the uncached (cache-miss)
rate and Cached Input the cache-hit rate; cache writes (billed at 1.25× input by Anthropic) are not modeled. GPT-4.1 publishes no
cached rate, so its cached tokens are billed at the input rate. DeepSeek uses preview release rates prior to the 8-16-26 price increase.
                        Model                   API Identifier             Input    Cached Input       Output
                        Opus 5                  claude-opus-5             $5.000           $0.5000      $25.00
                        Sonnet 5                claude-sonnet-5           $2.000           $0.2000      $10.00
                        GPT-5.6 Sol             gpt-5.6-sol               $5.000           $0.5000      $30.00
                        GPT-5.6 Terra           gpt-5.6-terra             $2.000           $0.2000      $12.00
                        GPT-4.1                 gpt-4.1                   $2.000                —        $8.00
                        DeepSeek V4 Pro         deepseek-v4-pro           $0.435           $0.0036       $0.87
                        DeepSeek V4 Flash       deepseek-v4-flash         $0.140           $0.0028       $0.28

LLMs. Anthropic and OpenAI models are served through the Stanford AI API Gateway2 at a discounted price. The
reported average costs are computed using the standard API rates at the time of experimentation (Table 5). The gateway
only supports structured output on OpenAI models (if reasoning is enabled). For Anthropic and DeepSeek models, we
append the response schema to the prompt and configure retry logic if the response isn’t parseable. We specify a max
token budget of 8192 when reasoning is disabled and 16384 when reasoning is enabled. We use medium effort for
Anthropic and OpenAI models and high effort for DeepSeek models. We found these settings produce comparable
reasoning efforts across model families. DeepSeek models reason for longer, but high is the lowest effort available.
When a model exhausts its token budget before emitting a verdict, we count the truncated response as a judgment of not
a reformulation; this occurs only for DeepSeek V4 Pro, on 22 of its 486 ablation runs.




    1
        https://modal.com
    2
        https://uit.stanford.edu/service/ai-api-gateway


                                                                  28
                        FLARE: Verifying MILP Reformulations with LLM-Based Theorem Proving



H    Additional Results

Table 6: Evaluation of FLARE across agent harnesses and LLM models. Accuracy results on the FormulationBench dataset are
provided in aggregate and segmented by source dataset. Metric cells report results from a single run and Bold indicates the best
method on a metric. The Claude Code harness with Opus 5 is the only configuration with 100% accuracy. Codex with GPT-5.6 Sol
misses one pair. The open-source OpenCode harness with DeepSeek V4 Pro is an order of magnitude cheaper, but is substantially
slower and less accurate. All 11 false negatives are attributable to ATP failure, 8 due to timeout limits (Appendix G).
              Harness       Model               Effort       TP       FP       TN    FN   Precision    Recall    Accuracy    Avg. Time    Avg. Cost
              Overall
              Claude Code Opus 5       medium                42        0       12     0     100.0%    100.0%      100.0%        410.6s      $1.180
              Codex       GPT-5.6 Sol  medium                41        0       12     1     100.0%     97.6%       98.1%        398.1s      $1.185
              OpenCode DeepSeek V4 Pro high                  31        0       12    11     100.0%     73.8%       79.6%       1366.9s      $0.127
              EquivaFormulation [68] (p2, p3)
              Claude Code Opus 5       medium                10        0        8     0     100.0%    100.0%      100.0%        229.8s      $0.628
              Codex       GPT-5.6 Sol  medium                10        0        8     0     100.0%    100.0%      100.0%        253.6s      $0.722
              OpenCode DeepSeek V4 Pro high                  10        0        8     0     100.0%    100.0%      100.0%        370.7s      $0.031
              EvoCut [66] (p6, p8–p12)
              Claude Code Opus 5       medium                25        0        3     0     100.0%    100.0%      100.0%        413.4s      $1.116
              Codex       GPT-5.6 Sol  medium                25        0        3     0     100.0%    100.0%      100.0%        478.1s      $1.436
              OpenCode DeepSeek V4 Pro high                  17        0        3     8     100.0%     68.0%       71.4%       1874.2s      $0.171
              Ferchtandiker et al. [16] (p13–p20)
              Claude Code Opus 5       medium                 7        0        1     0     100.0%    100.0%      100.0%        807.5s      $2.645
              Codex       GPT-5.6 Sol  medium                 6        0        1     1     100.0%     85.7%       87.5%        443.6s      $1.348
              OpenCode DeepSeek V4 Pro high                   4        0        1     3     100.0%     57.1%       62.5%       1833.0s      $0.187




Table 7: Evaluation of FLARE-NL across LLM models and reasoning effort levels. Results show FLARE-NL evaluated on the
FormulationBench dataset TSP problem. Metric cells report mean ± std. dev. across 3 runs; TP/FP/TN/FN reports totals. Every
model achieves perfect accuracy with reasoning enabled; performance without reasoning varies widely across model families. To
reduce costs, we only evaluate the leading frontier reasoning model from each provider in the ablation study (Table 3).
              Model                 Effort      TP   FP      TN       FN            Precision         Recall      Accuracy    Avg Time    Avg Cost
              Reasoning Disabled
              Opus 5                            15       0        9     0      100.0±0.0%       100.0±0.0%      100.0±0.0%        22.2s     $0.062
              Sonnet 5                          15       0        9     0      100.0±0.0%       100.0±0.0%      100.0±0.0%        38.9s     $0.042
              GPT-5.6 Sol                       15       0        9     0      100.0±0.0%       100.0±0.0%      100.0±0.0%         6.9s     $0.020
              GPT-5.6 Terra                     12       0        9     3      100.0±0.0%       80.0±20.0%      87.5±12.5%         5.2s     $0.008
              GPT-4.1                            0       0        9    15               —         0.0±0.0%       37.5±0.0%         6.5s     $0.008
              DeepSeek V4 Pro                    7       0        9     8      100.0±0.0%       46.7±11.5%       66.7±7.2%         6.4s     $0.001
              DeepSeek V4 Flash                  7       1        8     8      91.7±14.4%       46.7±23.1%      62.5±12.5%         5.0s    $0.0004
              Reasoning Enabled
              Opus 5                medium      15       0        9        0   100.0±0.0%       100.0±0.0%      100.0±0.0%        16.5s     $0.049
              Sonnet 5              medium      15       0        9        0   100.0±0.0%       100.0±0.0%      100.0±0.0%        23.4s     $0.029
              GPT-5.6 Sol           medium      15       0        9        0   100.0±0.0%       100.0±0.0%      100.0±0.0%        12.8s     $0.027
              GPT-5.6 Terra         medium      15       0        9        0   100.0±0.0%       100.0±0.0%      100.0±0.0%        10.6s     $0.012
              DeepSeek V4 Pro       high        15       0        9        0   100.0±0.0%       100.0±0.0%      100.0±0.0%        65.8s     $0.005
              DeepSeek V4 Flash     high        15       0        9        0   100.0±0.0%       100.0±0.0%      100.0±0.0%        46.3s     $0.002




                                                                                     29
