                                                         Towards Formal Verification of
                                                            a TPM Software Stack

                                             Yani Ziani1,2[0009−0000−8540−1273] , Nikolai Kosmatov1[0000−0003−1557−2813] ,
                                                               Frédéric Loulergue2[0000−0001−9301−7829] ,
                                                           Daniel Gracia Pérez1[0000−0002−5364−8244] , and
arXiv:2307.16821v2 [cs.SE] 27 Oct 2023




                                                                   Téo Bernier1[0009−0003−4834−7126]
                                                          1
                                                            Thales Research & Technology, Palaiseau, France
                                         {yani.ziani,nikolai.kosmatov,daniel.gracia-perez,teo.bernier}@thalesgroup.com
                                              2
                                                Université d’Orléans, INSA Centre Val de Loire, LIFO EA 4022, France
                                                                frederic.loulergue@univ-orleans.fr



                                                Abstract. The Trusted Platform Module (TPM) is a cryptoprocessor
                                                designed to protect integrity and security of modern computers. Com-
                                                munications with the TPM go through the TPM Software Stack (TSS),
                                                a popular implementation of which is the open-source library tpm2-tss.
                                                Vulnerabilities in its code could allow attackers to recover sensitive in-
                                                formation and take control of the system. This paper describes a case
                                                study on formal verification of tpm2-tss using the Frama-C verification
                                                platform. Heavily based on linked lists and complex data structures,
                                                the library code appears to be highly challenging for the verification
                                                tool. We present several issues and limitations we faced, illustrate them
                                                with examples and present solutions that allowed us to verify functional
                                                properties and the absence of runtime errors for a representative subset of
                                                functions. We describe verification results and desired tool improvements
                                                necessary to achieve a full formal verification of the target code.


                                         1    Introduction
                                         The Trusted Platform Module (TPM) [20] has become a key security compo-
                                         nent in modern computers. The TPM is a cryptoprocessor designed to protect
                                         integrity of the architecture and ensure security of encryption keys stored in it.
                                         The operating system and applications communicate with the TPM through a
                                         set of APIs called TPM Software Stack (TSS). A popular implementation of the
                                         TSS is the open-source library tpm2-tss. It is highly critical: vulnerabilities in its
                                         code could allow attackers to recover sensitive information and take control of
                                         the system. Hence, it is important to formally verify that the library respects its
                                         specification and does not contain runtime errors, often leading to security vul-
                                         nerabilities, for instance, exploiting buffer overflows or invalid pointer accesses.
                                         Formal verification of this library is the main motivation of this work. This tar-
                                         get is new and highly ambitious for deductive verification: the library code is
                                         very large for a formal verification project (over 120,000 lines of C code). It is
                                         also highly complex, heavily based on complex data structures (with multiple
levels of nested structures and unions), low-level code, calls to external (e.g.
cryptography) libraries, linked lists and dynamic memory allocation.
    In this paper we present a first case study on formal verification of tpm2-tss
using the Frama-C verification platform [15]. We focus on a subset of func-
tions involved in storing an encryption key in the TPM, one of the most critical
features of the TSS. We verify both functional properties and the absence of run-
time errors. The functions are annotated in the acsl specification language [2].
Their verification with Frama-C currently faces several limitations of the tool,
such as its capacity to reason about complex data structures, dynamic memory
allocation, linked lists and their separation from other data. We have managed
to overcome these limitations after minor simplifications and adaptations of the
code. In particular, we replace dynamic allocation with calloc by another al-
locator (attributing preallocated memory cells) that we implement, specify and
verify. We adapt a recent work on verification of linked lists [4] to our case
study, add new lemmas and prove them in the Coq proof assistant [19]. We
identify some deficiencies in the new Frama-C–Coq extraction for lists (modi-
fied since [4]), adapt it for the proof and suggest improvements. We illustrate all
issues and solutions on a simple illustrative example while the (slightly adapted)
real-life functions annotated in acsl and fully proved in Frama-C are avail-
able online as a companion artifact3 . Finally, we identify desired extensions and
improvements of the verification tool.
Contributions. The contributions of this paper include the following:
 – specification and formal verification in Frama-C of a representative subset
   of functions of the tpm2-tss library (slightly adapted for verification);
 – presentation of main issues we faced during their verification with an illus-
   trative example, and description of solutions and workarounds we found;
 – proof in Coq of all necessary lemmas (including some new ones) related to
   linked lists, realized for the new version of Frama-C–Coq extraction;
 – a list of necessary enhancements of Frama-C to achieve a complete formal
   verification of the tpm2-tss library.

Outline. The paper is organized as follows. Section 2 presents Frama-C. Sec-
tion 3 introduces the TPM, its software stack and the tpm2-tss library. Sec-
tions 4 and 5 present issues and solutions related, resp., to memory allocation
and memory management. Necessary lemmas are discussed in Sect. 6. Section 7
describes our verification results. Finally, Sect. 8 and 9 present related work and
a conclusion with necessary tool improvements.

2     Frama-C Verification Platform
Frama-C [15] is an open-source verification platform for C code, which con-
tains various plugins built around a kernel providing basic services for source-
code analysis. It offers acsl (ANSI/ISO C Specification Language) [2], a formal
3
    Available (with the illustrative example, all necessary lemmas and their proofs) on
    https://doi.org/10.5281/zenodo.8273295.


                                           2
specification language for C, that allows users to specify functional properties of
programs in the form of annotations, such as assertions or function contracts.
A function contract basically consists of pre- and postconditions (stated, resp.,
by requires and ensures clauses) expressing properties that must hold, resp.,
before and after a call to the function. It also includes an assigns clause listing
(non-local) variables and memory locations that can be modified by the func-
tion. While useful built-in predicates and logic functions are provided to handle
properties such as pointer validity or memory separation for example, acsl also
supplies the user with different ways to define predicates and logic functions.
    Frama-C offers Wp, a plugin for deductive verification. Given a C program
annotated in acsl, Wp generates the corresponding proof obligations (also called
verification conditions) that can be proved either by Wp or, via the Why3
platform [13], by SMT solvers or an interactive proof assistant like Coq [19]. To
ensure the absence of runtime errors (RTE), Wp can automatically add necessary
assertions via a dedicated option, and try to prove them as well.
    Our choice to use Frama-C/Wp is due to its capacity to perform deductive
verification of industrial C code with successful verification case studies [7] and
the fact that it is currently the only tool for C source code verification recognized
by ANSSI, the French Common Criteria certification body, as an acceptable
formal verification technique for the highest certification levels EAL6–EAL7 [8].


3     The TPM Software Stack and the tpm2-tss Library

This section briefly presents the Trusted Platform Module (TPM), its software
stack and the implementation we chose to study: the tpm2-tss library. Readers
can refer to the TPM specification [20] and reference books as [1] for more detail.

TPM Software Stack. The TPM is a standard conceived by the Trusted Com-
puting Group (TCG)4 for a passive secure cryptoprocessor designed to protect
secure hardware from software-based threats. At its base, a TPM is implemented
as a discrete cryptoprocessor chip, attached to the main processor chip and de-
signed to perform cryptographic operations. However, it can also be implemented
as part of the firmware of a regular processor or a software component.
    Nowadays, the TPM is well known for its usage in regular PCs to ensure
integrity and to provide a secure storage for the keys used to encrypt the disk
with Bitlocker and dm-crypt. However, it can be (and is actually) used to provide
other cryptographic services to the Operating System (OS) or applications. For
that purpose, the TCG defines the TPM Software Stack (TSS), a set of specifi-
cations to provide standard APIs to access the functionalities and commands of
the TPM, regardless of the hardware, OS, or environment used.
    The TSS APIs provide different levels of complexity, from the Feature API
(FAPI) for simple and common cryptographic services to the System API (SAPI)
for a one-to-one mapping to the TPM services and commands providing greater
4
    https://trustedcomputinggroup.org/


                                         3
flexibility but complexifying its usage. In between lies the Enhanced System API
(ESAPI) providing SAPI-like functionalities but with slightly limited flexibility.
Other TSS APIs complete the previous ones for common operations like data
formatting and connection with the software or hardware TPM.
    The TSS APIs, as any software component or the TPM itself, can have vul-
nerabilities5 that attackers can exploit to recover sensitive data communicated
with the TPM or take control of the system. We study the verification of one
of the implementations of the TSS, tpm2-tss, starting more precisely with its
implementation of the ESAPI.

ESAPI Layer of tpm2-tss. The ESAPI layer provides functions for decryption
and encryption, managing session data and policies, thus playing an essential
role in the TSS. It is very large (over 50,000 lines of C) and is mainly split into
two parts: the API part containing functions in a one-to-one correspondence
with TPM commands (for instance, the Esys_Create function of the TSS will
correspond to — and call — the TPM2_Create command of the TPM), and the
back-end containing the core of that layer’s functionalities. Each API function
will call several functions of the back-end to carry out various operations on
command parameters, before invoking the lower layers and finally the TPM.
    The ESAPI layer relies on a notion of context (ESYS_CONTEXT) containing all
data the layer needs to store between calls, so it does not need to maintain a
global state. Defined for external applications as an opaque structure, the context
includes, according to the documentation, data needed to communicate to the
TPM, metadata for each TPM resource, and state information. The specification,
however, does not impose any precise data structure: it is up to the developer
to provide a suitable definition. Our target implementation uses complex data
structures and linked lists.


4     Dynamic Memory Allocation
Example Overview. We illustrate our verification case study with a simplified
version of some library functions manipulating linked lists. The illustrative exam-
ple is split into Fig. 1–6 that will be explained below step-by-step. Its full code be-
ing available in the companion artifact, we omit in this paper some less significant
definitions and assertions which are not mandatory to understand the paper (but
we preserve line numbering of the full example for convenience of the reader).
This example is heavily simplified to fit the paper, yet it is representative for most
issues we faced (except the complexity of data structures). It contains a main list
manipulation function, getNode (esys_GetResourceObject in the real code),
used to search for a resource in the list of resources and return it if it is found, or
to create and add it using function createNode (esys_CreateResourceObject
in the real code) if not.
    Figure 1 provides the linked list structure as well as logic definitions used to
handle logic lists in specifications. Our custom allocator (used by createNode) is
5
    Like CVE-2023-22745 and CVE-2020-24455, documented on www.cve.org.


                                          4
     ...
11   typedef struct NODE_T {
12       uint32_t                    handle ;          // the h a n d l e used as r e f e r e n c e
13       RESOURCE                    rsrc ;            // the m e t a d a t a for this rsrc
14       struct NODE_T *                     next ; // next node in the list
15   } NODE_T ; // l i n k e d list of r e s o u r c e
     ...
25   /* @
26       p r e d i c a t e p t r _ s e p _ f r o m _ l i s t{ L }( NODE_T * e , \list<NODE_T *> ll ) =
27          ∀ Z n ; 0 ≤ n < \length ( ll ) ⇒ \ s e p a r a t e d(e , \nth ( ll , n ));
28       p r e d i c a t e d p t r _ s e p _ f r o m _ l i s t{ L }( NODE_T ** e , \list<NODE_T *> ll ) =
29          ∀ Z n ; 0 ≤ n < \length ( ll ) ⇒ \ s e p a r a t e d(e , \nth ( ll , n ));
30       p r e d i c a t e in_list { L }( NODE_T * e , \list<NODE_T *> ll ) =
31          ∃ Z n ; 0 ≤ n < \length ( ll ) ∧ \nth ( ll , n ) == e ;
32       p r e d i c a t e i n _ l i s t _ h a n d l e{ L }( uint32_t out_handle , \list<NODE_T *> ll ) =
33          ∃ Z n ; 0 ≤ n < \length ( ll ) ∧ \nth ( ll , n ) ->handle == o u t _ h a n d l e;
34       i n d u c t i v e l i n k e d _ l l{ L }( NODE_T * bl , NODE_T * el , \list<NODE_T *> ll ) {
35           case l i n k e d _ l l _ n i l{ L }: ∀ NODE_T * el ; l i n k e d _ l l{ L }( el , el , \Nil );
36           case l i n k e d _ l l _ c o n s{ L }: ∀ NODE_T * bl , * el , \list<NODE_T *> tail ;
37               ( \ s e p a r a t e d( bl , el ) ∧ \valid ( bl ) ∧ l i n k e d _ l l{ L }( bl ->next , el , tail ) ∧
38               p t r _ s e p _ f r o m _ l i s t( bl , tail )) ⇒
39                   l i n k e d _ l l{ L }( bl , el , \Cons ( bl , tail ));
40      }
41       p r e d i c a t e u n c h a n g e d _ l l{ L1 , L2 }( \list<NODE_T *> ll ) =
42          ∀ Z n ; 0 ≤ n < \length ( ll ) ⇒
43               \valid { L1 }( \nth ( ll , n )) ∧ \valid { L2 }( \nth ( ll , n )) ∧
44               \at (( \nth ( ll , n )) ->next , L1 ) == \at (( \nth ( ll , n )) ->next , L2 );
     ...
48       axiomatic Node_To_ll {
49           logic \list<NODE_T *> to_ll { L }( NODE_T * beg , NODE_T * end )
50               reads { node ->next | NODE_T * node ; \valid ( node ) ∧
51                                                       in_list ( node , to_ll ( beg , end ))};
52           axiom t o _ l l _ n i l{ L }: ∀ NODE_T * node ; to_ll { L }( node , node ) == \Nil ;
53           axiom t o _ l l _ c o n s{ L }: ∀ NODE_T * beg , * end ;
54               ( \ s e p a r a t e d( beg , end ) ∧ \valid { L }( beg ) ∧
55               p t r _ s e p _ f r o m _ l i s t{ L }( beg , to_ll { L }( beg ->next , end ))) ⇒
56                   to_ll { L }( beg , end ) == \Cons ( beg , to_ll { L }( beg ->next , end ));
57      }
58   */
59
60   # include " l e m m a s _ n o d e _ t. h "


                                      Fig. 1. Linked list and logic definitions.


     defined in Fig. 2. Figure 3 defines a (simplified) context and additional logic def-
     initions to handle pointer separation and memory freshness. The search function
     is shown in Fig. 4 and 5. As it is often done, some acsl notation (e.g. \forall,
     integer, ==>, <=, !=) is pretty-printed (resp., as ∀, Z, ⇒, ≤, 6=). In this section,
     we detail Fig. 1–3.

     Lists of Resources. Lines 11–15 of Fig. 1 show a simplified definition of the
     linked list of resources used in the ESAPI layer of the library. Each node of the
     list consists of a structure containing a handle used as a reference for this node,
     a resource to be stored inside, and a pointer to the next element. The handle
     is supposed to be unique6 . In our example, a resource structure (omitted in
     Fig. 1) is assumed to contain only a few fields of relatively simple types. The real
     code uses a more extensive and complex definition (with several levels of nested
     structures and unions), covering all possible types of TPM resources. While it
     6
         This uniqueness is currently not yet specified in the acsl contracts.


                                                              5
does add some complexity to prove certain properties (as some of them may
require to completely unfold all resource substructures), it does not introduce
new pointers that may affect memory separation properties, so our example
remains representative of the real code regarding linked lists and separation
properties.
    In particular, we need to ensure that the resource list is well-formed — that
is, it is not circular, and does not contain any overlap between nodes — and
stays that way throughout the layer. To accomplish that, we use and adapt the
logic definitions from [4], given on lines 26–44, 48–57 of Fig. 1. To prove the
code, we need to manipulate linked lists and segments of linked lists. Lines 48–
57 define the translating function to_ll that translates a C list defined by a
NODE_T pointer into the corresponding acsl logic list of (pointers to) its nodes.
By convention, the last element end is not included into the resulting logic list. It
can be either NULL for a full linked list, or a non-null pointer to a node for a linked
list segment which stops just before that node. Lines 34–40 show the linking
predicate linked_ll establishing the equivalence between a C linked list and an
acsl logic list. This inductive definition includes memory separation between
nodes, validity of access for each node, as well as the notion of reachability in
linked lists. In acsl, given two pointers p and q, \valid(p) states that *p can be
safely read and written, while \separated(p,q) states that the referred memory
locations *p and *q do not overlap (i.e. all their bytes are disjoint).
    Lines 26–29 provide predicates to handle separation between a list pointer
(or double pointer) and a full list. \nth(l,n) and \length(l) denote, resp., the
n-th element of logic list l and the length of l. The predicate unchanged_ll in
lines 41–44 states that between two labels (i.e. program points) L1 and L2, all
list elements in a logic list refer to a valid memory location at both points, and
that their respective next fields retain the same value. It is used to maintain the
structure of the list throughout the code. Line 60 includes lemmas necessary to
conduct the proof, further discussed in Sec. 6.

Lack of Support for Dynamic Memory Allocation. As mentioned above, per
the TSS specifications, the ESAPI layer does not maintain a global state be-
tween calls to TPM commands. The library code uses contexts with linked lists
of TPM resources, so list nodes need to be dynamically allocated at runtime.
The acsl language provides clauses to handle memory allocations: in particu-
lar, \allocable{L}(p) states that a pointer p refers to the base address of an
unallocated memory block, and \fresh{L1,L2}(p, n) indicates that p refers
to the base address of an unallocated block at label L1, and to an allocated
memory block of size n at label L2. Unfortunately, while the Frama-C/Wp
memory model7 is able to handle dynamic allocation (used internally to manage
local variables), these clauses are not currently supported. Without allocability
and freshness, proving goals involving validity or separation between a newly
allocated node and any other pointer is impossible.
7
    that is, intuitively, the way in which program variables and memory locations are
    internally represented and manipulated by the tool.


                                          6
62    # define _ a l l o c _ m a x 100
63    static NODE_T _ r s r c _ b a n k[ _ a l l o c _ m a x]; // bank used by the s t a t i c a l l o c a t o r
64    static int _ a l l o c _ i d x = 0; // index of the next rsrc node to be a l l o c a t e d
65    /* @
66        p r e d i c a t e v a l i d _ r s r c _ m e m _ b a n k{ L } = 0 ≤ _ a l l o c _ i d x ≤ _ a l l o c _ m a x;
67        p r e d i c a t e l i s t _ s e p _ f r o m _ a l l o c a b l e s{ L }( \list<NODE_T *> ll ) =
68           ∀ int i ; _ a l l o c _ i d x ≤ i < _ a l l o c _ m a x ⇒
69                                                  p t r _ s e p _ f r o m _ l i s t{ L }(& _ r s r c _ b a n k[ i ] , ll );
70        p r e d i c a t e p t r _ s e p _ f r o m _ a l l o c a b l e s{ L }( NODE_T * node ) =
71           ∀ int i ; _ a l l o c _ i d x ≤ i < _ a l l o c _ m a x ⇒ \ s e p a r a t e d( node , & _ r s r c _ b a n k[ i ]);
72        p r e d i c a t e d p t r _ s e p _ f r o m _ a l l o c a b l e s{ L }( NODE_T ** p_node ) =
73           ∀ int i ; _ a l l o c _ i d x ≤ i < _ a l l o c _ m a x ⇒ \ s e p a r a t e d( p_node , & _ r s r c _ b a n k[ i ]);
74    */
      ...
76    /* @
77        requires v a l i d _ r s r c _ m e m _ b a n k;
78        assigns _alloc_idx , _ r s r c _ b a n k[ \old ( _ a l l o c _ i d x)];
79        ensures v a l i d _ r s r c _ m e m _ b a n k;
      ...
89        behavior a l l o c a b l e:
90            assumes 0 ≤ _ a l l o c _ i d x < _ a l l o c _ m a x;
91
92           ensures_ a l l o c _ i d x == \old ( _ a l l o c _ i d x) + 1;
93           ensures\result == &( _ r s r c _ b a n k[ _ a l l o c _ i d x - 1]);
94           ensures\valid ( \result );
95           ensuresz e r o _ r s r c _ n o d e _ t( *( \result ) );
96                 ∀ int i ; 0 ≤ i < _ a l l o c _ m a x ∧ i 6= \old ( _ a l l o c _ i d x) ⇒
             ensures
97                  _ r s r c _ b a n k[ i ] == \old ( _ r s r c _ b a n k[ i ]);
98       disjoint b e h a v i o r s; complete b e h a v i o r s;
99    */
100   NODE_T * c a l l o c _ N O D E _ T()
101   {
102      static const RESOURCE e m p t y _ R E S O U R C E;
103      if ( _ a l l o c _ i d x < _ a l l o c _ m a x) {
104         _ r s r c _ b a n k[ _ a l l o c _ i d x]. handle = ( uint32_t ) 0;
105         _ r s r c _ b a n k[ _ a l l o c _ i d x]. rsrc = e m p t y _ R E S O U R C E;
106         _ r s r c _ b a n k[ _ a l l o c _ i d x]. next = NULL ;
107         _ a l l o c _ i d x += 1;
108         return & _ r s r c _ b a n k[ _ a l l o c _ i d x - 1];
109      }
110      return NULL ;
111   }


                                      Fig. 2. Allocation bank and static allocator.




      Static Memory Allocator. To circumvent that issue, we define in Fig. 2 a bank-
      based static allocator calloc_NODE_T that replaces calls to calloc used in the
      real-life code. It attributes preallocated cells, following some existing implemen-
      tations (like the memb module of Contiki [17]). Line 63 defines a node bank, that
      is, a static array of nodes of size _alloc_max. Line 64 introduces an allocation
      index we use to track the next allocable node and to determine whether an allo-
      cation is possible. Predicate valid_rsrc_mem_bank on line 66 states a validity
      condition for the bank: _alloc_idx must always be between 0 and _alloc_max.
      It is equal to the upper bound if all nodes have been allocated. Predicates lines
      67–73 specify separation between a logic list of nodes (resp., a pointer or a dou-
      ble pointer to a node) and the allocable part of the heap, and is used later on
      to simulate memory freshness.

                                                                       7
    Lines 76–99 show a part of the function contract for the allocator defined
on lines 100–111. The validity of the bank should be true before and after the
function execution (lines 77, 79). Line 78 specifies the variables the function is
allowed to modify. The contract is specified using several cases (called behaviors).
Typically, a behavior considers a subset of possible input states (respecting its
assumes clause) and defines specific postconditions that must be respected for
this subset of inputs. In our case, the provided behaviors are complete (i.e.
cover all states allowed by the function precondition) and their corresponding
subsets are disjoint (line 98). We show only one behavior (lines 89–97) describing
a successful allocation (when an allocable node exists, as stated on line 90).
Postconditions on lines 92–93 ensure the tracking index is incremented by one,
and that the returned pointer points to the first allocable block. While this fact is
sufficient to deduce the validity clause on line 94, we keep the latter as well (and
it is actually expected for any allocator). In the same way, lines 96–97 specify
that the nodes of the bank other than the newly allocated block have not been
modified8 .
    Currently, Frama-C/Wp does not offer a memory model able to handle
byte-level assignments in C objects. To represent as closely as possible the fact
that allocated memory is initialized to zero by a call to calloc in the real-life
code, we initialize each field of the allocated node to zero (see the C code on
lines 104–106 and the postcondition on line 95).

Contexts, Separation Predicates and Freshness. In the target library (and in
our illustrative example), pointers to nodes are not passed directly as function
arguments, but stored in a context variable, and a pointer to the context is
passed as a function argument. Lines 113–116 of Fig. 3 define a simplified context
structure, comprised of an int and a NODE_T pointer to the head of a linked list
of resources.
    Additional predicates to handle memory separation and memory freshness
are defined on lines 118–132. In particular, the ctx_sep_from_list predicate
on lines 118–119 specifies memory separation between a CONTEXT pointer and a
logic list of nodes. Lines 120–121 define separation between such a pointer and
allocables nodes in the bank.
    In C, a successful dynamic allocation of a memory block implies its freshness,
that is, the separation between the newly allocated block (typically located on
the heap) and all pre-existing memory locations (on the heap, stack or static
storages). As this notion of freshness is currently not supported by Frama-
C/Wp, we have to simulate it in another way. Our allocator returns a cell in a
static array, so other global variables — as well as local variables declared within
the scope of a function — will be separated from the node bank. To obtain a
complete freshness within the scope of a function, we need to maintain separation
between the allocable part of the bank and other memory locations accessible
through pointers. In our illustrative example, pointers come from arguments
8
    This property is partly redundant with the assigns clause on line 78 but its presence
    facilitates the verification.


                                            8
113   typedef struct CONTEXT {
114      int p l a c e h o l d e r _ i n t;
115      NODE_T * r s r c _ l i s t;
116   } CONTEXT ;
117   /* @
118      p r e d i c a t e c t x _ s e p _ f r o m _ l i s t( CONTEXT * ctx , \list<NODE_T *> ll ) =
119         ∀ Z i ; 0 ≤ i < \length ( ll ) ⇒ \ s e p a r a t e d( \nth ( ll , i ) , ctx );
120      p r e d i c a t e c t x _ s e p _ f r o m _ a l l o c a b l e s( CONTEXT * ctx ) =
121         ∀ int i ; _ a l l o c _ i d x ≤ i < _ a l l o c _ m a x ⇒ \ s e p a r a t e d( ctx , & _ r s r c _ b a n k[ i ]);
122
123        p r e d i c a t e f r e s h n e s s( CONTEXT * ctx , NODE_T ** node ) =
124            c t x _ s e p _ f r o m _ a l l o c a b l e s( ctx )
125           ∧ l i s t _ s e p _ f r o m _ a l l o c a b l e s( to_ll ( ctx ->rsrc_list , NULL ))
126           ∧ p t r _ s e p _ f r o m _ a l l o c a b l e s( ctx ->r s r c _ l i s t)
127           ∧ p t r _ s e p _ f r o m _ a l l o c a b l e s (* node )
128           ∧ d p t r _ s e p _ f r o m _ a l l o c a b l e s( node );
129
130        p r e d i c a t e s e p _ f r o m _ l i s t{ L }( CONTEXT * ctx , NODE_T ** node ) =
131            c t x _ s e p _ f r o m _ l i s t( ctx , to_ll { L }( ctx ->rsrc_list , NULL ))
132           ∧ d p t r _ s e p _ f r o m _ l i s t( node , to_ll { L }( ctx ->rsrc_list , NULL ));
133   */


      Fig. 3. Context and predicates to handle separation from a list and memory freshness.




      including a pointer to a CONTEXT object (and pointers accessible from it) and a
      double pointer to a NODE_T node. This allows us to define a predicate to handle
      freshness in both function contracts.

          The freshness predicate on lines 123–128 of Fig. 3 specifies memory separa-
      tion between known pointers within the scope of our functions and the allocable
      part of the bank, using separation predicates previously defined on lines 120–121,
      and on lines 67–73 of Fig 2. This predicate will become unnecessary as soon as
      dynamic allocation is fully supported by Frama-C/Wp.

          In the meanwhile, a static allocator with an additional separation predicate
      simulating freshness provides a reasonable solution to verify the target library.
      Since no specific constraint is assumed in our contracts on the position of previ-
      ously allocated list nodes already added to the list, the verification uses a specific
      position in the bank only for the newly allocated node. The fact that the newly
      allocated node does not become valid during the allocation (technically, being
      part of the bank, it was valid in the sense of acsl already before) is compen-
      sated in our contracts by the freshness predicate stating that the new node —
      as one the allocable nodes — was not used in the list before the allocation (cf.
      line 310 in Fig. 4). We expect that the migration from our specific allocator to a
      real-life dynamic allocator — with a more general contract — will be very easy
      to perform, as soon as necessary features are supported by Frama-C.

         Similarly, the sep_from_list predicate on lines 130–132 specifies separation
      between the context’s linked list and known pointers, using predicates on lines
      118–119, and on lines 28–29 of Fig 1.

                                                                  9
5   Memory Management
This section presents how we use the definitions introduced in Sec. 4 to prove
selected ESAPI functions involving linked lists. We also identify separation is-
sues related to limitations of the Typed memory model of Wp, as well as a way
to manage memory to overcome such issues. In this section, we detail Fig. 4–6.

The Search Function. Figure 4 provides the search operation getNode with a
partial contract illustrating functional and memory safety properties we aim to
verify and judge necessary for the proof at a larger scale. Some proof-guiding an-
notations (assertions, loop contracts) have been skipped for readability, but the
code is preserved (mostly with the same line numbers). The arguments include
a context, a handle to search and a double pointer for the returned node.
    Lines 380–416 perform the search of a node by its handle: variable temp_node
iterates over the nodes of the resource list, and the node is returned if its handle
is equal to the searched one (in which case, the function returns 616 for success).
    Lines 420–430 convert the resource handle to a TPM one, call the creation
function to allocate a new node and add it to the list as its new head with the
given handle if the allocation was successful (and return 833 if not). The new
node is returned by createNode in temp_node_2 (again via a double pointer).
    Lines 435–462 perform some modifications on the content of the newly allo-
cated node, without affecting the structure of the list. An error code is returned
in case of a failure, and 1611 (with the allocated node in *node) otherwise. Lines
450–451, 453–454 and 461 provide some assertions to propagate information to
the last return clause of the function, attained in case of the successful addition
of the new element to the list.
    Compared to the real-life code, we have introduced anonymous blocks on lines
380–416 and 422–452 (which are not semantically necessary and were not present
in the original code), as well as two local variables tmp_node and tmp_node2
instead of only one. We explain these code adaptations below.

Contract of the Search Function. Lines 309–375 of Fig. 4 provide a partial func-
tion contract, illustrating two behaviors of getNode: if the element was found
by its handle in the list (cf. lines 325–326), and if the element was not found at
first, but was then successfully allocated and added (cf. lines 355–359), for each
of them specific postconditions are stated. For instance, for the latter behavior,
lines 369–370 ensure that if a new node was successfully allocated and added
to the list, the old head becomes the second element of the list, while line 372
ensures the separation of known pointers from the new list. We specify that the
complete list of provided behaviors must be complete and disjoint (line 374).
    As global preconditions, we notably require for the list to be well-formed
(through the use of the linking predicate, cf. line 313), and the validity of our
bank and freshness of allocable nodes with respect to function arguments and
global variables (cf. line 310). Line 317 requires memory separation of known
pointers from the list of resources using the sep_from_list predicate, and sep-
aration among known pointers using the \separated predicate.

                                        10
309   /* @
310       requires v a l i d _ r s r c _ m e m _ b a n k{ Pre } ∧ f r e s h n e s s( ctx , node );
313       requires l i n k e d _ l l( ctx ->rsrc_list , NULL , to_ll ( ctx ->rsrc_list , NULL ));
317       requires s e p _ f r o m _ l i s t( ctx , node ) ∧ \ s e p a r a t e d( node , ctx );
      ...
321       ensures v a l i d _ r s r c _ m e m _ b a n k ∧ f r e s h n e s s( ctx , node );
      ...
325       behavior h a n d l e _ i n _ l i s t:
326          assumes i n _ l i s t _ h a n d l e( rsrc_handle , to_ll ( ctx ->rsrc_list , NULL ));
      ...
332          ensures u n c h a n g e d _ l l{ Pre , Post }( to_ll ( ctx ->rsrc_list , NULL ));
333          ensures \result == 616;
      ...
355       behavior h a n d l e _ n o t _ i n _ l i s t _ a n d _ n o d e _ a l l o c a t e d:
356          assumes !( i n _ l i s t _ h a n d l e( rsrc_handle , to_ll ( ctx ->rsrc_list , NULL )));
357          assumes r s r c _ h a n d l e ≤ 31 U ∨ ( r s r c _ h a n d l e \in {0 x10AU , 0 x10BU })
358                     ∨ (0 x120U ≤ r s r c _ h a n d l e ≤ 0 x12FU );
359          assumes 0 ≤ _ a l l o c _ i d x < _ a l l o c _ m a x;
      ...
369          ensures \old ( ctx ->r s r c _ l i s t) 6= NULL ⇒
370                      \nth ( to_ll ( ctx ->rsrc_list , NULL ) , 1) == \old ( ctx ->r s r c _ l i s t);
371          ensures l i n k e d _ l l( ctx ->rsrc_list , NULL , to_ll ( ctx ->rsrc_list , NULL ));
372          ensures s e p _ f r o m _ l i s t( ctx , node );
373          ensures \result == 1611;
374       disjoint b e h a v i o r s; complete b e h a v i o r s;
375   */
376   int getNode ( P S E U D O _ C O N T E X T * ctx , uint32_t rsrc_handle , NODE_T ** node ) {
377       /* @ assert l i n k e d _ l l( ctx ->rsrc_list , NULL , to_ll ( ctx ->rsrc_list , NULL ));*/
378       int r ;
379       uint32_t t p m _ h a n d l e;
380      { /* Block added to c i r c u m v e n t issues with the WP memory model */
381          NODE_T * tmp_node ;
401          for ( tmp_node = ctx ->r s r c _ l i s t; tmp_node 6= NULL ;
402               tmp_node = tmp_node ->next ) {
405             if ( tmp_node ->handle == r s r c _ h a n d l e ){* node = tmp_node ; return 616;}
415          }
416      }
420      r = i e s y s _ h a n d l e _ t o _ t p m _ h a n d l e( rsrc_handle , & t p m _ h a n d l e);
422      { /* Block added to c i r c u m v e n t issues with the WP memory model */
423          NODE_T * t m p _ n o d e _ 2 = NULL ;
428          r = c r e a t e N o d e( ctx , rsrc_handle , & t m p _ n o d e _ 2);
429          /* @ assert s e p _ f r o m _ l i s t( ctx , node );*/
430          if ( r == 833) { return r ;};
435          tmp_node_2 ->rsrc . handle = t p m _ h a n d l e;
436          tmp_node_2 ->rsrc . rsrcType = 0;
437          size_t offset = 0;
440          r = u i n t 3 2 _ M a r s h a l( tpm_handle , & tmp_node_2 ->rsrc . name . name [0] ,
441                                                  sizeof ( tmp_node_2 ->rsrc . name . name ) ,& offset );
443          if ( r 6=0) { return r ;};
444          tmp_node_2 ->rsrc . name . size = offset ;
449          * node = t m p _ n o d e _ 2;
450          /* @ assert u n c h a n g e d _ l l{ Pre , Here }(
451                            to_ll { Pre }( \at ( ctx ->rsrc_list , Pre ) , NULL ));*/
452      }
453       /* @ assert u n c h a n g e d _ l l{ Pre , Here }(
454                        to_ll { Pre }( \at ( ctx ->rsrc_list , Pre ) , NULL ));*/
461       /* @ assert s e p _ f r o m _ l i s t( ctx , node );*/
462       return 1611;
463   }


      Fig. 4. The (slightly rewritten) search function, where some annotations are removed.



          As a global postcondition, we require that our bank stays valid, and that
      freshness of the (remaining) allocable nodes relatively to function arguments
      and global variables is maintained (cf. line 321). However, properties regarding

                                                        11
the list itself — such as the preservation of the list when it is not modified (line
332), or ensuring it remains well-formed after being modified (line 371) — have
to be issued to acsl behaviors to be proved, due to the way how local variables
are handled in the memory model of Wp. The logic list properties are much
more difficult for solvers to manipulate in global behaviors.

Memory Model Limitation: an Uprovable Property. Consider the assertion on
line 377 of Fig. 4. Despite the presence of the same property as a precondition
of the function (line 313), currently this assertion cannot be proved by Wp at
the entry point for the real-life version of the function. Basically, the real-life
version can be obtained9 from Fig. 4 by removing the curly braces on lines 380,
416, 422, 452. This issue is due to a limitation of the Wp memory model.
    Indeed, for such an assertion (as in general for any annotation to be proved),
Wp generates a proof obligation, to be proved by either Wp itself or by external
provers via the Why3 platform [13]. Such an obligation includes a representation
of the current state of the program memory. In particular, pointers such as the
resource list ctx->rsrc_list (and by extension, any reachable node of the list)
will be considered part of the heap. To handle the existence of a variable in
memory — should it be the heap, the stack or the static segments — Wp uses
an allocation table to express when memory blocks are used or freed, which is
where the issue lies. For instance, on line 428 of Fig. 4, the temp_node_2 pointer
has its address taken, and is considered as used locally due to requires involving
it in our function contract for createNode. It is consequently transferred to the
memory model, where it has to be allocated.
    Currently, the memory model of Wp does not provide separated allocation
tables for the heap, stack and static segments. Using temp_node_2 the way
it is used on line 428 changes the modification status of the allocation table,
which is then considered as modified as a whole. This affects the status of other
”allocated” (relatively to the memory model) variables as well, including (but
not limited to) any reachable node of the list.
    Therefore, the call to createNode line 428 of Fig. 4 in the real-life code that
uses the address of a local pointer as a third argument is sufficient to affect the
status of the resource list on the scale of the entire function. As a result, the
assertion on line 377 is not proved.

A Workaround. As a workaround (found thanks to an indication of the Wp
team) to the aforementioned issue, we use additional blocks and variable decla-
rations. Figure 5 presents those minor rewrites (with line numbers in alphabetical
style to avoid confusion with the illustrative example). The left side illustrates
the structure of the original C code, where the address of temp_node is taken and
used in the createNode call on line j, and the same pointer is used to iterate on
the list. On the right, we add additional blocks and a new pointer temp_node_2,
9
    another difference — removing variable tmp_node2 declared on line 423 and using
    tmp_node instead — can be ignored in this context.

                                         12
 a    int getNode (... , NODE_T ** node ){                a    int getNode (... , NODE_T ** node ){
 b      // list p r o p e r t i e s u n p r o v a b l e   b      // list p r o p e r t i e s p r o v e d
  c     int r ;                                           c      int r ;
 d                                                        d      {
  e       NODE_T * tmp_node ;                             e        NODE_T * tmp_node ;
  f       ... // i t e r a t e over the list              f        ... // i t e r a t e over the list
 g                                                        g      }
 h                                                        h      {
  i                                                       i        NODE_T * t m p _ n o d e _ 2 = NULL ;
  j       r = c r e a t e N o d e(... , & tmp_node );     j        r = c r e a t e N o d e(... , & t m p _ n o d e _ 2);
 k        ...                                             k        ...
  l       * node = tmp_node ;                             l        * node = t m p _ n o d e _ 2;
 m                                                        m      }
 n        return 1611;                                    n      return 1611;
 o    }                                                   o    }


      Fig. 5. Comparison of the real-life code of getNode (on the left) and its rewriting with
      additional blocks (on the right) for proving list properties.


271   /* @
272       requires \valid ( src ) ∧ \valid ( dest + (0 .. sizeof (* src ) -1));
      ...
279   */
280   void m e m c p y _ c u s t o m( uint8_t * dest , uint32_t * src ) {
281       dest [3] = ( uint8_t )(* src & 0 xFF );
282       dest [2] = ( uint8_t )((* src >> 8) & 0 xFF );
283       dest [1] = ( uint8_t )((* src >> 16) & 0 xFF );
284       dest [0] = ( uint8_t )((* src >> 24) & 0 xFF );
285   }
      ...
298   int u i n t 3 2 _ M a r s h a l( uint32_t in , uint8_t buff [] , size_t buff_size , size_t * offset ){
299       size_t l o c a l _ o f f s e t = 0;
      ...
302       // m e m c p y(& buff [ l o c a l _ o f f s e t] , & in , s i z e o f ( in ));
303       m e m c p y _ c u s t o m(& buff [ l o c a l _ o f f s e t] , & in );
      ...
306   }


                           Fig. 6. Definition for memcpy replacement in marshal.



      initialized to NULL to match the previous iteration over the list. Each block de-
      fines a new scope, outside of which the pointer used by createNode will not
      exist and side-effect-prone allocations will not happen. It solves the issue.


      Additional Proof-Guiding Annotations. Additional annotations (mostly omitted
      in Fig. 4) include, as usual, loop contracts and a few assertions. Assertions
      can help the tool to establish necessary intermediate properties or activate the
      application of relevant lemmas. For instance, assertions of lines 450–451 and
      453–454 help propagate information over the structure of the linked list (by
      its logic list representation) outside of each block, and finally to postconditions.
      Assertions on lines 429 and 461 help propagate separations from the list through
      the function and its anonymous blocks. Some other intermediate assertions are
      needed to prove the unchanged nature of the list. Such additional assertions can
      be tricky to find in some cases and need some experience.

                                                          13
Handling Pointer Casts. Another memory manipulation issue we have encoun-
tered comes from the function call on line 440 in getNode: after having been
added to the resource list, the newly allocated node must have its name (or
more precisely, the name of its resource) set from its TPM handle tpm_handle
(derived from the handle of the node by the function call on line 420). This is
done through marshaling using the uint32_Marshal function, partially shown
on lines 298–306 of Fig. 6, whose role is to store a 4-byte unsigned int (in this
case, our TPM handle) in a flexible array of bytes (the name of the resource).
The function calls memcpy on (commented) line 302, which is the source of our
issue (a correct endianness being ensured by a previous byte swap in in).
    For most functions of the standard libraries, Frama-C provides basic acsl
contracts to handle their use. However, for memory manipulation functions like
memcpy, such contracts rely on pointer casts, whose support in Wp is currently
limited. To circumvent this issue, we define our own memory copy function on
lines 280–285: instead of directly copying the 4-byte unsigned int pointed by
src byte per byte using pointer casts using memcpy, we extract one-byte chunks
using byte shifts and bitmasks (cf. lines 281–284, 303) without casts. Line 272
requires that both source and destination locations are valid, also without casts.
This version is fully handled by Wp. Current contracts are sufficient for the
currently considered functional properties and the absence of runtime errors (and
we expect they will be easy to extend for more precise properties if needed).


6    Lemmas

When SMT solvers become inefficient (e.g. for inductive definitions), it can be
necessary to add lemmas to facilitate the proof. These lemmas can then be
directly instantiated by solvers, but proving them often requires to reason by
induction, with an interactive proof assistant.
    The previous work using logic lists [4] defined and proved several lemmas
using the Coq proof assistant. We have added two new useful lemmas (defined
in Fig. 7) and used twelve of the previous ones to verify both the illustrative
example and the subset of real-life functions. However, because the formalization
of the memory models and various aspects of acsl changed between the version
of Frama-C used in the previous work and the one we use, we could not reuse
the proofs of these lemmas. While older Frama-C versions directly generated
Coq specifications, more recent Frama-C versions let Why3 generate them.
Even if the new translation is close to the previous one, the way logic lists are
handled was modified significantly.
    In the past, Frama-C logic lists were translated into the lists Coq offers in
its standard library: an inductively defined type as usually found in functional
programming languages such as OCaml and Haskell. Such types come with an
induction principle that allows to reason by induction. Without reasoning induc-
tively, it also offers the possibility to reason by case on lists: a list is defined either
as empty, or as built with the cons constructor. In recent versions of Frama-
C, acsl logic lists are axiomatized as follows: two functions nil and cons are

                                            14
    lemma i n _ n e x t _ n o t _ b o u n d _ i n{ L }: ∀ NODE_T * bl , * el , * item , \list<NODE_T *> ll ;
      l i n k e d _ l l( bl , el , ll ) ⇒ in_list ( item , ll ) ⇒ item ->next 6= el ⇒
          in_list ( item ->next , ll );
    lemma l i n k e d _ l l _ s p l i t _ v a r i a n t{ L }:
      ∀ NODE_T * bl , * bound , * el , \list<NODE_T *> l1 , l2 ;
      l i n k e d _ l l( bl , el , l1 ^ l2 ) ⇒ l2 6= \Nil ⇒
      bound == \nth ( l1 ^ l2 , \length ( l1 ^ l2 ) - \length ( l2 )) ⇒
          l i n k e d _ l l( bl , bound , l1 ) ∧ l i n k e d _ l l( bound , el , l2 );


    Fig. 7. New lemmas proved in our verification work (in addition to those in [4]).


declared, as well as a few other functions on lists, including the length of a list
(length), the concatenation of two lists (concat), and getting an element from
a list given its position (nth). However, there is no induction principle to reason
by induction on lists, and because nil and cons are not constructors, it is not
possible to reason by case on lists in this formalization. It is possible to test if
a list is empty, but if not, we do not know that it is built with cons. Writing
new recursive functions on such lists is also very difficult. Indeed, we only have
nth to observe a list, while the usual way to program functions on lists uses the
head and the tail of a list for writing the recursive case.
    Interestingly, when the hypotheses of our lemmas include a fact expressed
using linked_ll, it is still possible to reason by case, because this inductive
predicate is translated into Coq as an inductive predicate. Consequently, there
are only two possible cases for the logic list: either it is empty, or it is built with
cons. When such a hypothesis is missing, we axiomatized a tail function, and
a decomposition principle stating that a list is either nil or cons. These axioms
are quite classic and can be implemented using a list type defined by induction.
We did not need an inductive principle on logic lists as either the lemmas did
not require a proof by induction, or we reasoned inductively on the inductive
predicate linked_ll. However, we proved such an induction principle using only
the axioms we added. It is thus available to prove some other lemmas provided
in [4] — not needed yet in our current work — that were proved by induction
on lists.
    Because of these changes, to prove all lemmas we need, we had to adapt all
previous proof scripts, and in a few cases significantly. The largest proof scripts
are about 100 lines long excluding our axioms, and the shortest takes a dozen
lines. We suggest that the next versions of Frama-C come back to a concrete
representation of lists. Thanks to our approach, we expect that the required
changes in our proofs of lemmas will remain minimal: we will only have to prove
the axioms introduced on tail and our decomposition principle.


7      Verification Results

Proof results, presented in Fig. 8, were obtained by running Frama-C 26.1
(Iron) on a desktop computer running Ubuntu 20.04.4 LTS, with an Intel(R)
Core(TM) i5-6600 CPU @ 3.30 GHz, featuring 4 cores and 4 threads, with 16GB

                                                     15
                                User-provided    RTE              Total
                                    acsl
            Code subset Prover     #Goals      #Goals       #Goals       Time
            Illustrative Qed         105          18     123 (43.62%)
            example      Script       1            0       1 (0.35%)
                         SMT         137          21     158 (56.03%)
                         All    243 (86.17%) 39 (13.83%)      282       5m13s
            Library      Qed         274          38     312 (47.34%)
            code subset Script        5            0       5 (0.76%)
                         SMT         311          31     342 (51.90%)
                         All    590 (89.53%) 69 (10.47%)      659       18m07s

       Fig. 8. Proof results for the illustrative example and the real-life code.


RAM. We ran Frama-C with options -wp-par 3 and -wp-timeout 30. We used
the Alt-Ergo v2.4.3 and CVC4 v1.8 solvers, via Why3 v1.5.1. Both functional
properties and the absence of runtime errors (RTE) were proved. Assertions to
ensure the absence of runtime errors are automatically generated by the Rte
plugin of Frama-C (using the -wp-rte option). Functional properties include
usual properties such as the fact that the well-formedness of the list is preserved,
that a new resource has been successfully added to the resource list, that the
searched element is correctly found if present, etc.
    In our illustrative example, 282 goals were proved in a total time of 5min13s
with 56% proved by SMT solvers, and the rest by the internal simplifier engine
Qed of Wp and one Wp script. The maximum time to prove a goal was 20s.
    Solutions to memory manipulation problems presented in this paper were
used on a larger verification study over 10 different functions of the target library
(excluding macro functions, and interfaces without code whose behaviors needed
to be modeled in acsl), related to linked-list manipulations and some internal
ESAPI feasibility checks and operations (cryptographic operations excluded).
Over 659 goals proved in a total of 18m07s, 52% were proved by SMT solvers
and 47% by Qed. Only 5 Wp proof scripts were used, when automatic proof
either failed or was too slow. This shows a high level of automation achieved
in our project, in particular, thanks to carefully chosen predicates and lemmas
(which are usually tricky to find for the first time and can be useful in other
similar projects). The maximum time to prove a goal was 1min50s.
    We also used smoke-tests to detect unexpected dead code or possible incon-
sistencies in the specification, and manually checked that no unexpected cases
of those were detected.
    As for the 14 lemmas we used, 11 are proved by Coq using our scripts,
and the remaining 3 directly by Alt-Ergo. Their proof takes 6 seconds in our
configuration, with the maximum time to prove a goal being 650ms.


8   Related Work

TPM related safety and security. Various case studies centered around TPM
uses have emerged over the last decade, often focusing on use cases relying on
functionalities of the TPM itself. A recent formal analysis of the key exchange

                                           16
primitive of TPM 2.0 [22] provides a security model to capture TPM protections
on keys and protocols. Authors of [21] propose a security model for the cryp-
tographic support commands in TPM 2.0, proved using the CryptoVerif tool.
A model of TPM commands was used to formalize the session-based HMAC
authorization and encryption mechanisms [18]. Such works focus on the TPM
itself, but to the best of our knowledge, none of the previously published works
aim at verifying the tpm2-tss library or any implementation of the TSS.

Linked lists and recursive data structures. We use logical definitions from [4] to
formalize and manipulate C linked lists as acsl logic lists in our effort, while
another approach [3] relies on a parallel view of a linked list via a companion
ghost array. Both approaches were tested on the linked list module of the Contiki
OS [12], which relies on static allocations and simple structures. In this work we
used a logic list based approach rather than a ghost code based approach follow-
ing the conclusions in [4]. Realized in SPARK, a deductive verification tool for
a subset of the Ada language and also the name of this subset, the approach to
the verification of black-red trees [11] is related to the verification of linked lists
in Frama-C using ghost arrays including the auto-verification aspects [5]. How-
ever, the trees themselves were implemented using arrays as pointers have only
been recently introduced in SPARK [10]. Programs with pointers in SPARK are
based on an ownership policy enforcing non-aliasing which makes their verifica-
tion closer to Rust programs than C programs.

Formal verification for real-life code. Deductive verification on real-life code has
been spreading in the last decades, with various verification case studies where
bugs were often found by annotating and verifying the code [14]. Such studies
include [9], providing feedback on the authors’ experience of using acsl and
Frama-C on a real-world example. Authors of [7] managed a large scale formal
verification of global security properties on the C code of the JavaCard Virtual
Machine. SPARK was used in the verification of a TCP Stack [6]. Authors of [16]
highlight some issues specific to the verification of the Hyper-V hypervisor, and
how they can be solved with VCC, a deductive verification tool for C.


9    Conclusion and Future Work

This paper presents a first case study on formal verification of the tpm2-tss li-
brary, a popular implementation of the TPM Software Stack. Making the bridge
between the TPM and applications, this library is highly critical: to take ad-
vantage of security guarantees of the TPM, its deductive verification is highly
desired. The library code is very complex and challenging for verification tools.
   We have presented our verification results for a subset of 10 functions of the
ESAPI layer of the library that we verified with Frama-C. We have described
current limitations of the verification tool and temporary solutions we used to
address them. We have proved all necessary lemmas (extending those of a pre-
vious case study for linked lists [4]) in Coq using the most recent version of the

                                          17
Frama-C–Coq translation and identified some necessary improvements in han-
dling logic lists. Finally, we identified desired tool improvements to achieve a full
formal verification of the library: support of dynamic allocations and basic acsl
clauses to handle them, a memory model that works at byte level, and clearer
separation of modification statuses of variables between the heap, the stack, and
static segments. The real-life code was slightly simplified for verification, but the
logical behavior was preserved in the verified version. While the current real-life
code cannot be verified without adaptations, we expect that it will become prov-
able as soon as those improvements of the tool are implemented10 .
    This work opens the way towards a full verification of the tpm2-tss library.
Future work includes the verification of a larger subset of functions, including
lower-level layers and operations. Specification and verification of specific secu-
rity properties is another future work direction. Maintaining proofs for changing
versions of tools and axiomatizations is also an interesting research direction. Fi-
nally, combining formally verified modules with modules which undergo a partial
verification (e.g. limited to the absence of runtime errors, or runtime assertion
checking of expected specifications on large test suites) can be another promising
work direction to increase confidence in the security of the library.

Acknowledgment. Part of this work was supported by ANR (grants ANR-22-
CE39-0014, ANR-22-CE25-0018) and French Ministry of Defense via a PhD
grant of Yani Ziani. We thank Allan Blanchard, Laurent Corbin and Loı̈c Cor-
renson for useful discussions, and the anonymous referees for helpful comments.


References

 1. Arthur, W., Challener, D.: A Practical Guide to TPM 2.0: Using the Trusted
    Platform Module in the New Age of Security. Apress, USA, 1st edn. (2015)
 2. Baudin, P., Cuoq, P., Filliâtre, J.C., Marché, C., Monate, B., Moy, Y., Prevosto,
    V.: ACSL: ANSI/ISO C Specification Language, http://frama-c.com/acsl.html
 3. Blanchard, A., Kosmatov, N., Loulergue, F.: Ghosts for Lists: A Critical Mod-
    ule of Contiki Verified in Frama-C. In: Proc. of the 10th NASA Formal Methods
    Symposium (NFM 2018). LNCS, vol. 10811, pp. 37–53. Springer (2018)
 4. Blanchard, A., Kosmatov, N., Loulergue, F.: Logic against ghosts: Comparison of
    two proof approaches for a list module. In: Proc. of the 34th Annual ACM/SIGAPP
    Symposium on Applied Computing, Software Verification and Testing Track (SAC-
    SVT 2019). pp. 2186–2195. ACM (2019)
 5. Blanchard, A., Loulergue, F., Kosmatov, N.: Towards Full Proof Automation in
    Frama-C using Auto-Active Verification. In: Proc. of the 11th NASA Formal Meth-
    ods Symposium (NFM 2019). LNCS, vol. 11460, pp. 88–105. Springer (2019)
 6. Cluzel, G., Georgiou, K., Moy, Y., Zeller, C.: Layered formal verification of a TCP
    stack. In: Proc. of the IEEE Secure Development Conference (SecDev 2021). pp.
    86–93. IEEE (2021)
10
     Detailed discussions of limitations and ongoing extensions of Frama-C can be found
     at https://git.frama-c.com/pub/frama-c/.


                                           18
 7. Djoudi, A., Hána, M., Kosmatov, N.: Formal Verification of a JavaCard Virtual
    Machine with Frama-C. In: Proc. of the 24th International Symposium on Formal
    Methods (FM 2021). LNCS, vol. 13047, pp. 427–444. Springer (2021)
 8. Djoudi, A., Hána, M., Kosmatov, N., Křı́ženecký, M., Ohayon, F., Mouy, P.,
    Fontaine, A., Féliot, D.: A bottom-up formal verification approach for common
    criteria certification: Application to JavaCard virtual machine. In: Proc. of the
    11th European Congress on Embedded Real-Time Systems (ERTS 2022) (Jun
    2022)
 9. Dordowsky, F.: An experimental study using ACSL and Frama-C to formulate and
    verify low-level requirements from a DO-178C compliant avionics project. Elec-
    tronic Proceedings in Theoretical Computer Science 187, 28–41 (2015)
10. Dross, C., Kanig, J.: Recursive data structures in SPARK. In: Proc. of the 32nd
    International Conference on Computer Aided Verification (CAV 2020). LNCS, vol.
    12225, pp. 178–189. Springer (2020)
11. Dross, C., Moy, Y.: Auto-active proof of red-black trees in SPARK. In: Proc. of
    the 9th NASA Formal Methods Symposium (NFM 2017). LNCS, vol. 10227, pp.
    68–83 (2017)
12. Dunkels, A., Grönvall, B., Voigt, T.: Contiki - A lightweight and flexible operating
    system for tiny networked sensors. In: Proc. of the 29th Annual IEEE Conference
    on Local Computer Networks (LCN 2004). pp. 455–462. IEEE Computer Society
    (2004)
13. Filliâtre, J.C., Paskevich, A.: Why3 - where programs meet provers. In: Proc. of
    the 22nd European Symposium on Programming (ESOP 2013). LNCS, vol. 7792,
    pp. 125–128. Springer (2013)
14. Hähnle, R., Huisman, M.: Deductive software verification: From pen-and-paper
    proofs to industrial tools. In: Computing and Software Science – State of the Art
    and Perspectives, LNCS, vol. 10000, pp. 345–373. Springer (2019)
15. Kirchner, F., Kosmatov, N., Prevosto, V., Signoles, J., Yakobowski, B.: Frama-C:
    A software analysis perspective. Formal Asp. Comput. 27(3), 573–609 (2015)
16. Leinenbach, D., Santen, T.: Verifying the microsoft Hyper-V hypervisor with VCC.
    In: Proc. of the Second World Congres on Formal Methods (FM 2009). LNCS, vol.
    5850, pp. 806–809. Springer (2009)
17. Mangano, F., Duquennoy, S., Kosmatov, N.: A memory allocation module of Con-
    tiki formally verified with Frama-C. A case study. In: Proc. of the 11th International
    Conference on Risks and Security of Internet and Systems (CRiSIS 2016). LNCS,
    vol. 10158, pp. 114–120. Springer (2016)
18. Shao, J., Qin, Y., Feng, D.: Formal analysis of HMAC authorisation in the TPM2.0
    specification. IET Inf. Secur. 12(2), 133–140 (2018)
19. The Coq Development Team: The Coq proof assistant. http://coq.inria.fr,
20. Trusted Computing Group: Trusted Platform Module Library Spec-
    ification,    Family    “2.0”,   Level 00,       Revision    01.59     – November.
    https://trustedcomputinggroup.org/work-groups/trusted-platform-module/
    (2019), last accessed: May 2023
21. Wang, W., Qin, Y., Yang, B., Zhang, Y., Feng, D.: Automated security proof of
    cryptographic support commands in TPM 2.0. In: Proc. of the 18th International
    Conference on Information and Communications Security (ICICS 2016). LNCS,
    vol. 9977, pp. 431–441. Springer (2016)
22. Zhang, Q., Zhao, S.: A comprehensive formal security analysis and revision of the
    two-phase key exchange primitive of TPM 2.0. Comput. Networks 179 (2020)



                                           19
     A       Appendix: Supplementary Material
     This appendix presents the complete illustrative example.

     A.1       Complete Illustrative Example
     Figures 10, 11, 12, 13, 14, 15, 16, 17 give the complete version of the illustrative
     example (presented in Fig. 1–6 in the paper), annotated in acsl. It was proved
     with Frama-C 26.1, Why3 1.5.1, Alt-Ergo 2.4.3 and CVC4 1.8. The command
     used to run the proof is given at the end of the file.
        Figure 9 provides the definition of the lemmas required to perform the proof.
     The same lemmas are used for the illustrative example and the proved subset of
     the real-life code. All necessary lemmas were proved with Coq 8.16.1 (but other
     recent versions should also work). The Coq proof scripts and the instructions
     how to run the proof are available in the companion artifact.

1    / * * * * * * * * * * * * * * * * * * * * * * l e m m a s _ n o d e _ t. h * * * * * * * * * * * * * * * * * * * * * * /
2    /* @
3        lemma l i n k e d _ l l _ i n _ v a l i d{ L }: ∀ NODE_T * bl , * el , \list<NODE_T *> ll ;
4            l i n k e d _ l l( bl , el , ll ) ⇒ ∀ Z n ; 0 ≤ n < \length ( ll ) ⇒
5                \valid ( \nth ( ll , n ));
6        lemma p t r _ s e p _ f r o m _ n i l{ L }: ∀ NODE_T * l ;
7            p t r _ s e p _ f r o m _ l i s t(l , \Nil );
8        lemma p t r _ s e p _ f r o m _ c o n s{ L }: ∀ NODE_T *e , * hd , \list<NODE_T *> l ;
9            p t r _ s e p _ f r o m _ l i s t(e , \Cons ( hd , l ))⇐⇒
10               ( \ s e p a r a t e d( hd , e ) ∧ p t r _ s e p _ f r o m _ l i s t(e , l ));
11       lemma d p t r _ s e p _ f r o m _ n i l{ L }:
12          ∀ NODE_T ** l ; d p t r _ s e p _ f r o m _ l i s t(l , \Nil );
13       lemma l i n k e d _ l l _ a l l _ s e p a r a t e d{ L }: ∀ NODE_T * bl , * el , \list<NODE_T *> ll ;
14           l i n k e d _ l l( bl , el , ll ) ⇒ a l l _ s e p _ i n _ l i s t( ll );
15       lemma l i n k e d _ l l _ u n c h a n g e d _ l l{ L1 , L2 }: ∀ NODE_T * bl , * el , \list<NODE_T *> ll ;
16           l i n k e d _ l l{ L1 }( bl , el , ll ) ⇒
17               u n c h a n g e d _ l l{ L1 , L2 }( ll ) ⇒ l i n k e d _ l l{ L2 }( bl , el , ll );
18       lemma l i n k e d _ l l _ t o _ l l{ L }: ∀ NODE_T * bl , * el , \list<NODE_T *> ll ;
19           l i n k e d _ l l( bl , el , ll ) ⇒ ll == to_ll ( bl , el );
20       lemma t o _ l l _ s p l i t{ L }: ∀ NODE_T * bl , * el , * sep , \list<NODE_T *> ll ;
21           ll 6= \Nil ⇒ l i n k e d _ l l( bl , el , ll ) ⇒ ll == to_ll ( bl , el ) ⇒
22               in_list ( sep , ll ) ⇒ ll == ( to_ll ( bl , sep ) ^ to_ll ( sep , el ));
23       lemma i n _ l i s t _ i n _ s u b l i s t: ∀ NODE_T * e , \list<NODE_T *> rl , ll , l ;
24           ( rl ^ ll ) == l ⇒ ( in_list (e , l )⇐⇒( in_list (e , rl ) ∨ in_list (e , ll )));
25       lemma l i n k e d _ l l _ e n d{ L }: ∀ NODE_T * bl , * el , \list<NODE_T *> ll ;
26           ll 6= \Nil ⇒ l i n k e d _ l l( bl , el , ll ) ⇒
27               \nth ( ll , \length ( ll ) -1) ->next == el ;
28       lemma l i n k e d _ l l _ e n d _ s e p a r a t e d{ L }: ∀ NODE_T * bl , * el , \list<NODE_T *> ll ;
29           l i n k e d _ l l( bl , el , ll ) ⇒ p t r _ s e p _ f r o m _ l i s t( el , ll );
30       lemma l i n k e d _ l l _ e n d _ n o t _ i n{ L }: ∀ NODE_T * bl , * el , \list<NODE_T *> ll ;
31           l i n k e d _ l l( bl , el , ll ) ⇒ ! in_list ( el , ll );
32   // new l e m m a s wrt . p r e v i o u s work on l i n k e d lists [ B l a n c h a r d et al . , SAC ’19]
33       lemma i n _ n e x t _ n o t _ b o u n d _ i n{ L }: ∀ NODE_T * bl , * el , * item , \list<NODE_T *> ll ;
34           l i n k e d _ l l( bl , el , ll ) ⇒ in_list ( item , ll ) ⇒ item ->next 6= el ⇒
35               in_list ( item ->next , ll );
36       lemma l i n k e d _ l l _ s p l i t _ v a r i a n t{ L }:
37          ∀ NODE_T * bl , * bound , * el , \list<NODE_T *> l1 , l2 ;
38           l i n k e d _ l l( bl , el , l1 ^ l2 ) ⇒ l2 6= \Nil ⇒
39           bound == \nth ( l1 ^ l2 , \length ( l1 ^ l2 ) - \length ( l2 )) ⇒
40               l i n k e d _ l l( bl , bound , l1 ) ∧ l i n k e d _ l l( bound , el , l2 );
41   */

     Fig. 9. Lemmas used to prove the illustrative example and the subset of real-life code.




                                                               20
1    # include <stdint . h>                            // for uint types d e f i n i t i o n s
2    # include <string . h>                            // for s i z e _ t d e f i n i t i o n
3    # include <byteswap . h>                          // used in m a r s h a l
4    # define H O S T _ T O _ B E _ 3 2( value ) _ _ b s w a p _ 3 2 ( value ) // swap e n d i a n n e s s
5    typedef struct T P M 2 B _ N A M E { uint16_t size ; uint8_t name [68];} T P M 2 B _ N A M E;
6    typedef struct {
7        uint32_t                    handle ;          // h a n d l e used by TPM
8        TPM2B_NAME                      name ;        // TPM name of the o b j e c t
9        uint32_t                    rsrcType ; // s e l e c t o r for r e s o u r c e type
10   } RESOURCE ;
11   typedef struct NODE_T {
12       uint32_t                    handle ;          // the h a n d l e used as r e f e r e n c e
13       RESOURCE                    rsrc ;            // the m e t a d a t a for this rsrc
14       struct NODE_T *                     next ; // next node in the list
15   } NODE_T ; // l i n k e d list of r e s o u r c e
16   /* @
17       p r e d i c a t e z e r o _ t p m 2 b _ n a m e( T P M 2 B _ N A M E t p m 2 b _ n a m e) =
18           t p m 2 b _ n a m e. size == 0 ∧ ∀ int i ; 0 ≤ i < 68 ⇒ t p m 2 b _ n a m e. name [ i ] == 0;
19       p r e d i c a t e z e r o _ r e s o u r c e( RESOURCE rsrc ) =
20           rsrc . handle == 0 ∧ z e r o _ t p m 2 b _ n a m e( rsrc . name ) ∧ rsrc . rsrcType == 0;
21       p r e d i c a t e z e r o _ r s r c _ n o d e _ t( NODE_T node ) =
22           node . handle == 0 ∧ z e r o _ r e s o u r c e( node . rsrc ) ∧ node . next == \null ;
23   */
24   / * * * * * * * * * * * * * * Logic lists and linked lists d e f i n i t i o n s * * * * * * * * * * * * * /
25   /* @
26       p r e d i c a t e p t r _ s e p _ f r o m _ l i s t{ L }( NODE_T * e , \list<NODE_T *> ll ) =
27          ∀ Z n ; 0 ≤ n < \length ( ll ) ⇒ \ s e p a r a t e d(e , \nth ( ll , n ));
28       p r e d i c a t e d p t r _ s e p _ f r o m _ l i s t{ L }( NODE_T ** e , \list<NODE_T *> ll ) =
29          ∀ Z n ; 0 ≤ n < \length ( ll ) ⇒ \ s e p a r a t e d(e , \nth ( ll , n ));
30       p r e d i c a t e in_list { L }( NODE_T * e , \list<NODE_T *> ll ) =
31          ∃ Z n ; 0 ≤ n < \length ( ll ) ∧ \nth ( ll , n ) == e ;
32       p r e d i c a t e i n _ l i s t _ h a n d l e{ L }( uint32_t out_handle , \list<NODE_T *> ll ) =
33          ∃ Z n ; 0 ≤ n < \length ( ll ) ∧ \nth ( ll , n ) ->handle == o u t _ h a n d l e;
34       i n d u c t i v e l i n k e d _ l l{ L }( NODE_T * bl , NODE_T * el , \list<NODE_T *> ll ) {
35           case l i n k e d _ l l _ n i l{ L }: ∀ NODE_T * el ; l i n k e d _ l l{ L }( el , el , \Nil );
36           case l i n k e d _ l l _ c o n s{ L }: ∀ NODE_T * bl , * el , \list<NODE_T *> tail ;
37               ( \ s e p a r a t e d( bl , el ) ∧ \valid ( bl ) ∧ l i n k e d _ l l{ L }( bl ->next , el , tail ) ∧
38               p t r _ s e p _ f r o m _ l i s t( bl , tail )) ⇒
39                   l i n k e d _ l l{ L }( bl , el , \Cons ( bl , tail ));
40       }
41       p r e d i c a t e u n c h a n g e d _ l l{ L1 , L2 }( \list<NODE_T *> ll ) =
42          ∀ Z n ; 0 ≤ n < \length ( ll ) ⇒
43               \valid { L1 }( \nth ( ll , n )) ∧ \valid { L2 }( \nth ( ll , n )) ∧
44               \at (( \nth ( ll , n )) ->next , L1 ) == \at (( \nth ( ll , n )) ->next , L2 );
45       p r e d i c a t e a l l _ s e p _ i n _ l i s t( \list<NODE_T *> ll ) =
46          ∀ Z n1 , n2 ; (0 ≤ n1 < \length ( ll ) ∧ 0 ≤ n2 < \length ( ll ) ∧ n1 6= n2 ) ⇒
47                   \ s e p a r a t e d( \nth ( ll , n1 ) , \nth ( ll , n2 ));
48       axiomatic Node_To_ll {
49           logic \list<NODE_T *> to_ll { L }( NODE_T * beg , NODE_T * end )
50               reads { node ->next | NODE_T * node ; \valid ( node ) ∧
51                                                       in_list ( node , to_ll ( beg , end ))};
52           axiom t o _ l l _ n i l{ L }: ∀ NODE_T * node ; to_ll { L }( node , node ) == \Nil ;
53           axiom t o _ l l _ c o n s{ L }: ∀ NODE_T * beg , * end ;
54               ( \ s e p a r a t e d( beg , end ) ∧ \valid { L }( beg ) ∧
55               p t r _ s e p _ f r o m _ l i s t{ L }( beg , to_ll { L }( beg ->next , end ))) ⇒
56                   to_ll { L }( beg , end ) == \Cons ( beg , to_ll { L }( beg ->next , end ));
57       }
58   */
59
60   # include " l e m m a s _ n o d e _ t. h "

     Fig. 10. Illustrative provable example of the adjusted tpm2-tss list manipulation code,
     part 1/8.




                                                             21
61
62    # define _ a l l o c _ m a x 100
63    static NODE_T _ r s r c _ b a n k[ _ a l l o c _ m a x]; // bank used by the s t a t i c a l l o c a t o r
64    static int _ a l l o c _ i d x = 0; // index of the next rsrc node to be a l l o c a t e d
65    /* @
66       p r e d i c a t e v a l i d _ r s r c _ m e m _ b a n k{ L } = 0 ≤ _ a l l o c _ i d x ≤ _ a l l o c _ m a x;
67       p r e d i c a t e l i s t _ s e p _ f r o m _ a l l o c a b l e s{ L }( \list<NODE_T *> ll ) =
68          ∀ int i ; _ a l l o c _ i d x ≤ i < _ a l l o c _ m a x ⇒
69                                                 p t r _ s e p _ f r o m _ l i s t{ L }(& _ r s r c _ b a n k[ i ] , ll );
70       p r e d i c a t e p t r _ s e p _ f r o m _ a l l o c a b l e s{ L }( NODE_T * node ) =
71          ∀ int i ; _ a l l o c _ i d x ≤ i < _ a l l o c _ m a x ⇒ \ s e p a r a t e d( node , & _ r s r c _ b a n k[ i ]);
72       p r e d i c a t e d p t r _ s e p _ f r o m _ a l l o c a b l e s{ L }( NODE_T ** p_node ) =
73          ∀ int i ; _ a l l o c _ i d x ≤ i < _ a l l o c _ m a x ⇒ \ s e p a r a t e d( p_node , & _ r s r c _ b a n k[ i ]);
74    */
75    /***************************************************************************/
76    /* @
77       requires v a l i d _ r s r c _ m e m _ b a n k;
78       assigns _alloc_idx , _ r s r c _ b a n k[ \old ( _ a l l o c _ i d x)];
79       ensures v a l i d _ r s r c _ m e m _ b a n k;
80
81       behavior n o t _ a l l o c a b l e:
82         assumes _ a l l o c _ i d x == _ a l l o c _ m a x;
83
84           ensures_ a l l o c _ i d x == _ a l l o c _ m a x;
85           ensures\result == NULL ;
86           ensures_ r s r c _ b a n k == \old ( _ r s r c _ b a n k);
87                 ∀ int i ; 0 ≤ i < _ a l l o c _ m a x ⇒
             ensures
88                      _ r s r c _ b a n k[ i ] == \old ( _ r s r c _ b a n k[ i ]);
89       behavior a l l o c a b l e:
90         assumes 0 ≤ _ a l l o c _ i d x < _ a l l o c _ m a x;
91
92           ensures_ a l l o c _ i d x == \old ( _ a l l o c _ i d x) + 1;
93           ensures\result == &( _ r s r c _ b a n k[ _ a l l o c _ i d x - 1]);
94           ensures\valid ( \result );
95           ensuresz e r o _ r s r c _ n o d e _ t( *( \result ) );
96                 ∀ int i ; 0 ≤ i < _ a l l o c _ m a x ∧ i 6= \old ( _ a l l o c _ i d x) ⇒
             ensures
97                  _ r s r c _ b a n k[ i ] == \old ( _ r s r c _ b a n k[ i ]);
98       disjoint b e h a v i o r s; complete b e h a v i o r s;
99    */
100   NODE_T * c a l l o c _ N O D E _ T()
101   {
102      static const RESOURCE e m p t y _ R E S O U R C E;
103      if ( _ a l l o c _ i d x < _ a l l o c _ m a x) {
104         _ r s r c _ b a n k[ _ a l l o c _ i d x]. handle = ( uint32_t ) 0;
105         _ r s r c _ b a n k[ _ a l l o c _ i d x]. rsrc = e m p t y _ R E S O U R C E;
106         _ r s r c _ b a n k[ _ a l l o c _ i d x]. next = NULL ;
107         _ a l l o c _ i d x += 1;
108         return & _ r s r c _ b a n k[ _ a l l o c _ i d x - 1];
109      }
110      return NULL ;
111   }

      Fig. 11. Illustrative provable example of the adjusted tpm2-tss list manipulation code,
      part 2/8.




                                                                      22
112
113   typedef struct CONTEXT {
114      int p l a c e h o l d e r _ i n t;
115      NODE_T * r s r c _ l i s t;
116   } CONTEXT ;
117   /* @
118      p r e d i c a t e c t x _ s e p _ f r o m _ l i s t( CONTEXT * ctx , \list<NODE_T *> ll ) =
119         ∀ Z i ; 0 ≤ i < \length ( ll ) ⇒ \ s e p a r a t e d( \nth ( ll , i ) , ctx );
120      p r e d i c a t e c t x _ s e p _ f r o m _ a l l o c a b l e s( CONTEXT * ctx ) =
121         ∀ int i ; _ a l l o c _ i d x ≤ i < _ a l l o c _ m a x ⇒ \ s e p a r a t e d( ctx , & _ r s r c _ b a n k[ i ]);
122
123        p r e d i c a t e f r e s h n e s s( CONTEXT * ctx , NODE_T ** node ) =
124            c t x _ s e p _ f r o m _ a l l o c a b l e s( ctx )
125           ∧ l i s t _ s e p _ f r o m _ a l l o c a b l e s( to_ll ( ctx ->rsrc_list , NULL ))
126           ∧ p t r _ s e p _ f r o m _ a l l o c a b l e s( ctx ->r s r c _ l i s t)
127           ∧ p t r _ s e p _ f r o m _ a l l o c a b l e s (* node )
128           ∧ d p t r _ s e p _ f r o m _ a l l o c a b l e s( node );
129
130        p r e d i c a t e s e p _ f r o m _ l i s t{ L }( CONTEXT * ctx , NODE_T ** node ) =
131            c t x _ s e p _ f r o m _ l i s t( ctx , to_ll { L }( ctx ->rsrc_list , NULL ))
132           ∧ d p t r _ s e p _ f r o m _ l i s t( node , to_ll { L }( ctx ->rsrc_list , NULL ));
133   */
134
135   /* @
136      requires v a l i d _ r s r c _ m e m _ b a n k ∧ f r e s h n e s s( ctx , out_node );
137      requires \valid ( ctx );
138      requires ctx ->r s r c _ l i s t 6= NULL ⇒ \valid ( ctx ->r s r c _ l i s t);
139      requires l i n k e d _ l l( ctx ->rsrc_list , NULL , to_ll ( ctx ->rsrc_list , NULL ));
140      requires s e p _ f r o m _ l i s t( ctx , out_node );
141      requires p t r _ s e p _ f r o m _ l i s t (* out_node , to_ll ( ctx ->rsrc_list , NULL ));
142      requires !( i n _ l i s t _ h a n d l e( esys_handle , to_ll ( ctx ->rsrc_list , NULL )));
143      requires \valid ( out_node ) ∧ \ s e p a r a t e d( ctx , out_node );
144      requires * out_node 6= NULL ⇒ \valid (* out_node ) ∧ (* out_node ) ->next == NULL ;
145      assigns _alloc_idx , _ r s r c _ b a n k[ _ a l l o c _ i d x] , ctx ->rsrc_list , * out_node ;
146      ensures v a l i d _ r s r c _ m e m _ b a n k ∧ f r e s h n e s s( ctx , out_node );
147      ensures s e p _ f r o m _ l i s t( ctx , out_node );
148      ensures u n c h a n g e d _ l l{ Pre , Post }( to_ll { Pre }( \old ( ctx ->r s r c _ l i s t) , NULL ));
149      ensures \result \in {1610 , 833};
150
151        behavior n o t _ a l l o c a b l e:
152          assumes _ a l l o c _ i d x == _ a l l o c _ m a x;
153
154          ensures _ a l l o c _ i d x == _ a l l o c _ m a x;
155          ensures \valid ( ctx );
156          ensures !( i n _ l i s t _ h a n d l e( esys_handle , to_ll ( ctx ->rsrc_list , NULL )));
157          ensures ctx ->r s r c _ l i s t == \old ( ctx ->r s r c _ l i s t);
158          ensures * out_node == \old (* out_node );
159          ensures u n c h a n g e d _ l l{ Pre , Post }( to_ll ( ctx ->rsrc_list , NULL ));
160          ensures \result == 833;
161        behavior a l l o c a t e d:
162          assumes 0 ≤ _ a l l o c _ i d x < _ a l l o c _ m a x;
163
164          ensures _ a l l o c _ i d x == \old ( _ a l l o c _ i d x) + 1;
165          ensures i n _ l i s t _ h a n d l e( esys_handle , to_ll ( ctx ->rsrc_list , NULL ));
166          ensures \valid ( ctx ->r s r c _ l i s t) ∧ * out_node == ctx ->r s r c _ l i s t;
167          ensures ctx ->r s r c _ l i s t == & _ r s r c _ b a n k[ _ a l l o c _ i d x - 1];
168          ensures ctx ->rsrc_list ->handle == e s y s _ h a n d l e;
169          ensures ctx ->rsrc_list ->next == \old ( ctx ->r s r c _ l i s t);
170          ensures l i n k e d _ l l( ctx ->rsrc_list , NULL , to_ll ( ctx ->rsrc_list , NULL ));
171          ensures u n c h a n g e d _ l l{ Pre , Post }( to_ll { Pre }( \old ( ctx ->r s r c _ l i s t) , NULL ));
172          ensures \old ( ctx ->r s r c _ l i s t) 6= NULL ⇒
173              \nth ( to_ll ( ctx ->rsrc_list , NULL ) , 1) == \old ( ctx ->r s r c _ l i s t);
174          ensures \result == 1610;
175        disjoint b e h a v i o r s; complete b e h a v i o r s;
176   */

      Fig. 12. Illustrative provable example of the adjusted tpm2-tss list manipulation code,
      part 3/8.


                                                                   23
177   int c r e a t e N o d e( CONTEXT * ctx , uint32_t esys_handle , NODE_T ** out_node ){
178   // @ ghost p r e _ c a l l o c:;
179      // @ g h o s t int if_id = 0;
180      /* @ assert \ s e p a r a t e d( out_node , & _ r s r c _ b a n k[ _ a l l o c _ i d x ]);*/
181      /* @ assert \ s e p a r a t e d( ctx ->rsrc_list , & _ r s r c _ b a n k[ _ a l l o c _ i d x ]); */
182      // N O D E _ T * n e w _ h e a d = c a l l o c(1 , s i z e o f( N O D E _ T)); /* l i b r a r y v e r s i o n*/
183      /* @ assert l i s t _ s e p _ f r o m _ a l l o c a b l e s( to_ll ( ctx ->rsrc_list , NULL )); */
184      /* @ assert p t r _ s e p _ f r o m _ l i s t(& _ r s r c _ b a n k[ _ a l l o c _ i d x] , to_ll { p r e _ c a l l o c}( ctx ->rsrc_list , NULL )); */
185      /* @ assert p t r _ s e p _ f r o m _ l i s t(& _ r s r c _ b a n k[ _ a l l o c _ i d x] , to_ll ( ctx ->rsrc_list , NULL )); */
186      NODE_T * new_head = c a l l o c _ N O D E _ T();
187      /* @ assert u n c h a n g e d _ l l{ pre_calloc , Here }(
188                         to_ll { p r e _ c a l l o c}( ctx ->rsrc_list , NULL )); */
189   // @ ghost p o s t _ c a l l o c:;
190      if ( new_head == NULL ){ return 833;}
191      /* @ assert \valid ( new_head ) ∧ new_head ->next == NULL ; */
192      /* @ assert p t r _ s e p _ f r o m _ l i s t( new_head , to_ll ( ctx ->rsrc_list , NULL )); */
193      /* @ assert u n c h a n g e d _ l l{ Pre , Here }( to_ll { Here }( ctx ->rsrc_list , NULL ));*/
194   // @ ghost p r e _ i f:;
195      if ( ctx ->r s r c _ l i s t == NULL ) {
196         /* The first object of the list will be added */
197         ctx ->r s r c _ l i s t = new_head ;
198         /* @ assert u n c h a n g e d _ l l{ pre_if , Here }( to_ll ( new_head , NULL ));*/
199         /* @ assert to_ll ( new_head , NULL ) == [| new_head |]; */
200         /* @ assert \ s e p a r a t e d( new_head , new_head ->next );*/
201         new_head ->next = NULL ;
202         /* @ assert to_ll ( new_head , NULL ) == [| new_head |]; */
203      }
204      else {
205         /* The new object will become the first element of the list */
206         /* @ assert d p t r _ s e p _ f r o m _ l i s t(& ctx ->rsrc_list ,
207                                                            to_ll ( ctx ->rsrc_list , NULL ));*/
208         new_head ->next = ctx ->r s r c _ l i s t;
209   // @ ghost p o s t _ a s s i g n:;
210         /* @ assert u n c h a n g e d _ l l{ pre_if , Here }(
211                                                   to_ll { pre_if }( ctx ->rsrc_list , NULL ));*/
212         /* @ assert to_ll ( new_head , NULL ) ==
213                 ([| new_head |] ^ to_ll ( \at ( ctx ->rsrc_list , pre_if ) , NULL ));*/
214         /* @ assert d p t r _ s e p _ f r o m _ l i s t(& ctx ->rsrc_list ,
215                                                            to_ll ( new_head , NULL ));*/
216         ctx ->r s r c _ l i s t = new_head ;
217         /* @ assert u n c h a n g e d _ l l{ post_assign , Here }(
218                                                   to_ll { p o s t _ a s s i g n}( new_head , NULL ));*/
219         /* @ assert ctx ->rsrc_list ->next == \at ( ctx ->rsrc_list , Pre );*/
220         /* @ assert to_ll ( ctx ->rsrc_list , NULL ) ==
221                 ([| new_head |] ^ to_ll { Pre }( \at ( ctx ->rsrc_list , Pre ) , NULL ));*/
222         /* @ assert ctx ->r s r c _ l i s t == \nth ( to_ll ( ctx ->rsrc_list , NULL ) , 0);*/
223      }
224      // @ ghost p o s t _ a d d:;
225      /* @ assert ctx ->r s r c _ l i s t == \nth ( to_ll ( ctx ->rsrc_list , NULL ) , 0);*/
226      /* @ assert c t x _ s e p _ f r o m _ l i s t( ctx , to_ll ( ctx ->rsrc_list , NULL ));*/
227      /* @ assert ctx ->r s r c _ l i s t == new_head ;*/
228      /* @ assert u n c h a n g e d _ l l{ Pre , Here }( to_ll { Pre }( \at ( ctx ->rsrc_list , Pre ) , NULL ));*/
229      /* @ assert to_ll ( new_head , NULL ) ==
230                         ([| new_head |] ^ to_ll { Pre }( \at ( ctx ->rsrc_list , Pre ) , NULL ));*/
231      /* @ assert d p t r _ s e p _ f r o m _ l i s t( out_node , to_ll ( new_head , NULL ));*/
232      * out_node = new_head ;
233      /* @ assert u n c h a n g e d _ l l{ post_add , Here }( to_ll { post_add }( new_head , NULL ));*/
234      /* @ assert ctx ->r s r c _ l i s t == \nth ( to_ll ( ctx ->rsrc_list , NULL ) , 0);*/
235      new_head ->handle = e s y s _ h a n d l e;
236      /* @ assert \nth ( to_ll ( ctx ->rsrc_list , NULL ) , 0) ->handle == e s y s _ h a n d l e;*/
237      /* @ assert i n _ l i s t _ h a n d l e( esys_handle , to_ll ( ctx ->rsrc_list , NULL ));*/
238      /* @ assert l i s t _ s e p _ f r o m _ a l l o c a b l e s( to_ll ( ctx ->rsrc_list , NULL )); */
239      /* @ assert u n c h a n g e d _ l l{ Pre , Here }( to_ll { Pre }( \at ( ctx ->rsrc_list , Pre ) , NULL ));*/
240      return 1610;
241   }

      Fig. 13. Illustrative provable example of the adjusted tpm2-tss list manipulation code,
      part 4/8.


                                                                24
243   /* @
244      requires \valid ( o u t _ h a n d l e);
245      assigns * o u t _ h a n d l e;
246      ensures \result \in {0 , 12};
247      ensures * o u t _ h a n d l e \in { esys_handle , 0 x4000000A , 0 x4000000B ,
248                                       0 x 4 0 0 0 0 1 1 0 + ( e s y s _ h a n d l e - 0 x120U ) , \old (* o u t _ h a n d l e)};
249      behavior o k _ h a n d l e:
250         assumes e s y s _ h a n d l e ≤ 31 U ∨ 0 x120U ≤ e s y s _ h a n d l e ≤ 0 x12FU
251                  ∨ e s y s _ h a n d l e \in {0 x10AU , 0 x10BU };
252         ensures \result == 0;
253      behavior w r o n g _ h a n d l e:
254         assumes e s y s _ h a n d l e > 31 U
255                  ∧ ( e s y s _ h a n d l e < 0 x120U ∨ e s y s _ h a n d l e > 0 x12FU );
256         assumes !( e s y s _ h a n d l e \in {0 x10AU , 0 x10BU });
257         ensures * o u t _ h a n d l e == \old (* o u t _ h a n d l e);
258         ensures \result == 12;
259      disjoint b e h a v i o r s; complete b e h a v i o r s;
260   */
261   int i e s y s _ h a n d l e _ t o _ t p m _ h a n d l e( uint32_t esys_handle , uint32_t * o u t _ h a n d l e)
262   {
263      if ( e s y s _ h a n d l e ≤ 31 U ) {* o u t _ h a n d l e = ( uint32_t ) e s y s _ h a n d l e; return 0;}
264      if ( e s y s _ h a n d l e == 0 x10AU ){* o u t _ h a n d l e = 0 x 4 0 0 0 0 0 0 A; return 0;}
265      if ( e s y s _ h a n d l e == 0 x10BU ){* o u t _ h a n d l e = 0 x 4 0 0 0 0 0 0 B; return 0;}
266      if ( e s y s _ h a n d l e ≥ 0 x120U ∧ e s y s _ h a n d l e ≤ 0 x12FU )
267        {* o u t _ h a n d l e = 0 x 4 0 0 0 0 1 1 0 + ( e s y s _ h a n d l e - 0 x120U ); return 0;}
268      return 12;
269   }
270
271   /* @
272      requires \valid ( src ) ∧ \valid ( dest + (0 .. sizeof (* src ) -1));
273      requires \ s e p a r a t e d( dest +(0.. sizeof (* src ) -1) , src );
274
275      assigns dest [0 .. sizeof (* src ) -1];
276
277      ensures \valid ( src );
278      ensures \valid ( dest + (0 .. sizeof (* src ) -1));
279   */
280   void m e m c p y _ c u s t o m( uint8_t * dest , uint32_t * src ) {
281      dest [3] = ( uint8_t )(* src & 0 xFF );
282      dest [2] = ( uint8_t )((* src >> 8) & 0 xFF );
283      dest [1] = ( uint8_t )((* src >> 16) & 0 xFF );
284      dest [0] = ( uint8_t )((* src >> 24) & 0 xFF );
285   }
286
287   /* @
288      requires       \valid ( offset ) ∧ 0 ≤ * offset ≤ U I N T 8 _ M A X - sizeof ( in );
289      requires       b u f f _ s i z e > 0 ∧ \valid (& buff [0] + (0 .. b u f f _ s i z e - 1));
290      requires       * offset ≤ b u f f _ s i z e ∧ sizeof ( in ) + * offset ≤ b u f f _ s i z e;
291      requires       \ s e p a r a t e d( offset , buff );
292
293      assigns * offset , (& buff [* offset ])[0.. sizeof ( in ) - 1];
294
295      ensures * offset == \old (* offset ) + sizeof ( in );
296      ensures \result == 0;
297   */
298   int u i n t 3 2 _ M a r s h a l( uint32_t in , uint8_t buff [] , size_t buff_size , size_t * offset ){
299      size_t l o c a l _ o f f s e t = 0;
300      if ( offset 6= NULL ){ l o c a l _ o f f s e t = * offset ;}
301      in = H O S T _ T O _ B E _ 3 2( in );
302      // m e m c p y(& buff [ l o c a l _ o f f s e t] , & in , s i z e o f ( in ));
303      m e m c p y _ c u s t o m(& buff [ l o c a l _ o f f s e t] , & in );
304      if ( offset 6= NULL ){* offset = l o c a l _ o f f s e t + sizeof ( in );}
305      return 0;
306   }

      Fig. 14. Illustrative provable example of the adjusted tpm2-tss list manipulation code,
      part 5/8.


                                                                    25
307
308
309   /* @
310      requires v a l i d _ r s r c _ m e m _ b a n k{ Pre } ∧ f r e s h n e s s( ctx , node );
311      requires \valid ( ctx );
312      requires ctx ->r s r c _ l i s t 6= \null ⇒ \valid ( ctx ->r s r c _ l i s t);
313      requires l i n k e d _ l l( ctx ->rsrc_list , NULL , to_ll ( ctx ->rsrc_list , NULL ));
314      requires 0 ≤ \length ( to_ll ( ctx ->rsrc_list , NULL )) < INT_MAX ;
315      requires \valid ( node );
316      requires * node 6= \null ⇒( \valid (* node ) ∧ (* node ) ->next == \null );
317      requires s e p _ f r o m _ l i s t( ctx , node ) ∧ \ s e p a r a t e d( node , ctx );
318      requires p t r _ s e p _ f r o m _ l i s t (* node , to_ll ( ctx ->rsrc_list , NULL ));
319      assigns _alloc_idx , _ r s r c _ b a n k[ _ a l l o c _ i d x] , ctx ->r s r c _ l i s t;
320      assigns * node , (& ctx ->rsrc_list ->rsrc . name . name [0])[0];
321      ensures v a l i d _ r s r c _ m e m _ b a n k ∧ f r e s h n e s s( ctx , node );
322      ensures \ s e p a r a t e d( node , ctx );
323      ensures \result \in {616 , 833 , 1611 , 12};
324
325        behavior h a n d l e _ i n _ l i s t:
326          assumes i n _ l i s t _ h a n d l e( rsrc_handle , to_ll ( ctx ->rsrc_list , NULL ));
327
328          ensures _ a l l o c _ i d x == \old ( _ a l l o c _ i d x);
329          ensures ctx ->r s r c _ l i s t == \old ( ctx ->r s r c _ l i s t);
330          ensures in_list (* node , to_ll ( ctx ->rsrc_list , NULL )) ∧ * node 6= NULL ;
331          ensures (* node ) ->handle == r s r c _ h a n d l e ∧ s e p _ f r o m _ l i s t( ctx , node );
332          ensures u n c h a n g e d _ l l{ Pre , Post }( to_ll ( ctx ->rsrc_list , NULL ));
333          ensures \result == 616;
334        behavior h a n d l e _ n o t _ c o n v e r t e d:
335          assumes !( i n _ l i s t _ h a n d l e( rsrc_handle , to_ll ( ctx ->rsrc_list , NULL )));
336          assumes r s r c _ h a n d l e > 31 U ∧ ! ( r s r c _ h a n d l e \in {0 x10AU , 0 x10BU } );
337          assumes r s r c _ h a n d l e < 0 x120U ∨ r s r c _ h a n d l e > 0 x12FU ;
338
339          ensures u n c h a n g e d _ l l{ Pre , Post }( to_ll ( ctx ->rsrc_list , NULL ));
340          ensures p t r _ s e p _ f r o m _ l i s t (* node , to_ll ( ctx ->rsrc_list , NULL ));
341          ensures s e p _ f r o m _ l i s t( ctx , node ) ∧ * node == \old (* node );
342          ensures \result == 12;
343        behavior h a n d l e _ n o t _ i n _ l i s t _ a n d _ n o d e _ n o t _ a l l o c a b l e:
344          assumes !( i n _ l i s t _ h a n d l e( rsrc_handle , to_ll ( ctx ->rsrc_list , NULL )));
345          assumes r s r c _ h a n d l e ≤ 31 U ∨ ( r s r c _ h a n d l e \in {0 x10AU , 0 x10BU })
346                  ∨ (0 x120U ≤ r s r c _ h a n d l e ≤ 0 x12FU );
347          assumes _ a l l o c _ i d x == _ a l l o c _ m a x;
348
349          ensures _ a l l o c _ i d x == _ a l l o c _ m a x;
350          ensures u n c h a n g e d _ l l{ Pre , Post }( to_ll { Pre }( ctx ->rsrc_list , NULL ));
351          ensures * node == \old (* node ) ∧ ctx ->r s r c _ l i s t == \old ( ctx ->r s r c _ l i s t);
352          ensures p t r _ s e p _ f r o m _ l i s t (* node , to_ll { Pre }( ctx ->rsrc_list , NULL ));
353          ensures s e p _ f r o m _ l i s t{ Pre }( ctx , node ); // has to stay in b e h a v i o r
354          ensures \result == 833;
355        behavior h a n d l e _ n o t _ i n _ l i s t _ a n d _ n o d e _ a l l o c a t e d:
356          assumes !( i n _ l i s t _ h a n d l e( rsrc_handle , to_ll ( ctx ->rsrc_list , NULL )));
357          assumes r s r c _ h a n d l e ≤ 31 U ∨ ( r s r c _ h a n d l e \in {0 x10AU , 0 x10BU })
358                  ∨ (0 x120U ≤ r s r c _ h a n d l e ≤ 0 x12FU );
359          assumes 0 ≤ _ a l l o c _ i d x < _ a l l o c _ m a x;
360
361          ensures i n _ l i s t _ h a n d l e( rsrc_handle , to_ll ( ctx ->rsrc_list , NULL ));
362          ensures (* ctx ->r s r c _ l i s t). handle == r s r c _ h a n d l e;
363          ensures _ a l l o c _ i d x == \old ( _ a l l o c _ i d x) + 1;
364          ensures \valid ( ctx ->r s r c _ l i s t) ∧ * node == ctx ->r s r c _ l i s t;
365          ensures ctx ->r s r c _ l i s t 6= \old ( ctx ->r s r c _ l i s t);
366          ensures ctx ->rsrc_list ->next == \old ( ctx ->r s r c _ l i s t);
367          ensures to_ll ( ctx ->rsrc_list , NULL )
368              == ([| ctx ->r s r c _ l i s t|] ^ to_ll { Pre }( \old ( ctx ->r s r c _ l i s t) , NULL ) );
369          ensures \old ( ctx ->r s r c _ l i s t) 6= NULL ⇒
370                   \nth ( to_ll ( ctx ->rsrc_list , NULL ) , 1) == \old ( ctx ->r s r c _ l i s t);
371          ensures l i n k e d _ l l( ctx ->rsrc_list , NULL , to_ll ( ctx ->rsrc_list , NULL ));
372          ensures s e p _ f r o m _ l i s t( ctx , node );
373          ensures \result == 1611;
374        disjoint b e h a v i o r s; complete b e h a v i o r s;
375   */

      Fig. 15. Illustrative provable example of the adjusted tpm2-tss list manipulation code,
      part 6/8.                                  26
376   int getNode ( CONTEXT * ctx , uint32_t rsrc_handle , NODE_T ** node ) {
377     /* @ assert l i n k e d _ l l( ctx ->rsrc_list , NULL , to_ll ( ctx ->rsrc_list , NULL ));*/
378     int r ;
379     uint32_t t p m _ h a n d l e;
380     { /* Block added to c i r c u m v e n t issues with the WP memory model */
381        NODE_T * tmp_node ;
382        /* @ ghost int n = 0;*/
383        /* @
384           loop i n v a r i a n t u n c h a n g e d _ l l{ Pre , Here }( to_ll ( ctx ->rsrc_list , NULL ));
385           loop i n v a r i a n t l i n k e d _ l l( ctx ->rsrc_list , NULL ,
386                                       to_ll ( ctx ->rsrc_list , NULL ));
387           loop i n v a r i a n t l i n k e d _ l l( ctx ->rsrc_list , tmp_node ,
388                                       to_ll ( ctx ->rsrc_list , tmp_node ));
389           loop i n v a r i a n t p t r _ s e p _ f r o m _ l i s t( tmp_node ,
390                                       to_ll ( ctx ->rsrc_list , tmp_node ));
391           loop i n v a r i a n t tmp_node 6= \null ⇒
392                                       in_list ( tmp_node , to_ll ( ctx ->rsrc_list , NULL ));
393           loop i n v a r i a n t ! i n _ l i s t _ h a n d l e( rsrc_handle ,
394                                       to_ll ( ctx ->rsrc_list , tmp_node ));
395           loop i n v a r i a n t n == \length ( to_ll ( ctx ->rsrc_list , tmp_node ));
396           for h a n d l e _ i n _ l i s t : loop i n v a r i a n t
397                 i n _ l i s t _ h a n d l e( rsrc_handle , to_ll ( ctx ->rsrc_list , NULL ));
398           loop assigns n , tmp_node ;
399           loop variant \length ( to_ll ( tmp_node , NULL ));
400        */
401        for ( tmp_node = ctx ->r s r c _ l i s t; tmp_node 6= NULL ;
402              tmp_node = tmp_node ->next ) {
403           /* @ assert tmp_node == \nth ( to_ll ( ctx ->rsrc_list , NULL ) , n );*/
404           /* @ assert l i n k e d _ l l( tmp_node , NULL , to_ll ( tmp_node , NULL ));*/
405           if ( tmp_node ->handle == r s r c _ h a n d l e){
406              /* @ assert d p t r _ s e p _ f r o m _ l i s t( node , to_ll ( ctx ->rsrc_list , NULL ));*/
407              * node = tmp_node ;
408              /* @ assert u n c h a n g e d _ l l{ Pre , Here }( to_ll { Pre }( ctx ->rsrc_list , NULL ));*/
409              /* @ assert p t r _ s e p _ f r o m _ a l l o c a b l e s(* node );*/
410              return 616;
411           }
412        /* @ assert to_ll ( ctx ->rsrc_list , tmp_node ->next )
413                  == ( to_ll ( ctx ->rsrc_list , tmp_node ) ^ [| tmp_node |]);*/
414        /* @ghost n ++;*/
415        }
416     }

      Fig. 16. Illustrative provable example of the adjusted tpm2-tss list manipulation code,
      part 7/8.




                                                        27
417   // @ ghost p o s t _ l o o p:;
418      /* @ assert !( i n _ l i s t _ h a n d l e( rsrc_handle , to_ll ( ctx ->rsrc_list , NULL )));*/
419      /* @ assert u n c h a n g e d _ l l{ Pre , Here }( to_ll ( ctx ->rsrc_list , NULL ));*/
420      r = i e s y s _ h a n d l e _ t o _ t p m _ h a n d l e( rsrc_handle , & t p m _ h a n d l e);
421      if ( r == 12) { return r ; };
422      { /* Block added to c i r c u m v e n t issues with the WP memory model */
423         NODE_T * t m p _ n o d e _ 2 = NULL ;
424         /* @ assert d p t r _ s e p _ f r o m _ l i s t(& tmp_node_2 ,
425                                                                to_ll { p o s t _ l o o p}( ctx ->rsrc_list , NULL ));*/
426         /* @ assert u n c h a n g e d _ l l{ Pre , Here }( to_ll { Pre }( ctx ->rsrc_list , NULL ));*/
427         /* @ assert \ s e p a r a t e d( node , & t m p _ n o d e _ 2 );*/
428         r = c r e a t e N o d e( ctx , rsrc_handle , & t m p _ n o d e _ 2);
429         /* @ assert s e p _ f r o m _ l i s t( ctx , node );*/
430         if ( r == 833) {/* @ assert s e p _ f r o m _ l i s t( ctx , node );*/ return r ;};
431   // @ ghost p o s t _ a l l o c:;
432         /* @ assert to_ll ( ctx ->rsrc_list , NULL )
433              ==([| ctx ->r s r c _ l i s t|] ^ to_ll { Pre }( \at ( ctx ->rsrc_list , Pre ) , NULL ));*/
434         /* @ assert c t x _ s e p _ f r o m _ l i s t( ctx , to_ll ( ctx ->rsrc_list , NULL ));*/
435         tmp_node_2 ->rsrc . handle = t p m _ h a n d l e;
436         tmp_node_2 ->rsrc . rsrcType = 0;
437         size_t offset = 0;
438         /* @ assert p t r _ s e p _ f r o m _ l i s t( tmp_node_2 ,
439                            to_ll ( ctx ->rsrc_list ->next , NULL ));*/
440         r = u i n t 3 2 _ M a r s h a l( tpm_handle , & tmp_node_2 ->rsrc . name . name [0] ,
441                                              sizeof ( tmp_node_2 ->rsrc . name . name ) ,& offset );
442         /* @ assert i n _ l i s t _ h a n d l e( rsrc_handle , to_ll ( ctx ->rsrc_list , NULL ));*/
443         if ( r 6= 0) { return r ;};
444         tmp_node_2 ->rsrc . name . size = offset ;
445         /* @ assert u n c h a n g e d _ l l{ post_alloc , Here }( to_ll ( ctx ->rsrc_list , NULL ));*/
446         /* @ assert d p t r _ s e p _ f r o m _ l i s t( node , to_ll ( ctx ->rsrc_list , NULL ));*/
447         /* @ assert d p t r _ s e p _ f r o m _ l i s t( node ,
448                            to_ll { Pre }( \at ( ctx ->rsrc_list , Pre ) , NULL ));*/
449         * node = t m p _ n o d e _ 2;
450         /* @ assert u n c h a n g e d _ l l{ Pre , Here }(
451                            to_ll { Pre }( \at ( ctx ->rsrc_list , Pre ) , NULL ));*/
452      }
453      /* @ assert u n c h a n g e d _ l l{ Pre , Here }(
454                        to_ll { Pre }( \at ( ctx ->rsrc_list , Pre ) , NULL ));*/
455      /* @ assert i n _ l i s t _ h a n d l e( rsrc_handle , to_ll ( ctx ->rsrc_list , NULL ));*/
456      /* @ assert ctx ->rsrc_list ->next == \at ( ctx ->rsrc_list , Pre );*/
457      /* @ assert \at ( ctx ->rsrc_list , Pre ) 6= \null ⇒
458            ctx ->rsrc_list ->next == \nth ( to_ll ( ctx ->rsrc_list , NULL ) , 1);*/
459      /* @ assert ctx ->rsrc_list ->handle == r s r c _ h a n d l e;*/
460      /* @ assert f r e s h n e s s( ctx , node );*/
461      /* @ assert s e p _ f r o m _ l i s t( ctx , node );*/
462      return 1611;
463   }
464
465   /* Command to run the proof with Frama - C :
466   frama -c - gui - c11 example . c - wp -wp - rte -wp - prover altergo , cvc4 , cvc4 - ce , script
467   -wp - timeout 50 -wp - smoke - tests -wp - prop =" - @lemma "
468   */

      Fig. 17. Illustrative provable example of the adjusted tpm2-tss list manipulation code,
      part 8/8.




                                                              28
