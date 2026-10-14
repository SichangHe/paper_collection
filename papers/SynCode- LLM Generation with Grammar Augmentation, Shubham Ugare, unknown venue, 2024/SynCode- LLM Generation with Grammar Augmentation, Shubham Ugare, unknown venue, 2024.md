                                        SynCode: LLM Generation with Grammar Augmentation

                                        Shubham Ugare
                                        University of Illinois Urbana-Champaign, USA

                                        Tarun Suresh
                                        University of Illinois Urbana-Champaign, USA

                                        Hangoo Kang
                                        University of Illinois Urbana-Champaign, USA
arXiv:2403.01632v4 [cs.LG] 6 Nov 2024




                                        Sasa Misailovic
                                        University of Illinois Urbana-Champaign, USA

                                        Gagandeep Singh
                                        University of Illinois Urbana-Champaign and VMware Research, USA



                                                                                         Abstract

                                                LLMs are widely used in complex AI applications. These applications underscore the need
                                                for LLM outputs to adhere to a specific format, for their integration with other components
                                                in the systems. Typically the format rules – e.g., data serialization formats such as JSON,
                                                YAML, or Code in Programming Language – are expressed as context-free grammar (CFG).
                                                Due to the hallucinations and unreliability of LLMs, instructing LLMs to adhere to specified
                                                syntax becomes an increasingly important challenge.
                                                We present SynCode, a novel framework for efficient and general syntactical decoding
                                                with LLMs, to address this challenge. SynCode ensures soundness and completeness with
                                                respect to the CFG of a formal language, effectively retaining valid tokens while filtering out
                                                invalid ones. SynCode uses an offline-constructed, efficient lookup table, the DFA mask
                                                store, created from the DFA (Deterministic Finite Automaton) of the language’s grammar
                                                for efficient generation. SynCode seamlessly integrates with any language defined by CFG,
                                                as evidenced by experiments focusing on generating JSON, SQL, Python, and Go outputs.
                                                Our experiments evaluating the effectiveness of SynCode for JSON generation demonstrate
                                                that SynCode eliminates all syntax errors and significantly outperforms state-of-the-art
                                                baselines. Furthermore, our results underscore how SynCode significantly reduces 96.07%
                                                of syntax errors in generated Python and Go code, showcasing its substantial impact on
                                                enhancing syntactical precision in LLM generation.
                                                Our code is available at https://github.com/uiuc-focal-lab/syncode


                                        1   Introduction

                                        Recent research has shown that transformer-based large language models (LLMs) can play a pivotal role
                                        within compound AI systems, where they integrate with other software tools (Zaharia et al., 2024; Mialon
                                        et al., 2023). For example, OpenAI’s code interpreter (OpenAI, 2024) generates and executes Python pro-
                                        grams automatically while responding to user prompts. Similarly, Wolfram Alpha (wolfram, 2024) translates
                                        user queries about mathematical questions into a domain-specific language (DSL) for utilizing various tools.
                                        LLMs are utilized in various other applications to translate natural language text into formal languages,
                                        such as inputs to logic solvers (Pan et al., 2023; Olausson et al., 2023) and theorem provers (Wu et al., 2022;
                                        Yang et al., 2023), among others. In all these applications, the LLM output is expected to follow a certain
                                        syntactic structure. However, challenges such as hallucination and non-robustness make LLMs unreliable for


                                                                                              1
such automated systems (Liang et al., 2023). Moreover, recent theoretical (Hahn, 2020; Yang et al., 2024)
and empirical (Ebrahimi et al., 2020; Bhattamishra et al., 2020; Delétang et al., 2023) research suggests that
language models based on transformers show difficulty in learning basic formal grammars.
The interaction between software tools and LLMs commonly occurs through data serialization formats like
JSON or YAML, or code in domain-specific or general-purpose programming languages, such as Python
or Go. Despite advancements in techniques such as fine-tuning and prompt engineering, which enhance
the model’s ability, these approaches fall short of fully addressing the challenge of syntactical accuracy in
generated output. This problem is especially prominent in two common scenarios: (1) using open-source
models, which are typically relatively small, and (2) generating text for formal languages with relatively
modest representation in the LLM’s training data.
Modern LLMs generate text sequentially, from left to right, one token at a time. For each prefix, the
model computes a probability distribution over a predefined vocabulary to predict the next token. The
LLM’s decoding algorithm dictates how these probabilities are used to generate the token sequence. Very re-
cently, researchers have proposed new techniques for grammar-guided generation to enhance the syntactical
accuracy of LLMs by modifying the decoding algorithm. Although they ensure that the model consis-
tently selects tokens that adhere to a specified formal language (Scholak et al., 2021; Poesia et al., 2022;
Gerganov and et. al., 2024; Willard and Louf, 2023), the existing approaches for grammar-guided gener-
ation either suffer from high error rates, resulting in syntactically incorrect output or impose significant
run time overhead in the inference:

• Issues with syntactical accuracy: The language grammar consists of the terminals, fundamental
  building blocks of the language (e.g., keywords, operators). Typically, a lexer creates lexical tokens from
  the input, each token associated with a terminal from the grammar. The LLM tokens form part of the
  model’s fixed vocabulary, defined before training, and do not directly correspond to lexical tokens asso-
  ciated with any specific grammar. This discrepancy, known as token misalignment, presents a significant
  challenge in ensuring precise grammar-guided generation (Poesia et al., 2022). Thus, formally showing
  the soundness of the algorithm poses a challenge for ensuring the precision of the approach.
• Issues with high computational overhead: Typically, the computational complexity of additional
  operations performed for syntactical generation is lower than the standard LLM generation operations
  needed for propagating the input through LLM layers. However, these syntactical generation opera-
  tions are typically executed sequentially on a CPU, in contrast to the GPU-accelerated LLM generation,
  adding to the run time. Achieving low inference overhead faces two primary challenges for syntactical
  LLM generation. First, the algorithm should facilitate offline computations that minimize the overhead
  during inference. Second, it should effectively utilize available hardware resources and offload additional
  computations to modern hardware, such as GPUs, to enable parallel computation.
• Issues with generality: Prior works are restricted to specific LLM decoding schemes (Scholak et al.,
  2021; Lundberg et al., 2023). A major challenge for generality is designing a composable algorithm that
  can integrate with any decoding strategy such as greedy, beam search, and different types of temperature
  sampling.

Our goal is to make grammar-guided generation precise and efficient by imposing formal grammar constraints
on LLM generations, ensuring the output adheres strictly to the predefined syntax.

SynCode. SynCode is an efficient and general approach for generating syntactically correct output. Syn-
Code takes a context-free grammar (CFG) represented with extended Backus–Naur form (EBNF) rules and
ensures that the LLM output follows the provided grammar. SynCode algorithm is general and can be
composed with any existing LLM decoding algorithm, including greedy, beam search, and sampling.
During the LLM decoding stage, where LLM selects the next token, SynCode employs a strategic two-step
approach. In the initial step, it leverages partial output to generate sequences of terminals that can follow
the partial output called accept sequences. This reduction to the level of terminals—a closer abstraction
to language grammar than LLM tokens—simplifies the problem. Simultaneously, SynCode computes a
remainder from the partial output, representing the suffix that may change its terminal type in subsequent


                                                      2
generations. In the second step, SynCode algorithm walks over the DFA using the remainder and uses the
mask store to compute the mask (a boolean array to filter the vocabulary) specific to each accept sequence.
By unifying masks for each accept sequence SynCode gets the set of syntactically valid tokens.
To ensure the efficiency of SynCode’s syntactic generation, we propose a novel data structure called DFA
mask store which is pre-computed offline. DFA mask store is a lookup table derived from Deterministic Finite
Automata (DFA) representing the terminals of the language grammar. SynCode algorithm can efficiently
compute the syntactically valid next LLM tokens by leveraging this mask store. Moreover, the SynCode
algorithm offers the additional benefit of parallelizing a substantial portion of the syntactical LLM generation
computations by offloading them to a GPU.
We demonstrate that the SynCode algorithm is sound – ensuring it retains all syntactically valid tokens
at every generation step. SynCode is also complete under specific conditions – affirming it rejects every
syntactically invalid token.
The SynCode framework seamlessly integrates with any language defined by deterministic CFGs and scales
efficiently to generate code for general-purpose programming languages (GPLs). We evaluate SynCode’s
ability to guide the Llama-2-7B-chat and Gemma2-2B-it models with the JSON grammar to generate valid
JSON completions to prompts from the JSONModeEval (NousResearch, 2024) dataset. We empirically
show that LLMs augmented with SynCode do not generate any syntax errors for JSON and that guiding
Gemma2-2B-it generation with SynCode achieves 100% JSON schema validation accuracy. We evaluate
SynCode on generating SQL queries from the text in Spider (Yu et al., 2018) and show that SynCode
improves both compilation rate and execution accuracy. Further, we evaluate the augmentation of SynCode
with a diverse set of state-of-the-art LLMs for the code completion tasks using problems from the HumanEval
and MBXP datasets (Athiwaratkun et al., 2023). Our experiments, conducted with CFGs for a substantial
subset of Python and Go, demonstrate that SynCode reduces 96.07% of the syntax errors for Python and
Go on average. The remaining syntax errors persist because the LLM fails to halt generation before reaching
the maximum generation limit defined in our experiments.

Contributions. The main contributions of this paper are:

⋆ We present a parsing-based technique for decoding of LLMs by designing novel algorithms that allow us
  to efficiently generate syntactically correct output.
⋆ We implement our approach into a scalable and general framework named SynCode that can work with
  any formal language with user-provided context-free grammar.
⋆ We present an extensive evaluation of the performance of SynCode in generating syntactically correct
  output for JSON, SQL and two general-purpose programming languages Python and Go.


2     Background

In this section, we provide the necessary background on LLMs and formal language grammar.
Notation. Let the alphabet Σ be a finite set of characters. We use ϵ to denote an empty string. Given a
               i
set S, we use
          S S to   denote the set of all i-length sequences that can be formed by selecting elements from S,
and S = i∈N S i . Thus Σ∗ represents the set of all strings over characters in Σ, including the empty string
      ∗

ϵ. Further, we use Σ+ to denote (Σ∗ − ϵ). Given two strings w1 , w2 ∈ Σ∗ , we use w1 .w2 to denote string
obtained by concatenating w2 to w1 . All symbols used in the paper are listed in Appendix A.1.

2.1   Language Models

Current language models (LM) operate on vocabulary V ⊆ Σ∗ of tokens. A tokenizer takes an input prompt
C0 ∈ Σ∗ , which is a sequence of characters, as input and converts C0 into a sequence of tokens t1 , t2 , . . . , tk .
Figure 2 shows a typical tokenization method, where common words (e.g., def ) have their own token
(even with a space in front), while rare words (e.g., incr_list ) are split into multiple tokens. In order


                                                          3
Figure 1: In the SynCode workflow, the LLM takes partial output Ck and generates a distribution for the
next token tk+1 . The parser processes Ck to produce accept sequences A and remainder r. These values
are used by the DFA mask store to create a token mask, eliminating syntactically invalid tokens. The LLM
iteratively generates a token tk+1 using the distribution and the mask, appending it to Ck to create the
updated code Ck+1 . The process continues until the LLM returns the final code Cn based on the defined
stop condition.




to generate the next token, the LM M : V ∗ → R|V | takes as input the sequence of tokens t1 , t2 , . . . , tk , and
outputs aPvector of scores z over the vocabulary: z = M (t1 , t2 , . . . , tk ). The softmax function softmax(zi ) =
exp(zi )/ j (exp(zj )) transforms z into a probability distribution over the vocabulary V .
Decoding. Building upon this, the language model M
is recurrently applied to generate a sequence of tokens
t1 , t2 . . . tk . When choosing the (k +1)-th token, the prob-
ability distribution for the next token is obtained through
softmax(M (t1 , t2 . . . tk )). Various approaches for token
selection from this distribution have been explored in the
literature such as greedy decoding, sampling, and beam
search. Each technique is repeated until the prediction of
a special end-of-sequence token, EOS , or the fulfillment           Figure 2: Tokenization of a string.
of another stopping criterion. This iterative process is
equivalent to sampling from a distribution over V ∗ , potentially resulting in multiple feasible decodings.
Constrained Masking. In the context of de-
coding, we encounter scenarios where excluding
specific tokens at particular positions becomes       Algorithm 1 Masked LLM Generation
crucial (e.g., excluding harmful words). This im-     Inputs: M : LLM, T : tokenizer, C0 : input prompt string,
plies we can disregard these tokens and proceed       fm : function that generates mask, nmax : maximum generated
with decoding based on the remaining set. An          tokens, D: any decoding algorithm
algorithm for such masking relies on a function       Output: string Cn
fm to generate the mask m based on the exact           1: function MaskedGenerate(M , T , fm , C0 )
use case. In the mask m ∈ {0, 1}|V | , ’1’ indi-       2:    Tcur ← Tokenize(T , C0 )
cates a viable token, and ’0’ signifies a discarded    3:    for i ∈ {1, . . . nmax } do
one. Decoding methods mentioned earlier can be         4:       scores ← M (Tcur )
applied to m ⊙ softmax(z), where ⊙ represents          5:       m ← fm (Tcur , T )
element-wise multiplication.P The resultant vec-       6:       scores ← m ⊙ scores
tor should be scaled by 1/ i (m × softmax(z))i         7:       ti ← D(scores)
to restore correct probabilities. Algorithm 1          8:          if ti = EOS then
presents the steps for masked decoding. In Syn-        9:              break
                                                      10:          Tcur ← append(Tcur , ti )
Code, we use the constrained masking technique
to exclude syntactically invalid tokens.              11:       Cn ← Detokenize(T , Tcur )
                                                      12:       return Cn

                                                            4
2.2   Formal Language Grammar

A formal language syntax is represented by defin-
ing a grammar. A formal grammar is essentially a set of production rules that describe all possible strings
in a given language. A grammar consists of terminal and nonterminal symbols, where terminal symbols are
the actual characters or tokens in the language, while nonterminal symbols are placeholders used to define
patterns or structures within the language.
The syntax for most programming languages can be defined using context-free grammar (CFG). CFG is a
formal grammar that consists of production rules that can be applied to a nonterminal symbol regardless of
its context. In CFG, each production rule is of the form E → β with E a single nonterminal symbol, and
β a string of terminals and nonterminals (β can be empty). Regardless of which symbols surround it, the
single nonterminal E on the left-hand side can always be replaced by β on the right-hand side.
Terminals. We use Γ to denote the set of terminals in the grammar. Regular expressions are used to
describe the terminals. For instance, A regular expression ∧ [0-9]+ is used for an integer literal: This regular
expression describes a sequence of one or more digits (0 to 9). We use ρ to denote a regular expression and
L(ρ) ⊆ Σ∗ to denote the language recognized ρ. Regular expressions are often associated with the creation
of Deterministic Finite Automata (DFAs). A DFA is a theoretical construct used to recognize patterns
specified by regular expressions.
Definition 1 (DFA). A deterministic finite automaton (DFA) D is a 5-tuple, (Q, Σ, δ, q0 , F ), consisting of a
finite set of states Q, a finite set of input symbols called the alphabet Σ, a transition function δ : Q × Σ → Q,
an initial state q0 ∈ Q and a set of accept states F ⊆ Q.

Let w = a1 a2 . . . an be a string over the alphabet Σ. The DFA computation δ ∗ : Q × Σ∗ → Q on a string
w is defined as δ ∗ (r0 , w) = rn when ri+1 = δ(ri , ai+1 ), for i = 0, . . . , n − 1. The automaton D accepts the
string w if δ ∗ (q0 , w) ∈ F .
Lexer. We assume lexical analysis with a 1-character lookahead and no backtracking. This assumption is
crucial for the efficiency of SynCode algorithm.
Definition 2 (Lexer). The function Lex is defined to take partial output Ck ∈ Σ∗ as input and produce a
sequence l1 , l2 , . . . , lf of lexical tokens where li ∈ Σ∗ .

3     Overview

3.1   Illustrative Example

Consider an example grammar in Figure 3 that
uses the Lark EBNF syntax for defining the gram-
mar production rules. The grammar represents
a Domain-Specific Language (DSL) consisting of
arithmetic expressions with basic operations like ad-
dition, subtraction, multiplication, and division over
integers and floating point numbers. It also in-
cludes support for parentheses to specify precedence
and allows functions like exponential (math_exp),
square root (math_sqrt), sine (math_sin), and co-
sine (math_cos) to be applied to expressions.
The symbols in the grammar such as expr
and factor that can expand into other sym-                  Figure 3: Example grammar for illustration.
bols through the application of production rules
are called non-terminals.         Symbols such as
( or INT cannot be further expanded and are called terminals.                      Let the set Γ =
{lpar, rpar, add, sub, mult, div, int, float, math_exp, math_sqrt, math_sin, math_cos} represent the set
of all terminals of the grammar.                The terminal int is defined by the regular expres-


                                                         5
sion [0-9]+ , and float is defined by the regular expression [0-9]+ .[0-9]+ .       We use terminals
lpar, rpar, add, sub, mult, div, math_exp, math_sqrt, math_sin, math_cos, to denote the strings ( , ) ,
+ , * , / , math_exp , math_sqrt , math_sin , math_cos respectively.
Task. Consider an LLM that is used to translate a
natural language text to an expression in the DSL
defined above. Since LLMs are typically not good
at mathematical calculations, it is common to in-
stead let the LLM generate intermediate outputs
in a certain syntax, and an interpreter of the DSL
then computes the LLM’s output into accurate re-
                                                       Figure 4: Prompt for the example which is provided
sults (Mialon et al., 2023). Figure 4 presents the
                                                       as input to the LLM.
prompt we use for our illustrative example, contain-
ing 2 question-answer pairs before the actual question that we want the LLM to answer. Providing question-
answer examples before asking the actual questions is called few-shot prompting (2-shot in this case) and
significantly improves the model’s accuracy (Brown et al., 2020).
Standard LLM Generation. As described in Section 2, the stan-
dard LLM first tokenizes the input and then iteratively predicts the
next token from its vocabulary V . Figure 5 presents the output
from the LLaMA-7B model and our SynCode when given the Fig. 4
prompt. The output of the model is not a valid program in the DSL;
it uses functions math_area and math_side that do not exist in the
grammar. Further, LLaMA-7B does not stop after generating the
answer to our question and continues to generate more irrelevant
question-answer pairs. SynCode on the other hand guarantees the
syntactic validity of the LLM’s output by excluding syntactically Figure 5: Output from LLM without
invalid choices when generating each token. For example, after gen- and with SynCode. The colors rep-
erating math , SynCode excludes _area and other choices from resent the tokenization of the output.
the LLM’s vocabulary. The LLM opts for _sqrt which is the top syntactically valid choice and continues
the generation from math_sqrt .

Constrained Decoding. Let G denote the grammar in our example and L(G) ⊆ Σ∗ denote all syntactically
valid strings in the grammar. Ideally, we want the final LLM output Cn to be in L(G). Strings such
as math_exp(2 + 3 + 5 + 7 + 11) and math_sin(30) + math_cos(60) belong to L(G) as they are
syntactically valid. Let Ck denote the LLM’s partial output during the k-th iteration of LLM generation.
Suppose Lp (G) denotes all prefixes of L(G), i.e., all strings that can be extended to a syntactically valid
output. math_sin(30 and math_sin(30) + math are in Lp (G) as they can be extended to be syntactically
valid. By ensuring that at each intermediate step, the invariant that the LLM partial generation Ck is in the
set Lp (G) is maintained, we can guarantee that upon completion of the generation process, Cn will indeed
be syntactically valid, i.e., Cn ∈ L(G). This ensures that an intermediate output such as math_area which
is not in Lp (G) is never generated by the model.

3.2   SynCode Algorithm

A key challenge in syntactic generation is token misalignment, where LLM tokens do not directly correspond
to lexical tokens from the grammar. The main reason for the high error rate in syntactic generation in prior
works is the lack of formalization in their approaches (Section 6). Our work addresses this challenge by
providing an algorithm that is provably sound — retains all syntactically valid tokens and is complete under
specific conditions—rejecting every syntactically invalid token at every generation step.
Another significant challenge for efficiency is developing a novel algorithm that facilitates offline computations
that minimize the overhead during inference. SynCode tackles this challenge by creating a novel structure
called the DFA mask store offline. For a given grammar G and vocabulary V , this mask store is constructed


                                                        6
once and can be used across all generations. DFA mask store maps states of DFAs (corresponding to terminals
in the grammar G) to boolean masks m ∈ {0, 1}|V | over the vocabulary. This approach also benefits from
parallelizing a substantial portion of the syntactical LLM generation computations by offloading them to a
GPU during inference.
Furthermore, it is challenging to ensure generality with efficiency. Many prior works are restricted to syntactic
generation with a specific type of decoding (Scholak et al., 2021; Lundberg et al., 2023). At k-th LLM
iteration, for partial LLM output Ck , let Vk ⊆ V denotes the subset of vocabulary such that for any token
t ∈ Vk the intermediate generation continues to maintain the invariant Ck .t ∈ Lp (G). Our formulation for
computing Vk from V is highly general and can be integrated with any decoding algorithm, such as greedy,
sampling, or beam-search. Any algorithm that could potentially be applied to V can instead be applied to
Vk . The mask store allows more efficient computation of a subset of tokens Vk .
SynCode works in two steps: first, it parses Ck and computes the unparsed remainder r ∈ Σ∗ along with
the acceptable terminal sequences A (formally defined in Section 4.2). In the second step, SynCode utilizes
r, A, and the mask store. This step involves traversing the DFA and performing a few lookups within the
DFA mask store to obtain a subset of tokens Vk . In the following sections, we elaborate on these steps
using our illustrative example.
Parsing Partial Output. SynCode’s parsing of partial output Ck begins with lexing Ck . We assume
our lexer has a 1-character lookahead and no backtracking. This assumption ensures that LLM’s future
generations do not alter the lexical types of any previous lexical tokens except for the final lexical token.
The remainder r denotes the suffix of Ck that may still change its lexical type in subsequent iterations. We
define two cases for assigning r:


• Case 1 is when Ck contains an unlexed suffix u, and here we assign r = u. For example,
  Ck = math_sqrt(3) * (2. is lexed as math_sqrt , ( , 3 , ) , * , ( , 2. , where math_sqrt ,
   ( , 3 , ) , * , ( are lexical tokens of type math_sqrt, lpar, int, rpar, mult, lpar, respectively. Here
   2. ( 2 followed by a . ) is unlexed suffix which we assign as the remainder r.

• Case 2 is when Ck ends with a complete lexical token, where r is assigned the value of the final lexical token.
  Hence, Ck = math_sqrt(3) * (2 is lexed as math_sqrt , ( , 3 , ) , * , ( , 2 . Where math_sqrt ,
    ( , 3 , ) , * , ( are lexical tokens of type math_sqrt, lpar, int, rpar, mult, lpar, respectively. Although
    2 is the complete final lexical token with type int, it is assigned as the remainder since in the subsequent
   iteration it may even change its lexical type to float.


In both cases, our lexer assumption ensures that the portion of Ck excluding the remainder r will retain its
lexical tokenization in subsequent LLM iterations. The assumption is crucial to enable incremental parsing
and ensures that that the remainder r is always small, both of which contribute to reducing time complexity.
Accept Sequences. Given a sequence of lexical tokens l1 , . . . lf , we use a bottom-up LR parser to compute
what types of lexical tokens are acceptable next according to the grammar. If at a certain point in the
generation, we have lexical tokens math_sqrt , ( , 3 , ) , * , ( , 2.27 then the immediate next lexical
token can be of type rpar, add or mult. We define an accept sequence as a function of the parsed partial
output (excluding the remainder) as a sequence of terminals such that those terminals can follow the currently
parsed output (Definition 7). For instance, in the case Ck = math_sqrt(3) * (2.27 , {rpar}, {add} and
{mult} all are 1-length accept sequences. {add, int} and {add, float} are some of the 2-length accept sequences
for this example that can follow the current partial output. In Section 4.2, we show how we efficiently
compute accept sequences of length 1 and 2 using an LR(1) parser, leveraging its immediate error detection
property (Aho and Johnson, 1974). Further, we discuss how an LR(κ) parser can be used to compute accept
sequences of length κ efficiently. However, in practice, SynCode can effectively operate with shorter accept
sequences while still ensuring the soundness of syntactical generation (see Theorem 1), thereby avoiding the
high memory needed for LR(κ) parsers for large values of κ.


                                                       7
DFA Mask Store. SynCode parsing step partitions partial output Ck into lexically fixed part Ck□ and
remainder r. The accept sequences A are computed using the parser state on parsing Ck□ and denote the
terminals that can follow Ck□ . Thus the problem of obtaining subset Vk of tokens that will lead to syntactical
continuation can be reduced to aligning accept sequence Λ ∈ A with the string r.t obtained by concatenating
remainder r and LLM token t in the vocabulary. One approach is to iterate through LLM vocabulary V
and verify this alignment for each token t individually. However, this method is inefficient due to the need
for matching |V | tokens with |A| terminal sequences. In SynCode algorithm, the precomputed DFA mask
store is crucial for allowing efficient computation of acceptable tokens Vk . Next, we show how the mask
store maps the states of DFAs of the terminals and a sequence of terminals to masks over the vocabulary to
enable this process.
Given a remainder r and any accept sequence Λ ∈ A, we want to check for a token t ∈ V , if r.t aligns or
partially matches with Λ. We formally define this notion of partial match in Definition 8. We establish a
connection between the match of a terminal sequence and a string through the DFAs corresponding to the
terminals.
                               Figure 6 presents a DFA for the terminal int. In this DFA, q0int is the start
                               state, and q1int is an accept state. Further, we say that q0int , q1int are live states
                               since there is a path from those states to an accept state and the state q2int is
                               not a live state.
                               Consider the partial output Ck = math_sqrt(3) * (2 . As described above,
                               in this case, the output is split in the parsed part math_sqrt(3) * ( and the
                               last lexical token 2 which is the remainder. {int, add}, {int, rpar}, {float} are
                               some of the accept sequences. For each of these accept sequences, we want to
Figure 6: DFA for terminal     compute tokens t ∈ V such that appending 2 and t i.e. 2 .t partially matches
int.                           the accept sequence.
                               Consider an accept sequence Λ = {float, rpar}. Figure 7 displays the DFAs
                               corresponding to the terminals in Λ. If we begin from the initial state q0float of
Dfloat and change the current DFA state according to the characters in r, in our example with r = 2 , the
resulting state of the DFA is q1float . We observe that any token t ∈ V is acceptable if continuing the DFA
walk from q1float ends on a live state. We also allow a transition from the end state and start state of DFAs
of subsequent terminals in the accept sequence as shown by the dotted arrow. The partial match of r.t
and Λ can thus be equivalently checked by doing a walk over the DFAs. Tokens such as 11 , . , .1 ,
and .27) are some of the tokens where initiating a walk from q1float leads to reaching one of the live states.
For example, by consuming .27) , we reach q1rpar , which is a live state. Consequently, SynCode approves
.27) as a valid continuation from Ck = math_sqrt(3) * (2 .
Our key insight for achieving efficiency is that for each DFA state, we can precompute LLM tokens that will
lead to a transition to a live state starting from that state. Precomputing these sets can significantly reduce
the computation required during inference. Further, these precomputed set of LLM tokens can be stored
as boolean masks for efficiently combining them during inference. Given a DFA state q and any sequence
terminals of length α, the mask store maps Mα (q, Λ) = m, where m ∈ {0, 1}|V | is the mask over vocabulary.
During the inference time, for each accept sequence Λ ∈ A, we first consume r and walk over the first DFA




                             Figure 7: DFAs for accept sequence Λ = {float, rpar}.
                                                         8
in the accept sequence. We then use the map Mα on the current DFA state to get the mask mΛ of valid
tokens for Λ. Hence, for each accept sequence Λ ∈ A, we require a walk over a DFA and a lookup in the
mask store to obtain mΛ .
Finally, we combine these masks obtained
                                       S for each acccept sequence to get the masks of all syntactically
valid tokens by computing their union Λ∈A mΛ . In practice, these masks can be stored as tensors and can
be combined efficiently using a small number of tensor union operations. We show in Theorem 1 that this
combined mask overapproximates the set Vk , ensuring the soundness of our approach. Further, we show
that for the LR parser with larger lookahead, our approach is complete and ensures the combined mask is
exactly Vk (Theorem 2).
Bringing It All Together. In our example, SynCode improves the LLM’s output by guiding the gen-
eration. Initially, the LLM produces math as C1 . Next, SynCode excludes LLMs top choices such as
 _area , _tri , and _p from the vocabulary, leading the decoding algorithm to select _sqrt . Further,
even in the 12th iteration where the LLM outputs C11 = math_sqrt(3)/4 * (2.27 , SynCode filters out
the LLM’s preferred choice ˆ from the vocabulary. Instead, the LLM opts for ∗, eventually generating Cn =
 math_sqrt(3)/4 * (2.27) * (2.27) , which is syntactically correct i.e. Cn ∈ L(G) and also semantically
accurate.

3.3   Time Complexity

At each decoding step in SynCode, the most resource-intensive tasks are computing accept sequences and
generating the mask using r and A. In Section 4.6, we demonstrate that our implementation, leveraging
LR(1) parsing, efficiently constructs 1 and 2-length accept sequences. We show that the complexity of
SynCode at each decoding step is O(T∪ · |A|), where T∪ represents the time needed for boolean mask union
operations. Typically, |A| is small (<10 on average in our experiments) and in the worst case, it equals
the size of set of all terminals |Γ| in the grammar. For our largest Python grammar, |Γ| is 94. Modern
hardware, especially with GPUs, can perform these vectorized union operations efficiently (Paszke et al.,
2019b), making the SynCode algorithm efficient in practice.

4     Syntactically Correct Generation

This section describes our main technical contributions and the SynCode algorithm.

4.1   Syntactical Decoding Problem

Given a language with grammar G, let L(G) ⊆ Σ∗ denote the set of all syntactically valid outputs according
to the grammar G. For a grammar G, Lp (G) represents the set of all syntactically valid partial outputs. If
a string w1 belongs to Lp (G), then there exists another string w2 such that appending w2 to w1 results in a
string that is in the language defined by G. Formally,
Definition 3 (Partial Outputs). For grammar G, Lp (G) ⊆ Σ∗ denotes all syntactically valid partial outputs.
Formally, if w1 ∈ Lp (G) then ∃w2 ∈ Σ∗ such that w1 .w2 ∈ L(G)

For a grammar G and a partial output Ck belonging to the set of prefix strings Lp (G), the syntactical decoding
problem aims to determine the set Vk of valid tokens from a finite vocabulary V such that appending any
token t ∈ Vk to Ck maintains its syntactic validity according to the grammar G.
Definition 4 (Syntactical Decoding). For grammar G, given partial output Ck ∈ Lp (G) and finite token
vocabulary V ⊂ Σ∗ , the syntactical decoding problem is to compute the set Vk ⊆ V such that for any
t ∈ Vk , Ck .t ∈ Lp (G)

We next present SynCode’s key aspects to solve this problem:

• In the initial step, it parses Ck and computes the unparsed remainder r ∈ Σ∗ along with the acceptable
  terminal sequences A (Section 4.2).


                                                      9
• In the second step, SynCode utilizes r, A, and the precomputed mask store. This phase involves travers-
  ing the DFA and performing a few lookups within the DFA mask store to obtain the set of syntactically
  valid tokens t capable of extending Ck (Section 4.3).
• Consequently, SynCode efficiently computes the set of syntactically valid tokens. We show the soundness
  and completeness of our approach in Section 4.4.
• We further discuss the theoretical complexity of SynCode in Section 4.6 and the SynCode framework
  in Section 4.7.

4.2   Parsing Partial Output

In this section, we describe the remainder r and accept sequences A returned by the parsing step.
Remainder. SynCode uses a lexer to convert Ck to sequence of lexical tokens l1 , l2 . . . lf ∈ Σ∗ . Each lexical
token li is associated with a terminal type τi , where li ∈ L(ρτi ) (ρτi is the regular expression for terminal
τi ). We assume our lexer uses a 1-character lookahead without backtracking. This ensures that the lexical
types of previous tokens in Ck remain unchanged, except for the final token. The remainder r represents
the suffix of Ck that could potentially change its lexical type in future iterations. Thus the remainder r is
assigned such that it is either unlexed because it does not match any terminal, or has been lexed but might
undergo a different lexing in subsequent iterations when Ck is extended by the LLM by appending tokens.
This assumption is crucial for enabling incremental parsing and ensures that the remainder r remains small,
which contributes to reducing overall time complexity. SynCode assigns the remainder according to the
following two cases:

 Case 1: Ck = l1 .l2 . . . lf Assuming a standard lexer with 1-character lookahead and no backtracking,
      all lexical tokens l1 , l2 , . . . , lf −1 remain unchanged upon extending Ck . However, the final lexical
      token lf may change. For example, in Python partial output in the k-th LLM iteration, if the final
      lexical token is lf = ret and the language model generates the token urn in the next iteration,
      the updated code results in the final lexical token becoming lf = return . This transition reflects a
      transformation from an identifier name to a Python keyword in the subsequent iterations. Thus, r
      is assigned the value lf , i.e., r = ret for k-th iteration in our example.
 Case 2: Ck = l1 .l2 . . . lf .u: Here, u ∈ Σ∗ is the unlexed remainder of Ck . In this case, considering
      the 1-character lookahead of the lexer, the types of l1 , l2 , . . . , lf do not change upon extending Ck .
      Consequently, r is assigned value u of the suffix that remains unlexed.

 SynCode parsing step partitions partial output Ck into lexically fixed part Ck□ and remainder r. Given a
sequence Λ = τ0 , τ1 , . . . , τf , we simplify notation by using L(Λ) = L(ρτ0 · ρτ1 . . . ρτf ) throughout the rest of
the paper.
Definition 5 (Partial Parse). Given the partial output Ck ∈ Σ∗ , the partial parse function pparse : Σ∗ →
Γ∗ × Σ∗ returns a terminal sequence Λ□ and remainder r such that Ck = Ck□ .r and Ck□ is parsed as Λ□ . i.e.
Ck□ ∈ L(Λ□ ).

Accept Sequences. A sentence is a sequence of terminals. A grammar G describes a (possibly infinite)
set of sentences, that can be derived by using the production rules of the grammar. We use LΓ (G) ⊆ Γ∗ to
denote the valid sequences of terminals that can be derived from the rules of G. Further, LΓp (G) denotes all
syntactically valid partial sentences of terminals. Formally,
Definition 6 (Partial Sentences). We define a set of all syntactically valid partial sentences LΓp (G) ⊆ Γ∗
such that Λ ∈ LΓp (G) if and only if ∃Λ1 ∈ Γ∗ such that Λ.Λ1 ∈ LΓ (G).

Note that L(G) and Lp (G) are defined over alphabet Σ, whereas LΓ (G) and LΓp (G) over terminals Γ.
Nevertheless, if a program C is parsed to obtain terminal sequence Λ, then C ∈ L(G) is equivalent to
Λ ∈ LΓ (G). The SynCode parsing algorithm obtains Λ□ = τ1 , τ2 . . . τf by parsing Ck corresponding to the
parserd part of partial output Ck□ . Given a partial sentence Λ□ , an accept sequence is a sequence over Γ
such that when appended to Λ□ the result is still a partial sentence.


                                                          10
Definition 7 (Accept Sequence). Given partial output Ck ∈ Lp (G), and Λ□ , r = pparse(Ck ), Λ1 ∈ Γ∗ is an
accept sequence if Λ□ .Λ1 ∈ LΓp (G).

Consider a Python partial program Ck = def is and let def, name, lpar and rpar be the terminals in Python
grammar. we get {def}, is = pparse( def is ), where Λ□ = {def} and r = is . Λ1 = {name, lpar, rpar}
is an accept sequence in this case as the sequence of terminals Λ□ .Λ1 = {def, name, lpar, rpar} is a valid
partial sentence. The parser state on parsing the partial output Ck can be utilized to compute a set of
accept sequences denoted as A. The soundness and completeness of the SynCode algorithm depend on the
length of these accept sequences in A. In theory, using longer accept sequences enhances the precision of the
SynCode algorithm at the cost of increased computational complexity. In Section 4.5, we show our method
for obtaining 1 and 2-length accept sequences that are efficient and precise in practice.

4.3   Grammar Mask

This section outlines the utilization of the set of acceptable terminal sequences A and the remainder r in
the creation of a boolean mask using the DFA mask store which is subsequently used for constraining the
LLM output. The DFA mask store is constructed offline and makes SynCode efficient during the LLM
generation. Given partial output Ck , our objective is to identify tokens t ∈ V such that appending them
to Ck leads to syntactical completion. Given remainder r and set of sequences A, the goal is to determine
whether r.t partially matches the regular expression derived from any of the sequences in A. To characterize
the notion of strings partially matching a regular expression, we next introduce the function pmatch.
Definition 8 (pmatch). The function pmatch takes a word w ∈ Σ∗ , a regular expression ρ and returns a
boolean. pmatch(w, ρ) = true if either of the following conditions holds:

      1. ∃w1 ∈ Σ∗ , w2 ∈ Σ+ such that w = w1 .w2 and w1 ∈ L(ρ) or
      2. ∃w1 ∈ Σ∗ such that w.w1 ∈ L(ρ)

Thus pmatch(w, ρ) is true when either a prefix of w matches ρ or w can be extended to match ρ. The
consequence of allowing pmatch to be defined such that it is true even when prefix matches, is that Syn-
Code will conservatively accept all tokens for which the prefix matches the accept sequence. Hence, we
overapproximate the precise set of syntactically valid tokens. We make this choice to ensure that SynCode
is sound for any length of accept sequences. Next, we give definitions related to DFAs. These definitions are
useful for describing the construction of the DFA mask store and proving properties related to its correctness
in the SynCode algorithm. In particular, we first define the live states of DFA. We say state q is live if
there is a path from q to any final states in F . Formally,
Definition 9 (DFA live states). Given a DFA D(Q, Σ, δ, q0 , F ), let live(Q) ⊆ Q denote the set of live states
such that
                                   q ∈ live(Q) iff ∃w ∈ Σ∗ s.t. δ ∗ (w, q) ∈ F

We use Dτ (Qτ , Στ , δτ , q0τ , Fτ ) to denote a DFA corresponding to a terminal τ ∈ Γ. Next, we establish the
definition of dmatch for DFA, which is an equivalent concept to pmatch with regular expressions. dmatch is
recursively defined such that its computation can be performed by walking over the DFAs of a sequence of
terminals.
Definition 10 (dmatch). Given a DFA D(Q, Σ, δ, q0 , F ), a string w ∈ Σ∗ , a DFA state q ∈ Q and any
sequence of terminals Λ = {τf +1 , τf +2 . . . τf +d }, dmatch(w, q, Λ) = true, if either of the following conditions
hold:

      1. δ ∗ (w, q) ∈ live(Q) or
      2. ∃w1 ∈ Σ∗ , w2 ∈ Σ+ such that w1 .w2 = w, δ ∗ (w1 , q) ∈ F and Λ = {} or
      3. ∃w1 ∈ Σ∗ , w2 ∈ Σ∗ such that w1 .w2 = w, δ ∗ (w1 , q) ∈ F ,
                          τ                                           τ
         and dmatch(w2 , q0f +1 , {τf +2 . . . τf +d }) = true where q0f +1 is the start state corresponding to the DFA
         for τf +1


                                                          11
Given an accept sequence Λ = {τf +1 , τf +2 . . . τf +d } ∈ A, our objective is to compute the set of tokens
t ∈ V such that pmatch(r.t, ρΛ ) holds, where ρΛ = (ρf +1 .ρf +2 . . . . .ρf +d ) is the regular expression obtained
by concatenating regular expressions for terminals. If Λp denotes the sequence {τf +2 , . . . τf +d }, Lemma 1
simplifies this problem to finding dmatch(r.t, q0τ1 , Λp ). Furthermore, utilizing Lemma 2, this can be further
reduced to computing q = δτ∗1 (r, q0τ1 ) and dmatch(t, q, Λp ). It’s important to note that dmatch(t, q, Λp )
does not depend on Ck and can be computed offline. While the computation of q for dmatch(t, q, Λp ) is
relatively inexpensive, evaluating dmatch(t, q, Λp ) can be computationally expensive both offline and online,
as it requires considering numerous potential accept sequences offline, and where it needs to iterate over
all tokens in V online. We observe that if we consider sequences of smaller lengths, we can efficiently
precompute the set of tokens satisfying dmatch(t, q, Λp ) for all q, t and Λp offline. We later establish the
soundness of SynCode when using accept sequences of length at least 1 (Theorem 1) and completeness
for accept sequences of the length greater than maximum length of tokens in the vocabulary (Theorem 2).
Typically, LLM tokens are small in size, allowing us to obtain these guarantees.
Lemma 1. Given Λ = {τf +1 , τf +2 . . . τf +d }, Λp = {τf +2 . . . τf +d } and ρΛ = (ρf +1 , ρf +2 , . . . , ρf +d ),
dmatch(w, q0τ1 , Λp ) ⇐⇒ pmatch(w, ρΛ ).

Lemma 2. If q = δτ∗ (r, q0τ ) and no prefix of r is in L(τ ) i.e. ∄w1 ∈ Σ∗ , w2 ∈ Σ∗ such that w1 .w2 =
r and δτ∗ (w1 , q0τ ) ∈ Fτ then dmatch(t, q, Λ) ⇐⇒ dmatch(r.t, q0τ , Λ).

The proofs of both the lemmas are in Appendix A.2.
Illustrative Example: Consider the scenario with Ck = def is , r = is , and an accept sequence
Λ = {name, lpar, rpar} in A, where name, lpar, and rpar are terminals in Γ. Our objective is to determine all
t ∈ V such that def is .t forms a valid partial program. This can be achieved by finding tokens t that satisfy
pmatch( is .t, ρΛ ), where ρΛ = [a-z, A-Z, _]∗ (). Let’s consider a token t = _prime(): . We observe that
r.t = is_prime(): can be decomposed into is_prime (name), ( (lpar), ) (rpar), and : . Consequently,
it partially matches ρΛ as defined by pmatch. In Figure 9, we present the DFAs for Λ used in computing
dmatch. The reduction dmatch(r.t, q0name , lpar, rpar) = dmatch( is_prime(): , q0name , lpar, rpar) simplifies
successively to dmatch( (): , q0lpar , rpar), then to dmatch( ): , q0rpar , ), and finally to dmatch( : , q1rpar , ). As
q1rpar is a final state, according to condition 2 of Definition 10, dmatch( : , q1rpar , ) holds true. Next, we define
a mask over vocabulary
Definition 11 (Vocabulary mask). Given vocabulary V ⊆ Σ∗ , m ∈ {0, 1}|V | is a mask over the vocabulary.
We also use set(m) ⊆ V to denote the subset represented by m.

DFA Mask Store For an integer α, we define a DFA table S        Mα as the mask store over the DFA states
with α lookahead. Given the set of all DFA states QΩ = τ ∈Γ Qτ , the table stores binary masks of
size |V |, indicating for token string t, for any DFA state q ∈ QΩ and a sequence of α terminals Λα if
dmatch(t, q, Λα ) = true. The lookahead parameter α signifies the number of subsequent terminals considered
when generating the mask stored in the table. Choosing a larger value for α enhances the precision of
SynCode algorithm, but it comes at the cost of computing and storing a larger table. We next formally
define the DFA mask store,




Figure 8: DFAs in accept sequence Λ = {name, lpar, rpar} for example. The start state, final states, and
dead states are in gray, green, and red respectively. The dashed arrows link the final states of one DFA to
the starting state of the next DFA, adhering to condition 3 in Definition 10. This illustrates the sequential
traversal across DFAs during the computation of dmatch.

                                                          12
Definition 12 (DFA mask store). For an   S integer α, the DFA mask store Mα is a function defined as
Mα : QΩ × Γα → {0, 1}|V | , where QΩ = τ ∈Γ Qτ represents the set of all DFA states and Γα is a set of
α-length terminal sequences. Then Mα (q, Λ) = m is a binary mask such that t ∈ set(m) if dmatch(t, q, Λ)

For our illustrative example if m = M2 (q1name , {lpar, rpar}) then t = _prime(): should be contained in
set(m). The grammar mask for a set of accept sequences A can be computed by combining masks for
each Λ ∈ A. The DFA mask store M0 maps each DFA state to all tokens such that they pmatch without
considering any following accept sequence (0-length sequence). In this case, the table maps each state with
a single mask denoting the tokens that match the regular expression of the corresponding DFA.
Computing Grammar Mask The mask store is constructed offline by enumerating all DFA states QΩ ,
considering all possible terminals in Γ, and all tokens in V . The DFA mask store depends on the set of
terminals Γ and the model’s vocabulary V . As a result, a unique mask store is created for each grammar
and tokenizer combination, and to enhance efficiency, we cache and reuse this table for future inferences.
Algorithm 2 presents our approach for comput- Algorithm 2 Computing Grammar Mask
ing the grammar mask during LLM generation. Inputs: A: set of accept sequences, r: remainder
It computes a grammar mask based on the sets
                                                      1: function GrammarMask(A, r)
of current accept sequences A, and the remain-
                                                      2:    m ← {}
der string (r). It iterates over A, considering
                                                      3:    for Λ ∈ A do
each sequence Λ. The algorithm initializes an
                                                      4:       τ1 ← Λ[0]
empty mask m. It iterates over each accept-
                                                      5:       qr ← δ ∗ (q0τ1 , r)
able sequence, considering the first terminal τ1
                                                      6:       if qr ∈ live(Qτ1 ) then
in each. It computes the resulting state qr by
                                         τ1           7:           Π ← len(Λ) − 1
processing τ1 from an initial state q0 and the                                             
                                                      8:           m ← m ∪ MΠ (qr , Λ[1 :])
remainder string r. If qr is in a live state, the al-
gorithm updates the grammar mask by unifying          9:    return m
the mask cached in Mα .

4.4   Soundness and Completeness

This section establishes the soundness and completeness of the SynCode algorithm. Algorithm 3 presents
the LLM generation algorithm with SynCode. It takes as inputs an LLM represented by M , a tokenizer
denoted by T , an input prompt string C0 , the maximum number of generated tokens nmax , and a base
decoding strategy D. The algorithm begins by tokenizing the input prompt using the tokenizer. It then
iteratively generates tokens using the LLM, decodes the current token sequence, and performs parsing to
obtain acceptable terminal sequences A, and a remainder r (line 6). A grammar mask is applied to the logit
scores based on these values (line 7). The algorithm subsequently selects the next token using the decoding
strategy, and if the end-of-sequence token (EOS) is encountered, the process terminates. The final decoded
output is obtained, incorporating the generated tokens, and is returned as the result of the MaskedGenerate
algorithm.
Given partial output Ck ∈ Lp (G), SynCode generates a corresponding mask m. If, for a token t ∈ V , the
concatenation Ck .t results in a syntactically valid partial output, i.e. Ck .t ∈ Lp (G), our soundness theorem
ensures that t is indeed a member of the set defined by the generated mask m. The subsequent theorem
formally states this soundness property.
Theorem 1. Let Ck ∈ Lp (G) be the partial output and any integer d ≥ 1, let Ad ⊆ Γd contain all possible
accept terminal sequences of length d and r ∈ Σ∗ denote the remainder. If m = GrammarMask(A, r) then
for any t ∈ V , if Ck .t ∈ Lp (G) then t ∈ set(m)

The proof of the theorem is in Appendix A.2.
Next, we give a definition that establishes a partial order on sets of terminal sequences, where given two sets
A1 and A2 , we say sets A1 ≼ A2 if every sequence in A2 has a prefix in A1 .
Definition 13 (≼). We define a partial order ≼ on set of terminal sequences P(Γ∗ ) such that A1 ≼ A2
when ∀Λ2 ∈ A2 ∃Λ1 ∈ A1 ∃Λ3 ∈ Γ∗ s.t. Λ2 = Λ1 .Λ3


                                                      13
We further state the lemma that shows the relation
in the grammar masks generated by two accept se- Algorithm 3 SynCode Generation
quences satisfying relation ≼.                     Inputs: M : LLM, T : tokenizer, C0 : input prompt, nmax :
Lemma 3. Given A1 and A2 are set of maximum generated tokens, D: decoding strategy
accept sequences such that A1 ≼ A2 and 1: function MaskedGenerate(M , T , C0 , nmax , D)
m1     =    GrammarMask(A1 , r) and m2           = 2:    Tcur ← Tokenize(T , C0 )
GrammarMask(A2 , r) then set(m2 ) ⊆ set(m1 )        3:   for i ∈ {1, . . . nmax } do
                                                       4:      scores ← M (Tcur )
The proof of the lemma is in Appendix A.2.             5:      Ck ← decode(T , Tcur )
                                                       6:      A, r ← Parse(Ck )
Theorem 1 proves soundness for accept sequences
                                                       7:      m ← GrammarMask(A, r)
Ad of length d, while Lemma 3 extends this proof       8:      scores ← m ⊙ scores
to any set of accept sequences A where A ≼ Ad .        9:      ti ← D(scores)
Our implementation, employing sequences of vary-      10:      if ti = EOS then
ing lengths, can be proven sound based on this ex-    11:          break
tension.                                              12:      Tcur ← append(Tcur , ti )
The completeness theorem ensures that, under spec- 13:      output ← decode(T , Tcur )
                                                      14:   return output
ified conditions, each token t ∈ set(m) guarantees
Ck .t as a syntactically valid partial output. An im-
plementation of SynCode with a short length of
accept sequences although sound, may not guarantee completeness. To illustrate, let’s take the example
where Λ = τf +1 , τf +2 ∈ A with simple singleton regular expressions ρτf +1 = ( and ρτf +2 = ( . In this
case, our algorithm conservatively treats all tokens t ∈ V as syntactically valid, whenever (( is a prefix
of those tokens (e.g., ((( , (() )) even though some tokens may not meet syntactic validity. However, by
assuming that the accept sequences are long enough, we can establish the completeness of the approach.
Theorem 2. Let Ck ∈ Lp (G) be the partial output, let Ad ⊆ Γd contain all possible accept terminal
sequences of length d and r ∈ Σ∗ denote the remainder. Suppose for any t ∈ V, d > len(t) and m =
GrammarMask(Ad , r) such that t ∈ set(m) then Ck .t ∈ Lp (G)

The proof of the theorem is in Appendix A.2. While our completeness theorem ensures the SynCode
consistently extends syntactically correct partial outputs, it does not guarantee termination with a correct
and complete output. The focus of the theorem is on generating syntactically valid partial outputs, and the
theorem does not address whether the process converges to a syntactically correct whole output. Termination
considerations go beyond the completeness theorem’s scope.

4.5   SynCode Implementation

Base LR parser:         Bottom-up LR parsers, including LR(1) and LALR(1) parsers, process terminals
generated from the lexical analysis of the code sequentially and perform shift or reduce operations (Aho
et al., 1986). LR(κ) parsers have the immediate error detection property, ensuring they do not perform shift
or reduce operations if the next input κ terminals on the input tape is erroneous (Aho and Johnson, 1974).
Consequently, every entry in the parsing table corresponding to κ terminals that maps to a shift or reduce
operation indicates that the terminal is acceptable. This property allows us to use LR(1) parsing tables
to efficiently compute accept sequences at any intermediate point, making them preferable for SynCode
applications. Thus, computing acceptable terminals with LR(1) parsers has a complexity of O(|Γ|). Although
LALR(1) parsers are more commonly used due to their smaller memory requirements and faster construction,
computing acceptable terminals with them requires iterating over all terminals leading to a complexity of
O(TP · |Γ|) due to the need for multiple reduce operations before confirming the validity of each terminal.
Furthermore, while for κ > 1, LR(κ) parsers can compute accept sequences of length κ immediately, they
incur extremely high memory requirements. Additionally, while we can use LL(κ) parsing tables to compute
the next κ accept terminals, LR(κ) parsers offer a higher degree of parsing power. Therefore, we employ
LR parsers in SynCode. Our evaluation indicates that LR(1) parsers suffice for eliminating most syntax
errors, making them a practical choice for SynCode. We discuss how the implementation of how parsing
is performed incrementally to obtain the accept sequences and remainder in the Appendix A.3.


                                                     14
Accept Sequences: In our implementation, we focus on generating accept sequences of length 1 or 2, as
they can be efficiently obtained from LR(1) parser. While this approach incurs some loss of precision, it
leads to sound but incomplete syntactical decoding. Further, our evaluation demonstrates that this strategy
is efficient and precise in practical scenarios. We note that pmatch r.t with a 2-length sequence is equivalent
to dmatch with a 1-length sequence, as stated in Lemma 1. Consequently, in our work, we precompute mask
stores M0 and M1 . On parsing the partial output Ck , the parser state of LR(1) parsers can be used to
directly obtain syntactically acceptable terminals for the current completion (A0 ) and the next completion
(A1 ). We utilize A0 and A1 to construct the accept sequences A, considering two cases:
Case 1: Ck = l1 .l2 . . . lf : Let τf represent the type of the final lexical token. In many instances, a
token may be extended in the subsequent generation step, such as when an identifier name grows longer or
additional words are appended to a comment. In those cases if A1 = τ11 , τ21 , . . . , τn1 , we include all 2-length
sequences {τf , τi1 } for each i. As previously discussed, the type of the final lexical token may change from
τf . Consequently, when A0 = {τ10 , τ20 , . . . , τn0 }, we add 1-length sequences Λi for each terminal sequence {τi }
from A0 , excluding τf . This method ensures the generation of sequences accounting for potential extensions
of the same token and changes in the type of the final lexical token.
Case 2 Ck = l1 .l2 . . . lf .u: In this scenario, the current terminal is incomplete, leading to a lack of information
about subsequent terminals. Consequently, when A1 = {τ1 , τ2 , . . . , τn }, we define A as a set of sequences:
{Λ1 , Λ2 , . . . , Λn }, where each Λi corresponds to a single terminal sequence {τi } from A1 . Specifically, Λ1 =
{τ1 }, Λ2 = {τ2 }, and so forth.




4.6   Time Complexity


In this section, we analyze the time complexity of the SynCode algorithm. We focus on the cost of creating
the mask at each iteration of the LLM generation loop. The key computations involved in this process
are the parsing carried out by the incremental parser to compute A and the lookup/unification operations
performed through the DFA mask store.
The incremental parser parses O(1) new tokens at each iteration and computes A. Let TA represent the
time taken by the parser to compute the accepted terminals and TP denote the time the parser takes to
parse a new token and update the parser state. Hence, in each iteration, the parser consumes O(TA + TP )
time to generate A. The DFA mask store lookup involves traversing |A| DFA sequences, with the number
of steps in this walk bounded by the length of the remainder r. As A can have a maximum of |Γ| sequences,
the DFA walk consumes O(|Γ| · len(r)) time. We employ a hashmap to facilitate efficient lookups at each
DFA node, ensuring that all lookups take constant time. Consequently, this step takes O(|Γ|) time. Let T∪
denote the time taken for computing the union of binary masks. With potentially |Γ| union operations to
be performed, the mask computation takes O(T∪ · |Γ|) time. Therefore, the overall time complexity at each
step during generation is given by O(TA + TP + |Γ| · len(r) + T∪ · |Γ|).
For an incremental LR(1) parser, the complexity of our algorithm at each step of LLM token generation is
O(|Γ| · len(r) + T∪ · |Γ|). With our lexer assumption, we ensure that the remainder r is small, allowing us to
further simplify our complexity analysis to O(T∪ · |Γ|) by treating len(r) as constant.
Offline cost:     The cost of computing the mask store Mα offline involves considering all DFA states
q ∈ QΩ , all possible terminal sequences of length α, and all tokens t ∈ V . Given that we need to traverse
the DFA for len(t) steps for each entry in the store, the time complexity for computing the mask store is
O(maxt∈V (len(t)).|QΩ |.|V |.|Γ|α ). Typically, len(t) is small, allowing us to simplify this to O(|QΩ |.|V |.|Γ|α ).
In our implementation, the use of M0 and M1 results in a cost of O(|QΩ |.|V |.|Γ|). The size of |QΩ | depends
on the complexity of regular expressions for the terminals, which may vary for each grammar. However,
as demonstrated in our evaluation section, these mask stores can be computed within 10 minutes for each
combination of grammar and LLM. This computation is a one-time cost that can be amortized over all
generations performed for the given LLM and grammar.


                                                         15
Figure 9: The upper section displays erroneous output from a standard LLM generation, failing to produce
the intended JSON format. The lower segment showcases the fix achieved through the use of the SynCode
framework.

4.7   SynCode Framework

Figure 9 shows how SynCode framework can be used in practice by selecting a grammar. We next discuss
other important features of the framework.
Adding a New Grammar. Our Python-based SynCode framework is shipped with several built-in
grammars such as JSON, Python, Go, etc. A user can apply SynCode for arbitrary grammar by providing
the grammar rules in EBNF syntax with little effort. The grammar needs to be unambiguous LALR(1) or
LR(1) grammar for using the respective base parsers.
Ignore Terminals. Our EBNF syntax adopted from Lark allows one to provide ignore terminals as part
of the grammar. Lark ignores those terminals while parsing. In the case of Python, this includes comments
and whitespaces. SynCode handles these ignore terminals by adding a trivial 1-length accept sequence for
each of these ignore terminals.
Parsers. SynCode supports both LALR(1) and LR(1) as base parsers. We adapt Lark’s (Lark, ) LALR(1)
parser generator for SynCode. Since Lark does not implement the LR(1) parser generator, we implemented
the LR(1) parser generator on top of the Lark. The generation of LR(1) parser which is performed offline may
take longer time compared to the LALR(1) parser (e.g., up to 2 mins for our Python grammar), however, it is
more efficient at inference time in computing the accept sequences. Further, since the Lark-generated parser
is non-incremental, we build the incremental parser on top of it by caching the parser state as described in
Appendix A.3.
Non-CFG Fragments of PLs. SynCode can handle non-context-free fragments of PLs, such as inden-
tation in Python and end-of-scope markers in Go. To support languages with indentation, such as Python
and YAML, SynCode has a mechanism that tracks acceptable indentation for the next token, effectively
masking tokens that violate indentation constraints at a given point. This indentation constraint feature can
be enabled with any new grammar. Similarly, for handling other custom parsing rules beyond CFGs, users
can add additional constraints to the generation by overriding specific SynCode functions. For instance, in
Go, semicolons are optional and may be automatically inserted at the end of non-blank lines. Implementing
such constraints in SynCode programmatically requires minimal effort. However, SynCode currently does
not support enforcing semantic constraints. (e.g, if a variable in a program is defined before it is used.)


5     Experimental Methodology

Models. In our evaluation, we select a diverse set of state-of-the-art open-weight LLMs of varying sizes.
Since closed-source LLMs, such as GPT-4 or Gemini, do not expose generation logits through their APIs,


                                                     16
applying a constrained generation approach in SynCode is not feasible. Therefore, we focus on enhanc-
ing smaller, open-source models in our evaluation. We select the state-of-the-art models Llama-2-7B-chat
(Touvron et al., 2023b) and Gemma2-2B-it (Team et al., 2024) for our JSON evaluation. For text-2-SQL
generation experiments, we use Llama-2-7B-chat, Llama-3.2-1B, Llama-3.2-3B, and Gemma-2-2B-it. Fur-
thermore, we chose models such as LLaMA-7B (Touvron et al., 2023a), WizardCoder-1B (Luo et al., 2023),
and CodeGen-350M (Nijkamp et al., 2023) for code completion.
Datasets. We focus our evaluation on generating JSON, SQL, Python, and Go outputs. We choose JSON
as it is supported by the baselines (Gerganov and et. al., 2024; Willard and Louf, 2023), which allows us to
compare against them. We selected Python since it is extensively present in the training data employed for
LLM training and fine-tuning. Conversely, we opted for Go due to its lower standard LLM accuracy and a
relatively smaller presence in the training data. We consider JSON-Mode-Eval (NousResearch, 2024) dataset
for text to JSON generation and HumanEval and MBXP (Athiwaratkun et al., 2023) dataset for evaluating
Python and Go code generation. We display examples of prompts from these datasets in Appendix A.7.


     • JSON-Mode-Eval (NousResearch, 2024). It consists of 100 zero-shot problems. Each problem
       prompt follows the chat format with a system prompt specifying a JSON schema and a user prompt
       requesting the LLM to generate a JSON object that contains specified contents.

     • Spider text-2-SQL. Spider (Yu et al., 2018) text-to-SQL dataset consists of 1,034 problems of
       varying difficulty levels: easy (250), medium (440), hard (174), and extra hard (170).

     • Multilingual HumanEval (Athiwaratkun et al., 2023). It is an extension of the original
       HumanEval collection (Chen et al., 2021), which comprises 164 Python programming problems, to
       include other languages like Go. Each problem in the dataset consists of a function definition, and
       text descriptions of the function as a part of the function docstring.

     • MBXP (Athiwaratkun et al., 2023). It is extended from the MBPP (Austin et al., 2021) dataset
       for Python to support other languages such as Go. The dataset consists of 974 problems with the
       same format as HumanEval.


Grammars. For Python, we used the readily available grammar from the Lark repository. For Go, we
converted an existing LL(*) grammar from (ANTLR, ) implementation to LR(1) grammar for our use.
We write the CFG for these languages using the Extended Backus-Naur Form (EBNF) syntax. We use a
substantial subset of grammar for Python and Go syntactic generation with SynCode. The grammar has
commonly used features of the language such as control flow, and loops, and excludes some features such as
Python’s support for lambda functions. Adding support for more features would require more engineering
effort but it will not change the overall technique. The grammars we used are available in Appendix A.8.
The JSON grammar consists of 19 rules and 12 terminals. The Python grammar we used contains 520
production rules and 94 terminals, whereas the Go grammar comprises 349 rules and 87 terminals.
Evaluating Syntax Errors. For evaluating the errors in the generated output in each of the languages,
we use their respective standard compilers.
Experimental Setup. We run experiments on a 48-core Intel Xeon Silver 4214R CPU with 2 NVidia RTX
A5000 GPUs. SynCode is implemented using PyTorch (Paszke et al., 2019a), HuggingFace transformers
library (Wolf et al., 2020) and Lark library (Lark, ).
Baselines. We evaluate three state-of-the-art baselines Outlines (Willard and Louf, 2023) v0.1.1, guid-
ance (Lundberg et al., 2023) v0.1.16, and llama.cpp (Gerganov and et. al., 2024) v0.3.1 in our study. The
algorithmic differences in the baselines and SynCode are discussed in Section 7. We perform a warmup run
for each experiment where we measure inference time to ensure that one-time precomputation time is not
included in the inference runtime. For a fair comparison with baselines, SynCode uses opportunistic mask-
ing (Beurer-Kellner et al., 2024), an optimization used in llama.cpp and guidance. Instead of computing
the full logit vector mask upfront, the model generates a token and only computes the mask if the proposed
token is incorrect.


                                                    17
6     Experimental Results

In this section, we evaluate SynCode on generating various formal languages. We compare SynCode with
state-of-the-art baselines and perform various ablation studies.
SynCode allows the model to generate a special EOS token (indicating the end of generation) only when
the output belongs to L(G). In practice, however, LLM generation typically stopped after a fixed maximum
number of tokens, nmax . Therefore, terminating with the EOS token within this limit is not always guaranteed
potentially resulting in syntax errors.


6.1    Effectiveness of SynCode for JSON Generation


         Table 1: Effectiveness of SynCode in generating JSON with original and explicit prompts.

             Model                   Tool     Syntax Errors       Validation Accuracy (%)    Generation Time (s)
                                            Original  Explicit    Original        Explicit   Original     Explicit
                                SynCode            0         0       66%             84%        3.07          3.02
                                 Standard         98        41        2%             58%        3.58          3.11
             Llama-2-7B-chat    llama.cpp         23        23       63%             68%       21.91         20.84
                                 guidance         13        11       57%             65%        5.14          4.14
                                Outlines†         16        14       62%             56%       38.07         41.79
                                     GCD           2         0       62%             64%        6.08          4.01
                                SynCode            0         0       99%            100%        4.82          4.74
                                 Standard         59        59       41%             41%        4.32          5.82
             Gemma2-2B-it       llama.cpp          7         7       92%             91%       22.06         21.97
                                 guidance          1         1       96%             96%        6.09          5.47
                                 Outlines          2         0       67%             90%        1.99          2.64
                                     GCD           1         0       96%             95%       19.12          9.49

    † We observed issues when using Llama-2-7B-chat with Outlines v0.1.1 and therefore, we use older version v0.0.46.


We evaluate the effectiveness of SynCode in guiding LLMs with the JSON grammar to generate syntactically
correct JSON. We run the inference with Llama-2-7B-chat and Gemma2-2B-it with SynCode, llama.cpp,
Outlines, guidance, GCD, and standard generation on the 100 problems from the JSON-Mode-Eval
dataset. We select these models for the JSON experiment as they are supported by all considered baselines.
We run llama.cpp on a CPU as it requires a specific CUDA version not compatible with our machine.
We set max new tokens nmax = 400. We also report an evaluation of augmenting the prompts with an
explicit request to output only JSON. We present an example of these explicit prompts in Appendix A.7.
We evaluate the correctness of JSON generated by an LLM by first evaluating whether the JSON string can
be parsed and converted to a valid JSON object. We further evaluate whether the generated JSON is valid
against the schema specified in the prompt. Although the SynCode does not enforce the specific schema to
the JSON output for each task, we believe it is an important research question to check whether the reduced
syntax errors due to SynCode can also lead to improved schema validity.
Table 1 presents our evaluation results. We report results for both the prompts taken directly from the
dataset (denoted as "Original") and after augmenting these prompts with an explicit request to output
JSON (denoted as "Explicit"). In the "Validation Accuracy" column, we compute the percentage of valid
completions against their respective schemas. In the "Generation Time (s)" column, we report the average
time taken to generate a completion to a prompt from the dataset. Guiding Llama-2-7B-chat and Gemma2-
2B-it with the JSON grammar via SynCode eliminates syntax errors in generated JSON. On the other hand,
standard generation results in syntactically incorrect JSON for 98% and 59% of completions to the original
prompts for the Llama-2-7B-chat and Gemma2-2B-it models respectively. A majority of these errors are
due to the generation of natural language before and after the JSON. Explicit prompts somewhat mitigate
this issue, but still results in syntactically invalid outputs to 41% and 59% of these prompts for standard
Llama-2-7B-chat and Gemma2-2B-it generation respectively, primarily due to errors such as unmatched
braces and unterminated string literals.llama.cpp, Outlines, guidance, and GCD face similar problems
with closing braces and terminating strings.


                                                             18
Notably, SynCode significantly improves the JSON schema validation accuracy of Gemma2-2B-it com-
pletions over standard generation, from 41% to 99% and 41% to 100% for original and explicit prompts
respectively. Furthermore, SynCode outperforms llama.cpp, Outlines,guidance, and GCD in valida-
tion accuracy of Llama-2-7B-chat completions by 3%, 4%, 9%, and 4% respectively for original prompts
and 16%, 28%, 19%, and 20% for explicit prompts. The remaining schema validation errors with SynCode
are semantic errors, including data type mismatch between the generation JSON and schema, missing fields
required by the schema, and adding extra fields not allowed by the schema. SynCode is faster than all
baseline grammar-guided generation methods for Llama-2-7B-chat and all but Outlines for Gemma2-2B-it.
The low generation time with Outlines for Llama-2-7B-chat can largely be attributed to the fact that many
of its completions to prompts are empty JSON (35% of original and 7% of explicit) which takes few tokens
to generate, but often does not conform to the schema.
Interestingly, we observe that for Llama-2-7B-chat, SynCode also reduces the average generation time
over standard generation. We attribute this finding to the fact that without grammar-guided generation,
the model generates syntactically invalid output, such as natural language, in addition to JSON and thus
generates more tokens in response to the same prompt than with SynCode. Thus, augmenting LLMs with
SynCode can significantly improve syntactical correctness and runtime efficiency.


6.2     Effectiveness of SynCode for SQL Generation

This study demonstrates that SynCode improves text-to-SQL generation by enforcing grammar con-
straints, ensuring that generated SQL queries are syntactically accurate. We evaluate the following mod-
els for SQL generation: Llama-3.2-1B, Llama-3.2-3B (base models) and Llama-2-7B-chat, Gemma-2-2B-it
(instruct-tuned models). We observe that despite explicitly prompting to only generate the SQL query, the
instruct-tuned Gemma-2-2B-it model often enclosed generated SQL queries within markers, such as ```
or ```sql . Thus, we consider another baseline for Gemma-2-2B where we extract the SQL query sub-
string within these markers, handling cases where the output format is either ```{SQL query} ``` or
```sql {SQL query} ``` .

For evaluation, we use the Spider (Yu et al., 2018) text-to-SQL dataset, which consists of 1,034 problems
of varying difficulty levels: easy (250), medium (440), hard (174), and extra hard (170). We prompt models
with schema information and text queries, instructing them to generate SQL queries only. Using greedy
decoding and \n\n is used as an additional stopping condition for all experiments.

              Table 2: Comparison of SynCode and unconstrained generation on SQL generation.

                                                   Accuracy (%)
      Model             Method                                                       Execute (%)   Tokens   Time (s)
                                    Easy   Medium     Hard         Extra   Overall
                        Standard     0.0    0.0         0.0         0.0      0.0         0.0       221.43    9.883
      Gemma2-2B-it      Standard+   44.8    18.9       21.9        17.1     25.4        77.6       221.43    9.893
                        SynCode     45.8    18.7       23.3        20.6     26.3        78.2       135.17    5.876
                        Standard    34.4    22.0       12.1         4.1     20.4        32.6        44.74    1.148
      Llama-2-7b-chat   SynCode     40.0    27.3       13.8         5.9     24.6        41.6        50.33    1.483
                        Standard    40.8    24.8       20.7        10.6     25.6        51.1        48.00    0.509
      Llama-3.2-1B      SynCode     46.8    28.2       23.0        10.6     28.8        59.0        56.36    0.916
                        Standard    38.0    29.5       28.2        12.9     28.6        67.4        47.78    0.846
      Llama-3.2-3B      SynCode     47.2    34.8       32.8        19.4     34.9        81.4        47.63    1.164



Table 2 presents a comparison of SynCode and unconstrained generation across key metrics. The Accuracy
(%) column shows the percentage of correctly generated SQL queries across different difficulty levels. Execute
(%) reflects the percentage of queries successfully executed without runtime errors in SQLite. The Tokens
column reports the average number of tokens generated, and Time(s) shows the average generation time.
Standard+ row for Gemma2 denotes the result for the additional baseline where we extract the SQL query
from the full generation using regex matching.


                                                              19
We observe that SynCode achieves better performance over the baselines in terms of both execution percent-
age and execution accuracy. For example, with the Llama-3.2-3B model, SynCode achieves an execution
success rate of 81.4%, compared to 67.4% for unconstrained generation. Further, the execution accuracy
improves from 28.6% to 34.9%. In the case of the Gemma2-2B-it model, we observe that SynCode shows
a moderate improvement over the Standard+ accuracy. However, it shows a significant gain in the speed
(1.7x) of generation and a reduction in the number of tokens generated. Although the Gemma2-2B-it model
has a good execution percentage without any runtime errors. The instruct-tuned models tends to use large
number of tokens that are not part of the query. In applications where the goal is to use LLMs to generate
SQL queries without additional explanations, the result with Gemma2-2B-it shows that SynCode is useful
in improving the efficiency of LLM generation along with the improvements in accuracy.

6.3   Effectiveness of SynCode for GPL

Table 3: Number of programs with syntax errors for standard and SynCode generation (↓ shows how much
SynCode reduces the occurrence of the syntax errors compared to Standard generation.

              Dataset     Model                       Python                      Go
                                           Standard    SynCode     ↓   Standard   SynCode     ↓
                          CodeGen-350M         271          15   95%       573         49   91%
              HumanEval   WizardCoder-1B        36           3   92%      1031         50   95%
                          LLaMA-7B             291           2   99%       725         10   99%
                          CodeGen-350M          78           4   95%       212          2   99%
              MBXP        WizardCoder-1B        28           2   93%       243         14   94%
                          LLaMA-7B             148           5   97%       414          1   99%



We run inference with CodeGen-350M, WizardCoder-1B, and LLaMA-7B with SynCode and with the
standard no-masking approch. We do not compare SynCode with the other baselines as none of these
works support general-purpose programming language grammars. We experiment with both Python and Go
programming languages, evaluating performance on zero-shot problems from the HumanEval and MBXP
datasets. For each dataset, we generate n = 20 and n = 1 samples per problem with the LLM, respectively.
We run the LLM-generated code completion against a predefined set of unit tests. For each unit test, we
record the error type when running the generated program against that test case. We use the hyperparameters
temperature = 0.2 and top p = 0.95. Table 3 presents our results for Python and Go. The columns standard
and SynCode represent the total number of generated programs with syntax errors for the respective
approaches. The column ↓ designates the percentage reduction in syntax errors from the standard generation
to the SynCode generation. In this evaluation, across both HumanEval and MBXP datasets, we generate a
total of 4154 samples for each language. On average, of all standard generated samples, 6% and 25% have
syntax errors for Python and Go, respectively.
Notably, our experiments reveal that SynCode reduces the number of syntax errors by over 90% over the
baseline in most experiments. Moreover, SynCode reduces the number of syntax errors to less than 1% of
the total samples. Interestingly, we observe significantly more Syntax errors in standard LLM-generated Go
code than in Python code, likely because the LLMs are trained more extensively on Python code than Go.
Thus, SynCode can be especially effective for Go and more underrepresented programming languages, where
LLMs are more likely to generate syntax errors due to a limited understanding of the language. SynCode
can bridge this gap by guiding the LLM to sample only the syntactically valid tokens during decoding.
We further analyze the errors in Python and Go code generated by the LLMs augmented with SynCode, an
example of which is presented in Appendix A.6. All of the errors were because the LLM failed to generate a
complete program within the maximum token limit. Recall, SynCode provides guarantees of completeness
for syntactically correct partial programs. However, it does not guarantee convergence to a syntactically
correct and complete program.
Functional Correctness for Code Generation. We investigate whether augmenting LLMs with Syn-
Code improves the functional correctness of the generated code. We evaluate functional correctness using
the pass@k metric, where k samples are generated per problem, and a problem is considered solved if any
sample passes a set of unit tests, and the fraction of solved problems is calculated. Table 4 reports our


                                                      20
                          Table 4: Functional correctness on HumanEval problems

                      Metric      Architecture                 Python                    Go
                                                         Standard   SynCode   Standard        SynCode
                                  CodeGen-350M              6.8%      6.9%       3.6%            3.6%
                      pass@1      WizardCoder-1B           20.0%      20.0%      9.3%           9.5%
                                  LLaMA-7B                 11.2%     11.5%       3.8%          4.25%
                                  CodeGen-350M             10.6%      10.6%      5.6%           6.1%
                      pass@10     WizardCoder-1B           27.6%     28.4%      12.5%          13.7%
                                  LLaMA-7B                 17.1%     18.9%       8.8%            8.8%



                               Table 5: DFA Mask store creation time and memory

                                                               Python                Go
                          Model                   |V |    Time(s)  Memory     Time(s)   Memory
                          CodeGen-350M           51200     602.26   1.87GB     603.03     1.58GB
                          WizardCoder-1B         49153     588.28   1.83GB     588.84     1.54GB
                          LLaMA-7B               32000     382.26   1.17GB     380.49     1.06GB




results for pass@1 and pass@10 for generated code completions to problems from the HumanEval dataset.
We observe that augmenting LLMs with SynCode has a slight improvement in functional correctness over
standard generation. This observation indicates that for these state-of-the-art models, syntactic correction
can result in a small improvement in the logical correctness of the code.

6.4   Mask Store Overhead

We analyze the time and memory overhead involved in generating a DFA mask store using SynCode.
The DFA mask store for Llama-2-7B-chat took 113.72 seconds to create and consumes 181 MB of memory.
Additionally, we report the creation time and memory overhead of DFA mask stores for models used for
Python and Go in Table 5. Each row shows the SynCode store generation time in seconds, and memory
in GBs, for a particular LLM and grammar. The |V | column represents the total vocabulary size of the
tokenizer of the particular LLM. We see that generating the store requires less than 2GB of memory and
several minutes across the evaluated models and grammars. This overhead is minimal for practical SynCode
use cases, as the mask store is a one-time generation task. Thereafter, the mask store can be efficiently loaded
into memory and used for repeated inference. We see smaller generation time and memory with Llama-2-7B-
chat and JSON grammar as opposed to LLaMA-7B, WizardCoder-1B, and CodeGen-350M with Python and
Go grammars since the size of the mask store is proportional to the number of terminals in the grammar.


7     Related Work

Our work focuses on enhancing the syntactical accuracy LLMs by using a constrained decoding algorithm.
Prior research has explored two other primary directions to enhance LLMs’ accuracy in generating formal
language: 1) Fine-tuning or prompt engineering (Bassamzadeh and Methani, 2024; Weyssow et al., 2024),
which demands substantial data, compute resources, and time, often without any formal guarantees. 2)
Modifications to the LLM’s architecture or tokenization (Murty et al., 2023; Dong et al., 2023; Zhu et al.,
2024), although these techniques have not yet achieved performance comparable to the current state-of-
the-art standard LLMs. However, both fine-tuning and architectural changes are complementary to the
grammar-guided decoding approach that we focus on in our work, and any gains through those techniques
will improve the overall quality of LLM generation.
There are several recent works on constrained LLM generation (Wei et al., 2023; Beurer-Kellner et al., 2023;
Lundberg et al., 2023; Willard and Louf, 2023; Scholak et al., 2021; Poesia et al., 2022; Gerganov and et. al.,
2024; Geng et al., 2023; Beurer-Kellner et al., 2024; Agrawal et al., 2023; Melcer et al., 2024). This includes
recent works that have used language-server (tools built for communication between IDEs and programming
language-specific tools like static analyzers and compilers) suggestions to enforce language-specific semantic


                                                              21
                         Table 6: Overview of various constrained decoding methods

                                               Regex    CFG     Precomputed     GPL     Max CFG      Input format
      lmql (Beurer-Kellner et al., 2023)         ✓        ✗           ✗           ✗       50-100     LMQL DSL
      guidance (Lundberg et al., 2023)           ✓        ✓           ✗           ✗       50-100     Python DSL
      Outlines (Willard and Louf, 2023)          ✓        ✓           ✓           ✗       50-100     Lark EBNF
      Picard (Scholak et al., 2021)              ✓        ✓           ✗           ✗       50-100       Haskell
      Synchromesh (Poesia et al., 2022)          ✓        ✓           ✗           ✗          ‡         ANTLR
      llama.cpp (Gerganov and et. al., 2024)     ✓        ✓           ✗           ✗       50-100     GBNF DSL
      gcd (Geng et al., 2023)                    ✓        ✓           ✗           ✗       50-100         GF
      Domino (Beurer-Kellner et al., 2024)       ✓        ✓           ✓           ✗       50-100     GBNF DSL
      SynCode (ours)                             ✓        ✓           ✓           ✓       500+       Lark EBNF
         † Implementation issues ‡ Synchromesh is closed-source and the information about DSL grammars is unavail-
         able
         GF: Grammatical Framework, GBNF is a DSL defined by LLAMA.CPP



constraints during decoding (Agrawal et al., 2023; Wei et al., 2023). These techniques do not guarantee
syntactical accuracy and rely on the availability and efficiency of language servers.
Structured LLM Generation. We focus our further discussion on comparison to the techniques that
constrain LLM for structured generation according to a formal language. We compare SynCode with prior
works in terms of precision and efficiency of the algorithms and generality and scalability of frameworks.
Table 6 presents the various recent techniques for structured LLM generation. The columns "Regex" and
"CFG" indicate regular expression and CFG constraining features, respectively. The "Precomputed" column
denotes techniques that precompute certain structures to enhance generation efficiency. The "GPL" column
specifies if the tools support general-purpose PLs. "Max CFG" displays the number of production rules
in the largest supported Grammar by these techniques. We obtained these numbers by examining the
built-in grammars that were provided in the corresponding libraries. Finally, the "Input Format" column
indicates the format used to specify generation constraints. In addition to the improvement over the baselines
presented in the evaluation, our work focuses on rigorously formalizing the correctness of our CFG-guided
generation approach.
Recent works such as guidance (Lundberg et al., 2023) and lmql (Beurer-Kellner et al., 2023) mitigate the
unpredictability of LLM responses by using template or constraint-based controlled generation techniques.
These libraries feature a templating engine where prompts are expressed with holes for the generation to fill.
lmql (Beurer-Kellner et al., 2023) supports general regular expression constraints, but not CFG constraints.
guidance (Lundberg et al., 2023) supports CFG-guided generation. It uses Earley parsing (Earley, 1970)
for constrained decoding. Similar to other related works, it incurs high inference overhead as it checks the
syntactical validity of the entire model vocabulary at each step. It uses a trie similar to (Poesia et al., 2022;
Willard and Louf, 2023; Beurer-Kellner et al., 2024). As shown in our evaluation it incurs higher overhead
for JSON generation than SynCode. It iterates over the vocabulary in order of the next token probability
to efficiently compute the next token. However, this leads to a lack of generality and it cannot be directly
combined with an arbitrary decoding strategy.
Outlines (Willard and Louf, 2023) is a library originally focused on regular expression-guided generation
and recently extended to support grammar-guided generation. During LLM generation, Outlines employs
an incremental Lark-based LALR parser to determine the next acceptable terminals based on the grammar.
It constructs a larger regular expression by computing the union of regular expressions from all terminals,
which is then converted into a DFA during inference. It then iterates over all LLM tokens and collects the
set of tokens that lead to a valid path through this combined DFA. As shown in our evaluation, SynCode
performs better than Outlines on generating with JSON grammar and it currently lacks support for large
GPL grammars.
llama.cpp (Gerganov and et. al., 2024), has also recently introduced support for grammar-guided gener-
ation. This approach models a nondeterministic pushdown automaton with N stacks to maintain possible
parse states. llama.cpp defines a new grammar syntax and implements a simplified basic parser in C++.
While this implementation in C++ reduces some parsing overhead compared to heavier LR(1) parsers im-


                                                          22
plemented in Python on top of Lark for SynCode, it is algorithmically inefficient. This inefficiency again
is due to the requirement to iterate over the entire vocabulary and update stack states during inference.
Moreover, the non-standard grammar syntax and limited support for general grammar features restrict its
evaluation to simpler grammars such as JSON. We anticipate that llama.cpp and Outlines would perform
even slower on grammars with more rules, terminals, and complex regular expressions, such as those found in
Python and Go. As shown in our evaluation, SynCode is more efficient and results in fewer syntax errors.
Synchromesh (Poesia et al., 2022) is a proprietary a tool from Microsoft that supports CFG-guided syn-
tactic decoding of LLMs. Similar to Outlines, it creates a union of regular expressions of terminals during
LLM generation. Further, Synchromesh uses a non-incremental parser for parsing. Both of which lead to
lower time complexity. Synchromesh uses techniques like Target Similarity Tuning for semantic example
selection and Constrained Semantic Decoding to enforce user-defined semantic constraints and works on
DSLs. In contrast, our work, SynCode focuses exclusively on syntactic generation.
Picard (Scholak et al., 2021) uses a specific decoding strategy that maintains a beam of multiple candidate
outputs and promptly rejects the candidates that violate the syntax. It utilizes an incremental monadic
parser and was developed specifically to support SQL generation. Introducing a new grammar into Picard
necessitates considerable effort, as it lacks support for a grammar-defining language to provide grammar
rules.
Recent work Domino (Beurer-Kellner et al., 2024) does CFG-guided LLM generation. It avoids traversing
the whole vocabulary during inference by precomputing a prefix tree corresponding to each NFA state of the
terminals of the grammar. The purpose of creating this structure is similar to SynCode’s DFA mask store.
We believe that SynCode’s mask store is more efficient than Domino’s prefix tree since on modern machines
(especially with GPUs) the union of the boolean masks from mask store can be performed quite efficiently
in practice (Paszke et al., 2019b). Domino defines the minimally invasive property which is equivalent to
SynCode’s soundness property. One key difference between SynCode and Domino is that Domino applies
under-approximation, permitting only tokens that align with the lookahead of the parser, while SynCode
adopts a conservative over-approximation approach, allowing tokens as long as their prefixes match the
parser lookahead. Due to the under-approximation, they claim that it requires ∞ parser lookahead to get
this soundness, whereas SynCode ensures soundness for any lookahead. Further, the largest grammar that
Domino can support currently is highly simplified C grammar with 70 rules with roughly 25% overhead.
Domino’s code is not available yet to experimentally compare it with SynCode.
Fixed Schema Generation. Many recent works perform constrained LLM decoding to ensure that the
generated output follows a fixed schema of JSON or XML (Zheng et al., 2023; Beurer-Kellner et al., 2024;
Willard and Louf, 2023; Sengottuvelu and et. al., 2024). When employing a fixed schema, many intermediate
points in the generation process offer either a single syntactical choice (e.g., key in the JSON schema) or
present only a handful of distinct options. In cases where only one choice exists, the generation of the
next token through the LLM can be entirely skipped. Alternatively, when there are multiple but limited
choices, techniques like speculative decoding can be used to expedite the generation process (Chen et al.,
2023; Leviathan et al., 2023). SynCode does not focus on generation problems with fixed schema, it solely
focuses on CFG-guided generation. We made the same observation as in (Beurer-Kellner et al., 2024),
techniques such as speculation are not useful for CFGs where the schema is not fixed.

8   Conclusion

Existing methods for guiding LLMs to produce syntactically correct output have been notably slow and
restrictive. In this paper, we present SynCode, an efficient and general framework to enhance LLMs’ ability
to generate syntactical output for various formal languages. During decoding, SynCode incrementally parses
the partially generated output, computes the unparsed remainder and acceptable terminal sequences, and
then leverages the remainder, accept sequences, and pre-computed DFA mask store to compute a mask to
constrain the LLM’s vocabulary to only syntactically valid tokens. We evaluated SynCode on generating
syntactically correct JSON, SQL, Python, and Go code with different combinations of datasets, models, and
tasks. SynCode eliminates syntax errors in JSON completions and significantly improves JSON schema
validation over the baselines. Furthermore, SynCode reduces the number of syntax errors in generated


                                                    23
Python and Go code by 96.07% on average compared to standard generation. We believe that our approach
will pave the way for more efficient and higher-quality structured LLM generation in real-world applications.

References
Lakshya A Agrawal, Aditya Kanade, Navin Goyal, Shuvendu K. Lahiri, and Sriram K. Rajamani. 2023.
  Guiding Language Models of Code with Global Context using Monitors. arXiv:2306.10763 [cs.CL]
A. V. Aho and S. C. Johnson. 1974. LR Parsing. ACM Comput. Surv. 6, 2 (jun 1974), 99–124.            https:
  //doi.org/10.1145/356628.356629
Alfred V. Aho, Ravi Sethi, and Jeffrey D. Ullman. 1986. Compilers, Principles, Techniques, and Tools.
  Addison-Wesley.
ANTLR. -. ANother Tool for Language Recognition.
Ben Athiwaratkun, Sanjay Krishna Gouda, Zijian Wang, Xiaopeng Li, Yuchen Tian, Ming Tan, Wasi Uddin
  Ahmad, Shiqi Wang, Qing Sun, Mingyue Shang, Sujan Kumar Gonugondla, Hantian Ding, Varun Kumar,
  Nathan Fulton, Arash Farahani, Siddhartha Jain, Robert Giaquinto, Haifeng Qian, Murali Krishna Ra-
  manathan, Ramesh Nallapati, Baishakhi Ray, Parminder Bhatia, Sudipta Sengupta, Dan Roth, and Bing
  Xiang. 2023. Multi-lingual Evaluation of Code Generation Models. arXiv:2210.14868 [cs.LG]
Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk Michalewski, David Dohan, Ellen
  Jiang, Carrie Cai, Michael Terry, Quoc Le, and Charles Sutton. 2021. Program Synthesis with Large
  Language Models. arXiv:2108.07732 [cs.PL]
Nastaran Bassamzadeh and Chhaya Methani. 2024. A Comparative Study of DSL Code Generation: Fine-
  Tuning vs. Optimized Retrieval Augmentation. arXiv:2407.02742 [cs.SE] https://arxiv.org/abs/2407.
  02742
Luca Beurer-Kellner, Marc Fischer, and Martin Vechev. 2023. Prompting Is Programming: A Query Lan-
  guage for Large Language Models. Proc. ACM Program. Lang. 7, PLDI, Article 186 (jun 2023), 24 pages.
  https://doi.org/10.1145/3591300
Luca Beurer-Kellner, Marc Fischer, and Martin Vechev. 2024. Guiding LLMs The Right Way: Fast, Non-
  Invasive Constrained Generation. arXiv:2403.06988 [cs.LG]
Satwik Bhattamishra, Kabir Ahuja, and Navin Goyal. 2020. On the Ability and Limitations of Transformers
  to Recognize Formal Languages. In Proceedings of the 2020 Conference on Empirical Methods in Natural
  Language Processing (EMNLP), Bonnie Webber, Trevor Cohn, Yulan He, and Yang Liu (Eds.). Association
  for Computational Linguistics, Online, 7096–7116. https://doi.org/10.18653/v1/2020.emnlp-main.
  576
Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind
  Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss,
  Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens
  Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack
  Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. 2020.
  Language Models are Few-Shot Learners. arXiv:2005.14165 [cs.CL]
Charlie Chen, Sebastian Borgeaud, Geoffrey Irving, Jean-Baptiste Lespiau, Laurent Sifre, and John Jumper.
  2023. Accelerating Large Language Model Decoding with Speculative Sampling. ArXiv preprint (2023).
Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan,
 Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger,
 Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder,
 Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Fe-
 lipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-
 Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir


                                                     24
  Balaji, Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam,
  Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie
  Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech
  Zaremba. 2021. Evaluating Large Language Models Trained on Code. arXiv:2107.03374 [cs.LG]
Grégoire Delétang, Anian Ruoss, Jordi Grau-Moya, Tim Genewein, Li Kevin Wenliang, Elliot Catt, Chris
  Cundy, Marcus Hutter, Shane Legg, Joel Veness, and Pedro A. Ortega. 2023. Neural Networks and the
  Chomsky Hierarchy. arXiv:2207.02098 [cs.LG] https://arxiv.org/abs/2207.02098
Yihong Dong, Ge Li, and Zhi Jin. 2023. CODEP: Grammatical Seq2Seq Model for General-Purpose Code
  Generation (ISSTA 2023). Association for Computing Machinery, New York, NY, USA, 188–198. https:
  //doi.org/10.1145/3597926.3598048
Jay Earley. 1970. An efficient context-free parsing algorithm. Commun. ACM 13, 2 (feb 1970), 94–102.
  https://doi.org/10.1145/362007.362035
Javid Ebrahimi, Dhruv Gelda, and Wei Zhang. 2020. How Can Self-Attention Networks Recognize Dyck-n
  Languages?. In Findings of the Association for Computational Linguistics: EMNLP 2020, Trevor Cohn,
  Yulan He, and Yang Liu (Eds.). Association for Computational Linguistics, Online, 4301–4306. https:
  //doi.org/10.18653/v1/2020.findings-emnlp.384
Saibo Geng, Martin Josifoski, Maxime Peyrard, and Robert West. 2023. Grammar-constrained decoding for
  structured NLP tasks without finetuning. In Proc. of EMNLP.
Georgi Gerganov and et. al. 2024. llama.cpp: Port of Facebook’s LLaMA model in C/C++.           https:
 //github.com/guidance-ai/guidance
Michael Hahn. 2020. Theoretical Limitations of Self-Attention in Neural Sequence Models. Transactions
 of the Association for Computational Linguistics 8 (Dec. 2020), 156–171. https://doi.org/10.1162/
 tacl_a_00306
Lark. -. Lark - a parsing toolkit for Python.
Yaniv Leviathan, Matan Kalman, and Yossi Matias. 2023. Fast Inference from Transformers via Speculative
  Decoding. arXiv:2211.17192 [cs.LG] https://arxiv.org/abs/2211.17192
Percy Liang, Rishi Bommasani, Tony Lee, Dimitris Tsipras, Dilara Soylu, Michihiro Yasunaga, Yian Zhang,
  Deepak Narayanan, Yuhuai Wu, Ananya Kumar, Benjamin Newman, Binhang Yuan, Bobby Yan, Ce
  Zhang, Christian Cosgrove, Christopher D. Manning, Christopher Ré, Diana Acosta-Navas, Drew A. Hud-
  son, Eric Zelikman, Esin Durmus, Faisal Ladhak, Frieda Rong, Hongyu Ren, Huaxiu Yao, Jue Wang,
  Keshav Santhanam, Laurel Orr, Lucia Zheng, Mert Yuksekgonul, Mirac Suzgun, Nathan Kim, Neel
  Guha, Niladri Chatterji, Omar Khattab, Peter Henderson, Qian Huang, Ryan Chi, Sang Michael Xie,
  Shibani Santurkar, Surya Ganguli, Tatsunori Hashimoto, Thomas Icard, Tianyi Zhang, Vishrav Chaud-
  hary, William Wang, Xuechen Li, Yifan Mai, Yuhui Zhang, and Yuta Koreeda. 2023. Holistic Evaluation
  of Language Models. arXiv:2211.09110 [cs.CL]
Scott Lundberg, Marco Tulio ArXiv preprinteia Ribeiro, and et. al. 2023. Guidance-Ai/Guidance: A Guid-
  ance Language for Controlling Large Language Models. https://github.com/guidance-ai/guidance
Ziyang Luo, Can Xu, Pu Zhao, Qingfeng Sun, Xiubo Geng, Wenxiang Hu, Chongyang Tao, Jing Ma, Qingwei
  Lin, and Daxin Jiang. 2023. WizardCoder: Empowering Code Large Language Models with Evol-Instruct.
  arXiv:2306.08568 [cs.CL]
Daniel Melcer, Nathan Fulton, Sanjay Krishna Gouda, and Haifeng Qian. 2024. Constrained Decoding for
 Fill-in-the-Middle Code Language Models via Efficient Left and Right Quotienting of Context-Sensitive
 Grammars. arXiv:2402.17988 [cs.PL] https://arxiv.org/abs/2402.17988
Grégoire Mialon, Roberto Dessì, Maria Lomeli, Christoforos Nalmpantis, Ram Pasunuru, Roberta Raileanu,
  Baptiste Rozière, Timo Schick, Jane Dwivedi-Yu, Asli Celikyilmaz, Edouard Grave, Yann LeCun, and
  Thomas Scialom. 2023. Augmented Language Models: a Survey. arXiv:2302.07842 [cs.CL]


                                                  25
Shikhar Murty, Pratyusha Sharma, Jacob Andreas, and Christopher D Manning. 2023. Pushdown Layers:
  Encoding Recursive Structure in Transformer Language Models. In The 2023 Conference on Empirical
  Methods in Natural Language Processing. https://openreview.net/forum?id=nRB8VpeM7b
Erik Nijkamp, Bo Pang, Hiroaki Hayashi, Lifu Tu, Huan Wang, Yingbo Zhou, Silvio Savarese, and Caiming
  Xiong. 2023. CodeGen: An Open Large Language Model for Code with Multi-Turn Program Synthesis.
  arXiv:2203.13474 [cs.LG]
NousResearch. 2024.        json-mode-eval.         https://huggingface.co/datasets/NousResearch/
  json-mode-eval
Theo Olausson, Alex Gu, Ben Lipkin, Cedegao Zhang, Armando Solar-Lezama, Joshua Tenenbaum, and
  Roger Levy. 2023. LINC: A Neurosymbolic Approach for Logical Reasoning by Combining Language
  Models with First-Order Logic Provers. In Proceedings of the 2023 Conference on Empirical Methods in
  Natural Language Processing. Association for Computational Linguistics. https://doi.org/10.18653/
  v1/2023.emnlp-main.313
OpenAI. 2024. OpneAI Tools. https://platform.openai.com/docs/assistants/tools
Liangming Pan, Alon Albalak, Xinyi Wang, and William Yang Wang. 2023. Logic-LM: Empowering Large
  Language Models with Symbolic Solvers for Faithful Logical Reasoning. arXiv:2305.12295 [cs.CL] https:
  //arxiv.org/abs/2305.12295
Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan,
  Trevor Killeen, Zeming Lin, Natalia Gimelshein, Luca Antiga, Alban Desmaison, Andreas
  Kopf, Edward Yang, Zachary DeVito, Martin Raison, Alykhan Tejani, Sasank Chilamkurthy,
  Benoit Steiner, Lu Fang, Junjie Bai, and Soumith Chintala. 2019a.    PyTorch: An Impera-
  tive Style, High-Performance Deep Learning Library.  In Advances in Neural Information Pro-
  cessing Systems 32. Curran Associates, Inc., 8024–8035.    http://papers.neurips.cc/paper/
  9015-pytorch-an-imperative-style-high-performance-deep-learning-library.pdf
Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor Killeen,
  Zeming Lin, Natalia Gimelshein, Luca Antiga, Alban Desmaison, Andreas Köpf, Edward Yang, Zach
  DeVito, Martin Raison, Alykhan Tejani, Sasank Chilamkurthy, Benoit Steiner, Lu Fang, Junjie Bai, and
  Soumith Chintala. 2019b. PyTorch: An Imperative Style, High-Performance Deep Learning Library.
  arXiv:1912.01703 [cs.LG]
Gabriel Poesia, Alex Polozov, Vu Le, Ashish Tiwari, Gustavo Soares, Christopher Meek, and Sumit Gul-
 wani. 2022. Synchromesh: Reliable Code Generation from Pre-trained Language Models. In International
 Conference on Learning Representations. https://openreview.net/forum?id=KmtVD97J43e
Mengye Ren, Eleni Triantafillou, Sachin Ravi, Jake Snell, Kevin Swersky, Joshua B. Tenenbaum, Hugo
 Larochelle, and Richard S. Zemel. 2018. Meta-Learning for Semi-Supervised Few-Shot Classification.
 arXiv:1803.00676 [cs.LG]
Torsten Scholak, Nathan Schucher, and Dzmitry Bahdanau. 2021. PICARD: Parsing Incrementally for
  Constrained Auto-Regressive Decoding from Language Models. In Proceedings of the 2021 Conference
  on Empirical Methods in Natural Language Processing, Marie-Francine Moens, Xuanjing Huang, Lucia
  Specia, and Scott Wen-tau Yih (Eds.). Association for Computational Linguistics, Online and Punta
  Cana, Dominican Republic, 9895–9901. https://doi.org/10.18653/v1/2021.emnlp-main.779
Rahul Sengottuvelu and et. al. 2024. jsonformer. https://github.com/1rgs/jsonformer
Gemma Team, Morgane Riviere, Shreya Pathak, Pier Giuseppe Sessa, Cassidy Hardin, Surya Bhupatiraju,
 Léonard Hussenot, Thomas Mesnard, Bobak Shahriari, Alexandre Ramé, Johan Ferret, Peter Liu, Pouya
 Tafti, Abe Friesen, Michelle Casbon, Sabela Ramos, Ravin Kumar, Charline Le Lan, Sammy Jerome, An-
 ton Tsitsulin, Nino Vieillard, Piotr Stanczyk, Sertan Girgin, Nikola Momchev, Matt Hoffman, Shantanu
 Thakoor, Jean-Bastien Grill, Behnam Neyshabur, Olivier Bachem, Alanna Walton, Aliaksei Severyn, Ali-
 cia Parrish, Aliya Ahmad, Allen Hutchison, Alvin Abdagic, Amanda Carl, Amy Shen, Andy Brock, Andy


                                                  26
  Coenen, Anthony Laforge, Antonia Paterson, Ben Bastian, Bilal Piot, Bo Wu, Brandon Royal, Charlie
  Chen, Chintu Kumar, Chris Perry, Chris Welty, Christopher A. Choquette-Choo, Danila Sinopalnikov,
  David Weinberger, Dimple Vijaykumar, Dominika Rogozińska, Dustin Herbison, Elisa Bandy, Emma
  Wang, Eric Noland, Erica Moreira, Evan Senter, Evgenii Eltyshev, Francesco Visin, Gabriel Rasskin, Gary
  Wei, Glenn Cameron, Gus Martins, Hadi Hashemi, Hanna Klimczak-Plucińska, Harleen Batra, Harsh
  Dhand, Ivan Nardini, Jacinda Mein, Jack Zhou, James Svensson, Jeff Stanway, Jetha Chan, Jin Peng
  Zhou, Joana Carrasqueira, Joana Iljazi, Jocelyn Becker, Joe Fernandez, Joost van Amersfoort, Josh Gor-
  don, Josh Lipschultz, Josh Newlan, Ju yeong Ji, Kareem Mohamed, Kartikeya Badola, Kat Black, Katie
  Millican, Keelin McDonell, Kelvin Nguyen, Kiranbir Sodhia, Kish Greene, Lars Lowe Sjoesund, Lauren
  Usui, Laurent Sifre, Lena Heuermann, Leticia Lago, Lilly McNealus, Livio Baldini Soares, Logan Kil-
  patrick, Lucas Dixon, Luciano Martins, Machel Reid, Manvinder Singh, Mark Iverson, Martin Görner,
  Mat Velloso, Mateo Wirth, Matt Davidow, Matt Miller, Matthew Rahtz, Matthew Watson, Meg Risdal,
  Mehran Kazemi, Michael Moynihan, Ming Zhang, Minsuk Kahng, Minwoo Park, Mofi Rahman, Mohit
  Khatwani, Natalie Dao, Nenshad Bardoliwalla, Nesh Devanathan, Neta Dumai, Nilay Chauhan, Oscar
  Wahltinez, Pankil Botarda, Parker Barnes, Paul Barham, Paul Michel, Pengchong Jin, Petko Georgiev,
  Phil Culliton, Pradeep Kuppala, Ramona Comanescu, Ramona Merhej, Reena Jana, Reza Ardeshir Rokni,
  Rishabh Agarwal, Ryan Mullins, Samaneh Saadat, Sara Mc Carthy, Sarah Cogan, Sarah Perrin, Sébastien
  M. R. Arnold, Sebastian Krause, Shengyang Dai, Shruti Garg, Shruti Sheth, Sue Ronstrom, Susan Chan,
  Timothy Jordan, Ting Yu, Tom Eccles, Tom Hennigan, Tomas Kocisky, Tulsee Doshi, Vihan Jain, Vikas
  Yadav, Vilobh Meshram, Vishal Dharmadhikari, Warren Barkley, Wei Wei, Wenming Ye, Woohyun Han,
  Woosuk Kwon, Xiang Xu, Zhe Shen, Zhitao Gong, Zichuan Wei, Victor Cotruta, Phoebe Kirk, Anand Rao,
  Minh Giang, Ludovic Peran, Tris Warkentin, Eli Collins, Joelle Barral, Zoubin Ghahramani, Raia Hadsell,
  D. Sculley, Jeanine Banks, Anca Dragan, Slav Petrov, Oriol Vinyals, Jeff Dean, Demis Hassabis, Koray
  Kavukcuoglu, Clement Farabet, Elena Buchatskaya, Sebastian Borgeaud, Noah Fiedel, Armand Joulin,
  Kathleen Kenealy, Robert Dadashi, and Alek Andreev. 2024. Gemma 2: Improving Open Language
  Models at a Practical Size. arXiv:2408.00118 [cs.CL] https://arxiv.org/abs/2408.00118

Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix,
 Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, Aurelien Rodriguez, Armand Joulin, Edouard
 Grave, and Guillaume Lample. 2023a. LLaMA: Open and Efficient Foundation Language Models.
 arXiv:2302.13971 [cs.CL]

Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bash-
 lykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, Dan Bikel, Lukas Blecher, Cristian Canton Fer-
 rer, Moya Chen, Guillem Cucurull, David Esiobu, Jude Fernandes, Jeremy Fu, Wenyin Fu, Brian Fuller,
 Cynthia Gao, Vedanuj Goswami, Naman Goyal, Anthony Hartshorn, Saghar Hosseini, Rui Hou, Hakan
 Inan, Marcin Kardas, Viktor Kerkez, Madian Khabsa, Isabel Kloumann, Artem Korenev, Punit Singh
 Koura, Marie-Anne Lachaux, Thibaut Lavril, Jenya Lee, Diana Liskovich, Yinghai Lu, Yuning Mao,
 Xavier Martinet, Todor Mihaylov, Pushkar Mishra, Igor Molybog, Yixin Nie, Andrew Poulton, Jeremy
 Reizenstein, Rashi Rungta, Kalyan Saladi, Alan Schelten, Ruan Silva, Eric Michael Smith, Ranjan Subra-
 manian, Xiaoqing Ellen Tan, Binh Tang, Ross Taylor, Adina Williams, Jian Xiang Kuan, Puxin Xu, Zheng
 Yan, Iliyan Zarov, Yuchen Zhang, Angela Fan, Melanie Kambadur, Sharan Narang, Aurelien Rodriguez,
 Robert Stojnic, Sergey Edunov, and Thomas Scialom. 2023b. Llama 2: Open Foundation and Fine-Tuned
 Chat Models. arXiv:2307.09288 [cs.CL] https://arxiv.org/abs/2307.09288

Yuxiang Wei, Chunqiu Steven Xia, and Lingming Zhang. 2023. Copiloting the Copilots: Fusing Large
  Language Models with Completion Engines for Automated Program Repair. In Proceedings of the 31st
  ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software
  Engineering (ESEC/FSE ’23). ACM. https://doi.org/10.1145/3611643.3616271

Martin Weyssow, Xin Zhou, Kisub Kim, David Lo, and Houari Sahraoui. 2024. Exploring Parameter-Efficient
 Fine-Tuning Techniques for Code Generation with Large Language Models. arXiv:2308.10462 [cs.SE]
 https://arxiv.org/abs/2308.10462

Brandon T. Willard and Rémi Louf. 2023.       Efficient Guided Generation for Large Language Models.
  arXiv:2307.09702 [cs.CL]


                                                   27
Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue, Anthony Moi, Pier-
  ric Cistac, Tim Rault, Remi Louf, Morgan Funtowicz, Joe Davison, Sam Shleifer, Patrick von Platen,
  Clara Ma, Yacine Jernite, Julien Plu, Canwen Xu, Teven Le Scao, Sylvain Gugger, Mariama Drame,
  Quentin Lhoest, and Alexander Rush. 2020. Transformers: State-of-the-Art Natural Language Process-
  ing. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing: System
  Demonstrations, Qun Liu and David Schlangen (Eds.). Association for Computational Linguistics, Online,
  38–45. https://doi.org/10.18653/v1/2020.emnlp-demos.6

wolfram. 2024.       Wolfram Alpha.          https://writings.stephenwolfram.com/2023/01/
  wolframalpha-as-the-way-to-bring-computational-knowledge-superpowers-to-chatgpt/
Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li, Markus Norman Rabe, Charles E Staats, Mateja Jamnik,
  and Christian Szegedy. 2022. Autoformalization with Large Language Models. In Advances in Neural
  Information Processing Systems, Alice H. Oh, Alekh Agarwal, Danielle Belgrave, and Kyunghyun Cho
  (Eds.). https://openreview.net/forum?id=IUikebJ1Bf0
Andy Yang, David Chiang, and Dana Angluin. 2024. Masked Hard-Attention Transformers Recognize
 Exactly the Star-Free Languages. arXiv:2310.13897 [cs.FL] https://arxiv.org/abs/2310.13897
Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad Godil, Ryan
 Prenger, and Anima Anandkumar. 2023. LeanDojo: Theorem Proving with Retrieval-Augmented Lan-
 guage Models. arXiv:2306.15626 [cs.LG] https://arxiv.org/abs/2306.15626
Tao Yu, Rui Zhang, Kai Yang, Michihiro Yasunaga, Dongxu Wang, Zifan Li, James Ma, Irene Li, Qingning
  Yao, Shanelle Roman, Zilin Zhang, and Dragomir Radev. 2018. Spider: A Large-Scale Human-Labeled
  Dataset for Complex and Cross-Domain Semantic Parsing and Text-to-SQL Task. In Proceedings of the
  2018 Conference on Empirical Methods in Natural Language Processing, Ellen Riloff, David Chiang, Julia
  Hockenmaier, and Jun’ichi Tsujii (Eds.). Association for Computational Linguistics, Brussels, Belgium,
  3911–3921. https://doi.org/10.18653/v1/D18-1425
Matei Zaharia, Omar Khattab, Lingjiao Chen, Jared Quincy Davis, Heather Miller, Chris Potts, James
 Zou, Michael Carbin, Jonathan Frankle, Naveen Rao, and Ali Ghodsi. 2024. The Shift from Models to
 Compound AI Systems. https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/.
Lianmin Zheng, Liangsheng Yin, Zhiqiang Xie, Jeff Huang, Chuyue Sun, Cody Hao Yu, Shiyi Cao, Christos
  Kozyrakis, Ion Stoica, Joseph E. Gonzalez, Clark Barrett, and Ying Sheng. 2023. Efficiently Programming
  Large Language Models using SGLang. arXiv:2312.07104 [cs.AI]
Qihao Zhu, Qingyuan Liang, Zeyu Sun, Yingfei Xiong, Lu Zhang, and Shengyu Cheng. 2024. Gram-
  marT5: Grammar-Integrated Pretrained Encoder-Decoder Neural Model for Code. In Proceedings of the
  IEEE/ACM 46th International Conference on Software Engineering (Lisbon, Portugal) (ICSE ’24). As-
  sociation for Computing Machinery, New York, NY, USA, Article 76, 13 pages. https://doi.org/10.
  1145/3597503.3639125




                                                   28
A     Appendix

A.1   List of Symbols

 G         Formal Grammar
 L(G)      Language of a grammar
 Lp (G)    Prefix language of a grammar
 l         lexical tokens
 li        i-th lexical token in the parsed output
 τ         A terminal in the grammar
 τi        Terminal type of i-th lexical token
 Γ         Set of all terminals in the grammar
 LΓ (G)    Language of terminals for grammar G
 LΓp (G)   Prefix language of terminals
 P         Parser
 Λ         Sequence of terminals
 T         Tokenizer in an LLM
 V         Vocabulary of an LLM
 Vk        Subset of vocabulary containing acceptable tokens at k-th LLM generation iteration
 ρτ        Regular expression for a terminal τ
 ρi        Regular expression corresponding to i-th lexical token
 ≼         Partial order over set of terminal sequences
 r         Remainder from SynCode parsing the partial output
 Ck        Partial output at k-th iteration of LLM generation
 Ck□       Parsed prefix of partial output Ck at k-th iteration of LLM generation
 A         Set of accept sequences
 Mα        DFA lookup store function for terminal sequences of length α
 dmatch    Match with DFA walk as defined in Section 4
 pmatch    Partial match with regular expression
 pparse    Partial parsing function
 m         Boolean mask
 D         Deterministic finite automaton
 Q         States in a DFA
 Σ         Set of characters i.e. alphabet for DFA
 δ         Transition function in a DFA
 δ∗        Extended transition function in a DFA
 q0        Start state of a DFA
 F         Set of final states in DFA
 live      Live states of the DFA
 QΩ        Set containing all DFA states for DFAs of all terminals in the grammar
 A0        Set of terminals acceptable for current lexical token
 A1        Set of terminals acceptable as for next lexical token
 Lex       Lexer function
 len       Length of a sequence
 Tcur      Current set of tokens
 S         Map for storing parser state




                                                   29
A.2      Proofs for Theorems

Lemma 1. Given Λ = {τf +1 , τf +2 . . . τf +d }, Λp = {τf +2 . . . τf +d } and ρΛ = (ρf +1 , ρf +2 , . . . , ρf +d ),
dmatch(w, q0τ1 , Λp ) ⇐⇒ pmatch(w, ρΛ ).

                                                 τ
Proof.       (a) First we prove dmatch(w, q0f +1 , Λp ) =⇒ pmatch(w, ρΛ ) We prove this using induction on
          the length i of w.
          For i = 0, pmatch(w, ρΛ ) is trivially true.
                                                                        τ
          Now, we assume that for w of length i < k, dmatch(w, q0f +1 , Λp ) =⇒ pmatch(w, ρΛ ).
                                                          τf +1 p
          We consider w of length k and dmatch(w, q0 , Λ ).
          We consider 3 conditions from Definition 10.
                                                   τ                                      τ
          If condition 1 is true, δτ∗f +1 (w, q0f +1 ) ∈ live(Qτf +1 ). Let q1 = δ ∗ (w, q0f +1 ). By Definition 9,
          ∃w1 s.t. δτ∗f +1 (w1 , q1 ) ∈ Fτf +1 . Hence,
                                                     τ
                                        δ ∗ (w.w1 , q0f +1 ) ∈ Fτf +1 =⇒ w.w1 ∈ L(ρτf +1 )

          We assume that each terminal L(τi ) is non-empty. Hence,

                                             ∃w2 ∈ L(ρΛp ) =⇒ w.w1 .w2 ∈ L(ρΛ )

          Hence, by condition 2 from Definition 8, pmatch(w, ρΛ ).
                                                                                      τ
          If condition 2 is true, ∃w1 , w2 such that w1 .w2 = w, δτ∗f +1 (w1 , q0f +1 ) ∈ F and Λp = {}. Here,
          w1 ∈ L(ρτf +1 ). Since Λp = {}, ρΛ = ρ1 , and hence, w1 ∈ L(ρΛ ). Hence by condition 1 from
          Definition 8, pmatch(w, ρΛ ).
                                                                                  τ
          If condition 3 is true, ∃w1 , w2 such that w1 .w2 = w, δτ∗f +1 (w1 , q0f +1 ) ∈ Fτf +1 ,
                             τ
          and dmatch(w2 , q0f +2 , {τf +3 . . . τf +d }) = true.
                                                         τ
                                         δτ∗f +1 (w1 , q0f +1 ) ∈ Fτf +1 =⇒ w1 ∈ L(ρτf +1 )

          Since length of w2 < k, by our induction hypothesis, pmatch(w2 , ρΛp ) = true. By Definition 8, there
          are two possibilities. Suppose ∃w2 = w3 .w4 such that w3 ∈ L(ρΛp ).

                                          w1 .w3 ∈ L(ρΛ ) =⇒ pmatch(w, ρΛ ) = true
          Alternatively, if ∃w3 such that w2 .w3 ∈ L(ρΛp )

                                        w1 .w2 .w3 ∈ L(ρΛ ) =⇒ pmatch(w, ρΛ ) = true

          Hence, our induction proof is complete and pmatch(w, ρΛ ) = true
                                                                   τ
      (b) Next we prove pmatch(w, ρΛ ) =⇒ dmatch(w, q0f +1 , Λp ) We prove this using induction on the
          length i of w.
                                 τ
          For i = 0, dmatch(w, q0f +1 , Λp ) is trivially true.
                                                                                  τ
          Now, we assume that for w of length i < k, pmatch(w, ρΛ ) =⇒ dmatch(w, q0f +1 , Λp )
          Now we consider w of length k and pmatch(w, ρΛ ).
          By Definition 8, there are two possible conditions

          Case 1: ∃w1 ∈ Σ∗ , w2 ∈ Σ+ such that w = w1 .w2 and w1 ∈ L(ρΛ )
          Hence, ∃w3 , w4 such that w1 = w3 .w4 and w3 ∈ L(ρτf +1 ) and w4 ∈ L(ρΛp ). By induction hypothesis,

                               pmatch(w4 .w2 , ρΛp ) =⇒ dmatch(w4 w2 , {τf +2 , τf +3 . . . τf +d })

          Since w = w3 .w4 .w2 and
                                                                            τ
                                         w3 ∈ L(ρτf +1 ) =⇒ δτ∗f +1 (w3 , q0f +1 ) ∈ Fτf +1


                                                             30
                                                                   τ
         Hence, by condition 3 in Definition 10, dmatch(w, q0f +1 , Λp )
         Case 2: ∃w1 such that w.w1 ∈ L(ρΛ )
         Hence, ∃w2 , w3 s.t w.w1 = w2 .w3 and w2 ∈ L(ρτf +1 ) and w3 ∈ L(ρΛ )
         Now there are two possibilities, either w is prefix of w2 or w2 is prefix of w2
                                                            τ
         Supoose w is prefix of w2 , then δτ∗f +1 (w, q0f +1 ) ∈ live(Qτf +1 ) and hence by Definition 10,
                     τ
         dmatch(w, q0f +1 , Λp ) Alternatively, if w2 is prefix of w then ∃w4 s.t. w = w2 w4
         Hence, w4 .w1 = w3 ∈ L(ρτf +1 ) and thus pmatch(w4 , ρΛp )
                                                    τ
         By induction hypothesis dmatch(w4 , q0f +2 , {τf +3 , τ4 . . . τf +d })
                                       ∗          τf +1                              τ
         and since w = w2 .w4 and δτf +1 (w2 , q0 ) ∈ Fτf +1 . We get dmatch(w, q0f +1 , Λp )


Lemma 2. If q = δτ∗ (r, q0τ ) and no prefix of r is in L(τ ) i.e. ∄w1 ∈ Σ∗ , w2 ∈ Σ∗ such that w1 .w2 =
r and δτ∗ (w1 , q0τ ) ∈ Fτ then dmatch(t, q, Λ) ⇐⇒ dmatch(r.t, q0τ , Λ).

Proof.      (a) First, we prove dmatch(t, q, Λ) =⇒ dmatch(r.t, q0τ , Λ).
         From Definition 10, either of the 3 conditions hold true for dmatch(t, q, Λ).

         If condition 1 is true then

                         δτ∗1 (t, q) ∈ live(Qτ ) =⇒ δτ∗ (r.t, q0τ ) ∈ live(Qτ ) =⇒ dmatch(r.t, q0τ , Λ)

         If condition 2 is true, ∃w1 , w2 such that w1 .w2 = t, δτ∗ (w1 , q) ∈ F and Λ = {}. Therefore,

                                          δτ∗ (r.w1 , q) ∈ F =⇒ dmatch(r.t, q0τ , Λ)

         If condition 3 is true, ∃w1 , w2 such that w1 .w2 = t, δτ∗ (w1 , q) ∈ F
         and dmatch(w2 , q0τ1 , {τ2 . . . τd }) = true. Therefore,

                                          δτ∗ (r.w1 , q) ∈ F =⇒ dmatch(r.t, q0τ , Λ)

         Therefore, in all cases, dmatch(rt, q0τ , Λ) must hold.

    (b) Now, we prove dmatch(rt, q0τ , Λ) =⇒ dmatch(t, q, Λ).
         From Definition 10, either of the 3 conditions hold true for dmatch(r.t, q0τ , Λ).

         If condition 1 is true then

                           δτ∗1 (r.t, q0τ ) ∈ live(Qτ ) =⇒ δτ∗ (t, q) ∈ live(Qτ ) =⇒ dmatch(t, q, Λ)

         If condition 2 is true, ∃w1 , w2 such that w1 .w2 = r.t, δτ∗ (w1 , q0τ ) ∈ F and Λ = {}. Since no prefix of
         r is accepted by L(τ ), ∃w3 s.t. w3 w4 = t and

                                            δτ∗ (w3 , q) ∈ F =⇒ dmatch(t, q, Λ)

         If condition 3 is true, ∃w1 , w2 such that w1 .w2 = r.t, δτ∗ (w1 , q0τ ) ∈ F
         and dmatch(w2 , q0τ1 , {τ2 . . . τd }) = true. Since no prefix of r is accepted by L(τ ), ∃w3 s.t. w3 w4 = t
         and
                                                 δτ∗ (w3 , q) ∈ F =⇒ dmatch(t, q, Λ)

         Therefore, in all cases, dmatch(t, q, Λ) must hold.



                                                          31
Theorem 1. Let Ck ∈ Lp (G) be the partial output and any integer d ≥ 1, let Ad ⊆ Γd contain all possible
accept terminal sequences of length d and r ∈ Σ∗ denote the remainder. If m = GrammarMask(A, r) then
for any t ∈ V , if Ck .t ∈ Lp (G) then t ∈ set(m)

Proof. Let r, Λ□ = pparse(Ck ) where Λ□ = τ1 , τ2 . . . τf and let r1 , Λ1                       = pparse(Ck .t) where
Λ1 = τ1 , τ2 . . . τf . . . τf +g
Hence, we can split r.t such that for w ∈ Σ∗ , r.t = w.r1 and w ∈ L(τf +1 . . . τf +g )
There are two possible cases:
Case 1: g < d

                                                     w ∈ L(τf +1 . . . τf +g )

                                                 =⇒ w ∈ Lp (τf +1 . . . τf +g )
By our assumption on Ad there must exist Λ2 = τf +1 . . . τf +d s.t. τf +1 . . . τf +g is prefix of Λ2 . Hence,

                                                       =⇒ w ∈ Lp (Λ2 )

                                                     =⇒ pmatch(r.t, Λ2 )

Case 2: g ≥ d
Since we assume that Ad contains all possible accept sequence of length d, Λ2 = τf +1 . . . τf +d must be
contained in Ad
Hence, ∃w1 , w2 ∈ Σ∗ such that w = w1 .w2 and

                                                          w1 ∈ L(Λ2 )

                                                       =⇒ w ∈ Lp (Λ2 )

                                                     =⇒ pmatch(r.t, Λ2 )
In both cases, pmatch(r.t, Λ2 ). Using Lemma 1,
                                                                τ
                                           =⇒ dmatch(r.t, q0f +1 , {τf +2 . . . τf +d })
                                   τ
Using Lemma 2 if q = δτ∗f +1 (r, q0f +1 )
                                       τ
                      dmatch(r.t, q0f +1 , {τf +2 . . . τf +d }) =⇒ dmatch(t, q, {τf +2 . . . τf +d })

Here from Definition 12, if Md−1 (q, {τf +2 . . . τf +d }) = m2 then t ∈ set(m2 ).
Since m2 ⊆ m, we have our result t ∈ set(m).



Lemma 3. Given A1 and A2 are set of accept sequences such that A1 ≼ A2 and m1 = GrammarMask(A1 , r)
and m2 = GrammarMask(A2 , r) then set(m2 ) ⊆ set(m1 )

Proof. Since ∀Λ2 ∈ A2 ∃Λ1 ∈ A1 ∃Λ3 ∈ Γ∗ s.t. Λ2 = Λ1 .Λ3 , Hence

                                           pmatch(w, ρΛ2 ) =⇒ pmatch(w, ρΛ1 )

Hence, for the mask set(m2 ) ⊆ set(m1 )

Theorem 2. Let Ck ∈ Lp (G) be the partial output, let Ad ⊆ Γd contain all possible accept terminal
sequences of length d and r ∈ Σ∗ denote the remainder. Suppose for any t ∈ V, d > len(t) and m =
GrammarMask(Ad , r) such that t ∈ set(m) then Ck .t ∈ Lp (G)


                                                                32
For the simplicity of presenting the proof, we assume that d > 2.
Since t ∈ set(m) for some Λ1 = {τf +1 , τf +2 . . . τf +d } ∈ A
                                                                               τ
                   =⇒ dmatch(t, q, {τf +2 . . . τf +d }) =⇒ dmatch(r.t, q0f +1 , {τf +2 . . . τf +d })

                                      =⇒ pmatch(r.t, {ρτf +1 .ρτf +2 . . . ρτf +d })
By Definition 8, there are two possible cases:

     1. ∃w1 ∈ Σ∗ , w2 ∈ Σ+ such that r.t = w1 .w2 and w1 ∈ L(ρτf +1 .ρτf +2 . . . ρτf +d )
        We show that this case is not possible since our terminal sequence Λ1 is long enough that no prefix
        of r.t cannot be in L(ρτf +1 .ρτf +2 . . . ρτf +d )
        We can infer that len(w1 ) < len(r.t) =⇒ len(w1 ) < len(r) + len(t)
        Further, from the assumption d > len(t), we have

                                                     len(w1 ) < d + len(r)

         Firstly, note that r ̸∈ L(ρτf +1 .ρτf +2 ) by the definition of remainder r
         Note that we assume no terminal contains empty string i.e. ϵ ̸∈ L(ρτi )
         Hence, every string in L(ρτf +2 . . . ρτf +d ) should have length at least d − 1

         Clearly, r is prefix of w1 . Let w3 ∈ Σ∗ , r.w3 = w1 and hence len(w3 ) > d − 1
         Hence,
                                                len(r) + d − 1 < len(w1 )
                                           len(r) + d − 1 < len(w1 ) < d + len(r)
         This is not possible and hence such w1 cannot exist.
     2. ∃w1 ∈ Σ∗ such that r.t.w1 ∈ L(ρτf +1 .ρτf +2 . . . ρτf +d )
         By Definition 5, we have Λ□ , r = pparse(Ck ) s.t Ck = Ck□ .r, Λ□ = τ1 , τ2 . . . τf Ck□ ∈
         L(ρτ1 .ρτ2 . . . ρτf ).
         Let Λ1 = τf +1 , τf +2 . . . τf +d
         Since, Ck .t = Ck□ .r.t, Ck□ ∈ L(Λ□ ) and r.t.w1 ∈ L(Λ1 ), we have

                                                    Ck□ .r.t.w1 ∈ L(Λ□ .Λ1 )

                                                     Ck .t.w1 ∈ L(Λ□ .Λ1 )
         By Definition 7 of accept sequence, Λ□ .Λ1 ∈ LΓp (G), Hence

                                            Ck .t.w1 ∈ Lp (G) =⇒ Ck .t ∈ Lp (G)

Thus, our proof is complete and Ck .t ∈ Lp (G)




                                                           33
A.3   Incremental Parsing Algorithm

Our parsing algorithm achieves incrementality in
LLM generation by utilizing a map S to store the Algorithm 4 Incremental Parsing
parser state. This map associates a list of lexical Inputs: Ck : partial output, S: state map
tokens with the corresponding parser state after      1: function Parse(Ck )
parsing those tokens. Frequently, in subsequent       2:    l1 , l2 . . . lf ← Lex(Ck )
LLM generation iterations, the count of lexical       3:    γ, Sγ ← RestoreState(S, L)
tokens remains the same—either the next vocab-        4:    P ← Initialize(Sγ )
ulary token is appended to the final lexical to-      5:    parsed ← l1 .l2 . . . lγ−1
ken, or it increases. Although uncommon, there        6:    for li ∈ lγ , lγ+1 . . . lf do
are cases where the number of parsed lexical to-      7:          Next(P, li )
kens may decrease during iterations. For exam-        8:          if P.state = Error then
ple, in Python, an empty pair of double quotes,       9:                break
"", is recognized as a complete lexical token rep- 10:            parsed ← parsed + li
resenting an empty string. On the other hand, 11:                 A0 ← A1
""" serves as a prefix to a docstring, constituting 12:           A1 ← Follow(P )
an incomplete parser token. Consequently, the 13:                 Si ← P.state
addition of a single double quote " reduces the 14:               Store(S, parsed, Si )
overall count of lexical tokens in these iterations.
We observe that while the total count of lexer 15:          if Ck = parsed then
tokens at the end may undergo slight changes         16:          r = lf
during these iterations, the majority of prefixes    17:          A ← {τf , A1 [0]}, {τf , A1 [1]} . . . }
of the parsed lexical tokens remain consistent.      18:                  ∪{A0 [0]}, {A0 [1]} . . . }
Hence, we establish a mapping between lists of       19:    else
prefixes of lexical tokens and the corresponding 20:              r = Ck − parsed
parser state after parsing those tokens. Subse-      21:          A ← {A1 [0]}, {A1 [1]} . . .
quently, when parsing a new list of lexer tokens,    22:    return        A, r
we efficiently determine the maximum length prefix of the lexer token list that is already present in S. This
incremental approach significantly reduces the complexity of our parsing algorithm.
While it could be feasible to introduce incrementality in the lexing operation, our experiments revealed
that lexing consumes insignificant time in comparison to parsing. As a result, we opted to focus only on
performing parsing incrementally.
Our incremental parsing algorithm uses a standard non-incremental base parser P that maintains a parser
state and supports two functions Next and Follow. The Next function accepts the next lexer token and then
updates the parser state. The Follow function returns a list of acceptable terminals at the current parser
state. These functions are present in common parser generator tools (Lark, ; ANTLR, ).
The Algorithm 4 presents our incremental parsing algorithm. The algorithm utilizes a lexer to tokenize the
partial output. The function RestoreState is used to restore the state of the parser to the maximal matching
prefix of lexical tokens that exist in S. The main loop iterates through the tokens and maintains a parser
state map. For each token, it updates the parser state, stores the mapping in S, and retrieves the next set
of acceptable terminals. The process continues until the end of the partial output. The algorithm returns
accept sequences A and remainder r.


A.4   Ablation Studies

In this section, we perform an ablation study for incremental parsing and max new tokens.
Incremental Parsing. We compare the runtime efficiency of utilizing incremental parsing over re-running
parsing from scratch in SynCode. We run inference on CodeGen-350M with SynCode using incremental
parsing and parsing from scratch on Python prompts from the HumanEval dataset. We generate n = 1
samples and control the max new tokens in the code completion. Our results are presented in Figure 10b,
where the x-axis represents the max new tokens and the y-axis represents the average generation time, in


                                                     34
                                   Table 7: SynCode on few-shot prompting

                             Architecture      Error Type       Standard   SynCode     ↓
                             CodeGen-350M      Syntax              53         0      100%
                                               Indentation         15         3       80%
                             WizardCoder-1B    Syntax               40        2      95%
                                               Indentation         22         1       95%
                             Llama-7B          Syntax              110        0      100%
                                               Indentation         40         5       88%




seconds, with and without incremental parsing. As shown in the figure, the average generation time when
re-parsing from scratch increases significantly as the maximum length of code that the LLM can generate
increases. On the other hand, the average generation time increases slowly with incremental parsing. For
max new tokens = 300, SynCode with incremental parsing achieves 9x speedup over running parsing
from scratch. Our results collectively demonstrate that augmenting SynCode with incremental parsing
dramatically improves generation time, especially when generating longer completions.




                                                                (b) Average generation time with and without incremen-
(a) Average generation time for different max new tokens        tal parser
                            Figure 10: Ablation studies on CodeGen-350M model.


Max New Tokens. We conduct an ablation study into the relationship between the maximum length of code
that the LLMs can generate and generation times. We used Python prompts from the HumanEval dataset
and leveraged CodeGen-350M to generate the code completions, both with and without the augmentation
of the SynCode. As shown in Figure 10a, as we increase the max new tokens, we observe a corresponding
increase in generation time.


A.5   Few-Shot Prompting

Few-shot prompting (Ren et al., 2018) refers to the idea that language models do not need to be specifically
trained for a downstream task such as classification or question answering. Rather, it is sufficient to train
them on broad text-sequence prediction datasets and to provide context in the form of examples when
invoking them. We study the performance of utilizing SynCode on few-shot prompting code generation
tasks. We selected Python few-shot examples from the MBXP dataset and generated code completions with
CodeGen-350M, LLaMA-7B, and WizardCoder-1B with SynCode and the standard no-masking generation.
We present our results in Table 7. The columns standard and SynCode represent the total number of errors
of a particular Error Type of LLM-generated code completions to problems in a particular dataset when
utilizing that respective generation approach. The column ↓ represents the percentage reduction from the
standard column to the SynCode column. As shown in the table, SynCode exhibits effectiveness not only
in zero-shot but also in the context of few-shot prompting tasks. This signifies the versatility of SynCode
in enhancing code generation across different prompt engineering techniques.


                                                           35
                          Figure 11: Syntactically Incorrect SynCode Program


A.6   SynCode Syntax Errors

Figure 11 presents an example of when the SynCode augmented LLM fails to generate a complete program
within the maximum token limit for a problem from the HumanEval dataset. While the code is a syntac-
tically correct partial program, it is not a syntactically correct complete program. Recall, that SynCode
guarantees completeness for syntactically correct partial programs but does not guarantee termination with
a syntactically correct complete program.




                                                   36
     A.7     Prompts Used in the Evaluation
1     <s >[ INST ] << SYS > >
2     You are a helpful assistant that answers in JSON . Here ’ s the json schema you must adhere to :
3     < schema >
4     { ’ title ’: ’ Person ’ , ’ type ’: ’ object ’ , ’ properties ’: { ’ firstName ’: { ’ type ’: ’ string ’ , ’
             description ’: " The person ’ s first name ."} , ’ lastName ’: { ’ type ’: ’ string ’ , ’ description ’:
              " The person ’ s last name ."} , ’age ’: { ’ description ’: ’ Age in years which must be equal to
              or greater than zero . ’ , ’ type ’: ’ integer ’ , ’ minimum ’: 0}} , ’ required ’: [ ’ firstName ’ , ’
             lastName ’ , ’age ’]}
5     </ schema >
6
7     < </ SYS > >
8
9     Please generate a JSON output for a person ’ s profile that includes their first name , last
           name , and age . The first name should be ’ Alice ’ , the last name ’ Johnson ’ , and the age
           35. [/ INST ]

     Listing 1: Example original JSON Prompt from the JSON-Mode-Eval dataset (NousResearch, 2024). The
     prompt consists of a system message that specifies a schema and a user message requesting JSON output
     given certain parameters.

1     <s >[ INST ] << SYS > >
2     You are a helpful assistant that answers in JSON . Here ’ s the json schema you must adhere to :
3     < schema >
4     { ’ title ’: ’ Person ’ , ’ type ’: ’ object ’ , ’ properties ’: { ’ firstName ’: { ’ type ’: ’ string ’ , ’
             description ’: " The person ’ s first name ."} , ’ lastName ’: { ’ type ’: ’ string ’ , ’ description ’:
              " The person ’ s last name ."} , ’age ’: { ’ description ’: ’ Age in years which must be equal to
              or greater than zero . ’ , ’ type ’: ’ integer ’ , ’ minimum ’: 0}} , ’ required ’: [ ’ firstName ’ , ’
             lastName ’ , ’age ’]}
5     </ schema >
6
7     < </ SYS > >
8
9     Please generate a JSON output for a person ’ s profile that includes their first name , last
           name , and age . The first name should be ’ Alice ’ , the last name ’ Johnson ’ , and the age
           35. Output only JSON . [/ INST ]

     Listing 2: Example JSON prompt from the JSON-Mode-Eval dataset                              (NousResearch, 2024) after
     augmentation with an explicit request to only output JSON.

1
2     db_id : concert_s inger
3     db_info : # stadium ( stadium_id , location , name , capacity , highest , lowest , average )
4     # singer ( singer_id , name , country , song_name , s o n g _ r e l e a s e _ y e a r , age , is_male )
5     # concert ( concert_id , concert_name , theme , stadium_id , year )
6     # si nger _in _ c o n c e r t ( concert_id , singer_id )
7     # concert . stadium_id = stadium . stadium_id
8     # si nger _in _ c o n c e r t . singer_id = singer . singer_id
9     # si nger _in _ c o n c e r t . concert_id = concert . concert_id
10
11    question : How many singers do we have ? Only output the SQL query .
12    SQL :

                                                 Listing 3: text-2-SQL prompt.

1     def h as _ cl os e _ e l e m e n t s ( numbers : List [ float ] , threshold : float ) -> bool :
2                """ Check if in given list of numbers , are any two numbers closer to each other than
3                given threshold .
4                >>> h a s _ c l o s e _ e l e m e n t s ([1.0 , 2.0 , 3.0] , 0.5)
5                False
6                >>> h a s _ c l o s e _ e l e m e n t s ([1.0 , 2.8 , 3.0 , 4.0 , 5.0 , 2.0] , 0.3)
7                True
8                """

              Listing 4: Example Python prompt from the HumanEval dataset (Athiwaratkun et al., 2023)

1     package main
2
3     import (
4       " encoding / json "
5       " reflect "
6     )
7     // You ’ re an expert Golang programmer
8     // Check if in given list of numbers , are any two numbers closer to each other than



                                                                  37
9     // given threshold .
10    // >>> h as _c l o s e _ e l e m e n t s ([1.0 , 2.0 , 3.0] , 0.5)
11    // False
12    // >>> h as _c l o s e _ e l e m e n t s ([1.0 , 2.8 , 3.0 , 4.0 , 5.0 , 2.0] , 0.3)
13    // True
14    //
15    func h as _ cl o s e _ e l e m e n t s ( numbers [] float64 , threshold float64 ) bool {

                Listing 5: Example Go prompt from the HumanEval dataset (Athiwaratkun et al., 2023)


     A.8     Grammars Used in the Evaluation

     A.8.1     JSON Grammar

1     ? start : value
2
3     ? value : object
4     | array
5     | UNESCAPED_ S T R I N G
6     | SIGNED_NUMBER               ->   number
7     | " true "                    ->   true
8     | " false "                   ->   false
9     | " null "                    ->   null
10
11    array : "[" [ value (" ," value ) *] "]"
12    object : "{" [ pair (" ," pair ) *] "}"
13    pair   : UNE S C A P E D _ S T R I N G ":" value
14
15    UNESCAPED_ST RI N G : /\"[^"]*\"/
16
17    DIGIT : "0".."9"
18    HEXDIGIT : " a ".." f "|" A ".." F "| DIGIT
19    INT : DIGIT +
20    SIGNED_INT : ["+"|" -"] INT
21    DECIMAL : INT "." INT ? | "." INT
22
23
24    _EXP : (" e "|" E ") SIGNED_INT
25    FLOAT : INT _EXP | DECIMAL _EXP ?
26    NUMBER : FLOAT | INT
27    SIGNED_NUMBER : ["+"|" -"] NUMBER
28    WS : /[ \ t \ f \ r \ n ]/+
29
30    % ignore WS

                                                             Listing 6: JSON Grammar


     A.8.2     SQL Grammar

1
2     start : set_expr ";"? -> final
3
4     set_expr :    query_expr
5              |    set_expr " UNION " i [" DISTINCT " i ] set_expr -> u nion_dis tinct
6              |    set_expr " UNION " i " ALL " i set_expr -> union_all
7              |    set_expr " INTERSECT " i [" DISTINCT " i ] set_expr -> i n t e r s e c t _ d i s t i n c t
8              |    set_expr " EXCEPT " i [" DISTINCT " i ] set_expr -> e xc ep t _d is ti n ct
9              |    set_expr " EXCEPT " i " ALL " i set_expr -> except_all
10
11    query_expr : select [ " ORDER " i " BY " i ( order_by_expr " ,") *                order_by_expr ] [ " LIMIT " i
           limit_count [ " OFFSET " i skip_rows ] ]
12
13    select : " SELECT " i [ S E L E C T _ C O N S T R A I N T ] [( select_expr " ,") *] select_expr " FROM " i [( from_expr
           " ,") *] from_expr [ " WHERE " i where_expr ] [ " GROUP " i " BY " i [( groupby_expr " ,") *]
           groupby_expr ] [ " HAVING " i having_expr ] [ " WINDOW " i window_expr ]
14
15    where_expr : bo o l_ ex pr e ss io n
16
17    select_expr .0: ex pr es s io n_ ma t h [ " AS " i alias ] -> s e l e c t _ e x p r e s s i o n
18
19    ? from_expr : from_item -> fr om _e x pr es si o n
20
21    order_by_expr : order -> o r d e r _ b y _ e x p r e s s i o n
22




                                                                             38
23    having_expr : b oo l_ e xp re ss i on
24
25    groupby_expr : expression -> group_by
26
27    window_expr : [ window_expr " ,"] _window_name " AS " i ( w i n d o w _ d e f i n i t i o n )
28
29    from_item : table_name [ " AS " i alias ] -> table
30                 | join -> join
31                 | cross_join -> c r o s s _ j o i n _ e x p r e s s i o n
32                 | subquery
33    table_name : name
34
35    subquery : ( "(" ( query_expr | join | cross_join ) ") " ) [ " AS " i alias ]
36
37    cross_join : from_item " CROSS " i " JOIN " i from_item
38    join : from_item JOIN_EXPR from_item [ " ON " i bo ol _ ex pr es s io n ] -> j oi n_ ex p re ss io n
39
40    JOIN_EXPR .5: ( JOIN_TYPE WS ) ? " JOIN " i
41    JOIN_TYPE : " INNER " i | " OUTER " i ? | JOI N_DIRECT ION ( WS " OUTER " i ) ? | JOI N_DIRECT ION
42    JOIN_DIRECTI ON : " FULL " i | " LEFT " i | " RIGHT " i
43
44    ? expression_ m at h : e x p r e s s i o n _ p r o d u c t
45                       | e xp re s si on _m a th "+" e x p r e s s i o n _ p r o d u c t -> expres sion_add
46                       | e xp re s si on _m a th " -" e x p r e s s i o n _ p r o d u c t -> expres sion_sub
47                       | " CASE " i ( when_then ) + " ELSE " i e xp re s si on _m a th " END " i -> ca se _e x pr es si o n
48                       | " CAST " i "(" e xp r es si on _ ma th " AS " i TYPENAME ") " -> as_type
49                       | " CAST " i "(" literal " AS " i TYPENAME ") " -> literal_cast
50                       | AGGREGATION e xp re ss i on _m at h ") " [ window_form ] -> s ql _a gg r eg at io n
51                       | " RANK " i "(" ") " window_form -> r an k_ e xp re ss i on
52                       | " DENSE_RANK " i "(" ") " window_form -> d e n s e _ r a n k _ e x p r e s s i o n
53                       | " COALESCE " i "(" [( ex pr es s io n_ ma t h " ,") *] e xp re ss i on _m at h ") " ->
                                coalesce_expression
54                       | subquery -> s u b q u e r y _ e x p r e s s i o n
55
56    window_form : " OVER " i "(" [" PARTITION " i " BY " i ( partition_by " ,") * partition_by ] [" ORDER " i " BY
          " i ( order " ,") * order [ r o w _ r a n g e _ c l a u s e ] ] ") "
57
58    partition_by : ex p re ss io n _m at h
59
60    row_range_cl au s e : ( ROWS | RANGE ) frame_extent
61    frame_extent : frame_between | fr am e _p re ce d in g
62    frame_between : " BETWEEN " i frame_bound " AND " i frame_bound
63    frame_bound : f ra me _ pr ec ed i ng | fr am e_ f ol lo wi n g | " CURRENT " i " ROW " i
64    frame_preced in g : UNBOUNDED PRECEDING | INT_NUMBER PRECEDING
65    frame_follow in g : UNBOUNDED FOLLOWING | INT_NUMBER FOLLOWING
66    RANGE : " RANGE " i
67    ROWS : " ROWS " i
68    UNBOUNDED : " UNBOUNDED " i
69    PRECEDING : " PRECEDING " i
70    FOLLOWING : " FOLLOWING " i
71
72    when_then : " WHEN " i bo ol _e x pr es si o n " THEN " i e xp r es si on _ ma th
73    order : expre ss io n _m at h [" ASC " i ] -> order_asc
74               | e xp r es si on _ ma th " DESC " i -> order_desc
75
76
77    ? ex p re ss i on _ p r o d u c t : e x p r e s s i o n _ p a r e n s
78                                    | e x p r e s s i o n _ p r o d u c t "*" e x p r e s s i o n _ p a r e n s -> ex pression _mul
79                                    | e x p r e s s i o n _ p r o d u c t "/" e x p r e s s i o n _ p a r e n s -> ex pression _div
80
81    ? e xpr ess ion_ p a r e n s :   expression
82                                 |   "(" e x p r e s s i o n _ p a r e n s   "*"    expression   ") "   ->   expre ssion_mu l
83                                 |   "(" e x p r e s s i o n _ p a r e n s   "/"    expression   ") "   ->   expre ssion_di v
84                                 |   "(" e x p r e s s i o n _ p a r e n s   "+"    expression   ") "   ->   expre ssion_ad d
85                                 |   "(" e x p r e s s i o n _ p a r e n s   " -"   expression   ") "   ->   expre ssion_su b
86
87    column_name : [ name "."] ( name | STAR )
88    ? expression : column_name -> column_name
89                  | literal
90
91
92    SE LEC T_CO NST R A I N T .9: " ALL " i | " DISTINCT " i
93    TYPENAME : " object " i
94                | " varchar " i
95                | " integer " i
96                | " int16 " i
97                | " smallint " i
98                | " int32 " i
99                | " int64 " i
100               | " int " i
101               | " bigint " i



                                                                                          39
102                 | " float16 " i
103                 | " float32 " i
104                 | " float64 " i
105                 | " float " i
106                 | " bool " i
107                 | " datetime64 " i
108                 | " timestamp " i
109                 | " time " i
110                 | " date " i
111                 | " cateSQLry " i
112                 | " string " i
113   AGGREGATION .8: (" SUM (" i | " AVG (" i | " MIN (" i | " MAX (" i | " COUNT (" i " DISTINCT " i | " COUNT (" i )
114   alias : name -> alias_string
115   _window_name : name
116   limit_count : INT_NUMBER -> limit_count
117   skip_rows : INT_NUMBER
118   bool_express io n : b o o l _ p a r e n t h e s e s
119                                | b oo l_ e xp re ss i on " AND " i b o o l _ p a r e n t h es e s -> bool_and
120                                | b oo l_ e xp re ss i on " OR " i b o o l _ p a re n t h e s e s -> bool_or
121   bool_parenth es e s : co mp a ri so n_ t yp e
122                                | "(" b oo l _e xp re s si on " AND " i co mp a ri so n_ t yp e ") " -> bool_and
123                                | "(" b oo l _e xp re s si on " OR " i co mp ar i so n_ ty pe ") " -> bool_or
124                                | " EXISTS " i subquery -> exists
125   comparison_t yp e : equals | not_equals | greater_than | less_than | g r e a t e r _ t h a n _ o r _ e q u a l
126   | l es s _t h an _ o r _ e q u a l | between | in_expr | not_in_expr | subquery_in | su bq u er y_ no t _i n |
            is_null | is_not_null | like_expr | not_like_expr
127
128   equals : expr es s io n_ ma t h "=" e x pr es si o n_ ma th
129   is_null : exp re ss io n _m at h " IS " i " NULL " i
130   is_not_null : e xp re s si on _m a th " IS " i " NOT " i " NULL " i
131   not_equals : ex p re ss io n _m at h (" < >" | "!=") e x pr es si o n_ ma th
132   greater_than : ex p re ss io n _m at h " >" ex pr es s io n_ ma t h
133   less_than : ex pr es s io n_ ma t h " <" e x pr es si o n_ ma th
134   g r e a t e r _ t h a n _ o r _ e q u a l : e xp r es si on _ ma th " >=" e xp r es si on _ ma th
135   l es s _t ha n _o r _ e q u a l : ex pr es s io n_ ma th " <=" ex pr es s io n_ ma t h
136   between : exp re ss io n _m at h " BETWEEN " i e xp re s si on _m a th " AND " i ex pr es s io n_ ma t h
137
138   // ‘ LIKE ‘ and ‘ NOT LIKE ‘
139   like_expr : ex pr es s io n_ ma t h " LIKE " i e xp r es si on _ ma th
140   not_like_expr : e x pr es si o n_ ma th " NOT " i " LIKE " i ex p re ss io n _m at h
141
142   // ‘IN ‘ and ‘ NOT IN ‘
143   in_expr : exp re ss io n _m at h " IN " i "(" [ e x pr es si o n_ ma th " ,"]* ex pr es s io n_ ma t h ") "
144   subquery_in : e xp re s si on _m a th " IN " i subquery
145   not_in_expr : e xp re s si on _m a th " NOT " i " IN " i "(" [ ex pr es s io n_ ma t h " ,"]* ex p re ss io n_ m at h ") "
146   subquery_not _i n : ex p re ss io n _m at h " NOT " i " IN " i subquery
147
148   ? literal : boolean -> bool
149           | number_expr -> number
150           | / ’([^ ’]) + ’| ’ ’/ -> string
151           | t i m e s t a m p _ e x p r e s s i o n -> t i m e s t a m p _ e x p r e s s i o n
152   boolean : " TRUE " i -> true
153           | " FALSE " i -> false
154   ? number_expr : product
155
156   ? product : INT_NUMBER -> integer
157           | FLOAT -> float
158
159   INT_NUMBER : /[1 -9][0 -9]*/
160
161   STAR : "*"
162   wi ndo w_de fin i t i o n :
163   t i m e s t a m p _ e x p r e s s i o n : " NOW " i "(" ") " -> datetime_now
164                                           | " TODAY " i "(" ") " -> date_today
165
166   date : YEAR " -" MONTH " -" DAY
167   YEAR : /[0 -9]{4}/
168   MONTH : /[0 -9]{2}/
169   DAY : /[0 -9]{2}/
170   time : HOURS ":" MINUTES ":" SECONDS
171   HOURS : /[0 -9]{2}/
172   MINUTES : /[0 -9]{2}/
173   SECONDS : /[0 -9]{2}/
174   name : CNAME | ESCA PED_STRI NG
175
176   _STRING_INNER : / ( ?: [^ "\ \ ]| \\ .) *?/
177   ESCAPED_STRI NG : "\"" _STRING_INNER "\""
178
179   % import common . CNAME
180   % import common . WS
181   % import common . SQL_COMMENT



                                                                                             40
182    % import common . WS_INLINE
183    % import common . FLOAT
184
185    % ignore WS
186    % ignore SQL_COMMENT

                                                   Listing 7: SQL Grammar


      A.8.3   Python Grammar

 1     single_input : _NL | simple_stmt | compound_stmt _NL
 2     start : ( _NL | stmt ) *
 3     eval_input : testlist _NL *
 4
 5     ! decorator : " @ " dotted_name [ "(" [ arguments ] ") " ] _NL
 6     decorators : decorator +
 7     decorated : decorators ( classdef | funcdef | async_funcdef )
 8
 9     async_funcdef : " async " funcdef
10     funcdef : " def " NAME "(" parameters ? ") " [" - >" test ] ":" ( suite | _NL )
11
12     ! parameters : paramvalue (" ," paramvalue ) * [" ," [ starparams | kwparams ]]
13                | starparams
14                | kwparams
15     starparams : "*" typedparam ? (" ," paramvalue ) * [" ," kwparams ]
16     kwparams : "**" typedparam
17
18     ? paramvalue : typedparam ["=" test ]
19     ? typedparam : NAME [":" test ]
20
21     ! varargslist : ( vfpdef ["=" test ] (" ," vfpdef ["=" test ]) * [" ," [ "*" [ vfpdef ] (" ," vfpdef
             ["=" test ]) * [" ," ["**" vfpdef [" ,"]]] | "**" vfpdef [" ,"]]]
22        | "*" [ vfpdef ] (" ," vfpdef ["=" test ]) * [" ," ["**" vfpdef [" ,"]]]
23        | "**" vfpdef [" ,"])
24
25     vfpdef : NAME
26
27     ? stmt : ( simple_stmt | compound_stmt ) [" eof "]
28     !? simple_stmt : small_stmt (";" small_stmt ) * [";"] _NL
29     ? small_stmt : ( expr_stmt | del_stmt | pass_stmt | flow_stmt | import_stmt | global_stmt |
               nonlocal_stmt | assert_stmt )
30     ? expr_stmt : t e s t l i s t _ s t a r _ e x p r ( annassign | augassign ( yield_expr | testlist )
31                    | ("=" ( yield_expr | t e s t l i s t _ s t a r _ e x p r ) ) *)
32     annassign : ":" test ["=" test ]
33     !? t e st li s t_ s t a r _ e x p r : ( test | star_expr ) (" ," ( test | star_expr ) ) * [" ,"]
34     ! augassign : ("+=" | " -=" | "*=" | " @ =" | "/=" | "%=" | "&=" | "|=" | "^=" | " < <=" | " > >=" |
              "**=" | "//=")
35     // For normal and annotated assignments , additional restrictions enforced by the interpreter
36     del_stmt : " del " exprlist
37     pass_stmt : " pass "
38     flow_stmt : break_stmt | continue_stmt | return_stmt | raise_stmt | yield_stmt
39     break_stmt : " break "
40     continue_stmt : " continue "
41     return_stmt : " return " [ testlist ]
42     yield_stmt : yield_expr
43     raise_stmt : " raise " [ test [" from " test ]]
44     import_stmt : import_name | import_from
45     import_name : " import " d o tt ed _a s _n am es
46     // note below : the ("." | "...") is necessary because "..." is tokenized as ELLIPSIS
47     import_from : " from " ( dots ? dotted_name | dots ) " import " ("*" | "(" i mp o rt _a s_ n am es ") " |
               import_ a s_ na me s )
48     ! dots : "."+
49     import_as_na me : NAME [" as " NAME ]
50     dotted_as_na me : dotted_name [" as " NAME ]
51     ! import_as_n a me s : impo rt_as_na me (" ," impor t_as_nam e ) * [" ,"]
52     dotted_as_na me s : d otted_as _name (" ," do tted_as_ name ) *
53     dotted_name : NAME ("." NAME ) *
54     global_stmt : " global " NAME (" ," NAME ) *
55     nonlocal_stmt : " nonlocal " NAME (" ," NAME ) *
56     assert_stmt : " assert " test [" ," test ]
57
58     compound_stmt : if_stmt | while_stmt | for_stmt | try_stmt | with_stmt | funcdef | classdef |
             decorated | async_stmt
59     async_stmt : " async " ( funcdef | with_stmt | for_stmt )
60     if_stmt : " if " test ":" suite (" elif " test ":" suite ) * [" else " ":" suite ]
61     while_stmt : " while " test ":" suite [" else " ":" suite ]
62     for_stmt : " for " exprlist " in " testlist ":" suite [" else " ":" suite ]



                                                                41
63    try_stmt : (" try " ":" suite (( except_clause ":" suite ) + [" else " ":" suite ] [" finally " ":"
           suite ] | " finally " ":" suite ) )
64    with_stmt : " with " with_item (" ," with_item ) * ":" suite
65    with_item : test [" as " expr ]
66    // NB compile . c makes sure that the default except clause is last
67    except_clause : " except " [ test [" as " NAME ]]
68    suite : simple_stmt | _NL _INDENT stmt + _DEDENT
69
70    ? test : or_test [" if " or_test " else " test ] | lambdef
71    ? test_nocond : or_test | lambd ef_nocon d
72    lambdef : " lambda " [ varargslist ] ":" test
73    lambdef_noco nd : " lambda " [ varargslist ] ":" test_nocond
74    ? or_test : and_test (" or " and_test ) *
75    ? and_test : not_test (" and " not_test ) *
76
77    ? not_test : " not " not_test -> not
78               | comparison
79    ? comparison : expr ( _comp_op expr ) *
80    star_expr : "*" expr
81    ? expr : xor_expr ("|" xor_expr ) *
82    ? xor_expr : and_expr ("^" and_expr ) *
83    ? and_expr : shift_expr ("&" shift_expr ) *
84    ? shift_expr : arith_expr ( _shift_op arith_expr ) *
85    ? arith_expr : term ( _add_op term ) *
86    ? term : factor ( _mul_op factor ) *
87    ? factor : _factor_op factor | power
88
89    ! _factor_op : "+"|" -"|"~"
90    ! _add_op : "+"|" -"
91    ! _shift_op : " < <"|" > >"
92    ! _mul_op : "*"|" @ "|"/"|" %"|"//"
93    // <> isn ’ t actually a valid comparison operator in Python . It ’ s here for the
94    // sake of a __future__ import described in PEP 401 ( which really works : -)
95    ! _comp_op : " <"|" >"|"=="|" >="|" <="|" < >"|"!="|" in "|" not " " in "|" is "|" is " " not "
96
97    ? power : await_expr ["**" factor ]
98    ! await_expr : [" await "] atom_expr
99
100   ? atom_expr :   atom_expr "(" [ arguments ] ") "         -> funccall
101               |   atom_expr "[" subscriptlist "]"        -> getitem
102               |   atom_expr "." NAME                     -> getattr
103               |   atom
104
105   ? atom :   "(" [ yield_expr | testlist_comp ] ") " -> tuple
106          |   "[" [ testlist_comp ] "]" -> list
107          |   "{" [ dic torsetma ker ] "}" -> dict
108          |   NAME -> var
109          |   number | string +
110          |   "(" test ") "
111          |   "..." -> ellipsis
112          |   " None "    -> const_none
113          |   " True "    -> const_true
114          |   " False "   -> const_false
115
116   !? testlist_comp : ( test | star_expr ) [ comp_for | (" ," ( test | star_expr ) ) + [" ,"] | " ,"]
117   ! subscriptlist : subscript (" ," subscript ) * [" ,"]
118   subscript : test | [ test ] ":" [ test ] [ sliceop ]
119   sliceop : ":" [ test ]
120   ! exprlist : ( expr | star_expr ) (" ," ( expr | star_expr ) ) * [" ,"]
121   ! testlist : test (" ," test ) * [" ,"]
122   ! dictorsetma ker : ( (( test ":" test | "**" expr ) ( comp_for | (" ," ( test ":" test | "**" expr )
           ) * [" ,"]) ) | (( test | star_expr ) ( comp_for | (" ," ( test | star_expr ) ) * [" ,"]) ) )
123
124   classdef : " class " NAME ["(" [ arguments ] ") "] ":" suite
125   ! arguments : argvalue (" ," argvalue ) * [" ," [ starargs | kwargs ]]
126             | starargs
127             | kwargs
128             | test comp_for
129
130   ! starargs : "*" test (" ," "*" test ) * (" ," argvalue ) * [" ," kwargs ]
131   kwargs : "**" test
132
133   ? argvalue : test ["=" test ]
134
135   comp_iter : comp_for | comp_if | async_for
136   async_for : " async " " for " exprlist " in " or_test [ comp_iter ]
137   comp_for : " for " exprlist " in " or_test [ comp_iter ]
138   comp_if : " if " test_nocond [ comp_iter ]
139
140   // not used in grammar , but may appear in " node " passed from Parser to Compiler
141   encoding_decl : NAME



                                                                    42
142
143   yield_expr : " yield " [ yield_arg ]
144   yield_arg : " from " test | testlist
145
146
147   number : DEC_NUMBER | HEX_NUMBER | OCT_NUMBER | FLOAT_NUMBER
148
149   string : STRING | LONG_STRING
150
151   // Tokens
152   NAME : /[ a - zA - Z_ ]\ w */
153   COMMENT : /#.*(\ n [\ t ]*) +/ | LONG_STRING
154   _NL : ( /(\ r ?\ n [\ t ]*) +/ | COMMENT ) +
155
156   LONG_STRING : /[ ubf ]? r ?("""(? <!\\) .*?"""| ’ ’ ’(? <!\\) .*? ’ ’ ’) / is
157
158   DEC_NUMBER : /0|[1 -9]\ d */ i
159   HEX_NUMBER .2: /0 x [\ da - f ]*/ i
160   OCT_NUMBER .2: /0 o [0 -7]*/ i
161   BIN_NUMBER .2 : /0 b [0 -1]*/ i
162   FLOAT_NUMBER .2: /((\ d +\.\ d *|\.\ d +) ( e [ -+]?\ d +) ?|\ d +( e [ -+]?\ d +) ) / i
163
164   % import common . WS_INLINE
165
166   % declare _INDENT _DEDENT
167   % ignore WS_INLINE
168   % ignore /\\[\ t \ f ]*\ r ?\ n /     // LINE_CONT
169   % ignore COMMENT

                                                         Listing 8: Python Grammar




                                                                           43
     A.8.4      Go Grammar

1
2     start : package_c lause eos ( import_decl eos ) * (( function_decl | method_decl | declaration )
           eos " eoc "?) *
3
4     package_clau se : " package " NAME
5
6     import_decl : " import "            ( import_spec | "(" ( import_spec eos ) * ") ")
7
8     import_spec : ("." | NAME ) ? import_path
9
10    import_path : string_
11
12    declaration : const_decl | type_decl | var_decl
13
14    const_decl : " const "          ( const_spec | "(" ( const_spec eos ) * ") ")
15
16    const_spec : id e nt if ie r _l is t ( type_ ? "=" ex pr e ss io n_ li s t ) ?
17
18    identifier_l is t : NAME (" ," NAME ) *
19
20    expression_l is t : expression (" ," expression ) *
21
22    type_decl : " type " ( type_spec | "(" ( type_spec eos ) * ") ")
23
24    type_spec : alias_decl | type_def
25
26    alias_decl : NAME "=" type_
27
28    type_def : NAME t y pe _p ar a me te rs ? type_
29
30    type_paramet er s : "[" t y p e _ p a r a m e t e r _ d e c l (" ," t y p e _ p a r a m e t e r _ d e c l ) * "]"
31
32    t y p e _ pa r a m e t e r _ d e c l : i de nt if i er _l is t type_element
33
34    type_element : type_term ("|" type_term ) *
35
36    type_term : "~"? type_
37
38    // Function declarations
39
40    function_decl : " func " NAME ty pe _p a ra me te r s ? signature ("{" statem ent_list ? ("}" | " eof ") ) ?
41
42    method_decl : " func " receiver NAME signature block ?
43
44    receiver : parameters
45
46    var_decl : " var " ( var_spec | "(" ( var_spec eos ) * ") ")
47
48    var_spec : id en ti f ie r_ li s t ( type_ ("=" e x pr es si on _ li st ) ? | "=" e xp r es si on _ li st )
49
50    block : "{" statemen t_list ? "}"
51
52    statement_li st : ((";"? | EOS ?) statement eos ) +
53
54    statement : declaration | labeled_stmt | simple_stmt | go_stmt | return_stmt | break_stmt |
           continue_stmt | goto_stmt | f a l l t h r o u g h _ s t m t | block | if_stmt | switch_stmt |
           select_stmt | for_stmt | defer_stmt
55
56    simple_stmt : send_stmt | inc_dec_stmt | assignment | expression | sh ort_var_ decl
57
58    send_stmt : expression              " < -" expression
59
60    inc_dec_stmt : expression ("++" | " - -")
61
62    assignment : expression assign_op expression | e xp re s si on _l i st "=" e xp re ss i on _l is t
63
64    assign_op : "+=" | " -=" | "|=" | "^=" | "*=" | "/=" | "%=" | " < <=" | " > >=" | "&=" | "&^="
65
66    short_var_de cl : e xp re s si on _l i st ":=" e xp re s si on _l i st
67
68    labeled_stmt : NAME ":" statement ?
69
70    return_stmt : " return " e x pr es si o n_ li st ?
71
72    break_stmt : " break " NAME ?
73
74    continue_stmt : " continue " NAME ?
75




                                                                                     44
76    goto_stmt : " goto "           NAME
77
78    fallthrough_ st m t : " fallthrough "
79
80    defer_stmt : " defer " expression
81
82    if_stmt : " if " ( expression | eos expression | simple_stmt eos expression ) block (" else " (
           if_stmt | block ) ) ?
83
84    switch_stmt : e x pr _ s w i t c h _ s t m t | t y p e _ s w i t c h _ s t m t
85
86    expr_switch_ st m t : " switch "             ( expression ? | simple_stmt ? eos expression ?) "{"
           expr_cas e _ c l a us e * "}"
87
88    expr_case_cl au s e : e x p r _ s w i t c h _ c a se ":" st atement_ list ?
89
90    expr_switch_ ca s e : " case " e x pr es si o n_ li st | " default "
91
92    type_switch_ st m t : " switch " ( t y p e _ s w i t c h _ g u a r d | eos t y p e _ s w i t c h _ g u a r d | simple_stmt eos
           ty pe_ sw i t c h _ g u a r d ) "{" t y p e _ c a s e _ c l a u s e * "}"
93
94    ty pe_ swit ch_ g u a r d : ( NAME ":=") ? NAME "." "(" " type "                       ") "
95
96    type_case_cl au s e : t y p e _ s w i t c h _ c a se ":" st atement_ list ?
97
98    type_switch_ ca s e : " case " type_list | " default "
99
100   type_list : ( type_ | " nil " ) (" ," ( type_ | " nil "                          ))*
101
102   select_stmt : " select " "{" comm_clause * "}"
103
104   comm_clause : comm_case ":" st atement_ list ?
105
106   comm_case : " case " ( send_stmt | recv_stmt ) | " default "
107
108   recv_stmt : ( ex p re ss io n _l is t "=" | i d en ti fi e r_ li st ":=") ? expression
109
110   for_stmt : " for " [ for_clause ] block
111
112   for_clause : simple_stmt ( eos expression eos simple_stmt ) ? | range_clause
113
114   range_clause : ( e xp re ss i on _l is t "=" | ex pr es s io n_ li s t ":=") " range "             expression
115
116   go_stmt : " go " expression
117
118   type_ : literal_type | v a r _ o r _ t y p e _ na m e type_args ? | "(" type_ ") "
119
120   channel_type
121
122   type_args : " - -"
123
124   var_or_type_ na m e : NAME "." NAME | NAME | NAME "." "(" type_ ") "
125
126   array_type : "[" array_length "]" element_type
127
128   array_length : expression
129
130   element_type : type_
131
132   pointer_type : "*" type_
133
134   interface_ty pe : " interface " "{" (( method_spec | type_element ) eos ) * "}"
135
136   slice_type : "[" "]" element_type
137
138   // It ’ s possible to replace ‘ type ‘ with more restricted type_lit list and also pay attention
             to nil maps
139   map_type : " map " "[" type_ "]" element_type
140
141   channel_type : (" ’ chan "             | " chan "        " < -" |     " < -" " chan " ) element_type
142
143   method_spec : NAME parameters result | NAME parameters
144
145   function_type : " func " signature
146
147   signature : parameters result ?
148
149   result : parameters | type_
150
151   parameters : "(" paramete r_decl (" ," pa rameter_ decl ) * " ,"? ") " | "(" ") "
152




                                                                                        45
153   // a comma - separated list of either ( a ) name , ( b ) type , or ( c ) name and type
154   // parameter_ decl : i d en ti fi e r_ li st ? "..."? type_
155
156
157   // Although following is o ve r ap pr ox i ma te it ’ s an easy way to avoid reduce / reduce conflicts
158   parameter_de cl : ( type_ | "..."? type_ | NAME type_ )
159
160
161   expression : primary_expr
162                | ("+" | " -"                 | "!" | "^" | "*" | "&" | " < -") expression
163                | expression                  ("*" | "/" | "%" | " < <" | " > >" | "&" | "&^") expression
164                | expression                  ("+" | " -" | "|" | "^") expression
165                | expression                  ("==" | "!=" | " <" | " <=" | " >" | " >=") expression
166                | expression                  "&&" expression
167                | expression                  "||" expression
168
169   primary_expr : operand | primary_expr ("." ( NAME | "(" type_ ") ") | index | slice_ |
           arguments ) | type_
170
171   // Giving operand higher precedence than type_ is a hack to avoid reduce / reduce conflicts
172   operand .3: literal | NAME | "(" expression ") " // removed NAME type_args ?
173
174   literal : basic_lit | composite_lit | function_lit
175
176   basic_lit : " nil " | integer | string_ | FLOAT_LIT | CHAR_LIT
177
178   integer : DECIMAL_LIT | BINARY_LIT | OCTAL_LIT | HEX_LIT
179
180   DECIMAL_LIT : /0|[1 -9]\ d */ i
181   HEX_LIT .2: /0 x [\ da - f ]*/ i
182   OCTAL_LIT .2: /0 o [0 -7]*/ i
183   BINARY_LIT .2 : /0 b [0 -1]*/ i
184   FLOAT_LIT .2: /((\ d +\.\ d *|\.\ d +) ( e [ -+]?\ d +) ?|\ d +( e [ -+]?\ d +) ) / i
185   CHAR_LIT : / ’. ’/ i
186
187   composite_lit : literal_type literal_value
188
189   literal_type : struct_type | array_type | "[" "..." "]" element_type | slice_type | map_type
           | " interface " "{" "}"
190
191   literal_value : "{" ( element_list " ,"?) ? "}"
192
193   element_list : keyed_element (" ," keyed_element ) *
194
195   keyed_element : ( key ":") ? element
196
197   key : expression | literal_value
198
199   element : expression | literal_value
200
201   struct_type : " struct " "{" ( field_decl eos ) * "}"
202
203   field_decl : ( i de nt if i er _l is t type_ | embedded _field ) string_ ?
204
205   string_ : RAW_STRING _LIT | I N T E R P R E T E D _ S T R I N G _ L I T
206
207   RAW_STRING_L IT : / ‘.*? ‘/
208   I N T E R P R E T E D _ S T R I N G _ L I T : /".*?"/ i
209
210   embedded_fie ld : "*"? ( NAME "." NAME | NAME )                   type_args ?
211
212   function_lit : " func " signature block // function
213
214   index : "[" expression "]"
215
216   slice_ : "[" ( expression ? ":" expression ? | expression ? ":" expression ":" expression ) "]"
217
218   type_asserti on : "." "(" type_ ") "
219
220   arguments : "(" ( e x pr es si o n_ li st ? "..."? " ,"?) ? ") "
221
222   eos : ";" | EOS // | { this . closin gBracket () }?
223
224   NAME : /[ a - zA - Z_ ]\ w */
225   EOS : _NL | ";" | "/* ’ .*? ’*/"
226
227   COMMENT : /\/\/[^\ n ]*/
228   _NL : ( /(\ r ?\ n [\ t ]*) +/ | COMMENT ) +
229
230   % ignore /[\ t ]/
231   % ignore /\\[\ t \ f ]*\ r ?\ n /               // LINE_CONT



                                                                                46
Listing 9: Go Grammar




         47
