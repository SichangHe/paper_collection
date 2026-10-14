                                             LSPRAG: LSP-Guided RAG for Language-Agnostic Real-Time
                                                              Unit Test Generation
                                                           Gwihwan Go                                                Quan Zhang∗                                     Chijin Zhou∗
                                                         Tsinghua University                               East China Normal University                     East China Normal University
                                                            Beijing, China                                       Shanghai, China                                   Shanghai, China
                                                        iejw1914@gmail.com                                     quanzh98@gmail.com                              tlock.chijin@gmail.com

                                                                                           Zhao Wei                                            Yu Jiang
                                                                                          Tencent                                        Tsinghua University
                                                                                       Beijing, China                                       Beijing, China
                                                                                   zachwei@tencent.com                                jiangyu198964@126.com
arXiv:2510.22210v2 [cs.SE] 2 Mar 2026




                                        Abstract                                                                                Engineering (ICSE ’26), April 12–18, 2026, Rio de Janeiro, Brazil. ACM, New
                                        Automated unit test generation is essential for robust software de-                     York, NY, USA, 13 pages. https://doi.org/10.1145/3744916.3773189
                                        velopment, yet existing approaches struggle to generalize across
                                        multiple programming languages and operate within real-time de-                         1    Introduction
                                        velopment. While Large Language Models (LLMs) offer a promising
                                                                                                                                Unit testing for modern software systems is crucial yet labor-
                                        solution, their ability to generate high coverage test code depends
                                                                                                                                intensive [5, 68]. To ensure reliability, test suites must achieve
                                        on prompting a concise context of the focal method. Current solu-
                                                                                                                                high coverage to expose subtle bugs and edge cases. It requires
                                        tions, such as Retrieval-Augmented Generation, either rely on im-
                                                                                                                                developers to have a deep understanding of the internal logic and
                                        precise similarity-based searches or demand the creation of costly,
                                                                                                                                dependencies of the codebase, including how the functions under
                                        language-specific static analysis pipelines. To address this gap, we
                                                                                                                                test interact with their surrounding implementation. This challenge
                                        present LspRag, a framework for concise-context retrieval tailored
                                                                                                                                is even greater in today’s software development, where enterprise
                                        for real-time, language-agnostic unit test generation. LspRag lever-
                                                                                                                                codebases frequently span multiple programming languages, and de-
                                        ages off-the-shelf Language Server Protocol (LSP) back-ends to
                                                                                                                                velopers expect real-time test generation as they code [1, 32, 61, 62].
                                        supply LLMs with precise symbol definitions and references in real
                                                                                                                                   Recent advances in Large Language Models (LLMs) have invig-
                                        time. By reusing mature LSP servers, LspRag provides an LLM with
                                                                                                                                orated research on real-time multi-language unit-test generation.
                                        language-aware context retrieval, requiring minimal per-language
                                                                                                                                Commercial systems such as GitHub Copilot [52] already offer
                                        engineering effort. We evaluated LspRag on open-source projects
                                                                                                                                one-click test generation, boosting test quality with simple heuris-
                                        spanning Java, Go, and Python. Compared to the best performance
                                                                                                                                tics—for example, giving higher weight to files a developer has
                                        of baselines, LspRag increased line coverage by up to 174.55% for
                                                                                                                                recently opened [23]. At the same time, Repository-level Retrieval-
                                        Golang, 213.31% for Java, and 31.57% for Python.
                                                                                                                                Augmented Generation (RAG) techniques supply LLMs with addi-
                                                                                                                                tional code context obtained via textual similarity [38, 63], graph-
                                        CCS Concepts                                                                            based relationships [36, 37], or even web search [59, 66].
                                        • Software and its engineering → Software testing and de-                                  Problem. Although existing methods enhanced code genera-
                                        bugging; • Computing methodologies → Neural networks;                                   tion practice, they are still limited in generating high coverage
                                        Natural language processing.                                                            unit tests, because they fail to retrieve relevant context precisely.
                                                                                                                                For example, in Figure 1, to cover the “true” branch of line 3 in
                                        Keywords                                                                                checkout method, it is necessary to retrieve the definition of the
                                        Unit Testing, Language Server Protocol, Retrieval Augmented Gen-                        guard-condition method isValid, which resides in another loca-
                                        eration, Large Language Model                                                           tion. ( e.g., PaymentService.java). Existing approaches, however,
                                                                                                                                struggle to handle this seemingly straightforward task effectively.
                                        ACM Reference Format:
                                                                                                                                GitHub Copilot is not able to pull dependent context across files,
                                        Gwihwan Go, Quan Zhang, Chijin Zhou, Zhao Wei, and Yu Jiang. 2026.
                                        LSPRAG: LSP-Guided RAG for Language-Agnostic Real-Time Unit Test
                                                                                                                                so the user must supply the relevant code manually [24].
                                        Generation. In 2026 IEEE/ACM 48th International Conference on Software                     Existing RAG approaches for code generation, unfortunately,
                                                                                                                                also struggle to discover such a use-definition relationship precisely.
                                        ∗ Quan Zhang and Chijin Zhou are corresponding authors.                                 This is because the RAG’s embedding-and-similarity approach de-
                                                                                                                                pends on superficial cues such as similar function names, variable
                                                                                                                                names, and comments to infer relationships. These cues are often
                                                                                                                                noisy and prone to variation across coding styles and conventions.
                                        This work is licensed under a Creative Commons Attribution 4.0 International License.   Recent research [8, 36] recognizes this deficiency and augments
                                        ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                     retrieval with static-analysis-based searches; however, that solu-
                                        © 2026 Copyright held by the owner/author(s).
                                        ACM ISBN 979-8-4007-2025-3/26/04                                                        tion demands substantial human effort and remains tied to specific
                                        https://doi.org/10.1145/3744916.3773189                                                 programming languages, limiting their generalizability in today’s
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                        Gwihwan Go, Quan Zhang, Chijin Zhou, Zhao Wei, and Yu Jiang


                 boolean checkout(Cart cart, Card card) {                            Without LSP                                  LSP
                     long t0 = System.nanoTime();
                                                                                                                                Formatting
                     if (paymentService.isValid(card)) { // branch guard
                         ship(cart);
                                                                                                                                Definition
                         metrics.markSuccess();
          Generate       return true;
          Unit Test                                                                                                             Diagnosis
                     }
Generator
                     metrics.markFailure();                                                           LSP                           ...        LSP
                     return false;                                                                    RAG                                      RAG
                 }
           Need To
            Refer                                                                                       Integration Effort
   Unit          boolean isValid(Card c) {      // in PaymentService.java
   Tests             return !c.isExpired() &&                                     Figure 2: Integration effort before and after LSP.
                            luhnCheck(c.number());
                 }


Figure 1: Unit test generation scenario for focal method
checkout. To cover the “true” block of the first branch of the              execute the generated test code. Furthermore, the codebase under
focal method, the generator needs the definition of isValid                 test is often not compilable or executable in real-time.
from another file.                                                             We tackle these challenges from two dimensions. To address
                                                                            Challenge (1), we design a key token extraction strategy that identi-
                                                                            fies symbols essential for high-coverage test generation. Specifically,
                                                                            we employ a hybrid analysis approach that combines fine-grained
software development. This highlights the urgent need for a new             lexical information from the LSP with structural information from
approach for real-time and language-agnostic unit test generation.          the Abstract Syntax Tree (AST), effectively filtering out unneces-
   Insight. This paper introduces LspRag, a concise context re-             sary context. To address Challenge (2), we design a compile-free
trieval framework for multi-language unit test generation. Our key          self-repair mechanism that automatically fixes syntax errors in
insight is that modern editors already ship with mature static an-          unit tests. Specifically, we utilize the LSP’s diagnostic feature in a
alyzers exposed through the Language Server Protocol (LSP). By              compilation-free loop and retrieve the necessary context for repairs.
querying these analyzers on demand, LspRag obtains the precise              We continue this process iteratively until the errors disappear or
location of context for every used symbol (e.g., function, method,          the retry budget is exhausted, ensuring real-time performance.
etc) in the focal method.                                                      We implemented LspRag as a Visual Studio Code Extension to
   Challenges. Despite having sufficient and precise symbol infor-          streamline language-agnostic unit test generation and evaluated its
mation, generating high-coverage unit tests remains non-trivial:            performance on real-world Java, Python, and Golang projects. The
there still exist challenges. (1) The focal method includes exces-          results show that LspRag consistently improves the line coverage
sive irrelevant context. Achieving high test coverage requires              and the rate of valid tests generated, irrespective of the program-
precisely identifying the definitions of symbols that control branch        ming language or the underlying LLM employed. Our evaluation
conditions. However, in practice, a focal method often includes             demonstrates that LspRag yields substantial improvements in unit
many symbols unrelated to the branch condition. For example,                test quality in terms of its line coverage and valid rate. Specifi-
the nine-line checkout method in Figure 1 references eight exter-           cally, when compared to the best value among baselines, LspRag
nal symbols (Cart, Card, System, ..., and markFailure),                     improved line coverage by a range of 91.4% to 174.55% for Golang
each with potentially several lines of definition. Despite this, test       projects, 27.79% to 213.31% for Java projects, and 16.87% to 31.57%
coverage is only influenced by the isValid call. While retrieving           for Python projects. Similarly, the valid rate of generated tests in-
the definition for isValid is essential, collecting every definition        creased by up to 242.86% for Golang projects, 251.91% for Java
within the focal method introduces unnecessary, noisy context.              projects, and 20.16% for Python projects.
This excess context complicates the generator’s ability to locate              In summary, this paper makes the following contributions:
the correct context for solving the branch condition, ultimately            • We identify a gap between academic research and industry prac-
hindering the generation of high-quality unit tests.                          tice: developers in large companies require high-quality test cases
   (2) Hard to guarantee valid tests in real-time. Even when                  in real-time for different programming languages, yet concise
concise and relevant context is collected, simply providing LLMs              context for LLM is difficult to obtain without compilation, execu-
with more context does not guarantee the generation of valid test             tion, or heavyweight analysis.
code. As noted in prior research [35, 65, 67], large code context           • We designed and implemented LspRag, which generate language-
slices often introduce noise, which can obscure the original intent           agnostic high-coverage unit tests in real-time. The source code
and reduce the LLM’s ability to generate correct code. As a result,           is available at https://thu-wingtecher.github.io/LSPRAG.
the generated test code is likely to contain syntax errors, which hin-      • We conducted a comprehensive evaluation of LspRag on real-
der high-coverage test generation rather than support it. Previous            world projects in three different programming languages. The
works [2, 22, 28, 46, 60] have mitigated this issue by executing the          results validate the ability of LspRag to consistently improve
generated test code in advance and collecting error messages in a             the performance of unit test generation in terms of both line
fixing loop. However, this approach is not practical for a real-time          coverage and the rate of valid tests.
scenario, as it requires a significant amount of time to compile and
LSPRAG: LSP-Guided RAG for Language-Agnostic Real-Time Unit Test Generation                                 ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


2 Background                                                                  3    Motivating Example
2.1 Language Server Protocol                                                  Existing real-time code-generation techniques struggle to produce
                                                                              comprehensive unit tests, mainly because they cannot automatically
The Language Server Protocol (LSP) was introduced by Microsoft [41]
                                                                              retrieve the concise context that the focal method relies on. Closing
to address a significant challenge in software development: the need
                                                                              this gap is essential because exercising every branch demands a
for each editor and IDE to have a unique implementation for every
                                                                              precise understanding of the symbols that guard those branches.
programming language’s analysis features. As the number of editors
                                                                              Without this understanding, it’s difficult for LLM to understand
and languages proliferated, this approach became unsustainable,
                                                                              branch conditions and fails to generate the specific inputs needed
forcing language authors to repeatedly rewrite the same analysis
                                                                              to exercise them. To ground the problem, we present a motivating
logic. At the same time, tool vendors struggled to keep pace with
                                                                              example from the project Black [20], a widely used Python code
the emergence of new languages. LSP has resolved these problems
                                                                              formatter, and compare how existing research efforts attempt to
by standardizing communication between a language server and
                                                                              retrieve necessary context.
any compliant editor or IDE.
                                                                                 Figure 3 (a) illustrates the simplified focal method of the Black
   Before vs. After LSP As illustrated in Fig 2, LSP significantly
                                                                              project for which we want to generate unit tests. The method
reduces implementation costs by defining a standardized commu-
                                                                              is_split_before_delimiter evaluates a tree leaf and its prede-
nication protocol between language clients and language servers.
                                                                              cessor to assign a numeric priority that determines whether the
The language client, typically an editor or IDE used by a developer
                                                                              formatter should split the line before that delimiter. It skips var-arg
(shown on the right in each sub-figure), communicates with a stan-
                                                                              constructs, then gives higher priority to dots in attribute chains and
dalone language server process. This server, depicted on the left,
                                                                              logical operators, returning 0 when no split is warranted. To trigger
handles parsing, static analysis, and other language-specific tasks.
                                                                              diverse actions of this method, the generator must supply inputs
Before the adoption of LSP, adding rich language support required
                                                                              that make each branch guard evaluate to true and false. For instance,
redundant effort. For instance, both Eclipse and VS Code needed
                                                                              to satisfy the first guard, we must understand exactly when the
separate Java plug-ins, with each language client implementing
                                                                              function is_vararg returns true and which value of leaf produces
its pipeline for identical language features. LSP streamlines this
                                                                              that outcome. To do this, we need to retrieve the definition of the
process by establishing a standard protocol. Now, any compliant
                                                                              function is_vararg from other files, which requires (1) identifying
IDE can leverage existing language servers that also adhere to the
                                                                              the correct file names and (2) isolating the precise code snippets
LSP standard. This enables a single server to support multiple edi-
                                                                              that define the needed functions.
tors, allowing one editor to work with various languages by simply
                                                                                 Context retrieval is a well-studied problem in the field of LLM,
connecting to the appropriate servers.
                                                                              with many RAG techniques proposing advanced strategies. Existing
   Typical LSP capabilities. A standard LSP provides a suite of
                                                                              RAG techniques may address real-time unit-test generation for the
powerful features, including code completion, go-to-definition, find-
                                                                              focal method is_split_before_delimiter in three main ways. (i)
all-references, and real-time diagnostics that display errors and
                                                                              Normal RAG [29] employs similarity search with fixed-size chunk-
warnings as you type. It also offers hover-to-view documentation,
                                                                              ing, designed for unstructured natural language. (ii) Code-aware
symbol renaming, code actions for quick fixes, and refactoring.
                                                                              RAG, such as CodeRAG [44] incorporates code-specific features by
Since these capabilities are delivered through a unified protocol,
                                                                              employing AST-based chunking and codebase indexing. (iii) Static-
users can enjoy a consistent, IDE-grade experience across any LSP-
                                                                              analysis-based RAG, such as DraCo [8], enhances code-aware RAG
compatible editor with minimal configuration.
                                                                              by leveraging traditional program analysis techniques, such as data-
                                                                              flow analysis. Although RAG techniques have shown encouraging
                                                                              results, they still face limitations in retrieving the necessary context
                                                                              for unit test generation.
                                                                                 These limitations are exemplified in Figure 3 (c). Both Normal
2.2    Real-Time Unit Test Generation
                                                                              RAG and Code RAG were able to identify only partial dependen-
In today’s fast-paced software development, developers frequently             cies (e.g., nodes.py ) while missing other essential contexts (e.g.,
need to generate unit tests while writing code, especially when               pytree.py and tokens.py). This occurs because their retrieval is
working on incomplete or experimental features. The traditional ap-           based on an embedding-and-similarity algorithm, which depends
proach of writing tests after the code is complete can slow down de-          on textual information such as variable names, function names, and
velopment, particularly when dealing with rapidly evolving projects.          comments. These cues are often noisy and prone to variation across
This is because some function implementations may be incomplete               different coding styles and project conventions. Furthermore, they
or stubbed, which can temporarily leave the project not compil-               cannot isolate the relevant snippet and therefore feed the LLM large
able and complicate test generation. Real-time unit test generation           amounts of noise (e.g., 20,389 and 13,859 tokens) that hinders code
addresses this by enabling developers to generate tests concur-               generation. As the latest open-sourced technique for static-analysis-
rently with their code, even for incomplete or partial function im-           based RAG, DraCo addressed the above limitations by building an
plementations. Modern tools like GitHub Copilot [52] and Amazon               import graph to follow dependencies, yet notable drawbacks remain.
CodeWhisperer [50] leverage LLMs to create unit tests in seconds,             First, it is still prone to including noise. Because it cannot recognize
helping developers stay in their flow. These are integrated directly          which part of the imported library is used, it retrieves every im-
into IDEs, providing test candidates within well under a minute,              ported target, thereby including unnecessary context. For instance,
ensuring that the development process remains uninterrupted.
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                             Gwihwan Go, Quan Zhang, Chijin Zhou, Zhao Wei, and Yu Jiang


 # brakets.py                                                                      Ground Truth                Normal RAG                Code RAG            Dataflow - Guided RAG
 from blib2to3.pytree import Leaf, Node
                                                                              # nodes.py (line 760 ~ )     # brakets.py             # brakets.py             # token.py -
 ...
                                                                              def is_vararg(l, w):           ==> 2,863 Tokens         ==> 2,863 Tokens         ==> 640 Tokens
 def is_split_before_delimiter(leaf, previous) -> Priority:                                                                                                  from typing ...
                                                                                if l.type ...              LN = Union[Leaf, Node]   LN = Union[Leaf, Node]
    if is_vararg(leaf, within=VARARGS_PAR | UNPACKING_PAR):                                                                                                  ENDMARKER: Final = 0
                                                                                   return False            Depth = int              Depth = int
          # defined in nodes.py from 760 to 780, 76 to 91.                                                                                                   ...
                                                                              ...                          ...                      ...
           return 0
                                                                              VARARGS_PAR: Final           # lines.py               # comments.py
       if (                                                                                                                                                  # pytree.py
                                                                              ...                            ==> 10,007 Tokens        ==> 3,477 Tokens
           leaf.type == token.DOT # defined in token.py line 32                                                                                                ==> 2,690 Tokens
                                                                                                           @dataclass               @dataclass               class Base:
           and leaf.parent # defined in pytree.py line 66                     # pytree.py (line 66 )       class Line:              class ProtoCommnt:
           and leaf.parent.type not in {syms.import_from, syms.dotted_name}                                                                                  ...
                                                                              parent:                      ...                      ...
           and (previous is None or previous.type in CLOSING_BRACKETS)        Optional["Node"]= None
       ): #                # defined in nodes.py line 136 ↑↑                                               # nodes.py               # nodes.py               # nodes.py
           return DOT_PRIORITY                                                # token.py (line 32 )         ==> 7,519 Tokens         ==> 7,519 Tokens          ==> 571 Tokens
       # ... existing code ...                                                DOT: Final = 23              MATH_OPERAT:= {          MATH_OPERAT:= {          COMPARATORS: Final = {
       if leaf.value in LOGIC_OPERATORS and leaf.parent:                      ...                             token.VBAR,               token.VBAR,              token.LESS,
           return LOGIC_PRIORITY # ↑↑ defined in nodes.py line 49                                          ...                      ...                      ...
       return 0
                                                                                    368 Tokens                20,389 Tokens            13,859 Tokens             3,901 Tokens
                            (a) Focal Function                                (b) Condition Context        (c) Retrieved Context Comparison for Unit Test Generation


Figure 3: Illustrative example of existing work’s context retrieval in unit-test generation. (a) presents a simplified version of
the focal method; (b) displays the ground-truth condition context and its location; and (c) compares the context slices and the
number of tokens retrieved by three existing RAG techniques.


it loads all constant definitions from tokens.py when only a single                             Definition 4.4 (Token). A token 𝜏 is the smallest lexical unit recog-
constant, token.DOT, is required. Second, the implementation cost                            nised through LSP. We describe 𝜏 as the tuple
is prohibitive. Although DraCo’s retrieval accuracy is relatively                                            𝜏 = loc, lex, tok_kind ,
                                                                                                                                     
                                                                                                                                           𝑓 ∈ W.
high, constructing and maintaining these language-specific data-
flow graphs requires substantial manual effort, limiting DraCo to                            The 𝑓 denotes the file containing the token; loc is the character
codebases written in Python alone.                                                           location (𝑓 , 𝑜 start, 𝑜 end ); lex is the raw lexeme text; and tok_kind
    Our approach. Rather than hand-crafting language-specific                                indicates the lexical category (e.g., identifier, keyword, . . . ).
data-flow graphs, we simply reuse the static-analysis features of
LSP. Through the LSP, these services surface the exact, minimal                              4.2         Provider Interfaces
code fragment for requested symbols, in almost any mainstream                                In addition to the above concepts, we specify the four code-context
language, giving us precise context with minimal effort. The next                            providers implemented on top of LSP that LspRag invokes.
section details how LspRag turns this observation into practice.                               Definition 4.5 (Symbol Provider). The Symbol Provider, denoted
                                                                                             SYM, is a function that, given a file 𝑓 ∈ W, returns the set of all
4       Basic Concepts                                                                       symbols in 𝑓 that are not nested within another symbol.
This section formalises the four LSP providers used by LspRag. We
                                                                                                                                Ø
                                                                                                              SYM(𝑓 ) = Σ 𝑓 \        𝜎 ′ .children
introduce each concept in a top-down hierarchy—from workspace                                                                          𝜎 ′ ∈Σ 𝑓
to file, symbol, and token—so that their relationships are clear
before provider interfaces are stated.                                                       where Σ 𝑓 is the set of all symbols in file 𝑓 .
                                                                                                Definition 4.6 (Token Provider). The token provider, denoted TOK,
4.1        Workspace, File, Symbol, and Token                                                is a function that, given a location 𝑙𝑜𝑐𝑞 ∈ W, returns an ordered
   Definition 4.1 (Workspace). A workspace, denoted W, is a finite                           sequence of all tokens whose spans are contained within 𝑙𝑜𝑐𝑞 . Let
set of source files: W = { 𝑓1, . . . , 𝑓 | W | }.                                            𝑇𝑓 be the complete, ordered sequence of all tokens in file 𝑓 . The
                                                                                             function is defined as:
  Definition 4.2 (File). Each file 𝑓 ∈ W is an ordered sequence of
                                                                                                                        
                                                                                                              TOK 𝑙𝑜𝑐𝑞 = ⟨𝜏 ∈ 𝑇𝑓 | 𝜏 .loc ⊆ 𝑙𝑜𝑐𝑞 ⟩
characters and contains a finite set of symbols, Σ 𝑓 = {𝜎1, . . . , 𝜎 |Σ 𝑓 | }.
                                                                                             The output is a sequence, not a set, preserving the original order of
  Definition 4.3 (Symbol). A symbol 𝜎 is a named program entity,                             the tokens as they appear in the file.
such as a class, function, or constant, represented by the tuple                                Definition 4.7 (Definition Provider). A Definition Provider, denoted
                                                                                            DEF, is a function that maps a given token 𝜏 to the set of locations 𝐿𝜏
                   𝜎 = name, kind, loc, children .                                           of its corresponding definition symbols. This can be expressed as:
                                                                                                              (
Here, name is the identifier appearing in the source code; kind is                                              {𝜎.loc | 𝜎 is a definition for 𝜏 } if definitions exist
                                                                                             DEF(𝜏) = 𝐿𝜏 ≜
an enumerated tag (e.g., Class, Function, or Constant); loc is the                                              ∅                                  otherwise
inclusive character location (𝑓 , 𝑜 start, 𝑜 end ) of the symbol within its
file 𝑓 , start offset 𝑜 start , and end offset 𝑜 end ; and children⊆ Σ 𝑓 is                     Subsequent to the definition retrieval, resolving a location 𝑙 to a
the set of nested symbols whose spans lie strictly inside loc (e.g., a                       symbol 𝜎 involves finding the symbol within the file’s symbol set
method symbol is one of the children from its class symbol.)                                 from SYM(𝑙 .𝑓 ) that satisfies:
                                                                                                                        𝜎 ∈ SYM(𝑙 .𝑓 ) ∧ 𝜎.loc = 𝑙
LSPRAG: LSP-Guided RAG for Language-Agnostic Real-Time Unit Test Generation                                      ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil



    Workspace                                          Key Token Extraction    5.1     Key Token Extraction
                         AST
                                            CFG
                                                                               A primary challenge in context retrieval is that a focal method often
      Focal                                                  Key Tokens
                    Semantic Tokens        Analysis                            contains many tokens irrelevant to its core logic. Including context
     Method
                                                                               of these tokens can degrade the quality of the generated tests by
                                                                               retrieving non-essential context. To address this, we introduce the
                                                               RAG             concept of a key token, which is a token 𝜏 whose semantics are
      Other                              Definition
      Other
       Other
      Files                                                   Unit Test        essential for constructing high-coverage tests. Specifically, we de-
       Files          Language
        Files                                                Generation        fine key tokens as those that represent control-flow decisions or
                       Server            References
                                                                               external dependencies. To identify these tokens, LspRag performs
                                                                               a hybrid analysis that combines fine-grained lexical information
                                                        Unit Test Refinement   with a structural understanding, as illustrated in Figure 5.
       Unit                               Context
       Test           Diagnosis                              Test Repair       5.1.1 Lexical Information from LSP.. LspRag begins by invoking a
                                          Gathering
                                                                               token provider, TOK (Definition 4.6), to retrieve a sequence of all
                                                                               tokens within the scope of the focal method’s location, 𝑙𝑜𝑐𝑚 .
                                                                                                       ⟨𝜏1, 𝜏2, . . . , 𝜏𝑛 ⟩ = TOK(𝑙𝑜𝑐𝑚 )
                Figure 4: Overall workflow of LspRag.
                                                                               Each token 𝜏 in this sequence includes its location, lexical name,
                                                                               and a semantic role, such as parameter or identifier. This in-
Note that the file containing the definition, 𝑙 .𝑓 , may reside outside        formation is necessary for the subsequent context retrieval phase,
of the current workspace W, for instance, within an external library           because the context provider on top of LSP accepts input as a spe-
or a standard system header.                                                   cific location of a token. Additionally, based on semantic role, one
   Definition 4.8 (Reference Provider). The reference provider, de-            can filter out unnecessary tokens, such as constants. While this
noted REF, performs the inverse operation of the definition provider.          lexical information is useful, it is insufficient on its own because it
Given a token 𝜏, it finds all tokens in the workspace that refer to            lacks structural context. For example, tokens like “if” and “def” are
the same definition. Let 𝜎def indicates the definition symbol for the          both classified simply as “Keyword” by TOK, despite their different
token 𝜏. The function is defined as:                                           structural implications for control flow. The LSP-oriented solution
                                     Ø                                         cannot resolve this limitation, since it is designed for editor-centric
                
                
                
                 {𝜏 ′ .loc | 𝜏 ′ ∈      𝑇𝑓                                    features, not compiler-level control-flow analysis1 . Consequently,
                
                
                                   𝑓 ∈𝑊               if 𝜎def ≠ null          relying solely on LSP features is insufficient for identifying the key
      REF(𝜏) =                           ′
                
                              ∧  DEF(𝜏    ) = 𝜎 def }                         tokens needed for high-coverage test generation.
                
                ∅
                
                                                       if 𝜎def = null
                                                                              5.1.2 Structural Analysis via AST.. To overcome the limitations of
The output is a set of locations, each corresponding to a token that           the LSP, LspRag leverages the Abstract Syntax Tree (AST). The AST
references the same definition symbol.                                         provides a language-agnostic structural view that is essential for
                                                                               understanding program hierarchy and can be easily implemented
5    Design of LspRag                                                          in a language-agnostic way, which is crucial for multi-language
This section presents the design of LspRag, an enhanced RAG                    support. The effectiveness of this technique has been demonstrated
framework for multi-language real-time unit test generation. As                in prior RAG research [8, 49]. LspRag reuses widely-used Tree-
illustrated in Figure 4, LspRag consists of three core modules that            sitter [53] to construct a AST for focal method. The critical step in
operate on a developer’s workspace W. We assume that a developer               this process is to bridge the structural AST view with the lexical
is working on a focal method within a file 𝑓 ∈ W, which may have               LSP tokens. To achieve this, LspRag preserves the precise source
dependencies on various symbols defined in other files.                        code location (i.e., line and column numbers) of every node during
    Upon a developer’s request to generate a unit test, LspRag begins          AST construction. This allows for a precise mapping between an
with Key Token Extraction module. This module is responsible                   AST node and its corresponding set of tokens if the node’s location
for identifying a set of key tokens within the focal method. These             span contains the tokens’ locations.
tokens are pivotal in guiding the generation of high-coverage test
                                                                               5.1.3 Key Token Identification. With the combined data, the tool
cases as they typically govern the method’s control flow and its in-
                                                                               constructs a lightweight, language-agnostic Control-Flow Graph
teractions with external components. Subsequently, these extracted
                                                                               (CFG) for the focal method. The CFG enables path-sensitive anal-
tokens are passed to the RAG Module. This module leverages DEF
                                                                               ysis to identify the final set of key tokens, 𝑇key . At a high level, a
and REF providers to gather contextual information, including defi-
                                                                               token 𝜏 from the focal method is added to 𝑇key if it participates in
nitions and usages of the key tokens. This context is then used to
                                                                               or affects the change of a conditional expression that determines
construct a detailed prompt that is fed to an LLM. Finally, to address
                                                                               a branch in the CFG. Specifically, we first identify tokens 𝜏 ′ that
potential syntactic errors in the generated test code, the Unit Test
                                                                               participate in a conditional expression. Next, we filter out the token
Refinement module inspects the test code without compilation.
                                                                               sequence TOK(𝑙𝑜𝑐𝑚 ) that does not need a context search by ex-
If any potential errors are detected, it gathers the necessary con-
                                                                               cluding tokens with semantic roles such as Keyword, Identifier,
text for remediation and feeds this information back to the LLM to
correct the code.                                                              1 https://github.com/microsoft/language-server-protocol/issues/1675
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                                            Gwihwan Go, Quan Zhang, Chijin Zhou, Zhao Wei, and Yu Jiang


 def is_split_before_delimiter(leaf, previous) -> Priority:                                                  𝑙𝑜𝑐𝑟′ ∈ 𝐿refs (e.g., a variable in an expression) is often insufficient,
    leaf.type = token.DOT
    if is_vararg(leaf, within=VARARGS_PAR | UNPACKING_PAR):                                                  as it only points to the token at other file without its surrounding
        # defined in nodes.py from 760 to 780, 76 to 91.
        return 0
                                                                                                             context. To create a meaningful example, LspRag enriches each
    if (                                                                                                     reference. For each location 𝑙𝑜𝑐𝑟′ ∈ 𝐿refs , the tool identifies the
        leaf.type == token.DOT # defined in token.py line 32
        and leaf.parent # defined in pytree.py line 66                                                       smallest symbol 𝜎enclosing that fully contains the reference location
        and leaf.parent.type not in {syms.import_from, syms.dotted_name}                                     (𝑙𝑜𝑐𝑟′ ⊆ 𝜎enclosing .loc). This is achieved by retrieving all top-level
        and (previous is None or previous.type in CLOSING_BRACKETS)
    ): #                # defined in nodes.py line 136 ↑↑                                                    symbols in the reference’s file 𝑙𝑜𝑐𝑟′ .𝑓 through SYM and then recur-
        return DOT_PRIORITY
    # ... existing code ...
                                                                                                             sively searching their children. The source code of 𝜎enclosing is then
                                                                                                             extracted, transforming a simple location into a complete usage
    Semantic Tokens Under Focal Method
                                                                                                             example (e.g., the entire function that uses the token 𝜏), which
                                                                            CFG
 1. is_split_before_delimiter( ... )                                                                         demonstrates how the symbol is used in other locations.
 2. leaf ( loc, lex, tok_kind),                                   Function Node
 3. previous ( ... ),                                             Text: is_split
 4. Priority ( ... ),                                             Range: ...                                 5.2.2 Prompt Construction. The final step synthesizes the retrieved
 5. leaf                                                                                                     information into a structured prompt for the LLM. This prompt
 6. type            Co-located with              Condition Node             Condition Node             ...
 7. token           10. leaf
                                                 Text: is_vararg             Text: (\n\t\tleaf.ty...
                                                                                                             is designed to guide the LLM in generating comprehensive unit
 8. DOT
                                                 Range: ...                  Range: ...                      tests and consists of three parts: (1) The full source code of the
 9. is_vararg ( ... ),
 10. leaf ( ... ),
                                                                                                             focal method to be tested. (2) The definitions and references of
                                                  Return Node                  Return Node             ...
 11. within ( ... ),
 12. VARARGS_PAR ( ... ),                        Text: return 0              Text: return ...
                                                                                                             the key tokens retrieved previously. (3) A lightweight unit-test
 13. UNPACKING_PAR ( ... ),                      Range: ...                  Range: ...                      template with necessary import statements and class or function
 ...
                                                                                                             structures inferred from the focal method’s file. This structured
 Key Tokens : { ..., is_vararg, leaf, within, VARARGS_PAR, UNPACKING_PAR, leaf, type,                        prompt provides the LLM with focused and relevant information,
                                   token, DOT ... }
                                                                                                             minimizing noise that can degrade code generation quality and
                                                                                                             empowering it to produce accurate and thorough unit tests. Due to
Figure 5: This figure illustrates the key token selection pro-                                               page limitations, we provide the full prompt format in our artifact,
cess. The red box highlights how key tokens are identified.                                                  which is open-sourced. The prompt is designed using CoT [58] with
Using the lexical information and CFG, LspRag identifies                                                     a one-shot setting [6].
those tokens involved in or influencing branch decisions.
                                                                                                             5.3      Unit Test Refinement
Literal, Comment, String, and Regex. In general, these tokens are                                            While LLMs excel at code generation, their output can be imperfect,
either constants or syntax keywords that do not require a context                                            containing syntactic errors that cause compilation failures. To ad-
search. Then, we extract tokens from TOK(𝑙𝑜𝑐𝑚 ) that appear on                                               dress this, LspRag employs an automated refinement module that
the same line as the token 𝜏 ′ and add them to 𝑇key . The resulting set                                      detects and repairs them. This process operates in two phases: (1)
𝑇key represents the tokens most likely to affect the focal method’s                                          real-time error detection and (2) context-aware error repair.
execution path. It is then passed to the subsequent RAG module.
                                                                                                             5.3.1 Real-Time Error Detection. LspRag leverages the diagnostic
5.2      RAG                                                                                                 capabilities of the LSP to perform immediate analysis on the gen-
                                                                                                             erated code. In detail, when code is modified within a file 𝑓 ∈ 𝑊 ,
This module is designed for precise context retrieval for the set
                                                                                                             LspRag notifies the corresponding language server. The server, in
of key tokens, 𝑇key , identified in the previous stage. To achieve
                                                                                                             turn, analyzes the file and returns a set of diagnostics. Each diagnos-
this, LspRag systematically queries the LSP’s DEF (Definition 4.7)
                                                                                                             tic is a tuple (𝑚, 𝑙𝑜𝑐), where 𝑚 is a human-readable error message
and REF (Definition 4.8) for each token in 𝑇key and assembles the
                                                                                                             (e.g., “undefined variable ’x”’) and 𝑙𝑜𝑐 is the location of the code that
retrieved information into a coherent prompt.
                                                                                                             triggers the error. This mechanism provides instantaneous feedback
5.2.1 Context Retrieval. To retrieve a token’s definition, LspRag                                            without requiring a project compilation or code execution, which
invokes the DEF to find the location where the token is defined,                                             is critical for real-time context.
which we denote as 𝑙𝑜𝑐 def . By default, DEF resolves symbols across
the entire project space, including standard and third-party libraries.
To maintain contextual relevance, LspRag filters these results, con-
                                                                                                              Table 1: Error Categories Grouped by Necessary Context
sidering only definitions within the current workspace W. This
prevents the inclusion of unnecessary definitions from standard
                                                                                                              Error Category                       Frequency   Context Needed for Fix
libraries (e.g., String, Integer). This filtering is expressed as:
                                                                                                              Redeclaration/Duplicate Definition     28 300    Workspace-level context
  process 𝑙𝑜𝑐 def only if 𝑙𝑜𝑐 def .𝑓 ∈ W, where 𝑙𝑜𝑐 def = DEF(𝜏 .𝑙𝑜𝑐)                                         Import/Module Resolution Error         13 517    (e.g., project structure)
                                                                                                              Member Access/Usage Error              13 387
If a valid definition location is found, LspRag first locates 𝜎def at                                                                                          Symbol-level context
                                                                                                              Type Mismatch/Compatibility Error       4388
                                                                                                                                                               (e.g., context of a specific symbol)
𝑙𝑜𝑐 def and then extracts the source code from 𝜎def .𝑙𝑜𝑐.                                                     Constructor Call Error                  1670
   Next, to find usage examples, LspRag queries the REF to find all                                           Syntax Error                            5467
                                                                                                                                                               No external context required
                                                                                                              Unhandled Exception                      179
use-sites of the token’s symbol within the workspace W. We de-
                                                                                                              Total                                  66908
note 𝐿refs as the queried result of REF(𝜏). A raw reference location
LSPRAG: LSP-Guided RAG for Language-Agnostic Real-Time Unit Test Generation                                    ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


5.3.2 Context-Aware Error Repair. Upon receiving a set of non-                    LspRag currently offers two main features for unit test gener-
empty diagnostics, LspRag initiates the repair phase. The core                ation. The first is method-level test generation, which automati-
challenge in automated code repair is providing the LLM with                  cally generates a unit test class for a given focal method. Such a
sufficient and relevant context to understand and fix the error.              class contains multiple test functions, each designed for a unique
   To determine the optimal context for different error types, We             execution branch within the focal method. The second feature,
constructed the dataset (Table 1) ourselves by collecting 70k errors          branch-targeted test generation, allows developers to select a spe-
across Java, Python, and Golang, since no dataset exists for LLM-             cific conditional branch within a focal method and generates a set of
generated code paired with error messages. These errors were                  test cases specifically designed to exercise the logic of that branch.
generated by prompting diverse LLMs to produce test cases for
different projects (including those used in evaluation), and then             7      Evaluation
diagnosing them via the LSP-based workflow. After collection, we              In this section, we comprehensively evaluate LspRag’s performance
manually analyzed the errors, identifying their root causes and the           on real-world projects across different programming languages. Our
contextual information helpful in fixing them. This information is            evaluation investigates the following questions:
general rather than tied to specific projects. For instance, “imported        • RQ1(§7.2): Can LspRag generate higher coverage unit tests than
and not used” consistently indicates import-related issues, while                other baselines?
“redeclared in this block” points to symbol redeclaration errors.             • RQ2(§7.3): Does LspRag maintain low latency and efficient token
Based on the analysis result, LspRag gathers the corresponding                   usage during generation?
necessary context by invoking the providers implemented on top                • RQ3(§7.4): How much does each pipeline component of LspRag
of LSP. For a given diagnostic (𝑚, 𝑙𝑜𝑐𝑒𝑟𝑟 ), LspRag collects context             contribute to test coverage?
as follows:
• Symbol-Level Context: For errors related to a specific symbol               7.1      Experiment Setup
  (e.g., undefined variables, incorrect method calls), LspRag re-             Benchmarks. Our evaluation is conducted on six open-source
  trieves its definition and usage examples. It invokes DEF to fetch          projects written in Python, Java, and Golang. Python and Java were
  the canonical definition and REF to find usage examples for the             selected due to their common use in prior unit test generation
  tokens at 𝑙𝑜𝑐𝑒𝑟𝑟 , providing the LLM with both the ground-truth             research. Golang was chosen as it is widely adopted in industry
  specification and concrete examples of correct usage.                       but less examined in academic studies, which we anticipated would
• Workspace-Level Context: For errors involving project struc-                present different challenges for LLMs. As shown in Table 2, we
  ture (e.g., missing imports), a broader view of the project is nec-         selected two projects per language, all of which are frequently used
  essary. LspRag provides this by supplying: (1) the workspace’s              as benchmarks in the unit test generation domain [28, 40, 56, 57, 60].
  file structure and (2) a list of top-level symbols (e.g., classes,
  functions) in the file where the error occurred (𝑙𝑜𝑐𝑒𝑟𝑟 .𝑓 ).
                                                                                                     Table 2: Dataset Statistics
   Finally, LspRag constructs a prompt containing the erroneous
code, the diagnostic message 𝑚, and the retrieved context. This
process is iterative: after the LLM proposes a fix, LspRag re-triggers            Project            Domain                             Version     Language
the diagnostic mechanism. This loop continues until all diagnostics               Black [20]         Code formatter                      8dc9127      Python
                                                                                  Tornado [14]       Network/Web framework              81d36df1      Python
are resolved or a predefined number of attempts is reached.
                                                                                  Commons-CLI [18]   Command line interface parser      266ab84a       Java
                                                                                  Commons-CSV [19]   Library for processing CSV files   ca3a95c3       Java
6    Implementation                                                               Cobra [21]         Framework for creating Go CLI       ceb39ab      Golang
                                                                                  Logrus [51]        Structured logging library         d1e6332       Golang
We implemented a prototype of LspRag in TypeScript, comprising
approximately 22k lines of code out of 8k lines of unit test code.
The implementation was guided by two primary goals: developer                    Baseline Selection. To evaluate the performance of LspRag,
usability and language generalizability.                                      we selected four baselines, comprising three RAG techniques and
   To enhance usability, LspRag was implemented as a VS Code                  one prompt engineering method.
extension, which integrates seamlessly into the developer’s ex-               • RAG: A normal RAG with OpenAI embeddings and FAISS index
isting workflow and reduces the barriers to adoption. The tool                  via LangChain. It retrieves the top 3 most similar snippets based
leverages the VS Code Extension API, which provides comprehen-                  on cosine vector similarity.
sive capabilities for user interface interactions, editor functionality,      • CodeQA [49]: An open-source RAG pipeline designed for code
and command handling. To achieve language generalizability, we                  generation. Its approach, which involves indexing the codebase
designed LspRag to be language-agnostic. It leverages the LSP to                and parsing code structure with an AST, is analogous to that used
consume semantic information from any compliant language server                 in modern AI-assisted IDEs like Cursor [3].
and utilizes Tree-sitter [53] for robust source code parsing into an          • DraCo [8]: A RAG pipeline integrated with program analysis.
AST. Consequently, LspRag is compatible with any programming                    Although it is specific to Python, this tool’s use of static analysis-
language supported by an LSP server and Tree-sitter. We have vali-              guided retrieval plays a comparable baseline for evaluating the
dated LspRag’s functionality with several major language servers,               context retrieval capabilities of LspRag.
including Pylance for Python [42], the Oracle Extension Pack for              • SymPrompt [47]: A prompt engineering technique for unit test
Java [45], and the official Go extension [26].                                  generation. It proposes a novel prompt format that translates
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                          Gwihwan Go, Quan Zhang, Chijin Zhou, Zhao Wei, and Yu Jiang


Table 3: Comparison of line coverage and valid rate across all baselines. Our approach, LspRag, consistently outperforms all
baselines, achieving higher scores across diverse projects and models. Missing values (–) indicate that the baseline does not
support test generation for those projects.

                                                          Coverage                                              Valid Rate
 Project        Model
                                CodeQA           RAG     SymPrompt   LspRag   DraCo     CodeQA        RAG      SymPrompt         LspRag       DraCo
                GPT4o-m           34.92%        26.29%     22.09%    41.91%   32.58%      55.57%     37.26%        66.35%         79.73%       54.52%
  Black         GPT4o             40.47%        29.94%     23.99%    48.10%   35.33%      79.46%     77.53%        59.87%         85.15%       73.31%
                DS-v3             46.03%        38.98%     34.18%    56.89%   37.64%      59.26%     72.24%        75.18%         88.03%       71.04%
                GPT4o-m           29.04%        49.44%     31.44%    57.78%   46.54%      71.26%     64.30%        77.01%         81.84%      75.82%
Tornado         GPT4o             29.97%        46.29%     34.35%    60.90%   41.09%      80.14%     83.95%        72.82%         84.53%      85.03%
                DS-v3             38.45%        54.05%     50.78%    64.62%   48.99%      85.93%     81.84%        85.30%         91.13%      90.48%
         GPT4o-m                  10.63%         5.02%      2.76%    33.29%     –         12.40%      8.18%         7.05%         45.08%          –
 Commons
         GPT4o                     9.60%         3.21%      3.00%    34.69%     –          8.23%      7.27%         7.20%         48.12%          –
  CLI
         DS-v3                    20.72%        17.68%      5.62%    37.72%     –         13.29%     14.55%         9.21%         60.52%          –
         GPT4o-m                  40.97%        24.93%     18.50%    80.51%     –         23.64%     13.20%         6.28%         82.85%          –
 Commons
         GPT4o                    44.85%        44.84%     25.28%    78.33%     –         20.68%     26.53%        14.41%         90.90%          –
  CSV
         DS-v3                    65.11%        44.68%     35.07%    83.20%     –         43.27%     32.24%        29.82%         90.95%          –
                GPT4o-m            7.11%        12.03%      3.39%    23.03%     –          6.01%      9.50%         1.23%         23.88%          –
  Cobra         GPT4o             10.05%         7.57%      0.22%    27.60%     –          9.70%      8.12%         0.81%         33.27%          –
                DS-v3             15.50%        13.01%      8.57%    37.22%     –         10.30%     10.69%         2.78%         34.65%          –
                GPT4o-m            5.52%        11.14%      0.23%    23.71%     –         14.32%     20.83%         0.83%         34.02%          –
 Logrus         GPT4o              5.61%        13.09%      0.23%    27.75%     –         14.17%     26.52%         0.83%         32.02%          –
                DS-v3             11.34%        11.00%      5.43%    21.81%     –         13.33%     15.83%         7.5 %         33.11%          –


   CFG paths into descriptive comments, thereby improving the                 resulted in 299 focal methods for Black, 521 for Tornado, 101 for Co-
   readability and structure of the generated tests. We replicated            bra, 24 for Logrus, 43 for Commons-CLI, and 145 for Commons-CSV.
   this prompt format using our own CFG.                                      To ensure reliable results, we repeated each experiment five times
   Model Selection and Environment. Our evaluation utilizes                   and report the average values. We configured LspRag to perform a
three LLMs to assess LspRag’s performance across different ar-                maximum of five self-correction iterations.
chitectures and scales. We selected GPT-4o [17] and its smaller                  Statistical Analysis. To verify the significance of our findings,
variant, GPT-4o-mini (GPT4o-m), to represent the transformer archi-           we performed statistical tests on the results. We computed p-values
tecture. To test against a different model design, we also included           to assess the significance of the improvements and reported effect
Deepseek-V3 [34] (DS-v3), which is based on a Mixture-of-Experts              sizes to quantify their magnitude, following the guidelines from
architecture. The experiments were conducted on a server run-                 Arcuri et al [4]. The null hypothesis (𝐻 0 ) posits that there is no
ning Ubuntu 22.04 LTS, equipped with a 128-core AMD EPYC 7763                 statistically significant difference in line coverage between LspRag
CPU and an NVIDIA V100 GPU featuring 32GB of memory. For                      and the baselines. Conversely, the alternative hypothesis (𝐻 1 ) states
all language models, we used the default generation parameters,               that LspRag achieves a statistically significant improvement.
including temperature, to ensure a consistent baseline.                          Results. The overall results, presented in Table 3, show that
                                                                              LspRag consistently improves line coverage across all projects, re-
                                                                              gardless of the programming language or the underlying LLM. Our
7.2      Generation of High Coverage Unit Tests                               statistical analysis confirms that these improvements are significant,
To answer RQ1, we evaluated LspRag’s ability to generate high                 with all p-values being less than 0.05, thus supporting the 𝐻 1 . This
coverage unit tests against selected baselines. We measured per-              finding highlights the effectiveness of LspRag’s context retrieval
formance using two key metrics: line coverage to quantify test                and code correction mechanisms. The following analysis examines
effectiveness, and valid rate to assess the proportion of syntacti-           the specific design choices in the baselines that may contribute to
cally correct, usable tests. We define the valid rate as the ratio of         this performance gap.
grammatically correct test cases to the total number of unit test                While SymPrompt is designed to guide an LLM in generating
generation attempts. Since invalid test cases are not compilable or           tests for specific conditions specified within comments, we found
executable, they cannot produce any coverage.                                 its effectiveness in our experiments to be limited by the absence
   Evaluation Setup. For each project listed in Table 2, we gen-              of code dependency information. We observed that its complex
erated unit tests for methods exceeding 10 lines of code, as these            prompt structure, when not grounded with the necessary context,
typically contain complex logic that is difficult to fully cover. This
LSPRAG: LSP-Guided RAG for Language-Agnostic Real-Time Unit Test Generation                                   ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


complicated the LLM’s generation process. This suggests that the              Table 4: Overall token usage distribution and comparison.
approach is robust but requires sufficient contextual input to steer
the LLM effectively, and without it, it can struggle to match the                       Method       Java      Golang       Python      Averaged
performance of simpler methods.                                                         LspRag - Breakdown
   The RAG-based approaches (RAG, CodeQA, and DraCo) showed                               GEN         2,144      3,379       2,674         2,732
                                                                                          FIX         3,252      1,458        586          1,832
varied performance, highlighting different trade-offs in context
retrieval. For instance, DraCo is a sophisticated tool employing                        Total Token Usage Comparison
                                                                                        LspRag        5,396    4,837         3,260         4,497
dedicated static analysis for Python. While effective, its reliance on                  CodeQA 11,720          4,831         5,466         7,339
import statements for dependency analysis means it can sometimes                        RAG           3,790    4,006         4,582         4,126
miss crucial intra-file context, such as helper functions or constants                  DraCo           –        –           2,439           –
defined in the same file. On the other hand, CodeQA and RAG are
designed to retrieve full code snippets of functions or classes, in-
cluding intra-file context. This approach, however, sometimes led to          Table 2 using the GPT4o API, following the same experimental setup
an excess of retrieved context, particularly in larger projects, such         as in §7.2. For each focal method, we measured the time and tokens
as Tornado. This frequently caused the context to exceed the LLM’s            consumed across all processes of the LspRag pipeline, including a
token limitation, resulting in the loss of potentially important in-          maximum of five self-correction attempts. The results of latency,
formation. Interestingly, our simpler baseline RAG, which retrieves           averaged by programming language, are detailed in Figure 6.
a maximum of three code snippets, often performed better than the                On average, our tool requires 28.27 seconds and 4,497 tokens
more complex RAG tools, suggesting that a more constrained and                per focal method to generate and refine a unit test. As detailed
focused context can be more effective than a larger, unverified one.          in 6, the majority of this time (approximately 70%) is spent on LLM
   LspRag’s strong performance stems from two primary mecha-                  API querying for generation and refinement. Our retrieval strategy,
nisms. First, for higher coverage, LspRag leverages LSP features              which includes key token extraction and leveraging the LSP for
like "go to definition" and "find references" to construct a precise          reference and definition providers, accounts for about 5 seconds of
semantic dependency graph. This provides the LLM with a com-                  the total time. While the refinement stage constitutes over 30% of
plete yet concise context, avoiding the noise of generic RAG and              the generation time, we consider this a necessary and acceptable
the intra-file blind spots of other methods. Second, to achieve a             trade-off for the improvements it yields in both line coverage and
higher valid rate, LspRag utilizes real-time diagnostics on top of            the rate of valid tests.
LSP to detect and correct syntactic errors in the generated code                 As shown in Table 4, LspRag averagely uses 2,732 tokens for
iteratively. This self-correction loop consistently improves the valid        the initial generation and 1,832 for fixing. While LspRag’s token
rate of generated test cases, as evidenced by the consistently high           consumption is not the lowest in all cases, we consider the gains in
valid rates in Table 3. The specific contribution of these LSP-driven         coverage justify the trade-off. For instance, compared to CodeQA,
features is quantified in our ablation study (§7.4).                          LspRag uses 39% fewer tokens while achieving a 135% improvement
   The improvement in the valid rate for the Python projects (Black           in coverage. When measured against DraCo, LspRag uses 9.6%
and Tornado) was less obvious than for the Java and Golang projects.          more tokens for generation and 24% more for fixing, but these
This is an expected outcome, as Python is a dynamically typed                 increases yield coverage improvements of 30% and an additional
language, which limits the language server’s ability to catch all             6%, respectively. Furthermore, LspRag demonstrates its efficiency
potential errors statically before execution. Conversely, for projects        against a RAG approach, delivering a 174% coverage improvement
written in statically-typed languages like Java and Go, LspRag                with an 8.9% increase in total tokens used for generation and fixing.
consistently delivered significant improvements in validity rates
because the language server could identify a broader range of po-                                                                             REF : 295
                                                                                                                                              Build CFg : 217

tential errors.                                                                                                                               DEF : 417
                                                                                                                                              REF : 277
   We did not include Copilot in our experiments because it heav-                                                                             Build CFg : 3.2



ily relies on human interaction during the unit test generation. In                                                                                REF : 244
                                                                                                                                                   Build CFg : 344

detail, it requires manual clicks to trigger its functionality, which
prevents large-scale automated experimentation as it does not pro-
vide automated APIs for programmatic code generation [10, 11].
Furthermore, it assumes that users will perform context collection
and error correction during interaction, introducing human factors
that make fair and consistent evaluation difficult.                           Figure 6: Test generation cost distribution per focal method,
                                                                              classified by programming languages.
7.3    Latency and Cost
For a code generation tool to be practical in an interactive develop-
ment workflow, it must operate with acceptable latency and cost.              7.4    Ablation Study
To answer RQ2, we assess whether LspRag meets this real-time                  To answer RQ3, we conducted an ablation study to isolate and
requirement by measuring its performance overhead in terms of la-             quantify the contribution of each of LspRag’s core components.
tency and cost. The evaluation was conducted on the projects from             We evaluated three configurations, with same setup from §7.2:
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                      Gwihwan Go, Quan Zhang, Chijin Zhou, Zhao Wei, and Yu Jiang


Table 5: Comparison of valid rate and line coverage across                             languages. Nevertheless, the fixing module proves its general utility
different versions of LspRag. This shows that each compo-                              by consistently enhancing both the validity and coverage of gener-
nent of LspRag shows meaningful improvement both on                                    ated tests across all three languages, demonstrating that real-time
coverage and valid rate.                                                               correction is a crucial component for robust test generation.

                                  Coverage                       Valid Rate            8      Discussion
 Project     Model
                         Naive    LspRag −    LspRag    Naive     LspRag −    LspRag   Fault-Finding Capability. While LspRag is designed to maximize
             GPT4o-m    22.72%     39.51%      41.91%   57.32%     72.04%     79.73%   test coverage, it does not explicitly optimize for the quality of test
  Black      GPT4o      23.56%     42.30%      48.10%   56.58%     77.99%     85.15%   assertions. Since effective assertions are critical for detecting faults,
             DS-v3      39.74%     53.36%      56.89%   75.62%     87.02%     88.03%
                                                                                       we conducted an experiment to evaluate this capability. We injected
             GPT4o-m    27.52%     56.72%      57.78%   67.14%     81.54%     81.84%
                                                                                       faults into the source code using standard mutation tools (Pit [9] and
 Tornado     GPT4o      29.55%     60.03%      60.90%   54.36%     82.00%     84.53%
             DS-v3      46.04%     63.70%      64.62%   89.56%     90.36%     91.13%   MutPy [16]) and measured whether the generated tests could detect
             GPT4o-m     4.59%     27.10%      33.29%   13.40%     23.49%     45.08%
                                                                                       them. As summarized in Table 6, LspRag consistently outperforms
 Commons
         GPT4o          12.71%     23.16%      34.69%   32.61%     28.59%     48.12%
  CLI
             DS-v3       6.46%     28.77%      37.72%   17.20%     31.32%     60.52%   Table 6: Comparison of mutation scores across all baselines.
             GPT4o-m    26.70%     69.77%      80.51%   15.74%     37.43%     82.85%
 Commons
         GPT4o          39.16%     76.05%      78.33%   35.69%     54.45%     90.9 %
  CSV                                                                                      Project   Model     LspRag   SymPrompt   CodeQA    StandardRAG    DraCo
             DS-v3      32.67%     75.29%      83.20%   36.76%     49.29%     90.95%
                                                                                                     DS-v3     25.21%     12.75%     11.85%       5.03%       7.73%
             GPT4o-m     1.36%      9.91%      23.03%    1.19%      7.13%     23.88%
                                                                                           Black     GPT4o     30.28%     21.04%     18.47%       9.69%      17.03%
  Cobra      GPT4o       2.72%     12.56%      27.60%    1.79%      8.91%     33.27%                 GPT4o-m   31.90%     15.01%     8.18%        2.31%       8.71%
             DS-v3      11.58%     25.61%      37.22%    9.13%     21.78%     34.65%
                                                                                                     DS-v3     35.39%     1.46%      2.03%        21.16%      2.03%
             GPT4o-m     2.32%     11.55%      23.71%    3.33%     18.86%     34.02%       Tornado   GPT4o     30.37%     9.11%      7.66%        18.16%     21.69%
 Logrus      GPT4o       0.65%     10.58%      27.75%    0.83%     15.00%     32.02%                 GPT4o-m   24.96%     5.15%      13.62%       9.28%      15.68%
             DS-v3      10.67%     13.55%      21.81%   22.50%     17.05%     33.11%
                                                                                                   DS-v3       19.67%     3.22%       4.21%       12.73%         —
                                                                                           Commons
                                                                                                   GPT4o       19.01%     1.32%       7.19%       0.41%          —
                                                                                            CLI
                                                                                                   GPT4o-m     19.92%     0.08%       1.40%       0.74%          —

• Naive: A baseline using the same prompt template as LspRag                                       DS-v3       58.50%     11.75%     39.63%       17.63%         —
                                                                                           Commons
                                                                                                   GPT4o       50.50%     0.25%      9.38%        5.63%          —
  but without LSP-guided context or code fixing.                                            CSV
                                                                                                   GPT4o-m     50.13%     1.13%      7.63%        2.75%          —
• LspRag− : The baseline enhanced with our context retrieval on
  top of LSP features.
• LspRag: The complete LspRag system, incorporating both con-                          the baselines, suggesting that its accurate context retrieval not only
  text retrieval and the real-time code fixing module.                                 boosts coverage but also enhances fault detection.
                                                                                          Comparison with SBST Tool. To contextualize the perfor-
   The results, averaged over five runs and presented in Table 5,                      mance of our LspRag, we conducted a direct comparison with
reveal two key findings. First, context retrieval is crucial for gen-                  EvoSuite, a widely-used SBST tool for java. For fair comparison,
erating comprehensive tests. As shown in Table 5, adding context                       EvoSuite was configured to generate unit tests per method under
(LspRag− ) substantially increases line coverage over the Naive base-                  a fixed time budget of 28 seconds per method under test. The re-
line across all projects and LLMs. Specifically, LspRag− improved                      sults are summarized in Table 7. The results indicate that LspRag
line coverage by 26% to 1528% for Golang, 82% to 490% for Java,
and 34% to 106% for Python. This demonstrates that the precise,                              Table 7: Comparison with EvoSuite on Java projects.
semantically aware context provided by our context retrieval on top
of the LSP module enables the LLM to understand class structures,
method dependencies, and necessary initializations.                                                                 Coverage                Valid Rate
                                                                                              Project
   Second, the real-time fixing module is vital for maintaining cor-                                            LspRag EvoSuite          LspRag EvoSuite
rectness, especially when the context is complex. While rich context                          Commons-CLI       37.72%      56.33%       60.52%           100%
boosts coverage, it can be a double-edged sword. For instance, with                           Commons-CSV       83.20%      69.70%       90.95%           100%
a complex project like Commons-CLI, the large volume of context
can distract the LLM, leading to syntactically incorrect code and a
lower valid rate for LspRag− . The full LspRag system mitigates this                   achieves competitive code coverage against EvoSuite. EvoSuite con-
issue. By adding the fixing module, LspRag improved line coverage                      sistently achieves a 100% valid generation rate. This is an expected
by an additional 45% to 162% for Golang, 3% to 49% for Java, and                       outcome, as its test generation process is rooted in a strict code mu-
1% to 13% for Python over LspRag− . More importantly, it increased                     tation strategy that inherently guarantees syntactically correct and
the valid rate by 59% to 273% for Golang, 67% to 121% for Java,                        compilable tests. In contrast, LspRag is designed with a different
and 0.5% to 10% for Python. The improvements for Python are less                       primary goal: to support multiple languages through a lightweight
pronounced, which is an expected outcome due to the language’s                         static analysis framework. This design choice involves a trade-off,
dynamic nature. Python’s dynamic nature means that its LSP diag-                       where we sacrifice a guaranteed valid rate for broader applicability
nostics, which rely on static analysis, cannot detect certain error                    and scalability. Nevertheless, the result demonstrates that LspRag
classes that would cause compile-time failures in statically-typed                     still delivers coverage results that are comparable to EvoSuite.
LSPRAG: LSP-Guided RAG for Language-Agnostic Real-Time Unit Test Generation                                ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


   Threats to Validity. We identify two primary external threats              previous work in terms of latency and coverage, they are still inap-
to the generalizability of our approach. First, the effectiveness of          propriate for real-time scenarios. Furthermore, both classical and
LspRag is inherently coupled with the correctness of the underlying           many LLM-based approaches are tailored for specific programming
LSP server implementation for a given language. Our approach                  languages (e.g., Java and Python), limiting their generalizability.
relies on the LSP server to provide accurate static analysis results             Retrieval-Augmented Generation. RAG [27, 30] mitigates
(e.g., definitions, references, and type hierarchies). Consequently, if       LLM’s limitation of having finite training data. Initially proposed
a programming language lacks robust LSP support, or for servers               for NLP, it has been widely applied to code, notably through
with erratic or incomplete analysis capabilities, the quality of the          repository-level techniques. These use code-specific features for
retreived context would be degraded, potentially impacting the                context retrieval, such as AST-based chunking [31, 39, 49] or
quality of the generated code. Second, the behavior of LspRag can             program-analysis-based retrieval [7, 36, 37, 64]. Repository-level
be influenced by environment-specific configurations. For example,            RAG techniques are representative of this effort. They used code-
the behavior of LSP server is affected by different IDEs. We observed         specific features to retrieve context, such as AST-based chunk-
that for a Java project, VS Code [43] might define the class path             ing [31, 39, 49], or program-analysis based retrieval [7, 36, 37, 64].
as the project’s top-level directory, whereas Cursor [3] sets it to           These techniques expose a fundamental trade-off. AST-based chunk-
the src/ subdirectory. Such discrepancies can affect which files are          ing is multi-lingual, but its reliance on superficial features leads to
analyzed, potentially affecting the LSP’s static analysis results. Our        imprecise retrieval. In contrast, program-analysis-based retrieval
prototype accommodates these variations through configuration.                achieves far greater precision by understanding the code’s execu-
   Extensibility to Other Languages. One of the key design goals              tion and data-flow relationships. However, this precision comes
of LspRag is extensibility. Its architecture is modular, comprising:          at a steep price: they require building and maintaining complex,
(1) a language-specific module for AST parsing and key feature                language-specific static analyzers, thereby limiting their applica-
extraction, and (2) language-agnostic modules that leverage the               bility to one specific language [8, 36, 37]. We compare LspRag
LSP for context retrieval and code fixing. To adapt LspRag for a new          with DraCo[8] and CodeQA[49] as they are the only open-sourced,
programming language, manual implementation is only necessary                 referred code-aware RAG works.
for the first module. This task involves translating the language’s              Neuro-Symbolic Approaches in Software Engineering. Re-
specific tree-sitter based AST nodes into LspRag’s IRs. This is a well-       cent neuro-symbolic approaches combine LLMs with program anal-
defined task requiring a modest implementation effort. Integrating            ysis for enhanced code intelligence. This synergy aids code auditing
the LSP-based capabilities is straightforward. It only requires the           and bug detection, with tools like LLMDFA [54] and DeepCon-
installation of the appropriate language server (e.g., as an IDE exten-       str [25] using LLMs for dataflow and constraint generation while
sion). Once installed, LspRag can immediately utilize the server’s            symbolic techniques validate paths and mitigate hallucinations. For
rich functionalities, such as “Go To Definition,” without any further         unit test generation, Tratto [12] uses a neural module to propose
modification to its core logic.                                               tokens and a symbolic module to constrain the search space based
                                                                              on program context. However, a common limitation is that they are
                                                                              tailored to a single programming language. In contrast, LspRag ad-
9    Related Work                                                             dresses this gap by leveraging the LSP to perform language-agnostic
Existing Approaches on Unit Test Generation. Automated unit                   neuro-symbolic unit test generation.
test generation has been a long-standing goal in software engineer-
ing, with two primary waves of innovation: classical search-based             10    Conclusion
and symbolic techniques, and more recent LLM-based approaches.                We addressed the challenge of generating high-coverage unit tests
Classical techniques primarily focus on maximizing a specific cri-            for modern, multi-language software systems in real-time. We iden-
terion, most often code coverage. Search-Based Software Testing               tified a key deficiency in existing approaches: their inability to pre-
(SBST) tools [15, 22, 33, 46, 48] for Java, and tools [2, 28, 40] for         cisely retrieve the necessary context, which hinders the generation
Python, employ evolutionary algorithms or random testing to gen-              of high-coverage and valid tests. To overcome this, we introduced
erate test suites. While powerful, these methods are inappropriate            LspRag, a novel framework that leverages the LSP to obtain precise
for real-time. They rely on whole-program compilation, heavy in-              code context. LspRag incorporates a hybrid analysis strategy to dis-
strumentation, and numerous execution iterations—steps that are               till essential, branch-governing symbols from the retrieved context
too slow and fragile when the codebase is in flux, changing every             and a compile-free self-repair mechanism to ensure the syntactic
few minutes during active development. Their operation assumes                validity of the generated tests without the overhead of compilation.
a stable, buildable project state, which is often not the case in the         Our extensive evaluation on real-world projects in Java, Python,
early, exploratory stages of writing new code. More recently, LLMs            and Golang demonstrates that LspRag significantly improves both
have been applied to test generation, often outperforming classical           line coverage and the rate of valid test generation across different
tools in terms of the readability and initial quality of generated            programming languages and underlying LLMs.
tests [2, 13, 47, 55, 60]. However, most of these works have selected
an iterative loop either for error detection or coverage feedback.            Acknowledgements
For instance, Altmayer et al. [2] propose coverage-guided pipelines           We appreciate the reviewers’ valuable and insightful comments.
where an LLM generates tests, which are then executed to gather               This research is partly sponsored by CCF-Tencent Rhino-Bird Fund
coverage data; this feedback is used to prompt the LLM to cover               Program (No. 20242001274) and NSFC Program (No. 62525207).
the remaining branches. While these approaches have improved
ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil                                                             Gwihwan Go, Quan Zhang, Chijin Zhou, Zhao Wei, and Yu Jiang


References                                                                                        ACM SIGSOFT International Symposium on Software Testing and Analysis (Vienna,
 [1] Mouna Abidi, Manel Grichi, and Foutse Khomh. 2019. Behind the scenes: devel-                 Austria) (ISSTA 2024). Association for Computing Machinery, New York, NY, USA,
     opers’ perception of multi-language practices. In Proceedings of the 29th Annual             1338–1350. https://doi.org/10.1145/3650212.3680364
     International Conference on Computer Science and Software Engineering (Toronto,         [26] Go Team at Google. 2024. Go Extension for Visual Studio Code. https:
     Ontario, Canada) (CASCON ’19). IBM Corp., USA, 72–81.                                        //marketplacevisualstudio.com/items?itemName=golang.Go. Accessed: 2025-05-
 [2] Juan Altmayer Pizzorno and Emery D Berger. 2024. CoverUp: Coverage-Guided                    23.
     LLM-Based Test Generation. arXiv e-prints (2024), arXiv–2403.                           [27] Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick Lewis, Wen-tsung Yih,
 [3] Inc. Anysphere. 2025. Cursor: The best way to code with AI. https://cursor.com/              Naman Goyal, and Wen-tau Chen. 2020. Dense Passage Retrieval for Open-
     Accessed: 2025-06-19.                                                                        Domain Question Answering. In Proceedings of the 2020 Conference on Empirical
 [4] Andrea Arcuri and Lionel C. Briand. 2014. A hitchhiker’s guide to statistical tests          Methods in Natural Language Processing (EMNLP). 6769–6781.
     for assessing randomized algorithms in software engineering. Software Testing,          [28] Caroline Lemieux, Jeevana Priya Inala, Shuvendu K Lahiri, and Siddhartha Sen.
     Verification and Reliability 24, 3 (2014), 219–250. https://doi.org/10.1002/stvr.1486        2023. Codamosa: Escaping coverage plateaus in test generation with pre-trained
 [5] Moritz Beller, Georgios Gousios, Annibale Panichella, and Andy Zaidman. 2015.                large language models. In 2023 IEEE/ACM 45th International Conference on Soft-
     When, how, and why developers (do not) test in their IDEs. In Proceedings of the             ware Engineering (ICSE). IEEE, 919–931.
     2015 10th Joint Meeting on Foundations of Software Engineering. 179–190.                [29] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin,
 [6] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D. Kaplan,                   Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel,
     Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda                   et al. 2020. Retrieval-augmented generation for knowledge-intensive nlp tasks.
     Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan,                Advances in neural information processing systems 33 (2020), 9459–9474.
     Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter,              [30] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin,
     and Dario Amodei. 2020. Language Models are Few-Shot Learners. In Advances                   Gustavo Nogueira, Heinrich Piele, Wen-tau Chen, Wen-Tsung Yih, Timo Rock-
     in Neural Information Processing Systems, H. Larochelle, M. Ranzato, R. Hadsell,             täschel, et al. 2020. Retrieval-Augmented Generation for Knowledge-Intensive
     M. F. Balcan, and H. Lin (Eds.), Vol. 33. Curran Associates, Inc., 1877–1901.                NLP Tasks. In Advances in Neural Information Processing Systems (NeurIPS), Vol. 33.
 [7] Bei Chen, Fengji Zhang, Anh Nguyen, Daoguang Zan, Zeqi Lin, Jian-Guang Lou,                  9459–9474.
     and Weizhu Chen. 2022. Codet: Code generation with generated tests. arXiv               [31] Jia Li, Xianjie Shi, Kechi Zhang, Ge Li, Zhi Jin, Lei Li, Huangzhao Zhang, Jia Li,
     preprint arXiv:2207.10397 (2022).                                                            Fang Liu, Yuwei Zhang, Zhengwei Tao, Yihong Dong, Yuqi Zhu, and Chongyang
 [8] Wei Cheng, Yuhan Wu, and Wei Hu. 2024. Dataflow-Guided Retrieval Augmen-                     Tao. 2025. GraphCodeAgent: Dual Graph-Guided LLM Agent for Retrieval-
     tation for Repository-Level Code Completion. In ACL.                                         Augmented Repo-Level Code Generation. (2025). arXiv:2504.10046 [cs.SE] https:
 [9] Henry Coles, Thomas Laurent, Christopher Henard, Mike Papadakis, and An-                     //arxiv.org/abs/2504.10046
     thony Ventresque. 2016. PIT: a practical mutation testing tool for Java (demo). In      [32] Wen Li, Na Meng, Li Li, and Haipeng Cai. 2021. Understanding language se-
     Proceedings of the 25th International Symposium on Software Testing and Analysis             lection in multi-language software projects on GitHub. In 2021 IEEE/ACM 43rd
     (ISSTA ’16). ACM, 449–452. https://doi.org/10.1145/2931037.2948707                           International Conference on Software Engineering: Companion Proceedings (ICSE-
[10] GitHub Community. 2023. Using Copilot chat API programatically. https:                       Companion). IEEE, 256–257.
     //github.com/orgs/community/discussions/112339 Accessed: 2025-07-13.                    [33] Yun Lin, Jun Sun, Gordon Fraser, Ziheng Xiu, Ting Liu, and Jin Song Dong. 2020.
[11] Stack Overflow Community. 2023. How to integrate GitHub Copilot’s API in a                   Recovering fitness gradients for interprocedural Boolean flags in search-based
     Python script? https://stackoverflow.com/questions/79208670/how-to-integrate-                testing. In Proceedings of the 29th ACM SIGSOFT International Symposium on
     github-copilots-api-in-a-python-script Accessed: 2025-07-13.                                 Software Testing and Analysis. 440–451.
[12] Erisa Daka, Giovanni Squillace, Michael Cooper, Alessandra Gorla, Gordon Fraser,        [34] Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Cheng-
     Pankaj Garg, and Alberto Bacchelli. 2025. Tratto: A Neuro-Symbolic Approach                  gang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, et al. 2024. Deepseek-v3
     to Deriving Axiomatic Test Oracles. In Proceedings of the 34th ACM SIGSOFT                   technical report. arXiv preprint arXiv:2412.19437 (2024).
     International Symposium on Software Testing and Analysis. ACM.                          [35] Fang Liu, Yang Liu, Lin Shi, Houkun Huang, Ruifeng Wang, Zhen Yang, Li Zhang,
[13] Arghavan Moradi Dakhel, Amin Nikanjam, Vahid Majdinasab, Foutse Khomh,                       Zhongqi Li, and Yuchi Ma. 2024. Exploring and evaluating hallucinations in
     and Michel C Desmarais. 2024. Effective test generation using pre-trained large              llm-powered code generation. arXiv preprint arXiv:2404.00971 (2024).
     language models and mutation testing. Information and Software Technology 171           [36] Wei Liu, Ailun Yu, Daoguang Zan, Bo Shen, Wei Zhang, Haiyan Zhao, Zhi Jin, and
     (2024), 107468.                                                                              Qianxiang Wang. 2024. GraphCoder: Enhancing Repository-Level Code Comple-
[14] Ben Darnell and the Tornado Developers. 2025. Tornado: Python Web Framework                  tion via Coarse-to-fine Retrieval Based on Code Context Graph. In Proceedings of
     and Asynchronous Networking Library. https://github.com/tornadoweb/tornado.                  the 39th IEEE/ACM International Conference on Automated Software Engineering
     Apache 2.0 licensed; originally developed at FriendFeed.                                     (Sacramento, CA, USA) (ASE ’24). Association for Computing Machinery, New
[15] Amirhossein Deljouyi, Roham Koohestani, Maliheh Izadi, and Andy Zaidman.                     York, NY, USA, 570–581. https://doi.org/10.1145/3691620.3695054
     2025. Leveraging Large Language Models for Enhancing the Understandability              [37] Xiangyan Liu, Bo Lan, Zhiyuan Hu, Yang Liu, Zhicheng Zhang, Fei Wang, Michael
     of Generated Unit Tests . In 2025 IEEE/ACM 47th International Conference on                  Shieh, and Wenmeng Zhou. 2024. Codexgraph: Bridging large language models
     Software Engineering (ICSE). IEEE Computer Society, Los Alamitos, CA, USA,                   and code repositories via code graph databases. arXiv preprint arXiv:2408.03910
     392–404. https://doi.org/10.1109/ICSE55347.2025.00032                                        (2024).
[16] Anna Derezińska and Konrad Hałas. 2015. Improving Mutation Testing Process              [38] Shuai Lu, Nan Duan, Hojae Han, Daya Guo, Seung-won Hwang, and Alexey Svy-
     of Python Programs. In Software Engineering in Intelligent Systems. Advances in              atkovskiy. 2022. ReACC: A Retrieval-Augmented Code Completion Framework.
     Intelligent Systems and Computing, Vol. 349. Springer, 233–242. https://doi.org/             In Proceedings of the 60th Annual Meeting of the Association for Computational
     10.1007/978-3-319-18473-9_23                                                                 Linguistics (Volume 1: Long Papers), ACL 2022, Dublin, Ireland, May 22-27, 2022,
[17] OpenAI et al. 2024. GPT-4 Technical Report. arXiv:2303.08774 [cs.CL] https:                  Smaranda Muresan, Preslav Nakov, and Aline Villavicencio (Eds.). Association for
     //arxiv.org/abs/2303.08774                                                                   Computational Linguistics, 6227–6240. https://doi.org/10.18653/V1/2022.ACL-
[18] Apache Software Foundation. 2025. Apache Commons CLI. https://github.com/                    LONG.431
     apache/commons-cli Accessed: 2025-01-15.                                                [39] Shuai Lu, Daya Guo, Shuo Ren, Junjie Huang, Alexey Svyatkovskiy, Ambrosio
[19] Apache Software Foundation. 2025. Apache Commons CSV. https://github.com/                    Blanco, Colin B. Clement, Dawn Drain, Daxin Jiang, Duyu Tang, Ge Li, Lidong
     apache/commons-csv Accessed: 2025-01-15.                                                     Zhou, Linjun Shou, Long Zhou, Michele Tufano, Ming Gong, Ming Zhou, Nan
[20] PSF (Python Software Foundation). 2025. Black. https://github.com/psf/black                  Duan, Neel Sundaresan, Shao Kun Deng, Shengyu Fu, and Shujie Liu. 2021.
     Accessed: 2025-01-15.                                                                        CodeXGLUE: A Machine Learning Benchmark Dataset for Code Understanding
[21] Steve Francia. 2013. Cobra. https://github.com/spf13/cobra. Accessed: 2025-01-15.            and Generation. CoRR abs/2102.04664 (2021).
[22] Gordon Fraser and Andrea Arcuri. 2011. Evosuite: automatic test suite generation        [40] Stephan Lukasczyk and Gordon Fraser. 2022. Pynguin: Automated unit test gen-
     for object-oriented software. In Proceedings of the 19th ACM SIGSOFT symposium               eration for python. In Proceedings of the ACM/IEEE 44th International Conference
     and the 13th European conference on Foundations of software engineering. 416–419.            on Software Engineering: Companion Proceedings. 168–172.
[23] Nat Friedman. 2021. Introducing GitHub Copilot: Your AI Pair Programmer. https:         [41] Microsoft. 2024. Language Server Protocol. https://github.com/microsoft/
     //github.blog/2021-06-29-introducing-github-copilot-ai-pair-programmer/ Ac-                  language-server-protocol Accessed: 2024-12-24.
     cessed: 2024-12-20.                                                                     [42] Microsoft. 2024. Python Extension for Visual Studio Code. https://marketplace.
[24] GitHub. 2024. Writing Tests with GitHub Copilot. https://docs.github.com/                    visualstudio.com/items?itemName=ms-python.python. Accessed: 2025-05-23.
     en/copilot/using-github-copilot/guides-on-using-github-copilot/writing-tests-           [43] Microsoft. 2025. Visual Studio Code. https://code.visualstudio.com/ Accessed:
     with-github-copilot. Accessed: 2025-05-13.                                                   2025-06-19.
[25] Gwihwan Go, Chijin Zhou, Quan Zhang, Xiazijian Zou, Heyuan Shi, and Yu                  [44] Neverdecel. 2024. CodeRAG: An AI-powered tool for real-time codebase query-
     Jiang. 2024. Towards More Complete Constraints for Deep Learning Library                     ing and augmentation using OpenAI and vector search. https://github.com/
     Testing via Complementary Set Guided Refinement. In Proceedings of the 33rd                  Neverdecel/CodeRAG. Accessed: 2025-05-18.
LSPRAG: LSP-Guided RAG for Language-Agnostic Real-Time Unit Test Generation                                                      ICSE ’26, April 12–18, 2026, Rio de Janeiro, Brazil


[45] Oracle. 2024. Java Platform Extension for Visual Studio Code. https://marketplace.           Systems, S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh
     visualstudio.com/items?itemName=oracle.oracle-java. Accessed: 2025-05-23.                    (Eds.), Vol. 35. Curran Associates, Inc., 24824–24837.
[46] Carlos Pacheco and Michael D Ernst. 2007. Randoop: feedback-directed random             [59] Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, and Lingming Zhang. 2024.
     testing for Java. In Companion to the 22nd ACM SIGPLAN conference on Object-                 Agentless: Demystifying llm-based software engineering agents. arXiv preprint
     oriented programming systems and applications companion. 815–816.                            arXiv:2407.01489 (2024).
[47] Gabriel Ryan, Siddhartha Jain, Mingyue Shang, Shiqi Wang, Xiaofei Ma, Murali Kr-        [60] Zhuokui Xie, Yinghao Chen, Chen Zhi, Shuiguang Deng, and Jianwei Yin. 2023.
     ishna Ramanathan, and Baishakhi Ray. 2024. Code-Aware Prompting: A Study of                  ChatUniTest: a ChatGPT-based automated unit test generation tool. arXiv preprint
     Coverage-Guided Test Generation in Regression Setting using LLM. Proc. ACM                   arXiv:2305.04764 (2023).
     Softw. Eng. 1, FSE, Article 43 (July 2024), 21 pages. https://doi.org/10.1145/3643769   [61] Haoran Yang, Yu Nong, Shaowei Wang, and Haipeng Cai. 2024. Multi-Language
[48] Arkadii Sapozhnikov, Mitchell Olsthoorn, Annibale Panichella, Vladimir Ko-                   Software Development: Issues, Challenges, and Solutions. IEEE Transactions on
     valenko, and Pouria Derakhshanfar. 2024. TestSpark: IntelliJ IDEA’s Ultimate                 Software Engineering 50, 3 (2024), 512–533. https://doi.org/10.1109/TSE.2024.
     Test Generation Companion. In Proceedings of the 2024 IEEE/ACM 46th Interna-                 3358258
     tional Conference on Software Engineering: Companion Proceedings. 30–34.                [62] Haoran Yang, Yu Nong, Shaowei Wang, and Haipeng Cai. 2024. Multi-language
[49] Sankalp Saxena. 2023. code_qa: LLM-based question-answering over code. https:                software development: Issues, challenges, and solutions. IEEE Transactions on
     //github.com/sankalp1999/code_qa. Accessed: 2025-05-23.                                      Software Engineering 50, 3 (2024), 512–533.
[50] Amazon Web Services. 2024. Amazon CodeWhisperer. https://aws.amazon.com/                [63] Fengji Zhang, Bei Chen, Yue Zhang, Jacky Keung, Jin Liu, Daoguang Zan, Yi Mao,
     codewhisperer/ Accessed: 2025-07-12.                                                         Jian-Guang Lou, and Weizhu Chen. 2023. Repocoder: Repository-level code com-
[51] Sirupsen. 2025. Logrus. https://github.com/sirupsen/logrus Accessed: 2025-01-15.             pletion through iterative retrieval and generation. arXiv preprint arXiv:2303.12570
[52] Parth Thakkar. 2022. Copilot Explorer. https://thakkarparth007.github.io/copilot-            (2023).
     explorer/posts/copilot-internals.html Accessed: 2024-12-20.                             [64] Fengji Zhang, Bei Chen, Yue Zhang, Jacky Keung, Jin Liu, Daoguang Zan, Yi Mao,
[53] tree-sitter. 2024. Tree-sitter: An incremental parsing system for programming                Jian-Guang Lou, and Weizhu Chen. 2023. RepoCoder: Repository-Level Code
     tools. https://tree-sitter.github.io/tree-sitter/. Accessed: 2025-05-23.                     Completion Through Iterative Retrieval and Generation. In Proceedings of the 2023
[54] Chengpeng Wang, Wuqi Zhang, Xiangzhe Xu, Zian Su, and Xiangyu Zhang.                         Conference on Empirical Methods in Natural Language Processing, Houda Bouamor,
     2024. LLMDFA: Analyzing Dataflow in Code with Large Language Models. arXiv                   Juan Pino, and Kalika Bali (Eds.). Association for Computational Linguistics,
     preprint arXiv:2402.10754 (2024).                                                            Singapore, 2471–2484. https://doi.org/10.18653/v1/2023.emnlp-main.151
[55] Han Wang, Han Hu, Chunyang Chen, and Burak Turhan. 2024. Chat-like As-                  [65] Feipeng Zhang, Wenyu Jiang, Jun Shu, Feng Zheng, Hongxin Wei, et al. 2024.
     serts Prediction with the Support of Large Language Model. arXiv preprint                    On the noise robustness of in-context learning for text generation. Advances in
     arXiv:2407.21429 (2024).                                                                     Neural Information Processing Systems 37 (2024), 16569–16600.
[56] Siwei Wang, Xue Mao, Ziguang Cao, Yujun Gao, Qucheng Shen, and Chao Peng.               [66] Kechi Zhang, Jia Li, Ge Li, Xianjie Shi, and Zhi Jin. 2024. Codeagent: Enhancing
     2023. NxtUnit: Automated Unit Test Generation for Go. In Proceedings of the 27th             code generation with tool-integrated agent systems for real-world repo-level
     International Conference on Evaluation and Assessment in Software Engineering                coding challenges. arXiv preprint arXiv:2401.07339 (2024).
     (Oulu, Finland) (EASE ’23). Association for Computing Machinery, New York, NY,          [67] Ziyao Zhang, Yanlin Wang, Chong Wang, Jiachi Chen, and Zibin Zheng. 2024.
     USA, 176–179. https://doi.org/10.1145/3593434.3593443                                        Llm hallucinations in practical code generation: Phenomena, mechanism, and
[57] Zejun Wang, Kaibo Liu, Ge Li, and Zhi Jin. 2024. HITS: High-coverage LLM-based               mitigation. arXiv preprint arXiv:2409.20550 (2024).
     Unit Test Generation via Method Slicing. In Proceedings of the 39th IEEE/ACM            [68] Yangyang Zhao, Alexander Serebrenik, Yuming Zhou, Vladimir Filkov, and Bog-
     International Conference on Automated Software Engineering. 1258–1268.                       dan Vasilescu. 2017. The impact of continuous integration on other software
[58] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi,                     development practices: a large-scale empirical study. In 2017 32nd IEEE/ACM
     Quoc V. Le, and Denny Zhou. 2022. Chain-of-Thought Prompting Elicits Rea-                    International Conference on Automated Software Engineering (ASE). IEEE, 60–71.
     soning in Large Language Models. In Advances in Neural Information Processing
