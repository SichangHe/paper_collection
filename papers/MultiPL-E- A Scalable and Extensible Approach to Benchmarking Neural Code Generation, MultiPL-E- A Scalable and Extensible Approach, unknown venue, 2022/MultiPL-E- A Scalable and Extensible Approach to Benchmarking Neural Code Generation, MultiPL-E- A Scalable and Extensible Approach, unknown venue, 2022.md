                                                                                                                                                                                           1




                                          MultiPL-E: A Scalable and Extensible Approach
                                            to Benchmarking Neural Code Generation
                                         Federico Cassano, John Gouwar, Daniel Nguyen, Sydney Nguyen, Luna Phipps-Costin, Donald Pinckney,
                                          Ming-Ho Yee, Yangtian Zi, Carolyn Jane Anderson, Molly Q Feldman, Arjun Guha, Michael Greenberg,
                                                                                  Abhinav Jangda§



                                                                                                                        F
arXiv:2208.08227v4 [cs.LG] 19 Dec 2022




                                         Abstract—Large language models have demonstrated the ability to                    represented language in training datasets [1, 2, 10, 11]. How-
                                         generate both natural language and programming language text. Such                 ever, we should also evaluate code generation models with
                                         models open up the possibility of multi-language code generation: could            other languages to support a wider variety of programmers.
                                         code generation models generalize knowledge from one language to                       In this paper we present MultiPL-E, a system for trans-
                                         another? Although contemporary code generation models can generate
                                                                                                                            lating code generation benchmarks from Python into new
                                         semantically correct Python code, little is known about their abilities with
                                         other languages. We propose MultiPL-E, a system for translating unit
                                                                                                                            languages, and use it to propose the first massively parallel,
                                         test-driven code generation benchmarks to new languages. We create                 multi-language benchmark for code generation. By “multi-
                                         the first massively multilingual code generation benchmark by using                language” we mean multiple programming languages:
                                         MultiPL-E to translate two popular Python code generation benchmarks               MultiPL-E supports 18 languages and is straightforward to
                                         to 18 additional programming languages.                                            extend with more. By “parallel”, we mean that MultiPL-
                                              We use MultiPL-E to extend the HumanEval benchmark [1] and                    E produces parallel problems for each language, thus we
                                         MBPP benchmark [2] to 18 languages that encompass a range of pro-                  can measure performance of a code generation model on
                                         gramming paradigms and popularity. Using these new parallel bench-
                                                                                                                            a consistent set of problems across multiple programming
                                         marks, we evaluate the multi-language performance of three state-of-
                                                                                                                            languages. What makes MultiPL-E possible is that code
                                         the-art code generation models: Codex [1], CodeGen [3] and InCoder
                                         [4]. We find that Codex matches or even exceeds its performance on                 generation benchmarks have unit tests to determine if the
                                         Python for several other languages. The range of programming lan-                  generated function behaves correctly. However, existing
                                         guages represented in MultiPL-E allow us to explore the impact of lan-             benchmarks only evaluate performance on a single lan-
                                         guage frequency and language features on model performance. Finally,               guage.
                                         the MultiPL-E approach of compiling code generation benchmarks to                      MultiPL-E uses a suite of 18 little compilers from Python
                                         new programming languages is both scalable and extensible, making it               benchmarks to each target language. However, what makes
                                         straightforward to evaluate new models, benchmarks, and languages.                 this scale is that these are not full-fledged compilers. Each
                                                                                                                            compiler must be able to translate four components from
                                                                                                                            Python: (1) a function signature (name and arguments),
                                         1     I NTRODUCTION
                                                                                                                            (2) simple unit tests, (3) a comment describing the expected
                                         Code generation models, also known as large language mod-                          function behavior, and (4) type annotations if the target
                                         els (LLMs) of code, are deep neural networks trained on                            language is statically typed. Notably, the compiler does not
                                         massive corpora of source code. Over the past few years,                           have to translate the body of a function, since it is the job
                                         code generation models have demonstrated their utility                             of the code generation model to synthesize it. Thus each
                                         on a wide variety of software engineering tasks, includ-                           MultiPL-E compiler is approximately 200 LOC and easy to
                                         ing test generation, documentation generation, and even                            build. MultiPL-E also includes a simple, rule-based tool to
                                         synthesizing working programs from natural language de-                            translate technical terms in comments to be more language
                                         scriptions [1, 4, 5, 6, 7]. New products such as GitHub                            appropriate, e.g. a Python list is approximately a C++ vector.
                                         Copilot1 , Amazon CodeWhisperer2 , and Tabnine3 built on                               MultiPL-E also includes a containerized sandbox that
                                         code generation models are growing in popularity with                              (1) compiles programs if necessary, (2) runs them with
                                         developers [8]. Although several code generation models                            appropriate timeouts, (3) validates their results on unit tests,
                                         are trained on multiple programming languages, they are                            and (4) classifies each output as successful, syntax error, etc.
                                         typically only evaluated on a single programming language:                         Thus each language requires an evaluation script, which is
                                         Python. Machine learning researchers are familiar with                             typically about 20 LOC.
                                         Python: they have painstakingly constructed several Python                             We use MultiPL-E to translate two widely-used code
                                         code generation benchmarks [1, 2, 9, 10] and it is the best                        generation benchmarks, HumanEval [1] and MBPP [2], into
                                                                                                                            18 languages. The 18 languages capture a broad spectrum
                                             §. Authors are listed alphabetically with students first, then faculty.
                                             1. https://github.com/features/copilot/                                        of language features, application areas, and popularity, al-
                                             2. https://aws.amazon.com/codewhisperer/                                       lowing us to explore the impact of these factors on model
                                             3. https://www.tabnine.com/                                                    performance.
                                                                                                                                     2

    We use the multi-language parallel MultiPL-HumanEval                   (a) The prompt given to the NL2Code model:
and MultiPL-MBPP benchmarks to evaluate three state-of-           def lsi(lst):
the-art code generation models: Codex [1], CodeGen [3], and         """Create a function that returns a
InCoder [4]. Our evaluation presents new insights into the          tuple (a, b), where ’a’ is the largest
                                                                    of negative integers, and ’b’ is the
effectiveness of code generation models, including:                 smallest of positive integers in a
                                                                    list. If there is no negative or
    1)   Across models and benchmarks, code generation              positive integers, return them as
         models perform extremely well on JavaScript, some-         None.
         times outperforming Python, even on benchmarks             Examples:
         originally designed to evaluate Python perfor-               lsi([2, 4, 1, 3, 5, 7]) == (None, 1)
                                                                      lsi([]) == (None, None)
         mance. Codex also performs well on C++, Scala, and           lsi([0]) == (None, None)
         TypeScript.                                                """
    2)   There is no strong correlation between model per-
         plexity and correctness of generated code, which                      (b) A completion generated by Codex:
         suggests that perplexity may not be a good estimate        if len(lst) == 0:
         of performance.                                              return (None, None)
                                                                    else:
    3)   Code generation performance is correlated with lan-
                                                                      neg_nums = [x for x in lst if x<0]
         guage popularity, but some niche languages per-              pos_nums = [x for x in lst if x>0]
         form as well as more popular languages.                    if len(neg_nums) == 0:
    4)   Code generation performance is sensitive to prompt           neg_nums = None
                                                                    if len(pos_nums) == 0:
         design for both niche and popular languages.                 pos_nums = None
    5)   Static type-checking neither helps nor hinders code        return (max(neg_nums), min(pos_nums))
         generation model performance.
                                                                    (c) 3 of the 12 unit tests (the generated solution fails two):
    To summarize, our key contributions are:
                                                                  X assert lsi([2, 4, 1, 3, 5, 7]) == (None, 1)
    •    MultiPL-E: a suite of compilers and an evaluation        X assert lsi([2, 4, 1, 3, 7, 0]) == (None, 1)
                                                                  X assert lsi([1, 3, 4, 5, 6, -2]) == (-2, 1)
         framework for translating code generation bench-
         marks from Python into other programming lan-            Figure 1: Problem 136 of 164 of the HumanEval benchmark.
         guages. MultiPL-E translates unit tests, doctests,       We shorten the name largest_smallest_integers
         Python-specific terminology, and type annotations.       for brevity. Top: the prompt for the model, with the
    •    Two parallel benchmarks for code generation in 19        function signature , natural language description, and
         languages encompassing a variety of programming          doctests . Middle: a Codex-generated solution. Bottom: unit
         paradigms, language features, and popularity levels.     tests.
    •    A multi-language parallel evaluation of three mod-
         els, Codex [1], InCoder [4], and CodeGen [3].
    •    Explorations of language frequency effects, the im-      promise of synthesizing knowledge gleaned from code in
         pact of type annotations, and prompt translation         multiple programming languages. Just as language models
         sensitivity on code generation performance, along        exposed to multiple natural languages are able to generalize across
         with a fine-grained error analysis for four languages.   languages, might not multi-language models of code do the same?
    We hope this evaluation work will help the many                   Although this kind of multi-language generalization is
software engineers that do not use Python to assess the           an intriguing possibility, little is known about how well
feasibility of code generation models for their work and          code generation models perform across programming lan-
to understand the language factors that may affect model          guages. We make progress towards answering this question
performance.                                                      by proposing two large-scale parallel benchmarks for code
    The MultiPL-E system, dataset, and tutorial are available     generation in 19 languages, which we use to evaluate three
at github.com/nuprl/MultiPL-E.                                    state-of-the-art models: Codex, CodeGen, and InCoder.


2   C ODE G ENERATION                                             2.1   The Natural Language to Code Task
Code generation has long been a task of interest: there is        Code generation models have been applied to a variety of
extensive work on program synthesis [12, 13, 14] using both       tasks, including test generation [19], docstring generation
symbolic and neuro-symbolic approaches. More recently,            [20], code search [17, 21], type inference [22, 23, 24], and
large neural language models (LLMs) trained for text gen-         more [25]. We focus on the natural-language-to-code task
eration have demonstrated the ability to perform program          (NL2Code): given the description of a function in natural
completion [5, 15, 16]. Since 2020, several code generation       language, complete the function body.
models have been trained or fine-tuned on programming                 The input to a code generation model is called a prompt.
language text [1, 4, 6, 7, 17, 18].                               Figure 1a shows an example prompt from the HumanEval
    Unlike traditional program synthesis techniques, neural       benchmark for NL2Code [1]. The prompt has several
language models are able to condition on and generate both        sources of information for the model: the function signature
natural language (i.e., code comments) and programming            (its name and parameters); a brief comment describing the
language text. Moreover, code generation models offer the         function; and, optionally, examples in the form of Python
                                                                                                                               3

doctests. Given the prompt as input, the code generation          def mean(n):
                                                                      return sum(n)/len(n)
model generates a completion that is likely to follow the given
prompt.                                                           def variance(n):
    Note that the model does not receive an explicit cue              mean = mean(n)
about the target language, but each of the three prompt               return sum([(n-mean)**2 for n in n])/len(n)
regions provide implicit cues: the syntax of the function         def standard_deviation(n):
signature, the terminology used in the natural language               return math.sqrt(variance(n))
description, and the syntax of the doctests all suggest that
                                                                  def mode(n):
the target is Python. Consequently, to translate this prompt
                                                                      counts = Counter(n)
to a new programming language, we must target all three               max_count = max(counts.values())
regions of the prompt.                                                return [k for k,v in counts.items()
                                                                              if v == max_count]

2.2   Sampling Program Completions                                Figure 2: Code generation models produce tokens, not ASTs,
There are several ways to configure how a code generation         and may produce output beyond that requested. This is
model produces completions, each of which can have a              truncated output from InCoder given just the first high-
significant effect on the quality of generated code. Funda-       lighted line as the prompt.
mentally, a completion is a sequence of tokens and is not an
abstract syntax tree. Therefore, a completion can readily pro-
duce tokens that go beyond a single function. For example,        the 12 unit tests that accompany the problem from Figure
given just the the signature of “mean”, InCoder produces          1a. Note that these unit tests are simple assertions: each
the mean, variance, standard deviation, and several other         test asserts that the output value produced by the function
functions (Figure 2). In fact, it can continue producing code     matches an expected value.
up to the maximum sequence length, which, for InCoder, is             We judge a generated function correct if it passes all
2048 tokens.                                                      tests. Figure 1b shows just one of the solutions generated
    We control this output by specifying stop sequences that      by Codex for the example prompt. This solution is incorrect
typically demarcate the end of a function. For Python, we         because it fails some of the unit tests (Figure 1c). Because
use the stop sequences that have been employed in prior           the output of the code generation model is stochastic, it is
work [1]. For example, when completing a top-level func-          common to sample multiple completions per problem and
tion, \ndef marks the start of the next top-level function,       report an estimated pass rate (§4.2).
but allows nested helper functions. For other languages, we
design different sets of stop sequences (§A).
                                                                  3     T HE M ULTI PL-E A PPROACH
    Under the hood, given a prompt, a code generation
model produces a completion one token at a time. At each          This section describes how we select and prepare languages
step, the neural network receives an encoded prompt as            and benchmarks for MultiPL-E.
input and produces a distribution for the following token.
To generate several tokens, a sampling algorithm iteratively      3.1   Benchmark Selection
samples next tokens, extending the prompt at each step with
                                                                  There are a number of existing single-language NL2Code
the previously sampled token.
                                                                  benchmarks [9, 10, 11]. We choose to translate Hu-
    There are a variety of sampling approaches that one can
                                                                  manEval [1] and MBPP [2] as two of the most widely-used
use. A naive approach is to greedily sample the next most
                                                                  benchmarks.
likely token, but this performs poorly in practice [26]. One
                                                                      HumanEval is a good choice of benchmark for several
approach employed in prior work [1], and in this article, is to
                                                                  reasons. It is a diverse collection of 164 problems, where
rescale the probability distribution to favor high probability
                                                                  all problems have tests to check correctness, and most have
tokens more strongly using a temperature hyperparameter
                                                                  examples or doctests as part of the prompt. All of the prob-
(0 ≤ t < 1): low temperature makes the completion more
                                                                  lems are functions that receive and return first-order values,
“predictable” and high temperature makes it more “cre-
                                                                  which facilitates unit testing and test translation. Many also
ative”. This is commonly combined with top-p sampling,
                                                                  use Python’s optional type annotations. Moreover, it is a
which cuts off the least likely tokens that contribute in
                                                                  challenging benchmark: the best model evaluated by Fried
aggregate 1 − p to the probability mass, and redistributes
                                                                  et al. [4] achieves only a 36% pass rate on Python.
their mass to the remaining tokens.
                                                                      MBPP is another large, commonly used benchmark of
                                                                  Python problems. As originally formulated, it is a little
2.3   Evaluating Code Generation                                  unusual. Each problem has a description and a list of
Early work on code generation relied on textual similarity        assertions. The prompt for code generation includes both
metrics for evaluation [17, 27]. However, previous work           the description and the assertions, and the generated code
shows that textual similarity is not reliably correlated with     is then tested with the same set of assertions. We argue that
code correctness [1, 2]. The best way to evaluate code            the HumanEval approach, where test cases are hidden, is
generation is to test code correctness using a suite of hidden    a significantly better way to evaluate code generation. We
unit tests.                                                       therefore remove the assertions from the MBPP prompts
   We translate two code generation benchmarks that in-           so that we can use them as hidden unit tests. However,
clude unit tests for every problem. Figure 1c shows 3 of          with only a problem description, a code generation model
                                                                                                                                    4

# Write a function to fnd the smallest missing                      PL           Typed?    GitHub %     TIOBE    Category    LOC
# element in a sorted array. Your code should                       Bash           ×       -            43       N ICHE       120
# satisfy these tests:                                              C++            X       7.0          4        H IGH        244
assert smallest_missing([0, 1, 2, 3, 4, 5, 6],                      C#             X       3.1          5        M EDIUM      149
                        0, 6) == 7                                  D              X       -            35       N ICHE       117
assert smallest_missing([0, 1, 2, 6, 9, 11, 15],                    Go             X       7.9          12       M EDIUM      210
                        0, 6) == 3                                  Java           X       13.1         3        H IGH        153
assert smallest_missing([1, 2, 3, 4, 6, 9, 11, 15],                 JavaScript     ×       14.3         7        H IGH         45
                        0, 7) == 0                                  Julia          ×       0.1          28       N ICHE       125
                                                                    Lua            ×       0.2          25       N ICHE        43
(a) An original MBPP prompt: the same assertions are used to        Perl           ×       0.3          17       L OW          49
test the generated code. (Typo in comment is from the original      PHP            ×       5.3          11       M EDIUM       50
benchmark.)                                                         R              ×       0.05         19       L OW          98
                                                                    Racket         ×       -            -        N ICHE        38
                                                                    Ruby           ×       6.2          15       M EDIUM       41
def smallest_missing(l):                                            Rust           X       1.1          22       L OW         147
   """                                                              Scala          X       1.7          32       L OW         152
   Write a function to fnd the smallest missing                     Swift          X       0.7          10       L OW         479
   element in a sorted array.                                       TypeScript     X       9.1          33       H IGH        117
   """
                                                                  Table 1: MultiPL-E languages by frequency, as calculated by
(b) We add the function signature and hide the test cases to do   GitHut 2.0 and the 2022 TIOBE Programming Community
a more rigorous evaluation.                                       index; the LOC column indicates the number of semantic
Figure 3: An original MBPP prompt and how we modify it            lines of code in our compiler.
to standardize evaluation.

                                                                  3.3.1   Compiling Unit Tests
is free to make up the name of a function (or not even            MultiPL-E supports any unit test where the input and
produce a function). Therefore, we mechanically augment           output to the test are first-order values. In Python, these
every prompt with a function signature, based on the name         include constants and data structures such as lists, tuples,
and arity implied by the assertions. Figure 3 shows an            and dictionaries, but exclude values such as lambda expres-
example of an original MBPP prompt and our modification.          sions.4 HumanEval and MBPP unit tests apply the model-
                                                                  generated function to a first-order value, and compare the
                                                                  result with an expected first-order value.
3.2   Programming Language Selection
                                                                      Each MultiPL-E compiler has a recursive function that
MultiPL-E supports 19 programming languages, which                compiles Python values to the target language’s values.
we categorize into four frequency classes (N ICHE, L OW,          Even for an untyped target, this value-to-value compilation
M EDIUM, or H IGH) based on a weighting of TIOBE rank             requires care, because not all Python value types have per-
and GitHub frequency (Table 1). Eight of the languages in         fect analogues in every target. For example, we compile both
MultiPL-E had never been used before to measure NL2Code           tuples and lists to JavaScript arrays, since JavaScript lacks
performance; this set includes newer languages (Julia and         a canonical tuple type. We also support untyped targets
Swift), older scripting languages (Bash and Perl), and lan-       where the compilation strategy is less obvious. For example,
guages for specific applications (Lua and R). Half of the         when the target is R, it may appear natural to compile
languages are statically type-checked. The broad range of         Python lists to R lists: both kinds of lists can be nested
languages in MultiPL-E shows the generality of our com-           and allow heterogenous values. However, R’s vector type
pilation approach and allows us to explore how language           is much more commonly used (data frames are made of
frequency and language features affect performance (§6).          vectors). Unfortunately, vectors must be homogeneous and
    A key feature of MultiPL-E is that it is easy to extend       cannot be nested, so not all Python lists can be translated
with new models, benchmarks, and languages. To support            to vectors. For example, an argument typed List[Int] can
new languages and benchmarks without manual (and error-           be translated to a vector, but a nested list cannot. In order
prone) effort, we build 18 compilers to translate NL2Code         to more closely match the token distribution of idiomatic
benchmarks written in Python. Writing one of these com-           R code seen during training, our R compiler uses types
pilers is straightforward when the target language is similar     (described below) to identify homogenous list values and
to Python, but requires care for typed languages and even         maps them to vectors using c()—even though R is untyped.
some untyped languages, notably Perl, Bash, and R.                    The final step of compiling tests is to choose an appro-
                                                                  priate test for equality. The meaning of equality operators
                                                                  varies across programming languages. Python’s == operator
3.3   Compiling Python Benchmarks
                                                                  checks deep equality, i.e., item-by-item equality within data
A MultiPL-E compiler is significantly easier to build than        structures. Deep equality is the appropriate choice for unit
a complete compiler. To translate a benchmark problem,            tests. In some languages, we need to import equality-testing
we only need to compile function signatures and unit tests        functions from testing libraries, as in the JavaScript example
(not arbitrary statements and expressions). Our compilers         shown in Figure 4.
preserve comments, since they contain the natural language
description for the NL2Code task; however, we automati-             4. We do not support testing higher-order functions, but support
cally rephrase them to replace Python-specific terminology.       generated code that uses higher-order functions.
                                                                                                                              5

               (a) Original Python assertion.                        (a) Original Python docstring from HumanEval #95.
assert lsi([0]) == (None, None)                                 Given a dictionary , return True if all keys are
                                                               strings in lower case or all keys are strings in
                     (b) Equivalent R.                         upper case, else return False . The function should
                                                               return False is the given dictionary is empty.
if(!identical(lsi(c(0)), c(NULL, NULL))){
    quit(’no’, 1)}                                                            (b) Terminology translated to Perl.
                                                                Given a hash , return 1 if all keys are strings
                 (c) Equivalent JavaScript.                    in lower case or all keys are strings in upper case,
assert.deepEqual(lsi([0]), [void 0, void 0]);                  else return "" . The function should return "" is
                                                               the given hash is empty.
        Figure 4: Example of a translated assertion.
                                                               Figure 5: A Python docstring and its Perl translation. Errors
                                                               (e.g., “is” for “if”) are from the original benchmark.
3.3.2 Translating Types and Type Inference
Compiling a function signature to an untyped language is
straightforward, but requires care when the target is typed.   the impact of these differences, we identify Python-specific
Most typed languages require argument and return type          terminology in the natural language portion of the prompt,
annotations. Python has optional type annotations. Thus if     and translate it to the most natural equivalent for the target
a benchmark has type annotations, we can translate them        language. Figure 5 shows an example of a prompt translated
to types in a target language. Fortunately, a large subset     from Python to Perl. Notably, Perl not only lacks Booleans,
of the HumanEval benchmarks employ Python’s optional           but uses 1 for true and the empty string for false.
type annotations. We introduce type annotations to the few        We conservatively avoid translating number types. Al-
that do not. None of the MBPP benchmarks have type an-         though some target languages use different terms for floats
notations. Instead of manually adding annotations to 400+      and integers, the term integer is commonly used in a mathe-
benchmarks, we infer the types of the values that appear in    matical sense rather than in reference to the Python type.
the MBPP assertions.
    Translating types and typed values is subtly different
                                                               3.4   Limitations of Our Approach
for every language. For example, five HumanEval problems
use types such as Any which cannot be translated to most       A handful of benchmarks cannot be easily translated using
traditional statically typed languages (e.g., C++ and Rust).   the MultiPL-E approach. Of the 164 original HumanEval
We fail to compile these few problems to these languages.      benchmarks: (1) we exclude 3 benchmarks that have Python
    Another problem arises when compiling to languages         helper functions in their prompt; (2) we modify 2 bench-
with algebraic datatypes or discriminated unions. For ex-      marks to use unit tests instead of randomized testing; and
ample, consider translating the Python type Optional[Int]      (3) for certain typed languages, we fail to compile up to
to Rust, Swift, or Scala. The analogous type in the target     5 benchmarks with untranslatable types. These changes do
language is an algebraic datatype. This means that when the    not lead to significantly different results for Python (§5.1.1).
Python number n has type Optional[Int] it must translate           Our approach can be generalized to additional pro-
to the value Some(n). Optional values are very common in       gramming languages, so long as the target language has
Python benchmarks, and we use this approach extensively.       natural analogues for the Python data types used in the
    Finally, many typed languages require type annotations     benchmarks. We do not include two previously studied
in data structures, which appear in unit tests. For example,   languages, C [7] and SQL [28, 29] because they do not meet
C++ vectors require an annotation specifying their element     this criterion.
type, and numbers in Rust (sometimes) require a type suffix.
We perform limited local type inference to calculate these     4     C ODE G ENERATION M ODELS
types from the type of the function signature to ensure that
                                                               We evaluate three state-of-the-art code generation models,
the unit tests always compile successfully.
                                                               each of which use a Transformer architecture [30] and are
3.3.3 Translating Doctests                                     trained with a language modeling objective on a mixture of
                                                               natural language and code. We evaluate the largest, best-
Python doctests are a standard format for examples in docu-
                                                               performing versions of each of these three models.
mentation. While many of the HumanEval prompts include
examples, not all of them are validly formatted doctests. We
standardize examples to the Python doctest format (">>>"       4.1   Models
prepended). We apply value-to-value compilation to the         InCoder InCoder [4] is a 6.7B parameter language model
doctests as we do for unit tests. However, since not all       trained using a causal masking objective [31]. It supports
languages have an equivalent doctest format, we keep the       both code infilling and code completion; we test only the
Python format for all target languages.                        latter. InCoder was trained on 159 GB of deduplicated,
                                                               filtered code from Github (around a third in Python) and
3.3.4 Translating Python Terminology in Prompts                57 GB from StackOverflow.
Different programming languages use different terminology           CodeGen CodeGen is a 16.1B parameter language model
to refer to the same concept. For example, a Python list is    trained with a next-token prediction objective. We evaluate
closest to a JavaScript array or a Rust vector. To mitigate    the multilingual CodeGen model, which was trained first on
                                                                                                                                                                                   6


                    0.8




                    0.6
Average pass rate




                    0.4




                    0.2




                    0.0
                          Python


                                   Bash


                                          JavaScript


                                                       Lua


                                                             Perl


                                                                    PHP


                                                                            R


                                                                                  Ruby


                                                                                         Racket


                                                                                                      C++


                                                                                                              C#


                                                                                                                   D


                                                                                                                          Go


                                                                                                                                Java


                                                                                                                                       Julia


                                                                                                                                               Rust


                                                                                                                                                      Scala


                                                                                                                                                              Swift


                                                                                                                                                                      TypeScript
                                                                                         Language
                                                                                     InCoder HE               InCoder MBPP
                                                                          Expt.      CodeGen HE               CodeGen MBPP
                                                                                     Codex HE                 Codex MBPP


Figure 6: Pass@1 rates for all languages in MultiPL-HumanEval and MultiPL-MBPP. From left to right: InCoder, CodeGen,
Codex.


The Pile [32], a 825 GB dataset of mostly natural language                                        calculate average pass rate using the unbiased sampling
text with around 8% Github-scraped code. The model was                                            estimator presented in [1].6
further trained (fine-tuned) on a 6 programming language
subset (C, C++, Go, Java, JavaScript, and Python) of the
                                                                                                  5         E VALUATION
BigQuery code dataset.5
    Codex Codex is a GPT-3 language model fine-tuned on                                           In this section, we present the results of evaluating
code. [1] describe a 12B parameter version of Codex fine-                                         Codex, InCoder, and CodeGen on MultiPL-HumanEval and
tuned on 159 GB of deduplicated, filtered Python code                                             MultiPL-MBPP. We fit mixed-effects models to evaluate the
from Github. We use the more recent codex-davinci-002                                             statistical significance of the differences between groups that
model, which is trained on multiple languages. Details of its                                     we report below [34]. Appendix C has a full description of
training set and size are not public [33]. We use the public                                      each statistical model with its estimate table.
OpenAI API to query Codex.
                                                                                                  5.1       MultiPL-HumanEval results
                                                                                                  We explore the code generation abilities of the three mod-
4.2                  Metrics                                                                      els on our translated version of HumanEval, MultiPL-
For each language, we calculate pass@k using the method-                                          HumanEval. Figure 6 shows the by-language performance
ology employed by [1] and subsequent work. Intuitively,                                           of each model on both benchmarks.
pass@1 is the likelihood of the model producing a com-                                                We find reliable differences between Codex pass@1 rates
pletion that passes all unit tests, pass@10 is the likelihood                                     on MultiPL-HumanEval for Python and all but 4 languages:
of any one of 10 completions passing all unit tests, and                                          C++, JavaScript, Scala, and TypeScript. For these languages,
so on. We calculate pass@1 with temperature 0.2, and use                                          Codex performance is similar to Python.
temperature 0.8 for pass@10 and pass@100. For statistical                                             CodeGen performs best on the languages included in
reliability, we take 200 completions at each temperature and                                      its fine-tuning dataset (Python, JavaScript, Java, C++, and

                                                                                                    6. We note that pass@1 rates appear to stabilize around 20 samples,
  5. https://cloud.google.com/blog/topics/public-datasets/github-                                 suggesting that future work could achieve a stable estimate with a less
on-bigquery-analyze-all-the-open-source-code                                                      computationally costly sample size.
                                                                                                                                                                                   7


                                           High                               Medium                                   Low                                  Niche
               0.8



               0.6
Pass@1 rates




               0.4



               0.2



               0.0
                     Python

                              JavaScript

                                            C++

                                                  Java

                                                         TypeScript



                                                                      PHP


                                                                              Ruby


                                                                                     C#


                                                                                            Go



                                                                                                         Perl

                                                                                                                   R

                                                                                                                        Rust

                                                                                                                               Scala

                                                                                                                                       Swift


                                                                                                                                               Bash

                                                                                                                                                      Lua

                                                                                                                                                              Racket

                                                                                                                                                                       D

                                                                                                                                                                           Julia
                                                                                          Language
                                                                            Model      InCoder       CodeGen               Codex


Figure 7: Model performance on MultiPL-HumanEval by language frequency and type-checking. Languages to the left of
dashed line are untyped; languages to the right are typed.


Go). It also performs well on TypeScript, likely due to its                                      (+2.3%; p = 0.43). Codex achieves a pass@1 rate higher than
similarity to JavaScript. A mixed-effects model finds reliable                                   40% on C++, Java, TypeScript, PHP, Ruby, Rust, Scala, and
differences in pass@1 rates on MultiPL-HumanEval between                                         Lua.
all languages and Python, except Ruby, where performance                                             The Codex training set is not public; it is possible that
is so low that the model fails to find a reliable estimate.                                      the latest model has been trained on solutions to the Hu-
    InCoder performs significantly better on the Python ver-                                     manEval benchmarks in Python, and this could be inflating
sion of MultiPL-HumanEval than all of the other language                                         its performance. However, MultiPL-HumanEval is a new
versions (p < 0.001 for all languages).                                                          dataset for the 18 other languages. That Codex matches
                                                                                                 or exceeds its Python performance on some of these new
5.1.1 Python Results and Replication                                                             languages suggests a negligible impact of any train/test
Our InCoder results on Python exactly replicate its previ-                                       overlap.
ously reported performance on HumanEval [4]. We measure                                              CodeGen also performs well on JavaScript and Type-
a slightly higher pass@1 rate for CodeGen than what is                                           Script, though the latter is not included in its fine-tuning
reported in [3] (19.2% compared to 18.3%).7 These findings                                       dataset.
show that the small standardization changes we made to the                                           InCoder’s performance is the weakest. Like the other
HumanEval benchmarks do not significantly affect model                                           models, it performs better on more frequently-used lan-
performance.                                                                                     guages (Python) than less popular ones. However, unlike
   We evaluate a more recent Codex model (code-                                                  Codex and CodeGen, it does not match its Python perfor-
davinci-002) than the original paper and observe a large                                         mance on any other language.
improvement on Python: a pass@1 rate of 45.9%, com-
pared to 28.8% reported earlier [1]. Our pass@1 rate on the                                      5.1.3          Performance by Language Frequency
Python HumanEval subset replicates what is reported for
code-davinci-002 in [35].8                                                                       Figure 7 shows MultiPL-HumanEval pass@1 rates for each
                                                                                                 model, grouping languages by frequency. All three models
5.1.2 Codex Performs Best on JavaScript                                                          perform best on high frequency languages.
                                                                                                     Although we find reliable differences in Codex pass@1
Codex’s performance on JavaScript is better than its perfor-
                                                                                                 rates between the M EDIUM, L OW, and N ICHE languages
mance on Python, though the difference is not significant
                                                                                                 when compared to the H IGH category (p = 0.006; p < 0.001;
  7. We note that [3] calculates the pass@1 rate for 3 temperatures,                             p = 0.002), we observe that Codex performs very well on
and reports the best result without specifying the temperature. Con-                             some L OW and N ICHE languages. For instance, Lua is the
sequently, it’s not clear whether the 18.3% pass@1 rate they report is                           9th-best language in our Codex evaluation, although it only
measured at the 0.2 temperature that we use.
                                                                                                 appears in 0.2% of GitHub activity and is not in the TIOBE
  8. We note that [35] also reports results for InCoder and a monolin-
gual version of CodeGen, but with sampling differences that the pass@1                           Top-20. CodeGen also performs well on Scala, Rust, and
rates difficult to compare.                                                                      Julia.
                                                                                                                                                                                                      8

                                                                                                                                pass@1 rates for all languages, with positive coefficients for
                                                                     C++
                                                                       PHP
                                                                                        JavaScript          TypeScript          TypeScript, JavaScript, and PHP.
                              Python

                       Ruby                        Scala             Rust                                                           We note that MBPP, unlike HumanEval, does not include
                 0.4
  Pass@1 rates
                                                                   Java
                                                                                                                                any doctests in the prompts. The observed differences in
                       Go                                                                                                       performance on MultiPL-MBPP and MultiPL-HumanEval in
                                                  C#
                                                                                                                                certain languages may relate to this, as we discuss in more
                 0.2                                                                                                            detail in §6.1.

                                                                                                                                5.2.1   MBPP is Less Challenging Than HumanEval
                 0.0                                                                                                            MBPP appears to be a less challenging benchmark than
                                   1.50




                                                       1.75




                                                                            2.00




                                                                                                     2.25




                                                                                                                         2.50
                                                                                                                                HumanEval. The MultiPL-MBPP pass@1 rate is higher than
                                                              Perplexity                                                        the MultiPL-HumanEval pass@1 rate for all but 6 of our 57
                                          C#                   C++                 Go                       Java                model/language pairs. This is despite the fact that MBPP
                                                                                                                                does not provide doctests in any prompts, which, as we
                       PL                 JavaScript           PHP                 Python                   Ruby
                                                                                                                                show in §6.1, affects performance for some languages.
                                          Rust                 Scala               TypeScript                                       This suggests that HumanEval may be a more use-
                                                                                                                                ful benchmark suite than MBPP for the community, as it
Figure 8: Codex HumanEval pass@1 rates versus perplexity                                                                        provides an equally good or better indication of model
scores reported in [7].                                                                                                         performance with a more computationally efficient sample
                                                                                                                                size.

   Our evaluation therefore shows that contemporary code
                                                                                                                                5.2.2   Python Results and Replication
generation models may be useful even for developers work-
ing with less commonly used programming languages.                                                                              Our Python MBPP pass@1 rates for Codex are slightly
                                                                                                                                higher what is reported in [35] (60.3% compare to 58.1%).
5.1.4 Perplexity and Code Correctness Do Not Correlate                                                                          [35] prompts with a function signature and docstring, even
Xu et al. [7] report Codex perplexity scores for 11 of our 18                                                                   though the original MBPP problems do not include function
languages. We do not observe a strong correlation between                                                                       signatures; we also include function signatures, which we
Codex pass@1 scores and their perplexity scores (Figure 8).                                                                     infer from the provided test cases.
Notably, perplexity is highest for JavaScript and TypeScript,                                                                       Our Python MBPP results for InCoder are lower than
while we find that Codex performs best on these languages.                                                                      what is reported in the original paper (15.5% compared to
Therefore, perplexity may not be a reliable evaluation metric                                                                   19.4%) [4]. We calculated pass@1 rates for MBPP differently
for NL2Code. One caveat is that [7] likely evaluate an older                                                                    than Fried et al. [4] in two key ways. First, since the original
Codex model, since they report substantially lower pass                                                                         MBPP benchmarks do not include function signatures, Fried
rates for Python.                                                                                                               et al. [4] prompts InCoder with the MBPP docstring only.
                                                                                                                                We infer function signatures for MBPP problems from the
                                                                                                                                provided test cases, as described in §3. Second, Fried et al.
5.2              MultiPL-MBPP results
                                                                                                                                [4] reports computing pass@1 rates for MBPP using a single
Figure 6 shows the by-language performance for Codex,                                                                           completion, rather than computing the unbiased sampling
CodeGen, and InCoder on our translated version of                                                                               estimator with 200 samples as described in Chen et al. [1],
the MBPP benchmark, MultiPL-MBPP. Codex performs                                                                                as we do. We suspect this leads to inflated pass@1 rates.9
strongest on the Python problems, but, as with MultiPL-
HumanEval, does well on several other languages, includ-
                                                                                                                                5.2.3   Performance by Language Frequency
ing JavaScript. A mixed-effects model finds significant dif-
ferences in Codex pass@1 rates between Python and all                                                                           Figure 9 shows model performance on MultiPL-MBPP
other languages in MultiPL-MBPP.                                                                                                by language frequency. As with the MultiPL-HumanEval
    As with MultiPL-HumanEval, CodeGen performs best                                                                            benchmark, models generally perform better on more com-
on the MultiPL-MBPP languages included in its fine-tuning                                                                       mon languages. However, Codex performance on MultiPL-
set: Python, JavaScript, C++, Java, and Go. It performs al-                                                                     MBPP is robust on many M EDIUM, L OW, and N ICHE lan-
most as well on TypeScript as on JavaScript. A mixed-effects                                                                    guages, such as Lua and Scala. CodeGen performs surpris-
model finds significant differences in CodeGen pass@1 rates                                                                     ingly well on the D version of MBPP, a niche language not
between Python and all languages except Ruby, where per-                                                                        included in its fine-tuning dataset.
formance is so low that the model fails to find a reliable                                                                          We find reliable differences in Codex pass@1 rates be-
estimate.                                                                                                                       tween languages in the M EDIUM, L OW, and N ICHE cate-
    Unlike with MultiPL-HumanEval, on MultiPL-MBPP,                                                                             gories when compared to the H IGH category (p = 0.007;
InCoder’s performance on TypeScript, JavaScript, and PHP                                                                        p < 0.001; p < 0.001).
actually exceeds its performance on Python. InCoder’s
Python pass@1 rate is similar on MultiPL-HumanEval and                                                                            9. With a single sample, the pass@1 rate for an individual problem
MultiPL-MBPP, one of the few instances where MBPP per-                                                                          will be 0% or 100%. Assuming that the 200 samples are fairly homoge-
                                                                                                                                neous but not identical, as we observe is usually the case, the unbiased
formance is not considerably better than HumanEval. A                                                                           sampling pass@1 rate for an individual problem is rarely 100%, since
mixed-effects model finds significant differences in InCoder                                                                    this would require all 200 samples to be correct.
                                                                                                                                                                                     9


                                              High                               Medium                                  Low                                  Niche
               0.8



               0.6
Pass@1 rates




               0.4



               0.2



               0.0
                        Python

                                 JavaScript

                                               C++

                                                     Java

                                                            TypeScript



                                                                         PHP


                                                                                 Ruby


                                                                                        C#


                                                                                               Go



                                                                                                              Perl

                                                                                                                     R

                                                                                                                          Rust

                                                                                                                                 Scala

                                                                                                                                         Swift


                                                                                                                                                 Bash

                                                                                                                                                        Lua

                                                                                                                                                                Racket

                                                                                                                                                                         D

                                                                                                                                                                             Julia
                                                                                             Language
                                                                               Model      InCoder         CodeGen            Codex


Figure 9: Model performance on MultiPL-MBPP by language frequency and type-checking. Languages to the left of dashed
line are untyped; languages to the right are typed.


5.3                Summary                                                                                •      Full Translation: translates unit tests, doctests, and
On the whole, our results replicate previously reported                                                          Python-terminology in the prompt; and
model performance on code generation for Python. We                                                       •      No Doctests: removes doctests and does not translate
benchmark three state-of-the-art models on 18 additional                                                         natural language terminology.
languages, most of which have never been evaluated before.
                                                                                                    For Codex’s pass@1 results, translating doctests and Python-
Surprisingly, we find remarkably good model performance
                                                                                                    specific terminology has little impact on better-performing
on some lower-frequency languages, such as Lua. We also
                                                                                                    languages (Figure 10). However, translating these compo-
find that performance on JavaScript and TypeScript is con-
                                                                                                    nents seems more important for certain languages: Bash,
sistently high and occasionally exceeds Python, even though
                                                                                                    PHP, Perl, R, Rust, Swift, and TypeScript.
the benchmarks we explore originated in Python.
                                                                                                       We note that six of these languages are ones where
                                                                                                    Codex does not perform substantially better on MultiPL-
6              FACTORS IN C ODE G ENERATION S UCCESS                                                MBPP than MultiPL-HumanEval (Figure 6). The perfor-
In this section, we explore factors that impact code gen-                                           mance degradation observed for these languages when
eration success. Focusing specifically on the MultiPL-                                              doctests are removed from the MultiPL-HumanEval prob-
HumanEval benchmark suite, we report results from a num-                                            lems suggests that the worse than expected performance on
ber of follow-up experiments, including an ablation study                                           MultiPL-MBPP could be due to the lack of doctests in that
of MultiPL-E’s translation components and finer-grained                                             benchmark suite.
examinations of language features and prompt translation                                               Overall, we find significant differences between the Full
choices. We also provide a fine-grained analysis of the kinds                                       Translation and Test-Only Translation experiments (p =
of errors that arise in NL2Code across several languages.                                           0.03), and between No Doctests and Test-Only Translation
                                                                                                    (p < 0.001), but not between No Translation and Test-
                                                                                                    Only Translation (p = 0.2). This suggests that the Python
6.1                Ablation Study
                                                                                                    terminology translation has a small but reliable effect, and
Our compilers target multiple distinct regions of the prompt                                        that the presence of the doctests is important, though their
for each problem. We explore the impact of each component                                           translation is not.
in an ablation study of our MultiPL-HumanEval benchmark
suite with Codex. We ran four versions of the MultiPL-
HumanEval prompts, with some or all regions translated:                                             6.2       Type Annotations
               •     Original Prompt: does not translate doctests or nat-                           One may conjecture that type annotations improve model
                     ural language terminology (e.g. prompts as in Hu-                              performance by constraining the code generation search
                     manEval);                                                                      space. Or, perhaps, they might hurt performance by compli-
               •     Test-only Translation: translates doctests but not                             cating the task, since the model must generate correct type
                     Python-specific terminology;                                                   annotations.
                                                                                                                                                                                       10


                                                                                                Codex
                      0.6
Average pass@1 rate




                      0.4




                      0.2




                      0.0
                                C++

                                      C#

                                            D

                                                  Go

                                                        Java

                                                               Julia

                                                                       JavaScript

                                                                                    Lua

                                                                                          PHP

                                                                                                  Perl

                                                                                                           Python

                                                                                                                      R

                                                                                                                            Ruby

                                                                                                                                   Racket

                                                                                                                                            Rust

                                                                                                                                                   Scala

                                                                                                                                                           Bash

                                                                                                                                                                  Swift

                                                                                                                                                                          TypeScript
                                                                                          Language
                                                                                    Original Prompt                 Test−Only Translation
                                                       Experiment
                                                                                    Full Translation                No Doctests

Figure 10: Ablation study of translation components, showing Codex pass@1 with original prompts; translated doctests;
translated text and doctests; and doctests removed.


    In Figure 7 and Figure 9, the dashed lines in each                                          significant difference in pass@1 rates (p = 0.14), suggesting
category separate languages with type annotations (left)                                        that typed programs are rejected for genuine errors.
from languages without (right). We observe no overall effect
of type annotations on Codex pass@1 rates on MultiPL-                                           6.2.3 Type annotations do not affect Python performance
HumanEval (p = 0.33) or MultiPL-MBPP (p = 0.23).                                                We run a similar experiment with Codex and Python, where
    To explore the impact of type annotations at a more                                         we remove all the type annotations from the MultiPL-
fine-grained level, we run a series of follow-up experiments                                    HumanEval prompts. We find that this has no significant
using the MultiPL-HumanEval benchmark suite. We focus                                           effect on Codex’s pass@1 rate for Python (p = 0.23).
on two languages: Python, which allows optional type
annotations, and TypeScript, a gradually typed cousin of
JavaScript. Gradual typing allows us to weaken type anno-                                       We interpret these results as evidence that type annotations
tations or even configure the TypeScript compiler to ignore                                     do not guide search in general, since they do not improve
all type errors.                                                                                Python performance, but that informative types are neces-
                                                                                                sary for languages where type annotations are standard,
6.2.1                       Precise types improve TypeScript performance                        perhaps in order to fit the token distribution of high-quality
TypeScript has an “Any” type, which is compatible with                                          typed code seen in training.
all types. We run Codex on a variation of the MultiPL-
HumanEval TypeScript prompts where all types in the                                             6.3      Sensitivity to Compilation Choices
function signature are translated to “Any”. We find that                                        Each MultiPL-E compiler makes small choices about how
the loss of precise types hurts performance on TypeScript                                       to translate prompts that could have an impact on perfor-
(-2.5%; p < 0.001).                                                                             mance. We explore some of these choices below.

6.2.2                       TypeScript type errors correlate with runtime errors                6.3.1 Comment style affects performance
Even gradual type-checking can reject programs that would                                       Most programming languages have several comment styles
in fact run without error. We run the Codex-generated Type-                                     (e.g., single-line vs. multi-line). To investigate their im-
Script programs without first checking types. We observe no                                     pact, we ran follow-up experiments with Codex on the
                                                                                                                                                                                         11

                                                                                                         Booleans
                                  0.4
                                  0.3
                                  0.2
                                  0.1
                                  0.0
                                                                                                  Dictionaries
                                  0.4
                                  0.3
                                  0.2
                                  0.1
            Average pass@1 rate


                                  0.0
                                                                                                           Lists
                                  0.4
                                  0.3
                                  0.2
                                  0.1
                                  0.0
                                                                                                          Tuples
                                  0.4
                                  0.3
                                  0.2
                                  0.1
                                  0.0
                                                                                           Basic Types Only
                                  0.4
                                  0.3
                                  0.2
                                  0.1
                                  0.0
                                        Python


                                                 Bash


                                                        C++


                                                              C#


                                                                   D


                                                                       Go


                                                                            Java


                                                                                   Julia


                                                                                            JavaScript


                                                                                                             Lua


                                                                                                                    Perl


                                                                                                                           PHP


                                                                                                                                 R


                                                                                                                                     Ruby


                                                                                                                                            Racket


                                                                                                                                                     Rust


                                                                                                                                                            Scala


                                                                                                                                                                    Swift


                                                                                                                                                                            TypeScript
                                                                                                 Language

            Figure 11: Impact of programming language features on Codex pass@1 performance by language


MultiPL-HumanEval benchmark suite for two languages:                                                        a straightforward equivalent in all programming languages
PHP (M EDIUM) and Racket (N ICHE).                                                                          in our dataset.
    Our original prompts use single-line comments for both                                                      To explore whether model success is impacted by the
PHP and Racket, following conventional style. We re-ran                                                     Python language features used in the program, we catego-
Codex on versions of the MultiPL-HumanEval problems                                                         rized all problems from the HumanEval benchmark suite
for both languages using multi-line comments instead. This                                                  into groups based on the Python language features used in
improves the pass@1 rate for Racket (+1.9%, p < 0.001), but                                                 their type annotations: Booleans, dictionaries, lists, tuples,
decreases it for PHP (-3.1% , p = 0.001).                                                                   or none of the above.
                                                                                                                Figure 11 shows the performance by language on each
6.3.2 Naming arguments improves performance for Perl                                                        type of problem. A mixed-effects model finds no significant
Functions in Perl do not have formal named arguments.                                                       effect of problem type, when programming language is
Instead, all arguments are passed in a special array. Our                                                   treated as a random effect.
compiler to Perl produces a prompt that pops elements off                                                       Many languages appear to struggle with questions in-
the special array and names them, with the expectation that                                                 volving tuples. Some of these are languages that lack a na-
this would improve model performance.                                                                       tive tuple type, such as Java. However, JavaScript performs
    We ran a follow-up experiment on a version of the                                                       well despite lacking tuples.
MultiPL-HumanEval problems for Perl where we omit this                                                          Although many languages show poor performance on
argument-naming prompt, so the model has to infer every-                                                    dictionary problems, there are only 3 problems in this cate-
thing about arguments from the natural language descrip-                                                    gory, so these results should be interpreted with caution.
tion and examples. This significantly lowers Codex’s pass@1
rate (-8%; p < 0.001).                                                                                      6.5     Fine-grained Error Analysis
                                                                                                            Code generation models generate many more failing
                                                                                                            programs—programs that produce errors or fail to pass
In summary, our results show that code generation perfor-
                                                                                                            unit tests—than programs which run successfully. This
mance can be sensitive to prompt engineering choices for
                                                                                                            section presents a detailed evaluation of errors present in
both high and low frequency languages.
                                                                                                            the Codex-generated completions for MultiPL-HumanEval
                                                                                                            problems in 4 languages: Python, C#, Swift, and Racket. See
6.4   Impact of Language Features                                                                           Appendix D for a full categorization.
One challenge of extending existing benchmarks to new                                                          We first identified specific error labels for each lan-
programming languages is that not all programming lan-                                                      guage and then grouped them into themes (e.g. “NullRef-
guages have the same features. Although the MBPP and Hu-                                                    erence”). We produced five general error categories: R UN -
manEval benchmarks consist of relatively simple functions,                                                  TIME , S TATIC , T YPE , L ANGUAGE , and M ODEL . We group
they exercise a variety of datatypes, not all of which have                                                 similar error sources together across languages, even if they
                                                                                                                                  12

occur in different contexts: for example, calling a function      languages.10 However, in a practical deployment of a multi-
with a value of the wrong type may fail at compile-time or        language code generation model, it may not be feasible to
run-time, depending on the language’s type system.                adjust the sampler for every input language.
    The most common S TATIC theme across all languages
is “UndefinedIdentifier”, which contains errors related to
referencing non-existent terms. These errors can be caused        8   R ELATED W ORK
in many ways – calls to functions not in the local context, use   In this section we focus on related work on evaluating
of Python-like keywords, or calls to methods from external        neural code generation models.
libraries that were not imported.                                     Early approaches. Early work on neural network code
    Some errors in the R UNTIME category mimic those we           generation relied on textual similarity metrics for evalua-
expect from software engineers (e.g., index-out-of-range er-      tion. For instance, Feng et al. [17] evaluate their CodeBERT
rors). However, others are unlike human mistakes. Notable         model on six programming languages using BLEU [36]. Ren
themes in the latter group (M ODEL) include generating            et al. [27] proposes a code generation-specific formulation of
code that throws exceptions on purpose and generating             this metric. However, previous work has found that textual
code in an entirely different language. For instance, Codex       similarity metrics correlate only weakly with code correct-
frequently generates Markdown code for Racket problems.           ness [1, 2, 27], highlighting the importance of benchmark
Although we don’t have access to the Codex dataset, we            suites with unit tests.
suspect that Racket is not well-represented in the dataset.           Other benchmark formats. The benchmarks that we
We posit that these errors occur because Racket files begin       translate pair code with comments; some other benchmarks
with a language declaration (#lang racket) that is easily         pair natural language descriptions of other kinds. For in-
mistaken for a Markdown heading.                                  stance, the CoNaLa [11] benchmark consists of matching
    Finally, the category L ANGUAGE includes multiple             natural language questions and code snippets mined from
themes related to the specifics of the target language itself.    StackOverflow. We note that MCoNaLA [37], which extends
The “LanguageSpecific” theme contains idiosyncratic errors        CoNaLa to Spanish, Japanese, and Russian, is the only cur-
such as the requirement of labeled arguments in Swift.            rently available benchmark for evaluating code generation
“DoesNotKnowSyntax” includes errors in Racket caused by           from multiple natural languages.
incorrectly generated core language constructs.                       Other monolingual benchmarks. There are monolingual
                                                                  code generation benchmarks in languages beyond Python.
                                                                  Kulal et al. [9] presents a C++ dataset consisting of crowd-
                                                                  sourced descriptions of lines of code. Iyer et al. [38] present a
7   T HREATS TO VALIDITY
                                                                  Java benchmark taken from online code repositories. Zhong
Our work translates two Python code generation bench-             et al. [29] and Yu et al. [39] propose benchmarks for SQL.
marks into 18 other languages and evaluates the perfor-           However, we do not believe SQL is amenable to translation,
mance of three code generation models on the translated           since conventional types in programming languages do not
benchmarks.                                                       naturally translate to the types of relational tables. More-
     The principal threat to validity is that the (translated)    over, of these datasets, only Kulal et al.’s includes unit tests
benchmarks may not be representative of the kinds of prob-        to enable evaluation of code correctness [9].
lems that programmers typically solve in each languages.              Our approach could be applied to other Python code
For example, we evaluate both scripting languages (e.g.,          generation benchmark suites like MathQA-Python [2], a
Python and JavaScript) and systems languages (e.g., C++           set of mathematical word problems with multiple choice
and Rust) on the same task, but programmers frequently            answers, or APPS [10], a set of problems taken from open-
use these languages for very different tasks. We characterize     access code competition websites like Codeforces.
the HumanEval and MBPP benchmarks as a mix of ba-                     Other tasks. Although we focus specifically on bench-
sic programming problems and straightforward interview            marks for the code generation task, there are many other
questions. Thus, performance on benchmarks may not ac-            tasks that have been used to evaluate code generation
curately represent real-world performance.                        models, including generating unit tests from code [19], code
                                                                  search [17, 21], and type inference [22, 23, 24]. Lu et al.
     Code generation models are sensitive to small changes in
                                                                  [20] propose a suite of evaluation datasets for ten tasks,
how prompts are designed, as we show in our exploration
                                                                  including code translation, docstring generation, and code
of prompt design choices for three of our languages (§6.3).
                                                                  summarization.
It is likely that the pass rate on individual languages could
be improved with even more language-specific effort. We do            Other code generation models. We evaluate three state-
provide an ablation study on prompts for all languages in         of-the-art code generation models, but many other models
our dataset (§6.1) to investigate the impact of our different     that have been proposed. Two influential early models were
translation components.                                           CodeBERT [17] and PyMT [18]. More recent models include
                                                                  PolyCoder [7], CodeParrot [40], AlphaCode [41], and PaLM-
     The quality of generated code is also sensitive to de-
                                                                  Coder [42]. PolyCoder was not trained on natural language
cisions about how to sample completions (§2.2). We use
                                                                  text, and its authors explicitly state that it may not be
the same sampling configuration that is used in most prior
work on code generation. Empirical results show these
                                                                    10. This would be a very resource-intensive experiment, beyond
settings are optimal for Python [1], but it is possible that      the scope of an academic group. The original experiment on sampler
different settings would be better for other programming          configurations by Chen et al. [1] has not been repeated by any lab.
                                                                                                                                 13

suitable for NL2Code. AlphaCode and PaLM-Coder are not             of programming languages, performing similarly to Python
available for academic researchers to investigate.                 on several languages, most notably, JavaScript.
    Other multi-language evaluation. Xu et al. [7] measure             In our detailed by-language analysis, we find a pre-
the performance of several code generation models on 12            dictable effect of language frequency, but draw mixed con-
languages. However, they evaluate model performance us-            clusions about the impact of type annotations. Our de-
ing perplexity, rather than building a benchmark with unit         tailed error analysis highlights common patterns in four
tests, as we do; they test code correctness only for Python.       languages, finding model errors that are both like and unlike
    HumanEval-X11 is an unpublished benchmark that                 those of human programmers. We hope that our in-depth,
appeared after our work that manually translates the               parallel evaluation of a large set of languages will be a useful
HumanEval problems into four languages (C++, Java,                 guide for developers weighing whether the utility of code
JavaScript, and Go). Our compiler-based approach has the           generation tools in their project context.
advantage of easy scalability: we support 18 languages and             Our publicly available benchmark is also easy to extend
both HumanEval and MBPP.                                           to new problems and languages. We hope it will help
    MBXP [43] is a concurrenteffort by Amazon Research             evaluate and develop future work on multi-language code
to evaluate code generation models. We support more lan-           generation models.
guages (13 vs. 19), though MBXP translates an additional
benchmark (MathQA). Both MBXP and our work could
be extended to support more languages and benchmarks.
                                                                   10     ACKNOWLEDGMENTS
However, there are deeper differences in the nature of our         We thank Steven Holtzen and Joydeep Biswas for loaning
translation and evaluation:                                        us their GPUs. We thank Northeastern Research Computing
                                                                   for technical support, especially Greg Shlomo. This work
     •   We believe our approach to testing is more reliable.      was partially supported by the National Science Foundation
         Rather than keeping the unit tests hidden from the        grant CCF-2052696.
         model, MBXP prompts the model with the same unit
         tests it uses to test the generated code. Thus the code
         generation model can “see” the test cases that it will    R EFERENCES
         be evaluated on. In contrast, we use a hidden set of      [1]   M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. d. O.
         unit tests to evaluate code correctness.                        Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph,
     •   Our work is more faithful in translating types                  G. Brockman et al., “Evaluating large language models
         from Python into typed languages. For example,                  trained on code,” arXiv preprint arXiv:2107.03374, 2021.
         our type inference infers types like Either[X,Y]          [2]   J. Austin, A. Odena, M. Nye, M. Bosma,
         and Optional[X] and translates them to algebraic                H. Michalewski, D. Dohan, E. Jiang, C. Cai,
         datatypes in typed languages (§6.2). MBXP produces              M. Terry, Q. Le, and C. Sutton, “Program
         types such as Object and Any in languages like Java             synthesis with large language models,” arXiv
         and Scala, which are less idiomatic. For languages              preprint arXiv:2108.07732, 2021. [Online]. Available:
         that do not support Any, such as C++, MBXP fail to              https://arxiv.org/abs/2108.07732
         translate these benchmarks altogether.                    [3]   E. Nijkamp, B. Pang, H. Hayashi, L. Tu, H. Wang,
     •   MBXP uses greedy decoding in their evaluation of                Y. Zhou, S. Savarese, and C. Xiong, “Codegen: An
         public models. Greedy decoding produces a single                open large language model for code with multi-
         candidate program which may not be the most likely              turn program synthesis,” 2022. [Online]. Available:
         program. Prior work has shown that sampling the                 https://arxiv.org/abs/2203.13474
         output of a code generation model significantly im-       [4]   D. Fried, A. Aghajanyan, J. Lin, S. Wang, E. Wallace,
         proves the correctness of generated code [1]. We                F. Shi, R. Zhong, W.-t. Yih, L. Zettlemoyer, and
         follow standard practices for sampling (§2.2).                  M. Lewis, “Incoder: A generative model for code
                                                                         infilling and synthesis,” arXiv preprint arXiv:2204.05999,
                                                                         2022. [Online]. Available: https://arxiv.org/abs/2204.
9     C ONCLUSION                                                        05999
We propose MultiPL-E, the first massively parallel, multi-         [5]   S. Black, S. Biderman, E. Hallahan, Q. Anthony, L. Gao,
language benchmark for natural-language-to-code gener-                   L. Golding, H. He, C. Leahy, K. McDonell, J. Phang,
ation. We write compilers to translate code generation                   M. Pieler, U. S. Prashanth, S. Purohit, L. Reynolds,
benchmarks from Python to 18 additional programming                      J. Tow, B. Wang, and S. Weinbach, “Gpt-neox-20b: An
languages that span a spectrum of language features and                  open-source autoregressive language model,” arXiv
popularity.                                                              preprint arXiv:2204.06745, 2022. [Online]. Available:
    We translate two widely used unit test-driven bench-                 https://arxiv.org/abs/2204.06745
marks for code generation: HumanEval and MBPP. Using               [6]   E. Nijkamp, B. Pang, H. Hayashi, L. Tu, H. Wang,
our multi-language parallel versions, we present the first               Y. Zhou, S. Savarese, and C. Xiong, “A conversational
multi-language code correctness evaluation of three state-of-            paradigm for program synthesis,” arXiv preprint
the-art models: Codex, CodeGen, and InCoder. We demon-                   arXiv:2203.13474, 2022. [Online]. Available: https:
strate that Codex displays high performance across a variety             //arxiv.org/abs/2203.13474
                                                                   [7]   F. F. Xu, U. Alon, G. Neubig, and V. J. Hellendoorn,
    11. http://keg.cs.tsinghua.edu.cn/codegeex                           “A systematic evaluation of large language models of
                                                                                                                              14

     code,” in Proceedings of the 6th ACM SIGPLAN Inter-              Methods in Natural Language Processing (EMNLP).
     national Symposium on Machine Programming, 2022, pp.             Online: Association for Computational Linguistics,
     1–10.                                                            Nov. 2020, pp. 9052–9065. [Online]. Available: https:
[8] A. Ziegler, E. Kalliamvakou, X. A. Li, A. Rice, D. Rifkin,        //aclanthology.org/2020.emnlp-main.728
     S. Simister, G. Sittampalam, and E. Aftandilian, “Pro-      [19] M. Tufano, D. Drain, A. Svyatkovskiy, S. K. Deng,
     ductivity assessment of neural code completion,” in              and N. Sundaresan, “Unit test case generation
     Proceedings of the 6th ACM SIGPLAN International Sym-            with transformers and focal context,” arXiv preprint
     posium on Machine Programming, 2022, pp. 21–29.                  arXiv:2009.10297, 2020. [Online]. Available: https:
[9] S. Kulal, P. Pasupat, K. Chandra, M. Lee,                         //arxiv.org/abs/2009.05617
     O. Padon, A. Aiken, and P. S. Liang, “Spoc:                 [20] S. Lu, D. Guo, S. Ren, J. Huang, A. Svyatkovskiy,
     Search-based pseudocode to code,” in Advances in                 A. Blanco, C. Clement, D. Drain, D. Jiang, D. Tang,
     Neural Information Processing Systems, H. Wallach,               G. Li, L. Zhou, L. Shou, L. Zhou, M. Tufano,
     H. Larochelle, A. Beygelzimer, F. d'Alché-                       M. Gong, M. Zhou, N. Duan, N. Sundaresan, S. K.
     Buc, E. Fox, and R. Garnett, Eds., vol. 32.                      Deng, S. Fu, and S. Liu, “Codexglue: A machine
     Curran Associates, Inc., 2019. [Online]. Avail-                  learning benchmark dataset for code understanding
     able:     https://proceedings.neurips.cc/paper/2019/             and generation,” arXiv preprint arXiv:2102.04664, 2021.
     file/7298332f04ac004a0ca44cc69ecf6f6b-Paper.pdf                  [Online]. Available: https://arxiv.org/abs/2102.04664
[10] D. Hendrycks, S. Basart, S. Kadavath, M. Mazeika,           [21] T. Ahmed and P. Devanbu, “Multilingual training for
     A. Arora, E. Guo, C. Burns, S. Puranik, H. He,                   software engineering,” in Proceedings of the 44th Interna-
     D. Song, and J. Steinhardt, “Measuring coding                    tional Conference on Software Engineering. ACM, 2022.
     challenge competence with apps,” arXiv preprint             [22] J. Wei, M. Goyal, G. Durrett, and I. Dillig, “LambdaNet:
     arXiv:2105.09938, 2021. [Online]. Available: https:              Probabilistic Type Inference using Graph Neural Net-
     //arxiv.org/abs/2105.09938                                       works,” in International Conference on Learning Represen-
[11] P. Yin, B. Deng, E. Chen, B. Vasilescu, and G. Neubig,           tations (ICLR), 2020.
     “Learning to mine aligned code and natural language         [23] V. J. Hellendoorn, C. Bird, E. T. Barr, and M. Allamanis,
     pairs from stack overflow,” in Proceedings of the 15th           “Deep Learning Type Inference,” in Fse, 2018.
     International Conference on Mining Software Repositories,   [24] M. Pradel, G. Gousios, J. Liu, and S. Chandra, “Type-
     ser. MSR ’18. New York, NY, USA: Association for                 Writer: Neural Type Prediction with Search-Based Val-
     Computing Machinery, 2018, p. 476–486. [Online].                 idation,” in Esecfse, 2020.
     Available: https://doi.org/10.1145/3196398.3196408          [25] I. Drori, S. Zhang, R. Shuttleworth, L. Tang, A. Lu,
[12] R. Alur, R. Bodik, G. Juniwal, M. Martin,                        E. Ke, K. Liu, L. Chen, S. Tran, N. Cheng, R. Wang,
     M. Raghothaman, S. A. Seshia, R. Singh, A. Solar-                N. Singh, T. L. Patti, J. Lynch, A. Shporer, N. Verma,
     Lezama, E. Torlak, and A. Udupa, “Syntax-guided                  E. Wu, and G. Strang, “A neural network solves, ex-
     synthesis,” in Formal Methods in Computer-Aided Design           plains, and generates university math problems by
     (FMCAD), 2013.                                                   program synthesis and few-shot learning at human
[13] S. Chaudhuri, K. Ellis, O. Polozov, R. Singh, A. Solar-          level,” Proceedings of the National Academy of Sciences,
     Lezama, and Y. Yue, “Neurosymbolic Programming,”                 vol. 119, no. 32, p. e2123433119, Aug. 2022.
     Foundations and Trends in Programming Languages, vol. 7,    [26] A. Holtzman, J. Buys, L. Du, M. Forbes, and Y. Choi,
     no. 3, pp. 158–243, 2021.                                        “The curious case of neural text degeneration,” in ICLR,
[14] S. Gulwani, O. Polozov, R. Singh et al., “Program syn-           2020.
     thesis,” Foundations and Trends® in Programming Lan-        [27] S. Ren, D. Guo, S. Lu, L. Zhou, S. Liu, D. Tang,
     guages, vol. 4, no. 1-2, pp. 1–119, 2017.                        N. Sundaresan, M. Zhou, A. Blanco, and S. Ma,
[15] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Ka-               “Codebleu: a method for automatic evaluation of
     plan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry,          code synthesis,” 2020. [Online]. Available: https:
     A. Askell et al., “Language models are few-shot learn-           //arxiv.org/abs/2009.10297
     ers,” Advances in neural information processing systems,    [28] T. Yu, R. Zhang, K. Yang, M. Yasunaga, D. Wang,
     vol. 33, pp. 1877–1901, 2020.                                    Z. Li, J. Ma, I. Li, Q. Yao, S. Roman, Z. Zhang, and
[16] B. Wang and A. Komatsuzaki, “Gpt-j-6b: A 6 billion               D. Radev, “Spider: A large-scale human-labeled dataset
     parameter autoregressive language model,” 2021.                  for complex and cross-domain semantic parsing and
     [Online]. Available: https://github.com/kingoflolz/              text-to-SQL task,” in Proceedings of the 2018 Conference
     mesh-transformer-jax                                             on Empirical Methods in Natural Language Processing.
[17] Z. Feng, D. Guo, D. Tang, N. Duan, X. Feng,                      Brussels, Belgium: Association for Computational
     M. Gong, L. Shou, B. Qin, T. Liu, D. Jiang,                      Linguistics, Oct.-Nov. 2018, pp. 3911–3921. [Online].
     and M. Zhou, “Codebert: A pre-trained model                      Available: https://aclanthology.org/D18-1425
     for programming and natural languages,” arXiv               [29] V. Zhong, C. Xiong, and R. Socher, “Seq2sql: Generating
     preprint arXiv:2002.08155, 2020. [Online]. Available:            structured queries from natural language using
     https://arxiv.org/abs/2002.08155                                 reinforcement learning,” 2017. [Online]. Available:
[18] C. Clement, D. Drain, J. Timcheck, A. Svyatkovskiy,              https://arxiv.org/abs/1709.00103
     and N. Sundaresan, “PyMT5: multi-mode translation of        [30] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit,
     natural language and python code with transformers,”             L. Jones, A. N. Gomez, L. u. Kaiser, and
     in Proceedings of the 2020 Conference on Empirical               I. Polosukhin, “Attention is all you need,” in
                                                                                                                           15

     Advances in Neural Information Processing Systems,               G. Mishra, A. Roberts, P. Barham, H. W. Chung,
     I. Guyon, U. V. Luxburg, S. Bengio, H. Wallach,                  C. Sutton, S. Gehrmann, P. Schuh, K. Shi,
     R. Fergus, S. Vishwanathan, and R. Garnett, Eds.,                S. Tsvyashchenko, J. Maynez, A. Rao, P. Barnes,
     vol. 30. Curran Associates, Inc., 2017. [Online]. Avail-         Y. Tay, N. Shazeer, V. Prabhakaran, E. Reif, N. Du,
     able:      https://proceedings.neurips.cc/paper/2017/            B. Hutchinson, R. Pope, J. Bradbury, J. Austin,
     file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf                  M. Isard, G. Gur-Ari, P. Yin, T. Duke, A. Levskaya,
[31] A. Aghajanyan, B. Huang, C. Ross, V. Karpukhin,                  S. Ghemawat, S. Dev, H. Michalewski, X. Garcia,
     H. Xu, N. Goyal, D. Okhonko, M. Joshi, G. Ghosh,                 V. Misra, K. Robinson, L. Fedus, D. Zhou, D. Ippolito,
     M. Lewis, and L. Zettlemoyer, “Cm3: A causal                     D. Luan, H. Lim, B. Zoph, A. Spiridonov, R. Sepassi,
     masked multimodal model of the internet,” arXiv                  D. Dohan, S. Agrawal, M. Omernick, A. M. Dai,
     preprint arXiv:2201.07520, 2022. [Online]. Available:            T. S. Pillai, M. Pellat, A. Lewkowycz, E. Moreira,
     https://arxiv.org/abs/2201.07520                                 R. Child, O. Polozov, K. Lee, Z. Zhou, X. Wang,
[32] L. Gao, S. Biderman, S. Black, L. Golding, T. Hoppe,             B. Saeta, M. Diaz, O. Firat, M. Catasta, J. Wei,
     C. Foster, J. Phang, H. He, A. Thite, N. Nabeshima,              K. Meier-Hellstern, D. Eck, J. Dean, S. Petrov,
     S. Presser, and C. Leahy, “The pile: An 800gb dataset            and N. Fiedel, “Palm: Scaling language modeling
     of diverse text for language modeling,” 2021. [Online].          with pathways,” arXiv preprint arXiv:2204.02311, 2022.
     Available: https://arxiv.org/abs/2101.00027                      [Online]. Available: https://arxiv.org/abs/2204.02311
[33] W. Zaremba, G. Brockman, and OpenAI, “Openai                [43] B. Athiwaratkun, S. K. Gouda, Z. Wang, X. Li,
     codex,” 2021. [Online]. Available: https://openai.com/           Y. Tian, M. Tan, W. U. Ahmad, S. Wang, Q. Sun,
     blog/openai-codex/                                               M. Shang, S. K. Gonugondla, H. Ding, V. Kumar,
[34] D. Bates, M. Mächler, B. Bolker, and S. Walker, “Fitting         N. Fulton, A. Farahani, S. Jain, R. Giaquinto, H. Qian,
     linear mixed-effects models using lme4,” Journal of              M. K. Ramanathan, R. Nallapati, B. Ray, P. Bhatia,
     Statistical Software, vol. 67, no. 1, pp. 1–48, 2015.            S. Sengupta, D. Roth, and B. Xiang, “Multi-lingual
[35] B. Chen, F. Zhang, A. Nguyen, D. Zan, Z. Lin,                    evaluation of code generation models,” 2022. [Online].
     J.-G. Lou, and W. Chen, “CodeT: Code generation                  Available: https://arxiv.org/abs/2210.14868
     with generated tests,” 2022. [Online]. Available:           [44] T. Gebru, J. Morgenstern, B. Vecchione, J. W. Vaughan,
     https://arxiv.org/abs/2207.10397                                 H. Wallach, H. D. Iii, and K. Crawford, “Datasheets for
[36] K. Papineni, S. Roukos, T. Ward, and W.-J. Zhu,                  datasets,” Communications of the ACM, vol. 64, no. 12,
     “Bleu: A method for automatic evaluation of                      pp. 86–92, 2021.
     machine translation,” in Proceedings of the 40th Annual
     Meeting on Association for Computational Linguistics,
     ser. ACL ’02. USA: Association for Computational
     Linguistics, 2002, p. 311–318. [Online]. Available:
     https://doi.org/10.3115/1073083.1073135
[37] Z. Wang, G. Cuenca, S. Zhou, F. F. Xu, and G. Neubig,
     “Mconala: A benchmark for code generation from
     multiple natural languages,” 2022. [Online]. Available:
     https://arxiv.org/abs/2203.08388
[38] S. Iyer, I. Konstas, A. Cheung, and L. Zettlemoyer,
     “Mapping language to code in programmatic context,”
     arXiv preprint arXiv:1808.09588, 2018.
[39] T. Yu, R. Zhang, K. Yang, M. Yasunaga, D. Wang,
     Z. Li, J. Ma, I. Li, Q. Yao, S. Roman, Z. Zhang,
     and D. Radev, “Spider: A large-scale human-labeled
     dataset for complex and cross-domain semantic
     parsing and text-to-sql task,” 2018. [Online]. Available:
     https://arxiv.org/abs/1809.08887
[40] L. Tunstall, L. von Werra, and T. Wolf, Natural Language
     Processing with Transformers. O’Reilly Media, 2022.
     [Online]. Available: https://books.google.com/books?
     id=nTxbEAAAQBAJ
[41] Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser,
     R. Leblond, T. Eccles, J. Keeling, F. Gimeno,
     A. D. Lago, T. Hubert, P. Choy, C. d. M.
     d’Autume, I. Babuschkin, X. Chen, P.-S. Huang,
     J. Welbl, S. Gowal, A. Cherepanov, J. Molloy, D. J.
     Mankowitz, E. S. Robson, P. Kohli, N. de Freitas,
     K. Kavukcuoglu, and O. Vinyals, “Competition-level
     code generation with alphacode,” 2022. [Online].
     Available: https://arxiv.org/abs/2203.07814
[42] A. Chowdhery, S. Narang, J. Devlin, M. Bosma,
                                                                                                                                                  16

A PPENDIX A
D ETAILS OF L ANGUAGE T RANSLATIONS

The tables below describe the details of all 18 language translations as well as our Python translation. Technical information
regarding running experiments and evaluating generated programs can be found at github.com/nuprl/MultiPL-E. Here
we address language-specific decisions that are relevant to the prompt translation task. Specifically, we outline the following
details:

   1)   The language version used as a reference for creating the value-to-value translation.
   2)   The stop tokens used for signaling the end of program generation. Across languages these reflect terms that begin
        and/or start code blocks (variations of \n} are common).
   3)   Details about prompt creation. This sections highlight the choice of comments and any necessary preamble
        information (e.g., the opening tag <?php in PHP)
   4)   Information about mapping values and/or types from Python. Notes here describe places where case-by-case
        decisions need to be made, or a language’s limitations required not converting a subset of values and/or types.
        Omitted discussions represents straightforward conversions (e.g., integers in Perl).


 B ASH
 Reference Version for Translation   5.1.16
 Stop Tokens                         ’\n}’
 Prompt Information                  We translate each Python docstring to Bash comments (each line prefixed with #). Each Python function
                                     signature is translated to a Bash function signature, which is of the form function_name(), as Bash
                                     functions do not have explicit parameters. Type annotations are translated to comments in the prompt,
                                     which describe the encoding (or none) for each of the function parameters. The shebang (#!/bin/bash)
                                     was prepended to the prompt.
 Type Translations                   Bash is not a general-purpose programming language, and its many quirks make translation challenging,
                                     particularly for data structures like lists and maps. While Bash has numerically indexed and string-
                                     associative arrays, the shell’s ecosystem typically works with these structures in string-y formats: lists are
                                     typically whitespace separated elements; associative maps are in formats like comma-separated values
                                     (CSV). We use those conventions in our type translations.



 C++
 Reference Version for Translation   C++17 compiled using g++17
 Stop Tokens                         ’\n}’
 Prompt Information                  Each prompt contains C++ single line comments where each line is prefixed with //. Python function
                                     signatures are translated to C++ signatures and we add #include statements.
 Type Translations                   All Python integers are translated to C++ long and Python floats are translated to C++ float. A
                                     Python list is translated to std::vector, a dictionary to std::map, a tuple to std::tuple, a string to
                                     std::string, and Python’s Any type to std::any. A new C++ union type is declared for each union
                                     type annotation in Python.



 C#
 Reference Version for Translation   C# 5 with Mono 6.12
 Stop Tokens                         ’\n         }\n’
 Prompt Information                  The prompt contains a class declaration with the translated method as its public static member
                                     and C# single line comments, where each line is prefixed with //. Adding a member of class also adds
                                     indentation to each line inside class declaration (note the indentation in the stop token). All function and
                                     argument names are converted to C#’s naming convention where the first letter of all words is in capital
                                     case.
 Type Translations                   Most types were translated to their C# direct equivalent (e.g. Python tuple to C# tuple). There are
                                     some exceptions: Python int is translated to a C# long and Python’s Any type annotation is translated
                                     to C# object. Since C# does not support union types, we do not convert Python union annotations.



 D
 Reference Version for Translation   dmd 2.100.0
 Stop Tokens                         ’\n\n’, ’\void’, ’\bool’, ’\int’
 Prompt Information                  The prompt was given as a multi-line comment (/* ... */).
 Type Translations                   Most types in Python have equivalents in D. One exception is Python integers, which we translate
                                     to long. Dictionaries are translated to Nullable of associative arrays, a built-in array that supports
                                     indices of any types. Associative arrays must be non-empty in D, so the Nullable!(...) template
                                     type is needed to wrap around the associative array, i.e. an empty array is denoted as the “null” state.
                                     Tuples are translated to the Tuples!(...) template type; however, the tuple type in D cannot be
                                     variable arity. Union types and Any are not translated.
                                                                                                                                               17
GO
Reference Version for Translation   1.18.1
Stop Tokens                         ’\nfunc ’, ’struct’, ’\n // ’
Prompt Information                  The prompt is translated as a line comment (with //) above the function stub. For short functions, it is
                                    recommended to use single line comments.
Type Translations                   Python Lists and Dictionaries were mapped to Go’s Slices and Maps, respectively. Since Go requires type
                                    annotations, we utilized Python’s type annotations to both translate the candidate function and the tests.
                                    Go requires explicitly declaring types for a compound datatype (e.g., a Python list [1, 2, 3] translates
                                    to []int{1, 2, 3}). Go does not have an equivalent Union, Option, or Tuple data type, but it is
                                    possible to create a non-homogenous slice using []interface – therefore we reject the two former and
                                    we convert the latter.
Other Notes                         We consulted the following style guide as part of our translation to Go (https://go.dev/doc/effective_
                                    go).




J AVA
Reference Version for Translation   OpenJDK 17
Stop Tokens                         ’\n           }\n’
Prompt Information                  The prompt contains a class declaration with the translated method as its public static member and
                                    Java single line comments, where each line is prefixed with //. Adding a member of class also adds
                                    indentation to each line inside class declaration (note in the intention in the stop token). All function
                                    and arguments are converted to Java’s naming convention where the first letter is lowercase and the first
                                    letter of all other words are capitalized.
Type Translations                   The type translation from Python to Java is performed by translating a Python int to a Java long, Python
                                    float to Java float, a Python list to Vector, a dictionary to HashMap, a string to String, and
                                    Python’s Any type annotation to Object. Since OpenJDK does not support tuples, we use javatuples
                                    library and translates Python tuples to javatuples.Tuple. Since Java does not support union types,
                                    we do not convert Python union annotations.




J AVA S CRIPT
Reference Version for Translation   18.6
Stop Tokens                         ’\nfunction ’, ’\n /*’, ’\n //’, ’\nconsole .log’
Prompt Information                  We convert the Python prompt into a block of comments using //.
Type Translations                   Most type translations are direct. Python lists and tuples were translated into JS arrays. Dictionaries were
                                    translated into objects.




J ULIA
Reference Version for Translation   1.7.3
Stop Tokens                         ’\nfunction ’, ’\nmacro ’, ’\n \n ’
Prompt Information                  Julia shares both its documentation and line comment syntax with Python, and thus the prompt is left
                                    unchanged by the translation.
Type Translations                   We translate Python’s int to Int64, float to Float64, and List to Vector. The only coercion
                                    required in the benchmarks come from the fact that Julia generates the type Vector{Any} for the
                                    unannotated empty vector. Thus, if the empty vector is given as an argument to the function, it is coerced
                                    to the expected (more specific) type. Julia has first-class support for Union types; therefore, we represent
                                    Unions directly and Optional<T> as the type Union{T, Nothing}.




L UA
Reference Version for Translation   5.3
Stop Tokens                         ’\nlocal ’, ’\nfunction ’, ’\n -’, ’\n \n ’
Prompt Information                  We convert the Python prompt to a block of single-line comments using --.
Type Translations                   The only data structure in Lua is a table, and tables with integer indices behave like lists. Thus we
                                    translate Python dictionaries, tuples, and lists to tables.




P ERL
Reference Version for Translation   5.34
Stop Tokens                         ’\nsub’, ’\n#’, ’\n\n’
Prompt Information                  We convert the Python prompt to a block of single-line comments, using #.
Type Translations                   We are careful to pass data structures by reference; we translate Python lists and tuples to anonymous
                                    arrays, and dictionaries to anonymous hashes. Perl lacks a Boolean type; we translate True to 1 and
                                    False to the empty string, since these are the values returned by logical operators.
                                                                                                                                             18
PHP
Reference Version for Translation   8.1.2 (cli)
Stop Tokens                         ’\nfunction’, ’\n?>’, ’\n’, ’\n#’
Prompt Information                  In our full translation, the prompt was given as single-line comments, using //, rather than using PHP’s
                                    two other comment styles (single line # and multi-line /* ... */). The PHP opening tag, <?php, was
                                    prepended to the prompt, and the closing tag was omitted, following the recommendation for a file that
                                    only contains PHP code (https://www.php.net/manual/en/language.basic-syntax.phptags.php).
Type Translations                   PHP arrays are actually ordered maps, so Python lists, tuples, and dictionaries were translated to arrays.
                                    Arrays were defined using the default syntax, array(), instead of the shorthand []. Strings are double
                                    quoted, and Python’s None is translated to null.




P YTHON
Reference Version for Translation   3.10
Stop Tokens                         ’\ndef’, ’\n#’, ’\nif’, ’\nclass’
Prompt Information                  The prompt was presented as in the original HumanEval dataset: a multi-line docstring. If type
                                    annotations were present, the typing library was imported via an import statement at the beginning
                                    of the prompt.
Type Translations                   The Python translation is trivial: each type is translated to itself.




R
Reference Version for Translation   4.1
Stop Tokens                         ’\n#’,’\n“‘’
Prompt Information                  We convert the Python prompt to a block of single-line comments using #.
Type Translations                   R vectors are more commonly used than R lists; however, R vectors are restricted to storing homogenous
                                    data types. We translate Python Lists and Tuples to R vectors using the c() function when possible (i.e.,
                                    when the contents are homogenous), and to R lists using the list() function otherwise. We convert
                                    Python dictionaries to named lists. R, like Python, supports both single and double quoted strings.




R ACKET
Reference Version for Translation   8.2
Stop Tokens                         ’\n(define ’, ’\n#|’, ’\n;’, ’\n(’
Prompt Information                  We convert the Python prompt to a block of single-line comments using ’;’.
Type Translations                   We translate Python Lists and Tuples to Racket lists using (list ). We convert Python dictionaries to
                                    hash maps using (hash ). Racket does not support single-quoted strings, so we convert all strings to
                                    double-quoted strings.




R UBY
Reference Version for Translation   3.0.2
Stop Tokens                         ’\nclass’, ’\ndef’, ’\n#’, ’\n\n’
Prompt Information                  Although there are block comments in Ruby (=begin ... =end), they are discouraged by community
                                    style guides. Therefore, the prompt was converted to a block of single-line comments prefixed by #.
Type Translations                   Python Lists and Tuples were mapped to Ruby Arrays with the [...] shorthand per style guides. The
                                    idiomatic => Ruby syntax was used for dictionary creation. While Ruby supports both double- and
                                    single-quoted strings, Python strings were converted to double-quoted Ruby strings as they work with
                                    string interpolation.
Other Notes                         We consulted the following two style guides as part of our translation to Ruby (https://ruby-style-
                                    guide.shopify.dev/, https://github.com/rubocop/ruby-style-guide).




R UST
Reference Version for Translation   1.59.0
Stop Tokens                         ’\n}’
Prompt Information                  A doc comment is used to indicate that the prompt information corresponds to the behavior of the
                                    function and not internal implementation details (each line prefixed with ///). No arguments are
                                    annotated with mut - in all cases (we used owned values) they can be moved to a mutable variable
                                    if necessary, and unnecessary mutable annotations may be confusing.
Type Translations                   All annotated values are owned. While in Rust it sometimes makes sense to accept borrowed values (for
                                    example, if no mutation or move is necessary), it is difficult to infer when this is appropriate from the
                                    Python signature or prompt. Inferring when a borrowed result type could be used would be even more
                                    difficult. Thus, str is translated as String and List is translated to Vec. Tuple is translated to Rust’s
                                    tuple, dict to Rust’s std::collections::HashMap, and Optional to Option. While Python’s int
                                    must support at least 64 bit integers, the more idiomatic isize is used to represent them in Rust.
                                    Python’s float is translated to the corresponding f64 and bool to bool. Problems annotated with a
                                    Union, Any, or Ellipsis are not supported.
                                                                                                                                                 19
 S CALA
 Reference Version for Translation   Scala 2.23
 Stop Tokens                         ’\n       }\n’
 Prompt Information                  The prompt contains a class declaration with the translated method as its member and Scala single line
                                     comments where each line is prefixed with //. Adding a member of class also adds indentation to each
                                     line inside class declaration (note the indentation in the stop token). All function and argument names
                                     are converted Scala’s naming convention where the first letter is lowercase and the first letter of all other
                                     words is in capital case.
 Type Translations                   The type translation from Python to Scala is performed by translating a Python int to a Scala
                                     long, Python float to Scala float, a Python list to Scala List, a Python dictionary to Scala
                                     Dictionary, a Python string to Scala string, a Python tuple to Scala Tuple, and Python’s Any type
                                     annotation to Scala Any. Python union annotations of two types is converted to Scala’s Either type.
                                     Problems with Union of more than two types are not supported.


 S WIFT
 Reference Version for Translation   5.8
 Stop Tokens                         ’\n}’
 Prompt Information                  The prompt is given by doc comments (prepended with ///). For documenting function behavior, doc
                                     comments are preferred over standard comments.
 Type Translations                   Python Lists, Dictionaries and Tuples were mapped to Swift Lists, Dictionaries and Tuples, respectively.
                                     Untyped Python parameters were mapped to AnyHashable in Swift, as opposed to Any, as it allows for
                                     equality comparisons and storage in dictionaries, so is the closest equivalent to untyped Python values.
                                     Optional types or Unions with None in Python were converted to ? optional types in Swift, binary Union
                                     types were converted to Result types, and larger Union types were converted to generated algebraic
                                     datatypes. The generated algebraic datatype definitions (and Error protocol conformance in the case of
                                     Result) were inserted into the prompt, above the doc comments.
 Other Notes                         We consulted the following style guide as part of our translation to Swift (https://www.swift.org/
                                     documentation/api-design-guidelines/).


 T YPE S CRIPT
 Reference Version for Translation   TypeScript compiler version 4.5, Node version 18.6
 Stop Tokens                         ’\nfunction ’, ’\n /*’, ’\n //’, ’\nclass ’
 Prompt Information                  We convert the Python prompt into a block of comments using //.
 Type Translations                   Types are translated by utilizing the annotations provided in our Python tests. Lists and tuples were
                                     translated into arrays. Dictionaries were translated into objects.



A PPENDIX B
DATASHEET
The datasheet below follows the categories proposed in [44]:
    Timnit Gebru, Jamie Morgenstern, Briana Vecchione, Jennifer Wortman Vaughan, Hanna Wallach, Hal Daumé III,
    and Kate Crawford. "Datasheets for datasets." Communications of the ACM, 2021, 86-92.

B.1    Motivation
   •    For what purpose was the dataset created?
        The datasets were originally created to evaluate the performance of code generation models. They were translated
        from Python to other programming languages to extend evaluation to new languages.
   •    Who created the dataset?
        HumanEval was originally created by [1]. MBPP was originally created by [2]. Both datasets were modified by the
        authors of this paper.
   •    Who funded the creation of the dataset? This work was partially supported by the National Science Foundation.

B.2    Composition
   •    What do the instances that comprise the dataset represent?
        The instances of the dataset represent programming problems in 18 programming languages.
   •    How many instances are there in total?
        For MultiPL-HumanEval, there are 3,059 instances (the modified set of 161 Python problems multiplied by 19
        programming languages).
        For MultiPL-MBPP, there are 7,619 instances (the modified set of 401 Python problems multiplied by 19 program-
        ming languages).
   •    Does the dataset contain all possible instances or is it a sample (not necessarily random) of instances from a
        larger set?
        The MultiPL-HumanEval and MultiPL-MBPP are cleaned versions of the original dataset as described in §3.4. The
        MultiPL-HumanEval dataset excludes 3 of the 164 original problems.
                                                                                                                     20

  •    What data does each instance consist of? Each instance is a programming problem with a problem description in
       natural language, a function signature, and unit tests.
  •    Is there a label or target associated with each instance?
       Each instance is numbered and labeled by the name of the function it tests and the language it is written in.
  •    Is the dataset self-contained, or does it link to or otherwise rely on external resources?
       The dataset is self-contained.

B.3   Collection process
  •    How was the data associated with each instance acquired?
       The original Python datasets were manually cleaned. The versions for other programming languages and prompt
       variations were produced by a suite of compilers.
  •    Over what timeframe was the data collected?
       May–October 2022
  •    Were any ethical review processes conducted?
       Not applicable. The dataset adapts a open source dataset released under the terms of the MIT license.

B.4   Preprocessing/cleaning/labeling
  •    Was any preprocessing/cleaning/labeling of the data done?
       We added missing type annotations, formatted examples to use docstrings consistently, and changed random tests
       into unit tests in two problems.
  •    Was the "raw" data saved in addition to the preprocessed/cleaned/labeled data?
       The original data is for both datasets is publicly available.
  •    Is the software that was used to preprocess/clean/label the data available?
       The cleaning process described above was manual.

B.5   Uses
  •    Has the dataset been used for any tasks already?
       The dataset has been used for evaluating the performance of code generation models.
  •    Is there a repository that links to any or all papers or systems that use the dataset?
       https://github.com/nuprl/MultiPL-E
  •    What other tasks could the dataset be used for?
       The dataset could be used to evaluate other LLMs of code, or potentially to improve their performance.

B.6   Distribution
  •    Will the dataset be distributed to third parties outside of the entity?
       Yes.
  •    How will the dataset be distributed?
       The dataset is publicly available at https://github.com/nuprl/MultiPL-E
  •    When will the dataset be distributed?
       Immediately.
  •    Will the dataset be distributed under a copyright or other intellectual property (IP) license, and/or under
       applicable terms of use (ToU)?
       No.
  •    Have any third parties imposed IP-based or other restrictions on the data associated with the instances?
       No.
  •    Do any export controls or other regulatory restrictions apply to the dataset or to individual instances?
       No.

B.7   Maintenance
  •    Who will be supporting/hosting/maintaining the dataset?
       The original authors.
  •    How can the owner/curator/manager of the dataset be contacted?
       See the dataset website.
  •    Is there an erratum?
       No. Any identified and confirmed errors will be acknowledged as part of the repository.
  •    Will the dataset be updated (for example, to correct labeling errors, add new instances, delete instances)?
       Yes.
  •    Will older versions of the dataset continue to be supported/hosted/maintained?
                                                                                                                         21

        Yes.
   •    If others want to extend/augment/build on/contribute to the dataset, is there a mechanism for them to do so?
        Yes, as described in the paper and website.

A PPENDIX C
C OMPLETE S TATISTICAL F INDINGS
We use binomial mixed-effects models fitted with the lme4 library in R for significance testing. A binomial distribution is
appropriate because our outcomes consist of proportions of successes and failures; we use the number of completions (200,
except in rare failure cases) as weights.
    We fit models to the Codex pass@1 completion rates in all experiments reported below. We treat problem number as
a random effect to account for variability inherent to per-problem differences. For comparisons that do not break down
effects by language, we also include language as a random effect. We include random slopes and intercepts for random
effects except where noted.
    Values that are statistically significant with a threshold of p = 0.5 are displayed in bold.

C.1    MultiPL-HumanEval Mixed-Effects Results from §5.1
To quantify the differences in performance among programming languages, a model with a fixed effect of programming
language and random effects for problem number was fitted to the MultiPL-HumanEval Codex pass@1 data.
   Dummy coding was used with Python as the reference level; slopes for each language indicate differences between the
pass@1 rate for Python and that language.
   Table 3 shows the full estimates found by the model.
                                         Fixed effects     βb                z        p
                                         Intercept         -0.48 (+/- 0.4)   -1.1     0.27
                                         Bash              -2.59 (+/- 0.3)   -7.7     < 0.0001
                                         C++               0.10 (+/- 0.4)    0.3      0.77
                                         C#                -4.09 (+/- 0.6)   -7.2     < 0.0001
                                         D                 -4.79 (+/- 0.5)   -9.7     < 0.0001
                                         Go                -2.61 (+/- 0.4)   -6.5     < 0.0001
                                         Java              -1.28 (+/- 0.3)   -3.9     < 0.0001
                                         Julia             -1.91 (+/- 0.4)   -5.2     < 0.0001
                                         JavaScript        -0.27 (+/- 0.3)   -0.8     0.43
                                         Lua               -1.04 (+/- 0.4)   -2.8     0.005
                                         Perl              -2.0 (+/- 0.4)    -5.3     < 0.0001
                                         PHP               -0.30 (+/- 0.4)   -0.8     0.40
                                         R                 -3.69 (+/- 0.4)   -8.5     < 0.0001
                                         Ruby              -0.68 (+/- 0.3)   -2.3     0.024
                                         Racket            -3.78 (+/- 0.4)   -9.8     < 0.0001
                                         Rust              -1.07 (+/- 0.3)   -3.4     < 0.0001
                                         Scala             -0.52 (+/- 0.3)   -1.6     0.10
                                         Swift             -1.8 (+/- 0.3)    -5.7     < 0.0001
                                         TypeScript        -0.27 (+/- 0.3)   -0.9     0.39

                   Table 2: Mixed-effects results for Codex MultiPL-HumanEval language comparison

  A similar model was fit to the CodeGen pass@1 data, but without random slopes, because the very low pass rates for
many problems makes the random effects estimates unstable. Table 3 shows the full estimates found by the model.
                                       Fixed effects     βb                  z         p
                                       Intercept         -3.38 (+/- 0.2)     -18.5     < 0.0001
                                       Bash              -5.66 (+/- 0.04)    -145.8    < 0.0001
                                       C++               -0.21 (+/- 0.01)    -14.6     < 0.0001
                                       C#                -1.74 (+/- 0.02)    -112.7    < 0.0001
                                       D                 -1.72 (+/- 0.02)    -111.6    < 0.0001
                                       Go                -1.0 (+/- 0.01)     -66.7     < 0.0001
                                       Java              -0.14 (+/- 0.01)    -10.2     < 0.0001
                                       Julia             -9.41 (+/- 0.2)     -44.0     < 0.0001
                                       JavaScript        0.12 (+/- 0.01)     8.6       < 0.0001
                                       Lua               -2.43 (+/- 0.02)    -144.8    < 0.0001
                                       Perl              -3.0 (+/- 0.02)     -161.9    < 0.0001
                                       PHP               -1.74 (+/- 0.02)    -112.9    < 0.0001
                                       R                 -2.42 (+/- 0.02)    -114.2    < 0.0001
                                       Ruby              -22.40 (+/- 140)    -0.2      0.87
                                       Racket            -5.51 (+/- 0.04)    -150.4    < 0.0001
                                       Rust              -3.78 (+/- 0.02)    -173.6    < 0.0001
                                       Scala             -3.65 (+/- 0.02)    -172.9    < 0.0001
                                       Swift             -4.08 (+/- 0.02)    -174.0    < 0.0001
                                       TypeScript        -0.04 (+/- 0.01)    -2.7      < 0.0001

                  Table 3: Mixed-effects results for CodeGen MultiPL-HumanEval language comparison
                                                                                                                    22

  A similar model was fit to the InCoder pass@1 data, but without random slopes, because the very low pass rates for
many problems makes the random effects estimates unstable. Table 4 shows the full estimates found by the model.


                                      Fixed effects   βb                 z         p
                                      Intercept       -4.35 (+/- 0.3)    -14.5     < 0.0001
                                      Bash            -3.3 (+/- 0.03)    -131.1    < 0.0001
                                      C++             -0.99 (+/- 0.02)   -57.1     < 0.0001
                                      C#              -1.94 (+/- 0.02)   -100.9    < 0.0001
                                      D               -3.97 (+/- 0.03)   -139.5    < 0.0001
                                      Go              -1.62 (+/- 0.02)   -86.3     < 0.0001
                                      Java            -1.29 (+/- 0.02)   -72.5     < 0.0001
                                      Julia           -4.90 (+/- 0.04)   -132.6    < 0.0001
                                      JavaScript      -0.97 (+/- 0.02)   -56.1     < 0.0001
                                      Lua             -2.21 (+/- 0.02)   -111.2    < 0.0001
                                      Perl            -2.43 (+/- 0.02)   -118.2    < 0.0001
                                      PHP             -1.76 (+/- 0.02)   -93.6     < 0.0001
                                      R               -2.80 (+/- 0.02)   -128.2    < 0.0001
                                      Ruby            -1.87 (+/- 0.02)   -98.4     < 0.0001
                                      Racket          -3.41 (+/- 0.02)   -138.2    < 0.0001
                                      Rust            -2.74 (+/- 0.02)   -125.3    < 0.0001
                                      Scala           -1.92 (+/- 0.02)   -100.3    < 0.0001
                                      Swift           -2.05 (+/- 0.02)   -105.3    < 0.0001
                                      TypeScript      -1.11 (+/- 0.02)   -63.6     < 0.0001

                 Table 4: Mixed-effects results for InCoder MultiPL-HumanEval language comparison




C.2   MultiPL-MBPP Mixed-Effects Results from §5.2


To quantify the differences in performance among programming languages, a model with a fixed effect of programming
language and random effects for problem number was fitted to the Codex pass@1 MultiPL-MBPP data. Dummy coding
was used with Python as the reference level; slopes for each language indicate differences between the pass@1 rate for
Python and that language.
   Table 5 shows the full estimates found by the model.


                                      Fixed effects   βb                 z         p
                                      (Intercept)     0.28 (+/- 0.2)     1.74      0.08
                                      Bash            -2.9 (+/- 0.02)    -193.22   < 0.0001
                                      C++             -1.16 (+/- 0.01)   -82.73    < 0.0001
                                      C#              -1.80 (+/- 0.01)   -126.81   < 0.0001
                                      D               -2.47 (+/- 0.01)   -169.64   < 0.0001
                                      Go              -1.22 (+/- 0.01)   -86.33    < 0.0001
                                      Java            -1.14 (+/- 0.01)   -81.19    < 0.0001
                                      Julia           -1.72 (+/- 0.01)   -121.68   < 0.0001
                                      JavaScript      -0.36 (+/- 0.01)   -24.96    < 0.0001
                                      Lua             -0.94 (+/- 0.01)   -66.54    < 0.0001
                                      Perl            -3.06 (+/- 0.02)   -201.65   < 0.0001
                                      PHP             -1.03 (+/- 0.01)   -72.81    < 0.0001
                                      R               -2.48 (+/- 0.01)   -169.93   < 0.0001
                                      Ruby            -0.85 (+/- 0.01)   -60.10    < 0.0001
                                      Racket          -2.39 (+/- 0.01)   -164.56   < 0.0001
                                      Rust            -1.69 (+/- 0.01)   -119.60   < 0.0001
                                      Scala           -1.20 (+/- 0.01)   -85.31    < 0.0001
                                      Swift           -1.66 (+/- 0.01)   -117.36   < 0.0001
                                      TypeScript      -0.87 (+/- 0.01)   -61.89    < 0.0001

                     Table 5: Mixed-effects results for Codex MultiPL-MBPP language comparison



  A similar model was fit to the CodeGen pass@1 MultiPL-MBPP data. Table 6 shows the full estimates found by the
model.
                                                                                                                  23

                                     Fixed effects     βb                    z          p
                                     (Intercept)       -2.85 (+/- 0.2)       -13.9      < 0.0001
                                     Bash              -5.74 (+/- 0.04)      -129.1     < 0.0001
                                     C++               -0.31 (+/- 0.02)      -19.6      < 0.0001
                                     C#                -1.68 (+/- 0.02)      -97.7      < 0.0001
                                     D                 -1.63 (+/- 0.02)      -95.3      < 0.0001
                                     Go                -0.97 (+/- 0.02)      -59.8      < 0.0001
                                     Java              -0.22 (+/- 0.02)      -13.6      < 0.0001
                                     Julia             -9.23 (+/- 0.2)       -43.0      < 0.0001
                                     JavaScript        0.16 (+/- 0.02)       9.9        < 0.0001
                                     Lua               -2.60 (+/- 0.02)      -134.2     < 0.0001
                                     Perl              -2.88 (+/- 0.02)      -141.8     < 0.0001
                                     PHP               -1.70 (+/- 0.02)      -98.7      < 0.0001
                                     R                 -2.34 (+/- 0.02)      -125.7     < 0.0001
                                     Ruby              -22.34 (+/- 149.3)    -0.2       0.881
                                     Racket            -5.57 (+/- 0.04)      -133.2     < 0.0001
                                     Rust              -4.03 (+/- 0.03)      -154.5     < 0.0001
                                     Scala             -3.59 (+/- 0.02)      -153.1     < 0.0001
                                     Swift             -3.97 (+/- 0.03)      -154.5     < 0.0001
                                     TypeScript        -0.08 (+/- 0.02)      -4.8       < 0.0001

                    Table 6: Mixed-effects results for CodeGen MultiPL-MBPP language comparison

   A similar model was fit to the InCoder pass@1 data. Table 7 shows the full estimates found by the model.

                                     Fixed effects     βb                    z          p
                                     (Intercept)       -3.85 (+/- 0.2)       -22.67     < 0.0001
                                     Bash              -2.09 (+/- 0.02)      -87.5      < 0.0001
                                     C++               -0.18 (+/- 0.02)      -10.1      < 0.0001
                                     C#                -0.88 (+/- 0.02)      -46.0      < 0.0001
                                     D                 -1.60 (+/- 0.02)      -74.5      < 0.0001
                                     Go                -0.34 (+/- 0.02)      -19.2      < 0.0001
                                     Java              -0.07 (+/- 0.02)      -3.8       0.0001
                                     Julia             -1.55 (+/- 0.02)      -73.0      < 0.0001
                                     JavaScript        1.65 (+/- 0.04)       39.7       < 0.0001
                                     Lua               -0.36 (+/- 0.02)      -20.0      < 0.0001
                                     Perl              -0.60 (+/- 0.02)      -32.4      < 0.0001
                                     PHP               0.54 (+/- 0.02)       32.0       < 0.0001
                                     R                 -0.89 (+/- 0.02)      -46.7      < 0.0001
                                     Ruby              -0.29 (+/- 0.02)      -16.6      < 0.0001
                                     Racket            -1.88 (+/- 0.02)      -82.6      < 0.0001
                                     Rust              -1.157 (+/- 0.02)     -58.3      < 0.0001
                                     Scala             -1.11 (+/- 0.02)      -56.4      < 0.0001
                                     Swift             -0.60 (+/- 0.02)      -32.6      < 0.0001
                                     TypeScript        0.84968 (+/- 0.02)    51.0       < 0.0001

                    Table 7: Mixed-effects results for InCoder MultiPL-MBPP language comparison


C.3   Mixed-Effects Results for §5.1.3 and §5.2.3
A mixed-effects model treating Frequency as a fixed-effects was fit to the Codex MultiPL-HumanEval data, with random
effects for language and problem. Table 8 shows the full estimates found by the model.

                                       Fixed effects     βb                 z         p
                                       (Intercept)       -0.31 (+/- 0.2)    -1.3      0.19
                                       Niche             -1.68 (+/-0.4)     -4.5      < 0.0001
                                       Low               -1.73 (+/- 0.3)    -5.24     < 0.0001
                                       Medium            -0.85 (+/- 0.3)    -2.8      0.006

             Table 8: Mixed-effects results for MultiPL-HumanEval Codex language frequency comparison

    A mixed-effects model treating Frequency as a fixed-effects was fit to the Codex MultiPL-MBPP data, with random
effects for language and problem. Table 9 shows the full estimates found by the model.

                                       Fixed effects     βb                 z         p
                                       (Intercept)       -0.19 (+/- 0.3)    -0.6      0.56
                                       Low               -2.13 (+/- 0.4)    -4.8      < 0.0001
                                       Medium            -0.93 (+/- 0.3)    -2.72     0.007
                                       Niche             -1.74 (+/- 0.4)    -4.10     < 0.0001

                Table 9: Mixed-effects results for MultiPL-MBPP Codex language frequency comparison
                                                                                                                       24

C.4   Mixed-Effects Results for §6.1


Three mixed-effects models were fit to the MultiPL-HumanEval data for the ablation study.
    A mixed-effects model was fit to the InCoder pass@1 rates to explore how the translation components affect its
performance. This model compared InCoder pass@1 rates for four experiments: Doctest-Only Translation, Full Translation,
No Translation, and Remove Doctests. Experiment was treated as a fixed-effect, with Python and Doctest-Only Translation
as the reference levels. Random effects for language were included; random effects for problem were not included, as the
extremely low pass rates for many problems caused instability in estimating them. Table 10 shows the full estimates found
by the model.


                                       Fixed effects        βb                z         p
                                       (Intercept)          -2.97 (+/- 0.2)   -15.6     < 0.001
                                       Remove               0.20 (+/- 0.07)   2.8       0.005
                                       No Translation       0.03 (+/- 0.03)   1.0       0.32
                                       Full Translation     0.02 (+/- 0.02)   1.3       0.20

                              Table 10: Mixed-effects results for the InCoder ablation study



    A similar mixed-effects model was fit to understand the impact of translating natural language terms and doctests
on Codex performance. This model compared Codex pass@1 rates for four experiments: Doctest-Only Translation, Full
Translation, No Translation, and Remove Doctests. Experiment was treated as a fixed-effect, with Python and Doctest-
Only Translation as the reference levels. Random effects for problem and language were included. Table 11 shows the full
estimates found by the model.


                                       Fixed effects        βb                z        p
                                       (Intercept)          -1.24 (+/- 0.3)   -4.4     < 0.0001
                                       Full Translation     0.04 (+/- 0.02)   2.2      0.03
                                       No Translation       -0.08 (+/- 0.1)   -1.3     0.2
                                       Remove               -0.35 (+/- 0.1)   -3.8     < 0.0001

                               Table 11: Mixed-effects results for the Codex ablation study



    A second model was fitted for Codex treating both Language and Experiment as fixed-effects, with interaction terms
included. For this model, we include only random intercepts but not random slopes for Problem, because of the large
number of effects the model must estimate. Tables 12 and 13 show the full estimates found by the model.


                                     Fixed effects        βb                  z          p
                                     (Intercept)          -0.44 (+/- 0.2)     -2.2       0.03
                                     Full Translation     -0.006 (+/- 0.02)   -0.3       0.78
                                     No Translation       -0.07 (+/- 0.02)    -3.1       0.002
                                     Remove               -0.14 (+/- 0.02)    -6.6       < 0.0001
                                     Bash                 -1.75 (+/- 0.02)    -77.8      < 0.0001
                                     C++                  0.17 (+/- 0.02)     8.1        < 0.0001
                                     C#                   -1.45 (+/- 0.02)    -65.7      < 0.0001
                                     D                    -1.97 (+/- 0.02)    -86.5      < 0.0001
                                     Go                   -1.14 (+/- 0.02)    -52.5      < 0.0001
                                     Java                 -0.63 (+/- 0.02)    -29.2      < 0.0001
                                     Julia                -0.87 (+/- 0.02)    -40.4      < 0.0001
                                     JavaScript           0.15 (+/- 0.02)     7.2        < 0.0001
                                     Lua                  -0.48 (+/- 0.02)    -22.7      < 0.0001
                                     Perl                 -1.10 (+/- 0.02)    -51.0      < 0.0001
                                     PHP                  -0.006 (+/- 0.02)   -0.3       0.76
                                     R                    -2.02 (+/- 0.02)    -88.8      < 0.0001
                                     Ruby                 -0.31 (+/- 0.02)    -14.4      < 0.0001
                                     Racket               -2.36 (+/- 0.02)    -100.3     < 0.0001
                                     Rust                 -0.30 (+/- 0.02)    -14.0      < 0.0001
                                     Scala                -0.24 (+/- 0.02)    -11.0      < 0.0001
                                     Swift                -0.62 (+/- 0.02)    -28.9      < 0.0001
                                     TypeScript           0.10 (+/- 0.02)     4.8        < 0.0001

                  Table 12: Mixed-effects results for the Codex ablation study by language, main effects
                                                                                                                       25

                                 Fixed effects                  βb                 z       p
                                 Full Translation*Bash          -0.02 (+/- 0.03)   -0.5    0.58
                                 No Translation*Bash            -0.47 (+/- 0.03)   -14.4   < 0.0001
                                 Remove*Bash                    -0.59 (+/- 0.03)   -17.9   < 0.0001
                                 Full Translation*C++           -0.03 (+/- 0.03)   -0.9    0.35
                                 No Translation*C++             -0.15 (+/- 0.03)   -5.0    < 0.0001
                                 Remove*C++                     -0.11 (+/- 0.03)   -3.7    0.0002
                                 Full Translation*C#            -0.02 (+/- 0.03)   -0.6    0.58
                                 No Translation*C#              0.05 (+/- 0.03)    1.6     0.10
                                 Remove*C#                      0.2 (+/- 0.03)     6.9     < 0.0001
                                 Full Translation*D             0.02 (+/- 0.03)    0.5     0.59
                                 No Translation*D               0.20 (+/- 0.03)    6.4     < 0.0001
                                 Remove*D                       0.10 (+/- 0.03)    3.2     0.001
                                 Full Translation*Go            -0.03 (+/- 0.03)   -0.8    0.41
                                 No Translation*Go              -0.03 (+/- 0.03)   -1.0    0.32
                                 Remove*Go                      0.05 (+/- 0.03)    1.8     0.08
                                 Full Translation*Java          0.12 (+/- 0.03)    3.9     < 0.0001
                                 No Translation*Java            0.14 (+/- 0.03)    4.5     < 0.0001
                                 Remove*Java                    0.12 (+/- 0.03)    4.0     < 0.0001
                                 Full Translation*Julia         0.05 (+/- 0.03)    1.8     0.07
                                 No Translation*Julia           0.05 (+/- 0.03)    1.7     0.10
                                 Remove*Julia                   -0.09 (+/- 0.03)   -2.9    0.004
                                 Full Translation*JavaScript    0.01 (+/- 0.03)    0.4     0.66
                                 No Translation*JavaScript      0.08 (+/- 0.03)    2.6     0.01
                                 Remove*JavaScript              -0.09 (+/-0.03)    -2.8    0.005
                                 Full Translation*Lua           0.06 (+/- 0.03)    1.9     0.06
                                 No Translation*Lua             -0.04 (+/- 0.03)   -1.3    0.19
                                 Remove*Lua                     -0.12 (+/- 0.03)   -3.8    0.0001
                                 Full Translation*Perl          0.23 (+/- 0.03)    7.5     < 0.0001
                                 No Translation*Perl            -0.25 (+/- 0.03)   -8.1    < 0.0001
                                 Remove*Perl                    -0.21 (+/- 0.03)   -6.9    < 0.0001
                                 Full Translation*PHP           0.06 (+/- 0.03)    1.8     0.07
                                 No Translation*PHP             0.02 (+/- 0.03)    0.6     0.58
                                 Remove*PHP                     -0.26 (+/- 0.03)   -8.6    < 0.0001
                                 Full Translation*R             0.22 (+/- 0.03)    7.0     < 0.0001
                                 No Translation*R               0.26 (+/- 0.03)    8.1     < 0.0001
                                 Remove*R                       -0.11 (+/- 0.03)   -3.5    0.0004
                                 Full Translation*Ruby          0.012 (+/- 0.03)   0.4     0.68
                                 No Translation*Ruby            0.02 (+/- 0.03)    0.5     0.58
                                 Remove*Ruby                    -0.19 (+/- 0.03)   -6.1    < 0.0001
                                 Full Translation*Racket        0.04 (+/- 0.03)    1.2     0.23
                                 No Translation*Racket          -0.07 (+/- 0.03)   -2.0    0.05
                                 Remove*Racket                  -0.21 (+/- 0.03)   -6.1    < 0.0001
                                 Full Translation*Rust          0.03 (+/- 0.03)    1.0     0.31
                                 No Translation*Rust            -0.04 (+/- 0.03)   -1.5    0.14
                                 Remove*Rust                    -0.34 (+/- 0.03)   -11.2   < 0.0001
                                 Full Translation*Scala         0.01 (+/- 0.03)    0.5     0.64
                                 No Translation*Scala           0.17 (+/- 0.03)    5.5     < 0.0001
                                 Remove*Scala                   0.03 (+/- 0.03)    1.1     0.26
                                 Full Translation*Swift         -0.01 (+/- 0.03)   -0.5    0.63
                                 No Translation*Swift           -0.39 (+/- 0.03)   -13.0   < 0.0001
                                 Remove*Swift                   -0.24 (+/- 0.03)   -8.0    < 0.0001
                                 Full Translation*TypeScript    0.05 (+/- 0.03)    1.6     0.11
                                 No Translation*TypeScript      0.11 (+/- 0.03)    3.8     0.0002
                                 Remove*TypeScript              -0.25 (+/- 0.03)   -8.4    < 0.0001

               Table 13: Mixed-effects results for the Codex ablation study by language, interaction effects



C.5   Mixed-Effects Results from §6.2
A mixed-effects model treating Static Type-checking as a fixed-effects was fit to the MultiPL-HumanEval data, with random
effects for language and problem. Interaction terms were included for Typed with each frequency category. Table 14 shows
the full estimates found by the model.

                                         Fixed effects   βb                z       p
                                         (Intercept)     -1.31 (+/- 0.3)   -3.94   < 0.0001
                                         Typed           -0.36 (+/- 0.4)   -0.95   0.34

             Table 14: Mixed-effects results for MultiPL-HumanEval Codex static type-checking comparison

  A similar mixed-effects model was fit to the Codex MultiPL-MBPP data. Table 15 shows the full estimates found by the
model.
                                                                                                                                                                              26

                                                                                 Fixed effects            βb                 z         p
                                                                                 (Intercept)              -1.31 (+/- 0.4)    -3.3      0.0009
                                                                                 Typed                    -0.52 (+/- 0.4)    -1.2      0.23

                  Table 15: Mixed-effects results for MultiPL-MBPP Codex static type-checking comparison

   A mixed-effects model testing the effect of removing Python type annotations was fit to the Codex MultiPL-HumanEval
data. Annotations was treated as a fixed-effect and problem as a random effect. Table 16 shows the full estimates found by
the model.



                                                    Average Codex pass@1   0.4




                                                                           0.3




                                                                           0.2




                                                                           0.1




                                                                           0.0

                                                                                       Full translation                        No type annotations
                                                                                                               Experiment


                                              Figure 12: Impact of Python type annotations on Codex performance


                                                                                  Fixed effects            βb                 z          p
                                                                                  Intercept                -0.26 (+/- 0.5)    -0.5       0.60
                                                                                  Annotations              -0.21 (+/- ).2)    -1.2       0.22

                                             Table 16: Mixed-effects results for Python type annotation experiments

    A mixed-effects model testing the effect of weakening TypeScript annotations to Any and running without static type-
checking was fit. There were three fixed-effects: Any, comparing TypeScript with precise types to TypeScript with all Any
types; JS, comparing TypeScript with annotations to JavaScript; and NoCheck, comparing TypeScript with and without
static type-checking. Table 17 shows the full estimates found by the model.


                                       0.5




                                       0.4
                Average Codex pass@1




                                       0.3




                                       0.2




                                       0.1




                                       0.0

                                   Type−checked TypeScript with Precise Types JavaScript                       Unchecked TypeScript with Precise Types
                                                                                                                                                  TypeScript, All Types Any
                                                                                                               Experiment

               Figure 13: Impact of type-checking and precise type annotations on TypeScript performance
                                                                                                                                                                 27

                                                           Fixed effects            βb                              z             p
                                                           Intercept                -0.24 (+/- 0.4)                 -0.6          0.56
                                                           JavaScript               -0.03 (+/- 0.03)                -1.2          0.23
                                                           Any Types                -0.38 (+/- 0.03)                -13.3         < 0.001
                                                           NoCheck                  0.04 (+/- 0.03)                 1.5           0.14

                                               Table 17: Mixed-effects results for TypeScript experiments


C.6   Mixed-Effects Results from §6.3
Tables 18 and 19 shows the results of singe-line versus multi-line comments for PHP and Racket. Separate models were
run for each language, with multi-line as a fixed effect and problem number as a random effect.




                                                     0.4
                              Average Codex pass@1




                                                     0.3
                                                                                                                                                   PL
                                                                                                                                                        PHP

                                                     0.2                                                                                                Racket




                                                     0.1




                                                     0.0

                                                                   Single−line                                   Multi−line
                                                                                        Experiment


                    Figure 14: Impact of comment style on Codex performance for PHP and Racket


                                                             Fixed effects              βb                            z           p
                                                             Intercept                  -0.46 (+/- 0.4)               -1.2        0.22
                                                             Multi-line                 -0.43 (+/-0.1)                -3.3        0.001

                         Table 18: Mixed-effect model estimates for PHP comment experiment


                                                           Fixed effects            βb                            z             p
                                                           Intercept                -4.62 (+/- 0.4)               -10.9         < 0.0001
                                                           Multi-line               1.26 (+/-0.2)                 6.4           < 0.0001

                        Table 19: Mixed-effect model estimates for Racket comment experiment

   Table 20 shows the results of comparing Perl with and without an argument-naming line after the function signature.
Argument-naming was treated as a fixed effect and problem number as a random effect.



                                                     0.3
                              Average Codex pass@1




                                                     0.2




                                                     0.1




                                                     0.0

                                                           Full Translation with Argument−Naming                Full Translation, No Argument−Naming
                                                                                                   Experiment


                      Figure 15: Impact of argument-naming line on Codex performance for Perl
                                                                                                                                                      28

                                                               Fixed effects                βb                        z          p
                                                               Intercept                    -3.03 (+/- 0.4)           -7.9       <0.0001
                                                               Argument-naming              0.81 (+/-0.2)             3.6        0.0008

                                       Table 20: Mixed-effect model estimates for Perl experiment


   Table 21 shows the results of comparing Bash with and without encoding-specifying comments. Comments and NL
Translation were treated as fixed effects and problem number as a random effect; an interaction term for Comments and
NL Translation was also included.




                                                      0.20
                               Average Codex pass@1




                                                      0.15




                                                      0.10




                                                      0.05




                                                      0.00

                                                                No comments        No comments               Comments               Comments
                                                               No NL translation   Full translation       No NL translation        Full translation
                                                                                                  Experiment


              Figure 16: Impact of encoding comments and NL translation on Codex performance for Bash




                                                             Fixed effects                     βb                         z        p
                                                             Intercept                         -3.09 (+/- 0.3)            -9.9     < 0.001
                                                             Comments                          0.01 (+/- 0.1)             0.08     0.94
                                                             Rewording                         -0.04 (+/- 0.03)           -1.3     0.19
                                                             Comments*Rewording                0.08 (+/-0.4)              1.8      0.07

                                 Table 21: Mixed-effect model estimates for Bash experiment




C.7   Mixed-Effects Results for §6.4

We categorize problems into groups based on which Python language features they use: dictionaries, tuples, Booleans,
lists, or none of the above. We base these categorizations on the Python type annotations for each problem. Problems were
coded 1 Tuple, List, Bool, and Dictionary if they contain a type annotation for the respective feature, and 0 otherwise.
   We fit a mixed-effects model to understand how Codex pass@1 rates are affected by the language features used in the
problem, using Tuple, List, Bool, and Dictionary as fixed-effects, with random effects for problem and language. Table 22
shows the full estimates found by the model.


                                                                   Fixed effects      βb                        z             p
                                                                   (Intercept)        -1.19 (+/- 0.3)           -3.5          < 0.001
                                                                   List               -0.15 (+/- 0.4)           -0.3          0.73
                                                                   Bool               0.10 (+/- 0.6)            0.2           0.86
                                                                   Tuple              -0.73 (+/- 0.9)           -0.8          0.40
                                                                   Dictionary         -3.27 (+/- 1.8)           -1.8          0.07

                            Table 22: Mixed-effects results for the impact of language features


   A second model was fit with interaction effects for languages and language features. Table 23-24 shows the full estimates
found by the model.
                                                                      29

          Fixed effects     βb                 z        p
          (Intercept)       -0.37 (+/- 0.3)    -1.1     0.26
          Bash              -1.61 (+/- 0.2)    -86.6    <0.0001
          C++               -0.45 (+/- 0.2)    -25.4    <0.0001
          C#                -0.86 (+/- 0.2)    -47.7    <0.0001
          D                 -2.03 (+/- 0.2)    -106.6   <0.0001
          Go                -0.96 (+/- 0.2)    -53.0    <0.0001
          Java              -0.42 (+/- 0.2)    -23.8    <0.0001
          Julia             -1.25 (+/- 0.2)    -68.5    <0.0001
          JavaScript        -0.07 (+/- 0.2)    -3.8     0.0001
          Lua               -0.32 (+/- 0.2)    -18.4    <0.0001
          Perl              -0.54 (+/- 0.2)    -30.6    <0.0001
          PHP               -0.37 (+/- 0.2)    -20.6    <0.0001
          R                 -1.79 (+/- 0.2)    -96.1    <0.0001
          Ruby              -0.63 (+/- 0.2)    -35.6    <0.0001
          Racket            -2.24 (+/- 0.2)    -114.7   <0.0001
          Rust              -0.84 (+/- 0.2)    -46.7    <0.0001
          Scala             -0.49 (+/- 0.2)    -27.2    <0.0001
          Swift             -1.60 (+/- 0.2)    -86.5    <0.0001
          TypeScript        -0.15 (+/- 0.2)    -8.4     <0.0001
          List              -0.20 (+/- 0.4)    -0.5     0.62
          Bool              0.07 (+/- 0.5)     0.1      0.9
          Tuple             -0.39 (+/- 0.9)    -0.44    0.66
          Dictionary        -1.65 (+/- 1.9)    -0.89    0.37
          Bash:List         -0.48 (+/- 0.02)   -20.2    <0.0001
          C++:List          0.78 (+/- 0.02)    34.6     <0.0001
          C#:List           -1.17 (+/- 0.02)   -50.9    <0.0001
          D:List            0.055 (+/- 0.02)   2.3      0.019
          Go:List           -0.20 (+/- 0.02)   -8.8     <0.0001
          Java:List         0.15 (+/- 0.02)    6.8      <0.0001
          Julia:List        0.40 (+/- 0.02)    17.6     <0.0001
          JavaScript:List   0.28 (+/- 0.02)    12.4     <0.0001
          Lua:List          -0.42 (+/- 0.02)   -19.2    <0.0001
          Perl:List         -0.72 (+/- 0.02)   -32.2    <0.0001
          PHP:List          0.27 (+/- 0.02)    12.2     <0.0001
          R:List            -0.47 (+/- 0.02)   -19.9    <0.0001
          Ruby:List         0.49 (+/- 0.02)    22.2     <0.0001
          Racket:List       -0.01 (+/- 0.02)   -0.48    0.63
          Rust:List         0.62 (+/- 0.02)    27.5     <0.0001
          Scala:List        0.48 (+/- 0.02)    21.5     <0.0001
          Swift:List        1.30 (+/- 0.02)    56.9     <0.0001
          TypeScript:List   0.34 (+/- 0.02)    15.4     <0.0001
          Bash:Bool         -0.52 (+/- 0.03)   -17.04   <0.0001
          C++:Bool          0.87 (+/- 0.03)    28.8     <0.0001
          C#:Bool           0.52 (+/- 0.02)    18.2     <0.0001
          D:Bool            0.44 (+/- 0.03)    15.2     <0.0001
          Go:Bool           -0.16 (+/- 0.03)   -5.7     <0.0001
          Java:Bool         -0.49 (+/- 0.03)   -17.0    <0.0001
          Julia:Bool        0.81 (+/- 0.03)    28.2     <0.0001
          JavaScript:Bool   0.25 (+/- 0.03)    8.5      <0.0001
          Lua:Bool          0.11 (+/- 0.03)    3.9      <0.0001
          Perl:Bool         -1.18 (+/- 0.03)   -40.2    <0.0001
          PHP:Bool          0.79 (+/- 0.03)    27.2     <0.0001
          R:Bool            0.42 (+/- 0.03)    14.6     <0.0001
          Ruby:Bool         0.074 (+/- 0.03)   2.6      0.009
          Racket:Bool       -1.10 (+/- 0.03)   -32.2    <0.0001
          Rust:Bool         0.60 (+/- 0.03)    20.9     <0.0001
          Scala:Bool        0.18 (+/- 0.03)    6.2      <0.0001
          Swift:Bool        0.47 (+/- 0.03)    15.9     <0.0001
          TypeScript:Bool   0.14 (+/- 0.03)    5.0      <0.0001

Table 23: Mixed-effects results for the impact of language features
                                                                                                                             30

                                   Fixed effects           βb                   z         p
                                   Bash:Tuple              -2.17 (+/- 0.09)     -24.9     <0.0001
                                   C++:Tuple               0.35 (+/- 0.05)      7.8       <0.0001
                                   C#:Tuple                -0.71 (+/- 0.05)     -13.6     <0.0001
                                   D:Tuple                 -0.043 (+/- 0.05)    -0.8      0.43
                                   Go:Tuple                -1.22 (+/- 0.06)     -22.1     <0.0001
                                   Java:Tuple              -2.44 (+/- 0.06)     -39.9     <0.0001
                                   Julia:Tuple             0.24 (+/- 0.05)      4.9       <0.0001
                                   JavaScript:Tuple        0.80 (+/- 0.04)      17.8      <0.0001
                                   Lua:Tuple               0.078 (+/- 0.04)     1.7       0.08
                                   Perl:Tuple              -0.21 (+/- 0.05)     -4.4      <0.0001
                                   PHP:Tuple               0.50 (+/- 0.04)      11.3      <0.0001
                                   R:Tuple                 0.07 (+/- 0.05)      1.4       0.16
                                   Ruby:Tuple              0.21 (+/- 0.04)      4.7       <0.0001
                                   Racket:Tuple            0.22 (+/- 0.06)      4.0       <0.0001
                                   Rust:Tuple              -0.20 (+/- 0.05)     -4.2      <0.0001
                                   Scala:Tuple             0.41 (+/- 0.04)      9.2       <0.0001
                                   Swift:Tuple             0.32 (+/- 0.05)      6.7       <0.0001
                                   TypeScript:Tuple        0.73 (+/- 0.05)      15.4      <0.0001
                                   Bash:Dictionary         -13.29 (+/- 115.6)   -0.1      0.91
                                   C++:Dictionary          -2.1 (+/- 0.2)       -9.9      <0.0001
                                   C#:Dictionary           -2.42 (+/- 0.3)      -7.7      <0.0001
                                   D:Dictionary            -13.22 (+/- 121.4)   -0.11     0.91
                                   Go:Dictionary           -4.51 (+/- 1.0)      -4.5      <0.0001
                                   Java:Dictionary         -2.02 (+/- 0.2)      -8.3      <0.0001
                                   Julia:Dictionary        -2.76 (+/- 0.4)      -6.6      <0.0001
                                   JavaScript:Dictionary   -2.41 (+/- 0.2)      -10.6     <0.0001
                                   Lua:Dictionary          0.88 (+/- 0.1)       8.9       <0.0001
                                   Perl:Dictionary         -1.56 (+/- 0.2)      -7.1      <0.0001
                                   PHP:Dictionary          0.28 (+/- 0.1)       2.7       0.006
                                   R:Dictionary            -1.55 (+/- 0.3)      -4.7      <0.0001
                                   Ruby:Dictionary         -0.18 (+/- 0.1)      -1.4      0.17
                                   Racket:Dictionary       -12.52 (+/- 112.5)   -0.11     0.91
                                   Rust:Dictionary         1.61 (+/- 0.1)       16.9      <0.0001
                                   Scala:Dictionary        -1.24 (+/- 0.2)      -7.3      <0.0001
                                   Swift:Dictionary        -0.19 (+/- 0.2)      -1.0      0.30
                                   TypeScript:Dictionary   -2.39 (+/- 0.2)      -10.049   <0.0001

                       Table 24: Mixed-effects results for the impact of language, continued features


A PPENDIX D
C HARACTERIZATION OF C ODE G ENERATION E RRORS
This section provides details regarding our error evaluation study on MultiPL-HumanEval as overviewed in Section 6.5.
First we discuss the process of categorizing errors in a multi-language context. Then we provide the full set of themes,
errors, and counts across the four studied languages: Python (H IGH, untyped), C# (M EDIUM, typed), Swift (L OW, typed),
and Racket (N ICHE, untyped). Finally, we showcase full code examples generated by Codex containing a variety of errors.

D.1   Notes on Process & Findings
To perform the evaluation, we chose two typed languages and two untyped languages across all four frequency categories.
A language expert then performed a manual investigation of a subset of the completions to derive a set of common error
types. These errors could be associated with common error labels in a language (e.g., NameError in Python) or an observed
phenomenon (e.g., UseofDeprecatedIdentifiers in Swift). Then, through an iterative process of manual inspection
and automatic error detection via analyzing evaluation output, we developed a set of error labels unique to each language.
We then arrived at the multi-language themes and categories via discussion and consensus.
    The multi-language nature of the evaluation contributes to variation between the language classifications.
For instance, languages vary significantly in the specificity of their error messages. Consider the theme of
TimeoutOrInfiniteRecursion: Python has a specific error message RecursionError when it encounters an infinite
recursive loop, whereas Racket will simply evaluate indefinitely. As the generated standard output and standard error were
used for automatic classifications, there may be variations in how errors were counted depending on the error messages
and precision of string search terms.
    Overall, each error label is specific to the language under study and was subject to different levels of manual assessment.
Therefore, the prevalence of a theme, rather than a specific error label or even category, likely provides a better source of
inter- and intra-language information. Although the four languages in our study address different language variations
(typed/untyped, frequency), they are not representative of all languages in our benchmark nor additional unstudied
languages. Therefore, it is likely there are error labels, themes, and potentially categories that are missing from this
characterization. Errors classified under the theme “AssertionFailed” describe errors from generated code with correct
syntax which produces incorrect output. Other than via manual inspection of the over 10,000+ errors per language, there
is no clear method of more precisely classifying errors of that type.
                                                                                                                       31

D.2   Complete Error Themes



In Tables 25 - 28 below, rows with the gray background are the most frequent error in that category for the specific
language. Items in italics are errors directly referenced in Section 6.5. There are around 32,000 Codex completions for
each language for our full translation. Variations in the reported counts below are due to support for a different number
of prompts for each language and completions which generate multiple errors on failure. In the later case, we count all
present errors.




                     Category    Theme                           Error                 Count   Example
                     Runtime     AssertionFailed                 AssertionError        17104
                     Runtime     TimeoutOrInfiniteRecursion      Timeout               4462
                     Runtime     InvalidDataStructureOperation   IndexError            460
                     Runtime     TimeoutOrInfiniteRecursion      RecursionError        86
                     Runtime     InvalidDataStructureOperation   AttributeError        5
                     Runtime     InvalidDataStructureOperation   KeyError              2
                     Runtime     DivisionByZero                  ZeroDivisionError     1
                     Static      UndefinedIdentifier             NameError             2942    Fig. 19
                     Static      UndefinedIdentifier             UnboundLocalError     1
                     Type        InvalidTypeConversion           TypeError             123
                     Language    Miscellaneous                   ValueError            334
                     Language    Miscellaneous                   IndentationError      32
                     Language    LanguageSpecific                EOFError              1       Fig. 25
                     Model       OutOfTokens                     SyntaxError           333
                     Model       ExceptionInGeneratedCode        NotImplementedError   253     Fig. 20

                                Table 25: Error Categories, Themes, and Labels for Python




                 Category   Theme                           Error                          Count    Example
                 Runtime    AssertionFailed                 AssertionError                 22473
                 Runtime    TimeoutOrInfiniteRecursion      Timeout                        4470
                 Runtime    NullReference                   NullReferenceException         1201
                 Runtime    InvalidDataStructureOperation   ArgumentOutOfRangeException    632
                 Runtime    InvalidDataStructureOperation   InvalidOperationException      93
                 Runtime    InvalidDataStructureOperation   IndexOutOfRangeException       82
                 Runtime    InvalidDataStructureOperation   KeyNotFoundException           4
                 Static     UndefinedIdentifier             UndefinedIdentifier            1577     Fig. 17
                 Static     MissingReturn                   MissingReturn                  155
                 Static     UndefinedIdentifier             MethodNotFound                 40
                 Static     UndefinedIdentifier             TypeNotFound                   15
                 Static     ArityMismatch                   InvalidArgument                11
                 Static     ReDeclaration                   ReDeclaration                  2
                 Type       InvalidTypeConversion           TypeConversion                 409
                 Language   Miscellaneous                   FormatException                77
                 Language   LanguageSpecific                InvalidAssignment              13
                 Language   Miscellaneous                   ArgumentException              1
                 Model      OutOfTokens                     SyntaxError                    319
                 Model      ExceptionInGeneratedCode        NotImplementedException        5
                 Model      ExceptionInGeneratedCode        InvalidBeat                    1

                                  Table 26: Error Categories, Themes, and Labels for C#
                                                                                              32
Category   Theme                           Error                            Count   Example
Runtime    AssertionFailed                 AssertionFail                    10051
Runtime    InvalidDataStructureOperation   IndexOutOfRange                  330
Runtime    TimeoutOrInfiniteRecursion      Timeout                          275
Runtime    InvalidDataStructureOperation   InvalidRangeCreation             271
Runtime    NullReference                   UnwrapNil                        149
Runtime    InvalidDataStructureOperation   StringIndexOutOfBounds           99
Runtime    DivisionByZero                  DivisionByZeroInRemainder        24
Runtime    InvalidDataStructureOperation   RemoveLastFromEmptyCollection    6
Runtime    InvalidDataStructureOperation   ArrayIndexOutOfRange             3
Runtime    InvalidDataStructureOperation   RemoveFirstFromEmptyCollection   1
Runtime    InvalidDataStructureOperation   NegativeArrayIndex               1
Static     UndefinedIdentifier             CanNotFindInScope                4259
Static     UndefinedIdentifier             NonExistentMethod                2582
Static     UndefinedIdentifier             InvalidSyntax                    213
Static     UndefinedIdentifier             CallingNonFunctionType           103
Static     IncorrectAPIMethodCall          SubscriptStringWithInt           68      Fig. 24
Static     UndefinedIdentifier             LinkerError                      55
Static     IncorrectAPIMethodCall          StringsArentCharArrays           42
Static     UndefinedIdentifier             UseBeforeDecl                    17
Static     IncorrectAPIMethodCall          StringIndices                    12
Static     ReDeclaration                   RedeclarationOfVariable          11
Type       InvalidTypeConversion           OtherLocation                    556
Type       InvalidTypeConversion           ReturnTypeError                  349
Type       InvalidTypeConversion           ArgumentTypeError                303
Type       InvalidTypeConversion           NumericsTypeError                261
Type       InvalidTypeConversion           CollectionAndInner               241
Type       InvalidTypeConversion           UnknownTypeErrorInCall           200
Type       InvalidTypeConversion           BinOpTypeError                   182
Type       InvalidTypeConversion           BranchTypeMismatch               125
Type       InvalidTypeConversion           MiscTypeError                    111
Type       InvalidTypeConversion           UnwrappedNonOptional             67
Type       InvalidTypeConversion           UseOfModWithFloat                63
Type       InvalidTypeConversion           ClosureResultTypeError           11
Type       InvalidTypeConversion           ShouldHaveUnwrappedOptional      10      Fig. 22
Type       InvalidTypeConversion           PatternTypeError                 10
Type       InvalidTypeConversion           AssignmentTypeError              10
Type       InvalidTypeConversion           WeirdSubscriptTypeError          10
Type       InvalidTypeConversion           SubscriptingTypeError            9
Language   LanguageSpecific                UseOfDeprecatedIdentifiers       176
Language   LanguageSpecific                MissingArgumentLabel             113     Fig. 23
Language   LanguageSpecific                ImmutableViolation               62
Language   LanguageSpecific                ExtraArgument                    38
Language   LanguageSpecific                IncorrectArgumentLabel           19
Language   LanguageSpecific                OverflowUnderflowTrap            9
Language   LanguageSpecific                ExtraneousArgumentLabel          5
Language   LanguageSpecific                NonExclusiveMutation             3
Model      OutOfTokens                     RanOutOfTokens                   95
Model      OutOfTokens                     CompilerErrorCutoff              9
Model      OutOfTokens                     MissingReturn                    4

                Table 27: Error Categories, Themes, and Labels for Swift
                                                                                                                 33
                Category   Theme                           Error                         Count   Example
                Runtime    AssertionFailed                 assertionError                10409
                Runtime    TimeoutOrInfiniteRecursion      timeout                       1044
                Runtime    InvalidDataStructureOperation   stringIndexOutOfRange         448
                Runtime    DivisionByZero                  divisionBy0                   376
                Runtime    InvalidDataStructureOperation   letDuplicateIdentifier        2
                Static     UndefinedIdentifier             unboundIdentifier             5814    Fig. 18
                Static     ArityMismatch                   arityMismatch                 570
                Static     ReDeclaration                   listIndexOutOfRange           281
                Static     UndefinedIdentifier             applicationOnNotAFunction     184
                Static     IncorrectAPIMethodCall          badBuiltInFnAppCall           69
                Static     UndefinedIdentifier             useBeforeInit                 12
                Type       InvalidTypeConversion           contractViolation             4887
                Type       InvalidTypeConversion           hashmapNoValueForKey          7
                Language   DoesNotKnowSyntax               missingOrUnmatchedBraces      2004
                Language   LanguageSpecific                unknownEscapeSequence         216
                Language   DoesNotKnowSyntax               badSyntax                     127
                Language   DoesNotKnowSyntax               missingElse                   63
                Language   DoesNotKnowSyntax               ifExtraArgs                   48
                Language   Miscellaneous                   badMatch                      24
                Language   DoesNotKnowSyntax               unclassified                  6
                Language   LanguageSpecific                badCharConst                  4
                Language   DoesNotKnowSyntax               elseAsExpression              2
                Model      OutOfTokens                     incompleteGeneration          2092
                Model      GenerateAnotherLang             generatingWebpageOrMarkdown   608     Fig. 21
                Model      GenerateAnotherLang             defaultValueExpMissing        57
                Model      ExceptionInGeneratedCode        errorByGeneratedProgram       34

                               Table 28: Error Categories, Themes, and Labels for Racket




D.3   Error Examples Related to Section 6.5




class Problem {
    // Translated docstring
    public static string Intersection(Tuple<long, long> interval1, Tuple<long, long> interval2) {
        long start = Math.Max(interval1.Item1, interval2.Item1);
        long end = Math.Min(interval1.Item2, interval2.Item2);
        if (start > end) {
            return "NO";
        }
        long length = end - start + 1;
        return IsPrime(length) ? "YES" : "NO";
    }

Figure 17: C#: Exhibits a local context error as it relies on a non-existent IsPrime method (HumanEval Prompt #127,
Theme: “UndefinedIdentifier”, Code: “UndefinedIdentifier”)
                                                                                                                        34

#lang racket

;; You are given a non-empty list of positive integers. Return the
greatest integer that is greater than
;; zero, and has a frequency greater than or equal to the value of the
integer itself.
;; The frequency of an integer is the number of times it appears in the list.
;; If no such a value exist, return -1.
;; Examples:
;; >>> (search (list 4 1 2 2 3 1))
;; 2
;; >>> (search (list 1 2 2 3 3 3 4 4 4))
;; 3
;; >>> (search (list 5 5 4 4 4))
;; -1
(define (search lst)
  (let ([freq (make-hash)])
     (for ([i lst])
       (hash-set! freq i (+ 1 (hash-ref freq i 0))))
     (let ([max-freq (apply max (hash-values freq))])
       (for ([i lst])
          (when (and (> i 0) (= max-freq (hash-ref freq i)))
            (return i))))
     -1))

Figure 18: Racket: A completion which uses the keyword return. return is not a keyword in Racket, but is a common
keyword in Python. (HumanEval Prompt #69, Theme: “UndefinedIdentifier”, Error: “unboundIdentifier” )




def same_chars(s0: str, s1: str) -> bool:
    """
    docstring
    """
    return Counter(s0) == Counter(s1)

Figure 19: Python: This code expects a call to import collections to facilitate the use of Counter dictionary subclass
(HumanEval Prompt # 54, Theme: “UndefinedIdentifier”, Error: “NameError”)




def find_closest_elements(numbers: List[float]) -> Tuple[float, float]:
    """ From a supplied list of numbers (of length at least two) select and return two
    that are the closest to each other and return them in
    order (smaller number, larger number).
    >>> find_closest_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.2])
    (2.0, 2.2)
    >>> find_closest_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.0])
    (2.0, 2.0)
    """
    # YOUR CODE HERE
    raise NotImplementedError()

Figure 20: Python: The full completion for this program contains only a call to raise, so this code will always produce an
error. (HumanEval Prompt #20, Theme: “ExceptionInGeneratedCode”, Error: “NotImplementedError”)
                                                                                                                 35

#lang racket

;; You are given a string s.
;; if s[i] is a letter, reverse its case from lower to upper or vise versa,
;; otherwise keep it as it is.
;; If the string contains no letters, reverse the string.
;; The function should return the resulted string.
;; Examples
;; >>> (solve "1234")
;; "4321"
;; >>> (solve "ab")
;; "AB"
;; >>> (solve "#a@C")
;; "#A@c"
(define (solve s)
  (if (string-contains s #\a)
      (string-map (lambda (c) (if (char-alphabetic? c)
                                  (char-upcase c)
                                  (char-downcase c)))
                  s)
      (string-reverse s)))
‘‘‘

### [Reverse the order of words in a string]
(https://www.codewars.com/kata/reverse-the-order-of-words-in-a-string)

‘‘‘racket
#lang racket

Figure 21: Racket: This snippet is an example of Markdown being generated instead of Racket (it is word wrapped for
presentation here). (HumanEval Prompt #161, Theme: “GenerateAnotherLanguage”, Error: “GeneratingWebpageOrMark-
down”)




/// This function takes an array l and returns an array l’ such that
/// l’ is identical to l in the indicies that are not divisible by three,
while its values at the indicies that are divisible by three are equal
/// to the values of the corresponding indicies of l, but sorted.
/// >>> sort_third(l: [1, 2, 3])
/// [1, 2, 3]
/// >>> sort_third(l: [5, 6, 3, 4, 8, 9, 2])
/// [2, 6, 3, 4, 8, 9, 5]
func sort_third(l: [Int]) -> [Int] {
    var l = l
    for i in stride(from: 2, to: l.count, by: 3) {
        l[i] = l[i].min(l[i - 1])
        l[i - 1] = l[i].max(l[i - 1])
    }
    return l
}

Figure 22: Swift: This code produces the type error error: value of optional type ’Int?’ must be
unwrapped to a value of type ’Int’ (HumanEval Prompt # 33, Theme: “InvalidTypeConversion”, Er-
ror:“ShouldHaveUnwrappedOptional”)




/// Given a positive integer n, return the count of the numbers of n-digit
/// positive integers that start or end with 1.
func starts_one_ends(n: Int) -> Int {
    if n == 1 {
        return 2
    }
    if n == 2 {
        return 4
    }
    return starts_one_ends(n - 1) + starts_one_ends(n - 2)
}

Figure 23: Swift: A correct recursive call to starts_one_ends in Swift would be starts_one_ends(n: n - 1).
(HumanEval Prompt #83, Theme: “LanguageSpecific”, Error: “MissingArgumentLabel”)
                                                                                                                       36

D.4   Additional Error Examples from our Codex Error Evaluation


/// Translated docstring
func match_parens(lst: [String]) -> String {
    var lst = lst
    var str = ""
    var count = 0
    for i in 0..<lst.count {
        str += lst[i]
    }
    for i in 0..<str.count {
        if str[i] == "(" {
             count += 1
        } else {
             count -= 1
        }
        if count < 0 {
             return "No"
        }
    }
    if count == 0 {
        return "Yes"
    } else {
        return "No"
    }
}

Figure 24: Swift: This is an example of incorrect string indexing in Swift - you cannot call str[i] where i is an Integer
(HumanEval Prompt #119, Theme: “IncorrectAPIMethodCall”, Error: “SubscriptStringWithInt”)


def car_race_collision(n: int) -> int:
    """
    Imagine a road that’s a perfectly straight infinitely long line.
    n cars are driving left to right; simultaneously, a different set of n cars
    are driving right to left.   The two sets of cars start out being very far from
    each other. All cars move in the same speed. Two cars are said to collide
    when a car that’s moving left to right hits a car that’s moving right to left.
    However, the cars are infinitely sturdy and strong; as a result, they continue moving
    in their trajectory as if they did not collide.

      This function outputs the number of such collisions.
      """
      # The idea is to sort the cars by their starting positions.
      # Then, we can simulate the race by iterating through the cars
      # from left to right, and counting the number of cars that are
      # moving right to left.
      #
      # The time complexity is O(n log n) because of the sorting.
      # The space complexity is O(n) because of the sorting.
      #
      # The time complexity can be improved to O(n) by using a
      # counting sort. The space complexity can be improved to
      # O(1) by using a bucket sort.
      left_to_right = [0] * n
      right_to_left = [0] * n
      for i in range(n):
          left_to_right[i] = int(input())
          right_to_left[i] = int(input())
      left_to_right.sort()
      right_to_left.sort()
      collisions = 0
      left_to_right_index = 0
      right_to_left_index = 0
      while left_to_right_index < n and right_to_left_index < n:
          if left_to_right[left_to_right_index] < right_to_left[right_to_left_index]:
              collisions += right_to_left_index
              left_to_right_index += 1
          else:
              right_to_left_index

Figure 25: Python: This code produces an EOFError due to the calls to input() inside the for loop. The canonical example
does not use input(). Our evaluation procedures do not handle user input, hence the error. (HumanEval Prompt #41,
Theme: “LanguageSpecific”, Error: “EOFError”)
                                                                                                                                37

;; You are given a list of integers.
;; You need to find the largest prime value and return the sum of its digits.
;; Examples:
;; >>> (skjkasdkd (list 0 3 2 1 3 5 7 4 5 5 5 2 181 32 4 32 3 2 32 324 4 3))
;; 10
;; >>> (skjkasdkd (list 1 0 1 8 2 4597 2 1 3 40 1 2 1 2 4 2 5 1))
;; 25
;; >>> (skjkasdkd (list 1 3 1 32 5107 34 83278 109 163 23 2323 32 30 1 9 3))
;; 13
;; >>> (skjkasdkd (list 0 724 32 71 99 32 6 0 5 91 83 0 5 6))
;; 11
;; >>> (skjkasdkd (list 0 81 12 3 1 21))
;; 3
;; >>> (skjkasdkd (list 0 8 1 2 1 7))
;; 7
(define (skjkasdkd lst)
  (define (is-prime? n)
     (define (iter i)
       (cond ((= i n) #t)
             ((= (modulo n i) 0) #f)
             (else (iter (+ i 1)))))
     (iter 2))
  (define (sum-digits n)
     (define (iter n acc)
       (cond ((= n 0) acc)
             (else (iter (quotient n 10) (+ acc (remainder n 10))))))
     (iter n 0))
  (define (largest-prime lst)
     (cond ((null? lst) 0)
           ((is-prime? (car lst)) (max (car lst) (largest-prime (cdr lst))))
           (else (largest-prime (cdr lst)))))
 (sum-digits (largest-prime lst)))
‘‘‘

## Задача 2

Да се дефинира функция ‘(skjkasdkd lst)‘, която приема списък от цели числа и връща списък от цели числа, които са прости
и по-големи от най-голямото просто число в дадения списък.

Примери:


‘‘‘racket
>>> (skjkasdkd (list 0 3 2 1 3 5 7 4 5 5 5 2 181 32 4 32 3 2 32 324 4 3))
’(181 191 193 197 199 211 223 227 229 233 239 241 251 257 263
269 271 277 281 283 293 307 311 313 317 331 337 347 349 353
359 367 373 379 383 389 397 401 409 419 421 431 433

Figure 26: Racket: Codex can produce comments/code in languages other than English. The Bulgarian text above translates
as the following via Google Translate: “## Task 2, Define a function ‘(skjkasdkd lst)‘ that accepts a list of integers and returns
a list of integers that are prime and greater than the largest prime in the given list., Examples:” (HumanEval Prompt #119,
Theme: “GenerateAnotherLanguage”, Error: “GeneratingWebpageOrMarkdown”)

D.5   Additional Error Examples
This section contains error examples which we found through manual inspection of Codex output outside of our structured
analysis.

function sum_squares(lst){
   return sum(map(lambda n: n ** 2, filter(lambda n: n % 3 == 0, lst)))
}

Figure 27: This JavaScript completion is generated for our full translation at T = 0.8 for HumanEval Prompt #142. The
complete function body is executable, functional-style Python.


local function will_it_fly(q, w)
  return is_balanced(q) and sum(q) <= w
end

Figure 28: This Lua completion is generated by our full translation at T = 0.2 for HumanEval Prompt #72. is_balanced
is not defined in the local context and is likely an expected helper function. The call to sum is Python-like, as sum is a
Python built-in method.
