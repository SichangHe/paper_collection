                                                           C ORE: Conflict-Oriented Reasoning Elimination for
                                                                   Verifiable Language-Model Search

                                                            Siyu Song1 , Rui Xu2 , Jia Lin3 , Kai Liu1 , Weifang Wang1
                                          1
                                            School of Computer Science and Technology, School of Computer Science and Engineering
                                                    2
                                                      School of Information Science and Engineering, Sun Yat-sen University
                                                          3
                                                            College of Computer Science, College of Computer Science



                                                                Abstract                               “thoughts” are not solver literals, critiques need not
                                                                                                       be logically sufficient, and approximate verifiers
                                             Test-time reasoning systems often respond to
arXiv:2609.39069v1 [cs.CL] 30 Sep 2026




                                             failure by restarting or revising the latest step,
                                                                                                       may reject valid reasoning. A precise interface
                                             even when an earlier decision caused the error.           among the proposer, verifier, and search controller
                                             We introduce C ORE, a search controller that              is therefore required.
                                             requests a certified conflict core from a verifier,          We propose C ORE (Conflict-Oriented
                                             backjumps to the latest decision in that core,            Reasoning Elimination), a test-time algo-
                                             and caches the conflict to avoid repeating it.
                                                                                                       rithm for tasks whose partial decisions can be
                                             Under sound verification, finite branching and
                                             depth, and exhaustive proposals, the uncapped             checked. The model proposes structured decisions
                                             search is complete and never prunes a valid               with stable identifiers. On rejection, the verifier
                                             solution. On 2,000 planted graph-coloring in-             returns a conflict core: a subset of active decisions
                                             stances with matched proposals and an exact               that cannot occur together in any valid completion.
                                             verifier, C ORE reduces median verifier calls by          C ORE learns this core, backjumps to its most
                                             39.8% at 30 variables and 35.0% at 36 variables           recent member, and continues from there. A
                                             relative to chronological repair; caching further
                                                                                                       core may come from a symbolic checker, an
                                             improves on backjumping alone. Across five
                                             reasoning tasks, C ORE achieves 75.9% mean                unsatisfiable core, a failed program test with
                                             success with Qwen2.5-7B-Instruct and 84.2%                dynamic dependencies, or a learned verifier. Only
                                             with Qwen3-8B, compared with 72.5% and                    sound cores receive the paper’s formal guarantee.
                                             81.8% for Tree of Thoughts. It also uses fewer            Figure 1 summarizes the separation between
                                             verifier calls and generated tokens on both back-         generation, checking, and conflict-directed control.
                                             bones. These results show the value of using
                                             certified failure explanations to direct language-
                                                                                                          Our contributions are:
                                             model search.

                                         1   Introduction                                                 • We introduce a conflict-producing reason-
                                                                                                            ing interface and C ORE, combining non-
                                         Chain-of-thought exposes intermediate computa-                     chronological backjumping with semantic no-
                                         tion (Wei et al., 2022). Test-time methods im-                     good memoization.
                                         prove reasoning by sampling traces (Wang et al.,
                                         2023), decomposing problems (Zhou et al., 2023),                 • We prove conditional safety, completeness,
                                         or searching over thoughts (Yao et al., 2023; Besta                and termination under explicit assumptions
                                         et al., 2024). Yet after failure, systems usually                  on verifier and conflict-core soundness.
                                         restart, edit the latest step, or reflect and retry
                                         (Madaan et al., 2023; Shinn et al., 2023). If the                • We provide a deterministic controlled testbed
                                         error was introduced earlier, such local repair revis-             that isolates search under matched proposals
                                         its irrelevant decisions.                                          and measures verifier calls, backtracks, and
                                            Classical solvers instead use conflict-directed                 core reuse.
                                         search: identify the responsible decisions, jump
                                         over unrelated ones, and cache the conflict                      • We evaluate an LLM instantiation across five
                                         (Dechter, 1990; Prosser, 1993; Marques-Silva and                   reasoning tasks and two backbones, compar-
                                         Sakallah, 1999). Transferring this principle to                    ing task success and inference cost with four
                                         language models is nontrivial: natural-language                    baselines.

                                                                                                   1
                       Problem + state                         LLM proposer                                        External verifier                   ¥
               A       x and retained prefix s        Æ      (1)        (2)              (3)
                                                                                                          è        solver · tests · tools              q
                                                           d           d             d




            Decision trajectory                                                                                   ¥ pass → append


                       d1                        d2             d3                               d4                   d5                          d6

             q fail                 C = {d2 , d5 }    d3 , d4 , d6 : unrelated




                      õ cache C / prune                                                         backjump to d5                             d′5


Figure 1: Illustration of C ORE. A proposer extends a decision trajectory and an external verifier checks it. The
highlighted decisions d2 and d5 form a conflict core, while gray decisions are irrelevant to this failure. The controller
learns the core, backjumps to d5 , and rejects future candidates that contain both conflicting decisions.


2   Related Work                                                                         ing for multi-constraint planning (Stechly et al.,
                                                                                         2025). C ORE contributes a different search rule:
Reasoning by sampling and search. Self-                                                  conflicts name responsible decisions, enabling non-
consistency aggregates independent traces (Wang                                          chronological backjumping and persistent pruning.
et al., 2023), while Tree of Thoughts, Graph of                                          Its lineage is conflict-directed backjumping and
Thoughts, RAP, and LATS organize branching                                               constraint learning (Dechter, 1990; Marques-Silva
search (Yao et al., 2023; Besta et al., 2024; Hao                                        and Sakallah, 1999), reformulated for a proposer
et al., 2023; Zhou et al., 2024). MLR separates plan                                     whose actions are generated in language.
descriptors from step execution (Xiong et al., 2026).
These methods structure generation, choose states                                        3       Problem Formulation
to expand, or aggregate plans and answers; C ORE
                                                                                     Let a problem instance be x. A reasoning state st =
instead determines where to return after a verified
                                                                                     (d1 , . . . , dt ) is an ordered sequence of decisions. A
failure and which combinations to forbid thereafter.
                                                                                     decision is a record
The methods are complementary: a best-first or
tree-of-thought frontier can use C ORE’s learned                                                       di = (id i , type i , value i , deps i ),
constraints.
                                                                                         where the identifier is stable within a run and depen-
Verification and refinement. Process supervi-                                            dencies refer to prior decisions. Examples include
sion scores intermediate steps (Uesato et al., 2022;                                     assigning a value to a variable, selecting a planning
Lightman et al., 2024), and ProcessBench evalu-                                          action, asserting a lemma, or choosing an API ar-
ates error localization (Zheng et al., 2025). Self-                                      gument. The proposer Proposeθ (x, st ) returns an
Refine, Reflexion, and CRITIC use feedback for re-                                       ordered finite list of candidates. It may be an LLM,
vision (Madaan et al., 2023; Shinn et al., 2023; Gou                                     a policy model, or a deterministic heuristic.
et al., 2024). Reasoning traces may be unfaithful                                           Let κ(d) be a canonical decision–value key that
(Turpin et al., 2023; Lanham et al., 2023), so C ORE                                     preserves the decision’s type, dependency context,
does not assume that prose explanations reveal the                                       and resource or occurrence identity when repeated
model’s internal computation. It requires only that                                      choices must remain distinct. The active keys of a
accepted structured decisions and returned cores                                         state are
satisfy an external contract.                                                                           K(st ) = {κ(di ) : 1 ≤ i ≤ t}.
Solver–LLM collaboration. LLM-Modulo sys-                                                This representation lets the controller compare deci-
tems separate candidate generation from reliable                                         sions across trajectories while keeping choices with
checking (Kambhampati et al., 2024). SWAP rep-                                           different dependencies distinct. Figures abbreviate
resents dependencies with entailment graphs and                                          κ(di ) as di .
verifies intermediate steps (Xiong et al., 2025),                                           The search-time verifier has three outputs:
while PAL executes model-generated programs                                                                        (
(Gao et al., 2023). Recent work also combines                                                                        pass,
                                                                                             Verify(x, st ⊕ d) =
an LLM with a solver and chronological backtrack-                                                                    fail(C), unknown,

                                                                                 2
where C is a set of canonical decision–value keys           Algorithm 1 C ORE search
drawn from the proposed state. fail(C) is reserved          Require: instance x, proposer Propose, verifier
for a certified sound core; heuristic feedback can-             Verify, final scorer FinalCheck
not enter the hard cache. Unknown means that                 1: s ← [ ]; N ← ∅
the checker cannot establish either a valid step or a        2: while budget remains do
sound conflict; search may retain the decision pro-          3:     if s is complete then
visionally, but it cannot learn a hard core from that        4:          if FinalCheck(x, s) = 1 then
outcome. A separate FinalCheck(x, s) ∈ {0, 1}                5:              return s
scores a complete state against the task’s final cri-        6:          end if
terion.                                                      7:          s ←R EJECT L EAF(s); continue
Definition 1 (Sound conflict core). Let S ⋆ (x) be           8:     end if
the valid complete states for x. A set C is a sound          9:     A ← Propose(x, s)
conflict core for x exactly when                            10:     d ← first untried a ∈ A such that
                                                                ¬Contains(s ⊕ a, N )
         ∀s⋆ ∈ S ⋆ (x),        C ⊈ K(s⋆ ).                  11:     if no such d exists then
                                                            12:          C ← E XPLAIN E XHAUSTION(s)
   The definition is stronger than “these steps look        13:          if C is certified then
suspicious.” It makes a core a semantic nogood. A           14:              (s, N ) ← L EARNA ND J UMP(s, C,
direct constraint violation may yield a two-decision            N)
core; a failed unit test may yield the decisions in         15:          else
its dynamic slice; a symbolic solver may return an          16:              s ←BACKTRACK(s)
unsatisfiable core. A learned verifier can approxi-         17:          end if
mate this interface, but its cores are not covered by       18:          continue
exact guarantees.                                           19:     end if
   The objective is to find a complete state accepted       20:     r ← Verify(x, s ⊕ d)
by FinalCheck within a budget of proposer and               21:     if r = pass or r = unknown then
verifier calls. We count verifier calls because they        22:          s←s⊕d
can involve tool execution, a second model, or a            23:     else
solver and frequently dominate orchestration cost.          24:          (s, N ) ← L EARNA ND J UMP(s ⊕ d,
4     C ORE                                                     r.C, N )
                                                            25:     end if
4.1    Algorithm                                            26: end while
C ORE maintains a stack of active decisions and a           27: return B UDGET E XCEEDED
set N of learned cores. Before verifying a candi-
date, it checks whether the resulting state contains
a learned core. Such a candidate is skipped without         marked tried. Decisions newer than j are skipped:
another verifier call. A new failure core is mini-          they cannot resolve a conflict that does not mention
mized when possible, stored, and used to choose a           them. If all candidates at a level are exhausted,
backjump target. An unknown result can extend               their individual explanations are resolved into an
the stack, but only the final scorer can accept a           exhaustion core, analogous to eliminating the cur-
complete state.                                             rent variable in constraint search (Robinson, 1965;
   L EARNA ND J UMP first removes redundant mem-            Dechter, 1990). Figure 2 contrasts this operation
bers if the verifier supports core minimization. It         with chronological repair: the conflict excludes an
inserts the remaining core into N , deleting stored         intermediate decision, so C ORE skips that level and
supersets. For a nonempty core C in st , the back-          records a reusable nogood.
jump level and retained state are
                                                            Candidate and core bookkeeping. The con-
       j(C, st ) = max{i ≤ t : κ(di ) ∈ C},                 troller keeps a tried-candidate ledger for each re-
              s′ = sj(C,st )−1 .                            tained prefix. A candidate key includes its decision
                                                            type, canonical value, dependencies, and any iden-
The state is thus truncated to the level immediately        tity needed to distinguish repeated choices; chang-
before j = j(C, st ), and the offending value at j is       ing a dependency changes the key even if the sur-

                                                        3
              (a) Chronological repair                                   (b) C ORE: learn and backjump

               d1          d2            d3          d4         p         d1           d2      d3                  d4     p
                                                            1                                       skip d3 , d4


                                               2
                                                                                 direct jump
                                                                                                 Û       C = {d1 , d2 }

                                 3



                                                                           ; prune supersets           õ     cache C
                           º    è è è     repeated checks




Figure 2: The same failure under matched decision order. Chronological repair retreats through d4 and d3 before
reconsidering d2 . C ORE uses C = {d1 , d2 } to jump directly to d2 and caches the conflict to prune its supersets.
Gray decisions are absent from the core.


face text is identical. Within an instance, the cache                   verifier rejects the terminal value 14 and uses exact
test is                                                                 rational-arithmetic replay to explain the failure. Ex-
                                                                      haustive completion from {4new , 4orig , 6} cannot
  Contains(s, N ) = 1 ∃C ∈ N : C ⊆ K(s) .                               yield 24, so the checker certifies fail(C = {d1 }):
                                                                        retaining d1 makes every completion invalid, re-
A cached core therefore rejects later supersets re-                     gardless of d2 and d3 . C ORE caches this core
gardless of the order of decisions outside C, with-                     and jumps from d3 to d1 , skipping d2 . A new
out treating an unverified critique as a constraint.                    first choice can then produce d′1 : 3/4 = 3/4,
Certifying a jump. Before learning C, the                               d′2 : 1 − 3/4 = 1/4, and d′3 : 6/(1/4) = 24. This
checker must establish that no valid completion                         illustrates how a certified prefix conflict identifies
contains all of C. Reproducing a failure on one                         an earlier decision to change, while the skipped
complete trajectory is insufficient: another con-                       decision is irrelevant to that failure.
tinuation might succeed. If core minimization is                        4.2    Prompt and verifier contract
available, each removed member is accepted only
after the smaller core is certified again; otherwise                    An LLM instantiation should ask for one decision
the last certified core is kept. An exhaustion core                     at a time in a machine-readable schema, not an un-
also requires coverage of every legal alternative at                    restricted replacement trace. A minimal response
that decision level. If the complete alternative set                    contains id, value, and depends_on; optional
is Aj , and each a ∈ Aj has a certified core Ca                         prose remains non-binding. The controller, rather
containing κ(a), a candidate exhaustion core is                         than the model, owns the stack, candidate ledger,
                                                                        and learned cores. On backjump, the prompt con-
                        [
                                                                        tains the retained prefix and only the cores relevant
                                           
            Cexh =              Ca \ {κ(a)} .
                      a∈Aj                                              to the next decision. This avoids an ever-growing
                                                                        transcript.
Any completion retaining Cexh must choose an                               R EJECT L EAF marks a complete state rejected
a ∈ Aj and therefore contain Ca . Running out of                        by the final scorer as tried and retreats chronologi-
sampled candidates in one proposal batch does not                       cally; it does not cache a conflict without a sound
establish exhaustion, so the controller falls back                      explanation. Likewise, exhaustion uses chronologi-
to chronological repair when the checker cannot                         cal backtracking when no certified exhaustion core
certify it. Under finite token or verifier-call budgets,                is available.
the loop may instead return B UDGET E XCEEDED;                             Conflict production has three practical tiers:
the completeness result below applies only when
the budget does not interrupt the search.                                 1. Exact: SAT/SMT/CSP solvers, parsers, type
                                                                             checkers, and deterministic task constraints
Worked 24-Game example. Consider the cards                                   can return certified cores.
{1, 3, 4, 6}. The proposer first chooses d1 : 1+3 =
4, leaving the new 4, the original 4, and 6. It then                      2. Replay-certified: a proposed core is accepted
chooses d2 : 4orig + 6 = 10 and d3 : 4new + 10 =                             only if a sound checker rules out every com-
14. Before accepting d3 , an illustrative search-time                        pletion containing that subset.

                                                                    4
  3. Heuristic: an LLM or learned process model                                                         Chronological
                                                                                            250         CORE-BJ
     names likely causes. These may guide search




                                                                    Median verifier calls
                                                                                                        CORE
                                                                                            200
     but should be soft constraints with expiration
     or confirmation, because hard pruning can de-                                          150

     stroy completeness.                                                                    100


                                                                                             50
4.3   Guarantees
                                                                                              0
Theorem 1 (Safety and completeness). Assume                                                        18             24          30          36
                                                                                                           Number of decision variables
(i) every learned core is sound, (ii) branching and
maximum reasoning depth are finite, (iii) the pro-            Figure 3: Median verifier calls over 500 paired instances
poser eventually enumerates every legal candidate             per size. All methods use the same proposal order and
at a revisited state, (iv) the search-time verifier           exact verifier.
never rejects a prefix of a valid solution, (v) the fi-
nal scorer accepts exactly the valid complete states,                          n                  Chron.     CORE-BJ       C ORE           ∆
and (vi) the run is not stopped by a finite budget                   18                             32.0            31.0     31.0      −3.1%
before search completes. Then C ORE never prunes                     24                             95.0            70.0     69.0     −27.4%
a valid complete solution and returns a solution                     30                            223.5           147.0    134.5     −39.8%
                                                                     36                            267.0           189.0    173.5     −35.0%
whenever one exists.
Proof. A partial branch is pruned by a learned core           Table 1: Median verifier calls. ∆ compares C ORE with
                                                              chronological repair. Every method solved every main-
only when it contains that core. By core soundness,
                                                              test instance within budget.
no valid solution contains the core. A complete
state rejected by the final scorer is also invalid un-
der the stated assumption. A backjump removes                 through a different ordering of irrelevant decisions.
only decisions newer than the latest member of                This is a structural benefit, not a claim that every
the conflict; changing any removed decision while             instance improves: uninformative cores contain-
retaining the whole core cannot produce a solu-               ing the full prefix reduce C ORE to chronological
tion. Thus backjumping skips only invalid subtrees.           backtracking plus bookkeeping.
Finite branching and eventual enumeration imply
that every unpruned candidate is eventually tried.            5     Search Mechanism Analysis
If a solution exists, none of its prefixes contains
                                                              We use a controlled graph-coloring testbed to iso-
a sound core, so its branch is eventually reached
                                                              late the effect of the search controller. The evalua-
and accepted by the final scorer. Unknown partial
                                                              tion on language-model reasoning tasks follows in
checks and chronological retreat without a certified
                                                              Section 6.
core cannot remove it.
Proposition 1 (Termination). Under the assump-                5.1       Testbed
tions of Theorem 1, C ORE terminates with a solu-             We use planted 3-coloring because it exposes all
tion or exhaustion.                                           relevant algorithmic objects without an ambiguous
                                                              learned judge. For each size n ∈ {18, 24, 30, 36},
Proof. There are finitely many decision sequences.
                                                              we generate 500 graphs. Each vertex receives a
Candidate ledgers prevent retrying the same deci-
                                                              planted color; edges are sampled with probabil-
sion at the same retained state, and learning can
                                                              ity 0.28 only between differently colored vertices,
only remove additional sequences. Therefore the
                                                              guaranteeing at least one solution. Variables are or-
loop cannot visit infinitely many distinct untried
                                                              dered by decreasing degree. A deterministic noisy
candidates.
                                                              proposer ranks the planted color first with probabil-
Why cores can save exponential work. Suppose                  ity 0.30 and otherwise uses a seeded random order.
a conflict depends on decisions at levels i < j but           All methods receive exactly the same candidate
is discovered at depth t. Chronological repair may            ordering.
enumerate combinations of levels j + 1, . . . , t be-            The verifier accepts a color when it differs from
fore changing j. A core that excludes those levels            every assigned neighbor. Upon failure it returns the
skips their Cartesian product immediately. Memo-              conflicting vertex assignments. When every color
ization also prunes the same conflict when reached            for a vertex fails, the search procedure resolves

                                                          5
                        GSM8K    MATH-500    24-Game    Blocks      HumanEval
  Method                 (500)     (500)       (200)    (200)         (164)      Mean   Verifier calls   Tokens (k)
  Qwen2.5-7B-Instruct
  Direct CoT              72.4        42.8       61.0       41.0          58.5   55.1             1.0          1.3
  Self-Consistency-8      80.6        51.2       78.0       48.0          64.0   64.4             8.0          9.6
  Self-Refine-4           78.1        49.6       75.0       55.0          67.7   65.1             3.2          4.9
  Tree of Thoughts        82.0        55.4       88.0       67.0          70.1   72.5            18.6         14.2
  C ORE                   83.8        58.6       92.0       73.0          72.0   75.9            10.9          9.1
  Qwen3-8B
  Direct CoT              87.8        73.8       64.5       50.5          68.3   69.0             1.0           1.5
  Self-Consistency-8      92.2        79.8       79.5       54.5          72.0   75.6             8.0           6.5
  Self-Refine-4           89.8        78.2       76.5       59.5          72.0   75.2             3.0           4.8
  Tree of Thoughts        93.2        82.8       88.5       69.5          75.0   81.8            19.0           7.0
  C ORE                   93.8        85.2       91.5       74.5          76.2   84.2            12.0           6.0

Table 2: End-to-end task success rates (%) for both backbones. Calls and generated tokens are per-problem means.
Mean success averages the five task columns; sample counts are shown in the headers.


those explanations into the set of prior assignments        Sensitivity to proposal quality. At n = 30,
that block its domain. These are exact conflict             we rerun 200 paired instances with planted-first
cores.                                                      probabilities 0.10 and 0.60. With the weaker pro-
                                                            poser, median calls are 236.0 for chronological
Systems. C HRONOLOGICAL is depth-first repair               repair, 149.5 for backjumping, and 135.0 for C ORE.
that returns one level after an exhausted decision.         With the stronger proposer, they are 133.5, 92.0,
CORE-BJ uses conflict-directed backjumping but              and 90.5. Conflict-directed search helps in both
does not cache cores. C ORE adds core memoiza-              regimes, while the incremental value of memory
tion. The primary metric is the number of veri-             shrinks when a good proposal reaches a solution
fier calls until the first solution; we also record         before conflicts recur.
expansions, backtracks, jump distance, and learned
cores. Runs are capped at 100,000 calls. All ran-           6     Experiments
dom choices are derived from recorded instance
seeds.                                                      6.1    Experimental setup
                                                            Backbone and decoding. We report results with
5.2   Results                                               Qwen2.5-7B-Instruct and Qwen3-8B as proposers,
Backjumping reduces verification. All three                 both served with vLLM using bfloat16 weights and
methods solve all 2,000 main instances. Figure 3            the same decoding configuration. Candidate deci-
and Table 1 show that the methods are similar on            sions are sampled at temperature 0.7 and top_p =
the smallest graphs, where most runs encounter              0.95, with at most 128 generated tokens per candi-
little backtracking. The gap grows with deeper              date. The controller requests four candidates per
search. At 30 variables, C ORE reduces the me-              decision and permits at most 24 accepted decisions.
dian from 223.5 to 134.5 calls (39.8%); at 36 vari-         Per-problem budgets are 16,384 generated tokens
ables, it reduces 267.0 to 173.5 (35.0%). Mean              and 32 verifier calls.
calls at n = 36 fall from 546.0 to 235.4, indicating
that conflict information is especially useful on the       State and cache representation. The proposer
heavy tail.                                                 emits JSON records with id, decision_type,
                                                            value, and depends_on. The controller canonical-
Memory adds value beyond jumping. CORE-                     izes numbers, variable names, API arguments, and
BJ already improves substantially over chronolog-           commutative expressions before hashing a decision
ical repair. Memoization lowers median calls fur-           together with its type and dependencies. Learned
ther at n = 24, 30, 36 by 5.7%, 8.5%, and 8.2%,             cores are stored as sorted sets of canonical decision–
respectively. At n = 18, little search repeats and          value hashes. Subset lookup uses an inverted index
the two variants tie. This pattern is consistent with       from hashes to core identifiers. Core minimiza-
the intended mechanism: learned cores matter only           tion performs deletion-based replay for at most
after search begins to revisit a failed combination         eight additional checker calls; if the cap is reached,
under irrelevant surrounding decisions.                     the non-minimal sound core is retained. Heuristic

                                                        6
                                                                        CORE                                                78
                                     85
                                                                                 ToT

                                     80                                                                                            75.9


             Mean task success (%)




                                                                                                    Mean task success (%)
                                                                                                                            76
                                                  Self-Refine                                                                                                      74.9
                                     75
                                                                SC-8
                                                                                                                            74             73.8
                                     70                                                                                                            72.9
                                              Direct CoT
                                                                                                                            72                            71.8
                                     65


                                     60
                                                                                                                            70
                                                                                  Qwen2.5-7B
                                     55
                                                                                  Qwen3-8B
                                                                                                                            68
                                          0          5            10       15          20                                          CORE     No      No     Full     Soft
                                                           Mean verifier calls                                                            memory   jump   prefix   cores



Figure 4: End-to-end results. Left: mean task success against mean verifier calls for both backbones. Right:
Qwen2.5-7B-Instruct ablations of core memory, backjumping, and conflict precision.


 Variant                                        Success         Calls   Core size      Jump        viewed manually. 24-Game: Exact rational arith-
 C ORE                                              75.9        10.9             2.7     3.8       metic checks operands, operators, results, and card-
 No core memory                                     73.8        12.7             2.7     3.6       use counts during search. Final scoring requires
 No backjumping                                     72.9        15.4             2.8     1.0
 Full-prefix conflicts                              71.8        16.1             8.9     1.2       each of the four cards exactly once and a value of
 Soft heuristic cores                               74.9        14.3             3.4     2.9       24. Blocksworld: A deterministic state-transition
                                                                                                   checker verifies action preconditions and successor
Table 3: Qwen2.5-7B-Instruct ablations. Success is
                                                                                                   states. Final scoring executes the full plan from
mean task accuracy (%); other columns are per-problem
means. “Jump” is the number of decision levels re-                                                 the initial state and tests the goal. HumanEval:
moved per repair.                                                                                  Search checks syntax and runs a fixed set of public
                                                                                                   tests. Test failures on unfinished programs return
                                                                                                   unknown. Only the final program is run against
cores are never inserted into the hard cache.                                                      held-out evaluation tests, with generated code exe-
Tasks and sampling. For GSM8K (Cobbe et al.,                                                       cuted in an isolated environment.
2021), we sample 500 problems from the offi-
                                                                                                   Baselines and budget matching. Direct CoT re-
cial test split with fixed seed 1729 and retain the
                                                                                                   ceives one 16,384-token attempt. Self-Consistency
selected problem IDs. We use all 500 MATH-
                                                                                                   samples eight complete traces and votes over nor-
500 problems (Lightman et al., 2024). For 24-
                                                                                                   malized answers. Self-Refine performs up to four
Game, we select 200 fixed puzzles from the Tree
                                                                                                   critique–revision rounds. Tree of Thoughts uses
of Thoughts collection (Yao et al., 2023), con-
                                                                                                   branching factor four, beam width five, and the
firm solvability with an exhaustive solver, and
                                                                                                   same verifier-call cap as C ORE. Within each back-
retain each puzzle’s four cards and ID. We se-
                                                                                                   bone, all methods use the same proposer, prompt
lect 200 Blocksworld instances from PlanBench
                                                                                                   examples, answer parser, and final verifier. We re-
(Valmeekam et al., 2023), stratified by plan length.
                                                                                                   port realized token and verifier-call usage alongside
We use all 164 HumanEval problems (Chen et al.,
                                                                                                   task success because the methods consume these
2021).
                                                                                                   resources differently.
Search-time checks and final scoring. GSM8K:
Search checks arithmetic in structured equations                                                   6.2                           Results and analysis
and consistency with declared dependencies. Tex-                                                   Main comparison. In Table 2, C ORE has the
tual inferences that cannot be checked mechani-                                                    highest success rate on all five tasks with both
cally return unknown. Final scoring extracts the                                                   backbones. With Qwen2.5-7B-Instruct, mean
numeric answer and compares it with the dataset                                                    success is 75.9%, versus 72.5% for Tree of
answer. MATH-500: Search checks explicit alge-                                                     Thoughts. With Qwen3-8B, it is 84.2%, versus
braic transformations and substitution equalities;                                                 81.8%. Blocksworld gives the largest gain over
parsing failures return unknown. Final answers                                                     Tree of Thoughts for both backbones (+6.0 and
are compared using a fixed version of Math-Verify                                                  +5.0 points, respectively), where failed precondi-
(Hugging Face, 2025), with disputed parses re-                                                     tions identify earlier causal decisions.

                                                                                               7
Efficiency. Figure 4 shows the success–call trade-          References
off for both backbones. Compared with Tree of
                                                            Maciej Besta, Nils Blach, Ales Kubicek, Robert Ger-
Thoughts, C ORE uses 10.9 versus 18.6 calls and              stenberger, Michal Podstawski, Lukas Gianinazzi,
9.1k versus 14.2k generated tokens with Qwen2.5-             Joanna Gajda, Tomasz Lehmann, Hubert Niewiadom-
7B-Instruct. With Qwen3-8B, the corresponding                ski, Piotr Nyczyk, and Torsten Hoefler. 2024. Graph
counts are 12.0 versus 19.0 calls and 6.0k versus            of thoughts: Solving elaborate problems with large
                                                             language models. In Proceedings of the AAAI Con-
7.0k tokens. Verifier calls alone do not measure             ference on Artificial Intelligence, volume 38, pages
wall-clock cost: structured generation and core re-          17682–17690.
play add work beyond a baseline answer check.
                                                            Mark Chen, Jerry Tworek, Heewoo Jun, et al. 2021.
                                                             Evaluating large language models trained on code.
Ablations. The Qwen2.5-7B-Instruct ablations                 arXiv preprint arXiv:2107.03374.
in Table 3 show that removing core memory lowers
mean task success from 75.9% to 73.8% and raises            Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,
                                                              Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias
mean verifier calls from 10.9 to 12.7. Removing               Plappert, Jerry Tworek, Jacob Hilton, Reiichiro
backjumping lowers success to 72.9% and raises                Nakano, Christopher Hesse, and John Schulman.
calls to 15.4. Full-prefix conflicts yield the lowest         2021. Training verifiers to solve math word prob-
success of the listed variants at 71.8%. Soft heuris-         lems. arXiv preprint arXiv:2110.14168.
tic cores reach 74.9%, but uncertified cores do not
                                                            Rina Dechter. 1990. Enhancement schemes for con-
provide the guarantee of hard, reusable nogoods.              straint processing: Backjumping, learning, and cutset
                                                              decomposition. Artificial Intelligence, 41(3):273–
                                                              312.
Task-level failure modes. In GSM8K, a mis-
used quantity propagates through later arithmetic.          Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon,
In MATH-500, a sign, algebra, or substitution er-             Pengfei Liu, Yiming Yang, Jamie Callan, and Gra-
ror can implicate an earlier equation. In 24-Game,            ham Neubig. 2023. PAL: Program-aided language
an early operation can leave no solution, and card            models. In Proceedings of the 40th International
                                                              Conference on Machine Learning, volume 202, pages
reuse violates the rules. In Blocksworld, an early            10764–10799. PMLR.
move can occupy a block or location needed later,
with unrelated actions in between. In HumanEval,            Zhibin Gou, Zhihong Shao, Yeyun Gong, Yelong Shen,
an interface choice can conflict with a later func-           Yujiu Yang, Nan Duan, and Weizhu Chen. 2024.
                                                              CRITIC: Large language models can self-correct
tion assumption. These cases motivate revising the            with tool-interactive critiquing. In International Con-
causal decision instead of only the latest step.              ference on Learning Representations.

                                                            Shibo Hao, Yi Gu, Haodi Ma, Joshua Hong, Zhen
7   Conclusion                                                Wang, Daisy Wang, and Zhiting Hu. 2023. Rea-
                                                              soning with language model is planning with world
C ORE treats a failed reasoning trajectory as more            model. In Proceedings of the 2023 Conference on
                                                              Empirical Methods in Natural Language Processing,
than a negative score. A small, valid explanation             pages 8154–8173. Association for Computational
of failure is reusable search information: it says            Linguistics.
which decision must change, which later decisions
are irrelevant, and which combination should never          Hugging Face. 2025. Math-Verify: Mathematical an-
                                                              swer parsing and equivalence checking. https:
be tried again. The resulting algorithm imports
                                                              //github.com/huggingface/Math-Verify.
conflict-directed backjumping and learning into a
model-agnostic reasoning interface, with guaran-            Subbarao Kambhampati, Karthik Valmeekam, Lin
tees that are explicit about verifier soundness. Con-         Guan, Kino Stechly, Mudit Verma, Siddhant Bham-
trolled experiments show reduced verification work            bri, and Lucas Saldyt. 2024. LLMs can’t plan,
                                                              but can help planning in LLM-modulo frameworks.
under matched proposals, and the five-task evalu-             arXiv preprint arXiv:2402.01817.
ation with both Qwen2.5-7B-Instruct and Qwen3-
8B reports higher task success and lower verifier-          Tamera Lanham, Anna Chen, Ansh Radhakrishnan,
call use than Tree of Thoughts. Measuring latency             Benoit Steiner, Carson Denison, Danny Hernan-
                                                              dez, Dustin Li, Esin Durmus, Evan Hubinger, Jack-
and auditing core soundness are the next steps for            son Kernion, et al. 2023. Measuring faithful-
assessing these gains.                                        ness in chain-of-thought reasoning. arXiv preprint
                                                              arXiv:2307.13702.


                                                        8
Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri-         Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
  son Edwards, Bowen Baker, Teddy Lee, Jan Leike,               Bosma, Fei Xia, Ed Chi, Quoc V. Le, and Denny
  John Schulman, Ilya Sutskever, and Karl Cobbe.                Zhou. 2022. Chain-of-thought prompting elicits rea-
  2024. Let’s verify step by step. In International             soning in large language models. In Advances in
  Conference on Learning Representations.                       Neural Information Processing Systems, volume 35,
                                                                pages 24824–24837.
Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler
 Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon,              Siheng Xiong, Ali Payani, and Faramarz Fekri. 2026.
 Nouha Dziri, Shrimai Prabhumoye, Yiming Yang,                 Enhancing language model reasoning with structured
 et al. 2023. Self-refine: Iterative refinement with           multi-level modeling. In International Conference
 self-feedback. In Advances in Neural Information              on Learning Representations, volume 2026, pages
 Processing Systems, volume 36, pages 46534–46594.             36557–36610.
                                                             Siheng Xiong, Ali Payani, Yuan Yang, and Faramarz
João P. Marques-Silva and Karem A. Sakallah. 1999.             Fekri. 2025. Deliberate reasoning in language mod-
  GRASP: A search algorithm for propositional satisfi-         els as structure-aware planning with an accurate
  ability. IEEE Transactions on Computers, 48(5):506–          world model. In Proceedings of the 63rd Annual
  521.                                                         Meeting of the Association for Computational Lin-
                                                               guistics (Volume 1: Long Papers), pages 31900–
Patrick Prosser. 1993. Hybrid algorithms for the con-          31931.
  straint satisfaction problem. Computational Intelli-
  gence, 9(3):268–299.                                       Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran,
                                                               Thomas L. Griffiths, Yuan Cao, and Karthik
J. Alan Robinson. 1965. A machine-oriented logic               Narasimhan. 2023. Tree of thoughts: Deliberate
   based on the resolution principle. Journal of the           problem solving with large language models. In Ad-
   ACM, 12(1):23–41.                                           vances in Neural Information Processing Systems,
                                                               volume 36, pages 11809–11822.
Noah Shinn, Federico Cassano, Ashwin Gopinath,
  Karthik Narasimhan, and Shunyu Yao. 2023. Re-              Chujie Zheng, Zhenru Zhang, Beichen Zhang, Runji
  flexion: Language agents with verbal reinforcement           Lin, Keming Lu, Bowen Yu, Dayiheng Liu, Jin-
  learning. In Advances in Neural Information Pro-             gren Zhou, and Junyang Lin. 2025. ProcessBench:
  cessing Systems, volume 36, pages 8634–8652.                 Identifying process errors in mathematical reasoning.
                                                               In Proceedings of the 63rd Annual Meeting of the
Kino Stechly, Matthew Marquez, and Subbarao Kamb-              Association for Computational Linguistics (Volume
  hampati. 2025. An LLM-solver collaboration frame-            1: Long Papers), pages 1009–1024. Association for
  work for multi-constraint planning. In International         Computational Linguistics.
  Conference on Learning Representations.
                                                             Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman,
                                                               Haohan Wang, and Yu-Xiong Wang. 2024. Lan-
Miles Turpin, Julian Michael, Ethan Perez, and                 guage agent tree search unifies reasoning, acting, and
  Samuel R. Bowman. 2023. Language models don’t                planning in language models. In Proceedings of the
  always say what they think: Unfaithful explana-              41st International Conference on Machine Learning,
  tions in chain-of-thought prompting. In Advances in          volume 235, pages 62138–62160. PMLR.
  Neural Information Processing Systems, volume 36,
  pages 74952–74965.                                         Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei,
                                                               Nathan Scales, Xuezhi Wang, Dale Schuurmans,
Jonathan Uesato, Nate Kushman, Ramana Kumar, Fran-             Claire Cui, Olivier Bousquet, Quoc V. Le, and Ed H.
  cis Song, Noah Siegel, Lisa Wang, Antonia Creswell,          Chi. 2023. Least-to-most prompting enables complex
  Geoffrey Irving, and Irina Higgins. 2022. Solving            reasoning in large language models. In International
  math word problems with process- and outcome-                Conference on Learning Representations.
  based feedback. arXiv preprint arXiv:2211.14275.

Karthik Valmeekam, Matthew Marquez, Alberto Olmo,
  Sarath Sreedharan, and Subbarao Kambhampati.
  2023. PlanBench: An extensible benchmark for eval-
  uating large language models on planning and reason-
  ing about change. In Advances in Neural Information
  Processing Systems, volume 36, pages 38975–38987.

Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V.
  Le, Ed H. Chi, Sharan Narang, Aakanksha Chowd-
  hery, and Denny Zhou. 2023. Self-consistency im-
  proves chain of thought reasoning in language mod-
  els. In International Conference on Learning Repre-
  sentations.


                                                         9
