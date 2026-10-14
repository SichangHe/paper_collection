                                         A Hybrid Approach to Formal Verification of Higher-Order
                                         Masked Arithmetic Programs

                                         PENGFEI GAO∗† , ShanghaiTech University, China
arXiv:2006.09171v1 [cs.CR] 16 Jun 2020




                                         HONGYI XIE, ShanghaiTech University, China
                                         FU SONG, ShanghaiTech University, China
                                         TAOLUE CHEN, Birkbeck, University of London, UK
                                         Side-channel attacks, which are capable of breaking secrecy via side-channel information, pose a growing
                                         threat to the implementation of cryptographic algorithms. Masking is an effective countermeasure against
                                         side-channel attacks by removing the statistical dependence between secrecy and power consumption via
                                         randomization. However, designing efficient and effective masked implementations turns out to be an error-
                                         prone task. Current techniques for verifying whether masked programs are secure are limited in their
                                         applicability and accuracy, especially when they are applied. To bridge this gap, in this article, we first propose
                                         a sound type system, equipped with an efficient type inference algorithm, for verifying masked arithmetic
                                         programs against higher-order attacks. We then give novel model-counting based and pattern-matching based
                                         methods which are able to precisely determine whether the potential leaky observable sets detected by the type
                                         system are genuine or simply spurious. We evaluate our approach on various implementations of arithmetic
                                         cryptographic programs. The experiments confirm that our approach outperforms the state-of-the-art baselines
                                         in terms of applicability, accuracy and efficiency.
                                         CCS Concepts: • Software and its engineering → Software verification; • Security and privacy →
                                         Logic and verification; Side-channel analysis and countermeasures.
                                         Additional Key Words and Phrases: Formal verification, higher-order masking, cryptographic programs,
                                         side-channel attacks
                                         ACM Reference Format:
                                         Pengfei Gao, Hongyi Xie, Fu Song, and Taolue Chen. 2020. A Hybrid Approach to Formal Verification of
                                         Higher-Order Masked Arithmetic Programs. ACM Trans. Softw. Eng. Methodol. 37, 4, Article 111 (August 2020),
                                         38 pages. https://doi.org/10.1145/1122445.1122456

                                         1    INTRODUCTION
                                         Side-channel attacks are capable of breaking secrecy via side-channel information such as power
                                         consumption [74, 79], execution time [108], faults [70, 102], acoustic [57] and cache [65], posing a
                                         growing threat to implementations of cryptographic algorithms. In this work, we focus on power
                                         ∗ Also with University of Chinese Academy of Sciences.
                                         † Also with Shanghai Institute of Microsystem and Information Technology.


                                         Authors’ addresses: Pengfei Gao, gaopf@shanghaitech.edu.cn, ShanghaiTech University, Shanghai, China, 201210; Hongyi
                                         Xie, xiehy@shanghaitech.edu.cn, ShanghaiTech University, Shanghai, China, 201210; Fu Song, ShanghaiTech University,
                                         Shanghai, China, 201210, songfu@shanghaitech.edu.cn; Taolue Chen, Birkbeck, University of London, London, UK, taolue@
                                         dcs.bbk.ac.uk.

                                         Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee
                                         provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and          111
                                         the full citation on the first page. Copyrights for components of this work owned by others than ACM must be honored.
                                         Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires
                                         prior specific permission and/or a fee. Request permissions from permissions@acm.org.
                                         © 2020 Association for Computing Machinery.
                                         1049-331X/2020/8-ART111 $15.00
                                         https://doi.org/10.1145/1122445.1122456


                                                                      ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
111:2                                                                                             Gao et al.


side-channel attacks, arguably the most effective physical side-channel attack [69], where power
consumption data are used as the side-channel information.
    To thwart power side-channel attacks, masking is one of the most widely-used and effective
countermeasures [31, 69]. Essentially, masking is designed to remove the statistical dependence
between secrecy and power consumption via randomization. Fix a sound security parameter d,
an order-d masking typically makes use of a secret-sharing scheme to logically split the secret
data into (d + 1) shares such that any d ′ ≤ d shares are statistically independent on the secret data.
Masked implementations of some specific cryptographic algorithms such as PRESENT, AES and
its non-linear component (Sbox) (e.g., [69, 83, 94, 96, 98]), as well as secure conversion algorithms
between Boolean and arithmetic maskings (e.g., [19, 38, 42, 59, 68]), have been published over
years. It is crucial to realize that an implementation that is based on a secure scheme does not
provide the secure guarantee in practice automatically. For instance, the order-d masking of AES
proposed in [96] and its extensions [30, 71] were later shown to be vulnerable to an attack of order-
(⌈ d2 ⌉ + 1) [44]. Indeed, designing efficient and effective masked implementations is an error-prone
process. Therefore, it is vital to verify masked programs in addition to the underlying security
scheme, which should ideally be done automatically.
    The predominant approach addressing this problem is the empirical leakage assessment by
statistical significance tests or launching state-of-the-art side-channel attacks, e.g., [4, 58, 99] to
cite a few. Although these approaches are able to identify some flaws, they can neither prove their
absence nor identify all possible flaws exhaustively. In other words, even if no flaw is detected, it is
still inconclusive, as it is entirely possible that the implementation could be broken with a better
measurement setup or more leakage traces. Recently, approaches based on formal verification are
emerging for automatically verifying masked programs [6–8, 22, 23, 25, 39, 50, 51, 55, 88, 110]. As the
state of the art, most of these methods can only tackle Boolean programs [8, 18, 22, 23, 25, 50, 51, 110]
or first-order security [55, 88, 89], thus are limited in applicability and usability. Some work [6, 7, 39]
is able to verify arithmetic programs against higher-order attacks, but is limited in accuracy in the
sense that secure programs may fail to pass the verification whereas potential leaky observable
sets are hard to be resolved automatically so tedious manual examination is usually necessary
to differentiate genuine and spurious ones. Therefore, formal verification of masked arithmetic
programs against higher-order attacks (with full tool support to automatically resolve potential
leaky observable sets) is still an unsolved question and requires further research.

Main contributions. Our work focuses on formal verification of higher-order masked arithmetic
programs based on the standard probing model (ISW model) proposed by Ishai, Sahai and Wag-
ner [69]. Arithmetic programs admit considerably richer operations such as finite-field multiplica-
tion, and are much more challenging than their Boolean counterparts whose variables are over
the Boolean domain only. Transforming arithmetic programs to equivalent Boolean ones and
then applying existing tools is theoretically possible, but suffers from several disadvantages: (1)
complicated arithmetic operations (e.g., finite-field multiplication) have to be encoded as bitwise
operations; (2) verifying order-d security of a 8-bit arithmetic program must be done by verifying
order-(8d ) security over its Boolean translation which has considerably more observable variables
(at least 8×). Because of this, we hypothesize that this approach is practically unfavourable, if not
infeasible. Indeed, the state-of-the-art tool maskVerif [8] has already required over 18 minutes
to accomplish verification of the fifth-order masked Boolean implementation of DOM Keccak
Sbox [64] which has only 618 observable variables.
   In light of this, we pursue a direct verification approach for higher-order masked arithmetic
programs. To guarantee that a masked program is order-d secure, one has to ensure that the joint
distributions of all size-d sets of observable variables (observable sets) that are potentially exposed

ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
Formal Verification of Higher-Order Masked Arithmetic Programs                                                   111:3


to an attacker are independent of secret data. There are two key challenges: (1) the combinatorial
explosion problem of observable sets when the number of observable variables and the security
order increasing, and (2) how to efficiently and automatically resolve potential leaky observable
sets. The first challenge is addressed by the first step of our hybrid approach, for which we propose
a sound type system together with an efficient type inference algorithm, which can prescribe a
distribution type for each observable set. One can often—but not always—deduce leakage-freeness
of observable sets from their distribution types, whereas observable sets that cannot be solved by
the type system are regarded as potential leaky observable sets.
   In case that potential leaky observable sets are produced by the type system (i.e., the second
challenge), we provide automated resolution methods which are the second step of our hybrid
approach. This step is important: for instance, [6] reported 98,176 potential third-order sets on
Sbox [98], which are virtually impossible to check individually by human beings. Technically, the
second step is based on model-counting and pattern matching based methods. For the model-counting,
we consider two baseline algorithms: the first one transforms the problem to the satisfiability
problem of a (quantifier-free) first-order logic formula that can be solved by SMT solvers (e.g.
Z3 [46]), an extension of our previous one for first-order security [55]; the second one computes
the probability distribution of an observable set by naively enumerating all possible valuations of
variables. We give, for the first time in the current paper, a third, GPU-accelerated parallel algorithm,
to leverage GPU’s computing capability. Instead of creating a general GPU-based solver which is
control-flow intensive and would downgrade the GPU performance, we automatically synthesize a
GPU program for each potential leaky observable set, which, in a nutshell, enumerates all possible
valuations of variables by leveraging GPU parallel computing. It turns out that the GPU-based
parallel algorithm significantly outperforms the two baseline algorithms.
   The pattern matching based method is devised to further reduce the cost of model-counting. This
method infers the distribution type of an observable set from observable sets whose distribution
types are known, by searching an “isomorphism” between the computation expressions of the
variables in two observable sets. If such an isomorphism exists, one can conclude that the two
observable sets have the same distribution type, by which one can save costly model-counting
procedures. The pattern matching based method also automatically summarizes patterns of leaky
observable sets which can be used for diagnosis and debugging.
   Our hybrid approach enjoys several advantages over the existing approaches. Compared to
the empirical methods based on the statistical analysis of leakage traces, our approach is able to
give conclusive security assertions independent of assessment conditions, testing strategies or the
amount of gathered leakage traces. Compared to the existing formal verification approaches, our
overall hybrid approach is both sound and complete, and is able to verify more types of masked
implementations. Remarkably, our model-counting and pattern matching based methods could also
be integrated into existing formal verification approaches, effectively making them complete and
more efficient.
   We implement our approach in a tool HOME (Higher-Order Masking vErifier), and evaluate on
various benchmarks including masked implementations of full AES and MAC-Keccak programs.
The results are very encouraging: HOME can handle benchmarks that have never been verified by
existing formal verification approaches, e.g., implementations of Boolean to arithmetic mask con-
version from [97], arithmetic to Boolean mask conversion from [41], the non-linear transformation
and round function of Simon from [101]. Our tool is also significantly faster than [6] on almost all
secure programs (e.g., 110× and 31× speed-up for Key schedule [96] and 4th-order Sbox [98]; cf.
Table 1), which is the only available tool to verify masked higher-order arithmetic programs under
an equivalent leakage model to the ISW model. The experimental results confirm that HOME is
superior to existing tools in both functionality and performance.

                          ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
111:4                                                                                            Gao et al.


    To sum up, the main contributions of this work are as follows:
      • We propose a sound type system and provide an efficient type inference algorithm for proving
        security of masked arithmetic programs;
      • We propose a novel GPU-accelerated parallel algorithm to resolve potential leaky observable
        sets which significantly outperforms two baselines;
      • We propose a novel pattern matching based method to automatically summarize patterns of
        leakage sets, which can reduce the cost of model-counting;
      • We implement our algorithms in a software tool and demonstrate the effectiveness and
        efficiency of our approach on various benchmarks.

  The remainder of this article is organized as follows. In Section 2, we introduce basic notations
and recall the probing leakage model. In Section 3, we present a motivating example and the
overview of our approach. In Section 4, we present the sound type system, its inference algorithm
and sound transformations to facilitate type inference. In section 5, we describe the model-counting
and patter matching based methods. In Section 6, we evaluate the performance of our approach
on representative examples from the literature. We discuss related work in Section 7. Finally, we
conclude the article in Section 8.

2     PRELIMINARIES
In this section, we describe masked cryptographic programs, masking schemes, leakage models
and security notions.

2.1     Masked Cryptographic Programs
We fix an integer κ > 0 and the domain I = {0, · · · , 2κ − 1}. For a set R of random variables, let
D(R) denote the set of joint distributions over R.
Syntax. We focus on programs written in C-like code that implement cryptographic algorithms
such as AES, as opposed to arbitrary software programs. The syntax is given as follows.
                          Operation:        OP ∋ ◦ ::= ⊕ | ∧ | ∨ | ⊙ | + | − | ×
                          Expression: e ::= c ∈ I | x | e ◦ e | ¬e | e ≪ c | e ≫ c
                          Statememt:                stmt ::= x ← e | stmt; stmt
                          Program:                P ::= stmt; return x 1 , ..., xm ;
A program P is a sequence of assignments x ← e followed by a return statement, where e is
an expression building from a set of variables and κ-bit constants using the bitwise operations:
negation (¬), and (∧), or (∨), exclusive-or (⊕), left shift ≪ and right shift ≫; modulo 2κ arithmetic
operations: addition (+), subtraction (−), multiplication (×); and finite-field multiplication (⊙) over
the finite field F2κ .
    To analyze a cryptographic program P, it is common to assume that it is in straight-line form
(i.e., branching- and loop-free) [6, 50]. Remark that our tool supports programs with non-recursive
procedure calls and static loops by transforming to straight-line form by procedure inlining and
loop unfolding. We further assume that P is in the single static assignment (SSA) form (i.e., there is
at most one assignment x ← e in P for x.) and each expression uses at most one operator. (One can
easily transform an arbitrary straight-line program to the SSA form.) For an assignment x ← e, we
will denote by Operands(x) the set of operands associated with the operator of e.
    We fix a program P annotated by the public, private (such as keys) and random input variables.
The set X of variables in P is partitioned into four sets: X p , X k , X i and X r , where X p denotes the
set of public input variables, X k denotes the set of private input variables, X i denotes the set of

ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
Formal Verification of Higher-Order Masked Arithmetic Programs                                                   111:5


intermediate variables, and X r denotes the set of uniform random variables on the domain I. In
general, random variables are used for masking the private input variables.

Semantics. For each variable x ∈ X , we define the computation of x, E(x), as an expression over
input variables X p ∪ X k ∪ X r . Formally, for each x ∈ X , E(x) = x if x ∈ X p ∪ X k ∪ X r , otherwise x is
an intermediate variable (i.e., x ∈ X i ) which must be uniquely defined by an assignment statement
x ← e (thanks to SSA form of P), and thus E(x) is defined as the expression obtained from e
by sequentially replacing all the occurrences of the intermediate variables in e by their defining
expressions in P.
   A valuation is a function η : X p ∪ X k → I that assigns a concrete value to each input variable in
X p ∪ X k . Let Θ denote the set of valuations. Two valuations η 1 and η 2 are X p -equivalent, denoted
by η 1 ≈X p η 2 , if η 1 (x) = η 2 (x) for x ∈ X p , i.e., η 1 and η 2 must agree on their values on public input
variables. We denote by Θ2=X p ⊆ Θ×Θ the set of pairs of X p -equivalent valuations. For each variable
x ∈ X , let Eη (x) denote the expression obtained from E(x) by instantiating variables y ∈ X p ∪ X k
with concrete values η(y).
   Given a valuation η ∈ Θ, for each variable x ∈ X , the computation E(x) of x under the valuation
η can be interpreted as the probability distribution, denoted by ⟦x⟧η , over the domain I with
respect to the uniform distribution of the random variables Eη (x) may contain. Concretely, for
each c ∈ I, ⟦x⟧η (c) is the probability that Eη (x) evaluates to c. Accordingly, let ⟦P⟧η denote the
joint distribution over I |X | such that for every C = (c x ∈ I)x ∈X , ⟦P⟧η (V ) is the probability that
(Eη (x))x ∈X evaluates to (c x ∈ I)x ∈X . Therefore, the semantics of P is interpreted as a function
⟦P⟧ : Θ → D(X ) which takes a valuation η ∈ Θ as the input and returns a joint distribution ⟦P⟧η .
For each subset Y ⊆ X of variables, let ⟦P⟧Y denote the function ⟦P⟧Y : Θ → D(Y ) that returns,
for each η ∈ Θ, the marginal distribution of Y under ⟦P⟧η .

2.2   Masking
Masking is a randomization technique used to break the statistical dependence of the private input
variables and observable variables of the adversary [31, 69]. Fix a sound security parameter d, an
order-d masking typically makes use of a secret-sharing scheme to logically split the private data
into (d + 1) shares such that any d ′ ≤ d shares are statistically independent on the value of the
private input. The computation of shares for each private input is usually called presharing. A
masking transformation aims at transforming an unmasked program P that directly operates on
the private inputs into a masked program P ′ that operates on their shares. Finally, the desired data
are recovered via de-masking of the outputted shares of the masked program P ′.
   For example, using the order-d Boolean masking [69], the (d+1) shares of a key k are (r 1 , · · · , rd +1 ),
where the shares r 1 , . . . , rd are generated uniformly at random and rd +1 is computed such that
            Éd
rd +1 = k ⊕ i=1 r i . The value of k can be recovered via performing exclusive-or (⊕) operations on
                     Éd +1
all the shares, i.e., i=1 r i .
   Besides Boolean masking schemes, there are arithmetic masking schemes such as additive (e.g.,
(k + r ) mod n) and multiplicative masking schemes (e.g., (k × r ) mod n) for protecting arithmetic
operations. Secure conversion algorithms between them (e.g., [19, 38, 42, 59, 68]) have been proposed
for masking cryptographic algorithms that embrace both Boolean and arithmetic operations (such
as IDEA [76] and RC6 [37]).
   When increasing the masking order d, the attack cost usually increases exponentially, but the
performance of the masked programs degrades polynomially [62]. Therefore, the masking order is
chosen by a trade-off between attack cost and performance.

                          ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
111:6                                                                                                Gao et al.


2.3     Leakage Model and Security Notions
To formally verify the security of masked programs, it is necessary to define the set of observable
variables to the adversary and a leakage model that formally captures the leaked information from
the set of observable variables.
Observable variables. In the context of side-channel attacks, the adversary is assumed to be
able to observe the public (X p ), random (X r ), and intermediate (X i ) variables via side-channel
information, but is not able to observe the private input variables X k or the intermediate variables
of presharing. Indeed, presharing of each private input variable is performed outside of the program
and is included only for the verification purpose [6, 96]. Therefore, for each program P, it is easy to
automatically identify the set of observable variables X o ⊆ X p ∪ X i ∪ X r which is assumed to be
observed by the adversary. Each subset O ⊆ X o of observable variables is called an observable set.
Leakage model. In this article, we adopt the standard d-threshold probing model proposed by
Ishai, Sahai and Wagner [69], usually referred to as ISW d-threshold probing model (ISW model
for short), where the adversary may have access to the values of at most d observable variables of
his/her choice (e.g., via side-channel information). The more variables an adversary observes, the
higher the attack cost is.
Uniform and statistical independence. Given a program P and an observable set O ⊆ X o ,
      • P is uniform w.r.t. O, denoted by O-uniform, iff for all valuations η ∈ Θ: ⟦P⟧ηO is a uniform
        joint distribution;
      • P is statistically independent of X k with respect to O, denoted by O-SI, iff for every (η 1 , η 2 ) ∈
        Θ2=X p (i.e., η 1 and η 2 agreeing on their values on public input variables): ⟦P⟧ηO1 = ⟦P⟧ηO2 .
We say P is O-leaky if it is not O-SI.
   According to the above definitions, it is straightforward to verify the following proposition.
   Proposition 2.1. Given an observable set O of a program P,
   (1) if P is O-uniform, then P is O-SI and O ′-uniform for all O ′ ⊆ O;
   (2) if P is O-SI, then P is O ′-SI for all O ′ ⊆ O.
   Definition 2.2 (Security under the ISW d-threshold probing model [69]). A program P is order-d
secure if P is O-SI or O-uniform for every observable set O ⊆ X o with |O| = d.
   Intuitively, if P is O-SI or O-uniform, then the distribution of the variables in O (hence power
consumptions based on the variables in O in the ISW d-threshold probing model) does not rely on
private data, and thus the adversary cannot deduce any information by observing variables in O.
   In literature, the ISW d-threshold probing model is also called order-d perfect masking [50] or
d-non-interference (d-NI) [6]. There are other leakage models such as noise leakage model [94],
bounded moment model [9], ISW model with transitions [40] and with glitches [23, 80] and strong
d-non-interference (d-SNI) [7, 8, 54]. It is known that all these models (except for d-SNI and d-NI
introduced in [7] and the extensions thereof) can be reduced to the ISW d-threshold probing
model [6, 8, 9, 48] possibly at the cost of introducing higher orders when chosen plaintext attacks
are adopted, namely, the adversary can use any plaintext during attack. The d-SNI and d-NI models
defined in [7] are however stronger than the ISW d-threshold probing model. Namely, not all secure
masked programs under the ISW d-threshold probing model are safe under d-SNI/d-NI, so cannot
pass verification under this notion [9]. In this work, we adopt the ISW d-threshold probing model,
which is more common in side-channel analysis [23, 50, 55, 110].

ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
Formal Verification of Higher-Order Masked Arithmetic Programs                                                            111:7



    1 B o o l e a n T o A r i t h m e t i c (k, r, r ′ ) {             7     y4 ← y3 ⊕ x ′ ;
    2    x′ ← k ⊕ r ; / / p r e s h a r i n g                          8     y5 ← y4 − y3 ;
    3 y0 ← x ′ ⊕ r ′ ;                                                 9     A ← y5 ⊕ y2 ;
    4 y1 ← y0 − r ′ ;                                                 10     return A ;
    5 y2 ← y1 ⊕ x ′ ;                                                 11 }
    6 y3 ← r ′ ⊕ r ;


                         Fig. 1. Goubin’s Boolean to arithmetic mask conversion algorithm [59].


   Remark that the d-NI notion defined in [7, 8] is strictly stronger than the one defined in [6],
although they bear the same name. Namely, in [7, 8], the d-NI notion requires that the number of
shares of each private input variable that can be accessed by the adversary is strictly less than d + 1.
Research objective. Our goal is to develop automated verification methods to determine whether
a given masked arithmetic program is order-d secure under the ISW d-threshold probing model.

3     MOTIVATING EXAMPLE AND OVERVIEW OF APPROACHES
In this section, we present a motivating example and an overview of our approach.

3.1     Motivating Example
Figure 1 presents an example which is an implementation of the Boolean to arithmetic mask
conversion algorithm of Goubin [59]. The program assumes that the inputs are the private key
k and two random variables r , r ′. Line 2 is presharing which computes two shares (x ′, r ) of the
private key k via Boolean masking. (Remark that Line 2 should be performed outside of the function
BooleanToArithmetic and is introduced for verification purpose only. The actual implementation in
Goubin [59] takes two shares (x ′, r ) as input and assigns r ′ by a uniformly sampled random value.)
The function BooleanToArithmetic returns two shares (A, r ) of the arithmetic masking of the private
key k such that A + r = k, but without directly recovers the key k by x ′ ⊕ r .
   As setup for further use, we have: X p = ∅, X k = {k}, X r = {r , r ′ }, X i = {x ′, A, y1 , · · · , y5 } and
X o = {x ′, A, y0 , · · · , y5 , r, r ′ }. The computations of variables in X i are:
                   E(x ′) = k ⊕ r ;
                   E(y0 ) = (k ⊕ r ) ⊕ r ′;
                   E(y1 ) = ((k ⊕ r ) ⊕ r ′) − r ′;
                   E(y2 ) = (((k ⊕ r ) ⊕ r ′) − r ′) ⊕ (k ⊕ r );
                   E(y3 ) = r ′ ⊕ r ;
                   E(y4 ) = (r ′ ⊕ r ) ⊕ (k ⊕ r );
                   E(y5 ) = ((r ′ ⊕ r ) ⊕ (k ⊕ r )) − (r ′ ⊕ r );
                   E(A) = ((r ′ ⊕ r ) ⊕ (k ⊕ r )) − (r ′ ⊕ r ) ⊕ (((k ⊕ r ) ⊕ r ′) − r ′) ⊕ (k ⊕ r ) .
                                                                                                    

   For each observable variable z ∈ X o , the program is {z}-uniform (note that E(A) is equivalent
to k − r ), and thus it is first-order secure. However, this program is not second-order secure, e.g.,
y0 ⊕ y3 ≡ x ′ ⊕ r ≡ k allowing to extract private key k by observing {y0 , y3 }.

3.2     Overview of Approach
The overview of our approach HOME is depicted in Figure 2, consisting of four main components:
pre-processor, type system, pattern matching based method, and model-counting based method.
Given a masked program P and the security order d, HOME checks whether the masked program P

                                   ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
111:8                                                                                                          Gao et al.


                                                         HOME

 Masked                          Program in            observable                  observable
 Program                         SSA form      Type       set     Pattern matching    set     Model-counting
                 Pre-processor                                                                                   Result
                                              System               based method               based method
    Order d



                                       Fig. 2. Overview of our approach HOME.


is order-d secure or not. If P is not order-d secure, then HOME outputs the leaks, i.e., all the size-d
observable sets O such that P is O-leaky.
   Given a masked program P and the order d, the pre-processor unfolds the static loops (i.e., loops
with a predetermined bound of iterations) and inlines the procedure calls, and then transforms
the program into the SSA form. The type system is used to check whether each size-d observable
set O is order-d secure by deriving valid type judgements. If we can deduce that the observable
set O is either order-d secure or certainly not according to the distribution type, then the result is
conclusive.
   However, as usual, the type system is incomplete, namely, it is possible that the distribution type
cannot be inferred in which case we first apply the pattern matching based method. This method
iteratively searches an “isomorphism" between the computation expressions of the variables in
O and the variables in O ′, where O ′ is another size-d observable set whose distribution type is
already known. If such an isomorphism exists, we can conclude that these two observable sets O
and O ′ have the same distribution type, effectively resolving the observable set O. The result of
the observable set O will be fed back to the type system which can be used to gradually improve
the accuracy of the type inference.
   When the pattern matching based method fails to resolve the observable set O, we will apply the
(normally expensive) model-counting based method, which is able to completely decide whether
the observable set O is order-d secure. Finally, the observable set O is cached for further invocation
of pattern matching. As before, the result of the observable set O will be fed back to the type
system.
   This procedure gives a sound and complete approach for verification of higher-order security. In
the next two sections, we will elucidate the details of the type system, type inference algorithm,
model-counting and pattern matching based methods.

4     TYPE SYSTEM
In this section, we first present a type system to infer the distribution type of an observable set,
then propose three sound transformations to facilitate type inference, and finally present the type
inference algorithm based on the type system and the sound transformations.

4.1      Dominant Variables
We first introduce the notion of dominant variables.
  Definition 4.1. A random variable r is called a dominant variable of an expression e if the following
two conditions hold:
  (1) r (syntactically) occurs in the expression e exactly once; and
  (2) for each operator ◦ on the path between the leaf r and the root in the abstract syntax tree of
      the expression e,
      • if ◦ = ⊙, then one of its children is a non-zero constant; or

ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
Formal Verification of Higher-Order Masked Arithmetic Programs                                                                                        111:9


         • ◦ ∈ {⊕, ¬, +, −}; or
         • ◦ is a (univariate) bijective function.
    We denote by Var(e) the set of variables appearing in an expression e, by RVar(e) the set Var(e) ∩
X r , and by Dom(e) the set of all dominant (random) variables of e. All of these sets can be computed
in polynomial time in the size of e. Furthermore, note that a particularly useful example of bijective
functions is Sbox which is ubiquitous in cryptographic programs. Ð
    If r x is a dominant variable of the expression E(x) such that r x < x ′ ∈ O.x ′ ,x RVar(E(x ′)), then
E(x) can be seen as a fresh random variable when evaluating ⟦P⟧ O . Therefore, if each expression
E(x) for x ∈ O has such dominant variables, we can deduce that P is O-uniform.
  Proposition 4.2. Given an observable  Ð set O ⊆ X o , if for every x ∈ O there exists a dominant
variable r x ∈ Dom(E(x)) such that r x < x ′ ∈ O.x ′ ,x RVar(E(x ′)), then P is O-uniform.
    Proof. To prove this proposition, we first introduce the notion of i-invertibility. An expression
(i.e., function) e(x 1 , · · · , x n ) is i-invertible if, for any concrete values c 1 , · · · , c i−1 , c i+1 , · · · , c n ∈ I,
the expression
                                        e(c 1 /x 1 , · · · , c i−1 /x i−1 , x i , c i+1 /x i+1 , · · · , c n /x n )
obtained by instantiating all the variables (x j )j,i with concrete values (c j )j,i is bijective. It is easy
to see that e(c 1 /x 1 , · · · , c i−1 /x i−1 , x i , c i+1 /x i+1 , · · · , c n /x n ) and x i have same distribution. Thus, if
x i is a random variable, then e(c 1 /x 1 , · · · , c i−1 /x i−1 , x i , c i+1 /x i+1 , · · · , c n /x n ) must be a uniform
distribution.
    The following claim reveals the relation between dominated expressions and i-invertibility.
     Claim. Given an expression e(x 1 , · · · , x n ) over variables {x 1 , · · · , x n }, for every 1 ≤ i ≤ n, if
     x i is a dominant variable of e(x 1 , · · · , x n ), then e(x 1 , · · · , x n ) is i-invertible.
   We prove that e(x 1 , · · · , x n ) is i-invertible by induction on the length ℓ of the path between the
leaf r and the root in the abstract syntax tree of e.
Base case ℓ = 0. The expression e(x 1 , · · · , x n ) must be x r which is a bijective function. The result
immediately follows.
Inductive step ℓ > 0. Let ◦ be the operator at the root of the syntax tree of e(x 1 , · · · , x n ), then
e(x 1 , · · · , x n ) is in the form of
   (1) ¬e 1 (x 1 , · · · , x n ), or
   (2) ◦(e 1 (x 1 , · · · , x n )) where ◦ is a (univariate) bijective function, or
   (3) e 1 (x 1 , · · · , x n )◦e 2 (x 1 , · · · , x i−1 , x i+1 , · · · , x n ) such that x i is a dominant variable of e 1 (x 1 , · · · , x n ),
          where ◦ ∈ {⊙, ⊕, +, −}. (Note that x i does not appear in e 2 (x 1 , · · · , x i−1 , x i+1 , · · · , x n ).)
By the induction hypothesis, e 1 (x 1 , · · · , x n ) is i-invertible. By the definition of i-invertibility, for any
concrete values c 1 , · · · , c i−1 , c i+1 , · · · , c n ∈ I, e 1 (c 1 /x 1 , · · · , c i−1 /x i−1 , x i , c i+1 /x i+1 , · · · , c n /x n ) is bi-
jective. Then, the result immediately follows if e(x 1 , · · · , x n ) is ¬e 1 (x 1 , · · · , x n ) or ◦(e 1 (x 1 , · · · , x n )),
i.e., Item (1) and Item (2). It remains to consider Item (3).
      • If ◦ = ⊙, then e 2 (x 1 , · · · , x i−1 , x i+1 , · · · , x n ) is a non-zero constant. Since the multiplicative
          group of the non-zero elements in I is cyclic and 0 ⊙ e 2 (x 1 , · · · , x i−1 , x i+1 , · · · , x n ) = 0, then
          e 1 (c 1 /x 1 , · · · , c i−1 /x i−1 , x i , c i+1 /x i+1 , · · · , c n /x n )⊙e 2 (c 1 /x 1 , · · · , c i−1 /x i−1 , c i+1 /x i+1 , · · · , c n /x n )
          is also bijective. Hence, the result follows.
      • If ◦ ∈ {⊕, +, −}, then e 2 (c 1 /x 1 , · · · , c i−1 /x i−1 , c i+1 /x i+1 , · · · , c n /x n ) is a constant. For any
          constant c ∈ I, e 1 (c 1 /x 1 , · · · , c i−1 /x i−1 , x i , c i+1 /x i+1 , · · · , c n /x n ) ◦ c is still bijective (note that
          + and − are operators over the ring I). Hence, the result follows.

                                    ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
111:10                                                                                                Gao et al.


   Now, we prove the proposition.
   Suppose for every x ∈ O, there exists r x ∈ Dom(E(x)) such that r x < x ′ ∈ O.x ′ ,x RVar(E(x ′)),
                                                                              Ð

let ⟦P[r x /x]x ∈ O ⟧ηO denote the distribution of ⟦P⟧ηO in which E(x) is replaced by r x for all x ∈ O,
then for all valuations η ∈ Θ, ⟦P⟧ηO = ⟦P[r x /x]x ∈ O ⟧ηO holds.
   By applying the above claim, we get that ⟦P[r x /x]x ∈ O ⟧ηO is a uniform distribution. Therefore,
the result immediately follows.                                                                       □

   Example 4.3. Let us consider the motivating example in Section 3.1. E(x ′) is dominated by the
random variable r . E(y0 ) and E(y3 ) both have two dominant variables r and r ′. E(y1 ) only has the
dominant variable r , as r ′ occurs twice. Similarly, E(y4 ) only has the dominant variable r ′, as r
occurs twice. Thus, for every observable set O ⊆ {x ′, y0 , t 1 , y3 , y4 } with |O| = 1, we can deduce
that the program is O-uniform. E(y2 ), E(y5 ) and E(A) have no dominant variables, as both r and r ′
occur more than once.
   For the observable set {x ′, y3 }, although the dominant variable r ′ of E(y3 ) does not appear in
E(x ′), the dominant variable r of E(x ′) appears in E(y3 ), thus we cannot deduce that the program
is {x ′, y3 }-uniform. Indeed, for any observable set O ⊆ {x ′, A, y1 , · · · , y5 , r , r ′ } with |O| ≥ 2, we
cannot deduce that the program is O-uniform.

4.2      Types and Type Inference Rules
In this subsection, we introduce distribution types and their inference rules for proving higher-order
security.

   Definition 4.4. Let T be the set of (distribution) types {τuf , τsi , τlk },
      • τuf stands for uniform distribution, i.e., O : τuf means that the program is O-uniform;
      • τsi stands for secret independent distribution, i.e., O : τsi means that the program is O-SI;
      • τlk stands for leak, i.e., O : τlk means that the program is O-leaky, namely, not O-SI.
where O is an observable set.

   The distribution type τuf is a subtype of τsi , i.e., τuf implies τsi , but τsi does not imply τuf .
Although, both τsi and τuf can be used to prove that the program is statistically independent of
the secret for an observable set O, i.e., no leak, τuf is more desired because the observable set O
not only is statistically independent of the secret (same as in τsi ), but also can be used like a set of
random variables. Therefore, we prefer τuf over τsi and want to infer as many τuf as possible.
   Type judgements are in the form of ⊢ O : τ where O is an observable set, τ ∈ T is the type
of O. Note that we omitted the context of the type judgement for simplifying presentation. The
type judgement ⊢ O : τ is valid iff the distribution of the values of variables from O satisfies the
property specified by τ in the program P.
   Figure 3 presents type inference rules for the first-order security. We denote by OP∗ the set
OP ∪ {≪, ≫}. Rule (Com) captures the commutative law of operators ⋆ ∈ OP. Rules (Idei ) for i =
1, 2, 3, 4 are straightforward. Rule (Sid4 ) states that x has type τsi if x ← x 1 ◦ x 2 for ◦ ∈ {∧, ∨, ⊙, ×},
both x 1 and x 2 have type τuf , and E(x 1 ) has a dominant variable r which is not used by E(x 2 ).
Indeed, E(x) can be seen as r ◦ E(x 2 ). Rule (Sid5 ) states that expression x has type τsi if x ← x 1 • x 2
for • ∈ OP∗ , both x 1 and x 2 have type τsi (as well as its subtype τuf ), and the sets of random
variables used by E(x 1 ) and E(x 2 ) are disjoint. Indeed, for each valuation η ∈ Θ, the distributions
⟦x 1 ⟧η and ⟦x 2 ⟧η are independent. Rule (Sdd) states that the variable x has type τlk if x ← x 1 ◦ x 2
for ◦ ∈ {∧, ∨, ⊙, ×}, x 1 has type τlk , x 2 has type τuf , and E(x 2 ) has a dominant variable r which is
not used by E(x 1 ). Intuitively, E(x) can be safely seen as E(x 1 ) ◦ r .

ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
Formal Verification of Higher-Order Masked Arithmetic Programs                                                                 111:11

                     ⊢ x1 ⋆ x2 : τ   x ← x2 ⋆ x1                                          ⊢ x′ : τ   x ← ¬x ′
                                 ⊢x :τ                                                            ⊢x :τ
                                                        (Com)                                                        (Ide1 )


                         ⊢ x ′ : τsi    x ← x′ • x′                                                 x ← x′ ⋄ x′
                                   ⊢ x : τsi                                                          ⊢ x : τsi
                                                        (Ide2 )                                                      (Ide3 )


                                                                      ⊢ x 1 : τuf ⊢ x 2 : τuf  x ← x1 ◦ x2
                        ⊢ x ′ : τlk    x ← x ′ ▷◁ x ′                     Dom(E(x 1 )) \ RVar(E(x 2 )) , ∅
                                   ⊢ x : τlk                                         ⊢ x : τsi
                                                        (Ide4 )                                                     (Sid4 )


           ⊢ x 1 : τsi  ⊢ x 2 : τsi  x ← x1 • x2                       ⊢ x 1 : τlk ⊢ x 2 : τuf  x ← x1 ◦ x2
               RVar(E(e 1 )) ∩ RVar(E(e 2 )) = ∅                           Dom(E(x 2 )) \ RVar(E(x 1 )) , ∅
                           ⊢ x : τsi                                                  ⊢ x : τlk
                                                        (Sid5 )                                                      (Sdd)


Fig. 3. Type inference rules for first-order security, where ⋆ ∈ OP, ◦ ∈ {∧, ∨, ⊙, ×}, • ∈ OP∗ , ▷◁∈ {∧, ∨} and
⋄ ∈ {⊕, −}.

                 x ∈ O Var(E(x))) ∩ X k = ∅                          ⊢ O1 : τsi       x ∈ O2 Var(E(x)) ⊆ X p
                 Ð                                                                    Ð
             (
                                                 (No-Key)                                                         (Sid1 )
                       ⊢ O : τsi                                                  ⊢ O1 ∪ O2 : τsi

                                                                  ⊢ O : τsi   Operands(x) ⊆ O ∪ X p ∪ I
                                                                                                                  (Sid2 )
                                                                         ⊢ O ∪ {x } : τsi

                             ⊢ O1 : τsi       ∀x ∈ O2 .∃r x ∈ Dom(E(x)) \ y ∈ O1 ∪O2 ∧y,x RVar(E(y))
                                                                          Ð
                                                                                                                  (Sid3 )
                                                            ⊢ O1 ∪ O2 : τsi

                             ⊢ O1 : τuf       ∀x ∈ O2 .∃r x ∈ Dom(E(x)) \          y ∈ O1 ∪O2 ∧y,x RVar(E(y))
                                                                                  Ð
                                                                                                                  (Rud)
                                                            ⊢ O1 ∪ O2 : τuf

                             Fig. 4. Type inference rules for higher-order security.


   Note that the type inference rules for the first-order security are similar to those from [55], which
are reproduced here for completeness. The new rules for the higher-order security are given in
Figure 4. We briefly explain these rules below.
   Rule (No-Key) states that if O is an observable set whose values are independent of private
variables, then O has type τsi . Rule (Sid1 ) states that if O1 has type τsi and the computations
E(x) of variables x ∈ O2 only involve public variables, then we can deduce that O1 ∪ O2 has type
τsi . Rule (Sid2 ) states that if O has type τsi and a variable x is defined using constants, public
variables or variables in O, then adding x into O does not change the type. Intuitively, as the
value of x is determined by its operands, for every (η 1 , η 2 ) ∈ Θ2=X p , ⟦P⟧ηO1 = ⟦P⟧ηO2 if and only
if ⟦P⟧ηO∪{x
        1
              }
                = ⟦P⟧ηO∪{x
                       2
                           }
                             . Rule (Sid3 ) deals with a τsi -typed observable set O1 and a τuf -typed
observable set O2 (cf. Proposition 4.2). Assume that each computation E(x) for x ∈ O2 has a
dominant variable r x which is not used in any computation of variable in O1 ∪ O2 except x, then
O1 ∪ O2 has type τsi . Intuitively, each computation E(x) for x ∈ O2 can be seen as the random
variable r x , and O1 has type τsi , hence, the distributions ⟦x⟧η for all x in O1 ∪ O2 and all valuations
η ∈ Θ are independent. Similarly, rule (Rud) deals with two τuf -typed observable sets O1 and O2 .
Although the dominant variables of E(x) for x ∈ O1 may appear in the computations of variable in
O2 , by Proposition 4.2, all the variables x ∈ O 2 can be seen as fresh random variables r x so that
Proposition 4.2 can be applied.
  Theorem 4.5 (Soundness of the type system). For every set observable O ⊆ X o ,
  (1) if ⊢ O : τsi is valid, then P is O-SI;

                           ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
111:12                                                                                                                              Gao et al.


   (2) if ⊢ O : τuf is valid, then P is O-uniform;
   (3) if ⊢ O : τlk is valid, then P is O-leaky.
   Proof. We only show the soundness of rules for the higher-order security. First, Item (3) directly
follows from the first-order case [55]. We now deal with the rules in Figure 4.
    • Rule (No-Key). Suppose ( x ∈ O Var(E(x))) ∩ X k = ∅, then the expression E(x) does not use
                                     Ð
      any private variable for all x ∈ O. This implies that ⟦P⟧ηO1 = ⟦P⟧ηO2 for every (η 1 , η 2 ) ∈ Θ2=X p
      (note that η 1 and η 2 must agree on their values on public input variables).
    • Rule (Sid1 ). Suppose ⊢ O1 : τsi , then ⟦P⟧ηO11 = ⟦P⟧ηO21 for every (η 1 , η 2 ) ∈ Θ2=X p . Consider O2
      such that x ∈ O2 Var(E(x)) ⊆ X p , then for every x ∈ O2 , (η 1 , η 2 ) ∈ Θ2=X p and assignment of
                    Ð

      random variables f : X r → I, the expression E(x) evaluates to same value under (η 1 , f ) and
      (η 2 , f ). This implies that ⟦P⟧ηO11 ∪O 2 = ⟦P⟧ηO21 ∪O 2 for every (η 1 , η 2 ) ∈ Θ2=X p .
   • Rule (Sid2 ). Suppose ⊢ O : τsi , then ⟦P⟧ηO1 = ⟦P⟧ηO2 for every (η 1 , η 2 ) ∈ Θ2=X p . Suppose the
     observable set O is {x 1 , · · · , x n }, then for each vector of concrete values (c 1 , · · · , c n ) ∈ In ,
     ⟦P⟧ηO1 (c 1 , · · · , c n ) = ⟦P⟧ηO2 (c 1 , · · · , c n ). Consider x n+1 such that Operands(x n+1 ) ⊆ O ∪X p ∪ I,
     let c n+1 denote the value of x n+1 under the valuation η 1 and x 1 = c 1 , · · · , x n = c n , and
     c n+1
       ′    denote the value of x n+1 under the valuation η 2 and x 1 = c 1 , · · · , x n = c n . Since η 1
     and η 2 must agree on their values on public input variables, then c n+1 = c n+1                                     ′ . Therefore,

     for every concrete value c, ⟦P⟧ηO∪{x                 1
                                                               n+1 }
                                                                     (c 1 , · · · , c n , c) = ⟦P⟧ηO∪{x
                                                                                                    2
                                                                                                        n+1 }
                                                                                                              (c 1 , · · · , c n , c) = 0 if
                            O∪{x n+1 }                                                                  O∪{x n+1 }
     c , c n+1 , ⟦P⟧η1                 (c 1 , · · · , c n , c) = ⟦P⟧η1 (c 1 , · · · , c n ) and ⟦P⟧η2
                                                                           O
                                                                                                                       (c 1 , · · · , c n , c) =
     ⟦P⟧ηO2 (c 1 , · · · , c n ) if c = c n+1 . Hence, the result immediately follows.
   • Rule (Sid3 ). Suppose ⊢ O1 : τsi , then ⟦P⟧ηO11 = ⟦P⟧ηO21 for every (η 1 , η 2 ) ∈ Θ2=X p . Consider O2
     such that ∀x ∈ O2 .∃r x ∈ Dom(E(x)) \ y ∈ O1 ∪O2 ∧x ,y RVar(E(y)), i.e., for each x ∈ O2 , there
                                                                Ð
     exists a dominant random variable r x ∈ Dom(E(x)) which is not used in other expressions
     in E(y) for y ∈ O1 ∪ O2 with x , y. Thus, ⟦P⟧ηO11 ∪O 2 = ⟦P⟧ηO21 ∪O 2 for every (η 1 , η 2 ) ∈ Θ2=X p .
   • Rule (Rud). Consider O2 such that ∀x ∈ O2 .∃r x ∈ Dom(E(x)) \ y ∈ O1 ∪O2 ∧x ,y RVar(E(y)),
                                                                                                      Ð
     i.e., for each x ∈ O2 , there exists a dominant random variable r x ∈ Dom(E(x)) which is not
     used in other expressions in E(y) for y ∈ O1 ∪ O2 with x , y. Let O3 denote the set of such
     random variables r x . Then, ⟦P⟧ηO11 ∪O 2 = ⟦P⟧ηO21 ∪O3 , for every (η 1 , η 2 ) ∈ Θ2=X p .
     Since the program is O1 -uniform, then we get that the program is O1 ∪ O3 -uniform. The
     result follows from ⟦P⟧ηO11 ∪O 2 = ⟦P⟧ηO21 ∪O3 .
The proof is completed.                                                                                                                        □
   Remark that our type inference rules are designed to be redundant for efficiency consideration.
Namely, they have distinct complexities to check the premises. For instance, rule (Rud) is special
case of rule (Sid3 ), as τuf is a subtype of τsi , but we prefer τuf over τsi . Also, rule (Rud) is a
reformation and generalization of Proposition 4.2 which allows to add more observable variables
to the observable set O1 without searching dominant variables in the computations of variables in
O1 . A valid judgement derived by rule (Sid2 ) in constant-time can also be derived by using other
rules, but rule (Sid2 ) could avoid unfolding the definitions of variables. When applying these rules,
we start with those which can infer the type τuf and whose premises can be established at a lower
cost, namely, in the order of rules (Rud), (Sid2 ), (Sid1 ), (No-Key) and (Sid3 ).
   Example 4.6. Let us consider the motivating example in Section 3.1. Recalling that E(y3 ) = r ′ ⊕ r ,
although we can derive both ⊢ {y3 } : τuf by applying rule (Rud) and ⊢ {y3 } : τsi by applying rule
(No-Key). We will prefer ⊢ {y3 } : τuf .

ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
Formal Verification of Higher-Order Masked Arithmetic Programs                                                  111:13


   In Example 4.3, we claim that for any observable set O ⊆ {x ′, A, y1 , · · · , y5 , r , r ′ } with |O| ≥ 2,
we cannot deduce that the program is O-uniform by applying Proposition 4.2. As an example, let us
consider the observable set {x ′, y3 }. As E(x ′) is dominated by the random variable r , we derive that
⊢ {x ′ } : τuf . As E(y3 ) has the dominant variable r ′ which does not appear in E(x ′), we can derive
that ⊢ {x ′, y3 } : τuf by applying rule (Rud). However, r appears in E(y3 ), so we cannot directly
apply Proposition 4.2 to prove that the program is {x ′, y3 }-uniform. Similarly, we can deduce that
⊢ {x ′, y0 } : τuf and ⊢ {x ′, y4 } : τuf , but we still cannot deduce the distribution types of the other
size-2 observable sets. For instance, we cannot infer the distribution type of the observable set
{x ′, y1 }, as Dom(E(x ′)) = Dom(E(y1 )) = {r }.

4.3   Sound Transformations
In this subsection, we describe three sound, domain-specific transformations for facilitating type
inference.
   The first transformation is based on the observation that some computations may share common
sub-expressions which are dominated by some random variables, and these random variables are
only used in these sub-expressions. Such sub-expressions, treated as random variables (i.e., replaced
by the dominant variables) when analyzing the computations, are uniform and independent. This
may enable type inference rules, as the other random variables in sub-expressions will be eliminated.
Therefore, we can simplify computations by leveraging the notion of dominant variables.
   For instance, consider the observable set {x ′, y1 } in the motivating example. Recall that E(x ′) =
k ⊕ r and E(y1 ) = ((k ⊕ r ) ⊕ r ′) − r ′. We can observe that the sub-expression k ⊕ r is dominated
by the random variable r which occurs exclusively in k ⊕ r . Therefore, E(x ′) and E(y1 ) can be
simplified as r and (r ⊕ r ′) − r ′ respectively, as the distributions of v ⊕ r and r are identical for any
value v ∈ I of k, and r does not affect the values of other sub-expressions. Using the simplified
computations r and (r ⊕ r ′) − r ′ of E(x ′) and E(y1 ), we can deduce ⊢ {x ′, y1 } : τsi by applying rule
(No-Key). This simple, but crucial, observation is formalized as the following definition.
    Definition 4.7. A sub-expression e in a set of computations E is dominated by a random variable r
if r ∈ Dom(e) and r only occurs in e, namely, does not occur in E elsewhere.
   To facilitate type inference, we may replace the largest r -dominated sub-expression e by r , which
can be done in polynomial-time by traversing the abstract syntax tree. Let SimplyDom (E) be the set
of computations obtained from E by repeatedly applying this strategy.
   SimplyDom is generally very effective in our experiments, but fails on one benchmark. This
is because SimplyDom only relies upon syntactic information of the computation. For instance,
consider the observable set {x 1 , x 2 } taking from the second-order masked implementation of the
AES Sbox [98], where
                                                          
    • E(x 1 ) = Sbox (0 ⊕ ((k ⊕ r 0 ) ⊕ r 1 )) ⊕ r 1 ⊕ r 2 ⊕ r 3 ,
                                                     
                                                           
    • E(x 2 ) = Sbox (r 0 ⊕ ((k ⊕ r 0 ) ⊕ r 1 )) ⊕ r 1 ⊕ r 2 ⊕ r 3 ,
                                                      

k is a private input variable, and r 0 , r 1 , r 2 , r 3 are random variables. SimplyDom is not able to simplify
the sub-expression r 2 ⊕ r 3 into a random variable, though both r 2 and r 3 are dominant variables of
r2 ⊕ r3.
   SimplyDom could be applied if we could transform E(x 1 ) and E(x 2 ) to equivalent forms (by the
associativity of ⊕), i.e.,
     Sbox (0 ⊕ ((k ⊕ r 0 ) ⊕ r 1 )) ⊕ r 1 ⊕ (r 2 ⊕ r 3 ) and Sbox (r 0 ⊕ ((k ⊕ r 0 ) ⊕ r 1 )) ⊕ r 1 ⊕ (r 2 ⊕ r 3 ).
                                                                                                  

However, carrying out such a transformation automatically is very challenge in general, as there is
no canonical representation of the computation to which SimplyDom can be applied. To address

                          ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
111:14                                                                                                 Gao et al.


this challenge, we propose the sound transformation which aims to collapse several variables into
one variable, e.g., collapse r 2 and r 3 into a new random variable even if they do not appear as the
sub-expression r 2 ⊕ r 3 . This idea is formalized as the following definition.
   Definition 4.8. Given a set of computations E and a set of variables Z ⊆ e ∈E Var(e), Z is
                                                                                        Ð
collapsible with respect to E if the following two conditions hold:
   (1) Z ⊆ X p or Z ⊆ X k or Z ⊆ X r , namely, variables in Z have the same type;
   (2) and there exist sub-expressions e 1 , · · · , ek in E such that: É
       • sub-expression e j for each 1 ≤ j ≤ k can be rewritten as ( z ∈Z z) ⊕ e j′ , i.e., clustering the
         variables in Z together,
       • and each variable z ∈ Z only occurs in {e 1 , · · · , ek }, and occurs in e j for each 1 ≤ j ≤ k
         exactly once.
   One can observe that if Z is collapsible, then z ∈Z z can be replaced by a fresh variable respecting
                                                    É
the type (i.e. public, key, or random) when analyzing {E(x) | x ∈ O} for the observable set O. For
simplicity, we usually use Z to denote the fresh variable. We denote by SimplyCol (E) the set of
computations computed from E by repeatedly applying this strategy. SimplyCol (E) is implemented
in polynomial-time by iteratively searching pairs of variables {x 1 , x 2 } that are collapsible and
replacing them by {x 1 , x 2 }.
   The third transformation is the application of algebra laws. We denote by SimplyAlg (E) the set of
computations computed from E by repeatedly applying algebra laws such as e ⊕ e ≡ 0, 0 ⊕ e ≡ e,
0 × e ≡ 0, 0 ⊙ e ≡ 0 and e − e ≡ 0. For 0 ⊕ e ≡ e, 0 × e ≡ 0, 0 ⊙ e ≡ 0, we directly search for the
constant 0. For e ⊕ e ≡ 0 and e − e ≡ 0, the representation of computations in E shares the same
common sub-expressions so that we do not need to compare whether two sub-expressions are
same or not when applying SimplyAlg (E). Moreover, instead of considering only sub-expressions of
the form e ⊕ e (resp. e − e), we search for two occurrences of the sub-expression e such that the
operators on the path between the roots of two occurrences of e are all ⊕ (resp. −).
   It is straightforward to verify the following proposition.
   Proposition 4.9. Given a program P and an observable set O, let P denote the program
                                             (x ← E(x); )x ∈ O return;
where E(x) is obtained from E(x) by applying SimplyDom (E), SimplyCol (E) and/or SimplyAlg (E), then
    O
⟦P⟧ and ⟦P⟧ O generate the same distribution over O.
   Example 4.10. Let us consider the above example, i.e., the observable set {x 1 , x 2 }, where
                                                          
    • E(x 1 ) = Sbox (0 ⊕ ((k ⊕ r 0 ) ⊕ r 1 )) ⊕ r 1 ⊕ r 2 ⊕ r 3 ,
                                                     
                                                           
    • E(x 2 ) = Sbox (r 0 ⊕ ((k ⊕ r 0 ) ⊕ r 1 )) ⊕ r 1 ⊕ r 2 ⊕ r 3 ,
                                                      

k is a private input variable, and r 0 , r 1 , r 2 , r 3 are random variables. The type system in Figure 4 fails
to prove ⊢ {x 1 , x 2 } : τuf .
   One can observe that Z = {r 2 , r 3 } is collapsible with respect to {E(x 1 ), E(x 2 )}, so by replacing
Z = {r 2 , r 3 } with a new random variable Z , {E(x 1 ), E(x 2 )} can be simplified to
          E 1 = {Sbox (0 ⊕ ((k ⊕ r 0 ) ⊕ r 1 )) ⊕ r 1 ⊕ Z , Sbox (r 0 ⊕ ((k ⊕ r 0 ) ⊕ r 1 )) ⊕ r 1 ⊕ Z }.
                                                                                                 

   By iteratively applying SimplyAlg to E 1 using algebraic laws r 0 ⊕ r 0 ≡ 0 and r 1 ⊕ r 1 ≡ 0, we obtain

                    E 2 = {Sbox 0 ⊕ ((k ⊕ r 0 ) ⊕ 0) ⊕ Z , Sbox (k ⊕ 0) ⊕ 0 ⊕ Z }.
                                                                             


ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
Formal Verification of Higher-Order Masked Arithmetic Programs                                                   111:15


     Algorithm 1: Type inference algorithm.
 1 PLS := ∅; λ :=empty_map; π :=empty_map;
 2 Function HOME(P, X p , X k , X r , X o , d)
 3    X check := {x ∈ X o | Var(E(x)) ⊈ X p };
 4     forall x ∈ X check do
 5         if SimplyAlg (E(x)) , E(x) then
 6              λ(x) := SimplyAlg (E(x));
 7              π (x) := Dom(λ(x));
 8         else π (x) := Dom(E(x));
 9     Explore({(d, X check )});
10     return PLS;
11 Function Explore(Y)
12    forall (i, O) ∈ Y do
13         Choose a subset Ci, O ⊆ O in a topological order from leaf to root s.t. |Ci, O | = i;
14    if Check({Ci, O }(i, O)∈Y ) = ⊤ then
15         forall (i, O) ∈ Y, x ∈ O \ Ci, O in a topological order from leaf to root do
16             if Check({Ci, O }(i, O)∈Y , {x }) = ⊤ then
17                  Ci, O := Ci, O ∪ {x };
                            Ð
18    else PLS := PLS ∪ { (i, O)∈Y Ci, O };
19    Y ′ := {(i, O) ∈ Y | |O| > i ∧ i , 0};
20    if Y ′ = ∅ then return;
      forall (i, O) ∈ Y ′, 0 ≤ i j ≤ min(i, |O \ Ci, O |) s.t. (i, O)∈Y ′ i j , 0 do
                                                                 Í
21
           Explore((Y \ Y ′ ) ∪ (i, O)∈Y ′ {(i − i j , Ci, O ), (i j , O \ Ci, O )});
                                 Ð
22

23    return;
24 Function Check({Ci, O }(i, O)∈Y , Y = ∅)
      if ⊢ Y ∪ (i, O)∈Y Ci, O : τ for some τ ∈ {τuf , τsi } is valid then
               Ð
25
26         return ⊤;
      else if ⊢SimplyDom Y ∪ (i, O)∈Y Ci, O : τ for some τ ∈ {τuf , τsi } is valid then
                             Ð
27
28         return ⊤;
      else if ⊢SimplyCol Y ∪ (i, O)∈Y Ci, O : τ for some τ ∈ {τuf , τsi } is valid then
                            Ð
29
30         return ⊤;
31    return ⊥;


      Since 0 ⊕ e ≡ 0 ⊕ e ≡ e, by iteratively applying SimplyAlg to E 2 , we obtain
                                   E 3 = {Sbox(k ⊕ r 0 ) ⊕ Z , Sbox(k) ⊕ Z }.
Since r 0 is the dominant variable of Sbox(k ⊕ r 0 ) ⊕ Z but does not occur in Sbox(k) ⊕ Z , by applying
SimplyDom , we obtain E 4 = {r 0 , Sbox(k)⊕Z }. Now, Z becomes the dominant variable of Sbox(k)⊕Z
but does not occur in r 0 , by applying SimplyDom again, we obtain that E 5 = {r 0 , Z }, from which
we can deduce ⊢ {x 1 , x 2 } : τuf .

4.4 Type Inference Algorithm
In this subsection, we present our type inference algorithm.
   To prove that P is order-d secure, it is necessary to ensure that, for all size-d observable subsets
O ⊆ X o , P is O-SI. Evidently, exhaustive enumeration of |Xdo | subsets may not scale. To address this
                                                                
issue, the key idea is Proposition 2.1 which states that if the program P is O-SI (resp. O-uniform),

                           ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
111:16                                                                                                       Gao et al.


then P is also O ′-SI (resp. O ′-uniform) for any subset O ′ ⊆ O. Therefore, the main strategy is to
find observable sets {Oi }i=1 n as large as possible such that P is O -SI for all 1 ≤ i ≤ n, and for each
                                                                      i
size-d subset O ⊆ X o , O ⊆ Oi for some 1 ≤ i ≤ n.
   Our idea is formalized in Algorithm 1, where ⊢ O : τ denotes the type inference without applying
the transformations SimplyDom or SimplyCol ; ⊢SimplyDom O : τ denotes the type inference aided
with the transformation SimplyDom ; ⊢SimplyCol O : τ denotes the type inference aided by both
transformations SimplyDom and SimplyCol . Taking a program P, sets of public (X p ), private (X k ),
random (X r ) and observable (X o ) variables, and the order d as inputs, the algorithm first initializes
three data structures: PLS for storing all potential leaky observable sets, λ for storing the simplified
computation of each variable, and π for storing the set of dominant variables of the (simplified)
computation E(x) for each variable x.
   At Line 3, Algorithm 1 computes the set X check of observable variables whose computation
involves either private or random variables. This allows to isolate the set of observable variables
whose computation involves public input variables only. Hence, according to rule (Sid1 ), it suffices
to consider size-d subsets O ⊆ X o \ {x ∈ X o | Var(E(x)) ⊆ X p }. At Lines 4-8, it simplifies the
computation E(x) for each variable x ∈ X check by invoking SimplyAlg and computes its dominant
variables; the results are stored in λ and π for later use. After that, it invokes the function Explore
with the set {(d, X check )} (Line 9). We assume that |X check | ≥ d, otherwise we can directly check
whether ⊢ X check : τsi is valid or not.
   The function Explore is more involved. It aims at proving     Ð that for all pairs (i, O) ∈ Y and all
possible subsets Oi ⊆ O with size i, the type judgement ⊢ (i, O)∈Y Oi : ττsi is valid. Taking a set
Y of pairs (i, O) as input which satisfies the following three properties:
   (1) Ò{i |(i, O)∈Y } i = d, namely, the sum of orders’ i for subsets O in Y is the target order d;
       Í
   (2) {O | (i, O) ∈ Y} = X check , namely, the subsets O in Y form a partition of X check ; and
   (3) |O| ≥ i for all (i, O) ∈ Y, namely, there are at least i variables in O for each (i, O) ∈ Y.
Remark that these properties are maintained and required to show the correctness and termination
of our algorithm.
   An illustration of the function Explore is given in Figure 5. The function Explore first chooses a
size-i subset Ci, O ⊆ O for each pair (i, O) ∈ YÐin a topological order from leaf to root (Line 13).
Then it checks whether the type judgement ⊢ (i, O)∈Y Ci, O : τ for some τ ∈ {τuf , τsi } is valid or
not by invoking the function Check (Line 14).
     • If it is valid, i.e., the observable set (i, O)∈Y Ci, O has distribution type τuf or τsi (as shown
                                               Ð
        in the middle-part of Figure 5), then Explore iteratively tries to add the remaining observable
        variables x to Ci, O for x ∈ O \ Ci, O and (i, O) ∈ Y by invoking the function Check (Lines
        15-17). The effect
                        Ð of this addition is shown in the right-part of FigureÐ5.
     • Otherwise ⊢ (i, O)∈Y Ci, O : τ for any τ ∈ {τuf , τsi } is invalid, then (i, O)∈Y Oi is a poten-
        tially leaky set and is added to the set PLS (Line 18).
                    Ð
Finally, to cover (i, O)∈Y Oi for all possible size-i subsets Oi ⊆ O and pairs (i, O) ∈ Y, it remains
                                  Ð
to check the observable sets (i, O)∈Y Oi , where there exists at least one pair (i, O) ∈ Y such that Oi
                                                                Ð                 Ð
contains at least one variable from O \ Ci, O . (Otherwise (i, O)∈Y Oi ⊆ (i, O)∈Y Ci, O .) To do this,
we first extract the pairs (i, O) such that |O| > i and i , Ð  0, i.e., Y := {(i, O) ∈ Y | |O| > i ∧ i , 0}
                                                                         ′

at Line 19. If Y ′ is empty, then all the possible subsets (i, O)∈Y Oi are covered and Algorithm 1
terminates (Line 20). Otherwise, we partition all the pairs (i, O) ∈ Y ′ into pairs     Í(i − i j , Ci, O ), (i j , O \
Ci, O ) for all combinations of values 0 ≤ i j ≤ min(i, |O \ Ci, O |) such that (i, O)∈Y ′ i j , 0. The
condition (i, O)∈Y ′ i j , 0 is used to avoid the case (i, O)∈Y Oi ⊆ (i, O)∈Y Ci, O . For each such
             Í                                             Ð                 Ð
combination of values, the partitioned pairs {(i − i j , Ci, O ), (i j , O \ Ci, O ) | (i, O) ∈ Y ′ } together

ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
Formal Verification of Higher-Order Masked Arithmetic Programs                                                   111:17


                                                   size = d                              size ≥ d


         (i1 , O1 )                                  Ci1 ,O1                                     Ci1 ,O1

                            ..           After          ..         ..      After            ..         ..   ..
                             .           Line 14         .          .      Line 17           .          .    .

        (ik , Ok )                                   Cik ,Ok                                     Cik ,Ok



                                        Fig. 5. Intuition of Algorithm 1.


with the pairs {(i, O) ∈ Y | |O| = i ∨ i = 0} (i.e., Y \ Y ′) are checked by recursively calling the
function Explore. It is easy to observe that the recursionÐ maintains the above three properties.
   The function Check first verifies whether ⊢ Y ∪ (i, O)∈Y Oi : τ for some τ ∈ {τuf , τsi } is
valid, which may be aided with data structures λ and π (Line 25). If it is valid, ⊤ is returned (Line
26). Otherwise,Ð it is verified with the additional transformation SimplyDom (Line 27). If it still
fails, ⊢ Y ∪ (i, O)∈Y Oi τ for some τ ∈ {τuf , τsi } is checked using the additional transformation
SimplyCol on the expressions yielded by SimplyDom (Line 29). Once ⊢ Y ∪ (i, O)∈Y Oi : τ for some
                                                                                 Ð
τ ∈ {τuf , τsi } is derived, Check returns ⊤ (Lines 28 and 30). If all of these
                                                                              Ð steps fail, ⊥ is returned
(Line 31). Notices that during the above type inference, once ⊢ Y ∪ (i, O)∈Y Oi : τlk becomes
valid, Check also returns ⊥. Moreover, in order to avoid recomputing SimplyDom and SimplyCol ,
the sequence of applied transformations are recorded, and the simplified expressions are cached.
When the function Check is invoked at Line 16, i.e., Y is nonempty, we first check whether the
recorded sequence of applied transformations is still legal. If it is still applicable, we will reuse
the simplified expressions and apply SimplyDom and/or SimplyCol to E(x) as well. Otherwise, the
function Check immediately returns ⊥.
   Remark that the type inference rules are applied in the order of increasing complexities of
checking the premises while preferring τuf over τsi . We also remark that the choice of the subsets
at Line 13 and the variable x at Line 15 may have significant impact on the performance. We choose
variables from leaf to root following the order of the size of the defining computation, in light of
Rule (Sid2 ) in Figure 4.
   The procedure terminates as we only partition pairs (i, O) ∈ Y such that |O| > i and i , 0
and the sizes of Ci, O and O \ Ci, O in partitioned pairs (i − i j , Ci, O ) and (i j , O \ Ci, O ) eventually
become smaller and smaller in recursive calls until |O| = i or i = 0. (Note that we keep pairs
of the form (0, O) in the worklist for simplifying presentation. They are indeed removed in our
implementation.)
  Theorem 4.11. P is order-d secure if PLS = ∅. Moreover, if P is O-leaky for O ⊆ X check with
|O| = d, then O ∈ PLS.
   Note that the reverse of Theorem 4.11 may not hold. To prove Theorem 4.11, we start with the
following lemmas. First, we show that the above three properties always hold.
  Lemma 4.12. In Algorithm 1, at each call Explore(Y), the following three properties are hold:
  (1) {(i, O)∈Y } i = d;
      Í
  (2) {O | (i, O) ∈ Y} = X check ;
      Ò
  (3) and |O| ≥ i for all (i, O) ∈ Y.

                          ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
111:18                                                                                                   Gao et al.


   Proof. Let Yℓ denote the parameter Y at the ℓt h call of Explore. Let us apply induction on ℓ. The
base case ℓ = 1 immediately follows from the fact that Y1 = {(d, X check )} (note that we assumed
|X check | ≥ d). It remains to prove the inductive step. Suppose the result holds at ℓ > 1 and Yℓ+1 =
(Yℓ \ Y ′) ∪ {(i − i j , Ci, O ), (i j , O \ Ci, O ) | (i, O) ∈ Y ′ }, where Y ′ = {(i, O) ∈ Yℓ | |O| > i ∧ i , 0}.
     • By applying the induction hypothesis, we get that {i | (i, O) ∈ Yℓ } = d. Since
                                                                        Í

                {i | (i, O) ∈ Yℓ+1 } = {i | (i, O) ∈ Yℓ \ Y ′ } + {i − i j , i j | (i, O) ∈ Y ′ }
             Í                                 Í                             Í
                                            = {i | (i, O) ∈ Yℓ \ Y ′ } + {i | (i, O) ∈ Y ′ }
                                               Í                             Í
                                            = {i | (i, O) ∈ Yℓ },
                                               Í

      we conclude the proof of Item (1).
    • By applying the induction hypothesis, we get that {O | (i, O) ∈ Yℓ } = X check . Since
                                                       Ò

        {O | (i, O) ∈ Yℓ+1 } = {O | (i, O) ∈ Yℓ \ Y ′ } ⊎ {Ci, O , O \ Ci, O | (i, O) ∈ Y ′ }
      Ò                         Ò                        Ò
                             = {O | (i, O) ∈ Yℓ \ Y ′ } ⊎ {O | (i, O) ∈ Y ′ }
                                Ò                        Ò
                             = {O | (i, O) ∈ Yℓ },
                                Ò

      we conclude the proof of Item (2).
    • By applying the induction hypothesis, |O| ≥ i for all (i, O) ∈ Yℓ \Y ′. For each pair (i, O) ∈ Yℓ ,
      according to Lines 13 and 17, |Ci, O | ≥ i , hence |Ci, O | ≥ i −i j . Since 0 ≤ i j ≤ min(i, |O \ Ci, O |),
      we get that |O \ Ci, O | ≥ i j . We conclude the proof of Item (3).
                                                                                                               □
   We now prove the termination of Algorithm 1.
   Lemma 4.13. Algorithm 1 always terminates.
  Proof. It suffices to show that the recursive procedure call of Explore always terminates. Let Yℓ
denote the parameter Y at the ℓt h call of Explore. By Lemma 4.12(3), |O| ≥ i for all (i, O) ∈ Yℓ .
   • If |O| = i or i = 0 for all (i, O) ∈ Yℓ , then Y ′ = ∅. In this case, Explore will not be called at
     Line 22 during the ℓt h call. Hence, Algorithm 1 terminates.
   • Otherwise, there are some (i, O) ∈ Yℓ such that |O| > i and i , 0. Then, such pairs (i, O) are
     always partitioned into (i −i j , Ci, O ) and (i j , O \ Ci, O ). Since (i, O)∈Y ′ i j , 0, by Lemma 4.12(1
                                                                            Í
     and 2), there exists ℓ > ℓ for Yℓ′ such that |O| = i or i = 0 for all (i, O) ∈ Yℓ′ . Hence,
                             ′

     Algorithm 1 always terminates.
                                                                                                              □
   We show the soundness of Algorithm 1.
   Lemma 4.14. For every subset O ⊆ X check such that |O| = d, O is covered by Algorithm 1, namely,
either O is added into PLS, or there exists a subset O ′ such that ⊢ O : τsi is valid and O ⊆ O ′.
  Proof. Given a set Y of pairs, let Cover (Y) denote the set of subsets O ⊆ X check such that
|O| = d and O contains i elements of O ′ for each pair (i, O ′) ∈ Y. It suffices to show that for every
call Explore(Y), each subset O ∈ Cover (Y) is covered.
  Let Yℓ denote the parameter Y at the ℓt h call of Explore. We apply induction on ℓ, where the
base case is the largest ℓ. Note that such ℓ exists by Lemma 4.13.
Base case. The base case is the largest ℓ such that Y ′ = ∅ at the ℓth call of Explore. Since
Y ′ = {(i, O ′) ∈ Yℓ | |O ′ | > i ∧ i , 0} = ∅, by Lemma 4.12(3), |O ′ | = i or i = 0 for all (i, O ′) ∈ Yℓ .
By Lemma 4.12(1 and 2), Cover (Y) is singleton set. Suppose Cover (Y) = {O}, then O is covered.
Indeed, either ⊢ O : τsi is valid or O is added into PLS.
Inductive step. There exists                     ′      such that |O ′ | > i and i , 0. For every subset
                                Ðsome pair (i, O ) ∈ Yℓ Ð
O ∈ Cover (Yℓ ), either O ⊆ (i, O′ )∈Yℓ Ci, O′ or O ⊈ (i, O′ )∈Yℓ Ci, O′ .

ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
Formal Verification of Higher-Order Masked Arithmetic Programs                                                   111:19


                                                                        (i, O ′ )∈Yℓ Ci, O ′ : τsi is valid.
               Ð                                                         Ð
    • If O ⊆      (i, O ′ )∈Yℓ Ci, O ′ , then O is covered. Indeed, ⊢
    • Otherwise O ⊈ (i, O′ )∈Yℓ Ci, O′ , then O contains at least one variable from O ′ \ Ci, O′ for
                           Ð
      some pair (i, O ′) ∈ Yℓ , i.e., O ∩ (O ′ \ Ci, O′ ) , ∅. There must exist a combination of values
      i j : 0 ≤ i j ≤ min(i, |O ′ \ Ci, O′ |) for (i, O ′) ∈ Y ′ such that
                 O ∈ cover ((Yℓ \ Y ′) ∪ {(i − i j , Ci, O′ ), (i j , O ′ \ Ci, O′ ) | (i, O ′) ∈ Y ′ }).
       By applying induction hypothesis, the subset O is covered.
We complete the proof.                                                                                                □

   Proof of Theorem 4.11. If PLS = ∅, then by Lemma 4.14, ⊢ O : τsi is valid for every size-d
subset O ⊆ X check . Hence P is order-d secure.
   On the other hand, for every size-d subset O ⊆ X check , if P is O-leaky, then ⊢ O : τsi is not valid.
By Lemma 4.14, all the size-d subsets O ⊆ X check are covered by Algorithm 1, hence, O is added
into PLS.                                                                                              □

   Example 4.15. We demonstrate Algorithm 1 on the motivating example (cf. Section 3.1) for d = 2.
First of all, X check = X o = {x ′, A, y0 , · · · , y5 , r , r ′ } as X p = ∅. After applying the transformation
SimplyAlg , λ and π are given below:
     λ(y4 ) = r ′ ⊕ k,                                            λ(y5 ) = (r ⊕ k) − (r ⊕ r ),
                                                                              ′         ′

     λ(A) = r ⊕ k) − (r ⊕ r ) ⊕ (((k ⊕ r ) ⊕ r ) − r ) ⊕ (k ⊕ r ) .
                 ′     ′                      ′     ′
                             

            π (x ′) = {r }, π (r ) = {r },          π (r ′) = {r ′ }, π (y0 ) = {r , r ′ }, π (y1 ) = {r },
            π (y2 ) = ∅,        π (y3 ) = {r , r }, π (y4 ) = {r ′ }, π (y5 ) = {r },
                                                ′                                           π (A) = ∅.
HOME invokes Explore({(2, X o )}). Suppose Explore chooses {r, r } at Line 13, i.e., C2,X o = {r , r ′ }
                                                                               ′

then, ⊢ C2,X o : τuf is valid, namely, Check({C2,X o }) will return ⊤. The loop at Lines 15-17 will
iteratively test x ′, y0 , · · · , y5 , A. Among them, only y3 can be added into C2,X o according to rule
(Sid2 ). Now, we can deduce that all size-2 subsets O ⊆ C2,X o = {r , r ′, y3 } have type τuf or τsi .
   It is easy to see that Y ′ = {(2, X o )}, as |X o | > 2. Therefore, at Line 22, the following two
procedure calls will be made:
    • Call1 : Explore(Y1 ), where Y1 = {(0, {r , r ′, y3 }), (2, {x ′, A, y0 , y1 , y2 , y4 , y5 })}
    • Call2 : Explore(Y2 ), where Y2 = {(1, {r , r ′, y3 }), (1, {x ′, A, y0 , y1 , y2 , y4 , y5 })}.
  For Call1 , suppose Explore chooses {x ′, y0 } at Line 13, i.e., C2, {x ′,A,y0,y1,y2,y4,y5 } = {x ′, y0 }. We
derive ⊢ {x ′, y0 } : τuf by applying rule (Rud) with O1 = {x ′ } and O2 = {y0 }. The loop at Lines
15-17 will add y1 into C2, {x ′,A,y0,y1,y2,y4,y5 } , as replacing the common sub-expression k ⊕ r in
{E(x ′), E(y0 ), E(y1 )} with r using the transformation SimplyDom , i.e., E(x ′), E(y0 ) and E(y1 ) re-
spectively becoming r , r ⊕r ′, (r ⊕r ′)−r ′, allow us to derive ⊢ {x ′, y0 , y1 } : τsi . By replaying this trans-
formation on E(y2 ), y2 can also be added into C2, {x ′,A,y0,y1,y2,y4,y5 } , which becomes {x ′, y0 , y1 , y2 }.
However, y4 , y5 and A cannot be added into C2, {x ′,A,y0,y1,y2,y4,y5 } .
  For Call2 , suppose Explore chooses {r } from {r , r ′, y3 } and x ′ from {x ′, A, y0 , y1 , y2 , y4 , y5 } at
Line 13. We cannot derive any type judgement ⊢ {r , x ′ } : τ for τ ∈ T . So {r , x ′ } is added to PLS.
Finally,
                      {r , r ′, x ′, y2 , y3 , y4 , y5 } × {A} ∪ {r ′, y2 } × {y4 } ∪
                                                                                                    
          PLS =                                                                                        .
                          {r , x ′, y0 , y1 , y2 } × {y5 }     ∪ {r } × {x ′, y1 , y2 } ∪ {y2 , y3 }

5   MODEL-COUNTING AND PATTERN MATCHING BASED METHODS
We propose three model-counting based methods (cf. Section 5.1—5.3) for resolving potential leaky
observable sets prescribed by type inference algorithm. Generally, model-counting is very costly,

                           ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
111:20                                                                                                                          Gao et al.


so we propose a complementary pattern matching based method to efficiently resolve potential
leaky observable sets from known sets, avoiding a vast amount of model-counting usage.

5.1      SMT-based Method
We first lift the SMT-based method [55] from first-order to higher-order.
  Recall that P is O-leaky iff ⟦P⟧ηO1 , ⟦P⟧ηO2 for some pair (η 1 , η 2 ) ∈ Θ2=X p . Let O = {x 1 , . . . , xm }.
For every valuation η ∈ Θ and tuple of values (c 1 , . . . , cm ) ∈ Im , let ♯η (x 1 = c 1 , · · · , xm = cm )
denotes the number of assignments ηr : X r → I such that for all 1 ≤ j ≤ m, E(x j ) evaluates to c j
under η and ηr . Then, O-leaky can be characterized as the following logical formula:

           Ω O := ∃(η 1 , η 2 ) ∈ Θ2=X p ∃(c 1 , · · · , cm ) ∈ Im .
                                                                                                                                      (1)
                                              ♯η1 (x 1 = c 1 , · · · , xm = cm ) , ♯η2 (x 1 = c 1 , · · · , xm = cm )
                                                                                                                            

   Proposition 5.1. Ω O is satisfiable iff P is O-leaky.
   Proof. The program P is O-leaky iff the following formula holds:

               ∃(η 1 , η 2 ) ∈ Θ2=X p ∃(c 1 , · · · , cm ) ∈ Im . ⟦P⟧ηO1 (c 1 , · · · , cm ) , ⟦P⟧ηO2 (c 1 , · · · , cm )
                                    ♯η (x 1 =c 1, ··· ,xm =cm )
Since ⟦P⟧ηO (c 1 , · · · , cm ) =            2κ ×|X r |
                                                                for η ∈ {η 1 , η 2 }, then the program P is O-leaky iff the
following formula holds:
                                                        ♯η1 (x 1 = c 1 , · · · , xm = cm )       ♯η2 (x 1 = c 1 , · · · , xm = cm )
   ∃(η 1 , η 2 ) ∈ Θ2=X p ∃(c 1 , · · · , cm ) ∈ Im .                                        ,
                                                                    2κ×|X r |                                2κ×|X r |
The result follows immediately.                                                                                                        □

   We further encode Ω O as a first-order logic formula that can be solved by SMT solvers (e.g.,
Z3 [46]). Suppose E(x j ) = e j for 1 ≤ j ≤ m, let E O = E 1 ⊎ E 2 with E 1 = {e | Var(e) ∩ X k , ∅}, and
E 2 = {e | Var(e) ∩ X k = ∅}. We define the first-order logic formula Ψ O as
                                   Ó                                            
                                                                          Θ ′ )
                                             Ó
                                ©     e ∈E 1    f :RVar(e)→I   (Θ e,f  ∧    e, f   ª
                                ­                        Ó                         ®
                                ­                                                  ®
                        Ψ O := ­
                                                                          
                                                      f :RVar(e)→I Θe, f
                                ­                                                  ®
                                          Ó
                                             e ∈E 2
                                                    Ó                              ®, where
                                ­                        Ó                         ®
                                ­                                                  ®
                                ­                                                  ®
                                               Θ         Θ ′      Θ
                                                                        
                                «                v2i ∧     v2i  ∧     ,            ¬
• Program logic (Θe, f and Θe,    ′ ): for every e = E(x) ∈ E and f : RVar(e) → I, Θ
                                    f                                   O                   e, f encodes the
   expression e into a first-order logic formula and asserts that the value of e under the assignment
   f is equal to a fresh variable x f . (Note there are 2 |RVar(e)| distinct conjuncts all of which share
   the variables X p ∪ X k .)
  Θe,
    ′ is similar to Θ
      f               e, f except that x f and k ∈ X k are replaced by fresh variables x f and k . Note
                                                                                                ′      ′

  that for every e ∈ E 2 , we do not construct Θe,   ′ , as e ∈ E 2 does not have any private variable
                                                       f
  k ∈ X k and hence Θe, f would be same as Θe, f .
                       ′


• Vector to integer (Θv2i and Θv2i  ′ ): Θ
                                            v2i asserts that for every f :   e ∈E O RVar(e) → I, a fresh
                                                                           Ð
  integer variable I f is 1 if the vector (x f )x ∈ O is equal to the vector (c 1 , · · · , cm ), otherwise 0.
  By doing so, we can count the number of assignments f ’s of random variables under which

ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
Formal Verification of Higher-Order Masked Arithmetic Programs                                                  111:21


      y000 = (k ⊕ 0) ⊕ 0 ∧ y000
                             ′ = (k ′ ⊕ 0) ⊕ 0 ∧ y
                                                   001 = (k ⊕ 1) ⊕ 0 ∧ y 001 = (k ⊕ 1) ⊕ 0 ∧
                                                                          ′       ′
                                                                                        
      y010 = (k ⊕ 0) ⊕ 1 ∧ y010
                             ′ = (k ′ ⊕ 0) ⊕ 1 ∧ y
                                                   011 = (k ⊕ 1) ⊕ 1 ∧ y 011 = (k ⊕ 1) ⊕ 1 ∧
                                                                          ′       ′
                                              

                  (y300 = 0 ⊕ 0) ∧ (y301 = 0 ⊕ 1) ∧ (y310 = 1 ⊕ 0) ∧ (y311 = 1 ⊕ 1) ∧
            I 00 = (y000 = c 1 ∧ y300 = c 2 ) ? 1 : 0 ∧ I 01 = (y001 = c 1 ∧ y301 = c 2 ) ? 1 : 0 ∧
                                                                                                   

           I 10 = (y010 = c 1 ∧ y310 = c 2 ) ? 1 : 0 ∧ I 11 = (y011 = c 1 ∧ y311 = c 2 ) ? 1 : 0 ∧ 
            I 00
              ′ = (y ′ = c ∧ y
                     000     1    300 = c 2 ) ? 1 : 0 ∧ I 01 = (y 001 = c 1 ∧ y 301 = c 2 ) ? 1 : 0 ∧
                                                           ′       ′

            I 10 = (y010 = c 1∧ y310 = c 2 ) ? 1 : 0 ∧ I 11 = (y011 = c 1 ∧ y311
              ′      ′                                     ′       ′
                                                                                   = c2) ? 1 : 0 ∧
                                     (I 00 + I 01 + I 10 + I 11 ) , (I 00
                                                                       ′ + I′ + I′ + I′ )
                                                                            01   10   11


                                           Fig. 6. The SMT encoding Ψ {y0,y3 } .


  (e 1 , · · · , em ) evaluates to (c 1 , · · · , cm ) when variables x ∈ X p ∪ X k take some concrete values.
  Formally,
                                       Û                                                                
                       Θv2i :=                           I f = (c 1 , · · · , cm ) == (x f )x ∈ O ? 1 : 0 .
                            f:   e ∈E O RVar(e)→I
                                 Ð


  Θv2i
    ′   is similar to Θv2i except that I f is replaced by I f′ , and x f is replaced by x f′ for all x ∈ O such
  that E(x) ∈ E 1 . Note that k ′ ∈ X k may have different value than k, but x ∈ X p has same value in
  Θv2i and Θv2i′ . This conforms to (η , η ) ∈ Θ2
                                             1 2        =X p in Equ. (1).
• Different sums (Θ, ): It asserts two sums of assignments f ’s of random variables for variables
  (k)k ∈X k and (k ′)k ∈X K (i.e., integers I f and I f′ ) differ. This conforms to ♯η1 (x 1 = c 1 , · · · , xm =
  cm ) , ♯η2 (x 1 = c 1 , · · · , xm = cm ) in Equ. (1). Formally,
                                           
                                               Õ                      Õ
                                   Θ, :=                  If ,                  I f′ .
                                          f:   e ∈E O RVar(e)→I     f : e ∈E RVar(e)→I
                                               Ð                       Ð
                                                                           O


  It is straightforward to get the following proposition,
  Proposition 5.2. Ω O is satisfiable iff Ψ O is satisfiable, where the size of Ψ O is exponential in the
number of (bits of) random variables.
  By Proposition 5.1 and Proposition 5.2, we get that:
  Corollary 5.3. Ψ O is satisfiable iff P is O-leaky.

  Example 5.4. Let us consider the observable set {y0 , y3 } in the motivating example (cf. Section 3.1).
Recall that E(y0 ) = (k ⊕ r ) ⊕ r ′ and E(y3 ) = r ′ ⊕ r . In this case, E 1 = {E(y0 )} and E 2 = {E(y3 )}.
The SMT formula Ψ {y0,y3 } is shown in Figure 6, where the first two lines correspond to the logical
formulas Θ E(y0 ), f , the third line corresponds to the logical formulas Θ E(y3 ),f , the next four lines
correspond to the logical formulas Θv2i and Θv2i′ , and the last one corresponds to the logical formula

Θ, . (For clarity, we only show the case when all variables are Boolean.) Ψ {y0,y3 } is satisfiable,
implying that the program is {y0 , y3 }-leaky.

5.2   Brute-force Method
The brute-force method (cf. Alg. 2) enumerates all possible valuations and then computes corre-
sponding distributions again by enumerating the assignments of random variables.
  Proposition 5.5. Ω O is satisfiable iff Algorithm 2 returns SAT.

                          ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
111:22                                                                                          Gao et al.


     Algorithm 2: A brute-force algorithm
 1 Function BFEnum(P, O = {x 1 , · · · , xm })
      forall ηp : x ∈ O X p ∩ Var(E(x)) → I do
                   Ð
 2
 3        D 1 := λ(c 1 , · · · , cm ) ∈ Im .0;
 4        b := false;
          forall ηk : x ∈ O X k ∩ Var(E(x)) → I do
                         Ð
 5
 6             D 2 := λ(c 1 , · · · , cm ) ∈ Im .0;
 7             if b = false then
 8                  D 1 :=Counting(P, O, ηp , ηk );
 9                  b := true;
10             else
11                  D 2 :=Counting(P, O, ηp , ηk );
12                  if D 1 , D 2 then return SAT;
13    return UNSAT;
14 Function Counting(P, O = {x 1 , · · · , xm }, ηp , ηk )
      forall ηr : x ∈ O RVar(E(x)) → I do
                 Ð
15
16        D[Eηp ,ηk ,ηr (x 1 ), · · · , Eηp ,ηk ,ηr (xm )] + +;
17    return D;


   The complexity of Algorithm 2 is exponential in the number of (bits of) variables in computations
(E(x))x ∈ O , so it would experience significant performance degradation when facing a large number
of variables. We propose a GPU-accelerated parallel algorithm to boost the performance.

5.3      GPU-accelerated Parallel Algorithm
In this subsection, we show how to leverage GPU’s superior compute capability to check satisfiability
of Ω O in Eqn. (1). In general, given a potential leaky observable set O, we automatically synthesize
a GPU program from the computations of observable variables in O such that the GPU program
outputs SAT iff Ω O is satisfiable, i.e., the program is O-leaky.
   Our work is based on CUDA, a parallel computing platform and programming model for NVIDIA
GPUs. Specifically, we utilize Nvidia GeForce GTX 1080 (Pascal) with compute capability 6.1. From
a programming perspective, the CUDA architecture defines three levels of threads, i.e., grid, block
and warp, to organize units. A warp consists of 32 consecutive threads which are executed in the
Single Instruction Multiple Thread fashion on Streaming Processors, namely, all threads execute
the same instruction, and each thread carries out that operation on its own private data. A block
running on Streaming Multiprocessors contains at most 32 wraps (giving rise to 32 × 32 threads).
The maximum number of blocks in a grid is 65, 535 × 65, 535 and each grid runs on the Scalable
Streaming Processor Array. The code running on GPUs is usually referred to as Kernel.
   We parallelize Algorithm 2 as a CUDA program. In this work, we illustrate the idea on byte
programs, i.e., each variable is of 8-bit. Typically, the number of random variables is usually much
larger than that of the other variables. Therefore, we enumerate assignments of random variables
in GPUs while enumerate valuations of public and input variables in CPUs. Namely, the Counting
function in Algorithm 2 is implemented as a Kernel. However, it would be difficult to implement a
generic Kernel to compute distributions of sets of computations (E(x))x ∈ O , unless computations
are evaluated by traversing their abstract syntax trees, which is control-flow intensive and would
downgrade the GPU performance. As a result, instead of designing a generic Kernel, for each
observable set O, we automatically synthesize a CUDA program which checks whether Ω O is
satisfiable based on Algorithm 2.

ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
Formal Verification of Higher-Order Masked Arithmetic Programs                                                   111:23


  Algorithm 3: The skeleton of synthesized GPU programs
 1 __device__ unsigned char op1(...)
 2     ...;
 3 ...

 4 __device__ unsigned char opj(...)
 5     ...;
 6 __device__ unsigned char exp1 (ηp , η k , η r , threadIdx, blockIdx)
 7     ...;
 8 ...

 9  __device__ unsigned char expm (ηp , ηk , ηr , threadIdx, blockIdx)
10     ...;
 11 int main GPUBFEnum(P, O = {x 1 , · · · , xm })
 12     int *D 1 ; int *D 2 ;
 13     cudaMallocManaged(&D 1 , 256m );
 14     cudaMallocManaged(&D 2 , 256m );
 15     dim3 block(16,16);
 16     dim3 grid(4096/block.x,4096/block.y);
        forall ηp : x ∈ O X p ∩ Var(E(x)) → I do
                       Ð
 17
18           memset(D 1 , 0, sizeof(unsignedchar));
19           b := false;
             forall ηk : x ∈ O X k ∩ Var(E(x)) → I do
                            Ð
20
21                 memset(D 2 , 0, sizeof(unsignedchar));
22                 if b = false then
23                      KernelCounting<<<grid, block>>> (D 1 , ηp , ηk );
24                      cudaDeviceSynchronize();
25                      b := true;
26                 else
27                      KernelCounting<<<grid, block>>> (D 2 , ηp , ηk );
28                      cudaDeviceSynchronize();
29                      if D 1 , D 2 then
30                            return SAT;
 31     return UNSAT;
32 __global__ void KernelCounting(D, ηp , ηk )
      {r 1 , · · · , rh } := x ∈ O RVar(E(x));
                            Ð
33

34    forall ηr : {r 4 , · · · , rh } → I do
35           c 1 :=exp1 (ηp , ηk , ηr , threadIdx, blockIdx);
36           ...
37           cm :=expm (ηp , ηk , ηr , threadIdx, blockIdx);
             index := m−1   i=0 c i × 256 ;
                                           i
                           Í
38
39           atomicAdd(&D[index], 1);



   The numbers of threads per block
                                 Ð and blocks per grid in each synthesized CUDA program are
determined by the number R := | x ∈ O RVar(E(x))| of random variables in (E(x))x ∈ O . If R = 3, we
choose 2-D (16, 16) blocks each of which has 28 threads, and 2-D (256, 256) grids each of which has
216 blocks. (Note that the number 224 of threads exactly corresponds to the number of valuations of
three 8-bits random variables.) Moreover, we do not need to enumerate those valuations, as the

                           ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
111:24                                                                                              Gao et al.


thread Id and block Id (i.e., threadIdx and blockIdx in CUDA) of each host thread in GPU exactly
corresponds one of those valuations. If R < 3, we reduce the number of blocks and/or threads such
that the total number of threads is the number of valuations of random variables. Otherwise R > 3,
we set 28 number of threads in each block and 216 number blocks in one grid for three random
variables, while the valuations of the rest of the random variables are enumerated in GPU.
   For each operation used in computations of (E(x))x ∈ O but is not supported in CUDA, we
synthesize a corresponding __device__ function which will be called from GPUs only and executed
therein. For each computation E(x), we also synthesize a __device__ function which computes the
value of E(x) using __device__ functions for operations based on thread Id and block Id of the host
thread which represent the valuations of some random variables.
   For memory management, we use int arrays to store distributions, which are accessed both from
CPU for comparing distributions (read-only) and GPU for computing distributions (read and write).
We utilize unified memory provided by CUDA to allocate memory for both int arrays, namely, to
allocate memory by invoking the cudaMallocManaged function, by which the managed pointers
to int arrays are valid on both the GPU and CPU. To resolve data race, the update of int arrays in
Kernel is performed in one atomic transaction (via the atomicAdd function in CUDA).
   Concretely, Algorithm 3 shows a skeleton of synthesized GPU programs, where the number of
random variables is greater than 3. Other cases are similar. The __device__ functions implement all
the CUDA non-supported operations and expressions which are invoked and executed on GPU.
D 1 and D 2 are int arrays for storing distributions. The function KernelCounting is the Kernel
which computes distributions for each valuation of public and private input variables. The function
KernelCounting is invoked at Line 20 and Line 24 for each valuation of public and private
input variables. After each invoking of KernelCounting, the function cudaDeviceSynchronize is
invoked which waits until all preceding commands in all streams of all host threads have completed.
In the body of KernelCounting, the valuations of the first three random variables are implicitly
represented by threadIdx and blockIdx, while ηr denotes a valuation of other random variables.
Finally, the values of expressions are iteratively computed via calling the corresponding __device__
functions. The value vector of expressions is encoded as an index to the array D, where the value
at this index increases 1 atomically to avoid data race.

5.4      Method based on Pattern Matching
In order to avoid (costly) model-counting, we propose a novel pattern matching based method,
which allows to resolve potential leaky observable sets more efficiently. This idea comes from the
observation that cryptographic programs usually have very similar blocks and many observable
sets share common observable variables. As a warmup, let us first consider two observable sets
{x, y} and {x ′, y ′ }, where E(x) = r , E(y) = k ⊕ r , E(x ′) = r ′, E(y) = k ⊕ r ′, k is a private input and
r , r ′ are two random variables. Then {E(x), E(y)} and {E(x ′), E(y ′)} are equivalent up to renaming
of random variables, thus, observable sets {x, y} and {x ′, y ′ } have same distribution type.
     Based on this observation, we propose a pattern matching method for inferring distribution
types of observable sets O from observable sets O ′ whose distribution types are known. Before
formalizing this idea, we first introduce type-respecting bijection functions.
     Given a bijective function f : X → X , the function f is type-respecting if for every x ∈ X , f (x)
is public (resp. private and random) iff x is public (resp. private and random).

  Definition 5.6. Two sets of computations E and E ′ are isomorphic respecting the type of variables,
denoted by E ≃ E ′, if there is a type-respecting bijection h : Var(E) → Var(E ′) such that E ′ =
{h(e) | e ∈ E}, where h(e) denotes the computation obtained from e by renaming each variable x
with h(x).

ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
Formal Verification of Higher-Order Masked Arithmetic Programs                                                  111:25


   For two observable sets O and O ′ with the same size, it is easy to see that O and O ′ have the
same distribution type if {E(x) | x ∈ O} ≃ {E(x ′) | x ′ ∈ O ′ }.
   One may notice that constants have to be preserved in the definition of isomorphic with respect
to the type of variables. In general, changing a constant in E may change its distribution type. For
instance, let us consider a family of sets Ei of (simplified) computations taking from the fourth-order
masked implementation of the Sbox [98],
            Ei, j := {x 0 , Sbox(k ⊕ j ⊕ x 0 ) ⊕ r , Sbox(k ⊕ i ⊕ x 0 ) ⊕ r }, for 0 ≤ i , j ≤ 255.
where x 0 and r are two random variables and k is a private input. In this case, for any distinct pairs
of constants (i, j) and (i ′, j ′), Ei, j ≃ Ei ′, j ′ does not hold, thus, we cannot infer the distribution of
Ei, j from Ei ′, j ′ , although they are almost identical.
   To address this issue, we propose a generalization taking into account constants. Our idea is
inspired on the observation that some constant can be assimilated without affecting the distribution
of computations. For instance, regarding k ⊕ j to be k ′, then k ⊕ i ≡ (k ′ ⊕ j) ⊕ i ≡ k ′ ⊕ (j ⊕ i).
Suppose the distribution of E 1,2 is known and by applying k ⊕ i ≡ k ′ ⊕ (j ⊕ i), E 1,2 is normalized as
(note 3 = 1 ⊕ 2)
                           norm(E 1,2 ) := {x 0 , Sbox(k ′ ⊕ x 0 ) ⊕ r , Sbox(k ′ ⊕ 3 ⊕ x 0 ) ⊕ r }.
Then, for any 0 ≤ i , j ≤ 255 such that (j ⊕ i) = 3, by applying k ⊕ i ≡ k ′ ⊕ (j ⊕ i), Ei, j is also
normalized as
                           norm(Ei, j ) := {x 0 , Sbox(k ′ ⊕ x 0 ) ⊕ r , Sbox(k ′ ⊕ 3 ⊕ x 0 ) ⊕ r }.
We can observe that Ei, j ≃ E 1,2 , thus, Ei, j has the same distribution as E 1,2 . This idea is formalized
in the following definition.
   Definition 5.7. A constant c is assimilable in a set E of computations if E can be transformed into
a set E ′ of equivalent computations by algebra laws such that all occurrences of the constant c in E ′
are within the context of x ◦ c for operator ◦ ∈ {⊕, +, −} and some variable x, such that x is either
not used elsewhere or used as x ◦ c ′ for some constant c ′ (note that c , c ′).
  If c is assimilable in E, we denote by norm(E) the set of normalized computations which is
obtained from E ′ by iteratively
  (1) replacing all occurrences of the constant c in E ′ (as x ◦ c) by x, and
  (2) every possible x ◦ c ′ (for c ′ , c) by x◦c ′′, where c ′′ = c ′ b
                                                                       ◦ c, b
                                                                            + = −, b
                                                                                   − = − and b
                                                                                             ⊕ = ⊕.
By this replacement, norm(E) = E [x/(x ◦ c)][∀(x ◦ c ) in E : (x◦c )/(x ◦ c ′)], one can reduce the
                                      ′                   ′       ′         ′′

number of constants in E.
   Example 5.8. Let us consider e = (x ⊕ 1) + (x ⊕ 2) + (y ⊕ 1). The constant 1 is not assimilable
because there are two occurrences of 1 which are within two different contexts x ⊕ 1 and y ⊕ 1
respectively. However, 2 is assimilable (by x), as 2 occurs in the context of x ⊕ 2 and x occurs
elsewhere in x ⊕ 1. After replacing x ⊕ 2 by x and x ⊕ 1 by x ⊕ 3, we get (x ⊕ 3) + x + (y ⊕ 1) in
which 1 becomes assimilable by y. Finally, norm(E) = (x ⊕ 3) + x + y.
  Theorem 5.9. For observable sets O and O ′, if norm({E(x) | x ∈ O}) ≃ norm({E(x) | x ∈ O ′ }),
then O and O ′ have same the distribution types.
  Proof. Let E = {E(x) | x ∈ O} and E ′ = {E(x) | x ∈ O ′ }. Let n be the number of constants
assimilated when computing norm(E) and norm(E ′). We prove by applying induction on n.
• Base case n = 0. Then, norm(E) and norm(E ′) are isomorphic respecting the type of variables. Let
  h : Var(E) → Var(E ′) be the type-respecting bijection, then for every pair (η 1 , η 2 ) ∈ Θ2=X p , there
  exists a pair (η 1′ , η 2′ ) ∈ Θ2=X p such that ηi (x) = ηi′ (h(x)) for all i ∈ {1, 2} and x ∈ (X p ∪X k )∩Var(E).
                                          ′          ′
  Moreover, ⟦P⟧ηO1 = ⟦P⟧ηO2 iff ⟦P⟧ηO′ = ⟦P⟧ηO′ .
                                         1          2


                          ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
111:26                                                                                                            Gao et al.


    For every pair (η 1 , η 2 ) ∈ Θ2=X p , there exists a pair (η 1′ , η 2′ ) ∈ Θ2=X p such that ηi (h −1 (x)) = ηi′ (x) for
                                                                                           ′          ′
  all i ∈ {1, 2} and x ∈ (X p ∪ X k ) ∩ Var(E ′), and ⟦P⟧ηO1 = ⟦P⟧ηO2 iff ⟦P⟧ηO′ = ⟦P⟧ηO′ . Thus, the result
                                                                                      1            2
  immediately follows.
• Inductive set n ≥ 1. Without loss of generation, we assume that c is assimilated by x as x ◦ c in
  E, and x ◦ c 1 , · · · , x ◦ c k are all the occurrences of x with constants c 1 , · · · , x k . Then, for every
  η 1 ∈ Θ, ⟦P⟧ηO1 using E and ⟦P⟧ηO1 [(η1 (x )◦c)/x ] using E[x/(x ◦c)][(x ◦c 1′ )/(x ◦c 1 ), · · · , (x ◦c k′ )/(x ◦c k )]
  have same distribution, where c i′ = c i b       ◦c for all i.
  By symmetry, for every η 2 ∈ Θ, ⟦P⟧η2 using E and ⟦P⟧ηO2 [(η2 (x )◦c)/x ] using E[x/(x ◦c)][(x ◦c 1′ )/(x ◦
                                                 O

  c 1 ), · · · , (x ◦ c k′ )/(x ◦ c k )] have same distribution.
  Therefore, for every (η 1 , η 2 ) ∈ Θ2=X p , ⟦P⟧ηO1 = ⟦P⟧ηO2 using E iff ⟦P⟧ηO1 [(η1 (x )◦c)/x ] = ⟦P⟧ηO2 [(η2 (x )◦c)/x ]
  using E[x/(x ◦ c)][(x ◦ c 1′ )/(x ◦ c 1 ), · · · , (x ◦ c k′ )/(x ◦ c k )]
  By applying the induction hypothesis: for every (η 1 , η 2 ) ∈ Θ2=X p , there exist a pair (η 1′ , η 2′ ) ∈ Θ2=X p
    such that ηi (h −1 (x)) = ηi′ (x) for all i ∈ {1, 2} and x ∈ (X p ∪ X k ) ∩ Var(E ′), and ⟦P⟧ηO1 = ⟦P⟧ηO2
                       ′           ′
    using E iff ⟦P⟧ηO′ = ⟦P⟧ηO′ . Hence, ⟦P⟧ηO1 [(η1 (x )◦c)/x ] = ⟦P⟧ηO2 [(η2 (x )◦c)/x ] using E[x/(x ◦ c)][(x ◦
                        1           2
                                                         ′          ′
    c 1′ )/(x ◦ c 1 ), · · · , (x ◦ c k′ )/(x ◦ c k )] iff ⟦P⟧ηO′ = ⟦P⟧ηO′ . Thus, the result immediately follows.
                                                        1          2
                                                                                                                         □

  Remark that pattern matching based method could be used to match secure sets and for program
debugging. When a new program is just a minor revision of a verified program, this method may
be able to quickly check many observable sets.

6     IMPLEMENTATION AND EVALUATION
We have implemented our methods in a tool HOME. We use Z3 [46] as the underlying SMT solver
(fixed size bit-vector theory) for the SMT-based method. The tool works as follows:
    (1) apply Algorithm 1 to compute the set of potential leaky observable sets;
    (2) for each procedure call Check({Ci, O }(i, O)∈Y ) at Line 14, when the type inference fails to derive
                                   Ð
        any distribution type of (i, O)∈Y Ci, O , check whether there is a recorded set of computations
        E ′ such that norm(E) ≃ norm(E Ð ) via the pattern matching based method, where E is the set
                                           ′

        of computations {E(x) | x (i, O)∈Y Ci, O } after transformations (e.g., SimplyAlg , SimplyDom
        and SimplyCol ), if E ′ exists, then returns the distribution type of E ′;
    (3) if E ′ does not exist, apply mode-counting methods to the set E and record E with its corre-
        sponding distribution type for later pattern matching.
Finally, PLS contains exactly the set of leaky observable sets. Note that we do not apply pattern
matching and model-counting based methods to observable sets whose size is greater than the
security order d for efficiency consideration.
   The experiments were conducted on arithmetic programs over the byte domain. We used a server
with 64-bit Ubuntu 16.04.4 LTS, Intel Xeon CPU E5-2690v4, 2.6GHz and 256GB RAM (only one core
is used in our computation). For GPU based algorithms, we use NVIDIA GeForce GTX 1080 with
compute capability 6.1, as mentioned in Section 5.3.

6.1      Evaluation on Higher-Order Masking
We evaluate our methods on implementations of masked arithmetic algorithms, ranging from
multiplication algorithms to (round-reduced or full) AES/MAC-Keccak. Some of them are provided
by authors of [6], while the others are implemented according to the published masked algorithms.

ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
Formal Verification of Higher-Order Masked Arithmetic Programs                                                  111:27


   The results of our type inference (Algorithm 1 without applying model-counting and pattern
matching based methods) are presented in Table 1. Column 1 shows the reference and description
of the program, where A2B and B2A denote the implementations of conversion algorithms from
Boolean to arithmetic masking and arithmetic to Boolean masking respectively, SecH and SecR
denote the implementations of the non-linear transformation and the round function of Simon [101],
and DOM AND is a GF (28 ) version from [63]. Columns 2-7 show the statistics of Algorithm 1,
including the numbers of potential leaky observable sets, tuples that should be considered with
respect to masking order d (i.e., all non-empty subsets of X o with size ≤ d) in order to compare
with the tool of [6], sets actually checked by Algorithm 1, sets whose verification involves the
SimplyDom and SimplyCol transformations, and verification time (excluding program parsing). Like-
wise, Columns 8–11 show the results reported in [6], the unique sound (but incomplete) approach
that is able to automatically verify masked implementations of higher-order arithmetic programs
under an equivalent leakage model of the ISW model. Since the tool of [6] is unavailable, in Columns
8–11, we simply replicate the statistics of the BBDFGS algorithm from the paper [6] when it is
available (N/A is marked otherwise). Recall that [6] used a different experimental setup: a headless
VM with a dual core 64-bit processor clocked at 2GHz (only one core is used in the computation).
Note that Sbox [98] under fourth-order masking is verified under third-order security only in order
to compare with [6], while other benchmarks are verified under their masking orders.
Results on common benchmarks. All the programs not marked as N/A in Columns 8–11 are
provided by the authors of [6]. We only did necessary pre-processing, e.g., transformed them into
SSA form. Because of this, from Columns 3 and 9 (i.e., ♯Tuples), one can see that we considered
more tuples in several benchmarks (e.g., Full AES (4) [44], Full MAC-Keccak [6], Sbox [96], Key
schedule [96], Sbox (4) [44], Sbox (5) [44]) than [6], namely, we considered more observable variables
than [6].
   From the experimental results, we can observe that there are two benchmarks (i.e., Sbox [96]
under second-order masking and Sbox [98] under fourth-order masking) which have potential
leaky observable sets, and Algorithm 1 produces the same number as [6]. This demonstrates that
Algorithm 1 is at least as precise as the one in [6]. We will report in Section 6.2 the results of
resolving these potential leaky observable sets using our model-counting and pattern matching
methods.
   From Columns 4 and 10 (i.e., ♯Sets), one can observe that the number of observable sets actually
verified by Algorithm 1 is less than the one in [6] on all the common benchmarks (despite there are
more observable variables to be considered in several benchmarks). The differences are noticeable
on several benchmarks (e.g., Full AES (4), Full Keccak, Sbox, Multiplication, Sbox [44, 96] and Key
schedule). Reducing the number of verified observable sets allows us to verify 5th-order Sbox
(4) [44] which has not been done in [6]. Furthermore, from Columns 7 and 11 (i.e., Time), we
observe that Algorithm 1 is faster than [6] on almost all the benchmarks, and the improvement is
significant on larger benchmarks (e.g., 110X, 64X and 31X speed-up for Key schedule, Full AES (4)
and 4th-order Sbox [98]). These results demonstrate that our type inference algorithm is superior
to the one in [6]. Furthermore, the algorithm presented in [6] has an issue which may miss the
verification of some observable sets. (We have informed some authors of [6].)

Results on new benchmarks. All the programs marked as N/A are new benchmarks. We note
that B2A [38] in Common Lisp has been semi-automatically verified under the ISW model by
Coron [39], the AES implementation [44] including Sbox (4) has been semi-automatically proved
under the d-NI model [7]. Some of the first-order A2B and B2A (except A2B [41]) have been verified
in [55]. All the other higher-order benchmarks have not been verified by computer-aided tools.

                          ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
111:28                                                                                                                        Gao et al.


                         Table 1. Experimental results of type inference on masked programs.

                                                       HOME                                                     [6]
   Description
                       Result       ♯Tuples         ♯Sets ♯SimplyDom ♯SimplyCol Time (s) Result       ♯Tuples         ♯Sets    Time (s)
                                                            First-Order Masking
 Multiplication [96]     0             13             6           5         0         ≈0       0         13             7         ≈0
    Sbox (4) [44]        0             73            15          14         0         ≈0       0         64             17        ≈0
  Full AES (4) [44]      0           20,060         515          514        0          2       0       17,206         3,342       128
   Full Keccak [6]       0           18,218        2,813        2,813       0         83       0       13,466         5,421       405
      B2A [59]           1             10             4           2         0         ≈0                        N/A
      A2B [59]          37             48            39           1         0        0.15                       N/A
      A2B [42]           0           1,448           14          13         0         ≈0                        N/A
      B2A [42]           0           2,494            2           1         0         ≈0                        N/A
      A2B [41]          45             86            56          12         0         ≈0                        N/A
      B2A [19]           0             19             3           2         0         ≈0                        N/A
      B2A [38]           1             14             4           2         0         ≈0                        N/A
                                                           Second-Order Masking
     Sbox [98]           0          1,188,111      1,285        1,284      256      1.073      0     1,188,111     4,104         1.649
 Multiplication [96]     0             435           52          51         0       0.001      0        435          92          0.001
     Sbox [96]           2            7,503         270          267        0        0.05      2       7,140        866          0.045
 Key schedule [96]       0         31,828,231     475,943      475,942      0       3,087      0     23,041,866   771,263       340,745
      B2A [19]           0            1,653          25          23         0         ≈0                      N/A
      B2A [97]           0             780           15          13         0         ≈0                      N/A
   SecH (2) [101]        0            1,770          14          13         0         ≈0                      N/A
     SecR [101]          0            3,003          25          24         0         ≈0                      N/A
  DOM AND [63]           0             435           46          45         0         ≈0                      N/A
                                                            Third-Order Masking
 Multiplication [96]     0           24,804         713         712         0       0.021      0        24,804      1,410        0.033
   Sbox (4) [44]         0         6,784,540       18,734      18,733       0       2.021      0      4,499,950    33,075        3.894
   Sbox (5) [44]         0         6,209,895       10,470      10,469       0       3.757      0      4,499,950    39,613        5.036
     B2A [42]            0      274,884,292,760       7           6         0        0.11                      N/A
     B2A [19]            0          457,310         816         807         0       0.052                      N/A
     B2A [97]            0           59,640         133         132         0         ≈0                       N/A
  DOM AND [63]           0           23,426         572         571         0         ≈0                       N/A
                                                           Fourth-Order Masking
     Sbox [98]       98,176      4,874,429,560    1,087,630 924,173       821,888    702     98,176 4,874,429,560 35,895,437 22,119
 Multiplication [96]    0          2,024,785        12,845    12,844         0      0.534       0     2,024,785     33,322   1.138
   Sbox (4) [44]        0        3,910,710,930    1,159,295 1,159,294        0       376        0   2,277,036,685 3,343,587   879
     B2A [19]           0         387,278,970       62,570    62,561         0       10.7                      N/A
     B2A [97]           0          6,438,740        1,271     1,270          0       0.11                      N/A
  DOM AND [63]          0          2,024,785        10,626    10,625         0       0.71                      N/A
                                                            Fifth-Order Masking
 Multiplication [96]     0         216,071,394     281,731    281,730       0         15       0    216,071,394 856,147            45
   Sbox (4) [44]         0      2,782,230,535,161 99,996,680 99,996,679     0       49,598                    N/A
     B2A [97]            0         901,289,592      29,926     29,838       0        3.03                     N/A



   From Table 1, we can observe that almost all benchmarks can be proved secure using our type
inference algorithms in a few seconds. The exceptions include B2A [59], A2B [59], A2B [41] and
B2A [38] which respectively have 1, 37, 45 and 1 potential leaky observable set(s). We shall see in
Section 6.2 that these potential leaky observable sets are actually spurious using model-counting.
To our knowledge, it is the first time that these higher-order programs are automatically proved
secure by computer-aided tools. Recall that A2B and B2A are two kinds of conversion algorithms
between arithmetic and Boolean masking. Our tool could be used to verify masked implementations
of cryptographic algorithms that use A2B and/or B2A conversion algorithms.
Usage of the transformations SimplyDom and SimplyCol . Columns 5 and 6 show the number
of sets whose verification involves the transformations SimplyDom and SimplyCol , respectively.

ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
Formal Verification of Higher-Order Masked Arithmetic Programs                                                  111:29


      Table 2. Comparison of three model-counting methods. O.T. denotes run out of time (three hours).

                      Description    Order     ♯CNT     Result     SMT BFEnum             GPU
                        k 3 [96]       1         2        2        96m     0.2s           0.43s
                       k 254 [96]      1         4        4        O.T.    30m           7.03s
                       B2A [59]        1         1        0         17s     2s           0.86s
                       A2B [59]        1         37       0        O.T.    O.T.          33.18s
                       A2B [41]        1         45       0        O.T.    O.T.          160m
                       B2A [38]        1         1        0       1m 35s 10m 59s         3.17s
                       Sbox [96]       2         2       1(1)      O.T.    O.T.          3,600s
                       Sbox [98]       4        766     98176      O.T.    O.T.           323s



We can see that SimplyDom is heavily used, while SimplyCol is used only in one benchmark (i.e.,
second-order and fourth-order Sbox [98]), which allows to prove lots of observable sets (e.g., 256
on second-order Sbox [98]) without invoking model-counting. Moreover, SimplyDom and SimplyCol
and simplify the expressions of the 98,176 potential leaky observable sets for Sbox [98], so that
pattern matching and model-counting methods can be easily applied. Remark that statistics of the
transformation SimplyAlg is not reported, as its complexity is of constant-time and is negligible.

6.2    Comparison of Model-Counting Methods
One important component of our approach is the model-counting method on which we rely to
resolve potential leaky observable sets. As mentioned in Section 1, we consider two baseline
algorithms (based on SMT encoding and brute-force methods) and a novel GPU-accelerated parallel
algorithm. For the sake of evaluation, we carry out experiments only on programs that have
potential leaky observable sets reported by our type inference algorithm (cf. Result in Table 1). We
also implemented two programs for computing k 3 and k 254 , which contain 1 private input variable,
3 and 5 random input variables, respectively. These programs are taken from the first-order secure
exponentiation [96] without the first RefreshMask function.
   Table 2 shows the statistics of the three model-counting methods, with time limited to three hours
per program. Column 1 shows the reference and description of the program. Column 2 shows the
security order. Column 3 (♯CNTs) shows the time of the model-counting method. Column 4 shows
the number of genuine leaky observable sets. Columns 5–7 show the verification time (excluding
the time for type inference algorithm) of the SMT-based, (naïve) brute-force and GPU-accelerated
parallel methods, respectively.
   The resolution shows that all potential leaky observable sets of B2A [59], A2B [59], A2B [41]
and B2A [38] are spurious, while all potential leaky observable sets of Sbox [98] are genuine. On
program Sbox [96], we resolved one of two potential leaky observable sets as a genuine one in 1
hour, but the other set cannot be resolved in 2 hour, which is the only case which was unsuccessful
in our experiments.
   In detail, the GPU-accelerated parallel method significantly outperforms the other two methods
on large programs. In particular, the SMT-based and brute-force methods runs out of time on five
and four programs, respectively. On the small program k 3 , the brute-force method is significantly
faster than the SMT-based one, and is also faster than the GPU-accelerated one. The latter is because
that the GPU-accelerated method synthesizes a GPU program for each expression and the involved
I/O cost is remarkable in small programs. The GPU-accelerated algorithm provides two orders of
magnitude improvements on the program k 254 . A2B [59] has been verified in [55] based on the
oracle provided by the authors. However, it is not always the case that one can find such an oracle
luckily. It runs out of time if we use the SMT-based method or the brute-force method without

                          ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
111:30                                                                                                             Gao et al.


the oracle, while the GPU-accelerated method can verify this program in less than 1 minute. As a
conclusion, when model-counting is concerned, we recommend the GPU-accelerated algorithm.
   For the fourth-order Sbox [98] which is faulty, it only took 4 minutes to automatically resolve all
the 98,176 potential leakage sets as genuine ones. Therefore, our tool is still faster than [6] albeit
it needs to invoke the model-counting method to resolve those sets which cannot be determined
by type inference. It should be emphasized that this was not possible without the patter matching
based method described in Section 5.4. Indeed, we estimate (based on the experiment) that each
set takes approximately 0.5s, and in total they would require approximately 14 hours. Instead,
we identified 766 (255 × 2 + 256) patterns which can be used to handle all 98,176 potential leaky
observable sets. As a result, only 766 times of model-counting are needed, which took less than 7
minutes, i.e., two orders of magnitude faster.
   The 766 patterns are summarized as follows:
   (1) {x 0 , Sbox(k ⊕ x 0 ) ⊕ r , Sbox(k ⊕ i ⊕ x 0 ) ⊕ r };
   (2) {Sbox(k) ⊕ r , Sbox(k ⊕ x 0 ) ⊕ r , Sbox(k ⊕ i ⊕ x 0 ) ⊕ r };
   (3) {x 0 , Sbox(k) ⊕ r , Sbox(k ⊕ x 0 ⊕ j) ⊕ r };
where 0 < i ≤ 255 and 0 ≤ j ≤ 255, x 0 is a random variable, k is a private input, and r is a
random variable which is introduced by our transformations. The family in Item (1) captures 65,280
observable sets, namely, 256 observable sets for each 0 < i ≤ 255, the family in Item (2) captures
32,640 observable sets, namely, 128 observable sets for each 0 < i ≤ 255, and the family in Item (3)
captures 256 observable sets, 1 observable set for each 0 ≤ j ≤ 255.
   Barthe et al. [6] manually analyzed the 98,176 potential leaky observable sets which are sum-
marized by four families. These are similar to our automatically computed patterns except for the
patterns in Item (3), which is {x 0 , y0 , Sbox(k ⊕ x 0 ⊕ j) ⊕ r } with y0 = Sbox(x 0 ) in [6] (note the third
expression is adjusted for sake of presentation). After manually analyzing source code of Sbox [98]
under fourth-order masking, we confirm that our pattern is correct while the pattern in [6] is not
correct. This demonstrates that it is hard to manually examine potential leaky observable sets.

6.3      Comparison with maskVerif
Our tool HOME is designed to tackle arithmetic programs, but it is also interesting to evaluate its
performance on Boolean programs, for which we compare with the latest version of the open source
tool maskVerif [8], which is limited to Boolean programs. To the best of our knowledge, maskVerif
is the only open source tool for verifying higher-order Boolean programs. We experiment on the
largest 6 Boolean programs (P12–P17) from [50] which are one-round versions of the full 24-round
MAC-Keccak [6], together with randomly selected benchmarks from maskVerif.
     In our experiment, maskVerif reported “stack overflow” error on P12–P17. (We have reported
this issue to the developers of maskVerif.) For the sake of experiments, we removed the last 5,000
assignments for each program when testing maskVerif while our tool HOME is still tested on
the whole programs P12–P17. (For the abridged version no “stack overflow” error was reported
from maskVerif.) We also revised DOM AND [63] and DOM Keccak Sbox [64] by introducing the
following extra dummy variables and statements:
        t 1 = r 1 ∧ x; t 2 = (¬r 1 ) ∧ (¬x); t 3 = t 1 ∧ t 2 ; t 4 = t 2 ∧ r 3 ; ... t 18 = t 16 ∧ r 17 ; t 19 = t 17 ∧ r 18 ;
where r 1 –r 17 are fresh random variables, and x denotes a share of a private input variable. Obviously,
t 3 –t 19 are always 0.
     Table 3 presents the results, with time being limited to two hours per program. Column 1 gives
the programs under comparison. Columns 2-3 show the verification time of maskVerif and our
tool respectively. Column 4 gives the number of leaky observable sets. On the programs taken
from maskVerif, maskVerif performs better (up to 5×) than HOME. We note that there is one

ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
Formal Verification of Higher-Order Masked Arithmetic Programs                                                    111:31


                                      Table 3. Comparison with maskVerif.

                                                                 Time (s)
                                Description                                              Result
                                                           maskVerif [8] HOME
                                             First-Order Masking
                              DOM AND [63]                  0.01              0.01          0
                           DOM Keccak Sbox [64]             0.01              0.01          0
                            DOM AES Sbox [63]              0.23               4.52          0
                           TI Fides-192 APN [21]           86.61             139.40         0
                                  P12 [50]                 3,223               2.9          0
                                  P13 [50]             3,257(1,234)           122         4.8k
                                P14-P17 [50]             O.T.(≤12)           72-168    1.6k-17.6k
                                               Second-Order Masking
                            DOM AND [63]                         0.01          0.01         0
                        DOM AND (Revised) [63]                  16.82         0.89          0
                         DOM Keccak Sbox [64]                   0.01           0.05         0
                      DOM Keccak Sbox(Revised) [64]             16.62         1.93          0
                          DOM AES Sbox [61]                     61.59         7,385         0
                                                Third-Order Masking
                            DOM AND [63]                         0.01          0.02         0
                        DOM AND(Revised) [63]                   828.70        6.39          0
                         DOM Keccak Sbox [64]                    0.33          1.26         0
                      DOM Keccak Sbox(Revised) [64]            1,041.67       27.40         0
                                               Fourth-Order Masking
                            DOM AND [63]                        0.13           0.40         0
                        DOM AND(Revised) [63]                    O.T.         77.40         0
                         DOM Keccak Sbox [64]                   16.35         78.13         0
                      DOM Keccak Sbox(Revised) [64]              O.T.        690.79         0




benchmark (second-order) DOM AES Sbox for which maskVerif performs exceptionally well. The
major reason is that an ad hoc rule is used therein but could not be used in HOME because it is
tailored for Boolean programs. It is perhaps worth pointing out that we have identified some bugs
of maskVerif. For instance, when maskVerif verifies DOM AND (under second-order), the leaky
observable set {(k ⊕ r 0 ⊕ r 1 ) ∧ r 2 , r 0 , r 1 , r 2 } where k is private and r 0 , r 1 , r 2 are random variables is
considered secure. This bug has inadvertently reduced the verification time of maskVerif as less
sets of variables need to be examined. (We have reported this issue to the developers of maskVerif.)
   On the programs P12–P17 and revised programs DOM AND [63] and DOM Keccak Sbox [64],
HOME significantly outperforms maskVerif. Specifically, on the secure program P12, HOME
takes 2.9s while maskVerif takes 3,223s on the reduced version. On the insecure program P13,
HOME identified all the flaws of the program in 122s, while maskVerif identified 1,234 flaws of
the reduced version in 3,257s. On the insecure programs P14–P17, HOME identified all the flaws
using at most 168s, while maskVerif runs out of time (2 hours) and identified at most 12 flaws. On
second-/third-order revised programs, HOME is 8.6–130× faster than maskVerif. On fourth-order
revised programs, maskVerif ran out of time.
   In conclusion, even for Boolean programs, HOME demonstrates largely comparable performance
on the benchmarks tested by maskVerif, and indeed considerably better performance on the new
benchmarks.

                           ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
111:32                                                                                           Gao et al.


7   RELATED WORK
In this section, we review related work on masking countermeasures in general, as well as existing
techniques on the analysis of masked programs and the detection/mitigation of other types of
side-channel leaks.
Masking. Boolean and arithmetic masking schemes [17, 24, 29, 53, 59, 69, 82, 83, 87, 94–96, 98, 106]
have been widely investigated in the past two decades with differences in adversary models, mask-
ing schemes, cryptographic algorithms and compactness. Secure conversion algorithms between
Boolean and arithmetic maskings have also been investigated [19, 38, 41, 42, 59, 68, 97]. These
countermeasures and conversion algorithms are often designed manually for specific cryptographic
algorithms. In this context, the common problem is the lack of efficient and effective tools for
automatically proving their correctness [43, 44]. Our work aims to bridge this gap.
Testing. The predominant approach addressing security of (masked) implementations of crypto-
graphic algorithms is the empirical leakage assessment by statistical significance tests or launching
state-of-the-art side-channel attacks [13, 14, 34, 45, 58, 66, 72, 77, 78, 81, 85, 86, 90, 93, 107]. These
approaches are valuable in identifying flaws even without any knowledge of the leakage model,
but can neither prove their absence nor identify all flaws, due to the limitation in measurement
setup and/or explored traces. This paper purses an alternative, formal verification based approach
which is largely complementary to the work based on testing.
Formal Verification. Formal verification approaches, which are able to prove the absence of
side-channel leaks, have been proposed in the prior work [6–8, 16, 18, 22, 23, 25, 39, 50, 51, 55, 56,
84, 88, 104, 110]. However, as we have explained earlier, these existing formal verification methods
are limited in applicability (i.e., Boolean program, stronger leakage model or first-order security
only) and accuracy (i.e., false alarms).
   Early work via type-based proof system refer to [16, 84], which checks if a computation result is
logically dependent of the secret data and, at the same time, logically independent of any random
variable used for masking the secret data. However, these incomplete approaches only support
verification of first-order arithmetic programs and may be even unsound under the ISW model, as
pointed out in [50].
   To improve accuracy, Eldib et al. proposed model-counting based method [50, 51], which is both
sound and complete under the ISW model. This method reduces the verification problem to a series
of satisfiability problems encoding model-counting constraints, which is solved by leveraging SMT
solvers. However, it is limited to the first-order Boolean programs only. Blot et al. extended this
SMT-based method to verify higher-order programs [25]. The SMT-encoding is exponential in the
number of bits of random variables and the number of orders, hence is short of scalability and
limited to Boolean programs only. Our SMT-based method can be seen as an generalization of
these methods. Nevertheless, our GPU-accelerated parallel algorithm significantly outperforms the
SMT-based method.
   To improve efficiency, Barthe et al. introduced the notion of d-NI to characterize security of
masked programs and proposed a sound proof system to verify higher-order masked programs [6].
The d-NI notion was later extended to d-SNI [7] which enables compositional verification. How-
ever, these approaches are incomplete, namely, it may produce spurious leaky observable sets.
Furthermore, as mentioned in Section 6.1, these approaches may miss the verification of some
observable sets. In this direction, Bisi et al. [22] proposed a technique for verifying higher-order
masking, which was limited to Boolean programs with linear operations only. Ouahma et al. gen-
eralized the approach of [6] to verify assembly-level code [88], but is incomplete and limited to
first-order programs only. Coron [39] proposed two complementary semi-automatic approaches
via elementary circuit transforms, and showed how to generate security proofs automatically, for

ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
Formal Verification of Higher-Order Masked Arithmetic Programs                                                  111:33


simple circuits, but are also incomplete. Barthe et al. developed a unified framework maskVerif [8]
for both software and hardware implementations taking into account glitch and transitions into
account, but is limited to Boolean programs only and their tool missed the verification of some
observable sets in our experiments.
   As a matter of fact, the most efficient masked programs do not achieve d-SNI directly, as mentioned
by Bloem et al. [23]. Thus, Bloem et al. proposed a sound approach [23] via Fourier analysis, which
considers the Fourier expansion of the Boolean functions and reduces the verification to checking
whether certain coefficients of the Fourier expansion are zero or not [23]. They studied the security
problem of Boolean programs/hardware circuits in the d-threshold probing model [69] and its
extension with glitches for any given d. The verification problem is solved by leveraging SAT solvers.
However, they considered Boolean programs/hardware circuits only. Furthermore, it was shown
by Barthe et al. [8] that maskVerif outperforms [23]. Belaïd et al. proposed another compositional
verification approach in [18] to overcome the limitation of d-SNI [7], but can only verify Boolean
programs composed of ISW multiplication functions, sharewise addition functions and d-SNI
refresh functions.
   In our prior work [55, 56, 110], we have proposed gradual refinement based approaches for
verifying masked Boolean and arithmetic programs respectively, which integrate the semantic type
system and model-counting based methods hence bring the best of both worlds. This semantic type
system was leveraged by Wang et al. [104] to identify transition-based flaws. All these approaches
are limited to first-order security only. It is challenging to generalize these approaches to higher-
order masked arithmetic program, which is addressed by the current work.
   Compared to the above existing formal verification approaches, the current work studies formal
verification of arithmetic programs against d-threshold probing model for any given d. Both our
type system and model-counting based method significantly improve the applicability and efficiency.
Our pattern matching based method is novel and effective at reducing the cost of model-counting
and summarizing patterns of leaky observable sets which can be used for diagnosis and debugging.
Putting them together, our hybrid formal verification approach goes significantly beyond the
state-of-the-art in terms of applicability, accuracy and efficiency.

Automated mitigation of power side-channel flaws. Automated mitigation techniques have
been proposed to repair power side-channel flaws [1, 7, 15, 25, 49, 84, 103, 104]. For example,
techniques proposed in [1, 7, 15, 84] rely on compiler-like pattern matching, whereas the ones
proposed in [25, 49, 103] use inductive program synthesis and the one in [104] constraints register
allocation. All these works either rely upon existing formal verification techniques, hence have
similar limitations as described above, or do not use formal verification techniques, thus, correctness
can not be guaranteed. It would be interesting to investigate whether our new approach can aid in
the mitigation of power side-channel flaws, effectively making countermeasures better, as done
in [25, 49].

Other types of side channels. In addition to power side-channel attacks, there are other types
of side-channel attacks against cryptographic programs, where the side channels can be in the
form of, e.g., CPU time, faults and cache behaviors. Techniques for verification and mitigation of
these types of side-channel attacks have been studied in the literature, such as [2, 3, 5, 28, 35, 73,
91, 92, 108, 109] for timing side-channel attacks, [11, 12, 32, 33, 36, 47, 60, 65, 75, 100, 105, 108] for
cache side-channel attacks and [10, 20, 26, 27, 52, 67] for fault attacks. Each type of side-channel
has unique characteristics, which usually requires specific verification techniques, so these results
are orthogonal to our work.


                          ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
111:34                                                                                                           Gao et al.


8   CONCLUSION
In this work, we have proposed a hybrid formal verification approach for higher-order masked
arithmetic programs. The approach comprise a sound proof system equipped with an efficient
algorithm for type inference which significantly outperforms the approach [6] for arithmetic
programs, as well as novel model-counting and pattern matching based methods for resolving
potential leaky observable sets automatically that cannot be accomplished by the existing tools.
Experimental results show that our approach is not only significantly faster but also is applicable
to more cryptographic implementations that could not be proved secure automatically before.
   Future work includes extending our methods to verifying programs with inherent branching
and loops, and/or under other leakage models such as d-NI/SNI, d-threshold probing model, as well
as their extensions with glitches and transitions as done in [8, 23]

REFERENCES
  [1] Giovanni Agosta, Alessandro Barenghi, and Gerardo Pelosi. 2012. A code morphing methodology to automate power
      analysis countermeasures. In Proceedings of the 49th Annual Design Automation Conference. 77–82.
  [2] José Bacelar Almeida, Manuel Barbosa, Gilles Barthe, François Dupressoir, and Michael Emmi. 2016. Verifying
      Constant-Time Implementations. In Proceedings of the 25th USENIX Security Symposium. 53–70.
  [3] Timos Antonopoulos, Paul Gazzillo, Michael Hicks, Eric Koskinen, Tachio Terauchi, and Shiyi Wei. 2017. Decomposi-
      tion instead of self-composition for proving the absence of timing channels. In Proceedings of the 38th ACM SIGPLAN
      Conference on Programming Language Design and Implementation. 362–375.
  [4] Victor Arribas, Svetla Nikova, and Vincent Rijmen. 2018. VerMI: Verification Tool for Masked Implementations. In
      Proceedings of the 25th IEEE International Conference on Electronics, Circuits and Systems. 381–384.
  [5] Lucas Bang, Abdulbaki Aydin, Quoc-Sang Phan, Corina S. Pasareanu, and Tevfik Bultan. 2016. String analysis for side
      channels with segmented oracles. In Proceedings of the 24th ACM SIGSOFT International Symposium on Foundations of
      Software Engineering. 193–204.
  [6] Gilles Barthe, Sonia Belaïd, François Dupressoir, Pierre-Alain Fouque, Benjamin Grégoire, and Pierre-Yves Strub. 2015.
      Verified Proofs of Higher-Order Masking. In Proceedings of the 34th Annual International Conference on the Theory
      and Applications of Cryptographic Techniques. 457–485.
  [7] Gilles Barthe, Sonia Belaïd, François Dupressoir, Pierre-Alain Fouque, Benjamin Grégoire, Pierre-Yves Strub, and
      Rébecca Zucchini. 2016. Strong Non-Interference and Type-Directed Higher-Order Masking. In Proceedings of the
      2016 ACM SIGSAC Conference on Computer and Communications Security. 116–129.
  [8] Gilles Barthe, Sonia Belaïd, Pierre-Alain Fouque, and Benjamin Grégoire. 2019. maskVerif: Automated Verification of
      Higher-Order Masking in Presence of Physical Defaults. In Proceedings of the 24th European Symposium on Research
      in Computer Security. 300–318.
  [9] Gilles Barthe, François Dupressoir, Sebastian Faust, Benjamin Grégoire, François-Xavier Standaert, and Pierre-Yves
      Strub. 2017. Parallel Implementations of Masking Schemes and the Bounded Moment Leakage Model. In Proceedings
      of the 36th Annual International Conference on the Theory and Applications of Cryptographic Techniques. 535–566.
 [10] Gilles Barthe, François Dupressoir, Pierre-Alain Fouque, Benjamin Grégoire, and Jean-Christophe Zapalowicz. 2014.
      Synthesis of Fault Attacks on Cryptographic Implementations. In Proceedings of the 2014 ACM SIGSAC Conference on
      Computer and Communications Security. 1016–1027.
 [11] Gilles Barthe, Boris Köpf, Laurent Mauborgne, and Martín Ochoa. 2014. Leakage Resilience against Concurrent Cache
      Attacks. In Proceedings of the 3rd International Conference on Principles of Security and Trust. 140–158.
 [12] Tiyash Basu, Kartik Aggarwal, Chundong Wang, and Sudipta Chattopadhyay. 2020. An exploration of effective
      fuzzing for side-channel cache leakage. Software Testing, Verification & Reliability 30, 1 (2020).
 [13] Lejla Batina, Lukasz Chmielewski, Louiza Papachristodoulou, Peter Schwabe, and Michael Tunstall. 2019. Online
      Template Attacks. Journal of Cryptographic Engineering 9, 1 (2019), 21–36.
 [14] Lejla Batina, Jip Hogenboom, and Jasper G. J. van Woudenberg. 2012. Getting More from PCA: First Results of Using
      Principal Component Analysis for Extensive Power Analysis. In Proceedings of the RSA Conference Cryptographers’
      Track. 383–397.
 [15] Ali Galip Bayrak, Francesco Regazzoni, Philip Brisk, François-Xavier Standaert, and Paolo Ienne. 2011. A first step
      towards automatic application of power analysis countermeasures. In ACM/IEEE Design Automation Conference.
      230–235.
 [16] Ali Galip Bayrak, Francesco Regazzoni, David Novo, and Paolo Ienne. 2013. Sleuth: Automated Verification of Software
      Power Analysis Countermeasures. In Proceedings of the 15th International Workshop on Cryptographic Hardware and


ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
Formal Verification of Higher-Order Masked Arithmetic Programs                                                         111:35


      Embedded Systems. 293–310.
 [17] Sonia Belaïd, Fabrice Benhamouda, Alain Passelègue, Emmanuel Prouff, Adrian Thillard, and Damien Vergnaud.
      2017. Private Multiplication over Finite Fields. In Proceedings of the 37th Annual International Cryptology Conference.
      397–426.
 [18] Sonia Belaïd, Dahmun Goudarzi, and Matthieu Rivain. 2018. Tight Private Circuits: Achieving Probing Security with
      the Least Refreshing. In Proceedings of the 24th International Conference on the Theory and Application of Cryptology
      and Information Security. 343–372.
 [19] Luk Bettale, Jean-Sébastien Coron, and Rina Zeitoun. 2018. Improved High-Order Conversion From Boolean to
      Arithmetic Masking. IACR Transactions on Cryptographic Hardware and Embedded Systems 2 (2018), 22–45.
 [20] Eli Biham and Adi Shamir. 1997. Differential Fault Analysis of Secret Key Cryptosystems. In CRYPTO. 513–525.
 [21] Begül Bilgin, Andrey Bogdanov, Miroslav Knezevic, Florian Mendel, and Qingju Wang. 2013. Fides: Lightweight
      Authenticated Cipher with Side-Channel Resistance for Constrained Hardware. In Proceedings of the 15th International
      Workshop on Cryptographic Hardware and Embedded Systems. 142–158.
 [22] Elia Bisi, Filippo Melzani, and Vittorio Zaccaria. 2017. Symbolic Analysis of Higher-Order Side Channel Countermea-
      sures. IEEE Transactions on Computers 66, 6 (2017), 1099–1105.
 [23] Roderick Bloem, Hannes Groß, Rinat Iusupov, Bettina Könighofer, Stefan Mangard, and Johannes Winter. 2018.
      Formal Verification of Masked Hardware Implementations in the Presence of Glitches. In Proceedings of the 37th
      Annual International Conference on the Theory and Applications of Cryptographic Techniques. 321–353.
 [24] Johannes Blömer, Jorge Guajardo, and Volker Krummel. 2004. Provably secure masking of AES. In Proceedings of the
      International Workshop on Selected Areas in Cryptography. 69–83.
 [25] Arthur Blot, Masaki Yamamoto, and Tachio Terauchi. 2017. Compositional Synthesis of Leakage Resilient Programs.
      In Proceedings of the 6th International Conference on Principles of Security and Trust. 277–297.
 [26] Jakub Breier, Xiaolu Hou, and Yang Liu. 2018. Fault Attacks Made Easy: Differential Fault Analysis Automation on
      Assembly Code. IACR Transactions on Cryptographic Hardware and Embedded Systems 2018, 2 (2018), 96–122.
 [27] J. Breier, X. Hou, and Y. Liu. 2019. On Evaluating Fault Resilient Encoding Schemes in Software. IEEE Transactions on
      Dependable and Secure Computing (2019), 1–14.
 [28] Tegan Brennan, Seemanta Saha, Tevfik Bultan, and Corina S. Pasareanu. 2018. Symbolic path cost analysis for
      side-channel detection. In Proceedings of the 27th ACM SIGSOFT International Symposium on Software Testing and
      Analysis. 27–37.
 [29] D. Canright and Lejla Batina. 2008. A Very Compact "Perfectly Masked" S-Box for AES. In Proceedings of the 6th
      International Conference on Applied Cryptography and Network Security. 446–459.
 [30] Claude Carlet, Louis Goubin, Emmanuel Prouff, Michaël Quisquater, and Matthieu Rivain. 2012. Higher-Order
      Masking Schemes for S-Boxes. In Proceedings of the 19th International Workshop Fast Software Encryption. 366–384.
 [31] Suresh Chari, Josyula R. Rao, and Pankaj Rohatgi. 2002. Template Attacks. In roceedings of the 4th International
      Workshop on Cryptographic Hardware and Embedded Systems. 13–28.
 [32] Sudipta Chattopadhyay, Moritz Beck, Ahmed Rezine, and Andreas Zeller. 2019. Quantifying the Information Leakage
      in Cache Attacks via Symbolic Execution. ACM Transactions on Embedded Computing Systems 18, 1 (2019), 7:1–7:27.
 [33] Sudipta Chattopadhyay and Abhik Roychoudhury. 2018. Symbolic Verification of Cache Side-Channel Freedom. IEEE
      Trans. on CAD of Integrated Circuits and Systems 37, 11 (2018), 2812–2823.
 [34] Ricardo Chaves, Lukasz Chmielewski, Francesco Regazzoni, and Lejla Batina. 2018. SCA-Resistance for AES: How
      Cheap Can We Go?. In Proceedings of the 10th International Conference on Cryptology in Africa. 107–123.
 [35] Jia Chen, Yu Feng, and Isil Dillig. 2017. Precise Detection of Side-Channel Vulnerabilities using Quantitative Cartesian
      Hoare Logic. In Proceedings of the 2017 ACM SIGSAC Conference on Computer and Communications Security. 875–890.
 [36] Duc-Hiep Chu, Joxan Jaffar, and Rasool Maghareh. 2016. Precise Cache Timing Analysis via Symbolic Execution. In
      Proceedings of the IEEE Symposium on Real-Time and Embedded Technology and Applications. 293–304.
 [37] Scott Contini, Ronald L. Rivest, Matthew J. B. Robshaw, and Yiqun Lisa Yin. 1999. Improved Analysis of Some
      Simplified Variants of RC6. In Proceedings of the 6th International Workshop on Fast Software Encryption. 1–15.
 [38] Jean-Sébastien Coron. 2017. High-Order Conversion from Boolean to Arithmetic Masking. In Proceedings of the 19th
      International Conference on Cryptographic Hardware and Embedded Systems. 93–114.
 [39] Jean-Sébastien Coron. 2018. Formal Verification of Side-Channel Countermeasures via Elementary Circuit Transfor-
      mations. In Proceedings of the 16th International Conference on Applied Cryptography and Network Security. 65–82.
 [40] Jean-Sébastien Coron, Christophe Giraud, Emmanuel Prouff, Soline Renner, Matthieu Rivain, and Praveen Kumar
      Vadnala. 2012. Conversion of Security Proofs from One Leakage Model to Another: A New Issue. In Proceedings of the
      3rd International Workshop on Constructive Side-Channel Analysis and Secure Design. 69–81.
 [41] Jean-Sébastien Coron, Johann Großschädl, Mehdi Tibouchi, and Praveen Kumar Vadnala. 2015. Conversion from
      Arithmetic to Boolean Masking with Logarithmic Complexity. In Proceedings of the 22nd International Workshop on
      Fast Software Encryption. 130–149.


                            ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
111:36                                                                                                          Gao et al.


 [42] Jean-Sébastien Coron, Johann Großschädl, and Praveen Kumar Vadnala. 2014. Secure Conversion between Boolean
      and Arithmetic Masking of Any Order. In Proceedings of the 16th International Workshop on Cryptographic Hardware
      and Embedded Systems. 188–205.
 [43] Jean-Sébastien Coron, Emmanuel Prouff, and Matthieu Rivain. 2007. Side Channel Cryptanalysis of a Higher Order
      Masking Scheme. In Proceedings of the 9th International Workshop on Cryptographic Hardware and Embedded Systems.
      28–44.
 [44] Jean-Sébastien Coron, Emmanuel Prouff, Matthieu Rivain, and Thomas Roche. 2013. Higher-Order Side Channel
      Security and Mask Refreshing. In Proceedings of the 20th International Workshop on Fast Software Encryption. 410–424.
 [45] Jean DaRolt, Amitabh Das, Santosh Ghosh, Giorgio Di Natale, Marie-Lise Flottes, Bruno Rouzeyre, and Ingrid
      Verbauwhede. 2012. Scan Attacks on Side-Channel and Fault Attack Resistant Public-Key Implementations. Journal
      of Cryptographic Engineering 2, 4 (2012), 207–219.
 [46] Leonardo Mendonça de Moura and Nikolaj Bjørner. 2008. Z3: An Efficient SMT Solver. In Proceedings of the 14th
      International Conference on Tools and Algorithms for the Construction and Analysis of Systems. 337–340.
 [47] Goran Doychev, Boris Köpf, Laurent Mauborgne, and Jan Reineke. 2015. CacheAudit: A Tool for the Static Analysis
      of Cache Side Channels. ACM Transactions on Information and System Security 18, 1 (2015), 4:1–4:32.
 [48] Alexandre Duc, Stefan Dziembowski, and Sebastian Faust. 2019. Unifying Leakage Models: From Probing Attacks to
      Noisy Leakage. Journal of Cryptology 32, 1 (2019), 151–177.
 [49] Hassan Eldib and Chao Wang. 2014. Synthesis of Masking Countermeasures against Side Channel Attacks. In
      Proceedings of the 26th International Conference on Computer Aided Verification. 114–130.
 [50] Hassan Eldib, Chao Wang, and Patrick Schaumont. 2014. Formal Verification Of Software Countermeasures against
      Side-Channel Attacks. ACM Transactions on Software Engineering and Methodology 24, 2 (2014), 11.
 [51] Hassan Eldib, Chao Wang, and Patrick Schaumont. 2014. SMT-Based Verification of Software Countermeasures
      against Side-Channel Attacks. In Proceedings of the 20th International Conference on Tools and Algorithms for the
      Construction and Analysis of Systems. 62–77.
 [52] Hassan Eldib, Meng Wu, and Chao Wang. 2016. Synthesis of Fault-Attack Countermeasures for Cryptographic
      Circuits. In Proceedings of the 28th International Conference Computer Aided Verification. 343–363.
 [53] Sebastian Faust, Vincent Grosso, Santos Merino Del Pozo, Clara Paglialonga, and François-Xavier Standaert. 2017.
      Composable Masking Schemes in the Presence of Physical Defaults and the Robust Probing Model. IACR Cryptology
      ePrint Archive 2017 (2017), 711.
 [54] Sebastian Faust, Vincent Grosso, Santos Merino Del Pozo, Clara Paglialonga, and François-Xavier Standaert. 2018.
      Composable Masking Schemes in the Presence of Physical Defaults & the Robust Probing Model. IACR Transactions
      on Cryptographic Hardware and Embedded Systems 3 (2018), 89–120.
 [55] Pengfei Gao, Hongyi Xie, Jun Zhang, Fu Song, and Taolue Chen. 2019. Quantitative Verification of Masked Arithmetic
      Programs Against Side-Channel Attacks. In Proceedings of the 25th International Conference on Tools and Algorithms
      for the Construction and Analysis of Systems. 155–173.
 [56] Pengfei Gao, Jun Zhang, Fu Song, and Chao Wang. 2019. Verifying and Quantifying Side-channel Resistance of
      Masked Software Implementations. ACM Trans. Softw. Eng. Methodol. 28, 3 (2019), 16:1–16:32.
 [57] Daniel Genkin, Adi Shamir, and Eran Tromer. 2017. Acoustic Cryptanalysis. Journal of Cryptology 30, 2 (2017),
      392–443.
 [58] Gilbert Goodwill, Benjamin Jun, Josh Jaffe, and Pankaj Rohatgi. 2011. A Testing Methodology for Side Channel
      Resistance Validation. In NIST non-invasive attack testing workshop.
 [59] Louis Goubin. 2001. A Sound Method for Switching between Boolean and Arithmetic Masking. In Proceedings of the
      3rd International Workshop on Cryptographic Hardware and Embedded Systems. 3–15.
 [60] Philipp Grabher, Johann Großschädl, and Dan Page. 2007. Cryptographic Side-Channels from Low-Power Cache
      Memory. In Proceedings of the 11th IMA International Conference on Cryptography and Coding. 170–184.
 [61] Hannes Groß, Martin Krenn, and Stefan Mangard. 2018. Second and Third Order Verilog Implementations of AES
      S-box.
 [62] Hannes Groß and Stefan Mangard. 2018. A Unified Masking Approach. Journal of Cryptographic Engineering 8, 2
      (2018), 109–124.
 [63] Hannes Groß, Stefan Mangard, and Thomas Korak. 2017. An Efficient Side-Channel Protected AES Implementation
      with Arbitrary Protection Order. In Proceedings of the RSA Conference Cryptographers’ Track. 95–112.
 [64] Hannes Groß, David Schaffenrath, and Stefan Mangard. 2017. Higher-Order Side-Channel Protected Implementations
      of KECCAK. In Proceedings of the Euromicro Conference on Digital System Design. 205–212.
 [65] Shengjian Guo, Meng Wu, and Chao Wang. 2018. Adversarial Symbolic Execution for Detecting Concurrency-related
      Cache Timing Leaks. In Proceedings of the 2018 ACM Joint Meeting on European Software Engineering Conference and
      Symposium on the Foundations of Software Engineering. 377–388.



ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
Formal Verification of Higher-Order Masked Arithmetic Programs                                                      111:37


 [66] Gabriel Hospodar, Benedikt Gierlichs, Elke De Mulder, Ingrid Verbauwhede, and Joos Vandewalle. 2011. Machine
      learning in side-channel analysis: a first study. Journal of Cryptographic Engineering 1, 4 (2011), 293–302.
 [67] Xiaolu Hou, Jakub Breier, Fuyuan Zhang, and Yang Liu. 2019. Fully Automated Differential Fault Analysis on Software
      Implementations of Block Ciphers. IACR Transactions on Cryptographic Hardware and Embedded Systems 2019, 3
      (2019), 1–29.
 [68] Michael Hutter and Michael Tunstall. 2019. Constant-Time Higher-Order Boolean-To-Arithmetic Masking. Journal of
      Cryptographic Engineering 9, 2 (2019), 173–184.
 [69] Yuval Ishai, Amit Sahai, and David A. Wagner. 2003. Private Circuits: Securing Hardware against Probing Attacks. In
      Proceedings of the 23rd Annual International Cryptology Conference. 463–481.
 [70] Anja F. Karl, Robert Schilling, Roderick Bloem, and Stefan Mangard. 2019. Small Faults Grow Up - Verification of
      Error Masking Robustness in Arithmetically Encoded Programs. In Proceedings of the 20th International Conference on
      Verification, Model Checking, and Abstract Interpretation. 183–204.
 [71] HeeSeok Kim, Seokhie Hong, and Jongin Lim. 2011. A Fast and Provably Secure Higher-Order Masking of AES S-Box.
      In Proceedings of the 13th International Workshop on Cryptographic Hardware and Embedded Systems. 95–107.
 [72] Yongdae Kim and Haengseok Ko. 2013. Using Principal Component Analysis for Practical Biasing of Power Traces
      to Improve Power Analysis Attacks. In Proceedings of the 16th International Conference on Information Security and
      Cryptology. 109–120.
 [73] Paul C. Kocher. 1996. Timing Attacks on Implementations of Diffie-Hellman, RSA, DSS, and Other Systems. In
      Proceedings of the 16th Annual International Cryptology Conference. 104–113.
 [74] Paul C. Kocher, Joshua Jaffe, and Benjamin Jun. 1999. Differential Power Analysis. In Proceedings of the 19th Annual
      International Cryptology Conference. 388–397.
 [75] Boris Köpf, Laurent Mauborgne, and Martín Ochoa. 2012. Automatic quantification of cache side-channels. In
      International Conference on Computer Aided Verification. 564–580.
 [76] Xuejia Lai and James L. Massey. 1990. A Proposal for a New Block Encryption Standard. In Proceedings of the Workshop
      on the Theory and Application of of Cryptographic Techniques. 389–404.
 [77] Rauf Mahmudlu, Valentina Banciu, Lejla Batina, and Ileana Buhan. 2016. LDA-Based Clustering as a Side-Channel
      Distinguisher. In Proceedings of the 12th International Workshop on Radio Frequency Identification and IoT Security.
      62–75.
 [78] Stefan Mangard. 2004. Hardware Countermeasures against DPA ? A Statistical Analysis of Their Effectiveness. In
      Proceedings of the RSA Conference Cryptographers’ Track. 222–235.
 [79] Stefan Mangard, Elisabeth Oswald, and Thomas Popp. 2007. Power Analysis Attacks - Revealing the Secrets of Smart
      Cards. Springer.
 [80] Stefan Mangard, Norbert Pramstaller, and Elisabeth Oswald. 2005. Successfully Attacking Masked AES Hardware
      Implementations. In Proceedings of the 7th International Workshop on Cryptographic Hardware and Embedded Systems.
      157–171.
 [81] Dimitrios Mavroeidis, Lejla Batina, Twan van Laarhoven, and Elena Marchiori. 2012. PCA, Eigenvector Localization
      and Clustering for Side-Channel Attacks on Cryptographic Hardware Devices. In Proceedings of the European
      Conference on Machine Learning and Knowledge Discovery in Databases. 253–268.
 [82] Thomas S. Messerges. 2000. Securing the AES Finalists Against Power Analysis Attacks. In Proceedings of the 7th
      International Workshop on Fast Software Encryption. 150–164.
 [83] Amir Moradi, Axel Poschmann, San Ling, Christof Paar, and Huaxiong Wang. 2011. Pushing the Limits: A Very
      Compact and a Threshold Implementation of AES. In Proceedings of the 30th Annual International Conference on the
      Theory and Applications of Cryptographic Techniques. 69–88.
 [84] Andrew Moss, Elisabeth Oswald, Dan Page, and Michael Tunstall. 2012. Compiler Assisted Masking. In Proceedings of
      the 14th International Workshop on Cryptographic Hardware and Embedded Systems. 58–75.
 [85] Yossef Oren, Ofir Weisse, and Avishai Wool. 2014. A New Framework for Constraint-Based Probabilistic Template
      Side Channel Attacks. In Proceedings of the 16th International Workshop on Cryptographic Hardware and Embedded
      Systems. 17–34.
 [86] Yossef Oren and Avishai Wool. 2016. Side-channel Cryptographic Attacks using Pseudo-Boolean Optimization.
      Constraints 21, 4 (2016), 616–645.
 [87] Elisabeth Oswald, Stefan Mangard, Norbert Pramstaller, and Vincent Rijmen. 2005. A Side-Channel Analysis Resistant
      Description of the AES S-Box. In Proceedings of the 12th International Workshop on Fast Software Encryption. 413–423.
 [88] Inès Ben El Ouahma, Quentin Meunier, Karine Heydemann, and Emmanuelle Encrenaz. 2017. Symbolic Approach for
      Side-Channel Resistance Analysis of Masked Assembly Codes. In Proceedings of the 6th International Workshop on
      Security Proofs for Embedded Systems.
 [89] Inès Ben El Ouahma, Quentin L. Meunier, Karine Heydemann, and Emmanuelle Encrenaz. 2019. Side-channel
      robustness analysis of masked assembly codes using a symbolic approach. Journal of Cryptographic Engineering 9, 3


                            ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
111:38                                                                                                         Gao et al.


      (2019), 231–242.
 [90] Elif Ozgen, Louiza Papachristodoulou, and Lejla Batina. 2016. Template attacks using classification algorithms. In
      Proceedings of the IEEE International Symposium on Hardware Oriented Security and Trust. 242–247.
 [91] Corina S. Pasareanu, Quoc-Sang Phan, and Pasquale Malacaria. [n.d.]. Multi-run Side-Channel Analysis Using
      Symbolic Execution and Max-SMT. In Proceedings of the 29th IEEE Computer Security Foundations Symposium, pages =
      387–400, year = 2016.
 [92] Quoc-Sang Phan, Lucas Bang, Corina S. Pasareanu, Pasquale Malacaria, and Tevfik Bultan. 2017. Synthesis of Adaptive
      Side-Channel Attacks. In Proceedings of the 30th IEEE Computer Security Foundations Symposium. 328–342.
 [93] Stjepan Picek, Kostas Papagiannopoulos, Baris Ege, Lejla Batina, and Domagoj Jakobovic. 2014. Confused by Confusion:
      Systematic Evaluation of DPA Resistance of Various S-boxes. In Proceedings of the 15th International Conference on
      Cryptology in India. 374–390.
 [94] Emmanuel Prouff and Matthieu Rivain. 2013. Masking against Side-Channel Attacks: A Formal Security Proof. In
      Proceedings of the 32nd Annual International Conference on the Theory and Applications of Cryptographic Techniques.
      142–159.
 [95] Oscar Reparaz, Begül Bilgin, Svetla Nikova, Benedikt Gierlichs, and Ingrid Verbauwhede. 2015. Consolidating Masking
      Schemes. In Proceedings of the 35th Annual Cryptology Conference. 764–783.
 [96] Matthieu Rivain and Emmanuel Prouff. 2010. Provably Secure Higher-Order Masking of AES. In Proceedings of the
      12th International Workshop on Cryptographic Hardware and Embedded Systems. 413–427.
 [97] Tobias Schneider, Clara Paglialonga, Tobias Oder, and Tim Güneysu. 2019. Efficiently Masking Binomial Sampling at
      Arbitrary Orders for Lattice-Based Crypto. In Proceedings of the 22nd IACR International Conference on Practice and
      Theory of Public-Key Cryptography. 534–564.
 [98] Kai Schramm and Christof Paar. 2006. Higher Order Masking of the AES. In Proceedings of the RSA Conference
      Cryptographers’ Track. 208–225.
 [99] François-Xavier Standaert. 2017. How (not) to Use Welch’s T-test in Side-Channel Security Evaluations. IACR
      Cryptology ePrint Archive 2017 (2017), 138.
[100] Chungha Sung, Brandon Paulsen, and Chao Wang. 2018. CANAL: a cache timing analysis framework via LLVM
      transformation. In Proceedings of the 33rd ACM/IEEE International Conference on Automated Software Engineering.
      904–907.
[101] Jiehui Tang, Yongbin Zhou, Hailong Zhang, and Shuang Qiu. 2015. Higher-Order Masking Schemes for Simon. In
      Proceedings of the 17th International Conference on Information and Communications Security. 379–392.
[102] David A. Wagner. 2004. Cryptanalysis of a Provably Secure CRT-RSA Algorithm. In Proceedings of the 11th ACM
      Conference on Computer and Communications Security. 92–97.
[103] Chao Wang and Patrick Schaumont. 2017. Security by compilation: an automated approach to comprehensive
      side-channel resistance. ACM SIGLOG News 4, 2 (2017), 76–89.
[104] Jingbo Wang, Chungha Sung, and Chao Wang. 2019. Mitigating power side channels during compilation. In Proceedings
      of the ACM Joint Meeting on European Software Engineering Conference and Symposium on the Foundations of Software
      Engineering. 590–601.
[105] Shuai Wang, Pei Wang, Xiao Liu, Danfeng Zhang, and Dinghao Wu. 2017. CacheD: Identifying Cache-Based Timing
      Channels in Production Software. In Proceedings of the 26th USENIX Security Symposium. 235–252.
[106] Weijia Wang, Yu Yu, and François-Xavier Standaert. 2019. Provable Order Amplification for Code-Based Masking:
      How to Avoid Non-Linear Leakages Due to Masked Operations. IEEE Transactions on Information Forensics and
      Security 14, 11 (2019), 3069–3082.
[107] Leo Weissbart, Stjepan Picek, and Lejla Batina. 2019. One Trace Is All It Takes: Machine Learning-Based Side-Channel
      Attack on EdDSA. In Proceedings of the 9th International Conference on Security, Privacy, and Applied Cryptography
      Engineering. 86–105.
[108] Meng Wu, Shengjian Guo, Patrick Schaumont, and Chao Wang. 2018. Eliminating timing side-channel leaks using
      program repair. In Proceedings of the 27th ACM SIGSOFT International Symposium on Software Testing and Analysis.
      15–26.
[109] Meng Wu and Chao Wang. 2019. Abstract interpretation under speculative execution. In Proceedings of the 40th ACM
      SIGPLAN Conference on Programming Language Design and Implementation. 802–815.
[110] Jun Zhang, Pengfei Gao, Fu Song, and Chao Wang. 2018. SCInfer: Refinement-Based Verification of Software
      Countermeasures Against Side-Channel Attacks. In Proceedings of the 30th International Conference on Computer
      Aided Verification. 157–177.




ACM Trans. Softw. Eng. Methodol., Vol. 37, No. 4, Article 111. Publication date: August 2020.
