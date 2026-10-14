        Formally Verified Linear-Time Invertible
                         Lexing

                     Samuel Chassot(B)         and Viktor Kunčak

                            EPFL, Lausanne, Switzerland
                      {samuel.chassot,viktor.kuncak}@epfl.ch



       Abstract. We present ZipLex, a veriﬁed framework for invertible
       linear-time lexical analysis following the longest match (maximal munch)
       semantics. Unlike past veriﬁed lexers that focus only on satisfying the
       semantics of regular expressions and the longest match property, ZipLex
       also guarantees that lexing and printing are mutual inverses. Thanks to
       veriﬁed memoization, it also ensures that the lexical analysis of a string
       is linear in the size of the string. Our design and implementation rely on
       two sets of ideas: (1) a new abstraction of token sequences that captures
       the separability of tokens in a sequence while supporting their eﬃcient
       manipulation, and (2) a combination of veriﬁed data structures and opti-
       mizations, including Huet’s zippers and memoization with a standalone
       veriﬁed imperative hash table. Our hash table oﬀers competitive perfor-
       mance as shown by our evaluation. We implemented and veriﬁed ZipLex
       using the Stainless deductive veriﬁer for Scala. Our evaluation demon-
       strates that ZipLex supports realistic applications such as JSON pro-
       cessing and lexers of programming languages, and behaves linearly even
       in cases that make ﬂex-style approaches quadratic. ZipLex is two orders
       of magnitude faster than Verbatim++, showing that veriﬁed invertibility
       and linear-time algorithms can be developed without prohibitive cost.
       Compared to Coqlex, ZipLex also oﬀers linear (instead of quadratic)
       time lexing, and is the ﬁrst lexer that comes with invertibility proofs for
       printing token sequences.


       Keywords: formal veriﬁcation · lexical analyzer · Stainless · regular
       expression · derivative · zipper · memoization · invertibility


1    Introduction
Lexical analysis, or lexing, is the ﬁrst step in most parsing pipelines, including
compilers and data analysis tools. A lexical analyzer (lexer ) transforms a raw
sequence of characters into a sequence of structured tokens that feeds into sub-
sequent phases. Given their critical role, lexers should satisfy strong correctness
guarantees. Yet lexers often remain trusted components: even in the CompCert
veriﬁed C compiler [21], the lexer is part of the trusted computing base and
is not itself veriﬁed [20]. Veriﬁed lexer generators such as Coqlex [27] and the
pioneering Verbatim frameworks [14,15] demonstrate that formal veriﬁcation of
 c The Author(s) 2026
E. Darulova et al. (Eds.): CAV 2026, LNCS 16683, pp. 141–164, 2026.
https://doi.org/10.1007/978-3-032-32526-6_7
142     S. Chassot and V. Kunčak

core lexing properties is feasible, but challenges remain in performance, as well
as in supporting use cases that involve printing tokens back to text.
    In many applications, lexers are used together with printing, for instance
when manipulating syntax trees in IDE refactoring engines, program synthe-
sis tools, or compiler pipelines. In such settings, it is essential that printing a
sequence of tokens produces a string whose subsequent lexical analysis yields
back the same tokens. Without this guarantee, information may be silently lost.
    We refer to this property as invertibility. Invertible lexing ensures that alter-
nating lexing and printing preserves information exactly, and can be seen as a
prerequisite for fully invertible parsing and pretty-printing frameworks. While
researchers studied invertible parsing [31], invertibility has not been investigated
for lexical analysis, where longest match makes common parsing techniques inad-
equate. Existing frameworks that support invertible parsing, such as Grammat-
ical Frameworks [30], do not enforce invertibility of user-deﬁned lexers.
    We present ZipLex, a framework for veriﬁed and eﬃcient invertible lex-
ing. ZipLex provides a fully veriﬁed lexer and regular expression engine based
on Brzozowski’s derivatives [3,28]. To reason about safe printing of token
sequences, we develop a simple and general abstraction for reasoning about R-
paths (sequences constrained by a given binary relation). We use this abstraction
to characterize sequences of tokens that can be printed and re-lexed without
merging adjacent tokens. Our predicates are preserved under slicing and con-
catenation, enabling eﬃcient manipulation of token sequences while maintaining
invertibility.
    To achieve acceptable performance, ZipLex incorporates veriﬁed optimiza-
tions, including memoization following Reps [32], yielding linear-time lexing in
the length of the input string, and the use of Huet’s zippers [18] and regular
expression derivatives for regular expression matching. Memoization makes use
of a veriﬁed and reusable memoization framework including a standalone veriﬁed
mutable hash table, building on top of previous work [7], which oﬀers competi-
tive performance as shown by our evaluation. We implemented all components
in Scala and veriﬁed them using Stainless [17]. The veriﬁed code remains com-
patible with the standard Scala compilation and build toolchain.
    We evaluate ZipLex on several scenarios, including a JSON lexer and a JSON
object-sorting application built on top of it. Our goal is to support high-ﬁdelity
applications that require strong guarantees about correctness and reversibility,
such as fully veriﬁed compilers and veriﬁed communication protocols.
Illustration of the challenge Mentioned as early as [6], the maximal munch
principle, or longest match semantics, is the classical correctness criterion for
lexers. It states that each produced token should be the longest possible at a given
position, given the input string and the token deﬁnitions. While suﬃcient for
correct tokenization in isolation, longest match alone is insuﬃcient to guarantee
correct interaction between lexing and printing.
    Consider the Scala-like statement val x = 1, whose token sequence is
 val       x      =      1 . Suppose now that a refactoring tool removes whites-
pace tokens around = , yielding val              x = 1 . Printing this sequence
                           Formally Veriﬁed Linear-Time Invertible Lexing    143

produces val x=1, which is lexed back into the same sequence of tokens,
up to whitespace, so no essential information is lost. In contrast, consider
instead the statement val x_ = 1. Removing whitespace around the equality pro-
duces val       x_ = 1 , which prints as val x_=1. Lexing this string yields
 val     x_= 1 , because x_= is a valid identiﬁer (e.g., in Scala) and is rec-
ognized by longest match. The printed output therefore does not lex back to
the original token sequence, breaking our expectations. Maintaining all whites-
pace tokens would avoid this issue, but this is incompatible with pretty printers
and refactoring tools whose purpose is precisely to modify whitespace according
to formatting conventions. The same problem can arise when reordering sub-
sequences, for example, moving function deﬁnitions around in a source ﬁle.
    The central problem we address is therefore: How can we support printing
and lexing while formally guaranteeing that no information is lost? To formalize
this problem, we deﬁne separable tokens and invertibility.
Invertibility as a Design Goal. We say that a lexer is invertible if both:

              ∀ ts. lex(print(ts)) = ts and
              .                               ∀s. print(lex(s)) = s

Note that if .∀s. print(lex(s)) = s then .lex(print(ts)) = ts whenever .∃s. ts =
lex(s). We deﬁne a separability condition, .sep, as any predicate on token
sequences .ts such that .∀ ts. sep(ts) =⇒ lex(print(ts)) = ts. Our goal is to
design separability conditions fulﬁlling two competing requirements: (1) they
are ﬂexible enough for practical use and (2) they can be checked and preserved
eﬃciently when token sequences are transformed in user code.
Contributions Our contributions include:
1. a deﬁnition of separability .sep(ts) and eﬃcient mechanisms to enforce it;
2. the design of a lexing framework that implements: (i) invertible printing (ii)
   regular-expression-based token deﬁnitions (iii) longest match semantics, and
   (iv) linear-time lexing thanks to memoization;
3. a library of eﬃcient veriﬁed data structures including a tree-based structure
   for sequences using immutable arrays with a zero-copy slicing operation in the
   leaves, a mutable hash table for arbitrary keys based on veriﬁed LongMap [7],
   and a reusable veriﬁed memoization framework.
4. the concrete realization and deductive veriﬁcation of a veriﬁed lexer, ZipLex,
   and its performance evaluation showing its eﬃciency, available as a Docker
   image [9], and in Bolts repository [1] under lexers/regex.

1.1   Related Work
We are aware of no existing work on lexers with veriﬁed invertibility; we survey
works that verify weaker or related properties.
Verified Lexing. Several veriﬁed lexer generators have been proposed.
Coqlex [27] provides a veriﬁed lexer generator in Rocq with a user experience
close to OCamllex. It relies on Brzozowski’s derivatives and supports additional
constructs such as negation and diﬀerence, but is restricted to ASCII strings and
144     S. Chassot and V. Kunčak

depends on an unveriﬁed code-generation step. Verbatim [14], later extended as
Verbatim++ [15], also uses derivatives, with Verbatim++ introducing a translation
to DFAs and memoization to improve performance, yielding a worst-case com-
plexity of .O(n log n). Our experiments in Sect. 8 show the performance advan-
tages of our lexer, ZipLex.
    Nipkow [24] presents an early veriﬁed lexer in Isabelle/HOL supporting arbi-
trary alphabets, based on an NFA-style algorithm that is not directly executable.
In contrast, our technique avoids automata construction altogether, supports
arbitrary alphabets, and achieves linear-time lexing through a veriﬁed variant of
memoization [32], without an upfront preprocessing overhead.
Regular Expressions and Grammars. Brzozowski’s derivatives [3] have
been extensively studied as a basis for regular expression matching. Owens
et al. [28] re-established derivatives as a practical technique, and later work
demonstrated that derivative-based engines can achieve state-of-the-art perfor-
mance [35], albeit without formal veriﬁcation.
    Edelmann’s thesis [12] explores derivatives for LL(1) parsing [13] and lex-
ing, introducing an optimization based on Huet’s zippers [18]. While that work
provides high-level proofs in Rocq, our eﬀort with ZipLex bridges the gap to
implementation, oﬀering a veriﬁed executable zipper-based matching engine. The
implementation of zipper-based regular expression representation and derivative
computation in Edelmann’s work [13] served as a starting point for ZipLex.
We did not make use of the associated Rocq proofs, though they provide useful
insights. Derivatives and zippers have also been used to parse grammars [2,11],
but without end-to-end formal veriﬁcation. Chattopadhyay et al. [10] verify reg-
ular expression matching with lookarounds in Rocq, and De Santo et al. [33]
formalize JavaScript regular expression semantics. These works target richer
regex features than ZipLex but do not aim for executable longest-match lexing.
Invertibility in Parsing and Serialization. Invertible parsing and pretty
printing have been studied extensively, notably by Rendel et al. [31], who enforce
invertibility by restricting transformations to isomorphisms but without instanti-
ating it to lexical analysis. A related problem is serialization and deserialization;
Bucev et al. [4] present a proof-producing ASN.1/SCC compiler in Scala, where,
given a data format description, serialization and deserialization functions are
generated together with proofs of invertibility accepted by Stainless. Lossless
image compression also has a natural speciﬁcation using mutually inverse func-
tions [5].

2     Usage Example and ZipLex API
To demonstrate the veriﬁed abstraction, we present ZipLex using a JSON lexer
and a simple application that sorts the objects within a JSON array (Fig. 1).
The implementation is included in the artifact, along with additional example
lexers including one for a Python subset and one for Amy, a teaching language.
JSON Application. The application proceeds as follows. It lexes the input
JSON ﬁle, and wraps the resulting token sequence in a PrintableTokens instance,
                            Formally Veriﬁed Linear-Time Invertible Lexing     145




Fig. 1. JSON sorting application. Outer gray boxes are PrintableTokens instances.
(Color ﬁgure online)


establishing the separability invariant. The application then shallowly parses the
sequence to identify JSON objects and extracts their "id" ﬁelds, yielding object
slices as PrintableTokens instances. It then sorts these objects by the extracted
identiﬁers and concatenates the resulting PrintableTokens instances to form a
single PrintableTokens instance. Finally, the application prints back the object
sequence to a character stream.
    All token-sequence manipulations are performed through PrintableTokens,
which preserves separability under slicing and concatenation, requiring only a
constant-time runtime check at concatenation boundaries. By verifying this pro-
gram in Stainless, we statically guarantee that printing the ﬁnal token sequence
and lexing it again yields the same tokens.
Lexer Interface and Usage. ZipLex performs lexical analysis using data
structures generated on-the-ﬂy, without a code-generation phase used in, e.g.,
Ocamllex [25]. Users deﬁne rules by associating regular expressions with token
constructors, and invoke the main .lex function with a rule list and an input
sequence. The result is a sequence of tokens and a possibly untokenized suﬃx,
corresponding to the uniform tokenization problem [22]. At each step, .lex selects
the longest preﬁx matched by any rule, breaking ties by rule order.
    The input alphabet is left abstract: ZipLex operates over sequences of an
arbitrary type, allowing users to target, e.g., ASCII, UTF-8, or binary formats.
To support invertibility, rules associate regular expressions with injective trans-
formations from substrings to semantic values (to build semantic tokens [15]),
together with their inverses. This guarantees that printing a token reproduces
exactly the substring it was created from. To be able to reason about invertibil-
ity, ZipLex provides functions to print sequences of tokens to strings, the main
one being .print. We defer the formal treatment of invertibility to Sect. 3.
Longest Match Specification. In addition to invertibility, the correctness
criterion for ZipLex is the maximal munch principle [6], or longest match
semantics. For each produced token, no rule matches a strictly longer preﬁx
of the remaining input, and no higher-priority rule matches an equally long one.
ZipLex veriﬁes this property in Stainless, which, by induction on the input,
establishes longest match semantics for the entire token sequence.
146     S. Chassot and V. Kunčak

3     Invertibility
This section formalizes invertibility of lexing. We diﬀerentiate the two directions:

– .print(lex(s)) = s, implying the injectivity of .lex;
– .lex(print(ts)) = ts, implying the injectivity of .print.
We explore these two directions separately in Sect. 3.1 and Sect. 3.2, respectively.
Our notation uses 0-based indexing .s(i) for sequences, and (following Scala) .s ++ t
for concatenation. For readability, we use .[a-z] and .[0-9] for unions of characters,
and .r+ for .r · r∗ .

3.1    Ensuring .print(lex(s)) = s

 Semantic Values and Injection. To achieve invertibility, we ﬁrst ensure that
 each token is printed as the same string that was consumed to produce it. This
 is trivial when tokens store substrings directly, but in practice tokens often store
 semantic values [15]. A transformation from strings to semantic values is suﬃ-
 cient to construct tokens, but insuﬃcient to print them back to the same strings.
 For this reason, ZipLex requires each rule to contain an injective transforma-
 tion .transform together with a corresponding .charsOf function and a proof that
.∀s. charsOf(transform(s)) = s. Surjectivity is not needed because tokens only
 contain values created by .transform. Users are free to pick types and transfor-
 mations that ﬁt subsequent token manipulation. If the desired transformation is
 not injective (or if proving injectivity is inconvenient), one can always fall back
 on .transform(s) = (v, s) with .charsOf((v, s)) = s.
     Our approach uses standard assume-guarantee reasoning for sequential pro-
 grams with preconditions and postconditions to require that token transforma-
 tions are injective as above. Stainless thus formally makes sure that clients of
 ZipLex establish injectivity to be able to use the lexer. To streamline these
 proofs for library clients, ZipLex provides an Injection construct that captures
 the semi-inverse relation between .transform and .charsOf. The deﬁnition of injec-
 tion relies on support of Stainless for explicitly instantiated quantiﬁers in speci-
 ﬁcations. These proofs are very localized and, in our experience, easy.
     From the required injectivity property, ZipLex proves .print(lex(s)) = s by
 induction on .s: at each step, injectivity ensures that printing the ﬁrst token
 reconstructs the consumed preﬁx, and the induction hypothesis concludes the
 proof on the suﬃx.

3.2    Towards .lex(print(ts)) = ts

Unlike the previous case, .lex(print(ts)) = ts is not true in general. For example,
with a rule based on .[a-z]+ , printing a list containing two tokens, foo and bar
yields ."foobar", which is tokenized as foobar . More generally, collapse may
depend on more than two adjacent tokens: with token rules based on .a∗ , .b∗ , and
                               Formally Veriﬁed Linear-Time Invertible Lexing     147

abc, the sequence a b can be printed safely, while a b c cannot. We call a
.
token sequence separable if it satisﬁes .lex(print(ts)) = ts.
    We consider two approaches to ensure separability: (1) a special class of sep-
arator tokens using a disjoint set of characters from other classes, and (2) an
approach based on R-Path conditions. Although usable when designing serializa-
tion formats, the separator-token approach is restrictive for lexing of program-
ming languages: for example, whitespaces appear naturally as separators but
also appear in strings and comments. We therefore focus on the more expressive
approach, (2).

3.3   R-Path Predicates
 As a simple basic abstraction, we introduce a family of predicates on sequences
 where a binary relation must hold for each pair of consecutive elements. We call
 such predicates R-Path conditions. An example of an R-Path condition is the
 sorted predicate where .R is a total order. More generally .R-paths are contiguous
 fragments of traces of a transition system given by the relation .R. For a relation
.R, we thus deﬁne .pR (s) as .∀i. 0 ≤ i < |s| − 1 =⇒ R(si , si+1 ).
      Checking an R-Path requires a number of evaluations of .R linear in the
 length of the sequence. When working with a deductive veriﬁer, R-Paths are
 convenient to maintain as invariants: slices of R-Paths are R-Paths, and con-
 catenation requires only a check at the boundary (where .n1 is the length of
.s1 ):


                 .pR (s) =⇒ pR (s.slice(i, j)), for 0 ≤ i ≤ j < |s|,

          pR (s1 ++ s2 ) ⇐⇒ pR (s1 ) ∧ R(s1 (n1 − 1), s2 (0)) ∧ pR (s2 ),

3.4   R-Paths That Ensure Invertibility
We deﬁne printable sequences as R-Paths for a particular relation .R. The intu-
ition is that tokens .t1 and .t2 are separable iﬀ the ﬁrst character of .t2 is already
suﬃcient to ensure that .t1 is the longest token that can match in the printed
string (regardless of any subsequent tokens following .t2 ). We thus take .R to be
the relation .sep(t1 , t2 ):

                 sep(t1 , t2 ) := ¬
                 .                          ri .preﬁxMatch(t1 ++ t2 (0)),
                                      i∈m

where .ri is the regular expression of rule .i. For notational simplicity, we view
tokens as strings. The predicate .     i∈m ri .preﬁxMatch(s) means that some
                                                                 m
 rule matches a string with preﬁx .s. Equivalently, .s ∈ k=1 preﬁxSet(rk ) where
.preﬁxSet(r) = { s | ∃s . (s ++ s ) ∈ L(r) }.

     We then deﬁne separability for a length-.n token sequence by the R-Path
 condition induced by .sep:

             sep(t1 , t2 , . . . , tn ) ⇐⇒ ∀i. 1 ≤ i < n =⇒ sep(ti , ti+1 ).
             .
148     S. Chassot and V. Kunčak

     The relation .sep(t1 , t2 ) is local with respect to tokens but not rules: it must
 consider all regular expressions appearing the lexer’s set of the rules. A relation
 local to both tokens and their producing rules cannot be suﬃcient: given a
 sequence .ts satisfying such a hypothetical local predicate, one can add a new rule
 matching exactly .print(ts), in which case lexing .print(ts) yields a single token,
 while the local predicate remains satisﬁed.
     We illustrate .sep on an example. Consider .r1 = [a-z]+ and .r2 = [0-9]+ . For
 t1 = foo and t2 = bar , the preﬁx ."foob" lies in the preﬁx set of .[a-z]+ , so
.sep(t1 , t2 ) does not hold. For t1 = foo and t2 = 123 , "foo1" is in no rule preﬁx

 set, so the tokens are separable. Because no rule matches any string starting with
."foo1", extending the sequence on the right cannot create a match either.
     The function .preﬁxMatch follows the same algorithm as the regular expression
 matching function .matchR (described in Sect. 4.1), but when reaching the end of
 the preﬁx it checks that the resulting language is non-empty rather than nullable.
 This enables .preﬁxMatch to take advantage of the memoization of derivatives,
 using the same cache (Sect. 6). We evaluate the cost of checking the R-Path .sep
 in Sect. 8.
     We provide an abstract type .PrintableTokens that maintains the R-Path
 invariant for .R = sep on a given sequence. The invariant is computed once at
 instantiation; slicing preserves it, and concatenation requires only a boundary
 check .sep(tlast , tfirst ).
     Our deﬁnition is sound: it implies separability. At the same time, it is eﬃcient
 to check. Whereas the condition could be made more permissive by taking more
 characters into account, our condition already provides most of the practical
 beneﬁts at a low computational cost. A maximally permissive predicate corre-
 sponds to printing, re-lexing and checking the equality; it is correct but, from a
 practical point of view, unnecessarily ineﬃcient when manipulating long token
 sequences.


3.5   R-Path vs Separator Tokens

We also prove that the token sequence implicitly produced by printing while
inserting separator tokens always satisﬁes the R-Path condition .sep(t1 , . . . , tn ).
This shows that the R-Path predicate is more general than interleaving sepa-
rator tokens, and that interleaving provides a simple way to obtain a separable
sequence without any runtime checks when a separator token is available.


4     Regular Expressions Engine
This section presents the fully veriﬁed regular expression matching engine under-
lying ZipLex. We ﬁrst describe a reference implementation based on naïve Brzo-
zowski’s derivatives with straightforward syntax trees for regular expressions. We
then detail our development of the optimized variant using Huet’s zippers as the
regular expression representation.
                             Formally Veriﬁed Linear-Time Invertible Lexing       149

4.1   Definition and Implementation
 Regular expressions are parameterized by an arbitrary alphabet type and include
 the usual constructs: empty string, empty language, single-character matching,
 union, concat, and Kleene star. In addition to these constructors, our regular
 expressions oﬀer a character-set primitive with an explicitly instantiated set
 of alphabet elements. This allows to describe sets without instantiating and
 deriving deep unions. Strings are sequences of alphabet elements.
     The matching function .matchR(r, s) decides membership of .s in the lan-
 guage of .r using Brzozowski’s derivatives [3,35]. The engine also provides
.ﬁndLongestMatch, which computes the longest preﬁx of an input string matched
 by a regular expression. Rather than testing all preﬁxes, this function traverses
 the input once, computing at most one derivative per character and stopping
 early when the derived expression denotes the empty language. If no preﬁx
 matches, the empty string is returned. Lexing rules are restricted to non-nullable
 expressions, so the empty string is never a token.
 Specification. We encode the standard semantic speciﬁcation of regular expres-
 sion matching as a ghost function .matchRSpec and prove: .∀r, s. matchR(r, s) =
 matchRSpec(r, s).

4.2   Zipper Optimization
While conceptually simple, naïve derivative-based matching suﬀers from expres-
sion blow-up and redundant computations. To address this, we implement and
verify an optimization based on an instance of Huet’s zippers [18], following the
approach of Edelmann [12, Chapter 2]. Zippers provide an alternative represen-
tation of regular expressions as sets of contexts, where each context is a sequence
of regular expressions (Fig. 2). Intuitively, contexts represent concatenations of
their regular expressions, while zippers represent unions of such contexts. This
representation yields a more eﬃcient derivative algorithm and is particularly well
suited to memoization: in contrast to naive derivatives for regular expressions,
the set of reachable zippers during derivation is provably ﬁnite [12, Chapter 2],
substantially reducing cache misses and recovering key properties of on-the-ﬂy
transformation to a ﬁnite automaton.




Fig. 2. ADT deﬁnitions for zipper-based representation of regular expressions and sig-
natures of focus and unfocus to transform regular expressions into zippers and back.



   Figure 2 shows the zipper deﬁnition and the interfaces for converting between
regular expressions and zippers. The zipper matching function .matchZ follows
150     S. Chassot and V. Kunčak

the same structure as .matchR, computing derivatives character by character and
checking nullability.
Specification. Zipper-based matching is a drop-in replacement for regular
expression matching. It satisﬁes .unfocus(z) = r             =⇒     matchR(r, s) =
matchZ(z, s) for all .s, r, z. This theorem is fully veriﬁed using Stainless.


5     Towards Acceptable Performance

In this section, we describe the optimizations required to obtain acceptable per-
formance while maintaining veriﬁability.
    First, we implement tail-recursive versions of all functions recursing on input
strings that are executed at runtime. Although recursive functions make induc-
tive proofs and executable code similar and therefore easier to write, they lead
to high stack usage and potential stack-overﬂow crashes on the Java Virtual
Machine. While this does not necessarily impact performance in a perceptible
way, it negatively impacts usability, as the program crashes for large inputs. In
our experiments, this issue arises mainly with the size operation on List, with the
main functions of the lexer, .lex and .print, and with the .ﬁndLongestMatch func-
tion (see Sect. 6 for in-depth explanations). To address this problem, we write
tail-recursive implementations and prove their equivalence to the original ver-
sions. This allows us to preserve the existing proofs while replacing the runtime
implementations, using equivalence theorems to bridge the gap between proofs
and execution.
    Second, we replace List by a more eﬃcient and fully veriﬁed data structure
named BalanceConc to represent sequences of alphabet elements and tokens, in
all code executed at runtime. This structure is speciﬁed by a List and represents
sequences as balanced binary trees with immutable arrays of up to parameter .N
elements in the leaves, where .N is a compile-time constant. Proofs are agnostic
of .N so changing its value does not aﬀect the correctness proofs. In this work,
we use .N = 512. It is inspired by the Balance Conc implementation of [23]. For
speciﬁcation and proofs, however, we continue to rely on List. Although List does
not provide satisfactory runtime performance, it is well suited for veriﬁcation: the
Stainless library provides many lemmas and properties for lists, and the SMT
theory of algebraic data types enables eﬀective reasoning about them within
Stainless. Using BalanceConc for execution and List for speciﬁcation thus yields
a practical combination of eﬃciency and veriﬁability.
    Third, we implement memoization to improve performance, as described in
Sect. 6, both for zipper derivatives and for inner functions of the lexer.


6     Verified Memoization
In this section, we present a fully veriﬁed and eﬃcient memoization framework.
The framework is backed by a veriﬁed hash table we developed based on the
work of Chassot et al. [7]. The framework is reusable, thanks to a small set of
                             Formally Veriﬁed Linear-Time Invertible Lexing       151

lemmas that simplify the implementation and veriﬁcation of memoization caches.
We then show how we apply this framework to ZipLex to improve performance
without sacriﬁcing correctness.
    As shown by Reps [32], longest match lexical analysis can be performed in
linear time in the size of the input string using memoization. However, memo-
ization is challenging in a formally veriﬁed setting: it requires a map-like data
structure that is both eﬃcient and fully veriﬁed. In proof assistants such as
Rocq, previous works including Verbatim++ [15] and a veriﬁed implementation
of orthologic proof search [16] rely on standard-library maps, such as ﬁnite maps
based on lists of pairs1 or more eﬃcient (but at best logarithmic) AVL-tree-based
maps2 . Even with such data structures, adding memoization typically requires
threading caches through functions in a monadic style, including in proofs, which
signiﬁcantly increases veriﬁcation eﬀort and limits reusability.
    To address these issues, we build on the veriﬁed mutable hash table of Chassot
et al. [7], which veriﬁes Scala’s LongMap3 , an optimized hash table indexed by 64-
bit integers. This allows us to obtain eﬃcient memoization without re-verifying
low-level hash-table machinery.


6.1   Memoization Framework

We ﬁrst deﬁne a veriﬁed hash table with arbitrary-type keys, HashMap[K,V],
implemented as a decorator of the veriﬁed LongMap. Values stored in the
LongMap are linked lists of key-value pairs, yielding an instance of type
LongMap[List[(K,V)]]. We use the hash of the keys to index in the LongMap.
Building on top of the already veriﬁed LongMap allows us to support generic
keys at moderate cost without sacriﬁcing too much in eﬃciency, provided that
hash collisions remain reasonable, as the LongMap is one of the most eﬃcient
implementations of a hash table in the Scala standard library. This design yields
an implementation and veriﬁcation eﬀort of approximately 1600 additional lines
of code, compared to nearly 8000 lines reported by Chassot et al. [7]. We also
implement and verify a functional executable speciﬁcation for the HashMap[K,V].
    To support memoization, we provide a small set of lemmas that capture
the invariant of a memoization cache: when memoizing a function .f : A → B
using a hash table .h, then .∀(k, v) ∈ h. v = f (k). The lemmas show that the
invariant is preserved by cache operations such as insertion. Notably, inserting a
pair .(k , f (k )) into a cache that already satisﬁes the invariant yields a new state
of the cache that continues to satisﬁes the invariant.
    Using these lemmas, implementing a memoization cache requires only a few
tens of lines of code, largely consisting of forwarding operations to the under-
lying hash table and applying the invariant-preservation lemmas. The mutable
nature of the cache avoids monadic threading: the cache can be passed through

1
  https://github.com/rocq-prover/stdlib/blob/master/theories/FSets/FMapList.v.
2
  https://github.com/rocq-prover/stdlib/blob/master/theories/FSets/FMapAVL.v.
3
  https://github.com/scala/scala/blob/2.13.x/src/library/scala/collection/mutable/
  LongMap.scala.
152     S. Chassot and V. Kunčak

the program directly, and call sites simply check for cached values, computing
and inserting results on cache misses. We view this as evidence of a usability
advantage of a veriﬁer that supports mutation.


6.2   Applying Memoization to ZipLex

 The memoization framework is general and applies to any pure function. In
 ZipLex, we use it to memoize the two zipper-derivative functions, derivStepUpZ,
 derivStepDownZ, and the function computing the longest matching preﬁx.
 Zipper Derivatives. Memoizing zipper-derivative functions follows the stan-
 dard pattern described above: derivative results are cached and reused across
 calls, substantially reducing repeated computations.
 Longest Match Prefix. Memoizing the longest-match computation requires
 additional care. The naive .ﬁndLongestMatch function has two drawbacks: it
 relies on plain recursion (see Sect. 5) and it operates on progressively shorter
 input strings (due to the preﬁxes being consumed to create tokens), which
 reduces memoization opportunities. To address these issues, we implement a tail-
 recursive algorithm that operates on the full input string together with indices.
     Instead of returning the longest matching preﬁx directly, the new algorithm
 computes the position of the furthest nullable state reachable from a given index
 (with the function furthestNullablePosition). This representation enables memo-
 ization, since all recursive calls operate on the same input string and diﬀer only
 in their indices. Figure 3 shows both the naive and the tail-recursive versions,
.ﬁndLongestMatch and .ﬁndLongestMatchTR respectively.

     Tail-recursive functions’ memoization cannot be implemented directly using
 the technique mentioned earlier, since updating the cache would break tail recur-
 sion. We therefore maintain an explicit stack of encountered parameters. Once
 the tail-recursive computation completes, the calling function iterates over this
 stack and updates the cache for all recorded calls. Because all recursive calls
 return the same result, this strategy preserves correctness while enabling mem-
 oization. This can be seen as an explicit simulation of the JVM call stack in
 the heap, inspired by techniques used in continuation-passing style and related
 defunctionalization transformations.
     The memoization of furthestNullablePosition is equivalent to the technique
 proposed by Reps [32]. As a result, lexing runs in .O(n) time, where .n is the
 input string length. To the best of our knowledge, this is the ﬁrst veriﬁed imple-
 mentation of longest match lexing with linear-time complexity. By contrast,
 Verbatim++ [15] also veriﬁes memoization, but due to its choice of data struc-
 tures achieves .O(n log n) complexity. We evaluate the performance impact in
 Sect. 8.
     As proposed by Reps [32], memory usage can be traded oﬀ against constant-
 factor performance by memoizing only a fraction of calls. We implement and
 verify this heuristic by storing only one out of every .k calls when the input
 string is longer than .M characters, where both .k and .M are computed by pure
 and opaque functions that can depend on the rules and the input string. The
                            Formally Veriﬁed Linear-Time Invertible Lexing      153




Fig. 3. Algorithms that ﬁnd the longest preﬁx matching a given zipper and signatures
of the memoized function used for .findLongestMatch.


correctness proof is agnostic to these functions, so changing them does not aﬀect
veriﬁcation. By default, we set them to the constant values .k = 10 and .M = 106 .


7   Verification Experience

We discuss our experience formally verifying ZipLex. In Stainless, proofs are
written as Scala functions and expressions alongside executable code. Table 1
shows the sizes of implementation and proof components in terms of lines of code.
Overall, the proof-related code amounts to roughly ten times more lines than the
executable implementation. We spent most of the time exploring strategies for
inductive proofs. Aside from simple completions in VS Code, we did not rely on
LLMs. In this section, we outline how each component (lexer, regular-expression
engine, zipper optimization, and memoization framework) is speciﬁed, which
154        S. Chassot and V. Kunčak

induction schemes and ghost arguments are used to discharge proof obligations,
and where the main proof challenges arise.

                        Table 1. Line of code count per component

      Module                                Program LOC Spec + Proof LOC Total
      Longest Match Lexing                  580           2030           2610
      Lexer Printing + Invertibility        130           1430           1560
      Regex Derivative Based Matching       470           2440           2910
      Zipper Based Matching                 390           2670           3060
      BalanceConc                           255           320            575
      List & Set lemmas                     -             1610           1610
      Mutable HashMap (excluding LongMap) 90              2700           2790
      Total                                 1’915         13’200         15’115


General Proof Methodology. Over the course of development, we ﬁrst imple-
mented an intentionally ineﬃcient but conceptually simple and easily veriﬁable
version of the target algorithm. We then incrementally veriﬁed more eﬃcient
implementations or optimizations, each time proving their equivalence with the
previous version. For regular expression matching, we started from a straightfor-
ward matching procedure (our executable speciﬁcation), then introduced Brzo-
zowski derivatives, followed by a zipper-based algorithm, and ﬁnally added mem-
oization. The lexer was ﬁrst implemented as a naive recursive function, then
transformed into a tail-recursive version, and ﬁnally extended with memoiza-
tion. We applied an analogous reﬁnement to the underlying data structure: we
moved from a simple singly linked list to the more eﬃcient BalanceConc con-
catenable tree representation with arrays as described in Sect. 5. (We denote
this data structure simply as Sequence.) This methodology yields a fully veri-
ﬁed, executable implementation early on, which we then optimize for eﬃciency
while preserving formal correctness.
Longest Match. We begin with the proof of the longest match semantics.
We ﬁrst establish this property for the list-based function lexList, which uses
plain recursion and relies on the intermediate functions maxPrefixOneRule and
maxPrefix to compute, respectively, the longest preﬁx for each rule and the global
longest preﬁx. The proof proceeds by induction on the input list and relies on two
key ingredients: (1) the correctness of regular expression matching, in particular
that findLongestMatch is sound and returns the longest matching preﬁx, and (2)
auxiliary lemmas establishing the soundness of maxPrefixOneRule and maxPrefix.
    From this basis, we ﬁrst show observational equivalence between the recursive
Sequence-based implementation lexRec and lexList, using the bridging speciﬁca-
tion of Sequence as a List. We then prove that the tail-recursive implementation
lexTailRec produces exactly the same output as lexRec on all inputs. This ﬁnal
step requires helper lemmas about associativity of list concatenation and prop-
erties of lex, such as the fact that removing a suﬃx of the input does not aﬀect
the lexing of the preﬁx, provided that the cut occurs at token boundaries.
                             Formally Veriﬁed Linear-Time Invertible Lexing     155

 Invertibility. We ﬁrst establish invertibility for the list-based implementations
 of printing functions, and then prove equivalence with their sequence-based and
 tail-recursive counterparts. The proof of .print(lex(s)) = s proceeds by induction
 on .s. For the converse direction, .lex(print(ts)) = ts, we likewise perform induc-
 tion on .ts, supported by several auxiliary lemmas. These include, for example,
 that the separability predicate .sep(ts) ensures that the ﬁrst token produced by
.lex(print(ts)) is .ts.head, and that the same property holds for sequences inter-
 leaving separator and non-separator tokens. Several lemmas rely on properties
 of regular expressions, such as character sets used by the rules and their impact
 on preﬁx.
 Naive Derivative-Based Regular Expression Matcher. For the derivative-
 based regular expression engine, we prove correctness by handling each construc-
 tor case separately and then combining the resulting lemmas to establish the
 main theorem .∀r, s. matchR(r, s) = matchRSpec(r, s). For example, one lemma
 shows that if .r1 + r2 matches a string .s, then either .r1 or .r2 matches .s. Con-
 versely, another lemma proves that if .r matches .s, then both .r + r and .r + r
 match .s. Taken together, these lemmas establish the correctness of Brzozowski’s
 derivative-based matching algorithm.
 Zipper Regular Expression Matching. As explained in Sect. 4.2, the main
 correctness theorem for zipper-based matching is .∀s, z. matchR(unfocus(z), s) =
 matchZ(z, s). We state and prove this theorem using a list-based representation
 of zippers (rather than sets) in order to enable induction on the list of contexts.
     Although the derivative operations on regular expressions and on zippers are
 structurally similar and intuitively equivalent, the proof of this theorem is com-
 plex and requires approximately 600 LOC on its own. The main diﬃculty stems
 from the non-injectivity of the unfocus function. An intuitive formulation of the
 equivalence would be .∀r, s. matchR(r, s) = matchZ(focus(r), s), which suggests
 induction on the regular expression and the input string. However, this approach
 fails in our setting. After rewriting .matchR using its speciﬁcation, one would
 need properties such as .focus(Union(r1 , r2 )) = focus(r1 ) ∪ focus(r2 ) to apply
 the induction hypothesis. This equality does not hold for our implementation of
 focus, even though unfocusing both sides yields equivalent regular expressions.
 As a result, the induction breaks down.
     We therefore use the formulation .∀z, s. matchR(unfocus(z), s) =
 matchZ(z, s), which allows induction on the zipper and the input string instead.
 This makes the proof possible, but signiﬁcantly more involved, as unfocus itself
 introduces an additional induction over the list of contexts.
     In summary, despite the similar high-level structure of the two derivative
 algorithms, the fundamental diﬀerence between regular expressions and zippers
 complicates the proof. Regular expressions form tree-like structures with a clear
 recursive schema, while zippers are ﬂat collections of contexts, which do not
 admit the same induction patterns.
Memoization Framework. As discussed in Sect. 6, the memoization frame-
work relies on a veriﬁed mutable HashMap[K, V]. To prove its correctness, we
follow the approach of Chassot et al. [7] by establishing equivalence between
156      S. Chassot and V. Kunčak

each mutable operation of HashMap[K, V] and the corresponding operation
on an immutable executable speciﬁcation ListMap[K, V] implemented as an
immutable association list of pairs. We therefore ﬁrst implement and verify a
generic ListMap[K, V], similar to their ListLongMap[V]. We then implement and
prove the correctness of the additional layer that stores buckets as immutable
linked lists of key-value pairs inside an underlying LongMap[V]. For this proof,
we rely on the correctness of the LongMap [7]. The proofs of the memoization
helper lemmas proceed by induction on the key-value pairs stored in the map.
Verification Condition Statistics. Stainless generates 21’961 veriﬁcation
conditions (VCs) for the entire project (8’802 of which are cache hits), and
takes .≈130 min to verify on the server described in Sect. 8, creating multiple GB
of SMT-LIB ﬁles. We use the Stainless version from the commit at the time of
paper preparation4 . VC veriﬁcation times resemble a negative exponential distri-
bution, with only 44 VCs taking more than 10 s to verify. The slowest VC takes
58 s to verify during the run with multiple approximating SMT-LIB queries.
Stainless uses function unfolding, so it queries SMT solvers multiple times for
a single VC. The ﬁnal SMT-LIB ﬁle for this slowest query has 100 lines; cvc5
takes less than a second to re-verify it.


8     Performance Evaluation
To evaluate the practicality of ZipLex, we present a performance evaluation
investigating the following questions:
Q1: What complexity does ZipLex exhibit on an adversarial grammar, and how
    does it compare to other state-of-the-art lexers?
Q2: What is the cost of computing .sep and what is the impact of the mix of
    static and runtime checks using the .PrintableTokens constructs?
Q3: What is the performance of ZipLex on a realistic JSON grammar and how
    does it compare to other veriﬁed and unveriﬁed lexers?
All experiments are run on a server running Linux with two sockets of an AMD
EPYC 9254 24-Core processor (base frequency 2.9 GHz, up to 4.15 GHz), oﬀer-
ing 96 virtual processors and 128 GB of RAM. Our algorithms are sequential and
do not exploit parallelism. Error bars show 99.9% conﬁdence intervals. We use
the JMH benchmarking library [19] from OpenJDK to benchmark Scala code.
We use OpenJDK JVM version 21.0.2 unless stated otherwise.
Evaluating Linear-Time Behavior Via Lexing .a and .a∗ b. To evaluate the
impact of memoization on lexing performance, we ﬁrst consider a grammar with
two rules, .r1 = a and .r2 = a∗ b, as in [22]. This grammar is adversarial for naive
longest-match lexers: when the input string contains only ‘.a’s, computing the
longest match for .r2 requires consuming the entire remaining input to ensure
that no ‘.b’ occurs at the end. As a result, naive lexing exhibits quadratic time
4
    https://github.com/epﬂ-lara/stainless/tree/d89c8eccaf0261f8be348bee7ﬀa
    6f5a3c1c5ca6.
                               Formally Veriﬁed Linear-Time Invertible Lexing          157

complexity. Although such grammars rarely appear in compiler lexers, they are
relevant in the context of uniform tokenization, where rules are part of the input.
In such settings, adversarial grammars can be used to mount denial-of-service
attacks on lexers. Even if rare, such patterns would arise in a lexer having one
rule for digits, .r1 = digit, and one for real number constants, .r2 = digit∗ .digit.
    Figure 4 compares lexing times for strings of ‘.a’s up to 50 000 characters using
ﬂex [29], Coqlex [27], Verbatim++ [15], and ZipLex. Both ﬂex and Coqlex exhibit
quadratic behavior on this grammar. Verbatim++ stack overﬂows beyond 85 000
characters. Figure 6 (Right) shows ZipLex’s performance in the same setting
(with larger ﬁles), experimentally conﬁrming the linear complexity.




Fig. 4. Lexing time with grammar rules .r1 = a and .r2 = a∗ b, on strings of ‘.a’s of sizes
ranging from 100 to 50K (or 100K) comparing ZipLex, ﬂex, Coqlex, and Verbatim++.



 Evaluating Printable Sequences on JSON Lexing and Sorting. We next
 evaluate ZipLex on the JSON object-sorting application presented in Sect. 2.
 We focus on the cost of enforcing separability through the R-Path predicate.
 Figure 5 (left) compares lexing alone with lexing followed by instantiating a
 PrintableTokens wrapper, which computes the R-Path predicate .sep. In both
 cases, memoization is enabled. The results show that the overhead of computing
.sep is small. This is partly explained by the fact that the derivative cache is
 already populated during lexing. In practice, we expect PrintableTokens to be
 instantiated immediately after lexing, reusing the cache and keeping the overhead
 low.
     Using PrintableTokens provides a signiﬁcant performance beneﬁt when slicing
 and recombining token sequences. Figure 5 (right) compares recombining slices
 represented as PrintableTokens with recombining plain token sequences followed
 by recomputing the .sep. Concatenating two PrintableTokens instances requires
 only a constant-time check of .sep(t1 , t2 ) at the boundary (Sect. 3.4), since .sep is
 maintained as a statically veriﬁed invariant. Consequently, recombining slices is
 linear in the number of slices, whereas recomputing .sep is linear in the number of
 tokens. These results illustrate that combining static guarantees with lightweight
 runtime checks, as done by PrintableTokens, provides an eﬀective way to obtain
158     S. Chassot and V. Kunčak

veriﬁed and eﬃcient programs. The right plot of Fig. 5 also shows that con-
catenation of large Sequences is eﬃcient, conﬁrming the suitability of this data
structure for runtime use.




Fig. 5. Left: Comparison between lexing and computing R-Path sep on the sequence
of tokens (instantiating PrintableTokens with the obtained tokens) against lexing only,
both using memoization. Right: Comparison between recombining slices as instances
of PrintableTokens and creating a sequence and computing the R-Path sep.




Fig. 6. Left: JSON lexers performance comparison; x-axis shows the length of input
ﬁles in number of characters; y-axis shows the time in seconds to lex the input ﬁle;
comparison between ZipLex, Coqlex, OCamllex, and variants of Verbatim++. Right:
ZipLex lexing time with grammar .r1 = a and .r2 = a∗ b, on strings of .as of sizes ranging
from 10K to 30M of characters, with a linear regression of degree 1.


Performance Comparison of JSON Lexers. We compare ZipLex against
veriﬁed and unveriﬁed JSON lexers using the benchmark inputs from the
Coqlex evaluation [27]. We reuse the benchmarking infrastructure released with
Coqlex [26], combined with our own infrastructure, to compare ZipLex with
Coqlex [27], Verbatim++ [15], OCamllex [25], and two additional Verbatim++
variants from Ouedraogo et al. [27]. All lexers are formally veriﬁed except for
OCamllex (but only ZipLex veriﬁes invertibility). The benchmark consists in
                             Formally Veriﬁed Linear-Time Invertible Lexing      159

lexing each ﬁle and measuring total execution time. Figure 6 (left) shows the
results. Unlike Verbatim++, which relies on a transformation from regular expres-
sions to DFAs and incurs a ﬁxed preprocessing overhead of approximately two
seconds, ZipLex’s zipper-based matching and memoization introduce no such
upfront cost. ZipLex is approximately .3.5× slower than Coqlex on JSON inputs,
while remaining two orders of magnitude faster than Verbatim++. To better
assess the reasons behind the diﬀerence with Coqlex, we run the same exper-
iments with two new variants of ZipLex with reduced memoization: one with
memoization enabled only for the zipper-based derivative computations, and
one with no memoization enabled. We also run our experiments using the Ora-
cle GraalVM [36] (version 21.0.11 ) instead of OpenJDK. The results are shown
in Fig. 7 (left). The results show that, while memoization ensures linear complex-
ity for lexing under all circumstances, it is detrimental to absolute performance
in the particular case of the JSON grammar. Indeed, without any memoization
enabled, ZipLex is faster when lexing JSON, and the variant with memoization
of derivatives lies between ZipLex with full memoization and ZipLex with no
memoization. Running on GraalVM without any memoization, ZipLex is faster
than on OpenJDK, and is .1.37× slower than Coqlex. Due to diﬀerences in the
underlying runtimes (OCaml vs diﬀerent JVMs), we are unable to deﬁnitely
establish the source of the remaining 1.37.× performance gap. We suspect that
a key diﬀerence is that Coqlex lexers are specialized for the alphabet of ASCII
characters and can make use of character intervals, whereas ZipLex characters
are entirely generic, leading to boxing and explicit sets of characters in the zipper
data structure.
    We believe that ZipLex’s performance is acceptable given its design goals.
In addition to correctness guarantees with respect to regular expressions and
longest match semantics, ZipLex provides invertible lexing and supports arbi-
trary alphabets, oﬀering greater ﬂexibility than existing veriﬁed lexers, as well as
guaranteed linear behavior in the input length thanks to veriﬁed memoization.
Performance of the Mutable Hash Table. Our veriﬁed hash table, being
mutable, allows us to add memoization to functions with less refactoring that
needed with an immutable cache. One could implement a mutable cache as a
variable containing an immutable map which would lead to a smaller veriﬁ-
cation eﬀort. Such immutable structure would, however, lead to worse perfor-
mance, as shown in Fig. 7 (right). The ﬁgure measures time for the following
operations: insert N random pairs to the map under evaluation, remove half
of those pairs, then insert all N pairs again. We compare our veriﬁed hash
map, veriﬁed LongMap [7], Scala’s standard library’s mutable hash map, and
its immutable HashMap. Our mutable HashMap is slower than Scala library’s
unveriﬁed hashmap but outperforms Scala library’s immutable HashMap, espe-
cially for large numbers of pairs. This demonstrates that using a mutable hash
table for caches improves performance and justiﬁes the veriﬁcation eﬀort.
160     S. Chassot and V. Kunčak




Fig. 7. Left: JSON lexers performance comparison; x-axis shows the length of input
ﬁles in number of characters; y-axis shows the time in seconds to lex the input ﬁle; com-
parison between Coqlex, OCamllex, and diﬀerent memoization variants of ZipLex, all
memoization (named ZipLex), only derivative computations memoized (named ZipLex
(Mem only deriv)), no memoization (named ZipLex (No Mem)), and ZipLex (No Mem)
run on Oracle GraalVM. Verbatim++ is not shown as it is several orders of magnitude
slower, see Fig. 6. Right: Performance evaluation of Scala library immutable map, Scala
library mutable hashmap, the veriﬁed LongMap hash table, and our veriﬁed hash map
on a benchmark performing the following tasks: insert N pairs into the map, remove
half of them, and update the N pairs again.


9     Conclusion
ZipLex is a veriﬁed framework for invertible lexical analysis with linear worst-
case complexity. Unlike past veriﬁed lexers, which only ensure the semantics
of matching regular expressions and maximal munch, ZipLex also guarantees
that lexing and printing are mutual inverses. Our design relies on two key ideas:
(1) a new class of predicates, R-Paths, that capture the separability of token
sequences, and (2) a combination of veriﬁed data structures and optimizations,
including Huet’s zippers and memoized derivatives and lexing, to achieve prac-
tical matching performance. We implemented ZipLex in Scala and veriﬁed its
correctness and invertibility using the Stainless veriﬁer. Our evaluation demon-
strates that ZipLex supports applications such as JSON processing and compiler
lexers. Thanks to veriﬁed memoization based on a veriﬁed mutable hash table,
ZipLex exhibits linear complexity in the worst case, even on grammars for which
state-of-the-art lexers such as ﬂex and OCamlex behave quadratically. On JSON
lexing, ZipLex is a factor of .3× slower than the best veriﬁed quadratic lexer,
Coqlex, but two orders of magnitude faster than Verbatim++. By disabling mem-
oization, the performance gap with Coqlex can be reduced to a factor of .1.37×.
Our experiments thus show that linear time, veriﬁcation, and invertibility can
be achieved without prohibitive cost.

Acknowledgments. This study was funded in part by Swiss National Science Foun-
dation grant number 200021_219474 and State Secretariat for Education, Research,
                               Formally Veriﬁed Linear-Time Invertible Lexing          161

and Innovation/European Space Agency grant “Embedded Flight Software Veriﬁca-
tion“.
    We thank Romain Edelmann for useful discussions; Chap. 2 of his dissertation [12]
on lexing with zippers and derivatives provided a starting point for our zipper-based
representation.


Data Availability Statement. This paper is accompanied by a Scala project includ-
ing the full implementation of the lexer, the regular expression matching engine, and the
memoization framework–including the mutable hash map implementation (and a copy
of the LongMap implementation [7]) together with all .k-inductive speciﬁcations and
lemmas. The project includes diﬀerent example lexers for diﬀerent grammars including
a subset of Python, Amy (a teaching language), as well as the adversarial grammar
described in Sect. 8. It also contains the JSON manipulation application example from
Sect. 2. The entire project veriﬁes using Stainless [34]. The project ﬁnally contains
the benchmarking code to reproduce our performance evaluation, as well as scripts to
run the evaluation and analyze the resulting data. The paper is also accompanied by
1.35GB of SMT-LIB ﬁles generated by Stainless during veriﬁcation, which can be used
as a source of benchmarks for expressive categories of SMT competitions. The artifact
consists of a Docker image containing all this material and all required software and
is available on Zenodo [9]. The version number 4 on Zenodo (https://doi.org/10.5281/
zenodo.20084365) has been evaluated by the artifact evaluation committee.
    The Scala project is also available in the Bolts repository [1] under lexers/regex. All
the code presented in this paper, including ZipLex and the memoization framework, is
part of the Bolts Continuous Integration (CI) on GitHub [1], and is therefore veriﬁed
on a nightly basis.
    Some of the improved data structures such as the immutable arrays with a zero-
copy slice operation, and the executable speciﬁcation of the hash table, ListMap, are
now part of the Stainless standard library [34] under frontends/library/stainless.
    An extended version of this paper is available of Arxiv [8].
Disclosure of Interests. The authors have no competing interests to declare that
are relevant to the content of this article.


References
 1. epﬂ-lara/bolts. https://github.com/epﬂ-lara/bolts (Apr 2026), https://github.
    com/epﬂ-lara/bolts, original-date: 2017-10-12T10:48:10Z
 2. Brachthäuser, J.I., Rendel, T., Ostermann, K.: Parsing with ﬁrst-class derivatives.
    In: Visser, E., Smaragdakis, Y. (eds.) Proceedings of the 2016 ACM SIGPLAN
    International Conference on Object-Oriented Programming, Systems, Languages,
    and Applications, OOPSLA 2016, part of SPLASH 2016, Amsterdam, The Nether-
    lands, October 30 - November 4, 2016, pp. 588–606. ACM (2016). https://doi.org/
    10.1145/2983990.2984026
 3. Brzozowski, J.A.: Derivatives of regular expressions. J. ACM 11(4), 481–494
    (1964). https://doi.org/10.1145/321239.321249
 4. Bucev, M., Chassot, S., Felix, S., Schramka, F., Kuncak, V.: Formally veriﬁ-
    able generated ASN.1/ACN encoders and decoders: a case study. In: Krishna,
    S., Sankaranarayanan, S., Trivedi, A. (eds.) Veriﬁcation, Model Checking, and
    Abstract Interpretation - 26th International Conference, VMCAI 2025, Denver,
162     S. Chassot and V. Kunčak

    CO, USA, January 20-21, 2025, Proceedings, Part II, pp. 185–207. LNCS. Springer
    (2025). https://doi.org/10.1007/978-3-031-82703-7_9
 5. Bucev, M., Kunčak, V.: Formally veriﬁed quite OK image format. In: Griggio,
    A., Rungta, N. (eds.) 22nd Formal Methods in Computer-Aided Design, FMCAD
    2022, Trento, Italy, October 17-21, 2022, pp. 343–348. IEEE (2022). https://doi.
    org/10.34727/2022/ISBN.978-3-85448-053-2_41
 6. Cattell, R.G.G.: Formalization and automatic derivation of code generators. Tech.
    rep., Carnegie-Mellon University, Dept. of Computer Science (1978)
 7. Chassot, S., Kunčak, V.: Verifying a realistic mutable hash table. In: Benzmüller,
    C., Heule, M.J., Schmidt, R.A. (eds.) Automated Reasoning, pp. 304–314. Springer,
    Cham (2024). https://doi.org/10.1007/978-3-031-63498-7_18
 8. Chassot, S., Kunčak, V.: Formally veriﬁed linear-time invertible lexing (2026).
    https://doi.org/10.48550/arXiv.2510.18479, https://arxiv.org/abs/2510.18479
 9. Chassot, S., Kunčak, V.: Formally Veriﬁed Linear-Time Invertible Lexing (Arti-
    fact). https://zenodo.org/records/19830775, May 2026. https://doi.org/10.5281/
    zenodo.19830775
10. Chattopadhyay, A., Li, A.W., Mamouras, K.: Veriﬁed and eﬃcient matching of
    regular expressions with lookaround. In: Proceedings of the 14th ACM SIGPLAN
    International Conference on Certiﬁed Programs and Proofs, pp. 198–213. CPP ’25.
    Association for Computing Machinery, New York, January 2025. https://doi.org/
    10.1145/3703595.3705884
11. Darragh, P., Adams, M.D.: Parsing with zippers (functional pearl). Proc. ACM
    Program. Lang. 4(ICFP), 108:1–108:28 (2020). https://doi.org/10.1145/3408990
12. Edelmann, R.: Eﬃcient Parsing with Derivatives and Zippers. Ph.D. thesis,
    EPFL (2021). https://doi.org/10.5075/epﬂ-thesis-7357, https://infoscience.epﬂ.
    ch/handle/20.500.14299/179767
13. Edelmann, R., Hamza, J., Kuncak, V.: Zippy LL(1) parsing with derivatives. In:
    Donaldson, A.F., Torlak, E. (eds.) Proceedings of the 41st ACM SIGPLAN Inter-
    national Conference on Programming Language Design and Implementation, PLDI
    2020, London, UK, June 15-20, 2020, pp. 1036–1051. ACM (2020). https://doi.org/
    10.1145/3385412.3385992
14. Egolf, D., Lasser, S., Fisher, K.: Verbatim: a veriﬁed lexer generator. In: 2021 IEEE
    Security and Privacy Workshops (SPW), pp. 92–100. IEEE, San Francisco, May
    2021. https://doi.org/10.1109/SPW53761.2021.00022
15. Egolf, D., Lasser, S., Fisher, K.: Verbatim++: veriﬁed, optimized, and semantically
    rich lexing with derivatives. In: Proceedings of the 11th ACM SIGPLAN Interna-
    tional Conference on Certiﬁed Programs and Proofs, pp. 27–39. ACM, Philadel-
    phia, January 2022. https://doi.org/10.1145/3497775.3503694
16. Guilloud, S., Pit-Claudel, C.: Veriﬁed and optimized implementation of orthologic
    proof search. In: Piskac, R., Rakamaric, Z. (eds.) Computer Aided Veriﬁcation -
    37th International Conference, CAV 2025, July 23-25, 2025, Proceedings, Part III.
    LNCS, vol. 15933, pp. 130–152. Springer, Zagreb, Croatia (2025). https://doi.org/
    10.1007/978-3-031-98682-6_8
17. Hamza, J., Voirol, N., Kuncak, V.: System FR: formalized foundations for the
    Stainless veriﬁer. Proc. ACM Program. Lang. 3(OOPSLA), 166:1–166:30 (2019).
    https://doi.org/10.1145/3360592
18. Huet, G.: The zipper. J. Functional Programm. 7(5), 549–554 (1997). https://doi.
    org/10.1017/S0956796897002864
19. Java microbenchmark harness (JMH). https://github.com/openjdk/jmh.
    Retrieved 25 January 2026
                             Formally Veriﬁed Linear-Time Invertible Lexing      163

20. Leroy, X.: The CompCert C veriﬁed compiler: Documentation and user’s manual.
    report, Inria, December 2024. https://inria.hal.science/hal-01091802, pages: 1
21. Leroy, X., Blazy, S., Kästner, D., Schommer, B., Pister, M., Ferdinand, C.: Com-
    pCert - a formally veriﬁed optimizing compiler. In: ERTS 2016: Embedded Real
    Time Software and Systems, 8th European Congress, SEE, HAL, Toulouse, France,
    January 2016. https://inria.hal.science/hal-01238879
22. Li, A.W., Mamouras, K.: Eﬃcient algorithms for the uniform tokenization problem.
    Proc. ACM Program. Lang. 9(OOPSLA1), 1492–1518 (2025). https://doi.org/10.
    1145/3720498
23. Madhavan, R., Kulal, S., Kuncak, V.: Contract-based resource veriﬁcation for
    higher-order functions with memoization. SIGPLAN Not. 52(1), 330–343 (2017).
    https://doi.org/10.1145/3093333.3009874
24. Nipkow, T.: Veriﬁed lexical analysis. In: Grundy, J., Newey, M. (eds.) TPHOLs
    1998. LNCS, vol. 1479, pp. 1–15. Springer, Heidelberg (1998). https://doi.org/10.
    1007/BFb0055126
25. OCamllex. https://ocaml.org/manual/5.3/lexyacc.html. retrieved 15 May 2026
26. Ouedraogo, W., Scherer, G., Strassburger, L.: Coqlex artifact gitlab repos-
    itory. https://gitlab.inria.fr/wouedrao/coqlex/-/tree/master/Comparison/JSON?
    ref_type=heads, December 2023
27. Ouedraogo, W., Scherer, G., Strassburger, L.: Coqlex: generating formally veri-
    ﬁed lexers. Art Sci. Eng. Programm. 8(1), 3–1 (2023). https://doi.org/10.22152/
    programming-journal.org/2024/8/3
28. Owens, S., Reppy, J., Turon, A.: Regular-expression derivatives re-
    examined. J. Funct. Program. 19(2), 173–190 (2009). https://doi.org/10.
    1017/S0956796808007090
29. Paxson, V., et al.: Flex–fast lexical analyzer generator. Lawrence Berkeley Labo-
    ratory (1995)
30. Ranta, A.: Grammatical Framework - Programming with Multilingual Grammars.
    CSLI Studies in Computational Linguistics, Cambridge University Press (2011).
    http://cslipublications.stanford.edu/site/9781575866277.shtml
31. Rendel, T., Ostermann, K.: Invertible syntax descriptions: unifying parsing and
    pretty printing. SIGPLAN Not. 45(11), 1–12 (2010). https://doi.org/10.1145/
    2088456.1863525
32. Reps, T.W.: “Maximal-munch” tokenization in linear time. ACM Trans. Program.
    Lang. Syst. 20(2), 259–273 (1998). https://doi.org/10.1145/276393.276394
33. Santo, N.D., Barrière, A., Pit-Claudel, C.: A Coq mechanization of JavaScript
    regular expression semantics. Proc. ACM Program. Lang. 8(ICFP), 1003–1031
    (2024). https://doi.org/10.1145/3674666
34. epﬂ-lara/stainless. https://github.com/epﬂ-lara/stainless, May 2026, original-
    date: 2016-08-17T14:08:38Z
35. Varatalu, I.E., Veanes, M., Ernits, J.: Re#: High performance derivative-based
    regex matching with intersection, complement, and restricted lookarounds. Proc.
    ACM Programm. Lang. 9(POPL), 1–32 (2025). https://doi.org/10.1145/3704837
36. Würthinger, T., et al.: Practical partial evaluation for high-performance dynamic
    language runtimes. In: Cohen, A., Vechev, M.T. (eds.) Proceedings of the 38th
    ACM SIGPLAN Conference on Programming Language Design and Implementa-
    tion, PLDI 2017, Barcelona, Spain, June 18-23, 2017, pp. 662–676. ACM (2017).
    https://doi.org/10.1145/3062341.3062381
164     S. Chassot and V. Kunčak

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
