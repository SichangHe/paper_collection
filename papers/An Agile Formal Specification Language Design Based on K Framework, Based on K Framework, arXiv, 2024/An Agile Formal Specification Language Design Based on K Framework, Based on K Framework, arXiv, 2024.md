                                             An Agile Formal Specification Language Design
                                                        Based on K Framework

                                                  Jianyu Zhang1 , Long Zhang2( B ) , Yixuan Wu3 , and Feng Yang2
                                         1
                                             School of Automation Engineering, University of Electronic Science and Technology
                                                                          of China, Chengdu, China
                                               2
                                                  National Key Laboratory of Science and Technology on Information System
arXiv:2404.18515v1 [cs.SE] 29 Apr 2024




                                                                        Security, AMS, Beijing, China
                                                                         zhanglong10@nudt.edu.cn
                                             3
                                                 School of Electronics and Information, Northwestern Polytechnical University,
                                                                                 Xi’an, China



                                                 Abstract. Formal Methods (FMs) are currently essential for verifying
                                                 the safety and reliability of software systems. However, the specification
                                                 writing in formal methods tends to be complex and challenging to learn,
                                                 requiring familiarity with various intricate formal specification languages
                                                 and verification technologies. In response to the increasing complexity of
                                                 software frameworks, existing specification writing methods fall short in
                                                 meeting agility requirements. To address this, this paper introduces an
                                                 Agile Formal Specification Language (ASL). The ASL is defined based
                                                 on the K Framework and YAML Ain’t Markup Language (YAML). The
                                                 design of ASL incorporates agile design principles, making the writing of
                                                 formal specifications simpler, more efficient, and scalable. Additionally,
                                                 a specification translation algorithm is developed, capable of converting
                                                 ASL into K formal specification language that can be executed for verifi-
                                                 cation. Experimental evaluations demonstrate that the proposed method
                                                 significantly reduces the code size needed for specification writing, en-
                                                 hancing agility in formal specification writing.

                                                 Keywords: Formal specification · Agile design concepts · K Framework


                                         1     Introduction

                                         As the code framework of modern software becomes more complex, its security
                                         and reliability are becoming a research concern. Existing methods such as strict
                                         software development processes and various testing methods have been adopted
                                         to ensure high reliability of software [26,36]. However, these traditional security
                                         assurance methods cannot meet the demand for simultaneous improvement of
                                         reliability and agility [23]. These methods are also difficult to completely prove
                                         the correctness of the system in theory [28].
                                             Formal methods diverge from traditional security assurance approaches. They
                                         employ rigorous mathematical techniques, including formal logic and mathe-
                                         matical reasoning, to verify the correctness of software systems against specified
properties and specifications. Formal methods are becoming an important means
of system security assurance and are widely used [24].
    Although formal methods can effectively prove the security of a target sys-
tem, writing formal specifications is intricate. This process demands developers
to possess not only system development expertise but also proficiency in math-
ematical logic. Furthermore, a thorough understanding of diverse formal speci-
fication languages and verification technologies is essential [16,14,15,21]. These
requirements, coupled with the frequent lack of integration with standard inte-
grated development environments [17], challenge the alignment of formal meth-
ods with the agility that is increasingly crucial in software development [37].
    Therefore, it is imperative to explore more agile solutions under the premise
of high reliability. This paper aims to develop a paradigm of formal specification
language that incorporates agile design principles [13], with the goal of reduc-
ing the complexity of specification writing in formal verification. Agile design
concepts and techniques within the field of software engineering emphasize sim-
plicity, efficiency, flexibility, and continuous feedback to enhance the quality and
adaptability of software development [34].
Challenges. From existing work, the conflict between formal methods and the
requirements of agility presents a core challenge for this paper, as illustrated by
the following points:

 – To support the description of complex properties and systems, formal meth-
   ods require a rigorous logical foundation and formal language [16]. This
   requirement can make their meanings and formal expressions obscure. As
   a result, it may lead to difficulties in writing and understanding formal
   specifications. In contrast, agility demands concise language and intuitive
   expression [1].
 – To facilitate formal verification, formal methods often necessitate working
   within a unified logical system. Each formal method typically has its unique
   specification language syntax, which is often incompatible with specifications
   from other methods. Agility, however, requires the use of familiar, efficient,
   and convenient methods and tools [37].

Overviews. To address the aforementioned challenges, the core idea of this
research is the proposal of a formal specification language. This language is
founded on the K Framework [32,30,8], utilizing a structured and parse-friendly
YAML [3] as a metalanguage. It is designed to integrate fine-grained specification
agility needs, aiming to be simple, efficient, and scalable[13]. Additionally, this
research develops a translation algorithm. This algorithm converts agile formal
specifications into K formal specifications. The overall technical framework is
illustrated in Figure. 1.
    K Framework is an executable semantics framework with language indepen-
dence, capable of automatically generating verification tools based on formal
language specifications. The K Framework is based on Matching Logic [31], a
variant of first-order logic. Matching Logic is used for describing and reasoning
about structures. It is known for its concise and intuitive expression capabilities.
                Fig. 1. Overall technical framework for this work.



These attributes are crucial for the K Framework’s ability to describe numerous
complex programming languages [7]. The powerful logical expression ability and
scalability of the K Framework make it chosen as the basis of ASL in this paper.
    YAML is a lightweight, easy-to-read, and write data serialization language,
widely used in configuration files and data interchange formats [3]. Despite its
less efficient performance in certain aspects compared to JavaScript Object No-
tation(JSON) [6], YAML has readability, ease of use, and support for multiple
tools. These features align well with the agile philosophy. Therefore, YAML was
selected as the metalanguage for ASL.
Contributions. The core contributions of this paper are as follows:

 – In response to the complexity and lack of agility in writing formal specifi-
   cation languages, an Agile Formal Specification Language is proposed. This
   language enables the completion of formal specification writing through con-
   cise and readable syntax.
 – To facilitate verification of agile formal specifications, a specification trans-
   lation algorithm has been developed. This algorithm transforms agile formal
   specifications into existing verifiable formal specifications.

    The structure of the remainder of this paper is as follows: Section 2 intro-
duces the technical background and motivation of this paper. Section 3 describes
the design of the proposed Agile Formal Specification Language, elucidating its
realization of agility principles. Section 4 delineates the specification translation
algorithm. Section 5 employs experimental validation to assess the method’s ef-
ficacy in enhancing specification agility. Concluding remarks and directions for
future research are provided in Section 6.
2   Background and Motivation
This paper primarily focuses on the intersection of two research domains: for-
mal verification methods and tools and agile software development approaches.
Consequently, this section reviews work within these realms to establish a com-
prehensive foundation for the study and introduces the motivation behind this
paper.
Formal Verification Methods and Tools. To ensure the security and reli-
ability of systems, academia and industry continuously explore more efficient
and convenient formal methods and tools. Rosu and Chen et al. [30,8] intro-
duced the K Framework based on Matching Logic [7,31], capable of generating
verifier tools from formal language definitions. It has been utilized to define
complete executable formal semantics for numerous real-world languages. Ste-
fuanescu et al. [35] instantiated the K Framework with the semantics of C, Java,
and JavaScript. The generated verifiers successfully checked the functional cor-
rectness of programs in these languages. Kroening et al. [22] proposed CBMC, a
bounded model checker for C programs. CBMC translates input C programs into
a formula and employs a Boolean Satisfiability Solver (SAT) [12] to determine
the presence of executions that violate specifications. It has seen widespread use
in C program verification. Heizmann and Dietsch et al. [11] developed Ultimate
Automizer, an automated program verification tool that employs trace abstrac-
tion algorithms and nested interpolators for computation in program analysis.
This tool has achieved notable success in the Software Verification Competition
(SV-COMP) [5]. Additionally, there are widely-used formal verification methods
and tools such as Z3 Theorem Prover [10], Isabelle Theorem Prover [29], Coq
Proof Assistant [4], and Simple Promela Interpreter (SPIN) [18].
    The aforementioned research has enhanced the efficiency of formal verifica-
tion and promoted its application. However, the issue of complex specification
writing remains. As modern software architectures become increasingly intricate,
they fail to meet the growing demand for agility. There is a need to develop a
formal specification language that possesses agile attributes.
Agile Software Development Approaches. Agile, as a software development
methodology, emphasizes adaptability to change and the continuous delivery of
high-value software [34]. Fowler et al. [13] introduced the Agile Manifesto. The
Agile Manifesto underscores the principle of simplicity by aiming to maximize the
reduction of unnecessary work as a core tenet of agile methods [9]. Subsequent
research on agile development methodologies has largely been guided by the
principles outlined in the Agile Manifesto [20]. Schwaber et al. [33] proposed the
Scrum Development Process (SCRUM). They treated the system development
process as a controlled black box, emphasizing flexibility and responsiveness
to changing requirements. Beck et al. [2] advocated for Extreme Programming
(XP). XP achieves continuous transformation in software development through
iterative cycles that include planning, analysis, and design activities.
    The research on agile development principles and methods has significantly
enhanced the efficiency and quality of software development, making it more
streamlined and convenient. However, in the realm of formal verification, there is
a lack of corresponding agile methodologies or tools. Developers are still required
to manually write extensive and complex formal specifications.
Motivation. To address the aforementioned issue, the goal of this paper is to
integrate agile development principles into the design of formal specification
languages, thereby addressing the complexity involved in writing formal speci-
fications. Consequently, we have established the following design objectives for
the specification language we propose to develop:
 – Specification understanding agility: The specification language should
   be simple and easy to read, possessing structured features, and adhere to the
   principle of Occam’s Razor [27] by retaining only the necessary core concepts
   required for formal specifications.
 – Specification writing agility: The specification language should support
   the reuse or extension of various definitions and specifications for functions
   and types, thereby avoiding redundant writing.
 – Specification extension agility: The specification language should be eas-
   ily scalable and modifiable in terms of syntax, allowing formal specifications
   to support the verification of different target languages.


3     Agile Formal Specification Language Design
This section details the syntax and language definition of the proposed Agile
Formal Specification Language, and explains its agility.

3.1   Specification Language Syntax Composition
The syntax of agile formal specifications is composed of three main parts: (1)
the YAML metalanguage, (2) the ASL keywords, and (3) the expression syntax.
    Firstly, YAML is used as the metalanguage. This means that the syntax of
the original YAML is adopted. Consequently, all valid agile formal specifications
are valid YAML files. This allows ASL to leverage the language features and
libraries of YAML.
    Secondly, the core concepts of the Agile Formal Specification Language are
types, functions, and specifications. Types are employed to define data types.
Functions are used to describe system functionalities. Specifications are asser-
tions about system behaviors. They restrict various system behaviors in a concise
and intuitive manner.
    Lastly, in the expression syntax, the expressions of agile formal specifications
follow the syntax of the K Framework [30]. For more details, please refer to the
official documentation of the K Framework (https://kframework.org/).

3.2   Specification Language Definition
This section delineates the definition of ASL. To visually depict the method of
writing specifications, this paper employs a combination of figures and text for
explanation.
    Figure 2 presents a schematic diagram of the composition of an ASL file.
The keyword within the rounded rectangle denotes a YAML node, with its value
corresponding to a specific entity type. The line signifies the relationship between
nodes, with the element at the arrow’s terminal being subordinate to the element
at its origin.
    As depicted in Figure 2, a complete specification file in the Agile Formal
Specification Language consists of the following five YAML nodes: spec, for,
imports, types, and funcs.




            Fig. 2. Composition rules of YAML nodes in an ASL file.


"spec". Node spec is a essential node used to represent the specification iden-
tifier for easy reference. The value of this node is equal to the all-capital form of
the specification file name.
"for". Node for is a essential node used to determine the verification target file,
which is the code file to be verified.
"imports". Node imports is an optional node used to specify the files that must
be incorporated. It enables the importation of either an ASL (.yaml) file or a K
Framework (.k) file to facilitate verification. These imported files are utilized as
components within the verification environment.
"types". Node types is optional and used to describe types. These types follow
the "sort as predicate" paradigm [19]. There are four sub-nodes under type.
One is essential: type/ctype. The other three are optional: is, functions, and
constructs. Here are the functions of these sub-nodes:

 – Sub-node type/ctype is used to declare the type. When the type is used to
   assist in verification, it is represented by the keyword type. When it directly
   involves the verification target, it is represented by ctype. In this article, C
   language is employed as the verification target, hence it is identified by the
   keyword ctype.
 – Sub-node is is used to declare a type constructor. The type constructor
   means: if t1 is t2, then t2 is the parent class of t1, and t1 can use the
   function of t2; t1 needs to satisfy the specification of t2.
 – Sub-node functions is used to declare function definitions and can contain
   multiple function definition expressions.
 – Sub-node constructs is used to declare specifications, and its value is an
   expression that can verify whether the value of the current type meets specific
   conditions.
"funcs". Node funcs is an optional node used to describe functions. It has
three sub-nodes. One is essential: func/cfunc. The other two are optional: is
and contracts. Here are the functions of these sub-nodes:
 – Sub-node func/cfunc is used to declare a function. The function is repre-
   sented by func when it is used to assist in verification; it is represented by
   cfunc when the function directly involves the verification target. Within this
   node, the input and output constraints of the function can be specified.
 – Sub-node is is used to declare a function constructor. The function construc-
   tor means: if f1 is f2, then f1 may represent an equivalent, refinement, or
   expansion of f2. Equivalence is a special case of refinement or expansion,
   where f1 and f2 are completely equal. Refinement entails making a function
   more specific, such that the refined function must meet all the requirements
   of the original function but may impose additional constraints on the domain
   or value range. Expansion, on the other hand, introduces additional inputs
   and outputs beyond the original ones, without affecting the original inputs
   and outputs. f1 should satisfy the specifications met by f2, thus enabling
   the reuse of specifications.
 – Sub-node contracts is used to declare the specification of the function and
   can verify whether the value of the current function meets specific conditions.
    In this context, we emphasize the key agile design aspects of ASL. Type-
related functions and their definitions are collocated, similar to the design in
object-oriented languages like Java. This arrangement facilitates a more intu-
itive reuse of functions alongside types. Moreover, specifications can be directly
added to types. This allows the reuse of type specifications while using the types,
enhancing the degree of specification reuse. Consequently, it eliminates the need
for redundant specification writing. The separation of definitions from other
specifications also enhances the agility of the specification-writing process.

3.3   Example
This subsection provides an application example of ASL to illustrate how the
aforementioned design is applied in practice.
     The code in Listing 1.1 is an agile formal specification in the example.yaml
file, which implements the verification of the insertion function for a specific type
of binary tree. It includes nodes such as spec, imports, for, types, and funcs.
                          Listing 1.1. An ASL example.
  1   spec : EXAMPLE
  2   imports :c - verifier . k
  3   for : bst . c
  4   types :
  5    - type : HTree
  6      is : BinaryTree < htree ( V :: Int , Height :: Int ) >
  7         functions :
  8           IntSet tree_keys ( HTree ) :
  9            - tree_keys ( node ( htree (V , Height ) ,T0 , T1 ) ) = { V } U (
        tree_keys ( T0 ) U tree_keys ( T1 ) )
 10            - tree_keys ( leaf ) = > . IntSet
 11   funcs :
 12    - cfunc : insert
 13      inputs : HTree ( T1 ) andBool min ( t (. Set , int ) ) < Int V : Int
       andBool V : Int <= Int max ( t (. Set , int ) )
 14    contracts : Htree (? T2 ) andBool tree_keys (? T2 ) == K { V } U
       tree_keys ( T1 )

Line 1. The spec node specifies that the specification is identified as EXAMPLE.
The specification identifier is equal to the uppercase version of the specification
file name, which is example.yaml.
Line 2. The imports node specifies the required imported file is c-verifier.k,
which is a C language verifier based on the K Framework. It defines some basic
syntax for C language verification.
Line 3. The for node specifies that the verification target file is bst.c, which
contains the C code implementation of the binary tree data structure and func-
tions.
Lines 4-6. The types node contains a type declaration variable Htree used to
assist in verification. In the is sub-node, a function constructor is declared as
follows: is:BinaryTree<htree(v::Int, height::Int)>. BinaryTree (binary
search tree) is the parent class, and HTree is a specific type of BinaryTree.
Each node in HTree contains two integer variables: V and Height. Through this
construction method, HTree can use the functions in BinaryTree and also needs
to satisfy the specifications of BinaryTree, achieving reuse of types, functions,
and specifications simultaneously.
Lines 7-10. The types node also defines a function named tree_keys which
outlines two rules: (1) The first rule specifies the method for extracting all keys
from an internal node of an HTree. node(htree(V,Height), T0, T1) represents
an internal node with three components: htree and two subtrees T0 and T1.
The tree_keys function is designed to extract the keys of all nodes in the
tree. The rule declares that to extract keys from an internal node, the value
V of the current node is first added to a set, followed by a recursive call to
the tree_keys function to extract the keys from the left and right subtrees T0
and T1, respectively, and then merge them into this set. (2) The second rule
defines the process for extracting keys from the leaf nodes of an HTree. The
rule implies that when extracting keys from a leaf node, the result is an empty
set. In essence, these two rules detail the approach for recursively traversing an
HTree and extracting keys from each node, ultimately aggregating these keys
into a set. The tree_keys function can serve as an auxiliary function during the
verification of the insertion function.
Lines 11-13. The funcs node contains a function declaration variable insert
that involves the verification target. It specifies that the verification target is
the insert function in the bst.c file. The input of this function is constrained
in the inputs node: Htree(T1) is used to check if T1 satisfies the properties
of a binary search tree. The constraint min(t(.Set,int)) <= Int V:Int and
Bool V:Int <= Int max(t(.Set,int)) requires that each value V in the tree
must be within the range of the minimum and maximum values of the tree.
Line 14. The contracts section defines the specification for verification func-
tion: Htree(?T2) andBool tree_keys(?T2) == K{V} U tree_keys(T1). This
specification states that if T2 is an Htree (? denotes an unmatched variable that
will be matched or deduced during verification), and all the keys in T2 are equal
to the set formed by all the keys in T1 plus an additional key V, then the spec-
ification is satisfied. This specification serves to validate whether the insert
function correctly implements its intended functionality. Since the tree_keys
function from the type Htree is invoked here, it also needs to adhere to the
specification of BinaryTree.


3.4   Specification Agility Statement

This subsection will elucidate the agile design philosophy integrated into the
design of the Agile Formal Specification Language.
    As illustrated in Figure 3, the fundamental requirements of agile design are
simplicity, efficiency, and flexibility [13]. To incorporate this philosophy into for-
mal specifications, ASL follows a design principle. This principle aims to simplify
specifications, enhance the efficiency of specification writing, and ensure the scal-
ability of the specifications.
Simplification of Specifications. ASL utilizes YAML as its metalanguage,
capitalizing on its ease of readability and structured nature. To further stream-
line the specification writing process, ASL retains only the essential core concepts
of formal specifications.
Enhancing Specification Writing Efficiency. ASL allows for the reuse of
types, functions, and specifications. Auxiliary functions necessary for verification
can be defined using the func or type nodes. These definitions can be based on
existing functions or types, facilitating reuse or extension and avoiding redundant
writing. Only specific specifications need to be incrementally added.
Scalability of Specifications. ASL supports different target languages. In this
paper’s introduction, the verification target is C language. It can also import K
Framework verifiers for different languages through the imports node to support
the verification of other languages [35]. This takes advantage of the K Frame-
work’s ease of extension.
                     Fig. 3. Agile design concepts in ASL.


4     Specification Translation Algorithm
This section presents the design of an algorithm for transforming agile formal
specifications into K formal specifications.

4.1   Overall Process
Figure 4 illustrates the entire process of ASL verification. It starts by loading
the ASL file, followed by loading the verification environment based on the spec-
ification target specified in the for node and the imported files listed in the
imports node. This process generates partial K formal specifications. Subse-
quently, the type and function translation modules generate corresponding K
formal specifications for types and functions, respectively. These specifications
are then combined to form a complete K formal specification. Finally, the for-
mal verification is executed using commands from the K Framework, and the
verification results are output. The type and function translation modules will
be introduced in the next subsection.

4.2   Translator Module
This subsection describes the functions of the translator module.
Type Translator Module. The role of the type translator is to convert the
values of the types node in ASL (represented by the variable ASL_type) into
the form of K formal specifications (represented by the variable k_type). The
detailed steps can be found in Algorithm 1.
Function Translator Module. The function translator is responsible for con-
verting the function nodes in ASL (represented by the variable ASL_func) into
the form of k formal specifications (represented by the variable k_func). The
implementation steps are similar to those of the type translator and will not be
repeated here.
Algorithm 1: Type translator module working steps
 Input: ASL_type
 Output: k_type
 Procedure initialization():
    Initialize k_type = empty string;
 Procedure handle_type_node():
    if type exists in ASL_type then
        parse ASL_type[type] and add the result to k_type;
    if ctype exists in ASL_type then
        parse ASL_type[ctype] and add the result to k_type;
    if Neither type nor ctype exists in ASL_type then
        Report an error and exit the program;

 Procedure handle_is_node():
    if is exists in ASL_type then
        if the value of ASL_type[is] is of list type then
            for each value(constructor) in ASL_type[is] do
                Parse each constructor to obtain the definition, functions and
                  specifications of the parent class;
                Add the parsing results to k_type by splicing strings;

        else if the value of ASL_type[is] is of string type then
            Perform lexical and syntactic analysis of the value (constructor)
             and obtain the definition, functions and specifications of the
             parent class;
            Add the parsing results to k_type;

 Procedure handle_functions_node():
    if functions exists in ASL_type then
        for each value(function rules) in ASL_type[functions] do
            Add function rules to k_type;

 Procedure handle_contracts_node():
    if contracts exists in ASL_type then
        if the value of ASL_type[contracts] is a list type then
            for each value(specification) in ASL_type[contracts] do
                Splice each specification with andBool and add it to k_type;

        else if the value of ASL_type[contracts] is of string type then
            Add value (specification) to k_type;

 Procedure main():
    initialization();
    handle_type_node();
    handle_is_node();
    handle_functions_node();
    handle_contracts_node();
    Add newline character to k_type;
    return k_type;
                    Fig. 4. Translation algorithm flow chart.


5     Evaluation
In this section, the Agile Formal Specification Language is used to perform spec-
ification writing and verification experiments on C code cases. Then it is com-
pared with existing formal specification methods to test the role of this method
in improving the agility of specification writing.

5.1   Comparison Method
In the experiments, this paper’s proposed Agile Formal Specification Language
and existing formal verification tools were used to write specifications and vali-
date C code cases, with a comparative analysis conducted.
    The K Framework [30] and CBMC[22] were selected as the comparison bench-
marks. The K Framework serves as the foundation for the Agile Formal Specifi-
cation Language, while CBMC is a widely-used tool for verifying C code.
    Due to the absence of quantitative metrics for agility in the field of formal
verification and the lack of a fixed method for writing formal specifications, this
paper employs the following comparative approach:

 – When compared with the K Framework, the complexity of the specification
   can be evaluated by comparing the number of code lines. This comparative
   method is effective because the expression syntax of ASL is identical to that
   of the K Framework. The selection of cases and the method for writing K
   formal specifications drew upon the work of Stefănescu et al. [35].
 – When compared with CBMC, since the syntax is different and there is no
   standard way to write specifications, the code lines cannot be used as a
   comparative metric. Therefore, this paper examines the differences in agility
   between two specification languages through the analysis of a case study.

    During the specification translation and verification process, Python 3.8 was
used to implement the specification translation algorithm, and the K Framework
4.0 was employed to run the verification.

5.2    Results and Analysis
Figure 5 illustrates a comparison of verification specifications for the Treap inser-
tion function [25], using K formal specification, CBMC specification, and ASL.
The K formal specification is produced by the specification translation algorithm.




      Fig. 5. Specification comparison for 3 kinds of specification languages.


    From Figure 5, it is evident that ASL can describe specifications more con-
cisely than K formal specifications, using only 16 lines. When compared to
CBMC specifications, although the number of lines is roughly the same, ASL’s
structure is clearer and more readable. This is because ASL uses YAML nodes
for structured representation, dividing the specification into parts. This struc-
ture makes it easier to modify and extend specifications. In contrast, CBMC
specifications require specific primitives like __CPROVER_assert for verification
at precise program locations. This process can be complex.
    Table 1 presents a comparison of code lines between ASL and K formal
specifications for other cases.
    As shown in Table 1, for the Treap’s insertion function, ASL achieves a 75%
reduction in code lines compared to K formal specifications. In the case of the
               Table 1. Line numbers comparison for Treap cases.
 Data Structure Function    Code Lines(ASL) Code Lines(K) Reduction Ratio(%)
 Treap          Insert Node 16              64            75.00%
 Treap          Find Node 9                 48            81.25%
 Treap          Delete Node 18              111           83.78%



search function, this reduction is 81.25%, and for the deletion function, it is
83.78%.
    To further validate the effectiveness of ASL, this paper also performed veri-
fication and comparison on additional cases, with the experimental results sum-
marized in Table 2.
               Table 2. Line numbers comparison for other cases.
Data Structure     Function       Code Lines(ASL) Code Lines(K) Reduction Ratio(%)
Linked List        Reverse List 69                294           76.53%
                   Append Node 64                 265           75.85%
                   Bubble Sort 96                 473           79.70%
                   Insertion Sort 101             501           79.84%
                   Merge Sort     103             483           78.67%
                   Quick Sort     107             548           80.47%
Binary Search Tree Insert Node 13                 126           89.68%
                   Search Node 29                 69            57.97%
                   Delete Node 118                308           61.69%
Red-Black Tree     Insert Node 38                 170           77.65%
                   Search Node 8                  47            82.98%
                   Delete Node 142                427           66.74%



    As shown in Table 2, ASL can significantly reduce the workload for specifi-
cation writing in verification cases of data structures. These structures include
linked lists, binary search trees, and red-black trees. On average, ASL achieves
a 76.07% reduction in code lines compared to K formal specifications.
    From the experiments conducted, it can be concluded that the ASL aligns
with the agility demands of formal specifications, boasting simplicity, efficiency,
and scalability. ASL can produce complex K formal specifications using the spec-
ification translation algorithm, which lessens the complexity and effort involved
in writing specifications. In contrast to CBMC, ASL offers a more structured
and clearer syntax for specification depiction.


6   Conclusion and Future Work

To resolve the complexities associated with writing specifications in the formal
verification process, this paper proposes an Agile Formal Specification Language
based on the K Framework. Firstly, the design of the ASL integrates agile de-
sign principles into the formal specification, improving the readability, efficiency,
and scalability of specification writing. Subsequently, a specification translation
algorithm is employed to convert ASL into K formal specifications to support ver-
ification. Experimental results demonstrate that the proposed method improves
the agility of specification writing compared to existing formal specification lan-
guages such as K Framework and CBMC.
    However, the current Agile Formal Specification Language has limitations.
Verification requires conversion to K formal specifications, which can limit case
selection and sometimes cause syntax errors. Our next goal is to research how
to enable ASL to directly and efficiently use solvers for verification, reducing
reliance on the K Framework. Additionally, we plan to apply ASL in more soft-
ware development projects and continue improving its reliability, completeness,
and portability.


References

 1. Al-Saqqa, S., Sawalha, S., AbdelNabi, H.: Agile software development: Methodolo-
    gies and trends. International Journal of Interactive Mobile Technologies 14(11)
    (2020). https://doi.org/10.3991/ijim.v14i11.13269
 2. Beck, K.: Embracing change with extreme programming. Computer 32(10), 70–77
    (1999). https://doi.org/10.1109/2.796139
 3. Ben-Kiki, O., Evans, C., Ingerson, B.: Yaml ain’t markup language (yaml™) version
    1.1. Working Draft 2008 5(11) (2009)
 4. Bertot, Y., Castéran, P.: Interactive theorem proving and program development:
    Coq’Art: the calculus of inductive constructions. Springer Science & Business Me-
    dia (2013). https://doi.org/10.1007/978-3-662-07964-5
 5. Beyer, D.: Competition on software verification and witness validation: Sv-comp
    2023. In: International Conference on Tools and Algorithms for the Construction
    and Analysis of Systems. pp. 495–522. Springer (2023). https://doi.org/10.1007/
    978-3-031-30820-8_29
 6. Bray, T.: The javascript object notation (json) data interchange format. Tech. rep.
    (2014)
 7. Chen, X., Lucanu, D., Roşu, G.: Matching logic explained. Journal of Logical and
    Algebraic Methods in Programming 120, 100638 (2021). https://doi.org/10.1016/
    j.jlamp.2021.100638
 8. Chen, X., Rosu, G.: Technical report: Applicative matching logic: Semantics of k
    (2020)
 9. Daraojimba, E.C., Nwasike, C.N., Adegbite, A.O., Ezeigweneme, C.A., Gidiagba,
    J.O.: Comprehensive review of agile methodologies in project management. Com-
    puter Science & IT Research Journal 5(1), 190–218 (2024). https://doi.org/10.
    51594/csitrj.v5i1.717
10. De Moura, L., Bjørner, N.: Z3: An efficient smt solver. In: International conference
    on Tools and Algorithms for the Construction and Analysis of Systems. pp. 337–
    340. Springer (2008). https://doi.org/10.1007/978-3-540-78800-3_24
11. Dietsch, D., Heizmann, M., Klumpp, D., Schüssele, F., Podelski, A.: Ultimate
    taipan and race detection in ultimate: (competition contribution). In: International
    Conference on Tools and Algorithms for the Construction and Analysis of Systems.
    pp. 582–587. Springer (2023). https://doi.org/10.1007/978-3-031-30820-8_40
12. Fichte, J.K., Berre, D.L., Hecher, M., Szeider, S.: The silent (r) evolution of
    sat. Communications of the ACM 66(6), 64–72 (2023). https://doi.org/10.1145/
    3560469
13. Fowler, M., Highsmith, J., et al.: The agile manifesto. Software development 9(8),
    28–35 (2001)
14. Garavel, H., Beek, M.H.t., Pol, J.v.d.: The 2020 expert survey on formal methods.
    In: Formal Methods for Industrial Critical Systems: 25th International Conference,
    FMICS 2020, Vienna, Austria, September 2–3, 2020, Proceedings 25. pp. 3–69.
    Springer (2020). https://doi.org/10.1007/978-3-030-58298-2_1
15. Gleirscher, M., Marmsoler, D.: Formal methods in dependable systems engineer-
    ing: a survey of professionals from europe and north america. Empirical Software
    Engineering 25, 4473–4546 (2020). https://doi.org/10.1007/s10664-020-09836-5
16. Gleirscher, M., van de Pol, J., Woodcock, J.: A manifesto for applicable formal
    methods. Software and Systems Modeling 22(6), 1737–1749 (2023). https://doi.
    org/10.1007/s10270-023-01124-2
17. Hähnle, R., Huisman, M.: Deductive software verification: from pen-and-paper
    proofs to industrial tools. Computing and Software Science: State of the Art and
    Perspectives pp. 345–373 (2019). https://doi.org/10.1007/978-3-319-91908-9_18
18. Holzmann, G.J.: The SPIN model checker: Primer and reference manual, vol. 1003.
    Addison-Wesley Reading (2004)
19. Kaneiwa, K.: The completeness of logic programming with sort predicates. Systems
    and Computers in Japan 35(1), 37–46 (2004). https://doi.org/10.1002/scj.10409
20. Kaushik, A.: Dsdm and asd agile methodologies. Int. Adv. Res. J. Sci. Eng. Technol.
    3(9), 2393–2394 (2016)
21. Krichen, M.: Improving formal verification and testing techniques for internet of
    things and smart cities. Mobile networks and applications 28(2), 732–743 (2023).
    https://doi.org/10.1007/s11036-019-01369-6
22. Kroening, D., Tautschnig, M.: Cbmc–c bounded model checker: (competition con-
    tribution). In: Tools and Algorithms for the Construction and Analysis of Sys-
    tems: 20th International Conference, TACAS 2014, Held as Part of the Eu-
    ropean Joint Conferences on Theory and Practice of Software, ETAPS 2014,
    Grenoble, France, April 5-13, 2014. Proceedings 20. pp. 389–391. Springer (2014).
    https://doi.org/10.1007/978-3-642-54862-8_26
23. Kuhrmann, M., Tell, P., Hebig, R., Klünder, J., Münch, J., Linssen, O., Pfahl, D.,
    Felderer, M., Prause, C.R., MacDonell, S.G., et al.: What makes agile software
    development agile? IEEE transactions on software engineering 48(9), 3523–3539
    (2021). https://doi.org/10.1109/TSE.2021.3099532
24. Kulik, T., Dongol, B., Larsen, P.G., Macedo, H.D., Schneider, S., Tran-Jørgensen,
    P.W., Woodcock, J.: A survey of practical formal methods for security. Formal
    aspects of computing 34(1), 1–39 (2022). https://doi.org/10.1145/3522582
25. Lammich, P., Nipkow, T.: Priority search trees. Archive of Formal Proofs (2019)
26. Mayeda, M., Andrews, A.: Evaluating software testing techniques: A systematic
    mapping study. Advances in Computers 123, 41–114 (2021). https://doi.org/10.
    1016/bs.adcom.2021.01.002
27. McFadden, J.: Razor sharp: The role of occam’s razor in science. Annals of the
    New York Academy of Sciences 1530(1), 8–17 (2023). https://doi.org/10.1111/
    nyas.15086
28. Mukherjee, S., Roy, S., Bose, R.: Defining an appropriate trade-off to overcome the
    challenges and limitations in software security testing. Journal of Xidian University
    14 (2020). https://doi.org/10.37896/jxu14.7/166
29. Paulson, L.C.: Isabelle: A generic theorem prover. Springer (1994). https://doi.
    org/10.1007/BFb0030558
30. Rosu, G.: K: A semantic framework for programming languages and formal analysis
    tools. Dependable Software Systems Engineering 50, 186–206 (2017). https://doi.
    org/10.3233/978-1-61499-810-5-186
31. Roşu, G., Chen, X.: Matching logic: the foundation of the k framework (invited
    talk). In: Proceedings of the 9th ACM SIGPLAN International Conference on
    Certified Programs and Proofs. pp. 1–1 (2020). https://doi.org/10.1145/3372885.
    3378574
32. Ros, u, G., S, erbănută, T.F.: An overview of the k semantic framework. The Journal
    of Logic and Algebraic Programming 79(6), 397–434 (2010). https://doi.org/10.
    1016/j.jlap.2010.03.012
33. Schwaber, K.: Scrum development process. In: Business Object Design and Imple-
    mentation: OOPSLA’95 Workshop Proceedings 16 October 1995, Austin, Texas.
    pp. 117–134. Springer (1997). https://doi.org/10.1007/978-1-4471-0947-1_11
34. Spagnoletti, P., Kazemargi, N., Prencipe, A.: Agile practices and organizational
    agility in software ecosystems. IEEE Transactions on Engineering Management
    69(6), 3604–3617 (2021). https://doi.org/10.1109/TEM.2021.3110105
35. Stefănescu, A., Park, D., Yuwen, S., Li, Y., Roşu, G.: Semantics-based program
    verifiers for all languages. ACM SIGPLAN Notices 51(10), 74–91 (2016). https:
    //doi.org/10.1145/3022671.2984027
36. Tauqeer, O.B., Jan, S., Khadidos, A.O., Khadidos, A.O., Khan, F.Q., Khattak, S.:
    Analysis of security testing techniques. Intelligent Automation & Soft Computing
    29(1), 291–306 (2021). https://doi.org/10.32604/iasc.2021.017260
37. Tsilionis, K., Ishchenko, V., Wautelet, Y., Simonofski, A.: Scaling agility in large
    software development projects: A systematic literature review. In: The Inter-
    national Research & Innovation Forum. pp. 771–784. Springer (2024). https:
    //doi.org/10.1007/978-3-031-44721-1_59
