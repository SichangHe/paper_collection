                                                     Formal Verification of Probing Security via
                                                             Conditional Independence
                                                                      Satoshi Kura                                                    Katsuyuki Takashima
                                              Faculty of Education and Integrated Arts and Sciences                 Faculty of Education and Integrated Arts and Sciences
                                                                Waseda University                                                     Waseda University
                                                                  Tokyo, Japan                                                          Tokyo, Japan
                                                          ORCID: 0000-0002-3954-8255                                            ORCID: 0000-0001-5216-2229
arXiv:2605.23316v2 [cs.LO] 25 May 2026




                                            Abstract—Side-channel attacks are a major threat to the                 programs, including cryptographic algorithms. This is a variant
                                         security of cryptosystems. Masking is a widely used countermea-            of separation logic [22], which is a Hoare-style logic that
                                         sure against such attacks, but proving the security of masked              can reason about separation of resources using the separating
                                         algorithms is error-prone without formal verification. In this
                                         work, we propose a novel approach to formal verification of                conjunction ϕ∗ψ. Together with the frame rule, the separating
                                         noninterference properties of masked algorithms based on prob-             conjunction enables local reasoning, which is particularly
                                         abilistic separation logic. By establishing a connection between           useful for modular verification of large programs.
                                         noninterference and conditional independence, we show how                     Separation logic was originally introduced to reason about
                                         noninterference can be verified using Lilac, a separation logic            mutable data structures in imperative programs [22], but it
                                         for conditional independence. We also provide several proof rules
                                         that facilitate the verification of probing security and demonstrate       has since been applied in a variety of contexts beyond memory
                                         their application to example algorithms.                                   separation. Probabilistic separation logic interprets the separat-
                                            Index Terms—Side-channel attack, Masking, Noninterference,              ing conjunction as probabilistic independence between random
                                         Conditional independence, Formal verification, Probabilistic sep-          variables and has been applied to verify input independence
                                         aration logic                                                              properties of cryptographic algorithms, such as the one-time
                                                                I. I NTRODUCTION                                    pad and private information retrieval. Several extensions of
                                                                                                                    probabilistic separation logic have been proposed [23]–[28],
                                         A. Formal Verification of Probing Security
                                                                                                                    including Lilac [29], which supports reasoning about condi-
                                            Information leakage through side-channel attacks is one of              tional independence.
                                         the major threats to the security of cryptographic schemes and                Masking can be viewed as a generalization of the one-time
                                         digital signatures. Among the widely used countermeasures                  pad, which strongly suggests that probabilistic separation logic
                                         against side-channel attacks is masking [1]. Masking protects              is a natural framework for verifying probing security. However,
                                         secrets by splitting a secret value into several shares via secret         to the best of our knowledge, none of these logics has been
                                         sharing and performing computations on those shares, so that               used to verify probing security of masked algorithms.
                                         the leakage of any subset of intermediate values does not
                                         reveal the underlying secret. Applications of masking include              C. Connection Between Simulator-Based Security Notions and
                                         the digital signature scheme Raccoon [2], which was submit-                Conditional Independence
                                         ted to the NIST Post-Quantum Cryptography Standardization                     In this work, we establish a connection between simulator-
                                         process, as well as Masked ML-DSA [3]–[5], a masked variant                based definitions of probing security and conditional indepen-
                                         of ML-DSA [6], among many others.                                          dence, enabling the use of probabilistic separation logic for
                                            The notion of noninterference is commonly used to for-                  formal verification of probing security.
                                         malize the security of masked algorithms in the ISW probing                   In cryptography, many security notions, including non-
                                         model [1]. However, proving noninterference by hand is error-              interference, are defined via simulators. To understand the
                                         prone, and several flaws have been identified in manual                    connection between such simulator-based definitions and con-
                                         security proofs for masked algorithms [7], [8]. To avoid such              ditional independence, consider a cryptographic algorithm
                                         errors, formal verification of probing security has been studied           (Fig. 1a) and an adversary who attempts to learn some secret
                                         in recent years [9]–[20].                                                  information from the input by observing information leaked
                                         B. Formal Verification via Separation Logic                                during the execution of the algorithm. In this situation, three
                                            Probabilistic separation logic [21] is a recently developed             kinds of information are involved: (i) secret information A
                                         formal verification method for reasoning about probabilistic               in the input, (ii) public (non-secret) information B in the
                                                                                                                    input, which is not directly observed by the adversary, and
                                           This work is supported by JSPS Grant-in-Aid for Scientific Research(C)   (iii) information C observed by the adversary. To formalize
                                         JP22K11912, JST K Program Grant Number JPMJKP24U2, MEXT Quantum
                                         Leap Flagship Program (MEXT Q-LEAP) JPMXS0120319794, and JSPS              the requirement that the adversary cannot learn A from C,
                                         KAKENHI Grant Number JP25H00446, JP25K21183.                               simulator-based security definitions postulate the existence of
                         secret input A                 cryptographic
                                                                           output C observed by adversary
                         public input B                   algorithm

                                          (a) A cryptographic algorithm with input and output


       public input B            simulator        observed output C                         A⊥C|B

                     (b) Simulator-based formulation                       (c) Conditional-independence-based formulation
     Fig. 1: Two formulations of security: simulator-based formulation and conditional-independence-based formulation.


a simulator that can compute C solely from B, without access          but are not provided in the original Lilac paper [29]. In
to A (Fig. 1b). If such a simulator exists, then the adversary        particular, we show that semi-graphoid axioms for conditional
cannot distinguish the real execution from the simulated one.         independence hold in Lilac. These additional rules enhance
Consequently, although the adversary may obtain some infor-           the verification power of Lilac for reasoning about probing
mation about B, it is impossible to learn A.                          security. We also consider proof rules related to composabil-
   We rephrase this simulator-based definition in terms of            ity of noninterference properties and capture them in Lilac.
conditional independence (Fig. 1c). Suppose that A, B, and            Composability is an important aspect and has been studied in
C are random variables. Given A and B, the probability                prior works [9], [31]. In contrast to prior works, our compos-
distribution of C generated by the cryptographic algorithm            ability rules focus on (I, O)-noninterference, which is a basic
(Fig. 1a) corresponds to the conditional probability distribution     building block for the definitions of t-noninterference and its
Pr[C|A, B]. On the other hand, given only B, the probabil-            variants. We demonstrate the effectiveness of our approach
ity distribution of C generated by the simulator (Fig. 1b)            by verifying non-interference of the R EFRESH algorithm [8],
corresponds to Pr[C|B]. The simulator-based definition re-            [9], multiplication [1], and A DD R EP N OISE [32] using Lilac:
quires that these two probability distributions are equal:            the first two are fundamental building blocks for masked
Pr[C|A, B] = Pr[C|B]. This is exactly the definition of               algorithms, and the last one is a key component of the security
conditional independence of A and C given B, denoted by               proof of Raccoon [2].
A ⊥ C | B. This connection leads to the idea of verifying                The contributions of this work are summarized as follows:
simulator-based security notions by proving conditional inde-            • We establish a connection between existence of simula-
pendence properties using probabilistic separation logic that               tors and conditional independence, which allows us to
can reason about conditional independence.                                  use probabilistic separation logics for conditional inde-
D. Contributions                                                            pendence, such as Lilac, to verify probing security.
                                                                         • We provide additional proof rules for Lilac that are nec-
   In this paper, we formalize the connection between
simulator-based definitions of probing security and conditional             essary to verify probing security of masked algorithms.
independence within the semantic framework of Lilac [29].                   In particular, we show that semi-graphoid axioms for
Although the underlying idea of this connection is conceptu-                conditional independence hold in Lilac. We also provide
ally simple, its formalization in Lilac is technically non-trivial.         proof rules related to composability of noninterference.
                                                                         • We demonstrate the effectiveness of our approach by
This difficulty stems from the fact that Lilac models probabilis-
tic independence using independent combination, rather than                 verifying non-interference of the R EFRESH algorithm [8],
the standard construction based on product probability spaces.              [9], multiplication [1], and A DD R EP N OISE [32] using
The relationship between these two notions of independence                  Lilac.
has been studied in [30]; however, that work does not address
                                                                                                II. OVERVIEW
the semantics of the conditioning modality defined via disin-
tegration. Consequently, establishing the desired connection in       A. Simulator-Based Security Notions and Probabilistic Inde-
Lilac requires a careful measure-theoretic argument.                  pendence
   Although technically demanding, this formalization pays off           We illustrate the connection between simulator-based secu-
by making it possible to reason about probing security directly       rity notions and probabilistic independence, using the one-time
within Lilac. Our main theorem (Theorem V.1) states that the          pad encryption as an example.
simulator-based definition of noninterference is equivalent to
the conditional independence property expressed as a Hoare            Example II.1 (One-time pad). Suppose that a plaintext mes-
triple in Lilac. By the main theorem, to verify probing security      sage is given as an element M in a finite abelian group K. The
of a masked algorithm, it suffices to prove the corresponding         following program implements the one-time pad encryption:
conditional independence property using proof rules of Lilac.             OTP(M )
   Moreover, we provide additional proof rules for Lilac that               K ← unif K;
are necessary to verify probing security of masked algorithms               C ← ret (M − K);
      ret C                                                        shares via secret sharing and computations are performed on
Here, unif K is the uniform distribution over K, and C ←           those shares. A bit more formally, let X be a secret value
ret (M − K) means deterministic assignment of the value            represented as an element in a finite abelian group K. The
M − K to the variable C. The programming language used in          secret value X is split into t + 1 shares
this paper will be formally introduced later in Section III-A.
                                                                           K∋X        7→    X = (X (0) , . . . , X (t) ) ∈ Kt+1
     a) Simulator-based formulation of security: We can for-
mulate the security of the one-time pad using simulators. In       such that the secret value X can be recovered as the sum of
this setting, a simulator is defined as a program Sim(OTP)         all shares X = X (0) + · · · + X (t) , but any proper subset of the
that simulates the distribution of C computed by OTP(M )           shares does not reveal any information about X. The value t
without knowing M . If such a simulator exists, then the           is called the masking order. An algorithm is said to be masked
adversary cannot learn any information about M because             if secret input values are represented using such shares, and
the adversary cannot distinguish the real execution from the       the algorithm operates on such shares.
simulated one, which does not depend on M . Concretely,            Example II.2. Consider adding two values X and Y in a finite
a valid simulator for the one-time pad can be given as a           abelian group K. A masked implementation of the addition
program that uniformly samples a random element from K             with two shares (t = 1) is given as follows.
as the ciphertext: Sim(OTP) := unif K.
                                                                        M ASKEDA DD(X (0) , X (1) , Y (0) , Y (1) )
     b) Independence-based formulation: Shannon’s perfect
                                                                           Z (0) ← ret (X (0) + Y (0) );
secrecy is a well-known security notion for encryption
                                                                           Z (1) ← ret (X (1) + Y (1) );
schemes [33] and defined as the independence between the
                                                                           ret (Z (0) , Z (1) )
plaintext M and the ciphertext C. This captures the intuition
that observing the ciphertext C does not provide any informa-      It is straightforward to see that the output shares Z (0) and Z (1)
tion about the plaintext M . In fact, the independence of M        represent the sum Z = X + Y of two input values.
and C is equivalent to the existence of a simulator described         Masked algorithms are expected to be secure against side-
above.                                                             channel attacks, since the leakage of at most t shares does not
   To express and verify such independence properties of           reveal any information about the underlying secret value. This
randomized programs, we can use probabilistic separation           security notion is formalized by t-noninterference [10], which
logic [21], [29]. In probabilistic separation logic, sources of    we informally describe below.
randomness are treated as resources. We have a basic assertion           a) Simulator-based formulation of t-noninterference: In
own E, which asserts ownership of a random variable E, and         Example II.2, the secret values X and Y remain secure even
the separating conjunction ϕ ∗ ψ expresses that the random         if an adversary can only guess at most t input shares for
variables mentioned in ϕ and those in ψ are independent.           each of X and Y . This intuition is formalized as a security
Therefore, we can express the independence between two             definition for masked algorithms, by considering a simulator
random variables X and Y as own X ∗ own Y .                        that takes t input shares as its input and outputs the values
   Using probabilistic separation logic, the probabilistic inde-   that are probed by an adversary. In the t-probing model, an
pendence between the plaintext M and the ciphertext C can          adversary is allowed to choose arbitrary probe locations and
be written as a Hoare triple                                       observe up to t intermediate values during the execution of the
        {own M } OTP(M ) {C. own M ∗ own C}                        program. A masked algorithm is said to be t-noninterfering
                                                                   if, for any choice of at most t probes, there exists a simulator
This states that, starting from an initial random variable
                                                                   that, given at most t input shares, can simulate the values
satisfying the precondition own M , after executing the pro-
                                                                   observed at those probes. The existence of such a simulator
gram OTP(M ), the resulting random variable satisfies the
                                                                   ensures that the adversary cannot learn any information about
postcondition own M ∗ own C where C is a random variable
                                                                   the secret values from the probed values, since the adversary
bound to the output of the program.
                                                                   cannot guess input shares that are not given to the simulator.
   To prove that the above Hoare triple holds, we can use the
proof rules of probabilistic separation logic, which have been           b) Conditional-independence-based formulation: Simi-
already demonstrated in [21, Section 5.1.2] for the one-time       larly to the case of the one-time pad, we can rephrase the
pad. In this case, we do not need conditional independence         definition of t-noninterference in terms of conditional indepen-
since the simulator does not take any input. However, as we        dence. Specifically, we consider the conditional independence
will see below, conditional independence becomes necessary         between the input shares not in the simulator’s input and the
when we consider simulators that take some input, such as in       probed values, given the input shares provided to the simulator.
the case of non-interference verification.                         It turns out that this conditional independence is equivalent to
                                                                   the simulator-based definition of t-noninterference, which we
B. Noninterference of Masked Programs and Conditional In-          will formally state in Theorem V.1.
dependence                                                            To reason about such conditional independence properties
  Masking is a widely used countermeasure against side-            of masked programs, we can use an extension of probabilistic
channel attacks [1], where a secret value is split into several    separation logic for conditional independence, namely, Lilac
[29]. In Lilac, the conditional independence between random                   This is a generalization of the weak union property of condi-
variables X and Y given Z can be expressed as a formula                       tional independence, which states W ⊥ (X, Y ) | Z implies
Cz←Z (own X ∗ own Y ) where the conditioning modality                         W ⊥ Y | (X, Z) for random variables W , X, Y , and Z.
Cz←Z represents conditioning on the random variable Z.                        We will prove the soundness of this rule in Proposition VI.1.
Using Lilac, the conditional independence required for t-                     Using this rule, we can have the following entailment:
noninterference of a masked program M ASKEDA DD can be                                                    as
                                                                               own(X, Y) ∗ Z (0) = X (0) + Y (0)
expressed as follows: for each choice of probe locations1 P ⊆
                                                                                                                                  as
{X (0) , X (1) , Y (0) , Y (1) , Z (0) , Z (1) } such that |P| ≤ t = 1,         ⊢           C         (own(X (1) , Y (1) ) ∗ Z (0) = X (0) + Y (0) )
                                                                                 (x,y)←(X (0) ,Y (0) )
there exists a choice of at most one input share X ⊆ X and
Y ⊆ Y from each of X = (X (0) , X (1) ) and Y = (Y (0) , Y (1) )              Under the conditioning modality, (X (0) , Y (0) ) are equal to
                                                                                                                                               as
such that |X |, |Y| ≤ |P| and the following Hoare triple holds.               deterministic values (x, y). Thus, we can conclude that Z (0) =
      { own(X, Y) }                                                           x + y is conditionally independent of (X (1) , Y (1) ), as desired.
                                                                                 As we have seen in the above example, we can use
      M ASKEDA DD(X, Y)                                                       Lilac to prove t-noninterference of masked programs, given
      { Z.         C        (own(X \ X , Y \ Y) ∗ own P) }                    (1) the connection between simulator-based definitions and
             (x,y)←(X ,Y)
                                                                              conditional independence and (2) additional proof rules for
Here, X\X denotes the tuple of variables that are in X but not                Lilac formulas, such as the weak union rule. In the subsequent
in X . This Hoare triple states that the information observed by              sections, we will formally present such results. We will also
the adversary (or the output of the simulator) P is independent               show more examples of masked programs and their security
of the secret input X \ X and Y \ Y, given the public input                   proofs using Lilac in Section VII.
X and Y provided to the simulator.
   Once we have established the connection between                                                       III. P RELIMINARIES
simulator-based definitions of t-noninterference and condi-                   A. A Probabilistic Programming Language: APPL
tional independence, it remains to show that the above Hoare                   We define a probabilistic programming language called
triple holds for each choice of probe locations P. This can                   APPL following [29].
be done by applying the proof rules of Lilac. For example,                     1) Syntax: Expressions are defined as follows.
consider the case when the adversary probes the output share
P = {Z (0) }. Then, we can choose X = {X (0) } and                              E      :=       x | X | T | F | k | i | if E0 then E1 else E2
Y = {Y (0) } as the input shares to be given to the simulator.                               | (E1 , . . . , En ) | proji E | E1 op E2
Using Lilac’s proof rules, we can derive the following Hoare
triple:                                                                       Here, x is a deterministic variable, X is a random variable,
                                                                              k ∈ K is a constant in a finite abelian group K, and i is
    { own(X, Y) }                                                             a natural number. The constant T (resp. F) represents the
    M ASKEDA DD(X, Y)                                                         boolean value true (resp. false). The symbol op ranges over
                                                                              binary operations, including group operations such as + and
    { Z.            C              (own(X (1) , Y (1) ) ∗ own Z (0) ) } (1)
           (x,y)←(X (0) ,Y (0) )                                              −; boolean operations such as ∧ and ∨; and comparison
                                                                              operations such as =, and ̸=.
A bit more concretely, this is proved as follows. We first use
                                                                                Expressions are typed in a standard way. Types are defined
the rule for Hoare triples in Fig. 4 to derive the following
                                                                              as follows.
Hoare triple.
             { own(X, Y) }                                                            A, B       :=      bool | K | index | A1 × · · · × An
             M ASKEDA DD(X, Y)                                                We have base types bool, K, and index for boolean values,
                                          (0) as   (0)        (0)             elements of the group K, and indices for for loops, respec-
             { Z.(own(X, Y)) ∗ Z              =X         +Y         }   (2)
                                                                              tively. Types also include product types A1 × · · · × An . The
        as
Here, = stands for the almost-sure equality between two                       empty product type (n = 0) is written as unit.
random variables. By the consequence rule (H-C ONSEQ), it                        Typing judgements for expressions are given in the form of
remains to show that the postcondition of (2) implies that                    Γ; ∆ ⊢ E : A where Γ = x : A1 , . . . , xm : Am is a typing
of (1). This is done by using the proof rules for Lilac formulas.             context for deterministic variables and ∆ = X : A1 , . . . , Xn :
Several proof rules are provided in [29]; however, they are                   An is a typing context for random variables. Typing rules are
not sufficient to derive the desired entailment. Therefore, we                standard [29] and omitted here.
introduce several new rules for Lilac formulas in Section VI,                    APPL programs are defined as follows.
including the following rule.
                                                                                    L, M, N :=       ret E | X ← M ; N | unif K
               ϕ ∗ (own(X, Y )) ⊢ C (ϕ ∗ own Y )                                                  | for (X ← E; i ← nstart . . . nend ) {M }
                                           x←X

  1 Without loss of generality, we may assume that the set of probes P does   In the for-loop for (X ← E; i ← nstart . . . nend ) {M }, i
not contain input shares: P ⊆ {Z (0) , Z (1) }.                               is the loop index variable ranging from nstart to nend . The
                                                                                                                    (0)        (t)
variable X is initialized with E at the beginning of the loop,        are shared inputs where each Xi = (Xi , . . . , Xi ) is a
and in each iteration, X is updated with the result of M . The        tuple of t + 1 shares. A masked program M is said to be t-
final value of X after the last iteration is returned as the result   noninterfering (t-NI) if for any set of probes O with |O| ≤ t,
of the for-loop. One might expect the for-loop to be written as       there exists a subset Ii ⊆ Xi for each i such that |Ii | ≤ |O|
X ← E; for i ← nstart · · · nend {M }. However, we adopt the          and the values of probes in O can be simulated using only the
above syntax because X is bound by the for-loop construct.            input shares in I1 , . . . , In .
   In sequential composition X ← M ; N and for-loops, we                 Below, we rephrase the definitions of t-noninterference and
often bind multiple variables at once. Formally, when the result      related notions in terms of APPL programs. Suppose that we
of M is a tuple, we define (X, Y ) ← M ; N as syntactic sugar         have an APPL program ∆ ⊢ M : GB where ∆ = X1 :
for Z ← M ; N [proj1 Z/X, proj2 Z/Y ] where Z is a fresh              A1 , . . . , Xm : Am and B = B1 × · · · × Bn . We assume that
variable, and similarly for for-loops. In many examples in this       M is in the static single assignment (SSA) form so that each
paper, we also use indexed variables such as Xi and Xi,j              internal value computed in M is assigned to a unique variable
and consider programs such as XE ← M ; N where E is an                name. Then, probes can be specified by a set of variables. We
expression of type index.                                             call variables X1 , . . . , Xm in the context ∆ the input variables
   We do not include conditional branching as a primitive             of M . The output variables of M are variables bound to the
construct in APPL. However, they can be defined as syntactic          output value of M and have type B. The output variables do
sugar using conditional branching for expressions.                    not a priori occur in the program, but we often introduce them
                                                                      to refer to the output of M . The internal variables of M are
  if E then M else N                                                  variables occurring in M other than input variables.
   := X ← M ; Y ← N ; ret (if E then X else Y )                          Later in Section IV, we will introduce Hoare triples to
                                                                      reason about APPL programs. A Hoare triple is given in
Since APPL does not cause computational effects other than
                                                                      the form {ϕ} M {Y.ψ} where ϕ is an assertion over input
randomness, this definition is semantically equivalent to the
                                                                      variables of M , Y is a tuple of variables bound to the output of
standard conditional branching construct.
                                                                      M , and ψ is an assertion over both input variables and output
   Typing judgments for programs are given in the form of
                                                                      variables Y. Hoare triples cannot refer to internal variables
∆ ⊢ M : GA where ∆ is a typing context for random variables.
                                                                      directly, but we can easily transform a given APPL program
Here, GA represents a type of distributions over values of type
                                                                      to expose internal variables as output variables.
A. Typing rules are shown in Fig. 2.
                                                                         For example, the APPL program X : K ⊢ Y ←
   2) Semantics: Each type A is interpreted as a measurable
                                                                      ret X + X; ret Y + X : K has one input variable X
space JAK in the standard way. Note that all base types
                                                                      and one internal variable Y , and outputs Y + X. Let Z
are interpreted as countably generated measurable spaces,
                                                                      be an output variable bound to the output. Hoare triples
which implies that any type is also interpreted as a countably
                                                                      {ϕ} Y ← ret X + X; ret Y + X {Z.ψ} for this program
generated measurable space. The interpretation of a context
                                                                      can refer to X and Z, but not to Y directly. In this case, we
Γ = x : A1 , . . . , xm : Am is defined as the product measurable
                                                                      can transform the program to X : K ⊢ Y ← ret X +X; Z ←
space JΓK = JA1 K × · · · × JAm K.
                                                                      ret Y + X; ret (Y, Z) : K × K so that both Y and Z are
   Expressions Γ; ∆ ⊢ E : A are interpreted as functions
                                                                      accessible as output variables.
                JEK : JΓK → Meas(J∆K, JAK)                               In general, given a program M , we can construct a program
                                                                      M ♯ that exposes all internal variables as output.
where Meas(X, Y ) is the set of measurable functions from
X to Y . Programs ∆ ⊢ M : GA are interpreted as Markov                         ∆ ⊢ M : GB       7→    ∆ ⊢ M ♯ : G(Bint × B)
kernels, i.e., measurable functions that maps each element in
J∆K to a probability measure over JAK:                                Here, Bint is the type of the tuple of all internal variables of
                                                                      M . Of course, the transformed program M ♯ is defined so that
                   JM K ∈ Meas(J∆K, GJAK)                             M is semantically equal to (Y, Z) ← M ♯ ; ret Z where Y
                                                                      and Z are tuples of internal and output variables, respectively.
Here, G is the Giry monad, which maps a measurable space to
                                                                         In what follows, we assume that APPL programs are appro-
the measurable space of probability measures over it. Concrete
                                                                      priately transformed so that internal variables are accessible
definitions of the semantics are standard [29] and omitted.
                                                                      as parts of output variables. Then, probes can be specified
B. t-Probing Model and Noninterference                                by output variables only. Now, we define the notion of
                                                                      noninterference for APPL programs. Throughout the paper,
   In the t-probing model, an adversary is allowed to probe up
                                                                      we write a tuple of variables X = (X1 , . . . , Xm ) in bold font
to t internal or output values during the execution of a masked
                                                                      and often identify the tuple with the set {X1 , . . . , Xm } for
program where t is the order of masking. The adversary
                                                                      notational convenience.
aims to guess secret information from the observed values,
which is achieved if the adversary can guess more than t              Definition III.1. Let ∆ ⊢ M : GB be an APPL program
input shares. The notion of t-noninterference formalizes the          where ∆ = X1 : A1 , . . . , Xm : Am and B = B1 × · · · × Bn .
security requirement in this setting. Suppose that X1 , . . . , Xn    We write I = {X1 , . . . , Xm } for the set of input variables and
                ∅; ∆ ⊢ E : A                  ∆ ⊢ M : GA  ∆, X : A ⊢ N : GB
               ∆ ⊢ ret E : GA                      ∆ ⊢ X ← M ; N : GB                                ∆ ⊢ unif K : GK

                                         ∅; ∆ ⊢ E : A  ∆, i : index, X : A ⊢ M : GA
                                          ∆ ⊢ for (X ← E; i ← ns . . . ne ) {M } : GA

                                             Fig. 2: Typing rule for APPL programs.


O = {Y1 , . . . , Yn } for the set of output variables of M . For   is (X1 ∪ · · · ∪ Xn ∪ Y, O)-noninterfering. A strong version of
I ⊆ I and O ⊆ O, we say that M is (I, O)-noninterfering             NIU (SNIU) can be defined similarly.
((I, O)-NI) if there exists an APPL program ∆I ⊢ Sim(M ) :
                                                                       There are other variants of t-NI in the literature, such
GBO such that the following equation holds:
                                                                    as noninterference with public outputs (NIo) [35] and probe
              Sim(M )      =    O ← M ; ret O                       isolating noninterference (PINI) [31]. Although we do not
                                                                    give their definitions here, they can also be defined via
Here, ∆I is the restriction of ∆ to variables in I and BO =         (I, O)-NI. Since (I, O)-NI is the basis of various notions of
                                                                    noninterference, we mainly focus on verifying (I, O)-NI for
Q
  Yi ∈O Bi is the restriction of B to components in O. We call
such a program Sim(M ) a simulator for M with input I and           APPL programs in the rest of this paper.
output O.
                                                                      IV. L ILAC : A S EPARATION L OGIC FOR C ONDITIONAL
   The notion of t-noninterference [10] for masked algorithms
                                                                                          I NDEPENDENCE
is defined using (I, O)-NI.
Definition III.2 (t-NI). Suppose that the input variables of the      We briefly review the syntax and semantics of Lilac [29], a
APPL program M consist of shared values X1 , . . . , Xn where       probabilistic separation logic that can reason about conditional
                (0)       (t)                                       independence.
each Xi = (Xi , . . . , Xi ) is a tuple of t + 1 shares, and
suppose that the output variables are O = {Y1 , . . . , Ym }. We         Syntax: Formulas of Lilac are defined as follows.
say that M is t-noninterfering (t-NI) if for any set of probes
                                                                      ϕ, ψ :=        ⊤ | ⊥ | ϕ ∧ ψ | ϕ ∨ ψ | ∀x.ϕ | ∃x.ϕ
O ⊆ O with |O| ≤ t, there exist subsets X1 ⊆ X1 , . . . , Xn ⊆
Xn such that |Xi | ≤ |O| for each i, and M is (X1 ∪ · · · ∪                     | ∀rv X.ϕ | ∃rv X.ϕ | ϕ ∗ ψ | ϕ −∗ ψ | own E | □ ϕ
                                                                                                          as
Xn , O)-noninterfering.                                                         |    C      ϕ | E ∼ µ | E1 = E2 | wp(M, X : A.ϕ)
                                                                                    x:A←E
   There are several variants of t-noninterference proposed in
the literature. One of such variants is strong noninterference      Here, µ := unif K | · · · is a distribution, including the
(SNI) [9], which exhibits a better composability property. This     uniform distribution unif K over a finite group K. Formulas
variant is also defined based on (I, O)-NI.                         defined above assert propositions about random variables and
                                                                    the ownership of sources of randomness. Below we briefly
Definition III.3 (t-SNI). Suppose the same setting as in            explain the intended meaning of each construct. The formula
Definition III.2. Let Oint ⊆ O be the set of exposed internal       own E asserts the probabilistic ownership of the random vari-
variables, which are not used as input to subsequent programs.      able E. The formula E ∼ µ asserts that the random variable E
We say that M satisfies t-strong noninterference (t-SNI) if for     follows the distribution µ and that its probabilistic ownership is
any set of probes O ⊆ O with |O| ≤ t, there exist subsets                                   as
                                                                    held. The formula E1 = E2 asserts that the random variables
X1 ⊆ X1 , . . . , Xn ⊆ Xn such that for each i, |Xi | ≤ |O∩Oint |   E1 and E2 are almost surely equal. The separating conjunction
and M is (X1 ∪ · · · ∪ Xn , O)-noninterfering.                      ϕ ∗ ψ asserts that ϕ and ψ own disjoint, probabilistically
   Another variant is noninterference with unshared input           independent sources of randomness and that ϕ holds for one
(NIU) [34], which generalizes ordinary noninterference by           part and ψ holds for the other part. The conditioning modality
allowing unshared inputs in addition to shared inputs.              Cx←E ϕ, which is one of the main features of Lilac, asserts
                                                                    that ϕ holds when conditioning on the value of E being x.
Definition III.4 (t-NIU). Suppose that the input variables of       The weakest precondition wp(M, X : A.ϕ) for program M
the APPL program M consist of shared inputs X1 , . . . , Xn         and postcondition ϕ asserts that after executing M and binding
and unshared inputs Y = (Y1 , . . . , Ym ) where each Xi =          the result to the random variable X, the formula ϕ holds. The
   (0)         (t)
(Xi , . . . , Xi ) is a tuple of t + 1 shares. Let O be the set     persistence modality [36] is denoted by □ ϕ, which asserts
of output variables of M . We say that M is t-noninterfering        that ϕ holds without owning any source of randomness. There
with unshared input (t-NIU) if for any set of probes O ⊆ O          are two types of quantifiers: the standard quantifiers ∀x.ϕ
with |O| ≤ t, there exist subsets X1 ⊆ X1 , . . . , Xn ⊆ Xn and     and ∃x.ϕ for deterministic variables, and the random variable
Y ⊆ Y such that |Xi | ≤ |O| for each i, |Y| ≤ |O|, and M            quantifiers ∀rv X.ϕ and ∃rv X.ϕ for random variables.
   For example, own X ∗ own Y means that the random                 deterministic variables in Γ, D : Ω → J∆K is a measurable
variables X and Y are independent. Conditional independence         function representing a random variable environment for ∆,
of X and Y given Z is expressed as Cz←Z (own X ∗own Y ).            and P ∈ Mdisint is an element of the KRM of which the
   Typing judgements for Lilac formulas are denoted by              formula has ownership. Below, we write RV A := {D : Ω →
Γ; ∆ ⊢ ϕ where Γ is a typing context for deterministic              A} for the set of random variables where A is a measurable
variables and ∆ is a typing context for random variables.           space. We show the semantics of important constructs; the
Typing rules are standard [29] and omitted here.                    semantics of other constructs can be found in [29].2
   We write ϕ ⊢ ψ if ϕ entails ψ in Lilac. We also write ⊢ ψ           γ, D, (F, µ) |= own E if JEK(γ) ◦ D is F-measurable
                                                                       •
when ϕ is ⊤. If both ϕ ⊢ ψ and ψ ⊢ ϕ hold, then we write               where ◦ is function composition.
ϕ ⊣⊢ ψ. The semantics of the entailment relation is given later.     • γ, D, (F, µ) |= E ∼ ν if JEK(γ) ◦ D is F-measurable
Inference rules for the entailment relation are shown in Fig. 3.       and the pushforward measure (JEK(γ) ◦ D)∗ µ is ν.
Most of the rules are taken from [29], but we also include some      • γ, D, P |= ϕ ∗ ψ if γ, D, P1 |= ϕ and γ, D, P2 |= ψ for
rules that are not explicitly in [29] but are easily proved to be      some P1 , P2 ∈ Mdisint such that P1 · P2 ⊑ P.
valid. Later in Section VI, we also provide several non-trivial                                                      ′
                                                                     • γ, D, (F, µ) |= Cx:A←E ϕ if for any (ΣΩ , µ ) ⊒ (F, µ)
additional rules that are not in [29].                                              ′
                                                                       and any µ -disintegration {νx }x∈JAK with respect to
   To reason about APPL programs, Hoare triples are defined            JEK(γ) ◦ D, it holds that γ, D, (F , νx |F ) |= ϕ for
in Lilac as follows.                                                   almost every x ∈ JAK. Here, the disintegration {νx }x∈JAK
      {ϕ} M {X.ψ}        :=    □(ϕ −∗ wp(M, X : A.ψ))                  intuitively represents the conditional distribution given
                                                                       the value of JEK(γ) ◦ D ∈ RVJAK.
This is semantically equivalent to ϕ ⊢ wp(M, X : A.ψ).               • γ, D, P |= wp(M, X : A.ϕ) if for all Pf and µ such that
Inference rules for Hoare triples are shown in Fig. 4.                 Pf · P ⊑ (ΣΩ , µ) and for all D ∈ RVJ∆e K, there exist
     Semantics: We briefly explain the semantics of Lilac for-         X ∈ RVJAK, P ′ , and µ′ such that Pf · P ′ ⊑ (ΣΩ , µ′ ),
mulas [29]. The semantics of separating conjunction in Lilac is        γ, (D, X), P ′ |= ϕ, and the following two distributions
based on the notion of Kripke resource monoids (KRMs) [37].            are equal:
A KRM is a partially ordered partial commutative monoid                                    
(M, 1, ·, ⊑) such that the order relation ⊑ is compatible with       ω ← µ;                                                   !
                                                                                                   ω ← µ′ ;
the monoid product. To capture probabilistic independence of        v ← JM K(D(ω));        =
                                                                                           
                                                                                                   ret (De (ω), D(ω), X(ω))
random variables, Lilac uses a specific KRM defined on the           ret (De (ω), D(ω), v)
set of probability spaces on a fixed sample space Ω.
                                                                       Finally, we define the entailment relation ϕ ⊢ ψ as follows.
Definition IV.1. Let (Ω, ΣΩ ) be the Hilbert cube [0, 1]N with
the standard Borel σ-algebra. We define a KRM Mind =                       ∀γ.∀D.∀P.         γ, D, P |= ϕ         =⇒        γ, D, P |= ψ
(M, 1, ·, ⊑) as follows.
   • The underlying set Ω is the set of probability spaces P =                V. N ONINTERFERENCE AND C ONDITIONAL
     (Ω, F, µ) over the sample space Ω where F ⊆ ΣΩ is a σ-                               I NDEPENDENCE
     algebra and µ : F → [0, 1] is a probability measure. We
                                                                       In this section, we present our main result that characterizes
     often omit Ω and simply write (F, µ) for a probability
                                                                    noninterference as conditional independence expressed by
     space in M.
                                                                    Lilac Hoare triples. Let ∆ ⊢ M : GB be an APPL program
   • The monoid product · is defined by the independent com-
                                                                    where ∆ = X1 : A1 , . . . , Xm : Am and B = B1 × · · · × Bn .
     bination of probability spaces: given a pair of probability
                                                                    Let I and O be subsets of input and output variables, respec-
     spaces (F, µ) and (G, ν) in Mdisint , their independent
                                                                    tively; i.e., I ⊆ {X1 , . . . , Xm } and O ⊆ {Y1 , . . . , Yn } where
     combination (F , µ) · (G, ν) is a (necessarily unique)
                                                                    Y1 , . . . , Yn are output variables of M . We show that (I, O)-NI
     probability space (H, λ) such that H is the smallest σ-
                                                                    is equivalent to the following Hoare triple.
     algebra containing both F and G, and λ witnesses the
     independence of F and G, i.e., for any F ∈ F and G ∈ G,                {own ∆} M {Y. C (own(∆ \ I) ∗ own O)}
     λ(F ∩ G) = µ(F ) · ν(G). The unit element is the trivial                                       x←I

     probability space ({∅, Ω}, µ).                                 Here, we identify ∆ with the tuple of all input variables
   • The order relation (F , µ) ⊑ (G, ν) is defined by F ⊆ G        (X1 , . . . , Xm ). Without loss of generality, we assume that
     and µ = ν|F where ν|F is the restriction of ν to F.            input and output variables are {X1 , X2 } and {Y1 , Y2 }, respec-
   Conditioning modalities in Lilac are interpreted by disinte-     tively, and consider ({X1 }, {Y1 })-NI.
grations [38]. To ensure the existence of disintegrations, Lilac
formulas are interpreted using a submonoid Mdisint ⊆ Mind              2 The semantics of almost-sure equality presented in [29] contains a flaw
that imposes technical conditions on probability spaces (see        and was later corrected in the arXiv version. In this paper, we adopt the
[29, Section 3] for details).                                       corrected semantics. In fact, our results do not depend heavily on the semantics
                                                                    of almost-sure equality itself, since we use it primarily through syntactic
   The semantics of Lilac formulas Γ; ∆ ⊢ ϕ is defined by           inference rules, whose soundness has been proved under the corrected
the relation γ, D, P |= ϕ where γ ∈ JΓK is a valuation for          semantics.
    C-E NTAIL                                               C-S UBST
                               C-I NDEP                                                      C-OWN                          □-E LIM
       ϕ⊢ψ                                                                      as
                               own E ∗ ϕ ⊢ C ϕ              own X ⊢ C (X = x)               own E ⊢ C own E                 □ϕ ⊢ ϕ
     C ϕ⊢ C ψ                                 x←E                      x←X                               x←E
    x←E         x←E

  C-A ND -D ISTRIBUTIVE                        C-U NIF                                                            □-C ONJ
    C (ϕ ∧ ψ) ⊣⊢ C ϕ ∧ C ψ                     own X ∧ C (Y ∼ unif K) ⊢ own X ∗ (Y ∼ unif K)                      ϕ ∧ □ψ ⊢ ϕ ∗ □ψ
  x←X                  x←X       x←X                       x←X

                      U NIF -B IJECTION
                      Γ; X : K ⊢ E : K    E is bijective in X                     T RANSFER -OWN
                                                                                                    as
                                                                                  own E1 ∧ (E1 = E2 ) ⊢ own E2
                             X ∼ unif K ⊢ E ∼ unif K

Fig. 3: Selected inference rules for Lilac formulas [29]. See Fig. 12 in the appendix for a more comprehensive list of rules.
We omit obvious structural rules like commutativity and associativity of the separating conjunction ∗. Note that Lilac is an
affine separation logic, and thus ϕ ∗ ψ ⊢ ϕ holds.


                                                                                      H-L ET
     H-U NIF                                      H-R ET                              {P } M {X.Q}    ∀rv X.{Q} N {Y.R}
     {⊤} unif K {X.X ∼ unif K}                    {Q[E/X]} ret E {X.Q}                       {P } X ← M ; N {Y.R}

    H-F OR                                                                            H-C ONSEQ
            ∀i : index.∀rv X : A.{I(i, X)} M {X ′ .I(i + 1, X ′ )}                     P ⊢ P′        {P ′ } M {X.Q′ }       Q′ ⊢ Q
     {I(ns , E)} for (X ← E; i ← ns . . . ne ) {M } {X.I(ne + 1, X)}                                  {P } M {X.Q}

                                                      H-F RAME
                                                         {P } M {X.Q}   X∈  /R
                                                          {P ∗ R} M {X.Q ∗ R}

                                          Fig. 4: Inference rules for Hoare triples in Lilac [29]


Theorem V.1. Let X1 : A1 , X2 : A2 ⊢ M : G(B1 × B2 ) be                X2 . By (4), the output distribution of (Y1 , Y2 ) ← M ; ret Y1
an APPL program. We have                                               also satisfies the same conditional independence. Therefore,
                                                                       we have the desired Hoare triple for M .
 {own(X1 , X2 )} M {(Y1 , Y2 ). C (own X2 ∗ own Y1 )}
                                     x←X1
                                                       (3)               The idea of the proof itself is simple, but its formal proof
if and only if there exists a simulator X1 : A1 ⊢ Sim(M ) :            requires several technical lemmas on disintegrations and the
GB1 such that the following equation holds.                            semantics of Lilac. Details are given in Appendix B.

X1 : A1 , X2 : A2 ⊢ Sim(M ) = (Y1 , Y2 ) ← M ; ret Y1 : GB1                    VI. A DDITIONAL P ROOF RULES FOR L ILAC
                                                         (4)              The original Lilac paper [29] provides several proof rules,
   We give a proof sketch of Theorem V.1. We write Pr[Y |X]            which are summarized in Fig. 3. However, these rules are not
for the conditional probability distribution of Y given X.             sufficient for our purpose. In this section, we present additional
                                                                       proof rules that we use in Section VII. In particular, we show
Proof sketch. ( =⇒ ): By the Hoare triple for M , the input            that semi-graphoid axioms for conditional independence hold
(X1 , X2 ) and the output (Y1 , Y2 ) satisfy X2 ⊥ Y1 | X1 , which      in Lilac. We also provide composability rules for (I, O)-NI
implies Pr[Y1 |X1 , X2 ] = Pr[Y1 |X1 ]. Since Pr[Y1 |X1 , X2 ] is      properties as proof rules for Lilac.
the output probability distribution of (Y1 , Y2 ) ← M ; ret Y1
for given inputs X1 and X2 , the equation Pr[Y1 |X1 , X2 ] =           A. Semi-Graphoid Axioms for Conditional Independence
Pr[Y1 |X1 ] implies that (Y1 , Y2 ) ← M ; ret Y1 does not                 In the classical probability theory, conditional independence
actually depend on X2 . Therefore, we define Sim(M ) as                is known to satisfy the graphoid axioms [39]. Here, we show
follows where v : A2 is an arbitrary value.                            that a subset of the graphoid axioms, called semi-graphoid
                                                                       axioms, hold in Lilac.
  Sim(M )       :=     X2 ← ret v; (Y1 , Y2 ) ← M ; ret Y1 (5)
                                                                          Using the conventional notation X ⊥ Y | Z meaning
  ( ⇐= ): If a simulator Sim(M ) satisfying (4) exists, then           conditional independence of random variables X and Y given
we have X2 ⊥ Y1 | X1 because Sim(M ) does not depend on                Z, the semi-graphoid axioms are stated as follows.
  •  Symmetry: X ⊥ Y | Z implies Y ⊥ X | Z.                      Proposition VI.3. Theorem V.1 holds when we replace
  •  Decomposition: W ⊥ (X, Y ) | Z implies W ⊥ X | Z.           {P } M {X.Q} with {{P }} M {{X.Q}}.
  • Weak union: W ⊥ (X, Y ) | Z implies W ⊥ X | (Y, Z).
                                                                   In particular, (I, O)-NI property of an APPL program M
  • Contraction: W ⊥ X | Z and W ⊥ Y | (X, Z) together
                                                                 can be written as follows by Theorem V.1.
     imply W ⊥ (X, Y ) | Z.
In Lilac, these axioms can be written as follows.                         {{⊤}} M {{Y. C (own(∆ \ I) ∗ own O)}}
                                                                                         x←I
 C (own X ∗ own Y ) ⊢ C (own Y ∗ own X)                          C. Monotonicity
z←Z                         z←Z
 C (own W ∗ own(X, Y )) ⊢ C (own W ∗ own X)                         By the simulator-based definition of (I, O)-NI, it is straight-
z←Z                                z←Z                           forward to see that if M is (I, O)-NI, I ⊆ I ′ , and O ⊇ O′ ,
 C (own W ∗ own(X, Y )) ⊢ C              C (own W ∗ own X)       then M is also (I ′ , O′ )-NI. This gives rise to the following
z←Z                                z←Z y←Y
                                                                 proof rule.

 C (own W ∗ own X) ∧ C              C (own W ∗ own Y )                          I ⊆ I′ ⊆ ∆   Y ⊇ O ⊇ O′
z←Z                          z←Z x←X                                      {{⊤}} M {{Y. C (own(∆ \ I) ∗ own O)}}
      ⊢ C (own W ∗ own(X, Y ))                                                           x←I
       z←Z                                                               {{⊤}} M {{Y. C (own(∆ \ I ′ ) ∗ own O′ )}}
                                                                                        ′x←I
We show these entailments hold in Lilac’s semantics. By C-
E NTAIL and C-A ND -D ISTRIBUTIVE, it suffices to show these     This is a consequence of Theorem V.1, but we can also prove
entailments without the outermost conditioning modalities        it from semi-graphoid axioms.
Cz←Z . The symmetry axiom is immediate from the com-             Lemma VI.4. Suppose I ⊆ I ′ ⊆ ∆ and X ⊇ O ⊇ O′ . Then,
mutativity of the separating conjunction. The decomposition      we have the following.
axiom is also straightforward because own(X, Y ) ⊢ own X
holds. The weak union and contraction axioms are non-trivial,           (∆ \ I) ⊥ O | I        =⇒        (∆ \ I ′ ) ⊥ O′ | I ′
but they also hold as stated in the following proposition. The   Proof. Without loss of generality, we show the case where
proofs are given in Appendix C-A.                                both ∆ = {X1 , X2 , X3 } and Y = (Y1 , Y2 , Y3 ) consist of
Proposition VI.1. The following entailments hold.                three variables, and we have I = {X1 }, I ′ = {X1 , X2 },
                                                                 O = {Y1 , Y2 }, and O′ = {Y1 }. Then, we have the following.
          G EN -W EAK -U NION
          ϕ ∗ own(X, Y ) ⊢       C (ϕ ∗ own(X, Y ))                    X2 , X3 ⊥ Y1 , Y2 | X1
                                x:A←X
                                                                         =⇒ X2 , X3 ⊥ Y1 | X1              by decomposition
         C ONTRACTION
         (own W ∗ own X) ∧ C (own W ∗ own Y )                            =⇒ X3 ⊥ Y1 | X1 , X2                 by weak union
                                 x←X
                                                                 D. Composability for Sequential Composition
             ⊢ own W ∗ own(X, Y )
                                                                   Suppose we have two APPL programs ∆ ⊢ M : GA and
                                                                 ∆, X : A ⊢ N : GB whose output variables are tuples X
   Note that we slightly generalize the statements of the weak   and Y, respectively. Consider the sequential composition ∆ ⊢
union. It subsumes C-I NDEP as a special case when Y is a        X ← M ; N : GB.
trivial random variable over a singleton set and also subsumes                   ∆
C-OWN. When verifying noninterference properties of the                                                   N       Y
                                                                                            M
examples in Section VII, we often use G EN -W EAK -U NION                                            X
to introduce conditioning modalities.
                                                                 If M is (IM , OM )-NI and N is (IN , ON )-NI with OM ⊇
B. Hoare Triples with Ownership Assertions                       IN ∩ X, then the sequential composition X ← M ; N is
  When we write Hoare triples for APPL programs ∆ ⊢ M :          (IM ∪ (IN ∩ ∆), ON )-NI. We formalize this composability
GA, we often want to assume own ∆ in the precondition.           property as a proof rule in Lilac as follows. By monotonicity
Writing own ∆ explicitly in every Hoare triple is tedious,       of (I, O)-NI (Section VI-C), it suffices to consider the case
so we introduce a syntactic sugar for this purpose. For each     where OM = IN ∩ X and IM = IN ∩ ∆:
APPL program ∆ ⊢ M : GA, we define {{P }} M {{X.Q}} as                  M is (I, OM )-NI   N is (I ∪ OM , ON )-NI
syntactic sugar for                                                              X ← M ; N is (I, ON )-NI
         {P ∧ own ∆} M {X.Q ∧ own ∆ ∧ own X}.                    This gives rise to the following proof rule.
   We can use this syntactic sugar in the same way as the                {{⊤}} M {{X. C (own(∆\I) ∗ own OM )}}
                                                                                         w←I
original Hoare triples.
                                                                   {{⊤}} N {{Y.      C    (own(∆\I, X\OM ) ∗ own ON )}}
                                                                               (w,x)←(I,OM )
Proposition VI.2. All rules in Fig. 4 is sound when we replace
all occurrences of {P } M {X.Q} with {{P }} M {{X.Q}}.              {{⊤}} X ← M ; N {{Y. C (own(∆\I) ∗ own ON )}}
                                                                                               x←I
  Similarly to monotonicity, this is a consequence of Theo-              A DD R EP N OISE ER({Vi }i∈[l] , ρ)
rem V.1, but we can also prove it from semi-graphoid axioms.                {Xi,0 }i∈[l] ← {Vi }i∈[l]
                                                                            for i = 1, . . . , l do
Lemma VI.5. We have the following.                                              for irep = 1, . . . , r do
     (∆\I ⊥ OM | I) ∧ (∆\I, X\OM ⊥ ON | I, OM )                                     Yi,irep ← M INI A DD R EP N OISE(Xi,irep −1 , ρi,irep )
                                                                                    Xi,irep ← R EFRESH(Yi,irep )
       =⇒ ∆\I ⊥ ON | I                                                      return {Xi,r }i∈[l]
E. Composability for For-Loops                                        Fig. 5: AddRepNoiseER [32] in conventional pseudocode.
  Consider a for-loop for (Y ← E; i ← ns . . . ne ) {M }              Here, [l] = {1, 2, . . . , l}, and ρ = {ρi,irep }i∈[l],irep ∈[r] where
where Y = (Y1 , . . . , Yn ) is a tuple of random variables, and      ρi,irep = {ρi,irep ,j }j∈{0,...,t} and ρi,irep ,j : K.
∆, i : index, Y : B ⊢ M : B.
                                                                         M INI A DD R EP N OISE(V, ρ)
      ∆                                                                     for j = 0, . . . , t do
                E       M          M     ···     M        Y                     X j ← V j + ρj
                               Y
                      i = ns                    i = ne                      return X
                                                                         Fig. 6: MiniAddRepNoise in conventional pseudocode.
Let Ii ⊆ {1, . . . , n} be a subset of indices for each i =
ns , . . . , ne + 1, and let I be a subset of ∆. If (i) for each
i = ns , . . . , ne , M is (I ∪ {Yj }j∈Ii , {Yj′ }j∈Ii+1 )-NI where           VII. A PPLICATIONS TO P ROBING S ECURITY
Y′ = (Y1′ , . . . , Yn′ ) is the output of M , and (ii) for each
j ∈ Ins , free variables of Ej are in I, then the for-loop is            Raccoon [2] is a masking-friendly lattice-based signature
(I, {Yj }j∈Ine +1 )-NI where Y = (Y1 , . . . , Yn ) is used as the    scheme. Raccoon employs a sum-of-uniforms distribution as
output of the for-loop. This gives the following proof rule.          its noise source to address the difficulty of generating dis-
                                                                      crete Gaussian noise in a side-channel-resistant manner. An
                own Y|ns ⊢ own E|ns                                   algorithm called A DD R EP N OISE is used in Raccoon to add
 {{⊤}} M {{Y′ . C (own(∆\I, Y\Y|i ) ∗ own Y′ |i+1 )}}                 uniform noise to masked values.
              (x,y)←(I,Y|i )
                                                                         In this section, we demonstrate how Lilac can be used to
          {{⊤}} for (Y ← E; i ← ns . . . ne ) {M }                    prove the probing security of A DD R EP N OISE ER, a variant
               {{Y. C (own(∆\I) ∗ own Y|ne +1 )}}                     of A DD R EP N OISE that is used in the security proof of
                     x←I                                              Raccoon [32]. The algorithm A DD R EP N OISE ER (Fig. 5) adds
Here, we write Y|i for the tuple (Yj )j∈Ii and similarly for          uniform noise ρi,irep ,j to each share Vij using M INI A DD R EP -
Y′ |i and E|i . We can prove this either from Theorem V.1 or          N OISE (Fig. 6), and then refreshes the shares using the R E -
by semi-graphoid axioms.                                              FRESH algorithm (Fig. 8). This procedure is repeated r times
                                                                      for each of the l shared variables. The uniform noise ρi,irep ,j
F. Weakening                                                          is sampled externally and provided to A DD R EP N OISE ER
                                                                      as an unshared input (ER stands for Explicit Randomness).
   When composing programs, a component program often                 Below, we prove that A DD R EP N OISE ER satisfies the t-SNIU
uses only a subset of input variables. The situation can be           property (Definition III.4), which plays a central role in the
illustrated as follows.                                               security proof of Raccoon [32]. Following [32, Lemma 6.1],
                    X              M        Y                         the proof is divided into three parts.
                    Z                       Z                            After proving the security of A DD R EP N OISE ER, we
                                                                      present another example in which we prove the t-SNI property
In this case, we want to reason about the component program           of a masked multiplication algorithm [1].
M with the subset X of input variables and then extend the
result to the whole set of input variables X, Z. Specifically,        A. t-NIU of M INI A DD R EP N OISE
suppose that M is (I, O)-NI where I ⊆ X and O ⊆ Y. Then,                 We first prove the noninterference property of M INI A D -
we want to conclude that M is also (I ∪ Z, O ∪ Z)-NI for              D R EP N OISE [32], which is a subroutine used in A DD R EP -
any Z ⊆ Z. This gives rise to the following proof rule.               N OISE ER. The program in conventional pseudocode is shown
                                                                      in Fig. 6 and its APPL version with proof outline is shown in
          {{⊤}} M {{Y. C (own(X \ I) ∗ own O)}}                       Fig. 7. This algorithm takes a shared input V = (V 0 , . . . , V t )
                         x←I
∀rv Z.{{⊤}} M {{Y. C (own(X\I, Z\Z) ∗ own(O, Z))}}                    and an unshared input ρ = (ρ0 , . . . , ρt ). The output is
                    (x,z)←(I,Z)                                       X = (X 0 , . . . , X t ), and there are no internal variables.
Note that Z need not be independent of X. Hence, this is              Theorem VII.1. Let O ⊆ X be a set of probed variables
                                                                                                        shared         unshared
a different local reasoning principle from the frame rule in          such that |O| ≤ t. We define I = IMARN   (O) ∪ IMARN      (O)
                                                                           shared           j      j               unshared
probabilistic separation logic.                                       by IMARN (O) := {V | X ∈ O} and IMARN (O) :=
                                                                                   R EFRESH(A)
   { own(V, ρ) }                                                                      for i = 0, . . . , t do
   {I(0; 0) }                                                                             C0i ← Ai
                                                                                      for i = 0, . . . , t do
   for (X ← 0; j ← 0, . . . , t) {
                                                                                          for j = i + 1, . . . , t do
          { I(j; X) }                                                                         Ri,j ← unif K
          {⊤}                                 H-F RAME                                        Cji ← Cj−1  i
                                                                                                              + Ri,j
                         j
          ret X[V + ρj /X ]           j                                                       Ci+1 ← Cij − Ri,j
                                                                                                j

                         as                                                           return Ct = (Ct0 , . . . , Ctt )
          { X′ . X′ = X[V j + ρj /X j ] }
                         as                                                     Fig. 8: Algorithm R EFRESH [9] in conventional pseudocode.
          { X′ . X′ = X[V j + ρj /X j ] ∗ I(j; X) }
                ′                 ′                                             Subscripts for C are used to conform to single-assignment
          { X . I(j + 1; X ) }
                                                                                style but may be omitted if multiple assignments to C are
   }                                                                            allowed.
   { X. I(t + 1; X) }
   { X.              C            (own(V \ I, ρ \ I) ∗ own O) }                             as
                                                                                Since X j = v j + rj is deterministic, we have □ own X j
           (v,r)←(V∩I,ρ∩I)
                                                                                for each X j ∈ O. Thus, we obtain the desired postcondition.
      I(j; X)       :=        own(V, ρ, X) ∗    ∗ X =V +ρ
                                                k<j
                                                         k as     k
                                                                          k     Details of the proof are given in Appendix D-A.
                                                                                Remark VII.2. As explained in Section III-B, reasoning about
Fig. 7: Algorithm M INI A DD R EP N OISE in APPL. Gray lines                    noninterference properties in our approach requires exposing
show the proof outline for Theorem VII.1. We apply the H-                       internal variables. This typically does not undermine the local
F OR rule to the loop with the loop invariant I(j; X).                          reasoning principle of separation logic, because the internal
                                                                                variables exposed in earlier steps are not used in subsequent
                                                                                steps. Moreover, the frame rule allows us to frame out postcon-
{ρj | X j ∈ O} (here, “MARN” stands for MiniAddRepNoise).                       ditions concerning those internal variables. This is illustrated
Then, the following Hoare triple is derivable in Lilac, meaning                 by the use of H-F RAME in Fig. 7.
that M INI A DD R EP N OISE is (I, O)-NI.                                       Corollary VII.3. M INI A DD R EP N OISE is t-NIU.
      {own(V, ρ)}                                                               Proof. Immediate from Theorem VII.1.
                                                         j            j
      for (X ← 0; j ← 0, . . . , t) { ret X[V + ρj /X ] }                       B. t-SNI of R EFRESH
      {        C              (own(V \ I, ρ \ I) ∗ own O)}                         R EFRESH is an algorithm shown in Fig. 8 and used in
       (v,r)←(V∩I,ρ∩I)
                                                                                masked algorithms to ensure noninterference [9], [32]. The
Proof sketch. The outline of the proof is shown in Fig. 7. It is                input is a shared variable A = (A0 , . . . , At ), and the output
straightforward to see that the following postcondition holds                   is Ct = (Ct0 , . . . , Ctt ) such that Ct and A represent the same
after executing the program by considering the loop invariant                   secret value. The internal variables are {Ri,j }0≤i<j≤t and
I(j; X) defined in the figure.                                                  {Cji }0≤i≤t,0≤j<t .
                                                as                              Theorem VII.4. Consider R EFRESH in Fig. 8. Let O ⊆
                    (own V ∧ own ρ) ∗ X = V + ρ
                                                                                {Ri,j | i, j ∈ {0, . . . , t}, i < j} ∪ {Cji | i, j ∈ {0, . . . , t}}
We can show that this implies the desired postcondition. By                     be a set of probed variables such that |O| ≤ t. We define
G EN -W EAK -U NION, we have the following entailment.                          I = IRefresh (O) ⊆ {A0 , . . . , At } as follows.
                                 as                                               IRefresh (O)         :=         {Ai | ∃j.Ri,j ∈ O ∨ ∃j < t.Cji ∈ O}
          own(V, ρ) ∗ X = V + ρ
                                                         as                     Then, the following Hoare triple is derivable in Lilac, meaning
          ⊢           C               (own(V, ρ) ∗ X = V + ρ)
              (v,r)←(V∩I,ρ∩I)                                                   that R EFRESH is (I, O)-NI.

By C-S UBST, we also have the following entailment.                             {own A} R EFRESH {(C, R). C (own(A \ I) ∗ own O)}
                                                                                                                          a←I

  own(V, ρ) ⊢
                                ^        as         as
                                    (v j = V j ∧ rj = ρj )                      Proof sketch. The outline of the proof is shown in Fig. 9. It is
                     C
                     (v,r)←(V∩I,ρ∩I)                                            straightforward to show that the following postcondition holds.
                                           X j ∈O

Then, it follows that the following entailment holds.
                                                                                    own A ∗      ∗ (R ∼ unif K) ∗ ∗(C = A + f (R))
                                                                                                 i<j
                                                                                                            i,j
                                                                                                                                i,j
                                                                                                                                      i as
                                                                                                                                      j
                                                                                                                                             i    i
                                                                                                                                                  j


 own(V, ρ) ∗ X = V + ρ
                         as                                                     where fji (R) is a function defined as follows.
                                                                 as
                                                     ^                                           ( P
  ⊢        C             (own(V \ I, ρ \ I) ∧                X j = v j + rj )          i           − k<j Rk,i                                    i≥j
  (v,r)←(V∩I,ρ∩I)
                                                    X j ∈O
                                                                                     fj (R) :=       P             P                                   (6)
                                                                                                   − k<i Rk,i + i<k≤j Ri,k                       i<j
        { own A }
        { I(0, 1; (A, 0, . . . , 0), 0) }
        for ( (C′ , R′ ) ← ((A, 0, . . . , 0), 0); i ← 0, . . . , t ) {
              for ( (C, R) ← (C′ , R′ ); j ← i + 1, . . . , t ) {
                     { I(i, j; C, R) }
                     {⊤}                                                                                                  H-F RAME
                     S ← unif K;
                     { S. S ∼ unif K }
                                 i
                     ret (C, R)[Cj−1 + S/Cji , Cij − S/Ci+1
                                                        j
                                                            , S/Ri,j ]
                                                                         as
                     { (C′′ , R′′ ). S ∼ unif K ∗ (C′′ , R′′ ) = (C, R)[Cj−1
                                                                         i                      j
                                                                             + S/Cji , Cij − S/Ci+1 , S/Ri,j ] }
                                                                         as
                     { (C′′ , R′′ ). S ∼ unif K ∗ (C′′ , R′′ ) = (C, R)[Cj−1
                                                                         i                      j
                                                                             + S/Cji , Cij − S/Ci+1 , S/Ri,j ] ∗ I(i, j; C, R) }
                     { (C′′ , R′′ ). I(i, j + 1; C′′ , R′′ ) }
              }
        }
        { (C, R). I(t, t + 1; C, R) }
        { (C, R). own A ∗          ∗ (R ∼ unif K) ∗ ∗(C = A + f (R)) }
                                   i<j
                                             i,j
                                                                  i,j
                                                                          i as
                                                                          j
                                                                                      i     i
                                                                                            j

        { (C, R). C (own(A \ I) ∗ own O) }
                      a←I


                                         ∗C = A ∗ ∗                                                                                 ′              ′
                                                                                                           ′ as  ′     ′                   ′
                                                                                                                                                          
                                               i as                                                                                     as
I(i, j; C, R)      :=     own A ∗              0
                                                      i
                                                                                     Ri′ ,j ′ ∼ unif K ∗ Cji′ = Ai + fji′ (R) ∗ Cij′ +1 = Aj + fij′ +1 (R)
                                         i                (i′ ,j ′ )<lex (i,j)
                                                            0≤i′ <j ′ ≤t


Fig. 9: Algorithm R EFRESH in APPL. Here, R is a shorthand for the collection of random variables Ri,j , and C = (C0 , . . . , Ct )
where Ci = (Ci0 , . . . , Cit ) for each i. Gray comments show the proof outline for Theorem VII.4. In the invariant, <lex denotes
the lexicographic order on pairs of integers (i, j) such that i < j, and fji (R) is a function defined in (6).


We can derive the desired postcondition by translating the                                tively. For each i and irep , we define Ji,irep ⊆ Yi,irep ,
                                                                                            shared                     unshared
proof in [9] into Lilac. See Appendix D-B for details.                                    Ii,i rep
                                                                                                   ⊆ Xi,irep −1 , and Ii,i rep
                                                                                                                                ⊆ ρi,irep as follows.
                                                                                                                                 shared        Refresh
                                                                                                     Ji,irep   :=     IRefresh (Ii,i rep +1
                                                                                                                                            ∪ Oi,i     )
Corollary VII.5. R EFRESH is t-SNI.                                                                                                               rep
                                                                                                     shared            shared             MARN
                                                                                                    Ii,irep
                                                                                                               :=     IMARN   (Ji,irep ∪ Oi,irep
                                                                                                                                                 )
Proof. By Theorem VII.4, for each set of probes O with |O| ≤                                       unshared            shared             MARN
t, there exists a set of inputs I with |I| smaller than or equal                                  Ii,irep
                                                                                                               :=     IMARN   (Ji,irep ∪ Oi,i rep
                                                                                                                                                  )
to internal probes in O such that R EFRESH is (I, O)-NI.                                                   shared :=
                                                                                          Here, we define Ii,r+1     ∅. Let I be defined as follows.
                                                                                                                                   [
C. t-SNIU of A DD R EP N OISE with Explicit Randomness                                          I := {Vik | Xi,0   k     shared
                                                                                                                     ∈ Ii,0     }∪       unshared
                                                                                                                                       Ii,irep
                                                                                                                                        i,irep
   A DD R EP N OISE ER is shown in Fig. 5. Here, we write [l] =
{1, 2, . . . , l}. The shared input is Vi = (Vi0 , . . . , Vit ) for i =                  Then, A DD R EP N OISE ER is (I, O)-NI.
1, . . . , n, and the unshared input is ρ = {ρi,irep }i∈[l],irep ∈[r]                     Proof. By using composability for sequential composition and
where ρi,irep = {ρi,irep ,j }j∈{0,...,t} and ρi,irep ,j : K. For                          for-loop with Theorem VII.4 and VII.1.
                                      0                t
each i and irep , Xi,irep = (Xi,i       rep
                                            , . . . , Xi,i rep
                                                               ) and Yi,irep =
    0                t
(Yi,irep , . . . , Yi,irep ) are used as internal or output variables.                    Corollary VII.7. A DD R EP N OISE ER is t-SNIU.
   We can prove that A DD R EP N OISE ER in Fig. 5 is t-SNIU                              D. t-SNI of S EC M ULT
by using the composability of NI discussed in Section VI.
                                                                                            The multiplication algorithm [1] is another basic building
Theorem VII.6. Let O be a set of probed variables such that                               block for masked algorithms. In Fig. 10, S EC M ULT takes
                     Refresh       MARN
|O| ≤ t. We write Oi,i rep
                             and Oi,i rep
                                             for the subsets of O                         two shared inputs A = (A0 , . . . , At ) and B = (B 0 , . . . , B t )
consisting of probed variables in the execution of R EFRESH                               and returns a shared output Ct = (Ct0 , . . . , CtP
                                                                                                                                            t
                                                                                                                                              ) such that
                                                                                                                                                t        i
and M INI A DD R EP N OISE in the (i, irep )-th iteration, respec-                        Ct represents the product of A and B, i.e.,           i=0 Ct =
   S EC M ULT(A, B)                                                  define KQ , KS ⊆ {(i, j) | 0 ≤ i < j ≤ t} as follows.
      for i = 0, . . . , t do
          for j = 0, . . . , t do                                              KQ := {(i, j) | Qi,j ∈ O ∨ Ri,j ∈ O}
                Pi,j ← Ai × B j                                                          ∪ {(i, k) | Cji ∈ O, j < t, i < k}
      (C0 , . . . , C0t ) ← (P0,0 , . . . , Pt,t )
         0
                                                                               KS := {(i, j) | Si,j ∈ O}
      for i = 0, . . . , t do
                                                                                         ∪ {(k, i) | Cji ∈ O, j < t, k < i}
          for j = i + 1, . . . , t do
                Qi,j ← unif K                                        The set KC is defined so that (a) KC bijectively corresponds
                Cji ← Cj−1 i
                               − Qi,j                                to the set {Cti ∈ O | ¬(∃j < t, Cji ∈ O)} and (b) for each
                Ri,j ← Qi,j + Pi,j                                   (i′ , j ′ ) ∈ KC corresponds to Cti , the uniform random variable
                Si,j ← Ri,j + Pj,i                                   Qi′ ,j ′ occurs in gti (Q, S). We can define such KC because
                    j
                Ci+1     ← Cij + Si,j                                we have |O ∩ Ct | ≤ |Vi \ (KQ ∪ KS )| for each Cti ∈ O
      return Ct = (Ct0 , . . . , Ctt )                               with no j < t such that Cji ∈ O, where Vi = {(k, i) | k <
                                                                     i} ∪ {(i, k) | i < k} is the indices of the free variables in
Fig. 10: Algorithm S EC M ULT in conventional pseudocode.            gti (Q, S).
Unlike the presentation in [9], our version computes Pi,j ←              We can then show that (a) {Cti ∈ O | ¬(∃j < t, Cji ∈ O)}
Ai × B j for all i, j in advance, since we need to assign a          can be “simulated” by sampling from the uniform distribution,
distinct variable name to each Ai × B j for the proof.               (b) {Si,j | (i, j) ∈ KS \ KQ } can be “simulated” by sampling
                                                                     from the uniform distribution, and (c) the rest of the variables
 Pt            Pt                                                    in O can be “simulated” from {Si,j | (i, j) ∈ KS \ KQ },
( i=0 Ai ) × ( i=0 B i ). It is proved in [9] that S EC M ULT        {Qi,j | (i, j) ∈ KQ }, and I ∪ J . In Lilac, (a) and (b)
is t-SNI. We show that by Theorem V.1, this result can be            correspond to applying U NIF -B IJECTION, and (c) corresponds
proved in Lilac as well.                                             to applying T RANSFER -OWN. See Appendix D-C for de-
                                                                     tails.
Theorem VII.8. Let O be a set of probed variables.
                                                                     Corollary VII.9. S EC M ULT is t-SNI.
         I1 := {i | Pi,j ∈ O} ∪ {i | Cji ∈ O ∧ j < t}                                     VIII. R ELATED W ORK
         J1 := {j | Pi,j ∈ O} ∪ {i | Cji ∈ O ∧ j < t}                      a) Probabilistic separation logic: Probabilistic separa-
  (I2 , J2 ) := Add(I1 , J1 ; {(i, j) | Qi,j ∈ O ∨ Ri,j ∈ O})        tion logic [21] is extended in various ways to support more ex-
  (I3 , J3 ) := Add(I2 , J2 ; {(i, j) | Si,j ∈ O})                   pressive reasoning about probabilistic programs. Some works
                                                                     support reasoning about conditional independence, such as
Here, for each I, J ⊆ {0, . . . , t} and K ⊆ {0, . . . , t}2 ,       Lilac [29], DIBI [23], BaSL [24], and BlueBell [25]. Other
Add(I, J; K) is the pair (I ′ , J ′ ) defined as follows.            works interpret separating conjunction in different ways: cryp-
                                                                     tographic probabilistic separation logic [27] interprets it as
                                                                     computational independence, while LINA [28] provides a
I ′ := I ∪ {i | (i, j) ∈ K ∧ i ∈
                               / I} ∪ {j | (i, j) ∈ K ∧ i ∈ I}
  ′
                                                                     separating conjunction for negative association. Probabilistic
J := J ∪ {j | (i, j) ∈ K ∧ j ∈  / J} ∪ {i | (i, j) ∈ K ∧ j ∈ J}      concurrent outcome logic (pcOL) [26] combines probabilis-
                                                                     tic separation logic with concurrent separation logic [40]
Let I := I3 , J := J3 , and I = {Ai | i ∈ I}, J = {B j | j ∈         to reason about probabilistic concurrent programs. Some of
J}. Then, S EC M ULT is (I ∪ J , O)-NI.                              the above logics have been applied to verify cryptographic
                                                                     algorithms [21], [25], [27], [29]. However, none of these
Proof sketch. We rephrase the simulator-based proof in [9]
                                                                     logics has been used to verify t-noninterference of masked
as a conditional-independence-based proof in Lilac. We first
                                                                     algorithms.
apply the rules in Fig. 4 to obtain a postcondition that
                                                                           b) Formal verification of masked programs: Formal veri-
expresses how each variable is computed from the inputs and
                                                                     fication of probing security has been actively studied in recent
the random variables. This step is rather straightforward, and
                                                                     years [9]–[20], [41], [42]. MASK V ERIF [10], [11] repeatedly
the proof sketch is shown in Fig. 11. Here, gji (Q, S) is defined
                                                                     substitute expressions in masked programs to prove noninter-
as follows.
                                                                     ference, based on the fact that applying bijective functions f to
                    (P                                               uniform random variables X gives uniform random variables
        i                   Sk,i                     i≥j
       gj (Q, S) := Pk<j           P                           (7)   f (X) as well. Lilac has an inference rule (U NIF -B IJECTION)
                        k<i Sk,i +    i<k≤j Qi,k     i<j             that captures this fact, which allows us to use the simulated
                                                                     their noninterference proof as a proof in Lilac. Substitution-
Then, we apply the H-C ONSEQ rule to obtain the desired              based approaches have also been used in [20]. Another line of
postcondition, which is the non-trivial part of the proof.           work uses inference-based approaches [12]–[14], [41], [42],
   We divide (the indices of) the uniform random variables Q         which infer distribution types for each intermediate values in
into four parts: KQ , KS \ KQ , KC , and the rest. Here, we          masked programs.
  { own(A, B) }
  P ← for (P ← 0; i ← 0, . . . , t) {
       for (P′ ← P; j ← 0, . . . , t) { ret P′ [Ai × B j /Pi,j
                                                           ′
                                                               ]}
  };
  { P. own(A, B) ∗ ∗P = A × B }
                           i,j
                                  i,j
                                            as    i           j


  { P. own(A, B) ∗ ∗ P = A × B ∗ I(0, 1; ((P ) , 0, . . . , 0), 0, 0, 0) }
                                            as    i           j                                    t
                                  i,j                                                          i,i i=0
                           i,j
  (C, Q, R, S) ← for ((C, Q, R, S) ← (((Pi,i )ti=0 , 0, . . . , 0), 0, 0, 0); i ← 0, . . . , t) {
       for ((C′ , Q′ , R′ , S′ ) ← (C, Q, R, S); j ← i + 1, . . . , t) {
            { own(A, B) ∗               ∗ P = A × B ∗ I(i, j; C , Q , R , S ) }
                                        i,j
                                                 i,j
                                                        as        i              j                        ′         ′         ′   ′


            Q′′i,j ← unif K;
                i                       i                                                                                                                                        j        j
            C ′′ j ← ret (C ′ j−1 − Q′′i,j ); Ri,j
                                               ′′
                                                   ← ret (Q′′i,j + Pi,j ); Si,j
                                                                            ′′          ′′
                                                                                ← ret (Ri,j + Pj,i ); C ′′ i+1 ← ret (C ′ i + Sj,i
                                                                                                                               ′′
                                                                                                                                   );
                                                        i             i          j              j
            ret (C′ , Q′ , R′ , S′ )[C ′′ j /C ′ j , C ′′ i+1 /C ′ i+1 , Q′′i,j /Q′i,j , Ri,j
                                                                                          ′′    ′
                                                                                              /Ri,j    ′′
                                                                                                    , Sj,i   ′
                                                                                                           /Sj,i ]
            { (C′′ , Q′′ , R′′ , S′′ ). own(A, B) ∗                                  ∗ P = A × B ∗ I(i, j + 1; C , Q , R , S ) }
                                                                                     i,j
                                                                                              i,j
                                                                                                    as        i               j               ′′     ′′        ′′         ′′


       }
  };
  { own(A, B) ∗     ∗ P = A × B ∗ I(t, t + 1; C, Q, R, S) }
                     i,j
                            i,j
                                  as         i          j


  ret (P, C, Q, R, S)
  { (P, C, Q, R, S). own(A, B) ∗        ∗ P = A × B ∗ ∗ Q ∼ unif K ∗ ∗ R = Q + P
                                                        i,j
                                                                      i,j
                                                                            as        i             j
                                                                                                          i<j
                                                                                                                        i,j
                                                                                                                                           i<j
                                                                                                                                                   i,j
                                                                                                                                                          as
                                                                                                                                                                    i,j        i,j


                                  ∗ ∗ S = R + P ∗ ∗ C = P + g (Q, S) }
                                                        as                                               i as                     i
                                                  i,j             i,j                j,i                 j              i,i       j
                                        i<j                                                   i,j
  { (P, C, Q, R, S).              C              (own(A \ I, B \ J ) ∗ own O) }
                           (a,b)←(I,J )



                                                                                          ∗
                                                                                                              
                                                 as                                                                                                 as                               as
 I(i, j; C, Q, R, S)        :=          C0 = (Pi,i )ti=0 ∗                                                        Qi′ ,j ′ ∼ unif K ∗ Ri′ ,j ′ = Qi′ ,j ′ + Pi′ ,j ′ ∗ Si′ ,j ′ = Ri′ ,j ′ + Pj ′ ,i′
                                                                                 (i′ ,j ′ )<lex (i,j)
                                                                                   0≤i′ <j ′ ≤t
                                                                                                                                                    ′
                                                                                                                                                                       j′
                                                                                                                   ′ as             ′
                                                                                                                                                                                  
                                                                                                                                                        as
                                                                                                              ∗ Cji′ = Pi′ ,i′ + gji ′ (Q, S) ∗ Cij′ +1 = Pj ′ ,j ′ + gi+1′ (Q, S)




Fig. 11: Algorithm S EC M ULT in APPL. Here, Q, R, and S are shorthands for the collection of random variables {Qi,j | 0 ≤
i < j ≤ t}, {Ri,j | 0 ≤ i < j ≤ t}, and {Si,j | 0 ≤ i < j ≤ t}, respectively; and C = (C0 , . . . , Ct ) where Ci = (Ci0 , . . . , Cit )
for each i. Gray comments show the proof outline for Theorem VII.8, but we omit some straightforward proof steps for brevity.
The function gji (Q, S) is defined as in (7). The loop invariant for the second loop is denoted as I(i, j; C, Q, R, S).


   When proving noninterference properties of masked al-                                                                      definition of (I, O)-NI is equivalent to a Hoare triple in Lilac
gorithms, one must in principle consider all possible sets                                                                    that asserts a certain conditional independence. We have also
of probed variables O. This combinatorial explosion can                                                                       provided several proof rules that facilitate the verification
be problematic, especially when pursuing algorithmic proof                                                                    of probing security and demonstrated their application to
search [10]. However, in the setting of formal verification with                                                              R EFRESH and A DD R EP N OISE ER.
an interactive theorem prover, this issue can be avoided by                                                                      Our current results focus on the information-theoretic set-
representing the set of probed variables symbolically. This is                                                                ting of probing security. As future work, we want to extend our
the approach adopted in this work.                                                                                            approach to the computational setting by adopting the ideas
                                                                                                                              from [27]. Implementing our method in an interactive theorem
           IX. C ONCLUSION AND F UTURE W ORK                                                                                  prover is another important direction for future work. We also
  We have presented a method for formally verifying probing                                                                   want to explore applications of our method to the verification
security using Lilac. We have shown that the simulator-based                                                                  of other cryptographic algorithms, such as secure multi-party
computation protocols, since Theorem V.1 would be applicable                     [14] P. Gao, H. Xie, J. Zhang, F. Song, and T. Chen, “Quantitative
to other security properties defined in terms of simulators as                        Verification of Masked Arithmetic Programs Against Side-Channel
                                                                                      Attacks,” in Tools and Algorithms for the Construction and Analysis
well.                                                                                 of Systems, ser. Lecture Notes in Computer Science, vol. 11427.
                                                                                      Cham: Springer International Publishing, 2019, pp. 155–173. [Online].
                              R EFERENCES                                             Available: http://link.springer.com/10.1007/978-3-030-17462-0 9
                                                                                 [15] P. Gao, F. Song, and T. Chen, “Compositional Verification of First-
 [1] Y. Ishai, A. Sahai, and D. Wagner, “Private Circuits: Securing Hardware          Order Masking Countermeasures against Power Side-Channel Attacks,”
     against Probing Attacks,” in Advances in Cryptology - CRYPTO 2003,               ACM Transactions on Software Engineering and Methodology,
     ser. Lecture Notes in Computer Science, vol. 2729. Berlin, Heidelberg:           vol. 33, no. 3, pp. 1–38, Mar. 2024. [Online]. Available: https:
     Springer Berlin Heidelberg, 2003, pp. 463–481. [Online]. Available:              //dl.acm.org/doi/10.1145/3635707
     http://link.springer.com/10.1007/978-3-540-45146-4 27                       [16] H. Eldib, C. Wang, and P. Schaumont, “Formal Verification of Software
 [2] R. Del Pino, T. Espitau, S. Katsumata, M. Maller, F. Mouhartem,                  Countermeasures against Side-Channel Attacks,” ACM Transactions on
     T. Prest, M. Rossi, and M.-J. Saarinen, “Raccoon,” National Institute of         Software Engineering and Methodology, vol. 24, no. 2, pp. 1–24, Dec.
     Standards and Technology, Technical Report, 2023. [Online]. Available:           2014. [Online]. Available: https://dl.acm.org/doi/10.1145/2685616
     https://csrc.nist.gov/Projects/pqc-dig-sig/round-1-additional-signatures    [17] J.-S. Coron, “Formal Verification of Side-Channel Countermeasures
 [3] J.-S. Coron, F. Gérard, M. Trannoy, and R. Zeitoun, “Improved Gadgets           via Elementary Circuit Transformations,” in Applied Cryptography and
     for the High-Order Masking of Dilithium,” IACR Transactions on                   Network Security, ser. Lecture Notes in Computer Science, vol. 10892.
     Cryptographic Hardware and Embedded Systems, vol. 2023, no. 4, pp.               Cham: Springer International Publishing, 2018, pp. 65–82. [Online].
     110–145, Aug. 2023. [Online]. Available: https://tches.iacr.org/index.           Available: https://link.springer.com/10.1007/978-3-319-93387-0 4
     php/TCHES/article/view/11160                                                [18] R. Bloem, H. Gross, R. Iusupov, B. Könighofer, S. Mangard, and
 [4] J.-S. Coron, F. Gérard, T. Lepoint, M. Trannoy, and R. Zeitoun,                 J. Winter, “Formal Verification of Masked Hardware Implementations
     “Improved High-Order Masked Generation of Masking Vector and                     in the Presence of Glitches,” in Advances in Cryptology – EUROCRYPT
     Rejection Sampling in Dilithium,” IACR Transactions on Cryptographic             2018, ser. Lecture Notes in Computer Science, vol. 10821. Cham:
     Hardware and Embedded Systems, vol. 2024, no. 4, pp. 335–354,                    Springer International Publishing, 2018, pp. 321–353. [Online].
     Sep. 2024. [Online]. Available: https://tches.iacr.org/index.php/TCHES/          Available: https://link.springer.com/10.1007/978-3-319-78375-8 11
     article/view/11795                                                          [19] D. Knichel, P. Sasdrich, and A. Moradi, “SILVER – Statistical
 [5] J. Hermelink, K.-C. Ning, and R. Petri, “Finding and Protecting the              Independence and Leakage Verification,” in Advances in Cryptology –
     Weakest Link - On Side-Channel Attacks on y in Masked ML-DSA,” in                ASIACRYPT 2020, ser. Lecture Notes in Computer Science, vol. 12491.
     Advances in Cryptology – CRYPTO 2025, (to appear), 2025, pp. xx–xx.              Cham: Springer International Publishing, 2020, pp. 787–816. [Online].
 [6] National Institute of Standards and Technology (US), “Module-lattice-            Available: https://link.springer.com/10.1007/978-3-030-64837-4 26
     based digital signature standard,” National Institute of Standards and      [20] Q. L. Meunier, E. Pons, and K. Heydemann, “LeakageVerif:
     Technology (U.S.), Washington, D.C., Tech. Rep. NIST FIPS 204,                   Efficient and Scalable Formal Verification of Leakage in Symbolic
     Aug. 2024. [Online]. Available: https://nvlpubs.nist.gov/nistpubs/FIPS/          Expressions,” IEEE Transactions on Software Engineering, vol. 49,
     NIST.FIPS.204.pdf                                                                no. 6, pp. 3359–3375, Jun. 2023. [Online]. Available: https:
 [7] T. Prest, “A Key-Recovery Attack Against Mitaka in the t-                        //ieeexplore.ieee.org/document/10059223/
     Probing Model,” in Public-Key Cryptography – PKC 2023, ser.                 [21] G. Barthe, J. Hsu, and K. Liao, “A probabilistic separation
     Lecture Notes in Computer Science, vol. 13940. Cham: Springer                    logic,” Proceedings of the ACM on Programming Languages,
     Nature Switzerland, 2023, pp. 205–220. [Online]. Available: https:               vol. 4, no. POPL, pp. 1–30, Jan. 2020. [Online]. Available:
     //link.springer.com/10.1007/978-3-031-31368-4 8                                  https://dl.acm.org/doi/10.1145/3371123
 [8] J.-S. Coron, E. Prouff, M. Rivain, and T. Roche, “Higher-Order Side         [22] J. Reynolds, “Separation logic: A logic for shared mutable data
     Channel Security and Mask Refreshing,” in Fast Software Encryption,              structures,” in Proceedings 17th Annual IEEE Symposium on Logic
     ser. Lecture Notes in Computer Science, vol. 8424. Berlin, Heidelberg:           in Computer Science. Copenhagen, Denmark: IEEE Computer
     Springer Berlin Heidelberg, 2014, pp. 410–424. [Online]. Available:              Society, 2002, pp. 55–74. [Online]. Available: http://ieeexplore.ieee.org/
     https://link.springer.com/10.1007/978-3-662-43933-3 21                           document/1029817/
 [9] G. Barthe, S. Belaı̈d, F. Dupressoir, P.-A. Fouque, B. Grégoire,           [23] J. Bao, S. Docherty, J. Hsu, and A. Silva, “A Bunched Logic
     P.-Y. Strub, and R. Zucchini, “Strong Non-Interference and Type-                 for Conditional Independence,” in 2021 36th Annual ACM/IEEE
     Directed Higher-Order Masking,” in Proceedings of the 2016 ACM                   Symposium on Logic in Computer Science (LICS). Rome, Italy: IEEE,
     SIGSAC Conference on Computer and Communications Security.                       Jun. 2021, pp. 1–14. [Online]. Available: https://ieeexplore.ieee.org/
     Vienna Austria: ACM, Oct. 2016, pp. 116–129. [Online]. Available:                document/9470712/
     https://dl.acm.org/doi/10.1145/2976749.2978427                              [24] S. H. Ho, N. Wu, and A. Raad, “Bayesian Separation Logic:
[10] G. Barthe, S. Belaı̈d, F. Dupressoir, P.-A. Fouque, B. Grégoire,                A Logical Foundation and Axiomatic Semantics for Probabilistic
     and P.-Y. Strub, “Verified Proofs of Higher-Order Masking,” in                   Programming,” Proceedings of the ACM on Programming Languages,
     Advances in Cryptology – EUROCRYPT 2015, ser. Lecture Notes                      vol. 10, no. POPL, pp. 1557–1585, Jan. 2026. [Online]. Available:
     in Computer Science, vol. 9056. Berlin, Heidelberg: Springer                     https://dl.acm.org/doi/10.1145/3776696
     Berlin Heidelberg, 2015, pp. 457–485. [Online]. Available: http:            [25] J. Bao, E. D’Osualdo, and A. Farzan, “Bluebell: An Alliance of
     //link.springer.com/10.1007/978-3-662-46800-5 18                                 Relational Lifting and Independence for Probabilistic Reasoning,”
[11] G. Barthe, S. Belaı̈d, G. Cassiers, P.-A. Fouque, B. Grégoire, and              Proceedings of the ACM on Programming Languages, vol. 9,
     F.-X. Standaert, “maskVerif: Automated Verification of Higher-Order              no. POPL, pp. 1719–1749, Jan. 2025. [Online]. Available: https:
     Masking in Presence of Physical Defaults,” in Computer Security –                //dl.acm.org/doi/10.1145/3704894
     ESORICS 2019, ser. Lecture Notes in Computer Science, vol. 11735.           [26] N. Zilberstein, A. Silva, and J. Tassarotti, “Probabilistic Concurrent
     Cham: Springer International Publishing, 2019, pp. 300–318. [Online].            Reasoning in Outcome Logic: Independence, Conditioning, and
     Available: https://link.springer.com/10.1007/978-3-030-29959-0 15                Invariants,” Proceedings of the ACM on Programming Languages,
[12] J. Zhang, P. Gao, F. Song, and C. Wang, “SCInfer: Refinement-                    vol. 10, no. POPL, pp. 235–264, Jan. 2026. [Online]. Available:
     Based Verification of Software Countermeasures Against Side-                     https://dl.acm.org/doi/10.1145/3776651
     Channel Attacks,” in Computer Aided Verification, ser. Lecture Notes        [27] U. Dal Lago, D. Davoli, and B. M. Kapron, “On Separation Logic,
     in Computer Science, vol. 10982. Cham: Springer International                    Computational Independence, and Pseudorandomness,” in 2024 IEEE
     Publishing, 2018, pp. 157–177. [Online]. Available: http://link.springer.        37th Computer Security Foundations Symposium (CSF). Enschede,
     com/10.1007/978-3-319-96142-2 12                                                 Netherlands: IEEE, Jul. 2024, pp. 80–95. [Online]. Available:
[13] P. Gao, H. Xie, F. Song, and T. Chen, “A Hybrid Approach to                      https://ieeexplore.ieee.org/document/10664346/
     Formal Verification of Higher-Order Masked Arithmetic Programs,”            [28] J. Bao, M. Gaboardi, J. Hsu, and J. Tassarotti, “A separation logic
     ACM Transactions on Software Engineering and Methodology,                        for negative dependence,” Proceedings of the ACM on Programming
     vol. 30, no. 3, pp. 1–42, Jul. 2021. [Online]. Available: https:                 Languages, vol. 6, no. POPL, pp. 1–29, Jan. 2022. [Online]. Available:
     //dl.acm.org/doi/10.1145/3428015                                                 https://dl.acm.org/doi/10.1145/3498719
[29] J. M. Li, A. Ahmed, and S. Holtzen, “Lilac: A Modal Separation Logic
     for Conditional Probability,” Proceedings of the ACM on Programming
     Languages, vol. 7, no. PLDI, pp. 148–171, Jun. 2023. [Online].
     Available: https://dl.acm.org/doi/10.1145/3591226
[30] J. M. Li, J. Aytac, P. Johnson-Freyd, A. Ahmed, and S. Holtzen, “A
     Nominal Approach to Probabilistic Separation Logic,” in Proceedings
     of the 39th Annual ACM/IEEE Symposium on Logic in Computer
     Science. Tallinn Estonia: ACM, Jul. 2024, pp. 1–14. [Online].
     Available: https://dl.acm.org/doi/10.1145/3661814.3662135
[31] G. Cassiers and F.-X. Standaert, “Trivially and Efficiently Composing
     Masked Gadgets With Probe Isolating Non-Interference,” IEEE
     Transactions on Information Forensics and Security, vol. 15, pp. 2542–
     2555, 2020. [Online]. Available: https://ieeexplore.ieee.org/document/
     8979162/
[32] R. Del Pino, S. Katsumata, T. Prest, and M. Rossi, “Raccoon:
     A Masking-Friendly Signature Proven in the Probing Model,” in
     Advances in Cryptology – CRYPTO 2024, ser. Lecture Notes in
     Computer Science, vol. 14920. Cham: Springer Nature Switzerland,
     2024, pp. 409–444. [Online]. Available: https://link.springer.com/10.
     1007/978-3-031-68376-3 13
[33] C. E. Shannon, “Communication Theory of Secrecy Systems,” Bell
     System Technical Journal, vol. 28, no. 4, pp. 656–715, Oct. 1949.
     [Online]. Available: https://ieeexplore.ieee.org/document/6769090
[34] M. F. Esgin, T. Espitau, G. Niot, T. Prest, A. Sakzad, and R. Steinfeld,
     “plover: Masking-friendly hash-and-sign lattice signatures,” in Advances
     in Cryptology – EUROCRYPT 2024, ser. Lecture Notes in Computer
     Science, vol. 14657. Cham: Springer Nature Switzerland, 2024,
     pp. 316–345. [Online]. Available: https://link.springer.com/10.1007/
     978-3-031-58754-2 12
[35] G. Barthe, S. Belaı̈d, T. Espitau, P.-A. Fouque, B. Grégoire, M. Rossi,
     and M. Tibouchi, “Masking the GLP Lattice-Based Signature Scheme
     at Any Order,” in Advances in Cryptology – EUROCRYPT 2018, ser.
     Lecture Notes in Computer Science, vol. 10821. Cham: Springer
     International Publishing, 2018, pp. 354–384. [Online]. Available:
     https://link.springer.com/10.1007/978-3-319-78375-8 12
[36] R. Jung, R. Krebbers, J.-H. Jourdan, A. Bizjak, L. Birkedal, and
     D. Dreyer, “Iris from the ground up: A modular foundation for higher-
     order concurrent separation logic,” Journal of Functional Programming,
     vol. 28, p. e20, 2018. [Online]. Available: https://www.cambridge.org/
     core/product/identifier/S0956796818000151/type/journal article
[37] D. Galmiche, D. Méry, and D. Pym, “The semantics of BI and resource
     tableaux,” Mathematical Structures in Computer Science, vol. 15, no. 6,
     pp. 1033–1088, Dec. 2005. [Online]. Available: https://www.cambridge.
     org/core/product/identifier/S0960129505004858/type/journal article
[38] J. T. Chang and D. Pollard, “Conditioning as disintegration,” Statistica
     Neerlandica, vol. 51, no. 3, pp. 287–317, Nov. 1997. [Online]. Available:
     https://onlinelibrary.wiley.com/doi/abs/10.1111/1467-9574.00056
[39] J. Pearl and A. Paz, “Graphoids: Graph-Based Logic for Reasoning
     about Relevance Relations or When would x tell you more about y if
     you already know z?” in Advances in Artificial Intelligence II, Seventh
     European Conference on Artificial Intelligence, ECAI 1986, Brighton,
     UK, July 20-25. North-Holland, 1986, pp. 357–363.
[40] S. Brookes, “A semantics for concurrent separation logic,”
     Theoretical Computer Science, vol. 375, no. 1-3, pp. 227–270,
     May 2007. [Online]. Available: https://linkinghub.elsevier.com/retrieve/
     pii/S0304397506009248
[41] I. B. E. Ouahma, Q. Meunier, K. Heydemann, and E. Encrenaz,
     “Symbolic approach for side-channel resistance analysis of masked
     assembly codes,” in PROOFS 2017. 6th International Workshop
     on Security Proofs for Embedded Systems, ser. EPiC Series in
     Computing, vol. 49. EasyChair, 2017, pp. 17–32. [Online]. Available:
     /publications/paper/9Bpn
[42] I. Ben El Ouahma, Q. L. Meunier, K. Heydemann, and E. Encrenaz,
     “Side-channel robustness analysis of masked assembly codes using a
     symbolic approach,” Journal of Cryptographic Engineering, vol. 9,
     no. 3, pp. 231–242, Sep. 2019. [Online]. Available: http://link.springer.
     com/10.1007/s13389-019-00205-7
                                      A BASIC FACTS ABOUT P ROBABILITY T HEORY
  Let f : A → B be a measurable function between measurable spaces (A, ΣA ) and (B, ΣB ), and let µ be a probability
measure on (A, ΣA ). The pushforward measure f∗ µ is the probability measure on (B, ΣB ) defined by
                                                  (f∗ µ)(E) = µ(f −1 (E))
for any measurable set E ∈ ΣB .
   Let P be a predicate on a set X. The Iverson bracket [P ] is defined by
                                                         (
                                                           1 P is true
                                                  [P ] =
                                                           0 otherwise.
Definition A.1 (π-system). Let P ⊆ 2X be a nonempty collection of subsets of X. Then, P is a π-system if for all A, B ∈ P ,
we have A ∩ B ∈ P .
Definition A.2 (λ-system). Let L ⊆ 2X be a nonempty collection of subsets of X. Then, L is a λ-system if:
  • X ∈ L.
  • If A, B ∈ L, then B \ A ∈ L.
                                                            S∞
  • If A1 ⊆ A2 ⊆ . . . is an increasing sequence in L, then  i=1 Ai ∈ L.

Theorem A.3 (Dynkin’s π-λ theorem). Let P be a π-system and L be a λ-system such that P ⊆ L. Then, the σ-algebra
generated by P is contained in L.
                                            P ⊆ L =⇒ σ(P) ⊆ L
  We list a few criteria for two functions/Markov kernels to be almost everywhere equal.
Lemma A.4. Let µ be a probability measure on (X, ΣX ) and f, g : (X, ΣX ) → [0, ∞] be measurable
                                                                                                  functions
                                                                                                             such
                                                                                                                that
f (x) ≤ g(x) for any x ∈ X. Then, f and g are µ-almost everywhere equal if and only if Ex∼µ f (x) = Ex∼µ g(x) .
Lemma A.5. Let f, g : (X, ΣX ) → [0, ∞] be measurable functions and µ be a probability measure on (X, ΣX ). Then, f and
g are µ-almost everywhere equal if and only if for any measurable set E ∈ ΣX , we have the following.
                                                                               
                                      Ex∼µ [x ∈ E] · f (x) = Ex∼µ [x ∈ E] · g(x)
Proof. The only-if part is obvious. For the if part, let E< = {x ∈ X : f (x) < g(x)}. If E< is non-negligible, then we have
                                                                                   
                                      Ex∼µ [x ∈ E< ] · f (x) < Ex∼µ [x ∈ E< ] · g(x) ,
which contradicts the assumption. Similarly, we can define E> = {x ∈ X : f (x) > g(x)} and obtain a contradiction if E> is
non-negligible. Therefore, {x ∈ X : f (x) ̸= g(x)} = E< ∪ E> is negligible.
Lemma A.6. Assume that (Y, ΣY ) is a countably generated σ-algebra. Let f, g : (X, ΣX ) → G(Y, ΣY ) be Markov kernels
and µ be a probability measure on (X, ΣX ). Then, f and g are µ-almost everywhere equal if and only if for any measurable
set E ∈ ΣX and F ∈ ΣY , we have
                                                                                 
                                  Ex∼µ [x ∈ E] · f (x)(F ) = Ex∼µ [x ∈ E] · g(x)(F ) .
If B is a basis of ΣY (i.e., σ(B) = ΣY ), then we can restrict F to be in B.
Proof. The only-if part is obvious. For the if part, let {Bm }m∈N be a countable basis of ΣY . Without loss of generality, we
assume that {Bm }m∈N is a π-system. By Lemma A.5, for any m, f (−)(Bm ) and g(−)(Bm ) are µ-almostTeverywhere equal,
that is, Sm := {x ∈ X | f (x)(Bm ) = g(x)(Bm )} satisfies
                                                        T    µ(Sm ) = 1. Now, we show that for any x ∈ m∈N Sm and any
F ∈ ΣY , we have f (x)(F ) = g(x)(F ). For any x ∈ m∈N Sm , it is easy to see that {F ∈ ΣY | f (x)(F ) = g(x)(F )} is a
λ-system containing {Bm }m∈N . By the Dynkin’s π-λ theorem, for any F ∈ ΣY , we have f (x)(F ) = g(x)(F ). The last claim
follows because the following set is a λ-system.
                                                                                          
                             {F ∈ ΣY | Ex∼µ [x ∈ E] · f (x)(F ) = Ex∼µ [x ∈ E] · g(x)(F ) }
Definition A.7 (disintegration). Let (A, ΣA , µ) and (B, ΣB , λ) be probability spaces, and f : A → B be a measurable
function. We say that {νy }y∈B is a disintegration of µ if y 7→ νy is a Markov kernel from B to A that satisfies the following
conditions [38]:
                                                                                                      
  • For λ-almost all y ∈ B, we have νy ({x | f (x) = y}) = 1. Equivalently, Ey∼λ νy ({x | f (x) = y}) = 1.
                                                                                                                     
  • The probability measure defined by E 7→ Ey∼λ νy (E) coincides with µ. Equivalently, Ey∼λ Ex∼νy g(x)                     =
                
     Ex∼µ g(x) for any measurable function g : A → [0, ∞].
  We often consider the case where λ = f∗ µ, in which case we say that {νy }y∈B is a µ-disintegration with respect to f .
  By the first property of disintegration, we have the following lemma.
Lemma A.8. Consider the setting in Definition A.7. For any measurable function g : A × B → [0, ∞], for λ-almost all y ∈ B,
we have                                                                      
                                       Ex∼νy g(x, f (x))     = Ex∼νy g(x, y) .
Proof. For νy -almost all x ∈ A, we have g(x, f (x)) = g(x, y).
  Disintegrations are unique up to almost everywhere equality.
Proposition A.9. Consider the setting in Definition A.7. If {νy }y∈B and {νy′ }y∈B are disintegrations, then νy and νy′ are
equal for λ-almost all y ∈ B.
Proof. By the properties of disintegration, for any measurable set E ∈ ΣB and F ∈ ΣA , we have the following equality.
                                                                      
                                                Ey∼λ [y ∈ E] · νy (F )
                                                                             
                                                 = Ex∼µ [f (x) ∈ E] · [x ∈ F ]
                                                 = Ey∼λ [y ∈ E] · νy′ (F )
                                                                         

By Lemma A.6, νy and νy′ are equal for λ-almost all y ∈ B.
                                                   B P ROOF OF T HEOREM V.1
   To prove Theorem V.1, we prepare several lemmas.
   The following lemma relates the conditional independence formula Cx←X (own Y ∗own Z) and the conditional independence
in terms of product probability measures.
Lemma B.1. Let ·; X : A, Y : B, Z : C ⊢ Cx←X (own Y ∗ own Z) be a Lilac formula. We have γ, D, (F, µ) ⊨
Cx←X (own Y ∗ own Z) if and only if for any (ΣΩ , µ′ ) ⊒ (F, µ) and µ′ -disintegration {νx }x with respect to X, for almost
all x, we have Y −1 (ΣB ) ∪ Z −1 (ΣC ) ⊆ F and Y∗ νx ⊗ Z∗ νx = (Y, Z)∗ νx . Here, ΣB and ΣC is the σ-algebra on JBK and
JCK, respectively; and ⊗ is the product probability measure.
Proof. By definition of γ, D, (F, µ) ⊨ Cx←X (own Y ∗ own Z), it suffices to show that for any (ΣΩ , µ′ ) ⊒ (F, µ), any
µ′ -disintegration {νx }x with respect to X, and any x, we have
         γ, D, (F, νx |F ) ⊨ own Y ∗ own Z         ⇐⇒        Y −1 (ΣB ) ∪ Z −1 (ΣC ) ⊆ F and Y∗ νx ⊗ Z∗ νx = (Y, Z)∗ νx
This is proved as follows.
                 γ, D, (F, νx |F ) ⊨ own Y ∗ own Z
                  ⇐⇒ ∃P1 , P2 such that P1 · P2 ⊑ (F, νx |F ); γ, D, P1 ⊨ own Y ; and γ, D, P2 ⊨ own Z
                  ⇐⇒ (Y −1 (ΣB ), νx |Y −1 (ΣB ) ) · (Z −1 (ΣC ), νx |Z −1 (ΣC ) ) ⊑ (F , νx |F )                           (8)
                  ⇐⇒ Y −1 (ΣB ) ∪ Z −1 (ΣC ) ⊆ F and Y∗ νx ⊗ Z∗ νx = (Y, Z)∗ νx                                             (9)
Here, (8) and (9) follow from the following facts:
                                                           −1
  • (8): Since ΣB and ΣC are countably generated, so are Y    (ΣB ) and Z −1 (ΣC ).
  • (9): By definition of product measurable spaces, we have Y∗ νx ⊗ Z∗ νx = (Y, Z)∗ νx if and only if for any measurable
    sets E ∈ ΣB and F ∈ ΣC , we have (Y∗ νx ⊗ Z∗ νx )(E × F ) = (Y, Z)∗ νx (E × F ). Note here that we have the following
    equations.
                                        (Y∗ νx ⊗ Z∗ νx )(E × F ) = (Y∗ νx )(E) · (Z∗ νx )(F )
                                                                    = νx (Y −1 (E)) · νx (Z −1 (F ))
                                              (Y, Z)∗ νx (E × F ) = νx (Y −1 (E) ∩ Z −1 (F ))
   In the semantics of conditioning modalities in Lilac, one needs to take a probability distribution over the common sample
space Ω. This requires assigning an arbitrary probability distribution to the region outside the domain of interest, but the
following lemma ensures that this choice does not essentially affect the semantics.
Lemma B.2. Let µ, µ′ be probability measures on ΣΩ . Let D = (DX , DY ) and D′ = (DX           ′
                                                                                                 , DY′ ) be random variables
     ′                                                        ′ ′
D, D ∈ RVJ∆K where ∆ = X : A, Y : B. If D∗ µ = D∗ µ , then for any µ-disintegration {νx }x∈A with respect to DX
and any µ′ -disintegration {νx′ }x∈A with respect to DX
                                                      ′
                                                        , for D∗ µ-almost all x and for any E ∈ ΣB , we have νx (DY−1 (E)) =
 ′   ′−1
νx (DY (E)).
Proof. By Lemma A.6, it suffices to show that for any measurable set E ∈ ΣB and F ∈ ΣA , we have
                                                                                          ′ −1
                      Ex∼(DX )∗ µ [x ∈ F ] · νx (DY−1 (E)) = Ex∼(DX                   ′
                                                                                               
                                                                   ′ ) µ′ [x ∈ F ] · ν (D
                                                                      ∗               x     Y (E)) .

By D∗ µ = D∗′ µ′ , it suffices to prove
                              Ex∼(DX )∗ µ [x ∈ F ] · νx (DY−1 (E)) = P(x,y)∼D∗ µ [x ∈ F ∧ y ∈ E].
                                                                 

This is proved as follows.
                                     P(x,y)∼D∗ µ [x ∈ F ∧ y ∈ E]
                                      = Pω∼µ [DX (ω) ∈ F ∧ DY (ω) ∈ E]
                                                                                    
                                      = Ex∼(DX )∗ µ Eω∼νx [DX (ω) ∈ F ] · [DY (ω) ∈ E]
                                      = Ex∼(DX )∗ µ [x ∈ F ] · νx (DY−1 (E))
                                                                           

  By Lemma B.2, we have the following lemma.
Lemma B.3. Let ∆ = X : A, Y : B, Z : C and D = (DX , DY , DZ ), D′ = (DX         ′
                                                                                   , DY′ , DZ
                                                                                            ′
                                                                                              ) be random variables such that
(DX , DY , DZ ), (DX , DY , DZ ) ∈ RVJ∆K. Let µ, µ be probability measures on ΣΩ such that D∗ µ = D∗′ µ′ . Let F , F ′ ⊆ ΣΩ
                   ′    ′    ′                    ′

be σ-algebras such that (DY , DZ ) is F-measurable and (DY′ , DZ
                                                               ′
                                                                 ) is F ′ -measurable. Then, we have
                                      γ, D, (F, µ|F ) ⊨ C (own Y ∗ own Z)
                                                        x←X
                                          ⇐⇒     γ, D′ , (F ′ , µ′ |F ′ ) ⊨ C (own Y ∗ own Z)
                                                                     x←X

Proof. By symmetry, it suffices to prove that if γ, D, P ⊨ Cx←X (own Y ∗own Z), then γ, D′ , P ′ ⊨ Cx←X (own Y ∗own Z).
By unfolding the definition, we have γ, D′ , P ′ ⊨ Cx←X (own Y ∗ own Z) if and only if for any µ′ -disintegration {νx′ }x with
            ′                                                                                   −1          −1
respect to DX , we have for D∗′ µ′ -almost all x, and for any E ∈ ΣB and F ∈ ΣC , we have D′ Y (E) ∩ D′ Z (F ) ∈ F ′ and
  ′  ′ −1        ′ −1          ′    ′ −1        ′   ′ −1
νx (D Y (E) ∩ D Z (F )) = νx (D Y (E)) · νx (D Z (F )). Fix a µ-disintegration {νx }x with respect to DX . By γ, D, P ⊨
Cx←X (own Y ∗ own Z) and Lemma B.2, we have the following equation for almost all x.
                                           −1          −1
                                    νx′ (D′ Y (E) ∩ D′ Z (F )) = νx′ ((DY′ , DZ
                                                                              ′ −1
                                                                                ) (E × F ))
                                                               = νx ((DY , DZ )−1 (E × F ))
                                                               = νx (DY−1 (E) ∩ DZ
                                                                                 −1
                                                                                    (F ))
                                                               = νx (DY−1 (E)) · νx (DZ
                                                                                      −1
                                                                                         (F ))
                                                               = νx′ (DY′−1 (E)) · νx′ (DZ
                                                                                         ′−1
                                                                                             (F ))
Therefore, we have γ, D′ , P ′ ⊨ Cx←X (own Y ∗ own Z).
Lemma B.4. For any APPL program ∆ ⊢ M : GA, we have
                                                {own ∆} M {X. own ∆ ∧ own X}
where own ∆ is shorthand for own(X1 , . . . , Xn ) when ∆ = X1 : A1 , . . . , Xn : An .
Proof. By induction on the structure of M .
  • ret E: Since ∅; ∆ ⊢ E : A, we have own ∆ ⊢ own E by FV-OWN .

                                 H-R ET
                                          {own ∆ ∧ own E} ret E {X. own ∆ ∧ own X}
                             H-C ONSEQ
                                              {own ∆} ret E {X. own ∆ ∧ own X}
  •   X ← M; N:
                                              {own ∆ ∧ own X} N {Y. own ∆ ∧ own X ∧ own Y }
                                                 H-C ONSEQ
               {own ∆} M {X. own ∆ ∧ own X}        {own ∆ ∧ own X} N {Y. own ∆ ∧ own Y }
        H-L ET
                                   {own ∆} X ← M ; N {Y. own ∆ ∧ own Y }
  •   unif K:
                                           H-U NIF
                                             {⊤} unif K {X.X ∼ unif K}
                                H-F RAME
                                        {own ∆} unif K {X. own ∆ ∗ X ∼ unif K}
                              H-C ONSEQ
                                          {own ∆} unif K {X. own ∆ ∧ own X}
  •   for (X ← E; i ← ns . . . ne ) {M }: Let I(i, X) := own ∆ ∧ own X.
                                {own ∆ ∧ own X} M {X ′ . own ∆ ∧ own X ∧ own X ′ }
                      H-C ONSEQ
                                   {own ∆ ∧ own X} M {X ′ . own ∆ ∧ own X ′ }
                 H-F OR
                        {own ∆ ∧ own E} for (X ← E; i ← ns . . . ne ) {M } {X. own ∆ ∧ own X}
             H-C ONSEQ
                            {own ∆} for (X ← E; i ← ns . . . ne ) {M } {X. own ∆ ∧ own X}
      Here, we use FV-OWN to show own ∆ ⊢ own E.
  To prove the ( =⇒ ) direction of Theorem V.1, we prepare several lemmas.
  In classical probability theory, X and Y are independent if and only if Pr[Y | X] = Pr[Y ]. The following lemma states a
similar characterization for the Lilac formula own X ∗ own Y in terms of disintegrations.
Lemma B.5. Let X : A, Y : B ⊢ own X ∗ own Y be a Lilac formula. We have γ, D, (F, µ) ⊨ own X ∗ own Y if and only
if X and Y are F-measurable, and for any (ΣΩ , µ′ ) ⊒ (F, µ) and µ′ -disintegration {νx }x∈JAK with respect to X, we have
Y∗ νx = Y∗ µ for almost all x ∈ JAK.
Proof of Lemma B.5. The only if direction follows from the proof of C-I NDEP in [29, Lemma B.27]. To prove the if direction,
it suffices to show
                                µ(X −1 (E) ∩ Y −1 (F )) = µ(X −1 (E)) · µ(Y −1 (F ))
for any measurable sets E ∈ ΣJAK and F ∈ ΣJBK . This is proved as follows.
                                      µ(X −1 (E) ∩ Y −1 (F ))
                                                                              
                                      = Ex∼X∗ µ Eω∼νx [X(ω) ∈ E] · [Y (ω) ∈ F ]
                                                                           
                                      = Ex∼X∗ µ [x ∈ E] · Eω∼νx [Y (ω) ∈ F ]
                                                                   
                                      = Ex∼X∗ µ [x ∈ E] · Y∗ νx (F )
                                                                  
                                      = Ex∼X∗ µ [x ∈ E] · Y∗ µ(F )
                                                                  
                                      = Y∗ µ(F ) · Ex∼X∗ µ [x ∈ E]
                                       = µ(Y −1 (F )) · µ(X −1 (E))
  Let M be a program with input variables X and output variables Y . The following lemma states that any disintegration that
represents the conditional distribution Pr[Y | X] is almost everywhere equal to the distribution of the output of M given the
input X.
Lemma B.6. Let ∆ ⊢ M : GA be an APPL program, D ∈ RVJ∆K be a random variable, and (ΣΩ , µ) ∈ Mdisint . If a random
variable Y ∈ RVJAK and (ΣΩ , µM ) ∈ Mdisint satisfy the following equation:
                                                    
                                   ω ← µ;                                          !
                                                                 ω ← µM ;
                                 y ← JM K(D(ω)); =
                                                    
                                                                 ret (D(ω), Y (ω))
                                   ret (D(ω), y)
then, for any µM -disintegration {νx }x∈J∆K with respect to D and for almost all x ∈ J∆K, we have
                                                   Y∗ νx   =    JM K(x).
Proof of Lemma   B.6. We apply Lemma  A.6 to Y∗ νx and JM K(x). Note      first that we have D∗ µM = D∗ µ. We show
Ex∼D∗ µM [x ∈ E] · νx (Y −1 (F )) = Ex∼D∗ µ [x ∈ E] · JM K(x)(F ) for any measurable sets E ∈ ΣA and F ∈ ΣB .
                                                                   

This is proved as follows:
                                   Ex∼D∗ µM [x ∈ E] · νx (Y −1 (F ))
                                                                   
                                                                              
                                   = Ex∼D∗ µM [x ∈ E] · Eω∼νx [Y (ω) ∈ F ]
                                                                              
                                   = Ex∼D∗ µM Eω∼νx [x ∈ E] · [Y (ω) ∈ F ]
                                                                                  
                                   = Ex∼D∗ µM Eω∼νx [D(ω) ∈ E] · [Y (ω) ∈ F ]
                                                                      
                                   = Eω∼µM [D(ω) ∈ E] · [Y (ω) ∈ F ]
                                                                        
                                   = E(x,y)∼(D,Y )∗ µM [x ∈ E] · [y ∈ F ]
                                                                           
                                   = Ex∼D∗ µ Ey∼JM K(x) [x ∈ E] · [y ∈ F ]
                                                                           
                                   = Ex∼D∗ µ [x ∈ E] · Ey∼JM K(x) [y ∈ F ]
                                                                    
                                   = Ex∼D∗ µ [x ∈ E] · JM K(x)(F )
   Given a pair of random variables (X, Y ), we can consider two types of disintegrations: one is joint disintegrations with
respect to the pair (X, Y ) and the other is iterated disintegrations with respect to X and then Y . We consider the relationship
between these two types of disintegrations.
Lemma B.7. Let (Ω, ΣΩ , µ) be a probability space, and X : Ω → A and Y : Ω → B be random variables. Suppose that
{νx }x∈A is a µ-disintegration with respect to X. For any g : A × B → R, we have the following equality.
                                                                                     
                                 Ex∼X∗ µ Ey∼Y∗ νx g(x, y)      = E(x,y)∼(X,Y )∗ µ g(x, y)

Proof.
                                                
                         Ex∼X∗ µ Ey∼Y∗ νx g(x, y)
                                                    
                         = Ex∼X∗ µ Eω∼νx g(x, Y (ω))
                                                       
                         = Ex∼X∗ µ Eω∼νx g(X(ω), Y (ω))                                   by Lemma A.8
                                                 
                         = Eω∼µ g(X(ω), Y (ω))                                         by Definition A.7
                                                   
                         = E(x,y)∼(X,Y )∗ µ g(x, y)



Lemma B.8. Let (Ω, ΣΩ , µ) be a probability space, and X : Ω → A and Y : Ω → B be random variables. Suppose that
{νx }x∈A is a µ-disintegration with respect to X, and {(νx )y }y∈B is a νx -disintegration with respect to Y . If (x, y) 7→ (νx )y
is a Markov kernel, i.e., (x, y) 7→ (νx )y (E) is measurable for any measurable set E ∈ ΣΩ , then {(νx )y }(x,y)∈A×B is a
µ-disintegration with respect to (X, Y ).
Proof.    •   For (X, Y )∗ µ-almost all (x, y), it follows that
                                                                                  
                                                 Eω∼(νx )y [(X(ω), Y (ω)) = (x, y)] = 1

      holds because
                                                                       
                      E(x,y)∼(X,Y )∗ µ Eω∼(νx )y [(X(ω), Y (ω)) = (x, y)]
                                                                            
                      = Ex∼X∗ µ Ey∼Y∗ νx Eω∼(νx )y [(X(ω), Y (ω)) = (x, y)]                       by Lemma B.7
                                                                        
                      = Ex∼X∗ µ Ey∼Y∗ νx Eω∼(νx )y [(X(ω), y) = (x, y)]                           by Lemma A.8
                                                              
                      = Ex∼X∗ µ Ey∼Y∗ νx Eω∼(νx )y [X(ω) = x]
                                                    
                      = Ex∼X∗ µ Eω∼νx [X(ω) = x]
                      =1

  •   We show
                                                                                    
                                          Eω∼µ f (ω) = E(x,y)∼(X,Y )∗ µ Eω∼(νx )y f (ω)

      for any measurable function f : Ω → [0, ∞].
                                          
                                Eω∼µ f (ω)
                                                       
                                 = Ex∼X∗ µ Eω∼νx f (ω)
                                                                    
                                 = Ex∼X∗ µ Ey∼Y∗ νx Eω∼(νx )y f (ω)
                                                                  
                                 = E(x,y)∼(X,Y )∗ µ Eω∼(νx )y f (ω)

  The following lemma states that a joint disintegration can be seen as an iterated disintegration.
Lemma B.9. Let (Ω, ΣΩ , µ) be a probability space with countably generated σ-algebra, and X : Ω → A and Y : Ω → B be
random variables. Suppose that {νx,y }(x,y)∈A×B is a µ-disintegration with respect to (X, Y ), and {νx }x∈A is a µ-disintegration
with respect to X. Then {νx,y }y∈B is a νx -disintegration with respect to Y for X∗ µ-almost all x.
                                                                  
Proof of Lemma B.9.     • We show Ey∼Y∗ νx Eω∼νx,y [Y (ω) = y]         = 1 for almost all x. We use Lemma B.7.
                                                                                  
                                            Ex∼X∗ µ Ey∼Y∗ νx Eω∼νx,y [Y (ω) = y]
                                                                                    
                                             = E(x,y)∼(X,Y )∗ µ Eω∼νx,y [Y (ω) = y]
                                              =1
                                                           
  •   Using Lemma A.6, we show that F 7→ Ey∼Y∗ νx νx,y (F ) and νx are equal for almost all x.
                                                                        
                                    Ex∼X∗ µ [x ∈ E] · Ey∼Y∗ νx νx,y (F )
                                                                        
                                    Ex∼X∗ µ Ey∼Y∗ νx [x ∈ E] · νx,y (F )
                                                                          
                                     = E(x,y)∼(X,Y )∗ µ [x ∈ E] · νx,y (F )
                                                                                   
                                     = E(x,y)∼(X,Y )∗ µ Eω∼νx,y [X(ω) ∈ E] · [ω ∈ F ]
                                                                    
                                     = Eω∼µ [X(ω) ∈ E] · [ω ∈ F ]
                                                                           
                                     = Ex∼X∗ µ Eω∼νx [X(ω) ∈ E] · [ω ∈ F ]
                                                                
                                     = Ex∼X∗ µ [x ∈ E] · νx (F )


Proof of Theorem V.1 ( =⇒ ). To show that the simulator (5) satisfies (4), it suffices to show that
                                         X1 : A1 , X2 : A2 ⊢ (Y1 , Y2 ) ← M ; ret Y1 : GB1
does not actually depend on X2 . We prove by contradiction. Let M ′ := (Y1 , Y2 ) ← M ; ret Y1 . Suppose that there exist
a1 ∈ JA1 K and a2 , a′2 ∈ JA2 K such that JM ′ K(a1 , a2 ) ̸= JM ′ K(a1 , a′2 ). By assumption and the rules in Fig. 4, we have the
following Hoare triple:
                                    {own X1 ∧ own X2 } M ′ {Y1 . C (own X2 ∗ own Y1 )}
                                                                      x←X1

Suppose that the input distribution is chosen so that (X1 , X2 ) is uniformly distributed over {(a1 , a2 ), (a1 , a′2 )}. By the above
Hoare triple, the output Y1 satisfies Cx←X1 (own X2 ∗ own Y1 ). Formally, let µ be a probability measure on ΣΩ and D ∈
RVJX1 : A1 , X2 : A2 K be such that D∗ µ is the uniform distribution over {(a1 , a2 ), (a1 , a′2 )}. Then, there exists Y1 ∈ RVJB1 K,
P ′ , and µ′ with P ′ ⊑ (ΣΩ , µ′ ) such that
                                                            
                                      ω ← µ;                                                      !
                                                                          ω ← µ′ ;
                                    (y1 , y2 ) ← JM K(D(ω)); =
                                                            
                                                                          ret (D(ω), Y1 (ω))
                                      ret (D(ω), y1 )
and γ, (D, Y1 ), P ′ ⊨ Cx←X1 (own X2 ∗own Y1 ). Let {νx1 }x1 ∈JA1 K be a µ′ -disintegration with respect to X1 . Since (X1 )∗ µ′ =
(X1 )∗ µ = δa1 , we have µ′ = νa1 and thus γ, (D, Y1 ), P ′ ⊨ own X2 ∗ own Y1 by the semantics of conditioning modalities.
                                     µ′ (E) = Ex∼(X1 )∗ µ′ Eω∼νx [ω ∈ E] = νa1 (E)
                                                                           

Let {νx1 ,x2 }x1 ∈JA1 K,x2 ∈JA2 K be a µ′ -disintegration with respect to (X1 , X2 ). By Lemma B.9, {νx1 ,x2 }x2 ∈JA2 K is a νx1 -
disintegration with respect to X2 for almost all x1 , i.e., {νa1 ,x2 }x2 ∈JA2 K is a µ′ -disintegration with respect to X2 . By applying
Lemma B.5 to γ, (D, Y1 ), P ′ ⊨ own X2 ∗ own Y1 , we have (Y1 )∗ νa1 ,a2 = (Y1 )∗ µ′ = (Y1 )∗ νa1 ,a′2 . By Lemma B.6, we
have (Y1 )∗ νx1 ,x2 = JM K(x1 , x2 ) for almost all (x1 , x2 ), i.e., for any (x1 , x2 ) ∈ {(a1 , a2 ), (a1 , a′2 )}. Therefore, we have
JM ′ K(a1 , a2 ) = JM ′ K(a1 , a′2 ), which is a contradiction.
  For the ( ⇐= ) direction of Theorem V.1, the key lemma is the following.
Lemma B.10. Let ∆ = X1 : A1 , . . . , Xn : An be a context, ∆ ⊢ M : GB be an APPL program, and Z ∈ RVJCK be a fresh
random variable. Then, we have
                                       {own ∆ ∧ own Z} M {Y. C (own Y ∗ own Z)}
                                                                     x̃←∆

where x̃ = (x1 , . . . , xn ) is the tuple of deterministic variables, and we write ∆ to denote both the context and the tuple of
random variables (X1 , . . . , Xn ).
Proof of Lemma B.10. Let µ be a probability measure on (Ω, ΣΩ ), and D ∈ RVJ∆K be a random variable. Suppose
γ, (D, Z), (F, µ|F ) ⊨ own ∆ ∧ own Z. By Lemma B.4, for any Pframe such that Pframe · (F, µ|F ) ⊑ (ΣΩ , µ) and any
Dext , there exists µM , Y , and FM such that Pframe · (FM , µM |FM ) ⊑ (ΣΩ , µM ),
                                                      
                         ω ← µ;                                                                    !
                                                                  ω ← µM ;
                      y ← JM K(D(ω));                  =                                           ,
                                                      
                                                                  ret (Dext (ω), D(ω), Z(ω), Y (ω))
                         ret (Dext (ω), D(ω), Z(ω), y)
and γ, (D, Z, Y ), (FM , µ|FM ) ⊨ own ∆ ∧ own Z ∧ own Y . Now, we show γ, (D, Z, Y ), (FM , µ|FM ) ⊨ Cx̃←∆ (own Y ∗
own Z). By Lemma B.1, it suffices to show that for any µM -disintegration {νx }x∈J∆K with respect to D, for almost all x,
we have Y∗ νx ⊗ Z∗ νx = (Y, Z)∗ νx . Strictly speaking, we need to consider (ΣΩ , µ′M ) ⊒ (FM , µ|FM ) and µ′M -disintegration
{νx }x with respect to D, but by Lemma B.3, it suffices to consider µM -disintegration. By Lemma A.6, it suffices to show the
following equation for any E, F, G.

                                      Ex∼D∗ µM [x ∈ E] · νx (Y −1 (F )) · νx (Z −1 (G))
                                                                                       

                                       = Ex∼D∗ µM [x ∈ E] · νx (Y −1 (F ) ∩ Z −1 (G))
                                                                                      

This is proved as follows:

                             Ex∼D∗ µM [x ∈ E] · νx (Y −1 (F )) · νx (Z −1 (G))
                                                                             

                             = Ex∼D∗ µM [x ∈ E] · νx (Y −1 (F )) · Eω∼νx [Z(ω) ∈ G]
                                                                                        

                             = Ex∼D∗ µM Eω∼νx [x ∈ E] · νx (Y −1 (F )) · [Z(ω) ∈ G]
                                                                                        

                             = Ex∼D∗ µM Eω∼νx [D(ω) ∈ E] · νD(ω) (Y −1 (F )) · [Z(ω) ∈ G]
                                                                                              

                             = Eω∼µM [D(ω) ∈ E] · νD(ω) (Y −1 (F )) · [Z(ω) ∈ G]
                                                                                      

                             = E(x,z)∼(D,Z)∗ µM [x ∈ E] · νx (Y −1 (F )) · [z ∈ G]
                                                                                    

                             = E(x,z)∼(D,Z)∗ µ [x ∈ E] · νx (Y −1 (F )) · [z ∈ G]
                                                                                  
                                                                                
                             = E(x,z)∼(D,Z)∗ µ [x ∈ E] · JM K(x)(F ) · [z ∈ G]
                                                                                        
                             = E(x,z)∼(D,Z)∗ µ [x ∈ E] · Ey∼JM K(x) [y ∈ F ] · [z ∈ G]
                                                                                       
                             = E(x,z)∼(D,Z)∗ µ Ey∼JM K(x) [x ∈ E] · [y ∈ F ] · [z ∈ G]
                                                                                  
                             = E(x,z,y)∼(D,Z,Y )∗ µM [x ∈ E] · [y ∈ F ] · [z ∈ G]
                                                                                 
                             = Eω∼µM [D(ω) ∈ E] · [Y (ω) ∈ F ] · [Z(ω) ∈ G]
                             = Ex∼D∗ µM Eω∼νx [D(ω) ∈ E] · [ω ∈ Y −1 (F ) ∩ Z −1 (G)]
                                                                                           

                             = Ex∼D∗ µM Eω∼νx [x ∈ E] · [ω ∈ Y −1 (F ) ∩ Z −1 (G)]
                                                                                       

                             = Ex∼D∗ µM [x ∈ E] · Eω∼νx [ω ∈ Y −1 (F ) ∩ Z −1 (G)]
                                                                                       

                             = Ex∼D∗ µM [x ∈ E] · νx (Y −1 (F ) ∩ Z −1 (G))
                                                                             

   In Lemma B.10, Z need not be independent of the input variables X1 , . . . , Xn , which makes the lemma stronger than the
frame rule H-F RAME.
   By Lemma B.10, we have the following Hoare triple for the simulator (5):

                              {own X1 ∧ own X2 } Sim(M ) {Y1 . C (own X2 ∗ own Y1 )}
                                                                     x←X1

By (4), this Hoare triple is also satisfied by (Y1 , Y2 ) ← M ; ret Y1 . Thus, we have the desired Hoare triple (3).
   Precisely speaking, we cannot directly conclude (3) because we have wp(M, X.wp(N, Y.ϕ)) ⊢ wp(X ← M ; N, Y.ϕ) but
in general no guarantee for the converse.

Proof of Theorem V.1 ( ⇐= ). Suppose that we have γ, D, (Fpre , µpre ) ⊨ own X1 ∧own X2 where γ ∈ J·K and D ∈ RVJX1 :
A1 , X2 : A2 K is a random variable. It is straightforward to show that

                                    {own(X1 , X2 )} M {(Y1 , Y2 ). own(X1 , X2 , Y1 , Y2 )}

holds (Lemma B.4). By unfolding the definition of the Hoare triple, for any Pframe , Dext ∈ RVJ∆ext K, and µ such that
Pframe · (Fpre , µpre ) ⊑ (ΣΩ , µ), there exist (DY1 , DY2 ) ∈ RVJY1 : B1 , Y2 : B2 K, µM , and PM such that Pframe · PM ⊑
(ΣΩ , µM ),
                                                                    
                                           ω ← µ;
                                         (y1 , y2 ) ← JM K(D(ω));
                                                                    
                                                                     
                                        ret (Dext (ω), D(ω), y1 , y2 )
                                                                                      !
                                             ω ← µM ;
                                      =                                                   ,
                                             ret (Dext (ω), D(ω), DY1 (ω), DY2 (ω))

and γ, (D, DY1 , DY2 ), PM ⊨ own(X1 , X2 , Y1 , Y2 ) hold. Below, we show that the same (DY1 , DY2 ), µM , and PM witness the
desired Hoare triple (3). For this purpose, it suffices to show γ, (D, DY1 , DY2 ), PM ⊨ Cx←X1 (own X2 ∗ own Y1 ). By the
             D IST-OWN                   T RANSFER -OWN                                            T RANSFER -D IST
                                                           as                                                     as
             E ∼ µ ⊢ own E               own E1 ∧ (E1 = E2 ) ⊢ own E2                              E1 ∼ µ ∧ (E1 = E2 ) ⊢ E2 ∼ µ

                                                                                                                         C-E NTAIL
    E Q -C ONGRUENCE                                                   E Q -C ONJ
                                 as                  as                             as                      as               ϕ⊢ψ
    own(F [E1 ], F [E2 ]) ∧ (E1 = E2 ) ⊢ F [E1 ] = F [E2 ]             ϕ ∧ (E1 = E2 ) ⊣⊢ ϕ ∗ (E1 = E2 )
                                                                                                                           C ϕ⊢ C ψ
                                                                                                                          x←E         x←E


                            C-S UBST                                                               U NIF -B IJECTION
C-I NDEP                                                    C-OWN
                                                as                                                 Γ; X : K ⊢ E : K    E is bijective in X
own E ∗ ϕ ⊢ C ϕ            own X ⊢ C (X = x)                own E ⊢ C own E
               x←E                     x←X                               x←E                              X ∼ unif K ⊢ E ∼ unif K

N ECESSITATION                                                                                              FV-OWN
                     C-A ND -D ISTRIBUTIVE                      C-O R -S EMI D ISTRIBUTIVE
  ⊢ϕ                                                                                                        Γ; X1 : A1 , . . . , Xn : An ⊢ E : B
                      C (ϕ ∧ ψ) ⊣⊢ C ϕ ∧ C ψ                     C ϕ ∨ C ψ ⊢ C (ϕ ∨ ψ)
⊢ C ϕ                x←X               x←X      x←X          x←X         x←X             x←X                  own(X1 , . . . , Xn ) ⊢ own E
  x←X

                                                                                                                                □-M ONO
   C-U NIF
                                                                                                                                  ϕ⊢ψ
   own X ∧ C (Y ∼ unif K) ⊢ own X ∗ (Y ∼ unif K)                          X ∼ µ ∧ (own X ∗ ϕ) ⊢ (X ∼ µ) ∗ ϕ
              x←X                                                                                                                □ϕ ⊢ □ψ

□-I DEM          □-E LIM       □-T RUE       □-A ND                         □-C ONJ                                                   n
                                                                                                                                      ^
□ϕ ⊢ □□ϕ         □ϕ ⊢ ϕ        ⊢ □⊤          □ ϕ ∧ □ ψ ⊢ □(ϕ ∧ ψ)           ϕ ∧ □ψ ⊢ ϕ ∗ □ψ                own(X1 , . . . , Xn ) ⊣⊢         own Xi
                                                                                                                                      i=1


Fig. 12: List of inference rules for Lilac formulas [29]. We omit obvious structural rules like commutativity and associativity
of the separating conjunction ∗. Note that Lilac is an affine separation logic, and thus ϕ ∗ ψ ⊢ ϕ holds.


substitution property [29, Lemma B.10], this is equivalent to γ, (D, DY1 ), PM ⊨ Cx←X1 (own X2 ∗ own Y1 ). By Lemma B.10,
we have
                              {own X1 ∧ own X2 } Sim(M ) {Y1 . C (own X2 ∗ own Y1 )}
                                                                            x←X1

and thus, there exist DY′ 1 ∈ RVJY1 : B1 K, µSim(M ) , and PSim(M ) such that Pframe · PSim(M ) ⊑ (ΣΩ , µSim(M ) ),
                                                                       
                                                ω ← µ;
                                               y1 ← JSim(M )K(DX1 (ω));
                                                                       

                                                 ret (Dext (ω), D(ω), y1 )
                                                                                           !
                                                      ω ← µSim(M ) ;
                                               =                                               ,
                                                      ret (Dext (ω), D(ω), DY′ 1 (ω))

and γ, (D, DY1 ), PSim(M ) ⊨ Cx←X1 (own X2 ∗ own Y1 ). Here, µM and µSim(M ) are not necessarily the same, but by (4),
we have the following equation:
                                                        !                        !
                                   ω ← µSim(M ) ;             ω ← µM ;
                                                          =                                                      (10)
                                   ret (D(ω), DY′ 1 (ω))      ret (D(ω), DY1 (ω))

   The remaining task is to show that if γ, (D, DY′ 1 ), PSim(M ) ⊨ Cx←X1 (own X2 ∗ own Y1 ), then γ, (D, DY1 ), PM ⊨
Cx←X1 (own X2 ∗ own Y1 ). This follows because (D, DY′ 1 )∗ µSim(M ) and (D, DY1 )∗ µM give the same distribution by (10)
(see Lemma B.3 for the formal argument).

                            C P ROOFS FOR S ECTION VI (A DDITIONAL P ROOF RULES FOR L ILAC )
A. Proof of Proposition VI.1
Proof of Proposition VI.1 (G EN -W EAK -U NION). Suppose γ, D, P ⊨ ϕ ∗ own(X, Y ). By definition, there exists P1 · P2 ⊑ P
such that γ, D, P1 ⊨ ϕ and γ, D, P2 ⊨ own(X, Y ). To show γ, D, P ⊨ Cx:A←X (ϕ ∗ own Y ), suppose P ⊑ (ΣΩ , µ) and let
{νx }x∈X be a µ-disintegration with respect to X. By the proof of C-I NDEP, we know that νx |P1 = P1 for almost all x. We
also have γ, D, νx |P2 ⊨ own(X, Y ) because own(X, Y ) does not depend on the probability distribution. Thus, it suffices to
show that νx |P1 · νx |P2 ⊑ νx holds for almost all x. Since we already know that P1 · P2 ⊑ P, we show that for almost all x,
for any F ∈ FP1 and G ∈ FP2 , νx (F ∩ G) = νx (F )νx (G). By Lemma A.6, this is equivalent to
                                                                              
                                          Ex∼(X(γ)◦D)∗ µ [x ∈ E] · νx (F ∩ G)
                                                                                     
                                           = Ex∼(X(γ)◦D)∗ µ [x ∈ E] · νx (F ) · νx (G)
which is proved as follows.
                                                            
                    Ex∼(X(γ)◦D)∗ µ [x ∈ E] · νx (F ) · νx (G)
                                                               
                    = Ex∼(X(γ)◦D)∗ µ [x ∈ E] · µ(F ) · νx (G)
                                                                  
                    = µ(F )Ex∼(X(γ)◦D)∗ µ [x ∈ E] · Eω∼νx [ω ∈ G]
                    = µ(F )Ex∼(X(γ)◦D)∗ µ Eω∼νx [ω ∈ G ∩ (X(γ) ◦ D)−1 (E)]
                                                                        

                    = µ(F )Eω∼µ [ω ∈ G ∩ (X(γ) ◦ D)−1 (E)]
                                                                 

                     = µ(F )µ(G ∩ (X(γ) ◦ D)−1 (E))
                     = µ(F ∩ G ∩ (X(γ) ◦ D)−1 (E))       by γ, D, P2 ⊨ own X and P1 · P2 ⊑ (ΣΩ , µ)
                     = Ex∼(X(γ)◦D)∗ µ Eω∼νx [ω ∈ F ∩ G ∩ (X(γ) ◦ D)−1 (E)]
                                                                          
                                                                 
                     = Ex∼(X(γ)◦D)∗ µ Eω∼νx [ω ∈ F ∩ G] · [x ∈ E]
                                                          
                     = Ex∼(X(γ)◦D)∗ µ [x ∈ E] · νx (F ∩ G)
Proof of Proposition VI.1 (C ONTRACTION). Suppose γ, D, P ⊨ (own W ∗ own X) ∧ Cx←X (own W ∗ own Y ). Let FX
and FW be the sub-σ-algebras generated by X and W , respectively. Let µ be a probability measure on (Ω, ΣΩ ) such that
P ⊑ (ΣΩ , µ). By γ, D, P ⊨ own W ∗ own X, we have (µ|FX , FX ) · (µ|FW , FW ) ⊑ (µ, ΣΩ ). By γ, D, P ⊨ Cx←X (own W ∗
own Y ), for any µ-disintegration {νx }x∈X with respect to X, there exists FY ⊆ F such that Y is FY -measurable and
(νx |FW , FW ) · (νx |FY , FY ) ⊑ (νx , ΣΩ ) for almost all x. By the proof of C-I NDEP, we know that νx |FW = µ|FW for almost
all x. Now, we show that for any E1 ∈ FX , E2 ∈ FY , and E3 ∈ FW , we have
                                          µ(E1 ∩ E2 ∩ E3 ) = µ(E1 ∩ E2 ) · µ(E3 ).
Since FX = {X −1 (E) | E ∈ ΣX }, there exists EX ∈ ΣX such that E1 = X −1 (EX ).
                                   µ(E1 ∩ E2 ∩ E3 )
                                   = Ex∼X∗ µ Eω∼νx [ω ∈ X −1 (EX )] · [ω ∈ E2 ∩ E3 ]
                                                                                  
                                                                            
                                   = Ex∼X∗ µ [x ∈ EX ] · Eω∼νx [ω ∈ E2 ∩ E3 ]
                                                                           
                                   = Ex∼X∗ µ [x ∈ EX ] · νx (E2 ) · νx (E3 )
                                                                          
                                   = Ex∼X∗ µ [x ∈ EX ] · νx (E2 ) · µ(E3 )
                                                                
                                   = Ex∼X∗ µ [x ∈ EX ] · νx (E2 ) · µ(E3 )
                                   = Ex∼X∗ µ Eω∼νx [ω ∈ X −1 (EX )] · [ω ∈ E2 ] · µ(E3 )
                                                                             

                                   = µ(E1 ∩ E2 ) · µ(E3 )
Consider the following set.
                               {E ∈ σ(FX ∪ FY ) | ∀E3 ∈ FW , µ(E ∩ E3 ) = µ(E) · µ(E3 )}
It is easy to see that this is a λ-system containing the π-system {E1 ∩E2 | E1 ∈ FX , E2 ∈ FY }. By Dynkin’s π-λ theorem, the
λ-system contains σ({E1 ∩ E2 | E1 ∈ FX , E2 ∈ FY }) = σ(FX ∪ FY ). Hence, we have (µ|FX , FX ) · (µ|σ(FX ∪FY ) , σ(FX ∪
FY )) ⊑ (µ, ΣΩ ). Note that σ(FX ∪ FY ) is countably generated because both FX and FY are countably generated.

B. Generalized U NIF -B IJECTION
Lemma C.1. U NIF -B IJECTION can be generalized to the following.
                                       Γ; ∆, Y : K ⊢ E : K  E is bijective in Y
                                    own ∆ ∗ F ∼ unif K ⊢ own ∆ ∗ E[F/Y ] ∼ unif K
Proof sketch. Suppose that we have own ∆ ∗ F ∼ unif K. By C-I NDEP, we have Cx←∆ (F ∼ unif K). By C-S UBST, we
                      as
have Cx←∆ (E[x/∆] = E ∧ F ∼ unif K). By applying U NIF -B IJECTION to E[x/∆], we have Cx←∆ (E[F/Y ] ∼ unif K).
Finally, by C-U NIF, we have own ∆ ∗ E[F/Y ] ∼ unif K.
C. Proof of Lemma VI.5
Proof of Lemma VI.5. Without loss of generality, we show the case where ∆ = {W1 , W2 }, X = {X1 , X2 }, and Y = {Y1 , Y2 }.
Also, let I = {W1 }, OM = {X1 }, and ON = {Y1 }. Then, we have the following.
                                                     W2 ⊥ X1 | W1 ∧ W2 , X2 ⊥ Y1 | W1 , X1
                                                      =⇒ W2 ⊥ X1 | W1 ∧ W2 ⊥ Y1 | W1 , X1
                                                      =⇒ W2 ⊥ X1 , Y1 | W1
                                                      =⇒ W2 ⊥ Y1 | W1
                             D P ROOFS FOR S ECTION VII (A PPLICATIONS TO P ROBING S ECURITY )
A. Detailed Proof of Theorem VII.1
Proof of Theorem VII.1. The proof outline is shown in Fig. 7. Here, we show non-trivial entailments used in the proof. We
often use E Q -C ONJ implicitly in the following.
       ′ as     j         j                       ′
   • X = X[V + ρj /X ] ∗ I(j; X) ⊢ I(j + 1; X ): By definition of I(j; X), the premise is equivalent to

                                                as
                                         X′ = X[V j + ρj /X j ] ∗ own(V, ρ, X) ∗                                 ∗ X =V +ρ .
                                                                                                               k<j
                                                                                                                         k as   k
                                                                                                                                       k


                                                         k
       – For each k ̸= j, we have own X ′ by T RANSFER -OWN.
                                                                         k as                                             k
                                                                   X ′ = X k ∧ own X j ⊢ own X ′
                             j
       – We have own X ′ by T RANSFER -OWN and FV-OWN.
                                                                                                           k as
                                                                  own V k ∧ own ρj ∧ X ′ = V k + ρj
                                                                                                          k as
                                                                   ⊢ own(V k + ρj ) ∧ X ′ = V k + ρj
                                                                                     k
                                                                   ⊢ own X ′
                                               k as                                                  as
       – For each k < j, we have X ′ = V k + ρk by transitivity of =.
                                                              as                              k as                k as
                                                         X k = V k + ρk ∧ X ′ = X k ⊢ X ′ = V k + ρk
                                         j as
       – We immediately have X ′ = V j + ρj from the premise.
      Therefore, we obtain the following entailments.
                                          as
                                       X′ = X[V j + ρj /X j ] ∗ own(V, ρ, X) ∗
                                                                               k<j
                                                                                   X k = V k + ρk          ∗         as


                                                                        k as                j as
                                                                  ^
                                       ⊢ own(V, ρ) ∧ own X′ ∧       (X ′ = V k + ρk ) ∧ X ′ = V j + ρj
                                                                                 k<j
                                       ⊢ I(j + 1; X′ )
  •   I(t + 1; X) ⊢ C(v,r)←(V∩I,ρ∩I) (own(V \ I, ρ \ I) ∗ own O):
                              as
           own(V, ρ) ∗ X = V + ρ
                                                             as
           ⊢         C             (own(V, ρ) ∗ X = V + ρ)                                                                                 by G EN -W EAK -U NION
               (v,r)←(V∩I,ρ∩I)
                                                     as         as
                                            ^
                      ∧             C           (v j = V j ∧ rj = ρj )                                                                               by C-S UBST
                          (v,r)←(V∩I,ρ∩I)
                                                 X j ∈O
                                                              as                                     as              as
                                                                                         ^
           ⊢         C             ((own(V, ρ) ∗ X = V + ρ) ∧                                  (v j = V j ∧ rj = ρj ))                by C-A ND -D ISTRIBUTIVE
               (v,r)←(V∩I,ρ∩I)
                                                                                     X j ∈O

       – By FV-OWN and □-M ONO and □-T RUE, we have ⊢ □ own(v j + rj ) for each X j ∈ O.
       – For each X j ∈ O, we also have the following entailment.
                                                                    as                   as
                             own V j ∧ own ρj ∧ v j = V j ∧ rj = ρj
                                                                                as                   as
                             ⊢ own(v j + rj , V j + ρj ) ∧ v j = V j ∧ rj = ρj                                                             by FV-OWN
                                   j       as        j
                             ⊢ v + rj = V + ρ j                                                                                     E Q -C ONGRUENCE
      Thus, we continue as follows.
                                                          as                                           as               as
                                                                                   ^
                C             ((own(V, ρ) ∗ X = V + ρ) ∧                                   (v j = V j ∧ rj = ρj ))
      (v,r)←(V∩I,ρ∩I)
                                                                                 X j ∈O
                                                                            as                                                                            as
                                                                                                       ^
      ⊢             C               (own(V \ I, ρ \ I) ∧ X = V + ρ ∧                                            (□ own(v j + rj ) ∧ v j + rj = V j + ρj ))
          (v,r)←(V∩I,ρ∩I)
                                                                                                   X j ∈O
                                                                                                                                   as
                                                                       ^
      ⊢             C               (own(V \ I, ρ \ I) ∧                         (□ own(v j + rj ) ∧ v j + rj = X j ))                                                       by transitivity
          (v,r)←(V∩I,ρ∩I)
                                                                      X j ∈O
                                                                                                                                   as
                                                                       ^
      ⊢             C               (own(V \ I, ρ \ I) ∗                         (□ own(v j + rj ) ∧ v j + rj = X j ))                                                         by □-C ONJ
          (v,r)←(V∩I,ρ∩I)
                                                                      X j ∈O
                                                                                                                              as
                                                                       ^
      ⊢             C               (own(V \ I, ρ \ I) ∗                         (own(v j + rj ) ∧ v j + rj = X j ))                                                           by □-E LIM
          (v,r)←(V∩I,ρ∩I)
                                                                      X j ∈O
      ⊢             C               (own(V \ I, ρ \ I) ∗ own O)                                                                                                        by T RANSFER -OWN
          (v,r)←(V∩I,ρ∩I)




B. Detailed Proof of Theorem VII.4
Proof of Theorem VII.4. The outline of the proof is shown in Fig. 9. We show the non-trivial entailments used in the proof.
We often use E Q -C ONJ implicitly in the following.
                     ′′  ′′ as           i         i  j     j                                       ′′   ′′
  • S ∼ unif K∗(C , R ) = (C, R)[Cj−1 +S/Cj , Ci −S/Ci+1 , S/Ri,j ]∗I(i, j; C, R) ⊢ I(i, j+1; C , R ): by T RANSFER -
                                                i
    D IST and E Q -C ONGRUENCE. Note that fj is defined so that the following holds for each i, j such that i < j.
                                                                                                                   j
                                                    fji (R) = fj−1
                                                               i
                                                                   (R) + Ri,j ,                                   fi+1 (R) = fij (R) − Ri,j

  •   own A ∗       ∗ (R ∼ unif K) ∗ ∗ (C = A + f (R)) ⊢ C (own(A \ I) ∗ own O): It suffices to prove the
                        i<j         i,j                        i,j
                                                                        i as
                                                                        j
                                                                                       i           i
                                                                                                   j                  a←I
      following.
                                own A ∗ ∗ (R ∼ unif K) ⊢ C (own(A \ I) ∗ ϕ )     i,j                 (11)                                           O
                                                                                                                                                    own
                                                                     i<j                                          a←I

      where
                                                  ^                                        ^                                             ^
                                     ϕO
                                      own :=                own Ri,j ∧                                 own(ai + fji (R)) ∧                       own(Ai + fti (R))
                                                Ri,j ∈O                           Cji ∈O,j<t                                            Cti ∈O

      because we have the following entailments then.
      own A ∗∗ (R ∼ unif K) ∗ ∗(C = A + f (R))
                    i<j
                              i,j
                                                    i,j
                                                               i as
                                                               j
                                                                        i          i
                                                                                   j


                           ) ∧ own I ∗ ∗(C = A + f (R)) ∧ C
                                                      
                                                                                   i as                                                      i as
                                                               ^
                                          O                                                    i            i                                        i
      ⊢ C (own(A \ I) ∗ ϕ                 own                    (a = A )          j                        j                                                              by C-S UBST
          a←I                                                           i,j                                              a←I
                                                                                                                               Ai ∈I

                           ) ∧ C ∗(C = A + f (R)) ∧ C                  i as                                                   i as
                                                         ^
                                          O                                       i        i                                         i
      ⊢ C (own(A \ I) ∗ ϕ                 own              (a = A )    j                   j                                                                               by C-I NDEP
          a←I                                       a←I i,j                                                     a←I
                                                                                                                     Ai ∈I

                            ) ∧ ∗(C = A + f (R)) ∧              i as                                               i as
                                                   ^
                                           O                                i          i                                  i
      ⊢ C ((own(A \ I) ∗ ϕ                 own       (a = A ))  j                      j                                                                       by C-A ND -D ISTRIBUTIVE
          a←I                                         i,j
                                                                                                        Ai ∈I
                                           ^
                                                                                                                                        as
                                                                                 ^
      ⊢ C (own(A \ I) ∗                             own Ri,j ∧                             (own(ai + fji (R)) ∧ Cji = ai + fji (R))
          a←I
                                          Ri,j ∈O                          Cji ∈O,j<t
                                                                         
                                                          as
                          ^
                    ∧            (own(Ai + fti (R)) ∧ Cji = Ai + fji (R)) )
                        Cti ∈O

      ⊢ C (own(A \ I) ∗ own O)                                                                                                                                      by T RANSFER -OWN
          a←I

      Now, we prove (11). Observe that free variables in fji (R) are the first j elements of
                                                          R0,i , R1,i , . . . , Ri−1,i , Ri,i+1 , Ri,i+2 , . . . , Ri,t                                                           (12)
      Let S ⊆ R be the set of random variables defined as follows.
                          S := {Ri,j | Ri,j ∈ O ∨ Ri,j is a free variable in fji (R) for some Cji ∈ O such that j < t}
    Then, the intersection of S and (12) is a subset of {Ri,j | i < j ∧ Aj ∈ I} ∪ {Rj,i | j < i ∧ Aj ∈ I}, which has at most
    |I| elements. Since |I| + |{Cji ∈ O | j = t}| ≤ |O| ≤ t, there exists an injective mapping from Cti ∈ O to Rj,k ∈ R \ S
    such that j = i or k = i (i.e., random variables in (12) excluding those in S). We write such Rj,k as R[Cti ]. Then, for
    each Cti ∈ O, we can see that Ai + fti (R) is a bijective function of R[Cti ] when other variables are fixed. Thus, we have
    the following entailments.
           own A ∗   ∗ (R ∼ unif K)
                     i<j
                             i,j
                                                                !
           ⊢ C
             a←I
                     own A ∗       ∗ (R ∼ unif K)
                                   i<j
                                                i,j                                                                    by G EN -W EAK -U NION
                                                                                                           !
           ⊢ C
             a←I
                     own(A \ I) ∗               ∗
                                            Cti ∈O
                                                      (R[Cti ] ∼ unif K) ∗       ∗ (R ∼ unif K)
                                                                                Ri,j ∈S
                                                                                           i,j

                                                                                                                !
           ⊢ C
             a←I
                     own(A \ I) ∗               ∗ (A
                                            Cti ∈O
                                                        i
                                                            + fti (R) ∼ unif K) ∗         ∗ (R ∼ unif K)
                                                                                      Ri,j ∈S
                                                                                                 i,j                           by Lemma C.1

    Moreover, since expressions in Ri,j ∈O own Ri,j ∧ C i ∈O,j<t own(ai + fji (R)) contain only random variables in S and
                                   V                     V
                                                           j
    deterministic variables, we have the following entailments.

                            ∗ (R ∼ unif K)
                           Ri,j ∈S
                                          i,j


                           ⊢ own S                                                                                  by D IST-OWN
                              ^                                 ^
                           ⊢       own Ri,j ∧                             own(ai + fji (R))                          by FV-OWN
                             Ri,j ∈O                         Cji ∈O,j<t

C. Proof of Theorem VII.8
Lemma D.1. Let E be a deterministic expression such that Γ; · ⊢ E : A. Then, we have
                                                                      as
                                                                    X=E          ⊢    own X
Proof.
                                     as
                               X=E
                                           as
                                   ⊢ X = E ∧ own E                                                          by FV-OWN
                                   ⊢ own X                                                        by T RANSFER -OWN
Lemma D.2. Let Γ; ∆, X : A ⊢ E : B be an expression. Then, we have
                                                                                                        as      
                           (own ∆ ∧ own X) ∗ ϕ                    ⊢        C    (own ∆ ∧ own X) ∗ ϕ ∗ E = E[x/X]
                                                                          x←X

Proof.
         (own ∆ ∧ own X) ∗ ϕ
                                             as
         ⊢ C     (own ∆ ∧ own X) ∗ ϕ ∧ C X = x                                                         by G EN -W EAK -U NION and C-S UBST
           x←X                          x←X
                                         as 
         ⊢ C     (own ∆ ∧ own X) ∗ ϕ ∧ X = x                                                                     by C-A ND -D ISTRIBUTIVE
           x←X
                                                      as 
         ⊢ C (own ∆ ∧ own X) ∗ ϕ ∧ own(E, E[x/X]) ∧ X = x                                                                      by FV-OWN
          x←X
                                     as       
         ⊢ C (own ∆ ∧ own X) ∗ ϕ ∧ E = E[x/X]                                                                          by E Q -C ONGRUENCE
          x←X
                                     as      
         ⊢ C (own ∆ ∧ own X) ∗ ϕ ∗ E = E[x/X]                                                                                 by E Q -C ONJ
           x←X

Proof of Theorem VII.8. I, J, KQ , and KS satisfy the following conditions:
  1) |I|, |J| ≤ |O \ Ct |
  2) If Cji ∈ O and j < t, then i ∈ I ∩ J.
  3) If i < j, Cji ∈ O, and i < k ≤ j < t, then (i, k) ∈ KQ .
  4) If Cji ∈ O, k < i, j < t, and (k, i) ∈ KQ , then k, i ∈ I and k, i ∈ J.
  5) If Qi,j ∈ O, then (i, j) ∈ KQ .
  6) If Ri,j ∈ O, then (i, j) ∈ KQ , i ∈ I, and j ∈ J.
  7) If (i, j) ∈ KQ and Si,j ∈ O, then i, j ∈ I and i, j ∈ J.
  8) If Cti ∈ O and there exists j < t with Cji ∈ O, then Vi ⊆ KQ ∪ KS .
  9) If Cti ∈ O and there is no j < t with Cji ∈ O, then Vi \ (KQ ∪ KS ) ̸= ∅.
Here, Vi = {(k, i) | k < i} ∪ {(i, k) | i < k} is the indices of the free variables in gti (Q, S). Condition 9 follows because
|Vi ∩ (KQ ∪ KS )| ≤ |O \ Ct | < |Vi | = t.
                                                             Vi ∩ (KQ ∪ KS )
                                                                 = Vi ∩ {(i, j) | Qi,j ∈ Q ∨ Ri,j ∈ O ∨ Si,j ∈ O}
                                                                         ∪ {(k, i) | k < i, Cjk ∈ O, j < t}
                                                                         ∪ {(i, k) | i < k, Cjk ∈ O, j < t}
In other words, we have |O ∩ Ct | ≤ |Vi \ (KQ ∪ KS )|. Thus, for each Cti ∈ O with no j < t such that Cji ∈ O, we take an
element of Vi \ (KQ ∪ KS ) in such a way that the chosen elements are distinct for distinct Cti ’s, and define the set KC as
the set of the chosen elements.
   By applying the rules in Fig. 4, we obtain the following postcondition (Fig. 11).
own(A, B) ∗        ∗ P = A × B ∗ ∗ Q ∼ unif K ∗ ∗ R = Q + P ∗ ∗ S = R + P ∗ ∗ C = P + g (Q, S)
                   i,j
                          i,j
                                as     i          j
                                                       i<j
                                                                   i,j
                                                                                                  i<j
                                                                                                               i,j
                                                                                                                         as
                                                                                                                                   i,j         i,j
                                                                                                                                                       i<j
                                                                                                                                                                 i,j
                                                                                                                                                                       as
                                                                                                                                                                                 i,j         j,i
                                                                                                                                                                                                   i,j
                                                                                                                                                                                                           i as
                                                                                                                                                                                                           j       i,i
                                                                                                                                                                                                                         i
                                                                                                                                                                                                                         j


  By applying G EN -W EAK -U NION and C-S UBST, we have the following postcondition.

               C
       (a,b)←(I,J )
                                 ∗ P = A × B ∗ ∗ Q ∼ unif K ∗ ∗ R = Q + P ∗ ∗ S = R + P
                          own(A, B) ∗
                                                      i,j
                                                             i,j
                                                                   as          i            j
                                                                                                 i<j
                                                                                                           i,j
                                                                                                                                               i<j
                                                                                                                                                           i,j
                                                                                                                                                                 as
                                                                                                                                                                           i,j         i,j
                                                                                                                                                                                              i<j
                                                                                                                                                                                                     i,j
                                                                                                                                                                                                           as
                                                                                                                                                                                                                  i,j    j,i


                     ∗ ∗ C = P + g (Q, S) ∗ ∗ A = a ∗ ∗ B = b
                                i as                   i                               i          i                      j           j
                                                              
                                j           i,i        j
                         i,j                                               i∈I                            j∈J

It follows that the above postcondition implies:

                                                            ∗
                   
                                                                           as                  as
                                                                     ^                  ^
                                       Qi,j ∼ unif K ∧ own(A, B, Q) ∧ Pi,j = Ai × B j ∧
                                                    
            C         own(A, B) ∗                                                         Ri,j = Qi,j + Pi,j
        (a,b)←(I,J )                                       i<j
                                                                                                                                                     i,j                                     i<j
                         ^             as
                                                                         ^             as
                                                                                                                                     ^           as
                                                                                                                                                                 ^             as   
                     ∧          Si,j = Ri,j + Pj,i ∧                           Cji = Pi,i + gji (Q, S) ∧                                      Ai = ai ∧                    B j = bj
                         i<j                                             i,j                                                         i∈I                         j∈J

Then, we focus on the underlined part; rewrite the equations for Pi,j , Ri,j , Si,j , and Cji ; and obtain equations for O.
  • Pi,j :

                                                 as                    as                as
                                         ^                     ^                ^
                                           Pi,j = Ai × B j ∧      Ai = ai ∧          B j = bj
                                                                     i,j                                                 i∈I                          j∈J
                                                                                                          as
                                                                                    ^
                                                                                                                 i             j
                                                                     ⊢                           Pi,j = a × b
                                                                           (i,j)∈I×J
                                                                                                  as
                                                                                   ^
                                                                     ⊢                      Pi,j = ai × bj
                                                                           Pi,j ∈O

  •   Ri,j :
                                                                                                  as                                                                  as
                                                                                   ^                                                           ^
                                                            own Q ∧                      Ri,j = Qi,j + Pi,j ∧                                              Pi,j = ai × bj
                                                                                   i<j                                                   (i,j)∈I×J
                                                                                            as
                                                                    ^
                                                                                                                 i             j
                                                            ⊢                      Ri,j = Qi,j + a × b
                                                                 Ri,j ∈O



  •   Si,j :
                                                                                     as                                                  as                                             as
                                                                    ^                                                ^                                                     ^
                                 own(A, B, Q) ∧                            Pi,j = Ai × B j ∧                                  Ri,j = Qi,j + Pi,j ∧                               Si,j = Ri,j + Pj,i
                                                                    i,j                                              i<j                                                   i<j
                                                      as
                                     ^
                                                                               i            j         j              i
                                 ⊢           Si,j = Qi,j + A × B + A × B
                                     i<j
      If Si,j ∈ O and (i, j) ∈ KQ , then i, j ∈ I and i, j ∈ J by Condition 7, and thus:
                                          as                                     as            as
                                 ^                                        ^              ^
                                     Si,j = Qi,j + Ai × B j + Aj × B i ∧      Ai = ai ∧    B j = bj
                                           i<j                                                 i∈I             j∈J
                                                                       as
                                                      ^
                                                                                      i   j       j      i
                                           ⊢                       Si,j = Qi,j + a × b + a × b
                                               (i,j)∈KQ ,Si,j ∈O

                                                 as                                       as                                 as
  •   Cji : First note that we have Cji = Ai × B i + gji (Q, S) from Cji = Pi,i + gji (Q, S) and Pi,i = Ai × B i .
       – If Cji ∈ O and j < t, then i ∈ I and i ∈ J by Condition 2.
                                     as                                 as                                     as           as
                               ^                                ^                                        ^            ^
            own(A, B, Q) ∧ Cji = Ai × B i + gji (Q, S) ∧           Si,j = Qi,j + Ai × B j + Aj × B i ∧      Ai = ai ∧   B j = bj
                                    i,j                                         i<j                                               i∈I        j∈J
                                as
                  ^
           ⊢                Cji = ai × bi + gji (Q, S)
               Cji ∈O,j<t


          If Sk,i is a free variable in gji (Q, S) and (k, i) ∈ KQ , then by Condition 4, k, i ∈ I and k, i ∈ J, and thus
               as
          Sk,i = Qk,i + ak × bi + ai × bk . Hence, we obtain
                                                                 as
                                                       ^
                                                             Cji = ai × bi + hij (Q, S)
                                                                   Cji ∈O,j<t


          where hij (Q, S) is defined as follows.
                                         X                                          X
                                   
                                                 (Qk,i + ak × bi + ai × bk ) +              Sk,i                                       i≥j
                                   
                      i              k<j,(k,i)∈KQ                               k<j,(k,i)∈K
                                                                                         / Q
                     hj (Q, S) :=        X                                          X               X
                                   
                                   
                                                 (Qk,i + ak × bi + ai × bk ) +              Sk,i +   Qi,k                              i<j
                                               k<i,(k,i)∈KQ                                           k<i,(k,i)∈K
                                                                                                               / Q           i<k≤j


         Note that the free variables in hij (Q, S) are in {Si,j | (i, j) ∈ KS \ KQ } ∪ {Qi,j | (i, j) ∈ KQ } if Cji ∈ O and j < t.
       – If Cti ∈ O and there exists j < t with Cji ∈ O, then similarly to the previous case, we have the following equations.
                                                                         as
                                                         ^
                                                                    Cti = ai × bi + hit (Q, S)
                                                             Cti ∈O,(∃j<t,Cji ∈O)


         The free variables in hit (Q, S) are in {Si,j | (i, j) ∈ KS \ KQ } ∪ {Qi,j | (i, j) ∈ KQ }.
       – If Cti ∈ O and there exists no j < t with Cji ∈ O:
                                                  as                                as
                                           ^                                ^
                       own(A, B, Q) ∧         Cji = Ai × B i + gji (Q, S) ∧    Si,j = Qi,j + Ai × B j + Aj × B i
                                                       i,j                                      i<j
                                                                 as
                                               ^
                              ⊢                              Cti = Ai × B i + gti (Q, {Qi,j + Ai × B j + Aj × B i }i<j )
                                  Cti ∈O,¬(∃j<t,Cji ∈O)


         Note that for each such Cti , there exists Qi′ ,j ′ ∈ KC that occurs in gti (Q, {Qi,j + Ai × B j + Aj × B i }i<j ), and
         moreover, the right-hand side of the above equation is a bijective expression in Qi′ ,j ′ .
By E Q -C ONJ, we now have the following postcondition.

                                            ∗                               ∗
                
                                                                        as
          C       own(A, B) ∗       Qi,j ∼ unif K ∗                Si,j = Qi,j + Ai × B j + Aj × B i
      (a,b)←(I,J )                         i<j                        (i,j)∈KS \KQ
                                      as                               as                                               as
                         ^                                   ^                                          ^
                  ∗              Pi,j = ai × bj ∧                 Ri,j = Qi,j + ai × bj ∧                           Si,j = Qi,j + ai × bj + aj × bi
                       Pi,j ∈O                          Ri,j ∈O                                 (i,j)∈KQ ,Si,j ∈O
                                       as                                                          as
                         ^                                                        ^
                                   Cji = ai × bi + hij (Q, S) ∧                                Cti = ai × bi + hit (Q, S)
                                                                                                                         
                  ∧
                      Cji ∈O,j<t                                       Cti ∈O,(∃j<t,Cji ∈O)

                             ∗
                                                                                                            
                                                     as
                  ∗                              Cti = Ai × B i + gti (Q, {Qi,j + Ai × B j + Aj × B i }i<j )
                      Cti ∈O,¬(∃j<t,Cji ∈O)
Now, we divide      ∗   i<j Qi,j ∼ unif K into three parts (technically, four parts, but one part is discarded).

                             ∗ Q ∼ unif K
                           i<j
                                   i,j

                             ⊢ ∗   Q ∼ unif K ∗
                                             i,j∗                                 Qi,j ∼ unif K ∗            ∗       Qi,j ∼ unif K
                                (i,j)∈KQ                           (i,j)∈KS \KQ                         (i,j)∈KC

Then, we apply Lemma C.1 and T RANSFER -U NIFORM to the second part and the third part, respectively.
     own(A, B) ∗           ∗
                        (i,j)∈KS \KQ
                                         Qi,j ∼ unif K ∗             ∗
                                                               (i,j)∈KS \KQ
                                                                                     as
                                                                                Si,j = Qi,j + Ai × B j + Aj × B i

     ⊢ own(A, B) ∗             ∗
                          (i,j)∈KS \KQ
                                           Si,j ∼ unif K

     own(A, B) ∗          ∗
                        (i,j)∈KC
                                   Qi,j ∼ unif K ∗                 ∗
                                                          Cti ∈O,¬(∃j<t,Cji ∈O)
                                                                                          as
                                                                                    Cti = Ai × B i + gti (Q, {Qi,j + Ai × B j + Aj × B i }i<j )

     ⊢ own(A, B) ∗                ∗
                          Cti ∈O,¬(∃j<t,Cji ∈O)
                                                    Cti ∼ unif K

The current postcondition is as follows.

                                             ∗                                   ∗
                
         C        own(A, B) ∗            Qi,j ∼ unif K ∗                                       Si,j ∼ unif K
     (a,b)←(I,J )                          (i,j)∈KQ                           (i,j)∈KS \KQ
                                      as                                 as                                                 as
                         ^                               ^                                             ^
                 ∗              Pi,j = ai × bj ∧                 Ri,j = Qi,j + ai × bj ∧                             Si,j = Qi,j + ai × bj + aj × bi
                      Pi,j ∈O                          Ri,j ∈O                                   (i,j)∈KQ ,Si,j ∈O
                                      as                                                            as
                         ^                                                       ^
                                  Cji = ai × bi + hij (Q, S) ∧                                  Cti = ai × bi + hit (Q, S)
                                                                                                                          
                 ∧
                     Cji ∈O,j<t                                          Cti ∈O,(∃j<t,Cji ∈O)

                           ∗
                                                                 
                 ∗                            Cti ∼ unif K
                     Cti ∈O,¬(∃j<t,Cji ∈O)

Here, the free variables of the right-hand sides of the remaining equations are in {Qi,j | (i, j) ∈ KQ }∪{Si,j | (i, j) ∈ KS \KQ }.
By applying T RANSFER -OWN, we obtain the following postcondition.
                                   ^                       ^                     ^                  ^
       C        own(A, B) ∗               own Qi,j ∧                own Si,j ∧         own Pi,j ∧         own Ri,j
 (a,b)←(I,J )
                                         (i,j)∈KQ                    (i,j)∈KS \KQ                  Pi,j ∈O                   Ri,j ∈O

                                                                                                                                 ∗
                         ^                               ^                                 ^                                                                    
                                                                   own Cji ∧                           own Cti                                   Cti ∼ unif K
                                                                                                                 
            ∧                       own Si,j ∧                                                                       ∗
                                                                                                                         Cti ∈O,¬(∃j<t,Cji ∈O)
                (i,j)∈KQ ,Si,j ∈O                     Cji ∈O,j<t                Cti ∈O,(∃j<t,Cji ∈O)

By definition of KQ and KS , we finally have the following postcondition.
                                                           C         (own(A \ I, B \ J ) ∗ own O)
                                                      (a,b)←(I,J )
