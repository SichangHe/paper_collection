              Verifiable Side-Channel Security
             of Cryptographic Implementations:
                 Constant-Time MEE-CBC

         José Bacelar Almeida1,2 , Manuel Barbosa1,3(B) , Gilles Barthe4 ,
                          and François Dupressoir4(B)
                       1
                         HASLab – INESC TEC, Porto, Portugal
                           2
                          University of Minho, Braga, Portugal
                                  jba@di.uminho.pt
                    3
                      DCC-FC, University of Porto, Porto, Portugal
                                  mbb@dcc.fc.up.pt
                      4
                        IMDEA Software Institute, Madrid, Spain
                                fdupress@gmail.com



       Abstract. We provide further evidence that implementing software
       countermeasures against timing attacks is a non-trivial task and requires
       domain-speciﬁc software development processes: we report an imple-
       mentation bug in the s2n library, recently released by AWS Labs.
       This bug (now ﬁxed) allowed bypassing the balancing countermeasures
       against timing attacks deployed in the implementation of the MAC-then-
       Encode-then-CBC-Encrypt (MEE-CBC) component, creating a timing
       side-channel similar to that exploited by Lucky 13.
          Although such an attack could only be launched when the MEE-CBC
       component is used in isolation – Albrecht and Paterson recently con-
       ﬁrmed in independent work that s2n’s second line of defence, once rein-
       forced, provides adequate mitigation against current adversary capabili-
       ties – its existence serves as further evidence to the fact that conventional
       software validation processes are not eﬀective in the study and valida-
       tion of security properties. To solve this problem, we deﬁne a method-
       ology for proving security of implementations in the presence of timing
       attackers: ﬁrst, prove black-box security of an algorithmic description of
       a cryptographic construction; then, establish functional correctness of an
       implementation with respect to the algorithmic description; and ﬁnally,
       prove that the implementation is leakage secure.
          We present a proof-of-concept application of our methodology to
       MEE-CBC, bringing together three diﬀerent formal veriﬁcation tools to
       produce an assembly implementation of this construction that is ver-
       iﬁably secure against adversaries with access to some timing leakage.
       Our methodology subsumes previous work connecting provable security
       and side-channel analysis at the implementation level, and supports the
       veriﬁcation of a much larger case study. Our case study itself provides
       the ﬁrst provable security validation of complex timing countermeasures
       deployed, for example, in OpenSSL.



c International Association for Cryptologic Research 2016
T. Peyrin (Ed.): FSE 2016, LNCS 9783, pp. 163–184, 2016.
DOI: 10.1007/978-3-662-52993-5 9
164     J.B. Almeida et al.

1     Introduction
There is an uncomfortable gap between provable security and practical imple-
mentations. Provable security gives strong guarantees that a cryptographic con-
struction is secure against eﬃcient black-box adversaries. Yet, implementations
of provably secure constructions may be vulnerable to practical attacks, due to
implementation errors or side-channels. The tension between provable security
and cryptographic engineering is illustrated by examples such as the MAC-then-
Encode-then-CBC-Encrypt construction (MEE-CBC), which is well-understood
from the perspective of provable security [22,26], but whose implementation has
been the source of several practical attacks in SSL or TLS implementations.
These security breaks are, in the case of MEE-CBC, due to vulnerable imple-
mentations providing the adversary with padding oracles, either through error
messages [29], or through observable non-functional behaviours such as execu-
tion time [2,16]. These examples illustrate two shortcomings of provable security
when it comes to dealing with implementations. First, the algorithmic descrip-
tions used in proofs elide many potentially critical details; these details must be
ﬁlled by implementors, who may not have the specialist knowledge required to
make the right decision. Second, attackers targeting real-world platforms may
break a system by exploiting side-channel leakage, which is absent in the black-
box abstractions in which proofs are obtained.
    These shortcomings are addressed independently by real-world cryptography
and secure coding methodologies, both of which have their own limitations. Real-
world cryptography [18] is a branch of provable security that incorporates lower-
level system features in security notions and proofs (for example, precise error
messages or message fragmentation). Real-world cryptography is a valuable tool
for analyzing the security of real-world protocols such as TLS or SSH, but is only
now starting to address side-channels [8,15] and, until now, has stayed short of
considering actual implementations. Secure coding methodologies eﬀectively mit-
igate side-channel leakage; for instance, the constant-time methodology [13,21]
is consensual among practitioners as a means to ensure a good level of protec-
tion against timing and cache-timing attacks. However, a rigorous justiﬁcation
of such techniques and their application is lacking and they are disconnected
from provable security, leaving room for subtle undetected vulnerabilities even
in carefully tailored implementations.
    In this paper we show how the real-world cryptography approach can be
extended – with computer-aided support – to formally capture the guarantees
that implementors empirically pursue using secure coding techniques.

1.1   Our Contributions
Recent high-visibility attacks such as Lucky 13 [2] have shown that timing leak-
age can be exploited in practice to break the security of pervasively used proto-
cols such as TLS, and have led practitioners to pay renewed attention to software
countermeasures against timing attacks. Two prominent examples of this are
the recent reimplementation of MEE-CBC decryption in OpenSSL [23], which
         Veriﬁable Side-Channel Security of Cryptographic Implementations         165

enforces a constant-time coding policy as mitigation for the Lucky 13 attack,
and the defense in depth mitigation strategy adopted by Amazon Web Services
Labs (AWS Labs) in a new implementation of TLS called s2n, where various
fuzzing- and balancing-based timing countermeasures are combined to reduce
the amount of information leaked through timing. However, the secure-coding
eﬀorts of cryptography practitioners are validated using standard software engi-
neering techniques such as testing and code reviews, which are not well-suited
to reasoning about non-functional behaviours or cryptography.
    As a ﬁrst contribution and motivation for our work, we provide new evidence
of this latent problem by recounting the story of Amazon’s recently released s2n
library, to which we add a new chapter.
New evidence in s2n. In June 2015, AWS-Labs made public a new open-source
implementation of the TLS protocol, called s2n [28] and designed to be “small,
fast, with simplicity as a priority”. By excluding rarely used options and exten-
sions, the implementation can remain small, with only around 6 K lines of code.
Its authors also report extensive validation, including three external security
evaluations and penetration tests. The library’s source code and documentation
are publicly available.1
    Recently, Albrecht and Paterson [1] presented a detailed analysis of the coun-
termeasures against timing attacks in the original release of s2n, in light of the
lessons learned in the aftermath of Lucky 13 [2]. In their study, they found that
the implementation of the MEE-CBC component was not properly balanced, and
exposed a timing attack vector that was exploitable using Lucky 13-like tech-
niques. Furthermore, they found that the second layer of countermeasures that
randomizes error reporting delays was insuﬃcient to remove the attack vector.
Intuitively, the granularity of the randomized delays was large enough in com-
parison to the data-dependent timing variations generated by the MEE-CBC
component that they could be ‘ﬁltered out’ leaving an exploitable side-channel.
As a response to these ﬁndings, the s2n implementation was patched,2 and both
layers of countermeasures were improved to remove the attack vector.3
    Unfortunately, this is not the end of the story. In this paper we report an
implementation bug in this “ﬁxed” version of the library, as well as a timing
attack akin to Lucky 13 that bypasses once more the branch-balancing timing
countermeasures deployed in the s2n implementation of MEE-CBC. This imple-
mentation bug was subtly hidden in the implementation of the timing counter-
measures themselves, which were added as mitigation for the attack reported

1
  https://github.com/awslabs/s2n.
2
  See the details of the applied ﬁxes in https://github.com/awslabs/s2n/commit/
  4d3729.
3
  We note that the delay randomization countermeasure was further improved since
  the attacks we describe to sampling the delay between 10 s and 30 s (https://github.
  com/awslabs/s2n/commit/731e7d). Further, measures were added to prevent care-
  less or rogue application code from forcing s2n to signal decryption failures to the
  adversary before that delay had passed (https://github.com/awslabs/s2n/commit/
  f8a155).
166      J.B. Almeida et al.

by Albrecht and Paterson [1]. We show that the bug rendered the countermea-
sure code in the MEE-CBC component totally ineﬀective by presenting a timing
attack that breaks the MEE-CBC implementation when no additional timing
countermeasures were present. Due to space constraints, details of the attack
are given in the full version of the paper.4

Disclosure Timeline and Recommendations. The implementation bug and tim-
ing attack were reported to AWS Labs on September 4, 2015. The problem
was promptly acknowledged and the current head revision of the oﬃcial s2n
repository no longer exhibits the bug and potential attack vector from the
MEE-CBC implementation. Subsequent discussions with Albrecht and Pater-
son and AWS Labs lead us to believe that s2n’s second line of defence (the ﬁner
grained error reporting delay randomization mechanism validated by Albrecht
and Paterson [1]) is currently suﬃcient to thwart potential exploits of the timing
side-channel created by the bug. Therefore, systems relying on unpatched but
complete versions of the library are safe. On the other hand, any system relying
directly on the unpatched MEE-CBC implementation, without the global ran-
domized delay layer, will be vulnerable and should upgrade to the latest version.
The need for formal validation. The sequence of events reported above5
shows that timing countermeasures are extremely hard to get right and very hard
to validate. Our view is that implementors currently designing and deploying
countermeasures against side-channel attacks face similar problems to those that
were faced by the designers of cryptographic primitives and protocols before
the emergence of provable security. On the one hand, we lack a methodology
to rigorously characterize and prove the soundness of existing designs such as
the ones deployed, e.g., in OpenSSL; on the other hand, we have no way of
assessing the soundness of new designs, such as those adopted in s2n, except via
empirical validation and trial-and-error. This leads us to the following question:
can we bring the mathematical guarantees of provable security to cryptographic
implementations? We take two steps towards answering this question.
A Case Study: Constant-Time MEE-CBC. Our second and main con-
tribution is the ﬁrst formal and machine-checked proof of security for an x86
implementation of MEE-CBC in an attack model that includes control-ﬂow and
cache-timing channels. In particular, our case study validates the style of coun-
termeasures against timing attacks currently deployed in the OpenSSL imple-
mentation of MEE-CBC. We achieve this result by combining three state-of-
the-art formal veriﬁcation tools: i. we rely on EasyCrypt [6,7] to formalize a
speciﬁcation of MEE-CBC and some of the known provable security results for


4
    https://eprint.iacr.org/2015/1241.
5
    The very interesting blog post in http://blogs.aws.amazon.com/security/post/
    TxLZP6HNAYWBQ6/s2n-and-Lucky-13 analyses these events from the perspective
    of the AWS Labs development team.
           Veriﬁable Side-Channel Security of Cryptographic Implementations            167

this construction;6 ii. we use Frama-C to establish a functional equivalence result
between EasyCrypt speciﬁcations and C implementations; and iii. we apply the
CompCert certiﬁed compiler [24] and the certiﬁed information-ﬂow type-system
from [4] to guarantee that the compiled implementation does not leak secret
information through the channels considered, and that the compiled x86 code is
correct with respect to the EasyCrypt speciﬁcation proved secure initially.
A Framework for Implementation Security. To tie these veriﬁcation
results together, we introduce — as our third contribution — a framework of
deﬁnitions and theorems that abstracts the details of the case study. This frame-
work yields a general methodology for proving security properties of low-level
implementations in the presence of adversaries that may observe leakage. This
methodology relies on separating three diﬀerent concerns: i. black-box specifi-
cation security, which establishes the computational security of a functional
speciﬁcation (here one can adopt the real-world cryptography approach); ii.
implementation correctness, which establishes that the considered implemen-
tation behaves, as a black-box, exactly like its functional speciﬁcation; and iii.
leakage security, which establishes that the leakage due to the execution of the
implementation code in some given leakage model is independent from its secret
inputs. Our main theorem, which is proven using the previous methodology,
establishes that our x86 implementation retains the black-box security proper-
ties of the MEE-CBC speciﬁcation, i.e., it is a secure authenticated encryption
scheme, even in the presence of a strong timing attacker, and based on standard
black-box cryptographic assumptions.
    We insist that we do not claim to formally or empirically justify the validity
of any particular leakage model: for this we rely on the wisdom of practitioners.
What we do provide is a means to take a well-accepted leakage model, and sepa-
rately and formally verify, through leakage security, that a concrete deployment
of a particular countermeasure in a given implementation does in fact guarantee
the absence of any leakage that would weaken a particular security property in
the chosen leakage model.

Outline. In Sect. 2, we describe the MEE-CBC construction and informally dis-
cuss its security at speciﬁcation- and implementation-level. We then present the
deﬁnitions for implementation-level security notions and the statement of our
main theorem (Sect. 3). In Sect. 4, we introduce our methodology, before detail-
ing its application to MEE-CBC in Sect. 5. We then present and discuss some
benchmarking results in Sect. 6. Finally, we discuss potential extensions to our
framework not illustrated by our case study (Sect. 7). We conclude the paper
and discuss directions for future work in Sect. 8. A long version of this paper,
6
    Formalizing all known results for MEE-CBC would be beyond the scope of this
    paper, and we assume that our EasyCrypt speciﬁcation of the construction inherits
    all the security properties that have been proved in the literature. In other words, in
    addition to the properties we formalize, we assume that our MEE-CBC speciﬁcation
    satisﬁes the standard notions of security for authenticated encryption as proved, e.g.,
    by Paterson, Ristenpart and Shrimpton [26].
168      J.B. Almeida et al.

with appendices including code snippets, formal deﬁnitions of standard black-
box speciﬁcation-level security notions, and a discussion of further related work
appears on the IACR eprint server.7


2     Case Study: MEE-CBC
MAC-then-Encode-then-CBC-Encrypt (MEE-CBC) is an instance of the MAC-
then-Encrypt generic construction that combines a block cipher used in CBC
mode with some padding and a MAC scheme in order to obtain an authenticated
encryption scheme. We consider the speciﬁc instantiation of the construction
that is currently most widely used within TLS: i. A MAC tag of length tlen
is computed over the TLS record header hdr, a sequence number seq and the
payload pld. The length of the authenticated string is therefore the length of
the payload plus a small and ﬁxed number of bytes. Several MAC schemes can
be used to authenticate this message, but we only consider HMAC-SHA256. ii.
The CBC-encrypted message m comprises the payload pld concatenated with the
MAC tag (the sequence number is not transmitted and the header is transmitted
in the clear). iii. The padding added to m comprises plen bytes of value plen − 1,
where plen may be any value in the range [1..256], such that plen + |m| is a
multiple of the cipher’s block size. iv. We use AES-128 as block cipher, which
ﬁxes a 16-byte block size.
    At the high level, the HMAC construction computes

             H((keyMAC ⊕ opad) || H((keyMAC ⊕ ipad) || hdr || seq || pld)) .

We consider a hash function such as SHA-256, which follows the Merkle-
Damgård paradigm: a compression function is iterated to gradually combine
the already computed hash value with a new 64-byte message block (hash values
are tlen bytes long).
Informal security discussion. The theoretical security of MEE-CBC has
received a lot of attention in the past, due to its high-proﬁle usage in the
SSL/TLS protocol. Although it is well-known that the MAC-then-Encrypt con-
struction does not generically yield a secure authenticated encryption scheme [9],
the particular instantiation used in TLS has been proven secure [22,25,26]. The
most relevant result for this paper is that by Paterson, Ristenpart and Shrimp-
ton [26]. Crucially, their high-level proof explicitly clariﬁes the need for the
implementation to not reveal, in any way, which of the padding or MAC check
failed on decryption failures. This is exactly the kind of padding oracles exploited
in practical attacks against MEE-CBC such as Lucky 13 [2].
    After the disclosure of the Lucky 13 attack [2], signiﬁcant eﬀort was invested
into identifying all potential sources of timing leakage in the MEE-CBC decryp-
tion algorithm. The implementation subsequently incorporated into OpenSSL,
for example, deploys constant-time countermeasures that guarantee the following

7
    https://eprint.iacr.org/2015/1241.
         Veriﬁable Side-Channel Security of Cryptographic Implementations       169

behaviours [23]: i. removing the padding and checking its well-formedness occurs
in constant-time; ii. the MAC of the unpadded message is always computed, even
for bad padding; iii. the MAC computation involves the same number of calls
to the underlying compression function regardless of the number of hash input
blocks in the decoded message, and regardless of the length of the ﬁnal hash
block (which may cause an additional block to be computed due to the internal
Merkle-Damgård length padding); and iv. the transmitted MAC is compared to
the computed MAC in constant-time (the transmitted MAC’s location in mem-
ory, which may be leaked through the timing of memory accesses, depends on
the plaintext length).Constant-time, here and in the rest of this paper, is used to
mean that the trace of program points and memory addresses accessed during
the execution is independent from the initial value of secret inputs. In particu-
lar, we note that the OpenSSL MEE-CBC implementation is not constant time
following this deﬁnition: the underlying AES implementation uses look-up table
optimizations that make secret-dependent data memory accesses and may open
the way to cache-timing attacks.
Our Implementation. The main result of this paper is a security theorem
for an x86 assembly implementation of MEE-CBC (MEE-CBCx86 ). The imple-
mentation is compiled using CompCert from standard C code that replicates the
countermeasures against timing attacks currently implemented in the OpenSSL
library [23]. We do not use the OpenSSL code directly because the code style of
the library (and in particular its lack of modularity) makes it a diﬃcult target for
veriﬁcation. Furthermore, we wish to fully prove constant-time security, which
we have noted is not achieved by OpenSSL. However, a large part of the code we
verify is existing code, taken from the NaCl library [14] without change (for AES,
SHA256 and CBC mode), or modiﬁed to include the necessary countermeasures
(HMAC, padding and MEE composition). Our C code is composed of the fol-
lowing modules, explicitly named for later reference: i. AES128NaCl contains the
NaCl implementation of AES128; ii. HMACSHA256NaCl contains a version of the
NaCl implementation of HMAC-SHA256 extended with timing countermeasures
mimicking those described in [23]; and iii. MEE-CBCC contains an implementa-
tion of MEE-CBC using AES128NaCl and HMACSHA256NaCl . We do not include
the code in the paper due to space constraints.
    As we prove later in the paper, a strict adherence to the coding style adopted
in OpenSSL is indeed suﬃcient to guarantee security against attackers that, in
addition to input/output interaction with the MEE-CBC implementation, also
obtain full traces of program counter and memory accesses performed by the
implementation. However, not all TLS implementations have adopted a strict
adherence to constant-time coding policies in the aftermath of the Lucky 13
attack. We now brieﬂy present the case of Amazon’s s2n library, discussing their
choice of countermeasures, and describing a bug in their implementation that
leads to an attack. A more detailed discussion can be found in the long version
of this paper.
170      J.B. Almeida et al.

Breaking the MEE-CBC implementation in s2n. Although parts of the
s2n code for MEE-CBC are written in the constant-time style, there are many
(intentional) deviations from a strict constant-time coding policy. For example,
no attempt is made to de-correlate memory accesses from the padding length
value that is recovered from the decrypted (but not yet validated) plaintext. As
an alternative, the code includes countermeasures that intend to balance the
execution time of secret-dependent conditional branches that might lead to sig-
niﬁcant variability in the execution time. Roughly, the goal of these countermea-
sures is to ensure that the total number of calls to the hash compression function
is always the same, independently of the actual padding length or validity.
    The bug we found resides in a special routine that aims to guarantee that
a dummy compression function computation is performed whenever particular
padding patterns might lead to shorter execution times. An oﬀ-by-one error
in the checking of a boundary condition implied that the dummy compression
function would be invoked unnecessarily for some padding values (more precisely,
there are exactly 4 such padding values, which are easily deduced from the
(public) length of the encrypted record).
    The leakage the bug produces is similar in size to that exploited by AlFardan
and Paterson [2] to recover plaintexts. We have implemented a padding-oracle-
style attack on the MEE-CBC decryption routine to recover single plaintext
bytes from a ciphertext: one simply measures the decryption time to check if
the recovered padding length causes the bug to activate and proceeds by trial
and error.8 The attack can be extended to full plaintext recovery using the same
techniques reported in [2].
    We already discussed the real-world impact of our attack and our disclosure
interaction with AWS Labs in the introduction of this paper. However, we insist
that for the purpose of this paper it is not the real-world impact of our attack
that matters, but the software bug that gave rise to it in the ﬁrst place. Indeed
the existence of such a programming bug and the fact that it remained unde-
tected through AWS Labs’ code validation process (and in particular despite unit
testing speciﬁcally designed to detect timing side-channels) reveal that there is
a need for a formal framework in which to rigorously prove that an implemen-
tation is secure against timing attacks. This is what we set out to do in the rest
of the paper.


3     Security Definitions and Main Theorem
After a brief reminder of the syntax and security notions for secret key encryp-
tion relevant to our case study, we introduce and discuss the corresponding
implementation-level security notions for the constant-time leakage model and
state our main theorem. Cryptographic implementations are often hardwired at
a particular security level, which means that asymptotic security notions are not
adequate to capture the security guarantees provided by software. We therefore
8
    Plaintext recovery is easier than in Lucky 13, since leakage occurs whether or not
    the padding string is correct.
         Veriﬁable Side-Channel Security of Cryptographic Implementations      171

omit the security parameter in all our deﬁnitions. For simplicity we also keep the
running time of algorithms implicit in our notations, although we take care to
account for it in our security proofs and to show that there is no hidden slackness
in our reductions.


3.1   Secret Key Encryption
We recall that a secret-key encryption scheme Π = (Gen, Enc, Dec) is speciﬁed
as three algorithms: i. a probabilistic key generation algorithm Gen(; r) that
returns a secret key SK on input some random coins r; ii. a probabilistic encryp-
tion algorithm Enc(m, SK; r) that returns a ciphertext c on input a message m,
the secret key SK, and some random coins r; and iii. a deterministic decryption
algorithm Dec(c, SK) that returns either a message m or a failure symbol ⊥ on
input a ciphertext c and secret key SK. We denote the set of valid messages with
MsgSp and adopt standard notions of correctness, conﬁdentiality (IND$-CPA)
and integrity (INT-PTXT and INT-CTXT) for authenticated symmetric encryp-
tion schemes.
    Our goal in the rest of this section is to adapt these standard notions to
formally capture implementation-level security. In particular, we wish to give
the adversary the ability to observe the leakage produced by the computation of
its oracle queries. We ﬁrst give generic deﬁnitions for some core concepts.


3.2   Implementation: Languages, Leakage and Generation

For the sake of generality, our deﬁnitions abstract the concrete implementation
languages and leakage models adopted in our case study. We later instantiate
these deﬁnitions with a black-box security model for C implementations and a
timing leakage model for x86 assembly implementations.
Language, leakage and machine. Given an implementation language L,
we consider a machine M that animates its semantics. Such a machine takes
as input a program P written in L, an input i for P , and some randomness r
and outputs both the result o of evaluating P with i and r, and the leakage 
produced by the evaluation. We use the following notation for this operation
o ← M(P, i; r)  . We make the assumption that the machine is deterministic,
so that all randomness required to execute programs is given by the input r.
However, our security experiments are probabilistic, and we write o←$ M(P, i) 
to denote the probabilistic computation that ﬁrst samples the random coins r
that must be passed as randomness input of P , and then runs M(P, i; r). This
approach agrees with the view that the problem of randomness generation is
orthogonal to the one of secure implementation [14]. We discuss this further in
Sect. 7.
    We note that the deﬁnition of M makes three implicit assumptions. First, the
semantics of a program must always be deﬁned, since M always returns a result;
termination issues can be resolved easily by aborting computations after a ﬁxed
number of steps. Second, our view of M does not allow an adversary to inﬂuence
172    J.B. Almeida et al.

a program’s execution other than through its queries. Finally, our model implies
that the semantics of L can be equipped with meaningful notions of leakage. In
the context of our use case, we adopt the common view of practical cryptography
that timing leakage can be captured via the code-memory and data-memory
accesses performed while executing a program. These can be sensibly formalized
over assembly implementations, but not over higher-level implementations (e.g.,
over C implementations), not least because there is no guarantee that optimizing
compilers do not introduce leakage. For this reason, in our case study, we consider
the following two implementation models:

– a C-level model using a machine M∅C (or simply MC ) that animates the C
  language semantics with no leakage;
– an assembly-level model using a machine MCTx86 that animates (a subset of)
  the x86 assembly language, and produces leakage traces in the constant-time
  leakage model as detailed below.

In both languages, we adopt the semantic deﬁnitions as formalized in the Com-
pCert certiﬁed compiler.
Constant-time leakage traces. Formally, we capture the constant-time
leakage model by assuming that each semantic step extends the (initially empty)
leakage trace with a pair containing: i. the program point corresponding to the
statement being executed; and ii. the (ordered) sequence of memory accesses
performed during the execution step. We specify when this particular leakage
model is used by annotating the corresponding notion with the symbol CT.

3.3   Authenticated Encryption in the Implementation Model
Given a language L and a (potentially leaking) machine M animating its seman-
tics, we now deﬁne M-correctness, M-IND$-CPA and M-INT-PTXT security for
L-implementations of SKE schemes in the leakage model deﬁned by M. In what
follows, we let Π∗ = (Gen∗ , Enc∗ , Dec∗ ) be an SKE implementation in language L.
SKE implementation correctness. We say that Π∗ is M-correct if, for all
m ∈ MsgSp, random coins rgen , renc , and SK = M(Gen∗ ; rgen ), we have that

                     M(Dec∗ , M(Enc∗ , m, SK; renc ), SK) = m .

SKE implementation security. The M-IND$-CPA advantage of an adversary
A against Π∗ and public length function φ is deﬁned as the following (concrete)
diﬀerence
                                                        
  AdvM  -ind$-cpa := 
       Π∗ ,φ,A       Pr M-IND$-CPAA  Π∗ ,φ (Real) ⇒ true
                                                                             
                                                                               
                                   − Pr M-IND$-CPAA       Π∗ ,φ (Ideal) ⇒ true  ,

where implementation-level game M-IND$-CPA is shown in Fig. 1. Here, public
length function φ is used to capture the fact that SKEs may partially hide the
            Veriﬁable Side-Channel Security of Cryptographic Implementations                          173

  Game M-IND$-CPAA
                 Π∗ ,φ (b):       proc. RoR(m):                             proc. Dec(c):
  SK ←$ M(Gen∗ )g               c ←$ M(Enc∗ , m, SK)e                   m ← M(Dec∗ , c, SK)d
  b ←$ ARoR,Dec (g )            If (b = Ideal) Then c ←$ {0, 1}φ(|m|)     Return (⊥, d )
  Return (b = b)                 Return (c, e )



                              Fig. 1. M-IND$-CPA experiment.

  Game M-INT-PTXTA   Π∗ :         proc. Enc(m):                           proc. Ver(c):
  List ← []; win ← ⊥              c ←$ M(Enc∗ , m, SK)e                 m ← M(Dec∗ , c, SK)d
  SK ←$ M(Gen∗ )g               List ← m : List                         win ← win ∨ (m = ⊥ ∧ m ∈
                                                                                                  / List)
  AEnc,Ver (g )                  Return (c, e )                         Return (m = ⊥, d )
  Return win



                              Fig. 2. M-INT-PTXT experiment.


length of a message. If φ is the identity function or is eﬃciently invertible, then
the message length is trivially leaked by the ciphertext. In the case of our MEE-
CBC speciﬁcation, for example, the message length is revealed only up to AES
block alignment.
    We observe that in this reﬁnement of the IND$-CPA security notion for imple-
mentations, the adversary may learn information about the secrets via the leak-
age produced by the decryption oracle Dec∗ , even if its functional input-output
behaviour reveals nothing. In particular, in a black-box adversary model where
leakage traces are always empty, the Dec oracle can be perfectly implemented by
the procedure that ignores its argument and returns (⊥, ), and the RoR oracle
can be simulated without any dependency on m in the Ideal world; this allows
us to recover the standard computational security experiment for IND$-CPA. On
the other hand, in models where leakage traces are not always empty, the adver-
sary is given the ability to use the decryption oracle with invalid ciphertexts and
recover information through its leakage output.
    We extend standard INT-PTXT security in a similar way and deﬁne the
M-INT-PTXT advantage of an adversary A against Π∗ as the following (con-
crete) probability:
                                                                  
                     M-int-ptxt
                AdvΠ   ∗ ,A     := Pr M-INT-PTXTA    Π ∗ () ⇒ true   ,

where implementation-level game M-INT-PTXT is shown in Fig. 2.
   We similarly “lift” INT-CTXT, PRP (pseudorandomness of a permutation)
and UF-CMA (existential MAC unforgeability) security experiments and advan-
tages to implementations. This allows us to state our main theorem.

3.4    Main Theorem
The proof of Theorem 1 is fully machine-checked. However, foregoing machine-
checking of the speciﬁcation’s security theorems allows us to strengthen the
results we obtain on the ﬁnal implementations. We discuss this further after we
present our proof strategy.
174    J.B. Almeida et al.

Theorem 1 (CT security of MEE-CBCx86 ). MEE-CBCx86 is MCT         x86 -correct and
provides MCT
          x86 -IND$-CPA and  M  CT
                                x86 -INT-PTXT    security if the underlying  com-
ponents AES128NaCl and HMACSHA256NaCl are black-box secure as a PRP and
a MAC, respectively. More precisely, let φ(i) = (i + 1)/16 + 3, then
– For any MCT x86 -IND$-CPA adversary A
                                          cpa
                                              that makes at most q queries to
  its RoR oracle, each of length at most n octets, there exists an (explicitly
  constructed) M∅C -IND$-CPA adversary B prp that makes at most q·(n+1)/16+
  2 queries to its forward oracle and such that

             x86 -ind$-cpa
            MCT                       M∅
                                       C -prp
                                                              (q · ( n+1
                                                                       16  + 2))
                                                                                 2
         AdvMEE -CBCx86 ,φ,Acpa ≤ Adv AES128NaCl ,B prp + 2 ·                      .
                                                                       2128
– For any MCTx86 -INT-PTXT adversary A
                                        ptxt
                                             that makes at most qE queries to
  its Enc oracle and qV queries to its Ver oracle, there exists an (explicitly
  constructed) M∅C -UF-CMA adversary B cma that makes at most qE queries to
  its Tag oracle and qV queries to its Ver oracle and such that

                        x86 -int-ptxt
                       MCT                     M∅
                                                C -uf -cma
                    AdvMEE -CBCx86 ,Aptxt ≤ AdvHMACSHA256NaCl ,Bcma .
    In addition, the running time of our constructed adversaries is essentially
that of running the original adversary plus the time it takes to emulate the
leakage of the x86 implementations using dummy executions in machine Mx86 .
Under reasonable assumptions on the eﬃciency of Mx86 , this will correspond to
an overhead that is linear in the combined inputs provided by an adversary to
its oracles (the implementations are proven to run in constant time under the
semantics of L when these inputs are ﬁxed).
    Note that the security assumptions we make are on C implementations of
AES (AES128NaCl ) and HMAC-SHA256 (HMACSHA256NaCl ). More importantly,
they are made in a black-box model of security where the adversary gets empty
leakage traces.
    The proof of Theorem 1 is detailed in Sect. 5 and relies on the general frame-
work we now introduce. Rather than reasoning directly on the semantics of the
executable x86 program (and placing our assumptions on objects that may not
be amenable to inspection), we choose to prove complex security properties on
a clear and simple functional speciﬁcation, and show that each of the reﬁnement
steps on the way to an x86 assembly executable preserves this property, or even
augments it in some way.


4     Formal Framework and Connection to PL Techniques
Our formal proof of implementation security follows from a set of conditions
on the software development process. We therefore introduce the notion of an
implementation generation procedure.
Implementation generation. An implementation generation procedure
C L1 →L2 is a mapping from speciﬁcations in language L1 to implementations in
          Veriﬁable Side-Channel Security of Cryptographic Implementations       175


           Game CorrA
                    M,Π,C ():                  proc. Eval(k, i, r):
           bad ← false                         o ← Π[k](i; r)
           Π∗ ← C(Π)                           o ← M(Π∗ [k], i; r)
           AEval (Π∗ )                         If o = o then bad = true
           Return ¬ bad


Fig. 3. Game deﬁning correct implementation generation. For compactness, we use
notation Π[k] (resp. Π∗ [k]) for k ∈ {1, 2, 3} to denote the k-th algorithm in scheme
Π (resp. implementation Π∗ ), corresponding to key generation (1), encryption (2) and
decryption (3).


language L2 . For example, in our use case, the top-level speciﬁcation language
is the expression language LEC of EasyCrypt (a polymorphic and higher-order
λ-calculus) and the overall implementation generation procedure C LEC →Lx86 is
performed by a veriﬁed manual reﬁnement of the speciﬁcation into C followed
by compilation to x86 assembly using CompCert (here, Lx86 is the subset of x86
assembly supported by CompCert).
    We now introduce two key notions for proving our main result: correct imple-
mentation generation and leakage security, which we relate to standard notions
in the domain of programming language theory. This enables us to rely on exist-
ing formal veriﬁcation methods and tools to derive intermediate results that are
suﬃcient to prove our main theorem. In our deﬁnitions we consider two arbitrary
languages L1 and L2 , a (potentially leaking) machine M animating the seman-
tics of the latter, and an implementation generation procedure C L1 →L2 . In this
section, L1 and L2 are omitted when denoting the implementation generation
procedure (simply writing C instead). In the rest of the paper, we also omit them
when clear from context.
Correct implementation generation. Intuitively, the minimum require-
ment for an implementation generation procedure is that it preserves the input-
output functionality of the speciﬁcation. We capture this in the following
deﬁnition.

Definition 1 (Correct implementation generation). The implementation
generation procedure C is correct if, for every adversary A and primitive speci-
fication Π, the game in Fig. 3 always returns true.

    For the programming languages we are considering (deterministic, I/O-free
languages) this notion of implementation generation correctness is equivalent
to the standard language-based notion of simulation, and its specialization
as semantic preservation when associated with general-purpose compilers. A
notable case of this is CompCert [24] for which this property is formally proven
in Coq. Similarly, as we discuss in Sect. 5, a manual reﬁnement process can be
turned into a correct implementation generation procedure by requiring a total
functional correctness proof. This is suﬃcient to guarantee black-box implemen-
tation security. However, it is not suﬃcient in general to guarantee implementa-
tion security in the presence of leakage.
176       J.B. Almeida et al.

Leakage security. In order to relate the security of implementations to that
of black-box speciﬁcations, we establish that leakage does not depend on secret
inputs. We capture this intuition via the notion of leakage security, which imposes
that all the leakage produced by the machine M for an implementation is benign.
Interestingly from the point of view of formal veriﬁcation, leakage security is
naturally related to the standard notion of non-interference [19]. In its simplest
form, non-interference is formulated by partitioning the memory of a program
into high-security (or secret) and low-security (or public) parts and stating that
two executions that start in states that agree on their low-security partitions
end in states that agree on their low-security partitions.
    We deﬁne what the public part of the input means by specifying a function
τ that parametrizes our deﬁnition of leakage security. For the case of symmetric
encryption, for example, τ is deﬁned to tag as public the inputs to the algorithms
an attacker has control over through its various oracle interfaces (in IND$-CPA,
INT-PTXT and INT-CTXT). More precisely, we deﬁne a speciﬁc projection func-
tion τSKE as follows:
    τSKE (Gen) =      τSKE (Enc, key, m) = (|key|, |m|)   τSKE (Dec, key, c) = (|key|, c)

 Our deﬁnition of leakage security then consists in constraining the information-
ﬂow into the leakage due to each algorithm, via the following non-interference
notion.9
Definition 2 ((M, τ )-non-interference). Let P be a program in L2 and τ be
a projection function on P ’s inputs. Then, P is (M, τ )-non-interferent if, for
any two executions o ← M(P, i; r)  and o ← M(P, i ; r )  , we have τ (P, i) =
τ (P, i ) ⇒  =  .
Intuitively, (M, τ )-non-interference labels the leakage  as a public output (which
must be proved independent of secret information), whereas τ is used to specify
which inputs of P are considered public. By extension, those inputs that are not
revealed by τ are considered secret, and are not constrained in any way during
either executions. Note that the leakage produced by a (M, τ )-non-interferent
program for some input i can be predicted given only the public information
revealed by τ (P, i): one can simply choose the remaining part of the input arbi-
trarily, constructing some input i such that τ (P, i) = τ (P, i ). In this case,
(M, τ )-non-interference guarantees that the leakage traces produced by M when
executing P on i and i are equal.
    We can now specialize this notion of leakage security to symmetric
encryption.
Definition 3 (Leakage-secure implementation generation for SKE).
An implementation generation procedure C produces M-leakage-secure implemen-
tations for SKE if, for all SKE specifications Π written in L1 , we have that
the generated L2 implementation (Gen∗ , Enc∗ , Dec∗ ) = C(Π) is (M, τSKE )-non-
interferent.
9
    For simplicity, the length of random inputs is assumed to be ﬁxed by the algorithm
    itself.
         Veriﬁable Side-Channel Security of Cryptographic Implementations      177

Putting the pieces together. The following lemma, shows that applying a
correct and leakage secure implementation generation procedure to a black-box
secure SKE speciﬁcation is suﬃcient to guarantee implementation security.

Theorem 2. Let C be correct and produce M-leakage-secure implementations.
Then, for all SKE scheme Π that is correct, IND$-CPA-, INT-PTXT- and
INT-CTXT-secure, the implementation Π∗ = C(Π) is M-correct, M-IND$-CPA-,
M-INT-PTXT- and M-INT-CTXT-secure with the same advantages.

Proof. Correctness of Π∗ follows directly from that of C and Π. The security
proofs are direct reductions. We only detail the proof of M-IND$-CPA, but note
that a similar proof can be constructed for M-INT-PTXT and M-INT-CTXT.
Given an implementation adversary A, we construct an adversary B against Π
as follows. Adversary B runs Gen∗ on an arbitrary randomness of appropriate
size to obtain the leakage Gen associated with key generation and runs adversary
A on Gen . Oracle queries made by A are simulated by using B’s speciﬁcation
oracles to obtain outputs, and the same leakage simulation strategy to present
a perfect view of the implementation leakage to A. When A outputs its guess,
B forwards it as its own guess. We now argue that B’s simulation is perfect.
The ﬁrst part of the argument relies on the correctness of the implementation
generation procedure, which guarantees that the values obtained by B from its
oracles in the CPA-game are identically distributed to those that A would have
received in the implementation game. The second part of the argument relies
on the fact that leakage-secure implementation generation guarantees that B
knows enough about the (unknown) inputs to the black-box algorithms (the
information speciﬁed by τSKE ) to predict the exact leakage that such inputs
would produce in the implementation model. Observe for example that, in the
case of decryption leakage, the adversary B only needs the input ciphertext c to
be able to exactly reproduce the leakage Dec . Finally, note that the running time
of the constructed adversary B is that of adversary A where each oracle query
A introduces an overhead of one execution of the implementation in machine M
(which can reasonably be assumed to be close to that of the speciﬁcation).


5   Implementation Security of MEE-CBC
We now return to our case study, and explain how to use the methodology from
Sect. 4, instantiated with existing veriﬁcation and compilation tools, to derive
assembly-level correctness and security properties for MEE-CBCx86 .
Proof strategy. We ﬁrst go brieﬂy over each of the steps in our proof strategy,
and then detail each of them in turn in the remainder of this section. In the
ﬁrst step, we specify and verify the correctness and black-box computational
security of the MEE-CBC construction using EasyCrypt. In a second step, we
use Frama-C to prove the functional correctness of program MEE-CBCC with
respect to the EasyCrypt speciﬁcation. Finally, we focus on the x86 assembly code
generated by CompCert (MEE-CBCx86 ), and prove: i. its functional correctness
178       J.B. Almeida et al.

with respect to the C code (and thus the top-level EasyCrypt speciﬁcation); and
ii. its leakage security. An instantiation of Theorem 2 allows us to conclude the
proof of Theorem 1.
Black-box specification security. We use EasyCrypt to prove that the
MEE-CBC construction provides IND$-CPA security (when used with freshly
and uniformly sampled IVs for each query) and INT-PTXT security.

Lemma 1 (Machine-checked MEE-CBC security).                    The following two
results hold:

 – For all legitimate IND$-CPA adversary Acpa that makes at most q queries,
   each of length at most n octets, to its RoR oracle, there exists an explicitly
   constructed PRP adversary B prp that makes q · (n + 1) / λ + 2 queries to its
   forward oracle and such that:
                                                          
                       ind$-cpa      prp          (q · n+1
                                                        λ    + 2)2
                  AdvΠ,φ,A ≤ AdvPerm,Bprp + 2 ·                    ,
                                                        28·λ
   where φ(i) = (i + 1) / λ+3 reveals only the number of blocks in the plaintext
   (and adds to it the fixed number of blocks due to IV and MAC tag).
 – For all PTXT adversary A that makes qV queries to its Dec oracle, there
   exists an explicitly constructed SUF-CMA adversary B cma that makes exactly
   qV queries to its Ver oracle and such that:
                                    int-ptxt         -cma
                                 AdvΠ,A      ≤ Advuf
                                                  Mac,Bcma .

    Our EasyCrypt speciﬁcation relies on abstract algorithms for the primitives.
More precisely, it is parameterized by an abstract, stateless and deterministic
block cipher Perm with block size λ octets, and by an abstract, stateless and
deterministic MAC scheme Mac producing tags of length 2 · λ.10 The proofs, for-
malized in EasyCrypt, are fairly standard and account for all details of padding
and message formatting in order to obtain the weak length-hiding property
shown in this lemma. Running times for B prp and B cma are as usual.
    We note that, although we have not formalized in EasyCrypt the proof of
INT-CTXT security (this would imply a signiﬁcant increase in interactive theo-
rem proving eﬀort) the known security results for MEE-CBC also apply to this
speciﬁcation and, in particular, it follows from [26] that it also achieves this
stronger level of security when the underlying MAC and cipher satisfy slightly
stronger security requirements.
implementation generation. Using Frama-C, a veriﬁcation platform for C
programs,11 we prove functional equivalence between the EasyCrypt speciﬁcation
and our C implementation. Speciﬁcally, we use the deductive veriﬁcation (WP)
plugin to check that our C code fully and faithfully implements a functionality
described in the ANSI/ISO C Speciﬁcation Language (ACSL). To make sure
10
     This is only for convenience in these deﬁnitions.
11
     http://frama-c.com/.
            Veriﬁable Side-Channel Security of Cryptographic Implementations           179

that the ACSL speciﬁcation precisely corresponds to the EasyCrypt speciﬁcation
on which black-box security is formally proved, we rely on Frama-C’s ability to
link ACSL logical constructs at the C annotation level to speciﬁc operators in
underlying Why3 theories, which we formally relate to those used in the Easy-
Crypt proof. This closes the gap between the tools by allowing us to refer to a
common speciﬁcation. Note that, since the abstract block cipher Perm and MAC
scheme Mac are concretely instantiated in the C implementation, we instantiate
λ = 16 (the AES block length in bytes) in this common speciﬁcation and lift the
assumptions on Perm and Mac to the C implementation of their chosen instan-
tiation. We then use the CompCert certiﬁed compiler [24] to produce our ﬁnal
x86 assembly implementation.
    To prove leakage security, we use the certifying information-ﬂow type sys-
tem for x86 built on top of CompCert [4], marking as public those inputs that
correspond to values revealed by τSKE . Obtaining this proof does not put any
additional burden on the user—except for marking program inputs as secret
or public. However, the original C code must satisfy a number of restrictions in
order to be analyzed using the dataﬂow analysis from [4]. Our C implementations
were constructed to meet these restrictions, and lifting them to permit a wider
applicability of our techniques is an important challenge for further work.12

Proof of Theorem 1. Let us denote by C LEC →x86 the implementation gener-
ation procedure that consists of hand-crafting a C implementation (annotated
with τSKE consistent security types), equivalence-checking it with an EasyCrypt
speciﬁcation using Frama-C, and then compiling it to assembly using CompCert
(accepting only assembly implementations that type-check under the embedded
secure information-ﬂow type system), as we have done for our use case. We
formalize the guarantees provided by this procedure in the following lemma.

Lemma 2 (Implementation generation). C LEC →x86 is a MCT        x86 -correct imple-
mentation generation procedure that produces MCT
                                              x86 -leakage secure SKE implemen-
tations.

Proof. Correctness follows from the combination of the Frama-C functional cor-
rectness proof and the semantic preservation guarantees provided by CompCert.
CompCert’s semantics preservation theorem implies that the I/O behaviour of
the assembly program exactly matches that of the C program. Functional equiv-
alence checking using Frama-C yields that the C implementation has an I/O
behaviour that is consistent with that of the EasyCrypt speciﬁcation (under the
C semantics adopted by Frama-C). Finally, under the reasonable assumption that
12
     In a recent development in this direction, Almeida et al. [3] describe a method, based
     on limited product programs, for verifying constant-time properties of LLVM code.
     Their method and the implementation they describe can deal with many examples
     that the type system from [4] cannot handle, including a less ad hoc version of our
     code and some of the OpenSSL code for MEE-CBC, whilst preserving a high degree
     of automation. In addition, their construction easily extends to situations where
     public outputs are needed to simulate the leakage trace.
180       J.B. Almeida et al.

the CompCert semantics of C are a sound reﬁnement of those used in Frama-C,
we obtain functional correctness of the assembly implementation with respect
to the EasyCrypt speciﬁcation. For leakage security, we rely on the fact that the
information-ﬂow type system of [4] enforces τSKE -non-interference and hence only
           x86 , τSKE )-leakage secure implementations.
accepts (MCT

    Theorem 1 follows immediately from the application of Theorem 2 instan-
tiated with Lemmas 1 and 2. Furthermore, foregoing machine-checking of the
black-box speciﬁcation security proof and simply accepting known results on
MEE-TLS-CBC [26], we can also show that MEE-CBCx86 is MCT    x86 -INT-CTXT-
secure under slightly stronger black-box assumptions on AES128NaCl and
HMACSHA256NaCl .


6      Performance Comparison
We now characterize the diﬀerent assurance/performance trade-oﬀs of the tim-
ing mitigation strategies discussed in this paper. Figure 4 shows the time taken
by 5 diﬀerent implementations of MEE-CBC (one of them compiled in diﬀer-
ent ways) when decrypting a 1.5KB TLS1.2 record using the AES128-SHA256
ciphersuite.13 More speciﬁcally, we consider code from s2n (#1) and OpenSSL
(#2), and ﬁve diﬀerent compilations of our formally veriﬁed MEE-CBC imple-
mentation (#3-7), focusing on raw invocations of MEE-CBC. It is clear that
the s2n code (#1) beneﬁts from its less strict timing countermeasures, gaining
roughly 1.8× performance over OpenSSL’s (semi-)constant-time implementation
approach (#2). The ﬁgures for our veriﬁed implementation of MEE-CBC show
both the cost of formal veriﬁcation and the cost of full constant-time guarantees.
Indeed, the least eﬃcient results are obtained when imposing full code and data
memory access independence from secret data (#4-6).


            #   Implementation          Compiler       Clock Cycles   Time
            1   s2n                  GCC x86-64 -O2        14K         5µs
            2   OpenSSL              GCC x86-64 -O2        23K         9µs
            3   MEE-CBCC (AES-NI)    CompCert x86-32       51K        21µs
            4   MEE-CBCC             GCC x86-64 -O2        59M        25ms
            5   MEE-CBCC             GCC x86-64 -O1        62M        26ms
            6   MEE-CBCx86           CompCert x86-32      101M        42ms
            7   MEE-CBCC             GCC x86-64 -O0       237M        99ms

Fig. 4. Performance comparison of various MEE-CBC implementations. (Median over
500 runs.)




13
     The numbers were obtained in a virtualized Intel x86-64 Linux machine with 4 GB
     RAM.
            Veriﬁable Side-Channel Security of Cryptographic Implementations   181

    The assembly implementation produced using the constant-time version of
CompCert (#6), is roughly 8400× slower than s2n, but still over twice as fast as
unoptimized GCC. However, the fact that the same C code compiled with GCC
-O2 (#4) is only 1.7× faster14 than the fully veriﬁed CompCert-generated code
shows that the bottleneck does not reside in veriﬁcation, but in the constant-
time countermeasures. Indeed, proﬁling reveals that NaCl’s constant-time AES
accounts for 97 % of the execution time. These results conﬁrm the observations
made in [12] as to the diﬃculties of reconciling resistance against cache attacks
and eﬃciency in AES implementations. To further illustrate this point, we also
include measurements corresponding to a modiﬁcation of our MEE-CBC imple-
mentation that uses hardware-backed AES (#3). This cannot, in fairness, be
compared to the other implementations, but it does demonstrate that, with cur-
rent veriﬁcation technology, the performance cost of a fully veriﬁed constant-time
MEE-CBC implementation is not prohibitive.


7      Discussions

On randomness. Restricting our study to deterministic programs with an argu-
ment containing random coins does not exclude the analysis of real-world sys-
tems. There, randomness is typically scarce and pseudorandom generators are
used to expand short raw high-entropy bitstrings into larger random-looking
strings that are fed to deterministic algorithms, and it is common to assume
that the small original seed comes from an ideal randomness source, as is done
in this paper. Our approach could therefore be used to analyze the entire pseudo-
random generation implementation, including potential leakage-related vulner-
abilities therein.
On length-hiding security. Existing implementations of MEE-TLS-CBC
(and indeed our own implementation of MEE-CBC) are not length-hiding as
deﬁned in [26] in the presence of leakage. Indeed, the constant-time countermea-
sures are only applied in the decryption oracle and precise information about
plaintext lengths may be leaked during the execution of the encryption ora-
cle. Carrying length-hiding properties down to the level of those implementa-
tions may therefore require, either the implementation to be modiﬁed (and the
Frama-C equivalence proof adapted accordingly), or the speciﬁcation of imple-
mentation security to more closely reﬂect particular scenarios–such as the TLS
record layer–where it may be diﬃcult for the adversary to make chosen-plaintext
queries, but easy to make padding and veriﬁcation oracle queries. In any case,
Lemma 1 does capture the length-hiding property given by our choice of min-
imal padding, and could be adapted to capture the more general length-hiding
property of Paterson, Ristenpart and Shrimpton [26] by making padding length
a public choice.


14
     This is in line with general CompCert benchmarks.
182       J.B. Almeida et al.

Leakage simulation and weaker non-interference notions. Our use
of leakage security in proving that leakage is not useful to an adversary natu-
rally generalizes to a notion of leakage simulation, whereby an implementation
is secure as long as its leakage can be eﬃciently and perfectly simulated from
its public I/O behaviour, including its public outputs. For example, an imple-
mentation of Encrypt-then-MAC that aborts as soon as MAC veriﬁcation fails,
but is otherwise fully constant-time should naturally be considered secure,15
since the information gained through the leakage traces is less than that gained
by observing the output of the Ver oracle. The more general notion of leakage
simulation informally described here would capture this and can be related to
weaker notions of non-interference, where equality on low outputs is only required
on traces that agree on the value of public outputs. Theorem 2 can be modi-
ﬁed to replace leakage security with the (potentially weaker) leakage simulation
hypothesis.


8      Conclusions and Directions for Future Work

Our proposed methodology allows the derivation of strong security guarantees
on assembly implementations from more focused and tractable veriﬁcation tasks.
Each of these more specialized tasks additionally carries its own challenges.
    Proving security in lower-level leakage models for assembly involves consid-
ering architectural details such as memory management, scheduling and data-
dependent and stateful leakage sources. Automatically relating source and exist-
ing assembly implementations requires developing innovative methods for check-
ing (possibly conditional or approximate) equivalences between low-level prob-
abilistic programs. Finally, obtaining formal proofs of computational security
and functional correctness in general remain important bottlenecks in the proof
process, requiring high expertise and eﬀort. However, combining formal and
generic composition principles (such as those used in our case study) with tech-
niques that automate these two tasks for restricted application domains [5,11,20]
should enable the formal veriﬁcation of extensive cryptographic libraries, in the
presence of leakage. We believe that this goal is now within reach.
    On the cryptographic side, the study of computational security notions that
allow the adversary to tamper with the oracle implementation [10] may lead
to relaxed functional correctness requirements that may be easier to check, for
example by testing. Extensions of our framework to settings where the adversary
has the ability to tamper with the execution of the oracle are possible, and would
allow it to capture recent formal treatments of countermeasures against fault
injection attacks [27].



15
     Some anonymity properties, such as untraceability, may require the cause of decryp-
     tion failure to remain secret in the black-box model, in which case leakage must not
     reveal it either [17].
          Veriﬁable Side-Channel Security of Cryptographic Implementations         183

Acknowledgements. The ﬁrst two authors were funded by Project “TEC4Growth -
Pervasive Intelligence, Enhancers and Proofs of Concept with Industrial Impact/
NORTE-01-0145-FEDER-000020”, which is ﬁnanced by the North Portugal Regional
Operational Programme (NORTE 2020), under the PORTUGAL 2020 Partnership
Agreement, and through the European Regional Development Fund (ERDF). The
third and fourth authors were supported by projects S2013/ICE-2731 N-GREENS
Software-CM and ONR Grants N000141210914 (AutoCrypt) and N00014151 2750
(SynCrypt). The fourth author was supported by FP7 Marie Cure Actions-COFUND
291803 (Amarout II). The machine-checked proof for CBC improves on a script by
Benjamin Grégoire and Benedikt Schmidt. Pierre-Yves Strub provided support for
extracting Why3 deﬁnitions from EasyCrypt speciﬁcations. We thank Mathias Pedersen
and Bas Spitters for useful comments.


References
 1. Albrecht, M.R., Paterson, K.G.: Lucky microseconds: a timing attack on Amazon’s
    s2n implementation of TLS. Cryptology ePrint Archive, report 2015/1129 (2015).
    http://eprint.iacr.org/
 2. AlFardan, N.J., Paterson, K.G.: Lucky thirteen: breaking the TLS and DTLS
    record protocols. In: IEEE Symposium on Security and Privacy SP 2013, pp. 526–
    540. IEEE Computer Society (2013)
 3. Almeida, J., Barbosa, M., Barthe, G., Dupressoir, F., Emmi, M.: Verifying
    constant-time implementations. Manuscript (2015). https://fdupress.net/ﬁles/
    ctverif.pdf
 4. Barthe, G., Betarte, G., Campo, J.D., Luna, C.D., Pichardie, D.: System-level
    non-interference for constant-time cryptography. In: Ahn, G.-J., Yung, M., Li, N.
    (eds.) ACM CCS 2014, pp. 1267–1279. ACM Press, November 2014
 5. Barthe, G., Crespo, J.M., Grégoire, B., Kunz, C., Lakhnech, Y., Schmidt, B.,
    Béguelin, S.Z.: Fully automated analysis of padding-based encryption in the com-
    putational model. In: Sadeghi, A.-R., Gligor, V.D., Yung, M. (eds), ACM CCS
    2013, pp. 1247–1260. ACM Press, November 2013
 6. Barthe, G., Dupressoir, F., Grégoire, B., Kunz, C., Schmidt, B., Strub, P.-Y.:
    EasyCrypt: a tutorial. In: Aldini, A., Lopez, J., Martinelli, J. (eds.) FOSAD 2013,
    pp. 146–166. Springer, Heidelberg (2014)
 7. Barthe, G., Grégoire, B., Heraud, S., Béguelin, S.Z.: Computer-aided security
    proofs for the working cryptographer. In: Rogaway, P. (ed.) CRYPTO 2011. LNCS,
    vol. 6841, pp. 71–90. Springer, Heidelberg (2011)
 8. Barwell, G., Page, D., Stam, M.: Rogue decryption failures: reconciling AE robust-
    ness notions. In: Groth, J., et al. (eds.) IMACC 2015. LNCS, vol. 9496, pp. 94–111.
    Springer, Heidelberg (2015). doi:10.1007/978-3-319-27239-9 6
 9. Bellare, M., Namprempre, C.: Authenticated encryption: relations among notions
    and analysis of the generic composition paradigm. In: Okamoto, T. (ed.) ASI-
    ACRYPT 2000. LNCS, vol. 1976, pp. 531–545. Springer, Heidelberg (2000)
10. Bellare, M., Paterson, K.G., Rogaway, P.: Security of symmetric encryption against
    mass surveillance. In: Garay, J.A., Gennaro, R. (eds.) CRYPTO 2014, Part I.
    LNCS, vol. 8616, pp. 1–19. Springer, Heidelberg (2014)
11. Bernstein, D., Schwabe, P.: Cryptographic software, side channels, and veriﬁcation.
    In: COST CryptoAction WG3 Meeting, April 2015
12. Bernstein, D.J.: AES timing variability at a glance (2015). http://cr.yp.to/mac/
    variability1.html. Accessed 25 Oct 2015
184     J.B. Almeida et al.

13. Bernstein, D.J.: Cache-timing attacks on AES (2005). Author’s webpage
14. Bernstein, D.J., Lange, T., Schwabe, P.: The security impact of a new crypto-
    graphic library. In: Hevia, A., Neven, G. (eds.) LatinCrypt 2012. LNCS, vol. 7533,
    pp. 159–176. Springer, Heidelberg (2012)
15. Boldyreva, A., Degabriele, J.P., Paterson, K.G., Stam, M.: On symmetric encryp-
    tion with distinguishable decryption failures. In: Moriai, S. (ed.) FSE 2013. LNCS,
    vol. 8424, pp. 367–390. Springer, Heidelberg (2014)
16. Canvel, B., Hiltgen, A.P., Vaudenay, S., Vuagnoux, M.: Password interception in
    a SSL/TLS channel. In: Boneh, D. (ed.) CRYPTO 2003. LNCS, vol. 2729, pp.
    583–599. Springer, Heidelberg (2003)
17. Chothia, T., Smirnov, V.: A traceability attack against e-Passports. In: Sion, R.
    (ed.) FC 2010. LNCS, vol. 6052, pp. 20–34. Springer, Heidelberg (2010)
18. Degabriele, J.-P., Paterson, K.G., Watson, G.J.: Provable security in the real world.
    IEEE Secur. Priv. 9(3), 33–41 (2011)
19. Goguen, J.A., Meseguer, J.: Security policies and security models. In: 1982 IEEE
    Symposium on Security and Privacy, Oakland, CA, USA, April 26–28, pp. 11–20.
    IEEE Computer Society (1982)
20. Hoang, V.T., Katz, J., Malozemoﬀ, A.J.: Automated analysis and synthesis of
    authenticated encryption schemes. Cryptology ePrint Archive, report 2015/624
    (2015). http://eprint.iacr.org/2015/624
21. Käsper, E., Schwabe, P.: Faster and timing-attack resistant AES-GCM. In: Clavier,
    C., Gaj, K. (eds.) CHES 2009. LNCS, vol. 5747, pp. 1–17. Springer, Heidelberg
    (2009)
22. Krawczyk, H.: The order of encryption and authentication for protecting commu-
    nications (or: how secure is SSL?). In: Kilian, J. (ed.) CRYPTO 2001. LNCS, vol.
    2139, pp. 310–331. Springer, Heidelberg (2001)
23. Langley, A.: Lucky thirteen attack on TLS CBC. Imperial violet, February 2013.
    https://www.imperialviolet.org/2013/02/04/luckythirteen.html. Accessed 25 Oct
    2015
24. Leroy, X.: Formal certiﬁcation of a compiler back-end, or: programming a com-
    piler with a proof assistant. In: ACM Symposium on Principles of Programming
    Languages POPL 2006 (2006)
25. Maurer, U., Tackmann, B.: On the soundness of Authenticate-then-Encrypt: for-
    malizing the malleability of symmetric encryption. In: Al-Shaer, E., Keromytis,
    A.D., Shmatikov, V. (eds.) ACM CCS 2010, pp. 505–515. ACM Press, October
    2010
26. Paterson, K.G., Ristenpart, T., Shrimpton, T.: Tag size Does matter: attacks and
    proofs for the TLS record protocol. In: Lee, D.H., Wang, X. (eds.) ASIACRYPT
    2011. LNCS, vol. 7073, pp. 372–389. Springer, Heidelberg (2011)
27. Rauzy, P., Guilley, S.: A formal proof of countermeasures against fault injection
    attacks on CRT-RSA. J. Crypt. Eng. 4(3), 173–185 (2014)
28. Schmidt, S.: Introducing s2n, a new open source TLS implementation,
    June 2015. https://blogs.aws.amazon.com/security/post/TxCKZM94ST1S6Y/
    Introducing-s2n-a-New-Open-Source-TLS-Implementation. Accessed 25 Oct 2015
29. Vaudenay, S.: Security ﬂaws induced by CBC padding - applications to SSL,
    IPSEC, WTLS. In: Knudsen, L.R. (ed.) EUROCRYPT 2002. LNCS, vol. 2332,
    pp. 534–546. Springer, Heidelberg (2002)
