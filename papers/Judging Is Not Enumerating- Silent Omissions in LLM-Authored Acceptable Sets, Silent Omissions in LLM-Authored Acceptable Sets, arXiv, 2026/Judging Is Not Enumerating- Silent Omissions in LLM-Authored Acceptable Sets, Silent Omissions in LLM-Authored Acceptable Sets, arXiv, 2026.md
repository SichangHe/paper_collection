                                                       Judging Is Not Enumerating:
                                            Silent Omissions in LLM-Authored Acceptable Sets
                                            Wenhui Chen∗1 , Jianlin Chen†2 , Ziyao Lin‡1 , Peiji Long§3 , and Chi Man Vong¶1
                                                                                1
                                                                                  University of Macau
                                                                     2
                                                                         South China University of Technology
                                                                              3
                                                                                Independent Researcher




                                                                                        Abstract
                                                Language models are increasingly promoted from examinees to examiners: they write the test
arXiv:2608.01000v1 [cs.AI] 2 Aug 2026




                                            suites, answer keys, rubrics, and reward functions that define correctness for other systems. We
                                            measure the capability that role assumes and find it lacking under the protocol the role is usually
                                            deployed with, one-shot greedy authoring with no test-time reasoning. That scope condition
                                            changes the remedy, so we state it first: where a compact rule exists, test-time reasoning closes
                                            the gap outright on our algorithmic construction (§3.7), a far cheaper fix than the probe gating
                                            we propose where it does not.
                                                We use four reference constructions: two with complete finite truth (mechanically de-
                                            cidable predicates over presented lists), one with a hardened executable reference (Hu-
                                            manEval+/MBPP+), and one with an explicitly incomplete lexical reference (WordNet).
                                            Across all four, models judge whether a candidate belongs far better than they author the set
                                            itself, enumerating it where it is finite and writing the suite that induces it where it is not. On
                                            the incompleteness-proof algorithmic construction the gap is +0.34 to +0.29 F1 across a 24×
                                            parameter range and does not close over it. On executable code, models judging correctness at
                                            F1 0.74–0.90 author suites admitting only 19–42% of oracle-correct solutions, over-rejecting by
                                            inventing requirements the specification never states.
                                                A control locates the deficit. Asked to emit the predicate rather than its extension, the
                                            same models reach F1 ≈ 0.99 with every generated predicate executable, above even their own
                                            judging. The failure is not missing knowledge or an inability to specify. It is an inability to
                                            materialise the region a specification induces, which is exactly what keys, rubrics, and suites
                                            demand.
                                                The dominant error is omission, and omission resists audit: an over-inclusion is a written
                                            token a reviewer can challenge, while a missing member is an absence whose discovery is the
                                            authoring problem itself. Models detect planted over-inclusions 6–7× more often than planted
                                            omissions, and a production deployment of 43,227 scored items fails omission-first at 10:1. Wired
                                            into RLVR, an authored key costs 1.9 points of accuracy where the acceptable set is mechanically
                                            exact and 18.5 points WordNet-relative on the lexical task, each in all six paired seeds (two-sided
                                            p=0.031).
                                                One mitigation works: discard any authored verifier that rejects a known-correct probe.
                                            False rejection falls from 58–92% to ≤5%, but only 5–39% of suites survive. Most of that loss is
                                            recoverable. Rewriting each wrong expected value to what a reference execution returns raises
                                        ∗
                                          mc35092@um.edu.mo
                                        †
                                          202330450231@mail.scut.edu.cn
                                        ‡
                                          mc35081@um.edu.mo
                                        §
                                          longpeiji@gmail.com
                                        ¶
                                          Corresponding author. cmvong@um.edu.mo


                                                                                            1
      yield 3.3–10.6× across four author families, by the largest factor for the weakest author, whose
      survivors go from 43% vacuous to none. What survives measures the split: the model chooses
      discriminating inputs well (94% of wrong solutions still caught once expectations are corrected)
      and computes their expected outputs badly.


1    Introduction
A quiet role reversal is underway in how language-model systems are built. Models no longer
merely produce answers that some fixed verifier grades; increasingly they write the verifier : unit
tests generated from a docstring, answer keys attached to authored assessment items, rubrics used
as reward signals [13], and machine-checkable acceptance criteria wired directly into reinforcement-
learning-with-verifiable-rewards (RLVR) pipelines. Once authored, such a specification becomes the
operational definition of “correct” for everything downstream: benchmark labels, agent feedback,
reward gradients. The literature has studied at length whether a given verifier can be gamed [14, 30],
how noisy verdicts propagate into RLVR [3], and how verifiers falsely reject correct behavior, as when
rule-based math checkers reject valid answer formats [16] or benchmark suites fail valid solutions [7].
All of it varies or audits the verifier while treating its origin as exogenous. This paper asks the prior
question, in the specific form our measurements can answer: can a language model materialise
the acceptable set that a correctness specification denotes? The question is not whether it
can state a specification; §3.11 shows it can, near-perfectly. Recent benchmarks report symptoms
of the answer being no: model-generated rubrics that lag human ones [47], generated test suites too
weak or misaligned to trust [9, 24]. We add more than another symptom. We establish the effect
under complete ground truth, where no incompleteness confound survives, identify its mechanism
as silent omission, and measure what it costs as an RLVR reward.
     The question has a clean formal core. A specification over a candidate space V is a membership
predicate with acceptable set S ∗ ⊆ V ; executing it means answering “is x ∈ S ∗ ?” for one given
x. Authoring it means producing an artifact that induces an acceptance region Ŝ ⊆ V , and it
comes in two forms. The extensional form emits the members themselves, so Ŝ is the emitted
list; it exists only where S ∗ is small and finite, and it is what our three word-list constructions
measure. The intensional form emits a predicate (for programs, a test suite), and Ŝ is whatever
that predicate accepts under execution; where V is unbounded, as for code, it is the only authoring
interface there is. In every arm we measure the same quantity: the fidelity of Ŝ to S ∗ , scored as a
classifier over the same candidates on which we score the model’s own execution, so “the gap” is one
statistic throughout. The two forms fail differently, and one further variable decides which failure
is reachable: whether S ∗ admits a compact intensional characterisation available to the author. On
the mechanical constructions it does: the defining rule is stated in the prompt, so restating it as an
executable predicate is near-free (F1 ≈ 0.99, §3.11), and the measured deficit isolates extensional
enumeration: emitting an unordered set under a causal mask, deciding element-by-element what to
emit and, critically, when to stop, without ever inspecting the candidates not sampled [37, 39, 61].
On code no such rule exists to restate: the specification is prose and examples. The forced intensional
interface therefore fails in its own mode, inventing requirements the specification never states; the
induced region ends up too small there too. The unified claim is therefore not “models cannot
write predicates”: it is that models execute membership far better than they author artifacts whose
induced region matches S ∗ , except where authoring collapses into restating a compact rule they
were already given. The generative-AI-paradox literature has established that models can generate
what they cannot discriminate [18, 34, 41]. The authoring problem is the harsher dual: here the
model must generate a discriminator, so every weakness of set-construction lands inside the artifact
that will later define correctness for other systems.

                                                     2
                      AUTHOR Ŝ ≈ S ∗
                       extensional : emit                            omission-dominated
                      the set (F1 .26–.48)                            6–7× harder to audit
                       intensional : emit                               (word-list arms)
                        a suite (.19–.44)           scissors
                                              authoring ≪ judging
                                                 (one-shot, no
                                                   reasoning)
                         JUDGE x∈S ∗                                      same-model          gate on a known-
 same weights
                     classify one candidate                            sample-then-verify       correct probe:
 & knowledge
                      (strong: F1 .60–.90)                              does not repair it     FRR → ≤5%




                          RESTATE                   escapes            as an RLVR key:
                          a given rule          predicate emis-         −1.9 pts (com-
                         emit a predi-         sion, or test-time         plete truth)
                        cate, execute it        reasoning where        −18.5 (WordNet-
                    (near-perfect: F1 ≈.99)       a rule exists             relative)

Figure 1: The paper in one view, and its boundaries. The same weights expose three interfaces to a
correctness specification (column 2). Judging membership is strong; authoring an artifact whose induced
region should equal S ∗ is much weaker in both of its realisations, extensional enumeration on the word-list
constructions and test-suite authoring on code, and does not catch up over the scale range tested; restating a
rule the prompt already supplied, as an executable predicate, is near-perfect. The deficit is therefore specific
to one-shot materialisation of a region with no compact rule to restate, and it has two escapes (green path)
that both require such a rule. Where none exists the failure is omission-dominated, resists local review,
survives same-model self-repair, and costs accuracy as an RLVR key.


    Measuring this cleanly requires ground truth that no LLM judge supplies, since using a judge
to grade judge-authorship is circular. We therefore build the entire measurement on constructed
ground truth, but no single construction is above suspicion. A lexical construction (WordNet synsets
[26], where the acceptable set for “a word meaning g” is enumerated by the lexicon) is intuitive but
incomplete: the lexicon omits some genuine synonyms, so a model that authors a correct-but-
lexicon-absent word is scored wrong, deflating apparent authoring precision. We therefore anchor
the paper on constructions where incompleteness is impossible, and use agreement across all three,
not any one, as the load-bearing evidence. (a) Complete truth: mechanically decidable predicates
(“contains a double letter”, “has ≥ 8 letters”) over a presented finite word list; the acceptable set is
exactly the list members the predicate accepts, computable and complete, so there is nothing for
incompleteness to hide. (b) Executable truth: HumanEval+ [23], where a hardened oracle test
suite decides code correctness by execution. (c) Lexical truth: WordNet, retained as a third,
independent construction whose recall -side findings are incompleteness-robust (a missing lemma
cannot inflate recall) and whose precision we report as a lower bound. Every number in this paper
is computed against one of these constructions; no model output is ever graded by a model. The
confound that could explain away any one construction (lexical incompleteness, oracle weakness,
predicate triviality) is orthogonal across the three, so their agreement is not.

Findings in brief. Across the Qwen2.5 family (3B–72B) with replication on Qwen3, Llama,
gemma, Mistral, and Phi-4: on the incompleteness-proof algorithmic construction judging rises
0.60 → 0.77 with scale while enumerating rises 0.26 → 0.48, so enumerating improves but does not
catch up (gaps +0.34/+0.25/+0.29/+0.29, all CI pairs disjoint). On executable code the separation
is largest: models judging at F1 0.74–0.90 author suites admitting only 19–42% of correct solutions.
Omission dominates the residual error and is 6–7× harder to surface in review than over-inclusion.
Asked for a predicate instead of an extension, the same models reach F1 ≈ 0.99. Used as an RLVR


                                                          3
reward, an authored key costs 1.9 points against a complete oracle, in every one of six paired seeds.
Table 1 maps every claim to its evidence and its status.

Contributions. Figure 1 previews the argument end-to-end and Table 1 maps each claim to its
supporting evidence (flagging the one falsified and two unconfirmed predictions). (i) The judging–
authoring asymmetry as a measured, judge-free, scale-resolved phenomenon. Authoring means
extensional enumeration on the word-list constructions and, for the executable construction, the
acceptance region an authored suite induces, since over an unbounded candidate space authoring is
intensional by necessity (§2). The result is triangulated across construction types whose confounds
are mutually orthogonal: mechanically complete truth, executable truth, and lexical truth. No
single incompleteness artifact can explain all three. The complete-truth construction also corrects
an impression native to any lexicon-only study, that authoring does not scale. It does scale, just
sub-critically, never catching execution over the range tested. (ii) the silent-omission mechanism: a
6–7× detectability asymmetry that explains why subtractive review pipelines shift authored specifi-
cations further toward omission rather than repairing them; (iii) production-scale field evidence that
model-authored answer keys fail omission-first and that even expert judging destabilizes exactly at
the specification boundary; (iv) two interventions, sample-then-verify repair (falsified) and RLVR
propagation (−1.9 pts against a complete oracle; −18.5 to −32.0 pts WordNet-relative across five
policies spanning a 24× scale range and a different family, the tax present at every scale, formalized
as a two-sided reward channel, Observation 3), plus a robustness sweep over scale, six model fam-
ilies/generations (Qwen2.5, Qwen3, Llama, gemma, Mistral, Phi-4), two executable benchmarks,
two complete-truth constructions, and four authoring prompts, showing the gap robust across all;
(v) a working mitigation, gating authored verifiers on a known-correct probe, which cuts code false-
rejection from 58–92% to ≤ 5%, turning the diagnosis into an actionable prescription; and (vi) a
repair for the majority the gate discards: rewriting each wrong expected value to what a reference
execution returns recovers 3.3–10.6× more usable suites across four author families, most where
the gate works least, which additionally separates the two operations suite authoring requires and
shows only one of them fails.


2    Formal Setup
Fix a finite candidate space V and a specification whose acceptable set is S ∗ ⊆ V . Two interfaces
expose the same underlying knowledge.
Definition 1 (Execution and authoring). The execution interface, given a query x ∈ V , returns
a membership judgment m̂(x) ∈ {0, 1} approximating ⊮[x ∈ S ∗ ]; it is scored by membership F1
over a query distribution that includes every member of S ∗ (positives) and curated hard negatives.
The authoring interface returns a set Ŝ ⊆ V approximating S ∗ ; it is scored by set F1, F1 (Ŝ, S ∗ ) =
2 |Ŝ∩S ∗ |
            , with recall ρ = |Ŝ ∩ S ∗ |/|S ∗ | and precision π = |Ŝ ∩ S ∗ |/|Ŝ|.
|Ŝ|+|S ∗ |

    Both interfaces are queried on the same items and draw on the same weights; only the output
type differs, a pointwise bit versus an entire set emitted under a causal mask with a learned stopping
rule. Scope of the construct. What we call “authoring” throughout is producing an artifact whose
induced acceptance region Ŝ is meant to be S ∗ , and what we score is always the fidelity of Ŝ, as a
classifier over the same candidates used to score execution. Three of our four constructions realise
this extensionally, emitting the members themselves, which is what answer keys and enumerated
rubrics require; the executable construction realises it intensionally, since over the unbounded
space of programs no extensional interface exists. What the paper does not claim is that models

                                                           4
Claim                                Evidence                                                                 Status
Enumerating ≪ judging,               complete truth +0.34/+0.25/+0.29/+0.29 (3B–72B, CIs disjoint)            confirmed,
one-shot; gap does not close                                                                                  triangulated
with scale
The deficit is enumeration, not      same models write the predicate for the same sets at F1 ≈0.99            confirmed,
knowledge or specification                                                                                    triangulated
Part of the gap is serialisation,    JSON-checkbox gains +0.09/+0.02/+0.13; 42% of 3B tokens off-list         confirmed, single
not set construction                                                                                          constr.
Authoring scales but                 algorithmic authoring F1 0.26→0.48                                       confirmed, single
sub-critically                                                                                                constr.
Omission is witness-poor :           net of clean-key false alarms, dover =+0.30 [.22,.40] vs. domit =+0.09   confirmed, two
harder to audit than                 [−.01,.20]                                                               constr.†
over-inclusion
Field signature at production        43K corpus: key errors omission-dominated 10:1                           observational
scale
Authored code suites over-reject     authored F1 0.07–0.60 vs. execution 0.35–0.90; suites admit 19–44% of    confirmed,
correct implementations              correct code                                                             triangulated
Sample-then-verify closes the        repaired F1 0.13–0.21 ≤ one-shot                                         falsified
scissors
Authored keys cost accuracy as       lexical −18.5 pts WordNet-relative, dz =6.5                              supported, 6/6
RLVR rewards                                                                                                  seeds, p=0.031‡
   — same effect on complete         −1.9 pts, dz =1.4; small because the key is accurate (recall 0.93)       supported, 6/6
truth                                                                                                         seeds, p=0.031‡
Gap robust across scale, family,     8 models, 2 benchmarks, 4 constructions, 4 prompts                       confirmed,
generation, benchmark, prompt                                                                                 triangulated
Test-time reasoning removes the      GPT-5.1 +0.259 → +0.008 (CI covers 0)                                    closes
gap where a compact rule exists
Reasoning does not reliably          Opus +0.274 → +0.096 (still >0); GPT-5.1 no improvement                  mixed
repair test-suite authoring
Known-correct-probe gate             FRR 0.58–0.92→≤0.05, at 5–39% yield                                      confirmed§
mitigates
Trace repair recovers most of        yield 3.3× to 10.6× over 4 author families, all at FRR ≤0.06,            confirmed, 4
the discarded suites                 catch-wrong ≥0.94                                                        authors
Low gated false rejection is         vs. a non-Qwen pool, gated FRR 0.010→0.064                               confirmed
partly pool-proximity

Table 1: Claim–evidence map; each row’s section gives the full evidence. Every construction number is
computed against constructed ground truth; no LLM judge grades any construction measurement, except the
field row (§6), which is judge-relative by nature. One registered prediction was falsified, two sub-predictions
were not confirmed, and a monotone scale trend in the RLVR tax was retracted after adding 72B. Status:
“triangulated” = holds across construction types with orthogonal confounds; “single constr.” = construct-
generality untested. Markers: † this review condition only; ‡ small against a complete oracle, large only
against the incomplete lexical reference; § weakest authors excepted, and repaired by the row below.


                                                        V (candidate space)

                                    S ∗ oracle                                         Ŝ authored


                                          omission               TP             over-incl.
                                           S ∗ \ Ŝ            Ŝ ∩S ∗            Ŝ \S ∗



                                            witness-poor                    review sees
                                            (starvation)                    = pollution

Figure 2: The geometry of an authored set. The authoring interface emits Ŝ; scored against the oracle S ∗ it
has recall ρ and precision π. Its two error regions behave oppositely under audit: over-inclusions are named
tokens a reviewer or an RLVR reward can act on, while omissions are unnamed. These crescents are the
starvation and pollution terms of Observation 3; the witness-poorness of the left crescent is Observation 2.


                                                                 5
cannot write predicates whose rule they were given: §3.11 shows that restating such a rule executably
is near-perfect. A test suite is also a predicate in the broad sense, and there the same models do
fail. The difference is that its expected behaviour must be derived from prose and examples rather
than restated (§3.11, closing paragraph). The deficit is in materialising Ŝ when no such compact
rule is available to restate: by enumeration where the set is finite, and by suite authoring where
it is not. The paper’s object of study is the gap ∆ = F1exec − F1auth as a function of scale, and
its decomposition through ρ and π (Figure 2). Two structural facts, established below, make the
gap consequential rather than cosmetic: omission errors (the S ∗ \ Ŝ side) are witness-poor : no local
review can certify their absence (Observation 2), and when Ŝ is used as a reward the gap becomes
a two-sided reward channel that displaces the RLVR optimum (Observation 3; Figure 9): both are
argued in Appendix A.


3     The Judging–Enumerating Scissors
3.1    Why the two interfaces differ: set construction vs. pointwise judgment
The two interfaces of Definition 1 draw on the same knowledge but factor through radically different
decoding problems (Figure 3). Execution answers a single presented query with one categorical
decision,
                                 m̂(x) = ⊮ pθ (yes | spec, x) > 12 ,
                                                                 
                                                                                                 (1)
a balanced binary judgment on a curated query (each true member against a hard negative). Au-
thoring must instead emit an entire set autoregressively, choosing both the elements and, critically,
when to stop, with no lookahead over candidates it has not yet sampled:
                                                                               k
                                                                               Y
               pθ (Ŝ = ⟨e1 , . . . , ek ⟩ | spec) = pθ (stop | spec, e1:k )         pθ (ei | spec, e<i ) .            (2)
                                                     |        {z          }          |        {z       }
                                                                               i=1
                                                         when to stop                 what to emit next

Scored against S ∗ , authoring F1 is the harmonic mean of its recall and precision,
                                       2ρπ                   −1
                           F1auth =        = 21 ρ−1 + 12 π −1     ≤ 2 min(ρ, π),                                       (3)
                                       ρ+π
so it is throttled by whichever of recall or precision is , which is what makes the WordNet precision
confound (§3.8) able to flatten F1auth even as ρ climbs.
    The algorithmic construction (§3.2) is designed to isolate the cost of Eq. (2) from knowledge.
Because the predicate is mechanically decidable over a presented list of L words, the execution arm
evaluates it pointwise and the induced “execution-composed” set Ŝexec = {x ∈ list : m̂(x) = 1} is
exactly what a perfect enumerator would emit. This gives a clean decomposition.

                        spec + one                                                                  one pass,
      execution                                     LM                  m̂(x) ∈ {0, 1}           balanced 2-class
                        candidate x


                                                                                                    enumerate Ŝ,
      authoring       spec only            LM             e1       e2         ···        stop?      no lookahead,
                                                                                                 decide when to stop

Figure 3: The two interfaces to the same weights. Execution (Eq. 1) is one forward pass yielding a single bit
on a curated, balanced query. Authoring (Eq. 2) emits the acceptable set left-to-right under a causal mask,
conditioning each element on the prefix (dashed) and choosing when to stop, with no access to candidates
it has not yet sampled. The paper measures how far apart these two readouts of the same knowledge sit.


                                                         6
Observation 1 (Set-emission penalty; an interpretation of the measurement). On a construction
where the full candidate universe U is presented to both arms, so candidate discovery is controlled:
the gap ∆ = F1exec − F1auth measures the cost of emitting the acceptable subset in one pass relative
to judging each presented candidate, holding per-candidate knowledge fixed. It is an upper bound
on set-construction cost, not a pure measure: it still bundles one-shot batch labeling, coverage,
and stopping (Eq. 2). The matched-budget decomposition (App. K) separates these components:
emission-vs-labeling, batching, and the programmatic-union floor, which is near zero by construction.

This is why the complete-truth constructions matter: the 15-item list is shown to both arms, so the
residual ∆ is not free-recall/candidate-discovery but one-shot set emission, and on the arithmetic
construction execution is near-perfect so almost all of ∆ is emission cost. For the open-set con-
structions (code, lexical), where U is not presented, a second and larger force is candidate discovery,
compounded by base-rate dilution: authoring emits into a space where true members have base rate
b ≪ 12 , so precision π = b TPR+(1−b)
                               b TPR
                                      FPR collapses as b → 0, whereas execution is scored on a curated
                     1
balanced set (b = 2 ). We therefore attribute the open-set gap to discovery+emission jointly, and
isolate the emission component only on the complete-truth constructions.

3.2   Judge-free constructions
Every construction instantiates the same two tasks over the same items, so that only the interface
to the model’s knowledge differs: Authoring (open-set): produce the complete acceptable set,
scored by precision/recall/F1 of the normalized predicted set against the constructed oracle set; and
Execution (closed-set): judge one presented candidate’s membership (yes/no), posed for every
oracle member (positive) and every hard negative, scored as membership F1 on the positive class
plus raw accuracy. Authoring F1 and execution membership F1 are the two comparable axes of the
scissors. Construction and training details are in Appendix C, worked examples in Appendix D,
full per-model results in Appendix F, and a per-predicate breakdown in Appendix E. We use three
construction types whose incompleteness confounds are mutually orthogonal (the complete-truth
type is instantiated by two constructions, string and arithmetic; four in total).
    (a) Algorithmic (complete truth). Each item presents a finite list of 15 real English words
(drawn from WordNet lemmas, length 3–11, deterministically shuffled, seed 0) and one mechanically
decidable predicate: contains a double letter, has ≥ 8 letters, contains “th”, ends in “s”, cycled across
n=240 items, lists resampled to keep a non-degenerate accept/reject split. The acceptable set is ex-
actly {w ∈ list : predicate(w)}: computable, finite, and complete by construction, so incompleteness
cannot inflate any error. Authoring asks the model to list every list-word satisfying the predicate;
execution asks, for each list-word, whether it satisfies the predicate. Any authoring<execution gap
here isolates set-enumeration and stopping from world knowledge, because the predicate needs none.
    (b) Executable (execution truth). HumanEval+ [23]: authoring a test suite from a doc-
string, executing candidate-correctness judgment against an oracle-verified solution pool; full design
and results in §3.4.
    (c) Lexical (WordNet). Synsets with 3–8 single-word lemmas and a usage example, excluding
highly polysemous targets (> 4 senses), n=240 after deterministic sampling (seed 0). Each item
anchors a sense by gloss g and example e; the oracle set is the synset’s lemma set; hard negatives
are co-hyponyms, hypernym lemmas, and antonyms. Authoring: “List every single English word
that can mean ‘g’ (as in: ‘e’).” Execution: “Can the word ‘c’ mean ‘g’ (as in: ‘e’)? yes/no.”
This construction is intuitive but incomplete, the lexicon omits some real synonyms, so we treat its
precision as a lower bound and lean on its incompleteness-robust recall side (§3.8).
    Models: Qwen2.5-Instruct at 3B/7B/14B/72B [29] (a single family, so scale is the only variable),


                                                   7
                                        Algorithmic (string, complete truth)                                 Arithmetic (numeric, complete truth)
                            1.0                                                                   1.0



                            0.8                                                                   0.8

                                                                                                                                                  Qwen2.5
                            0.6                                                                   0.6                                             Qwen3
                                                                             execution                                                            Llama
 F1




                                                                                             F1
                                                                             authoring                                                            Mistral
                                                                                                                                                  Phi
                            0.4                                                                   0.4
                                                                                                                                                  gemma


                            0.2                                                                   0.2



                            0.0                                                                   0.0
                                   3B         7B        14B            32B       72B                    3B         7B        14B            32B      72B

                                             Executable code (oracle)                                                   Lexical (WordNet)
                            1.0                                                                   1.0
 exec F1 / accept-correct




                            0.8                                                                   0.8



                            0.6                                                              F1   0.6



                            0.4                                                                   0.4



                            0.2                                                                   0.2



                            0.0                                                                   0.0
                                   3B         7B        14B            32B       72B                    3B         7B        14B            32B      72B
                                                   Model scale (log)                                                    Model scale (log)

Figure 4: The judging–enumerating scissors across four LLM-judge-free constructions and six model fami-
lies/generations. Colour encodes interface (blue judging; magenta authoring, i.e. extensional enumeration on
the word-list panels, test-suite authoring on the code panel, per §2); marker shape encodes family. Qwen2.5
is drawn as connected lines with 95% bootstrap CI bands and the shaded gap; the other families are points
at their parameter count. In every model–construction cell evaluated, judging sits above enumerating and
the gap does not close over the tested scale range (coverage matrix in App. F). On executable code the
separation is largest.


with cross-family replication from Qwen3-14B/32B, Llama-3.2-3B/3.1-8B, Mistral-7B, and Phi-4
(algorithmic and code) and gemma-4-12B (lexical); greedy decoding throughout.

3.3                               Results: the scissors on complete truth
Table 2 is the paper’s central measurement, chosen because it is immune to the incompleteness
confound (§3.8): the predicate decides membership mechanically over a list the model is shown, so
a word is acceptable iff the predicate accepts it: there is no “missing synonym” to mislabel. Three
readings. First, the asymmetry is present at every scale and statistically clean: every authoring–
execution CI pair is disjoint, in both families. Second, and correcting the impression a lexicon-only
study would give, authoring is not a flat line: it improves substantially with scale (Qwen
0.259→0.483). What does not happen is catching up: the gap narrows from 0.34 (3B) to 0.25 (7B),
then settles at ≈ 0.29 for 14B–72B rather than closing. Authoring does improve with scale, over the
small-model range even faster than execution, but the two never converge: the gap stops shrinking

                                                                                         8
   Family      Model    Authoring F1 [95% CI]      Execution F1 [95% CI]        Exec. acc.     Gap [95% CI]
               3B            0.259 [.23,.29]           0.599 [.55,.64]            0.826        +0.340 [.29,.39]
               7B            0.405 [.37,.44]           0.657 [.63,.68]            0.735        +0.252 [.22,.29]
   Qwen2.5
               14B           0.475 [.44,.51]           0.761 [.73,.79]            0.855        +0.286 [.25,.32]
               72B           0.483 [.45,.52]           0.769 [.74,.79]            0.884        +0.286 [.25,.32]
               3.2-3B        0.439 [.41,.47]              0.567 [.52,.61]           —          +0.128 [.09,.17]
   Llama-3
               3.1-8B        0.485 [.46,.51]              0.676 [.64,.71]           —          +0.190 [.16,.22]
Table 2: Complete truth (algorithmic, n=240, greedy; bootstrap CIs). The acceptable set is computed
by a mechanical predicate over a presented finite list, so no incompleteness is possible and every authoring
error is genuine. Enumerating improves with scale (0.26 → 0.48) but judging stays above it, every CI pair is
disjoint, and the gap does not close (+0.34, +0.25, +0.29, +0.29). Llama-3 reproduces the ordering at both
sizes.


well above zero. Third, the effect is not Qwen-specific: Llama-3.2-3B and Llama-3.1-8B show
the same execution>authoring ordering with disjoint CIs (gaps +0.13, +0.19); the gap is smaller
for Llama than for Qwen because it pairs weaker execution with stronger authoring at this scale
(Llama-3.2-3B authors 0.44 vs. Qwen2.5-3B’s 0.26), so both differences shrink the gap. Figure 4
shows the same structure holding across all four constructions and all six model families/generations
simultaneously.

A second complete-truth construction (arithmetic). To check that the complete-truth re-
sult is not specific to string predicates, we repeat the design with numeric predicates (is even,
divisible by 3, > 50, prime) over presented integer lists: again mechanically decidable, again zero in-
completeness, but disjoint in surface form and knowledge from the word-list construction (Table 3).
The scissors is unchanged: execution reaches 0.94–1.00 (the predicates are trivial to check pointwise)
while authoring plateaus at 0.66–0.79, a gap of +0.28, +0.30, +0.22, +0.21 with disjoint CIs. That
execution is near-perfect here sharpens the reading of Observation 1: since pointwise membership is
essentially solved and the candidate list is shown to both arms, the residual ≈ 0.25 gap is dominated
by one-shot set emission rather than knowledge or discovery (decomposed in App. K).

                     Model            Authoring F1     Execution F1         Gap [95% CI]
                     Qwen2.5-3B           0.660               0.936         +0.276 [.25,.30]
                     Qwen2.5-7B           0.699               1.000         +0.301 [.27,.33]
                     Qwen2.5-14B          0.760               0.978         +0.218 [.19,.24]
                     Qwen2.5-72B          0.787               1.000         +0.213 [.19,.24]
Table 3: A second complete-truth construction: numeric predicates over presented integer lists (n=240,
2,000-resample CIs). Execution is near-perfect (the predicates are pointwise-trivial), so the persistent 0.21–
0.30 gap is dominated by one-shot set emission (Observation 1; App. K), independent of the algorithmic
string construction.



3.4    The executable construction: authored suites vs. oracles
The lexical and algorithmic constructions have sharp ground truth but a skeptic may ask whether
the asymmetry survives where the community actually authors verifiers, unit tests, with correctness
decided by execution, the strongest ground truth available. This is the executable construction of
§3.2, and it produces the largest scissors in the paper.


                                                      9
  Family     Model    Exec. F1 [95% CI]    Accept-corr.    Canon. acc. [95% CI]   Catch-wrong   FRR|sane
  HumanEval+ (164 problems)
          3B        0.763 [.72,.81]           0.331           0.348 [.28,.42]        0.937        0.043
          7B        0.853 [.82,.88]           0.186           0.201 [.14,.27]        0.980        0.051
  Qwen2.5
          14B       0.742 [.69,.79]           0.289           0.268 [.20,.34]        0.971        0.025
          72B       0.895 [.87,.92]           0.422           0.390 [.32,.46]        0.966        0.014
             3.2-3B     0.580 [.51,.64]       0.209           0.213 [.15,.27]        0.963         0.007
  Llama-3
             3.1-8B     0.766 [.72,.81]       0.101           0.134 [.09,.19]        0.976         0.000
  MBPP+ (378 problems; pool built the same way)
          3B        0.715 [.68,.75]      0.357                0.288 [.24,.33]        0.940         0.028
          7B        0.828 [.81,.85]      0.211                0.156 [.12,.20]        0.975         0.000
  Qwen2.5
          14B       0.787 [.76,.82]      0.270                0.217 [.18,.26]        0.972         0.026
          72B       0.871 [.85,.89]      0.441                0.339 [.29,.39]        0.966         0.011
Table 4: Executable truth (HumanEval+ as a hardened executable reference, not a decision procedure
for program equivalence; pool of 1,560 reference-passing / 904 reference-failing solutions; execution F1 with
bootstrap CIs). Models that judge correctness at F1 up to 0.90 author suites admitting only 19–42% of correct
solutions while still catching 94–99.8% of wrong ones. Accept-correct is a recall, so it is not comparable to
execution F1; Table 5 scores both arms with the same statistic. The population is bimodal: among suites
that accept the reference, false rejection collapses to ≤ 5%.


Design. From HumanEval+ [23] (164 problems) we build an oracle-verified solution pool: 2,464
candidate solutions sampled from Qwen2.5-7B/14B (K=8, T =0.8), each graded by the full EvalPlus
suite, yielding 1,560 oracle-correct and 904 oracle-wrong solutions, a diverse pool of independently
certified implementations. The two arms, both scored by sandboxed execution: Execution: present
the docstring and one pooled solution and ask the model to judge correctness (yes/no), scored vs. the
oracle label as membership F1; Authoring, the model writes a test suite (def check(candidate))
from the docstring alone, and we run oracle-labeled solutions through it, reporting accept-correct
(fraction of oracle-correct solutions the suite admits), canonical acceptance (does the suite even
admit the reference solution), catch-wrong (fraction of oracle-wrong solutions rejected; the suite
must not be trivially permissive), and FRR|sane (false-rejection rate among suites that pass the
canonical check). Both arms are run at all four Qwen scales and for Llama-3.2-3B/3.1-8B.

Results. Authored suites do not err at the margin; they over-reject (Table 4). Per the scope defini-
tion of §2, this arm scores the acceptance region an intensional artifact induces, not an enumeration.
The two levels then separate cleanly. At the artifact level the dominant error is over-specification:
invented requirements and wrong expected outputs, with 70% of suites rejecting the canonical so-
lution by assertion (App. D), not missing test cases. At the induced-set level the consequence is
omission: correct implementations fall outside the acceptance region. The code construction there-
fore shares the paper’s consequence, an acceptable set too small and invisibly so, while differing in
mechanism, and we use it only at that consequence level: the enumeration mechanics of §3.1 and
the detectability results of §4 are established on the word-list arms and are not claimed for suites.
Across scale, models that judge correctness at execution F1 0.74–0.90 author suites admitting only
19–42% of oracle-verified correct solutions while catching 94–99.8% of wrong ones. Code author-
ing is non-monotone in scale (accept-correct 0.33/0.19/0.29/0.42 at 3B/7B/14B/72B, so only 72B
exceeds 3B) and stays far below judging everywhere; Llama’s suites are stricter still (8–10%). The
conditional structure is the sharpest finding: given that a suite accepts the canonical solution, its
false-rejection rate on other correct implementations collapses to ≤ 5%. The authored population


                                                      10
                                      Authored suite as a classifier   Exec.        Gap
              Bench      Model        Prec.   Rec.     F1     MCC       F1     ∆F1 [95% CI]
                         Qwen 3B      0.900   0.331 0.484 0.306 0.763 +0.279 [.18,.38]
                         Qwen 7B      0.942   0.186 0.311 0.243 0.853 +0.542 [.45,.64]
                         Qwen 14B     0.944   0.289 0.442 0.317 0.742 +0.300 [.20,.40]
              HE+
                         Qwen 72B     0.955   0.422 0.586 0.417 0.895 +0.309 [.23,.39]
                         Llama 3B     0.907   0.209 0.340 0.236 0.580 +0.240 [.14,.34]
                         Mistral 7B   0.776   0.054 0.101 0.063 0.801 +0.700 [.62,.77]
                    Qwen 3B           0.913   0.357 0.514 0.330 0.715          +0.201 [.14,.26]
                    Qwen 7B           0.936   0.211 0.344 0.254 0.828          +0.484 [.42,.55]
              MBPP+
                    Qwen 14B          0.945   0.270 0.421 0.302 0.787          +0.366 [.30,.43]
                    Qwen 72B          0.958   0.441 0.604 0.429 0.871          +0.267 [.22,.33]
Table 5: Same statistic, same pool. Both interfaces scored as binary classifiers over the identical oracle-
labelled pool, so the gap is a paired difference of one quantity rather than execution F1 minus authoring
recall. CIs are problem-cluster bootstraps, since solutions nest in problems. This matters asymmetrically:
the execution arm contributes one independent judgment per solution, whereas the authoring arm contributes
one artifact per problem whose verdicts on that problem’s solutions are perfectly correlated by construction,
so its effective sample size is the 164 (HumanEval+) or 378 (MBPP+) problems, not the pooled solution
count. Resampling problems rather than solutions is what makes the two arms comparable; a solution-level
bootstrap would understate the authoring arm’s uncertainty by roughly the average cluster size. Every
cell keeps a positive gap with a CI excluding zero under the clustered procedure. Authored suites are
high-precision, low-recall: what they accept is almost always correct, but they admit only 4–44% of correct
solutions.


is bimodal, a small sane minority and a large majority whose assertions encode incorrect expected
behavior. Validating a generated verifier on known-correct solutions before trusting it, the disci-
pline human re-annotation applies to benchmark suites [7], is the difference between a ≤ 5% and a
58–92% false-rejection instrument.
    Second executable benchmark (MBPP+). Repeating the entire protocol on MBPP+ [2, 23] (378
problems, pool built the same way) leaves the scissors unchanged: execution F1 0.72–0.87 against
accept-correct 0.21–0.44, the same sub-critical scaling, the same near-zero FRR among canonical-
sane suites, and the same high catch rate (Table 4, lower block).
    Error-type audit. A dedicated one-shot 14B study (a separate, stricter prompt; canonical ac-
ceptance 20.7%) classifies every rejection by exception type and shows the failure is semantic, not
mechanical: of 164 suites, 115 (70%) run correctly and fail on assertions, meaning the suite executes
but its author-computed expected outputs are wrong, while only 15 (9%) crash. Among rejection
events from broken suites, 87.5% are assertion failures against 11.3% runtime errors. Seven in ten
authored verifiers are thus wrong-by-assertion: syntactically healthy artifacts confidently encoding
incorrect expected behavior. This is also why catch-wrong stays high while accept-correct collapses.
An over-constrained suite rejects almost everything, so its ability to reject wrong code is no evidence
that it admits right code; since specificity stays 0.94–0.98, the low accept-correct reflects genuine
under-acceptance rather than a permissive suite inflating a balanced score. Related SE work makes
the direction plausible, finding that generated oracles encode the author’s misreading of the spec
[20] and that benchmark tests unfairly reject valid solutions [7], but it has not measured authoring
against a certified-diverse correct pool with the model’s own judging as the paired baseline.




                                                     11
  Family     Model     Ungated FRR     Gated FRR      Yield   Gated catch-wrong    Gated BA    Vacuous
             3B             0.669         0.043      0.348           0.826           0.892      0.053
             7B             0.814         0.051      0.201           0.914           0.932      0.000
  Qwen2.5
             14B            0.711         0.025      0.268           0.919           0.947      0.023
             72B            0.578         0.014      0.390           0.919           0.953      0.016
             3.2-3B         0.791         0.007       0.213          0.770           0.882      0.086
  Llama-3
             3.1-8B         0.899         0.000       0.134          0.857           0.929      0.000
  Mistral    7B-v0.3        0.946         0.000       0.049          0.542           0.771       0.250
Table 6: A working mitigation (HumanEval+, same authored suites as Table 4): discard any suite that
rejects a known-correct probe. False rejection falls from 0.58–0.92 to ≤ 0.05, at the cost of yield. The
gate is not passed by being vacuous: survivors still reject 83–100% of wrong solutions with ≤ 5% accepting
everything. It is only as good as the author, though: for Mistral-7B a quarter of survivors are vacuous and
gated catch-wrong falls to 0.54. That defect is repaired rather than probed around: on an independently
authored Mistral suite set whose gate leaves 43% of survivors vacuous at catch-wrong 0.471, trace repair
returns catch-wrong 1.000 with no vacuous survivors (§3.6). (Llama’s rows were originally far worse; that
was a tokenization defect on our side, not the models’; see App. G.)


3.5    A working mitigation: gate on known-correct probes
The repair arm (§4.4) shows the failure cannot be fixed by better authoring or self-verification. But
the bimodal structure of Table 4, in which broken suites reject the reference too while sane suites
are near-perfect, implies a cheap external gate: trust a model-authored suite only if it accepts a
solution already known to be correct. The canonical reference solution is the cheapest such probe,
and the gate is one execution. We should not oversell its availability: on a benchmark a reference
implementation is given, but on a real task obtaining one may be the very problem being solved,
a single hand-verified input/output example is much weaker than a reference implementation, and
gates correspondingly less. The honest scope is: wherever any known-correct behaviour can be
exhibited, use it as a gate; that is strictly better than trusting the suite, and it is not always
obtainable. Table 6 and Figure 5 quantify the trade-off on the HumanEval+ suites (probe-strength
sweep in Appendix I). Gating on the reference solution converts a 58–92% false-rejection instrument
into a ≤ 5% one (0% for Llama), at the cost of yield : only 20–39% of Qwen suites (7–10% of Llama’s)
survive the gate. Holding out k=1–3 pooled correct solutions as probes instead of the canonical
gives the same picture (FRR 0.01–0.08).
    This is the actionable form of the paper’s thesis: a model-authored verifier is usable only after
external validation against known-correct behavior. The gate is not a fix for authoring but a filter,
admitting the rare sane suite and rejecting the common broken one. Its cost is the discarded
majority, and §3.6 shows that most of that majority need not be discarded at all.

3.6    Repair instead of discard: execution can supply what authoring cannot
The gate throws away four suites in five, and our own audit says it need not: among rejection events
from broken suites, 87.5% are assertion failures and only 11.3% runtime errors (§3.4). An assertion
failure means the model chose an input and then computed the wrong expected output for it, and
that output is what executing a known-correct solution supplies. So rather than discard a suite that
fails the gate, rewrite each wrong expectation to the value the reference returns, and re-gate. This
also performs the decomposition §3.11 argues for: suite authoring needs an extensional operation,
choosing which inputs to check, and an intensional one, computing what each should return. Repair
hands the intensional half to execution, so what a repaired suite still catches measures the model’s


                                                    12
                                          1.0


                                          0.8




                   False-rejection rate
                                          0.6


                                          0.4


                                          0.2
                                                   y=0.35         y=0.20
                                                                                  y=0.27      y=0.39        y=0.07         y=0.10
                                          0.0
                                                Qwen 3B       Qwen 7B        Qwen 14B      Qwen 72B     Llama 3B      Llama 8B


                                                            ungated (trust all suites)      gated on known-correct probe


Figure 5: The known-correct-probe gate (§3.5). Trusting all authored suites gives a 0.58–0.92 false-rejection
rate (magenta); discarding suites that reject the canonical reference collapses it to ≤ 0.05 (green). The
annotation y is yield, the fraction of authored suites that survive the gate; most do not, which is itself a
restatement of the fail-closed result.


input selection with expectations held perfect.
    Two rules keep the measurement honest. No assertion is ever dropped in the headline
condition, since deletion would raise yield for free by making suites vacuous. And because repairing
from the reference and then gating on it is tautological, every reported quantity is measured
on solutions the repair never saw: false rejection on the held-out EvalPlus-correct pool, catch-
wrong on the EvalPlus-wrong pool. A repair that “succeeded” by accepting everything would show
as catch-wrong collapsing.
    The discard is largely unnecessary (Table 18). For the Qwen2.5-14B suites yield rises from
0.207 to 0.690, a 3.3× recovery whose interval does not overlap the gate’s, while false rejection
(0.010 → 0.036) and catch-wrong (0.951 → 0.946) stay within overlapping intervals. Repair is a no-
op where nothing was broken: of the 34 suites that already passed, none regress and their metrics
are unchanged to three decimals. The recovery grows as the author weakens. Re-authoring the same
164 specifications with three further families, the recovery factor rises monotonically as the gate’s
yield falls: 3.3× at Qwen2.5-14B, 4.7× at Llama-3.2-3B, 6.9× at Llama-3.1-8B, 10.6× at Mistral-
7B. Every repaired population lands in the same band (FRR 0.035–0.059, catch-wrong ≥ 0.94), so
what differs across authors is how much there is to recover, not the quality of what is recovered.
Mistral is the sharpest case and the one §3.5 flagged as the gate’s weak point: its survivors go from
43% vacuous at catch-wrong 0.471 to none vacuous at 1.000. The known-wrong probe we proposed
for weak authors is unnecessary if their failed suites are repaired instead of filtered.
    Three readings follow. (i) The extensional half is not the problem. With expectations made
perfect, the model’s chosen inputs still reject 94.6% of wrong solutions: it picks discriminating inputs
well and computes their expected outputs badly, as §3.11 predicted. (ii) The residual failure is a
different authoring error. Every suite still failing after value repair contains an invented exception
contract, an assert False sentinel demanding the function raise on inputs the specification never
mentions. That is a promise the spec never made rather than a miscomputed value, so substitution
cannot touch it. Neutralising those sentinels deletes rather than corrects, so we report it only as a
ceiling (yield 0.819 at catch-wrong 0.942); the neutralisation is self-limiting, since an assert False
is reached only when the reference did not raise. (iii) It does not rescue self-repair. §4.4 showed the
model cannot fix its own suites; here the repairing agent is the interpreter, not the model. Together
the two are the paper’s prescription in miniature: an authored artifact is salvageable, but only by
an external oracle, never by its author.
    This also bears on the word “omission”. Our vocabulary comes from the word-list constructions,

                                                                                    13
               Construction            Direction             D   F       d = D − F [95% CI]
                                       over-inclusion    0.943 0.640    +0.303 [+.215, +.395]
               Algorithmic (n=114)
                                       omission          0.636 0.544    +0.092 [−.013, +.197]
                                       over-inclusion    0.858 0.654   +0.204 [+.133, +.273]
               Lexical (n=240)
                                       omission          0.569 0.842   −0.273 [−.337, −.208]
Table 7: Repair recovers most of what the gate discards, and recovers more the worse the author is
(HumanEval+, n=164 suites per author, problem-cluster bootstrap; the solution pool is held fixed so the
author is the only variable). Trace repair rewrites each wrong expected value to what the reference solution
actually returns. Every repaired population lands in a narrow band (FRR 0.035–0.059, catch-wrong ≥ 0.94)
while the gate alone keeps between 4% and 21% of suites, so the recovery factor is largest exactly where the
gate is least usable. FRR is measured on held-out EvalPlus-correct solutions and catch-wrong on EvalPlus-
wrong ones, never on the reference the repair read, so the numbers are not tautological; a repair that “worked”
by accepting everything would show as catch-wrong collapsing. For Qwen2.5-14B, additionally neutralising
the 63 invented assert False contracts raises yield to 0.819 at catch-wrong 0.942; because that deletes
rather than corrects an assertion it is a ceiling, not the method.


where the model genuinely cannot produce the missing member. The code failure has the same
shape, an induced acceptance region that is wrong, but a different mechanism, and readers should
not carry the lexical one into the code results. The scope is likewise narrow: repair requires a
reference implementation, the assumption §3.5 already flags as unavailable when obtaining one is
the task. Where it holds, discarding is the wrong default.
    One caveat we can now quantify, and it cuts against us. Both gate and repair are scored against
a pool of oracle-verified solutions generated by Qwen2.5-7B/14B, so a Qwen-authored suite has
been meeting code written in a style close to its own. A second pool from three non-Qwen families
under an identical sampling budget (1,781 verified-correct solutions over 142 problems) raises false
rejection in every arm: gated Qwen2.5-14B 0.010 → 0.064, and repaired 0.036 → 0.075 (Qwen2.5-
14B), 0.035 → 0.123 (Llama-3.1-8B), 0.059 → 0.161 (Mistral-7B). Validity is not what changed,
since every solution in either pool passes the full plus-suite; the rise measures how much of the
low figure came from stylistic proximity. The gate’s headline should therefore read “≤0.05 against
implementations resembling the pool’s authors, rising to ≈0.06–0.16 against more distant ones”.
The qualitative conclusion is unchanged, since the worst cross-family figure is far below the 0.58–
0.92 of trusting suites ungated, and it sharpens what the residual over-rejection is: authored suites
encode incidental properties of one implementation.

3.7    Frontier: newer generations and closed models
A natural rebuttal is that a stronger or newer model closes the gap, so it is a temporary artifact
of mid-tier open models. We test this two ways: a full generation step on open weights (Qwen3
vs. Qwen2.5 at matched 14B, plus Qwen3-32B), and two closed frontier models, OpenAI GPT-5.1
and Anthropic Claude Opus 4.8, run via API with reasoning disabled to match the one-shot pro-
tocol (Table 9). Table 8 and Figure 6 show the gap is invariant to the generation. At matched
14B scale, Qwen3 improves both interfaces over Qwen2.5 (algorithmic execution 0.761→0.795, au-
thoring 0.475→0.497; code execution 0.742→0.800, accept-correct 0.289→0.324) but the authoring–
execution gap does not shrink, if anything it widens slightly (+0.286→ + 0.298 algorithmic). All
results here are one-shot and greedy, with reasoning disabled where it is optional, so they charac-
terize a specific protocol : parameter count is varied, inference compute is held near-constant (the
compute axis is varied separately in App. K, where 16× sampling raises union recall but not past
execution), and we do not claim the gap would survive arbitrary decoding, reasoning budgets, or

                                                        14
                                                     Qwen2.5-14B               Qwen3-14B        Qwen2.5-72B           Qwen3-32B
                                  Authoring F1            0.475                   0.497             0.483                   0.512
       Algorithmic                Execution F1            0.761                   0.795             0.769                   0.822
                                  Gap                     +0.286                 +0.298            +0.286                   +0.309
                                  Execution F1             0.742                 0.800              0.895                   0.783
       Code
                                  Accept-correct           0.289                 0.324              0.422                   0.262
Table 8: Frontier / cross-generation control. A full generation newer (Qwen3 vs. Qwen2.5), at matched
14B scale, lifts both interfaces but does not close the authoring–execution gap (it widens slightly on the
complete-truth construction). Over the one-shot protocol tested, the gap does not shrink with scale, family,
or generation (we do not claim invariance beyond that protocol; cf. the reasoning condition below).

                                                   open-weight (local)                             closed frontier (API)
                                                                                                 +0.26              +0.08
                           1.00
                                                 +0.30                            +0.31
                                   +0.29                          +0.29
          Algorithmic F1




                           0.75


                           0.50


                           0.25


                           0.00
                                  Qwen2.5      Qwen3             Qwen2.5          Qwen3         GPT-5.1          Opus 4.8
                                   14B          14B               72B              32B


                                                                    execution       authoring


Figure 6: The gap survives a model generation and the jump to the closed frontier. Left of the divider
(open weights, local): Qwen3 raises both interfaces over Qwen2.5 at matched scale without shrinking the
gap (bold numbers). Right (closed frontier, API, reasoning disabled to match the one-shot protocol): both
models push judging to 0.93–0.96 while enumerating lags, by +0.26 for GPT-5.1 and +0.08 for Opus, which
nearly closes this construction but retains +0.14 on numeric and a large gap on code.


future training methods. Within that protocol, no open-weight axis we vary, whether scale (§3.3),
family (Llama, gemma), or generation (Qwen3), makes authoring catch execution; at the closed
frontier the strongest models narrow the gap on the simplest constructions (Opus algorithmic,
GPT-5.1 numeric) but neither closes both, and both retain a large gap on code (Table 9).
    At the closed frontier (Table 9), the scissors narrows but does not disappear. GPT-5.1 and
Opus 4.8 execute the specification at F1 0.93–0.96 (algorithmic) and 0.87–0.93 (code); their au-
thoring improves markedly over open weights, and each strongest model nearly closes one simple
construction: Opus on algorithmic (0.881 authoring, +0.08 gap) and GPT-5.1 on numeric (+0.04),
but neither closes both (GPT-5.1 stays +0.26 on string predicates, Opus +0.14 on numeric), and
both admit under half of oracle-correct code (36–44%). Frontier capability therefore relocates the
gap to the harder authoring domain rather than eliminating it; on open weights it persists at every
scale.

Test-time reasoning closes it, where a rule can be executed. We then ran the strongest
form of the “a better model fixes it” rebuttal that we had earlier only flagged: the same two models
with reasoning enabled (effort=low, n=120, algorithmic construction; Table 9, bottom). It does
fix it here. GPT-5.1’s authoring rises 0.673 → 0.976 and its gap falls to +0.008 with a bootstrap
CI covering zero; Opus reaches 0.964 authoring and a +0.035 gap. We report this as a negative


                                                                          15
                 Construction    metric                     GPT-5.1               Claude Opus 4.8
                                 Authoring F1                0.673                     0.881
                 Algorithmic     Execution F1                0.932                     0.961
                                 Gap                         +0.259                   +0.080
                 Numeric         Gap                         +0.041                   +0.140
                                 Execution F1                 0.872                      0.933
                 Code (HE+)
                                 Accept-correct               0.361                      0.441
                 Reasoning enabled (off-protocol; effort=low, n=120, algorithmic)
                                Authoring F1             0.976               0.964
                 Algorithmic    Execution F1             0.984               0.999
                                Gap                +0.008 [−.01,.02]    +0.035 [.02,.05]
Table 9: Closed frontier (GPT-5.1, Claude Opus 4.8; n=240 per complete-truth construction, HumanEval+
pool for code). Frontier capability narrows the gap on the simplest constructions without abolishing it: each
strongest model nearly closes one of them, neither closes both, and both retain a large gap on code. With
reasoning enabled (bottom block) the algorithmic gap closes for GPT-5.1 (CI covers zero) and nearly so for
Opus; §3.7 discusses why, and Table 10 shows the same intervention on test suites. Gemini 3.x is omitted:
its API mandates reasoning, so it cannot run the matched reasoning-off protocol.

                                         Authored suite as a classifier            Exec.          Gap
       Model       Reasoning     Prec.      Rec.      F1 [95% CI]         MCC       F1       ∆F1 [95% CI]
                   off          1.000       0.387    0.558 [.42,.67]      0.420    0.867     +0.309 [.20,.44]
       GPT-5.1
                   on           0.974       0.316    0.477 [.34,.60]      0.343    0.918     +0.441 [.32,.58]
                   off           0.963     0.490     0.650 [.54,.75]   0.454       0.924     +0.274 [.18,.39]
       Opus 4.8
                   on            0.957     0.787     0.864 [.79,.92]   0.683       0.960     +0.096 [.04,.17]
Table 10: Does test-time reasoning repair test-suite authoring? Matched 2 × 2 on one fixed 80-problem
HumanEval+ subsample, effort=low; both arms scored as classifiers on the same pool, CIs are problem-
cluster bootstraps. It substantially helps one model and closes nothing. Opus’s reduction is clean, its two
∆F1 intervals being disjoint, yet the residual still excludes zero. GPT-5.1’s point estimate moves the wrong
way while recall and canonical acceptance fall, but its intervals overlap, so we claim only no improvement.
Contrast Table 9, where reasoning closes the algorithmic gap outright.


result for the universality of our headline: on a construction whose acceptable set is generated
by a mechanically executable rule, one-shot greedy decoding is not the only regime that matters,
and test-time reasoning removes the deficit. The mechanism is the one §3.11 identifies, which is
why we find the result coherent rather than contradictory: a scratchpad lets the model apply the
rule candidate-by-candidate, internally reconstructing the intensional-then-execute route instead of
emitting the set in a single pass. Reasoning and predicate-emission are two ways to buy the same
escape.

But on test suites the escape is unreliable. We then ran the same condition where no compact
rule generates the acceptable set: authoring a test suite, in a matched 2 × 2 on a fixed 80-problem
HumanEval+ subsample (Table 10). Reasoning does not transfer cleanly, and scoring both arms
with the same statistic (as in Table 5) makes the result precise. For Opus the improvement is
large and statistically clean: authored-suite F1 0.650 → 0.864 and ∆F1 +0.274 → +0.096, with
disjoint problem-cluster intervals ([.18, .39] vs. [.04, .17]), but the residual gap still excludes zero, so
reasoning shrinks this construction’s gap without closing it. For GPT-5.1 there is no improvement:


                                                       16
                               Authoring (open-set)                  Execution
      Model           P (lower bd.)     R       F1 [95% CI]      memb. F1 [95% CI]      Gap [95% CI]
      Qwen2.5-3B          0.153       0.233    0.153 [.13,.18]     0.331 [.29,.38]     +0.178 [.13,.23]
      Qwen2.5-7B          0.223       0.364    0.248 [.22,.28]     0.699 [.66,.73]     +0.451 [.41,.49]
      Qwen2.5-14B         0.153       0.448    0.211 [.19,.24]     0.599 [.56,.64]     +0.388 [.34,.43]
      Qwen2.5-72B         0.129       0.581    0.191 [.17,.21]     0.786 [.76,.82]     +0.596 [.56,.63]
      gemma-4-12B         0.132        0.518   0.191 [.17,.21]     0.743 [.71,.78]     +0.552 [.52,.59]
Table 11: The scissors on lexical truth (WordNet, n=240, greedy; 2,000-resample bootstrap 95% CIs).
Reported for triangulation, with its confound made explicit: authoring precision is a lower bound, because
a valid synonym the lexicon lacks is scored as a false positive. The incompleteness-robust signal is recall (a
missing lemma cannot inflate it), which rises with scale (0.233→0.581), so knowledge is increasingly present
while F1 stays low. gemma-4-12B reproduces the gap.


F1 0.558 → 0.477 and ∆F1 +0.309 → +0.441, with recall 0.387 → 0.316 and canonical acceptance
falling, consistent with a scratchpad making it over-specify more, the failure of §3.4 amplified rather
than repaired, though its two intervals overlap, so we claim only that reasoning does not help it, not
that it significantly hurts. Precision stays 0.96–1.00 and execution improves for both (0.867 → 0.918,
0.924 → 0.960), so no suite population is becoming vacuous. The pattern across the two constructions
is therefore consistent with the mechanism and not with a blanket “reasoning fixes authoring”:
where the acceptable set is the extension of a rule the model can execute, a scratchpad recovers it
(algorithmic, both models); where the set can only be approximated by enumerated cases, reasoning
shrinks the gap for one frontier model without closing it and does not help the other. One boundary
remains untested: WordNet, where no rule exists at all. Second, it does not touch the downstream
result: the RLVR keys of §5 were authored one-shot, which is how such keys are produced at scale,
and the mitigation of §3.5 is what one needs when they are. The honest summary is that the deficit
is real, mechanistically identified, and escapable, by emitting rules or by paying test-time
reasoning where a rule exists, and that it bites exactly when a pipeline does neither.

3.8    The lexical construction and its confound
The lexical (WordNet) construction is the most intuitive but the least trustworthy, and treating it
carefully is what the complete-truth construction lets us do. Its results (Table 11) reproduce the
scissors, but with one number that must not be over-read.
    The suspicious number is authoring precision, which falls with scale (0.153→0.129). Read
naively this says larger models emit more indiscriminate boundaries; but WordNet is incomplete,
so a large model that correctly volunteers a real synonym the lexicon happens to lack is charged a
false positive. Precision here is therefore a lower bound, and its apparent decline is what one expects
if a stronger model proposes more genuine-but-lexicon-absent words. We consequently do not rest
any claim on WordNet precision. The two WordNet signals we do use are both incompleteness-
robust: recall (a missing lemma can only lower it, so the observed rise 0.233→0.581 is a valid
lower bound on how much the knowledge is present) and authoring recall itself. We must retract
a symmetry argument that would be convenient here: a missing lemma does not penalize the two
interfaces equally. If the model volunteers a genuine-but-absent synonym while authoring, it is
scored a false positive; but that same word is rarely queried in the execution arm, whose positives
are drawn from the synset itself, so execution pays no matching penalty unless the word happens to
appear among the hard negatives. The lexical F1 gap can therefore be inflated by incompleteness,
and we do not treat it as an unbiased comparison; we report the lexical arm as descriptive and


                                                      17
let the complete-truth constructions carry the comparative claim. Crucially, the complete-truth
construction (Table 2), where no synonym can be missing, shows the same gap, so the phenomenon
survives removing the confound entirely, and WordNet’s role is corroboration, not proof. This is
also why the “authoring is flat” reading of a WordNet-only study is an artifact: WordNet F1 looks
flat because its confounded precision drags the rising recall back down; on complete truth, where
precision is exact, authoring visibly scales.

3.9    Prompt sensitivity: the gap narrows but does not close
A natural objection is that authoring merely needs a better prompt. We test this directly on
the 14B model with four independently phrased authoring prompts per domain (the default plus
three rewrites; Appendix B), holding the execution arm fixed (Table 12). Prompting does move
authoring quality: code accept-correct ranges 0.29–0.51 and algorithmic authoring F1 0.46–0.57
across prompts, so the effect is not a single unlucky wording. But no prompt closes the gap:
the best code prompt still admits only 50.5% of correct solutions against execution F1 0.742, and
the best algorithmic prompt reaches authoring F1 0.572 against execution 0.761. The scissors is
prompt-sensitive in magnitude and prompt-invariant in direction; a better prompt buys a few points
of authoring, not the boundary.

                                     default   rewrite 1   rewrite 2   rewrite 3   execution (fixed)
        Algorithmic authoring F1      0.475      0.572       0.571       0.460          0.761
          gap vs. execution          +0.286     +0.188      +0.190      +0.301            —
        Code accept-correct           0.289      0.376      0.505        0.387        (F1 0.742)
          canonical acceptance        0.268      0.390      0.470        0.384            —
Table 12: Prompt-sensitivity ablation (Qwen2.5-14B, four authoring prompts per domain, execution arm
held fixed). Prompting shifts authoring quality but does not close the gap in any of the four phrasings: even
the best prompt leaves authoring far below execution in both domains. The asymmetry is not a prompt
artifact.



3.10    Emission-format controls: how much is serialization?
A fair objection to the authoring arm is that free-form listing bundles set construction with serial-
ization: the model must copy tokens, avoid duplicates, and decide when to stop. We hold the task,
items, and gold sets fixed and vary only the emission format (Table 13). L is the paper’s free-list
prompt; J replaces it with a JSON checkbox over every presented word, which removes both the
copying-of-a-subset problem and the stopping decision, since the schema fixes the output’s length
and content; S re-runs L with the presented list permuted.
    Three findings, one of which concedes part of the objection. (i) Format matters, and we were
previously overcharging “emission”. Moving to the checkbox schema raises authoring F1 at every
scale (+0.09/+0.02/+0.13 at 3B/7B/14B), so a real serialization component exists and the App. K
emission term should be read as set-construction plus residual formatting. (ii) But it does not close
the gap. Even in the schema that eliminates copying and stopping, authoring stays far below the
same model’s pointwise execution (0.300 vs. 0.599; 0.364 vs. 0.657; 0.528 vs. 0.761), a remaining
+0.23 to +0.30. (iii) It is not an ordering artifact: permuting the list moves F1 by −0.02 on
average, within the bootstrap intervals. The failure decomposition explains where the small-model
deficit actually lives: at 3B, 42% of emitted tokens are words not in the presented list (hallucinated
copies), against 5% at 7B and 1% at 14B. So a large part of the 3B gap is a copying failure, while
the 14B gap, where copying is essentially clean and the schema still leaves +0.23, is set construction

                                                     18
                                 L free list     J JSON checkbox      S shuffled    Execution
              Model           (paper’s format)    (no copy/stop)        order      (pointwise)
              Qwen2.5-3B       0.207 [.18,.24]     0.300 [.26,.34]      0.210        0.599
              Qwen2.5-7B       0.343 [.31,.38]     0.364 [.33,.40]      0.313        0.657
              Qwen2.5-14B      0.396 [.36,.43]     0.528 [.50,.56]      0.373        0.761
Table 13: Emission-format controls (algorithmic, n=240, 3B–14B; identical items, gold sets, and set-F1;
item bootstraps). J replaces the free list with a JSON checkbox over every presented word, removing token
copying and the stopping decision. It helps at every scale, so part of what App. K charges to emission
is serialisation, but it leaves a +0.23 to +0.30 deficit against the same model’s judging, and shuffling the
presentation order changes little. Caveats: L differs from Table 2 in token budget as well as format, so
J-vs-L is the clean contrast; and J’s parse success is 1.000/0.879/1.000, so the 7B gain is partly schema
non-compliance rather than set construction.


proper. The claim is therefore: the gap is partly serialization at small scale and almost entirely
construction at large scale.

3.11    Intensional control: the deficit is enumeration, not specification
A central question of construct validity: does our authoring arm measure the inability to specify a
correctness boundary, or only the inability to enumerate the set it induces? The two are separable,
and separating them changes what the paper claims. We therefore add a third interface on the same
algorithmic items, gold sets, and scoring. Instead of listing the acceptable words (extensional au-
thoring), the model writes the specification as a Python predicate, def accepts(w), which we then
execute mechanically over the presented list (intensional authoring). Nothing else changes. The
result is unambiguous (Table 14): intensional authoring is near-perfect and scale-insensitive
(F1 = 0.999/0.978/0.999 at 3B/7B/14B, 100% of predicates executable, no runtime failures), far
above the extensional authoring of the identical specification (0.259/0.405/0.475) and above even
pointwise execution (0.599/0.657/0.761). Three consequences, stated carefully. (i) The gap our
other constructions measure is an enumeration/emission deficit, not a knowledge or specifi-
cation deficit: the same 3B model that emits only 26% of the acceptable set can state the rule that
generates it essentially perfectly. This is the mechanism behind the matched-budget decomposition
(App. K), where the residual at 72B is almost entirely the emission term. (ii) It bounds our claim.
We do not show that LLMs cannot author correctness specifications in general; we show they fail
to make an authored artifact’s induced acceptance region match the intended one: extensionally
for answer keys and enumerated rubrics, and intensionally for the test suites that actually require
them. Where a compact intensional form exists and the model is allowed to emit it, authoring is not
the bottleneck. (iii) It makes an existing technique load-bearing for verifier construction. Emitting
a program and delegating execution is the established idea of program-aided prompting [58, 59];
our contribution is not that technique but the measurement that shows it is not an optimization
here but the difference between 0.26 and 0.99, on the specific artifact, the acceptable set, that keys,
rubrics, and suites consist of. The prescription (§7.2) is accordingly: never ask a model to enumerate
an acceptable set it could instead characterize. The catch is that this escape is unavailable exactly
where verification is hardest: no predicate enumerates the synonyms of a gloss, and a test suite,
though intensional in form, is not a restatement of any rule it was given. Where a test suite sits on
this axis. Suite authoring is constrained intensional authoring: it requires two operations at once,
choosing which inputs to check, an extensional selection over the input space, and computing the
expected output for each, which is the intensional part. Either can fail, and our data say which
does. Of 164 one-shot 14B suites, 115 (70%) execute correctly and reject the canonical solution on


                                                    19
                               Intensional authoring      Extensional authoring      Execution
            Model            (write predicate) [95% CI]     (enumerate set)         (pointwise)
            Qwen2.5-3B           0.999 [.998,1.00]                 0.259               0.599
            Qwen2.5-7B           0.978 [.971,.984]                 0.405               0.657
            Qwen2.5-14B          0.999 [.998,1.00]                 0.475               0.761
Table 14: The deficit is enumeration, not specification (algorithmic, identical items, gold sets, and set-
F1; n=240; 3B–14B, where the effect is already saturated). Asked to write the predicate rather than
list its extension, every model is near-perfect and every generated predicate executes, above both its own
extensional authoring and its own pointwise judging. This bounds the paper’s claim to exhaustive acceptable-
set construction and motivates the prescription of §7.2.


an assertion, while only 15 (9%) crash; among rejection events from broken suites, 87.5% are asser-
tion failures against 11.3% runtime errors (§3.4). The dominant failure is therefore the intensional
component, computing what the program should return, not the extensional one. This is also why
the near-perfect predicate result and the poor suite result are consistent rather than contradictory:
in §3.11 the rule to be expressed was supplied in the prompt and the model only had to restate
it, whereas a suite author must derive the expected behaviour from prose and examples. It is the
derivation, not the act of writing a predicate, that these models fail at.

3.12    Alignment control: the deficit predates instruction tuning
Every model measured so far is instruction-tuned, which admits an alternative reading of the whole
paper: post-training rewards short, decisive answers, so what we call an inability to materialise
the acceptable set might be a learned disposition to stop early. That reading would relocate the
finding from a representational limit to an alignment artifact, and would change the remedy from
externalised verification to a different fine-tuning recipe. It is testable, because a base checkpoint
has never been under that pressure. We therefore run the algorithmic construction on Qwen2.5-7B
and Qwen2.5-7B-Instruct at one scale. A base model has no chat template, so both arms receive the
identical 3-shot plain-text prompt, the controlled comparison, and the instruct model is additionally
run through its own template to show what the template is worth. Membership is computed by
the predicate throughout. The alternative reading does not survive (Table 15). Under the matched
prompt the base and instruct checkpoints author the set equally well (0.384 vs. 0.382), and both
retain a judging advantage (+0.14 and +0.12). Alignment is not the source of the deficit. The
mechanism evidence is sharper than the headline. If post-training had taught brevity, the never-
aligned checkpoint should emit more of the set; instead it emits more than the set, 8.50 words
against a gold mean of 4.89, a 74% over-emission, and converts none of that surplus into accuracy.
The base model is not withholding candidates; it is naming the wrong ones. Nor does the alignment
stack hurt: the instruct model under its own chat template is the best authoring arm of the three
(0.417) and has the smallest gap, the opposite of what the artifact hypothesis predicts. Two caveats.
First, the plain-text harness is weaker than the paper’s main prompt for both arms (execution here
is 0.50–0.52 against 0.657 for the same model in Table 13), so the absolute gaps in this table are
compressed and should not be compared to the headline; the load-bearing quantity is the base-
vs-instruct contrast at a matched harness. Second, the base checkpoint frequently continues the
few-shot pattern, fabricating further List:/Rule: blocks after its answer; we cut each completion
at the first such marker, which is what keeps the fabricated blocks from inflating its score. Scoring
only the first output line instead, which is correct for the base model but unfair to a chat model
that opens with a preamble, leaves the base-vs-instruct comparison unchanged (0.384 vs. 0.374)
and depresses only the chat-template arm, an artifact of the parser rather than of the model. Both

                                                     20
                                                  Authoring    Execution              Mean emitted
         Checkpoint                 Prompt           F1           F1          Gap       set size
         Qwen2.5-7B (base)        plain 3-shot      0.384        0.521      +0.138         8.50
         Qwen2.5-7B-Instruct      plain 3-shot      0.382        0.499      +0.117         6.78
         Qwen2.5-7B-Instruct     chat template      0.417        0.516      +0.100         5.49
Table 15: The authoring deficit is not an instruction-tuning artifact (algorithmic construction, n=240,
identical items, gold sets, and set-F1; gold sets average 4.89 words). Rows 1–2 are the controlled comparison:
one prompt, two checkpoints of the same family and scale, one of which has never been post-trained. They
author the acceptable set equally well and both judge better than they author. The brevity hypothesis
predicts the base model would emit more of the set; it emits 74% more than the set and is no more accurate,
so its errors are commission rather than truncation. Absolute values are compressed relative to Table 13
because the plain-text harness required to make a base model comparable is weaker for both arms; the
contrast, not the magnitude, is the result.


parsers are reported in the released receipt.

3.13    What does not explain it
Knowledge coverage cannot explain the gap at fixed scale, since both interfaces draw on the same
weights over the same items, and enumerating capability itself rises with scale while judging stays
ahead. Prompt format is bounded by the algorithmic construction, whose predicate is simple
enough that no knowledge or format gap remains to blame. Candidate access and compute. The
complete-truth constructions present the candidate list to both arms, so the classical free-recall-
versus-recognition asymmetry is controlled by design. With candidates given and the assembly
floor at zero, App. K still finds a 0.24–0.26 gap at every scale, and the decomposition is scale-
revealing: the batching term vanishes by 72B while the emission term grows to 0.231. Because the
residual grows with scale it is not the length-driven enumeration failure of Vinyals et al. [37], Welleck
et al. [39], Hou et al. [61]. Sampling budget does not explain it either, as 16× authoring samples
raise union recall only to ≈0.80; reasoning budget partly does (§3.7), so this claim is scoped to
sampling at fixed decoding rather than to test-time compute in general. Part of the emission term
is serialisation rather than set construction (§3.10). Finally, enumeration-without-lookahead and
retrieval limits are separated by the repair arm (§4.4), which finds both bind: sampled unions
reach at most 55% of the oracle set, and membership adjudication fails to restore precision on
self-generated candidates. Alignment is ruled out at one scale by §3.12: a never-post-trained base
checkpoint authors no better than its instruct sibling under a matched prompt, and over-emits
rather than truncates, so the deficit is not a learned disposition toward brevity.


4    Why Local Review Is Asymmetric: Witness-Poor Omissions and
     Failed Self-Repair
An authored specification can be wrong in two directions: it can include an invalid member or omit a
valid one. The two are not symmetric to any reviewer, human or model, because review interrogates
tokens that exist. An included error is present and can be challenged; an omitted member is an
absence, and recovering it requires re-enumerating the open set, the operation §3 shows models
perform poorly. The asymmetry is a reduction, not an accident (Figure 7).

Observation 2 (Omission is witness-blind to local review). Grant a local reviewer even a perfect
membership oracle m(x) = ⊮[x ∈ S ∗ ], queryable only on candidates it can name, with a query budget

                                                     21
                 authored key Ŝ (tokens that exist)
                                                              review queries
                                                                                   over-inclusion
              valid     valid      valid    over-incl.        m̂(x) on each
                                                                                    detected ✓
                                                               named token


                 oracle S ∗ has a member not in Ŝ
                                                                                    omission
                                                                 no token
                                omitted                                            undetected
                                                              exists to query
                                                                                       ×
Figure 7: Why omission is witness-poor (Observation 2). Review interrogates the tokens the artifact names,
so an over-inclusion is exposed by a single membership query (top). An omitted member names no token; to
query it the reviewer must first author it, the capability under audit (bottom). Subtractive review therefore
removes over-inclusions and keeps omissions.


smaller than |V \ Ŝ| and no cardinality or coverage certificate for S ∗ . Then (i) every over-inclusion
x ∈ Ŝ \ S ∗ is a named token, exposed by one query m(x) = 0; but (ii) there exist two oracle sets
S1∗ , S2∗ with S1∗ ∩ Ŝ = S2∗ ∩ Ŝ and S1∗ \ Ŝ ̸= S2∗ \ Ŝ on which, unless the reviewer happens to name an
element of (S1∗ △S2∗ ) \ Ŝ, its observations coincide, so it cannot certify recall completeness. Locating
a specific omission requires producing a witness x ∈ S ∗ \ Ŝ, an out-of-set search that is itself an
instance of authoring. Stated with a perfect oracle the result is strongest: even an ideal judge cannot
help, and the model’s approximate judge only makes over-inclusion detection imperfect too, never
improving the omission side.

Three boundaries sharpen the claim rather than weaken it. First, Observation 2 is an information-
theoretic indistinguishability statement, not an LLM-specific mechanism: no procedure, human or
machine, can certify recall of an unknown set under a sub-universe query budget without a coverage
certificate. It therefore licenses “omission cannot be certified absent”, not “omission cannot be no-
ticed”. Our own data make that distinction concrete: reviewers do volunteer out-of-set candidates,
and at 72B they flood (5.46 spurious additions per item, Table 16), so a reviewer is plainly not
confined to named tokens. What we show empirically is the weaker, sufficient claim that subtrac-
tive review removes over-inclusions while generative review does not recover omissions at usable
precision. Second, a cardinality or coverage certificate lets a reviewer detect incompleteness with-
out a witness, but detection is not repair: fixing the gap still needs the missing witness, and such
certificates are unavailable precisely when the acceptable set is the unknown being authored. Third,
a reviewer that volunteers candidates may inject fresh errors. The net effect is a directional blind
spot, so any subtractive review loop pushes an authored set toward under-acceptance. The rest of
this section measures that asymmetry.

4.1    Design
For each of the 240 constructed items we present the model with a proposed answer key for the same
gloss/example task under three conditions: clean (the exact oracle set), over-corrupted (oracle set
plus two hard negatives), and omission-corrupted (oracle set minus two valid members), instructing
it to critique and repair the key in a fixed format (REMOVE: . . . / ADD: . . . ). Detection is scored
objectively: an injected negative counts as caught iff it is named in REMOVE; a deleted member
counts as recovered iff it is named in ADD. Clean items measure false-alarm rates.




                                                         22
                                 Detection rate                        False alarms / clean item
            Model           over-inclusion   omission      Asymmetry   REMOVE          ADD
            Qwen2.5-7B          0.706         0.100          7.1×       2.06          1.10
            Qwen2.5-14B         0.860         0.148          5.8×       1.83          1.18
            Qwen2.5-72B         0.860         0.375          2.3×       1.09          5.46
Table 16: Silent omission (WordNet, n=240 per condition). Reviewers see a drafted key and may add
or remove entries. Planted over-inclusions are caught 71–86% of the time, planted omissions only 10–15%,
a 6–7× asymmetry that holds at every scale. The 72B model narrows it only by flooding the key with
unsupported additions, which trades one error direction for the other rather than repairing recall. The 6–7×
figure is measured under the weakest review condition: one model, no auxiliary information; showing the full
candidate pool and using a frontier reviewer changes the raw ratio but not the direction once clean-key false
alarms are netted out (Table 17), and further enriched conditions (§7.3) may shrink it, and Observation 2
bounds only what local review can certify, not what a better-resourced reviewer could find.


4.2    Results
Table 16 confirms the prediction with a 6–7× asymmetry at 7–14B. Three further observations
sharpen it. It is not reluctance to add: on clean keys the models volunteer ≈1.1 additions per
item (false alarms against the oracle); when two members are genuinely missing they recover them
only 10–15% of the time, the model is willing to extend the set but cannot find the specific absent
members, blind search in an open space. Scale improves the presence side first: the 7B→14B
gain concentrates on catching what is written (+15.4 vs. +4.8 points). At 72B the asymmetry
converts rather than closes: the ratio drops to 2.3×, but the mechanism is flooding, not finding:
false-alarm additions on clean specifications roughly quintuple (4.6–5×; 1.1→5.46 per item) while
genuine recovery reaches only 0.375. A reviewer that “fixes” omissions by indiscriminate addition
has traded the silent error for the visible one, the recall-for-precision trade of §3; no scale we tested
yields a reviewer that locates the specific missing members.

Is the asymmetry lexical-specific? A complete-truth replication. The measurement above
uses the lexical construction, whose acceptable set is fuzzy: a reviewer hunting a missing synonym
must also decide whether the missing word really carries the intended sense. The asymmetry could
therefore be an artifact of that fuzziness rather than a property of omission. We close that escape
by re-running the identical review protocol on the algorithmic construction, where the reviewer is
shown the full 15-word candidate list and a mechanically decidable predicate, so every membership
question has a checkable answer and finding an omission requires only scanning the list. Both
constructions are run with one frontier reviewer (GPT-5.1) in the same session, so construction is
the only variable (Table 17).
    Two things follow, and the second reverses the first. Raw detection rates make the frontier
reviewer look far more symmetric than the 7–14B models (1.4–1.5× rather than 6–7×), and equally
so on both constructions. But those raw rates are not corrected for what the reviewer does to a
clean key, and it does a great deal: it volunteers additions on 64% of clean algorithmic keys and 83%
of clean lexical ones. Net of that base rate the picture inverts. On the algorithmic construction the
reviewer gains +0.28 over chance at catching planted over-inclusions but only +0.04 at recovering
planted omissions, a ratio of roughly seven; on the lexical construction the omission figure is negative
(−0.26), meaning it proposes additions more readily on keys that need none than it recovers members
that are genuinely absent. The asymmetry is therefore construct-general. It survives on complete
truth, where lexical fuzziness cannot explain it, and the frontier reviewer’s apparent improvement


                                                      23
                              Raw detection      Clean-key false alarm
      Construction            Dover     Domit    Frem          Fadd             Adjusted [95% CI]
                                                                          dover = +0.303 [+.215, +.395]
      Algorithmic (n=114)      0.943    0.636    0.640        0.544
                                                                          domit = +0.092 [−.013, +.197]
                                                                          dover = +0.204 [+.133, +.273]
      Lexical (n=240)          0.858    0.569    0.654        0.842
                                                                          domit = −0.273 [−.337, −.208]
Table 17: The detectability asymmetry replicated across constructions with one reviewer (GPT-5.1), so
construction is the only variable. Raw rates suggest near-symmetry, but the reviewer volunteers removals
on 64–65% and additions on 54–84% of clean keys, so a raw rate is mostly base rate. D is the detection
rate for the planted error, F the rate at which the reviewer volunteers the same edit on an uncorrupted key.
We therefore report the false-alarm-adjusted quantities dover = Dover − Frem and domit = Domit − Fadd , the
hit-minus-false-alarm statistic of signal-detection theory, with the clean condition supplying the false-alarm
rate, each with a 2,000-resample item bootstrap. Reading the intervals rather than a ratio: over-inclusion
detection is reliably above its own false-alarm floor on both constructions, whereas omission detection is
indistinguishable from its floor on complete truth (the interval covers zero) and significantly below it on
WordNet, where the reviewer adds spurious members faster than it recovers real ones. We deliberately do
not lead with the over/omit ratio: its denominator’s interval spans zero, so the ratio is unstable even though
the ordering is not. The asymmetry is thus not an artifact of lexical fuzziness. Item counts differ because the
algorithmic construction requires at least four accepted words per list, which its candidate pool supplies for
114 of the 240 attempted lists. These figures come from a re-run that retains per-item vectors so the intervals
could be computed; an earlier run of the identical protocol gave the same ordering with somewhat different
magnitudes (dover =+0.276, domit =+0.039 algorithmic), which is run-to-run variation of the reviewer model,
not of the construction.


is the same flooding we already observed at 72B, now at the top of the capability range. What
changes with capability is the willingness to add, not the ability to find what is missing. Stated
at the strength the intervals support: on complete truth this reviewer detects over-inclusions well
above its own false-alarm rate and detects omissions at a rate we cannot distinguish from that rate.

4.3    Consequence: subtractive review shifts error toward omission
The asymmetry converts review pipelines from quality filters into directional filters. Any authored
specification passed through self-critique, cross-model review, or adversarial revision will prefer-
entially shed over-inclusions (visible, challengeable) while retaining omissions (invisible), so the
surviving artifact is systematically under-accepting, and the process that was meant to certify it is
the process that skewed it. This is a Goodhart mechanism one level above reward hacking: not a
policy exploiting a reward, but the reward being born wrong in a direction its own audit cannot
see. Formally, a subtractive review round maps Ŝt 7→ Ŝt+1 = Ŝt \ Dt , where by Observation 2 the
detected set Dt ⊆ OI(Ŝt ) = Ŝt \ S ∗ contains only over-inclusions (the sole errors it can name and
challenge). Consequently

                     πt+1 ≥ πt ,       ρt+1 = ρt ,       OM(Ŝt+1 ) = OM(Ŝt ) = S ∗ \ Ŝt ,               (4)

so the omitted mass is a fixed point of review: iteration walks the artifact monotonically down-and-
right on the precision–recall plane, sharpening precision while never recovering a missing member.
Section 6 shows this signature verbatim in a production system whose generation pipeline included
exactly such an adversarial review stage: over-inclusions falling round-over-round while omissions
persist, exactly Eq. (4).


                                                         24
           spec           sample K=10              union                      membership
        (open set)                               U = j Ŝ (j)
                                                    S
                                                                               filter m̂(·)             Ŝrep
                            at T =0.9


                                                 retrieval bind:            filter collapses on
                                                   RU ≤ 0.55               self-gen. candidates

Figure 8: Sample-then-verify authoring (§4.4) and its two failure points. Diversity sampling supplies recall
and the model’s stronger membership interface supplies precision, in principle. In practice the union misses
nearly half of S ∗ (retrieval bind) and the filter, strong on curated contrasts, collapses on the model’s own
near-boundary proposals; by Eq. (5) the composed F1 cannot beat one-shot.

                                One-shot          Union (K=10, T =0.9)               Sample-then-verify
           Model              F1      (P /R)        P               R                P            R    F1
           Qwen2.5-3B       0.169    (.13/.28)    0.072            0.425           0.121      0.188   0.126
           Qwen2.5-7B       0.229    (.19/.34)    0.100            0.548           0.161      0.491   0.210
           Qwen2.5-14B      0.192    (.14/.40)    0.057            0.521           0.167      0.393   0.207
           Qwen2.5-72B      0.168    (.12/.42)    0.045            0.490           0.094      0.442   0.143
Table 18: Sample-then-verify repair (algorithmic, K=10 at T =0.9, then self-filtered by membership). The
registered prediction that self-verification closes the gap is falsified: repaired F1 does not beat one-shot
authoring at any scale. Union recall saturates near half the gold set, and the membership judge degrades on
the very self-generated near-boundary candidates it must filter. Precision/recall of the one-shot baseline are
given for reference.


4.4    Failed self-repair: sample-then-verify authoring
If the scissors of §3 are a property of the one-shot generation interface (enumeration without looka-
head, uncalibrated stopping) rather than of the model’s knowledge, then the model’s own execution
ability should repair its authoring. We re-architect authoring as sample-then-verify: (1) sample
the open-set task K=10 times at temperature 0.9 and take the union of normalized candidates
(recall via diversity, the pass@k logic); (2) present each candidate to the same model as a closed-set
membership query (precision via execution, the interface it is good at); (3) the authored specifica-
tion is the accepted subset (Figure 8; full incident log in Appendix J). No external knowledge, no
other model, no oracle access: the same weights, differently interfaced.
     Registered predictions: if the asymmetry is interface-bound, repaired F1 substantially exceeds
one-shot F1 at every scale, with precision recovered by filtering; if the union’s recall stays low,
retrieval binds; if filtering fails to restore precision, the
                                                           S boundary       itself is diffusely represented.
     The pipeline has a hard ceiling. Writing U = K           j=1 Ŝ (j) for the sampled union with oracle

recall RU = |U ∩ S ∗ |/|S ∗ |, and πf for the precision of the membership filter on U , the repaired set
Ŝrep = {x ∈ U : m̂(x) = 1} satisfies
                                               2 RU πf
                                   F1rep ≤             ≤ 2 min(RU , πf ),                                       (5)
                                               RU + πf
because its recall cannot exceed the union’s (RU ) and its precision cannot exceed the filter’s (πf ).
Repair therefore needs both factors high; the experiment finds both low (RU ≤ 0.55; πf near
one-shot precision), which Eq. (5) converts into the falsification below.

Result: the prediction is falsified, and the falsification is informative. Table 18: re-
paired F1 (0.126/0.210/0.207/0.143) shows no consistent improvement over one-shot authoring
(0.169/0.229/0.192/0.168): it is lower at 3 of 4 scales and essentially tied at 14B (0.207 vs. 0.192,

                                                        25
overlapping intervals), so sample-then-verify does not close the scissors. The failure decomposes
into two binding constraints. Retrieval binds: even ten diverse samples surface at most 55% of
the acceptable set, the missing members of §4 are not hiding in the sampling distribution. The
judge collapses off-distribution: membership execution, strong on oracle members versus curated
negatives (membership F1 0.60–0.79 for 7B–72B, Table 11), filters the self-generated candidate pool
barely above chance because a model’s own high-temperature proposals are concentrated exactly
at the boundary where its calibration is worst [17, 44]. The strong-interface hypothesis is dead:
the scissors are not an artifact of the one-shot prompt that a generation+execution decomposition
repairs. What survives is the stronger structural reading: the acceptable-set boundary is not
sharply represented in the weights under any interface we tested: one-shot emission, high-
temperature exploration, and pointwise self-adjudication all fail on it, each in its characteristic way.
Practically, this closes the escape hatch a skeptic (or a practitioner) would reach for first: authored
specifications cannot be made trustworthy by asking the same model to check itself; external ground
truth is not an optimization but a requirement.


5    Propagation: Authored Keys as RLVR Rewards
The silent-omission mechanism matters most where authored specifications are consumed automat-
ically: as reward functions. RLVR theory treats verifier false negatives as a noise parameter [3],
and case studies of falsely-rejecting verifiers uniformly project that, used as rewards, they would
penalize correct outputs [7, 16]. We execute that projection twice: once on the lexical task (large
effect, but scored against WordNet, an admittedly incomplete reference; see the caveat below) and
once on a complete-truth numeric task where the acceptable set is decidable by construction and no
incompleteness is possible (§5.1). The complete-truth run is the clean causal estimate; the lexical
run is the larger but reference-relative one. First, what the authoring gap does to a reward is not
one-sided noise but a specific two-sided channel.

Observation 3 (The authored reward is a two-sided channel). Let the oracle set be S ∗ and the
authored key Ŝ. Under the reward R(x) = ⊮[x ∈ Ŝ] (vs. oracle R∗ (x) = ⊮[x ∈ S ∗ ]), the two disagree
exactly on Ŝ△S ∗ : outputs in S ∗ \ Ŝ get zero reward ( starvation) and outputs in Ŝ \ S ∗ get positive
reward ( pollution). Two distortion measures follow, and it is important not to conflate them. The
set-level rates are 1 − ρ (fraction of S ∗ starved) and 1 − π (fraction of Ŝ that pollutes), with ρ, π the
key’s recall and precision. The policy-experienced rates are the masses the policy actually places
there, ϵstarve = Prx∼qθ [x ∈ S ∗ \ Ŝ] and ϵpollute = Prx∼qθ [x ∈ Ŝ \ S ∗ ]; these coincide with the set-
level rates only in degenerate cases (a policy uniform on the relevant set) and in general differ; the
policy-experienced rates are what enter the RLVR gradient. The empirical “reward pollution” we
report (Table 19, 0.179) is the conditional rate Prqθ [x ∈   / S ∗ | x ∈ Ŝ], the policy-weighted analog
of 1 − π, and the directly measurable “fraction of rewarded rollouts that are wrong”, which differs
from the unconditional mass ϵpollute by the factor qθ (Ŝ). In either case R is blind in both directions
at once, and no on-policy optimization against R can distinguish its errors from the oracle intent,
because R is the loop’s only definition of correct.

The proposition dictates the measurements we report: set-level, the authored key has recall ρ =
0.507 (so 1 − ρ = 0.493 starved) and low precision; policy-level, we measure ϵpollute directly on
trained-policy rollouts (0.179 under the authored key vs. 0.041 under the oracle key, §5). Reporting
the policy-weighted mass, not just 1 − ρ, 1 − π, is what ties the identity to the observed training
damage.



                                                    26
                                                  policy update


                                           (oracle key R∗ = ⊮[x ∈ S ∗ ]: no leaks ⇒ +18.5 pts)

                                                              reward key
                                                                                              GRPO
                policy πϕ           rollouts x                  R(x) =
                                                                                             gradient
                                                               ⊮[x ∈ Ŝ]


                                                x ∈ S ∗ \ Ŝ:              x ∈ Ŝ \S ∗ :
                                     reward 0 (starvation, 1−ρ=.49) reward 1 (pollution, .18)

Figure 9: Propagation as a two-sided reward channel (Observation 3). An RLVR loop identical except for
the reward key: the authored key withholds reward from correct rollouts in S ∗ \ Ŝ and grants it to incorrect
rollouts in Ŝ \ S ∗ . The reference key has neither leak. On complete truth the two arms end 1.9 points apart;
on the lexical task 18.5 points apart in synset-membership accuracy.


Design. Task: given gloss and example, produce one word meaning g (single-token-style rollouts,
so RL is cheap and attribution clean). Dataset: 2,400 WordNet items (train 2,040 / eval 360) built
as in §3.2. The 14B model authors an answer key per item (one-shot, greedy); measured against the
reference synsets these keys have recall 0.507, and 2,157/2,400 items carry at least one omitted
valid answer, the raw material of silent punishment.

What the lexical “oracle” is, and is not. Both arms here are scored by membership in the
WordNet synset, which §3.8 establishes is incomplete. Three consequences follow. (i) The evaluation
metric is a reference-relative quantity, synset-membership rate rather than semantic correctness; we
name it accordingly below and reserve “true accuracy” for the complete-truth run. (ii) Measured
pollution is an upper bound : a genuine, context-appropriate synonym that WordNet omits is counted
as pollution. (iii) Most importantly, the reference-key arm enjoys a criterion-alignment advantage:
it is trained on the same membership predicate used to score it, while the authored arm is trained
on a proper subset of that predicate. This experiment therefore establishes that training on a key
that disagrees with the evaluation criterion costs performance on that criterion; it does not by itself
establish an equally large loss in semantic correctness. We must be careful about how far this can
be bounded. Writing a and r for the fraction of each arm’s off-synset outputs that are genuinely
correct, semantic accuracy is 0.722 + 0.278a (authored) versus 0.913 + 0.087r (reference). The
measured gap survives for any plausible configuration; e.g. it persists even at a = 0.7, r = 0.1, but
it is not mathematically excluded that the ordering reverses in the extreme (a → 1, r → 0 gives 1.000
vs. 0.913). Without human adjudication of off-synset answers we therefore cannot claim a one-sided
bound, only that reversal requires the authored arm’s off-reference outputs to be almost entirely
valid while the reference arm’s are almost entirely invalid. The complete-truth replication in §5.1,
where the acceptable set is exact and no such caveat applies, is what licenses the causal reading.
The authored key is wrong in both directions at once: evaluated over the base policy’s own rollouts
it is not only starved but polluted : of every answer it pays reward for, 25.8% are oracle-invalid (a
dedicated base-policy evaluation; the multiseed base arm gives 0.264, Table 19), so the training
signal simultaneously withholds reward from correct behavior and grants it to incorrect behavior.
Two GRPO [32] arms on a Qwen2.5-3B policy, identical in everything except the reward: authored-
key arm, reward = membership of the rollout in the authored key; oracle-key arm, reward =
membership in the full synset. Instrumented against the oracle throughout: per-step frequency
of correct-but-omitted answers (rollouts the oracle accepts but the authored key rejects), reward
pollution (rollouts the authored key rewards but the oracle rejects), oracle-valid rate, and distinct-


                                                        27
     Arm (reward key) Synset-membership Reward pollution Omitted frac. of valid Distinct valid / item
     base (no training)                                0.567                     0.264                                             0.112                     1.064
     authored key                                   0.726 ±.026               0.179 ±.019                                       0.121 ±.008               1.032 ±.015
     oracle key                                     0.911 ±.003               0.041 ±.002                                       0.156 ±.001               0.970 ±.004

Table 19: E6 lexical arm (mean±std, 6 seeds): identical GRPO runs differing only in the reward key,
evaluated by WordNet synset membership. This is a reference-relative metric, not semantic correctness, and
the reference arm is additionally criterion-aligned (§5); the complete-truth estimate is in §5.1. Training on
the authored key forfeits 18.5 points relative to the reference key, in every one of six seeds. Reward pollution
shows the two-sided damage. Both trained arms are less diverse than the untrained base (1.064 → 1.032 and
0.970), the ordinary diversity collapse of RL fine-tuning; the reference key collapses it slightly more, which
is what a sharper reward should do and is not evidence about key quality. The registered sub-predictions on
omission suppression and diversity narrowing are not confirmed: at the K=32 sampling budget of App. G the
authored arm is in fact more diverse than the reference arm, the opposite of the prediction, and the diversity
column is budget-dependent (it counts distinct valid answers among K samples) so it is not comparable
across K.

                                       Policy synset-membership (WordNet-relative)                                                     Reward pollution

                                 1.0
                                                                             91.3
                                                                                                                       0.30
                                                                                      Reward pollution (of rewarded)          0.27
                                                                      −19.1 pts
                                 0.8
        Synset-membership rate




                                                          72.2                                                         0.25

                                                                                                                                                0.18
                                 0.6    56.5                                                                           0.20


                                                                                                                       0.15
                                 0.4

                                                                                                                       0.10

                                 0.2
                                                                                                                       0.05                                   0.04



                                 0.0                                                                                   0.00
                                        base            authored            oracle                                            base            authored       oracle
                                                          key                key                                                                key           key


Figure 10: E6 propagation (mean±std over 6 seeds; dots are per-seed values). Left: synset-membership
accuracy (WordNet-relative). Wiring the model-authored key into an otherwise-identical loop costs 18.5
points relative to the reference key. Right: reward pollution (fraction of rewarded rollouts the oracle rejects).
The oracle key drives the trained policy to 0.04, the authored key leaves it at 0.18: the authored reward not
only starves correct behavior (recall 0.507) but teaches the policy to emit oracle-invalid answers it happens
to accept.


valid coverage (how many different correct answers the policy can still produce at evaluation).
    Registered predictions: the authored-key arm suppresses correct-but-omitted answers and nar-
rows distinct-valid coverage relative to the oracle arm; oracle-valid rate may remain superficially
comparable.

Result: a 19-point WordNet-relative tax, unobservable in-loop. Table 19 and Figure 10:
with everything held fixed except which key pays the reward, the reference-key arm reaches 91.3%
synset-membership accuracy while the authored-key arm stops at 72.2% (mean over 3 seeds; the
effect is robust, the best authored seed, 0.758, lies below the worst oracle seed, 0.910; per-seed
values in Appendix H). The mechanism is the one the measured key predicts, and it is two-sided.
The authored key omits 1 − ρ = 0.49 of the synset lemma types, but the policy concentrates its
correct rollouts on common in-key words, so the policy-experienced starvation is milder: about 12%
of its correct rollouts go unrewarded (Table 19, omitted-fraction-of-valid). Meanwhile 25.8% of the


                                                                                     28
               Policy          Axis      Base   Authored key     Oracle key    Tax (pts)
               Qwen2.5-3B      anchor   0.567     0.726 ±.026    0.911 ±.003     −18.5
               Qwen2.5-7B      scale    0.562     0.695 ±.018    0.929 ±.003     −23.3
               Qwen2.5-14B     scale    0.566     0.612 ±.007    0.932 ±.012     −32.0
               Qwen2.5-72B     scale    0.740     0.701 ±.020    0.966 ±.001     −26.6
               Phi-3.5-mini    family   0.451     0.637 ±.038    0.919 ±.004     −28.2
Table 20: E6 across scale and family (lexical arm: synset-membership accuracy, WordNet-relative;
mean±std, 3 seeds; base is the untrained policy). Each row is an independent pair of GRPO runs dif-
fering only in the reward key. The reference arm reaches 0.91–0.97 at every scale while the authored arm
never exceeds 0.72, a 19–32 point gap over a 24× parameter range and a different family. The tax is not
monotonic: it peaks near 14B and is smaller at 72B, whose stronger base lifts both arms.


rollouts that are rewarded are oracle-invalid (pollution), so the damage is pollution-dominated and
the authored arm trains on a signal that is both false-negative- and false-positive-noisy, the regime
whose convergence cost RLVR theory anticipates [3]. The pollution side leaves a fingerprint in
the trained policies: training on the oracle key drives the policy’s own reward pollution down to
0.041, whereas the authored key halves the base rate only to 0.179 (base 0.264): it fails to purge
the false-positive channel that the oracle key eliminates, leaving the trained policy nearly 5× more
polluted than under the oracle key. Two honest notes. First, the sharper registered predictions
were not confirmed at this budget: one LoRA epoch does not actively drive omitted-but-correct
answers toward zero (they stay flat or rise) or collapse diversity; whether longer horizons produce
that distributional damage remains open. Second, the 18.5-point gap is precisely the quantity the
authored arm cannot observe from inside: by its own key’s accounting it improved substantially,
and nothing in its loop distinguishes “the policy is wrong” from “the key is missing the answer.”
The cost of authoring is thus paid in capability and booked nowhere.

The tax persists at every scale, but does not grow without bound. The 18.5-point result
is a single policy (Qwen2.5-3B); a natural hope is that a stronger base model escapes a weak key’s
flaws. It does not. We replicate the identical two-arm protocol (3 seeds each; same data, steps,
and hyperparameters; same authored and oracle keys) across scale (Qwen2.5-7B and -14B) and
across family (Phi-3.5-mini, a different lab’s model) (Table 20, Figure 11). The tax does not close
at any scale tested: the reference-key arm reaches 0.91–0.97 synset-membership accuracy while the
authored-key arm never exceeds 0.72, leaving a 19–32 point gap across a 24× parameter range, and
−28.2 points for the different family. (These are lexical runs, so they inherit the reference-relative
caveat above; the complete-truth estimate is in §5.1.) But it is not monotonic in scale: it rises from
3B to a peak at 14B (−32.0) then falls to −26.6 at 72B, whose much stronger base policy (0.740 vs.
≈0.56 for 3B–14B) lifts both arms (oracle 0.966) yet still forfeits 27 points. Reward pollution tracks
the same shape: authored-key pollution 0.18/0.24/0.34/0.27 at 3B/7B/14B/72B, peaking at 14B,
against oracle pollution ≤0.04 throughout, so a more capable policy optimizes harder onto what the
key pays for (pollution included) up to mid scale, while the largest model’s stronger prior pulls it
partway back. (An OLS fit of the tax on log10 parameters is positive but weak, slope 5.5 pt/decade,
R2 =0.29, but with only four scale points we report it as exploratory and draw no scaling law from
it.) the robustly supported claim is persistence, not monotone growth: there is no scale we test at
which training on a model-authored key matches training on the oracle. Capability raises absolute
accuracy but does not repair the authored-key tax.




                                                  29
                                       1.0
                                                                 scale (same family)                                 family




          Synset-membership accuracy
                                                −19.1         −23.3                                    −26.6
                                       0.8                                             −32.0                           −28.2



              (WordNet-relative)       0.6



                                       0.4



                                       0.2



                                       0.0
                                             Qwen2.5       Qwen2.5              Qwen2.5             Qwen2.5          Phi-3.5
                                               3B             7B                  14B                 72B             mini
                                                        base (no RL)        authored-key arm       oracle-key arm


Figure 11: The authoring tax persists across scale but is not monotonic. Base, authored-key, and reference-
key synset-membership accuracy (WordNet-relative, ±std over 3 seeds) for five policies spanning scale and
family. The reference arm reaches 0.91–0.97 at every scale while the authored arm never exceeds 0.72, so
the gap stays in a 19–32 point band. It peaks at 14B rather than growing without bound.


5.1    Complete-truth replication: the clean causal estimate
The lexical run above is reference-relative. We therefore repeat the identical two-arm protocol on a
numeric construction, where the acceptable set is computed by a mechanical predicate, so the oracle
is exact: “true accuracy” is literally true, nothing can be missing, and the reference arm’s criterion
is ground truth rather than a proxy. Because finiteness is essential here we state the task fully (full
specification in App. L): the candidate universe is the bounded set V = {1, . . . , 100} and every
predicate is range-scoped, e.g. “between 20 and 80 that is divisible by 3 or by 5”, “between 1 and
100 whose two digits differ by exactly 2”, so each acceptable set is finite (mean |S ∗ | = 10.3, range
4–29). Note these are compound, range-bounded predicates, not the four unbounded predicates
used for the numeric scissors of §3.2. The policy is asked for one number satisfying the predicate;
the reward is set membership in the arm’s key. Train and evaluation predicates are disjoint (100
train, 60 held-out, zero overlap), so nothing is memorisable across the split. Measured on the
held-out predicates the 14B-authored key has recall 0.926 and precision 0.987, far more accurate
than its lexical counterpart (0.507), which is why the resulting tax is much smaller. We repeat the
two-arm protocol on the numeric construction, the same open-set generative task (“give a whole
number that P ”) but with mechanically decidable predicates, so the oracle is complete truth and
the 14B-authored key is scored against it exactly (100 predicates, 6 seeds). Here authoring is far
more accurate than on synonyms, and the downstream tax shrinks in lockstep:

          Downstream task family                                 Authoring recall              Authoring pollution     RLVR tax
          Lexical (WordNet synonyms)                                      0.51                       0.26                  −18.5
          Numeric (arithmetic predicates)                                 0.93                       ≈0.04                 −1.9

The tax appears in both families (all six numeric seeds are positive, +3.0/ + 1.6/ + 0.5/ + 3.2/ +
0.1/ + 3.1; base 0.888 → authored 0.953 → oracle 0.972) but is far larger where authoring is worse
(lexical recall 0.51 → −18.5; numeric recall 0.93 → −1.9). Authoring quality is thus a determinant
of the tax, not the only one. The scale sweep of Table 20 separates the two cleanly, and the design
point is worth stating explicitly because it is easy to misread: every arm in that sweep trains
against one and the same authored key, a single file written once by Qwen2.5-14B, so the key
is a fixed input and the policy is the only thing that varies across 3B, 7B, 14B, 72B and Phi. The tax

                                                                            30
nevertheless moves across that sweep and peaks at 14B, which it could not do if authored-key quality
were the sole driver. The two families also differ in base accuracy (0.90 numeric vs. 0.57 lexical), a
second non-key determinant. We therefore read this as directional evidence, the downstream harm
concentrates where authoring is hardest (fuzzy semantic sets; code suites that admit only 19–44% of
correct solutions, §3.4–3.7) and is mild where the acceptable set is mechanically enumerable, rather
than a precise scaling law. It still unifies the paper’s two halves: the scissors (§3–3.4) measures the
authoring error, and the RLVR tax is what that error costs once the key becomes a reward.

What three seeds can and cannot support. Each arm is a set of paired runs (same seed, same
data, same steps; only the reward key differs), so we report the paired per-seed differences rather than
arm means alone. The two anchor arms were extended to six seeds and re-scored with the precise
evaluation of App. G; the four scale-sweep arms remain at three seeds and their original scoring.
Lexical 3B {21.8, 14.7, 20.3, 15.7, 20.4, 18.1}, complete-truth numeric {3.0, 1.6, 0.5, 3.2, 0.1, 3.1}; 7B
{20.8, 25.1, 24.1}, 14B {31.5, 30.5, 33.8}, 72B {24.1, 26.8, 28.8}, Phi {31.1, 23.4, 30.0} points. First,
the two anchor arms now clear conventional significance and the four scale arms cannot. Both
anchors have all six differences positive, giving an exact two-sided sign-permutation p = 2 · 2−6 =
0.031, with paired dz = 6.5 (lexical, 18.51 ± 2.83 points) and 1.4 (numeric, 1.91 ± 1.40 points).
The four scale-sweep arms are still n=3, where the two-sided minimum attainable p is 0.25, so
no p < 0.05 is available for them by construction and we claim none; their evidence remains the
direction, the non-overlap of seed ranges, and the effect size. Second, precision mattered more than
seed count here. At the original K=8 sampling budget the evaluation’s own binomial standard
error was near 1.0 point per arm, comparable to the entire numeric effect, and under it one numeric
seed appeared to reverse (−0.8). Re-scoring the identical checkpoints at K=32 with three seeded
repeats reduces evaluation noise to 0.18 points and that seed becomes +0.05: the reversal was
measurement noise, not training variation. We report this because it also revises our own earlier
estimates downward (2.29 → 1.91 points, dz 2.4 → 1.4): a large dz at n=3 under a noisy instrument
is not evidence of a large effect, and we had said so before it cost us. Third, we still deliberately do
not rescue the scale arms by aggregating them. All paired runs favour the reference key, but the
arms are not independent trials: the five lexical arms share the same dataset and the same authored
and reference keys, four of them are the same model family differing only in scale, and the numeric
arm is a different task family altogether. A sign test over them would presuppose an inferential unit
we have not established, so we report their consistent direction as descriptive replication


6    Field Evidence at Production Scale
The constructions above are controlled; the phenomenon they isolate was first met in the wild. We
operated a production K–12 assessment deployment of 43,227 scored items across 755 curriculum
standards and ten generator LLMs, in which every fill-in-the-blank item requires an exhaustive
authored answer key and a fixed commercial expert evaluator graded the results. What follows
is a qualitative field signature, not a replication, and the confounds come first. The format
comparison is observational; we stratify on the two covariates the corpus records and the deficit
survives both (App. M): holding difficulty fixed, fill-in trails the closed formats by 2.28/1.29/3.25
points, pooling to −2.27 (Mantel–Haenszel-style, 95% CI [−2.93, −1.61], z = −6.8); holding grade
fixed it is lower in 12/12 grades (p = 2.4 × 10−4 ). Subject, generator model, answer-space size
and prompt length cannot be matched, so residual confounding remains. The error taxonomy is
evaluator-diagnosed by the same grader we show to be 25% self-consistent on open-format failures,
so the 10:1 ratio is directional, not a measured rate. This is the weakest link between the paper


                                                   31
and a real deployment, and we mark it as such: a categorisation produced by an instrument that
reproduces one fail verdict in four cannot be read as a rate, and no adjudication independent
of that grader is reported here. Settling it needs only a small blinded re-check, on the order of
50–100 sampled failures, re-categorised as omission or over-inclusion by raters who never see the
grader’s own label, and the blinded two-rater instrument for exactly this is built and released with
the artifact, so the check is available to anyone who disputes the ratio. Read as corroboration of
direction only:
    (1) Key errors are omission-dominated. Among all 2,586 open-format failures, evaluator-
diagnosed answer-key errors split 316 omissions to 33 over-inclusions (≈10:1), consistent across all
ten generators. (2) The review stage predicts the direction. The pipeline ran an adversarial
self-review over each drafted key, the operation Table 16 characterizes, and it behaved as predicted:
over-inclusion counts fall while omission counts rise round-over-round, error mass sliding along a
precision–recall frontier rather than shrinking. (3) Judging destabilizes at the boundary.
The expert evaluator, re-run on identical items, re-affirms its fail verdicts on open-format items
only 25% of the time (41–42% for closed formats), against 96–99% self-consistency on passes: at
the specification boundary, even the strongest available judge cannot reproduce its own decisions.
Table 21 gives the numbers with Wilson intervals. The fill-in format, the only one requiring an
authored exhaustive key, is both the lowest-passing and the least self-consistent on its failures (0.25
against 0.41–0.42 for closed formats whose acceptable set is enumerated by construction): instability
concentrates where a set must be authored.

    Item format                     Pass rate [95% Wilson]     Fail self-consistency   Pass self-consistency
    fill-in (authored key)            96.48 [95.84, 97.02]             0.25                    0.956
    multiple-choice (enumerated)      99.13 [98.70, 99.42]             0.409                   0.976
    multi-select (enumerated)         98.61 [98.07, 99.01]             0.417                   0.989
Table 21: Production corpus (n=8,873 re-scored items; 43,227 total). The measurement this table exists for
is the self-consistency pair: the fill-in format, the only one whose correctness requires an authored exhaustive
answer key, has the least reproducible fail verdicts, the evaluator re-affirming only 25% of its open-format
rejections against ≥96% of its passes, while the closed formats, whose acceptable set is enumerated by
the item, are far more stable. Judge instability tracks the need to author a set. The pass-rate column
is a descriptive statistic of the shared corpus and is also reported by the companion manuscript; the self-
consistency columns are measured here and appear only here.

    The field and the constructions agree: open-set boundaries are where enumeration fails, where
review is least able to certify, and where judging itself becomes unstable.


7     Discussion
7.1    Related work
Generation–discrimination and verification asymmetry. A large literature contrasts a
model’s ability to generate a solution with its ability to verify one, and the recurring finding runs
the reassuring way: verification is typically easier than generation [18, 34, 41], which underwrites
generate-then-verify and best-of-n pipelines and process-reward supervision [22]. All of it compares
generating a solution with verifying a solution against a given standard. We measure one level
up, where the object being generated is the standard itself. This is not a reversal of that asym-
metry but its meta-level extension: executing a specification is judgment given an object, while
authoring one is generation from scratch, so the familiar recall-versus-recognition gap reappears


                                                      32
on the verifier. The load-bearing consequence is that the verifier advantage does not transfer to
verifier construction: verification is cheap only after the specification exists, and the weakness of
construction is then baked into the artifact that defines correctness downstream.

Model-generated specifications, rubrics, and verifiers. The closest work observes the same
construction-versus-application gap in specific settings. Zhou et al. [47] show that model-generated
rubrics lag well behind human-authored ones and that the deficit lies in rubric formation, not
application; test-generation studies find LLM-authored suites too weak or misaligned to serve as
reliable verifiers [9, 20, 23, 24]. A longer-running line in open-domain QA evaluation establishes
that reference answer sets are systematically incomplete, so exact-match against them undercounts
correct answers [52, 53]; we show the same incompleteness arises when the model itself authors
the acceptable set, pair it against that model’s own execution ability, and trace it into an RLVR
reward. We do not claim to discover this bottleneck; we explain and generalize it. Relative to this
line our increments are: (i) complete-truth constructions (finite string/arithmetic predicate sets) that
remove the human-rubric incompleteness confound those benchmarks inherit; (ii) a representation-
agnostic measurement that scores enumerated sets, test suites, and reward keys on one footing (§2),
a unification of protocol rather than a new formalism; (iii) silent omission as the identified dominant
failure mechanism (§4), not merely an error statistic; and (iv) a controlled execution of a downstream
cost prior work only projected, measuring it with the mechanism (starvation+pollution) isolated
against an oracle, what an authored verifier does inside an RLVR loop (§5). A parallel line has
models author reward signals or verifiers directly: self-rewarding training [48], generative verifiers
[49], and model critics of code [50], and finds they can help when trained or grounded on labels;
we study the harder zero-/one-shot regime where the authored specification has no such grounding.
Test-generation benchmarks further report LLMs detect planted bugs well [51], a complementary
axis to our finding that authored suites over-reject correct alternatives.

Test-oracle generation, and a contrary result we must address. The software-engineering
literature on LLM-authored oracles bounds our claims in three ways, and we state each rather
than leave it implicit. First, stronger authoring pipelines exist. Fine-tuning raises oracle quality
substantially [54], filtering candidate tests on token-probability/semantic-entropy signals improves
validity [55], and multi-agent consensus improves oracle correctness over the fine-tuned state of the
art [56]. Our falsified repair arm (§4.4) is therefore a claim about same-model, one-shot sample-
then-verify, not a claim that authored verifiers cannot be improved, they demonstrably can be, by
training, external signals, or ensembling, all of which add information our setting withholds. Second,
a result points the other way. Konstantinou et al. [57] report that LLMs are better at generating
oracles than at classifying which oracles are correct, the opposite ordering to our scissors. The
settings differ in what is judged: their classification task asks a model to adjudicate externally
supplied oracle code, whereas our execution arm asks whether a presented candidate solution is
correct; and their generation target is a single assertion rather than an exhaustive acceptable set. We
read the two results as compatible under our sharpened construct (§3.11): writing one specification-
like artifact is easy, and can beat meta-judging that artifact; exhaustively enumerating an acceptable
set is what is hard. Third, that same paper’s primary finding, that generated oracles tend to encode
the actual rather than the expected behaviour, independently corroborates our modal code failure,
over-specification by invented requirement (§3.4, App. D).

The generation–verification gap, and why our sign is the interesting one. That verifying
is easier than generating is the working premise of RLVR, best-of-n, and test-time scaling, and a


                                                  33
literature exists on exploiting and shrinking that gap [22, 49, 62]. Our scissors is an instance of the
same asymmetry, but the sign of its consequence is reversed, and that reversal is the contribution.
In the standard framing the asymmetry is a resource: because judging is cheap and reliable, one
can filter, rerank, or reward with it. We study the case where the artifact a pipeline needs defines
the judged set itself, an answer key, an enumerated rubric, a test suite, so the cheap capability
cannot substitute for the expensive one, and the asymmetry becomes a liability that is inherited by
everything downstream of the artifact. Two further specializations distinguish our claim from the
generic gap: it is set-valued (the failure is coverage, not correctness of a single answer), and its errors
are directional (omission-dominated, hence witness-poor and review-resistant, Observation 2).

Enumeration as a capability. That LLMs enumerate poorly is independently established: they
do not spontaneously count when asked to enumerate, and free-form enumeration lacks any stopping
criterion for completeness [37, 39, 61]. We take that as given rather than as our finding. What we
add is (i) the paired comparison against the same model’s pointwise judging and against its own
intensional specification of the same set, which localizes the deficit, and (ii) the consequence when
the enumerated object is a correctness criterion.

Reward hacking, Goodhart, and RLVR. Imperfect rewards are a foundational safety concern
[1], formalized as reward hacking [33], mapped empirically for misspecified rewards [28], and quan-
tified as over-optimization scaling laws [11]. Reinforcement learning with verifiable rewards [8, 21],
typically optimized with GRPO-style objectives [32, 45], makes an executable check the reward, so
its defects propagate into the policy. The dominant concern is that checks are too weak : hacking
exploits verifiers that accept wrong behavior [14], fuzzing surfaces false positives before training [30],
and RLVR theory treats the false-negative rate as a given channel parameter [3, 16]. Our result is the
complementary direction: machine-authored verifiers are first of all too strict: omission-dominated,
false-negative-heavy, failing closed, so the danger is not that the policy games them but that they
starve correct behavior of reward while simultaneously polluting it (§5, Observation 3). We supply
the missing upstream cause: whether a model can author the verifier at all.

LLM-as-judge and the limits of self-checking. Model judges are now standard evaluators
[12, 46], and the natural remedy for a weak authored specification is to have the model check or
refine its own output: self-consistency [38], self-verification [40], and self-refinement [25]. A growing
counter-literature shows these do not reliably work: models often cannot self-correct reasoning
without external signal [15] and are poor verifiers of their own reasoning and plans [35]. Our repair
arm (§4.4) is the specialization of this finding to verifier authoring, with a mechanism (Eq. 5):
self-filtering fails because the union under-covers S ∗ and the membership judge collapses on self-
generated near-boundary candidates; Observation 2 explains why review is directional rather than
merely weak.

Test, oracle, and specification synthesis. Generating tests to drive or check code is well stud-
ied, from execution-agreement filtering [5] to LLM unit-test generation [31], on benchmarks such
as HumanEval [6] and MBPP [2], with hardened oracles exposing that generated and benchmark
tests are too weak to reject wrong code [23] and that generated oracles encode the author’s mis-
readings [20]. The formal-methods analogue, synthesizing specifications and proofs [10, 43], likewise
reports that specification quality, not proof search, is the binding constraint. We use these hard-
ened oracles as ground truth and measure the authoring direction against them, paired with the



                                                    34
same model’s execution ability, the contrast that turns “generated tests are noisy” into a measured
authoring–execution scissors with a canonical-conditioned decomposition (§3.4).

Mechanisms: enumeration, calibration, and structured decoding. Set-construction
deficits of autoregressive decoders are documented: order sensitivity, non-terminating or premature
stopping, enumeration failures are documented [37, 39, 61]; token distributions misestimate human
cloze acceptability [17]; and calibration degrades exactly at ambiguity boundaries [19, 36, 44].
Constrained/guided decoding [42] can enforce output format but not the completeness of an enu-
merated set, which is the failure we isolate. Finally, human label-variation work [27] measures
disagreement over given labels; our boundary is constructed, so disagreement with it is error, not
opinion, which is what lets us attribute the scissors to the model rather than to annotation noise.

7.2   Design implications
Elicit the rule, not the roster. Where the acceptable set has a compact characterization,
ask the model for the predicate and let machinery enumerate (§3.11). Offloading execution to an
interpreter is program-aided prompting [58, 59]; what our measurement adds is that for acceptable
sets this is not a marginal gain but the whole gap. The boundary is sharp: the escape is unavailable
where no compact rule exists, and a finite test suite only partially escapes, since it is a program
whose checked cases are still enumerated by hand.

Never trust a one-shot authored specification as ground truth. An authored key, suite, or
rubric is not a noisy-but-unbiased artifact; it is directionally wrong in a way its own review cannot
certify. Treat authored specifications as proposals requiring constructed ground truth, execution-
based adjudication, or explicit recall auditing, rather than more review passes, which §4 shows shed
the wrong error direction.

Self-verification is not a substitute for ground truth. Having the model check its own spec-
ification, or assemble it by filtering its own samples, is what our repair arm falsifies (§4.4): the mem-
bership judge that looks strong on curated contrasts collapses on the self-generated near-boundary
candidates that need adjudication. Same-model self-critique therefore buys the appearance of vali-
dation; a known-correct probe (§3.5) is the cheapest real gate.

Controls we did not run. For the record, five checks a skeptical reader is entitled to and we
do not provide. (i) Constrained decoding. We ran structured-emission and order controls (§3.10)
but not grammar-constrained decoding, which would force the output to be a syntactically legal
subset by construction; the residual formatting component we measure is therefore an upper bound
on what constrained decoding would leave. (ii) Decoding sweeps. Everything is greedy and one-
shot, and we did not sweep temperature/top-p/beam. We did run the reasoning-enabled frontier
condition on two constructions: it closes the algorithmic gap for both models but does not reliably
repair test-suite authoring (shrinking Opus’s gap without closing it, not helping GPT-5.1; §3.7),
so our claim is bounded to the no-reasoning regime only where a compact executable rule exists.
The lexical construction under reasoning is untested. (iii) Suite strength beyond catch-wrong. We
report rejection of held-out oracle-wrong solutions, not mutation score or the number of indepen-
dent faulty implementations caught, so “the gated suite is usable” is supported only in that weaker
sense. (iv) Pool diversity. We now measure this rather than only flagging it: a second pool from
three non-Qwen families raises gated false rejection 0.010 → 0.064 and repaired false rejection to


                                                   35
0.075–0.161 (§3.6), so part of the low figure was stylistic proximity. Human-written and adversari-
ally diverse pools remain untested, and both would likely push it higher still. (v) Enriched review
conditions. Our review arm gives the reviewer the drafted key and nothing else. We did not run the
informationally richer variants that would separate “omission is witness-poor” from “our reviewer
was under-equipped”: presenting the full candidate universe, supplying the correct cardinality, sup-
plying a coverage checklist of semantic categories, or comparing independent-model, multi-agent,
and retrieval-augmented review against the single-model loop we test. Observation 2 is stated to be
robust to these (it assumes a perfect membership oracle and only bounds the query budget), but
the empirical 6–7× asymmetry is a property of the review condition we ran, and richer conditions
could shrink it.

Budget for omission when authored artifacts feed RLVR. False-negative-aware RLVR
analyses [3] need a direction and a magnitude for verifier noise; for machine-authored verifiers our
measurements supply both. Two neighbouring results belong alongside ours. Wang et al. [60]
measure verifier false negatives directly and show they cost RL training real prompt efficiency,
but theirs are dominated by formatting brittleness and remedied by a learned verifier, whereas
ours arise from an acceptable set incomplete by omission and are isolated by a controlled A/B;
the two are complementary. Helff et al. [14] supply the dual of our finding, showing RLVR policies
abandon rule induction and enumerate instance labels to satisfy verifiers that check only extensional
correctness. The intensional/extensional distinction thus cuts both ways: policies are rewarded for
enumerating when they should generalize, while verifier authors fail at enumerating and succeed
at characterizing. Reward designers should assume correct-but-omitted behavior exists, measure
it against held-out oracles where possible, and prefer continuous or rubric-style credit [4, 13] over
exhaustive enumerated keys.

7.3   Limitations
Construct validity. WordNet synsets approximate “all acceptable words” imperfectly, which is
precisely why the paper does not rest on them: the central measurement is the algorithmic con-
struction (Table 2), where the acceptable set is computed mechanically over a presented list and
incompleteness is impossible, and the executable construction (§3.4), where correctness is decided
by execution. The three construction types’ confounds are orthogonal (lexical incompleteness, or-
acle weakness, predicate triviality) and the scissors survives on all four constructions, so no single
confound explains it; residual risks are that all three share some deeper artifact of set-enumeration
prompting, which the repair arm (§4.4) partially addresses by varying the interface. Scale and
family coverage. The scaling ladder is one family (Qwen2.5, a deliberate control so scale is the
only variable) with cross-family replication across five further families and generations (Qwen3,
Llama, gemma, Mistral, Phi-4); closed-weight frontier-API models and non-English constructions
remain open. Predicate difficulty and extrapolation. The complete-truth predicates are delib-
erately simple (single-character and small-arithmetic tests) because their purpose is a mechanically
decidable reference, not difficulty realism. This establishes the gap’s existence and direction, not its
magnitude at deployment complexity: with harder predicates both interfaces should degrade, and
which degrades faster is untested, so the numbers here should not be extrapolated as effect sizes for
compositional specifications. The escape assumes the rule is given. Predicate emission is near-
perfect (§3.11) under a condition worth stating plainly: the defining rule appears in the prompt,
so the model restates rather than infers it. Real verification rarely supplies the rule; it must be
derived from prose and examples, which is the operation the suite results show these models failing
(§3.4). We have not run the intermediate condition, inferring a predicate from examples alone, and


                                                  36
it is the experiment that would locate the boundary between restatement and inference. One-shot
authoring baseline. Greedy single-pass authoring is the deployed default we critique, not the
strongest conceivable authoring prompt; the repair arm is the strongest same-model alternative we
know, and it failed, but tool-augmented or multi-model authoring pipelines remain untested. Prop-
agation budget. E6 is one LoRA epoch on single-word rollouts: good for attribution, narrow in
task realism. Its two arms differ in what the effect size means. The lexical arm’s 19–32 point gaps
are WordNet-relative and additionally favour the reference arm through criterion alignment (§5), so
they bound rather than measure a semantic loss; the complete-truth arm is exact but yields a much
smaller 2.3 points (§5.1), and we treat that as the honest causal magnitude on an easy-authoring
task. Effect size therefore depends on how badly the key is authored and on the task, and neither
arm establishes a single universal tax; the unconfirmed suppression/diversity sub-predictions may
yet emerge at longer horizons. Trace repair is measured on one author model. §3.6 now
covers four author families and one benchmark. The recovery is established on HumanEval+ only;
MBPP+ and non-Python targets are untested, and every number assumes a reference implementa-
tion exists (§3.5). The alignment control is one scale, one family. §3.12 rules out instruction
tuning as the cause at 7B on Qwen2.5, using a plain-text harness that is weaker than the paper’s
main prompt for both arms. It shows the deficit exists before post-training; it does not establish
that the base-vs-instruct equivalence holds at every scale, nor for post-training recipes more aggres-
sive than Qwen’s. Field evidence is judge-relative. Corpus facts in §6 come from a commercial
evaluator whose own boundary instability we document; we use them as convergent field signature,
never as ground truth for any headline claim.
     Relation to a companion manuscript. A companion paper by the same author studies the
deployment of §6 as its primary object: the generation pipeline that produced it, its pass rate over
the full curriculum, a cross-validation of the evaluator against judges from other vendors, and a
distillation probe on the evaluator itself. The two manuscripts therefore share one dataset, 43,227
scored items over 755 curriculum standards and ten generator LLMs, graded by one fixed commercial
evaluator, and two format pass rates recur in both (fill-in 96.48%, MCQ 99.13%). The analyses
of that dataset do not overlap. The omission-dominant key-error split (316 to 33), the evaluator’s
25% self-consistency on open-format failures, and the stratified confound analysis of Appendix M
are reported here and not there; the pipeline components, the production run’s headline rate, the
independent-judge validation and the distillation probe are reported there and not here. Nothing
else is common to the two: the four reference constructions, the detectability experiment, the
RLVR propagation study and the gated-verifier mitigation, which is this paper’s entire evidence
base, appear only here, and neither paper’s claims depend on the other’s results. We flag the shared
dataset so reviewers can judge the overlap directly.

7.4   Conclusion
Language models are being promoted from examinees to examiners: they write the tests, keys,
and rubrics that define correctness for other systems. Measured against constructed references,
that promotion outruns one specific capability. The same models that judge membership well,
and that can state the rule generating a set almost perfectly, cannot reliably materialise that set
in one pass; enumeration lags judging across a 24× scale range and does not catch up over it.
Their dominant failure is omitting valid behavior, which is witness-poor: an over-inclusion is a
written token a reviewer can challenge, whereas locating a missing member is itself the enumeration
problem. Local subtractive review therefore shifts an artifact toward under-acceptance rather than
repairing it, and a production corpus shows an observational signature consistent with that (10:1
omission-dominated, with the expert judge least self-consistent at the boundary).


                                                 37
    The cheapest repair, letting the model verify its own proposals, fails where it is needed: four
in five one-shot suites reject even the canonical solution, and sample-then-verify cannot beat the
baseline it was designed to fix, because self-generated candidates sit where the model’s own mem-
bership judgment is worst. Stronger pipelines do help, and prior work shows it; our negative result
concerns the same-model, one-shot procedure. The downstream price is measured and bounded: an
authored key costs 1.9 points of genuine accuracy where the acceptable set is mechanically exact
and 18.5 points of WordNet-relative accuracy on the lexical task, where the reference is incomplete
and favours the reference arm through criterion alignment.
    What the paper does not claim is equally definite, because our own controls bound it. Two
interfaces escape the deficit: emitting an executable predicate recovers the set almost perfectly,
and test-time reasoning closes the algorithmic gap at the frontier. Both require that a compact
executable rule exist, and reasoning does not reliably repair test-suite authoring. The deficit we
characterise is therefore one-shot materialisation of an acceptance region with no compact rule to
restate, extensional where the set is finite and intensional where it is not, which is nonetheless how
answer keys, enumerated rubrics, and test suites are produced at scale today. The practical reading
is constructive: ask a model for the rule, not the roster; where no rule exists, budget for omission
and gate every authored verifier on behavior known to be correct, then repair rather than discard
what the gate rejects, since the same execution that gates can also supply the expected values the
model got wrong. A model-authored verifier is not ground truth, but the model’s weakest interface
wearing the authority of its strongest. Configurations, protocols, and statistical procedures are
specified in App. C.


References
 [1] Dario Amodei, Chris Olah, Jacob Steinhardt, Paul Christiano, John Schulman, and Dan Mané.
     Concrete problems in ai safety. arXiv preprint arXiv:1606.06565, 2016.

 [2] Jacob Austin, Augustus Odena, Maxwell Nye, et al. Program synthesis with large language
     models. arXiv preprint arXiv:2108.07732, 2021.

 [3] Xin-Qiang Cai, Wei Wang, Feng Liu, Tongliang Liu, Gang Niu, and Masashi Sugiyama. Rein-
     forcement learning with verifiable yet noisy rewards under imperfect verifiers. arXiv preprint
     arXiv:2510.00915, 2025.

 [4] Nikhil Chandak, Shashwat Goel, Ameya Prabhu, Moritz Hardt, and Jonas Geiping. An-
     swer matching outperforms multiple choice for language model evaluation. arXiv preprint
     arXiv:2507.02856, 2025.

 [5] Bei Chen, Fengji Zhang, Anh Nguyen, et al. CodeT: Code generation with generated tests. In
     International Conference on Learning Representations (ICLR), 2023.

 [6] Mark Chen, Jerry Tworek, Heewoo Jun, et al. Evaluating large language models trained on
     code. arXiv preprint arXiv:2107.03374, 2021.

 [7] Neil Chowdhury, James Aung, Chan Jun Shern, Oliver Jaffe, Dane Sherburn, Giulio Starace,
     Evan Mays, Rai Dias, Marwan Aljubeh, Mia Glaese, Carlos E. Jimenez, John Yang, Kevin Liu,
     and Aleksander Madry. Introducing SWE-bench verified. OpenAI Blog, 2024.

 [8] DeepSeek-AI. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learn-
     ing. arXiv preprint arXiv:2501.12948, 2025.

                                                 38
 [9] Aleksander Ficek, Somshubra Majumdar, Vahid Noroozi, and Boris Ginsburg. Scoring verifiers:
     Evaluating synthetic verification for code and reasoning. arXiv preprint arXiv:2502.13820,
     2025.

[10] Emily First, Markus N. Rabe, Talia Ringer, and Yuriy Brun. Baldur: Whole-proof genera-
     tion and repair with large language models. In ACM Joint European Software Engineering
     Conference (ESEC/FSE), 2023.

[11] Leo Gao, John Schulman, and Jacob Hilton. Scaling laws for reward model overoptimization.
     Proceedings of ICML, 2023.

[12] Jiawei Gu, Xuhui Jiang, Zhichao Shi, et al. A survey on LLM-as-a-judge. arXiv preprint
     arXiv:2411.15594, 2024.

[13] Anisha Gunjal, Anthony Wang, Elaine Lau, Vaskar Nath, Bing Chen, and Sean Hendryx.
     Rubrics as rewards: Reinforcement learning beyond verifiable domains. arXiv preprint
     arXiv:2507.17746, 2025.

[14] Lukas Helff, Quentin Delfosse, David Steinmann, Raban Härle, Hikaru Shindo, Patrick
     Schramowski, Wolfgang Stammer, Kristian Kersting, and Felix Friedrich. LLMs gaming veri-
     fiers: RLVR can lead to reward hacking. arXiv preprint arXiv:2604.15149, 2026.

[15] Jie Huang, Xinyun Chen, Swaroop Mishra, et al. Large language models cannot self-correct
     reasoning yet. In International Conference on Learning Representations (ICLR), 2024.

[16] Yuzhen Huang, Weihao Zeng, Xingshan Zeng, Qiyuan Zhu, and Junxian He. Pitfalls of
     rule- and model-based verifiers: A case study on mathematical reasoning. arXiv preprint
     arXiv:2505.22203, 2025.

[17] Cassandra L. Jacobs, Loïc Grobol, and Alvin Tsang. Large-scale cloze evaluation reveals
     that token prediction tasks are neither lexically nor semantically aligned. arXiv preprint
     arXiv:2410.12057, 2024.

[18] Dongwei Jiang, Jingyu Zhang, Orion Weller, Nathaniel Weir, Benjamin Van Durme, and Daniel
     Khashabi. SELF-[IN]CORRECT: LLMs struggle with discriminating self-generated responses.
     arXiv preprint arXiv:2404.04298, 2024.

[19] Saurav Kadavath, Tom Conerly, Amanda Askell, et al. Language models (mostly) know what
     they know. arXiv preprint arXiv:2207.05221, 2022.

[20] Michael Konstantinou, Renzo Degiovanni, and Mike Papadakis. Do LLMs generate test oracles
     that capture the actual or the expected program behaviour? arXiv preprint arXiv:2410.21136,
     2024.

[21] Nathan Lambert, Jacob Morrison, Valentina Pyatkin, et al. Tulu 3: Pushing frontiers in open
     language model post-training. arXiv preprint arXiv:2411.15124, 2024.

[22] Hunter Lightman, Vineet Kosaraju, Yura Burda, et al. Let’s verify step by step. In International
     Conference on Learning Representations (ICLR), 2024.

[23] Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang. Is your code generated
     by ChatGPT really correct? rigorous evaluation of large language models for code generation.
     In Advances in Neural Information Processing Systems (NeurIPS), 2023.

                                                 39
[24] Zihan Ma, Taolin Zhang, Maosong Cao, Junnan Liu, Wenwei Zhang, Minnan Luo, Songyang
     Zhang, and Kai Chen. Rethinking verification for LLM code generation: From genera-
     tion to testing. In Advances in Neural Information Processing Systems (NeurIPS), 2025.
     arXiv:2507.06920.

[25] Aman Madaan, Niket Tandon, Prakhar Gupta, et al. Self-refine: Iterative refinement with
     self-feedback. In Advances in Neural Information Processing Systems (NeurIPS), 2023.

[26] George A. Miller. WordNet: A lexical database for English. Communications of the ACM, 38
     (11):39–41, 1995.

[27] Yixin Nie, Xiang Zhou, and Mohit Bansal. What can we learn from collective human opinions
     on natural language inference data? In Proceedings of EMNLP, 2020.

[28] Alexander Pan, Kush Bhatia, and Jacob Steinhardt. The effects of reward misspecification:
     Mapping and mitigating misaligned models. In International Conference on Learning Repre-
     sentations (ICLR), 2022.

[29] Qwen Team. Qwen2.5 technical report. arXiv preprint arXiv:2412.15115, 2024.

[30] Jonas Ray. Before the model learns the bug: Fuzzing RLVR verifiers.                 arXiv preprint
     arXiv:2606.01066, 2026.

[31] Max Schäfer, Sarah Nadi, Aryaz Eghbali, and Frank Tip. An empirical evaluation of using
     large language models for automated unit test generation. IEEE Transactions on Software
     Engineering, 2024.

[32] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang,
     Mingchuan Zhang, Y.K. Li, Y. Wu, and Daya Guo. DeepSeekMath: Pushing the limits of
     mathematical reasoning in open language models. arXiv preprint arXiv:2402.03300, 2024.

[33] Joar Skalse, Nikolaus H. R. Howe, Dmitrii Krasheninnikov, and David Krueger. Defining
     and characterizing reward hacking. In Advances in Neural Information Processing Systems
     (NeurIPS), 2022.

[34] Yuda Song, Hanlin Zhang, Carson Eisenach, Sham Kakade, Dean Foster, and Udaya Ghai.
     Mind the gap: Examining the self-improvement capabilities of large language models. arXiv
     preprint arXiv:2412.02674, 2024.

[35] Kaya Stechly, Karthik Valmeekam, and Subbarao Kambhampati. On the self-verification
     limitations of large language models on reasoning and planning tasks. arXiv preprint
     arXiv:2402.08115, 2024.

[36] Katherine Tian, Eric Mitchell, Allan Zhou, et al. Just ask for calibration: Strategies for eliciting
     calibrated confidence scores from language models. In Empirical Methods in Natural Language
     Processing (EMNLP), 2023.

[37] Oriol Vinyals, Samy Bengio, and Manjunath Kudlur. Order matters: Sequence to sequence for
     sets. In International Conference on Learning Representations (ICLR), 2016.

[38] Xuezhi Wang, Jason Wei, Dale Schuurmans, et al. Self-consistency improves chain of thought
     reasoning in language models. In International Conference on Learning Representations
     (ICLR), 2023.

                                                   40
[39] Sean Welleck, Ilia Kulikov, Jaedeok Kim, Richard Yuanzhe Pang, and Kyunghyun Cho. Con-
     sistency of a recurrent language model with respect to incomplete decoding. In Proceedings of
     EMNLP, 2020.

[40] Yixuan Weng, Minjun Zhu, Fei Xia, et al. Large language models are better reasoners with
     self-verification. In Findings of EMNLP, 2023.

[41] Peter West, Ximing Lu, Nouha Dziri, Faeze Brahman, Linjie Li, Jena D. Hwang, Liwei Jiang,
     Jillian Fisher, Abhilasha Ravichander, Khyathi Chandu, Benjamin Newman, Pang Wei Koh,
     Allyson Ettinger, and Yejin Choi. The generative AI paradox: “what it can create, it may not
     understand”. In International Conference on Learning Representations (ICLR), 2024.

[42] Brandon T. Willard and Rémi Louf. Efficient guided generation for large language models.
     arXiv preprint arXiv:2307.09702, 2023.

[43] Yuhuai Wu, Albert Q. Jiang, Wenda Li, et al. Autoformalization with large language models.
     In Advances in Neural Information Processing Systems (NeurIPS), 2022.

[44] Miao Xiong, Zhiyuan Hu, Xinyang Lu, Yifei Li, Jie Fu, Junxian He, and Bryan Hooi. Can
     LLMs express their uncertainty? an empirical evaluation of confidence elicitation in LLMs. In
     International Conference on Learning Representations (ICLR), 2024.

[45] Qiying Yu et al. DAPO: An open-source LLM reinforcement learning system at scale. arXiv
     preprint arXiv:2503.14476, 2025.

[46] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, et al. Judging LLM-as-a-judge with MT-bench
     and chatbot arena. In Advances in Neural Information Processing Systems (NeurIPS), 2023.

[47] Junyi Zhou, Qiyuan Zhang, Yufei Wang, Fuyuan Lyu, Yidong Ming, Can Xu, Qingfeng Sun,
     Kai Zheng, Peng Kang, Xue Liu, and Chen Ma. RubricBench: Aligning model-generated
     rubrics with human standards. In Proceedings of the 64th Annual Meeting of the Association
     for Computational Linguistics (ACL), 2026. arXiv:2603.01562.

[48] Weizhe Yuan, Richard Yuanzhe Pang, Kyunghyun Cho, Sainbayar Sukhbaatar, Jing Xu, and
     Jason Weston. Self-rewarding language models. arXiv preprint arXiv:2401.10020, 2024.

[49] Lunjun Zhang, Arian Hosseini, Hritik Bansal, Mehran Kazemi, Aviral Kumar, and Rishabh
     Agarwal. Generative verifiers: Reward modeling as next-token prediction. arXiv preprint
     arXiv:2408.15240, 2024.

[50] Nat McAleese, Rai Michael Pokorny, Juan Felipe Ceron Uribe, Evgenia Nitishinskaya, Maja
     Trebacz, and Jan Leike. LLM critics help catch LLM bugs. arXiv preprint arXiv:2407.00215,
     2024.

[51] Niels Mündler, Mark Niklas Müller, Jingxuan He, and Martin Vechev. SWT-Bench: Test-
     ing and validating real-world bug-fixes with code agents. In Advances in Neural Information
     Processing Systems (NeurIPS), 2024.

[52] Ehsan Kamalloo, Nouha Dziri, Charles L. A. Clarke, and Davood Rafiei. Evaluating open-
     domain question answering in the era of large language models. In Proceedings of the 61st
     Annual Meeting of the Association for Computational Linguistics (ACL), 2023.



                                               41
[53] Jannis Bulian, Christian Buck, Wojciech Gajewski, Benjamin Börschinger, and Tal Schuster.
     Tomayto, tomahto: Beyond token-level answer equivalence for question answering evaluation.
     In Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing
     (EMNLP), 2022.

[54] Soneya Binta Hossain and Matthew B. Dwyer. TOGLL: Correct and strong test oracle genera-
     tion with LLMs. In Proceedings of the 47th IEEE/ACM International Conference on Software
     Engineering (ICSE), pages 1475–1487, 2025. arXiv:2405.03786.

[55] Hamed Taherkhani and Hadi Hemmati. VALTEST: Automated validation of language model
     generated test cases. arXiv preprint arXiv:2411.08254, 2024. Later versions appear as
     Taherkhani et al., IEEE TSE 52(4), 2026, rebuilt around semantic entropy.

[56] Qinghua Xu, Guancheng Wang, Lionel Briand, and Kui Liu. Hallucination to consensus: Multi-
     agent LLMs for end-to-end JUnit test generation. ACM Transactions on Software Engineering
     and Methodology, 2026. Introduces the CANDOR framework. arXiv:2506.02943.

[57] Michael Konstantinou, Renzo Degiovanni, and Mike Papadakis. Do LLMs generate test oracles
     that capture the actual or the expected program behaviour? arXiv preprint arXiv:2410.21136,
     2024.

[58] Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon, Pengfei Liu, Yiming Yang, Jamie Callan,
     and Graham Neubig. PAL: Program-aided language models. In Proceedings of the 40th Inter-
     national Conference on Machine Learning (ICML), 2023. arXiv:2211.10435.

[59] Wenhu Chen, Xueguang Ma, Xinyi Wang, and William W. Cohen. Program of thoughts
     prompting: Disentangling computation from reasoning for numerical reasoning tasks. Trans-
     actions on Machine Learning Research, 2023. arXiv:2211.12588.

[60] Zhangchen Wang et al. TinyV: Reducing false negatives in verification improves RL for LLM
     reasoning. arXiv preprint arXiv:2505.14625, 2025.

[61] Kuinan Hou, Marco Zorzi, and Alberto Testolin. Sequential enumeration in large language
     models. arXiv preprint arXiv:2512.04727, 2025.

[62] Jon Saad-Falcon et al. Shrinking the generation–verification gap with weak verifiers. arXiv
     preprint arXiv:2506.18203, 2025.




                                              42
A     Proofs
Observations 2 and 3 are consequences of Definition 1; we give the arguments in full because their
force is structural, not quantitative. (Observation 1 is a measurement identity: its decomposition
of ∆ into batching, coverage, and stopping is established empirically in Appendix K, not proved
here.)

Proof of Observation 2. Let Ŝ ⊆ V and let the reviewer query m̂(x) = ⊮[x ∈ S ∗ ] only on candidates
it names; write OI = Ŝ \ S ∗ , OM = S ∗ \ Ŝ. (i) Over-inclusion. Every x ∈ OI is named by Ŝ, so
querying m̂ on each element of Ŝ flags exactly OI in O(|Ŝ|) queries. (ii) Witness-blindness. The
reviewer’s observations are a function only of Ŝ and of m̂ on the finite set of candidates it names.
Take two oracles S1∗ , S2∗ with S1∗ ∩ Ŝ = S2∗ ∩ Ŝ (so m̂ agrees on all of Ŝ) and S1∗ \ Ŝ ̸= S2∗ \ Ŝ. Because
the query budget is smaller than |V \ Ŝ|, at least one candidate in V \ Ŝ is never named; place
the oracles’ distinguishing element there. The reviewer then names no element of (S1∗ △S2∗ ) \ Ŝ,
so its observations coincide under the two oracles, and it cannot distinguish them or certify which
members are omitted. To break the tie it must name (emit) some x ∈ S ∗ \ Ŝ, which by Definition 1
is the authoring problem restricted to OM. Thus repairing an omission requires authoring. This
is weaker than claiming omission cannot be detected : an external cardinality or coverage certificate
(“|S ∗ | = 10”; “category C uncovered”) can reveal that some omission exists, but such a certificate is
unavailable when S ∗ is the unknown being authored, and detection without a witness still cannot
repair the set.


                                                                       world S1∗ = (Ŝ ∩ S ∗ ) ∪ {a}

           local reviewer            Ŝ: named tokens
            queries m̂(x)                 (the only
                                       queryable set)

                                    m̂ agrees on all of Ŝ;            world S2∗ = (Ŝ ∩ S ∗ ) ∪ {b}
                                 the witnesses a,b lie in the
                                  un-queried region V \ Ŝ

                                                                observations identical ⇒ recall uncertifiable

Figure A.1: The indistinguishability core of Observation 2. A local reviewer can query the membership
oracle only on tokens the artifact names. Two oracles that agree with Ŝ on the intersection but differ by
a witness placed in the un-queried region (non-empty by the query budget) produce identical observations,
so the reviewer cannot tell which members are omitted: certifying recall would require first authoring the
missing witness.

Corollary (directional review; Figure A.1). A review loop that only subtracts flagged errors
(removes members of Ŝ it can challenge) strictly reduces |OI| and leaves |OM| unchanged in expec-
tation up to its authoring ability; iterating it moves Ŝ monotonically toward higher precision and
no-higher recall, i.e. toward under-acceptance. This is the mechanism behind the field trace of §6
(over-inclusions fall round-over-round while omissions persist).

Proof of Observation 3. Write the two rewards as indicator functions R = ⊮[ · ∈ Ŝ] and R∗ =
⊮[ · ∈ S ∗ ] on V . For any x, R(x) ̸= R∗ (x) iff x ∈ Ŝ△S ∗ , with two disjoint cases: (a) x ∈ S ∗ \ Ŝ,
where R(x) = 0 < 1 = R∗ (x) (a withheld reward on correct behavior, starvation); (b) x ∈ Ŝ \ S ∗ ,
where R(x) = 1 > 0 = R∗ (x) (a granted reward on incorrect behavior, pollution). By Definition 1,
|S ∗ \ Ŝ| = (1 − ρ)|S ∗ | and |Ŝ \ S ∗ | = (1 − π)|Ŝ|, giving the stated fractions. For a policy p
over V , the reward it collects is Ep [R] = p(Ŝ) whereas its true accuracy is p(S ∗ ); these differ by


                                                          43
p(Ŝ \ S ∗ ) − p(S ∗ \ Ŝ), so the gradient of expected reward is insensitive to moving mass between
S ∗ \ Ŝ and its complement within the unrewarded region, and rewards moving mass into Ŝ \ S ∗ .
Hence no stationary point of Ep [R] need be a stationary point of p(S ∗ ): R and R∗ disagree exactly
on the two error masses Ŝ△S ∗ , so the two optima need not coincide and the reward’s disagreement
with the oracle is supported precisely on those masses, which §5 measures (1 − ρ = 0.493 set-level
starvation; trained-policy pollution 0.179).


B     Prompts
All prompts are reproduced verbatim; greedy decoding throughout except the sample-then-verify
union (§4.4, T =0.9) and the RLVR rollouts (§5, on-policy). Qwen3 models are run with thinking
disabled so authoring/execution remain one-shot and comparable to the other families.

Intensional control (§3.11), verbatim. Authoring (intensional): “Write a Python function def
accepts(w): that returns True exactly when the lowercase word w {pred}, and False otherwise.
Reply with ONLY a Python code block containing the function.” The emitted function is then
executed over the presented list in a fresh subprocess (8 s timeout); a predicate that fails to parse
or run scores 0.

Emission-format controls (§3.10), verbatim. L (free list, the paper’s format): “Here is a list
of words: {lst}.\nList every word from this list that {pred}. Reply with ONLY a comma-separated
list of words from the given list.” J (JSON checkbox): “Here is a list of words: {lst}.\nFor EVERY
word in the list, decide whether it {pred}. Reply with ONLY a JSON object mapping each word
to true or false, including every word exactly once, in the order given.” S is L with the presented
list order permuted by a fixed seed.

Lexical (WordNet). Authoring: “List every single English word that can mean ‘{gloss}’ (as in:
‘{example}’). Reply with only a comma-separated list.” Execution: “Can the word ‘{cand}’ mean
‘{gloss}’ (as in: ‘{example}’)? Answer yes or no.” Review (§4): the proposed key is shown with
instruction to critique and repair in a fixed REMOVE:/ADD: format.

Algorithmic (complete truth). Authoring: “Here is a list of words: {list}. List every word
from this list that {predicate}. Reply with ONLY a comma-separated list of words from the given
list.” Execution: “Consider the word “{w}”. Does it {predicate}? Answer with exactly one word:
yes or no.” Predicates: contains a double letter ; has 8 or more letters; contains the letters ‘th’ ; ends
with the letter ‘s’.

Code (HumanEval+/MBPP+). Execution (judge): the docstring and a candidate implemen-
tation are shown with “Is the candidate a correct implementation of the specification? Answer with
exactly one word: yes or no.” Authoring: “Write a thorough test suite for this function as a single
function def check(candidate): containing assert statements . . . Reply with ONLY a Python
code block.”

RLVR (§5). “Give ONE English word that means “{gloss}” (as in: “{example}”). Reply with
only the word, nothing else.” Reward = membership of the normalized first line in the arm’s key
(authored or oracle), computed by the deterministic plugin.


                                                   44
C     Construction and training details
The four construction pipelines are summarized in Figure C.1. All measurements ran single-GPU
(bfloat16, PyTorch/Transformers; executable grading via EvalPlus; RLVR via ms-swift’s GRPO).
Lexical: WordNet synsets with 3–8 single-word lemmas and ≥ 1 usage example, target poly-
semy ≤ 4; n=240 items, deterministic seed 0; hard negatives from co-hyponyms, hypernym lem-
mas, antonyms. Algorithmic: n=240 items, each a list of 15 WordNet lemmas (length 3–11,
shuffled seed 0) plus one of four predicates cycled by item index; lists resampled to keep a 2–
13 accept split. Code: HumanEval+ (164 problems) and MBPP+ (378 problems); an oracle-
verified pool built from K=8, T =0.8 samples of Qwen2.5-7B/14B graded by the full EvalPlus suite.
RLVR: GRPO (ms-swift), Qwen2.5-3B policy, LoRA rank 8 (α=32, dropout 0.05, target mod-
ules all-linear); KL coefficient β=0.04; num_generations=8, per-device batch 16, grad-accum 2,
max_completion_length=16, lr 1×10−5 with cosine schedule, rollouts at T =0.9, top-p 1.0, 1 epoch
(510 steps), identical at every scale; 2,400 items (2,040 train / 360 eval). Seeds {1, 2, 3} for the four
scale-sweep arms, {1, . . . , 6} for the two anchor arms; evaluation k=8 per item at T =1.0 as origi-
nally run, superseded for the anchor arms by K=32 with three seeded repeats (App. G); per-step
logs and fully resolved configurations retained for all 27 runs. Determinism and sandboxing:
constructions are sampled at fixed seed 0; execution and one-shot authoring are greedy; the repair
union uses T =0.9, K=10; every authored code suite runs in a fresh subprocess with an 8 s timeout,
and a suite accepts a solution only if the process prints the success sentinel, so crashes and timeouts
count as rejections, a conservative choice that if anything understates authoring failure. Statistics:
all CIs are 2,000-resample item bootstraps, with additional problem-cluster bootstraps for the code
constructions (solutions are nested in problems); production pass rates use Wilson intervals; RLVR
arms are paired per-seed differences; the two anchor arms were extended to n=6 (minimum attain-
able two-sided permutation p=0.031), the four scale-sweep arms remain at n=3, where 0.25 is the
two-sided minimum and no p < 0.05 is attainable. The primary endpoint, fixed before the sweep, is
the authoring–execution gap on the two complete-truth constructions with the preregistered pred-
icates and the single authoring prompt of App. B; the prompt-rephrasing ablation, per-predicate
breakdown, closed-frontier point estimates, OLS scale fit, and cross-family comparisons beyond
Qwen2.5 are exploratory and reported without correction. Closed-model protocol: frontier runs
go through OpenRouter to openai/gpt-5.1 and anthropic/claude-opus-4.8 (accessed 2026-07;
no finer immutable snapshot pins are exposed, a reproducibility limitation of any closed-model
measurement); no system prompt, temperature= 0, six retries with linear backoff, empty com-
pletions counted as failures. Reasoning-enabled conditions use OpenRouter’s provider-normalised
reasoning field rather than each vendor’s native control, so “matched” means matched request,
not verified-identical internal budget; visible-output budgets were 512 (algorithmic authoring), 900
(test-suite authoring), and 64/512 for one-word execution judgments without/with reasoning; sub-
sets (algorithmic n=120, code n=80) are seed-0 draws, with reasoning-off baselines re-run on the
same subsets so off/on are paired. Gemini 3.x could not be run: its API rejects disabling reasoning,
and with reasoning on it returned empty content for the one-word judgments. Raw per-item vectors
are retained alongside each result for recomputation without GPUs.




                                                   45
                                             filter: 3–8 lemmas,
    WordNet
                                                polysemy ≤ 4,                                 240 lexical items
    synsets
                                              + hard negatives

                                     15-word lists × 4 mechan-                                 240 algorith-
    WordNet
                                       ical predicates, seed 0                                 mic/numeric
    lemmas
                                                                                                   items

 HumanEval+                             K=8, T =0.8 Qwen-                                       oracle pool
  / MBPP+                            7B/14B → EvalPlus grade                                   1560✓ / 904×


  2,400 items                           GRPO: Qwen2.5-3B
                                                                                              tax vs. oracle key
  (2040/360)                          LoRA, 510 steps, 3 seeds


                                                     lexical items feed RLVR

Figure C.1: The four construction pipelines and the RLVR loop (App. C). Each construction produces
items carrying a complete oracle set (mechanical predicate, executable oracle, or WordNet synset) plus, for
execution, hard negatives; the lexical items also feed the downstream GRPO experiment (§5). All sampling
seeds and filters are fixed so the pipeline is reproducible end-to-end.


D     Worked examples
Two real, unedited instances make the failure concrete.

Lexical (both errors at once). For the gloss “something that serves as a model or a basis
for making copies” (example: “this painting is a copy of the original”), the oracle synset is S ∗ =
{archetype, original, pilot}. The 14B model authored

      Ŝ = {archetype, copy, master, model, original, prototype, specimen, standard, template, . . . }.

It omits pilot (starvation: a correct member absent, and no review of Ŝ can surface it; Observation 2)
while over-including copy, model, prototype, specimen (pollution: near-synonyms outside this sense).
Recall and precision both suffer, and the two errors are exactly the two crescents of Figure 2.

                                                                                  Ŝ authored key
                 S ∗ oracle synset

                                                                     copy, master, model,
                                                     archetype
                                     pilot                           prototype, specimen,
                                                      original
                                 omission                             standard, template
                                                        TP
                                                                        over-inclusion




                         witness-poor = starvation
                                                                    review sees = pollution

Figure D.1: The lexical worked example as the geometry of Figure 2 on real words. The oracle synset S ∗
(green) and the 14B-authored key Ŝ (pink) share only archetype and original (TP). pilot sits in the oracle-only
crescent (omission: no query on Ŝ can surface it, Observation 2), while seven near-synonyms of the wrong
sense sit in the authored-only crescent (over-inclusion: each is a named token a reviewer or reward can act
on). The single item drives both a recall and a precision loss.



                                                          46
Code (over-specification by invented requirement). Figure D.1 shows the pattern end to
end; for HumanEval/1 (separate_paren_groups), whose spec says nothing about malformed input,
the 14B model authored a suite that invents a ValueError requirement and rejects the problem’s
own canonical solution:

def check(candidate):
    assert candidate(’() (( )) (( )( ))’) == [’()’, ’(())’, ’(()())’]
    assert candidate(’()’) == [’()’]
    assert candidate(’’) == []
    try:                                  # <- requirement not in the spec
         candidate(’(()’)
         assert False, "Expected ValueError for unbalanced parentheses"
    except ValueError:
         pass

The suite runs cleanly (no crash) but asserts behavior the specification never requires; the canonical
solution does not raise, so it is rejected. This is the modal code failure: a syntactically healthy
verifier encoding an expected behavior its author could not correctly compute.

Error taxonomy (HumanEval+, 14B suites). Classifying all 164 authored suites by how they
treat the canonical solution (Table D.1) shows the failure is semantic, not mechanical: 70% run and
reject on an assertion (over-specification), only 9% crash, and 21% accept. Among rejection events
from broken suites, 87.5% are assertion failures and 11.3% runtime errors.

                       Outcome on canonical solution               # suites       fraction
                       Accept (sane)                                   34          0.207
                       Reject by assertion (over-specification)       115          0.701
                       Reject by runtime error (harness bug)          15           0.091
Table D.1: Code authoring error taxonomy (HumanEval+, 14B). Seven in ten authored suites are wrong-by-
assertion, they execute but encode incorrect expected behavior, while fewer than one in ten fail mechanically,
confirming the failure is a boundary the author cannot compute, not a coding accident.



E     Per-predicate algorithmic breakdown
The algorithmic authoring difficulty is predicate-dependent but the ordering (authoring < execution)
holds within every predicate. Table E.1 gives authoring F1 by predicate: enumerating “≥ 8 letters”
is easiest (it is monotone in a single salient feature), “ends in ‘s’ ” is hardest (a sparse suffix condition),
yet all scale sub-critically.

                 Model            double letter    ≥ 8 letters    contains “th”     ends in “s”
                 Qwen2.5-3B           0.264           0.348          0.231             0.194
                 Qwen2.5-7B           0.289           0.608          0.444             0.279
                 Qwen2.5-14B          0.356           0.755          0.515             0.273
                 Qwen2.5-72B          0.362           0.730          0.524             0.316
Table E.1: Authoring F1 by predicate (algorithmic construction). Difficulty varies by predicate structure,
but authoring never approaches the corresponding execution F1 (0.60–0.77, Table 2) for any predicate.



                                                      47
F    Full results: all models × constructions
Table F.1 consolidates every model×construction cell behind the paper’s figures, with 95% bootstrap
CIs on the gaps. The authoring<execution ordering holds in every cell that was run; “—” marks
a cell not run for that model (algorithmic and code cover the four Qwen2.5 scales, both Qwen3
models, both Llama models, Mistral-7B, and Phi-4; lexical covers the Qwen2.5 ladder and gemma).
Per-model numeric results are in Table 3; the two closed-frontier models are in Table 9.

                                      Algorithmic         Code (exec F1 /       Lexical
                Family     Model      gap [95% CI]        accept-correct)    gap [95% CI]
                           3B        +0.340 [.29,.39]      0.763 / 0.331    +0.178 [.13,.23]
                           7B        +0.252 [.22,.29]      0.853 / 0.186    +0.451 [.41,.49]
                Qwen2.5
                           14B       +0.286 [.25,.32]      0.742 / 0.289    +0.388 [.34,.43]
                           72B       +0.286 [.25,.32]      0.895 / 0.422    +0.596 [.56,.63]
                           14B       +0.298 [.27,.32]      0.800 / 0.324          —
                Qwen3
                           32B       +0.309 [.28,.34]      0.783 / 0.262          —
                           3.2-3B    +0.128 [.09,.17]      0.580 / 0.209          —
                Llama-3
                           3.1-8B    +0.190 [.16,.22]      0.766 / 0.101          —
                gemma      4-12B           —                    —           +0.552 [.52,.59]
                Mistral    7B-v0.3 +0.044 [.01,.08]        0.799 / 0.054          —
                Phi        4 (14B) +0.339 [.31,.37]        0.856 / 0.238          —
Table F.1: Master results: authoring–execution gap (algorithmic and lexical) and code execution-
F1/accept-correct, for all eleven models. Every run shows execution above authoring; the gap is present
across four scales and five model families (Qwen, Llama, gemma, Mistral, Phi) spanning two Qwen genera-
tions (Qwen2.5/Qwen3).



G     Two defects we found in our own instrumentation
Both were found by us during a late audit, not by review, and both are reported here with the
before/after numbers rather than silently corrected.
    (1) A double-BOS tokenization defect affecting three of ten open-weight models.
Our measurement scripts build a prompt with apply_chat_template(tokenize=False) and then
encode it with the tokenizer’s default add_special_tokens=True. For model families whose chat
template already emits a beginning-of-sequence token, that prepends a second one. We established
the affected set by token-level comparison rather than by assumption: with the fix, the encoded ids
are byte-identical for Qwen2.5 (3B/7B/14B/72B), Qwen3 (14B/32B) and Phi-4, whose tokenizers
define no BOS, so those seven models provably cannot change and were not re-run. Llama-3.2-3B,
Llama-3.1-8B and Mistral-7B differ by exactly one token and were re-measured on both construc-
tions.
    The paper’s central result is unaffected, since the scaling ladder is Qwen2.5, and the direction
survives everywhere: the execution>authoring ordering holds for all three re-measured models, and
for both Llama models the gap widened (algorithmic +0.091 → +0.128 and +0.148 → +0.190),
because the defect had been depressing the judging arm more than the authoring arm. Mistral’s
algorithmic gap narrowed (+0.079 → +0.044) but stayed positive. What did change materially
is cross-family commentary: Llama-3.2-3B’s code judging F1 rises 0.354 → 0.580 and its authored
suites’ acceptance of correct solutions 0.078 → 0.209, so its gated yield nearly triples (0.073 → 0.213),


                                                     48
its gated catch-wrong rises 0.450 → 0.770 and its vacuous fraction falls 0.250 → 0.086. The claim
that weak authors produce vacuous survivors therefore rests on Mistral alone, not on Llama, and
§3.5 now says so.
    (2) An evaluation too imprecise for the effect it measured. The RLVR arms were
originally scored by sampling K=8 completions per held-out item at temperature 1.0 with no fixed
RNG seed. At an oracle-valid rate near 0.95 over 60 numeric items that is 480 samples, a binomial
standard error of about 1.0 point per arm and roughly 1.4 points on the paired difference, against
a true effect near 2 points. The measurement was therefore of the same order as the quantity being
measured, and under it one numeric seed appeared to reverse sign (−0.8 points).
    We re-scored the identical checkpoints, with no retraining, at K=32 with three explicitly seeded
repeats per adapter, which both shrinks the noise and lets it be measured rather than assumed. The
observed within-adapter spread across eval seeds is 0.18 points (numeric) and 0.16 points (lexical),
an order of magnitude below the effects. Under this instrument all six numeric seeds are positive
and the apparent reversal becomes +0.05. To avoid any ambiguity about which numbers are
which: the superseded K=8 numeric differences were {+3.3, +2.1, +1.5, +1.9, −0.8, +4.2} and the
K=32 ones reported everywhere in the paper are {+3.0, +1.6, +0.5, +3.2, +0.1, +3.1}. Wherever
the body cites per-seed numeric differences it cites the second list; the first appears only here, as
the discarded measurement. The corrected estimates are smaller than our earlier ones: numeric
2.29 → 1.91 points with dz 2.4 → 1.4, lexical 19.10 → 18.51, and both arms now reach two-sided
p=0.031 at n=6. One column is not comparable across the change: distinct_valid_per_item
counts distinct valid answers among K samples and so scales with K; at K=32 its ordering across
arms reverses relative to K=8, which is a further reason the registered diversity sub-prediction is
reported as unconfirmed.


H     E6 per-seed results
Table H.1 lists the six seeds behind Table 19. All figures are the precise re-evaluation of App. G
(K=32, three seeded repeats), so the base row is identical across training seeds by construction.
The oracle arm is tight (σ=0.003); the authored arm varies more (σ=0.026) but every authored
seed lies below every oracle seed (the best authored run, 0.764, still falls short of the worst oracle
run, 0.904), so the gap is not a seed artifact. Seeds 4–6 were added after the first three to lift the
arm past the n=3 significance floor (§5); they were produced by the same script, hyperparameters,
datasets, and keys, verified by checksum before the run.

                   Seed     base     authored key (pollution)    oracle key (pollution)
                   1        0.567          0.694 (0.204)             0.912 (0.039)
                   2        0.567          0.764 (0.155)             0.911 (0.041)
                   3        0.567          0.711 (0.187)             0.914 (0.039)
                   4        0.567          0.754 (0.162)             0.911 (0.043)
                   5        0.567          0.700 (0.196)             0.904 (0.041)
                   6        0.567          0.733 (0.170)             0.914 (0.041)
                   mean     0.567          0.726 (0.179)             0.911 (0.041)
Table H.1: E6 per-seed oracle-valid rate (and trained-policy reward pollution). Training on the oracle key
drives pollution to ≈ 0.04; the authored key holds it near 0.18.




                                                   49
I   Mitigation: probe-strength tradeoff
Beyond the canonical reference, holding out k pooled known-correct solutions as probes gives the
same collapse in false rejection (Table I.1, 14B): a single probe already suffices; additional probes
trade a little yield for marginally lower FRR.

                               Gate                       FRR     Yield
                               ungated                    0.711   1.000
                               canonical reference        0.025   0.268
                               k=1 known-correct          0.013   0.238
                               k=2 known-correct          0.017   0.226
                               k=3 known-correct          0.024   0.213
Table I.1: Probe-strength tradeoff (Qwen2.5-14B, HumanEval+). One known-correct probe is enough to
collapse false rejection; more probes slightly reduce yield.



J    Negative result and incident log
In the spirit of full reporting we record what did not work. Boundary entropy (N1). We tested
whether token-level entropy at the specification boundary predicts authoring error per item, as a
cheap self-signal; the correlation was negligible (r=−0.06), so entropy is not a usable proxy for “this
authored member is wrong.” Registered sub-predictions (E6). Active suppression of omitted-
but-correct answers and diversity narrowing were registered but not confirmed at the one-epoch
budget (omitted fraction and distinct-valid coverage stayed flat or rose); we report the first-order
effect (starvation+pollution) and leave the distributional dynamics to longer horizons. Repair
(E5). The sample-then-verify prediction was registered and falsified (§4.4). Infrastructure inci-
dents. vLLM memory-profiling races on shared GPUs (mitigated by single-GPU + enforce-eager
+ free-memory guard); a remote GRPO run OOM’d under neighbor-job contention and was re-run
locally; ms-swift required an added msgspec dependency. Full claim→script→log→artifact prove-
nance is maintained in the project records.


K     Matched-information decomposition of the algorithmic gap
To test whether the complete-truth gap reflects verifier construction or the classical free-recall-
vs-recognition and compute asymmetries, we decompose it on the algorithmic construction with
the candidate universe U (the 15-word list) presented to every condition, so candidate discovery is
controlled. We score four ways of producing Ŝ as set-F1 against the gold set: A free authoring
(“list every word that P ”, one call); B one-shot label-all (“for each word say yes/no”, one call,
take the yes-set); C pointwise judging (one call per word, take the yes-set); D = C’s yes-set
assembled programmatically (identical set to C, so the pure-assembly floor is 0 by construction).
The comparisons isolate: A→B emission-vs-labeling, B→C batching/context, C→D pure assembly
(≈ 0); Table K.1 reports the decomposition.
Three conclusions. (i) With candidates presented to both arms and the assembly floor at zero, the
complete-truth gap is a set-emission deficit, not recognition-vs-recall or programmatic assembly.
(ii) The decomposition is scale-revealing: batching cost vanishes by 72B (0.004) while emission cost
grows to 0.231: scaling fixes labeling-under-context but not the act of emitting the set, which is
the durable bottleneck. (iii) On the compute axis, scaling authoring samples raises union recall but


                                                     50
      Model            A free-author   B label-all     C pointwise       batching (C−B)     emission (B−A)
      Qwen2.5-7B           0.405          0.471              0.646           0.174                 0.067
      Qwen2.5-14B          0.475          0.590              0.734           0.144                 0.116
      Qwen2.5-72B          0.483          0.714              0.718           0.004                 0.231
Table K.1: Matched-information decomposition (algorithmic, universe U presented to all conditions; set-
F1; assembly floor C→D = 0 by construction). With candidate discovery controlled, one-shot authoring still
lags pointwise judging by 0.24–0.26 at every scale. The decomposition is scale-revealing: the batching term
vanishes (0.174 → 0.004) while the emission term grows (0.067 → 0.231), so at 72B the residual is almost
entirely emission. Paired-bootstrap CIs support the trend. Part of the emission term is serialisation (§3.10).

              Model            K=1         2          4              8     16        execution ceiling
              Qwen2.5-7B       0.381     0.472       0.556      0.646     0.707           ≈ 0.95
              Qwen2.5-14B      0.594     0.679       0.719      0.771     0.797           ≈ 0.97
              Qwen2.5-72B      0.544     0.635       0.714      0.798     0.842           ≈ 0.98
Table K.2: Compute–recall frontier (algorithmic; free authoring sampled K times at T =0.9, union recall
against gold). More authoring inference does raise recall, but it stays below the pointwise arm’s recall at
every scale, even at 16× budget, so the gap is not an artifact of granting judging more calls. The ceiling is a
recall, not the set-F1 of Table K.1; recall upper-bounds F1, which is what makes this an a-fortiori argument.


saturates below execution at every scale, so “the gap does not close” is not an artifact of giving
execution more calls; it holds even at 16× the authoring sampling budget (Table K.2).


L    Complete-truth numeric RLVR: full specification
The complete-truth propagation run (§5.1) carries the paper’s causal claim, so we specify it exhaus-
tively. Generator: a deterministic construction script, seed 0.
How to read the magnitude. With 60 held-out predicates, 3 seeds, and an authored key of recall
0.926 (full specification in Table L.1), the 2.3-point result should be read as a small-scale existence
estimate on an easy-authoring task, not as a general causal magnitude: it establishes that the effect
is present and positive under exact ground truth (3/3 seeds), and its size is bounded by how good
the key is. The larger lexical figure is reference-relative and cannot be substituted for it (§5).




                                                       51
    Item                         Value
    Candidate universe V         {1, . . . , 100} (bounded, so every S ∗ is finite)
    Predicate form               range-scoped, “between a and b that/whose . . . ”
    Predicate families           divisible by 3 or 5; odd and not prime; two digits differ by 2;
                                 prime; multiple of 4 not 8; perfect square; digit-sum = S; multiple of K
    Windows (a, b)               a ∈ {1, 11, . . . , 51}, widths {30, 45, 70}, plus (1, 100), (20, 80), (30, 90)
    Item filter                  keep items with 4 ≤ |S ∗ | ≤ 30, de-duplicated by description
    Unique predicates            160 total: 100 train / 60 held-out, zero overlap
    |S ∗ | (held-out)            mean 10.3, min 4, max 29
    Train instances              2,000 (the 100 train predicates replicated ×20, shuffled)
    Authored key                 Qwen2.5-14B, one-shot greedy, “list every whole number . . . ”;
                                 parsed integers intersected with V ; empty parse backed off to {min S ∗ }
    Authored key quality         held-out recall 0.926, precision 0.987
    Reference (oracle) key       the exact predicate extension, computed in code
    Reward                       ⊮[first integer in the completion ∈ arm’s key]
    Policy / algorithm           Qwen2.5-3B-Instruct, GRPO+LoRA, identical config to §5
    Evaluation                   K=32 samples per held-out predicate at T =1.0, three seeded
                                 repeats per adapter, averaged (App. G); scored by S ∗
    Per-seed authored            0.9432, 0.9547, 0.9554, 0.9469, 0.9731, 0.9434
    Per-seed reference           0.9734, 0.9708, 0.9604, 0.9786, 0.9736, 0.9745
    Base (seed-independent)      0.8877
    Paired differences           +3.0, +1.6, +0.5, +3.2, +0.1, +3.1 points; all positive,
                                 mean 1.9, two-sided permutation p=0.031
Table L.1: Full specification of the complete-truth numeric RLVR arm. Two properties matter for the
causal reading: the universe is bounded, so an authored key can in principle be complete (unlike WordNet);
and train/eval predicates are disjoint, so the gap is not memorisation. The authored key here is nearly
complete (recall 0.926), which is precisely why the tax is small, the effect scales with how badly the key is
authored, and this task is easy to author.


M      Field corpus: stratified analysis
The production comparison in §6 is observational. Here we hold the two covariates the corpus
records fixed and ask whether the fill-in (authored-key) deficit survives within strata. It does, on
both.

                    Difficulty   n fill-in   Pass %     n closed       Pass %       Diff (pts)
                    easy           1267       96.53       1764          98.81         −2.28
                    medium         1261       97.46       1766          98.75         −1.29
                    hard           1250       95.44       1766          98.69         −3.25
                    Pooled (Mantel–Haenszel-style common risk difference)             −2.27
                      95% CI [−2.93, −1.61], z = −6.76
Table M.1: Fill-in vs. closed formats (mcq + msq pooled), stratified by item difficulty. The deficit is
present at every level, so it is not an artifact of fill-in items being harder.

What this does and does not license (Tables M.1 and M.2). It rules out difficulty and grade as
explanations of the format gap; it does not rule out subject, generator model, answer-space size,
evaluator-prompt, or length effects, which the recorded aggregates do not resolve. And the error
taxonomy (the 10:1 omission ratio) remains evaluator-diagnosed, so it is directional evidence about
the kind of failure, not a calibrated rate.


                                                        52
                   Grade     Fill-in pass %             MCQ pass %                 Diff (pts)
                     1            95.83                     99.07                    −3.24
                     2            96.81                     98.41                    −1.60
                     3            95.89                     99.58                    −3.69
                     4            96.80                     99.26                    −2.46
                     5            97.71                     99.09                    −1.38
                     6            97.10                     99.52                    −2.42
                     7            96.46                     98.99                    −2.53
                     8            98.04                     99.02                    −0.98
                     9            95.29                     99.49                    −4.20
                     10           95.81                     97.95                    −2.14
                     11           97.40                     99.48                    −2.08
                     12           96.70                     99.46                    −2.76
                   12/12 grades lower; mean −2.46; sign test p = 2.4 × 10−4
Table M.2: Fill-in vs. MCQ pass rate within each grade. The authored-key format is lower in every one of
the twelve grades, so the deficit is not driven by grade composition. Grade-wise pass rates are themselves flat
within format (χ2 (11) = 6.2 mcq, 6.4 fill-in; p > 0.84), i.e. neither format’s difficulty drifts systematically
with grade.




                                                      53
