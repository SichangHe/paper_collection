                                             Beyond Objective Equivalence: Constraint Injection for LLM-Based
                                                    Optimization Modeling on Vehicle Routing Problems

                                                 Xizi Luo1,3 , Changhong He2,3 , Dongdong Geng3 , Chenggong Shi3 , Yu Mei3 *
                                                  1
                                                    School of Economics and Management, Beihang University, Beijing, China
                                            2
                                              School of Mechanical Engineering and Automation, Beihang University, Beijing, China
                                                                          3
                                                                            Baidu Inc., Beijing, China



                                                              Abstract                                             Input Natural-Language Problem
                                                                                                    Prompt: Write a Gurobi script to dispatch one drone from base 0
                                            Large language models (LLMs) can generate               to visit 4 towers exactly once and return, ensuring a single
                                                                                                    continuous tour. Coordinates (x, y) on a 100 × 100 plane: depot 0 =
arXiv:2606.04816v2 [cs.AI] 5 Oct 2026




                                            executable solver code from natural-language
                                                                                                    (50, 50), tower 1 = (18, 48), tower 2 = (48, 12), tower 3 = (85, 42),
                                            descriptions of optimization problems. How-             tower 4 = (56, 79). Minimize total distance.
                                            ever, existing verification signals focus on             Reference Optimum: {0→1→2→3→4→0} Obj: 203.18
                                            whether the generated formulation produces
                                            the correct objective value. Such signals can                        LLM-Generated Candidate Code
                                            overlook constraint-level errors: incorrect for-              Generated During Data-synthesis or RL rollouts
                                            mulations may still produce the same optimum             x = m.addVars(N, N, vtype=GRB.BINARY)
                                                                                                     m.setObjective(x.prod(d), GRB.MINIMIZE)
                                            when extra or missing constraints do not af-             m.addConstrs(x.sum(i, '*') == 1 for i in range(N))
                                            fect the tested instance. We propose constraint          m.addConstrs(x.sum('*', j) == 1 for j in range(N))
                                                                                                     # ... remaining implementation omitted
                                            injection, a verification method that directly
                                            tests whether the generated code implements                      Critical Bug: Omitted subtour elimination

                                            the intended constraints. We use feasible so-
                                            lutions to detect incorrectly added constraints        Optimal Value Check: Opt Only        +Constraint Injection: Opt+Inj
                                            and one-constraint-violating solutions to detect        Reference Obj = 203.18               Opt: Δ = 0 → Pass
                                                                                                    Candidate Obj = 203.18               Inj: An infeasible subtour
                                            omissions. Together with the optimal value              Opt: Δ = 0 → Pass                    {0→2→0, 1→4→3→1}
                                            check, these tests verify both the objective and        → Accept candidate ✓                 Reference: infeasible
                                                                                                                                         Candidate: feasible
                                            the constraint set. We evaluate this approach on                                             → Reject candidate ×
                                                                                                     Accepted bug → SFT/RL noise
                                            vehicle routing problems (VRPs), which pro-                 Bug enters supervision           Bug blocked before supervision
                                            vide a challenging testbed with diverse, tightly
                                            coupled operational constraints. We develop                       Optimal Value Check is not enough.
                                            VRPCoder, an 8B model for generating Gurobi
                                            code from natural-language VRP descriptions,           Figure 1: A candidate missing the subtour-elimination
                                            and VRPBench, an expert-verified benchmark             constraint still matches the reference optimal value, so
                                            spanning 21 VRP variants across four subsets.          the optimal value check accepts it. Constraint injection
                                            The verifier serves as a rejection-sampling cri-       injects a disconnected-subtour solution: correct code re-
                                            terion for synthetic data construction and as a        jects it as infeasible, while the buggy candidate accepts
                                            rollout-level reward for reinforcement learning        it, exposing the missing constraint.
                                            (RL). On VRPBench, VRPCoder-RL reaches
                                            93% overall Pass@1, outperforms Gemini-3.1-
                                            Pro Preview on three subsets, exceeds Claude-          verifying the correctness of the generated formula-
                                            Sonnet-4.5 by 28 percentage points, and ex-            tion remains difficult: code that runs successfully
                                            ceeds the strongest prior OR-LLM by 78 per-            and produces the expected objective value may still
                                            centage points.                                        fail to faithfully encode the intended constraints.
                                        1    Introduction                                          Such errors are particularly concerning in optimiza-
                                                                                                   tion modeling, where an incorrect constraint set
                                        Optimization problems are often described in natu-         can yield seemingly valid solutions while misrep-
                                        ral language, but solving them requires translating        resenting the original problem.
                                        these descriptions into formal mathematical models            Existing LLM-based optimization model-
                                        and executable solver code (Ramamonjison et al.,           ing methods mainly fall into three categories.
                                        2022). Large language models (LLMs) provide a              Inference-time enhancement methods improve
                                        promising way to automate this process. However,           frozen LLMs via prompting, retrieval, self-
                                            * Corresponding author: whqyqy@hotmail.com             debugging, or agentic workflows (Jiang et al.,

                                                                                               1
2025c; Li et al., 2025; Zhang et al., 2026). Super-         jection, a constraint-level verifier that uses feasible
vised fine-tuning (SFT) trains operations research          solutions to detect spurious over-constraints and
LLMs (OR-LLMs) on synthetic problem–code                    one-constraint-violating solutions to detect silent
pairs, often filtered by executability, optimal value       omissions, and combine it with the optimal value
checks, or self consistency (Huang et al., 2025a;           check into a dual verifier reused for data synthesis
Lu et al., 2025; Zhang et al., 2025). Reinforcement         and RL. (3) We introduce VRPCoder together with
learning (RL) methods use solver feedback such              VRPBench, an expert-verified benchmark covering
as objective matching or answer agreement (Chen             21 VRP variants across four subsets. VRPCoder-
et al., 2025; Zhou et al., 2026; Ding et al., 2026).        RL reaches 93.00% overall Pass@1 on VRPBench,
Despite their differences, both SFT filtering and           outperforms Gemini-3.1-Pro Preview on three sub-
RL rewards often reduce to objective equivalence,           sets, and substantially outperforms Claude-Sonnet-
typically assessed by comparing optimal objective           4.5 and prior OR-LLMs.
values.
   However, objective equivalence does not guaran-          2     Related Work
tee constraint fidelity. A generated formulation can
                                                            2.1    Supervised Fine-Tuning of OR-LLMs
match the reference optimum even if it adds redun-
dant constraints or omits required ones, provided           Data synthesis has been widely adopted to train OR
that the affected constraints are non-binding on the        LLMs (Xiao et al., 2025). ORLM (Huang et al.,
tested instance. We call these two failure modes            2025a) expands industry-case seeds with GPT-4;
spurious over-constraint and silent constraint omis-        OptMATH (Lu et al., 2025) generates complexity-
sion. Since both can survive executability and opti-        controlled problems and filters them via bidirec-
mal value checks, they can contaminate SFT data             tional re-modeling; LLMOPT (Jiang et al., 2025a)
and be rewarded during RL. Figure 1 shows such a            defines a five-element unified formulation for multi-
case in a routing instance where the omission of a          instruction tuning; ReSocratic (Yang et al., 2025)
subtour-elimination constraint leaves the optimum           derives problem–code pairs from structured demon-
unchanged.                                                  strations. Across many such pipelines, sample veri-
   We address this gap with constraint injection,           fication relies mainly on executability, re-modeling
a verification operator that checks whether gener-          consistency, or objective equivalence. While useful
ated code accepts a feasible solution and rejects           for filtering invalid or clearly incorrect code, such
one-constraint-violating solutions. Combined with           signals do not verify whether the generated code
the optimal value check, it forms a dual verifier           faithfully implements the intended constraints, and
whose constraint-level signal is decoupled from the         can therefore miss constraint omissions that leave
optimum on any single instance. We instantiate the          the optimum unchanged.
dual verifier on vehicle routing problems (VRPs),
                                                            2.2    Reinforcement Learning for OR-LLMs
a constraint-dense testbed whose capacities, time
windows, depots, and service rules are coupled into         Beyond SFT, RL with solver-based verifiable re-
natural-language scenarios (Toth and Vigo, 2014;            wards has become a natural direction for OR-
Laporte, 2009; Lahyani et al., 2015). The verifier          LLMs, since generated code can be executed,
is reused first as a rejection-sampling filter during       solved, and evaluated by feasibility, objective
data synthesis and then as a per-rollout reward dur-        values, or answer agreement (Le et al., 2022).
ing RL. The resulting model, VRPCoder, is an 8B             SIRL (Chen et al., 2025) uses solver execution
end-to-end model that translates natural-language           as outcome feedback, FOARL (Jiang et al., 2025b)
VRP scenarios into Gurobi code, accompanied by              introduces feasibility-and-optimality-aware RL for
VRPBench1 , an expert-verified benchmark cover-             combinatorial optimization, StepORLM (Zhou
ing 21 VRP variants across four subsets.                    et al., 2026) uses a generative process reward
   Our contributions are as follows: (1) We iden-           model for step-wise supervision, and OR-R1 (Ding
tify objective equivalence as a shared blind spot           et al., 2026) performs test-time group relative pol-
of SFT data filtering and RL rewards, with two              icy optimization (GRPO) using majority-voting
failure modes: spurious over-constraint and silent          pseudo-labels as the reward. Although these re-
constraint omission. (2) We propose constraint in-          wards improve OR reasoning beyond SFT, they
                                                            mainly operate at the solution or answer level and
   1
       https://github.com/ccccziiii/VRPBench                do not directly verify whether each required con-

                                                        2
straint is implemented in the generated code. For             with customer set N = {1, . . . , n}, depot node
constraint-dense VRP solver-code generation, re-              0, node set V = N ∪ {0}, vehicle set M , and
warding constraint-level correctness beyond solver            arc set A. Each customer i has demand di , each
outcomes or answer agreement remains underex-                 vehicle has capacity Q, and each arc (i, j) has cost
plored.                                                       cij . Let xkij ∈ {0, 1} indicate whether vehicle k
                                                              traverses arc (i, j), and let vi ∈ [1, n] denote the
2.3    LLMs for Vehicle Routing Problems                      position of customer i in its route. The CVRP
VRP is a representative testbed for LLM-based                 minimizes total routing cost (2) subject to: each
optimization modeling under coupled constraints.              customer is visited exactly once (3), each vehicle
NLCO (Jiang et al., 2026) benchmarks LLM rea-                 departs at most once (4), flow conservation (5),
soning on natural-language combinatorial optimiza-            vehicle capacity (6), and subtour elimination via
tion including routing tasks; Huang et al. (2024)             Miller–Tucker–Zemlin (MTZ) ordering (7):
show that general-purpose LLMs exhibit prelimi-
                                                                                              X X
nary VRP code-generation ability but remain lim-                                   min                       cij xkij ,   (2)
ited under complex constraints. Another line of                                               k∈M (i,j)∈A
work improves VRP solving through inference-                         X        X
time mechanisms: DRoC (Jiang et al., 2025c) com-                                       xkij = 1,      ∀i ∈ N,             (3)
                                                                     k∈M j:(i,j)∈A
bines constraint decomposition with retrieval and                            X
self-debugging, while ARS (Li et al., 2025) and                                        xk0j ≤ 1,      ∀k ∈ M,             (4)
AFL (Zhang et al., 2026) adopt agentic workflows                         j:(0,j)∈A
over frozen LLMs. These studies do not directly                               X
                                                                                       xkij =
                                                                                                   X
                                                                                                             xkji ,       (5)
address whether generated solver code faithfully
                                                                          j:(i,j)∈A              j:(j,i)∈A
encodes intended constraints; this is the focus of
our work.                                                                                       ∀i ∈ V, k ∈ M,
                                                                       X            X
                                                                             di               xkij ≤ Q,      ∀k ∈ M,      (6)
3     Preliminaries                                                    i∈N        j:(i,j)∈A
                                                                                      X
3.1    Problem Definition                                           vi − v j + n              xkij ≤ n − 1,               (7)
We formulate the task of automated optimization                                      k∈M
modeling: given a natural-language problem de-                                                  ∀i, j ∈ N, i ̸= j.
scription p, an LLM generates solver code y that
produces an optimal solution and its optimal value               VRP variants. We extend CVRP with constraint
upon execution:                                               modules such as time windows, pickup-delivery,
                                                              backhauls, multi-depot, heterogeneous fleets, and
        y = LLM(p),      (s∗ , z ∗ ) = Solve(y)    (1)        open routes, yielding 21 variants in total: 18 used
where s∗ denotes the optimal solution and z ∗ the             for training and 3 held out for generalization testing.
corresponding optimal value. A correct y must (1)             Full mapping is provided in Appendix A.
produce a feasible optimal solution with the correct
                                                              3.3   Abstract and Concrete Code
optimal value z ∗ and (2) faithfully encode the ex-
plicit constraints in p together with the implicit con-       To enable scalable data synthesis, we decompose
straints of the corresponding problem variant. We             Gurobi solver code into two layers based on the
use objective equivalence to denote agreement in              observation that a VRP instance is fully determined
the optimal objective value between generated and             by a parameter set (nodes, vehicles, demands, ca-
reference code on the same instance; such agree-              pacities, costs, and variant-specific fields such as
ment alone does not guarantee faithful constraint             time windows or fleet attributes).
encoding. In this work, y is instantiated as Gurobi
                                                              Abstract code Cabsv . For each variant v, an OR
solver code for VRPs.
                                                              expert writes a Gurobi code template that defines
3.2    Vehicle Routing Problem                                the decision variables, constraints, and objective,
The Capacitated Vehicle Routing Problem                       with instance-specific parameters left as inputs.
(CVRP) (Braekers et al., 2016) is adopted as the                 v serves as the reusable template for variant
                                                              Cabs
foundation for VRP variants. Consider a graph                 v.

                                                          3
                                     v with a
Concrete code Ccon . Instantiating Cabs                        Stage 1: Code Instantiation and Solution Construction

sampled parameter set ξ ∼ Pv yields executable                                                    Solution                        '$()#$% *+! *,+"& -
                                                                !"#"$%&%#                       Construction
                                                                                                                         "!
concrete code:                                                                       $"%&!"#
                                                                           !
                                                                    %&'(   "#$                                           #$!" %
                    v
            Ccon = Cabs (ξ),     ξ ∼ Pv            (8)
                                                               Stage 2: Back-Translation and Code Regeneration
   where Pv is the parameter distribution for variant                     Teacher                  Teacher                               !"#
                                                                                                                                   &'(%)"$%#
                                                                           LLM                      LLM
                                                                                     !"#$%&' {(}
                                                                                                                         !"#
v. Since each ξ yields a distinct instance, arbitrarily         $"%&!"#                                        &%'"      $%#

many Ccon can be generated from a single template.
                                                                                                )*+,-*./0" 1 ( /23'4"&'# 23'4"&'#
                                                                                                                              !"#
                                                                                                                                  25$ 265 %( 7 )
4     Method
                                                               Stage 3: Dual-Verified Rejection Sampling
4.1   Overview
                                                                                    Dual        &'( ( )%*"$%#
                                                                                                          !"#
                                                                                                              +)%*"$%# )
                                                                                 Verification                                        !"#$%"&'()*+,"
Our framework consists of a data synthesis pipeline            !"#$%"&'()
and a training pipeline. In the data synthesis                                                  )#* ( +',"   !"#
                                                                                                             &'#   -. -/. 0 )
                                                                                                                     $    %
                                                                                                                          (


pipeline, we instantiate expert-written abstract code
into concrete code, construct feasible and one-               Figure 2: Overview of the three-stage data synthesis
constraint-violating solutions, back-translate the            pipeline.
concrete code into natural-language problems, and
regenerate solver code with a teacher LLM. Each               vehicle when no extension satisfies capacity or dis-
generated sample is then filtered by the dual veri-           tance limits, and inserts any remaining customers
fier, which jointly applies the optimal value check           into routes with the largest slack. If the heuris-
and the constraint injection check. In the training           tic fails to produce a feasible solution, we replace
pipeline, accepted samples are first used for SFT;            the objective of Ccon with a constant and invoke
the same dual verifier is then reused as the reward           Gurobi to return any feasible solution under a short
signal during RL with GRPO. The following sec-                time limit.
tions detail each component.
                                                              Infeasible solutions {s−  i }. For each variant v,
4.2   Data Synthesis Pipeline
                                                              we define a set of perturbation operators Av that
Figure 2 summarizes our data synthesis pipeline.              perturb s+ into infeasible solutions {s−          −
                                                                                                     i }. Each si
Stage 1: Code Instantiation and Solution Con-                 violates exactly one class of constraints while sat-
struction. For each of the 18 training variants, we           isfying all others, which we term a one-constraint-
sample multiple parameter sets and substitute them            violating solution. This design isolates the effect
        v , producing multiple concrete code in-
into Cabs                                                     of specific categories of constraints, enabling the
stances {Ccon } per abstract template. Specifically,          model to learn fine-grained feasibility reasoning.
each instance is parameterized by customer count              The operators fall into two categories depending
|N |, vehicle count |M |, customer coordinates, and           on whether they modify the parameters of Ccon .
base demand range. Variant-specific parameters
                                                                 • Structural perturbations (Astruct
                                                                                               v     ) keep all pa-
such as capacities, time windows, distance limits,
                                                                   rameters of Ccon unchanged and perturb s+
and fleet types are then derived accordingly. We
                                                                   alone, introducing a local structural change
define 12 regular scale profiles and 3 boundary
                                                                   that renders the resulting s−
                                                                                               i infeasible with
profiles that test extreme geometric layouts, tight
                                                                   respect to exactly one class of constraints.
capacities, and narrow time-resource budgets. Pa-
                                                                   They are applicable to specific categories of
rameters are randomly sampled or selected under a
                                                                   constraints—subtour elimination, precedence,
fixed random seed per instance (see Appendix B.1
                                                                   and coverage—whose violations are deter-
and Appendix B.2). We then construct a feasible
                                                                   mined by solution topology alone, indepen-
solution s+ and a set of infeasible solutions {s−i }               dent of numerical parameters such as capaci-
for each Ccon as follows.
                                                                   ties or time windows. Figure 3(a) illustrates
Feasible solution s+ . We construct s+ with a                      a CVRP example: the subtour cycle opera-
greedy nearest-neighbor heuristic that, starting                   tor removes the depot connections from route
from a depot, iteratively appends the closest fea-                 0 → 3 → 4 → 5 → 0 to form the closed cycle
sible customer to the current route, opens a new                   3 → 4 → 5 → 3, which disconnects these nodes

                                                          4
               (a) Structural Perturbation：Subtour Cycle                                      that a single Ccon yields multiple training sam-
     Original Feasible Solution            Constraint-Violating Solution                      ples: (1) Scenario Instantiation (core path) builds
                             1                                        1

      6                                        6
                                                                                              a baseline problem p0 across 60 scenarios via a
                                 5
                         0                                       0        5                   generate–critique–repair loop (Lu et al., 2025);
                                     4                                            4
                                                                                              (2) Condensation (augmentation) eliminates solver-
      2                                        2

                     3                                       3
                                                                                              exclusive modeling elements or simplifies business
    V a lid path 1       0 →2 →6 →1→0       V a lid path 1           0 →2 →6 →1→0             expressions, producing a concise pcond ; (3) Index
    V a lid path 2       0 →3 →4 →5 →0     I n valid path 2           3 →4 →5 →3
                                                                                              Rewriting (augmentation) varies node-ID conven-
              (b) Parameter Perturbation ：Move Overload                                       tions, producing pidx (Jiang et al., 2026). Subse-
     O riginal Feasible Solution         C onstraint-Violating Solution                       quently, the same teacher maps each p to a tar-
                             1                                   1                                         gen
                                                                              Tightened
                                                                               Capacity
                                                                                              get code Ccon    , which serves as the SFT ground
      6                                    6                                    17.48                          gen
                         0
                                 5
                                                             0
                                                                                              truth. Using Ccon     rather than Ccon as the training
                                                                              5
                                                                                              target introduces cross-sample diversity in code
                                     4                                        4
      2                                    2
                                                       3
                                                                                              structure. Accordingly, each sample now takes the
                     3                                                                                             gen
    V a lid path 1     0 →2 →6 →1→0       I n valid path 1 0 →2 →6 →1→5 →0
                                                                                              form (p, Ccon , Ccon     , s+ , {s−
                                                                                                                                i }). Detailed back-
                L o ad: 14.5                            L o ad: 18.0
    V a lid path 2      0 →3 →4 →5 →0       Valid path 2     0→3→4→5→0                        translation procedures and prompts are provided in
                 L o ad: 16.1                          Load: 12.6
                                                                                              Appendix C and Appendix H.
Figure 3: Two illustrative perturbation operators: (a)                                        Stage 3: Dual-Verified Rejection Sampling.
Subtour Cycle (structural perturbation); (b) Move Over-                                               gen
                                                                                              Since Ccon  is generated by the teacher LLM rather
load (parameter perturbation).
                                                                                              than derived from verified templates, it may con-
                                                                                              tain modeling errors. To filter out incorrect sam-
      from the depot and thereby violates the MTZ                                             ples, we apply a dual verification mechanism that
                                                                                                             gen
      subtour elimination constraints (Eq. (7)).                                              checks each Ccon   with two complementary checks
                                                                                              against the ground-truth Ccon and the solution set
   • Parameter perturbations (Aparam
                                   v     ) construct                                          S = {s+ } ∪ {s−    m
                                                                                                              i }i=1 .
     s−i by modifying s + together with the relevant
                                                                                              Optimal value check Opt. Let z ∗ (C) denote the
     parameter settings in Ccon , producing a per-
                                                                                              optimal value returned by executing code C. We in-
     turbed concrete code C̃con . They are needed                                                                       gen
                                                                                              dependently solve both Ccon   and the ground-truth
     for resource-bound categories of constraints—
                                                                                              Ccon , then compare their optimal values:
     capacity, distance, compartment, and hard
     time windows—where s+ leaves slack under                                                       gen
                                                                                               Opt(Ccon , Ccon ) ≜ |z ∗ (Ccon
                                                                                                                          gen
                                                                                                                              ) − z ∗ (Ccon )| . (9)
     the original parameters, so structural changes
     alone may not trigger infeasibility. The rel-                                            The check passes if Opt ≤ εobj , where εobj is a
     evant parameter settings are adjusted so that                                            small numerical tolerance accounting for floating-
                                                                                                                                       gen
     s+ remains feasible under C̃con while s−  i be-                                          point differences in solver outputs; if Ccon fails to
     comes infeasible. Figure 3(b) illustrates a                                              compile or yields an infeasible model, the check
     CVRP example: the move overload operator                                                 fails immediately. However, matching the optimal
     moves customer 5 between routes, changing                                                value alone cannot guarantee faithful constraint
                                                                                                              gen
     route loads from (14.5, 16.1) to (18.0, 12.6),                                           encoding in Ccon    . This motivates the following
     and adjusts capacity to Q̃ = 17.48 so that s+                                            constraint injection check.
     stays feasible while s−
                           i violates Eq. (6).                                                Constraint injection check Inj. Given gener-
                                                                                                          gen
   Across the 18 training variants, our operator cat-                                         ated code Ccon  , constraint injection checks whether
alogue contains 5 structural and 7 parameter per-                                             the encoded constraints are consistent with the la-
turbation operators in total. Per-variant parameter                                           beled solutions S constructed from Ccon . Specif-
ranges and the full operator catalogue are listed in                                          ically, we do not modify the constraints origi-
                                                                                                                       gen
Appendices B.2 and B.4, respectively.                                                         nally generated by Ccon      , but replace the objec-
                                                                                              tive function with a constant and, for each so-
Stage 2: Back-Translation and Code Regenera-                                                  lution s ∈ S, append arc-level constraints Φ(s)
tion. A teacher LLM back-translates each Ccon                                                 via Gurobi addConstr calls so that the solver an-
into a set of natural-language problems {p} via                                               swers a pure feasibility query. Let the ground-
one core path and two augmentation paths, so                                                  truth label be ℓ(s), where ℓ(s+ ) = Feasible and

                                                                                          5
ℓ(s−
   i ) = Infeasible. The constraint injection check           both s+ and {s−                 s
                                                                            i } instead use xuv
                                                                                                   κ (u,v)
                                                                                                     = 1 for ev-
passes if and only if:                                        ery used customer arc (u, v), where κs (u, v) is its
                                                              assigned vehicle in s; unused arcs and unserved
               gen
          Inj(Ccon , s) = ℓ(s),    ∀ s ∈ S.       (10)        customers are handled as above, with details in
                                                              Appendix D.
   Recall that N denotes the customer set and V
denotes the full node set of the current VRP vari-            4.3   Model Training Pipeline
ant. Let E(s) ⊆ N × N denote the customer-to-
                                                              Stage 1: Supervised Fine-Tuning. Based on the
customer arcs used by solution s, and U (s) ⊆ N
                                                              data synthesis pipeline described above, we con-
the customers left unserved by s. Since a solution
                                                              struct the verified SFT dataset:
contains multiple routes, we further define Er (s)
as the customer-to-customer arcs on route r. Below                                     gen
                                                                               D = (p, Ccon ) .                   (14)
we describe how to construct the injection con-
straints Φ(s) from s. For each solution s ∈ S, we                For the SFT stage, we fine-tune a pre-trained
first fix its customer-level routing structure with the       LLM on D, where the input is the problem p and
following constraint set, denoted by Φcust (s):               the target is the tokenization y = (y1 , . . . , yT ) of
                                                                gen
  X                                                           Ccon  . The training objective minimizes the stan-
        xkuv = I[(u, v) ∈ E(s)],       ∀ u, v ∈ N,            dard autoregressive negative log-likelihood:
  k∈M
        X      X
                     xkuc = 0,
                                                                                        " T                         #
                                   ∀ c ∈ U (s).                                          X
      u∈V \{c} k∈M
                                                              LSFT (θ) = −E(p,y)∼D              log pθ (yt | p, y<t ) ,
                                                 (11)                                     t=1
                                                                                                            (15)
That is, each customer-to-customer arc (u, v) is
                                                              where pθ (yt | p, y<t ) denotes the probability of
fixed according to the indicator I[(u, v) ∈ E(s)]:
                                                              generating token yt conditioned on the problem
arcs used in s must be traversed by exactly one
                                                              description p and all preceding tokens y<t . The
vehicle, whereas all customer arcs not appearing
                                                              fine-tuned model is denoted VRPCoder-SFT.
in E(s) are deactivated. Moreover, every unserved
customer c ∈ U (s) has its incoming arcs blocked              Stage 2: Reinforcement Learning with GRPO.
entirely. By injecting s+ , we can detect whether             While SFT teaches the model to imitate teacher-
  gen
Ccon  introduces spurious constraints that incor-             generated code, it cannot leverage execution feed-
rectly exclude a feasible solution. For a homo-               back to further improve constraint modeling accu-
geneous fleet, this gives Φ(s+ ) = Φcust (s+ ).               racy. To address this, we apply GRPO (Shao et al.,
   For an infeasible solution s−i under a homoge-             2024) to fine-tune the policy πθ , initialized from
neous fleet, the customer-level injection Φcust (s−i )        VRPCoder-SFT, using reward signals derived from
alone is insufficient: the solver can reassign arcs           solver execution. Figure 4 summarizes the model
across vehicles to silently repair the violation. We          training pipeline.
therefore add route-level consistency constraints:
                                                              Reward function. For a code y generated for
  Φroute (s−      k     k                                     problem p, the reward is a weighted combination
           i ) : xij = xab ,
                                                              of three components:
    ∀ k ∈ M, ∀ (i, j), (a, b) ∈ Er (s−
                                     i ), ∀ r. (12)

This ensures that all customer arcs on the same                 r(p, y) = λbuild rbuild (y) + λopt ropt (y, Ccon )
route r are assigned to a single vehicle, without                                          + λinj rinj (y, S), (16)
specifying which one. For a homogeneous fleet,
the full injection for s−
                        i is thus:
                                                              where the individual terms are defined as fol-
                                                              lows: (1) rbuild (y) = I[build(y)], indicating
      Φ(s−             −              −
         i ) = Φcust (si ) ∪ Φroute (si ).        (13)        whether y successfully constructs a valid Gurobi
                                                              model; (2) ropt (y, Ccon ) = I[Opt(y, Ccon ) ≤
In this way, the violation introduced by perturba-            εobj ], indicating whether the optimal value pro-
tion is preserved on its original route, enabling us          duced by y matches that returned by the refer-
                     gen
to check whether Ccon    misses the corresponding             ence concrete    code Ccon ; and (3) rinj (y, S) =
                                                                 −1
                                                                      P
category of constraint. For heterogeneous fleets,             |S|       s∈S I[Inj(y, s) = ℓ(s)], measuring the


                                                          6
 Stage 1: Supervised Fine-Tuning
                                                                                                                   
    Problems 𝒑                                                                     G       |oi | 
                                                                                 1    1                           
                                                                                                             (i,t) 
                                                                                                   Lclip
                                                                                   X       X
           𝒈𝒆𝒏
                                                                      J (θ) = E                    i,t − β DKL       ,
    Code 𝑪𝒄𝒐𝒏                                                                    G   |oi |
                              Base               VRPCoder                              i=1      t=1
    Training Data             Model                SFT                                                                    (18)
 Stage 2: Reinforcement Learning with GRPO                              where the expectation is over prompts p ∼
            Reward Components for Rollout 𝒚                          DGRPO and rollout groups {oi }G       i=1 sampled from
                     Build Reward 𝒓𝒃𝒖𝒊𝒍𝒅 (𝒚)
          Optimal Value Check Reward 𝒓𝒐𝒑𝒕 (𝒚, 𝑪𝒄𝒐𝒏 )
                                                                     πθold (· | p). For token t in rollout oi , the impor-
          Constraint Injection Check Reward 𝒓𝒊𝒏𝒋 (𝒚, 𝑺)              tance ratio is ρi,t = πθ (oi,t | p, oi,<t )/πθold (oi,t |
                    Offline sample filtering                         p, oi,<t ). The clipped surrogate is Lclip     i,t     =
                                           𝜎=0
                                                                                            
                               Reward      𝜎>0                       min ρi,t Âi , ρ̄i,t Âi , where ρ̄i,t = clip(ρi,t , 1 −
   Problems 𝒑            100%
                        correct                    Filtered
                                                  Problems           ϵ, 1 + ϵ). The rollout-level group-normalized ad-
                                                                     vantage is Âi = (r(p, oi )−µr )/(σr +εadv ), where
        VRPCoder
                                             🗑 Discard
                          0%                                         µr and σr are the mean and standard deviation of
          SFT           correct
                                                                     {r(p, oj )}Gj=1 , and εadv > 0 is a small constant for
                    Online GRPO training
                                                                     numerical stability; the same Âi is shared across
                                                                                                    (i,t)
     Filtered 𝒑                                                      all tokens in oi . Finally, DKL denotes the token-
                                                 VRPCoder
                                                                     level KL penalty against the reference policy πref ,
     Training Data           VRPCoder
                               SFT                 RL                a frozen copy of VRPCoder-SFT.
                                                                        Here β is the KL coefficient, ϵ is the clipping
  Figure 4: Overview of the model training pipeline.                 range, and G is the number of rollouts per problem.
                                                                     The resulting model is denoted VRPCoder-RL.

fraction of solutions in S that pass the constraint in-              5     Experiments
jection check. Here, I[·] denotes the indicator func-                5.1    Experimental Setup
tion, and λbuild , λopt , and λinj denote the weights
assigned to the three reward components, respec-                     Benchmark. The training dataset D contains
                                                                                  gen
tively.                                                              6,797 (p, Ccon   ) pairs produced by the synthesis
                                                                     pipeline in Section 4.2. For evaluation, we intro-
                                                                     duce VRPBench, a 700-problem expert-verified
Offline sample filtering. To ensure effective pol-                   benchmark comprising four subsets: (1) In-domain
icy optimization, we filter training samples that                    synthetic (310 problems), generated from the 18
provide meaningful learning signal. Specifically,                    training variants with unseen random seeds, eval-
for each problem p, we pre-generate H rollouts us-                   uating in-distribution generalization; (2) Out-of-
ing VRPCoder-SFT and compute the within-group                        domain synthetic (66 problems), generated from
reward standard deviation:                                           the 3 held-out compositional variants, evaluating
               v                                                     whether the model can combine familiar constraint
               u
               u1 XH
                                    2                               primitives into unseen VRP variants; (3) Expert-
          σp = t     r(p, yh ) − r̄p ,                    (17)       written (74 problems), sampled from public op-
                 H
                         h=1                                         timization libraries and formulated by OR ex-
                                                                     perts, evaluating performance on human-authored
where r̄p = H1 H
                P                                                    problem descriptions; (4) Externally-sourced (250
                   h=1 r(p, yh ). We retain only sam-
ples with σp > 0, discarding groups whose rollouts                   problems), collected from MAMO (Huang et al.,
receive identical rewards, as they provide no within-                2025b), IndustryOR (Huang et al., 2025a), Opt-
group learning signal.                                               MATH (Lu et al., 2025), and NLCO (Jiang et al.,
                                                                     2026), evaluating cross-source robustness.

Online GRPO training. On the dataset DGRPO                           Baselines. We compare against four baseline
obtained after sample filtering, for each problem p                  groups: (1) closed-source frontier LLMs, in-
we sample G rollouts from πθold , compute group-                     cluding Gemini-3.1-Pro Preview (Google Deep-
normalized advantages, and update πθ via:                            Mind, 2026) and Claude-Sonnet-4.5 (Anthropic,

                                                                 7
                                                                       VRPBench
                     Model                     Subset 1     Subset 2     Subset 3     Subset 4     AVG
                     Closed-source frontier LLMs
                     Gemini-3.1-Pro Preview      95.81        89.39        91.89        96.40      95.00
                     Claude-Sonnet-4.5           70.65        42.42        79.73        58.80      64.71
                     Open-source general-purpose LLMs
                     DeepSeek-V3.2             31.29            7.58       51.35        45.60      36.29
                     MiniMax-M2.5              21.61            9.09       17.57        32.80      24.00
                     Qwen2.5-72B-Instruct      15.81            6.06       12.16        27.20      18.57
                     Qwen3-8B                   0.00            0.00       1.35         1.20       0.57
                     OR-LLMs
                     ORLM-LLaMA-3-8B             3.87           0.00       12.16         7.60      5.71
                     OptMATH-Qwen2.5-7B          0.97           0.00        2.70         8.40      3.71
                     SIRL-Gurobi-8B              1.94           0.00        0.00        13.20      5.57
                     SIRL-Gurobi-32B             8.71           3.03        1.35        30.00      15.00
                     Our 8B model
                     VRPCoder-SFT               92.26         89.39        82.43        85.20      88.43
                     VRPCoder-RL                96.13         96.97        93.24        88.00      93.00

Table 1: Pass@1 (%) on the four subsets of VRPBench. Best scores are bolded; second-best are underlined. AVG
is computed over all samples in VRPBench.

                                                                         VRPBench
            Method                          Subset 1      Subset 2     Subset 3     Subset 4     AVG       ∆ AVG
            VRPCoder-SFT w/o Injection       91.61         81.82        83.78        79.60       85.57       –
            VRPCoder-SFT                     92.26         89.39        82.43        85.20       88.43     +2.86
            VRPCoder-RL w/o Injection        94.19         93.94        91.89        80.40       89.00       –
            VRPCoder-RL                      96.13         96.97        93.24        88.00       93.00     +4.00

Table 2: Ablation of constraint injection for SFT and RL on VRPBench. Best scores are bolded. ∆ AVG reports the
percentage-point gain in overall Pass@1 over the corresponding model without injection.


2025); (2) open-source general-purpose LLMs,                    tier prompts DGRPO , and run GRPO with G = 8
including DeepSeek-V3.2 (DeepSeek-AI, 2025),                    rollouts per prompt, temperature 0.4, top-p 0.95,
MiniMax-M2.5 (MiniMax Team, 2026), Qwen2.5-                     and KL coefficient β = 0.02. The composite re-
72B-Instruct (Qwen Team, 2024), and Qwen3-                      ward weights are 0.2, 0.5, and 0.3 for rbuild , ropt ,
8B (Qwen Team, 2025); (3) SFT-based OR-LLMs,                    and rinj , respectively, yielding VRPCoder-RL. Full
including ORLM-LLaMA-3-8B (Huang et al.,                        settings are provided in Appendix E.
2025a) and OptMATH-Qwen2.5-7B (Lu et al.,
2025); (4) RL-based OR-LLMs, including SIRL-                    5.2    Main Results
Gurobi-8B and SIRL-Gurobi-32B (Chen et al.,
2025). We evaluate groups (1) and (2) with the                  Table 1 reports Pass@1 on the four subsets of
shared code-regeneration prompt (Appendix H),                   VRPBench. VRPCoder-RL outperforms Gemini-
and evaluate groups (3) and (4) with their original             3.1-Pro Preview on Subsets 1, 2, and 3, achiev-
prompts and solver settings.                                    ing 96.13%, 96.97%, and 93.24% versus 95.81%,
                                                                89.39%, and 91.89%, but trails on Subset 4, which
Implementation Details. Both stages use a                       includes the traveling salesman problem with time
LoRA adapter with rank r = 16, α = 32, and                      windows (TSPTW), a variant absent from train-
dropout 0.1 on Qwen3-8B, trained on 4×A100-                     ing. It exceeds Claude-Sonnet-4.5 by a large mar-
40GB GPUs. We first apply LoRA SFT on D for 3                   gin, with 93.00% versus 64.71% overall Pass@1.
epochs with a maximum sequence length of 8192,                  Existing OR-LLMs achieve notably low perfor-
using AdamW with learning rate 2 × 10−4 and                     mance across all subsets, where the strongest,
cosine scheduling, to obtain VRPCoder-SFT. We                   SIRL-Gurobi-32B, reaches only 15.00% average
then perform offline sample filtering with H = 6                Pass@1, indicating limited applicability to real-
pre-generated rollouts per prompt to select fron-               world VRP scenarios and further demonstrating the

                                                            8
                                    1.0                                              λbuild   λopt   λinj   AVG Pass@1
                                    0.9
0.2                                                                                    0.2     0.6    0.2       91.57
                                    0.8                                                0.2     0.5    0.3       93.00
                                    0.7                                                0.2     0.4    0.4       92.86
0.1                                                                                    0.2     0.3    0.5       90.71
                                    0.6
      0   500 1000 1500 2000 2500         0     200    400    600
             (a) SFT Loss                 (b) RL Reward (Mean ± Std)       Table 3: Sensitivity analysis of the three reward weights
                                                                           (λbuild , λopt , λinj ) for VRPCoder-RL. Best score is
Figure 5: Training dynamics of SFT and RL. The left                        bolded.
panel shows the SFT training loss, while the right panel
shows the RL mean reward. The dark curve indicates
the smoothed trend, and the shaded region visualizes                       injection is down-weighted (0.6/0.2: 91.57%) or
local variation over training steps.                                       made dominant (0.3/0.5: 90.71%). This suggests
                                                                           that constraint injection works best as a comple-
                                                                           ment to the optimal value check rather than as the
value of VRPBench as a challenging evaluation
                                                                           dominant reward. All weight configurations out-
benchmark. Before fine-tuning, the base model
                                                                           perform removing injection entirely (Table 2).
Qwen3-8B is essentially non-functional, achieving
only 0.57% overall Pass@1; after our full pipeline,
                                                                           6   Conclusion
it achieves 93.00% overall Pass@1, confirming the
effectiveness of the proposed training framework.                          We identified objective equivalence as a shared
                                                                           blind spot in SFT- and RL-based optimization-
5.3       Ablation Studies                                                 modeling pipelines, where spurious over-
Table 2 isolates the contribution of constraint injec-                     constraints and silent constraint omissions can
tion. The no-injection setting removes the injection                       be indistinguishable from correct code when
signal from both stages: SFT retains samples that                          the affected constraints are non-binding at the
pass the optimal value check but fail injection, and                       optimum. We proposed constraint injection, a
RL scores rollouts using only build success and                            constraint-level verification operator that uses
the optimal value check. Removing injection low-                           feasible and one-constraint-violating solutions;
ers overall Pass@1 by 2.86 percentage points for                           combined with the optimal value check, it forms
SFT (88.43% to 85.57%) and by 4.00 points for                              a dual verifier. We applied this verifier as a
RL (93.00% to 89.00%). The largest gain appears                            rejection-sampling filter during data synthesis and
on Subset 4, where RL improves from 80.40% to                              a per-rollout reward in GRPO. When instantiated
88.00%. Subset 2 also improves substantially at the                        on vehicle routing as a constraint-dense testbed,
SFT stage, from 81.82% to 89.39%. These results                            our framework yields VRPCoder-RL, which
indicate that constraint-level supervision provides                        reaches 93.00% overall Pass@1 on VRPBench. It
information beyond the optimal value check, espe-                          is competitive with frontier LLMs and surpasses
cially under distribution shift and unseen constraint                      prior OR-LLMs by a large margin. Ablations
combinations.                                                              show that constraint injection is a key component:
                                                                           the largest improvement appears on the most
5.4       Model Analysis                                                   distribution-shifted subset, and constraint-level
Training dynamics. Figure 5 shows the training                             supervision provides benefits beyond the optimal
curves of both stages. In the SFT stage, the training                      value check.
loss decreases steadily from 0.272 to 0.043 over
2,550 steps, indicating stable convergence. In the                         Limitations
RL stage, the mean reward shows a clear overall
                                                                           Our empirical validation focuses on vehicle routing,
upward trend over 714 steps, with its late-stage
                                                                           and transferring constraint injection to other opti-
level around 0.94.
                                                                           mization domains requires expert-written abstract-
Sensitivity Analysis. Table 3 shows the reward                             code templates, constraint-family-specific perturba-
weight sensitivity analysis. We keep the three                             tion operators, and compatible solution-encoding
weights summing to 1, fix λbuild =0.2, and vary                            rules. This effort is incurred once per recurring
λopt and λinj . Pass@1 remains above 90%                                   constraint family rather than per instance, but trans-
across all configurations and peaks at 93.00% for                          ferability beyond routing remains to be evaluated.
λopt /λinj = 0.5/0.3. It is slightly lower when                            Our one-constraint-violating solutions isolate in-

                                                                       9
dividual constraint families while the other con-              Zezhen Ding, Zhen Tan, Jiheng Zhang, and Tianlong
straints in the generated model remain active, but               Chen. 2026. OR-R1: Automating Modeling and
                                                                 Solving of Operations Research Optimization Prob-
they may not expose errors that arise only through
                                                                 lem via Test-Time Reinforcement Learning. In Pro-
interactions among multiple constraints. We report               ceedings of the AAAI Conference on Artificial Intelli-
instance-level Pass@1 to enable consistent com-                  gence, volume 40, pages 228–236.
parison across all four subsets of VRPBench. Al-
                                                               Bruce L. Golden, Edward A. Wasil, James P. Kelly,
though Appendix F reports constraint-level failures              and I-Ming Chao. 1998. The Impact of Metaheuris-
during data synthesis, benchmark-wide constraint-                tics on Solving the Vehicle Routing Problem: Al-
level evaluation of final model outputs remains fu-              gorithms, Problem Sets, and Computational Results.
ture work.                                                       In Teodor Gabriel Crainic and Gilbert Laporte, edi-
                                                                 tors, Fleet Management and Logistics, pages 33–56.
                                                                 Springer, Boston, MA.
Acknowledgments
                                                               Google DeepMind. 2026. Gemini 3.1 Pro Model Card.
This research was supported by the National Nat-                 https://deepmind.google/models/model-cards/gem
ural Science Foundation of China under Grant                     ini-3-1-pro/. Accessed: 2026-05-26.
72571017.
                                                               Chenyu Huang, Zhengyang Tang, Shixi Hu, Ruoqing
                                                                 Jiang, Xin Zheng, Dongdong Ge, Benyou Wang,
                                                                 and Zizhuo Wang. 2025a. ORLM: A Customiz-
References                                                       able Framework in Training Large Models for Auto-
                                                                 mated Optimization Modeling. Operations Research,
Anthropic. 2025. Claude Sonnet 4.5 System Card. ht               73(6):2986–3009.
  tps://www.anthropic.com/claude-sonnet-4-5-syste
  m-card. Accessed: 2026-05-26.                                Xuhan Huang, Qingning Shen, Yan Hu, Anningzhe Gao,
                                                                 and Benyou Wang. 2025b. LLMs for Mathematical
Anthropic. 2026. Claude Opus 4.6 System Card. https://           Modeling: Towards Bridging the Gap between Natu-
  www.anthropic.com/claude-opus-4-6-system-card.                 ral and Mathematical Languages. In Findings of the
  Accessed: 2026-05-26.                                          Association for Computational Linguistics: NAACL
                                                                 2025, pages 2678–2710, Albuquerque, New Mexico.
Philippe Augerat, José Manuel Belenguer, Enrique Be-             Association for Computational Linguistics.
  navent, Angel Corberán, Denis Naddef, and Giovanni
  Rinaldi. 1995. Computational Results with a Branch           Zhehui Huang, Guangyao Shi, and Gaurav S. Sukhatme.
  and Cut Code for the Capacitated Vehicle Routing               2024. From Words to Routes: Applying Large Lan-
  Problem. Technical Report 949-M, Université Joseph             guage Models to Vehicle Routing. arXiv preprint
  Fourier, Grenoble.                                             arXiv:2403.10795.

José M. Belenguer, M. Cristina Martinez, and Ernesto           Caigao Jiang, Xiang Shu, Hong Qian, Xingyu Lu, Jun
  Mota. 2000. A Lower Bound for the Split Deliv-                 Zhou, Aimin Zhou, and Yang Yu. 2025a. LLMOPT:
  ery Vehicle Routing Problem. Operations Research,              Learning to Define and Solve General Optimization
  48(5):801–810.                                                 Problems from Scratch. In International Conference
                                                                 on Learning Representations, volume 2025, pages
Kris Braekers, Katrien Ramaekers, and Inneke                     101580–101606.
  Van Nieuwenhuyse. 2016. The Vehicle Routing Prob-
                                                               Xia Jiang, Jing Chen, Cong Zhang, Jie Gao, Cheng-
  lem: State of the Art Classification and Review. Com-
                                                                 peng Hu, Chenhao Zhang, Yaoxin Wu, and Yingqian
  puters & Industrial Engineering, 99:300–313.
                                                                 Zhang. 2026. Reasoning in a combinatorial and
                                                                 constrained world: Benchmarking LLMs on natural-
Yitian Chen, Jingfan Xia, Siyu Shao, Dongdong Ge, and            language combinatorial optimization. In Findings of
  Yinyu Ye. 2025. Solver-Informed RL: Grounding                  the Association for Computational Linguistics: ACL
   Large Language Models for Authentic Optimization              2026, pages 30592–30648, San Diego, California,
   Modeling. In Advances in Neural Information Pro-              United States. Association for Computational Lin-
   cessing Systems, volume 38, pages 106027–106069.              guistics.
   Curran Associates, Inc.
                                                               Xia Jiang, Yaoxin Wu, Minshuo Li, Zhiguang Cao,
Jean-François Cordeau, Michel Gendreau, and Gilbert              and Yingqian Zhang. 2025b. Large language mod-
   Laporte. 1997. A Tabu Search Heuristic for Periodic           els as end-to-end combinatorial optimization solvers.
   and Multi-Depot Vehicle Routing Problems. Net-                In Advances in Neural Information Processing Sys-
   works, 30(2):105–119.                                         tems, volume 38, pages 164787–164826. Curran As-
                                                                 sociates, Inc.
DeepSeek-AI. 2025. DeepSeek-V3.2: Pushing the
  Frontier of Open Large Language Models. Preprint,            Xia Jiang, Yaoxin Wu, Chenhao Zhang, and Yingqian
  arXiv:2512.02556.                                              Zhang. 2025c. DRoC: Elevating Large Language


                                                          10
  Models for Complex Vehicle Routing via Decom-                  the 26th ACM SIGKDD International Conference on
  posed Retrieval of Constraints. In International Con-          Knowledge Discovery & Data Mining, pages 3505–
  ference on Learning Representations, volume 2025,              3506. Association for Computing Machinery.
  pages 46731–46752.
                                                               Gerhard Reinelt. 1991. TSPLIB–A Traveling Sales-
Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying                     man Problem Library. ORSA Journal on Computing,
 Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E. Gon-               3(4):376–384.
 zalez, Hao Zhang, and Ion Stoica. 2023. Efficient
 Memory Management for Large Language Model                    Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,
 Serving with PagedAttention. In Proceedings of the              Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan
 29th Symposium on Operating Systems Principles,                 Zhang, Y. K. Li, Y. Wu, and Daya Guo. 2024.
 pages 611–626, Koblenz, Germany. Association for                DeepSeekMath: Pushing the Limits of Mathemat-
 Computing Machinery.                                            ical Reasoning in Open Language Models. Preprint,
                                                                 arXiv:2402.03300.
Rahma Lahyani, Mahdi Khemakhem, and Frédéric
  Semet. 2015. Rich Vehicle Routing Problems: From             Marius M. Solomon. 1987. Algorithms for the Vehicle
  a Taxonomy to a Definition. European Journal of               Routing and Scheduling Problems with Time Win-
  Operational Research, 241(1):1–14.                            dow Constraints. Operations Research, 35(2):254–
                                                                265.
Gilbert Laporte. 2009. Fifty Years of Vehicle Routing.
  Transportation Science, 43(4):408–416.                       Paolo Toth and Daniele Vigo. 1997. An Exact Algo-
                                                                 rithm for the Vehicle Routing Problem with Back-
Hung Le, Yue Wang, Akhilesh Deepak Gotmare, Silvio               hauls. Transportation Science, 31(4):372–385.
  Savarese, and Steven Chu Hong Hoi. 2022. Coderl:
  Mastering code generation through pretrained models          Paolo Toth and Daniele Vigo, editors. 2014. Vehicle
  and deep reinforcement learning. In Advances in                Routing: Problems, Methods, and Applications, 2
  Neural Information Processing Systems, volume 35,              edition. Number 18 in MOS-SIAM Series on Opti-
  pages 21314–21328. Curran Associates, Inc.                     mization. Society for Industrial and Applied Mathe-
                                                                 matics, Philadelphia, PA.
Kai Li, Fei Liu, Zhenkun Wang, Xialiang Tong, Xiong-
  wei Han, Mingxuan Yuan, and Qingfu Zhang. 2025.              Eduardo Uchoa, Diego Pecin, Artur Pessoa, Marcus
  ARS: Automatic Routing Solver with Large Lan-                  Poggi, Thibaut Vidal, and Anand Subramanian. 2017.
  guage Models. Preprint, arXiv:2502.15359v3.                    New Benchmark Instances for the Capacitated Vehi-
                                                                 cle Routing Problem. European Journal of Opera-
Hongliang Lu, Zhonglin Xie, Yaoyu Wu, Can Ren, Yux-
                                                                 tional Research, 257(3):845–858.
  uan Chen, and Zaiwen Wen. 2025. OptMATH: A
  Scalable Bidirectional Data Synthesis Framework              Ziyang Xiao, Jingrong Xie, Lilin Xu, Shisi Guan,
  for Optimization Modeling. In Proceedings of the               Jingyan Zhu, Xiongwei Han, Xiaojin Fu, WingYin
  42nd International Conference on Machine Learn-                Yu, Han Wu, Wei Shi, Qingcan Kang, Jiahui Duan,
  ing, volume 267 of Proceedings of Machine Learning             Tao Zhong, Mingxuan Yuan, Jia Zeng, Yuan Wang,
  Research, pages 40769–40802. PMLR.                             Gang Chen, and Dongxiang Zhang. 2025. A Survey
MiniMax Team. 2026. MiniMax-M2.5 Model Card.                     of Optimization Modeling Meets LLMs: Progress
  https://huggingface.co/MiniMaxAI/MiniMax-M2.5.                 and Future Directions. In Proceedings of the Thirty-
  Accessed: 2026-05-26.                                          Fourth International Joint Conference on Artificial
                                                                 Intelligence, IJCAI-25, pages 10742–10750. Inter-
Qwen Team. 2024.       Qwen2.5 Technical Report.                 national Joint Conferences on Artificial Intelligence
 Preprint, arXiv:2412.15115.                                     Organization. Survey Track.

Qwen Team. 2025. Qwen3 Technical Report. Preprint,             Zhicheng Yang, Yiwei Wang, Yinya Huang, Zhi-
  arXiv:2505.09388.                                              jiang Guo, Wei Shi, Xiongwei Han, Liang Feng,
                                                                 Linqi Song, Xiaodan Liang, and Jing Tang. 2025.
Rindranirina Ramamonjison, Timothy Yu, Raymond                   OptiBench Meets ReSocratic: Measure and Improve
  Li, Haley Li, Giuseppe Carenini, Bissan Ghaddar,               LLMs for Optimization Modeling. In The Thirteenth
  Shiqi He, Mahdi Mostajabdaveh, Amin Banitalebi-                International Conference on Learning Representa-
  Dehkordi, Zirui Zhou, and Yong Zhang. 2022.                    tions.
  NL4Opt Competition: Formulating Optimization
  Problems Based on Their Natural Language Descrip-            Ni Zhang, Zhiguang Cao, Jianan Zhou, Cong Zhang,
  tions. In Proceedings of the NeurIPS 2022 Competi-             and Yew-Soon Ong. 2026. An Agentic Framework
  tions Track, volume 220 of Proceedings of Machine              with LLMs for Solving Complex Vehicle Routing
  Learning Research, pages 189–203. PMLR.                        Problems. In The Fourteenth International Confer-
                                                                 ence on Learning Representations.
Jeff Rasley, Samyam Rajbhandari, Olatunji Ruwase,
   and Yuxiong He. 2020. DeepSpeed: System Opti-               Xinzhi Zhang, Zeyi Chen, Humishka Zope, Hugo Bar-
   mizations Enable Training Deep Learning Models                balho, Konstantina Mellou, Marco Molinaro, Janard-
   with Over 100 Billion Parameters. In Proceedings of           han Kulkarni, Ishai Menache, and Sirui Li. 2025.


                                                          11
  OptiMind: Teaching LLMs to Think Like Optimiza-            A    VRP Variant Overview
  tion Experts. Preprint, arXiv:2509.22979v2. Version
  2.                                                         We build 21 VRP variants. The 21-variant count
                                                             refers to the variants constructed for Subsets 1–
Chenyu Zhou, Tianyi Xu, Jianghao Lin, and Dongdong
  Ge. 2026. StepORLM: A Self-Evolving Framework              3; the externally sourced Subset 4 additionally in-
  With Generative Process Supervision For Operations         cludes TSPTW.
  Research Language Models. In The Fourteenth Inter-            MD (multi-depot) introduces multiple depots,
  national Conference on Learning Representations.           with each vehicle departing from and returning
                                                             to its assigned depot. MC (multi-compartment)
                                                             partitions each vehicle into multiple non-mixing
                                                             compartments, each with an independent capacity.
                                                             PD (pickup-and-delivery) pairs pickup and deliv-
                                                             ery nodes that must be visited by the same vehicle
                                                             in order. Open (open routing) allows each route
                                                             to terminate at the last customer without returning
                                                             to the depot. HTW (hard time window) imposes
                                                             hard time windows [ai , bi ] on service start times;
                                                             early arrival is allowed through waiting, but service
                                                             cannot start before ai or after bi . STW (soft time
                                                             window) relaxes time-window violations into ob-
                                                             jective penalties. Dist (distance limit) imposes a
                                                             maximum travel distance Dmax on each route. BH
                                                             (backhaul) splits customers into linehaul and back-
                                                             haul segments and requires all linehaul customers
                                                             to precede backhaul customers on each route. Split
                                                             (split delivery) allows a customer to be served by
                                                             multiple vehicles. HF (heterogeneous fleet) al-
                                                             lows capacities, fixed costs, and per-distance costs
                                                             to vary by vehicle.
                                                                The Cap. column in Table 4 specifies capacity
                                                             semantics: Q for homogeneous capacity, Qk for
                                                             heterogeneous capacity, and “–” for no effective
                                                             capacity limit. VRPB accounts for linehaul and
                                                             backhaul loads separately, whereas MCVRP and
                                                             HFMCVRP account for capacities separately for
                                                             each compartment.

                                                             B Constraint-Level Solution Construction
                                                             In the three-stage data synthesis pipeline (Sec-
                                                             tion 4.2), Stage 1 constructs feasible and one-
                                                             constraint-violating solutions with auditable fea-
                                                             sibility labels for each training sample. Given
                                                             a variant v and a profile, we first determine the
                                                             customer count, fleet size, coordinate distribution,
                                                             and base demand range (Appendix B.1). Variant-
                                                             specific rules then specify capacities, time win-
                                                             dows, route-distance limits, heterogeneous vehicle
                                                             types, pickup–delivery pairs, compartments, and
                                                             backhaul labels, yielding a complete instance and
                                                             its reference concrete code Ccon (Appendix B.2).
                                                             We then construct a feasible solution s+ (Ap-
                                                             pendix B.3) and derive one-constraint-violating so-

                                                        12
       Variant         Cap.   MD     MC     PD    Open    HTW       STW    Dist   BH    Split   HF     Train
       TSP               –                                                                              ✓
       CVRP             Q                                                                               ✓
       MDVRP            Q      ✓                                                                        ✓
       MCVRP            Q             ✓                                                                 ✓
       PDP              Q                   ✓                                                           ✓
       OVRP             Q                          ✓                                                    ✓
       DCVRP            Q                                                   ✓                           ✓
       VRPB             Q                                                          ✓                    ✓
       SDVRP            Q                                                                ✓              ✓
       VRPHTW           Q                                     ✓                                         ✓
       VRPSTW           Q                                            ✓                                  ✓
       HFVRP            Qk                                                                      ✓       ✓
       HFMDVRP          Qk     ✓                                                                ✓       ✓
       HFMCVRP          Qk            ✓                                                         ✓       ✓
       HFVRPHTW         Qk                                    ✓                                 ✓       ✓
       MDVRPSTW         Q      ✓                                     ✓                                  ✓
       PDPSTW           Q                   ✓                        ✓                                  ✓
       PDPTW             –                  ✓                 ✓                                         ✓
       OVRPHTW          Q                          ✓          ✓                                      Held-out
       MCVRPSTW         Q             ✓                              ✓                               Held-out
       DCVRPHTW         Q                                     ✓             ✓                        Held-out

Table 4: Structural module matrix for the 21 VRP variants. A check mark (✓) indicates the module is enabled. The
Train column specifies the participation in SFT/GRPO training. Bold and italicized variants are strictly held out
from the training mixture: their constituent modules are present in the training set, but their pairwise combinations
are never seen, forming Subset 2 for evaluating compositional generalization.


lutions {s−           +
           i } from s (Appendix B.4). Finally,                specified by a boundary-profile grid, H for the
bounded resources are slightly relaxed and each               time horizon in time-window variants, and C for
labeled solution set S is checked by Ccon before              the number of compartments. A grid tuple such as
assembly (Appendix B.5). The main depot is fixed              (n, k, Q, d), (n, k, Q, H), or (n, k, Q, C) denotes
at (50, 50); multi-depot variants use two depots at           an instance-level configuration. If an entry contains
(25, 50) and (75, 50); all customer coordinates are           an interval, such as d = [3, 6], the tuple is first se-
clipped to the coordinate range [5, 95]2 .                    lected and each customer demand is then sampled
                                                              from that interval. In Table 5, “locked” means that
B.1   Profiles                                                the profile family directly uses the resource values
                                                              from its grid rather than the default rules in Ap-
A profile serves as a parameter envelope rather than          pendix B.2; “–” means that the profile specifies
a training split or an algorithmic component. It is           only scale and geometry, and the resource parame-
applied before instance generation and specifies the          ters are supplied by the variant-specific rules.
customer count n, vehicle count k, spatial distribu-
tion, and base range for scalar customer demands,                Uniform, Clustered, and Radial distributions
while variant-specific modules fill in capacities,            are inspired by the VRP instance designs of
time windows, pickup-delivery demand, compart-                Augerat et al. (1995) and Uchoa et al. (2017);
ment demand, and other constraints. Profiles are              time-window generation follows Solomon (1987);
designed so that small-scale instances, regular lay-          and regular geometric arrays follow Golden et al.
outs, and geometric, capacity, or time-boundary               (1998). These references serve only as sources of
cases all lie in a single auditable parameter space,          design factors and do not indicate that our samples
instead of being listed instance by instance. We use          are drawn from the corresponding benchmarks.
15 profiles in total: 12 regular profiles and 3 bound-           The five spatial distributions define geomet-
ary profiles; this appendix specifies their parameter         ric families for customer coordinates only, rather
coverage. Unless otherwise stated, an interval [a, b]         than complete VRP instances. Capacities, time
denotes a sampling envelope, and a discrete set lists         windows, pickup-delivery pairs, compartments,
the admissible choices.                                       and other constraint modules are supplied by Ap-
   We use d for scalar customer demand, Q for ho-             pendix B.2. Uniform samples customer coordi-
mogeneous vehicle capacity or a capacity bound                nates independently in the plane. Clustered first

                                                         13
samples 2–3 centers and then draws compact cus-                    subfamily uses a split-cluster layout and samples
tomer groups around them. Radial samples angles                    (n, k, Q, C) from four configurations: (8, 3, 24, 2),
and radii around the depot. Elongated forms a                      (10, 3, 26, 2), (10, 4, 24, 2), and (12, 4, 28, 2).
narrow corridor along a random direction. Split
places customers in two separated groups.                          B.2   Variant-Specific Parameters
   For profile 13, only the hexagon subfamily                      After a profile determines (n, k), the spatial distri-
fixes Q = 100, keeping capacity safely non-                        bution, and the base demand, the variant genera-
binding so that the resulting solutions focus on                   tor generates the additional parameters required by
depot connectivity and subtour structure; other                    each constraint module. Unless otherwise specified,
geometry-boundary subfamilies still take capacity                  continuous values are sampled within the reported
values from Appendix B.2. Profiles 14 and 15 are                   intervals and discrete values are selected from the
marked as locked because they are generated by                     reported sets.
directly sampling grid tuples such as (n, k, Q, d),
                                                                   Capacity. For homogeneous-capacity variants,
(n, k, Q, H), or (n, k, Q, C).
                                                                   effective vehicle capacities lie within the enve-
   The boundary profiles specify parameter arrange-
                                                                   lope [8, 100]. The capacity-boundary family does
ments rather than new VRP variants or training
                                                                   not sample from the default envelope; it directly
subsets. Profile 13 covers deterministic geomet-
                                                                   uses the (n, k, Q, d) grid from Appendix B.1, mak-
ric structures. Its hexagon subfamily uses n =
                                                                   ing the average route demand close to the capac-
6, k = 1, places customers on a regular hexagon
                                                                   ity bound. TSP has no effective capacity con-
with radius r ∈ [15, 25], places the depot at the
                                                                   straint and assigns zero demand to nodes. SDVRP
midpoint of one hexagon edge, and fixes Q = 100.
                                                                   uses split-delivery demand, with scalar demand in
The polygon subfamily samples n ∈ {4, 6, 8} and
                                                                   [2, 20] and vehicle capacity in [30, 85]. MCVRP,
places customers on a regular polygon centered at
                                                                   HFMCVRP, and MCVRPSTW use two compart-
c ∈ [45, 55]2 , with radius r ∈ [25, 40] and a ran-
                                                                   ments. Each customer has per-compartment de-
dom rotation. The collinear / coverage subfamily
                                                                   mand sampled from [0, 6]; per-compartment capac-
places n ∈ {5, 6, 7, 8} customers at equal spac-
                                                                   ity is obtained by splitting vehicle capacity across
ing on a randomly rotated segment, with spacing
                                                                   compartments and applying a mild perturbation,
in [3, 8]. The local-cluster subfamily places cus-
                                                                   yielding values within the range [5, 55]. The total
tomers within radius r ∈ [1, 3] around a center in
                                                                   vehicle capacity equals the sum of compartment
[20, 80]2 .
                                                                   capacities.
   Profile 14 samples from several (n, k, Q, d)
grids so that the average route demand                             Heterogeneous fleets. HFVRP, HFVRPHTW,
 ¯
dn/k     is close to the capacity bound. The                       HFMDVRP, and HFMCVRP use three vehicle
small-grid settings include (5, 2, 12, [3, 6]),                    types. Type-specific capacities, fixed costs, and
(6, 2, 14, [3, 7]), (6, 3, 12, [2, 5]), (8, 3, 16, [2, 6]),        per-distance costs fall within [10, 65], [20, 70], and
(6, 3, 8, [3, 4]), (8, 4, 8, [3, 4]), (6, 2, 12, [3, 5]),          [0.8, 1.2], respectively. This covers small, medium,
and (8, 3, 12, [3, 5]). To cover split delivery and                and large vehicles, requiring the model to index
heavy-route cases, the extended grids allow n                      both capacity and cost by vehicle type rather than
up to 12, k up to 4, scalar demand up to [2, 20],                  reducing the instance to a homogeneous fleet. In
and capacities within the envelope specified in                    HFMCVRP, the three total base capacities are
Appendix B.2. Customer coordinates use uniform                     {15, 30, 50} and then split into two compartments
or split-cluster layouts.                                          within each type.
   Profile 15 includes time-window, pickup-
                                                                   Route-distance limits. DCVRP and DCVR-
delivery, and compartment subfamilies. The
                                                                   PHTW use route-level distance limits Dmax within
time-window subfamily arranges customers in
                                                                   the range [60, 1000]. When a distance-boundary
a radial sequence, uses d ∈ [1, 4], and
                                                                   perturbation is constructed, Dmax is tightened by
samples (n, k, Q, H) from four configurations:
                                                                   the operator according to the route lengths of s+
(8, 3, 60, 240), (10, 3, 70, 260), (10, 4, 60, 260),
                                                                   and the corresponding solution s−
                                                                                                   i .
and (12, 4, 80, 300). The pickup-delivery time-
window subfamily uses one vehicle and a longer                     Time windows. Regular time-window variants
time horizon, with n ∈ {4, 6, 8, 10, 12}; pairing                  use H = 500, except PDPTW, which uses a chain-
is supplied by the variant rules. The compartment                  length-dependent horizon H = max(1200, 120p+

                                                              14
     #   Profile                          n       k     Spatial distribution       Demand d          Q
     1   Tiny uniform                     5       2     Uniform                    [2, 10]           –
     2   Tiny clustered                   6       2     Clustered                  [1, 10]           –
     3   Small radial                     7       2     Radial                     [2, 8]            –
     4   Small elongated                  7       3     Elongated                  [1, 10]           –
     5   Medium uniform                   8       3     Uniform                    [1, 10]           –
     6   Medium clustered                 9       3     Clustered                  [2, 12]           –
     7   Medium split                     10      3     Split                      [1, 8]            –
     8   Medium light                     8       3     Uniform                    [0.5, 3]          –
     9   Medium heavy                     9       4     Uniform                    [5, 15]           –
    10   Large uniform                    12      4     Uniform                    [1, 8]            –
    11   Large clustered                  12      4     Clustered                  [2, 10]           –
    12   Large mixed                      12      4     Elongated                  [1, 12]           –
    13   Geometry boundary                4–8    1–4    Deterministic geometry     Family-specific   Partially locked
    14   Capacity boundary                5–12   1–4    Uniform / split clusters   Family-specific   Locked
    15   Time / multi-resource boundary   4–12   1–4    Radial / split clusters    Family-specific   Locked

Table 5: Compact profile definitions. The demand column gives the default scalar demand range. Zero scalar
demand for TSP, pickup-delivery demand, and SDVRP split-delivery demand are supplied by the variant-specific
rules. The Q column indicates only whether capacity-related values are fixed at the profile level; the time horizon H
and compartment count C are specified only in the family descriptions for profile 15.


600), where p is the number of pickup-delivery                three construct pickup–delivery pairs; their cus-
pairs, yielding H = 1200 for p ≤ 5 and H = 1320               tomer counts are even and lie in {4, 6, 8, 10, 12}.
for p = 6. After resource relaxation, customer win-           VRPB labels customers as linehaul or backhaul and
dow endpoints remain within [0, 1500]. Depot win-             requires linehaul-first service. OVRP and OVR-
dows are [0, H]. Customer service times lie within            PHTW allow routes to terminate at the last cus-
the effective envelope [0, 10]: PDPTW uses zero               tomer without counting a return-to-depot leg.
service time, while the remaining time-window
variants sample positive values, with DCVRPHTW                B.3   Feasible Solution Construction
allowing values up to 10. Let d0 be the Euclidean             For each complete instance, we first run a variant-
distance from a customer to the main depot. Cus-              specific heuristic to obtain s+ . The heuristic is
tomer window starts are sampled from intervals                mainly based on nearest-neighbor insertion and
proportional to d0 , lie in [0, 250], and have widths         checks common VRP resource constraints, such as
in [30, 120]. For MDVRPSTW, d0 is instead the                 capacity, route-distance limits, and time windows,
distance to the nearest depot when generating each            at each step. If customers remain uninserted, they
customer’s soft time window; this does not assign             are preferentially inserted into the route with the
the customer to that depot. During initial instance           largest remaining slack. If the heuristic fails, we
generation, PDPSTW and PDPTW first sample                     invoke the reference concrete code Ccon for a time-
pickup windows and then derive the paired deliv-              limited feasibility solve with TimeLimit = 15
ery windows. PDPSTW initializes each delivery-                seconds and MIPFocus = 1. The returned solution
window start as the pickup start plus pickup ser-             is then checked by Ccon through a feasibility asser-
vice and 0.5 times the direct pickup–delivery dis-            tion. If any assertion fails, the candidate sample is
tance, whereas PDPTW uses the pickup start plus               discarded. The resulting s+ is used to construct the
0.3 times that distance with zero service time.               one-constraint-violating solutions {s−  i }.
These windows may subsequently be widened dur-
ing feasibility-preserving relaxation. The time-              B.4   One-Constraint-Violating Solution
boundary family directly uses the (n, k, Q, H) grid                 Construction
in Appendix B.1.
                                                              Each variant v is associated with a perturbation-
Depots, pickup-delivery pairs, backhauls,                     operator set Av = Astruct
                                                                                     v     ∪ Aparam
                                                                                                v    . Each oper-
and open routes. MDVRP, MDVRPSTW, and                         ator transforms s+ into a one-constraint-violating
HFMDVRP use two depots. PDP and PDPSTW                        solution s−
                                                                        i that targets one active constraint family.
set scalar node demand to zero and sample paired              Structural perturbations change only the customer
pickup–delivery demand from [1, 8], whereas                   visiting sequence and do not modify instance pa-
PDPTW uses unit demand for every pair. All                    rameters. Parameter perturbations change the vis-

                                                         15
iting sequence and tighten one family of resource             it from its route; for example, [0, 1, 2, 0] becomes
bounds. We construct these solutions for logical              [0, 1, 0], leaving customer 2 unserved. In SDVRP,
structure constraints such as customer coverage, de-          where a customer may be split across vehicles, the
pot connectivity, and pickup–delivery precedence,             selected customer is removed from every route
                                                                                                     gen
and for common resource constraints such as ca-               that serves any portion of it. If Ccon      omits the
pacity, distance, compartments, and hard time win-            coverage/demand-satisfaction constraint, relaxes
dows. Constraints that mainly affect objective                it to an inequality, or covers only a subset of cus-
penalties rather than producing deterministic in-             tomers, the resulting s−i may be accepted.
feasibility, such as soft time-window penalties, are
handled by the optimal value check.                           Subtour cycle targets depot connectivity con-
   The perturbation operators only generate can-              straints: every route must be connected through
didate solutions. The final labels are assigned               a depot and cannot contain a customer-only cycle.
by checking each candidate instance–solution pair             The operator extracts at least two customers from a
with Ccon . Each s−                         +
                      i is derived from s by one              feasible route and forms a cycle that does not pass
operator and targets one constraint family by con-            through the depot, e.g., a detached cycle such as
struction. If s+ is infeasible on the corresponding                          gen
                                                              [1, 2, 1]. If Ccon omits subtour elimination or only
instance, or if any s− i is not rejected by Ccon , the        enforces local flow balance, the detached cycle
candidate is discarded.                                       may be accepted. SDVRP uses an isolated-subtour
   Each s− i is injected separately into the complete         solution, which additionally removes the cycle cus-
generated model, while all other generated con-               tomers from other routes so that split service cannot
straints remain active. Combining several viola-              reconnect them to the depot.
tions in one solution would make the verdict non-
diagnostic, because the model could reject that so-
                                                              Backhaul order violation targets the VRPB
lution by correctly enforcing any one of the vio-
                                                              linehaul-first rule: all linehaul customers must
lated constraints while still omitting another. We
                      gen                                     precede all backhaul customers on each route,
therefore require Ccon     to accept s+ and reject ev-
      −                                                       equivalently forbidding any transition from a back-
ery si separately. This design isolates individual
                                                              haul customer to a linehaul customer. The op-
constraint-family errors but does not exhaustively
                                                              erator moves a backhaul customer before a line-
test errors that emerge only through interactions
                                                              haul customer, e.g., changing [0, l1 , l2 , b1 , 0] into
among multiple constraints.
                                                              [0, l1 , b1 , l2 , 0]. The optimal value check alone can-
   SDVRP is handled separately because split de-
                                                              not verify that this rule is encoded, because the
livery changes the semantics of coverage, subtours,
                                                              optimum in an enlarged feasible region may not
and capacity. A customer can be served by mul-
                                                              use a reversed edge.
tiple vehicles; removing a customer must remove
all of its delivered portions; a subtour customer
may otherwise be reconnected to a depot through               Precedence violation targets pickup-delivery
another route; and overload can be repaired by re-            precedence. All pickup–delivery variants require
distributing demand across vehicles. Therefore,               each pickup to precede its paired delivery on the
SDVRP uses split-delivery versions of the remove-             same route. PDPTW enforces this through service-
customer and isolated-subtour perturbations, to-              start times, whereas PDP and PDPSTW use route-
gether with two capacity-oriented perturbations:              order variables. The operator swaps the pickup
quarantine overload and phantom delivery. Repeat-             and delivery within the same route, e.g., 0, p, d, 0
edly visiting the same customer is not necessarily            becomes 0, d, p, 0.
a violation under split delivery and is therefore not
used to construct an s−  i .
                                                              Split pickup-delivery pair targets same-vehicle
                                                              coupling for pickup-delivery pairs: each pair (p, d)
B.4.1   Structural Perturbations                              must
                                                                 P be servedP  by the same vehicle, expressible
Remove customer targets coverage or demand-                   as j xp,j,k = j xd,j,k , ∀k. The operator keeps
satisfaction constraints. For standard non-split vari-        the pickup on the original vehicle and moves the
                   P c ∈ N must be visited ex-
ants, every customer                                          delivery into another vehicle route. It exposes mod-
actly once, e.g., i,k xi,c,k = 1. The operator                els that encode precedence but omit same-vehicle
selects a visited customer from s+ and removes                coupling.

                                                         16
B.4.2 Parameter Perturbations                                 For HFVRP and HFVRPHTW, we construct an
Parameter perturbations construct a boundary case             extreme-overload solution: customers are greed-
for one resource. Let g be the resource usage of              ily accumulated into a single route until their to-
the target route, vehicle, or compartment, and let b          tal demand exceeds the maximum capacity of any
be the corresponding resource usage of a perturbed            vehicle, making the route infeasible under any re-
solution s−i , with b > g. Let B̃ be the tightened
                                                              assignment. If this construction fails, the imple-
resource bound in the perturbed instance, such as             mentation falls back to the generic move-overload
capacity Q̃, route-distance limit D̃max , or compart-         perturbation. For heterogeneous multi-depot or
ment bound Q̃c . If B̃ ≤ g, the feasible solution is          multi-compartment variants, the generic overload
incorrectly excluded; if B̃ ≥ b, the one-constraint-          operator tightens only the target vehicle’s capacity,
violating solution no longer violates the resource.           while compartment-specific variants additionally
Thus, except for time-window violations, param-               use compartment-overload solutions. These pertur-
                                                                                      gen
eter perturbations set B̃ inside the open interval            bations test whether Ccon   respects vehicle-specific
(g, b):                                                       capacities rather than replacing them with a single
                                                            homogeneous bound.
 B̃ = max g + ε, min g + 0.85(b − g), b − ε .
                                                (19)          Distance
                                                              P            overrun targets route-distance limits
Here ε > 0 is a small numerical margin ensur-                    i,j ci,j xi,j,k ≤ Dmax for all vehicles k. It moves
ing that B̃ is strictly between g and b. The 0.85             customers into the longest route in s+ so that the
interpolation places the one-constraint-violating so-         perturbed route length b exceeds the largest route
lution close to the boundary, testing whether the             length in s+ , denoted by g, and then tightens Dmax
regenerated model truly encodes that upper bound.             to a value in (g, b). It tests whether the distance
Clipping prevents numerical rounding from mov-                limit is enforced separately for each vehicle and
ing B̃ onto g or b. SDVRP uses a more conservative            computed from all traveled legs of its route.
margin because split-delivery quantities are more
sensitive to rounding. The time-window violation              Compartment overload
                                                                                 P      Ptargets compartment ca-
operator does not use this scalar bound-tightening            pacity constraints i di,c j xi,j,k ≤ Qc for each
rule, because it swaps the visiting order to create           vehicle k and compartment c. Multi-compartment
hard time-window lateness.                                    routing is not captured by total vehicle load: one
                                                              compartment can overflow while the total load still
Capacity
P P overload targets capacity constraints                     appears feasible. The operator concentrates de-
   i di   j xi,j,k ≤ Q for all vehicles k. It moves           mand from one compartment on a vehicle and tight-
one or more customers from other routes into a                ens only that compartment bound while keeping
target route until the target route exceeds the tight-        total vehicle capacity non-binding.
ened capacity. We set g to the target route’s orig-
inal load under s+ and b to the load of the over-             Quarantine overload targets  P the SDVRP per-
loaded target route. We then tighten Q, or the                vehicle capacity constraint i dki ≤ Q for every
target vehicle’s capacity, to a value in (g, b). For          vehicle k, where dki is the portion of customer i
homogeneous fleets, the tightened bound is addi-              served by vehicle k. Ordinary capacity perturba-
tionally kept above the largest route load in s+ ; for        tions can be repaired in SDVRP by redistributing
vehicle-specific bounds, it is applied only to the            demand. This operator fixes the service assignment
target vehicle. The resulting s−  i checks whether
                                                              of the target customers so the diagnostic question
capacity is present and applied per vehicle. VRPB             becomes whether the model still enforces the ca-
computes linehaul and backhaul loads separately               pacity bound for that vehicle.
and uses their maximum. PDP and PDPSTW move
                                                              Phantom delivery targets the coupling between
whole pickup-delivery pairs, and rebuild the target
                                                              vehicle visits and delivered quantities in SDVRP.
route in pickup-before-delivery order, to avoid con-
                                                              Split delivery models commonly use delivery-
founding capacity with same-vehicle or precedence
                                                              allocation variables to indicate how much demand
violations.
                                                              of customer i is served by vehicle k, and these
Heterogeneous fleet overload targets vehicle-                 quantities must be coupled to whether vehicle k
specific capacity constraints, where each vehi-               actually visits customer i. The operator grafts
cle has its own capacity and cost parameters.                 the customers of one active vehicle onto another

                                                         17
capacity-tightened vehicle and deactivates the orig-         Non-target resources may be adjusted only to avoid
inal vehicle’s route. The resulting s−i is infeasible        confounding violations, ensuring that s−   i targets
when visit–delivery coupling is enforced, because            the intended constraint family. We retain a labeled
the tightened vehicle cannot carry the combined              solution only when Ccon verifies s+ as feasible and
demand. If the regenerated model allows a deac-              the corresponding s− i as infeasible on the same in-
tivated vehicle to deliver positive demand without           stance: I ∗ for structural perturbations and Ia∗ for
visiting the customer, the same solution can be              resource-bound perturbations. For each resource-
incorrectly accepted. This exposes models that en-           bound sample, its natural-language description and
code aggregate customer demand satisfaction but              reference concrete code are generated from the
omit the coupling between routing variables and              same Ia∗ .
split-delivery quantities.
                                                             C     Natural-Language Rewriting and Code
Time window violation targets hard time win-                       Regeneration
dow constraints ai ≤ τik ≤ bi . It swaps adjacent
customers in a feasible route while preserving the           This appendix describes Stage 2 of the data syn-
customer set, vehicle assignment, and load, and              thesis pipeline. We use Gemini-3.1-Pro Pre-
then sets narrow windows around the legal arrival            view (Google DeepMind, 2026) and Claude Opus
times in the original route. The resulting s−
                                            i is re-
                                                             4.6 (Anthropic, 2026) as the teacher LLMs in the
tained only if the swapped route violates at least           synthesis pipeline. Within Stage 2, the teacher first
one hard time window under the same windows.                 rewrites the reference concrete code into natural-
                                                                                                              gen
For PDPTW, the operator is precedence-aware and              language descriptions and then regenerates Ccon
avoids swaps that directly invert a pickup-delivery          from each description.
pair, so that the violation remains attributable to
                                                             C.1    Natural-Language Rewriting
time windows rather than precedence. Soft-time-
window variants do not use this operator because             Scenario instantiation. The main path rewrites
time-window violations are penalized rather than             Ccon into a natural-language problem statement
infeasible.                                                  p0 organized into business background, resources,
                                                             constraints, and objective. It uses a generate–
B.5   Instance Relaxation and Assembly                       critique–repair loop: the teacher first produces a
Resource-bound perturbations require an open in-             draft, a critic then checks numerical completeness,
terval between the resource usage of the feasible            constraint coverage, objective direction, absence of
solution s+ and that of the corresponding one-               fabrication, ID–attribute binding, and unit plausibil-
constraint-violating solution s−                             ity, and a repair call edits only the parts identified
                                  i . After obtaining
  +
s , we therefore apply one-way relaxation to the             as inconsistent. Each call is given a deterministic
bounded resource families present in each variant,           scene–style hint, described below.
such as vehicle capacity, route-distance limits, and         Condensation. The first augmentation path re-
time windows. Capacities and route-distance lim-             moves solver-side or formulation-side wording
its are widened relative to the load or route length         from p0 while preserving the optimization prob-
of s+ , while time-window variants receive addi-             lem. Typical deletions include self-loop prohibi-
tional slack around the service times induced by             tions, explicit in-degree or out-degree formulations,
s+ . This step only enlarges the feasible region, so         subtour-elimination wording, and explanatory ref-
s+ remains feasible while later operator-specific            erences to virtual depots or sink nodes when they
tightening has room to place the target bound be-            are only modeling devices. Two prompt variants
tween the usage of s+ and s−  i .                            are used: a permissive version that allows such dele-
         ∗
   Let I denote the relaxed instance used as the             tions, and a stricter version that forces virtual-node
sample instance before perturbation-specific tight-          wording to be replaced by natural route-termination
ening. Structural perturbations are evaluated di-            statements. Outputs that fail static fidelity checks
rectly on I ∗ , since their violations are induced           are repaired through minimal local edits.
by route structure rather than numerical resource
bounds. For each resource-bound operator a, we               Index rewriting. The second augmentation path
create a perturbation-specific copy Ia∗ and tighten          changes node identifiers in p0 or pcond while pre-
only the intended resource bound on that copy.               serving all other semantics. The target style is

                                                        18
 Variant         Structural perturbations                            Parameter perturbations
 TSP             Base pair                                           –
 CVRP            Base pair                                           Capacity overload
 MDVRP           Base pair                                           Capacity overload
 MCVRP           Base pair                                           Capacity overload; compartment overload
 PDP             Base pair; precedence violation; split pickup-      Capacity overload
                 delivery pair
 OVRP            Base pair                                           Capacity overload
 DCVRP           Base pair                                           Capacity overload; distance overrun
 VRPB            Base pair; backhaul order violation                 Capacity overload
 SDVRP           Split delivery base pair                            Quarantine overload; phantom delivery
 VRPHTW          Base pair                                           Capacity overload; time window violation
 VRPSTW          Base pair                                           Capacity overload
 HFVRP           Base pair                                           Capacity overload; heterogeneous fleet overload
 HFMDVRP         Base pair                                           Capacity overload
 HFMCVRP         Base pair                                           Capacity overload; compartment overload
 HFVRPHTW        Base pair                                           Capacity overload; heterogeneous fleet overload;
                                                                     time window violation
 MDVRPSTW        Base pair                                           Capacity overload
 PDPSTW          Base pair; precedence violation; split pickup-      Capacity overload
                 delivery pair
 PDPTW           Base pair; precedence violation                     Time window violation
 OVRPHTW         Base pair                                           Capacity overload; time window violation
 MCVRPSTW        Base pair                                           Capacity overload; compartment overload
 DCVRPHTW        Base pair                                           Capacity overload; distance overrun; time window
                                                                     violation

Table 6: Perturbation operators enabled for the 21 variants. Base pair denotes the remove-customer and subtour-cycle
perturbations. Split-delivery base pair denotes the SDVRP-specific remove-customer and isolated-subtour pertur-
bations. Structural perturbations modify only the visiting sequence, whereas parameter perturbations additionally
tighten one target resource family.


deterministically selected from three options: con-           straints, and objective; and use precise conservative
secutive one-based integer identifiers, consecutive           wording that avoids storytelling and remains easy
integer identifiers starting from 2, or uppercase let-        to parse into a mathematical model.
ter identifiers. The rewrite call must also return
a one-to-one node_id_map. This map is required                C.2    Code Regeneration
downstream because s+ and {s−     i } are constructed         Each problem description p ∈ {p0 , pcond , pidx } is
     ∗
on I using source node IDs; the verifier must                 then sent to the code-regeneration prompt to ob-
                                                                     gen
translate the reference solutions into the rewritten          tain Ccon  . The same code-generation instruction
naming space before applying Inj.                             template and output protocol are used when con-
                                                              structing SFT examples, during GRPO rollouts,
Scene and style configuration. Scenario instan-               and in final evaluation.
tiation appends a deterministic scene–style hint to
the rewriting prompt. The scene pool contains 60              D     Constraint-Injection Encoding Details
entries and the style pool contains three entries.
                                                              This appendix provides implementation details for
Both are selected from a seed derived from the
                                                              the Inj check introduced in Section 4.2. Given
sample triple (variant, seed, profile), so rerunning             gen                              gen
                                                              (Ccon  , s), the verifier executes Ccon to obtain the
the same sample yields the same scene and style.
                                                              Gurobi model, copies the model, replaces the ob-
The template contains no additional random per-
                                                              jective with a constant, and appends the solution-
turbation. The unit hints are drawn from a small
                                                              encoding constraints Φ(s). The resulting model
set of base unit families, including tons, kilograms,
                                                              is solved only as a feasibility query; its objective
liters, kWh, seat-kilometers, and order-equivalents,
                                                              value is ignored.
sometimes with domain-specific modifiers. The
three style instructions are: use a concise academic-         Variable parsing and index alignment. The ver-
problem style similar to a benchmark or methods               ifier searches for routing variables named x, fol-
paper; use a formal optimization-problem style                lowing the output protocol in Appendix H. It sup-
with stable ordering from background to data, con-            ports both two-dimensional arc variables and three-

                                                         19
dimensional arc–vehicle variables, provided that                be split across vehicles. The SDVRP-specific one-
their indices follow the arc-first convention spec-             constraint-violating solutions in Appendix B.4, in-
ified by the output protocol. For index-rewritten               cluding quarantine overload and phantom delivery,
statements, the recorded node_id_map is used to                 therefore prevent the violation from being repaired
translate the routes in s back to the internal node in-         by redistributing the same customer’s demand to
                       gen
dices expected by Ccon     . If the routing variables or        another vehicle. This keeps the Inj query aligned
node indices cannot be matched reliably, the case               with the targeted capacity or visit–delivery cou-
is not used as a valid Inj verdict and the sample               pling constraint.
fails rejection sampling.
                                                                Verdict handling. The feasible solution s+
Homogeneous-fleet injection. For homo-                          passes Inj when the solution-encoded model is
geneous fleets, s+ is encoded through a                         feasible. A one-constraint-violating solution s−  i
vehicle-agnostic customer–customer projection:                  passes Inj when the solution-encoded model is
customer–customer arcs appearing in s+ are                      infeasible. Cases with model-construction fail-
required, customer–customer arcs absent from s+                 ures, unsupported variable formats, unreliable node
are forbidden, customer self-loops are blocked,                 matching, or unresolved solver statuses are treated
and intentionally unvisited customers have their                as verification failures during rejection sampling.
incoming arcs blocked. Vehicle identities remain
free. For each s−                                               E   Training Details
                 i , the verifier additionally applies
the route-level consistency constraints in Eq. (12),            Implementation environment. All optimization
so that the customer–customer edges of the same                 solves in data synthesis, verification, training-time
diagnostic route cannot be distributed across                   reward computation, and evaluation are conducted
interchangeable vehicles.                                       with Gurobi Optimizer under an academic license.
                                                                The main SFT and GRPO runs share one LoRA
Heterogeneous-fleet injection. For heteroge-
                                                                adapter configuration with rank r = 16, α = 32,
neous fleets, the verifier uses the vehicle-specific
                                                                and dropout 0.1. All model calls use the shared
fixing described in Section 4.2. This preserves the
                                                                code-regeneration system prompt in Appendix H.
vehicle assignment carried by the injected solu-
tion, which is necessary when capacities, costs, or             SFT. We apply LoRA SFT to Qwen3-8B on
resource bounds depend on vehicle type. In this                              gen
                                                                6,797 (p, Ccon   ) pairs. Training uses four A100-
case, both s+ and {s− i } are injected with vehicle             40GB GPUs, per-device batch size 1, gradient ac-
identities fixed.                                               cumulation 2, and global effective batch size 8. We
                                                                train for 3 epochs with sequence length 8192. The
Depot edges. The main injection encoding fo-
                                                                optimizer is AdamW with learning rate 2 × 10−4 ,
cuses on customer–customer transitions and does
                                                                cosine scheduling, warmup ratio 0.1, weight decay
not use depot-departure or depot-return patterns as
                                                                0.01, and maximum gradient norm 1.0.
primary evidence for the injected solution. It there-
fore does not directly test every depot-structure               Frontier filtering. For each prompt in the SFT
constraint; such errors are detected by the optimal             pool, we sample H = 6 offline rollouts from
value check only when they change the optimum.                  VRPCoder-SFT under the same decoding settings
For a small number of one-constraint-violating so-              as online GRPO (temperature 0.4, top-p 0.95),
lutions, the verifier adds solution-specific depot-             score each rollout with the dual verifier under the
edge restrictions to prevent degenerate repairs, such           GRPO reward weights, and retain only prompts
as serving an intentionally unvisited customer out-             whose within-group reward standard deviation is
side the encoded route structure or reassigning                 strictly positive. This yields the 716 frontier
an isolated SDVRP customer to another vehicle.                  prompts used in the main GRPO run.
These restrictions preserve the intended solution
semantics and are not used as a general test of                 GRPO. Starting from the SFT checkpoint, we
depot-structure constraints.                                    train on 716 frontier prompts. Policy training uses
                                                                three A100-40GB GPUs with DeepSpeed ZeRO-
Split-delivery solutions. For SDVRP, the veri-                  2 (Rasley et al., 2020), while one additional A100-
fier must preserve the service assignment in the                40GB GPU runs a vLLM (Kwon et al., 2023) server
injected solution because customer demand may                   for rollouts. The per-device batch size is 1, gradient

                                                           20
accumulation is 8, and the global effective batch             Source or slice    Group              N Pass@1 (%)
size is 24. We train for 3 epochs. For each prompt,           Subsets 1–2        0 active modules 25          100.00
we sample G = 8 rollouts with a maximum com-                  Subsets 1–2        1 active module   20         100.00
                                                              Subsets 1–2        2 active modules 191          95.81
pletion length of 3072, temperature 0.4, top-p 0.95,          Subsets 1–2        3 active modules 140          95.71
and KL coefficient β = 0.02. The optimizer is
                                                              TSPLIB             TSP                16        100.00
AdamW with β2 = 0.95, learning rate 2 × 10−5 ,                CVRPLIB            CVRP               15        100.00
cosine scheduling, 5 warmup steps, weight decay               Solomon            VRPTW              11         81.82
0.01, and maximum gradient norm 0.5.                          Cordeau-MDVRP      MDVRP               7         85.71
                                                              SDVRPLIB           SDVRP              13         92.31
                                                              VRPB               VRPB               12         91.67
No-injection ablation. For the no-injection ab-
lation, we retrain the SFT checkpoint on 7,347                Cleaned SIRL       TSP/VRP            50        100.00
                                                              NLCO               TSP                50         92.00
samples. Compared with the main 6,797-sample                  NLCO               CVRP               50         90.00
SFT set, the additional 550 samples pass the op-              NLCO               TSPTW†             50         74.00
timal value check but fail constraint injection and           NLCO               PDPTW              50         84.00
are therefore rejected by the main pipeline. All
                                                             Table 7: VRPCoder-RL Pass@1 by active-module count
other SFT hyperparameters are unchanged. For                 and evaluation source or task. † denotes a variant absent
GRPO, we remove rinj from the reward and keep                from training.
only build success and the optimal value check, so
the maximum reward becomes 0.7 under the origi-
nal weights. We then generate new rollouts from              95.81% and 95.71% Pass@1 on variants with two
the 7,347-sample no-injection SFT checkpoint and             and three active constraint modules, respectively.
apply the same positive-variance frontier filtering
without injection verification, yielding 855 fron-           G    Evaluation Benchmarks and Protocol
tier prompts. Decoding, learning rate, scheduling,           VRPBench comprises four subsets with 700 total
LoRA configuration, and effective batch size re-             instances, ranging from in-domain synthesis to ex-
main aligned with the main GRPO run.                         ternally sourced problems. All problem statements
                                                             and reference answers are manually verified by
F   Constraint-Level Error Analysis
                                                             operations-research experts.
Across several rounds of synthesis and regenera-
tion, 7,347 candidates passed the optimal value              Subset 1: In-domain synthetic. This subset con-
check, among which 550 (7.49%) failed constraint             tains 310 instances generated by the three-stage
injection. Among the 450 silent-omission cases,              data synthesis pipeline on the 18 training variants
the failures were associated with the base struc-            with a separate set of random seeds. Samples are
tural pair (268), hard time windows (56), backhaul           retained after the same dual verifier procedure used
ordering (44), capacity (30), distance limits (24),          for training data.
compartment capacity (21), precedence (5), and               Subset 2: Out-of-domain synthetic. This sub-
split pickup–delivery coupling (2). Here, the base           set contains 66 instances generated by the same
structural pair denotes the remove-customer and              pipeline on the three held-out variants OVRPHTW,
subtour-cycle solutions. Among the 100 spurious-             MCVRPSTW, and DCVRPHTW. The individual
over-constraint cases, the failures involved distance        constraint modules in these variants appear in train-
limits (40), vehicle capacity (38), hard time win-           ing, but the corresponding pairwise combinations
dows (21), and compartment capacity (1). To ex-              are never observed during training, making this
amine whether these synthesis-time patterns persist          benchmark a test of compositional generalization.
after training, Table 7 reports final performance by
active-module count and evaluation source or task.           Subset 3: Public OR libraries. This subset
                                                             contains 74 instances derived from public OR li-
  Hard time windows appear in both synthesis fail-           braries, including TSPLIB (Reinelt, 1991), CVR-
ure modes and remain challenging in final eval-              PLIB (Uchoa et al., 2017), Solomon (1987),
uation: VRPCoder-RL obtains 81.82% Pass@1                    Cordeau-MDVRP (Cordeau et al., 1997), SDVR-
on Solomon VRPTW and 74.00% on the unseen                    PLIB (Belenguer et al., 2000), and VRPB (Toth
NLCO TSPTW task. Aggregating Subsets 1 and                   and Vigo, 1997). It covers TSP, CVRP, VRPTW,
2 by variant complexity, VRPCoder-RL achieves                MDVRP, SDVRP, and VRPB. Since the original

                                                        21
public instances often contain tens to hundreds of
customers, we extract 5–12-customer subinstances
while preserving real coordinates, demands, time
windows, multi-depot structure, split delivery, or
backhaul structure when present. OR experts then
write the natural-language statements after down-
sampling, ensuring that all numerical and structural
constraints remain consistent.
Subset 4: Externally sourced. This subset con-
tains 250 instances. The first 200 come from the
routing subset of NLCO (Jiang et al., 2026), cov-
ering TSP, CVRP, TSPTW, and PDPTW with 50
small instances per type. We make two lightweight
adaptations: removing the JSON output-format and
reasoning instructions from the original prompts,
and adding the annotated vehicle count to CVRP
statements because code-generation tasks require
the fleet size to be explicit. The surface format and
indexing scheme of NLCO are otherwise preserved.
The remaining 50 instances come from the cleaned
SIRL release (Chen et al., 2025), which aggregates
OptMATH (Lu et al., 2025), IndustryOR (Huang
et al., 2025a), and MAMO (Huang et al., 2025b);
we extract all TSP and VRP variants, consisting
of 9 OptMATH, 2 IndustryOR, and 39 MAMO
ComplexLP cases.
Evaluation. All four subsets use instance-level
Pass@1 with absolute objective tolerance 10−3 , a
600-second Gurobi time limit per instance, and
greedy decoding. Trained models use the shared
code-regeneration system prompt in Figure 11;
OR-LLM baselines use their original prompts and
solver settings.

H    Prompts Used in Experiments
This appendix collects all prompt texts used in the
paper. Placeholders in braces are filled by the data-
generation scheduler at runtime.




                                                        22
Scenario Instantiation: System Prompt

You are an operations research expert. Given Gurobi solver code, produce a formal English business
problem description suitable as code−generation training data.
Data fidelity:
1. Preserve ALL numerical data exactly (coordinates, demands, capacities, fleet size, time windows,
service times, max distances, etc.). Do not omit, invent, or round any number.
2. State the optimization objective and every constraint in business language. No math symbols,
variable names, or code jargon.
3. Index preservation (critical): every vehicle, customer, and depot must carry its explicit numeric
ID from the code. Write "Truck 0 (capacity 50.0, fixed cost 70.0)" −− never describe entities by type
alone without their ID. Never renumber or reorder.
Unit consistency:
4. Demand/capacity values may be fractional (e.g. 3.4). Use continuous units only (tons, kilograms,
liters). Never use bare countable nouns (pallets, boxes, items) −− "3.4 pallets" is nonsensical.
5. If the problem has time−window or scheduling constraints, do NOT also use time−based units for
demand/capacity −− this creates a logical contradiction. Use a tangible goods unit instead.
Style:
6. Structure: background −> resources/data −> operational constraints −> objective.
7. Plain prose only. No Markdown, no bullets/tables/dialogue/email tone.
8. If a scene hint is given, adapt terminology naturally while preserving the optimization structure.

Scenario Instantiation: User Prompt

Generate a natural−language business problem statement from the code below.
===== Scene and Style Instructions =====
{scene_hint}
===== Gurobi Code (with complete data) =====
{code}
===== Critical Numbers That Must Appear =====
Embed each number naturally in context (e.g. "a capacity of 50.0"), do not list them as a bare table:
{critical_numbers_str}
Output the problem description directly:

                                Figure 6: Scenario Instantiation Prompts.




                                                   23
Self-Critique: Critic System Prompt

You are a strict reviewer. Compare the Gurobi code with the generated NL description for full
consistency.
Check these dimensions:
1. Numerical completeness: all critical values (depot/customer/vehicle counts, capacities, demands,
coordinates, time windows, etc.) present?
2. Constraint coverage: every code constraint has a corresponding business description?
3. Objective: optimization direction correctly stated?
4. No fabrication: no numbers or conditions invented beyond the code?
5. Index−attribute binding: every entity carries its numeric ID, and ID−to−attribute mappings (ID
−> capacity, cost, type) are faithful to the code? Missing or ambiguous IDs = INCOMPLETE.
6. Unit plausibility: demand/capacity units are continuous (not countable nouns) and do not conflict
with time−window dimensions?
Output exactly one of:
− COMPLETE
− INCOMPLETE: <discrepancy_1> | <discrepancy_2> | ...

Self-Critique: Critic User Prompt

Please compare the following content and determine whether the natural−language description fully
and accurately reflects the optimization problem in the code:
===== Gurobi Code (with complete data) =====
{code}
===== Generated Natural−Language Description =====
{nl_description}
Please provide the evaluation result:

Repair: System Prompt

You are an operations research expert.
Revise the natural−language problem description based on the review feedback so that it is fully
consistent with the original mathematical problem.
Rules:
1. Only modify the parts identified as problematic.
2. Preserve the correct and fluent parts of the original description.
3. Ensure all critical numbers appear accurately after revision.
4. Do not introduce new errors.

Repair: User Prompt

Review feedback: {criticism}
Original code and data: {code}
Current natural−language description: {nl_description}
Please output the revised complete natural−language description (only modify the parts identified as
problematic; preserve the correct parts):

Figure 7: Self-Critique and Repair Prompts. Critic and repair prompts used in the generate–critique–repair loop.




                                                      24
 Condensation: Shared System-Prompt Skeleton
 You condense verbose vehicle−routing problem statements into shorter business−requirement
 descriptions. The rules are specified as follows:
 1. Preserve every numeric value exactly as written. Do not delete, alter, round, merge, or restate
 numbers in a different form.
 2. Preserve every explicit entity ID exactly as written. Do not renumber, reorder, relabel, or collapse
 depots, customers, vehicles, compartments, pickup−delivery pairs, or any other named entities.
 3. Preserve every fact that changes the optimization problem: objective terms, route start/end
 behavior, depot assignment, fleet size, capacities, coordinates, demands, service times, time
 windows, maximum distance or duration, fixed or travel costs, heterogeneous vehicle attributes,
 compartment rules, pickup−delivery logic, backhaul ordering, split−delivery permission, and any
 other operational restriction.
 4. Keep the original business scene and terminology. This is condensation, not stylistic rewriting.
 5. <See variant−specific block below>
 6. Micro−examples of allowed compression: (1) "each node has exactly one incoming arc and
 exactly one outgoing arc" can usually be shortened to "each customer/location must be visited
 exactly once" if route start/end behavior is already clear elsewhere. (2) "no self−loops, no arcs into
 depot 0, no arcs out of sink 13" can be deleted if these are only solver−hygiene details and the route
 endpoints are already clear.
 7. Merge duplicated statements into one concise statement. Remove tutorial tone, repeated
 reminders, and repeated restatements of the same requirement.
 8. Prefer plain prose. Do not output bullets, markdown, JSON, XML, commentary, or surrounding
 quotation marks.
 9. If the source is already concise, make only small cuts.
 Output only the condensed problem statement.
 Condensation: Rule 5 for Pilot 1
 5. You MAY delete solver−side or formulation−side wording when it is not real business content.
 Typical deletable items include self−loop prohibitions, forbidden−arc wording such as "no arcs into
 the start depot" or "no arcs out of the sink", exact in−degree / out−degree phrasing, explicit
 subtour−elimination wording, and explanations of why a virtual depot or sink is introduced.
 Condensation: Rule 5 for Pilot 2
 5. You MUST delete ALL virtual−node wording. Specifically remove: (1) Any mention of "virtual
 depot", "virtual sink", "virtual return node", "dummy node" and their node IDs when used only as
 route endpoints. (2) Sentences like "Upon completing their routes, all trucks must proceed to Virtual
 Distribution center N". (3) Replace with natural route termination: "All vehicles return to the depot
 after completing deliveries" (closed routes) or "Vehicles do not need to return to the depot" (open
 routes). You may also delete other solver−side wording (self−loop prohibitions, forbidden−arc
 phrasing, explicit in−degree / out−degree constraints, subtour−elimination wording).
 Condensation: User Prompt
 Variant: {variant}; Condensation task: Turn the following source description into a shorter
 business−requirement description. Keep the same scene, terminology, numbers, IDs, objective, and
 operational constraints. You may compress duplicated explanations and solver−side wording such
 as self−loop or forbidden−arc phrasing when the business meaning is already clear. Do not
 introduce a new writing style.
 Source description: {original_nl}
 Output only the condensed problem statement.
Figure 8: Condensation prompts. The prompt template used for condensation, consisting of a shared system-prompt
skeleton, pilot-specific Rule 5 instructions, and the corresponding user prompt.



                                                      25
Index Rewriting: System Prompt

Rewrite the VRP problem statement by replacing node/location identifiers only.
Rules:
1. First identify every node/location identifier that appears in the source text: depots, customers,
pickup nodes, delivery nodes, virtual depots, sink nodes, endpoint nodes, start nodes, and end nodes.
2. Replace all of those node/location identifiers consistently using the requested target style.
3. Create the node−ID mapping yourself from the source text. Do not rely on any external mapping
table.
4. Do not change vehicle IDs or any non−ID number.
5. Preserve all constraints and business meaning.
6. Do not add nodes or virtual−node details that are absent from the source.
7. Report the exact mapping you used in the JSON field node_id_map.
8. Do not output markdown, explanations, or commentary.
Output JSON only:
{
  "rewritten_nl": "...",
  "node_id_map": [
    {"source_id": "0", "target_id": "A", "role": "start_depot"},
    {"source_id": "7", "target_id": "B", "role": "virtual_end_depot"}
  ]
}

Index Rewriting: User Prompt

Variant: {variant}
Target style: {target_style}
Source description: {original_nl}
Rewrite the source by replacing every node/location identifier that appears in it. Include physical
depots, customer nodes, pickup/delivery nodes, and virtual/sink/end depots if they appear. Decide
the mapping yourself from the source text and keep it consistent. Preserve everything else. Return
JSON only with rewritten_nl and node_id_map. node_id_map must list every source node/location
identifier you replaced and the exact target identifier used in rewritten_nl.

                                  Figure 9: Index Rewriting Prompts.




                                                 26
Index Rewriting Check: System Prompt

You check node−identifier rewrites for VRP problem statements.
Return JSON only with these fields:
{
  "passed": true/false,
  "missing_replacements": [],
  "leaked_source_ids": [],
  "added_absent_nodes": [],
  "mapping_issues": [],
  "issues": []
}
Compare the source statement, rewritten statement, and node_id_map directly. Check only
node/location/depot/customer/pickup/delivery/virtual/sink/end identifiers. Do not treat vehicle IDs,
coordinates, capacities, demands, costs, times, route counts, vehicle counts, or objective values as
node IDs. If a source virtual/sink/end node is present, it must be replaced and included in
node_id_map. If a virtual/sink/end node is absent from the source, it must not be added in the
rewrite. The rewrite should consistently use the requested target style. node_id_map must describe
the actual replacements used in rewritten_nl, must be one−to−one for node identifiers, and must not
include vehicle IDs or non−node numeric values.

Index Rewriting Check: User Prompt

Target style: {target_style}
Source statement: {original_nl}
Rewritten statement: {rewritten_nl}
Reported node_id_map: {node_id_map}
Check whether every node/location identifier that appears in the source statement has been
consistently rewritten in the rewritten statement and correctly recorded in node_id_map. Pay special
attention to virtual depots, sink nodes, endpoint nodes, start depots, and end depots. Return JSON
only.

                              Figure 10: Index Rewriting Check Prompts.




                                                 27
 Code Regeneration: System Prompt

 You are an operations research expert. Given a natural−language business problem, generate
 complete Gurobi Python solver code.
 Output ONLY code wrapped in a Python fenced code block. No explanations, no commentary.

 Code structure:
 1. import gurobipy as gp and from gurobipy import GRB.
 2. Define def build_model(): containing all model logic. It must call m.optimize() and return the
 model object.
 3. Set m.setParam(’OutputFlag’, 0) before optimize.
 4. Model ALL constraints described in the problem −− omit none, fabricate none.
 5. Use exact numerical values from the problem description.

 Index convention:
 − Use internal integer node indices 0..N−1 for routing variables, where N is the total number of
 routing nodes: depots, customers, pickup/delivery nodes, and explicit virtual/end nodes if present.
 − If the problem already uses natural zero−based node IDs, use them directly as model indices. In
 this case, depot is usually node 0, customers are the following nodes, and no node ID mapping is
 needed.
 − If the problem uses any other node ID scheme, such as one−based IDs or simple letter IDs, keep
 those original IDs only in raw data, then map them to internal indices with node_ids = [...], id2idx =
 {bid: i for i, bid in enumerate(node_ids)}, idx2id = {i: bid for bid, i in id2idx.items()}, and N =
 len(node_ids).
 − Use input order as node_ids order. Convert every node−indexed attribute through id2idx when a
 mapping is used: depot IDs, customer IDs, coordinates, demands, service times, time windows,
 pickup−delivery pairs, virtual/sink depots, and start/end nodes.
 − Use node IDs exactly as stated in the problem. Do not invent labels such as Customer A, Node A,
 Location A, Depot A, Outlet 7, or Hub 0.
 − Index fidelity: preserve every ID−to−attribute mapping exactly as described, e.g., Truck 0 capacity
 30 means vehicle 0 gets capacity 30. Never reorder or reassign.
 − Vehicle IDs are not part of this identifier augmentation requirement; keep the vehicle convention
 0..K−1 unless the problem explicitly specifies otherwise.

 Variable format (critical for verification):
 − Route variable MUST be named x with name=’x’ in addVars, indexed arc−first: x[i,j] or x[i,j,k]
 (i=origin, j=destination, then vehicle/depot). Never x[k,i,j] or x[(i,j),k].
 − x MUST span the full node set, e.g., m.addVars(N, N, K, vtype=GRB.BINARY, name=’x’). Do
 NOT pre−filter arcs with tuplelist; forbid invalid arcs via constraints instead.
 − When a mapping is used, set N = len(node_ids) and define x over internal integer node indices.
 Do not use string/letter business IDs directly as x indices.

 Code Regeneration: User Prompt

 {nl_description}

                                                            gen
Figure 11: Shared code-regeneration prompt used to produce Ccon during data synthesis, to generate GRPO rollouts,
and to evaluate trained models.




                                                      28
ID   Scene                          Depot term                      Customer term               Vehicle term
 1   Classical Distribution Plan-   distribution center             customer                    vehicle
     ning
 2   Retail Store Replenishment     warehouse                       retail store                delivery truck
 3   E-commerce Order Fulfill-      fulfillment center              delivery address            delivery van
     ment
 4   Wholesale Grocery Supply       regional distribution hub       grocery outlet              supply truck
 5   Cold-Chain Food Distribu-      cold storage facility           supermarket                 refrigerated truck
     tion
 6   Dairy Product Delivery         dairy processing plant          convenience store           insulated vehicle
 7   Urban Parcel Last-Mile De-     local sorting station           residential address         courier van
     livery
 8   Meal Delivery Dispatch         cloud kitchen hub               diner location              delivery rider
 9   Factory Parts Supply           parts warehouse                 assembly workstation        AGV cart
10   Construction Material De-      building material yard          construction site           flatbed truck
     livery
11   Pharmaceutical Distribu-       pharma distribution center      hospital pharmacy           medical transport vehicle
     tion
12   Home Healthcare Visiting       community health center         patient residence           nurse dispatch vehicle
13   Municipal Waste Collec-        waste treatment plant           collection point            garbage truck
     tion
14   School Bus Routing             school campus                   student pickup stop         school bus
15   Power Grid Maintenance         maintenance depot               substation                  service crew vehicle
16   Telecom Equipment Repair       telecom operations center       base station site           field engineer van
17   Agricultural Produce Col-      produce purchasing station      farm                        collection truck
     lection
18   Livestock Feed Distribu-       feed mill                       livestock farm              bulk feed truck
     tion
19   Disaster Relief Supply         relief staging area             shelter site                relief vehicle
20   Hazardous Waste Trans-         licensed disposal facility      industrial generator site   hazmat transport vehicle
     port
21   Urban Logistics Delivery       distribution center             delivery address            freight truck
22   Food Delivery Dispatch         delivery station                merchant/customer           delivery rider
23   Express Parcel Pickup          courier hub                     pickup point                pickup van
24   Furniture Last-Mile Deliv-     furniture warehouse             customer apartment          moving van
     ery
25   Laundry Pickup and Deliv-      laundry processing center       hotel/household             laundry van
     ery
26   Fresh Food Cold Chain          cold storage warehouse          grocery supermarket         refrigerated truck
27   Seafood Cross-City Trans-      seafood wholesale market        seafood restaurant          live fish transport truck
     port
28   Bakery Product Distribu-       central bakery                  cafe/pastry shop            bread delivery van
     tion
29   Frozen Meal Delivery           frozen food warehouse           vending kiosk               freezer van
30   Agricultural Product Col-      produce purchasing station      farm plantation             farm transport vehicle
     lection
31   Flower Wholesale Distribu-     flower auction center           florist shop                climate-controlled van
     tion
32   Vending Machine Restock-       restocking warehouse            vending machine location    restocking van
     ing
33   Bookstore Chain Replen-        book distribution center        bookstore branch            delivery truck
     ishment
34   Bike-Sharing Battery Swap      battery swap station            bike parking spot           maintenance dispatch vehi-
                                                                                                cle
35   Ride-Hailing / Custom Bus      vehicle hub                     boarding stop               shuttle bus
36   Drone Last-Mile Delivery       drone base station              community receiving tower   logistics drone
37   Autonomous Vehicle Deliv-      AGV dispatch station            office building drop-off    AGV delivery robot
     ery
38   EV Charging Truck Dis-         mobile charging depot           stranded EV location        mobile charger truck
     patch
39   Medical Supply Delivery        pharmaceutical distribution     community clinic/hospital   medical cold chain vehicle
                                    center
40   Blood Bank Distribution        central blood bank              surgical hospital           blood transport vehicle

                    Table 8: Scene hint pool, part I. Entries 1–40 of the 60-entry scene pool.




                                                               29
ID   Scene                         Depot term                      Customer term                 Vehicle term
41   Mobile Home Nursing           community health center         patient household             visiting nurse
42   Mobile Vaccination Ser-       disease control center          temporary vaccination site    mobile medical vehicle
     vice
43   Medical Waste Collection      medical waste treatment         fever clinic                  special collection truck
                                   plant
44   Organ Transport Coordina-     transplant    coordination      recipient hospital            emergency medical vehicle
     tion                          center
45   Municipal Waste Collec-       landfill site                   residential waste station     garbage truck
     tion
46   Snow Removal / De-icing       municipal works depot           major traffic intersection    snowplow
47   School Bus Service            school campus                   student pickup point          school bus
48   Mobile Library Tour           city central library            remote community branch       mobile library van
49   Street Light Maintenance      city lighting depot             faulty lamppost location      maintenance bucket truck
50   Armored Cash Transport        vault center                    bank branch/ATM               armored transport vehicle
51   Factory JIT Parts Delivery    line-side warehouse             assembly line station         AGV transport robot
52   Port Container Dispatch       container yard                  berth/cargo ship              straddle carrier
53   Semiconductor       Wafer     cleanroom storage               fabrication tool bay          overhead transport robot
     Transport
54   High-Voltage Grid Inspec-     power maintenance base          transmission tower/substa-    drone/inspection vehicle
     tion                                                          tion
55   Telecom Base Station Re-      telecom operations center       faulty base station           repair engineer
     pair
56   Wind Farm Turbine Main-       wind farm service center        wind turbine                  maintenance crew vehicle
     tenance
57   Offshore Oil Platform Sup-    onshore supply base             offshore drilling platform    offshore supply vessel
     ply
58   Mine Ore Transport            ore processing plant            mining site                   heavy-duty mining truck
59   Earthquake Relief Distribu-   emergency relief tent/depot     displaced persons shelter     rescue helicopter/off-road
     tion                                                                                        vehicle
60   Forest Fire Patrol            forestry fire prevention cen-   key forest      observation   forest patrol vehicle
                                   ter                             point

                   Table 9: Scene hint pool, part II. Entries 41–60 of the 60-entry scene pool.




                                                            30
