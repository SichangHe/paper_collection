                                               V IVA L A V IDA: Verification and Accumulation
                                                    Failures in Multi-Agent Proof Search


                                                                     Benji Xu      Ken Zheng         Noah Han
                                                                         University of California, Berkeley
                                                               {benji.xu, kenzhengjk, noah0427}@berkeley.edu
arXiv:2610.04829v1 [cs.CL] 4 Oct 2026




                                                                                           Abstract
                                                  When an agentic prover works on an open problem, there is no proof assistant
                                                  to fall back on: its verifier and lemma library are ultimately language models
                                                  judging model outputs. We instrumented such a system end to end and analyzed
                                                  51,754 traced observations across three full runs (186 hours, $5,694). We find
                                                  three connected failure modes. First, the three-model verifier requires unanimity
                                                  and treats parse or API failure as non-approval; in 10 of 12 verification events,
                                                  one member returned no parseable output or an API error, making acceptance
                                                  arithmetically impossible without surfacing an error. Second, when the ensemble
                                                  did function, one verifier approved 3 attempts that GPT rejected, each claiming to
                                                  resolve the open problem; a single-verifier design would therefore have announced
                                                  a solution three times. Third, because nothing could be approved, every review was
                                                  a refutation, yet the lemma extractor mines reviews as well as proofs: 24 of 93 lem-
                                                  mas (26%) were extracted from rejected arguments with their refutational context
                                                  removed. Taken together, these findings show that without external verification,
                                                  supervision is itself a critical trust boundary: systems must distinguish abstention
                                                  from rejection, preserve useful disagreement, and preserve the provenance and
                                                  polarity of information before it becomes future context. We release traces and
                                                  analysis scripts here.


                                        1    Introduction
                                        Memory-augmented provers are attractive in part because a failed run can still leave behind useful
                                        artifacts: a lemma, a reduction, or a ruled-out direction. On benchmark problems, the question of
                                        what to keep has a clean answer, since a proof assistant can check each candidate [Yang et al., 2023,
                                        Wang et al., 2025, Xin et al., 2025]. On an open problem, this is no longer the case. The relevant
                                        mathematics is largely unformalized [LeanDojo, 2026], informal proof is where current models
                                        perform best [Varambally et al., 2025], and no oracle can say whether a proposed lemma is actually
                                        true. Both verification and retention therefore become judgment calls made by other models.
                                        We built V IVA L A V IDA, an agentic prover targeting the exact optimal erasure resilience ratio α⋆ for
                                        binary interactive error-correcting codes (iECCs), where the known bounds leave a gap [Gupta et al.,
                                        2022]. Recursive prover agents write to a shared library behind three gates (Section 2). We ran the
                                        system three times, once per prover backbone, and traced every model call. This paper is not about
                                        α⋆ itself; rather, it is about what the gates did in practice and what ended up in the library as a result.
                                        The target problem. In an interactive error-correcting code, Alice holds a message x, and Bob
                                        must learn it by exchanging bits with her over a binary channel while an adversary erases part of
                                        the communication. The adversary’s budget is a fraction of the total communication, so bits sent
                                        in both directions count against it. The erasure resilience ratio α⋆ is the largest such fraction that
                                        some binary iECC can tolerate while Bob still recovers x. Interaction is what makes the question

                                        40th Conference on Neural Information Processing Systems (NeurIPS 2026). Workshop: The 6th Workshop on Mathematical
                                        Reasoning and AI.
                                                                                                                   proof attempts
                                                                                                                                GATE 3

                                     Library                             integrator add/merge/skip                       lemma extractor
                               Qdrant + JSON                                                                     take only self-contained proven claims


                                                                                                                                           the critique
                                                                                                                                           channel
 retrieval                                                                                                                    Reviews
                                                                                             GATE 1
                                                                                                                                                    GATE 2
                                                                                                              claims
      library                                                       Proof                Coordinator          proved    Verifier ensemble all approve
                                     Prover                                                                             GPT · Claude · Gemini         verified
     samples               stateful across iterations              Attempt             claims completion?
                                                                                                                         unanimity required           success


                        tool calls                                  direction
                                                                                  verifier critiques




                discuss 3 models               fork inherits ctx          spawn sub prover                  web · ask library

                                          recursive to depth dmax ; then non-recursive tools only



Figure 1: V IVA L A V IDA. The spine is one iteration: a stateful prover with recursive (fork,
spawn_sub_prover) and non-recursive tools emits a proof attempt; a coordinator triages whether
it claims completion; if so, a three-model ensemble must approve unanimously. Above the spine is
the intake path: proof attempts and reviews are both mined for lemmas by a conservative extractor,
curated, and embedded for retrieval by later provers. All three gates scrutinize the prover. The red
edge is the channel none of them was designed for.

Table 1: The three full runs. “Iters” counts coordinator judgements; “Verified” counts attempts
reaching the ensemble.

                Prover backbone                 Hours              Cost         Generations            Iters      Verified          fork          spawn
                GPT-5.4                           91.3         $3,517                 11,743             10                 0         404             689
                Gemini 3.1 Pro                    81.4         $1,947                  4,929             12                10         366              30
                Claude Opus 4.7                   13.9           $229                    881             15                 2          17              40
                Total                           186.6          $5,694                 17,553             37                12         787             759



interesting: Gupta et al. [2022] show that it lets binary codes survive the erasure of more than half of
all communication, constructing an iECC resilient to 3/5 and proving that no binary iECC is resilient
to 2/3. The exact value in between is open. V IVA L A V IDA is built to search for informal proofs of
open statements like this one, which is also why no proof assistant can check its output.

2      V IVA L A V IDA’s Tri-Gate Architecture
The T RIAGE gate (coordinator) decides only whether an attempt claims completion, not whether
it is correct. The V ERIFY gate (verifier ensemble) runs GPT-5.4, Claude Opus 4.7, and Gemini
3.1 Pro in parallel, and all three must approve. The gate is fail-closed: an API error, turn-limit
exhaustion, or unparseable response is recorded as a review with approved=false. The E XTRACT
gate (lemma extractor) is deliberately restrictive. It emits only (statement, proof) pairs that the source
both states and proves, never repairs, extends, or supplies a missing proof, and returning zero pairs is
acceptable. This extractor is applied to every proof attempt and every review. Survivors are passed to
an integrator that may skip, merge, or add them, and are then embedded for retrieval. See Figure 2
for a more structured presentation of the V IVA L A V IDA algorithm.

3      Result 1: The Ensemble Could Not Approve
Twelve attempts reached V ERIFY, producing 36 reviews in total, with zero unanimous approvals.
That number is misleading on its own, however, because in most cases approval was not actually
possible. In fact, ten of the 36 reviews were not mathematical judgments at all; all ten came from the
Claude verifier. Eight carry the reason string "Claude returned no parsed output.", meaning


                                                                                     2
    V IVA L A V IDA Algorithm.
    Input: Problem x, library L, max iterations T , max recursion depth dmax . Init: System
    prompt and uniform sample of k artifacts (proofs, reviews, lemmas) from L.
    For i = 1, . . . , T :
          1. Prover generates attempt Pi via conversation and tools (discuss, web,
             ask_library, fork, spawn_sub_prover if depth < dmax ). If empty, save, re-
             prompt, continue.
          2. T RIAGE. Coordinator emits Ji ∈ {claimed proved, incomplete} (with direction if
             incomplete). No correctness assessment.
          3. If incomplete: Save Pi , Ji ; inject Pi into L (Step 7); feed direction to prover;
             continue.
          4. V ERIFY.         Parallel verifiers m        ∈     {GPT, CLAUDE, GEMINI} return
             (approvedm , reasonsm ).      Errors, timeouts, or unparseable responses yield
             approvedm = FALSE (fail-closed).
                V
          5. If m approvedm : Save Pi as success and halt.
          6. Else: Save Pi and reviews Ri ; inject Pi and each r ∈ Ri into L (Step 7); feed
             reasonsm to prover.
          7. E XTRACT (Library intake for all injected a, proofs or reviews). Extract (statement,
             proof) pairs stated/proven by a; integrator skips, merges, or adds them; embed a and
             new lemmas for retrieval.
    Return: Final proof attempt.

Figure 2: V IVA L A V IDA pipeline run. Step 4 treats infrastructure failures as non-approvals, making
Step 5’s unanimity test fail if any verifier errors. Step 7 ingests both reviews and proof attempts,
letting the critique channel feed the library equally.


the model produced no parseable structured response, and two record an API error. The fail-closed
path stored all ten as non-approvals, identical to a rejection on the merits. Under the unanimity rule, a
single guaranteed non-approval vetoes the entire ensemble. So in 10 of 12 verification events (83%),
acceptance was arithmetically impossible before any mathematics was read. The pipeline’s only
success state was unreachable, and nothing surfaced this to the operator: runs completed normally,
and the outcome was indistinguishable from a correct unanimous rejection. An infrastructure failure
should not admit an unchecked proof, and unanimity is the conservative aggregation rule. However,
conservative-on-error composed with conservative-on-aggregation does not yield a safe verifier but
an inert one that always rejects. Separating abstention and rejection as distinct booleans and treating
an aggregate containing an abstention as an error that is surfaced in real-time could be an interesting
follow-up work here.
The same pattern beyond verification. V IVA L A V IDA caps prover recursion at depth 5, beyond
which sub-provers lose fork and spawn_sub_prover, and the traces record the depth at every level.
This bound held for the GPT backbone, but the Claude backbone reached depth 8 and the Gemini
backbone depth 108. Like the verifier, the guard was correct on the path we developed against and
silently absent on another, and nothing in the run output revealed it.


4    Result 2: Critic’s Model Diversity Was Load-Bearing

In three of the twelve events, the ensemble split: the Gemini verifier approved an attempt that the
GPT verifier rejected. All three approvals endorsed claims that α⋆ = 2/3, using unambiguous
language such as “mathematically rigorous, complete, and elegantly resolves the open problem” and
“successfully and rigorously establishes the exact optimal worst-case erasure resilience.” No verifier
other than Gemini approved anything in any event. A single-verifier system built on that model would
have announced a resolution of an open problem three times in twelve opportunities. We read this
as evidence that disagreement, rather than any single verifier, is what blocked these approvals. This
finding is distinct from the unanimity rule itself: what blocked them was disagreement, which any
aggregation rule stricter than “any-approve” would have caught.


                                                   3
Table 2: Lemma intake by channel across the three runs. Every review in the corpus is a critique of a
rejected attempt, so the entire review channel is refutation-derived.

         Channel               Source artifacts   Candidates extracted   Lemmas added   Share
         Proof attempts                     37                     98              69   74%
         Reviews (critiques)                36                     38              24   26%
         Total                              73                    136              93


5   Result 3: The Library Filled with Refutations
Because nothing could be approved, every attempt reaching V ERIFY was rejected, and so every
review in the corpus is a refutation. Since E XTRACT mines reviews as well as proofs, 24 of the 93
lemmas added during the runs (26% of everything accumulated) came from critiques of arguments
the ensemble had just rejected. We quote four of the results this channel contributed verbatim, each
stored as a lemma and retrievable by any later prover:
       • “Balancing p with 12 − 18 p gives p = 49 , not 58 .”
       • “From the equation p = 1/2 − p/6, it follows that p = 3/7, which gives a cost of C = 3/7.”
       • “For p ∈ (3/5, 4/5), the term p alone exceeds 3/5.”
       • “For p = 32 , one has 1 − p2 = 32 > 53 .”
Two of these are true but vacuous: i.e., correct, uninformative, consuming retrieval budget, and
lending the library a false appearance of substance. Two are worse, and the first is the clearest
example. It is explicitly a correction, where the verifier demonstrates that a proof’s arithmetic does
not give what it claimed, yet it is stored as a standalone result. A later prover retrieving it sees an
established fact about α⋆ and not a rebuttal of one.
One point of clarification is that the 26% is a provenance share, not an error rate: it counts where
lemmas came from, not whether they are wrong. Another point is that neither channel is gated by
verification. Since nothing was approved, all 69 proof-attempt lemmas also came from unverified
attempts, 25 of which never reached V ERIFY at all. What sets the critique channel apart is not missing
verification but lost polarity, as these examples show.
Why a conservative extractor admits this. The leak follows from the rule: retain only what the
source states and proves. This is reasonable for proofs, but fails on critiques, where short claims
depend on refutational context: “p = 3/7” may hold only under a premise introduced to disprove the
proof. The extractor preserves the claim but loses the contradiction. More fundamentally, it distrusts
the prover while implicitly trusting critics: T RIAGE and V ERIFY filter the prover, but E XTRACT
provides no analogous trust boundary for the critic.
Exposure. Provenance alone does not show that these lemmas reached a prover, but the traces do.
Of the 1,469 answers the ask_library agent returned to provers across the three runs, 174 (11.8%)
cited at least one refutation-derived lemma, and 21 of the 24 such lemmas surfaced at least once.
Nearly all of these answers (168 of 923) went to the GPT run, which never reached V ERIFY and so
produced no critiques of its own: every refutation-derived lemma it retrieved was mined from another
run’s reviews through the library the three runs shared. Exposure is still not harm (see Limitations).
We computed these counts from the full trace export rather than the released subset.

6   Discussion
A controlled check. The library snapshot contains 8 attempts produced while the prover prompt
carried a smoke-test override instructing it to invent an argument and claim success. These attempts
assert four mutually contradictory values for α⋆ . Against these, the extractor behaves as designed:
0.25 lemmas per fabricated attempt compared to 3.82 per genuine one in the same snapshot, a 15×
suppression. The proof channel resists bad input; the critique channel is the one no gate was designed
for, because it was never conceived as an input in the first place.
Design Implications. Here are some of our potentially interesting mitigation ideas. (i) Not extracting
from critiques. This is the cheapest option and removes the channel entirely, at the cost of whatever


                                                    4
genuine content critiques carry. (ii) Carry polarity into the store: retain review-derived statements
but tag their role (e.g. “established while refuting artifact X”) and surface the tag at retrieval time.
(iii) Propagate verdicts to descendants: when the ensemble rejects an attempt, mark lemmas from
that attempt and its reviews as provisional. V IVA L A V IDA already stores the parent–child links and
simply never consulted them at intake. (iv) Gate on utility as well as justification: a vacuity filter
would catch the true-but-vacuous half of the problem.


7    Related Work

Our verifier finding instantiates two modes of the MAST taxonomy of multi-agent failures, namely
“no or incomplete verification” and “incorrect verification” [Cemri et al., 2025]. Our crucial addition
is the mechanism: a fail-closed error path composed with unanimity. Zheng et al. [2023] established
LLM-as-a-judge while documenting its position, verbosity, and self-enhancement biases, and Huang
et al. [2024] showed that intrinsic self-correction fails on reasoning tasks without external feedback.
Both motivate a multi-model critic, and Result 2 is what judge error looks like when the judged
object is a claimed proof of an open problem and no human reference exists. Retaining critique as
memory is standard practice. Reflexion, for instance, keeps verbal reflections in an episodic buffer
that conditions later trials [Shinn et al., 2023]. However, in that setting reflections stay anchored to
an observable success signal, which an open problem does not supply. AgentPoison showed that an
adversary can backdoor an agent by poisoning its memory or RAG store [Chen et al., 2024]. Our
Result 3 is the same hazard with no adversary, produced by the system’s own verifier.


8    Limitations

We conducted three runs on one open problem, with one extractor, one embedding model, one
integrator, and one prompt each. No confidence interval is meaningful at 12 verification events. The
Claude failure is also not fully diagnosed: output token counts do not indicate budget exhaustion, so
we suspect structured-output parsing against a reasoning-heavy response; we’ve studied the effect but
not yet the cause. Our evidence also stops short in three places. The 26% and 11.8% figures measure
provenance and exposure, not harm; a memory ablation that withholds critique-derived lemmas and
compares downstream attempts would be needed to show damage. No expert adjudicated the three
contested approvals; and without a repeated single-model baseline, we cannot separate the value of a
second model from the value of a second sample, or from not letting a model grade its own work.
Lastly, we’ve seen no progress on α⋆ for the still open iECCs problem.


9    Conclusion

On an open problem, a prover’s verifier and library are both models judging models. Our experiments
show that, without an external proof checker, the supervision layer is a critical trust boundary:
its outputs must remain interpretable, disagreements informative, and judgments must not silently
change meaning in future context. This yields three lessons. First, abstention is not rejection: API,
parse, or infrastructure failures must remain distinguishable from substantive rejections, as collapsing
them masks supervision failures. Second, critic diversity is load-bearing: the approvals blocked
by disagreement suggest independent models provide important protection when external checkers
are absent. Third, verification and accumulation are separate trust boundaries: a critique can
be rigorous yet unsafe to store as a lemma once its refutational context is removed. Our 24/93
refutation-derived lemmas show conservative extractors amplify this when applied symmetrically.
More broadly, safeguards must cover every channel where model outputs become future context,
with telemetry making failures observable. In our system, traces revealed hidden failures: fail-closed
errors and unanimity prevented approval, a single verifier would have announced a solution three
times, and a quarter of the library came from refutations. Thus, when agents supervise agents, the
supervision layer must be a first-class component: its failure modes, disagreement structure, and
information-flow semantics require the same instrumentation applied to the agents it supervises.


                                                   5
References
Meghal Gupta, Yael Tauman Kalai, and Rachel Yun Zhang.          Interactive error cor-
 recting codes over binary erasure channels resilient to > 12 adversarial corruption.
 In Proceedings of the 54th Annual ACM SIGACT Symposium on Theory of Computing, pages
 609–622, 2022.

Haiming Wang et al. Kimina-Prover Preview: Towards large formal reasoning models with reinforce-
  ment learning. arXiv preprint arXiv:2504.11354, 2025.

Ran Xin, Chenguang Xi, Jie Yang, Feng Chen, Hang Wu, Xia Xiao, Yifan Sun, Shen Zheng, and
  Kai Shen. BFS-Prover: Scalable best-first tree search for LLM-based automatic theorem proving.
  arXiv preprint arXiv:2502.03438, 2025.

Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil,
  Ryan Prenger, and Anima Anandkumar. LeanDojo: Theorem proving with retrieval-augmented
  language models. arXiv preprint arXiv:2306.15626, 2023.

Sumanth Varambally, Thomas Voice, Yanchao Sun, Zhifeng Chen, Rose Yu, and Ke Ye. Hilbert:
  Recursively building formal proofs with informal reasoning. arXiv preprint arXiv:2509.22819,
  2025.

LeanDojo. Lean Millennium Prize Problem statements. GitHub repository, 2026.

Mert Cemri, Melissa Z. Pan, Shuyi Yang, Lakshya A. Agrawal, Bhavya Chopra, Rishabh Tiwari,
 Kurt Keutzer, Aditya Parameswaran, Dan Klein, Kannan Ramchandran, Matei Zaharia, Joseph E.
 Gonzalez, and Ion Stoica. Why do multi-agent LLM systems fail? arXiv preprint arXiv:2503.13657,
 2025.

Zhaorun Chen, Zhen Xiang, Chaowei Xiao, Dawn Song, and Bo Li.                      AgentPoi-
  son: Red-teaming LLM agents via poisoning memory or knowledge bases.                    In
  Advances in Neural Information Processing Systems 37 (NeurIPS), 2024. arXiv:2407.12784.

Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xiny-
   ing Song, and Denny Zhou. Large language models cannot self-correct reasoning yet. In
   International Conference on Learning Representations (ICLR), 2024. arXiv:2310.01798.

Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan,
  and Shunyu Yao. Reflexion: Language agents with verbal reinforcement learning. In
 Advances in Neural Information Processing Systems 36 (NeurIPS), 2023. arXiv:2303.11366.

Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao
  Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonza-
  lez, and Ion Stoica. Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. In
  Advances in Neural Information Processing Systems 36 (NeurIPS), 2023. arXiv:2306.05685.


A     Example Artifacts from a Full Run
This appendix follows one iteration of the Gemini 3.1 Pro run through the pipeline of Section 2,
captured from our Langfuse traces: a proof attempt, the ensemble’s response to it, and the library
intake that followed. The three are consecutive spans of the same trace, and together they show
Result 1 and Result 3 occurring within a single pass.

A.1   Proof Attempt from the Prover

Figure 3 shows the proof attempt. The span tree on the left captures the prover’s discuss tool
calls feeding into the final GenerateContent call; the output panel on the right shows the prover
declaring the problem resolved with α⋆ = 3/5 and asserting that the known 2/3 impossibility bound
is loose. Neither claim is correct. The coordinator triages the attempt as “claimed proved” and
dispatches it to the verifier ensemble.


                                                6
A.2   The Ensemble’s Response

Figure 4 shows the Gemini verifier’s review, which returns approved: false and identifies fatal
flaws in the 3-Way Intersection Attack used to claim the upper bound. That review is a genuine
mathematical judgement, and so is the GPT verifier’s. The third is not: in this same event the Claude
verifier returned an API Error, which the fail-closed path records as approved: false. All three
values are identical in the stored Review, so the ensemble’s aggregate is indistinguishable from a
unanimous rejection on the merits. This is Result 1 in a single iteration.

A.3   Library Intake After the Rejection

Figure 5 shows what the library ingested next. The lemma-integrator span is nested un-
der verifier-oai-injector: its source is the verifier’s critique, not the proof attempt. It
decides add/merge/skip per candidate and embeds the survivors into the vector store with
text-embedding-3-large. Across this window the proof-attempt channel contributed one lemma
and the three review channels contributed three. Material extracted from a refutation enters the library
on the same footing as material extracted from a proof, with nothing recording that it came from an
argument the ensemble had just rejected. This is Result 3 in a single iteration.




Figure 3: Proof attempt from the Gemini 3.1 Pro prover claiming α⋆ = 3/5. (The root span’s
displayed total ($1,258.61) is Langfuse’s own aggregate; summing the per-generation costs over the
same trace gives the $1,947 reported in Table 1.)




                                                   7
Figure 4: The Gemini verifier returning approved: false on the attempt in Figure 3. The Claude
verifier’s approved: false in the same event was an API Error, not a judgement.




                                              8
Figure 5: Library intake following the rejection. The lemma-integrator runs under
verifier-oai-injector, so the lemmas being embedded are extracted from the verifier’s cri-
tique instead of from the proof attempt.




                                            9
