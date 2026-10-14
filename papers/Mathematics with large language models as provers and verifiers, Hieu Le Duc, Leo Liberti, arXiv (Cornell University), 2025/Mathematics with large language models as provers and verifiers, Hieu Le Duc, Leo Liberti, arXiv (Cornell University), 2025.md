                                        Mathematics with large language models as provers and verifiers
                                                                           Hieu Le Duc1 , Leo Liberti2

                                              1
                                                  Télécom SudParis, Institut Polytechnique de Paris, 91000 Évry-Courcouronnes, France
                                                  Email:duc-hieu.le@telecom-sudparis.eu
                                              2
                                                  LIX CNRS, École Polytechnique, Institut Polytechnique de Paris, F-91128 Palaiseau,
                                                  France
                                                  Email:liberti@lix.polytechnique.fr
arXiv:2510.12829v3 [cs.CL] 6 Nov 2025




                                                                                  November 7, 2025




                                                  This paper presents mathematical arguments obtained from a pro-
                                                  tocol based on LLMs from OpenAI. We are currently in the process
                                                  of telling apart the correct from the wrong proofs produced by our
                                                  protocol. One of the problems is that the formalization step, partly
                                                  carried out by humans, takes much longer than expected. We are
                                                  currently asking human experts to verify the proofs. We shall post
                                                  further versions of this report as the verification work progresses.
                                                  Meanwhile, for the moment, none of the “proofs” mentioned herein
                                                  should be taken as correct.

                                                                                       Abstract

                                                 During 2024 and 2025 the discussion about the theorem-proving capabilities of large
                                             language models started reporting interesting success stories, mostly to do with difficult
                                             exercises (such as problems from the International Mathematical Olympiad), but also with
                                             conjectures [9] formulated for the purpose of verifying whether the artificial intelligence
                                             could prove it. In this paper we report a theorem proving feat achieved by ChatGPT by
                                             using a protocol involving different prover and verifier instances of the gpt-5 model working
                                             collaboratively. To make sure that the produced proofs do not suffer from hallucinations, the
                                             final proof is formally verified by the lean proof assistant, and the conformance of premises
                                             and conclusion of the lean code is verified by a human. Our methodology is by no means
                                             complete or exact. It was nonetheless able to solve five out of six 2025 IMO problems, and
                                             close almost a third of the sixty-six number theory conjectures in [5].



                                        1    Introduction

                                        This paper describes a protocol, involving the OpenAI Application Programming Interface (API)
                                        with a minimal human interaction, which was able to solve five out of six problems of the
                                        International Mathematical Olympiads (IMO), close almost a third of sixty-six open conjectures
                                        on cyclic numbers proposed in [5], as well as discover and prove several new theorems in a
                                        variety of fields of mathematics. The human intervention only arises to verify that a formal
                                        version of the generated theorem statement is consistent with its semi-formal natural language
2


description. More precisely, we only ask the human to verify the conformance of all premises
and the conclusion of the formal and the semi-formal versions of the proof∗ .

   Alan Turing conceived his computational model of the computer not only as a mechanical
way of performing computations [30], and not only as a precise definition of the Leibnitzian
calculemus dream, with roots in Renaissance steganographers, whose influence crept through
the centuries to reach Hilbert’s tenth problem and its vague “finite process” to solve polynomial
equations in integers. In the last years of his life, Turing defined machine intelligence by means
of a probabilistic game played between a (Turing) machine and a human exchanging messages
in natural language [31]. If a human evaluator with access to the messages fails to reliably tell
the machine apart from the human, the machine is deemed to be as intelligent as the human.

   This test, initially called by Turing the “imitation game”, but today simply known as the
“Turing test”, held a prominent position in Artificial Intelligence (AI) literature since its birth.
In [31], Turing forecasted that by the year 2000 people would have attuned to computers being
“intelligent” (according to his definition thereof). Over the years, commentators and AI experts
made all sorts of predictions about the time when the Turing test would be passed by a computer.
Most of them predicted the latest possible times at which they could reasonably expect to be
alive [2].

   The Turing test situation changed abruptly with the advent of Large Language Models
(LLM), a Machine Learning (ML) paradigm consisting in complicated architectures of intercon-
nected Artificial Neural Networks (ANN) of extremely large size, and trained on huge textual
datasets to predict the next word of an answer to a question posed by a human in natural
language. Since the mid-2020s, the Turing test was passed by ChatGPT gpt-4.5 LLM [14]. We
remark that no theory of learning involving ANNs guarantees exact results: typically, we are
more in the “probably approximately correct” (PAC) setting [32]: with respect to an unknown
ground truth, the likelihood of producing more or less correct predictions from sufficiently large
training sets is reasonably high. Moreover, it is well known that LLMs suffer from “hallucina-
tions”: wrong predictions involving mistakes that no humans would make [12].

   Rather independently of these developments, computer science devised computer programs
to help humans prove [16] and verify [7] theorems by means of formal language constructs. Since
checking is easier than solving, there are more verifiers than provers. Unlike the PAC learning
theory mentioned above, all proof assistants (verifiers) and most theorem provers are based on
formal systems (FS) [27], and therefore give rise to exact and guaranteed results.

   The whole endeavour proposed herein, then, appears a bit paradoxical: we are employing an
LLM without exactness guarantees, trained on natural language text and prone to hallucinations,
in order to prove formal theorems. But consider the following: (i) ANNs have been devised by
analogy with the neurons that humans have in the brain; (ii) nontrivial theorem proving has
been an exclusively human activity until very recently; (iii) humans do not come with guarantees
either, and may also hallucinate, or in any case get proofs wrong. So that paradox is only
apparent.

   The essential point is that proving theorems requires creativity, and intuition plays a promi-
nent part in human creativity: analogies, metaphors, similitudes, even daring comparisons that
short-circuit logical arguments are often used by humans in devising (or discovering?) proofs.
   ∗
     At the time of publishing this technical report we are still carrying out the human part of the protocol: no
proof should not be trusted yet.
1       INTRODUCTION                                                                                         3


Automated theorem provers, being mostly based on FS, heuristically explore the countably infi-
nite digraph of formal sentences derived from given axioms by recursively applied inference rules:
the validity of every sentence follows from its premises. Since this graph is infinite, the search
for the path leading from the axioms to the conclusion of the desired theorem statement may be
indefinitely long, and establishing unprovability yields a non-terminating search (this is exactly
the “Entscheidungsproblem” that Turing settled in [30]). It seems that LLMs may provide useful
shortcuts in proving theorems, which is an invaluable feature even at the cost of inexactness and
errors. Human brains, errors notwithstanding, establish proofs or the unprovability of formal
sentences by a different process, without guarantees but generally with better success rates than
those achieved by FS-based computer programs. The most visible link between humans and
LLMs being natural language, there is a remarkable interest in using natural language (and thus
LLMs) in having computers prove theorems.

    The rest of this paper is organized as follows: Sect. 2 summarizes the relevant literature.
In Sect. 3 we describe our protocol in depth, and analyse its strengths and weaknesses. Then
follows the description of the implemented system in Sect. 4. The results are described in Sect. 5.
Sect. 6 concludes the paper.


1.1      Contributions of this paper

The main contribution of this paper is a conceptually simple protocol, involving the repeated
interaction of different LLM-based computational agents and terminating with a final human
verification, that proves theorems. This protocol solved five out of the six problems of the 2025
IMO, exactly like the specialized (and as far as we know undisclosed) LLMs built by Google
DeepMind and OpenAI; it solved several theoretical conjectures in [5]; and it discovered and
solved new conjectures in three fields of mathematics (see Sect. 4.1.1 and 5.3)1 . Obviously, the
protocol does not guarantee that every conjecture will be proved or disproved: after a given
amount of time it can give up empty-handed.

    A smaller contribution is the minimization of the human interaction, which is limited to ver-
ifying the conformance of premises and conclusion between the formal and the natural language
versions of the proof of interest. This is enough to guarantee correctness of the formal version of
the proof (Sect. 3.2) despite the possibility of hallucinations (Sect. 3.2.1), under the assumption
that the human does not make any mistakes.

   A more subtle contribution, which may not sound new to LLM experts but may surprise
traditional computer scientists, is the idea that “programming with an LLM” involves rhetorical
skills in giving natural language instructions to LLM-based agents to tell them how to behave.
Much like the grammarians of the late middle ages who fought over the vocative of ego, LLM
programmers often resort to various imperative forms “to be”: we tell our LLM agents “you
are a meticulous researcher”, “be cautious”, “be concise”, and even “you are a senior research
assistant who is finding advanced sources in the literature to tackle an open problem”. These
prompts are passed to LLM instances to prepare them for their work and define their output (see
Sect. 4.1). The new field of computational pragmatics is arising from such needs [3, 25, 18], but
most of the literature takes “prompt engineering” to mean different data structures (sequences,
    1
    None of these announced results is sure yet: the proofs have been produced in semi-formal natural language,
but the verification process involves a mixture of human and automatic work, which takes longer than initially
anticipated
4


trees, tables) containing inter-dependent prompts and corresponding answers, all of which are
used to provide additional training to the LLM at hand. The prompts we use in our paper are
of the “zero-shot” type with no additional training [19, 1].


2     A review of the relevant literature

Contributions reporting the successful use of LLMs to prove theorems are extremely recent:
so recent, in fact, that the corresponding articles are often in the form of unrefereed technical
reports.

   Such contributions describe either fully automated or semi-automated approaches. In fully
automated ones, LLMs are asked to devise proofs, and then encode them as programs for proof
assistant languages, which are then executed to either deny or accept the proof produced by the
LLMs. Wrong proofs are either discarded or modified [4, 38]. In semi-automated approaches
there is at least one step of the protocol that is assigned to a human: at best this is a verification
step [9], but sometimes humans also guide2 the LLM around invalid inferences [24].

   The problem of LLM “hallucinations” is by now well known [12]. Employing a fully automated
process for proving theorems therefore exposes the proof to the risk of hallucinations. The
interaction with a proof assistant such as lean [7] decreases the risk of hallucinations, but it is
not eliminated [21, 28, 36].

   Consider this scenario: the LLM generates a proof and the corresponding proof assistant code,
both of which may be subject to hallucinations. The hallucinated code may still be accepted
as valid by the proof assistant as long as the premises lead to the conclusion by inference, but
these premises may not correspond to those of the LLM-generated proof. While we agree with
[21, 36] that such an occurrence is unlikely, we also think that a wrong proof of this kind would
be extremely difficult to catch by humans exactly because it is known to have been checked by a
proof assistant. Our process overcomes this difficulty by introducing a limited human interaction:
a human verifies the conformance of all premises and conclusion of the proof between the proof
assistant code and the LLM-generated proof3 .

   The interaction of humans and AI agents in the context of proving theorems is not new. See
for example the end of [28, §2] for a few cases. In [28], the interaction between the human and
the AI agent is based on the agent being a “co-pilot”: the human leads the investigation but
can ask the AI agents for suggestions. In our case the human is limited to a verification task to
be carried out only once, at the end of the computer-based process.

    Since we describe a protocol involving a human step rather than a fully automated process,
   2
     One of us (LL) has once enlisted the help of ChatGPT to reconstruct a proof of a result he had seen in
the past but had forgotten, and could not afford the time to reconstruct by himself: the creativity originated,
through the semi-formal use of natural language, from both parties (human and machine), in a protocol involving
ChatGPT as the prover and the human as the verifier. The final verification was embodied by the full human
re-write of the proof in the context of the paper where the proof was needed. Moreover, Scott Aaronson reported
on Sept. 27th, 2025 on his blog that he and a co-author used ChatGPT to obtain the proof of a lemma needed in
a larger scope; he believes that they would have been able to prove this lemma without ChatGPT “in a week or
two”, and adds that the proof was obtained by a prover/verifier protocol where he was the verifier.
   3
     Humans also make mistakes when proving theorems, but at this stage of LLM technology development we
should be happy if computers do not make more mistakes than we do.
3   A THEOREM PROVING PROTOCOL                                                                   5


we do not test our protocol on known benchmarks [26]. Instead, we test our methodology on:
(i) the six problems in the 2025 IMO, (ii) a set of sixty-six open conjectures in number theory
taken from the recent paper [5], (iii) a set of conjectures (in three different mathematical fields
chosen by us authors) found an LLM agent in a pre-processing step in our protocol.

    Comparative success stories in proving theorems using LLMs focus either on solving IMO
problems [37, 22, 35], or conjectures in combinatorial optimization formulated for the explicit
purpose of testing the system [9]. We note that neither of these are “open problems” in the
literature. Interestingly, though, the system described in [9] gave enough evidence to its authors
that one of their own conjectures designed to test their system (which the system could not
prove) was more difficult than the authors had envisaged, and is now an open problem.

   By contrast, the protocol described in [24] really did advance the knowledge related to the
“cap set problem”, i.e. finding the largest possible set of vectors in Zn3 such that no three of
them sum to zero. While the exact answer is only known for a handful of small values of n, the
methodologies proposed by [24] improved the upper bound for n = 8.

  Overall, we believe that our approach is the first to close open conjectures from a mathe-
matical paper in the literature. Our belief is strengthened by the negative answer provided by
ChatGPT (using the gpt-5 LLM) to the question, posed on Sept. 23rd, 2025:

      Excluding IMO problems and “open problems” stated by the authors of the paper
      describing the LLM that solved them, can you find a list of papers or technical re-
      ports that report that an LLM actually solved truly open mathematical conjectures,
      namely conjectures that can be found in a refereed (mathematical) paper?

The answer (which took 32s of LLM “thinking”) concluded with the sentence “under your strict
definition the list is empty today.” Relaxing the criterion to “nontrivial, peer-reviewed new
theorems not previously stated as a conjecture” the list provided by ChatGPT (after 26s of
“thinking”) reduces to the paper [24] already mentioned. Since the research in this field is very
recent and very intense, we have no doubt that there will soon be other systems that can close
open conjectures from the literature.


3     A theorem proving protocol

The protocol we propose employs a Test-Time Verify-Revise (TTVR) loop followed by a human
verification. TTVR is employed by analogy with the human process of ssolving hard tasks:
devise an initial (possibly wrong) solution, check it, correct it, and repeat.


3.1   Agents

The TTVR loop in our protocol involves two computational agents that work side-by-side: a
prover and a verifier interact in an alternating fashion. Both agents are gpt-5 LLMs that have
access to a Python interpreter. The difference between one and the other is determined by the
phrasing of system-prompts and user-prompts (more on this in Sect. 4.1).
6


    Given a theorem statement T (consisting of premises and the conclusion), at the i-th iteration
of the loop the prover proposes a proof Pi , and the verifier either accepts it or rejects it. If the
verifier accepts Pi as a valid proof, the loop terminates; if the verifier rejects Pi as invalid, it
provides evidence Vi of the issue and the position pi in the proof Pi where the issue arises. The
proof Pi , the position pi , and the evidence Vi are passed to the prover as input for the next
iteration i + 1. We set a maximum number N of iterations of this loop, after which termination
is enforced even if a proof was not found.

   Suppose that the loop terminates at the n-th iteration (where n ≤ N ) with a proof Pn that is
accepted by the verifier. Then the prover is asked to formalize the proof into the formal sentence
π in a proof assistant programming language (we use lean [7] in our implementation). Next, a
human checks that all premises of π and its conclusion are a correct formal restatement of the
premises and conclusion of Pn (which are equal to those of T ) written in semi-formal natural
language. If this human test is successful, π is passed to the corresponding proof assistant for
the final validity test. If this test is also passed, the proof Pn is deemed to be valid. In all other
cases the proof is rejected.


3.2   Correctness

This protocol has an interesting twist, which can be described by means of a remark to the
following correctness result. Let T be statement of the theorem being proved, and assume that
neither the human nor the proof assistant can ever be wrong in performing their verifications.

3.1 Proposition
For any pair (P, π) where P is a semi-formal natural language proof of T and π is a formalized
proof of T , if (P, π) are accepted by the protocol above, then π is a valid proof of T .

Proof. Since the premises of P and π and their conclusions have been certified by the human
to have the same formal semantics, and the rest of the proof has been certified by the proof
assistant to constitute a valid inference chain from the premises to the conclusion, π is a valid
formal proof of T .                                                                            2


First, we remark that the encoding of the symbol T is unspecified: it does not matter whether
it is expressed in the semi-formal natural language used by human mathematicians and LLMs
or in formal language, because the human in the protocol certifies the semantic equivalence of
premises and conclusion between P and π, and the theorem statement T consists exactly of
those premises and conclusion.

    Secondly, and most importantly, the almost trivial Prop. 3.1 was stated to emphasize its only
non-trivial feature: it does not prove that P is a valid proof of T , but only that π is. The reason
is the hallucinating scenario already considered in Sect. 2. To keep human interaction minimal,
we only require that the human should certify conformance of premises and conclusions of P and
π, but not of the whole proof. There is a chance that either P , or π, or both, were actually the
fruit of LLM hallucinations. But as long as: (i) the theorem statement T was correctly stated
as input to the protocol, (ii) its formalized premises and conclusion in π were certified correct
by the human, and (iii) the formalized proof was certified correct by the proof assistant, then π
is a valid proof of T , even though the LLM might have hallucinated.
3       A THEOREM PROVING PROTOCOL                                                                            7


3.2.1     Hallucinations in the protocol

We think that the occurrence of a set of LLM hallucinations that impact the prover/verifier loop
and the proof assistant code generation is exceedingly rare, but not impossible. We also think
that humans, at least those that are conversant with FS and contemporary computer science,
tend to trust a proof that is labeled as “formally certified” beyond all doubt. It would therefore
be catastrophic if a wrong proof of this kind were to be accepted at large. Our protocol is
designed to deliver correct formal proofs even in the case of LLM hallucinations. More precisely,
most cases of LLM hallucinations will result in failure to deliver any proof; but in the minuscule
chance that hallucinations in prover/verifier and lean code generation should deliver a valid
formal proof, that proof will be recognized as valid for T by the human and the proof assistant,
and therefore returned to the user as valid by our protocol.

    A creative way of interpreting this situation is that we recognize that theorem proving is the
province of formal languages, but that the creativity necessary to construct (or find?) a proof
requires a set of very human skills, many of which manifest themselves in natural language, and
remain present in the enormous set of natural language knowledge stored in LLMs. By several
accounts (e.g. Hardy about Ramanujan), mathematicians often derive their ideas for proofs in
flashes, illuminations, and even dreams4 . We like to think that if an LLM has an incredibly rare
pair of hallucinations leading to a valid formal proof, it might be considered, rather arbitrarily
but satisfactorily, as an excellent analogy of the mathematician’s illumination. And our protocol
saves those proofs.


3.2.2     Further remarks

Here are a few additional remarks about our protocol.

    1. A practical issue of our protocol is the lack of reproducibility. This stems from the fact
       that the OpenAI pipelines include a probabilistic system for selecting its output in a likely
       set. In practice, the impact is that one should save all of the valid proofs found by our
       system, because, in the worst case, they may not be found again.

    2. The prover/verifier TTVR interaction loop in our protocol is reminiscent of Interactive
       Proofs (IP) Systems [10], but for now this is just an analogy rather than a correspondence.
       Every result in the IP complexity class is based on a probabilistic verifier that can challenge
       the prover with random bits. Although by remark 1 the verifier is actually probabilistic,
       by the same token the prover is also probabilistic. We are unsure whether this warrants
       a complexity study of our protocol under the banner of IP. The fact that we repeat our
       loop for at most a given number N of times is unlikely to be admissible in IP.

    3. Our protocol could be restricted to proving theorems that can be formally expressed by
       existential second-order sentences: by Fagin’s theorem [8], such “theorems” are equivalent
       to decision problems in the complexity class NP. This would be tantamount to using
       our protocol to find solutions to instances of NP-complete problems. The complementary
       view is that of proving propositional tautologies (which is in co-NP [6]). We do not think,
       however, that this specific use of our protocol will be very fruitful, as sat solvers are much
    4
    By our own experience, the amount of illuminations/dreams leading to good ideas that turn into actual proofs
are a tiny minority, but they are precious nonetheless.
8


      better suited to this task. On the other hand, only problems are hard, not single instances:
      therefore there is some hope that there could exist some instance of an NP-hard problem
      where traditional methods such as Branch-and-Bound (BB) will take a longer time than
      our protocol. So far we have not tested this idea.

    4. The other well-known link between proofs and algorithms is the Curry-Howard corre-
       spondence [34]: proofs that can be framed in intuitionistic logic (e.g. no excluded middle
       arguments) correspond to terminating algorithms. Restricting our protocol to intuition-
       istic logic might involve convincing the prover agent to exclude the use of certain proof
       techniques. The benefit of such a restriction might simply be a computable certificate
       of validity. Currently, we cannot estimate the additional value of such a certificate with
       respect to the ACCEPT/REJECT bit of output of a proof assistant that can also tackle
       classical (non-intuitionistic) logic.


4     System implementation

The protocol presented in Sect. 3 is similar, albeit not identical, to several other approaches in
the literature (see Sect. 2). The only theoretically interesting innovation is the limited inter-
action with a human at the very end (see Prop. 3.1 and the remarks below it), but this just
ensures a correctness guarantee: it cannot explain the capability of our protocol for solving open
conjectures and discovering new theorem statements (see Sect. 5).

  In this section we discuss some implementation features that we believe are key to this success:
namely agents and context. The rest of the TTVR implementation is a standard loop coded in
Python, and therefore we do not think that it deserves much credit for the system’s success. Still,
we make some suggestions about different types of agent interactions which might considerably
improve the system’s efficacy.


4.1    Agent defined by prompts

Our protocol is implemented using the OpenAI API. The LLM we employ is gpt-5. The TTVR
loop distinguishes between the first iteration and the subsequent ones by means of different
prompts to the various instances of gpt-5. The prompts consist of imperative instructions
written in natural language. Each gpt-5 instance receives a system prompt and a user prompt
through the API (the ChatGPT user interface only allows the specification of the user prompt).
Here are more details about the prompts we use.

    • Prover at the first iteration: system prompt: specifies that this prover should behave like
      a rigorous mathematician, gives the output format, and prescribes further rules to be used
      in questions of plane geometry (this is mostly useful for IMO questions), and gives strict
      guidelines about focusing on the proof itself rather than produce bullet lists of literature
      review.

    • Prover at the first iteration: user prompt: passes the theorem statement provided in
      semi-formal natural language to the prover, repeats some of the recommendations of the
      system prompt but applied to the proof rather than to general instance behaviour.
4   SYSTEM IMPLEMENTATION                                                                           9


    • Prover at other iterations: system prompt: repeats the recommendations for the prover
      at the first iteration, and adds the recommendation for: (i) understanding the core idea
      and structure of the existing proof so far, (ii) fixing the proof based on the verifier feedback
      with minimal necessary changes if possible, otherwise produce a new correct proof.
    • Prover at other iterations: user prompt: passes the theorem statement, the previous
      proof, and the verifier feedback to the prover, and repeats some of the recommendations
      of the system prompt but applied to the rpoof rather than to general instance behaviour.
    • Verifier at all iterations: system prompt: specifies that this verifier should behave like a
      rigorous mathematician, gives the output format, and repeats some of the recommenda-
      tions already listed for provers.
    • Verifier at all iterations: user prompt: passes the theorem statement and the current
      proof to the verifier, and prescribes a YES/NO answer where NO must come with an
      brief explanations of all logical flaws found, without including suggestions for fixes; flag as
      wrong all proofs involving appeals to literature status.


4.1.1    Research mode agents

So far, we have described a system which, given a theorem statement T , attempts to find
its proof: this is the default mode of operations. On top of this system we have also built
an advanced “research mode” that, given the informal description of a mathematical goal, it
attempts to find new and interesting theorems towards that goal, and then attempts to prove
them.

   The research mode is implemented by means of four more agents (i.e. other gpt-5 instances
with specific prompts).

    • The literature reviewer is a meticulous research assistant that searches the existing
      literature for relevant results in the theorem at hand.
    • The context preparer is a senior research assistant that searches for auxiliary references
      for a difficult open problem.
    • The predictor is a researcher who proposes new conjectures from looking at the literature
      in a certain field.
    • Given a theorem T and a proof P , the refiner simply recognizes whether P proves or
      disproves P ; if the latter, the refiner logically inverts T so that P proves ¬T .

We note that all of these agents are deployed once only, either as pre-processing or post-
processing (refiner) with respect to the TTVR loop. Moreover, the context preparer is
also used in the pre-processing of the default mode when deployed on an conjecture rather than
a theorem.


4.2     Advanced agent interactions

The simple TTVR protocol described above would certainly benefit from multiple provers and
verifiers working in parallel (possibly organised by prover/verifier “master” instances). Because
10


of OpenAI subscription limitations and cost, we were only able to allow for two verifiers working
sequentially so as to increase the chances of finding faults in the single prover’s work. The
prompt of the second verifier is a slight variant of that of the first verifier (described in Sect. 4.1
above).

   It is not hard to imagine more advanced interaction schemes. Within the same simple
TTVR loop, one could deploy more complicated message-passing schemes (through sophisti-
cated prompts) between provers and verifiers. Prompts could even be written automatically by
agents conditionally on the progress made on the proof.

   The elementary loop itself could be replaced by a full-fledged algorithm that coordinates the
agents’ work. As an example, consider the well-known BB algorithm for integer programming
based on linear relaxations [17]. Theorems can be relaxed by strenghtening premises or weaken-
ing conclusions: by assigning a measure to such relaxations, one could devise a theorem-proving
branch-and-bound algorithm that automatically devises a decomposition of the theorem, thereby
making it easier to derive a proof. This would yield a form of nontrivial recursion proof for the
given theorem.

   Unfortunately (for us), implementing, fine-tuning, and testing such schemes would require
an exceedingly costly subscription to OpenAI. We therefore encourage OpenAI researchers to
consider the ideas in this section5 .


4.3         LLM Context

According to the OpenAI API documentation, each gpt-5 instance has a context window of four-
hundred thousand tokens (the word “token” is to be interpreted in the light of natural language
parsing). If we used a single gpt-5 instance for all provers and verifiers at every iteration we
would quickly fill the context window, which might lead to degraded performance and increase
the chances of hallucinations [33]: therefore each of our agents is used once and then discarded;
new agents are created in the subsequent TTVR loop iterations.

   Moreover, since the system has to correct its own wrong proofs, we think that the context
bias might prevent the prover from exploring new ideas. For these reasons, every instance of
gpt-5 is discarded after use. Every prover and verifier at each iteration is a new instance.


4.4         Human interaction issues

In practice, the human interaction, albeit limited to a verification at the end, remains very
time-consuming. This is mostly due to the limited ability shown by gpt-5 in converting its own
natural language proofs into formal lean codes. So, although our protocol does minimize human
interaction, this interaction remains considerable, because the human has to construct the whole
lean code from a relatively thin base. A more intensive LLM training using lean codes could
improve the situation. This is another situation (as that described in Sect. 4.2) which would be
better tackled by OpenAI.

   In order to reduce human interaction, we had initially instructed OpenAI’s Codex interface
to reduce to “axiom” any proof step that it could find by means of a web search. This reduced
     5
         Or, alternatively, to either employ us for this purpose or at least give us free unlimited subscriptions!
5   RESULTS                                                                                                     11


the extent of lean checking (the formalization was partial) but made it possible to run a limited
certification step at the end of our protocol6 .


5     Results

In this section we give an account of our system’s achievements. We note that gpt-5 was trained
on data up to 2024, while the problems we submitted to our system all date from 2025. Therefore,
the LLM in our TTVR loop cannot have been contaminated in the sense of [29], namely that
its training set cannot contain any IMO 2025 information, nor any solution to conjectures in [5]
(the situation for the research mode conjectures in Sect. 5.3 is more fluid in this respect: some
contamination could be possible). We also emphasize the fact that our prompts do not include
instructions to the LLM to the effect of checking the literature; on the contrary, they discourage
the production of bullet lists with literature references.

   Given that our system is based on a TTVR loop, we consider the number of iterations
required to arrive at a solution as an index of difficulty of the problem for our LLM-based
protocol. Accordingly, we compiled some tables in this sense (Tables 2-6).

   The number of iterations N for the TTVR loop was fixed at 15 for the whole set of ex-
periments. Another constant M = 5 was used to abort the loop after an excessive number of
“bad gateway” error messages from the OpenAI API: typically, harder problems run into longer
reasoning time, which increases the chances of such API errors.


5.1    2025 IMO Problems

The 2025 edition of the IMO contained six problems. Our system solved five out of six problems
(it could not solve the sixth one), which is the same achievement announced by the specialized
and undisclosed LLMs used by OpenAI [35] and Google DeepMind [22] for the task. Both
problem statements and solutions can be obtained from the PDF document at evanchen.cc.
The length of the human proofs of these problems have lengths reported in the second row
(labelled “human”) of Table 1. The human proof lengths are expressed in number of space-

                              problem         1       2      3      4      5      6
                              human         321     495    320    599    434    639
                              LLM          1105     490    604    690    434    NA


Table 1: Human versus generated proof lengths for the IMO 2025 problems in number of tokens.
Drawings in human proofs were not counted in their lengths.

separated tokens extracted by the ASCII representation of the PDF referred to above. The
LLM-generated proof lengths are expressed in number of space-separated tokens in the proofs
given in MarkDown language [11] with inline LaTeX.
    6
      We have since enlisted the help of human experts in analytic number theory to help us verify the solutions of
conjectures in [5]. Some of them were found to be incorrect despite the limited formalization effort; and not all
of them have been yet vetted.
12


5.1.1         Notes about the proofs

We now look at the five proofs of problems 1–5 in more detail.

Problem 1. The human and computer-generated proofs are different, and give rise to very dif-
           ferent proof lengths in Table 1. Our system failed to consider a shortcut taken by
           the human proof.

Problem 2. The two proofs are different, even though the proof lengths are similar. The human
           proof is more compact and geometrically clearer to a human reader. The computer
           proof is algebraic (instead of geometric) insofar as it uses the complex plane to
           reason about plane geometry (this was due to an explicit instruction to the LLM
           on our part through a prompt). It relates to the human proof similarly to the way
           Miles Edwards’ proof of Heron’s formula relates to most other proofs of the same
           result (see [20, §2] for more details).

Problem 3. Overall, the structure of the two proofs is the same; the human proof is more
           compact but also leaves more to be worked out by the reader w.r.t. the computer
           proof, which explains the proof length difference. The case analysis at the end differs
           in the details.

Problem 4. The two proofs are almost the same. Both proofs state the solution nonconstruc-
           tively, and then prove its correctness. The differ only for some minor details (con-
           sistently with the similar proof lenghts).

Problem 5. The two proofs are essentially the same, but differ on a few details (the identical
           lengths are just a coincidence). Both proofs state the solution nonconstructively,
           and then prove its correctness. The human proof looks “neater” to a human reader,
           but the computer proof gives more details, which makes the inferences easier to
           understand. There is a point at which the human proof infers correctnes from the
           fact that the value of a certain variable belongs to a given closed real interval having
           zero lower bound; in the same situation, the computer proof simply assigns the zero
           value to the variable. In this case it seems that the human proof contributes more
           knowledge even if that knowledge is not useful to the proof itself, while the computer
           proof states the weakest premise for the inference. Lastly, the fact that there is a
           unique value of the main game parameter for which there is no winning strategy
           for either player is stated by both proofs, but it is only explicitly proved by the
           computer proof.


5.1.2         Qualitative comparison of our system compared to others

As mentioned above, we use the number of TTVR iterations as an index of problem difficulty for
our system. According to Table7 2, the easiest problem for humans (Problem 1) is the hardest
for our protocol; the second-hardest is Problem 2. We note that both problems are geometric.
The benchmark found in [29] agrees on Problem 6 (no LLM-based approach could solve it),
and approximately also on the relative ease with which such approaches can solve Problems
3, 4, and 5. This benchmark tells a rather different story for Problems 1 and 2: Problem 2
     7
         Missing entries correspond to ongoing tests.
5       RESULTS                                                                                                  13


                                   problem        1    2    3    4    5      6
                                   |itn|          9    7    3    6    5     NA
                                   correct?       Y    Y    Y    Y    Y     NA
                                   certified?               Y               NA


Table 2: Number of iterations required by the TTVR loop to arrive at a solution of the IMO25
problems, together with a human evaluation of correctness and a lean certification.


is much more difficult than Problem 1 — in fact it is the most difficult problem in the set
1–5. Our protocol, however, finds that the opposite holds: Problem 1 is harder than problem
2 (admittedly according to a different measure than that of the benchmark). In general, given
that LLMs are based on symbolic textual training more than on geometric drawings, one might
guess that LLMs find geometric problems harder to solve than other types of problems. Our
tests provide one more piece of evidence to reinforce confidence in this guess.


5.2       Conjectures of primes and cyclics

We considered number theory as a promising field to test our system for several reasons: (i) it
is a cornerstone of pure mathematics; (ii) many of its theorems and conjectures, albeit difficult,
can be formalized using first-order or second-order logic; (iii) many of its theorem statements
and conjectures can be understood by people possessing limited mathematical education. It
promised to be a hard benchmark with potentially wide audience.

   For this particular test we wanted to benchmark the ability of our system to prove stated
theorems rather than its creativity to discover new theorems. But instead of conceiving our own
conjectures (as [9]) we thought the exercise would be less biased if we used existing ones. While
perusing the OEIS [13] we came across a conjecture which led us to [5], an article that lists 66
conjectures about primes and cyclic numbers.

    Cyclic numbers are analogous to prime numbers in a certain sense, and therefore it makes
sense to conjecture that many results known for primes should also apply to cyclics. The
definition of a cyclic number is as follows. Let n be a positive integer, and consider the cardinality
m of the set C of positive integers r < n and relatively prime to n (obviously, m is a function
of n). If n, m are relatively prime, then n is cyclic. It is analogous to the definition of “prime”
insofar as they both involve the comparison of an integer with the cardinality m of a set of
numbers r < n that have a certain relationship with n concerning integer division. If the set is
that of the divisors of n and m = 1 (only r = 1 < n divides n), then n is prime; if the set is
that of the coprimes of n and gcd(n, m) = 1, then n is cyclic. To render notation more compact,
we introduce Euler’s totient function ϕ(n) = m to be the cardinality of the integers r < n and
coprimes with n, and define n to be cyclic if gcd(n, ϕ(n)) = 1. Note that, if n is prime, then r
is coprime with n for each r < n, so m = n − 1, and since gcd(n, n − 1) = 1 for each integer
n, each prime is also cyclic. The paper [5] goes on to list the 66 (numbered) conjectures about
cyclic numbers.

    Our system produced a proof8 or refutation for twenty out of the sixty-six conjectures: namely
    8
   In analytic number theory, a “proof” can only be correct, otherwise it is not a proof, but a fallacious argument.
An “argument” may be correct or incorrect, and a correct argument provides a proof. Moreover, one does not
14


3, 6, 9, 14, 17, 20, 32, 35, 36, 37, 41, 42, 47, 52, 53, 54, 56, 59, 60, 61, with seventeen proofs and
three refutations (35, 53, 59). Seven out of the sixty-six conjectures, namely 2, 3, 4, 36, 37, 52,
53, had already been closed by C. Pomerance [23] prior to the publication of [5], by personal
communication to its author. The five conjectures solved by Pomerance that appear in our list
(3, 36, 37, 52, 53) must therefore be removed from the list of “open conjectures”. This leaves
our system with 17 (previously open) conjectures for which it obtained a proof. In Table 3 we

        conjecture    3 6 9 14 17 20 32 35 36 37 41 42 47 52 53 54 56 59 60 61
        |itn|         4 9 9 6 1 9 3 3 4 8 15 1 9 9 1 9 9 1 1 1
        O or C        C O O O O O O O C C O O O C C O O O O O
        P or R        P P P P P P P R P P P P P P R P P R P P
        correct?      ? Y Y N Y Y Y N ? ? Y Y Y ? ? Y Y Y Y Y
        certified?    ? Y Y Y Y             ? ? Y          ? ?


Table 3: Number of iterations required by our TTVR loop to produce either correct and lean-
certified or incorrect P roofs or Refutations of the conjectures in [5].

report, for each proof produced9 by our system: the number of TTVR iterations (|itn|), whether
the conjecture was open or already closed (O/C ), whether the conjecture was settled by proof or
refutation (P /R), whether the authors of this paper (who are not specialists in analytic number
theory10 ) think that the semi-formal natural language proofs are correct or not, and whether the
lean certificate is correct and conformant with the premises and conclusions of the corresponding
proofs.

    We note that some of the confirmed conjectures have been “closed” only partially, i.e. in the
asymptotic sense, not in the absolute one. For example, the proof of Conjecture 6 shows that
there is an n0 such that for every n > n0 the conjecture holds, but we have no idea about this
n0 , so Conjecture 6 is still open “for all n ∈ N”. This is also the case for Conj. 32.

   In one of the refuted conjectures, namely Conj. 59, our system has provided a formally correct
refutation that would be unsatisfactory to any human mathematician: it addresses one of finitely
many exceptions, providing no refutation for the asymptotic part.

   The most difficult conjecture to solve, according to the number of TTVR iterations11 , is 41.
We report it here as an example, as Thm. 5.1: cn is the n-th cyclic number, and log is the
natural logarithm.

  5.1 Theorem (Third Firoozbakht conjecture on cyclics)
  For every k ∈ N, there exists a least m ∈ N, call it N (k), such that, for all n > N (k), we
         1/(n+k)      1/(n+k+1)
  have cn          > cn+1         .



use “theorem” to just indicate the theorem statement: a theorem is the statement followed by its proof. Because
the subject matter of this paper is the automated generation of proofs rather than analytic number theory, we
abuse those rules to keep descriptions more compact: proofs and refutations may be correct or incorrect.
   9
     Missing entries in Table 3 correspond to ongoing tests.
  10
     These proofs ar enow being vetted by experts in the subject matters, who have already invalidated some of
the proofs we believed to be correct, and have yet to go through the complete list.
  11
     The “?” entries in Table 3 are due to a mishap in our file management: we are re-running these tests.
5    RESULTS                                                                                            15


                                                           e
       Proof. Let L(x) = log3 x = log log log x for x ≥ ee and let

                              C(x) = #{m ≤ x : gcd(m, φ(m)) = 1}.
                                                                                                   e
    By Pollack’s refinement of Erdős’ asymptotic, there exist absolute constants X0 ≥ ee and
    A0 > 0 such that for all x ≥ X0 ,
                       1     γ     q                                      π2                 A0
       C(x) = e−γ x        −     +      + R(x)  ,              q = γ2 +        ,   |R(x)| ≤         .
                       L(x) L(x)2 L(x)3                                     12                L(x)4

    Define the smooth comparison functions
                                 1     γ     q    A0 
                  F± (x) = e−γ x     −     +     ±                            (x ≥ X0 ),
                                 L(x) L(x)2 L(x)3 L(x)4

    so that for x ≥ X0 ,
                                     F− (x) ≤ C(x) ≤ F+ (x).

       1) Uniform lower bound for F−′ . Write ℓ = L(x) and G(ℓ) = ℓ−1 − γℓ−2 + qℓ−3 − A0 ℓ−4 .
    Since L′ (x) = (x log x log2 x)−1 ,
                                               h                     i
                                  F−′ (x) = e−γ G(ℓ) + x G′ (ℓ)L′ (x) .

    Because G′ (ℓ) = −ℓ−2 + O(ℓ−3 ), there exist X1 ≥ X0 and C1 > 0 such that for all x ≥ X1 ,

                                                          C1
                                  x G′ (ℓ)L′ (x) ≤    2
                                                                        .
                                                     ℓ log x log   2x

    Moreover G(ℓ) = ℓ−1 + O(ℓ−2 ). As ℓ → ∞ and log x log2 x → ∞, enlarging X1 if needed
    we obtain                              1 
                            F−′ (x) ≥ e−γ            (x ≥ X1 ).                       (1)
                                           2L(x)
    In particular F− is strictly increasing on [X1 , ∞) and, since F− (x) ≫ x/L(x), one has
    F− (x) → ∞ as x → ∞.

       2) One-step growth via level-crossing of F− . Fix n with cn ≥ X1 and set y = cn , so
    C(y) = n and F− (y) ≤ n. Because F− is continuous, strictly increasing, and unbounded,
    there is a unique ∆(y) ≥ 0 such that

                                      F− (y + ∆(y)) = n + 1.

    Then C(y + ∆(y)) ≥ F− (y + ∆(y)) = n + 1, hence the first point where C reaches n + 1
    (namely cn+1 ) lies in (y, y + ∆(y)]. Thus

                                      0 < cn+1 − cn ≤ ∆(y).

    By the mean value theorem there exists ξ ∈ [y, y + ∆(y)] with

                              F− (y + ∆(y)) − F− (y) = F−′ (ξ) ∆(y).
16


 Because F− (y + ∆(y)) = n + 1 ≥ n ≥ F− (y), the left-hand side is ≥ 1, so by (1)
                                                    1
                                        ∆(y) ≤    ′     ≤ 2eγ L(ξ).                         (2)
                                                 F− (ξ)

 As L(t) = o(tε ) for any fixed ε > 0, there exists X2 ≥ X1 such that 2eγ L(t) ≤ t/4 for all
 t ≥ X2 . Suppose y ≥ X2 . If ∆(y) ≥ y, then from (2) we get ∆(y) ≤ (y + ∆(y))/4, i.e.
 3∆(y) ≤ y, a contradiction. Hence ∆(y) < y, so y + ∆(y) ≤ 2y and, by monotonicity of L
                                      e
 and the elementary bound for t ≥ ee ,

                               L(y + ∆(y)) ≤ L(2y) ≤ L(y) + log 2 ≤ 2L(y).

 Combining with (2) yields

                   0 < cn+1 − cn ≤ ∆(y) ≤ 4eγ L(y) = 4eγ L(cn )            (n large).       (3)


    3) A coarse upper bound for L(cn )/cn . From C ≤ F+ and, for large ℓ = L(x), the
 estimate ℓ−1 − γℓ−2 + qℓ−3 + A0 ℓ−4 ≤ 2ℓ−1 , we obtain

                                                2e−γ x
                                       C(x) ≤             (x ≥ X3 )
                                                 L(x)

 for some X3 ≥ X2 . Evaluating at x = cn ≥ X3 gives

                                             L(cn )   2e−γ
                                                    ≤      .                                (4)
                                              cn       n

     4) Bounding the logarithmic increment. From Eq. (3)-(4), using log(1 + u) ≤ u,

                               cn+1   cn+1 − cn       L(cn )   8
                         log        ≤           ≤ 4eγ        ≤        (n large).            (5)
                                cn       cn            cn      n

    5) Conclusion. Let an = log cn . Since cn ≥ n, we have an ≥ log n. Fix k ∈ N. Choose
 N (k) so large that for all n ≥ N (k): (i) n ≥ 2k, (ii) cn ≥ X3 , and (iii) log n > 16. Then by
 (5), for all such n,

                                                   n+k
                          (n + k)(an+1 − an ) ≤        · 8 ≤ 16 < log n ≤ an .
                                                    n
 This is equivalent to
                                           log cn   log cn+1
                                                  >          ,
                                           n+k      n+k+1
      1/(n+k)      1/(n+k+1)
 i.e. cn        > cn+1          . As k was arbitrary, the claim follows.                      2
5        RESULTS                                                                                             17


5.3        Research mode results

We used our system in research mode (Sect. 4.1.1) on three different goals (literally specified to
the system by the sentences that follow):

     1. improve gradient descent in machine learning;
     2. the 1-2-3 conjecture in graph theory;
     3. sphere packing in Euclidean spaces.

The first (pre-processing) step is to ask the LLM to construct a list of “seed results” from
the single sentence given by the human user (e.g. one of the three above sentences). Second,
we deploy the literature reviewer agent that returns interesting conjectures, problems, theorem
statements, or other provable sentence from sources in the open literature. Third, the context
preparer returns a relevant selection of formal statements to be proved, by discarding some of the
items from the literature reviewer (specifically, items for which the solution is already known).
The TTVR loop is then deployed on each of them in turn.

   In the rest of this section, output generated from the system (possibly only slightly edited
for LATEX typos or to merge multiple definitions) is on light gray background12 .


5.3.1        Gradient descent in ML

The human-provided guideline “improve gradient descent in machine learning” used as input
for the pre-processing step yielded the following seed results.

          1. Let f be convex and L-smooth. Gradient descent with step size η ∈ (0, 1.75/L]
             induces a convex optimization curve: the mapping n 7→ f (xn ) is convex (equivalently,
             the sequence f (xn ) − f (xn+1 ) is non-increasing).

          2. For any L > 0 there exists a convex L-smooth function and initialization such that
             for every step-size η ∈ (1.75/L, 2/L), the gradient descent optimization curve is not
             convex (despite converging and monotonically decreasing).

          3. For convex L-smooth f and η ∈ (0, 2/L], the sequence of gradient norms {∥∇f (xn )∥}
             is non-increasing.

          4. For convex L-smooth f , the gradient flow optimization curve t 7→ f (x(t)) is always
             convex.

          5. For convex L-smooth f , under gradient flow, the function t 7→ ∥∇f (x(t))∥ is non-
             increasing.

          6. Fix any L > 0 and any relative noise level δ ∈ (0, 1). There does not exist a pos-
             itive universal step size ηmax (δ, L) > 0 with the property that for every (even one-
             dimensional) convex L-smooth quadratic f , every nonzero initialization x0 ̸= 0, and
    12
    None of the proofs in this section has yet been verified formally in lean, nor has it been verified by human
experts in the subject matters of the three topics.
18


           every sequence of inexact-gradient noises satisfying ∥en ∥ ≤ δ∥∇f (xn )∥, the inexact
           gradient descent iterates xn+1 = xn − η(∇f (xn ) + en ) produce a convex sequence
           of function values n 7→ f (xn ) for every choice of step size 0 < η ≤ ηmax (δ, L). In
           particular, no nonzero universal convexity-preserving step-size depending only on δ
           and L (and valid for all one-dimensional convex L-smooth quadratics and all nonzero
           initializations) exists when δ > 0.


   The literature reviewer found 19 interesting sources from the literature13 leading to 19 con-
jectures. The context preparer agent formulated a set of 14 conjectures of interest that we report
below.

  Conjecture 1. (EG convexity up to the stability limit.) Let f be convex and L-smooth.
                For extragradient with any stepsize η ∈ (0, 2/L], the optimization curve is
                convex: the sequence n 7→ f (xn ) satisfies δn ≥ 0 for all n.

  Conjecture 2. (Two-point time-averaging restores convexity beyond 1.75.) Let f be con-
                vex and L-smooth and fix η ∈ (0, 2/L]. There exists a sharp threshold
                λ⋆ (θ) ∈ [0, 1/2) with λ⋆ (θ) = 0 for θ ≤ 1.75 and λ⋆ (θ) ↓ 0 as θ ↓ 1.75 such
                that for all λ ∈ [λ⋆ (θ), 1 − λ⋆ (θ)] the 2-term averaged curve n 7→ M (λ) (a)n =
                (1 − λ)f (xn ) + λf (xn+1 ) is convex for every convex L-smooth f and every
                initialization, while for any fixed λ ∈ / [λ⋆ (θ), 1 − λ⋆ (θ)] there exist counterex-
                amples.

  Conjecture 3. (Implicit step convexifies the discrete curve.) Let f be convex and L-smooth.
                For the implicit (backward Euler) method xn+1 = xn − η∇f (xn+1 ) with any
                η > 0, the sequence n 7→ f (xn ) is convex: δn ≥ 0 for all n. Moreover, if f is
                µ-strongly convex, then (∆n ) is strictly decreasing unless xn is optimal.

  Conjecture 4. (Gradient-norm convexity in the conservative regime.) Let f be convex and
                L-smooth. For GD with η ∈ (0, 1/L], the sequence n 7→ ∥∇f (xn )∥2 is convex:
                ∥∇f (xn+2 )∥2 − 2∥∇f (xn+1 )∥2 + ∥∇f (xn )∥2 ≥ 0 for all n.

  Conjecture 5. (Convexity of a Moreau-smoothed evaluation along GD.) Let f be convex
                and L-smooth and fix η ∈ (0, 2/L]. There exists a universal γ̄(θ) ∈ (0, ∞)
                with γ̄(θ) = Θ (2 − θ)/L as θ ↑ 2 such that, for every γ ∈ (0, γ̄(θ)], the
                sequence n 7→ eγ (f )(xGD
                                       n ) is convex in n.

  Conjecture 6. (Windowed convexity for GD near the stability edge.) Let f be convex
                and L-smooth and fix η ∈ (0,2/L]. Then there exists an integer win-
                dow size W⋆ (θ) = O 1/(2 − θ) such that the W⋆ -point running average
                        P ⋆ −1
                bn = W1⋆ Wj=0 f (xn+j ) is convex in n.

  Conjecture 7. (Adaptive curvature-aware steps ensure convexity up to 2/L.) Let f be con-
                vex and L-smooth, and suppose along the GD trajectory the local smoothness
                surrogate Ln = supt∈[0,1] ∥∇2 f (xn + t(xn+1 − xn ))∥ satisfies Ln+1 ≤ Ln for



 13
      Many of these sources are arXiv reports, so they may never have been peer-reviewed.
5    RESULTS                                                                                        19


                  all n (nonincreasing local curvature). Then for any constant η ∈ (0, 2/L0 ],
                  the GD loss curve is convex: δn ≥ 0 for all n.

    Conjecture 8. (Exact line-search GD yields convex values.) Let f be convex and L-smooth.
                  For exact line-search along negative gradient, xn+1 = xn − ηn ∇f (xn ) with
                  ηn = argminη≥0 f (xn − η∇f (xn )), the sequence n 7→ f (xn ) is convex for all
                  initializations.

    Conjecture 9. (Moreau-envelope descent curve convexity under GD on f .) Let f be convex
                  and L-smooth, and fix η ∈ (0, 2/L]. Let yn = xn − η∇f (xn ) be the GD
                  predictor and define mn = eη (f )(yn ). Then n 7→ mn is convex for all n.

 Conjecture 10. (EG monotonicity of one-step decrease.) Let f be convex and L-smooth. For
                extragradient with any η ∈ (0, 2/L], the one-step decreases are nonincreasing:
                ∆n+1 ≤ ∆n for all n.

 Conjecture 11. (Diagonal preconditioning criterion.) Let f be convex and coordinate-wise
                Li -smooth (i.e., ∂i ∇f is Li -Lipschitz). Consider preconditioned GD xn+1 =
                xn −D∇f (xn ) with diagonal D = diag(di ), di > 0, and define Θ = maxi Li di .
                If Θ ∈ (0, 1.75], then for every convex coordinate-wise smooth f and any ini-
                tialization, the optimization curve n 7→ f (xn ) is convex; furthermore, for
                every Θ ∈ (1.75, 2), there exist convex coordinate-wise smooth f and initial-
                izations where convexity fails even though f (xn ) ↘ f∗ .

 Conjecture 12. (Lookahead with small pull guarantees convexity.) Let f be convex and
                L-smooth. Consider lookahead with inner GD step-size η ∈ (0, 2/L] and
                outer parameters k ∈ N, α ∈ (0, ᾱ(θ, k)] with zt+1 = (1 − α)zt + αxt,k ,
                where xt,0 = zt and xt,j+1 = xt,j − η∇f (xt,j ). There exists ᾱ(θ, k) > 0 with
                ᾱ(θ, k) = Θ (2 − θ)/k as θ ↑ 2 such that t 7→ f (zt ) is convex for every convex
                L-smooth f and initialization.

 Conjecture 13. (Implicit step is a discrete convexifier for GD.) Fix convex L-smooth f and
                any η ∈ (0, 2/L]. Define the hybrid scheme xn+1 = xn − η∇f (xn ), zn+1 =
                zn − η∇f (zn+1 ) with z0 = x0 , and the mixed curve cn = 21 (f (xn ) + f (zn )).
                Then n 7→ cn is convex for all n.

 Conjecture 14. (Restart-on-curvature rule ensures convexity without L.) Let f be convex
                with L-Lipschitz gradient unknown. Consider GD with an adaptive stepsize
                ηn obtained by doubling until ∆n−1 ≥ ∆n , and halving otherwise. This rule
                produces a piecewise-constant stepsize sequence with finitely many halving
                events and guarantees global convexity of n 7→ f (xn ).


   The TTVR loops deployed on each managed to settle 5 out of the 14 statements, and, more
precisely, statements 3, 4, 5, 7, and 13. Of these, 3 and 13 were proved while 4, 5, and 7 were
refuted. We record the number of TTVR iterations for each of the successful runs in Table 4.
The table shows that the system found conjecture 13 to be the hardest. We report it here by
way of example (exactly as the system produced it, with a couple of minor cosmetic changes).
We only need to introduce the slightly non-standard definition of “convex sequence”: a sequence
cn is convex if the sequence of first differences is non-decreasing, i.e. (cn+2 − cn+1 ) ≥ (cn+1 − cn )
20


                                   conjecture    3     4   5   7   13
                                   |itn|         2     1   1   5    6


Table 4: Number of iterations required by our TTVR loop to arrive at a solution of the convex
optimization conjectures.


for all indices n over which the sequence is defined.

  5.2 Theorem
  Let f : Rd → R be convex and differentiable, and fix any stepsize η > 0. Define the explicit
  and implicit iterates by xn+1 = xn − η∇f (xn ) and zn+1 = zn − η∇f (zn+1 ) with arbitrary
  initial points x0 , z0 , and set cn = 12 f (xn ) + f (zn ) . Then the sequence n 7→ cn is convex,
  i.e., cn+2 − 2cn+1 + cn ≥ 0 for all n.

    Proof. Let f : Rd → R be convex and differentiable, and fix η > 0. Define the explicit
  and implicit iterates by

                       xn+1 = xn − η∇f (xn ),        zn+1 = zn − η∇f (zn+1 ),

  with arbitrary initial points x0 , z0 , and set cn = 21 f (xn ) + f (zn ) . We prove δnc = cn+2 −
                                                                           

  2cn+1 + cn ≥ 0 for all n.

     Write the Bregman divergence Df (u, v) = f (u) − f (v) − ⟨∇f (v), u − v⟩ ≥ 0. Denote
  gn = ∇f (xn ), hn+1 = ∇f (zn+1 ), and the steps ∆xn = xn+1 − xn = −ηgn , ∆zn+1 =
  zn+1 − zn = −ηhn+1 . The identities (obtained from the definition of Df ) are

                                                     1
                       ∆xn = f (xn ) − f (xn+1 ) =     ∥∆xn ∥2 − Df (xn+1 , xn )
                                                     η
  and
                                                    1
                      ∆zn = f (zn ) − f (zn+1 ) =     ∥∆zn+1 ∥2 + Df (zn , zn+1 ).
                                                    η
  Since ∆cn = cn − cn+1 = 12 (∆xn + ∆zn ), we have

                        2 δnc = (∆xn − ∆xn+1 ) + (∆zn − ∆zn+1 ) = η Sg + SB ,

  where

                   ∥gn ∥2 − ∥gn+1 ∥2 + ∥hn+1 ∥2 − ∥hn+2 ∥2
                                                            
          Sg =
                                                                                           
          SB =     Df (xn+2 , xn+1 ) − Df (xn+1 , xn ) + Df (zn , zn+1 ) − Df (zn+1 , zn+2 ) .

  Use the three-point identity (valid for all a, b, c):

                    Df (a, b) − Df (b, c) = Df (a, c) − ⟨∇f (b) − ∇f (c), a − b⟩.
5    RESULTS                                                                                                     21


    With (a, b, c) = (xn+2 , xn+1 , xn ) and (a, b, c) = (zn , zn+1 , zn+2 ), and xk+1 − xk = −ηgk ,
    zk+1 − zk = −ηhk+1 , this gives

    SB = Df (xn+2 , xn ) − ⟨gn+1 − gn , xn+2 − xn+1 ⟩ + Df (zn , zn+2 ) − ⟨hn+1 − hn+2 , zn − zn+1 ⟩
            = Df (xn+2 , xn ) + Df (zn , zn+2 ) + η ⟨gn+1 − gn , gn+1 ⟩ + η ⟨hn+2 − hn+1 , hn+1 ⟩.

    Therefore

     2δnc         η ∥gn ∥2 − ∥gn+1 ∥2 + η ∥hn+1 ∥2 − ∥hn+2 ∥2 + SB
                                                            
              =
                  Df (xn+2 , xn ) + Df (zn , zn+2 ) + η ∥gn ∥2 − ⟨gn , gn+1 ⟩ + η ⟨hn+2 , hn+1 ⟩ − ∥hn+2 ∥2
                                                                                                           
              =
              =   Df (xn+2 , xn ) + Df (zn , zn+2 ) + ⟨gn − gn+1 , xn − xn+1 ⟩ + ⟨hn+2 − hn+1 , zn+2 − zn+1 ⟩,
                                                      |         {z          } |             {z             }
                                                                ≥0                            ≥0

     where we used xn − xn+1 = ηgn and zn+2 − zn+1 = −ηhn+2 . The two inner products are
    nonnegative by the monotonicity of ∇f (convexity of f ), and the Bregman divergences are
    nonnegative by convexity. Hence 2 δnc ≥ 0, i.e., δnc ≥ 0 for all n. Thus n 7→ cn is convex. 2




5.3.2       The 1-2-3 conjecture in graph theory

The human-provided guideline “1-2-3 conjecture in graph theory” yielded (among other sources)
the paper [15], which made us aware that the conjecture was actually closed in 2024 (we had
not realized it). The seed results found by the pre-processing step consist of the following text:
graph definitions, a theorem statement, and an informal version thereof, copied below almost
verbatim.

    5.3 Definition
    A graph G = (V, E) is finite and simple if V is a finite set of vertices and E ⊆ V2 is a set of
                                                                                       

    unordered pairs called edges. For v ∈ V , the neighborhood of v is NG (v) = {u ∈ V : {u, v} ∈
    E} and the degree is degG (v) = |NG (v)|. Two vertices u, v are adjacent if {u, v} ∈ E. An
    isolated edge of G is an edge whose two endpoints have degree 1 and form a connected
    component on exactly two vertices. Equivalently, a connected component isomorphic to
    K2 (a single edge) is called a K2 -component. For an integer k ≥ 1, a k-edge-weighting of
                  Pω : E → [k]. The weighted degree (or sum-color of a vertex v ∈ V under
    G is a function
    ω is sω (v) = u∈NG (v) ω({u, v}). A k-edge-weighting ω is a vertex-coloring by sums (or
    neighbor-sum distinguishing) if for every edge {u, v} ∈ E we have sω (u) ̸= sω (v).

    5.4 Theorem (Keusch, Solution to the 1–2–3 Conjecture, 2024)
    Let G = (V, E) be a finite simple graph with no K2 -component (i.e., with no isolated edge).
    Then there exists a 3-edge-weighting ω : E → {1, 2, 3} that is vertex-coloring by sums: for
    every {u, v} ∈ E, sω (u) ̸= sω (v).

    In words: every graph without an isolated edge admits edge weights from {1, 2, 3} so that
    adjacent vertices receive different sums of incident weights.


    The literature reviewer found 16 sources from the literature, leading to 14 conjectures. The
22


context preparer selected from these a set of 11 conjectures of interest (in the sense that they
bear some relation to the 1-2-3 conjectures and are probably open), together with the following
remarks about mathematical notations.

     • G = (V, E) is a graph; E(v) denotes the set of edges incident to v; d(v) = |E(v)|;
       ∆(G), δ(G) are the maximum and minimum degrees.

     • A component isomorphic to K2 is a K2 -component. A graph with no K2 -component
       (i.e., no isolated edge) is called nice.

     • For k ∈ N, write [k] = {1, 2, . . . , k}. A k-edge-weighting
                                                               P is a map ω : E → [k]. The
       weighted degree (sum-color) of v under ω is sω (v) = e∈E(v) ω(e).

     • A k-edge-weighting ω is neighbor-sum distinguishing (NSD) if ∀{u, v} ∈ E we have
       sω (u) ̸= sω (v).

     • For hypergraphs H = (V, E), sω (v) = e∈E,v∈e ω(e). We call ω edge-proper by sums
                                                P
       if every e ∈ E contains u, v with sω (u) ̸= sω (v).

     • Total weighting: ϕ : V ∪ E → R with vertex-sum Sϕ (v) = ϕ(v) + e∈E(v) ϕ(e). A
                                                                               P

       graph is (k, k ′ )-total weight choosable if for every list assignment L with |L(v)| = k
       for v ∈ V and |L(e)| = k ′ for e ∈ E, there exists a proper total L-weighting ϕ (i.e.,
       Sϕ (u) ̸= Sϕ (v) for all {u, v} ∈ E).

     • Multiplicative variant: pω (v) = e∈E(v) ω(e). A weighting ω is multiplicative-NSD if
                                          Q
       ∀{u, v} ∈ E, pω (u) ̸= pω (v).

     • Logs are natural; constants c > 0 are absolute unless specified.

     • For a real interval I, an edge-weighting ω : E(G) → I is called t-strong if |sω (u) −
       sω (v)| ≥ t for every edge {u, v} ∈ E(G). We write Badt (ω) = {{u, v} ∈ E(G) :
       |sω (u) − sω (v)| ≤ t}.

     • For a graph class G, we say that NSD 3-edge-weightings are c-locally-reconfigurable
       in G if for every G ∈ G and every NSD 3-edge-weighting ω there is a sequence of NSD
       3-edge-weightings from ω to some canonical NSD 3-edge-weighting that changes at
       most c incident edges at any vertex at each step.

     • For bipartite graphs with bipartition (A, B), let parPω (v) = sω (v) mod 2. The parity
       profile of ω is (parω (A), parω (B)) where parω (X) = v∈X parω (v) mod 2.

     • For integers k ≥ 1 and ℓ ≥ 0, an NSD k-edge-weighting ω is ℓ-slack if |sω (u) − sω (v)| ≥
       1 + ℓ for all edges {u, v}.

     • For ∆ ≥ 1, let θ∆ (G) = minω:E(G)→{1,2,3} |{{u, v} ∈ E(G) : |sω (u) − sω (v)| ≤
       1}|/|E(G)|.

     • For graphs G, H, write G□H for the Cartesian product; K2 □G is the “layered double”
       of G.

     • A graph is triangle-sparse if tri(G) ≤ |E(G)|2 /|V (G)|.
5    RESULTS                                                                                      23


       • For a list assignment L : E(G) → 2{1,2,3} , say L is α-dense if |L(e)| ≥ 2 for all e and
         for every v, at most α degG (v) incident edges e have |L(e)| = 2.

       • For p ∈ (0, 1), Gp is the binomial random subgraph obtained by retaining each edge
         independently with probability p.

       • All asymptotics with probability 1 (a.a.s.) are with respect to the natural size param-
         eter indicated (e.g., ∆ → ∞ or n → ∞ as specified in each statement).


    There are a few more notations that the system did not mention, but which we believe will
be useful to many readers of this paper, namely: (i) for two graphs G, F the cartesian product
G□F is the graph on V (G) × V (F ) where (uG , uF ) and (vG , vF ) are adjacent iff uG = vG or
uF = vF ; (ii) the disjoint union G ⊔ F is the graph on the disjoint union V (G)∪V    ˙ (F ) of their
vertex sets with the corresponding edges; (iii) if F is a subgraph of G, the difference G − F
is the graph obtained by deleting E(F ) from G(F ) and any resulting isolated vertices from V ;
(iv) arb(G) is the arboricity of G, namely the minimum number of forests into which the graph
can be partitioned; (v) the 3-lift R3 (G) of a graph G is obtained as follows: replace each vertex
v ∈ V (G) with three copies v1 , v2 , v3 ; for each edge (u, v) ∈ E(G) choose a permutation πuv ∈ S3
and connect ui to vπuv (i) by an edge for each i ∈ {1, 2, 3} (in general, the choice of permutations
πuv may be random or structured); (vi) a d-regular graph is an expander if the second-largest
eigenvalue λ2 of its adjacency matrix is ≪ d (then the spectral gap d − λ2 is large).

    Here is the conjecture list selected by the context preparer.

    Conjecture 1. (Layer-doubling amplifies small-difference edges). There exists an absolute
                  c > 0 such that for every graph G with sufficiently large maximum degree,
                  one has θ∆ (K2 □G) ≥ max(θ∆ (G), c). In particular, there is a universal c such
                  that every 3-edge-weighting of K2 □G leaves at least a c-fraction of edges with
                  |s(u) − s(v)| ≤ 1, regardless of G.

    Conjecture 2. (Reconfiguration connectivity for trees). For every tree T on at least 3 ver-
                  tices, the NSD reconfiguration graph R3 (T ) is connected and has diameter
                  O(|E(T )|). Moreover, NSD 3-edge-weightings are 1-locally-reconfigurable on
                  trees.

    Conjecture 3. (Near-parity surjectivity on bipartite graphs under 3-weights). Let G be con-
                  nected and bipartite with bipartition (A, B). Among the four parity profiles
                  (parity sums on A and B), exactly two occur for some NSD 3-edge-weighting
                  of G, and these two profiles differ by flipping all parities in one side. More-
                  over, both profiles occur unless G is a tree with |A| odd and |B| odd, in which
                  case neither occurs.

    Conjecture 4. (Triangle-sparse graphs admit global 2-slack after deleting o(|E|) edges). For
                  every ϵ > 0 there exists ∆ = ∆(ϵ) > 0 such that every nice triangle-sparse
                  graph G admits a set F ⊆ E(G) with |F | ≤ ϵ|E(G)| so that G − F has an
                  ℓ-slack NSD 3-edge-weighting with ℓ = 1 (i.e., |s(u) − s(v)| ≥ 2 on all edges
                  of G − F ).
24


  Conjecture 5. (Threshold for random subgraphs of high-degree hosts). There exists an
                absolute c > 0 such that for every family of nice graphs G with ∆(G) → ∞
                and |V (G)| ≤ ∆(G)O(1) , if p ≥ c log ∆(G)/∆(G), then a.a.s. Gp is nice and
                hence admits an NSD 3-edge-weighting.

  Conjecture 6. (Product obstruction is pervasive). There exists an absolute β > 0 such that
                for every pair of graphs (G, H) with sufficiently large maximum degrees, every
                3-edge-weighting of G□H has ≥ β min(|E(G)|, |E(H)|) max(|V (G)|, |V (H)|)
                edges with |s(u) − s(v)| ≤ 1. Equivalently, θ∆ (G□H) ≥ β for all such pairs,
                extending the existence of pairs with θ∆ ≥ 1/4 to a universal lower bound.

  Conjecture 7. (List-NSD robustness under sparse 2-lists). There exists an absolute α ∈
                (0, 1) such that the following holds for all sufficiently large ∆′ : for every nice
                graph G with ∆(G) = ∆′ and every α-dense list assignment L : E(G) → 21,2,3
                (i.e., at most an α-fraction of edges around any vertex have 2-lists, all others
                have 3-lists), there is a list NSD 3-edge-weighting from L.

  Conjecture 8. (Quantitative strong edge-separation in Kn ). There exists an absolute γ > 0
                such that for all n sufficiently large, every 3-edge-weighting ω of Kn satisfies
                |Bad1 (ω)| ≥ γn2 . Moreover, the extremal order n2 is tight up to constants.

  Conjecture 9. (NSD reconfiguration expansion in expanders). There exists c > 0 such that
                if G is a d-regular expander on n vertices with spectral gap at least c and n
                sufficiently large, then R3 (G) is connected and has diameter at most nO(1) ,
                and furthermore the simple “single-edge resampling” Markov chain on R3 (G)
                is rapidly mixing (polynomial mixing time).

 Conjecture 10. (Bipartite two-phase correction with tolerance-1 succeeds). There exists a
                universal C > 0 and an unbounded function g such that for every graph
                G = Cn ⊔ K1,∆ and every initial weighting ω : E(G) → {1, 2, 3}, if Stage
                2 resamples the edges in Bad1 (ω) (instead of Bad2 (ω)), then the expected
                number resampled is at most C|E(G)|/g(∆).

 Conjecture 11. (Sparse robust NSD in dense host graphs). For every ϵ > 0 there exists
                C = C(ϵ) > 0 such that for every n-vertex graph G with ∆(G) ≥ (1/2 + ϵ)n
                and every subgraph F ⊆ G with arb(F ) ≤ C and ∆(F ) ≤ C log n, the graph
                G − F admits an NSD 3-edge-weighting that is 1-locally-reconfigurable.


    Our TTVR loop refuted 9 out of 11 of the above conjectures, i.e. all but 2 and 7, which
remain open. We can blame this conjectural failure on gpt-5 in the sense that in all likelihood
it did not find, but rather inferred, these conjectures from the open literature.

                    conjecture   1    2    3   4   5   6    7    8   9   10   11
                    |itn|        1   NA    1   1   1   1   NA    3   5    1    1


Table 5: Number of iterations required by our TTVR loop to settle the graph theoretical con-
jectures.

     The iteration effort made by the TTVR loop is reported for each settled conjecture in Table
5    RESULTS                                                                                             25


5. Among the easiest conjectures, 1, 3, and 11 have the property that the contra-positive can be
proved by exhibiting reasonably simple counter-examples. The rest, including the hardest con-
jectures 8 and 9, have contra-positive statements that involve more complicated constructions.

   We report here the refutation proof that the system found hardest, namely that of Conjecture
9. The statement is its contra-positive, since the conjecture is refuted. Before we present the
theorem and its proof, we need to introduce one extra notion not provided by the LLM: a
Ramanujan graph is a finite, connected, d-regular graph whose adjacency matrix
                                                                             √ has eigenvalues
(and hence singular values) σ1 = d ≥ σ2 ≥ · · · ≥ σn ≥ −d such that |σi | ≤ 2 d − 1 for all i ≥ 2.
The (alphabetically indexed) footnotes in Theorem 5.5 are of the authors of this paper (rather
than the LLM): most are explanatory, but one emphasizes a formal error, i.e. the “overloading”
of the symbol x, which has an impact on the formalized version of the proof encoded in lean [7].

    5.5 Theorem
    There is no absolute c > 0 such that every sufficiently large d-regular expander G with
    adjacency spectral gap at least c has connecteda R3 (G) and a rapidly mixing single-edge
    resampling Markov chain on R3 (G). More precisely, for every c > 0 there exist a fixed
    degree d and infinitely many d-regular expanders G with adjacency spectral gap at least c
    for which R3 (G) is disconnected; consequently the single-edge resampling chain on R3 (G)
    is not irreducible (hence not rapidly mixing).

       Proof. By contradictionb . Assume there exists c > 0 such that whenever G is a d-
    regular expander on n vertices with adjacency spectral gap at least c and n sufficiently
    large, then R3 (G) is connected and the single-edge resampling Markov chain on R3 (G) is
    rapidly mixing.

       Fix c > 0. Choose an integerc m ≥ 17 large enough that
                                                 √      
                                min{ m, 2 m − 2 m − 1 } ≥ c.

    Let N be large, and let P = PN be an m-regular bipartite √    Ramanujan graph on bipartition
    (L0 , R0 ) with |L0 | = |R0 | = N (any family with σ2 (P ) ≤ 2 m − 1 suffices).

       Construct a graph Y = YN as follows.

       • Vertex set: for each coarsed vertex x ∈ L0 ∪R0 create a fiber of 3 vertices (x, 1), (x, 2), (x, 3).
         Thus |V (Y )| = 6N . Write Li = {(ℓ, i) : ℓ ∈ L0 } and Ri = {(r, i) : r ∈ R0 } for
         i ∈ {1, 2, 3}.

       • H-edges (intra-fiber triangles):
         for every x ∈ L0 ∪ R0 , add the 3 edges of K3 on {(x, 1), (x, 2), (x, 3)}.

       • B-edges (across L–R): for every coarse edge {ℓ, r} ∈ E(P ) and every i ∈ {1, 2, 3}, add
         the two edges {(ℓ, i), (r, i)} and {(ℓ, i), (r, i + 1 mod 3)}.

    Each vertex has 2m B-neighbors and 2 H-neighbors; hence Y is d-regular with d = 2m + 2.
    Connectivity of Y follows since P is connected and the B-edges change the index i by 0 or
    +1 mod 3, so B-edges alone connect all layers; adding H-edges preserves connectivity.
26


 Spectral gap. Lete A(Y ) = B + AH , where B is the adjacency of the B-edges and AH that
 of the disjoint union of all intra-fiber triangles. Thenf ∥AH ∥ = 2. Order the vertices so that
 the bipartition is (L1 ∪ L2 ∪ L3 ) ∪ (R1 ∪ R2 ∪ R3 ) and writeg
                                            
                                      0 C
                             B=                ,     C = (I3 + S) ⊗ P,
                                     C⊤ 0

 where S is the 3 × 3 cyclic shift matrix. Since S is unitary, I3 + S is normal with eigenvalues
 2, 1, 1, so its singular values are 2, 1, 1. Hence the nonzero eigenvalues of B are ±σj (C) with

                     σ(C) = { 2σj (P ), σj (P ), σj (P ) : j = 1, . . . , N }.
                                                                √
 Because P is m-regular bipartite, σ1 (P ) = m and σ2 (P ) ≤ 2 m − 1. Therefore

                          λ1 (B) = 2m,        λ2 (B) = max{2σ2 (P ), m}.

 For any unith x⊥1,

            x⊤ A(Y )x = x⊤ Bx + x⊤ AH x ≤ λ2 (B) + ∥AH ∥ ≤ max{2σ2 (P ), m} + 2.

 Since λ1 (A(Y )) = d = 2m + 2,

 gap(Y ) ≜ λ1 (A(Y ))−λ2 (A(Y )) ≥ 2m+2−max(2σ2 (P ), m)+2 = min(m, 2(m−σ2 (P ))) ≥ c.

 Thus Y is a d-regular expander with adjacency spectral gap at least c, and |V (Y )| = 6N
 grows with N .

 Triangle gadget. On K3 , any NSD {1, 2, 3}-weighting uses weights 1, 2, 3 once and induces
 vertex sums {3, 4, 5}. Fix the canonical labeling of the three vertices by their H-sums 3, 4, 5
 and set
                        w({3, 4}) = 1, w({4, 5}) = 3, w({5, 3}) = 2.
 Changing any one H-edge to either of its two other values adjusts the two endpoint sums by
 ±1 or ±2, while the third vertex is unchanged; a direct check shows that in each of the six
 possibilities one of the changed endpoints hits the unchanged third value, so that triangle
 acquires a badi edge.

     Define two {1, 2, 3}-weightings ω, ω ′ of Y .

     • For ω, give every B-edge weight 2. In each L-fiber use the canonical triangle; in each
       R-fiber use the canonical triangle cyclically shifted so that the H-sums at indices i ∈
       {1, 2, 3} are (4, 5, 3) respectively (while on L they are (3, 4, 5)). Writej Bx (i) ∈ {3, 4, 5}
       for the H-sum at (x, i). Because every vertex has exactly 2m B-neighbors of weight 2,
       its B-contribution is 4m, so

                                      sω (x, i) = 4m + Bx (i).      (∗)

     • For ω ′ , keep all H-edges as in ω, but give every B-edge weight 1. Then for all (x, i),

                                     sω′ (x, i) = 2m + Bx (i).      (†)
5    RESULTS                                                                                      27


    We now prove ω is NSD and isolated in R3 (Y ), and ω ′ is NSD (hence R3 (Y ) is disconnected).

    NSD of ω.

       • On every H-edge within a fiber x, by (∗) the two endpoint sums differ byk Bx (i) −
         Bx (j) ∈ {±1, ±2} \ {0}.

       • On every B-edge, edges join (ℓ, i) ∈ Li to (r, j) ∈ Rj only for j ∈ {i, i + 1}; with the
         chosen H-sums on L andl R, the ordered pair (Bℓ (i), Br (j)) lies in

                                  {(3, 4), (4, 5), (5, 3), (3, 5), (4, 3), (5, 4)},

         so again sω (ℓ, i) − sω (r, j) = Bℓ (i) − Br (j) ∈ {±1, ±2} \ {0}. Thus ω is neighbor-sum
         distinguishing.

    Isolation of ω in R3 (Y ). Consider any single-edge resampling from ω.

       • Case H (resampling an H-edge within a fixed triangle). Only the two incident vertex
         sums change (by ±1 or ±2), the third vertex in that triangle stays unchanged, and
         by the triangle blocking property one of the two changed endpoints assumes the third
         vertex’s H-sum. Since all three vertices in the triangle share the same B-contribution
         4m in (∗), this equality persists for the full sums; hence a bad H-edge is created.

       • Case B (resampling a B-edge e = {(ℓ, i), (r, j)}). Here j ∈ {i, i + 1} and only the two
         endpoints change, each by δ ∈ {±1}. Inspecting the six pairs above, in each case and
         for each sign of δ one changed endpoint matches the unchanged H-sum of one of its
         two triangle-neighbors, thereby creating a bad H-edge. Concretely:

            – (3, 4) : δ = +1 makes 3 → 4 on the left (collision with the left vertex of H-sum
              4); δ = −1 makes 4 → 3 on the right.
            – (4, 5) : δ = +1 makes 4 → 5 on the left; δ = −1 makes 5 → 4 on the right.
            – (5, 3) : δ = +1 makes 3 → 4 on the right; δ = −1 makes 5 → 4 on the left.
            – (3, 5) : δ = +1 makes 3 → 4 on the left; δ = −1 makes 5 → 4 on the right.
            – (4, 3) : δ = +1 makes 4 → 5 on the left; δ = −1 makes 4 → 3 on the left.
            – (5, 4) : δ = +1 makes 4 → 5 on the right; δ = −1 makes 5 → 4 on the left.

         In all cases the resampled weighting is not NSD, so ω has degree 0 in R3 (Y ).

    NSD of ω ′ . Using (†) the same H- and B-edge checks as above (with 4m replaced by 2m)
    show that ω ′ is NSD and ω ′ ̸= ω.

    Conclusion and contradiction. For the fixed degree d = 2m + 2, the graphs YN form an
    infinite family of d-regular expanders with adjacency spectral gap at least c. Since ω is
    isolated in R3 (YN ) while ω ′ is another NSD weighting, R3 (YN ) is disconnected for all large
    N . This contradicts the assumption that for the universal constant c, all sufficiently large
    d-regular expanders with adjacency spectral gap at least c have connected R3 (G) (and, in
28


  particular, an irreducible and rapidly mixing single-edge resampling chain). Therefore, no
  such c exists.                                                                           2

     a
        The proof constructs a graph Y then appeals to R3 (Y ) without mentioning the construction of the
  permutations, and hence we must conclude that it is random.
      b
        Syntactically, the contradiction is applicable to the first paragraph of the theorem statement.
      c
        We could not explain why 17 must be a lower bound for m.
     d
        We do not know why this vertex is called “coarse”; we believe the system used “coarse” to denote vertices
  and edges of P .
      e
        The symbol A is used to denote adjacency matrices: A(Y ) is that of the graph Y , while AH is that of
  the subgraph of Y limited to the H-edges. Perhaps a little strangely, the adjacency matrix of the subgraph
  of Y limited to the B-edges is simply called B instead of AB .
      f
        This is the spectral or operator norm.
      g
        This equation says that the B-edges subgraph with adjacency matrix B consists of the two types of edges
  mentioned above: direct i → i (matrix I3 ) and skew i → i + 1 (matrix S); and that these patterns occur
  for each nonzero entry of P (here identified by its homonymous adjacency matrix), whence the Kronecker
  product ⊗.
     h
        This means “any unit vector x orthogonal to the all-one vector”. We remark that the proof overloads
  here the symbol x, which was previously used to denote vertices of P . Subsequent mentions of x refer to
  vertices of P .
      i
        A “bad edge” in this context is an edge bearing a weight that negates the NSD property.
      j
        This sentence is a definition of the symbol Bx (i) — the notation somewhat clashes with B being a
  matrix. Note that x here is a vertex of P rather than a unit vector orthogonal to the all-one vector.
      k
        Since {±1, ±2} does not contain 0, the specification is pleonastic; we think that the system meant to
  emphasize the fact that Bx (i) cannot be equal to Bx (j).
      l            S
        Here, L = i≤3 Li and similarly for R.




5.3.3    Sphere packing in Euclidean spaces

The human-provided guideline “sphere packing in Euclidean spaces” yielded the following seed
results.

  5.6 Definition (Euclidean norm, balls, and volume)
  Fix n ∈ N. On Rn let ∥ · ∥ denote the Euclidean norm and, for x ∈ Rn and r > 0, write

                                    Bn (x, r) = {y ∈ Rn : ∥y − x∥ ≤ r}.
                                                                           
  Write voln (·) for n–dimensional Lebesgue measure and ωn = voln Bn (0, 1) for the volume
  of the unit ball.
  5.7 Definition (Sphere packing and asymptotic density)
  Let r > 0. A sphere packing of radius r in Rn is a set X ⊂ Rn such that the closed balls
  {Bn (x, r) : x ∈ X} are pairwise disjoint. Its (upper) asymptotic density is
                                          S                         
                                      voln x∈X Bn (x, r) ∩ Bn (0, R)
                    δ(X, r) = lim sup                                 ∈ [0, 1].
                                R→∞            voln Bn (0, R)

  The optimal packing density in dimension n is

               θ(n) = sup{δ(X, r) : X ⊂ Rn , r > 0, {Bn (x, r)}x∈X pairwise disjoint}.
5    RESULTS                                                                                      29


    5.8 Definition (Lattices, covolume, and lattice packings)
    A lattice L ⊂ Rn is a discrete additive subgroup of rank n of the form L = AZn for some
    invertible A ∈ GLn (R). Its covolume (or determinant) is det(L) = | det A|, i.e. the volume
    of a fundamental domain of L. The minimum of L is λ(L) = min{∥v∥ : v ∈ L \ {0}}. For
    r ≤ 12 λ(L), the translates {Bn (ℓ, r) : ℓ ∈ L} form a lattice packing with density
                                                              
                                               voln Bn (0, r)     ωn rn
                                 ∆(L, r) =                      =        .
                                                   det(L)         det(L)

    5.9 Definition (Absolute constant)
    A constant c > 0 is called absolute if it does not depend on n (or any other parameter in
    the statement).

    5.10 Theorem (Klartag’s quadratic lower bound for sphere packing density, 2025)
    There exists an absolute constant c > 0 such that, for every n ≥ 2,

                                                       n2
                                            θ(n) ≥ c      .
                                                       2n
    Moreover, this lower bound is achieved by a lattice packing: for each n there exists a lattice
    L ⊂ Rn and a radius r > 0 with
                                                      n2
                                         ∆(L, r) ≥ c n .
                                                      2

    Theorem 5.10 improves the classical order θ(n) ≳ n 2−n (Rogers 1947 and subsequent re-
    finements) by a further linear factor in n. It also strengthens the 2023 bound θ(n) ≥
    (1 − o(1)) n2log n
                 n+1 by replacing log n with n and, in addition, obtaining a lattice packing with
    the stated density.


   The literature reviewer found 14 conjectures. The context preparer rejected one and focused
on the following 13 conjectures. We point out that: (i) ∆(L) is the lattice density, i.e. the
maximal density attainable by non-overlapping equal spheres centered at the lattice points; (ii)
the condition number κ(E) of the ellipsoid E is the condition number of the matrix A in its
definition E = {x ∈ Rn | x⊤ Ax ≤ 1}; (iii) the kissing number τ (n) is the largest number
of unit balls that an be placed adjacent to a central unit ball such that the balls intersect at
most in their frontier; (iv) V (L) denotes the volume of a fundamental region of the lattice L,
namely | det gen L|, where gen L is a generating basis of the lattice; (v) L∗ is the dual lattice
{y ∈ Rn | ∀x ∈ L ⟨y, x⟩ ∈ Z} of L; (vi) Ln is the set of all lattices of dimension n up to orthogonal
transformations; (vii) the random variable X is uniform in V (L) if it is uniformly distributed
in the fundamental domain of the lattice; (viii) GLn (R) is the set of all invertible n × n real
matrices; (ix) let r(L) be the largest sphere packing radius and R(L) the smallest sphere covering
                                                                                     √
radius of L: Jarnı́k’s inequality states that there is an absolute constant cn ≤ n/2 such that
R(L) ≤ cn r(L).


    Conjecture 1. (Low-kissing high-density lattices.) There exist absolute c, C > 0 such that
                  for every n ≥ 3 there is a unimodular lattice L with ∆(L) ≥ cn2 2−n and
                  kissing number τ (L) ≤ Cn log n.
30


 Conjecture 2. (Abundance of high-density lattices.) There exist absolute c, C > 0 such that
               for all sufficiently large n there are at least exp(cn log n) pairwise non–SLn (Z)-
               equivalent unimodular lattices L with ∆(L) ≥ cn2 2−n and
                                                      Z
                                               1
                                                             ||x||2 dx ≤ Cn.
                                         voln (V (L)) V (L)

 Conjecture 3. (Robustness under small unimodular perturbations.) There exist absolute
               c, ϵ0 > 0 such that for all sufficiently large n there is a unimodular lattice L
               with ∆(L) ≥ cn2 2−n and the following holds: for every T ∈ SLn (R) with
               ||T − I||op ≤ ϵ0 , one has ∆(T L) ≥ (c/2)n2 2−n .

 Conjecture 4. (Dual successive minima growth.) There exist absolute c0 , c1 > 0 such that
               for every n ≥ 2 there is a unimodular lattice
                                                      √      L with ∆(L) ≥ c0 n2 2−n and for
                                               ∗
               all 1 ≤ k ≤ ⌊c1 n⌋ one has λk (L ) ≥ c0 k.

 Conjecture 5. (Successive minima growth at the Klartag scale.) There exist absolute c0 , c1 >
               0 such that for every n ≥ 2 there is a unimodular lattice
                                                                    √       L with ∆(L) ≥
                   2 −n
               c0 n 2 and for all 1 ≤ k ≤ ⌊c1 n⌋ one has λk (L) ≥ c0 k.

 Conjecture 6. (Randomized inverse-polynomial construction.) There exist absolute c, C > 0
               and a randomized algorithm running in time poly(n) which, on input n,
               outputs with probability at least cn−C a basis of a unimodular lattice L with
               ∆(L) ≥ cn2 2−n .

 Conjecture 7. (Bounded–eccentricity Klartag ellipsoids.) There exist absolute c, C > 0
               such that for every n ≥ 2 there is an origin-symmetric ellipsoid E ⊂ Rn
               with voln (E) ≥ cn2 , E ∩ (Z n ∖ {0}) = ∅, and condition number κ(E) ≤ nC .
               Equivalently, the lattice packing realizing density ≥ cn2 2−n can be chosen to
               arise from an integer–free ellipsoid whose axis ratios are bounded by a fixed
               polynomial in n.

 Conjecture 8. (Probability at the quadratic scale is θ(n−2 ).) There exists an absolute c > 0
               such that for all sufficiently large n, one has cn−2 ≤ µ{L ∈ Ln : ∆(L) ≥
               cn2 2−n } ≤ Cn−2 , where the upper bound holds for some absolute C by
               known tail inequalities, and the lower bound is conjectured to match it up to
               constants.

 Conjecture 9. There exist absolute constants c, C > 0 such that for every n ≥ 2 there is
               a unimodular lattice L ⊂ Rn with ∆(L) ≥ cn2 2−n , whose dual has large
                                                                                            √
               minimum and whose  R Voronoi      cell has bounded inertia, namely λ(L∗ ) ≥ c n
               and 1/ voln (V (L)) V (L) ||x||2 dx ≤ Cn.

Conjecture 10. (Voronoi thin-shell concentration at the quadratic scale.) There exist absolute
               c, C > 0 such that for every n ≥ 3 one can find a unimodular lattice   L with
                           2  −n
               ∆(L) ≥ cn 2 for which the uniform random X in V (L) obeys Pr | ||X|| −
                                  √         2
               (E||X||2 )1/2 | ≥ t n ≤ 2 e−ct n , where (0 ≤ t ≤ 1).

Conjecture 11. (Well-spread minimal vectors at the Klartag scale.) There exist absolute
               c, C > 0 such that for every n ≥ 3 there is a unimodular lattice L with
5    RESULTS                                                                                     31


                  ∆(L) ≥ cn2 2−n whose  set S of minimal directions S = {v/||v|| : v ∈ L, ||v|| =
                                   1 P        ⊤   1           √
                  λ(L)} satisfies |S|  u∈S uu − n I op ≤ C/ n.

 Conjecture 12. (Explicit sparse subsequence achieving quadratic-order lattice packing.) There
                exist absolute c, C > 0 and an explicit infinite sequence of dimensions (nk )
                with a deterministic, polynomial-time construction of unimodular         lattices
                Lnk ⊂ Rnk such that ∆(Lnk ) ≥ cn2k 2−nk and 1/ volnk (V (Lnk )) V (Ln ) ||x||2 dx ≤
                                                                               R
                                                                                     k
                Cnk .

 Conjecture 13. (Transference near-tightness across many indices with spectral gap.) There
                exist absolute c, C > 0 such that for every n ≥ 3 there is a unimodular lattice
                L with ∆(L) ≥ cn2 2−n for which, simultaneously, λk (L) λn+1−k (L∗ ) ≥ cn for
                all 1 ≤ k ≤ ⌊cn⌋ and gap(L) = 4π 2 λ(L∗ )2 ≥ Cn.


   Our TTVR loop proved 5 out of the 13 conjectures above, and refuted none. This conjectural
success is mitigated by the relatively low number of closed conjectures (8 of them remain open).
Even though, similarly to Sect. 5.3.2, our system did not find but inferred these conjectures, this
time the inference was more insightful (or probably simply luckier). The iteration effort made

          conjecture    1   2    3    4     5    6    7    8     9    10    11    12    13
          |itn|         2   2   NA   NA     1   NA    8   NA    NA     6   NA    NA    NA


Table 6: Number of iterations required by our TTVR loop to settle the sphere packing conjec-
tures.

by the TTVR loop is reported for each settled conjecture in Table 6. We report the proof of the
hardest conjecture according to number of iterations.

    5.11 Theorem (Bounded-eccentricity Klartag ellipsoids)
    There exist absolute c, C > 0 such that for every n ≥ 2 there is an origin-symmetric
    ellipsoid E ⊂ Rn with voln (E) ≥ cn2 , E ∩ (Zn ∖ {0}) = ∅, and condition number κ(E) ≤ nC .
    Equivalently, the lattice packing realizing density ≥ cn2 2−n can be chosen to arise from an
    integer–free ellipsoid whose axis ratios are bounded by a fixed polynomial in n.

       Proof. Fix n ≥ 2. We produce an origin–symmetric ellipsoid E ⊂ Rn with E∩(Zn \{0}) =
    ∅, voln (E) ≥ c n2 , and κ(E) ≤ nC for absolute constants c, C > 0, and then record the
    equivalence with the packing formulation.

    1) Linear normalization and the integer–free difference body. Let L ⊂ Rn be a lattice with
       minimum λ(L) and choose U ∈ GLn (R) with U (L) = Zn . Put
                                        
                   K(U ) = U Bn 0, λ(L)
                                                                              
                                      2    ,    E(U ) = 2K(U ) = U Bn 0, λ(L) .

       Since {Bn (ℓ, λ(L)                                                         n
                      2 ) : ℓ ∈ L} is a packing, the translates {K(U ) + z : z ∈ Z } are pairwise
       disjoint. Hence E(U ) = K(U ) − K(U ) is integer–free: if z ∈ Zn \ {0} lay in E(U ), there
       would exist x, y ∈ K(U ) with z = x − y, forcing K(U ) ∩ (K(U ) + z) ̸= ∅, a contradiction.
32


     Moreover,
                                                                    n
                 voln E(U ) = 2 n voln K(U ) = 2 n | det U | ωn λ(L)    = 2 n ∆(L),
                                           
                                                                 2

     using | det U | = 1/ det(L). Finally, E(U ) = U Bn (0, λ(L)) is an ellipsoid whose semi–axes
     are λ(L) times the singular values of U , so κ(E(U )) = κ(U ).

 2) A lattice with quadratic packing and controlled local geometry. By the lattice version of
    Klartag’s theorem and standard normalizations, there exist absolute constants c0 , C0 > 0
    and, for each n ≥ 2, a unimodular lattice L ⊂ Rn such that

                    ∆(L) ≥ c0 n2 2−n          and      c0 n ≤ ρ(L) λ(L) ≤ C0 n.
                             n
     Since ∆(L) = ωn λ(L)
                      2           and ωn ≤ (2πe/n)n/2 , we obtain

                         n     c0 n2     2
                                            n n/2                                √
                    λ(L)     ≥       ≥ cn                     =⇒       λ(L) ≥ c1       n
                                ωn          2πe
     for an absolute c1 > 0. The product bound ρ(L) λ(L) ≤ C0 n then gives

                                                C0 n     √
                                       ρ(L) ≤        ≤ C2 n.
                                                λ(L)
                                                                √
     In particular, by Jarnı́k’s inequality, λn (L) ≤ 2ρ(L) ≤ C3 n, while λ1 (L) = λ(L) ≥
       √
     c1 n.

 3) A primal–dual reduction and a lower bound on λ1 (L∗ ). We use two inputs.

      (i) Slab transference for the covering radius. Claim: for every lattice L,
                                                            1
                                             ρ(L) ≥                .
                                                        2 λ1 (L∗ )

          Proof: let y ∈ L∗ with ∥y∥ = λ1 (L∗ ) and choose x ∈ Rn with ⟨y, x⟩ = 21 . For any
          ℓ ∈ L, one has ⟨y, x − ℓ⟩ ∈ 12 + Z, hence |⟨y, x − ℓ⟩| ≥ 12 . By Cauchy–Schwarz,
                       1
          ∥x − ℓ∥ ≥ 2∥y∥ . Taking the infimum over ℓ and then the supremum over x yields
          ρ(L) ≥ 2∥y∥ ; minimizing over y ∈ L∗ \ {0} gives the claim.
                   1
                                   √
          Together with ρ(L) ≤ C2 n from Step 2 this implies
                                                       1
                                        λ1 (L∗ ) ≥         ≥ c2 n−1/2
                                                     2ρ(L)

          for an absolute c2 > 0.
      (ii) Seysen’s theorem: there exists a basis B = [b1 · · · bn ] of L with dual basis B ∗ =
           [b∗1 · · · b∗n ] such that
                                      S(B) = max ∥bi ∥ ∥b∗i ∥ ≤ CS n
                                                 i
6    CONCLUSION                                                                                      33


            for an absolute CS > 0. Put U = B −1 , so U (L) = Zn . Using ∥B∥ ≤ ∥B∥F ≤
            √                           √
              n maxi ∥bi ∥ and ∥B −1 ∥ ≤ n maxi ∥b∗i ∥, together with

                                  S(B)          S(B)                          S(B)        S(B)
                   max ∥bi ∥ ≤               ≤          ,     max ∥b∗i ∥ ≤              ≤        ,
                     i           minj ∥b∗j ∥   λ1 (L∗ )        i             minj ∥bj ∥   λ1 (L)

            we obtain the condition number bound
                                                        n S(B)2           n (CS n)2
                κ(U ) = κ(B) = ∥B∥ ∥B −1 ∥ ≤                         ≤   √              ≤ C n3
                                                     λ1 (L) λ1 (L∗ )   c1 n · c2 n −1/2


            for an absolute constant C > 0.

    4) The ellipsoid. With U from Step 3 and the lattice L from Step 2, set E = E(U ) =
       U Bn (0, λ(L)). By Step 1, E is origin–symmetric and integer–free, and

                         voln (E) = 2 n ∆(L) ≥ c0 n2 ,        κ(E) = κ(U ) ≤ C n3 .

       This proves the ellipsoid formulation with absolute constants c, C > 0.

    5) Equivalence with the packing formulation. If E ⊂ Rn is origin–symmetric and inte-
       ger–free, then { 21 E + z : z ∈ Zn } is a lattice packing with density

                                                                 n2
                                 δ = voln 12 E = 2−n voln (E) ≥ c n .
                                              
                                                                 2
       Conversely, if {Bn (ℓ, r) : ℓ ∈ L} is a lattice sphere packing, choose U ∈ GLn (R) with
       U (L) = Zn , set K = U Bn (0, r) and E = 2K. Then E is integer–free and

                                                             ωn r n
                            voln (E) = 2 n voln (K) = 2 n           = 2 n ∆(L, r).
                                                            det(L)

       Taking L from Step 2 and r = λ(L)/2 recovers the ellipsoid from Step 4, whose axis
       ratios are bounded by a fixed polynomial in n.

    Therefore, for every n ≥ 2 there exists an origin–symmetric integer–free ellipsoid E ⊂ Rn
    with voln (E) ≥ c n2 and κ(E) ≤ nC for absolute c, C > 0, and equivalently a lattice packing
    of density at least c n2 2−n .                                                             2




6     Conclusion

We described a system that employs the OpenAI LLM gpt-5 in order to prove mathematical
theorems. The system is based on protocol including an alternating loop of prover and verifier
agents impersonated by gpt-5, followed by the creation of a formal lean code version of the proof
(if any was found). A human verifies the conformance of the natural language version with the
formal version of the premises and conclusion of the theorem, which ensures proof correctness.
We showcase our system’s capabilities: (i) on the International Mathematical Olympiad prob-
lems in 2025, where our system was as successful as OpenAI and Google DeepMind’s internal
34                                                                                REFERENCES


LLMs, (ii) on the solution of several conjectures on cyclics proposed in [5], and (iii) on the
solution of a list on conjectures, formulated by the system itself, in three fields of mathematics:
gradient descent in machine learning, the 1-2-3 conjecture in graph theory, and sphere packings
in Euclidean spaces.


References

 [1] R. Anam. Prompt engineering and the effectiveness of large language models in enhancing
     human productivity. Technical Report 2507.18638v2, arXiv, 2025.

 [2] S. Armstrong and K. Sotala. How we’re predicting AI — or failing to. In J. Romportl,
     P. Ircing, E. Zackova, M. Polak, and R. Schuster, editors, Beyond AI: Artificial dreams,
     pages 52–75. University of West Bohemia, Pilsen, 2012.

 [3] T. Chang and B. Bergen. Language model behavior: A comprehensive survey. Computa-
     tional Linguistics, 50(1):293–350, 2024.

 [4] L. Chen, J. Gu, L. Huang, W. Huang, Z. Jiang, A. Jie, X. Jin, X. Jin, C. Li, K. Ma, C. Ren,
     J. Shen, W. Shi, T. Sun, H. Sun, J. Wang, S. Wang, Z. Wang, C. Wei, S. Wei, Y. Wu,
     Y. Wu, Y. Xia, H. Xin, F. Yang, H. Ying, H. Yuan, Z. Yuan, T. Zhan, C. Zhang, Y. Zhang,
     G. Zhang, T. Zhao, J. Zhao, Y. Zhou, and T. Zhu. Seed-Prover: Deep and broad reasoning
     for automated theorem proving. Technical Report 2507.23726, arXiv, 2025.

 [5] J. Cohen. Conjectures about primes and cyclic numbers. Journal of Integer Sequences,
     28:25.4.7, 2025.

 [6] S. Cook and R. Reckhow. The relative efficiency of propositional proof systems. Journal of
     Symbolic Logic, 44(1):36–50, 1979.

 [7] L. de Moura and S. Ullrich. The Lean 4 theorem prover and programming language. In
     A. Platzer and G. Sutcliff, editors, Automated Deduction — CADE 28, volume 12699 of
     LNAI, pages 625–635, Cham, 2021. Springer.

 [8] R. Fagin. Generalized first-order spectra and polynomial-time recognizable sets. In R. Karp,
     editor, Complexity of Computation, pages 43–73, Providence, RI, 1974. SIAM-AMS.

 [9] M. Feldman and A. Karbasi. Gödel Test: Can large language models solve easy conjectures?
     Technical Report 2509.18383v1, arXiv, 2025.

[10] S. Goldwasser, S. Micali, and C. Rackoff. The knowledge complexity of interactive proof
     systems. SIAM Journal on Computing, 18(1):186–208, 1989.

[11] J. Gruber. Daring fireball. https://daringfireball.net/projects/markdown/, Decem-
     ber 2004.

[12] L. Huang, W. Yu, W. Ma, W. Zhong, Z. Feng, H. Wang, Q. Chen, W. Peng, X. Feng,
     B. Oin, and T. Liu. A survey on hallucation in large language models: Principles, taxonomy,
     challenges, and open questions. ACM Transactions on Information Systems, 43(2):42/1–55,
     2025.

[13] OEIS Foundation Inc. The on-line encyclopedia of integer sequences, 2019.
REFERENCES                                                                                    35


[14] C. Jones and B. Bergen. Large language models pass the Turing test. Technical Report
     2503.23674, arXiv, 2025.

[15] R. Keusch. A solution to the 1-2-3 conjecture. Journal of Combinatorial Theory B, 166:183–
     202, 2024.

[16] L. Kovács and A. Voronkov. First-order theorem proving and Vampire. In N. Sharygina
     and H. Veith, editors, Computer-Aided Verification (CAV), volume 8044 of LNCS, pages
     1–35, Cham, 2013. Springer.

[17] A. Land and A. Doig. An automatic method of solving discrete programming problems.
     Econometrica, 28(3):497–520, 1960.

[18] Wenwu Li, X. Wang adn Wenhao Li, and B. Jin. A survey of automatic prompt engineering:
     An optimization perspective. Technical Report 2502.11560v1, arXiv, 2025.

[19] Y. Li. A practical survey on zero-shot prompt design for in-context learning. In Proceedings
     of Recent Advances in Natural Language Processing, RANLA, pages 641–647. 2023.

[20] L. Liberti and C. Lavor. Six mathematical gems in the history of distance geometry.
     International Transactions in Operational Research, 23:897–920, 2016.

[21] C. Liu, Y. Yuan, Y. Yin, Y. Xu, X. Xu, Z. Chen, Y. Wang, L. Shang, Q. Liu, and M. Zhang.
     Safe: Enhancing mathematical reasoning in large language models via retrospective step-
     aware formal verification. Technical Report 2506.04592v1, arXiv, 2025.

[22] T. Luong and E. Lockhart. Advanced version of Gemini with Deep Think officially achieves
     gold-medal standard at the international mathematical olympiad. Google DeepMind, July
     21st 2025.

[23] C. Pomerance. Patterns for cyclic numbers. Integers, to appear.

[24] B. Romera-Paredes, M. Barekatain, A. Novikov, M. Balog, M. Pawan Kumar, E. Dupont,
     F. Ruiz, J. Ellenberg, P. Wang, O. Fawzi, P. Kohli, and A. Fawzi. Mathematical discoveries
     from program search with large language models. Nature, 625:468–475, 2024.

[25] S. Schulhoff, M. Ilie, N. Balepur, K. Kahadze, A. Liu, C. Si, Y. Li, A. Gupta, H. Han,
     S. Schulhoff, P. Sandeep Dulepet, S. Vidyadhara, D. Ki, S. Agrawal, C. Pham, G. Kroiz,
     F. Li, H. Tao, A. Srivastava, H. Da Costa, S. Gupta, M. Rogers, I. Goncearenco, G. Sarli,
     I. Galynker, D. Peskoff, M. Carpuat, J. White, S. Anadkat, A. Hoyle, and P. Resnik. The
     prompt report: A systematic survey of prompt engineering techniques. Technical Report
     2406.06608v6, arXiv, 2024.

[26] K. Seßler, Y. Rong, E. Gözlüklü, and E. Kasneci. Benchmarking large language models for
     math reasoning tasks. Technical Report 2408.10839v2, arXiv, 2024.

[27] R.M. Smullyan. Theory of formal systems. Princeton University Press, Princeton, NJ, 1961.

[28] P. Song, K. Yang, and A. Anandkumar. Lean copilot: Large Language Models as copilots
     for theorem proving in Lean. In G. Pappas, P. Ravikumar, and S. Sashia, editors, 2nd
     International Conference on Neuro-symbolic Systems (NEUS), volume 288 of Proceedings
     of Machine Learning Research, pages 1–26. ML Research Press, 2025.
36                                                                              REFERENCES


[29] SRILAB, EHTZ, and INSAIT. MathArena: Evaluating LLMs on uncontaminated math
     competitions. https://matharena.ai/?comp=imo--imo 2025, Sept 30th 2025.

[30] A. Turing. On computable numbers, with an application to the Entscheidungsproblem.
     Proceedings of the London Mathematical Society, 42(1):230–265, 1937.

[31] A. Turing. Computing machinery and intelligence. Mind, 59:433–460, 1950.

[32] L. Valiant. Probably Approximately Correct. Basic Books, New York, 2013.

[33] K. Vodrahalli, S. Onta nón, N. Tipuraneni, K. Xu, S. Jain, R. Shivanna, J. Hui, N. Dikkala,
     M. Kazemi, B. Fatemi, R. Anil, E. Dyer, S. Shakeri, R. Vij, H. Mehta, V. Ramasesh,
     Q. Le, E. Chi, Y. Lu, O. Firat, A. Lazaridou, J.-B. Lespiau, N. Attaluri, and K. Ol-
     szewska. Michelangelo: Long context evaluations beyond haystacks via latent structure
     queries. Technical Report 2409.12640v2, arXiv, 2024.

[34] P. Wadler. Propositions as types. Communications of the ACM, 58(12):75–84, 2015.

[35] A. Wei. Openai experimental reasoning llm has achieved a longstanding grand challenge in
     ai. OpenAI, July 19th 2025.

[36] K. Weng, L. Du, S. Li, W. Lu, H. Sun, H. Liu, and T. Zhang. Autoformalization in the era
     of large language models. Technical Report 2505.23486v2, arXiv, 2025.

[37] Z. Zhang, J. Xu, Z. He, T. Liang, Q. Liu, Y. Li, L. Song, Z. Liang, Z. Zhang, R. Wang,
     Z. Tu, H. Mi, and D. Yu. DeepTheorem: Advancing LLM reasoning for theorem proving
     through natural language and reinforcement learning. Technical Report 25050.23754v2,
     arXiv, 2025.

[38] C. Zheng, H. Wang, E. Xie, Z. Liu, J. Sun, H. Xin, J. Shen, Z. Li, and Y. Li. Lyra:
     Orchestrating dual correction in automated theorem proving. Technical Report 2309.15806,
     arXiv, 2023.
