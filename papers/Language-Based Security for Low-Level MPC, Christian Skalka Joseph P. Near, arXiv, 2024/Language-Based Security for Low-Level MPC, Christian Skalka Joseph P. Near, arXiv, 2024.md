                                                                     Language-Based Security for Low-Level MPC
                                                                          Christian Skalka                                                                     Joseph P. Near
                                                                        University of Vermont                                                               University of Vermont
                                                                         ceskalka@uvm.edu                                                                     jnear@uvm.edu
                                         ABSTRACT                                                                                         [30] but mostly manual. Somewhat independently, a signiﬁcant
                                         Secure Multi-Party Computation (MPC) is an important enabling                                    body of work in programming languages has focused on deﬁni-
                                         technology for data privacy in modern distributed applications.                                  tion and enforcement of conﬁdentiality and integrity hyperproper-
                                         Currently, proof methods for low-level MPC protocols are primar-                                 ties [14] such as noninterference and gradual release [6, 40]. Fol-
arXiv:2407.16504v1 [cs.CR] 23 Jul 2024




                                         ily manual and thus tedious and error-prone, and are also non-                                   lowing a tradition of connecting cryptographic and PL-based secu-
                                         standardized and unfamiliar to most PL theorists. As a step towards                              rity models [1, 24], recent work has also recognized connections
                                         better language support and language-based enforcement, we de-                                   between MPC security models and hyperproperties of, e.g., nonin-
                                         velop a new staged PL for deﬁning a variety of low-level probabilis-                             terference [22], and even leveraged these connections to enforce
                                         tic MPC protocols. We also formulate a collection of conﬁdential-                                MPC security through mechanisms such as security types [3]. Ma-
                                         ity and integrity hyperproperties for our language model that are                                jor beneﬁts of this connection in an MPC setting include better lan-
                                         familiar from information ﬂow, including conditional noninterfer-                                guage abstractions for deﬁning protocols and for mechanization
                                         ence, gradual release, and robust declassiﬁcation. We demonstrate                                and even automation of security proofs. The goal of this paper is
                                         their relation to standard MPC threat models of passive and mali-                                to develop a PL model for deﬁning a variety of low-level probabilis-
                                         cious security, and how they can be leveraged in security veriﬁca-                               tic MPC protocols, to formulate a collection of conﬁdentiality and
                                         tion of protocols. To prove these properties we develop automated                                integrity hyperproperties for our model with familiar information
                                         tactics in F2 that can be integrated with separation logic-style rea-                            ﬂow analogs, and to show how these properties can be leveraged
                                         soning.                                                                                          for improved proof automation.
                                                                                                                                              The distinction between high- and low-level languages for MPC
                                         CCS CONCEPTS                                                                                     is important. High-level languages such as Wysteria [37] and Viaduct
                                                                                                                                          [3] are designed to provide eﬀective programming of full applica-
                                         • Security and privacy → Logic and veriﬁcation; • Theory
                                                                                                                                          tions. These language designs incorporate sophisticated veriﬁed
                                         of computation → Probabilistic computation; Programming
                                                                                                                                          compilation techniques such as orchestration [2] to guarantee high-
                                         logic.
                                                                                                                                          level security properties, and they rely on libraries of low-level
                                         KEYWORDS                                                                                         MPC protocols, such as binary and arithmetic circuits. These low-
                                                                                                                                          level protocols encapsulate abstractions such as secret sharing and
                                         Secure multiparty computation, security veriﬁcation, probabilistic                               semi-homomorphic encryption, and must be veriﬁed by hand. So,
                                         programming, programming languages, information ﬂow.                                             low-level MPC programming and protocol veriﬁcation remains a
                                         ACM Reference Format:                                                                            distinct challenge and both critical to the general challenge of PL
                                         Christian Skalka and Joseph P. Near. 2024. Language-Based Security for                           design for MPC and complementary to high-level language design.
                                         Low-Level MPC. In Proceedings of the 26th Symposium on Principles and                                The connection between information ﬂow hyperproperties and
                                         Practice of Declarative Programming, PPDP 2024, Milano, Italy, September                         MPC security is also complicated especially at a low level. MPC
                                         10-11, 2024. ACM, New York, NY, USA, 14 pages.
                                                                                                                                          protocols involve communication between a group of distributed
                                                                                                                                          clients called a federation that collaboratively compute and pub-
                                         1     INTRODUCTION                                                                               lish the result of some known ideal functionality F , maintaining
                                         Secure Multi-Party Computation (MPC) protocols support data pri-                                 conﬁdentiality of inputs to F without the use of a trusted third
                                         vacy in important modern, distributed applications such as privacy-                              party. However, since the outputs of F are public, some informa-
                                         preserving machine learning [26, 27, 29, 31] and Zero-Knowledge                                  tion about inputs is inevitably leaked. Thus, the ideal functional-
                                         proofs in blockchains [20, 25, 32, 43]. The security semantics of                                ity establishes a declassiﬁcation policy [40], which is more diﬃ-
                                         MPC include both conﬁdentiality and integrity properties incor-                                  cult to enforce than pure noninterference. And subtleties of, e.g.,
                                         porated into models such as real/ideal (aka simulator) security and                              semi-homomorphic encryption are central to both conﬁdentiality
                                         universal composability (UC), developed primarily by the cryptog-                                and integrity properties of protocols and similarly diﬃcult to track
                                         raphy community [19]. Related proof methods are well-studied                                     with coarse-grained security types alone.
                                         Permission to make digital or hard copies of all or part of this work for personal or                Nevertheless, as previous authors have observed [12], low-level
                                         classroom use is granted without fee provided that copies are not made or distributed            protocol design patterns such as secret sharing and circuit gate
                                         for proﬁt or commercial advantage and that copies bear this notice and the full cita-            structure have compositional properties that can be independently
                                         tion on the ﬁrst page. Copyrights for components of this work owned by others than
                                         the author(s) must be honored. Abstracting with credit is permitted. To copy other-              veriﬁed and then leveraged in larger proof contexts. We contribute
                                         wise, or republish, to post on servers or to redistribute to lists, requires prior speciﬁc       to this line of work by developing an automated veriﬁcation tech-
                                         permission and/or a fee. Request permissions from permissions@acm.org.
                                         PPDP ’24, September 10-11, 2024, Milano, Italy
                                                                                                                                          nique for subprotocols and show how it can be integrated as a tac-
                                         © 2024 Copyright held by the owner/author(s). Publication rights licensed to ACM.                tic in a larger security proof.
                                         ACM ISBN 9-8-4007-0969-297. . . $15.00

                                                                                                                                      1
PPDP ’24, September 10-11, 2024, Milano, Italy                                                                                                                 Christian Skalka and Joseph P. Near




                                                                                                                                  probabilistic conditioning
1.1     Overview and Contributions




                                                                                                         probabilistic language
In summary, our work provides a complete methodology for end-




                                                                                                                                                                  low-level protocols



                                                                                                                                                                                                           malicious security
to-end veriﬁcation of MPC protocols via three components:




                                                                                                                                                                                                                                hyperproperties
                                                                                                                                                                                        passive security
   (1) A low-level language for deﬁning MPC primitives (Section




                                                                                                                                                                                                                                                  automation
       2) with an associated metalanguage to ease programming
       (Section 6)1 .
   (2) A fully-automated veriﬁcation method for low-level MPC
       primitives in F2 (Section 5).
   (3) A partially-automated veriﬁcation method for MPC pro-                  Haskell EDSL [34]             X                                                       X                     X                                       X               X
       tocols, which leverages automated proofs for low-level prim-           MPC in SecreC [5]             X                        X                                                    X                                       X               X
       itives (Section 7).                                                    𝜆obliv [17]                   X                                                       X                                                             X               X
As part of this methodology, we also develop hyperproperties that             PSL [8]                       X                                                       X
encode MPC security that may be of independent interest. The                  Lilac [28]                    X                        X
complete methodology enables the veriﬁcation of real-world MPC                Wys∗ [38]                                                                                                   X                                       X               X
protocols like GMW [21].                                                      Viaduct [2, 3]                                                                                              X                  X                    X               X
                                                                              MPC in EasyCrypt [22]         X                        X                              X                     X                  X                    X
   Language design. In Section 2 we develop a new probabilistic               Prelude/Overture              X                        X                              X                     X                  X                    X               X
programming language Overture for deﬁning synchronous distributed
protocols over an arbitrary arithmetic ﬁeld. The syntax and se-
                                                                          Figure 1: Comparison of systems for veriﬁcation of MPC se-
mantics provides a succinct account of synchronous messaging
                                                                          curity in PLs.
between protocol clients. In Section 6 we deﬁne a metalanguage
Prelude that dynamically generates Overture protocols. It is able to
express important low-level abstractions, as we illustrate via im-
plementations of protocols including Shamir addition (Section 2),
GMW boolean circuits (Section 7), and Beaver Triple multiplica-           1.2 Related Work
tion gates with BDOZ authentication (Section 7.2).                         Our main focus is on PL design and automated and semi-automated
                                                                           reasoning about security properties of low-level MPC protocols.
    Hyperproperty formulation. In Section 3 we develop our formal-         Prior work has considered automated veriﬁcation of high-level
ism for expressing the joint probability mass function of program          protocols and manual veriﬁcation of low-level protocols—but none
variables, and give standard deﬁnitions of passive and malicious           oﬀers the combination of automation and low-level support we
real/ideal security in our model. In Section 4, we formulate a vari-       consider. We summarize this comparison in Figure 1, with the caveat
ety of familiar information ﬂow properties in our probabilistic set-       that works vary in the degree of development in each dimension.
ting, including conditional noninterference, gradual release, and             As mentioned above, several high-level languages have been de-
robust declassiﬁcation, and consider the relation between these            veloped for writing MPC applications, and frequently exploit the
and real/ideal security. While it has been previously shown that           connection between hyperproperties and MPC security. Previous
probabilistic conditional noninterference is sound for passive secu-       work on analysis for the SecreC language [5, 11] is concerned with
rity, we formulate new properties of integrity which, paired with          properties of complex MPC circuits, in particular a user-friendly
passive security, imply malicious security (Theorem 4.8). We ob-           speciﬁcation and automated enforcement of declassiﬁcation bounds
serve in Section 7.2 that authentication mechanisms such as BDOZ/SPDZ in programs that use MPC in subprograms. The Wys★ language
style MACs enforce a strictly weaker property of “cheating detec-          [38], based on Wysteria [37], has similar goals and includes a trace-
tion” (Lemma 7.10).                                                        based semantics for reasoning about the interactions of MPC proto-
    Fully and partially automated veriﬁcation. In Section 5 we de-         cols. Their compiler also guarantees that underlying multi-threaded
                                                                           protocols enforce the single-threaded source language semantics.
velop a method for automatically computing the probability mass
function (pmf) of Overture protocols in F2 , that can be automati-         These  two lines of work were focused on passive security. The
cally queried to enforce hyperproperties of security. This method          Viaduct  language [3] has a well-developed information ﬂow type
                                                                           system that automatically enforces both conﬁdentiality and integrity
is perfectly accurate but has high complexity; we show this can
be partially mitigated by conversion of protocols in F2 to strati-         through hyperproperties such as robust declassiﬁcation, in addi-
ﬁed Datalog which is amenable to HPC acceleration. Furthermore,            tion to rigorous compilation guarantees through orchestration [2].
                                                                           However, these high level languages lack probabilistic features and
in Section 7 we consider in detail how this automated technique
can be used as a local automated tactic for proving security in ar-        other abstractions of low-level protocols, the implementation and
bitrarily large GMW circuits using conditional probabilistic inde-         security of which are typically assumed as a selection of library
                                                                           components.
pendence as in [28] (Lemmas 7.4 and 7.3 and Theorem 7.6).
                                                                              Various related low-level languages with probabilistic features
                                                                           have also been developed. The 𝜆obliv language [17] uses a type
1 By metalanguage we mean a multi-stage aka metaprogramming language where system to automatically enforce so-called probabilistic trace oblivi-
code is a value, as in, e.g., MetaML [42].                                 ousness. But similar to previous work on oblivious data structures
                                                                      2
Language-Based Security for Low-Level MPC                                                                     PPDP ’24, September 10-11, 2024, Milano, Italy


[45], obliviousness is related to pure noninterference, not the re-           𝑣 ∈ F𝑝 , 𝑤 ∈ String, 𝜄 ∈ Clients ⊂ N
laxed form related to passive MPC security. The Haskell-based se-
curity type system in [34] enforces a version of noninterference              𝜀   ::=   r[𝑤] | s[𝑤] | m[𝑤] | p[𝑤] |                            expressions
that is sound for passive security, but does not verify the correct-                    𝑣 | 𝜀 −𝜀 | 𝜀 +𝜀 | 𝜀 ∗𝜀
ness of declassiﬁcations and does not consider malicious security.            𝑥   ::=   r[𝑤]@𝜄 | s[𝑤]@𝜄 | m[𝑤]@𝜄 | p[𝑤] | out@𝜄                  variables
And properties of real/ideal passive and malicious security for a
probabilistic language have been formulated in EasyCrypt [22]–                c   ::=   m[𝑤]@𝜄 := 𝜀@𝜄 | p[𝑤] := 𝑒@𝜄 | out@𝜄 := 𝜀@𝜄 commands
though their proof methods, while mechanized, are fully manual,               𝜋   ::=   ∅ | c; 𝜋                                                 protocols
and their formulation of malicious security is not as clearly related
to robust declassiﬁcation as is the one we present in Section 4.
   Program logics for probabilistic languages and speciﬁcally rea-
                                                                                                  J𝜎, 𝑣K𝜄     =   𝑣
soning about properties such as joint probabilistic independence is
                                                                                           J𝜎, 𝜀 1 + 𝜀 2 K𝜄   =   JJ𝜎, 𝜀 1 K𝜄 + J𝜎, 𝜀 2 K𝜄 K
also important related work. Probabilistic Separation Logic (PSL)
                                                                                           J𝜎, 𝜀 1 − 𝜀 2 K𝜄   =   JJ𝜎, 𝜀 1 K𝜄 − J𝜎, 𝜀 2 K𝜄 K
[8] develops a logical framework for reasoning about probabilis-
                                                                                           J𝜎, 𝜀 1 ∗ 𝜀 2 K𝜄   =   JJ𝜎, 𝜀 1 K𝜄 ∗ J𝜎, 𝜀 2 K𝜄 K
tic independence (aka separation) in programs, and they consider
                                                                                            J𝜎, r[𝑤]K𝜄        =   𝜎 (r[𝑤]@𝜄)
several (hyper)properties, such as perfect secrecy of one-time-pads
                                                                                            J𝜎, s[𝑤]K𝜄        =   𝜎 (s[𝑤]@𝜄)
and indistinguishability in secret sharing, that are critical to MPC.
                                                                                            J𝜎, m[𝑤]K𝜄        =   𝜎 (m[𝑤]@𝜄)
However, their methods are manual, and don’t include conditional
                                                                                            J𝜎, p[𝑤]K𝜄        =   𝜎 (p[𝑤])
independence (separation). This latter issue has been addressed in
Lilac [28]. The application of Lilac-style reasoning to MPC proto-
cols has not previously been explored, as we do in Section 7.
   Our work also shares many ideas with probabilistic program-
ming languages designed to perform (exact or approximate) statis-                                            − (𝜎{𝑥 ↦→ J𝜎, 𝜀K𝜄 }, 𝜋)
                                                                                            (𝜎, 𝑥 := 𝜀@𝜄; 𝜋) →
tical inference [4, 10, 13, 18, 23, 36, 39, 44]. Our setting, however,
requires verifying properties beyond inference, including condi-             Figure 2: Top-to-bottom: Basic Overture syntax, expression
tional statistical independence. Recent work by Li et al. [28] pro-          interpretation, and command evaluation.
poses a manual approach for proving such properties, but does not
provide automation.
                                                                                  • m[𝑤]@𝜄 2 := 𝜀@𝜄 1 : This is a message send where expression
                                                                                    𝜀 is computed by client 𝜄 1 and sent to client 𝜄 2 as message
2     THE Overture PROTOCOL LANGUAGE                                                m[𝑤].
The Overture language establishes a basic model of synchronous                    • p[𝑤] := 𝜀@𝜄: This is a public reveal where expression 𝜀 is
protocols between a federation of clients exchanging values in the                  computed by client 𝜄 and broadcast to the federation, typ-
binary ﬁeld. A model of synchronous communication captures a                        ically to communicate intermediate results for use in ﬁnal
wide range of MPC protocols. Concurrency is out of scope in this                    output computations.
work but an avenue for future work. The lack of sophisticated con-                • out@𝜄 := 𝜀@𝜄: This is an output where expression 𝜀 is com-
trol structures in Overture is intentional, since minimizing features               puted by client 𝜄 and reported as its output. As a sanity con-
eases analysis and control abstractions such as function deﬁnitions                 dition we disallow commands out@𝜄 1 := 𝜀@𝜄 2 where 𝜄 1 ≠ 𝜄 2 .
can be integrated into a metalanguage that generates Overture pro-           For example, in the following protocol, a client 1 subtracts a ran-
grams (Section 6).                                                           dom sample r[𝑦] from F𝑝 from their secret value s[𝑥] and sends
   We identify clients by natural numbers and federations- ﬁnite             the result to client 2 as a message m[𝑧]:
sets of clients- are always given statically. Our threat model as-
sumes a partition of the federation into honest 𝐻 and corrupt 𝐶                                    m[𝑧]@2 := (s[𝑥] − r[𝑦])@1
subsets. We model probabilistic programming via a random tape                Both messages m[𝑤] and reveals p[𝑤] can be referenced in ex-
semantics. That is, we will assume that programs can make refer-             pressions once they’ve been deﬁned. This distinction between mes-
ence to values chosen from a uniform random distributions deﬁned             sages and broadcast public reveal is consistent with previous for-
in the initial program memory. Programs aka protocols execute de-            mulations, e.g., [34]. To identify and distinguish between collec-
terministically given the random tape.                                       tions of variables in protocols we introduce the following notation.
                                                                                Deﬁnition 2.1. We let 𝑥 range over variables which are identi-
2.1    Syntax                                                                ﬁers where client ownership is speciﬁed- e.g., m[foo]@𝜄 is a mes-
The syntax of Overture, deﬁned in Figure 2, includes values 𝑣 and            sage foo that was sent to 𝜄. We let 𝑋 range over sets of variables,
standard operations of addition, subtraction, and multiplication in          and more speciﬁcally, 𝑆 ranges over sets of secret variables s[𝑤]@𝜄,
a ﬁnite ﬁeld F𝑝 where 𝑝 is some prime. Protocols are given input             𝑅 ranges over sets of random variables r[𝑤]@𝜄, 𝑀 ranges over sets
secret values s[𝑤] as well as random samples r[𝑤] on the input               of message variables m[𝑤]@𝜄, 𝑃 ranges over sets of public variables
tape, implemented using a memory as described below (Section                 p[𝑤], and 𝑂 ranges over sets of output variables out@𝜄. Given a
2.2) where 𝑤 is a distinguishing identiﬁer string. Protocols are se-         program 𝜋, we write iovars(𝜋) to denote the particular set 𝑆 ∪ 𝑀 ∪
quences of assignment commands of three diﬀerent forms:                      𝑃 ∪ 𝑂 of variables in 𝜋 and secrets(𝜋) to denote 𝑆, and we write
                                                                         3
PPDP ’24, September 10-11, 2024, Milano, Italy                                                                           Christian Skalka and Joseph P. Near


rands(𝜋) to denote the particular set 𝑅 of random samplings in 𝜋.             as a one-time pad with another random sample r[𝑥] and s[𝜄]. This
We write vars(𝜋) to denote iovars(𝜋)∪rands(𝜋). For any set of vari-           yields two secret shares communicated as messages to the other
ables 𝑋 and clients 𝐼 , we write 𝑋𝐼 to denote the subset of 𝑋 owned           clients, while each client keeps r[local] as its own share.
by any client 𝜄 ∈ 𝐼 , in particular we write 𝑋𝐻 and 𝑋𝐶 to denote the
                                                                                         m[𝑠1]@2        :=     (s[1] − r[local] − r[𝑥])@1
subsets belonging to honest and corrupt parties, respectively.
                                                                                         m[𝑠1]@3        :=     r[𝑥]@1
                                                                                         m[𝑠2]@1        :=     (s[2] − r[local] − r[𝑥])@2
2.2     Semantics
                                                                                         m[𝑠2]@3        :=     r[𝑥]@2
Memories are fundamental to the semantics of Overture and pro-                           m[𝑠3]@1        :=     (s[3] − r[local] − r[𝑥])@3
vide random tape and secret inputs to protocols, and also record                         m[𝑠3]@2        :=     r[𝑥]@3
message sends, public broadcast, and client outputs.
                                                                              This scheme guarantees that messages are viewed as random noise
   Deﬁnition 2.2. Memories 𝜎 are ﬁnite (partial) mappings from                by any observer besides 𝜄 [8]. Next, each client publicly reveals the
variables 𝑥 to values 𝑣 ∈ F𝑝 . The domain of a memory is written              sum of all of its shares, including its local share. This step does
dom(𝜎) and is the ﬁnite set of variables on which the memory is de-           reveal information about secrets– note in particular that r[local]
ﬁned. We write 𝜎{𝑥 ↦→ 𝑣 } for 𝑥 ∉ dom(𝜎) to denote the memory 𝜎 ′             is reused and is no longer a one-time-pad:
such that 𝜎 ′ (𝑥) = 𝑣 and otherwise 𝜎 ′ (𝑦) = 𝜎 (𝑦) for all 𝑦 ∈ dom(𝜎).
We write 𝜎 ⊆ 𝜎 ′ iﬀ dom(𝜎) ⊆ dom(𝜎 ′ ) and 𝜎 (𝑥) = 𝜎 ′ (𝑥) for                            p[1]     :=        (r[local] + m[𝑠2] + m[𝑠3])@1
all 𝑥 ∈ dom(𝜎). Given any 𝜎 and 𝜎 ′ with 𝜎 (𝑥) = 𝜎 ′ (𝑥) for all                          p[2]     :=        (m[𝑠1] + r[local] + m[𝑠3])@2
𝑥 ∈ dom(𝜎) ∩ dom(𝜎 ′ ), we write 𝜎 ⊎ 𝜎 ′ to denote the memory                             p[3]     :=        (m[𝑠1] + m[𝑠2] + r[local])@3
with domain 𝑋 = dom(𝜎) ∪ dom(𝜎 ′ ) such that:                                 Finally, each client outputs the sum of each sum of shares, yielding
                                                                              the sum of secrets. The protocol is correct because the outputs are
                                  (
                                    𝜎 (𝑥) if 𝑥 ∈ dom(𝜎)
          ∀𝑥 ∈ 𝑋 .(𝜎 ⊎ 𝜎 ′ )(𝑥) = ′                                           all the true sum of secrets, and it is secure because no more infor-
                                    𝜎 (𝑥) otherwise
                                                                              mation about the secrets other than that revealed by their sum is
   In our subsequent presentation we will often want to consider              exposed.
arbitrary memories that range over particular variables and to re-
                                                                                             out@1       :=     (p[1] + p[2] + p[3])@1
strict memories to particular subsets of their domain:
                                                                                             out@2       :=     (p[1] + p[2] + p[3])@2
   Deﬁnition 2.3. Given a set of variables 𝑋 and memory 𝜎, we                                out@3       :=     (p[1] + p[2] + p[3])@3
write 𝜎𝑋 to denote the memory with dom(𝜎𝑋 ) = 𝑋 and 𝜎𝑋 (𝑥) =
𝜎 (𝑥) for all 𝑥 ∈ 𝑋 . We deﬁne mems(𝑋 ) as the set of all memories            3 SECURITY MODEL
with domain 𝑋 :                                                               MPC protocols are intended to implement some ideal functionality
                      mems(𝑋 ) , {𝜎 | dom(𝜎) = 𝑋 }                            F with per-client outputs. In the Overture setting, Given a protocol
                                                                              𝜋 that implements F , with iovars(𝜋) = 𝑆 ∪ 𝑀 ∪ 𝑃 ∪ 𝑂, the domain
   So for example, given a protocol 𝜋, the set of all random tapes            of F is mems(𝑆) and its range is mems(𝑂). Real/ideal security in
for 𝜋 is mems(rands(𝜋)), and the memory 𝜎secrets (𝜋 ) is 𝜎 restricted         the MPC setting means that, given 𝜎 ∈ mems(𝑆), a secure proto-
to the secrets in 𝜋.                                                          col 𝜋 does not reveal any more information about honest secrets
   Given a variable-free expression 𝜀, we write J𝜀K to denote the             𝜎𝐻 to parties in 𝐶 beyond what is implicitly declassiﬁed by F (𝜎).
standard interpretation of 𝜀 in the arithmetic ﬁeld F𝑝 . With the             Security comes in passive and malicious ﬂavors, wherein the adver-
introduction of variables to expressions, we need to interpret vari-          sary either follows the rules or not, respectively. Characterization
ables with respect to a speciﬁc memory, and all variables used in             of both real world protocol execution and simulation is deﬁned
an expression must belong to a speciﬁed client. Thus, we denote in-           probabilistically. Following previous work [8] we use probability
terpretation of expressions 𝜀 computed on a client 𝜄 as J𝜎, 𝜀K𝜄 . This        mass functions to express joint dependencies between input and
interpretation is deﬁned in Figure 2. The small-step reduction re-            output variables, as a metric of information leakage.
lation →
       − is then deﬁned in Figure 2 to evaluate commands. Reduc-
tion is a relation on conﬁgurations (𝜎, 𝜋) where all three command            3.1 Probability Mass Functions
forms- message send, broadcast, and output- are implemented as
updates to the memory 𝜎. We write →     − ∗ to denote the reﬂexive,           We deﬁne discrete joint probability mass functions (pmfs) in a stan-
transitive closure of →.
                       −                                                      dard manner but develop some notations that are useful for our
                                                                              presentation. Firstly, whereas distributions typically map realiza-
2.3     Example: Passive Secure Addition                                      tions of random variables to values in [0..1], for convenience and
                                                                              following [8] we use memories to represent realizations, so for ex-
Shamir addition leverages homomorphic properties of addition in
                                                                              ample given a pmf P over variables {s[𝑥]@1, m[𝑦]@2} we write
arithmetic ﬁelds to implement secret addition. If a ﬁeld value 𝑣 1 is
                                                                              P ({s[𝑥]@1 ↦→ 0, m[𝑦]@2 ↦→ 1}) to denote the (joint) probability
uniformly random, then 𝑣 1 −𝑣 2 is an encryption of 𝑣 2 where 𝑣 1 is an
                                                                              that s[𝑥]@1 = 0 ∧ m[𝑦]@2 = 1. Recall from Section 2.2 that ⊎ de-
information theoretically secure one-time-pad, which is exploited
                                                                              notes the combination of memories, so for example {s[𝑥]@1 ↦→
for secret sharing, noting that 𝑣 2 can be reconstructed by summing
                                                                              0} ⊎ {m[𝑦]@2 ↦→ 1} = {s[𝑥]@1 ↦→ 0, m[𝑦]@2 ↦→ 1}.
𝑣 1 and 𝑣 3 , 𝑣 1 − 𝑣 2 .
    In Overture, to privately sum secret values s[𝜄], each client 𝜄 in           Deﬁnition 3.1. A probability mass function P is a function map-
the federation {1, 2, 3} samples a value r[local] that can be used            ping memories in mems(𝑋 ) for given variables 𝑋 to values in R
                                                                          4
Language-Based Security for Low-Level MPC                                                                   PPDP ’24, September 10-11, 2024, Milano, Italy


such that:                   Õ                                                3.3 Honest and Corrupt Views
                                        P (𝜎) = 1                             Information about honest secrets can be revealed to corrupt clients
                         𝜎 ∈mems (𝑋 )                                         through messages sent from honest to corrupt clients, and through
   Now, we can deﬁne a notion of marginal and conditional dis-                publicly broadcast information from honest clients. Dually, corrupt
tributions as follows, which are standard for discrete probability            clients can impact protocol integrity through the messages sent
mass functions.                                                               from corrupt to honest clients, and through publicly broadcast in-
   Deﬁnition 3.2. Given P with dom(P) = mems(𝑋 2 ), the marginal              formation from corrupt clients. We call the former corrupt views,
distribution of variables 𝑋 1 ⊆ 𝑋 2 in P is denoted P𝑋1 and deﬁned            and the latter honest views. Generally we let 𝑉 range over sets of
as follows:                                                                   views.
                                             Õ
     ∀𝜎 ∈ mems(𝑋 1 ) . P𝑋1 (𝜎) ,                      P (𝜎 ⊎ 𝜎 ′ )               Deﬁnition 3.6 (Corrupt and Honest Views). We let 𝑉 range over
                                            𝜎 ′ ∈mems (𝑋2 −𝑋1 )               views which are sets of messages and reveals. Given a program 𝜋
   Deﬁnition 3.3. Given P, the conditional distribution of 𝑋 1 given          with iovars(𝜋) = 𝑆 ∪ 𝑀 ∪ 𝑃 ∪ 𝑂, deﬁne views(𝜋) , 𝑀 ∪ 𝑃, and
𝑋 2 where 𝑋 1 ∪ 𝑋 2 ⊆ dom(P) and 𝑋 1 ∩ 𝑋 2 = ∅ is denoted P (𝑋1 |𝑋2 )         deﬁne 𝑉𝐻 ⊲𝐶 as the messages and reveals in 𝑉 = 𝑀 ∪ 𝑃 sent from
and deﬁned as follows:                                                        honest to corrupt parties, called corrupt views:
                                         (
                                           0 if P𝑋2 (𝜎𝑋2 ) = 0                 𝑉𝐻 ⊲𝐶    ,    { p[𝑤] | p[𝑤] := 𝜀@𝜄 ∈ 𝜋 ∧ 𝜄 ∈ 𝐻 } ∪
∀𝜎 ∈ mems(𝑋 1 ∪𝑋 2 ) . P (𝑋1 |𝑋2 ) (𝜎) ,
                                           P𝑋1 ∪𝑋2 (𝜎)/P𝑋2 (𝜎𝑋2 ) o.w.                       { m[𝑤]@𝜄 | m[𝑤]@𝜄 := 𝜀@𝜄 ′ ∈ 𝜋 ∧ 𝜄 ∈ 𝐶 ∧ 𝜄 ′ ∈ 𝐻 }
   We also deﬁne some convenient syntactic sugarings. The ﬁrst                and similarly deﬁne 𝑉𝐶⊲𝐻 as the subset of 𝑉 sent from corrupt to
will allow us to compare marginal distributions under diﬀerent re-            honest parties, called honest views:
alization conditions (as in, e.g., Deﬁnition 4.1), the others are stan-
dard.                                                                          𝑉𝐶⊲𝐻     ,    { p[𝑤] | p[𝑤] := 𝜀@𝜄 ∈ 𝜋 ∧ 𝜄 ∈ 𝐶 } ∪
                                                                                             { m[𝑤]@𝜄 | m[𝑤]@𝜄 := 𝜀@𝜄 ′ ∈ 𝜋 ∧ 𝜄 ∈ 𝐻 ∧ 𝜄 ′ ∈ 𝐶 }
  Deﬁnition 3.4. Given P, for all 𝜎1 ∈ mems(𝑋 1 ) and 𝜎2 ∈ mems(𝑋 2 )
deﬁne:
                                                                              3.4 Passive Correctness and Security
  (1) P (𝑋1 |𝜎2 ) (𝜎1 ) , P (𝑋1 |𝑋2 ) (𝜎1 ⊎ 𝜎2 )
  (2) P (𝜎1 ) , P𝑋1 (𝜎1 )                                                     In the passive setting we assume that 𝐻 and 𝐶 follow the rules of
  (3) P (𝜎1 |𝜎2 ) , P (𝑋1 |𝑋2 ) (𝜎1 ⊎ 𝜎2 )                                    protocols and share messages as expected. A ﬁrst consideration is
                                                                              whether a given protocol is correct with respect to an ideal func-
3.2    Basic Distribution of a Protocol                                       tionality.
Now we can deﬁne the probability distribution of a program 𝜋, that              Deﬁnition 3.7 (Passive Correctness). We say that a protocol 𝜋 is
we denote BD(𝜋). Since Overture is deterministic the results of any           passive correct for a functionality F iﬀ for all 𝜎 ∈ mems(secrets(𝜋))
run are determined by the input values together with the random               we have BD(𝜋)(F (𝜎) | 𝜎) = 1.
tape. And since we constrain programs to not overwrite views, we
are assured that ﬁnal memories contain both a complete record                    In the passive setting the simulator must construct a probabilis-
of all initial secrets as well as views resulting from communicated           tic algorithm Sim, aka a simulation, that is parameterized by cor-
information.                                                                  rupt inputs and the output of an ideal functionality, and that re-
   Our semantics require that random tapes contain values for all             turns a reconstruction of corrupt views that is probabilistically in-
program values r[𝑤]@𝜄 sampled from a uniform distribution over                distinguishable from the corrupt views in the real world protocol
F𝑝 . Input memories also contain input secret values and possibly             execution.
other initial view elements as a result of pre-processing, e.g., Beaver
triples for eﬃcient multiplication, and/or MACed share distribu-                 Deﬁnition 3.8. Given 𝜎, and 𝑣,we write Pr(Sim(𝜎, 𝑣) = 𝜎 ′ ) to
                                                                              denote the probability that Sim(𝜎, 𝑣) returns corrupt views 𝜎 ′ as
tions as in BDOZ/SPDZ [19, 35]. We deﬁne runs(𝜋) as the set of ﬁ-
                                                                              a result. We write D(Sim(𝜎, 𝑣)) to denote the distribution of cor-
nal memories resulting from execution of 𝜋 given any initial mem-
ory, and treat all elements of runs(𝜋) as equally likely. This estab-         rupt views reconstructed by the simulation, where for all 𝜎 ′ ∈
                                                                              mems(𝑉 ):
lishes the basic program distribution that can be marginalized and
conditioned to quantify input/output information dependencies.                              D(Sim(𝜎, 𝑣))(𝜎 ′ ) , Pr(Sim(𝜎, 𝑣) = 𝜎 ′ )
  Deﬁnition 3.5. Given 𝜋 with secrets(𝜋) = 𝑆 and rands(𝜋) = 𝑅
and pre-processing predicate preproc on memories, deﬁne:                         Then we can deﬁne passive security in the real/ideal model as
                                                                              follows.
                          runs(𝜋) ,
                                                      − ∗ (𝜎, ∅)}
 {𝜎 | ∃𝜎1 ∈ mems(𝑅).∃𝜎2 .preproc(𝜎2 ) ∧ (𝜎1 ⊎ 𝜎2 , 𝜋) →                          Deﬁnition 3.9 (Passive Security). Assume given a program 𝜋 that
By default, preproc(𝜎) ⇐⇒ dom(𝜎) = 𝑆, i.e., the initial memory                correctly implements an ideal functionality F , with views(𝜋) = 𝑉 .
contains all input secrets in a uniform marginal distribution. Then           Then 𝜋 is passive secure in the simulator model iﬀ there exists a
the basic distribution of 𝜋, written BD(𝜋), is deﬁned such that for           simulation Sim such that for all partitions of the federation into
all 𝜎 ∈ mems(iovars(𝜋) ∪ 𝑅):                                                  honest and corrupt sets 𝐻 and 𝐶 and for all 𝜎 ∈ mems(secrets(𝜋)):

        BD(𝜋)(𝜎) = 1/|runs(𝜋)| if 𝜎 ∈ runs(𝜋), otherwise 0                                   D(Sim(𝜎𝐶 , F (𝜎))) = BD(𝜋) (𝑉𝐻 ⊲𝐶 |𝜎 )
                                                                          5
PPDP ’24, September 10-11, 2024, Milano, Italy                                                                              Christian Skalka and Joseph P. Near


3.5     Malicious Security                                                              Deﬁnition 3.12 (Malicious Simulation). Given a protocol 𝜋 with
In the malicious model we assume that corrupt clients are in thrall                  iovars(𝜋) = 𝑆 ∪ 𝑉 ∪ 𝑂, honest and corrupt clients 𝐻 and 𝐶, adver-
to an adversary A who does not necessarily follow the rules of the                   sary A, and honest inputs 𝜎 ∈ mems(𝑆𝐻 ), the malicious simulation
protocol. We model this by positing a rewrite A function which is                    Sim(𝜎) has three phases:
given a corrupt memory 𝜎𝐶 and expression 𝜀, and returns a rewrit-                       (1) In the ﬁrst phase Sim1 , A gives the simulator some 𝜎 ′ ∈
ten expression that can be interpreted to yield a corrupt input. We                         mems(𝑆𝐶 ), and the simulator consults an oracle to compute
deﬁne the evaluation relation that incorporates the adversary in                            F (𝜎 ⊎ 𝜎 ′ ) ∈ mems(𝑂).
Figure 3.                                                                               (2) In the second phase Sim2 , the simulator is given the corrupt
                                                                                            outputs F (𝜎 ⊎ 𝜎 ′ )𝐶 , which are again given to A, who de-
                                                                                            cides either to abort or not. If so, then the simulator is given
 (𝜎, 𝑥 := 𝜀@𝜄; 𝜋)     →
                      −A        (𝜎{𝑥 ↦→ J𝜎, 𝜀K𝜄 }, 𝜋)                  𝜄∈𝐻
                                                                                            𝜎out , {out@𝜄 ↦→ ⊥ | 𝜄 ∈ 𝐻 } and arbitrary internal state 𝜍.
 (𝜎, 𝑥 := 𝜀@𝜄; 𝜋)     →
                      −A        (𝜎{𝑥 ↦→ Jrewrite A (𝜎𝐶 , 𝜀)K𝜄 }, 𝜋)    𝜄 ∈𝐶
                                                                                            Otherwise the simulator is given 𝜎out , F (𝜎 ⊎ 𝜎 ′ )𝐻 and 𝜍.
                                                                                        (3) In the third phase Sim3 , given 𝜎out and 𝜍, the simulator ﬁ-
 (𝜎, assert(𝜙 (𝜀))@𝜄; 𝜋)         →
                                 −A       (𝜎, 𝜋)     if 𝜙 (J𝜎, 𝜀K𝜄 ) or 𝜄 ∈ 𝐶
                                                                                            nally outputs 𝜎out ⊎𝜎views for some calculated 𝜎views ∈ mems(𝑉𝐻 ⊲𝐶 ).
 (𝜎, assert(𝜙 (𝜀))@𝜄; 𝜋)         →
                                 −A       (𝜎, ∅)           if ¬𝜙 (𝜎, J𝜎, 𝜀K𝜄 )
                                                                                        Deﬁnition 3.13 (Malicious Security). We write D(Sim(𝜎)) to de-
 Figure 3: Adversarial semantics, and semantics of assert.                           note the distribution of honest outputs and corrupt views recon-
                                                                                     structed by the malicious simulation, where for all 𝜎 ′ :
   A key technical distinction of the malicious setting is that it typ-                             D(Sim(𝜎))(𝜎 ′ ) , Pr(Sim(𝜎) = 𝜎 ′ )
ically incorporates “abort”. Honest parties implement strategies to
detect rule-breaking– aka cheating– by using, e.g., message authen-                  Then a protocol 𝜋 with iovars(𝜋) = 𝑆 ∪ 𝑉 ∪ 𝑂 is malicious secure
tication codes with semi-homomorphic properties as in BDOZ/SPDZ                      iﬀ for all 𝐻 , 𝐶, A, and 𝜎 ∈ mems(𝑆𝐻 ):
[35]. If cheating is detected, the protocol is aborted. To model this,
                                                                                                    D(Sim(𝜎)) = BD(𝜋, A) (𝑉𝐻 ⊲𝐶 ∪𝑂𝐻 |𝜎 )
we extend Overture with an assert command and extend the range
of memories with ⊥. Note that the adversary is free to ignore their
own assertions.                                                                      4 SECURITY HYPERPROPERTIES
                                                                                     In this Section we formulate probabilistic versions of well-studied
   Deﬁnition 3.10. We add assertions of the form assert(𝜙 (𝜀))@𝜄                     hyperproperties of conﬁdentiality and integrity, including nonin-
to the command syntax of Overture, where 𝜙 is a decidable predi-                     terference, gradual release, declassiﬁcation, and robust declassiﬁca-
cate on F𝑝 and with operational semantics given in Figure 3. We                      tion. We follow nomenclature developed in previous work on char-
also extend the range of memories 𝜎 to F𝑝 ∪ {⊥}.                                     acterizing declassiﬁcation policies in deterministic settings [40],
   It is necessary to add ⊥ to the range of memories since the pos-                  but adapt them to our probabilistic one.
sibility of abort needs to be reﬂected in adversarial runs of a proto-
col. We can deﬁne runs A (𝜋) as the “preﬁx” memories that result                     4.1 Conditional Noninterference
from possibly-aborting protocols, but we also need to “pad out”                      Since MPC protocols release some information about secrets through
the memories of partial runs with ⊥, as we deﬁne in runs A,⊥ (𝜋),                    outputs of F , they do not enjoy strict noninterference. As discussed
to properly reﬂect the contents of views and outputs even in case                    in Section 2, public reveals and protocol outputs are fundamen-
of abort.                                                                            tally forms of declassiﬁcation. But consistent with other work [22],
                                                                                     we can formulate a version of probabilistic noninterference condi-
   Deﬁnition 3.11. Given program 𝜋 with iovars(𝜋) = 𝑆 ∪𝑉 ∪𝑂 and
rands(𝜋) = 𝑅, and any assumed pre-processing predicate preproc                       tioned on output that is sound for passive security.
on memories, deﬁne:                                                                     Deﬁnition 4.1 (Noninterference modulo output). We say that a
                         runs A (𝜋) ,                                                program 𝜋 with iovars(𝜋) = 𝑆 ∪ 𝑉 ∪ 𝑂 satisﬁes noninterference
                                                      − ∗A (𝜎, ∅)}
 {𝜎 | ∃𝜎1 ∈ mems(𝑅).∃𝜎2 .preproc(𝜎2 ) ∧ (𝜎1 ⊎ 𝜎2 , 𝜋) →                              modulo output iﬀ for all 𝐻 and 𝐶 and 𝜎1 ∈ mems(𝑆𝐶 ∪ 𝑂) and
                                                                                     𝜎2 ∈ mems(𝑉𝐻 ⊲𝐶 ) we have:
where by default, preproc(𝜎) ⇐⇒ dom(𝜎) = 𝑆, and also deﬁne
the following which pads out undeﬁned views and outputs with ⊥:                                      BD(𝜋) (𝑆𝐻 |𝜎1 ) = BD(𝜋) (𝑆𝐻 |𝜎1 ⊎𝜎2 )
      runs A,⊥ (𝜋) ,
                                                                                        This conditional noninterference property implies that corrupt
           {𝜎{𝑥 1 ↦→ ⊥, . . . , 𝑥𝑛 ↦→ ⊥} |
                                                                                     views give the adversary no better chance of guessing honest se-
            𝜎 ∈ runs A (𝜋) ∧ {𝑥 1 , . . . , 𝑥𝑛 } = (𝑉 ∪ 𝑂) − dom(𝜎)}
                                                                                     crets than just the output and corrupt inputs do. So the simulator
Then the A distribution of 𝜋, written BD(𝜋, A), is deﬁned such                       can just arbitrarily pick any honest secrets that could have pro-
that for all 𝜎 ∈ mems(iovars(𝜋) ∪ 𝑅):                                                duced the given outputs and run the protocol in simulation to re-
                                                                                     construct real world corrupt views. This requires that the simulator
 BD(𝜋, A)(𝜎) = 1/|runs A,⊥ (𝜋)| if 𝜎 ∈ runs A,⊥ (𝜋), otherwise 0
                                                                                     can tractably “pre-image” a given output of a functionality F , to
  Given this preamble, we can deﬁne malicious simulation and                         determine the inputs that could have produced it. This equivalence
malicious security in a standard manner [19], as follows.                            class is called a kernel in recent work [24].
                                                                                 6
Language-Based Security for Low-Level MPC                                                                   PPDP ’24, September 10-11, 2024, Milano, Italy


   Deﬁnition 4.2. Given a functionality F and outputs 𝜎out , their               The following result establishes that integrity implies malicious
kernel, denoted F −1 (𝜎out ) is {𝜎 | F (𝜎) = 𝜎out }. We say that F is         security for protocols that are passive secure (which also subsumes
pre-imageable iﬀ F −1 (𝜎out ) for all 𝜎out can be computed tractably.         correctness).
   A soundness result for passive security can then be given as                  Theorem 4.8. If a protocol is passive secure and has integrity,
follows. It is essentially the same as “perfect passive NI security”          then it is malicious secure.
explored in previous work [22].
                                                                                 Proof. Let 𝜋 be some protocol with passive security and in-
   Theorem 4.3. Assume given pre-imageable F and a protocol 𝜋
that correctly implements F . If 𝜋 satisﬁes noninterference modulo            tegrity where iovars(𝜋) = 𝑆 ∪𝑉 ∪ 𝑂, and let A be some adversary.
                                                                              Suppose 𝜎 ∈ runs A (𝜋). As integrity requires, and as Lemma 4.7
output then 𝜋 is passive secure.
                                                                              demonstrates with respect to outputs, the most the adversary can
4.2    Gradual Release                                                        do in the presence of integrity is to elicit the same responses from
                                                                              the honest parties– via the strategy 𝜎𝑉𝐶⊲𝐻 – as are elicited from
Probabilistic noninterference is related to perfect secrecy and is
                                                                              some passive run of the protocol using some 𝜎 ′ ∈ mems(𝑆) where
preserved by components of cryptographic protocols generally. It                ′ = 𝜎 , and perhaps to force an abort after some number of
                                                                              𝜎𝐻       𝑆𝐻
can be expressed using probabilistic independence, aka separation,
                                                                              message exchanges.
[8, 17], and we adopt the following notation to express indepen-
                                                                                 Therefore, in simulation, A can provide the simulator with some
dence:
                                                                              𝜎𝐶′ in Sim1 which its strategy is “impersonating”, allowing F (𝜎 ′ )
  Deﬁnition 4.4. We write P ⊢ 𝑋 1 ∗𝑋 2 iﬀ for all 𝜎 ∈ mems(𝑋 1 ∪𝑋 2 )         to be communicated to A in Sim2 who can then decide whether or
we have P𝑋1 ∪𝑋2 (𝜎) = P (𝜎𝑋1 ) ∗ P (𝜎𝑋2 )                                     not to abort. In the case of abort, the subset of 𝑉𝐻 ⊲𝐶 to be deﬁned
   In practice, MPC protocols typically satisfy a gradual release             can be communicated to Sim3 , along with F (𝜎 ′ ), via Σ. In Sim3 ,
property [40], where messages exchanged remain probabilistically              the simulator can then run 𝜋 in simulation with inputs 𝜎𝐶′ and ar-
separable from secrets, with only declassiﬁcation events (reveals             bitrary 𝜎 ′′ ∈ mems(𝑆𝐻 ) such that 𝜎𝐶′ ⊎ 𝜎 ′′ ∈ F −1 (F (𝜎 ′ )). The
and outputs) releasing information about honest secrets. A key dif-           assumption of passive security of 𝜋 implies the result.            ⊔
                                                                                                                                                 ⊓
ference is that while these declassiﬁcation events essentially deﬁne
                                                                                  The hyperproperty of robust declassiﬁcation [46] similarly com-
the policy in gradual release, the ideal functionality sets the release
                                                                              bines a conﬁdentiality property with integrity to establish that ma-
policy for MPC passive security, so its necessary to show that de-
                                                                              licious actors cannot declassify more information than is intended
classiﬁcation events respect these bounds.
                                                                              by policy. But in this prior work, this policy is established by the
  Deﬁnition 4.5. Given 𝐻, 𝐶, a protocol 𝜋 with iovars(𝜋) = 𝑆 ∪                declassiﬁcations themselves, as in gradual release. Thus, we can
𝑀 ∪ 𝑃 ∪ 𝑂 satisﬁes gradual release iﬀ BD(𝜋) ⊢ 𝑀𝐶 ∗ 𝑆𝐻 .                       deﬁne a robust declassiﬁcation property as follows.

4.3    Integrity and Robust Declassiﬁcation                                     Deﬁnition 4.9 (Robust Declassiﬁcation). A protocol satisﬁes ro-
Integrity is an important hyperproperty in security models that ad-           bust declassiﬁcation iﬀ it has integrity and satisﬁes gradual release.
mit malicious adversaries. Consistent with formulations in deter-                 However, it is important to note that gradual release, and hence
ministic settings, we have already deﬁned protocol conﬁdentiality             robust declassiﬁcation, are not suﬃcient to establish passive or ma-
as the preservation of low equivalence (of secrets and views), and            licious simulator security, where the declassiﬁcation policy is es-
now we deﬁne protocol integrity as the preservation of high equiv-            tablished by the ideal functionality F .
alence (of secrets and views). Intuitively, this property says that
any adversarial strategy either “mimics” a passive strategy with                  Theorem 4.10. Robust declassiﬁcation does not imply malicious
some choice of inputs or causes an abort.                                     security, but passive security with robust declassiﬁcation implies ma-
                                                                              licious security.
   Deﬁnition 4.6 (Integrity). We say that a protocol 𝜋 with iovars(𝜋) =
𝑆 ∪𝑉 ∪𝑂 has integrity iﬀ for all 𝐻 , 𝐶, and A, if 𝜎 ∈ runs A (𝜋) then         5 AUTOMATED VERIFICATION IN F2
there exists 𝜎 ′ ∈ mems(𝑆) with 𝜎𝑆𝐻 = 𝜎𝑆′ and:
                                                  𝐻                           In the binary ﬁeld F2 , a brute force strategy for computing BD(𝜋)
               BD(𝜋, A) (𝑋 |𝜎𝑆 ∪𝑉           ) = BD(𝜋) (𝑋 |𝜎 ′ )               for any 𝜋 is to directly compute runs(𝜋). By querying BD(𝜋) we
                                𝐻   𝐶⊲𝐻

where 𝑋 , (𝑉𝐻 ⊲𝐶 ∪ 𝑂 𝐻 ) ∩ dom(𝜎).                                            can verify any of the hyperproperties discussed previously, or other
                                                                              properties such as perfect secrecy [8]. A basic method to do this
   A ﬁrst important observation is that integrity preserves proto-            is to calculate a truth table for the given protocol. Since runs(𝜋)
col correctness for honest outputs, except for the possibility of             is exponential in the size of secrets(𝜋) ∪ rands(𝜋), this strategy
abort.                                                                        is feasible only for smaller protocols. However, to support some
   Lemma 4.7. If a protocol 𝜋 with iovars(𝜋) = 𝑆 ∪ 𝑉 ∪ 𝑂 is passive           scaling we can eﬃciently convert protocols in the passive setting
correct for F and has integrity, then for all 𝐻 , 𝐶, A, 𝜎1 ∈ mems(𝑆𝐻 ),       (without assert) to stratiﬁed Datalog programs, and then extract
out@𝜄 ∈ (𝑂 𝐻 ), and 𝜈 ∈ F𝑝 , if:                                              runs(𝜋) by calculating Least Herbrand models by parallelization
                  BD(𝜋, A)({out@𝜄 ↦→ 𝜈 } | 𝜎1 ) > 0                           and/or other HPC acceleration techniques for logic programs [7].
                                                                              The rewriting we describe here is to Datalog with negation, with
then exists 𝜎2 ∈ mems(𝑆𝐶 ) such that:                                         a negation-as-failure model, though we can also use techniques in
                        F (𝜎1 ⊎ 𝜎2 )(out@𝜄) = 𝜈                               [41] to eliminate negation from resulting programs.
                                                                          7
PPDP ’24, September 10-11, 2024, Milano, Italy                                                                                          Christian Skalka and Joseph P. Near



            models Σ 1 𝜄       =       Σ                                                     ... and so on. Then, to convert a protocol 𝜋 to a Datalog we ﬁrst
                                                                                             deﬁne the function bodies that applies models locally to each com-
            models Σ 0 𝜄       =       ∅
                                                                                             mand in 𝜋, obtaining the subset of memories that result in a vari-
        models Σ m[𝑤] 𝜄        =       {𝜎 ∈ Σ | 𝜎 (m[𝑤]@𝜄 ) = 1}
                                                                                             able assignment of 1.
        models Σ r[𝑤] 𝜄        =       {𝜎 ∈ Σ | 𝜎 (r[𝑤]@𝜄 ) = 1}
        models Σ s[𝑤] 𝜄        =       {𝜎 ∈ Σ | 𝜎 (s[𝑤]@𝜄 ) = 1}                                Deﬁnition 5.3. Deﬁne:
        models Σ p[𝑤] 𝜄        =       {𝜎 ∈ Σ | 𝜎 (p[𝑤]) = 1}
                                                                                                    bodies(𝑥 := 𝜀@𝜄) , (𝑥, (models (mems(vars 𝜀 𝜄)) 𝜀 𝜄))
      models Σ (not 𝜀 ) 𝜄      =       Σ − (models Σ 𝜀 𝜄 )
 models Σ (𝜀 1 and 𝜀 2 ) 𝜄     =       (models Σ 𝜀 1 𝜄 ) ∩ (models Σ 𝜀 2 𝜄 )                    The mapping of bodies across a program 𝜋– i.e., (map bodies 𝜋)–
  models Σ (𝜀 1 or 𝜀 2 ) 𝜄     =       (models Σ 𝜀 1 𝜄 ) ∪ (models Σ 𝜀 2 𝜄 )                 essentially deﬁnes the logic program, modulo some syntactic con-
 models Σ (𝜀 1 xor 𝜀 2 ) 𝜄     =       ( (models Σ 𝜀 1 𝜄 ) ∩ (Σ − models Σ 𝜀 2 𝜄 ) ) ∪       version. We can accomplish the latter as follows, where datalog(𝜋)
                                       ( (Σ − models Σ 𝜀 1 𝜄 ) ∩ (models Σ 𝜀 2 𝜄 ) )
                                                                                             deﬁnes the full conversion.

                                                                                                Deﬁnition 5.4. We deﬁne the conversion from memories to lit-
        Figure 4: Filtering solutions to expressions in F2 .                                 erals and clause bodies as follows:
                                                                                                            ⌊𝑥 ↦→ 1⌋ , 𝑥                 ⌊𝑥 ↦→ 0⌋ , ¬𝑥
5.1      Computing a Truth Table                                                                ⌊{𝑥 1 ↦→ 𝛽 1, . . . , 𝑥𝑛 ↦→ 𝛽𝑛 }⌋ , ⌊𝑥 1 ↦→ 𝛽 1 ⌋ ∧ · · · ∧ ⌊𝑥𝑛 ↦→ 𝛽𝑛 ⌋
Letting Σ denote sets of memories, in Figure 4 we deﬁne the algo-
rithm models Σ 𝜀 𝜄 which ﬁlters a given Σ to obtain the subset whose                         Given pairs (𝑥, Σ) in the range of bodies, we deﬁne the conversion
elements satisfy 𝜀. In this Figure and elsewhere we use logical con-                         to clauses as clauses(𝑥, {𝜎1, ..., 𝜎𝑛 }) , 𝑥 ← ⌊𝜎1 ⌋ ∨ · · · ∨ 𝑥 ← ⌊𝜎𝑛 ⌋.
nectives as ﬁeld operations (and and xor for ∗ and + respectively)                           The Overture-to-Datalog conversion is then deﬁned as:
in F2 and add not and or as trivial but convenient extensions. The
correctness of this operation is characterized as follows.                                                datalog(𝜋) , map clauses (map bodies 𝜋)

   Lemma 5.1. (models Σ 𝜀 𝜄) = {𝜎 ∈ Σ | J𝜎, 𝜀K𝜄 = 1}.                                           In addition to converting view deﬁnitions to logic clauses, we
                                                                                             also need to convert secrets and random tapes. Since we assume
   We immediately note that runs(𝜋) can be obtained by a left-                               given values for these in an arbitrary run of the program, we can
folding of models across 𝜋.                                                                  capture these as a particular fact base.
   Lemma 5.2. Given 𝜋 where iovars(𝜋) = 𝑆 ∪𝑉 ∪𝑂 and rands(𝜋) =                                  Deﬁnition 5.5. Given 𝜎, let {𝑥 1, . . . , 𝑥𝑛 } = {𝑥 ∈ dom(𝜎) | 𝜎 (𝑥) =
𝑅. Deﬁne:                                                                                    1}. Then deﬁne facts(𝜎) , 𝑥 1 ←, . . . , 𝑥𝑛 ←.
                                           let Σ′ = models Σ 𝜀 𝜄 in
                                                                                               The following result ties these pieces together and establishes
         𝑡𝑡 Σ (𝑥 := 𝜀@𝜄)           ,         {𝜎{𝑥 ↦→ 1} | 𝜎 ∈ Σ′ } ∪
                                                                                             correctness of this approach.
                                             {𝜎{𝑥 ↦→ 0} | 𝜎 ∈ Σ − Σ′ }
Then assuming default preprocessing, foldl 𝑡𝑡 mems(𝑆 ∪ 𝑅) 𝜋 =                                   Lemma 5.6. For all 𝜋, datalog(𝜋) is a normal, stratiﬁed program
runs(𝜋).                                                                                     [7], and 𝜎 is the unique Least Herbrand Model of:

   However, this method does not take advantage of paralleliza-                                             (facts(𝜎secrets (𝜋 )∪rands (𝜋 ) ), datalog(𝜋))
tion, in that elements of runs(𝜋) can be calculated independently.
                                                                                             iﬀ 𝜎 ∈ runs(𝜋).
5.2      Conversion to Stratiﬁed Datalog                                                        Finally, to compute runs(𝜋), and thus BD(𝜋), we compute the
We deﬁne the syntax of Datalog as follows. As per standard nomen-                            Least Herbrand Model 𝜎 of (facts(𝜎 ′ ), datalog(𝜋)) for all 𝜎 ′ ∈ mems(secrets(𝜋)∪
clature, atoms are Overture variables 𝑥, literals are atoms or negated                       rands(𝜋)), observing that model computation for distinct fact bases
atoms, and clause bodies are conjunctions of literals. A fact is a                           can be done in parallel.
clause with no body. A Datalog program is a list of clauses.
                                                                                                Verifying Security Properties. We can query correct representa-
               body      ::=       𝑥 | ¬𝑥 | 𝑥 ∧ body | ¬𝑥 ∧ body                             tions of runs(𝜋) by using implementations of conditioning and
              clause     ::=       𝑥 ← body | 𝑥 ←                                            marginalization to automatically verify the passive model hyper-
When translating protocols, we need to extract the variables that                            properties described in Section 4– in particular correctness and
occur in expressions 𝜀 computed by a client 𝜄, written vars 𝜀 𝜄                              noninterference modulo output, which imply passive security. We
where:                                                                                       have used this method to verify security in F2 of Shamir addition
                                                                                             as deﬁned in Section 2.3, and single-gate and and xor circuits with
       vars s[𝑤]𝜄 , {s[𝑤]@𝜄}                      vars m[𝑤]𝜄 , {m[𝑤]@𝜄}
                                                                                             GMW Beaver triples. We have also veriﬁed properties composi-
       vars p[𝑤]𝜄 , {p[𝑤]@𝜄}                      vars r[𝑤]𝜄 , {r[𝑤]@𝜄}                      tional properties of gates themselves that establish circuit invari-
                                                                                             ants that imply passive security in larger circuits. We discuss these
               vars (𝜀 1 xor𝜀 2 ) 𝜄 , (vars 𝜀 1 𝜄) ∪ (vars 𝜀 2 𝜄)                            examples and proof methods in Section 7.
                                                                                         8
Language-Based Security for Low-Level MPC                                                                                                 PPDP ’24, September 10-11, 2024, Milano, Italy


       ℓ ∈ Field, 𝑦 ∈ EVar, 𝑓 ∈ FName                                                                   and Overture commands. The construction of a command has the
              𝑒     ::=     𝜈 | r[𝑒] | s[𝑒] | m[𝑒] | p[𝑒] | 𝑒 binop 𝑒 |                                 side-eﬀect of adding to the residual Overture protocol. Formally,
                            m[𝑒]@𝑒 := 𝑒@𝑒 | p[𝑒] := 𝑒@𝑒 | out@𝑒 := 𝑒@𝑒 |                                we consider a complete metaprogram to include both a codebase
                            assert(𝜙 (𝑒))@𝑒 | 𝑦 | let 𝑦 = 𝑒 in 𝑒 |                                      and a “main” program that uses the codebase.
                            𝑓 (𝑒, . . . , 𝑒) | {ℓ = 𝑒; . . . ; ℓ = 𝑒 } | 𝑒.ℓ | 𝑒; 𝑒
                                                                                                          Deﬁnition 6.1. A codebase C is a list of function declarations. We
        binop       ::=     + | − | ∗ | ++
                                                                                                        write C(𝑓 ) = 𝑦1, . . . , 𝑦𝑛 , 𝑒 iﬀ 𝑓 (𝑦1, . . . , 𝑦𝑛 ){𝑒 } ∈ C. A metaprogram,
             𝜈      ::=     𝑤 | 𝜄 | 𝜀 | {ℓ = 𝜈; . . . ; ℓ = 𝜈 } | ()
                                                                                                        aka metaprotocol is a pair of a codebase and expression C, 𝑒. We
             fn     ::=     𝑓 (𝑦, . . . , 𝑦) {𝑒 }                                                       may omit C if it is clear from context.

                                                                                                           When we consider larger examples, our focus will be on devel-
                                           𝐸 ::=                                                        oping a codebase that can be used to deﬁne arbitrary circuits, i.e.,
    [ ] | 𝐸 binop 𝑒 | 𝜈 binop 𝐸 | r[𝐸] | s[𝐸] | m[𝐸] | p[𝐸] |
                                                                                                        complete and concrete protocols. Since strings and identiﬁers can
    m[𝐸]@𝑒 := 𝑒@𝑒 | m[𝜈]@𝐸 := 𝑒@𝑒 | m[𝜈]@𝜈 := 𝐸@𝑒 | m[𝜈]@𝜈 := 𝜈@𝐸 |
    p[𝐸] := 𝑒@𝑒 | p[𝜈] := 𝐸@𝑒 | p[𝜈] := 𝜈@𝐸 |
                                                                                                        be constructed manually, and expressions can occur inside assign-
    out@𝐸 := 𝑒@𝑒 | out@𝜈 := 𝐸@𝑒 | out@𝜈 := 𝜈@𝐸 |                                                        ments and ﬁeld expression forms, function deﬁnitions can gener-
    assert(𝜙 (𝐸 ))@𝑒 | assert(𝜙 (𝜈 ))@𝐸 |                                                               alize over Overture-level patterns to obtain composable program
    let 𝑦 = 𝐸 in 𝑒 | 𝑓 (𝜈, . . . , 𝜈, 𝐸, 𝑒, . . . , 𝑒) | 𝐸; 𝑒                                           units.
    {ℓ = 𝜈; . . . ; ℓ = 𝜈; ℓ = 𝐸; ℓ = 𝑒; . . . ; ℓ = 𝑒 } | 𝐸.ℓ
                                                                                                        6.2 Semantics
                                                                                                        We deﬁne a small-step evaluation aka reduction relation →   − in Fig-
                          h𝜋, let 𝑦 = 𝜈 in 𝑒i →
                                              − h𝜋, 𝑒 [𝜈/𝑦 ] i                                          ure 5. We write →− ∗ to denote the reﬂexive, transitive closure of →.
                                                                                                                                                                           −
                                                                                                        Reduction is deﬁned on conﬁgurations which are pairs of the form
                                  C (𝑓 ) = 𝑦1 , . . . , 𝑦𝑛 , 𝑒                                          h𝜋, 𝑒i, where 𝜋 is the Overture program accumulated during evalu-
                  h𝜋, 𝑓 (𝜈1 , ..., 𝜈𝑛 ) i →
                                          − h𝜋, 𝑒 [𝜈1 /𝑦1 , . . . , 𝜈𝑛 /𝑦𝑛 ] i                          ation. In this deﬁnition we write 𝑒 [𝜈/𝑦] to denote the substitution
                                                                                                        of 𝜈 for free occurrences of 𝑦 in 𝑒. The rules are mostly standard,
    h𝜋, {. . . ; ℓ = 𝜈; . . .}.ℓ i →
                                   − h𝜋, 𝜈 i            h𝜋, 𝑤1 ++𝑤2 i →
                                                                      − h𝜋, 𝑤1 𝑤2 i                     except when a concrete Overture assignment is encountered it is
                                                                            − h𝜋 ′ , 𝑒 ′ i
                                                                     h𝜋, 𝑒i →                           added to the end of 𝜋.
h𝜋, 𝜈; 𝑒i →
          − h𝜋, 𝑒i                    − h𝜋 ; c, () i
                               h𝜋, ci →                                                                    The rules rely on a deﬁnition of evaluation contexts 𝐸 allowing
                                                                              − h𝜋 ′ , 𝐸 [𝑒 ′ ] i
                                                                 h𝜋, 𝐸 [𝑒 ] i →
                                                                                                        computation within a larger program context, where 𝐸 [𝑒] denotes
                                                                                                        an expression with 𝑒 in the hole [] of 𝐸. The syntax of 𝐸 imposes
Figure 5: Prelude syntax (T), evaluation contexts (M), and op-                                          a left-to-right order of evaluation of subexpressions for all forms.
erational semantics (B).
                                                                                                        7 2-PARTY GMW AND PASSIVE SECURITY
                                                                                                          PROOF TACTICS
6     THE Prelude METALANGUAGE                                                                          As an extended example of our language and security model, and
Practical MPC computations protocols are typically composed of                                          how the automated techniques in Section 5 can serve as tactics
compositional units. Examples include GMW circuits and Yao’s                                            integrated with PSL/Lilac-style proofs, we consider GMW circuits.
Garbled Circuits (YGC), that are composed of so-called garbled                                          The GMW protocol is a garbled binary circuit protocol. We will
gates. Languages such as Fairplay [33] provide gates as units of                                        assume the 2-party version, though it generalizes to 𝑛 parties [21].
abstraction that are “wired” together by the programmer to gener-                                       GMW uses a common technique in MPC, which is to represent
ate a complete circuit.                                                                                 values 𝑣 as distributed shares 𝑣 1 and 𝑣 2 with 𝑣 = 𝑣 1 + 𝑣 2 . This
   The Overture language is low-level and does not include ab-                                          trick maintains secrecy of 𝑣 from both parties, and in GMW it is
stractions for deﬁning composable elements. So in this Section we                                       used to maintain the intermediate values of internal gate outputs
introduce the Prelude language that includes structured data and                                        in circuits. In related literature the notation h𝑥i is used to represent
function deﬁnitions for deﬁning composable protocol elements at                                         the “true” value of 𝑥 and [𝑥] is often used to represent the share of
a higher level of abstraction. The Prelude language is a metalan-                                       given party.
guage, where Overture protocols are the residuum of computation.                                           To capture this convention, which is used in many other pro-
In addition to these declarative beneﬁts of Prelude, component def-                                     tocols, we introduce a new naming convention for “global view”
initions support compositional veriﬁcation of larger protocols as                                       elements hm[𝑤]i, which denote the summed value of m[𝑤]@1 and
we will discuss with examples in Sections 7 and 7.2.                                                    m[𝑤]@2 in a protocol run. This concept integrates program distri-
                                                                                                        butions in the usual manner, as the probability of the outcome of
6.1     Syntax                                                                                          summation of two variables in the distribution.
The syntax of Prelude is deﬁned in Figure 5. It includes a syntax of                                       Deﬁnition 7.1. For all m[𝑤] deﬁne:
function deﬁnitions and records, and values 𝜈 include client ids 𝜄,
identiﬁer strings 𝑤, expressions 𝜀 in ﬁeld F𝑝 , and the unit value ().
                                                                                                                                                    Õ
                                                                                                                               P (hm[𝑤]i = 𝑣) ,            P (𝜎)
Expression forms allow dynamic construction of ﬁeld expressions                                                                                     𝜎 ∈𝐴
                                                                                                    9
PPDP ’24, September 10-11, 2024, Milano, Italy                                                                        Christian Skalka and Joseph P. Near


    encodegmw(in, i1, i2) {                                                 a simple passive secure OT can be deﬁned with the addition of pub-
      m[in]@i2 := (s[in] xor r[in])@i2;
      m[in]@i1 := r[in]@i2;                                                 lic key cryptography as a primitive. But given the diversity of ap-
      m[in]                                                                 proaches to OT, we instead assume that OT is abstract with respect
    }
                                                                            to its implementation, where calls to OT in F2 are of the following
    andtablegmw(b1, b2, r) {                                                form– given a choice bit 𝜀 1 provided by a receiver 𝜄, the sender
      let r11 = r xor (b1 xor true) and (b2 xor true) in                    sends either 𝜀 2 or 𝜀 3 .
      let r10 = r xor (b1 xor true) and (b2 xor false) in
      let r01 = r xor (b1 xor false) and (b2 xor true) in                                             OT(𝜀 1 @𝜄, 𝜀 2 , 𝜀 3 )
      let r00 = r xor (bl xor false) and (b2 xor false) in
      { row1 = r11; row2 = r10; row3 = r01; row4 = r00 }                    Critically, the sender learns nothing about 𝜀 1 and the receiver learns
    }
                                                                            nothing about the unselected value, so we interpret these calls in
    andgmw(z, x, y) {                                                       our implementation in F2 as follows.
      let r = r[z] in
      let table = andtablegmw(x,y,r) in                                               models Σ OT(𝜀 1 @𝜄 1 , 𝜀 2 , 𝜀 3 ) 𝜄 2 =
      m[z]@2 := OT4(x,y,table,2,1);                                                       ((models Σ 𝜀 1 𝜄 1 ) ∩ (models Σ 𝜀 2 𝜄 2 ))∪
      m[z]@1 := r@1;
      m[z]
                                                                                          ((Σ − (models Σ 𝜀 1 𝜄 1 )) ∩ (models Σ 𝜀 3 𝜄 2 )
    }
                                                                            7.1 Correctness Proof with Veriﬁcation Tactics
    xorgmw(z, x, y)
    { m[z]@1 := (x xor y)@1; m[z]@2 := (x xor y)@2; m[z] }                  As discussed above and in related work [22], probabilistic separa-
                                                                            tion conditional on certain variables– e.g., secret inputs or public
    decodegmw(z) {
      p["1"] := z@1; p["2"] := z@2;
                                                                            outputs– is a key mechanism for reasoning about MPC protocol
      out@1 := (p["1"] xor p["2"])@1;                                       security. Following [8], we deﬁne a conditional separation relation
      out@2 := (p["1"] xor p["2"])@2                                        P |𝑋 1 ⊢ 𝑋 2 ∗ 𝑋 3 to mean that 𝑋 2 and 𝑋 3 are independent in P con-
    }
                                                                            ditionally on any assignment of values to 𝑋 1 – i.e., conditionally
                                                                            on any 𝜎 ∈ mems(𝑋 1 ). Another key concept needed especially for
              Figure 6: 2-party GMW circuit library.                        reasoning about circuits is conditional determinism. For example,
                                                                            if h𝑧i is an output of an internal gate, it will deﬁnitely be computed
                                                                            using random variables, however, it should be deterministic under
and also for all 𝜎 ′ ∈ mems(𝑋 ) deﬁne:                                      any set of input secrets 𝑆, since we assume that F is deterministic.
                                       Õ                                    Conditional uniformity is also important, since the gradual release
                P (𝑋 | hm[𝑤]i=𝑣) (𝜎) ,   P (𝑋 |𝜎 ) (𝜎 ′ )                   property of many protocols means that messages appear in a uni-
                                            𝜎 ∈𝐴                            form distribution to the adversary.
where 𝐴 is:                                                                   Deﬁnition 7.2 (Conditioning Properties). Given P and 𝑋 1, 𝑋 2, 𝑋 3 ⊆
{𝜎 ∈ mems({m[𝑤]@1, m[𝑤]@2}) | J𝜎 (m[𝑤]@1) + 𝜎 (m[𝑤]@2)K = 𝑣 }               dom(P), we write:
                                                                               • P |𝑋 1 ⊢ 𝑋 2 ∗𝑋 3 iﬀ for all 𝜎 ′ ∈ mems(𝑋 1 ) and 𝜎 ∈ mems(𝑋 2 ∪
   For full details of the GMW protocol the reader is referred to                𝑋 3 ) we have P (𝜎 |𝜎 ′ ) = P (𝜎𝑋2 |𝜎 ′ ) ∗ P (𝜎𝑋3 |𝜎 ′ ).
[19]. Our implementation library is shown in Figure 6, and includes            • P |𝑋 1 ⊢ D(𝑋 2 ) iﬀ for all 𝜎 ′ ∈ mems(𝑋 1 ) there exists 𝜎 ∈
encoding functions, where input secrets are split into shares, and               mems(𝑋 2 ) such that P (𝜎 |𝜎 ′ ) = 1.
and xor gate functions, and a decoding function. Note that xor                 • P |𝑋 1 ⊢ U(𝑋 2 ) iﬀ for all 𝜎 ′ ∈ mems(𝑋 1 ) and 𝜎 ∈ mems(𝑋 2 )
requires no interaction between parties, while conjunction neces-                we have P (𝜎 |𝜎 ′ ) = 1/𝑝 |𝑋2 | .
sitates 1-of-4 oblivious transfer. The gate computation is done en-
tirely in secret, and the decoding function is where the declassi-             Given these deﬁnitions, we can formulate an invariant for cir-
ﬁcation occurs– both parties reveal their shares of the ﬁnal gate           cuit computation with respect to internal gates as follows. It says
output h𝑧i.                                                                 that the output of any gate is deterministic given inputs 𝑆, and
   For example, the following program uses our GMW library to               conditionally on 𝑆 corrupt views are always in a uniform random
deﬁne a circuit with a single and gate and input secrets s1 and s2          distribution (pure noise), while output hm[𝑧]i remains separable
from client’s 1 and 2 respectively:                                         from corrupt views and both shares of hm[𝑧]i. This last condition
                                                                            (incidentally missing from PSL due to the reliance on more recent
             let s1 = encodegmw("s1",2,1) in
                                                                            innovations in conditioning logic [28]) is critical since those shares
             let s2 = encodegmw("s2",1,2) in
                                                                            will in fact be revealed if hm[𝑧]i is decoded as the circuit output.
             decodegmw(andgmw("z",s1,s2))
By convention we will assume that all gates are assigned unique               Lemma 7.3 (GMW Invariant). Given:
output identiﬁers, and that all programs are in the form of a se-                                  − ∗ (𝜋, decodegmw(𝐸 [m[𝑧]]))
                                                                                            (∅, 𝑒) →
quence of let-bindings followed by a call to decodegmw wrapping
                                                                            Then all of the following conditions hold for all 𝐻 and 𝐶 where iovars(𝜋) =
a circuit.
                                                                            𝑆 ∪ 𝑀:
   Oblivious Transfer. A passive secure oblivious transfer (OT) pro-           (1) BD(𝜋)|𝑆 ⊢ D({hm[𝑧]i})
tocol based on previous work [8] can be deﬁned in Prelude, how-                (2) BD(𝜋)|𝑆 ⊢ U(𝑀𝐶 )
ever this protocol assumes some shared randomness. Alternatively,              (3) BD(𝜋)|𝑆 ⊢ {hm[𝑧]i} ∗ {m[𝑧]@1, m[𝑧]@2})
                                                                       10
Language-Based Security for Low-Level MPC                                                                      PPDP ’24, September 10-11, 2024, Milano, Italy


   To prove this, we can formulate and automatically prove local,             auth(s,m,k,i) { assert(m == k + (m["delta"] * s))@i; }

gate-level versions of the invariant. This serves as a proof tactic           sum_she(z,x,y,i) {
that simpliﬁes the proof of the GMW invariant.                                  m[z++"s"]@i := (m[x++"s"] + m[y++"s"])@i;
                                                                                m[z++"m"]@i := (m[x++"m"] + m[y++"m"])@i;
   Lemma 7.4 (And Gate Tactic). Given:                                          m[z++"k"]@i := (m[x++"k"] + m[y++"k"])@i
                                                                              }
                                         − ∗ (𝜋, m[𝑧])
               (∅, andgmw(𝑧, m[𝑥], m[𝑦]) →                                    open(x,i1,i2){
                                                                                m[x++"exts"]@i1 := m[x++"s"]@i2;
Then all of the following conditions hold for both 𝜄 ∈ {1, 2} where             m[x++"extm"]@i1 := m[x++"m"]@i2;
iovars(𝜋) = 𝑀:                                                                  auth(m[x++"exts"], m[x++"extm"], m[x++"k"], i1);
                                                                                m[x]@i1 := (m[x++"exts"] + m[x++"s"])@i1
   (1) BD(𝜋)|{hm[𝑥]i, hm[𝑦]i} ⊢ D({hm[𝑧]i})                                   }
   (2) BD(𝜋)|{hm[𝑥]i, hm[𝑦]i} ⊢ U({m[𝑧]@𝜄})
   (3) BD(𝜋)|{hm[𝑥]i, hm[𝑦]i} ⊢ {hm[𝑧]i} ∗ {m[𝑧]@1, m[𝑧]@2}                               Figure 7: 2-party BDOZ protocol library.

   Proof. Veriﬁed automatically using techniques described in Sec-
tion 5.                                                        ⊔
                                                               ⊓              Additionally Lemma 7.5 (2) gives BD(𝜋)|𝑆 ⊢ U({m[𝑧]@𝜄}), and 𝑥.2
                                                                              and 𝑦.2 give BD(𝜋)|𝑆 ⊢ U((𝑀 1 ∪ 𝑀 2 )𝐶 ), 𝑧.3 together with unique-
   To properly integrate the local reasoning of Lemma 7.4 with                ness of gate identiﬁers implies:
the global reasoning of Lemma 7.3, we can demonstrate the fol-
                                                                                             BD(𝜋)|𝑆 ⊢ U((𝑀 1 ∪ 𝑀 2 )𝐶 ∪ {m[𝑧]@𝜄})
lowing properties of conditioning-based reasoning. While a frame
rule was developed in [28], these properties are distinct and useful          This implies the result.                                                    ⊔
                                                                                                                                                          ⊓
for reasoning about MPC. We omit proofs for brevity.                             The preceding Lemma, together with some additional observa-
  Lemma 7.5. Given P, each of the following hold for 𝑆, 𝑉1, 𝑉2, 𝑉3 ∈          tions about decoding, establish correctness of arbitrary circuits.
dom(P):                                                                                                                                            −∗
                                                                                Theorem 7.6. If 𝑒 is a GMW circuit protocol in Prelude with (∅, 𝑒) →
   (1) Given P |𝑆 ⊢ D(𝑉1 ) and P |𝑉1 ⊢ D(𝑉2 ), then P |𝑆 ⊢ D(𝑉2 ).            (𝜋, ()) then 𝜋 satisﬁes noninterference modulo output.
   (2) Given P |𝑆 ⊢ D(𝑉1 ) and P |𝑉1 ⊢ U(𝑉2 ), then P |𝑆 ⊢ U(𝑉2 ).
                                                                                 Proof. Given that 𝑒 is a GMW circuit protocol, then by deﬁni-
   (3) Given P |𝑆 ⊢ D(𝑉1 ) and P |𝑉1 ⊢ 𝑉2 ∗ 𝑉3 , then P |𝑆 ⊢ 𝑉2 ∗ 𝑉3 .
                                                                              tion we have:
   Then we can put the pieces together to prove the invariant, us-                               − ∗ (𝜋 ′, decodegmw(m[𝑧])) →
                                                                                          (∅, 𝑒) →                          − ∗ (𝜋, ())
ing automated tactics for gate-level reasoning. We sketch some el-
                                                                              where by Lemma 7.3 and deﬁnition of decodegmw, for any 𝐻 and
ements of this proof to focus on novel aspects of our technique.
                                                                              𝐶 letting iovars(𝜋) = 𝑆 ∪ 𝑀 ∪ 𝑃 ∪ 𝑂 we have:
  Proof of Lemma 7.3. By induction on the length of (∅, 𝑒) →   −∗                    BD(𝜋)|𝑆 ⊢ D({hm[𝑧]i})BD(𝜋)|𝑆 ⊢ U(𝑀𝐶 )BD(𝜋)|𝑆 ⊢
(𝜋, decodegmw(𝐸 [m[𝑧]])). Encoding establishes the invariant in the
basis. The most interesting inductive case is the andgmw gate.                                    {hm[𝑧]i} ∗ {m[𝑧]@1, m[𝑧]@2})
                                                                              and by deﬁnition of decodegmw the value {hm[𝑧]i} is output after
   Case andgmw. In this case we have:                                         the parties publicly reveal {m[𝑧]@1, m[𝑧]@2}, so we have:
           − ∗ (𝜋 ′ , decodegmw (𝐸 [andgmw(𝑧, m[𝑥], m[𝑦])])) →
    (∅, 𝑒) →                                                 −∗                          BD(𝜋)|𝑆 ⊢ U(𝑀𝐶 )                  BD(𝜋)|𝑆 ⊢ 𝑂 ∗ 𝑃
                       (𝜋, decodegmw (𝐸 [m[𝑧]]))
                                                                              which implies the result.                                                   ⊔
                                                                                                                                                          ⊓
Letting iovars(𝜋) = 𝑆 ∪ 𝑀, by deﬁnition and the induction hypoth-
esis there exist 𝑆 1, 𝑆 2 ⊆ 𝑆 and 𝑀 1 , 𝑀 2 ⊆ 𝑀 such that:                    7.2 2-Party BDOZ and Integrity Enforcement
    (x.1) BD(𝜋)|𝑆 1 ⊢ D({hm[𝑥]i})                                             In a malicious setting, “detecting cheating” by adding information-
    (x.2) BD(𝜋)|𝑆 1 ⊢ U(𝑀𝐶1 )                                                 theoretic secure MAC codes to shares is a fundamental technique
and also:                                                                     pioneered in systems such as BDOZ and SPDZ [9, 15, 16, 35]. These
                                                                              protocols assume a pre-processing phase that distributes shares
    (y.1) BD(𝜋)|𝑆 2 ⊢ D({hm[𝑦]i})                                             with MAC codes to clients. This integrates well with pre-processed
    (y.2) BD(𝜋)|𝑆 2 ⊢ U(𝑀𝐶2 )                                                 Beaver Triples to implement malicious secure, and relatively eﬃ-
and by Lemma 7.4 we have:                                                     cient, multiplication [19]. Recall that Beaver triples are values 𝑎, 𝑏, 𝑐
    (z.1) BD(𝜋)|{hm[𝑥]i, hm[𝑦]i} ⊢ D({hm[𝑧]i})                                with J𝑎 ∗ 𝑏K = 𝑐, unique per multiplication gate, that are secret
    (z.2) BD(𝜋)|{hm[𝑥]i, hm[𝑦]i} ⊢ U({m[𝑧]@𝜄})                                shared with clients during pre-processing. Here we consider the
    (z.3) BD(𝜋)|{hm[𝑥]i, hm[𝑦]i} ⊢ {hm[𝑧]i} ∗ {m[𝑧]@1, m[𝑧]@2}                2-party version.
                                                                                   A ﬁeld value 𝑣 is secret shared among 2 clients in BDOZ in the
Given 𝑥.1 and 𝑦.1 and assumed uniqueness of random variables
                                                                              same manner as in GMW, but with the addition of a separate MAC
used in each gate we have BD(𝜋)|𝑆 ⊢ D({hm[𝑥]i, hm[𝑦]i}), so it
                                                                              values. Each client 𝜄 gets a pair of values (𝑣𝜄 , 𝑚𝜄 ), where 𝑣𝜄 is a share
follows from 𝑧.1 and Lemma 7.5 (1) that BD(𝜋)|𝑆 ⊢ D({hm[𝑧]i}),
                                                                              of 𝑣 reconstructed by addition, i.e., 𝑣 = J𝑣 1 +𝑣 2 K, and 𝑚𝜄 is a MAC of
and also by 𝑧.3 and Lemma 7.5 (3):
                                                                              𝑣𝜄 . More precisely, 𝑚𝜄 = 𝑘 +(𝑘 Δ ∗𝑣𝜄 ) where keys 𝑘 and 𝑘 Δ are known
              BD(𝜋)|𝑆 ⊢ {hm[𝑧]i} ∗ {m[𝑧]@1, m[𝑧]@2}                           only to 𝜄 ′ ≠ 𝜄 and 𝑘 Δ . The local key 𝑘 is unique per MAC, while the
                                                                         11
PPDP ’24, September 10-11, 2024, Milano, Italy                                                                         Christian Skalka and Joseph P. Near


global key 𝑘 Δ is common to all MACs authenticated by 𝜄 ′ . This is             sum_she("d","a","x",1);
                                                                                sum_she("d","a","x",2);
a semi-homomorphic encryption scheme that supports addition of                  sum_she("e","b","y",1);
shares and multiplication of shares by a constant– for more details             sum_she("e","b","y",2);
the reader is referred to Orsini [35]. We note that while we restrict           open("d",1,2);
values 𝑣, 𝑚, and 𝑘 to the same ﬁeld in this presentation for simplic-           open("e",1,2);
ity, in general 𝑚 and 𝑘 can be in extensions of F𝑝 .
                                                                                p["xys2"] := (m["bs"] * m["d"] + m["as"] * m["e"] + m["cs"])@2;
   We can capture both the preliminary distribution of Beaver triples           p["xym2"] := (m["bm"] * m["d"] + m["am"] * m["e"] + m["cm"])@2;
and BDOZ shares as a pre-processing predicate that establishes
conditions for initial memories (see Deﬁnition 3.11). Here we as-               m["xys"]@1 := (m["bs"] * m["d"] + m["as"] * m["e"] + m["cs"] +
                                                                                               m["d"] * m["e"])@1;
sume two input secrets s[𝑥]@1 and s[𝑦]@2 and a single Beaver                    m["xyk"]@1 := (m["bk"] * m["d"] + m["ak"] * m["e"] + m["ck"])@1;
Triple to compute s[𝑥]@1 ∗ s[𝑦]@2, but we can extend this for ad-
                                                                                auth(p["xys2"], p["xym2"], m["xyk"], 1);
ditional gates. As for GMW, we use hm[𝑤]i to refer to secret-shared
values reconstructed with addition, but for BDOZ by convention                  out@1 := m["xys"] + p["xys2"]@1
each share of hm[𝑤]i is represented as m[𝑤s]@𝜄, the MAC of which
is represented as a m[𝑤m]@𝜄 for all 𝜄, and each client holds a key              Figure 8: Authenticated 2-party multiplication with honest
m[𝑤k]@𝜄 for authentication of the other’s share.                                client 1.
   Deﬁnition 7.7 (BDOZ preprocessing). Deﬁne:
         shares , {m[𝑤s]@𝜄 | 𝜄 ∈ {1, 2} ∧ 𝑤 ∈ {𝑎, 𝑏, 𝑐, 𝑥, 𝑦}}                  7.3 Cheating Detection and Integrity
                                                                                We can carry out similar proofs of passive security for the protocol
          macs , {m[𝑤m]@𝜄 | 𝜄 ∈ {1, 2} ∧ 𝑤 ∈ {𝑎, 𝑏, 𝑐, 𝑥, 𝑦}}                   in Figure 8 as for GMW, even using automated tactics for the pro-
                                                                                tocol in F2 . But in the case of BDOZ we are also concerned with
                   {m[𝑤k]@𝜄 | 𝜄 ∈ {1, 2} ∧ 𝑤 ∈ {𝑎, 𝑏, 𝑐, 𝑥, 𝑦}}∪
        keys ,                                                                  malicious security. To demonstrate this, we can show that the pro-
                   {m[delta]@𝜄 | 𝜄 ∈ {1, 2}}
                                                                                tocol satisﬁes integrity in the sense of Deﬁnition 4.6. To do so, we
Then a memory 𝜎 satisﬁes BDOZ preprocessing iﬀ:                                 observe that it satisﬁes a stronger property, that we call cheating
        dom(𝜎) = {s[𝑥]@1, s[𝑦]@2} ∪ shares ∪ macs ∪ keys                        detection. Cheating detection says that the adversary can only exe-
                                                                                cute the protocol honestly, or or else gets caught (and abort). Note
and, writing 𝜎 (hm[𝑤]i) to denote J𝜎 (m[𝑤s]@1) + 𝜎 (m[𝑤s]@2)K,                  in particular that this is not a form of endorsement (the dual of de-
the following conditions hold:                                                  classiﬁcation), which allows the adversary some leeway. Rather, it
      𝜎 (hm[𝑥]i) = 𝜎 (s[𝑥]@1)                    𝜎 (hm[𝑦]i) = 𝜎 (s[𝑦]@2)        is a conﬁrmation of high integrity.
                                                                                   Focusing in, we identify the adversarial inputs as the messages
                 J𝜎 (hm[𝑎]i) ∗ 𝜎 (hm[𝑏]i)K = 𝜎 (hm[𝑐]i)                         sent from the adversary to honest parties on which honest responses
and for all 𝜄, 𝜄 ′ ∈ {1, 2} with 𝜄 ≠ 𝜄 ′ and 𝑤 ∈ {𝑎, 𝑏, 𝑐, 𝑥, 𝑦}:               to the adversary may depend. We want to say that these are the
                                                                                messages that must be legitimate.
 𝜎 (m[𝑤m]@𝜄) = J𝜎 (m[𝑤k]@𝜄 ′ ) + 𝜎 (m[delta]@𝜄 ′ ) ∗ 𝜎 (m[𝑤s]@𝜄)K
                                                                                   Deﬁnition 7.8. Given 𝜋 with iovars(𝜋) = 𝑆 ∪ 𝑉 ∪ 𝑂, let 𝑋𝐻 ⊆
   With these conventions, a BDOZ library is deﬁned in Figure
                                                                                {𝑥 | 𝑥 ∈ (𝑉𝐻 ⊲𝐶 ∪ 𝑂 𝐻 ) ∧ 𝑥 ∈ dom(𝜎)}. Then the adversarial inputs
7 and a multiplication protocol to compute s[𝑥]@1 ∗ s[𝑦]@2 is
                                                                                to 𝑋𝐻 is the least set 𝑋𝐶 ⊆ 𝑉𝐶⊲𝐻 such that BD(𝜋) 0 𝑋𝐶 ∗ 𝑋𝐻 .
deﬁned in Figure 8. The latter is malicious secure assuming that
client 1 is trusted. Initially, in calls to sum_she each party computes            Now, we can characterize protocols with cheating detection as
the sum of their shares of s[𝑥]@1 + hm[𝑎]i and s[𝑦]@2 + hm[𝑏]i,                 those where the adversary can only behave honestly/passively, or
and non-interactively computes the associated MACs and keys in                  else cause abort.
the SHE authentication scheme. These values are then securely
                                                                                   Deﬁnition 7.9 (Cheating Detection). Cheating is detectable in 𝜋
opened on client 1, which authenticates client 2’s share via a call
                                                                                with iovars(𝜋) = 𝑆 ∪ 𝑉 ∪ 𝑂 iﬀ for all 𝜎 ∈ runs A (𝜋), letting 𝑋𝐻 =
to auth that asserts the BDOZ authentication property. Note that
                                                                                {𝑥 | 𝑥 ∈ (𝑉𝐻 ⊲𝐶 ∪ 𝑂 𝐻 ) ∧ 𝑥 ∈ dom(𝜎)}, and letting 𝑋𝐶 be the
the opening of s[𝑦]@2 + hm[𝑏]i reveals no information to client 1
                                                                                adversarial inputs to 𝑋𝐻 , there exists 𝜎 ′ ∈ runs(𝜋) with 𝜎𝑋𝐶 =
about s[𝑦]@2 since hm[𝑏]i is in a uniform random distribution by
                                                                                𝜎𝑋′ .
assumption. It is also malicious secure since any cheating is de-                 𝐶

tected by the assert.                                                              It is straightforward to demonstrate that cheating detection has
   Following this, each party non-interactively calculates their share          integrity, since only the “passive” adversary can elicit a response
of s[𝑥]@1∗s[𝑦]@2, while client 2 calculates the MAC of their share,             from honest parties.
and reveals both their share and MAC to client 1. These are reveals
                                                                                  Lemma 7.10. If cheating is detectable in 𝜋, then 𝜋 has integrity.
since information about s[𝑦]@2 is exposed by the multiplication.
Client 1 also calculates the appropriate key and authenticates client              In the case of BDOZ, cheating detection is accomplished by the
2’s share following the BDOZ SHE MAC scheme [35] and the stan-                  information-theoretic security of the encryption scheme [19]. Fur-
dard Beaver protocol [19]. Hence the protocol is correct and mali-              thermore, the symmetry of the protocol in Figure 8 ensures that
cious secure given trusted client 1. The authentication scheme can              both parties will authenticate shares, so it is robust to corruption
also be run symmetrically on client 2.                                          of either party.
                                                                           12
Language-Based Security for Low-Level MPC                                                                                            PPDP ’24, September 10-11, 2024, Milano, Italy


8    CONCLUSION AND FUTURE WORK                                                               [13] Bob Carpenter, Andrew Gelman, Matthew D Hoﬀman, Daniel Lee, Ben
                                                                                                   Goodrich, Michael Betancourt, Marcus A Brubaker, Jiqiang Guo, Peter Li, and
The Prelude/Overture language model developed in this paper, along                                 Allen Riddell. 2017. Stan: A probabilistic programming language. Journal of
with the suite of hyperproperties explored, are a foundation for                                   statistical software 76 (2017).
                                                                                              [14] Michael R. Clarkson and Fred B. Schneider. 2010. Hyperproperties. J. Comput.
deﬁning low-level MPC protocols and exploring methods for se-                                      Secur. 18, 6 (sep 2010), 1157–1210.
curity veriﬁcation. There are several promising avenues for future                            [15] Ivan Damgård and Claudio Orlandi. 2010. Multiparty Computation for Dishon-
work. Concurrency will be important to capture common MPC id-                                      est Majority: From Passive to Active Security at Low Cost. In Advances in Cryp-
                                                                                                   tology – CRYPTO 2010, Tal Rabin (Ed.). Springer Berlin Heidelberg, Berlin, Hei-
ioms such as commitment and circuit optimizations, and to con-                                     delberg, 558–576.
sider the UC security model [2, 19]. To support better veriﬁcation,                           [16] Ivan Damgård, Valerio Pastro, Nigel Smart, and Sarah Zakarias. 2012. Multiparty
integration of our tactics with a proof assistant is a compelling di-                              Computation from Somewhat Homomorphic Encryption. In Advances in Cryp-
                                                                                                   tology – CRYPTO 2012, Reihaneh Safavi-Naini and Ran Canetti (Eds.). Springer
rection that resonate with previous work [22].                                                     Berlin Heidelberg, Berlin, Heidelberg, 643–662.
   Better automated veriﬁcation is a main goal for future work.                               [17] David Darais, Ian Sweet, Chang Liu, and Michael Hicks. 2019. A language for
                                                                                                   probabilistically oblivious computation. Proceedings of the ACM on Programming
Security types have been eﬀectively leveraged for high-level pro-                                  Languages 4, POPL (2019), 1–31.
grams, for both passive and malicious security. This suggests that                            [18] Luc De Raedt, Angelika Kimmig, and Hannu Toivonen. 2007. ProbLog: A proba-
they can be similarly applied at low levels in a way that is comple-                               bilistic Prolog and its application in link discovery. In IJCAI 2007, Proceedings of
                                                                                                   the 20th international joint conference on artiﬁcial intelligence. IJCAI-INT JOINT
mentary to high-level systems. Generalizing our automated anal-                                    CONF ARTIF INTELL, 2462–2467.
ysis in F2 to larger arithmetic ﬁelds is also a compelling techni-                            [19] David Evans, Vladimir Kolesnikov, Mike Rosulek, et al. 2018. A pragmatic intro-
cal challenge with potential practical beneﬁts, e.g., application to                               duction to secure multi-party computation. Foundations and Trends® in Privacy
                                                                                                   and Security 2, 2-3 (2018), 70–246.
arithmetic circuits.                                                                          [20] Shang Gao, Zhe Peng, Feng Tan, Yuanqing Zheng, and Bin Xiao. 2022. Symme-
                                                                                                   Proof: Compact zero-knowledge argument for blockchain conﬁdential transac-
                                                                                                   tions. IEEE Transactions on Dependable and Secure Computing (2022).
                                                                                              [21] Oded Goldreich, Silvio Micali, and Avi Wigderson. 2019. How to play any mental
REFERENCES                                                                                         game, or a completeness theorem for protocols with honest majority. In Provid-
 [1] Martin Abadi and Phillip Rogaway. 2000. Reconciling Two Views of Cryptogra-                   ing Sound Foundations for Cryptography: On the Work of Shaﬁ Goldwasser and
     phy. In Theoretical Computer Science: Exploring New Frontiers of Theoretical In-              Silvio Micali. 307–328.
     formatics, Jan van Leeuwen, Osamu Watanabe, Masami Hagiya, Peter D. Mosses,              [22] H. Haagh, A. Karbyshev, S. Oechsner, B. Spitters, and P. Strub. 2018. Computer-
     and Takayasu Ito (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 3–22.                Aided Proofs for Multiparty Computation with Active Security. In 2018 IEEE 31st
 [2] C. Acay, J. Gancher, R. Recto, and A. Myers. 2024. Secure Synthesis of Dis-                   Computer Security Foundations Symposium (CSF). IEEE Computer Society, Los
     tributed Cryptographic Applications. In 2024 IEEE 37th Computer Security Foun-                Alamitos, CA, USA, 119–131. https://doi.org/10.1109/CSF.2018.00016
     dations Symposium (CSF). IEEE Computer Society, Los Alamitos, CA, USA, 315–              [23] Steven Holtzen, Guy Van den Broeck, and Todd Millstein. 2020. Scaling exact
     330. https://doi.org/10.1109/CSF61375.2024.00021                                              inference for discrete probabilistic programs. Proceedings of the ACM on Pro-
 [3] Coşku Acay, Rolph Recto, Joshua Gancher, Andrew C. Myers, and Elaine Shi.                     gramming Languages 4, OOPSLA (2020), 1–31.
     2021. Viaduct: An Extensible, Optimizing Compiler for Secure Distributed                 [24] Sebastian Hunt, David Sands, and Sandro Stucki. 2023. Reconciling Shannon
     Programs. In Proceedings of the 42nd ACM SIGPLAN International Conference                     and Scott with a Lattice of Computable Information. Proc. ACM Program. Lang.
     on Programming Language Design and Implementation (Virtual, Canada) (PLDI                     7, POPL, Article 68 (jan 2023), 30 pages. https://doi.org/10.1145/3571740
     2021). Association for Computing Machinery, New York, NY, USA, 740–755.                  [25] Yuval Ishai, Eyal Kushilevitz, Rafail Ostrovsky, and Amit Sahai. 2009. Zero-
     https://doi.org/10.1145/3453483.3454074                                                       knowledge proofs from secure multiparty computation. SIAM J. Comput. 39,
 [4] Aws Albarghouthi, Loris D’Antoni, Samuel Drews, and Aditya V Nori. 2017.                      3 (2009), 1121–1152.
     Fairsquare: probabilistic veriﬁcation of program fairness. Proceedings of the ACM        [26] Brian Knott, Shobha Venkataraman, Awni Hannun, Shubho Sengupta, Mark
     on Programming Languages 1, OOPSLA (2017), 1–30.                                              Ibrahim, and Laurens van der Maaten. 2021. Crypten: Secure multi-party com-
 [5] José Bacelar Almeida, Manuel Barbosa, Gilles Barthe, Hugo Pacheco, Vitor                      putation meets machine learning. Advances in Neural Information Processing
     Pereira, and Bernardo Portela. 2018. Enforcing ideal-world leakage bounds in                  Systems 34 (2021), 4961–4973.
     real-world secret sharing MPC frameworks. In 2018 IEEE 31st Computer Security            [27] Karl Koch, Stephan Krenn, Donato Pellegrino, and Sebastian Ramacher. 2020.
     Foundations Symposium (CSF). IEEE, 132–146.                                                   Privacy-preserving analytics for data markets using MPC. In IFIP International
 [6] Aslan Askarov and Andrei Sabelfeld. 2007. Gradual Release: Unifying Declassiﬁ-                Summer School on Privacy and Identity Management. Springer, 226–246.
     cation, Encryption and Key Release Policies. In 2007 IEEE Symposium on Security          [28] John M Li, Amal Ahmed, and Steven Holtzen. 2023. Lilac: a Modal Separation
     and Privacy (SP ’07). 207–221. https://doi.org/10.1109/SP.2007.22                             Logic for Conditional Probability. Proceedings of the ACM on Programming Lan-
 [7] Yaniv Aspis. 2018. A Linear Algebraic Approach to Logic Programming. Ph.D.                    guages 7, PLDI (2023), 148–171.
     Dissertation. Master thesis at Imperial College London.                                  [29] Xiling Li, Rafael Dowsley, and Martine De Cock. 2021. Privacy-preserving fea-
 [8] Gilles Barthe, Justin Hsu, and Kevin Liao. 2019. A probabilistic separation                   ture selection with secure multiparty computation. In International Conference
     logic. Proc. ACM Program. Lang. 4, POPL, Article 55 (dec 2019), 30 pages.                     on Machine Learning. PMLR, 6326–6336.
     https://doi.org/10.1145/3371123                                                          [30] Yehuda Lindell. 2017.        How to Simulate It – A Tutorial on the Simula-
 [9] Rikke Bendlin, Ivan Damgård, Claudio Orlandi, and Sarah Zakarias. 2011. Semi-                 tion Proof Technique.       Springer International Publishing, Cham, 277–346.
     homomorphic Encryption and Multiparty Computation. In Advances in Cryptol-                    https://doi.org/10.1007/978-3-319-57048-8_6
     ogy – EUROCRYPT 2011, Kenneth G. Paterson (Ed.). Springer Berlin Heidelberg,             [31] Jun Liu, Yuan Tian, Yu Zhou, Yang Xiao, and Nirwan Ansari. 2020. Privacy
     Berlin, Heidelberg, 169–188.                                                                  preserving distributed data mining based on secure multi-party computation.
[10] Eli Bingham, Jonathan P Chen, Martin Jankowiak, Fritz Obermeyer, Neeraj Prad-                 Computer Communications 153 (2020), 208–216.
     han, Theofanis Karaletsos, Rohit Singh, Paul Szerlip, Paul Horsfall, and Noah D          [32] Donghang Lu, Thomas Yurek, Samarth Kulshreshtha, Rahul Govind, Aniket
     Goodman. 2019. Pyro: Deep universal probabilistic programming. The Journal                    Kate, and Andrew Miller. 2019. Honeybadgermpc and asynchromix: Practical
     of Machine Learning Research 20, 1 (2019), 973–978.                                           asynchronous mpc and its application to anonymous communication. In Pro-
[11] Dan Bogdanov, Peeter Laud, and Jaak Randmets. 2014. Domain-Polymorphic                        ceedings of the 2019 ACM SIGSAC Conference on Computer and Communications
     Programming of Privacy-Preserving Applications. In Proceedings of the Ninth                   Security. 887–903.
     Workshop on Programming Languages and Analysis for Security (Uppsala, Swe-               [33] Dahlia Malkhi, Noam Nisan, Benny Pinkas, and Yaron Sella. 2004. Fairplay—A
     den) (PLAS’14). Association for Computing Machinery, New York, NY, USA, 53–                   Secure Two-Party Computation System. In 13th USENIX Security Symposium
     65. https://doi.org/10.1145/2637113.2637119                                                   (USENIX Security 04). USENIX Association, San Diego, CA.
[12] Chris Brzuska and Sabine Oechsner. 2023.              A State-Separating Proof           [34] John C. Mitchell, Rahul Sharma, Deian Stefan, and Joe Zimmerman.
     for Yao’s Garbling Scheme. In Proceedings - 2023 IEEE 36th Computer                           2012.      Information-Flow Control for Programming on Encrypted Data.
     Security Foundations Symposium, CSF 2023 (Proceedings - IEEE Com-                             In 2012 IEEE 25th Computer Security Foundations Symposium. 45–60.
     puter Security Foundations Symposium). IEEE Computer Society, 137–152.                        https://doi.org/10.1109/CSF.2012.30
     https://doi.org/10.1109/CSF57540.2023.00009 36th IEEE Computer Security                  [35] Emmanuela Orsini. 2021. Eﬃcient, Actively Secure MPC with a Dishonest Ma-
     Foundations Symposium, CSF 2023 ; Conference date: 09-07-2023 Through                         jority: A Survey. In Arithmetic of Finite Fields, Jean Claude Bajard and Alev Top-
     13-07-2023.                                                                                   uzoğlu (Eds.). Springer International Publishing, Cham, 42–71.
                                                                                         13
PPDP ’24, September 10-11, 2024, Milano, Italy                                                                                              Christian Skalka and Joseph P. Near


[36] Avi Pfeﬀer. 2009. Figaro: An object-oriented probabilistic programming lan-                 10th International Conference, KSEM 2017, Melbourne, VIC, Australia, August 19-
     guage. Charles River Analytics Technical Report 137, 96 (2009), 4.                          20, 2017, Proceedings 10. Springer, 520–533.
[37] Aseem Rastogi, Matthew A Hammer, and Michael Hicks. 2014. Wysteria: A                  [42] Walid Taha and Tim Sheard. 2000. MetaML and multi-stage programming
     programming language for generic, mixed-mode multiparty computations. In                    with explicit annotations. Theoretical Computer Science 248, 1 (2000), 211–242.
     2014 IEEE Symposium on Security and Privacy. IEEE, 655–670.                                 https://doi.org/10.1016/S0304-3975(00)00053-0 PEPM’97.
[38] Aseem Rastogi, Nikhil Swamy, and Michael Hicks. 2019. Wys*: A DSL                      [43] Antonio Emerson Barros Tomaz, Jose Claudio Do Nascimento, Abdelhakim Sen-
     for Veriﬁed Secure Multi-party Computations. In 8th International Conference                haji Haﬁd, and Jose Neuman De Souza. 2020. Preserving privacy in mobile health
     on Principles of Security and Trust (POST) (Lecture Notes in Computer Sci-                  systems using non-interactive zero-knowledge proof and blockchain. IEEE ac-
     ence), Flemming Nielson and David Sands (Eds.), Vol. 11426. Springer, 99–122.               cess 8 (2020), 204441–204458.
     https://doi.org/10.1007/978-3-030-17138-4_5                                            [44] Frank Wood, Jan Willem Meent, and Vikash Mansinghka. 2014. A new approach
[39] Feras A Saad, Martin C Rinard, and Vikash K Mansinghka. 2021. SPPL: prob-                   to probabilistic programming inference. In Artiﬁcial intelligence and statistics.
     abilistic programming with fast exact symbolic inference. In Proceedings of the             PMLR, 1024–1032.
     42nd ACM SIGPLAN International Conference on Programming Language Design               [45] Qianchuan Ye and Benjamin Delaware. 2022.           Oblivious Algebraic Data
     and Implementation. 804–819.                                                                Types. Proc. ACM Program. Lang. 6, POPL, Article 51 (jan 2022), 29 pages.
[40] Andrei Sabelfeld and David Sands. 2009. Declassiﬁcation: Dimensions and Prin-               https://doi.org/10.1145/3498713
     ciples. J. Comput. Secur. 17, 5 (oct 2009), 517–548.                                   [46] S. Zdancewic and A.C. Myers. 2001.           Robust declassiﬁcation. In Pro-
[41] Chiaki Sakama, Katsumi Inoue, and Taisuke Sato. 2017. Linear algebraic charac-              ceedings. 14th IEEE Computer Security Foundations Workshop, 2001. 15–23.
     terization of logic programs. In Knowledge Science, Engineering and Management:             https://doi.org/10.1109/CSFW.2001.930133




                                                                                       14
