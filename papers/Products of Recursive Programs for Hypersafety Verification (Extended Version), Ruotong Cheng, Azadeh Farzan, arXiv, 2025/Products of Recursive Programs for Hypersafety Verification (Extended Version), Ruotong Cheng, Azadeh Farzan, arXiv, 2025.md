                                         Products of Recursive Programs for Hypersafety Verification
                                         (Extended Version)

                                         RUOTONG CHENG, University of Toronto, Canada
                                         AZADEH FARZAN, University of Toronto, Canada
                                         We study the problem of automated hypersafety verification of infinite-state recursive programs. We propose an
                                         infinite class of product programs, specifically designed with recursion in mind, that reduce the hypersafety
                                         verification of a recursive program to standard safety verification. For this, we combine insights from language
arXiv:2504.10800v2 [cs.PL] 23 Aug 2025




                                         theory and concurrency theory to propose an algorithmic solution for constructing an infinite class of recursive
                                         product programs. One key insight is that, using the simple theory of visibly pushdown languages, one can
                                         maintain the recursive structure of syntactic program alignments which is vital to constructing a new product
                                         program that can be viewed as a classic recursive program — that is, one that can be executed on a single
                                         stack. Another key insight is that techniques from concurrency theory can be generalized to help define
                                         product programs based on the view that the parallel composition of individual recursive programs includes
                                         all possible alignments from which a sound set of alignments that faithfully preserve the satisfaction of the
                                         hypersafety property can be selected. On the practical side, we formulate a family of parametric canonical
                                         product constructions that are intuitive to programmers and can be used as building blocks to specify recursive
                                         product programs for the purpose of relational and hypersafety verification, with the idea that the right
                                         product program can be verified automatically using existing techniques. We demonstrate the effectiveness of
                                         these techniques through an implementation and highly promising experimental results.
                                         CCS Concepts: • Software and its engineering → Software verification; • Theory of computation →
                                         Logic and verification; Concurrency; Grammars and context-free languages.
                                         Additional Key Words and Phrases: hyperproperties,product programs,reductions,visibly pushdown languages
                                         This article is an extended version of:
                                         Ruotong Cheng and Azadeh Farzan. 2025. Products of Recursive Programs for Hypersafety Verification. Proc.
                                         ACM Meas. Anal. Comput. Syst. 9, OOPSLA2, Article 382 (October 2025), 29 pages. https://doi.org/10.1145/
                                         3763160

                                         1   Introduction
                                         Hyperproperties [16] are properties expressible over multiple runs of a program. A 𝑘-safety property
                                         is a property whose violation is witnessed by 𝑘 finite-length program runs. Determinism is an
                                         example of such a property: non-determinism can only be witnessed by two runs of the program
                                         on the same input that produce two different outputs. This makes determinism an instance of a
                                         2-safety property. A hypersafety property is a 𝑘-safety property for 𝑘 > 1.
                                            Verification of hypersafety properties was first achieved by reducing the problem to a standard
                                         safety verification by means of self-composition [8]. For example, in order to verify that 𝑃 is
                                         deterministic, one can verify that 𝑃; 𝑃 ′ under the assumption of equivalent inputs for 𝑃 and 𝑃 ′
                                         guarantee the equivalence of their outputs at the end, where 𝑃 ′ is a fresh copy of 𝑃 with a disjoint
                                         memory. It was argued in [8] that any other independent composition operator can be used in
                                         place of the sequential composition operator. Later, cross products [58], which combine 𝑃 and 𝑃 ′
                                         synchronously in lockstep, were used in a more limited setup of compiler validation. Program
                                         products [7] were introduced as combining the two notions where one can fuse the two programs
                                         both synchronously and asynchronously where appropriate.
                                            It is now well-established that product programs are vital to verification of hypersafety properties
                                         and relational reasoning in general [14, 27, 38, 52, 53]. In algorithmic verification, they permit
                                         Authors’ Contact Information: Ruotong Cheng, University of Toronto, Toronto, Canada, chengrt@cs.toronto.edu; Azadeh
                                         Farzan, University of Toronto, Toronto, Canada, azadeh@cs.toronto.edu.
2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         Ruotong Cheng and Azadeh Farzan


the use of existing tools and techniques for classic safety verification of sequential programs to
be applied to hypersafety verification. This is mainly due to the fact that they accommodate the
creation of instances that admit simpler proofs. Approaches to hypersafety or relational verification
typically implicitly or explicitly define a state space of product programs that may be used to simplify
verification. For instance in [7, 53], a successful derivation of the underlying logical rules implicitly
defines the verified product program, while in [26], the product programs are syntactically defined
and look like classic programs. With the implicit construction, since the choice of application of
a proof rule and the next alignment step are combined and one typically has control over the
entire verification stack, one can opt for an ergonomic design that works more effectively; e.g.,
heuristics for proofs search can be tuned to the specific problem. On the other hand, since the
explicit construction decouples the construction of the program from the construction of the proof,
it can benefit from improvements in standard verification tools. More importantly, having access
to a concrete (product) program opens up possibilities for using other standard tools for program
analyses such as symbolic/concolic execution, fuzzing, monitoring and/or repair, and static analyses.
The two sets of techniques are therefore complementary and serve different use cases. In this paper,
we are interested in the explicit construction of product programs.
   This problem is somewhat well-studied for iterative programs, but has only been lightly studied
in the context of recursive programs, and the majority of the proposed techniques fit in the implicit
construction category. Most even bypass the program view entirely and considers the question
of how a similar concept can be incorporated in the CHC (Constrained Horn Clauses) encoding
of them, in the form of CHCproduct [47] or fold/unfold [4, 20] techniques to implicitly explore
the space of the product programs and proofs simultaneously (more details in Section 9). The very
few [22] that construct explicit product programs use specialized constructions that help solve a
limited set of verification instances.
   Consider the recursive code illustrated in Figure 1, which def div(n: nat, d: nat) -> nat
                                                                 <latexit sha1_base64="4962dsqH/Gd8W0IOqE13rri/K00=">AAAGBnicjZRbT9RAFIAL7CquN9A3fZm4IYFYSHeNaIhrUBLlEUUuye4Gp9PTZWRmWmamwKbpu7/GN+Or/8En/42n3YIsu2GZpunJOec7t86MHwturOf9nZqeqVRv3Z69U7t77/6Dh3Pzj3ZNlGgGOywSkd73qQHBFexYbgXsxxqo9AXs+UcbuX3vBLThkfpi+zF0Je0pHnJGLaoO5mf+LHSEsSKigaCql9AemLS9fUh13N1wt6hhVGS1wseATUOu0RlztZquoKX40j1HW2k8ILLaOXFhehdQt0auLIZBTBSG6NnyRs3YGWfG9gW0OtaGVHLR7/jorTmYUfcj6J9GOiiBYjipLxLILuBRxljNVW8I0RBcR7BISlB2COlpAHUdJCMNJdhqi2675PBvoIZm3bRTz64fT8MlY6OeN91KDRy7XNkxccYN5gOyxn4sCh8T+nLq5sTUAYSuACmpi3+fuYiCti4ok2ASV9IzV3LlEkVvWt1nCHZ5JMBOqu3FxNo2I4mPjg+5kduJvGEBe1wE21bTUx+07k+qwqvhjvehx1WanyY8t7ipshqOhQT8ZFGt5a27JCi+S2T5bf7NI/KQKPImN2iwiVbEy7UgDKyRY9Ia0GSZBAgvkeek8b+MEjiudUAFQ2kP5ureilcsMio0SqHulGvrYH7qSSeIWJJvz6KtdsOLbTel2nImAHtLDMSUHeF2baOoqATTTYtJZWQBNQEJI42vsqTQXiZSKo3pSx89JbWH5qotV46ztRMbvu6mXMWJBcUGicJEEBuR/C7D4eChsqKPAmWaY62E4c1FmcUbbyhLORoz3ElwwmNT9nI2aGaIshxNGU6zcXV2o8Juc6WxurL6qVlff1/OddZ56jxzFp2G88pZdzadLWfHYZW1ytcKr3yrfq/+qP6s/hq4Tk+VzGNnaFV//wMsHtPQ</latexit>




computes the integer result of dividing the numerator n                if n < d: return 0
by the denominator d. Assume that we want to check if                  else: q = div(n - d, d) + 1
                                                                               return q
this implementation satisfies the following property of the
original mathematical function:                                       Fig. 1. Recursive integer division.

                        𝑛 ≤ 𝑛 ′ =⇒ div(𝑛, 𝑑) ≤ div(𝑛 ′, 𝑑)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             (monotonicity)
First, observe that monotonicity is a 2-safety property. The most straightforward encoding for
solving the monotonicity property uses self-composition, that is, it reduces the problem to the
safety verification of div(n, d); div(n′, d′ ). However, this instance cannot be verified by an existing
automated solver due to the nonlinearity of the arithmetic reasoning involved in guessing the
required inductive function summaries [30]. In particular, the summary must precisely capture that
div(n, d) is the integer division function.
   Product programs are conceptually straightforward when it comes to non-recursive code. How-
ever, recursion introduces significant additional complexity. If 𝑃 and 𝑃 ′ are recursive, then 𝑃; 𝑃 ′
is a recursive program in the standard sense. However, the same cannot be said for an arbitrary
product program made from 𝑃 and 𝑃 ′ (even if 𝑃 ′ is a copy of 𝑃). For instance, it is well-known that
the parallel product of two recursive programs is a 2-stack machine, whose syntactic traces form a
context sensitive language [37], which does not correspond to a recursive program. This problem
does not exist in the iterative setting.
   For monotonicity, the programmer’s intuition points to a lockstep (or synchronous) product
program, namely one in which the two recursive codes are executed in tandem, when possible.
An appropriate product program then is one that (1) looks like a classic (single stack) recursive
program, and (2) simulates the two copies of div in tandem. This product program can be defined
Products of Recursive Programs for Hypersafety Verification                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              3


using four recursive functions: div1 and div2 as two distinct copies of div from Figure 1, and two
distinct copies of the variation illustrated in Figure 2. In a lockstep simulation we need to execute
in tandem while both copies last, and then a given copy alone when the other copy has terminated.
div12 assumes that the second copy is still running and as such calls it in tandem, while div1
assumes that the second copy has terminated and only locally recurses.

def div12(n1, d1, n2, d2) -> (nat,nat)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          def div21(n2, d2, n1, d1) -> (nat,nat)
<latexit sha1_base64="nJUI9/+HNN+KIi9Xdzn1+WqfuQY=">AAAGTHicjVRbT9RAFC66i7jeQJ/Ul4kbEogDaWtEY1yDkiiPKHJJdjdk2p4uE2amZWYKbJpN/DW+6i/x3f/hmzHxtFsIy26AaSY5Pef7zjnzzSVIBTfWdX9P3bhZq0/fmrnduHP33v0Hs3MPt02S6RC2wkQkejdgBgRXsGW5FbCbamAyELATHKwV8Z0j0IYn6qvtp9CVrKd4zENm0bU3V3s83xHGioRFgqlexnpg8vbmPtNpd41uMBMyMWiUGAM2j7lGMNZq+VSwynxJT6mtPB0yBo1TxlnofcRog1wYISYxSRwjsuWOh3FlPDS2L6DVsTZmkot+J0C05mDG4QfQP050VBFKcfJAZDA4I49zjNVc9UYoGqLLGGEiJSg7QulpAHUZSSYaKmKrLbrtioe7gR426Oad5uByeTxKJmY9XXQrN3BIubI04keePyHbJHk+YgZjP5XtTyhwvgH/ygawsE8jiKkAKRnFgxBS5IO2FJTJsBKV7IRKrihRzF6zxS8QbfNEgL2qwRdXNrieSPx0us+N3MxkoZTvXbONHS6iTavZcQBa96/qxW3gFQigx1VeXC+8yHjKBg0Uh5Tbs6BwPyOcCmWN/EWy9I4soCYU5yJm5jFRHnmLkDfk0CetgoWkClyW1mAzrYhLEYAOEAYKLP56Fd6rCLTItVSWi7zF82SEPidemaEDKhrpdW+26S675SDjhlcZTacaG3tzU086URJmxSEvtWh7bmq7OdOWhwJQkMxAysIDPPRtNBWTYLp5Ke+AzKMnInGicSpLSu95Rs6kMX0ZIFIyu28uxgrnpFg7s/Hrbs5VmllQ4bBQnAliE1K8iKgUXk0r+miwUHPslYT4/rHQ4rs5UqWSxoyuJDriqanWcjJczAjLcgwNUE3vonbjxra/7K0sr3z2m6sfKl1nnKfOM2fB8ZxXzqqz7mw4W05Y+1b7XvtR+1n/Vf9T/1v/N4TemKo4j5yRMT39H0ei5XM=</latexit>                                                                      <latexit sha1_base64="KWBEkziJrfRbpUuIpkUUPdylrNk=">AAAGT3icjVRbTxNBFF6wRag30Df1YWJDAnEg3TWiIdagJMojilyStiGzu2fLhJnZZWYWaDb75K/xVX+Jj/4S34yny5ZQ2lCmmeT0nO87l29nxk8EN7bR+DM1fadSnbk7O1e7d//Bw0fzC4/3TJzqAHaDWMT6wGcGBFewa7kVcJBoYNIXsO8fb/bj+6egDY/VN9tLoCNZV/GIB8yi63Ch8nyxLYwVMQsFU92UdcFkrZ0jppPOJt1mJmAirxUYAzaLuEYw1mp6VLDSfE0H1GaWXDDy2oBxGfoQMloj11aASUwcRYhsNkbDOBkPjO0JaLatjZjkotf2Ea05mFH4MfTOYh2WhEKczBcp5JfkUY6xmqvuEEVDeBMjiKUEZYcoXQ2gbiLJWENJbLZEp1Xy8Gugh+WdrF3Pb5bHpWRs1sHQzczACeXKUhLyU9cbk26cPp8whbGfi/7HVLjagTexg35hLA8RFSAlo3gUAooJQFsKyqRYikp2TiVXlChmb9njVwj3eCzATurw1cQOt2KJP50ccSN3UkmxY8+9ZRv7XIQ7VrMzH7TuTeqlUcNL4EOXq6x/wfAq4znLaygOKYouKdQzxK36krnLZOU9WUJNKO5lzMwjojzyDiHrhJy4pFl81qUBuqitwaZakQZFADpAGFhHE/96Jd4rCbSfbKWoF3rLV8kIfUncIkMbVDjU7OF8vbHaKBYZNdzSqDvl2j5cmHraDuMg7Z/zQoyW20hsJ2Pa8kAAKpIaSFhwjOe+haZiEkwnK/TNySJ6QhLFGreypPBeZWRMGtOTPiIls0fmeqzvHBdrpTZ628m4SlILKrgoFKWC2Jj0H0VUCm+nFT00WKA59koCfAJZYPHpHKpSSmOGJwlPeWLKWc4vhhliWY6hHNV0r2s3aux5q+7a6toXr77xsdR11nnmvHCWHNd542w4W862s+sEle+VH5WflV/V39W/1X8zJXR6qjSeOENrZu4/PDDk7w==</latexit>




  if n1 < d1: q2 = div2(n2, d2)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   if n2 < d2: q1 = div1(n1, d1)
    return 0, q2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    return 0, q1
  else: q2, q1 = div21(n2, d2, n1 - d1, d1)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       else: q1, q2 = div12(n1, d1, n2 - d2, d2)
    return q1 + 1, q2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               return q2 + 1, q1

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             Fig. 2. With two disjoints copies of div, these functions simulate a synchronous product of two div’s


   This product program does not syntactically match the one that we formally define and algorith-
mically construct in this paper, but it is more human-readable and conveys the two main ideas: (1)
our product programs are syntactic in the sense that any syntactic run of it is identical to a syntactic
run of the full (parallel) product of two distinct copies of div (not strictly true for this simplified
example), and (2) even in the simplest case, they are far from trivial. How can one systematically
construct such a program?
   In [26–28], this is achieved for iterative (non-recursive) programs, by taking an operational view
of the program [25]. The set of all possible alignments are defined by the parallel composition of the
components, which include arbitrary interleavings of syntactic runs from individual components.
Then, a particular choice of product programs becomes about selecting a sound subset of these
interleavings. As long as the subset has a finite representation (in a program or program-like
structure), the product program and this set of behaviours are interchangeable.
   Our first important observation is that, for the same operational style to work for recursive
programs, one has to be explicitly conscious of the structure of the recursive runs,                 ⌧0
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        <latexit sha1_base64="8NA2bcS7DdmpSEu6gqypInG+fKU=">AAAB7HicbVBNS8NAEJ3Ur1q/qh69LBbRU0lEqseiF48VTFtoQ9lsN+3SzSbsToRS+hu8eFDEqz/Im//GbZuDtj4YeLw3w8y8MJXCoOt+O4W19Y3NreJ2aWd3b/+gfHjUNEmmGfdZIhPdDqnhUijuo0DJ26nmNA4lb4Wju5nfeuLaiEQ94jjlQUwHSkSCUbSS30WanffKFbfqzkFWiZeTCuRo9Mpf3X7CspgrZJIa0/HcFIMJ1SiY5NNSNzM8pWxEB7xjqaIxN8FkfuyUnFmlT6JE21JI5urviQmNjRnHoe2MKQ7NsjcT//M6GUY3wUSoNEOu2GJRlEmCCZl9TvpCc4ZybAllWthbCRtSTRnafEo2BG/55VXSvKx6tWrt4apSv83jKMIJnMIFeHANdbiHBvjAQMAzvMKbo5wX5935WLQWnHzmGP7A+fwBhmuOhA==</latexit>




                                                                                                ⌧                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       <latexit sha1_base64="1Lym2pIKMt9vtZz8fhSf8X6lEpk=">AAAB63icbVBNS8NAEJ3Ur1q/qh69BIvgqSQi1WPRi8cK9gPaUDbbTbt0dxN2J0IJ/QtePCji1T/kzX/jps1Bqw8GHu/NMDMvTAQ36HlfTmltfWNzq7xd2dnd2z+oHh51TJxqyto0FrHuhcQwwRVrI0fBeolmRIaCdcPpbe53H5k2PFYPOEtYIMlY8YhTgrk0QJIOqzWv7i3g/iV+QWpQoDWsfg5GMU0lU0gFMabvewkGGdHIqWDzyiA1LCF0Ssasb6kikpkgW9w6d8+sMnKjWNtS6C7UnxMZkcbMZGg7JcGJWfVy8T+vn2J0HWRcJSkyRZeLolS4GLv54+6Ia0ZRzCwhVHN7q0snRBOKNp6KDcFfffkv6VzU/Ua9cX9Za94UcZThBE7hHHy4gibcQQvaQGECT/ACr450np03533ZWnKKmWP4BefjGyS/jlM=</latexit>




in terms of the matching of calls and returns in each component. To visualize this,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      ( ...( ...) ...)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   [ ...[ ...[ ...] ...] ...]


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         <latexit sha1_base64="yJpFNgSkj2rDSizSEWNgNiJ4qqo=">AAACFnicdZDLSsNAFIYn9VbrLepK3AwWoW5C0krT7opuXFawF2hDmUwn7dDJhZmJUELxNXwBt/oG7sStW1/A53DSpmBFDwzn5zvncOb8bsSokKb5qeXW1jc2t/LbhZ3dvf0D/fCoLcKYY9LCIQt510WCMBqQlqSSkW7ECfJdRjru5Dqtd+4JFzQM7uQ0Io6PRgH1KEZSoYF+UoL9YSgFXOaLZR7oRdOw7Xr50oamYc5DiUqtXqnXoJWRIsiiOdC/1CSOfRJIzJAQPcuMpJMgLilmZFbox4JECE/QiPSUDJBPhJPMT5jBc0WG0Au5eoGEc/pzIkG+EFPfVZ0+kmPxu5bCv2q9WHo1J6FBFEsS4MUiL2ZQhjD1Aw4pJ1iyqRIIc6r+CvEYcYSlcm1lS4oVnCljltfD/0W7bFhVo3pbLjauMovy4BScgRKwgA0a4AY0QQtg8ACewDN40R61V+1Ne1+05rRs5hishPbxDWUInmw=</latexit>
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     <latexit sha1_base64="NRrx8vbuvh/gX6y502/VEGSthII=">AAACJ3icdVDLSsNAFJ3UV62vqEs3g0UQFyGJIW13RTcuK9gHpKFMppN26OTBzEQopf/gb/gDbvUP3Iku3fgdTtoKtuiB4R7OvYc79wQpo0Ka5odWWFvf2Nwqbpd2dvf2D/TDo5ZIMo5JEycs4Z0ACcJoTJqSSkY6KScoChhpB6PrvN++J1zQJL6T45T4ERrENKQYSSX19AsPdvuJFHC1+svVh7Cnl03DdG2nZkPTcJyqW3MVqTgVy72ElmHOUAYLNHr6l7LiLCKxxAwJ4VlmKv0J4pJiRqalbiZIivAIDYinaIwiIvzJ7KYpPFNKH4YJVy+WcKb+dkxQJMQ4CtRkhORQrPZy8a+el8mw6k9onGaSxHi+KMwYlAnMA4J9ygmWbKwIwpyqv0I8RBxhqWJc2pLLSpyqYH6uh/+Tlm1YruHe2uX61SKiIjgBp+AcWKAC6uAGNEATYPAAnsAzeNEetVftTXufjxa0hecYLEH7/AbL5aV0</latexit>




consider runs 𝜏, 𝜏 ′ illustrated on the right, as being runs of the two disjoint copies
div(n, d) and div(n′, d′ ) respectively. Open and closed brackets respectively denote
calls and returns, and all internal actions are represented as the ellipses, since their
specifics are unimportant. Note that each illustrated run is well-nested, in the sense that
we have a balanced sequence of calls and returns. These are also called interprocedurally
realizable paths [50, 51].
   Below we can see two (of the many) ways that one can interleave (or align) 𝜏 and 𝜏 ′ :
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              [. . . [. . . (. . . (. . . [. . . . . . ] . . . ) . . . ) . . . ] . . . ]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     (well-nested)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              [. . . [. . . (. . . (. . . [. . . . . . ) . . . ) . . . ] . . . ] . . . ]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       (ill-nested)
and we contend that the well-nested run belongs to a product program and the ill-nested one does
not. In the well-nested one, the matched calls and returns belong to the same component from
which they originated. If we ignore the types/colours, we can pretend that the former is a well-
matched run of a classic recursive program, whereas in the latter, we obtain an interprocedurally
unrealizable path: a call and a non-matching return. Therefore, to construct a product program in
this operational style, one needs (1) representations for syntactic program runs that maintain the
recursive structure, and (2) mechanisms to isolate sound appropriate subsets of the well-nested
alignments as product programs.
   For (1), we lean on the well-established theory of visibly pushdown languages [2] to formally
represent the syntactic runs of recursive programs, while retaining the recursive structure in
4                                                                        Ruotong Cheng and Azadeh Farzan


the runs. Unlike a call graph, a classic model for recursive program analysis, a visibly pushdown
grammar or automaton captures the well-matched syntactic runs of a recursive program. We then
give a construction of the product program in the same formalism, which guarantees that it can be
treated as a classic recursive program for all intents and purposes.
   To understand the complications of devising (2), let us further expand our simple div example
with a slightly more complicated property:

                             𝑛 = 2 × 𝑛 ′ =⇒ div(𝑛, 𝑑) ≥ 2 × div(𝑛 ′, 𝑑)                      (scaling)

where scaling is a 2-safety property. Observe that a lockstep product is no longer appropriate.
For scaling, we expect the execution of the first copy to be twice as long as the second copy. A
suitable product program, therefore, must synchronize each recursive call of div(n, d) against two
recursive calls of div(n′, d′ ). Consider a variation of this property where the scale factor changes
from 2 to a different constant, like 5, which immediately changes the product program needed
for its verification to a new one. This motivates the following research question: how can one
systematically define a state space of useful product programs for recursive programs for the
purpose of relational and hypersafety verification? Any specific choice of a product program can
be viewed as a reduction of the set of all alignments (or the behaviours of the parallel product). For
a group of 𝑘 syntactic runs, one from each individual component, a (minimal) reduction includes
precisely one alignment of them, and discards all others. For recursive programs, with syntactic
runs of unbounded length, there are infinitely many choices that can be made and as such infinitely
many reductions that can be defined.
   Our key (theoretical) contribution in this paper is to define an infinite space of product programs
(reductions). Each reduction is representable as standard recursive programs and therefore can be
proved correct using standard verification techniques. Each member of this space is then formally
definable and algorithmically constructible, and the set is countable and (recursively) enumerable,
in the same style as [27, 28].
   To define the state space of these programs, we rely on the observation that the task of choosing
one alignment from a group is like scheduling. Intuitively, one can think of the resolution of the
nondeterminism to be done through the choices made by a scheduler. Most importantly, we observe
that these schedulers can also be modelled in the same formalism as recursive programs. Given a set
of statements, coming from distinct components, one can formally define a set of schedules (which
are basically sequences over these statements), which can then serve as a restriction of the set of
all alignments. For instance, a lockstep scheduler of two (distinct) components can be viewed as
one that admits any schedule alternating statements from the two components. Construction of a
reduction then becomes a standard intersection of the set of schedules defined by the scheduler and
the well-nested shuffle of the components; a construction that is supported by the theory of visibly
pushdown languages for both automata and grammars. In Section 3, we formalize these schedulers as
contextual lexicographical orders and the yielded reductions as contextual lexicographical reductions,
lex reductions for short. Here, context refers to the fact that the schedule is stateful and adjusts its
future choices based on what it has done in the past. These can be viewed as generalization of
similar concepts from [26–28] to recursive programs.
   We use ideas from trace theory [46] (a simple theory for concurrency) to argue that our reductions
are constructible. However, in Section 4, we propose a new optimized algorithm for constructing
a representation of our contextual lexicographic reductions as visibly pushdown automata and
grammars. The new construction leverages the fact that, in the context of hypersafety (and relational)
verification, we have the full commutativity of the actions from different components, to propose a
simpler and more compact construction of visibly pushdown (VP) lex reductions.
Products of Recursive Programs for Hypersafety Verification                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              5


   The specific feature of our proposed space
                                                                                   • uncountable
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            <latexit sha1_base64="8NbaOzqMoqJ5f8VpwOppcGm7bBM=">AAACCHicdVDLSgMxFM3UV62vqks3wSK4KjMtVnFVcOOygn1AO5RMmmlDM8mQ3BHK0B9w71Z/wZ249S/8Az/DTFuhFT0QOJxzLvfmBLHgBlz308mtrW9sbuW3Czu7e/sHxcOjllGJpqxJlVC6ExDDBJesCRwE68SakSgQrB2MbzK//cC04UrewyRmfkSGkoecErBSN5FUJRKIjfeLJa/szoDdJVJxL6pV/GOV0AKNfvGrN1A0iZgEKogxXc+NwU+JBk4FmxZ6iWExoWMyZF1LJYmY8dPZyVN8ZpUBDpW2TwKeqcsTKYmMmUSBTUYERua3l4l/ed0Ewis/5TJOgEk6XxQmAoPC2f/xgGtGQUwsIVRzeyumI6IJBdvSypZMtuIU4+Vq/ietStmrlWt3lVL9elFSHp2gU3SOPHSJ6ugWNVATUaTQE3pGL86j8+q8Oe/zaM5ZzByjFTgf36QrmrE=</latexit>




                                                             All Reductions
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       <latexit sha1_base64="BSf0CLajyw/hxzl49XeaVBxcTNI=">AAACBHicdZDLSgNBEEVrfMb4irp00xgEV2Em0SiuAm5cRjAPSIbQ06lJmvQ86O4RwpCte7f6C+7Erf/hH/gZ9iQREtGChsu5VVT19WLBlbbtT2tldW19YzO3ld/e2d3bLxwcNlWUSIYNFolItj2qUPAQG5prge1YIg08gS1vdJP5rQeUikfhvR7H6AZ0EHKfM6oNanW9RAjUvULRKdnTIvaCKNsXlQr5sYowr3qv8NXtRywJMNRMUKU6jh1rN6VScyZwku8mCmPKRnSAHSNDGqBy0+m5E3JqSJ/4kTQv1GRKFydSGig1DjzTGVA9VL+9DP7ldRLtX7kpD+NEY8hmi/xEEB2R7O+kzyUyLcZGUCa5uZWwIZWUaZPQ0pYMGzghZDGa/0WzXHKqperdebF2PQ8pB8dwAmfgwCXU4Bbq0AAGI3iCZ3ixHq1X6816n7WuWPOZI1gq6+MbOjGYzw==</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          <latexit sha1_base64="1n7PzSUYMfNYAK5ZpZMESbD63KI=">AAACCXicdVDLSsNAFJ34rPVVdelmsAiuQlJD2u4qblxWsQ9oY5lMJu3QySTMTIQS+gX+gFv9A3fi1q/wB/wOJ20FK3pg4Nxz7uXeOX7CqFSW9WGsrK6tb2wWtorbO7t7+6WDw7aMU4FJC8csFl0fScIoJy1FFSPdRBAU+Yx0/PFl7nfuiZA05rdqkhAvQkNOQ4qR0tLdBWPwhgQpzis5KJUt03IrTr0CLdNxam7d1aTqVG33HNqmNUMZLNAclD77QYzTiHCFGZKyZ1uJ8jIkFMWMTIv9VJIE4TEakp6mHEVEetns6ik81UoAw1joxxWcqT8nMhRJOYl83RkhNZK/vVz8y+ulKqx5GeVJqgjH80VhyqCKYR4BDKggWLGJJggLqm+FeIQEwkoHtbQll7U41cF8/x7+T9oV03ZN97pSbjiLiArgGJyAM2CDKmiAK9AELYCBAI/gCTwbD8aL8Wq8zVtXjMXMEViC8f4FfMabgA==</latexit>




of reductions is that, unlike the set of all reduc-                                • not finitely representable
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 <latexit sha1_base64="rMMjr37wd1d9bWVcaWQtOAD7pZQ=">AAACGXicdVBNS0JBFJ1nX2ZfVrvaDEnQSp5KFq2ENi0N8gNUZN54nw7Om/eYuS8QEfof7dvWX2gXbVv1D/oZzVMDjTowcDjnHu7c40VSGHTdTye1srq2vpHezGxt7+zuZfcP6iaMNYcaD2Womx4zIIWCGgqU0Iw0sMCT0PCG14nfuAdtRKjucBRBJ2B9JXzBGVqpmz1SIVJfKIEgR1SDDRtQyGy+m80V8u4U1F0gRfe8VKI/Vo7MUe1mv9q9kMeBzXPJjGkV3Ag7Y6ZRcAmTTDs2EDE+ZH1oWapYAKYznt4woadW6VE/1PYppFN1MTFmgTGjwLOTAcOB+e0l4l9eK0b/sjMWKooRFJ8t8mNJMaRJIbQnNHC0x/cE41rYv1I+YJpxtLUtbUlkK04oXazmf1Iv5gvlfPm2mKtczUtKk2NyQs5IgVyQCrkhVVIjnDyQJ/JMXpxH59V5c95noylnnjkkS3A+vgHsxKE5</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       <latexit sha1_base64="BSf0CLajyw/hxzl49XeaVBxcTNI=">AAACBHicdZDLSgNBEEVrfMb4irp00xgEV2Em0SiuAm5cRjAPSIbQ06lJmvQ86O4RwpCte7f6C+7Erf/hH/gZ9iQREtGChsu5VVT19WLBlbbtT2tldW19YzO3ld/e2d3bLxwcNlWUSIYNFolItj2qUPAQG5prge1YIg08gS1vdJP5rQeUikfhvR7H6AZ0EHKfM6oNanW9RAjUvULRKdnTIvaCKNsXlQr5sYowr3qv8NXtRywJMNRMUKU6jh1rN6VScyZwku8mCmPKRnSAHSNDGqBy0+m5E3JqSJ/4kTQv1GRKFydSGig1DjzTGVA9VL+9DP7ldRLtX7kpD+NEY8hmi/xEEB2R7O+kzyUyLcZGUCa5uZWwIZWUaZPQ0pYMGzghZDGa/0WzXHKqperdebF2PQ8pB8dwAmfgwCXU4Bbq0AAGI3iCZ3ixHq1X6816n7WuWPOZI1gq6+MbOjGYzw==</latexit>




tions, it is recursively enumerable. This means
                                                                                      • countable
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           <latexit sha1_base64="7gZYi4bmykZbncvPqPI6m/Y6S7Q=">AAACBnicdVDLSsNAFJ3UV62vqks3g0VwFZJSEuuq4MZlBfuQNpTJdNIOncyEmYlQQvfu3eovuBO3/oZ/4Gc4aStY0QMXDuecy32ECaNKO86HVVhb39jcKm6Xdnb39g/Kh0dtJVKJSQsLJmQ3RIowyklLU81IN5EExSEjnXBylfudeyIVFfxWTxMSxGjEaUQx0ka6wyLlGpnwoFxxbNd161UHOrbne55fM8Sp+XW/Cl3bmaMClmgOyp/9ocBpTLjGDCnVc51EBxmSmmJGZqV+qkiC8ASNSM9QjmKigmy+8AyeGWUIIyFNcQ3n6s+ODMVKTePQJGOkx+q3l4t/eb1URxdBRnmSasLxYlCUMqgFzK+HQyoJ1mxqCMKSml0hHiOJsDY/WpmSy0acQWhe830//J+0q7br2d5NtdK4XD6pCE7AKTgHLvBBA1yDJmgBDGLwCJ7As/VgvViv1tsiWrCWPcdgBdb7F0mUmfs=</latexit>




                                                           VP Lex Reductions
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      <latexit sha1_base64="JDpc5QepgMRb7Vf/zwzI+1qgtJY=">AAACBHicdVDLSsNAFJ3UV62vqks3g0VwFZJSEuuq4MZlBfuANpTJ9KYdOpmEmYlQQrfu3eovuBO3/od/4Gc4fQgqeuDC4Zx7ufeeMOVMacd5twpr6xubW8Xt0s7u3v5B+fCorZJMUmjRhCeyGxIFnAloaaY5dFMJJA45dMLJ1dzv3IFULBG3eppCEJORYBGjRBup0w8zzkEPyhXHdl23XnWwY3u+5/k1Q5yaX/er2LWdBSpoheag/NEfJjSLQWjKiVI910l1kBOpGeUwK/UzBSmhEzKCnqGCxKCCfHHuDJ8ZZYijRJoSGi/U7xM5iZWaxqHpjIkeq9/eXPzL62U6ughyJtJMg6DLRVHGsU7w/Hc8ZBKo5lNDCJXM3IrpmEhCtUnox5a5bMQZxiaar//x/6RdtV3P9m5qlcblKqQiOkGn6By5yEcNdI2aqIUomqAH9IierHvr2XqxXpetBWs1c4x+wHr7BJ29mRA=</latexit>




                                                                <latexit sha1_base64="J1bzhwzob9Rl2qhQ3ABzX4J2YRk=">AAACDnicdZBLSgNBEIZ74ivGV6JLN41BcDXMDOPE7AJuXLiIYh6QhNDTqSRNeh5096gh5A5ewK3ewJ249QpewHPYk0Qwoj80/HxVRVX/fsyZVJb1YWRWVtfWN7Kbua3tnd29fGG/LqNEUKjRiEei6RMJnIVQU0xxaMYCSOBzaPij87TeuAUhWRTeqHEMnYAMQtZnlCiNuvlCvYov4R5fQy+hKZLdfNEy3ZLjuC62TOfULpdT47klr2Rh27RmKqKFqt38Z7sX0SSAUFFOpGzZVqw6EyIUoxymuXYiISZ0RAbQ0jYkAcjOZHb6FB9r0sP9SOgXKjyjPycmJJByHPi6MyBqKH/XUvhXrZWo/llnwsI4URDS+aJ+wrGKcJoD7jEBVPGxNoQKpm/FdEgEoUqntbQlxRpOdTDfv8f/m7pj2p7pXTnFiruIKIsO0RE6QTYqoQq6QFVUQxTdoUf0hJ6NB+PFeDXe5q0ZYzFzgJZkvH8BwHicoA==</latexit>




that assuming the existence of a verifiable re-                                       • finitely representable                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        <latexit sha1_base64="JDpc5QepgMRb7Vf/zwzI+1qgtJY=">AAACBHicdVDLSsNAFJ3UV62vqks3g0VwFZJSEuuq4MZlBfuANpTJ9KYdOpmEmYlQQrfu3eovuBO3/od/4Gc4fQgqeuDC4Zx7ufeeMOVMacd5twpr6xubW8Xt0s7u3v5B+fCorZJMUmjRhCeyGxIFnAloaaY5dFMJJA45dMLJ1dzv3IFULBG3eppCEJORYBGjRBup0w8zzkEPyhXHdl23XnWwY3u+5/k1Q5yaX/er2LWdBSpoheag/NEfJjSLQWjKiVI910l1kBOpGeUwK/UzBSmhEzKCnqGCxKCCfHHuDJ8ZZYijRJoSGi/U7xM5iZWaxqHpjIkeq9/eXPzL62U6ughyJtJMg6DLRVHGsU7w/Hc8ZBKo5lNDCJXM3IrpmEhCtUnox5a5bMQZxiaar//x/6RdtV3P9m5qlcblKqQiOkGn6By5yEcNdI2aqIUomqAH9IierHvr2XqxXpetBWs1c4x+wHr7BJ29mRA=</latexit>
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                <latexit sha1_base64="j5s57b86agGsAUxPSrCo2MdRsb0=">AAACFXicdVDLSsNAFJ34rPUVFdy4GSyCq5CUklhXBTcuK9gHtKVMpjft0MkkzEyEUvsd7t3qL7gTt679Az/D6UOwogcuXM65h3vvCVPOlHbdD2tldW19YzO3ld/e2d3btw8O6yrJJIUaTXgimyFRwJmAmmaaQzOVQOKQQyMcXk31xh1IxRJxq0cpdGLSFyxilGhDde3jiAmmgY+wBGNUIDQx3q5dcB3P88pFF7uOH/h+UDKNWwrKQRF7jjtDAS1Q7dqf7V5Cs9j4KSdKtTw31Z0xkZpRDpN8O1OQEjokfWiZVpAYVGc8u3+CzwzTw1EiTQmNZ+xPx5jESo3i0EzGRA/Ub21K/qW1Mh1ddMZMpJkGQeeLooxjneBpGLjHJFBtnu8xQiUzt2I6IJJQbSJb2jKlDTnB2ETz/T/+v6kXHc93/JtioXK5CCmHTtApOkceClAFXaMqqiGK7tEjekLP1oP1Yr1ab/PRFWvhOUJLsN6/AEnOn+E=</latexit>




duction in the space, one can set up a trivial
                                                            Canonical Reductions      • efficiently constructible
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     <latexit sha1_base64="22NimW+mbik9DwOBKFF6Zusq+2c=">AAACEXicdZBLTsMwEIad8irlFR47NhYVEqsobUIfu0rdsCyIPqQ2qhzHba06TmQ7SKXqKbgAW7gBO8SWE3ABzoHTFokiGMnSP9/MaMa/HzMqlW1/GJm19Y3Nrex2bmd3b//APDxqySgRmDRxxCLR8ZEkjHLSVFQx0okFQaHPSNsf19N6+44ISSN+qyYx8UI05HRAMVIa9c2TOuIR1ymDNyRIcEpl38zblltyHKcIbcsuXVaq1VS4jlt2YcGy55EHy2j0zc9eEOEkJFxhhqTsFuxYeVMkFMWMzHK9RJIY4TEakq6WHIVEetP59TN4rkkAB5HQjys4pz8npiiUchL6ujNEaiR/11L4V62bqEHFm1IeJ4pwvFg0SBhUEUytgAEVBCs20QJhQfWtEI+QQFhpw1a2pFjDmTbm+/fwf9EqWoWSVbou5mvu0qIsOAVn4AIUQBnUwBVogCbA4B48gifwbDwYL8ar8bZozRjLmWOwEsb7F9KInlQ=</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                <latexit sha1_base64="LUPTjwqLZCp1avI2N6EVRvwUJvw=">AAACGHicdVDLSsNAFJ34rPUVdSVuBovgKiSlJNZVwY3LCvYBbSiTyaQdOpmEmYlQQvE/3LvVX3Anbt35B36Gk7aCFT0wcOfce+bOOUHKqFS2/WGsrK6tb2yWtsrbO7t7++bBYVsmmcCkhROWiG6AJGGUk5aiipFuKgiKA0Y6wfiq6HfuiJA04bdqkhI/RkNOI4qR0tTAPCaRvlDCFZtAnHCpRIYV1fKBWbEtx3HqVRvaluu5rlfThV3z6l4VOpY9QwUs0ByYn/0wwVms38IMSdlz7FT5ORKKYkam5X4mSYrwGA1JT5ccxUT6+czCFJ5pJoRRIvThCs7Yn4ocxVJO4kBPxkiN5O9eQf7V62UquvBzytNMEY7ni6KMQZXAIg8YUkFwYT6kCAuq/wrxCAmElU5taUtBa3IKoY7m2z/8v2hXLce13JtqpXG5CKkETsApOAcO8EADXIMmaAEM7sEjeALPxoPxYrwab/PRFWOhOQJLMN6/ANp6oUI=</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      <latexit sha1_base64="JDpc5QepgMRb7Vf/zwzI+1qgtJY=">AAACBHicdVDLSsNAFJ3UV62vqks3g0VwFZJSEuuq4MZlBfuANpTJ9KYdOpmEmYlQQrfu3eovuBO3/od/4Gc4fQgqeuDC4Zx7ufeeMOVMacd5twpr6xubW8Xt0s7u3v5B+fCorZJMUmjRhCeyGxIFnAloaaY5dFMJJA45dMLJ1dzv3IFULBG3eppCEJORYBGjRBup0w8zzkEPyhXHdl23XnWwY3u+5/k1Q5yaX/er2LWdBSpoheag/NEfJjSLQWjKiVI910l1kBOpGeUwK/UzBSmhEzKCnqGCxKCCfHHuDJ8ZZYijRJoSGi/U7xM5iZWaxqHpjIkeq9/eXPzL62U6ughyJtJMg6DLRVHGsU7w/Hc8ZBKo5lNDCJXM3IrpmEhCtUnox5a5bMQZxiaar//x/6RdtV3P9m5qlcblKqQiOkGn6By5yEcNdI2aqIUomqAH9IierHvr2XqxXpetBWs1c4x+wHr7BJ29mRA=</latexit>




decision procedure to find it. The underlying
verification problem remains undecidable for
generic infinite-state programs, but at least, we
know that the component of searching for a reduction does not add any new divergence opportuni-
ties. This is in sharp contrast to, for example, considering the state space of all possible reductions,
where one has to either bound the space to a finite subset [7] or use ad-hoc heuristics [47, 53] to
curb this intrinsic divergent behaviour. Moreover, the VP lex reductions are finitely representable,
whereas an arbitrary reduction may not be.
   Rather than setting up a search algorithm for a reduction in the space of VP lex reductions, we
opted for investigating a different more practical hypothesis in this paper. This is motivated by
the fact that the search, even in the simpler setup of [27, 28], is very expensive and unscalable and
the problem only gets worse with the increased complexity of the same operations for pushdown
systems [23]. So, there is a natural question about what to do when one hits that scalability barrier.
There is a well-established tradition of user-provided annotations to help with the automation of
harder instances. For instance, in [52], when the mined predicates are insufficient for the combined
search for an alignment and a proof, the user can input predicates in the proof (of the unknown
alignment) to help; which is in line with this tradition. In this paper, we explore the alternative
possibility of user-provided annotations for the specification of reductions. we devise a smaller (yet
infinite) subfamily of lex reductions, we call canonical reductions, that have three properties:
    (1) They are intuitive to the programmer. For instance, looking at div and scaling, the pro-
         grammer can easily guess and specify that they are interested in an asynchronous product
         of two div instances where one copy moves twice as fast as the other copy.
    (2) They are simply and succinctly specifiable (like a correctness property is in a logical
         language) as part of the verification command, using composable building blocks.
    (3) They are expressive enough to provide the means of solving a broad range of instances.
   To understand the obstacles in achieving this, let us expand our simple div example one more
time with a substantially more sophisticated property:
                𝑛 ′′ = 𝑛 + 𝑛 ′ =⇒ div(𝑛 ′′, 𝑑) ≥ div(𝑛, 𝑑) + div(𝑛 ′, 𝑑)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              (distributivity)
where distributivity is a 3-safety property, and clearly, lockstep product is not the right choice
for this and varying the rate is also insufficient. Consider the product program
                                   (div(n, d) ⊕ div(n′, d′ )) ⊗ div(n′′, d′′ )
where we intentionally use the vague ⊕ and ⊗ operators for the choice of product operators for now.
Intuitively, since 𝑛 ′′ = 𝑛 + 𝑛 ′ , we expect the execution length of the div(n′′, d′′ ) copy to be roughly
the same as the sum of the execution lengths of the div(n, d) and div(n′, d′ ) copies. Therefore,
in a suitable product program, we want to run a kind of sequential composition of div(n, d) and
div(n′, d′ ) in tandem with div(n′′, d′′ ); that is, align each of the first 𝑛 recursive calls of div(n′′, d′′ )
with a call from div(n, d) and the last 𝑛 ′ recursive calls of div(n′′, d′′ ) with a call from div(n′, d′ ).
This is precisely how looped computations are split [7] to accommodate the construction of an
effective product program. However, a recursive computation cannot be split like a loop through
loop fission, by breaking a loop into two sequentially composed loops. The solution, at the high
level, is in fact the complete opposite. One first merges div(n, d) and div(n′, d′ ) so that it looks like
6                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    Ruotong Cheng and Azadeh Farzan


one recursive sequence of calls, and then synchronizes this merged program with div(n′′, d′′ ) in a
lockstep manner. This merge can be viewed as a recursive analog of loop fusion.
    To visualize this, recall the runs 𝜏 and 𝜏 ′ illustrated    00
                                                                               <latexit sha1_base64="pfhg0h0wunpaO8Cf+eMAhe3+e3A=">AAAB7XicbVDLTgJBEOzFF+IL9ehlIjF4IrvGoEeiF4+YyCOBDZkdZmFkdnYz02tCCP/gxYPGePV/vPk3DrAHBSvppFLVne6uIJHCoOt+O7m19Y3Nrfx2YWd3b/+geHjUNHGqGW+wWMa6HVDDpVC8gQIlbyea0yiQvBWMbmd+64lrI2L1gOOE+xEdKBEKRtFKzS7StFzuFUtuxZ2DrBIvIyXIUO8Vv7r9mKURV8gkNabjuQn6E6pRMMmnhW5qeELZiA54x1JFI278yfzaKTmzSp+EsbalkMzV3xMTGhkzjgLbGVEcmmVvJv7ndVIMr/2JUEmKXLHFojCVBGMye530heYM5dgSyrSwtxI2pJoytAEVbAje8surpHlR8aqV6v1lqXaTxZGHEziFc/DgCmpwB3VoAINHeIZXeHNi58V5dz4WrTknmzmGP3A+fwDoQI61</latexit>




earlier, and consider 𝜏 ′′ illustrated on the right, as being ⌧ { . . . { . . . { . . . { . . . { . . . } . . . } . . . } . . . } . . . }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             <latexit sha1_base64="30l/+famLWSIcv58wEV3kdiL33g=">AAACT3icjZBLS8NAEMc38dXWV9Sjl8UieApJKYm9Fb14rGIf0Iay2W7apZsHuxuhhH4vv4ZHLx7Vb+BN3NQItio4sOyP/8wwM38/YVRIy3rU9LX1jc2tUrmyvbO7t28cHHZEnHJM2jhmMe/5SBBGI9KWVDLSSzhBoc9I159e5vnuHeGCxtGtnCXEC9E4ogHFSCppaNwMMjgYxVLAf8F8BdT/A4ZG1TJt227U69AyHddxHFuBVXcbrgtt01pEFRTRGhrPqhOnIYkkZkiIvm0l0ssQlxQzMq8MUkEShKdoTPoKIxQS4WWL2+fwVCkjGMRcvUjChfq9I0OhELPQV5UhkhOxmsvF33L9VAbnXkajJJUkwp+DgpRBGcPcSDiinGDJZgoQ5lTtCvEEcYSlsntpSi4rMTfm63r4N3Rqpu2YznWt2rwoLCqBY3ACzoANXNAEV6AF2gCDe/AEXsCr9qC9ae96UaprBRyBpdDLH397tGQ=</latexit>




respectively runs of the three disjoint copies div(n, d),
                                                               ⇢ [ ...[ ...[ ...( ...( ...)...) ...] ...] ...]
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        <latexit sha1_base64="8H5X6Dq1QG1iHmYGAEKtPZUu4pA=">AAACL3icbVDLSsNAFJ3UV62vqks3g0XoQkqSSh+7ohuXFewD0lAm00k7dPJgZiKUkP/wN/wBt/oH4kZcCf6Fk7SCbT0wcDjnnrmX44SMCqnr71puY3Nreye/W9jbPzg8Kh6fdEUQcUw6OGAB7ztIEEZ90pFUMtIPOUGew0jPmd6kfu+BcEED/17OQmJ7aOxTl2IklTQsmvEg+8TiY8eO9Uq93jSv6pd6Rc+gSLXRrDYbCSzDwSiQAibDYunXhuvEWJASWKA9LH6pJI484kvMkBCWoYfSjhGXFDOSFAaRICHCUzQmlqI+8oiw4+ysBF4oZQTdgKvnS5ipfxMx8oSYeY6a9JCciFUvFf/zrEi6DTumfhhJ4uP5IjdiUAYwLQqOKCdYspkiCHOqboV4gjjCUtW5tCWVlZgWY6zWsE66ZsWoVWp3Zql1vagoD87AOSgDA9RBC9yCNugADB7BM3gBr9qT9qZ9aJ/z0Zy2yJyCJWjfP/mKpZA=</latexit>   <latexit sha1_base64="zhTDdSY1k/vJ110q/gLy7i/dnYs=">AAACMHicbVDLSgMxFM34rPU16tJNsAgVZJhppY9d0Y3LCvYB7VAyaaYNzWSGJCOUoR/ib/gDbvUPdCVuXPgVZtoKtvVA4HDOPbmX40WMSmXb78ba+sbm1nZmJ7u7t39waB4dN2UYC0waOGShaHtIEkY5aSiqGGlHgqDAY6TljW5Sv/VAhKQhv1fjiLgBGnDqU4yUlnpmMelOP+mIgecmtlUuVwtX5UvbsqfQpFipFquVCczDbj9UEl5Membu14erxJmTHJij3jO/dBTHAeEKMyRlx7Ej5SZIKIoZmWS7sSQRwiM0IB1NOQqIdJPpXRN4rpU+9EOhH1dwqv5NJCiQchx4ejJAaiiXvVT8z+vEyq+4CeVRrAjHs0V+zKAKYdoU7FNBsGJjTRAWVN8K8RAJhJXuc2FLKmsxLcZZrmGVNAuWU7JKd4Vc7XpeUQacgjOQBw4ogxq4BXXQABg8gmfwAl6NJ+PN+DA+Z6NrxjxzAhZgfP8AbjClww==</latexit>   <latexit sha1_base64="QtnHtIxFin/i+O9LcrvHPvpjEDc=">AAACMHicbVDLSgMxFM3UV62vUZdugkVQkDLTSqfdFd24rGAf0A4lk6ZtaCYzJBmhDP0Qf8MfcKt/oCtx48KvMNOOYFsPBA7n3JN7OV7IqFSW9W5k1tY3Nrey27md3b39A/PwqCmDSGDSwAELRNtDkjDKSUNRxUg7FAT5HiMtb3yT+K0HIiQN+L2ahMT10ZDTAcVIaalnluLu7JOOGHpubBUcp1q8ci6tgjWDJqVKtVStTCHs9gMl4QWc9sz8rw9XiZ2SPEhR75lfOosjn3CFGZKyY1uhcmMkFMWMTHPdSJIQ4TEako6mHPlEuvHsrik800ofDgKhH1dwpv5NxMiXcuJ7etJHaiSXvUT8z+tEalBxY8rDSBGO54sGEYMqgElTsE8FwYpNNEFYUH0rxCMkEFa6z4UtiazFpBh7uYZV0iwW7HKhfFfM167TirLgBJyCc2ADB9TALaiDBsDgETyDF/BqPBlvxofxOR/NGGnmGCzA+P4BYqeluw==</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          <latexit sha1_base64="8FD0CU4dAiCLm7lSSQPSfTH+fzQ=">AAACL3icbVDLSsNAFJ3UV62vqks3g0VwISWJIW13RTcuK9gHpKFMptN26OTBzEQoIf/hb/gDbvUPxI24EvwLJ20WtvXAwOGcc+dejhcxKqSuf2iFjc2t7Z3ibmlv/+DwqHx80hFhzDFp45CFvOchQRgNSFtSyUgv4gT5HiNdb3qb+d1HwgUNgwc5i4jro3FARxQjqaRB2Uz6808cPvbcRK/qtmk1zCu9all1u2ErUrNqhn2dQgf2h6EUMB2UKyo3B1wnRk4qIEdrUP5Wkzj2SSAxQ0I4hh5JN0FcUsxIWurHgkQIT9GYOIoGyCfCTeZnpfBCKUM4Crl6gYRz9e9EgnwhZr6nkj6SE7HqZeJ/nhPLUd1NaBDFkgR4sWgUMyhDmBUFh5QTLNlMEYQ5VbdCPEEcYanqXNqSyUrMijFWa1gnHbNq2FX73qw0b/KKiuAMnINLYIAaaII70AJtgMETeAGv4E171t61T+1rES1o+cwpWIL28wtglaXP</latexit>   <latexit sha1_base64="8FD0CU4dAiCLm7lSSQPSfTH+fzQ=">AAACL3icbVDLSsNAFJ3UV62vqks3g0VwISWJIW13RTcuK9gHpKFMptN26OTBzEQoIf/hb/gDbvUPxI24EvwLJ20WtvXAwOGcc+dejhcxKqSuf2iFjc2t7Z3ibmlv/+DwqHx80hFhzDFp45CFvOchQRgNSFtSyUgv4gT5HiNdb3qb+d1HwgUNgwc5i4jro3FARxQjqaRB2Uz6808cPvbcRK/qtmk1zCu9all1u2ErUrNqhn2dQgf2h6EUMB2UKyo3B1wnRk4qIEdrUP5Wkzj2SSAxQ0I4hh5JN0FcUsxIWurHgkQIT9GYOIoGyCfCTeZnpfBCKUM4Crl6gYRz9e9EgnwhZr6nkj6SE7HqZeJ/nhPLUd1NaBDFkgR4sWgUMyhDmBUFh5QTLNlMEYQ5VbdCPEEcYanqXNqSyUrMijFWa1gnHbNq2FX73qw0b/KKiuAMnINLYIAaaII70AJtgMETeAGv4E171t61T+1rES1o+cwpWIL28wtglaXP</latexit>   <latexit sha1_base64="8FD0CU4dAiCLm7lSSQPSfTH+fzQ=">AAACL3icbVDLSsNAFJ3UV62vqks3g0VwISWJIW13RTcuK9gHpKFMptN26OTBzEQoIf/hb/gDbvUPxI24EvwLJ20WtvXAwOGcc+dejhcxKqSuf2iFjc2t7Z3ibmlv/+DwqHx80hFhzDFp45CFvOchQRgNSFtSyUgv4gT5HiNdb3qb+d1HwgUNgwc5i4jro3FARxQjqaRB2Uz6808cPvbcRK/qtmk1zCu9all1u2ErUrNqhn2dQgf2h6EUMB2UKyo3B1wnRk4qIEdrUP5Wkzj2SSAxQ0I4hh5JN0FcUsxIWurHgkQIT9GYOIoGyCfCTeZnpfBCKUM4Crl6gYRz9e9EgnwhZr6nkj6SE7HqZeJ/nhPLUd1NaBDFkgR4sWgUMyhDmBUFh5QTLNlMEYQ5VbdCPEEcYanqXNqSyUrMijFWa1gnHbNq2FX73qw0b/KKiuAMnINLYIAaaII70AJtgMETeAGv4E171t61T+1rES1o+cwpWIL28wtglaXP</latexit>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             <latexit sha1_base64="y+mOOizjtpS/6ecwvshSKQcZ8bI=">AAACL3icbVDLSsNAFJ3UV62vqEs3g0VwISGJIW13RTcuK9gHtKFMppN26OTBzEQoof/hb/gDbvUPxI24EvwLJ20XtvXAwOGcc+dejp8wKqRpfmiFjc2t7Z3ibmlv/+DwSD8+aYk45Zg0ccxi3vGRIIxGpCmpZKSTcIJCn5G2P77N/fYj4YLG0YOcJMQL0TCiAcVIKqmv21lv9kmXD30vMw3TtZ2afWUajlN1a64iFadiuddTCHuDWAroTft6WeVmgOvEWpAyWKDR17/VKE5DEknMkBBdy0yklyEuKWZkWuqlgiQIj9GQdBWNUEiEl83OmsILpQxgEHP1Igln6t+JDIVCTEJfJUMkR2LVy8X/vG4qg6qX0ShJJYnwfFGQMihjmBcFB5QTLNlEEYQ5VbdCPEIcYanqXNqSy0rMi7FWa1gnLduwXMO9t8v1m0VFRXAGzsElsEAF1MEdaIAmwOAJvIBX8KY9a+/ap/Y1jxa0xcwpWIL28wtjoKXR</latexit>   <latexit sha1_base64="y+mOOizjtpS/6ecwvshSKQcZ8bI=">AAACL3icbVDLSsNAFJ3UV62vqEs3g0VwISGJIW13RTcuK9gHtKFMppN26OTBzEQoof/hb/gDbvUPxI24EvwLJ20XtvXAwOGcc+dejp8wKqRpfmiFjc2t7Z3ibmlv/+DwSD8+aYk45Zg0ccxi3vGRIIxGpCmpZKSTcIJCn5G2P77N/fYj4YLG0YOcJMQL0TCiAcVIKqmv21lv9kmXD30vMw3TtZ2afWUajlN1a64iFadiuddTCHuDWAroTft6WeVmgOvEWpAyWKDR17/VKE5DEknMkBBdy0yklyEuKWZkWuqlgiQIj9GQdBWNUEiEl83OmsILpQxgEHP1Igln6t+JDIVCTEJfJUMkR2LVy8X/vG4qg6qX0ShJJYnwfFGQMihjmBcFB5QTLNlEEYQ5VbdCPEIcYanqXNqSy0rMi7FWa1gnLduwXMO9t8v1m0VFRXAGzsElsEAF1MEdaIAmwOAJvIBX8KY9a+/ap/Y1jxa0xcwpWIL28wtjoKXR</latexit>   <latexit sha1_base64="y+mOOizjtpS/6ecwvshSKQcZ8bI=">AAACL3icbVDLSsNAFJ3UV62vqEs3g0VwISGJIW13RTcuK9gHtKFMppN26OTBzEQoof/hb/gDbvUPxI24EvwLJ20XtvXAwOGcc+dejp8wKqRpfmiFjc2t7Z3ibmlv/+DwSD8+aYk45Zg0ccxi3vGRIIxGpCmpZKSTcIJCn5G2P77N/fYj4YLG0YOcJMQL0TCiAcVIKqmv21lv9kmXD30vMw3TtZ2afWUajlN1a64iFadiuddTCHuDWAroTft6WeVmgOvEWpAyWKDR17/VKE5DEknMkBBdy0yklyEuKWZkWuqlgiQIj9GQdBWNUEiEl83OmsILpQxgEHP1Igln6t+JDIVCTEJfJUMkR2LVy8X/vG4qg6qX0ShJJYnwfFGQMihjmBcFB5QTLNlEEYQ5VbdCPEIcYanqXNqSy0rMi7FWa1gnLduwXMO9t8v1m0VFRXAGzsElsEAF1MEdaIAmwOAJvIBX8KY9a+/ap/Y1jxa0xcwpWIL28wtjoKXR</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                <latexit sha1_base64="S3ArUb+j6acSKW3edSXDVlZdNF0=">AAAB63icbVDLSgNBEOyNrxhfUY9eBoPgKeyKRI9BLx4jmAckS5idzGaHzGOZmRVCyC948aCIV3/Im3/jbLIHjRY0FFXddHdFKWfG+v6XV1pb39jcKm9Xdnb39g+qh0cdozJNaJsornQvwoZyJmnbMstpL9UUi4jTbjS5zf3uI9WGKflgpykNBR5LFjOCbS4NdKKG1Zpf9xdAf0lQkBoUaA2rn4ORIpmg0hKOjekHfmrDGdaWEU7nlUFmaIrJBI9p31GJBTXhbHHrHJ05ZYRipV1Jixbqz4kZFsZMReQ6BbaJWfVy8T+vn9n4OpwxmWaWSrJcFGccWYXyx9GIaUosnzqCiWbuVkQSrDGxLp6KCyFYffkv6VzUg0a9cX9Za94UcZThBE7hHAK4gibcQQvaQCCBJ3iBV094z96b975sLXnFzDH8gvfxDSM+jlI=</latexit>




div(n′, d′ ), and div(n′′, d′′ ). First, 𝜏 and 𝜏 ′ are merged
together, by fully nesting 𝜏 ′ inside 𝜏 to get 𝜌. This operation (standing in for ⊕) can be viewed as
the recursive analog of concatenation in the looped (iterative) setting.
    We introduce nested concatenation, the recursive dual of concatenation as a novel building block.
Note that, for a tail recursion, nested concatenation behaves similar to concatenation, but otherwise,
it is an entirely different and new way of composing computations. 𝜌 can then be composed with
𝜏 ′′ through a standard lockstep composition, where the green and blue/pink calls are executed
in tandem. Effectively, the innermost two calls of 𝜏 ′′ are synched with the two calls of 𝜏 ′ , and its
outermost three calls are synched with the calls of 𝜏.
    Looking at the monotonicity and scaling properties of div, a parametric-by-speed version of
lockstep is also a suitable candidate for another building block. Note that the parametric lockstep,
by itself, yields an unbounded family of reductions. Combined with nested concatenation, they
give rise to an infinite number of possibilities for product programs that can be very succinctly
specified by the user. These building blocks are highly intuitive, but very nontrivial to define
formally and construct correctly. Our second (theoretical and practical) key contribution is that we
propose formal definitions for these building block reductions (Section 6.1), and also show that
these reductions all belong to the state space of lex reductions. Moreover, we propose an alternative
direct way of constructing product programs made from the two building block reductions of nested
concatenation and parametrized lockstep (Section 6.3) that yields much more compact representations
for these canonical reductions, compared to the generic (but optimized) construction from Section
4 for all lex reductions. Remarkably, the subfamily demonstrates a large degree of expressivity with
nearly all of our 103 benchmarks becoming solvable using a a reduction from this family.
    As a bonus (third) contribution, we make a new observation for the verification of concurrent
recursive programs: The well-nested shuffle is an under-approximation of a concurrent recursive
program, which itself is a standard (nondeterministic) recursive program. As such, any existing
technique for recursive program analysis and bug finding can be used to find errors in it which are
guaranteed to be errors in the original program. Moreover, in Section 5, we formulate conditions
under which this under-approximation becomes a sound one; that is, any property proven for the
well-nested shuffle (using standard techniques) is guaranteed to hold for the original program.
    In Section 7, we outline how the language-theoretic (automata or grammar) description of a
product program can be turned into a classic recursive program and encoded for standard safety
verification, which serves as the last step of our reduction of the problem of hypersafety verification
of recursive programs to standard safety verification.
    We have a tool called HyRec, that reduces an input hypersafety instance to a classic safety instance
by constructing the appropriate product programs. We experiment with the a large set (103) of
benchmarks to show that the product programs are absolutely vital for hypersafety verification
of recursive programs. Specifically, our experiments with 103 benchmarks confirm that the high
level idea of the product program is intuitively known to the programmer and can be succinctly
specified and facilitates the verification of the hypersafety instance.
Products of Recursive Programs for Hypersafety Verification                                                   7


2     Background
2.1    Languages, Automata, and Grammars
Visibly pushdown langauges [2] are a well-established formal model for capturing the set of inter-
procedurally realizable paths [50, 51] of a program: procedure calls always return to the correct
location, but the (data) feasibility of the paths is not considered.
   We review some key concepts for visibly pushdown languages, and refer the reader to [2] for a full
exposition. A visibly pushdown alphabet (VP alphabet) e     Σ is the union of three disjoint finite alphabets,
Σcall (calls), Σret (returns), and Σint (internals). We use eΣ when we want to emphasize the alphabet
is visibly pushdown and use Σ for a general alphabet. A word 𝑤 1 · · · 𝑤𝑙 ∈ e           Σ∗ induces a unique
matching relation [3] ⇝ over {−∞, 1, 2, . . . , 𝑙 } × {1, 2, . . . , 𝑙, +∞} so that 𝑖 ⇝ 𝑗 (−∞ < 𝑖 < 𝑗 < +∞)
means 𝑤𝑖 , 𝑤 𝑗 are a pair of call and return that match in the usual sense, and 𝑖 ⇝ +∞ (resp. −∞ ⇝ 𝑖)
means 𝑖 is a pending call (resp. return). A word without pending letter is well-matched.
   A visibly pushdown automaton (VPA) [2] over a VP alphabet is a pushdown automaton whose
stack operations are entirely controlled by the type of the letter read: it pushes when reading a call,
pops when reading a return, and neither pushes nor pops when reading an internal.
  Definition 2.1 (Visibly Pushdown Automaton (VPA)). A visibly pushdown automaton over a
VP alphabet e     Σ is a tuple 𝑀 = (𝑄, 𝑄 in, Γ, 𝛿, 𝑄 F ) where 𝑄 is a finite set of states, 𝑄 in ⊂ 𝑄 is a
set of initial states, Γ is a finite stack alphabet that contains a special bottom-of-stack symbol ⊥,
𝛿 = 𝛿 call ∪𝛿 ret ∪𝛿 int is a set of transitions, where 𝛿 call ⊂ 𝑄 ×Σcall ×𝑄 × (Γ \{⊥}), 𝛿 ret ⊂ 𝑄 ×Σret ×Γ ×𝑄,
and 𝛿 int ⊂ 𝑄 × Σint × 𝑄, and 𝑄 F ⊂ 𝑄 is a set of final states.
  We say a VPA is complete if at any state, reading any letter leads to a next state. A visibly
pushdown language (VPL) is a language recognized by some VPA. VPLs can also be characterized
by visibly pushdown grammars (VPGs) [2], a subclass of context-free grammars. We are mainly
concerned with languages of well-matched words, which are generated by well-matched VPGs [39].
We additionally permit a grammar to have more than one start symbols.
                                                                      Σ, 𝑃, 𝑆) is a well-matched
   Definition 2.2 (Well-matched VPG). A context-free grammar 𝐺 = (𝑉 , e
VPG if every production rule in 𝑃 has the form 𝑋 → 𝜖, 𝑋 → 𝑎𝑌 , or 𝑋 → 𝑐𝑌𝑟𝑍 where 𝑎 ∈ Σint ,
𝑐 ∈ Σcall , and 𝑟 ∈ Σret .
  We recall the shuffle operator ∥ over languages. For any alphabet Σ and Σ′ ⊂ Σ, let the projection
function Π Σ′ : Σ∗ → Σ′∗ be the string homomorphism that erases letters that are not in Σ′ .
    Definition 2.3 (Shuffle). Let Σ be an alphabet that can be partitioned into a disjoint union Σ1 ⊎
· · · ⊎ Σ𝑛 . Let 𝐿𝑖 be a language over alphabet Σ𝑖 (𝑖 = 1, . . . , 𝑛). The shuffle 𝐿1 ∥ · · · ∥ 𝐿𝑛 is the set of
words 𝑤 ∈ Σ∗ such that Π Σ𝑖 (𝑤) ∈ 𝐿𝑖 for each 𝑖.
    Regular languages are closed under shuffle, but this is not true for VPLs, even in the case where
𝐿𝑖 ’s are copies of the same language. For instance, the shuffle of two Dyck languages [19] over
disjoint VP alphabets (opening/closing delimiters are calls/returns) is not context-free [37].

2.2    Recursive Programs
Let 𝑉 be the set of all valuations, i.e., maps from program variables to values, and Stack(𝑉 ) be the
set of all nonempty stacks whose frames are elements of 𝑉 . We use 𝑆.𝜈 to denote a stack whose top
frame is 𝜈 and the rest is 𝑆, which is a smaller stack.
   Following [35], we model a recursive program as a VPL 𝑃 over a VP alphabet e    Σ and a semantics
S :eΣ → P (Stack(𝑉 ) × Stack(𝑉 )) which respects the VP alphabet e    Σ: the type of stack operation
performed by SJ𝑎K is determined by the type of 𝑎. For our purpose, we assume 𝑃 is well-matched.
Formally, there is a map F ⊂ (Σcall × 𝑉 × 𝑉 ) ∪ (Σret × 𝑉 × 𝑉 × 𝑉 ) ∪ (Σint × 𝑉 × 𝑉 ) such that
8                                                                          Ruotong Cheng and Azadeh Farzan


      • If 𝑐 ∈ Σcall , then SJ𝑐K := {(𝑆.𝜈, 𝑆.𝜈.𝜈 ′ ) : 𝜈 ′ ∈ F J𝑐K(𝜈)}.
      • If 𝑟 ∈ Σret , then SJ𝑟 K := {(𝑆.𝜈 < .𝜈, 𝑆.𝜈 ′ ) : 𝜈 ′ ∈ F J𝑟 K(𝜈, 𝜈 < )}.
      • If 𝑎 ∈ Σint , then SJ𝑎K := {(𝑆.𝜈, 𝑆.𝜈 ′ ) : 𝜈 ′ ∈ F J𝑎K(𝜈)}.
Extend S from letters to syntactic runs (words over e           Σ without pending return) via relation com-
position. For a syntactic run 𝜌, the hoare triple {pre}𝜌 {post} holds if for all (𝑆.𝜈, 𝑆 ′ .𝜈 ′ ) ∈ SJ𝜌K, if
𝜈 |= pre, then 𝜈 ′ |= post. We say 𝜌 is feasible if SJ𝜌K ≠ ∅. If 𝜌 is infeasible, any triple {pre}𝜌 {post}
is vacuously true. Given a recursive program (𝑃, S), define {pre}𝑃 {post} as ∀𝜌 ∈ 𝑃 . {pre}𝜌 {post}.
When S is clear from the context, we sometimes use just 𝑃 to refer to the recursive program.

2.3    Commutativity and Reductions
   Definition 2.4 (Commutativity-based Equivalence [46]). Given an irreflexive symmetric commuta-
tivity relation 𝐼 ⊂ Σ × Σ, define the commutativity-based equivalence ≡𝐼 on Σ∗ as the least transitive
reflexive relation such that for all 𝑢, 𝑣 ∈ Σ∗ and 𝑎, 𝑏 ∈ Σ, if (𝑎, 𝑏) ∈ 𝐼 , then 𝑢𝑎𝑏𝑣 ≡𝐼 𝑢𝑏𝑎𝑣.
   It is straightforward to verify that ≡𝐼 is indeed an equivalence relation. Intuitively, two words 𝑢, 𝑣
are equivalent under ≡𝐼 if 𝑣 can be obtained from 𝑢 by repeatedly swapping adjacent commuting
letters. The equivalence relation ≡𝐼 partitions a language into equivalence classes. If a subset of the
language contains representatives from all equivalence classes, we call it a reduction.
   Definition 2.5 (Reduction). Given a commutativity relation 𝐼 on Σ, for a language 𝐿 over Σ, a
       𝐿 of 𝐿 is said to be a reduction if for all 𝜌 ∈ 𝐿, there exists 𝜎 ∈ b
subset b                                                                   𝐿 such that 𝜎 ≡𝐼 𝜌. A reduction
is minimal if there is precisely one such 𝜎 for every 𝜌.
   In our context, letters are statements and words are runs of a program. Thus, we are interested
in not an arbitrary commutativity relation but one that is sound: if (𝑎, 𝑏) ∈ 𝐼 , then 𝑎𝑏 and 𝑏𝑎 have
the same semantics. If 𝑃b is a reduction of 𝑃 under a sound commutativity relation, then 𝑃b covers all
semantics of 𝑃, which results in the following theorem:
   Theorem 2.6 (Soundness of Reductions). If 𝑃b is a reduction of 𝑃 under a sound commutativity
relation, then {pre} 𝑃b {post} if and only if {pre} 𝑃 {post}.

3     Reductions Space for Hypersafety Verification
The classic way [8] to verify a hypersafety property for a recursive procedure is to produce 𝑛 disjoint
copies 𝑃1, . . . , 𝑃𝑛 from it and state the pre/postconditions pre and post as a property of the sequential
composition of these disjoint copies: {pre} 𝑃1 ; . . . ; 𝑃𝑛 {post}. Observe that the same disjointness
assumption implies that the sequential composition can be replaced by a parallel composition (or
the shuffle). Hence we can state our goal as constructing a single (product) recursive program 𝑃b
such that for any hypersafety property expressed as a pair of pre/postconditions pre and post:
                           {pre} 𝑃1 ∥ . . . ∥ 𝑃𝑛 {post} ⇐⇒ {pre} 𝑃b {post}                    (Soundness)
which makes it sound to verify 𝑃b instead. The parallel product is more useful for our purpose,
because it already includes every possible imaginable alignment of individual program runs inside
it. We start by assuming that the programs 𝑃𝑖 ’s are entirely disjoint, and later (in Section 5) address
the concurrency case where some may share variables.
    Each 𝑃𝑖 is a classic recursive program over a disjoint memory and, in the classic sense, can be
interpreted using a stack semantics in the style outlined in 2.2. In order to track the semantic
meaning of an arbitrary run of a product of these programs, which may align the executions from
the programs in an arbitrary way, the semantic function has to maintain 𝑛 stacks, one for each
component, to keep track of each of the 𝑛 disjoint recursive computations. In other words, the
Products of Recursive Programs for Hypersafety Verification                                                  9


global state is now a tuple of 𝑛 stacks, and a statement from the 𝑖-th component operates on the 𝑖-th
stack from this tuple. To get a classic recursive program, we need this tuple to collapse into a single
stack while preserving the ability to keep track of the computation of any arbitrary component 𝑃𝑖 .
This can be guaranteed precisely when the alignments are well-nested.

   Definition 3.1 (Well-nested Words). Let eΣ=eΣ1 ⊎ · · · ⊎ e
                                                            Σ𝑛 , with disjoint e
                                                                               Σ𝑖 ’s. A word 𝑤 ∈ e
                                                                                                 Σ∗ is
well-nested if 𝑖 ⇝ 𝑗 (where ⇝ is the matching relation on 𝑤) implies that 𝑤𝑖 and 𝑤 𝑗 both belong
to the same eΣ𝑘 . For any language 𝐿 ⊂ e
                                       Σ∗ , wn(𝐿) denotes the set of all well-nested words in 𝐿.

    If a language over e Σ contains only well-nested words, we say the language is well-nested. Note
that being well-nested is different from being well-matched (see Section 2.1).
    We need a suitable representation for individual 𝑃𝑖 ’s and 𝑃b that facilitates this goal. The control
flow graph (or equivalent) representations lose track of the recursive structure of the runs. Context
free grammars (CFG) or a pushdown automaton (PA) are the classic models that maintain this
structure. However, visibly pushdown languages (VPL) [2], or alternatively the regular nested word
languages (RNWL) [3], are a strict subset of context free languages that are expressive enough to
model recursive programs and yet have the same desirable boolean properties as regular languages.
    It is straightforward to take as input the code of a recursive component 𝑃𝑖 and construct a visibly
pushdown grammar (VPG) or visibly pushdown automaton (VPA) that precisely captures the set of
well-matched syntactic runs of 𝑃𝑖 . We abuse the notation 𝑃𝑖 to refer both to the program and the
set of syntactic runs, which form a well-matched VPL, since the distinction is always clear from
context. We can always ensure that each 𝑃𝑖 is over a distinct visibly pushdown alphabet e         Σ𝑖 , and
introduce e   Σ=e Σ1 ⊎ · · · ⊎ e
                               Σ𝑛 .
    The language 𝑃 ∥ = 𝑃1 ∥ . . . 𝑃𝑛 is not necessary visibly pushdown, even if all 𝑃𝑖 ’s are; nor does it
exclude ill-nested alignments. In this section, we formulate how we can use simple observations
from language theory and concurrency theory to define and algorithmically construct individual
product programs (reductions) from 𝑃 ∥ , which (1) satisfy the Soundness condition, (2) only contain
well-nested alignments, and (3) are visibly pushdown and therefore representable through VPAs and
VPGs. It is very important to understand that we manipulate the language (i.e. the set of syntactic
runs) to achieve this, and do not formulate this as a manipulation of any specific representation of
it. So, even though we operate on sets of syntactic runs, we do not manipulate (bounded) syntactic
structures (grammars, automata, control flow graphs, etc) to achieve this. Syntactic structures are
bounded and assume bounded amount of manipulation; that is, unless one resorts to unfolding and
therefore changing the structures. Languages are unbounded and as such present an unbounded
amount of potential for selection of product programs.

3.1   Contextual Lexicographic Reductions
For every run 𝜌 ∈ 𝑃 ∥ , it suffices that the reduction 𝑃b contains at least one permutation of statements
of 𝜌 while maintaining the order of the statements within each 𝑃𝑖 . All other permutations are
equivalent and it suffices that the entire equivalence class (see Definition 2.4) has at least one of its
elements. This is a commutativity type argument, where pairs of statements from different copies can
be considered to soundly commute, since they operate on disjoint memories. If the goal is to opt for
programs with simpler proofs then we select precisely one representative, since it is generally easier
to prove a program with fewer behaviours correct. Such a language 𝑃b is by definition a minimal
reduction (see Section 2) of 𝑃 ∥ under the commutativity relation I = {(𝑎, 𝑏) | 𝑎 ∈ e   Σ𝑖 , 𝑏 ∈ e
                                                                                                 Σ 𝑗 , 𝑖 ≠ 𝑗 },
the largest sound commutativity relation.
   Note that for any program that is not bounded, there are infinitely many equivalence classes of
I, and as long as these equivalence classes have more than one member, then uncountably many
10                                                                                      Ruotong Cheng and Azadeh Farzan


minimal reductions (see Definition 2.5), each uniquely determined by a selector of representatives
from the equivalence classes under 𝐼 .
     Proposition 3.2. In general, the set of minimal reductions of 𝑃 ∥ under I is not countable.
   Our goal is to introduce an infinite yet finitely representable (and thus countable) subset of
this. To this end, we are interested in a selector (from equivalence classes) that can be finitely
represented. Inspired by [26, 28], we focus on selectors of the form 𝐸 ↦→ min ⪯ (𝐸), where 𝐸 is
an equivalence class, and ⪯ is a contextual lexicographic order, a generalization of the standard
lexicographic orders. We define a contextual order on e  Σ as a map from e
                                                                         Σ∗ to strict partial orders on
Σ (denoted PO(e
e               Σ)); this allows the order on letters to vary according to the left context, which is a
word over eΣ. Each contextual order on e Σ determines a contextual lexicographic order on e    Σ∗ .
   Definition 3.3 (Contextual Lexicographic Order). Given a contextual order ≺: e  Σ∗ → PO(e
                                                                                           Σ), we
                                                    Σ by having 𝜎 ⪯ 𝜌 if and only if
lift ≺ to a contextual lexicographic order (CLO) on e∗

      • 𝜎 is a prefix of 𝜌, or
      • 𝜎 = 𝛼𝑎𝛽 and 𝜌 = 𝛼𝑏𝛾 for some 𝛼, 𝛽, 𝛾 ∈ e Σ∗ and 𝑎, 𝑏 ∈ e
                                                               Σ such that 𝑎 ≺𝛼 𝑏.
  The standard lexicographic orders are the special case where the map ≺ is a constant function
and its image is a total order.
   Proposition 3.4. If ≺ is a contextual order on e  Σ, then the CLO induced by ≺ is a partial order on
Σ∗ . Furthermore, if ≺𝑥 is a total order on e
e                                           Σ for every 𝑥 ∈ e
                                                            Σ∗ , then the CLO induced by ≺ is total.
   Example 3.5 (A Round-Robin1 CLO). Let e    Σ1 = {(, )} and e Σ2 = {[, ]} be the VP alphabet of
                                               Σ=e
parentheses and brackets respectively, and let e  Σ1 ⊎ e
                                                       Σ2 . Define the contextual order ≺ as follows:
                     Σ∗ such that 𝑤 is nonempty and well-matched,
for any words 𝑥, 𝑤 ∈ e
                                                      𝑥( ↦→ [ < ( < ) < ]
                                                    𝑥(𝑤 ↦→ ) < ( < [ < ]
                                                    𝑥[𝑤 ↦→ ] < [ < ( < )
                                             otherwise ↦→ ( < [ < ] < )
Intuitively, ≺ simulates round-robin scheduling and it enforces well-nestedness. Let ⪯ be the CLO
induced by the contextual order ≺. Consider 𝛼 = ([()]), 𝛽 = (([])), and 𝛾 = ([(])). They are
in the same equivalence class under I, and we have 𝛼 ⪯ 𝛽 and 𝛼 ⪯ 𝛾. Note that 𝛽 does not follow a
round-robin scheduling and 𝛾 is ill-nested, and 𝛼 is selected over both by this CLO.            □
  If ⪯ is a CLO, the set of ⪯-minimal representatives of the equivalence classes, induced by a
commutativity relation 𝐼 , of a language 𝐿 form a lex reduction of 𝐿.
                                                           Σ and 𝐼 ⊆ e
  Definition 3.6 (Lex Reduction). Let 𝐿 be a language over e         Σ ×e
                                                                        Σ a commutativity relation.
The reduction of 𝐿 induced by contextual order ≺ on Σ is defined as
                                                       e
                       red𝐼,≺ (𝐿) := {𝑤 ∈ 𝐿 | ∀𝑢 ∈ 𝐿 : 𝑢 ≡𝐼 𝑤 ∧ 𝑢 ⪯ 𝑤 =⇒ 𝑢 = 𝑤 },
where ⪯ is the CLO induced by ≺.
  If ⪯ is total, then red𝐼,≺ (𝐿) is a minimal reduction. For simplicity, we assume from now on that
the contextual orders in consideration map words over e  Σ to strict total orders on e
                                                                                     Σ (denoted TO(e
                                                                                                   Σ)),
which is a sufficient (but not necessary) condition for the order yielding a minimal reduction. Recall
that I is the relation that declares any letters from distinct alphabets as commuting. Since we are
1 Round-robin here is an intuitive simplification of (1,1)-lockstep, whose formal definition is presented in Section 6.1.
Products of Recursive Programs for Hypersafety Verification                                            11


strictly interested in this commutativity relation, we use the shorthand notation red ≺ in place of
redI,≺ , since the commutativity relation will always be I.
   Example 3.7. We continue in the setting of Example 3.5. Observe that for any 𝑃 1 ⊂ {(𝑛 )𝑛 : 𝑛 > 0}
and 𝑃 2 ⊂ {[𝑛 ]𝑛 : 𝑛 > 0}, the reduction red ≺ (𝑃 1 ∥ 𝑃 2 ) is precisely the round-robin like scheduling
of 𝑃1 and 𝑃2 that also enforces well-nestedness.
  If 𝐼 is a sound commutativity relation (such as I in the hypersafety context), then any reduction
under 𝐼 can be verified in place of the original program (Theorem 2.6). This naturally applies to lex
reductions, which we restate as follows:
  Theorem 3.8 (Soundess of Lex Reductions). Let 𝐼 be a sound commutativity relation over e         Σ∗ and
                        Σ. The lex reduction red𝐼,≺ (𝑃1 ∥ . . . ∥ 𝑃𝑛 ) satisfies the Soundness condition.
≺ a contextual order on e
 We conclude our discussion around lex reductions with the following observations, which
motivate the content of the next section.
  Proposition 3.9. There exists a contextual order ≺ such that red ≺ (𝑃1 ∥ 𝑃2 ) is not context-free.
There also exists a contextual order ≺ such that red ≺ (𝑃1 ∥ 𝑃2 ) contains ill-nested words.

3.2   Visibly Pushdown Well-Nested Lex Reductions
The conclusion from the results presented in the previous section is that we need to further restrict
the set of lex reductions so that we can get reductions that are well-nested and visibly pushdown.
We achieve this by restricting the set of contextual orders in consideration.
   Definition 3.10 (Visibly Pushdown Contextual Order (VPO)). A contextual order ≺: e        Σ∗ → TO(e  Σ)
is represented by a deterministic VPA 𝐴 = (𝑄 𝐴 , 𝑄 𝐴 , Γ𝐴 , 𝛿𝐴 , 𝑄 𝐴 ) if 𝐴 is complete and there is a map
                                                     in            F

ord : 𝑄 𝐴 → TO(e  Σ) such that for any 𝑤 ∈ e
                                           Σ∗ , if the run of 𝐴 on 𝑤 ends at state 𝑞, then ≺𝑤 is ord(𝑞).
We call such orders visibly pushdown contextual orders.
   An alternative way of interpreting this definition, for the reader unfamiliar with language theory,
is to think about the contextual order to be definable through a scheduler that has the same
computation power as a visibly pushdown automaton.
   Example 3.11. The contextual order ≺ in Example 3.5 is visibly pushdown, which can be seen as
follows. Under the map ≺, the preimage of each order on e       Σ is a VPL: the four different types of
prefixes (i.e., context) that would lead to the four different choices of orders are all recognizable by
deterministic VPA. Then, the product of the four VPAs (as in the proof of closure under intersection
[2]) can represent the contextual order ≺.
  The set of all minimal runs defined by any visibly pushdown order is visibly pushdown. In
other words, if the order is VP, then all schedules (independent of the choice of language) that are
accepted by the order form a VP language.
                                               Σ∗ ) is visibly pushdown.
  Proposition 3.12. If ≺ is a VPO, then red ≺ (e
  Yet, this result is not strong enough to imply that a minimal reduction of 𝑃1 ∥ · · · ∥ 𝑃𝑛 induced
by a VPO is visibly pushdown or well-nested.
  Proposition 3.13. There exists a VPO ≺ such that red ≺ (𝑃1 ∥ 𝑃2 ) is not context-free. There also
exists a VPO ≺ such that red ≺ (𝑃1 ∥ 𝑃2 ) contains ill-nested words.
  What is the missing piece? Interestingly, there is a correlation between the reduction being
well-nested and it being visibly pushdown. Namely, if we enforce well-nestedness, we get visibly
pushdown for free.
12                                                                                   Ruotong Cheng and Azadeh Farzan


   Theorem 3.14 (Visibly Pushdown Lex Reduction). If ≺ is visibly pushdown and red ≺ (𝑃1 ∥
𝑃2 ) ⊂ wn(𝑃1 ∥ 𝑃2 ), then red ≺ (𝑃 1 ∥ 𝑃2 ) is visibly pushdown.2
   The problem is that the above condition is dependent on the specific choices of 𝑃𝑖 ’s and is
rather non-constructive (or equivalently hard to check). To obtain a condition on the order alone,
independent of 𝑃𝑖 ’s, we introduce the concept of coherent contextual orders. Intuitively, a coherent
contextual order deprioritizes any returns that do not match the last open/pending call, because if
the non-matching return is prioritized, then one ends up violating well-nestedness. Formally:
  Definition 3.15 (Coherent Contextual Order). Let e    Σ𝑖 be VP alphabets (𝑖 = 1, 2) and e
                                                                                          Σ=eΣ1 ⊎ e
                                                                                                  Σ2 . A
contextual order ≺ on Σ is said to be coherent if for any word 𝑢 ∈ Σ and 𝑖 ∈ {1, 2}, if 𝑢 has pending
                        e                                             e ∗

calls and the last one is from Σ𝑖call , then for any letter 𝑎 ∈ e
                                                                Σ𝑖 and 𝑟 ∈ 𝑗≠𝑖 Σret
                                                                          Ð
                                                                                  𝑗 , we have 𝑎 ≺𝑢 𝑟 .

  Example 3.16. The contextual order ≺ in Example 3.5 is coherent. For instance, if 𝑢 = 𝑥(𝑤, then
the last pending call in 𝑢 is ( ∈ Σcall
                                   1 , and we can verify that 𝑎 ≺𝑢 ] for all 𝑎 ∈ Σ1 .
                                                                                 e

   For specific languages 𝑃1, 𝑃2 , coherency is not a necessary condition for the well-nestedness of
red ≺ (𝑃1 ∥ 𝑃2 ). For instance, the word 𝑢 that witnesses the violation of coherency may not occur as
a prefix in the shuffle 𝑃1 ∥ 𝑃2 at all. However, coherency is always a sufficient condition.
  Proposition 3.17. Let ≺ be a coherent contexual order on e  Σ=e  Σ1 ⊎ e
                                                                        Σ2 and 𝑃1, 𝑃2 be well-matched
VPLs over Σ1, Σ2 respectively. Then red ≺ (𝑃1 ∥ 𝑃2 ) ⊂ wn(𝑃1 ∥ 𝑃2 ).
          e   e

  Note that a coherent contextual order is not necessarily visibly pushdown, and vice versa. As a
consequence of Theorem 3.14 and Proposition 3.17, we can conclude that the combination of the
two properties in an order is sufficient to guarantee that it induces a reduction that is both visibly
pushdown and well-nested.
  Theorem 3.18 (VP and Coherent Contextual Order). If ≺ is a visibly pushdown and coherent
contextual order, then red ≺ (𝑃1 ∥ 𝑃2 ) is visibly pushdown and well-nested.
  Once we know a reduction is visibly pushdown, we know that it is theoretically constructible.
However, in the next section, we take a closer look at what is the best way of algorithmically
constructing a visibly pushdown and well-nested red ≺ (𝑃1 ∥ 𝑃2 ).

4     Constructing Reductions
A language 𝐿 over e   Σ is called closed under a commutativity relation 𝐼 if each equivalence class of 𝐼
is either entirely included in 𝐿 or none of the members appear in 𝐿. For example, 𝑃1 ∥ . . . ∥ 𝑃𝑛 is by
definition closed under any commutativity relation that does not reorder statements from the same
𝑃𝑖 . It is straightforward to see that if 𝐿 is closed under 𝐼 then
                                                                Σ∗ ) ∩ 𝐿.
                                           red𝐼,≺ (𝐿) = red𝐼,≺ (e                                                    (1)
This simple observation puts forward an algorithmic path for the construction of the reductions
in the iterative case [26–28]. The generic language red𝐼,≺ (eΣ∗ ), which is somewhat independent of
any given verification instance and is purely defined based on an alphabet of statements, can be
constructed by an adaptation of the idea of sleep sets [29]. Then, any reduction can be constructed
through a simple construction of the intersection of this generic language and the baseline parallel
product 𝑃1 ∥ . . . ∥ 𝑃𝑛 . The proof of Theorem 3.18 puts forward a similar type of construction for
the visibly pushdown case. However, this is unsatisfactory in two orthogonal ways:
2 For notational simplicity, the statement is made only for two components, but this theorem and the ones below also hold

for 𝑛 > 2 components.
Products of Recursive Programs for Hypersafety Verification                                                     13


   (1) Complexity: the construction is generic and does not exploit properties of the commutativity
       relation. We are primarily interested in the commutativity relation I, and as we demonstrate
       in Section 4.3, there is a construction that is strictly simpler under the assumption that all
       copies fully commute and the stack alphabet is small.
   (2) Burden on user: Theorem 3.18 demands two independent conditions on the order. The visibly
       pushdown condition on the order is rather trivial; if the order can be expressed in a specific
       template (grammar or automata), then it is visibly pushdown. However, the coherence
       condition is an extra burden to check/verify, which should ideally be avoidable.
Here, we give an alternative construction of VP lex reductions that overcomes these restrictions.

4.1 Well-nested Shuffle
Recall that the role of the coherence condition is to ensure that the reduction only includes well-
nested alignments, or in other words, it is a subset of wn(𝑃1 ∥ . . . ∥ 𝑃𝑛 ). It turns out that the latter
is an object that is interesting on its own, and we can define it in a more elegant way using a new
binary composition operator:
  Definition 4.1 (Well-Nested Shuffle). For languages 𝐿1, . . . , 𝐿𝑛 respectively over disjoint alphabets
Σ1, . . . , e
e           Σ𝑛 , define the well-nested shuffle 𝐿1 ⧛ · · · ⧛𝐿𝑛 as the set of well-nested words in 𝐿1 ∥ · · · ∥ 𝐿𝑛 .
  We observe that well-nested shuffle is associative, so the well-nested shuffle of 𝑛 languages for
any 𝑛 > 1 is well-defined. For well-matched languages 𝐿1, 𝐿2 , we have 𝐿1 ; 𝐿2 ⊂ 𝐿1 ⧛ 𝐿2 ⊂ 𝐿1 ∥ 𝐿2 .
  Theorem 4.2 (Closure). Visibly pushdown languages are closed under the well-nested shuffle.
   This is significant, because the same is not true for the standard shuffle operator. If we view
programs 𝑃 1 , . . . , 𝑃𝑛 as languages of their behaviours, then the program 𝑃1 ⧛ · · · ⧛ 𝑃𝑛 is the maximal,
in terms of the set of its behaviours, program consisting of arbitrary alignments of behaviours of
𝑃1 , . . . , 𝑃𝑛 that can be executed using a single stack.
   The well-nested shuffle is a construction of interest, independent of the specific problem of
constructing lex reductions. We further remark on this in Section 5.

4.2   Visibly Pushdown Lex Reductions as Reductions of The Well-Nested Shuffle
When a contextual order ≺ defines a reduction of 𝑃1 ∥ · · · ∥ 𝑃𝑛 , coherency of ≺ guarantees that only
well-nested words are selected from it. If we can alternatively define a reduction as a restriction
of 𝑃1 ⧛ · · · ⧛ 𝑃𝑛 , it will by definition include only well-nested words. There is, however, a major
technical challenge in achieving this goal: the construction path of Theorem 3.18 relies on the
validity of Equation 1, which in turn relies on the closedness of the language. 𝑃1 ⧛ · · · ⧛ 𝑃𝑛 is not
closed (w.r.t. I), because swapping a pair of adjacent calls or returns may break well-nestedness.
   Our alternative construction relies on a new insight: any VPO ≺ can be repaired to a coherent
(Definition 3.15) VPO ≺′ such that for any well-matched 𝜌, 𝜏 ∈ wn(e     Σ∗ ) such that 𝜌 ≡I 𝜏, we have
𝜌 ⪯ 𝜏 ⇒ 𝜌 ⪯ 𝜏. We can construct ≺ as follows: for any 𝑎, 𝑏 ∈ Σ and 𝑢 ∈ e
                ′                         ′                                   Σ∗ , with 𝑅𝑘 := 𝑗≠𝑘 Σret
                                                                                             Ð
                                                                                                    𝑗 ,
                                                                    e
           (
              ((𝑎 ∈ 𝑅𝑘 ↔ 𝑏 ∈ 𝑅𝑘 ) ∧ 𝑎 ≺𝑢 𝑏) ∨ (𝑎 ∉ 𝑅𝑘 ∧ 𝑏 ∈ 𝑅𝑘 ), if 𝑢 has a last pending call from e Σ𝑘
𝑎 ≺𝑢′ 𝑏 ≡
              𝑎 ≺𝑢 𝑏.                                                otherwise
  Lemma 4.3. For any VPO ≺, there exists a coherent VPO ≺′ such that red ≺ (𝑃1 ⧛ · · · ⧛ 𝑃𝑛 ) =
red ≺ ′ (𝑃1 ∥ · · · ∥ 𝑃𝑛 ) for any well-matched languages 𝑃1, . . . , 𝑃𝑛 over disjoint VP alphabets.
   This leads to the key theorem of this section that links a family of VPL reductions to the family
of visibly pushdown contextual orders by construction:
14                                                                           Ruotong Cheng and Azadeh Farzan


  Theorem 4.4 (Visibly Pushdown Lex Reduction). If ≺ is a visibly pushdown contextual order
and 𝑃1, . . . , 𝑃𝑛 are VPLs, then so is red ≺ (𝑃1 ⧛ · · · ⧛ 𝑃𝑛 ).
   The theorem is a consequence of Theorem 3.18 (a generic construction via sleep sets) and Lemma
4.3 and yields an automaton of 𝑂 (𝑞𝑛 𝑞𝐴𝑛 2 | Σ | ) states, assuming the VPA for each 𝑃𝑖 has 𝑂 (𝑞) states
                                            e

and the VPA representing the contextual order has 𝑂 (𝑞𝐴 ) states. Next, we argue that under the
assumption of full commutativity, one can do better than this.

4.3    Optimized Construction Specific to Hypersafety
Remarkably, it turns out that one can exploit the assumption of a full commutativity relation,
applicable in all hypersafety verification instances, to devise a simple construction for the VPA,
resulting in a more efficient algorithm. Consider two singleton well-matched languages {𝜌 1 } and
{𝜌 2 }. Under the assumption of full commutativity between the two alphabets, the lex reduction
red ≺ ({𝜌 1 } ⧛ {𝜌 2 }), which consists of exactly one word, can be computed in a greedy manner: If
we have correctly interleaved the prefixes 𝜌 1′ , 𝜌 2′ of 𝜌 1, 𝜌 2 as 𝜎, then the next letter is the smaller
one of the letters following 𝜌 1′ , 𝜌 2′ that do not break well-nestedness: if 𝜎 contains a pending call
and the last one is from e   Σ𝑖 , then the next letter is not from any Σret𝑗 such that 𝑗 ≠ 𝑖.
   With modest assumptions on the order, this idea can be applied to the construction of red ≺ (𝑃 1 ⧛𝑃2 )
as well. An order ≺ is uniform w.r.t. VPA 𝑃1, 𝑃2 if for any pair of states 𝑞 1, 𝑞 2 from 𝑃1, 𝑃2 , for any
𝑤 ∈e   Σ∗ , ≺𝑤 ranks outgoing letters of 𝑞 1, 𝑞 2 consistently, i.e., if some outgoing letter from 𝑞 1 is
less than some outgoing letter from 𝑞 2 , then all outgoing letters from 𝑞 1 are less than all outgoing
letters from 𝑞 2 . If the VPAs are directly obtained from code, the only operational restriction is that
the then and else branches of a component have to be ordered the same way against actions of
another component. The uniformity condition is not practically limiting, as one can always adjust
𝑃1 and 𝑃2 (while preserving the language) to accommodate the order. For instance, any VPA can
be converted in linear time to one such that for every state, the outgoing letters are all internals,
all calls, or all returns. For a uniform VP contextual order, we can construct a compact VPA for
red ≺ (𝑃1 ⧛ 𝑃 2 ) in the same greedy manner:
   Theorem 4.5. Let ≺ be a uniform VP order represented by VPA 𝐴. Then the lex reduction red ≺ (𝑃 1 ⧛
𝑃2 ) is recognized by a VPA with 𝑂 (𝑛 1𝑛 2𝑛𝐴𝑛 Γ ) states, where 𝑛 1 , 𝑛 2 , and 𝑛𝐴 are the number of states of
𝑃1 , 𝑃2 , and 𝐴 respectively and 𝑛 Γ is the sum of the size of the stack alphabets of 𝑃1 and 𝑃2 .
   As outlined in Section 8, one can convert an automaton to a grammar using a standard con-
struction [3] or verify this automaton directly. Directly constructing a VPG for the same language
is not straightforward, since the contextual information (used by the contextual order) needs to
propagate not in a top-down manner but through the linear and hierarchical edges.

5     Sound Reductions for Concurrency
As an underapproximation of the shuffle, the well-nested shuffle and its lex reductions are classic
recursive programs that can always be used for bug finding for recursive concurrent programs.
  In the hypersafety context, it is sound to consider only behaviours of 𝑃1 ∥ · · · ∥ 𝑃𝑛 that are
subsets of 𝑃1 ⧛ · · · ⧛ 𝑃𝑛 , since under the assumption that 𝑃𝑖 ’s are fully disjoint, we have
                     {pre} 𝑃1 ⧛ · · · ⧛ 𝑃𝑛 {post} =⇒ {pre} 𝑃1 ∥ . . . ∥ 𝑃𝑛 {post}.                         (2)
  In the presence of shared memory, there may be dependency between different components. It is
then no longer the case that any run of 𝑃1 ∥ · · · ∥ 𝑃𝑛 can be soundly rearranged to be well-nested
and condition 2 may no longer hold. We outline under what assumptions about 𝑃𝑖 ’s, we can recover
this property for shared memory concurrent programs, so the well-nested shuffle can also be
soundly verified in place of the original recursive concurrent program.
Products of Recursive Programs for Hypersafety Verification                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                15


   Consider a simple case of tail-recursive programs first. Since a tail-recursion can be transformed
to a standard iteration, one intuitively expects this case to be problem-free, and it is. Assume 𝑃1 and
𝑃2 each make a single call of a tail-recursive function, resulting in runs 𝜌 1 ∈ 𝑃 1 and 𝜌 2 ∈ 𝑃2 . Since a
return statement is always a local operation and therefore soundly commutes with any statement
from other components, one can commute the return statements to make any interleaving of 𝜌 1
and 𝜌 2 well-nested while preserving semantics. For example, below, the last (pink) return can be
commuted to turn the run to a semantically equivalent well-nested one.
                [ ...[ ...[ ...( ...( ...) ] ] ] )      [ ...[ ...[ ...( ...( ...) ) ] ] ]
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         <latexit sha1_base64="8H5X6Dq1QG1iHmYGAEKtPZUu4pA=">AAACL3icbVDLSsNAFJ3UV62vqks3g0XoQkqSSh+7ohuXFewD0lAm00k7dPJgZiKUkP/wN/wBt/oH4kZcCf6Fk7SCbT0wcDjnnrmX44SMCqnr71puY3Nreye/W9jbPzg8Kh6fdEUQcUw6OGAB7ztIEEZ90pFUMtIPOUGew0jPmd6kfu+BcEED/17OQmJ7aOxTl2IklTQsmvEg+8TiY8eO9Uq93jSv6pd6Rc+gSLXRrDYbCSzDwSiQAibDYunXhuvEWJASWKA9LH6pJI484kvMkBCWoYfSjhGXFDOSFAaRICHCUzQmlqI+8oiw4+ysBF4oZQTdgKvnS5ipfxMx8oSYeY6a9JCciFUvFf/zrEi6DTumfhhJ4uP5IjdiUAYwLQqOKCdYspkiCHOqboV4gjjCUtW5tCWVlZgWY6zWsE66ZsWoVWp3Zql1vagoD87AOSgDA9RBC9yCNugADB7BM3gBr9qT9qZ9aJ/z0Zy2yJyCJWjfP/mKpZA=</latexit>   <latexit sha1_base64="zhTDdSY1k/vJ110q/gLy7i/dnYs=">AAACMHicbVDLSgMxFM34rPU16tJNsAgVZJhppY9d0Y3LCvYB7VAyaaYNzWSGJCOUoR/ib/gDbvUPdCVuXPgVZtoKtvVA4HDOPbmX40WMSmXb78ba+sbm1nZmJ7u7t39waB4dN2UYC0waOGShaHtIEkY5aSiqGGlHgqDAY6TljW5Sv/VAhKQhv1fjiLgBGnDqU4yUlnpmMelOP+mIgecmtlUuVwtX5UvbsqfQpFipFquVCczDbj9UEl5Membu14erxJmTHJij3jO/dBTHAeEKMyRlx7Ej5SZIKIoZmWS7sSQRwiM0IB1NOQqIdJPpXRN4rpU+9EOhH1dwqv5NJCiQchx4ejJAaiiXvVT8z+vEyq+4CeVRrAjHs0V+zKAKYdoU7FNBsGJjTRAWVN8K8RAJhJXuc2FLKmsxLcZZrmGVNAuWU7JKd4Vc7XpeUQacgjOQBw4ogxq4BXXQABg8gmfwAl6NJ+PN+DA+Z6NrxjxzAhZgfP8AbjClww==</latexit>   <latexit sha1_base64="LuEP5FGNmOc8ge0/JWEAiiDmU7M=">AAACK3icbZDLSsNAFIYn9VbrrerSzWARFCQkrTTtrujGZQV7gTSUyXTaDp1cmJkIJeQtfA1fwK2+gSvFrT6Hk7SCbT0w8PP958w5/G7IqJCG8a7l1tY3Nrfy24Wd3b39g+LhUVsEEcekhQMW8K6LBGHUJy1JJSPdkBPkuYx03MlN6nceCBc08O/lNCSOh0Y+HVKMpEL9oh73sk9sPnKd2NAtq16+si4N3chKiUqtXqnXEgjhBUz6xdKvBVeFORclMK9mv/jdGwQ48ogvMUNC2KYRSidGXFLMSFLoRYKECE/QiNhK+sgjwomzkxJ4psgADgOuni9hRv9OxMgTYuq5qtNDciyWvRT+59mRHNacmPphJImPZ4uGEYMygGlIcEA5wZJNlUCYU3UrxGPEEZYqyoUtKVYwDcZcjmFVtMu6WdWrd+VS43oeUR6cgFNwDkxggQa4BU3QAhg8gmfwAl61J+1N+9A+Z605bT5zDBZK+/oBD5Gjcw==</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              <latexit sha1_base64="8FD0CU4dAiCLm7lSSQPSfTH+fzQ=">AAACL3icbVDLSsNAFJ3UV62vqks3g0VwISWJIW13RTcuK9gHpKFMptN26OTBzEQoIf/hb/gDbvUPxI24EvwLJ20WtvXAwOGcc+dejhcxKqSuf2iFjc2t7Z3ibmlv/+DwqHx80hFhzDFp45CFvOchQRgNSFtSyUgv4gT5HiNdb3qb+d1HwgUNgwc5i4jro3FARxQjqaRB2Uz6808cPvbcRK/qtmk1zCu9all1u2ErUrNqhn2dQgf2h6EUMB2UKyo3B1wnRk4qIEdrUP5Wkzj2SSAxQ0I4hh5JN0FcUsxIWurHgkQIT9GYOIoGyCfCTeZnpfBCKUM4Crl6gYRz9e9EgnwhZr6nkj6SE7HqZeJ/nhPLUd1NaBDFkgR4sWgUMyhDmBUFh5QTLNlMEYQ5VbdCPEEcYanqXNqSyUrMijFWa1gnHbNq2FX73qw0b/KKiuAMnINLYIAaaII70AJtgMETeAGv4E171t61T+1rES1o+cwpWIL28wtglaXP</latexit>   <latexit sha1_base64="8FD0CU4dAiCLm7lSSQPSfTH+fzQ=">AAACL3icbVDLSsNAFJ3UV62vqks3g0VwISWJIW13RTcuK9gHpKFMptN26OTBzEQoIf/hb/gDbvUPxI24EvwLJ20WtvXAwOGcc+dejhcxKqSuf2iFjc2t7Z3ibmlv/+DwqHx80hFhzDFp45CFvOchQRgNSFtSyUgv4gT5HiNdb3qb+d1HwgUNgwc5i4jro3FARxQjqaRB2Uz6808cPvbcRK/qtmk1zCu9all1u2ErUrNqhn2dQgf2h6EUMB2UKyo3B1wnRk4qIEdrUP5Wkzj2SSAxQ0I4hh5JN0FcUsxIWurHgkQIT9GYOIoGyCfCTeZnpfBCKUM4Crl6gYRz9e9EgnwhZr6nkj6SE7HqZeJ/nhPLUd1NaBDFkgR4sWgUMyhDmBUFh5QTLNlMEYQ5VbdCPEEcYanqXNqSyUrMijFWa1gnHbNq2FX73qw0b/KKiuAMnINLYIAaaII70AJtgMETeAGv4E171t61T+1rES1o+cwpWIL28wtglaXP</latexit>   <latexit sha1_base64="8FD0CU4dAiCLm7lSSQPSfTH+fzQ=">AAACL3icbVDLSsNAFJ3UV62vqks3g0VwISWJIW13RTcuK9gHpKFMptN26OTBzEQoIf/hb/gDbvUPxI24EvwLJ20WtvXAwOGcc+dejhcxKqSuf2iFjc2t7Z3ibmlv/+DwqHx80hFhzDFp45CFvOchQRgNSFtSyUgv4gT5HiNdb3qb+d1HwgUNgwc5i4jro3FARxQjqaRB2Uz6808cPvbcRK/qtmk1zCu9all1u2ErUrNqhn2dQgf2h6EUMB2UKyo3B1wnRk4qIEdrUP5Wkzj2SSAxQ0I4hh5JN0FcUsxIWurHgkQIT9GYOIoGyCfCTeZnpfBCKUM4Crl6gYRz9e9EgnwhZr6nkj6SE7HqZeJ/nhPLUd1NaBDFkgR4sWgUMyhDmBUFh5QTLNlMEYQ5VbdCPEEcYanqXNqSyUrMijFWa1gnHbNq2FX73qw0b/KKiuAMnINLYIAaaII70AJtgMETeAGv4E171t61T+1rES1o+cwpWIL28wtglaXP</latexit>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      <latexit sha1_base64="Ez+p/ynbgaP2o+ZlQBlp4udH2SQ=">AAACKXicbVDLSsNAFJ34rPVVdelmsAguSkliSNtd0Y3LCvYBbSiT6aQdOnkwMxFKyE/4G/6AW/0Dd+pW8DuctFnY1gMDh3POnXs5bsSokLr+qW1sbm3v7Bb2ivsHh0fHpZPTjghjjkkbhyzkPRcJwmhA2pJKRnoRJ8h3Gem609vM7z4SLmgYPMhZRBwfjQPqUYykkoalSjKYf9LnY9dJ9Kpum1bDrOhVy6rbDVuRmlUz7OsUQicdlsoqMQdcJ0ZOyiBHa1j6GYxCHPskkJghIfqGHkknQVxSzEhaHMSCRAhP0Zj0FQ2QT4STzA9K4aVSRtALuXqBhHP170SCfCFmvquSPpITsepl4n9eP5Ze3UloEMWSBHixyIsZlCHMKoIjygmWbKYIwpyqWyGeII6wVEUubclkJWbFGKs1rJOOWTXsqn1vlps3eUUFcA4uwBUwQA00wR1ogTbA4Am8gFfwpj1r79qH9rWIbmj5zBlYgvb9C65no18=</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         <latexit sha1_base64="LuEP5FGNmOc8ge0/JWEAiiDmU7M=">AAACK3icbZDLSsNAFIYn9VbrrerSzWARFCQkrTTtrujGZQV7gTSUyXTaDp1cmJkIJeQtfA1fwK2+gSvFrT6Hk7SCbT0w8PP958w5/G7IqJCG8a7l1tY3Nrfy24Wd3b39g+LhUVsEEcekhQMW8K6LBGHUJy1JJSPdkBPkuYx03MlN6nceCBc08O/lNCSOh0Y+HVKMpEL9oh73sk9sPnKd2NAtq16+si4N3chKiUqtXqnXEgjhBUz6xdKvBVeFORclMK9mv/jdGwQ48ogvMUNC2KYRSidGXFLMSFLoRYKECE/QiNhK+sgjwomzkxJ4psgADgOuni9hRv9OxMgTYuq5qtNDciyWvRT+59mRHNacmPphJImPZ4uGEYMygGlIcEA5wZJNlUCYU3UrxGPEEZYqyoUtKVYwDcZcjmFVtMu6WdWrd+VS43oeUR6cgFNwDkxggQa4BU3QAhg8gmfwAl61J+1N+9A+Z605bT5zDBZK+/oBD5Gjcw==</latexit>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           <latexit sha1_base64="Ez+p/ynbgaP2o+ZlQBlp4udH2SQ=">AAACKXicbVDLSsNAFJ34rPVVdelmsAguSkliSNtd0Y3LCvYBbSiT6aQdOnkwMxFKyE/4G/6AW/0Dd+pW8DuctFnY1gMDh3POnXs5bsSokLr+qW1sbm3v7Bb2ivsHh0fHpZPTjghjjkkbhyzkPRcJwmhA2pJKRnoRJ8h3Gem609vM7z4SLmgYPMhZRBwfjQPqUYykkoalSjKYf9LnY9dJ9Kpum1bDrOhVy6rbDVuRmlUz7OsUQicdlsoqMQdcJ0ZOyiBHa1j6GYxCHPskkJghIfqGHkknQVxSzEhaHMSCRAhP0Zj0FQ2QT4STzA9K4aVSRtALuXqBhHP170SCfCFmvquSPpITsepl4n9eP5Ze3UloEMWSBHixyIsZlCHMKoIjygmWbKYIwpyqWyGeII6wVEUubclkJWbFGKs1rJOOWTXsqn1vlps3eUUFcA4uwBUwQA00wR1ogTbA4Am8gFfwpj1r79qH9rWIbmj5zBlYgvb9C65no18=</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 <latexit sha1_base64="Ez+p/ynbgaP2o+ZlQBlp4udH2SQ=">AAACKXicbVDLSsNAFJ34rPVVdelmsAguSkliSNtd0Y3LCvYBbSiT6aQdOnkwMxFKyE/4G/6AW/0Dd+pW8DuctFnY1gMDh3POnXs5bsSokLr+qW1sbm3v7Bb2ivsHh0fHpZPTjghjjkkbhyzkPRcJwmhA2pJKRnoRJ8h3Gem609vM7z4SLmgYPMhZRBwfjQPqUYykkoalSjKYf9LnY9dJ9Kpum1bDrOhVy6rbDVuRmlUz7OsUQicdlsoqMQdcJ0ZOyiBHa1j6GYxCHPskkJghIfqGHkknQVxSzEhaHMSCRAhP0Zj0FQ2QT4STzA9K4aVSRtALuXqBhHP170SCfCFmvquSPpITsepl4n9eP5Ze3UloEMWSBHixyIsZlCHMKoIjygmWbKYIwpyqWyGeII6wVEUubclkJWbFGKs1rJOOWTXsqn1vlps3eUUFcA4uwBUwQA00wR1ogTbA4Am8gFfwpj1r79qH9rWIbmj5zBlYgvb9C65no18=</latexit>




                 <latexit sha1_base64="8FD0CU4dAiCLm7lSSQPSfTH+fzQ=">AAACL3icbVDLSsNAFJ3UV62vqks3g0VwISWJIW13RTcuK9gHpKFMptN26OTBzEQoIf/hb/gDbvUPxI24EvwLJ20WtvXAwOGcc+dejhcxKqSuf2iFjc2t7Z3ibmlv/+DwqHx80hFhzDFp45CFvOchQRgNSFtSyUgv4gT5HiNdb3qb+d1HwgUNgwc5i4jro3FARxQjqaRB2Uz6808cPvbcRK/qtmk1zCu9all1u2ErUrNqhn2dQgf2h6EUMB2UKyo3B1wnRk4qIEdrUP5Wkzj2SSAxQ0I4hh5JN0FcUsxIWurHgkQIT9GYOIoGyCfCTeZnpfBCKUM4Crl6gYRz9e9EgnwhZr6nkj6SE7HqZeJ/nhPLUd1NaBDFkgR4sWgUMyhDmBUFh5QTLNlMEYQ5VbdCPEEcYanqXNqSyUrMijFWa1gnHbNq2FX73qw0b/KKiuAMnINLYIAaaII70AJtgMETeAGv4E171t61T+1rES1o+cwpWIL28wtglaXP</latexit>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        <latexit sha1_base64="Ez+p/ynbgaP2o+ZlQBlp4udH2SQ=">AAACKXicbVDLSsNAFJ34rPVVdelmsAguSkliSNtd0Y3LCvYBbSiT6aQdOnkwMxFKyE/4G/6AW/0Dd+pW8DuctFnY1gMDh3POnXs5bsSokLr+qW1sbm3v7Bb2ivsHh0fHpZPTjghjjkkbhyzkPRcJwmhA2pJKRnoRJ8h3Gem609vM7z4SLmgYPMhZRBwfjQPqUYykkoalSjKYf9LnY9dJ9Kpum1bDrOhVy6rbDVuRmlUz7OsUQicdlsoqMQdcJ0ZOyiBHa1j6GYxCHPskkJghIfqGHkknQVxSzEhaHMSCRAhP0Zj0FQ2QT4STzA9K4aVSRtALuXqBhHP170SCfCFmvquSPpITsepl4n9eP5Ze3UloEMWSBHixyIsZlCHMKoIjygmWbKYIwpyqWyGeII6wVEUubclkJWbFGKs1rJOOWTXsqn1vlps3eUUFcA4uwBUwQA00wR1ogTbA4Am8gFfwpj1r79qH9rWIbmj5zBlYgvb9C65no18=</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            <latexit sha1_base64="8H5X6Dq1QG1iHmYGAEKtPZUu4pA=">AAACL3icbVDLSsNAFJ3UV62vqks3g0XoQkqSSh+7ohuXFewD0lAm00k7dPJgZiKUkP/wN/wBt/oH4kZcCf6Fk7SCbT0wcDjnnrmX44SMCqnr71puY3Nreye/W9jbPzg8Kh6fdEUQcUw6OGAB7ztIEEZ90pFUMtIPOUGew0jPmd6kfu+BcEED/17OQmJ7aOxTl2IklTQsmvEg+8TiY8eO9Uq93jSv6pd6Rc+gSLXRrDYbCSzDwSiQAibDYunXhuvEWJASWKA9LH6pJI484kvMkBCWoYfSjhGXFDOSFAaRICHCUzQmlqI+8oiw4+ysBF4oZQTdgKvnS5ipfxMx8oSYeY6a9JCciFUvFf/zrEi6DTumfhhJ4uP5IjdiUAYwLQqOKCdYspkiCHOqboV4gjjCUtW5tCWVlZgWY6zWsE66ZsWoVWp3Zql1vagoD87AOSgDA9RBC9yCNugADB7BM3gBr9qT9qZ9aJ/z0Zy2yJyCJWjfP/mKpZA=</latexit>   <latexit sha1_base64="zhTDdSY1k/vJ110q/gLy7i/dnYs=">AAACMHicbVDLSgMxFM34rPU16tJNsAgVZJhppY9d0Y3LCvYB7VAyaaYNzWSGJCOUoR/ib/gDbvUPdCVuXPgVZtoKtvVA4HDOPbmX40WMSmXb78ba+sbm1nZmJ7u7t39waB4dN2UYC0waOGShaHtIEkY5aSiqGGlHgqDAY6TljW5Sv/VAhKQhv1fjiLgBGnDqU4yUlnpmMelOP+mIgecmtlUuVwtX5UvbsqfQpFipFquVCczDbj9UEl5Membu14erxJmTHJij3jO/dBTHAeEKMyRlx7Ej5SZIKIoZmWS7sSQRwiM0IB1NOQqIdJPpXRN4rpU+9EOhH1dwqv5NJCiQchx4ejJAaiiXvVT8z+vEyq+4CeVRrAjHs0V+zKAKYdoU7FNBsGJjTRAWVN8K8RAJhJXuc2FLKmsxLcZZrmGVNAuWU7JKd4Vc7XpeUQacgjOQBw4ogxq4BXXQABg8gmfwAl6NJ+PN+DA+Z6NrxjxzAhZgfP8AbjClww==</latexit>   <latexit sha1_base64="Ez+p/ynbgaP2o+ZlQBlp4udH2SQ=">AAACKXicbVDLSsNAFJ34rPVVdelmsAguSkliSNtd0Y3LCvYBbSiT6aQdOnkwMxFKyE/4G/6AW/0Dd+pW8DuctFnY1gMDh3POnXs5bsSokLr+qW1sbm3v7Bb2ivsHh0fHpZPTjghjjkkbhyzkPRcJwmhA2pJKRnoRJ8h3Gem609vM7z4SLmgYPMhZRBwfjQPqUYykkoalSjKYf9LnY9dJ9Kpum1bDrOhVy6rbDVuRmlUz7OsUQicdlsoqMQdcJ0ZOyiBHa1j6GYxCHPskkJghIfqGHkknQVxSzEhaHMSCRAhP0Zj0FQ2QT4STzA9K4aVSRtALuXqBhHP170SCfCFmvquSPpITsepl4n9eP5Ze3UloEMWSBHixyIsZlCHMKoIjygmWbKYIwpyqWyGeII6wVEUubclkJWbFGKs1rJOOWTXsqn1vlps3eUUFcA4uwBUwQA00wR1ogTbA4Am8gFfwpj1r79qH9rWIbmj5zBlYgvb9C65no18=</latexit>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        <latexit sha1_base64="Ez+p/ynbgaP2o+ZlQBlp4udH2SQ=">AAACKXicbVDLSsNAFJ34rPVVdelmsAguSkliSNtd0Y3LCvYBbSiT6aQdOnkwMxFKyE/4G/6AW/0Dd+pW8DuctFnY1gMDh3POnXs5bsSokLr+qW1sbm3v7Bb2ivsHh0fHpZPTjghjjkkbhyzkPRcJwmhA2pJKRnoRJ8h3Gem609vM7z4SLmgYPMhZRBwfjQPqUYykkoalSjKYf9LnY9dJ9Kpum1bDrOhVy6rbDVuRmlUz7OsUQicdlsoqMQdcJ0ZOyiBHa1j6GYxCHPskkJghIfqGHkknQVxSzEhaHMSCRAhP0Zj0FQ2QT4STzA9K4aVSRtALuXqBhHP170SCfCFmvquSPpITsepl4n9eP5Ze3UloEMWSBHixyIsZlCHMKoIjygmWbKYIwpyqWyGeII6wVEUubclkJWbFGKs1rJOOWTXsqn1vlps3eUUFcA4uwBUwQA00wR1ogTbA4Am8gFfwpj1r79qH9rWIbmj5zBlYgvb9C65no18=</latexit>




                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          <latexit sha1_base64="8FD0CU4dAiCLm7lSSQPSfTH+fzQ=">AAACL3icbVDLSsNAFJ3UV62vqks3g0VwISWJIW13RTcuK9gHpKFMptN26OTBzEQoIf/hb/gDbvUPxI24EvwLJ20WtvXAwOGcc+dejhcxKqSuf2iFjc2t7Z3ibmlv/+DwqHx80hFhzDFp45CFvOchQRgNSFtSyUgv4gT5HiNdb3qb+d1HwgUNgwc5i4jro3FARxQjqaRB2Uz6808cPvbcRK/qtmk1zCu9all1u2ErUrNqhn2dQgf2h6EUMB2UKyo3B1wnRk4qIEdrUP5Wkzj2SSAxQ0I4hh5JN0FcUsxIWurHgkQIT9GYOIoGyCfCTeZnpfBCKUM4Crl6gYRz9e9EgnwhZr6nkj6SE7HqZeJ/nhPLUd1NaBDFkgR4sWgUMyhDmBUFh5QTLNlMEYQ5VbdCPEEcYanqXNqSyUrMijFWa1gnHbNq2FX73qw0b/KKiuAMnINLYIAaaII70AJtgMETeAGv4E171t61T+1rES1o+cwpWIL28wtglaXP</latexit>   <latexit sha1_base64="8FD0CU4dAiCLm7lSSQPSfTH+fzQ=">AAACL3icbVDLSsNAFJ3UV62vqks3g0VwISWJIW13RTcuK9gHpKFMptN26OTBzEQoIf/hb/gDbvUPxI24EvwLJ20WtvXAwOGcc+dejhcxKqSuf2iFjc2t7Z3ibmlv/+DwqHx80hFhzDFp45CFvOchQRgNSFtSyUgv4gT5HiNdb3qb+d1HwgUNgwc5i4jro3FARxQjqaRB2Uz6808cPvbcRK/qtmk1zCu9all1u2ErUrNqhn2dQgf2h6EUMB2UKyo3B1wnRk4qIEdrUP5Wkzj2SSAxQ0I4hh5JN0FcUsxIWurHgkQIT9GYOIoGyCfCTeZnpfBCKUM4Crl6gYRz9e9EgnwhZr6nkj6SE7HqZeJ/nhPLUd1NaBDFkgR4sWgUMyhDmBUFh5QTLNlMEYQ5VbdCPEEcYanqXNqSyUrMijFWa1gnHbNq2FX73qw0b/KKiuAMnINLYIAaaII70AJtgMETeAGv4E171t61T+1rES1o+cwpWIL28wtglaXP</latexit>




                                                                                                indep
One can further relax the tail-recursion condition to tail-independence. For any e    Σ𝑖 , let e
                                                                                               Σ𝑖     be all
           Σ𝑖 that soundly commute with all letters in other components.
letters in e
  Definition 5.1 (Tail/Head-Independent). We call a component 𝑃𝑖 tail-independent (resp. head-
independent) if every run 𝜌 of 𝑃𝑖 can be written as 𝑢𝑣 (𝑢, 𝑣 ∈ e Σ𝑖∗ ) such that
     • all calls are in 𝑢 and all returns are in 𝑣, except those at a position 𝑗 such that all letters
                                                       indep
       between 𝑗 and its matching position are in e   Σ𝑖     ; and
                                          indep
                                         Σ𝑖
     • all letters in 𝑣 (resp. 𝑢) are in e      .
                                                              indep
                                                      Σ𝑖 and e
  This definition is effective, since given alphabets e      Σ𝑖     , one can construct a VPL 𝑃𝑖max
                                                       max
such that a component 𝑃𝑖 is tail-independent iff 𝑃𝑖 ⊂ 𝑃𝑖 . The same holds for head-independence.
Hence, for any concurrent recursive program, one can algorithmically check if Defintion 5.1 applies.
                                                                       indep
  Proposition 5.2. Given a component 𝑃𝑖 as a VPA and the alphabet e   Σ𝑖     , it is decidable in
polynomial time whether 𝑃𝑖 is tail-independent (or head-independent).
  We can then conclude conditions under which the well-nested shuffle can be soundly used for
verification of a concurrent program:
   Theorem 5.3 (Soundness of Well-Nested Shuffle Under Concurrency). If every component
𝑃𝑖 is tail-independent (or respectively head-independent) then condition (2) is satisfied.
  The well-nested shuffle can be verified as a classic recursive program using classic verification
techniques, without concurrency posing an additional complication. Moreover, as we discuss in
Section 4.2, any sound reduction of it can also be used for the purpose of verification.

6     Canonical Reductions and Their Construction
In Section 3, we introduce lex reductions as an infinite family of recursive product programs. Here,
we introduce a simpler (still infinite) subfamily of lex reductions that are defined based on a set of
building blocks, called canonical reductions, which are intuitive for the programmer to understand,
compose, and use as annotations in hypersafety verification of recursive programs.
   In Section 6.1, we give the formal definitions, and show that this new family is a subset of the lex
reductions. As such, the results from the previous section support the construction of these in the
style presented in Section 4.3. We observe, however, that for this sub-family, one can follow the
inductive definitions and provide a direct VPG construction of a reduction from the family. This
construction yields smaller grammars compared to that of Section 4.3 as we illustrate in Section 8.

6.1    Canonical Reductions for Recursive Programs
We start by giving a formal definition for the nested concatenation, motivated by the distributivity
property of div from Section 1, and then one for the parametric lockstep. We define them on words
for simplicity, since one can lift the definition from words to languages (i.e., sets of words) in the
16                                                                            Ruotong Cheng and Azadeh Farzan


standard way. We formally argue that these are instances of lex reductions, and then use an example
to discuss the expressive power of the simple subfamily.
   Nested Concatenation. The rules in Fig. 3 inductively define a ternary relation 𝑤 1 ⊕ 𝑤 2 → 𝑤,
where 𝑤 1 and 𝑤 2 are well-matched words. The nested concatenation 𝑤 1 ⊕ 𝑤 2 is the word 𝑤 such
that 𝑤 1 ⊕ 𝑤 2 → 𝑤, which can be shown to be uniquely defined and well-matched. We generalize
this from two to 𝑛 words by letting 𝑤 1 ⊕ 𝑤 2 · · · ⊕ 𝑤𝑛 = 𝑤 1 ⊕ (𝑤 2 ⊕ · · · ⊕ 𝑤𝑛 ).

                                    𝑤1 ⊕ 𝑤2 → 𝑤 ′                       𝑤1 ⊕ 𝑤2 → 𝑤 ′
                                                     NC-int                                NC-call
       𝜖 ⊕ 𝑤 2 → 𝑤 2 NC-𝜖          𝑎𝑤 1 ⊕ 𝑤 2 → 𝑎𝑤 ′                 𝑐𝑤 1𝑟𝑣 ⊕ 𝑤 2 → 𝑐𝑤 ′𝑟𝑣

Fig. 3. Definition of nested concatenation: 𝑐, 𝑟 , and 𝑎 respectively stand for a call, a return, or an internal
statement. In 𝑐𝑤𝑟𝑣, the 𝑟 is meant to be the return that matches 𝑐.

   Parametric Lockstep. Next, we define a lockstep product that is parametric on a vector 𝒔 of
positive integers that provides the nominal speed of the movement of each component in the
lockstep synchronization. We define a simple modulo decrement operation for such vectors to
simplify our definition. For vectors of natural numbers 𝒔 and 𝒕 such that |𝒔| = |𝒕 | = 𝑛 > 0, 0 ≤ 𝒕 ≤ 𝒔
(componentwise), and 𝒕 ≠ 𝒔, define
                              (
                                (𝑠 1 − 1, 𝑠 2, . . . , 𝑠𝑛 ),               if 𝒕 = 0
                  dec𝒔 (𝒕) :=
                                (0, . . . , 0, 𝑡𝑖 − 1, 𝑡𝑖+1, . . . , 𝑡𝑛 ). if 𝑖 = min{ 𝑗 : 𝑡 𝑗 > 0}
   LS𝒔 (𝑤 1, . . . , 𝑤𝑛 ) denotes the lockstep composition of the 𝑛 well-matched words at the speed of 𝒔.
To inductively define it, we need an additional helper vector 𝒕. The rules in Fig. 4 define a relation
LS𝒔,𝒕 (𝑤 1, . . . , 𝑤𝑛 ) → 𝑤 ′ , where 𝒔 and 𝒕 are vectors satisfying the constraints above. The 𝒔-lockstep
of 𝑤 1, . . . , 𝑤𝑛 is the unique word 𝑤 ′ such that LS𝒔,0 (𝑤 1, . . . , 𝑤𝑛 ) → 𝑤 ′ .
   Note that the definition is inductive over the structure that exposes the leftmost letter of a word.
This is intentional, for consistency with the definition of CLO (Definition 3.3), which looks at the
left context. However, this is not the only valid choice, and we discuss the alternative in Section 6.2.
   Subfamily of Lex Reductions. Crucially, we can show that the nested concatenation and
𝒔-lockstep of well-matched VPLs over disjoint alphabets can be produced through a VP contextual
order (VPO) as a lex reduction of the well-nested shuffle.
   Proposition 6.1. If 𝑃1, . . . , 𝑃𝑛 are well-matched VPLs over disjoint alphabets, then their concatena-
tion, nested concatenation, and 𝒔-lockstep are lex reductions of 𝑃1 ⧛ · · · ⧛ 𝑃𝑛 induced by VPOs.
  We point out that the VPOs used by the construction are uniform (see Section 4.3) w.r.t. VPA
such that for every state, the outgoing letters are all internals, all calls, or all returns. Combining
Proposition 6.1 and Theorem 4.4, we have the following theorem:
   Theorem 6.2. If 𝑃1, . . . , 𝑃𝑛 are well-matched VPLs over disjoint alphabets, then any reduction built
from a combination of concatenation, nested concatenation, and 𝒔-lockstep and one occurrence of each
𝑃𝑖 is a VP reduction of 𝑃1 ⧛ · · · ⧛ 𝑃𝑛 .
   Expressive Power. Superficially, nested concatenation and parametric lockstep may seem
simple and trivial. As we illustrate empirically in Section 8, their compositions yields a powerful
family that can solve nearly all our benchmarks. However, to discuss this in depth, let us look at
an example borrowed from [14], which puts forward a solution for constructing semantic product
programs. Our reductions are syntactic and as we remark in Section 8.4, this implies a strict
limitation compared to semantic ones. However, as we demonstrate using the example below, the
Products of Recursive Programs for Hypersafety Verification                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  17


                                          LS𝒔 ′,𝒕 ′ (𝑤 1, . . . , 𝑤 𝑗 −1, 𝑤 𝑗+1, . . . 𝑤𝑛 ) → 𝑤 ′ 𝒔 ′, 𝒕 ′ ← 𝒔 − 𝑗 , 𝒕 − 𝑗
                        LS-single                                                                                          LS-𝜖
 LS𝒔,𝒕 (𝑤 1 ) → 𝑤 1                                    LS𝒔,𝒕 (𝑤 1, . . . , 𝑤 𝑗 −1, 𝜖, 𝑤 𝑗+1, . . . 𝑤𝑛 ) → 𝑤 ′

  LS𝒔,𝒕 (𝑤 1, . . . , 𝑤𝑛 ) → 𝑤 ′ none of 𝑤𝑖 where 𝑖 < 𝑚 starts with an internal
                                                                                LS-int
                      LS𝒔,𝒕 (𝑤 1, . . . , 𝑤𝑚−1, 𝑎𝑤𝑚 , 𝑤𝑚+1, . . . , 𝑤𝑛 ) → 𝑤 ′

      LS𝒔,dec𝒔 (𝒕 ) (𝑤 1, 𝑐 2𝑤 2𝑟 2, . . . , 𝑐𝑛𝑤𝑛 𝑟𝑛 ) → 𝑢 ′ 𝒕 = 0 LS𝒔,𝒕 (𝑣 1, . . . , 𝑣𝑛 ) → 𝑣 ′
                                                                                                  LS-call-1st
                           LS𝒔,𝒕 (𝑐 1𝑤 1𝑟 1𝑣 1, . . . , 𝑐𝑛𝑤𝑛 𝑟𝑛 𝑣𝑛 ) → 𝑐 1𝑢 ′𝑟 1𝑣 ′

LS𝒔,dec𝒔 (𝒕 ) (. . . , 𝑐𝑚−1𝑤𝑚−1𝑟𝑚−1, 𝑤𝑚 , 𝑐𝑚+1𝑤𝑚+1𝑟𝑚+1, . . . ) → 𝑢 ′ 𝒕 ≠ 0 𝑚 = min{𝑖 : 𝑡𝑖 > 0}
                                                                                                LS-call
                             LS𝒔,𝒕 (𝑐 1𝑤 1𝑟 1𝑣 1, . . . , 𝑐𝑛𝑤𝑛 𝑟𝑛 𝑣𝑛 ) → 𝑐𝑚𝑢 ′𝑐𝑚 𝑣𝑚

Fig. 4. Inductive defintion of parametric lockstep. 𝒔 − 𝑗 denotes the vector obtained from 𝒔 by dropping the
𝑗-th component, and similar for 𝒕 − 𝑗 .



combination of canonical reductions with slight customizations, which operate on unbounded and
rich syntax, can be surprisingly powerful.
   Consider the functions 𝑓 and 𝑔 illustrated on def g(n: nat, m: nat, i: nat, k: nat) -> nat
                                                               <latexit sha1_base64="r6OqOGpO3EzWeV4LOLHegpCa6tI=">AAAGGXicjVTNbtNAEHbbBEr4a+HYy4qoUitMlQRRECKoUAl64FAo/ZGSKFqvx+kqu2uzu24bGT8JT8MNceXEA/AejB23qpuo6VrWjmfmm5/Ps+tFghvbaPydm1+oVG/dXrxTu3vv/oOHS8uPDkwYawb7LBShPvKoAcEV7FtuBRxFGqj0BBx6w+3MfngC2vBQfbWjCHqSDhQPOKMWVf3lhX+rXWGsCKkvqBrEdAAm6ewdUx31tt1dahgVaS33MWCTgGt0xlztlitoIb5wz6HtJBoj0to54sL0zqdujVxZDIOYMAjQs92YNGNnnBk7EtDuWhtQycWo66G35mAm3YcwOg21XwBychJPxJBegCcxxmquBiWIBv86BAulBGVLkIEGUNeBZKihALY7otcpcPg3UEPTXtKtp9fT03TJ1KjnTbcTA99cruyUONOI+YBYYz/mhU8JfTl1a2ZqHwJXgJTUxb/PXISCti4oE2MSV9IzV3LlEkVvWt0X8A94KMDOqu35zNp2QomPjo65kXuxdImJ5Q2rOOTC37Oannqg9WhWKY0ajr0HA66S7Ejh4cXJSmvIDRmsqddZ9y6Rxc6LfZjv6+TZ22zP4vOAcPKGIKDINiRtfJ8SeekbA2IsDIN6nIzhembTYGOtyLDWBeWXaugv1RsbjXyRSaFZCHWnWLv95bmVrh+yOBvYvMdOsxHZXkK15UwANhobiCgb4gB3UFRUguklOW0pWUWNT4JQ46ssybWXEQmVxoykh56S2mNz1ZYpL2yrpVQ2eNVLuIpiC4qNMwWxIDYk2fVGfI7nzIoRCpRpjsUShpcZZRYvwVKaghtTbsU/4ZEpmjkbd1NCWY6mFOlsXiVvUjhobTQ3NzY/t+pb7wtiF50V54mz5jSdl86Ws+PsOvsOq3yq6EpS+V79Uf1Z/VX9PXadnyswj53Sqv75D3nm14Y=</latexit>




the right and the goal of proving them equiv-            if i < n:
                                                            k = k + m
alent. They both increment 𝑘 by 𝑚 for 𝑛 times;              k = g(n, m, i + 1, k)
the only difference is that in 𝑓 , the number 𝑚 is       return k
computed by an auxiliary function ℎ as the sum defiff(n:         nat, m: nat, i: nat, k: nat) -> nat
                                                               <latexit sha1_base64="As9PQLjecyMXYmoJ0jX3iqL1C0I=">AAAGHHicjVTbbtNAEHXbBEq4tfDYlxVRpVY1lRNEQYigQiXoG4XSi5RE1doeJ6vsrs3uum1kGf6Er+EN8YrEH/AZjB2nqpuo6UbRjmbmzJw53l034kwbx/k7N79Qqd66vXindvfe/QcPl5YfHeowVh4ceCEP1bFLNXAm4cAww+E4UkCFy+HIHexk8aNTUJqF8osZRtAVtCdZwDxq0HWyvPBvtcO14SH1OZW9mPZAJ+39PlVRd8feo9qjPK3lORpMEjCFydir1bQ5Lczn9hjaSqIRIq2NERehtz61a+TK8rCIDoMAM1vOZBgnY542Qw6tjjEBFYwPOy5mKwZ6Mn0Aw7NQ+QUgFydxeQzpBXgSo41isleCKPCvQ3ihECBNCdJTAPI6kAgVFMBWm3fbBQ6/Bnpo2k069fR6eRo2mVp1PHQr0fDVZtJMqTNNmPeI1eZDTnxK6cutmzNb+xDYHISgNn59z0YoKGOD1DE2sQU9twWTNpH0puw+g3/IQg5mFrdnM7nthgJ/KuozLfZjYZONG3I4YtzfN4qeuaDUcBYRp4aH3oUek0l2ofDq4rlKa6gMCdbkq2x2m4hiZ8U+yPd18vRNtmf1WUAYeU0QUHQbkBbpryFtB9PXLzmxKhbEWmSDNMYxBSZWkgxqHZB+icjJUt3ZdPJFJo1GYdStYu2dLM+tdPzQi7Mzmw/abjiR6SZUGeZxwGljDRH1BniG22hKKkB3k1y7lKyixydBqPAvDcm9lxEJFVoPhYuZgpq+vhrLnBex1VIrE7zsJkxGsQHpjToFMScmJNkLR3yGV83wIRrUUwzJEg/fM+oZfAdLbQptdHkU/5RFuhjmfDRNCWUYhlKUs3FVvEnjsLnZ2Nrc+tSsb78rhF20Vqwn1prVsF5Y29autWcdWF7lYyWufKt8r/6o/qz+qv4epc7PFZjHVmlV//wHsj/Xjg==</latexit>




                                                            i < n:
of 𝑚 1’s. They appear in Figure 12 from [14],               k = h(m, 0, k)
where an iterative version of this is cited as              k = f(n, m, i + 1, k)
                                                         return k
a challenge for verification using product pro-
                                                      def h(m: nat, j: nat, k: nat) -> nat
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        <latexit sha1_base64="bHWJ6wfZTaCwO4+Kxb6qdMJqh4s=">AAAF/XicjZTdbtMwFIAz1sIofxtc7saimrSJMKVFDIQoGkyCXQ7GukltVZzkpPVqO8F2tlVRxNNwh7jlGXgE3oaTNJuWtVrnKPKRz/nOn3/ciDNtHOffwq3FSvX2naW7tXv3Hzx8tLzyuK3DWHlw4IU8VEcu1cCZhAPDDIejSAEVLodDd7ST6Q9PQGkWyq9mHEFP0IFkAfOowaX+yuLftS7XhofU51QOYjoAnXT2h1RFvR17j2qP8rSW22gwScAUGmOsVtPmtBBf2udoK4kmRFo7Jy5U731q18iV4aETHQYBWracaTVWxjxtxhxaXWMCKhgfd120Vgz0tPkIxqeh8gsgb07i8hjSC3ia0UYxOSghCvzrCC8UAqQpIQMFIK+DRKigAFsd3usUHO4GrtC0l3Tr6fXtadhkptfzoluJhu82k2aGn1mN+YisNp/yxGe4vhy6OTe0D4HNQQhq4+57NqKgjA1SxxjEFvTMFkzaRNKbZvcF/DYLOZh5ub2Ym9tuKPBT0ZBpsR+LGyZwyLi/bxQ9dUGp8bwsnBqeeBcGTCbZbcJ7i4cqrWFbyHBdvMkKt8lxMY/yeYM8f5fNmV8WkGPylqBhEWVEWhmIDHlGcOdH2bSRKRWYWEkyqnVB+qVg/eW6s+nkg0wLjUKoW8XY668srHb90IuzQ5kX02k4keklVBnmccCKYg0R9UZ4SDsoSipA95K8PylZwxWfBKHCXxqSr14mEiq0HgsXLQU1Q31Vly1e6NZKoUzwupcwGcUGpDeJFMScmJBkTxjxGd4lw8coUE8xTJZ4+GBRz+BDVwpT9EaXS/FPWKSLYs4m1ZQow1CVYjsbV5s3LbSbm42tza3Pzfr2h6KxS9aq9dRatxrWK2vb2rX2rAPLqziVdqVf+Vb9Uf1Z/VX9PTG9tVAwT6zSqP75D8KUz2c=</latexit>




grams, even semantically constructed ones. To            if j < m:
solve this in [14], the parameter 𝑚 is bounded               k = h(m, j + 1, k + 1)
                                                         return k
to a small constant.
   In constrast, our methodology easily yields              Fig. 5. Challenging Example From [14]
a solution. In each interleaving run, we intuitively want to match every call of 𝑓 against one call of
𝑔. This is almost a (1, 1)-lockstep, except that the formal definition in Fig. 4 dictates that every call
and return participates in the scheduling, which undesirably forces the calls of ℎ to also participate
in the lockstep matching of the calls; as a result, the second recursive call of 𝑔 are nested inside the
first call of ℎ. However, as we demonstrate in Section 6.2, this limitation in the formal definitions
of the canonical reductions is superficial, and we can easily customize them to schedule only a
selected subset of calls and returns (in this case, those of functions 𝑓 and 𝑔) and treat the rest the
same way as internal actions. Our tool HyRec can verify this instance when such a customized
(1, 1)-lockstep reduction is given as input.

6.2     Customizations of Canonical Reductions
In this section, we introduce two simple customizations of canonical reductions.

   Scheduling Selected Calls/Returns Only. By default, every call and return participates in
the scheduling of the canonical reductions, and our first customization is to allow only a selected
subset to participate, and the rest stack operations Σ′ ⊂ Σcall ∪ Σret are treated the same way as
internal actions.
18                                                                              Ruotong Cheng and Azadeh Farzan


   To achieve this, one cannot simply change the partition of the visibly pushdown alphabet, which
breaks the mechanics of visibly pushdown languages; nor can we apply the NC-int rule or LS-
int rule for runs that start with a call that does not participate in the scheduling, which breaks
well-nestedness of the reduction. Instead, we modify the contextual orders ≺ for the canonical
reductions (Proposition 6.1): Based on ≺, we can define another contextual order ≺′ that replaces
letters in Σ′ with internal letters, queries ≺, and returns the result. Then the reduction induced by
≺′ is exactly the customization that we want. Formally, let 𝑓 : e  Σ∗ → e Σ∗ be a letter-to-letter string
homomorphism such that
                      𝑓 (𝑎) ∈ Σ𝑖int if 𝑎 ∈ Σ′ ∩ e
                                                Σ𝑖 for any 𝑖, and 𝑓 (𝑎) = 𝑎 otherwise.                         (3)
                                                                  Σ. 𝑎 𝑓 (≺)𝑤 𝑏 ⇔ 𝑓 (𝑎) ≺ 𝑓 (𝑤 ) 𝑓 (𝑏).
Then ≺′ is given by the contextual order 𝑓 (≺) defined by ∀𝑎, 𝑏 ∈ e
   In general, 𝑓 (≺)𝑤 is not a linear order even when ≺ is a map e  Σ∗ → TO(e  Σ), as we have been
assuming; but in our use case, where 𝑓 replaces excluded calls and returns with internals from the
same component, such a definition is sufficient to induce a minimal reduction. Moreover, when ≺
is a VPO (as in Proposition 6.1), with a reasonable assumption on Σ′ , there is a contextual order
equivalent to 𝑓 (≺) that is a VPO:
   Proposition 6.3. Let Σ′ be a subset of Σcall ∪ Σret such that for all 𝑖 ∈ {1, . . . , 𝑛} and 𝑐, 𝑟 ∈ e   Σ𝑖 that
match in some run of 𝑃𝑖 , we have 𝑐 ∈ Σ′ ⇔ 𝑟 ∈ Σ′ . Let 𝑓 be a letter-to-letter string homomorphism that
satisfies (3). If ≺ is a VPO, then there is a VPO ≺′ such that red ≺ ′ (𝑃1 ⧛· · ·⧛𝑃𝑛 ) = red 𝑓 (≺) (𝑃1 ⧛· · ·⧛𝑃𝑛 ).
     The proof in Appendix C gives a construction for the VPO ≺′ given ≺ and 𝑓 .
   Right Alignment. The canonical reductions are defined over the structure that exposes the
leftmost letter of a word, for consistency with the use of left context (Definition 3.3), which eventually
leads to Proposition 6.1. However, this does not have to be the case: we can customize the alignment
of canonical reductions. To have right-aligned canonical reductions, we consider well-matched
words of the form 𝜖, 𝑤𝑎, and 𝑣𝑐𝑤𝑟 and change the rules accordingly. Then Proposition 6.1 holds
for the modified version of contextual lex reductions that look at the right context.
   As an example, consider a benchmark from [48] about proving the monotonicity of the Ackermann
function 𝐴(𝑚, 𝑛) over the second argument:
                                   
                                   
                                   𝑛 + 1,                           if 𝑚 = 0
                                   
                                   
                         𝐴(𝑚, 𝑛) := 𝐴(𝑚 − 1, 1),                     if 𝑚 > 0 ∧ 𝑛 = 0
                                   
                                   𝐴(𝑚 − 1, 𝐴(𝑚, 𝑛 − 1)).
                                   
                                                                     if 𝑚 > 0 ∧ 𝑛 > 0
                                   
Intuitively, a (1, 1)-lockstep reduction seems like the appropriate choice. However, let us consider a
run 𝜌 1 that starts with calling 𝐴(𝑚, 0) and a run 𝜌 2 that starts with calling 𝐴(𝑚, 𝑛) (𝑚, 𝑛 > 0). The
run 𝜌 1 consists of one direct recursive call 𝐴(𝑚 − 1, 1), whereas the run 𝜌 2 consists of two direct
recursive calls 𝑎 := 𝐴(𝑚, 𝑛 − 1) and 𝐴(𝑚 − 1, 𝑎), in that order. We would want to match 𝐴(𝑚 − 1, 1)
in 𝜌 1 against the second call 𝐴(𝑚 − 1, 𝑎) in 𝜌 2 , since it is the second call that produces the final result
and has the same argument 𝑚 − 1. A concise way to describe such a reduction is the right-aligned
(1, 1)-lockstep.

6.3     Direct Construction of Canonical Reductions
Given well-matched VPGs 𝐺 1, . . . , 𝐺𝑛 describing the language of the syntactic runs of each com-
ponent, the inductive definitions of the canonical reductions (Figures 3 and 4) inspire a way to
directly construct them as VPGs. A syntactic assumption on the form of input VPGs facilitate this
construction: for any productions 𝑋 → 𝛼 and 𝑋 → 𝛽, we assume that the right-hand sides 𝛼, 𝛽
Products of Recursive Programs for Hypersafety Verification                                                          19


both start with a call, both start with an internal, or both are empty. Any VPG can be converted in
linear time to an equivalent one in this form.
  Nested Concatenation: One can view the construction as a type of product construction. The
nonterminal symbols of the grammar 𝐺 for the language L (𝐺 1 ) ⊕ L (𝐺 2 ) are of the form [𝑊1,𝑊2 ],
where 𝑊1,𝑊2 are nonterminal symbols of 𝐺 1, 𝐺 2 respectively; [𝑊1,𝑊2 ] is a start symbol if 𝑊1,𝑊2
are start symbols of 𝐺 1, 𝐺 2 respectively. The productions of 𝐺 are defined by the rules in Figure 6,
where (𝑋 → 𝛼) ∈ 𝐺 denotes (𝑋 → 𝛼) is a production in 𝐺, a slight abuse of notation. Observe
the syntactic similarity between the rules of Figure 3 and those in Figure 6. The extra syntactic
condition guarantees this simplicity of inference of a grammar from the inductive definition.

     (𝑌1 → 𝜖 ) ∈ 𝐺 1                   (𝑌1 → 𝑎𝑊1 ) ∈ 𝐺 1                         (𝑌1 → 𝑐𝑊1𝑟𝑉 ) ∈ 𝐺 1
    (𝑊2 → 𝛼 ) ∈ 𝐺 2                     (𝑊2 → 𝛼 ) ∈ 𝐺 2                            (𝑊2 → 𝛼 ) ∈ 𝐺 2
                         GN-𝜖                                      GN-int                                       GN-call
 ( [𝑌1 ,𝑊2 ] → 𝛼 ) ∈ 𝐺            ( [𝑌1 ,𝑊2 ] → 𝑎[𝑊1 ,𝑊2 ] ) ∈ 𝐺            ( [𝑌1 ,𝑊2 ] → 𝑐 [𝑊1 ,𝑊2 ]𝑟𝑉 ) ∈ 𝐺

                                Fig. 6. VPG productions for nested concatenation

    𝒔-Lockstep: The construction of 𝒎-lockstep follows the same pattern. The nonterminal symbols
of the grammar 𝐺 of the 𝒎-lockstep of L (𝐺 1 ), . . . , L (𝐺𝑛 ) have the form [𝒔, 𝒕, (𝑊1, . . . ,𝑊𝑘 )], where
𝒔, 𝒕 satisfy the constraints in Section 6.1, 𝑊𝑖 is a nonterminal in 𝐺𝑖 for each 𝑖, and the length
and maximum element of 𝒔 are bounded by those of 𝒎. The rules for generating the grammar
construction rules mimic those of the inductive definition in Figure 4.
    There is, however, a small complication with an easy fix. In the rules for nested concatenation
(in Figure 3), for every pattern in the conclusion, the parts that appear in the premises have a
nonterminal symbol dedicated to it. For instance, 𝑎𝑤 1 is a pattern in the inductive definition, and
𝑤 1 corresponds to nonterminal symbol 𝑊1 in the grammar construction rules. This makes things
straightforward. Now consider the rule “LS-call” (of figure 4).
    There is a pattern 𝑐𝑖 𝑤𝑖 𝑟𝑖 𝑣𝑖 in the conclusion, yet the subword 𝑐𝑖 𝑤𝑖 𝑟𝑖 is isolated in the premise, for
which there does not exist a nonterminal. We can fix this if, for every rule of the form 𝑌 → 𝑐𝑊 𝑟𝑉
in 𝐺𝑖 , we add a rule 𝑌 ′ → 𝑐𝑊 𝑟 𝐸 (where 𝐸 → 𝜖), so subwords generated by 𝑐𝑊 𝑟 can be referred to
as 𝑌 ′ . The full set of production rules are listed in Figure 8 in Appendix D.2.
  Algorithmic Construction: In an algorithmic view of this construction, we can maintain
a queue of reachable symbols, so only the productions that are truly needed are added to the
grammar, making the construction efficient. Otherwise, the grammar would end up having a lot of
unreachable non-terminals. These VPG constructions exploit properties of the canonical reductions:
the contextual information is propagated in a top-down manner. For an arbitrary VP contextual
order, the contextual information propagates through the linear and hierarchical edges of the
nested words, so the reduction does not necessarily admit a direct VPG construction in the style
demonstrated in this section.

7   The Semantics of The Recursive Product Program
Recall that our full notation for a recursive program is a pair (𝑃, S) with 𝑃 representing its syntax as a
visibly pushdown language and S representing its semantics. Let (𝑃1, S1 ), . . . , (𝑃𝑛 , S𝑛 ) be recursive
programs over disjoint VP alphabets e     Σ1, . . . , e
                                                      Σ𝑛 respectively. Assume that we have constructed a
product program 𝑃 that is sound, well-nested, and visibly pushdown. To complete its description,
                    b
we need to discuss its semantics. Here, we discuss how to compose S1, . . . , S𝑛 into a single S.
   We assume the variable names from the individual programs are disjoint. Suppose S𝑘 is induced
by F𝑘 (see Section 2.2) and 𝑉 = 𝑉1 ⊎ · · · ⊎ 𝑉𝑛 where 𝑉𝑘 is the set of all valuations for 𝑃𝑘 . The trivial
20                                                                                                 Ruotong Cheng and Azadeh Farzan


                                                                        Σ → P (Π𝑛𝑗=1 Stack(𝑉𝑗 ) ×
solution would be to use 𝑛 stacks, which corresponds to a semantics M : e
Π 𝑗=1 Stack(𝑉𝑗 )). Each component uses the corresponding stack from the tuple, and its semantic
  𝑛

is defined in the standard way. For an interleaving run 𝜌 ∈ 𝑃1 ∥ · · · ∥ 𝑃𝑛 , the Hoare triple
{pre}𝜌 {post} is valid w.r.t. M if
                                                                                      𝑛
                                                                                      Ø                     𝑛
                                                                                                            Ø
          ∀((𝑆 1 .𝜈 1, . . . , 𝑆𝑛 .𝜈𝑛 ), (𝑆 1′ .𝜈 1′ , . . . , 𝑆𝑛′ .𝜈𝑛′ )) ∈ MJ𝜌K :         𝜈 𝑗 |= pre =⇒         𝜈 ′𝑗 |= post.
                                                                                      𝑗=1                   𝑗=1

M is the semantics where all commutativity reasoning happens: the commutativity relation I (see
Section 3.1) is sound w.r.t. M.
   By construction, any product program 𝑃b is well-nested, so it conceptually runs on a single stack.
However, if we just naively push and pop on the same stack, we run into a problem with scoping
of variables from different components. For instance, suppose 𝑃1 pushes and writes to variable 𝑥 1 ;
if 𝑃2 pushes next, then 𝑃1 loses track of 𝑥 1 , which is no longer on the top frame.
   There is a simple solution to this problem. We interpret the letters slightly differently: let
each frame in the single stack store the variables from all 𝑛 recursive programs (recall that the
variable names are assumed to be disjoint); when 𝑃𝑘 pushes or pops the stack, we also copy
over the irrelevant variables, i.e., those from 𝑃 𝑗 where 𝑗 ≠ 𝑘. Formally, we define a semantics
S :e Σ → P (Stack(𝑉 ) ×Stack(𝑉 )) induced by F ⊂ (Σcall ×𝑉 ×𝑉 ) ∪ (Σret ×𝑉 ×𝑉 ×𝑉 ) ∪ (Σint ×𝑉 ×𝑉 ):
       • If 𝑐 ∈ Σ𝑘call , then F J𝑐K := {(𝜈, 𝜈) : 𝜈 ∈ 𝑉𝑗 , 𝑗 ≠ 𝑘 } ∪ Fk J𝑐K.
       • If 𝑟 ∈ Σ𝑘ret , then F J𝑟 K := {(𝜈, 𝜈 < , 𝜈) : 𝜈, 𝜈 < ∈ 𝑉𝑗 , 𝑗 ≠ 𝑘 } ∪ Fk J𝑟 K.
       • If 𝑎 ∈ Σ𝑘int , then F J𝑎K := {(𝜈, 𝜈) : 𝜈 ∈ 𝑉𝑗 , 𝑗 ≠ 𝑘 } ∪ Fk J𝑎K.
S can be easily adjusted to account for shared memory: the shared global variables are also copied
over when when the stack is pushed and popped.
   Recall that M is the 𝑛-stack semantics. Well-nestedness guarantees that the shift from M to S
preserves the validity of Hoare triples, so any run in the well-nested shuffle has no distinction from
a run of a standard recursive program.
   Theorem 7.1. For any syntactic run 𝜌 ∈ 𝑃1 ⧛ · · · ⧛ 𝑃𝑛 and assertions 𝐴, 𝐵, the validity of {𝐴}𝜌 {𝐵}
is the same with respect to the semantics M and S.

8     Experimental Results
We have implemented our reduction-based scheme as a tool, called HyRec, that verifies hypersafety
properties of sequential recursive programs.

8.1     Implementation
HyRec verifies an input program written in a simple procedural programming language against a
given pair of pre/postconditions. The programming language supports the integer, boolean, and
array data types. The user specifies the property and one of the built-in (parametric) canonical
reductions, or a combination of canonical reductions. For instance, to verify the distributivity
property of div, one would use the command3 :
    HyRec div -property distributivity -reduction "(1,1)-lockstep(P3, nested_concatenation(P1,P2))"                               (C)
HyRec also accepts an arbitrary uniform visibly pushdown order, but none was required to solve
any of the benchmarks used for the evaluation.
  HyRec implements the following algorithms:
3 distributivity is a shorthand for the pre/postcondition that expresses the property.
Products of Recursive Programs for Hypersafety Verification                                         21


      Aut: the optimized construction of Section 4.3 as a nested word automaton (NWA) [3], a
        model that is equivalent to a VPA and supported by existing libraries [33];
      VPG: the same optimized construction but additionally converting the NWA into a VPG;
      Direct: the direct construction of Section 6.3.
   In each case, the resulting product program (in NWA or VPG format) and the corresponding
hypersafety property are encoded by HyRec as system of constrained Horn clauses (CHCs) in the
SMT-LIB format [6], which is satisfiable if and only if the pre/postcondition holds. We did not find
a classic recursive verification tool that does well and is not already using a similar CHC encoding
in the backend. In particular, [34] cannot handle these instances well. We use Z3/Spacer [21, 40],
Eldarica [36], and Golem [11] as the backend CHC solvers.
   CHC Encodings. We interpret the product program under the semantics S in Section 7. An
NWA can be directly encoded as CHCs in linear time (see Appendix D.1): one predicate for each
state, and one constraint for each transition that captures the inductivity [35] of the predicates
(assertions). In [35], the assertions annotate a nested trace, whereas in our setting, the assertions
annotate the NWA, and the naive encoding would be unsound with respect to unsat since it does
not distinguish context-sensitive and insensitive paths. Our solution is to introduce a ghost variable
that represents the “return address”, so only assertions along context-sensitive paths are required
to be inductive.
   In the conversion of the NWA to a VPG, we use the standard quadratic time [3] algorithm and
then eliminate the useless symbols and productions [37]. A VPG is encoded as CHCs in linear time
(see Appendix D.1): one predicate for each nonterminal that overapproximates the semantics of the
language generating by this nonterminal. The semantics S involves a stack, but for a well-matched
language, if we are only concerned with partial correctness, then we may use a stack-free semantics
defined inductively over the nesting structure, relating the variables before and after the execution
of a trace. VPGs have this nesting structure built-in, and each production is translated into one
constraint. This encoding is similar to “transition summaries” from [10].

8.2   Benchmarks
We built a benchmark set by including the safe relational benchmarks from [48] (28 in total, which
are in turn adapted from [20, 47]), taking the iterative hypersafety (non-concurrent) benchmarks
from [27] (17 in total) and rewriting them as recursive code, and adding 58 new ones. In some cases,
the new additional instances are in the form of additional hypersafety properties of benchmarks
from [27, 48]. Our newly added benchmarks consist of two groups, one for arithmetic functions
(33), and one for functions on arrays (25). In total, we have 62 arithmetic benchmarks, and 41 array
benchmarks. (See Appendix E for details.)
   The arithmetic benchmarks are hypersafety properties of primitives, in the spirit of the div
example from Section 1. They include programs with linear or non-linear recursion, and then
several hypersafety properties per program. Recall that the monotonicity property of div is
relatively straightforward, but the distributivity property of it is rather challenging to solve.
So, the hardness of an instance can depend on the benchmark or the property or both. The array
benchmarks are hypersafety properties of, or relations between, aggregate functions (min, max,
and sum) and comparators (pointwise comparison and lexicographic order) on arrays; we have
also included benchmarks that manipulate trees that are encoded as heaps in arrays; this is due to
restrictions in the CHC solvers’ support for theories and has nothing to do with our methodology.
   Despite the fact that hyperproperties were originally motivated by their applications in security,
in terms of diversity and quantity, there are many more instances of primitives (like division or
lexicographical orders on vectors) implementing known operations where 𝑘-safety properties are
22                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        Ruotong Cheng and Azadeh Farzan



                            (a)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 (b)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                <latexit sha1_base64="XW2ZqXNvbGJ0OOnKdWRTD4YWRlk=">AAAB/nicbZDLSsNAFIZP6q3WW9Wlm8Ei1E1JilSXBTcuK9oLtKFMppN26GQSZiZCCQVfwK2+gTtx66v4Aj6HkzQL2/rDwM93zuGc+b2IM6Vt+9sqbGxube8Ud0t7+weHR+Xjk44KY0lom4Q8lD0PK8qZoG3NNKe9SFIceJx2veltWu8+UalYKB71LKJugMeC+YxgbdBD1bsclit2zc6E1o2Tmwrkag3LP4NRSOKACk04Vqrv2JF2Eyw1I5zOS4NY0QiTKR7TvrECB1S5SXbqHF0YMkJ+KM0TGmX070SCA6VmgWc6A6wnarWWwv9q/Vj7N27CRBRrKshikR9zpEOU/huNmKRE85kxmEhmbkVkgiUm2qSztCXFBs5NMM5qDOumU685jVrjvl5pXuURFeEMzqEKDlxDE+6gBW0gMIYXeIU369l6tz6sz0VrwcpnTmFJ1tcv1wKWFA==</latexit>




                             <latexit sha1_base64="4UTbYTRTAAvdjzOyJ1y5653/lWQ=">AAAB/nicbZDLSsNAFIZP6q3WW9Wlm8Ei1E1JilSXBTcuK9oLtKFMppN26GQSZiZCCQVfwK2+gTtx66v4Aj6HkzQL2/rDwM93zuGc+b2IM6Vt+9sqbGxube8Ud0t7+weHR+Xjk44KY0lom4Q8lD0PK8qZoG3NNKe9SFIceJx2veltWu8+UalYKB71LKJugMeC+YxgbdBDFV8OyxW7ZmdC68bJTQVytYbln8EoJHFAhSYcK9V37Ei7CZaaEU7npUGsaITJFI9p31iBA6rcJDt1ji4MGSE/lOYJjTL6dyLBgVKzwDOdAdYTtVpL4X+1fqz9GzdhIoo1FWSxyI850iFK/41GTFKi+cwYTCQztyIywRITbdJZ2pJiA+cmGGc1hnXTqdecRq1xX680r/KIinAG51AFB66hCXfQgjYQGMMLvMKb9Wy9Wx/W56K1YOUzp7Ak6+sX1WmWEw==</latexit>




Fig. 7. Experimental Results: logscale plots. (a): quantile plot of performance comparison HyRec’s algorithms
against the baseline. (b): scatter plot of comparing CHC encoding sizes for the two grammar constructions.

essential to encode and check the basic properties of these primitives. The arities of the hypersafety
instances for these can vary. All but four benchmarks are 2- or 3-safety properties, and the rest has
𝑘 = 7 at maximum. These properties are specified in the style of (C).

8.3   Experiments
Our experiments were designed to answer the following research questions:
 RQ1: Is our reduction approach essential and effective in proving hypersafety properties of
      recursive programs?
 RQ2: Are parameterized lockstep and nested concatenation, as building blocks, expressive enough
      to support the construction of effective product programs for a broad range of examples?
 RQ3: Does the representation of reduction (automata v.s. two grammar styles) have an impact on
      the effectiveness of the process?
  With respect to concurrency, this paper mainly proposes the theoretical insight that our reduction
methodology acts as a complete sequentialization scheme for certain classes of recursive programs.
We do not view HyRec as a tool for verification or bug finding of recursive concurrent programs.
   Results. As a baseline comparison, we use three standard scenarios, with the VPG encoding
in Appendix D.1: (1) sequential composition as the product program, (2) a direct encoding of the
problem without reductions and without making 𝑘 disjoint copies for the 𝑘-safety property, and (3)
the variation of (2) in which 𝑘 disjoint copies are made. We refer to Baseline as the best of these
three algorithms, including the best performing CHC solver. We tried RelRecMc (the tool from
[48]) on all baseline encodings, but it times out or throws a Segmentation fault on every instance.
We also tested the div examples from Section 1 with its own style of encoding, and scaling and
distributivity cannot be solved.
   On average, the production of the CHC encoding takes very little time (around 1 second) for all
instances. As expected, the direct construction method is the fastest, followed by the generation of
the automaton and the VPG based on the automaton. Our reported runtimes, therefore, are only
for the time to verify the product program, and excludes this negligible construction time. We use
a timeout of 600 seconds for the combination of both steps.
Products of Recursive Programs for Hypersafety Verification                                          23


   Figure 7(a) illustrates the log-scale quantile plot that compares our three algorithms (Aut, VPG,
and Direct) against the Baseline. HyRec is the best of the three algorithms. The arithmetic
benchmarks solved by Baseline are exactly those with a function summary in Linear Integer
Arithmetic. (RQ1) Direct, VPG, and Aut contribute 73, 17, and 13 instances to HyRec respectively
(accounting for the ties). The number for each curve lists the total number of benchmarks solved
by that algorithm. It is noteworthy that CHC encodings based on grammars are on average much
more efficiently solvable than the one based on automata; yet, Aut is better at solving harder
instances: out of the 13 winners contributed by Aut, 9 of them are only solvable by Aut, whereas
all 17 benchmarks where VPG wins can be solved by others albeit more slowly. (RQ3)
   Our direct construction does offer a significant improvement. This is while the resulting product
programs are identical when it comes to the set of their syntactic runs. The difference may stem
from the compactness of the resulting grammar. Figure 7(b) compares the sizes of the resulting
CHC encodings: blue dots compare the number constraints and green dots that of predicates. (RQ3)
   HyRec fails to solve 5 of the 103 benchmarks. One instance is a shortcoming of the CHC solvers
and is not related to the product program aspect. It is the simplest of a group of 4 benchmarks from
[27] that increasingly unroll loops. HyRec successfully proves unrolling the loop by 3, 4, and 5
times, but fails at the 2 unrolling. The rest of the failures are worthy of a deeper discussion, and are
explored in the next section. (RQ2)
   Separately, we also evaluate the scalability of our approach for higher arity hypersafety instances.
With increasing 𝑘 until the first timeout or error, we run the tool with the div program (Fig. 1),
(1, . . . , 1)-lockstep reduction, and the variation of (monotonicity) as a 𝑘-property:
                             𝑛 1 ≤ · · · ≤ 𝑛𝑘 ⇒ div(𝑛𝑘 , 𝑑) ≤ · · · ≤ div(𝑛𝑘 , 𝑑).
As the arity of the hypersafety instance goes higher, the time for generating the CHC encoding is
increasing. The three algorithms Direct, Aut, and VPG scale to 𝑘 = 12, 7, and 6 respectively; for
the largest instance (Direct, 𝑘 = 12, and 105 predicates in the CHC encoding), CHC generation
takes up 33% of the total time. In practice, however, these arities for hypersafety are very rare. As
expected, the size of the CHC encodings (measured by the number of predicates or constraints)
grows multiplicatively for all algorithms.

8.4   Discussion and Limitations
Here, we summarize some key observations from the experiments and discuss some unique features
and limitations of our proposed solution. Most importantly, we discuss the reasons behind why 4
benchmarks from the set cannot be solved by HyRec.
  Representation matters. It is somewhat surprising that although the same exact set of align-
ments are represented by the two different grammar constructions and the automata construction,
the results significantly differ in some cases. The difference between the grammar constructions
can be attributed to the size, as the scattered plot in Figure 7(b) highlights. This advantage, of
having 3 chances at solving an instance, is a strict consequence of our operational framework.
  Alignments do not always work. It is undeniable that reductions are essential to the success of
these hypersafety verification instances. It is also important to note that not all hypersafety verifi-
cation instances can be solved using these reductions. For instance, we use a primitive mult(𝑎, 𝑏) in
our benchmark set that multiplies 𝑎 by 𝑏 through repetitive addition. Consider the following simple
theorem about the commutativity of multiplication: mult(𝑛, 𝑚) = mult(𝑚, 𝑛). This is a 2-safety
property, where none of the lex reductions in this paper can simplify the proof down to a decidable
theory (linear integer arithmetic). The same is true for the iterative version of this code as well.
Two benchmarks from the set cannot be solved for this reason.
24                                                                        Ruotong Cheng and Azadeh Farzan


   Explicit Product Programs v.s. Integrated Verification Technique. There is a benchmark from
[48] related to Fibonacci that HyRec cannot solve, which stems from the fact that the conceptual
product program for this must reorder the two recursive calls to succeed. In code (and standard
semantics), this reordering is forbidden, but at the level of CHC encoding, once one is looking at a
symbolic encoding, it can be done semantically and soundly. One can weaken program semantics
to permit such sound reorderings. However, when the manipulations are done at the level of the
symbolic encoding, it comes for free. As discussed in Section 1, having an explicit product program
can have other advantages: one can get testing, symbolic execution, program analysis, and other
off-the-shelf applications for free.

   Syntactic v.s. Semantic alignments. Our reduction are syntactic, and HyRec fails at solving the
sum of squares benchmark [52] (modeled by an array in our benchmark set), which truly requires a
semantic alignment in the sense that one needs access to the program data to determine the right
synchronization; the tool from [38], for iterative programs, can handle the iterative version of this
benchmark automatically. We believe semantic alignments can be incorporated in our framework,
but this requires a nontrivial shift in representation, for instance to symbolic automata [17, 18],
and this is left for future work. It is noteworthy, however, that in some instances in the literature,
semantic alignments are used to account for limitations in syntactic alignments that are superficial.
For instance, our nested concatenation is an instance of a syntactic benchmark that may seem
superficially like a semantic benchmark: one needs to wait for one recursive call to be finished
before starting the second one (which is meant to be nested inside it). However, we handle this in a
purely syntactic way, and lex reductions in general include reductions in which the two copies can
go out of synch for arbitrarily long durations, without the need to rely on program data to make
this happen.

   Programmer’s intuition goes a long way. We found it very easy and straightforward to
guess and specify the right choice of reduction for each benchmark. Considering that 45% of our
benchmarks were not designed by us, but acquired from other sources (including those that search
for reductions), this is remarkable.

9    Related Work
The most closely related work to ours is a line of work that identifies the gap in relational verification
with the aid of CHC solving [4, 10, 20, 24, 47, 48] where the models are expressive enough to encode
arbitrary recursion schemes like ours. While we operate at the recursive program level, these
techniques directly target the CHC encodings [10] of these programs and employ transformations
such as fold/unfold [4, 20]. In [24], asynchronous fold/unfold transformation is proposed for fixpoint
logic; the transformed logic formula is encoded and passed to a CHC solver. Our product programs
go beyond a bounded number of unfoldings. Recall the distributivity property of div. In the spirit
of fold/unfold, one may think that unfolding once each of the div(𝑛, 𝑑) and div(𝑛 ′, 𝑑) instances
and twice the div(𝑛 ′′, 𝑑) instance may yield a product program, but this would not work due to a
problem with the base case. Our product program conceptually unfolds div(𝑛 + 𝑛 ′, 𝑑) for 𝑛 ′ times,
which is essential in handling cases like this.
   CHCproduct [47] is a family of transformations that resemble synchronous lockstep. The net
effect is not theoretically equivalent to our Figure 4 with 𝒔 = (1, . . . , 1), since CHCproduct operates
on the symbolic encoding of the programs, which allows the function calls to be “rearranged” and
“duplicated”. This flexibility also means the CHCproduct is not uniquely defined, and the extension
of synchronous CHCproduct [47] employs a heuristic to select a unique product. In [48], an
alternative technique based on Property Directed Reachability is proposed, which maintains over-
Products of Recursive Programs for Hypersafety Verification                                           25


and under-approximations of groups of predicates and automatically infers synchronous lockstep
strategies, also on the symbolic encoding of the programs.
   Putting CHC aside, in [22] for programs with procedures, modular product programs are con-
structed via a source-to-source transformation. Such product programs are intuitively a (1, . . . , 1)-
lockstep reduction of copies of the same program. In this special case, modular product programs
introduce Boolean activation variables to encode control-flow symbolically, thereby avoiding taking
the product of control locations.
   Multi-Stack Models and Sequentialization. The languages of runs of a multi-stack pushdown
automata are equivalent to those of Turing machines, even with two stacks. There are a number
of solutions in the literature that deal with this problem by under-approximating these multi-
stack languages. The most well-known ones are based on bounding a measure in the set of runs;
these include bounding the number of context switches [49, 55], phase bounding [41, 55], and
scope bounding [42–44]. Our reductions are not an under-approximation, but rather a faithful
representation. The languages are also theoretically incomparable against all these models. For
example, in a bounded context switching scheme, one is permitted to break the respective order of
calls and returns a bounded number of times, whereas it cannot be done in our model. In contrast, we
include runs that are not bounded in up to any of the measures: number of context switches, phases,
or scopes. Our focus in this paper is not on developing new classes of languages or giving new
decidability results. There is a loose connection between reductions and notion of sequentialization
[45] in the literature based on the same ideas of bounding the number of context switches, phases,
or scopes. The well-nested shuffle can be considered as sequentialization that is complete under
the conditions given in Section 5. It would be interesting to explore in future how well incomplete
reductions of concurrent programs perform as means of under-approximations for bug finding.
  Hyperproperty Verification. There is a large body of work studying verification of hyper-
properties, where earlier work mostly focused on verification of hypersafety properties [5, 7, 8, 22,
27, 31, 38, 52–54, 56, 57]. Since our focus is on verification of infinite-state hypersafety properties,
we forgo surveying the verification of hyperliveness properties for finite-state programs, unless
there is an overlap in techniques that makes the comparison worthwhile. There is a cluster of
work [1, 12, 32] on verification of hyperproperties [15] based on HyperLTL (a temporal logic for
hyperproperties) [15]. The work [32] on the verification of finite-state recursive programs, in the
context of asynchronous HyperLTL, is the only one from the cluster that addresses recursion in
the hyperproperty space. The focus of [32] is on the decidability results of the relaxations of the
logic for finite state recursive programs. We are in the scope of infinite-state programs, where
verification is undecidable even in the absence of recursion. The state space of alignments (i.e., the
degree of asynchrony) in [32] is not as general as an arbitrary reduction we define in Section 3.
   Alignments for Iterative Programs. Putting recursion aside, the closest to our work in terms
of aim and scope are those that focus on verification of infinite-state programs and take advantages
of the state space of alignments to solve the verification task. Specifically, in [27, 52, 53], automated
hypersafety verification techniques for sequential and concurrent programs [27] are proposed.
In [56], a generalization of CHCs with a specialized solving algorithm is introduced, which is
able to encode hyperproperties beyond hypersafety. In [9], an automated game-based verification
technique is used for a subset of hyperproperties that includes hypersafety properties but go beyond
to include some classes of hyperliveness. Finally, in [38], a solution based on CHC encoding of
a similar class of hyperproperties is proposed, which searches for a semantic alignment and a
proof simultaneously. The tool from [38] can handle some infinite-state programs, but for others, it
requires the right abstraction, given by the user, that would translate the program into a finite-state
26                                                                                     Ruotong Cheng and Azadeh Farzan


one; consequently, the search space for alignments also become finite. As an instance, none of
the three properties of the iterative version of the div example (from Section 1) can be verified by
the tool over the concrete state. In some sense, recursive programs inherit all the complications of
the iterative framework and add an extra layer of complexity. We discuss this extra complexity in
Section 1 and also note that the existence of a stack means even a program with finite data domain
may have infinite state space.
   In the paper, we mostly target the additional layer of complexity, and do not offer a new insight
for iterative programs, with one exception: canonical reductions as building blocks for the user
to communicate reduction ideas to a verification tool. More precisely, the analogous set of lex
reductions for iterative programs were already introduced in [26], but the analog of canonical
reductions (as a simple and effective way to specify a reduction) does not exist in the iterative
program literature, to the best of our knowledge. It is noteworthy that the iterative counterparts
of the canonical reductions are far easier to define formally and implement. Therefore, they may
offer a practical solution to program alignments that sits between one fixed reduction (which has
limited expressivity) and automated alignment search (which has limited scalability [27] or requires
user-provided abstractions in practice [38]).

Data-Availability Statement
Our tool HyRec and the benchmarks used in the evaluation (Section 8) can be found at [13]. A
description of all benchmarks is provided in Appendix E.

References
 [1] Shreya Agrawal and Borzoo Bonakdarpour. 2016. Runtime Verification of K-Safety Hyperproperties in HyperLTL. In
     2016 IEEE 29th Computer Security Foundations Symposium (CSF). 239–252. https://doi.org/10.1109/CSF.2016.24
 [2] Rajeev Alur and P. Madhusudan. 2004. Visibly Pushdown Languages. In Proceedings of the Thirty-Sixth Annual ACM
     Symposium on Theory of Computing. ACM, Chicago IL USA, 202–211. https://doi.org/10.1145/1007352.1007390
 [3] Rajeev Alur and P. Madhusudan. 2009. Adding Nesting Structure to Words. J. ACM 56, 3 (May 2009), 16:1–16:43.
     https://doi.org/10.1145/1516512.1516518
 [4] Emanuele De Angelis, Fabio Fioravanti, Alberto Pettorossi, and Maurizio Proietti. 2018. Predicate Pairing for Pro-
     gram Verification. Theory and Practice of Logic Programming 18, 2 (March 2018), 126–166. https://doi.org/10.1017/
     S1471068417000497
 [5] Timos Antonopoulos, Eric Koskinen, Ton Chanh Le, Ramana Nagasamudram, David A. Naumann, and Minh Ngo. 2023.
     An Algebra of Alignment for Relational Verification. Proc. ACM Program. Lang. 7, POPL (Jan. 2023), 20:573–20:603.
     https://doi.org/10.1145/3571213
 [6] Clark Barrett, Aaron Stump, and Cesare Tinelli. 2010. The SMT-LIB Standard: Version 2.0. In Proceedings of the 8th
     International Workshop on Satisfiability modulo Theories (Edinburgh, UK), A. Gupta and D. Kroening (Eds.).
 [7] Gilles Barthe, Juan Manuel Crespo, and César Kunz. 2011. Relational Verification Using Product Programs. In FM
     2011: Formal Methods, Michael Butler and Wolfram Schulte (Eds.). Springer, Berlin, Heidelberg, 200–214. https:
     //doi.org/10.1007/978-3-642-21437-0_17
 [8] Gilles Barthe, Pedro R. D’Argenio, and Tamara Rezk. 2004. Secure Information Flow by Self-Composition. In Proceedings.
     17th IEEE Computer Security Foundations Workshop. IEEE Computer Society, 100–100. https://doi.org/10.1109/CSFW.
     2004.1310735
 [9] Raven Beutner and Bernd Finkbeiner. 2022. Software Verification of Hyperproperties Beyond K-Safety. In Computer
     Aided Verification, Sharon Shoham and Yakir Vizel (Eds.). Vol. 13371. Springer International Publishing, Cham, 341–362.
     https://doi.org/10.1007/978-3-031-13185-1_17
[10] Nikolaj Bjørner, Arie Gurfinkel, Ken McMillan, and Andrey Rybalchenko. 2015. Horn Clause Solvers for Program
     Verification. In Fields of Logic and Computation II, Lev D. Beklemishev, Andreas Blass, Nachum Dershowitz, Bernd
     Finkbeiner, and Wolfram Schulte (Eds.). Vol. 9300. Springer International Publishing, Cham, 24–51. https://doi.org/10.
     1007/978-3-319-23534-9_2
[11] Martin Blicha, Konstantin Britikov, and Natasha Sharygina. 2023. The Golem Horn Solver. In Computer Aided
     Verification, Constantin Enea and Akash Lal (Eds.). Springer Nature Switzerland, Cham, 209–223. https://doi.org/10.
     1007/978-3-031-37703-7_10
Products of Recursive Programs for Hypersafety Verification                                                             27


[12] Laura Bozzelli, Adriano Peron, and César Sánchez. 2021. Asynchronous Extensions of HyperLTL. In 2021 36th Annual
     ACM/IEEE Symposium on Logic in Computer Science (LICS). 1–13. https://doi.org/10.1109/LICS52264.2021.9470583
[13] Ruotong Cheng and Azadeh Farzan. 2025. HyRec: Artifact for "Products of Recursive Programs for Hypersafety
     Verification". Zenodo. https://doi.org/10.5281/zenodo.16930073
[14] Berkeley Churchill, Oded Padon, Rahul Sharma, and Alex Aiken. 2019. Semantic Program Alignment for Equivalence
     Checking. In Proceedings of the 40th ACM SIGPLAN Conference on Programming Language Design and Implementation
     (PLDI 2019). Association for Computing Machinery, New York, NY, USA, 1027–1040. https://doi.org/10.1145/3314221.
     3314596
[15] Michael R. Clarkson, Bernd Finkbeiner, Masoud Koleini, Kristopher K. Micinski, Markus N. Rabe, and César Sánchez.
     2014. Temporal Logics for Hyperproperties. In Principles of Security and Trust, Martín Abadi and Steve Kremer (Eds.).
     Springer, Berlin, Heidelberg, 265–284. https://doi.org/10.1007/978-3-642-54792-8_15
[16] Michael R. Clarkson and Fred B. Schneider. 2010. Hyperproperties. JCS 18, 6 (Sept. 2010), 1157–1210. https:
     //doi.org/10.3233/JCS-2009-0393
[17] Loris D’Antoni and Rajeev Alur. 2014. Symbolic Visibly Pushdown Automata. In Computer Aided Verification, Armin
     Biere and Roderick Bloem (Eds.). Springer International Publishing, Cham, 209–225. https://doi.org/10.1007/978-3-
     319-08867-9_14
[18] Loris D’Antoni and Margus Veanes. 2017. The Power of Symbolic Automata and Transducers. In Computer Aided
     Verification, Rupak Majumdar and Viktor Kunčak (Eds.). Springer International Publishing, Cham, 47–67. https:
     //doi.org/10.1007/978-3-319-63387-9_3
[19] Martin Davis, Ron Sigal, and Elaine J. Weyuker. 1994. Computability, Complexity, and Languages: Fundamentals of
     Theoretical Computer Science (2nd. ed ed.). Academic Press, Harcourt, Brace, Boston.
[20] Emanuele De Angelis, Fabio Fioravanti, Alberto Pettorossi, and Maurizio Proietti. 2016. Relational Verification
     Through Horn Clause Transformation. In Static Analysis, Xavier Rival (Ed.). Springer, Berlin, Heidelberg, 147–169.
     https://doi.org/10.1007/978-3-662-53413-7_8
[21] Leonardo de Moura and Nikolaj Bjørner. 2008. Z3: An Efficient SMT Solver. In Tools and Algorithms for the Construction
     and Analysis of Systems, C. R. Ramakrishnan and Jakob Rehof (Eds.). Springer, Berlin, Heidelberg, 337–340. https:
     //doi.org/10.1007/978-3-540-78800-3_24
[22] Marco Eilers, Peter Müller, and Samuel Hitz. 2018. Modular Product Programs. In Programming Languages and Systems,
     Amal Ahmed (Ed.). Springer International Publishing, Cham, 502–529. https://doi.org/10.1007/978-3-319-89884-1_18
[23] Javier Esparza, David Hansel, Peter Rossmanith, and Stefan Schwoon. 2000. Efficient Algorithms for Model Checking
     Pushdown Systems. In Computer Aided Verification, E. Allen Emerson and Aravinda Prasad Sistla (Eds.). Springer,
     Berlin, Heidelberg, 232–247. https://doi.org/10.1007/10722167_20
[24] Mahmudul Faisal Al Ameen, Naoki Kobayashi, and Ryosuke Sato. 2024. Asynchronous Unfold/Fold Transformation for
     Fixpoint Logic. Science of Computer Programming 231 (Jan. 2024), 103014. https://doi.org/10.1016/j.scico.2023.103014
[25] Azadeh Farzan. 2023. Commutativity in Automated Verification. In 2023 38th Annual ACM/IEEE Symposium on Logic
     in Computer Science (LICS). 1–7. https://doi.org/10.1109/LICS56636.2023.10175734
[26] Azadeh Farzan, Dominik Klumpp, and Andreas Podelski. 2022. Sound Sequentialization for Concurrent Program
     Verification. In Proceedings of the 43rd ACM SIGPLAN International Conference on Programming Language Design
     and Implementation (PLDI 2022). Association for Computing Machinery, New York, NY, USA, 506–521. https:
     //doi.org/10.1145/3519939.3523727
[27] Azadeh Farzan and Anthony Vandikas. 2019. Automated Hypersafety Verification. In Computer Aided Verification, Isil
     Dillig and Serdar Tasiran (Eds.). Springer International Publishing, Cham, 200–218. https://doi.org/10.1007/978-3-
     030-25540-4_11
[28] Azadeh Farzan and Anthony Vandikas. 2020. Reductions for Safety Proofs. Proc. ACM Program. Lang. 4, POPL (Jan.
     2020), 1–28. https://doi.org/10.1145/3371081
[29] Patrice Godefroid, Gerhard Goos, Juris Hartmanis, and Jan Leeuwen (Eds.). 1996. Partial-Order Methods for the
     Verification of Concurrent Systems. Lecture Notes in Computer Science, Vol. 1032. Springer, Berlin, Heidelberg.
     https://doi.org/10.1007/3-540-60761-7
[30] Patrice Godefroid, Aditya V. Nori, Sriram K. Rajamani, and Sai Deep Tetali. 2010. Compositional May-Must Program
     Analysis: Unleashing the Power of Alternation. In Proceedings of the 37th Annual ACM SIGPLAN-SIGACT Symposium
     on Principles of Programming Languages (POPL ’10). Association for Computing Machinery, New York, NY, USA, 43–56.
     https://doi.org/10.1145/1706299.1706307
[31] Benny Godlin and Ofer Strichman. 2013. Regression Verification: Proving the Equivalence of Similar Programs.
     Software Testing Verif & Rel 23, 3 (May 2013), 241–258. https://doi.org/10.1002/stvr.1472
[32] Jens Oliver Gutsfeld, Markus Müller-Olm, and Christoph Ohrem. 2024. Deciding Asynchronous Hyperproperties for
     Recursive Programs. Proc. ACM Program. Lang. 8, POPL (Jan. 2024), 2:33–2:60. https://doi.org/10.1145/3632844
28                                                                                      Ruotong Cheng and Azadeh Farzan


[33] Matthias Heizmann, Jürgen Christ, Daniel Dietsch, Evren Ermis, Jochen Hoenicke, Markus Lindenmann, Alexander
     Nutz, Christian Schilling, and Andreas Podelski. 2013. Ultimate Automizer with SMTInterpol. In Tools and Algorithms
     for the Construction and Analysis of Systems, Nir Piterman and Scott A. Smolka (Eds.). Springer, Berlin, Heidelberg,
     641–643. https://doi.org/10.1007/978-3-642-36742-7_53
[34] Matthias Heizmann, Jochen Hoenicke, and Andreas Podelski. 2009. Refinement of Trace Abstraction. In Static
     Analysis, Jens Palsberg and Zhendong Su (Eds.). Vol. 5673. Springer Berlin Heidelberg, Berlin, Heidelberg, 69–85.
     https://doi.org/10.1007/978-3-642-03237-0_7
[35] Matthias Heizmann, Jochen Hoenicke, and Andreas Podelski. 2010. Nested Interpolants. In Proceedings of the 37th
     Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL ’10). Association for
     Computing Machinery, New York, NY, USA, 471–482. https://doi.org/10.1145/1706299.1706353
[36] Hossein Hojjat and Philipp Rümmer. 2018. The ELDARICA Horn Solver. In 2018 Formal Methods in Computer Aided
     Design (FMCAD). 1–7. https://doi.org/10.23919/FMCAD.2018.8603013
[37] John E. Hopcroft, Rajeev Motwani, and Jeffrey D. Ullman. 2007. Introduction to Automata Theory, Languages, and
     Computation (3rd ed ed.). Pearson/Addison Wesley, Boston.
[38] Shachar Itzhaky, Sharon Shoham, and Yakir Vizel. 2024. Hyperproperty Verification as CHC Satisfiability. In Pro-
     gramming Languages and Systems, Stephanie Weirich (Ed.). Springer Nature Switzerland, Cham, 212–241. https:
     //doi.org/10.1007/978-3-031-57267-8_9
[39] Xiaodong Jia, Ashish Kumar, and Gang Tan. 2021. A Derivative-Based Parser Generator for Visibly Pushdown
     Grammars. Proc. ACM Program. Lang. 5, OOPSLA (Oct. 2021), 1–24. https://doi.org/10.1145/3485528
[40] Anvesh Komuravelli, Arie Gurfinkel, and Sagar Chaki. 2016. SMT-based Model Checking for Recursive Programs.
     Form Methods Syst Des 48, 3 (June 2016), 175–205. https://doi.org/10.1007/s10703-016-0249-4
[41] Salvatore La Torre, P. Madhusudan, and Gennaro Parlato. 2008. An Infinite Automaton Characterization of Double
     Exponential Time. In Computer Science Logic, Michael Kaminski and Simone Martini (Eds.). Springer, Berlin, Heidelberg,
     33–48. https://doi.org/10.1007/978-3-540-87531-4_5
[42] Salvatore La Torre and Margherita Napoli. 2011. Reachability of Multistack Pushdown Systems with Scope-Bounded
     Matching Relations. In CONCUR 2011 – Concurrency Theory, Joost-Pieter Katoen and Barbara König (Eds.). Springer,
     Berlin, Heidelberg, 203–218. https://doi.org/10.1007/978-3-642-23217-6_14
[43] Salvatore La Torre, Margherita Napoli, and Gennaro Parlato. 2014. Scope-Bounded Pushdown Languages. In Develop-
     ments in Language Theory, Arseny M. Shur and Mikhail V. Volkov (Eds.). Springer International Publishing, Cham,
     116–128. https://doi.org/10.1007/978-3-319-09698-8_11
[44] Salvatore La Torre, Margherita Napoli, and Gennaro Parlato. 2020. Reachability of Scope-Bounded Multistack Pushdown
     Systems. Information and Computation 275 (Dec. 2020), 104588. https://doi.org/10.1016/j.ic.2020.104588
[45] Akash Lal and Thomas Reps. 2008. Reducing Concurrent Analysis Under a Context Bound to Sequential Analysis.
     In Computer Aided Verification, Aarti Gupta and Sharad Malik (Eds.). Springer, Berlin, Heidelberg, 37–51. https:
     //doi.org/10.1007/978-3-540-70545-1_7
[46] A Mazurkiewicz. 1987. Trace Theory. In Advances in Petri Nets 1986, Part II on Petri Nets: Applications and Relationships
     to Other Models of Concurrency. Springer-Verlag, Berlin, Heidelberg, 279–324.
[47] Dmitry Mordvinov and Grigory Fedyukovich. 2017. Synchronizing Constrained Horn Clauses. In LPAR-21. 21st
     International Conference on Logic for Programming, Artificial Intelligence and Reasoning. 338–319. https://doi.org/10.
     29007/gr5c
[48] Dmitry Mordvinov and Grigory Fedyukovich. 2019. Property Directed Inference of Relational Invariants. In 2019
     Formal Methods in Computer Aided Design (FMCAD). 152–160. https://doi.org/10.23919/FMCAD.2019.8894274
[49] Shaz Qadeer and Jakob Rehof. 2005. Context-Bounded Model Checking of Concurrent Software. In Tools and Algorithms
     for the Construction and Analysis of Systems, Nicolas Halbwachs and Lenore D. Zuck (Eds.). Springer, Berlin, Heidelberg,
     93–107. https://doi.org/10.1007/978-3-540-31980-1_7
[50] G. Ramalingam. 2000. Context-Sensitive Synchronization-Sensitive Analysis Is Undecidable. ACM Trans. Program.
     Lang. Syst. 22, 2 (March 2000), 416–430. https://doi.org/10.1145/349214.349241
[51] Thomas Reps, Susan Horwitz, and Mooly Sagiv. 1995. Precise Interprocedural Dataflow Analysis via Graph Reachability.
     In Proceedings of the 22nd ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL ’95).
     Association for Computing Machinery, New York, NY, USA, 49–61. https://doi.org/10.1145/199448.199462
[52] Ron Shemer, Arie Gurfinkel, Sharon Shoham, and Yakir Vizel. 2019. Property Directed Self Composition. In Computer
     Aided Verification, Isil Dillig and Serdar Tasiran (Eds.). Vol. 11561. Springer International Publishing, Cham, 161–179.
     https://doi.org/10.1007/978-3-030-25540-4_9
[53] Marcelo Sousa and Isil Dillig. 2016. Cartesian Hoare Logic for Verifying K-Safety Properties. In Proceedings of the
     37th ACM SIGPLAN Conference on Programming Language Design and Implementation. ACM, Santa Barbara CA USA,
     57–69. https://doi.org/10.1145/2908080.2908092
Products of Recursive Programs for Hypersafety Verification                                                                    29


[54] Tachio Terauchi and Alex Aiken. 2005. Secure Information Flow as a Safety Problem. In Static Analysis, David
     Hutchison, Takeo Kanade, Josef Kittler, Jon M. Kleinberg, Friedemann Mattern, John C. Mitchell, Moni Naor, Oscar
     Nierstrasz, C. Pandu Rangan, Bernhard Steffen, Madhu Sudan, Demetri Terzopoulos, Dough Tygar, Moshe Y. Vardi,
     Gerhard Weikum, Chris Hankin, and Igor Siveroni (Eds.). Vol. 3672. Springer Berlin Heidelberg, Berlin, Heidelberg,
     352–367. https://doi.org/10.1007/11547662_24
[55] Salvatore La Torre, Parthasarathy Madhusudan, and Gennaro Parlato. 2007. A Robust Class of Context-Sensitive
     Languages. In 22nd Annual IEEE Symposium on Logic in Computer Science (LICS 2007). 161–170. https://doi.org/10.
     1109/LICS.2007.9
[56] Hiroshi Unno, Tachio Terauchi, and Eric Koskinen. 2021. Constraint-Based Relational Verification. In Computer Aided
     Verification: 33rd International Conference, CAV 2021, Virtual Event, July 20–23, 2021, Proceedings, Part I. Springer-Verlag,
     Berlin, Heidelberg, 742–766. https://doi.org/10.1007/978-3-030-81685-8_35
[57] Weikun Yang, Yakir Vizel, Pramod Subramanyan, Aarti Gupta, and Sharad Malik. 2018. Lazy Self-composition for
     Security Verification. In Computer Aided Verification, Hana Chockler and Georg Weissenbacher (Eds.). Vol. 10982.
     Springer International Publishing, Cham, 136–156. https://doi.org/10.1007/978-3-319-96142-2_11
[58] Anna Zaks and Amir Pnueli. 2008. CoVaC: Compiler Validation by Program Analysis of the Cross-Product. In
     FM 2008: Formal Methods, Jorge Cuellar, Tom Maibaum, and Kaisa Sere (Eds.). Springer, Berlin, Heidelberg, 35–51.
     https://doi.org/10.1007/978-3-540-68237-0_5
30                                                                          Ruotong Cheng and Azadeh Farzan


A     Background
A.1    Recursive Programs as VPLs
Following [35], we model a (single-stack) recursive program as a VPL (a well-matched one, for
our purpose), where the alphabet e    Σ is the program statements. Such VPLs can be obtained from a
recursive control-flow graph by viewing the graph as a VPA. Not all words in the language is a
semantically valid run of the program: a sequence of statements (also called a trace) that repsects
the control-flow structure and correctly matches the calls and returns may be infeasible when
semantics is taken into account. Below, we define a concrete alphabet e      Σ and its semantics. We use
it in the examples in Appendix B and in our implementation of HyRec. The theory developed in
Section 3–7 does not rely on this concrete alphabet.
    For any set 𝑋 , let Stack(𝑋 ) denote the set of stacks whose frames are elements of 𝑋 , and let
P (𝑋 ) denote the power set of 𝑋 . Let 𝐿 be the set of local variables, 𝐹 the set of function names,
𝐿p ⊂ 𝐿 the set of function parameters, param : 𝐹 → P (𝐿p ) that maps each function name to a set
of parameters, and output : 𝐹 → P (𝐿) the maps each function name to a set of output variables.
Define 𝐿¯p := {𝑝¯ | 𝑝 ∈ 𝐿p }, which represents dummy variables that record the initial value of the
                                                                                                 ¯
parameters when a function is called. Let 𝐷 be the domain of the variables and 𝑇 = 𝐷 𝐿∪𝐿p the set
of all valuations.                                                                 
    We assume that e  Σ consists of assign statements 𝑥 := 𝑡 , assume statements assume 𝜙 , call state-
                                       
ments call 𝑓 , and return statements ret 𝑓 , where 𝑥 ∈ 𝐿, 𝑡 is an expression over 𝐿, 𝜙 is an assertion
over 𝐿, and 𝑓 ∈ 𝐹 . The first two types of statements are internal. For a program
                                                                                     𝑃 over this alphabet
Σ, we always assume that for any word in 𝑃, if a call call 𝑓 and a return ret 𝑓 match, then 𝑓 = 𝑔.
e
Define the semantics function S : e   Σ → P (Stack(𝑇 ) × Stack(𝑇 )) as follows:

                SJ𝑥 := 𝑡K := {(𝑆.𝜈, 𝑆.𝜈 ′ ) : 𝜈 ′ = 𝜈 ⊕ {𝑥 ↦→ 𝜈 (𝑡)}},
                     SJ𝜙K := {(𝑆.𝜈, 𝑆.𝜈) : 𝜈 |= 𝜙 },
              SJcall 𝑓 K := {(𝑆.𝜈, 𝑆.𝜈.𝜈 ′ ) : ∀𝑝 ∈ param(𝑓 ). 𝜈 ′ (𝑝) = 𝜈 ′ (𝑝)
                                                                              ¯ = 𝜈 (𝑝)},
                SJret 𝑓 K := {(𝑆.𝜈 < .𝜈, 𝑆.𝜈 ′ ) : 𝜈 ′ = 𝜈 < ⊕ {𝑦 ↦→ 𝜈 (𝑦) : 𝑦 ∈ output(𝑓 )}}.

Extend S from letters to words via relation composition. For a program 𝑃 over e  Σ, a run 𝜌 ∈ 𝑃 is
said to be infeasible if SJ𝜌K = ∅. When talking about the runs of a program, we by default include
both the feasible ones and infeasible ones.

B     Examples of Product Programs
The formal semantics of the alphabet that we use is presented in Appendix A.1.

B.1    div
The grammar for div is as follows:

                                           
                         𝐷 → assume 𝑛 < 𝑑 𝑞 := 0 
                                                                
                         𝐷 → assume 𝑛 ≥ 𝑑 call div 𝐷 ret div 𝑞 := 𝑞 + 1 
                                                                           
  The grammar for synchronously lockstepping two copies of call div 𝐷 ret div is as follows,
where 𝜎 : 𝑘 means performing 𝜎 on the 𝑘-th stack and 𝑆 is the start symbol:
Products of Recursive Programs for Hypersafety Verification                                           31



                                      
                  𝑆 → call div : 1 𝐴 ret div : 1 
                       
                  𝐴 → assume 𝑛 < 𝑑 : 1 𝐷 2
                                                                      
                  𝐴 → assume 𝑛 ≥ 𝑑 : 1 call div : 2 𝐵 ret div : 2 𝑞 := 𝑞 + 1 : 1 
                       
                  𝐵 → assume 𝑛 < 𝑑 : 2 𝐷 1
                                                                      
                  𝐵 → assume 𝑛 ≥ 𝑑 : 2 call div : 1 𝐴 ret div : 1 𝑞 := 𝑞 + 1 : 2 
                                          
                 𝐷 1 → assume 𝑛 < 𝑑 : 1 𝑞 := 0 : 1 
                                                                        
                 𝐷 1 → assume 𝑛 ≥ 𝑑 : 1 call div : 1 𝐷 1 ret div : 1 𝑞 := 𝑞 + 1 : 1 
                                          
                 𝐷 2 → assume 𝑛 < 𝑑 : 2 𝑞 := 0 : 2 
                                                                        
                 𝐷 2 → assume 𝑛 ≥ 𝑑 : 2 call div : 2 𝐷 2 ret div : 2 𝑞 := 𝑞 + 1 : 2 
   This does not exactly match the lockstep that we formally define when it comes to the ordering
of internals but has the same spirits.

C    Proofs
   Proof of Proposition 3.2. Let Σ = {𝑎, 𝑏}, 𝑃 1 = 𝑎𝑎 ∗ , and 𝑃 2 = 𝑏𝑏 ∗ . Each minimal reduction
corresponds to a choice function on (𝑃1 ∥ 𝑃2 )/≡I . Note that (𝑃1 ∥ 𝑃2 )/≡I is an infinite set, and each
element in the quotient has size at least 2.                                                           □
  Proof of Proposition 3.4. Let ⪯ be a CLO induced by a contextual order ≺.
  To show transitivity, suppose 𝛼 ⪯ 𝛽 and 𝛽 ⪯ 𝛾. Suppose 𝛼 = 𝑥𝑎𝑦, 𝛽 = 𝑥𝑏𝑧 = 𝑥 ′𝑏 ′𝑧 ′ , and 𝛾 = 𝑥 ′𝑐𝑡,
where 𝑎 ≺𝑥 𝑏 and 𝑏 ′ ≺𝑥 ′ 𝑐.
     • If 𝑥 = 𝑥 ′ , then 𝛾 = 𝑥𝑐𝑡 and 𝑎 ≺𝑥 𝑐, so 𝛼 ⪯ 𝛾.
     • If 𝑥 is a proper prefix of 𝑥 ′ , then 𝑥𝑏 is a prefix of 𝛾 and 𝑎 ≺𝑥 𝑏, so 𝛼 ⪯ 𝛾.
     • If 𝑥 ′ is a proper prefix of 𝑥, then 𝑥 ′𝑏 ′ is a prefix of 𝛼 and 𝑏 ′ ≺𝑥 ′ 𝑐 ′ , so 𝛼 ⪯ 𝛾.
The three other cases can be verified in the same way, and transitivity holds. Similarly, we can
verify reflxivity and antisymmetry.
  For the sufficient condition for totality, for any distinct two distinct words, consider the first
position where they differ.                                                                         □
   Proof of Theorem 4.2. Let 𝐴𝑖 = (𝑄𝑖 , 𝑄𝑖in, Γ𝑖 , 𝛿𝑖 , 𝑄𝑖F ) be a VPA over the visibly pushdown alpha-
bet eΣ𝑖 . Define the VPA 𝐴 = (𝑄, 𝑄 in, Γ, 𝛿, 𝑄 F ) over e  Σ as follows:
      • 𝑄 = 𝑄 1 × · · · × 𝑄𝑛 .
      • 𝑄 in = 𝑄 1in × · · · × 𝑄𝑛in .
      • Γ = (Γ1 \ {⊥}) ⊎ · · · ⊎ (Γ2 \ {⊥}) ⊎ {⊥}.
      • 𝛿 int = {(𝒒, 𝜎, 𝒒[𝑖 ↦→ 𝑞𝑖′ ]) : 𝒒 ∈ 𝑄, 𝑖 ∈ {1, . . . , 𝑛}, (𝑞𝑖 , 𝜎, 𝑞𝑖′ ) ∈ 𝛿𝑖 }.
      • 𝛿 call = {(𝒒, 𝜎, 𝒒[𝑖 ↦→ 𝑞𝑖′ ], 𝛾) : 𝒒 ∈ 𝑄, 𝑖 ∈ {1, . . . , 𝑛}, (𝑞𝑖 , 𝜎, 𝑞𝑖′, 𝛾) ∈ 𝛿𝑖 }.
      • 𝛿 ret = {(𝒒, 𝜎, 𝛾, 𝒒[𝑖 ↦→ 𝑞𝑖′ ]) : 𝒒 ∈ 𝑄, 𝑖 ∈ {1, . . . , 𝑛}, (𝑞𝑖 , 𝜎, 𝛾, 𝑞𝑖′ ) ∈ 𝛿𝑖 }.
      • 𝑄 F = 𝑄 1F × · · · × 𝑄𝑛F .
It can be verified that L (𝐴) = L (𝐴1 ) ⧛ · · · ⧛ L (𝐴𝑛 ).                                           □
  Proof of Proposition 3.12. We prove the statement for a generic 𝐼 using the sleep set [29]
construction. Suppose ≺ is represented by a complete and deterministic VPA (𝑄 𝑆 , 𝑄 𝑆in, Γ𝑆 , 𝛿𝑆 , 𝑄 𝑆 ).
Define the VPA 𝐴 = (𝑄, 𝑄 in, Γ, 𝛿, 𝑄 F ) as follows:
      • 𝑄 = 2Σ × 𝑄 𝑆 .
               e
32                                                                                Ruotong Cheng and Azadeh Farzan


      • 𝑄 in = {∅} × 𝑄 𝑆in .
      • Γ = Γ𝑆 .
      • 𝛿 is the smallest subset of (𝑄 × Σcall × 𝑄 × (Γ \ {⊥})) ∪ (𝑄 × Σret × Γ × 𝑄) ∪ (𝑄 × Σint × 𝑄)
        such that for all set 𝑟 ∈ 2Σ , states 𝑠, 𝑠 ′ ∈ 𝑄 𝑆 , letter 𝜎 ∈ e     Σ \ 𝑟 , and stack symbol 𝛾 ∈ Γ, writing
                                        e

        𝑟 = {𝜎 ∈ Σ | 𝜎 ∈ 𝐼 (𝜎) ∧ (((𝜎 , 𝜎) ∈ ord(𝑠)) ∨ (𝜎 ∈ 𝑟 ))},
         ′       ′   e        ′                 ′                          ′

           – if (𝑠, 𝜎, 𝑠 ′, 𝛾) ∈ 𝛿𝑆 , then ((𝑟, 𝑠), 𝜎, (𝑟 ′, 𝑠 ′ ), 𝛾) ∈ 𝛿;
           – if (𝑠, 𝜎, 𝛾, 𝑠 ′ ) ∈ 𝛿𝑆 , then ((𝑟, 𝑠), 𝜎, 𝛾, (𝑟 ′, 𝑠 ′ )) ∈ 𝛿; and
           – if (𝑠, 𝜎, 𝑠 ′ ) ∈ 𝛿𝑆 , then ((𝑟, 𝑠), 𝜎, (𝑟 ′, 𝑠 ′ )) ∈ 𝛿.
           F
      • 𝑄 = 𝑄.
It can be shown that L (𝐴) = red ≺ (e       Σ∗ ).                                                                   □

   Proof of Proposition 3.9 and Proposition 3.13. Let e       Σ1, e
                                                                  Σ2 be the visibly pushdown alphabet
of parentheses and brackets respectively. Define ≺: Σ∗ → TO(Σ) that maps strings of an even
length to ( < ) < [ < ], and strings of an odd length to [ < ] < ( < ). Let 𝐿1 be the language of
balanced parentheses and 𝐿2 be the language of balanced brackets.
   Suppose red ≺ (𝐿1 ∥ 𝐿2 ) is context-free, and let 𝑝 be a pumping length. Pumping the string
                                             ([ · · · ([ (] · · · (] )2𝑝
                                             | {z } | {z }
                                               𝑝 times    𝑝 times

leads to a contradiction, so red ≺ (𝐿1 ∥ 𝐿2 ) cannot be context-free.                                              □

     Proof of Theorem 3.14. If 𝐿 is closed under 𝐼 then
                                                               Σ∗ ) ∩ 𝐿.
                                          red𝐼,≺ (𝐿) = red𝐼,≺ (e
     Suppose ≺ is a VP contextual order and red𝐼,≺ (𝑃 1 ∥ 𝑃2 ) ⊂ 𝑃1 ⧛ 𝑃2 ⊂ 𝑃1 ∥ 𝑃 2 . It follows that
                                                                              Σ∗ ) ∩ (𝑃1 ⧛ 𝑃 2 ).
                red𝐼,≺ (𝑃1 ∥ 𝑃2 ) = red𝐼,≺ (𝑃 1 ∥ 𝑃2 ) ∩ (𝑃1 ⧛ 𝑃2 ) = red𝐼,≺ (e
By Proposition 3.12, Theorem 4.2, and the closedness of VPLs under intersection, it follows that
red𝐼,≺ (𝑃1 ∥ 𝑃 2 ) is visibly pushdown.                                                       □

   Proof of Proposition 3.17. Write e   Σ𝑖 = Σ𝑖call, Σ𝑖ret, Σ𝑖int (𝑖 = 1, 2). Suppose for contradiction
there is some word in red ≺ (𝐿1 ∥ 𝐿2 ) \ (𝐿1 ∥ 𝐿2 ). Use (, ), [, and ] to denote a letter in Σcall
                                                                                                1 , Σ1 ,
                                                                                                      ret

Σcall
  2 , and Σ2 respectively. Consider the shortest prefix where the well-nestedness is broken, and
            ret

WLOG suppose the last letter in the prefix is a ]. Then ] is wrongly matched with a (. Then the
word has the form 𝛼 (𝛽]𝛾)𝛿. Note that the ( is the last pending call in the prefix 𝛼 (𝛽. The first letter
from eΣ1 in 𝛾) can be swapped to the position of the ] to give a smaller interleaving, which is a
contradiction.                                                                                         □

     Proof of Theorem 3.18. By Proposition 3.17 and Theorem 3.14.                                                  □

   Proof of Lemma 4.3. The coherency of ≺′ is evident. The VPA for ≺′ can be constructed from
the VPA for ≺ and an additional state to track (1) whether there is a pending call and (2) the
component which the last pending call is from.
   Any equivalence class 𝐸 of 𝑃⧛ = 𝑃1 ⧛ · · · ⧛ 𝑃𝑛 is the restriction of a unique equivalence class
𝐸 ′ of 𝑃 ∥ = 𝑃1 ∥ · · · ∥ 𝑃𝑛 to 𝑃⧛ . The definition of ≺′ ensures that the min ⪯ (𝐸) = min ⪯ ′ (𝐸 ′ ).
Then, since any equivalence class of 𝑃 ∥ contains a unique equivalence class of 𝑃 ⧛ , it follows that
red ≺ (𝑃⧛ ) = red ≺ ′ (𝑃 ∥ ).                                                                      □
Products of Recursive Programs for Hypersafety Verification                                                     33


  Proof of Theorem 4.4. Suppose ≺ is a VPO and 𝑃1, . . . , 𝑃𝑛 are VPLs (well-matched by our global
assumption). By Lemma 4.3, for some coherent VPO ≺′ , we have
                                  red ≺ (𝑃 1 ⧛ · · · ⧛ 𝑃𝑛 ) = red ≺ ′ (𝑃1 ∥ · · · ∥ 𝑃𝑛 ).
Then, by Theorem 3.18, red ≺ (𝑃1 ⧛ · · · ⧛ 𝑃𝑛 ) is visibly pushdown.                                            □
   Proof of Theorem 4.5. Suppose 𝐴 = (𝑄 𝐴 , {𝑞𝐴in }, Γ𝐴 , 𝑄 𝐴 , 𝛿𝐴 ) and 𝑃𝑖 is given by 𝐴𝑖 = (𝑄𝑖 , 𝑄𝑖in, Γ𝑖 , 𝐹𝑖 , 𝛿𝑖 ).
Suppose ≺ is uniform w.r.t. 𝐴1, 𝐴2 . We further assume that 𝐹𝑖 has no outgoing transition; 𝐴𝑖 can
be modified to satisfy this condition without breaking uniformity. Assume Γ1 ∩ Γ2 = {⊥} and let
Γ12 = Γ1 ∪ Γ2 . For any 𝑞 1 ∈ 𝑄 1 , 𝑞 2 ∈ 𝑄 2 , and 𝛾 ∈ Γ12 , define enabled(𝑞 1, 𝑞 2, 𝛾) as the set of outgoing
letters enabled at 𝑞 1 or 𝑞 2 when the stack top is 𝛾 (if 𝛾 ∉ Γ𝑖 , then enabled(𝑞 1, 𝑞 2, 𝛾) contains no
letter from Σ𝑖ret ).
   We construct 𝑅 = (𝑄, 𝑄 in, Γ, 𝐹, 𝛿), which simulates the interleaving of 𝐴1 and 𝐴2 , with a concep-
tual stack 𝑆, guided by 𝐴.
      • 𝑄 = 𝑄 1 ×𝑄 2 ×𝑄 𝐴 × Γ12 . The state (𝑞 1, 𝑞 2, 𝑞𝐴 , 𝛾) ∈ 𝑄 maintains the states 𝑞 1, 𝑞 2, 𝑞𝐴 in 𝐴1, 𝐴2, 𝐴
         respectively and the top 𝛾 of the stack 𝑆.
      • 𝑄 in = 𝑄 1in × 𝑄 2in × {𝑞𝐴in } × {⊥}.
      • Γ = (Γ12 × Γ𝐴 × Γ12 ) ∪ {⊥}. When (𝛾, 𝛾𝐴 , 𝛾 ′ ) is the stack top of 𝑅, the top two elements of 𝑆
         are 𝛾 and 𝛾 ′ (in that order), and the stack top of 𝐴 is 𝛾𝐴 .
      • 𝐹 = 𝐹 1 × 𝐹 2 × 𝑄 𝐴 × Γ12 .
      • For any 𝑞 = (𝑞 1, 𝑞 2, 𝑞𝐴 , 𝛾) ∈ 𝑄, if minord(𝑞𝐴 ) (enabled(𝑞 1, 𝑞 2, 𝛾)) ∈ e Σ1 ,
           – for all (𝑞 1, 𝜎, 𝑞 1′ ) ∈ 𝛿 1int and (𝑞𝐴 , 𝜎, 𝑞𝐴′ ) ∈ 𝛿𝐴int , we have
                                               (𝑞, 𝜎, (𝑞 1′ , 𝑞 2, 𝑞𝐴′ , 𝛾)) ∈ 𝛿 int ;
           – for all (𝑞 1, 𝜎, 𝑞 1′ , 𝛾 1 ) ∈ 𝛿 1call and (𝑞𝐴 , 𝜎, 𝑞𝐴′ , 𝛾𝐴 ) ∈ 𝛿𝐴call , we have
                                      (𝑞, 𝜎, (𝑞 1′ , 𝑞 2, 𝑞𝐴′ , 𝛾 1 ), (𝛾 1, 𝛾𝐴 , 𝛾)) ∈ 𝛿 call ;
           – for all (𝑞 1, 𝜎, 𝛾, 𝑞 1′ ) ∈ 𝛿 1ret , (𝑞𝐴 , 𝜎, 𝛾𝐴 , 𝑞𝐴′ ) ∈ 𝛿𝐴ret , and 𝛾 ′ ∈ Γ12 , we have
                                      (𝑞, 𝜎, (𝛾, 𝛾𝐴 , 𝛾 ′ ), (𝑞 1′ , 𝑞 2, 𝑞𝐴′ , 𝛾 ′ )) ∈ 𝛿 ret .
       The case where minord(𝑞𝐴 ) (enabled(𝑞 1, 𝑞 2, 𝛾)) ∈ eΣ2 is symmetrical, and 𝛿 is the smallest set
       defined by these rules.
Let 𝑃 be the automaton for 𝑃1 ⧛ 𝑃 2 constructed in Theorem 4.2. By relating accepted runs of 𝑅 to
those of 𝑃, one can show that L (𝑅) ⊂ L (𝑃). Furthermore, for any word 𝜌 over e        Σ, 𝜌 ∈ L (𝑅) ⇔
𝜌 ∈ red ≺ (𝑃 1 ⧛ 𝑃 2 ). We omit a formal proof by induction but point out the key lemmas.
   ⇒: For any word 𝜌 ∈ L (𝑅) and words 𝛼, 𝛽 such that 𝜌 = 𝛼𝛽, if 𝑅 reaches state (𝑞 1, 𝑞 2, 𝑞𝐴 , 𝛾) after
       reading 𝛼 in an accepted run over 𝜌, then 𝑥 ∈ enabled(𝑞 1, 𝑞 2, 𝛾) for any letter 𝑥 ∈ alph(𝛽)
       that can commute to the right of 𝛼.
   ⇐: For any word 𝜌 ∈ red ≺ (𝑃1 ⧛ 𝑃2 ) and words 𝛼, 𝛽 and letter 𝑥 ∈ e     Σ𝑖 such that 𝜌 = 𝛼𝑥𝛽, if 𝑃
       reaches (𝑞 1, 𝑞 2 ) with stack top 𝛾 after reading 𝛼 in an accepted run over 𝜌, then 𝑥 ≺𝛼 𝑦 for
                                             Σ𝑖 .
       all letter 𝑦 ∈ enabled(𝑞 1, 𝑞 2, 𝛾) \ e
       Note that this does not hold without the assumption that 𝐹 1 and 𝐹 2 have no outgoing
       transition.
  Lastly, we observe that |𝑄 | = |𝑄 1 ||𝑄 2 ||𝑄 𝐴 ||Γ12 |.                                             □
                    dep
          Σ𝑖 , let e
  For any e        Σ𝑖 be all letters in e
                                        Σ𝑖 that do not soundly commute with all letters in other
                                                       indep
components. In other words, it is the complement of e Σ𝑖     .
34                                                                                Ruotong Cheng and Azadeh Farzan

                                                                                               indep
                                                                                Σ𝑖
   Lemma C.1. Let the nonterminal 𝑌 generate exactly the well-matched runs over e                      . The following
statements are equivalent:
     (1) 𝑃𝑖 is tail-independent (resp. head-independent).
                                                                                                                  dep
                                                                                                                 Σ𝑖 ,
     (2) For every run 𝜌 of 𝑃𝑖 and every pair of positions 𝑗 < 𝑗 ′ (resp. 𝑗 > 𝑗 ′ ) in 𝜌 such that 𝜌 𝑗 , 𝜌 𝑗 ′ ∈ e
         for all positions 𝑘, 𝑙 in 𝜌 such that 𝑘 ⇝ 𝑙, we have 𝑘 < 𝑗 < 𝑙 ⇒ 𝑘 < 𝑗 < 𝑙.     ′

     (3) Every run of 𝑃𝑖 is derivable from 𝑋 , whose grammar is given by

                                          𝑋 → 𝑌 | 𝑎𝑋 | 𝑐𝑌𝑟𝑋 | 𝑐𝑋𝑟𝑌 ,

         where 𝑎, 𝑐, and 𝑟 range over all letters in Σ𝑖int , Σ𝑖call , and Σ𝑖ret respectively. (resp. 𝑋 → 𝑌 | 𝑋𝑎 |
         𝑋𝑐𝑌𝑟 | 𝑌𝑐𝑋𝑟 )

  Proof. We prove the equivalence for tail-independence. The case for head-independence is
symmetrical.
      (1) ⇒ (2): Suppose (1). Let 𝜌 be a run of 𝑃𝑖 . Write 𝜌 = 𝑢𝑣 as in the definition. Let 𝑗 < 𝑗 ′ be a
                                                    dep
                                                   Σ𝑖 . Then they are both in 𝑢. Let 𝑘, 𝑙 be positions such
         pair of positions such that 𝜌 𝑗 , 𝜌 𝑗 ′ ∈ e
         that 𝑘 ⇝ 𝑙 and 𝑘 < 𝑗 < 𝑙. Then 𝑘 is in 𝑢 and 𝑙 is in 𝑣, which shows that 𝑘 < 𝑗 < 𝑗 ′ < 𝑙.
                                                                                 dep
      (2) ⇒ (1): Suppose (2). Let 𝜌 be a run of 𝑃𝑖 . If there is no letter in eΣ𝑖 in 𝑃𝑖 , then any division
         𝜌 = 𝑢𝑣 satisfies the requirement. Otherwise, let 𝑢 be the shortest prefix of 𝜌 that contains
                               dep                                                   indep
         the last letter in eΣ𝑖 and write 𝜌 = 𝑢𝑣. Then all letters in 𝑣 are in e    Σ𝑖     .
                                                          dep
         Suppose 𝑘 ⇝ 𝑙 and there is some letter in Σ𝑖 . It suffices to show that 𝑘 is in 𝑢 and 𝑙 is in 𝑣.
                                                        e
                                         dep
         Indeed: since any letter in e Σ𝑖 must be in 𝑢, the position 𝑘 is in 𝑢; since 𝑙 is behind the last
                       dep
         letter in eΣ𝑖 , the position 𝑙 is in 𝑣.
      (2) ⇒ (3): We will prove the stronger claim that for any well-matched run over e           Σ𝑖 , if for every
                                                                  dep
         pair of positions 𝑗 < 𝑗 in 𝜌 such that 𝜌 𝑗 , 𝜌 𝑗 ∈ Σ𝑖 , for all positions 𝑘, 𝑙 in 𝜌 such that
                                    ′                       ′    e
         𝑘 ⇝ 𝑙, we have 𝑘 < 𝑗 < 𝑙 ⇒ 𝑘 < 𝑗 ′ < 𝑙, then 𝜌 is derivable from 𝑋 .
         Let 𝜌 be well-matched run over e     Σ𝑖 such that the condition holds. Assume by induction that
         the statement holds for shorter runs.
         If 𝜌 = 𝜖, then 𝜌 is derivable from 𝑌 and therefore 𝑋 .
                                                                                                             dep
         If 𝜌 = 𝑎𝑣, where 𝑎 ∈ Σ𝑖int , then 𝑣 also satisfies the condition, no matter whether 𝑎 ∈ e         Σ𝑖 or
         not, and is therefore derivable from 𝑋 . Thus, 𝜌 is derivable from 𝑋 .
         If 𝜌 = 𝑐𝑤𝑟𝑣, where 𝑐 ∈ Σ𝑖int and 𝑟 is the matching return, then 𝑤 also satisfies the condition
                                                                           indep
         and is thus derivable from 𝑋 ; all letters in 𝑣 must be in e    Σ𝑖      , so 𝑣 is derivable from 𝑌 .
         Hence, 𝑋 ⇒ 𝑐𝑋𝑟𝑌 ⇒∗ 𝜌.
      (3) ⇒ (2): Suppose (3). Let 𝜌 be a run of 𝑃𝑖 . Suppose words shorter than 𝜌 all satisfy the
                                                                                             dep
         requirement in (2). Let 𝑗 < 𝑗 ′ be a pair of positions such that 𝜌 𝑗 , 𝜌 𝑗 ′ ∈ e Σ𝑖 . Consider the
         first step of a derivation of 𝜌 from 𝑋 . We will show that for all positions 𝑘, 𝑙 in 𝜌 such that
         𝑘 ⇝ 𝑙, we have 𝑘 < 𝑗 < 𝑙 ⇒ 𝑘 < 𝑗 ′ < 𝑙.
           𝑋 ⇒ 𝑌 . This cannot happen due to the existence of 𝜌 𝑗 .
           𝑋 ⇒ 𝑎𝑋 . If 𝑗 is the position of 𝑎, then no 𝑘, 𝑙 exist. Otherwise, by induction hypothesis.
           𝑋 ⇒ 𝑐𝑌𝑟𝑋 . Both 𝑗 and 𝑗 ′ can only be in 𝑋 on the RHS. Use induction hypothesis.
           𝑋 ⇒ 𝑐𝑋𝑟𝑌 . Still, both 𝑗 and 𝑗 ′ can only be in 𝑋 on the RHS. Suppose 𝑘 ⇝ 𝑙 and 𝑘 < 𝑗 < 𝑙.
               If 𝑘, 𝑙 are the positions of 𝑐, 𝑟 respectively, then they also enclose 𝑗 ′ . Otherwise, they
               are inside 𝑋 on the RHS, and we use induction hypothesis.
                                                                                                                    □
Products of Recursive Programs for Hypersafety Verification                                                     35


  Proof of Proposition 5.2. By Lemma C.1, 𝑃𝑖 is tail-independent iff 𝑃𝑖 ⊂ L (𝑋 ). Note that

                                               𝑌 → 𝜖 | 𝑎𝑌 | 𝑐𝑌𝑟𝑌 ,
                                                     indep
where 𝑎, 𝑐, and 𝑟 range over all letters in Σ𝑖int ∩ e
                                                    Σ𝑖     , Σ𝑖call , and Σ𝑖ret respectively. (Recall we assume
that calls and returns fully commute with letters in other components.) Thus, the grammar for 𝑋
can be rewritten to a VPG, which shows L (𝑋 ) is a VPL.
  We have 𝑃𝑖 ⊂ L (𝑋 ) ⇐⇒ 𝑃𝑖 ∩ L (𝑋 ) c = ∅. By [2, Theorem 6], one can convert the VPG for
L (𝑋 ) into a VPA with 𝑂 (1) states and stack alphabet of size 𝑂 (|e         Σ𝑖 |). By [2, Theorem 2], this VPA
can be determinized to have 𝑂 (1) states and stack alphabet of size 𝑂 (|e            Σ𝑖 |). Then, 𝑃𝑖 ∩ L (𝑋 ) c can
be constructed as a VPA with polynomial size, and its emptiness can be decided in polynomial time.
  A similar argument, rewriting the grammar to a “reversed” VPG, holds for head-independence. □

   Proof of Theorem 5.3. We use the characterization (3) of tail-independence in Lemma C.1.
   Let 𝜋𝑖 be the projection ΠeΣ𝑖 . Let e    Σ𝑖′ be the subset of e
                                                                 Σ𝑖 that soundly commutes with every letter
          Σ 𝑗 . Let 𝐼 be the largest sound commutativity relation.
   Ð
in 𝑗≠𝑖 e
   We will prove by induction that, if 𝑃 1, . . . , 𝑃𝑛 are tail-independent singleton languages, then
every word in 𝑃1 ∥ · · · ∥ 𝑃𝑛 is 𝐼 -equivalent to some word in 𝑃1 ⧛ · · · ⧛ 𝑃𝑛 .
   Let 𝑃 1 = {𝜌 1 }, . . . , 𝑃𝑛 = {𝜌𝑛 } be tail-independent singleton languages and suppose the statement
holds on smaller instances. Let 𝜌 ∈ 𝑃1 ∥ · · · ∥ 𝑃𝑛 . If 𝜌 contains no call (and thus no return), then
the statement holds. Otherwise, write 𝜌 = 𝛼𝑐𝛽𝑟𝛾, where 𝑐 is the first call in 𝜌, and 𝑟 ∈ Σ𝑖ret matches
𝑐 in 𝜌𝑖 .
                          Σ𝑖′ , then 𝜌 ≡𝐼 𝛼𝑐𝛽 ′𝑟 𝛽 ′′𝛾, where 𝛽 ′ = 𝜋𝑖 (𝛽); in other words, we move letters
      • If alph(𝜋𝑖 (𝛽)) ⊂ e
                          Σ𝑖 forward. Invoke the induction hypothesis on ({𝜋 𝑗 (𝛽 ′′𝛾)}) 𝑗 ∈ [𝑛] .
        in 𝛽𝑟 that are in e
                          Σ𝑖′ , then the derivation of 𝜌𝑖 must have the form
      • If alph(𝜋𝑖 (𝛽)) ⊄ e

                      𝑋 ⇒ 𝑎 1𝑋 ⇒ · · · ⇒ 𝑎 1 · · · 𝑎𝑛 𝑋 ⇒ 𝑎 1 · · · 𝑎𝑛 𝑐𝑋𝑟𝑌 ⇒ · · · ⇒ 𝜌𝑖 ,

        where 𝑌 ⇒∗ 𝜋𝑖 (𝛾). Therefore, 𝜌 ≡𝐼 𝛼𝑐𝛽𝛾 ′𝑟𝛾 ′′ , where 𝛾 ′′ = 𝜋𝑖 (𝛾); in other words, we move
                                  Σ𝑖 backward. Invoke the induction hypothesis on ({𝜋 𝑗 (𝛽𝛾 ′ )}) 𝑗 ∈ [𝑛] .
        letters in 𝑟𝛾 that are in e
   For any languages 𝐿1, . . . , 𝐿𝑛 , the shuffle (resp. well-nested shuffle) of 𝐿1, . . . , 𝐿𝑛 is the union of
the shuffle (resp. well-nested shuffle) of {𝜌 1 }, . . . , {𝜌𝑛 } for all 𝜌 1 ∈ 𝐿1, . . . , 𝜌𝑛 ∈ 𝐿𝑛 . Therefore, if
𝑃1, . . . , 𝑃𝑛 are tail-independent languages that are not necessarily singletons, it still holds that every
word in 𝑃1 ∥ · · · ∥ 𝑃𝑛 is 𝐼 -equivalent to some word in 𝑃1 ⧛ · · · ⧛ 𝑃𝑛 .
   The case for head-independent languages is symmetrical.                                                      □

   Proof of Proposition 6.1. A VP contextual order is given by a complete deterministic VPA
𝐴 = (𝑄, {𝑞 in }, Γ, 𝑄, 𝛿) together with a map ord : 𝑄 → TO(Σ). Below, we define 𝐴 and ord for each
of concatenation, nested concatenation, and 𝒔-lockstep. We assume Γ = 𝑄 ⊎ {⊥} and write the VPA
like a weakly-hierarchical linear accepting NWA [3], i.e., the automaton pushes 𝑞 if at state 𝑞 a call
letter is read. Since 𝑃𝑖 ’s are well-matched, we omit the case when a pending return is read.
     Concatenation Let 𝐴 be a complete deterministic VPA with a single state ★. Let ord(★) be
       any linear order such that Σ1 < · · · < Σ𝑛 , i.e., if 𝑥 ∈ Σ𝑖 , 𝑦 ∈ Σ 𝑗 , and 𝑖 < 𝑗, then 𝑥 < 𝑦.
     Nested Concatenation Let 𝐴 be a complete deterministic VPA with a single state ★. Let
       ord(★) be any linear order such that Σint
                                               1 ∪ Σ1 < · · · < Σ𝑛 ∪ Σ𝑛 < Σ .
                                                        call            int      call   ret
36                                                                                       Ruotong Cheng and Azadeh Farzan


       𝒔-lockstep Let 𝑄 = {(𝑡 1, . . . , 𝑡𝑛 ) | 0 ≤ 𝑡𝑖 ≤ 𝑠𝑖 for each 𝑖} ∪ {★}. Let 𝑞 in = (0, . . . , 0). For all
          states 𝑞, 𝑞 ′, (𝑡 1, . . . , 𝑡𝑛 ) ∈ 𝑄 and letters 𝑎𝑖 ∈ Σ𝑖int, 𝑐𝑖 ∈ Σ𝑖call, 𝑟𝑖 ∈ Σ𝑖ret ,
                                 𝛿 int (𝑞, 𝑎𝑖 ) = 𝑞,
                               𝛿 call (★, 𝑐𝑖 ) = ★,
                                                   (
                      call                           (0, . . . , 0, 𝑠𝑖 − 1, 𝑠𝑖+1, . . . , 𝑠𝑛 ), if 𝑡𝑖 = 0
                     𝛿 ((𝑡 1, . . . , 𝑡𝑛 ), 𝑐𝑖 ) =
                                                     (0, . . . , 0, 𝑡𝑖 − 1, 𝑡𝑖+1, . . . , 𝑡𝑛 ), otherwise
                                                   (
                                                    𝑞 ′, if 𝑞 ′ = (𝑡 1, . . . , 𝑡𝑛 ) ∧ 𝑡𝑖 = 0
                           𝛿 ret (𝑞, 𝑞 ′, 𝑟𝑖 ) =
                                                    ★. otherwise
          ord(★) is any linear order such that Σ1 < · · · < Σ𝑛 . ord((𝑡 1, . . . , 𝑡𝑛 )) is any linear order such
          that Σint
                1 < · · · < Σ𝑛 < Σ 𝑗
                               int     call < Σcall < · · · < Σcall < Σcall < · · · Σcall < Σret , where 𝑗 is
                                               𝑗+1             𝑛        1                 𝑗 −1
          smallest index such that 𝑡 𝑗 > 0.
                                                                                                                □
   Proof of Theorem 6.2. By Proposition 6.1, induction, and the fact that for any permuation 𝜋
of {1, . . . , 𝑛},
                            𝑃𝜋 (1) ⧛ · · · ⧛ 𝑃𝜋 (𝑛) = 𝑃 1 ⧛ · · · ⧛ 𝑃𝑛 .
                                                                                                                      □
  Proof of Proposition 6.3. Suppose ≺ is represented by VPA 𝐴 = (𝑄 𝐴 , 𝑄 𝐴in, Γ𝐴 , 𝛿𝐴 , 𝑄 𝐴F ) together
with map ord. Define VPA 𝐴′ = (𝑄 𝐴 , 𝑄 𝐴in, Γ𝐴 ⊎ {★}, 𝛿𝐴′ , 𝑄 𝐴F ), where 𝛿𝐴′ is obtained from 𝛿𝐴 by
       • replacing every (𝑞, 𝑐, 𝑞 ′, 𝛾) ∈ 𝛿𝐴call such that 𝑐 ∈ Σ′ with (𝑞, 𝑐, 𝑞 ′′, ★), where (𝑞, 𝑓 (𝑐), 𝑞 ′′ ) ∈ 𝛿𝐴 ;
          and
       • replacing every (𝑞, 𝑟, 𝛾, 𝑞 ′ ) ∈ 𝛿𝐴ret such that 𝑟 ∈ Σ′ with (𝑞, 𝑟, ★, 𝑞 ′′ ), where (𝑞, 𝑓 (𝑟 ), 𝑞 ′′ ) ∈ 𝛿𝐴 .
    Let 𝑤 = 𝑤 1 · · · 𝑤𝑘 be any prefix of any run of 𝑃1 ⧛ · · · ⧛ 𝑃𝑛 . Let (𝑞, 𝑠) be the configuration of
𝐴 after reading 𝑓 (𝑤). Then the configuration of 𝐴′ after reading 𝑤 is (𝑞, 𝑠 ′ ), where 𝑠 ′ is obtained
from 𝑠 by inserting ★ pushed by all 𝑤𝑖 ∈ Σ′ that is a pending call.
    Define map ord′ : 𝑄 𝐴 → TO(e           Σ) over the states of 𝐴′ by mapping 𝑞 ∈ 𝑄 𝐴 to any linear order
extending {(𝑎, 𝑏) | (𝑓 (𝑎), 𝑓 (𝑏)) ∈ ord(𝑞)}. One can show that such an extension always exists, e.g.,
by the Order-Extension Principle. We can take any extension because reducing 𝑃1 ⧛ · · · ⧛ 𝑃𝑛 under
I only compares 𝑎, 𝑏 from different e          Σ𝑖 ’s, and in this case 𝑓 (𝑎) and 𝑓 (𝑏) are already comparable by
ord(𝑞). The contextual order ≺′ represented by VPA 𝐴′ together with map ord′ satisfies red ≺ ′ (𝑃1 ⧛
· · · ⧛ 𝑃𝑛 ) = red 𝑓 ( ≺ ) (𝑃1 ⧛ · · · ⧛ 𝑃𝑛 ).                                                                       □

C.1     Semantics
Let top(𝑆) denote the top frame of a nonempty stack 𝑆 and let
                                          top(𝑺) := (top(𝑆 1 ), . . . , top(𝑆𝑛 ))
for a tuple of nonempty stacks 𝑺 = (𝑆 1, . . . , 𝑆𝑛 ). We have the following lemma, which can be proved
by induction. Note the right-hand side of the implication states the equation of two sets.
                               Σ1 ⧛ · · · ⧛ e   Σ𝑛 without pending returns, 𝑺 ∈ 𝑛𝑗=1 Stack(𝑉𝑗 ), and
                                                                                    Î
   Lemma C.2. For any 𝜌 ∈ e
𝑆 ∈ Stack(𝑉 ),
                      top(𝑺) = top(𝑆) =⇒ top(MJ𝜌K(𝑺)) = top(SJ𝜌K(𝑆)).
                                                 Σ1 ⧛ · · · ⧛ e
     Proof of Theorem 7.1. Formally, for any 𝜌 ∈ e            Σ𝑛 without pending returns,
Products of Recursive Programs for Hypersafety Verification                                                                 37


       • under the semantics M, {𝐴}𝜌 {𝐵} is valid iff top(𝑺) |= 𝐴 ⇒ top(𝑺 ′ ) |= 𝐵 for all (𝑺, 𝑺 ′ ) ∈
         MJ𝜌K;
       • under the semantics S, {𝐴}𝜌 {𝐵} is valid iff top(𝑆) |= 𝐴 ⇒ top(𝑆 ′ ) |= 𝐵 for all (𝑆, 𝑆 ′ ) ∈ SJ𝜌K.
  Let 𝜌 ∈ 𝑃1 ⧛ · · · ⧛ 𝑃𝑛 . Suppose {𝐴}𝜌 {𝐵} under the semantics S. By Lemma C.2, for any (𝑺, 𝑺 ′ ) ∈
MJ𝜌K, there is some (𝑆, 𝑆 ′ ) ∈ SJ𝜌K such that top(𝑺) = top(𝑆) and top(𝑺 ′ ) = top(𝑆 ′ ); since
{𝐴}𝜌 {𝐵} under the semantics S, we have top(𝑆) |= 𝐴 ⇒ top(𝑆 ′ ) |= 𝐵, and therefore top(𝑺) |=
𝐴 ⇒ top(𝑺 ′ ) |= 𝐵. This shows that {𝐴}𝜌 {𝐵} under the semantics M ′ . The other direction is
symmetrical.                                                                                        □

D     Extra Details
D.1     CHC Encodings
We use the alphabet introduced in Appendix A.1.

   Directly Encode an NWA. Let 𝐴 = (𝑄, 𝑄 in, 𝑄 F, e   Σ, 𝛿) be a linearly accepting, weakly hierarchical

NWA      without  pending  returns such that for any (𝑞, 𝑞 ′, ret f , 𝑞 ′′ ) ∈ 𝛿, any outgoing call letter at 𝑞 ′ is
call f . For each state 𝑞 ∈ 𝑄, declare a predicate 𝐼𝑞 (𝒙, 𝒍, 𝑟 ), which represents an assertion that holds
at 𝑞 relating the function arguments 𝒙, the local variables 𝒍, and the return address 𝑟 ∈ 𝑄 ⊎ {⊥}
at the current stack frame, where ⊥ denotes the stack bottom. Each transition in 𝛿 translates to a
constrained Horn clause:
       • (𝑞, 𝑎, 𝑞 ′ ) ∈ 𝛿 such that 𝑎 ∈ Σint translates to

                                     𝐼𝑞 (𝒙, 𝒍, 𝑟 ) ∧ SJ𝑎K(𝒍, 𝒍 ′ ) =⇒ 𝐼𝑞 ′ (𝒙, 𝒍 ′, 𝑟 ).
             
       • (𝑞, call f , 𝑞 ′ ) ∈ 𝛿 translates to
                                                    Û
                              𝐼𝑞 (𝒙, 𝒍, 𝑟 ) ∧                  𝑝 ′ = 𝑝 ′ = 𝑝 =⇒ 𝐼𝑞 ′ (𝒙 ′, 𝒍 ′, 𝑞).
                                                𝑝 ∈param(𝑓 )
                  
       • (𝑞, 𝑞 ′, ret f , 𝑞 ′′ ) ∈ 𝛿 translates to

                                            © Û
    𝐼𝑞 (𝒙, 𝒍, 𝑞 ′ ) ∧ 𝐼𝑞 ′ (𝒙 ′, 𝒍 ′, 𝑟 ) ∧ ­             𝑝 = 𝑝 ′®
                                                                 ª

                                            «𝑝 ∈param(𝑓 )        ¬                             !
                                                             Û
                                                          ∧      𝑙 = ite(𝑙 ∈ output(𝑓 ), 𝑙, 𝑙 ) =⇒ 𝐼𝑞 ′′ (𝒙 ′, 𝒍 ′′, 𝑟 ).
                                                                  ′′                         ′

                                                          𝑙 ∈𝒍

    To verify a pair of pre/postconditions pre and post, add the clauses

                                                                 pre =⇒ 𝐼𝑞 in (𝒙, 𝒍, ⊥),
                                        𝐼𝑞 F (𝒙, 𝒍, 𝑟 ) ∧ ¬post =⇒ ⊥

for all 𝑞 in ∈ 𝑄 in , 𝑞 F ∈ 𝑄 F , and 𝑟 ∈ 𝑄 ⊎ {⊥}. If it is known that L (𝐴) is well-matched, then it suffices
to take 𝑟 = ⊥.
   The following proposition states the soundness and completeness of the encoding:

  Proposition D.1. Let 𝐴 = (𝑄, 𝑄 in, 𝑄 F, eΣ, 𝛿) be a linearly accepting, weakly hierarchical NWA
without pending returns such that for any (𝑞, 𝑞 ′, ret f , 𝑞 ′′ ) ∈ 𝛿, any outgoing call letter at 𝑞 ′ is call f .
Let 𝑃 = L (𝐴). For the recursive program (𝑃, S), the CHC encoding is satisfiable iff {pre}𝑃 {post}.
38                                                                                    Ruotong Cheng and Azadeh Farzan


  Proof. ⇒: Suppose the CHC encoding is satisfiable. Let 𝜌 be a nested word with an accepting
         𝜌1       𝜌𝑛
run 𝑞 0 −→ · · · −−→ 𝑞𝑛 . Then 𝜌 can be annotated with an inductive sequence of nested interpolants4 [35,
Definition 5] 𝐽0, . . . , 𝐽𝑛 , where 𝐽𝑖 = {(𝒙, 𝒍) | 𝐼𝑞𝑖 (𝒙, 𝒍, 𝑟 )} (we use (𝒙, 𝒍) to denote the corresponding
valuation) and 𝑟 is the state just before the last pending call in 𝜌 1 · · · 𝜌𝑖 , or ⊥ if no such state exists.
By the construction of the CHC, pre ⇒ 𝑞 0 and 𝑞𝑛 ⇒ post. One can show that such an annotation
implies {pre}𝜌 {post}.
  ⇐: Prove by induction that given a derivation of 𝐼𝑞 (𝒙, 𝒍, 𝑟 ), one can construct a nested word 𝜌
such that
       • There is a partial run of 𝐴 over 𝜌 that ends at state 𝑞. Moreover, if 𝑟 = ⊥, then 𝜌 is well-
         matched; otherwise, 𝜌 has a pending call, 𝑟 is the state before the last pending call in this
         run.
       • 𝜌 can be annotated with an inductive sequence of nested interpolants that starts with some
         {𝜈 } such that 𝜈 |= pre and ends with {(𝒙, 𝒍)}.
Then, from a derivation of ⊥, one can extract a counterexample that witnesses {pre}𝑃 {post} does
not hold.                                                                                     □

   Encode a VPG. The semantics of a well-matched syntactic run can be given without an explicit
stack, as a relation on valuations rather than stacks of valuations. Let 𝑇 be the set of all valuations.
Unlike the direct encoding of an NWA, the ghost variables for function arguments are not needed.
    • S ′ J𝜖K
             := {(𝜈, 𝜈) : 𝜈 ∈ 𝑇 }.
    • S ′ Jassume 𝜙 K := {(𝜈, 𝜈) : 𝜈 |= 𝜙 }.
            
    • S ′ J𝑥 := 𝑡 K :=
                         {(𝜈, 𝜈 ⊕ {𝑥 ↦→ 𝜈Ð(𝑡)}) : 𝜈 ∈ 𝑇 }.
    • S ′ Jcall 𝑞 𝜌 ret 𝑞 K := {(𝜈, 𝜈 ⊕ 𝑦 {𝑦 ↦→ 𝜇 ′ (𝑦)}) : (𝜇, 𝜇 ′ ) ∈ S ′ J𝜌K ∧ 𝑥 𝜇 (𝑥) = 𝜈 (𝑥)}, where
                                                                                     Ó
       𝜌 is well-matched and 𝑥, 𝑦 range over the input and output variables of 𝑞 respectively.
    • S ′ J𝜌𝜏K = S ′ J𝜏K ◦ S ′ J𝜌K, where 𝜌, 𝜏 are well-matched.
  Let 𝑋 be all variables in the program. Given a well-matched VPG 𝐺 = (𝑉 , e                Σ, 𝑃, 𝑆), for each
nonterminal 𝐿 ∈ 𝑉 , declare a predicate 𝑃𝐿 (𝑋, 𝑋 ′ ) that overapproximates the semantics of all words
produced by 𝐿. Each production in 𝑃 translates to a constrained horn clause:
       • 𝐿 → 𝑎𝐿 ′ translates to
                                SJ𝑎K(𝑋, 𝑋 ′ ) ∧ 𝑃𝐿′ (𝑋 ′, 𝑋 ′′ ) =⇒ 𝑃𝐿 (𝑋, 𝑋 ′′ ).
                        
      • 𝐿 → call 𝑞 𝐿 ′ ret 𝑞 𝐿 ′′ translates to
              !                         !               !
      Û             Û                       Û
         ′                  (3)      ′′          (3)
        𝑥 =𝑥 ∧            𝑦 =𝑦 ∧               𝑧 =𝑧
       𝑥                 𝑦                    𝑧≠𝑦

                                                         ∧ 𝑃𝐿′ (𝑋 ′, 𝑋 ′′ ) ∧ 𝑃𝐿′′ (𝑋 (3) , 𝑋 (4) ) =⇒ 𝑃𝐿 (𝑋, 𝑋 (4) )
         where 𝑥, 𝑦 range over the input and output variables of 𝑞 respectively.
       • 𝐿 → 𝜖 translates to         Û
                                         𝑧 ′ = 𝑧 =⇒ 𝑃𝐿 (𝑋, 𝑋 ′ ).
                                            𝑧 ∈𝑋
     To verify a safety property 𝑝 (𝑋, 𝑋 ′ ), add for all start symbol 𝐿 the clause
                                         𝑃𝐿 (𝑋, 𝑋 ′ ) ∧ ¬𝑝 (𝑋, 𝑋 ′ ) =⇒ ⊥.
4 In the context of this definition, an interpolant is a set of valuations. For our purpose, we remove the requirement that

𝐽0 = ⊤ and 𝐽𝑛 = ⊥.
Products of Recursive Programs for Hypersafety Verification                                              39


D.2    Parameterized Lockstep
Define 𝐺 0 := 𝑛𝑖=1 (𝐺𝑖 ∪ {𝑌 ′ → 𝑐𝑊 𝑟 𝐸 : (𝑌 → 𝑐𝑊 𝑟𝑉 ) ∈ 𝐺𝑖 }) ∪ {𝐸 → 𝜖}. The rules are listed in
               Ð
Fig. 8. The nonterminal symbols of the grammar 𝐺 of the 𝒎-lockstep of L (𝐺 1 ), . . . , L (𝐺𝑛 ) have
               Î
the form [𝒔, 𝒕, 𝑘𝑖=0 𝑊𝑖 ], where 𝒔, 𝒕 satisfy the constraints in Section 6.1, 𝑊𝑖 is a nonterminal in 𝐺 0
for each 𝑖, and the length and maximum element of 𝒔 are bounded by those of 𝒎. Moreover, to
                           Î 𝑗 −1          Î                   Î
account for Ls-Eps, [𝒔, 𝒕, 𝑖=1    𝑊𝑖 × 𝐸 × 𝑘𝑖=𝑗 𝑊𝑖 ] and [𝒔, 𝒕, 𝑘𝑖=1 𝑊𝑖 ] are treated as the same symbol
for any 𝑘 > 1.

                                    G-LsInt
 G-LsOne                                                   ∀𝑖 ∈ [𝑘]. (𝑊𝑖 → 𝛼𝑖 ) ∈ 𝐺 0
      (𝑋 → 𝛼) ∈ 𝐺 0                 (𝑈 𝑗 → 𝑎𝑊 𝑗 ) ∈ 𝐺 0     none of 𝛼𝑖 where 𝑖 < 𝑗 starts with an internal
                                                                                                
  ([𝒔, 𝒕, 𝑋 ] → 𝛼) ∈ 𝐺                            Î 𝑗 −1         Î                     Î
                                            [𝒔, 𝒕, 𝑖=1 𝑊𝑖 × 𝑈 𝑗 × 𝑘𝑖=𝑗+1 𝑊𝑖 ] → 𝑎[𝒔, 𝒕, 𝑘𝑖=1 𝑊𝑖 ] ∈ 𝐺

                 G-LsFstCall
                                       ∀𝑖 ∈ [𝑘]. (𝑌𝑖 → 𝑐𝑖𝑊𝑖 𝑟𝑖 𝑉𝑖 ) ∈ 𝐺 0        𝒕 =0
                                                                                               
                      [𝒔, 𝒕,
                               Î𝑘                                Î𝑘       ′            Î𝑛
                                𝑖=1 𝑌𝑖 ] → 𝑐 1 [𝒔, dec𝒔 (𝒕),𝑊1 ×    𝑖=2 𝑌𝑖 ] 𝑟 1 [𝒔, 𝒕, 𝑖=1 𝑉𝑖 ] ∈ 𝐺

                G-LsRstCall
                      ∀𝑖 ∈ [𝑘]. (𝑌𝑖 → 𝑐𝑖𝑊𝑖 𝑟𝑖 𝑉𝑖 ) ∈ 𝐺 0      𝒕 ≠0     𝑗 = min{𝑖 : 𝑡𝑖 > 0}
                                                       Î 𝑗 −1 ′                          
                     [𝒔, 𝒕, 𝑖=1 𝑌𝑖 ] → 𝑐 𝑗 [𝒔, dec𝒔 (𝒕), 𝑖=1 𝑌𝑖 × 𝑊 𝑗 × 𝑖=𝑗+1 𝑌𝑖′ ] 𝑟 𝑗 𝑉𝑗 ∈ 𝐺
                           Î𝑘                                          Î𝑘


             Fig. 8. VPG productions for parameterized lockstep . [𝑘] denotes the set {1, . . . , 𝑘 }.



D.3    Implementation of VPG Canonical Reductions via a Queue

Algorithm 1 Direct VPG reduction
Require: 𝐺𝑖 ’s are uniform, with disjoint nonterminals
  procedure Reduction(𝐺 1, . . . , 𝐺𝑛 )
     𝑉 ′ ←ÐStart-Symbols(𝐺 1 . start, . . . , 𝐺𝑛 . start)
     𝑃 ← 𝑖 𝐺𝑖 . productions
     𝑄 ← Queue(𝑉 ′ ), 𝑉 ← Set(𝑉 ′ ), 𝑅 ← Vpg(𝑉 ′ )
     while 𝑄 is nonempty do
         𝑋 ← Deqeue(𝑄)
         (𝑌1, . . . , 𝑌𝑚 ) ← Components(𝑋 )
         for all (𝑌1 → 𝛼 1 ), . . . , (𝑌𝑚 → 𝛼𝑚 ) in 𝑃 do
             rhs, splits ← Product(𝑋, ((𝑌1 → 𝛼 1 ), . . . , (𝑌𝑚 → 𝛼𝑚 )))
             Add the production 𝑋 → rhs to 𝑅
             Add the productions splits to 𝑃
             for all nonterminal 𝐵 in 𝛽 do
                    if 𝐵 ∉ 𝑉 then
                         Enqeue(𝑄, 𝐵)
                         Add(𝑉 , 𝐵)
     return 𝑅
40                                                                      Ruotong Cheng and Azadeh Farzan


   Algorithm 1 outlines the scheme for constructing a (canonical) reduction as a VPG that maintains
a queue 𝑄 of reachable symbols, and is parametric on the implementations of the procedures
Start-Symbols, Components, and Product which differ from one reduction to another. By main-
taining a queue 𝑄 of reachable symbols, Algorithm 1 only adds those productions that are truly
needed, making the construction efficient. We assume the input VPGs are uniform: for any produc-
tions 𝑋 → 𝛼 and 𝑋 → 𝛽, the right-hand sides 𝛼, 𝛽 both start with a call, both start with an internal,
or both are empty. Any VPG can be converted in linear time to an equivalent one that is uniform.
See also Algorithm 2 and 3.

Algorithm 2 Direct VPG reduction for nested_concat of two components
 1: function Start-Symbols(𝑉1st, 𝑉2st )
 2:     return {[𝑋 1, 𝑋 2 ] : 𝑋 1 ∈ 𝑉1st, 𝑋 2 ∈ 𝑉2st }

 3: function Components(𝑋 )
 4:    if 𝑋 is of the form [𝑌1, 𝑌2 ] then
 5:         return (𝑌1, 𝑌2 )
 6:     else
 7:         return (𝑋 )

 8: function Product(𝑋, 𝒑)
 9:    (𝑌1 → 𝛼 1 ), . . . , (𝑌𝑛 → 𝛼𝑛 ) ← 𝒑
10:    if n = 1 then
11:        return 𝛼 1, ∅
12:     else if 𝛼 1 is of the form 𝑐𝑍 1𝑟𝑊1 then
13:         return 𝑐 [𝑍 1, 𝑌2 ]𝑟𝑊1, ∅
14:     else if 𝛼 1 is of the form 𝑎𝑍 1 then
15:         return 𝑎[𝑍 1, 𝑌2 ], ∅
16:     else
17:         return 𝛼 2, ∅


E Benchmarks
Table 1, 2, 3, and 4 describe the benchmarks that we use for evaluating HyRec. Table 1 lists
the benchmarks adapted from the safe relational benchmarks from [48]; if a benchmark is about
recursive functions that are better understood by looking at the code, we list the name of the original
benchmark and the number 𝑘 when it is viewed as a 𝑘-property; these recursive functions only
call themselves and at most once. The Ackermann benchmark from [48] is discussed in Section 6.2.
Table 2 lists the benchmarks adapted from the iterative sequential benchmarks from [27].
   The benchmarks involve a variety of common functions on natural numbers and aggregate
functions on arrays. We make the following assumptions:
      • The implementation of mult recurses on the first parameter.
      • On arrays, the functions min, max, sum scan linearly from left to right unless otherwise
        specified. On binary trees simulated by arrays via a binary heap, they follow the structure
        of the heap.
      • For arrays and trees, pointwise operations (sum and scaling) are fused with aggregate
        functions. For example, sum(𝐴 + 2𝐵) is implemented as a single function that scans 𝐴, 𝐵
        simultaneously from left to right.
Products of Recursive Programs for Hypersafety Verification                                                  41


Algorithm 3 Direct VPG reduction for 𝒔-lockstep
 1: function Start-Symbols(𝑉1st, . . . , 𝑉𝑛st )
 2:      return {[𝒔, 0, 𝑿 ] : 𝑋 1 ∈ 𝑉1st, . . . , 𝑋𝑛 ∈ 𝑉𝑛st }

 3: function Components(𝑋 )
 4:    if 𝑋 is of the form [𝒔, 𝒕, 𝒀 ] then
 5:          return 𝒀
 6:      else
 7:          return (𝑋 )

 8: function Product(𝑋, 𝒑)
 9:    (𝑌1 → 𝛼 1 ), . . . , (𝑌𝑛 → 𝛼𝑛 ) ← 𝒑
10:    if 𝑛 = 1 then
11:        return 𝛼 1, ∅
12:      [𝒔, 𝒕, 𝒀 ] ← 𝑋
13:      if 𝑛 > 1 and there is 𝑖 such that 𝛼𝑖 = 𝜖 then
14:           drop the 𝑖-th component in 𝒔, 𝒕, 𝒀 , 𝒑
15:           return Product( [𝒔, 𝒕, 𝒀 ], 𝒑)
16:      else if there is a smallest 𝑖 such that 𝛼𝑖 is of the form 𝑎𝑍𝑖 then
17:           𝒀 ′ ← 𝒀 [𝑖 ↦→ 𝑍𝑖 ]
18:           return 𝑎[𝒔, 𝒕, 𝒀 ′ ], ∅
19:      else
20:           write 𝛼𝑖 = 𝑐𝑖 𝑍𝑖 𝑟𝑖𝑊𝑖 for each 𝑖
21:           𝒕 ′ ← (𝒕 − 1) mod 𝒔
22:           if 𝒕 = 0 then
23:                let 𝑈𝑖 = [𝑐𝑖 𝑍𝑖 𝑟𝑖 ] for each 𝑖
24:                𝒁 ′ ← 𝑼 [1 ↦→ 𝑍 1 ]
25:                return 𝑐 1 [𝒔, 𝒕 ′, 𝒁 ′ ]𝑟 1 [𝒔, 𝒕, 𝑾 ], {𝑈𝑖 → 𝑐𝑖 𝑍𝑖 𝑟𝑖 𝐸 : 𝑖 = 2, . . . , 𝑛} ∪ {𝐸 → 𝜖}
26:           else
27:                𝑖 ← min{ 𝑗 : 𝑡 𝑗 > 0}
28:                𝒁 ′ ← 𝒀 [𝑖 ↦→ 𝑍𝑖 ]
29:                return 𝑐𝑖 [𝒔, 𝒕 ′, 𝒁 ′ ]𝑟𝑖𝑊𝑖 , ∅


   For succinctness, we may omit ranges of variables that can be inferred from context, such as
𝑛 ≥ 0.
   We label benchmarks 1–30, 32, 41–57, 77–99 and 103 with (1, . . . , 1)-lockstep; 33–40, 58–73,
and 99 with 𝒔-lockstep where 𝒔 ≠ (1, . . . , 1); 31, 74–76, and 100–102 with (1, 1)-lockstep of one
component and the nested concatenation of the other two.
   Note that for benchmarks that are theoretically out of reach for our tool, we still label them with
(1, . . . , 1)-lockstep for a uniform treatment.
42                                                                  Ruotong Cheng and Azadeh Farzan


     No.   Description
      1    add-horn, a 2-property
      2    barthe, a 2-property
      3    div(𝑛 + 𝑑, 𝑑) = div(𝑛, 𝑑) + 1
      4    𝑑 < 𝑑 ′ =⇒ div(𝑛, 𝑑) ≥ div(𝑛, 𝑑 ′ )
      5    double-inc-loop, a 2-property
      6    𝑛𝑛 < 𝑛! for 𝑛 > 1
      7    𝑛 < 𝑛 ′ =⇒ fib(𝑛) ≤ fib(𝑛 ′ )
      8    fib(𝑛) = fib′ (𝑛 + 1), where the first term in fib′ is fib′ (1)
      9    fib is equivalent to fib′ , where the two recursive calls are swapped
     10    gcd(𝑛, 𝑚) = gcd(𝑚, 𝑛)
     11    inc-loop-1, a 2-property
     12    inc-loop-2, a 3-property
     13    inc-loop-5, a 6-property
     14    limit-1, a 2-property
     15    limit-2, a 2-property
     16    1 < 𝑛 < 𝑛 ′ =⇒ lucas(𝑛) ≤ lucas(𝑛 ′ )
     17    𝑛 > 2 =⇒ fib(𝑛) < lucas(𝑛)
     18    McCarthy91 is equivalent to McCarthy91′ , where the two branches are swapped
     19    𝑛 ≤ 𝑛 ′ =⇒ McCarthy91(𝑛) ≤ McCarthy91(𝑛 ′ )
     20    𝑞 = div(𝑛, 𝑑) =⇒ mult(𝑞, 𝑑) + mod(𝑛, 𝑑)
     21    mod(𝑛 + 𝑑, 𝑑) = mod(𝑛, 𝑑)
     22    𝑎 < 𝑎 ′, 𝑏 > 0 =⇒ mult(𝑎, 𝑏) < mult(𝑎 ′, 𝑏)
     23    0 < 𝑎 < 𝑎 ′, 0 < 𝑏 < 𝑏 ′ =⇒ mult(𝑎, 𝑏) < mult(𝑎 ′, 𝑏 ′ )
     24    the number of digits of 𝑛, i.e., ⌊log10 𝑛⌋ + 1, is monotone
     25    0 < 𝑥 < 𝑦, 𝑛 > 0 =⇒ 𝑥 𝑛 < 𝑦𝑛
     26    𝑥, 𝑦 > 0, 𝑛 > 0 =⇒ 𝑥 𝑛 + 𝑦𝑛 ≤ (𝑥 + 𝑦)𝑛
     27    sum-6, a 7-property
     28    twice-sum-1, a 2-property
                            Table 1. Benchmarks adapted from [48]
Products of Recursive Programs for Hypersafety Verification                                    43


         No.     Description
         29      array equality is symmetric
         30      array equality is transitive
         31      mult(𝑎, 𝑐) + mult(𝑏, 𝑐) = mult(𝑎 + 𝑏, 𝑐)
         32      mult(𝑎, 𝑏) + mult(𝑎, 𝑐) = mult(𝑎, 𝑏 + 𝑐)
         33      equivalence before and after unrolling a loop twice
         34      equivalence before and after unrolling a loop three times
         35      equivalence before and after unrolling a loop four times
         36      equivalence before and after unrolling a loop five times
         37      equivalence before and after unrolling a loop twice, with cleaning up
         38      equivalence before and after unrolling a loop three times, with cleaning up
         39      equivalence before and after unrolling a loop four times, with cleaning up
         40      equivalence before and after unrolling a loop five times, with cleaning up
         41      the lexicographic order comparator is symmetric
         42      a variation of the lexicographic order comparator is symmetric
         43      the lexicographic order comparator respects equality
         44      a variation of the lexicographic order comparator respects equality
         45      the lexicographic order is transitive
             Table 2. Benchmarks adapted from the iterative sequential benchmarks from [27]
44                                                                      Ruotong Cheng and Azadeh Farzan


     No.   Description
     46    the function inc that recursively sums up 𝑛 ones is injective
     47    𝑎 > 0 ∧ 𝑏 < 𝑏 ′ =⇒ mult(𝑎, 𝑏) < mult(𝑎, 𝑏 ′ )
     48    div(𝑛, 𝑑) = div(2𝑛, 2𝑑)
     49    𝑛 ≤ 𝑛 ′ =⇒ div(𝑛, 𝑑) ≤ div(𝑛 ′, 𝑑)
     50    𝑛 ≤ 𝑛 ′, 𝑑 ≥ 𝑑 ′ =⇒ div(𝑛, 𝑑) ≤ div(𝑛 ′, 𝑑 ′ )
     51    2 mod(𝑛, 𝑑) = mod(2𝑛, 2𝑑)
     52    (1 + 2) + · · · + ((2𝑛 − 1) + 2𝑛) = (2 + 4 + · · · + 2𝑛) + (1 + 3 + · · · + (2𝑛 − 1))
     53    𝑚 < 𝑛 =⇒ 𝑚! ≤ 𝑛!
     54    𝑎 > 1, 0 < 𝑚 < 𝑛 =⇒ 𝑎𝑚 < 𝑎𝑛
     55    fib(𝑛) = 3 fib(𝑛 − 3) + 2 fib(𝑛 − 4) for 𝑛 > 3
     56    the Tribonacci sequence is monotone
     57    the Tetranacci sequence is monotone
     58    2 inc(𝑛) = inc(2𝑛)
     59    inc(2𝑛) = 2 inc(𝑛)
     60    2 mult(𝑎, 𝑏) = mult(2𝑎, 𝑏)
     61    mult(2𝑎, 𝑏) = 2 mult(𝑎, 𝑏)
     62    3 mult(𝑎, 𝑏) = mult(3𝑎, 𝑏)
     63    mult(3𝑎, 𝑏) = 3 mult(𝑎, 𝑏)
     64    3 mult(2𝑎, 𝑏) = 2 mult(3𝑎, 𝑏)
     65    2 mult(3𝑎, 𝑏) = 3 mult(2𝑎, 𝑏)
     66    𝑑 | 𝑛 =⇒ 𝑑 | 2𝑛
     67    𝑑 | 2𝑛 ⇐= 𝑑 | 𝑛
     68    𝑑 | 𝑛 =⇒ 𝑑 | 3𝑛
     69    𝑑 | 3𝑛 ⇐= 𝑑 | 𝑛
     70    2 div(𝑛, 𝑑) ≤ div(2𝑛, 𝑑)
     71    div(2𝑛, 𝑑) ≥ 2 div(𝑛, 𝑑)
     72    3 div(𝑛, 𝑑) ≤ div(3𝑛, 𝑑)
     73    div(3𝑛, 𝑑) ≥ 3 div(𝑛, 𝑑)
     74    div(𝑛, 𝑑) + div(𝑛 ′, 𝑑) ≤ div(𝑛 + 𝑛 ′, 𝑑)
     75    𝑑 | 𝑛, 𝑑 | 𝑛 ′ =⇒ 𝑑 | (𝑛 + 𝑛 ′ )
     76    mod(𝑛, 𝑑) = 0, mod(𝑛 ′, 𝑑) = 0 =⇒ mod(𝑛 + 𝑛 ′, 𝑑) = 0
     77    mult(𝑎, 𝑏) = mult(𝑏, 𝑎)
                              Table 3. More arithmetic benchmarks
Products of Recursive Programs for Hypersafety Verification                                          45


   No.    Description
    78    sum(𝐴) + sum(𝐵) = sum(𝐴 + 𝐵)
    79    the lexicographic order is antisymmetric
    80    min(𝐴 + 𝐵) ≥ min(𝐴) + min(𝐵)
    81    min(𝐴) ≤ max(𝐴) for nonempty array 𝐴
    82    2 sum(𝐴) = sum(𝐴)
    83    2 sum(𝐴) + sum(𝐵) = sum(2 𝐴 + 𝐵)
    84    pointwise ≤ on arrays is transitive
    85    pointwise ≤ on arrays is reflexive
    86    pointwise ≤ on arrays is antisymmetric
    87    𝐴 ≤ 𝐵 =⇒ 2𝐴 ≤ 2𝐵
    88    𝐴 ≤ 𝐵 =⇒ 𝐴 + 𝐶 ≤ 𝐴 + 𝐶
    89    max(𝐴) < min(𝐵) =⇒ max(𝐵) < min(𝐶) =⇒ min(𝐴) < min(𝐶)
    90    max(𝐴) < min(𝐵) =⇒ max(𝐵) < min(𝐶) =⇒ min(𝐴) < max(𝐶)
    91    min(𝑇 ) ≤ max(𝑇 ) for tree 𝑇
    92    min(𝑇 ) ≤ max(𝑇 ) for tree 𝑇 , another implementation of min, max
    93    max(𝑇 ) < min(𝑇 ′ ) =⇒ min(𝑇 ) < min(𝑇 ′ )
    94    𝑇 ≤ 𝑇 ′ =⇒ 2𝑇 ≤ 2𝑇 ′ , where 𝑇 ,𝑇 ′ has the same shape and ≤ is pointwise
    95    sum(𝑇 ) + sum(𝑇 ′ ) = sum(𝑇 + 𝑇 ′ )
    96    min(𝐴) ≤ max(𝐴), where min, max recurse on the two halves of 𝐴
    97    max(𝐴) < min(𝐵) =⇒ min(𝐴) < min(𝐵), where min, max recurse on the two halves
    98    min(𝑇 ) + min(𝑇 ′ ) ≤ min(𝑇 + 𝑇 ′ )
    99    sum up two consecutive elements at a time = sum up one element at a time
   100    min(𝐴[𝑖..𝑘]) = min(min(𝐴[𝑖..𝑗]), min(𝐴[ 𝑗 ..𝑘]))
   101    max(𝐴[𝑖..𝑘]) = max(max(𝐴[𝑖..𝑗]), max(𝐴[ 𝑗 ..𝑘]))
   102    sum(𝐴[𝑖..𝑘]) = sum(𝐴[𝑖..𝑗]) + sum(𝐴[ 𝑗 ..𝑘])
   103    𝑖 < 𝑖 ′ < 𝑗 ′ < 𝑖 =⇒ sum(𝐴[𝑖 ′ ..𝑗 ′ ]) < sum(𝐴[𝑖..𝑗]) if every element of 𝐴 is positive
                                        Table 4. More array benchmarks
