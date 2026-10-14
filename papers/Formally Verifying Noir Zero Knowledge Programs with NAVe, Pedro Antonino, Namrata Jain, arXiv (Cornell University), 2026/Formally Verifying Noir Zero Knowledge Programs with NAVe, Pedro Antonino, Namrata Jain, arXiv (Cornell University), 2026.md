                                                Formally Verifying Noir Zero Knowledge
                                                         Programs with NAVe

                                                                Pedro Antonino and Namrata Jain

                                                            The Blockhouse Technology Ltd., Oxford, UK
                                                                    {pedro,namrata}@tbtl.com
                                                                          www.tbtl.com
arXiv:2601.09372v1 [cs.CR] 14 Jan 2026




                                               Abstract. Zero-Knowledge (ZK) proof systems are cryptographic pro-
                                               tocols that can (with overwhelming probability) demonstrate that the
                                               pair (X, W ) is in a relation R without revealing information about the
                                               private input W . This membership checking is captured by a complex
                                               arithmetic circuit: a set of polynomial equations over a finite field. ZK
                                               programming languages, like Noir, have been proposed to simplify the
                                               description of these circuits. A developer can write a Noir program using
                                               traditional high-level constructs that can be compiled into a lower-level
                                               ACIR (Abstract Circuit Intermediate Representation), which is essen-
                                               tially a high-level description of an arithmetic circuit. In this paper, we
                                               formalise some of the ACIR language using SMT-LIB and its extended
                                               theory of finite fields. We use this formalisation to create an open-source
                                               formal verifier for the Noir language using the SMT solver cvc5. Our
                                               verifier can be used to check whether Noir programs behave appropri-
                                               ately. For instance, it can be used to check whether a Noir program has
                                               been properly constrained, that is, the finite-field polynomial equations
                                               generated truly capture the intended relation. We evaluate our verifier
                                               over 4 distinct sets of Noir programs, demonstrating its practical appli-
                                               cability and identifying a hard-to-check constraint type that charts an
                                               improvement path for our verification framework.

                                               Keywords: Zero Knowledge Proofs · Zero Knowledge Programs · Noir
                                               · Privacy · Formal Verification


                                         1   Introduction
                                         Zero Knowledge (ZK) proof systems were initially introduced as interactive pro-
                                         tocols [21, 22, 20] where a prover P convinces a verifier V of a statement of the
                                         form R(X, W ) where R is a relation (known to P and V), X is an input common
                                         to both P and V, and W is an input private to the prover (commonly referred
                                         to as a witness); the protocol’s execution must reveal nothing about W apart
                                         from the fact that R(X, W ) holds. These proof systems have been made non-
                                         interactive [17, 23] and (their generated proof) succinct [19, 32, 24, 26]. ZK proof
                                         systems have gained renewed interest with the advent of blockchains and the
                                         growth of the Web3 ecosystem. They have been promoted as a technology to
                                         deliver privacy [1, 12] and, even, improve the efficiency of blockchains [10, 7].
2       P. Antonino and N. Jain

    In these proof systems, the relation R is typically captured by an arithmetic
circuit: a set of constraints (i.e. polynomial equations) over a finite field that
capture the relationship between X and W . If one is not familiar with such sys-
tems, describing these circuits can be challenging. To simplify the use of these
systems and increase their adoption, Domain-Specific Languages (DSLs) target-
ing arithmetic circuits have been developed. These ZK programming languages
provide high-level constructs and an infrastructure to compile these constructs
into arithmetic circuits used by ZK proof systems; Noir [8], Cairo [2], and (in
a lower level of abstraction) Circom [3] are examples of such languages. Sim-
ply put, they can be used to create a high-level program P that captures R: if
R(X, W ) holds, the program P successfully runs with parameters (X, W ).
    The Noir language [8] was proposed by the Aztec community [1]. It can be
used to both create independent ZK programs and private smart contracts for
the Aztec network; smart contracts are a type of program that manages digital
assets sometimes worth large amounts of money. Noir programs are compiled
into an intermediate language called ACIR (Abstract Circuit Intermediate Rep-
resentation), which is then used by a ZK proof system. This intermediate rep-
resentation has opcodes capturing finite-field polynomial equations, but it also
has higher-level opcodes, such as range check — a constraint that ensures that
a finite-field value can be represented with a determined number of bits — and
brillig call — an opcode that allows the execution of unconstrained code. Uncon-
strained code is a feature of these languages designed to help the prover produce
a proof, but it does not contribute to the underlying constraints capturing the
relation R. The programmer is expected to include separately the appropriate
matching constraints using, for instance, the assert command in Noir.
    This new programming paradigm is prone to several subtle types of bugs [9,
18]. For instance, a lack of appropriate constraining in the Noir program, say if it
executes unconstrained code that was not appropriately constrained, can lead to
a divergence between the program P and the underlying relation it is trying to
capture R. This type of bug has already led to serious real-world vulnerabilities;
see [13], for instance. ZK programs can also suffer from other types of bugs,
such as non-determinism — the underlying relation was meant to be a function,
but it is not — and even compiler bugs — the constraints generated do not
appropriately capture the behaviour of the high-level programming constructs.
The subtlety of these bugs and the increased application of ZK programs in
high-stakes contexts — protecting users’ private information or managing large
sums of digital assets — make them a perfect target for formal verification.
    In this paper, we formalise a subset of ACIR using SMT-LIB [16] and propose
NAVe: the Noir Acir (formal) Verifier; not to be confused with the underlying ZK
proof system verifier. We encode the semantics of a subset of the ACIR opcodes
into SMT-LIB. We propose two encodings: one based on the standard theory of
integer arithmetic and another based on a non-standard theory of finite fields [29,
30] that is implemented in the cvc5 solver [15]. We use this formalisation(s)
and the convention of capturing verification goals/proof obligations using the
Noir function verify_assert(b: bool) to create our open-source formal verifier
              Formally Verifying Noir Zero Knowledge Programs with NAVe           3

NAVe. Our verifier focuses on identifying unconstrained bugs: a Noir developer
can use verify_assert call at the program’s exit point to specify the desired
relation R it is expected to capture. We have integrated our verifier into Nargo,
Noir’s package manager, to ease developers into using it. We have evaluated our
verifier in some test programs that are part of the Noir language infrastructure
to assess its efficiency in practice. We analyse its performance using both of our
encodings with encouraging results. This evaluation suggests that: (a) some types
of constraints, induced by opcodes like range checks, can significantly increase
verification time and that (b) our encodings are complementary in the sense
that some programs are more quickly analysed using one and some others using
the other. So, our evaluation charts a path for future work: we need to propose
abstractions/approximations to address (a) and some form of analysis of a Noir
program with both encodings concurrently to benefit from (b).
    There has been some work on the automated formal verification of ZK pro-
grams [28, 31, 33], none of which targets the Noir language and its particular-
ities. Noir has high-level constructs with complex semantics. For instance, un-
like other languages, Noir/ACIR supports high-level memory operations, uncon-
strained functions, and bit-level operations like range checks, bitwise operators,
etc. Lampe [6] captures the semantics of Noir using Lean 4 [27]. Unlike our au-
tomated verifier, the Lampe user has to interactively drive the proof of program
properties. We chose to formalise ACIR instead of Noir directly, as the former
should be more stable and undergo fewer evolutionary changes than the latter.
Also, our formalisations could be used by other languages built to target ACIR.
    To sum up, our contributions are:
 – Formalisations of ACIR (and indirectly Noir) using SMT-LIB standard the-
   ory of integer arithmetic and the non-standard theory of finite fields [29].
 – An open-source formal verifier, NAVe, for the Noir programming language
   based on our formalisation, which is integrated into the popular Noir package
   manager (and build tool) Nargo.
 – An evaluation of NAVe on Noir test programs that demonstrate its practical
   applicability and identifies a class of complex constraints and solver/encoding
   combinations, charting a path for future improvement.
Outline. In Section 2, we present the necessary background to make our paper
self-contained. Section 3 introduces our formalisation(s), verifier, and its evalua-
tion. Section 4 presents some related work and Section 5 our concluding remarks.


2     Background
In this section, we introduce some concepts to make our paper self-contained.

2.1   SMT-LIB, CVC5, and Finite Field Theory
Satisfiability Modulo Theories (SMT) generalises boolean satisfiability to other
theories such as integer arithmetic. An SMT formula involves predicates in
4         P. Antonino and N. Jain

these theories that can be combined using boolean operators. SMT solvers, like
cvc5 [15], are tools implementing decision procedures to verify the satisfiability
of such formulas. SMT-LIB [16] is a library that standardises some of these the-
ories, providing the semantics and syntax for those. It has become the de-facto
standard syntax to represent these formulas. So, even theories that are not SMT-
LIB standard use its syntax. For instance, (declare-const x Int) can be used to
declare a constant x of type/sort Int, whereas (assert (or (= x 0) (= x 1)))
declares the constraint that x is either 0 or 1. And one can use (+ x y), (* x y),
and (mod x y) to construct the corresponding typical integer operations.
    The cvc5 solver also supports the non-standard theory of finite fields of prime
order [4] described in [29]. A finite field of prime order p is isomorphic to the
integers modulo p. For integer x and positive integer y, we use (x mod y) to
denote the unique integer r such that q is an integer, x = qy + r and 0 ≤ r < y.
Let p be a prime number, F be the sort representing a field of prime order p, N
be an integer, xi be terms capturing field values in the same field F , and [x] be
the integer denoted by the finite-field term x.
    – (_ FiniteField p) denotes the field of prime order p sort, i.e. the set of
      integers modulo p.
    – (as ffN F ) denotes the finite field element N , i.e. the integer (N mod p).
    – (ff.add x1 . . . xn ) captures the n-ary field addition operation. This term
      denotes the integer ([x1 ] + . . . + [xn ] mod p).
    – (ff.mul x1 . . . xn ) captures the n-ary field multiplication operation. This
      term denotes the integer ([x1 ] × . . . × [xn ] mod p).
    – (ff.bitsum x1 . . . xn ) captures the n-ary bitsum operation. This term de-
      notes the integer (20 [x1 ] + . . . + 2n−1 [xn ] mod p).
    – (= x y ) denotes the equality operator. For the integers denoted by [x] and
      [y], this equality holds if and only if [x] = [y].
   The isomorphism between the field of prime order p and the integers modulo
p means that one can encode finite-field terms as non-linear integer arithmetic
terms and use a solver for this theory to check for satisfiability; this problem is
undecidable in general, however, whereas it is decidable for finite-field terms.

2.2     Noir
Noir [8] is a ZK programming language that was proposed by the Aztec [1]
community. It can be used to either construct stand-alone programs or smart
contracts for the Aztec network. Noir is a high-level programming language
whose syntax is inspired by Rust [11]. Like in Rust, abstract data types can be
created via structs and their corresponding implementation. Unlike traditional
programming languages, Noir has a built-in Field type denoting a finite field
and field operations like addition and multiplication. The actual field depends
on the (backend) proof system used. For Noir’s default backend, a field element
would be a 254-bit integer that spans the Grumpkin curve [5]1 . Another pe-
1
    The finite field has order 218882428718392752222464057452572750885483644004160
    34343698204186575808495617.
                Formally Verifying Noir Zero Knowledge Programs with NAVe           5


fn main(x: Field) -> pub Field {                fn main(x: Field) -> pub Field {
    let invx: Field = inv(x);                       let mut invx = 0;
    invx                                            unsafe {
}                                                       invx = invu(x);
                                                    }
fn inv(x: Field) -> Field {                         assert(invx * x == 1);
    let mut cur = x;                                invx
    let mut y = 1;                              }
    let rep: [u1; 253] =
        [1,1,. . . omitted . . .];              unconstrained fn invu(x: Field)
    for i in 0..253 {                               -> Field {
        if (rep[i] == 0) {                              inv(x)
            cur = cur * cur;                    }
        } else {
            y = y * cur;
            cur = cur * cur;
        }
    }
    y * cur
}

                 Fig. 1. Noir programs: constrained vs unconstrained.



culiarity of ZK programming languages is the distinction between constrained
and unconstrained code. While the former gives rise to arithmetic-circuit con-
straints, the latter does not, and it has to be combined with separate constraints
manually added by the developer. Unconstrained code can greatly reduce the
size and complexity of the underlying arithmetic circuit generated, improving
proving and verification times.
    We briefly present the Noir language and the advantages of unconstrained
code with the Noir programs in Figure 1. The multiplicative inverse of a non-zero
element x in a finite field can be calculated by computing xp−2 , by Fermat’s little
theorem, where p is the prime order of the field. Both the left- and right-hand side
programs, denoted by the respective main functions, compute the public value
xp−2 , denoted by the pub Field return type, from the private value x. With this
program, a prover can convince a verifier that it knows x for the public value xp−2
without revealing x.2 The left-hand side Noir program uses constrained code to
carry out this computation, whereas the right-hand side one uses unconstrained
code. In Noir, the let keyword is used to declare a variable, and the mut modifier
denotes that the variable is mutable. The inv function uses iterative squaring [25]
to compute xp−2 : a for-loop iterates over the binary iterative decomposition rep

2
    These programs can be found at https://github.com/pedrotbtl/nave. They are a
    didactic tool to demonstrate the discrepancy between constrained and unconstrained
    code. Noir has built-in unconstrained code and constraints to calculate 1/x, and a
    verifier could compute x from xp−2 , bypassing the program’s privacy guarantees.
6       P. Antonino and N. Jain

of p − 2 to carry out this exponentiation. For this example, we use p, the prime
order of the Grumpkin base field, and we omit this 253-bit array from the code
for brevity. The right-hand side uses the same inv (inside function invu) code
but in an unconstrained way and relies on the assert(invx * x == 1) statement
to ensure the output invx, calculated in an unconstrained way, is the inverse of x;
the assert command generates constraints for the underlying arithmetic circuit.
While the left-hand side Noir program generates 379 constraints, the right-hand
side one only generates 2. In ZK programs, unconstrained code helps the prover
in generating a proof. In this case, in a ZK proof system, the prover needs to
compute the inverse of x to create a proof. For the ZK verification, however, the
verifier only needs to check that invx is the inverse of x.


3     NAVe: a formal verifier for Noir programs

In this section, we formalise Noir’s ACIR, propose a formal program verifier
called NAVe, and conduct an evaluation to assess NAVe’s practical applicability.


3.1   ACIR formalisation

A Noir program is compiled into an intermediate ACIR program, which is later
translated into an arithmetic circuit targeting a specific ZK proof system. ACIR
is designed to decouple the frontend high-level ZK language from the backend
ZK proving system. It was created by the Aztec community for Noir, but it
is designed to be high-level-language agnostic. We decided to target ACIR as
opposed to Noir directly to: (a) benefit from the infrastructure used to compile
Noir programs into ACIR and the lower-level nature of ACIR makes it simpler
to capture its semantics, (b) for as long as this intermediate language is stable,
and it should be stabler than Noir, our formal verifier should remain compatible
with Noir as it evolves into new versions, and (c) as ACIR was designed to be
frontend agnostic, our ACIR semantics could be used in the future to verify other
high-level ZK languages targeting ACIR as their intermediate representation.
    The ACIR language has 6 opcodes: AssertZero, BlackBoxFuncCall, MemoryOp,
MemoryInit, BrilligCall, and Call. In this work, we only formalise a subset of
ACIR. We do not formalise the Call opcode and some of the behaviour of the
BlackBoxFuncCall opcode; we leave that as future work. Functions in Noir are
typically inlined, so the Call opcode is only used in some specific, and somewhat
intricate, proving scenarios using recursive proving. As for the BlackBoxFuncCall,
some of its behaviour is quite complex as we detailed later.
    For a given finite field, an ACIR program consists of a list of ACIR opcodes
⟨op1 , . . . , opm ⟩ operating on field variables, which are called witnesses, and a
list of brilling functions; the latter is not relevant for this paper. Opcodes can
be seen as creating constraints limiting which values the witnesses can take,
and a valid assignment for the witnesses captures an execution of the ACIR
program. In the following, we formalise the semantics of opcodes via SMT-LIB,
namely, we define the constraints that capture each of ACIR opcodes’ behaviour.
                  Formally Verifying Noir Zero Knowledge Programs with NAVe                           7

We propose a translation of ACIR opcodes both into a non-standard SMT-LIB
theory of finite fields (see Section 2) and the standard theory of integers.
     Some opcodes operate over an ACIR Expression: a datatype representing a
polynomial of degree at most 2. Let ri , si , q be (literal) field elements and ai , bi , ci
witnesses. This datatype is a triple containing: an n-long list of triples of the form
(ri , ai , bi ), an m-longP
                          list of pairs (sP
                                          i , ci ), and a field element q, and it represents
                            n                 m
the field polynomial i=1 ri ai bi + j=1 sj cj + q. We capture this expression in
SMT-LIB as follows. Both ACIR and SMT-LIB variables span over the same
finite field F . We use JtKf to denote our encoding for ACIR term t (be it an
opcode or expression) using the finite-field theory. To simplify our presentation,
we omit the encoding of field elements: the value v is, of course, encoded as
(as ffv F ) where F is a sort definition for the appropriate field.

J(⟨(r1 , a1 , b1 ), . . . , (rn , an , bn )⟩, ⟨(s1 , c1 ), . . . , (sm , cm )⟩, q) : ExpressionKf ≡
   (ff.add (ff.mul r1 a1 b1 ) . . . (ff.mul rn an bn )
         (ff.mul s1 c1 ) . . . (ff.mul sm cm ) q )

    We rely on the isomorphism between modular integer arithmetic and field
arithmetic to propose an alternative ACIR encoding via SMT-LIB standard
theory of integers; we use JtKi to denote this formalisation. In the following
SMT-LIB formula, ri , si , q are (literal) integers and ai , bi , ci are integer variables.

J(⟨(r1 , a1 , b1 ), . . . , (rn , an , bn )⟩, ⟨(s1 , c1 ), . . . , (sm , cm )⟩, q) : ExpressionKi ≡
   (mod (+ (* r1 a1 b1 ) . . . (* rn an bn )(* s1 c1 ) . . . (* sm cm ) q ) p)

    The AssertZero opcode gives rise to a polynomial-equation constraint. For an
ACIR
Pn expression  Pm exp, this opcode induces the polynomial-equation constraint
      r a b
   i=1 i i i +   j=1 sj cj + q = 0. The integer translation is the same, but for the
integer expression encoding.

JAssertZero(exp)Kf ≡ (= JexpKf 0)

    For instance, the opcode AssertZero(⟨(1, w1 , w2 )⟩, ⟨⟩, −1) captures the con-
straint w1 w2 − 1 = 0, namely, that w2 is the multiplicative inverse of w1 . This
type of opcode is generated, for instance, by Noir statement assert(invx * x = 1).
    The BlockBoxFuncCall opcode allows the execution of black box functions.
They encompass behaviours that cannot usually be efficiently captured by poly-
nomial constraints such as the ones generated by AssertZero opcodes. They are
designed to give the underlying ZK proof system some flexibility in providing its
own optimised circuits to capture these functions. ACIR supports 14 block box
functions: varying from range checking to complex hash functions and encryp-
tion computations. In this paper, we have only provided a formalisation of the
Range black box function; we leave the formalisation of the other functions as
future work. For a witness x and an integer n, the Range(x, n) function checks
that the value of x can be encoded as an n-bit-long unsigned integer. We use a
binary representation of x to implement this check. We use new field variables
8        P. Antonino and N. Jain

                                                                     Pn
y1 , . . . , yn to encode a bitsum representation for x, that is, x = i=1 2i−1 yi , and
we enforce that yi represent a binary value with constraint yi (yi − 1) = 0.

JBlockBoxFuncCall(Range(x, n))Kf ≡
    (= (ff.bitsum y1 . . . yn ) x)∧
      (= (ff.mul y1 (ff.add y1 −1)) 0) ∧ . . . ∧ (= (ff.mul yn (ff.add yn −1)) 0)

Similar black box functions, like AND and XOR, representing bit-level logical
and and xor, respectively, can be formalised using this binary representation.
   Unlike the finite-field encoding, the integer-arithmetic formalisation can rely
on the intrinsic order of the integers to implement this check.

JBlockBoxFuncCall(Range(x, n))Ki ≡ (< x 2n )

    The MemoryOp and MemoryInit opcodes give ACIR the ability to create, access,
and mutate arrays of (new) witnesses. These arrays are identified by a memory
block id. Our encodings also need a way to track when arrays have been mutated.
We use mid,i,j to represent the value of the element i of array (i.e. memory block)
id after j mutations. For instance, m2,1,0 gives the element at index 1 for array
2 at initialisation, whereas m2,1,1 gives the value for the same element and array
after the first write. We translate/encode memory operations sequentially and
keep track of the mutation index of arrays with the map mi. So, mi is part of
the translation context, and it is updated when an array is created and updated.
We do not add it to the translation rules for the sake of conciseness.
    The MemoryInit opcode creates an array of new witnesses.3 Given a block
identifier (an unsigned 32-bit integer) id and witnesses x1 , . . . , xn as inputs, for
each input witness xi , this opcode generates a new (fresh) witness mid,i,0 with
the same value as xi . As part of this operation, the mutation index map is
updated as follows mi′ = mi ⊕ {id → 0}, where mi′ and mi are the value of the
map after and before the translation, respectively, and ⊕ adds a new maplet to
the map or updates it if there already existed another maplet with the same id.

JMemoryInit(id, ⟨x1 , . . . , xn ⟩)Kf ≡ (= mid,1,0 x1 ) ∧ . . . ∧ (= mid,n,0 xn )

    The MemoryOp opcode can be used to read from and write into memory blocks.
Its inputs are a block identifier id, a memory operation op (can be 0 for a read
or 1 for a write), an index ACIR expression ind and a value ACIR expression
val. A read copies the value at index ind into the witness given by val. Note how
we use the value mi(id) to identify the witnesses representing the current state
of the array and how the implication identifies the correct index to be accessed.
There is no change in the state of the array, and hence to mi.

JMemoryOp(id, op = 0, ind, val)Kf ≡ (=> (= JindKf 1) (= mid,1,mi(id) JvalKf ))∧
    . . . ∧ (=> (= JindKf n) (= mid,n,mi(id) JvalKf ))
3
    ACIR allows for different memory block types. Here, we only formalise the more
    general Memory type.
                   Formally Verifying Noir Zero Knowledge Programs with NAVe                                               9

   A write mutates the value at index ind to val. Note how we use the value
mi(id) and mid(id) + 1 to identify the witnesses representing the current and
the next state of the array, respectively. The first set of conjunctions is very
similar to a read, apart from the fact that they constrain the next state of the
array mi(id), and they define what happens to the element being written to.
The second set of conjuncts defines what happens to the elements of the array
that are not written to; that is, they retain their previous value. The mutation
mapping mi is also updated: mi′ = mi ⊕ {id → mi(id) + 1}.

JMemoryOp(id, op = 1, ind, val)Kf ≡ (=> (= JindKf 1) (= mid,1,mi(id)+1 JvalKf ))∧
    . . . ∧ (=> (= JindKf n) (= mid,n,mi(id)+1 JvalKf ))∧
    (=> (not (= JindKf 1)) (= mid,1,mi(id)+1 mid,1,mi(id) ))∧
    . . . ∧ (=> (not (= JindKf n)) (= mid,n,mi(id)+1 mid,n,mi(id) ))

    The modular integer formalisation for memory opcodes mirrors the above
definitions by using corresponding integer witnesses and expression encoding.
    Finally, BrilligCall opcodes capture unconstrained code. As we are inter-
ested in analysing and formalising constrained code, whose execution integrity
is enforced by the underlying ZK proof system, we do not translate these op-
codes, or perhaps more appropriately, they are translated as the always satisfied
constraint true.

3.2     Verifier
We propose NAVe: a formal verifier for Noir programs based on our SMT-LIB
semantics — its high-level architecture is given in Figure 2. It relies on the Noir
infrastructure for compiling Noir programs into ACIR, and cvc5 [8] to solve the
SMT constraints generated by our semantics (i.e. SMT-LIB translations). Our
verifier is publicly available in our repository.4
    We use the basic Noir program in Figure 3 to demonstrate the usage of
our formal verification framework. A Noir program can be annotated with a
verify_assert(cond). Unlike a built-in Noir assert which creates a constraint,
this formal verification function creates a proof obligation: the condition cond
must hold at the point of that statement. The cond is a side-effect-free predicate
over the variables in scope at that point in the program. For now, this is a simple,
unquantified Noir expression. This verification function must be declared by the
4
    https://github.com/pedrotbtl/nave


                                                                        NAVe
    Noir program
                                  ACIR program                             SMT constraints
                                 AssetZero (1,x1,x2) -1
                                 AssetZero (1,x3,x4) -1
                                                                         (= (ff.add (ff.mul x1 x2) -1) 0)
                                                                         (= (ff.add (ff.mul x3 x4) -1) 0)
                                                                                                                    cvc5
                   Compilation                            Translation    (= (ff.add (ff.mul x5 x6) -1) 0)
                                                                                                            Input
                                 AssetZero (1,x5,x6) -1




                            Fig. 2. Overview of NAVe formal verifier.
10      P. Antonino and N. Jain


fn main(x : Field) {
    assert(x * (x - 1) == 0);
    unsafe { verify_assert((x == 0) | (x == 1)); }
}

unconstrained fn verify_assert(b: bool) {}

                          Fig. 3. Basic example program.



user of NAVe, like in the basic example program. This approach minimises the
changes to the Noir language infrastructure. We do not have to add new lan-
guage constructs (and define their parsing, compilation, etc) to track verification
conditions. Instead, we intercept at the ACIR-level a call to this specific func-
tion and do the appropriate translation into a verification condition. Moreover,
this function does not modify the behaviour of the Noir program at all. As it is
an unconstrained function, it does not contribute constraints to the underlying
arithmetic circuit, and its execution does nothing. So, developers can annotate
their programs with these formal verification constructs without impacting their
corresponding ZK proof generation and verification.
    NAVe is implemented (in a public fork of and) as a command (formal-verify)
of the Nargo package manager. We hope that by using a tool that is familiar
to Noir developers, they will be more comfortable making use of NAVe. For a
Noir program P , we use the Noir compiler to generate the ACIR program A.
We use our formalisation to translate A into an SMT formula JAKf ; we trans-
late opcodes sequentially as per the ACIR program, conjoining the constraints
generated for each opcode. For each verification condition in the ACIR program,
these are BrilligCall opcodes capturing verify_assert(cond) statements in the
Noir program, we recover the boolean ACIR Expression expcond representing the
cond, and we create the formula F = JAKf ∧ ¬Jexpcond Kf . The modular integer
encoding can be used instead of the finite field one, if preferred, of course. We
then use the cvc5 SMT solver to check the satisfiability of each of these F formu-
las. Unsatisfiability means that the verification condition holds. A satisfiable for-
mula, however, represents the failure of the corresponding verification condition,
namely, there is a program execution that falsifies the corresponding predicate
at the given program point. In this case, cvc5 generates a model, i.e. a satisfying
assignment to the witnesses (including the ones representing the input param-
eters of the Noir program). This model represents a counterexample detailing
how the verification condition is falsified, which is passed back to the developer
to help debug the program. For instance, in Figure 3, we use NAVe to verify
that the program input x is either 0 or 1; it checks that the x * (x - 1) == 0
constraining works as expected, and a | b captures a disjunction between a and
b. If one of the disjuncts in the verification condition is removed, however, NAVe
returns a model demonstrating that x can take that value too, namely, if we
remove (x == 1), NAVe offers a counterexample where x = 1.
               Formally Verifying Noir Zero Knowledge Programs with NAVe             11

3.3    Evaluation

We evaluate our Noir program formal verifier in practice. We analyse its perfor-
mance on some test programs that are part of the Noir language infrastructure.
They come from the Noir repository, but we have annotated them with verifica-
tion conditions. We tried to collect programs that had a mix of complexity and
adhered to the ACIR subset that we have formalised. We have created sets of
test programs with both verified and falsified conditions to analyse the behaviour
of the solver with these two distinct types of searches. Moreover, we have also
created sets of programs with and without range checks — i.e. BlackBoxFuncCall
opcodes calling function Range(x, n). We wanted to analyse the performance of
the solver, and consequently of our verifier, in analysing the type of complex bit-
sum constraints they induce. We have carried out our evaluation on a dedicated
machine with Intel Core i7-9750H CPU @ 2.60GHz x 12, and 16GB of RAM,
running Ubuntu 22.04.5 LTS. The test programs that we used and instructions
on how to reproduce our evaluation are available in our repository.5
    In Table 1, we present the results for running NAVe in two sets of programs
without range check constraints: one set has programs with verified verification
conditions, and the other one falsified conditions. We test both of our encodings.
For the finite-field one, we also tested two cvc5 finite-field solver configurations:
5
    https://github.com/pedrotbtl/nave


                                                             Falsified
                 Verified
                                                    Benchmark           Time(s)
          Benchmark       Time(s)
                                                 id        #w #o sp gb int
       id      #w #o sp gb int
                                                 pnf1      189 126 42.5 22.9 t
       pnv1     1   1 17.5 20.3 17.8
                                                 pnf2       5    4 18.9 17.9 t
       pnv2     1   2 16.0 22.3 17.3
                                                 pnf3       3    2 16.0 18.2 16.6
       pnv3     6   6 18.9 20.2 t
                                                 pnf4       6    4 17.8 18.0 19.1
       pnv4     17 18 16.2 18.8 t
                                                 pnf5       9 10 17.3 19.1 t
       pnv5     1   1 17.5 17.1 19.0
                                                 pnf6       20 3 18.1 18.9 16.0
       pnv6    207 139 18.5 17.9 17.2
                                                 pnf7       4    3 17.9 17.6 15.0
       pnv7     1   1 18.2 16.8 20.3
                                                 pnf8       12 6 17.6 18.9 14.8
       pnv8    285 286 19.2 17.1 19.7
                                                 pnf9       2    2 16.8 18.7 14.8
       pnv9     4   4 18.4 16.7 t
                                                 pnf10      9    5 17.1 18.4 14.6
       pnv10    1   1 19.0 15.7 17.8
                                                 pnf11      1    1 17.5 18.8 16.0
       pnv11    1   2 20.1 17.0 17.5
                                                 pnf12      2    2 16.3 18.5 t
       pnv12    5   4 17.4 17.4 15.2
                                                 pnf13      63 64 16.6 16.5 17.4
Table 1. Results for Noir programs without range constraints with verification con-
ditions verified and falsified, respectively. The column id identifies the program being
tested, column #w gives the program’s number of witnesses, and column #o the num-
ber of ACIR opcodes excluding BrilligCalls. Columns sp and gb give the program
analysis time for our ACIR finite-field encoding, whereas int gives the time for our
integer encoding; we use t to represent a 120-second timeout. For column sp, we used
cvc5 solver with configuration --ff=split, while for column gb, we used --ff=gb.
12      P. Antonino and N. Jain

--ff=split and the default --ff=gb. These two configurations deploy two differ-
ent solvers to check for the satisfiability of a finite-field theory formula. Simply
put, the technique used by the former (described in [30]) approximates the one
used by the latter (described in [29]); these approximations can be very effective
in tackling certain combinations of bitsum constraints. The results demonstrate
that there is no clear winner between our three NAVe backends: encoding with
integer theory, and finite-field theory with both cvc5 configurations. For exam-
ple, there are test programs for which the integer encoding is the quickest, and
there are others for which it is the sole backend to timeout. The two finite-field
solvers behave very similarly; this is expected, given that the --ff=split solver
is meant to improve on bitsum constraints, and these programs have no range
checks, i.e. the opcode leading to these types of constraints.
   In Table 2, we present the results for two sets of programs with range check
constraints. Again, one set has programs with verified verification conditions,
and the other one has falsified conditions, and we test both encoding and solver
configurations for the finite-field encoding. Again, the results demonstrate that
there is no clear winner between our three NAVe backends. However, we do see
a pattern: range checks for larger ranges — i.e. for representations with larger


                  Verified
       Benchmark                 Time(s)
                                                               Falsified
 id     #w #o #r rmax sp gb int
                                                       Benchmark              Time(s)
 prv1    12 21 11 32 17.2 16.1 18.9
                                                 id    #w #o #r rmax sp gb int
 prv2    147 154 52 32 17.6 15.5 17.7
                                                 prf1   24 31 15 1 18.3 18.0 16.3
 prv3    15 13 11 8 16.9 15.6 19.6
                                                 prf2   3    4 3 32 18.8 19.3 16.8
 prv4     1    3 2       1 16.5 14.5 18.2
                                                 prf3   4    4 2 32 17.2 18.5 t
 prv5     5    6 3 32 16.4 14.6 18.6
                                                 prf4   7    6 1        1 17.5 17.8 17.4
 prv6    20 28 13 8 20.1 14.7 18.9
                                                 prf5   3    3 3        1 17.7 16.7 17.0
 prv7    10 14 5 32 17.8 14.8 18.7
                                                 prf6   5    7 1        1 18.0 17.6 16.0
 prv8    50 61 15 128 16.6 14.5 19.0
                                                 prf7   2    3 1        8 18.0 86.2 16.3
 prv9    10 13 1 32 18.1 14.9 t
                                                 prf8   3    4 1        1 16.5 17.9 16.9
 prv10 969 984 292 8 17.6 15.9 19.9
                                                 prf9   32 28 6 32 22.6 19.4 17.0
 prv11 74 86 26 238 19.2 15.7 18.8
                                                 prf10  9 16 7 32 57.9 t              t
 prv12 21 37 9 32 18.0 t                 t
                                                 prf11  6 13 7 32 28.6 t              t
 prv13    8    6 1       1 16.4 18.5 t
 prv14 20 31 13 1 17.5 18.9 15.4
Table 2. Results for Noir programs without range constraints with verification con-
ditions verified and falsified, respectively. The column id identifies the program being
tested, column #w gives the program’s number of witnesses, column #o the number
of ACIR opcodes excluding BrilligCalls, #r the number of BlackBoxFuncCall range-
check opcodes, and rmax the number of bits for the largest range checked. Columns sp
and gb give the program analysis time for our ACIR finite-field encoding, whereas int
gives the time for our integer encoding; we use t to represent a 120-second timeout.
For column sp, we used cvc5 solver with configuration --ff=split, while for column
gb, we used --ff=gb.
              Formally Verifying Noir Zero Knowledge Programs with NAVe          13


fn main(x: Field) {                           fn main(x: u1, y: u1, z: u1)
    let y = unsafe {                              -> pub u1 {
        empty(x + 1) };                           let p = y - z;
    let z = y + x + 1;                            if p != 0 {
    let z1 = z + y;                                   let a = x / z;
    assert(z + z1 != 3);                              let b = a - z;
    let w = y + 2 * x + 3;                            if b != 0 {
    assert(w + z1 != z);                                  let _ = a / b;
    unsafe {                                          }
    verify_assert(                                }
        ((y != 1/3) | (x != 0))                   let u = x - z;
        & ((y != 0) | (x != 1/2))                 let v = y - u;
        & ((y != -1) | (x != -1/2))               unsafe {
        & ((y != -1/2) | (x != -1))               verify_assert(
    );}                                               ((u != 0) | (x == z))
}                                                     & ((v != 0) | (u == y))
                                                      & ((p != 0) | (y == x))
unconstrained fn empty(_: Field)                  );}
    -> Field { 0 }                                v
                                              }


Fig. 4. Regression test programs without (excerpt of prv13 with range check removed)
and with (prv14 ) range-check opcode, respectively.



number of bits — take longer, timing out or taking significantly longer than
other test programs. Also, we can see a difference in the behaviour of the finite-
field solvers: the --ff=split solver significantly outperforms the --ff=gb solver
in some instances (see prv12 , prf7 , prf10 , and prf11 ).
    We illustrate two of the test programs used in our evaluation in Figure 4. They
are both regression tests for the Noir language. The left-hand-side program is an
excerpt of the prv13 — we removed some code for the sake of conciseness. The
verify_assert statement that we added to this program captures restrictions on
the valid values of x and y based on the two asserts in the code; a & b captures
a conjunction between a and b. The first two conjuncts in the verify_assert are
enforced by the first assert, and the following two are enforced by the second
assert. The right-hand-side program (prv14 ) relies on range constraints imposed
by the 1-bit unsigned integer u1 type. The verify_assert statement we added
to this program captures some restrictions that are enforced by the assignments
to variables u, v, and p.
    Our results suggest that we could use our encodings and the different solvers
for finite-field encodings in a complementary way. We could use the three back-
ends concurrently for the same program, reporting the results of whichever one
finishes first. Furthermore, the results suggest that programs with large range
checks can take a significant amount of time to be verified. This demonstrates
that abstractions (i.e. approximations) need to be investigated to address this
14     P. Antonino and N. Jain

issue. These results chart a path for future work where we will investigate this
concurrent combination of solvers and abstractions to tackle complex constraints.


4    Related Work

In this section, we discuss the literature related to our verification framework.
    ZK programming languages and compilers. CirC [28] provides an infrastruc-
ture for compiling programs into circuits. The program is first converted to an
intermediate representation called CirC-IR. This IR is an abstract existentially
quantified circuit (EQC) based on the SMT-LIB standard and supports booleans,
numbers, bit vectors, and arrays. Thus, CirC is somewhat similar to LLVM but
is targeted at ZKP DSLs. The infrastructure can support compilation of cryp-
tographic languages to CirC-IR; however, integrating a new language requires
implementing a corresponding parser and interpreter. CirC has been evaluated
on Circom [3]: this is arguably the most popular (low-level) arithmetic circuit
DSL. The main difference between NAVe and CirC is that NAVe operates on
ACIR, which already resembles CirC-IR, eliminating the need for conversion.
Also, ACIR support some complex higher-level constructs, like black box func-
tions and memory manipulations, underpinning Noir, which Circ-IR does not.
    Like Noir, Cairo [2] is another popular high-level ZK programming language.
So far, there has been very little work on the formal verification of Cairo pro-
grams. The only paper in this area that we found [14] formalises and proves the
soundness of a transformation of Cairo programs into an algebraic representation
used by a ZK proof system. Our verifier and formalisation seem to be the first
to deal with a high-level ZK programming language and its particularities. For
instance, in Noir, we have complex constructs in the form of black box functions
and a notion of memory manipulation.
    Static analysis and bug detection. The majority of the existing work here has
focused on Circom and other circuit DSLs. Some claim that their approaches
can generalise beyond Circom, but their evaluations are limited to Circom cir-
cuits. Noir also compiles its Rust-style DSL to ACIR, making it prover-agnostic.
ZEQUAL [33] is a framework for verifying ZK circuits using static analysis and
deductive verification. It is built on top of the Circom compiler and performs
SMT queries via Z3 using a modular integer arithmetic encoding of finite-field
constraints. It can analyse circuit templates that do not require full instantia-
tion. However, the key difference from NAVe is that ZEQUAL also operates at the
DSL level and is evaluated only on Circom circuits. ZKAP [34] is also a static
analysis framework to detect vulnerabilities in ZK circuits. ZKAP’s approach is
guided by a manual study of existing bugs in Circom programs. It uses a cir-
cuit dependence graph to capture key circuit properties and expresses semantic
vulnerability patterns as Datalog-like queries. They have implemented nine dif-
ferent detectors, each identifying a specific anti-pattern. QED2 [31] also uses
SMT solvers for automated verification, focusing on particular circuit properties
(underconstrained bug to be precise) rather than full functional correctness. Al-
              Formally Verifying Noir Zero Knowledge Programs with NAVe           15

though QED2 can, in principle, analyse polynomial equations over finite fields,
it has been evaluated only on Circom circuits.
    Verification of Noir programs. Lampe [6] is a project that aims to support
the formal verification of both the semantics of the Noir language and the prop-
erties of programs written in Noir. It models Noir’s semantics in the Lean [27]
programming language and theorem prover, focusing more on capturing the se-
mantics of Noir rather than on providing a verification framework. Given its
use of a theorem prover, Lampe users have to iteratively drive the proving of
properties, whereas NAVe uses SMT solving to automatically check them.


5   Conclusion

Motivated by the recent increase in popularity of ZK programs and the emer-
gence of high-level ZK programming languages, we propose NAVe: a framework
for the formal verification of Noir programs. We propose a formalisation for Noir
via ACIR, an intermediate representation for Noir programs. We propose two
SMT-LIB-based formalisations of ACIR programs: one using a non-standard
finite-field theory, and another using the standard theory of integers. Our for-
malisation tackles some peculiarities of the Noir/ACIR language that are not
present in other languages. For instance, ACIR has several black box functions
with complex behaviour. We started tackling the range-check black box function,
but we intend to expand our encoding to other ones. The memory operations
of ACIR are another feature that is not present in other traditional languages.
Moreover, we have to address particularities of the ZK paradigm, such as the
distinction between constrained and unconstrained code.
    We use our formalisation to create the NAVe formal verifier. It is implemented
as the formal-verify command within a fork of Nargo, Noir’s popular package
manager. We hope that this integration motivates Noir developers to use our
tool. We rely on the Noir compiler to generate the ACIR representation of a
program, which is later SMT-LIB encoded using our formalisation and checked
for satisfiability by cvc5. The main goal of our tool is to identify underconstrained
programs, a common affliction of ZK programs. These are programs that have
some constraints missing, possibly due to the unrestricted use of unconstrained
code. NAVe users can specify verification conditions using the verify_assert(·)
function. Our tool also reports counterexamples to developers for verification
conditions that are falsified, helping them debug their code in the process. We
have evaluated NAVe on some test programs that are part of the Noir language
infrastructure with promising results. They also demonstrate that, in some cases,
better abstractions are needed to tackle complex constraints, such as the bitsum
ones generated by range checks.
    As future work, we plan to extend our formal verifier to tackle a larger subset
of ACIR. We will particularly investigate how we can formalise other types of
black box functions; these are notoriously difficult to encode. Moreover, we plan
to investigate new abstractions to tackle complex ACIR constraints/programs.
16      P. Antonino and N. Jain

References

 1. Aztec network. https://aztec.network/blog/introducing-aztec-nr-aztecs-private-
    smart-contract-framework. Accessed: 2025-11-24.
 2. Cairo language. https://www.cairo-lang.org. Accessed: 2025-11-21.
 3. Circom language. https://docs.circom.io/. Accessed: 2025-11-21.
 4. cvc5 finite fields theory reference.              https://cvc5.github.io/docs/cvc5-
    1.3.1/theories/finite_field.html. Accessed: 2025-11-21.
 5. Grumpkin           curve.                     https://aztecprotocol.github.io/aztec-
    connect/primitives.html#2-grumpkin—a-curve-on-top-of-bn-254-for-snark-
    efficient-group-operations. Accessed: 2025-11-28.
 6. Lampe repository. https://github.com/reilabs/lampe. Accessed: 2025-11-21.
 7. Lean consensus ethereum. https://leanroadmap.org/. Accessed: 2025-11-24.
 8. Noir language. https://noir-lang.org. Accessed: 2025-11-21.
 9. Oxparc zk bug tracker. https://noir-lang.org. Accessed: 2025-11-21.
10. Polygon technology. https://polygon.technology/. Accessed: 2025-11-24.
11. Rust language. https://rust-lang.org/. Accessed: 2025-11-28.
12. Starknet. https://www.starknet.io/. Accessed: 2025-11-24.
13. Tornado cash explainer. https://tornado-cash.medium.com/tornado-cash-got-
    hacked-by-us-b1e012a3c9a8. Accessed: 2025-11-28.
14. Jeremy Avigad, Lior Goldberg, David Levit, Yoav Seginer, and Alon Titelman. A
    verified algebraic representation of cairo program execution. In Proceedings of the
    11th ACM SIGPLAN International Conference on Certified Programs and Proofs,
    CPP 2022, page 153–165, New York, NY, USA, 2022. Association for Computing
    Machinery.
15. Haniel Barbosa, Clark W. Barrett, Martin Brain, Gereon Kremer, Hanna Lach-
    nitt, Makai Mann, Abdalrhman Mohamed, Mudathir Mohamed, Aina Niemetz,
    Andres Nötzli, Alex Ozdemir, Mathias Preiner, Andrew Reynolds, Ying Sheng,
    Cesare Tinelli, and Yoni Zohar. cvc5: A versatile and industrial-strength SMT
    solver. In Dana Fisman and Grigore Rosu, editors, Tools and Algorithms for the
    Construction and Analysis of Systems - 28th International Conference, TACAS
    2022, Held as Part of the European Joint Conferences on Theory and Practice
    of Software, ETAPS 2022, Munich, Germany, April 2-7, 2022, Proceedings, Part
    I, volume 13243 of Lecture Notes in Computer Science, pages 415–442. Springer,
    2022.
16. Clark Barrett, Pascal Fontaine, and Cesare Tinelli. The Satisfiability Modulo
    Theories Library (SMT-LIB). www.SMT-LIB.org, 2016.
17. Manuel Blum, Paul Feldman, and Silvio Micali. Non-interactive zero-knowledge
    and its applications. In Proceedings of the Twentieth Annual ACM Symposium
    on Theory of Computing, STOC ’88, page 103–112, New York, NY, USA, 1988.
    Association for Computing Machinery.
18. Stefanos Chaliasos, Jens Ernstberger, David Theodore, David Wong, Mohammad
    Jahanara, and Benjamin Livshits. Sok: What don’t we know? understanding secu-
    rity vulnerabilities in snarks. In Davide Balzarotti and Wenyuan Xu, editors, 33rd
    USENIX Security Symposium, USENIX Security 2024, Philadelphia, PA, USA,
    August 14-16, 2024. USENIX Association, 2024.
19. Rosario Gennaro, Craig Gentry, Bryan Parno, and Mariana Raykova. Quadratic
    span programs and succinct nizks without pcps. IACR Cryptol. ePrint Arch., page
    215, 2012.
                Formally Verifying Noir Zero Knowledge Programs with NAVe                   17

20. Oded Goldreich, Silvio Micali, and Avi Wigderson. Proofs that yield nothing but
    their validity or all languages in NP have zero-knowledge proof systems. In Pro-
    ceedings of the 27th Annual ACM Symposium on Theory of Computing (STOC),
    pages 174–187. ACM, 1991.
21. Shafi Goldwasser, Silvio Micali, and Charles Rackoff. The knowledge complexity
    of interactive proof-systems (extended abstract). In Robert Sedgewick, editor,
    Proceedings of the 17th Annual ACM Symposium on Theory of Computing, May
    6-8, 1985, Providence, Rhode Island, USA, pages 291–304. ACM, 1985.
22. Shafi Goldwasser, Silvio Micali, and Charles Rackoff. The knowledge complexity
    of interactive proof systems. SIAM Journal on Computing, 18(1):186–208, 1989.
23. Jens Groth. Short pairing-based non-interactive zero-knowledge arguments. In
    Masayuki Abe, editor, Advances in Cryptology - ASIACRYPT 2010 - 16th Inter-
    national Conference on the Theory and Application of Cryptology and Information
    Security, Singapore, December 5-9, 2010. Proceedings, volume 6477 of Lecture Notes
    in Computer Science, pages 321–340. Springer, 2010.
24. Jens Groth. On the size of pairing-based non-interactive arguments. page 305–326,
    Berlin, Heidelberg, 2016. Springer-Verlag.
25. Donald E. Knuth. The Art of Computer Programming, Volume 2: Seminumerical
    Algorithms. Addison-Wesley, Reading, MA, 3 edition, 1997.
26. Mary Maller, Sean Bowe, Markulf Kohlweiss, and Sarah Meiklejohn. Sonic: Zero-
    knowledge snarks from linear-size universal and updatable structured reference
    strings. CCS ’19, page 2111–2128, New York, NY, USA, 2019. Association for
    Computing Machinery.
27. Leonardo de Moura and Sebastian Ullrich. The lean 4 theorem prover and pro-
    gramming language. In Automated Deduction – CADE 28: 28th International
    Conference on Automated Deduction, Virtual Event, July 12–15, 2021, Proceed-
    ings, page 625–635, Berlin, Heidelberg, 2021. Springer-Verlag.
28. Alex Ozdemir, Fraser Brown, and Riad S. Wahby. Circ: Compiler infrastructure
    for proof systems, software verification, and more. In 43rd IEEE Symposium on
    Security and Privacy, SP 2022, San Francisco, CA, USA, May 22-26, 2022, pages
    2248–2266. IEEE, 2022.
29. Alex Ozdemir, Gereon Kremer, Cesare Tinelli, and Clark W. Barrett. Satisfiability
    modulo finite fields. In Constantin Enea and Akash Lal, editors, Computer Aided
    Verification - 35th International Conference, CAV 2023, Paris, France, July 17-22,
    2023, Proceedings, Part II, volume 13965 of Lecture Notes in Computer Science,
    pages 163–186. Springer, 2023.
30. Alex Ozdemir, Shankara Pailoor, Alp Bassa, Kostas Ferles, Clark W. Barrett, and
    Isil Dillig. Split gröbner bases for satisfiability modulo finite fields. In Arie Gurfinkel
    and Vijay Ganesh, editors, Computer Aided Verification - 36th International Con-
    ference, CAV 2024, Montreal, QC, Canada, July 24-27, 2024, Proceedings, Part I,
    volume 14681 of Lecture Notes in Computer Science, pages 3–25. Springer, 2024.
31. Shankara Pailoor, Yanju Chen, Franklyn Wang, Clara Rodríguez-Núñez, Jacob Van
    Geffen, Jason Morton, Michael Chu, Brian Gu, Yu Feng, and Isil Dillig. Automated
    detection of under-constrained circuits in zero-knowledge proofs. Proc. ACM Pro-
    gram. Lang., 7(PLDI):1510–1532, 2023.
32. Bryan Parno, Jon Howell, Craig Gentry, and Mariana Raykova. Pinocchio: nearly
    practical verifiable computation. Commun. ACM, 59(2):103–112, January 2016.
33. Jon Stephens, Shankara Pailoor, and Isil Dillig. Automated verification of consis-
    tency in zero-knowledge proof circuits. In Ruzica Piskac and Zvonimir Rakamaric,
    editors, Computer Aided Verification - 37th International Conference, CAV 2025,
18      P. Antonino and N. Jain

    Zagreb, Croatia, July 23-25, 2025, Proceedings, Part I, volume 15931 of Lecture
    Notes in Computer Science, pages 315–338. Springer, 2025.
34. Hongbo Wen, Jon Stephens, Yanju Chen, Kostas Ferles, Shankara Pailoor, Kyle
    Charbonnet, Isil Dillig, and Yu Feng. Practical security analysis of zero-knowledge
    proof circuits. In Davide Balzarotti and Wenyuan Xu, editors, 33rd USENIX
    Security Symposium, USENIX Security 2024, Philadelphia, PA, USA, August 14-
    16, 2024. USENIX Association, 2024.
