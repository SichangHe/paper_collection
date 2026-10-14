Empirical Software Engineering (2026) 31:181
https://doi.org/10.1007/s10664-026-10914-3




Automated formalisation of informal specifications by
combining LLMs and grammar-based language processing

Iat Tou Leong1        · Raul Barbosa1

Received: 4 March 2025 / Accepted: 16 June 2026 / Published online: 6 July 2026
© The Author(s) 2026


Abstract
Informal specifications of software artefacts need to be formalised to facilitate rigorous
analysis, including deductive verification. Automated formalisation of informal specifica-
tions can significantly reduce the effort of manual translation. However, a major challenge
lies in bridging the gap between the rich syntax of natural language and the need for
precise semantics in formal specification languages. Building on the empirical observation
that modern pre-trained large language models (LLMs) can effectively handle the breadth
of natural language, while symbolic natural language processing (NLP) is more efficient in
formal languages, this paper proposes an approach that combines both methodologies. The
proposed solution, Hybrid Automated Formalisation of Informal Specifications (HAFIS),
uses an LLM to restrict the syntax of informal specifications into the language of a for-
mal grammar, and proposes the concept of Typed Semantic Interpretation to enforce the
semantics of the resulting formal specifications. Using a public set of real-world informal
specifications, we evaluated HAFIS and compared it with a purely symbolic approach and
the direct use of LLMs as baselines. Results show that HAFIS increases language accep-
tance from 23% to 100% and accurately translates 88% of the cases into Java Modeling
Language (JML). Furthermore, mutation analysis shows that the HAFIS-generated JML
effectively finds defects in programs. These results substantiate that the proposed approach
is effective and contributes to software analysis using natural language.

Keywords Software engineering · Formal specification · Software verification · Java
modeling language · Compilers




Communicated by: Lei Ma, Roberto Pietrantuono
This article belongs to the Topical Collection: Special Issue on Software Reliability Engineering.

    Iat Tou Leong
    itleong@dei.uc.pt
    Raul Barbosa
    rbarbosa@dei.uc.pt
1
    CISUC, DEI, University of Coimbra, Coimbra, Portugal
181 Page 2 of 47                                         Empirical Software Engineering (2026) 31:181


1 Introduction

Informal specifications are commonly used to describe software behaviour using natural
language. To ensure software correctness, formal verification can be applied to show the
absence of defects, requiring specifications written in formal syntax and semantics. How-
ever, the process of formalising informal specifications is typically manual and requires
significant effort. Therefore, automating the formalisation process can significantly reduce
the effort required for software analysis.
    The challenge of formalising informal specifications has become increasingly pressing
in recent years, given that AI-powered assistants have become mainstream and are widely
used for code writing. Therefore, one possibility to improve the correctness of generated
code is to formalise the content of natural language interactions with such assistants. More
generally, formal specifications can contribute to the correctness of software, regardless of
whether it is AI- or human-generated.
    Formalising informal specifications involves interpreting the meaning of natural lan-
guage and constructing specifications with rigorous syntax and semantics. Natural language
terms can be ambiguous, while formal specification languages provide unambiguous syn-
tax and semantics. Meaning representations (MRs), which are logic representations of the
semantic relationships in textual inputs, are examples of syntactic structures that can be
automatically derived with a state-of-the-art NLP.
    Recent advancements in classical symbolic NLP are promising with regard to the genera-
tion of formal specifications, although some restrictions to the input language are required.
Conversely, modern pre-trained large language models accept a greater variety of natural
language constructs, but lack the precise syntax and semantics of formal specification lan-
guages like JML. Therefore, none of the two approaches is sufficient for handling real-world
problems.
    This paper addresses the challenges of automating the translation of real-world informal
specifications into formal specification languages, namely JML, which is closely related
to first-order logic. We propose a hybrid solution, HAFIS, that uses an LLM to restrict
input informal specifications into sentences that comply with the formal grammar of a sym-
bolic grammar-based NLP approach. The syntax-restricted informal specifications include
explicit information about method parameters, data types and method return types, which
are identified by the LLM with only the method signature information from the programs.
The deliberate reliance on method signatures rather than program code avoids conflating
informal specification translation with program analysis, and they represent pre-implemen-
tation design artefacts that exist independently of executable code (e.g. in interface defi-
nitions or early design documents). The grammar-based NLP approach developed in this
paper consists of a compiler that translates MRs derived from syntax-restricted informal
specifications, by a state-of-the-art NLP called ccg2lambda (Martínez-Gómez et al. 2016),
to target method-level JML.
    MR is a logic representation of the semantic relationships in textual inputs, and is the clos-
est representation to the JML which is the first-order logic based language. The ccg2lambda
tool is a symbolic NLP tool that derives MRs encoded in Neo-Davidsonian event seman-
tics from natural language sentences. The process of ccg2lambda starts with tagging words
with part-of-speech tags. Then, it parses the tagged sentences with the C&C parser (Curran
et al. 2007) to generate combinatory Categorical Grammar (CCG) parse trees. The CCG is


13
Empirical Software Engineering (2026) 31:181                                Page 3 of 47 181


a linguistically expressive grammar formalism that is particularly used for parsing natural
language. Finally, it traverses the parse trees to construct MRs by mapping the tree nodes
with lambda calculus templates.
    The compiler is developed to translate the MRs encoded in Neo-Davidsonian event
semantics into JML specifications. JML is a formal specification language that is specifi-
cally designed for Java programs. It is based on first-order logic and provides a rigorous
syntax and semantics for specifying program behaviour, for instance, pre/postconditions
with predicates and nested quantifications, as well as Boolean side-effect free expressions.
Tools such as OpenJML (Cok 2011) support deductive verification of Java programs with
JML specifications.
    We hypothesise that HAFIS can effectively translate informal specifications into a formal
language, namely JML, in an automated manner. The main contributions of this work are:

● Improving the language acceptance of the grammar-based approach. The proposed ap-
  proach uses an LLM to restrict informal specifications into sentences that comply with
  the formal grammar of the symbolic approach. This aims to solve the main observed
  limitation of grammar-based approaches, which is related to handling the diversity of
  natural language and the consequent inability to generate correct MRs.
● Disambiguating and identifying symbols and types. The proposed approach tasks an
  LLM with identifying method parameters along with their types, as well as method
  return types in informal specifications, to improve the success rate of the translation.
● Automating the formalisation of informal specifications. The paper introduces the con-
  cept of typed semantic interpretation (TSI) to assure the meaning and validity of formal
  specifications. This aims to address the main observed limitation of LLMs, which is the
  lack of rigorous semantics of the generated JML. This is achieved by performing scope
  and type analysis over the intermediate meaning representation.
● Evaluating and assessing the quality of the generated formal specifications. The paper
  presents the results of evaluating HAFIS on a real-world public dataset. As baselines for
  comparison, we consider the use of a purely symbolic grammar-based approach and the
  direct use of a pure LLM to perform the translation tasks. Furthermore, the quality of
  the generated JML is evaluated through mutation analysis, to measure the ability of the
  generated JML to find defects using a state-of-the-art theorem prover.

HAFIS can work with any LLM which provides a prompt interface. To illustrate the gener-
ality of the LLM acceptance in HAFIS, both industrial and open source LLMs are compared
in this paper. We evaluate HAFIS on a real-world dataset of 84 programs with 1697 speci-
fication sentences, found on GitHub. These programs are answers to problems in LeetCode
coding platform that commonly checks the submission of programs using testing based on
the informal specifications. The JML syntax and semantic correctness are checked with
OpenJML (Cok 2011), and the z3 (de Moura and Bjørner 2008) theorem prover checks the
consistency regarding the programs. A mutation analysis is performed to check the com-
pleteness of the translated JML regarding to the informal specification.
    The following research questions are answered with the evaluation:
RQ1        How effective is using an LLM in improving the derivation of MRs from informal
specifications by restricting the syntax of informal specifications?
HAFIS and the purely grammar-based approach use the MRs derived from informal specifi-


                                                                                  13
181 Page 4 of 47                                       Empirical Software Engineering (2026) 31:181


cations to generate target JML specifications. To increase the breadth of language that can be
accepted by the purely grammar-based approach, one needs to write the NLTK (Bird et al.
2009) templates used in ccg2lambda (Martínez-Gómez et al. 2016) in the form of a CCG.
We aim to investigate whether HAFIS using an LLM can restrict the syntax of real-world
informal specifications into sentences that the purely grammar-based approach can accept,
such that one can save time spent in learning the concepts of CCG and writing the templates.
To measure the effectiveness of improving the MR derivation from informal specifications,
we compare the derivation rate between HAFIS and the purely grammar-based approach.
The experimental result shows that using an LLM in HAFIS has significantly improved the
MR derivation.
RQ2        How effective is using an LLM in improving the translation of informal specifica-
tions into JML by disambiguating the parameters and identifying the datatypes of param-
eters and method return types?
In restricting the syntax of informal specifications, we also ask the LLM to return syntax-
restricted informal specifications with explicit method parameters, data types, and return
types. The syntax-restricted informal specifications use specific notations to provide this
information, such that even if the parameter names are common nouns, their usages are
distinguishable. We hypothesise that this explicit information can improve the translation
from informal specifications into JML. To measure the effectiveness of this improvement,
we compare the percentage of syntactically and semantically correct JML translated from
HAFIS, pure grammar-based and pure LLM approaches. Results show that using an LLM
to restrict the syntax of informal specifications with explicit information greatly improved
the translation from informal specifications into JML.
RQ3        How effective is the HAFIS-generated JML in finding defects compared to the
pure LLM approach?
We hypothesise that the translated JML is effective in finding defects in software artefacts.
Given that HAFIS performs scope and type analysis based upon typed semantic interpreta-
tions, the resulting JML should be more effective than a pure LLM which lacks formal se-
mantics. To measure this effectiveness, we perform mutation analysis to show the use of the
translated JML with deductive verification. We compare the mutants killed by the theorem
prover using JML generated by HAFIS and pure LLM approach and use the resulting score
to assess the quality of these JML specifications. Results show that the JML generated by
HAFIS outperforms the pure LLM approach regarding quality, namely, killing the mutants.
The proposed solution explores the possibility of using an LLM to complement state-of-
the-art NLP techniques, to provide improved correctness of software. To the best of our
knowledge, this work is the first to combine LLMs, to restrict the syntax of requirements,
with a symbolic NLP technique to ensure the formal semantics of the resulting specification.
Experimental results substantiate that the formal specifications generated from the proposed
automated formalisation effectively find defects in software artefacts. The overall result
shows that using an LLM and a grammar-based approach can contribute to avoiding manual
translation without retraining a model for domain-specific usage.
   The remainder of this paper is organised as follows: Section 2 briefly introduces the
related concepts. Section 3 empirically examines the limitations of purely symbolic and
pure LLM approaches. Section 4 explains the hybrid approach. Sections 5 and 6 describe
the experimental methodology, the results and the main observations. Section 8 examines




13
Empirical Software Engineering (2026) 31:181                                 Page 5 of 47 181


limitations and potential threats to the validity of this study. Section 9 surveys the related
literature. Section 10 discusses the main conclusions of the paper.


2 Background

Automating the formalisation of informal specifications involves using an LLM to restrict
informal specifications and symbolic NLP to translate the syntax-restricted text into a for-
mal specification language.

2.1 Formal Specification Language

A formal specification language is a precise, unambiguous, and machine-readable language
used to describe software functionalities. Deductive verification techniques, including theo-
rem proving, are often used to verify the correctness of formally specified software. Recent
works have put effort into developing formal specification languages for different program-
ming languages, for instance, Dafny (Leino 2010), why3 (Filliâtre and Paskevich 2013),
OCL (Warmer and Kleppe 2003), ACSL (Kirchner et al. 2015) and JML (Leavens et al.
2006), where ACSL is inspired by JML.
   The JML language is a behavioural interface specification language for Java that sup-
ports design by contract through formally defined method specifications. A JML specifica-
tion characterises the externally observable behaviour of a method by explicitly stating the
obligations of the caller and the guarantees provided by the callee. The core contractual ele-
ments are preconditions and postconditions, expressed as logical predicates over program
states.
   JML specifications are annotated in Java programs as code comments, starting with //@
followed by keywords and specification bodies. Tools like OpenJML (Cok 2011) and ESC/
Java (Chalin et al. 2005) accept JML for deductive verification.
   A method contract in JML is primarily composed of preconditions, introduced by
the requires clause, and postconditions, introduced by the ensures clause. Seman-
tically, a method contract of the form requires P; ensures Q; is interpreted as
∀s, s′ (P (s) ∧ Terminates(M, s, s′ )) =⇒ Q(s′ ), where s, s′ denote pre-state and post-state
of method M, respectively.
   Let s, s′ ∈ Σ, where Σ is the set of all possible states. Define P, Q : Σ → {true, false}
as pure predicate functions over the program state. JML is a first-order logic language con-
structed inductively from the set of JML expressions EJML , the classical propositional con-
nectives (!, &&, ||, ==>, <==>), and quantifiers (\forall, \exists). The EJML set consists
of all Java Boolean expressions, extended with JML operators such as \old and \result. We
refer the reader to Chalin et al. (2005) for a thorough and comprehensive specification of
JML.

2.2 Natural Language Processing

NLP is a field of study focused on creating computational models capable of understand-
ing and analysing human language. NLP can be broadly divided into two main approaches
depending on how it handles language: symbolic and deep learning. The symbolic approach


                                                                                  13
181 Page 6 of 47                                        Empirical Software Engineering (2026) 31:181


uses explicit representations, varying from basic regular expressions to intricate grammati-
cal rules, along with algorithms designed to interpret a language’s syntax and semantics.
The deep learning approach harnesses deep neural networks to learn the intricacies and
configurations of language patterns from the corpus.
   Our compiler takes as input intermediate MRs constructed by ccg2lambda (Martínez-
Gómez et al. 2016), which represents sentence meaning using a typed λ-calculus–based
language. The syntax of the representation consists of variables, constants, λ-abstractions,
and function application, augmented with logical operators and quantifiers. A complete and
detailed specification of the MR language grammar can be found in Martínez-Gómez et al.
(2016). The formal grammar is listed in Fig. 8, and the language is defined as follows.
   Let M denote the set of MRs generated by ccg2lambda. The language of M is a λ-calcu-
lus. Formally, we define its syntax and semantics as follows. Let V be a countably finite set
of variables and C be a set of lexical constants denoting individuals or predicates. The set of
well-formed expressions E is constructed inductively:

1. If x ∈ V , then x ∈ E .
2. If c ∈ C , then c ∈ E .
3. If x ∈ V and M ∈ E , then (λx.M ) ∈ E(λ-abstraction).
4. If M, N ∈ E , then (M, N ) ∈ E (function application).
5. If M, N ∈ E , then (M ∧ N ) ∈ E (logical connectives), (M ∨ N ) ∈ E (logical connec-
   tives), (¬M ) ∈ E (logical connectives), (M =⇒ N ) ∈ E (logical connectives) and
   (M = N ) ∈ E (logical connectives).
6. If x ∈ V and M ∈ E , then (∀x.M ) ∈ E (quantifiers) and (∃x.M ) ∈ E (quantifiers).

Types are drawn from a small set of atomic types (most commonly e for individuals and t for
truth values) together with functional types constructed recursively (e.g. < e, t >). Seman-
tic composition is strictly compositional and mirrors the combinatory rules of CCG. Each
lexical item is paired with a typed λ-expression, and CCG rule applications correspond
directly to λ-calculus operations, primarily function application and abstraction. The out-
put of this process is a well-typed higher-order formula, which is subsequently normalised
through β -reduction and variable renaming to eliminate λ-abstractions.
    Within the λ-calculus meaning representation described above, ccg2lambda adopts a
Neo-Davidsonian treatment of predicate–argument structure, in which verbal predicates
introduce explicit event variables. A verb denotes a property of events, while its arguments
and modifiers are represented as independent predicates that relate participants and prop-
erties to the same event via thematic roles. For example, the sentence “The method sorts
the array” can be represented as ∃e(sort(e) ∧ Agent(e, method) ∧ T heme(e, Array))
. Passive forms are handled without altering the underlying event structure. Thus,
“The array is sorted in ascending order” results in a representation of the form
∃e(sort(e) ∧ T heme(e, Array) ∧ ascending(e)), where the agent role is not expressed
but the event predicate remains explicit. By separating event predicates from their par-
ticipants and modifiers, this representation supports uniform semantic composition across
active and passive constructions. The goal of our compiler is to generate JML by taking as
input these MR and contextualising them using the method signatures.
    MR is a logical representation that expresses the meaning of text, which can be encoded
into many structures. Neo-Davidsonian event semantics is an MR framework that focuses


13
Empirical Software Engineering (2026) 31:181                                           Page 7 of 47 181


on the verbs as the meaning of events. The syntax and semantics of this event semantics
involve representing verbs with event arguments (e.g. ‘e’) which are existentially quanti-
fied. These arguments of verbs are linked to the event arguments through thematic roles,
for instance, ‘equal(e03) & (Subj(e03) = x01)’ provides ‘e03’ as an argument to the verb
‘equal’ and ‘Subj’ is a thematic role associated to an entity ‘x01’. Adverbs and other modi-
fiers are analysed as predicates of event arguments to provide further information about the
event. Tools such as ccg2lambda (Martínez-Gómez et al. 2016) can derive MR from natural
language through the flow of tokenisation, CCG trees derivation and mapping semantic
compositions with NLTK (Bird et al. 2009) semantic templates.
    An example of MR in Neo-Davidsonian semantics derived from an informal speci-
fication using ccg2lambda is listed in Table 1. In our last work, we have contributed to
ccg2lambda to add the syntax of each predicate in Penn Treebank format to the output MR.
The predicate associated with an event argument variable (e.g. e03) provides the semantics
of the action of a predicate, for instance, equal{JJ}(e03) represents a predicate which is
an adjective that provides the semantics equal as an event. The grammatical relationships
connect the associated semantics to form the semantics of a phrase, such as (Subj(e03) =
x01) describes the subject of the event associated to e03 is the entity variable x01 (i.e. the
length). The Rel relationship provides the possessive semantics that the predicate semantics
of length is possessed by that of result.
    MEARC (Leong and Barbosa 2024) is a symbolic approach involving a compiler that
translates MR encoded in higher-order logic (HOL) derived from ccg2lambda into a formal
specification in JML. The work provides translation from restricted informal specification
into JML using an expandable semantic interpretation library and idiom template. To extend
the work to cover wider language support, one needs to add semantic interpretations and
identifying English idioms.
    Pre-trained LLMs such as GPT (OpenAI 2022), Llama (Touvron et al. 2023), Minerva
(Lewkowycz et al. 2022) and StarCoder2 (Lozhkov et al. 2024) trained on extensive corpora
offer enhanced natural language processing. These models can be prompted to perform vari-
ous tasks, such as extracting information from input text. By providing specific examples in
the prompts, it is possible to refine the output and facilitate repetitive tasks, such as format-
ting the output message with relevant examples.

2.3 Restricted Natural Language to Formal Specifications

In the field of formalising informal specifications, recent efforts often focus on narrowing
down the scope of natural language due to its rich syntax and semantics. By limiting the
scope, it becomes easier to map the language within that scope to a formal specification lan-

Table 1 Example of MR in Neo-        Informal specification                    Meaning representation
Davidsonian semantics derived
                                     The type_integer_array_ result’s length   exists x01.(exists x02.
from an informal specification
                                     is equal to 2.                            (_result{NN}(x02) & _
using ccg2lambda
                                                                               type_integer_array_{NN}
                                                                               (x02) & Rel(x01,x02)) &
                                                                               _length{NN}(x01) & ex-
                                                                               ists e03.(_equal{JJ}(e03)
                                                                               & (Subj(e03) = x01) &
                                                                               exists x04.(_2{CD}(x04)
                                                                               & (Dat(e03) = x04))))


                                                                                             13
181 Page 8 of 47                                       Empirical Software Engineering (2026) 31:181


guage. Recent works can be broadly categorised into structured (controlled) and restricted
(non-controlled) (Kuhn 2014).
   Structured natural language is commonly used for well-defined languages with clear
lexicons, syntax, and semantics. On the other hand, restricted natural language refers to
language that imposes a scope without explicit definitions.
   FRET has been addressed by several research works using structured natural language
approaches (Giannakopoulou et al. 2020; Farrell et al. 2022). This type of approach is usu-
ally designed for specific purposes and ensures unambiguous syntax and semantics. Still,
they require developers to invest time in learning the language.
   Works such as MEARC (Leong and Barbosa 2024) and ARSENAL (Ghosh et al. 2014)
are examples of using restricted natural language. These works adopt language based on
formal grammars of MR, such as HOL and temporal logic. Their usage is not limited to
specific domains as they do not have a controlled scope. Language can be accepted as long
as the MR adheres to the defined rules, and the corresponding semantics can be composed.


3 Challenges of Automating the Formalisation

We analyse the results of applying purely symbolic MEARC (Leong and Barbosa 2024)
and directly using the LLM of GPT-3.5 (OpenAI 2022) to generate formal specifications
in JML. The results obtained from these two approaches are detailed in Table 2. The goal
is to thoroughly understand the limitations of purely symbolic and pure LLM approaches,
so this section extends our preliminary work (Leong and Barbosa 2023) before the follow-
ing sections devise the HAFIS approach to combine their advantages. The MR required by
MEARC is derived by using ccg2lambda (Martínez-Gómez et al. 2016). In order to com-
pare the generated JML, we use OpenJML (Cok 2011) to check the syntax and semantics
correctness. Deductive verification is carried out using OpenJML along with z3 (de Moura
and Bjørner 2008) to check the correctness of JML regarding the programs.
    By analysing the results listed in the above table, the main challenges of automating the
formalisation of informal specifications using pure symbolic and pure LLM approaches can
be observed to fall into four distinct categories:
Challenge 1         Expanding language acceptance in grammar-based approach. In rows 3
and 5, MEARC has failed because ccg2lambda does not produce correct MRs. An MR en-
coded in HOL is considered correct if it is fully reduced and complies with the parsing rules
defined in MEARC. The idiom templates must also be expanded to accommodate specific
sentence structures, such as the ‘if and only if’ structure for these two cases. However, en-
compassing the entire English language could pose a significant challenge. Sentence struc-
tures, including idioms and slang, must be identified, and the associated parsing rules must
be added.
Challenge 2         Distinguishing between precondition and postcondition. For row 8 (the
row with a question mark), the result is arguably correct as the informal specification can be
a precondition to a binary search method or a postcondition to a sorting method. Ambiguity
arises when there is no information about whether the term ‘input arr’ is a parameter or a
result of a method. The informal specifications need explicit syntax to provide information
for distinguishment; however, this requires manual rewriting.
Challenge 3         Insufficient knowledge in domain-specific usage of LLM. In the case of


13
Empirical Software Engineering (2026) 31:181                                            Page 9 of 47 181

Table 2 Preliminary Results of translating informal specifications to JML using grammar-based NLP and
LLM. The prompt fed to the LLM is “Please convert this sentence to JML: [specification]”, where ‘specifica-
tion’ is replaced by the input informal specification
Informal specification          JML generated by the grammar- Correct JML generated by            Correct
                                based approach                           LLM
1. The array should not be      requires (array != null);          Y     requires array != null; Y
null.
2. If parameter x deeply        ensures(((((x == null &&           N     requires                 N
equals parameter y, then        y == null) && ((x == y) ||               x.deepEquals(y); en-
result is true.                 (x.equals(y)) || Arrays.equals(x,        sures \result == true;
                                y))) || ((x != null && y != null
                                && x.length == y.length) &&
                                (\forall int i; 0 <= i < x.length;
                                ((x[i] == null && y[i] == null) ||
                                (x[i] != null && y[i] != null &&
                                (!x[i].getClass().isArray() &&
                                !y[i].getClass().isArray() &&
                                x[i].equals(y[i])))))))) ==> (\
                                result==true));
3. If and only if parameter x NO CORRECT MR IS                     N     requires                 N
deeply equals parameter y, DERIVED                                       x.deepEquals(y) <==>
then result is true.                                                     \result == true;
4. If the input n is a prime    ensures((n == 2 || (n > 2 && (\    Y     requires isPrime(n);     N
number, the result is true.     forall int k; n > 2 && 2 <= k            ensures \result ==
                                && k <= n/2; n % k != 0))) ==>           true;
                                (\result==true));
5. If and only if the input n No correct MR was derived.           N     requires isPrime(n)      N
is prime, the result is true                                             <==> \result == true;
6. If the result is true, the   ensures((\result==true) ==>        Y     requires isEven(n)       N
input number is even            (number % 2 == 0));                      ==> \result == true;
7. If the result is false, the  ensures((\result==false) ==>       Y     requires !isEven(n)      N
input number is not even        (!(number % 2 == 0)));                   ==> \result == false;
8. The input arr should be      ensures (\forall int i; 0 <= i && Y      requires (\forall int i, Y (?)
sorted in descending order i < arr.length - 1; arr[i] >= arr[i           j; 0 <= i && i < j &&
                                + 1]);                                   j < arr.length; arr[i]
                                                                         >= arr[j]);
9. The result is less than or ensures((\result >= 0) && (\         Y     ensures \result >= 0     Y
equal to 2000 and the result result <= 2000));                           && \result <= 2000;
is greater than or equal to 0.
10. The input num1 is less requires((num2 <= 1000) &&              Y     requires num1 <=         Y
than or equal to 1000 and       (num1 <= 1000));                         1000 && num2 <=
the input num2 is less than                                              1000;
or equal to 1000.


LLM results, despite the syntactic error in the 2nd row, there are four instances of failure
in rows 4, 5, 6, and 7. These instances involve references to undeclared methods, which
can be considered model hallucinations. These semantic errors indicate that the LLM lacks
grounding regarding the semantics of JML. Fine-tuning an LLM, using specialised corpora
and substantial retraining, could mitigate this issue although it would not formally solve it.
Challenge 4         Non-deterministic feature of LLM. To further explore the issue of unde-
clared methods in the results of LLM, we adjusted the prompt, instructing the LLM not to
invoke a separate function. The results of applying the modified prompt to rows 2 and 4 are
presented in Table 3. The change in JML keyword and inconsistent impact to the target JML
suggest that the LLM can exhibit nondeterministic behaviour.


                                                                                              13
181 Page 10 of 47                                              Empirical Software Engineering (2026) 31:181


Table 3 Results of modifying      Informal              JML produced        JML produced by         Correct
the prompt to the LLM. The ad-    specification         by original query   modified query
ditional commands of “without
                                  If parameter x        Requires            Ensures (\re-           N
calling a separate function” is
                                  deeply equals         x.deepEquals(y);    sult == true &&
added to the original prompt
                                  parameter y, then     ensures \result     x.deepEquals(y)) || (\
used in Table 2
                                  result is true.       == true;            result == false &&
                                                                            !x.deepEquals(y));
                                  If the input n is     Requires            Ensures (\result ==     Y
                                  a prime number,       isPrime(n);         true && (\forall int i;
                                  the result is true.   ensures \result     2 <= i && i < n; n %
                                                        == true;            i != 0)) || (\result ==
                                                                            false && (\exists int
                                                                            i; 2 <= i && i < n; n
                                                                            % i == 0));


Neither the pure grammar-based nor the pure LLM approach can fully resolve the issue.
While the grammar-based approach provides accurate translations, extending it to encom-
pass the English language could be a daunting endeavour. Conversely, LLM offers com-
prehensive language coverage; however, it necessitates specialised corpora and additional
training time. The key question remains: Is it feasible to leverage the strengths of both solu-
tions to tackle these challenges?
   This paper introduces HAFIS, which is an approach combining the two approaches – the
grammar-based approach and the LLM approach – to address the challenges of automat-
ing the formalisation of informal specifications. Table 4 shows the results of applying the
proposed approach to the informal specifications in Table 2. Results show that the proposed
approach can derive MR in all cases compared to those that the grammar-based approach
and the LLM approach fail to derive. The case of row 8 with ambiguity in both pre/post-
condition is also resolved by the proposed approach, as identification of method result has
been made explicit in the syntax-restricted form automatically. All the generated JML are
syntactically and semantically correct, as verified by OpenJML. The next section will pres-
ent the details of the approach.


4 Hybrid Automated Formalisation of Informal Specifications

We aim to formalise informal specifications into checkable specifications. As outlined in
Section 3, a key challenge is to develop an approach with a wide language coverage that can
generate syntactically and semantically valid sentence structure for both grammar-based
NLP and MEARC (Leong and Barbosa 2024) to facilitate accurate JML generation.

4.1 Conceptual Roadmap

Each step of the solution is designed to tackle a specific aspect of the problem, gradually
building toward the solution. We begin by providing a high-level, non-technical summary
of the overall approach, outlining the key ideas and the logical flow of the solution. This
overview is intended to present the rationale behind the structure of the solution and the
sequence of the core contributions.




13
Empirical Software Engineering (2026) 31:181                                                Page 11 of 47 181

Table 4 Applying HAFIS on the sentences in Table 2 to generate target JML
Informal specification Syntax-restricted form                      JML generated by HAFIS                Correct
1. The array should not The integer array parameter ‘arr’ is requires (arr != null);                     Y
be null.                   not null.
2. If parameter x deep- The boolean result is equal to             ensures(((x == null && y ==           Y
ly equals parameter y, the true literal if the integer array       null) || (x == y) || (x.length ==
then result is true.       parameter ‘x’ deeply equals the         y.length && (\forall int i; 0 <= i
                           integer array parameter ‘y’.            < x.length; x[i] == y[i]))) ==>
                                                                   (\result == true));
3. If and only if param- The boolean result is equal to the        ensures(((x == null && y ==           Y
eter x deeply equals       true literal if and only if the integer null) || (x == y) || (x.length ==
parameter y, then          array parameter ‘x’ deeply equals       y.length && (\forall int i; 0 <= i
result is true.            the integer array parameter ‘y’.        < x.length; x[i] == y[i]))) ==>
                                                                   (\result == true));
4. If the input n is a     If the boolean result is equal to the ensures((\result == true) ==>           Y
prime number, the          true literal, the integer parameter     (n == 2 || (n > 2 && (\forall int
result is true.            ‘n’ has no divisors other than 1 and k; n > 2 && 2 <= k && k <=
                           itself.                                 n/2; n%k != 0))));
5. If and only if the      If the boolean result is equal to the ensures((\result == true) ==>           Y
input n is prime, the      true literal, the integer parameter     (n == 2 || (n > 2 && (\forall int
result is true             ‘n’ is a prime number.                  k; n > 2 && 2 <= k && k <=
                                                                   n/2; n%k != 0))));
6. If the result is true, If the boolean result is equal to the ensures((\result == true) ==>            Y
the input number is        true literal, the integer parameter     (number % 2 == 0));
even                       ‘number’ mod 2 is equal to 0.
7. If the result is false, If the boolean result is equal to the ensures((\result == false) ==>          Y
the input number is        false literal, the integer parameter    (!(number % 2 == 0)));
not even                   ‘number’ mod 2 is not equal to 0.
8. The input arr should If the length of the integer array         ensures((arr.length > 1) ==> (\       Y
be sorted in descend-      parameter ‘arr’ is greater than 1, all forall int i; 0 <= i < arr.length-1;
ing order                  values in the integer array param-      arr[i] >= arr[i+1]));
                           eter ‘arr‘ are sorted in descending
                           order after execution.
9. The result is less      The integer result is less than or      ensures(\result <= 2000) && (\        Y
than or equal to 2000      equal to 2000 and is greater than or result >= 0));
and the result is greater equal to 0.
than or equal to 0.
10. The input num1         The integer parameter ‘num1’ is         requires((num1 <= 1000) &&            Y
is less than or equal      less than or equal to 1000 and is       (num1 >= -2147483648));
to 1000 and the input      greater than or equal to the mini-      requires((num2 <= 1000) &&
num2 is less than or       mum value of a java integer. The        (num2 >= -2147483648));
equal to 1000.             integer parameter ‘num2’ is less
                           than or equal to 1000 and is greater
                           than or equal to the minimum value
                           of a java integer.


  Suppose we have a requirement for a software component and the corresponding method
written in Java, such as:




    Our goal is to derive a formal specification in JML that rigorously captures this informal
specification. This process involves four key steps: syntax restriction of informal specifica-
tion, parsing meaning representation, semantic analysis, and specification synthesis.


                                                                                                    13
181 Page 12 of 47                                        Empirical Software Engineering (2026) 31:181


   The first step is to restrict the input informal specification’s syntax to align with the for-
mal grammar accepted by the symbolic pipeline. This ensures compatibility with the CCG
framework used in the ccg2lambda (Martínez-Gómez et al. 2016) implementation. An LLM
is prompted with few-shot examples to rewrite the informal specification into a syntax-
restricted form. For instance:

   Input: “The input array must not be null. ”

   Output: “The integer array parameter ‘arr’ is not null. ”

This step ensures the requirement adheres to the grammatical structures that can be parsed
by ccg2lambda, which relies on CCG rules to derive MR. By using a simple regular expres-
sion, the sentence is classified as a precondition because it does not mention the method
result.
   Once the informal specification is syntax-restricted, the next step is to parse it into a
formal structure using the ccg2lambda pipeline. The sentence is tokenised and parsed into a
CCG derivation tree. Each word is assigned a syntactic category (e.g. noun, verb, adjective),
enabling compositional semantics. Each subtree is mapped to a lambda calculus expression
defined in the template of ccg2lambda. After the parsing, alpha and beta reductions are
performed on the expression to reduce a finalised MR encoded in HOL with Neo-David-
sonian Event Semantics. The semantics provide thematic role relationships (e.g. Subject
of, Accusative of, etc.) between entity variables. The MR of this sentence is -exists x01.
(_param_arr_{NN}(x01) & _type_integer_array_{NN}(x01) & exists e02.(_null{JJ}(e02)
& (Subj(e02) = x01))).
   The MR is then parsed by our compiler into an abstract syntax tree (AST) (see Fig. 1)
using an LR(1) grammar. The AST provides a hierarchical and analysable structure to facili-
tate the semantic analysis and code synthesis. A compiler symbol table (see Table 5) is con-
structed to keep track of the references and data types of the identified entity variables. Data
types (e.g. integer array) are identified during parsing and assigned to associated entity vari-
ables. An event table (see Table 6) is built to record the thematic relationships for each event
variable to relate the associated entities.
   With the AST constructed, semantic analysis – including type checking and semantic
synthesis – is performed using TSIs. TSIs are JML semantic templates that can be mapped
to MR predicates. Each TSI defines the term (the predicate symbol), syntax (the syntactic
category), argument definition, synthesised data type, synthesised interpretation type and
the interpretation (the JML template for code generation). Table 7 shows the TSIs that are
involved in the semantic synthesis of the AST from Fig. 1. For each parameter predicate
(e.g. arr), there is a TSI created based on the method signature information. Type checking
is performed between the data type that is decided during parsing, and the data type in the
created TSI. Developers can indicate inconsistency between these data types to perform
correction either in the specification or program. There can be multiple TSIs with the same
term and the same syntax as a predicate. Type checking ensures that the TSI matched to a
predicate rooted at a subtree accepts the same number of children with the same data types
declared in the TSI.
   The final step synthesises JML specifications from the AST using visitor patterns and
symbol tables. The AST is traversed recursively using a visitor pattern. The visitor pattern


13
Empirical Software Engineering (2026) 31:181                                           Page 13 of 47 181

Fig. 1 The AST of the sentence ‘The integer array parameter
‘arr’ is not null’




Table 5 The compiler symbol table built during parsing the sentence ‘The integer array parameter ‘arr’ is
not null’
Symbol name                                                                               Data type
x01                                                                                       Integer array
e02                                                                                       Undefined



Table 6 The event table built during parsing the sentence ‘The integer array parameter ‘arr’ is not null’
Symbol name                                  Thematic role                               Associated entity
e02                                          Subject of                                  x01



Table 7 The TSIs involved in         Term      Syntax   Argument    Synthesised    Interpreta-   Interpre-
semantic synthesis of the AST                           definition  data type      tion type     tation
in Fig. 1
                                     arr       NN       *           Primitive:     direct        arr
                                                                    integer
                                                                    reference:
                                                                    array
                                     null      JJ       symbol:     primitive:     expressions (Subj)
                                                        Subj primi- boolean                    == null
                                                        tive: any   reference:
                                                        reference: undefined
                                                        array




                                                                                                 13
181 Page 14 of 47                                        Empirical Software Engineering (2026) 31:181


decouples the AST structure from code generation logic to enable modular extensions, such
that new TSIs can always be added without changing the logic in the existing compiler.
Each node is processed to generate the corresponding JML fragment. The compiler symbol
table resolves the symbol’s data type. Finally, the target code of the informal specification is:




   The resulting JML specification is ready for deductive verification with tools such as
OpenJML (Cok 2011) and z3 (de Moura and Bjørner 2008). One could also consider devel-
oping backends for other specification languages.

4.2 Design Detail

In this paper, we present HAFIS, an approach that utilises both an LLM and grammar-based
NLP to translate informal specifications in rich semantics into JML. We exploit the exten-
sive language coverage provided by LLM to produce restricted informal specifications that
specify datatypes of parameters and method returns, and adhere to the sentence structures
that can be derived into MRs in Neo-Davidsonian event semantics. The TSI (explained in
Section 4.5.2) is introduced to facilitate type checking in the translation. Finally, JML is
synthesised by mapping the semantics in the TSI to the predicates in the MR.
    The design of HAFIS is broadly divided into three steps:

● Restricting syntax of informal specification (Section 4.3): An LLM with a few-shot
  prompt restricts the syntax of input informal specification.
● MR derivation (Section 4.4): Ccg2lambda (Martínez-Gómez et al. 2016) with default
  Neo-Davidsonian semantic template derives the MR of each syntax-restricted sentence.
● MR to JML translation (Section 4.5): To enable MEARC (Leong and Barbosa 2024)
  to accept the MR encoded in Neo-Davidsonian event semantics, enhancements in its
  whole pipeline are required. To further improve the accuracy of produced JML, TSI is
  introduced to allow type-checking during the translation.

    1. AST construction and scope checking (Section 4.5.1): AST is produced by parsing
       the MR with an LR(1) grammar supporting the Neo-Davidsonian event semantics.
       The entity and event argument variables are associated with scopes in the symbol
       table.
    2. TSI analysis (Section 4.5.3): Predicates are associated with their syntactically
       mapped TSIs.
    3. TSI synthesis (Section 4.5.4): Synthesis is performed based on event relationships
       identified from parsing on each subtree rooted at predicate nodes with syntactically
       and semantically mapped TSIs.
    4. Code generation (Section 4.5.5): JML is generated using the resulting AST and TSIs.

To clarify the whole approach (see Fig. 2), we illustrate the input and output for all the pipe-
lines with a Java program listed in Fig. 3 and its corresponding set of informal specifications
enclosed in Fig. 4.




13
Empirical Software Engineering (2026) 31:181                                                 Page 15 of 47 181




Fig. 2 Diagram of HAFIS for automated formalising informal specifications into JML. The process starts
with a Java program with a piece of informal specifications. Syntax restriction is applied on the informal
specifications using LLM with a few-shot prompt. Target JML is translated through the steps of MR deri-
vation and the translation of MR into JML



4.3 Restricting Syntax of Informal Specification

We begin with a program (see Fig. 3) and a piece of informal specifications (see Fig. 4)
documented individually. To guide the LLM in syntax restriction, a prompt with multiple
examples (see Fig. 5) is created. The prompt is structured into three sections: (i) an overview
of the task that explains the role of LLM as a specification analyser responsible for writing
specifications (ii) a list of examples, and (iii) a section specifying the input context, com-
mand and output format.
     Each example comprises an informal functional specification, a method signature, and
a set of syntax-restricted informal specifications. The pairs of informal specifications and
method signatures are chosen from an open-source code repository ​(​h​t​t​p​s​:​/​/​g​i​t​h​u​b​.​c​o​m​/​j​a​v​
a​d​ev​ ​/L
          ​ ​e​et​​Co​ ​d​e​-​i​n​-​J​av​ ​a​​​​)​. These pairs contain diversity in parameter datatypes and method
returns, including integer, string, array and list. The syntax-restricted informal specifica-
tion examples are written based on the acceptable syntax from both ccg2lambda (Martínez-
Gómez et al. 2016) and MEARC (Leong and Barbosa 2024) by the authors. Each example
sentence is written specifying the datatypes of parameters and method return.
     The sentences describing only the behaviour of parameters (i.e. mentioning ‘parameter’)
are considered as preconditions. Those describing method return (i.e. mentioning ‘result’)
are considered as postconditions. This distinguishment is based on the design of JML (Leav-
ens et al. 2006), which indicates that the method return (\result) cannot be used in a pre-
condition. These sentences are filtered with simple regular expressions to the terms that
are related to data types and parameter names recognised by the LLM. Figure 6 shows the
output produced by using the prompt on the informal specifications (see Fig. 4) and the
method signature of the sample Java program (see Fig. 3). To better clarify how an MR is
derived and translated into JML, the following sections illustrate the translation of the first
sentence in Fig. 6.




                                                                                                    13
181 Page 16 of 47                                            Empirical Software Engineering (2026) 31:181




Fig. 3 A real-world Java program taken as an example to demonstrate the flow of HAFIS throughout this
section



4.4 Deriving Meaning Representation

Each sentence goes through the ccg2lambda (Martínez-Gómez et al. 2016) process to derive
the MR, which includes tokenisation, CCG tree derivation, and semantic composition.
Firstly, the sentence is tokenised using special characters and white spaces as delimiters. It
then undergoes part-of-speech tagging and parsing by the C&C (Curran et al. 2007) parser
to produce a CCG tree.
   After that, the leaves and nodes of this tree are matched with the rules outlined in the
template, formulated in NLTK (Bird et al. 2009) lambda calculus format. This matching
process assigns meaning to the words within the nodes, resulting in a higher-order logic
MR in Neo-Davidsonian event semantics. To further refine the MR, we have contributed to
ccg2lambda (Martínez-Gómez et al. 2016) to automatically annotate all MR predicates with
their corresponding syntactic categories. Figure 7 shows the MRs derived from the syntax-
restricted informal specifications returned from the LLM listed in Fig. 6.




13
Empirical Software Engineering (2026) 31:181                                          Page 17 of 47 181




Fig. 4 The informal specifications of the Java program in Fig. 3 taken as an example to demonstrate the
flow of HAFIS throughout this section


4.5 Translating MR into JML

The derived MR is subjected to MEARC (Leong and Barbosa 2024) to generate JML speci-
fication. To translate accurate JML, scope and type analysis are performed with the support
of TSI. If any errors are encountered during the translation process, it is immediately halted,
and an error message is displayed. We consider that a future work can be on a feedback loop,
which can be formed by sending these messages to the LLM to improve the syntax of the
informal specifications. The remainder of this section provides a detailed explanation of the
translation process.

4.5.1 Abstract Syntax Tree Construction

A parser based on flex and bison is constructed using an LR(1) grammar, which is detailed
in Fig. 8. Upon receiving each input MR, an AST is created in a binary tree format. The
internal nodes (subtree roots) are either connectives (and ( &), or (|), imply (→), equivalence
(↔)) or predicates. The leaf nodes consist of entity or event variables serving as arguments
for the predicates.
   For each sentence, there can be many quantifying expressions (i.e. exist or forall). Each
quantifying expression has an entity variable and it must be argument to a predicate, or the


                                                                                             13
181 Page 18 of 47                                             Empirical Software Engineering (2026) 31:181




Fig. 5 The prompt used in HAFIS with multiple examples feeding to the LLM for restricting the syntax
of the input specification. To provide context to the LLM, the method signature of the input program is
needed


MR cannot be translated due to variables are not resolved. Two quantifying expressions can
reference to the entity variables that are outside their quantifying expression. There is a need
to build a reference table to keep track of their references, and the correct scopes prevent
incorrect predicate associations.
   A compiler symbol table is built to link all the symbols and references, as well as data
types. The parameter and result data type is found in the Java data type predicates, for
instance, ‘_type_string_’ is a data type predicate for Java String. The grammatical rela-
tions within the formula are stored separately in an event table. For instance, the relation
of ‘(Subj(e05) = x01)’ provides a record in the table of the event is e05, and an associated
entity variable x01 with the role is subject.
   The importance of recognising the data types and grammatical relations is to provide
information in the synthesis process to choose the correct TSI. The matching of TSI will
be explained in the later section in detail. The parsed AST with compiler symbol table and
event table are shown in Fig. 9.




13
Empirical Software Engineering (2026) 31:181                                               Page 19 of 47 181




Fig. 6 Syntax-restricted sentences returned by the model for Fig. 4 using the prompt from Fig. 5 on infor-
mal specifications from Fig. 4 and the method signature from the program listed in Fig. 3




Fig. 7 The meaning representations encoded in Neo-Davidsonian event semantics derived from the sen-
tence ‘The length of the string parameter ‘inputString’ is less than or equal to 2000 and is greater than or
equal to 0.’ from Fig. 6


4.5.2 Typed Semantic Interpretation

This semantic gap arises from their differing representational paradigms: the MRs employ
Neo-Davidsonian event semantics, treating actions as events with variables and thematic
roles to abstractly link entities, whereas JML focuses on concrete program states via such
as Boolean expressions referencing parameters, \result, \old, and quantifiers directly tied to
Java program execution. We introduce the TSI, which is the template to provide information
on what and how to synthesise the JML correctly. Figure 10 shows two TSI of the predicate
‘less than or equal’, and it is used in the current implementation. Matching a TSI includes
two stages: syntax and semantics. Synthesis of a predicate with a TSI is performed if and
only if both syntax and semantics are fulfilled.
    To syntactically matching a TSI, a predicate symbol must be the same as the term of a
TSI, and the syntax of predicate is listed in the syntax list in such TSI. By the above mecha-
nism, predicate symbols can be differentiated with different syntax according to their usages
in the sentences. For instance, ‘equal’ can be a verb in ‘The array’s length is equal to 2.’ and
an adjective in ‘The array’s length is equal to 2.’.




                                                                                                  13
181 Page 20 of 47                                         Empirical Software Engineering (2026) 31:181




Fig. 8 The LR(1) grammar specifies the input MR encoded in Neo-Davidsonian event semantics. This
grammar is used in the compiler of MEARC


   To semantically matching a TSI, the subtree rooted at the predicate node is checked
against the arguments described in the TSI. Each argument consists of a symbol that can be a
grammatical role, or an asterisk (i.e. *) represents no argument is required. We leverage the
event table of each event variable as the predicate’s child to check related entity variables.
An entity variable satisfies as an argument if and only if the data type is fulfilled. The syn-
thesised type is the data type of the synthesised subtree intermediate semantic interpretation.

4.5.3 Abstract Syntax Tree Analysis

After AST is constructed, syntax checking and synthesis ordering construction is performed
to the predicates. Every predicate is checked to syntactically match a number of TSI. Predi-
cates with syntax as a cardinal number (CD) and parameter names with noun syntax are
assigned with runtime generated TSI according to their predicate symbol. If there are no
TSIs matched, a semantic interpretation not found error is thrown, and developers are
acknowledged with the TSI missing predicate symbol.
    Event predicates require the semantics from nodes associated with their event argument
variables. However, predicates in MR are written according to the lexical order in the sen-
tence. To avoid missing semantics when synthesising the event predicates, we arrange the
synthesis order of predicates with direct semantics (e.g. nouns, cardinal numbers) at the top
priority.




13
Empirical Software Engineering (2026) 31:181                                   Page 21 of 47 181




Fig. 9 The AST parsed from the MR in Fig. 7 with the grammar shown in Fig. 8




                                                                                     13
181 Page 22 of 47                                               Empirical Software Engineering (2026) 31:181

Fig. 10 Example of TSI for the predicate ‘less than or equal’




   The argument variables in the arranged predicates are marked as visited. An event
predicate is added to the synthesised order if and only if all its grammatical related entity
variables are visited. A semantic error is thrown if any predicates are not added to the syn-
thesised order after all predicates are checked. Predicates are synthesised according to the
order provided by the analysis.

4.5.4 Semantic Interpretation Synthesis

Following the synthesis order, each subtree rooted at a predicate is visited to perform the
synthesis process. Every subtree synthesis produces an intermediate semantic interpretation,
and it is associated with the argument event or entity variable (represented as ‘assigned’).
All syntheses can only be performed when all the children’s variable nodes are assigned.
There are four types of synthesis: direct, event, substitute and relative.
    A subtree satisfies the criteria for direct synthesis if it has the root’s syntactic category as
either a cardinal number or noun. The interpretation and synthesised datatype of the mapped
TSI is associated with the entity variable’s compiler symbol. The whole subtree is then
removed from the AST. Figure 11 shows the example AST after direct synthesis.
    A subtree with a ‘Rel’ predicate is subjected to relative synthesis. The subtree must have
two children, with one having a relative interpretation (i.e. starting with ‘__REL__’). A TSI
syntax matching is performed with the relative interpretation as a symbol, and semantic
matching is performed by using the data type of its sibling node as the argument data type.
The synthesised semantic interpretation replaces the relative interpretation, and the subtree
is pruned. Figure 12 shows the example AST after relative synthesis.
    A subtree satisfies the criteria for event synthesis if it has only one leaf representing an
event variable. To synthesise this subtree, the grammatical relations are retrieved from the
event table. Semantic matching is performed to check if the syntactical matched TSI has
argument matching with the current argument variables from the event table. The synthe-
sised semantic interpretation is stored in the symbol table of the event variable, and the child
node is removed. The predicate maintains a pointer to the symbol table of the event variable,
and the predicate node is marked as synthesised. Figure 13 shows the example AST after an
event is synthesised.




13
Empirical Software Engineering (2026) 31:181                                Page 23 of 47 181




Fig. 11 The AST after applying direct synthesis on applicable subtrees


4.5.5 Code Generation

After synthesising all the predicates, a post-order traversal is performed to remove the quan-
tifier nodes and connective nodes (i.e. and, or, etc.) without synthesised nodes. The simpli-
fied AST is then ready for code generation. The process starts at the AST root node by
calling the output method, which recursively traverses every node by calling the walktree
method. If a null node is encountered, an error is recorded, and the code generation fails
with an error thrown.
    The code emission is performed by calling the printree method to extract the TSI associ-
ated with the synthesised node. When a connective node is visited, the walktree method is
called on its left subtree, followed by resolving the target operator code (e.g. &&, ||), and
then calling the walktree method on the right subtree. Figure 14 shows the output JML after
synthesis.


5 Testing and Evaluation

Multiple experiments are set up to evaluate HAFIS. Each experiment is a comparison
between an approach and HAFIS. To analyse the results objectively, metrics are derived in
this section.




                                                                                  13
181 Page 24 of 47                                              Empirical Software Engineering (2026) 31:181




Fig. 12 The AST after applying relative synthesis on applicable subtrees



5.1 Experimental Setup

To evaluate HAFIS, it is essential to have a dataset that includes both natural language
specifications and corresponding program implementations. Both elements are necessary
because HAFIS focuses on translating natural language specifications into JML with the


13
Empirical Software Engineering (2026) 31:181                                                          Page 25 of 47 181




Fig. 13 The AST after applying event synthesis on applicable subtrees


method signature information. The goal of obtaining JML specifications is to verify them
against their respective program implementations. Therefore, we have searched the open-
source repositories that meet the above criteria.
   A real-world dataset containing 84 programs is chosen from an open-source code reposi-
tory which contains codes for LeetCode problems ​(​h​t​t​p​s​:​/​/​g​i​t​h​u​b​.​c​o​m​/​j​a​v​a​d​e​v​/​L​e​e​t​C​o​d​e​-​i​n​


                                                                                                               13
181 Page 26 of 47                                             Empirical Software Engineering (2026) 31:181




Fig. 14 The AST after the synthesis and generates the output JML



-​J​a​v​a​​​​)​. Each program has its complicated informal specification written in a file. These pro-
grams are accepted by the LeetCode programming platform, and they have been rigorously
evaluated with test cases in the platform. Therefore, they are initially correct regarding the
test cases written based on the informal specifications.
      These programs are chosen because of their diversity in data types. In terms of data types,
we have chosen these programs due to their complexity in the mixing of different param-
eters and return data types. For instance, there are programs accepting strings and returning
boolean or integer. Once the JML is generated and accepted by the theorem prover, the data
types of both the parameters and return of the method must be consistent with the program.
      The chosen programs are representative of programming topics. For instance, hamming
distance, parentheses validation and removal, as well as reversing integers are very common
methods in software engineering. To avoid bias and mistakes in theorem proving, we tend
to choose self-contained programs such that there are no JML needed to be written for the
dependent methods. Loop invariants are added manually to all programs in order to facili-
tate formal verification. Therefore, rejecting the JML reflects the faults found in the method.
      The prompt listed in Fig. 5 is used in the experiment. All chosen programs are not used in
the example section of the prompt. There are 18 shots written in the example section for the
LLM to follow in restricting the syntax of the input natural language specifications to strictly
adhere to the formal grammar in the compiler. The experiment has been performed in mod-
els of Claude-4 Opus, o3, GPT-3.5 and StarCoder2. Table 8 lists the capabilities of the mod-
els used in the experiment. All models use the same prompt. The temperature parameters of
Claude-4 Opus, o3, GPT-4o and GPT-3.5 are set to zero, and that of StarCoder2 is set to 0.1.
      Each program has the corresponding informal specification. To prepare the experiment
of the pure grammar-based approach, we use the common tokenisation method of using
periods (‘.’) to break these informal specifications. There are 1697 sentences found in these
84 program informal specifications. For the pure LLM and HAFIS approaches, every infor-




13
Empirical Software Engineering (2026) 31:181                                        Page 27 of 47 181


Table 8 The capabilities of the      Model                                 Capabilities
LLMs used in the experiment
                                     GPT-3.5                               General-purpose
                                     GPT-4o                                General-purpose
                                     o3                                    Coding task solving, rea-
                                                                           soning and problem-solving
                                     StarCoder2                            Coding task solving
                                     Claude-4 Opus                         Coding task solving, rea-
                                                                           soning and problem-solving


mal specification is directly used as the input. To evaluate the HAFIS, derivation accuracy,
translation accuracy and specification average mutation score metrics are considered.
   For both the pure grammar-based and HAFIS, MR is needed for the later translation.
The derivation accuracy measures the proportion of informal specifications that are derived
into correct MRs regarding the syntax and reduction completeness of MRs. The design of
ccg2lambda (Martínez-Gómez et al. 2016) fails by providing no output MR if semantic
composition fails to map a lambda calculus template for a tree leaf. Therefore, the metric of
derivation accuracy is computed as follows:
                                                       mrcorrect
               accuracyderivation =
                                          mrcorrect + mrnooutput + mrincorrect                    (1)


The translation accuracy measures the proportion of translated specifications that are cor-
rect regarding the syntax and semantics of JML, which is checked by using OpenJML (Cok
2011). To prevent double counting, JMLs that are identical in syntax and semantics within
a program specification set are counted only once. To calculate the translation accuracy of
the pure LLM approach, we divide the number of syntax and semantic correct JML by the
number of lines returned by the LLM. As we have clearly commanded the LLM to translate
the input informal specifications into JML, all the return lines should be counted as JML
specifications. The metric of translation accuracy is computed as follows:

                                                              jmlcorrect
          accuracytranslation_haf is =                                                            (2)
                                               jmlcorrect + jmlincorrect + jmlnooutput

                                                            jmlcorrect
                             accuracytranslation_llm =                                            (3)
                                                             jmltotal

The average mutation score metric refers to the ability of finding bugs in the programs. The
metric is computed as the average number of mutants killed by the theorem prover using the
generated JML specifications. The mutants are produced by using Major mutation frame-
work (Just 2014) with a set of mutation operators shown in Table 9. A mutant is killed if
at least one new error is found in the verification of mutant. A mutation score is computed
based on the number of mutants generated from a program that are killed by the theorem
prover with the corresponding set of JML specifications, as follows:

                                                      {impl ∈ M |impl ⊭ c}
                      MutationScore(c, M ) =                                                      (4)
                                                              M



                                                                                           13
181 Page 28 of 47                                             Empirical Software Engineering (2026) 31:181


Table 9 Mutation operators and     Mutation           Label    Description                       Num-
the number of mutants produced.    operator                                                      ber of
All mutants are subjected to the                                                                 mutants
mutation analysis
                                   Arithme-           AOR      Replaces a binary arithmetic      976
                                   tic operator                operator with compatible
                                   replacement                 alternatives.
                                   Conditional        COR      Replaces a conditional opera-     306
                                   operator                    tor with compatible alterna-
                                   replacement                 tives. Also replaces atomic
                                                               boolean conditions with true
                                                               and false.
                                   Logical operator LOR        Replaces a binary logical         6
                                   replacement                 operator with compatible
                                                               alternatives.
                                   Operator re-       ORU      Replaces a unary operator with    8
                                   placement unary             compatible alternatives.
                                   Relational oper-   ROR      Replaces a relational operator    989
                                   ator replacement            with compatible alternatives.
                                   Shift operator     SOR      Replaces a bit-shift operator     16
                                   replacement                 with compatible alternatives.
                                   Statement          STD      Deletes (omits) a single state-   387
                                   deletion                    ment of the following kind:
                                                               return, break, continue, method
                                                               call, assignment, pre/post
                                                               increment and decrement


Then, the average mutation score is computed as follows:
                                                  ∑k
                                                      i=1 MutationScore                               (5)
                        MutationScoreavg =
                                                              k

where k is the number of programs in the dataset, c is the JML specification and M is the set
of mutants generated from the program implementation.


6 Results and Discussion

This section provides the results and discussions of applying HAFIS, pure grammar-based
and pure LLM approaches on the chosen dataset.

6.1 How Effective is using an LLM in Improving the Derivation of MRs from Informal
Specifications, Namely by Restricting the Syntax of Informal Specifications?

Table 10 shows the MR derivation results of applying HAFIS and the pure grammar-based
approach on the specifications and programs which compose the dataset. Starting with 1697
distinct sentences, the pure grammar-based approach attempts an MR derivation for each
one, while HAFIS begins by restricting the syntax of the sentences and, as one can observe,
the intermediate number of syntax-restricted sentences is lower and depends on each spe-
cific LLM.




13
Empirical Software Engineering (2026) 31:181                                    Page 29 of 47 181


Table 10 Derivation accuracy         Approach                 Number of   Number of     Derivation
results for pure grammar-based                                sentences   MRs derived   accuracy
and HAFIS to construct MRs
                                     Pure grammar-based       1697        426           23%
for the dataset’s 1697 distinct
sentences                            HAFIS with GPT-3.5       488         486           99%
                                     HAFIS with GPT-4o        561         561           100%
                                     HAFIS with o3            622         606           97%
                                     HAFIS with StarCoder2    736         731           99%
                                     HAFIS with Claude-4-Opus 700         695           99%


   The pure grammar-based approach derived 426 meaning representations out of 1697
sentences, therefore handling 23% of the cases. Failures to construct MRs are due to the use
of complex phrases (e.g. “if and only if”, “is true”), mathematical symbols (e.g. ‘-’ and ‘+’)
and program expressions (e.g. “c = a + 1”). Consequently, the derivation accuracy of the
pure grammar-based approach is only 23%, and this result validates our observation that a
purely symbolic approach lacks the accuracy needed to handle intricate natural language,
thereby leading to HAFIS.
   For the results of HAFIS, the LLMs generate syntax-restricted sentences based on infor-
mal input specifications. GPT-4o produced a total of 561 sentences, all of which can be
derivable into MRs. GPT-3.5 returned 488 sentences, of which 486 were derivable into
MRs. The two instances of failure can be attributed to ccg2lambda (Martínez-Gómez et al.
2016) lacking adequate support for relative pronouns (e.g. ‘whose’ and ‘whom’).
   o3 returned 622 sentences, of which 606 were derivable into MRs. There are five sen-
tences that have reached the limitation of words in the C&C parser, such that the parser
had failed to derive the CCG trees. The rest of them have used relative pronouns, which
ccg2lambda has limited support in its templates.
   StarCoder2 generated 736 syntax-restricted sentences, with 731 of those successfully
being converted into MRs. This results in over 99% accuracy, which is a promising outcome
given that it is a comparatively smaller open-source model. Among the five instances of
failure, four involved the use of ‘there’ to convey existential meaning, which ccg2lambda
struggles to manage within complex sentence structures. These failures indicate that future
research could enhance the prompt with additional examples to enable LLMs to produce
sentences which avoid unsupported terms. The final failure from StarCoder2 occurred due
to an incomplete sentence, as the LLM failed to prevent itself from repetitively generating
the same sentence.
   Claude-4 Opus returned 700 sentences, and 695 of them were derivable into MRs. Among
the five instances of failure, four involved the use of implicit conjunctions (e.g. The values
of the integer array parameter ‘x’ are equal to 5, 10, or 20.). These failures suggest that the
prompt can be enhanced with additional examples to enable LLMs to produce sentences
with explicit conjunctions. The final failed instances are due to the use of relative pronouns.
   The experimental results demonstrated that HAFIS maintains high effectiveness across
different LLMs, with both industrial and open-source models achieving 97-100% derivation
accuracy. These results have demonstrated the generality of the approach as these models
consist of both industrial and open-source models. The improvement in derivation accuracy
from 23% to at most 100% provides a positive answer to RQ1 that it is effective to use an
LLM to improve MR derivation namely using syntax restriction on informal specifications.




                                                                                        13
181 Page 30 of 47                                           Empirical Software Engineering (2026) 31:181


6.2 How Effective is using an LLM in Improving the Translation of Informal
Specifications into JML by Disambiguating the Parameters and Identifying the
Datatypes of Parameters and Method Return Types?

Table 11 shows the results of translating informal specifications into JML applying pure
grammar-based, pure LLM and HAFIS on the dataset. Out of 426 MRs from pure grammar-
based approach, there is only a single JML successfully generated. The reason is that the
syntax and semantics of these MR are not accepted by the formal-grammar used in the
MEARC. The design of the synthesis rules in MEARC greatly follows declarative sentence
structure with subject, predicate and object, such that the resulting MR can be derived into
event described predicates. However, most of the sentences in the informal specifications do
not follow this sentence structure.
   In terms of translation accuracy, HAFIS has outperformed the pure LLM approach in the
corresponding models. The integration with GPT-4o has the highest translation accuracy of
88%, while the integration with StarCoder2 has provided the highest quantity of correctly
translated JML.
   Incomparable datatypes are present in certain sentences where no JML is translated. For
example, the statement ‘a string parameter x is equal to 1’ cannot be translated because
there are no operators available between string and integer in JML. In the integration with
GPT-3.5, 11 out of 96 failed cases involved incomparable datatypes. For the integration with
GPT-4o, 1 out of 88 failed cases displayed the same issues. In the integration with o3, 2
out of 208 failed cases involved incomparable datatypes. For the integration with Claude-4
Opus, 7 out of 157 failed cases found using incomparable datatypes. Meanwhile, in the
integration with StarCoder2, 30 out of 149 failed cases involved incomparable datatypes.
These findings indicate that type checking is effective in identifying incorrect informal
specifications.
   The remaining failed cases without translated JML are a result of lacking adequate infor-
mation in the informal specifications. Terms such as ‘words’ and ‘zigzag’ are used to rep-
resent programming structures in the sentences. However, their meanings can vary based


Table 11 The translation accuracy results of applying the pure grammar-based, pure LLM and HAFIS on
the dataset
Approach             Model               No. of JML cor- No. of JML No. of translation Translation
                                         rectly translated incorrectly has no output     accuracy
                                                            translated
Pure                 N/A                 1                  0           0                0%
grammar-based
                     GPT-3.5             509                302         0                62%
                     GPT-4o              172                40          0                81%
Pure LLM             o3                  279                103         0                73%
                     StarCoder2          4                  6           0                40%
                     Claude-4 Opus       467                137         0                77%
                     GPT-3.5             379                11          96               77%
                     GPT-4o              496                3           62               88%
HAFIS                o3                  413                1           208              66%
                     StarCoder2          563                19          149              76%
                     Claude-4 Opus       541                2           157              77%



13
Empirical Software Engineering (2026) 31:181                               Page 31 of 47 181


on the specific context of the programs. These observations suggest that the examples pre-
sented in the prompt could be refined to offer more guidance to LLMs, enabling them to
articulate complex terms into phrases that provide program behavioural descriptions.
    The incorrectly translated JML is caused by LLMs returning inconsistent datatypes
regarding to the programs. By observation, these cases are found when inconsistent param-
eter names are used between the informal specifications and programs, for instance, ‘s’
is being mentioned in the informal specification but ‘str’ is applied in the program. Their
datatypes can be correct such that type checking is passed. These cases are caught by using
OpenJML (Cok 2011) to check the syntax and semantics of JML specifications regarding
the programs.
    The result of purely using StarCoder2 has provided a few JML specifications. The model
has returned a large amount of explanations and examples, as well as implementations for
the input informal specifications. 4 out of 10 returned JML specifications are correct regard
to JML syntax and semantics. The result suggests that StarCoder2 requires training with
specific corpora to generate the target JML.
    Both o3 and Claude-4 Opus have returned a relatively high quantity of JML specifica-
tions. The incorrectly translated JMLs have referred to undeclared methods or JML model
methods with incorrect syntax. The result suggests that additional corpora are required in
training the models to generate correct model methods.
    In contrast, using GPT-4o purely has returned 172 correct JML specifications out of 212
lines. GPT-4o has provided hallucinations in using undeclared methods and non-existing
JML syntax and semantics. Purely using GPT-3.5 has outperformed the other models in
translating the informal specifications into JML. The result suggests that fine-tune training
is required for the models to provide correct JML.
    The above results provide that HAFIS integrating with GPT-4o has the highest transla-
tion accuracy of 88%. In terms of quantity, HAFIS integrating with StarCoder2 has pro-
vided more JML specifications. Challenge 1 has been addressed, with the support from
the translation accuracy improving from 0% to 88% by comparing the results of the pure
symbolic approach and HAFIS. The high translation accuracy also supports that Challenge
2 is mitigated by using explicit syntax of method parameter and return in distinguishing the
pre/postconditions.
    Using HAFIS with StarCoder2 has the highest number of correctly translated JML with
24% of failed sentences. Comparing to the pure LLM approach using GPT-3.5, it has 38%
of failed sentences while it provides the highest number of correctly translated JML in the
pure LLM approach. This provides that Challenge 3 is resolved by using HAFIS with the
knowledge base of TSI.
    While HAFIS integrated with GPT-4o that is a general-purpose LLM delivered the high-
est translation accuracy at 88%, domain-specialised LLMs like StarCoder2 (trained with
programming corpora) generated a higher number of sentences, suggesting that general-
purpose LLMs produce more number of grammar-compliant outputs with a lower number
of sentences. The results also show that LLMs with reasoning capability can be integrated
with the proposed method. Claude-4 Opus has produced the second highest number of sen-
tences with translation accuracy at 77%, while o3 returned a lower number of sentences
with the lowest translation accuracy.
    All models have successfully restricted syntax to match the formal grammar and cor-
rectly identified parameter and method return types using only method signatures. The


                                                                                 13
181 Page 32 of 47                                               Empirical Software Engineering (2026) 31:181


above results show that HAFIS can be successfully integrated with LLMs regardless of
their capabilities to provide the translation.
   The result supports that using an approach of combining an LLM with a grammar-based
improves the translation from informal specifications into syntactically and semantically
correct JML up to 88%. The RQ2 is positively answered that using an LLM can improve
the translation from informal specifications into JML by disambiguating the parameters and
identifying the datatypes of parameters and method return types.

6.3 How Effective is the HAFIS-Generated JML in Finding Defects Compared to the
Pure LLM Approach Generated JML?

To investigate the quality of the generated JML, mutation analysis is performed to check
whether the generated JML can find defects in the mutated programs. This technique con-
sists of producing defective programs, by mutating the original source code, and running
some verification method (in our case theorem proving) to determine the mutation score,
that is, the proportion of mutants that are identified. There are 2688 mutants being produced.
Figure 15 illustrates the flow of the mutation analysis in obtaining a mutation score.
   Results (see Fig. 16) show that HAFIS has outperformed the pure LLM approach in all
five models. The highest average mutation score of 0.44 is the JML translated from HAFIS
with both o3 and Claude-4 Opus. HAFIS integrating with GPT-3.5 has a relatively low aver-
age mutation score of 0.36, and the lowest average mutation score is 0.006 from pure LLM
approach using StarCoder2. These results show that using HAFIS with these models can
generate JML killing more mutants.
   To further investigate the average mutation score in finding defects using the translated
JML, we analyse the mutants killed by both HAFIS and pure LLM approach using each
model. Figures 17, 18, 19, 20 and 21 show the analysis of mutation scores for both pure
LLM and HAFIS using the same model, as well as the mutation scores of the mutants killed
in union and intersection set. Each sample in these plots represents a the mutation score of a
program. We aim to further analyse whether there is a complementary relationship between
the JML translated from these two approaches.




Fig. 15 The flow of mutation analysis for method contracts. A set of mutants are generated by the Major
framework using the set of mutation operators listed in Table 9. The generated mutation score is the num-
ber of mutants killed by the theorem prover


13
Empirical Software Engineering (2026) 31:181                                        Page 33 of 47 181




Fig. 16 The comparison of average mutation score metrics from HAFIS and pure LLM approach with
five LLMs. The orange bars represent the HAFIS approach, while the blue bars represent the pure LLM
approach. Each approach has been applied to integrate with each of these models to provide the above
visualisation


   Figure 17 shows the analysis of mutation scores from using GPT-3.5 with the two
approaches, and the mutation scores of killed mutants union and intersection sets. The
results show that HAFIS has contributed a higher portion in the union set. Nevertheless,
there exists a significant portion of killed mutants not in the intersection set. Therefore,
applying the JML translated from using GPT-3.5 in both approaches in finding defects can
be a complementary effect.
   Figure 18 shows the analysis of mutation scores from using GPT-4o with the two
approaches, and the mutation scores of killed mutants union and intersection sets. Results
show that HAFIS has dominated in killing mutants because the mutation scores of HAFIS
and union set are close. The intersection has a low score with very few outliers. There-
fore, using the JML translated from pure LLM with GPT-4o does not help much in killing
mutants comparing to those from HAFIS using the same model.
   Figure 19 shows the analysis from using StarCoder2. As pure LLM using StarCoder2 has
returned a few JML, the intersection is low as expected with a very few outliers. The muta-
tion scores of the JML from HAFIS and the union set are almost the same. Therefore, using
HAFIS with StarCoder2 contributes to almost all mutants killed in the union set.
   Figure 20 shows the analysis of mutation scores from using o3 with the two approaches,
and the mutation scores of killed mutants union and intersection sets. The pure LLM using
o3 has returned a few correct JML specifications, and the intersection is very low with a few
outliers. The mutation scores of HAFIS and the union set are close. Therefore, the result
indicates that HAFIS has contributed to most of the mutants killed.


                                                                                           13
181 Page 34 of 47                                              Empirical Software Engineering (2026) 31:181




Fig. 17 An analysis with mutation score is performed on HAFIS and pure LLM approach using GPT-3.5.
The union represents the mutation scores of the union set of killed mutants. The intersection represents
the mutation scores of the intersection set of killed mutants

    Figure 21 shows the analysis from using Claude-4 Opus. Both approaches using Claude-4
Opus have returned a high quantity of correct JML specifications. Comparing to the other
models, the intersection is relatively high. Besides, both mutation scores of from the two
approaches are close, with HAFIS having a slightly higher mutation score. Therefore, the
result indicates that HAFIS has contributed to most of the mutants killed, but the pure LLM
approach using Claude-4 Opus can also help in finding defects.
    The results show that LLM capability differences primarily affect the quality of JML gen-
erated by HAFIS, with both o3 and Claude-4 Opus achieving 0.44 average mutation score
compared to other models from 0.36 to 0.41. These results indicate that more advanced
reasoning capabilities in newer LLM integrated with HAFIS produce JML specifications
with slightly better defect detection ability.
    The mutation analysis with theorem proving and JML semantics checking with Open-
JML (Cok 2011) has provided the support to guarantee the semantic correctness of the
generated JML. The generated JML can only be correct regarding the semantics if and only
if the MR is semantically correct. Based on the above observations, HAFIS generated JML
outperforms that of the pure LLM approach, namely finding defects in programs. The result
supports a positive answer for RQ3 that the generated JML specifications from HAFIS are
more effective in finding defects than that of the pure LLM approach.




13
Empirical Software Engineering (2026) 31:181                                           Page 35 of 47 181




Fig. 18 An analysis with mutation score is performed on HAFIS and pure LLM approach using GPT-4o.
The union represents the mutation scores of the union set of killed mutants. The intersection represents
the mutation scores of the intersection set of killed mutants

7 Ablation Study

To investigate the robustness of HAFIS to LLM variability, an ablation study was performed
to compare the derivation and translation accuracy of the proposed approach with the use of
intentionally degraded shots.
   To provide better, we changed the 18 shots that were included in the prompt sent to the
LLM. Specifically, we prepared an experiment with two different prompts:

● A prompt with 18 shots that were from newspaper articles.
● A prompt with nine shots from the newspaper articles and the rest of them were ran-
  domly selected from the original shots used in the syntax restriction.

The newspaper articles were chosen to provide context that are unrelated to the software
engineering domain.
   The experiment was performed using the model of o3. The temperature parameter was
set to zero. The same dataset of 84 programs with their informal specifications was used in
the experiment. The same metrics of derivation accuracy and translation accuracy were used
to evaluate the performance of HAFIS with the two different prompts.




                                                                                              13
181 Page 36 of 47                                               Empirical Software Engineering (2026) 31:181




Fig. 19 An analysis with mutation score is performed on HAFIS and pure LLM approach using StarCod-
er2. The union represents the mutation scores of the union set of killed mutants. The intersection repre-
sents the mutation scores of the intersection set of killed mutants

    Table 12 shows the derivation accuracy results of the proposed approach with two differ-
ent prompts in the ablation study with o3 to construct MRs for the LLM-returned sentences.
The derivation accuracy with both prompts is high, with 92% and 98% respectively. The
high derivation accuracy indicates that mostly the LLM-returned sentences are derivable
into MRs by using ccg2lambda (Martínez-Gómez et al. 2016). The reason is that the news-
paper articles are well-written and the sentences are in declarative structure.
    Table 13 shows the translation accuracy results of applying the proposed approach with
the two prompts in the ablation study with o3. The translation accuracy with the prompt
using all unrelated shots is 0%. The proposed approach has detected the sentences returned
from the LLM with all shots unrelated to syntax restriction. These sentences are not accept-
able by MEARC, because no shots provide the syntax of the formal-grammar and the sup-
port of identifying the datatypes of parameters and method return types. Regarding the
result from using 9 related and 9 unrelated shots, the translation accuracy is 58% comparing
to the translation accuracy of 66% from using all related shots (see Table 11). The difference
in translation accuracy shows that there are sentences that require those replaced shots for
the LLM to produce syntax-restricted sentences that are acceptable by MEARC.
    The results of the ablation study show that HAFIS is robust to LLM variability, as the
sentences returned from using all unrelated shots are detected by the proposed approach.
Therefore, challenge 4 is mitigated by using the proposed approach.




13
Empirical Software Engineering (2026) 31:181                                           Page 37 of 47 181




Fig. 20 An analysis with mutation score is performed on HAFIS and pure LLM approach using o3. The
union represents the mutation scores of the union set of killed mutants. The intersection represents the
mutation scores of the intersection set of killed mutants

8 Limitations and Threats to Validity

The proposed approach utilizes explicit terms (i.e. ‘parameter’ and ‘result’) in informal
specifications to distinguish between preconditions and postconditions. This concept is valid
because specifying the result of a method in the preconditions can lead to syntax errors. As
a result, we have excluded sentences without explicit terms, as more advanced methods
are necessary to classify these sentences effectively. There is a need for research in natural
language inference with sentiment analysis to evaluate these sentences as hypotheses that
derive from the complex syntax of informal specifications treated as premises.
    To emphasize the necessity of advanced methods for distinguishing between precondi-
tions and postconditions, we refer to row 8 in Table 2, along with the explanations provided
in Challenge 2 in Section 3. The complexity of the task highlights that significant research
effort is still needed since even the involvement of LLMs cannot guarantee task completion.
Therefore, using explicit terms as indicators to convey information about preconditions and
postconditions is essential for automating the translation from natural language to JML.
    The informal specifications present in the dataset are well-articulated and have under-
gone review by the coding platform. The prompt examples utilized in the experiment exhibit
a diverse range of syntactical structures. The LLMs have demonstrated an understanding
of the syntax within the informal specifications and have adhered to the directives outlined
in the prompts to generate statements that conform to restricted syntax. Furthermore, there




                                                                                              13
181 Page 38 of 47                                              Empirical Software Engineering (2026) 31:181




Fig. 21 An analysis with mutation score is performed on HAFIS and pure LLM approach using Claude
4 Opus. The union represents the mutation scores of the union set of killed mutants. The intersection
represents the mutation scores of the intersection set of killed mutants


Table 12 Derivation accuracy results of HAFIS in the ablation study with o3 to construct MRs for the LLM-
returned sentences. ‘Number of shots related’ refers to the number of shots are from the shots used in the
syntax restriction (see Fig. 5)
Number of shots related         Number of sentences     Number of MRs derived        Derivation accuracy
0                               256                     235                          92%
9                               604                     590                          98%



Table 13 Translation accuracy       Number of No. of JML          No. of        No. of trans- Translation
results of applying HAFIS in the    shots related correctly       JML           lation has no accuracy
ablation study with o3                            translated      incorrectly   output
                                                                  translated
                                    0             0               0             0             0%
                                    9             350             0             254           58%


exist research opportunities to employ LLMs in the revision of poorly written informal
specifications.
   The proposed approach focuses on translating informal specifications into method-level
JML specifications. To ensure the consistency of generated JML with the programs in the
dataset, including loop invariants is necessary to facilitate additional verification of loop
correctness. The authors have added these loop invariants to each program in the dataset


13
Empirical Software Engineering (2026) 31:181                                         Page 39 of 47 181

Fig. 22 An example postcondi-
tion does not refer to the method
return directly



manually. The task of inferring loop invariants from informal specifications is recognized
as a direction for future work.
   Distinguishing preconditions and postconditions can be difficult. The design of JML has
indicated that the result of a method (i.e. \result) can only be used in a postcondition (i.e. an
ensures clause). Based on this concept, the proposed approach has suggested the use of
explicit syntax of ‘parameter’ and ‘result’ to mitigate the situation. There can be other cases
to specify a postcondition without referring to the method return. For instance, Fig. 22
shows an example that a postcondition can be written following the syntax in the prompt
without specifying the method return. Future research opportunity can be to study how to
accurately acquire pre/postconditions using LLM.
   The field of LLM is rapidly evolving, and the models used in this paper can be advanced
in a short period of time. The LLM may return sentences that are richer in the context related
to other domains according to the training data. The proposed approach only relies on the
LLMs to return sentences that are restricted to the syntax of the compiler, with careful
instructions in the prompt. We have enclosed results from both industrial and open-source
LLMs to demonstrate that the proposed approach can be applied to different models. Future
work can be conducted to investigate the impact of different LLMs that are trained with
completely different corpora to provide advanced observations.
   This paper focuses on accurately translating natural language into formal specifications.
LLMs are integrated to return syntax restricted sentences to broaden the language accep-
tance of the symbolic NLP approach. The number of sentences generated is lower than the
original number because the LLMs are instructed to strictly follow the examples given in the
prompt. Future work can be on investigating the factors that change the quality and quantity
of sentences produced by the LLM, for instance, the number of examples in the prompt.
   The experimental results have demonstrated that the proposed approach can effectively
collaborate with both industrial and open-source LLMs. However, the non-deterministic
nature of LLMs can produce similar phrases that convey the same meaning. Table 14 show
that two sentences with different syntax have the same meaning. These two sentences should
be translated into the same JML as “array.length == 2”. One can expand the TSI knowledge
base to support the compilation process, subsequently building a reusable knowledge base.
   Various training methods and corpora can influence the output of LLMs. The StarCoder2
model is a code LLM trained with some programs, while the GPT models are considered
more general purpose without knowing all the details in the training corpus. The knowledge

Table 14 Two sentences refer         Informal specification     Corresponding meaning representation
to the same semantic can be writ-
                                       The array has a length   exists x.(_array{NN}(x) & exists z2.(_
ten differently. Their meaning
                                               of 2.            length{NN}(z2) & exists z1.(_2{CD}
representations show that their
                                                                (z1) & exists e.(_of{IN}(e,z1) &
internal predicates are associated
                                                                (Subj(e) = z2))) & exists e.(_have{VBZ}
differently
                                                                (e) & (Subj(e) = x) & (Acc(e) = z2) )))
                                      The length of the array   exists x.(_length{NN}(x) & exists
                                               is 2.            z1.(_array{NN}(z1) & exists e.(_of{IN}
                                                                (e,z1) & (Subj(e) = x))) & exists
                                                                e.(_2{CD}(e) & (Subj(e) = x)))


                                                                                            13
181 Page 40 of 47                                       Empirical Software Engineering (2026) 31:181


of these models are growing because they can be kept training with different sources. There-
fore, we expect the LLMs are improved in the near future such that repeating the experiment
in this paper can obtain better results.
    The proposed approach addresses the need to check that the MR encoded in Neo-David-
sonian semantics are semantically correct by using TSI, which we introduce when convert-
ing MR to JML (see Section 4.5.2). A TSI acts as a bridge between two different logical
systems: the Neo-Davidsonian event semantics used in MRs and the first-order logic used
in JML. It does so by providing template-like functions that perform type checking, scope
checking and argument validation, though a recursive traversal of the AST.
    Each TSI template defines the following components: predicate symbols, syntactic cat-
egories, argument definitions with thematic roles (e.g. Subject, Dative), data types, and
interpretation types. This ensures that predicates are checked in two ways: they must match
syntactically and be validated semantically against method signatures and event relation-
ships. If there’s a mismatch, the translation halts to prevent creating invalid JML.
    This two-stage checking process ensures that the MR’s logical structure accurately cap-
tures what the original informal specification intended. Our evaluation results support this:
we achieved high consistency rates with OpenJML and z3 verifications, and our approach
performed well in mutant-killing tests. This shows we’re ensuring semantic accuracy, not
just correct syntax.
    The semantic correctness of the MRs derived from syntax-restricted informal specifications
is not formally proven equivalent to the original inputs due to the inherent challenges of natu-
ral language ambiguity and the probabilistic nature of NLP parsing, even with state-of-the-
art tools like ccg2lambda. Instead, we establish empirical confidence in MR fidelity through
a multi-faceted evaluation pipeline: first, manual expert assessment on a public dataset of
real-world informal specifications confirms that 88% of HAFIS-generated JMLs accurately
capture the intended semantics, implying upstream MR reliability given the deterministic,
rule-based translation via TSI templates. Second, consistency checks using OpenJML and the
Z3 theorem prover validate the logical soundness of the JML, which, per our compiler design,
directly relies on MR semantic integrity – any MR deviation would manifest as verifiable
inconsistencies or failed proofs. Finally, mutation analysis demonstrates that HAFIS-derived
JML effectively kills mutants in corresponding Java programs at higher rates than baselines,
substantiating that the MRs preserve the behavioral intent of the informal specs without formal
equivalence proofs, as such proofs remain intractable for unrestricted NLP but are approxi-
mated through these rigorous empirical proxies.
    The ground truth for the correct semantics of programs in our evaluation is based upon
the public dataset of real-world informal specifications, where the original Java programs
are selected as correct implementations that align with the intended behaviors described
in natural language provided by the LeetCode platform. This correctness is established
through a combination of expert manual validation and rigorous deductive verification. In
contrast, mutated versions introduce deliberate faults via the Major framework’s operators,
serving as negative controls that should fail verification, thereby allowing mutation scores
to empirically validate that the JML captures the true semantics.




13
Empirical Software Engineering (2026) 31:181                                   Page 41 of 47 181


9 Related Work

This paper focuses on automated formalising informal specifications into JML specifica-
tions. Recent works (Wu et al. 2022; Zhou et al. 2024; Janßen et al. 2024; Endres et al. 2024;
Poiroux et al. 2024; Cosler et al. 2023) in this area have provided approaches using purely
LLM in translating informal specifications into formal statements. SpecGen (Ma et al. 2024)
provides output in JML format using pure LLM approach. Houdini (Flanagan and Leino
2001) and Daikon (Ernst et al. 2007) infers JML from program implementations. AutoSpec
(Wen et al. 2024) analyses C programs with natural language specifications and cooperates
with an LLM to output formal specifications in ACSL format. Xie et al. (2022) provides
deductive verification on neural network with a newly introduced logical specification lan-
guage. Our work introduces a combination of LLM and symbolic NLP to translate infor-
mal specifications into formal specifications of JML format with only the method signature
information, and pure LLM approach results are provided as a baseline for comparison.
   Other works (Konrad and Cheng 2005; Kress-Gazit et al. 2008; Di Guglielmo et al. 2010;
Gavran et al. 2020; Yan et al. 2015; Autili et al. 2015; Wang et al. 2018; Blasi et al. 2018;
Zhang et al. 2020; Zhang and El-Gohary 2022; Wang et al. 2020, 2021; Bombieri et al. 2023;
Norheim and Rebentisch 2024) have provided symbolic approaches to formalise informal
specifications by using structured models/natural language and internal predefined rules. FRET
(Farrell et al. 2022) translates structured natural language into formal specifications, however,
the output does not support quantification that is supported by JML. ARSENAL (Ghosh et al.
2014) is closely related to the symbolic approach used in this paper, nevertheless, the input and
output format, as well as complexity are different. DDPSL (Di Guglielmo et al. 2010) accepts
a series of descriptions related to events and translates them into Property Specification Lan-
guage. Other works (Kress-Gazit et al. 2008; Yan et al. 2015; Autili et al. 2015; Konrad and
Cheng 2005; Bombieri et al. 2023; Wang et al. 2021) translate with structured natural language
into temporal logic formats. Our work provides the symbolic approach results as a baseline to
compare with the proposed approach that combines LLM and symbolic approaches.
   Our work provides comparisons of the JML generated from both the proposed approach
and pure LLM approach. Other works have used purely the LLM to generate formal speci-
fications in different formats, such as JML (Ma et al. 2024; Endres et al. 2024), ACSL (Wen
et al. 2024), Propositional Projection Temporal Logic (Li et al. 2022), computation tree
logic (Zrelli et al. 2025) and temporal logic (Hahn et al. 2022; Cosler et al. 2023; Pan et al.
2023; Xu et al. 2024; Barrientos et al. 2024). We have considered that these are pure LLM
approaches and obtained results from both industrial and open-source LLMs.
   Our work accepts informal specifications by using a prompt that can be accepted by
LLM. Recent works such as C2S (Zhai et al. 2020) and Baldur (First et al. 2023) perform
the translation by retraining a model. To repeat these works to support much broader lan-
guage acceptance, specific corpora and retraining time are required. This paper introduces
an approach that can provide broad language acceptance without the need of specific cor-
pora and time for retraining a model.
   Regarding extracting structured natural language requirements, there are works (Grunske
2008; Cobleigh et al. 2006; Autili et al. 2007; Tiwari et al. 2022) that have provided




                                                                                     13
181 Page 42 of 47                                        Empirical Software Engineering (2026) 31:181


approaches to extract the information from informal specifications. Grunske (2008) have
provided a structured English grammar to facilitate property specification through a natu-
ral language interface. Cobleigh et al. (2006) have introduced an approach that requires
engineers to select the proper template to define the property, and they guide them with a
series of questions. Autili et al. (2007) have provided a wizard for property sequence chats
(WPSC) to assist system engineers in resolving potential occurrences of uncertainty and
ambiguity in system requirements. Tiwari et al. (2022) have introduced an approach to elicit
the natural language into a structured natural language through mapping of requirement
templates. This paper provides an approach that uses an LLM to write structured infor-
mal specifications based on few-shots prompting, which provides examples of syntax and
semantics of a formal-grammar based structured natural language.
    Recent works (Manas and Paschke 2023; Jha et al. 2023; He et al. 2021; Zaki-Ismail et al.
2022; Ramzan et al. 2024) have provided approaches that integrate symbolic information
with LLM to generate formal specifications. Manas and Paschke (2023) have used semantic
role labelling information to generate formal specifications for intelligent vehicles. Jha et al.
(2023) have integrated counter-examples from SMT solvers with LLM to provide a feedback
loop for generating formal specifications. He et al. (2021) have designed a grammar-based
approach to translate English to signal temporal logic, then used the input-output pairs to
train a model. Zaki-Ismail et al. (2022) have proposed an NLP-based approach (statistical) to
extract semi-formal representations from natural language. Ramzan et al. (2024) have intro-
duced a rule-based approach with machine learning to translate structured natural language
requirements into class diagrams. This paper provides a symbolic approach that integrates an
LLM to restrict the syntax of informal specification to adhere a formal-grammar, then uses
a compiler to translates the syntax-restricted sentences with symbolic information including
idiom knowledge base and TSIs, to generate formal specifications in JML format.
    To measure the quality of the generated contracts, this paper has included the mutation
analysis of contracts. Le Traon et al. (2006) have introduced different metrics to measure
vigilance and diagnosability of contracts. FEATUREIDE (Thüm et al. 2014) has provided
experiments to analyse the effectiveness and time required for existing tools in verifying
programs with contracts. This paper focuses on formalising informal specifications, and
mutation analysis is included as a measure to quantify the quality of the generated contracts.


10 Conclusion

Formalising natural language specifications can be achieved in different ways, including
symbolic grammar-based approaches as well as the direct use of LLMs. However, this paper
exposes several limitations of those approaches when it comes to addressing real-world speci-
fications. The symbolic approach generates rigorous specifications with correct syntax and
semantics, but requires manual extension of grammar rules to cover the breadth of natural lan-
guage. An LLM, on the other hand, can handle a broad scope of natural language but lacks the
syntactic and semantic rigour needed to write specifications in formal specification languages.
   To improve upon the existing approaches, this paper introduces HAFIS, which combines
the broad language acceptance from the LLM and explicit rules from a symbolic approach




13
Empirical Software Engineering (2026) 31:181                                                          Page 43 of 47 181


in formalising informal specifications. The approach includes restricting the informal speci-
fications to sentences that follow the rules of the symbolic approach, by building prompts
with method signatures and few-shot examples. Then, the symbolic approach translates
these sentences into target JML in two steps: deriving MRs encoded in lambda expressions
with Neo-Davidsonian event semantics from these sentences, and translating these MRs
into JML. To address these steps, the paper introduces the notion of typed semantic inter-
pretation to ensure the meaning and validity of generated JML.
    Using a real-world dataset, the paper experimentally evaluates the proposed HAFIS
approach combined with five distinct LLMs. HAFIS is compared to the pure grammar-based
approach and to the pure LLMs. First, HAFIS has significantly improved the MR derivation
from 23% to 100% when compared to using only the symbolic approach. Second, HAFIS pro-
vides up to 88% accuracy in formalising the real-world informal specifications, compared to
that of 81% from directly using an LLM with a relatively low quantity of JML specifications.
    To further investigate the quality of JML generated from the pure LLM approach and
HAFIS, mutation analysis was applied to assess the efficiency in finding defects. The JML
generated by HAFIS kills up to 44% of the mutants on average, and that of pure LLM kills
up to 24%. Moreover, the mutants killed by the JML generated by pure LLM are always
killed by that of HAFIS. Therefore, both the quantity and quality of JML generated by
HAFIS are greater than that of the pure LLM approach.
    The proposed method has performed substantially in MR derivation and translating infor-
mal specifications into JML. The JML specifications generated through this method have
demonstrated their ability to detect defects. Moreover, those specifications generated via the
integration with LLMs of advanced reasoning capabilities performed slightly better. These
findings indicate that the proposed method can be applied across various models. Finally,
the results from the ablation study support that the proposed method effectively mitigates
LLM variability, as even when provided with deliberately degraded prompts, HAFIS main-
tained over 90% of derivation accuracy and rejected non-compliant LLM outputs.
    Overall, these results substantiate that the proposed approach contributes to formalising
natural language requirements, by harnessing the benefits of LLMs in combination with the
rigour of symbolic grammar-based approaches.

Author Contributions Iat Tou Leong: conceptualisation, methodology, software, validation, formal analysis,
investigation, resources, data curation, writing – original draft, visualisation, and project administration. Raul
Barbosa: conceptualisation, methodology, formal analysis, investigation, resources, data curation, and writ-
ing – original draft.

Funding Open access funding provided by FCT|FCCN (b-on). This work is funded by national funds through
FCT – Foundation for Science and Technology, I.P., through the Digital Person project (Ref. 14765, COM-
PETE2030-FEDER-00926800) and within the scope of the research unit UID/00326 – Centre for Informatics
and Systems of the University of Coimbra.

Data Availability The data that is used in the experiment is publicly accessible in a repository ​(​h​t​t​p​s​:​/​/​g​i​t​h​u​
b​.​c​o​m​/​i​t​lc​ ​h​r​i​s​s​/​H​A​F​I​S​​​​)​.​​

Materials Availability Not applicable.

Code Availability The source code that has implemented the proposed approach is publicly accessible in a
repository (https://github.com/itlchriss/HAFIS).




                                                                                                              13
181 Page 44 of 47                                                 Empirical Software Engineering (2026) 31:181

Declarations

Ethics approval and consent to participate Not applicable.

Consent for publication/Informed consent Not applicable.

Clinical trial number Not applicable.

Conflicts of Interest/Competing interests The authors declare that they have no known competing financial
interests or personal relationships that could have appeared to influence the work reported in this paper.
The authors declare that no financial interests/personal relationships which can be considered as potential
competing interests.

Open Access This article is licensed under a Creative Commons Attribution 4.0 International License,
which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as long as
you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons
licence, and indicate if changes were made. The images or other third party material in this article are
included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the material.
If material is not included in the article’s Creative Commons licence and your intended use is not permitted
by statutory regulation or exceeds the permitted use, you will need to obtain permission directly from the
copyright holder. To view a copy of this licence, visit http://creativecommons.org/licenses/by/4.0/.




References
Autili M, Inverardi P, Pelliccione P (2007) Graphical scenarios for specifying temporal properties: an auto-
     mated approach. Autom Softw Eng 14(3):293–340
Autili M, Grunske L, Lumpe M et al (2015) Aligning qualitative, real-time, and probabilistic property speci-
     fication patterns using a structured English grammar. IEEE Trans Software Eng 41(7):620–638
Barrientos M, Winter K, Rinderle-Ma S (2024) Automatic extraction and formalization of temporal require-
     ments from text: A survey. In: International Conference on Enterprise Design, Operations, and Comput-
     ing, Springer, pp 259–278
Bird S, Klein E, Loper E (2009) Natural Language Processing with Python, 1st edn. O’Reilly Media, Inc
Blasi A, Goffi A, Kuznetsov K (2018) Translating code comments to procedure specifications. In: Proceed-
     ings of the 27th ACM SIGSOFT international symposium on software testing and analysis, pp 242–253
Bombieri M, Meli D, Dall’Alba D et al (2023) Mapping natural language procedures descriptions to linear
     temporal logic templates: an application in the surgical robotic domain. Appl Intell 53(22):26351–26363
Chalin P, Kiniry JR, Leavens GT (2005) Beyond assertions: Advanced specification and verification with
     JML and ESC/Java2. In: International Symposium on Formal Methods for Components and Objects,
     Springer, pp 342–363
Cobleigh RL, Avrunin GS, Clarke LA (2006) User guidance for creating precise and accessible property
     specifications. In: Proceedings of the 14th ACM SIGSOFT international symposium on Foundations of
     software engineering, pp 208–218
Cok DR (2011) OpenJML: JML for Java 7 by extending OpenJDK. In: Bobaru M, Havelund K, Holzmann
     GJ et al (eds) NASA Formal Methods. Springer, Berlin Heidelberg, Berlin, Heidelberg, pp 472–479
Cosler M, Hahn C, Mendoza D (2023) nl2spec: Interactively translating unstructured natural language to
     temporal logics with large language models. In: International Conference on Computer Aided Verifica-
     tion, Springer, pp 383–396
Curran J, Clark S, Bos J (2007) Linguistically motivated large-scale NLP with C&C and boxer. In: Proceed-
     ings of the 45th Annual Meeting of the Association for Computational Linguistics Companion Vol-
     ume Proceedings of the Demo and Poster Sessions. Association for Computational Linguistics, Prague,
     Czech Republic, pp 33–36
Di Guglielmo D, Fummi L, Orlandi F, N (2010) DDPSL: An easy way of defining properties. In: 2010 IEEE
     International Conference on Computer Design, pp 468–473. IEEE
Endres M, Fakhoury S, Chakraborty S (2024) Can large language models transform natural language intent
     into formal method postconditions?. arXiv:2310.01831



13
Empirical Software Engineering (2026) 31:181                                              Page 45 of 47 181

Ernst MD, Perkins JH, Guo PJ et al (2007) The daikon system for dynamic detection of likely invariants. Sci
      Comput Program 69(1–3):35–45
Farrell M, Luckcuck M, Sheridan O (2022) Fretting about requirements: formalised requirements for an
      aircraft engine controller. In: International Working Conference on Requirements Engineering: Founda-
      tion for Software Quality, Springer, pp 96–111
Filliâtre JC, Paskevich A (2013) Why3—where programs meet provers. In: Programming Languages and
      Systems: 22nd European Symposium on Programming, ESOP 2013, Held as Part of the European Joint
      Conferences on Theory and Practice of Software, ETAPS 2013, Rome, Italy, March 16-24, 2013. Pro-
      ceedings 22, Springer, pp 125–128
First E, Rabe MN, Ringer T et al (2023) Baldur: Whole-proof generation and repair with large language mod-
      els. In: Proceedings of the 31st ACM Joint European Software Engineering Conference and Symposium
      on the Foundations of Software Engineering. Association for Computing Machinery, New York, NY,
      USA, ESEC/FSE 2023, pp 1229–1241. https://doi.org/10.1145/3611643.3616243
Flanagan C, Leino K (2001) Houdini, an annotation assistant for ESC/JAVA. In: International Symposium of
      Formal Methods Europe, Springer, pp 500–517
Gavran I, Darulova E, Majumdar R (2020) Interactive synthesis of temporal specifications from examples
      and natural language (2020). https://doi.org/10.1145/34282
Ghosh S, Elenius D, Li W (2014) Automatically extracting requirements specifications from natural lan-
      guage. arXiv:1403.3142
Giannakopoulou D, Pressburger T, Mavridou A et al (2020) Generation of formal requirements from struc-
      tured natural language. In: Requirements Engineering: Foundation for Software Quality: 26th Interna-
      tional Working Conference, REFSQ 2020, Pisa, Italy, March 24–27, 2020, Proceedings 26, Springer,
      pp 19–35
Grunske L (2008) Specification patterns for probabilistic quality properties. In: Proceedings of the 30th inter-
      national conference on Software engineering, pp 31–40
Hahn C, Schmitt F, Tillman JJ et al (2022) Formal specifications from natural language. arXiv:2206.01962
He J, Bartocci E, Ničković D (2021) From English to signal temporal logic. arXiv:2109.10294
Janßen C, Richter C, Wehrheim H (2024) Can ChatGPT support software verification? In: Beyer D, Caval-
      canti A (eds) Fundamental Approaches to Software Engineering. Springer Nature Switzerland, Cham,
      pp 266–279
Jha SK, Jha S, Lincoln P et al (2023) Neuro symbolic reasoning for planning: Counterexample guided induc-
      tive synthesis using large language models and satisfiability solving. arXiv:2309.16436
Just R (2014) The major mutation framework: efficient and scalable mutation analysis for Java. In: Interna-
      tional Symposium on Software Testing and Analysis
Kirchner F, Kosmatov N, Prevosto V et al (2015) Frama-C: A software analysis perspective. Formal Aspects
      Comput 27:573–609
Konrad S, Cheng BH (2005) Real-time specification patterns. In: Proceedings of the 27th international con-
      ference on Software engineering, pp 372–381
Kress-Gazit H, Fainekos GE, Pappas GJ (2008) Translating structured English to robot controllers. Adv
      Robot 22(12):1343–1359
Kuhn T (2014) A survey and classification of controlled natural languages. Computational Linguistics
      40(1):121–170. https://doi.org/10.1162/coli_a_00168,
Le Traon Y, Baudry B, Jézéquel JM (2006) Design by contract to improve software vigilance. IEEE Trans
      Software Eng 32(8):571–586
Leavens GT, Baker AL, Ruby C (2006) Preliminary design of JML: A behavioral interface specification
      language for Java. SIGSOFT Softw Eng Notes 31(3):1–38
Leino KRM (2010) Dafny: An automatic program verifier for functional correctness. In: Clarke EM,
      Voronkov A (eds) Logic for Programming, Artificial Intelligence, and Reasoning. Springer, Berlin Hei-
      delberg, Berlin, Heidelberg, pp 348–370
Leong IT, Barbosa R (2023) Translating natural language requirements to formal specifications: A study
      on GPT and symbolic NLP. In: 2023 53rd Annual IEEE/IFIP International Conference on Depend-
      able Systems and Networks Workshops (DSN-W), pp 259–262. https:​​​//d​oi.​or​g/10​.11​09/DSN​-W58​399​
      .2023.00065
Leong IT, Barbosa R (2024) Translating meaning representations to behavioural interface specifications. J
      Syst Softw 211:112009. https://doi.org/10.1016/j.jss.2024.112009
Lewkowycz A, Andreassen A, Dohan D et al (2022) Solving quantitative reasoning problems with language
      models. arXiv:2206.14858
Li C, Chang J, Wang X (2022) Formalization of natural language into PPTL specification via neural machine
      translation. In: International Workshop on Structured Object-Oriented Formal Language and Method,
      Springer, pp 79–92
Lozhkov A, Li R, Allal LB (2024) Starcoder 2 and the stack v2: The next generation. arXiv:2402.19173


                                                                                                  13
181 Page 46 of 47                                                Empirical Software Engineering (2026) 31:181

Ma L, Liu S, Li Y (2024) SpecGen: Automated generation of formal program specifications via large lan-
     guage models. arXiv:2401.08807
Manas K, Paschke A (2023) Semantic role assisted natural language rule formalization for intelligent vehicle.
     In: International Joint Conference on Rules and Reasoning, Springer, pp 175–189
Martínez-Gómez P, Mineshima K, Miyao Y (2016) ccg2lambda: A compositional semantics system. In:
     Proceedings of ACL 2016 System Demonstrations. Association for Computational Linguistics, Berlin,
     Germany, pp 85–90
de Moura L, Bjørner N (2008) Z3: An efficient SMT solver. In: Ramakrishnan CR, Rehof J (eds) Tools and
     Algorithms for the Construction and Analysis of Systems. Springer, Berlin Heidelberg, Berlin, Heidel-
     berg, pp 337–340
Norheim JJ, Rebentisch E (2024) Structuring natural language requirements with large language models. In:
     2024 IEEE 32nd International Requirements Engineering Conference Workshops (REW), pp 68–71.
     IEEE
OpenAI (2022) Introducing ChatGPT. Internet: https://openai.com/blog/chatgpt
Pan J, Chou G, Berenson D (2023) Data-efficient learning of natural language to linear temporal logic transla-
     tors for robot task specification. arXiv:2303.08006
Poiroux A, Weiss G, Kunčak V (2024) ) Improving autoformalization using type checking. arXiv:2406.07222
Ramzan M, Sadiqi GS, Bashir MS et al (2024) A rule-based approach for automatic generation of class dia-
     gram from functional requirements using natural language processing and machine learning. J Comput
     Biomed Inf 7(02)
Thüm T, Meinicke J, Benduhn F et al (2014) Potential synergies of theorem proving and model checking for
     software product lines. In: Proceedings of the 18th International Software Product Line Conference-
     Volume 1, pp 177–186
Tiwari S, Shah P, Khare M (2022) NL2RT: A tool to translate natural language text into requirements tem-
     plates (RTS). In: 2022 IEEE 30th International Requirements Engineering Conference (RE), pp 262–
     263. IEEE
Touvron H, Lavril T, Izacard G et al (2023) Llama: Open and efficient foundation language models.
     arXiv:2302.13971
Wang C, Pastore F, Briand L (2018) Automated generation of constraints from use case specifications to sup-
     port system testing. In: 2018 IEEE 11th International Conference on Software Testing. Verification and
     Validation (ICST), IEEE, pp 23–33
Wang X, Li G, Li C et al (2020) Automatic generation of specification from natural language based on tem-
     poral logic. In: International Workshop on Structured Object-Oriented Formal Language and Method,
     Springer, pp 154–171
Wang C, Ross C, Kuo YL (2021) Learning a natural-language to LTL executable semantic parser for grounded
     robotics. In: Conference on Robot Learning, PMLR, pp 1706–1718
Warmer JB, Kleppe AG (2003) The object constraint language: getting your models ready for MDA. Addi-
     son-Wesley Professional
Wen C, Cao J, Su J (2024) Enchanting program specification synthesis by large language models using
     static analysis and program verification. In: International Conference on Computer Aided Verification,
     Springer, pp 302–328
Wu Y, Jiang AQ, Li W (2022) Autoformalization with large language models. In: Koyejo S, Mohamed S,
     Agarwal A (eds) Advances in Neural Information Processing Systems, vol 35. Curran Associates Inc,
     pp 32353–32368
Xie X, Kersting K, Neider D (2022) Neuro-symbolic verification of deep neural networks. arXiv:2203.00938
Xu Y, Feng J, Miao W (2024) Learning from failures: Translation of natural language requirements into linear
     temporal logic with large language models. In: 2024 IEEE 24th International Conference on Software
     Quality. Reliability and Security (QRS), IEEE, pp 204–215
Yan R, Cheng CH, Chai Y (2015) Formal consistency checking over specifications in natural languages. in
     2015 design, automation & test in Europe conference & exhibition (date)
Zaki-Ismail A, Osama M, Abdelrazek M et al (2022) RCM-extractor: an automated NLP-based approach for
     extracting a semi formal representation model from natural language requirements. Autom Softw Eng
     29(1):10
Zhai J, Shi Y, Pan M (2020) C2S: translating natural language comments to formal program specifications.
     In: Proceedings of the 28th ACM Joint Meeting on European Software Engineering Conference and
     Symposium on the Foundations of Software Engineering, pp 25–37




13
Empirical Software Engineering (2026) 31:181                                           Page 47 of 47 181

Zhang R, El-Gohary N (2022) Natural language generation and deep learning for intelligent building codes.
      Adv Eng Inform 52:101557
Zhang S, Zhai J, Bu L (2020) Automated generation of LTL specifications for smart home IoT using natu-
      ral language. In: Proceedings of the 23rd Conference on Design, Automation and Test in Europe, pp
      622–625
Zhou JP, Staats C, Li W (2024) Don’t trust: Verify - grounding LLM quantitative reasoning with autoformal-
      ization. arXiv:2403.18120
Zrelli R, Misson HA, Attia B, M (2025) Automatic translation of natural language requirements into CTL
      specifications using large language models: A multi-approach evaluation. Available at SSRN 5334216

Publisher's Note Springer Nature remains neutral with regard to jurisdictional claims in published maps and
institutional affiliations.




                                                                                              13
