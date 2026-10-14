                                                              The Café in Amsterdam
                                                                     When the Incumbent Becomes the Oracle
                                          Augusto Camargo • Bluecore Consulting, São Paulo, Brazil • augusto.camargo@bluecore.com.br • 25 August 2026



                                                           A research note. It proposes a way of looking at computational reformulation —
                                                           a lens, not a theorem. No component is claimed novel in isolation; the offering is
                                                                           the synthesis, and the question it makes easy to ask.

                                            In 1956, sitting in a café in Amsterdam, Edsger            and a predecessor tree form a certificate check-
                                         Dijkstra worked out—in about twenty minutes,                  able in time linear in the graph. So the freedom
                                         with no pencil—how a computer should find                     never depended on verification being free. It
arXiv:2607.13393v3 [cs.PF] 25 Aug 2026




                                         the shortest route between two Dutch cities. He               depended on this: the obligation was stated
                                         needed a concrete problem to show off the AR-                 without mentioning the incumbent implemen-
                                         MAC machine, so he picked one anybody could                   tation. From this point on, I simply call it the
                                         check on a map: the shortest way from Rotter-                 incumbent. Dijkstra’s algorithm was one solver
                                         dam to Groningen. The algorithm that came out                 of a named problem. It was never the definition
                                         of that afternoon is now taught to virtually every            of a correct answer.
                                         computer science student on Earth [1].
                                                                                                         The stakes are silicon and joules
                                            Notice the order in which he did it, because
                                         the whole idea I want to offer lives inside that                 This is not an antiquarian point. It seems to
                                         order.                                                       decide what a field can afford to build. Modern
                                                                                                      accelerators pay for one shape of computation—
                                            He formulated the demand first. Find a path of
                                                                                                      dense, regular, reused—and a problem posed
                                         minimum total length. That sentence exists inde-
                                                                                                      in that shape can run several times faster, at a
                                         pendently of any algorithm—it is a specification,
                                                                                                      fraction of the energy, than the same problem
                                         not an implementation. The algorithm came
                                                                                                      posed the way a sequential machine liked it.
                                         second, as one way, out of many, to satisfy it.
                                                                                                      When you are free to change the formulation,
                                         Dijkstra never confused the two. The demand
                                                                                                      that speedup is on the table. When you are not,
                                         was a shortest path. His procedure was one method
                                                                                                      it is not. A speech frontend we re-posed as a sin-
                                         for producing one.
                                                                                                      gle matrix multiplication measured 1.64×–3.29×
                                            And because the demand existed indepen-                   speedup and up to 3.03× less energy across four
                                         dently of the algorithm, the field stayed free               accelerators—not by computing the incumbent’s
                                         to reinvent the algorithm entirely. Over the                 answer faster, but by computing a different an-
                                         following sixty years, shortest-path computa-                swer that the task could not distinguish from
                                         tion was reformulated almost beyond recogni-                 it [2]. Whether a field is allowed to reach for that
                                         tion: A* adds a heuristic; Contraction Hierar-               trade is, it seems to me, exactly the question the
                                         chies precompute shortcuts and answer conti-                 café quietly decided.
                                         nental queries in microseconds; hub labelling,
                                         transit-node routing, bidirectional search, land-               A computation whose café conversation
                                         mark methods—a family whose members share                     never happened
                                         remarkably little internal structure.                            The dominant audio frontend in speech pro-
                                            Not one of them was ever required to repro-                cessing is a pipeline: a Fourier transform, a Mel
                                         duce Dijkstra’s path. A new algorithm is not                  filterbank, a logarithm. Decades of engineering
                                         asked whether it visits the same intermediate                 have tuned it, vendors have accelerated it, and
                                         cities. It is asked whether it satisfies the same             accelerators still inherit its assumptions. Ask the
                                         specification: return a shortest path—or, in the              awkward question—what is the implementation-
                                         approximate variants, one whose gap from short-               independent demand that a structurally different
                                         est is explicitly declared. Establishing that is              frontend must satisfy to replace it?—and the an-
                                         not trivial: summing a path’s weights tells you               swer is not that audio is blind to it. Audio, of all
                                         its cost, not its optimality. But the algorithms              fields, has the oracle. SincNet and LEAF replace
                                         can carry their own evidence—distance labels                  the Fourier–Mel frontend with entirely different
objects and are admitted purely on downstream         where R(Out0 ) is any acceptance region defined
task accuracy [3, 4]; the community plainly ac-       from the incumbent’s output rather than from
cepts a task-level criterion when it wants one.       D; its extreme case R(Out0 ) = {Out0 } is exact
   But look at where that criterion was pointed. It   regression. Baseline capture is the drift TD ⇝ T0 .
was pointed at representation—at learning a task-     Writing A( T ) = { P : ∃ Out ∈ [[ P]], T (Out) = 1}
adapted frontend—and, as far as I can see, never      for the representations a test admits, A( TD ) is ev-
at the substrate. When those systems changed          erything that can serve the demand, while A( T0 )
the formulation, they changed it in the direction     is only what can reach the incumbent. Nothing
that made it slower: LEAF is far more expensive       here needs a metric, an ε, or a margin. The one
to compute than a fixed Mel filterbank, and its       question a reader can carry to any paper is just:
own successors report that it fails to consistently   does the definition of T mention Out0 ?
beat one [5]. Meanwhile the part of the field            Two properties of a ⟨problem, field⟩ then pull
that did care about speed—the ports, the vendor       apart, and should not be confused. Whether a
kernels—judged a replacement by whether it re-        reformulation can be judged at all looks like it
produced the pipeline’s output. So the demand-        turns on whether an incumbent-independent TD
side oracle existed and the substrate motive ex-      exists. Whether its discovery can be automated—
isted, in the same field, and—this is the thing I     dropped inside a program-search loop, as Fun-
keep turning over—I had not seen the two put          Search or AlphaEvolve do [10, 11]—looks like
together. Where the substrate was the reason to       it turns additionally on whether T is cheap to
change, the incumbent’s output was still the test.    evaluate. Routing has both: an independent ob-
   That is the phenomenon I want to point at.         jective and a linear-time certificate. The matrix-
Not a field with no ruler—a field holding a ruler     multiplication frontend has the first but not the
it never thought to use for this. The consequence     second—a frozen model is an independent TD ,
is the same either way: a genuinely different         but it costs hours to consult, which may be ex-
frontend does not lose on the merits. On the only     actly why finding the reformulation stayed a
ruler in routine use, proximity to the incumbent’s    human, experimental act. In the captured case
output, it cannot be scored at all. It looks wrong    the missing ingredient does not look primarily
because it is different, even when it serves the      like a cheap evaluator. It looks like a shared,
task equally well.                                    incumbent-independent demand.
   When a field has an implementation-
independent demand, the incumbent looks                 Two honesties
like mere evidence that the demand can be met.           The mechanism is old. The question I want
When it lacks one—or never aims the one it            to ask about it is simple, and it may not be
has—the incumbent itself seems to become the          mine alone. Software testing has lived with the
practical oracle. I have taken to calling that        oracle problem for decades. Weyuker described
transition baseline capture: the moment an            non-testable programs, whose correct output can-
incumbent stops being evidence and becomes            not be independently determined [6]. Barr and
judge. The incumbent only ever proved the             colleagues surveyed the substitutes the field
demand could be satisfied. It never proved the        reaches for—pseudo-oracles, previous versions,
demand had to be satisfied that way.                  golden outputs—and noted that such a substi-
                                                      tute can “migrate, over time, to become” the
  The lens, in four lines                             specification [7]. Requirements engineering calls
  The prose above wants only a little notation,       a close cousin implementation bias: stating how
and no more than this. Let O be the set of possi-     instead of what [8]. I lean on all of it, gratefully—
ble outputs, and write Out |= D when an output        that serious people have named these pieces is
satisfies the demand D. Then                          what makes me think the lens is real rather than
  P represents D:   ∃ Out ∈ [[ P]]. Out |= D;         a private illusion. The question I keep wanting
                                                      to ask, and have not often seen asked in these
  P is sound for D: ∀ Out ∈ [[ P]]. Out |= D.
                                                      words, is what this substitution costs a computa-
An acceptance test is a predicate T : O → {0, 1},     tion: whether the practice quietly decides which
and the whole distinction is what T is built from:    reformulations a field is willing, or even able,
                                                      to admit—and therefore how fast that field is
   TD (Out) = 1[ Out |= D ]    (independent)          allowed to run.
   T0 (Out) = 1[ Out ∈ R(Out0 ) ]    (captured)          Judging by acceptability rather than numeri-
                           demand stated               how a candidate is       what happened
                           independently of the        justified
                           incumbent?
   Routing                 yes — shortest path, or a   proof, certificate, or   continuous
   (Dijkstra → A* →        declared approximation      bound against the stated reformulation for six
   CH)                                                 objective                decades
   Audio frontend,         available, not applied      agreement with the       deep optimization
   for the substrate       here — the task oracle      established              within the incumbent
                           exists, yet                 representation           family
                           substrate-motivated
                           replacement is judged by
                           matching the pipeline


cal proximity alone is not new. Felzmann, Filho,        tistical test asking whether a run represents the
de Oliveira and Wanner argued for evaluating            same climate rather than the same bits [13]. In
approximate designs in terms of whether their           each case someone made the acceptance condi-
outputs remain acceptable for the application,          tion explicit, operational, and independent of
rather than treating conventional quality metrics       the incumbent. That is all I mean by buying
as sufficient [9]. Theirs is prior work and I am        a verifier: not necessarily writing an objective
glad to stand next to it. The distinction I find        function—CESM-ECT is a consistency test, not
myself caring about is narrower: approximate            an objective—but making the demand answer-
computing ordinarily begins from an incumbent           able without pointing back at the incumbent. It
computation and asks which deviations from              has a price, and the guess I would like to test is
it remain acceptable. The cases that made me            that the price is measurable, and that paying it
look twice need not be naturally described as           enlarges the space of reformulations, and thus
degraded versions of that computation. A Mel-           the hardware performance, a field can reach.
spaced projection is not simply an inaccurate
FFT; there is no obvious parameter that continu-          Coda
ously turns one into the other. So the question I          Dijkstra spent twenty minutes in a café and,
am left with is not how much quality may I spend        without meaning to, handed an entire field sixty
against the incumbent, but when is a structurally       years of freedom. Most fields never had that
different formulation admissible at all—and the in-     conversation. Whether this phenomenon de-
cumbent’s output, alone, does not seem able to          serves a name is ultimately less important than
answer that.                                            whether it exists. If it does, then making a field’s
                                                        demand explicit—stating it without mention-
  What buying a verifier looks like                     ing the incumbent—may be one of the cheapest
                                                        ways we have of enlarging the space of admissi-
   The escape, if it is one, is not cleverness. It      ble reformulations, and one of the few that can
looks more like bookkeeping done late. When             be done before a single line of the new computa-
a community finally makes its acceptance con-           tion is written.
dition explicit, reformulations that had been un-
justifiable for years seem to become admissible
almost at once. ZIP 215: independent imple-
mentations of Ed25519 had inherited their no-
tion of a valid signature from an obsolete build
of a library—bug and all—and could disagree
on which signatures were valid; the fix was to
write the validation rules down explicitly, which
let implementations agree and, as a named re-
ward, enabled batch validation [12]. CESM-ECT:
climate simulations cannot be compared bit-for-
bit across compilers, so instead of handing four
hundred simulated years to a senior scientist for
subjective approval, the community built a sta-
References
 [1] P. L. Frana, “Oral history interview with Edsger W. Dijkstra,” OH 330, Charles Babbage Institute, University of
     Minnesota, Aug. 2, 2001; revised as “An interview with Edsger W. Dijkstra,” Communications of the ACM, vol. 53, no. 8,
     pp. 41–47, 2010.
 [2] A. Camargo and M. Finger, “MelT: a portable, single-GEMM Mel audio frontend via non-uniform DFT with measured
     latency and energy gains on GPUs,” arXiv:2606.01009v3 [cs.SD], 2026.
 [3] M. Ravanelli and Y. Bengio, “Speaker recognition from raw waveform with SincNet,” in IEEE Spoken Language Technology
     Workshop (SLT), 2018, pp. 1021–1028.
 [4] N. Zeghidour, O. Teboul, F. de Chaumont Quitry, and M. Tagliasacchi, “LEAF: a learnable frontend for audio classifica-
     tion,” in International Conference on Learning Representations (ICLR), 2021.
 [5] J. Schlüter and G. Gutenbrunner, “EfficientLEAF: a faster learnable audio frontend of questionable use,” in 30th
     European Signal Processing Conference (EUSIPCO), 2022, pp. 205–208.
 [6] E. J. Weyuker, “On testing non-testable programs,” The Computer Journal, vol. 25, no. 4, pp. 465–470, 1982.
 [7] E. T. Barr, M. Harman, P. McMinn, M. Shahbaz, and S. Yoo, “The oracle problem in software testing: a survey,” IEEE
     Transactions on Software Engineering, vol. 41, no. 5, pp. 507–525, 2015.
 [8] P. Zave and M. Jackson, “Four dark corners of requirements engineering,” ACM Transactions on Software Engineering
     and Methodology, vol. 6, no. 1, pp. 1–30, 1997.
 [9] I. Felzmann, J. Fabrício Filho, J. R. de Oliveira, and L. Wanner, “How much quality is enough quality? A case for
     acceptability in approximate designs,” in IEEE International Conference on Computer Design (ICCD), 2021, pp. 5–8.
[10] B. Romera-Paredes et al., “Mathematical discoveries from program search with large language models,” Nature, vol.
     625, pp. 468–475, 2024.
[11] A. Novikov et al., “AlphaEvolve: a coding agent for scientific and algorithmic discovery,” arXiv:2506.13131, 2025.
[12] Electric Coin Company, “ZIP 215: explicitly defining and modifying Ed25519 validation rules,” Zcash Improvement
     Proposals, 2022.
[13] A. H. Baker et al., “A new ensemble-based consistency test for the Community Earth System Model (pyCECT v1.0),”
     Geoscientific Model Development, vol. 8, pp. 2829–2840, 2015.
