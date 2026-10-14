                                                             3DGen: AI-Assisted Generation of
                                                           Provably Correct Binary Format Parsers
                                                    Sarah Fakhoury, Markus Kuppe, Shuvendu K. Lahiri, Tahina Ramananandro and Nikhil Swamy
                                                                                           Microsoft Research, Redmond, USA
                                                                            {sfakhoury, makuppe, shuvendu, taramana, nswamy}@microsoft.com


                                           Abstract—Improper parsing of attacker-controlled input is            that yield trustworthy executable code. However, more com-
                                        a leading source of software security vulnerabilities, especially       monly, specifications are not entirely formal and come from a
                                        when programmers transcribe informal format descriptions in             variety of sources, ranging from natural language documents,
arXiv:2404.10362v2 [cs.SE] 6 May 2024




                                        RFCs into efficient parsing logic in low-level, memory unsafe
                                        languages. Several researchers have proposed formal specification       diagrams, example code snippets, sample input/output pairs,
                                        languages for data formats from which efficient code can be             etc. Extracting a formal specification from such a variety of
                                        extracted. However, distilling informal requirements into formal        sources requires a significant human effort, typically requiring
                                        specifications is challenging and, despite their benefits, new,         a process that involves:
                                        formal languages are hard for people to learn and use.
                                           In this work, we present 3DGen, a framework that makes use             1) Learning a new DSL;
                                        of AI agents to transform mixed informal input, including natural         2) Understanding the informal specification;
                                        language documents (i.e., RFCs) and example inputs into format            3) Expressing one’s understanding of the informal specifi-
                                        specifications in a language called 3D. To support humans in                 cation in the DSL;
                                        understanding and trusting the generated specifications, 3DGen            4) Iterating to refine intent, revisiting the previous steps to
                                        uses symbolic methods to also synthesize test inputs that can
                                        be validated against an external oracle. Symbolic test generation            arrive at a desired specification.
                                        also helps in distinguishing multiple plausible solutions. Through         This is challenging enough that developers often directly
                                        a process of repeated refinement, 3DGen produces a 3D specifica-        transcribe informal specifications into executable code in gen-
                                        tion that conforms to a test suite, and which yields safe, efficient,   eral purpose programming languages, leaving the door open
                                        provably correct, parsing code in C.
                                           We have evaluated 3DGen on 20 Internet standard formats,             to low-level coding errors that lead to security vulnerabilities.
                                        demonstrating the potential for AI-agents to produce formally
                                        verified C code at a non-trivial scale. A key enabler is the use        A. 3 D G EN: A Framework for AI-assisted DSL Programming
                                        of a domain-specific language to limit AI outputs to a class for           In this work, we present 3 D G EN, a framework that uses AI
                                        which automated, symbolic analysis is tractable.                        agents to assist a human in translating an informal specification
                                           Index Terms—Code Generation, Agentic AI Systems, Trust-
                                        worthy AI programming
                                                                                                                to executable code via a DSL, grounded specifically in generat-
                                                                                                                ing binary format parsers using 3D. Our framework is agnostic
                                                              I. I NTRODUCTION                                  to the AI model used, though for our experiments we use GPT-
                                           Improper parsing of attacker-controlled input is a leading           4 [4]. The core of 3 D G EN is an automated intent-refinement
                                        source of software security vulnerabilities,12 especially when          loop which assists a user in constructing a 3D specification that
                                        programmers transcribe informal format descriptions into ef-            matches an oracle’s behavior on a set of test inputs. Figure 1
                                        ficient parsing logic in low-level, memory unsafe languages.            sketches the high-level workflow, whose main elements mirror
                                        For example, the format of TCP headers is specified in natural          the steps outlined above.
                                        language and packet diagrams in the classic RFCs 793 and                1. Teaching a DSL to an agent: 3D is a small language
                                        9293; meanwhile, tcp input.c, the TCP header parser in the              whose syntax is based on C’s syntax for typedefs, structures,
                                        Linux kernel was patched to prevent an out of bounds access             and unions. Its manual is relatively compact, consisting of
                                        in 2019, after being in the kernel for nearly 20 years.                 around 2,000 lines of text and around 20 examples. We “teach”
                                           In response, researchers have proposed languages for de-             3 D G EN about 3D by giving it access to the manual, and the
                                        scribing low-level binary message formats backed by code                ability to query parts of the manual based on techniques that
                                        generators that yield parsing and serialization tools, e.g.,            we describe in §III-B.
                                        Nail [1] and EverParse [2], [3]. EverParse is notable in that it        2 & 3. Digesting informal specifications into 3D: A user gath-
                                        produces formally verified C code from a format description             ers a collection of informal specifications, including natural
                                        language (called 3D), guaranteeing memory safety, functional            language documents that describe message formats and sample
                                        correctness, and double-fetch freedom..                                 test inputs, and presents it to 3 D G EN. In turn, our framework,
                                           In an ideal world, one might hope for specifications to              prompts the underlying agents to generate a 3D specification.
                                        always be written in domain-specific languages (DSLs) like 3D           4. Refining intent The 3D compiler analyzes candidate 3D
                                          1 https://cwe.mitre.org/data/definitions/20.html                      specifications, providing syntax and type errors that we feed
                                          2 https://cwe.mitre.org/data/definitions/502.html                     back to the agents to repair their code until the produced 3D
                                                                         growing a carefully curated test suite.
                                                                            A key enabler of our technique is the use of an effectively
                                                                         analyzable DSL, coupled with a verified code generator, as
                                                                         a medium of interaction between a user’s informal intent
                                                                         and AI-generated output. In contrast, directly prompting AI
                                                                         agents to produce C code from informal specifications would
                                                                         leave open the question of analyzing ad hoc C code for
                                                                         safety and security, and with an unclear formal basis against
                                                                         which to assess code correctness. Further, targeting a DSL
                                                                         enables us to integrate powerful, fully automated tools like
                                                                         symbolic test-case generation and differential analysis that
                                                                         are usually intractable for large, general-purpose languages.
                                                                         We conjecture that future AI-assisted programming techniques
                                                                         might also benefit from the use of effectively analyzable DSLs
                                                                         as intermediate languages.
                     Fig. 1: Workflow of 3 D G EN                           In summary, we make the following contributions:
                                                                           1) An architecture for AI-assisted programming using DSLs
                                                                              coupled with symbolic analysis tools to refine informal
specifications are at least well defined. Next, exploiting the                user intent into formal specifications, grounded in the
fact that 3D is a small language with a well-designed formal                  scenario of binary format parsers.
semantics, we develop 3 D T EST G EN a new symbolic test-case              2) A new symbolic analysis and test generation tool for
generator for 3D. This allows us to automatically generate                    the 3D format language, integrated in 3 D G EN’s intent
new test inputs for candidate specifications, and we rely on                  refinement loop.
various external oracles to decide the intended classification             3) An evaluation of 3 D G EN on a suite of 20 binary format
of an input. Enriching the input with the new test cases, we                  parsers specified in Internet standard RFCs, yielding safe
repeat the loop.                                                              and secure C code.
   Having converged with 3 D G EN’s help on a given 3D
specification, the user relies on EverParse to generate verified                         II. P ROBLEM F ORMULATION
C code that is guaranteed to parse only all messages that are               Ramananandro et al. [2] present EverParse, a library
well-formed according to the specification.                              of parser and serializer combinators in the F⋆ pro-
   We evaluate 3 D G EN on 20 Internet standard formats, start-          gramming language. They prove that every well-typed
ing from their specification in RFCs. While 3 D T EST G EN can           program assembled from their parser combinators pro-
generate tests from candidate specifications, we still require           duces a parser that is the inverse of the correspond-
oracles to label those tests with their desired outcome; specifi-        ing serializer, i.e., ∀s. parse (serialize s) == Some s and
cally, we use the Wireshark3 network packet analyzer to decide           ∀b v. parse b == Some v =⇒ serialize v == b. Parsers for for-
if a packet should be accepted or not. Interestingly, in 11 cases,       mats that satisfy this mutual inverse property are particularly
3 D G EN discovers constraints specified in RFCs that Wireshark          relevant in security-critical settings. EverParse combinators are
does not enforce. Additionally, for 7 protocol formats, we               themselves embedded within a fragment of F⋆ called Low* [5],
also evaluated 3 D G EN’s ability to produce 3D specification            which supports transpilation to C via a tool called Karamel.
that match the behavior of prior, handwritten specifications                Swamy et al. [3] present a DSL built on top of EverParse
for various formats provided as samples by the authors of                combinators called 3D, a language similar to C’s language
EverParse. In this setting, 3 D G EN uncovers 3 cases in which           of type definitions, with typedefs, structures, and unions.
the human authored specifications were incorrect. That said,             3D allows users to express a variety of “tag-length-value”
the specifications 3 D G EN produces are only as good as the             style formats, which are commonly used in many networking
tests on which it is evaluated. In 2 cases, 3 D G EN produces            protocols and other variable-length formats.
specifications that agree with Wireshark, but 3 D T EST G EN                Internet RFCs often specify tag-length-value formats in
detects, via symbolic differential testing, that the generated           natural language in an ad hoc way. For example, the TCP
specification is semantically distinct from a human-authored             RFC 793 specifies the format of TCP options as follows:
EverParse sample—the 3 D G EN-produced specification does                There are two cases for the format of an option:
not enforce a constraint that it should. As such, we caution
that 3 D G EN should not be used to blindly match the behavior           Case 1: A single octet of option-kind.
                                                                         Case 2: An octet of option-kind, an octet of
of a legacy tool. Instead, we envision 3 D G EN and its symbolic         option-length, and the actual option-data octets.
tools to be used by humans to iteratively refine a natural               ...
language document into a formal specification, while also                Currently defined options include
                                                                         (kind indicated in octal):
  3 https://www.wireshark.org/docs/man-pages/tshark.html                     Kind        Length      Meaning




                                                                     2
      ----     ------       -------                                    the intent of the RFC—a process that typically involves careful
       0         -          End of option list.                        review combined with testing. While 3D was designed to be
       1         -          No-Operation.
       2         4          Maximum Segment Size.                      used by C programmers and benefits from its resemblance
...                                                                    to C, the constructs it offers, including type dependency,
                                                                       value constraints, parameterization, case analysis, etc. take
 Maximum Segment Size
                                                                       effort to learn and use correctly. Further, while EverParse
         +--------+--------+---------+--------+                        guarantees that the generated C code is memory safe, free from
         |00000010|00000100|   max seg size   |                        bugs that trigger undefined behaviors, and faithfully parses
         +--------+--------+---------+--------+
          Kind=2   Length=4                                            exactly the specified format, the source specification is still
                                                                       subject to audit. For example, one could easily have specified
Maximum Segment Size Option Data:          16 bits                     UINT16 MaxSegSize, forgetting a convention that networking
...
                                                                       protocols like TCP typically use big-endian integers—users
  To produce a parser for a TCP option in 3D, one starts by            need assistance in specification testing and validation.
specifying the format declaratively. Here’s one way to do it,             Swamy et al. [3] report that 3D has been used to specify a
defining an OPTION as a structure with two fields: a byte field        suite of networking protocols used in production software at
Kind with a constraint that restricts its values to 0, 1, and 2;       Microsoft, including in the kernel of the Windows 11 release.
and a payload field of type OPTION_OF_KIND(Kind), a type that          They report using 3D to specify “137 structs, 22 casetypes,
depends on the value of the Kind field.                                and 30 enum type definitions” in around 5,000 lines of 3D
                                                                       specifications, stating that “describing those message formats
  typedef struct _OPTION {
      UINT8 Kind {                                                     required careful specification engineering and discovery” over
         Kind == 0x00 ||                                               a period of 18 months. With 3 D G EN, we seek to lower this
         Kind == 0x01 ||                                               overhead, making 3D accessible to non-experts by directly
         Kind == 0x02
      };                                                               synthesizing specifications from informal intent, and to offer
      OPTION_OF_KIND(Kind) payload;                                    systematic testing tools to assist with validation.
  } OPTION;
                                                                                       III. T HE 3 D G EN A PPROACH
   The type OPTION_OF_KIND, a casetype in 3D, represents
a form of union type in C, where the parameter Kind dis-                  In this Section, we make precise the workflow in Figure 1,
criminates the case of the union. When Kind is 0 or 1, the             showing how we derive a 3D specification from RFCs and
payload is empty, and when the Kind is 2, the payload has              tests. We start by describing the algorithm abstractly, pa-
type MAX_SEG_SIZE.                                                     rameterized by several non-deterministic choices, AI-based
                                                                       components, and a test generator for 3D. We then describe
  casetype _OPTION_OF_KIND(UINT8 Kind) {
      switch (Kind) {
                                                                       an agent-based implementation of the AI-based components,
         case 0x00: unit case0; /*unit: empty payload*/                and 3 D T EST G EN, a new symbolic test generator for 3D.
         case 0x01: unit case1; /*unit: empty payload*/
         case 0x02: MAX_SEG_SIZE case2;                                A. 3DG EN: An Abstract Algorithm
      }
  } OPTION_OF_KIND;                                                       We assume the 3D DSL is equipped with the following
                                                                       functions:
   Finally, the type MAX_SEG_SIZE is a structure, with one byte           • 3DS YN C HK : A syntax and type checker function, given
for the Length and 2-bytes for an unsigned 16-bit big-endian                 a specification p checks for syntax as well as type
integer for the MaxSegSize.                                                  constraints imposed by the 3D language.
  typedef struct _MAX_SEG_SIZE {                                          • 3DE XEC : An execution function; for any 3D specifica-
     UINT8 Length;                                                           tion p that satisfies 3DS YN C HK(p), given a packet i,
     UINT16BE MaxSegSize;
  } MAX_SEG_SIZE;                                                            3DE XEC(p, i) returns true iff the specification p accepts
                                                                             the packet i. Concretely, we use EverParse to compile p
   From this specification, EverParse (in its simplest mode)                 to C code and execute it on i.
generates a C program with the following signature, a function            • 3DDoc: Natural language documentation about the 3D
CheckOption which, when called with a byte buffer Input                      language and examples, provided as a manual.
containing at least Length bytes, checks that Input contains              Algorithm 1 takes as input an RFC document, function
a valid representation of OPTION, returning an error code              LblImpl that is used to classify packets, as well as a (possibly
recording success, or details about where and why validation           empty) seed sets of positive and negative packets, I0+ and
failed.                                                                I0− . The desired 3D specification p should accept the positive
  EVERPARSE_ERROR_CODE CheckOption(                                    packets I0+ and reject I0− . The algorithm returns a set of
     UINT8* Input,                                                     possible candidate 3D specifications CandProgs, along with
     UINT64 Length)
                                                                       an augmented set of positive (I + ) and negative (I − ) packets,
  A 3D user turning an ad hoc description from an RFC to a             generated by 3 D T EST G EN and labeled using LblImpl, ensur-
specification must convince themselves that they have captured         ing that every specification in CandProgs is consistent with the



                                                                   3
augmented set of packet inputs. Formally, I0+ ⊆ I + , I0− ⊆ I − ,              examples, failing tests to focus on, etc. Composing a single
and for each p ∈ CandProgs, 3DE XEC(p, i+ ) = true for each                    monolithic prompt with all relevant context needed to solve
i+ ∈ I + , and 3DE XEC(p, i− ) = false for each i− ∈ I − .                     a task is often impossible, given the restricted token context-
   The algorithm iterates non-deterministically, accumulating                  window for LLMs.
state which records all relevant information to be fed to an                      Instead, research shows that LLM-based agents significantly
LLM in st, initialized to the 3DDoc, the RFC, and the seed                     extend the capabilities of standalone LLMs by equipping them
tests. At each iteration, it performs one of the following two                 with the abilities needed to solve tasks in a self-directed
actions non-deterministically: (i) augment CandProgs with a                    fashion, such as long-term planning, reasoning [6], conversing
new well-formed 3D specification p by querying an LLM                          with other LLMs, using tools, and retrieving information
(lines 5–13); or, (ii) augment the labeled packets in I + and                  critical to task resolution [7]. Agents demonstrate improved
I − using 3 D T EST G EN and L ABEL I NPUTS (lines 14–17).                     performance and generalization of task resolution abilities
Finally, at lines 18–26, candidates in CandProgs that are not                  for a number of increasingly complex and real-world tasks
consistent with the labeled packets are pruned, and any failing                [8], [9]. Furthermore, orchestrating multiple agents that are
candidate/test pairs are added to the state (line 20).                         instructed to cooperate together, can scale up the capabilities
   To generate a candidate program p, at line 6 we                             of a single agent by decomposing tasks, improving factuality
Q UERY LLM with the accumulated state—this step is imple-                      and reasoning [10], and validation [11].
mented using agents, as described in Section III-B. If p fails                    Motivated by these findings, we design an agent system
the 3DS YN C HK, we update the state with the error, and retry.                based on the AutoGen [12] multi-agent framework. AutoGen
   The 3D symbolic test generator 3 D T EST G EN takes as input                allows the instantiation of multiple agents, each unique in their
a set of well-formed candidate programs that satisfy the current               task description, access to tools and inputs, and instructed to
I + ∪I − , and outputs new (unlabeled) packets by symbolically                 cooperate together to achieve a solution. We choose to use a
analyzing the programs in CandProgs; we describe the precise                   multi-agent framework over a single agent, to decompose tasks
implementation in Section III-C. We then use LblImpl to                        and reduce overall input in the context window, shielding other
label each packet as positive or negative—concretely, we                       agents from unrelated intermediate reasoning steps involved
use Wireshark as an implementation of LblImpl. Details of                      in distinct task refinement loops. In the AutoGen multi-agent
L ABEL I NPUTS is present in Section IV-C.                                     setup agents converse in a group chat setting, critiquing and
                                                                               reflecting on task progress based on conversation history,
Algorithm 1 3DG EN Algorithm
                                                                               and adapting from feedback. AutoGen provides the multi-
Input: RFC, LblImpl, I0+ , I0−
Output: CandProgs, I + , I −
                                                                               agent conversation framework as a high level abstraction,
 1: (I + , I − ) ← (I0+ , I0− )                                                requiring only meta prompts and tool customization from
 2: st ← {3DDoc, RFC, I + , I − }                                              the user. The agent framework designed for 3 D G EN is not
 3: CandProgs ← {}
 4: for ∗ do                                                                   reliant on one particular LLM, however we use GPT4-32k
 5:     if ∗ then                                                              across all experiments. The 3 D G EN multi-agent framework is
 6:         p ← Q UERY LLM(st)
 7:         se ← 3DS YN C HK(p)                                                implemented concretely as three distinct agents:
 8:         if se ̸= SUCCESS then
 9:              st ← st ∪ {(p, se)}                                            1) Planner Agent: the planner agent is a tool-backed agent
10:              continue                                                          that orchestrates the multi-agent conversation. In Auto-
11:          end if
12:          CandProgs ← CandProgs ∪ {p}                                           Gen it is instantiated as the group chat manager. It has
13:      end if                                                                    access to the meta task prompt, descriptions of the other
14:      if ∗ then
15:          I ′ ← 3 D T EST G EN(CandProgs, I + ∪ I − )                           two agents, and the ability to invoke tools 3DS YN C HK
16:          (I + , I − ) ← (I + , I − ) ∪ L ABEL I NPUTS(I ′ , LblImpl)           and 3DE XEC, and communicate the results to the other
17:      end if
18:      for q ∈ CandProgs do                                                      agents.
19:          for all i ∈ I + ∪ I − do                       !                   2) 3D Developer Agent: the 3D developer agent is tasked
                    W         i ∈ I + ∧ ¬3DE XEC(q, i)
20:              if                                              then              with generating 3D code based on instructions com-
                               i ∈ I − ∧ 3DE XEC(q, i)
21:                  st ← st ∪ {(q, i)}                                            municated from the other two agents. This agent has
22:                  CandProgs ← CandProgs \ {q}
23:                  break
                                                                                   access to the full 3D language manual 3DDoc, a set
24:              end if                                                            of task examples, and high level tips about generating
25:          end for
26:      end for
                                                                                   syntactically correct 3D code.
27: end for                                                                     3) Domain Expert Agent: the domain expert agent is tasked
28: return CandProgs, I + , I −
                                                                                   with communicating specifications to the 3D Developer
                                                                                   Agent, and critiquing generated 3D code. It has access
B. Agent Based Implementation                                                      to all domain-relevant documents needed to solve the
   Constructing a prompt for an LLM from the diverse in-                           problem. In this work, the domain expert agent has access
formation in Algorithm 1’s accumulated state is non-trivial.                       to an RFC, the network protocol specification document
It involves choosing relevant sections of natural language                         needed to solve the task, and examples of the task.
documentations from several pages of RF C, 3DDoc, relevant                       All three agents communicate via an inter-agent group chat,



                                                                           4
until one of two termination conditions are met: either the out-        complex ones in a correct-by-construction way. For example,
put of 3DE XEC indicates that the generated 3D specification            the following 3D program defines a message data format
passes on the test set, or the maximum number of iterations,            specification as a structure of two unsigned 8-bit integer fields,
as set by the user, have been completed. The control flow of            first and second, where first has a constraint on its value:
task resolution follows the paradigm provided in AutoGen, and             typedef struct _message {
is entirely conversation-driven, i.e. the participating agents’             UINT8 first { first > 42 };
decisions on which agents to send messages to and the                       UINT8 second;
                                                                          } message;
procedure of computation are functions of the inter-agent
conversation. An example of control flow is as follows: 1)              The semantics of that 3D program is modeled in F⋆ by the
the Domain Expert agent communicates the relevant parts of              following message parser parse message as an application
the RFC specification to the 3D Developer Agent 2) the 3D               of the parse pair combinator:
Agent generates a candidate specification 3) the Planner Agent            let parse message =
makes a call to 3DS YN C HK and communicates the result to                parse pair (parse refine parse uint8 (λ first → first > 42))
the group 4) the 3D Agent reflects on a syntax error reported                         parse uint8
by the Planner and refines the specification. One example of            where parse pair, defined in EverParse, has a higher-order
the control flow is later shown in Figure 2.                            type parser t1 → parser t2 → parser (t1 * t2). Operationally,
C. 3 D T EST G EN: Symbolic Test Case Generation                        the code above first checks that the input sequence contains
                                                                        at least one byte; then parses the first byte using parse uint8
   In this section, we discuss our implementation of the
                                                                        and reads it into the variable first; then advances the posi-
3 D T EST G EN sub-routine of Algorithm 1. Our test (packet)
                                                                        tion in the input by one byte; then checks that first < 42;
generator, called 3 D T EST G EN, is implemented as an extension
                                                                        then tries to read and return the next byte. If any of the
of the EverParse toolchain, and is grounded in the formal
                                                                        checks fail, the parser returns None. Otherwise, it returns
semantics of 3D. 3 D T EST G EN encodes 3D programs into the
                                                                        Some ((first, second), 2), a pair containing the two bytes that
SMT-LIB version 2 language (a.k.a. SMT2) [13], relying on
                                                                        were read and 2 to indicate that two bytes were consumed.
SMT-solver Z3 [14] to produce test cases. Given a 3D program               We would like to encode parse message to Z3, but
p, to obtain positive (resp. negative) test cases, 3 D T EST G EN       SMT2 does not directly support higher-order functions like
encodes the semantics of p to Z3 and asks for models of the             parse pair. So, at the heart of 3 D T EST G EN is a specialization
existential predicate: ”does there exist a sequence of bytes            pass over the 3D parser-combinator AST to turn it into a first-
that makes p succeed (resp. fail)”. Z3 returns with one of the          order program.
following answers:                                                         For starters, the SMT2 semantics of a 3D program is given
   • SAT: Z3 finds a model to satisfy predicate, including a            in the context of an uninterpreted function Input representing
      concrete sequence of bytes that makes the parser succeed          the input byte sequence on which the parser operates. The
      (resp. fail)                                                      assertion below constrains Z3 to pick models for the Input
   • UNSAT: the predicate is unsatisfiable, which means that            array where every element is a byte in the range [0, 256).
      p always fails (resp. succeeds)                                     (declare−fun Input (Int) Int)
   • UNKNOWN: Z3 times out. While there may be multiple                   (assert (forall ((i Int))
      causes to Z3 timeout; in our case, this happens rarely.                          (and (<= 0 (Input i)) (< (Input i) 256))))
   Further, given two 3D programs p1 and p2 , 3 D T EST G EN               Next, we encode a 3D program as an SMT2 State
can also produce differential test cases by asking Z3 to find a         transforming function, where the State records (among
sequence of bytes that satisfy p1 but not p2 . If Z3 returns            other things) the remaining size of the Input byte se-
UNSAT, then there are no such test cases: every packet                  quence (remaining−input−size); the number of bytes read
satisfying p1 also satisfies p2 . Separately, we can ask Z3 the         so far (current−pos); whether or not the parser has failed
same satisfiability question but with p1 and p2 swapped. If Z3          (has−failed); and the value they return (return−value).
returns UNSAT for both ways, then the 3D programs p1 and p2                We start by showing a simplified encoding of parse_uint8:
accept and reject the exact same packets: they are semantically           (define−fun parse−uint8 ((s0 State)) State
equivalent. We do not bound the size of packets.                            (if (and (not (has−failed s0))
   The semantics of a 3D program is represented                                      (> (remaining−input−size s0) 0))
                                                                                (success−state
by a pure F⋆ function whose (simplified) signature                                (Input (current−pos s0)) ;; return value.
is a value of type parser t, a function of the form                               (incr (current−pos s0)) ;; new position.
(input:seq byte) → option (t * nat) which when applied to                         (decr (remaining−input−size s0))) ;; new remaining size.
                                                                                (fail−state s0)))
an input sequence of bytes may fail returning None, or
succeed with Some (v, n), where v is the parsed value (of                 Next, we show the encoding of the parse message
type t) and n is the number of bytes of the input that were             parser, where 3 D T EST G EN has inlined the parse pair and
consumed.                                                               parse refine higher-order combinators from the 3D AST. This
   As described in §II, EverParse provides combinators, library         representation of the parse−message is adequate for test-case
functions that allow combining simpler parsers to build more            generation.



                                                                    5
                                                                                              RFC           Length
                                                                          #   Protocol                                 Description
                                                                                            (Version)       (Pages)
  (define−fun parse−message ((s0 State)) State
    (let ((s1 (parse−uint8 s0)))                                          1   UDP*             768               3     User Datagram Protocol
                                                                          2   ICMPv4 *         792              21     Internet Control Message Protocol
      (if (has−failed s1) s1                                              3   VXLAN*          7348              22     Virtual eXtensible Local Area Network
        (if (> (return−value s1) 42)                                      4   IPV6*           2460           39 (24)   Internet Protocol version 6
            (parse−uint8 s1)                                              5   IPV4*            791           45 (12)   Internet Protocol version 4
                                                                          6   TCP*             793           85 (10)   Transmission Control Protocol
            (fail−state s1)))))                                           7   Ethernet*       7348              22     Ethernet II Frames in VXLAN
                                                                          8   GRE             2784               9     Generic Routing Encapsulation
   Given a query such as the following, which con-                        9   IGMPv2          2236              24     Internet Group Managment Protocol
                                                                         10   DHCP            2131            45 (4)   Dynamic Host Configuration Protocol
strains the initial state init and asserts that message                  11   DCCP            4340          129 (14)   Datagram Congestion Control Protocol
                                                                         12   ARP              826              10     Address Resolution Protocol
parser parse−message does not fail when applied to init,                 13   NTP             5905           110 (4)   Network Time Protocol
                                                                         14   NBNS            1002            84 (6)   NetBIOS Name Service
Z3 can produce models for the Input variable and its                     15   NSH             8300            40 (8)   Network Service Header
length in bytes, yielding a positive test case; to gener-                16
                                                                         17
                                                                              TFTP
                                                                              RTP
                                                                                              1350
                                                                                              3550
                                                                                                                11
                                                                                                             104 (3)
                                                                                                                       Trivial File Transfer Protocol
                                                                                                                       Transport Protocol for Real-Time Applications
ate a negative test case, we would assert instead that                   18   PPP             1661           52 (11)   Point-to-Point Protocol
                                                                         19   TPKT            2126              25     ISO Transport Service on top of TCP
(has−failed (parse−message init)). Since the input byte se-              20   OSPF            5340           94 (13)   Internet Official Protocol Standards
quence can be arbitrarily long, we do not constrain its initial
                                                                         TABLE I: Dataset of protocols and corresponding RFCs. * denotes
size.                                                                    protocols for which there is a human written 3D specification. Page
  (declare−fun init () State) ;; initial state.                          numbers in ( ) indicate the length of the extracted RFC.
  (assert (and (not (has−failed init))
             (= 0 (current−pos init))))
  (assert (not (has−failed (parse−message init))))
  (check−sat)
  (eval (remaining−input−size init)) ;; input size from model.           syntax, we explore the number of refinement loops needed to
  (eval (Input 0)) ;; retrieve first input byte.
                                                                         generate 1) a syntax- and type-correct solution as determined
   If Z3 returns a model, then 3 D T EST G EN can iteratively            by 3DS YN C HK and 2) a semantically correct solution with
query Z3 for further distinct models with additional appropri-           respect to the test set, as determined by 3DE XEC. In addition,
ate assertions to avoid duplicates. However, with this encoding,         we highlight common mistakes made by the agents, as well as
Z3 generates models that may not cover all possible branches.            several instances where the agent is able to learn constraints
Our implementation uses a more sophisticated encoding to                 from the RFC that are not enforced by the Wireshark.
track which branches of a specification are covered by a given              For each protocol we instantiate 3 D G EN, using GPT-4-
test case, allowing us to systematically generate tests that cover       32k as the underlying LLM, at temperature 1.0. We set the
all branches up to a user-provided branch depth. We provide              number of specifications to generate to 5 and the max number
more details in the Appendix.                                            of syntax or packet refinements to 15 per attempt. If the
   Leveraging the existing semantics of 3D and its compact,              agents are able to produce a specification that passes before
structured language of parser combinators, our implementation            15 refinements, the agent loop is terminated. We observe
of 3 D T EST G EN took less than 3 person-weeks and around               that allowing more refinement loops within the 3 D G EN agent
2000 lines of F⋆ , OCaml, and SMT2.                                      conversation flow does not always lead to a successful attempt
                 IV. E XPERIMENTAL S ETUP                                at generating a specification. On the other hand, reducing the
                                                                         number of refinement loops often does not give the agents
A. Network Protocols
                                                                         enough attempts at solving the problem. This is especially
   We evaluate 3 D G EN on 20 network protocols specified in             true when the protocol is more complex, requiring the agents
IETF standards. Table I lists each protocol and a short descrip-         to produce a longer specification, for example in the case of
tion and the specific RFC number. We include the length of the           ICMP, where there are 8 distinct message types for which the
RFC in pages, as a rough measure of complexity, though RFCs              agent must generate a 3D specification.
contain a lot of information beyond the description of the
                                                                           For each protocol, we download the RFC from the IETF
format—the number in parenthesis, when present, shows the
                                                                         Data Tracker4 as a text file to provide as input in the 3D
number of pages in the RFC concerned with header formats.
                                                                         Developer agent prompt. In some cases, the full RFC is
B. Generating Specifications with 3 D G EN                               prohibitively long, and would exhaust the GPT-4-32k token
   To evaluate 3 D G EN’s ability to translate natural language          window. Since we are only interested in the part of the
specifications into 3D format specifications, we use it to               specification related to the header data format, in such cases
generate 5 candidate specifications for the protocols in Table I.        we manually extract the pages of the RFC related to the
We deem a generation successful if the produced specification            data format specification, (usually labeled in a section called
correctly classifies a test set of generated packets labeled by          “Header Specification”). The length of the extract pages is
Wireshark. We report a pass@5 metric, which counts the                   denoted in ( ) in Table I.In the future, we plan to explore
number of successful generations out of 5 runs. To evaluate              building a retrieval tool specific to RFC extraction.
how well agents in the 3 D G EN multi-agent framework are able
to understand the natural language specifications contained in
the network protocol RFC, as well as its ability to learn 3D               4 https://datatracker.ietf.org




                                                                     6
C. Generating a Labeled Test Set for each Protocol                                                       V. R ESULTS
   We build a test suite consisting of a mixture of real-                 A. Capabilities of 3 D G EN
world packet captures and synthetically generated tests by                   In this section, we present experimental evidence to answer
3 D T EST G EN, where we use Wireshark to decide if the packet            the following central question underpinning our work:
should be considered valid or not. For each protocol, we                  RQ1: Can 3DGen produce format specifications for networks
collected a small number of real world packets from various               protocols standardized in RFCs?
sources on the Internet and retain only those that Wireshark                 Table II details results of 3 D G EN on our dataset of 20
considers valid—we discard the negative cases, since they                 network protocols, We report the pass@5 metric, the average
are sometimes arbitrarily malformed. For synthetic tests, we              number of syntax refinement, and packet feedback refinement
run one iteration of the 3 D G EN loop seeded with the real-              loops across all attempts.
world packets. This produces a single candidate specification                At a first glance, 3 D G EN is able to generate a passing
on which we run 3 D T EST G EN to generate 200 test cases.                specification for 9/20 protocols, with a pass@5 = 45%. For
We configure 3 D T EST G EN to fully explore a trace with 100             two protocols, such as UDP and IGMP, 3 D G EN generates a
branch points, and observed that while many examples have                 passing specification in all 5 attempts, requiring an average
a large number of branches (e.g., ICMP has 82 branches),                  of 0.3 syntax refinements and 0 packet refinements for UDP,
none of them have more than 100 branches. We then collect at              and 3.8 and 0 for IGMP respectively. For the other seven,
least two examples from each branch point, until we reach 200             IPV4, DHCP, DCCP, ARP, NTP, NBNS, and NSH, 3 D G EN
examples. This gives us some confidence that the generated                can generate at least one passing specification, but is not
test suite is diverse, though its completeness is limited by the          successful in all 5 attempts.
quality of the specification on which 3 D T EST G EN is executed.            For the remaining 11 protocols, 3 D G EN is unable to gen-
We then use Wireshark to label the tests, obtaining both                  erate a specification that passes on the test set labeled by
positive and negative test cases.                                         Wireshark. We investigate the cause of the errors and find
   Using Wireshark to label packets comes with its own chal-              in all cases that 3 D G EN generates a specification that is
lenges. For starters, Wireshark is a protocol analyzer typically          consistent with the header format described in the RFC, but
used for diagnostics and experimentation and, by design, does             that Wireshark labels packets as valid despite there being
not always enforce all constraints when validating a packet.              constraint violations, i.e., Wireshark does not fully enforce
Wireshark does not implement a dissector for a single RFC,                the RFC. In some cases, Wireshark emits a warning about
but rather for a family of RFCs. Thus, a dissector may be                 these violations, which can be filtered on a case-by-case basis.
more permissive compared to a given RFC, perhaps because                  However, this is not a straightforward task as some warnings
a related RFC mandates such a behavior—our experiments in                 do not impact the data format specification, e.g., Wireshark
Section V uncover many such unenforced constraints. To label              emits a warning when a packet indicates the TCP connection
a test case produced by 3 D T EST G EN, we rely on a Wireshark            is reset. Besides, in most cases a warning is not reported.
feature called Export PDU, which allows validating a given                   Using the RFC as a guide, two authors manually identified
packet header without encapsulating it within outer protocol              tests that Wireshark labels too permissively and corrected the
headers. Two exceptions were Ethernet, which does not re-                 labels. Using these corrected labels, we checked if any of the
quire outer encapsulation; and TFTP which is not supported                3 D G EN generated specifications already pass on this modified
by Export PDU. We wrapped TFTP headers generated by                       test set, or else restart the 3 D G EN loop with the corrected tests.
3 D T EST G EN with a dummy UDP header. For Ethernet, IPv4,               Protocols for which 3 D G EN is able to generate a specification
IPv6, VXLan, TCP, and UDP, we also had to generate dummy                  that passes on the corrected test set are denoted as (1*) in
payloads to prevent Wireshark from raising trivial errors. We             Table II—3 D G EN is able to generate at least one candidate
also had to disable checksums, since this is not enforced at              specification that is consistent with the labels in all cases.
the level of the formats. As such, using Wireshark as a labeler              1) Labeler and RFC disagreement
for 3 D T EST G EN outputs involved a non-trivial effort.                    We look more closely at examples where Wireshark is
                                                                          too permissive: Table III details the cause(s) of disagreement
D. Handwritten 3D Specifications
                                                                          between the Wireshark labels and the constraints specified by
   The EverParse GitHub5 repository contains 3D specifica-                the RFC in each case.
tions for seven network protocols, written by the authors of                 For example, for RTP, RFC 35506 states that the version
EverParse. Protocols with an existing handwritten 3D speci-               field is 2 bits and “The version defined by this specification
fication are marked with a * in Table I. In Section V-C we                is two (2)”. Although the RFC does not indicate a strong
use 3 D T EST G EN to compare the specifications generated by             constraint that the version field must be set to 2, a large number
3 D G EN to the seven handwritten specifications. We report if            of negative packets in the RTP test set include version numbers
any of the specifications produced by 3 D G EN are semantically           other than 2. Wireshark labels these packets as acceptable,
equivalent to the handwritten specifications, and otherwise use           however the 3 D G EN agent consistently generates a specifica-
the generated set of tests to identify the cause(s) of differences.       tion with UINT16BE Version:2 {Version == 2}. In this case, the
  5 https://github.com/project-everest/everparse                            6 https://www.ietf.org/rfc/rfc3550.txt




                                                                      7
                                                                        that 3D supports (UINT8, UINT16, UINT32, UINT64 and their BE
                                                                        counterparts) and refraining from using reserved keywords like
                                                                        ‘type’ as identifier names also require refinement steps. On the
                                                                        other hand, the agents are able to easily learn some other 3D
                                                                        specific constructs, such as the consume−all notation. We also
                                                                        observe that semantic mistakes, i.e., incorrect specifications,
                                                                        can stem from the agent’s difficulty in understanding the
                                                                        natural language in the RFC document. Figure 2 shows one
                                                                        such example for VXLAN. The RFC describes the fields in
                                                                        the header in natural language, and also provides an ASCII
                                                                        diagram. However, the natural language description of the
                                                                        fields do not indicate the order in which the different values
                                                                        should occur in the VXLAN header, and without the ASCII
                                                                        diagram a reader would not be able to correctly interpret the
                                                                        RFC. The agent first produces a specification which is then
                                                                        executed using 3DE XEC, resulting in a parsing error on the
                                                                        flags field, for one of the tests in the test set. Then the agent
                                                                        reflects on the result of 3DE XEC and determines that the
Fig. 2: Example of a packet refinement loop by the 3 D G EN agent       parsing failed due to the mis-ordering of the Reserved and
for VXLAN RFC 7348
                                                                        I fields. It then refined the specification by flipping the order
                                                                        of the fields (4) and produces a candidate that passes on all
agent is unable to learn from feedback about why a test with            tests. Interestingly, the language in the RFC first describes the
                                                                        I flag and then says specifies the values of the other 7 bits,
a different version value should pass, because Wireshark does
not provide any warning. Enforcing this constraint by changing          without indicating that there are 4 reserved bits, followed by
the Wireshark label to negative allows the specification to pass        an I bit, followed by the remaining 3 bits. Ambiguities in the
all tests.                                                              RFC language may cause the agent to misinterpret the true
   Similarly for TFTP, RFC 13507 states that a TFTP header              intent.
                                                                         Result 1: 3 D G EN is able to generate syntactically correct 3D
contains a 2 byte opcode field and enumerates 5 possible
                                                                         code, and learn from mistakes to refine specifications. Even in
opcode values. 3 D G EN always produces a specification con-             the presence of a noisy labeler and non-exhaustive tests, 3DGen
straining the value of the opcode field to one of the 5 values in        enables users to leverage the generated specifications to align the
the RFC. Wireshark does not label packets with other opcode              test set with the RFC, yielding specifications that pass all aligned
values as malformed. When we manually label tests with                   tests for all 20 network protocols.
incorrect opcode fields as negative, the specification generated
by 3 D G EN passes on the test set.
                                                                                            Accepted        Avg. Syntax     Avg. Packet
   In the case of GRE, RFC 27848 states “The Version Number                    Protocol
                                                                                              (x/5)         Refinements     Refinements
field MUST contain the value zero”. However, Wireshark does
                                                                               UDP              5               0.3               0
not enforce version constraints on GRE, likely because the for                 ICMP          0 (1∗ )            7.5               6
the PPTP variant of GRE, the version field is set to 1, and                    VXLAN         0 (2∗ )            7.6              7.4
                                                                               IPV6          0 (1∗ )            7.8              2.0
Wireshark uses the same dissector for all GRE versions.                        IPV4             2                 4              11
   In the case of IPV6, the generated specification consistently               Ethernet      0 (1∗)            11.4              4.6
fails to reject packets labeled as malformed by Wireshark. The                 TCP           0 (2∗)            10.2              2.5
                                                                               GRE           0 (1∗)            10.4              4.6
IPV6 NextHeader field indicates the value of the encapsulated                  DHCP             2               8.2               0
packet, however the RFC focuses only on the constraints of                     DCCP             1              14.25            0.75
                                                                               TPKT          0 (1∗ )            5.0              6.6
a single layer, not of any encapsulated packets. In contrast,                  ARP              3               4.8              1.8
Wireshark validates packet contents across layers and rejects                  NTP              3               7.4               3
                                                                               NBNS             1               4.6               4
packets that don’t encapsulate the next layer correctly.                       IGMP             5               3.8               0
   2) Agent Mistakes                                                           NSH              1               11.0             2.0
                                                                               TFTP          0 (1∗ )             11               1
   From Table II, we observe that the agents frequently make                   RTP           0 (1∗ )              3              12
syntax mistakes, despite having access to the language manual                  PPP           0 (1∗ )            7.6               5
for the 3D language. However, given that 3D is not yet a                       OSPFv3        0 (1∗ )           13.6               2
widely used DSL, syntax mistakes from a model like GPT-4                                  pass@5: (45%)   pass*@5: (100%)
are anticipated. We observe that the agents struggle most with          TABLE II: Results of 3 D G EN for 20 network protocols. * denotes
using correct 3D bitfield notation. Using only the primitives           protocols for which the test labels were adjusted to be consistent with
                                                                        the RFC.
  7 https://datatracker.ietf.org/doc/html/rfc1350
  8 https://datatracker.ietf.org/doc/html/rfc2784




                                                                    8
                                                                                                      # Distinct
                                                            Wireshark       Protocol   # Candidates                Divergent Fields
Protocol   Detected RFC vs Wireshark Disagreement                                                     Candidates
                                                            Message
                                                                            UDP             5             2        Optional Data[:consume-all] field
ICMP       Header length constraints                       None             IPV4            2             2        Additional constraints on Flag values
                                                                            VXLAN           2             1        None
Ethernet   Ethertype payload length                        None
                                                                                                                    options field length
                                                                            DHCP            2             2
           Reserved bits must be 0                         None                                                     Additional constraints on Flags field

VXLAN      I flag must be 1                                None             ARP             3             2        Incorrect additional remainder[:consume-all] field
           Header must be 8 bytes                          None             NTP             3             3        Additional constraints on LeapIndicator, Status, Type fields
                                                                            IGMP            5             3        Optional OtherFields[:consume-all]
IPV6       Payload Length exceeds framing length           Warning
                                                                            TCP             2             2        Constraints on Options field
           Reserved0 must be zero                          None                    TABLE IV: Semantically distinct candidate specifications
GRE
           Version number must be zero                     None
TFTP       Opcode fields must be between 0-5               None
           Window fields must not be zero                  Warning          ification has a field: UINT16BE flags:3 { flags == Reserved0
TCP
           ACK number must be consistent with ACK flag     Warning
                                                                            || flags == DF || flags == MF }, where Reserved0, DF, MF are
           Version field must be 3                         None
TPKT
           Reserved field must be 8 bits                   None
                                                                            equal to 0, 1, and 2, which is consistent with the RFC. The
                                                                            second specification has the same field as UINT16BE Flags:3
           Code field must be between 1-11                 None
PPP        Length field must be 1 octet, at least size 4   None             and does not enforce constraints on the value. While these
           Data must be constrained by Length              None             constraints should be added to be consistent with the RFC,
RTP        Version must be 2                               None             the test set did not contain a test violating this constraint, thus
           Version field must not be 3                     None             both specifications were able to pass the test set.
OSPF       Reserved field must be 0                        None                 In both the cases of ARP and IPV4, 3 D T EST G EN labels
           Header length must be 16 bytes                  None             the one specification as more permissive than the other, e.g.
TABLE III: Constraints specified in the RFC, that wireshark does            for IPV4 every test that passes on the first specification also
not enforce.                                                                passes on the second, but not the other way around. For both of
                                                                            these cases, the stricter specification correctly implements the
                                                                            RFC. Thus, a user of 3 D G EN could decide to always accept the
B. Distinguishing Candidates with Differential Testing                      stricter specification as a pruning heuristic between candidates.
   In many cases, 3 D G EN produces multiple specifications that              Result 2: Multiple distinct specifications may be produced by
                                                                              3 D G EN for a single protocol, and the degree to which they diverge
are compatible with the test set. In this section, we aim to                  is dependent on the quality and coverage of the test suite on which
answer the following question:                                                they are evaluated. 3 D T EST G EN helps by finding differentiating
RQ2: How do candidate format specifications generated for                     tests or by grouping equivalent candidates, allowing users to focus
the same protocol differ?                                                     on a semantic differences exhibited by concrete test cases.
   We make use of 3 D T EST G EN to help us answer this
question, in particular its differential testing feature, to find           C. 3 D G EN vs. Human Written Specs
tests that distinguish specifications or prove them semantically               The authors of EverParse provide specifications for 7 out of
equivalent. Distinguishing tests, if any, can be surfaced to                the 20 protocols we ran 3 D G EN on. In this section, we ask:
the user, along with feedback from 3 D T EST G EN localizing                RQ3: How do format specifications generated by 3 D G EN
semantic differences in 3D specifications, to help the user                 compare to handwritten specifications?
identify their desired specification.                                          As before, we use 3 D T EST G EN’s differential testing to se-
   Table IV shows protocols for which 3 D G EN generates mul-               mantically compare 3 D G EN’s specifications to the handwritten
tiple candidate specifications, and the results of 3 D T EST G EN’s         ones, with the results in Table V. For IPV6 and Ethernet,
differential testing between every pair of candidates, with a de-           3 D T EST G EN proves that the specifications are equivalent,
scription of the differences found, if any. Out of 8 protocols, 7           though syntactically distinct.
have at least two semantically distinct specifications, whereas                For UDP, ICMP, and VXLAN, we use 3 D T EST G EN to
for VXLAN the two candidates are semantically equivalent.                   identify tests that distinguish the handwritten and generated
   For example, for ARP, 3 D G EN generates 3 candidate spec-               specifications. In all three cases, the root cause is incorrect or
ifications, two which are semantically equivalent, whereas the              missing constraints in the handwritten specifications, demon-
third mistakenly adds a field to the end of the ARP header                  strating that even experts make mistakes when interpreting
UINT8 remainder[:consume-all]. This field consumes the rest                 RFCs as 3D, and that 3 D G EN can help in ensuring consistency
of the data in the packet and is often used for optional variable           with RFCs. For UDP, the handwritten specification is missing
length fields. The ARP RFC 826 does not describe such a field,              a constraint on the Length field that exists in the 3 D G EN
and the specification is incorrect but passes the test set because          specification. For ICMP, the Unused Bytes field is too short,
there is no negative-label test for which there is additional data          misinterpreting the 32 bytes as 32 bits. Similarly, in VXLAN,
at the end of the ARP header.                                               the VXLanID is two bytes short. After correcting the hand-
   3 D G EN generates two candidate specifications for IPV4,                written specification, 3 D T EST G EN proves them equivalent to
and 3 D T EST G EN find a test that distinguishes them. One spec-           the 3 D G EN generated specifications. Pull requests with the



                                                                        9
revised specifications were merged into EverParse for all three                                    input-output examples as specifications [21], constrained by
protocols.                                                                                         restrictions on syntax (e.g., SyGuS [22]). These restrictions
   On the other hand, for TCP and IPV4, the 3 D G EN spec-                                         make it difficult to apply them for new domains with formal
ification is missing constraints that exist in the handwritten                                     guarantees. Office Domain Specific Language (ODSL) [23]
specification. For TCP, although the produced specification                                        has been proposed as an intermediate layer for LLMs to
passes on the set of tests, it is underconstrained and does                                        translate natural language user commands to programs over
not include a condition checking if the SYN flag is set to 1                                       Office APIs. Although it shares our motivation for using 3D
and it does not implement all possible constraints for different                                   as a DSL, generated programs from ODSL do not have any
Max Segment Size payloads. Instead it includes size constraints                                    formal guarantees since the generated programs lack a formal
that are general to all options.                                                                   notion of correctness and there is no symbolic encoding of
   For IPV4, there are missing constraints on the IHL,                                             programs in ODSL into a logical formula.
TotalLength, and Options fields, which indicates that tests                                           Closer to our setting, Ticoder [24] uses LLMs to partially
labeled by Wireshark do not capture these constraints. We ex-                                      formalize user-intent as tests. Unlike 3 D G EN, TiCoder requires
plore whether 3 D G EN would be able to generate an equivalent                                     a user in the loop to validate each test, relies on an LLM-
specification, if it had access to a set of tests that can capture                                 based test generation that cannot be as exhaustive as our
the missing constraints. To do this, we use 3 D T EST G EN                                         symbolic technique and cannot provide any formal guarantees
to generate positive and negative tests from the handwritten                                       on the generated code. Endres et al. [25] generate declarative
specification, guaranteeing that tests exercising the constraints                                  postconditions in Java and Python using LLMs and evaluate
will be included in the test set. With these tests, 3 D G EN                                       the quality of specifications offline using validation tests, but
is able to produce two passing specifications that contain                                         do not generate tests or verified code. Misu et al. [26] generate
the missing constraints, after an average of 11 syntax and                                         formal specifications and code that satisfies such specifications
4 packet refinements. The generated specifications are both                                        in Dafny programming language using LLMs, but there is no
semantically equivalent to the handwritten specification.                                          automation in helping the user establish the correctness of the
 Result 3: 3 D G EN is able to produce 3D specifications semantically                              specifications.
 equivalent to human written 3D. In addition, using our framework                                     All these approaches are evaluated for a simple setup
 we were able to uncover three bugs in existing handwritten 3D                                     where the requirements are present as a few line docstrings,
 code for UDP, ICMP, and VXLAN, highlighting the difficulties in                                   and do not require problem decomposition or the translation
 translating RFCs into correct implementations.
                                                                                                   of requirements from complex documents such as RFCs.
                                                                                                   SAGE [27] uses natural language processing (NLP) techniques
Protocol   Equivalent?   Root Cause Divergence                               After H.S. Fix        to translate informal requirements in RFCs into protocol
UDP                      H.S. Missing constraint on Length field             ✓                     implementations semi-automatically. SAGE extracts and sur-
ICMP                     H.S. UNUSED BYTES type too short                    ✓
VXLAN                    H.S. VXLanID field too short                        ✓                     faces ambiguities in RFCs through an intermediate logical
IPV6           ✓         None                                                n/a
IPV4                     G.S Missing value constraints on IHL, TotalLength   n/a
                                                                                                   form, that are resolved by the user, before generating code.
Ethernet       ✓         None                                                n/a                   Unlike 3DG EN, SAGE can generate protocol implementation
TCP                      G.S. Missing constraints on options payload         n/a
                                                                                                   in addition to the parser; however, the generated code may
TABLE V: Comparison of 3 D G EN generated specifications to hand-
written specifications (denoted H.S.). We list the cause(s) of diver-                              have functional and security bugs, as it lacks formal specifi-
gence, and where applicable, we correct the handwritten specification.                             cations. Extending 3DG EN and the 3D language to support
                                                                                                   full protocol implementation would be interesting avenue for
                                                                                                   future work.
                            VI. R ELATED W ORK                                                                           VII. C ONCLUSION
   LLMs have enabled generating code from informal natural                                            Programming in natural language using AI is a powerful
language requirements, and have shown ability to generate                                          new capability. But, for AI-based program synthesizers to
human like code on benchmark problems [15], [16] – however,                                        be truly useful, they must also be trustworthy. We believe
they come with no guarantees, and have been known to contain                                       coupling AI programming assistants with symbolic tools to
bugs and security errors [17]. Alphacode [18] and CodeT [19]                                       support intent formalization and refinement, as well guarantees
have used tests to cluster and rank generated code to improve                                      about generated outputs, is a key step towards fully realizing
the empirical accuracy on benchmarks; however they do not                                          their potential. We have explored this idea, showing it is
add trust to the generated code as the natural language does                                       possible to synthesize verified binary format parsers from
not impose any correctness checks.                                                                 specification documents using AI agents, while providing
   On the other hand, classical program synthesis [20] for-                                        symbolic test-case generators to help both humans and AIs
mulates the problem of generating code that meets a formal                                         confirm and refine intent, and verification tools to ensure that
specification. However, these techniques are limited due to                                        intent is preserved down to executable C code. As a next
lack of availability of formal specifications, along with the                                      step, we plan to evaluate our approach through user studies to
intractable theoretical complexity of the synthesis. Lately,                                       assess whether tools like 3 D G EN more easily enable humans
program synthesis has been applied in restricted domains with                                      to author correct-by-construction programs in new DSLs.



                                                                                              10
                             R EFERENCES                                             [19] B. Chen, F. Zhang, A. Nguyen, D. Zan, Z. Lin, J.-G. Lou, and
                                                                                          W. Chen, “Codet: Code generation with generated tests,” 2022.
 [1] J. Bangert and N. Zeldovich, “Nail: A practical tool for parsing                     [Online]. Available: https://arxiv.org/abs/2207.10397
     and generating data formats,” in 11th USENIX Symposium on                       [20] Z. Manna and R. Waldinger, “A deductive approach to program
     Operating Systems Design and Implementation (OSDI 14). Broomfield,                   synthesis,” ACM Trans. Program. Lang. Syst., vol. 2, no. 1, p. 90–121,
     CO: USENIX Association, Oct. 2014, pp. 615–628. [Online].                            jan 1980. [Online]. Available: https://doi.org/10.1145/357084.357090
     Available: https://www.usenix.org/conference/osdi14/technical-sessions/         [21] S. Gulwani, O. Polozov, and R. Singh, “Program synthesis,” Found.
     presentation/bangert                                                                 Trends Program. Lang., vol. 4, no. 1-2, pp. 1–119, 2017. [Online].
 [2] T. Ramananandro, A. Delignat-Lavaud, C. Fournet, N. Swamy, T. Cha-                   Available: https://doi.org/10.1561/2500000010
     jed, N. Kobeissi, and J. Protzenko, “Everparse: Verified secure zero-           [22] R. Alur, R. Bodı́k, G. Juniwal, M. M. K. Martin, M. Raghothaman,
     copy parsers for authenticated message formats,” in Proceedings of the               S. A. Seshia, R. Singh, A. Solar-Lezama, E. Torlak, and A. Udupa,
     28th USENIX Conference on Security Symposium, ser. SEC’19. USA:                      “Syntax-guided synthesis,” in Formal Methods in Computer-Aided
     USENIX Association, 2019, p. 1465–1482.                                              Design, FMCAD 2013, Portland, OR, USA, October 20-23, 2013.
 [3] N. Swamy, T. Ramananandro, A. Rastogi, I. Spiridonova, H. Ni,                        IEEE, 2013, pp. 1–8. [Online]. Available: https://ieeexplore.ieee.org/
     D. Malloy, J. Vazquez, M. Tang, O. Cardona, and A. Gupta,                            document/6679385/
     “Hardening attack surfaces with formally proven binary format                   [23] A. Gandhi, T. Q. Nguyen, H. Jiao, R. Steen, and A. Bhatawdekar,
     parsers,” in Proceedings of the 43rd ACM SIGPLAN International                       “Natural language commanding via program synthesis,” 2023.
     Conference on Programming Language Design and Implementation                    [24] S. K. Lahiri, S. Fakhoury, A. Naik, G. Sakkas, S. Chakraborty,
     (PLDI ’22), June 13–17, 2022, San Diego, CA, USA, 2022. [Online].                    M. Musuvathi, P. Choudhury, C. von Veh, J. P. Inala, C. Wang,
     Available: https://www.fstar-lang.org/papers/EverParse3D.pdf                         and J. Gao, “Interactive code generation via test-driven user-intent
 [4] OpenAI, “Gpt-4 technical report,” 2023.                                              formalization,” CoRR, vol. abs/2208.05950, 2023. [Online]. Available:
 [5] J. Protzenko, J.-K. Zinzindohoué, A. Rastogi, T. Ramananandro,                      https://doi.org/10.48550/arXiv.2208.05950
     P. Wang, S. Zanella-Béguelin, A. Delignat-Lavaud, C. Hritcu,                   [25] M. Endres, S. Fakhoury, S. Chakraborty, and S. K. Lahiri, “Formalizing
     K. Bhargavan, C. Fournet, and N. Swamy, “Verified low-level                          natural language intent into program specifications via large language
     programming embedded in F*,” PACMPL, vol. 1, no. ICFP, pp. 17:1–                     models,” CoRR, vol. abs/2310.01831, 2023. [Online]. Available:
     17:29, Sep. 2017. [Online]. Available: http://arxiv.org/abs/1703.00053               https://doi.org/10.48550/arXiv.2310.01831
 [6] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao,           [26] M. Md Rakib Hossain Misu, C. V. Lopes, I. Ma, and J. Noble, “Towards
     “React: Synergizing reasoning and acting in language models,” arXiv                  ai-assisted synthesis of verified dafny methods,” 2024.
     preprint arXiv:2210.03629, 2022.                                                [27] J. Yen, T. Lévai, Q. Ye, X. Ren, R. Govindan, and B. Raghavan, “Semi-
 [7] Y. Gao, Y. Xiong, X. Gao, K. Jia, J. Pan, Y. Bi, Y. Dai, J. Sun, and                 automated protocol disambiguation and code generation,” in Proceedings
     H. Wang, “Retrieval-augmented generation for large language models:                  of the 2021 ACM SIGCOMM 2021 Conference, ser. SIGCOMM ’21.
     A survey,” arXiv preprint arXiv:2312.10997, 2023.                                    New York, NY, USA: Association for Computing Machinery, 2021, p.
 [8] Z. Xi, W. Chen, X. Guo, W. He, Y. Ding, B. Hong, M. Zhang, J. Wang,                  272–286. [Online]. Available: https://doi.org/10.1145/3452296.3472910
     S. Jin, E. Zhou et al., “The rise and potential of large language model
     based agents: A survey,” arXiv preprint arXiv:2309.07864, 2023.
 [9] L. Wang, C. Ma, X. Feng, Z. Zhang, H. Yang, J. Zhang, Z. Chen,
     J. Tang, X. Chen, Y. Lin et al., “A survey on large language model
     based autonomous agents,” arXiv preprint arXiv:2308.11432, 2023.
[10] Y. Du, S. Li, A. Torralba, J. B. Tenenbaum, and I. Mordatch, “Improving
     factuality and reasoning in language models through multiagent debate,”
     arXiv preprint arXiv:2305.14325, 2023.
[11] C. Qian, X. Cong, C. Yang, W. Chen, Y. Su, J. Xu, Z. Liu, and
     M. Sun, “Communicative agents for software development,” arXiv
     preprint arXiv:2307.07924, 2023.
[12] Q. Wu, G. Bansal, J. Zhang, Y. Wu, S. Zhang, E. Zhu, B. Li,
     L. Jiang, X. Zhang, and C. Wang, “Autogen: Enabling next-gen llm
     applications via multi-agent conversation framework,” arXiv preprint
     arXiv:2308.08155, 2023.
[13] C. Barrett, P. Fontaine, and C. Tinelli, “The Satisfiability Modulo
     Theories Library (SMT-LIB),” https://smtlib.cs.uiowa.edu/, 2016.
[14] L. De Moura and N. Bjørner, “Z3: An efficient smt solver,” in Tools
     and Algorithms for the Construction and Analysis of Systems: 14th
     International Conference, TACAS 2008, Held as Part of the Joint
     European Conferences on Theory and Practice of Software, ETAPS
     2008, Budapest, Hungary, March 29-April 6, 2008. Proceedings 14.
     Springer, 2008, pp. 337–340.
[15] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. d. O. Pinto, J. Kaplan,
     H. Edwards, Y. Burda, N. Joseph, G. Brockman et al., “Evaluating large
     language models trained on code,” arXiv preprint arXiv:2107.03374,
     2021.
[16] J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan,
     E. Jiang, C. Cai, M. Terry, Q. Le et al., “Program synthesis with large
     language models,” arXiv preprint arXiv:2108.07732, 2021.
[17] H. Pearce, B. Ahmad, B. Tan, B. Dolan-Gavitt, and R. Karri, “Asleep
     at the keyboard? assessing the security of github copilot’s code contri-
     butions,” in 2022 IEEE Symposium on Security and Privacy (SP), 2022,
     pp. 754–768.
[18] Y. Li, D. Choi, J. Chung, N. Kushman, J. Schrittwieser, R. Leblond,
     T. Eccles, J. Keeling, F. Gimeno, A. D. Lago, T. Hubert, P. Choy,
     C. d. M. d’Autume, I. Babuschkin, X. Chen, P.-S. Huang, J. Welbl,
     S. Gowal, A. Cherepanov, J. Molloy, D. J. Mankowitz, E. S.
     Robson, P. Kohli, N. de Freitas, K. Kavukcuoglu, and O. Vinyals,
     “Competition-level code generation with alphacode,” 2022. [Online].
     Available: https://arxiv.org/abs/2203.07814




                                                                                11
                           A PPENDIX                                            Metric (mean)       All Protocols      3 D G EN     H.S.
A. Branch coverage with 3DTestGen                                               LOC (3D)            26.2               33.14        60
                                                                                Fields              15.7               22.5         24.1
   In this supplement, we briefly cover how 3DTestGen pro-                      Constraints         3.4                4            5.14
duces tests that achieve branch coverage.                                       Casetypes           0.3                0.42         0.42
   Recall the message parser from Section III of the paper.                     Structs             2.75               4.14         4.14
It has has two branches and four paths: fail to parse the first                 Bitfields           3.35               4.71         4.71
byte; fail because the first byte is less than 42; fail to parse                Enum                0.15               0.00         0.42
the second byte; success.                                                       Consume-all         0.71               0.42         0.28
   Thus, to query Z3 for models that achieve a form of branch             TABLE VI: Highlevel characteristics of code produced by 3DGen.
                                                                          Mean is reported across all specifications. For the subset for which a
coverage, we instrument our encoding with branch tags—
                                                                          handwritten spec exists, the last two columns compare characteristics
in practice, 3DTestGen does not instrument every branch,                  between generated specifications (G.S.) and handwritten specifica-
heuristically only picking branches of interest, focusing on              tions (H.S.).
those that involve value constraints and casetypes.
   Next, we introduce a global uninterpreted function,
branch − trace, representing a trace of branches to be taken.
                                                                          of the generated specification to the correct handwritten spec-
The State argument to an encoded parser also contains a
                                                                          ification, if applicable, across all protocols. Table VII contains
branch − index component which records a position in the
                                                                          the full breakdown of metrics for each protocol.
branch trace. For a given branch trace, the encoding forces the
parser to follow that trace of branches. By querying Z3 while                In general, we observe that handwritten specifications have
fixing the branch trace, we obtain models of the Input that               on average, more lines of code (ignoring comments and empty
also are compatible with the trace, i.e., the Input is a byte             lines), than code generated by 3 D G EN. This could be due to
sequence that forces the parser to follow the branch trace.               formatting and stylistic choices. For example, in Figure 4, the
Then, by simply enumerating the traces up to a user-specified             handwritten specification adds extra lines around the version
branch depth in a depth-first fashion, we get Z3 to generate a            constraint, and extracts the version number into a defined
diversity of Input models that achieve branch coverage.                   variable, where the 3 D G EN spec uses a constant.
   We show a fragment of the parse message parser encoding                   While the mean is the same, we observe that the number of
augmented with branch tags below. Note how each branch                    bitfields can vary between the generated and handwritten spec-
of the constraint check for x > 42 is taken only if the                   ifications. An example of this can be seen in Figure 4, where
corresponding branch tag in the trace also permits it (0 if the           the handwritten specification divides the T raf f icClass and
constraint holds, 1 if it does not.)                                      F lowLabel fields. The 3 D G EN specification combined both of
                                                                          these fields into one T raf f icClassF lowLabel field of the
  (define−fun parse−message ((s0 State)) State                            appropriate size. There is no constraint on the value of this
    (let ((s1 (parse−uint8 s0)))
       (if (has−failed s1) s1                                             field in either specification, therefore, both specifications are
          (if (and (> (return−value s1) 42)                               semantically equivalent. On the other hand, Figure 3 shows
                   (= 0 (branch−trace (branch−index s1))))                an example of semantically equivalent specification where
              (parse−uint8 (incr−branch−index s1))
              (if (and (not (> (return−value s1) 42))                     3 D G EN represented the V lanT ag field with three bitfield
                       (= 1 (branch−trace (branch−index s1))))            variables P CP , DEI, and V ID.
                                                                             Interestingly, both 3 D G EN and the handwritten specifica-
  Now, to generate models that explore a given trace of
                                                                          tions contain the same number of casetypes, with a mean of
branches, we add the following assertions to the query to
                                                                          0.42 across the seven specifications for which a handwritten
constrain the prefix of the branch trace recorded by the parser.
                                                                          spec exists. The number of constraints in the 3 D G EN spec-
  (assert (= (branch−index init) 0)) ;; start from index 0.               ification is lower than that of the handwritten specifications,
  ;; take the first branch in message.                                    which follows from observations in RQ3, Table V, where the
  (assert (and (= (branch−trace 0) 0)))
  ;; make at least as many choices as branch−depth.                       IPV6 and TCP specifications are missing constraints.
  (assert (>= (branch−index (parse−message init))
                   branch−depth))
                                                                          C. Syntactic Characteristics of code produced by 3 D G EN
                                                                             Results of RQ3 in this work, as well as results from
B. Comparing code produced by 3DGen to Handwritten Spec-
                                                                          related work in the domain, confirm that accurately translating
   ifications
                                                                          nuanced and often ambiguous RFC specifications into correct
  We report the high level characteristics of code produced               code by hand is an error prone task and often laborious
by 3 D G EN in Table VI. For each characteristic (Lines of                task. Table VII contains several syntactic metrics of the code
code (LOC), number of constraints, etc.) we report the mean               generated by 3 D G EN for each protocol. Though these syntactic
across all valid specifications generated by 3 D G EN in the first        metrics may not serve as an ideal proxy for the complexity
column. In the last two columns, we compare characteristics               of a protocol’s data format specification, they do give some



                                                                     12
Fig. 3: Semantically equivalent 3D specification for Ethernet II frames in VXLAN. (Left) Handwritten Specification, (Right) 3 D G EN
Specification.




       Fig. 4: Semantically equivalent 3D specification for IPV6. (Left) Handwritten Specification, (Right) 3 D G EN Specification.




                                                                   13
       #    Protocol   LOC (C)     LOC (3D)     Fields   Constraints       Casetypes   Structs   Bitfields   Enum    Consume-all
       1    UDP           158           7          4          1                0          1          0         0           0
            H.S.          158           8          4          1                0          1          0         0           0
       2    ICMPv4       1208          99         72          11               1          12         0         0           2
            H.S.         2119          164        61           6               1          13         0         3           1
       3    VXLAN         296          16         10          7                0          3          5         0           0
            H.S.          266          10          7          6                0          1          3         0           0
       4    IPV6          341          10          7          1                0          1          2         0           0
            H.S.          427          16          7          1                0          1          3         0           0
       5    IPV4          544          30         25          5                0          3         15         0           0
            H.S.          534          35         15          5                0          2          6         0           0
       6    TCP           615           45        27           3               1          5          8         0           1
            H.S.         1445          161        64          17               1          8         21         0           1
       7    Ethernet      352          25         13          0                1          4          3         0           0
            H.S.          353          26         11          0                1          3          0         0           0

       8    GRE           309          22         12           0               1          3          3         0           1
       9    IGMPv2        223          10          4           4               0          1          0         0           0
      10    DHCP          838          25         18           5               0          3          0         0           0
      11    DCCP          491          38         17           0               1          3          4         1           1
      12    ARP           530          12         10           0               0          1          0         0           0
      13    NTP           497          35         15           3               0          2          3         0           1
      14    NBNS          416          17         15          14               0          1         10         0           0
      15    NSH           486          24         16           1               0          4          8         0           1
      16    TFTP          304          43         15           7               1          1          0         0           4
      17    RTP           320          17         13           1               0          2          6         0           1
      18    PPP           270          20          6           1               0          1          0         1           1
      19    TPKT          232           6          4           3               0          1          0         0           0
      20    OSPF          351          23         11           1               0          3          0         1           1

TABLE VII: Syntactic metrics of 3D code produced by 3 D G EN and the handwritten specification (H.S.) for each of the 20 protocols used
in this work.



insight into the relative complexity and structural elements of         to specify the data type.
the generated code.                                                        Interestingly, the number of lines of C code produced for
   We report both the lines of 3D code generated by 3 D G EN            each of the formats is several factors larger than the size of
as well as the lines of C code automatically generated from             the 3D specification, for several reasons. First, designed as
the 3D specification by Everparse. Overall, we observe a                as declarative specification language, 3D is inherently more
modest range of lines of 3D code generated for the 20 selected          compact than imperative C code that implements a parser,
protocols, 3 D G EN generated as little as 6 (TPKT) and at most         e.g., the parser implementation has to repeatedly check if
99 (ICMP) lines of code. Intuitively, the number of fields              there is enough space left in the input buffer to parse the
follows overall lines of code, ranging from 4 (IGMP, TPKT)              next field. Further, the C code includes various features that
to 72 (ICMP). Although we observe only a modest numbers of              are important for a practical parser, including error handling
lines of 3D code generated, the lines of auto-generated C code          logic—such error handling is not present in individual 3D
to correctly parse these specifications is considerably larger—         specifications and is instead baked into the definition of the
we comment more on this shortly.                                        3D language. This points to the benefit of using a compact
                                                                        specification language as a target for AI-generation—many
   The number of structs, bitfields, enums, and consume-all             features can be incorporated into the language definition, rather
types used varies based on the protocol specification. The              than having the programmer specify them repeatedly for every
number of value constraints can indicate increasing nuance              program. Directly generating, say, 1K lines of C code for an
in the data specification. For example, NBNS spans 17 lines             ICMP parser, even if it could be AI-generated, would pose
of code but contains 14 constraints, as measured by boolean             a difficult program verification problem; using a DSL like
operators. This is because of the 10 bitfields, 8 have value            3D enables analysis such as symbolic test-case generation to
constraints defined in the NBNS RFC 1002. The NM_FLAGS                  systematically test and refine AI generated code, and correct-
field defines value constraints for each flag of either 0 or            by-construction code generation ultimately yields verified C
1. The casetypes field appears to be a reliable indicator if            code.
the protocol contains multiple message types, however for the
protocols studied there is never more than one casetype needed



                                                                   14
