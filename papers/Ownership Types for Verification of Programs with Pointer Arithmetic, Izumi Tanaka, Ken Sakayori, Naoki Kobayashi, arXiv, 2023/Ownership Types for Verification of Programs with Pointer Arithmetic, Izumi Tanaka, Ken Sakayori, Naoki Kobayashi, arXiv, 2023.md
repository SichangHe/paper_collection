                                            Ownership Types for Veriﬁcation of Programs with
                                                          Pointer Arithmetic
                                                        Izumi Tanaka                                   Ken Sakayori                               Naoki Kobayashi
                                                  The University of Tokyo                        The University of Tokyo                        The University of Tokyo
                                                          Japan                                          Japan                                          Japan
                                              tanaka-izumi@g.ecc.u-tokyo.ac.jp                  sakayori@is.s.u-tokyo.ac.jp                     koba@is.s.u-tokyo.ac.jp

                                         Abstract
                                                                                                                               let 𝑥 = ref 0 in       // 𝑥 : {𝜈 : int | 𝜈 = 0} ref 1
arXiv:2312.06455v1 [cs.PL] 11 Dec 2023




                                         Toman et al. have proposed a type system for automatic
                                         veriﬁcation of low-level programs, which combines owner-                             𝑥 := 1;                 // 𝑥 : {𝜈 : int | 𝜈 = 1} ref 1
                                         ship types and reﬁnement types to enable strong updates                              𝑎𝑠𝑠𝑒𝑟𝑡 (∗𝑥 = 1);        // ok
                                         of reﬁnement types in the presence of pointer aliases. We
                                         extend their type system to support pointer arithmetic, and                                   Figure 1. A ConSORT Program
                                         prove its soundness. Based on the proposed type system, we
                                         have implemented a prototype tool for automated veriﬁca-
                                         tion of the lack of assertion errors of low-level programs                    type environments after each line. Here, please note that the
                                         with pointer arithmetic, and conﬁrmed its eﬀectiveness through type of 𝑥 is also updated: on the ﬁrst line, the type of 𝑥 indi-
                                         experiments.                                                                  cates that the value stored in 𝑥 is 0, while the type of 𝑥 on
                                                                                                                       the second line indicates that the value stored in 𝑥 is now 1.
                                         Keywords: Automated Program Veriﬁcation, Ownership Types, Please ignore the superscript 1 of ref for the moment. Based
                                         Reﬁnement Types, Pointer Arithmetic                                           on that, we can conclude that the assertion on the third line
                                                                                                                       succeeds.
                                         1 Introduction                                                                   As the example above shows, we need to strongly update
                                         Techniques for fully automated program veriﬁcation1 have                      reﬁnement types in the presence of mutable reference. A
                                         made a lot of progress in recent years [1, 2, 8, 11, 12, 14, 16,              naive update of reﬁnement types leads to a wrong reason-
                                         23], but it is still challenging to automatically verify low-                 ing. For example, consider the program in Figure 2. Since the
                                         level imperative programs that involve mutable references.                    variable 𝑦 is an alias of 𝑥, the value of 𝑦 (i.e., ∗𝑦) is updated
                                         Due to possible aliasing, it is in general diﬃcult to keep                    to 1 on the third line, and thus the assertion on the last line
                                         track of information about the value stored in each refer-                    should fail. The type of 𝑦 in the comment on the third line
                                         ence cell in a sound, precise, and eﬃcient manner. Toman                      has not been updated, so a naive type system may wrongly
                                         et al. [23] addressed this problem by combining reﬁnement                     judge that the program is safe. One way to correctly main-
                                         types with fractional ownerships, and constructed an auto-                    tain reﬁnement types would be to keep track of alias infor-
                                         mated veriﬁcation tool called ConSORT for a simple impera-                    mation; in the case of this example, if a type system keeps
                                         tive language with mutable references and ﬁrst-order recur-                   information that 𝑦 is an alias of 𝑥, then it can update the
                                         sive functions. In the present paper, we extend their type                    types of 𝑥 and 𝑦 together on the third line. It would, how-
                                         system to support pointer arithmetic.                                         ever, be diﬃcult in general, as complete alias information is
                                            Review of the Ideas of ConSORT. Before explaining our                      not always available statically.
                                         extension, let us ﬁrst explain the ideas of ConSORT. Con-                        To address the issue above, ConSORT combines fractional
                                         sider the program in Figure 1. The ﬁrst line creates a ref-                   ownerships with reﬁnement types. The type of a pointer to
                                         erence cell whose value is initialized to 0 and binds 𝑥 to it,                a value of type 𝜏 is of the form 𝜏 ref 𝑜 , where 𝑜, called an
                                         the second line updates the value of 𝑥 to 1, and the third                    ownership, ranges over [0, 1]. The type system of ConSORT
                                         line asserts that the value of 𝑥 is indeed 1. The comments of                 enforces that (i) if there are multiple aliases to a reference
                                         the ﬁrst and second lines (after “//”) show the (reﬁnement)                   cell, the sum of their ownerships is no greater than 1, (ii) a
                                         1 By fully automated program veriﬁcation, we refer to automated veriﬁca-
                                                                                                                       pointer can be used for update only when its ownership is
                                                                                                                       1 (so that even if other aliases exist, their ownerships are 0),
                                         tion of functional correctness (typically expressed by using assertions) of
                                         programs that require no or little user intervention. It should be contrasted and (iii) when a value is read through a pointer with own-
                                         with semi-automated veriﬁcation based on the veriﬁcation condition gen-       ership 0, information carried by the reﬁnement type is not
                                         eration approach [7, 15, 18], which require annotations of loop invariants    trusted. In the case of the program in Figure 2, the types
                                         and pre/post conditions of recursive procedures.                              indicated in the comments follow the constraints described
                                         Conference’17, July 2017, Washington, DC, USA                                 above. On line 2, the sum of ownerships is kept to 1 + 0 = 1;
                                         2023. ACM ISBN 978-x-xxxx-xxxx-x/YY/MM. . . $15.00                            on line 3, 𝑥 can be updated because the ownership of 𝑥 is
                                         https://doi.org/10.1145/nnnnnnn.nnnnnnn                                       1; on line 4, as the type of 𝑦 is {𝜈 : int | 𝜈 = 0} ref 0 , the
                                                                                                               1
Conference’17, July 2017, Washington, DC, USA                                                                                               Tanaka et al.



let 𝑥 = ref 0 in     // 𝑥 : {𝜈 : int | 𝜈 = 0} ref 1
let 𝑦 = 𝑥 in         // 𝑥 : {𝜈 : int | 𝜈 = 0} ref 1, 𝑦 : {𝜈 : int | 𝜈 = 0} ref 0
𝑥 := 1;              // 𝑥 : {𝜈 : int | 𝜈 = 1} ref 1, 𝑦 : {𝜈 : int | 𝜈 = 0} ref 0
𝑎𝑠𝑠𝑒𝑟𝑡 (∗𝑦 = 0);     // wrong

                                                  Figure 2. A Buggy ConSORT Program


let 𝑥 = ref 0 in     // 𝑥 : {𝜈 : int | 𝜈 = 0} ref 1
let 𝑦 = 𝑥 in         // 𝑥 : {𝜈 : int | 𝜈 = 0} ref 1, 𝑦 : {𝜈 : int | 𝜈 = 0} ref 0
𝑥 := 1;              // 𝑥 : {𝜈 : int | 𝜈 = 1} ref 1, 𝑦 : {𝜈 : int | 𝜈 = 0} ref 0
alias(𝑥 = 𝑦);        // 𝑥 : {𝜈 : int | 𝜈 = 1} ref 0.5, 𝑦 : {𝜈 : int | 𝜈 = 1} ref 0.5
assert(∗𝑦 = 1);      // ok

                                                  Figure 3. A Correct ConSORT Program

reﬁnement type {𝜈 : int | 𝜈 = 0} of ∗𝑦 is not trusted; hence,                 where the ownership 𝑟 is now a function from the set of rel-
the wrong conclusion ∗𝑦 = 0 is avoided.                                       ative addresses to the set of rational numbers in [0, 1]. For
   Figure 3 shows a variation of the program in Figure 2,                     example, if a pointer 𝑝 has the ownership {[0, 𝑛 − 1] ↦→
where the assertion on the last line has been replaced with                   1} (which represents the function 𝑟 such that 𝑟 (𝑖) = 1 if
∗𝑦 = 1. The expression alias(𝑥 = 𝑦); assumes that 𝑥 and 𝑦                     0 ≤ 𝑖 ≤ 𝑛 − 1 and 𝑟 (𝑖) = 0 otherwise), then it has the full
are aliases; it is provided as a hint to allow the type system                ownership to read/update 𝑝 [0], . . . , 𝑝 [𝑛 − 1]. The part 𝜏 of
to merge the ownerships and type information of 𝑥 and 𝑦                       (𝜆𝑖.𝜏) ref 𝑟 , which may depend on 𝑖, describes the type of
and redistribute them between the types of 𝑥 and 𝑦. In this                   the value stored in 𝑝 [𝑖]. For example, (𝜆𝑖.{𝜈 : int | 𝑖 = 0 ⇒
case, 0.5 ownership is redistributed to 𝑥 and 𝑦, and the re-                  𝜈 = 0}) ref { [0,𝑛−1]↦→1} describes the type of a pointer to an
ﬁnement type information {𝜈 : int | 𝜈 = 1} is propagated to                   integer array of size 𝑛, whose ﬁrst element is 0.
𝑦 ({𝜈 : int | 𝜈 = 0} is discarded, as the reﬁnement type with                    In Figure 4, the type of the function init on the ﬁrst two
0 ownership cannot be trusted, as described above). Based                     lines describes that the function takes an integer 𝑥 and a
on the type information, we can conclude that the assertion                   pointer 𝑝 with the full ownerships for 𝑝 [0], . . . , 𝑝 [𝑥 −1], and
on the last line is correct. The alias expressions can be auto-               returns an integer in a state where the values of 𝑝 [0], . . . , 𝑝 [𝑥−
matically inserted by static must-alias analysis, or provided                 1] have been updated to 0.2 Here the type on the right-hand
by a programmer as hints.                                                     side of the arrow not only describes the return type of the
                                                                              function, namely int, but also the types of the arguments af-
                                                                              ter the function call. On the fourth line, ifnp checks if 𝑥 is
   Our Proposal in This Paper. We extend the type sys-                        “not positive”, and if that is the case the function returns sta-
tem of ConSORT to support pointer arithmetic (i.e., pointer                   tus 1. On the ﬁfth line, the reﬁnement condition is updated
addition and subtraction; other operations such as XOR op-                    to 𝑖 = 0 ⇒ 𝜈 = 0, since the value of (the cell pointed to
erations and casting from/to integers are out of scope). We                   by) 𝑝 has been updated. On the next line, a new pointer 𝑞 is
also generalize reﬁnement types of arrays (or a chunk of                      created and the ownerships for 𝑝 [1], . . . , 𝑝 [𝑥 − 1] have been
memory consisting of consecutive memory addresses); Con-                      passed to 𝑞. On the seventh line, init is recursively called
SORT supported only integer arrays (not arrays of pointers),                  and the type of 𝑞 is updated. On the eighth line, the types of
and did not allow an array to be split into multiple arrays.                  𝑝 and 𝑞 are merged into the type of 𝑝. The alias command
   As a motivating example, consider the program in Fig-                      alias(𝑞 = 𝑝 + 1) can be automatically inserted in this case
ure 4, which deﬁnes a recursive function init. The function                   by a simple must-alias analysis.
init takes an integer 𝑛 and a pointer 𝑝 as arguments, and ini-                   We have formalized a new type system based on the ideas
tializes consecutive 𝑛 memory cells from 𝑝 (i.e., 𝑝 [0], . . . , 𝑝 [𝑛−        described above. Based on the type system, we have also
1]) to 0, by ﬁrst setting 𝑝 [0] to 0, and then by calling init re-            implemented a prototype tool for automated veriﬁcation of
cursively for 𝑝 + 1. We generalize the type of a pointer so
that a pointer may have an ownership for multiple memory                      2 Since there are no ownerships for 𝑖 ∉ [0, 𝑥 − 1], there is an implicit as-

cells. The extended pointer type is of the form (𝜆𝑖.𝜏) ref 𝑟 ,                sumption 0 ≤ 𝑖 ≤ 𝑥 − 1 for the reﬁnement condition 𝜈 = 0.
                                                                          2
Ownership Types for Verification of Programs with Pointer Arithmetic                                             Conference’17, July 2017, Washington, DC, USA



init (𝑥, 𝑝){ // init : h𝑥 : int, 𝑝 : (𝜆𝑖.{𝜈 : int | true}) ref { [0,𝑥 −1]↦→1} i → h𝑥 : int, 𝑝 : (𝜆𝑖.{𝜈 : int | 𝜈 = 0}) ref { [0,𝑥 −1]↦→1} | inti
    ifnp 𝑥 then 1 else
    𝑝 := 0;                         // 𝑝 : (𝜆𝑖.{𝜈 : int | 𝑖 = 0 ⇒ 𝜈 = 0}) ref { [0,𝑥 −1]↦→1}
    let 𝑞 = 𝑝 + 1 in                // 𝑝 : (𝜆𝑖.{𝜈 : int | 𝜈 = 0}) ref { [0,0]↦→1} , 𝑞 : (𝜆𝑖.{𝜈 : int | true}) ref { [0,𝑥 −2]↦→1}
    init (𝑥 − 1, 𝑞);                // 𝑝 : (𝜆𝑖.{𝜈 : int | 𝜈 = 0}) ref { [0,0]↦→1} , 𝑞 : (𝜆𝑖.{𝜈 : int | 𝜈 = 0}) ref { [0,𝑥 −2]↦→1}
    alias(𝑞 = 𝑝 + 1);               // 𝑝 : (𝜆𝑖.{𝜈 : int | 𝜈 = 0}) ref { [0,𝑥 −1]↦→1} , 𝑞 : (𝜆𝑖.{𝜈 : int | true}) ref ∅
    0      }

                                                               Figure 4. A Motivating Example

programs with pointer arithmetic. The tool takes simply typed                          reduces to 𝑒 1 if 𝑥 ≤ 0, and reduces to 𝑒 2 otherwise. The ex-
programs as inputs and infers the ownership functions and                              pression let 𝑥 = alloc 𝑛 in 𝑒 allocates a memory region of
the reﬁnement predicates. If the inference succeeds, it im-                            size 𝑛 (where the size denotes the number of words, rather
plies that no assertion failures will occur by the soundness                           than bytes), binds 𝑥 to the pointer to it, and evaluates 𝑒. The
of our type system. Note that the comments in Figure 4 were                            term ∗𝑦 denotes a dereference of the pointer 𝑦, and the term
shown merely for the sake of explanation, and these are not                            𝑦 ⊞ 𝑧 denotes a pointer arithmetic; we use ⊞ instead of + to
manual annotations.                                                                    avoid the confusion with the integer operator +. The alias
   The rest of this paper is organized as follows. Section 2 in-                       expressions alias(𝑥 = ∗𝑦); 𝑒 and alias(𝑥 = 𝑦 ⊞ 𝑧); 𝑒 check
troduces the target language. Section 3 introduces our type                            whether 𝑥 = ∗𝑦 and 𝑥 = 𝑦 ⊞ 𝑧 hold, respectively, and pro-
system and proves its soundness. Section 4 describes a type                            ceed to evaluate 𝑒 if that is the case; otherwise they stop
inference procedure and our prototype tool. Section 5 re-                              the execution of the whole program. The assert expression
ports experimental results. Section 6 discusses related work                           assert(𝜑); 𝑒 checks whether 𝜑 is true, and if so, proceeds to
and Section 7 concludes the paper.                                                     evaluate 𝑒; otherwise, the program is aborted with an (asser-
                                                                                       tion) error. The purpose of our type-based veriﬁcation is to
2        Target Language                                                               check that no assertion error occurs.
This section deﬁnes the syntax and operational semantics                                  Compared with the language of ConSORT [23], we have
of the target language of our veriﬁcation. It is a simple im-                          added the pointer addition 𝑦 ⊞ 𝑧, and replaced the primitive
perative language with pointer arithmetic.                                             let 𝑥 = ref 𝑦 in 𝑒 for creating a single reference cell with
                                                                                       the primitive let 𝑥 = alloc 𝑛 in 𝑒 for creating a contiguous
2.1 Syntax                                                                             memory region of arbitrary size. While this may seem to
The sets of deﬁnitions, expressions, and programs, ranged over                         be a small extension, it imposes a signiﬁcant challenge in
by 𝑑, 𝑒, and 𝑃 respectively, are deﬁned by:                                            the design of the type system and type inference discussed
                                                                                       in the following sections. In particular, as discussed in Sec-
        𝑑 ::= 𝑓 ↦→ (𝑥 1, . . . , 𝑥𝑛 )𝑒                                                 tion 1, the ownership of a pointer needs to be extended from
        𝑒 ::= 𝑛 | 𝑥 | let 𝑥 = 𝑒 1 in 𝑒 2                                               a single number (representing the ownership of the single
                                                                                       cell referred to by the pointer) to a function that maps each
           | ifnp 𝑥 then 𝑒 1 else 𝑒 2 | let 𝑥 = 𝑓 (𝑦1 , . . . , 𝑦𝑛 ) in 𝑒
                                                                                       relative address to a number (representing the ownership
           | let 𝑥 = alloc 𝑛 in 𝑒 | let 𝑥 = ∗𝑦 in 𝑒 | 𝑥 := 𝑦; 𝑒                        for the cell referred to by the relative address).
           | let 𝑥 = 𝑦 ⊞ 𝑧 in 𝑒 | let 𝑥 = 𝑦 op 𝑧 in 𝑒
                                                                                       Example 2.1. Recall the motivating example in Figure 4. It
           | alias(𝑥 = ∗𝑦); 𝑒 | alias(𝑥 = 𝑦 ⊞ 𝑧); 𝑒                                    is expressed as the function deﬁnition 𝑑 = init ↦→ (𝑥, 𝑝)𝑒 1 ,
           | assert(𝜑); 𝑒                                                              where 𝑒 1 is:
        𝑃 ::= h{𝑑 1 , . . . , 𝑑𝑛 }, 𝑒i.                                   ifnp 𝑥 then 1 else
Here, the meta-variables 𝑥, 𝑦, 𝑧, ... denote variables, and 𝑓             𝑝 := 0; let 𝑗 = 1 in let 𝑞 = 𝑝 ⊞ 𝑗 in let 𝑦 = 𝑥 − 𝑗 in
denotes a function name. The meta-variable 𝜑 denotes a                    let 𝑧 = init (𝑦, 𝑞) in alias(𝑞 = 𝑝 ⊞ 𝑗 ); 0
formula of the ﬁrst-order logic over integer arithmetic. The
meta-variable op ranges over a set of operators on integers         Let 𝑃 = ({𝑑 }, 𝑒 2 ) where 𝑒 2 is
such as + and −.                                                     let 𝑎 = alloc 3 in let 𝑢 = init (3, 𝑎) in
  We informally explain the meaning of expressions; the
                                                                     let  𝑘 =𝑒2 in let 𝑞 = 𝑎 ⊞ 𝑘 in let 𝑥 = ∗𝑞 in assert(𝑥 = 0); 0.
formal semantics is given in Section 2.2. The expression ifnp 𝑥 then 𝑒 1 else  2
                                                                                   3
Conference’17, July 2017, Washington, DC, USA                                                                                             Tanaka et al.


Then the assertion assert(𝑥 = 0) should succeed. If we re-             Remark 3. A run-time conﬁguration in ConSORT [23] was
place init (3, 𝑎) with init (2, 𝑎), then the assertion may fail.       expressed as a quadruple consisting of a register 𝑅, a heap 𝐻 ,
                                                                      a stack frame, and an expression 𝑒. We have removed the stack
                                                                       frame for the sake of simplicity and revised the rules accord-
Remark 1. As explained in Section 1, alias expressions are a
                                                                       ingly.                                                      
kind of program annotations to allow the type system to redis-
tribute ownership and reﬁnement type information. Following            3 Type System
the work of ConSORT, to keep the type system simple, we as-
sume that programs are annotated with proper alias expres-             This section introduces our ownership reﬁnement type sys-
sions in Sections 2–4. It is not diﬃcult to insert those annota-       tem.
tions automatically by using a must-alias analysis. According
                                                                       3.1 Types
to our inspection of the ConSORT benchmark3 and our own ex-
periments, a straightforward, extremely naive local must-alias         The syntax of types (ranged over by 𝜏) and function types
analysis (such as the one that just inserts alias(𝑝 = 𝑞 ⊞ 𝑛)           (ranged over by 𝜎 ) is given by:
in the body of let 𝑝 = 𝑞 ⊞ 𝑛 in · · ·) usually suﬃces. In fact,             𝜏 ::= {𝜈 : int | 𝜑} | (𝜆𝑖.𝜏) ref 𝑟
as described in Section 5, alias expressions are automatically
                                                                            𝜎 ::= h𝑥 1 : 𝜏1, . . . , 𝑥𝑛 : 𝜏𝑛 i → h𝑥 1 : 𝜏1′ , . . . , 𝑥𝑛 : 𝜏𝑛′ | 𝜏i
inserted in our prototype tool, so that programmers need not
provide alias annotations.                                            Here, the meta-variable 𝜑 ranges over the set of formulas of
                                                                       ﬁrst-order logic with integer arithmetic and 𝑟 ranges over
Remark 2. We consider only pointer addition (and subtrac-
                                                                       the set of functions (called ownership functions) from inte-
tion through the addition of a negative integer) as pointer op-
                                                                       gers to rational numbers in the range of [0, 1].
erations for the sake of simplicity. It would not be diﬃcult to
                                                                          The type {𝜈 : int | 𝜑} describes an integer 𝜈 that satisﬁes
extend our method to support pointers to structures. It would,
                                                                       𝜑; we often call 𝜑 a reﬁnement predicate. For example, {𝜈 :
however, be diﬃcult to deal with the XOR operation supported
                                                                       int | 𝜈 > 0} is the type of positive integers. We sometimes
in some of the semi-automated veriﬁcation methods [22]. 
                                                                       just write int for {𝜈 : int | ⊤}, where ⊤ denotes true. The
2.2   Operational Semantics                                            type (𝜆𝑖.𝜏) ref 𝑟 describes a pointer 𝑝 to a memory region,
                                                                       where the pointer has 𝑟 (𝑖) ownership for the address 𝑝 + 𝑖
This section deﬁnes the operational semantics of our lan-              and 𝜏 (which may depend on 𝑖) describes the type of the
guage. A conﬁguration is a triple h𝑅, 𝐻, 𝑒i. Here, 𝑅, called           value stored at 𝑝 + 𝑖. The ownership 𝑟 (𝑖) ranges over [0, 1].
a register ﬁle, is a map from a ﬁnite set of variables to the          If 𝑟 (𝑖) = 1, the cell at 𝑝 + 𝑖 can be read/written through the
set 𝑉 consisting of integers and pointer addresses, where a            pointer. If 0 < 𝑟 (𝑖) < 1, then the cell at 𝑝 + 𝑖 can only be
pointer address is a pair (𝑎, 𝑖) of integers; 𝑎 denotes the ab-        read; and if 𝑟 (𝑖) = 0, then the cell at 𝑝 +𝑖 cannot be accessed
solute address of a base pointer and 𝑖 is the relative address.        at all through the pointer 𝑝. For example, (𝜆𝑖.{𝜈 : int | 0 ≤
A heap 𝐻 is a map from a ﬁnite set of pointer addresses to 𝑉 .         𝑖 ≤ 9 ⇒ 𝜈 = 𝑖}) ref 𝑟 with 𝑟 (𝑖) = 1 for 𝑖 ∈ {0, . . . , 9} and
The reduction relation −→𝐷 for conﬁgurations is given in               𝑟 (𝑖) = 0 for 𝑖 ∈ Z \ {0, . . . , 9} describes (a pointer to the ﬁrst
Figure 5. In the ﬁgures, 𝐸 ranges over the set of evaluation           address of) a mutable array of size 10 whose 𝑖-th value is 𝑖.
contexts, deﬁned by: 𝐸 ::= [ ] | let 𝑥 = 𝐸 in 𝑒.                          We often write {[𝑚, 𝑛] ↦→ 𝑢} for the ownership function
   As most of the rules should be self-explanatory, we only            𝑟 such that 𝑟 (𝑖) = 𝑢 if 𝑚 ≤ 𝑖 ≤ 𝑛 and 𝑟 (𝑖) = 0 other-
explain a few rules. The rule R-MkArray is for allocating              wise. In this section, we allow an ownership function to be
a memory region. It picks a fresh address 𝑎 (which is rep-             any mathematical function in Z → [0, 1], but we will re-
resented as a label, rather than an integer; thus, memory              strict the shape of ownership functions to those of the form
regions with diﬀerent base pointers never overlap), and al-            {[𝑚, 𝑛] ↦→ 𝑢} in Section 4 for the purpose of type inference.
locates a region consisting of the addresses from (𝑎, 0) to               A function type is of the form h𝑥 1 : 𝜏1, . . . , 𝑥𝑛 : 𝜏𝑛 i →
(𝑎, 𝑛 − 1). Initial values stored in those memory cells can be         h𝑥 1 : 𝜏1′ , . . . , 𝑥𝑛 : 𝜏𝑛′ | 𝜏i, where 𝜏𝑖 and 𝜏𝑖′ are the types of the
arbitrary. In the rules R-AliasDeref and R-AliasDerefFail,             𝑖-th argument respectively before and after a function call,
it is checked whether 𝑥 = ∗𝑦 holds. If that does not hold,             and 𝜏 is the type of the return value. For example, as given
the conﬁguration is reduced to AliasFail. Note that we dis-            in Section 1, the type:
tinguish it from AssertFail in the rule R-AssertFail. The
goal of our veriﬁcation is to check that AssertFail does not             h𝑥 : int, 𝑝 : (𝜆𝑖.int) ref { [0,𝑥 −1]↦→1} i
occur, assuming that the alias annotations are correct (i.e.,
                                                                          → h𝑥 : int, 𝑝 : (𝜆𝑖.{𝜈 : int | 𝜈 = 0}) ref { [0,𝑥 −1]↦→1} | inti
AliasFail never occurs). In the rule R-Assert, [𝑅]𝜑 repre-
sents the formula obtained by replacing each variable 𝑥 ∈              describes a function that takes an integer 𝑥 and (a pointer
dom(𝑅) in 𝜑 with 𝑅(𝑥).                                                 to) an array of size 𝑥 with the full ownership, sets all the
                                                                       elements to 0, and returns an integer.
3 https://github.com/SoftwareFoundationGroupAtKyotoU/consort.

                                                                   4
Ownership Types for Verification of Programs with Pointer Arithmetic                                 Conference’17, July 2017, Washington, DC, USA



                   h𝑅, 𝐻, 𝑒i −→𝐷 h𝑅 ′ , 𝐻 ′ , 𝑒 ′ i                                        (𝑎, 0) ∉ dom(𝐻 )           𝑥 ′ ∉ dom(𝑅)
                                                          (R-Context)               𝐻 ′ = 𝐻 {(𝑎, 0) ↦→ 𝑚 0 } · · · {(𝑎, 𝑛 − 1) ↦→ 𝑚𝑛−1 }
               h𝑅, 𝐻, 𝐸 [𝑒]i −→𝐷 h𝑅 ′ , 𝐻 ′ , 𝐸 [𝑒 ′ ]i
                                                                                            h𝑅, 𝐻, let 𝑥 = alloc 𝑛 in 𝑒i −→𝐷
                           𝑥 ′ ∉ dom(𝑅)                                                      h𝑅{𝑥 ′ ↦→ (𝑎, 0)}, 𝐻 ′ , [𝑥 ′ /𝑥]𝑒i
                                                           (R-LetInt)
                    h𝑅, 𝐻, let 𝑥 = 𝑛 in 𝑒i                                                                                         (R-MkArray)
                 −→𝐷 h𝑅{𝑥 ′ ↦→ 𝑛}, 𝐻, [𝑥 ′ /𝑥]𝑒i
                                                                                               𝑓 ↦→ (𝑥 1 , . . . , 𝑥𝑛 )𝑒 ∈ 𝐷
                                                                                                                                           (R-Call)
                           𝑥 ′ ∉ dom(𝑅)                                               h𝑅, 𝐻, let 𝑥 = 𝑓 (𝑦1 , . . . , 𝑦𝑛 ) in 𝑒 ′ i
                                                           (R-LetVar)
                    h𝑅, 𝐻, let 𝑥 = 𝑦 in 𝑒i                                       −→𝐷 h𝑅, 𝐻, let 𝑥 = [𝑦1 /𝑥 1 ] · · · [𝑦𝑛 /𝑥𝑛 ]𝑒 in 𝑒 ′ i
               −→𝐷 h𝑅{𝑥 ′ ↦→ 𝑅(𝑦)}, 𝐻, [𝑥 ′ /𝑥]𝑒i
                                                                                               𝐻 (𝑅(𝑦)) = 𝑅(𝑥)
                                                                                                                                (R-AliasDeref)
                              𝑅(𝑥) ≤ 0                                            h𝑅, 𝐻, alias(𝑥 = ∗𝑦); 𝑒i −→𝐷 h𝑅, 𝐻, 𝑒i
                                                           (R-IfTrue)
                  h𝑅, 𝐻, ifnp 𝑥 then 𝑒 1 else 𝑒 2 i
                          −→𝐷 h𝑅, 𝐻, 𝑒 1 i                                     𝑅(𝑥) = (𝑎, 𝑖 + 𝑅(𝑧))          𝑅(𝑦) = (𝑎, 𝑖)
                                                                                                                               (R-AliasAddPtr)
                                                                             h𝑅, 𝐻, alias(𝑥 = 𝑦 ⊞ 𝑧); 𝑒i −→𝐷 h𝑅, 𝐻, 𝑒i
                              𝑅(𝑥) > 0
                                                           (R-IfFalse)
                  h𝑅, 𝐻, ifnp 𝑥 then 𝑒 1 else 𝑒 2 i                                                   𝐻 (𝑅(𝑦)) ≠ 𝑅(𝑥)
                          −→𝐷 h𝑅, 𝐻, 𝑒 2 i                                              h𝑅, 𝐻, alias(𝑥 = ∗𝑦); 𝑒i −→𝐷 AliasFail
                                                                                                                    (R-AliasDerefFail)
                           𝑥 ′ ∉ dom(𝑅)
                                                            (R-Deref)                      𝑅(𝑥) = (𝑎 1 , 𝑖 1 )  𝑅(𝑦) = (𝑎 2 , 𝑖 2 )
                   h𝑅, 𝐻, let 𝑥 = ∗𝑦 in 𝑒i
             −→𝐷 h𝑅{𝑥 ′ ↦→ 𝐻 (𝑅(𝑦))}, 𝐻, [𝑥 ′ /𝑥]𝑒i                                            𝑎 1 ≠ 𝑎 2 ∨ 𝑖 1 ≠ 𝑖 2 + 𝑅(𝑧)
                                                                                       h𝑅, 𝐻, alias(𝑥 = 𝑦 ⊞ 𝑧); 𝑒i −→𝐷 AliasFail
               𝑅(𝑥) = (𝑎, 𝑖)        (𝑎, 𝑖) ∈ dom(𝐻 )                                                                (R-AliasAddPtrFail)
                                                           (R-Assign)
                       h𝑅, 𝐻, 𝑥 := 𝑦; 𝑒i
                 −→𝐷 h𝑅, 𝐻 {(𝑎, 𝑖) ←↪ 𝑅(𝑦)}, 𝑒i                                                             |= [𝑅]𝜑
                                                                                                                                      (R-Assert)
                                                                                           h𝑅, 𝐻, assert(𝜑); 𝑒i −→𝐷 h𝑅, 𝐻, 𝑒i
             𝑅(𝑦) = (𝑎, 𝑖)        𝑥 ′ ∉ dom(𝑅)
                                                          (R-AddPtr)                                  6 |= [𝑅]𝜑
            h𝑅, 𝐻, let 𝑥 = 𝑦 ⊞ 𝑧 in 𝑒i                                                                                           (R-AssertFail)
      −→𝐷 h𝑅{𝑥 ′ ↦→ (𝑎, 𝑖 + 𝑅(𝑧))}, 𝐻, [𝑥 ′ /𝑥]𝑒i                                   h𝑅, 𝐻, assert(𝜑); 𝑒i −→𝐷 AssertFail


                                                            Figure 5. Reduction Rules

Remark 4. Here we summarize the diﬀerence from the types                     3.2 Typing Rules
of ConSORT [23]. In ConSORT, the type of a pointer is of the                 A type judgment for expressions is of the form Θ | Γ ⊢ 𝑒 :
form 𝜏 ref 𝑟 where 𝜏 is the type of a value stored in the target             𝜏 =⇒ Γ ′ , where Θ, called a function type environment, is a
cell of the pointer, 𝑟 ∈ [0, 1] is the ownership for the cell. To al-        map from variables to function types, and Γ, called a type en-
low pointer arithmetic, we needed to extend it so that both the              vironment, is a sequence of type bindings of the form 𝑥 : 𝜏.
𝜏-part (now described as 𝜆𝑖.𝜏) and 𝑟 -part carry information                 We sometimes view the type environment as a map from
about the memory region around the cell, not just the cell. Con-             variables to types, and implicitly allow re-ordering of type
SORT also supports an array type of the form (𝜆𝑖.𝜏) array𝑟                   bindings (subject to the well-formedness condition below).
(though not formalized in the paper [23]) but the ownership                  We write dom(Γ) for the domain of the map Γ. The judg-
𝑟 ∈ [0, 1] is a single value that expresses the ownership for the            ment Θ | Γ ⊢ 𝑒 : 𝜏 =⇒ Γ ′ means that the expression 𝑒
entire array, and the decomposition of the ownership for sub-                is well-typed under Θ and Γ, and evaluates to a value of
arrays (which is crucial for the support of pointer arithmetic)              the type 𝜏, modifying Γ to Γ ′ . We implicitly require the fol-
is not allowed. ConSORT supports context polymorphism; we                    lowing well-formedness conditions on types, type environ-
have omitted it for the sake of simplicity, as it is orthogonal to           ments, and type judgments. First, the variables that occur
our extension for supporting pointer arithmetic.                            in reﬁnement predicates and ownership functions must be
                                                                             bound as integer variables. For example, the type (𝜆𝑖.{𝜈 :int |


                                                                         5
Conference’17, July 2017, Washington, DC, USA                                                                                            Tanaka et al.


𝜈 > 𝑥 }) ref { [0,𝑥 −1]↦→1} is well formed under the type envi-               strengthening operation 𝜏 ∧𝑥 𝜑 and typed equality proposi-
ronment 𝑥 : int but not under the empty type environment                      tion 𝑥 =𝜏 𝑦 are deﬁned by:
•. Second, for each pointer type (𝜆𝑖.𝜏) ref 𝑟 , we require that
                                                                                       {𝜈 : int | 𝜑} ∧𝑥 𝜑 ′ = {𝜈 : int | 𝜑 ∧ [𝜈/𝑥]𝜑 ′ }
𝑟 (𝑖) = 0 implies Empty(𝜏), where Empty is inductively de-
ﬁned by: (i) Empty({𝜈 : int | 𝜑}) if 𝜑 is equivalent to true,                           (𝜆𝑖.𝜏) ref 𝑟 ∧𝑥 𝜑 ′ = (𝜆𝑖.𝜏) ref 𝑟
and (ii) Empty((𝜆𝑖.𝜏) ref 𝑟 ) if Empty(𝜏) and 𝑟 (𝑖) = 0 for ev-                           (𝑥 = {𝜈:int|𝜑 } 𝑦) = (𝑥 = 𝑦)
ery 𝑖 ∈ Z. We write Γ ⊢WF 𝜏 if 𝜏 is well-formed under Γ; the                             (𝑥 = (𝜆𝑖 .𝜏 ) ref 𝑟 𝑦) = ⊤
formal deﬁnition is given in Appendix A.
   The typing rules for expressions and programs and aux-                     The operations 𝜏 ∧𝑥 𝜑 and 𝑥 =𝜏 𝑦 are always used together
iliary rules for subtyping are given in Figures 6–8. In the                   to propagate the information about equalities over integer
rules, Γ [𝑥 : 𝜏] represents a type environment Γ such that                    variables.
Γ(𝑥) = 𝜏. We write Γ, 𝑥 : 𝜏 for the extension of Γ (where                        In the rule T-Assign, the premise 𝑟 (0) = 1 ensures that
𝑥 ∉ dom(Γ)) with the binding 𝑥 : 𝜏, and Γ [𝑥 ←↪ 𝜏] for the                    the ownership of the pointer 𝑥 (at index 0) is 1. The type of
type environment obtained from Γ by updating the binding                      𝑦 is split into 𝜏1 for the type of 𝑦 after the assignment, and 𝜏2
of 𝑥 to 𝜏. The empty environment is represented as •.                         for the type of the value stored at 𝑥 with index 0. In the rule
   We explain key rules and notations used in the rules be-                   T-AddPtr for pointer arithmetic, the type and ownership of
low. Except for the rules for new primitives, i.e. T-MkArray,                 𝑦 is split into those for 𝑦 and 𝑥, and the indices for the type
T-AddPtr, and T-AliasAddPtr, the typing rules have been                       and ownership of 𝑥 are shifted accordingly.
made to look superﬁcially similar to those of ConSORT [23]                       The rules T-AliasAddPtr and T-AliasDeref allow us to
by appropriately extending operations on types and owner-                     redistribute the ownerships of pointers based on alias in-
ships. The rule T-Var is for variables. The operation 𝜏1 + 𝜏2                 formation. These rules are analogous to the corresponding
is inductively deﬁned by:                                                     rules of ConSORT, but more complex due to the presence
                                                                              of pointer arithmetic.
      {𝜈 : int | 𝜑 1 } + {𝜈 : int | 𝜑 2 } = {𝜈 : int | 𝜑 1 ∧ 𝜑 2 }               The rule T-Assert requires that the asserted formula 𝜑
       (𝜆𝑖.𝜏1 ) ref 𝑟 1 + (𝜆𝑖.𝜏2 ) ref 𝑟 2 = (𝜆𝑖.𝜏1 + 𝜏2 ) ref 𝑟 1 +𝑟 2       must be valid under the current context, where JΓK is de-
                                                                              ﬁned by:
Here, 𝑟 1 + 𝑟 2 denotes the pointwise addition of the owner-                             J•K = ⊤                 J{𝜈 : int | 𝜑}K𝑦 = [𝑦/𝜈]𝜑
ships. Intuitively, T-Var splits the current type 𝜏1 + 𝜏2 of 𝑥
                                                                                   JΓ, 𝑥 : 𝜏K = JΓK ∧ J𝜏K𝑥        J(𝜆𝑖.𝜏) ref 𝑟 K𝑦 = ⊤
into 𝜏1 and 𝜏2 , respectively for the expression 𝑥 and the type
environment after the evaluation of the expression. For ex-                      In the rule T-Sub, the premise Γ ≤ Γ ′ means that Γ is a
ample,                                                                        stronger type assumption than Γ ′ (for example, 𝑥 : {𝜈 : int |
                                                                              𝜈 = 1} ≤ 𝑥 :{𝜈 :int | 𝜈 > 0}). The rule allows us to strengthen
             Θ | Γ ⊢ 𝑥 : (𝜆𝑖.{𝜈 : int | 𝜑 1 }) ref {0↦→1}                     the type environment before an execution of the expression,
                                                                              and weakens the type and type environment after the exe-
                  =⇒ 𝑥 : (𝜆𝑖.{𝜈 : int | 𝜑 2 }) ref {1↦→1}
                                                                              cution.
                                                                                 Figure 8 gives typing rules for function deﬁnitions and
and
                                                                              programs. The rule T-FunDef checks that the function def-
                                                                              inition is consistent with the assumption Θ on the types of
           Θ | Γ ⊢ 𝑥 : (𝜆𝑖.{𝜈 : int | 𝜑}) ref { [0,1]↦→0.5}
                                                                              functions. The conclusion of the rule T-Funs means that the
                 =⇒ 𝑥 : (𝜆𝑖.{𝜈 : int | 𝜑}) ref { [0,1]↦→0.5}                  function deﬁnitions 𝐷 provides a function environment as
                                                                              described by Θ. The rule T-Prog is for the whole program,
                                                               def
hold for Γ = 𝑥 : (𝜆𝑖.{𝜈 : int | 𝜑}) ref { [0,1]↦→1} , 𝜑 1 = 𝑖 = 0 ⇒           which checks that 𝑒 is well-typed under the function type
           def                             def                                environment Θ provided by 𝐷.
𝜈 = 0, 𝜑 2 = 𝑖 = 1 ⇒ 𝜈 = 1, and 𝜑 = 𝜑 1 ∧ 𝜑 2 .
   In the rule T-MkArray for memory allocation, we assign                     Example 3.1. Recall Example 2.1. The else-part of 𝑒 1 is typed
the full ownership 1 for the relative addresses 𝑖 = 0, . . . , 𝑛−1,           as shown in Figure 9. Here, we have omitted some of the
and the null ownership 0 to other addresses, to prevent out-                  type bindings (such as 𝑥 : int). The ﬁrst line indicates that
of-boundary memory access. In addition, we require that                       there is initially no information on the value stored at 𝑝. Af-
the types of values stored in the allocated memory region                     ter the assignment 𝑝 := 0, the type of the value stored at 𝑝 is
satisfy the Empty predicate, as those values are not initial-                 updated accordingly. After let 𝑞 = 𝑝 ⊞ 𝑗 , the ownership held
ized. In the rule T-Deref for pointer deference, we require                   by 𝑝 is split into {0 ↦→ 1} and {[1, 𝑥 −1] ↦→ 1}, and the latter
that the ownership 𝑟 (0) of the pointer 𝑥 with index 0 is pos-                is passed to 𝑞. By using the rule T-Call, and assuming that
itive. The type 𝜏 𝑦 of the value stored at 𝑦 (with index 0) is                init has the type given in Figure 4, the type of 𝑞 is updated.
split into 𝜏 ′ and 𝜏𝑥 , and the type of 𝑥 in 𝑒 is set to 𝜏𝑥 . The             On the last line, the types of 𝑝 and 𝑞 are merged into the
                                                                          6
Ownership Types for Verification of Programs with Pointer Arithmetic                                             Conference’17, July 2017, Washington, DC, USA



                                                                   (T-Int)                                                                      (T-Var)
               Θ | Γ ⊢ 𝑛 : {𝜈 : int | 𝜈 = 𝑛} =⇒ Γ                                                 Θ | Γ [𝑥 : 𝜏1 + 𝜏2 ] ⊢ 𝑥 : 𝜏1 =⇒ Γ [𝑥 ←↪ 𝜏2 ]
                                                                                                               (
                                                                                                                 1 0 ≦𝑖 ≦𝑛−1
                                                                                                       𝑟 (𝑖) =
                                                                                                                 0 𝑜𝑡ℎ𝑒𝑟𝑤𝑖𝑠𝑒
               Θ | Γ ⊢ 𝑒 1 : 𝜏1 =⇒ Γ1 𝑥 ∉ dom(Γ ′ )                                                  𝑥 ∉ dom(Γ ′ )         𝐸𝑚𝑝𝑡𝑦(𝜏 ′ )
                                                                                                                         𝑟
                   Θ | Γ1, 𝑥 : 𝜏1 ⊢ 𝑒 2 : 𝜏 =⇒ Γ ′                                                Θ | Γ, 𝑥 : (𝜆𝑖.𝜏 ) ref ⊢ 𝑒 : 𝜏 =⇒ Γ ′
                                                                                                                  ′
                                                                   (T-Let)                                                               (T-MkArray)
                Θ | Γ ⊢ let 𝑥 = 𝑒 1 in 𝑒 2 : 𝜏 =⇒ Γ ′                                            Θ | Γ ⊢ let 𝑥 = alloc 𝑛 in 𝑒 : 𝜏 =⇒ Γ ′

                                                 Θ | Γ [𝑥 ←↪ {𝜈 : int | 𝜑 ∧ 𝜈 ≤ 0}] ⊢ 𝑒 1 : 𝜏 =⇒ Γ ′
                                                 Θ | Γ [𝑥 ←↪ {𝜈 : int | 𝜑 ∧ 𝜈 > 0}] ⊢ 𝑒 2 : 𝜏 =⇒ Γ ′
                                                                                                                                                          (T-If)
                                           Θ | Γ [𝑥 : {𝜈 : int | 𝜑}] ⊢ ifnp 𝑥 then 𝑒 1 else 𝑒 2 : 𝜏 =⇒ Γ ′


                         Θ(𝑓 ) = h𝑥 1 : 𝜏1, . . . , 𝑥𝑛 : 𝜏𝑛 i → h𝑥 1 : 𝜏1′ , . . . , 𝑥𝑛 : 𝜏𝑛′ | 𝜏i      𝜎 = [𝑦1 /𝑥 1 ] · · · [𝑦𝑛 /𝑥𝑛 ]
                                        Θ | Γ [𝑦𝑖 ←↪ 𝜎𝜏𝑖′ ], 𝑥 : 𝜎𝜏 ⊢ 𝑒 : 𝜏 ′ =⇒ Γ ′                  𝑥 ∉ dom(Γ ′ )
                                                                                                                                                       (T-Call)
                                             Θ | Γ [𝑦𝑖 : 𝜎𝜏𝑖 ] ⊢ let 𝑥 = 𝑓 (𝑦1 , . . . , 𝑦𝑛 ) in 𝑒 : 𝜏 ′ =⇒ Γ ′

                                         𝑖 : {𝜈 : int | 𝜈 = 0} ⊢ 𝜏 ′ + 𝜏𝑥 ≈ 𝜏 𝑦 , 𝜏 𝑦′ ≈ 𝜏 ′ ∧𝑦 (𝑦 =𝜏 ′ 𝑥)
                                                          𝑖 : {𝜈 : int | 𝜈 ≠ 0} ⊢ 𝜏 𝑦′ ≈ 𝜏 𝑦
                                                        𝑟
                              Θ | Γ [𝑦 ←↪ (𝜆𝑖.𝜏 𝑦 ) ref ], 𝑥 : 𝜏𝑥 ⊢ 𝑒 : 𝜏 =⇒ Γ ′
                                                ′                                        𝑥 ∉ dom(Γ ′ )                   𝑟 (0) > 0
                                                                           𝑟                                                                          (T-Deref)
                                                Θ | Γ [𝑦 : (𝜆𝑖.𝜏 𝑦   ) ref ] ⊢ let 𝑥 = ∗𝑦 in 𝑒 : 𝜏 =⇒ Γ ′

                               𝑖 : {𝜈 : int | 𝜈 = 0} ⊢ 𝜏𝑥′ ≈ 𝜏2 ∧𝑥 (𝑥 =𝜏2 𝑦)          𝑖 : {𝜈 : int | 𝜈 ≠ 0} ⊢ 𝜏𝑥′ ≈ 𝜏𝑥
                                       Θ | Γ [𝑥 ←↪ (𝜆𝑖.𝜏𝑥′ ) ref 𝑟 ] [𝑦 ←↪ 𝜏1 ] ⊢ 𝑒 : 𝜏 =⇒ Γ ′         𝑟 (0) = 1
                                                                                                                                                     (T-Assign)
                                            Θ | Γ [𝑥 : (𝜆𝑖.𝜏𝑥 ) ref 𝑟 ] [𝑦 : 𝜏1 + 𝜏2 ] ⊢ 𝑥 := 𝑦; 𝑒 : 𝜏 =⇒ Γ ′

                                           𝑥 ∉ dom(Γ ′ )       ∀𝑖 ∈ Z.𝑟 𝑥 (𝑖 − 𝑧) + 𝑟 𝑦′ (𝑖) = 𝑟 𝑦 (𝑖)
                                                  𝑟 𝑦′
                          Θ | Γ [𝑦 ←↪ (𝜆𝑖.𝜏1 ) ref ], 𝑥 : (𝜆𝑖.[(𝑖 + 𝑧)/𝑖]𝜏2 ) ref 𝑟𝑥 , 𝑧 : {𝜈 : int | 𝜑} ⊢ 𝑒 : 𝜏 =⇒ Γ ′
                                                                                                                                                    (T-AddPtr)
                              Θ | Γ [𝑦 : (𝜆𝑖.(𝜏1 + 𝜏2 )) ref 𝑟 𝑦 ] [𝑧 : {𝜈 : int | 𝜑}] ⊢ let 𝑥 = 𝑦 ⊞ 𝑧 in 𝑒 : 𝜏 =⇒ Γ ′
                                                                                                                    ′                     ′
                      𝑖 2 : {𝜈 : int | 𝜈 = 0} ⊢ ((𝜆𝑖 1 .𝜏𝑥 ) ref 𝑟𝑥 + (𝜆𝑖 1 .𝜏 𝑦 ) ref 𝑟 𝑦 ) ≈ ((𝜆𝑖 1 .𝜏𝑥′ ) ref 𝑟𝑥 + (𝜆𝑖 1 .𝜏 𝑦′ ) ref 𝑟 𝑦 )
                                                                                                                  ′
                                            𝑖 2 : {𝜈 : int | 𝜈 ≠ 0} ⊢ (𝜆𝑖 1 .𝜏 𝑦 ) ref 𝑟 𝑦 ≈ (𝜆𝑖 1 .𝜏 𝑦′ ) ref 𝑟 𝑦
                                                               ′                                    ′
                                 Θ | Γ [𝑥 ←↪ (𝜆𝑖 1 .𝜏𝑥′ ) ref 𝑟𝑥 ] [𝑦 ←↪ (𝜆𝑖 2 .(𝜆𝑖 1 .𝜏 𝑦′ ) ref 𝑟 𝑦 ) ref 𝑟 ] ⊢ 𝑒 : 𝜏 =⇒ Γ ′
                                                                                                                                                 (T-AliasDeref)
                          Θ | Γ [𝑥 : (𝜆𝑖 1 .𝜏𝑥 ) ref 𝑟𝑥 ] [𝑦 : (𝜆𝑖 2 .(𝜆𝑖 1 .𝜏 𝑦 ) ref 𝑟 𝑦 ) ref 𝑟 ] ⊢ alias(𝑥 = ∗𝑦); 𝑒 : 𝜏 =⇒ Γ ′

                                              ∀𝑖 ∈ Z.𝑟 𝑥𝑧 (𝑖) = 𝑟 𝑥 (𝑖 − 𝑧), 𝑟 𝑥′ 𝑧 (𝑖) = 𝑟 𝑥′ (𝑖 − 𝑧)
                                                                                                         ′                   ′
                       ((𝜆𝑖.[(𝑖 − 𝑧)/𝑖]𝜏𝑥 ) ref 𝑟𝑥𝑧 + (𝜆𝑖.𝜏 𝑦 ) ref 𝑟 𝑦 ) ≈ ((𝜆𝑖.[(𝑖 − 𝑧)/𝑖]𝜏𝑥′ ) ref 𝑟𝑥𝑧 + (𝜆𝑖.𝜏 𝑦′ ) ref 𝑟 𝑦 )
                                                       ′                          ′
                            Θ | Γ [𝑥 ←↪ (𝜆𝑖.𝜏𝑥′ ) ref 𝑟𝑥 ] [𝑦 ←↪ (𝜆𝑖.𝜏 𝑦′ ) ref 𝑟 𝑦 ], 𝑧 : {𝜈 : int | 𝜑} ⊢ 𝑒 : 𝜏 =⇒ Γ ′
                                                                                                                                                (T-AliasAddPtr)
                     Θ | Γ [𝑥 : (𝜆𝑖.𝜏𝑥 ) ref 𝑟𝑥 ] [𝑦 : (𝜆𝑖.𝜏 𝑦 ) ref 𝑟 𝑦 ] [𝑧 : {𝜈 : int | 𝜑}] ⊢ alias(𝑥 = 𝑦 ⊞ 𝑧); 𝑒 : 𝜏 =⇒ Γ ′

                     |= JΓK ⇒ 𝜑        Γ ⊢WF 𝜑                                                              Γ ≤ Γ′     Γ ′′, 𝜏 ≤ Γ ′′′ , 𝜏 ′
                        Θ | Γ ⊢ 𝑒 : 𝜏 =⇒ Γ ′                                                                  Θ | Γ ⊢ 𝑒 : 𝜏 =⇒ Γ ′′
                                                                                                                   ′
                                                              (T-Assert)                                                                                (T-Sub)
                 Θ | Γ ⊢ assert(𝜑); 𝑒 : 𝜏 =⇒ Γ ′                                                               Θ | Γ ⊢ 𝑒 : 𝜏 ′ =⇒ Γ ′′′


                                                         Figure 6. Expression Typing Rules




                                                                                7
Conference’17, July 2017, Washington, DC, USA                                                                                                            Tanaka et al.



                          |= JΓK ⇒ (𝜑 1 ⇒ 𝜑 2 )                                                            ∀𝑥 ∈ dom(Γ ′ ).Γ ⊢ Γ(𝑥) ≤ Γ ′ (𝑥)
                                                                       (S-Int)                                                                           (S-TyEnv)
                   Γ ⊢ {𝜈 : int | 𝜑 1 } ≤ {𝜈 : int | 𝜑 2 }                                                                    Γ ≤ Γ′

                        𝑟1 ≥ 𝑟2            Γ ⊢ 𝜏1 ≤ 𝜏2                                                   Γ, 𝑥 : 𝜏 ≤ Γ ′, 𝑥 : 𝜏 ′           𝑥 ∉ dom(Γ)
                                      𝑟1                    𝑟2         (S-Ref)                                                       ′     ′
                                                                                                                                                             (S-Res)
                   Γ ⊢ (𝜆𝑖.𝜏1 ) ref        ≤ (𝜆𝑖.𝜏2 ) ref                                                                   Γ, 𝜏 ≤ Γ , 𝜏

                                                         Γ ⊢ 𝜏1 ≈ 𝜏2 iﬀ Γ ⊢ 𝜏1 ≤ 𝜏2 and Γ ⊢ 𝜏2 ≤ 𝜏1

                                                                    Figure 7. Subtyping Rules


                                                Θ(𝑓 ) = h𝑥 1 : 𝜏1, . . . , 𝑥𝑛 : 𝜏𝑛 i → h𝑥 1 : 𝜏1′ , . . . , 𝑥𝑛 : 𝜏𝑛′ | 𝜏i
                                                 Θ | 𝑥 1 : 𝜏1, . . . , 𝑥𝑛 : 𝜏𝑛 ⊢ 𝑒 : 𝜏 =⇒ 𝑥 1 : 𝜏1′ , . . . , 𝑥𝑛 : 𝜏𝑛′
                                                                                                                                                        (T-FunDef)
                                                                      Θ ⊢ 𝑓 ↦→ (𝑥 1 , . . . , 𝑥𝑛 )𝑒

                         dom(𝐷) = dom(Θ)                                                                            Θ⊢𝐷          ⊢WF Θ
      ∀𝑓 ↦→ (𝑥 1 , . . . , 𝑥𝑛 )𝑒 ∈ 𝐷.Θ ⊢ 𝑓 ↦→ (𝑥 1, . . . , 𝑥𝑛 )𝑒                                                   Θ | • ⊢ 𝑒 : 𝜏 =⇒ Γ
                                                                     (T-Funs)                                                                             (T-Prog)
                               Θ⊢𝐷                                                                                            ⊢ h𝐷, 𝑒i


                                                                 Figure 8. Program Typing Rules


                             // 𝑝 : (𝜆𝑖.{𝜈 : int | true}) ref { [0,𝑥 −1]↦→1}
𝑝 := 0;                      // 𝑝 : (𝜆𝑖.{𝜈 : int | 𝑖 = 0 ⇒ 𝜈 = 0}) ref { [0,𝑥 −1]↦→1}
let 𝑗 = 1 in                 // 𝑗 : {𝜈 : int | 𝜈 = 1}
let 𝑞 = 𝑝 ⊞ 𝑗 in             // 𝑝 : (𝜆𝑖.{𝜈 : int | 𝑖 = 0 ⇒ 𝜈 = 0}) ref {0↦→1} , 𝑞 : (𝜆𝑖.{𝜈 : int | ⊤}) ref { [0,𝑥 −2]↦→1}
let 𝑦 = 𝑥 − 𝑗 in             // 𝑦 : {𝜈 : int | 𝜈 = 𝑥 − 1}
let 𝑧 = init (𝑦, 𝑞) in       // 𝑝 : (𝜆𝑖.{𝜈 : int | 𝑖 = 0 ⇒ 𝜈 = 0}) ref {0↦→1} , 𝑞 : (𝜆𝑖.{𝜈 : int | 0 ≤ 𝑖 < 𝑥 − 2 ⇒ 𝜈 = 0}) ref { [0,𝑥 −2]↦→1}
alias(𝑞 = 𝑝 ⊞ 𝑗 );           // 𝑝 : (𝜆𝑖.{𝜈 : int | 0 ≤ 𝑖 ≤ 𝑥 − 1 ⇒ 𝜈 = 0}) ref { [0,𝑥 −1]↦→1}

                                                                 Figure 9. Typing for Example 2.1

type of 𝑝, by using T-AliasAddPtr (and the rule T-Sub for                               system ensures that no out-of-bound access occurs even though
subsumption).                                                                          memory safety is not the main focus of this paper.

Example 3.2. As mentioned, our type system supports ar-                                 Theorem 3.3 (Soundness). If ⊢ h𝐷, 𝑒i, then h∅, ∅, 𝑒i 6−→𝐷     +
rays of pointers, which are not supported by ConSORT. An                                AssertFail. Moreover, the reduction does not get stuck. That
example of a program manipulating such an array is given                                is, every well-typed program either (i) halts in a conﬁguration
in Figure 10. The function initMatrix takes integers 𝑥, 𝑦 and                           h𝑅, 𝐻, 𝑣i, where 𝑣 is either a variable or an integer, (ii) runs
a 𝑥 × 𝑦 matrix 𝑝 (represented as a pointer of a pointer) and                            into an AliasFail, or (iii) diverges.
initializes it as a zero matrix by using the running example
init. Some important type information is given as comments                                 Note that the type system does not guarantee the absence
to help readers understand how initMatrix is typed.                                    of AliasFail. It is the responsibility of the programmer or the
                                                                                        tool used for the alias analysis to ensure that the inserted
                                                                                        alias expressions are correct.
3.3     Soundness                                                                          The proof of soundness is by standard subject reduction
Our type system ensures that any typed program will never                               and progress lemmas. We deﬁne the notion of well-typed
experience an assertion failure. It also guarantees that a well-                        conﬁgurations, and prove that the reduction preserves the
typed program never gets stuck. This means that our type                                well-typedness. Roughly speaking, h𝑅, 𝐻, 𝑒i is well-typed if
                                                                                    8
Ownership Types for Verification of Programs with Pointer Arithmetic                                            Conference’17, July 2017, Washington, DC, USA



// initMatrix : h𝑥 : {𝜈 : int | ⊤}, 𝑦 : {𝜈 : int | ⊤}, 𝑝 : (𝜆𝑖.(𝜆 𝑗 .{𝜈 : int | ⊤}) ref { [0,𝑦−1]↦→1} ) ref { [0,𝑥 −1]↦→1} i
//               → h𝑥 : {𝜈 : int | ⊤}, 𝑦 : {𝜈 : int | ⊤}, 𝑝 : (𝜆𝑖.(𝜆 𝑗 .{𝜈 : int | 𝜑𝑝 }) ref { [0,𝑦−1]↦→1} ) ref { [0,𝑥 −1]↦→1} | {𝜈 : int | ⊤}i
//                        𝜑𝑝 = 0 ≤ 𝑖 ≤ 𝑥 − 1 ∧ 0 ≤ 𝑗 ≤ 𝑦 − 1 ⇒ 𝜈 = 0
initMatrix (𝑥, 𝑦, 𝑝){
     ifnp 𝑥 then 1 else
     let 𝑞 = ∗𝑝 in                            // 𝑞 : (𝜆 𝑗 .{𝜈 : int | true}) ref { [0,𝑦−1]↦→1}
     let 𝑧 = init (𝑦, 𝑞) in                   // 𝑞 : (𝜆 𝑗 .{𝜈 : int | 0 ≤ 𝑗 ≤ 𝑦 − 1 ⇒ 𝜈 = 0}) ref { [0,𝑦−1]↦→1}
     alias(𝑞 = ∗𝑝);                           // 𝑝 : (𝜆𝑖.(𝜆 𝑗 .{𝜈 : int | 𝑖 = 0 ∧ 0 ≤ 𝑗 ≤ 𝑦 − 1 ⇒ 𝜈 = 0}) ref { [0,𝑦−1]↦→1} ) ref { [0,𝑥 −1]↦→1}
                                                                                                                    ′
     let 𝑖 = 1 in let 𝑝 ′ = 𝑝 ⊞ 𝑖 in          // 𝑝 ′ : (𝜆𝑖.(𝜆 𝑗 .{𝜈 : int | true}) ref { [0,𝑦−1]↦→1} ) ref { [0,𝑥 −2]↦→1}
     let 𝑥 ′ = 𝑥 − 𝑖 in
                                                                                                                                                             ′
     let 𝑧 ′ = initMatrix (𝑥 ′, 𝑦, 𝑝 ′ ) in   // 𝑝 ′ : (𝜆𝑖.(𝜆 𝑗 .{𝜈 : int | 𝑖 = 0 ∧ 0 ≤ 𝑗 ≤ 𝑦 − 1 ⇒ 𝜈 = 0}) ref { [0,𝑦−1]↦→1} ) ref { [0,𝑥 −1]↦→1}
     alias(𝑝 ′ = 𝑝 ⊞ 𝑖);                      // 𝑝 : (𝜆𝑖.(𝜆 𝑗 .{𝜈 : int | 𝜑𝑝 }) ref { [0,𝑦−1]↦→1} ) ref { [0,𝑥 −1]↦→1}
     0}

                                                 Figure 10. An Example with Arrays of Pointers

(i) Θ | Γ ⊢ 𝑒 : 𝜏 =⇒ Γ ′ , (ii) each predicate formula 𝜑 appear-                   form [𝑐 0 +𝑐 1 𝑥 1 + · · · +𝑐 𝑘 𝑥𝑘 , 𝑑 0 +𝑑 1𝑥 1 + · · · +𝑑𝑘 𝑥𝑘 ] ↦→ 𝑜 where
ing in Γ satisﬁes |= [𝑅] [𝑅(𝑥)/𝜈]𝜑 (for an appropriate vari-                       𝑥 1, . . . , 𝑥𝑘 are the integer variables available in the context
able 𝑥), and (iii) the sum of the ownerships of pointers point-                    of the expression, and 𝑐 𝑖 , 𝑑𝑖 , 𝑜 are unknown constants. The
ing to (𝑎, 𝑖) does not exceed 1 for every (𝑎, 𝑖) ∈ dom(𝐻 ).                        goal of the ownership inference phase is to determine those
Details of the proof are found in Appendix B.                                      unknown constants so that all the ownership constraints in
                                                                                   the typing rules in Section 3 are satisﬁed. To this end, we
4      Type Inference                                                              ﬁrst generate constraints on the unknown constants based
This section describes a type inference procedure, which                           on the typing rules, and then solve them with a help of the
takes a program with no ownership/reﬁnement type anno-                             Z3 SMT solver.
tations as an input, and checks whether the program is well-                           We illustrate the constraint generation by using the run-
typed in our type system. Thanks to Theorem 3.3 in the pre-                        ning example.
vious section, the procedure serves as a sound (but incom-
                                                                                   Example 4.1. Let us consider the part 𝑝 := 0; let 𝑞 = 𝑝 ⊞
plete) method for automatically checking the lack of asser-
                                                                                   1 in · · · of the example in Figure 4. We prepare the following
tion failures. We assume below that the simple type (without
                                                                                   template of type environments for each program point:
ownerships and reﬁnement predicates) of each expression is
already known; it can be automatically obtained by the stan-                                       //𝑝 : 𝜆𝑖.int ref [𝑐 0,0 +𝑐 0,1 𝑥,𝑑0,0 +𝑑0,1𝑥 ]↦→𝑜 0
dard uniﬁcation-based simple type inference algorithm.                                             𝑝 := 0;
   Following ConSORT, the type inference proceeds in two
steps: the ﬁrst phase for ownership inference, and the sec-                                        // 𝑝 : 𝜆𝑖.int ref [𝑐 1,0 +𝑐 1,1 𝑥,𝑑1,0 +𝑑1,1 𝑥 ]↦→𝑜 1
ond phase for reﬁnement type inference. The ﬁrst phase                                             let 𝑞 = 𝑝 ⊞ 1 in
of ownership inference requires a signiﬁcant extension of
                                                                                                   // 𝑝 : 𝜆𝑖.int ref [𝑐 2,0 +𝑐 2,1 𝑥,𝑑2,0 +𝑑2,1 𝑥 ]↦→𝑜 2 ,
the ownership inference of ConSORT, as an ownership has
been extended from a single constant to a function that may                                        //𝑞 : 𝜆𝑖.int ref [𝑐 3,0 +𝑐 3,1 𝑥,𝑑3,0 +𝑑3,1 𝑥 ]↦→𝑜 3
depend on contexts.
                                                                                   From 𝑝 := 0, we generate the following constraints based
4.1 Ownership Inference                                                            on the rule T-Assign:
As mentioned earlier, we restrict an ownership to the form                                  𝑜 0 = 1 ∧ ∀𝑥 > 0.𝑐 0,0 + 𝑐 0,1 𝑥 ≤ 0 ≤ 𝑑 0,0 + 𝑑 0,1𝑥 .
[𝑙, 𝑢] ↦→ 𝑜, which represents the map 𝑓 such that 𝑓 (𝑖) = 𝑜 if                              ∀𝑥 > 0.𝑐 0,0 + 𝑐 0,1 𝑥 ≤ 𝑐 1,0 + 𝑐 1,1 𝑥
𝑙 ≤ 𝑖 ≤ 𝑢, and 𝑓 (𝑖) = 0 otherwise. As 𝑙 and 𝑢 may depend on
                                                                                                   ∧ 𝑑 1,0 + 𝑑 1,1 𝑥 ≤ 𝑑 0,0 + 𝑑 0,1𝑥 ∧ 𝑜 0 ≥ 𝑜 1 .
variables (recall that in the example in Figure 4, we needed
an ownership of the form [0, 𝑥 −1] ↦→ 1), for each expression                      Here, the constraint on the ﬁrst line requires that 𝑝 holds the
of a reference type, we prepare an ownership template of the                       full ownership at index 0. The condition 𝑥 > 0 comes from
                                                                               9
Conference’17, July 2017, Washington, DC, USA                                                                                                           Tanaka et al.


the fact that the expression occurs in the else clause of the                           undecidable in general). This phase is similar to that of Con-
conditional expression “ifnp 𝑥”.4 The constraint on the sec-                            SORT, except that we have more complex constraints due to
ond line requires that the ownership after the assignment                               the extension of reference types.
𝑝 := 0 is no greater than that before the assignment.                                     We explain more details by using the running example.
   From let 𝑞 = 𝑝 ⊞ 1 in · · ·, we generate the following con-
straints based on the rule T-AddPtr:                                                    Example 4.2. Recall the fragment 𝑝 := 0; let 𝑞 = 𝑝 ⊞1 in · · ·
                                                                                        of our running example. Based on the result of the owner-
        ∀𝑥 > 0.𝑐 1,0 + 𝑐 1,1 𝑥 ≤ 𝑐 2,0 + 𝑐 2,1 𝑥                                        ship inference in the previous phase, we can prepare the
             ∧ 𝑑 2,0 + 𝑑 2,1𝑥 ≤ 𝑑 1,0 + 𝑑 1,1𝑥 ∧ 𝑜 1 ≥ 𝑜 2 .                            following template for the type environment (which now in-
                                                                                        cludes reﬁnement type information) at each program point.
        ∀𝑥 > 0.𝑐 1,0 + 𝑐 1,1 𝑥 − 1 ≤ 𝑐 3,0 + 𝑐 3,1 𝑥
                ∧ 𝑑 3,0 + 𝑑 3,1𝑥 ≤ 𝑑 1,0 + 𝑑 1,1𝑥 − 1 ∧ 𝑜 1 ≥ 𝑜 3 .                                //𝑝 : (𝜆𝑖.{𝜈 : int | 𝑃0 (𝑥, 𝑖, 𝜈)}) ref [0,𝑥 −1]↦→1
        ∀𝑥 > 0.𝑜 1 ≥ 𝑜 2 + 𝑜 3 ∨                                                                   𝑝 := 0;
                     𝑑 3,0 + 𝑑 3,1𝑥 < 𝑐 2,0 + 𝑐 2,1 𝑥 − 1∨                                         // 𝑝 : (𝜆𝑖.{𝜈 : int | 𝑃1 (𝑥, 𝑖, 𝜈)}) ref [0,𝑥 −1]↦→1
                     𝑑 2,0 + 𝑑 2,1𝑥 − 1 < 𝑐 3,0 + 𝑐 3,1 𝑥 .                                        let 𝑞 = 𝑝 ⊞ 1 in
The constraints ensure that the sum of the ownerships of 𝑝                                         // 𝑝 : (𝜆𝑖.{𝜈 : int | 𝑃2 (𝑥, 𝑖, 𝜈)}) ref [0,0]↦→1,
and 𝑞 after the let-expression is no greater than the owner-                                       // 𝑞 : (𝜆𝑖.{𝜈 : int | 𝑃3 (𝑥, 𝑖, 𝜈)}) ref [0,𝑥 −2]↦→1
ship of 𝑝 before the expression.                          
                                                                                        From the assignment 𝑝 := 0, we generate the following con-
    As in the above example, we prepare a template of a type                            straints based on T-Assign:
environment (without reﬁnement type information) for each
program point, and generate the constraints based on the                                   ∀𝑥, 𝑖, 𝜈 .𝑥 > 0 ∧ 𝑖 = 0 ∧ 𝜈 = 0 ⇒ 𝑃1 (𝑥, 𝑖, 𝜈).
typing rules.
                                                                                           ∀𝑥, 𝑖, 𝜈 .𝑥 > 0 ∧ 0 < 𝑖 ≤ 𝑥 − 1 ∧ 𝑃0 (𝑥, 𝑖, 𝜈) ⇒ 𝑃1 (𝑥, 𝑖, 𝜈).
    It remains to solve the constraints on 𝑐 𝑖,𝑗 , 𝑑𝑖,𝑗 , 𝑜 𝑖 . Unfortu-
nately, the constraints involve nested quantiﬁers of the form                           The ﬁrst and second constraints respectively reﬂect the facts
∃𝑐 𝑖,𝑗 , 𝑑𝑖,𝑗 , 𝑜.∀𝑥 .𝜑, which cannot be solved eﬃciently by Z3.                        that the value of ∗𝑝 is 0 after the assignment, and that the
We have thus employed the following heuristic method to                                 values at other addresses are unchanged.
reduce the constraints further to the satisﬁability problem                               From the let-expression, we obtain the following constraints
for quantiﬁer-free formulas. Given a formula of the form                                based on T-AddPtr:
∃e𝑐 .∀e𝑥 .𝜓 (e    𝑥 ) (where e
               𝑐, e            𝑐 and e
                                     𝑥 denote sequences of variables),
we ﬁrst under-approximate it to ∃e           𝑐 .𝜓 (e  e1 ) ∧ · · · ∧ 𝜓 (e
                                                   𝑐, 𝑛                 𝑐, e
                                                                           𝑛𝑘 ),        ∀𝑥, 𝑖, 𝜈 .𝑥 > 0 ∧ 𝑃1 (𝑥, 0, 𝜈) ⇒ 𝑃2 (𝑥, 0, 𝜈)
where e                e𝑘 are randomly-chosen values for 𝑥e. We then
          𝑛 1, . . . , 𝑛                                                                ∀𝑥, 𝑖, 𝜈 .𝑥 > 0 ∧ 0 ≤ 𝑖 ≤ 𝑥 − 2 ∧ 𝑃1 (𝑥, 𝑖 + 1, 𝜈) ⇒ 𝑃3 (𝑥, 𝑖, 𝜈).
invoke an SMT solver (Z3 in our implementation) to obtain a
solution e    𝑐 =𝑚   e for the under-approximation. We then check                       The second constraint captures the fact that the value at 𝑞 +𝑖
whether the original formula ∀e                 ee
                                         𝑥 .𝜓 (𝑚,  𝑥 ) is valid by calling              corresponds to the one at 𝑝 + (𝑖 + 1).
an SMT solver. If so, we are done. Otherwise, we increase                                 In addition, we generate the following well-formedness
𝑘 to reﬁne the under-approximation, and repeat until a so-                              conditions (recall that at an index with no ownership, the
lution is found or an under-approximation is found to be                                reﬁnement type 𝜏 should satisfy Empty(𝜏)).
unsatisﬁable. It is left for future work to replace this heuris-
tic method with a more systematic, eﬃcient method.                                             ∀𝑥, 𝑖, 𝜈 .𝑥 > 0 ∧ (𝑖 < 0 ∨ 𝑖 > 𝑥 − 1) ⇒ 𝑃0 (𝑥, 𝑖, 𝜈)
                                                                                               ∀𝑥, 𝑖, 𝜈 .𝑥 > 0 ∧ (𝑖 < 0 ∨ 𝑖 > 𝑥 − 1) ⇒ 𝑃1 (𝑥, 𝑖, 𝜈)
4.2    Reﬁnement Inference                                                                     ∀𝑥, 𝑖, 𝜈 .𝑥 > 0 ∧ 𝑖 ≠ 0 ⇒ 𝑃2 (𝑥, 𝑖, 𝜈)
In the phase for reﬁnement type inference, we prepare a                                        ∀𝑥, 𝑖, 𝜈 .𝑥 > 0 ∧ (𝑖 < 0 ∨ 𝑖 > 𝑥 − 2) ⇒ 𝑃3 (𝑥, 𝑖, 𝜈)
predicate variable for each occurrence of integer type, and
generate constraints on the predicate variables. The gener-                             By solving the constraints on predicate variables by using a
ated constraints are in the form of Constrained Horn Clauses                            CHC solver, and substituting a solution for the templates of
(CHC) [2], which can be solved by using an oﬀ-the-shelf                                 types and type environments, we can obtain typing as given
CHC solver [4, 10, 14] (though the CHC solving problem is                               in Figure 4.5                                             

4 Currently, we locally collect such conditions from conditional expressions.           5We may obtain a slightly diﬀerent typing, depending on the solution found

Note that without the condition 𝑥 > 0, the co-eﬃcients 𝑐 0,1 and 𝑑 0,1 have             by a CHC solver; anyway, if the constraints are satisﬁable, we know that the
to be 0. For more precise analysis, we need to combine the ownership in-                given program is well-typed, hence also that the program does not suﬀer
ference and reﬁnement type inference phases.                                            from any assertion failures.
                                                                                   10
Ownership Types for Verification of Programs with Pointer Arithmetic                                           Conference’17, July 2017, Washington, DC, USA


4.3     Limitations                                                                   tool takes programs written in the language described in
In this subsection, we show programs that cannot be han-                              Section 2 as inputs. The tool ﬁrst inserts some trivial alias
dled by our current method. The ﬁrst example given below                              annotations automatically, by replacing let 𝑥 = 𝑦 ⊞ 𝑧 in 𝑒
comes from the restriction on the shape of ownership func-                            with let 𝑥 = 𝑦 ⊞ 𝑧 in let 𝑤 = 𝑒 in alias(𝑥 = 𝑦 ⊞ 𝑧); 𝑤.7 The
tions to [𝑙, 𝑢] ↦→ 𝑜.                                                                 tool then runs the type inference algorithm described in Sec-
                                                                                      tion 4 to statically checks lack of assertion failures. The cur-
Example 4.3 (Limitation caused by the restriction of own-                             rent tool does not support nested pointers. We used Z3 [6]
ership functions). Consider the following program.                                    version 4.11.2 as the backend SMT-solver, and HoIce [5] ver-
let 𝑝 = alloc 3 in           // 𝑝 : int ref { [0,2]↦→1}                               sion 1.10.0 as the backend CHC-solver.
                                                                                          The benchmark programs we prepared for evaluation are
let 𝑞 1 = 𝑝 ⊞ 1 in           // 𝑞 1 : int ref {0↦→1} , 𝑝 : int ref {0↦→1,2↦→1}
                                                                                      as follows:
𝑝 := 1;
                                                                                           • Init : The motivating program shown in Figure 4 in
𝑞 1 := 2;                                                                                    Section 1.
let 𝑞 2 = 𝑝 ⊞ 2 in           // 𝑞 2 : int ref {0↦→1} , 𝑝 : int ref {0↦→1}                  • Sum : A program to verify that the sum of the ele-
                                                                                             ments in an non-negative integer array remains non-
𝑞 2 := 3; ...
                                                                                             negative.
In order to type the program above, as indicated by the com-                               • Copy-Array : A program that copies array elements
ment on the second line, we have to assign to 𝑝 the owner-                                   to another array.
ship 𝑟 such that 𝑟 (0) = 1, 𝑟 (1) = 0, 𝑟 (2) = 1, which is not                             • Add-Array : A program that takes two integer arrays
supported by our type inference procedure.                                                  of the same size and writes the element-wise sum to
  The second example given below identiﬁes the limitation                                    another array.
caused by the lack of polymorphic function types.                                     Copy-Array and Add-Array were included as representa-
Example 4.4. Consider the following variation of the init                             tive programs that deal with multiple arrays. To make sure
function, where the ﬁrst argument 𝑥 has been replaced by a                            that our tool works equally well with diﬀerent array access
pointer 𝑥 𝑝 to an integer. In this case, the range of the own-                        patterns, we have prepared a few variants of Sum. The orig-
ership of 𝑝 depend on the value pointed to by 𝑥 𝑝 , which                             inal Sum (as well as the other programs listed above) ac-
cannot be expressed by our syntax of types.                                           cesses each element of the array from the front. The pro-
                                                                                      gram Sum-Back reads each element of the array from the
 init (𝑥 𝑝 , 𝑝){                                                                      back; Sum-Both accesses each element from both front and
 ifnp ∗𝑥 𝑝 then 1 else 𝑝 := 0; let 𝑞 = 𝑝 ⊞ 1 in 𝑥 𝑝 := ∗𝑥 𝑝 − 1;                      back at the same time; and Sum-Div divides the array into
 let 𝑧 = init (𝑥 𝑝 , 𝑞) in          // ∗𝑥 𝑝 = 𝑥 − 1                                   halves and calculates the summation recursively.8 The lengths
                                                                                      of arrays are ﬁxed to 1000 in all the programs we described
 alias(𝑞 = 𝑝 ⊞ 1); 1}
                                                                                      so far. To see how the length aﬀects the performance of our
To type the program above, we need to allow polymorphic                               tool, we also prepared a program Init-10 that is essentially
function types and assign the following type to init:                                 the same as Init but uses an array of length 10. Those bench-
∀𝑥 .h𝑥 𝑝 : (𝜆𝑖.{𝜈 : int | 𝜈 = 𝑥 }) ref {0↦→1} ,                                       mark programs are listed in Appendix C.
                                                                                          We compared the performance of our tool with SeaHorn
        𝑝 : (𝜆𝑖.{𝜈 : int | ⊤}) ref { [0,𝑥 −1]↦→1} i                                   (version 10.0.0-rc0-3bf79a59) [9], an existing CHC-based au-
→ h𝑥 𝑝 : (𝜆𝑖.{𝜈 : int | ⊤}) ref {0↦→1} ,                                              tomatic veriﬁer for C.9 The results of the experiments are
                                                                                      shown in Table 1. All the instances were run on a machine
        𝑝 : (𝜆𝑖.{𝜈 : int | 0 ≤ 𝑖 ≤ 𝑥 − 1 ⇒ 𝜈 = 0}) ref { [0,𝑥 −1]↦→1}                 with 16 GB RAM and Apple M2 CPUs, with a time out of
         | {𝜈 : int | ⊤}i.                                                            600 seconds. The table shows the running time in seconds
Although it is not diﬃcult to extend the type system itself,                          if the program was successfully veriﬁed.
the introduction of polymorphic types requires a signiﬁcant                               From these results, we conﬁrmed that our method can
extension of the type inference procedure, which is left for                          verify non-trivial programs that involve pointer arithmetic
future work.                                                                         within a realistic amount of time. The results also demon-
                                                                                      strate that the ownership functions of the form [𝑙, 𝑢] ↦→ 𝑜
5       Experiments                                                                   is not too restrictive.
We have implemented a prototype veriﬁer based on the meth-                            7 Note that the addition of alias annotations only increases the precision

ods outlined in Section 4 and conducted preliminary exper-                            of our type-based analysis. As reported below, thanks to the automatic in-
iments to conﬁrm the eﬀectiveness of our approach.6 Our                               sertion of alias expressions, no user annotations of alias expressions were
                                                                                      required in our experiments.
6 The     source    code   of     our   tool  is               available    at        8 Splitting an array to multiple arrays was not allowed in ConSORT.

https://github.com/mamizu-git/Extended_ConSORT                                        9 The input programs were manually translated into C for SeaHorn.

                                                                                 11
Conference’17, July 2017, Washington, DC, USA                                                                                                Tanaka et al.


Table 1. The results of the experiments. All times are in                     types, their type system distinguishes between concrete lo-
seconds.                                                                      cations and abstract locations, and allows strong updates for
                                                                              only concrete locations. To our knowledge, their type sys-
                   Ours                    SeaHorn                            tem does not support reﬁnement predicates that depend on
       Name       w/HoIce             w/HoIce w/Spacer                        an index to a memory region of variable length (such as “the
       Init-10     1.67              tool error   0.37                        𝑖-th element of a memory region pointed to by 𝑝 is no less
       Init        3.69               timeout   timeout                       than 𝑖”).
       Sum         2.01              tool error timeout                          In the context of separation logic, Calcagno et al. [3] pro-
       Sum-Back    0.54               timeout   timeout                       posed a shape analysis method in the presence of pointer
       Sum-Both    1.07               timeout   timeout                       arithmetic. To our knowledge, their method is specialized
       Sum-Div     0.83              tool error timeout                       for inferring shape information, and cannot be used for ver-
       Copy-Array  31.31              timeout   timeout                       ifying general properties of the contents stored in a memory
       Add-Array  338.30              timeout   timeout                       region.
                                                                                 There are a number of semi-automated approaches to ver-
                                                                              iﬁcation of pointer-manipulating programs [17–19, 22, 24].
   SeaHorn resulted in timeout for all benchmark programs,                    While those approaches cover a wider range of pointer op-
except for Init-10. This did not change even if we switched                   erations (such as XOR [22]) and computation models (in-
SeaHorn’s backend CHC-solver from Spacer [13] (which is                       cluding concurrency), they require much more human inter-
the default) to HoIce, which our tool uses. This is probably                  ventions, such as annotations of loop invariants and pre/-
because SeaHorn models the heap memory as an integer ar-                      post conditions for each recursive function. Furthermore,
ray and thus the resulting CHC problems involve predicates                    the main interests in many of those studies are in memory
on integer arrays. Thanks to our ownership types, the CHC                     safety and pointer races, while our interest is in the veriﬁ-
problems generated by our method are much easier to solve,                    cation of functional correctness (expressed by using asser-
involving only integer predicates.                                            tions) of low-level programs.
   The bottleneck of our approach is the heuristic used for
solving the formula of the shape ∃e             𝑐 , 𝑥e) in the own-
                                          𝑥 .𝜓 (e
                                      𝑐 .∀e                                   7 Conclusion
ership inference process, which we described in Section 4.
                                                                              We have proposed a type system for an imperative language
Our tool struggles to solve formulas of this shape and it may
                                                                              with pointer arithmetic, as an extension of the ownership
time out even if the formula is valid. This is more likely
                                                                              reﬁnement type system of ConSORT [23], and proved its
to occur when the number of pointers handled in a pro-
                                                                              soundness. We have implemented a prototype system for
gram increases. Indeed, Copy-Array, which manipulates
                                                                              fully automated veriﬁcation of programs with pointer arith-
two pointers, spends most of the time for the iteration that
                                                                              metic, and conﬁrmed its eﬀectiveness. Future work includes
generates the randomly-chosen values e                  e𝑘 for e
                                           𝑛 1, . . . , 𝑛      𝑥 . For
                                                                              an extension of the tool to support the full language (nested
the same reason, Add-Array, which manipulates three point-
                                                                              pointers, in particular), and an improvement of the eﬃciency
ers, needs even longer time to be veriﬁed.
                                                                              of the ownership inference procedure.
   As mentioned earlier, it is left for future work to imple-
ment more eﬃcient methods for solving formulas with quan-
tiﬁers of the form ∃∀.                                                        Acknowledgments
                                                                              We thank Ryosuke Sato for discussions on this work. We
6    Related Work                                                             would also like to thank anonymous referees for useful com-
We are not aware of so many studies on automated meth-                        ments. This work was supported by JSPS KAKENHI Grant
ods for static veriﬁcation of low-level programs with pointer                 Number JP20H05703.
arithmetic.
   As already mentioned in Section 1, our type system is an                   References
extension of that of ConSORT [23], which did not support                       [1] Thomas Ball, Byron Cook, Vladimir Levin, and Sriram K. Rajamani.
pointer arithmetic. Also, ConSORT supports arrays, but el-                         2004. SLAM and Static Driver Veriﬁer: Technology Transfer of Formal
                                                                                   Methods inside Microsoft. In Integrated Formal Methods 2004 (LNCS,
ements are restricted to integers (thus, arrays of pointers                        Vol. 2999). Springer, 1–20.
are not supported), and a pointer to an array must hold the                    [2] Nikolaj Bjørner, Arie Gurﬁnkel, Kenneth L. McMillan, and Andrey
ownership for the entire array ([23], Section 4.2).                                Rybalchenko. 2015. Horn Clause Solvers for Program Veriﬁcation. In
   Rondon et al. [20, 21] also developed a reﬁnement type                          Fields of Logic and Computation II - Essays Dedicated to Yuri Gurevich
system for a low-level language with reﬁnement types. It is                        on the Occasion of His 75th Birthday (LNCS, Vol. 9300). Springer, 24–51.
                                                                                   https://doi.org/10.1007/978-3-319-23534-9_2
diﬃcult to compare the approaches directly, as their mech-                     [3] Cristiano Calcagno, Dino Distefano, Peter W. O’Hearn, and Hongseok
anism for strong updates of reﬁnement types is diﬀerent                            Yang. 2006. Beyond Reachability: Shape Abstraction in the Presence of
from that of ConSORT and ours: instead of using ownership                          Pointer Arithmetic. In Static Analysis, 13th International Symposium,
                                                                         12
Ownership Types for Verification of Programs with Pointer Arithmetic                                         Conference’17, July 2017, Washington, DC, USA


     SAS 2006, Seoul, Korea, August 29-31, 2006, Proceedings (Lecture Notes         [15] K. Rustan M. Leino. 2010. Dafny: An Automatic Program Ver-
     in Computer Science, Vol. 4134), Kwangkeun Yi (Ed.). Springer, 182–203.             iﬁer for Functional Correctness. In Logic for Programming, Ar-
     https://doi.org/10.1007/11823230_13                                                 tiﬁcial Intelligence, and Reasoning - 16th International Confer-
 [4] Adrien Champion, Tomoya Chiba, Naoki Kobayashi, and Ryosuke                         ence, LPAR-16, Dakar, Senegal, April 25-May 1, 2010, Revised Se-
     Sato. 2020. ICE-Based Reﬁnement Type Discovery for Higher-Order                     lected Papers (Lecture Notes in Computer Science, Vol. 6355), Ed-
     Functional Programs. J. Autom. Reason. 64, 7 (2020), 1393–1418.                     mund M. Clarke and Andrei Voronkov (Eds.). Springer, 348–370.
     https://doi.org/10.1007/s10817-020-09571-y                                          https://doi.org/10.1007/978-3-642-17511-4_20
 [5] Adrien Champion, Naoki Kobayashi, and Ryosuke Sato. 2018. HoIce:               [16] Yusuke Matsushita, Takeshi Tsukada, and Naoki Kobayashi.
     An ICE-Based Non-linear Horn Clause Solver. In Programming Lan-                     2021.       RustHorn: CHC-based Veriﬁcation for Rust Programs.
     guages and Systems, Sukyoung Ryu (Ed.). Springer International Pub-                 ACM Trans. Program. Lang. Syst. 43, 4 (2021), 15:1–15:54.
     lishing, Cham, 146–156.                                                             https://doi.org/10.1145/3462205
 [6] Leonardo Mendonça de Moura and Nikolaj S. Bjørner. 2008. Z3:                   [17] Roland Meyer, Thomas Wies, and Sebastian Wolﬀ. 2023. Embedding
     An Eﬃcient SMT Solver. In Tools and Algorithms for the Construc-                    Hindsight Reasoning in Separation Logic. Proc. ACM Program. Lang.
     tion and Analysis of Systems, 14th International Conference, TACAS                  7, PLDI (2023), 1848–1871. https://doi.org/10.1145/3591296
     2008, Held as Part of the Joint European Conferences on Theory and             [18] Peter Müller, Malte Schwerhoﬀ, and Alexander J. Summers. 2017.
     Practice of Software, ETAPS 2008, Budapest, Hungary, March 29-April                 Viper: A Veriﬁcation Infrastructure for Permission-Based Rea-
     6, 2008. Proceedings (Lecture Notes in Computer Science, Vol. 4963),                soning.      In Dependable Software Systems Engineering, Alexan-
     C. R. Ramakrishnan and Jakob Rehof (Eds.). Springer, 337–340.                       der Pretschner, Doron Peled, and Thomas Hutzelmann (Eds.).
     https://doi.org/10.1007/978-3-540-78800-3_24                                        NATO Science for Peace and Security Series - D: Informa-
 [7] Jean-Christophe Filliâtre and Andrei Paskevich. 2013.            Why3               tion and Communication Security, Vol. 50. IOS Press, 104–125.
     - Where Programs Meet Provers. In Programming Languages                             https://doi.org/10.3233/978-1-61499-810-5-104
     and Systems - 22nd European Symposium on Programming, ESOP                     [19] Christopher Pulte, Dhruv C. Makwana, Thomas Sewell, Kayvan
     2013, Held as Part of the European Joint Conferences on Theory                      Memarian, Peter Sewell, and Neel Krishnaswami. 2023. CN: Verifying
     and Practice of Software, ETAPS 2013, Rome, Italy, March 16-24,                     Systems C Code with Separation-Logic Reﬁnement Types. Proc. ACM
     2013. Proceedings (Lecture Notes in Computer Science, Vol. 7792),                   Program. Lang. 7, POPL (2023), 1–32. https://doi.org/10.1145/3571194
     Matthias Felleisen and Philippa Gardner (Eds.). Springer, 125–128.             [20] Patrick Maxim Rondon, Alexander Bakst, Ming Kawaguchi, and Ran-
     https://doi.org/10.1007/978-3-642-37036-6_8                                         jit Jhala. 2012. CSolve: Verifying C with Liquid Types. In Computer
 [8] Arie Gurﬁnkel, Temesghen Kahsai, Anvesh Komuravelli, and                            Aided Veriﬁcation - 24th International Conference, CAV 2012, Berkeley,
     Jorge A. Navas. 2015.         The SeaHorn Veriﬁcation Framework.                    CA, USA, July 7-13, 2012 Proceedings (Lecture Notes in Computer Sci-
     In Computer Aided Veriﬁcation - 27th International Conference,                      ence, Vol. 7358), P. Madhusudan and Sanjit A. Seshia (Eds.). Springer,
     CAV 2015, San Francisco, CA, USA, July 18-24, 2015, Proceed-                        744–750. https://doi.org/10.1007/978-3-642-31424-7_59
     ings, Part I (Lecture Notes in Computer Science, Vol. 9206), Daniel            [21] Patrick Maxim Rondon, Ming Kawaguchi, and Ranjit Jhala.
     Kroening and Corina S. Pasareanu (Eds.). Springer, 343–361.                         2010. Low-level liquid types. In Proceedings of the 37th ACM
     https://doi.org/10.1007/978-3-319-21690-4_20                                        SIGPLAN-SIGACT Symposium on Principles of Programming
 [9] Arie Gurﬁnkel, Temesghen Kahsai, Anvesh Komuravelli, and Jorge A.                   Languages, POPL 2010, Madrid, Spain, January 17-23, 2010,
     Navas. 2015. The SeaHorn Veriﬁcation Framework. In Computer                         Manuel V. Hermenegildo and Jens Palsberg (Eds.). ACM, 131–
     Aided Veriﬁcation, Daniel Kroening and Corina S. Păsăreanu (Eds.).                  144. https://doi.org/10.1145/1706299.1706316
     Springer International Publishing, Cham, 343–361.                              [22] Michael Sammler, Rodolphe Lepigre, Robbert Krebbers, Kayvan
[10] H. Hojjat and P. Rümmer. 2018. The ELDARICA Horn Solver. In 2018                    Memarian, Derek Dreyer, and Deepak Garg. 2021. ReﬁnedC: au-
     Formal Methods in Computer Aided Design (FMCAD). 1–7.                               tomating the foundational veriﬁcation of C code with reﬁned owner-
[11] Temesghen Kahsai, Philipp Rümmer, Huascar Sanchez, and Mar-                         ship types. In PLDI ’21: 42nd ACM SIGPLAN International Conference
     tin Schäf. 2016. JayHorn: A Framework for Verifying Java pro-                       on Programming Language Design and Implementation, Virtual Event,
     grams. In Computer Aided Veriﬁcation - 28th International Con-                      Canada, June 20-25, 2021, Stephen N. Freund and Eran Yahav (Eds.).
     ference, CAV 2016, Toronto, ON, Canada, July 17-23, 2016, Pro-                      ACM, 158–174. https://doi.org/10.1145/3453483.3454036
     ceedings, Part I (Lecture Notes in Computer Science, Vol. 9779),               [23] John Toman, Ren Siqi, Kohei Suenaga, Atsushi Igarashi, and Naoki
     Swarat Chaudhuri and Azadeh Farzan (Eds.). Springer, 352–358.                       Kobayashi. 2020. ConSORT: Context- and Flow-Sensitive Own-
     https://doi.org/10.1007/978-3-319-41528-4_19                                        ership Reﬁnement Types for Imperative Programs. In Program-
[12] Naoki Kobayashi, Ryosuke Sato, and Hiroshi Unno. 2011. Predicate                    ming Languages and Systems - 29th European Symposium on Pro-
     abstraction and CEGAR for higher-order model checking. In Proceed-                  gramming, ESOP 2020, Held as Part of the European Joint Con-
     ings of the 32nd ACM SIGPLAN Conference on Programming Language                     ferences on Theory and Practice of Software, ETAPS 2020, Dublin,
     Design and Implementation, PLDI 2011, San Jose, CA, USA, June 4-                    Ireland, April 25-30, 2020, Proceedings (Lecture Notes in Com-
     8, 2011, Mary W. Hall and David A. Padua (Eds.). ACM, 222–233.                      puter Science, Vol. 12075), Peter Müller (Ed.). Springer, 684–714.
     https://doi.org/10.1145/1993498.1993525                                             https://doi.org/10.1007/978-3-030-44914-8_25
[13] Anvesh Komuravelli, Arie Gurﬁnkel, and Sagar Chaki. 2014. SMT-                 [24] Sebastian Wolﬀ. 2021. Verifying Non-blocking Data Structures with
     Based Model Checking for Recursive Programs. In Computer Aided                      Manual Memory Management. Ph. D. Dissertation. University of
     Veriﬁcation, Armin Biere and Roderick Bloem (Eds.). Springer Inter-                 Braunschwig.
     national Publishing, Cham, 17–34.
[14] Anvesh Komuravelli, Arie Gurﬁnkel, and Sagar Chaki. 2016. SMT-
     based model checking for recursive programs. Formal Methods Syst.
     Des. 48, 3 (2016), 175–205. https://doi.org/10.1007/s10703-016-0249-4




                                                                               13
Conference’17, July 2017, Washington, DC, USA                                                                                                Tanaka et al.


Appendices
    A     Well-formedness Conditions                                                                                                                   14
    B     Proof of Soundness                                                                                                                           14
    B.1      Conﬁguration Typing                                                                                                                       15
    B.2      Proof of Subject Reduction                                                                                                                18
    B.3      Proof of Progress                                                                                                                         28
    C     Benchmark Programs                                                                                                                           29

A Well-formedness Conditions
The well-formedness conditions for types and type environments are given in Figure 11.


                                                                                                       Empty(𝜏)        ∀𝑖 ∈ Z.𝑟 (𝑖) = 0
                                                           (Emp-Int)                                                                         (Emp-Ref)
                      Empty({𝜈 : int | ⊤})                                                                    Empty((𝜆𝑖.𝜏) ref 𝑟 )

                                                                  𝑥 ∉ 𝑑𝑜𝑚(Γ)
                                                               ⊢WF Γ     Γ ⊢WF 𝜏                                              Γ ⊢WF 𝜑
                             (WF-Empty)                                                   (WF-Env)                                             (WF-Int)
                  ⊢WF •                                             ⊢WF Γ, 𝑥 : 𝜏                                         Γ ⊢WF {𝜈 : int | 𝜑}


                             ∀𝑗 ∈ {𝑖 | 𝑟 (𝑖) = 0}∃𝜏 ′ .𝐸𝑚𝑝𝑡𝑦(𝜏 ′ ), • ⊢ 𝜏 ′ ≈ [ 𝑗 /𝑖]𝜏 ∀𝑗 ∈ Z.Γ ⊢WF [ 𝑗 /𝑖]𝜏
                                                ∀𝑥 ∈ FV(𝑟 ).Γ(𝑥) = {𝜈 : int | 𝜑}, Γ ⊢WF 𝜑
                                                                                                                                               (WF-Ref)
                                                                  Γ ⊢WF (𝜆𝑖.𝜏) ref 𝑟


                                            ∀𝑥 ∈ FV(𝜑) \ {𝜈 }.Γ(𝑥) = {𝜈 : int | 𝜑 ′ }, Γ ⊢WF 𝜑 ′
                                                                                                                                               (WF-Phi)
                                                                        Γ ⊢WF 𝜑

                                                                Γ ⊢WF 𝜏            ⊢WF Γ
                                                                                                                                           (WF-Result)
                                                                     ⊢WF 𝜏 =⇒ Γ

                                                            ⊢WF 𝑥 1 : 𝜏1, . . . , 𝑥𝑛 : 𝜏𝑛
                                                          ⊢WF 𝜏 =⇒ 𝑥 1 : 𝜏1′ , . . . , 𝑥𝑛 : 𝜏𝑛′
                                                                                                                                          (WF-FunType)
                                           ⊢WF h𝑥 1 : 𝜏1 , . . . , 𝑥𝑛 : 𝜏𝑛 i → h𝑥 1 : 𝜏1′ , . . . , 𝑥𝑛 : 𝜏𝑛′ | 𝜏i


                                                            ∀𝑓 ∈ 𝑑𝑜𝑚(Θ). ⊢WF Θ(𝑓 )
                                                                                                                                          (WF-FunEnv)
                                                                         ⊢WF Θ


                                                          Figure 11. Well-formedness


B    Proof of Soundness
This section proves the soundness of our type system. Our proof strategy follows that for the soundness proof of the type
system of ConSORT [23]. At a very high-level, what we prove are (1) a lemma that states (assert) failure cannot be typed, (2)
subject reduction (for conﬁgurations) and (3) a standard progress lemma:
Lemma B.1. If ⊢ h𝐷, 𝑒i, then ⊢𝐷 h∅, ∅, 𝑒i : 𝜏 =⇒ Γ ′ for some 𝜏 and Γ ′ .

Lemma B.2. If ⊢𝐷 h𝑅, 𝐻, 𝑒i : 𝜏 =⇒ Γ ′ , then h𝑅, 𝐻, 𝑒i 6−→𝐷 AssertFail.

                                                                            14
Ownership Types for Verification of Programs with Pointer Arithmetic                                          Conference’17, July 2017, Washington, DC, USA


                                 def
                                              Õ
                Own(𝐻, 𝑅, Γ) =                      own(𝐻, 𝑅, 𝑅(𝑥), Γ(𝑥))
                                       𝑥 ∈𝑑𝑜𝑚 (Γ)
                                       (                                           Í
                                           {(𝑎, 𝑖 + 𝑗 ) ↦→ [𝑅]𝑟 ( 𝑗 ) | 𝑗 ∈ Z} +                                             ′    if (♠)
                                 def                                                   𝑗 ∈Z own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏 )
              own(𝐻, 𝑅, 𝑣, 𝜏) =
                                           0                                                                                      otherwise
                                         (♠) 𝑣 = (𝑎, 𝑖), (𝑎, 𝑖) ∈ 𝑑𝑜𝑚(𝐻 ) and 𝜏 = (𝜆𝑖.𝜏 ′ ) ref 𝑟
                                  def
                SAT(𝐻, 𝑅, Γ) ⇐⇒ ∀𝑥 ∈ 𝑑𝑜𝑚(Γ).𝑥 ∈ dom(𝑅) and SATv(𝐻, 𝑅, 𝑅(𝑥), Γ(𝑥))
                SATv(𝐻, 𝑅, 𝑣, 𝜏)
                      
                       1. 𝑣 ∈ Z, 𝜏 = {𝜈 : int | 𝜑} and |= [𝑅] [𝑣/𝜈]𝜑 or
                      
                      
                     def
                    ⇐⇒ 2. 𝑣 = (𝑎, 𝑖), 𝜏 = (𝜆𝑖.𝜏 ′ ) ref 𝑟 , (𝑎, 𝑖) ∈ 𝑑𝑜𝑚(𝐻 ) and
                      
                      
                            ∀𝑗 ∈ {𝑖 | [𝑅]𝑟 (𝑖) > 0}.(𝑎, 𝑖 + 𝑗 ) ∈ dom(𝐻 ) and SATv(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏 ′ )



                                                       Figure 12. Deﬁnition of the invariants.

Lemma B.3 (Subject reduction). If ⊢𝐷 h𝑅, 𝐻, 𝑒i : 𝜏 =⇒ Γ ′ and h𝑅, 𝐻, 𝑒i −→𝐷 C, then either
   • C = AliasFail or
   • C = h𝑅 ′ , 𝐻 ′ , 𝑒 ′ i with ⊢𝐷 h𝑅 ′ , 𝐻 ′ , 𝑒 ′ i : 𝜏 =⇒ Γ ′ .

Lemma B.4 (Progress). Suppose ⊢𝐷 h𝑅, 𝐻, 𝑒i : 𝜏 =⇒ Γ ′ . Then either
  1. h𝑅, 𝐻, 𝑒i −→𝐷 h𝑅 ′ , 𝐻 ′ , 𝑒 ′ i holds for some conﬁguration h𝑅 ′ , 𝐻 ′ , 𝑒 ′ i,
  2. h𝑅, 𝐻, 𝑒i −→𝐷 AliasFail, or
  3. h𝑅, 𝐻, 𝑒i is of the form h𝑅, 𝐻, 𝑣i, where 𝑣 is some variable 𝑥 or an integer 𝑛 (and thus cannot be reduced anymore).
   The deﬁnition of ⊢𝐷 h𝑅, 𝐻, 𝑒i : 𝜏 =⇒ Γ ′ will be given later in this section.
  From these lemmas, we obtain the following soundness result by a straightforward inductive argument.
Theorem 3.3 (Soundness). If ⊢ h𝐷, 𝑒i, then h∅, ∅, 𝑒i 6−→𝐷  + AssertFail. Moreover, the reduction does not get stuck. That is, every

well-typed program either (i) halts in a conﬁguration h𝑅, 𝐻, 𝑣i, where 𝑣 is either a variable or an integer, (ii) runs into an AliasFail,
or (iii) diverges.
  The rest of this section is organized as follows. Section B.1 deﬁnes the judgement ⊢𝐷 h𝑅, 𝐻, 𝑒i : 𝜏 =⇒ Γ ′ and proves
Lemma B.1 and B.2. Section B.2 proves subject reduction after proving some additional lemmas. Section B.3 proves progress.

B.1 Conﬁguration Typing
Here we deﬁne the type judgement for conﬁgurations ⊢𝐷 h𝑅, 𝐻, 𝑒i : 𝜏 =⇒ Γ ′ and prove some basic properties about well-typed
conﬁgurations.
Deﬁnition B.5 (Well-typed conﬁguration). Given a conﬁguration h𝑅, 𝐻, 𝑒i, we write ⊢𝐷 h𝑅, 𝐻, 𝑒i : 𝜏 =⇒ Γ ′ if the following
conditions hold for some type environment Γ and function type environment Θ:
   1. Θ | Γ ⊢ 𝑒 : 𝜏 → Γ ′ and Θ ⊢ 𝐷
   2. for each (𝑎, 𝑖) ∈ dom(𝐻 ), Own(𝐻, 𝑅, Γ) ≤ 1
   3. SAT(𝐻, 𝑅, Γ)
where Own(𝐻, 𝑅, Γ) and SAT(𝐻, 𝑅, Γ) are deﬁned in Figure 12. We say that a conﬁguration h𝑅, 𝐻, 𝑒i is well-typed if there exist
𝜏 and Γ ′ such that ⊢𝐷 h𝑅, 𝐻, 𝑒i : 𝜏 =⇒ Γ ′ .
  The expression 0 in the deﬁnition of own(𝐻, 𝑅, 𝑣, 𝜏) represents the constant function that always returns 0, and the function
{(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 ( 𝑗 ) | 𝑗 ∈ Z} returns 0 if the argument is not of the form (𝑎, 𝑗 ). The addition of functions is deﬁned pointwise.
As we already mentioned, [𝑅]𝜑 represents the formula obtained by replacing each variable 𝑥 (of type int) in 𝜑 with 𝑅(𝑥).
Formally, it is inductively deﬁned as follows:
                                        def                          def                                            def
                              [∅]𝜑 = 𝜑              [𝑅{𝑦 ↦→ 𝑛}]𝜑 = [𝑅] [𝑛/𝑦]𝜑                  [𝑅{𝑦 ↦→ (𝑎, 𝑖)}]𝜑 = [𝑅]𝜑.
                                                                             15
Conference’17, July 2017, Washington, DC, USA                                                                                                       Tanaka et al.


Similarly, [𝑅]𝑟 is the ownership function obtained by instantiating the free variables of 𝑟 using 𝑅. Hence, [𝑅]𝑟 is a function
from Z to [0, 1]. To simplify the, notation we often omit [𝑅] and write 𝑟 even if we mean [𝑅]𝑟 .
   Now we brieﬂy explain Own and SAT. The function own(𝐻, 𝑅, 𝑣, 𝜏) maps an address (𝑎, 𝑖) to the hereditary ownership of
(𝑎, 𝑖) that 𝑣 : 𝜏 owns. By hereditary, we mean that if 𝑣 is a pointer of a pointer, then 𝑣 also owns the ownership of ∗𝑣, and so
on.10 It should be emphasized that own(𝐻, 𝑅, (𝑎, 𝑖), (𝜆𝑖.𝜏) ref 𝑟 ) is not focusing on a single memory cell whose address is (𝑎, 𝑖),
but is describing the hereditary ownership that the chunk of memory starting from (𝑎, 𝑖) has. On the other hand, intuitively,
SATv(𝐻, 𝑅, 𝑣, 𝜏) checks whether “𝑣 has the type 𝜏” under 𝐻 and 𝑅. For example, SATv(𝐻, 𝑅, 𝑣, {𝜈 : int | 𝜑}) holds if and only
if 𝑣 is an integer that satisﬁes the predicate [𝑅]𝜑. In case 𝜏 = (𝜆𝑖.𝜏 ′ ) ref 𝑟 , SATv not only checks that 𝑣 is an address, but also
checks that out-of-bounds access does not occur. The conditions ∀(𝑎, 𝑖) ∈ dom(𝐻 ).Own(𝐻, 𝑅, Γ) (𝑎, 𝑖) ≤ 1 and SAT(𝐻, 𝑅, Γ)
are the two invariants that will not change during the reduction. (Note, however, that the type environment Γ appearing in
these expressions may change during reductions.)
   We now prove Lemma B.1 and B.2, i.e all the lemmas we used to prove the soundness, except for subject reduction.
Lemma B.1. If ⊢ h𝐷, 𝑒i, then ⊢𝐷 h∅, ∅, 𝑒i : 𝜏 =⇒ Γ ′ for some 𝜏 and Γ ′ .
Proof. First, observe that Own(𝐻, 𝑅, •) = 0 and SAT(𝐻, 𝑅, •) holds for any heap 𝐻 and register ﬁle 𝑅; in particular, we
have Own(∅, ∅, •) = 0 and SAT(∅, ∅, •) holds. Since ⊢ h𝐷, 𝑒i, we have Θ | • ⊢ 𝑒 : 𝜏 =⇒ Γ ′ for some 𝜏 and Γ ′ , and thus
⊢𝐷 h∅, ∅, 𝑒i : 𝜏 =⇒ Γ ′ .                                                                                              
  The claim that AssertFail never happens (Lemma B.2) should be intuitively evident as SAT(𝐻, 𝑅, Γ) ensures that all the
reﬁnement predicates are valid. To formally prove this claim, we also need to prove that SAT(𝐻, 𝑅, Γ) is preserved by subtyp-
ing.11
Lemma B.6. If SAT(𝐻, 𝑅, Γ), then |= [𝑅]JΓK.
Proof. By the deﬁnition of JΓK, it suﬃces to show that Γ(𝑥) = {𝜈 : int | 𝜑} implies |= [𝑅] [𝑥/𝜈]𝜑. This clearly is the case
because SATv(𝐻, 𝑅, 𝑅(𝑥), {𝜈 : int | 𝜑}) implies |= [𝑅] [𝑅(𝑥)/𝜈]𝜑 (= [𝑅] [𝑥/𝜈]𝜑).                                          
Lemma B.7. If Γ ⊢ 𝜏 ≤ 𝜏 ′ , |= [𝑅]JΓK and SATv(𝐻, 𝑅, 𝑣, 𝜏) then SATv(𝐻, 𝑅, 𝑣, 𝜏 ′ ).
Proof. By induction on the derivation of Γ ⊢ 𝜏 ≤ 𝜏 ′ . The base case is when 𝜏 = {𝜈 : int | 𝜑} and 𝜏 ′ = {𝜈 : int | 𝜑 ′ } with
|= JΓK ⇒ 𝜑 ⇒ 𝜑 ′ . This means that we have |= [𝑅]JΓK ⇒ [𝑅] [𝑣/𝜈]𝜑 ⇒ [𝑅] [𝑣/𝜈]𝜑 ′ , by taking 𝑅{𝜈 ↦→ 𝑣 } as the valuation. By
SATv(𝐻, 𝑅, 𝑣, 𝜏), we have [𝑅] [𝑣/𝜈]𝜑. Together with |= [𝑅]JΓK, we have [𝑅] [𝑣/𝜈]𝜑 ′ , i.e. SATv(𝐻, 𝑅, 𝑣, 𝜏 ′ ).
   The inductive case is the case where 𝜏 = (𝜆𝑖.𝜏1 ) ref 𝑟 1 and 𝜏 ′ = (𝜆𝑖.𝜏2 ) ref 𝑟 2 with 𝑟 1 ≥ 𝑟 2 and Γ ⊢ 𝜏1 ≤ 𝜏2 . Assume that 𝑣 is
an address (𝑎, 𝑖); otherwise it is trivial. Our goal is to show that SATv(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏2) for 𝑗 such that 𝑟 2 ( 𝑗 ) > 0. Note
that if 𝑟 2 ( 𝑗 ) > 0 then so is 𝑟 1 ( 𝑗 ) because 𝑟 1 ≥ 𝑟 2 . From SATv(𝐻, 𝑅, 𝑣, 𝜏), we have SATv(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏1 ). By applying
the induction hypothesis we obtain SATv(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏2 ).12                                                                    
Lemma B.8. If Γ ⊢ 𝜏 ≤ 𝜏 ′ and |= [𝑅]JΓK, then own(𝐻, 𝑅, 𝑣, 𝜏) ≥ own(𝐻, 𝑅, 𝑣, 𝜏 ′ ).
Proof. By induction on the derivation of Γ ⊢ 𝜏 ≤ 𝜏 ′ . The base case is trivial as the two ownership functions are the constant
function 0. The inductive case is the case where 𝜏 = (𝜆𝑖.𝜏1 ) ref 𝑟 1 and 𝜏 ′ = (𝜆𝑖.𝜏2 ) ref 𝑟 2 with 𝑟 1 ≥ 𝑟 2 and Γ ⊢ 𝜏1 ≤ 𝜏2 . We
suppose that 𝑣 is an address (𝑎, 𝑖) because, if not, it is trivial. We have
                                                                         Õ
             own(𝐻, 𝑅, (𝑎, 𝑖), 𝜏) = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 1 ( 𝑗 ) | 𝑗 ∈ Z} +   own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏1)              (by def.)
                                                                                   𝑗 ∈Z
                                                                                   Õ
                                          ≥ {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 1 ( 𝑗 ) | 𝑗 ∈ Z} +          own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏2)                          (by I.H.)
                                                                                   𝑗 ∈Z
                                                                                   Õ
                                          ≥ {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 2 ( 𝑗 ) | 𝑗 ∈ Z} +          own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏2)                   (since 𝑟 1 ≥ 𝑟 2 )
                                                                                   𝑗 ∈Z
                                          = own(𝐻, 𝑅, (𝑎, 𝑖), 𝜏 ′ )
as desired.                                                                                                                                                    
10 Dereferencing ∗𝑣 corresponds to 𝐻 (𝑎, 𝑖 ) provided that 𝑣 = (𝑎, 𝑖 ).
11We also prove that Own(𝐻, 𝑅, Γ) (𝑎, 𝑖 ) ≤ 1 is preserved by subtyping even if this is not needed to prove Lemma B.2. This is a property that we use later

in this section.
12 Strictly speaking, we also need a substitution lemma for the subtyping relation to show Γ ⊢ [ 𝑗 /𝑖 ]𝜏
                                                                                                           1 ≤ [ 𝑗 /𝑖 ]𝜏2 . This can be proved by induction on the
subtyping relation.
                                                                              16
Ownership Types for Verification of Programs with Pointer Arithmetic                                Conference’17, July 2017, Washington, DC, USA


Lemma B.9. Suppose that Γ ≤ Γ ′ and SAT(𝐻, 𝑅, Γ).
    1. We have SAT(𝐻, 𝑅, Γ ′ ) and
    2. if Own(𝐻, 𝑅, Γ) (𝑎, 𝑖) ≤ 1, then Own(𝐻, 𝑅, Γ ′ ) (𝑎, 𝑖) ≤ 1 for all (𝑎, 𝑖) ∈ dom(𝐻 ).

Proof.
    1. Follows from Lemma B.6 and B.7.
    2. Follows from Lemma B.6 and B.8.
                                                                                                                                               

Lemma B.2. If ⊢𝐷 h𝑅, 𝐻, 𝑒i : 𝜏 =⇒ Γ ′ , then h𝑅, 𝐻, 𝑒i 6−→𝐷 AssertFail.

Proof. Suppose that h𝑅, 𝐻, assert(𝜑); 𝑒 0 i −→𝐷 AssertFail. Then we must have 6 |= [𝑅]𝜑. Our goal is to show that |= [𝑅]𝜑, which
leads to a contradiction. Since ⊢𝐷 h𝑅, 𝐻, assert(𝜑); 𝑒 0 i, we must have Θ | Γ ⊢ assert(𝜑); 𝑒 0 : 𝜏 =⇒ Γ ′ and SAT(𝐻, 𝑅, Γ) for
some Γ. By inversion on the typing of assert(𝜑); 𝑒 0 , we have |= JΓ0 K =⇒ 𝜑 for some Γ0 such that Γ ≤ Γ0 . Using Lemma B.9
with SAT(𝐻, 𝑅, Γ), we obtain SAT(𝐻, 𝑅, Γ0 ). Therefore, we have |= [𝑅]JΓ0 K by Lemma B.6, and thus, |= [𝑅]𝜑.                   

Auxiliary lemmas about the invariants. The rest of this subsection is devoted to the proofs of auxiliary lemmas about
the invariants that are used to prove subject reduction. All the lemmas proved here are quite simple. We do not prove any
lemmas that have to do with the dynamics of a program; such lemmas will be proved later in Section B.2.

Lemma B.10. Suppose that own(𝐻, 𝑅, (𝑎 ′ , 𝑖 ′ ), (𝜆𝑖.𝜏) ref 𝑟 ) (𝑎, 𝑖) = 0 and 𝑟 ( 𝑗 ) > 0. Then (𝑎, 𝑖) ≠ (𝑎 ′ , 𝑖 ′ + 𝑗 ).

Proof. Obvious from the deﬁnition of own.                                                                                                      

                                                                                                                    def                       def
  By abuse of notation, we write ⊤ for types 𝜏 that satisfy Empty(𝜏). Moreover, we deﬁne ⊤0 = {𝜈 : int | ⊤}, ⊤𝑚 =
(𝜆𝑖.⊤𝑚−1 ) ref 0 .

Lemma B.11. For all 𝐻 , 𝑣 and 𝑛 we have own(𝐻, 𝑅, 𝑣, ⊤𝑛 ) = 0.

Proof. By induction on 𝑛.                                                                                                                      

Lemma B.12. For any 𝐻 , 𝑅 and 𝑣, we have that
    1. if 𝑣 is an integer, then SATv(𝐻, 𝑅, 𝑣, ⊤0 ), and
    2. if 𝑣 is an address with 𝑣 ∈ dom(𝐻 ), then SATv(𝐻, 𝑅, 𝑣, ⊤𝑛 ) for any 𝑛 ≥ 1.

Proof. By induction on 𝑛.                                                                                                                      

  Lemma B.13 shows that type equivalence preserves own and SATv and Lemma B.14 states that strengthening operation
does not aﬀect own.

Lemma B.13. Suppose that Γ ⊢ 𝜏1 ≈ 𝜏2 and |= [𝑅]JΓK. Then
    1. own(𝐻, 𝑅, 𝑣, 𝜏1 ) = own(𝐻, 𝑅, 𝑣, 𝜏2 ) and
    2. SATv(𝐻, 𝑅, 𝑣, 𝜏1 ) if and only if SATv(𝐻, 𝑅, 𝑣, 𝜏2 ).

Proof. By Lemma B.7 and B.8.                                                                                                                   

Lemma B.14. For any 𝜑 and 𝑥, we have own(𝐻, 𝑅, 𝑣, 𝜏) = own(𝐻, 𝑅, 𝑣, 𝜏 ∧𝑥 𝜑).

Proof. By straightforward induction on the structure of 𝜏.                                                                                     

  The following lemmas say that own and SATv can be “split” in accordance with type splitting.

Lemma B.15. If 𝜏 = 𝜏1 + 𝜏2 , we have own(𝐻, 𝑅, 𝑣, 𝜏) = own(𝐻, 𝑅, 𝑣, 𝜏1 ) + own(𝐻, 𝑅, 𝑣, 𝜏2 ).

Proof. By induction on the rules used to derive 𝜏 = 𝜏1 + 𝜏2 . The base case where 𝜏1 = {𝜈 : int | 𝜑 1 } and 𝜏2 = {𝜈 : int | 𝜑 2 } is
trivial because own(𝐻, 𝑅, 𝑣, 𝜏1 + 𝜏2 ) = own(𝐻, 𝑅, 𝑣, 𝜏1 ) = own(𝐻, 𝑅, 𝑣, 𝜏2 ) = 0.
                                                                       17
Conference’17, July 2017, Washington, DC, USA                                                                                                     Tanaka et al.


  The inductive case is the case where 𝜏1 = (𝜆𝑖.𝜏1′ ) ref 𝑟 1 , 𝜏2 = (𝜆𝑖.𝜏2′ ) ref 𝑟 2 and 𝜏 = (𝜆𝑖.𝜏1′ + 𝜏2′ ) ref 𝑟 1 +𝑟 2 . We only consider the
case where 𝑣 is an address (𝑎, 𝑖) and is in dom(𝐻 ); remaining cases are trivial as the own functions become 0. We have
                               own(𝐻, 𝑅, 𝑣, 𝜏1 ) + own(𝐻, 𝑅, 𝑣, 𝜏2 )
                                                                       Õ
                                = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 1 ( 𝑗 ) | 𝑗 ∈ Z} +   own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏1′ )
                                                                           𝑗
                                                                           Õ
                                  + {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 2 ( 𝑗 ) | 𝑗 ∈ Z} +            own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏2′ )
                                                                               𝑗
                                = {(𝑎, 𝑖 + 𝑗 ) ↦→ (𝑟 1 + 𝑟 2 ) ( 𝑗 ) | 𝑗 ∈ Z}
                                   Õ                                                                                   
                                 +       own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏1′ ) + own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏2′ )
                                      𝑗
                                = {(𝑎, 𝑖 + 𝑗 ) ↦→ (𝑟 1 + 𝑟 2 ) ( 𝑗 ) | 𝑗 ∈ Z}
                                   Õ
                                 +      own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖] (𝜏1′ + 𝜏2′ ))                                                              (by I.H.)
                                      𝑗
                                = own(𝐻, 𝑅, 𝑣, (𝜆𝑖.𝜏1′ + 𝜏2′ ) ref 𝑟 1 +𝑟 2 ) = own(𝐻, 𝑅, 𝑣, 𝜏).
                                                                                                                                                            
Lemma B.16. If 𝜏 = 𝜏1 + 𝜏2 , we have SATv(𝐻, 𝑅, 𝑣, 𝜏) iﬀ SATv(𝐻, 𝑅, 𝑣, 𝜏1 ) and SATv(𝐻, 𝑅, 𝑣, 𝜏2 ).
Proof. By induction on the rules used to derive 𝜏 = 𝜏1 + 𝜏2 . The base case is the case where 𝜏1 = {𝜈 : int | 𝜑 1 }, 𝜏2 = {𝜈 : int | 𝜑 2 }
and 𝜏 = {𝜈 : int | 𝜑 1 ∧ 𝜑 2 }. From the deﬁnition of SATv, it suﬃces to show that |= [𝑅] [𝑣/𝜈] (𝜑 1 ∧ 𝜑 2 ) iﬀ |= [𝑅] [𝑣/𝜈]𝜑 1 and
|= [𝑅] [𝑣/𝜈]𝜑 2 . This is obvious because [𝑅] [𝑣/𝜈] (𝜑 1 ∧ 𝜑 2 ) = [𝑅] [𝑣/𝜈]𝜑 1 ∧ [𝑅] [𝑣/𝜈]𝜑 2 .
   We now consider the inductive case where 𝜏1 = (𝜆𝑖.𝜏1′ ) ref 𝑟 1 , 𝜏2 = (𝜆𝑖.𝜏2′ ) ref 𝑟 2 and 𝜏 = (𝜆𝑖.𝜏1′ + 𝜏2′ ) ref 𝑟 1 +𝑟 2 . We only prove
the only if direction; the other direction is somewhat symmetric. Since SATv(𝐻, 𝑅, 𝑣, 𝜏), 𝑣 must be an address (𝑎, 𝑖) and we
have
                                                                  (𝑎, 𝑖) ∈ dom(𝐻 )                                                                         (1)
               (𝑎, 𝑖 + 𝑗 ) ∈ dom(𝐻 ) and SATv(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖] (𝜏1′ + 𝜏2′ ))               (for 𝑗 such that (𝑟 1 + 𝑟 2 ) ( 𝑗 ) > 0)            (2)
From (2) and the induction hypothesis, we have
                                 SATv(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏1′ )        and SATv(𝐻, 𝑅, (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏2′ )
for each 𝑗 that satisﬁes (𝑟 1 +𝑟 2 ) ( 𝑗 ) > 0. In particular, for 𝑙 ∈ {1, 2}, we have SATv(𝐻, 𝑅, (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏𝑙′ ) and (𝑎, 𝑖 + 𝑗 ) ∈ dom(𝐻 )
for each 𝑗 such that 𝑟𝑙 ( 𝑗 ) > 0. Hence, we have SATv(𝐻, 𝑅, 𝑣, (𝜆𝑖.𝜏1′ ) ref 𝑟 1 ) and SATv(𝐻, 𝑅, 𝑣, (𝜆𝑖.𝜏2′ ) ref 𝑟 2 ) as desired.              

B.2    Proof of Subject Reduction
This subsection is divided into two parts: the ﬁrst part proves additional lemmas about own and SATv, and the second part
gives the main proof of subject reduction. As usual, the main part of the proof of subject reduction is an inductive proof on
the transition relation. The lemmas we prepare in the ﬁrst part are lemmas that are used in the cases for the transition rules
that update the heap 𝐻 or the register ﬁle 𝑅 (e.g. R-Assign).
B.2.1 Preservation properties under modiﬁcations of heaps and register ﬁles. We deﬁne a relation that expresses
that a heap is obtained by modifying a single cell of another heap.
Deﬁnition B.17. Two heaps 𝐻 and 𝐻 ′ are equivalent modulo (𝑎, 𝑖), written 𝐻 ≈ (𝑎,𝑖 ) 𝐻 ′ if:
  1. 𝑑𝑜𝑚(𝐻 ) = 𝑑𝑜𝑚(𝐻 ′ )
  2. ∀(𝑎 ′ , 𝑖 ′ ) ∈ 𝑑𝑜𝑚(𝐻 ).(𝑎 ′ , 𝑖 ′ ) ≠ (𝑎, 𝑖) ⇒ 𝐻 (𝑎 ′ , 𝑖 ′ ) = 𝐻 ′ (𝑎 ′ , 𝑖 ′ )
   Of course, own(𝐻, 𝑅, 𝑣, 𝜏) nor SATv(𝐻, 𝑅, 𝑣, 𝜏) is not preserved under modiﬁcations of the heap 𝐻 if 𝑣 (directly or indirectly)
refers to the modiﬁed address. However, if 𝑣 does not own the cell that has been modiﬁed, then own and SATv are preserved.


Lemma B.18. If 𝐻 ≈ (𝑎,𝑖 ) 𝐻 ′ and own(𝐻, 𝑅, 𝑣, 𝜏) (𝑎, 𝑖) = 0, then own(𝐻, 𝑅, 𝑣, 𝜏) = own(𝐻 ′ , 𝑅, 𝑣, 𝜏).
Proof. By induction on the structure of 𝜏. The base case 𝜏 = {𝜈 : int | 𝜑} trivially holds because, in this case, own(𝐻, 𝑅,
𝑣, 𝜏) = 0 = own(𝐻 ′ , 𝑅, 𝑣, 𝜏).
                                                                               18
Ownership Types for Verification of Programs with Pointer Arithmetic                                                Conference’17, July 2017, Washington, DC, USA


   The inductive case is the case where 𝜏 = (𝜆𝑖.𝜏 ′ ) ref 𝑟 . We only consider the case where 𝑣 is an address (𝑎 ′ , 𝑖 ′ ) and (𝑎 ′ , 𝑖 ′ ) is
in dom(𝐻 ) (which is equal to dom(𝐻 ′ )); the other cases are trivial because the functions become zero functions. We have
         own(𝐻, 𝑅, (𝑎 ′ , 𝑖 ′ ), 𝜏)
                                                      Õ
          = {(𝑎 ′ , 𝑖 ′ + 𝑗 ) ↦→ 𝑟 ( 𝑗 ) | 𝑗 ∈ Z} +        own(𝐻, 𝑅, 𝐻 (𝑎 ′ , 𝑖 ′ + 𝑗 ), [ 𝑗 /𝑖]𝜏 ′)                                                   (by def.)
                                                       𝑗
                                                        Õ
          = {(𝑎 ′ , 𝑖 ′ + 𝑗 ) ↦→ 𝑟 ( 𝑗 ) | 𝑗 ∈ Z} +                 own(𝐻, 𝑅, 𝐻 (𝑎 ′ , 𝑖 ′ + 𝑗 ), [ 𝑗 /𝑖]𝜏 ′ )      (by well-formedness and Lemma B.11)
                                                      𝑗:𝑟 ( 𝑗 )>0
                                                        Õ
          = {(𝑎 ′ , 𝑖 ′ + 𝑗 ) ↦→ 𝑟 ( 𝑗 ) | 𝑗 ∈ Z} +                 own(𝐻 ′ , 𝑅, 𝐻 (𝑎 ′ , 𝑖 ′ + 𝑗 ), [ 𝑗 /𝑖]𝜏 ′)                                       (by I.H.)
                                                      𝑗:𝑟 ( 𝑗 )>0
                                                        Õ
          = {(𝑎 ′ , 𝑖 ′ + 𝑗 ) ↦→ 𝑟 ( 𝑗 ) | 𝑗 ∈ Z} +                 own(𝐻, 𝑅, 𝐻 ′ (𝑎 ′ , 𝑖 ′ + 𝑗 ), [ 𝑗 /𝑖]𝜏 ′)            (by 𝐻 ≈ (𝑎,𝑖 ) 𝐻 ′ and Lemma B.10)
                                                      𝑗:𝑟 ( 𝑗 )>0
          = own(𝐻, 𝑅, (𝑎 ′ , 𝑖 ′ ), 𝜏)                                                              (by a reasoning symmetric to the ﬁrst two equations)
To justify the above equational reasoning, we are left to check that, for any 𝑗 such that 𝑟 ( 𝑗 ) > 0, own(𝐻, 𝑅, 𝐻 (𝑎 ′ , 𝑖 ′ +
𝑗 ), [ 𝑗 /𝑖]𝜏 ′ ) (𝑎, 𝑖) = 0 so that we can indeed apply the induction hypothesis. If, to the contrary, 0 < own(𝐻, 𝑅, 𝐻 (𝑎 ′ , 𝑖 ′ +
𝑗 ), [ 𝑗 /𝑖]𝜏 ′ ) (𝑎, 𝑖), then we have own(𝐻, 𝑅, (𝑎 ′ , 𝑖 ′ ), 𝜏) (𝑎, 𝑖) > 0, which contradicts to own(𝐻, 𝑅, (𝑎 ′ , 𝑖 ′ ), 𝜏) (𝑎, 𝑖) = 0. 
Lemma B.19. If 𝐻 ≈ (𝑎,𝑖 ) 𝐻 ′ , own(𝐻, 𝑅, 𝑣, 𝜏) (𝑎, 𝑖) = 0 and SATv(𝐻, 𝑅, 𝑣, 𝜏), then SATv(𝐻 ′ , 𝑅, 𝑣, 𝜏).
Proof. By induction on the structure of 𝜏.
   The base case where 𝜏 = {𝜈 : int | 𝜑} is trivial because the deﬁnition of SATv(𝐻, 𝑅, 𝑣, 𝜏) does not depend on the heap 𝐻 .
   The step case is the case where 𝜏 = (𝜆𝑖.𝜏 ′ ) ref 𝑟 and 𝑣 is an address (𝑎 ′ , 𝑖 ′ ). Take 𝑗 such that 𝑟 ( 𝑗 ) > 0; note that (𝑎 ′ , 𝑖 ′ + 𝑗 ) ≠
(𝑎, 𝑖) by Lemma B.10. Our goal is to show that SATv(𝐻 ′ , 𝑅, 𝐻 ′ (𝑎 ′ , 𝑖 ′ + 𝑗 ), [ 𝑗 /𝑖 ′ ]𝜏 ′ ) because this would imply SATv(𝐻 ′ , 𝑅,
(𝑎 ′ , 𝑖 ′ ), 𝜏). Since own(𝐻, 𝑅, (𝑎 ′ , 𝑖 ′ ), 𝜏) (𝑎, 𝑖) = 0, it must be the case that own(𝐻, 𝑅, 𝐻 (𝑎 ′ , 𝑖 ′ + 𝑗 ), [ 𝑗 /𝑖 ′ ]𝜏 ′ ) (𝑎, 𝑖) = 0. We also
have SATv(𝐻, 𝑅, 𝐻 (𝑎 ′ , 𝑖 ′ + 𝑗 ), [ 𝑗 /𝑖 ′ ]𝜏 ′ ) from SATv(𝐻, 𝑅, (𝑎 ′ , 𝑖 ′ ), 𝜏). Therefore, we have SATv(𝐻 ′ , 𝑅, 𝐻 (𝑎 ′ , 𝑖 ′ + 𝑗 ), [ 𝑗 /𝑖 ′ ]𝜏 ′ ) by
the induction hypothesis. We also have 𝐻 (𝑎 ′ , 𝑖 ′ + 𝑗 ) = 𝐻 ′ (𝑎 ′ , 𝑖 ′ + 𝑗 ) because 𝐻 ≈ (𝑎,𝑖 ) 𝐻 ′ and (𝑎 ′ , 𝑖 ′ + 𝑗 ) ≠ (𝑎, 𝑖). Hence,
SATv(𝐻 ′ , 𝑅, 𝐻 ′ (𝑎 ′ , 𝑖 ′ + 𝑗 ), [ 𝑗 /𝑖 ′ ]𝜏 ′ ) holds.                                                                                                  
   Now we show that own and SATv are preserved under extension of heaps.
Lemma B.20. If SATv(𝐻, 𝑅, 𝑣, 𝜏), then for any 𝑣 ′ and address (𝑎 ′ , 𝑖 ′ ) such that (𝑎 ′ , 𝑖 ′ ) ∉ dom(𝐻 ) we have own(𝐻, 𝑅, 𝑣, 𝜏) =
own(𝐻 {(𝑎 ′ , 𝑖 ′ ) ←↪ 𝑣 ′ }, 𝑅, 𝑣, 𝜏).
Proof. By induction on the structure of 𝜏. The case where 𝜏 = {𝜈 :int | 𝜑} is trivial because own(𝐻, 𝑅, 𝑣, 𝜏) = own(𝐻 {(𝑎 ′ , 𝑖 ′ ) ←↪
𝑣 ′ }, 𝑅, 𝑣, 𝜏) = 0 by the deﬁnition of own.
     Now we consider the case 𝜏 = (𝜆𝑖.𝜏 ′ ) ref 𝑟 . From the assumption SATv(𝐻, 𝑅, 𝑣, 𝜏), it must be the case that 𝑣 is an address
(𝑎, 𝑖) such (𝑎, 𝑖) ∈ dom(𝐻 ) (which implies that (𝑎, 𝑖) ∈ dom(𝐻 {(𝑎 ′ , 𝑖 ′ ) ←↪ 𝑣 ′ }). We also have
                                         SATv(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏 ′)                 (for 𝑗 such that 𝑟 ( 𝑗 ) > 0)                                   (3)
by the deﬁnition of SATv. We, therefore, have
           own(𝐻, 𝑅, (𝑎, 𝑖), (𝜆𝑖.𝜏 ′ ) ref 𝑟 )
                                                      Õ
            = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 ( 𝑗 ) | 𝑗 ∈ Z} +           own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏 ′ )                                                       (by def.)
                                                       𝑗
                                                        Õ
            = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 ( 𝑗 ) | 𝑗 ∈ Z} +                    own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏 ′)            (by well-formedness and Lemma B.11)
                                                      𝑗:𝑟 ( 𝑗 )>0
            = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 ( 𝑗 ) | 𝑗 ∈ Z}
                 Õ
             +          own(𝐻 {(𝑎 ′ , 𝑖 ′ ) ←↪ 𝑣 ′ }, 𝑅, 𝐻 {(𝑎 ′ , 𝑖 ′ ) ←↪ 𝑣 ′ }(𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏 ′)                                    (by I.H. with (3))
                𝑗:𝑟 ( 𝑗 )>0
            = own(𝐻 {(𝑎 ′ , 𝑖 ′ ) ←↪ 𝑣 ′ }, 𝑅, (𝑎, 𝑖), (𝜆𝑖.𝜏 ′ ) ref 𝑟 ).
                                                                                                                                                                
                                                                     ′          ′   ′                  ′   ′                                   ′   ′       ′
Lemma B.21. If SATv(𝐻, 𝑅, 𝑣, 𝜏), then for any 𝑣 and (𝑎 , 𝑖 ) such that (𝑎 , 𝑖 ) ∉ dom(𝐻 ) we have SATv(𝐻 {(𝑎 , 𝑖 ) ←↪ 𝑣 }, 𝑅,
𝑣, 𝜏).
                                                                                        19
Conference’17, July 2017, Washington, DC, USA                                                                                       Tanaka et al.


Proof. By induction on the structure of 𝜏. The base case where 𝜏 = {𝜈 : int | 𝜑} is trivial because the deﬁnition of SATv(𝐻, 𝑅,
𝑣, {𝜈 : int | 𝜑}) does not depend on the heap.
   The inductive case is the case where 𝜏 = (𝜆𝑖.𝜏 ′ ) ref 𝑟 . From the deﬁnition of SATv, 𝑣 must be an address (𝑎, 𝑖) and must be
in dom(𝐻 ). We also have
                                                                  (𝑎, 𝑖 + 𝑗 ) ∈ dom(𝐻 )                                                      (4)
                                                                                                 ′
                                                          SATv(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏 )                                               (5)
for each 𝑗 such that 𝑟 ( 𝑗 ) > 0. By the induction hypothesis and (5), we have
                                                SATv(𝐻 {(𝑎 ′ , 𝑖 ′ ) ←↪ 𝑣 ′ }, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏 ′ ).                               (6)
Observe that (𝑎, 𝑖 + 𝑗 ) ≠ (𝑎 ′ , 𝑖 ′ ) because of (4), and thus 𝐻 (𝑎, 𝑖 + 𝑗 ) = 𝐻 {(𝑎 ′ , 𝑖 ′ ) ←↪ 𝑣 ′ }(𝑎, 𝑖 + 𝑗 ). From this, (4) and (6), we
conclude SATv(𝐻 {(𝑎 ′ , 𝑖 ′ ) ←↪ 𝑣 ′ }, 𝑅, 𝑣, 𝜏).                                                                                              
  We also show that SATv is preserved under the extension of register ﬁles.
Deﬁnition B.22. We write 𝑅 ⊑ 𝑅 ′ to denote two register ﬁles such that:
  1. 𝑑𝑜𝑚(𝑅) ⊆ 𝑑𝑜𝑚(𝑅 ′ ), and
  2. ∀𝑥 ∈ 𝑑𝑜𝑚(𝑅).𝑅(𝑥) = 𝑅 ′ (𝑥)
  We say that a register ﬁle 𝑅 is a valid substitution of 𝜏 if for each 𝑥 ∈ FV(𝜏), 𝑅(𝑥) is an integer.
Lemma B.23. Suppose that SATv(𝐻, 𝑅, 𝑣, 𝜏) and 𝑅 is a valid substitution of 𝜏. Then for any 𝑅 ′ such that 𝑅 ⊑ 𝑅 ′ , SATv(𝐻, 𝑅 ′ ,
𝑣, 𝜏).
Proof. By induction on 𝜏. We ﬁrst consider the base case where 𝜏 = {𝜈 : int | 𝜑}. Clearly, [𝑅] [𝑣/𝜈]𝜑 = [𝑅 ′ ] [𝑣/𝜈]𝜑 by the fact
that 𝑅 is a valid substitution of 𝜏. By SATv(𝐻, 𝑅, 𝑣, 𝜏), we have 𝑣 ∈ Z and |= [𝑅] [𝑣/𝜈], and thus we conclude SATv(𝐻, 𝑅 ′ , 𝑣, 𝜏).
The inductive case follows from the induction hypothesis.                                                                        
Main Proof of Subject Reduction. Finally, we are ready to prove subject reduction. Prior to starting the standard inductive
argument on the transition rules, we state one last lemma, which is a standard substitution lemma.
Lemma B.24 (Substitution). If Θ | Γ ⊢ 𝑒 : 𝜏 → Γ ′ and 𝑥 ′ ∉ dom(Γ), then Θ | [𝑥 ′ /𝑥]Γ ⊢ [𝑥 ′ /𝑥]𝑒 : [𝑥 ′ /𝑥]𝜏 → [𝑥 ′ /𝑥]Γ ′ .
Proof. By straightforward induction on the type derivation.                                                                                   
Lemma B.3 (Subject reduction). If ⊢𝐷 h𝑅, 𝐻, 𝑒i : 𝜏 =⇒ Γ ′ and h𝑅, 𝐻, 𝑒i −→𝐷 C, then either
   • C = AliasFail or
   • C = h𝑅 ′ , 𝐻 ′ , 𝑒 ′ i with ⊢𝐷 h𝑅 ′ , 𝐻 ′ , 𝑒 ′ i : 𝜏 =⇒ Γ ′ .
Proof. By induction on the derivation of the transition relation with a case analysis on the last rule applied.
  Before proceeding to the case analysis, let us explain the overall structure that are common across each case. By the
deﬁnition of well-typed conﬁguration, there exists a type environment Γ that satisﬁes
                                                                  Θ | Γ ⊢ 𝑒 : 𝜏 =⇒ Γ ′
                                        ∀(𝑎, 𝑖) ∈ dom(𝐻 ). Own(𝐻, 𝑅, Γ) ≤ 1                       SAT(𝐻, 𝑅, Γ)                               (7)
for some Θ. Our goal is to ﬁnd a type environment Γ ′′ such that
                                                                Θ | Γ ′′ ⊢ 𝑒 ′ : 𝜏 =⇒ Γ ′
                                   ∀(𝑎, 𝑖) ∈ dom(𝐻 ′ ). Own(𝐻 ′ , 𝑅 ′ , Γ ′′ ) (𝑎) ≤ 1               SAT(𝐻 ′ , 𝑅 ′ , Γ ′′ )
   For simplicity, we will ignore the subsumption rule T-Sub and argue as if the shape of 𝑒 determines the last rule applied
to derive Θ | Γ ⊢ 𝑒 : 𝜏 =⇒ Γ ′ . This does not cause any problem as the conditions about Own and SAT are preserved by the
subtyping relation (Lemma B.9).
   Now we proceed to the case analysis. The order of the cases does not follow how the rules are ordered in Figure 5. We
rather start from interesting cases, namely those that involves heap manipulations or ownership distributions.
    Case R-Assign: In this case, we must have
                                         𝑒 = 𝑥 := 𝑦; 𝑒 ′           𝐻 ′ = 𝐻 {𝑅(𝑦) ←↪ (𝑎, 𝑖)}              𝑅′ = 𝑅
                                                          𝑅(𝑥) = (𝑎, 𝑖)       (𝑎, 𝑖) ∈ dom(𝐻 )
                                                                             20
Ownership Types for Verification of Programs with Pointer Arithmetic                                         Conference’17, July 2017, Washington, DC, USA


       for some 𝑥, 𝑦, 𝑒 ′ , 𝑎 and 𝑖. By inversion of the typing of 𝑒, we must also have

                                                             Γ [𝑥 : (𝜆𝑖.𝜏𝑥′ ) ref 𝑟 ] [𝑦 : 𝜏1 + 𝜏2 ]
                                                                           𝑟 (0) = 1
                                                  Θ | Γ [𝑥 ←↪ (𝜆𝑖.𝜏𝑥 ) ref 𝑟 ] [𝑦 ←↪ 𝜏1 ] ⊢ 𝑒 ′ : 𝜏 =⇒ Γ ′                                             (8)
                                 𝑖 : {𝜈 : int | 𝜈 = 0} ⊢ 𝜏𝑥′ ≈ 𝜏2 ∧𝑥 (𝑥 =𝜏2 𝑦)              𝑖 : {𝜈 : int | 𝜈 ≠ 0} ⊢ 𝜏𝑥′ ≈ 𝜏𝑥                           (9)

       for some 𝑟 , 𝜏𝑥 , 𝜏𝑥′ , 𝜏1 and 𝜏2 . Observe that we have

                                  • ⊢ [0/𝑖]𝜏𝑥′ ≈ [0/𝑖] (𝜏2 ∧𝑥 (𝑥 =𝜏2 𝑦))                • ⊢ [𝑛/𝑖]𝜏𝑥′ ≈ [𝑛/𝑖]𝜏𝑥     (𝑛 ≠ 0)                           (10)

       from (9). Note that we also have 𝐻 ≈ (𝑎,𝑖 ) 𝐻 ′ .
                   def
       We set Γ ′′ = Γ [𝑥 ←↪ (𝜆𝑖.𝜏𝑥 ) ref 𝑟 ] [𝑦 ←↪ 𝜏1 ]. The typability of 𝑒 ′ under Γ ′′ is exactly what (8) claims.
       We check that ∀(𝑎 ′ , 𝑖 ′ ) ∈ dom(𝐻 ′ ). Own(𝐻 ′ , 𝑅, Γ ′′ ) (𝑎 ′ , 𝑖 ′ ) ≤ 1. First, observe that 𝑥 has the full ownership of (𝑎, 𝑖)
       because 𝑟 (0) = 1. Formally, we have

                                                             own(𝐻, 𝑅, 𝑅(𝑥), Γ(𝑥)) (𝑎, 𝑖) = 1                                                        (11)

       by the deﬁnition of own. Now we would like to appeal to Lemma B.18, which states that equivalent heaps have the
       same own function if “the modiﬁed part of the heap is not owned”. To this end, we show that

                                    for each 𝑧 ∈ dom(Γ) \ {𝑥 }, own(𝐻, 𝑅, 𝑅(𝑧), Γ(𝑧)) (𝑎, 𝑖) = 0                                                     (12)
                                    for each 𝑗 ≠ 0 with 𝑟 ( 𝑗 ) > 0, own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏𝑥 ) (𝑎, 𝑖) = 0                                 (13)

       The ﬁrst equality follows from the following inequality:

                                                                     Õ
                                           Own(𝐻, 𝑅, Γ) (𝑎, 𝑖) =               own(𝐻, 𝑅, 𝑅(𝑧), Γ(𝑧)) (𝑎, 𝑖)                                     (by def.)
                                                                   𝑧 ∈dom(Γ)
                                                                               Õ
                                                                =1+                     own(𝐻, 𝑅, 𝑅(𝑧), Γ(𝑧)) (𝑎, 𝑖)                            (by (11))
                                                                       𝑧 ∈dom(Γ)\{𝑥 }
                                                                ≤1                                                                               (by (7))

       The second equality, i.e. (13), can be shown by a similar argument. We therefore have:

                      Own(𝐻 ′ , 𝑅, Γ ′′ )
                         Õ
                      =            own(𝐻 ′ , 𝑅, 𝑅(𝑧), Γ ′′ (𝑧))                                                                                 (by def.)
                           𝑧 ∈dom(Γ ′′ )
                         = own(𝐻 , 𝑅, 𝑅(𝑥), (𝜆𝑖.𝜏𝑥 ) ref 𝑟 ) + own(𝐻 ′ , 𝑅, 𝑅(𝑦), 𝜏1 )
                                     ′
                                   Õ
                            +                own(𝐻, 𝑅, 𝑅(𝑧), Γ(𝑧))                                     (by Lemma B.18 with (12) and Γ(𝑧) = Γ ′′ (𝑧))
                                𝑧 ∈dom(Γ ′′ )\{𝑥,𝑦 }


       To give a bound to Own(𝐻 ′ , 𝑅, Γ ′′ ), we show that

                                             own(𝐻 ′ , 𝑅, 𝑅(𝑥), (𝜆𝑖.𝜏𝑥 ) ref 𝑟 ) + own(𝐻 ′ , 𝑅, 𝑅(𝑦), 𝜏1 )
                                              ≤ own(𝐻, 𝑅, 𝑅(𝑥), (𝜆𝑖.𝜏 ′ ) ref 𝑟 ) + own(𝐻, 𝑅, 𝑅(𝑦), 𝜏1 + 𝜏2 ).
                                                                                21
Conference’17, July 2017, Washington, DC, USA                                                                                                                 Tanaka et al.


      because this would imply Own(𝐻 ′ , 𝑅, Γ ′′ ) ≤ Own(𝐻, 𝑅, Γ). For all (𝑎 ′ , 𝑖 ′ ) ≠ (𝑎, 𝑖), we have
               own(𝐻 ′ , 𝑅, 𝑅(𝑥), (𝜆𝑖.𝜏𝑥 ) ref 𝑟 ) (𝑎 ′ , 𝑖 ′ ) + own(𝐻 ′ , 𝑅, 𝑅(𝑦), 𝜏1 ) (𝑎 ′ , 𝑖 ′ )
                = own(𝐻 ′ , 𝑅, (𝑎, 𝑖), (𝜆𝑖.𝜏𝑥 ) ref 𝑟 ) (𝑎 ′ , 𝑖 ′ ) + own(𝐻, 𝑅, 𝑅(𝑦), 𝜏1 ) (𝑎 ′ , 𝑖 ′ )                                  (Lemma B.18 and 𝐻 ≈ (𝑎,𝑖 ) 𝐻 ′ )
                = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 ( 𝑗 ) | 𝑗 ∈ Z}(𝑎 ′ , 𝑖 ′ )
                   Õ
                 +      own(𝐻 ′ , 𝑅, 𝐻 ′ (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏𝑥 ) (𝑎 ′ , 𝑖 ′ ) + own(𝐻, 𝑅, 𝑅(𝑦), 𝜏1 ) (𝑎 ′ , 𝑖 ′ )                                      (by def. of own)
                      𝑗
                                                                           Õ
                = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 ( 𝑗 ) | 𝑗 ∈ Z}(𝑎 ′ , 𝑖 ′ ) +                   own(𝐻 ′ , 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏𝑥 ) (𝑎 ′ , 𝑖 ′ )
                                                                           𝑗:𝑗≠0
                 + own(𝐻, 𝑅, 𝑅(𝑦), [0/𝑖]𝜏𝑥 ) (𝑎 ′ , 𝑖 ′ ) + own(𝐻, 𝑅, 𝑅(𝑦), 𝜏1 ) (𝑎 ′ , 𝑖 ′ )                   (by 𝐻 ′ (𝑎, 𝑖) = 𝑅(𝑦) and 𝐻 ≈ (𝑎,𝑖 ) 𝐻 ′ )
                                                                 Õ
                = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 ( 𝑗 ) | 𝑗 ∈ Z}(𝑎 ′ , 𝑖 ′ ) +   own(𝐻 ′ , 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏 ′) (𝑎 ′ , 𝑖 ′ )
                                                                           𝑗:𝑗≠0
                 + own(𝐻, 𝑅, 𝑅(𝑦), 𝜏2 ) (𝑎 , 𝑖 ) + own(𝐻, 𝑅, 𝑅(𝑦), 𝜏1 ) (𝑎 ′ , 𝑖 ′ )
                                                 ′    ′
                                                                                                                                              (by (10) and Lemma B.14)
                                                               Õ
                = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 (𝑖) | 𝑖 ∈ Z}(𝑎 ′ , 𝑖 ′ ) +   own(𝐻 ′ , 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏 ′) (𝑎 ′ , 𝑖 ′ )
                                                                          𝑗:𝑗≠0
                                                          ′       ′
                 + own(𝐻, 𝑅, 𝑅(𝑦), 𝜏1 + 𝜏2 ) (𝑎 , 𝑖 )                                                                                                  (by Lemma B.15)
                                                                           Õ
                                                              ′       ′                                                   ′    ′   ′
                = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 ( 𝑗 ) | 𝑗 ∈ Z}(𝑎 , 𝑖 ) +                       own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏 ) (𝑎 , 𝑖 )
                                                                           𝑗:𝑗≠0
                 + own(𝐻, 𝑅, 𝑅(𝑦), 𝜏1 + 𝜏2 ) (𝑎 ′ , 𝑖 ′ )                                                                                 (Lemma B.18 and 𝐻 ≈ (𝑎,𝑖 ) 𝐻 ′ )
                                                                            Õ
                ≤ {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 ( 𝑗 ) | 𝑗 ∈ Z}(𝑎 ′ , 𝑖 ′ ) +                   own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏 ′) (𝑎 ′ , 𝑖 ′ )
                                                                           𝑗:𝑗≠0
                  + own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖), 𝜏 ′ ) (𝑎 ′ , 𝑖 ′ ) + own(𝐻, 𝑅, 𝑅(𝑦), 𝜏1 + 𝜏2 ) (𝑎 ′ , 𝑖 ′ )
                = own(𝐻, 𝑅, 𝑅(𝑥), (𝜆𝑖.𝜏𝑥′ ) ref 𝑟 ) (𝑎 ′ , 𝑖 ′ ) + own(𝐻, 𝑅, 𝑅(𝑦), 𝜏1 + 𝜏2 ) (𝑎 ′ , 𝑖 ′ ).
      The case where the argument is (𝑎, 𝑖) can be proved in a similar manner using Lemma B.18 and Lemma B.15.
      Now we show that SAT(𝐻 ′ , 𝑅, Γ ′′ ). By SAT(𝐻, 𝑅, Γ), for each 𝑧 ∈ dom(Γ), we have SATv(𝐻, 𝑅, 𝑅(𝑧), Γ(𝑧)). Because
      satisﬁability is preserved between equivalent heaps, we have SATv(𝐻 ′ , 𝑅, 𝑅(𝑧), Γ ′′ (𝑧)) for 𝑧 ∈ dom(Γ) \ {𝑥, 𝑦}; more
      formally, this is by Lemma B.19 with 𝐻 ≈ (𝑎,𝑖 ) 𝐻 ′ and (12). Similarly, we have SATv(𝐻 ′ , 𝑅, 𝑅(𝑦), 𝜏1 + 𝜏2 ). In particular,
      we have
                                               SATv(𝐻 ′ , 𝑅, 𝑅(𝑦), 𝜏1 )                   and SATv(𝐻 ′ , 𝑅, 𝑅(𝑦), 𝜏2 )                                                (14)
     by Lemma B.16. Since 𝜏1 = Γ ′′ (𝑦), it remains to show SATv(𝐻 ′ , 𝑅, 𝑅(𝑥), Γ ′′ (𝑥)). We need to show that SATv(𝐻 ′ , 𝑅,
     𝐻 ′ (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏𝑥′ ) for each 𝑗 such that 𝑟 ( 𝑗 ) > 0. For 𝑗 ≠ 0, we can appeal to Lemma B.19 together with (13) and the
     fact that SATv(𝐻, 𝑅, 𝑅(𝑥), Γ(𝑥)) with • ⊢ [ 𝑗 /𝑖]𝜏𝑥′ ≈ [ 𝑗 /𝑖]𝜏𝑥 and Lemma B.13. We also have SATv(𝐻 ′ , 𝑅, 𝐻 ′ (𝑎, 𝑖), 𝜏𝑥′ [0/𝑖])
     from (14) because 𝐻 ′ (𝑎, 𝑖) = 𝑅(𝑦) (hence the strengthening has no eﬀect) and (10).
   Case R-Deref: We must have
                                                     𝑒 = let 𝑥 = ∗𝑦 in 𝑒 0                 𝑒 ′ = [𝑥 ′ /𝑥]𝑒 0     𝐻 = 𝐻′
                                                          𝑅 ′ = 𝑅{𝑥 ′ ←↪ 𝐻 (𝑅(𝑦))}                   𝑥 ′ ∉ dom(𝐻 )
      for some 𝑥, 𝑥 ′ , 𝑦 and 𝑒 0 . Furthermore, by inversion of the typing of 𝑒, we have
                                                                              Γ [𝑦 : (𝜆𝑖.𝜏 𝑦 ) ref 𝑟 ]
                                                     Θ | Γ [𝑦 ←↪ (𝜆𝑖.𝜏 𝑦′ ) ref 𝑟 ], 𝑥 : 𝜏𝑥 ⊢ 𝑒 : 𝜏 =⇒ Γ ′                                                            (15)
                                                                  ′
                             𝑖 : {𝜈 : int | 𝜈 = 0} ⊢ 𝜏                + 𝜏𝑥 ≈ 𝜏 𝑦        𝑖 : {𝜈 : int | 𝜈 = 0} ⊢ 𝜏 𝑦′ ≈ 𝜏 ′ ∧𝑦 (𝑦 =𝜏 ′ 𝑥)                              (16)
                                                                        𝑖 : {𝜈 : int | 𝜈 ≠ 0} ⊢ 𝜏 𝑦′ ≈ 𝜏 𝑦                                                            (17)
                                                                                       ′
                                                                          𝑥 ∉ dom(Γ )             𝑟 (0) > 0
      for some 𝜏𝑥 , 𝜏 𝑦 , 𝜏 𝑦′ 𝜏 ′ and 𝑟 .
      We take Γ [𝑦 ←↪ (𝜆𝑖.𝜏 𝑦′ ) ref 𝑟 ], 𝑥 ′ : 𝜏𝑥        for Γ ′′ . Then from the substitution lemma (Lemma B.24), (15) and 𝑥 ∉ Γ ′ , we have
      Θ | Γ ′′ ⊢ 𝑒 ′ : 𝜏 =⇒ Γ ′ .
                                                                                           22
Ownership Types for Verification of Programs with Pointer Arithmetic                                               Conference’17, July 2017, Washington, DC, USA


       We now show that ∀(𝑎, 𝑖).Own(𝐻, 𝑅 ′ , Γ ′′ ) (𝑎, 𝑖) ≤ 1. Since the diﬀerences between Γ and Γ ′′ are in the type of 𝑥 ′ and 𝑦,
       we only need to show that
                                            own(𝐻, 𝑅, 𝑅(𝑦), (𝜆𝑖.𝜏 𝑦 ) ref 𝑟 )
                                             = own(𝐻, 𝑅 ′ , 𝑅 ′ (𝑦), (𝜆𝑖.𝜏 𝑦′ ) ref 𝑟 ) + own(𝐻, 𝑅 ′ , 𝑅 ′ (𝑥 ′ ), 𝜏𝑥 ).
       Since 𝑅(𝑦) must be an address, let us write (𝑎, 𝑖) for 𝑅(𝑦). The above equation is shown as follows:
                               own(𝐻, 𝑅, 𝑅(𝑦), (𝜆𝑖.𝜏 𝑦 ) ref 𝑟 )
                                                                        Õ
                               = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 ( 𝑗 ) | 𝑗 ∈ Z} +            own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏 𝑦 )                                   (by def.)
                                                                          𝑗
                                                                        Õ
                               = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 ( 𝑗 ) | 𝑗 ∈ Z} +             own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏 𝑦 )
                                                                        𝑗:𝑗≠0
                                 + own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖), [0/𝑖]𝜏 𝑦 )
                                                                        Õ
                               = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 ( 𝑗 ) | 𝑗 ∈ Z} +             own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏 𝑦′ )
                                                                        𝑗:𝑗≠0
                                + own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖), 𝜏𝑥 + 𝜏 𝑦′ [0/𝑖])                         (by Lemmas B.13 and B.14 with (16) and (17))
                                                                    Õ
                               = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 ( 𝑗 ) | 𝑗 ∈ Z} +    own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏 𝑦′ )
                                                                        𝑗:𝑗≠0
                                + own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖), 𝜏𝑥 ) + own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖), 𝜏 𝑦′ [0/𝑖])                                                    (Lemma B.15)
                                                                    Õ
                               = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 ( 𝑗 ) | 𝑗 ∈ Z} +   own(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏 𝑦′ )
                                                                          𝑗
                                 + own(𝐻, 𝑅, 𝑅 ′ (𝑥 ′ ), 𝜏𝑥 )                                                                             (𝑅 ′ (𝑥 ′ ) = 𝐻 (𝑅(𝑦)))
                               = own(𝐻, 𝑅 ′ , 𝑅 ′ (𝑦), (𝜆𝑖.𝜏 𝑦′ ) ref 𝑟 ) + own(𝐻, 𝑅 ′ , 𝑅 ′ (𝑥 ′ ), 𝜏𝑥 )
       For this case, it remains to show that SAT(𝐻, 𝑅 ′ , Γ ′′ ). Again, it suﬃces to consider SATv(𝐻, 𝑅 ′ , 𝑅 ′ (𝑥 ′ ), Γ ′′ (𝑥 ′ )) and
       SATv(𝐻, 𝑅 ′ , 𝑅 ′ (𝑦), Γ ′′ (𝑦)). Since SAT(𝐻, 𝑅, Γ), we have SATv(𝐻, 𝑅, 𝑅(𝑦), Γ(𝑦)), and thus
                                                                SATv(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏 𝑦 )
       for each 𝑟 such that 𝑟 ( 𝑗 ) > 0, where (𝑎, 𝑖) = 𝑅(𝑦). In particular, since 𝑟 (0) > 0 and (16), we have
                                          SATv(𝐻, 𝑅, 𝐻 (𝑅(𝑦)), 𝜏𝑥 )             and SATv(𝐻, 𝑅, 𝐻 (𝑅(𝑦)), [0/𝑖]𝜏 ′ )
      thanks to Lemma B.16. Because 𝑅 ′ (𝑥 ′ ) = 𝐻 (𝑅(𝑦)) and 𝑅 ′ is an extension of 𝑅, we have SATv(𝐻, 𝑅 ′ , 𝑅 ′ (𝑥 ′ ), Γ ′′ (𝑥 ′ )) by
      Lemma B.23. Similarly, we also have SATv(𝐻, 𝑅 ′ , 𝑅 ′ (𝑦), Γ ′′ (𝑦)).
    Case R-AddPtr: In this case, we must have
                                                 𝑒 = let 𝑥 = 𝑦 ⊞ 𝑧 in 𝑒 0            𝑒 ′ = [𝑥 ′ /𝑥]𝑒 0       𝐻′ = 𝐻
                                          𝑅 ′ = 𝑅{𝑥 ′ ←↪ (𝑎, 𝑖 + 𝑅(𝑧))}                  𝑅(𝑦) = (𝑎, 𝑖)      𝑥 ′ ∉ dom(𝑅)                                    (18)
       for some 𝑥, 𝑦, 𝑧, 𝑒 0 and (𝑎, 𝑖). By inversion of the typing of 𝑒, it must also be the case that
                                                       Γ [𝑦 : (𝜆𝑖.(𝜏1 + 𝜏2 )) ref 𝑟 𝑦 ] [𝑧 : {𝜈 : int | 𝜑}]
                                                            ′
                           Θ | Γ [𝑦 ←↪ (𝜆𝑖.𝜏1 ) ref 𝑟 𝑦 ], 𝑥 : (𝜆𝑖.[(𝑖 + 𝑧)/𝑖]𝜏2 ) ref 𝑟𝑥 , 𝑧 : {𝜈 : int | 𝜑} ⊢ 𝑒 0 : 𝜏 =⇒ Γ ′                              (19)
                                                                                            ′
                                                                              𝑥 ∉ dom(Γ )
                                                                  𝑟 𝑥 (𝑖 − 𝑅(𝑧)) + 𝑟 𝑦′ (𝑖) = 𝑟 𝑦 (𝑖)                                                       (20)
       for some 𝑟 𝑥 , 𝑟 𝑦 , 𝑟 𝑦′ , 𝜏1 and 𝜏2 .
                         def                            ′
       We deﬁne Γ ′′ = Γ [𝑦 ←↪ (𝜆𝑖.𝜏1 ) ref 𝑟 𝑦 ], 𝑥 ′ : (𝜆𝑖.[(𝑖 − 𝑧)/𝑖]𝜏2 ) ref 𝑟𝑥 , 𝑧 : {𝜈 : int | 𝜑}. By substitution lemma (Lemma B.24),
       (19) and 𝑥 ∉ dom(Γ ′ ) we have Γ ′′ ⊢ 𝑒 ′ : 𝜏 =⇒ Γ ′ .
       We check the condition ∀(𝑎 ′ , 𝑖 ′ ).Own(𝐻, 𝑅 ′ , Γ ′′ ) (𝑎 ′ , 𝑖 ′ ) ≤ 1. It is enough to show that
                                own(𝐻, 𝑅, 𝑅(𝑦), (𝜆𝑖.(𝜏1 + 𝜏2 )) ref 𝑟 𝑦 )
                                                                                                                                 ′
                                 = own(𝐻, 𝑅 ′ , 𝑅 ′ (𝑥 ′ ), (𝜆𝑖.[𝑖 + 𝑧/𝑖]𝜏2 ) ref 𝑟𝑥 ) + own(𝐻, 𝑅 ′ , 𝑅 ′ (𝑦), (𝜆𝑖.𝜏1 ) ref 𝑟 𝑦 ).
                                                                                    23
Conference’17, July 2017, Washington, DC, USA                                                                                                                    Tanaka et al.


      because then we have Own(𝐻, 𝑅, Γ) = Own(𝐻, 𝑅 ′ , Γ ′′ ). Indeed, we have
              own(𝐻, 𝑅, 𝑅(𝑦), (𝜆𝑖.(𝜏1 + 𝜏2 )) ref 𝑟 𝑦 )
                                                      Õ
               = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 𝑦 ( 𝑗 ) | 𝑗 ∈ Z} +   own(𝐻, 𝑅, (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏1 + 𝑖 [ 𝑗 /𝑖]𝜏2)                                         (by def. and 𝑅(𝑦) = (𝑎, 𝑖))
                                                                 𝑗
                                                                 Õ
               = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 𝑦 ( 𝑗 ) | 𝑗 ∈ Z} +                    own(𝐻, 𝑅, (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏1)
                                                                 𝑗
                    Õ
                +       own(𝐻, 𝑅, (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏2 )                                                                                                   (Lemma B.15)
                    𝑗
                                                                                        Õ
               = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 𝑥 ( 𝑗 − 𝑅(𝑧)) + 𝑟 𝑦′ ( 𝑗 ) | 𝑗 ∈ Z} +                         own(𝐻, 𝑅, (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏1)
                                                                                          𝑗
                    Õ
                +       own(𝐻, 𝑅, (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏2 )                                                                                                          (by (20))
                    𝑗
                                                                 Õ
               = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 𝑦′ ( 𝑗 ) | 𝑗 ∈ Z} +                   own(𝐻, 𝑅, (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏1)
                                                                 𝑗
                                                                              Õ
                + {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 𝑥 ( 𝑗 − 𝑅(𝑧)) | 𝑗 ∈ Z} +                         own(𝐻, 𝑅, (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏2)
                                                                                𝑗
                                                             ′
               = own(𝐻, 𝑅 ′ , 𝑅 ′ (𝑦), (𝜆𝑖.𝜏1 ) ref 𝑟 𝑦 )
                                                                              Õ
                + {(𝑎, 𝑖 + 𝑅(𝑧) + 𝑗 ) ↦→ 𝑟 𝑥 ( 𝑗 ) | 𝑗 ∈ Z} +                        own(𝐻, 𝑅, (𝑎, 𝑖 + 𝑅(𝑧) + 𝑗 ), [𝑅(𝑧) + 𝑗 /𝑖]𝜏2 )
                                                                               𝑗
                                                         ′
               = own(𝐻, 𝑅, 𝑅 ′ (𝑦), (𝜆𝑖.𝜏1 ) ref 𝑟 𝑦 )
                                                                              Õ
                + {(𝑎, 𝑖 + 𝑅(𝑧) + 𝑗 ) ↦→ 𝑟 𝑥 ( 𝑗 ) | 𝑗 ∈ Z} +                        own(𝐻, 𝑅, (𝑎, 𝑖 + 𝑅(𝑧) + 𝑗 ), [ 𝑗 /𝑖] [𝑖 + 𝑧/𝑖]𝜏2 )
                                                                               𝑗
                                                             ′
               = own(𝐻, 𝑅 ′ , 𝑅 ′ (𝑦), (𝜆𝑖.𝜏1 ) ref 𝑟 𝑦 ) + own(𝐻, 𝑅 ′ , 𝑅 ′ (𝑥 ′ ), (𝜆𝑖.[𝑖 + 𝑧/𝑖]𝜏2 ) ref 𝑟𝑥 )                                    (𝑅 ′ (𝑥 ′ ) = (𝑎, 𝑖 + 𝑅(𝑧)))
      Similarly, to show that SAT(𝐻, 𝑅 ′ , Γ ′′ ) it suﬃces to show that, SATv(𝐻, 𝑅 ′ , 𝑅 ′ (𝑥 ′ ), Γ ′′ (𝑥 ′ )) and SATv(𝐻, 𝑅 ′ , 𝑅 ′ (𝑥 ′ ), Γ ′′ (𝑦)).
      Since SAT(𝐻, 𝑅, Γ), we have SATv(𝐻, 𝑅, 𝑅(𝑦), Γ(𝑦)). In particular, we have SATv(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏1 + [ 𝑗 /𝑖]𝜏2 ) for
      each 𝑗 such that 𝑟 𝑦 ( 𝑗 ) > 0. Therefore,
                                SATv(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏1 )                    and SATv(𝐻, 𝑅, 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏2)
      for each 𝑗 such that 𝑟 𝑦 ( 𝑗 ) > 0, by Lemma B.16. Since 𝑟 𝑦 ( 𝑗 ) ≥ 𝑟 𝑦′ ( 𝑗 ) and 𝑟 𝑦 ( 𝑗 ) ≥ 𝑟 𝑥 ( 𝑗 − 𝑅(𝑧)) by (20), we have
                                                         SATv(𝐻, 𝑅 ′ , 𝐻 (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖]𝜏1)                  (for 𝑗 s.t. 𝑟 𝑦′ ( 𝑗 ) > 0)
                                 SATv(𝐻, 𝑅 ′ , 𝐻 (𝑎, 𝑖 + 𝑅(𝑧) + 𝑗 ), [ 𝑗 /𝑖] [𝑖 + 𝑧/𝑖]𝜏2 )                        (for 𝑗 s.t. 𝑟 𝑥 ( 𝑗 ) > 0)
      with the help of Lemma B.23. Hence, we conclude SATv(𝐻, 𝑅 ′ , 𝑅 ′ (𝑦), Γ ′′ (𝑦)) and SATv(𝐻, 𝑅 ′ , 𝑅 ′ (𝑥 ′ ), Γ ′′ (𝑥 ′ )) as desired.
   Case R-AliasAddPtr It must be the case that
                                                                           𝑒 = alias(𝑥 = 𝑦 ⊞ 𝑧); 𝑒 ′
                                      𝐻′ = 𝐻                 𝑅′ = 𝑅                 𝑅(𝑥) = (𝑎, 𝑖 + 𝑅(𝑧))               𝑅(𝑦) = (𝑎, 𝑖)
      for some 𝑥, 𝑦 and 𝑧. By inversion on the typing of 𝑒 we must also have
                                           Γ [𝑥 : (𝜆𝑖.𝜏𝑥 ) ref 𝑟𝑥 ] [𝑦 : (𝜆𝑖.𝜏 𝑦 ) ref 𝑟 𝑦 ] [𝑧 : {𝜈 : int | 𝜑}]
                                                                     ′                                ′
                             Θ | Γ [𝑥 ←↪ (𝜆𝑖.𝜏𝑥′ ) ref 𝑟𝑥 ] [𝑦 ←↪ (𝜆𝑖.𝜏 𝑦′ ) ref 𝑟 𝑦 ], 𝑧 : {𝜈 : int | 𝜑} ⊢ 𝑒 ′ : 𝜏 =⇒ Γ ′
                                                                                                                                 ′                   ′
                     • ⊢ ((𝜆𝑖.[(𝑖 − 𝑧)/𝑖]𝜏𝑥 ) ref 𝑟𝑥𝑧 + (𝜆𝑖.𝜏 𝑦 ) ref 𝑟 𝑦 ) ≈ ((𝜆𝑖.[(𝑖 − 𝑧)/𝑖]𝜏𝑥′ ) ref 𝑟𝑥𝑧 + (𝜆𝑖.𝜏 𝑦′ ) ref 𝑟 𝑦 )                                        (21)
                                                𝑟 𝑥𝑧 (𝑖) = 𝑟 𝑥 (𝑖 − 𝑅(𝑧))                         𝑟 𝑥′ 𝑧 (𝑖) = 𝑟 𝑥′ (𝑖 − 𝑅(𝑧))                                            (22)
                                                  𝑟 𝑥′                                    𝑟 𝑦′
      We deﬁne Γ ′′ as Γ [𝑥 ←↪ (𝜆𝑖.𝜏𝑥′ ) ref ] [𝑦 ←↪ (𝜆𝑖.𝜏 𝑦′ ) ref ], 𝑧 : {𝜈 : int | 𝜑}. Obviously, Θ | Γ ′′ ⊢ 𝑒 ′ : 𝜏 ′ =⇒ Γ ′ .
      Now we check that the invariant about the ownership is preserved. It is enough to check that
                                           own(𝐻, 𝑅, 𝑅(𝑥), Γ(𝑥)) + own(𝐻, 𝑅, 𝑅(𝑦), Γ(𝑦))
                                            = own(𝐻, 𝑅, 𝑅(𝑥), Γ ′′ (𝑥)) + own(𝐻, 𝑅, 𝑅(𝑦), Γ ′′ (𝑦)).
                                                                                          24
Ownership Types for Verification of Programs with Pointer Arithmetic                                               Conference’17, July 2017, Washington, DC, USA


       Observe that
                             own(𝐻, 𝑅, 𝑅(𝑥), Γ(𝑥))
                              = own(𝐻, 𝑅, (𝑎, 𝑖 + 𝑅(𝑧)), (𝜆𝑖.𝜏𝑥 ) ref 𝑟𝑥 )
                                                                            Õ
                              = {(𝑎, 𝑖 + 𝑅(𝑧) + 𝑗 ) ↦→ 𝑟 𝑥 ( 𝑗 ) | 𝑗 ∈ Z} +   own(𝐻, 𝑅, (𝑎, 𝑖 + 𝑅(𝑧) + 𝑗 ), [ 𝑗 /𝑖]𝜏𝑥 )
                                                                                        𝑗
                                                                                     Õ
                              = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 𝑥 ( 𝑗 − 𝑅(𝑧)) | 𝑗 ∈ Z} +                  own(𝐻, 𝑅, (𝑎, 𝑖 + 𝑗 ), [ 𝑗 − 𝑅(𝑧)/𝑖]𝜏𝑥 )
                                                                                        𝑗
                                                                        Õ
                              = {(𝑎, 𝑖 + 𝑗 ) ↦→ 𝑟 𝑥𝑧 ( 𝑗 ) | 𝑗 ∈ Z} +             own(𝐻, 𝑅, (𝑎, 𝑖 + 𝑗 ), [ 𝑗 /𝑖] [𝑖 − 𝑧/𝑖]𝜏𝑥 )                          (by (22))
                                                                         𝑗
                              = own(𝐻, 𝑅, 𝑅(𝑦), (𝜆𝑖.[(𝑖 − 𝑧)/𝑖]𝜏𝑥 ) ref 𝑟𝑥𝑧 )                                                                       (by 𝑅(𝑦) = 𝑎)
                                                                                                                       𝑟 𝑥′ 𝑧
       Similarly, we have own(𝐻, 𝑅, 𝑅(𝑥), Γ ′′ (𝑥)) = own(𝐻, 𝑅, 𝑅(𝑦), (𝜆𝑖.[(𝑖 − 𝑧)/𝑖]𝜏𝑥′ ) ref                                  ). Hence, we have
                    own(𝐻, 𝑅, 𝑅(𝑥), Γ(𝑥)) + own(𝐻, 𝑅, 𝑅(𝑦), Γ(𝑦))
                     = own(𝐻, 𝑅, 𝑅(𝑦), (𝜆𝑖.[(𝑖 − 𝑧)/𝑖]𝜏𝑥 ) ref 𝑟𝑥𝑧 ) + own(𝐻, 𝑅, 𝑅(𝑦), (𝜆𝑖.𝜏 𝑦 ) ref 𝑟 𝑦 )
                     = own(𝐻, 𝑅, 𝑅(𝑦), (𝜆𝑖.[(𝑖 − 𝑧)/𝑖]𝜏𝑥 ) ref 𝑟𝑥𝑧 + (𝜆𝑖.𝜏 𝑦 ) ref 𝑟 𝑦 )                                                            (Lemma B.15)
                                                                         𝑟 𝑥′ 𝑧                     𝑟 𝑦′
                     = own(𝐻, 𝑅, 𝑅(𝑦), (𝜆𝑖.[(𝑖 − 𝑧)/𝑖]𝜏𝑥′ ) ref                    + (𝜆𝑖.𝜏 𝑦′ ) ref )                                    (Lemma B.13 with (21))
                                                                         𝑟 𝑥′ 𝑧                                        ′
                     = own(𝐻, 𝑅, 𝑅(𝑦), (𝜆𝑖.[(𝑖 − 𝑧)/𝑖]𝜏𝑥′ ) ref                   ) + own(𝐻, 𝑅, 𝑅(𝑦), (𝜆𝑖.𝜏 𝑦′ ) ref 𝑟 𝑦 )                          (Lemma B.15)
                                        ′′                                            ′′
                     = own(𝐻, 𝑅, 𝑅(𝑥), Γ (𝑥)) + own(𝐻, 𝑅, 𝑅(𝑦), Γ (𝑦)).
       as desired.
       To ﬁnish this case we show that SAT(𝐻, 𝑅, Γ ′′ ). Once again, we may focus on 𝑥 and 𝑦. By a similar reasoning we did
       above for own, we have
                                  SATv(𝐻, 𝑅, 𝑅(𝑥), Γ(𝑥))         iﬀ      SATv(𝐻, 𝑅, 𝑅(𝑦), (𝜆𝑖.[(𝑖 − 𝑧)/𝑖]𝜏𝑥 ) ref 𝑟𝑥𝑧 )
                                                                                                                                    ′
                                SATv(𝐻, 𝑅, 𝑅(𝑥), Γ ′′ (𝑥))       iﬀ      SATv(𝐻, 𝑅, 𝑅(𝑦), (𝜆𝑖.[(𝑖 − 𝑧)/𝑖]𝜏𝑥′ ) ref 𝑟𝑥𝑧 )
      Since SAT(𝐻, 𝑅, Γ), we have SATv(𝐻, 𝑅, 𝑅(𝑥), Γ(𝑥)) and SATv(𝐻, 𝑅, 𝑅(𝑦), Γ(𝑦)). Hence, from the above bi-implication
      and Lemma B.16, it follows that SATv(𝐻, 𝑅, 𝑅(𝑦), (𝜆𝑖.𝜏 𝑦 ) ref 𝑟 𝑦 ] + (𝜆𝑖.[(𝑖 − 𝑧)/𝑖]𝜏𝑥 ) ref 𝑟𝑥𝑧 ). Lemma B.13 with (21) gives
                                           ′                               ′
      us SATv(𝐻, 𝑅, 𝑅(𝑦), (𝜆𝑖.𝜏 𝑦′ ) ref 𝑟 𝑦 ) + (𝜆𝑖.[(𝑖 − 𝑧)/𝑖]𝜏𝑥′ ) ref 𝑟𝑥𝑧 . By Lemma B.16 together with the above bi-implication, we
      conclude SATv(𝐻, 𝑅, 𝑅(𝑥), Γ ′′ (𝑥)) and SATv(𝐻, 𝑅, 𝑅(𝑦), Γ ′′ (𝑦)).
    Case R-AliasDeref Similar to the case of R-AliasAddPtr.
    Case R-MkArray For this case, we have
                                                   𝑒 = let 𝑥 = alloc 𝑛 in 𝑒 0                  𝑒 ′ = [𝑥 ′ /𝑥]𝑒 0
                           𝐻 ′ = 𝐻 {(𝑎, 0) ↦→ 𝑚 0 } · · · {(𝑎, 𝑛 − 1) ↦→ 𝑚𝑛−1 }                     (𝑎, 0), . . . , (𝑎, 𝑛 − 1) ∉ dom(𝐻 )
                                                       ′        ′                               ′
                                                     𝑅 = 𝑅{𝑥 ←↪ (𝑎, 0)}                       𝑥 ∉ dom(𝑅)
       for some 𝑥, 𝑥 ′ , 𝑒   0 and a base address 𝑎. By inversion on the typing of 𝑒 0 , we also have

                                                      Θ | Γ, 𝑥 : (𝜆𝑖.⊤𝑘 ) ref 𝑟 ⊢ 𝑒 0 : 𝜏 =⇒ Γ ′                                                             (23)
                                                                    (
                                                                      1 0 ≦𝑖 ≦𝑛−1
                                                            𝑟 (𝑖) =                                                                                          (24)
                                                                      0 𝑜𝑡ℎ𝑒𝑟𝑤𝑖𝑠𝑒
                                                                        𝑥 ∉ dom(Γ ′ )
                     def
       We set Γ ′′ = Γ, 𝑥 : (𝜆𝑖.⊤𝑘 ) ref 𝑟 . The fact that Θ | Γ ′′ ⊢ 𝑒 ′ : 𝜏 =⇒ Γ ′ is immediate from substitution lemma
       (Lemma B.24), (23) and 𝑥 ∉ dom(Γ ′ ).
       We ﬁrst check that SAT(𝐻 ′ , 𝑅 ′ , Γ ′′ ). Since SAT(𝐻, 𝑅, Γ), we have
                                                SATv(𝐻, 𝑅, 𝑅(𝑧), Γ(𝑧))                      for each 𝑧 ∈ dom(Γ)                                              (25)
       Because 𝑅 ⊑ 𝑅 ′ and Γ(𝑧) = Γ ′′ (𝑧) for 𝑧 ∈ dom(Γ), we have SATv(𝐻, 𝑅, 𝑅 ′ (𝑧), Γ ′′ (𝑧)) by Lemma B.23. Hence, it remains
       to show that SATv(𝐻 ′ , 𝑅 ′ , 𝑅(𝑥 ′ ), (𝜆𝑖.⊤𝑘 ) ref 𝑟 ). This is immediate by the deﬁnition of SATv and the fact that “⊤𝑘 is valid”
       (Lemma B.12).
                                                                                   25
Conference’17, July 2017, Washington, DC, USA                                                                                                  Tanaka et al.


      Now we check that, for every (𝑎 ′ , 𝑖 ′ ) ∈ dom(𝐻 ′ ), Own(𝐻 ′ , 𝑅 ′ , Γ ′′ ) (𝑎 ′ , 𝑖 ′ ) ≤ 1. Observe that own(𝐻, 𝑅, 𝑅(𝑧), Γ(𝑧)) =
      own(𝐻 ′ , 𝑅, 𝑅 ′ (𝑧), Γ ′′ (𝑧)) for each 𝑧 ∈ dom(Γ) thanks to Lemma B.20 and (25). We therefore have
                                  Own(𝐻 ′ , 𝑅 ′ , Γ ′′ ) = Own(𝐻, 𝑅, Γ) + own(𝐻 ′ , 𝑅 ′ , 𝑅 ′ (𝑥 ′ ), Γ ′′ (𝑥 ′ ))
                                                        = Own(𝐻, 𝑅, Γ) + own(𝐻, 𝑅 ′ , (𝑎, 0), (𝜆𝑖.⊤𝑘 ) ref 𝑟 )
                                                        = Own(𝐻, 𝑅, Γ) + {(𝑎, 𝑖) ↦→ 𝑟 (𝑖) | 𝑖 ∈ Z}                                         (Lemma B.11)
     Thus, for each (𝑎 ′ , 𝑖 ′ ) ∈ dom(𝐻 ′ ) if (𝑎 ′ , 𝑖 ′ ) ∈ dom(𝐻 ), then Own(𝐻 ′ , 𝑅 ′ , Γ ′′ ) (𝑎 ′ , 𝑖 ′ ) = Own(𝐻, 𝑅, Γ) (𝑎 ′, 𝑖 ′ ) ≤ 1; other-
     wise Own(𝐻 ′ , 𝑅 ′ , Γ ′′ ) (𝑎 ′ , 𝑖 ′ ) = 1 by (24).
   Case R-LetVar In this case, we must have
                                             𝑒 = let 𝑥 = 𝑦 in 𝑒 0           𝑒 ′ = [𝑥 ′ /𝑥]𝑒 0            𝐻′ = 𝐻
                                                    𝑅 ′ = 𝑅{𝑥 ′ ←↪ 𝑅(𝑦)}               𝑥 ′ ∉ dom(𝑅)
      for some 𝑥, 𝑦, 𝑒 0 , 𝑎 and 𝑖. By inversion of the typing of 𝑒, we must also have
                                                                Θ | Γ ⊢ 𝑦 : 𝜏1 =⇒ Γ1                                                                   (26)
                                                                                                   ′
                                                            Θ | Γ1, 𝑥 : 𝜏1 ⊢ 𝑒 0 : 𝜏 =⇒ Γ                                                              (27)
                                                            𝑥 ∉ dom(Γ ′ )            𝑥 ∉ fv(𝜏)
      for some Γ1 and 𝜏1 . By inversion on (26), Γ and Γ1 must satisfy
                                                       Γ [𝑦 : 𝜏1 + 𝜏2 ]           Γ1 = Γ [𝑦 ←↪ 𝜏2 ]
      for some 𝜏2 .
                    def
      We deﬁne Γ ′′ = Γ [𝑦 ←↪ 𝜏2 ], 𝑥 ′ : 𝜏1 . By substitution lemma (Lemma B.24), (27) and 𝑥 ∉ dom(Γ ′ ) ∪ fv(𝜏), we have
      Θ | Γ ⊢ [𝑥 /𝑥]𝑒 0 : 𝜏 =⇒ Γ ′ .
            ′′    ′

      Now we check that the ownership invariant is preserved. As in other cases, it suﬃces to check that
                           own(𝐻, 𝑅, 𝑅(𝑦), Γ(𝑦)) = own(𝐻, 𝑅, 𝑅 ′ (𝑦), Γ ′′ (𝑦)) + own(𝐻, 𝑅, 𝑅 ′ (𝑥 ′ ), Γ ′′ (𝑥 ′ ))
      This trivially holds because
                          own(𝐻, 𝑅, 𝑅 ′ (𝑦), Γ ′′ (𝑦)) + own(𝐻, 𝑅, 𝑅 ′ (𝑥 ′ ), Γ ′′ (𝑥 ′ ))
                           = own(𝐻, 𝑅, 𝑅(𝑦), 𝜏2 ) + own(𝐻, 𝑅, 𝑅(𝑦), 𝜏1 )                                          (by 𝑅 ′ (𝑦) = 𝑅(𝑦) and 𝑅 ′ (𝑥 ′ ) = 𝑅(𝑦))
                           = own(𝐻, 𝑅, 𝑅(𝑦), 𝜏1 + 𝜏2 )                                                                                     (Lemma B.15)
                           = own(𝐻, 𝑅, 𝑅(𝑦), Γ(𝑦)).
     Finally, we show that SAT(𝐻, 𝑅 ′ , Γ ′′ ). We only need to check SATv(𝐻, 𝑅 ′ , 𝑅 ′ (𝑦), Γ ′′ (𝑦)) and SATv(𝐻, 𝑅 ′ , 𝑅 ′ (𝑥 ′ ), Γ ′′ (𝑥 ′ )).
     By SAT(𝐻, 𝑅, Γ), we have SATv(𝐻, 𝑅, 𝑅(𝑦), 𝜏1 + 𝜏2 ). Applying Lemma B.16 and B.23 together with 𝑅 ⊑ 𝑅 ′ and 𝜏1 + 𝜏2 =
     Γ ′′ (𝑦) + Γ ′′ (𝑥 ′ ) concludes this case.
   Case R-LetInt Similar to the case for R-LetVar.
   Case R-Context By induction on the structure of 𝐸. If 𝐸 = [ ] then the result holds by the induction hypothesis (of the
     induction on the transition rules).
     Now suppose that
                                             𝑒 = 𝐸 [𝑒 0 ]       𝑒 ′ = 𝐸 [𝑒 0′ ]       𝐸 = let 𝑥 = 𝐸 ′ in 𝑒 2
                                                             h𝑅, 𝐻, 𝑒 0 i −→ h𝑅 ′ , 𝐻 ′ , 𝑒 0′ i                                                       (28)
      By inversion on the typing of 𝑒, we have
                                                             Θ | Γ ⊢ 𝐸 [𝑒 0 ] : 𝜏1 =⇒ Γ1
                                                            Θ | Γ1, 𝑥 : 𝜏1 : 𝑒 2 : 𝜏 =⇒ Γ ′                                                            (29)
                                                              𝑥 ∉ dom(Γ1 ) ∪ FV(𝜏1 )
      for some 𝜏1 and Γ1 . We have
                                                       h𝑅, 𝐻, 𝐸 ′ [𝑒 0 ]i −→ h𝑅 ′ , 𝐻 ′ , 𝐸 ′ [𝑒 0′ ]i
      by R-Context and (28).
                                                                             26
Ownership Types for Verification of Programs with Pointer Arithmetic                                             Conference’17, July 2017, Washington, DC, USA


       By the induction hypothesis (on the evaluation context) there exists a type environment Γ ′′ such that
                                                              Θ | Γ ′′ ⊢ 𝐸 ′ [𝑒 0′ ] : 𝜏1 =⇒ Γ1                                                          (30)
                                                               ′    ′    ′′                              ′   ′   ′′
                                           ∀(𝑎, 𝑖).Own(𝐻 , 𝑅 , Γ ) (𝑎, 𝑖) ≤ 1                  SAT(𝐻 , 𝑅 , Γ )
      It remains to check that Θ | Γ ′′ ⊢ 𝑒 ′ : 𝜏 =⇒ Γ ′ . This is immediate from (29) and (30).
    Case R-AssertFail This case cannot happen by Lemma B.2.
    Case R-Assert In this case, we must have
                                                       𝑒 = assert(𝜑); 𝑒 ′        𝑅′ = 𝑅       𝐻′ = 𝐻.
       Furthermore, we have
                                                                   Θ | Γ ⊢ 𝑒 ′ : 𝜏 =⇒ Γ ′
      by inversion on the typing of 𝑒. Therefore, we can simply take Γ for Γ ′′ .
    Case R-IfTrue It must be the case that
                                              𝑒 = ifnp 𝑥 then 𝑒 1 else 𝑒 2             𝑒 ′ = 𝑒1        𝐻′ = 𝐻
                                                                   𝑅′ = 𝑅           𝑅(𝑥) ≤ 0
       By inversion on the typing of 𝑒, we have
                                                Γ [𝑥 : {𝜈 : int | 𝜑}]
                                               Θ | Γ [𝑥 ←↪ {𝜈 : int | 𝜑 ∧ 𝜈 ≤ 0}] ⊢ 𝑒 1 : 𝜏 =⇒ Γ ′                                                       (31)
                    def
      We set Γ ′′ = Γ [𝑥 ←↪ {𝜈 : int | 𝜑 ∧ 𝜈 ≤ 0}]. Clearly, we have Θ | Γ ′′ ⊢ 𝑒 ′ : 𝜏 =⇒ Γ ′ from (31), Since own(𝐻, 𝑅,
      𝑅(𝑥), Γ(𝑥)) = 0 = own(𝐻, 𝑅, 𝑅(𝑥), Γ ′′ (𝑥)), we have Own(𝐻, 𝑅, Γ) = Own(𝐻, 𝑅, Γ ′′ ). Hence, it remains to show that
      SAT(𝐻, 𝑅, Γ ′′ ). In particular, we need to show that SATv(𝐻, 𝑅, 𝑅(𝑥), {𝜈 : int | 𝜑 ∧ 𝜈 = 0}). Since 𝑅(𝑥) ≤ 0, we have
      |= [𝑅] (𝑥 ≤ 0). It remains to show |= [𝑅] [𝑅(𝑥)/𝜈]𝜑, which we have from SATv(𝐻, 𝑅, 𝑅(𝑥), Γ(𝑥)).
    Case R-IfFalse Similar to the case of T-IfTrue.
    Case R-Call In this case, we have
                               𝑒 = let 𝑥 = 𝑓 (𝑦1 , . . . , 𝑦𝑛 ) in 𝑒 2        𝑒 ′ = let 𝑥 = [𝑦1 /𝑥 1 ] · · · [𝑦𝑛 /𝑥𝑛 ]𝑒 1 in 𝑒 2
                                                                𝑓 ↦→ (𝑥 1, . . . , 𝑥𝑛 )𝑒 2 ∈ 𝐷
                                                                   𝐻′ = 𝐻            𝑅′ = 𝑅
       for some 𝑥, 𝑓 , 𝑒 1 and 𝑒 2 . Without loss of generality we may assume that 𝑥 1, . . . , 𝑥𝑛 are fresh. By inversion on the typing
       of 𝑒, we have
                                                               Γ [𝑦1 : 𝜎𝜏1 ] · · · [𝑦𝑛 : 𝜎𝜏𝑛 ]
                                          Θ(𝑓 ) = h𝑥 1 : 𝜏1 , . . . , 𝑥𝑛 : 𝜏𝑛 i → h𝑥 1 : 𝜏1′ , . . . , 𝑥𝑛 : 𝜏𝑛′ | 𝜏𝑥 i
                                    Θ | Γ [𝑦𝑖 ←↪ 𝜎𝜏𝑖′ ], 𝑥 : 𝜎𝜏𝑥 ⊢ 𝑒 2 : 𝜏 =⇒ Γ ′              𝑥 ∉ dom(Γ ′ ) ∪ FV(𝜏)                                     (32)
       for some 𝜏𝑥 , 𝜏𝑖 and 𝜏𝑖′ where 𝜎 = [𝑦1 /𝑥 1 ] · · · [𝑦𝑛 /𝑥𝑛 ]. Moreover, because Θ ⊢ 𝐷, we must have
                                             Θ | 𝑥 1 : 𝜏1 . . . 𝑥𝑛 : 𝜏𝑛 ⊢ 𝑒 1 : 𝜏𝑥 =⇒ 𝑥 1 : 𝜏1′ , . . . , 𝑥𝑛 : 𝜏𝑛′                                       (33)
       by the rules T-Funs and T-FunDef.
       We take Γ as Γ ′′ . Since the preservation of the invariants are trivial, we only need to check that 𝑒 ′ can be typed under Γ.
       By repeatedly applying the substitution lemma (Lemma B.24) to (33), and then applying a standard weakening lemma,
       we obtain
                                            Θ | Γ ⊢ [𝑦1 /𝑥 1 ] · · · [𝑦𝑛 /𝑥𝑛 ]𝑒 1 : 𝜎𝜏𝑥 =⇒ Γ [𝑦𝑖 ←↪ 𝜎𝜏𝑖′ ].
      Applying T-Let to this and (33) gives Θ | Γ ⊢ 𝑒 ′ : 𝜏 =⇒ Γ ′ as desired.
    Case R-AliasDerefFail and R-AliasAddPtrFail Trivial.
                                                                                                                                                            
                                                                               27
Conference’17, July 2017, Washington, DC, USA                                                                                  Tanaka et al.


B.3   Proof of Progress
Finally, we prove the progress lemma (Lemma B.4) to conclude the soundness of our type system. We ﬁrst observe that any
expression can be decomposed into an evaluation context and a redex.
Lemma B.25. For any expression 𝑒, either (i) 𝑒 = 𝑥 for some variable 𝑥, (ii) 𝑒 = 𝑛 for some integer 𝑛, or (iii) 𝑒 = 𝐸 [𝑒 ′ ] for some
evaluation context 𝐸 and an expression 𝑒 ′ where 𝑒 ′ is one of the following forms:
   1. let 𝑥 = 𝑛 in 𝑒 0
   2. let 𝑥 = 𝑦 in 𝑒 0
   3. ifnp 𝑥 then 𝑒 1 else 𝑒 2
   4. let 𝑥 = ∗𝑦 in 𝑒 0
   5. 𝑥 := 𝑦; 𝑒 0
   6. let 𝑥 = 𝑦 ⊞ 𝑧 in 𝑒 0
   7. let 𝑥 = alloc 𝑛 in 𝑒 0
   8. let 𝑥 = 𝑓 (𝑦1 , . . . , 𝑦𝑛 ) in 𝑒 0
   9. alias(𝑥 = ∗𝑦); 𝑒 0
  10. alias(𝑥 = 𝑦 ⊞ 𝑧); 𝑒 0
  11. assert(𝜑); 𝑒 0
Proof. By a straight forward induction on the structure of 𝑒.                                                                            
Lemma B.4 (Progress). Suppose ⊢𝐷            h𝑅, 𝐻, 𝑒i : 𝜏 =⇒ Γ ′ . Then either
  1. h𝑅, 𝐻, 𝑒i −→𝐷 h𝑅 ′ , 𝐻 ′ , 𝑒 ′ i holds for some conﬁguration h𝑅 ′ , 𝐻 ′ , 𝑒 ′ i,
  2. h𝑅, 𝐻, 𝑒i −→𝐷 AliasFail, or
  3. h𝑅, 𝐻, 𝑒i is of the form h𝑅, 𝐻, 𝑣i, where 𝑣 is some variable 𝑥 or an integer 𝑛 (and thus cannot be reduced anymore).
Proof. The proof is by a case analysis on the shape of 𝑒 according to Lemma B.25. The case where 𝑒 = 𝑥 or 𝑒 = 𝑛 is exactly
the case 3, so it remains to consider the case where 𝑒 = 𝐸 [𝑒 ′ ]. Now the proof proceeds by induction on the structure of 𝐸. We
only show the base case where 𝐸 = [ ] because the inductive case follows immediately from the induction hypothesis.
  Note that, by ⊢𝐷 h𝑅, 𝐻, 𝑒i : 𝜏 =⇒ Γ ′ , we have Θ | Γ ⊢ 𝑒 : 𝜏 =⇒ Γ ′ and SAT(𝑅, 𝐻, Γ) for some Γ. In particular, this implies
that
                            ∀𝑥 ∈ dom(Γ). 𝑥 ∈ dom(𝑅)                                                                                    (34)
                            if 𝑥 : {𝜈 : int | 𝜑} ∈ Γ, then 𝑅(𝑥) ∈ Z                                                                    (35)
                                        ′       𝑟
                            if 𝑥 : (𝜆𝑖.𝜏 ) ref ∈ Γ, then 𝑅(𝑥) = (𝑎, 𝑖) for some (𝑎, 𝑖) and (𝑎, 𝑖) ∈ dom(𝐻 ).                           (36)
  Now we proceed by a case analysis on the shape of 𝑒 ′ .
   Case 𝑒 ′ = let 𝑥 = 𝑛 in 𝑒 0 and 𝑒 ′ = let 𝑥 = 𝑦 in 𝑒 0 : The conﬁguration can reduce using R-LetInt and R-LetVar, respec-
     tively.
   Case 𝑒 ′ = ifnp 𝑥 then 𝑒 1 else 𝑒 2 : By (35), we have 𝑅(𝑥) ∈ Z. The conﬁguration can reduce depending on the value 𝑅(𝑥)
     using R-IfTrue or R-IfFalse.
   Case 𝑒 ′ = let 𝑥 = ∗𝑦 in 𝑒 0 : By inversion on the typing of 𝑒 ′ , 𝑦 must be a reference type. Therefore, by (36), 𝐻 (𝑅(𝑦)) is
     deﬁned, and the conﬁguration can reduce using R-Deref.
   Case 𝑒 ′ = 𝑥 := 𝑦; 𝑒 0 : We can reduce the conﬁguration using R-Assign if 𝑅(𝑥) ∈ dom(𝐻 ). The condition 𝑅(𝑥) ∈ dom(𝐻 )
     is met by (36) and the fact that 𝑥 has a reference type, which follows from the well-typedness of 𝑒 ′ .
   Case 𝑒 ′ = let 𝑥 = 𝑦 ⊞ 𝑧 in 𝑒 0 : Since 𝑅(𝑧) ∈ Z by (35) and the typing of 𝑒 ′ , we can reduce the conﬁguration using R-AddPtr.
   Case 𝑒 ′ = let 𝑥 = alloc 𝑛 in 𝑒 0 : This case is obvious as we can reduce the conﬁguration according to R-MkArray.
   Case let 𝑥 = 𝑓 (𝑦1 , . . . , 𝑦𝑛 ) in 𝑒 0 : It suﬃces to check that 𝑓 ↦→ (𝑥 1, . . . , 𝑥𝑛 )𝑒 ′′ ∈ 𝐷. Then we can conclude this case using
     R-Call. By inversion on the typing of 𝑒 ′ , we have 𝑓 ∈ dom(Θ). We must also have Θ ⊢ 𝐷 from ⊢𝐷 h𝑅, 𝐻, 𝑒i : 𝜏 =⇒ Γ ′ .
     By the deﬁnition of Θ ⊢ 𝐷, we have 𝑓 ↦→ (𝑥 1, . . . , 𝑥𝑛 )𝑒 ′′ ∈ 𝐷 as desired.
   Case alias(𝑥 = ∗𝑦); 𝑒 0 : By (35), (36) and the fact that 𝑒 ′ is well-typed, we know that 𝑅(𝑥) and 𝐻 (𝑅(𝑦)) are deﬁned. Hence,
     we can reduce the conﬁguration using R-AliasDeref or R-AliasDerefFail.
   Case 𝑒 ′ = alias(𝑥 = 𝑦 ⊞ 𝑧); 𝑒 0 : Similar to the previous case.
   Case 𝑒 ′ = assert(𝜑); 𝑒 0 : We can reduce the conﬁguration using R-Assert or R-AssertFail according to whether [𝑅] |= 𝜑
     holds or not. However, by Lemma B.2 we know that the conﬁguration cannot reduce to assert failure, so the state after
     the reduction step must be a conﬁguration.
                                                                                                                                          
                                                                       28
Ownership Types for Verification of Programs with Pointer Arithmetic                Conference’17, July 2017, Washington, DC, USA


C     Benchmark Programs
Figures 13–20 list the benchmark programs used in the experiments described in Section 5. Note that those programs were
given as they are, without any annotations of ownerships and reﬁnement predicates. For the comparison with SeaHorn, we
prepared corresponding C programs and passed them to SeaHorn.

init(n, p)
[ <n: int, p: int ref> ->
  <n: int, p: int ref | int> ]
{
    if n <= 0 then {
      1
    } else {
      p := 0; let q = p + 1 in let m = n - 1 in
      let d = init(m, q) in 0
    }
}

init_assert (n, p)
[ <n: int, p: int ref> ->
  <n: int, p: int ref | int> ]
{
    if n <= 0 then {
      1
    } else {
      let y = *p in assert (y = 0); let q = p + 1 in let m = n - 1 in
      let d = init_assert (m, q) in 0
    }
}

{
    let p = alloc 10 in let m = 10 in
    let d1 = init(m, p) in let d2 = init_assert (m, p) in 0
}


                                                               Figure 13. Init-10




                                                                       29
Conference’17, July 2017, Washington, DC, USA                           Tanaka et al.


init(n, p)
[ <n: int, p: int ref> ->
  <n: int, p: int ref | int> ]
{
    if n <= 0 then {
      1
    } else {
      p := 0; let q = p + 1 in let m = n - 1 in
      let d = init(m, q) in 0
    }
}

init_assert (n, p)
[ <n: int, p: int ref> ->
  <n: int, p: int ref | int> ]
{
    if n <= 0 then {
      1
    } else {
      let y = *p in assert (y = 0); let q = p + 1 in let m = n - 1 in
      let d = init_assert (m, q) in 0
    }
}

{
    let p = alloc 1000 in let m = 1000 in
    let d1 = init(m, p) in let d2 = init_assert (m, p) in 0
}


                                                      Figure 14. Init




                                                              30
Ownership Types for Verification of Programs with Pointer Arithmetic             Conference’17, July 2017, Washington, DC, USA


sum(n, p)
[ <n: int, p: int ref> ->
  <n: int, p: int ref | int> ]
{
    if n <= 0 then {
      0
    } else {
      let x = *p in let q = p + 1 in let m = n - 1 in
      let s = sum(m, q) in let y = x + s in y
    }
}

abs(m)
[ <m: int> -> <m: int | int> ]
{
    if m >= 0 then {
      m
    } else {
      let k = -m in k
    }
}

init_x(n, x, p)
[ <n: int, x: int, p: int ref> ->
  <n: int, x: int, p: int ref | int> ]
{
    if n <= 0 then {
      1
    } else {
      p := x; let q = p + 1 in let m = n - 1 in
      let d = init_x(m, x, q) in 0
    }
}

{
    let p = alloc 1000 in let m = 1000 in
    let rand = _ in let z = abs(rand) in
    let d = init_x(m, z, p) in let x = sum(m, p) in
    assert(x >= 0); 0
}


                                                                Figure 15. Sum




                                                                       31
Conference’17, July 2017, Washington, DC, USA                           Tanaka et al.


sum_back (n, p)
[ <n: int, p: int ref> ->
  <n: int, p: int ref | int> ]
{
    if n <= 0 then {
      0
    } else {
      let m = n - 1 in let q = p + m in let x = *q in
      let s = sum_back (m, p) in let y = x + s in y
    }
}

abs(m)
[ <m: int> -> <m: int | int> ]
{
    if m >= 0 then {
      m
    } else {
      let k = -m in k
    }
}

init_x(n, x, p)
[ <n: int, x: int, p: int ref> ->
  <n: int, x: int, p: int ref | int> ]
{
    if n <= 0 then {
      1
    } else {
      p := x; let q = p + 1 in let m = n - 1 in
      let d = init_x(m, x, q) in 0
    }
}

{
    let p = alloc 1000 in let m = 1000 in
    let rand = _ in let z = abs(rand) in
    let d = init_x(m, z, p) in let x = sum_back (m, p) in
    assert(x >= 0); 0
}


                                                  Figure 16. Sum-Back




                                                            32
Ownership Types for Verification of Programs with Pointer Arithmetic              Conference’17, July 2017, Washington, DC, USA


sum_both (n, p)
[ <n: int, p: int ref> ->
  <n: int, p: int ref | int> ]
{
    if n <= 0 then {
      0
    } else {
      let x = *p in
      if n = 1 then {
         x
        } else {
          let k = n - 1 in let q = p + k in let x2 = *q in
          let y = x + x2 in let m = n - 2 in let p' = p + 1 in
          let s = sum(m, p') in let z = y + s in z
        }
    }
}

abs(m)
[ <m: int> -> <m: int | int> ]
{
    if m >= 0 then {
      m
    } else {
      let k = -m in k
    }
}

init_x(n, x, p)
[ <n: int, x: int, p: int ref> ->
  <n: int, x: int, p: int ref | int> ]
{
    if n <= 0 then {
      1
    } else {
      p := x; let q = p + 1 in let m = n - 1 in
      let d = init_x(m, x, q) in 0
    }
}

{
    let p = alloc 1000 in let m = 1000 in
    let rand = _ in let z = abs(rand) in
    let d = init_x(m, z, p) in let x = sum_both (m, p) in
    assert(x >= 0); 0
}


                                                            Figure 17. Sum-Both




                                                                       33
Conference’17, July 2017, Washington, DC, USA                                     Tanaka et al.


sum_div(n, m, p)
[ <n: int, m: int, p: int ref> ->
  <n: int, m: int, p: int ref | int> ]
{
    if n < m then {
      0
    } else {
      if n <= 0 then {
        0
      } else {
        let x = *p in
        if n = 1 then {
             x
            } else {
              let q = p + m in let m2 = m / 2 in let s1 = sum_div (m, m2, p) in
              let k = n - m in let k2 = k / 2 in let s2 = sum_div (k, k2, q) in
              let z = s1 + s2 in z
            }
        }
    }
}

abs(m)
[ <m: int> -> <m: int | int> ]
{
    if m >= 0 then {
      m
    } else {
      let k = -m in k
    }
}

init_x(n, x, p)
[ <n: int, x: int, p: int ref> ->
  <n: int, x: int, p: int ref | int> ]
{
    if n <= 0 then {
      1
    } else {
      p := x; let q = p + 1 in let m = n - 1 in
      let d = init_x(m, x, q) in 0
    }
}

{
    let p = mkarray 1000 in let m = 1000 in
    let rand = _ in let z = abs(rand) in let d = init_x(m, z, p) in
    let m2 = 500 in let x = sum_div (m, m2, p) in
    assert(x >= 0); 0
}


                                                        Figure 18. Sum-Div




                                                                 34
Ownership Types for Verification of Programs with Pointer Arithmetic               Conference’17, July 2017, Washington, DC, USA


copy_array (n, p, q)
[ <n: int, p: int ref, q: int ref> ->
  <n: int, p: int ref, q: int ref | int> ]
{
    if n <= 0 then {
      1
    } else {
      let x = *p in q := x; let p' = p + 1 in let q' = q + 1 in
      let m = n - 1 in let d = copy_array (m, p', q') in 0
    }
}

abs(m)
[ <m: int> -> <m: int | int> ]
{
    if m >= 0 then {
      m
    } else {
      let k = -m in k
    }
}

init_x(n, x, p)
[ <n: int, x: int, p: int ref> ->
  <n: int, x: int, p: int ref | int> ]
{
    if n <= 0 then {
      1
    } else {
      p := x; let q = p + 1 in let m = n - 1 in
      let d = init_x(m, x, q) in 0
    }
}

copy_assert (n, p)
[ <n: int, p: int ref> ->
  <n: int, p: int ref | int> ]
{
    if n <= 0 then {
      1
    } else {
      let y = *p in assert (y >= 0); let q = p + 1 in
      let m = n - 1 in let d = copy_assert (m, q) in 0
    }
}

{
    let p = alloc 1000 in let q = alloc 1000 in let m = 1000 in
    let rand = _ in let z = abs(rand) in let d1 = init_x(m, z, p) in
    let d2 = copy_array (m, p, q) in let d3 = copy_assert (m, q) in 0
}


                                                           Figure 19. Copy-Array




                                                                       35
Conference’17, July 2017, Washington, DC, USA                             Tanaka et al.


add_array (n, p, q, r)
[ <n: int, p: int ref, q: int ref, r: int ref> ->
  <n: int, p: int ref, q: int ref, r: int ref | int> ]
{
    if n <= 0 then {
      1
    } else {
      let x = *p in let y = *q in let z = x + y in r := z;
      let p' = p + 1 in let q' = q + 1 in let r' = r + 1 in
      let m = n - 1 in let d = add_array (m, p', q', r') in 0
    }
}

abs(m)
[ <m: int> -> <m: int | int> ]
{
    if m >= 0 then {
      m
    } else {
      let k = -m in k
    }
}

init_x(n, x, p)
[ <n: int, x: int, p: int ref> ->
  <n: int, x: int, p: int ref | int> ]
{
    if n <= 0 then {
      1
    } else {
      p := x; let q = p + 1 in let m = n - 1 in
      let d = init_x(m, x, q) in 0
    }
}

add_assert (n, p)
[ <n: int, p: int ref> ->
  <n: int, p: int ref | int> ]
{
    if n <= 0 then {
      1
    } else {
      let y = *p in assert (y >= 0); let q = p + 1 in
      let m = n - 1 in let d = add_assert (m, q) in 0
    }
}

{
    let p = alloc 1000 in let q = alloc 1000 in let r = alloc 1000 in
    let m = 1000 in let rand = _ in let z = abs(rand) in
    let d1 = init_x(m, z, p) in let d2 = init_x(m, z, q) in
    let d3 = add_array (m, p, q, r) in let d4 = add_assert (m, r) in 0
}


                                                   Figure 20. Add-Array




                                                                36
