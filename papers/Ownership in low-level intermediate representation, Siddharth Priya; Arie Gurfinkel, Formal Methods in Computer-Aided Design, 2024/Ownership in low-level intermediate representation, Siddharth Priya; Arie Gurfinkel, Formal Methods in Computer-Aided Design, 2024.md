                                          Ownership in low-level intermediate representation
                                                                        Siddharth Priya∗                                       Arie Gurfinkel∗
                                                                 siddharth.priya@uwaterloo.ca                             arie.gurfinkel@uwaterloo.ca




                                            Abstract—The concept of ownership in high level languages can      reference exists. This has been useful for program verification.
                                         aid both the programmer and the compiler to reason about the          For example, the Move Prover [5] replaces references by ob-
                                         validity of memory operations. Previously, ownership semantics        jects in the generated verification conditions (VC). Similarly,
                                         has been used successfully in high level automatic program veri-
                                         fication to model a reference to data by a first order logic (FOL)    RustHorn [3], [6] is able to generate pure First Order Logic VC
                                         representation of data instead of maintaining an address map.         for safe Rust programs without introducing a memory model.
arXiv:2408.04043v3 [cs.PL] 13 Aug 2024




                                         However, ownership semantics is not used in low-level program            The advances in verification using ownership semantics
                                         verification. We have identified two challenges. First, ownership     have not made their way to verification of low-level programs.
                                         information is lost when a program is compiled to a low-level         One of the problems is that low-level languages do not support
                                         intermediate representation (e.g., in LLVM IR). Second, pointers
                                         in low-level programs point to bytes using an address map (e.g.,      ownership out of the box. As an example, LLVM bitcode
                                         in unsafe Rust) and thus the verification condition (VC) cannot       is a register based intermediate representation (IR) used by
                                         always replace a pointer by its FOL abstraction. To remedy            C, C++, and, Rust compilers. It only has an attribute for
                                         the situation, we develop ownership semantics for an LLVM-            marking pointers as noalias [7] and no ownership operations.
                                         like low-level intermediate representation. Using these semantics,    The noalias attribute is useful for optimization. However, the
                                         the VC can opportunistically model some memory accesses by a
                                         direct access of a pointer cache that stores byte representation      semantics of noalias in unclear and has caused confusion [8].
                                         of data. This scheme reduces instances where an address map           Another challenge is that ownership in high-level language
                                         must be maintained, especially for mostly safe programs that          does not translate directly to low-level settings. For example,
                                         follow ownership semantics. For unsafe functionality, memory          in verification of safe Rust programs, it is correct to model
                                         accesses are modelled by operations on an address map and we          a reference by the FOL representation of the value it refers
                                         provide mechanisms to keep the address map and pointer cache
                                         in-sync. We implement these semantics in S EA BMC, a bit-precise      to. However, this model does not work for LLVM-like IR
                                         bounded model checker for LLVM. For evaluation, the source            (and unsafe Rust) because such languages (dialect) have
                                         programs are assumed to be written in C. Since C does not             pointers that treat values as a collection of bytes and rely on
                                         have ownership built-in, suitable macros are added that introduce     pointer arithmetic to access individual bytes. In verification,
                                         and preserve ownership during translation to LLVM-like IR for         the standard solution models memory using an address map
                                         verification. This approach is evaluated on mature open source C
                                         code. For both handcrafted benchmarks and practical programs,         from addresses to byte or word values. However, such address
                                         we observe a speedup of 1.3x–5x during SMT solving.                   maps are expensive to execute symbolically.
                                                                                                                  This work improves the state-of-the-art by the following
                                                                I. I NTRODUCTION                               contributions. First, we develop an ownership semantics for an
                                            Ownership is a scheme to control aliasing of references in         LLVM-like low level language that operates on single words
                                         high level languages. It has been studied in a long line of           in memory. This language replaces unrestricted aliasing with
                                         academic research [1], [2], [3], [4]. More recently, the concept      mutable borrow, read-only borrow, and copy operations that
                                         has gained attention due to Rust, a popular systems language          track outstanding aliases for a memory allocation. Second, we
                                         that offers low level control like C/C++ and uses ownership           define a caching mechanism for capturing data at a pointer
                                         semantics to record aliases and mutation of data. In Rust, (1) a      itself. This cache can by written and read by operations on
                                         value has exactly one owner, (2) a reference to a value (called a     the pointer. A pointer cache allows us to replace memory
                                         borrow) cannot outlive the owner, and (3) a value can have one        accesses in the generated VC by the cache whenever correct
                                         mutable reference xor many immutable references. A program            to do so. This can simplify the VC and improve the solving
                                         that follows this programming discipline allows the Rust              time. For mostly safe programs, many memory accesses may
                                         compiler to reason about memory safety statically. However,           be replaced by pointer cache accesses. These semantics are
                                         for reasons of expressivity and performance, programs may             discussed in Section II.
                                         need to break this discipline for certain operations. For this,          Third, we discuss our design for VCGen and especially
                                         Rust provides unsafe code blocks where the static checks are          modelling the borrow operation in Section III. Borrowing tem-
                                         temporarily turned off.                                               porarily transfers memory access rights from the lender pointer
                                            While, ownership can aid in generating correct and efficient       (a.k.a. lender) to the borrowing pointer (a.k.a. borrower). In
                                         code, it is also useful in program verification. Usually, the pres-   the given semantics, this means that the pointer cache is also
                                         ence of aliasing necessitates an address map to soundly model         copied from lender to borrower. However, the borrower is
                                         object accesses through different aliases. With ownership, this       assumed to return the borrow by the first instance of a memory
                                         map can be eliminated when it is known that only a single             access by a lender. This means that the updated cache at
the borrower must be copied back to the lender before this.               instruction. The ro_* instructions create read-only borrows of
This transfer ordinarily requires a memory model that allows              the lending pointer. The cpy_* instructions create unrestricted
shared accesses between the borrower and lender aliases. A                copies of the lending pointer. The mut_mkbor_mem2reg instruction
more efficient way uses prophecy variables [9] and was first              borrows (loads) a pointer stored in memory to a register. The
proposed in [3]. We adapt the prophecy solution to our setting.           mov_reg2mem instruction moves (stores) a pointer in a register to
   Fourth, to make our ownership semantics practical, we add              memory. There is no move instruction between registers since
support for multi-word memory operations and evaluate the                 the operation is equivalent to α-renaming.
semantics by incorporating it in S EA BMC [10]. S EA BMC is               Semantics of M0 . The semantics are given in terms of a
a bit-precise bounded model checking engine for S EA H ORN                machine M0 and is based on the stacked borrows model
that uses an SMT solver as its backend. To ease writing                   for Rust [11]. In our formulation, each pointer type (ptype)
programs using these ownership semantics, the user writes                 is one of owned (o), mutably borrowed (mb), immutably
C programs laced with calls to ownership macros. During                   borrowed (rb), or, copied (c). Access to memory is controlled
compilation, the macros expand to LLVM intrinsics that are                by maintaining a per-location borrow stack that captures both
then interpreted using the given semantics to generate VC. The            valid accessors and access order. The configuration of M0
benchmark programs are a mix of handcrafted examples and                  is given by the program counter state (P ), register map
practical programs. The handcrafted examples are used to fine             (R : id → value), address map (M : addr → value) and
tune performance and show what is possible. The practical                 a borrow store state (SB : addr → stack((tag, ptype))). A
programs are from the mbedTLS project - an open-source                    value is either a bit-vector bv(N ) or a pointer type. An address
SSL/TLS library and has routines for encryption and secure                (addr) is represented as a bit-vector. A pointer is a tuple of
communications. We get a speedup of 1.3x–5x during SMT                    (addr, tag) and is considered fat on account of additional
solving. The evidence shows that the verification simplicity              metadata carried along with the address1 . A tag : bv(N ) is a
(speedup) correlates positively with the number of memory                 unique id given to a pointer when it is defined. Operations that
accesses that can be replaced by pointer cache accesses in a              introduce and remove aliases, then push and pop alias tags on
program.                                                                  the borrow stack, respectively. Each borrow stack entry also
                                                                          stores ptype along with an identifier for finer access control.
                   II. OSEA-IR LANGUAGE                                   An important restriction is that memory access is allowed for
   In this section, we present the syntax and semantics of the            an alias if its tag is top-of-(borrow)stack for that address.
OSEA-IR language. To simplify the presentation, we propose                   The semantics for relevant pointer introduction, aliasing,
machines that work with a single datatype bv(N ), a bit-vector            and, removal are given through operations on the borrow
of N bits, as the word size. We impose two restrictions. First,           stack (B) in Table I. A borrow stack state is represented
all memory operations - allocation, load, and, store work on              as a list B = e :: B1 , where e is the top of stack and
a single word. Second, the machine can only store integers                B1 represents the rest of the stack. We do not explicitly
in memory and does not support store and load of pointers.                show effect of operations on (P, R, M ) nor do we give the
We lift the first restriction in Section IV, and the second in            semantics for all instructions of M0 due to space constraints.
Appendix A.                                                               The interested reader is referred to the stacked borrows [11]
Syntax. We introduce ownership semantics on the base lan-                 and SEA-IR [10] papers for further background. The mk_own
guage SEA-IR [10]. SEA-IR is an intermediate representa-                  operation allocates and stores n at the given location. This
tion (IR) itself based on LLVM IR. LLVM assumes a register                operation must provide a location that is un-allocated. After
based machine and dependency between memory operations                    the operation, the new pointer tag is pushed onto the stack
are implied. SEA-IR explicates this dependency information                with ptype = o. The mutable borrow operations use mut_mkbor,
between memory operations by introducing memory registers.                mut_mksuc instructions that always occur in a pair on a lender
We assume that the type of each register is known. Figure 1               pointer p0 to create a borrowed pointer q0 and a succeeding
shows the ownership extended syntax of SEA-IR called                      pointer p1 . For a successful operation, the borrow stack is
OSEA-IR. We use R to represent a scalar register, P for a                 popped until p0 is on top and its ptype is either an owning or
pointer register and M for a memory register. A legal OSEA-IR             a mutably borrowed pointer. This operation removes p0 .tag as
program is assumed to be in a Static Single Assignment (SSA)              an accessor and instead pushes p1 .tag, the succeeding pointer
form. OSEA-IR primarily replaces unrestricted alias creation              and q0 .tag, the borrowed pointer, to the borrow stack in that
by new operations that introduce and remove aliases in a                  order. The associated type of a pointer is also added to each
restricted manner. The mk_own instruction initializes memory              stack entry. Note that the type of q1 is always mb. However
at the given location (simlar to a Box::new(n) in Rust). The              the type of p1 depends on the type of p0 . The intent is for q0
mut_mkbor, mut_mksuc instructions occur in pairs. The first creates       to have access rights till it surrenders them to p1 .
a mutable borrow pointer from a lender pointer. The second                   The copy operation creates two copies c1 and c2 using
creates a succeeding pointer from the lender pointer that be-             cpy_mkcpy1 and cpy_mkcpy2 instructions. A copied pointer cor-
comes active after the mutable borrow ends. The mut_mkbor_off
is similar to a mut_mkbor and creates a pointer at an offset                 1 We use the shorthand .addr to refer to the first tuple element, similarly
within an allocation. It must be followed by a mut_mksuc                  for other elements.




                                                                      2
          ⟨S⟩   ::=    . . . | ⟨OS⟩
       ⟨RDEF⟩   ::=    ... |
                       ⟨P⟩, ⟨M⟩ = mk own ⟨R⟩, ⟨M⟩
                       ⟨P⟩ = mut mkbor ⟨P⟩ | ⟨P⟩ = mut mkbor off ⟨P⟩, ⟨R⟩ | ⟨P⟩ = mut mksuc ⟨P⟩ |
                       ⟨P⟩ = ro mkbor ⟨P⟩ | ⟨P⟩ = ro mkbor off ⟨P⟩, ⟨R⟩ | ⟨P⟩ = ro mksuc ⟨P⟩ |
                       ⟨P⟩ = cpy mkcpy1 ⟨P⟩ | ⟨P⟩ = cpy mkcpy1 off ⟨P⟩, ⟨R⟩ | ⟨P⟩ = cpy mkcpy2 ⟨P⟩ |

      ⟨MDEF⟩    ::=    . . . | ⟨P⟩, ⟨M⟩ = mut mkbor mem2reg ⟨P⟩, ⟨M⟩ | ⟨M⟩ = mov reg2mem ⟨P⟩, ⟨P⟩, ⟨M⟩
         ⟨OS⟩   ::=    die ⟨P⟩

Fig. 1: Ownership instr. in OSEA-IR grammar, where R, P, and M are scalar registers, pointer registers, and memory registers respectively.

       Operation                  Pre-condition                                        Post-condition
       p,m1 = mkown n, m0         SB [p.addr] = ∅                                      SB [p.addr] = (tagp , o) :: []
       q0 = mut_mkbor p0          SB [p0 .addr] = B0 :: (tagp0 , t) :: B1 ,
                                                                                       SB [p0 .addr] = (tagq0 , mb) :: (tagp1 , t) :: B1
       p1 = mut_mksuc p0          t ∈ {o, mb}, p0 .tag = tagp0
       c1 = cpy_mkcpy1 p0         SB [p0 .addr] = B0 :: (tagp0 , t) :: B1 ,
                                                                                       SB [p0 .addr] = (tagc1 , c) :: (tagc2 , t) :: B1
       c2 = cpy_mkcpy2 p0         p0 .tag = tagp0
                                  SB [q.addr] = (tagq , tq ) :: (tagp , tp ) :: B1 ,
       die q                                                                           SB [q.addr] = (tagp , tp ) :: B1
                                  q.tag = tagq , tq = mb, tp ∈ {o, mb}
                                                                                       SB [p.addr] = B2 :: (tagp , tp ) :: B1 ,
                                  SB [p.addr] = B0 :: (tagp , tp ) :: B1 ,
       m1 = store r, p, m0                                                             (p.tag = tagp , tp ∈ {o, mb}) =⇒ (B2 = ∅),
                                  tp ̸= rb, p.tag = tagp
                                                                                       (tp = c) =⇒ (B2 = B0 )
                                                                                       SB [p.addr] = B2 :: (tagp , tp ) :: B1 ,
                                  SB [p.addr] = B0 :: (tagp , tp ) :: B1 ,
       r = load p, m                                                                   (tp ∈ {o, mb, rb}) =⇒ (B2 = [(tagq , tq ) ∈ B0 | tq = c]),
                                  p.tag = tagp
                                                                                       (tp = c) =⇒ (B2 = B0 )

     TABLE I: Effect of selected operations on borrow stack (SB ) in machine M0 . Effects on R and M are not shown.
responds to a raw pointer in Rust. The lender pointer p0 for                                             1 fun main() {
                                                                                                         2 BB0:
a copy operation can be of any ptype. Similar to a mutable                                               3 m00 = mem.init()
borrow operation, all entries on top of p0 are popped from                                               4 ; R = []         M = []      SB = []
                                                                                                         5 p0,m0 = mk_own 42, m00
the borrow stack and p0 itself is removed. Next c1 :: c2 are                                             6 ; R[p0] = (0x4,1)         M[0x4] = 42      SB[0x4] = 1 :: []
pushed onto the borrow stack in that order. The ptype of c1                                              7 q0 = mut_mkbor p0
                                                                                                         8 p1 = mut_mksuc p0
is always c. However, the ptype of c2 depends on the lender                                                      R[p1] = (0x4,2)
                                                                                                         9 ;
pointer p0 . This ensures that the ptype of a lender pointer is                                                  R[q0] = (0x4,3)     M      SB[0x4] = 3 :: 2 :: []
                                                                                                        10 r1 = load q0, m0
not lost through successive copy operations. Finally, the die                                           11      R[r1] = 42     M     SB ;
operation surrenders access rights for a pointer by popping off                                         12 m1 = store r1 + 1,q0,m0
                                                                                                        13 ; R         M[0x4] = 43      SB
its entry from the borrow stack. It is only defined for a mutably                                       14 die q0
borrowed pointer q and signals transfer of data from such a                                             15 ; R         M     SB[0x4] = 2 :: []
                                                                                                        16 r = load p1, m1
pointer to its immediate lender, which must be of ptype = o                                             17 ; R[r] = 43         M     SB
or ptype = mb. The pointer q must be top of borrow stack.                                               18 halt
                                                                                                        19 }
The die operation is an extension of stacked borrows and is
useful for returning information from a mutable borrow to                          Fig. 2: Example of M0 operation. Effect on register map (R),
the succeeding pointer without going through shared memory.                        memory map (M ), and borrow store (SB ) shown in pink.
The store instruction writes a value to memory. If the lender
pointer p is mutably borrowed or owning then all elements                          a word of memory is allocated with (addr=0x4,tag=1) in the
before p are popped. If p is copied then borrow stack remains                      register map at key p0, the integer 42 is written to memory at
unchanged. The load instruction reads values from memory                           M[0x4], and the tag value 1 is pushed to the borrow stack at
into a register using a lender pointer p. If p is owning, mutably                  SB[0x4]. Next an alias is created using the mutable borrow
borrowed or read-only borrowed, then all pointers above p                          operation at lines 7–8 using tags 3 and 2 for borrowed q0
(except copied pointers) are removed from the borrow stack.                        and succeeding pointer p1 respectively. First the tag for p1
If p is copied, then the borrow stack is unchanged. Finally,                       is pushed, then the tag for q0 is pushed. The next couple of
the observable state ObsStateM0 of machine M0 is given by                          lines load 42 using q0, increment it, and write it back. The
the tuple (P, R, M, SB ).                                                          program ends the mutable borrow in line 14. This removes
                                                                                   q0’s tag from SB. Now only p1 can access addr 0x4. Finally,
   Let us look at an example of how M0 operates in Fig. 2.                         the program reads the new value 43 from addr 0x4 in line 19.
The intent of the program is to (1) create an owned pointer,                       Semantics of M1 . We now define an extension to M0 called
(2) make its alias (3) update data through the alias, and,                         M1 . In M1 , a fat pointer additionally has a cache bit-vector
(4) observe the data through the owned pointer. At line 5,                         field called val. Each store operation also updates val with the



                                                                               3
value to be written to memory. A load from memory may be                                  1 fun main() {
                                                                                          2 BB0:
replaced by val when correct to do so. A pointer value now                                3 m00 = mem.init()
becomes (addr, tag, val). Overall, the semantics of existing                              4 ;m00
instructions aim to maintain the val cache. The semantics is                              5 p0,m0 = mk_own 42, m00
                                                                                          6 ;p0 .addr = 4 ∧ p0 .val = 42 ∧
laid out in Table II. The mk_own instruction updates its cache
                                                                                          7    ;m0 = m00 [p0 .addr 7→ 42]
with the value it initialized the memory allocation with. The
                                                                                          8    q0 = mut_mkbor p0
pair of mut_mkbor and mut_mksuc operations have two cases: (1) if                         9    p1 = mut_mksuc p0
the lender is top-of-(borrow)stack then the operation reads the                          10    ;q0 .addr = p0 .addr ∧ q0 .val = p0 .val ∧ q0 .retval = x ∧
value stored at lender pointer p0 and updates the caches of q0                           11    ;p1 .addr = p0 .addr ∧ p1 .val = x ∧ p1 .retval = p0 .retval
and p1 with that value; (2) if the lender is not top of stack                            12    r1 = load q0, m0
then the value at lender may be stale and the correct value                              13    ;r1 = q0 .val
                                                                                         14    m1 = store r1 + 1, q0, m0
is read from memory. The pair of cpy_mkcpy1 and cpy_mkcpy2
                                                                                         15    ;q1 .addr = q0 .addr ∧ q1 .retval = q0 .retval ∧
instructions similarly update the cache of c1 and c2 with the
                                                                                         16    ;q1 .val = r1 + 1 ∧ m1 = m0 [q1 .addr 7→ q1 .val]
correct value. The die instruction transfers the value cached at                         17    die q0
q to the cache of the immediately succeeding pointer, called                             18    ;q1 .val = q1 .retval
p here. The transfer to the succeeding pointer occurs by first                           19    r = load p1, m1
searching for the pointer with the correct tag in the register                           20    ;r = p1 .val
map R and then updating the corresponding val field. Since we                            21    assert r == 43
                                                                                         22 ;¬(r = 43)
do not support the storage of pointers to memory, the search
                                                                                         23 halt
through R is enough to find the right pointer. Note that the die                         24 }
operation enables transfer of a value from a mutable borrow to
the succeeding pointer without using shared memory. A store                    Fig. 3: Verification condition (VC) shown in yellow.
instruction updates the cache with the value r to be written to             in-sync (by assumption) and mutably borrowed pointer
memory. This value is then written to memory and to p.val. In               cache gets this value;
M1 , a store does not support storing pointers to memory. This            • die, before this die Thm. 1 holds for the mutably bor-
restriction is lifted in Appendix A. A load has two cases. First,           rowed pointer. Then, die copies cache value from muta-
if the lender pointer p is top-of-(borrow)stack, and is mutably             bly borrowed pointer to succeeding pointer, keeping the
borrowed or owning, then the read from memory is replaced                   succeeding pointer cache in-sync with memory.        ■
by a read of the val (cache) field. Second, if the load uses a
lender pointer p that is not top-of-(borrow)stack, or is copied,           We now define ObsStateM 1 for M1 as a tuple
then the read from memory proceeds as usual. In the second              (P, R, M, S) with the pointer val field excluded from view.
case, the pointer cache is also updated with the value read             Let ≡ be the equivalence relation between M0 and M1
from memory.                                                            defined as follows: sm      m1
                                                                                             M 0 ≡ sM 1 ↔ ObsStateM 0 (sM 0 ) =
                                                                                               0


   The optimisation we describe for the load instruction is             ObsStateM 1 (sM 1 ). By Thm. 1, starting in equivalent observ-
correct because M1 always maintains the following invariant:            able states, both M0 and M1 operate in lock-step. Thus, the
                                                                        following theorem holds:
Theorem 1 (Cache equivalence). For all pointers in the reg-
ister map, if the pointer is top-of-(borrow)stack and is owning         Theorem 2. The relation ≡ is both a forward and a backward
or mutably borrowed then the pointer cache value is the same            simulation between M0 and M1 .
as the value of memory at address of the pointer. Formally,             Thus, safety of M1 implies safety of M0 and vise versa.
let R be a register map, M memory, and SB a borrow store.
Then,                                                                                         III. VC G ENERATION
  (R[p] = (addr, tagp , n)) ∧                                              We introduce the general encoding of an OSEA-IR pro-
               (SB [addr] = (tagp , tp ) :: B) ∧                        gram and the modelling of mutable borrows in particular
                                                                        using the example in Fig. 3. Note that this example runs
                       (tp ∈ {o, mb})) =⇒ M [addr] = n                  throughout this section. For now, we suggest the reader
Proof. The proof proceeds by structural induction on the                ignore the generated VC (in yellow). We focus on aliasing
syntax of the program P. Assume Thm. 1 holds in some                    instructions and how the pointer cache is affected. The mk_own
configuration (P0 , R0 , M0 , SB0 ). The next instruction takes         instruction defines p0 writing 42 to both memory and the
the configuration to (P1 , R1 , M1 , SB1 ). We case-split on each       pointer cache maintaining Cache Equivalence. The mut_mkbor,
possible instruction. We illustrate the process through some of         mut_mksuc instructions create aliases q0, p1 from p0. Here, the
the relevant instructions.                                              cache at p0 is copied to q0 and p1, again maintaining the cache
   • store keeps the cache in-sync with memory according to             equivalence invariant. The q0 mutably borrowed alias updates
     given semantics;                                                   memory (and its pointer cache) to 43. It then surrenders access
   • mut_mkbor keeps the mutably borrowed pointer cache in-             rights using the die instruction. At this point, the succeeding
     sync with memory since the lender cache value is already           alias p1 becomes active (top-of-(borrow)stack). However, for



                                                                    4
               Operation              Pre-condition                      Post-condition
               p = mkown n            –                                  R[p] = (p.addr, tagp , n), M [p.addr] = n
                                                                         R[q0 ] = (p0 .addr, tagq0 , v), R[p1 ] = (p0 .addr, tagp1 , v),
               q0 = mut_mkbor p0
                                      R[p0 ] = (p0 .addr, tagp0 , vp )   (B0 = ∅) =⇒ (v = vp ),
               p1 = mut_mksuc p0
                                                                         (B0 ̸= ∅) =⇒ (v = M [p0 .addr])
                                                                         R[c1 ] = (p0 .addr, tagc1 , v), R[c2 ] = (p0 .addr, tagc2 , v),
               c1 = cpy_mkcpy1 p0
                                      R[p0 ] = (p0 .addr, tagp0 , vp )   (B0 = ∅ ∧ t = {o, mb, rb}) =⇒ (v = vp ),
               c2 = cpy_mkcpy2 p0
                                                                         ¬(B0 = ∅ ∧ t = {o, mb, rb}) =⇒ (v = M [p0 .addr])
                                                                         R[p] = (q.addr, tagp , n),
               die q                  R[q] = (q.addr, tagq , n)
                                                                         ∃p.R[p] = (q.addr, tagp , )
               m1 = store r, p, m0    R[p] = (p.addr, tagp , )           M [p.addr] = v, R[p] = (p.addr, tagp , v)
                                                                         R[r] = v, R[p] = (p.addr, tagp , v),
               r = load p, m          R[p] = (p.addr, tagp , vp )        ((B0 = ∅, tp ∈ {o, mb}) =⇒ (v = vp ))
                                                                         ((B0 ̸= ∅ ∨ tp = c) =⇒ (v = M [p.addr]))

TABLE II: Effect of selected operations on SB ,R, and M in machine M1 in addition to pre-and-post conditions from Table I.
p1 to maintain cache equivalence (Theorem 1), it must get a
copy of q0’s cache. This is not straightforward since there is no              sym(p0, m1 = mk_own n, m0) ≜ ∃ℓ.(m1 = m0 [ℓ 7→ n]) ∧
                                                                                                                       (p0 .addr = ℓ) ∧ (p0 .val = n)
explicit transfer instruction from q0 to p1. The standard solution
is to use shared memory so that q0 can write to this memory
                                                                                            Fig. 4: Definition of sym for mk_own.
on a die and the succeeding pointer p1 can then read from
this memory on next access. However, the aim of caching is                   in its cache in p1 .val. Moving ahead, lines 13–16 model the
to eschew memory accesses as much as possible to keep the                    increment of the value pointed to by q0 . Note that apart from
operation (and VC) simple. The concrete semantics of M1                      updating the value in memory, the q0 .val variant q1 .val also
provides one alternative to accessing memory. There, a die                   gets the updated value. Finally, in line 18, the die operation
instruction finds the succeeding pointer tag in the borrow store             causes the prophecy x to be constrained by equating q1 .val and
SB and then searches through the register map R to update                    q1 .retval. As expected, this defines p1 .val to get the correct
the pointer cache with the same tag. This mechanism is as (or                cache value 43 maintaining cache equivalence. The transfer
more) expensive to execute symbolically as shared memory.                    of cache from q0 to p1 is, therefore, modelled without any
An elegant solution proposed in RustHorn [3] uses a prophecy                 expensive symbolic operations involving memory accesses or
variable [9] to model the return of a mutable borrow in the VC.              register map lookups. In the end, we see that the generated
We adapt the scheme to VC generation (VCGen) for OSEA-                       VC is unsatisfiable and the property is valid.
IR. We now explain VCGen, emphasizing the role of prophecy
                                                                                We now describe the function sym for selected pointer
variables to model return of a mutable borrow.
                                                                             operations. The semantics of mk_own is given in Fig. 4. We
   The VC is generated using the sym translation function.                   assume that an address ℓ is given by an external allocator. The
It builds up the VC in a recursive, bottom-up fashion on the                 allocator should follow the usual property that ℓ has not been
abstract syntax tree of an OSEA-IR program. For simplicity                   allocated previously. Note that p0 .retval field is free since
of presentation, we assume that two fundamental sorts are                    an owning pointer does not return the cache value to another
used in the encoding: bit-vector of 64 bits, bv (64), and a map              alias. We define sym for mutable borrow and die operations
between bit-vectors, bv (64) → bv (64). We now revisit the                   in Fig. 5. The mutable borrow aliasing operation copies the
example and explain the VC for each line of source code.                     addr field from the lender to the borrower and succeeding
Line 4 models mem.init as m00 , a free variable. Line 6 models               pointer. The cache is wired as follows. First, the mutably
the mk_own instruction. It updates memory at m00 [addr] to 42                borrowing pointer gets the lender cache using q0 .val = p0 .val.
and defines the fat pointer p0 . A fat pointer is modelled as                Second, we entangle p1 .val with the free symbol q0 .retval
a tuple (addr, val, retval). Here addr holds the address, val                using the tngle macro. The macro itself entangles the first
holds the current cache value (42 here), and retval holds a                  argument with the second by equating them. Third, p1 .retval
prophecy value, the use of which will be laid out soon. A                    gets the prophecy in p0 .retval to model cascading borrows
mutable borrow operation occurs in lines 10–11. The lender                   (reborrows). The sym for die equates the given pointer’s val
pointer p0 creates two aliases, the mutable borrow q0 and the                and retval field, constraining the prophecy value in q.retval
succeeding pointer p1 . The location p0 .addr is copied to both              and returning the borrow.
q0 .addr and p1 .addr. The cache at p0 .val is copied to q0 .val.               In summary, the fat pointer concept is our workhorse in
To set up the return of the cache value from the mutably                     mapping two previous high level VCGen schemes to a low-
borrowed alias to the succeeding pointer, we entangle the                    level verification setting. First, the reference elimination mech-
q0 .retval and p1 .val field using a fresh prophecy value x.                 anism is replaced by fat pointers that cache values. Second,
This prophecy x will resolve to the correct cache value when                 a fat pointer field holds a prophecy value that expresses the
q0 dies. When this happens, p1 instantly gets the same value                 cache value after returning from a mutable borrow.



                                                                         5
       tngle(r1 , r2 ) ≜ r1 = r2                                            1 extern void escapeToMemory(char *);
                                                                            2 int main() {
       sym(q_0 = mut_mkbor p_0; p_1 = mut_mksuc p_0) ≜                      3   char *p = MK OWN(0, sizeof(char));
            q0 .addr = p0 .addr ∧ q0 .val = p0 .val ∧                       4 char c = nd_char();
                tngle(p1 .val, q0 .retval) ∧ p1 .retval = p0 .retval        5 assume (c == 42);
                                                                            6   SET CACHE(p, c);
       sym(die q) ≜ q.val = q.retval
                                                                            7 *p = c;
                                                                            8 char *b;
Fig. 5: Definition of sym for mutable borrow, die, and tngle macro          9   MUT BORROW(b, p);
for entanglement.                                                          10 if (nd_bool()) {
                                                                           11     c = nd_char();
   ⟨RDEF⟩    ::=   . . . | ⟨P⟩, ⟨M⟩ = mk own ⟨R⟩, ⟨M⟩ |                    12     assume(c > 43);
                   ⟨P⟩ = begin unique ⟨P⟩ | ⟨P⟩ = end unique ⟨P⟩ |
                   ⟨P⟩ = set cache ⟨P⟩, ⟨R⟩ | ⟨R⟩ = get cache ⟨P⟩          13     SET CACHE(b, c);
                                                                           14     *b = c;
       Fig. 6: Grammar of new instructions for OSEA-IR.                    15     escapeToMemory(b);
                                                                           16 }
            IV. T OWARDS A PRACTICAL MACHINE                               17   DIE(b);
                                                                           18 char r;
   In Section II, we described M0 and M1 , both machines                   19   GET CACHE(p, r);
that could only allocate a single word through mk_own. We lift             20 sassert(r == 42 || r > 43);
                                                                           21 return 0;}
this restriction now in M2 . To allocate multiple words (wide
allocations), we change the mk_own syntax. Instead of taking               Fig. 7: An example C program with ownership intrinsics wrapped in
a bit-vector to write to memory, it now takes a bit-vector                 C Macros, highlighted in yellow.
allocation size argument. For cache equivalence to hold, the
pointer cache width must now be wide enough to cache multi-                API is in the form of C macros. The C program is compiled
byte allocation data. This complicates the design of the cache.            to an OSEA-IR program. The low-level OSEA-IR program
To keep things simple, instead of hard-wiring the pointer cache            then generates the VC in SMT-LIB form. This is finally sent
to replicate memory contents, we only cache a summary of the               to an SMT solver. We discuss the API using the example
data in memory and provide operations to set and get the cache             high level program in Fig. 7. The program starts in line 3,
value using set_cache and get_cache, respectively. A property              the MK_OWN macro allocates a byte of memory to an owning
to be verified can be cached at the pointer. Pointer aliasing              pointer. The next line uses the nd_char function to assign a
operations copy the value as before. The decoupling of cache               non-deterministic char to c. The value of c is constrained to
from load and store operations does introduce burden on the                be 42 using an assume statement. In line 6, the cache at pointer
programmer to update the cache as required. As we move                     p is set to the value of c using the SET_CACHE macro. The value
towards a practical machine, we also add a new unique (u)                  is also stored in memory using pointer p. The macro MUT_BORROW
variant to pointer type ptype. A unique pointer is created using           in line 9 then creates a mutable borrow. Internally, the macro
begin_unique and end_unique instructions.                                  expands to mut_mkbor and mut_mksuc with b getting the mutable
   The syntax of these new instructions is given in Fig. 6.                borrow and p getting the succeeding pointer. Next, the non-
The mk_own instruction takes three arguments - the bit-vector              deterministic boolean value from nd_bool is used in line 10
to write, the size (in bytes) of the allocation and the incom-             to conditionally update b’s cache to a non-deterministic value
ing memory to update. The operation now does not update                    greater than 43. The escapeToMemory function takes the address
memory or the pointer cache since that is the programmer’s                 of b thwarting any optimisation attempts to promote b to a
responsibility. The begin_unique and end_unique operations take            register. Finally, b dies in line 17 using the macro DIE. The
a copied (unique) pointer and define a unique (copied) pointer             succeeding pointer’s cache is now read using GET_CACHE into r
with the same addr and val fields as the source pointer. These             in line 19. The sassert (static assert) then checks that the value
operations are useful in practical situations where the user only          of r is either 42 or greater than 43.
wants to mark a pointer as unique temporarily. The get_cache                  For the program in Fig. 7, Fig. 8a is its OSEA-IR form
instruction returns the val field of a pointer. the set_cache              and Fig. 8b is the generated VC. We now describe the VCGen
instruction takes a pointer and a value. It then defines a new             in M2 using Fig. 8. The high-level ownership instructions
pointer where all fields are the same as the source pointer,               are highlighted in yellow in both figures. The MK_OWN macro
except the val field that has been updated to the given value.             in C becomes the mk_own instruction in OSEA-IR and is
Verification pipeline. To evaluate the efficacy of ownership               translated to SMT-LIB form using sym. Note that in M2 ,
intrinsics for verification, we use the S EA BMC bit-precise               mk_own does not write to memory or update the pointer cache.
bounded model checker. S EA BMC operates on LLVM IR                        The symbolic semantics therefore only allocates memory and
programs. For this work, the S EA BMC VCGen process has                    provides a previously unallocated address addr0 . The set_cache
been enhanced to handle ownership instructions. It is cumber-              instruction in line 7 defines a pointer p3 with the same addr as
some to construct low-level OSEA-IR programs by hand to                    p2 and the cache updated to r5 . The mutable borrow occurs
be verified in S EA BMC. To ease the task, we provide an API               in lines 9–10. The semantics copies the lender p3 .addr to
for adding ownership semantics to C programs resulting in a                p5 .addr and p6 .addr. The val and retval fields are set up as
C-like programming language with ownership semantics. The                  usual. The cache of the borrowed pointer p5 is conditionally



                                                                       6
1 fun main() {
2 BB0:
3 m3 = mem.init()
4   p2, m0 = mk own 1, m3         p2 .addr = addr 0 ∧ m0 = m3 ∧                                         100
                                   r6 = (r5 = 0) ∧
5 r5 = nd_char()
6 r6 = r5 == 42                   p3 .addr = p2 .addr ∧ p3 .val = r5 ∧
7   p3 = set cache p2 r5          p5 .addr = p3 .addr ∧ p6 .addr = p3 .addr ∧                           80
8 m1 = store r5, p3, m0           tngle(p5 .retval, p6 .val) ∧ p5 .val = p3 .val ∧
9   p5 = mut mkbor p3              r17 = (r15 = 0) ∧
                                                                                                        60




                                                                                          Baseline(s)
                                   r19 = r18 > 1 ∧
10   p6 = mut mksuc p3
                                   r20 = r6 ∧ r19 ∧
11 r15 = nd_bool();               p23 .addr = p5 .addr ∧ p23 .val = r18 ∧
12 r17 = r15 == 42
13 br r17, ERR, BB1                r22 = ite(r17 , r6 , r20 ) ∧                                         40                              flight_append_shad
14                                 p24 = ite(r17 , p5 , p23 ) ∧                                                                         write_records_shad
15 BB1:                           p24 .retval = p24 .val ∧ r22 ∧                                                                        write_handshake_shad
                                                                                                                                        write_handshake_main
16 r18 = nd_char()                r29 = p6 .val ∧                                                       20                              many_buffers_main
17 r19 = r18 > 43                  r30 = r29 = 0 ∧
18 r20 = r6 && r19                 r31 = r29 > 1 ∧
                                                                                                                                        y=x
19   p23 = set cache p5 r18        r32 = (r30 ∨ r31 ) ∧
                                                                                                                                        y = 3x
                                                                                                         0
20 m2 = store r18, p23, m1         a = ¬r32 ∧                                                                 0   20   40          60        80          100
21 escapeToMemory(p0)              a∧                                                                                       Ownsem(s)
22 br ERR                          ¬false
23
24 ERR:                                       (b) SMT-LIB program.                       Fig. 10: Solve time (in sec.) using ownership semantics vs baseline.
25 r22 = select r17, r6, r20
26 p24 = select r17, p5, p23
                                                                                         in Fig. 9. Here, we want to check that a write function in
27   die p24                                                                             Fig. 9b writes only to an open file and the file is always
28   r29 = get cache p6                                                                  closed after a write. The state of the file object is encoded as
29 r30 = r29 == 42                                                                       a typestate property [12] that records (and checks) operations
30 r31 = r29 > 43
31 r32 = r30 || r31                                                                      that have occurred on an object. The write function is called
32 A = not r32                                                                           using the unit proof harness in Fig. 9a. It defines n file pointers
33 assume A
34 assert false                                                                          based on user input. The typestate is marked open for each
35 halt                                                                                  file pointer in shadow memory using the set_shad function.
36 }
                                                                                         Shadow memory is an address map (addr to bv (64)). It is
             (a) OSEA-IR program.                                                        used to stash verification relevant object metadata. In practice,
 Fig. 8: Program from Fig. 7 in OSEA-IR and SMT-LIB forms.                               shadow memory is provided by verification and testing tools
 Ownership intrinsics and their counterpart expressions in SMT are                       like S EA BMC and Memcheck [13]. If shadow memory is not
 highlighted in yellow.                                                                  available then metadata can be stashed in a separate main
  1 enum status {O, C};                                                                  (program) memory allocation, which is available when the
  2 int unit_proof(const char **fnames,
  3     int n) {
                                                                                         program is built in debug or verification mode. In the example,
  4 FILE *f[MAX];// assume n < MAX                                                       after the typestate is set to open for each file pointer, we choose
  5 for(int i=0; i < n; i++) {
  6     set_shad(f[i], O);
                                                                                         one file pointer file out of n for calling write — the system
  7     f[i] = open(fnames[i], "w");}   1 void write(FILE *fp) {                         under test (SUT). In the SUT, we first check that the typestate
  8 size_t choose = nd_size_t();        2 // check file opened
  9 assume(choose < n);                 3 sassert(get_shad(fp) == O);
                                                                                         of the file object is open using get_shad to get the typestate
 10 FILE *file = f[choose];             4 fputc(’a’, fp);                                value. Then the char ’a’ is written and the file is closed, with
 11 write(file);                        5 // mark closed
 12 // check file closed                6 set_shad(fp, C);
                                                                                         the typestate marked as closed. Finally, the harness checks that
 13 sassert(get_shad(file) == C);}      7 fclose(fp);}                                   the file typestate is indeed closed.
              (a) A unit proof.                       (b) An SUT.                           Note in the given unit proof, the write and read of shadow
                                                                                         memory can resolve to one of n allocations since any file object
     Fig. 9: An example of typestate storage in shadow memory.
                                                                                         can be chosen. Therefore, in the VC, memory access would
 updated in line 19. The borrowed (variant) pointer p24 dies in                          involve solving an ITE (if-then-else) expression for 1 of n
 line 27 with the usual semantics. The cache of the succeeding                           choices. Here, solving the ITE is redundant since we only
 pointer p6 is read into r29 in line 28. The lines 29 to 32                              want to check that a given operation occurred on the chosen
 set up the program such that if an execution satisfies assume                           file pointer. A better solution would be to store typestate in
 A then it reaches the error state (assert false). An important                          the file (fat) pointer cache itself. With this optimisation, an
 consequence of using ownership semantics is that the SMT-                               ITE would not be traversed since read, writes of the typestate
 LIB program does not need to model the store instruction in                             would be at the pointer (using get_cache and set_cache) leading
 line 20.                                                                                to simpler VC.
                                                                                            We base our experiments on this idea utilizing the S EA BMC
                            V. E VALUATION
                                                                                         model checking engine for S EA H ORN. S EA BMC originally
   We would like to cache verification properties for practical                          takes a SEA-IR program as input and generates VC that are
 programs. We first describe properties of interest and our                              solved by an SMT solver. We enhance S EA BMC to now take
 baseline property carrying mechanisms through the example                               OSEA-IR programs as input. Using the C macro API, C unit



                                                                                     7
proofs are compiled to SMT. We then measure how typestate                 https://github.com/priyasiddharth/mbedtls-ownsem.
cached at pointers compares to typestate stored in memory.                   Overall, a speedup in solving time occurs as expected.
   The C unit proofs we work with come from mbedTLS [14],                 The speedup is due to simpler VC. However, the speedup is
a C library of cryptographic primitives, SSL/TLS and DTLS                 sensitive to the property expressed as a typestate check and
protocols. In particular, we look at three functions in ssl_msg.c         number of operations on object (pointer) that affect typestate.
that handles SSL message construction and de-construction.
The flow we consider are (1) flight_append that appends                                        VI. R ELATED WORK
messages to the current flight of messages, (2) write_records                RustBelt [16], Oxide [17] formalize subsets of high level
that encrypts messages into records and sends them on the                 Rust. RustBelt uses a continuation passing style functional
wire, and, (3) write_handshake that writes handshake messages.            language to describe the semantics. Oxide uses a high level
Each SUT operates on a byte buffer data structure. We are                 language similar to Rust. These approaches do not map
interested in recording and checking typestate properties for             directly to a low–level register machine like LLVM. Stacked
such a buffer. However, similar to example Fig. 9, the unit               Borrows [11] formulates Rust ownership semantics as a stack
proof is set up such that a single byte buffer pointer may                discipline working on de–sugared (MIR) Rust syntax that
point to 1-of-n buffer objects. Therefore, we study if using              represents memory by an address map. Its aim is to provide a
pointer caching improves solver performance.                              reference semantics for the borrow checker separate from the
   The experiments are run on an Intel(R) Xeon(R) E5-2680                 production version in the Rust compiler. Stacked Borrows is
CPU operating at 2.70GHz with 64 GiB of main memory.                      implemented in the MIR interpreter (MIRI) and is part of the
The generated VC are solved using Z3 [15] smtfd tactic. The               Rust standard distribution. We rely heavily on stacked borrows
scatter plot in Fig. 10 shows the solving time for unit proof             to design low-level semantics for this paper.
with ownership semantics (ownsem) in the x-axis. The y-axis                  The Move Prover [5] uses reference elimination to replace
records the solving time for the same unit proof that either uses         a reference by its data. It assumes an alias free memory
shadow memory or main memory as the baseline. The legend                  model and solves the problem of return of a mutable borrow
makes it clear which memory we compare against using either               by recording the origin (lender) of a mutable borrow and
shad or main in the name suffix. We run each flow for increas-            returning data to it explicitly rather than utilizing prophecies.
ing number of byte buffers behind a pointer (e.g., 2, 4, 6, . . . )       RustHorn [3] uses a prophecy value to model return of
and stop when the running time in either ownsem or baseline               a mutable borrow and assumes a safe Rust-like language
mode reaches 100 seconds. The many_buffers benchmark is a                 and, therefore, forgoes modelling an address map entirely.
handcrafted benchmark that shows a consistent 3x improve-                 RustHornBelt [6] extends this work to cover unsafe Rust where
ment for ownsem. The flows from mbedTLS show more spread.                 the safety in the unsafe part is manually proven in Iris [18], a
For small number of buffers, ownsem and baseline are usually              concurrent separation logic prover built on top of Coq [19].
head-to-head. As the number of buffers increase, ownsem out-                 Verus [20], Prusti [21], and Creusot [22] are deductive ver-
performs baseline. For write_handshake_shad, the performance              ifers for Rust. Creusot uses RustHorn style prophecy variables.
boost is 1.3x when using 8 buffers. For write_records_shad,               These deductive tools can model complicated features of the
the performance boost at 8 buffers is 5x. This is shown on                language, like polymorphism, directly. This paper focuses on
the scatter plot. Looking at the SMT solver metrics, we see               low-level memory manipulating programs.
internal metrics like sat conflicts and sat backjumps correlate              The memory models used in CBMC [23], LLBMC [24],
with the timings (See Appendix B for details). When a unit                and stock SeaBMC [10] assume an unsafe language allowing
proof is faster, then it sees fewer conflicts and backjumps               unrestricted aliasing of pointers and support pointer arithmetic.
compared to the baseline. This is indirect evidence that the              Kani [25] is a Rust verifier that compiles to goto-cc, the same
performance boost is due to simplicity of the VC.                         low-level backend as CBMC. Ownership information, though,
   Simplification of VC itself depends on how many memory                 is lost is this conversion. Overall, we expect these low-level
accesses can be soundly replaced by pointer cache accesses.               tools would perform similar to our baseline experiments.
VC simplicity is affected by (1) the extent a conditional
typestate check depends on program memory state, and (2) the                                    VII. C ONCLUSION
number of typestate memory accesses as a fraction of the total               We describe formal ownership semantics for multiple low-
number of memory accesses. As an example, for a conditional               level machines of increasing complexity. Particularly, we ex-
check such as if(*unrelated_ptr == 1){get_cache(ptr);}, a read            plain the mechanism for caching values at fat pointers and
of ptr cache using get_cache does not access ptr memory. How-             keeping the values in-sync with memory. We use the given se-
ever, for the check to be reachable, the guarding if condition            mantics to describe VCGen for BMC such that the number of
does require a memory access. Therefore, it is not always                 occurrences of memory accesses in the VC is reduced. For this
possible to remove dependency on program memory for con-                  we model return of mutable borrows using prophecy values
ditional typestate checks. Also if the unit proof (and the SUT)           added to fat pointers. We evaluate the efficiency of generated
do not set/get typestate checks frequently then replacing such            VC by experiments using the S EA BMC tool. Overall, we see
checks by pointer cache accesses has limited benefits. The data           improvements in solving time and attribute it to the simplicity
and units proofs to reproduce our experiments are available at            of VC.



                                                                      8
                             R EFERENCES                                           [16] R. Jung, J. Jourdan, R. Krebbers, and D. Dreyer, “Rustbelt: securing the
                                                                                        foundations of the rust programming language,” Proc. ACM Program.
 [1] M. Fähndrich and R. DeLine, “Adoption and focus: Practical linear                 Lang., vol. 2, no. POPL, pp. 66:1–66:34, 2018. [Online]. Available:
     types for imperative programming,” in Proceedings of the 2002                      https://doi.org/10.1145/3158154
     ACM SIGPLAN Conference on Programming Language Design and                     [17] A. Weiss, D. Patterson, N. D. Matsakis, and A. Ahmed, “Oxide: The
     Implementation (PLDI), Berlin, Germany, June 17-19, 2002, J. Knoop                 essence of rust,” CoRR, vol. abs/1903.00982, 2019. [Online]. Available:
     and L. J. Hendren, Eds. ACM, 2002, pp. 13–24. [Online]. Available:                 http://arxiv.org/abs/1903.00982
     https://doi.org/10.1145/512529.512532                                         [18] R. Jung, D. Swasey, F. Sieczkowski, K. Svendsen, A. Turon,
 [2] D. Grossman, J. G. Morrisett, T. Jim, M. W. Hicks, Y. Wang,                        L. Birkedal, and D. Dreyer, “Iris: Monoids and invariants as an
     and J. Cheney, “Region-based memory management in cyclone,” in                     orthogonal basis for concurrent reasoning,” in Proceedings of the
     Proceedings of the 2002 ACM SIGPLAN Conference on Programming                      42nd Annual ACM SIGPLAN-SIGACT Symposium on Principles of
     Language Design and Implementation (PLDI), Berlin, Germany, June                   Programming Languages, POPL 2015, Mumbai, India, January 15-17,
     17-19, 2002, J. Knoop and L. J. Hendren, Eds. ACM, 2002, pp.                       2015, S. K. Rajamani and D. Walker, Eds. ACM, 2015, pp. 637–650.
     282–293. [Online]. Available: https://doi.org/10.1145/512529.512563                [Online]. Available: https://doi.org/10.1145/2676726.2676980
                                                                                   [19] C. Developers. (2024) The coq proof assistant. [Online]. Available:
 [3] Y. Matsushita, T. Tsukada, and N. Kobayashi, “Rusthorn: Chc-
                                                                                        https://coq.inria.fr/
     based verification for rust programs,” ACM Trans. Program. Lang.
                                                                                   [20] A. Lattuada, T. Hance, C. Cho, M. Brun, I. Subasinghe, Y. Zhou,
     Syst., vol. 43, no. 4, pp. 15:1–15:54, 2021. [Online]. Available:
                                                                                        J. Howell, B. Parno, and C. Hawblitzel, “Verus: Verifying rust
     https://doi.org/10.1145/3462205
                                                                                        programs using linear ghost types,” Proc. ACM Program. Lang.,
 [4] J. Noble, J. Vitek, and J. Potter, “Flexible alias protection,” in                 vol. 7, no. OOPSLA1, pp. 286–315, 2023. [Online]. Available:
     ECOOP’98 - Object-Oriented Programming, 12th European Conference,                  https://doi.org/10.1145/3586037
     Brussels, Belgium, July 20-24, 1998, Proceedings, ser. Lecture Notes          [21] V. Astrauskas, A. Bı́lý, J. Fiala, Z. Grannan, C. Matheja, P. Müller,
     in Computer Science, E. Jul, Ed., vol. 1445. Springer, 1998, pp.                   F. Poli, and A. J. Summers, “The prusti project: Formal verification
     158–185. [Online]. Available: https://doi.org/10.1007/BFb0054091                   for rust,” in NASA Formal Methods - 14th International Symposium,
 [5] D. L. Dill, W. Grieskamp, J. Park, S. Qadeer, M. Xu, and J. E. Zhong,              NFM 2022, Pasadena, CA, USA, May 24-27, 2022, Proceedings, ser.
     “Fast and reliable formal verification of smart contracts with the move            Lecture Notes in Computer Science, J. V. Deshmukh, K. Havelund,
     prover,” in Tools and Algorithms for the Construction and Analysis of              and I. Perez, Eds., vol. 13260. Springer, 2022, pp. 88–108. [Online].
     Systems - 28th International Conference, TACAS 2022, Held as Part of               Available: https://doi.org/10.1007/978-3-031-06773-0 5
     the European Joint Conferences on Theory and Practice of Software,            [22] X. Denis, J. Jourdan, and C. Marché, “Creusot: A foundry for the
     ETAPS 2022, Munich, Germany, April 2-7, 2022, Proceedings, Part                    deductive verification of rust programs,” in Formal Methods and
     I, ser. Lecture Notes in Computer Science, D. Fisman and G. Rosu,                  Software Engineering - 23rd International Conference on Formal
     Eds., vol. 13243. Springer, 2022, pp. 183–200. [Online]. Available:                Engineering Methods, ICFEM 2022, Madrid, Spain, October 24-27,
     https://doi.org/10.1007/978-3-030-99524-9 10                                       2022, Proceedings, ser. Lecture Notes in Computer Science, A. Riesco
 [6] Y. Matsushita, X. Denis, J. Jourdan, and D. Dreyer, “Rusthornbelt:                 and M. Zhang, Eds., vol. 13478. Springer, 2022, pp. 90–105. [Online].
     a semantic foundation for functional verification of rust programs                 Available: https://doi.org/10.1007/978-3-031-17244-1 6
     with unsafe code,” in PLDI ’22: 43rd ACM SIGPLAN International                [23] D. Kroening, P. Schrammel, and M. Tautschnig, “CBMC: the C
     Conference on Programming Language Design and Implementation,                      bounded model checker,” CoRR, vol. abs/2302.02384, 2023. [Online].
     San Diego, CA, USA, June 13 - 17, 2022, R. Jhala and                               Available: https://doi.org/10.48550/arXiv.2302.02384
     I. Dillig, Eds. ACM, 2022, pp. 841–856. [Online]. Available:                  [24] F. Merz, S. Falke, and C. Sinz, “LLBMC: bounded model checking
     https://doi.org/10.1145/3519939.3523704                                            of C and C++ programs using a compiler IR,” in Verified Software:
 [7] L. Developers. (2024) llvm website. [Online]. Available: https:                    Theories, Tools, Experiments - 4th International Conference, VSTTE
     //llvm.org/docs/LangRef.html#noalias-and-alias-scope-metadata                      2012, Philadelphia, PA, USA, January 28-29, 2012. Proceedings, ser.
 [8] R. Developers. (2024) Rust website. [Online]. Available: https:                    Lecture Notes in Computer Science, R. Joshi, P. Müller, and A. Podelski,
     //github.com/rust-lang/rust/issues/54878#issuecomment-429578187                    Eds., vol. 7152. Springer, 2012, pp. 146–161.
 [9] M. Abadi and L. Lamport, “The existence of refinement mappings,”              [25] K. Developers. (2023) The kani book. [Online]. Available: https:
     Theor. Comput. Sci., vol. 82, no. 2, pp. 253–284, 1991. [Online].                  //model-checking.github.io/kani/
     Available: https://doi.org/10.1016/0304-3975(91)90224-P
[10] S. Priya, Y. Su, Y. Bao, X. Zhou, Y. Vizel, and A. Gurfinkel, “Bounded                                        A PPENDIX
     model checking for LLVM,” in 22nd Formal Methods in Computer-
     Aided Design, FMCAD 2022, Trento, Italy, October 17-21, 2022,                 A. Appendix A
     A. Griggio and N. Rungta, Eds. IEEE, 2022, pp. 214–224. [Online].
     Available: https://doi.org/10.34727/2022/isbn.978-3-85448-053-2 28            Semantics of M3 . The machines M0 and M1 do not support
[11] R. Jung, H. Dang, J. Kang, and D. Dreyer, “Stacked borrows: an aliasing       storage of fat pointers to memory. We now define an extension
     model for rust,” Proc. ACM Program. Lang., vol. 4, no. POPL, pp.              to M1 called M3 , that allows this in Table III. We only
     41:1–41:32, 2020. [Online]. Available: https://doi.org/10.1145/3371109
[12] R. E. Strom and S. Yemini, “Typestate: A programming language con-
                                                                                   show definitions for instructions that change from M1 . A
     cept for enhancing software reliability,” IEEE Transactions on Software       die instruction returns a mutable borrow as before. However,
     Engineering, vol. SE-12, no. 1, pp. 157–171, 1986.                            since the succeeding pointer may exist in the register map or
[13] N. Nethercote and J. Seward, “How to shadow every byte of
     memory used by a program,” in Proceedings of the 3rd International
                                                                                   memory map, the search for tagp now occurs in both maps.
     Conference on Virtual Execution Environments, VEE 2007, San                   Once the succeeding pointer is found, the pointer cache is
     Diego, California, USA, June 13-15, 2007, C. Krintz, S. Hand,                 updated as before to nq .
     and D. Tarditi, Eds. ACM, 2007, pp. 65–74. [Online]. Available:
     https://doi.org/10.1145/1254810.1254820
                                                                                      A store and load operation now becomes more involved.
[14] mbedTLS Developers. (2023) mbedtls project. [Online]. Available:              This is because when storing a fat pointer in memory, the
     https://github.com/Mbed-TLS/mbedtls                                           memory must be wide enough to contain (addr, tag, val)
[15] L. M. de Moura and N. S. Bjørner, “Z3: an efficient SMT solver,” in           fields. However, the val field may itself be a pointer, leading
     Tools and Algorithms for the Construction and Analysis of Systems,
     14th International Conference, TACAS 2008, Held as Part of the Joint          to unbounded recursion. We work around this by bounding the
     European Conferences on Theory and Practice of Software, ETAPS                memory to be wide enough to contain (addr, tag, val) where
     2008, Budapest, Hungary, March 29-April 6, 2008. Proceedings, ser.            val is word size. A store of a value r using pointer-to-pointer
     Lecture Notes in Computer Science, C. R. Ramakrishnan and J. Rehof,
     Eds., vol. 4963. Springer, 2008, pp. 337–340. [Online]. Available:            p has two cases. If r is a (scalar) value then it is stored (and
     https://doi.org/10.1007/978-3-540-78800-3 24                                  cached) as in M1 . If r is a fat pointer then we remove the r.val



                                                                               9
     Operation                 Pre-condition                  Post-condition
                                                              (∃p.R[p] = (q.addr, tagp , ) =⇒ R[p] = (q.addr, tagp , nq )),
     die q                     R[q] = (q.addr, tagq , nq )
                                                              (∃a.M [a] = (q.addr, tagp , ) =⇒ M [a] = (q.addr, tagp , nq ))
                                                              R[p] = (p.addr, tagp , vs ), M [p.addr] = vs ,
     m1 = store r, p, m0       R[p] = (p.addr, tagp , )       (r = v) =⇒ (vs = v),
                                                              (r = (tag, t, v)) =⇒ (vs = (tag, t))
                                                              R[r] = vr ,
                                                              R[p] = (p.addr, tagp , vr ),
                                                              (B0 = ∅, tp ∈ {o, mb},
     r = load p, m             R[p] = (p.addr, tagp , vp )
                                                                 ((∃addrp1 ∃tagp1 .(addrp1 , tagp1 ) = vp , vp1 = M [addrp1 ]) =⇒ (vr = (addrp1 , tagp1 , vp1 ))),
                                                                 (∃v.v = vp ) =⇒ (vr = v)),
                                                              (tp = c =⇒ (vr = M [p.addr])

TABLE III: Effect of selected operations on SB ,R, and M in machine M3 . The remaining instructions stay the same as Table II.




           30000                                                                             25000

           25000
                                                                                             20000
           20000
                                                                                             15000
Baseline




                                                                                  Baseline


           15000
                                                                                             10000
           10000                                   flight_append_shad                                                                flight_append_shad
                                                   write_handshake_shad                                                              write_handshake_shad
                                                   write_handshake_main                      5000                                    write_handshake_main
           5000                                    many_buffers_main                                                                 many_buffers_main
                                                   y=x                                                                               y=x
                                                   y = 3x                                                                            y = 3x
              0                                                                                 0
                   0   5000   10000    15000     20000       25000    30000                          0   5000   10000        15000        20000       25000
                                      Ownsem                                                                            Ownsem

Fig. 11: Number of SAT conflicts using ownership semantics vs                       Fig. 12: Number of SAT backjumps using ownership semantics vs
baseline.                                                                           baseline.
                                                                                    B. Appendix B

field to make a value of type (r.addr, r.tag). This value is then                      Solving time gives an overall measure of how caching
written both to memory and to p.val. Therefore, the pointer                         at pointer (ownsem) compares to memory (baseline). For
cache now contains either a scalar or a tuple (r.addr, r.tag).                      evidence that ownsem problems are easier for the SMT solver,
                                                                                    we look at the number of conflicts in (Fig. 11) and number
   A load has three distinct behaviours. First, if the lender                       of backjumps (Fig. 12) in both settings. The dots correspond
pointer p is (1) top of borrow stack, and (2) mutably borrowed                      to different number of buffer as in Section V. We can see the
or owning, and (3) a bit-vector (scalar) value, then the read                       number of conflicts in ownsem is generally much lower than
from memory is replaced by a read of the p.val field. Second,                       baseline configurations. The write_handshake_shad flow is an
if the load uses a lender pointer p that is (1) top of borrow                       exception and, correspondingly, the speedup obtained is lowest
stack, and (2) mutably borrowed or owning, and (3) a partial                        in this case (1.3x). The write_records_shad ownsem flow reports
pointer value (p.addr, p.tag), then the read from memory                            only one conflict consistently for all buffer sizes vs a large
is replaced by a read of the p.val (cache) field. This is                           number of conflicts (around 500k) for baseline for 8 buffers.
used to write (r.addr, r.tag) Additionally, memory is read at                       Including this metric would skew the graph towards larger
M [addr] to get the r.val field. The construction of the value                      numbers hiding details, hence we exclude it. The number
(r.addr, r.tag, r.val) is now complete. In the third case, the                      of backjumps follows a similar trajectory where the number
load uses a copied lender pointer p and value is read directly                      of backjumps seen for ownsem is lower than baseline with
from memory. Note that in this case, if r is a pointer then its                     the exception of write_handshake_shad. The write_records_shad
cache will contain a garbage value. With these changes, M3                          flow again shows lower number of backjumps for ownsem vs
is a practical machine that can load and store pointers.                            baseline. We do not include it so as to not skew the graph



                                                                               10
towards larger numbers. Overall, both the number of conflicts
and the number of backjumps correlate strongly with faster
solving time.




                                                                11
