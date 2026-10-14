                                        Syntax-driven Incremental Program Verification of Matching
                                        Logic Properties

                                        DOMENICO BIANCULLI, University of Luxembourg
                                        ANTONIO FILIERI, Imperial College London
                                        CARLO GHEZZI, DINO MANDRIOLI, and ALESSANDRO MARIA RIZZI, Politecnico di
                                        Milano
                                        Incrementality is a fundamental design principle to master the complexity of large, long-lived software systems.
arXiv:2606.08824v1 [cs.SE] 7 Jun 2026




                                        This principle has been embraced by agile development processes and it lays at the base of continuous software
                                        evolution. A major challenge in this context is to incrementally re-verify the correctness of software artifacts
                                        after every change, focusing the verification efforts only on the parts affected by the change.
                                            We present an approach to the incremental verification of programs written in KernelC, annotated with
                                        properties expressed in matching logic. The approach is based on a syntactic-semantic framework that enables
                                        analyzing code chunks in isolation so that, after a change to a program fragment, only the part whose semantics
                                        is affected by the change is re-processed. This property is obtained by expressing the language syntax through
                                        an operator precedence grammar and by formalizing its semantics through a synthesized attribute schema.
                                            We have implemented our technique in a prototype tool and experimentally evaluated its effectiveness.
                                        The results show that our approach does not penalize the efficiency of formal verification and can outperform
                                        program re-verification after changes, depending on the presence and type of annotations, as well as the
                                        position of the change and the program structure.
                                        CCS Concepts: • Software and its engineering → Formal software verification;
                                        Additional Key Words and Phrases: incremental verification, matching logic
                                        ACM Reference Format:
                                        Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro Maria Rizzi. 2026. Syntax-
                                        driven Incremental Program Verification of Matching Logic Properties. 1, 1 (June 2026), 60 pages. https:
                                        //doi.org/10.1145/nnnnnnn.nnnnnnn

                                        1   INTRODUCTION
                                        Incrementality is a fundamental engineering principle that manifests itself in many situations and
                                        in different forms. To dominate complexity, real-world problems are seldom solved monolithically,
                                        but rather through increments. Additionally, design is often exploratory in nature: different design
                                        decisions are explored (and detracted) before choosing the most desirable ones. Whenever a change
                                        is made in a design decision it is useful for the designer to just focus on the effect of the change.
                                           We are especially interested in understanding how the effect of changes may be analyzed
                                        incrementally through formal verification. The best way to achieve incrementality is through
                                        careful design that tries to anticipate likely changes, encapsulating their possible effects within
                                        modules, accessible through well-defined interfaces [47], specified by following the principle of
                                        design by contract [44].
                                           Changes, however, cannot always be anticipated; moreover, their effect can be cross-cutting.
                                        It is therefore important to complement incrementality “by design” with an approach that, for
                                        any given change, automatically and dynamically discovers the minimal extent of new analysis
                                        required and re-uses as much as possible from previous analysis.
                                        Authors’ addresses: Domenico Bianculli, University of Luxembourg; Antonio Filieri, Imperial College London; Carlo Ghezzi;
                                        Dino Mandrioli; Alessandro Maria Rizzi, Politecnico di Milano.

                                        2026. XXXX-XXXX/2026/6-ART $15.00
                                        https://doi.org/10.1145/nnnnnnn.nnnnnnn


                                                                                                              , Vol. 1, No. 1, Article . Publication date: June 2026.
:2     Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

   To further motivate the need for incremental formal verification, we mention two possible
important applications, which concern agile development and verification at run time. Agile
development [2] is a widely practiced software development approach that implements and delivers
software through increments, which may progressively add new functionalities and/or adjust
existing ones through direct control of the stakeholders [37]. Development proceeds through
continuous iterations. As for verification, the current state-of-the-art is based on continuous
testing [45, 53]. The adoption of formal verification into agile development to complement testing
requires a serious effort to make verification incremental. Incrementality may not only make the
verification faster, but also can help the designer to reason on the effects of changes. Another area
where incrementality is of paramount importance is on-the-fly verification or, more appropriately,
verification during system operation: in many cases software maintenance must occur without
interrupting — or minimizing the suspension of — system operations. In this case verification of the
updated version must also satisfy strong real-time requirements, which may be solved by exploiting
incrementality.
   Furthermore, in some sense incremental formal verification is the formal counterpart of regres-
sion testing in the same way as formal correctness proof is the traditional alternative or complement
to testing as the main verification technique. Incremental formal verification, in fact, while con-
centrating on the system fragment affected by the change, it also implicitly guarantees that the
remaining part of the system still behaves as in the previous version.
   In this paper, we use the term program verification in a broad sense that needs to be clarified
upfront. The term is often used to denote a proof that a program satisfies a specification. In our
work the specification is expressed in terms of logic statements, embedded in the program as
annotations written according to a suitable syntax. Following Hoare’s approach, annotations are
used to specify the initial state of the program (the precondition) and the expected end state (the
postcondition). Verification is successful if we can prove that whenever the program execution
starts in a state satisfying the precondition and execution ends, the desired postcondition holds.
The task of verification can be mechanized and modularized by further annotating the program
with intermediate assertions that summarize the intended behavior of certain program portions.
Loop invariants summarize the intended behavior of loops. Once the invariant is proved to hold
for a loop, it can be used in the verification of enclosing program segments as a summary of
the effect of the loop. Likewise, if pre and postconditions are provided for a function, once the
function is proved to be correct with respect to them, they can be used as function summary in the
verification of a program unit that invokes the function. Program verification à la Hoare assumes a
program to be fully annotated with pre and postconditions and invariants; the verification task is
performed by simple propagation of the program’s symbolic state along linear (non branching)
statement sequences. Our approach, however, does not require programs to be fully annotated. If
no annotations at all are provided, then verification amounts to propagating the symbolic state
and checking that no violating states are entered: it corresponds to symbolic execution. If the
program is partially annotated, assertions are used to check that the symbolic state satisfies the
corresponding assertion. Missing annotations in general penalize verification efficiency and may
even cause non termination. For example, missing invariants cause loop unfolding. In summary, the
term verification is used to cover a whole spectrum of activities ranging from Hoare-style program
verification to what we may call debugging-style verification.
   The specific context we explore in this paper is incremental verification at the program level
— although the problem can also be studied at the model level) [56] — using a logical framework
for defining the properties to check. More specifically, we focus on the incremental verification of
programs written in KernelC [16] (a subset of the C programming language) and annotated with
properties expressed in matching logic [51]. Our choice is motivated by the following reasons:

, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                    :3

   • KernelC is a large and meaningful subset of C, so that it can support writing and analyzing
     non-trivial, realistic, and large programs;
   • KernelC’s semantics is fully formalized in terms of matching logic which is a prerequisite for
     formal verification;
   • Matching logic is a nice and effective formalism that integrates verification through Hoare’s
     style annotations and through symbolic execution;
   • KernelC program verification is supported by a publicly available tool, namely MatchC [16],
     and the accompanying benchmark, useful for various types of experimental evaluations and
     comparisons.
   The present work on incremental program verification is based on our previous proposal for
a general-purpose, syntactic-semantic approach to incremental verification of various types of
system properties such as reliability, efficiency, etc., called SiDECAR (Syntax-DrivEn inCrementAl
veRification) [5]. The SiDECAR approach is rooted into the past work of some of the authors
on incremental syntactic program analysis [26], which is extended to formal verification using
attribute grammars [34] and incremental attribute evaluation [3, 32].
   SiDECAR defines the verification procedure through semantic attributes, which are computed
and propagated through the syntax tree of a program. SiDECAR leverages operator precedence
grammars [24] which, upon a change in a program, allow for re-parsing, and hence semantic
re-analysis, to be confined within an inner portion of the input that encloses the changed part [1].
This property is the key for an efficient incremental verification procedure: since the verification
procedure is encoded within attributes, their evaluation proceeds incrementally, hand-in-hand with
parsing of the new version of the program. In our earlier work, we applied SiDECAR to reachability
analysis in simple toy programs [3] and to reliability analysis of structured workflows [4]. In this
paper we show how SiDECAR can be used to build an incremental verifier for realistic KernelC
programs specified in matching logic, by completing and extending our preliminary work [6] where
the first steps to encode KernelC’s semantics in our attribute schema evaluation are reported, and
by making it incremental.
   We performed an extensive experimental assessment to show that:
   • Our syntactic-semantic approach based on attribute grammars does not penalize the efficiency
     of formal verification when (re)done from scratch. We do this assessment by comparing
     the efficiency of verification with SiDECAR with the efficiency of the state-of-the-art, non-
     incremental tool MatchC [16].
   • The incremental approach supported by SiDECAR outperforms program re-verification after
     changes if the program is fully annotated; instead, benefits range from just significant to
     striking if annotations are missing. In this latter case, the efficiency gains vary according to
     several conditions. Since verification through symbolic evaluation is intrinsically based on a
     sequential scan of the program, the gain may depend on the position in the program where
     the change is made, as well as on the program structure.
   To summarize, the contributions of this paper are: 1) the definition of an incremental verification
procedure for KernelC programs annotated with matching logic properties, built on top of SiDECAR,
our general syntactic-semantic framework for incremental verification; 2) an extensive experimental
evaluation of the benefits and costs introduced by our incremental verification procedure, using a
large benchmark including non-toy, industrial-size programs.

 Reading guide. The paper is organized in three parts.
 The first part (sections 2–3 as well as appendices A.1–A.2) makes the reader acquainted with the
main concepts used in the paper: section 2 provides the reader with some background concepts

                                                           , Vol. 1, No. 1, Article . Publication date: June 2026.
:4     Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

on operator-precedence grammars, incremental parsing, attribute grammars, and matching logic;
section 3 and appendices A.1–A.2 introduce KernelC and its formalization in terms of matching
logic.
   The second part (sections 4–5 and appendix A.4) describes and exemplifies how to encode
KernelC’s semantics in our attribute schema evaluation: section 4 illustrates how to encode a
verification procedure for KernelC programs annotated with matching logic properties using a
syntactic-semantic approach; section 5 and appendix A.4 show the application of this verification
procedure to a sample program.
   The third part (sections 6–9 and appendix 6.2) presents our approach for incremental verification,
compares it, also experimentally, with the state of the art, and discusses open problems: section 6
and appendix 6.2 discuss how to make the syntactic-semantic verification procedure for KernelC
incremental using SiDECAR; section 7 reports on the experimental evaluation of our implementa-
tion; section 8 discusses related work; section 9 concludes the paper, illustrating further research
directions.
   We remark that, given the large amount of technical details necessary to carry out such a work,
the main body of the paper focuses on the most relevant and critical issues; additional finer-grain
technical details have been included in appendices.

2     BACKGROUND
2.1    A syntactic-semantic approach to incremental evaluation
Upon performing a change on the data represented with a tree structure, it is possible to identify
the subtree affected by the change and replace it, without touching the rest of the tree. Various
techniques have been developed to perform this type of incremental evaluation; see, for example,
the procedure for efficient incremental parsing of LR and other deterministic context-free languages
in [26].
   In this section we outline the theoretical underpinnings for building tree structures that are
particularly well-suited for incremental evaluation, both upon syntactic and semantic changes. We
consider Floyd’s operator precedence grammars (OPGs) [24], enriched with semantic annotations
defined through a synthesized attribute schema [34]. We show how the combination of these two
formalisms allows for a simple, bottom-up parsing coupled with a semantic evaluation procedure,
which can be started efficiently at any position of the input stream, without being constrained to
proceed rigorously left-to-right. This feature naturally lends itself to incremental—and possibly
parallel—evaluation since changes may occur at any position of the program.
   Operator Precedence Grammars and their incremental parsing. Herewith we summarize the es-
sential definitions and properties that are necessary to make the paper self-contained. For more
information on formal languages and grammars, we refer the reader to classic textbooks such
as [54].
   A context-free (CF) grammar 𝐺 is a tuple 𝐺 = ⟨𝑉𝑁 , 𝑉𝑇 , 𝑃, 𝑆⟩, where 𝑉𝑁 is a finite set of non-terminal
symbols; 𝑉𝑇 is a finite set of terminal symbols, disjoint from 𝑉𝑁 ; 𝑃 ⊆ 𝑉𝑁 × (𝑉𝑁 ∪ 𝑉𝑇 ) ∗ is a relation
representing the productions of the grammar; 𝑆 ∈ 𝑉𝑁 is the axiom or start symbol. Unless otherwise
specified, we use the following convention: non-terminals are shown in sans serif font, such as
A; terminals are enclosed within single quotes, such as ‘+’ or are denoted by lowercase letters at
the beginning of the alphabet (𝑎, 𝑏, 𝑐); lowercase letters at the end of the alphabet (𝑢, 𝑣, 𝑤, 𝑥, 𝑦, 𝑧)
denote terminal strings; Greek letters denote strings in (𝑉𝑁 ∪ 𝑉𝑇 ) ∗ ; 𝜀 denotes the empty string.
   For a CF grammar 𝐺, the immediate derivation relation, denoted by ⇒, is defined on (𝑉𝑁 ∪ 𝑉𝑇 ) ∗
as follows: 𝛼 ⇒ 𝛽 if and only if (iff ) there exist 𝛼 1, 𝛼 2 , such that 𝛼 = 𝛼 1 A𝛼 2 and 𝛽 = 𝛼 1𝛿𝛼 2 , and
                                                                      ∗
(A, 𝛿) ∈ 𝑃. Its reflexive and transitive closure is denoted by ⇒. The language generated by a

, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                             :5


                                                                           ‘n’ ‘*’ ‘+’
                               S F E|T                               ‘n’       ⋗ ⋗
                               E F E ‘+’ T | T ‘+’ T                 ‘*’   
                               T F T ‘*’ ‘n’ | ‘n’                   ‘+’   ⋖ ⋖ ⋗
                                           (a)                              (b)

                 Fig. 1. Example of an operator grammar and its operator precedence matrix

                                                          ∗
grammar 𝐺 is the set of strings 𝐿(𝐺) = {𝑥 | 𝑆 ⇒ 𝑥}. Through the rest of the paper we denote a
production (A, 𝛿) ∈ 𝑃 with the usual notation A F 𝛿, where A and 𝛿 are the left hand side (lhs)
and the right hand side (rhs) of 𝑃, respectively.
   Any string generated by a grammar 𝐺 can be represented by a syntax tree describing the
derivation of the string through repeated application of the production rules starting from a root
node representing the axiom. A string is recognized to belong to the language if such syntax tree
can be constructed. This recognition is called parsing. Different parsing strategies have been studied
to build the syntax tree, either bottom-up or top-down.
   A production is in operator form if its rhs has no adjacent non-terminals; an operator grammar
(OG) contains only productions in operator form. Any CF grammar admits an equivalent OG [54].
A classic example of an operator grammar is the one generating arithmetic expressions, shown in
Figure 1a, where ‘n’ stands for any number.
   R.W. Floyd took inspiration from the traditional notion of precedence between arithmetic
operators and defined a broad class of languages, called operator-precedence languages (OPLs) or
Floyd languages, which are characterized by the fact that the shape of their syntactic tree is solely
determined by binary relations between terminals that are consecutive, or become consecutive, up
to a possible non-terminal in between, after a bottom-up reduction step. OPLs are generated by
OPGs, which are formalized as follows.
                                                                                              ∗
   Let 𝐺 be an OG, A ∈ 𝑉𝑁 , and 𝐵 ∈ 𝑉𝑁 ∪ {𝜀}; L𝐺 (A) is defined as L𝐺 (A) = {𝑎 ∈ 𝑉𝑇 | A ⇒ 𝐵𝑎𝛼 }
                                                                                   ∗
and is named the left terminal set of A; symmetrically, R𝐺 (A) = {𝑎 ∈ 𝑉𝑇 | A ⇒ 𝛼𝑎𝐵} is the right
terminal set. Three binary relations on 𝑉𝑇 , called operator precedence relations, are defined:

             equal-in-precedence:          𝑎  𝑏 iff ∃A F 𝛼𝑎𝐵𝑏𝛽, 𝐵 ∈ 𝑉𝑁 ∪ {𝜀}
                takes-precedence:          𝑎 ⋗ 𝑏 iff ∃A F 𝛼D𝑏𝛽, D ∈ 𝑉𝑁 and 𝑎 ∈ R𝐺 (D)
               yields-precedence:          𝑎 ⋖ 𝑏 iff ∃A F 𝛼𝑎D𝛽, D ∈ 𝑉𝑁 and 𝑏 ∈ L𝐺 (D)
For an OG 𝐺, the operator precedence matrix (OPM) 𝑀 = OPM (𝐺) is a |𝑉𝑇 | × |𝑉𝑇 | matrix, in which
an entry 𝑚𝑎,𝑏 represents the set of operator precedence relations holding between 𝑎 and 𝑏.
  Definition 2.1. An operator grammar 𝐺 is an operator precedence grammar1 iff 𝑀 = OPM (𝐺) is a
conflict-free matrix, i.e., for each 𝑎, 𝑏 ∈ 𝑉𝑇 , |𝑚𝑎,𝑏 | ≤ 1.
   Notice that, despite the adopted symbols, operator precedence relations are neither transitive nor
reflexive nor symmetric. Intuitively, they drive the parsing of OPLs since the rhs of any production
is enclosed within a pair ⟨⋖, ⋗⟩, and  holds between consecutive terminals occurring within such a
pair. This pair determines a rhs to be replaced, with a shift-reduce algorithm, by the corresponding
lhs. For instance, consider the grammar given in figure 1a, whose OPM is displayed in figure 1b, and
the input string ‘n + n * n’. By adding at the beginning and at the end of this string the conventional
1 Operator precedence grammars are also often called Floyd grammars in honor of the inventor.



                                                                    , Vol. 1, No. 1, Article . Publication date: June 2026.
:6     Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

                                                              S


                                                    x A z B w

                                                          y        v

                                        Fig. 2. The syntax tree of sentence 𝑥𝑦𝑧𝑣𝑤


symbol ‘#’, which yields precedence to all symbols in 𝑉𝑇 and over which all symbols in 𝑉𝑇 take
precedence, we obtain the following labeling of the string: ‘#’ ⋖ ‘n’ ⋗ ‘+’ ⋖ ‘n’ ⋗ ‘*’  ‘n’ ⋗ ‘#’. This
labeled string displays two occurrences of the rhs ‘n’ (each of them enclosed in a ⟨⋖, ⋗⟩ pair); each
of them can be reduced, in any order, to the corresponding lhs T. Since for OPGs non-terminals
are unessential to compute precedence relations, we now obtain the new precedence relations
‘#’ ⋖ T‘+’ ⋖ T‘*’  ‘n’ ⋗ ‘#’, which display the rhs T‘*’‘n’, which in turn is reduced to T. We obtain
‘#’ ⋖ T‘+’T ⋗ ‘#’, which is reduced to E and finally to S. A detailed description of parsing algorithms
for OPGs can be found in [28]. Notice that the precedence relations of the grammar of figure 1
impose that the ‘*’ operator is reduced before ‘+’, so that the resulting syntax tree reflects the usual
semantics of arithmetic expressions, where multiplication has precedence over addition.
   The main reason for the choice of OPGs is that, unlike more commonly used grammars that
support deterministic parsing, they enjoy the local parsability property, i.e., the possibility of starting
the parsing from any arbitrary point of the sentence to be analyzed, independent of the context
within which the sentence is located. Since the parsing of an OPL sentence is driven by precedence
                                                                    ∗
relations, a partial syntax tree corresponding to a derivation N ⇒ 𝑥 can be deterministically built2
(in linear time) in a bottom-up way by using only a pair of single characters, say, ⟨𝑎, 𝑏⟩ as the
context of 𝑥 (notice that necessarily 𝑎 yields precedence to the first character of 𝑥 and the last
character of 𝑥 takes precedence over 𝑏).
   Consider now the case where, after building a syntax tree for a given program, one or more
parts of the input are changed. Thanks to the local parsability property, only the changed parts
should be re-parsed. Afterwards, the newly built subtrees must be merged with the global syntax
tree using the matching condition. This condition is satisfied when, after parsing a substring, it is
possible to identify the correct nesting point of its syntax subtree within the global one.
   To intuitively illustrate the notion of matching condition, consider a sentence 𝑥𝑦𝑧𝑣𝑤 and let its
corresponding syntax tree be the one displayed in figure 2. Imagine now that within the string
𝑦 = 𝑦1𝑦2𝑦3 , the substring 𝑦2 is replaced by 𝑢, and that within string 𝑣 = 𝑣 1𝑣 2𝑣 3 the substring 𝑣 2 is
replaced by 𝑠. The new parsing could be restarted independently, possibly even in parallel, at the
beginning of 𝑢 and 𝑠 respectively (by looking for suitable ⋖, , and ⋗ within them and at their left
and right). Suppose now that during the reparsing of the input, two independent derivations are
                             ∗                ∗
obtained, respectively, A ⇒ 𝑦1𝑢𝑦3 and B ⇒ 𝑣 1𝑠𝑣 3 . Such a situation satisfies the matching condition,
since at this point we can stop re-parsing, and simply replace (i.e., match) in the original syntax tree
                                                    ∗
the subtree corresponding to the derivation A ⇒ 𝑦 with the one corresponding to the derivation
    ∗
A ⇒ 𝑦1𝑢𝑦3 and similarly for the subtree rooted in B. As a result, the overall cost of reparsing is
proportional to the length of 𝑦1𝑢𝑦3𝑣 1𝑠𝑣 3 , which in many practical cases may be considerably shorter
2 Every OPG can be tranformed into en equivalent one in Fischer normal form [23], where no two productions have the

same rhs (as in the case of figure 1a), so that for every reduction the lhs to replace the rhs is univocally defined.


, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                    :7

than the whole 𝑥𝑦1𝑢𝑦3𝑧𝑣 1𝑠𝑣 3𝑤. The above example also shows that the local parsability property
naturally supports both incremental and parallel parsing, thus enabling managing multiple changes
and even increasing the efficiency of parsing from scratch.
   A complete and detailed description of a parallel but not incremental parsing algorithm exploiting
the local parsability property of OPGs is given in [1]. In this paper our attention is mainly focused
on incremental evaluation of single changes, without exploiting parallelism; such a feature however,
is already present in our tool and, where appropriate, we will add a few hints on the further
improvements that can be obtained by enabling it.
   The local parsability property has a price in terms of generative power. More specifically, while
LR grammars—traditionally used to describe and parse programming languages but not featuring
this property—can generate all deterministic languages, OPGs cannot. This limitation, however, is
more of theoretical interest than of real practical impact. In fact, large parts of the grammars of
many computer languages are operator precedence [28, p. 271]. Complete OPGs have been given for
Prolog [18] and Algol 68 [43]; recently, OPG-based (parallel) parsers for JSON, XML, Lua have been
developed [1]. Moreover, in many practical cases an OPG can be obtained with minor adjustments
to a non operator-precedence grammar [24].
   In summary, OPGs appear to be a natural choice to support our syntactic-semantic approach to
incremental and possibly parallel evaluation.




   Attribute Grammars and incremental semantic evaluation. Attribute Grammars (AGs) have been
proposed by Knuth as a formalism to represent semantics of programming languages [34]. AGs
extend CF grammars by associating attributes and semantic functions to the production rules of a
CF grammar; attributes define the “meaning” of the corresponding nodes in the syntax tree of a
sentence generated by the grammar.
   Attributes can be of two types: synthesized attributes describe a bottom-up information flow,
from descendent nodes (of a syntax tree) to their ancestors; inherited attributes instead describe a
top-down information flow, from ancestors to descendants. In this paper we are only interested in
synthesized attributes, whose evaluation can go hand-in-hand with bottom-up parsing. It has been
proved that synthesized attributes are semantically complete, i.e., any inherited attribute can be
translated into a (set of) synthesized attribute(s) reproducing the same information [34].
   An attribute grammar that has only synthesized attributes is called an S-attributed grammar. Such
a grammar can be obtained from a context-free grammar 𝐺 = ⟨𝑉𝑁 , 𝑉𝑇 , 𝑃, 𝑆⟩ by adding a finite set of
attributes SYN and a set SFÐof semantic functions. Each symbol X ∈ 𝑉𝑁 has a set of (synthesized)
attributes SYN (X); SYN = X ∈𝑉𝑁 SYN (X). We use the symbol A to denote a generic element of
SYN ; we assume that each A takes values from a corresponding domain 𝑇A . The set SF consists of
functions, each of which is associated with a production 𝑝 in 𝑃. For each attribute A of the left hand
side of 𝑝, a function 𝑓𝑝 A ∈ SF synthesizes the value of A based on (a subset of) the attributes of the
nonterminals occurring in the right hand side of 𝑝. For example, the grammar in figure 1a can be
extended to an attribute grammar that computes the value of an expression, in the following way:
the set of attributes is defined as SYN = SYN (E) ∪ SYN (T) = {value} ∪ {value} = {value}, with
𝑇value = N; in other words, we associate an attribute value over the naturals, to both non-terminals E
and T. The set of semantic functions SF is defined as below, where semantic functions are enclosed
in braces next to each production:



                                                           , Vol. 1, No. 1, Article . Publication date: June 2026.
:8     Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

                                                           A𝑆



                                                                A𝐾
                                                          A𝑀
                                                 A𝑃                  A𝑄
                                                            A𝑁


                                                          𝑥𝑤 ′𝑧

                                 Fig. 3. Incremental evaluation of semantic attributes


                                S    FE           {value(S) = value(E)}
                                S    FT           {value(S) = value(T)}
                                E0   F E1 ‘+’ T {value(E0 ) = value(E1 ) + value(T)}
                                E    F T1 ‘+’ T2 {value(E) = value(T1 ) + value(T2 )}
                                T0   F T1 ‘*’ ‘n’ {value(T0 ) = value(T1 ) ∗ eval(‘n’)}
                                T    F ‘n’        {value(T) = eval(‘n’)}
The + and ∗ operators appearing within braces correspond to the standard arithmetic operators
(addition and multiplication); 𝑒𝑣𝑎𝑙 (·) evaluates its input as a number. Notice also that, within a
production, different occurrences of the same grammar symbol are labeled by distinct subscripts.
   During a bottom-up syntax analysis, semantic actions may be performed in conjunction with a
reduction and the computed attribute values for each node of the tree are kept for future use in case
of change. When a change is made, it is only necessary to compute the new values of attributes
for the new nodes of the new subtree produced by the incremental parser and then propagate
these values to the tree root by recomputing the attributes of the nodes encountered along the path
towards the root.
   For example, suppose that after replacing the substring 𝑤 with 𝑤 ′ in the input string 𝑥𝑤𝑧,
                                               ∗                                                 ∗
incremental re-parsing builds a derivation N ⇒ 𝑥𝑤 ′𝑧, with the same non-terminal N as in N ⇒ 𝑥𝑤𝑧,
so that the matching condition is satisfied. Assume also that N has an attribute A𝑁 . Two situations
may occur related to the computation of A𝑁 :
   (1) The A𝑁 attribute associated with the new subtree rooted in N has the same value as before
the change. In this case, all the remaining attributes in the rest of the tree will not be affected, and
no further analysis is needed.
   (2) The new value of A𝑁 is different from the one it had before the change. In this case (see
figure 3) only the attributes on the path from N to the root S (e.g., A𝑀 , A𝐾 , A𝑆 ) may change and
they need to be recomputed. The values of the other attributes not on the path from N to the root
(e.g., A𝑃 and A𝑄 ) do not change and thus there is no need to recompute them.
   We emphasize that the effort spent in evaluating the semantic attributes is proportional only
to the size of (the data structure that has been affected by) the change. Notice also that often the
semantic evaluation may cost orders of magnitude more than the cost of pure parsing (as it is the
case of the application developed in this paper); hence, the global gain obtained from incrementality
may become quite tangible. Finally, since synthesized attributes depend only on the attributes of
their descendants in the syntax-tree, their computation can be parallelized "hand in hand" with
parallel bottom-up parsing.

, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                                :9

2.2    Matching Logic
Matching logic [51] is a system to formalize the semantics, and reason about the properties,
of programs written in a von-Neumann language, such as C. It is inspired by the traditional
Floyd-Hoare method to prove program correctness. In essence, matching logic integrates a formal
operational semantics based on the notion of state and its transformation during program execution
with an axiom system that relates the preconditions holding before executing a piece of code and the
postconditions holding after its execution. This section introduces the basic concepts and notation
of matching logic, which are then used throughout the paper. For a detailed and comprehensive
description of matching logic and its proof system the reader can refer to [50, 51]. Please notice,
however, that slight notational changes appear in the various published versions of matching logic;
hereafter we take the liberty of providing a unified notation.
   Matching logic defines a basic element called configuration [49], which represents the code to be
executed at a given point of the program execution and the current state of the abstract machine
executing the program. More precisely, a configuration is a set of cells, where each cell represents
a specific semantic item whose content depends both on the purpose of the analysis and on the
features of the programming language. For example, cells may represent the current memory
allocation table, the residual code to be executed, the I/O output buffer, the next instruction pointer,
the state of the activation record. Cells are denoted with labeled angle-brackets, as in ⟨. . . ⟩label ;
a configuration is denoted with a pair of outer angle brackets enclosing a number of cells. For
example, the following configuration for a C-like program fragment:
                                        ⟨⟨x=2; y=x⟩𝑘 ⟨x ↦→ 5, y ↦→ 4⟩ env ⟩                                               (1)
contains two cells, labeled as 𝑘 and env. Cell 𝑘 represents the residual program code to be executed,
in the form of a list of statements; in this case there are two statements: the assignment of value 2
to variable x and the assignment of the value of x to y. Cell env contains a representation of the
current memory state as a map from program variables to values; in this case variable x is bound
to value 5 and y to 4.
   Matching logic formulae, also called configuration patterns (or patterns), are defined as follows.
Let Var be an infinite set of logical variables. A matching logic formula has the form ∃𝑋 .(𝜋 ∧ 𝜑) 3 ,
where:
    • 𝑋 is a subset of Var;
    • 𝜋, called the pattern structure (or basic pattern), generalizes a configuration by allowing logical
      variables in Var;
    • 𝜑, called the pattern constraint, is a formula in an arbitrary first-order logic with equality
      (FOL= ) with variables in Var.
Notice that in matching logic, differently from Hoare logic, there is a distinction between program
variables (appearing in the program code) and logical variables (defined in Var). To better highlight
this distinction, we use a monospaced font to denote program variables (e.g., x) and italics to
denote logical variables (e.g., 𝑎). On the other hand, similarly to Hoare logic, free variables in
specifications act as proof parameters, and they are expected to be bound during the proof.
   A configuration pattern defines (intensionally) a set of configurations through the concept
of matching: a configuration 𝛾 matches a configuration pattern 𝜓 ≡ ∃𝑋 .(𝜋 ∧ 𝜑) iff there is a
substitution 𝜏 of concrete values to the variables in Var such that 𝛾 is equal to 𝜋 after applying
𝜏 and the predicate obtained by applying 𝜏 to 𝜑 holds. For example, the following configuration
3 From a syntactic point of view, reference [50] introduces a dummy symbol □ of type “configuration” so that by writing

∃𝑋 .( (□ = 𝜋 ) ∧ 𝜑 ) in place of ∃𝑋 .(𝜋 ∧ 𝜑 ) we obtain a syntactically-complete FOL= formula. For simplicity, we leave the
inclusion of the □ symbol and subsequent ‘=’ as implicit in our formulae.


                                                                       , Vol. 1, No. 1, Article . Publication date: June 2026.
:10    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

pattern
                                ∃𝑎. ⟨⟨x=2; y=x⟩𝑘 ⟨x ↦→ 𝑎, y ↦→ 𝑏, . . . ⟩ env ⟩ ∧ 𝑎 ≥ 4                                       (2)
matches any configuration in which the residual program statements to execute are “x=2; y=x”
and the program variable x has a value greater than or equal to 4. In this configuration, the logical
variable 𝑏 is free, hence it has to be bound by the proof context; the symbol “. . . ” captures the other
elements of the environment. We use the notation “⟨·⟩ label ”, taken from [50], to represent an empty
cell. Configuration (1) matches configuration pattern (2) with 𝜏 = {𝑎 ↦→ 5, 𝑏 ↦→ 4}. Other examples
of configuration patterns matched by configuration (1) are:
                                          ⟨⟨x=2; y=x⟩𝑘 ⟨x ↦→ 5 . . . ⟩ env ⟩
                                     ∃𝑎. ⟨⟨x=2; y=x⟩𝑘 ⟨x ↦→ a . . . ⟩ env ⟩ ∧ a ≥ 4
                                  ∃𝑎, 𝑏. ⟨⟨x=2; . . .⟩𝑘 ⟨x ↦→ a, y ↦→ b⟩ env ⟩ ∧ a > b
    Given a programming language, it is possible to define its semantics by specifying how the
program’s abstract state changes by executing each instruction. Matching logic captures this aspect
through the concept of reachability rule, which defines a transition 𝜓 ⤋ 𝜓 ′ between two patterns
𝜓 and 𝜓 ′ . Intuitively, a rule 𝜓 ⤋ 𝜓 ′ states that every configuration 𝛾 that matches pattern 𝜓 , after
the execution of the next instruction (as defined in the 𝑘 cell of 𝛾), becomes a configuration 𝛾 ′ that
matches pattern 𝜓 ′ 4 .
    We express reachability rules using the same notation as the K framework [49], where the lhs
of a rule is above a horizontal line and the rhs is below the line; parts of the rule without a line
are the same on both sides of the rule. In this notation, we also unify the pattern constraints 𝜑
and 𝜑 ′ into a single constraint for the reachability rule, which expresses the conjunction of 𝜑 and
𝜑 ′ . For sake of clarity, we omit in this notation the existential quantifiers before the rule patterns,
avoiding situations in which a logical variable contained in both patterns of a reachability rule is
existentially quantified. For example, the reachability rule:
                                                                E 
                                x=2; y=x D          a
                                               x ↦→ , y ↦→ 4 . . .      ∧a ≥ 0                        (3)
                                  2; y=x 𝑘           2              env

allows the transition from a configuration matching pattern (2) to another configuration where the
residual program x=2; y=x has been partially interpreted (leaving the value of the expression, the
integer value 2, in cell 𝑘 5 ) and the previous value of x (i.e., 𝑎) is replaced by the integer number 2
(cell env). In general, reachability rules can be used to express the semantics of each instruction of
a programming language. These mechanisms will be described in detail in Section 3 to specify the
semantics of KernelC.
   Besides defining the semantics of a programming language, reachability rules can be used for
specifying function contracts (e.g., pre and postconditions) on the behavior of a program fragment,
e.g., a function: in fact, a rule would map the configuration pattern on the lhs (e.g., defining a function
precondition) to the pattern on the rhs (defining a postcondition). For example, a reachability rule
that defines a contract for a function sqrt computing the square root of a positive integer 𝑥 can be

4We recall that, as usual, only the free variables of the patterns are shared in a rule. For example, the following rule correctly

describes the patterns before and after the statement, but incorrectly specifies the intended semantics, since the bound
variables in the two existential quantifiers are unrelated: ∃𝑎. ⟨ ⟨x+=1;⟩𝑘 ⟨x ↦→ a⟩ env ⟩ ⤋ ∃𝑎. ⟨ ⟨·⟩𝑘 ⟨x ↦→ a + 1⟩ env ⟩. The
following reachability rule instead correctly specifies the intended semantics, since the a in the left pattern is the same as a
in the right pattern: ⟨ ⟨x+=1;⟩𝑘 ⟨x ↦→ a⟩ env ⟩ ⤋ ⟨ ⟨·⟩𝑘 ⟨x ↦→ a + 1⟩ env ⟩.
5 Notice that the integer value 2 remains in cell 𝑘 even after evaluating the assignment statement; this is consistent with the

standard C semantics, and is required to support, for example, multiple assignment statements like y=x=2.


, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                                   :11

defined as follows:
                                      
                               sqrt(𝑥)
                                           ∧ 𝑥 ≥ 0 ∧ 𝑦 ∗ 𝑦 ≤ 𝑥 ∧ (𝑦 + 1) ∗ (𝑦 + 1) > 𝑥                                        (4)
                                  𝑦     𝑘
In this example, configurations contain only cell 𝑘. In the pattern on the rhs, variable 𝑦 represents
the value computed by function sqrt after its termination6 . The pattern constraint contains both
the precondition (𝑥 ≥ 0) and the postcondition (𝑦 ∗ 𝑦 ≤ 𝑥 ∧ (𝑦 + 1) ∗ (𝑦 + 1) > 𝑥).
   Assuming that the semantics of a programming language is defined through reachability rules, it
is possible to verify the correctness of program execution by means of reachability checking over
configuration patterns. Let 𝜗, 𝜗 ′ be some configuration patterns, and R be the set of reachability rules
that define the semantics of a program fragment; we define the reachability relation { between
patterns over R as follows. We say that R ⊢ 𝜗 { 𝜗 ′ iff for each configuration 𝛾 matching 𝜗, there
exists a configuration 𝛾 ′ matching 𝜗 ′ and there is a reachability rule 𝜓 ⤋ 𝜓 ′ ∈ R such that 𝛾 and 𝛾 ′
match 𝜓 and 𝜓 ′ respectively and 𝛾 ′ is the configuration obtained applying 𝜓 ⤋ 𝜓 ′ to 𝛾. Similarly,
                ∗        +
we can define { and { as the reflexive-transitive and transitive closure of {, respectively.
                                                                                                    ∗
   In other words, given a program characterized by a set of reachability rules R, R ⊢ 𝜗 { 𝜗 ′
corresponds to a program execution, where 𝜗 is the configuration pattern representing the state
before the program execution, and 𝜗 ′ is the one representing the state after the program execution.
The reachability relation can also express a Hoare style of program (fragment) verification, in which
𝜗 expresses the program preconditions and 𝜗 ′ the program postconditions. For example, verifying
the correctness of the example above is equivalent to checking whether this reachability relation,
which represents a proof obligation, holds:
                                                      ∗
            R sqrt ⊢ ⟨⟨sqrt(𝑥)⟩𝑘 ⟩ ∧ 𝑥 ≥ 0 { ∃𝑦. ⟨𝑦⟩𝑘 ∧ 𝑦 ∗ 𝑦 ≤ 𝑥 ∧ (𝑦 + 1) ∗ (𝑦 + 1) > 𝑥                                     (5)
where R sqrt is the set containing the reachability rules that describes the semantics of the im-
plementation of function sqrt. On the basis of such proof obligation it is possible to derive the
following reachability relation:
                                                                            ∗
   R sqrt ⊢ ⟨⟨y = sqrt(x)⟩𝑘 ⟨x ↦→ 𝑎, y ↦→ 𝑏⟩ env ⟩ ∧ 𝑎 ≥ 0 {
                                         ∃𝑐. ⟨⟨·⟩𝑘 ⟨x ↦→ 𝑎, y ↦→ 𝑐⟩ env ⟩ ∧ 𝑐 ∗ 𝑐 ≤ 𝑎 ∧ (𝑐 + 1) ∗ (𝑐 + 1) > 𝑎                 (6)
   Reachability properties can be expressed by adding suitable annotations to the program code
as it is now customary in various programming languages. These annotations may also specify
loop invariants, which are a key point in Hoare style verification. Proofs are then built by applying
matching logic’s axiomatization, which consists of eight axioms and inference rules [50].
   The verification of reachability properties is supported by MatchC [16], a tool implemented on
top of the K framework [49], which is a rewriting-based formalism for developing and analyzing
programming languages. The K framework in turn uses Maude [12] as rewriting system. To
check that every possible execution reaches a desired configuration pattern 𝜗 ′ , a set of reachable
configurations is first initialized with the configuration pattern 𝜗; then, all the reachability rules in
R are applied on all the reachable configurations matching the pattern, discovering new reachable
configurations. The process terminates when a fixed point is reached or as soon as a configuration
pattern violating 𝜗 ′ survives the next iteration (i.e., the execution cannot leave it). Notice that
reachability rules have to encode also the execution of invalid operations, e.g., a division by zero,
by moving the execution into a sink error configuration that cannot be left. Given that program
correctness is an undecidable problem, the tool cannot always provide a final answer. In particular,
in the case of loops, if they are annotated by suitable invariants, the tool tries to exploit them;
6 Note that it is possible to have logical variables to represent integer values in cell 𝑘, like 𝑥 and 𝑦.



                                                                           , Vol. 1, No. 1, Article . Publication date: June 2026.
:12    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

otherwise it unfolds them, on the condition that an upperbound for the number of unfolding steps
is provided (to avoid the risk of nontermination).

Reading Guide
The next two sections describe how KernelC and its matching logic formal semantics can be used
in SiDECAR to build an incremental verifier for realistic KernelC programs specified in matching
logic. More precisely:
    • In Section 3 we show how the syntax of KernelC has been reshaped into an operator prece-
       dence grammar. We remark that “reshaping the language syntax” is a fairly normal and easy
       practice whenever one has to adapt the original BNF of a programming language to the
       format of a given parser generator (e.g., by removing shift-reduce conflicts when using an
       LALR parser like Bison [40] or to make it suitable for LL parsing). Section 3 also includes a
       summary of the semantics of KernelC expressed using matching logic.
    • In the key Section 4 we show how the language semantics has been implemented as a suitable
       attribute schema, to be used within SiDECAR. We remark that the equivalence between
       the original KernelC definition and our own implementation can be verified by a — tedious
       but natural — inspection of the various attribute definitions; it is further confirmed by our
       experiments, as will be shown in Section 7.
After these two sections, we describe how KernelC programs specified in matching logic can be
verified using SiDECAR, either from scratch (through an example Section 5) or incrementally
(Section 6).

3     KERNELC AND ITS SEMANTICS
KernelC supports several types of expression (assignment, pointer referencing and de-referencing,
structure member, arithmetic and logic operators, ternary conditional, function call), the basic
control structures (sequences, while, if/else, return), the data types integer, void, struct and
corresponding pointers, arrays, and some functions from the standard library (malloc/free and
basic I/O). An excerpt of the KernelC grammar (in operator precedence form) is shown in figure 47 ,
where question marks indicate optional elements. The non-terminal Annotation (not expanded
in the grammar) is used to define function contracts and loop invariants, further discussed in
Section 3.2 and 3.3.
   We present the operational semantics of KernelC constructs in the form of Matching Logic
reachability rules. These rules correspond to the original semantics defined in [16], with minor
syntactic changes. We adopt the same assumptions and restrictions as [16] to resolve the ambiguity
inherited from the corresponding C semantics and to simplify reachability verification: expressions
are evaluated left to right to avoid non-determinism; integers have infinite precision; structure
fields can only be of type integer; I/O primitives can only read and write integers.
   KernelC semantics is defined using the following Matching Logic configuration cells:
     • 𝑘: the residual program code to be executed;
     • env: a mapping of variable identifiers to their values;
     • stack: the call stack of the active functions;
     • estack: the stack of the local scopes for each active function in stack;
     • mem: the heap state, represented as a map from addresses to dynamically-allocated objects;
     • ma: a map from dynamically-allocated objects to the size of the memory allocated for them;
     • in: standard input, represented as a list of integers in which values are accessed left to right;
     • out: standard output, represented as a list of integers to which values can only be appended.
7 The full operator precedence KernelC grammar is available at https://hub.docker.com/r/arizzi/scmatchc/.



, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                  :13

program ::= global_decl
global_decl ::= ‘struct’ IDENTIFIER ‘{’ struct_field_list ‘}’ ‘;’ global_decl? |
      parameter ‘;’ global_decl? | function_def
struct_field_list ::= parameter ‘;’ struct_field_list?
compound ::= compound_decl | compound_stm
compound_decl ::= parameter ‘;’ compound
parameter ::= type IDENTIFIER | ptr_type ‘*’ id
parameter_list ::= parameter | parameter ‘,’ parameter_list
type ::= ‘int’ | ‘void’ | ‘struct’ IDENTIFIER
ptr_type ::= ptr_type ‘*’ | type
type2 ::= ‘(’ ( type | ptr_type ) ‘)’
id ::= IDENTIFIER
compound_stm ::= Annotation? ‘while’ ‘(’exp‘)’ ‘{’ compound ‘}’ compound_stm |
      ‘if’ ‘(’exp‘)’ ‘{’ compound ‘}’ ‘else’ ‘{’ compound ‘}’ compound_stm |
      ‘if’ ‘(’exp‘)’ ‘{’ compound ‘}’ compound_stm |
      ‘return’? exp ‘;’ compound_stm | stm
stm ::= ‘return’? exp ‘;’ | ‘{’ compound_decl ‘}’ |
      ‘if’ ‘(’exp‘)’ ‘{’ compound ‘}’ ‘else’ ‘{’ compound ‘}’ |
      ‘if’ ‘(’exp‘)’ ‘{’ compound ‘}’
argument_exp_list ::= exp ‘,’ argument_exp_list | exp ‘,’ exp
exp ::= unary_exp (‘=’|‘+=’|‘-=’|‘*=’|‘/=’|‘%=’) exp | cond_exp
cond_exp ::= log_or_exp | log_or_exp ‘?’ exp ‘:’ cond_exp
log_or_exp ::= log_or_exp ‘||’ log_and_exp | log_and_exp
log_and_exp ::= log_and_exp ‘&&’ eq_exp | eq_exp
eq_exp ::= eq_exp (‘==’|‘!=’) relat_exp | relat_exp
relat_exp ::= relat_exp (‘>’|‘<’|‘>=’|‘<=’) add_exp | add_exp
add_exp ::= add_exp (‘+’|‘-’) mult_exp | mult_exp
mult_exp ::= mult_exp (‘*’|‘/’|‘%’) cast_exp | cast_exp
cast_exp ::= ‘(’ ptr_type ‘)’ cast_exp | unary_exp
function_def ::= ptr_type IDENTIFIER function_def2
function_def2 ::= ‘(’ parameter_list? ‘)’ Annotation? ‘{’ compound? ‘}’ global_decl?
postfix_exp ::= id | Constant postfix_exp1? | ‘(’exp‘)’ |
      IDENTIFIER ( postfix_exp2 | postfix_exp1 )
postfix_exp1 ::= (‘.’|‘->’) IDENTIFIER ( postfix_exp1 )?
postfix_exp2 ::= ‘(’(exp|argument_exp_list)?‘)’ postfix_exp1?
unary_exp ::= postfix_exp | ‘sizeof’ type2 | cast_exp |
      (‘+’|‘-’|‘*’|‘!’|‘sizeof’) unary_exp

                               Fig. 4. Excerpt of the KernelC grammar



   In the rest of the section we describe semantics by presenting, for each type of syntactic con-
struct, the structure of the corresponding cells and the associated reachability rules. Due to space
reasons, we omit the description of input/output and provide only a short overview to mem-
ory management; the description of the complete semantics for these constructs is available in
Appendices A.1.2 and A.2, respectively.

3.1   Basic constructs
Table 1 shows the reachability rules related to KernelC constructs for declaration, expression
evaluation, assignment, and choice.

                                                          , Vol. 1, No. 1, Article . Publication date: June 2026.
:14    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

                           Table 1. Reachability rules for the basic constructs of KernelC


                            Construct                     Reachability rule
                                                                                                       
                                                             type x;                       ·
                 Typed variable declaration                               ...                         ...
                                                                  ·              𝑘 x ↦→ (type, ⊥)          env
                                                                                                 
                                                               x
                  Typed variable evaluation                          . . . ⟨x ↦→ (t, a) . . . ⟩ env
                                                             (𝑡, 𝑎)         𝑘
                                                          D                E                
                                                             x = 𝑎                     𝑏
                           Assignment                                  ...       x ↦→ . . .
                                                                𝑎             𝑘        𝑎      env
                                                                                             
                                                             if(𝑐) {T} else {E}
                   Selection (then branch)                                                ...       ∧𝑐 ≠ 0
                                                                            T                   𝑘
                                                                                             
                                                             if(𝑐) {T} else {E}
                   Selection (else branch)                                                ...       ∧𝑐 = 0
                                                                            E                   𝑘
                                                                                  
                                                             if(𝑐) {T}
                   Selection (branch taken)                                    ...     ∧𝑐 ≠ 0
                                                                    T               𝑘
                                                                                  
                                                             if(𝑐) {T}
                 Selection (branch not taken)                                  ...     ∧𝑐 = 0
                                                                    ·               𝑘




   A variable declaration adds to env a mapping from the identifier used in the declaration to an
undefined value (conventionally denoted with ⊥)8 . Expressions composed by a single variable
are evaluated replacing the variable with its value from env. We maintain in cells 𝑘 and env pairs
(type,variable) keeping track of the specific variable type, where type is any of the types supported
by Kernel C, e.g., int or struct listNode*.
   We use the logical variable 𝑡 to represent a generic type, which remains unknown up to the
application of the reachability rule to a configuration pattern which binds 𝑡 to a certain type. To
simplify the notation, throughout the rest of the paper we omit the type for a plain C int integer
logical variable.
   More complex expressions are evaluated recursively, preserving the precedence among the
operators defined in the grammar of KernelC. Evaluating an assignment statement results in
updating the entry in env corresponding to the lhs with the new value obtained evaluating the
rhs of the assignment. As already mentioned in Section 2.2, the assignment statement in cell 𝑘 is
replaced by the new value of the assigned variable.
   Evaluating a selection statement introduces a branch in the execution, accounting for the satis-
faction or violation of the selection condition. This corresponds to the introduction of two guarded
reachability rules, which determine the next statements to execute based on the boolean evaluation
of the selection condition. The evaluation of a sequence of statements corresponds to evaluating
each statement in the sequence, in the order prescribed by the sequence itself.
   Note that for any reachability rule, unless otherwise specified, every logical variable contained
in it has a local scope within the rule itself and is different from the variables with the same name
in other reachability rules.
8 The case in which the variable identifier is already declared is not discussed here.



, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                                 :15

3.2    Loops
KernelC only provides while loops. The semantics of a loop construct corresponds to its one-
step unwinding, as described in rule (7). Notice that rule (7) is applied before evaluating the loop
condition C; the latter is evaluated before executing the selection statement. The unwinding is
recursively applied until the condition cannot be satisfied (possibly leading to nontermination9 ).
                                                                
                                         while(C){T}
                                                             ...                                  (7)
                                   if(C){T while(C){T}}            𝑘
For example, for the code snippet while(t>0){c=c+t; t=t-1;}, the corresponding loop unrolling
reachability rule is:
                                                                             
                               while(t>0){c=c+t; t=t-1;}
                                                                          ...              (8)
                 if(t > 0){c=c+t; t=t-1; while(t>0){c=c+t; t=t-1;}}            𝑘
Let us consider the following configuration, characterizing the state of the abstract machine at the
beginning of the loop:
                           ⟨⟨while(t>0){c=c+t; t=t-1;}⟩𝑘 ⟨t ↦→ 1, c ↦→ 0⟩ env ⟩                                             (9)
By applying rule (8) we obtain the configuration:
           ⟨⟨if(t>0){c=c+t;t=t-1; while(t>0){c=c+t;t=t-1;}}⟩𝑘 ⟨t ↦→ 1, c ↦→ 0⟩ env ⟩                                       (10)
The execution of the if statement leads to the following configuration:
                            ⟨⟨while(t>0){c=c+t;t=t-1;}⟩𝑘 ⟨t ↦→ 0, c ↦→ 1⟩ env ⟩                                            (11)
Although similar to configuration (9), in this configuration the program variable t has value 0,
which will cause the if branch to be skipped in the next loop iteration.
   Rule (7) executes loops through a series of successive unwinding steps. However, KernelC
supports also the concept of a loop invariant, as already proposed in Hoare logic. The loop invariant
is represented by an annotation 𝐴 placed before the loop body; the invariant is checked and used
to execute the loop (instead of the unwinding steps). Annotation 𝐴 has the form of the following
configuration pattern
                                    ⟨⟨while(C){T} . . . ⟩𝑘 𝛹⟩ ∧ 𝜑                                (12)
with 𝛹 representing the rest of the basic pattern and 𝜑 the pattern constraint.
  An example of an invariant for the above example loop is that the value of t is non-negative and
that c contains the sum of the numbers between 𝑖 and the initial value of t (denoted with ℎ); this
invariant is formalized by the following configuration pattern:


   ∃𝑖, 𝑗 . ⟨⟨while(t>0){c=c+t; t=t-1;} . . . ⟩𝑘 ⟨t ↦→ 𝑖, c ↦→ 𝑗⟩ env ⟩
                                                                             ℎ(ℎ + 1) − 𝑖 (𝑖 + 1)
                                                                            ∧𝑖 ≥ 0∧ 𝑗 =                                    (13)
                                                                                      2
The loop invariant is checked to see if it holds after every iteration of the loop.
                                                            +
                ∃𝑋 . ⟨⟨while(C){T} . . . ⟩𝑘 𝛹⟩ ∧ 𝜑 { ∃𝑋 ′ . ⟨⟨while(C){T} . . . ⟩𝑘 𝛹 ′ ⟩ ∧ 𝜑 ′                             (14)
  This check is performed by evaluating formula (14), in which the lhs is the invariant itself and
the rhs is another instance of the invariant, obtained by replacing any bound variable in 𝛹 and
9 For practical reasons, the total number of execution steps can be bound by the user to guarantee the (possibly inconclusive)

termination of the verification process.


                                                                         , Vol. 1, No. 1, Article . Publication date: June 2026.
:16     Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

𝜑 with a new variable, thus 𝛹 ′ and 𝜑 ′ are obtained respectively from 𝛹 and 𝜑 by renaming every
logical variable occurrence. This corresponds to the application of the while rule of Hoare logic.
  To check the invariant, any execution from the configuration pattern ∃𝑋 . ⟨⟨if(C){T}⟩𝑘 𝛹⟩ ∧ 𝜑
must reach the target configuration pattern ∃𝑋 ′ . ⟨⟨·⟩𝑘 𝛹 ′ ⟩ ∧ 𝜑 ′ . Notice that as part of this check,
one iteration of the loop is performed and thus the while loop is reduced to an if statement. For
the example above, checking the invariant corresponds to evaluating the following formula, given
LOOP ≡ while(t>0){c=c+t;t=t-1;}:
                                                                 ℎ(ℎ + 1) − 𝑖 (𝑖 + 1) +
   ∃𝑖, 𝑗 . ⟨⟨LOOP⟩𝑘 ⟨t ↦→ 𝑖, c ↦→ 𝑗⟩ env ⟩ ∧ 𝑖 ≥ 0 ∧ 𝑗 =                              {
                                                                          2
                                                                                             ℎ(ℎ + 1) − 𝑙 (𝑙 + 1)
                             ∃𝑙, 𝑚. ⟨⟨LOOP⟩𝑘 ⟨t ↦→ 𝑙, c ↦→ 𝑚⟩ env ⟩ ∧ 𝑙 ≥ 0 ∧ 𝑚 =                                   (15)
                                                                                                      2
In this case, the initial configuration pattern is:
                                                                                            ℎ(ℎ + 1) − 𝑖 (𝑖 + 1)
      ∃𝑖, 𝑗 . ⟨⟨if(t>0){c=c+t;t=t-1;}⟩𝑘 ⟨t ↦→ 𝑖, c ↦→ 𝑗⟩ env ⟩ ∧ 𝑖 ≥ 0 ∧ 𝑗 =                                        (16)
                                                                                                     2
and the target configuration pattern is:
                                                                                ℎ(ℎ + 1) − 𝑙 (𝑙 + 1)
                      ∃𝑙, 𝑚. ⟨⟨·⟩𝑘 ⟨t ↦→ 𝑙, c ↦→ 𝑚⟩ env ⟩ ∧ 𝑙 ≥ 0 ∧ 𝑚 =                                             (17)
                                                                                         2
   After checking that a loop invariant is satisfied, it can be used in the following reachability rule10 :
                                                             
                                   while(C){T}              𝛹
                                                    ...       ′
                                                                  ∧ 𝜑 ∧ 𝜑′                           (18)
                                   assume(!C);            𝑘 𝛹
which changes the current configuration replacing bound variables in the pattern with fresh ones,
while still satisfying the invariant. In this rule, function assume (whose semantics is provided in
rule (19)), is used to discard from the obtained configuration pattern all the configurations in which
the loop condition C evaluates to false.
                                                         
                                        assume(𝑐);
                                                      ...     ∧𝑐 ≠ 0                               (19)
                                              ·            𝑘

   In the case of our example, rule (18) is instantiated as:
                                                            
       while(t>0){c=c+t;t=t-1;}                    𝑖        𝑗
                                     ...      t ↦→ , c ↦→
            assume(!(t>0));               𝑘        𝑙       𝑚 env
                                                  ℎ(ℎ + 1) − 𝑖 (𝑖 + 1)          ℎ(ℎ + 1) − 𝑙 (𝑙 + 1)
                          ∧𝑖 ≥ 0∧𝑙 ≥ 0∧ 𝑗 =                            ∧𝑚 =                          (20)
                                                           2                             2
By combining it with the semantics of assume, we obtain the following reachability rule:
                                                            
       while(t>0){c=c+t;t=t-1;}                    𝑖        𝑗
                                     ...      t ↦→ , c ↦→
            assume(!(t>0));               𝑘        𝑙       𝑚 env
                                                              ℎ(ℎ + 1) − 𝑖 (𝑖 + 1)         ℎ(ℎ + 1)
                                     ∧𝑖 ≥ 0∧𝑙 = 0∧ 𝑗 =                             ∧𝑚 =              (21)
                                                                       2                       2
   Notice that the constraint 𝑙 = 0 is derived from the conjunction of the condition in rule (20)
(𝑙 ≥ 0) with the semantics of assume over the condition 𝑙 ≤ 0. Thus 𝑙 (𝑙 + 1) has value 0.

10 The notation 𝜓 is a generalization of the one used in rule (3) for expressing the pattern structure.
                𝜓′


, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                               :17

3.3    Functions
Supporting function invocation requires formalizing the call stack and the local scope of each active
function. This is accomplished by introducing cells stack and estack.
   When a function f is invoked, its identifier is pushed to stack, the current environment described
in env is pushed to estack, and the new current environment becomes a mapping from the formal
parameters of f to their values at the invocation11 . This is formalized in rule (22), where F represents
the body of the function, which is inlined at the invocation site in cell 𝑘 and followed by the
placeholder END (representing the end of the function body).
                                                           D                              
                f(arg 1, . . . )                𝐸                  ·     E         ·
                                 ...                                 ...             ...                                 (22)
                   F END              𝑘 param1 ↦→ arg 1, . . . 𝑒𝑛𝑣 𝐸       𝑒𝑠𝑡𝑎𝑐𝑘 f        𝑠𝑡𝑎𝑐𝑘
For example, let us consider the following function:
   int sum(int a, int b) { return a + b; }
Its associated reachability rule is the following:
                                                    D                                 
                  sum(𝑖, 𝑗)                    𝐸            ·     E       D ·      E
                                  ...                         ...              ...                                       (23)
             return a + b; END         𝑘 a ↦→ 𝑖, b ↦→ 𝑗 𝑒𝑛𝑣 𝐸       𝑒𝑠𝑡𝑎𝑐𝑘 sum       𝑠𝑡𝑎𝑐𝑘
   Let us assume the following start configuration:
                                   ⟨⟨sum(x, x)⟩𝑘 ⟨x ↦→ 2⟩𝑒𝑛𝑣 ⟨·⟩𝑒𝑠𝑡𝑎𝑐𝑘 ⟨·⟩𝑠𝑡𝑎𝑐𝑘 ⟩                                        (24)
Before executing the function call, we have to evaluate the actual parameters to be passed to
function sum, evaluating the expression x thus getting:
                                   ⟨⟨sum(2, 2)⟩𝑘 ⟨x ↦→ 2⟩𝑒𝑛𝑣 ⟨·⟩𝑒𝑠𝑡𝑎𝑐𝑘 ⟨·⟩𝑠𝑡𝑎𝑐𝑘 ⟩                                        (25)
By applying rule (23), we get
                ⟨⟨return a + b; END⟩𝑘 ⟨a ↦→ 2, b ↦→ 2⟩𝑒𝑛𝑣 ⟨(x ↦→ 2)⟩𝑒𝑠𝑡𝑎𝑐𝑘 ⟨sum⟩𝑠𝑡𝑎𝑐𝑘 ⟩ ;                                (26)
continuing the execution, we end up with:
                     ⟨⟨return 4; END⟩𝑘 ⟨a ↦→ 2, b ↦→ 2⟩𝑒𝑛𝑣 ⟨(x ↦→ 2)⟩𝑒𝑠𝑡𝑎𝑐𝑘 ⟨sum⟩𝑠𝑡𝑎𝑐𝑘 ⟩                                 (27)
   The return of a function, corresponding to the evaluation of the return construct, is formalized
as shown in rule (28): all the code from the return point to the placeholder END is consumed, the
function identifier is popped out of stack and the environment env is restored to its state before
the function invocation (by popping out from estack), the returned value i is added to the residual
code in place of the function invocation. Notably, the evaluation of recursive functions may lead to
nontermination.
                                        D E                                 
                  return i . . . END        ...      𝐸               f
                                     ...               ...             ...                  (28)
                          i               𝑘  𝐸 𝑒𝑛𝑣 ·         𝑒𝑠𝑡𝑎𝑐𝑘 ·        𝑠𝑡𝑎𝑐𝑘
  In the example above, the application of reachability rule (28) would result in the following
configuration:

                                        ⟨⟨·⟩𝑘 ⟨x ↦→ 2⟩𝑒𝑛𝑣 ⟨·⟩𝑒𝑠𝑡𝑎𝑐𝑘 ⟨·⟩𝑠𝑡𝑎𝑐𝑘 ⟩                                           (29)
11 In this way we can handle only local variables. Although global variables are not supported by KernelC, it would be

possible to manage them by adding another cell global, with the same structure of env, holding global variables. Differently
from env, such cell would not be modified by function calls. This addition would only require slight changes to the rules
evaluating and storing variables.


                                                                       , Vol. 1, No. 1, Article . Publication date: June 2026.
:18    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

   A function can be annotated with a function specification (i.e., function contract) that represents
a reachability rule defining how the program state changes after the function execution. This rule,
which can be used to summarize a function call, has the form:
                                                                
                                      f(arg 1, . . . )         𝛹
                                                       ...       ′
                                                                     ∧𝜑                           (30)
                                            𝑖                𝑘 𝛹
   For the sum function above, let us assume that the function is annotated with a specification that
states that the result of the function is the sum of the two arguments. The behavior of the function
can then be summarized by the following reachability rule:
                                                    
                                       sum(𝑜, 𝑝)
                                                 ...     ∧𝑞 = 𝑜 +𝑝                               (31)
                                            𝑞         𝑘
  Starting from rule (30), one can generate the configuration patterns representing the state at the
beginning of the function invocation:
                                              ∃𝑋 .        f(arg 1, . . . ) 𝑘 𝛹 ′ ∧ 𝜑                                  (32)
and at the end:
                                                      ∃𝑋 ′ . ⟨⟨𝑖⟩𝑘 𝛹⟩ ∧ 𝜑                                             (33)
   The function contract can then be checked by checking that pattern (33) is always reached
starting from pattern (32).

3.4    Memory Management
KernelC supports dynamic allocation of memory objects. These objects can be either integers or
sequences of integers, possibly constituting a struct.
   The cell mem of a KernelC configuration is used to represent dynamically allocated objects, with
a map between locations and objects. For example ⟨𝑙 ↦→ 𝑂⟩ mem represents a heap allocation in
which the memory object 𝑂 is at location 𝑙. Object 𝑂 can be an integer, a structured type (i.e., a
sequence of integers or a struct), or an abstract data type like a list. Each addressable memory
location contains one infinite-precision integer12 ; structured objects span over multiple locations.
   Structured types can have two different representations: a compact one, in which the whole
object is associated to its first location; a flat one, in which the object is split into contiguous
locations, each holding an integer value. For example, let us assume that the sequence [2, 3] is
stored starting from memory location 𝑝. The content of the cell mem using the compact notation
would be ⟨𝑝 ↦→ [2, 3]⟩ mem ; using the flat notation for the same memory location, we would get
⟨𝑝 ↦→ 2, 𝑝 + 1 ↦→ 3⟩ mem .
   The deallocation of an object through a pointer to its first location (similarly to the free operation
in C) is supported by keeping track of the size of each object. More precisely, the number of blocks
allocated for a structured object is saved in the KernelC configuration cell ma, which contains a
map 𝑙 ↦→ 𝑛 associating to each location allocated in cell mem the number of blocks occupied by the
associated object13 .

4     SEMANTIC EVALUATION
We now describe how reachability checking over matching logic configuration patterns can be
performed by evaluating semantic attributes.
12 Notice that the actual size of the memory location may vary depending on the size of the integer stored in the location.
13We further extend the operations supported in [16] to catch additional errors related to memory allocation. These

extensions are described in details in Appendix A.2.


, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                               :19


 1: function Process(𝑣𝑡 = ⟨𝐶𝑟 , 𝑅𝑣 , 𝑐𝑡 ⟩ )                   22: function Check(𝑣𝑡 = ⟨𝐶𝑟 , 𝑅𝑣 , 𝑐𝑡 ⟩ )
 2: repeat                                                    23: if CheckNonFinal (𝐶𝑟 ) then
 3:     Changed ← false                                       24:     return false
 4:     for 𝑐𝑖 ∈ 𝐶𝑟 do                                        25: end if
 5:       temp ← ∅                                            26: for 𝑐𝑖 ∈ 𝐶𝑟 do
 6:       for 𝑟𝑖 ∈ 𝑅𝑣 do                                      27:     if ¬isContained (𝑐𝑖 , 𝑐 𝑡 ) then
 7:           if isApplicable (𝑟𝑖 , 𝑐𝑖 ) then                 28:        return false
 8:              𝑐 ′ ← ApplyRule (𝑟𝑖 , 𝑐𝑖 )                   29:     end if
 9:              if isSat (𝑐 ′ ) then                         30: end for
10:                  temp ← temp ∪ c ′                        31: return true
11:              end if                                       32: end function
12:           end if
13:        end for                                            33: function CheckNonFinal(𝐶𝑟 )
14:        if temp ≠ ∅ then                                   34: for 𝑐𝑖 ∈ 𝐶𝑟 do
15:           Changed ← true                                  35:     if isNonFinal (𝑐𝑖 ) then
16:           𝐶𝑟 ← 𝐶𝑟 ∪ temp ∖ {𝑐𝑖 }                          36:        return true
17:        end if                                             37:     end if
18:     end for                                               38: end for
19: until ¬Changed                                            39: return false
20: return ⟨𝐶𝑟 , 𝑅𝑣 , 𝑐𝑡 ⟩                                    40: end function
21: end function


                              Fig. 5. The Process and Check algorithms for verification tasks

4.1     Overview
As we mentioned earlier, our approach can handle program verification at any level of precision,
ranging from Hoare-style program verification, when the program is fully annotated, to debugging-
style verification if few or no annotations are provided. In fact, a distinguishing feature of Matching
Logic is the integration of symbolic interpretation to evaluate program semantics with program
property proofs in classical Hoare’s style through the key concept of reachability rule. For instance,
a reachability rule can formalize the effect of a single loop iteration, which can be iterated through
loop unfolding, but can also be used to prove a loop invariant if such an invariant is supplied.
   To encompass the entire spectrum of kinds of program verification, we introduce the notion of
verification task, which is attached to any single program unit in a typical compositional, syntax-
directed style. A verification task is a triple vt = ⟨𝐶𝑟 , 𝑅𝑣 , 𝑐𝑡 ⟩, where:
    • 𝐶𝑟 is a set of configuration patterns, initialized with the singleton {𝑐𝑠 }, where 𝑐𝑠 is a configu-
       ration pattern representing the initial state of the program as defined by the precondition;
    • 𝑅𝑣 is a set of reachability rules specifying the program behavior;
    • 𝑐𝑡 is a configuration pattern representing the desired state after the program execution, as
       defined by the postcondition.
   Before presenting the algorithm for performing a verification task, we introduce the concept of
final configuration pattern. A configuration pattern is final if one of these conditions is satisfied:
    • its cell 𝑘 is empty, i.e., there is no residual program code to be executed;
    • its cell 𝑘 is not empty but contains only an integer value resulting from the evaluation of a
       statement;
    • it represents a sink error configuration, i.e., a configuration characterized by a special token
       in cell 𝑘 from which no further steps can be performed.
Notice that 𝑐𝑡 in a verification task is always final.
   A verification task is performed using the Process and Check algorithms shown in figure 5.
The latter takes as input a verification task vt (resulting from the processing by the former), and
returns a boolean value stating whether the unit in vt satisfies its specification. These algorithms
use a number of auxiliary functions:

                                                                       , Vol. 1, No. 1, Article . Publication date: June 2026.
:20    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

      • function isApplicable(𝑟, 𝑐) takes as input a reachability rule 𝑟 of the form 𝜓 ⤋ 𝜓 ′ and a
        pattern 𝑐, and returns true iff there exists a configuration 𝛾 such that 𝛾 matches both 𝑐 and 𝜓
        without considering their constraints,; its purpose is to avoid the application of expensive
        operations using the structure of the configuration pattern;
      • function ApplyRule(𝑟, 𝑐) applies rule 𝑟 to pattern 𝑐 (corresponding to abstractly executing
        the next statement in cell 𝑘 of 𝑐) and returns the new configuration reached by the abstract
        execution;
      • function isSat (c) takes a configuration pattern 𝑐, transforms it into a logic formula with
        integer arithmetics and unspecified functions, and checks the satisfiability of this formula with
        an SMT solver; if the formula is satisfiable it means that there exists at least one configuration
        satisfying the constraints in the configuration pattern 𝑐;
      • function isNonFinal(𝑐) checks whether the configuration pattern 𝑐 is non-final;
      • function isContained (𝑐 1, 𝑐 2 ) takes two configuration patterns and uses an SMT solver to
        check whether all the configurations matching the first configuration pattern also match the
        second.
   Algorithm Process performs a verification task by iterating (lines 2–19) through the set 𝐶𝑟
(initially containing only 𝑐𝑠 ) until reaching a fixed point, i.e., when 𝐶𝑟 does not change anymore.
For each configuration pattern 𝑐𝑖 ∈ 𝐶𝑟 , the algorithm applies all the rules in 𝑅𝑣 (lines 6–13) that
are applicable to 𝑐𝑖 . At each iteration, the application of a rule 𝑟𝑖 ∈ 𝑅𝑣 to a pattern 𝑐𝑖 results in
a new configuration pattern 𝑐 ′ ; if the constraints in 𝑐 ′ are satisfiable, 𝑐 ′ is added to an auxiliary
list temp. When all the applicable rules have been applied to 𝑐𝑖 , if at least one new configuration
pattern has been discovered (meaning that list temp is not empty), 𝑐𝑖 is removed from 𝐶𝑟 , while
the newly-generated configuration patterns stored in temp are added to 𝐶𝑟 (lines 14–17). At each
iteration, 𝐶𝑟 represents the maximal front of reachable configuration patterns from the initial
configuration.
   Algorithm Check analyzes whether a verification task obtained through the Process algorithm
satisfies its specification. In the verification task provided by Process, the configuration patterns
𝐶𝑟 must be final; a non-final configuration pattern in 𝐶𝑟 would indicate an incorrect input program
(e.g., a program in which some function definitions are missing). Function CheckNonFinal is
invoked (line 23) to detect non-final configuration patterns (through the loop at lines 34–38); in
case a non-final configuration pattern is found, the algorithm is aborted returning false. The final
loop (lines 26–30) checks whether for each configuration pattern 𝑐𝑟 ∈ 𝐶𝑟 , for all configuration 𝛾
matching 𝑐𝑟 , 𝛾 also matches 𝑐𝑡 ; the algorithm returns true iff this check is successful.
   To better understand our reachability checking procedure, let us consider the following simple
example:
       1   int sum(int t)
               DD     E E
                      sum(𝑥 )
            ML




       2                 𝑦        ∧ 𝑥 ≥ 0 ∧ 𝑦 = 𝑥 (𝑥 + 1)/2
                              𝑘
       3   {
       4       int c;
       5       c=0;
                 ML




       6           ∃𝑖, 𝑗 . ⟨ ⟨while(t>0){c=c+t;t=t-1;}⟩𝑘 ⟨t ↦→ 𝑖, c ↦→ 𝑗 ⟩ env ⟩ ∧ 𝑖 ≥ 0 ∧ 𝑗 = (ℎ (ℎ + 1) − 𝑖 (𝑖 + 1) )/2
       7       while(t>0){
       8         c=c+t;
       9         t=t-1;
      10       }
      11       return c;
      12   }



, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                       :21

   This code snippet consists of a function which sums the first t non-zero natural numbers.
The function contract (line 2) specifies that the input parameter must be non-negative and the
returned value must be the sum of the first t numbers. The loop is annotated with an invariant
(line 6) specifying that program variable t must be non-negative and 𝑐 must contain the sum of
the natural numbers between the current value of t and the initial value of t. The specifications
provided as matching logic configuration patterns and reachability rules are enclosed in a box like
 ML




    specification .
   For this example, our reachability checking procedure would consider two verification tasks:
one for the function contract and one for the loop invariant. Here, for brevity, we only illustrate
how to perform the verification task corresponding to the loop invariant.
   Notice that the loop code (and its loop invariant) are the same as the ones examined in Sec-
tion 3.2; following the same reasoning, we have to check formula (15). The three components of
the verification task for the loop invariant are:
    • 𝐶𝑟 = {∃𝑖, 𝑗 . ⟨⟨if(t>0){c=c+t;t=t-1;}⟩𝑘 ⟨t ↦→ 𝑖, c ↦→ 𝑗⟩ env ⟩ ∧ 𝑖 ≥ 0 ∧ 𝑗 = (ℎ(ℎ + 1) − 𝑖 (𝑖 +
       1))/2} (the same as formula (16));
    • 𝑅𝑣 is the set containing the reachability rules describing the semantics of the program; in this
       case, it includes the reachability rules for the if statement, expression (variable) evaluation,
       assignment and comparison operations (see Section 3);
    • 𝑐𝑡 = ∃𝑙, 𝑚. ⟨⟨·⟩𝑘 ⟨t ↦→ 𝑙, c ↦→ 𝑚⟩ env ⟩ ∧𝑙 ≥ 0 ∧𝑚 = (ℎ(ℎ + 1) −𝑙 (𝑙 + 1))/2 (the same as formula
       (17)).
   According to algorithm Process, the first iteration of the application of all rules in 𝑅𝑣 to the
configuration patterns in 𝐶𝑟 will derive the following configuration patterns:
         ∃𝑖, 𝑗 . ⟨⟨c=c+t;t=t-1;⟩𝑘 ⟨t ↦→ 𝑖, c ↦→ 𝑗⟩ env ⟩ ∧ 𝑖 > 0 ∧ 𝑗 = (ℎ(ℎ + 1) − 𝑖 (𝑖 + 1))/2                  (34)
and
                       ∃𝑖, 𝑗 . ⟨⟨·⟩𝑘 ⟨t ↦→ 𝑖, c ↦→ 𝑗⟩ env ⟩ ∧ 𝑖 = 0 ∧ 𝑗 = ℎ(ℎ + 1)/2.                            (35)
Both patterns are satisfiable and are added to the set 𝐶𝑟 . A second iteration of rules application will
derive from configuration pattern (34) another pattern:
            ∃𝑖.∃𝑗 . ⟨⟨·⟩𝑘 ⟨t ↦→ 𝑖 − 1, c ↦→ 𝑗 + 𝑖⟩ env ⟩ ∧ 𝑖 > 0 ∧ 𝑗 = (ℎ(ℎ + 1) − 𝑖 (𝑖 + 1))/2.                 (36)
This iteration will reach the fixed point, with 𝐶𝑟 containing configuration patterns (35) and (36).
Both configuration patterns are final, so algorithm Process terminates.
   Then, algorithm Check ensures that both patterns (35) and (36) match pattern 𝑐𝑡 . Configuration
pattern (35) trivially matches 𝑐𝑡 for 𝑙 = 𝑖 ∧ 𝑚 = 𝑗. Configuration pattern (36) matches pattern
𝑐𝑡 for 𝑙 = 𝑖 − 1 and 𝑚 = 𝑗 + 𝑖, since 𝑖 > 0 entails that 𝑖 + 1 > 0, which corresponds to 𝑖 ≥ 0 of
the constraint in 𝑐𝑡 . Then, by substituting 𝑙 and 𝑚 into the second constraint, we obtain 𝑗 + 𝑖 =
(ℎ(ℎ + 1) − 𝑖 (𝑖 − 1))/2. Since from the constraint of pattern (36) 𝑗 = (ℎ(ℎ + 1) − 𝑖 (𝑖 + 1))/2, we
have that (ℎ(ℎ + 1) − 𝑖 (𝑖 + 1))/2 + 𝑖 = (ℎ(ℎ + 1) − 𝑖 (𝑖 − 1))/2. By simplifying the last expression, we
obtain 𝑖 − 𝑖 2 = 𝑖 − 𝑖 2 . Finally, algorithm Check returns true since both checks are successful.

4.2   Semantic evaluation for reachability checking
We now present our semantic procedure, which encodes the approach presented in Section 4.1
using the evaluation of semantic attributes.
  We associate the following attributes to each node in the parse tree:
    • 𝐾, the program fragment underlying the subtree rooted in the node.
    • 𝑅, the set of instances of matching logic reachability rules defining the semantics of the code
      fragment(s) contained in 𝐾, and instantiated for this code. Note that we use the reachability

                                                               , Vol. 1, No. 1, Article . Publication date: June 2026.
:22    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi


 1: function CompAttribute(𝑎 1 , ...𝑎𝑛 )                       15:     res ← Check (𝑣𝑖′ )
 2: 𝐾 ← compose (𝑎 1 .𝐾, . . . , 𝑎𝑛 .𝐾 )                       16:     if res = delay then
 3: 𝑅temp Ð  ← gen(𝐾 )                                         17:        𝑉 ← 𝑉 ∪ 𝑣𝑖′
 4: 𝑅 ← 𝑛𝑖=1Ð𝑎𝑖 .𝑅 ∪ 𝑅temp                                     18:     end if
 5: 𝑉temp Ó  ← 𝑛𝑖=1 𝑎𝑖 .𝑉                                      19:     if res = false then
 6: 𝐶 ← 𝑛𝑖=1 𝑎𝑖 .𝐶                                             20:        𝐶 ← false
 7: if hasContract ( ) then                                    21:     end if
 8:     𝑉temp ← 𝑉temp ∪ genVT (𝑅)                              22: end for
 9: end if                                                     23: if isRootNode () ∧ 𝑉 ≠ ∅ then
10: 𝑉 ← ∅                                                      24:     𝐶 ← false
11: for 𝑣𝑖 ∈ 𝑉temp do                                          25: end if
12:     𝑣𝑖′ ← 𝑣𝑖                                               26: 𝑎 0 ← (𝐾, 𝑅, 𝑉 , 𝐶 )
13:     𝑣𝑖′ .𝑅𝑣 ← 𝑣𝑖′ .𝑅𝑣 ∪ 𝑅temp                              27: return 𝑎 0
14:     𝑣𝑖′ ← Process (𝑣𝑖′ )
                                                               28: end function



                      Fig. 6. The CompAttribute algorithm for semantic attribute evaluation

        rules defined in Section 3 as templates which are instantiated on the actual code of the
        program to be verified.
      • 𝑉 , a set of pending verification tasks.
      • 𝐶, a boolean flag indicating whether the specification can be satisfied, according to the
        information available at the node.
      • Two attributes 𝑆 and 𝐹 to handle struct definitions.
   Our syntax-driven reachability checking procedure computes the attributes of each node in
the parse tree according to algorithm CompAttribute, shown in figure 6. Since attributes are
evaluated during parsing, CompAttribute is called by the parser as it proceeds bottom-up. The
algorithm takes as input the attributes 𝑎 1, . . . , 𝑎𝑛 computed for all the 𝑛 children of the node. Each
𝑎𝑖 is a tuple containing the attributes of a child node. Node attributes are denoted by a dot notation;
e.g., attribute 𝐾 of the first child is 𝑎 1 .𝐾; when clear from the context, we refer to attribute 𝑎𝑖 .𝐾 of
node𝑖 with the shortcut 𝐾𝑖 .
   Attribute 𝐾 is built by suitably composing the children’s 𝐾 attributes (line 2)14 .
   Attribute 𝑅 (lines 3–4) is the union of the children’s 𝑅 attributes and the reachability rules
created for the node using its code (computed by invoking function gen(𝐾)). For the leaf nodes, 𝑅
is obtained by instantiating the reachability rules according to specific templates associated with
each possible production of the grammar.
   Attribute 𝑉 contains the set of verification tasks available in each node. A verification task
⟨𝐶𝑟 , 𝑅𝑣 , 𝑐𝑡 ⟩ is generated as soon as an annotated loop, an annotated function, or the definition of the
main function is encountered: 𝐶𝑟 and 𝑐𝑡 are generated according to the node attribute 𝐾, while 𝑅𝑣
is set to the value of the attribute 𝑅. Since a verification task is instantiated as soon as the definition
of a verification unit is found, some of the required reachability rules may be missing; this situation
will be described below (Section 4.2.1).
   Attribute 𝐶 is initially computed as the conjunction of the corresponding attributes 𝐶 of the
children (line 6), since if one child does not satisfy a verification task, the entire program is incorrect.
If a verification task is not satisfied, attribute 𝐶 is set to false (lines 19–21). If some verification
tasks are still not completed in the root node (lines 23–25), attribute 𝐶 is also set to false.
   We now outline how program verification (in the generalized meaning defined in the context of
matching logic) is performed by exploiting these attributes. Essentially, given a program 𝑃 to verify,
its correctness is determined by the value of attribute 𝐶 of the root node 𝑟 of 𝑃 parse tree. The
14 For the leaves of the parse tree, 𝐾 is directly defined by the corresponding terminal symbol.



, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                                 :23

verification procedure starts by building the parse tree of 𝑃 and then computes the attributes of the
internal nodes in a bottom-up way, until reaching node 𝑟 . However, the application of algorithm
CompAttribute on node 𝑟 requires the value of the attributes 𝑎 1, . . . , 𝑎𝑛 of the children of 𝑟 . Thus,
algorithm CompAttribute has to be recursively applied to the children of the root node, until the
leaves of the parse tree are reached and no further call to CompAttribute is required.
   In other words, program (interpretation and) verification is performed through a bottom-up
attribute evaluation; however, completing these evaluation requires, once the root node is reached,
to execute a second traversal15 of the tree, in a top-down fashion.
   The following two subsections provide some technical details and examples about our syntax-
driven verification approach.
   4.2.1 Syntax-based evaluation of verification tasks. As mentioned above, some of the required
reachability rules may be missing when a verification task is instantiated, since the instantiation
happens as soon as the definition of a verification unit is found. This is illustrated by verification
of the following snippet, which includes function sum from the example in Section 4.1 and its
generalization anySum, which accepts as parameter any integer (not necessarily positive):
      1 int sum(int t)
            DD     E E
                    sum(𝑥 )
          ML




      2                𝑦        ∧ 𝑥 ≥ 0 ∧ 𝑦 = 𝑥 (𝑥 + 1)/2
                            𝑘
      3 {
      4   int c;
      5   c=0;
               ML




      6        ∃𝑖, 𝑗 . ⟨ ⟨while(t>0){c=c+t;t=t-1;}⟩𝑘 ⟨t ↦→ 𝑖, c ↦→ 𝑗 ⟩ env ⟩ ∧ 𝑖 ≥ 0 ∧ 𝑗 = (ℎ (ℎ + 1) − 𝑖 (𝑖 + 1) )/2
      7   while(t>0){
      8     c=c+t;
      9     t=t-1;
     10   }
     11   return c;
     12 }
     13
     14 int anySum(int t)
            DD              E E
               anySum(𝑥 )
          ML




     15             𝑦           ∧ 𝑥 ≥ 0 ∧ 𝑦 = 𝑥 (𝑥 + 1)/2 ∨ 𝑥 < 0 ∧ 𝑦 = 𝑥 (𝑥 − 1)/2
                                𝑘
     16 {
     17   int i;
     18   i = t;
     19   if(i < 0){
     20     i = -i;
     21   }
     22   return sum(i);
     23 }

   A sketch of the parse tree is shown in Figure 7; the definitions of functions sum and anySum are
contained in nodes 1 and 4, respectively, When following a bottom-up parsing strategy, node 4 is
evaluated before node 1. This means that, when the verification task associated with the anySum
function is performed, the definition of function sum is not available. However, to verify anySum, the
semantics of sum (invoked at line 22) is required. In such a situation, we define the verification task
as incomplete. The idea is that access to missing semantic information interrupts the verification
task. The interrupted task is propagated upwards the tree, until the missing information needed to
resume verification becomes available.
15 In the next sections we will show how some optimizations may anticipate the execution of some verification (sub)tasks

already during the construction of the parse tree and the evaluation of its attributes.


                                                                         , Vol. 1, No. 1, Article . Publication date: June 2026.
:24    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

                                                   ○
                                                   1
                                              function_def


                              ○
                              2          ○
                                         3                            ○
                                                                      4
                             type IDENTIFIER                    function_def2


                                                          ○
                                                          5         ○
                                                                    6                  ○
                                                                                       7
                                                    parameter compound_stm        function_def


                                                  Fig. 7. Sample parse tree

1: function CheckNonFinal(𝐶𝑟 )
2: for 𝑐𝑖 ∈ 𝐶𝑟 do
3:     if isNonFinal (𝑐𝑖 ) then
4:        return delay
5:     end if
6: end for
7: return false
8: end function

               Fig. 8. The CheckNonFinal function changed to handle delayed verification tasks


   To deal with delayed verification tasks, we have to modify the Check algorithm in figure 5,
described in Section 4.1. While the original formulation assumed that 𝑅𝑣 contains the complete
semantics, and thus the Process algorithm could complete the execution of the verification task, the
modified version must also handle the case in which 𝑅𝑣 is not sufficient to complete the execution of
the verification task in Process. In this case, a partially-processed verification task can be supported
by having the function Check return a true/false/delay answer. A delay answer indicates that the
semantic information currently available in 𝑅𝑣 is incomplete and does not allow algorithm Process
to complete the verification task. In this case, algorithm Check cannot determine whether the
specification is satisfied or violated. The change to algorithm Check can be accomplished by
modifying the definition of the CheckNonFinal function as shown in figure 8: the function will
now return delay (line 4, which corresponds to line 36 in figure 5) if a non-final configuration is
found.
   To compute attribute 𝑉 , we first collect the incomplete verification tasks from children nodes
and save them in the temporary variable 𝑉temp (line 5 in figure 6). If the current node is annotated
with a specification, we generate a new verification task with function genVT (lines 7–9). We then
update the reachability rules of every verification task, adding the new rules generated in the node
(line 13), and then we execute them through the Process function (line 14). Only the verification
tasks that cannot be fully performed are retained (lines 16–18).
  4.2.2 Example of attributes computation. To exemplify the CompAttribute algorithm, consider
the following simple annotated while loop:
          ML




      1     ∃𝑖, 𝑗 . ⟨ ⟨while(t>0){c=c+t;t=t-1;}⟩𝑘 ⟨t ↦→ 𝑖, c ↦→ 𝑗 ⟩ env ⟩ ∧ 𝑖 ≥ 0 ∧ 𝑗 = (ℎ (ℎ + 1) − 𝑖 (𝑖 + 1) )/2
      2 while(t>0){
      3   c=c+t;
      4   t=t-1;
      5 }

whose parse tree fragment is:


, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                                 :25

                                                         ○
                                                         9
                                                         stm

                                  ○
                                  0            ○
                                               1            ○
                                                            2                   ○
                                                                                8
                             Annotation ‘while’          relat_exp        compound_stm


                                                                       ○
                                                                       3 ○
                                                                         4               ○
                                                                                         7
                                                                       exp    ‘;’        stm


                                                                                      ○
                                                                                      5 ○
                                                                                        6
                                                                                      exp    ‘;’

  The corresponding attributes are:
   • 𝐾2 = {t > 0}, 𝐾3 = {c = c + t}, 𝐾5 = {t = t - 1}, 𝐾7 = {t = t - 1;},
     𝐾8 = {c = c + t; t = t - 1;}, 𝐾9 = {while(t > 0){c = c + t; t = t - 1;}};
   • 𝑅2 = {(37)}, 𝑅7 = {(38)}, 𝑅8 = {(38), (39)}, 𝑅9 = 𝑅2 ∪ 𝑅8 ∪ {(21), (40), (41)};
   • 𝑉2 = 𝑉3 = 𝑉5 = 𝑉7 = 𝑉8 = 𝑉9 = ∅16 ;
   • 𝐶 2 = 𝐶 3 = 𝐶 5 = 𝐶 7 = 𝐶 8 = 𝐶 9 = true;
where the additional reachability rules (37)–(41) are defined below:
                                                       
                                   t > 0
                                              ⟨t ↦→ 𝑖⟩ env ∧ 𝑗 = 𝑖 > 0                                                     (37)
                                     𝑗      𝑘
                                                           
                                   t = t - 1;               𝑖
                                                      t ↦→         ∧ 𝑗 =𝑖 −1                                               (38)
                                        ·           𝑘       𝑗 env
                                                                 
                                   c = c + t;               𝑖
                                                      c ↦→ t ↦→ 𝑙         ∧ 𝑗 = 𝑖 +𝑙                                       (39)
                                        ·           𝑘       𝑗        env
                                                                   
                                   if(𝑏) {c=c+t; t=t-1;}
                                                                ...      ∧𝑏 ≠ 0                                            (40)
                                       c=c+t; t=t-1;
                                                                  𝑘 
                                   if(𝑏) {c=c+t; t=t-1;}
                                                                ...      ∧𝑏 = 0                                            (41)
                                                  ·                  𝑘

5   A COMPLETE EXAMPLE
   In this section we present a complete example of application of our reachability checking
procedure on a sorting program, shown in figure 9, which contains function sort that takes as
input a pointer to a list and returns a pointer to its sorted rearrangement. Function sort invokes
function min, which takes as input a pointer to a list and returns a pointer to a list which is a
permutation of the input list and in which the lowest value is at the beginning of the list. Function
min, in turn, invokes function swap.
   Functions sort and min are annotated with a matching logic specification, while function swap
                                                               ML




is not; the functions and predicates used in the      specifications of Fig. 9 are described in Fig. 10.
The specification of function min (lines 20–21) states that upon execution of the function, the heap
content changes from a list 𝐴 whose first element is pointed to by parameter 𝑖 (as indicated by
the mapping 𝑖 ↦→ list (𝐴) in cell mem) to a new list 𝐴′ , whose first element is pointed by pointer
𝑗 (specified by the mapping 𝑗 ↦→ list (𝐴′ ) in cell mem). List 𝐴′ has the same elements as list 𝐴
16 The verification task set attribute of node 9 would be 𝑉 = { ⟨ {(16)}, 𝑅 , (17)⟩ }. However, notice that the newly generated
                                                           𝑇               9
verification task is completely processed by algorithm Process (line 14) inside the node, since all the necessary reachability
rule instances are available, thus 𝑉9 = ∅.


                                                                         , Vol. 1, No. 1, Article . Publication date: June 2026.
:26    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

       1 #include <stdlib.h>
       2 #include <stdio.h>
       3 struct listNode {
       4 int val;
       5 struct listNode *next;
       6 };
       7 struct listNode* swap(struct listNode* x){
       8 struct listNode* p;
       9 if(x != 0){
      10   if(x->next->val - x->val <0){
      11    p = x->next;
      12    x->next = p->next;
      13    p->next = x;
      14    return p;
      15   }
      16 }
      17 return x;
      18 }
      19 struct listNode* min(struct listNode* x)
             DD            E D                      E E
                min(𝑖)         𝑖↦→list (𝐴)
           ML




      20           j   ...     𝑗 ↦→list (𝐴′ ) . . .
                                      𝑘                    mem
             ∧𝑖 ≠ 0 ∧ 𝑗 ≠ 0 ∧ listPermutation(𝐴, 𝐴′ ) ∧ leq( [head (𝐴′ ) ], 𝐴′ )
           ML




      21
      22 {
      23 if(x->next != 0) {
      24   x->next = min(x->next);
      25 }
      26 return swap(x);
      27 }
      28 struct listNode* sort(struct listNode* x)
             DD             E D                      E E
                sort(𝑖)         𝑖↦→list (𝐴)
                                                         ∧ listPermutation(𝐴, 𝐴′ ) ∧ isSorted (𝐴′ )
           ML




      29           j    ...     𝑗 ↦→list (𝐴′ ) . . .
                                       𝑘                    mem
      30 {
      31 struct listNode* p;
      32 struct listNode* y;
      33 if(x == 0){
      34   return x;
      35 }
      36 y = min(x);
      37 x = y->next;
      38 y->next = 0;
      39 p = y;
           ML ML ML




      40     ∃𝑖, 𝑙, 𝑣, 𝐵, 𝐶.⟨⟨while(x != 0){. . . } . . . ⟩𝑘 ⟨x ↦→ 𝑖, y ↦→ 𝑗, p ↦→ 𝑙 ⟩ env
      41              ⟨ 𝑗 ↦→ lseg (𝑙, 𝐵), 𝑙 ↦→ [𝑣, 0], 𝑖 ↦→ list (𝐶 ) ⟩ mem ⟩
      42     ∧listPermutation(𝐴, 𝐵@[𝑣 ]@𝐶 ) ∧ leq( [𝑣 ], 𝐶 ) ∧ leq(𝐵, [𝑣 ] ) ∧ isSorted (𝐵)
      43 while(x != 0){
      44   p->next = min(x);
      45   p = p->next;
      46   x = p->next;
      47   p->next = 0;
      48 }
      49 return y;
      50 }
                                                                                                ML




                      Fig. 9. List sort example (see Fig. 10 for the functions used in the            specifications )



, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                             :27

    • list (𝐴) creates a heap object for a struct listNode list, containing the elements of the list 𝐴.
    • lseg (𝑖, 𝐴) creates a heap object for a fragment of a struct listNode list, which contains the elements of 𝐴 up to
      (and including) the first one whose next field address is equal to variable 𝑖.
    • listPermutation(𝐴, 𝐵) indicates whether 𝐴 is a permutation of 𝐵.
    • leq(𝐴, 𝐵) indicates whether every element of 𝐴 is less than or equal to every element of 𝐵.
    • [𝑖 ] is a list constructor.
    • head (𝐴) returns the first element of list 𝐴.
    • isSorted (𝐴) indicates whether 𝐴 is sorted.
    • 𝐴@𝐵 represents the list concatenation function.




                                                                                              ML
Fig. 10. Signatures and description of the functions and predicates used in the                    specifications of the
example in Fig. 9; 𝐴 and 𝐵 are lists, 𝑖 is an integer


(specified by the predicate listPermutation(𝐴, 𝐴′ )) and the first element of 𝐴′ is less than or equal
to any other element of 𝐴′ (specified by the predicate leq( [head (𝐴′ )], 𝐴′ )).
   The specification of function sort (line 29) states that upon the invocation of the function, list
𝐴, whose first element is pointed to by parameter 𝑖, is transformed into list 𝐴′ , whose first element
is pointed to by the returned value 𝑗. List 𝐴′ has the same elements as list 𝐴 and it is sorted (as
specified by the predicate isSorted (𝐴′ )). The function works by repeatedly removing the minimum
element from the list pointed to by x, and appending it to the list pointed to by y; this behavior is
specified by the loop invariant at lines 40–42. More precisely, the invariant specifies that:
    • the elements of the list 𝐴 are contained either in the list pointed to by x or in the one
       pointed to by y (as indicated by the mappings in the cell mem (line 41) and by the predicate
       listPermutation(𝐴, 𝐵@[𝑣]@𝐶)), where 𝑣 is the element pointed by p, which is the last element
       of the sorted list segment 𝐵@[𝑣];
    • the list pointed by y is sorted (as indicated by the predicate leq(𝐵, [𝑣]) ∧ isSorted (𝐵));
    • the last element of the list pointed by y is less than or equal to all the elements of the list
       pointed by x (specified by predicate leq( [𝑣], 𝐶)).
   Notice that there is a bug in function swap: field x->next is dereferenced at line 10 without first
performing a NULL pointer check.
   A sketch of the abstract syntax tree of the example is shown in figure 12. For space reasons, we
only describe the application of our approach to function swap; its (simplified) abstract syntax tree
is shown in figure 13, in which the triangle-shaped leaves correspond to subtrees not expanded.
Throughout the example we use the abbreviations for code/environment snippets shown in figure 11.

   𝑚          ≡   𝑎 ↦→ list (𝐴)                                   THEN1     ≡ if(COND){ THEN }
   𝑚′         ≡   𝑎 ↦→ [𝑣, 𝑑 ], 𝑑 ↦→ list (𝐵)                     THEN2     ≡ x->next = min(x->next);
   𝑚 ′′       ≡   𝑎 ↦→ [𝑣, 𝑑 ]                                    OTH       ≡ {x->next = min(x->next);} OTH1
   𝑒0         ≡   x ↦→ (listNode∗, 𝑎)                             OTH1      ≡ return swap(x);
   𝑒          ≡   x ↦→ (listNode∗, 𝑎), p ↦→ undef                 OTH2      ≡ { THEN1} return x;
   𝑝          ≡   𝐴 ≠ nil ∧ 𝑎 ≠ 0 ∧ 𝐴 = [𝑣 ]@𝐵                    OTH3      ≡ - read (x->val)){THEN} return x;
   𝑝′         ≡   𝑝 ∧𝑑 = 0                                        SWAP      ≡ struct listNode* p; if(COND1) OTH2
   COND       ≡   read(read(x->next)->val )-                      MIN       ≡ if(x−>next!=0) OTH
                  read(x->val) < 0                                EM        ≡ ⟨𝑒 ⟩ env ⟨𝑚 ′′ . . . ⟩𝑚𝑒𝑚
   COND1      ≡   x != 0                                          𝑉𝑡 MIN    ≡ ⟨ {(71)}, 𝑅29 , (43)⟩
   ASSIGN     ≡   x->next = read(p->next)
                  ; p->next = x;

                                           Fig. 11. List of abbreviations



                                                                     , Vol. 1, No. 1, Article . Publication date: June 2026.
:28    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

                                                  ○
                                                  1
                                              program


                                                  ○
                                                  2
                                            global_decl

                       ...                 ○
                                           5                                     ○
                                                                                 8
                                    struct_field_list                         global_decl


                               struct listNode definition
                                                                  ...                        ○
                                                                                             9
                                                                                        function_def
                                                                                        (swap definition)
                                                                                              ○
                                                                                              26
                                                                                          function_def2

                                                                        ...            ○
                                                                                       28                         ○
                                                                                                                  29
                                                                                compound_decl                 function_def
                                                                                                              (min definition)

                                                                                  swap body                           ○
                                                                                                                      130
                                                                                                               function_def2

                                                                                                     ...        ○
                                                                                                                132                    ○
                                                                                                                                       133
                                                                                                           compound_stm            function_def


                                                                                                              min body         sort definition



                             Fig. 12. Sketch of the abstract syntax tree of the example in Fig. 9

                                                             ○
                                                             28
                                                    compound_decl




                                  ○
                                  36                                                         ○
                                                                                             43
                               parameter                                           compound_stm



                                           ○
                                           44           ○
                                                        46                             ○
                                                                                       49                                              ○
                                                                                                                                       53
                                   #8      ‘if’    eq_exp                              stm                                             stm



                                                                  ○
                                                                  50             ○
                                                                                 51                    ○
                                                                                                       52
                                                        #9        ‘if’        relat_exp           compound_stm                         #17




                                                                                              ○
                                                                                              87               ○
                                                                                                               94
                                                                                 #10          exp          compound_stm




                                                                                                       ○
                                                                                                       95               ○
                                                                                                                        99
                                                                                              #11      exp      compound_stm




                                                                                                                  ○
                                                                                                                  100        ○
                                                                                                                             101
                                                                                                       #12        exp        stm




                                                                                                                  #13        #14


Fig. 13. Simplified abstract syntax tree of the swap function. Triangle-shaped leaves correspond to subtrees
not expanded; the numbers on them refer to the corresponding line numbers in Fig. 9.




, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                              :29

                            Table 2. Values of the attributes for the example in Fig. 9

            (a) Attributes: 𝐾 (list of code tokens), 𝑅 (set of reachability rules), 𝑉 (set of verification
            tasks), 𝐶 (verification failed flag)
             Node     𝐾                                        𝑅                                𝑉        𝐶
             100      {p->next = x;}                           {(44), (45), (46), (47)}         ∅        true
             101      {return p;}                              {(46), (48)}                     ∅        true
             95       {x->next = read (p->next);}              {(50), (45), (46), (47), (49)}   ∅        true
             87       {p = read (x->next);}                    {(51), (45), (49)}               ∅        true
             99       {p->next = x; return p;}                 {(44), (45), (46), (47), (48)}   ∅        true
             94       𝐾95 𝐾99                                  𝑅95 ∪ 𝑅99                        ∅        true
             52       𝐾87 𝐾94                                  𝑅87 ∪ 𝑅94                        ∅        true
             51       {COND}                                   {(52), (53), (54), (55), (45)}   ∅        true
             49       {if(COND){THEN }}                        {(56), (57)} ∪ 𝑅51 ∪ 𝑅52         ∅        true
             46       {x != 0}                                 {(58), (59), (45)}               ∅        true
                                                                 {(60), (61), (48), (45)}
             43       {if(COND1){THEN1} return x;}                                              ∅        true
                                                                ∪𝑅46 ∪ 𝑅49
             28       {struct listNode* p; 𝐾43 }               {(62)} ∪ 𝑅43                     ∅        true
             9        { (SWAP ) }                              {(63)} ∪ 𝑅28 ∪ 𝑅29               𝑉𝑡 MIN   true
                                                                 {(64), (65), (48), (49),
             132      {MIN }                                                                    ∅        true
                                                                (47), (50) ∪ 𝑅46 }
             29       {}                                       {(66), (67)} ∪ 𝑅132 ∪ 𝑅133       𝑉𝑡 MIN   true

                     (b) Attributes: 𝑁 (description of struct field), 𝑆 (offset of struct
                     field), 𝐹 ( struct fields description)
                       Node     𝑁                    𝑆     𝐹
                       13        (next, listNode∗)   N/A   N/A
                       7                             1     { (next, listNode∗, 0) }
                       6         (val, int )         N/A   N/A
                       5                             2     { (val, int, 0), (next, listNode∗, 1) }




5.1   Attribute evaluation
The final values of all the attributes at the end of their evaluation and the reachability rules
referenced by them are reported, respectively, in table 2 and in table 3 whereas the details of the
step are explained in Appendix A.4, node by node. Here we only illustrate the generation of the
verification task for function min which is the core of the attribute of the corresponding subtree.

   Node 29 (figure 12): verification task generation. The specification of function min (lines 20–21) is
translated into the initial configuration pattern (42):

                     ∃𝑎. ⟨⟨MIN ⟩𝑘 ⟨x ↦→ (listNode∗, 𝑎)⟩ env ⟨𝑎 ↦→ list (𝐴)⟩𝑚𝑒𝑚 ⟩ ∧ 𝑝                                    (42)

and target configuration pattern (43):

           ∃𝑎 ′ . ⟨⟨a′ ⟩𝑘 ⟨𝑎 ′ ↦→ list (𝐴′ )⟩𝑚𝑒𝑚 ⟩ ∧ listPermutation(𝐴, 𝐴′ ) ∧ leq(head (𝐴′ ), 𝐴′ ).                    (43)

  The corresponding verification task, vt 29 = ⟨{(42)}, 𝑅29, (43)⟩, is produced in node 29 by function
genVT of the CompAttribute procedure (figure 6, line 8).

                                                                      , Vol. 1, No. 1, Article . Publication date: June 2026.
:30    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

                                             Table 3. Reachability rule instances


                            Node       Reachability rule
                                       DD                          E E
                                            p->next=𝑖;
                             100          write (p->next,𝑖 ) . . .                                        (44)
                                                                         𝑘
                                       DD                   E                                         E
                                                x
                             100            (typeX,𝑖 ) . . . 𝑘 ⟨x ↦→ (typeX, 𝑖) . . . ⟩ env               (45)
                                       DD                   E                                         E
                                                p
                             100            (typeP,𝑖 ) . . . 𝑘 ⟨p ↦→ (typeP, 𝑖) . . . ⟩ env               (46)
                                       DD                   E D              E                E
                                            write (𝑖,𝑗 )
                             100                 ·       ...   𝑖 ↦→ ℎ𝑗 . . .                              (47)
                                                             𝑘                      𝑚𝑒𝑚
                                       DD                           E E
                                            return (t,𝑖 );
                             101                (t,𝑖 )     ...                                            (48)
                                                               𝑘
                                       DD                       E                             E
                                            read ( (𝑡,𝑖 ) )
                              95               (𝑡,𝑗 )       . . . ⟨𝑖 ↦→ 𝑗 . . . ⟩𝑚𝑒𝑚                      (49)
                                                                 𝑘
                                       DD                              E E
                                              x->next=𝑖;
                              95            write (x->next,𝑖 ) . . . 𝑘                                    (50)
                                       DD                 E D                           E         E
                                            p=(𝑡,𝑖 );
                              87               ·      ...           p ↦→ (𝑠,𝑗 )
                                                                         (𝑠,𝑖 ) . . .                     (51)
                                                          𝑘                                 env
                                       DD           E E
                                            𝑖-𝑗
                              51             𝑙 ... 𝑘      ∧𝑙 = 𝑖 − 𝑗                                      (52)
                                       DD           E E
                                            𝑖<𝑗
                              51             𝑙 ... 𝑘      ∧𝑖 < 𝑗 ∧𝑙 ≠ 0                                   (53)
                                       DD           E E
                                            𝑖<𝑗
                              51             𝑙 ... 𝑘      ∧𝑖 ≥ 𝑗 ∧𝑙 = 0                                   (54)

                                            0
                              51            𝑖 ... 𝑘     ∧𝑖 = 0                                            (55)
                                       DD                           E E
                                            if(𝑖){THEN }
                              49                THEN     ...              ∧𝑖 ≠ 0                          (56)
                                                             𝑘
                                       DD                           E E
                                            if(𝑖){THEN }
                              49                  ·      ...              ∧𝑖 = 0                          (57)
                                                             𝑘
                                       DD             E E
                                            𝑖!=𝑗
                              46              𝑙 ... 𝑘       ∧𝑖 ≠ 𝑗 ∧𝑙 ≠ 0                                 (58)
                                       DD             E E
                                            𝑖!=𝑗
                              46              𝑙 ... 𝑘       ∧𝑖 = 𝑗 ∧𝑙 = 0                                 (59)
                                       DD                           E E
                                            if(𝑖){THEN1}
                              43              𝑇 𝐻 𝐸𝑁 1   ...              ∧𝑖 ≠ 0                          (60)
                                                             𝑘




, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                                    :31

                              Table 3 (Continued). Reachability rule instances


           Node   Reachability rule
                  DD                  E E
                     if(𝑖){THEN1}
            43             ·      ...     ∧𝑖 = 0                                                              (61)
                                           𝑘
                  DD                                 E D                                E    E
                       struct listNode* p;                            ·
            28                  ·          ...             p↦→ (listNode∗,undef) . . . env                    (62)
                                               𝑘
                  DD                            E                       E
                       swap((listNode∗,𝑖 ))             ·
             9               SWAP           ...       x↦→𝑖 . . . env                                          (63)
                                                𝑘
                  DD                      E E
                       if(𝑖){THEN2}
           132             THEN2    ...            ∧𝑖 ≠ 0                                                     (64)
                                        𝑘
                  DD                      E E
                       if(𝑖){THEN2}
           132               ·      ...            ∧𝑖 = 0                                                     (65)
                                        𝑘
                    DD                             E D              E         D              E     E
                         min((listNode∗,𝑖 )) 𝑖↦→list (𝐴)            𝑖
            29                    j          𝑗↦→list (𝐴′ ) 𝑚𝑒𝑚 x ↦→ 𝑗 . . . env
                                             ...
                                                 𝑘                                                            (66)
                    ∧𝑖 ≠ 0 ∧ 𝑗 ≠ 0 ∧ listPermutation(𝐴, 𝐴′ ) ∧ leq(head (𝐴′ ), 𝐴′ )
                  DD                           E                     E
                       min((listNode∗,𝑖 ))           x↦→𝑖
            29              ERROR          ...         · . . . env       ∧𝑖 = 0                               (67)
                                               𝑘
                  DD                           E E
                       (listNode∗,𝑖 )->val
             2                  𝑖          ...                                                                (68)
                                               𝑘
                  DD                            E E
                       (listNode∗,𝑖 )->next
             2              (listNode∗,𝑗 )  ...       ∧ 𝑗 =𝑖 +1                                               (69)
                                                𝑘
                  DD                                     E E
                       sizeof(struct listNode)
             2                    2            ...                                                            (70)
                                                   𝑘




5.2   Symbolic evaluation
We illustrate the evaluation of the verification task for function min, as executed through the
Process and Check algorithms shown in figure 5. The evaluation of the verification task starts
at node 29 with configuration pattern (42), which captures the state in which min is invoked: x
points to a non-empty list 𝐴. The configuration patterns reached through the symbolic execution
are shown in table 4.
   The first operation is the replacement of variable x with its value 𝑎 by reachability rule in-
stance (45), which yields configuration pattern (71). The evaluation of the task in node 29 must
stop here, since no further rule instances are available to process this configuration pattern: the
Process algorithm exits from the loop and returns. Since configuration pattern (71) is non-final,
the execution of the Check algorithm will return a delay answer, terminating the Check algorithm;
the verification task will be resumed in node 2.
   Figure 14 depicts the remaining steps in the symbolic execution: nodes represent the traversed
configuration patterns, while edges are labeled with the applied reachability rule instances.

                                                                            , Vol. 1, No. 1, Article . Publication date: June 2026.
:32    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

      Table 4. Configuration patterns reached through the symbolic execution of the example in Fig. 9


      ∃𝑎. ⟨⟨if(read ((listNode∗, 𝑎)->next)!=NULL)OTH ⟩𝑘 ⟨𝑒 0 ⟩ env ⟨𝑚 . . . ⟩𝑚𝑒𝑚 ⟩ ∧ 𝑝                              (71)

      ∃𝑎, 𝑣, 𝑑, 𝐵. ⟨⟨if((listNode∗, 𝑑)!=0)OTH ⟩𝑘 ⟨𝑒 0 ⟩ env ⟨𝑚 ′ . . . ⟩𝑚𝑒𝑚 ⟩ ∧ 𝑝                                   (72)

      ∃𝑎, 𝑣, 𝑑, 𝐵. ⟨⟨return swap(x);⟩𝑘 ⟨𝑒 0 ⟩ env ⟨𝑚 ′′ . . . ⟩𝑚𝑒𝑚 ⟩ ∧ 𝑝 ′                                          (73)

      ∃𝑎, 𝑣, 𝑑, 𝐵. ⟨⟨return (if(COND1) OTH2)⟩𝑘 ⟨𝑒⟩ env ⟨𝑚 ′′ . . . ⟩𝑚𝑒𝑚 ⟩ ∧ 𝑝 ′                                     (74)

      ∃𝑎, 𝑣, 𝑑, 𝑓 , 𝐵. ⟨return (if(𝑓 )OTH2)⟩𝑘 ⟨𝑒⟩ env ⟨𝑚 ′′ . . . ⟩𝑚𝑒𝑚 ∧ 𝑝 ′ ∧ 𝑓 = 1                                (75)

      ∃𝑎, 𝑣, 𝑑, 𝑔, 𝐵. ⟨⟨return (if(read ((listNode∗, 𝑑)->val)OTH3⟩𝑘 EM⟩ ∧ 𝑝 ′ ∧ 𝑔 = 𝑎 + 1                           (76)

      ∃𝑎, 𝑣, 𝑑, 𝑟, 𝐵. ⟨⟨return (if(read (𝑟 )OTH3⟩𝑘 EM⟩ ∧ 𝑝 ′ ∧ 𝑟 = 0                                                (77)




                                               ...
                     (69),(49)          (58)

             (71)                (72)           (45),(63),(62)                 (61),(45),(69),(49)

                                        (59)   (73)          (74)            (75)            (76)            (77)

                                                                                                     (68)
                                                                      (45),(59)

Fig. 14. Steps of the symbolic execution for the example in Fig. 9 (nodes are labeled with the configuration
patterns from Table 4, edges are labeled with the reachability rule instances from Table 3)


   First reachability rule instance (69) is applied and the address of next field is computed. Then,
reachability rule instance (49) reads the value of next field, reaching configuration pattern (72)17 .
At this stage, both reachability rule instances (58) and (59) could be applied; we only consider the
case where rule instance (59) is applied, corresponding to the execution of line 26 in Fig. 9.
   To execute the call to function swap, first the value of x is retrieved through reachability rule
instance (45); the actual function call is performed by applying reachability rule instance (63). The
first statement of function swap defines variable p. Reachability rule instance (62) executes this
statement and yields configuration pattern (74). To execute the outer if statement of function
swap, variable x is evaluated by reachability rule instance (45); reachability rule instance (59) is
applied, resulting in configuration pattern (75) 18 . The then branch of the if statement is not
entered through reachability rule instance (61); hence, the inner if of function swap is reached.
Variable x is evaluated through reachability rule instance (45); then, the actual address of the
17 Note that the list object 𝐴 in mem is split into a first object [𝑣 ] containing the first element and a second list object 𝐵

containing the tail of list 𝐴.
18 In this case reachability rule instance (58) cannot be applied, meaning that the then branch cannot be followed.



, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                              :33

                                              ○
                                              228
                                        log_and_exp


                        ○
                        46     ○
                               229                                       ○
                                                                         230
                      eq_exp ‘&&’                                    eq_exp

                                                    ○
                                                    231                        ○
                                                                               236       ○
                                                                                         237
                                               postfix_exp                     ‘!=’ postfix_exp

                                         ○
                                         232                 ○
                                                             233                         ○
                                                                                         238
                                     IDENTIFIER       postfix_exp1                    Constant

                                                      ○
                                                      234          ○
                                                                   235
                                          x          ‘->’ IDENTIFIER                      0



                                                                   next

                  Fig. 15. Subtree affected by the change at line 9 of the example in Fig. 9


next field is obtained through reachability rule instance (69); the memory read is then performed
through reachability rule instance (49). Starting from configuration pattern (76), reachability rule
instance (68) computes the val offset, yielding configuration pattern (77). In this state, the memory
read cannot be performed, since the address to be read is zero. The sink error configuration is
reached and the verification must stop. Since no further configuration patterns are reachable from
the sink error configuration, algorithm Process exits, returning the performed verification task.
   A subsequent invocation of the Check algorithm on the returned verification task would yield
false: indeed, algorithm Check would report the verification failure, since all sink error configura-
tions are final and do not match the target configuration.

6     INCREMENTAL REACHABILITY CHECKING
Our approach for reachability checking is intrinsically incremental because:
      • it is syntactically incremental, since it assumes that the input program is described by means
        of an operator precedence grammar, which allows for limiting the parsing process only to a
        fraction of the input, thanks to its peculiar properties described in Section 2.1;
      • our semantic attribute evaluation method relies only on synthesized attributes, meaning
        that the semantics of a certain node depends only on its descendants. Upon changes of the
        semantic attributes of the nodes in a subtree, it suffices to recompute the attributes of the
        ancestors along the path to the root.
   This can lead to an incremental verification procedure once verification is encoded as syntax-
directed attribute evaluation.
   In the remaining of the section we show an application of incremental verification to the example
presented in Section 5 and also discuss how to speed up the incremental evaluation process.

6.1    Incremental Verification: Application to the Example
We consider a change occurring at line 9 of the sort program shown in (figure 9), which replaces
the original (and faulty) condition x!=0 with x!=0 && x->next!=0; figure 15 shows the portion of
the syntax tree enclosing the change.

                                                                      , Vol. 1, No. 1, Article . Publication date: June 2026.
:34    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

                                                                 ○ 1
                                                                program




                                                                       ...
                                                                ○
                                                                227
                                                            compound_stm
                                               ○
                                               44
                                                                   ○228
                                                                                   ○ 53
                                               ‘if’ . . .                     . . . stm
                                                                log_and_exp



                                                       if(. . .){. . .}return x;


                 Fig. 16. Part of the syntax tree of the example in Fig. 9 affected by the change


                           COND2        ≡ x != 0 && read (x->next)!= 0
                           SWAP ′       ≡ struct listNode* p; if(COND2) OTH2

                     Fig. 17. New abbreviations (in addition to the ones introduced in Fig. 11)


  6.1.1 Incremental attribute evaluation. The change requires re-evaluating the semantic attributes
as shown in figure 16. The changed part (bounded by nodes 44 and 53) is the subtree rooted in
node 227: only the attributes of this subtree must be recomputed and it is enough to propagate
these attributes through the path to the root of the tree (node 1). This way the attributes of other
nodes (e.g., node 29 in Figure 12) do not need to be evaluated.
  The newly computed attributes and reachability rule instances are shown in table 5. Notice the
use of the abbreviations defined in figure 17, in addition to those defined in figure 11.
   6.1.2 Incremental symbolic execution. We analyze the symbolic execution of the min verification
task after the change; for brevity, we only consider the part of the verification task analyzed in
Section 5.2.
   The execution proceeds as described in Section 5.2 until reaching configuration pattern (73) (see
table 4); the configuration patterns reached during the evaluation of the verification task are shown
in table 5. From configuration pattern (73), the execution continues as depicted in figure 18 (nodes
represent the traversed configuration patterns; edges are labeled with the applied reachability rule
instances). Configuration pattern (81) is obtained from configuration pattern (73) by executing the
new swap function through reachability rules (80) and by defining variable p through (62). Then,
the first condition of the outer if statement is executed through reachability rule instances (45)
and (59), yielding configuration pattern (82). At this point, the execution of the program is affected
by the change, reflected in the second condition of the if. Reachability rule instances (79), (45),
(69), and (49) retrieve the values required by the expression, reaching configuration pattern (83). In
this case, the then branch cannot be taken, since the condition evaluates to false (because 𝑑 = 0);
the execution of the false branch yields configuration pattern (84), through reachability rule
instance (61). The value to be returned is retrieved through rules (45) and (48) (the latter executed
twice) reaching the final configuration pattern (85). The invocation of algorithm Check checks
whether pattern (85) matches the target configuration pattern (43). Logical variable 𝑎 in pattern (85)
is equal to 𝑎 ′ in pattern (43); 𝐴 and 𝐴′ are equal, i.e., they contain the same elements; since 𝐴

, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                                          :35

Table 5. Values of the attributes, reachability rule instances, and configuration patterns resulting from the
change at line 9 of the example in Fig. 9

              (a) Attributes: 𝐾 (list of code tokens), 𝑅 (set of reachability rules), 𝑉 (set of
              verification tasks), 𝐶 (verification failed flag)
                Node       𝐾                                               𝑅                               𝑉     𝐶
                 230       {read (x->next) != 0}                           {(58), (59), (45), (49)}        ∅     true
                 228       {x!=0 && read (x->next)!=0}                     𝑅230 ∪ 𝑅46 ∪ {(78), (79)}       ∅     true
                                                                             {(60), (61), (48), (45)}
                 227           {if(𝐾228 ){THEN1}return x;}                                                 ∅     true
                                                                            ∪𝑅228 ∪ 𝑅49
                  28       {struct listNode* p; 𝐾227 }                     {(62)} ∪ 𝑅227                   ∅     true
                  9        {SWAP }                                         {(80)} ∪ 𝑅28 ∪ 𝑅29              𝑉29   true
                  2        {}                                              {(68), (69), (70)} ∪ 𝑅9         ∅     true

                                                (b) Reachability rule instances
                                  Node     Reachability rule
                                           DD                                   E E
                                                𝑖 && read (x->next) != 0
                                   228                      𝑖            ...          ∧𝑖 = 0        (78)
                                                                             𝑘

                                           DD                                   E E
                                                𝑖 && read (x->next) != 0
                                   228             read (x->next) != 0   ...          ∧𝑖 ≠ 0        (79)
                                                                             𝑘

                                           DD                          E                        E
                                                swap((listNode∗,𝑖 ))             ·
                                    9                SWAP ′          ...       x↦→𝑖 . . . env       (80)
                                                                         𝑘




                                                  (c) Configuration patterns
            Configuration pattern
            ∃𝑎, 𝑣, 𝑑, 𝐵.   return (if(COND2 ) OTH2) 𝑘 ⟨𝑒 ⟩ env ⟨𝑚 ′′ . . . ⟩𝑚𝑒𝑚 ∧ 𝑝 ′                                   (81)


            ∃𝑎, 𝑣, 𝑑, 𝑓 , 𝐵. ⟨return (if(𝑓 AND)OTH2) ⟩𝑘 ⟨𝑒 ⟩ env ⟨𝑚 ′′ . . . ⟩𝑚𝑒𝑚 ∧ 𝑝 ′ ∧ 𝑓 = 1                         (82)


            ∃𝑎, 𝑣, 𝑑, 𝐵. ⟨ ⟨return (if((listNode∗, 𝑑 ) != 0 )OTH2) ⟩𝑘 ⟨𝑒 ⟩ env ⟨𝑚 ′′ . . . ⟩𝑚𝑒𝑚 ⟩ ∧ 𝑝 ′                 (83)


            ∃𝑎, 𝑣, 𝑑, 𝐵. ⟨ ⟨return (return x;) ⟩𝑘 ⟨𝑒 ⟩ env ⟨𝑚 ′′ . . . ⟩𝑚𝑒𝑚 ⟩ ∧ 𝑝 ′                                     (84)


            ∃𝑎, 𝑣, 𝑑, 𝐵. ⟨ ⟨ (listNode∗, 𝑎) ⟩𝑘 ⟨𝑒 ⟩ env ⟨𝑚 ′′ . . . ⟩𝑚𝑒𝑚 ⟩ ∧ 𝑝 ′                                        (85)




contains only one element, the expression 𝑣, leq(head (𝐴′ ), 𝐴′ ) is equivalent to 𝑣 ≤ 𝑣, and evaluates
to true.

6.2   Improving performance of incremental evaluation
The technique described above allows for efficiently re-evaluating only the nodes affected by the
changes. The speed-up that can be achieved depends on the distribution of the computational
effort along the syntactic tree, since the nodes close to the root of the tree are those re-evaluated
more often. Furthermore, most of the computational time is spent inside the verification tasks,

                                                                                  , Vol. 1, No. 1, Article . Publication date: June 2026.
:36    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

          (45),(59)                     (79),(45),(69),(49)           (61)             (45),(48),(48)
   (81)                     (82)                               (83)             (84)                    (85)


Fig. 18. Steps of the symbolic execution for the example in Fig. 9 modified with the change at line 9 (nodes
are labeled with the configuration patterns from Tables 4 and 5, edges are labeled with the reachability rule
instances from Tables 3 and 5)


whose evaluation can be started only in nodes containing a loop invariant or a function definition
(the latter are close to the root). When function definitions or loop invariants are missing, the
verification tasks can be started even closer to the root, if not at the root at all.
   Performance can be improved by making rule propagation along the tree more efficient, balancing
the distribution of the computation efforts. Within each node, instead of simply copying the semantic
rules of the children, we generate intermediate state transitions that summarize the behavior of the
program fragment contained in the node subtree. These intermediate state transitions are obtained
by collapsing the reachability rules propagated from the children nodes. The generation starts with
expanding the program code related to the node into a symbolic configuration pattern, from which
the traditional verification procedure can be applied. When a final configuration pattern is reached,
the relation between the final and the initial patterns is used to generate a new reachability rule
that summarizes the execution.
   To illustrate this optimization, consider the previous example referring to the symbolic inter-
pretation attached to node 227 (see Figure 16): instead of considering the sequence of reachability
rules (45), (59), (79), (45), (69) as in Figure 18, the generation starts from the code part of node 227
belonging to configuration pattern (81), and first yields configuration pattern (86):
                                                 ⟨⟨if(COND2) OTH2⟩𝑘 ⟩                                     (86)
When the new reachability rules are generated, the initial configuration is not fully known. This
incomplete knowledge may make the verification procedure unfeasible; for example, it could be
impossible to evaluate the loop termination conditions within the appropriate execution context.
Therefore, when loops or function calls occur, the generation process ought to be suspended to
prevent indefinite looping; instead, we do execute loops but we restrict their execution to only one
iteration and we allow functions to be called only once, forbidding further iterations (respectively,
calls) inside the same loop (respectively, function). This way, we are still able to improve the
individual execution of a loop or a function; this improvement will be later on reflected on the
execution of the loop/function in the appropriate context.
    Another case of incomplete knowledge is the access to a variable which has not been declared
(i.e., a variable whose declaration lies in another part of the program). In this case it is sufficient to
add the missing variable to the initial patterns. Continuing the example above, the application of
reachability rule (45) to configuration pattern (86) yields configuration pattern 87:
                                     ∃𝑡 . ⟨⟨if(COND2) OTH2⟩𝑘 ⟨x ↦→ 𝑡, . . . ⟩ env ⟩                       (87)
However, there is no variable x in the env cell. Thus, we add a symbolic variable x and continue
the generation process from configuration pattern (87) by propagating the logical constraints as
shown below:
                   ∃𝑡 . ⟨⟨if(read ((listNode∗, 𝑡 + 1))!=0) OTH2⟩𝑘 ⟨x ↦→ 𝑡, . . . ⟩ env ⟩ ∧ 𝑡 ≠ 0          (88)

                                ∃𝑡, 𝑢. ⟨⟨if(𝑢) OTH2⟩𝑘 ⟨x ↦→ 𝑡⟩ env ⟩ ∧ 𝑡 = 0 ∧ 𝑢 = 0                      (89)

, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                     :37

                                                 (90),(49)
                                        (81)                   (83)


Fig. 19. Excerpt of the reduced symbolic execution for the example in Fig. 9 modified with the change at
line 9 (nodes are labeled with the configuration patterns from Tables 4 and 5, edges are labeled with the
reachability rule instances from Tables 3 and 5)


   Let us assume that symbolic execution stops upon reaching configuration patterns (88) and (89).
In this case the available information does not allow us to conclude whether x is always different
from zero; we have to generate two different configuration patterns, covering both cases. These
configuration patterns, paired with the initial pattern (87) produce reachability rules (90) and (91):
                                                                           
                                  COND2
                                                    . . . ⟨x ↦→ 𝑡, . . . ⟩ env ∧ 𝑡 ≠ 0            (90)
                       read ((listNode∗, 𝑡 + 1))!=0        𝑘
                                                            
                               COND2
                                     . . . ⟨x ↦→ 𝑡, . . . ⟩ env ∧ 𝑡 = 0 ∧ 𝑢 = 0                                (91)
                                 𝑢          𝑘
As a result of this optimization (not fully explained here for space reasons), the original fragment
from pattern (81) to (83) of the path depicted in Figure 18 is replaced by the one in Figure 19, where
the single rule (90) replaces the sequence (45), (59), (79), (45), (69). Since the verification of every
reachability rule requires one or more calls to the SMT solver, we can expect a gain proportional to
the reduction of the number of reachability rules.
   Another performance improvement can be obtained by exploiting the natural parallelism enabled
by the local parsability property and the use of synthesized attributes, as already hinted in Section 2.1.
Parallelism may come in various forms: several computations are launched in different fragments of
the source code; the corresponding syntactic subtrees are built in parallel and in conjunction with
semantic attributes evaluation; when some verification tasks are ready, instances of the constraint
solver are launched in parallel.
   The two optimization techniques described above aim at increasing the overall efficiency of the
whole verification process, both when carried on from scratch and when performed incrementally.
In the latter case, however, their benefits are amplified:
    • Collapsing several symbolic interpretation steps (and therefore decreasing the calls to the
      solver) may positively impact not only the analysis of the portion of syntax tree modified by
      the change, but also the unavoidable verification that is replayed identically when revisiting
      some nodes close to the root.
    • Exploiting the intrinsic parallelism enabled by the local parsability property and the bottom-
      up attribute evaluation schema not only improves the performance of the global evaluation
      but also allows for managing multiple changes in a natural way.

7   IMPLEMENTATION AND EVALUATION
We implemented our approach in a prototype tool, called SCMatchC (SiDECAR Matching logic
verifier).
   In this section we evaluate our tool along two dimensions. First we show that the harness needed
to support incremental verification does not significantly alter the performance of non-incremental
verification. We then investigate how different aspects of the program being verified (e.g., presence
and type of annotations, size of the original program and of its modified version, size, position, and

                                                             , Vol. 1, No. 1, Article . Publication date: June 2026.
:38    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi


         SiDECAR Matching logic verifier




                   KernelC                 Verification task    verification          Verification
                   Parser                     Generator            tasks                Engine
                                    ast                                                                 formula
                                                                                           Constraint                Z3
                  SiDECAR                                                                   Handler                 Solver
                                           Reachability rules   reachability                            sat/unsat
                                              Generator            rules




               Annotated                                                       Counterexample
               Input                                                           or proof
               Program




                                            Fig. 20. The architecture of SCMatchC


type of changes) affect the benefits of our approach for incremental verification. More specifically,
we evaluate our approach by answering the following research questions:
RQ1: What is the overhead introduced by the machinery needed to support our syntax-based incre-
      mental verification approach when compared with non-incremental tools for the verification of
      matching logic properties in non-incremental settings?
RQ2: How effective is the incremental speedup provided by our approach and which major factors
      influence it?

7.1    Implementation and Experimental Settings
SCMatchC is developed in Scala 2.11.6 and Java 8 and is rooted in SiDECAR, our general framework
for implementing syntax-based incremental verification procedures [5].
   The architecture of SCMatchC is shown in figure 20. SCMatchC takes as input the KernelC
program to be verified, possibly annotated with matching logic specifications. The input program
is parsed by an incremental KernelC operator-precedence parser built on top of SiDECAR. The
resulting abstract syntax tree is processed by two generator components, which generate the
reachability rule instances describing the semantics of the program, as well as the verification tasks;
these generators work according to the CompAttribute algorithm described in section 4 (figure 6).
The verification tasks are then performed by the Verification Engine, which also takes as input the
reachability rule instances; this engine implements the Process and Check algorithms (figure 5).
During the verification process, the reachability of configurations is checked by querying an external
SMT solver (Z3 [19]); the Constraint Handler component translates configuration patterns into SMT
formulae. The SMT solver is also used to check whether the final configuration pattern satisfies the
verification task contract. We chose the Z3 solver because it is a fairly well-known, widely adopted
and available tool; notice, however, that it is an "external black box" in our architecture, so that it
could be easily replaced by, or integrated with, other possible solvers with complementary features.

  The experiments are conducted on a Docker container run on a machine equipped with an Intel
Core i5 3.2 GHz processor, 32 GB memory, running a 64 Bit GNU/Linux OS distribution. We use
MatchC revision 56519 and Z3 version 4.4. The execution times reported in the following sections
are the average over 5 executions, which we deemed as enough to produce fairly stable average
values. Due to the warm-up of the Docker containers involved, the results of the first run of the
experiments in a session have been discarded. We also point out that the parallel execution features
19 Taken from https://code.google.com/archive/p/matching-logic/source/default/commits.



, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                     :39

                                         Table 6. Benchmarks used


                Name        Number of programs   LOCs per program       Tokens per program
                 MB1        29                   6–56                   12–269
                 MB2        228                  6–10                   12–269
                 MB3        201                  54                     276
                 MB4        201                  60                     316
                 MB5        42                   180                    961–975
                 MB6        5                    434–450                2675–2808


available in the tool (see Section 6.2) have been purposely disabled to obtain data that depend
exclusively on incrementality, even at the expenses of some loss in terms of absolute performance;
we will comment on the further benefits that can be obtained by combining incrementality with
parallelism in the conclusions (Section 9).

7.2    Benchmarks and Evaluation Settings
We built a suite of six benchmarks to evaluate SCMatchC, each of them containing various KernelC
programs and modified versions; Table 6 indicates, for each benchmark, the number of programs,
the number of lines of code (LOC) and the number of tokens per program.
   MB1 contains four groups of sample programs (“undefined”, “simple”, “list”, “sorting”) taken
from the original MatchC benchmark.
   MB2 has been built starting from the seven programs of the “simple” group from benchmark
MB1. For each program, we generated mutations according to an operator mutation schema and
pruned those that could not be verified (i.e., those with the non-linear constraints not supported by
the current SMT solver).
   MB3 contains artificially created programs, obtained by concatenating different programs from
benchmarks MB1 and MB2. More precisely, each program in MB3 is the textual concatenation of the
seven programs from benchmark MB1 used for generating benchmark MB2, where six programs
are the original version from MB1 and the seventh is one of the corresponding mutations contained
in MB2. This benchmark was created to compensate for the relatively small size of the programs
in benchmark MB2, so that the size of the modified part of each program in MB2 is a significant
fraction of the whole code.
   MB4 is obtained by artificially adding to a each program of MB3 a new function that calls all the
functions contained in the program. This way a semantic dependency is introduced between the
different functions and the incremental approach is more stressed, since it is not possible to reason
anymore on different modules separately. Furthermore, by controlling the position of the newly
inserted function, this benchmark allows us to correlate the performance of our approach with the
characteristics of the changes.
   MB5 contains programs derived from the well known Siemens collection20 . We chose the TCAS
benchmark because it contains programs from a safety-critical domain (avionics) where the pro-
gramming style is based on the typical features of KernelC. This benchmark has been widely used
in the literature; e.g., [7, 8, 10, 35]. We slightly adapted it to replace the C language features not
supported by KernelC, i.e., global variables, for loops, and static arrays. Each program in the
Siemens collection comes with several versions; for some programs, some versions have multiple
changes in different locations. Although SCMatchC can handle multiple changes, we chose to
20 Available at http://sir.unl.edu/.



                                                             , Vol. 1, No. 1, Article . Publication date: June 2026.
:40       Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

modify these versions so that any change affects only a single point of the original program;
hence the effect of each individual change can be analyzed independently. This benchmark was
selected to evaluate our approach when dealing with real-world changes generated in an industrial
environment. Furthermore the programs in this benchmark are significantly larger than those in
the previous benchmarks; hence this benchmark can assess the scalability of our approach with
respect to the size of the program.
   MB6 contains five versions of a program manipulating red-black trees, inspired by classic
algorithms as those presented in [15], with additional functions for testing purpose. Besides the
base version, we created two new versions. In the first version, we unified the functions performing
the left and right tree rotations into a single function with a parameter that specifies the rotation to
be applied. In the second version, we modified a function that extracts the minimum element of a
subtree, by using recursion instead of a while-loop. During the development of these new versions,
we unintentionally introduced a few errors in the code: two versions containing a bug were also
added to the benchmark.
This benchmark addresses yet another dimension to our empirical assessment: it stresses the
effects of incrementality when changes are applied to fairly sophisticated algorithms. Indeed, the
algorithms to manage red-black trees are cleverly designed and rather complex; moreover, their
functions use heap objects extensively.
   Benchmark MB1 is the only one used for answering RQ1, while benchmarks MB2–MB6 are used
for answering RQ2. Another major distinguishing feature among the various benchmarks concerns
the use of annotations. MB1–MB4, being derived from the original MatchC benchmark, contain
programs annotated with matching logic specifications in the classical Hoare style: functions’
semantics is specified by pre- and postconditions and loops are annotated with invariants. Instead,
MB5 and MB6 did not contain annotations, in the original repositories where they have been found.
We added, however, a few annotations in the form of debugging assertions, to check correctness of
the state at selected critical points. Thus, for MB1–MB4, program verification amounts to proving or
disproving that the program execution guarantees satisfying the program’s postcondition; whereas,
in case of MB5 and MB6, the tool considers the program as correct iff its execution does not violate
the intermediate assertions (see also the discussion at the beginning of Section 4.1.)

7.3       Non-incremental verification: comparison between SCMatchC and MatchC
To answer RQ1, we executed SCMatchC on benchmark MB1 in a non-incremental setting, i.e.,
performing the verification from scratch. We compared our execution time with MatchC [16],
the state-of-the-art tool for the verification of KernelC programs annotated with matching logic
specifications. The results are shown in Table 721 .
    The results show that in most cases SCMatchC performs similarly to, and in some cases better
than, MatchC. We further investigated the cases in which SCMatchC is slower than MatchC
(i.e., 7 comm_assoc_1_0.c, 13 filter_3_0.c, and the five programs of the sorting group): we
notice that a large amount of the execution time is spent in constraint solving (indicated in column
SCMatchC Solver). Indeed, the type of constraints generated for these programs can be solved more
easily through a rewrite-based approach, as in MatchC with Maude, than through an SMT solver,
as in SCMatchC.
    The answer to RQ1 is that in the majority of the cases the overhead introduced by the machinery
to support our syntax-based incremental approach is negligible, yielding execution times for
verification comparable to a state-of-the-art non-incremental approach. However, for programs

21 Some preliminary results of a comparison between a previous version of our tool and MatchC were published earlier

in [6].


, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                          :41

Table 7. Comparison of the execution time of SCMatchC and MatchC on benchmark MB1 (Column “Ratio”
is the ratio between the execution time of SCMatchC and the one of MatchC)

                                                                    SCMatchC
      Program                                  SCMatchC (ms)                         MatchC (ms)          Ratio
                                                                   Solver (ms)
       group undefined
      1 division_by_zero_0_1.c                      28                 5                359                7.80%
      2 uninitialized_variable_0_1.c                12                 0                347                3.46%
      3 unallocated_location_0_1.c                  22                 0                353                6.23%
      4 uninitialized_memory_0_1.c                  40                 4                361               11.08%
       group simple
      1 average_1_0.c                               15                 0                328               4.57%
      2 minimum_1_0.c                               39                14                350              11.14%
      3 maximum_1_0.c                               39                16                344              11.34%
      4 multiplication_by_addition_1_0.c            79                35                375              21.07%
      5 sum_recursive_1_0.c                         65                33                358              18.16%
      6 sum_iterative_2_0.c                         88                46                363              24.24%
      7 comm_assoc_1_0.c                         1,273             1,217                343             371.14%
       group list
      01 head_1_0.c                                 23                7                 338                6.80%
      02 tail_1_0.c                                 30               11                 338                8.88%
      03 add_1_0.c                                  30                7                 340                8.82%
      04 swap_1_0.c                                 54               19                 344               15.70%
      05 deallocate_2_0.c                           78               46                 359               21.73%
      06 length_recursive_1_0.c                     74               56                 359               20.61%
      07 length_iterative_2_0.c                     94               54                 376               25.00%
      08 sum_recursive_1_0.c                        57               41                 356               16.01%
      09 sum_iterative_2_0.c                       102               55                 374               27.27%
      10 reverse_2_0.c                             119               74                 370               32.16%
      11 append_2_0.c                              189              156                 393               48.09%
      12 copy_2_0.c                                262              101                 418               62.68%
      13 filter_3_0.c                              407              297                 467               87.15%
       group sorting
      1 insert_2_0.c                               461               356                522              88.31%
      2 insertion_sort_3_0.c                       609               378                561             108.56%
      3 bubble_sort_3_0.c                          597               511                514             116.15%
      4 quicksort_4_0.c                            812               830                615             132.03%
      5 merge_sort_3_0.c                         2,938             3,451              1,341             219.09%
      Total                                      8,636                 0             12,266               70.41%



whose verification entails solving complex constraints, the execution time can be negatively affected
by the chosen SMT solver.

7.4    Assessing the benefits of incremental verification
To answer RQ2, we executed SCMatchC on benchmarks MB2–MB6. For each program in these
benchmarks, we consider the initial version 𝑣 0 and several variations thereof, 𝑣 1, . . . , 𝑣𝑖 , . . . , 𝑣𝑛 ; for
each program version 𝑣𝑖 , we compared the time needed to verify 𝑣𝑖 from scratch with the time
spent for the incremental verification (based on the original verification of 𝑣 0 ).
    Benchmark MB2. Table 8 reports the results obtained for MB2. Column avg. initial indicates
the average execution time for the (non-incremental) verification of the initial version 𝑣 0 of the
program; column avg. w/o incr. indicates the average execution time for the verification from scratch
(i.e., without using incrementality) of the various modified versions of the original program; column

                                                                  , Vol. 1, No. 1, Article . Publication date: June 2026.
:42    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

        Table 8. Execution time and speedup for the verification of the programs in benchmark MB2

                                       avg.          avg.                   avg. solv.   avg. solv.
                                     initial       w/o incr.   avg. incr.                              avg. solv.
         Program                                                 (ms)
                                                                             initial     w/o incr.
                                                                                                      incr. (ms)
                                                                                                                    Speedup
                                      (ms)          (ms)                      (ms)         (ms)
         1_average                          7            12           11           0             5             5        1.09
         2_minimum                         21            23           20          13            14            13        1.15
         3_maximum                         23            23           21          14            14            14        1.10
         4_mult_by_add                     41            38           16          26            24             6        2.37
         5_sum_recursive                   33            27           14          23            18             7        1.93
         6_sum_iterative                   52            40           23          35            24            11        1.74
         7_comm_assoc                    1116           267          257        1096           247           241        1.04
         Average                               –          61          52            –           49            42        1.19



avg. w/incr. indicates the average execution time for the incremental verification (starting from the
results of the initial version) of the various modified versions of the original program; columns
avg. solv. initial, avg. solv. w/o incr., and avg. solv. w/incr. indicate the average time taken by the
SMT solver during the verification of the initial version, the non-incremental verification, and the
incremental verification, respectively; column speedup indicates the ratio between the average time
for non-incremental verification and the one for incremental verification.
   For the first three programs the speedup is limited and the incremental verification time is not
significantly different from the verification time of 𝑣 0 . This is not surprising since these programs
consist of few lines of code (corresponding to circa 30 tokens); this means that for any change
almost the entire program has to be re-evaluated (about 10–20 tokens were re-parsed for every
change), minimizing the benefits of incremental verification. For the next three programs, however,
we can already see a significant speedup despite their relatively small size. The last program,
7_comm_assoc, has the lowest speedup. One can notice that most of the verification time is spent by
the SMT solver, to verify both the original version and also the modified versions; this is due to the
complex constraints generated for this program, especially those containing non-linear operators.
   Benchmark MB3. Table 9 shows the execution time and the speedup for the verification of
the programs in benchmark MB3. Each row, except the first one indicating the initial version,
corresponds to a group of programs containing an operator mutation in the function indicated in
the row name; the columns have the same meaning as in Table 8.
   The results show that the incremental verification time is always lower than the non-incremental
one by an order of magnitude, with an average speed-up of about 15. It is interesting to remark the
sharp difference between the verification time for the programs with changes in function 7_comm_-
assoc and programs with changes in other functions (rows 2–7). Since most of the verification
time is spent in verifying function 7_comm_assoc, when the change does not affect this function,
the incremental verification is extremely fast. On the other hand, when the change affects function
7_comm_assoc, the non-incremental verification time is often reduced, while the incremental
verification time is increased. The non-incremental verification time is reduced because a random
mutation in function 7_comm_assoc can frequently introduce a violation that is easy to detect,
although the verification of programs with changes to this function is generally heavier than the
verification of programs with changes to other functions. In fact, the global average non-incremental
verification time and the solver time are mainly determined by the few cases in which changes to
function 7_comm_assoc make the verification non-trivial.
   Benchmark MB4. The different functions in the programs in benchmark MB3 are independent: if
a function is modified, there is no need to re-evaluate the others. This is the best-case scenario for
incremental verification and indeed we obtained a high speedup value. To assess the performance

, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                                   :43

        Table 9. Execution time and speedup for the verification of the programs in benchmark MB3

                                                                              avg. solv.
                                                  avg. w/o    avg. incr.                      avg. solv.
             Program                             incr. (ms)     (ms)
                                                                              w/o incr.
                                                                                             incr. (ms)
                                                                                                           Speedup
                                                                                (ms)
             Initial                                  1256            –             1309               –           –
             Change in 1_average                      1270            9             1325               4      140.84
             Change in 2_minimum                      1263           17             1316              10       74.07
             Change in 3_maximum                      1258           18             1314              10       69.93
             Change in 4_mult_by_add                  1259           19             1306               5       66.22
             Change in 5_sum_recursive                1265           23             1314               6       54.94
             Change in 6_sum_iterative                1255           35             1294              12       35.80
             Change in 7_comm_assoc                    320          223              371             192        1.44
             Average                                  1127           49             1177              34       22.99


       Table 10. Execution time and speedup for the verification of the programs in benchmark MB4

                                                                              avg. solv.
                                                  avg. w/o    avg. incr.                      avg. solv.
             Program                             incr. (ms)     (ms)
                                                                              w/o incr.
                                                                                             incr. (ms)
                                                                                                           Speedup
                                                                                (ms)
             Initial                                  1282            –             1274               –           –
             Change in 1_average                      1321          184             1312             124        7.18
             Change in 2_minimum                      1315          226             1302             165        5.82
             Change in 3_maximum                      1320          200             1309             138        6.60
             Change in 4_mult_by_add                  1311          197             1295             130        6.65
             Change in 5_sum_recursive                1311          207             1293             138        6.33
             Change in 6_sum_iterative                1309          203             1289             129        6.44
             Change in 7_comm_assoc                    432          330              417             251        1.31
             Average                                  1188          221             1114             154        5.38



of incremental verification also in a less favorable scenario, we verified the programs in benchmark
MB4, in which a new function calls all subprograms. In this new scenario, the overall correctness
depends on all subprograms; this dependency necessarily penalizes the incremental verification
time. The results are shown in Table 10: the incremental approach is still quite effective — achieving
an average speedup of 4.69 — despite the intra-procedural dependencies in the programs.
   Benchmark MB5. Table 11 shows the results for the verification of the programs in benchmark
MB5. In addition to the columns used in Table 8, column Error indicates whether a program version
introduces an error; column Change Type denotes the type of change applied to each version
(see legend at the bottom of the table for details); column StCh Position represents the position
(expressed in percentage) where the program state differs from the original run (not to be confused
with the position of the change in the source code).
   In this case, the overall result in terms of speedup is much lower than in the previous benchmarks,
although still appreciable and in some cases quite relevant. The explanation for this performance
gap lies in the most distinctive difference between MB5 and MB1–4: the former does not contain
any Hoare-style annotation and thus the verification is rather in the debugging style. In fact, the
lack of separate and well-structured annotations for key program fragments, such as functions and
loops, makes the global verification not compositional and constrains most of it to be performed in
a purely sequential way, which restarts from scratch upon any change. Under this scenario, only
the initial phase, i.e., parsing and attribute evaluation, is incremental (to a first approximation22 ).
22 More precisely, some optimizations already produce incremental benefits even in the following phases of symbolic

interpretation and constraints solving; as we will discuss in Section 9, additional optimizations are the object of further
investigation.


                                                                           , Vol. 1, No. 1, Article . Publication date: June 2026.
:44    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

Table 11. Characterization of the change, execution time, and speedup for the verification of the programs in
benchmark MB5

                                                             avg.                   avg. solv.
                                   Change        StCh      w/o incr.   avg. incr.                 avg. solv.
       Version         Error        Type       Position                  (ms)
                                                                                    w/o incr.
                                                                                                 incr. (ms)
                                                                                                               Speedup
                                                            (ms)                      (ms)
       Initial               –           –             –      13371           –          4403             –           –
       1                    no           a         53.86      13982        8034          4580           806        1.74
       2                   yes           b         62.69       1122         102           447             0       11.00
       3                    no           c          1.33      17339       13460          5668          1657        1.29
       4                    no           c         35.46      14954        9037          4906          1132        1.65
       5                    no           d          1.20      16417       16181          4895          4621        1.01
       6                    no           a          9.97      13421        7851          4333          2405        1.71
       7                    no           b          1.33      13348        9528          4404           813        1.40
       8                    no           b          1.33      13348        9580          4412           847        1.39
       9                    no           a          2.56      20103       18804          7118          6573        1.07
       10                   no           a          9.90      13259        6564          4330          1809        2.02
       11                  yes           d         61.41      11354        7551          4049           416        1.50
       12                   no           c          0.70      28980       28907          8952          8708        1.00
       13                   no           b          1.73      13360       13155          4427          4178        1.02
       14                   no           b          1.88      13340       13058          4404          4132        1.02
       15                   no           d          1.20      16436       16162          4907          4634        1.02
       16                   no           b          1.33      13391        9602          4404           856        1.39
       17                   no           b          1.33      13353        9540          4427           808        1.40
       18                   no           b          1.33      13350        9596          4411           846        1.39
       19                   no           b          1.33      13366        9600          4429           859        1.39
       20                   no           a          2.56      20151       18846          7161          6573        1.07
       21                   no           e          3.37      15768       14523          5934          5433        1.09
       22                   no           e          3.46      15202       12954          5700          4241        1.17
       23                   no           e         19.29      15524       10621          5743          2894        1.46
       24                   no           e         18.81      15562       10458          5607          2646        1.49
       25                   no           a         29.82      13987        8186          4581           966        1.71
       26                   no           d          1.60      13087       12814          4335          4077        1.02
       27                   no           d          1.20      16444       16130          4905          4632        1.02
       28                   no           c          4.74      13356       11973          4423          3854        1.12
       29                   no           d          8.66       7156        3969          2383             0        1.80
       30                   no           d          8.66       7308        5994          2458          1957        1.22
       31                  yes           d          3.50       9377        7343          3562          1643        1.28
       32                   no           d         18.40      12477        8875          4075           491        1.41
       33                  yes           f         97.14        483          82           267            49        5.89
       34                   no           g          0.56      44403       40309         13549          9414        1.10
       35                   no           h          4.74      13367       11980          4415          3834        1.12
       36                   no           b          1.57      13378        9293          4429           348        1.44
       37                   no           f         16.44      13389        7298          4423          1774        1.83
       38                  yes           f         79.41        469          61           257            37        7.69
       39                   no           a         29.82      13976        8214          4581           967        1.70
       40                   no           d          9.16      12856        8222          4220           389        1.56
       41                   no           d          8.35      14249       11048          4685          2230        1.29
       Average                 –         –            –       14054       11110           4663         2550        1.27

         Description of the column Change Type: "a": relational operator mutation; "b": value change; "c":
         logic operator mutation; "d": remove logic expression; "e": arithmetic expression mutation; "f":
         array index change; "g": change in structure of logic expression; "h": ternary operand switch.


   The effects of incrementality are determined by various factors, such as the type of the change
(e.g., which operator is replaced), the percentage of time taken by the SMT solver, whether the
change resulted into an error, and—in case of an error—its type (e.g., a memory access violation or
an assertion violation), the position of the error in the code, and the position where the program
state differs from the original one. We do no report a detailed analysis on the impact of these factors
on the resulting speedup, because it would be cumbersome and not conclusive due to the interplay
among all these factors; however, we enriched Table 11 with the three columns mentioned above,
referring to three major factors which certainly have significant impact on the overall performances
of the incremental tool.

, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                                 :45

                                      Table 12. Incremental evaluation of MB6

                                              avg. w/o    avg. incr.    avg. solv.     avg. solv.
                 Program                      incr. (s)     (s)        w/o incr. (s)   incr. (s)
                                                                                                    Speedup

                 rbtree_v0_6_0.c                  2247           –               67             –           –
                 rbtree_v1_6_0.c                  2416        1612               66            30        1.50
                 rbtree_v2_6_0.c                  2249          90               63             3       24.81
                 rbtree_v3_BUG_2_4.c               640         386               15             4        1.66
                 rbtree_v4_BUG_5_1.c              1776        1384               37            31        1.28




   Benchmark MB6. Table 12 shows the results for the verification of the programs in benchmark
MB6. The results confirm the observation made for the previous benchmark: the lack of Hoare-style
annotations leads to a decreased, but still relevant, effectiveness of the incremental verification
approach. The increased algorithmic complexity, specific to this benchmark, produces a combi-
natorial explosion of the execution paths to be verified and, consequently, a substantial increase
of the execution time, both for the case of incremental verification and for the non-incremental
one. Indeed, differently from all other benchmarks, in this case the execution times reported in
Table 12 are expressed in seconds rather than in milliseconds. The lack of compositionality in the
whole verification process has also constrained us to analyze trees with a minimum amount23 of
nodes.
   The remarkable difference between the speedup obtained for version v1 and the one obtained for
version v2 can be explained in terms of the changes applied to the two program versions and their
effects. In v1, the change is the merge of the functions for performing left and right tree rotations.
In red-black tree algorithms, rotations are invoked very often; when program annotations are not
provided, the rotation function has to be (symbolically) re-executed at every call. This impacts on
the total execution time, yielding a modest speedup of 1.41. In v2, the change is the replacement
of a loop by a recursive call in function find-minimum. This change has a limited impact on the
overall (symbolic) execution of the program, yielding a remarkable speedup of 28.55.
   The (unintended) errors introduced in versions v3 and v424 were detected by the violation of
debugging assertions that we introduced in the code; such violations triggered the immediate
interruption of the execution but also resulted in repeating a significant part thereof even in the
case of incremental verification.
  Discussion. The above results show that our approach for incremental verification can provide a
speedup in program verification ranging from 1.06 to 109.64. The main explanation for the wide gap
between these extreme values is the fundamental difference between the two types of verification
supported by the Matching logic approach: the compositional, Hoare-style verification and the
more traditional, but essentially sequential, verification carried on through symbolic execution.
Among the additional factors determining this gap we recall:
    • Size of the program. For small programs, for any change almost the entire program has to be
      re-evaluated, minimizing the speedup.
    • Constraint solver. The verification of some programs involves the solution of complex con-
      straints (e.g., with non-linear operators), which affects the overall checking time.
    • Inter-procedural dependencies. When a change occurs in a function with strong inter-procedural
      dependencies, these dependencies penalize the speedup.

23 Although minimum, the size of the analyzed tree is still big enough so that all possible code branches are exercised.
24 In v3, the lack of a return statement resulted in changing the color of both children of a node, instead of only one; v4

does not handle correctly the case in which the same key is inserted several times.


                                                                         , Vol. 1, No. 1, Article . Publication date: June 2026.
:46    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

      • Position, type, and consequences of the change. The position of the change (e.g., whether it
        is located at the beginning or at the end of the code), its type, and its consequences (e.g.,
        whether it produces an early or a late deviation from the original execution flow; whether it
        introduces an error or a different but still correct behavior) certainly affect the verification
        performance; however, such an impact may be hardly abstracted into general rules.
  Overall, the results of incremental verification derive from a combination of these factors; as a
consequence, often their effects cannot be easily analyzed separately. Finally, let us remark that
highly-sophisticated algorithms dramatically increase the global complexity of verification, both
for the case of non-incremental verification and for the incremental one; in the latter, however,
even small speedups may result into high gain in absolute execution time.

8     RELATED WORK
The approach presented in this paper is mainly related to work performed in the context of matching
logic and incremental verification.
   The verification of programs annotated with matching logic specifications has been investigated
in [50], which provides a language-independent program verification framework and an instantia-
tion of this framework for KernelC (as implemented in MatchC [16]). Differently from our approach,
this work does not support incremental verification.
   The problem of incremental verification has been tackled from different angles [25]. One of the
most common approaches is based on the assume-guarantee paradigm [33], which considers the
system as a collection of cooperating modules, each of them annotated with properties that are
guaranteed to the other modules. Verification is done in a compositional way, first by reasoning
about each module separately and then by deducing properties about the integration of the different
modules. If a change impacts only one module, verification can be performed only on it, with no
need for verifying the other modules. This approach has been used both in the context of model
checking [13], program analysis [9], and also for the quantitative analysis of models [36]; it has also
been extended to support the substitutability problem [55]. The main weakness of compositional
verification methods is their reliance on the modular structure of the system, which cannot deal with
cross-module changes and intrinsically entails a coarse granularity at the model level. By contrast,
our approach does not require any a priori decomposition of the system into a modular structure,
since it leverages the natural structure encoded in parse tree, which is available at any granularity
level. Furthermore, we have seen that our approach can achieve the benefits of compositionality
even independently from a modular structure by exploiting suitable annotations.
   Parametric analysis is an approach for incremental verification that allows for a certain degree
of uncertainty (e.g., due to future changes) in the system to verify, by replacing some actual system
parameters with symbolic placeholders. The output of parametric analysis is an expression having
as unknowns those parameters. If a change in the system can be conveniently reflected by a new
assignment to the parameters, one can just re-evaluate the symbolic expression with the new
parameters, instead of re-executing the verification procedure from scratch. This technique has
been mainly used for the analysis of quantitative properties [17, 21, 22, 30]. Parametric analysis
requires anticipated knowledge of both the global structure of the system and the location of
possible changes; furthermore, it requires an ability to cast changeable information as system
parameters. Our approach, instead, does not require to know in advance the location of possible
changes, and supports any kind of change (not only the one related to system parameters).
   Another approach for incremental verification is based on model reuse, where the idea is to reuse
“models” constructed during the verification of a base version for the verification of a new version.
For example, extreme model checking [31] proposes to reuse a proof of correctness obtained from a

, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                    :47

previous run and to start the new state-space exploration from the point in the abstract state space
in which the old proof cannot be further followed. Changes are detected by comparing the control
flow automata of the new program with the abstract reachability tree of the previous version.
Reference [14] proposes two incremental algorithms for automaton-based safety analysis of C/C++
programs. The idea is to first compute the synchronous product of the control-flow graphs (CFGs)
of the program functions and the automaton of the property to verify; this product is represented as
a derivation graph. Upon a change (represented as a list of additions, deletions, and modifications
of the program CFGs), the previous derivation graph is inspected and the synchronous product
is recomputed only for the parts affected by the changes. In the context of explicit-state model
checking, reference [38] proposes incremental state-space exploration (ISSE), which saves the
state-space graph of a previous program version and examines it during the next exploration for a
new program version, to check which transitions need to be re-executed and explored, based on
the code changes made since the previous exploration. The basic idea of ISSE is to avoid executing
unnecessary transitions and the related computations. Another approach for explicit-state model
checking is Regression Model Checking [58] (RMC), which also first saves the state space from the
analysis of a previous version; upon a change, it performs (dynamic) impact analysis to identify
that parts affected by a change, identifies “dangerous elements” in the graph, i.e., elements whose
behavior can be affected by the change, and prunes the safe ones. eVolCheck [20] is a bounded
model checker for C programs that (re)uses over-approximating summaries of all program functions,
obtained through Craig interpolation. eVolCheck compares two versions for identifying the set
of syntactic changes, function by function, using the longest common sub-sequence algorithm.
Upon a change, it checks whether the summaries of the functions affected by the change are still
valid over-approximations; if it is the case the change is considered safe and the verification stops.
Otherwise, either the function summaries have to be refined or one of the summaries is violated and
the check has to be propagated up through the call tree. The main differences of these approaches
with ours lie in: 1) change detection: our approach exploits the mechanism of incremental parsing
for OPG; 2) granularity of the information that can be reused: our approach maintains information
relevant to the verification (in the form of grammar attributes) at a very fine level of granularity,
for each node of the syntax tree.
   Other approaches for incremental verification are based on equivalence checking between a new
program version and an old one. For example, regression verification [27] uses bounded model
checking to prove the partial equivalence of two programs (i.e., of two sets of functions), by the
analysis of the call graph. An extension of regression verification for multi-threaded programs,
including a notion of partial equivalence for non-deterministic programs, is presented in [11].
Another way of checking the equivalence of programs is checking only the fragments impacted by
changes, for example using change-impact analysis; this method has been exploited in the context
of incremental symbolic execution [29, 48, 52]. The main difference of these approaches with ours
is that the latter is agnostic from the point of view of equivalence between two versions, since our
algorithm is driven by changes at the attribute level (as determined by changes in the parse tree).
   Also related is the work addressing general approaches for defining incremental program analyses
integrated into IDEs, such as the IncA language [57]. IncA is a domain-specific language for defining
efficient incremental program analyses, which are then translated into graph patterns; the analyses
are performed using incremental graph pattern matching. This approach is conceptually similar to
our general approach SiDECAR [3, 5], at the basis of the work presented in this paper.
   Finally, the benefits of our incremental approach can certainly be affected by suitable caching
strategies of verification results, such as those used in the context of proof obligations for the Dafny
verifier [39]; we have not addressed this issue in this paper, but plan to investigate it as part of
future work.

                                                            , Vol. 1, No. 1, Article . Publication date: June 2026.
:48    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

9     CONCLUSIONS
In this paper we applied the SiDECAR technology—a general syntactic-semantic framework for
incremental verification—to make matching logic-based [51] verification of KernelC [16] programs
incremental. More precisely, we encoded a verification procedure for KernelC programs (annotated
with matching logic properties) as (synthesized) semantic attributes associated with an operator
precedence grammar that defines the syntax of KernelC. In this representation, every attribute of
an internal node of the syntax tree is a collection of: 1) semantic rules associated with the code
fragment that is the frontier of the tree; 2) verification tasks, to be combined later with those of
other subtrees. Verification tasks are performed as soon as possible during the construction of the
tree until its root is reached and the whole verification is completed (unless an error is detected
before that).
   The chosen application field is particularly challenging because, even if parsing (and the as-
sociated evaluation of synthesized attributes) can be performed locally in the case of operator
precedence languages, software execution is necessarily sequential. This peculiarity is well caught
by the matching logic formalism, which is a nice synthesis of two major formal verification tech-
niques: 1) Hoare’s style, based on invariants and function input-output specifications, which is
compositional but requires human ingenuity; 2) symbolic execution, which is more sequential in
nature and subject to state explosion.
   We have implemented this approach in the SCMatchC tool and evaluated it through a rich and
structured benchmark. The evaluation results show that our syntactic-semantic approach is at least
comparable, in terms of efficiency, with the state-of-the-art, non-incremental tool MatchC [16].
Furthermore, when compared to redoing the whole verification from scratch, our approach outper-
forms program re-verification after changes if the program is fully annotated, as in Hoare’ style
proofs; when instead the verification is based on sequential symbolic interpretation the effectiveness
of incrementality depends on various factors (e.g., the position of the change and its type), often in
an interdependent way, but in any case the benefits range from minimum but still meaningful to
quite relevant.
   The results obtained by this new application of SiDECAR can be empowered along two main
directions.

   Generalization. The first experience with KernelC, which is a significant subset of C including
cumbersome language features such as dynamic memory management, argues in favor of the
possibility of replicating it with other languages. Furthermore, the fairly large and heterogeneous
benchmark adopted gives evidence that the benefits of incrementality can be exploited in many
program categories and application domains, although, necessarily, one must expect strong varia-
tions in the performance of the tool depending on program features, type of changes, and adopted
verification techniques (i.e., whether programs are annotated).

   Taming complexity and scalability by means of parallelism. There is no doubt that (semi)automatic
verification suffers from scalability problems due to the intrinsic complexity of the necessary
algorithms — essentially the combinatorial explosion of execution paths (see, for example, the
difference between the execution times of benchmark MB6 and the other benchmarks). These
problems can be alleviated by traditional approaches such as modularity and the compositionality
that can be achieved through program annotations. Incrementality is another powerful tool which
can be further endowed by allowing for processing multiple, scattered changes simultaneously and
by pairing it with parallelism. The latter in fact is another way of exploiting the local parsability
property which has already been applied successfully to compiler generation [1].
The current version of SiDECAR actually already integrates the parallel parser proposed in [1] with

, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                                 :49

parallel attribute evaluation, It also supports parallel calls to the solver, which are anticipated during
attribute evaluation of the internal nodes of the syntax tree. The combination of these techniques
enables the simultaneous support of multiple changes in parallel and in an incremental way (as
described in Section 6.2). Such features already significantly improve the overall performance of
the tool; however, they have been switched off during the experimentation reported in Section 7
because our goal was to evaluate the benefits of incrementality in isolation. Nevertheless, by
switching on these parallel-enabling features, the overall ratio between SCMatchC and MatchC
would decrease from 117.19% to 70.41%. A more ambitious way to exploit parallelism even during
the—not completely necessarily—sequential symbolic interpretation of program code is the object
of further investigation.

REFERENCES
 [1] Alessandro Barenghi, Stefano Crespi Reghizzi, Dino Mandrioli, Federica Panella, and Matteo Pradella. 2015. Parallel
     Parsing Made Practical. Science of Computer Programming 112, P3 (Nov. 2015), 195–226. DOI:http://dx.doi.org/10.1016/
     j.scico.2015.09.002
 [2] Kent Beck, Mike Beedle, Arie van Bennekum, Alistair Cockburn, Ward Cunningham, Martin Fowler, James Grenning,
     Jim Highsmith, Andrew Hunt, Ron Jeffries, Jon Kern, Brian Marick, Robert C. Martin Steve Mellor, Ken Schwaber, Jeff
     Sutherland, and Dave Thomas. 2001. Manifesto for Agile Software Development. http://agilemanifesto.org/. (2001).
 [3] Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, and Dino Mandrioli. 2013. A Syntactic-Semantic Approach to
     Incremental Verification. (2013). http://arxiv.org/abs/1304.8034.
 [4] Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, and Dino Mandrioli. 2014. Incremental Syntactic-semantic Reliability
     Analysis of Evolving Structured Workflows. In Part I of the Proceedings of the 6th International Symposium on Leveraging
     Applications of Formal Methods, Verification and Validation. Technologies for Mastering Change, ISoLA’14 (Lecture
     Notes in Computer Science), Vol. 8802. Springer-Verlag, Berlin, Heidelberg, 41–55. DOI:http://dx.doi.org/10.1007/
     978-3-662-45234-9_4
 [5] Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, and Dino Mandrioli. 2015a. Syntactic-semantic Incrementality for
     Agile Verification. Science of Computer Programming 97 (2015), 47–54. DOI:http://dx.doi.org/10.1016/j.scico.2013.11.026
 [6] Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro Maria Rizzi. 2015b. Syntax-driven
     Program Verification of Matching Logic Properties. In Proceedings of the 3rd IEEE/ACM FME Workshop on Formal
     Methods in Software Engineering (FORMALISE’15). IEEE Computer Society Press, Los Alamitos, CA, USA, 68–74. DOI:
     http://dx.doi.org/10.1109/FormaliSE.2015.18
 [7] Geoff Birch, Bernd Fischer, and Michael R. Poppleton. 2015. Fast Model-Based Fault Localisation with Test Suites.
     Springer-Verlag, Berlin, Heidelberg, 38–57. DOI:http://dx.doi.org/10.1007/978-3-319-21215-9_3
 [8] Roderick Bloem, Rolf Drechsler, Görschwin Fey, Alexander Finder, Georg Hofferek, Robert Könighofer, Jaan Raik,
     Urmas Repinski, and André Sülflow. 2013. FoREnSiC– An Automatic Debugging Environment for C Programs. Springer-
     Verlag, Berlin, Heidelberg, 260–265. DOI:http://dx.doi.org/10.1007/978-3-642-39611-3_24
 [9] Cristiano Calcagno, Dino Distefano, Peter W. O’Hearn, and Hongseok Yang. 2011. Compositional Shape Analysis by
     Means of Bi-Abduction. J. ACM 58, 6, Article 26 (Dec. 2011), 66 pages. DOI:http://dx.doi.org/10.1145/2049697.2049700
[10] Sagar Chaki, Edmund M. Clarke, Alex Groce, Somesh Jha, and Helmut Veith. 2004. Modular Verification of Software
     Components in C. IEEE Trans. Softw. Eng. 30, 6 (June 2004), 388–402. DOI:http://dx.doi.org/10.1109/TSE.2004.22
[11] Sagar Chaki, Arie Gurfinkel, and Ofer Strichman. 2012. Regression Verification for Multi-threaded Programs. In
     Verification, Model Checking, and Abstract Interpretation (Lecture Notes in Computer Science), Vol. 7148. Springer-Verlag,
     Berlin, Heidelberg, 119–135.
[12] Manuel Clavel, Francisco Durán, Steven Eker, Patrick Lincoln, Narciso Martí-Oliet, José Meseguer, and Carolyn Talcott.
     2007. All About Maude - a High-performance Logical Framework: How to Specify, Program and Verify Systems in Rewriting
     Logic. Springer-Verlag, Berlin, Heidelberg.
[13] Jamieson M. Cobleigh, Dimitra Giannakopoulou, and Corina S. Păsăreanu. 2003. Learning Assumptions for Compo-
     sitional Verification. In Proceedings of the 9th International Conference on Tools and Algorithms for the Construction
     and Analysis of Systems (TACAS’03). Springer-Verlag, Berlin, Heidelberg, 331–346. http://dl.acm.org/citation.cfm?id=
     1765871.1765903
[14] Christopher L. Conway, Kedar S. Namjoshi, Dennis Dams, and Stephen A. Edwards. 2005. Incremental Algorithms for
     Inter-procedural Analysis of Safety Properties. In Proceedings of the 17th International Conference on Computer Aided
     Verification (CAV’05). Springer-Verlag, Berlin, Heidelberg, 449–461. DOI:http://dx.doi.org/10.1007/11513988_45
[15] Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. 2009. Introduction to Algorithms (3. ed.).
     MIT Press, Cambridge MA. http://mitpress.mit.edu/books/introduction-algorithms


                                                                         , Vol. 1, No. 1, Article . Publication date: June 2026.
:50    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

[16] Andrei Ştefănescu. 2014. MatchC: A Matching Logic Reachability Verifier Using the K Framework. Electronic Notes in
     Theoretical Computer Science 304 (2014), 183–198. DOI:http://dx.doi.org/10.1016/j.entcs.2014.05.010
[17] C. Daws. 2005. Symbolic and Parametric Model Checking of Discrete-Time Markov chains. In Proc. of ICTAC 2004
     (LNCS), Vol. 3407. Springer, Berlin, Heidelberg, 280–294.
[18] Koen de Bosschere. 1996. An Operator Precedence Parser for Standard Prolog Text. Software: Practice and Experience
     26, 7 (July 1996), 763–779. DOI:http://dx.doi.org/10.1002/(SICI)1097-024X(199607)26:7<763::AID-SPE33>3.3.CO;2-C
[19] Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: An Efficient SMT Solver. In Proceedings of the Theory and
     Practice of Software, 14th International Conference on Tools and Algorithms for the Construction and Analysis of Systems
     (TACAS’08/ETAPS’08). Springer-Verlag, Berlin, Heidelberg, 337–340. http://dl.acm.org/citation.cfm?id=1792734.1792766
[20] Grigory Fedyukovich, Ondrej Sery, and Natasha Sharygina. 2013. eVolCheck: Incremental Upgrade Checker for C. In
     Proceedings of the 19th International Conference on Tools and Algorithms for the Construction and Analysis of Systems
     (TACAS’13). Springer-Verlag, Berlin, Heidelberg, 292–307. DOI:http://dx.doi.org/10.1007/978-3-642-36742-7_21
[21] Antonio Filieri and Carlo Ghezzi. 2012. Further steps towards efficient runtime verification: Handling probabilistic
     cost models. In Proc. of FormSERA. IEEE Computer Society, Los Alamitos, CA, USA, 2–8.
[22] Antonio Filieri, Carlo Ghezzi, and Giordano Tamburrelli. 2011. Run-time efficient probabilistic model checking. In
     Proc. of ICSE 2011. ACM, New York, NY, USA, 341–350.
[23] Michael J. Fischer. 1969. Some Properties of Precedence Languages. In Proceedings of the 1st Annual ACM Symposium
     on Theory of Computing (STOC’69). ACM, New York, NY, USA, 181–190. DOI:http://dx.doi.org/10.1145/800169.805432
[24] Robert W. Floyd. 1963. Syntactic Analysis and Operator Precedence. J. ACM 10, 3 (July 1963), 316–333. DOI:
     http://dx.doi.org/10.1145/321172.321179
[25] Carlo Ghezzi. 2012. Evolution, Adaptation, and the Quest for Incrementality. In Proceedings of the 17th Monterey
     Conference on Large-Scale Complex IT Systems: Development, Operation and Management. Springer-Verlag, Berlin,
     Heidelberg, 369–379. DOI:http://dx.doi.org/10.1007/978-3-642-34059-8_19
[26] Carlo Ghezzi and Dino Mandrioli. 1979. Incremental Parsing. ACM Transactions on Programming Languages and
     Systems 1, 1 (Jan. 1979), 58–70. DOI:http://dx.doi.org/10.1145/357062.357066
[27] Benny Godlin and Ofer Strichman. 2012. Regression Verification: Proving the Equivalence of Similar Programs. STVR
     23, 3 (2012), 241–258.
[28] Dick Grune and Ceriel J. H. Jacobs. 2008. Parsing Techniques: A Practical Guide (Second Edition). Springer-Verlag, Berlin,
     Heidelberg.
[29] Shengjian Guo, Markus Kusano, and Chao Wang. 2016. Conc-iSE: Incremental Symbolic Execution of Concurrent
     Software. In Proceedings of the 31st IEEE/ACM International Conference on Automated Software Engineering (ASE 2016).
     ACM, New York, NY, USA, 531–542. DOI:http://dx.doi.org/10.1145/2970276.2970332
[30] ErnstMoritz Hahn, Holger Hermanns, Björn Wachter, and Lijun Zhang. 2010. PARAM: A Model Checker for Parametric
     Markov Models. In Proc. of CAV 2010. LNCS, Vol. 6174. Springer, Berlin, Heidelberg, 660–664.
[31] Thomas A. Henzinger, Ranjit Jhala, Rupak Majumdar, and Marco A. A. Sanvido. 2003. Extreme Model Checking. In
     Verification: Theory and Practice, Essays Dedicated to Zohar Manna on the Occasion of His 64th Birthday (Lecture Notes in
     Computer Science), Vol. 2772. Springer-Verlag, Berlin, Heidelberg, 332–358.
[32] Fahimeh Jalili. 1985. A General Incremental Evaluator for Attribute Grammars. Science of Computer Programming 5, 1
     (1985), 83–96. DOI:http://dx.doi.org/10.1016/0167-6423(85)90005-X
[33] Cliff B. Jones. 1983. Tentative Steps Toward a Development Method for Interfering Programs. ACM Transactions on
     Programming Languages and Systems 5, 4 (Oct. 1983), 596–619. DOI:http://dx.doi.org/10.1145/69575.69577
[34] Donald E. Knuth. 1968. Semantics of Context-Free Languages. Mathematical Systems Theory 2, 2 (1968), 127–145. DOI:
     http://dx.doi.org/10.1007/BF01692511
[35] Robert Könighofer, Ronald Toegl, and Roderick Bloem. 2014. Automatic Error Localization for Software Using Deductive
     Verification. Springer Berlin Heidelberg, Berlin, Heidelberg, 92–98. DOI:http://dx.doi.org/10.1007/978-3-319-13338-6_8
[36] Marta Kwiatkowska, Gethin Norman, David Parker, and Hongyang Qu. 2010. Assume-Guarantee Verification for
     Probabilistic Systems. In Proceedings of the 16th International Conference on Tools and Algorithms for the Construc-
     tion and Analysis of Systems (TACAS’10). Springer-Verlag, Berlin, Heidelberg, 23–37. DOI:http://dx.doi.org/10.1007/
     978-3-642-12002-2_3
[37] Craig Larman and Victor R. Basili. 2003. Iterative and Incremental Development: A Brief History. Computer 36, 6
     (June 2003), 47–56. DOI:http://dx.doi.org/10.1109/MC.2003.1204375
[38] Steven Lauterburg, Ahmed Sobeih, Darko Marinov, and Mahesh Viswanathan. 2008. Incremental State-space Explo-
     ration for Programs with Dynamically Allocated Data. In Proceedings of the 30th International Conference on Software
     Engineering (ICSE’08). ACM, New York, NY, USA, 291–300. DOI:http://dx.doi.org/10.1145/1368088.1368128
[39] K. Rustan M. Leino and Valentin Wüstholz. 2015. Fine-Grained Caching of Verification Results. In Part I of the
     Proceedings of the 27th International Conference on Computer Aided Verification, CAV’15 (Lecture Notes in Computer
     Science), Vol. 9206. Springer-Verlag, Berlin, Heidelberg, 380–397. DOI:http://dx.doi.org/10.1007/978-3-319-21690-4_22


, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                               :51

[40] John Levine and Levine John. 2009. Flex & Bison (1st ed.). O’Reilly Media, Inc., Sebastopol, CA, USA.
[41] G. S. Makanin. 1977. The problem of the solvability of equations in a free semigroup. Matematicheskii Sbornik 103(145),
     2 (1977), 147–236, 319.
[42] John McCarthy. 1962. Towards a Mathematical Science of Computation. In IFIP Congress. Springer Netherlands,
     Dordrecht, 21–28.
[43] Lambert G. L. T. Meertens and Johannes C. van Vliet. 1981. An Operator-Priority Grammar For Algol 68+. CWI Technical
     Report IW 173/81. Stichting Mathematisch Centrum. 1–24 pages.
[44] Bertrand Meyer. 1992. Applying “Design by Contract”. Computer 25, 10 (Oct. 1992), 40–51. DOI:http://dx.doi.org/10.
     1109/2.161279
[45] Kivanç Muşlu, Yuriy Brun, Michael D. Ernst, and David Notkin. 2013. Making Offline Analyses Continuous. In
     Proceedings of the 2013 9th Joint Meeting on Foundations of Software Engineering (ESEC/FSE 2013). ACM, New York, NY,
     USA, 323–333. DOI:http://dx.doi.org/10.1145/2491411.2491460
[46] Derek C. Oppen. 1980. Reasoning About Recursively Defined Data Structures. J. ACM 27, 3 (July 1980), 403–411. DOI:
     http://dx.doi.org/10.1145/322203.322204
[47] David Lorge Parnas. 1972. On the Criteria to Be Used in Decomposing Systems into Modules. Commun. ACM 15, 12
     (Dec. 1972), 1053–1058. DOI:http://dx.doi.org/10.1145/361598.361623
[48] Suzette Person, Guowei Yang, Neha Rungta, and Sarfraz Khurshid. 2011. Directed Incremental Symbolic Execution.
     ACM SIGPLAN Notices 46, 6 (June 2011), 504–515. DOI:http://dx.doi.org/10.1145/1993316.1993558
[49] Grigore Roşu and Traian-Florin Şerbănuţă. 2010. An Overview of the K Semantic Framework. Journal of Logic and
     Algebraic Programming 79, 6 (2010), 397–434. DOI:http://dx.doi.org/10.1016/j.jlap.2010.03.012
[50] Grigore Roşu and Andrei Ştefănescu. 2012. Checking Reachability Using Matching Logic. ACM SIGPLAN Notices 47,
     10 (Oct. 2012), 555–574. DOI:http://dx.doi.org/10.1145/2398857.2384656
[51] Grigore Roşu, Chucky Ellison, and Wolfram Schulte. 2011. Matching Logic: An Alternative to Hoare/Floyd Logic.
     In Proceedings of the 13th International Conference on Algebraic Methodology and Software Technology (AMAST’10).
     Springer-Verlag, Berlin, Heidelberg, 142–162. http://dl.acm.org/citation.cfm?id=1946031.1946042
[52] Neha Rungta, Joshua Branchaud, and Suzette Person. 2012. A Change Impact Analysis to Characterize Evolving
     Program Behaviors. In Proceedings of the 28th IEEE International Conference on Software Maintenance (ICSM’12). IEEE
     Computer Society Press, Los Alamitos, CA, USA, 109–118. DOI:http://dx.doi.org/10.1109/ICSM.2012.6405261
[53] David Saff and Michael D. Ernst. 2004. An Experimental Evaluation of Continuous Testing During Development. ACM
     SIGSOFT Software Engineering Notes 29, 4 (July 2004), 76–85. DOI:http://dx.doi.org/10.1145/1013886.1007523
[54] Arto Salomaa. 1987. Formal Languages. Academic Press Professional, Inc., Cambridge, Massachusetts.
[55] Natasha Sharygina, Sagar Chaki, Edmund Clarke, and Nishant Sinha. 2005. Dynamic Component Substitutability
     Analysis. In Proceedings of the 2005 International Conference on Formal Methods (FM’05). Springer-Verlag, Berlin,
     Heidelberg, 512–528. DOI:http://dx.doi.org/10.1007/11526841_34
[56] Prasad Sistla. 1996. Hybrid and Incremental Model Checking Techniques. Comput. Surveys 28, 4es (Dec. 1996), 125.
     DOI:http://dx.doi.org/10.1145/242224.242384
[57] Tamás Szabó, Sebastian Erdweg, and Markus Voelter. 2016. IncA: A DSL for the Definition of Incremental Program
     Analyses. In Proceedings of the 31st IEEE/ACM International Conference on Automated Software Engineering (ASE 2016).
     ACM, New York, NY, USA, 320–331. DOI:http://dx.doi.org/10.1145/2970276.2970298
[58] Guowei Yang, Matthew B. Dwyer, and Gregg Rothermel. 2009. Regression Model Checking. In Proceedings of the 25th
     IEEE International Conference on Software Maintenance (ICSM’09). IEEE Computer Society, Los Alamitos, CA, USA,
     115–124. DOI:http://dx.doi.org/10.1109/ICSM.2009.5306334



APPENDICES
In these appendices we first provide various details about the formalization of KernelC semantics
in terms of matching logic and of its reshaping to make formulas processable by our SMT solver
and to increase the efficiency of incremental verification. In Appendix A.1, we provide the rules
to manage the stack of function calls and input/output operations; then, Appendix A.2 deals with
the complex operations to manage the heap, which have been presented in a fairly sketched way
in the main body of the paper to make it not too cumbersome. Appendix A.3 describes another
technique, complementing those presented in Section 6.2, to increase the level of incrementality
when verifying code with no annotations. Finally, in Appendix A.4, we illustrate the attribute
evaluation step for the example shown in figure 9 in section 5.

                                                                       , Vol. 1, No. 1, Article . Publication date: June 2026.
:52    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

A.1     Construct-specific details
  A.1.1 Functions. The cell stack (see Section 3.3) contains the list of active subroutines which is
represented as a list of integers. For instance, function foo is expressed by constant foo and the
configuration pattern (92) specifies that function bar can be called only from function foo.

                                     ⟨⟨bar() . . .⟩𝑘 ⟨𝑆 . . .⟩ stack ∧ head (𝑆) = foo⟩              (92)
   Logical function head is used to retrieve the first element of the list, thus foo must be the active
function when the call to function bar is performed.
   Stack properties are part of function contracts which are checked when the function is called: if
the stack does not match the function specification, the function call cannot be performed, thus
execution stops into a sink error configuration.
   We stress the fact that a theory of lists is needed to handle stack-related properties. In fact the
call stack is seen as a list of active functions; stack properties can be expressed on such list. It is
possible to provide different theories for lists which can handle any program stack. Our SMT solver
was already equipped with the basic LISP list theory, composed of the empty list, the constructor
cons, and the selectors car and cdr [46]. We have introduced additional operations/axioms to check
more specific stack properties. Nevertheless, neither our extensions nor other approaches (e.g., [41]
) allow to deal with list theory in its full generality.
   A.1.2 Input/output. KernelC provides two functions for reading and writing integer values
from the input and output streams scanf and printf. The two streams are represented as lists of
integers stored in the cells in and out, respectively.
   Function scanf takes as argument the address of a variable v. This variable will be assigned the
value of the first element of list in; such element will be removed from the list. This is formalized in
rule (93):
                                                                           
                                   scanf("%i", &v)         𝑗             𝑖
                                                   ...       ...     v ↦→ . . .                     (93)
                                          ·             𝑘 ·       𝑖𝑛     𝑗       env
  Similarly, function printf takes as argument an integer value and appends it to list out, as
described in rule (94):
                                                                D          
                                             printf("%i", 𝑖)         · E
                                                             ...      ...                           (94)
                                                    ·             𝑘 i     𝑜𝑢𝑡

  Both in and out contain lists of integers; thus, configuration patterns involving input/output can
be managed by our SMT solver as explained above.

A.2     Complete Heap formalization
We now specify heap encoding and its properties. First we formally define the basic operations
which can be performed on the heap in terms of reachability rules. Then, we present the logical
constraints that a valid heap must satisfy, in a way manageable by an SMT solver. Finally we show
how more complex memory objects (such as lists or user-defined structures) can be handled by our
heap model.
   A.2.1 Reachability rules for Heap operations. The four memory primitives available in KernelC
to manipulate the heap are malloc, free, write, and read.
   Operation malloc(𝑖) allocates 𝑖 contiguous memory blocks starting from a new location 𝑙. Rule (95)
shows the semantics of this primitive: mem is extended by mapping 𝑖 consecutive locations, starting

, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                           :53

from 𝑙, to 𝑖 empty blocks (⊥); the mapping 𝑙 ↦→ 𝑖 is added to ma to record the number of blocks
allocated starting from 𝑙.
                                D           E                                         
                   malloc(𝑖)           ·                            ·
                             ...           ...                                    ...                                (95)
                   (void*)𝑙       𝑘 𝑙 ↦→ 𝑖      ma 𝑙 ↦→ ⊥, . . . , 𝑙 + 𝑖 − 1 ↦→ ⊥      𝑚𝑒𝑚
   Operation free(𝑙) removes the sequence of consecutive locations allocated starting from the
initial address 𝑙; the number of locations to free is determined according to the content of cell ma.
Rule (96) shows the semantics of the free primitive.
                                                                                       
                    free(𝑙)         𝑙 ↦→ 𝑖            𝑙 ↦→ ⊥, . . . , 𝑙 + 𝑖 − 1 ↦→ ⊥
                            ...            ...                                       ...                             (96)
                       ·         𝑘     ·         ma                    ·                  𝑚𝑒𝑚
    Operation write(𝑙, 𝑗) stores the value 𝑗 at location 𝑙. If 𝑙 is not allocated before the write operation
(i.e., it does not appear in cell mem), the sink error configuration is reached. The semantics of write
is described in rule (97), where the value ℎ (which can possibly be the empty block ⊥) stored at
location 𝑙 is replaced by 𝑗.
                                                                      
                                        write(𝑙, 𝑗)            ℎ
                                                    ...    𝑙 ↦→ . . .                                                (97)
                                            ·            𝑘     𝑗       𝑚𝑒𝑚
   Operation read (𝑙) retrieves the content of the block at location 𝑙. If the requested address is not
allocated, the execution will move to a sink error configuration. The semantics of read is shown in
rule (98).
                                                                         
                                          read (𝑙)
                                                   . . . ⟨𝑙 ↦→ 𝑗 . . . ⟩𝑚𝑒𝑚                                          (98)
                                             𝑗            𝑘
  When the read and write operations are executed through the C dereferencing operator *, the
corresponding reachability rules become rules (99) and (100) respectively.
                                                     
                                            *𝑖
                                                  ...                                    (99)
                                         read (𝑖)      𝑘
                                                                  
                                                    *𝑖 = 𝑗;
                                                               ...                                                 (100)
                                                   write(𝑖, 𝑗)      𝑘

   A.2.2 Expressing memory-related constraints through the SMT solver. The contents of a con-
figuration pattern mem must satisfy certain regularity properties to be a valid heap state. These
properties are enforced as additional constraints, which are added to the logic formula passed to
the SMT solver. In fact the solver evaluates a formula 𝐹𝑆 composed by two parts: 𝐹𝑆 = 𝐹𝑐 ∧ 𝐶ℎ
where 𝐹𝑐 is the original configuration formula and 𝐶ℎ is the conjunction of the constraints derived
from the heap. The constraints required for heaps are given below:
   NULL value. The C NULL constant points to a non-existing memory cell. For consistency with C
semantics we use for it the value 0. Of course, it should never happen that a location with value 0
is allocated in the heap. To ensure this property we need the following logical constraint:

                                     𝐶 0 = ∀((𝑖 ↦→ 𝑗) ∈ 𝑚 : mem).𝑖 ≠ 0                                             (101)
  Since every mem structure has a finite number of elements, constraint (101) is instantiated in
our solver as a finite logical ∧; e.g., in a mem cell containing 𝑛 locations with addresses ℎ 1, . . . , ℎ𝑛 ,

                                                                   , Vol. 1, No. 1, Article . Publication date: June 2026.
:54    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

constraint (101) would be:
                                                                 𝑛
                                                                 Û
                                                          𝐶0 =         ℎ𝑖 ≠ 0                     (102)
                                                                 𝑖=1

   Heap separation. We also have to ensure that the heap cannot have different entries at the same
location, as specified by the logical constraint

      𝐶ℎ𝑠 = ∀((𝑖 ↦→ 𝑎) ∈ 𝑚 : mem), (( 𝑗 ↦→ 𝑏) ∈ 𝑚 : mem).(𝑖 = 𝑗 =⇒ (𝑖 ↦→ 𝑎) ≡ ( 𝑗 ↦→ 𝑏))          (103)
   The distinct function provided by the Z3 SMT solver, which assesses that its arguments are
distinct, has been exploited to join in one constraint both logical constraints (101) and (103):

                                              𝐶 0𝑖𝑠 = distinct (0, ℎ 1, . . . , ℎ𝑛 )              (104)
   Positive memory locations. Usually the memory locations allowed by the C semantics are only
positive integers. Thus, it may be useful to include the following constraint (for convenience,
formulated in an abstract version making use of a quantifier):

                                           𝐶 + = ∀((𝑖 ↦→ 𝑎) ∈ 𝑚 : mem).𝑖 > 0                      (105)
  A.2.3 Arrays and structs. Arrays in C are just ”syntactic sugar” for pointer arithmetics and have
not been included in the original KernelC syntax; our version of the language, instead, does include
syntactic constructs to use arrays but they are limited to the case where their elements are integers
and therefore have unitary size: consistently, the access to an array element is formalized through
rule (106):
                                                             
                                         array[index]
                                                          ...                                 (106)
                                       ∗(array + index)        𝑘
  Structs too are implemented as contiguous memory locations. In such a case we must provide
access to a location with a certain offset using an identifier. For instance, with reference to the
typical -> operator, reachability rule (107) computes the actual address of a struct field, whereas
rule (108) formalizes the assignment to a struct’s field.
                                                        
                                           p->field
                                                     ...     ∧ 𝑙 = p + fieldOffset                (107)
                                               𝑙          𝑘
                                                                         
                                                 ptr->field=𝑖;
                                                                      ...                         (108)
                                               write(ptr->field, 𝑖)        𝑘

   A.2.4 Struct and Typing. Since KernelC has only one integer type it seems perfectly reasonable
to avoid storing the type of each logical variable. To handle structs, however, this need arises, since,
e.g., there could be multiple struct definitions with the same field at different positions. On the
other hand, there is no way for reachability rule (107) to associate a particular struct definition to
pointer 𝑝, unless extending logical variables with a type.
   To handle these situations, we introduced an optional type for integer logical variables, forming
a pair (type, value) which can be used along traditional value integer logical variables. A typed
value can discard its type to match an untyped variable, but not vice-versa. The only reachability
rules which are affected by types are variable declaration, evaluation, assignment (see Table 1) and
read operation (see reachability rule (99)).

, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                    :55

   Types are associated with local variables in cell env for any variable, as shown in reachability
rule (109), which associates type foo∗ to program variable ptr.
                                                                                 
                      struct foo* ptr;                              ·
                                                 ...                            ...            (109)
                                 ·                    𝑘 ptr ↦→ (foo∗, undef)         env
   Of course, during program variable evaluation the associated type (if present) must be retrieved,
as shown in reachability rule (110).
                                                                         
                                        x
                                             . . . ⟨x ↦→ (t, a) . . . ⟩ env                    (110)
                                      (𝑡, 𝑎)        𝑘
   The type of local program variables in env is preserved, as shown in reachability rule (111).
                                                                       
                                  x = (𝑠, 𝑎)                  (𝑡, 𝑏)
                                                 ...     x ↦→         ...                      (111)
                                     (𝑠, 𝑎)           𝑘       (𝑡, 𝑎)        env
In this case even though type 𝑠 of expression 𝑎 is maintained in cell 𝑘, type 𝑡 is not overwritten in
cell env.
   Logical variable types are not stored in the mem cell. However in read operation (reachability
rule (98)), the type of the address is maintained as the type of the value read, as shown in rule (112).
                                                                        
                                    read ((𝑡, 𝑙))
                                                  . . . ⟨𝑙 ↦→ 𝑗 . . . ⟩𝑚𝑒𝑚                        (112)
                                        (𝑡, 𝑗)           𝑘
  Logical variable types are used to trigger a specific reachability rule to access struct fields:
rule (113) extends rule (107) to provide access to field field of struct structPtr in the case of a
typed variable.                                       
                           (structPtr, p)->field
                                                   ...     ∧ 𝑙 = p + fieldOffset              (113)
                                (fieldType, 𝑙)          𝑘
The type of the field value fieldType is set for the field location, which, after applying the read
operation of reachability rule (112) will be transferred to the read value.
  We also introduced a casting operator, allowing to change the type of an object. Its semantics is
shown in reachability rule (114).
                                                              
                                          (otherType)𝑜
                                                           ...                                (114)
                                           (otherType, 𝑜)       𝑘
In this case 𝑜 type is changed to otherType.
   Finally, we define the behavior of operator sizeof, through reachability rule (115).
                                                                 
                                sizeof(struct structName)
                                                              ...                                           (115)
                                               𝑆                   𝑘
   The rule computes the number of memory blocks required by a structName object. The value 𝑆
is a constant computed from the struct declaration as the sum of the sizes of its fields.
  A.2.5 Storing data structures. Arrays and records are stored in memory as sequences of contigu-
ous memory cells; thus we define a reachability rule that associates to a variable identifier a finite
sequence of contiguous locations, starting from a base address as shown in cell (116).
                                          ⟨𝑥 ↦→ [𝑎, 𝑏, 𝑐]⟩ mem                                              (116)
The contents of cell (116) is equivalent to cell (117).
                                  ⟨𝑥 ↦→ 𝑎, 𝑥 + 1 ↦→ 𝑏, 𝑥 + 2 ↦→ 𝑐⟩ mem                                      (117)

                                                            , Vol. 1, No. 1, Article . Publication date: June 2026.
:56    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

Cell (116) is more abstract and useful to write specifications; cell (117) is lower-level and useful to
execute a program.
  As usual, a list element consists of a struct with two fields: the first field is the element’s value,
the second one is the pointer to the next element. To illustrate how lists are managed in our
implementation, consider cell (118)
                                                     ⟨𝑥 ↦→ list (𝐴)⟩ mem                           (118)
where 𝐴 is a logical variable representing a list of elements, which abstracts away from implemen-
tation details such as the precise address of each element. This information, however, is necessary
to execute a program using such data structure; thus, to access a single element of the list, an
equivalent representation of the list must be built as a sequence of locations.
   A naive solution would be to perform this conversion at the beginning of a verification task
by “statically allocating” a fixed number of cells for any list. In the example of cell (118), if 𝐴 is
composed by elements [4, 2], the resulting heap for mem (118) would be:
                                       ⟨𝑥 ↦→ 4, 𝑥 + 1 ↦→ 𝑖, 𝑖 ↦→ 2, 𝑖 + 1 ↦→ 0⟩ mem                (119)
In this case read/write operations can be easily implemented but this approach has an obvious
drawback: since lists are unbounded dynamic objects, we would be compelled to allocate a fixed
maximum number of locations for each of them. To overcome this limitation the unrolling of such
objects is delayed to the moment in which an operation on the object is required. In the above
example we have the structure:
                                      ⟨𝑥 ↦→ list ( [4, 2])⟩ mem                             (120)
When an operation on the locations 𝑥 or 𝑥 + 1 is required, the heap is expanded as follows:
                                         ⟨𝑥 ↦→ 4, 𝑥 + 1 ↦→ 𝑖, 𝑖 ↦→ list ( [2])⟩ mem                (121)
One step of unrolling is performed: the first location is expanded; the rest of the list is pointed by 𝑖.
In this case 𝑖 is a fresh logical variable, distinct from any other location in the heap.
   A subsequent access to 𝑖 or 𝑖 + 1 locations would cause the complete extension of the list as
follows:
                                ⟨𝑥 ↦→ 4, 𝑥 + 1 ↦→ 𝑖, 𝑖 ↦→ 2, 𝑖 + 1 ↦→ 0⟩ mem                       (122)
In this way infinite objects can be handled by performing successive unrolling steps only when
needed, requiring only the minimum number of locations in the heap.
   A second problem arises when a final configuration pattern is reached: in order to verify the list
contents against a possible postcondition it may be necessary to fold the heap back, if the final
configuration pattern contains list object in the more abstract format.
   As a particular case let us consider the original example of mem cell 118, when 𝐴 is (or becomes)
the empty list. In this situation the entry 𝑥 ↦→ list (𝐴) should be removed from the heap since the
list does not occupy any cell and a constraint stating 𝑥 = 0 should be added (to be consistent with
C semantics).

A.3     Increasing compositionality in memory management
In Section 6.2 we have emphasized that the intrinsically sequential program execution may compel
to concentrate most of the computational effort in the syntactic nodes close to the root, with
serious risks of loss of efficiency, mainly during incremental re-evaluation. In that section we
mentioned a few techniques to “compact” reachability rules propagated from children nodes onto a
sort of “macro reachability rules” forwarded to the father node. In this appendix we detail a further
technique to avoid delaying many execution steps towards the root of the syntax tree. Precisely,
notice that the previous memory access operations need a complete knowledge of the memory

, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                          :57

contents at the time of their execution; such a knowledge is available if we are executing a function
provided with suitable preconditions or a loop provided with an invariant, but it is lacking if such
annotations are missing.
   In such a case, we model the initial memory contents of the code fragment with a dummy array
term [42] 𝑒 added to the mem cell, which can be used to handle memory reads and writes. The mem
cell will also contain the map between memory addresses and contents of the memory locations
allocated during the execution, which would have a known address independent on the rest of the
heap. Thus, memory operations are specified along the following reachability rules.
   Read/write. We handle the read operation in two ways depending on whether the address belongs
to the newly allocated part or not. In the former case, as specified by semantic rule (123), a normal
read is performed.
                                                                     
                                   read (𝑖)
                                            . . . ⟨𝑒, 𝑖 ↦→ 𝑗 . . . ⟩𝑚𝑒𝑚                          (123)
                                       𝑗           𝑘
Otherwise the result of such read is the term read ( 𝑗, 𝑒) which depends on the dummy environment
variable 𝑒:                                                                     
                           read (𝑖)
                                    . . . ⟨𝑒 . . . ⟩ mem ∧ 𝑖 ≠ 0 ∧ 𝑗 = read (𝑖, 𝑒)           (124)
                              𝑗            𝑘
Note that the read array term (read (𝑖, 𝑒)) is an assumption we make on the state of the heap at the
beginning of the execution. This assumption must be discarded at the end of execution by adding a
suitable precondition to the generated rules.
  Similarly, write operations are specified by rule (125) when they are applied to newly allocated
variables:                                                          
                                 write(𝑖, 𝑗)                ℎ
                                              ...    𝑒, 𝑖 ↦→ . . .                             (125)
                                      ·            𝑘        𝑗        mem
Otherwise the operation is stored inside the term write(𝑖, 𝑗, 𝑒), which keeps track of the sequence
of operations on memory.
                                                                    
                              write(𝑖, 𝑗)             𝑒
                                          ...                   ...                            (126)
                                   ·           𝑘 write(𝑖, 𝑗, 𝑒)      𝑚𝑒𝑚

   When performing read and write operations on the heap, the functional composition of terms
related to the read and write operations are always simplified by applying the array theory proposed
in reference [42].
                            ∀𝑖, 𝑗, 𝑙, 𝑒.write(𝑖, 𝑙, write(𝑖, 𝑗, 𝑒)) = write(𝑖, 𝑙, 𝑒)            (127)
                 ∀𝑖, 𝑗, 𝑙, 𝑒.𝑖 ≠ 𝑗 → write(𝑖, 𝑙, write( 𝑗, 𝑙, 𝑒)) = write( 𝑗, 𝑙, write(𝑖, 𝑙, 𝑒))                  (128)
                                     ∀𝑖, 𝑗, 𝑒.read (𝑖, write(𝑖, 𝑗, 𝑒)) = 𝑗                                        (129)
Equation (127) states that if two nested writes are performed over the same address, only the last
one must be considered, while the previous one can be removed. Equation (128) states that write
occurring at different addresses can be switched and equation (129) states that the value of a read
at the same address of a write holds the last written value.
   Malloc/free. The malloc(𝑖) is handled by adding a new mapping between memory addresses and
location contents (using reachability rule (95)), since the newly generated addresses will never
collide with the older ones. The free operation, instead, can only be handled if the address to be
freed belongs to the new part of memory.

                                                                  , Vol. 1, No. 1, Article . Publication date: June 2026.
:58    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

                                                              ○
                                                              95
                                                              exp


                                      ○
                                      96                        ○
                                                                97                 ○
                                                                                   98
                                   postfix_exp                  ‘=’            postfix_exp


                             ○
                             102                 ○
                                                 103                     ○
                                                                         106                 ○
                                                                                             107
                        IDENTIFIER        postfix_exp1                IDENTIFIER      postfix_exp1


                                         ○
                                         104           ○
                                                       105                           ○
                                                                                     108           ○
                                                                                                   109
                              x         ‘->’ IDENTIFIER                   p         ‘->’ IDENTIFIER




                                                       next                                        next

                    Fig. 21. Subtree representing the statement at line 12 of the swap function


   A.3.1 Fixing the heap. Once the final configuration patterns have been obtained, the precise
conditions of the heap state at the beginning must be met. First, all the memory locations affected
by a read or a write must be disambiguated, obtaining the set of distinct memory locations by
splitting undefined addresses, potentially generating new configuration pattern. Then it is possible
to build the full heap of the initial configuration pattern. The unknown heap obtained in the final
configuration pattern is taken and all the write operations are removed, by transforming a heap in
the form write(𝑖, 𝑗, 𝑒) to 𝑒 and producing a pair 𝑖 ↦→ 𝑗 until the resulting heap does not contain any
write operations. All this pairs are added to the initial configuration pattern heap cell. Finally all
the read operation terms in the final configuration can be resolved as before providing a symbolic
value.
   Notice that the technique illustrated in this appendix introduces some level of compositionality
even in case of code fragments partially annotated or with no annotations. In particular, portions of
identical computations, where the unknown initial memory contents are represented by symbolic
parameters, can be saved and further reused when instantiating such parameters to concrete values.

A.4     Attribute evaluation
We illustrate how attributes are evaluated for the most significant subtrees of the example shown
in figure 9 in section 5. We recall that throughout the example we use the abbreviations for
code/environment snippets shown in figure 11 on page 27; the reachability rules used for attribute
evaluation are shown in Table 3 on page 30, with a reference to the nodes where they are generated.
   Node 95 (figure 21): variable evaluation and assignment. The semantics is expressed by reachability
rule instance (50), which performs the assignment of value p->next to x->next. This rule instance
relies on both the computation of the actual destination address and on the evaluation of p->next.
   Since pointers are involved, memory operations must be considered; we use memory primi-
tives25 read and write to access and modify memory. Operation read (𝑖) retrieves the value stored
at address 𝑖 in cell mem; its semantics is defined by reachability rule instance (49) in table 3. Note
that the type 𝑡 of address 𝑖 is used to specify the type of the value 𝑗, to guarantee that the memory
25 In this example we show a simplified version of the memory write rules; see appendices A.1 and A.2 for the complete

formalization.


, Vol. 1, No. 1, Article . Publication date: June 2026.
Syntax-driven Incremental Program Verification of Matching Logic Properties                                             :59

                                                     ○
                                                     101
                                                     stm

                                               ○
                                               120          ○
                                                            121
                                          ‘return’              id

                                                            ○
                                                            122
                                                      IDENTIFIER



                                                                p

                Fig. 22. Subtree representing the statement at line 14 of the swap function


                                                           ○
                                                           51
                                                     relat_exp

                                          ○
                                          69                ○
                                                            77            ○
                                                                          78
                                       add_exp              ‘<’       postfix_exp

                                                                          ○
                                                                          79
                                x->next->val - x->val                  Constant



                                                                            0

                Fig. 23. Subtree representing the statement at line 10 of the swap function



location contains a value of the expected type. Operation write(𝑖, 𝑗) modifies the mem cell by
writing value 𝑗 at address 𝑖; its semantics is defined by reachability rule instance (47), which writes
to memory by replacing the previous value stored at address 𝑖 with value 𝑗.
   Reachability rule instance (45) in table 3 describes the evaluation of variable x. It looks up for
variable x in memory and places it as a variable in cell 𝑘. The value of x is a tuple consisting of
the variable type and its actual value. Both tuple elements are used in the evaluation, since they
are needed to compute the actual addresses of fields val and next. Reachability rule instance (46)
works in the same way for variable p. Reachability rule instance (45) (and (46)) are propagated from
nodes 102 and 106, respectively.
   The reachability rule instance responsible for computing the offset of the struct field next in
variable x is generated inside the struct listNode definition.

   Node 101 (figure 22 ): return. Its semantics is defined by reachability rule instance (48) in table 3.
The rule leaves in cell 𝑘 the address pointed by p (represented by the tuple (𝑡, 𝑖)). The evaluation of
p is handled by reachability rule instance (46), which is received from node 121.

   Node 51 (figure 23): if statement. The evaluation of the condition of this statement requires to
retrieve the values of x->next->val and x->val, which are obtained through reachability rule
instances (45) and (49) in table 3. The fields val and next are evaluated with the reachability rules
from the struct definition. Reachability rule instance (52) performs the actual subtraction between
the two variables.

                                                                     , Vol. 1, No. 1, Article . Publication date: June 2026.
:60    Domenico Bianculli, Antonio Filieri, Carlo Ghezzi, Dino Mandrioli, and Alessandro M. Rizzi

                                                                     ○
                                                                     36
                                                                parameter


                                                    ○
                                                    37                  ○
                                                                        40        ○
                                                                                  41
                                                   type                 ‘*’        id

                                             ○
                                             38             ○
                                                            39                    ○
                                                                                  42
                                         ‘struct’ IDENTIFIER                   IDENTIFIER



                                                          listNode                  p

                    Fig. 24. Subtree representing the statement at line 8 of the swap function

                                                           ○
                                                           5
                                                   struct_field_list


                                     ○
                                     6                                          ○
                                                                                7
                                 parameter                                struct_field_list


                              ○
                              10           ○
                                           12                                   ○
                                                                                13
                              type    IDENTIFIER                              parameter

                              ○
                              11                                 ○
                                                                 14                 ○
                                                                                    17        ○
                                                                                              18
                             ‘int’                               type               ‘*’       id

                                                           ○
                                                           15             ○
                                                                          16                  ○
                                                                                              19
                                                     ‘struct’ IDENTIFIER                  IDENTIFIER

Fig. 25. Excerpt from the abstract syntax tree in Fig. 12, corresponding to the declaration of struct listNode
(lines 3–6 in Fig. 9)


  Node 36 (figure 24): declaration of variable p. The variable declaration is performed through
reachability rule instance (62), which adds to cell env variable p as a pointer to a struct listNode
holding an undefined value.
   Node 5 (figure 25): definition of a struct. To handle struct fields data, nodes of type parameter have
an attribute 𝑁 containing a pair (name, type). Nodes of type struct_field_list have two additional
attributes: 𝑆, an integer containing the size of the struct; 𝐹 , a list of tuples (one for each field of
the struct) of the form (name, type, offset). The former is used to generate the rule instances that
evaluate the sizeof operator for the struct. The latter is used to build the rule instances that
retrieve the field offsets.
   Reachability rule instances (68) and (69) compute, respectively, the offsets of fields val and next
of the listNode struct. Reachability rule instance (70) is used to evaluate the sizeof operator
for the listNode struct.
   The complete attribute evaluation is available in table 2 on page 29.




, Vol. 1, No. 1, Article . Publication date: June 2026.
