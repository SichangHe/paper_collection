                                             CheckDP: An Automated and Integrated Approach for Proving
                                               Differential Privacy or Finding Precise Counterexamples
                                                                           Yuxin Wang, Zeyu Ding, Daniel Kifer, Danfeng Zhang
                                                                                          The Pennsylvania State University
                                                                                 {yxwang,zyding}@psu.edu,{dkifer,zhang}@cse.psu.edu

                                         ABSTRACT                                                                 or if the actual privacy cost is slightly higher than the privacy claim.
                                         We propose CheckDP, an automated and integrated approach for             Recently, static program analyses were proposed to accomplish
                                         proving or disproving claims that a mechanism is differentially          both goals [4, 30]. However, they either only analyze a non-trivial
                                         private. CheckDP can find counterexamples for mechanisms with            but restricted class of programs [4], or rely on heuristic strategies
arXiv:2008.07485v2 [cs.PL] 11 Sep 2020




                                         subtle bugs for which prior counterexample generators have failed.       whose effectiveness on many sutble mechanisms is unclear [30].
                                         Furthermore, it was able to automatically generate proofs for correct       In this paper, we present CheckDP, an automated and integrated
                                         mechanisms for which no formal verification was reported before.         tool for proving or disproving the correctness of a mechanism that
                                         CheckDP is built on static program analysis, allowing it to be more      claims to be differentially private. Significantly, CheckDP automati-
                                         efficient and precise in catching infrequent events than sampling        cally finds counterexamples via static analysis, making it unneces-
                                         based counterexample generators (which run mechanisms hun-               sary to run the mechanism. Like prior work [14], CheckDP still uses
                                         dreds of thousands of times to estimate their output distribution).      PSI [33] at the end. However, replacing sampling-based search with
                                         Moreover, its sound approach also allows automatic verification of       static analysis enables CheckDP to find violations in a few seconds,
                                         correct mechanisms. When evaluated on standard benchmarks and            while previous sampling-based methods [14, 23] may fail even after
                                         newer privacy mechanisms, CheckDP generates proofs (for cor-             running for hours. Furthermore, sampling-based methods may still
                                         rect mechanisms) and counterexamples (for incorrect mechanisms)          require manual setting of some program inputs (e.g., DP-Finder [14]
                                         within 70 seconds without any false positives or false negatives.        requires additional arguments to be set manually for Sparse Vector
                                                                                                                  Technique in our evaluation) while CheckDP is fully automated.
                                         KEYWORDS                                                                 Furthermore, the integrated approach of CheckDP allows it to effi-
                                                                                                                  ciently analyze a larger class of differentially privacy mechanisms,
                                         Differential privacy; formal verification; counterexample detection
                                                                                                                  compared with concurrent work using static analyses [4, 30].
                                         1    INTRODUCTION                                                           Meanwhile, CheckDP still offers state-of-the-art verification ca-
                                                                                                                  pability compared with existing language-based verifiers and is
                                         Differential privacy [27] has been adopted in major data sharing
                                                                                                                  further able to automatically generate proofs for 3 mechanisms
                                         initiatives by organizations such as Google [15, 29], Apple [48],
                                                                                                                  for which no formal verification was reported before. CheckDP
                                         Microsoft [22], Uber [36] and the U.S. Census Bureau [1, 17, 35, 41].
                                                                                                                  takes the source code of a mechanism along with its claimed level
                                         It allows these organizations to collect and share data with provable
                                                                                                                  of privacy and either generates a proof of correctness or a verifi-
                                         bounds on the information that is leaked about any individual.
                                                                                                                  able counterexample (a pair of related inputs and a feasible output).
                                             Crucial to any differentially private system is the correctness of
                                                                                                                  CheckDP is built upon a proof technique called randomness align-
                                         privacy mechanisms, the underlying privacy primitives in larger
                                                                                                                  ment [24, 50, 51], which recasts the task of proving differential
                                         privacy-preserving algorithms. Manually developing the necessary
                                                                                                                  privacy into one of finding alignments between random variables
                                         rigorous proofs that a mechanism correctly protects privacy is a
                                                                                                                  used by two related runs of the mechanism. CheckDP uses a novel
                                         subtle and error-prone process. For example, detailed explanations
                                                                                                                  verify-invalidate loop that alternatively improves tentative proofs
                                         of significant errors in peer-reviewed papers and systems can be
                                                                                                                  (in the form of alignments), which are then used to improve ten-
                                         found in [21, 40, 42]. Such mistakes have led to research in the ap-
                                                                                                                  tative counterexamples (and vice versa) until either the tentative
                                         plication of formal verification for proving that mechanisms satisfy
                                                                                                                  proof has no counterexample, or the tentative counterexample has
                                         differential privacy [3, 5, 7, 9–11, 50, 51]. However, if a mechanism
                                                                                                                  no alignment.
                                         has a bug making its privacy claim incorrect, these techniques can-
                                                                                                                     We evaluated CheckDP on correct/incorrect versions of existing
                                         not disprove the privacy claims – a counterexample detector must
                                                                                                                  benchmarks and newly proposed mechanisms. It generated a proof
                                         be used instead [14, 23, 34]. Finding a counterexample is typically
                                                                                                                  for each correct mechanism within 70 seconds and a counterexam-
                                         a two-phase process that (1) first searches an infinitely large space
                                                                                                                  ple for each incorrect mechanism within 15 seconds.
                                         for candidate counterexamples and then (2) uses an exact symbolic
                                                                                                                     In summary, this paper makes the following contributions:
                                         probabilistic solver like PSI [33] to verify that the counterexam-
                                                                                                                  (1) CheckDP, one of the first automated tools (with concurrent
                                         ple is indeed valid. The search phase currently presents the most
                                                                                                                       work [4, 30]) that generates both proofs for correct mechanisms
                                         problems (i.e., large runtimes or failure to find counterexamples are
                                                                                                                       and counterexamples for incorrect mechanisms (Section 2.4).
                                         most often attributed to the search phase). Earlier search techniques
                                         were based on sampling (running a mechanism hundreds of thou-            (2) A syntax-directed translation from the probabilistic mechanism
                                         sands of times), which made them slow and inherently imprecise:               being checked to non-probabilistic target code with explicit
                                         even with enormous amounts of samples, they can still fail if a               proof obligations (Section 3).
                                         privacy-violating section of code is not executed frequently enough      (3) An alignment template generation algorithm (Section 3.4).
(4) A novel verify-invalidate loop that incrementally improves                                     The Laplace Mechanism which, on input q, outputs q + η (where
    tentative proofs and counterexamples (Section 4).                                              η is sampled from the Laplace distribution with mean 0 and scale
(5) Case studies and experimental comparisons between CheckDP                                      parameter ∆f /ϵ) satisfies ϵ-differential privacy.
    and existing tools using correct/incorrect versions of existing                                   We sometimes abuse notation and refer to the sensitivity ∆q of a
    benchmarks and newly proposed mechanisms. For incorrect                                        numerical value q – we always take this to mean as the sensitivity
    mechanisms, CheckDP automatically found counterexamples in                                     of the function that produced q.
    all cases, even in cases where competing methods [14, 23] failed.
    For correct mechanisms, CheckDP automatically generated                                        2.2     Randomness Alignment
    proofs of privacy, including proofs for 3 mechanisms for which
                                                                                                   Randomness alignment is a simple yet powerful proof technique
    no formal verification was reported before (Section 5).
                                                                                                   that underpins the verification tools LightDP [51] and its successor
                                                                                                   ShadowDP [50]. Precise reasoning using this proof technique was
2 PRELIMINARIES AND RUNNING EXAMPLE
                                                                                                   used to improve a variety of algorithms, allowing them to release
2.1 Differential Privacy                                                                           strictly more information at the same privacy cost [24]. Given two
Among several popular variants of differential privacy [16, 26, 27,                                executions of a randomized algorithm M on D and D ′ respectively, a
43], we focus on pure differential privacy [27]. The goal of differ-                               randomness alignment is a mapping between the random variables
ential privacy is to hide the effect of any person’s record on the                                 in the first execution to random variables in the second execution
output of an algorithm. This is achieved by considering all pairs of                               that will cause the second execution to always produce the same
datasets D and D ′ that differ on one record. We call such datasets                                output as the first. Upper bounds on privacy parameters depend on
adjacent and denote it by D ∼ D ′ . To offer privacy, a differentially                             how much the random variables change under this mapping [51].
private algorithm injects carefully calibrated random noise dur-                                      We use the Laplace Mechanism [28] to illustrate the key ideas
ing its computation. Given a pair of datasets (D, D ′ ), we call the                               behind randomness alignment. Let D ∼ D ′ be a pair of neighboring
execution of an algorithm on D the original execution and the ex-                                  datasets and let f be a query with sensitivity ∆f . Let q = f (D)
ecution on (neighboring) D ′ the related execution. Intuitively, we                                and q ′ = f (D ′ ) be the respective query answers. If we use the
say a randomized algorithm is differentially private if the output                                 Laplace Mechanism to answer these queries with privacy, on input
distribution of the original execution and its related execution are                               q (resp. q ′ ) it will output q + η (resp. q ′ + η ′ ) where η (resp. η ′ ) is a
hard to distinguish for all such dataset pairs:                                                    Laplace random variable with scale ∆f /ϵ. In order for the Laplace
                                                                                                   Mechanism to produce the same output in both executions, we
   Definition 1 (Pure Differential Privacy [25]). Let ϵ ≥ 0. A                                     need q + η = q ′ + η ′ and therefore η ′ = η + q − q ′ . This creates
probabilistic computation M : D → O is ϵ-differentially private if                                 a “mapping” between the values of random noises: if we change
for every pair of neighboring datasets D ∼ D ′ ∈ D and every output                                the input from q to q ′ , we need to adjust the random noise by an
o ∈ O, P[M(D) = o] ≤ e ϵ P[M(D ′ ) = o].                                                           amount of q − q ′ (i.e., this is the distance we need to move η ′ to get
   Often, a differentially private algorithm M interacts with a dataset                            to η). Clearly q − q ′ ≤ ∆f by definition of sensitivity. The privacy
D through a list of queries f 1 , f 2 , . . .: it iteratively runs a query fi                      proof follows from the fact that if two random samples η and η ′
on D to get an exact answer qi , then performs some randomized                                     (from the Laplace distribution with scale ∆f /ϵ) are at most distance
computation on the set of query answers {q j | j ≤ i}. We call the                                 ∆f apart, the ratio of their probabilities is at most e ϵ . Hence, the
vector (q 1 , q 2 , . . .) along with other data-independent parameters to                         privacy cost, the natural log of this ratio, is bounded by ϵ.
M (e.g., privacy parameter ϵ) an input to M. The notion of adjacent                                   Thus randomness alignment can be viewed in terms of distances
datasets translates into the notion of sensitivity on those queries:                               that we need to move random variables. Let q ∼ q ′ be query answers
                                                                                                   from neighboring datasets and Mbe a randomized algorithm which
   Definition 2 (Global Sensitivity [28]). The global sensitivity                                  uses a set of random noises H = η . We associate to every random
of a query f is ∆f = supD∼D ′ f (D) − f (D ′ ) .                                                   variable η a numeric value b     η which tracks precisely the amount in
    We say two inputs inp = {(q 1 , q 2 , . . .), params} and inp ′ =                              value we need to change η in order to obtain the same output when
{(q 1′ , q 2′ , . . .), params} are adjacent with respect to the queries f 1 , f 2 , . . .,        the input to M is changed from q to q ′ . In    other words, the output
and write inp ∼ inp ′ , if the params are the same and there exist                                 of M with input q and random values η is the same as that of
                                                                                                   M with input q ′ and random values η + b           η . Taking M to be the
                                                                                                                                               
two adjacent datasets D and D ′ such that (f 1 (D), f 2 (D), . . . ) =
(q 1 , q 2 , . . .) and (f 1 (D ′ ), f 2 (D ′ ), . . . ) = (q 1′ , q 2′ , . . .). Note that this   Laplace    Mechanism, then the alignment in the previous paragraph
                                                                                                   is bη = q − q ′ . Note that the alignment is a function that depends
                                                                                                      
implies that qi − qi′ ≤ ∆fi , ∀i. It follows that differential privacy
                                                                                                   on M as well as q and q ′ .
can be proved by showing that for all pair of inputs inp ∼ inp ′ and                                  If all of the random variables are Laplace, the cost of an alignment
all outputs o ∈ O, P[M(inp) = o] ≤ e ϵ P[M(inp ′ ) = o]. As stan-                                  is the summation of noise  distance for each random variable. To find
dard, we assume that the sensitivity of inputs are either manually                                                                 scale
                                                                                                   the overall privacy cost (e.g., the ϵ in differential privacy), we then
specified or computed by sensitivity analysis tools (e.g., [32, 44]).                              find an upper bound on the alignment cost for all related q and q ′ .
   Many mechanisms are built on top of the Laplace Mechanism
[27] which adds Laplace noise to query answers:                                                    2.3     Privacy Proof and Counterexample
   Theorem 1 (Laplace Mechanism [27]). Let ϵ > 0, let D be                                         Not all randomness alignments serve as proofs of differential pri-
a dataset, let f be a query with sensitivity ∆f and let q = f (D).                                 vacy. To form a proof, one must show that (1) the alignment forces
                                                                                              2
the two related executions to produce the same output, (2) the pri-                              threshold Tη ). For each query answer, another independent Laplace
vacy cost of an alignment must be bounded by the promised level of                               noise η 2 = Lap (4N /ϵ) is added. If the noisy query answer q[i] +
privacy, and (3) the alignment is injective. Hence, in this paper, an                            η 2 is above the noisy threshold Tη , the gap between them (q[i] +
(alignment-based) privacy proof refers to a randomness alignment                                 η 2 − Tη ) is added to the output list out, otherwise 0 is added.
that satisfies these requirements.
    On the other hand, to show that an algorithm violates differential
privacy, it suffices to demonstrate the existence of a counterexample.                           function GapSVT (T,N,size : num0 ,q : list num∗ )
Formally, if an algorithm M claims to satisfy ϵ-differential privacy,                            returns (out : list num0 ), check(ϵ )
a counterexample to this claim is a triple (inp, inp ′, o) such that                             precondition ∀ i. −1 ≤ bq[i] ≤ 1
inp ∼ inp ′ and P[M(inp) = o] > e ϵ P[M(inp ′ ) = o].                                             1   η 1 := Lap (2/ϵ )
                                                                                                      Tη := T + η 1 ;
   Challenges. LightDP [51] and ShadowDP [50] can check if a                                      2
                                                                                                  3   count := 0; i := 0;
manually generated alignment is an alignment-based privacy proof.
                                                                                                  4   while ( count < N ∧ i < size )
On the other hand, an exact symbolic probabilistic solver, such as                                5      η 2 := Lap (4N /ϵ )
PSI [33], can check if a counterexample, either generated manually                                6      if (q[i] + η 2 ≥ Tη ) then
or via a sampling-based generator, witnesses violation of differ-                                 7         out := ( q [ i ] + η 2 - Tη ):: out ;
ential privacy. To the best of our knowledge, CheckDP is the first                                8          count := count + 1;
tool that automatically generates alignment-based proofs/counterex-                               9      else
amples via static program analysis.1 To do so, a key challenge is                                10         out := false :: out ;
to tackle the infinite search space of proofs (i.e., alignments) and                             11      i := i + 1;
counterexamples. CheckDP uses a novel proof template generation
                                                                                                 function Transformed GapSVT (T,N,size,q, b
                                                                                                                                          q, sampl e, θ )
algorithm to reduce the search space of candidate alignments (Sec-
                                                                                                 returns (out)
tion 3) and uses a novel verify-invalidate loop (Section 4) to find
                                                                                                 12   vϵ := 0; idx = 0;
tentative proofs, counterexamples showing their privacy cost is too
                                                                                                 13   η 1 := sampl e[idx]; idx := idx + 1;
high, improved proofs, improved counterexamples, etc.
                                                                                                 14   vϵ := vϵ + | A1 | × ϵ /2; ηb1 := A1 ;
                                                                                                 15   Tη := T + η 1 ;
2.4      Running Examples
                                                                                                 16   Tc
                                                                                                       η := ηb1 ;
To illustrate our approach, we now discuss two variants of the
                                                                                                 17   count := 0; i := 0;
Sparse Vector Technique [28], one correct and one incorrect. Using                               18   while ( count < N ∧ i < size )
the two variants, we sketch how CheckDP automatically proves/dis-                                19     η 2 := sampl e[idx]; idx := idx + 1;
proves (as appropriate) their claimed privacy properties.                                        20     vϵ := vϵ + | A2 | × ϵ /4N ; ηb2 := A2 ;
   Sparse Vector Technique (SVT) [28]. A powerful mechanism proven                               21     if ( q [ i ] + η 2 ≥ Tη ) then
to satisfy differential privacy. It can be used as a building block for                          22         assert(q[i] + η 2 + bq[i] + ηb2 ≥ Tη + Tc
                                                                                                                                                    η );
many advanced differentially private algorithms. This mechanism                                  23         assert(bq[i] + ηb2 - Tc
                                                                                                                                  η ==  0);
is designed to solve the following problem: given a series of queries                            24       out := ( q [ i ] + η 2 - Tη ):: out ;
and a preset public threshold, we want to identify the first N queries                           25       count := count + 1;
whose answers are above the threshold, but in a privacy-preserving                               26     else
manner. To achieve this, it adds independent Laplace noise both to                               27       assert(¬(q[i] + η 2 + bq[i] + ηb2 ≥ Tη + Tc
                                                                                                                                                    η ));
the threshold and each query answer, then it returns the identities                              28        out := false :: out ;
of the first N queries whose noisy answers are above the noisy                                   29      i := i + 1;
threshold. The standard implementation of SVT outputs true for                                   30   assert(vϵ ≤ ϵ );
the above-threshold queries and false for the others (and termi-
nates when there are a total of N outputs equal to true). We use                                 Figure 1: GapSVT and its transformed code, where under-
two variants of SVT for an overview of CheckDP.                                                  lined parts are added by CheckDP. The transformed code
                                                                                                 contains two alignment templates for η 1 and η 2 : A1 = θ [0]
   GapSVT. This is an improved (and correct) variant of SVT which                                                                                          q [i]) : (θ [4] +
                                                                                                 and A2 = (q[i] + η 2 ≥ Tη ) ? (θ [1] +θ [2] × Tbη +θ [3] ×b
provides numerical information about some queries. When a noisy                                  θ [5]×Tη +θ [6]×b
                                                                                                                 q [i]). The random variables and θ are inserted
query exceeds the noisy threshold, it outputs the difference between                             as part of the function input.
these noisy values; otherwise it returns false. This provides an
estimate for how much higher a query is compared to the threshold.                                   One key observation from the manual proofs of SVT and its
The algorithm was first proposed and verified in [50]; its pseudo                                variants [21, 24, 28, 40] is that the privacy cost is only paid for
code is shown in Figure 1. Here, Lap (2/ϵ) draws one sample from                                 the queries whose noisy answers are above the noisy threshold. In
Laplace distribution with mean 0 and scale factor of 2/ϵ. This ran-                              other words, outputting false does not incur any new privacy cost.
dom value is then added to the public threshold T (stored as noisy                               Correspondingly, the correct alignment for GapSVT [24, 50] (that is,
1 Prior work [3] automatically generates coupling proofs, an alternative language-based
                                                                                                 the distance that η 1 and η 2 need to be moved to ensure the output
proof technique for differential privacy. But all existing verifiers using alignment-based       is the same when the input changes from q[i] to q ′ [i] ≡ q[i] + b q [i],
proofs[50, 51] require manually provided alignments.                                             for all i) is: η 1 : 1 and η 2 : q[i] + η 2 ≥ Tη ? (1 - b
                                                                                                                                                         q[i]) : 0.
                                                                                             3
    Note that η 2 is aligned with non-zero distance only under the                 Verify Sub-loop. Its goal is to generate a proof (i.e., an instantia-
true branch; hence, no privacy cost is paid in the other branch. It             tion of θ ) such that
is easy to verify that if every query has sensitivity 1, the cost of this                               c sample. all assertions in M ′ pass
                                                                                                 ∀inp, inp,
alignment is bounded by ϵ.
                                                                                   This is done by two iterative phases:
   BadGapSVT. We also consider a variant of SVT (and GapSVT)
                                                                                (1) Generating invalidating inputs: Given a proof candidate (i.e.,
that incorrectly tries to release numerical information. When a
                                                                                    an instantiation of θ ), it is incorrect if
noisy query answer is larger than the noisy threshold, the variant
releases that noisy query answer (that is, it does not subtract from it                               c sample. some assertion in M ′ fails
                                                                                               ∃inp, inp,
the noisy threshold); otherwise it outputs false. This is an incorrect
                                                                                    We use I to denote a triple of inp, inp,c sample. Hence, given any
variant of SVT [45] that was reported in [40] and was called iSVT4
                                                                                    instantiation of θ , we use an off-the-shelf symbolic execution
in [23]. More precisely, BadGapSVT replaces line 7 of GapSVT
                                                                                    tool such as KLEE [18] to find invalidating inputs when possible.
with out := (q[i] + η 2 )::out;. This small change makes it
                                                                                (2) Generating proof candidates: with a set of invalidating inputs
not ϵ-differentially private [40]. The reason why is subtle, but the
                                                                                    found so far I 1 , · · · , Ii , we can try to generate a new proof
intuition is the following. Suppose BadGapSVT returns a noisy
                                                                                    candidate to satisfy
query answer q[i] + η 2 = 3, the attacker is able to deduce that
Tη ≤ 3. Once this information is leaked, outputting false in the                                         ∃θ . M ′ (I 1 , θ ) ∧ · · · ∧ M ′ (Ii , θ )
else branch is no longer “free”; every output incurs a privacy cost.
                                                                                    Starting from a default instantiation (e.g., one that sets ∀i. θ [i] =
                                                                                0), CheckDP iteratively repeats Phases 1 and 2. Since CheckDP uses
2.5    Approach Overview
                                                                                all invalidating inputs found so far in Phase 2, the proof candidate
We use GapSVT and BadGapSVT to illustrate how CheckDP gener-                    after each iteration is improving. When Phase 1 gets stuck, CheckDP
ates proofs and counterexamples.                                                obtains a proof candidate θ which is a privacy proof if
    Code Transformation (Section 3). CheckDP first takes the proba-                                     c sample. M ′ (inp, inp,
                                                                                                 ∀inp, inp,                  c sample, θ )
bilistic algorithm being checked, written in the CheckDP language
(Section 3.1), and generates the non-probabilistic target code with             due to the soundness property above. Hence, a proof (alignment) can
assertions and alignment templates (i.e. templates for possible align-          be validated by program verification tools such as CPAChecker [13].
ments). The bottom of Figure 1 shows the transformed code of                    For GapSVT, CheckDP generates and verifies (via CPAChecker) that
GapSVT with alignment templates. The transformed code is dis-                   θ = {1, 1, 0, −1, 0, 0, 0} results in a proof that GapSVT satisfies ϵ-
tinguished from the source code in a few important ways: (1) The                differential privacy.
probabilistic sampling commands (at lines 1 and 5) are replaced                    Invalidate Sub-loop. While the verify sub-loop is conceptually
by non-probabilistic counterparts that read samples from the in-                similar to a CEGIS loop [46], CheckDP also employs an invalidate
strumented function input sample. (2) An alignment template (e.g.,              sub-loop (integrated with the verify sub-loop); its goal is to generate
A1 , A2 ) is generated for each sampling command; each template                 one invalidating input I such that ∀θ . some assertion in M ′ fail. This
contains a few holes, i.e., θ , which is also instrumented as func-             is done by two iterative phases:2
tion input. (3) A distinguished variable vϵ is added to track the               (1) Generating proof candidates: Given an invalidating input I ,
overall privacy cost and lines 14 and 20 update the cost variable in                it is incorrect if ∃θ . M ′ (I, θ ). Hence, given any I , we can use
a sound way. (4) Assertions are inserted in the transformed code                    KLEE [18] to find an alignment when possible.
(lines 22,23,27,30) to ensure the following soundness property:                 (2) Generating counterexamples: with a set of previously found
    if M(inp) is transformed to M ′ (inp, inp,
                                           c sample, θ ), then                      alignments θ 1 , · · · , θ i , we try to find a new invalidating input
                       c sample. all assertions in M ′ pass
           ∃θ . ∀inp, inp,                                                          to satisfy
                               =⇒ M is differentially private                                           ∃I .¬M ′ (I, θ 1 ) ∧ · · · ∧ ¬M ′ (I, θ i )
  We note that the transformed code forms the basis for both proof
                                                                                To integrate with the verify sub-loop, Phase 1 of the invalidate
and counterexample generation in CheckDP.
                                                                                sub-loop starts when Phase 2 of the verify sub-loop gets stuck with
   Proof/Counterexample Generation (Section 4). Inspired by the                 a set of invalidating inputs I 1 , · · · , Ii ; it uses Ii to proceed since it is
Counterexample Guided Inductive Synthesis (CEGIS) [46] tech-                    the most promising one. When Phase 1 of invalidate sub-loop gets
nique, originally proposed for program synthesis, CheckDP uses a                stuck, CheckDP obtains a counterexample candidate, which can be
verify-invalidate loop to simultaneously generate proofs and coun-              validated by PSI [33] (this is necessary since a mechanism might
terexamples. Unlike CEGIS, however, the verify-invalidate loop                  be differentially private even if no alignment-based proof exists).
is bidirectional, in the sense that it internally records all previous              For example, the counterexample found for BadGapSVT sets
counterexamples (resp. proofs) to generate one proof (resp. coun-               the threshold T = 0, N = 1 (max number of outputs equal to
terexample) as the algorithm output. On the other hand, the CEGIS               true before termination), neighboring inputs q = [0, 0, 0, 0, 0] and
loop is unidirectional: it only collects and uses a set of inputs to            q ′ = [1, 1, 1, 1, −1], and the following output to examine [0, 0, 0, 0, 1].
guide synthesis internally. At a high level, the verify-invalidate              2 Note that a set of invalidating inputs I , · · · , I , generated from Phase 2 of the verify
                                                                                                                          1           i
loop of CheckDP includes two integrated sub-loops, one for proof                sub-loop is not a counterexample candidate, since by definition, a differential privacy
generation and the other for counterexample generation.                         counterexample consists of only one invalidating input.
                                                                            4
 Reals               r     ∈    R                                                        For clarity, we distinguish variables holding random values, de-
 Booleans            b     ∈    {true, false}                                          noted by η ∈ H, from other ones, denoted by x ∈ V.
 Vars                x     ∈    V
 Rand Vars           η     ∈    H
 Linear Ops          ⊕    ::=   +|−                                                        Types with Distances. To enable alignment-based proof, one im-
 Other Ops           ⊗    ::=   ×|/                                                    portant aspect of the type system in CheckDP is the ability to
 Comparators         ⊙    ::=   <|>|=|≤|≥                                              compute and track the distances for each program variable. Moti-
 Bool Exprs          b    ::=   true | false | x | ¬b | n1 ⊙ n2                        vated by verification tools using alignments (e.g., LightDP [51] and
 Num Exprs           n    ::=   r | x | η | n1 ⊕ n2 | n1 ⊗ n2 | b ? n1 : n2            ShadowDP [50]), types in the source language of CheckDP have
 Expressions         e    ::=   n | b | e 1 :: e 2 | e 1 [e 2 ]                        the form of B0 or B∗ , where B is the base type such as numerics
 Commands            c    ::=   skip | x := e | η := д | c 1 ; c 2 |                   (num), booleans (bool) and lists (list τ ). The subscript of each type
                                if e then (c 1 ) else (c 2 ) |
                                                                                       is the key to alignment-based proofs: it explicitly tracks the exact
                                while e do (c) | return e
 Rand Exps           д    ::=   Lap r                                                  difference between the value of a variable in two related runs.
 Types               τ    ::=   numd | bool | list τ                                       In the source language of CheckDP, the distances can either be 0
 Distances           d    ::=   0|∗                                                    or ∗: the former indicates the variables stay the same in the related
                                                                                       runs; the latter means that the variable might hold different values in
               Figure 2: CheckDP: language syntax.                                     two related runs and the value difference is stored in a distinguished
                                                                                       variable b x added by the program transformation (i.e., a syntactic
                                                                                       sugar for dependent sum type (b                  x ). For example, inputs
                                                                                                                         Í
                                                                                                                            x : num0 ) Bb
                                                                                       T,N,size are annotated with distance 0 in Figure 1, meaning that
PSI confirms that the probability of this output when q is an input                    they are public parameters to the algorithm; query answers q are
is ≥ e ϵ times the probability of this output when q ′ is the input.                   annotated with distance ∗, meaning that each q[i] differ by exactly
   When Phase 1 of the invalidate sub-loop generates a new align-                      q [i] in two related runs. The type system distinguishes zero-distance
                                                                                       b
ment θ , which happens in our empirical study (Section 5), Phase                       variables as an optimization: as we show shortly, it helps to reduce
2 follows to generate an “improved” invalidating input, which is                       the code size for later stages (Section 3.3) as well as aids proof
then used to start Phase 2 of the validate sub-loop.                                   template generation (Section 3.4).
                                                                                           Note that boolean types (bool) and list types (list τ ) cannot
3     PROGRAM TRANSFORMATION                                                           be associated with numeric distances, hence omitted in the syntax.
CheckDP takes a probablistic program along with an adjacency                           However, nested cases such as list num∗ still accurately track the
specification (i.e., how much two adjacent inputs can differ) and                      distances of the elements inside the list.
the claimed level of differential privacy as inputs. It translates the                     The semantics of CheckDP follows the standard definitions of
source code into a non-probabilistic program with assertions to                        probabilistic programs [37]; the formal semantics can be found
ensure differential privacy. The transformed code forms the basis                      in the Appendix. Finally, CheckDP also supports shadow execu-
of finding a proof or a counterexample (Section 4).                                    tion, a technique that underpins ShadowDP [50] and is crucial to
                                                                                       the verification of challenging mechanisms such as Report Noisy
3.1     Syntax                                                                         Max [25]. However, in order to focus on the most interesting parts
                                                                                       of CheckDP, we first present the transformation without shadow
The syntax of CheckDP source code is listed in Figure 2. Most of                       execution, and later discuss how to support it.
the syntax is standard with the following features:
  • Real numbers, booleans and their standard operations;
  • Ternary expressions b ? n1 : n2 , it returns n1 when b evaluates                   3.2    Program Transformation
    to true or n2 otherwise;                                                           CheckDP is equipped with a flow-sensitive type system whose
  • List operations: e 1 :: e 2 appends element e 1 to list e 2 , and e 1 [e 2 ]       typing rules are shown in Figure 3. At command level, each rule has
    gets the e 2th element of list e 1 ;                                               the following format: ⊢ Γ {c ⇀ c ′ } Γ ′ where a typing environment Γ
  • Loop with keyword while and branch with keyword if;                                tracks for each program variable its type with distance, c and c ′ are
  • A final return command return e.                                                   the source and target programs respectively, and the flow-sensitive
                                                                                       type system also updates typing environment to Γ ′ after command c.
   We now introduce other interesting parts that are needed for
                                                                                       At a high-level, the type system transforms the probabilistic source
developing differentially private algorithms.
                                                                                       code c into the non-probabilistic target code c ′ in a way that if all
   Random Expressions. Differential privacy relies heavily on prob-                    assertions in c ′ holds, then c is differentially private.
abilistic computations: many mechanisms achieve differential pri-                         CheckDP’s program transformation is motivated by those of
vacy by adding appropriate random noise to variables. To model this                    LightDP and ShadowDP [50, 51], all built on randomness alignment
behavior, we embed a sampling command η := Lap r in CheckDP,                           proof. However, there are a few important differences:
which draws a sample from the Laplace distribution with mean 0                           • CheckDP generates an alignment template for each sampling in-
and scale of r . In this paper, we only focus on the most interesting                      struction, rather than requiring manually provided alignments.
sampling command Lap r (which is used in Laplace Mechanism                               • CheckDP defers all privacy-related checks to assertions. This is
and GapSVT in Section 2). However, we note that it is fairly easy                          crucial since information needed for proof and counterexample
to add new sampling distributions to CheckDP.                                              generation is unavailable in a lightweight static type system.
                                                                                   5
Transformation rules for expressions with form Γ ⊢ e : Bn
                                   (T-Num)                                          (T-Boolean)                                                        (T-VarZero)
             Γ ⊢ r : num0 | true                            Γ ⊢ b : bool | true                                     Γ, x : B0 ⊢ x : B0 | true

                                                                  Γ ⊢ e : bool | C                           Γ ⊢ e 1 : Bn1 | C1         Γ ⊢ e 2 : Bn2 | C2
                                       (T-VarStar)                                       (T-Neg)                                                                (T-OPlus)
         Γ, x : B∗ ⊢ x : Bxb | true                              Γ ⊢ ¬e : bool | C                                Γ ⊢ e 1 ⊕ e 2 : Bn1 ⊕n2 | C1 ∧ C2

                                                                                            Γ ⊢ e 1 : numn1 | C1      Γ ⊢ e 1 : numn2 | C2
                 Γ ⊢ e 1 : numn1 | C1     Γ ⊢ e 2 : numn2 | C2                                                                                             (T-ODot)
                                                                    (T-OTimes)                                                  (e 1 ⊙ e 2 ) ⇔
                                                                                     Γ ⊢ e 1 ⊙ e 2 : bool | C1 ∧ C2 ∧
               Γ ⊢ e 1 ⊗ e 2 : num0 | C1 ∧ C2 ∧ (n1 = n2 = 0)                                                             (e 1 + n1 ) ⊙ (e 2 + n2 )

                  Γ ⊢ e 1 : Bn1 | C1     Γ ⊢ e 2 : list Bn2 | C2                                    Γ ⊢ e 1 : list τ | C1     Γ ⊢ e 2 : numn | C2
                                                                       (T-Cons)                                                                            (T-Index)
               Γ ⊢ e 1 :: e 2 : list Bn | C1 ∧ C2 ∧ (n1 = n2 = 0)                                      Γ ⊢ e 1 [e 2 ] : τ | C1 ∧ C2 ∧ (n = 0)

                                              Γ ⊢ e 1 : bool | C1    Γ ⊢ e 2 : Bn1 | C2      Γ ⊢ e 3 : Bn2 | C3
                                                                                                                    (T-Select)
                                                   Γ ⊢ e 1 ? e 2 : e 3 : Bn1 | C1 ∧ C2 ∧ C3 ∧ (n1 = n2 )

Transformation rules for commands with form ⊢ Γ {c ⇀ c ′ } Γ′
                                          (
                                            ⟨0, skip⟩, if n == 0,
                 Γ ⊢ e : Bn | C ⟨d, c ⟩ =
                                                x := n⟩, otherwise
                                            ⟨∗, b                                                            ⊢ Γ {c 1 ⇀ c 1′ } Γ1        ⊢ Γ1 {c 2 ⇀ c 2′ } Γ2
                                                                                     (T-Asgn)                                                                     (T-Seq)
                       ⊢ Γ {x := e; ⇀ assert(C); x := e; c } Γ[x 7→ Bd ]                                               ⊢ Γ {c 1 ; c 2 ⇀ c 1′ ; c 2′ } Γ2

                                          Γ ⊢ e : Bn | C
                                                                                 (T-Return)                                                        (T-Skip)
                     ⊢ Γ {return e ⇀ assert(C ∧ n = 0); return e } Γ                                                 ⊢ Γ {skip ⇀ skip} Γ

                                              ⊢ Γ ⊔ Γf {c ⇀ c ′ } Γf     Γ, Γ ⊔ Γf ⇛ c s       Γf , Γ ⊔ Γf ⇛ c ′′
                                                                                                                            (T-While)
                                       ⊢ Γ {while e do c ⇀ c s ; (while e do (assert(Le, ΓM◦ ); c ′ ; c ′′ ))} Γ ⊔ Γf

                                                      ⊢ Γ {c i ⇀ c i′ } Γi   Γi , Γ1 ⊔ Γ2 ⇛ c i′′   i ∈ {1, 2}
                                                                                                                                                       (T-If)
                     ⊢ Γ {if e then c 1 else c 2 ⇀ if e then (assert(Le, ΓM ); c 1′ ; c 1′′ ) else (assert(¬Le, ΓM◦ ); c 2′ ; c 2′′ )} Γ1 ⊔ Γ2
                                                                                     ◦


                A = GenerateTemplate(Γ, All Assertions)               c a = assert(((η + A){η 1 /η } = (η + A){η 2 /η } ⇒ η 1 = η 2 ))
                                                                                                                                                     (T-Laplace)
                 ⊢ Γ {c a ; η := Lap r ⇀ η := sampl e[idx ]; idx := idx + 1; vϵ := vϵ + | A |/r ; b
                                                                                                  η := A ; } Γ[η 7→ num∗ ]

Transformation rules for merging environments

                                                       Γ1 ⊑ Γ2         x := 0 | Γ1 (x ) = num0 ∧ Γ2 (x ) = num∗ }
                                                                  c = {b
                                                                               Γ1, Γ2 ⇛ c


 Figure 3: Program transformation rules. Distinguished variable vϵ and assertions are added to ensure differential privacy.


 • CheckDP only tracks if a variable has the same value in two                             variable is retrieved from the environment (T-VarZero,T-VarStar)
   related runs (with distance 0) or not (with distance ∗). This                           (note that rule (T-VarStar) just desugers the ∗ notation). For linear
   design aids alignment template generation and reduces the size                          operation (⊕), the distance of the result is computed in a precise
   of transformed code.                                                                    way (Rule (T-OPlus)), while the other operations are treated in a
                                                                                           more conservative way: constraints are generated to ensure that
    Checking Expressions. Each typing rule for expression e computes                       the result is identical in Rules (T-OTimes, T-ODot). For example,
the correct distance for its resulting value: Γ ⊢ e : Bn | C, which                        (T-ODot) ensures boolean value of e 1 ⊙ e 2 will be the same in two
reads as: expression e has type B and distance n under the typing                          related runs by adding a constraint
environment Γ if the constraints C are satisfied. The reason to
collect constraints C instead of statically checking them, is to defer                                           (e 1 ⊙ e 2 ) ⇔ (e 1 + n1 ) ⊙ (e 2 + n2 )
all privacy-related checks to later stages.
    Most of the expression rules are straightforward: they check the                       (T-Cons) restricts constructed list elements to have 0-distance (note
base types (just like a traditional type system) and compute the                           that the restriction does not apply to input lists), while (T-Index)
distance of e’s value in two related runs. For example, all constants                      requires the index to have zero-distance. Rule (T-Select) restricts
must be identical (Rules (T-Num,T-Boolean)) and the distance of a                          e 1 and e 2 to have the same distance. The constraints gathered in the
                                                                                     6
expression rules will later be explicitly instrumented as assertions          3.4    Checking Sampling Commands
in the translated programs, which we will explain shortly.                    Rule (T-Laplace) performs a few important tasks:

3.3    Checking Commands                                                         Replacing Sampling Command. Rule (T-Laplace) removes the
                                                                              sampling instruction and assign to η the next (unknown) sample
For each program statement, the type system updates the typing en-
                                                                              value sample[idx], where sample is a parameter of type list num
vironment and if necessary, instruments code to update b x variables
                                                                              added to the transformed code. The typing rule also increments idx
to the correct distances. Moreover, it ensures that the two related
                                                                              so that the next sampling command will read out the next value.
runs take the same branch in if-statement and while-statement.
                                                                                 Checking Injectivity. T-Laplace adds an assertion c a to check the
    Flow-Sensitivity. Each typing rule updates the typing environ-
                                                                              injectivity of the generated alignment (a fundamental requirement
ment to track if a variable has zero-distance. When a variable has
                                                                              of alignment-based proofs): the same aligned value of η implies the
non-zero distance, it instruments the source code to properly main-
                                                                              same value of η in the original execution.
tain the corresponding b  x variables. The most interesting rules are:
rule (T-Asgn) properly promotes the type of x to be B∗ (tracked by               Tracking Privacy Cost. A distinguished privacy cost variable vϵ
distance variables) in Γ ′ if the distance of e is not 0. Meanwhile it        is also instrumented to track the cost for aligning the random vari-
optimizes away updates to b    x and properly downgrades type to B0           ables in the program. Due to the properties of Laplace distribution,
if e has a zero-distance. For example, line 16 in GapSVT (Figure 1)           for a sampling command η := Lap r with alignment template A, we
is instrumented to update distance of Tη , according to the distance          have P(η)/P(η +A) ≤ e| A |/r . Hence, the privacy cost for aligning η
of T + η 1 . Moreover, variable count in GapSVT always has the type           by A is|A| /r . Note that the symbols in gray, including A, are place-
num0 ; therefore its distance variable never appears in the translated        holders when the rule is applied, since function GenerateTemplate
program due to the optimization in (T-Asgn).                                  takes all assertions in the transformed code as inputs. Once trans-
    Rule (T-If) and (T-While) are more complicated since they both            lation is complete, the placeholders are filled in by the algorithm
need to merge environments. In rule (T-If), as c 1 and c 2 might              that we discuss in Section 4.
update Γ to Γ1 and Γ2 respectively, we need to merge them in a
natural way: the distance of a type form a two-level lattice with                Alignment Template Generation. For each sampling command
0 ⊏ ∗. Thus we define a union operator ⊔ for distances d as:                  η := Lap r , an alignment of η is needed in a randomness alignment
                                  (                                           proof. In its most flexible form, the alignment can be written as
                                    d1 if d1 = d2                             any numerical expression n, which is prohibitive for our goal of
                      d1 ⊔ d2 ≜                                               automatic proof generation. On the other hand, using simple heuris-
                                    ∗ otherwise
                                                                              tics such as only considering constant alignment does not work:
therefore the union operator for two environments are defined as              for example, the correct alignment for η 2 in GapSVT is written as
follows: Γ1 ⊔ Γ2 = λx . Γ1 [x] ⊔ Γ2 [x].                                                                 q[i]) : 0”, where the alignment actually
                                                                              “(q[i] + η 2 ≥ Tη ) ? (1 − b
   Moreover, we use an auxiliary function Γ1 , Γ2 ⇛ c to “promote”            depends on which branch is taken during the execution.
a variable to star type. For example, with Γ(x) = ∗, Γ(y) = ∗ and                To tackle the challenges, CheckDP generates an alignment tem-
Γ(b) = 0, rule (T-If) translates the source code                              plate for each sampling instruction; a template is a numerical ex-
if b then x := y else x := 1 to the following:                                pression with “holes” whose values are to be searched for in later
if b then (x := y; bx := b
                         y ; ) else (x := 1; b
                                             x := 0)                          stages. For example, the template generated for η 2 in GapSVT is
where bx := b y is instrumented by (T-Asgn) and b    x := 0 is instru-
mented due to the promotion.                                                         (q[i] + η 2 ≥ Tη )?(θ [0] + θ [1] × Tbη + θ [2] × b
                                                                                                                                       q[i]):
   Similarly, the typing environments are merged in rule (T-While),                                         (θ [3] + θ [4] × Tbη + θ [5] × b
                                                                                                                                           q[i])
except that it requires a fixed point Γf such that ⊢ Γ ⊔ Γf {c} Γf .
                                                                              where θ [0] − θ [5] are symbolic coefficients to be found later.
We follow the construction in [50] to compute a fixed point, noting
                                                                                 In general, for each sampling command η = Lap r , CheckDP
that the computation always terminates since all of the translation
                                                                              first uses static program analysis to find a set of relevant program
rules are monotonic and the lattice only has two levels.
                                                                              expressions, denoted by E, and a set of relevant program variables,
   Assertion Generation. To ensure differential privacy, the type             denoted by V (as described shortly). Second, it generates an align-
system inserts assertion in various rules:                                    ment template as follows:
 • To ensure that two related runs take the same control flow, (T-                     (
                                                                                         e 0 ? AE\{e0 } : AE\{e0 } , when E = {e 0 , · · · }
    If) and (T-While) asserts that the value of the branch condition           AE ::=
                                                                                         θ 0 + vi ∈V θ i × vi with fresh θ 0 , · · · , θ | V | , otherwise
                                                                                               Í
    stays the same across two related executions. A helper function
    Le, ΓM◦ is used to compute the value of e in the aligned execution;       where θ denotes coefficients (“holes”) to be filled out out by later
    its full definition can be found in the Appendix.                         stages and each of them is generated fresh.
 • To ensure that the final output value is differentially private,              To find proper E and V, our insight is that the alignments serve
    rule (T-Return) asserts that its distance is zero (i.e., identical        to “cancel out” the differences between two related runs (i.e., to
    in two related runs).                                                     make all assertions pass). Algorithm 1 follows the insight to com-
 • To ensure all constraints collected in the expression rules are            pute E and V for each sampling instruction: it takes Γs , the typing
    satisfied, assignment rules (T-Asgn) and (T-AsgnStar) also                environment right before the sampling instruction and A, all asser-
    insert corresponding assertions.                                          tions in the transformed code, as inputs. It also assumes an oracle
                                                                          7
Depends(e, x) which returns true whenever the expression e de-                      3.5    Function Signature Rewrite
pends on the variable x. We note that the oracle can be implemented                 Finally, CheckDP rewrites the function signature to reflect the
as standard program dependency analysis [2, 31] or information                      extra parameters and holes introduced in the transformed code.
flow analysis [12]; hence, we omit the details in this paper.                       In general, M(inp) is transformed to a new function signature
                                                                                    M ′ (inp, inp,
                                                                                               c sample, θ ) where inp
                                                                                                                    c are the distance variables associ-
                                                                                    ated with inputs whose distance is not zero (e.g., bq is associated
  Algorithm 1: Template generation for η := Lap r
                                                                                    with q in GapSVT), sample is a list of random values used in M, and
   input : Γs : typing environment at sampling command                              θ are the missing holes in alignment templates.
           A: set of the generated assertions in the program
 1 function GenerateTemplate(Γs , A):
 2    E ← ∅, V ← ∅                                                                  3.6    Shadow Execution
 3    foreach assert(e) ∈ A do                                                      To tackle challenging mechanisms such as Report Noisy Max [25],
 4         if Depends(e, η) then
 5               if assert(e) is generated by (T-If) then                           CheckDP uses shadow execution [50]. Intuitively, the shadow exe-
 6                   e ′ ← the branch condition of if                               cution tracks another program execution where the injected noises
 7                   E ← E ∪ {e ′ }                                                 are always the same as those in the original execution. Therefore,
                                                                                    values computed in the shadow execution incur no privacy cost.
 8               foreach v ∈ V ars ∪ {e 1 [e 2 ]|e 1 [e 2 ] ∈ e} do
 9                   if Γs ̸⊢ v : B0 ∧ Depends(e, v) then                           The aligned execution can then switch to shadow execution when
10                       V ← V ∪ {v}                                                certain conditions are met, allowing extra permissiveness [50].
                                                                                       Supporting shadow execution only requires a few modifications:
11     foreach e ∈ E ∪ V do                                                         (1) Expressions will have a pair of distances (⟨d◦ , d† ⟩), where the
12        remove e from E and V if not in scope                                         extra distance d† tracks the distance in the shadow execution;
13     return E,V;                                                                  (2) Since the branches and loop conditions in shadow execution
                                                                                        are not aligned, they might diverge from the original execution.
                                                                                        Hence, a separate shadow branch/loop is generated to correctly
                                                                                        update the shadow distances for the variables.
    The algorithm first checks (at line 4) if aligning η has a chance to               Since the extended transformation rules largely follow the cor-
make an assertion pass. If so, it will increment E and V as follows.                responding typing rules of ShadowDP, we present the complete set
For E, we notice that only for the assertions generated by rule (T-If),             of rules with detailed explanations in the Appendix.
depending on the branch condition allows the alignment to have
different values under different branches. Hence, we add the branch
condition to E in this case. For V, our goal is to use the alignment to             3.7    Soundness
“cancel” the differences caused by other variables and array elements               CheckDP enforces a fundamental property: suppose M(inp) is trans-
such as q[i] used in e. Hence, we only need to consider v         b if (1) v        formed to M ′ (inp, inp,
                                                                                                         c sample, θ ), then M(inp) is differentially pri-
is different between two related runs (i.e., Γs ̸⊢ v : B0 ) and (2) v               vate if there is a list of values of θ , such that all assertions in M ′
contributes the assertion (i.e., e depends on v).                                   hold for all inp, inp,
                                                                                                       c sample. Recall that an alignment template A
    Finally, the algorithm performs a “scope check”: if any element in              is a function of θ . Hence, we have a concrete alignment A(θ ) (i.e.,
E or V contains out-of-scope variables, then the element is excluded;               a proof) when such values of θ exist.
for example, η 1 should not depend on q[i] in GapSVT since q[i],                       We build the soundness of CheckDP based on that of Shad-
essentially an iterator of q, is not in scope at that point.                        owDP [50]. The main difference is that ShadowDP requires every
    Consider η 1 and η 2 in GapSVT. The assertions in the translated                sampling command η := Lap r to be manually annotated. Thus,
programs are (we only list the assertion in the true branch since                   we can easily rewrite a program M in CheckDP to a program M̃ in
the constraint in false branch is symmetric) :                                      ShadowDP by adding the following annotations:
 (1) assert(q[i] + η 2 + b      q[i] + ηb2 ≥ Tη + Tbη )                             η := Lap r → η := Lap r ; ◦; Aη (θ ) (CheckDP to ShadowDP)
 (2) assert(b   q[i] + ηb2 - Tbη = 0)                                                  where Aη is the alignment template for η. We formalize the
    For η 1 , we have Γs = {q : ∗} (we omit the base types and the vari-            main soundness results next; the full proof can be found in the
ables that have 0 distance for brevity) and both assertions depend                  Appendix.
on η 1 . Since both assertions depend on η 1 and q[i], Algorithm 1
adds b q[i] into V. Moreover, assertion (1) is generated by rule (T-If).               Theorem 2 (Soundness). Let M be a mechanism written in
Thus,the algorithm adds q[i] + η 2 ≥ Tη into E. Finally, since                      CheckDP. With a list of concrete values of θ , let M̃ be the correspond-
q[i] is out of scope at the sampling instruction, expression using                  ing mechanism in ShadowDP by rule (CheckDP to ShadowDP). If
q[i] and variable q[i] are excluded, resulting V ={ } and E ={ }.                   (1) M type checks, i.e., ⊢ Γ {M ⇀ M ′ } Γ ′ and (2) the assertions in
    For η 2 , we have Γs = {q: *, Tη : *}. Since both assertions depend on          M ′ hold for all inputs. Then M̃ type checks in ShadowDP, and the
η 2 and q[i] and T , Algorithm 1 adds b       q[i] and Tbη into V. Similar          assertions in M̃ ′ (transformed from M̃ by ShadowDP) pass.
to η 1 , the algorithm also adds q[i] + η 2 ≥ Tη into E. Finally, all
expressions and variable are in scope, resulting V ={b        q[i], Tbη } and         Theorem 3 (Privacy). With exactly the same notation and as-
E ={q[i] + η 2 ≥ Tη }.                                                              sumption as Theorem 2, M satisfies ϵ-differential privacy.
                                                                                8
                                    𝜃"                      CheckDP                                    Input Space                             Input Space
                                                                                                                                                          𝜃2
             Invalidating Input      𝐼! , ⋯ , 𝐼"                                                            𝐼0                                      𝐼0
                                                       Proof Generation                                          𝜃1
                Generation                                                                                                                               𝜃1
                       𝜃"
                                          𝐼!"#              𝐼"                                          𝜃2 𝐼$                                       𝐼$
        𝜃!                    𝐼"                                                                                                                              …
                                             𝜃! , ⋯ , 𝜃" Counterexample
                  Verifier
                                     Restart
                                                          Generation                       (a) A case where θ i cannot be           (b) Iteratively improving the
                                                                                               improved.                                alignment θ i .
                      𝜃"                                     𝐶
                                   Unknown                    PSI                             Figure 5: Tentative alignments and invalidating inputs.

                   Proof                               Counterexample                      violation at Line 22. Hence, the identified invalidating input I 0 is
         Verify Sub-loop             Invalidate Sub-loop               Exit                fed to the Proof Generation component.
Figure 4: Overview of the verify-invalidate loop of CheckDP.                                   Proof Generation. This component takes in a series of invalidat-
                                                                                           ing inputs I 0 , · · · , Ii seen so far, and tries to find an proof candidate
4     PROOF AND COUNTEREXAMPLE                                                             θ i such that:
      GENERATION                                                                                                      M ′ (I 0 , θ i ) ∧ · · · ∧ M ′ (Ii , θ i ).
Recall that the transformed source code has the form of the fol-                               Intuitively, the goal is to find a proof candidate θ i that success-
lowing: M ′ (inp, inp,          c sample, θ ). For brevity, Let I denote a triple of       fully “covers” all invalidating inputs seen so far. Most likely, an
(inp, inp, c sample), and C denote a counterexample in the form of                         improved proof candidate θ i that is able to align randomness for
C = (inp, inp ′, o) as defined in Section 2.3. Proof/counterexample                        more inputs is generated by the component. Then θ i is fed back to
generation is divided into two tasks:                                                      the Invalidating Input Generation component, closing the loop.
  • Proof Generation: find an instantiation of θ such that assertions                          Consider the GapSVT example again. In order to align random-
        in M ′ never fail for any input I , or                                             ness for the invalidating input I 0 , one possible θ 1 is to align the
  • Counterexample Generation: find an instantiation of I , such                           random variable η 2 by −b         q [i] to cancel out the difference introduced
        that no θ exists to make all assertions in M ′ pass, and then                      by q[i]. Note that this tentative proof θ 1 does not work for all pos-
        construct a counterexample C based on I .                                          sible inputs: it only serves as the “best” proof given I 0 . With the
     The key challenge here is the infinite search space of both θ                         Verify Sub-loop, such imperfect proof candidates enable the gen-
and I . Our insight is to use a verify-invalidate loop, as depicted in                     eration of more invalidating inputs, such as an invalidating input
Figure 4, to improve θ and I after each iteration. At a high-level,                        I 1 where the query answers are mostly below the threshold T (I 1
the iterative process involves two sub-loops: the (green) verify                           invalidates θ 1 since a privacy cost incurs whenever any branch is
sub-loop generates proofs, and the (blue) invalidate sub-loop gener-                       taken, which eventually exhausts the given privacy budget). There-
ates counterexamples. Moreover, the two sub-loops are integrated:                          fore, a more general proof that leverages the conditional expression
starting from a default θ 0 where θ 0 [i] = 0. ∀i, the procedure gen-                      q[i] + η 2 ≥ T ? • : • in the alignment template can be discovered
erates sequences of proofs and invalidating inputs in the form of                          by Proof Generation. For GapSVT, the Verify sub-loop eventually
θ 0 , I 0 , θ 1 , I 1 , · · · . The final θ k or Ik is used to construct proof or          terminates with a correct proof (Section 5).
counterexamples correspondingly.
                                                                                               Exit Edges. The verify loop has two exit edges. First, when no
                                                                                           invalidating input is generated, θ i is likely a valid proof. Hence, θ i
4.1     Verify Sub-Loop
                                                                                           is passed to a verifier with the following condition: ∀I . M ′ (I , θ i ).
The verify sub-loop that involves Invalidating Input Generation                            Due to the soundness result (Theorem 3), we have a proof of dif-
and Proof Generation components is responsible of generating a                             ferential privacy when the verifier passes (the “Exit” edge from
sequence of improving alignments θ 0 , θ 1 , · · · , θ i such that, if the                 Verifier component). Otherwise, CheckDP uses the counterexample
mechanism is correct, θ i is a privacy proof (i.e, ∀I . M ′ (I, θ i )).                    returned by the verifier to construct Ii (the “Verify Sub-loop” edge).
    Invalidating Input Generation. This component takes a proof                            We note that the verification step is required since KLEE, the sym-
candidate θ i and then tries to find an input Ii such that ¬M ′ (Ii , θ i )                bolic executor that we use to find invalidating inputs, is unsound
(meaning that at least one assertion in M ′ fails).                                        (i.e., it might miss an invalidating input) in theory; however, we did
    Intuitively, θ i is the currently “best” proof candidate (initially,                   not experience any such unsound case of KLEE in our experience.
a default null proof θ 0 = [0, · · · ] is used to bootstrap the process)                       Second, the Proof Generation component might fail to find an
that is able to validate all previously found inputs (I 0 , · · · , Ii−1 ). An             alignment for I 0 , · · · , Ii , a case that will eventually occur for incor-
input Ii , if any, shows that θ i is in fact not a valid proof (recall                     rect mechanisms. This exit edge leads to the invalidate sub-loop
that a proof needs to ensure M ′ (I, θ i ) ∀I ). Hence, we call such Ii                    that we discuss next.
an invaliding input of θ i and feed it with all previously identified
invalidating inputs to the Proof Generation component following                            4.2     Invalidate Sub-Loop
the “Verify Sub-loop” edge.                                                                The invalidate sub-loop involves Counterexample Generation and
    Take GapSVT (Figure 1) for example. Since the initial null proof                       Restart; it is responsible of generating one single invalidating input
θ 0 = [0, · · · ] does not align any random variable, any input, say I 0 ,                 I such that, if the mechanism is incorrect, I cannot be aligned (i.e,
that diverges on the branch q[i] + η 2 ≥ T will trigger an assertion                       θ . M ′ (I, θ )). At first glance, it could be attempting to directly use
                                                                                       9
Ii from the Verify Sub-Loop. However, this is problematic both in                        We also note that it is crucial to consider all invalidating inputs
theory and in practice: no alignment for I 0 , · · · , Ii does not imply no        so far rather than the last input Ii in the Proof Generation compo-
alignment of Ii alone. In practice, we found such a naive approach                 nent: the efficiency of our approach crucially relies on “improving”
fails for BadSmartSum and BadGapSVT in Section 5.                                  the proofs quantified by validating more invalidating inputs. With-
                                                                                   out the improving proofs, the iterative procedure might fail to
    Counterexample Generation. This component takes an invali-
                                                                                   terminate in case shown in Figure 5a: the procedure might repeat
dating input Ii and then tries to find an alignment θ i such that
                                                                                   I 0 , θ 1 , I 1 , θ 2 , I 0 , θ 1 , · · · . This is confirmed in our empirical study.
M ′ (Ii , θ i ) (meaning that Ii is not a counterexample since it can be
aligned by θ i ). For example, consider a corner case in Figure 5a,                    Unknown State. Due to the soundness result (Theorem 3), the
where Proof Generation fails to find a common proof of both I 0                    program being analyzed is verified whenever CheckDP returns with
and I 1 , but each of I 0 and I 1 has a proof (illustrated by the two solid        a proof. Moreover, a validated counterexample by PSI disproves
circles around them). Mostly likely, this occurs when the program                  an incorrect mechanism. However, two reasons might lead to the
being analyzed is incorrect (hence, no common proof) but neither                   “unknown” state in the Figure 4: the generated counterexample
I 1 nor I 2 is a good candidate for counterexample of differential                 is invalid or the Restart component fails to find a new invalidat-
privacy, since each of them can be aligned in isolation.                           ing input. However, for all the correct and incorrect examples we
                                                                                   explored, the unknown state never showed up.
   Restart. This component is symmetric to the Invalidating Input
Generation component in the verify sub-loop: it takes all previously
                                                                                   5     IMPLEMENTATION AND EVALUATION
found proof candidates θ 1 , · · · , θ i and tries to find an invalidating
input Ii+1 such that:                                                              We implemented CheckDP in Python3 . The Program Transforma-
                                                                                   tion phase is implemented as a trans-compiler from CheckDP code
                  ¬M ′ (Ii+1 , θ 1 ) ∧ · · · ¬M ′ (Ii+1 , θ i ).                   (Figure 2) to C code. Following the transformation rules in Fig-
   If found, Ii+1 will intuitively be out of scope of all found proofs             ure 3, the trans-compiler tracks the typing environment, gathers
and serve as a “better” invalidating input. In theory, we can close                the needed constraints for the expressions, and more importantly,
the invalidate sub-loop by feeding Ii+1 back to Counterexample                     instruments corresponding statements when appropriate. More-
Generation. However, doing so will make proof and counterexample                   over, it adds a final assertion assert(vϵ ≤ ϵb ) before each return
generation isolated tasks. Instead, we take an integrated approach,                command, where ϵb is the annotated privacy bound to be checked.
which we discuss shortly, where the verify and invalidate sub-loops                Once all assertions are generated, the trans-compiler generates one
communicate to generate proofs and counterexamples in a more                       alignment template for each sampling instruction as described in
efficient and simultaneous way.                                                    Algorithm 1. For the Proof and Counterexample Generation phase
                                                                                   (i.e., verify-invalidate loop in Section 4), we used an efficient sym-
   Exit Edges. If no θ is found to prove Ii = (inp, inp,   c sample), a            bolic executor KLEE [18] for most tasks. Due to limited support of
counterexample C = (inp, inp + inp,  c M ′ (inp, inp,c sample, θ 0 )) can          unbounded lists in KLEE, we fix the length of lists to be 5 in our
be formed and sent to an external exact probabilistic solver PSI [33]              evaluation. Also, to speed up the search, KLEE is configured to exit
for validation. In theory, the Restart component might fail to find a              once an assertion is hit. We note that the use of KLEE is to discover
new invalidating input given θ 1 , · · · , θ i . However, this “unknown”           alignments and counterexamples, where alignments are eventu-
state never showed up in our experience.                                           ally verified by our sound Verifier component with arbitrary array
                                                                                   length; counterexamples are confirmed by PSI. Moreover, CheckDP
4.3    Integrating Verify and Invalidate Sub-Loops                                 automatically extends the array length until either a verified proof
We integrate the verify and invalidate sub-loops as follows: follow-               or verified counterexample is produced.
ing the “Invalidate Sub-loop” edge of the Proof Generation com-                        Finally, we deploy a verification tool CPAChecker [13] for the
ponent, the latest invalidating input Ii (i.e., the “best” invalidating            Verifier component in CheckDP, which is capable of automatically
input so far) is passed to the Counterexample Generation compo-                    verifying C programs with given configuration (predicateAnalysis
nent to start the invalidate sub-loop. Moreover, the newly generated               is used). Note that CPAChecker is able to generate counterexam-
invalidating input Ii from the Restart component is fed back to the                ples for a failed verification. If the verification fails (which did not
Proof Generation component to start the verify sub-loop.                           happen in our evaluation), CheckDP can feed the counterexample
    We note that by the design of the verify-invalidate loop, it alter-            back to the Proof and Counterexample Generation component.
natively runs Invalidating Input Generation and Proof Generation
components. By doing so, the proof keeps improving while the in-                   5.1      Case Studies
validating inputs are getting closer to a true counterexample (since               Aside from GapSVT, we also evaluate CheckDP on the standard
the most recent one violates a “better” proof). More intuitively,                  benchmark used in previous mechanism verifiers [3, 50, 51] and
consider an invalidating input I 0 as a point in the entire input space,           counterexample generators [14, 23],4 including correct ones such as
illustrated in Figure 5b. A proof candidate θ 1 is able to prove the               NumSVT, PartialSum, and SmartSum, as well as the incorrect vari-
algorithm for a subset of inputs including I 0 (indicated by the circle            ants of SVT reported in [40] and BadPartialSum. To show the power
around I 0 ). The Invalidating Input Generation component then tries
                                                                                   3 Publically available at https://github.com/cmla-psu/checkdp.
to find another invalidating I 1 that violates θ 1 (falls outside of the           4 We note that like all tools designed for privacy mechanisms (e.g., [3, 14, 23, 50, 51]),
θ 1 circle). Next, the Proof Generation component finds better proof               the benchmark do not include iterative programs that are built on those privacy
candidate θ 2 which proves (“covers”) both I 0 and I 1 .                           mechanisms, such as k-means clustering, k-medians, since they are out of scope.
                                                                              10
Table 1: Detected counterexamples for the incorrect algorithms and comparisons with other sampling-based counterexample
detectors. #t stands for true and #f stands for false.
   Mechanism              q                 q′           Extra Args              Output               Iterations    Time(s)        StatDP [23]              DP-Finder [14]        DiPC [4]
  BadNoisyMax      [0, 0, 0, 0, 0]   [−1, 1, 1, 1, 1]         N/A                    0                     3           5.7              11.2                      2561.5            N/A
    BadSVT1        [0, 0, 0, 0, 1]    [1, 1, 1, 1, 0]     T : 0, N : 1    [#f , #f , #f , #f , #t ]        4           3.2              4.9              3847.5 (Semi-Manual)       N/A
    BadSVT2        [0, 0, 0, 0, 1]   [1, 1, 1, 1, −1]     T : 0, N : 1    [#f , #f , #f , #f , #t ]        4           2.0              15.6              4126.1 (Semi-Manual)      N/A
    BadSVT3        [0, 0, 0, 0, 1]   [1, 1, 1, 1, −1]     T : 0, N : 1    [#f , #f , #f , #f , #t ]        4           2.1              9.1              3476.2 (Semi-Manual)       269
   BadGapSVT       [0, 0, 0, 0, 0]   [1, 1, 1, 1, −1]     T : 0, N : 1        [0, 0, 0, 0, 1]              4           5.7              10.6             11611.6 (Semi-Manual)      N/A
 BadAdaptiveSVT    [0, 0, 0, 0, 2]   [1, 1, 1, 1, −1]     T : 0, N : 1       [0, 0, 0, 0, 17]              8          14.2         Search Failed              Search Failed         N/A
  Imprecise SVT    [0, 0, 0, 0, 1]   [1, 1, 1, 1, −1]     T : 0, N : 1    [#f , #f , #f , #f , #t ]        4           8.6         Search Failed              Search Failed         N/A
  BadSmartSum      [0, 0, 0, 0, 0]    [0, 0, 0, 1, 0]     T : 3, M : 4        [0, 0, 0, 0, 0]              4           6.3      22.4 (Semi-Manual)            Search Failed         N/A
  BadPartialSum    [0, 0, 0, 0, 0]    [0, 0, 0, 0, 1]         N/A                    0                     3           3.7              3.8                       1128.5            N/A

Table 2: Alignments found for the correct algorithms. Ω∗ stands for the branch condition in each mechanism, where Ω N M =
q[i] + η > bq ∨ i = 0, ΩSV T = q[i] + η 2 ≥ Tη , ΩT op = q[i] + η 2 − Tη ≥ σ , Ω Middl e = q[i] + η 3 − Tη ≥ 0
                                                             Alignment
       Mechanism                                                                                               Iterations     Time (s)     ShadowDP [50]       Coupling [3]       DiPC [4]
                                     η1                         η2                           η3
    ReportNoisyMax                       q [i] : 0
                              ΩN M ? 1 − b                     N/A                          N/A                    10           69.3            Manual                22             193
       PartialSum                  −
                                    s um                       N/A                          N/A                    2            5.6             Manual                14             N/A
       SmartSum                 −
                                 s um − bq [i]                −bq [i]                       N/A                    6            6.8             Manual               255             N/A
          SVT                         1                 ΩSV T ? 1 − bq [i] : 0              N/A                    4            6.2             Manual               580             825
 Monotone SVT (Increase)              0                 ΩSV T ? 1 − bq [i] : 0              N/A                    8            18.4             N/A                 N/A             N/A
 Monotone SVT (Decrease)              0                  ΩSV T ? −b q [i] : 0               N/A                    8            20.5             N/A                 N/A             N/A
        GapSVT                        1                 ΩSV T ? 1 − bq [i] : 0              N/A                    6            13.5            Manual               N/A             N/A
        NumSVT                        1                    ΩSV T ? 2 : 0                   −bq [i]                 4            8.8             Manual                5              N/A
      AdaptiveSVT                     1                 ΩT op ? 1 − bq [i] : 0                     q [i] : 0
                                                                                  Ω M iddl e ? 1 − b               10           25.6             N/A                 N/A             N/A


of CheckDP and expressiveness of our template generation algo-                                         of queries in an infrequent branch. Details of SmartSum and this
rithm, we also evaluate on a couple of correct/incorrect mechanisms                                    variant can be found in the Appendix.
that, to the best of our knowledge, have not been proved/disproved
                                                                                                          SVT with Wrong Privacy Claims (Imprecise SVT). We also study
by existing verifiers and counterexample generators. This set of
                                                                                                       another interesting yet quite challenging violation of differential
mechanisms include: Sparse Vector with monotonic queries [40],
                                                                                                       privacy: suppose a mechanism satisfies 1.1-differential privacy but
AdaptiveSVT (called Adaptive Sparse Vector with Gap in [24]) as
                                                                                                       claims to be 1-differentially private. This slight violation requires
well as new incorrect variants of SVT, AdaptiveSVT and SmartSum.
                                                                                                       precise reasoning about the privacy cost and poses challenges for
For all mechanisms we explore, CheckDP is able to: (1) provide a
                                                                                                       prior sampling-based approaches. We thus evaluate a variant of SVT,
proof if it satisfies differential privacy, or (2) provide a counterexam-
                                                                                                       referred to as Imprecise SVT, which is ϵ = 1.1-differentially private
ple if it violates the claimed level of privacy. Neither false positives
                                                                                                       but with an incorrect claim of ϵ = 1 (check(1) in the signature).
nor false negatives were observed. In this section, we discuss the
new cases; detailed explanations can be found in the Appendix.
                                                                                                       5.2      Experiments
                                                                                                       We evaluate CheckDP on a Intel® Xeon® E5-2620 v4 CPU machine
   Sparse Vector with Monotonic Queries. The queries in some usages                                    with 64 GB memory. To compare CheckDP with the state-of-the-art
of SVT are monotonic. In such cases, a Lap 2N /ϵ noise (instead of                                     tools, we either directly run tools on the benchmark when they
Lap 4N /ϵ in SVT) is sufficient for ϵ-privacy [40].                                                    are publicly available (including ShadowDP [50], StatDP [23] and
                                                                                                       DP-Finder [14]), or cite the reported results from the corresponding
    AdaptiveSVT, BadAdaptiveSVT and BadSmartSum. Ding et al. [24]                                      papers (including Coupling [3] and DiPC [4]).5 For the latter case,
recently proposed a new variant of SVT which adaptively allocates                                      we note that the numbers are for reference only, due to different
privacy budget, saving privacy cost when noisy query answers are                                       settings, including hardware, used in the experiments.
much larger than the noisy threshold. The difference from standard
                                                                                                           Counterexample Generation. Table 1 lists the counterexamples
(correct) SVT is that it first draws a η 2 := Lap 8N /ϵ noise (instead
                                                                                                       (i.e., a pair of related inputs and a feasible output that witness the
of Lap 4N /ϵ in SVT) and checks if the gap between noisy query and
                                                                                                       violation of claimed level of privacy) automatically generated by
noisy threshold Tη is larger than a preset hyper-parameter σ (if
                                                                                                       CheckDP for the incorrect algorithms. For all incorrect algorithms,
q[i] + η 2 - Tη ≥ σ ). If the test succeeds, the gap is directly returned,
                                                                                                       CheckDP is able to provide a counterexample (validated by PSI [33])
hence costing only ϵ/(8N ) (instead of ϵ/(4N )) privacy budget. Oth-
                                                                                                       in 15 seconds and 8 iterations.6
erwise, it draws η 3 := Lap 4N /ϵ and follows the same procedure
                                                                                                           Notably, both StatDP and DP-Finder fail to find the privacy viola-
as SVT. We also create an incorrect variant called BadAdaptiveSVT.
                                                                                                       tions in BadSmartSum and BadAdaptiveSVT, as well as the violation
It directly releases the noisy query answer instead of the gap after
the first test. Sampling-based methods can have difficulty detecting                                   5 Default settings are used in our evaluation: 100K/500K samples for event selection/hy-

the privacy leakage because the privacy-violating branch of the                                        pothesis testing components of StatDP; 50 iterations for sampling and optimization
                                                                                                       components of DP-Finder where each iteration collects 409,600 samples on average.
BadAdaptiveSVT code is not executed frequently. We also create                                         6 We note that the counterexample of BadSmartSum is validated on a slightly modified
an incorrect variant of SmartSum by releasing a noise-less sum                                         algorithm since PSI does not support modulo operation.
                                                                                                 11
of ϵ = 1-privacy in Imprecise SVT after hours of searching.7 This                          privacy-related checks to later stages. Both changes are important
is due to the limitations of sampling-based approaches. In certain                         for automatically generating proofs and counterexamples.
cases, we can help these sampling-based algorithms by manually                                Besides alignment-based proofs, probabilistic couplings and lift-
providing proper values for the extra arguments that some of the                           ings [3, 7, 9] have also been used in language-based verification
mechanisms require (4t h column of Table 1). This extra advantage                          of differential privacy. Most notably, Albarghouthi and Hsu [3]
(labeled Semi-Manual in the table) sometimes allows the sampling-                          proposed the first automated tool capable of generating coupling
based methods to find counterexamples. We note that CheckDP, in                            proofs for complex mechanisms. Coupling proofs are known to be
contrast, generates all inputs automatically.                                              more general than alignment-based proofs, while alignment-based
                                                                                           proofs are more light-weight. Since CheckDP and [3] are built on
   Verification. Table 2 lists the automatically generated proofs (i.e.,                   different proof techniques, the proof generation algorithm in [3]
alignments) for each random variable in the correct algorithms.                            is not directly applicable in our context. Moreover, [3] does not
Due to the soundness of CheckDP, all returned proofs are valid.                            generate counterexamples and we do not see an obvious way to
We note that correct algorithms on average take more iterations                            extend the Synthesize-Verify loop of [3] to do so .
(and hence, time) to verify; still all of them are verified within 70                         With verified privacy mechanisms, such as SVT and Report Noisy
seconds. . Report Noisy Max is the only example that uses shadow                           Max, we still need to verify that the larger program built on top of
execution; the selector generated is S = q[i] +η 2 ≥ bq ∨i = 0 ? † : ◦,                    them is differentially private. An early line of work [8, 10, 11, 32, 44]
the same as the manually generated one in [50].                                            uses (variations of) relational Hoare logic and linear indexed types
   Performance. We note that all examples finish within 10 itera-                          to derive differential privacy guarantees. For example, Fuzz [44]
tions. We contribute the efficiency to the reduced search space of                         and its successor DFuzz[32] combine linear indexed types and light-
Algorithm 1 (e.g., the alignment template for GapSVT only con-                             weight dependent types to allow rich sensitivity analysis and then
tains 7 “holes”) as well as our novel verify-invalidate loop that                          use the composition theorem to prove overall system privacy. We
allows verification and counterexample generation components                               note that CheckDP and those systems are largely orthogonal: those
to communicate in meaningful ways. Compared with StatDP and                                systems rely on trusted mechanisms (e.g., SVT and Report Noisy
DP-Finder, CheckDP is more efficient on the cases where they do                            Max) without verifying them, while CheckDP is likely less scalable;
find counterexamples. Compared with static tools [3, 4], we note                           they can be combined for sophisticated verification tasks.
that CheckDP is much faster on BadSVT3, SmartSum and SVT. In
summary, CheckDP is mostly more efficient compared to coun-                                   Counterexample Generation. Ding et al. [23] and Bichsel et al.
terexample detectors and automated provers.                                                [14] proposed counterexample generators that rely on sampling –
                                                                                           running an algorithm hundreds of thousands of times to estimate
6    RELATED WORK                                                                          the output distribution of mechanisms (this information is then
    Proving and Disproving Differential Privacy. Concurrent works [4,                      used to find counterexamples). The strength of these methods is
30] also target both proving and disproving differential privacy.                          that they do not rely on external solvers, and more importantly, they
Barthe et al. [4] identify a non-trivial class of programs where                           are not tied to (the limitation of) any particular proof technique
checking differential privacy is decidable. Their work also supports                       (e.g., randomness alignment and coupling). However, sampling also
approximate differential privacy. However, the decidable programs                          make the counterexample detectors imprecise and more likely to
only allow finite inputs and outputs, while CheckDP is applicable to                       fail in some cases, as confirmed in the evaluation.
a larger class of programs. Moreover, CheckDP is more scalable, as
observed in our evaluation. Farina [30] builds a relational symbolic                       7    CONCLUSIONS AND FUTURE WORK
execution framework, which when combined with probabilistic
                                                                                           We proposed CheckDP, an integrated tool based on static analysis
couplings, is able to prove differential privacy or generate failing
                                                                                           for automatically proving or disproving that a mechanism satisfies
traces for SVT and its two incorrect variants. However, it is unclear
                                                                                           differential privacy. Evaluation shows that CheckDP is able to pro-
if the employed heuristic strategies work on other mechanisms,
                                                                                           vide proofs for a number of algorithms, as well as counterexamples
such as Report Noisy Max. Moreover, CheckDP is likely to be more
                                                                                           for their incorrect variants within 2 to 70 seconds. Moreover, all
scalable since their approach treats both program inputs and proofs
                                                                                           generated proofs and counterexamples are validated.
in a symbolic way, whereas in the novel verify-invalidate loop of
                                                                                              For future work, CheckDP relies on the underlying randomness
CheckDP, either program inputs or proofs are concrete.
                                                                                           alignment technique; hence it is subject to its limitations, including
   Formal Verification of Differential Privacy. From the verification                      lack of support for (ϵ, δ )-differential privacy and renyi differential
perspective, CheckDP is mostly related to LightDP [51] and Shad-                           privacy [43]. We plan to extend the underlying proof technique for
owDP [50] – all use randomness alignment. The type system of                               other variants of differential privacy.
CheckDP is directly inspired by that of [50, 51]. However, the most                           Moreover, subtle mechanisms such as PrivTree [52] and private
important difference is that CheckDP is the first that automati-                           selection [39], where the costs of intermediate results are dependent
cally generates alignment-based proofs; both LightDP and Shad-                             on the data but the cost of sum is data-independent, is still out of
owDP assume manually-provided proofs. As discussed in Section 3,                           reach for formal verification (including CheckDP).
CheckDP also simplifies the previous type systems and defers all                              Finally, CheckDP is designed for DP mechanisms, rather than
                                                                                           larger programs built on top of them. An interesting area of future
7 For StatDP, we use 1000X of the default number of samples to confirm the failure.        work is integrating CheckDP with tools like DFuzz [32], which are
                                                                                      12
more efficient on programs built on top of DP mechanisms (but                                  [17] U. S. Census Bureau. 2019. On The Map: Longitudinal Employer-Household
don’t verify the mechanisms themselves).                                                            Dynamics.        https://lehd.ces.census.gov/applications/help/onthemap.html#
                                                                                                    !confidentiality_protection
                                                                                               [18] Cristian Cadar, Daniel Dunbar, and Dawson Engler. 2008. KLEE: Unassisted and
ACKNOWLEDGMENTS                                                                                     Automatic Generation of High-coverage Tests for Complex Systems Programs.
                                                                                                    In Proceedings of the 8th USENIX Conference on Operating Systems Design and
We thank the anonymous reviewers for their insightful feedbacks.                                    Implementation (San Diego, California) (OSDI’08). USENIX Association, Berkeley,
This work was supported by NSF Awards CNS-1702760.                                                  CA, USA, 209–224. http://dl.acm.org/citation.cfm?id=1855741.1855756
                                                                                               [19] T.-H. Hubert Chan, Elaine Shi, and Dawn Song. 2011. Private and Continual
                                                                                                    Release of Statistics. ACM Trans. Inf. Syst. Secur. 14, 3, Article 26 (Nov. 2011),
REFERENCES                                                                                          24 pages.
 [1] John M. Abowd. 2018. The U.S. Census Bureau Adopts Differential Privacy.                  [20] Rui Chen, Qian Xiao, Yu Zhang, and Jianliang Xu. 2015. Differentially Private
     In Proceedings of the 24th ACM SIGKDD International Conference on Knowledge                    High-Dimensional Data Publication via Sampling-Based Inference. In Proceedings
     Discovery and Data Mining (London, United Kingdom) (KDD ’18). ACM, New                         of the 21th ACM SIGKDD International Conference on Knowledge Discovery and
     York, NY, USA, 2867–2867.                                                                      Data Mining (Sydney, NSW, Australia) (KDD ’15). ACM, New York, NY, USA,
 [2] Alfred V Aho, Ravi Sethi, and Jeffrey D Ullman. 1986. Compilers, principles,                   129–138. https://doi.org/10.1145/2783258.2783379
     techniques. Addison wesley 7, 8 (1986), 9.                                                [21] Yan Chen and Ashwin Machanavajjhala. 2015. On the Privacy Properties of
 [3] Aws Albarghouthi and Justin Hsu. 2017. Synthesizing Coupling Proofs of Differ-                 Variants on the Sparse Vector Technique. http://arxiv.org/abs/1508.07306.
     ential Privacy. Proceedings of ACM Programming Languages 2, POPL, Article 58              [22] Bolin Ding, Janardhan Kulkarni, and Sergey Yekhanin. 2017. Collecting Telemetry
     (Dec. 2017), 30 pages.                                                                         Data Privately. In Proceedings of the 31st International Conference on Neural
 [4] Gilles Barthe, Rohit Chadha, Vishal Jagannath, A. Prasad Sistla, and Mahesh                    Information Processing Systems (Long Beach, California, USA) (NIPS’17). Curran
     Viswanathan. 2020. Deciding Differential Privacy for Programs with Finite                      Associates Inc., USA, 3574–3583. http://dl.acm.org/citation.cfm?id=3294996.
     Inputs and Outputs. In Proceedings of the 35th Annual ACM/IEEE Symposium on                    3295115
     Logic in Computer Science (Saarbrücken, Germany) (LICS ’20). Association for              [23] Zeyu Ding, Yuxin Wang, Guanhong Wang, Danfeng Zhang, and Daniel Kifer.
     Computing Machinery, New York, NY, USA, 141–154. https://doi.org/10.1145/                      2018. Detecting Violations of Differential Privacy. In Proceedings of the 2018 ACM
     3373718.3394796                                                                                SIGSAC Conference on Computer and Communications Security (Toronto, Canada)
 [5] Gilles Barthe, George Danezis, Benjamin Gregoire, Cesar Kunz, and Santiago                     (CCS ’18). ACM, New York, NY, USA, 475–489.
     Zanella-Beguelin. 2013. Verified Computational Differential Privacy with Appli-           [24] Zeyu Ding, Yuxin Wang, Danfeng Zhang, and Daniel Kifer. 2019. Free Gap Infor-
     cations to Smart Metering. In Proceedings of the 2013 IEEE 26th Computer Security              mation from the Differentially Private Sparse Vector and Noisy Max Mechanisms.
     Foundations Symposium (CSF ’13). IEEE Computer Society, Washington, DC, USA,                   PVLDB 13, 3 (2019), 293–306. https://doi.org/10.14778/3368289.3368295
     287–301.                                                                                  [25] Cynthia Dwork. 2006. Differential Privacy. In Proceedings of the 33rd International
 [6] Gilles Barthe, Pedro R. D’Argenio, and Tamara Rezk. 2004. Secure Information                   Conference on Automata, Languages and Programming - Volume Part II (Venice,
     Flow by Self-Composition. In Proceedings of the 17th IEEE Workshop on Computer                 Italy) (ICALP’06). Springer-Verlag, Berlin, Heidelberg, 1–12. https://doi.org/10.
     Security Foundations (CSFW ’04). IEEE Computer Society, Washington, DC, USA,                   1007/11787006_1
     100–.                                                                                     [26] Cynthia Dwork, Krishnaram Kenthapadi, Frank McSherry, Ilya Mironov, and
 [7] Gilles Barthe, Noémie Fong, Marco Gaboardi, Benjamin Grégoire, Justin Hsu,                     Moni Naor. 2006. Our Data, Ourselves: Privacy via Distributed Noise Generation.
     and Pierre-Yves Strub. 2016. Advanced Probabilistic Couplings for Differential                 In Proceedings of the 24th Annual International Conference on The Theory and
     Privacy. In Proceedings of the 2016 ACM SIGSAC Conference on Computer and                      Applications of Cryptographic Techniques (St. Petersburg, Russia) (EUROCRYPT’06).
     Communications Security (Vienna, Austria) (CCS ’16). ACM, New York, NY, USA,                   Springer-Verlag, Berlin, Heidelberg, 486–503.
     55–67.                                                                                    [27] Cynthia Dwork, Frank McSherry, Kobbi Nissim, and Adam Smith. 2006. Cali-
 [8] Gilles Barthe, Marco Gaboardi, Emilio Jesús Gallego Arias, Justin Hsu, César                   brating Noise to Sensitivity in Private Data Analysis. In Theory of Cryptography,
     Kunz, and Pierre-Yves Strub. 2014. Proving Differential Privacy in Hoare Logic.                Shai Halevi and Tal Rabin (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg,
     In Proceedings of the 2014 IEEE 27th Computer Security Foundations Symposium                   265–284.
     (CSF ’14). IEEE Computer Society, Washington, DC, USA, 411–424.                           [28] Cynthia Dwork, Aaron Roth, et al. 2014. The algorithmic foundations of differ-
 [9] Gilles Barthe, Marco Gaboardi, Benjamin Grégoire, Justin Hsu, and Pierre-Yves                  ential privacy. Theoretical Computer Science 9, 3–4 (2014), 211–407.
     Strub. 2016. Proving Differential Privacy via Probabilistic Couplings. In Proceed-        [29] Úlfar Erlingsson, Vasyl Pihur, and Aleksandra Korolova. 2014. RAPPOR: Ran-
     ings of the 31st Annual ACM/IEEE Symposium on Logic in Computer Science (New                   domized Aggregatable Privacy-Preserving Ordinal Response. In Proceedings of
     York, NY, USA) (LICS ’16). ACM, New York, NY, USA, 749–758.                                    the 2014 ACM SIGSAC Conference on Computer and Communications Security
[10] Gilles Barthe, Boris Köpf, Federico Olmedo, and Santiago Zanella Béguelin. 2012.               (Scottsdale, Arizona, USA) (CCS ’14). ACM, New York, NY, USA, 1054–1067.
     Probabilistic Relational Reasoning for Differential Privacy. In Proceedings of the        [30] Gian Pietro Farina. 2020. Coupled Relational Symbolic Execution. Ph.D. Disserta-
     39th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming                          tion. State University of New York at Buffalo.
     Languages (Philadelphia, PA, USA) (POPL ’12). ACM, New York, NY, USA, 97–110.             [31] Jeanne Ferrante, Karl J Ottenstein, and Joe D Warren. 1987. The program de-
[11] Gilles Barthe and Federico Olmedo. 2013. Beyond Differential Privacy: Compo-                   pendence graph and its use in optimization. ACM Transactions on Programming
     sition Theorems and Relational Logic for f-divergences Between Probabilistic                   Languages and Systems (TOPLAS) 9, 3 (1987), 319–349.
     Programs. In Proceedings of the 40th International Conference on Automata, Lan-           [32] Marco Gaboardi, Andreas Haeberlen, Justin Hsu, Arjun Narayan, and Benjamin C.
     guages, and Programming - Volume Part II (Riga, Latvia) (ICALP’13). Springer-                  Pierce. 2013. Linear Dependent Types for Differential Privacy. In Proceedings of
     Verlag, Berlin, Heidelberg, 49–60.                                                             the 40th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming
[12] Jean-Francois Bergeretti and Bernard A. Carré. 1985. Information-flow and Data-                Languages (Rome, Italy) (POPL ’13). ACM, New York, NY, USA, 357–370. https:
     flow Analysis of While-programs. ACM Trans. Program. Lang. Syst. 7, 1 (Jan.                    //doi.org/10.1145/2429069.2429113
     1985), 37–61. https://doi.org/10.1145/2363.2366                                           [33] Timon Gehr, Sasa Misailovic, and Martin Vechev. 2016. PSI: Exact Symbolic
[13] Dirk Beyer and M. Erkan Keremoglu. 2011. CPACHECKER: A Tool for Config-                        Inference for Probabilistic Programs. In Computer Aided Verification, Swarat
     urable Software Verification. In Proceedings of the 23rd International Conference              Chaudhuri and Azadeh Farzan (Eds.). Springer International Publishing, Cham,
     on Computer Aided Verification (Snowbird, UT) (CAV’11). Springer-Verlag, Berlin,               62–83.
     Heidelberg, 184–190.                                                                      [34] Anna Gilbert and Audra McMillan. 2018. Property Testing for Differential Privacy.
[14] Benjamin Bichsel, Timon Gehr, Dana Drachsler-Cohen, Petar Tsankov, and Martin                  arXiv:1806.06427 [cs.CR]
     Vechev. 2018. DP-Finder: Finding Differential Privacy Violations by Sampling and          [35] Samuel Haney, Ashwin Machanavajjhala, John M. Abowd, Matthew Graham,
     Optimization. In Proceedings of the 2018 ACM SIGSAC Conference on Computer                     Mark Kutzbach, and Lars Vilhuber. 2017. Utility Cost of Formal Privacy for
     and Communications Security (Toronto, Canada) (CCS ’18). ACM, New York, NY,                    Releasing National Employer-Employee Statistics. In Proceedings of the 2017
     USA, 508–524.                                                                                  ACM International Conference on Management of Data (Chicago, Illinois, USA)
[15] Andrea Bittau, Úlfar Erlingsson, Petros Maniatis, Ilya Mironov, Ananth Raghu-                  (SIGMOD ’17). ACM, New York, NY, USA, 1339–1354. https://doi.org/10.1145/
     nathan, David Lie, Mitch Rudominer, Ushasree Kode, Julien Tinnes, and Bernhard                 3035918.3035940
     Seefeld. 2017. Prochlo: Strong Privacy for Analytics in the Crowd. In Proceedings         [36] Noah Johnson, Joseph P Near, and Dawn Song. 2018. Towards practical differential
     of the 26th Symposium on Operating Systems Principles (Shanghai, China) (SOSP                  privacy for SQL queries. Proceedings of the VLDB Endowment 11, 5 (2018), 526–
     ’17). ACM, New York, NY, USA, 441–459. https://doi.org/10.1145/3132747.3132769                 539.
[16] Mark Bun and Thomas Steinke. 2016. Concentrated Differential Privacy: Sim-                [37] Dexter Kozen. 1981. Semantics of probabilistic programs. J. Comput. System Sci.
     plifications, Extensions, and Lower Bounds. In Proceedings, Part I, of the 14th                22, 3 (1981), 328 – 350.
     International Conference on Theory of Cryptography - Volume 9985. Springer-Verlag         [38] Jaewoo Lee and Christopher W. Clifton. 2014. Top-k Frequent Itemsets via Dif-
     New York, Inc., New York, NY, USA, 635–658.                                                    ferentially Private FP-trees. In Proceedings of the 20th ACM SIGKDD International
                                                                                          13
     Conference on Knowledge Discovery and Data Mining (New York, New York, USA)               [46] Armando Solar-Lezama, Liviu Tancau, Rastislav Bodik, Sanjit Seshia, and Vijay
     (KDD ’14). ACM, New York, NY, USA, 931–940. https://doi.org/10.1145/2623330.                   Saraswat. 2006. Combinatorial Sketching for Finite Programs. In Proceedings of the
     2623723                                                                                        12th International Conference on Architectural Support for Programming Languages
[39] Jingcheng Liu and Kunal Talwar. 2019. Private Selection from Private Candidates.               and Operating Systems (San Jose, California, USA) (ASPLOS XII). Association for
     In Proceedings of the 51st Annual ACM SIGACT Symposium on Theory of Computing                  Computing Machinery, New York, NY, USA, 404–415. https://doi.org/10.1145/
     (Phoenix, AZ, USA) (STOC 2019). Association for Computing Machinery, New                       1168857.1168907
     York, NY, USA, 298–309. https://doi.org/10.1145/3313276.3316377                           [47] Ben Stoddard, Yan Chen, and Ashwin Machanavajjhala. 2014. Differentially
[40] Min Lyu, Dong Su, and Ninghui Li. 2017. Understanding the sparse vector                        Private Algorithms for Empirical Machine Learning. arXiv:1411.5428 [cs.LG]
     technique for differential privacy. Proceedings of the VLDB Endowment 10, 6               [48] Apple Differential Privacy Team. 2017. Learning with Privacy at Scale. https:
     (2017), 637–648.                                                                               //machinelearning.apple.com/2017/12/06/learning-with-privacy-at-scale.html
[41] A. Machanavajjhala, D. Kifer, J. Abowd, J. Gehrke, and L. Vilhuber. 2008. Privacy:        [49] Tachio Terauchi and Alex Aiken. 2005. Secure information flow as a safety
     Theory meets Practice on the Map. In 2008 IEEE 24th International Conference on                problem. In International Static Analysis Symposium. Springer, 352–367.
     Data Engineering. IEEE, Piscataway, NJ, USA, 277–286. https://doi.org/10.1109/            [50] Yuxin Wang, Zeyu Ding, Guanhong Wang, Daniel Kifer, and Danfeng Zhang. 2019.
     ICDE.2008.4497436                                                                              Proving Differential Privacy with Shadow Execution. In Proceedings of the 40th
[42] Frank McSherry. 2018. Uber’s differential privacy .. probably isn’t. https:                    ACM SIGPLAN Conference on Programming Language Design and Implementation
     //github.com/frankmcsherry/blog/blob/master/posts/2018-02-25.md (retrieved                     (Phoenix, AZ, USA) (PLDI 2019). ACM, New York, NY, USA, 655–669. https:
     11/15/2019).                                                                                   //doi.org/10.1145/3314221.3314619
[43] I. Mironov. 2017. Rényi Differential Privacy. In 2017 IEEE 30th Computer Security         [51] Danfeng Zhang and Daniel Kifer. 2017. LightDP: Towards Automating Differential
     Foundations Symposium (CSF). IEEE, Piscataway, NJ, USA, 263–275. https://doi.                  Privacy Proofs. In Proceedings of the 44th ACM SIGPLAN Symposium on Principles
     org/10.1109/CSF.2017.11                                                                        of Programming Languages (Paris, France) (POPL 2017). ACM, New York, NY,
[44] Jason Reed and Benjamin C. Pierce. 2010. Distance Makes the Types Grow                         USA, 888–901.
     Stronger: A Calculus for Differential Privacy. In Proceedings of the 15th ACM SIG-        [52] Jun Zhang, Xiaokui Xiao, and Xing Xie. 2016. PrivTree: A Differentially Private
     PLAN International Conference on Functional Programming (Baltimore, Maryland,                  Algorithm for Hierarchical Decompositions. In Proceedings of the 2016 Interna-
     USA) (ICFP ’10). ACM, New York, NY, USA, 157–168. https://doi.org/10.1145/                     tional Conference on Management of Data (San Francisco, California, USA) (SIG-
     1863543.1863568                                                                                MOD ’16). Association for Computing Machinery, New York, NY, USA, 155–170.
[45] Aaron Roth. 2011. The Sparse Vector Technique. http://www.cis.upenn.edu/                       https://doi.org/10.1145/2882903.2882928
     ~aaroth/courses/slides/Lecture11.pdf.




                                                                                          14
A    CHECKDP SEMANTICS                                                         that the branch at Line 26 is not affected by the new assignment of
Let A be a discrete set. The set of sub-distributions over A, writ-            bq.
ten Dist(A), to be the set of functions µ : A → [0, 1] such that
                                                                                       Lr, ΓM⋆ = r         Ltrue, ΓM⋆ = true             Lfalse, ΓM⋆ = false
  a ∈A µ(a) ≤ 1. The reasonÍto use sub-distributions instead of distri-
Í
butions (those µ such that a ∈A µ(a) = 1) is that sub-distributions
                                                                                                                     x + n†   , if Γ ⊢ x : num ⟨n◦, n† ⟩
                                                                                                                 
give rise to an elegant semantics for programs that do not nec-                                Lx, ΓM⋆ =
                                                                                                                     x        , else
essarily terminate [37]. We use 1a to represent the degenerate
distribution µ that µ(a) = 1 and µ(a ′ ) = 0 if a ′ , a. Moreover, we                Le 1 op e 2, ΓM⋆ = Le 1, ΓM⋆ op Le 2, ΓM⋆ where op = ⊕ ∪ ⊗ ∪ ⊙
define monadic functions unit and bind functions to formalize the                                          
semantics for commands:                                                               Le 1 [e 2 ], ΓM⋆ =       e 1 [e 2 ] + eb1 † [e 2 ] , if Γ † ⊢ e 1 : list num∗
                                                                                                               e 1 [e 2 ]                , else
           unit : A → Dist(A) ≜ λa. 1a
           bind : Dist(A) → (A → Dist(B)) → Dist(B)                                Le 1 :: e 2, ΓM⋆ = Le 1, ΓM⋆ :: Le 2, ΓM⋆                   L¬e, ΓM⋆ = ¬Le, ΓM⋆

                                                                                             Le 1 ? e 2 : e 3, ΓM⋆ = Le 1 M⋆ ? Le 2, ΓM⋆ : Le 3, ΓM⋆
                                 Õ
                ≜ λµ. λ f . (λb.   (f a b) × µ(a))
                                  a ∈A
That is, unit takes an element in A and returns the Dirac distribu-                                                           Lc 1 ; ΓM⋆ = c 1′       Lc 2 ; ΓM⋆ = c 2′
tion where all mass is assigned to a; bind takes µ, a distribution on                  Lskip, ΓM⋆ = skip
                                                                                                                                      Lc 1 ; c 2, ΓM⋆ = c 1′ ; c 2′
A, and f , a mapping from A to distributions on B (e.g., a conditional
distribution of B given A), and returns the corresponding marginal                                  Lx := e, ΓM⋆ = (b
                                                                                                                    x † := Le, ΓM⋆ − x )
distribution on B. This monadic view avoids cluttered definitions
and proofs when probabilistic programs are involved.                                                        Lc i , ΓM⋆ = c i′     i ∈ {1, 2}
                                                                                       Lif e then c 1 else c 2, ΓM⋆ = if Le, ΓM⋆ then c 1′ else c 2′
B    SHADOW EXECUTION
                                                                                                              Lc, ΓM⋆ = c ′
We show how to extend the program transformation in Figure 3
to support shadow execution. At a high level, the extension en-                                 Lwhile e do c, ΓM⋆ = while Le, ΓM⋆ do c ′
codes the selectors (which requires manual annotations in Shad-
owDP [50]) and integrates them with the generated templates. With              Figure 6: Transformation of expressions and commands for
the extra “holes” in the templates, the verify-invalidate loop will au-        aligned and shadow execution, where ⋆ ∈ {◦, †}.
tomatically find alignments (including selectors)/counterexamples.
The complete set of transformation rules with shadow execution is                  As previously explained, a separate shadow branch / loop has
shown in Figure 7, where the extensions are highlighted in gray.               to be generated to correctly track the shadow distances of the
                                                                               variables. More specifically, Rules (T-If) and (T-While) is extended
   Syntax and Expressions. Since a new shadow execution is tracked,
                                                                               to include an extra shadow execution command c † when pc transits
types for each variable would be expanded to include a pair of dis-
                                                                               from ⊥ to ⊤. The shadow execution is constructed by an auxiliary
tances ⟨d◦ , d† ⟩. More specifically, the types should now be defined
                                                                               function Lc, ΓM† , as defined in Figure 6, which is the same as the
as: τ ::= num ⟨d◦, d† ⟩ | bool | list τ .
                                                                               ones in ShadowDP [50]. It essentially replaces each variable with
   With the modified types, corresponding modifications to the
transformation rules for expressions are straightforward and mini-                                                         x † ), as is standard in self-
                                                                               its correspondence (e.g., variable x to x + b
mal: the handling of shadow distances are essentially the same as              composition [6, 49]. Note that the value of an expression e in an
that of aligned distances.                                                     aligned execution (i.e., Le, ΓM◦ used in Rules (T-If) and (T-While))
                                                                               are defined in a similar way.
   Normal Commands. Following the type system of ShadowDP,
a program counter pc ∈ {⊤, ⊥} is introduced to each transforma-                   Sampling Commands. The most interesting rule is (T-Laplace).
tion rule for commands to capture potential divergence of shadow               In order to enable the automatic discovery of the selectors, our
execution. Specifically, pc ⊢ c ⇀ c ′ . pc = ⊤ (resp. ⊥) means that            GenerateTemplate algorithm needs to be extended to return a
the branch / loop command might diverge in the shadow execu-                   selector template S. Intuitively, a selector expression S with the
tion (resp. must stay the same). The value of pc is used to guide              following syntax decides if the aligned or shadow execution is
how each rule should handle the shadow distances (e.g., (T-Asgn)),             picked:
which we will explain shortly. Therefore, another auxiliary function                          Var Versions               k       ∈      {◦, †}
updatePC is added to track the value of pc.                                                   Selectors                  S      ::=     e ? S1 : S2 | k
   Compared with the type system of ShadowDP, the first major                     The definition of the selector template is then similar to the
difference is in (T-Asgn). If pc = ⊥, shadow distances are handled             alignment template, where the value can depend on the branch
as the aligned distances. However, when pc = ⊤ (shadow execution               conditions:
diverges), it updates the shadow distance of the variable to make                           (
                                                                                              e 0 ? SE\{e0 } : SE\{e0 } , when E = {e 0 , · · · }
                                             x † ) remains the same af-
sure the value in shadow execution (i.e., x +b                                       SE ::=
ter the assignment. For example, Line 20 in Figure 8 is instrumented                          θ with fresh θ , otherwise
                                                                 †
to maintain the value of bq in the shadow execution (bq + c    bq ), so
                                                                          15
Transformation rules for expressions with form Γ ⊢ e : B⟨n◦, n† ⟩
                                                                                                                                                       Γ ⊢ e : bool | C
                                                    (T-Num)                                                      (T-Boolean)                                            (T-Neg)
                Γ ⊢ r : num ⟨0, 0⟩ | true                                       Γ ⊢ b : bool | true                                                   Γ ⊢ ¬e : bool | C
                                                                                        ⋆
                                                         Γ(x ) = B⟨d◦, d† ⟩      n⋆ = b x  if d⋆ = ∗                      ⋆ ∈ {◦, †}
                                                                                        0  otherwise
                                                                                                                                          (T-Var)
                                                                              Γ ⊢ x : B ◦ † | true
                                                                                            ⟨n , n ⟩

                                                                                                       Γ ⊢ e 1 : num ⟨n1, n2 ⟩ | C1         Γ ⊢ e 2 : num ⟨n3, n4 ⟩ | C2
             Γ ⊢ e 1 : num ⟨n1, n2 ⟩ | C1           Γ ⊢ e 2 : num ⟨n3, n4 ⟩ | C2                                                                                            (T-OTimes)
                                                                                   (T-OPlus)                                                       (n = n =
                  Γ ⊢ e 1 ⊕ e 2 : num ⟨n1 ⊕n3, n2 ⊕n4 ⟩ | C1 ∧ C2                                          Γ ⊢ e 1 ⊗ e 2 : num ⟨0, 0⟩ | C1 ∧ C2 ∧ n 1= n 2= 0)
                                                                                                                                                           3      4

                                                             Γ ⊢ e 1 : num ⟨n1, n2 ⟩ | C1       Γ ⊢ e 2 : num ⟨n3, n4 ⟩ | C2
                                                                                                                                                                      (T-ODot)
                      Γ ⊢ e 1 ⊙ e 2 : bool | C1 ∧ C2 ∧ (e 1 ⊙ e 2 ) ⇔ (e 1 + n1 ) ⊙ (e 2 + n3 )∧(e 1 ⊙ e 2 ) ⇔ (e 1 + n2 ) ⊙ (e 2 + n4 )

               Γ ⊢ e 1 : B⟨n1, n2 ⟩ | C1            Γ ⊢ e 2 : list B⟨n3, n4 ⟩ | C2                                      Γ ⊢ e 1 : list τ | C1         Γ ⊢ e 2 : num ⟨n1, n2 ⟩ | C2
                                                                                                   (T-Cons)                                                                          (T-Index)
        Γ ⊢ e 1 :: e 2 : list B⟨n3, n4 ⟩ | C1 ∧ C2 ∧ (n1 = n2 = n3 = n4 = 0)                                                Γ ⊢ e 1 [e 2 ] : τ | C1 ∧ C2 ∧ (n1 = n2 = 0)

                                               Γ ⊢ e 1 : bool | C1      Γ ⊢ e 2 : B⟨n1, n2 ⟩ | C2 Γ ⊢ e 3 : B⟨n3, n4 ⟩ | C3
                                                                                                                            (T-Select)
                                                Γ ⊢ e 1 ? e 2 : e 3 : B⟨n1, n2 ⟩ | C1 ∧ C2 ∧ C3 ∧ (n1 = n2 = n3 = n4 )
 Transformation rules for commands with form pc ⊢ Γ {c ⇀ c ′ } Γ′

                                                        (
                                                                                                                  ⟨0, skip,
                                                                                                                             skip⟩,      if pc = ⊥ ∧ n† = 0
                                                                         if n◦ == 0,
                                                                                                                 
                                                            ⟨0, skip⟩,
                                                                                                                 
        Γ⊢e : B                          ◦
                                      ⟨d , c ⟩ =◦                                                      †    †     ′
                                                                                                   ⟨d , c , c ⟩ = ⟨∗, b  †
                                                                                                                           := n , skip⟩, if pc = ⊥ ∧ n† , 0
                                                                                                                                †
                                                                                                                 
                               | C                               ◦                                                     x
                  ⟨n◦ , n† ⟩                                    x := n ⟩, otherwise
                                                            ⟨∗, b      ◦
                                                                                                                                †
                                                                                                                                  := x + n† − e ⟩, otherwise
                                                                                                                 
                                                                                                                  ⟨∗, skip, b
                                                                                                                             x
                                                                                                                                                                                     (T-Asgn)
                                                                                                                 
                                                pc ⊢ Γ {x := e ⇀ assert(C); c ′ ; x := e; c ◦ ; c † } Γ[x 7→ B⟨d◦, d† ⟩ ]
                         pc ⊢ Γ {c 1 ⇀ c 1′ } Γ1             pc ⊢ Γ1 {c 2 ⇀ c 2′ } Γ2
                                                                                        (T-Seq)                                                                       (T-Skip)
                                       pc ⊢ Γ {c 1 ; c 2 ⇀ c 1′ ; c 2′ } Γ2                                                      pc ⊢ Γ {skip ⇀ skip} Γ

                                                                              Γ ⊢ e : B⟨n◦, n† ⟩ | C
                                                                                                   (T-Return)
                                           pc ⊢ Γ {return e ⇀ assert(C ∧ n◦ = 0); return e } Γ
                                                                                 (
                           pc ⊢ Γ ⊔ Γf {c ⇀ c ′ } Γf Γ, Γ ⊔ Γf , pc ′ ⇛ c s   †    skip,   if (pc = ⊤ ∨ pc ′ = ⊥)
                                                                          ′′ c =
                             ′
                           pc = updatePC(pc, Γ, e) f Γ , Γ ⊔ Γf , pc  ⇛ c          Lwhile e do c, Γ ⊔ Γf M†,  else
                                                                                                                                                                (T-While)
                                      pc ⊢ Γ {while e do c ⇀ c s ; (while e do (assert(Le, ΓM◦ ); c ′ ; c ′′ )); c † } Γ ⊔ Γf
                                                                                                                   (
                                                              pc ′ = updatePC(pc, Γ, e)                                skip,    if (pc = ⊤ ∨ pc ′ = ⊥)
                     pc ⊢ Γ {c i ⇀ c i′ } Γi                                                                †
                                                                                                           c =
                                                        Γi , Γ1 ⊔ Γ2, pc ′ ⇛ c i′′ i ∈ {1, 2}                          Lif e then c 1 else c 2, Γ1 ⊔ Γ2 M†, else
                                                                                                                                                                                 (T-If)
                pc ⊢ Γ {if e then c 1 else c 2 ⇀ (if e then (assert(Le, ΓM◦ ); c 1′ ; c 1′′ ) else (assert(¬Le, ΓM◦ ); c 2′ ; c 2′′ )); c † } Γ1 ⊔ Γ2

                         A, S = GenerateTemplate(Γ, All Assertions)                                                    x ◦ := 0 | Γ′ (x ) = num ⟨∗, d† ⟩ ∧ Γ(x ) = num ⟨0, d† ⟩ }
                                                                                                                c ′ = {b
    pc = ⊥       c a = assert(((η + A){η 1 /η } = (η + A){η 2 /η } ⇒ η 1 = η 2 ))                                         c ′′ = {bx ◦ := n† | Γ′ ⊢ x : num ⟨−, n† ⟩ }
                        Γ′ = λx . ⟨d◦ ⊔ d†, d† ⟩ where Γ(x ) = num ⟨d◦, d† ⟩                                                   c d = (if S then c ′ else c ′′ )
                                                                                                                                                                                      (T-Laplace)
        pc ⊢ Γ {η := Lap r ⇀ c a ; η := sampl e[idx ]; idx := idx + 1; vϵ := (S ? vϵ : 0) + | A |/r ; b
                                                                                                      η := A; c d } Γ′ [η 7→ num ⟨∗, 0⟩ ]

Transformation rules for merging environments
                                                                                                                                          (
                                                           x ◦ := 0 | Γ1 (x ) = num ⟨0, d1 ⟩ ∧ Γ2 (x ) = num ⟨∗, d2 ⟩ }
                                                    c ◦ = {b                                                                               c ◦; c †     if pc = ⊥
                                                                                                                                   c′ =
                                     Γ1 ⊑ Γ2
                                                      †
                                                    c = {b x † := 0 | Γ1 (x ) = num ⟨d1, 0⟩ ∧ Γ2 (x ) = num ⟨d2, ∗⟩ }                      c◦           if pc = ⊤
                                                                                        Γ1, Γ2, pc ⇛ c ′

 PC update function                                                                         (
                                                                                                ⊥ , if pc = ⊥ ∧ Γ ⊢ e : num ⟨−, 0⟩
                                                              updatePC(pc, Γ, e) =
                                                                                                ⊤ , else

Figure 7: Rules for transforming probabilistic programs into deterministic ones with shadow execution extension. Differences
that shadow execution introduce are marked in gray boxes.

                                                                                                    16
   Compared with other holes (θ ) in the alignment template (AE ),             distances), as long as Γ is consistent with Γ̃. We list a few interesting
the only difference is that θ in SE has Boolean values representing            cases here. The proofs for other types of expressions are omitted
whether to stay on aligned execution (◦), or switch to shadow                  since their rules in CheckDP are identical other than collecting
execution (†).                                                                 static checks in ShadowDP as constraints.
   To embed shadow execution into CheckDP, the type system                       • e = x: the interesting case is when Γ(x) = B ⟨∗,∗⟩ and Γ̃(x) =
dynamically instruments an auxiliary command (c d ) according to                   B ⟨n1, n2 ⟩ . We have the derived types are equivalent under Γ and
the selector template S. Once a switch is made (S = †), the distances              Γ̃ by the consistency assumption.
of all variables are replaced with their shadow versions by this                 • e = e 1 ?e 2 : e 3 . Let e 2 , e 3 be such that Γ ⊢ e 2 : num ⟨n1, n2 ⟩ , Γ ⊢ e 3 :
command. Moreover, the privacy cost vϵ will also be properly reset                 num ⟨n3, n4 ⟩ . The T-Select rule restricts that n1 = n2 = n3 = n4 ,
according to the selector.                                                         which entails the requirement that e 2 and e 3 have the same
                                                                                   type in the corresponding rule of ShadowDP.
C    SOUNDNESS PROOF                                                           Next, we show that if Γ is consistent with Γ̃ and ⊢ Γ {M ⇀ M ′ } Γ ′ ,
CheckDP’s alignment-based proof system is built on that of Shad-               then ⊢ Γ̃ {M̃ ⇀ M̃ ′ } Γ̃ ′ and Γ ′ and Γ̃ ′ are consistent. We proceed
owDP [50]. At a high level, CheckDP automatically infers a proof               by rule induction on commands. For most rules, all assumptions
in the form of alignment templates, so that the proof will be type-            in ShadowDP rules are guaranteed by the corresponding asser-
checked in a ShadowDP-like type system. Hence, given   an inferred             tions in CheckDP, making them trivial cases. Next, we present the
proof (i.e., concrete values of holes θ used in Aη | η ∈ H or                  interesting cases and omit the rest ones.
                                                 

  Aη , Sη | η ∈ H (with shadow execution), we can transform a                    • x := e: let Γ ⊢ e : num ⟨n◦, n† ⟩ . The interesting case is when


program M in CheckDP to a program M̃ in ShadowDP according                         pc = ⊥ ∧ n† , 0. In CheckDP, since x := e type checks in
to the following rule:                                                             CheckDP, we know that Γ ′ (x) = ∗ and b           x† is updated to n† after
η := Lap r → η := Lap r ; Sη (θ ); Aη (θ ) (CheckDP to ShadowDP)                   the transformed assignment. In ShadwoDP, we have Γ ′ (x) = n† .
   Without losing generality, we will proceed with the case with                   Hence, Γ ′ and Γ̃ ′ are still consistent: Lx, Γ ′ M† = x + n† = x +
shadow execution (i.e., the type system Γ tracks a pair of distances               Γ̃ ′ (x) = Lx, Γ̃ ′ M† .
for both aligned and shadow executions), since a proof without                   • η := д: the assertion c a ensures that the corresponding static
shadow execution is subsumed by the one with shadow execution                      check succeeds in rule T-Laplace of ShadowDP. One notable
and a selector that always selects the aligned distances.                          difference between CheckDP and ShadowDP is that since selec-
   Proof of Theorem 2                                                              tor S is unknown statically, a branch c d is inserted to update
Let M be a mechanism written in CheckDP. With a list of concrete                   the alignment of aligned execution. For consistency, checking
values of θ , let M̃ be the corresponding mechanism in ShadowDP by                 Lx, Γ ′ M† = Lx, Γ̃ ′ M† is trivial since the shadow distances are
rule (CheckDP to ShadowDP). If (1) M type checks, i.e., ⊢ Γ {M ⇀                   updated in the same way as in ShadowDP. When S = ◦, the
M ′ } Γ ′ and (2) the assertions in M ′ hold for all inputs. Then                  interesting case is when the distance of x is promoted to ∗
(1) M̃ type checks in ShadowDP, and                                                (i.e., Γ ′ (x) = num ⟨∗, n† ⟩ ∧ Γ(x) = num ⟨0, n† ⟩ . In this case, due to
(2) the assertions in M̃ ′ (transformed from M̃ by ShadowDP) pass.                 the inserted commands c ′ , Lx, Γ ′ M◦ = x + b            x◦ = x = Lx, Γ̃ ′ M◦ .
                                                                                   When S = †, due to the inserted commands c ′′ , Lx, Γ ′ M† =
   Proof. The proof is mostly straightforward due to the similarity                x +b   x† = x + n† = Lx, Γ̃ ′ M◦ where Γ ⊢ x : num ⟨_, , n† ⟩ . Finally,
between the type systems of CheckDP and ShadowDP. As stated
                                                                                   the typing environment changes to Γ ′ [η 7→ num ⟨nη ,0⟩ ] in Shad-
in Section 3, the only difference that requires extra work in the
                                                                                   owDP, but since all nonzero distances are dynamically tracked
proof is that CheckDP only tracks if a variable has the same value
                                                                                   in CheckDP, this becomes Γ ′ [η 7→ num ⟨∗,0⟩ ], which is the one
in two related runs (with distance 0) or not (with distance ∗), while
                                                                                   given by CheckDP rule.
ShadowDP also allows distance of an arbitrary expression. To gap
the potential difference, we define that Γ ′ and Γ̃ ′ are consistent if                                                                                             □

       ∀x ∈ V ∪ H. Lx, Γ ′ M◦ = Lx, Γ̃ ′ M◦ ∧ Lx, Γ ′ M† = Lx, Γ̃ ′ M†            Proof of Theorem 3
                                                                               With exactly the same notation and assumption as Theorem 2, M
Note that since we only need to convert CheckDP types to the                   satisfies ϵ-differential privacy.
(more expressive) ShadowDP types, such restriction of CheckDP
types does not cause any issue.                                                   Proof. This follows directly from Theorem 2 and the soundness
   First we show that if an expression e of M type checks with Γ in            of ShadowDP ([50], Theorem 2) and the fact that M and M̃ are
CheckDP, and all of the generated constraints C hold, then e type              semantically the same.                                        □
checks with Γ̃ in ShadowDP with an equivalent type (including




                                                                          17
function NoisyMax (size : num ⟨0, 0⟩ , q : list num ⟨∗, ∗⟩ )                      To prove its correctness using randomness alignment technique,
returns max : num ⟨0, −⟩                                                       we need to align the only random variable η in the mechanism
                                                                               (Line 3). Therefore, a corresponding privacy cost of aligning η
                       q◦ [i] ≤ 1 ∧ b
precondition ∀ i. −1 ≤ b            q† [i] = b
                                             q◦ [i]
                                                                               would be incurred for each iteration of the loop. However, manual
     i := 0; bq := 0; max := 0;
 1
 2   while (i < size )
                                                                               proof [25] suggests that we only need to align the random variable
 3     η := Lap (2/ϵ ) ;                                                       added to the actual maximum query answer. In other words, we
 4     if (q[i] + η > bq ∨ i = 0)                                              need an ability to “reset” the privacy cost upon seeing a new current
 5
 6
        max := i;
        bq := q[i] + η ;
                                                                               maximum noisy query answer.
 7     i := i + 1;
                                                                                  Bad Noisy Max. We also created an incorrect variant of Report
function Transformed NoisyMax (size,q, b
                                       q, sampl e, θ )                         Noisy Max. This variant directly returns the maximum noisy query
returns (max)                                                                  answer, instead of the index.
 8   vϵ := 0; idx := 0;                                                           More specifically, it can be obtained by changing Line 5 in Fig-
 9   i := 0; bq := 0; max := 0;                                                ure 8 from max := i to max := q[i] + η. CheckDP is then able
10   b ◦ := 0; bq
     bq          b † := 0; max
                            c ◦ := 0; max c † := 0;                            to find a counterexample for this incorrect variant.
11   while (i < size )
12      η := sampl e [idx]; vϵ := ( S ? vϵ : 0) + | A | × ϵ ;                  D.2    Variants of Sparse Vector Technique
13      η := A ;
                                                                                   SVT. We first show a correctly-implemented standard version
        b
                   ◦       †
14     if ( S ) bq
                b := bq      c ◦ := max
                       b ; max        c †;                                     of SVT [40]. This standard implementation is less powerful than
       if (q[i] + η > bq ∨ i = 0)
15
16       assert(q[i] + b
                       q[i] + η + η ◦ > bq + bq◦ ∨ i = 0);
                                                                               running example GapSVT, as it outputs true instead of the gap
17                c ◦ = 0);
          assert(max
                                                                               between noisy query answer and noisy threshold. This can be
18        max := i;                                                            obtained by changing Line 7 in Figure 1 from out := (q[i] +
19        max◦ := 0;                                                           η 2 )::out; to out := true::out;.
          b † := bq + bq
         bq             b † - (q[i] + η );
20
                                                                                  SVT with Monotonic Queries. There exist use cases with SVT
21        bq := q[i] + η ;
          b ◦ := b
                                                                               where the queries are monotonic. More formally, queries are mono-
22       bq      q◦ [i] + bη◦;
23     else
                                                                               tonic if for related queries q ∼ q ′ , ∀i. qi ≤ qi′ or ∀i. qi ≥ qi′ .
24       assert(¬(q[i] + b q[i] + η + η ◦ > bq + bq◦ ∨ i = 0));                As shown in [40]. When the queries are monotonic, it suffices to
25     // shadow execution                                                     add η 2 := Lap 2N /ϵ to each queries (Line 5 in Figure 1) and the
26                                  b † ∨ i = 0)
                  q† [i] + η > bq + bq
       if (q[i] + b                                                            algorithm still satisfies ϵ-DP.
27        b † := q[i] + b
          bq            q† [i] + η − bq;                                          Thanks to the flexibility of CheckDP, it only requires one change
28       c † := i - max;
         max
                                                                               in the function specification in order to verify this variant: mod-
29     i := i + 1;                                                             ify the constraint on b  q[i] in the precondition. Specifically, the
                                                                               new precondition for SVT with monotonic queries becomes ∀
                                                                               i. 0 ≤ bq[i] ≤ 1 for the ∀i. qi ≤ qi′ and ∀ i. −1 ≤ b       q[i] ≤ 0
Figure 8: Report Noisy Max and its transformed code, where                     for the other case. The final found alignment by CheckDP is the
S = q[i] + η > bq ∨ i = 0 ? θ [0] : θ [1] and A = θ [3] + θ [4] ×              same as the ones reported in the manual randomness alignment
q◦ [i] + θ [5] × bq◦
b                                                                              based proofs [24]:
                                                                                               (
                                                                                                                       q[i] : 0, if ∀i. qi ≤ qi′
                                                                                                 q[i] + η 2 ≥ Tη ? 1 − b
D     EXTRA CASE STUDIES                                                          η1 : 0 η2 :
                                                                                                 q[i] + η 2 ≥ Tη ? −bq[i] : 0, otherwise
In this section we list the pseudo-code of the algorithms we eval-
uated in the paper for completeness. The incorrect part for the                  To the best of our knowledge, no prior verification works have
incorrect algorithms is marked with a box.                                     automatically verified this variant.
                                                                                  NumSVT. Numerical Sparse Vector (NumSVT) [28] is another
D.1     Report Noisy Max                                                       interesting correct variant of SVT which outputs a numerical an-
   Report Noisy Max [25]. This is an important building block for de-          swer when the input query is larger than the noisy threshold. It
veloping differentially private algorithms. It generates differentially        follows the same procedure as Sparse Vector Technique, the dif-
private synthetic data by finding the identity with the maximum                ference is that it draws a fresh noise η 3 in the true branch, and
(noisy) score in the database. Here we present this mechanism in a             outputs q[i] + η 3 instead of true. Note that this is very similar
simplified manner: for a series of query answers q, where each of              to our running example GapSVT and BadGapSVT, the key differ-
them can differ at most one in the adjacent underlying database,               ence is that the freshly-drawn random noise hides the information
its goal is to return the index of the maximum query answer in a               about Tη , unlike the BadGapSVT. This variant can be obtained by
privacy-preserving way. To achieve differential privacy, the mecha-            making the following changes in Figure 1: (1) Line 1 is changed
nism first adds η = Lap 2/ϵ noise to each of the query answer, then            from Lap 2/ϵ to Lap 3/ϵ; (2) Line 5 is changed from Lap 4N /ϵ to
returns the index of the maximum noisy query answers q[i] + η,                 Lap 6N /ϵ; (3) Line 7 is change from out := (q[i] + η)::out;
instead of the true query answers q[i]. The pseudo code of this                to “η 3 := Lap (3N /ϵ); out := (q[i] + η 3 )::out;”. CheckDP
mechanism is shown in Figure 8.
                                                                          18
function SVT (T,N,size : num0 , q : list num∗ )                             has been exhausted. Moreover, the noise added to the queries does
returns (out : list bool ), check(ϵ )                                       not scale with parameter N. Specifically, based on BadSVT1, Line 5 is
precondition ∀ i. −1 ≤ bq[i] ≤ 1                                            changed to Lap 2/ϵ. BadSVT3 [38] is an interesting case since it tries
 1   η 1 := Lap (2/ϵ )
                                                                            to spend its privacy budget in a different allocation strategy between
 2   Tη := T + η 1 ;                                                        the threshold T and the query answers q[i] (1 : 3 instead of 1 : 1).
 3   count := 0; i := 0;                                                    However, the noise added to η 2 does not scale with parameter N.
 4   while ( count < N ∧ i < size )                                         The 3/4 privacy budget is allocated to each of the queries where it
 5      η 2 := Lap (4N /ϵ )
 6      if (q[i] + η 2 ≥ Tη ) then                                          should be shared among them. To get this variant, based on SVT
 7         out := true :: out ;                                             algorithm, the noise generation commands (Line 1 and Line 5) are
 8         count := count + 1;                                              changed to η 1 := Lap 4/ϵ and η 2 := Lap 4/(3 × ϵ) , respectively.
 9     else
10       out := false :: out ;
11     i := i + 1;                                                          function NumSVT (T,N,size : num0 , q : list num∗ )
function Transformed SVT (T,N,size,q, b
                                      q, sampl e, θ )                       returns (out : list bool ), check(ϵ )
returns (out)                                                               precondition ∀ i. −1 ≤ bq[i] ≤ 1
12    vϵ := 0; idx = 0;                                                      1   η 1 := Lap (3/ϵ )
13   η 1 := sampl e [idx]; idx := idx + 1;                                   2   Tη := T + η 1 ;
                                                                             3   count := 0; i := 0;
14    vϵ := vϵ + | A1 | × ϵ /2; ηb1 := A1 ;
                                                                             4   while ( count < N ∧ i < size )
15   Tη := T + η 1 ;                                                         5      η 2 := Lap (6N /ϵ )
16   Tcη := ηb1 ;                                                            6      if (q[i] + η 2 ≥ Tη ) then
17    count := 0; i := 0;                                                    7         η 3 := Lap (3N /ϵ ) ;
18    while ( count < N ∧ i < size )                                         8         out := ( q [ i ] + η 3 ):: out ;
19      η 2 := sampl e [idx]; idx := idx + 1;                                9         count := count + 1;
20      vϵ := vϵ + | A2 | × ϵ /4N ; ηb2 := A2 ;                             10     else
                                                                            11       out := false :: out ;
21      if (q[i] + η 2 ≥ Tη ) then                                          12     i := i + 1;
22         assert(q[i] + η 2 + b q[i] + ηb2 ≥ Tη + Tc
                                                    η );
23          out := true :: out ;                                            function Transformed NumSVT (T,N,size,q, b
                                                                                                                     q, sampl e, θ )
24          count := count + 1;                                             returns (out)
25     else
                                                                            12    vϵ := 0; idx = 0;
26        assert(¬(q[i] + η 2 + b
                                q[i] + ηb2 ≥ Tη + Tc
                                                   η ));
                                                                            13   η 1 := sampl e [idx]; idx := idx + 1;
27        out := false :: out ;
                                                                            14    vϵ := vϵ + | A1 | × ϵ /3; ηb1 := A1 ;
28      i := i + 1;
29   assert(vϵ ≤ ϵ );                                                       15   Tη := T + η 1 ;
                                                                            16   Tcη := ηb1 ;
                                                                            17    count := 0; i := 0;
Figure 9: Standard Sparse Vector Technique and its trans-                   18    while ( count < N ∧ i < size )
                                                                            19      η 2 := sampl e [idx]; idx := idx + 1;
formed code, where underlined parts are added by CheckDP.
                                                                            20      vϵ := vϵ + | A2 | × ϵ /6N ; ηb2 := A2 ;
The transformed code contains two alignment templates for
                                                                            21      if ( q [ i ] + η 2 ≥ Tη ) then
η 1 and η 2 : A1 = θ [0] and A2 = (q[i] + η 2 [i] ≥ Tη ) ? (θ [1] +                    assert(q[i] + η 2 + b q[i] + ηb2 ≥ Tη + Tc
                                                                            22                                                  η );
                      q[i]) : (θ [4] + θ [5] × Tη + θ [6] × b
θ [2] × Tbη + θ [3] × b                                     q[i]).          23         η 3 := sampl e [idx]; idx := idx + 1;
                                                                            24         vϵ := vϵ + | A3 | × ϵ /3N ; ηb3 := A3 ;
finds the same alignment as shown in [51] with which CPAChecker             25         assert(b q[i] + ηb3 = 0);
is able to verify the algorithm with this generated alignment.              26          out := ( q [ i ] + η 3 ):: out ;
                                                                            27          count := count + 1;
  Adaptive SVT. As mentioned in Section 5, we list the pseudo               28     else
code of Adaptive SVT in Figure 11.                                          29        assert(¬(q[i] + η 2 + b
                                                                                                            q[i] + ηb2 ≥ Tη + Tc
                                                                                                                               η ));
                                                                            30        out := false :: out ;
   BadSVT1 - 3. We now study other three incorrect variants of              31      i := i + 1;
SVT collected from [40]. All three variants are based on the classic        32   assert(vϵ ≤ ϵ );
SVT algorithm we have seen (i.e., Line 7 in Figure 1 is out :=
true::out;).                                                                Figure 10: Numerical Sparse Vector Technique and its
   BadSVT1 [47] adds no noise to the query answers and has no               transformed code, where underlined parts are added by
bounds on the number of true’s it can output. This variant is               CheckDP. The transformed code contains three alignment
obtained by changing Line 4 from while (count<N∧i<size) to                  templates for η 1 , η 2 and η 3 respectively: A1 = θ [0], A2 =
while (i<size) and Line 5 from Lap 4N /ϵ to 0. Another variant
                                                                            (q[i] + η 2 [i] ≥ Tη ) ? (θ [1] + θ [2] × Tbη + θ [3] × bq[i]) : (θ [4] +
BadSVT2 [20] has no bounds on the number of true’s it can output
as well. It keeps outputting true even if the given privacy budget          θ [5] × Tη + θ [6] × b
                                                                                                 q[i]), A3 = θ [7] + θ [8] × Tbη + θ [9] × b
                                                                                                                                           q[i])




                                                                       19
function AdaptiveSVT (T,N,size : num0 ,q : list num∗ )                             Note that apart from BadSVT1, which does not sample η 2 , the
returns (out : list num0 ), check(ϵ )                                          generated templates are identical to the GapSVT since they all have
precondition ∀ i. −1 ≤ bq[i] ≤ 1                                               similar typing environments.
 1  cost := 0;                                                                     Interestingly, since the errors are very similar among them
 2  η 1 := Lap (2/ϵ );                                                         (no bounds on number of outputs / wrong scale of added noise),
 3  cost := cost + ϵ /2;                                                       CheckDP finds a common counterexample [0, 0, 0, 0, 0], [1, 1, 1, 1, −1]
 4  Tη := T + η 1 ;                                                            where T = 0 and N = 1 within 6 seconds, and this counterexample
    i := 0;
 5
                                                                               is further validated by PSI.
 6  while ( cost ≤ ϵ - 4N /ϵ ∧ i < size )
 7     η 2 := Lap (8N /ϵ );                                                       BadGapSVT. As discussed in Section 2.4, we list one of our run-
       if (q[i] + η 2 − Tη ≥ σ ) then
 8
                                                                               ning examples BadGapSVT in Figure 15 for completeness.
 9        out := ( q [ i ] + η 2 - Tη ):: out ;
10        cost := cost + ϵ /(8N );
11     else                                                                    function BadSVT1 (T,N,size : num0 , q : list num∗ )
12        η 3 := Lap (4N /ϵ );
13        if (q[i] + η 3 − Tη ≥ 0) then                                        returns (out : list bool ), check(ϵ )
14           out := ( q [ i ] + η 3 - Tη ):: out ;                             precondition ∀ i. −1 ≤ bq[i] ≤ 1
15           cost := cost + ϵ /(4N );                                           1   η 1 := Lap (2/ϵ ) ;
16        else                                                                  2   Tη := T + η 1 ;
17           out := 0:: out ;                                                   3   count := 0; i := 0;
18     i := i + 1;                                                              4   while ( i < size )
                                                                                5     η 2 := 0 ;
function Transformed AdaptiveSVT (T,N,size,q, b    q, sampl e, θ )
                                                                                6     if (q[i] + η 2 ≥ Tη ) then
returns (out)                                                                   7        out := true :: out ;
12  vϵ := 0; idx = 0;                                                           8        count := count + 1;
13  η 1 := sampl e[idx]; idx := idx + 1;                                        9     else
                                                                               10       out := false :: out ;
14  vϵ := vϵ + | A1 | × ϵ /2; ηb1 := A1 ;
                                                                               11     i := i + 1;
15  Tη := T + η 1 ;
16  Tcη := ηb1 ;                                                               function Transformed BadSVT1 (T,N,size,q, b
                                                                                                                         q, sampl e, θ )
17   count := 0; i := 0;                                                       returns (out)
18   while ( cost ≤ ϵ - 4N /ϵ ∧ i < size )                                     12    vϵ := 0; idx = 0;
19     η 2 := sampl e[idx]; idx := idx + 1;                                    13   η 1 := sampl e [idx]; idx := idx + 1;
20      vϵ := vϵ + | A2 | × ϵ /8N ; ηb2 := A2 ;                                14    vϵ := vϵ + | A1 | × ϵ /2; ηb1 := A1 ;
21      if ( q [ i ] + η 2 - Tη ≥ σ ) then                                     15   Tη := T + η 1 ;
22         assert(q[i] + η 2 + b q[i] + ηb2 - (Tη + Tcη ) ≥ σ );               16   Tcη := ηb1 ;
                                                                               17    count := 0; i := 0;
23         assert(b q[i] + ηb2 - Tc
                                  η == 0);
                                                                               18    while ( i < size )
24       out := ( q [ i ] + η 2 - Tη ):: out ;                                 19      η 2 := 0;
25       cost := cost + ϵ /(8N );                                              20      if ( q [ i ] + η 2 ≥ Tη ) then
26     else                                                                    21         assert(q[i] + η 2 + b q[i] ≥ Tη + Tc
                                                                                                                             η );
27       assert(¬(q[i] + η 2 + b                      η ) ≥ σ ));
                                  q[i] + ηb2 - (Tη + Tc                        22         out := true :: out ;
28       η 3 := sampl e[idx]; idx := idx + 1;                                  23         count := count + 1;
                                                                               24     else
29       vϵ := vϵ + | A3 | × ϵ /4N ; ηb2 := A3 ;
                                                                               25        assert(¬(q[i] + η 2 + b
                                                                                                               q[i] ≥ Tη + Tc
                                                                                                                            η ));
30       if ( q [ i ] + η 3 - Tη ≥ 0)
                                                                               26        out := false :: out ;
31           assert(q[i] + η 3 + bq[i] + ηb3 - (Tη + Tcη ≥ 0) ;                27      i := i + 1;
                                                                               28   assert(vϵ ≤ ϵ );
32           assert(bq[i] + ηb3 - Tη == 0);
                                  c
33          out := ( q [ i ] + η 3 - Tη ):: out ;
34          cost := cost + ϵ /(4N );
                                                                               Figure 12: BadSVT1 and its transformed code, where under-
35        else
                                                                               lined parts are added by CheckDP. The transformed code
36          assert(¬(q[i] + η 3 + b                    η ) ≥ 0));
                                   q[i] + ηb3 - (Tη + Tc
                                                                               contains a alignment template for η 1 : A1 = θ [0].
37          out := false :: out ;
38      i := i + 1;
39   assert(vϵ ≤ ϵ );


Figure 11: Adaptive SVT and its transformed code, where un-
derlined parts are added by CheckDP. The transformed code
contains three alignment templates for η 1 and η 2 : A1 = θ [0],
A2 = ΩT op ?(θ [1]+θ [2]×Tbη +θ [3]×bq[i]):(θ [4]+θ [5]×Tη +θ [6]×
                                                       q[i]) : (θ [4] +
q[i]) and A3 = Ω Middl e ? (θ [1] +θ [2] × Tbη +θ [3] ×b
b
θ [5] × Tη + θ [6] × b
                     q[i]), where Ω∗ denotes the corresponding
branch condition at Line 8 and 13.
                                                                          20
function BadSVT3 (T,N,size : num0 , q : list num∗ )                         function BadSVT2 (T,N,size : num0 , q : list num∗ )
returns (out : list bool ), check(ϵ )                                       returns (out : list bool ), check(ϵ )
precondition ∀ i. −1 ≤ bq[i] ≤ 1                                            precondition ∀ i. −1 ≤ bq[i] ≤ 1
 1   η 1 := Lap (4/ϵ ) ;                                                     1   η 1 := Lap (2/ϵ ) ;
                                                                             2   Tη := T + η 1 ;
 2   Tη := T + η 1 ;                                                         3   count := 0; i := 0;
 3   count := 0; i := 0;
 4   while ( count < N ∧ i < size)                                           4   while ( i < size )
 5     η 2 :=   Lap (4/3ϵ ) ;                                                5     η 2 :=   Lap (2/ϵ ) ;
 6     if (q[i] + η 2 ≥ Tη ) then                                            6     if (q[i] + η 2 ≥ Tη ) then
 7        out := true :: out ;                                               7        out := true :: out ;
 8        count := count + 1;                                                8        count := count + 1;
 9     else                                                                  9     else
10       out := false :: out ;                                              10       out := false :: out ;
11     i := i + 1;                                                          11     i := i + 1;

function Transformed BadSVT3 (T,N,size,q, b
                                          q, sampl e, θ )                   function Transformed BadSVT2 (T,N,size,q, b
                                                                                                                      q, sampl e, θ )
returns (out)                                                               returns (out)
12    vϵ := 0; idx = 0;                                                     12    vϵ := 0; idx = 0;
13   η 1 := sampl e [idx]; idx := idx + 1;                                  13   η 1 := sampl e [idx]; idx := idx + 1;
14    vϵ := vϵ + | A1 | × ϵ /4; ηb1 := A1 ;                                 14    vϵ := vϵ + | A1 | × ϵ /2; ηb1 := A1 ;
15   Tη := T + η 1 ;                                                        15   Tη := T + η 1 ;
16   Tcη := ηb1 ;
                                                                            16   Tcη := ηb1 ;

17    count := 0; i := 0;                                                   17    count := 0; i := 0;
18    while ( count < N ∧ i < size )                                        18    while ( i < size )
19      η 2 := sampl e [idx]; idx := idx + 1;                               19      η 2 := sampl e [idx]; idx := idx + 1;
20      vϵ := vϵ + | A2 | × 3ϵ /4; ηb2 := A2 ;                              20      vϵ := vϵ + | A2 | × ϵ /2; ηb2 := A2 ;
21      if (q[i] + η 2 ≥ Tη ) then                                          21      if ( q [ i ] + η 2 ≥ Tη ) then
22         assert(q[i] + η 2 + b q[i] + ηb2 ≥ Tη + Tc
                                                    η );
                                                                            22         assert(q[i] + η 2 + b q[i] + ηb2 ≥ Tη + Tc
                                                                                                                                η );

23          out := true :: out ;                                            23          out := true :: out ;
24          count := count + 1;                                             24          count := count + 1;
25     else                                                                 25     else
26        assert(¬(q[i] + η 2 + b
                                q[i] + ηb2 ≥ Tη + Tc
                                                   η ));
                                                                            26        assert(¬(q[i] + η 2 + b
                                                                                                            q[i] + ηb2 ≥ Tη + Tc
                                                                                                                               η ));

27        out := false :: out ;                                             27        out := false :: out ;
28      i := i + 1;                                                         28      i := i + 1;
29   assert(vϵ ≤ ϵ );                                                       29   assert(vϵ ≤ ϵ );



Figure 14: BadSVT3 and its transformed code, where under-                   Figure 13: BadSVT2 and its transformed code, where under-
lined parts are added by CheckDP. The transformed code                      lined parts are added by CheckDP. The transformed code
contains two alignment templates for η 1 and η 2 : A1 = θ [0]               contains two alignment templates for η 1 and η 2 : A1 = θ [0]
                                                             q[i]) :
and A2 = (q[i] + η 2 ≥ Tη ) ? (θ [1] + θ [2] × Tbη + θ [3] × b                                                                           q[i]) :
                                                                            and A2 = (q[i] + η 2 ≥ Tη ) ? (θ [1] + θ [2] × Tbη + θ [3] × b
(θ [4] + θ [5] × Tη + θ [6] × b
                              q[i]).                                        (θ [4] + θ [5] × Tη + θ [6] × b
                                                                                                          q[i]).




                                                                       21
function BadGapSVT (size,T,N : num0 , q : list num∗ )                              function PartialSum (size : num0 , q : list num∗ )
returns (out : list num0 ), check(ϵ )                                              returns (out : num0 ), check(ϵ )
precondition ∀ i. −1 ≤ bq[i] ≤ 1                                                   precondition ∀i. −1 ≤b  q[i] ≤ 1∧(∀i. (b
                                                                                                                          q[i], 0) ⇒ (∀j. b
                                                                                                                                          q[j] = 0))
 1   η 1 := Lap (2/ϵ ) ;                                                            1   sum := 0; i := 0;
 2   Tη := T + η 1 ;                                                                2   while ( i < size )
 3   count := 0; i := 0;                                                            3     sum := sum + q [ i ];
 4   while ( count < N )                                                            4     i := i + 1;
 5   η 2 := Lap (4N /ϵ ) ;                                                          5   η = Lap (1/ϵ ) ;
 6   if (q[i] + η 2 ≥ Tη ) then                                                     6   out := sum + η ;
 7     out :=     (q[i] + η 2 ) :: out ;
                                                                                   function Transformed PartialSum (size,q,b
                                                                                                                           q, sampl e, θ )
 8      count := count + 1;
                                                                                   returns (out)
 9   else
10     out := 0:: out ;                                                             7   vϵ := 0; sum
                                                                                                  c := 0;
11   i := i + 1;                                                                    8   sum := 0; i := 0;
                                                                                    9   while ( i < size )
function Transformed BadGapSVT (T,N,size,q, b
                                            q, sampl e, θ )                        10      sum := sum + q [ i ];
                                                                                   11     sum
                                                                                           c := sum
                                                                                                  c +b   q[i];
returns (out)
                                                                                   12      i := i + 1;
12    vϵ := 0; idx = 0;                                                            13                          η := θ ;
                                                                                        vϵ := vϵ + | A | × ϵ ; b
13   η 1 := sampl e [idx]; idx := idx + 1;
                                                                                   14   assert(sum
                                                                                               c + b η );
14    vϵ := vϵ + | A1 | × ϵ /2; ηb1 := A1 ;                                        15   out := sum + η ;
15   Tη := T + η 1 ;                                                               16   assert(vϵ ≤ ϵ );
16   Tcη := ηb1 ;
17    count := 0; i := 0;
18    while ( count < N ∧ i < size )                                               Figure 16: PartialSum and its transformation using
     η 2 := sampl e [idx]; idx := idx + 1;
19
                                                                                   CheckDP, where A = θ [0] + θ [1] × sd
                                                                                                                       um + θ [2] × b
                                                                                                                                    q[i].
20    vϵ := vϵ + | A2 | × ϵ /4N ; ηb2 := A2 ;
21    if (q[i] + η 2 ≥ Tη ) then
22      assert(q[i] + η 2 + b  q[i] + ηb2 ≥ Tη + Tc
                                                  η );                             D.4     SmartSum and BadSmartSum
        assert(b  q[i] + ηb2 = 0);
23
                                                                                   SmartSum [19] continually releases aggregated statistics with pri-
24       out := (q[i] + η 2 ):: out ;
25       count := count + 1;                                                       vacy protections. For a finite sequence of queries q[0], q[1], · · · , q[T ],
26   else                                                                          where T is the length of q, the goal of SmartSum is to release the
                                                                                   prefix sum: q[0], q[0] + q[1], · · · , Ti=0 q[i] in a private way. To
                                                                                                                          Í
27     assert(¬(q[i] + η 2 + b
                             q[i] + ηb2 ≥ Tη + Tc
                                                η ));
28      out := 0:: out ;                                                           achieve differential privacy, SmartSum first divides the sequence
     i := i + 1;
29
30   assert(vϵ ≤ ϵ );
                                                                                   into non-overlapping blocks B 0 , · · · , Bl with size M, then maintains
                                                                                   the noisy version of each query and noisy version of the block sum,
                                                                                   both by directly adding Lap 1/ϵ noise. Then to compute the k th
Figure 15: BadGapSVT and its transformed code. The trans-                          component of the prefix sum sequence ki=0 q[i], it only has to add
                                                                                                                                Í
formed code contains two alignment templates for η 1 and η 2 :                     up the noisy block sum that covers before k, plus the remaining
A1 = θ [0] and A2 = (q[i] + η 2 [i] ≥ Tη ) ? (θ [1] + θ [2] × Tbη +                (k + 1) mod M noisy queries. The pseudo code is shown in Figure 17.
      q[i]):(θ [4]+θ [5]×Tη +θ [6]×b
θ [3]×b                            q[i]). Note that the random                     The if branch is responsible for dividing the queries and summing
variables and θ are inserted as part of the function input.                        up the block sums (stored in sum variable), where else branch adds
                                                                                   the remaining noisy queries.
                                                                                      Notably, SmartSum satisfies 2ϵ-differential privacy instead of
D.3     Partial Sum                                                                ϵ-differential privacy. Moreover, the adjacency requirement of the
Next, we study a simple algorithm PartialSum (Figure 16) which                     inputs is that only one of the queries can differ by at most one.
outputs the sum of queries in a privacy-preserving manner: it di-                  These two requirements are specified in the function signature
rectly computes sum of all queries and adds a Lap 1/ϵ to the final                 (check(2ϵ) and precondition).
output sum. Note that similar to SmartSum, it has the same adja-                      An incorrect variant of SmartSum, called BadSmartSum, is ob-
cency requirement (only one query can differ by at most one). The                  tained by changing Line 4 to η 1 := 0 in Figure 17. It directly releases
alignment is easily found for η by CheckDP which is to “cancel                     sum + q[i] without adding any noise (since η 1 = 0), where sum
out” the distance of sum variable (i.e., -d sum). With the alignment               stores the accurate, non-noisy sum of queries (at Line 11), hence
CPAChecker verifies this algorithm.                                                breaking differential privacy. Interestingly, the violation only hap-
    An incorrect variant for PartialSum called BadPartialSum is cre-               pens in a rare branch if ((i + 1) mod M = 0), where the
ated where Line 5 is changed from 1/ϵ to 1/(2×ϵ), therefore making                 accurate sum is added to the output list out. In other words, out
it fail to satisfy ϵ-differential privacy (though it actually satisfies            contains mostly private data with only a few exceptions. This rare
2ϵ-differential privacy). A counterexample [0, 0, 0, 0, 0], [0, 0, 0, 0, 1]        event makes it challenging for sampling-based tools to find the
is found by CheckDP and further validated by PSI.                                  violation.



                                                                              22
function SmartSum (M,T,size : num0 , q : list num∗ )
returns (out : list num0 ), check(2ϵ )
precondition ∀i. −1 ≤b q[i] ≤ 1∧(∀i. (bq[i], 0) ⇒ (∀j. b
                                                       q[j] = 0))
 1   next := 0; i := 0; sum := 0;
 2   while ( i < size ∧ i ≤ T )
 3     if (( i + 1) mod M = 0) then
 4       η 1 := Lap (1/ϵ );
 5       next := sum + q [ i ] + η 1 ;
 6       sum := 0;
 7       out := next :: out ;
 8     else
 9       η 2 := Lap (1/ϵ );
10       next := next + q [ i ] + η 2 ;
11       sum := sum + q [ i ];
12       out := next :: out ;
13     i := i + 1;

function Transformed SmartSum (M,T,size,q, b
                                           q, sampl e, θ )
returns (out)
14   vϵ := 0; idx := 0;
15    next := 0; i := 0; sum := 0;
16   sdum := 0; next := 0;
17    while ( i < size ∧ i ≤ T )
18       if (( i + 1) mod M = 0) then
19         η 1 := sampl e[idx]; idx := idx + 1;
20         vϵ := vϵ + |A1 | × ϵ ; ηb1 := A1 ;
21          next := sum + q [ i ] + η 1 ;
22         next := sd    q[i] + ηb1 ;
                     um + b
23          sum := 0;
24         sdum := 0;
25         assert(next = 0);
26          out := next :: out ;
27       else
28         η 2 := sampl e[idx]; idx := idx + 1;
29         vϵ := vϵ + |A2 | × ϵ ; ηb2 := A2 ;
30          next := next + q [ i ] + η 2 ;
31         next := n     q[i] + ηb2 ;
                     ext + b
32          sum := sum + q [ i ];
33         sdum := sd
                    um + b
                         q[i];
34         assert(next = 0);
35          out := next :: out ;
36       i := i + 1;
37   assert(vϵ ≤ 2ϵ );


Figure 17: SmartSum and its transformed code. Underlined
parts are added by CheckDP. A1 = θ [0] + θ [1] × sd   um + θ [2] ×
q[i] + θ [3] × n
b               ext and A2 = θ [4] + θ [5] × sd
                                              um + θ [6] × b
                                                           q[i] +
θ [7] × n
         ext.




                                                                     23
