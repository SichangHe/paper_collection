                                                                                                                                                                                         1




                                                            Local Reasoning about Block-based
                                                                  Cloud Storage Systems
                                                                   Zhao Jin, Hanpin Wang, Lei Zhang, Bowen Zhang, and Yongzhi Cao,

                                              Abstract—Owing to the massive growth in the storage demands of big data, Cloud Storage Systems (CSSs) have been put forward to
                                              improve the storage capacity. Compare with traditional storage systems, CSSs have lots of advantages, such as higher capacity, lower
                                              cost, and easier scalability. However, they suffer from the main shortcoming of high complexity. To ensure the reliability of CSSs, the
                                              correctness of management programs should be proven. Therefore, a verification framework based on Separation Logic (SL) is
                                              proposed to prove the correctness of management programs in Block-based Cloud Storage Systems (BCSSs), which is the most
                                              popular CSSs. The main contributions are as follows. (1) Two-tier heap structure is constructed as the type of storage units in BCSSs.
arXiv:1904.04442v2 [cs.LO] 11 Nov 2019




                                              All the operations to BCSSs are based on the structure. (2) Assertion pairs are defined to describe the properties for the two-tier
                                              structure. The fact that the two components of a pair effect each other leads lots of interesting properties. (3) A proof system with
                                              Hoare-style specification rules is proposed to reason about the BCSSs. The results show that the correctness of BCSSs can be
                                              verified precisely and flexibly.

                                              Index Terms—Separation Logic, Hoare Logic, Block-based Cloud Storage Systems, Deduction, Formal Verification.

                                                                                                                       F

                                         1    I NTRODUCTION


                                         W      ITH the rapid growth of data, the capacity of tra-
                                                ditional storage devices could not meet the great
                                         demands. The Cloud Storage Systems (CSSs) have been put
                                                                                                                           servers where the blocks are stored. These characteristics
                                                                                                                           lead to the different management in BCSSs from tradition
                                                                                                                           and higher complexity as well. As a result, the reliability
                                         forward to improve the storage capacity [9]. According to                         of BCSSs has been constantly questioned. For instance, the
                                         the data types stored, CSSs are divided into three categories:                    Amazon Simple Storage Service (S3) accidentally removed
                                         Block-based CSSs (BCSSs), Object-based CSSs, and File-                            a set of servers due to system software errors, resulting in
                                         based CSSs. Among these CSSs, BCSSs have the lowest                               tremendous data loss with many customers involved, which
                                         cost and are the easiest to scale, hence BCSSs are the most                       caused great harm to the data integrity in the cloud storage
                                         popular systems used in CSSs at present.                                          system [32]. Therefore the problem of reliability of BCSSs is
                                             In BCSSs, data are stored in the block-based storage                          coming up.
                                         structure, which means that the resources in BCSSs consist                            Generally, the reliability of BCSSs is reflected in the
                                         of small block spaces. When user submit their data file to                        correctness and security aspects. The correctness refers to
                                         a BCSS, the system would cut the file into some segments,                         the algorithm which can produce the expected output for
                                         and then take those segments into property blocks. Using                          each input [7]. The security demands a series of mech-
                                         Hadoop distribeted file system (HDFS) [23] as an example,                         anisms to protect data from theft or damage. Obviously,
                                         uploaded file is divided into lots of 128MB segments firstly.                     the correctness is the most basic requirement of reliability.
                                         Then the system allocates those segments to a sequence of                         The correctness analysis not only proves the correctness of
                                         blocks one by one, and the size of each block is 128MB as                         the data processing, but also helps to find potential system
                                         well. Finally, the system will generate a file table to record                    design errors. Therefore, we aim to verify the correctness of
                                         the block addresses and the relation between file segments                        BCSSs. In BCSSs, the correctness refers to the management
                                         and blocks. The others, like Google file system (GFS) [8],                        programs correctness. The BCSSs management programs
                                         have the similar procedure. For example, the MapReduce                            mean a series of commands which are used to deal with the
                                         programs, which is a popular tool in big data analysis,                           request of user or to manage storage system, such as create,
                                         run on block-based distributed file systems, such as GFS                          append, and delete commands. There are plenty of ways to
                                         [31] and HDFS, etc. In the MapReduce programs, the input                          verify the correctness of programs, such as software testing
                                         data is stored in a file partitioned by blocks, and each of                       techniques and formal verification. The former is popular
                                         the block is processed by a map task. To reduce the cost                          due to its low cost, but the disadvantage of incomplete.
                                         of data transmission, the map task is invoked on the data                         Although the latter is a little more expensive, it can provide
                                                                                                                           strict mathematical analysis support and is efficient in find-
                                         •   Z. Jin, H. Wang, L. Zhang, B. Zhang, Y. Cao are with the Key Laboratory       ing errors. Therefore, it is widely used in the safety-critical
                                             of High Confidence Software Technologies (MOE), School of Electronics         systems.
                                             Engineering and Computer Science, Peking University, Beijing 100871,              Memory management is challenging for formal verifi-
                                             China.
                                             E-mail:     {jinzhao,      whpxhy,      zhangleijuly,      zhangbowen,        cation, and memory errors are not easily handled during
                                             caoyz}@pku.edu.cn.                                                            program execution. Separation Logic (SL) [22], which is a
                                         •   H. Wang is with the School of Computer Science and Cyber Engineering,         Hoare-style logic, is a well-established approach for formal
                                             Guangzhou University, Guangzhou 510006, China.
                                                                                                                           verification of pointer programs. SL is best at reasoning
                                                                                                                                2

about computer memory, especially random access memory            ment programs the data granularity of LMDSS is not fine
[21]. Through introducing a connective ∗ called separating        enough to accurately describe the process of reading and
conjunction, SL is able to reason about the shared mutable        appending data record in blocks. Second, the block variables
data structures (e.g., various types of linked lists, binary      and general variables are disconnected, which means we
search trees, and AVL trees). Besides, it has complete asser-     cannot get a value that can be used for general arithmetic
tions and specification rules support for logical reasoning.      operations from the block content data by some commands.
In view of data processing operations of files and blocks         Third, the assertions and specifications in LMDSS are based
in BCSSs management programs are similar to the ordinary          on SL, which has a strong theoretical and practical signif-
computer memory, SL may just meet the requirements. It            icance in verifying low-level storage model. But for BCSSs
seem that SL is a reasonable way to reason about BCSSs, but       model, these are not enough. So if we can enhance LMDSS
there are some following challenges that are specific to the      by redefining the block content values, connecting block and
complicated target system. (1). How to model the features of      general variables, and constructing a proof system, it should
the block-based storage structure? For example, a file consist    be capable to model the BCSSs management programs.
of a sequence of blocks located by block address. The low-            SL [22] is a mainstream formalization to verify the cor-
level heap-manipulating framework in SL cannot describe           rectness of traditional storage systems, which has a strong
the complicated structure. (2). How to construct the asser-       theoretical and practical significance. By using SL, N.T
tions and specifications according to the block-based storage     Smith et al. [3] verified the correctness of Cheney’s copy-
framework? While the key operations of SL, i.e. separating        ing garbage collector programs in memory management
conjunction ∗, permit the concise and flexible description        system. R. Jung et al. [14] extended SL and created the
of shared mutable data structures gracefully, they are not        Iris Logic, which supports the verification of concurrent
effective in describing the execute actions on the content of     programs. J. Berdine et al. [2] proposed the semantics of
blocks. (3). How to refine the specification rules to make        symbolic heaps, which is a variant of SL. In recent years,
them concise and effective? When considering a algorithm          most of the assertion languages based on SL have adopted
with while-loop, the cumbersome specification is difficult in     the symbolic heaps model. Recently, several studies [4], [5],
finding loop invariants. In order to accommodate to these         [16], [25] focused on the logical properties of SL. For exam-
requirements and restrictions, a novel framework with two-        ple, Q.T Ta et al. [25] presented a sequent-based deductive
tier heap structure is constructed, several new operators is      system for automatically proving entailments by the sym-
introduced to describe the properties of BCSSs, and a proof       bolic heap fragment with arbitrary user-defined inductive
system with Hoare-style specification rules is presented to       heap predicates. In addition, some verification systems have
reason about the block-manipulating programs.                     been implemented in SL [6], [15], [17], [24], [29].
    Formal verification is mature enough for developing the           The prior approach of SL to construct verification sys-
correctness of most computer programs. For example, P.            tems relies on the principle called “local reasoning”, which
Gardner and G. Nizik [18] proposed their work about local         was proposed by O’Hearn [19] as a solution for potential
reasoning for the POSIX file system. W.H Hesselink and            pointer aliasing problem in program verification. The key
M.I Lali [33] provided abstract definitions for file systems      idea of local reasoning is that even though each phrase
which are defined as a partial function from paths to data.       of a program can access all stores variables and heaps in
In addition, some efforts to formalize CSSs have been made.       principle, it usually only uses a few of them. Therefore, a
Stephen et al. [11] used formal methods to analyze data flow      specification and proof can concentrate on only portions of
and proposed an execution model for executing Pig Latin           the heaps that a program accesses. More specifically, two
scripts in cloud systems without sacrificing confidentiality      points are worth emphasizing. Point 1 is that every valid
of data. I. Pereverzeva et al. [20] founded a formal solution     specification {p}C{q} is “tight” in the sense that every cell,
for CSS development, which had the capability of modeling         which is actually used by C , must be either guaranteed to
large and elastic data storage system. However, all the above     exist by p or allocated by C . Point 2 is a proof method called
works cannot model or reason about the existed BCSSs.             Frame Rule to formalize local reasoning. Such rule which is
    Before the formal verification work, firstly a formal         an inference rule, allows one to derive a specification from a
model of the target system is created, which requires a for-      given one without ever referring to the actual implementa-
mal modeling language. However, due to the above special          tion of a program. However, SL cannot reason about BCSSs
features of BCSSs, it is difficult for existing formal methods    since it is based on a low-level storage model. Our novel
to describe the execution process of BCSSs management             model works directly on the characteristics of BCSSs, which
programs accurately from a view of data details. In our           can address all the aforementioned problems.
previous work [13], [26], we presented a formal language              In this paper, we propose a verification framework to
to describe management programs of Massive Data Storage           verify the correctness of BCSSs management programs. The
System (henceforth, LMDSS). It is an extension of WHILEh          main contributions are as follows.
[28] programming language with new ingredients to de-                 1) A novel framework with two-tier heap structure is
scribe file and block operations. Not only can describe mem-              constructed to reflect the characteristics of BCSSs,
ory management operations, it also describes block-based                  and a modeling language is defined based on the
storage mutation operations. However, there are three flaws               framework. Especially, we introduce the file and block
in LMDSS which make it difficult to describe the BCSSs                    expressions to describe the file-block relationship and
programming model: First, LMDSS regards the content of                    refined block content.
a block as a big integer. Although it is sufficient to describe       2) Assertions based on SL are constructed to describe
macroscopic file and block operations, for BCSSs manage-                  the properties of BCSSs. Several new operators are
                                                                                                                                    3

       introduced to describe the block-heap manipulating            is also extended to reflect the file-block relationship, such as
       operations, e.g., b1 # b2 asserts that the content of         StoresF . The whole computational states of the framework
       b1 is corresponding to b2 , which enables the block           is described later in Sect.3. In our model, the files are stored
       content to be obtained directly and leaves the address        as follows. A file variable f is mapped to a sequence of
       sequence of the block as an implied condition. Mean-          block addresses bloc1 , ..., block by StoresF . HeapsB maps
       while, we introduce quantifiers over block and file           each of these block addresses to a sequence of location
       variables, which makes the assertions more expres-            addresses. HeapsV maps each of these location addresses
       sive.                                                         to a value. In particular, not every location address must
    3) A proof system with the Hoare-style specification             belong to a certain block, the rest addresses in HeapsV are
       rules is proposed to reason about the BCSSs. The              likewise mapped to values. Notice that this novel model is
       specification rules, which support local reasoning, are       not simply a double combination of SL since there is a joint
       able to describe the behavior of block-manipulating           implication between the two tiers of the heap structure, i.e.,
       commands concisely, and some special situations are           some location address in HeapsV belongs to a certain block,
       addressed that suffice for formal proofs. An example          which SL cannot express.
       of verifying a practical algorithm with while-loop is
       given to demonstrate the feasibility of our method.
    The paper is organized as follows. Section 2 contains
background. Section 3 presents a modeling language for
BCSSs, and an assertion language based on SL is constructed
to describe the properties of BCSSs in Section 4. Section
5 proposes the Hoare-style proof system to reason about
the BCSSs. Section 6 prove that the Frame Rule for BCSSs
to reflect local reasoning is soundness. Section 7 gives an
illustrating example, and Section 8 draws conclusions.


2   BACKGROUND                                                       Fig. 1. Abstract Model of the Verification Framework
In HDFS, the DataNode stores the data blocks into local
filesystem directories. However, when writing new blocks
to it, there is no guarantee that HDFS will automatically            3     M ODELING L ANGUAGE FOR BCSS S
distribute data evenly among the DataNodes in a cluster, so
it can easily become imbalanced. That may lead to the fre-           In this section, the definition of the block content is adjusted
quent use of network bandwidth and low storage efficiency            based on LMDSS in the introduction in order to have a
[1].                                                                 better description of data processing in BCSSs management
     For redistributing data blocks when an imbalance occurs,        programs. Furthermore, we connect new block variables
HDFS provides a command line tool called Disk Balancer.              with general variables to reflect the characteristics of the
It is mainly implemented by an algorithm called Transfer,            block-based storage structure.
which can let administrators rebalance data across multiple
disks by moving blocks from one disk to another [24].                3.1   Syntax
Apparently, moving blocks is the key operation of Disk
                                                                     In our language there are four kinds of expressions: (arith-
Balancer, which should not lead to any memory errors such
                                                                     metic) location expressions, file expressions, block expres-
as block losing or content changed. Hence, formal reasoning
                                                                     sions, and Boolean expressions. The full syntax for expres-
is of fundamental importance for this operation.
                                                                     sions and commands in the language is as follows.
     SL is often used in reasoning about heap-manipulating
programs. However, SL cannot reason about BCSSs since
it is difficult to describe the execution process of the man-         e    ::= n | x, y, ... | e1 + e2 | e1 − e2 | e1 × e2 | #f | #bk
agement programs accurately from a view of block oper-               fe    ::= nil | f | f e · bk | f e1 · f e2
ation details. Taking the Disk Balancer as an example, it
involves lots of execute actions on the content of blocks,           bk    ::= n | b | f.e
which is hard for SL to construct the specifications. Besides,       be    ::= e1 = e2 | e1 ≤ e2 | bk1 == bk2 | true | false | ¬be |
SL cannot check whether the file is consistent before or                       be1 ∧ be2 | be1 ∨ be2
after the execution. Therefore, it is necessary to construct         C     ::= x := e | x := cons(ē) | x := [e] | [e] := e0 |
a verification framework of BCSSs to prove the correctness
problems caused by the complexity of the block-based stor-                     dispose(e) | f := create(bk ∗ ) | attach(f, bk ∗ ) |
age structure according to the characteristics of BCSSs.                       delete f | b := allocate(ē) | append(bk, e) |
     The main concepts of the proposed framework is illus-                     x := {bk.e} | b := bk | delete bk | f.e := bk |
trated in the rest of the section. An initial, high level, and in-             C; C 0 | if be then C else C 0 | while be do C 0
complete abstract model of the framework is shown in Fig.1.
To describe the BCSSs management programs, the SL heap                  where e is written for location expressions, f e for file
is extended by introducing a two-tier heap structure, which          expressions, bk for block expressions, be for Boolean expres-
is consist of HeapsB and HeapsV , while the ordinary store           sions, and C for commands.
                                                                                                                                                                 4

     Intuitively, #f means the block numbers the file f                subset BLoc of the integers, and it is accessed using indirect
occupies, and f.e points out the address that the i-th block           addressing {bk}, where bk is a block expression.
of the file f corresponds to, where i is the value of the lo-
cation expression e. For brevity, we abbreviate the sequence
e1 , ..., en of the location expressions by ē, and the sequence       Values , {... − 1, 0, 1, ...} = Z                   Loc, BLoc, Atoms ⊆ Values
bk1 , ..., bk2 of the block expressions by bk ∗ .                      Var , {x, y, ...} BKVar , {b1 , b2 , ...} FVar , {f1 , f2 , ...}
     Besides the commands in WHILEh, which contains all                StoresV , Var → Values                        StoresB , BKVar → BLoc
commands of IMP [27], we introduce some new commands                                                         ∗
                                                                       StoresF , FVar → BLoc
to describe the special operations about files and blocks in
the BCSSs management programs.                                         HeapsB , BLoc *fin Loc∗                           HeapsV , Loc *fin Values
     File commands contain four core operations, which seem
                                                                           where * and *fin can be found in [30]. Loc, BLoc
to be enough to describe the majority of daily-file operations
                                                                       and Atoms are disjoint, and BLoc∗ = {(bloc1 , ..., blocn ) |
in CSSs.
                                                                       bloci ∈ BLoc, n ∈ N}, and for any element (bloc1 , ...,
                        ∗
   • f := create(bk ):                                file creation;   blocn ) of BLoc∗ , |(bloc1 , ..., blocn )| means its length, that is,
                      ∗
   • attach(f, bk ):                  block address appending;         |(bloc1 , ..., blocn )| = n. Similarly, Loc∗ = {(loc1 , ..., locn ) |
   • delete f :                                       file deletion.   loci ∈ Loc, n ∈ N}.
     The file creation command creates a file that consists of             To make sure the successful allocation, we place the
block sequence at block addresses expressed by bk ∗ . The              following requirements on the sets of Loc and BLoc. For
block address appending command can append blocks at                   any positive integer m, there are infinitely many sequences
block addresses bk ∗ to an existing file. The file deletion            of length m of consecutive integers in Loc. For any positive
command removes a file and all blocks belong to it become              integer n, there are infinitely many sequences of length m
orphaned.                                                              of discrete integers in BLoc. These requirement are satisfied
     Block commands express block operations. They are as              if we take Loc and BLoc as the non-negative integers. Then
follows.                                                               we can take Atoms as the negative integers, and nil as -1.
   • b := allocate(ē):                           block allocation;        The states of our language are defined as follows:
   • append(bk, e):                       block content append;        States , StoresF × StoresB × StoresV × HeapsB × HeapsV
   • x := {bk.e}:                         block content lookup;
   • b := bk :                        block address assignment;              A state σ ∈ States is a 5-tuple: (sF , sB , sV , hB , hV ).
   • f.e := bk :              block address of a file assignment;
   • delete bk :                                    block deletion.    3.3     Semantics of the modeling language
     The block allocation command creates a block with the
                                                                       Once the states are defined, we can specify the evaluation
initial value ē, which is the content data of the block. The
                                                                       rules of our new expressions. Notice that when we try to
block content append command appends data e after the
                                                                       give out the semantic of an expression, some stores and
content. Since the content of a block is an integer value
                                                                       heaps may not be used. For example, expression #f only
sequence at present, the block content lookup command
                                                                       needs StoresF and StoresV . So we will only list the necessary
reads the content of the i-th field of the block bk , where
                                                                       stores and heaps for each expression. The semantics of the
i is the evaluation of expression e. The block address as-
                                                                       expressions which is similar to LMDSS can be found in [13].
signment command assigns value bk to block variable b. In
                                                                       Here we give out the semantics of new expressions. One
most of the time, this command is used for the situation
                                                                       is the block content length expression #bk , which is used
involving the file operations, so we add the block address
                                                                       to calculate the content size of the block at address bk . Note
of a file assignment command as an alternative to make
                                                                       that in the extended language the content of a block will be a
the modeling language more powerful. The block deletion
                                                                       sequence of integers. This expression will count the length of
command is formulated similarly as file deletion command
                                                                       this sequence. So we can find out how much data(integers)
with the difference in replacing the file variable by block
                                                                       has been written in the current block, and then calculate
variable.
                                                                       how much data can be write to this clock, for the maximum
                                                                       size of a block in the system is fixed. The denotational
3.2   Domains                                                          semantics of expression #bk is in the following.
                                                                              J#bkK(sF )(sB )(sV )(hB ) = k,
The model has five components: StoresV , StoresB , StoresF ,                  where hB (JbkK(sF )(sB )(sV )(hB )) = (loc1 , loc2 , ..., lock ),
HeapsV , and HeapsB . StoresV is a total function mapping                  The others are file expressions, the denotational seman-
from location variables to addresses. StoresB denotes a total          tics of file expressions is ruled out by the following func-
function mapping from block variables to block addresses.              tions:
                                                                              JnilK(sF ) = ();
Strictly speaking, values, addresses, and block addresses are                 Jf K(sF ) = sF (f );
different in type. But in our language, to permit unrestricted                Jf e · bkK(sF )(sB ) = (bloc1 , . . . , blocn , bloc0 ),
address arithmetic, we assume that all the values, addresses,                 if Jf eK(sF )(sB ) = (bloc1 , . . . , blocn ) and JbkK(sB ) = bloc0 ;
and block addresses are integers. StoresF represents a total                  Jf e1 · f e2 K(sF )(sB ) = (bloc1 , . . . , blocn , bloc1 0 , . . . , blocn 0 ),
                                                                              if Jf e1 K(sF )(sB ) = (bloc1 , . . . , blocn ) and
function mapping from file variables into a sequence of                       Jf e2 K(sF )(sB ) = (bloc1 0 , . . . , blocn 0 ).
block addresses. HeapsV is indexed by a subset Loc of the                 To state the semantics of the modeling language for-
integers, and it is accessed using indirect addressing [e],            mally, following [28], we use the crucial operations on the
where e is a location expression. HeapsB is indexed by a               heaps:
                                                                                                                                                           5

  • dom(hH ) denotes the domain of a heap hH ∈ HeapsH ,                                4     A SSERTION L ANGUAGE FOR BCSS S
    where hH range over hV and hB , HeapsH range over                                  To describe the properties of BCSSs, we construct a logic to
    HeapsV and HeapsB , and dom(sS ) is the domain of a                                deal with both locations and blocks. BI Pointer Logic [10]
    store sS ∈ StoresS , where sS range over sV , sB and sF ,                          provides a powerful formalism for ordinary locations. We
    StoresS range over StoresV , StoresB and StoresF ;                                 extend BI pointer logic with the file and block expressions
              0                                          0
  • hH #hH indicates that the domains of hH and hH are                                 to describe the file-block relationship. Following [28], the
    disjoint;                                                                          formal semantics of an assertion is defined by a satisfactory
              0                          0
  • hH ∗ hH is defined when hH #hH holds and is a finite                               relation “ |= ” between a state and an assertion. σ |= p means
    function obtained by taking the union of hH and hH 0 ;                             that the assertion p holds in the state σ .
  • i 7→ j is a singleton partial function which maps i to j ;                             We rename the assertions of BI pointer logic as loca-
                                                 0
  • for a partial function f from U to W and f from V to                               tion assertions, meanwhile call the block formulas as block
                                   0
    W , the partial function f [f ] from U to W is defined                             assertions. Both location assertions and block assertions are
    by:                                                                                built on expressions. The key challenge is that the assertion
                                                                                       language should be able to express the two-tier structure of
                                   f 0 (i)   if i ∈ dom(f 0 ),
                           
                  0
                                                                                      the framework.
            f [f ](i) ,            f (i)     if i ∈ dom(f ),
                                   undefined otherwise.
                           
                                                                                       4.1    Location Assertion
   Here we give out the denotational semantics of our new Syntax. Location assertions describe the properties of loca-
commands.                                                                       tions. However, there are some differences between the BI
                                                                                assertions and the location assertions. Quantifiers over block
                                                                                and file variables are allowed in location assertions. This
                     ∗
    Jf := create(bk )Kσ = (sF [(Jbk1 Kσ, ..., Jbkn Kσ)/f ], sB , sV , hB , hV ) makes the location assertions much more complicated since
    where the term of sequence determined by hB (Jbki Kσ) (1 ≤ i ≤ n) belong they are not first-order quantifiers.
      todom(hV );
                      ∗
      Jattach(f, bk )Kσ = (sF [(sF (f )  (Jbk1 Kσ, ..., Jbkn Kσ))/f ], sB , sV , hB
      , hV )where the term of sequence determined by hB (Jbki Kσ) (1 ≤ i ≤ n)
                                                                                       α     ::= trueV | falseV | ¬α | α1 ∧ α2 | α1 ∨ α2 | α1 → α2
      belong to dom(hV );                                                                         | e1 = e2 | e1 ≤ e2 | ∀x.α | ∃x.α | | ∀f.α | ∃f.α |
      Jdelete f K(sF , sB , sV , hB , hV ) = (sF [JnilKσ/f ], sB , sV , hB , hV );               ∀b.α | ∃b.α | empV | e 7→ e0 | α1 ∗ α2 | α1 −∗ α2
      Jb := allocate(ē)Kσ = (sF , sB [bloc/b], sV , hB [(loc1 , ..., locn )/bloc],
      [hV |loc1 : Je1 Kσ, ..., locn : Jen Kσ])
                                                                                       Semantics. Intuitively, the truth value of a location assertion
      where bloc ∈ BLoc − dom(hB ) , and loc1 , ..., locn ∈ Loc − dom(hV );
                                                                                       depends only on the stores and heaps for location variables.
                                                                                       Given a location assertion α, we define σ |= α by induction
      Jappend(bk, e)Kσ = (sF , sB , sV , hB [(loc1 , ..., locm , locm+1 )/JbkKσ],
                                                                                       on α in the following.
      [hV |locm+1 : JeKσ]) where hB (JbkKσ) = (loc1 , ..., locm ), the term of
      sequence (loc1 , ..., locm ) belong to dom(hV ), and locm+1 ∈ Loc−                  • σ |= trueV ;

      dom(hV );                                                                           • σ |= α1 → α2 iff if σ |= α1 then σ |= α2 ;
                                                                                          • σ |= (∀x.α) iff sF , sB , sV [n/x], hB , hV |= α for any n ∈
      Jx := {bk.e}Kσ = (sF , sB , sV [hV (loci )/x], hB , hV )
      where hB (JbkKσ) = (loc1 , ..., locm ),JeKσ = i and 1 ≤ i ≤ m;
                                                                                            Loc;
                                                                                          • σ |= (∀f.α) iff sF [n̄/f ], sB , sV , hB , hV |= α
      Jb := bkKσ = (sF , sB [JbkKσ/b], sV , hB , hV );
                                                                                            for any n̄ = (n1 , n2 , . . . , nk ) ∈ BlockLoc*;
      Jf.e := bkKσ = (sF [(bloc1 , ..., JbkKσ, ..., blocn )/f ], sB , sV , hB , hV )      • σ |= (∃f.α) iff sF [n̄/f ], sB , sV , hB , hV |= α
      where sF (f ) = (bloc1 , ..., bloci , ..., blocn ),JeKσ = i and 1 ≤ i ≤ n;
                                                                                            for some n̄ = (n1 , n2 , . . . , nk ) ∈ BlockLoc*;
      Jdelete bKσ = (sF , sB , sV , hB e(dom(hB ) − {JbKσ}), hV ).                        • σ |= empV iff dom(hV ) = ∅;
                                                                                                          0                                              0
                                                                                          • σ |= e 7→ e iff dom(hV ) = {JeKσ} ∧ hV (JeKσ) = Je Kσ ;
                                                                                                                                1   2
                                                                                          • σ |= α1 ∗ α2 iff there exist hV , hV with
                                                                                            h1V #h2V and hV = h1V ∗h2V such that
                                                                                            sF , sB , sV , hB , h1V |= α1 and sF , sB , sV , hB , h2V |= α2 .
3.4   A Semantic Example                                                                   Definition of other location assertions are similar to these
                                                                                       in BI pointer logic.
At this stage we will give a slightly nontrivial example of a
formal proof with our modeling language. In the example,
                                                                                       4.2    Block Assertion
according to the denotational semantics, we derive a final
state from the initial state by steps. The final state describes                       Syntax. Block assertions describe the properties about
the configuration of the system after running the program,                             blocks. So they include the logic operations and heap
which achieved the expected results. This results show the                             operations on block expressions besides ordinary logical
modeling language is expressive enough to describe the                                 connectives and quantifies.
management programs in BCSSs, and the semantics is strict
and feasible. The modeling language and its semantic pro-                              β     ::= trueB | falseB | ¬β | β1 ∧ β2 | β1 ∨ β2 | β1 → β2
vide the basis for the nature of BCSSs research. Hence, we
                                                                                                  | bk1 == bk2 | bk == bk1 ~ · · · ~ bkn | ∀x.β |
can define our assertion language and prove the correctness
of management programs. The description of the example                                           ∃x.β | ∀b.β | ∃b.β | ∀f.β | ∃f.β | empB |
and all proofs are relegated to Appendix A.                                                      bk 7→ (ē) | β1 ∗ β2 | β1 −∗ β2 | f e = f e0 | b1 # b2
                                                                                                                                        6

Semantics. Obviously, the truth value of a block assertion           we define sV , sB , sF , hV , hB |= p by induction on p in the
depends on the stores and heaps for blocks. Given a block            following.
assertion β , we define σ |= β by induction on β as follows.
                                                                       • true , htrueV , trueB i; emp , hempV , empB i;
   • σ |= trueB ;
                                                                       • σ |= hα, βi iff σ |= α and σ |= β ;
   • σ |= bk1 == bk2 iff Jbk1 Kσ = Jbk2 Kσ ;
                                                                       • σ |= ¬p iff σ 6|= p;
   • σ |= bk == bk1 ~ · · · ~ bkn iff JbkKσ = Jbk1 Kσ · · · · ·
                                                                       • σ |= p1 ∨ p2 iff σ |= p1 or σ |= p2 ;
      Jbkn Kσ and Jbki Kσ⊥Jbkj Kσ                                      • σ |= p1 → p2 iff if σ |= p1 then σ |= p2 ;
      for all i, j ∈ N, 1 ≤ i < j ≤ n                                  • σ   |= ∀x.p iff sV [n/x], sB , sF , hV , hB |= p for any
   • σ |= (∀x.β) iff sF , sB , sV [n/x], hB , hV |= β
                                                                         n ∈ Loc;
      for any n ∈ Loc;                                                 • σ |= ∀b.p iff sV , sB [n/b], sF , hV , hB |= p        for any n ∈
   • σ |= (∃b.β) iff sF , sB [n/b], sV , hB , hV |= β
                                                                         BLoc;
      for some n ∈ BLoc;                                               • σ |= ∀f.p iff sV , sB , sF [n̄/f ], hV , hB |= p
   • σ |= (∀f.β) iff sF [n̄/f ], sB , sV , hB , hV |= β
                                                                         for any n̄ = (n1 , n2 ,. . ., nk ) ∈ BLoc*;
      for any n̄ = (n1 , n2 , . . . , nk ) ∈ BLoc*;                    • σ |= emp iff dom(hV ) = ∅ and dom(hB ) = ∅;
   • σ |= bk 7→ (ē) iff dom(hB ) = {JbkKσ},                                                                                    1     2
                                                                       • sV , sB , sF , hV , hB |= p1 ∗p2 iff there exists hH , hH with
      hB (JbkKσ) = (Je1 Kσ, ..., Jen Kσ), and                              1     2                  1
                                                                         hH #hH and hH = hH ∗ hH such that 2
      Jei Kσ ∈ dom(hV ) (1 ≤ i ≤ n);                                     sV , sB , sF , h1V , h1B |= p1 and sV , sB , sF , h2V , h2B |= p2
                                                     0
   • σ |= (β1 −∗ β2 ) iff for any block heap hB ,
            0                                0                           where hiH range over hiV and hiB and i = 1, 2;
      if hB #hB and sF , sB , sV , hB , hV |= β1 ,                     • σ |= (p1 −∗ p2 ) iff for any block heap hH ,
                                                                                                                           0
      then sF , sB , sV , hB ∗hB 0 , hV |= β2 ;                                0                               0
                                                                         if hH #hH and sV , sB , sF , hV , hB |= p1 ,0
                     0                      0
   • σ |= f e = f e iff Jf eKσ = Jf e Kσ ;
                                                                         then sV , sB , sF , hV ∗ hV 0 , hB ∗ hB 0 |= p2 ,
   • σ |= b1 # b2 iff sB (b1 ) ∈ dom(hB ) when b1 = b2 or
                                                                         where hH range over hV and hB .
      hV (hB (sB (b1 ))) = hV (hB (sB (b2 ))) when b1 6= b2 .
                                                                         Notice that, in the semantic of hα, βi, we do not just
    where the notation · means the concatenation of se-
                                                                     simply use α ∧ β here, because such form will mislead
quences, and ⊥ denotes two sequences have no common
                                                                     the reader that block assertions can be used all alone. In
subsequence.
                                                                     practical, the content of blocks are stored in HeapsV for the
    It is noticed that quantifiers over block and file vari-
                                                                     architecture of BCSSs. In our setting, location assertions and
ables are necessary for the assertions. In the specification
                                                                     block assertions work together to describe the blocks cor-
language, we need to express the existence of a sequence
                                                                     rectly, and the pair form can elegantly express the relation
of addresses due to the inherent complexity of BCSSs. If
                                                                     between the two tiers as well as the properties of BCSSs.
the length of the sequence is dynamic, for example in a
while loop, we cannot use the existence of location variables            It is convenient to introduce several complex forms as
because the number of the variables is indeterminate. We             abbreviations below, which are from [22], where some simi-
address this case by introducing the quantifier over block           lar terminologies can be found. For brevity, we use location
variable that implicitly shows the dynamic length of the             variable l to denote the address, and location variable x
address sequence.                                                    denotes the content, which will be more readable.
    In addition, we define some new block assertions to                • e 7→ e1 , ..., en , e1 7→ e1 ∗ ... ∗ e + n − 1 7→ en
describe the address sequence and the content of a block,              • bk 7→ ¯
                                                                               l , bk 7→ (l1 , ..., ln ) where #bk = |¯l| = n;
for example, bk 7→ (ē) and b1 # b2 . In these assertions,             • ¯
                                                                         l # (ē|i  x) , l1 7→ e1 ∗ ... ∗ li 7→ x ∗ ... ∗ ln 7→ en ;
we straightly show the content of blocks and leaves the                • ¯
                                                                         l # (ē[x0 /x]|i  x00 ) , l1 7→ e1 [x0 /x] ∗ ... ∗ li 7→
address sequence as an implied condition. In the specifica-              x00 ∗ ... ∗ ln 7→ en [x0 /x];
tion language, some commands only change the content of                • bk # ē , ∃x̄.hx̄ # ē, bk 7→ x̄i where |x̄| = |ē| and the
a block, so we do not need to describe the address sequence              term of sequence x̄ are disjoint;
                                                                               0
in pre- and post-conditions, this improvement permits the              • e ,→ e  , e 7→ e0 ∗ trueV ;
concise description of the inference rules. Furthermore, with          • bk ,→ (ē) , bk 7→ (ē) ∗ trueB .
the quantifiers over block variables, the assertion language
                                                                        The advantages of global assertions are threefold:
could express the change of block content flexibly.
                                                                      1) The pair form of global assertions is consistent with the
4.3    Global Assertion                                                  hierarchical structural of the framework. Location and
                                                                         block assertions can describe the state of HeapsV and
Syntax. Roughly speaking, (location assertion,block assertion)
                                                                         HeapsB , respectively. Meanwhile, the pair can exactly
pairs are called global assertions, and the two components of
                                                                         express the content of each block.
a pair effect each other. We use the symbol p to stand for the
                                                                      2) We mainly focus on the properties of blocks in BCSSs.
global assertions, with the following BNF equation:
                                                                         With the new defined notations ==, 7→, and #, we are
                                                                         able to describe the address sequence and the content
p     ::= hα, βi | true | false | ¬p | p1 ∧ p2 | p1 ∨ p2 | p1 → p2       of a block.
           | ∀x.p | ∃x.p | ∀b.p | ∃b.p | ∀f.p | ∃f.p |                3) We introduce quantifiers over block and file variables,
                                                                         which makes the assertion language more expressive.
          emp | p1 ∗ p2 | p1 −∗ p2
                                                                         Combined with the new defined assertions, we are able
Semantics. The truth value of a global assertion depends on              to write the pre- and post-conditions in Hoare triples,
all kinds of stores and heaps. Given a global assertion p,               especially the while loop invariants.
                                                                                                                                              7

   With the advantages, our logic is quite different from SL,              Transfer Function. According to syntax, any Boolean ex-
and more complicated. The assertion language can support                   pression cannot be any kind of assertion. Hence, it cannot
the specification language well. More discussions about                    appear in any specification. Thus Boolean expressions in if
assertion language will be discussed in the future.                        or while commands cannot be used directly in pre- or post-
                                                                           conditions. To fix this problem, we define the transfer func-
5     H OARE - STYLE P ROOF S YSTEM FOR BCSS S                             tion T that maps Boolean expressions to global assertions.
For reasoning about management programs in BCSSs, com-
                                                                               T ∈ Transfer functions = Boolean expressions * Global
                                                                           assertions
bining with the modeling language and the assertion lan-
guage above, we introduce a Hoare-style proof system. The                   T (e1 = e2 ) = he1 = e2 , trueB i
main concept in Hoare-style logic are Hoare triples, which                  T (e1 ≤ e2 ) = he1 ≤ e2 , trueB i
consists of a precondition, a program, and a postcondition.
In our setting, we restrict the pre- and post-conditions to be              T (bk1 == bk2 ) = htrueV , bk1 == bk2 i
global assertions only. Formally, a Hoare triple is of the form             T (be1 ∧ be2 ) = T (be1 ) ∧ T (be2 )
{p} C {q}, where p and q are global assertion, and C is a                   T (be1 ∨ be2 ) = T (be1 ) ∨ T (be2 )
command.                                                                    T (true) = true T (false) = false T (¬be) = ¬T (be)
5.1   Local Reasoning                                                       T (abort) = abort
To define the semantics of Hoare triples , two point of local
reasoning from the Introduction are recalled as follows.                   5.3     The Proof System
    Point 1: Every valid specification {p}C{q} is “tight”,                 In this section, we present the proof system for BCSSs, which
that is to say when C runs in a state satisfying p, it must                consists of the axioms, the compound command rules, and
dereference only those cells that guaranteed to exist by p or              the structural rules. We propose one or more axioms for each
allocated during the execution by possible commands like                   basic command. Similar to BI pointer logic, the compound
x := cons(e1 , ..., en ) or f := create(bk ∗ ).                            command rules and the structural rules does not depend on
    Point 2: An inference rule about specification, known as               particular programming constructs.
the Frame Rule, enables us obtain {p ∗ r}C{q ∗ r} from the                 Axioms. Firstly, we give the original axioms of SL. The
initial specification {p}C{q} of a command when premise                    pre- and post-conditions are both given in the form of
of the Frame Rule is valid. Thus, we can concentrate on the                hlocation assertion, block assertioni since they are global as-
variables and parts of heaps that are actually accessed by                 sertions. It is observed that these cases do not involve files
the program which is ensured correct by Point 1, and we                    or block operations, so all of the rules given here remain
can extend a local specification by using the Frame Rule. We               valid for our logic.
will proof soundness of the Frame Rule in Sect.6.                             •   Skip
                                                                                                                  {p} skip {p}              (A1)

5.2   Interpretation of Hoare Triples                                         •   The Simple Assignment form (SA)
                                                                                                       0
                                                                                               {hx = x ∧ empV , empB i} x := e
Interpretation of Hoare Triples. According to Point 1, a tight                                                0                             (A2)
                                                                                                {hx = e[x /x] ∧ empV , empB i}
interpretation of specifications does not dereference the non-
addresses, otherwise it will lead to an error memory fault or              where x0 is distinct from x.
                                                                             • The Location Allocation form (LA)
fault for short.                                                                                  0
                                                                                        {hx = x ∧ empV , empB i} x := cons(e1 , ..., en )
    We use the terminologies below to specify                                                        0                  0                   (A3)
                                                                                         {hx 7→ e1 [x /x], ..., en [x /x], empB i}
the certain properties of the program execu-
tion.    “hC, (sV , sB , sF , hV , hB )i           is   safe      ” when   where x0 is distinct from x.
                                         ∗                                   • The Location Lookup form (LL)
hC, (sV , sB , sF , hV , hB )i                   fault is impossible;                                   0       00
                                                                                                {hx = x ∧ e 7→ x , empB i} x := [e]
“hC, (sV , sB , sF , hV , hB )i must terminate normally” when                                            00         0       00              (A4)
                                                                                               {hx = x ∧ e[x /x] 7→ x , empB i}
hC, (sV , sB , sF , hV , hB )i is safe and there exists no infinite
     − sequences starting from hC, (sV , sB , sF , hV , hB )i.             where x, x0 , and x00 are distinct.
                                                                             • The Location Mutation form (LM)
Each Hoare triple can be interpreted for partial correctness                                                         0        0
                                                                                           {he 7→ −, empB i} [e] := e {he 7→ e , empB i}    (A5)
and for total correctness as follows.
    Partial Correctness:                                                      •   The Deallocation form (DL)
      {p}C{q} is true iff for ∀(sV , sB , sF , hV , hB ).                               {he 7→ −, empB i} dispose(e) {hempV , empB i}       (A6)
                    if (sV , sB , sF , hV , hB ) |= p then
                    1.hC, (sV , sB , sF , hV , hB )i is safe
                                                                               Commands of file will change StoresF , which may have
                    2. if hC, (sV , sB , sF , hV , hB )i ∗
                                                                           impact on both location assertions and block assertions. To
                    (sV 0 , sB 0 , sF 0 , hV 0 , hB 0 )                    make axioms simple, we only discuss the situation when the
                    then (sV 0 , sB 0 , sF 0 , hV 0 , hB 0 ) |= q          file changed in commands does not appear in the location
    Total Correctness:
      {p}C{q} is true iff for ∀(sV , sB , sF , hV , hB ).                  assertion. In A8, one may argue that it cannot be applied
                    if (sV , sB , sF , hV , hB ) |= p then                 when file expression #f appears in the assertion. To this
                    1.hC, (sV , sB , sF , hV , hB )i must terminate        end, we construct an alternative axiom for A8, which is
                    2. if hC, (sV , sB , sF , hV , hB )i ∗                 described latter in Sect.5.4. For the moment, we ignore
                    (sV 0 , sB 0 , sF 0 , hV 0 , hB 0 )                    particular specifications, and give the common axioms that
                    then (sV 0 , sB 0 , sF 0 , hV 0 , hB 0 ) |= q          suffice for formal proofs.
                                                                                                                                                                                                        8
                                                                                                                0   00                            0                        00            0         00
                                                                                                        {∃b, b , b , l.h#b = i − 1 ∧ x = x ∧ e = i ∧ l ,→ x , bk == b ~ b ~ b
  • The File Creation form (FC)                                                                             0                                 0       00                            00       0
                                                                                                         ∧ b ,→ (l)i} x := {bk.e} {∃b, b , b , l.h#b = i − 1 ∧ x = x ∧ e[x /x]
 {hα, f = nil ∧ βi} f := create(bk1 , ..., bkn ) {hα, β[(bk1 , ..., bkn )/f ]i}                                            00             0    00          0
                                                                             (A7)                        = i ∧ l ,→ x , bk == b ~ b ~ b ∧ b ,→ (l)i}
where f is not free in α or bk1 , ..., bkn .                                                                                                                                                     (A15)
  • The Block Address Appending form (BAA)                                                                          0           00
                                                                                                       where x, x , and x are distinct.
                                    0
                 {hα, f = f ∧ βi} attach(f, bk1 , ..., bkn )                                             • The Block Address Assignment form (BAA)
                        0                   0           0             0                         (A8)                        0                         0                0            0
                 {hα[f /f ], β[f · (bk1 [f /f ], ..., bkn [f /f ])/f ]}                                   {hα, b == b ∧ βi} b := bk {hα[b /b], b == bk[b /b] ∧ β[b /b]i}                         (A16)
          0                                                                                                     0
where f is distinct from f .                                                                           where b is distinct from b.
  • The File Deletion form (FD)                                                                          • Alternative Axiom for Block Address Assignment (BAAalt)
                         0                 0                                                                                                                   0
            {hα, f = f ∧ βi} delete f {hα[f /f ], β[nil/f ]i}                                   (A9)                     {h#f2 = i − 1 ∧ α, f = f2 · b · f3 ∧ βi} b := f.i
                                                                                                                                                               0                0                (A17)
                                                                                                                         {h#f2 = i − 1 ∧ α, f = f2 · b · f3 ∧ b == b ∧ βi}
          0
where f is distinct from f .
                                                                                                       where b0 is distinct from b, and b is not free in α or β .
      Finally, we come to the block commands for manipulat-
                                                                                                         • The Block Address Replacement of a File form (BARF)
ing the HeapsB , which gives rise to a surprising variety of                                                                                                       0
                                                                                                                        {h#f2 = e − 1 ∧ α, f = f2 · bk · f3 ∧ βi} f.e := bk
axioms. For some commands, two axioms are given to make                                                                 {h#f2 = e − 1 ∧ α, f = f2 · bk · f3 ∧ βi}
                                                                                                                                                                                                 (A18)
the specification language more expressive. To explain these
                                                                                                       where f.e does not appear in α or β .
axioms, we begin with A10. Here, for a precondition with
                                                                                                         • The Block Deletion form (BD)
empty HeapsV and HeapsB (to show locality), the post-                                                              {∃l̄.hl̄ # −, b 7→ l̄i} delete b {∃l̄.hl̄ # −, empB i}                        (A19)
condition says that a new block is created with a sequence
of location addresses, and the content of these addresses                                              where b does not appear in the expressions which are omitted.
is ē. The restrictions on this axiom are needed to avoid                                                  For space reasons, the soundness of the axioms given
aliasing. But this axiom cannot be applied generally since                                             above is proved in the appendix of [12].
the postcondition of a specific form restricts our reasoning.                                          Rules. In contrast to aforementioned axioms, the rules are
Especially, the quantifiers over a sequence of location ad-                                            applicable to arbitrary commands, which are be called
dresses cannot appear in while loop invariants. Therefore,                                             structural rules. In our new setting, the command-specific
an alternative axiom A11 is given to avoid these complex                                               inference rules and the structural rules of SL remain sound.
quantification using block variables. The rest axioms will be                                              Rule of composition applies to sequentially executed
proceed similarly if necessary. Notice that in A12 and A13,                                            programs.
we can not substitute empV for α since bk is well-defined.                                                                {p} C {q} {q} C 0 {r}
                                                                                                                                                               (R1)
      When we turn to the axiom for block content lookup, the                                                                  {p} C; C 0 {r}
situation becomes more complicated since such command
                                                                                                           Conditional rule states that a postcondition common to
involves refined block content, i.e., query the content of a
                                                                                                       then and else part is also a postcondition of the whole if
certain location address belonging to a block. The difficulty
                                                                                                       statement.
with this axiom is the accumulation of quantifiers. In A15,
one can think of b0 as the first part of block bk , and b00                                                               {p ∧ T (be)}C{q} {p ∧ ¬T (be)}C 0 {q}
denotes the latter part. While, b denotes a singleton block                                                                                                                                      (R2)
                                                                                                                               {p} if be then C else C 0 {q}
heap, the content of which is a single address l with content
x00 .                                                                                                      If the evaluation of be causes an abort, we can use the
      In most time, we use block address assignment com-                                               following rule to show the program aborts.
mand to assign the content of a file block to a new block,
so an axiom A17 is added in the special case of A16 to make                                             {r1 ∧T (be) = abort} if be then c1 else c2 {abort} (R2A)
the specifications more powerful. The remaining axioms are
relatively well-understood, and not explained in detail.                                                  While rule states that the loop invariant is preserved by
   •    The Block Allocation form (BA)                                                                 the loop body.
         {hempV , empB i} b := allocate(ē) {∃l̄.hl̄ # ē, b 7→ l̄i}                           (A10)
                                                                                                                                      {p ∧ T (be)}C 0 {p}
where b is not free in ē.                                                                                                                                                                       (R3)
                                                                                                                                {p} while be do C 0 {p ∧ ¬T (be)}
    • Alternative Axiom for Block Allocation (BAalt)
                                                  0                      0     0      0
  {hempV , empB i} b := allocate(ē) {∃b .htrueV , b == b ∧ b # b i}                                      Similar to R2A, R3A shows the program aborts when
                                                                                      (A11)
where b is not free in ē.                                                                             evaluating be.
    • The Block Content Append form (BCA)

{∃l¯0 .hl¯0 # e¯0 , bk 7→ l¯0 i} append(bk, e) {∃l¯0 , l.hl¯0 # e¯0 ∗l 7→ e, bk 7→ l¯0 ·(l)i}
                                                                                      (A12)                 {r ∧ T (be) = abort} while be do c {abort}                                   (R3A)
where bk is not free in e¯0 , ē and #bk does not appear in bk.
    • Alternative Axiom for Block Content Append (BCAalt)                                                  We use FV(C) to denote the set of free variables which
    0                           0       0       0
{∃b .htrueV , bk == b ∧ b # b i} append(bk, e)                                                         occur in C , and Modify(C) represents the set of variables
    0    00                                         0            00        0       0   00
{∃b , b , l.htrueV ∗ l 7→ e, bk == b ~ b ∧ trueB ∗ b # b ∗ b                                7→ (l)i}   modified by C , which appear on a left side of an assignment
                                                                                               (A13)   statement. Let V arV be a set of location variables, V arB
where bk is not free in e¯0 , ē and #bk does not appear in bk.                                        be a set of block variables, V arF be a set of file variables,
  • The Block Content Lookup form (BCL)                                                                and V arS range over V arV , V arB , and V arF ; YS be the
                0                                           00
   {∃l̄.hx = x ∧ e = i ∧ l̄ # (ē|i  x ), bk 7→ l̄i} x := {bk.e}                                      set of variables that all allocated variables in stores are
                00          0                                    0    00       0               (A14)
   {∃l̄.hx = x ∧ e[x /x] = i ∧ l̄ # (ē[x /x]|i  x ), bk[x /x] 7→ l̄i}                                precisely in and YS range over YV , YB , and YF ; XS be the
where x, x0 , and x00 are distinct.                                                                    set of variables modified by C and XS range over XV ,XB ,
  • Alternative Axiom for Block Content Lookup (BCLalt)                                                and XF . Then, for commands C with ModifyV (C) = XV ,
                                                                                                                                      9

ModifyB (C) = XB , ModifyF (C) = XF , X = XV ∪ XB ∪                  6    S OUNDNESS OF THE F RAME R ULE FOR BCSS S
XF , and FV(C) ⊆ Y , we give the following structural rules.         In this section, we undertake to prove that the Frame Rule
   Consequence Rules:                                                for BCSSs is soundness. The soundness result guarantees
              |= p0 → p    {p}C{q} |= q → q 0                        that the approach we formalize local reasoning is valid.
                                                             (R4)    Recall the structural rules, we have the syntactic version of
                           {p0 }C{q 0 }
                                                                     the Frame Rule:
   Auxiliary Variable Elimination:                                              {p} − {q}
                                                                                                   ModifyS (C) ∩ FV(r) = ∅
                                                                             {p ∗ r} − {q ∗ r}
                  {p}C{q}
                                      xS ∈
                                         / FV(C)             (R5)    where ModifyS (C) range over ModifyV (C), ModifyB (C),
              {∃xS .p}C{∃xS .q}
                                                                     and ModifyF (C).
where xS ∈ V arS and xS range over xV , xB , and xF .                   Since we treat predicates semantically in this paper,
  Auxiliary Variable Renaming:                                       we need to reformulate the Frame Rule to get a semantic
                                                                     version and we need to rewrite the condition in the syntactic
         {p}C{q}              xS ∈
                                 / FV(C) ∧ yS ∈/ (FV(C)∪
                                                                     version of the Frame Rule. Let ModifyS (C) = XS , then the
 {p[yS /xS ]}C{q[yS /xS ]}          FV(p) ∪ FV(q))
                                                                     condition in the syntactic version of the Frame Rule can be
                                                        (R6)
                                                                     written as:
where xS , yS ∈ V arS , xS range over xV ,xB and xF , and yS
range over yV , yB and yF .                                                                XS ∩ FV(r) = ∅
   Frame Rule:                                                             Now we analyze such condition, review the Sect.4,
         {p}C{q}                                                       the interpretation of an assertion r is given by
                             ModifyS (C) ∩ FV(r) = ∅             (R7) {(sV , sB , sF , hV , hB ) | (sV , sB , sF , hV , hB ) ∈ r}.
      {p ∗ r}C{q ∗ r}
                                                                           1) For variables whether location variables, block vari-
where ModifyS (C) range over ModifyV (C), ModifyB (C),                        ables, or file variables, the condition simply checks
and ModifyF (C).                                                              whether any variable in r is modified by the com-
                                                                              mand C .
5.4 More about Specification                                               2) For heap cells which are composed of the heap for
                                                                              variables and heap for blocks, the condition is more
Additional Axioms. For several of the axioms we have                          elaborate. Consider for the conclusion of the rule,
given, there are particular versions. For instance:                           with the definition of “∗”, which says that for every
   • The Block Address Appending form (BAAp)                                  state satisfying p ∗ r , the current heap can be split
{h#f = m ∧ α, f = f 0 ∧ βi} attach(f, bk ∗ )                                  into two subheaps so that p holds for the one and r
                         0        0         0                0                for the other. Then for the premise of the rule, the tight
{h#f = m + n ∧ α[f /f ], β[f · (bk1 [f /f ], ..., bkn [f /f ])/f ]}
                                                                              interpretation of the Hoare triple {p}C{q} says that
                                                                (A20)
                                                                              the command can only access the cells guaranteed
where f 0 is distinct from f .                                                to exist by p which is involved in Point1. So r is
                                                                              an invariant during the execution which is what the
   • An instance:
                                                                              condition says.
   {h#f1 = 3 ∧ #f2 = 2, f1 = f2 · bi} attach(f1 , f1 .3)
                                                                   (1)     Similar to the semantic of ∀x.r, we define:
   {h#(f2 · b) = 3 ∧ #f2 = 2, , f1 = f2 · b · b}
                                                                          ∀XV .r = {(sV , sB , sF , hV , hB ) | ∀sV 0 ∈ StoresV (XV ).
    In practice, such axiom is rarely used. The only time it is
necessary to use is when one must prove a specification with                            (sV [sV 0 ], sB , sF , hV , hB ) ∈ r};
the location expression #f . It can usually be avoided by                 ∀XB .r = {(sV , sB , sF , hV , hB ) | ∀sB 0 ∈ StoresB (XB ).
renaming #f in the program before proving it. The similar                               (sV , sB [sB 0 ], sF , hV , hB ) ∈ r};
situation will occur in the specifications that include #b,               ∀XF .r = {(sV , sB , sF , hV , hB ) | ∀sF 0 ∈ StoresF (XF ).
which will be discussed in the future.
Scalability Issues. For each of commands, we can give three                             (sV , sB , sF [sF 0 ], hV , hB ) ∈ r}.
kinds of inference: local, global, and backward-reasoning.                 where sS [sS 0 ] denotes the update of sS by sS 0 defined
SL has some work in this area [10], and some similar work by:
for BCSSs is done. For example, the following instance of
block content loop command is the most complex one,
                                                                                                     sS 0 (y)        if y ∈ dom(sS 0 ),
                                                                                             
which is shown in equation A21. Obviously, such backwards                          0
                                                                                             
version can be applied generally since it works for any                      sS [sS ](y) ,           sS (y)          if y ∈ dom(sS ),
                                                                                                     undefined       otherwise.
                                                                                             
postcondition (p).
   • The Block Content Lookup Backward form (BCLBw)                        Hence, we have that:
  {e = i ∧ ∃¯l, x .(h¯l # (ē|i  x ), bk 7→ ¯li ∗ (h¯l # (ē[x /x]|
                 0                   0                         0
                                                                              ModifyS (C) ∩ FV(r) = ∅ holds iff r = ∀XS .r.
  i  x0 ), bk[x0 /x] 7→ ¯li −∗ p[x0 /x]))} x := {bk.e} {p}
                                                                (A21)      The Semantic Version of the Frame Rule:
                                                                                            {p} − {q}
where x0 is not free in e and p.                                                                                   r = ∀XS .r
                                                                                        {p ∗ r} − {q ∗ r}
                                                                                                                                                       10
                                                                                                                                     0     0
   where XS range over XV , XB , and XF .                                         Now we have that (sV 0 , sB 0 , sF 0 , h1V , h1B ) |= q . By
                                                                                                                             2     2
Theorem 6.1 (Soundness of the Frame Rule). The Frame Rule                         Lemma 6.3 since (sV , sB , sF , hV , hB ) |= r and r =
   is sound for both partial and total correctness.                               ∀XS .r, we obtain that (sV 0 , sB 0 , sF 0 , h2V , h2B ) |= r.
                                                                                                                           0                   0
                                                                                  Hence, we find the heaps h1H , h2H with h1H #h2H and
Proof 6.1.                                                                                  0                                                0   0
                                                                                  hH = h1H ∗ h2H such that (sV 0 , sB 0 , sF 0 , h1V , h1B ) |= q
   The proof uses the local properties which are from [28],                               0    0      0    2     2
                                                                                  and (sV , sB , sF , hV , hB ) |= r.
   where some similar properties are shown.                                       Therefore, (sV 0 , sB 0 , sF 0 , hV 0 , hB 0 ) |= q ∗ r, Theorem 1 is
Lemma 6.1 (Safety and Termination Monotonicity).                                  proved.
   1 If hC, σi is safe, and hV #hV 0 , hB #hB 0 ,                                 (2) The case for total correctness can be handled simi-
       then hC, (sV , sB , sF , hV ∗ hV 0 , hB ∗ hB 0 )i is safe.                 larly, the only difference is to use the Termination Mono-
   2 If hC, σi must terminate, and hV #hV 0 , hB #hB 0 ,                          tonicity instead of the Safety Monotonicity.
       then hC, (sV , sB , sF , hV ∗ hV 0 , hB ∗ hB 0 )i
       must terminate.
Lemma 6.2 (Frame Property).                                                   7    A N I LLUSTRATING E XAMPLE
     Suppose hC, (sV , sB , sF , h0V , h0B )i is safe and                     In this section, we will demonstrate how to use the ax-
        hC, (sV , sB , sF , h0V ∗ h1V , h0B ∗ h1B )i ∗                        ioms and rules by a practical example from Disk Balancer
                                                            0     0
     (sV 0 , sB 0 , sF 0 , hV 0 , hB 0 ), then there are h0V , h0B ,          (cf.Sect.2), which proves the correctness of Transfer algo-
                                                                     0
     where hC, (sV , sB , sF , h0V , h0B )i ∗ (sV , sB , sF , h0V ,           rithm as follows. To make the action of the inference rules
         0                        0                   0
     h0B ) and hV 0 = h0V ∗ h1V , hB 0 = h0B ∗ h1B .                          clear, each assertion is given by the unabbreviated form.
Lemma 6.3 (Write Locality).
                                                                              Algorithm 1 Transfer
     If hC, σi ∗ (sV 0 , sB 0 , sF 0 , hV 0 , hB 0 ), and
     x∈ / ModifyS (C), then sS (x) = sS 0 (x).                                 1: b1 := allocate(1011, 1012);
                                                                               2: f := create(b1 );
   We deal with the soundness of the Frame Rule for BCSSs                      3: b2 := allocate();
   in the following:                                                           4: function M OVE( )
   (1) For partial correctness:                                                5:     i := 1;
   We will show {p∗r}C{q∗r} is true. By the interpretation                     6:     while i <= #b1 do
   of partial correctness, we have:                                            7:         x := {b1 .i};
         {p ∗ r}C{q ∗ r} is true iff for ∀(sV , sB , sF , hV , hB ).           8:         append(b2 , x);
         if σ |= p ∗ r then                                                    9:         i := i + 1;
         1.hC, σi is safe and                                                 10:     end while
         2. if hC, σi ∗ (sV 0 , sB 0 , sF 0 , hV 0 , hB 0 )                   11: end function
         then (sV 0 , sB 0 , sF 0 , hV 0 , hB 0 ) |= q ∗ r                    12: f.1 := b2 ;
   Pick a state σ , suppose σ |= p ∗ r, by the definition of “ ∗              13: delete b1 ;
   ”, we have:
   σ |= p ∗ r iff
                                                                               Here is the full proof.
           there exists h1H , h2H with h1H #h2H and hH = h1H ∗h2H
           such that sV , sB , sF , h1V , h1B |= p and                    1{hempV , empB i}                                                           (Given)
                              2     2
           sV , sB , sF , hV , hB |= r;                                        b 1   :=    allocate(1011,  1012);
           where hiH range over hiV and hiB and i = 1, 2.                 {∃l̄.hl̄ # (1011, 1012), b1 7→ l̄i}                                            (A10)
                                                                                   0                       0    0       0
   By the premise of the frame rule, we have {p}C{q} is 2{∃b1 .htrueV , b1 == b1 ∧ b1 # b1 i}                                                               (1)
                                                                                   0                       0    0       0
   true,                                                                  3{∃b1 .htrueV , b1 == b1 ∧ b1 # b1 i}
         {p}C{q} is true iff for ∀(sV , sB , sF , h1V , h1B ).                 f := create(b1 );
                                 1      1                                       0                                   0       0     0
         if (sV , sB , sF , hV , hB ) |= p then                           {∃b 1 .htrueV , f = (b1 ) ∧ b1 == b1 ∧ b1 # b1 i}                            (2, A7)
         1.hC, (sV , sB , sF , h1V , h1B )i is safe and                            0                                  0
                                                                          4{∃b1 .htrueV , f = (b1 ) ∧ b1 == b1 ∧ b1 # b1 i}
                                                                                                                              0     0


         2. if hC, (sV , sB , sF , h1V , h1B )i ∗ (sV 0 , sB 0 , sF 0 ,        b2 := allocate();
           1 0     1 0                0   0      0   1 0  1 0             {∃b
                                                                                0        0                                0             0   0     0
                                                                                  , b2 .htrueV , f = (b1 ) ∧ b1 == b1 ∧ b2 == b2 ∧ b1 # b1 ∗ b2 # nili}
                                                                                                                                                          0
         hV , hB ) then (sV , sB , sF , hV , hB ) |= q                        1
                                                                                                                                                      (3, A10)
   By Lemma 1.(1) since hC, (sV , sB , sF , h1V , h1B )i is safe,
   hC, (sV , sB , sF ,                                                         After the executing of while-loop, the content of b2
   hV , hB )i is safe, where hV = h1V ∗ h2V and hB = h1B ∗ h2B . should be its initial content followed by the content of b1 ,
   By Lemma 2, now we have that hC, (sV , sB , sF , h1V , h1B )i or formally:
   is      safe,       and         hC, (sV , sB , sF , h1V ∗ h2V , h1B ∗               0     0                   0              0     0   0
                                                                             {∃b1 , b2 .htrueV , b1 == b1 ∧ b2 == b2 ∧ b1 # b1 ∗ b2 # nili}
                                                                                                                                                0
     2
   hB )i          ∗
                       (sV , sB 0 , sF 0 , hV 0 , hB 0 ), then there exit
                            0
                                                                                      i := 1; while be do C ;
                                                                                                              0
       0      0                                                         ∗
   h1V , h1B such that hC, (sV , sB , sF , h1V , h1B )i                      {∃b     1
                                                                                       0     0                   0              0             0
                                                                                         , b2 .htrueV , b1 == b1 ∧ b2 == b2 ∧ trueB ∗ b2 # b1 i}
                                                                                                                                                    0
                            0       0
   (sV 0 , sB 0 , sF 0 , h1V , h1B ).
   We will show that (sV 0 , sB 0 , sF 0 , hV 0 , hB 0 ) |= q ∗ r:
   (sV 0 , sB 0 , sF 0 , hV 0 , hB 0 ) |= q ∗ r iff                            We are proving the correctness of the Move function step
                          0                   0                    0
     there exist h1H , h2H with h1H #h2H and hH = h1H ∗ h2H               by step. After the first command i := 1, a complicated
                                            0      0                      condition is obtained from the initial condition and some
     such that (sV 0 , sB 0 , sF 0 , h1V , h1B ) |= q and
          0      0      0   2
     (sV , sB , sF , h , h ) |= r; 2                                      unnecessary conditions is omitted in the loop.
                        V    B
                                                                                                                                                                              11

                                                                                      trueB ∗ b4 # b4 ∗ b5 # b3 i} in 16 is A itself. So we prove
          0       0
 5{∃b1 , b2 .h1 ≤ #b1 + 1 ∧ #nil = 0 ∧ trueV , b1 == (nil, nil) ~ b1 ∧
                                                                           0          that {A ∧ T (be)} C 0 {A}. By the rule of while-loops (R3),
              0                           0
 b2 == b2 ~ (nil, nil) ∧ b1 # b1 ∗ b2 # nili}
                                                  0   0
                                                                                (4)   {A} while be do C 0 {A ∧ ¬T (be)} is acquired.
 6{∃b3 , b4 , b5 .h1 ≤ #b1 + 1 ∧ #b3 = 0 ∧ #b4 = #b1 ∧ trueV , b1 ==
 b3 ~ b4 ∧ b2 == b5 ∧ trueB ∗ b4 # b4 ∗ b5 # b3 i}                              (5)   17A ∧ ¬T (be) = ∃b3 , b4 , b5 .hi = #b1 + 1 ∧ #b3 = i − 1 ∧ #b4 = #b1 −
 7{∃b3 , b4 , b5 .h1 ≤ #b1 + 1 ∧ #b3 = 0 ∧ #b4 = #b1 ∧ trueV , b1 ==                  i + 1 ∧ trueV , b1 == b3 ~ b4 ∧ b2 == b5 ∧ trueB ∗ b4 # b4 ∗ b5 # b3 i
 b3 ~ b4 ∧ b2 == b5 ∧ trueB ∗ b4 # b4 ∗ b5 # b3 i}                                    18{∃b3 , b4 , b5 .hi ≤ #b1 + 1 ∧ #b3 = i − 1 ∧ #b4 = #b1 − i + 1 ∧ trueV ,
     i := 1;                                                                          b1 == b3 ~ b4 ∧ b2 == b5 ∧ trueB ∗ b4 # b4 ∗ b5 # b3 i}
                                                                                                                   0
 {∃b3 , b4 , b5 .hi ≤ #b1 + 1 ∧ #b3 = i − 1 ∧ #b4 = #b1 − i + 1 ∧ trueV ,                      while be do C ;
 b1 == b3 ~ b4 ∧ b2 == b5 ∧ trueB ∗ b4 # b4 ∗ b5 # b3 i}                  (6, A2)     {∃b3 , b4 , b5 .hi = #b1 + 1 ∧ #b3 = i − 1 ∧ #b4 = #b1 − i + 1 ∧ trueV ,
                                                                                      b1 == b3 ~ b4 ∧ b2 == b5 ∧ trueB ∗ b4 # b4 ∗ b5 # b3 i}                    (8-16, R3)



  The next command is a while-loop. To use the rule of                                    From the while-loop, we know i = #b1 + 1 when it
while-loops (R3), we need to find the loop invariant first.                           finished. The following conclusions is obtained from 18 and
                                                                                      the correctness of the Move function is proven.
 Let A ≡ ∃b3 , b4 , b5 .hi ≤ #b1 + 1 ∧ #b3 = i − 1 ∧ #b4 = #b1 − i + 1∧
          trueV , b1 == b3 ~ b4 ∧ b2 == b5 ∧ trueB ∗ b4 # b4 ∗ b5 # b3 i,              19{∃b3 , b4 , b5 .hi = #b1 + 1 ∧ #b3 = #b1 ∧ #b4 = 0 ∧ trueV , b1 == b3
    be ≡ i ≤ #b1 ,                                                                         ~ b4 ∧ b2 == b5 ∧ trueB ∗ b4 # b4 ∗ b5 # b3 i}                                    (18)
      0                                                                                20{∃b3 , b5 .hi = #b1 + 1 ∧ #b3 = #b1 ∧ trueV , b1 == b3 ∧ b2 == b5 ∧
    C ≡ x := {b1 .i}; append(b2 , x); i := i + 1;
                                                                                       trueB ∗ b5 # b3 i}                                                                    (19)
                                                                                                       0       0           0               0              0          0
                                                                                       21{∃b1 , b2 .htrueV , b1 == b1 ∧ b2 == b2 ∧ trueB ∗ b2 # b1 i} (20)
    Here b4 means the block content copied, b5 means the
rest block content. We will prove A is the loop invariant in
the following, i.e. {A ∧ T (be)} C 0 {A}.
                                                                                         After the Move function, using the axioms A15 and A17,
                                                                                      the final result can be obtained.
 8A ∧ T (be) = {∃b3 , b4 , b5 .hi ≤ #b1 ∧ #b3 = i − 1 ∧ #b4 = #b1 − i + 1
 ∧ trueV , b1 == b3 ~ b4 ∧ b2 == b5 ∧ trueB ∗ b4 # b4 ∗ b5 # b3 i}                                 0       0                           0              0                  0
                                                                                      22{∃b1 , b2 .htrueV , f = (b1 ) ∧ b1 == b1 ∧ b2 == b2 ∧ trueB ∗ b2 #
 9{∃b3 , b5 , b6 , b7 , l, y.hi ≤ #b1 ∧ #b3 = i − 1 ∧ #b7 = #b1 − i + 1 − 1∧               0
                                                                                      b1 i}                                                                              (4, 21)
 trueV ∗ l 7→ y, b1 == b3 ~ b6 ~ b7 ∧ b2 == b5 ∧ trueB ∗ b6 7→ (l)∗
                                                                                                   0       0                           0              0                  0
                                                                                      23{∃b1 , b2 .htrueV , f = (b1 ) ∧ b1 == b1 ∧ b2 == b2 ∧ trueB ∗ b2 #
 b7 # b7 ∗ b5 # b3 i}                                                           (8)
                                                                                           0
 10{∃b3 , b5 , b6 , b7 , l, y.hi ≤ #b1 ∧ #b3 = i − 1 ∧ #b7 = #b1 − i + 1 − 1          b1 i}
 ∧ trueV ∗ l 7→ y, b1 == b3 ~ b6 ~ b7 ∧ b2 == b5 ∧ trueB ∗ b6 7→ (l)∗                          f.1 := b2 ;
                                                                                               0       0                           0              0                  0         0
 b7 # b7 ∗ b5 # b3 i}                                                                 {∃b1 , b2 .htrueV , f = (b2 ) ∧ b1 == b1 ∧ b2 == b2 ∧ trueB ∗ b2 # b1
     x := {b1 .i};                                                                    i}                                                                             (22, A15)
 {∃b3 , b5 , b6 , b7 , l, y.hi ≤ #b1 ∧ #b3 = i − 1 ∧ #b7 = #b1 − i + 1 − 1∧           24{∃l̄, l¯0 .hl̄ # (1011, 1012) ∗ l¯0 # (1011, 1012), f = (b2 ) ∧ b1 7→ l̄ ∗ b2 7→
 x = y ∧ trueV ∗ l 7→ y, b1 == b3 ~ b6 ~ b7 ∧ b2 == b5 ∧ trueB ∗ b6 7→                l¯0 i}                                                                        (1, 23)
 (l) ∗ b7 # b7 ∗ b5 # b3 i}                                              (9, A12)     25{∃l̄, l¯0 .hl̄ # (1011, 1012) ∗ l¯0 # (1011, 1012), f = (b2 ) ∧ b1 7→ l̄ ∗ b2 7→
 11{∃b3 , b5 , b6 , b7 , l, y.hi ≤ #b1 ∧ #b3 = i − 1 ∧ #b7 = #b1 − i + 1 − 1          l¯0 i}
 ∧ x = y ∧ trueV ∗ l 7→ y, b1 == b3 ~ b6 ~ b7 ∧ b2 == b5 ∧ trueB ∗ b6                       delete b1 ;
 7→ (l) ∗ b7 # b7 ∗ b5 # b3 i}                                                        {∃l̄, l¯0 .hl̄ # (1011, 1012) ∗ l¯0 # (1011, 1012), f = (b2 ) ∧ b2 7→ l¯0 i}
                                                                                                                                                                     (24, A17)
     append(b2 , x);
                              0
 {∃b3 , b5 , b6 , b7 , b8 , l, l , y.hi ≤ #b1 ∧ #b3 = i − 1 ∧ #b7 = #b1 − i + 1
                                                  0                                      With all 1-25 and the rule of composition (R1), the
 − 1 ∧ x = y ∧ trueV ∗ l 7→ y ∗ l 7→ y, b1 == b3 ~ b6 ~ b7 ∧ b2 == b5
                                                              0                       correctness of Transfer Algorithm is proven.
 ~ b8 ∧ trueB ∗ b6 7→ (l) ∗ b7 # b7 ∗ b5 # b3 ∗ b8 7→ (l )i}            (10, A11)
                          0
 12{∃b3 , b6 , b7 , b9 , l, l , y.hi ≤ #b1 ∧ #b3 = i − 1 ∧ #b7 = #b1 − i + 1
                                  0
 − 1 ∧ trueV ∗ l 7→ y ∗ l 7→ y, b1 == b3 ~ b6 ~ b7 ∧ b2 == b9 ∧ trueB                 8         C ONCLUSION
                                                          0
 ∗ b3 # b3 ∗ b6 7→ (l) ∗ b7 # b7 ∗ b9 7→ (l )i}                                (11)   To insure reliability of block operations in BCSSs and reduce
                      0
 13{∃b7 , b9 , b10 , l, l , y.hi ≤ #b1 ∧ #b10 = i − 1 + 1 ∧ #b7 = #b1 − i+            the complexity of the block-based storage structure and at
                                      0
 1 − 1 ∧ trueV ∗ l 7→ y ∗ l 7→ y, b1 == b10 ~ b7 ∧ b2 == b9 ∧ trueB ∗                 the same time refine the block content, a verification frame-
                                              0
 b10 7→ (l) ∗ b7 # b7 ∗ b9 7→ (l )i}                                           (12)   work based on SL is introduced to prove the correctness
 14{∃b7 , b9 , b10 .hi ≤ #b1 ∧ #b10 = i − 1 + 1 ∧ #b7 = #b1 − i + 1 − 1∧              of BCSSs management programs. The framework is con-
 trueV , b1 == b10 ~ b7 ∧ b2 == b9 ∧ trueB ∗ b7 # b7 ∗ b9 # b10 i} (13)               structed by introducing a novel two-tier heap structure, and
 15{∃b7 , b9 , b10 .hi ≤ #b1 ∧ #b10 = i − 1 + 1 ∧ #b7 = #b1 − i + 1 − 1               a defined modeling language. Moreover, assertions based on
 ∧ trueV , b1 == b10 ~ b7 ∧ b2 == b9 ∧ trueB ∗ b7 # b7 ∗ b9 # b10 i}                  SL is constructed to describe the properties of BCSSs. Then a
     i := i + 1;
                                                                                      proof system with Hoare-style specifications is proposed to
 {∃b7 , b9 , b10 .hi ≤ #b1 + 1 ∧ #b10 = i − 1 ∧ #b7 = #b1 − i + 1 ∧ trueV ,
                                                                                      reason about the BCSSs. Using these methods, an example of
 b1 == b10 ~ b7 ∧ b2 == b9 ∧ trueB ∗ b7 # b7 ∗ b9 # b10 i}               (14, A2)
                                                                                      practical algorithm with while-loop is verified. The results
 16{∃b3 , b4 , b5 .hi ≤ #b1 + 1 ∧ #b3 = i − 1 ∧ #b4 = #b1 − i + 1 ∧ trueV ,
                                                                                      show that the proving process is scientific and correct.
 b1 == b3 ~ b4 ∧ b2 == b5 ∧ trueB ∗ b4 # b4 ∗ b5 # b3 i}                       (15)
                                                                                          Future work will focus on the following directions: (1)
                                                                                      Consider more characteristics of BCSSs, such as parallelism,
  Notice that, {∃b3 , b4 , b5 .hi ≤ #b1 + 1 ∧ #b3 = i − 1 ∧                           (key,value) pairs and the relations between blocks and lo-
#b4 = #b1 − i + 1 ∧ trueV , b1 == b3 ~ b4 ∧ b2 == b5 ∧                                cations. (2) Investigate the expressiveness, decidability and
                                                                                                                                                    12

model checking algorithms of assertions. (3) Find out highly                 [18] Gian Ntzik and Philippa Gardner.: Reasoning about the posix file
efficient proof strategies by selecting adaptive bi-abduction                    system: Local update and global pathnames. In: ACM SIGPLAN
                                                                                 Notices, volume 50, pages 201–220. ACM, (2015).
rules to improve the usability of our proof system.                          [19] Peter O’Hearn, John Reynolds, and Hongseok Yang.: Local rea-
                                                                                 soning about programs that alter data structures. In: International
                                                                                 Workshop on Computer Science Logic, pages 1–19. Springer, (2001).
ACKNOWLEDGMENTS                                                              [20] Inna Pereverzeva, Linas Laibinis, Elena Troubitsyna, Markus
                                                                                 Holmberg, and Mikko Pöri.: Formal modelling of resilient data
This work is supported by the National Key R&D                                   storage in cloud. In: International Conference on Formal Engineering
Program of China under Grants 2017YFB1103602 and                                 Methods, pages 363–379. Springer, (2013).
2018YFB1003904, the National Natural Science Founda-                         [21] David Pym, Jonathan M Spring, and Peter O’Hearn.: Why separa-
tion of China under Grants 61572003, 61772035, 61751210,                         tion logic works. Philosophy & Technology, pages 1–34, (2018).
                                                                             [22] John C Reynolds.: Separation logic: A logic for shared mutable
61972005 and 61932001, and the Major State Research Devel-                       data structures. In: Proceedings 17th Annual IEEE Symposium on Logic
opment Program of China under Grant 2016QY04W0804.                               in Computer Science, pages 55–74. IEEE, (2002).
                                                                             [23] Konstantin Shvachko, Hairong Kuang, Sanjay Radia, and Robert
                                                                                 Chansler.: The hadoop distributed file system. In: 2010 IEEE 26th
R EFERENCES                                                                      symposium on mass storage systems and technologies, pages 1–10. IEEE,
                                                                                 (2010).
[1] Apache Software Foundation.: Rebalance data blocks when new              [24] Kasper Svendsen and Lars Birkedal.: Impredicative concurrent ab-
    data nodes added or data nodes become full - ASF JIRA, (2019).               stract predicates. In: European Symposium on Programming Languages
    https://issues.apache.org/jira/browse/HADOOP-1652                            and Systems, pages 149–168. Springer, (2014).
[2] Josh Berdine, Cristiano Calcagno, and Peter W O’hearn.: Symbolic         [25] Quang-Trung Ta, Ton Chanh Le, Siau-Cheng Khoo, and Wei-Ngan
    execution with separation logic. In: Asian Symposium on Program-             Chin.: Automated mutual explicit induction proof in separation
    ming Languages and Systems, pages 52–68. Springer, (2005).                   logic. In: International Symposium on Formal Methods, pages 659–676.
[3] Lars Birkedal, Noah Torp-Smith, and John C Reynolds.: Local                  Springer, (2016).
    reasoning about a copying garbage collector. In: ACM SIGPLAN             [26] Hanpin Wang, Zhao Jin, Lei Zhang, Yuxin Jing, and Yongzhi
    Notices, volume 39, pages 220–231. ACM, (2004).                              Cao.: Reasoning about cloud storage systems. In: 2018 IEEE Third
[4] James Brotherston, Nikos Gorogiannis, and Max Kanovich.: Biab-               International Conference on Data Science in Cyberspace, pages 107–114.
    duction (and related problems) in array separation logic. In: Inter-         IEEE, (2018).
    national Conference on Automated Deduction, pages 472–490. Springer,     [27] Glynn Winskel.: The formal semantics of programming languages: an
    (2017).                                                                      introduction. MIT press, (1993).
[5] James Brotherston, Nikos Gorogiannis, Max Kanovich, and Reuben           [28] Yang H.: Local Reasoning for Stateful Programs. PhD thesis, Univer-
    Rowe.: Model checking for symbolic-heap separation logic with                sity of Illinois at Urbana-Champaign, (2001).
    inductive predicates. ACM SIGPLAN Notices, 51(1):84–96, (2016).          [29] Hongseok Yang and Peter O’Hearn.: A semantic basis for local
[6] Mike Dodds, Xinyu Feng, Matthew Parkinson, and Viktor                        reasoning. In: International Conference on Foundations of Software
    Vafeiadis.: Deny-guarantee reasoning. In: European Symposium on              Science and Computation Structures, pages 402–416. Springer, (2002).
    Programming, pages 363–377. Springer, (2009).                            [30] Hoare, Charles Antony Richard.: An axiomatic basis for computer
[7] Victor R Basili and Douglas D Dunlop.: A comparative analysis                programming. Communications of the ACM, pages 576–580, (1969).
    of functional correctness. In: ACM Computing Surveys, volume 14,         [31] Dean, Jeffrey and Ghemawat, Sanjay.: MapReduce: simplified data
    pages 229–244. ACM, (1980).                                                  processing on large clusters. Communications of the ACM, pages 107–
[8] S. Ghemawat, H. Gobioff, and S. Leung.: The google file system.              113, (2008).
    In: Proceedings of the 19th ACM Symposium on Operating Systems           [32] CNN Business.: Amazon broke the internet with a typo [EB/OL],
    Principles, 29–43, (2003).                                                   (2017). https://money.cnn.com/2017/03/02/technology/amazon-
[9] Ibrahim Abaker Targio Hashem, Ibrar Yaqoob, Nor Badrul Anuar,                s3-outage-human-error/index.html
    Salimah Mokhtar, Abdullah Gani, and Samee Ullah Khan.: The               [33] Hesselink, Wim H and Lali, Muhammad Ikram.: Formalizing a
    rise of “big data” on cloud computing: Review and open research              hierarchical file system. Formal Aspects of Computing, pages 27–44,
    issues. Information Systems, 47:98–115, (2015).                              (2012).
[10] Samin S Ishtiaq and Peter W O’hearn.: Bi as an assertion language
    for mutable data structures. ACM SIGPLAN Notices, 36(3):14–26,
    (2001).
[11] Julian James Stephen, Savvas Savvides, Russell Seidel, and Patrick
    Eugster.: Program analysis for secure big data processing. In: Pro-
    ceedings of the 29th ACM/IEEE international conference on Automated
    software engineering, pages 277–288. ACM, (2014).
[12] Zhao Jin, Hanpin Wang, Lei Zhang, Bowen Zhang, Kun
    Gao, and Yongzhi Cao.:              Reasoning about Block-based
    Cloud Storage Systems.            arXiv:1904.04442 [cs.LO] (2019).
    https://arxiv.org/abs/1904.04442
[13] Yuxin Jing, Hanpin Wang, Yu Huang, Lei Zhang, Jiang Xu, and
    Yongzhi Cao.: A modeling language to describe massive data
    storage management in cyber-physical systems. Journal of Parallel
    and Distributed Computing, 103:113–120, (2017).
[14] Ralf Jung, David Swasey, Filip Sieczkowski, Kasper Svendsen,
    Aaron Turon, Lars Birkedal, and Derek Dreyer.: Iris: Monoids and
    invariants as an orthogonal basis for concurrent reasoning. In: ACM
    SIGPLAN Notices, volume 50, pages 637–650. ACM, (2015).
[15] Morten Krogh-Jespersen, Kasper Svendsen, and Lars Birkedal.:
    A relational model of types-and-effects in higher-order concurrent
    separation logic. In: ACM SIGPLAN Notices, volume 52, pages 218–
    231. ACM, (2017).
[16] Quang Loc Le, Makoto Tatsuta, Jun Sun, and Wei-Ngan Chin.: A
    decidable fragment in separation logic with inductive predicates
    and arithmetic. In: International Conference on Computer Aided Verifi-
    cation, pages 495–517. Springer, (2017).
[17] Wonyeol Lee and Sungwoo Park.: A proof system for separation
    logic with magic wand. In: ACM SIGPLAN Notices, volume 49,
    pages 477–490. ACM, (2014).
                                                                                                                                                                          13

A PPENDIX A                                                                             For
A S EMANTIC E XAMPLE
                                                                                      Ji <= #b1 K(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV [1/i], hB [(loc11 ,
We will use our modeling language to write a program that                             loc12 )/bloc1 ][nil/bloc2 ], [hV |loc11 : 1011, loc12 : 1012])
tries to create and copy a file. First, we create a file f1 with a                    = J1 <= 2K(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV [1/i], hB [(loc11 ,
sole block b1 , which value is (1011, 1012). Then we create a                         loc12 )/bloc1 ][nil/bloc2 ], [hV |loc11 : 1011, loc12 : 1012])
new empty block b2 , which later is appended with content                             = true
of file b1 one by one in the while-loop. Finally, we create
a new empty file f2 , and attach the block b2 to it. When
it is finished, we got a file f1 and its copy f2 . Note that                            Thus
we cannot change the order of command L2 and L2 since                               JL12 K(JL11 K(JWK(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV [1/i], hB
that the semantics of f := create(bk1 , ..., bkn ) request that                     [(loc11 , loc12 )/bloc1 ][nil/bloc2 ], [hV |loc11 : 1011, loc12 : 1012])))
the term of sequence determined by hB (Jbki Kσ) belong to                           = JL12 K(JL11 K(JWK(JL9 K(JL8 K(JL7 K(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ]
dom(hV ).                                                                           [bloc2 /b2 ], sV [1/i], hB [(loc11 , loc12 )/bloc1 ][nil/bloc2 ], [hV |loc11 : 1011,
                                                                                    loc12 : 1012]))))))
Algorithm 2 Copy a File                                                             = JL12 K(JL11 K(JWK(JL9 K(JL8 K(Jx := {b1 .i}K(sF [(bloc1 )/f1 ], sB [bloc1
 1: function C OPY( )                                                               /b1 ][bloc2 /b2 ], sV [1/i], hB [(loc11 , loc12 )/bloc1 ][nil/bloc2 ], [hV |loc11 :
 2:    b1 := allocate(1011, 1012);                                                  1011, loc12 : 1012]))))))
 3:    f1 := create(b1 );                                                           = JL12 K(JL11 K(JWK(JL9 K(JL8 K(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ],
 4:    b2 := allocate();                                                            sV [1/i][1011/x], hB [(loc11 , loc12 )/bloc1 ][nil/bloc2 ], [hV |loc11 : 1011,
 5:    i := 1;                                                                      loc12 : 1012])))))
                                                                                    = JL12 K(JL11 K(JWK(JL9 K(Jappend(b2 , x)K(sF [(bloc1 )/f1 ], sB [bloc1 /
 6:    while i <= #b1 do
                                                                                    b1 ][bloc2 /b2 ], sV [1/i][1011/x], hB [(loc11 , loc12 )/bloc1 ][nil/bloc2 ], [hV |
 7:        x := {b1 .i};
                                                                                    loc11 : 1011, loc12 : 1012])))))
 8:        append(b2 , x)
                                                                                    = JL12 K(JL11 K(JWK(JL9 K(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV
 9:        i := i + 1;
                                                                                    [1/i][1011/x], hB [(loc11 , loc12 )/bloc1 ][(loc21 )/bloc2 ], [hV |loc11 : 1011,
10:    end while                                                                    loc12 : 1012, loc21 : 1011]))))
11:    f2 := create();                                                              = JL12 K(JL11 K(JWK(Ji := i + 1K(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ],
12:    attach(f2 , b2 );                                                            sV [1/i][1011/x], hB [(loc11 , loc12 )/bloc1 ][(loc21 )/bloc2 ], [hV |loc11 : 1011,
13: end function                                                                    loc12 : 1012, loc21 : 1011]))))
                                                                                    = JL12 K(JL11 K(JWK(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV [2/i][1011
    We try to use the denotational semantics to analyze the                         /x], hB [(loc11 , loc12 )/bloc1 ][(loc21 )/bloc2 ], [hV |loc11 : 1011, loc12 : 1012,
sample program Algorithm 1. Assume the initial state is                             loc21 : 1011])))
(sF , sB , sV , hB , hV ), after the execution, we can get a final
state.
    For convenience, we use label Ln to express the com-
                                                                                       After the first loop of the while-loop command, block b2
mand in line n of the Algorithm 1, as an example, L3 is the
                                                                                    has copied the first content of b1 . And the index variable i
command b1 := allocate(1011, 1012);. Also, we use W to
                                                                                    equals 2. Therefore, the second loop will be started.
express the while loop part of the program. So there is:
                                                                                       For
JL2 ; L3 ; L4 ; L5 ; W; L11 ; L12 K(sF , sB , sV , hB , hV )                         Ji <= #b1 K(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV [2/i][1011/x], hB [
= JL12 K(JL11 K(JWK(JL5 K(JL4 K(JL3 K(JL2 K(sF , sB , sV , hB , hV )))))))          (loc11 , loc12 )/bloc1 ][(loc21 )/bloc2 ], [hV |loc11 : 1011, loc12 : 1012, loc21 :
= JL12 K(JL11 K(JWK(JL5 K(JL4 K(JL3 K(Jb1 := allocate(1011, 1012)K(sF ,             1011])
sB , sV , hB , hV )))))))                                                            = J2 <= 2K(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV [2/i][1011/x], hB [
= JL12 K(JL11 K(JWK(JL5 K(JL4 K(JL3 K(sF , sB [bloc1 /b1 ], sV , hB [(loc11 ,       (loc11 , loc12 )/bloc1 ][(loc21 )/bloc2 ], [hV |loc11 : 1011, loc12 : 1012, loc21 :
loc12 )/bloc1 ], [hV |loc11 : 1011, loc12 : 1012]))))))                             1011])
= JL12 K(JL11 K(JWK(JL5 K(JL4 K(Jf1 := create(b1 )K(sF , sB [bloc1 /b1 ], sV ,       = true
hB [(loc11 , loc12 )/bloc1 ], [hV |loc11 : 1011, loc12 : 1012]))))))
= JL12 K(JL11 K(JWK(JL5 K(JL4 K(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ], sV , hB
[(loc11 , loc12 )/bloc1 ], [hV |loc11 : 1011, loc12 : 1012])))))                        Thus
= JL12 K(JL11 K(JWK(JL5 K(Jb2 := allocate()K(sF [(bloc1 )/f1 ], sB [bloc1 /
b1 ], sV , hB [(loc11 , loc12 )/bloc1 ], [hV |loc11 : 1011, loc12 : 1012])))))      JL12 K(JL11 K(JWK(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV [2/i][1011
= JL12 K(JL11 K(JWK(JL5 K(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV ,      /x], hB [(loc11 , loc12 )/bloc1 ][(loc21 )/bloc2 ], [hV |loc11 : 1011, loc12 : 1012,
hB [(loc11 , loc12 )/bloc1 ][nil/bloc2 ], [hV |loc11 : 1011, loc12 : 1012]))))      loc21 : 1011])))
= JL12 K(JL11 K(JWK(Ji := 1K(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV ,   = JL12 K(JL11 K(JWK(JL9 K(JL8 K(JL7 K(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2
hB [(loc11 , loc12 )/bloc1 ][nil/bloc2 ], [hV |loc11 : 1011, loc12 : 1012]))))      /b2 ], sV [2/i][1011/x], hB [(loc11 , loc12 )/bloc1 ][(loc21 )/bloc2 ], [hV |loc11 :
= JL12 K(JL11 K(JWK(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV [1/i], hB    1011, loc12 : 1012, loc21 : 1011]))))))
[(loc11 , loc12 )/bloc1 ][nil/bloc2 ], [hV |loc11 : 1011, loc12 : 1012])))          = JL12 K(JL11 K(JWK(JL9 K(JL8 K(Jx := {b1 .i}K(sF [(bloc1 )/f1 ], sB [bloc1 /
                                                                                    b1 ][bloc2 /b2 ], sV [2/i][1011/x], hB [(loc11 , loc12 )/bloc1 ][(loc21 )/bloc2 ], [hV
                                                                                    |loc11 : 1011, loc12 : 1012, loc21 : 1011]))))))
                                                                                    = JL12 K(JL11 K(JWK(JL9 K(JL8 K(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ],
   Now we have got an intermediate state after executing                            sV [2/i][1012/x], hB [(loc11 , loc12 )/bloc1 ][(loc21 )/bloc2 ], [hV |loc11 : 1011,
commands L2, L3, L4 and L5. Next, we will analyze the                               loc12 : 1012, loc21 : 1011])))))
while-loop codes.
                                                                                                                                                                            14

= JL12 K(JL11 K(JWK(JL9 K(Jappend(b2 , x)K(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ]             A PPENDIX B
[bloc2 /b2 ], sV [2/i][1012/x], hB [(loc11 , loc12 )/bloc1 ][(loc21 )/bloc2 ], [hV |      S OUNDNESS OF THE S PECIFICATION A XIOMS
loc11 : 1011, loc12 : 1012, loc21 : 1011])))))
= JL12 K(JL11 K(JWK(JL9 K(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV [2/
                                                                                          The soundness of axioms can be proved in denotational
i][1012/x], hB [(loc11 , loc12 )/bloc1 ][(loc21 , loc22 )/bloc2 ], [hV |loc11 : 1011,
                                                                                          semantics by case:
loc12 : 1012, loc21 : 1011, loc22 : 1012]))))                                                Location Commands:
= JL12 K(JL11 K(JWK(Ji := i + 1K(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ],            • Skip
sV [2/i][1012/x], hB [(loc11 , loc12 )/bloc1 ][(loc21 , loc22 )/bloc2 ], [hV |loc11 :        JskipKσ = σ
1011, loc12 : 1012, loc21 : 1011, loc22 : 1012]))))
= JL12 K(JL11 K(JWK(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV [3/i][1012              σ |= p
                                                                                               σ |= p
/x], hB [(loc11 , loc12 )/bloc1 ][(loc21 , (loc22 )/bloc2 ], [hV |loc11 : 1011, loc12 :
1012, loc21 : 1011, loc22 : 1012])))

                                                                                            • The Simple Assignment form (SA)
                                                                                             Jx := eKσ = (sF , sB , sV [JeKσ/x], hB , hV )
   After the second loop, block b2 has copied the other
content of b1 .Now the index variable i equals 3, which will                                 let sV 0 ≡ sV [JeKσ/x]
terminate the while-loop command.                                                                              σ |= hx = x0 ∧ empV , empB i
                                                                                                          σ |= x = x0 ∧ empV and σ |= empB
   For                                                                                            JxKσ = Jx0 Kσ, dom(hV ) = {}, and dom(hB ) = {}
                                                                                                                        dom(hV ) = {}∧
                                                                                               sV 0 (x) = Je[x0 /x]K(sF , sB , sV 0 , hB ) and dom(hB ) = {}
 Ji <= #b1 K(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV [3/i][1012/x], hB                  sF , sB , sV 0 , hB , hV |= x = e[x0 /x] ∧ empV and
[(loc11 , loc12 )/bloc1 ][(loc21 , loc22 )/bloc2 ], [hV |loc11 : 1011, loc12 : 1012,                            sF , sB , sV 0 , hB , hV |= empB
loc21 : 1011, loc22 : 1012])                                                                    sF , sB , sV 0 , hB , hV |= hx = e[x0 /x] ∧ empV , empB i
 = J3 <= 2K(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV [3/i][1012/x], hB
[(loc11 , loc12 )/bloc1 ][(loc21 , loc22 )/bloc2 ], [hV |loc11 : 1011, loc12 : 1012,
                                                                                            • The Location Allocation form (LA)
loc21 : 1011, loc22 : 1012])
 = false                                                                                      Jx := cons(ē)Kσ = (sF , sB , sV [loc/x], hB , [hV |loc :
                                                                                          Je1 Kσ|...|loc + n − 1 : Jen Kσ])
                                                                                              where loc, ..., loc + n − 1 ∈ Loc − dom(hV )
    Thus                                                                                      let sV 0 ≡ sV [loc/x] and hV 0 ≡ hV |loc : Je1 Kσ|...|loc +
                                                                                          n − 1 : Jen Kσ , then:
                                                                                                                   σ |= hx = x0 ∧ empV , empB i
JL12 K(JL11 K(JWK(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV [3/i][1012/                              σ |= x = x0 ∧ empV and σ |= empB
x], hB [(loc11 , loc12 )/bloc1 ][(loc21 , loc22 )/bloc2 ], [hV |loc11 : 1011, loc12 :                 JxKσ = Jx0 Kσ, dom(hV ) = {}, and dom(hB ) = {}
1012, loc21 : 1011, loc22 : 1012])))                                                           JxKσ = Jx0 Kσ, dom(hV 0 ) = {loc, ..., loc + n − 1}, hV 0 (loc) =
                                                                                                Je1 Kσ ∧ ... ∧ hV 0 (loc + n − 1) = Jen Kσ, and dom(hB ) = {}
= JL12 K(JL11 K(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV [3/i][1012/x],                dom(hV 0 ) = {loc, ..., loc + n − 1}, hV 0 (loc) = Je1 [x0 /x]K
hB [(loc11 , loc12 )/bloc1 ][(loc21 , loc22 )/bloc2 ], [hV |loc11 : 1011, loc12 :                 (sF , sB , sV 0 , hB ) ∧ ... ∧ hV 0 (loc + n − 1) = Jen [x0 /x]K
1012, loc21 : 1011, loc22 : 1012]))                                                                (sF , sB , sV 0 , hB ) and sV 0 (x) = loc and dom(hB ) = {}
                                                                                                dom(hV 0 ) = {loc, ..., loc + n − 1} ∧ hV 0 (loc) = Je1 [x0 /x]K
= JL12 K(Jf2 := create()K(sF [(bloc1 )/f1 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV [3/                  (sF , sB , sV 0 , hB ) ∧ ... ∧ hV 0 (loc + n − 1) = Jen [x0 /x]K
i][1012/x], hB [(loc11 , loc12 )/bloc1 ][(loc21 , loc22 )/bloc2 ], [hV |loc11 : 1011,              (sF , sB , sV 0 , hB ) and sV 0 (x) = loc and dom(hB ) = {}
loc12 : 1012, loc21 : 1011, loc22 : 1012]))                                                       sF , sB , sV 0 , hB , hV 0 |= x 7→ e1 [x0 /x], ..., en [x0 /x] and
                                                                                                                  sF , sB , sV 0 , hB , hV 0 |= empB
= JL12 K(sF [(bloc1 )/f1 ][nil/f2 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV [3/i][1012/x],
                                                                                                sF , sB , sV 0 , hB , hV 0 |= hx 7→ e1 [x0 /x], ..., en [x0 /x], empB i
hB [(loc11 , loc12 )/bloc1 ][(loc21 , loc22 )/bloc2 ], [hV |loc11 : 1011, loc12 :
1012, loc21 : 1011, loc22 : 1012])
= Jattach(f2 , b2 )K(sF [(bloc1 )/f1 ][nil/f2 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV [3/        • The Location Lookup form (LL)
i][1012/x], hB [(loc11 , loc12 )/bloc1 ][(loc21 , loc22 )/bloc2 ], [hV |loc11 : 1011,
                                                                                             Jx := [e]Kσ = (sF , sB , sV [hV (JeKσ)/x], hB , hV )
loc12 : 1012, loc21 : 1011, loc22 : 1012])
= (sF [(bloc1 )/f1 ][(bloc2 )/f2 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV [3/i][1012/x],
                                                                                             let sV 0 ≡ sV [hV (JeKσ)/x], then:
hB [(loc11 , loc12 )/bloc1 ][(loc21 , loc22 )/bloc2 ], [hV |loc11 : 1011, loc12 :                                    σ |= hx = x0 ∧ e 7→ x00 , empB i
1012, loc21 : 1011, loc22 : 1012])                                                                              σ |= x = x0 ∧ e 7→ x00 and σ |= empB
                                                                                                   JxKσ = Jx0 Kσ, dom(hV ) = {JeKσ}, hV (JeKσ) = Jx00 Kσ, and
                                                                                                                                dom(hB ) = {}
                                                                                                             dom(hV ) = {Je[x0 /x]K(sF , sB , sV 0 , hB )},
                                                                                                  hV (Je[x0 /x]K(sF , sB , sV 0 , hB )) = Jx00 Kσ, and dom(hB ) = {}
    Hence                                                                                      JxK(sF , sB , sV 0 , hB , hV ) = hV (JeKσ) = Jx00 K(sF , sB , sV 0 , hB , hV ),
                                                                                                          dom(hV ) = {Je[x0 /x]K(sF , sB , sV 0 , hB , hV )},
                                                                                                hV (Je[x0 /x]K(sF , sB , sV 0 , hB , hV )) = Jx00 K(sF , sB , sV 0 , hB , hV ),
                                                                                                                              and dom(hB ) = {}
  JL2 ; L3 ; L4 ; L5 ; W; L11 ; L12 K(sF , sB , sV , hB , hV )
                                                                                                        sF , sB , sV 0 , hB , hV |= x = x00 ∧ e[x0 /x] 7→ x00 and
  = (sF [(bloc1 )/f1 ][(bloc2 )/f2 ], sB [bloc1 /b1 ][bloc2 /b2 ], sV [3/i][1012/x],                                  sF , sB , sV 0 , hB , hV |= empB
 hB [(loc11 , loc12 )/bloc1 ][(loc21 , loc22 )/bloc2 ], [hV |loc11 : 1011, loc12 :                      sF , sB , sV 0 , hB , hV |= hx = x00 ∧ e[x0 /x] 7→ x00 , βi
 1012, loc21 : 1011, loc22 : 1012])



                                                                                            • The Location Mutation form (LM)
    Finally, the program is terminated, and we got a final                                   J[e] := e0 Kσ = (sF , sB , sV , hB , hV [Je0 Kσ/JeKσ])
state.
                                                                                                                                                                       15
            0
   let hV ≡ hV [Je0 Kσ/JeKσ], then:
   The soundness of axioms can be proved in denotational                               Block Commands
semantics by case:
                                σ |= he 7→ −, empB i
                           σ |= e 7→ − and σ |= empB                                 • The Block Allocation form (BA)
                     dom(hV ) = {JeKσ} and dom(hB ) = {}
      dom(hV 0 ) = {JeKσ} and hV 0 (JeKσ) = Je0 Kσ and dom(hB ) = {}
     sF , sB , sV , hB , hV 0 |= e 7→ e0 and sF , sB , sV , hB , hV 0 |= empB
                                                                                      Jb := allocate(ē)Kσ = (sF , sB [bloc/b], sV , hB [(loc1 , ...,
                     sF , sB , sV , hB , hV 0 |= he 7→ e0 , empB i                 locn )/bloc], [hV |loc1 : Je1 Kσ, ..., locn : Jen Kσ])
                                                                                     where bloc ∈ BLoc−dom(hB ) , and loc1 , ..., locn ∈ Loc−
  • The Deallocation form (DL)                                                     dom(hV )
   Jdispose eKσ                =      (sF , sB , sV , hB , hV e(dom(hV ) −             let sB 0 ≡ sB [bloc/b], hB 0 = hB [(loc1 , ..., locn )/bloc]
{JeKσ}))                                                                           and hV 0 ≡ [hV |loc1 : Je1 Kσ, ..., locn : Jen Kσ], where
                                                                                   bloc ∈ BLoc−dom(hB ) , and loc1 , ..., locn ∈ Loc−dom(hV ),
   let hV 0 ≡ hV e(dom(hV ) − {JeKσ}, then:                                        as b is not free in e1 , ..., en , so we have:
                                σ |= he 7→ −, empB i
                                                                                                                     σ |= hempV , empB i
                           σ |= e 7→ − and σ |= empB
                                                                                                                σ |= empV and σ |= empB
                     dom(hV ) = {JeKσ} and dom(hB ) = {}
                                                                                                            dom(hV ) = {} and dom(hB ) = {}
           dom(hV 0 ) = {JeKσ} − {JeKσ} = {} and dom(hB ) = {}
                                                                                          dom(hV 0 ) = {loc1 , ..., locn } ∧ hV 0 (loc1 ) = Je1 K(sF , sB 0 , [sV
     sF , sB , sV , hB , hV 0 |= empV and sF , sB , sV , hB , hV 0 |= empB                     |l1 : loc1 , ..., ln : locn ], hB 0 ) ∧ ... ∧ hV 0 (loc1 ) = Jen K
                     sF , sB , sV , hB , hV 0 |= hempV , empB i                               (sF , sB 0 , [sV |l1 : loc1 , ..., ln : locn ], hB 0 ), dom(hB 0 ) =
                                                                                              {bloc}, hB 0 (bloc) = (loc1 , ..., locn ), and sB 0 (b) = bloc
                                                                                          dom(hV 0 ) = {loc1 , ..., locn } ∧ hV 0 (loc1 ) = Je1 K(sF , sB 0 , [sV
   File Commands                                                                          |l1 : m1 , ..., ln : mn ], hB 0 ) ∧ ... ∧ hV 0 (locn ) = Jen K(sF , sB 0 ,
                                                                                        [sV |l1 : m1 , ..., ln : mn ], hB 0 ), dom(hB 0 ) = {bloc}, hB 0 (bloc) =
  • The File Creation form (FC)                                                           (loc1 , ..., locn ), and sB 0 (b) = bloc, for some m1 , ..., mn ∈ Loc
   Jf := create(bk ∗ )Kσ = (sF [(Jbk1 Kσ, ..., Jbkn Kσ)/f ], sB ,                                       sF , sB 0 , sV , hB 0 , hV 0 |= ∃l̄.hl̄ 7→ ē, b 7→ l̄i
sV , hB , hV )
    where the term of sequence determined by
hB (Jbki Kσ) (1 ≤ i ≤ n) belong to dom(hV ).                                         • Alternative Axiom for Block Allocation (BAalt)
    let sF 0 ≡ sF [(Jbk1 Kσ, ..., Jbkn Kσ)/f ], as f does not ap-
pear in α or bk1 , ..., bkn , so we have:                                             Jb := allocate(ē)Kσ = (sF , sB [bloc/b], sV , hB [(loc1 , ...,
                                σ |= hα, f = nil ∧ βi
                         σ |= α, σ |= f = nil, and σ |= β                          locn )/bloc], [hV |loc1 : Je1 Kσ, ..., locn : Jen Kσ])
                       σ |= α, Jf Kσ = JnilKσ, and σ |= β
     sF 0 , sB , sV , hB , hV |= α, sF 0 (f ) = (Jbk1 K(sF 0 , sB , sV , hB ),       where bloc ∈ BLoc−dom(hB ) , and loc1 , ..., locn ∈ Loc−
                    ..., Jbkn K(sF 0 , sB , sV , hB )) and σ |= β                  dom(hV )
                          sF 0 , sB , sV , hB , hV |= α and
                  sF 0 , sB , sV , hB , hV |= β[(bk1 , ..., bkn )/f ]                   let sB 0 ≡ sB [bloc/b], sB 00 ≡ sB 0 [bloc/b0 ], hB 0 = hB [(loc1 ,
              sF 0 , sB , sV , hB , hV |= hα, β[(bk1 , ..., bkn )/f ]i             ..., locn )/bloc] and hV 0 ≡ [hV |loc1 : Je1 Kσ, ..., locn : Jen Kσ],
                                                                                   where bloc ∈ BLoc − dom(hB ) , and loc1 , ..., locn ∈ Loc −
  • The Block Address Appending form (BAA)
                                                                                   dom(hV ), as b is not free in e1 , ..., en , so we have:
                                                                                                                 σ |= hempV , empB i
   Jattach(f, bk ∗ )Kσ = (sF [(sF (f )  (Jbk1 Kσ, ..., Jbkn Kσ))                                           σ |= empV and σ |= empB
/f ], sB , sV , hB , hV )                                                                               dom(hV ) = {} and dom(hB ) = {}
    where the term of sequence determined by hB (Jbki Kσ)                                                sB 0 = bloc and dom(hB ) = {bloc}
                                                                                        sB 00 (b) = sB 0 [bloc/b0 ](b) = sB [bloc/b][bloc/b0 ](b) = bloc,
(1 ≤ i ≤ n) belong to dom(hV ).                                                         sB 00 (b0 ) = sB 0 [bloc/b0 ](b0 ) = bloc, and dom(hB ) = {bloc}
                                                                                             sF , sB 0 [bloc/b0 ], sV , hB 0 , hV 0 |= b == b0 ∧ b0 # b0
   let sF 0 ≡ sF [(sF (f )  (Jbk1 Kσ, ..., Jbkn Kσ))/f ], then:                                     sF , sB 0 [bloc/b0 ], sV , hB 0 , hV 0 |= trueV
                               σ |= hα, f = f 0 ∧ βi                                           sF , sB 0 [m/b0 ], sV , hB 0 , hV 0 |= b == b0 ∧ b0 # b0
                        σ |= α, σ |= f = f 0 , and σ |= β                                sF , sB 0 [m/b0 ], sV , hB 0 , hV 0 |= trueV for some m ∈ BLoc
                       σ |= α, Jf Kσ = Jf 0 Kσ, and σ |= β                              sF , sB 0 [m/b0 ], sV , hB 0 , hV 0 |= htrueV , b == b0 ∧ b0 # b0 i
                                                                                                                   for some m ∈ BLoc
              sF 0 , sB , sV , hB , hV |= α[f 0 /f ], σ |= β, and
             sF 0 (f ) = (f 0  (Jbk1 [f 0 /f ]K(sF 0 , sB , sV , hB ),                  sF , sB 0 , sV , hB 0 , hV 0 |= ∃b0 .htrueV , b == b0 ∧ b0 # b0 i
                      ..., Jbkn [f 0 /f ]K(sF 0 , sB , sV , hB )))
                     sF 0 , sB , sV , hB , hV |= α[f 0 /f ] and
     sF 0 , sB , sV , hB , hV |= β[f 0 · (bk1 [f 0 /f ], ..., bkn [f 0 /f ])/f ]
                  sF 0 , sB , sV , hB , hV |= hα[f 0 /f ], β[f 0 ·                   • The Block Content Append form (BCA)
                         (bk1 [f 0 /f ], ..., bkn [f 0 /f ])/f ]i

                                                                                      Jappend(bk, e)Kσ = (sF , sB , sV , hB [(loc1 , ..., locm ,
  • The File Deletion form (FD)                                                    locm+1 )/JbkKσ], [hV |locm+1 : JeKσ])
    Jdelete f K(sV , sB , sF , hB , hV ) = (sF [JnilKσ/f ], sB , sV ,                  where hB (JbkKσ) = (loc1 , ..., locm ), the term of sequence
hB , hV )                                                                          (loc1 , ..., locm ) belong to dom(hV ), and locm+1 ∈ Loc −
    let sF 0 ≡ sF [JnilKσ/f ], then:                                               dom(hV );
                        σ |= hα, f = f 0 ∧ βi
                σ |= α, σ |= f = f 0 , and σ |= β                                     let hB 0 ≡ hB [(loc1 , ..., locm , locm+1 )/JbkKσ] and hV 0 ≡
               σ |= α, Jf Kσ = Jf 0 Kσ, and σ |= β
     sF 0 , sB , sV , hB , hV |= α[f 0 /f ], sF 0 (f ) = (JnilK
                                                                                   [hV |locm+1 : JeKσ], where hB (JbkKσ) = (loc1 , ..., locm ) , and
                 (sF 0 , sB , sV , hB )), and σ |= β                               locm+1 ∈ Loc − dom(hV ), as bk is not free in e1 0 , ..., em 0 , e
             sF 0 , sB , sV , hB , hV |= α[f 0 /f ] and                            and #bk does not appear in bk . Note that we can get
                sF 0 , sB , sV , hB , hV |= β[nil/f ]
        sF 0 , sB , sV , hB , hV |= hα[f 0 /f ], β[nil/f ]i                        JbkK(sF , sB , sV , hB 0 ) from JbkKσ , so we have:
                                                                                                                                                                                 16
                                 σ |= ∃l¯0 .hl¯0 # e¯0 , bk 7→ l¯0 i
         sF , sB , [sV |l1 0 : n1 , ..., lm 0 : nm ], hB , hV |= l1 0 7→ e1 0 ∗ ...∗        • The Block Address Replacement of a File form (BARF)
         lm 7→ em and sF , sB , [sV |l1 0 : n1 , ..., lm 0 : nm ], hB , hV |=
              0         0
                                                                                              Jf.e := bkKσ = (sF [(bloc1 , ..., JbkKσ, ..., blocn )/f ], sB , sV ,
                     bk 7→ (l1 0 , ..., lm 0 ), for some n1 , ..., nm ∈ Loc
           dom(hV ) = {n1 , ..., nm }, hV (n1 ) = Je1 0 K(sF , sB , [sV |l1 0 :           hB , hV )
             n1 , ..., lm 0 : nm ], hB ), ..., hV (nm ) = Jem 0 K(sF , sB , [sV |             where sF (f ) = (bloc1 , ..., bloci , ..., blocn ),JeKσ = i and
           l1 0 : n1 , ..., lm 0 : nm ], hB ), dom(hB ) = {JbkK(sF , sB , [sV |
           l1 0 : n1 , ..., lm 0 : nm ], hB )}, hB (JbkK(sF , sB , [sV |l1 0 : n1 ,
                                                                                          1≤i≤n
         ..., lm 0 : nm ], hB )) = (n1 , ..., nm ), for some n1 , ..., nm ∈ Loc               Let sF 0 ≡ sF [(bloc1 , ..., JbkKσ, ..., blocn )/f ], then:
            dom(hV 0 ) = {n1 , ..., nm } ∪ {n}, hV (n1 ) = Je1 0 K(sF , sB ,                                σ |= h#f2 = e − 1 ∧ α, f = f2 · bk0 · f3 ∧ βi
           [sV |l1 0 : n1 , ..., lm 0 : nm , l : n], hB 0 ), ..., hV (nm ) = Jem 0 K                   σ |= #f2 = e − 1 ∧ α and σ |= f = f2 · bk0 · f3 ∧ β
          (sF , sB , [sV |l1 0 : n1 , ..., lm 0 : nm , l : n], hB 0 ), hV (nm+1 ) =             J#f2 Kσ = Je − 1Kσ, σ |= α, Jf Kσ = Jf2 · bk0 · f3 Kσ, and σ |= β
        JeK(sF , sB , [sV |l1 0 : n1 , ..., lm 0 : nm , l : n], hB 0 ), dom(hB 0 ) =                 Jf.eK(sF 0 , sB , sV , hB , hV ) = JbkK(sF 0 , sB , sV , hB , hV )
            {JbkK(sF , sB , [sV |l1 0 : n1 , ..., lm 0 : nm , l : n], hB 0 )}, and               J#f2 K(sF 0 , sB , sV , hB , hV ) = Je − 1K(sF 0 , sB , sV , hB , hV ),
           hB 0 (JbkK(sF , sB , [sV |l1 0 : n1 , ..., lm 0 : nm , l : n], hB 0 )) =                (sF 0 , sB , sV , hB , hV ) |= α and Jf K(sF 0 , sB , sV , hB , hV ) =
                      (n1 , ..., nm , n) for some n1 , ..., nm , n ∈ Loc                       Jf2 · bk · f3 K(sF 0 , sB , sV , hB , hV ) and (sF 0 , sB , sV , hB , hV ) |= β
            sF , sB , [sV |l1 0 : n1 , ..., lm 0 : nm , l : n], hB 0 , hV 0 |= l¯0 #                        sF , sB 0 , sV , hB , hV |= #f2 = e − 1 ∧ α and
       e¯0 ∗ l 7→ e and sF , sB , [sV |l1 0 : n1 , ..., lm 0 : nm , l : n], hB 0 , hV 0                      sF , sB 0 , sV , hB , hV |= f = f2 · bk · f3 ∧ β
                      |= bk 7→ l¯0 · (l) for some n1 , ..., nm , n ∈ Loc                                      sF , sB 0 , sV , hB , hV |= h#f2 = i − 1 ∧ α,
          sF , sB , sV , hB 0 , hV 0 |= ∃l¯0 , l.hl¯0 # e¯0 ∗ l 7→ e, bk 7→ l¯0 · (l)i                                f = f2 · b0 · f3 ∧ b == b0 ∧ βi



     • The Block Content Lookup form (BCL)                                                  • Block Deletion form (BD)
     Jx := {bk.e}Kσ = (sF , sB , sV [hV (loci )/x], hB , hV )                                 Jdelete bKσ = (sF , sB , sV , hB e(dom(hB )−{JbKσ}), hV )
     where hB (JbkKσ) = (loc1 , ..., locn ),JeKσ = i and 1 ≤ i ≤                              let hB 0 ≡ hB e(dom(hB ) − {JbKσ}), then:
n;                                                                                                                          σ |= ∃l̄.hl̄ # −, b 7→ l̄i
                00                                                                   0          dom(hV ) = {n1 , ..., nm } and hV (n1 ) = −, ..., hV (nm ) = − and
    let sV        ≡ [sV |l1 : n1 , ..., lm : nm ], sV           ≡                                         dom(hB ) = {JbKσ} and hB (JbKσ) = (n1 , ..., nm ),
sV 00 [hV (loci )/x], where hB (JbkKσ) = (loc1 , ..., locn ), and                                                         for some n1 , ..., nm ∈ Loc
                                                                                                dom(hV ) = {n1 , ..., nm } and hV (n1 ) = −, ..., hV (nm ) = − and
1 ≤ i ≤ n, then:        0                 00                                                      dom(hB 0 ) = {JbKσ} − {JbKσ} = {} for some n1 , ..., nm ∈ Loc
              σ |= ∃l̄.hx = x ∧ e = i ∧ l̄ # (ē|i  x ), bk 7→ l̄i
                                                                                               sF , sB , [sV |l1 : n1 , ..., lm : nm ], hB 0 , hV |= l1 7→ − ∗ ... ∗ lm 7→ −
        JxK(sF , sB , sV 00 , hB ) = Jx0 K(sF , sB , sV 00 , hB ), dom(hV ) =
                                                                                                     and sF , sB , [sV |l1 : n1 , ..., lm : nm ], hB 0 , hV |= empB ,
           {n1 , ..., nm }, hV (n1 ) = Je1 K(sF , sB , sV 00 , hB ), ..., hV
                                                                                                                          for some n1 , ..., nm ∈ Loc
            (nJeK(s ,s ,s 00 ,h ) ) = Jx00 K(sF , sB , sV 00 , hB ), ...,
                      F B V          B                                                                        sF , sB , sV , hB 0 , hV |= ∃l̄.hl̄ # −, empB i
            hV (nm ) = Jem K(sF , sB , sV 00 , hB ), dom(hB ) = {JbkK
           (sF , sB , sV 00 , hB )}, and hB (JbkK(sF , sB , sV 00 , hB )) =
                      (n1 , ..., nm ), for some n1 , ..., nm ∈ Loc
       dom(hV ) = {n1 , ..., nm }, hV (n1 ) = Je1 [x0 /x]K(sF , sB , sV 0 ,
        hB ), ..., hV (nJe[x0 /x]K(s ,s ,s 0 ,h ) ) = Jx00 K(sF , sB , sV 0 ,
                                       F B V       B
       hB ), ..., hV (nm ) = Jem [x0 /x]K(sF , sB , sV 0 , hB ), dom(hB ) =
         {Jbk[x /x]K(sF , sB , sV , hB )}, and hB (Jbk[x0 /x]K(sF , sB ,
                 0                     0

             sV 0 , hB )) = (n1 , ..., nm ), for some n1 , ..., nm ∈ Loc
        sF , sB , sV 0 , hB , hV |= x = x00 ∧ e[x0 /x] = i ∧ l̄ # (ē[x0 /x]
              |i  x00 ) and sF , sB , sV 0 , hB , hV |= bk[x0 /x] 7→ l̄,
                               for some n1 , ..., nm ∈ Loc
               sF , sB , sV 0 , hB , hV |= ∃l̄.hx = x00 ∧ e[x0 /x] = i∧
                       l̄ # (ē[x0 /x]|i  x00 ), bk[x0 /x] 7→ l̄i



     • The Block Address Assignment form (BAA)
     Jb := bkKσ = (sF , sB [JbkKσ/b], sV , hB , hV )
     Let sB 0 ≡ sB [JbkKσ/b], then:
                              σ |= hα, b == b0 ∧ βi
                         σ |= α and σ |= b == b0 ∧ β
                      σ |= α, JbKσ = Jb0 Kσ, and σ |= β
         sF , sB 0 , sV , hB , hV |= α[b0 /b] ∧ sB 0 (b) = Jbk[b0 /b]K
         (sF , sB 0 , sV , hB ) and sF , sB 0 , sV , hB , hV |= β[b0 /b]
                     sF , sB 0 , sV , hB , hV |= α[b0 /b] and
             sF , sB 0 , sV , hB , hV |= b == bk[b0 /b] ∧ β[b0 /b]
       sF , sB 0 , sV , hB , hV |= hα[b0 /b], b == bk[b0 /b] ∧ β[b0 /b]i



     • The Block Address Assignment form (BAAalt)
     Jb := f.iKσ = (sV , sB [Jf.iKσ/b], sF , hB , hV )
     Let sB 0 ≡ sB [Jf.iKσ/b], then:
                      σ |= h#f2 = i − 1 ∧ α, f = f2 · b0 · f3 ∧ βi
                 σ |= #f2 = i − 1 ∧ α and σ |= f = f2 · b0 · f3 ∧ β
         J#f2 Kσ = Ji − 1Kσ, σ |= α, Jf Kσ = Jf2 · b0 · f3 Kσ, and σ |= β
              JbK(sF , sB 0 , sV , hB , hV ) = Jb0 K(sF , sB 0 , sV , hB , hV )
         J#f2 K(sF , sB 0 , sV , hB , hV ) = Ji − 1K(sF , sB 0 , sV , hB , hV ),
             (sF , sB 0 , sV , hB , hV ) |= α, Jf K(sF , sB 0 , sV , hB , hV ) =
       Jf2 · b0 · f3 K(sF , sB 0 , sV , hB , hV ), and (sF , sB 0 , sV , hB , hV ) |= β
                     sF , sB 0 , sV , hB , hV |= #f2 = i − 1 ∧ α and
               sF , sB 0 , sV , hB , hV |= f = f2 · b0 · f3 ∧ b == b0 ∧ β
                       sF , sB 0 , sV , hB , hV |= h#f2 = i − 1 ∧ α,
                              f = f2 · b0 · f3 ∧ b == b0 ∧ βi
