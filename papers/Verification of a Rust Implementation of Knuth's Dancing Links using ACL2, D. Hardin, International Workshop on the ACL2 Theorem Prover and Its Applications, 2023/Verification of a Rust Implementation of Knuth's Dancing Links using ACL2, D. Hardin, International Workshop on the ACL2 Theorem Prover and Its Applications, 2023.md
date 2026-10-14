    Verification of a Rust Implementation of Knuth’s Dancing
                        Links using ACL2

                                               David S. Hardin
                                              Cedar Rapids, IA USA
                                          david.s.hardin@gmail.com


      “Dancing Links” connotes an optimization to a circular doubly-linked list data structure implementa-
      tion which provides for fast list element removal and restoration. The Dancing Links optimization is
      used primarily in fast algorithms to find exact covers, and has been popularized by Knuth in Volume
      4B of his seminal series The Art of Computer Programming. We describe an implementation of the
      Dancing Links optimization in the Rust programming language, as well as its formal verification
      using the ACL2 theorem prover. Rust has garnered significant endorsement in the past few years as
      a modern, memory-safe successor to C/C++ at companies such as Amazon, Google, and Microsoft,
      and is being integrated into both the Linux and Windows operating system kernels. Our interest in
      Rust stems from its potential as a hardware/software co-assurance language, with application to criti-
      cal systems. We have crafted a Rust subset, inspired by Russinoff’s Restricted Algorithmic C (RAC),
      which we have imaginatively named Restricted Algorithmic Rust, or RAR. In previous work, we de-
      scribed our initial implementation of a RAR toolchain, wherein we simply transpile the RAR source
      into RAC. By so doing, we leverage a number of existing hardware/software co-assurance tools with
      a minimum investment of time and effort. In this paper, we describe the RAR Rust subset, describe
      our improved prototype RAR toolchain, and detail the design and verification of a circular doubly-
      linked list data structure employing the Dancing Links optimization in RAR, with full proofs of
      functional correctness accomplished using the ACL2 theorem prover.


1    Introduction
The exact cover problem [17], in its simplest form, attempts to find, for an n × m matrix with binary
elements, all of the subsets of the rows of the matrix such that all the column sums are exactly one. This
basic notion naturally extends to matrix elements that are in some numerical range; indeed, the popular
puzzle game Sudoku is an extended exact cover problem for a 9 × 9 matrix with element values in the
range of 1 to 9, inclusive.
     The exact cover problem is NP-complete, but computer scientists have devised recursive, nonde-
terministic backtracking algorithms to find exact covers. One such procedure is Knuth’s Algorithm X,
described in [17]. In this algorithm, elements of the matrix are connected via circular doubly-linked lists,
and individual elements are removed, or restored, as the algorithm proceeds, undergoing backtracking,
etc. As these removals and restorations out of/into the list are quite common, making these operations
efficient is a laudable goal. This is where Knuth’s “Dancing Links” comes in, resulting in an optimized
algorithm for finding exact covers which Knuth calls DLX (Dancing Links applied to algorithm X).


2    Dancing Links
The concept behind Dancing Links is quite simple: when a given element Y of a list is removed in
an exact cover algorithm, it is very likely that this same element will later be restored. Thus, rather

                                                                             © D.S. Hardin
A. Coglio, S. Swords (Eds.): 18th ACL2 Workshop (ACL2-2023)
                                                                             This work is licensed under the
EPTCS 393, 2023, pp. 161–174, doi:10.4204/EPTCS.393.13
                                                                             Creative Commons Attribution License.
162                                                        Verification of Rust Dancing Links using ACL2


                           Element               Element               Element
                              X                     X                     X
                        next         prev                  prev     next         prev

                           Element               Element               Element
                              Y                     Y                     Y
                        next         prev     next                  next         prev

                           Element               Element               Element
                              Z                     Z                     Z

                               (a)                   (b)                   (c)

Figure 1: Dancing Links in action. (a) Portion of a circular doubly-linked list prior to a remove operation;
(b) After the remove operation on element Y; (c) After the restore operation for element Y.


than “zero out” the ‘previous’ and ‘next’ links associated with element Y, as good programming hygiene
would normally dictate, in Dancing Links, the programmer leaves the link values in place for the removed
element. The Dancing Links remove operator thus deletes element Y from the list, setting the ’next’
element of the preceding element X to the following element Z, and setting the ’previous’ element of Z
to a link to X, but not touching the ’next’ and ’previous’ links of the removed element Y. Later on, if Y
needs to be restored, it is simply hooked back in to the list using a simple restore operator. In Knuth’s
words, if one monitors the list links as the DLX algorithm proceeds, the links appear to ‘dance’, hence
the name. Knuth’s Dancing Links functionality is summarized in Fig. 1.


3     The Rust Programming Language
The Rust programming language has garnered significant interest and use as a modern, type-safe, memory-
safe, and potentially formally analyzable programming language. Google [29] and Amazon [25] are
major Rust adopters, and Linus Torvalds has commented positively on the near-term ability of the Rust
toolchain to be used in Linux kernel development [1]. And after spending decades dealing with a never-
ending parade of security vulnerabilities due to C/C++, which continue to manifest at a high rate [24]
despite their use of sophisticated C/C++ analysis tools, Microsoft announced at its BlueHat 2023 devel-
oper conference that is was beginning to rewrite core Windows libraries in Rust [6].
    Our interest in Rust stems from its potential as a hardware/software co-assurance language. This
interest is motivated in part by emerging application areas, such as autonomous and semi-autonomous
platforms for land, sea, air, and space, that require sophisticated algorithms and data structures, are sub-
ject to stringent accreditation/certification, and encourage hardware/software co-design approaches. (For
an unmanned aerial vehicle use case illustrating a formal methods-based systems engineering environ-
ment, please consult [7] [23].) In this paper, we explore the use of Rust as a High-Level Synthesis (HLS)
language [26].
    HLS developers specify the high-level abstract behavior of a digital system in a manner that omits
hardware design details such as clocking; the HLS toolchain is then responsible for “filling in the details”
to produce a Register Transfer Level (RTL) structure that can be used to realize the design in hardware.
D.S. Hardin                                                                                            163


HLS development is thus closer to software development than traditional hardware design in Hardware
Description Languages (HDLs) such as Verilog or VHDL. Most incumbent HLS languages are a subset
of C, e.g. Mentor Graphics’ Algorithmic C [21], or Vivado HLS by Xilinx [31], although other languages
have also been used, e.g. OCaml [15]. A Rust-based HLS would bring a single modern, type-safe, and
memory-safe expression language for both hardware and software realizations, with very high assurance.
    For formal methods researchers, Rust presents the opportunity to reason about application-level logic
written in the imperative style favored by industry, but without the snarls of the unrestricted pointers of
C/C++. Much progress has been made to this end in recent years, to the point that developers can ver-
ify the correctness of common algorithm and data structure code that utilizes common idioms such as
records, loops, modular integers, and the like, and verified compilers can guarantee that such code is
compiled correctly to binary [18]. Particular progress has been made in the area of hardware/software
co-design algorithms, where array-backed data structures are common [10, 11]. (NB: This style of pro-
gramming also addresses one of the shortcomings of Rust, namely its lack of support for cyclic data
structures.)
    As a study of the suitability of Rust as an HLS, we have crafted a Rust subset, inspired by Russinoff’s
Restricted Algorithmic C (RAC) [27], which we have imaginatively named Restricted Algorithmic Rust,
or RAR [13]. In fact, in our first implementation of a RAR toolchain, we merely “transpile” (perform a
source-to-source translation of) the RAR source into RAC. By so doing, we leverage a number of existing
hardware/software co-assurance tools with a minimum investment of time and effort. By transpiling
RAR to RAC, we gain access to existing HLS compilers (with the help of some simple C preprocessor
directives, we are able to generate code for either the Algorithmic C or Vivado HLS toolchains). But most
importantly for our research, we leverage the RAC-to-ACL2 translator that Russinoff and colleagues at
Arm have successfully utilized in industrial-strength floating point hardware verification.
   We have implemented several representative algorithms and data structures in RAR, including:


    • a suite of array-backed algebraic data types, previously implemented in RAC (as reported in [10]);

    • a significant subset of the Monocypher [30] modern cryptography suite, including XChacha20
      and Poly1305 (RFC 8439) encryption/decryption, BLAKE2b hashing, and X25519 public key
      cryptography [12]; and

    • a DFA-based JSON lexer, coupled with an LL(1) JSON parser. The JSON parser has also been
      implemented using Greibach Normal Form (previously implemented in RAC, as described in [14]).


    The RAR examples created to date are similar to their RAC counterparts in terms of expressive-
ness, and we deem the RAR versions somewhat superior in terms of readability (granted, this is a very
subjective evaluation).
     In this paper, we will describe the development and formal verification of an array-based circular
doubly-linked list (CDLL) data structure in RAR, including the Dancing Links optimization. Along the
way, we will introduce the RAR subset of Rust, the RAR toolchain, the CDLL example, and detail our
ACL2-based verification techniques, as well as the ACL2 books that we brought to bear on this example.
It is hoped that this explication will convince the reader of the practicality of RAR as a high-assurance
hardware/software co-design language, as well as the feasibility of the performing full functional cor-
rectness proofs of RAR code. We will then conclude with related and future work.
164                                                       Verification of Rust Dancing Links using ACL2


                              Algorithmic C
                                 Headers                                 Lemmas

                                       #include
                              Algorithmic C            ACL2               ACL2
                                                                         Theorem
                                 Source              Translator           Prover


                          C++           Hardware                          Proofs
                         Compiler       Synthesis

                           Figure 2: Restricted Algorithmic C (RAC) toolchain.

          Formal Verification “Comfort Zone”                       Real-World Development
                Functional programming                              Imperative programming
               Total, terminating functions              Partial, potentially non-terminating functions
              Non-tail-recursive functions                                    Loops
    Okasaki-style pure functional algebraic data types                   Structs, Arrays
            Infinite-precision Integers, Reals            Modular Integers, IEEE 754 floating point
                    Linear Arithmetic                          Linear and Non-linear Arithmetic
                Arithmetic or Bit Vectors                          Arithmetic and Bit Vectors


                    Table 1: Formal verification vs. real-world development attributes.


4     RAC: Hardware/Software Co-Assurance at Scale
In order to begin to realize hardware/software co-assurance at scale, we have conducted several experi-
ments employing a state-of-the-art toolchain, due to Russinoff and O’Leary, and originally designed for
use in floating-point hardware verification [27], to determine its suitability for the creation of safety-
critical/security-critical applications in various domains. Note that this toolchain has already demon-
strated the capability to scale to industrial designs in the floating-point hardware design and verification
domain, as it has been used in design verifications for CPU products at both Intel and Arm.
     Algorithmic C [21] is a High-Level Synthesis (HLS) language, and is supported by hardware/software
co-design environments from Mentor Graphics, e.g., Catapult [22]. Algorithmic C defines C++ header
files that enable compilation to both hardware and software platforms, including support for the peculiar
bit widths employed, for example, in floating-point hardware design.
     The Russinoff-O’Leary Restricted Algorithmic C (RAC) toolchain, depicted in Fig. 2, translates a
subset of Algorithmic C source to the Common Lisp subset supported by the ACL2 theorem prover, as
augmented by Russinoff’s Register Transfer Logic (RTL) books.
     The ACL2 Translator component of Fig. 2 provides a case study in the bridging of Formal Model-
ing and Real-World Development concerns, as summarized in Table 1. The ACL2 translator converts
imperative RAC code to functional ACL2 code. Loops are translated into tail-recursive functions, with
automatic generation of measure functions to guarantee admission into the logic of ACL2 (RAC subset-
ting rules ensure that loop measures can be automatically determined). Structs and arrays are converted
D.S. Hardin                                                                                            165


into functional ACL2 records. The combination of modular arithmetic and bit-vector operations of typi-
cal RAC source code is faithfully translated to functions supported by Russinoff’s RTL books. ACL2 is
able to reason about non-linear arithmetic functions, so the usual concern about formal reasoning about
non-linear arithmetic functions does not apply. Finally, the RTL books are quite capable of reasoning
about a combination of arithmetic and bit-vector operations, which is a very difficult feat for most auto-
mated solvers.
     Recently, we have investigated the synthesis of Field-Programmable Gate Array (FPGA) hardware
directly from high-level architecture models, in collaboration with colleagues at Kansas State University.
The goal of this work is to enable the generation of high-assurance hardware and/or software from high-
level architectural specifications expressed in the Architecture Analysis and Design Language (AADL)
[9], with proofs of correctness in ACL2.



5    Rust and RAR

The Rust Programming Language [16] is a modern, high-level programming language designed to com-
bine the code generation efficiency of C/C++ with drastically improved type safety and memory man-
agement features. A distinguishing feature of Rust is that a non-scalar object may only have one owner.
For example, one cannot assign a reference to an object in a local variable, and then pass that reference
to a function. This restriction is similar to those imposed on ACL2 single-threaded objects (stobjs) [4],
with the additional complexities of enforcing such “single-owner” restrictions in the context of a general-
purpose, imperative programming language. The Rust runtime performs array bounds checking, as well
as arithmetic overflow checking (the latter can be disabled by a build environment setting).
    In most other ways, Rust is a fairly conventional modern programming language, with interfaces
(called traits), lambdas (termed closures), and pattern matching, as well as a macro capability. Also in
keeping with other modern programming language ecosystems, Rust features a language-specific build
and package management sytem, named cargo.



5.1 Restricted Algorithmic Rust

As we wish to utilize the RAC toolchain as a backend in our initial work, Restricted Algorithmic Rust
is semantically equivalent to RAC. Thus, we adopt the same semantic restrictions as described in Russi-
noff’s book. Additionally, in order to enable translation to RAC, as well as to ease the transition from
C/C++, RAR supports a commonly used macro that provides a C-like for loop in Rust. Note that, despite
the restrictions, RAR code is proper Rust; it compiles to binary using the standard Rust compiler.
     RAR is transpiled to RAC via a source-to-source translator, as depicted in Fig. 3. Our transpiler
is based on the plex parser and lexer generator [28] source code. We thus call our transpiler Plexi,
a nickname given to a famous (and now highly sought-after) line of Marshall guitar amplifiers of the
mid-1960s. Plexi performs lexical and syntactic transformations that convert RAR code to RAC code.
Recent improvements in the plexi tool include better handling of array declarations, as well as providing
support for Rust const declarations.
     The generated RAC code can then be compiled using a C/C++ compiler, fed to an HLS-based FPGA
compiler, as well as translated to ACL2 via the RAC ACL2 translator, as illustrated in Fig. 3.
166                                                       Verification of Rust Dancing Links using ACL2


                                              Algorithmic C
                                                 Headers                                 Lemmas

                                                       #include
         Rust              Plexi              Algorithmic C             ACL2              ACL2
                         Transpiler                                                      Theorem
        Source                                   Source               Translator          Prover


                                         C++            Hardware                          Proofs
                                        Compiler        Synthesis

                        Figure 3: Restricted Algorithmic Rust (RAR) toolchain.

6     Dancing Links in Rust
In this section, we describe an array-based circular doubly-linked list (CDLL) employing Knuth’s “Danc-
ing Links” optimization, realized using our RAR Rust subset. The CDLL data structure implementation
constitutes over 700 lines of Rust code, which becomes 890 lines of code when translated to ACL2.

6.1 Definitions
First, we present the basic RAR declaration for the CDLL.


const CDLL_MAX_NODE1: usize = 8191;
const CDLL_MAX_NODE: usize = CDLL_MAX_NODE1 - 1;

#[derive(Copy, Clone)]
struct CDLLNode {
  alloc: u2,
  val: i64,
  prev: usize,
  next: usize,
}

#[derive(Copy, Clone)]
struct CDLL {
  nodeHd: usize,
  nodeCount: usize,
  nodeArr: [CDLLNode; CDLL_MAX_NODE1],
}
    Rust data structure declarations are similar to those in C, but struct elements are declared by specify-
ing the element name, followed by the : separator, then the element type. Also note that Rust pragmas
may be given using the derive attribute. In the declaration above, the array nodeArr holds the list
element nodes. Each element has next and prev indices. Note that indices in Rust are normally de-
clared to be of the usize type. Note also that by using array indices instead of references, we get around
D.S. Hardin                                                                                          167

fn CDLL_remove(n: usize, mut CDObj: CDLL) -> CDLL {
  if (n > CDLL_MAX_NODE) {
    return CDObj;
  } else {
    if (n == CDObj.nodeHd) { // Can’t remove head
      return CDObj;
    } else {
      if (CDObj.nodeCount < 3) { // Need three elements for remove to work
        return CDObj;
      } else {
        let nextNode: usize = CDObj.nodeArr[n].next;
        let prevNode: usize = CDObj.nodeArr[n].prev;

                CDObj.nodeArr[prevNode].next = nextNode;
                CDObj.nodeArr[nextNode].prev = prevNode;

                CDObj.nodeCount = CDObj.nodeCount - 1;

                return CDObj;
            }
        }
    }
}



                                Figure 4: cdll_remove() function in RAR.


Rust ownership model issues with circular data structures. The alloc field of the CDLLNode structure
is declared to be a two bit unsigned field, but its only allowed values are two non-zero values: 2 (not
currently allocated), and 3 (allocated). The reason for this has to do with the details of ACL2 untyped
record reasoning, which will be discussed in Section 6.2.
     The Dancing Links operators cdll_remove and cdll_restore are presented in Figures 4 and 5,
respectively. Rust functions begin with the fn keyword, followed by the function name, a parenthesized
list of parameters, the -> (returns) symbol, the return type name, followed by the function body (de-
limited by a curly brace pair). A function parameter list element consists of the parameter name, the
: symbol, then the parameter type. Additional parameter modifiers, for example mut, may be present
to indicate that the parameter is changed in the function body. Within the function body, the syntax is
similar to other C-like languages, but local variable declarations begin with let, and use the variable
name, :, variable type declaration syntax. A local variable declaration may also require the mut modifier
if that local variable is updated after its initialization.


6.2 Translation to ACL2
We use Plexi to transpile the RAR source to RAC (not shown), then use the RAC translator to convert
the resulting RAC source to ACL2. The translation of cdll_restore() appears in Fig. 6.
168                                                     Verification of Rust Dancing Links using ACL2




fn CDLL_restore(n: usize, mut CDObj: CDLL) -> CDLL {
  if (n > CDLL_MAX_NODE) {
    return CDObj;
  } else {
    if (n == CDObj.nodeHd) { // Can’t restore head
      return CDObj;
    } else {
      if ((CDObj.nodeCount < 2) ||         // Need two elements for restore to work
           (CDObj.nodeCount == CDLL_MAX_NODE1)) { // Can’t restore to a full list
        return CDObj;
      } else {

                let prevNode: usize = CDObj.nodeArr[n].prev;
                let nextNode: usize = CDObj.nodeArr[n].next;

                CDObj.nodeArr[prevNode].next = n;
                CDObj.nodeArr[nextNode].prev = n;

                CDObj.nodeCount = CDObj.nodeCount + 1;

                return CDObj;
            }
        }
    }
}



                                Figure 5: cdll_restore() function in RAR.
D.S. Hardin                                                                               169




(DEFUND CDLL_RESTORE (N CDOBJ)
   (IF1 (LOG> N (CDLL_MAX_NODE))
        CDOBJ
        (IF1 (LOG= N (AG ’NODEHD CDOBJ))
             CDOBJ
             (IF1 (LOGIOR1 (LOG< (AG ’NODECOUNT CDOBJ) 2)
                           (LOG= (AG ’NODECOUNT CDOBJ)
                                 (CDLL_MAX_NODE1)))
                  CDOBJ
                  (LET* ((PREVNODE (AG ’PREV (AG N (AG ’NODEARR CDOBJ))))
                         (NEXTNODE (AG ’NEXT (AG N (AG ’NODEARR CDOBJ))))
                         (CDOBJ (AS ’NODEARR
                                    (AS PREVNODE
                                        (AS ’NEXT
                                            N (AG PREVNODE (AG ’NODEARR CDOBJ)))
                                        (AG ’NODEARR CDOBJ))
                                    CDOBJ))
                         (CDOBJ (AS ’NODEARR
                                    (AS NEXTNODE
                                        (AS ’PREV
                                            N (AG NEXTNODE (AG ’NODEARR CDOBJ)))
                                        (AG ’NODEARR CDOBJ))
                                    CDOBJ)))
                        (AS ’NODECOUNT
                            (+ (AG ’NODECOUNT CDOBJ) 1)
                            CDOBJ))))))



              Figure 6: cdll_restore() function translated to ACL2 using the RAC tools.
170                                                        Verification of Rust Dancing Links using ACL2


    The first thing to note about Fig. 6 is that, even though we are two translation steps away from
the original RAR source, the translated function is nonetheless quite readable, which is a rare thing for
machine-generated code. Another notable observation is that struct and array ‘get’ and ‘set’ operations
become untyped record operators, AG and AS, respectively — these are slight RAC-specific customiza-
tions of the usual ACL2 untyped record operators. Further, IF1 is a RAC-specific macro, and LOG>,
LOG=, LOG<, and LOGIOR1 are all RTL functions. Thus, much of the proof effort involved with RAR
code is reasoning about untyped records and RTL — although not a lot of RTL-specific knowledge is
needed, at least in our experience.
    One aspect of untyped records that can be tricky is that record elements that take on the default value
are not explicitly stored in the association list for the record. For RAC untyped records, that default value
is zero. Thus, it is easy for a given record to attain a nil value. When reasoning about arrays of such
records, it is often desirable to be able to state that the array size remains constant. Thus, for example, for
the CDLL array nodeArr of Section 6.1, we ensure that all CDLLNode elements of that array are non-nil
by making sure that the alloc fields of the CDLLNode elements are always non-zero (2 or 3).


6.3 Dancing Links Theorems
Once we have translated the circular doubly-linked list functions into ACL2, we can begin to prove
theorems about the data structure implementation. We begin by defining a “well-formedness” predicate
for CDLLs.

(defun cdllnodeArrp-helper (arr j)
  (cond ((not (true-listp arr)) nil)
        ((null arr) t)
        ((not (and (integerp j) (<= 0 j))) nil)
        ((not (consp (car arr))) nil)
        ((not (= (car (car arr)) j)) nil)
        ((not (cdllnodep (cdr (car arr)))) nil)
        (t (cdllnodeArrp-helper (cdr arr) (1+ j)))))

(defun cdllnodeArrp (arr)
  (cdllnodeArrp-helper arr 0))

(defun cdllp (Obj)
  (and (integerp (ag ’nodeHd Obj))
       (<= 0 (ag ’nodeHd Obj))
       (<= (ag ’nodeHd Obj) (CDLL_MAX_NODE))
       (integerp (ag ’nodeCount Obj))
       (<= 0 (ag ’nodeCount Obj))
       (<= (ag ’nodeCount Obj) (CDLL_MAX_NODE1))
       (cdllnodeArrp (ag ’nodeArr Obj))
       (= (len (ag ’nodeArr Obj)) (CDLL_MAX_NODE1))))

    Given this definition of a good CDLL state, we can prove functional correctness theorems for
Dancing Links operations, of the sort stated below. Note that this proof requires some detailed well-
formedness hypotheses related to the prev and next indices for the nth element:
D.S. Hardin                                                                                            171


(defthm restore-of-remove--thm
 (implies
  (and (cdllp Obj)
       (good-nodep n Obj)
       (not (= n (ag ’nodeHd Obj)))
       (>= (ag ’nodeCount Obj) 3))
  (= (CDLL_restore n (CDLL_remove n Obj))
     Obj)))

    ACL2 performs the correctness proof for this cdll_restore of cdll_remove theorem automati-
cally. In addition to the Dancing Links operator proofs, we have proved approximately 160 theorems
related to the CDLL data structure, including theorems about cdll_cns() (cons equivalent), cdll_-
rst() (cdr equivalent), cdll_snc() (add to end of data structure), cdll_tsr() (delete from end of
data structure), cdll_nth(), etc. All of these proofs will be made publicly available in the ACL2
workshop books repository.


7    Related Work
A number of domain-specific languages targeting both hardware and software realization, and providing
support for formal verification, have been created. Cryptol [5], for example, has been employed as a
“golden spec” for the evaluation of cryptographic implementations, in which automated tools perform
equivalence checking between the Cryptol spec for a given algorithm, and the VHDL implementation.
    Formal verification systems for Rust include Creusot [8], based on WhyML; Prusti [3], based on the
Viper verification toolchain; and RustHorn [20], based on constrained Horn clauses. AWS is developing
a model-checker for Rust, Kani [2]. Additionally, Carnegie-Mellon University is developing Verus,
an SMT-based tool for formally verifying Rust programs [19]. With Verus, programmers express proofs
and specifications using Rust syntax, allowing proofs to take advantage of Rust’s linear types and borrow
checking. It will be interesting to attempt the sorts of correctness proofs achievable on our system using
these verification tools.


8    Conclusion
We have developed a prototype toolchain to allow the Rust programming language to be used as a hard-
ware/software co-design and co-assurance language for critical systems, standing on the shoulders of
Russinoff’s team at Arm, and all the great work they have done on Restricted Algorithmic C. We have
demonstrated the ability to establish the correctness of several practical data structures commonly found
in high-assurance systems (e.g., array-backed singly-linked lists, doubly-linked lists, stacks, and de-
queues) through automated formal verification, enabled by automated source-to-source translation from
Rust to RAC to ACL2, and have detailed the specification and verification of one such data structure, a
circular doubly-linked list employing Knuth’s “Dancing Links” optimization. We have also successfully
applied our toolchain to cryptography and data format filtering examples typical of the sorts of algorithms
that one encounters in critical systems development.
    In future work, we will continue to develop our toolchain, increasing the number of Rust features that
we can support in the RAR subset, as well as continuing to improve the ACL2 verification libraries in
order to increase the ability to discharge RAR correctness proofs automatically. We will also continue to
172                                                             Verification of Rust Dancing Links using ACL2


work with our colleagues at Kansas State University on the direct synthesis and verification of RAR code
from architectural models, as well as working with colleagues at the University of Kansas on verified
synthesis of Rust code from high-level attestation protocol specifications written using the Coq theorem
prover.


9     Acknowledgments
Many thanks to Donald Knuth for his detailed study of exact cover problems in general, and the “Dancing
Links” optimization in particular, that can now be found in Volume 4B of his seminal series, The Art
of Computer Programming. It was a pleasure discovering this particular corner of Computer Science,
beginning when the author accidentally stumbled upon a previously recorded Knuth “Christmas Lecture”
on the subject in late 2022.
    Previous foundational work on hardware/software co-assurance in Rust was funded by DARPA con-
tract HR00111890001. The views, opinions and/or findings expressed are those of the authors and should
not be interpreted as representing the official views or policies of the Department of Defense or the U.S.
Government.
    Many thanks to David Russinoff of Arm for developing and improving the RAC toolchain, without
which most of the current work would not be possible. Thanks also go to the anonymous reviewers for
their insightful comments.


References
 [1] Ron    Amadeo   (2021):       Google    is now    writing  low-level  Android  code
     in    Rust.             Available    at    https://arstechnica.com/gadgets/2021/04/
     google-is-now-writing-low-level-android-code-in-rust/.
 [2] Amazon    Web   Services  (2022):    Announcing  the    Kani Rust   Verifier Project.
     Available      at        https://model-checking.github.io/kani-verifier-blog/2022/
     05/04/announcing-the-kani-rust-verifier-project.html?fbclid=IwAR2M_
     B1IEBfkVhIXSuuAxt3McC_QpUnTuzDq9jG40HOaJzxw8z1Nw9XU_i4.
 [3] V. Astrauskas, A. Bı́lý, J. Fiala, Z. Grannan, C. Matheja, P. Müller, F. Poli & A. J. Summers (2022): The Prusti
     Project: Formal Verification for Rust (invited). In: NASA Formal Methods (14th International Symposium),
     Springer, pp. 88–108, doi:10.1007/978-3-031-06773-0_5. Available at https://link.springer.
     com/chapter/10.1007/978-3-031-06773-0_5.
 [4] Robert S. Boyer & J Strother Moore (2002): Single-Threaded Objects in ACL2. In: Practical Aspects of
     Declarative Languages, 4th International Symposium, PADL 2002, Portland, OR, USA, January 19-20, 2002,
     Proceedings, LNCS 2257, Springer, pp. 9–27, doi:10.1007/3-540-45587-6_3.
 [5] Sally Browning & Philip Weaver (2010): Designing Tunable, Verifiable Cryptographic Hardware Using
     Cryptol. In David S. Hardin, editor: Design and Verification of Microprocessor Systems for High-Assurance
     Applications, Springer, pp. 89–143, doi:10.1007/978-1-4419-1539-9_4.
 [6] Thomas Claburn (2023): Microsoft is busy rewriting core Windows code in memory-safe Rust. Available at
     https://www.theregister.com/2023/04/27/microsoft_windows_rust/.
 [7] Darren Cofer, Isaac Amundson, Junaid Babar, David Hardin, Konrad Slind, Perry Alexander, John Hatcliff,
     Robby, Gerwin Klein, Corey Lewis, Eric Mercer & John Shackleton (2022): Cyber Assured Systems Engi-
     neering at Scale. In: IEEE Security & Privacy, pp. 52–64, doi:10.1109/MSEC.2022.3151733.
 [8] Xavier Denis (2022): Creusot. Available at https://github.com/xldenis/creusot.
D.S. Hardin                                                                                               173


 [9] Peter H. Feiler & David P. Gluch (2012): Model-Based Engineering with AADL: An Introduction to the SAE
     Architecture Analysis & Design Language, 1st edition. Addison-Wesley Professional.
[10] David S. Hardin (2020): Put Me on the RAC. In: Proceedings of the Sixteenth International Workshop on the
     ACL2 Theorem Prover and its Applications (ACL2-20), pp. 142–145, doi:10.4204/eptcs.327.13.
[11] David S. Hardin (2020): Verified Hardware/Software Co-Assurance: Enhancing Safety and Security for
     Critical Systems. In: Proceedings of the 2020 IEEE Systems Conference, doi:10.1109/SysCon47679.
     2020.9381831.
[12] David S. Hardin (2022): Hardware/Software Co-Assurance for the Rust Programming Language Applied to
     Zero-Trust Architecture Development. ACM SIGAda Ada Letters 42(2), pp. 55–61, doi:10.1145/3591335.
     3591340.
[13] David S. Hardin (2022): Hardware/Software Co-Assurance using the Rust Programming Language and
     ACL2. In: Proceedings of the Seventeenth International Workshop on the ACL2 Theorem Prover and its
     Applications (ACL2-22), pp. 202–216, doi:10.4204/EPTCS.359.16.
[14] David S. Hardin & Konrad L. Slind (2021): Formal Synthesis of Filter Components for Use in Security-
     Enhancing Architectural Transformations. In: Proceedings of the Seventh Workshop on Language-Theoretic
     Security, 42nd IEEE Symposium and Workshops on Security and Privacy (LangSec 2021), doi:10.1109/
     SPW53761.2021.00024.
[15] Jane Street Group, LLC (2023): Hardcaml: An OCaml library for designing and testing hardware designs.
     Available at https://github.com/janestreet/hardcaml.
[16] Steve Klabnik & Carol Nichols (2018): The Rust Programming Language. No Starch Press.
[17] Donald E. Knuth (2022): The Art of Computer Programming. 4B: Combinatorial Algorithms, Part 2,
     Addison-Wesley.
[18] Ramana Kumar, Magnus O. Myreen, Michael Norrish & Scott Owens (2014): CakeML: a verified implemen-
     tation of ML. In Suresh Jagannathan & Peter Sewell, editors: The 41st Annual ACM SIGPLAN-SIGACT
     Symposium on Principles of Programming Languages, POPL ’14, San Diego, CA, USA, January 20-21,
     2014, ACM, pp. 179–192, doi:10.1145/2535838.2535841.
[19] Andrea Lattuada, Travis Hance, Chanhee Cho, Matthias Brun, Isitha Subasinghe, Yi Zhou, Jon Howell,
     Bryan Parno & Chris Hawblitzel (2023): Verus: Verifying Rust Programs Using Linear Ghost Types. Proc.
     ACM Program. Lang. 7(OOPSLA1), doi:10.1145/3586037.
[20] Yusuke Matsushita, Takeshi Tsukada & Naoki Kobayashi (2021): RustHorn: CHC-Based Verification for
     Rust Programs. ACM Trans. Program. Lang. Syst. 43(4), doi:10.1145/3462205.
[21] Mentor Graphics Corporation (2016): Algorithmic C (AC) Datatypes. Available at https://www.mentor.
     com/hls-lp/downloads/ac-datatypes.
[22] Mentor Graphics Corporation (2020): Catapult High-Level Synthesis. Available at https://www.mentor.
     com/hls-lp/catapult-high-level-synthesis/.
[23] Eric Mercer, Konrad Slind, Isaac Amundson, Darren Cofer, Junaid Babar & David Hardin (2023): Synthesiz-
     ing Verified Components for Cyber Assured Systems Engineering. In: Software and Systems Modeling, 22,
     pp. 1451–1471, doi:10.1007/s10270-023-01096-3.
[24] Matt Miller (2019): A proactive approach to more secure code. Available at https://msrc-blog.
     microsoft.com/2019/07/16/a-proactive-approach-to-more-secure-code/.
[25] Shane Miller & Carl Lerche (2022): Sustainability with Rust. Available at https://aws.amazon.com/
     blogs/opensource/sustainability-with-rust/.
[26] Razvan Nane, Vlad-Mihai Sima, Christian Pilato, Jongsok Choi, Blair Fort, Andrew Canis, Yu Ting Chen,
     Hsuan Hsiao, Stephen Brown, Fabrizio Ferrandi, Jason Anderson & Koen Bertels (2016): A Survey and Eval-
     uation of FPGA High-Level Synthesis Tools. IEEE Transactions on Computer-Aided Design of Integrated
     Circuits and Systems 35(10), pp. 1591–1604, doi:10.1109/TCAD.2015.2513673.
174                                                        Verification of Rust Dancing Links using ACL2


[27] David M. Russinoff (2022): Formal Verification of Floating-Point Hardware Design: A Mathematical Ap-
     proach, second edition. Springer, doi:10.1007/978-3-030-87181-9.
[28] Geoffry Song (2020): plex: a parser and lexer generator as a Rust procedural macro. Available at https://
     github.com/goffrie/plex.
[29] Jeff Vander Stoep & Stephen Hines (2021): Rust in the Android platform. Available at https://security.
     googleblog.com/2021/04/rust-in-android-platform.html.
[30] Loup Vaillant (2022): Monocypher: Boring Crypto that Simply Works. Available at https://monocypher.
     org.
[31] Xilinx, Inc. (2018):   Vivado Design Suite User Guide:  High-Level Synthesis.  Avail-
     able    at     https://www.xilinx.com/support/documentation/sw_manuals/xilinx2018_3/
     ug902-vivado-high-level-synthesis.pdf.
