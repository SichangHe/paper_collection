             CoqCryptoLine: A Verified Model
               Checker with Certified Results

          Ming-Hsien Tsai4(B) , Yu-Fu Fu2 , Jiaxiang Liu5 , Xiaomu Shi3 ,
                     Bow-Yaw Wang1 , and Bo-Yin Yang1
                            1
                              Academia Sinica, Taipei, Taiwan
                          {bywang,byyang}@iis.sinica.edu.tw
                   2
                      Georgia Institute of Technology, Atlanta, USA
                                    yufu@gatech.edu
         3
           Institute of Software, Chinese Academy of Sciences, Beijing, China
                                  xshi0811@gmail.com
                 4
                   National Institute of Cyber Security, Taipei, Taiwan
                                  mhtsai208@gmail.com
                        5
                           Shenzhen University, Shenzhen, China
                                jiaxiang0924@gmail.com

       Abstract. We present the veriﬁed model checker CoqCryptoLine
       for cryptographic programs with certiﬁed veriﬁcation results. The
       CoqCryptoLine veriﬁcation algorithm consists of two reductions. The
       algebraic reduction transforms into a root entailment problem; and the
       bit-vector reduction transforms into an SMT QF_BV problem. We
       specify and verify both reductions formally using Coq with MathComp.
       The CoqCryptoLine tool is built on the OCaml programs extracted
       from veriﬁed reductions. CoqCryptoLine moreover employs certiﬁed
       techniques for solving the algebraic and logic problems. We evaluate
       CoqCryptoLine on cryptographic programs from industrial security
       libraries.


1    Introduction

CoqCryptoLine [1] is a veriﬁed model checker with certiﬁed veriﬁcation
results. It is designed for verifying complex non-linear integer computations
commonly found in cryptographic programs. The veriﬁcation algorithms of
CoqCryptoLine consist of two reductions. The algebraic reduction transforms
polynomial equality checking into a root entailment problem in commutative
algebra; the bit-vector reduction reduces range properties to satisﬁability of
queries in the Quantiﬁer-Free Bit-Vector (QF_BV) logic from Satisﬁability
Modulo Theories (SMT) [6]. Both veriﬁcation algorithms are formally speciﬁed
and veriﬁed by the proof assistant Coq with MathComp [7,17]. CoqCryp-
toLine veriﬁcation programs are extracted from the formal speciﬁcation and
therefore veriﬁed by the proof assistant automatically.

The original version of this chapter was revised: The mistakes in authors aﬃliation
information and typographical errors have been corrected. The correction to this
chapter is available at https://doi.org/10.1007/978-3-031-37703-7_22
c The Author(s) 2023, corrected publication 2023
C. Enea and A. Lal (Eds.): CAV 2023, LNCS 13965, pp. 227–240, 2023.
https://doi.org/10.1007/978-3-031-37703-7_11
228     M.-H. Tsai et al.

    To minimize errors from external tools, recent developments in certiﬁed veriﬁ-
cation are employed by CoqCryptoLine. The root entailment problem is solved
by the computer algebra system (CAS) Singular [19]. CoqCryptoLine asks
the external algebraic tool to provide certiﬁcates and validates certiﬁcates with
the formal polynomial theory in Coq. SMT QF_BV queries on the other hand
are answered by the veriﬁed SMT QF_BV solver CoqQFBV [33]. Answers to
SMT QF_BV queries are therefore all certiﬁed as well. With formally veriﬁed
algorithms and certiﬁed answers from external tools, CoqCryptoLine gives
veriﬁcation results with much better guarantees than average automatic veriﬁ-
cation tools.
    Reliable veriﬁcation tools would not be very useful if they could not check
real-world programs eﬀectively. In our experiments, CoqCryptoLine veriﬁes
54 real-world cryptographic programs. 52 of them are from well-known security
libraries such as Bitcoin [35] and OpenSSL [30]. They are implementations
of ﬁeld and group operations in elliptic curve cryptography. The remaining two
are the Number-Theoretic Transform (NTT) programs from the post-quantum
cryptosystem Kyber [10]. All ﬁeld operations are implemented in a few hundred
lines and veriﬁed in 6 minutes. The most complicated generic group operation
in the elliptic curve Curve25519 consists of about 4000 lines and is veriﬁed by
CoqCryptoLine in 1.5 h.

Related Work. There are numerous model checkers in the community, e.g. [8,
13,21–23]. Nevertheless, few of them are formally veriﬁed. To our knowl-
edge, the ﬁrst veriﬁcation of a model checker was performed in Coq for
the modal μ-calculus [34]. The LTL model checker CAVA [15,27] and the
model checker Munta [38,39] for timed automata were developed and veriﬁed
using Isabelle/HOL [29], which can be considered as veriﬁed counterparts
of SPIN [21] and Uppaal [23], respectively. CoqCryptoLine instead checks
CryptoLine models [16,31] that are for the correctness of cryptographic pro-
grams. It can be seen as a veriﬁed version of CryptoLine. A large body of work
studies the correctness of cryptographic programs, e.g. [2–4,9,12,14,24,26,40],
cf. [5] for a survey. They either require human intervention or are unveriﬁed, while
our work is fully automatic and veriﬁed. The most relevant work is bvCryp-
toLine [37], which is the ﬁrst automated and partly veriﬁed model checker
for a very limited subset of CryptoLine. We will compare our work with it
comprehensively in Sect. 2.3.

2     CoqCryptoLine
CoqCryptoLine is an automatic veriﬁcation tool that takes a CryptoLine
speciﬁcation as input and returns certiﬁed results indicating the validity of the
speciﬁcation. We brieﬂy describe the CryptoLine language [16] followed by the
modules, features, and optimizations of CoqCryptoLine in this section.

2.1   CryptoLine Language
A CryptoLine speciﬁcation contains a CryptoLine program with pre-
and post-conditions, where the CryptoLine program usually models some
         CoqCryptoLine: A Veriﬁed Model Checker with Certiﬁed Results         229

cryptographic program [16,31]. Both the pre- and post-conditions consist of an
algebraic part, which is formulated as a conjunction of (modular) equations, and
a range part as an SMT QF_BV predicate. A CryptoLine speciﬁcation is
valid if every program execution starting from a program state satisfying the
pre-condition ends in a state satisfying the post-condition.
    CryptoLine is designed for modeling cryptographic assembly programs.
Besides the assignment (mov) and conditional assignment (cmov) statements,
CryptoLine provides arithmetic statements such as addition (add), addition
with carry (adc), subtraction (sub), subtraction with borrow (sbb), half multi-
plication (mul) and full multiplication (mull). Most of them have versions that
model the carry/borrow ﬂags explicitly (like adds, adcs, subs, sbbs). It also
allows bitwise statements, for instance, bitwise AND (and), OR (or) and left-
shift (shl). To deal with multi-word arithmetic, CryptoLine further includes
multi-word constructs, for example, those that split (split) or join (join) words,
as well as multi-word shifts (cshl). CryptoLine is strongly typed, admitting
both signed and unsigned interpretations for bit-vector variables and constants.
The cast statement converts types explicitly. Finally, CryptoLine also sup-
ports special statements (assert and assume) for veriﬁcation purposes.

2.2   The Architecture of CoqCryptoLine
CoqCryptoLine reduces the veriﬁcation problem of a CryptoLine speciﬁ-
cation to instances of root entailment problems and SMT problems over the
QF_BV logic. These instances are then solved by respective certiﬁed techniques.
Moreover, the components in CoqCryptoLine are also speciﬁed and veriﬁed
by the proof assistant Coq with MathComp [7,17]. Figure 1 gives an overview
of CoqCryptoLine. In the ﬁgure, dashed components represent external tools.
Rectangular boxes are veriﬁed components and rounded boxes are unveriﬁed.
Note that all our proof eﬀorts using Coq are transparent to users. No Coq
proof is required from users during veriﬁcation of cryptographic programs with
CoqCryptoLine. Details can be found in [36].
    Starting from a CryptoLine speciﬁcation text, the CoqCryptoLine parser
translates the text into an abstract syntax tree deﬁned in the Coq module DSL.
The module gives formal semantics for the typed CryptoLine language [16].
The validity of CryptoLine speciﬁcations is also formalized. Similar to most
program veriﬁcation tools, CoqCryptoLine transforms CryptoLine speciﬁ-
cations to the static single assignment (SSA) form. The SSA module gives our
transformation algorithm. It moreover shows that validity of CryptoLine speci-
ﬁcations is preserved by the SSA transformation. CoqCryptoLine then reduces
the veriﬁcation problem via two Coq modules.
    The SSA2ZSSA module contains our algebraic reduction to the root entail-
ment problem. Concretely, a system of (modular) equations is constructed from
the given program so that program executions correspond to the roots of the
system of (modular) equations. To verify algebraic post-conditions, it suﬃces to
check if the roots for executions are also roots of (modular) equations in the
post-condition. However, program executions can deviate from roots of (modu-
lar) equations when over- or under-ﬂow occurs. CoqCryptoLine will generate
230           M.-H. Tsai et al.




                                                               trusted
                       C OQ C RYPTO L INE parser



                                  DSL




                                                               verified
          SSA2ZSSA                SSA              SSA2QFBV


                Validator                          solve
                                 solve
      solve
                                            SMT QF BV solver               verified module
                     validate
                                                                           unverified module




                                                               untrusted
                                                                           verified external solver
  computer algebra system
                                                                           unverified external solver


                                Fig. 1. Overview of CoqCryptoLine


soundness conditions to ensure the executions conform to our (modular) equa-
tions. The algebraic veriﬁcation problem is thus reduced to the root entailment
problem provided that soundness conditions hold.
    The SSA2QFBV module gives our bit-vector reduction to the SMT QF_BV
problem. It constructs an SMT query to check the validity of the given Crypto-
Line range speciﬁcation. Concretely, an SMT QF_BV query is built such that
all program executions correspond to satisfying assignments to the query and
vice versa. To verify the range post-conditions, it suﬃces to check if satisfying
assignments for the query also satisfy the post-conditions. The range veriﬁca-
tion problem is thus reduced to the SMT QF_BV problem. On the other hand,
additional SMT queries are constructed to check soundness conditions for the
algebraic reduction. We formally prove the equivalence between soundness con-
ditions and corresponding queries.
    With the two formally veriﬁed reduction algorithms, it remains to solve the
root entailment problems and the SMT QF_BV problems with external solvers.
CoqCryptoLine invokes an external computer algebra system (CAS) to solve
the root entailment problems, and improves the techniques in [20,37] to validate
the (untrusted) returned answers. Currently, the CAS Singular [19] is sup-
ported. To solve the SMT QF_BV problems, CoqCryptoLine employs the
certiﬁed SMT QF_BV solver CoqQFBV [33]. In all cases, instances of the two
kinds of problems are solved with certiﬁcates. And CoqCryptoLine employs
veriﬁed certiﬁcate checkers to validate the answers to further improve assurance.
    Note that the algebraic reduction in SSA2ZSSA is sound but not complete due
to the abstraction of bit-accurate semantics into (modular) polynomial equations
over integers. Thus a failure in solving the root entailment problem by CAS does
not mean that the algebraic post-conditions are violated. On the other hand, the
bit-vector reduction in SSA2QFBV is both sound and complete.
    The CoqCryptoLine tool is built on OCaml programs extracted from
veriﬁed algorithms in Coq with MathComp. We moreover integrate the OCaml
         CoqCryptoLine: A Veriﬁed Model Checker with Certiﬁed Results         231

programs from the certiﬁed SMT QF_BV solver CoqQFBV. Our trusted
computing base consists of (1) CoqCryptoLine parser, (2) text interface with
external SAT solvers (from CoqQFBV), (3) the proof assistant Isabelle [29]
(from the SAT solver certiﬁcate validator Grat used by CoqQFBV) and (4) the
Coq proof assistant. Particularly, sophisticated decision procedures in external
CASs and SAT solvers used in CoqQFBV need not be trusted.


2.3   Features and Optimizations

CoqCryptoLine comes with the following features and optimizations imple-
mented in its modules.

Type System. CoqCryptoLine fully supports the type system of the Cryp-
toLine language. The type system is used to model bit-vectors of arbitrary
bit-widths with unsigned or signed interpretation. Such a type system allows
CoqCryptoLine to model more industrial examples translated from C pro-
grams via GCC [16] or LLVM [24] compared to bvCryptoLine [37], which only
allows unsigned bit-vectors, all of the same bit-width.

Mixed Theories. With the assert and assume statements supported by
CoqCryptoLine, it is possible to make an assertion on the range side (or
on the algebraic side) and then make an equivalent assumption on the alge-
braic side (or resp. on the range side). With this feature, a predicate can be
asserted on one side where the predicate is easier to prove, and then assumed
on the other side to ease the veriﬁcation of other predicates. The equivalence
between the asserted predicate and the assumed predicate is currently not ver-
iﬁed by CoqCryptoLine, though it is achievable. Both assert and assume
statements are not available in bvCryptoLine.

Multi-threading. All extracted OCaml code from the veriﬁed algorithms in Coq
runs sequentially. To speed up, SMT QF_BV problems, as well as root entail-
ment problems, are solved parallelly.

Eﬃcient Root Entailment Problem Solving. CoqCryptoLine can be used as
a solver for root entailment problems with certiﬁcates validated by a veriﬁed
validator. A root entailment problem is reduced to an ideal membership problem,
which is then solved by computing Gröbner basis [20]. To solve a root entailment
problem with a certiﬁcate, we need to ﬁnd a witness of polynomials c0 , . . . , cn
such that
                                         n
                                  q = Σi=0 ci pi                               (1)
where q and pi ’s are given polynomials. To compute the witness, bvCryptoLine
relies on gbarith [32], where new variables are introduced. CoqCryptoLine
utilizes the lift command in Singular instead without adding fresh variables.
We show in the evaluation section that using lift is more eﬃcient than using
gbarith. The witness found is further validated by CoqCryptoLine, which
232     M.-H. Tsai et al.

relies on the polynomial normalization procedure norm_subst in Coq to check
if Eq. 1 holds. bvCryptoLine on the other hand uses the ring tactic in Coq,
where extra type checking is performed. Elimination of ideal generators through
variable substitution is an eﬃcient approach to simplify an ideal membership
problem [37]. The elimination procedure implemented in CoqCryptoLine can
identify much more variable substitution patterns than those found by bvCryp-
toLine.

Multi-moduli. Modular equations with multi-moduli are common in post-
quantum cryptography. For example, the post-quantum cryptosystem Kyber
uses the polynomial ring Z3329 [X]/X 256 + 1 containing two moduli 3329 and
X 256 +1. To support multi-moduli in CoqCryptoLine, in the proof of our alge-
                                                                              n
braic reduction, we have to ﬁnd integers c0 , . . . , cn such that e1 − e2 = Σi=0 ci mi
given the proof of e1 = e2 (mod m0 , . . . , mn ) where e1 , e2 , and mi ’s are inte-
gers. Instead of implementing a complicated procedure to ﬁnd the exact ci ’s, we
simply invoke the xchoose function provided by MathComp to ﬁnd ci ’s based
on the proof of e1 = e2 (mod m0 , . . . , mn ). Multi-moduli is not supported by
bvCryptoLine.
Tight Integration with CoqQFBV. CoqCryptoLine veriﬁes every atomic
range predicate separately using the certiﬁed SMT QF_BV solver CoqQFBV.
Constructing a text ﬁle as the input to CoqQFBV for every atomic range
predicate is not a good idea because the bit-blasting procedure in CoqQFBV
is performed several times for the identical program. CoqCryptoLine thus is
tightly integrated with CoqQFBV to speed up bit-blasting of the same program
using the cache provided by CoqQFBV. bvCryptoLine uses the SMT solver
Boolector to prove range predicates without certiﬁcates.

Slicing. During the reductions from the veriﬁcation problem of a Crypto-
Line speciﬁcation to instances of root entailment problems and SMT QF_BV
problems, a veriﬁed static slicing is performed in CoqCryptoLine to produce
smaller problems. Unlike the work in [11], which sets all assume statements as
additional slicing criteria, the slicing in CoqCryptoLine is capable of pruning
unrelated predicates in assume statements. The slicing procedure implemented
in CoqCryptoLine is much more complicated than the one in bvCryptoLine
due to the presence of assume statements. This feature is provided as command-
line option because it makes the veriﬁcation incomplete. With slicing, the time
in verifying industrial examples is reduced dramatically.


3     Walkthrough
We illustrate how CoqCryptoLine is used in this section. The x86_64 assembly
subroutine ecp_nistz256_mul_montx from OpenSSL [30] shown in Fig. 2 is
veriﬁed as an example.
    An input for CoqCryptoLine contains a CryptoLine speciﬁcation for the
assembly subroutine. The original subroutine is marked between the comments
           CoqCryptoLine: A Veriﬁed Model Checker with Certiﬁed Results        233

PROGNAME STARTS and PROGNAME ENDS, which is obtained automatically from
the Python script provided by CryptoLine [31].
    Prior to the “START” comment are the parameter declaration, pre-condition,
and variable initialization. After the “END” comment is the post-condition of
the subroutine. After the subroutine ends, the result is moved to the output
variables.
    The assembly subroutine ecp_nistz256_mul_montx takes two 256-bit
unsigned integers a and b and the modulus m as inputs. The 256-bit integer
m is the prime p256 = 2256 − 2224 + 2192 + 296 − 1 from the NIST curve. The
256-bit integers a and b (less than the prime) are the multiplicands. Each 256-bit
input integer d ∈ {a, b, m} is denoted by four 64-bit unsigned integer variables
di (for 0 ≤ i < 4) in little-endian representation. The expression limbs n [d0 ,
d1 , ..., di ] is short for d0 + d1 *2**n + ... +di *2**(i *n )1 . The inputs and
constants are then put in the variables for memory cells with the mov state-
ments. There are two parts to a pre-condition. The ﬁrst part is for the algebraic
reduction; the second part is for the bit-vector reduction:
and [ m0=0xffffffffffffffff, m1=0x00000000ffffffff,
      m2=0x0000000000000000, m3=0xffffffff00000001 ]
&&
and [ m0=0xffffffffffffffff@64, m1=0x00000000ffffffff@64,
      m2=0x0000000000000000@64, m3=0xffffffff00000001@64,
      limbs 64 [a0,a1,a2,a3] <u limbs 64 [m0,m1,m2,m3],
      limbs 64 [b0,b1,b2,b3] <u limbs 64 [m0,m1,m2,m3] ]

    The output 256-bit integer represented by the four variables ci (for 0 ≤ i < 4)
has two requirements. Firstly, the output integer times 2256 equals the product
of the input integers modulo p256. Secondly, the output integer is less than p256.
Formally, we have this post-condition:
eqmod limbs 64 [0, 0, 0, 0, c0, c1, c2, c3]
      limbs 64 [a0, a1, a2, a3] * limbs 64 [b0, b1, b2, b3]
      limbs 64 [m0, m1, m2, m3]
&&
limbs 64 [c0, c1, c2, c3] <u limbs 64 [m0, m1, m2, m3]

    Here, we employ the algebraic reduction to verify the non-linear modular
equality, and the bit-vector reduction to verify the proper range of the output
integer.
    However, verifying ecp_nistz256_mul_montx takes extra annotations to hint
CoqCryptoLine how to verify the post-condition. E.g., in adding two 256-
bit integers represented by 64-bit variables, a chain of four 64-bit additions is
performed and carries are propagated. The last carry as the chain ends must be
zero or the 256-bit sum is incorrect. In ecp_nistz256_mul_montx two interleaved
addition chains use the carry and the overﬂow ﬂags for carries respectively, so
we annotate as follows at the end of two interleaving addition chains to tell
CoqCryptoLine about the ﬁnal carries:
1
    ** is the exponentiation operator in CryptoLine.
234         M.-H. Tsai et al.

      proc main                                         adcs carry r9 r9 rcx carry;
      (uint64 a0, uint64 a1, uint64 a2, uint64 a3,      adcs overflow r10 r10 rbp overflow;
       uint64 b0, uint64 b1, uint64 b2, uint64 b3,      mull rbp rcx rdx L0x7fffffffd9b8;
       uint64 m0, uint64 m1, uint64 m2, uint64 m3) =    adcs carry r10 r10 rcx carry;
      { and [ m0 = 0xffffffffffffffff,                  adcs overflow r11 r11 rbp overflow;
               m1 = 0x00000000ffffffff,                 mull rbp rcx rdx L0x7fffffffd9c0;
               m2 = 0x0000000000000000,                 adcs carry r11 r11 rcx carry;
               m3 = 0xffffffff00000001 ]                adcs overflow r12 r12 rbp overflow;
      &&                                                mull rbp rcx rdx L0x7fffffffd9c8;
         and [ m0 = 0xffffffffffffffff@64,              mov rdx r9;
               m1 = 0x00000000ffffffff@64,
               m2 = 0x0000000000000000@64,              adcs carry r12 r12 rcx carry;
               m3 = 0xffffffff00000001@64,              split ddc rcx r9 32;
               limbs 64 [a0, a1, a2, a3] <u             shl rcx rcx 32;
                   limbs 64 [m0, m1, m2, m3],           adcs overflow r13 r13 rbp overflow;
               limbs 64 [b0, b1, b2, b3] <u             split rbp dc r9 32;
                   limbs 64 [m0, m1, m2, m3] ] }
                                                        assert true && rbp=ddc;
      mov L0x7fffffffd9b0 a0; mov L0x7fffffffd9b8 a1;   assume rbp=ddc && true;
      mov L0x7fffffffd9c0 a2; mov L0x7fffffffd9c8 a3;
      mov L0x7fffffffd9d0 b0; mov L0x7fffffffd9d8 b1;   adcs carry r13 r13 r8 carry;
      mov L0x7fffffffd9e0 b2; mov L0x7fffffffd9e8 b3;   adcs overflow r8 r8 r8 overflow;

      mov L0x55555557c000 0xffffffffffffffff@uint64;    assert true && and [carry=0@1,overflow=0@1];
      mov L0x55555557c008 0x00000000ffffffff@uint64;    assume and [carry=0,overflow=0] && true;
      mov L0x55555557c010 0x0000000000000000@uint64;
      mov L0x55555557c018 0xffffffff00000001@uint64;    ...

      (* ecp_nistz256_mul_montx STARTS *)               mov L0x7fffffffda00 r8;
      mov rdx L0x7fffffffd9d0;                          mov L0x7fffffffda08 r9;
      mov r9 L0x7fffffffd9b0;                           (* ecp_nistz256_mul_montx ENDS *)
      mov r10 L0x7fffffffd9b8;
      mov r11 L0x7fffffffd9c0;                          mov c0 L0x7fffffffd9f0;
      mov r12 L0x7fffffffd9c8;                          mov c1 L0x7fffffffd9f8;
      mull r9 r8 rdx r9;                                mov c2 L0x7fffffffda00;
      mull r10 rcx rdx r10;                             mov c3 L0x7fffffffda08;
      mov r14 0x20@uint64;
      mov r13 0@uint64;                                 { eqmod limbs 64 [0, 0, 0, 0, c0, c1, c2, c3]
                                                                 limbs 64 [a0, a1, a2, a3] *
      ...                                                        limbs 64 [b0, b1, b2, b3]
                                                                 limbs 64 [m0, m1, m2, m3]
      mov r8 0@uint64;                                  &&
      clear carry;                                         limbs 64 [c0, c1, c2, c3] <u
      clear overflow;                                          limbs 64 [m0, m1, m2, m3] }
      mull rbp rcx rdx L0x7fffffffd9b0;



                  Fig. 2. CryptoLine Model for ecp_nistz256_mul_montx


assert true && and [ carry=0@1, overflow=0@1 ];
assume and [ carry=0, overflow=0 ] && true;

    The assert statement veriﬁes that both the carry and overﬂow ﬂags are
zeroes through the bit-vector reduction. The assume statement then passes this
information to the algebraic reduction. Eﬀectively, CoqCryptoLine checks that
both ﬂags are zero for all inputs satisfying the pre-condition, then uses those facts
as lemmas to verify the post-condition with the algebraic reduction.
    The full speciﬁcation for ecp_nistz256_mul_montx has 230 lines, including
50 lines of manual annotations. 20 are straightforward annotations for variable
declaration and initialization. The remaining 30 lines of annotations are hints to
CoqCryptoLine, which then veriﬁes the post-condition in 30 s with 24 threads.
    The illustration of the typical veriﬁcation ﬂow shows how a user constructs
a CryptoLine speciﬁcation. The pre-condition for program inputs, the post-
condition for outputs, and variable initialization must be speciﬁed manually.
Additional annotations may be added as hints. Notice that hints only tell
CoqCryptoLine what, not why properties should hold. Proofs of annotated
hints and the post-condition are found by CoqCryptoLine automatically. Con-
sequently, manual annotations are minimized and veriﬁcation eﬀorts are reduced
signiﬁcantly.
          CoqCryptoLine: A Veriﬁed Model Checker with Certiﬁed Results                235

4    Evaluation
We evaluate CoqCryptoLine on 52 benchmarks from four industrial security
libraries Bitcoin [35], boringSSL [14,18], nss [25], and OpenSSL [30]. The C
reference and optimized avx2 implementations of the Number-Theoretic Trans-
form (NTT) from the post-quantum key encapsulation mechanism Kyber [10]
are also evaluated. Among the total 54 benchmarks, 43 benchmarks contain fea-
tures not supported by bvCryptoLine such as signed variables. All experiments
are performed on an Ubuntu 22.04.1 machine with a 3.20GHz Intel Xeon Gold
6134M CPU and 1TB RAM.
    Benchmarks from security libraries are various ﬁeld and group operations
from elliptic curve cryptography (ECC). In ECC, rational points on curves are
represented by elements in large ﬁnite ﬁelds. In Bitcoin, the ﬁnite ﬁeld is the
residue system modulo the prime p256k1 = 2256 − 232 − 29 − 28 − 27 − 26 − 24 − 1.
For other security libraries (boringSSL, nss, and OpenSSL), we verify the
operations in Curve25519 using the residue system modulo the prime p25519 =
2255 − 19 as the underlying ﬁeld. Rational points on elliptic curves form a group.
The group operation in turn is implemented by a number of ﬁeld operations.
    In lattice-based post-quantum cryptosystems, polynomial rings are used.
Speciﬁcally, the polynomial ring Z3329 [X]/X 256 + 1 is used in Kyber. To
speed up multiplication in the polynomial ring, Kyber requires the multiplica-
tion to be implemented by NTT. NTT is a discrete Fast Fourier Transform over
ﬁnite ﬁelds. Instead of complex roots of unity, NTT uses the principal roots of
unity in ﬁelds. Mathematically, the Kyber NTT computes the following ring
isomorphism

    Z3329 [X]/X 256 + 1 ∼
                          = Z3329 [X]/X 2 − ζ0  × · · · × Z3329 [X]/X 2 − ζ127 

where ζi ’s are the principal roots of unity.
    We ﬁrst compare CoqCryptoLine with all optimizations described in this
paper against the unveriﬁed model checker CryptoLine [16]. Both tools invoke
the computer algebra system Singular [19], but CryptoLine neither lets Sin-
gular produce certiﬁcates nor certiﬁes answers from Singular. CoqCrypto-
Line moreover uses the certiﬁed SMT QF_BV solver CoqQFBV [33]; Cryp-
toLine uses the uncertiﬁed but very eﬃcient Boolector [28].
    For the ECC experiments, CoqCryptoLine veriﬁes all ﬁeld operations in
6 minutes. It takes a few thousand seconds to verify group operations. The
most complex implementation (x25519_scalar_mult_generic) from boringSSL
(4274 statements) takes about 1.5 hours.2 For Kyber, CoqCryptoLine veriﬁes
in 2642 and 1048 seconds, respectively, that the reference and avx2 NTT imple-
mentations indeed compute the isomorphism. The unveriﬁed CryptoLine in
comparison ﬁnishes veriﬁcation in about 95 seconds. A summary of the compar-
ison between CoqCryptoLine and CryptoLine is shown in Fig. 3a. Though
CoqCryptoLine is much slower than CryptoLine, the running time (1.5
hours) for the most complex implementation is still acceptable.
2
    Two (out of three) modular polynomial equations in the post-condition are certiﬁed.
236        M.-H. Tsai et al.

                                                      100              93.38
            3
          10


                                                       50
          101



         10−1                                                2.09                    4.63
                                                         0

                10−1      101       103


(a) C OQ C RYPTO L INE versus C RYPTO -          (b) Percentages of average running time
L INE                                            for C OQ C RYPTO L INE internal OC AML
                                                 code (INT), external SMT QF BV solver
                                                 (SMT), and external computer algebra sys-
                                                 tem (CAS)

                                                       105

          103
                                                       103
  lift




          101
                                                       101


         10−1                                        10−1

                10−1     101        103                       10−1    101      103      105
                       gbarith

          (c) gbarith versus lift                (d) C OQ C RYPTO L INE− versus C OQ C RYP -
                                                 TO L INE


                       Fig. 3. Running time (in seconds) comparisons


   Figure 3b shows the percentages of average running time for CoqCrypto-
Line internal OCaml code (INT), external SMT QF_BV solver (SMT), and
external computer algebra system (CAS). External solvers take much more time
than the internal OCaml program does. Between external solvers, the exter-
nal computer algebra system takes 4.63% of the time and the external SMT
QF_BV solver spends 93.28% of the time.
   To show the performance of the lift optimization, we run CoqCryptoLine
and bvCryptoLine on root entailment problems generated from the bench-
marks. Here we only consider 12 root entailment problems that trigger gbarith
in bvCryptoLine. Figure 3c shows the running time of Singular in solving
         CoqCryptoLine: A Veriﬁed Model Checker with Certiﬁed Results            237

root entailment problems based on gbarith in bvCryptoLine and lift in
CoqCryptoLine. bvCryptoLine fails to solve 3 root entailment problems in
one hour. For the other 9 root entailment problems, lift outperforms gbarith.
   We also compare CoqCryptoLine with and without slicing. The version of
CoqCryptoLine without slicing is denoted by CoqCryptoLine− . The run-
ning time comparison between CoqCryptoLine and CoqCryptoLine− in
Fig. 3d shows that slicing reduces the running time obviously.


5   Conclusion

CoqCryptoLine is a veriﬁed model checker for cryptographic programs with
certiﬁed results. Its modules are formally veriﬁed in Coq with MathComp.
CoqCryptoLine moreover employs external tools and validates their answers
with certiﬁcates. We evaluate CoqCryptoLine on benchmarks from indus-
trial security libraries (Bitcoin, boringSSL, nss and OpenSSL) and a
post-quantum cryptography standard candidate (Kyber). In our experiments,
CoqCryptoLine veriﬁes most cryptographic programs with certiﬁcates in a
reasonable time (6 min). Benchmarks with thousands of lines are veriﬁed in
1.5 h. To our knowledge, this is the ﬁrst certiﬁed veriﬁcation on operations of
the elliptic curve secp256k1 used in Bitcoin, and the avx2 and reference imple-
mentations of Kyber number-theoretic transform.

Acknowledgments. The authors in Academia Sinica are partially funded by National
Science and Technology Council grants NSTC110-2221-E-001-008-MY3, NSTC111-
2221-E-001-014-MY3, NSTC111-2634-F-002-019, the Sinica Investigator Award AS-
IA-109-M01, the Data Safety and Talent Cultivation Project AS-KPQ-109-DSTCP,
and the Intel Fast Veriﬁed Postquantum Software Project. The authors in Shenzhen
University and ISCAS are partially funded by Shenzhen Science and Technology Inno-
vation Commission (JCYJ20210324094202008), the National Natural Science Founda-
tion of China (62002228, 61836005), and the Natural Science Foundation of Guangdong
Province (2022A1515011458, 2022A1515010880).


References
 1. CoqCryptoLine GitHub repository (2023). https://github.com/fmlab-iis/coq-
    cryptoline
 2. Aﬀeldt, R.: On construction of a library of formally veriﬁed low-level arithmetic
    functions. Innov. Syst. Softw. Eng. 9(2), 59–77 (2013)
 3. Almeida, J.B., et al.: Jasmin: High-assurance and high-speed cryptography. In:
    ACM SIGSAC Conference on Computer and Communications Security, pp. 1807–
    1823. ACM (2017)
 4. Appel, A.W.: Veriﬁcation of a cryptographic primitive: SHA-256. ACM Trans.
    Programm. Lang. Syst. 37(2), 7:1–7:31 (2015)
 5. Barbosa, M., et al.: Sok: Computer-aided cryptography. In: 42nd IEEE Symposium
    on Security and Privacy, SP 2021, San Francisco, CA, USA, 24-27 May 2021, pp.
    777–795. IEEE (2021). https://doi.org/10.1109/SP40001.2021.00008
238     M.-H. Tsai et al.

 6. Barrett, C., Fontaine, P., Tinelli, C.: The Satisﬁability Modulo Theories Library
    (SMT-LIB). www.SMT-LIB.org (2016)
 7. Bertot, Y., Castéran, P.: Interactive Theorem Proving and Program Development -
    Coq’Art: The Calculus of Inductive Constructions. Texts in Theoretical Computer
    Science, Springer (2004). https://doi.org/10.1007/978-3-662-07964-5
 8. Beyer, D., Keremoglu, M.E.: Cpachecker: A tool for conﬁgurable software veriﬁ-
    cation. In: Gopalakrishnan, G., Qadeer, S. (eds.) Computer Aided Veriﬁcation -
    23rd International Conference, CAV 2011, Snowbird, UT, USA, July 14-20, 2011.
    Proceedings. Lecture Notes in Computer Science, vol. 6806, pp. 184–190. Springer
    (2011). https://doi.org/10.1007/978-3-642-22110-1_16
 9. Bond, B., et al.: Vale: Verifying high-performance cryptographic assembly code.
    In: USENIX Security Symposium, pp. 917–934. USENIX Association (2017)
10. Bos, J., et al.: CRYSTALS - Kyber: a CCA-secure module-lattice-based KEM. In:
    Smith, M., Piessens, F. (eds.) IEEE European Symposium on Security and Privacy,
    pp. 353–367. IEEE (2018)
11. Chalupa, M., Strejcek, J.: Evaluation of program slicing in software veriﬁcation. In:
    Ahrendt, W., Tarifa, S.L.T. (eds.) Integrated Formal Methods - 15th International
    Conference, IFM 2019, Bergen, Norway, December 2-6, 2019, Proceedings. Lecture
    Notes in Computer Science, vol. 11918, pp. 101–119. Springer (2019). https://doi.
    org/10.1007/978-3-030-34968-4_6
12. Chen, Y.F., et al.: Verifying Curve25519 software. In: Ahn, G.J., Yung, M., Li, N.
    (eds.) ACM SIGSAC Conference on Computer and Communications Security, pp.
    299–309. ACM (2014)
13. Cimatti, A., et al.: NuSMV 2: An opensource tool for symbolic model checking. In:
    Brinksma, E., Larsen, K.G. (eds.) Computer Aided Veriﬁcation, 14th International
    Conference, CAV 2002,Copenhagen, Denmark, July 27-31, 2002, Proceedings. Lec-
    ture Notes in Computer Science, vol. 2404, pp. 359–364. Springer (2002). https://
    doi.org/10.1007/3-540-45657-0_29
14. Erbsen, A., Philipoom, J., Gross, J., Sloan, R., Chlipala, A.: Simple high-level
    code for cryptographic arithmetic - with proofs, without compromises. In: IEEE
    Symposium on Security and Privacy, pp. 1202–1219. IEEE (2019)
15. Esparza, J., Lammich, P., Neumann, R., Nipkow, T., Schimpf, A., Smaus, J.: A
    fully veriﬁed executable LTL model checker. In: Sharygina, N., Veith, H. (eds.)
    Computer Aided Veriﬁcation - 25th International Conference, CAV 2013, Saint
    Petersburg, Russia, July 13-19, 2013. Proceedings. Lecture Notes in Computer
    Science, vol. 8044, pp. 463–478. Springer (2013). https://doi.org/10.1007/978-3-
    642-39799-8_31
16. Fu, Y.F., Liu, J., Shi, X., Tsai, M.H., Wang, B.Y., Yang, B.Y.: Signed cryptographic
    program veriﬁcation with typed cryptoline. In: Cavallaro, L., Kinder, J., Wang,
    X., Katz, J. (eds.) ACM SIGSAC Conference on Computer and Communications
    Security, pp. 1591–1606. ACM (2019)
17. Gonthier, G., Mahboubi, A.: An introduction to small scale reﬂection in Coq. J.
    Formalized Reason. 3(2), 95–152 (2010)
18. Google: Boringssl (2021). https://boringssl.googlesource.com/boringssl/
19. Greuel, G.M., Pﬁster, G.: A Singular Introduction to Commutative Algebra.
    Springer-Verlag (2002)
20. Harrison, J.: Automating elementary number-theoretic proofs using Gröbner bases.
    In: Pfenning, F. (ed.) CADE 2007. LNCS (LNAI), vol. 4603, pp. 51–66. Springer,
    Heidelberg (2007). https://doi.org/10.1007/978-3-540-73595-3_5
21. Holzmann, G.J.: The SPIN Model Checker - primer and reference manual. Addison-
    Wesley (2004)
         CoqCryptoLine: A Veriﬁed Model Checker with Certiﬁed Results              239

22. Lamport, L.: Specifying Systems, The TLA+ Language and Tools for Hardware
    and Software Engineers. Addison-Wesley (2002). http://research.microsoft.com/
    users/lamport/tla/book.html
23. Larsen, K.G., Pettersson, P., Yi, W.: UPPAAL in a nutshell. Int. J. Softw. Tools
    Technol. Transf. 1(1-2), 134–152 (1997). https://doi.org/10.1007/s100090050010
24. Liu, J., Shi, X., Tsai, M.H., Wang, B.Y., Yang, B.Y.: Verifying arithmetic in cryp-
    tographic C programs. In: Lawall, J., Marinov, D. (eds.) IEEE/ACM International
    Conference on Automated Software Engineering, pp. 552–564. IEEE (2019)
25. Mozilla: Network security services (2021). https://developer.mozilla.org/en-US/
    docs/Mozilla/Projects/NSS
26. Myreen, M.O., Curello, G.: Proof Pearl: a veriﬁed bignum implementation in x86-
    64 machine code. In: Gonthier, G., Norrish, M. (eds.) CPP 2013. LNCS, vol. 8307,
    pp. 66–81. Springer, Cham (2013). https://doi.org/10.1007/978-3-319-03545-1_5
27. Neumann, R.: Using promela in a fully veriﬁed executable LTL model checker.
    In: Giannakopoulou, D., Kroening, D. (eds.) Veriﬁed Software: Theories, Tools
    and Experiments - 6th International Conference, VSTTE 2014, Vienna, Austria,
    July 17-18, 2014, Revised Selected Papers. Lecture Notes in Computer Science,
    vol. 8471, pp. 105–114. Springer (2014). https://doi.org/10.1007/978-3-319-12154-
    3_7
28. Niemetz, A., Preiner, M., Biere, A.: Boolector 2.0. J. Satisﬁability, Boolean Mod-
    eling Comput. 9(1), 53–58 (2014)
29. Nipkow, T., Wenzel, M., Paulson, L.C. (eds.): Isabelle/HOL. LNCS, vol. 2283.
    Springer, Heidelberg (2002). https://doi.org/10.1007/3-540-45949-9
30. OpenSSL: OpenSSL library. https://github.com/openssl/openssl (2021)
31. Polyakov, A., Tsai, M.H., Wang, B.Y., Yang, B.Y.: Verifying arithmetic assembly
    programs in cryptographic primitives. In: Schewe, S., Zhang, L. (eds.) Interna-
    tional Conference on Concurrency Theory, pp. 4:1–4:16. LIPIcs, Schloss Dagstuhl
    - Leibniz-Zentrum fuer Informatik (2018)
32. Pottier, L.: Connecting Gröbner bases programs with Coq to do proofs in algebra,
    geometry and arithmetics. In: Rudnicki, P., Sutcliﬀe, G., Konev, B., Schmidt, R.A.,
    Schulz, S. (eds.) Proceedings of the LPAR 2008 Workshops, Knowledge Exchange:
    Automated Provers and Proof Assistants, and the 7th International Workshop on
    the Implementation of Logics, Doha, Qatar, November 22, 2008. CEUR Workshop
    Proceedings, vol. 418. CEUR-WS.org (2008). http://ceur-ws.org/Vol-418/paper5.
    pdf
33. Shi, X., Fu, Y.F., Liu, J., Tsai, M.H., Wang, B.Y., Yang, B.Y.: CoqQFBV: a
    scalable certiﬁed SMT quantiﬁer-free bit-vector solver. In: Leino, R., Silva, A.
    (eds.) International Conference on Computer Aided Veriﬁcation. Springer, Lecture
    Notes in Computer Science (2021)
34. Sprenger, C.: A veriﬁed model checker for the modal µ-calculus in Coq. In: Steﬀen,
    B. (ed.) Tools and Algorithms for Construction and Analysis of Systems, 4th Inter-
    national Conference, TACAS ’98, Held as Part of the European Joint Conferences
    on the Theory and Practice of Software, ETAPS’98, Lisbon, Portugal, March 28
    - April 4, 1998, Proceedings. Lecture Notes in Computer Science, vol. 1384, pp.
    167–183. Springer (1998). https://doi.org/10.1007/BFb0054171
35. The Bitcoin Developers: Bitcoin source code (2021). https://github.com/bitcoin/
    bitcoin
36. Tsai, M.H., Fu, Y.F., Shi, X., Liu, J., Wang, B.Y., Yang, B.Y.: Automatic certiﬁed
    veriﬁcation of cryptographic programs with COQCRYPTOLINE. IACR Cryptol.
    ePrint Arch. p. 1116 (2022)
240     M.-H. Tsai et al.

37. Tsai, M.H., Wang, B.Y., Yang, B.Y.: Certiﬁed veriﬁcation of algebraic properties
    on low-level mathematical constructs in cryptographic programs. In: Evans, D.,
    Malkin, T., Xu, D. (eds.) ACM SIGSAC Conference on Computer and Communi-
    cations Security, pp. 1973–1987. ACM (2017)
38. Wimmer, S.: Munta: A veriﬁed model checker for timed automata. In: André,
    É., Stoelinga, M. (eds.) Formal Modeling and Analysis of Timed Systems - 17th
    International Conference, FORMATS 2019, Amsterdam, The Netherlands, August
    27-29, 2019, Proceedings. Lecture Notes in Computer Science, vol. 11750, pp. 236–
    243. Springer (2019). https://doi.org/10.1007/978-3-030-29662-9_14
39. Wimmer, S., Lammich, P.: Veriﬁed model checking of timed automata. In: Beyer,
    D., Huisman, M. (eds.) Tools and Algorithms for the Construction and Analysis
    of Systems - 24th International Conference, TACAS 2018, Held as Part of the
    European Joint Conferences on Theory and Practice of Software, ETAPS 2018,
    Thessaloniki, Greece, April 14-20, 2018, Proceedings, Part I. Lecture Notes in
    Computer Science, vol. 10805, pp. 61–78. Springer (2018). https://doi.org/10.1007/
    978-3-319-89960-2_4
40. Zinzindohoué, J.K., Bhargavan, K., Protzenko, J., Beurdouche, B.: HACL*: A
    veriﬁed modern cryptographic library. In: ACM SIGSAC Conference on Computer
    and Communications Security, pp. 1789–1806. ACM (2017)




Open Access This chapter is licensed under the terms of the Creative Commons
Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/),
which permits use, sharing, adaptation, distribution and reproduction in any medium
or format, as long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons license and indicate if changes were
made.
     The images or other third party material in this chapter are included in the
chapter’s Creative Commons license, unless indicated otherwise in a credit line to the
material. If material is not included in the chapter’s Creative Commons license and
your intended use is not permitted by statutory regulation or exceeds the permitted
use, you will need to obtain permission directly from the copyright holder.
