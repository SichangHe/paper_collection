                                                    Models That Prove Their Own Correctness


                                                 Noga Amit∗          Shafi Goldwasser∗            Orr Paradise∗          Guy N. Rothblum∗
                                                 UC Berkeley           UC Berkeley                UC Berkeley                 Apple



                                                                                        Abstract
arXiv:2405.15722v4 [cs.LG] 18 Dec 2025




                                                   How can we trust the correctness of a learned model on a particular input of in-
                                                   terest? Model accuracy is typically measured on average over a distribution of in-
                                                   puts, giving no guarantee for any fixed input. This paper proposes a theoretically-
                                                   founded solution to this problem: to train Self-Proving models that prove the cor-
                                                   rectness of their output to a verification algorithm V via an Interactive Proof. Self-
                                                   Proving models satisfy that, with high probability over an input sampled from a
                                                   given distribution, the model generates a correct output and successfully proves
                                                   its correctness to V. The soundness property of V guarantees that, for every in-
                                                   put, no model can convince V of the correctness of an incorrect output. Thus, a
                                                   Self-Proving model proves correctness of most of its outputs, while all incorrect
                                                   outputs (of any model) are detected by V . We devise and analyze two generic
                                                   methods for learning Self-Proving models: Transcript Learning (TL) which relies
                                                   on access to transcripts of accepting interactions, and Reinforcement Learning
                                                   from Verifier Feedback (RLVF) which trains a model by emulating interactions
                                                   with the verifier.


                                         Contents

                                         1   Introduction                                                                                          2

                                         2   Related Work                                                                                          3

                                         3   Defining Self-Proving Models                                                                          4

                                         4   Algorithms for Learning Self-Proving Models                                                           8

                                         5   Convergence of Transcript Learning                                                                   12

                                         6   Learning From Annotations                                                                            13

                                         7   Experiments                                                                                          13

                                         8   Conclusion                                                                                           17

                                         A Formal Proofs                                                                                          24

                                         B Full Details of the Experimental Setup                                                                 29
                                             ∗
                                             Authors listed alphabetically. This paper appeared under the title “A Theory for Worst-Case vs. Average-
                                         Case Guarantees for LLMs” [Amit et al., 2025].

                                         39th Conference on Neural Information Processing Systems (NeurIPS 2025).
                                              Input 𝒙

                                          Output 𝒚
                 Self-Proving                              Verification
                 Model                                  𝒒𝟏 Algorithm
                                         𝒂𝟏


                                 𝑷𝜽      𝒂𝑹
                                                        𝒒𝑹
                                                                            𝑽
                                                             accept/reject
Figure 1: Self-Proving models. For input x, Self-Proving model Pθ generates an output y and
sends it to a Verification Algorithm V . Then, over i ∈ [R] rounds, V sends query qi , and receives
an answer ai from Pθ . Finally, V decides (“accept/reject”) whether it is convinced that y is a correct
output for x.



1   Introduction

Bob is studying for his algebra exam and stumbles upon a question Q that he cannot solve. He
queries a Large Language Model (LLM) for the answer, and it responds with a number: 42. Bob
is aware of recent research showing that the LLM attains a 90% score on algebra benchmarks (cf.
Frieder et al. 2023), but should he trust that the answer to his particular question Q is indeed 42?
Bob could ask the LLM to explain its answer in natural language. Though he must proceed with cau-
tion, as the LLM might try to convince him of an incorrect answer [Turpin et al., 2023]. Moreover,
even if 42 is the correct answer, the LLM may fail to produce a convincing proof [Wang et al., 2023].
If only the LLM could formally prove its answer, Bob would verify the proof and be convinced.
This paper initiates the study of Self-Proving models (Fig. 1) that prove the correctness of their
answers via an Interactive Proof system [Goldwasser et al., 1985]. Self-Proving models successfully
convince a verification algorithm V with worst-case soundness guarantees: for any question, V
rejects all incorrect answers with high probability over the interaction. This guarantee holds even
against provers that have access to V ’s specification, and unbounded computational power.
Our contributions are as follows.

       • We define Self-Proving models (Section 3).

       • We propose two methods for learning Self-Proving models (Section 4). The first, Tran-
         script Learning (TL), relies on access to transcripts of accepting interactions. The second
         method, Reinforcement Learning from Verifier Feedback (RLVF), trains a model by emu-
         lating interactions with the verifier.

       • We prove gradient approximation lemmas for both methods (Theorems 4.2 and 4.3), and
         a convergence bounds for TL under convexity and Lipschitzness assumptions (Section 5).
         These are supplemented by empirical validation on a simple arithmetic capability (Sec-
         tion 7). Code and data are at https://github.com/orrp/self-proving-models

This paper develops a theory of learned models that prove their own correctness via an interactive
proof system, and thus lies at the intersection of machine learning and Interactive Proof systems. We
defer the discussion of relevant prior work from these areas to the related work section in Section 2.
The rich and well-studied question of which settings are verifiable within an interactive proof system
is beyond our scope. Our theory is general in that it applies to any setting which is verifiable within
an interactive proof system, e.g., any decision problem solvable in polynomial space [Shamir, 1992].
For a broader introduction to proof systems, see Goldreich [2008].


                                                  2
2   Related Work
We overview related work from machine learning (ML) and interactive proof systems (IPs) literature.

ML and IPs. IPs have found numerous applications in ML towards a diverse set of goals. Anil
et al. [2021] introduce Prover–Verifier Games (PVGs), a game-theoretic framework for learned
provers and learned verifiers. Since our paper initially appeared, PVGs were further investigated
in at least two subsequent works: Hammond and Adam-Day [2025] study multi-prover and Zero
Knowledge variants of PVGs. Additionally, Kirchner et al. [2024] successfully utilize PVGs to-
wards obtaining human-legible outputs from LLMs. Notably, they require a relaxed completeness
guarantee of their learned proof system—this requirement is the same as our Theorem 3.4 of Self-
Proving models.
Beyond PVGs, Wäldchen et al. [2024] cast the problem of model interpretability as a Prover–Verifier
interaction between a learned feature selector and a learned feature classifier. Debate systems [Con-
don et al., 1995], a multiprover variant of IPs, were considered for aligning models with human
values [Irving et al., 2018, Brown-Cohen et al., 2024]. In such Debate systems, two competing
models are each given an alleged answer y ̸= y ′ , and attempt to prove the correctness of their an-
swer to a (human or learned) judge. Lastly, Murty et al. [2023] define Pseudointelligence: a model
learner LM and an evaluator learner LE are each given samples from a ground-truth; LM learns
a model of the ground-truth, while LE learns an evaluator of such models; the learned evaluator
then attempts to distinguish between the learned model and the ground-truth in a Turing Test-like
interaction.
All of these works consider learned verifiers, whereas our work focuses on training models that
interact with a manually-defined verifier. More related in this regard is IP-PAC [Goldwasser et al.,
2021], in which a learner proves that she learned a model that is Probably Approximately Correct
[Valiant, 1984]. We, however, consider models that prove their own correctness on a per-input basis,
rather than learners that prove average-case correctness of a model.

Models that generate formal proofs. Self-Proving models are verified by an algorithm with for-
mal completeness and soundness guarantees (see Theorem 3.2). In this sense, Self-Proving models
generate a formal proof of the correctness of their output. Several works propose specialized models
that generate formal proofs.
AlphaGeometry [Trinh et al., 2024] is capable of formally proving olympiad-level geometry prob-
lems; Others have trained models to produce proofs in Gransden et al. [2015], Polu and Sutskever
[2020] and others train models to produce proofs in Coq [Gransden et al., 2015], Metamath [Polu
and Sutskever, 2020], Lean [Yang et al., 2023], or manually-defined deduction rules [Tafjord et al.,
2021]; FunSearch [Romera-Paredes et al., 2024] evolves LLM-generated programs by systemati-
cally evaluating their correctness. Indeed, all of these can be cast as Self-Proving models developed
for specific proof systems. Meanwhile, this work defines and studies the class of such models in
general. Several works (e.g. Welleck et al. 2022) consider models that generate natural language
proofs or explanations, which are fundamentally different from formal proofs (or provers) verified
by an algorithm.

Training on intermediate steps. Chain-of-Though (CoT, Wei et al. 2022) refers to additional
supervision on a model in the form of intermediate reasoning steps. CoT is known to improve
model performance whether included in-context [Wei et al., 2022] or in the training phase itself
[Yang et al., 2022]. Transcript Learning (TL, Section 4.1) can be viewed as training the model on a
Chain-of-Thought induced by the interaction of a verifier and an honest prover (Theorem 3.2).
To complete the analogy, let us adopt the terminology of Uesato et al. [2022], who consider outcome
supervision and process supervision. In our case, the outcome is the decision of the verifier, and the
process is the interaction between the verifier and the model. Thus, Reinforcement Learning from
Verifier Feedback (RLVF, Section 4.2) is outcome-supervised while TL is process-supervised. In a
recent work, Lightman et al. [2024] find that process-supervised transformers outperform outcome-
supervised ones on the MATH dataset [Hendrycks et al., 2021].

Subsequent work on RLVF. Following the preprint version of this paper on May 2024, Rein-
forcement Learning from Verifier Feedback (RLVF, Section 4.2) has been implemented and widely


                                                  3
adopted. Of particular note is RLVR (Reinforcement Learning from Verifiable Reward, Lambert
et al. 2024), which implements RLVF by adding KL regularization to the RL objective of Algo-
rithm 2. This implementation provided valuable empirical validation and state-of-the-art perfor-
mance on full-scale LLMs, sparked additional empirical analysis [Wu et al., 2025a, Zhou et al.,
2025], and led to widespread adoption across numerous domains including medical reasoning, com-
puter vision, and robotics [Zhang et al., 2025, Wu et al., 2025b, Song et al., 2025]. Most recently,
Pyatkin et al. [2025] presented IFBench which measures performance in interactive (3-round) proof
systems. These empirical contributions complement our theoretical foundations, demonstrating the
surprising power and applicability of RLVF as a practical post-training method.

3         Defining Self-Proving Models
We introduce and formally define our learning framework in which models prove the correctness of
their output. We start with preliminaries from the learning theory and proof systems literatures in
Section 3.1. We then introduce our main definition in Section 3.2.

3.1        Preliminaries

Let Σ be a finite set of tokens and Σ∗ denote the set of finite sequences of such tokens. We consider
sequence-to-sequence models Fθ : Σ∗ → Σ∗ , which are total functions that produce an output for
each possible input sequence. A model is parameterized by a real-valued, finite dimensional vector
θ. We consider models as randomized functions, meaning that Fθ (x) is a random variable over Σ∗ ,
of which samples are denoted by y ∼ Fθ (x).
Before we can define models that prove their own correctness, we must first define correctness.
Correctness is defined with respect to an input distribution µ over Σ∗ , and a ground-truth F ∗ that
defines correct answers. For simplicity of presentation, we focus on the case that each input x ∈ Σ∗
has exactly one correct output F ∗ (x) ∈ Σ∗ , and a zero-one loss function on outputs (the general
case is deferred to Section 3.3). The fundamental goal of machine learning can be thought of as
learning a model of the ground-truth F ∗ . Formally,
Definition 3.1 (Correctness). Let µ be a distribution of input sequences in Σ∗ and let F ∗ : Σ∗ → Σ∗
be a fixed (deterministic) ground-truth function. For any α ∈ [0, 1], we say that model Fθ is α-
correct (with respect to µ) if
                                        Pr [y = F ∗ (x)] ≥ α.
                                       x∼µ
                                           y∼Fθ (x)

An interactive proof system [Goldwasser et al., 1985] is a protocol carried out between an efficient
verifier and a computationally unbounded prover. The prover attempts to convince the verifier of the
correctness of some assertion, while the verifier accepts only correct claims. The prover is powerful
yet untrusted; in spite of this, the verifier must reject false claims with high probability.
In the context of this work, it is important to note that the verifier is manually-defined (as opposed to
learned). Formally, the verifier is a probabilistic polynomial-time algorithm tailored to a particular
ground-truth capability F ∗ . Informally, the verifier is the anchor of trust: think of the verifier as an
efficient and simple algorithm, hosted in a trustworthy environment.
Given an input x ∈ Σ∗ , the model Fθ “claims” that y ∼ Fθ (x) is correct. We now define what
it means to prove this claim. We will use Pθ to denote Self-Proving models, noting that they are
formally the same object2 as non-Self-Proving (“vanilla”) models Fθ . This notational change is to
emphasize that Pθ first outputs y ∼ Pθ (x) and is then prompted by the verifier, unlike Fθ who only
generates an output y ∼ Fθ (x).
A Self-Proving model proves that y ∼ Pθ (x) is correct to a verifier V over the course of R rounds of
interaction (Figure 1). In each round i ∈ [R], verifier V queries Pθ on a sequence qi ∈ Σ∗ to obtain
an answer ai ∈ Σ∗ ; once the interaction is over, V accepts or rejects. For fixed x, y ∈ Σ∗ , the deci-
sion of V after interacting with Pθ is a random variable over V ’s decision (accept/reject), determined
by the randomness of V and Pθ . The decision random variable is denoted by ⟨V, Pθ ⟩ (x, y).
Next, we present a definition of Interactive Proofs restricted to our setting.
      2
          Both are randomized mappings from Σ∗ to Σ∗ .


                                                         4
Table 1: Formal guarantees. Completeness and soundness are fundamental guarantees of a veri-
fication algorithm V . Verifiability (novel in this work) is a feature of a model Pθ with respect to a
verifier V and input distribution µ. Importantly, V ’s soundness holds for any input x and output y.
                 Guarantee                        Type                                Def.
            V      Completeness & Soundness            Worst-case: ∀x, y                          3.2
            Pθ     Verifiability                       Average-case: x ∼ µ, y ∼ Pθ (x)            3.4


Definition 3.2. Fix a soundness error s ∈ (0, 1), a finite set of tokens Σ and a ground-truth
F ∗ : Σ∗ → Σ∗ . A verifier V (in an Interactive Proof) for F ∗ is a probabilistic polynomial-time
algorithm that is given explicit inputs x, y ∈ Σ∗ and black-box (oracle) query access to a prover
P .3 It interacts with P over R rounds (see Figure 1) and outputs a decision ⟨V, P ⟩ (x, y) ∈
{reject, accept}. Verifier V satisfies the following two guarantees:

        • Completeness: There exists an honest prover P ∗ such that, for all x ∈ Σ∗ ,

                                         Pr[⟨V, P ∗ ⟩(x, F ∗ (x)) accepts] = 1,

          where the probability is over the randomness of V .4
        • Soundness: For all P and for all x, y ∈ Σ∗ , if y ̸= F ∗ (x) then

                                             Pr[⟨V, P ⟩ (x, y) accepts] ≤ s,

          where the probability is over the randomness of V and P , and s is the soundness error.

The efficiency of an interactive proof is usually measured with respect to four parameters: the round
complexity R, the communication complexity (the overall number of bits transferred during the
interaction), P ∗ ’s efficiency and V ’s efficiency. These complexity measures scale with the com-
putational complexity of computing the ground-truth F ∗ . For example, an interactive proof for a
complex F ∗ may require multiple rounds of interaction.
Remark 3.3 (Verifier efficiency). Theorem 3.2 requires that V is a polynomial-time algorithm
whereas provers are unbounded. This captures a requirement for efficient verification. We chose
polynomial time as a measure of efficiency because it is common in the Proof systems literature.
That said, one could adapt Theorem 3.2 to fit alternative efficiency measures, such as space com-
plexity [Condon and Lipton, 1989] or circuit depth [Goldwasser et al., 2007]. Regardless of which
measure is taken, to avoid a trivial definition it is crucial that V should be more efficient than the
honest prover P ∗ ; else, V can simply execute P ∗ to perform the computation itself.

By definition, the soundness error s of a verifier V bounds the probability that it is mistakenly
convinced of an incorrect output; in that sense, the smaller s, the “better” the verifier V . In our
setting, we think of a manually-defined verifier V who is formally proven (by a human) to have a
small soundness error by analysis of V ’s specification.
As depicted in Figure 1, each of the model’s answers depends on all previous queries and answers
in the interaction. This captures the setting of stateful models, e.g. a session with a chatbot.
Towards defining Self-Proving models (Section 3.2), let us observe the following. Completeness
and soundness are worst-case guarantees, meaning that they hold for all possible inputs x ∈ Σ∗ .
In particular, completeness implies that for all x ∈ Σ∗ , the honest prover P ∗ convinces V of the
correctness of F ∗ (x); in classical proof systems there is no guarantee that an “almost honest” prover
can convince the verifier (cf. Paradise 2021). Yet, if we are to learn a prover Pθ , we cannot expect it
to agree with P ∗ perfectly, nor can we expect it to always output F ∗ (x). Indeed, Self-Proving mod-
els will have a distributional guarantee with respect to inputs x ∼ µ. This distinction is summarized
in Table 1.
   3
      We intentionally write P rather than Pθ : Interactive Proofs are defined with respect to all possible provers,
not just parameterized ones.
    4
      WLOG, the honest prover is deterministic by fixing the optimal randomness of a randomized prover.


                                                         5
3.2        Self-Proving Models

We define the Verifiability of a model Pθ with respect to an input distribution µ and a verifier V .
Intuitively, Verifiability captures the ability of the model to prove the correctness of its answer
y ∼ Pθ (x), when the input x is sampled from µ. We refer to models capable of proving their
own correctness as Self-Proving models. Notice that, as in Theorem 3.2, the verifier is fixed and
agnostic to the choice of the Self-Proving model.
Definition 3.4 (Self-Proving model). Fix a verifier V for a ground-truth F ∗ : Σ∗ → Σ∗ as in
Theorem 3.2, and a distribution µ over inputs Σ∗ . The Verifiability of a model Pθ : Σ∗ → Σ∗ is
defined as
                                         Pr [⟨V, Pθ ⟩ (x, y) accepts] .
                          verV,µ (θ) := x∼µ                                                 (1)
                                                   y∼Pθ (x)

We say that model Pθ is β-Self-Proving with respect to V and µ if verV,µ (θ) ≥ β.
Remark 3.5 (Verifiability =⇒ correctness). Notice that the ground-truth F ∗ does not appear in
Theorem 3.4 except for the first sentence. Indeed, once it is established that V is a verifier for F ∗
(as per Theorem 3.2), then Verifiability w.r.t V implies correctness w.r.t F ∗ : Consider any input
distribution µ, ground-truth F ∗ , and a verifier V for F ∗ with soundness error s. By a union bound,
if a model Pθ is β-Verifiable, then it is (β − s)-correct. That is to say, Verifiability is formally a
stronger guarantee than correctness when V has small soundness error s.

As depicted in Figure 1, a Self-Proving model Pθ plays a dual role: first, it generates an output
y ∼ Pθ (x), and then it proves the correctness of this output to V . Note also that Verifiability is a
feature of a model, unlike completeness and soundness which are features of a verifier (see Table 1).
The benefit of Verifiability over correctness is captured by the following scenario. Alice wishes
to use a model Pθ to compute some functionality F ∗ on an input x0 in a high risk setting. Alice
generates y0 ∼ Pθ (x0 ). Should Alice trust that y0 is correct? If Alice has a held-out set of la-
beled samples, she can estimate Pθ ’s average correctness on µ. Unfortunately, (average) correctness
provides no guarantee regarding the correctness of the particular (x0 , y0 ) that Alice has in hand.
If, however, Alice has access to a verifier V for which Pθ is Self-Proving, then she can trust the
model on an input-by-input (rather than average-case) basis: Alice can execute V on (x0 , y0 ) and
black-box access to Pθ . Soundness of V guarantees that if y0 is incorrect, then V rejects with high
probability, in which case Alice should either generate Pθ (x0 ) again—or find a better model.

3.3        A Definition for General Loss Functions and One-To-Many Relations

We present variants of Self-Proving models (Theorem 3.4) generalized to one-to-many relations, and
general bounded loss functions. While these generalizations provide a richer framework that may
accommodate a wider range of applications, the theorems in this paper are based on the forgoing
Theorem 3.4, which captures the essential properties while remaining mathematically manageable.

General (bounded) loss functions. In Theorem 3.1 we implicitly use the 0-1 loss when measuring
the correctness of a model: For any x ∈ X, we measure only whether the model generated the
correct output y = F ∗ (x), but not how “far” the generated y was from F ∗ (x). It is often the case
in machine learning that we would be satisfied with models that generate a “nearly-correct” output.
This is formalized by specifying a loss function ℓ : Σ∗ × Σ∗ → [0, 1] and measuring the probability
that ℓ(x, y) is smaller than some threshold λ ∈ [0, 1), where x is drawn from the input distribution
µ, and y is generated by the model when given input x.
In the context of language modeling, different loss function allow for a more fine-grained treatment
of the semantics of a given task. As an example, consider the prime-counting task:

             • Given an integer x < 109 , output the number of primes less than or equal to x.

In the notation of Section 3, the prime-counting task would be captured by the ground-truth function
                                     F ∗ (x) := |{p ∈ N | p ≤ x, p is prime}| .5
      5
          Formally, the input and output are strings in Σ∗ representing integers (e.g. in decimal representation).


                                                              6
Per Theorem 3.1, any output other than F ∗ (x) is “just as incorrect” as any other. Yet, we might
prefer outputs that are closer to the correct answer, say, in L1 norm. This preference can be captured
by the following bounded loss function
                                          |y − F ∗ (x)| · 10−9     if y ≤ 109
                                        
                           ℓ1 (x, y) :=
                                          1                        else.
In particular, if we are interested in knowing the answer only up to some additive constant C, we
could say that an output y is “correct-enough” if ℓ1 (x, y) ≤ C · 10−9 .
More generally, we relax Theorem 3.1 to capture approximate correctness as follows.
Definition 3.6 (Approximate correctness). Let µ be a distribution over input sequences in Σ∗ and let
ℓ : Σ∗ × Σ∗ → [0, 1] be a loss function. For any α, λ ∈ [0, 1], we say that model Fθ is (α, λ)-correct
with respect to µ if
                                        Pr [ℓ(x, y) ≤ λ] ≥ α.
                                       x∼µ
                                      y∼Fθ (x)


One-to-many-relations. In Section 3, we focused on the setting of models of a ground-truth func-
tion F ∗ : Σ∗ → Σ∗ . That is, when each input x has exactly one correct output, namely F ∗ (x). A
more general setting would be to consider a ground-truth relation L ⊆ Σ∗ × Σ∗ . Then, we say that
y is a correct output for x if (x, y) ∈ L. Importantly, this allows a single x to have many possible
correct outputs, or none at all.
Note that we must take care to choose a loss function ℓ that captures correctness with respect to the
relation L, i.e., ℓ(x, y) = 0 if and only if (x, y) ∈ L. Equivalently, any loss function ℓ induces a
relation L := {(x, y) | ℓ(x, y) = 0}. Therefore, our relaxation to approximate-correctness Theo-
rem 3.6 already captures the setting of one-to-many relations, since an input x may have multiple y ∗
such that ℓ(x, y ∗ ) = 0.

3.3.1   The General Definition
We first present a relaxed definition of Interactive Proof systems for verifying approximate-
correctness.
Definition 3.7 (Theorem 3.2, generalized). Fix a soundness error s ∈ (0, 1), a threshold λ ∈ [0, 1),
a finite set of tokens Σ, and a loss function ℓ : Σ∗ × Σ∗ → [0, 1]. A verifier V for ℓ with threshold
λ is a probabilistic polynomial-time algorithm that is given explicit inputs x, y ∈ Σ∗ and black-box
(oracle) query access to a prover P . It interacts with P over R rounds (see Figure 1) and outputs a
decision ⟨V, P ⟩ (x, y) ∈ {reject, accept}. Verifier V satisfies the following two guarantees:
        • Completeness: There exists an honest prover P ∗ such that, for all x, y ∈ Σ∗ , if ℓ(x, y) = 0
          then
                                        Pr[⟨V, P ∗ ⟩(x, y) accepts] = 1,
          where the probability is over the randomness of V .
        • Soundness: For all P and for all x, y ∈ Σ∗ , if ℓ(x, y) > λ then
                                        Pr[⟨V, P ⟩ (x, y) accepts] ≤ s,
          where the probability is over the randomness of V and P , and s is the soundness error.
Indeed, for a given ground-truth function F ∗ : Σ∗ → Σ∗ , Theorem 3.2 can be recovered by choosing
the 0-1 loss
                                                 1 if x ̸= F ∗ (y)
                                               
                                 ℓF (x, y)
                                   ∗       :=
                                                 0 else
and any threshold λ ∈ [0, 1).
Remark 3.8 (Connection to Interactive Proofs of Proximity). Theorem 3.7 can be seen as a slight
generalization of (perfect completeness) Interactive Proofs of Proximity (IPPs, Rothblum et al.
2013). An IPP for a relation L ⊆ Σ∗ × Σ∗ with proximity parameter λ is obtained by instanti-
ating Theorem 3.7 with the loss function ℓHamming defined by
                                         #{i | yi ̸= yi∗ }
                                                                                     
              ℓHamming (x, y) := min                       (x, y ∗ ) ∈ L, |y ∗ | = |y| ,
                                               |y|

                                                   7
that is, ℓHamming (x, y) is the fraction of tokens in y that must be changed to obtain an output
y ∗ with (x, y ∗ ) ∈ L. However, the motivation of Rothblum et al. [2013] was studying sublinear
time verification, whereas ours is to relax the requirements of traditional Interactive Proofs towards
meeting common desiderata in machine learning.

With this relaxed notion of Interactive Proofs in hand, we are now ready to define Self-Proving
models for general (bounded) loss functions.
Definition 3.9 (Theorem 3.4, generalized). Fix a loss function ℓ : Σ∗ × Σ∗ → [0, 1], a verifier V for
ℓ with threshold λ ∈ [0, 1) as in Theorem 3.7, and a distribution µ over inputs Σ∗ . The Verifiability
of a model Pθ := Σ∗ → Σ∗ is defined as
                            verV,µ (θ) :=    x∼µ
                                                Pr     [⟨V, Pθ ⟩ (x, y) accepts] .
                                            y∼Pθ (x)

We say that model Pθ is β-Self-Proving with respect to V and µ if verV,µ (θ) ≥ β.

Analogously to Theorem 3.5, we observe that Verifiability as per Theorem 3.9 implies approximate-
correctness: Suppose Pθ is β-Self-Proving model with respect to a verifier V that has soundness
error s and threshold parameter λ for loss function ℓ. Then, by a union bound,
                                       Pr
                                      x∼µ
                                                [ℓ(x, y) ≤ λ] ≥ β − s.
                                     y∼Pθ (x)

Importantly, as emphasized throughout this paper, soundness of V implies that for all inputs x, any
output y such that ℓ(x, y) > λ is rejected with high probability (1 − s).

4     Algorithms for Learning Self-Proving Models
With a sound verifier V at hand, obtaining Self-Proving models with respect to V holds great
promise: a user that prompts the model with input x does not need to take it on good faith that
Pθ (x) is correct; she may simply verify this herself by executing the verification protocol. How,
then, can we learn models that are not just approximately-correct, but Self-Proving as well?
We focus on differentiable autoregressive models, and assume that the learner has access to input
samples x ∼ µ and correct outputs F ∗ (x), as well as the verifier’s specification (code). Additionally,
the learner can emulate the verifier, as the latter is computationally efficient (Theorem 3.3).
Importantly, we may not assume that the verifier V is differentiable—it is an arbitrary (efficient
oracle) Turing machine—and so we cannot directly compute gradients of its decision with respect
to model parameters. The challenge is to align the model with a verifier. Algorithms 1 and 2
address this challenge by (essentially) computing unbiased estimators for the Verifiability verV (θ)
or a surrogate (lower-bound) thereof. We formally prove these properties in Theorems 4.2 and 4.3.
Our approach is inspired by Reinforcement Learning from Human Feedback [Christiano et al.,
2017], a method for aligning models with human preferences, which has recently been used to
align sequence-to-sequence models [Ouyang et al., 2022]. However, there are two important differ-
ences between humans and algorithmic verifiers: (1) Verifiers are efficient algorithms which may
be emulated by the learner. This is unlike humans, whose preferences are costly to obtain. On the
other hand, (2) verifiers make a single-bit decision at the end of an interaction, but cannot guide the
prover (model) in intermediate rounds. In RL terms, this is known as the exploration problem for
sparse reward signals (e.g. Ladosz et al. 2022).
The full specification of the learning model can be found in Section A.1. We will refer to the
transcript of an interaction between a verifier and a prover (see Figure 1), denoted by π =
(y, q1 , a1 , . . . , qR , aR ). Let π<s ∈ Σs−1 denote the s-token long prefix of π.

4.1   Transcript Learning

We first present an algorithm for learning Self-Proving models which relies on access to a distribu-
tion of accepting transcripts. We focus on the algorithm first, and then discuss how the learner may
obtain accepting transcripts in Section 4.1.1. The idea is to learn a model not just of x 7→ y ∗ for a
correct output y ∗ , but of x 7→ y ∗ π ∗ , where π ∗ is a transcript of an interaction in which the verifier


                                                       8
    accepted. Formally, Transcript Learning assumes access to a transcript generator—a random vari-
    able over transcripts that faithfully represents the interaction of the verifier with some prover for a
    given input. An honest transcript generator is one which is fully supported on transcripts accepted
    by the verifier. These are defined next.
    Definition 4.1 (Transcript generator). Fix a verifier V in a proof system of R ∈ N rounds. A
    transcript generator TV for V is a randomized mapping from inputs x ∈ Σ∗ to transcripts π =
    (y, q1 , a1 , . . . , qR , aR ) ∈ Σ∗ . For any input x, TV (x) satisfies that for each r ≤ R, the marginal of
    TV (x) on the rth query qr agrees with the corresponding marginal of the query generator (Vq )r .6
    A transcript generator TV∗ := TV is honest if it is fully supported on transcripts π ∗ for which the
    verifier accepts.

    Notice that for any verifier V , there is a one-to-one correspondence between transcript generators
    and (possibly randomized) provers. We intentionally chose not to specify a prover in Theorem 4.1 to
    emphasize that transcripts can be “collected” independently of the honest prover (see completeness
    in Theorem 3.2), and in fact can be collected “in advance” prior to learning (see Figure 2). As long
    as the generator is fully supported on honest transcripts, it can be used for Transcript Learning as
    depicted in Algorithm 1 and Figure 2.

  Algorithm 1: Transcript Learning (TL)
  Hyperparameters: Learning rate λ ∈ (0, 1) and number of samples N ∈ N.
  Input: An autoregressive model family {Pθ }θ∈Rd , verifier specification (code) V , and sample
           access to an input distribution µ and an accepting transcript generator TV∗ (·).
  Output: A vector of parameters θ̄ ∈ Rd .
1 Initialize θ0 := ⃗ 0.
2 for i = 0, . . . , N − 1 do
3      Sample x ∼ µ and π ∗ = (y ∗ , q1∗ , a∗1 , . . . , qR   ∗
                                                                , a∗R ) ∼ TV∗ (x). Denote a0 := y ∗ .
4      foreach Round of interaction r = 0, . . . , R do
5          Let S(r) denote the indices of the rth answer ar in π ∗ , and let π<s denote the prefix of
            the partial transcript (y, q1∗ , a∗1 , . . . , qr∗ ).
6          for s ∈ S(r) do
7              Compute                                                     # Forwards and backwards pass
                                    αs (θi ) :=         Pr         [σ = πs∗ ]
                                                   σ∼pθi (xπ<s )

                                        d⃗s (θi ) := ∇θ log αs (θi ) = ∇θ log             Pr         [σ = πs∗ ].
                                                                                     σ∼pθi (xπ<s )

8       Update
                                                             Y                        X
                                  θi+1 := θi + λ ·                     αs (θi ) ·               d⃗s (θi ).
                                                        r∈[R]∪{0}                   r∈[R]∪{0}
                                                         s∈S(r)                      s∈S(r)

    Output θ̄ := N1
                      P
9                         i∈[N ] θi .



    TL trains a Self-Proving model by autoregressively optimizing towards generating accepting tran-
    scripts. At a high level, it works by repeatedly sampling x ∼ µ and y ∗ π ∗ ∼ T ∗ (x), and updating the
    logits log pθ towards agreeing with y ∗ π ∗ via Gradient Ascent. While TL does not directly estimate
    the Verifiability gradient ∇θ verV (θ), we are able to show that it estimates a gradient of a lower-
    bounding function A(θ) ≤ verV (θ). Therefore, as it ascends the gradient, it optimizes verV (θ)
    via the surrogate. Formally, the lower-bounding function A(θ) is the agreement of the transcripts
    generated by the current model Pθ , with the transcripts generated by the honest transcript generator.
    That is, A(θ) := Pr[π = π ∗ ] where the probability is over x ∼ µ, πθ ∼ TVθ (x), and π ∗ ∼ TV∗ (x).
       6
          A query generator Vq corresponding to V takes as input a partial interaction and samples from the dis-
    tribution over next queries by V . Formally, for any r ≤ R, given input x, output y, and partial interaction
    (qi , ai )ri=1 , Vq (x, y, q1 , a1 , . . . , qr , ar ) is a random variable over ΣLq . For completeness’ sake, we can say
    that when prompted with any sequence z that does not encode an interaction, Vq (z) is fully supported on a
    dummy sequence ⊥ · · · ⊥ ∈ ΣLq .


                                                                   9
Figure 2: Transcript Learning, visualized. To understand Algorithm 1, consider the above visu-
alization. In Phase 1, N honest transcripts are collected by interacting an honest prover with the
Verifier; these serve as samples from the transcript generator TV∗ (x). Phase 2 runs Algorithm 1:
for each transcript π ∗ (lines 2–3) and each prefix πs (lines 4–6), the values αs (θi ) and d⃗s (θi ) are
computed via forward and backward passes (line 7), followed by a parameter update (line 8).


Lemma 4.2 (TL gradient estimation). Fix an input distribution µ over Σ∗ and a verifier V with
round complexity R and answer length La . Fix an honest transcript generator TV∗ . Let θ denote the
parameters of the model Pθ , let A(θ) be as defined above and let the terms S(r), αs (θ), and d⃗s (θ)
be as defined in Algorithm 1. Then,
                                                                         
                                               Y                     X
                                                                               d⃗s (θ)
                                                                                     
                       ∇A(θ) =       E
                                    x∼µ 
                                                       αs (θ) ·                      .
                                  π ∗ ∼TV∗ r∈[R]∪{0}               r∈[R]∪{0}
                                            s∈S(r)                  s∈S(r)


The proof is deferred to Section A.2. Note that Theorem 4.2 is true for any model Pθ . Moreover, the
random vector over which the expectation is taken (in the right hand side) is precisely the direction
of the update performed in Algorithm 1. In Section 5, we will use Theorem 4.2 to prove convergence
bounds for TL under certain conditions.

4.1.1   Access to Accepting Transcripts
As mentioned, Transcript Learning relies on access to accepting transcripts. In this section we
discuss how such access can be realized (grounded in the theory of Interactive Proofs).

Doubly-Efficient Interactive Proofs. When the honest prover P ∗ is efficient (polynomial time),
the learner (who has the code for P ∗ and V ) can execute P ∗ on input x to collect accepting
transcripts—asuming no distribution shift at inference time. This setting is formalized by the notion
of Doubly-Efficient Interactive Proofs (DEIPs), introduced in the foundational work of Goldwasser
et al. [2015], who construct DEIPs for all problems computable by log-space uniform families of
polynomial-size circuits with polylogarithmic depth. Their protocols ensure that the verifier runs in
nearly linear time, while the prover operates in polynomial time—or more generally, in time pro-
portional to the circuit size. Later, Reingold et al. [2016] showed that any problem computable by
a Turing machine running in polynomial time and sublinear space admits a constant-round DEIP.
Subsequent theoretical works (e.g., Goldreich and Rothblum 2018a,b) have constructed DEIPs for
specific problems, while applied works (e.g., Zhang et al. 2021, Thaler 2013) have improved the
time and space complexity of such protocols in practice.


                                                   10
     Backward Data Generation. Recent works on “AI for advanced mathematical problems” [Char-
     ton et al., 2021, Alfarano et al., 2024] propose to reverse the generation process of problem-solution
     pairs as follows: rather than sampling problems and searching for solutions, one first samples so-
     lutions and then constructs the corresponding problems. In our setting, this inspires the following
     approach. Suppose it is computationally hard in the worst case to start with the input x and generate
     an accepting transcript π = (y, q1 , a1 , . . . , qR , aR ) for x. Could we instead jointly sample (x, π),
     or first sample a transcript π and then extract the input x for which π is an accepting transcript?
     As long as the resulting x’s are distributed the same as inference time, this would enable Transcript
     Learning of such instances.
     We explain the idea further with a cryptographic example. Setting up a Diffie–Hellman key-
     exchange scheme for security parameter 1k requires producing as a public parameter a prime p
     in a factored form, namely p − 1 = Πqi αi where qi are primes. However, factoring (p − 1) is gen-
     erally hard. Instead, one could go “backwards:” first generate (p − 1) in factored form by choosing
     primes qi and exponents αi [Kalai, 2003] and then testing if p = 1 + Πqi αi is prime. By the prime
     number theorem, p is likely to be prime after a few attempts. In the context of our paper, one may
     ask a Self-Proving model to produce certified primes, training it on tuples (x := p, π := (qi , αi )i ).

     4.2     Reinforcement Learning from Verifier Feedback (RLVF)

     As mentioned in Section 4.1, Transcript Learning uses access to an honest transcript generator to
     estimate gradients of (a lower bound on) the Verifiability of a model Pθ . Next we present Reinforce-
     ment Learning from Verifier Feedback (RLVF, Algorithm 2), which estimates this gradient without
     access to a transcript generator.


   Algorithm 2: Reinforcement Learning from Verifier Feedback (RLVF)
   Hyperparameters: Learning rate λ ∈ (0, 1) and number of samples N ∈ N.
   Input: An autoregressive model family {Pθ }θ∈Rd , initial parameters θ0 ∈ Rd , verifier
           specification (code) V , and sample access to an input distribution µ.
   Output: A vector of parameters θ̄ ∈ Rd .
 1 for i = 0, . . . , N − 1 do
 2     Sample x ∼ µ.
 3     Initialize a0 := y ∼ Pθi (x).
 4     foreach Round of interaction r = 1, . . . R do
 5          Sample the rth query                                        # Emulate the verifier
                                             qr ∼ Vq (x, a0 , q1 , a1 , . . . , qr−1 , ar−1 ).
                 Sample the rth answer                                                            # Forwards pass
                                                 ar ∼ Pθi (x, a0 , q1 , a1 , . . . , qr ).
                Let τr := (a0 , q1 , . . . , ar−1 , qr ).
 6             for s ∈ [La ] do
 7                 Let ar,s denote the sth token in ar . Compute                                  # Backwards pass

                                                d⃗s (θi ) := ∇θ log        Pr      [σ = ar,s ].
                                                                       σ∼pθi (xτr )

 8         if V (x, y, q1 , a1 , . . . , qR , aR ) accepts then
 9             Update
                                                                          X
                                                    θi+1 := θi + λ ·               d⃗s (θi ).
                                                                       r∈[R]∪{0}
                                                                         s∈[La ]

     Output θ̄ := N1
                        P
10                         i∈[N ] θi .



     Note that the parameters are updated (line 11) only when an accepting transcript was generated.
     This means that the learner can first fully generate the transcript (lines 6-7), and then take backwards


                                                                11
passes (line 9) only if the transcript was accepted by V . This is useful in practice (e.g. when using
neural models) as backwards passes are more computationally expensive than forwards passes.
On the other hand, this means that RLVF requires the parameter initialization θ0 to have Verifiability
bounded away from 0, so that accepting transcripts are sampled with sufficient probability. Fortu-
nately, such a Self-Proving base model can be learned using TL. This gives a learning paradigm
in which a somewhat-Self-Proving base model is learned with TL (with Verifiability δ ≫ 0), and
then “amplified” to a fully Self-Proving model using RLVF. This can be seen as an adaptation of the
method of Nair et al. [2018] to the setting of Self-Proving models.
When comparing Algorithms 1 and 2, we see that the latter (RLVF) does not keep track of the prob-
abilities αs . This is because, in RL terms, RLVF is an on-policy algorithm; it generates transcripts
using the current learned model, unlike TL that samples them from a distribution whose parameter-
ization is unknown to the learner. Hence, the update step in RLVF is simpler than TL.
We show that the update step in RLVF maximizes the Verifiability of Pθ .
Lemma 4.3 (RLVF gradient estimation). Fix an input distribution µ over Σ∗ and a verifier V
with round complexity R and answer length La . For any transcript (x, y, q1 , . . . , aR ) we let
AccV (x, y, q1 , . . . , aR ) denote the indicator random variable which equals 1 if and only if V ac-
cepts the transcript. For any model Pθ , denote by ver(θ) the verifiability of Pθ with respect to V
and µ (Theorem 3.4). Then, for any θ,
                                                                                    
                                                                                   X
                                                                                             d⃗s (θ)
                                                                                                   
                 ∇θ ver(θ) =       E
                                  x∼µ
                                              AccV (x, y, q1 , . . . , aR ) ·
                                                                                                   
                                y∼Pθ (x)                                         r∈[R]∪{0}
                               (qr ,ar )R
                                        r=1
                                                                                   s∈[La ]


where (qr , ar )R                                           ⃗
                r=1 are as in lines 5-6 of Algorithm 2, and ds (θ) is as defined in line 8 therein.

Note that, because AccV (·) is a 0-1 indicator of whether a transcript was accepted, then the right
hand side of the above equation is precisely the direction of the step taken in RLVF (line 9). The
proof of Theorem 4.3 can be found in Section A.3.

5   Convergence of Transcript Learning
As an application of Theorem 4.2, we prove that, under certain conditions, Transcript Learning (TL,
Algorithm 1) is expected to output a Self-Proving model. While the theorem relies on simplifying
assumptions such as convexity and Lipschitzness, it offers clean mathematical guarantees that illu-
minate the core dynamics of Transcript Learning. As we discuss following the theorem statement,
such conditions are common in theoretical machine learning literature, allowing us to build intuition
even when the assumptions may not hold in practice.
Theorem 5.1 (informal). Fix a verifier V , an input distribution µ, and an autoregressive model
family {Pθ }θ∈Rd . Fix an honest transcript generator TV∗ . Assume the following:

      1. The agreement A(θ), informally defined as the probability that Pθ generates transcripts
         agreeing with TV∗ , is concave in θ. Additionally, the logits of Pθ are BLip -Lipschitz in θ.
      2. There exist parameters θ∗ with ||θ∗ || ≤ BNorm such that Pθ∗ is (1 − ε/2)-Self Proving.
      3. The number of tokens sent by the prover in the proof system is at most C.

Then, in expectation, TL run on O(C 2 BNorm
                                       2     2
                                            BLip /ε2 ) samples outputs a (1−ε)-Self Proving model.

The full statement and proof of Theorem 5.1 are deferred to Section A.4. Its conditions can be
split into two parts. First (item 1), convexity and Lipschitzness, which are simplifying assumptions
commonly needed to prove SGD convergence. While convexity does not hold in general for DNNs,
analyzing convex settings provides clean mathematical tools for establishing foundational results—
an approach commonly used in ML theory, particularly for DNNs. Indeed, several works have
addressed the problem of proving convergence without convexity [Du et al., 2019, Bartlett et al.,
2006, Khaled and Richtárik, 2023].


                                                         12
Norm-boundedness (item 2), on the other hand, is a (necessary) realizability assumption: if the
architecture {Pθ }θ cannot be instantiated with parameters θ∗ , then it cannot be trained to be Self-
Proving. This assumption is well-grounded for transformer architectures, as recent theoretical work
has established their Turing-completeness [Bhattamishra et al., 2020, Dehghani et al., 2019].
Finally (item 3), the bound C on the communication complexity of the prover in the Interactive Proof
system. This parameter directly affects the efficiency of TL, as reflected in the number of iterations
                                                                                         2      2
(and sampled transcripts): it depends on both the optimization landscape complexity BNorm     BLip /ε2
                                       2
and the communication complexity C . Reducing communication has long been a central objective
in the study of proof systems (e.g., Goldreich and Håstad 1998, Goldreich et al. 2002, Reingold
et al. 2016). Theorem 5.1 formalizes how communication-efficient proof systems improve the per-
formance of Self-Proving models.
Remark 5.2 (Towards a convergence theorem for RLVF). RLVF can be derived by viewing Self-
Proving as a reinforcement learning problem in which the agent (prover) is rewarded when the
verifier accepts. Indeed, RLVF is the Policy Gradient method [Sutton et al., 1999] for a verifier-
induced reward. Convergence bounds for Policy Gradient methods are a challenging and active
area of research (e.g. Agarwal et al. 2021), and so we leave the full analysis to future work.

6   Learning From Annotations
To minimize the length of messages exchanged in an Interactive Proof system, the honest prover is
designed to send the shortest possible message to the verifier, containing only essential information.
However, when training Self-Proving model, it may be useful for it to first generate an “annotated”
answer ea which is then trimmed down to the actual answer a to be sent to the verifier. We adapt
Sections 3 and 4 to this setting via Annotated Transcripts. The TL and RLVF algorithms natu-
rally extend to annotated transcripts as well. Table 2 shows that annotations significantly improve
performance of TL in practice.
Annotations can be viewed as adding Chain-of-Thought [Wei et al., 2022]. As a concrete example,
consider our experiments on computing the GCD. As detailed in Section 7.2, a proof π in this setting
is the output of an iterative process—the extended Euclidean algorithm—starting from the input x:
x 7→ π1 7→ π2 7→ · · · 7→ π. The annotation of the proof π consists the first T steps (π1 , . . . , πT ) up
to some fixed cutoff T . These are prepended to the proof and shown to the model during TL training.
At inference time, the model is evaluated only on whether it generated the proof π correctly.
We formally capture annotations by introducing a transcript annotator and an answer extractor
incorporated into the training and inference stages, respectively. Fix a verifier V in an R-round
proof system with question length Lq and answer length La . An annotation system with annotation
length L
       fa consists of a transcript annotator A, and an answer extractor E.
In terms of efficiency, think of the annotator as an algorithm of the same computational resources as
an honest prover in the system (see Theorem 3.2), and the answer extractor as an extremely simple
algorithm (e.g., trim a fixed amount of tokens from the annotation).
To use an annotation system the following changes need to be made:
       • At training time, an input x and transcript π is annotated to obtain π       e := A(x, π), e.g. before
         the forwards backwards pass in TL (line 3 in Algorithm 1).
       • At inference time (i.e., during interaction between V and Pθ ), the prover keeps track of
         the annotated transcript, but in each round passes the model-generated (annotated) answer
         through the extractor E before it is sent to the verifier. That is, in each round r ∈ [R], the
         prover samples
                                      aer ∼ Pθ (x, y, q1 , ae1 , . . . , ag
                                                                          r−1 , qr ).
         The prover then extracts an answer ar := E(aer ) which is sent to the verifier.

7   Experiments
We describe our experimental setup, and present ablation studies that shed additional light on the
effect of annotation and representation on Verifiability.


                                                     13
Table 2: Self-Proving transformers computing the GCD. We train a 6.3M parameter GPT to com-
pute the GCD of two integers sampled log-uniformly from [104 ]. Vanilla GPT correctly generates
the GCD for almost all inputs, but does not prove correctness to a simple verification algorithm. GPT
trained with Transcript Learning (GPT+TL) proves its answer 60.3% of the time; adding Reinforce-
ment Learning from Verifier Feedback (+RLVF) increases this to 78.3%; training with Annotated
Transcript Learning (GPT+ATL) gives the highest Verifiability score of 96%.

                             L EARNING METHOD        C ORRECTNESS      V ERIFIABILITY
                             GPT ( BASELINE )            99.8%                -
                             GPT+TL                      98.8%              60.3%
                             GPT+TL+RLVF                 98.9%              78.3%
                             GPT+ATL                     98.6%              96.0%


7.1        Setup: Training transformers to predict the GCD

Charton [2024] empirically studies the power and limitations of learning GCDs with transformers.
We follow their setup and two conclusions on settings that make for faster learning: Training from
the log-uniform distribution, and choosing a base of representation with many prime factors.
We fix a base of representation B = 210 and use x to denote an integer x encoded as a B-ary string.7
For sequences of integers, we write (x1 x2 ) to denote the concatenation of x1 with x2 , delimited by
a special token. The vocabulary size needed for this representation is |Σ| ≈ 210.
We choose the input distribution µ to be the log-uniform distribution on [104 ], and train the trans-
former on sequences of the form (x1 x2 y), where x1 , x2 ∼ µ and y = GCD(x1 , x2 ). This is a
scaling-down of Charton [2024], to allow single GPU training of Self-Proving transformers. In all
of our experiments, we use a GPT model [Vaswani et al., 2017] with 6.3M parameters trained on a
dataset of 1024K samples in batches of 1024. Full details are deferred to Section B.2.

Proving correctness of GCD. Following Charton [2024] as a baseline, we find that transformers
can correctly compute the GCD with over 99% probability over (x1 , x2 ) ∼ µ. To what extent can
they prove their answer? To answer this question, we first devise a natural proof system based on
Bézout’s theorem. Its specification and formal guarantees are deferred to Section B.1. We denote its
verification algorithm by V , and highlight some important features of the experimental setup:

             • The proof system consists of one round (R = 1). The verifier makes no query, and simply
               receives a proof π from the prover.
             • Completeness: For any x1 , x2 , y ∈ [104 ] such that y = GCD(x1 , x2 ), there exists a proof
               π such that V (x1 x2 yπ) accepts. As detailed in Section B.1, the proof π consists of a pair
               of integers who are Bézout coefficients for x1 , x2 .
             • Soundness: If y ̸= GCD(x1 , x2 ), then V (x1 x2 yπ) rejects8 for any alleged proof π ∈ Σ∗ .

To measure Verifiability, we train a Self-Proving transformer using Transcript Learning on sequences
(x1 x2 yπ) and estimate for how many inputs x1 , x2 ∼ µ does the model generate both the correct
GCD y and a valid proof π. We test on 1000 pairs of integers x′1 , x′2 ∼ µ held-out of the training
set, prompting the model with (x′1 x′2 ) to obtain (y′ π ′ ), and testing whether V (x′1 x′2 y′ π ′ ) accepts.
Table 2 shows our main experimental result, which has the following key takeaways:

           1. Transcript Learning (TL) for 100K iterations (≈100M samples) results in a Self-Proving
              transformer that correctly proves 60.3% of its answers.
           2. A base Self-Proving Model with fairly low Verifiability of 40% can be improved to 79.3%
              via Reinforcement Learning from Verifier Feedback (RLVF). Although it does not rely on
              honest transcripts, RLVF trains slowly: this nearly-twofold improvement took four million
              iterations.
      7
          B = 210 is chosen following Charton [2024] to be an integer with many prime factors.
      8
          With probability 1, i.e., s = 0 in Theorem 3.2.


                                                         14
      3. Most efficient is Annotated Transcript Learning, which yielded a model with 96% Verifia-
         bility in 100K iterations. We further investigate their effect next.

7.2   Models generalize beyond annotations




Figure 3: Verifiability with increasing amounts of annotation. T is the number of steps added in
Annotated Transcript Learning. Dashed lines indicate Euclidean depth, that bound the Verifiability
of models that prove only for integers up to a certain number of steps. Each T was run with three
seeds, with mean ± standard error depicted. The upper graph provides a zoomed-in view of the 82%
to 98% range from the lower graph, which spans a broader scale from 20% to 100%.

The proof π is annotated by including intermediate steps in its computation. Details are deferred to
Section B.1; roughly speaking, we observe that the proof π for input (a, b) is obtained as the last
element in a sequence a, b, π1 , π2 , . . . computed by the Euclidean algorithm. We annotate the proof
π by prepending to it the sequence of Euclidean steps (π1 , . . . , πT ) up to some fixed cutoff T .
Figure 3 shows how T affects the Verifiability of the learned model. As suggested by Lee et al.
[2024], training the model on more intermediate steps results in better performance; in our case,
increasing the number of intermediate steps T yields better Self-Proving models. One might suspect
that models only learn to execute the Euclidean algorithm in-context. To rule out this hypothesis, we
derive an upper bound on the possible efficacy of such limited models. This bound is based on the
Euclidean depth of integers (x1 , x2 ), which we define as the number of intermediate steps that the
Euclidean algorithm makes before terminating on input (x1 , x2 ). Indeed, a model that only learns
to compute (in-context) the arithmetic of the Euclidean algorithm would only be able to prove the
correctness of inputs (x1 , x2 ) whose depth does not exceed the annotation cutoff T .
Figure 3 tells a different story: For each cutoff T , we estimate the probability that integers x1 , x2 ∼
µ have Euclidean depth at most T on 105 sampled pairs. Larger annotation cutoff T increases
Verifiability, but all models exceed their corresponding Euclidean depth bound.

7.3   Base of representation

As mentioned previously, Charton [2024] concludes that, for a given base of representation B,
transformers correctly compute the GCD of integers x1 , x2 that are products of primes dividing
B. Simply put, choosing a base B with many different prime factors yields models with better
correctness (accuracy), which suggests why base B = 210 = 2 · 3 · 5 · 7 yielded the best results. To


                                                   15
Figure 4: Annotated TL Verifiability as a function of the number of samples N . Each iteration
(X axis) is a batch of 1024 samples from a dataset of ≈10M sequences. Every 10k iterations,
Verifiability was evaluated on a held-out dataset of 1k inputs. T is the number of steps in Annotated
Transcript Learning (Figure 3), and T = 0 is non-annotated Transcript Learning. Each T was run
with three seeds, with mean depicted by the curve and standard error by the shaded area.




Figure 5: The number of prime divisors of a base ω(B) determines Verifiability. For each
o ∈ [4], we sampled 17 bases B ∈ {2, . . . , 1386} such that ω(B) = o. A Self-Proving transformer
was trained via Transcript Learning for twenty epochs on an identical dataset of 1024K samples
encoded in base B. For each ω(B) we depict the mean ± standard error.



test if B’s factorization has a similar effect on Verifiability, we train transformers on 68 bases varying
the number of prime divisors from ω(B) = 1 (i.e., B is a prime power) to ω(B) = 4. Figure 5
shows that ω(B) correlates not just with correctness [Charton, 2024], but also with Verifiability.
Although the finding is statistically significant (no overlapping error margins), the difference is by
a few percentages; we attribute this to the smaller (10%) number of samples on which models were
trained, relative to other experiments.


                                                   16
Figure 6: RLVF Verifiability as a function of the number of samples N . Starting from a base
model with Verifiability 48% (obtained via Transcript Learning), in each iteration a batch of 2048
inputs are sampled; the model generates a proof for each; the Verifier is used to check which proofs
are accepted; then, the model parameters are updated accordingly (see Algorithm 2). Verifiability
was evaluated on a held-out dataset of 1k inputs.


8   Conclusion

Trust between a learned model and its user is fundamental. Interactive Proofs [Goldwasser et al.,
1985] provide a general framework for establishing trust via verification algorithms. This work
shows that models can be trained to formally prove their outputs within such systems—we call these
Self-Proving models. Self-Proving models connect the theory of Interactive Proofs with the goal of
Trustworthy ML: they offer formal worst-case soundness guarantees; enabling users to be confident
when their models generate correct answers—and detect incorrect answers with high probability.
We support our definition with two general-purpose training methods: Transcript Learning (TL)
and Reinforcement Learning from Verifier Feedback (RLVF), whose analyses draw on learning
theory, RL, and computational complexity. This work can be extended in several directions: finding
conditions for the convergence of RLVF, improving sample complexity bounds for TL, or designing
altogether different learning algorithms (e.g., by taking advantage of properties of the verifier).

Limitations. In our current learning methods, each individual ground-truth capability requires
training a separate Self-Proving model. A natural generalization of this approach is to adapt our
definition and methods to deal with a single generalist Self-Proving model that proves its correctness
to multiple verifiers of different ground-truths.


                                                 17
Moreover, the second strategy presented in Section 4.1.1—namely, generating accepting transcripts
first and then constructing matching inputs—has an inherent limitation: the resulting training dis-
tribution is biased by the design of the generator. As a consequence, models may end up learning
patterns of the construction process, rather than acquiring generalizable reasoning capabilities. This
highlights the importance of using sufficiently diverse generators, and of evaluating model perfor-
mance on out-of-distribution inputs.

Acknowledgments and Disclosure of Funding
We are grateful to Micah Carroll, Mark Rofin, Avishay Tal, Mojtaba Yaghoobzadeh and anonymous
reviewers for their helpful comments. This research was supported by DARPA-TA1 under grant no.
HR001119S0076, and by the Simons Collaboration on the Theory of Algorithmic Fairness.

References
Alekh Agarwal, Sham M. Kakade, Jason D. Lee, and Gaurav Mahajan. On the theory of policy
  gradient methods: Optimality, approximation, and distribution shift. J. Mach. Learn. Res., 22:
  98:1–98:76, 2021. URL http://jmlr.org/papers/v22/19-736.html.
Alberto Alfarano, François Charton, and Amaury Hayat. Global lyapunov functions: a long-
  standing open problem in mathematics, with symbolic transformers. In Amir Globersons, Lester
  Mackey, Danielle Belgrave, Angela Fan, Ulrich Paquet, Jakub M. Tomczak, and Cheng Zhang,
  editors, Advances in Neural Information Processing Systems 38: Annual Conference on Neu-
  ral Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December
  10 - 15, 2024, 2024. URL http://papers.nips.cc/paper_files/paper/2024/hash/
  aa280e73c4e23e765fde232571116d3b-Abstract-Conference.html.
Noga Amit, Shafi Goldwasser, Orr Paradise, and Guy N. Rothblum. A theory for worst-case vs.
  average-case guarantees for LLMs. In Advances in Neural Information Processing Systems 39:
  Annual Conference on Neural Information Processing Systems 2025, NeurIPS 2025, 2025.
Cem Anil, Guodong Zhang, Yuhuai Wu, and Roger B. Grosse. Learning to give checkable answers
  with prover-verifier games. CoRR, abs/2108.12099, 2021. URL https://arxiv.org/abs/
  2108.12099.
Peter L Bartlett, Michael I Jordan, and Jon D McAuliffe. Convexity, classification, and risk bounds.
  Journal of the American Statistical Association, 101(473):138–156, 2006.
E. Bezout. Theorie Generale Des Equations Algebriques. Kessinger Publishing, 1779. ISBN
  9781162056128. URL https://books.google.co.il/books?id=wQZvSwAACAAJ.
Satwik Bhattamishra, Arkil Patel, and Navin Goyal. On the computational power of transform-
  ers and its implications in sequence modeling. In Raquel Fernández and Tal Linzen, editors,
  Proceedings of the 24th Conference on Computational Natural Language Learning, CoNLL
  2020, Online, November 19-20, 2020, pages 455–475. Association for Computational Linguis-
  tics, 2020. doi: 10.18653/V1/2020.CONLL-1.37. URL https://doi.org/10.18653/v1/
  2020.conll-1.37.
Jonah Brown-Cohen, Geoffrey Irving, and Georgios Piliouras. Scalable AI safety via doubly-
  efficient debate. In Forty-first International Conference on Machine Learning, ICML 2024, Vi-
  enna, Austria, July 21-27, 2024. OpenReview.net, 2024. URL https://openreview.net/
  forum?id=6jmdOTRMIO.
François Charton. Can transformers learn the greatest common divisor? In The Twelfth Interna-
  tional Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 6-11, 2024.
  OpenReview.net, 2024.
Francois Charton, Amaury Hayat, and Guillaume Lample. Learning advanced mathematical com-
  putations from examples. In International Conference on Learning Representations, 2021. URL
  https://openreview.net/forum?id=-gfhS00XfKj.


                                                 18
Paul F. Christiano, Jan Leike, Tom B. Brown, Miljan Martic, Shane Legg, and Dario Amodei.
  Deep reinforcement learning from human preferences. In Isabelle Guyon, Ulrike von Luxburg,
  Samy Bengio, Hanna M. Wallach, Rob Fergus, S. V. N. Vishwanathan, and Roman Gar-
  nett, editors, Advances in Neural Information Processing Systems 30: Annual Conference on
  Neural Information Processing Systems 2017, December 4-9, 2017, Long Beach, CA, USA,
  pages 4299–4307, 2017. URL https://proceedings.neurips.cc/paper/2017/hash/
  d5e2c0adad503c91f91df240d0cd4e49-Abstract.html.
Anne Condon and Richard J. Lipton. On the complexity of space bounded interactive proofs (ex-
  tended abstract). In 30th Annual Symposium on Foundations of Computer Science, Research
  Triangle Park, North Carolina, USA, 30 October - 1 November 1989, pages 462–467. IEEE Com-
  puter Society, 1989. doi: 10.1109/SFCS.1989.63519. URL https://doi.org/10.1109/SFCS.
  1989.63519.
Anne Condon, Joan Feigenbaum, Carsten Lund, and Peter W. Shor. Probabilistically checkable
  debate systems and nonapproximability of pspace-hard functions. Chic. J. Theor. Comput. Sci.,
  1995, 1995. URL http://cjtcs.cs.uchicago.edu/articles/1995/4/contents.html.
Mostafa Dehghani, Stephan Gouws, Oriol Vinyals, Jakob Uszkoreit, and Lukasz Kaiser. Universal
 transformers. In 7th International Conference on Learning Representations, ICLR 2019, New
 Orleans, LA, USA, May 6-9, 2019. OpenReview.net, 2019. URL https://openreview.net/
 forum?id=HyzdRiR9Y7.
Simon S. Du, Jason D. Lee, Haochuan Li, Liwei Wang, and Xiyu Zhai. Gradient descent finds global
  minima of deep neural networks. In Kamalika Chaudhuri and Ruslan Salakhutdinov, editors,
  Proceedings of the 36th International Conference on Machine Learning, ICML 2019, 9-15 June
  2019, Long Beach, California, USA, volume 97 of Proceedings of Machine Learning Research,
  pages 1675–1685. PMLR, 2019. URL http://proceedings.mlr.press/v97/du19c.html.
Simon Frieder, Luca Pinchetti, Alexis Chevalier, Ryan-Rhys Griffiths, Tommaso Salvatori, Thomas
  Lukasiewicz, Philipp Petersen, and Julius Berner. Mathematical capabilities of chatgpt. In Al-
  ice Oh, Tristan Naumann, Amir Globerson, Kate Saenko, Moritz Hardt, and Sergey Levine,
  editors, Advances in Neural Information Processing Systems 36: Annual Conference on Neu-
  ral Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December
  10 - 16, 2023, 2023. URL http://papers.nips.cc/paper_files/paper/2023/hash/
  58168e8a92994655d6da3939e7cc0918-Abstract-Datasets_and_Benchmarks.html.
Oded Goldreich. Probabilistic proof systems: A primer. Found. Trends Theor. Comput. Sci., 3(1):
  1–91, 2008. doi: 10.1561/0400000023. URL https://doi.org/10.1561/0400000023.
Oded Goldreich and Johan Håstad. On the complexity of interactive proofs with bounded commu-
  nication. Inf. Process. Lett., 67(4):205–214, 1998. doi: 10.1016/S0020-0190(98)00116-1. URL
  https://doi.org/10.1016/S0020-0190(98)00116-1.
Oded Goldreich and Guy Rothblum. Counting t-cliques: Worst-case to average-case reductions
  and direct interactive proof systems. In 2018 IEEE 59th Annual Symposium on Foundations of
  Computer Science (FOCS), pages 77–88, 2018a. doi: 10.1109/FOCS.2018.00017.
Oded Goldreich and Guy N. Rothblum. Simple doubly-efficient interactive proof systems for
  locally-characterizable sets. In Anna R. Karlin, editor, 9th Innovations in Theoretical Com-
  puter Science Conference, ITCS 2018, January 11-14, 2018, Cambridge, MA, USA, volume 94
  of LIPIcs, pages 18:1–18:19. Schloss Dagstuhl - Leibniz-Zentrum für Informatik, 2018b. doi:
  10.4230/LIPICS.ITCS.2018.18. URL https://doi.org/10.4230/LIPIcs.ITCS.2018.18.
Oded Goldreich, Salil P. Vadhan, and Avi Wigderson. On interactive proofs with a laconic prover.
  Comput. Complex., 11(1-2):1–53, 2002. doi: 10.1007/S00037-002-0169-0. URL https://doi.
  org/10.1007/s00037-002-0169-0.
Shafi Goldwasser, Silvio Micali, and Charles Rackoff. The knowledge complexity of interactive
  proof-systems (extended abstract). In Robert Sedgewick, editor, Proceedings of the 17th Annual
  ACM Symposium on Theory of Computing, May 6-8, 1985, Providence, Rhode Island, USA, pages
  291–304. ACM, 1985. doi: 10.1145/22145.22178. URL https://doi.org/10.1145/22145.
  22178.


                                              19
Shafi Goldwasser, Dan Gutfreund, Alexander Healy, Tali Kaufman, and Guy N. Rothblum. Ver-
  ifying and decoding in constant depth. In David S. Johnson and Uriel Feige, editors, Pro-
  ceedings of the 39th Annual ACM Symposium on Theory of Computing, San Diego, California,
  USA, June 11-13, 2007, pages 440–449. ACM, 2007. doi: 10.1145/1250790.1250855. URL
  https://doi.org/10.1145/1250790.1250855.

Shafi Goldwasser, Yael Tauman Kalai, and Guy N. Rothblum. Delegating computation: Interactive
  proofs for muggles. J. ACM, 62(4):27:1–27:64, 2015. doi: 10.1145/2699436. URL https:
  //doi.org/10.1145/2699436.

Shafi Goldwasser, Guy N. Rothblum, Jonathan Shafer, and Amir Yehudayoff. Interactive proofs
  for verifying machine learning. In James R. Lee, editor, 12th Innovations in Theoretical Com-
  puter Science Conference, ITCS 2021, January 6-8, 2021, Virtual Conference, volume 185
  of LIPIcs, pages 41:1–41:19. Schloss Dagstuhl - Leibniz-Zentrum für Informatik, 2021. doi:
  10.4230/LIPICS.ITCS.2021.41. URL https://doi.org/10.4230/LIPIcs.ITCS.2021.41.

Thomas Gransden, Neil Walkinshaw, and Rajeev Raman. SEPIA: search for proofs using inferred
  automata. In Amy P. Felty and Aart Middeldorp, editors, Automated Deduction - CADE-25 - 25th
  International Conference on Automated Deduction, Berlin, Germany, August 1-7, 2015, Proceed-
  ings, volume 9195 of Lecture Notes in Computer Science, pages 246–255. Springer, 2015. doi:
  10.1007/978-3-319-21401-6\_16. URL https://doi.org/10.1007/978-3-319-21401-6_
  16.

Lewis Hammond and Sam Adam-Day. Neural interactive proofs. In The Thirteenth International
  Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025. OpenRe-
  view.net, 2025. URL https://openreview.net/forum?id=R2834dhBlo.

Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song,
  and Jacob Steinhardt. Measuring mathematical problem solving with the MATH dataset. In
  Joaquin Vanschoren and Sai-Kit Yeung, editors, Proceedings of the Neural Information Process-
  ing Systems Track on Datasets and Benchmarks 1, NeurIPS Datasets and Benchmarks 2021, De-
  cember 2021, virtual, 2021. URL https://datasets-benchmarks-proceedings.neurips.
  cc/paper/2021/hash/be83ab3ecd0db773eb2dc1b0a17836a1-Abstract-round2.html.

Geoffrey Irving, Paul F. Christiano, and Dario Amodei. AI safety via debate. CoRR, abs/1805.00899,
  2018. URL http://arxiv.org/abs/1805.00899.

Adam Tauman Kalai. Generating random factored numbers, easily. Journal of Cryptology, 16(4):
  287–289, 2003.

Ahmed Khaled and Peter Richtárik. Better theory for SGD in the nonconvex world. Trans. Mach.
  Learn. Res., 2023, 2023. URL https://openreview.net/forum?id=AU4qHN2VkS.

Jan Hendrik Kirchner, Yining Chen, Harri Edwards, Jan Leike, Nat McAleese, and Yuri Burda.
  Prover-verifier games improve legibility of LLM outputs. CoRR, abs/2407.13692, 2024. doi:
  10.48550/ARXIV.2407.13692. URL https://doi.org/10.48550/arXiv.2407.13692.

Donald E. Knuth. The Art of Computer Programming, Volume II: Seminumerical Algorithms.
  Addison-Wesley, 1969. ISBN 0201038021. URL https://www.worldcat.org/oclc/
  310551264.

Pawel Ladosz, Lilian Weng, Minwoo Kim, and Hyondong Oh. Exploration in deep reinforcement
  learning: A survey. Inf. Fusion, 85:1–22, 2022. doi: 10.1016/J.INFFUS.2022.03.003. URL
  https://doi.org/10.1016/j.inffus.2022.03.003.

Nathan Lambert, Jacob Morrison, Valentina Pyatkin, Shengyi Huang, Hamish Ivison, Faeze Brah-
  man, Lester James V. Miranda, Alisa Liu, Nouha Dziri, Shane Lyu, Yuling Gu, Saumya Malik,
  Victoria Graf, Jena D. Hwang, Jiangjiang Yang, Ronan Le Bras, Oyvind Tafjord, Chris Wilhelm,
  Luca Soldaini, Noah A. Smith, Yizhong Wang, Pradeep Dasigi, and Hannaneh Hajishirzi. Tülu
  3: Pushing frontiers in open language model post-training. CoRR, abs/2411.15124, 2024. doi:
  10.48550/ARXIV.2411.15124. URL https://doi.org/10.48550/arXiv.2411.15124.


                                               20
Nayoung Lee, Kartik Sreenivasan, Jason D. Lee, Kangwook Lee, and Dimitris Papailiopoulos.
  Teaching arithmetic to small transformers. In The Twelfth International Conference on Learn-
  ing Representations, ICLR 2024, Vienna, Austria, May 6-11, 2024. OpenReview.net, 2024.
Hunter Lightman, Vineet Kosaraju, Yura Burda, Harrison Edwards, Bowen Baker, Teddy Lee, Jan
  Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. Let’s verify step by step. In The Twelfth
  International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 6-11,
  2024. OpenReview.net, 2024.
Shikhar Murty, Orr Paradise, and Pratyusha Sharma. Pseudointelligence: A unifying lens on lan-
  guage model evaluation. In Houda Bouamor, Juan Pino, and Kalika Bali, editors, Findings of
  the Association for Computational Linguistics: EMNLP 2023, Singapore, December 6-10, 2023,
  pages 7284–7290. Association for Computational Linguistics, 2023. doi: 10.18653/V1/2023.
  FINDINGS-EMNLP.485. URL https://doi.org/10.18653/v1/2023.findings-emnlp.
  485.
Ashvin Nair, Bob McGrew, Marcin Andrychowicz, Wojciech Zaremba, and Pieter Abbeel. Over-
  coming exploration in reinforcement learning with demonstrations. In 2018 IEEE International
  Conference on Robotics and Automation, ICRA 2018, Brisbane, Australia, May 21-25, 2018,
  pages 6292–6299. IEEE, 2018. doi: 10.1109/ICRA.2018.8463162. URL https://doi.org/
  10.1109/ICRA.2018.8463162.
Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin,
  Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser
  Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul F. Christiano, Jan
  Leike, and Ryan Lowe. Training language models to follow instructions with human feedback.
  In Sanmi Koyejo, S. Mohamed, A. Agarwal, Danielle Belgrave, K. Cho, and A. Oh, editors,
  Advances in Neural Information Processing Systems 35: Annual Conference on Neural Infor-
  mation Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 - De-
  cember 9, 2022, 2022. URL http://papers.nips.cc/paper_files/paper/2022/hash/
  b1efde53be364a73914f58805a001731-Abstract-Conference.html.
Orr Paradise. Smooth and strong pcps. Comput. Complex., 30(1):1, 2021. doi: 10.1007/
  S00037-020-00199-3. URL https://doi.org/10.1007/s00037-020-00199-3.
Stanislas Polu and Ilya Sutskever. Generative language modeling for automated theorem proving.
  CoRR, abs/2009.03393, 2020. URL https://arxiv.org/abs/2009.03393.
Valentina Pyatkin, Saumya Malik, Victoria Graf, Hamish Ivison, Shengyi Huang, Pradeep Dasigi,
  Nathan Lambert, and Hannaneh Hajishirzi. Generalizing verifiable instruction following. CoRR,
  abs/2507.02833, 2025. doi: 10.48550/ARXIV.2507.02833. URL https://doi.org/10.
  48550/arXiv.2507.02833.
Omer Reingold, Guy N. Rothblum, and Ron D. Rothblum. Constant-round interactive proofs for
 delegating computation. In Proceedings of the 48th Annual ACM SIGACT Symposium on Theory
 of Computing (STOC), pages 49–62, 2016. doi: 10.1145/2897518.2897652.
Bernardino Romera-Paredes, Mohammadamin Barekatain, Alexander Novikov, Matej Balog,
  M Pawan Kumar, Emilien Dupont, Francisco JR Ruiz, Jordan S Ellenberg, Pengming Wang,
  Omar Fawzi, et al. Mathematical discoveries from program search with large language models.
  Nature, 625(7995):468–475, 2024.
Guy N. Rothblum, Salil P. Vadhan, and Avi Wigderson. Interactive proofs of proximity: delegating
  computation in sublinear time. In Dan Boneh, Tim Roughgarden, and Joan Feigenbaum, editors,
  Symposium on Theory of Computing Conference, STOC’13, Palo Alto, CA, USA, June 1-4, 2013,
  pages 793–802. ACM, 2013. doi: 10.1145/2488608.2488709. URL https://doi.org/10.
  1145/2488608.2488709.
Shai Shalev-Shwartz and Shai Ben-David.       Understanding Machine Learning
  - From Theory to Algorithms.     Cambridge University Press, 2014.    ISBN
  978-1-10-705713-5.           URL     http://www.cambridge.org/de/academic/
  subjects/computer-science/pattern-recognition-and-machine-learning/
  understanding-machine-learning-theory-algorithms.


                                               21
Adi Shamir. IP = PSPACE. J. ACM, 39(4):869–877, 1992. doi: 10.1145/146585.146609. URL
  https://doi.org/10.1145/146585.146609.

Zirui Song, Guangxian Ouyang, Mingzhe Li, Yuheng Ji, Chenxi Wang, Zixiang Xu, Zeyu Zhang, Xi-
  aoqing Zhang, Qian Jiang, Zhenhao Chen, Zhongzhi Li, Rui Yan, and Xiuying Chen. Maniplvm-
  r1: Reinforcement learning for reasoning in embodied manipulation with large vision-language
  models. CoRR, abs/2505.16517, 2025. doi: 10.48550/ARXIV.2505.16517. URL https:
  //doi.org/10.48550/arXiv.2505.16517.

Richard S. Sutton, David A. McAllester, Satinder Singh, and Yishay Mansour. Policy gra-
  dient methods for reinforcement learning with function approximation. In Sara A. Solla,
  Todd K. Leen, and Klaus-Robert Müller, editors, Advances in Neural Information Process-
  ing Systems 12, [NIPS Conference, Denver, Colorado, USA, November 29 - December 4,
  1999], pages 1057–1063. The MIT Press, 1999. URL http://papers.nips.cc/paper/
  1713-policy-gradient-methods-for-reinforcement-learning-with-function-approximation.

Oyvind Tafjord, Bhavana Dalvi, and Peter Clark. Proofwriter: Generating implications, proofs, and
  abductive statements over natural language. In Chengqing Zong, Fei Xia, Wenjie Li, and Roberto
  Navigli, editors, Findings of the Association for Computational Linguistics: ACL/IJCNLP
  2021, Online Event, August 1-6, 2021, volume ACL/IJCNLP 2021 of Findings of ACL,
  pages 3621–3634. Association for Computational Linguistics, 2021. doi: 10.18653/V1/2021.
  FINDINGS-ACL.317. URL https://doi.org/10.18653/v1/2021.findings-acl.317.

Justin Thaler. Time-optimal interactive proofs for circuit evaluation. In Ran Canetti and Juan A.
  Garay, editors, Advances in Cryptology – CRYPTO 2013, pages 71–89, Berlin, Heidelberg, 2013.
  Springer Berlin Heidelberg.

Trieu H. Trinh, Yuhuai Wu, Quoc V. Le, He He, and Thang Luong. Solving olympiad geometry with-
  out human demonstrations. Nat., 625(7995):476–482, 2024. doi: 10.1038/S41586-023-06747-5.
  URL https://doi.org/10.1038/s41586-023-06747-5.

Miles Turpin, Julian Michael, Ethan Perez, and Samuel R. Bowman. Language models don’t
 always say what they think: Unfaithful explanations in chain-of-thought prompting. In Al-
 ice Oh, Tristan Naumann, Amir Globerson, Kate Saenko, Moritz Hardt, and Sergey Levine,
 editors, Advances in Neural Information Processing Systems 36: Annual Conference on Neu-
 ral Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December
 10 - 16, 2023, 2023. URL http://papers.nips.cc/paper_files/paper/2023/hash/
 ed3fea9033a80fea1376299fa7863f4a-Abstract-Conference.html.

Jonathan Uesato, Nate Kushman, Ramana Kumar, H. Francis Song, Noah Y. Siegel, Lisa Wang,
  Antonia Creswell, Geoffrey Irving, and Irina Higgins. Solving math word problems with process-
  and outcome-based feedback. CoRR, abs/2211.14275, 2022. doi: 10.48550/ARXIV.2211.14275.
  URL https://doi.org/10.48550/arXiv.2211.14275.

Leslie G. Valiant. A theory of the learnable. Commun. ACM, 27(11):1134–1142, 1984. doi: 10.
  1145/1968.1972. URL https://doi.org/10.1145/1968.1972.

Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez,
  Lukasz Kaiser, and Illia Polosukhin. Attention is all you need. In Isabelle Guyon, Ulrike
  von Luxburg, Samy Bengio, Hanna M. Wallach, Rob Fergus, S. V. N. Vishwanathan, and Ro-
  man Garnett, editors, Advances in Neural Information Processing Systems 30: Annual Con-
  ference on Neural Information Processing Systems 2017, December 4-9, 2017, Long Beach,
  CA, USA, pages 5998–6008, 2017. URL https://proceedings.neurips.cc/paper/2017/
  hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html.

Stephan Wäldchen, Kartikey Sharma, Berkant Turan, Max Zimmer, and Sebastian Pokutta. Inter-
  pretability guarantees with Merlin-Arthur classifiers. In Sanjoy Dasgupta, Stephan Mandt, and
  Yingzhen Li, editors, Proceedings of The 27th International Conference on Artificial Intelligence
  and Statistics, volume 238 of Proceedings of Machine Learning Research, pages 1963–1971.
  PMLR, 02–04 May 2024. URL https://proceedings.mlr.press/v238/waldchen24a.
  html.


                                                22
Boshi Wang, Xiang Yue, and Huan Sun. Can chatgpt defend its belief in truth? evaluating LLM
  reasoning via debate. In Houda Bouamor, Juan Pino, and Kalika Bali, editors, Findings of the
  Association for Computational Linguistics: EMNLP 2023, Singapore, December 6-10, 2023,
  pages 11865–11881. Association for Computational Linguistics, 2023. doi: 10.18653/V1/2023.
  FINDINGS-EMNLP.795. URL https://doi.org/10.18653/v1/2023.findings-emnlp.
  795.
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed H. Chi,
  Quoc V. Le, and Denny Zhou. Chain-of-thought prompting elicits reasoning in large language
  models. In Sanmi Koyejo, S. Mohamed, A. Agarwal, Danielle Belgrave, K. Cho, and A. Oh,
  editors, Advances in Neural Information Processing Systems 35: Annual Conference on Neural
  Information Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 -
  December 9, 2022, 2022. URL http://papers.nips.cc/paper_files/paper/2022/hash/
  9d5609613524ecf4f15af0f7b31abca4-Abstract-Conference.html.
Sean Welleck, Jiacheng Liu, Ximing Lu, Hannaneh Hajishirzi, and Yejin Choi. Natural-
  prover: Grounded mathematical proof generation with language models. In Sanmi Koyejo,
  S. Mohamed, A. Agarwal, Danielle Belgrave, K. Cho, and A. Oh, editors, Advances in
  Neural Information Processing Systems 35: Annual Conference on Neural Information Pro-
  cessing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 - Decem-
  ber 9, 2022, 2022. URL http://papers.nips.cc/paper_files/paper/2022/hash/
  1fc548a8243ad06616eee731e0572927-Abstract-Conference.html.
Fang Wu, Weihao Xuan, Ximing Lu, Zaïd Harchaoui, and Yejin Choi. The invisible leash: Why
  RLVR may not escape its origin. CoRR, abs/2507.14843, 2025a. doi: 10.48550/ARXIV.2507.
  14843. URL https://doi.org/10.48550/arXiv.2507.14843.
Jialong Wu, Shaofeng Yin, Ningya Feng, and Mingsheng Long. Rlvr-world: Training world models
   with reinforcement learning. CoRR, abs/2505.13934, 2025b. doi: 10.48550/ARXIV.2505.13934.
   URL https://doi.org/10.48550/arXiv.2505.13934.
Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing
  Yu, Saad Godil, Ryan J. Prenger, and Animashree Anandkumar.        Leandojo: Theo-
  rem proving with retrieval-augmented language models.    In Alice Oh, Tristan Nau-
  mann, Amir Globerson, Kate Saenko, Moritz Hardt, and Sergey Levine, editors, Ad-
  vances in Neural Information Processing Systems 36: Annual Conference on Neural In-
  formation Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December
  10 - 16, 2023, 2023. URL http://papers.nips.cc/paper_files/paper/2023/hash/
  4441469427094f8873d0fecb0c4e1cee-Abstract-Datasets_and_Benchmarks.html.
Mengjiao Yang, Dale Schuurmans, Pieter Abbeel, and Ofir Nachum. Chain of thought imitation with
 procedure cloning. In Sanmi Koyejo, S. Mohamed, A. Agarwal, Danielle Belgrave, K. Cho, and
 A. Oh, editors, Advances in Neural Information Processing Systems 35: Annual Conference on
 Neural Information Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November
 28 - December 9, 2022, 2022. URL http://papers.nips.cc/paper_files/paper/2022/
 hash/ebdb990471f653dffb425eff03c7c980-Abstract-Conference.html.
Jiaheng Zhang, Tianyi Liu, Weijie Wang, Yinuo Zhang, Dawn Song, Xiang Xie, and Yupeng
   Zhang. Doubly efficient interactive proofs for general arithmetic circuits with linear prover
   time. In Yongdae Kim, Jong Kim, Giovanni Vigna, and Elaine Shi, editors, CCS ’21: 2021
   ACM SIGSAC Conference on Computer and Communications Security, Virtual Event, Republic
   of Korea, November 15 - 19, 2021, pages 159–177. ACM, 2021. doi: 10.1145/3460120.3484767.
   URL https://doi.org/10.1145/3460120.3484767.
Sheng Zhang, Qianchu Liu, Guanghui Qin, Tristan Naumann, and Hoifung Poon. Med-rlvr: Emerg-
  ing medical reasoning from a 3b base model via reinforcement learning. CoRR, abs/2502.19655,
  2025. doi: 10.48550/ARXIV.2502.19655. URL https://doi.org/10.48550/arXiv.2502.
  19655.
Jiecheng Zhou, Qinghao Hu, Yuyang Jin, Zerui Wang, Peng Sun, Yuzhe Gu, Wenwei Zhang, Ming-
   shu Zhai, Xingcheng Zhang, and Weiming Zhang. Rl in the wild: Characterizing rlvr training in
   llm deployment. arXiv preprint arXiv:2509.25279, 2025.


                                              23
A     Formal Proofs

Section A.1 formally specifies the setup in which our results reside. We then prove Theorem 4.2 in
Section A.2, Theorem 4.3 in Section A.3, and Theorem 5.1 in Section A.4.

A.1    Specification of the Learning Model

In this section, we fully specify the theoretical framework in which our results reside. We define
a learner as an algorithm Λ with access to a family of autoregressive models {Pθ }θ and samples
from the input distribution x ∼ µ. In our setting of Self-Proving models (and in accordance with
the Interactive Proofs literature), we give the learner the full specification of the verifier V . More
formally,
Definition A.1 (Self-Proving model learner). A (Self-Proving model) learner is a probabilistic ora-
cle Turing Machine Λ with the following access:

        • A family of autoregressive models {Pθ }θ∈Rd where d ∈ N is the number of parameters in
          the family. For each θ and z ∈ Σ∗ , the random variable Pθ (z) is determined by the logits
          log pθ (z) ∈ R|Σ| . For any z ∈ Σ∗ and σ ∈ Σ, the learner Λ can compute the gradient of
          the σ th logit, that is, ∇θ log Prσ′ ∼pθ (z) [σ = σ ′ ]. In particular, log Prσ′ ∼pθ (z) [σ = σ ′ ] is
          always differentiable in θ.

        • Sample access to the input distribution µ. That is, Λ can sample x ∼ µ.

        • The full specification of the verifier V , i.e., the ability to emulate the verification algorithm
          V . More specifically, Λ is able to compute V ’s decision after any given interaction; that
          is, given input x, output y, and a sequence of queries and answers (qi , ai )R     i=1 , the learner
          Λ can compute the decision of V after this interaction.

A.2    Proof of Theorem 4.2

We let TVθ denote the transcript generator induced by the model Pθ when interacting with V : for
each x, TVθ (x) is the distribution over transcripts of interactions between V and Pθ on input x. We
stress that π ∗ ∼ TV∗ (x) and π ∼ TVθ (x) are transcripts produced when interacting with the same
verifier queries; we can think of the verifier as simultaneously interacting with the honest prover
and with the model Pθ .9 In what follows, we use π ∗ ∼ TV∗ (x) and π ∼ TVθ (x) to denote two
transcripts that share the same queries. That is, taking π ∗ = (y ∗ , q1∗ , a∗1 , . . . , qR
                                                                                           ∗
                                                                                             , a∗R ) to denote
                                           ∗                     ∗          ∗
an accepting transcript sampled from TV (x), and π = (y, q1 , a1 , . . . , qR , aR ) to denote a random
transcript sampled from TVθ (x), we say that π and π ∗ agree if they agree on the prover answers,
namely if:
                                      (y, a1 , . . . , aR ) = (y ∗ , a∗1 , . . . , a∗R ).

This definition implicitly uses the independence of the verifier and model’s randomness. We now
prove that TL correctly estimates the gradient of A(θ) in its update step.


Proof of Theorem 4.2. Throughout this proof, expectations and probabilities will be over the same
distributions as in the lemma statement. First, we use the law of total probability together
with the autoregressive property of Pθ (Section 4) to switch from probabilities on transcripts,
to products of next-token probabilities. Formally, consider a fixed input x, an honest transcript
π ∗ = (y ∗ , q1∗ , a∗1 , . . . , qR
                                  ∗
                                    , a∗R ), and denote a random transcript sampled from TVθ (x) when using the
same verifier queries by π = (y, q1∗ , a1 , . . . , qR      ∗
                                                              , aR ). For any r ∈ [R] denote the random variable

   9
     The way it is presented in the algorithm, first the verifier is called by TV∗ and outputs queries (q1∗ , . . . qR
                                                                                                                     ∗
                                                                                                                       ),
and then the model is prompted with the verifier queries one a time. This maintains soundness, since a proof
system is sound as long as the prover does not know the verifier’s queries in advance.


                                                             24
TVθ,<r := TVθ (yq1∗ a1 · · · ar−1 qr∗ ). Then,
                       Pr [π = π ∗ ] = Pr[(y, a1 , . . . , aR ) = (y ∗ , a∗1 , . . . , a∗R )]                              (2)
                       π               π
                                                               Y
                                     = Pr [y = y ∗ ] ·                  Pr [a = a∗r ]
                                           y∼Pθ (x)                           a∼TVθ,<r
                                                                      r∈[R]
                                                                       Y
                                       =       Pr [y = y ∗ ] ·                     Pr ∗ )
                                                                                            [σ = πs∗ ]                     (3)
                                           y∼Pθ (x)                            σ∼pθ (π<s
                                                                       r∈[R]
                                                                      s∈S(r)
                                               Y
                                       =                    αs (θ),                                                        (4)
                                           r∈[R]∪{0}
                                            s∈S(r)

where, as noted above, Equation (2) uses the independence of the verifier and model’s randomness,
Equation (3) uses the autoregressive property of Pθ (Theorem A.1), and Equation (4) is by definition
of αs and of a0 . Next, a basic calculus identity gives
                                                                         
                    ∇θ Pr [π = π ∗ ] = Pr [π = π ∗ ] · ∇θ log Pr [π = π ∗ ] .                    (5)
                              π                         π                            π

This implicitly assumes that Prπ [π = π ∗ ] is differentiable in θ; indeed, this follows from Theo-
rem A.1, where the logits of the model were assumed to by differentiable. Let us focus on the
rightmost factor. By Equation (4),
                                                   
                                              Y                              X                             X
∇θ log Pr [π = π ∗ ] = ∇θ log                                                                                         d⃗s (θ)
                                                                 
                                                            αs (θ)
                                                                  =                     ∇θ log αs (θ) =
            π                 
                                           r∈[R]∪{0}                     r∈[R]∪{0}                         r∈[R]∪{0}
                                            s∈S(r)                        s∈S(r)                            s∈S(r)
                                                                                                                           (6)

where the last equality is by definition of d⃗s (θ). Combining Equation (4) and Equation (5) gives
                                                 Y              X
                       ∇θ Pr [π = π ∗ ] =               αs (θ) ·         d⃗s (θ).
                                  π
                                                        r∈[R]∪{0}               r∈[R]∪{0}
                                                         s∈S(r)                  s∈S(r)

By the law of total probability and the linearity of the gradient,
        h                i              h              i                   
                        ∗                               ∗                     ∗
    E ∗ ∇θ Pr [π = π ] = ∇θ E ∗ Pr [π = π ] = ∇θ                     Pr
                                                                      ∗
                                                                        [π = π ] = ∇θ A(θ).
   x,π           π                            x,π       π                                x,π ,π

which concludes the proof.

A.3      Proof of Theorem 4.3

Recall the transcript generator of Pθ , denoted by TVθ (see Theorem 4.2). By the definitions of
Verifiability in Theorem 3.4 and V (x, y, q1 , . . . , aR ) in the lemma statement,
                                  ver(θ) :=      Pr
                                               x∼µ
                                                            [⟨V, Pθ ⟩ (x, y) accepts]
                                              y∼Pθ (x)

                                         =          E
                                                  x∼µ
                                                             [AccV (x, y, q1 , . . . , aR )]
                                               y∼Pθ (x)
                                              (qr ,ar )R
                                                       r=1
                                                    "                               #
                                         = E                Pr      [AccV (x, π) ]                                         (7)
                                              x∼µ       π∼TVθ (x)


Now, for every input x, let Π∗ (x) ⊂ Σ∗ denote the set of accepting transcripts:
                                   Π∗ (x) := {π ∗ ∈ Σ∗ : AccV (x, π ∗ ) = 1} .


                                                               25
We can assume that Π∗ (x) has finite cardinality, since V ’s running time is bounded and hence the
number of different transcripts that it can read (and accept) is finite. For any fixed input x, we can
express its acceptance probability by the finite sum:
                                                     X
                          Pr [AccV (x, π)] =                  Pr [π = π ∗ ].                        (8)
                         π∼TVθ (x)                                          π∼TVθ (x)
                                                              π ∗ ∈Π∗ (x)

We will use Equations (2) through (6) from the proof of Theorem 4.2. Up to a change in index
notation, these show that, for any π ∗ ,
                                                            X
                   ∇θ Pr [π = π ∗ ] = Pr [π = π ∗ ] ·             ∇θ d⃗s (θ).
                        π∼T θ (x)                     π∼T θ (x)
                                                                                  r∈R∪{0}
                                                                                   s∈[La ]


Combining Equations (7) and (8), by linearity of expectation we have that
                                                             
                                   X
            ∇θ ver(θ) = E                ∇θ Pr [π = π ∗ ]
                              x∼µ                         π∼T θ (x)
                                        π ∗ ∈Π∗ (x)
                                                                                                      
                                           X                                        X
                                                                   [π = π ∗ ] ·              ∇θ d⃗s (θ)
                                                                                                      
                          = E                           Pr
                           x∼µ                       π∼T θ (x)                                        
                                        π ∗ ∈Π∗ (x)                               r∈R∪{0}
                                                                                   s∈[La ]
                                                                                                
                                                                              X
                                                                                        ∇θ d⃗s (θ)
                                                                                                
                          = E    E AccV (x, π) ·                                                 
                           x∼µ π∼T θ (x)                                                        
                                                                            r∈R∪{0}
                                                                             s∈[La ]
                                                                                         
                                                                      X
                                                                              ∇θ d⃗s (θ)
                                                                                       
                          =         E      AccV (x, π) ·
                                x∼µ                                                    
                              π∼T θ (x)                            r∈R∪{0}
                                                                    s∈[La ]
                                                                                                          
                                                                                        X
                                                                                               ∇θ d⃗s (θ)
                                                                                                        
                          =                  AccV (x, y, q1 , . . . , aR ) ·
                                  E
                                 x∼µ                                                                    ,
                               y∼Pθ (x)                                             r∈R∪{0}
                              (qr ,ar )R
                                       r=1
                                                                                     s∈[La ]

where in the last equality, the probability is over (qr , ar ) sampled as in Algorithm 2, and it follows
from the definition of the transcript generator T θ (x).

A.4   Proof of Theorem 5.1

We first restate Theorem 5.1 in full formality.
Theorem A.2. Fix a verifier V , an input distribution µ, an autoregressive model family {Pθ }θ∈Rd ,
and a norm || · || on Rd . Fix an honest transcript generator TV∗ , and assume that the agreement
function A(θ) := Pr [π = π ∗ ] is concave in θ, where the verifier queries are the same in π ∗ and π,
and the probability is over x ∼ µ, πθ ∼ TVθ (x), and π ∗ ∼ TV∗ (x). For any ε > 0, let BNorm , BLip
and C be upper-bounds such that the following conditions hold:
       • There exists θ∗ ∈ Rd with ||θ∗ || < BNorm such that A(θ∗ ) ≥ 1 − ε/2.
       • For all θ, the logits of Pθ are BLip -Lipschitz in θ. That is, sup θ∈Rd ||∇θ log pθ (z)|| ≤ BLip .
                                                                                           z∈Σ∗

       • In the proof system defined by V , the total number of tokens (over all rounds) is at most C.
                                                                            2
Denote by θ̄ the output of TL running for N ≥ 4 · C 2 · BNorm    2     2
                                                                    · BLip  /ε iterations and learning
                           √
rate λ = BNorm /CBLip N . Then the expected Verifiability (over the randomness of the samples
                                                                ¯ ≥ 1 − ε.
collected by TL) of θ̄ is at least 1 − ε. That is, Eθ̄ [verV,µ (θ)]


                                                              26
  The proof of Theorem A.2 goes by reduction to Stochastic Gradient Descent (SGD). Theorem 4.2
  showed that the learner can use its only available tools—sampling honest transcripts, emulating the
  verifier, and differentiating the logits—to optimize the agreement A(θ). Since A(θ) lower bounds
  the Verifiability of Pθ , the former can be used as a surrogate for the latter.
  For convenience of the reader, we first provide a description of Stochastic Gradient Ascent (equiv.
  to SGD) and quote a theorem on its convergence. We adapt the presentation in Shalev-Shwartz and
  Ben-David [2014], noting that they present Stochastic Gradient Descent in its more general form
  for non-differentiable unbounded functions. The familiar reader may skip directly to the proof in
  Section A.4.3.

  A.4.1   Preliminaries on Stochastic Gradient Ascent
  Stochastic Gradient Ascent (SGA) is a fundamental technique in concave optimization. Given a
  concave function f : Rd → [0, 1], SGA starts at w0 = ⃗0 ∈ Rd and tries to maximize f (w) by taking
  a series of “steps.” Than directly differentiating f , SGA instead relies on an estimation ∇f (w): in
  each iteration, SGA takes a step in a direction that estimates ∇f (w).
  Definition A.3 (Gradient estimator). Fix a differentiable function f : Rd → R for some d. A gradient
  estimator for f is a randomized mapping Df : Rd → Rd whose expectation is the gradient of f . That
  is, for all w ∈ Rd ,
                                            E [v] = ∇f (w).
                                            v∼Df (w)

  Note that this is an equality between d-dimensional vectors.


  Algorithm 3: Stochastic Gradient Ascent
  Hyperparameters: Learning rate λ > 0 and number of iterations N ∈ N.
  Input: A function f : Rd → R to maximize and a gradient estimator Df for f .
  Output: A vector w̄ ∈ Rd .
1 Initialize w0 := ⃗  0 ∈ Rd .
2 for i = 1, . . . , N − 1 do
3      Sample vi ∼ Df (wi−1 ).
4      Update wi := wi−1 + λ · vi .
                   1
                      P
5 Output w̄ := N        i∈[N ] wi .



  Theorem 14.8 in Shalev-Shwartz and Ben-David [2014] implies the following fact.
  Fact A.4. Fix a concave f : Rd → [0, 1], a norm || · || on Rd , and upper-bounds BNorm , BLip > 0.
  Let
                                    w∗ ∈ argmax f (w),
                                                 w:||w||<BNorm

  and let w̄ denote the output of Algorithm 3 run for N iterations with learning rate
                                                        BNorm
                                                λ=         √ .
                                                       BLip N
  If at every iteration it holds that ||vi || < BLip , then
                                                              BNorm · BLip
                                     E [f (w̄)] ≥ f (w∗ ) −      √         .
                                     w̄                            N

  A.4.2   Learning with Stochastic Gradient Ascent/Descent
  Theorem A.4 captures the general case of using SGA for maximization of concave problems. It
  is more common for the literature to discuss the equivalent setting of Stochastic Gradient Descent
  (SGD) for minimization of convex problems. Specifically, a common application of SGD is for the
  task of Risk Minimization: given a loss function and access to an unknown distribution of inputs,
  the goal is to minimize the expected loss with respect to the distribution. Assuming that the loss
  function is differentiable, the gradient of the loss serves as a gradient estimator (see Theorem A.3)


                                                       27
for the risk function. We refer the reader to Shalev-Shwartz and Ben-David [2014, Section 14.5.1]
for a complete overview of SGD for risk minimization.
For the sake of completeness, we formulate Transcript Learning (TL, Algorithm 1) in the frame-
work of Risk Minimization for Supervised Learning. This is not strictly needed for the proof of
Theorem A.2, but is an illuminating connection. Although multiple loss functions may achieve our
ultimate goal—learning Self-Proving models—in what follows we define the loss that corresponds
to TL.
Fix a verifier V and let TV∗ denote a distribution over accepting transcripts. We define
                                       loss (θ, (x, π ∗ )) :=            Pr       [π ̸= π ∗ ] ,                               (9)
                                                                      π∼TVθ (x)

where π ∗ and π share the same verifier messages (as in Theorem 4.2) so the inequality is
only over the prover’s messages, namely Prπ∼TVθ (x) [π ̸= π ∗ ] = Prπ∼TVθ (x) [(y, a1 , . . . , aR ) ̸=
(y ∗ , a∗1 , . . . , a∗R )].10
The risk function is the expected value of the loss over the joint distribution of inputs and accepting
transcripts µ × TV∗ (µ):
                               Risk (θ) := x∼µE [loss (θ, (x, π ∗ ))] ,
                                                          π ∗ ∼TV∗

which means that the agreement function defined in Theorem A.2:
                                               A(θ) =        x∼µ
                                                                 Pr      [π = π ∗ ] ,
                                                           π ∼TV∗ (x)
                                                             ∗

                                                           π∼TVθ (x)

satisfies A(θ) = 1 − Risk(θ).
Thus, maximizing the agreement is equivalent to minimizing the risk. The hypothesis class over
which the optimization is performed is the ball of radius BNorm , i.e., θ ∈ Rd : ||θ|| < BNorm .
The assumption that A is concave in θ implies that the loss function is convex in θ, which is the
required assumption for using SGD for risk minimization.

A.4.3     Proof of Theorem A.2
Our strategy is to cast TL as Stochastic Gradient Ascent and apply Theorem A.4. Let ε, BNorm ,
BLip and C as in the theorem statement be given. Let θ∗ be such that A(θ∗ ) ≥ 1 − ε/2 and
||θ∗ || ≤ BNorm .
First, notice that                                          
                                                E verV,µ (θ̄) ≥ E[A(θ̄)].
                                                θ̄                       θ̄

This holds because, for any x and model Pθ , whenever the transcript generated by T θ (x) agrees
with π ∗ , then the verifier accepts (because π ∗ is honest). Therefore, to prove the theorem it suffices
to show that
                                            E[A(θ̄)] ≥ 1 − ε.
                                                     θ̄

Following the notation in Algorithm 1, in every iteration i ∈ [N ] the norm of the update step is


         Y                        X                              Y                          X
                   αs (θi ) ·               d⃗s (θi ) =                  αs (θi ) ·                 d⃗s (θi )
       r∈[R]∪{0}                r∈[R]∪{0}                  r∈[R]∪{0}                    r∈[R]∪{0}
        s∈S(r)                   s∈S(r)                     s∈S(r)                       s∈S(r)
                                                                                                           X
                                                                                                  ≤1·               d⃗s (θi ) ,
                                                                                                        r∈[R]∪{0}
                                                                                                         s∈S(r)

  10
    This loss is not to be confused with those discussed in Section 3.3. Here, we are simply explaining how
TL can be viewed as a supervised risk minimizer for the loss function defined in Equation (9).


                                                                 28
where the inequality is because αs (θi ) are probabilities, so ≤ 1. Moreover, we have
                            X                      X
                                    d⃗s (θi ) ≤             BLip ≤ C · BLip .
                              r∈[R]∪{0}          r∈[R]∪{0}
                               s∈S(r)             s∈S(r)

The first inequality is by definition of BLip as an upper-bound on the gradient of Pθ ’s logits. The
second is because, by definition, C is an upper-bound on the number of tokens sent by the prover in
the proof system, which is exactly the number of terms in the sum: r indexes rounds, and s indexes
tokens sent in each round.
To conclude, Theorem 4.2 shows that TL samples from a gradient estimator for A(θ), while the
above equation shows that the gradient is upper-bounded by C · BLip . We can therefore apply
Theorem A.4 to obtain
                    E A θ̄ ≥ A(θ∗ ) − ε/2 ≥ (1 − ε/2) − ε/2 = 1 − ε,
                           
                         θ̄

where the inequality is by definition of θ∗ . This completes the proof of Theorem A.2.

B        Full Details of the Experimental Setup
B.1       The Bézout proof system for GCD

The Euclidean algorithm for computing the Greatest Common Divisor (GCD) of two integers is
possibly the oldest algorithm still in use today [Knuth, 1969]. Its extended variant gives a simple
proof system.
Before we dive in, let us clarify what we mean by a proof system for the GCD. Prover Paul has two
integers 212 and 159; he claims that GCD(212, 159) = 53. An inefficient way for Verifier Veronica
to check Paul’s answer is by executing the Euclidean algorithm on (212, 159) and confirm that the
output is 53. In an efficient proof system, Veronica asks Paul for a short string π ∗ (describing two
integers) with which she can easily compute the answer—without having to repeat Paul’s work all
over. On the other hand, if Paul were to claim that “GCD(212, 159) = 51” (it does not), then for
any alleged proof π, Veronica would detect an error and reject Paul’s claim.
The verifier in the proof system relies on the following fact.
Fact B.1 (Bézout’s identity [Bezout, 1779]). Let x0 , x1 ∈ N and z0 , z1 ∈ Z. If z0 · x0 + z1 · x1
divides both x0 and x1 , then z0 · x0 + z1 · x1 = GCD(x0 , x1 ).

Any coefficients z0 , z1 satisfying the assumption of Theorem B.1 are known as Bézout coefficients
for (x0 , x1 ). Theorem B.1 immediately gives our simple proof system: For input x = (x0 , x1 ) and
alleged GCD y, the honest prover sends (alleged) Bézout coefficients (z0 , z1 ). The Verifier accepts
if and only if y = z0 · x0 + z1 · x1 and y divides both x0 and x1 .
In this proof system the Verifier does not need to make any query; to fit within Theorem 3.2, we
can have the verifier issue a dummy query. Furthermore, by Theorem B.1 it is complete and has
soundness error s = 0. Lastly, we note that the Verifier only needs to perform two multiplications,
an addition, and two modulus operations; in that sense, verification is more efficient than computing
the GCD in the Euclidean algorithm as required by Theorem 3.3.

Annotations. To describe how a proof z = (z0 , z1 ) is annotated, let us first note how it can be
computed. The Bézout coefficients can be found by an extension of the Euclidean algorithm. It is
described in Algorithm 4.11
Referring to Algorithm 4, the annotation of a proof z = (z0 , z1 ) will consist of intermediate steps
in its computation. Suppose that in each iteration of the While-loop, the algorithm stores each of r0 ,
s0 and q in an arrays r⃗0 , s⃗0 and ⃗q. The annotation z̃ of z is obtained by concatenating each of these
arrays. In practice, to avoid the transformer block (context) size from growing too large, we fix a
cutoff T and first trim each array to its first T elements.
    11
         Our description follows https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm.


                                                   29
  Algorithm 4: Extended Euclidean algorithm
  Input: Nonzero integers x0 , x1 ∈ N.
  Output: Integers (y, z0 , z1 ), such that y = GCD(x0 , x1 ) and (z0 , z1 ) are Bézout coefficients
             for (x0 , x1 ).
1 Initialize r0 = x0 , r1 = x1 , s0 = 1, s1 = 0, and q = 0.
2 while r1 ̸= 0 do
3      Update q := ⌊r0 /r1 ⌋.
4      Update (r0 , r1 ) := (r1 , r0 − q × r1 ).
5      Update (s0 , s1 ) := (s1 , s0 − q × s1 ).
6 Output GCD y = r0 and Bézout coefficients z0 := s0 and z1 := (r0 − s0 · x0 )/x1 .




  We formalize this in the terminology of Section 6 by defining a Transcript Annotator and Answer
  Extractor. Note that, since our proof system consists only of one “answer” z send from the prover
  to the verifier, the entire transcript π is simply z = (z0 , z1 ). Since the verification is deterministic,
  this means that the proof system is of an NP type (however, note that the search problem of finding
  the “NP-witness” z = (z0 , z1 ) is in fact in P).

         • Transcript Annotator A: For a fixed cutoff T and given input x = (x0 , x1 ) and transcript
           z = (z0 , z1 ), A executes Algorithm 4 on input x = (x0 , x1 ). During the execution, A
           stores the first T intermediate values of r0 , s0 and q in arrays r⃗0 , s⃗0 and ⃗q. It outputs
           A(x, z) := (r⃗0 , s⃗0 , ⃗q, z).
         • Answer Extractor E: Given an annotated transcript z̃ = (r⃗0 , s⃗0 , ⃗q, z), outputs E(z̃) := z.

  We note that the computational complexity of A is roughly that of the honest prover, i.e., Algorithm 4
  (up to additional space due to storing intermediate values). As for E, it can be implemented in
  logarithmic space and linear running time in |z̃|, i.e., the length of the description.12

  B.2    Implementation details

  Code, data and models are available at https://github.com/orrp/self-proving-models.

  Model architecture. We use Karpathy’s nanoGPT 13 implementation of GPT. Note that we train
  the model “from scratch” only on sequences related to the GCD problem, rather than starting from
  a pretrained checkpoint. We use a 6.3M parameter architecture of 8 layers, 8 attention heads, and
  256 embedding dimensions. We optimized hyperparameters via a random hyperparameter search,
  arriving at learning rate 0.0007, AdamW β1 = 0.733 and β2 = 0.95, 10% learning rate decay factor,
  no dropout, gradient clipping at 2.0, no warmup iterations, and 10% weight decay.

  Data. We sample integers from the log10 -uniform distribution over {1, . . . , 104 }. Models in Ta-
  ble 2 and Fig. 3 are trained for 100K iterations on a dataset of ≈10M samples. For Figure 5 (base
  ablation) we train for 20K iterations on a dataset of ≈1M samples; this is because this setting re-
  quired 68 many runs in total, whereas the annotation-cutoff ablation required 18 longer runs.

  Compute. All experiments were run on a machine with an NVIDIA A10G GPU, 64GB of RAM,
  and 32 CPU cores. The longest experiment was the single RLVF run, which took one month and
  four days. The annotation-cutoff ablation runs took about 75 minutes each. Base of representation
  ablation runs were shorter at about 15 minutes each. The total running time of the Transcript Learn-
  ing experiments was approximately 40 hours (excluding time dedicated to a random hyperparameter
  search), and the RLVF experiment took another month and four days. The overall disk space needed
  for our models and data is 4GB.

  Representing integers. We fully describe how integer sequences are encoded. As a running ex-
  ample, we will use base 210. To encode a sequence of integers, each integer is encoded in base 210,
    12
        That is, if integers are represented by n-bits, then E has space complexity O(log n + log T ) and running
  time O(n · T ).
     13
        https://github.com/karpathy/nanoGPT.


                                                        30
a sign is prepended and a delimiter is appended, with a unique delimiter identifying each component
of the sequence. For example, consider the input integers x0 = 212 (which is 12 in base 210) and
x1 = 159. Their GCD is y = 53, with Bézout coefficients z0 = 1 and z1 = −1. Therefore, the
sequence (212, 159, 53, 1, −1) is encoded as

                         +,1,2,x0,+,159,x1,+,53,y,+,1,z0,-,1,z1

where commas are added to distinguish between different tokens. Null tokens are appended to pad
all sequences in a dataset to the same length. Both the input and the padding components are ignored
when computing the loss and updating parameters.

Annotations Annotations are encoded as above, with each component in an intermediate step πt
delimited by a unique token. Since different integer pairs may require a different number of inter-
mediate steps to compute the Bézout coefficients, we chose to pad all annotations to the same length
T by the last step πT in the sequence (which consists of the final Bézout coefficients). This ensures
that the final component output by the model in each sequence should be the Bézout coefficient,
and allows us to batch model testing (generation and evaluation) resulting in a 1000x speed-up over
sequential testing.
As an example, consider the inputs x0 = 46 and x1 = 39. Tracing through the execution of
Algorithm 4, we have
                             x0 x1 y s⃗0 r⃗0 ⃗q      z0   z1
                             46 39        1 46 1
                                          0 39 5
                                          1   7 1
                                         −5 4 1
                                          6   3 3
                                      1             −11 13

To encode this as an annotated transcript for the transformer, we must specify a base of represen-
tation and an annotation cutoff. Suppose that we wish to encode this instance in base B = 10 and
cutoff T = 3. Then the input with the annotated transcript is encoded as

                                  +,4,6,x0,+,3,9,x1,+,1,y,
                                 +,1,z0’,+,4,6,z1’,+,1,q’,
                                 +,0,z0”,+,3,9,z1”,+,5,q”,
                                 +,1,z0”’,+,7,z1”’,+,1,q”’,
                                     -,1,1,z0,+,1,3,z1

where commas are used to separate between tokens, and linebreaks are added only for clarity. No-
tice the three types of tokens: signs, digits, and delimiters. Notice also that the output y is added
immediately after the input, followed by the annotated transcript (whose six tokens comprise the
proof itself). Since the Self-Proving model we train has causal attention masking, placing the output
y before the proof means that the model “commits” to an output and only then proves it.




                                                 31
