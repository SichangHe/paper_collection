                                                        Incompleteness of AI Safety Verification via Kolmogorov Complexity, 2026, 1–17


                                                                                                                              Original article




                                        Incompleteness of AI Safety Verification via
arXiv:2604.04876v1 [cs.AI] 6 Apr 2026




                                        Kolmogorov Complexity
                                        Munawar Hasan 1,∗

                                        1 Mechanical and Aerospace Engineering, Michigan Technological University, Houghton, MI, USA


                                        ∗ Address for correspondence. Munawar Hasan, MTU, Houghton, MI, 49931, USA. munawarh@mtu.edu




                                        Abstract

                                        Ensuring that artificial intelligence (AI) systems satisfy formal safety and policy constraints is a central challenge

                                        in safety-critical domains. While limitations of verification are often attributed to combinatorial complexity and

                                        model expressiveness, we show that they arise from intrinsic information-theoretic limits. We formalize policy

                                        compliance as a verification problem over encoded system behaviors and analyze it using Kolmogorov complexity.

                                        We prove an incompleteness result: for any fixed sound computably enumerable verifier, there exists a threshold

                                        beyond which true policy-compliant instances cannot be certified once their complexity exceeds that threshold.

                                        Consequently, no finite formal verifier can certify all policy-compliant instances of arbitrarily high complexity.

                                        This reveals a fundamental limitation of AI safety verification independent of computational resources, and

                                        motivates proof-carrying approaches that provide instance-level correctness guarantees.

                                        Key words: Kolmogorov Complexity, AI Safety Verification, Incompleteness, Verifiable AI



                                        1. Introduction

                                        A central challenge in modern artificial intelligence (AI) is guaranteeing that

                                        autonomous and intelligent systems behave in accordance with prescribed safety


                                        © Munawar Hasan 2026. All rights reserved. For permissions, please e-mail: munawarh@mtu.edu                          1
2                                                                            Munawar Hasan

and policy constraints. In safety-critical domains such as autonomous driving, multi-

agent perception, and secure decision-making, systems’ outputs must satisfy formally

specified properties, including collision avoidance, cross-modal consistency, and

adherence to regulatory or operational constraints. These requirements naturally

give rise to a fundamental verification problem: given an input-output pair and a

policy specification, can one certify that the system’s behavior is compliant?

    Existing approaches to AI safety and verification largely rely on empirical

validation, statistical testing, and formal checking of specific properties. While these

methods have achieved significant progress, their limitations are typically attributed

to practical factors such as combinatorial explosion of environments, continuous

state spaces, and the complexity of learned models. In this work, we argue that such

limitations are not merely practical, but fundamental.

    Recent work has established information-theoretic limitations in AI security

and alignment (Vassilev, 2025), drawing connections to incompleteness phenomena

rooted in Gödel’s theorem (Gödel, 1931) and its information-theoretic formulation

due to Chaitin (Chaitin, 1974). These perspectives suggest that complete safety

guarantees may be inherently unattainable in complex systems. In this work, we

provide a formal Kolmogorov complexity-based characterization of these limitations

in the setting of policy verification, together with concrete implications for the design

of verifiable AI systems.

    We adopt a formal perspective in which AI behavior is encoded as finite binary

strings and policy compliance is expressed as a predicate over these encodings, so

that verification corresponds to proving that a given instance satisfies the policy. We

analyze the limits of such verification through the lens of Kolmogorov complexity (Li
Limits of AI Safety Verification                                                        3

et al., 2008), which provides a canonical measure of the information content of an

individual instance.

     Our main result establishes an information-theoretic incompleteness result for AI

policy verification: for any fixed sound computably enumerable verification system,

there exists a threshold beyond which true policy-compliant instances cannot be

certified once their Kolmogorov complexity exceeds that threshold. Consequently,

no finite formal verifier can capture all policy-compliant instances of arbitrarily high

complexity, revealing an intrinsic limitation of verification that is independent of

computational resources.

     This limitation has important implications for the design of trustworthy

AI systems. In particular, it suggests that universally complete verification is

unattainable and motivates a shift toward alternative paradigms in which correctness

is established through structured, instance-specific evidence rather than exhaustive

characterization of all valid behaviors. This perspective aligns with emerging designs

in verifiable AI and secure perception systems, such as the Hermes framework (Hasan

et al., 2026), where correctness is established through instance-level constraints and

verifiable artifacts in the form of succinct proofs rather than global detection. In such

systems, participants provide structured outputs that satisfy formal constraints, and

correctness is validated through explicit verification procedures.

     More broadly, this shift reflects a change in how correctness is established in

complex AI systems: from attempting to characterize all valid behaviors, to verifying

the validity of individual instances. This distinction becomes especially important in

settings where the space of possible inputs and behaviors is large and highly variable,

rendering exhaustive verification infeasible. Our incompleteness result provides a

theoretical foundation for this design philosophy, showing that no fixed verifier can
4                                                                         Munawar Hasan

certify all valid behaviors and motivating a reliance on per-instance verifiability

rather than global completeness.

Contributions.

•   We formalize AI policy compliance as a verification problem over encoded system

    behaviors of the form x = ⟨z, y, Π⟩.

•   We establish an information-theoretic incompleteness result via Kolmogorov

    complexity, showing that no fixed formal verifier can certify all policy-compliant

    instances of sufficiently high complexity.

•   We connect these theoretical limits to the design of verifiable AI systems,

    providing a principled justification for proof-carrying and certificate-based

    approaches to instance-level verification.

    Our result does not assume incompleteness, but derives it from fundamental

information-theoretic limits. The existence of arbitrarily high-complexity instances,

together with the finite descriptive capacity of any computable verifier, implies that

some true policy-compliant instances cannot be certified within a fixed system.

This limitation arises at the level of universal verification rather than instance-

level certification, and motivates a shift toward proof-carrying approaches in which

correctness is established through instance-specific certificates.


2. Related Work

Incompleteness and algorithmic information theory. Our work is rooted

in classical results on the limits of formal reasoning, most notably Gödel’s

incompleteness theorems (Gödel, 1931) and their information-theoretic formulations

via Kolmogorov complexity. Chaitin (Chaitin, 1974) showed that any sufficiently

strong formal system cannot prove statements asserting that the Kolmogorov
Limits of AI Safety Verification                                                       5

complexity of a string exceeds a given threshold. This perspective establishes a

fundamental connection between provability and information content, which we

adopt in the context of AI policy verification.

     Kolmogorov complexity in learning and generalization. Kolmogorov

complexity has long been studied as a theoretical foundation for learning and model

selection, including the Minimum Description Length (MDL) (Grünwald, 2007)

principle. Prior work has used description length to characterize generalization,

compression, and inductive bias in machine learning. In contrast, our focus is not on

learning performance, but on the limits of verifying properties of individual instances.

We use Kolmogorov complexity as a measure of instance-level information content

to establish limits of formal verification.

     Formal verification of AI systems. A growing body of work studies

formal verification (Katz et al., 2017; Huang et al., 2017) of neural networks

and autonomous systems, including reachability analysis, constraint solving, and

robustness certification. These approaches aim to provide guarantees about system

behavior under specified conditions, and are typically evaluated in terms of

scalability and coverage (Cohen et al., 2019). Our work complements this line of

research by identifying a fundamental limitation: even in principle, no fixed formal

verifier can certify all policy-compliant instances once their Kolmogorov complexity

exceeds a threshold.

     AI safety and policy compliance. Recent work in AI safety has explored

methods for ensuring that system outputs satisfy policy constraints, including rule-

based filtering, constrained optimization, and post-hoc verification (Amodei et al.,

2016; Gehr et al., 2018). These approaches often assume that policy-compliant

behavior can be characterized or approximated within a sufficiently expressive
6                                                                            Munawar Hasan

system. Our results challenge this assumption by showing that complete certification

of policy compliance is impossible for any fixed formal verifier, independent of

computational resources.

    Verifiable computation and proof systems. There has been significant

progress in cryptographic proof systems,           including verifiable computation

frameworks (Gennaro et al., 2010) and succinct zero-knowledge proofs such as

zk-SNARKs (Groth, 2016) and related systems (Ben-Sasson et al., 2018), which

enable efficient verification of complex computations. These techniques provide

a mechanism for certifying correctness via explicit proofs rather than exhaustive

validation. Our work provides a theoretical justification for such approaches: since

universal verification is fundamentally incomplete, proof-carrying paradigms offer a

principled alternative by shifting verification to instance-specific certificates.

    These approaches address computational and algorithmic aspects of verification,

whereas our result identifies a fundamental information-theoretic limitation. We

provide an information-theoretic incompleteness result for AI policy verification,

showing that these limitations are not merely practical, but arise from intrinsic

bounds on information and provability.




3. Preliminaries and Problem Formulation

3.1. Kolmogorov Complexity

Kolmogorov complexity provides a measure of the information content of an

individual object. Let U be a fixed universal prefix-free Turing machine. The prefix

Kolmogorov complexity of a string x ∈ {0, 1}∗ is defined as


                             K(x) := min{ |q| : U (q) = x }.
Limits of AI Safety Verification                                                    7

3.2. Policy-Compliance Model

We model an AI interaction as a finite binary encoding


                                        x = ⟨z, y, Π⟩,


where:

•   z is the input (e.g., scene, observation),

•   y is the system output (e.g., action, prediction),

•   Π is a formal policy specification, such as collision avoidance constraints,

    minimum stopping distance requirements, or consistency conditions over system

    outputs.

     This encoding represents a single AI interaction instance, capturing the input,

the system’s output, and the governing policy in a unified binary form. This allows

us to treat policy compliance as a property of a single encoded instance.




Definition 1 (Policy-compliance) Define the predicate P : {0, 1}∗ → {0, 1} by


                     P (x) = 1 ⇐⇒ output y satisfies policy Π on input z.


3.3. Proof System

We model verification as the ability of a formal system to certify policy compliance,

i.e., to prove statements of the form P (x).
8                                                                         Munawar Hasan

Definition 2 (Formal verifier) Let T be a sound computably enumerable formal

theory. A proof checker


                              CT (φ, π) : {0, 1}∗ × {0, 1}∗ → {0, 1}


returns 1 if π is a valid proof of φ in T , and 0 otherwise.


     This definition models verification as provability within a formal system. In our

setting, we are interested in statements of the form φ = P (x), where x = ⟨z, y, Π⟩

encodes an AI interaction, and verification corresponds to the existence of a proof

π such that CT (P (x), π) = 1.


4. Kolmogorov Complexity Limits of Policy Verification

We now analyze the limits of policy verification through the lens of Kolmogorov

complexity. Our approach proceeds in two steps: first, we show that policy-compliant

instances can have arbitrarily high complexity under a mild richness assumption;

second, we establish that such instances cannot all be certified by any fixed formal

verifier.

4.1. High-Complexity Policy-Compliant Instances

Assumption 1 (Richness) There exists a constant d such that for infinitely many

m,

                              |{x ∈ {0, 1}m : P (x) = 1}| ≥ 2m−d .


     This assumption captures the fact that policy-compliant behaviors are not

confined to a small, highly structured subset of the space. In practical systems, many

distinct configurations satisfy safety constraints, leading to a large and diverse set
Limits of AI Safety Verification                                                       9

of valid instances. Importantly, the richness assumption does not require the policy

Π itself to be complex; rather, it reflects variability in inputs z and outputs y, which

can give rise to a vast number of distinct compliant instances. Even simple policies

may therefore admit many instances with high Kolmogorov complexity.

     This assumption is mild and holds in settings where the space of valid system

behaviors is large, such as perception-driven or environment-dependent systems,

where diverse inputs can yield many distinct policy-compliant outputs.


Lemma 1 (High-complexity compliant instances) Under Assumption 1, for

infinitely many m, there exists x such that


                                   P (x) = 1 and K(x) ≥ m − d.



Proof Among strings of length m, fewer than 2m−d have Kolmogorov complexity less

than m − d. Since at least 2m−d satisfy P (x) = 1, one must satisfy K(x) ≥ m − d.

□

4.2. Incompleteness of Policy Verification

We now show that no fixed formal verifier can certify all such high-complexity policy-

compliant instances.


Theorem 1 (Incompleteness of policy verification) Let T be a sound computably

enumerable formal theory sufficiently expressive to represent statements involving

P (x) and K(x) > n. Then there exists a constant cT such that for all sufficiently

large n, no statement of the form


                                             P (x) ∧ K(x) > n
10                                                                         Munawar Hasan

is provable in T .




Proof sketch Assume that for arbitrarily large n, there exists a string x such that T

proves P (x) ∧ K(x) > n. One can construct a program that enumerates proofs in T

and outputs the corresponding x, yielding a description of x of size cT + O(log n).

This implies K(x) ≤ cT + O(log n), contradicting the assumption that K(x) > n for

sufficiently large n. A full proof is provided in Appendix A.4.    □



     This result separates truth from provability in the context of AI policy

compliance, showing that some valid behaviors cannot be certified within any fixed

formal system.


Corollary 1 (Limit of complete policy verification) No fixed sound computably

enumerable formal verifier (i.e., theory T ) can certify all true policy-compliant

instances whose Kolmogorov complexity exceeds any fixed bound.


5. Implications for Verifiable AI

Theorem 1 reveals a fundamental limitation of verification-based AI safety: no fixed

formal system can certify all valid behaviors of arbitrarily high complexity once their

descriptive complexity exceeds a threshold.

     This highlights a key distinction between detection-based and proof-based

approaches. Detection-based systems attempt to characterize all valid behaviors

through global rules, whereas proof-based systems require each instance to provide

its own certificate of correctness.
Limits of AI Safety Verification                                                      11

     Consider an augmented representation


                                   x = ⟨z, y, Π, π⟩,


where π is a proof that P (x) = 1. Verification reduces to checking π, which can be

done efficiently using modern succinct proof systems. This paradigm shift avoids the

need for universal characterization and instead ensures correctness on a per-instance

basis. It provides a principled foundation for building trustworthy AI systems in

safety-critical settings.




6. Adaptation to Autonomous Systems

Consider an autonomous system where z encodes the environment (objects,

velocities, sensor inputs, etc.) and y represents a decision such as a control action or

trajectory. Let Π encode safety constraints such as collision avoidance or minimum

stopping distance. The predicate P (x) then determines whether the decision y is

safe in context z.

     In modern autonomous systems, decision-making may be implemented using

learned models, including neural network-based policies, or hybrid architectures

combining learning and structured components. Verification is therefore applied

either directly to model outputs or through auxiliary mechanisms such as safety

filters, reachability analysis, or constraint-checking procedures. While these

approaches differ in implementation, they share a common objective: to certify that

system behavior satisfies predefined safety constraints.

     Theorem 1 shows that these limitations are not merely computational, but

fundamental. Even in idealized settings, there exist safe configurations whose
12                                                                                     Munawar Hasan

                                                            Proof Generator   Verify Proof
                                                                                               Accept
                                                                  (π)              (π)



 Input z        AI Model           Output y ch
                                                   eck
                                                       P   (x
                                                                )


                                                            Verifier T


                                        Not Certified (Reject / Unknown)


Fig. 1: Verification Paradigm: A fixed verifier T may fail to certify policy-compliant
instances due to fundamental incompleteness, while proof-carrying approaches
attach an instance-specific proof π enabling verifiable acceptance.



correctness cannot be certified by any fixed formal verifier due to their intrinsic

informational complexity.

     Figure 1 illustrates this limitation, highlighting the gap between validity and

certifiability and motivating proof-carrying approaches.


6.1. Connection to Verifiable Perception Systems

The incompleteness result in Theorem 1 suggests a shift in how safety-critical

systems should be designed. Rather than attempting to construct globally complete

verification mechanisms, systems can instead rely on instance-level certification,

where correctness is established through structured, verifiable evidence attached

to each output.

     This perspective is reflected in emerging designs for verifiable perception

and decision-making systems. For example, in multi-vendor perception fusion,

contributors provide structured outputs that are validated under shared constraints,
Limits of AI Safety Verification                                                      13

while proof-based communication frameworks enable participants to attach succinct

cryptographic proofs certifying compliance with safety policies.

     These approaches align with the principle that, since no fixed verifier can certify

all valid behaviors of arbitrarily high complexity, correctness must be established on

a per-instance basis. In this setting, verification becomes the validation of explicit

certificates rather than exhaustive characterization of all possible behaviors.




7. Conclusion

We established an information-theoretic incompleteness result for AI policy

verification, showing that no fixed formal verifier can certify all policy-compliant

instances beyond a complexity threshold. This limitation motivates a shift toward

proof-based verification paradigms, providing a principled and mathematically

grounded direction for the design of verifiable and trustworthy AI systems.




Acknowledgments

The author thanks Apostol Vassilev for his work (Vassilev, 2025) on information-

theoretic limitations in AI security and alignment, which served as a key inspiration

for this work.




A. Appendix: Incompleteness of Policy Verification

This appendix provides a self-contained proof of Theorem 1 using standard

arguments from Kolmogorov complexity. For completeness, we briefly restate the

necessary definitions.
14                                                                      Munawar Hasan

A.1. Preliminaries

Let U be a universal prefix-free Turing machine. The prefix Kolmogorov complexity

of a string x is

                                 K(x) := min{ |q| : U (q) = x }.


     A formal theory T is said to be sound if every statement provable in T is true,

and computably enumerable if the set of its proofs can be effectively enumerated.

A.2. Counting Bound

Lemma 2 (Counting bound) For any integer n, the number of strings x satisfying

K(x) < n is less than 2n .




Proof There are at most 2n − 1 binary programs of length strictly less than n. Since

U is prefix-free, the set of valid programs forms a prefix-free code, and thus there

are at most 2n − 1 programs of length less than n.          □

A.3. High-Complexity Instances

Lemma 3 (Existence of incompressible strings) For every n, there exists a string x

such that K(x) ≥ n.




Proof There are 2n binary strings of length n, while fewer than 2n strings can have

complexity less than n by Lemma 2. Hence at least one string must satisfy K(x) ≥ n.

□

A.4. Proof of Theorem 1

We restate the theorem:
Limits of AI Safety Verification                                                 15

Theorem 2 (Restatement of Theorem 1) For any sound computably enumerable

theory T sufficiently expressive to represent statements involving both P (x) and

K(x) > n, there exists a constant cT such that for all sufficiently large n, no

statement of the form

                                   P (x) ∧ K(x) > n


is provable in T .




Proof Assume for contradiction that for infinitely many n, there exists a string x

such that T proves

                                   P (x) ∧ K(x) > n.


     Since T is computably enumerable, we can construct a program AT,n that

operates as follows:

1. Enumerate all candidate proofs in T .

2. For each proof π, check whether it proves a statement of the form P (x)∧K(x) > n

    for some explicitly represented string x.

3. Extract x from the statement and output it.

     Because T is assumed to prove such a statement, the program AT,n eventually

halts and outputs a corresponding x.

     The description length of AT,n consists of:

•   a fixed proof enumeration procedure,

•   a fixed description of the theory T ,

•   an encoding of the integer n, which requires O(log n) bits.
16                                                                                           Munawar Hasan

       Thus there exists a constant cT such that


                                         K(x) ≤ cT + O(log n).


       On the other hand, since T is sound and proves K(x) > n, the statement is true,

and hence

                                                   K(x) > n.


       Combining the inequalities yields


                                      n < K(x) ≤ cT + O(log n),


which is impossible for sufficiently large n since cT + O(log n) < n eventually.

       Therefore, for sufficiently large n, no statement of the form


                                            P (x) ∧ K(x) > n


can be proved in T .           □

A.5. Remark

The proof shows that the limitation arises from a mismatch between the descriptive

capacity of the formal system T and the information content of individual instances.

This argument is independent of computational constraints and applies to any sound

computably enumerable verification system.


References

D. Amodei, C. Olah, J. Steinhardt, P. Christiano, J. Schulman, and D. Mané. Concrete Problems in AI Safety,

     2016. URL https://arxiv.org/abs/1606.06565.
Limits of AI Safety Verification                                                                            17

E. Ben-Sasson et al. Scalable, transparent, and post-quantum secure computational integrity. IACR ePrint, 2018.

G. J. Chaitin. Information-Theoretic Limitations of Formal Systems. Journal of the ACM (JACM), 21(3):403–424,

  1974.

J. M. Cohen, E. Rosenfeld, and J. Z. Kolter. Certified Adversarial Robustness via Randomized Smoothing, 2019.

  URL https://arxiv.org/abs/1902.02918.

T. Gehr, M. Mirman, D. Drachsler-Cohen, P. Tsankov, S. Chaudhuri, and M. Vechev. AI2: Safety and Robustness

  Certification of Neural Networks with Abstract Interpretation. In 2018 IEEE Symposium on Security and

  Privacy (SP), pages 3–18, 2018. doi: 10.1109/SP.2018.00058.

R. Gennaro, C. Gentry, and B. Parno. Non-interactive verifiable computing: Outsourcing computation to untrusted

  workers. In T. Rabin, editor, Advances in Cryptology – CRYPTO 2010, pages 465–482, Berlin, Heidelberg,

  2010. Springer Berlin Heidelberg. ISBN 978-3-642-14623-7.

K. Gödel.   On formally undecidable propositions of principia mathematica and related systems i 1 (1931).

  Monatshefte für Mathematik und Physik, 38:173–198, 1931.

J. Groth. On the Size of Pairing-based Non-interactive Arguments. In EUROCRYPT, 2016.

P. D. Grünwald. The Minimum Description Length Principle. MIT press, 2007.

M. Hasan, A. Vassilev, E. Griffor, and T. Gamage. Hermes Seal: Zero-Knowledge Assurance for Autonomous

  Vehicle Communications, 2026. URL https://arxiv.org/abs/2603.26343.

X. Huang, M. Kwiatkowska, S. Wang, and M. Wu. Safety Verification of Deep Neural Networks, 2017. URL

  https://arxiv.org/abs/1610.06940.

G. Katz, C. Barrett, D. Dill, K. Julian, and M. Kochenderfer. Reluplex: An Efficient SMT Solver for Verifying

  Deep Neural Networks, 2017. URL https://arxiv.org/abs/1702.01135.

M. Li, P. Vitányi, et al. An Introduction to Kolmogorov Complexity and Its Applications, volume 3. Springer,

  2008.

A. Vassilev. Robust AI Security and Alignment: A Sisyphean Endeavor?, 2025. URL https://arxiv.org/abs/2512.

  10100.
