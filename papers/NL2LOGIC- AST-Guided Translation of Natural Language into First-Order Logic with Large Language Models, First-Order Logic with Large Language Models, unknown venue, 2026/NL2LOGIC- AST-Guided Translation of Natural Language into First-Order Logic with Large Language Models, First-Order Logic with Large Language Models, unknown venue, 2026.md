                                                NL2L OGIC: AST-Guided Translation of Natural Language into
                                                      First-Order Logic with Large Language Models
                                             Rizky Ramadhana Putra1 , Raihan Sultan Pasha Basuki2 , Yutong Cheng1 , Peng Gao1
                                                                           1
                                                                         Virginia Tech, Blacksburg, VA, USA
                                                                       2
                                                                      Universitas Ary Ginanjar, Jakarta, Indonesia
                                                                     {rizky, yutongcheng, penggao}@vt.edu
                                                                  raihansultan.pashabasuki@students.uag.ac.id

                                                               Abstract                         where models assess whether a claim is entailed
                                                                                                by supporting evidence. Early approaches rely on
                                             Automated reasoning is critical in domains
                                                                                                neural entailment frameworks (Evans et al., 2018;
arXiv:2602.13237v1 [cs.AI] 29 Jan 2026




                                             such as law and governance, where verifying
                                             claims against facts in documents requires both    Bowman et al., 2015; Rocktaschel et al., 2016)
                                             accuracy and interpretability. Recent work has     that employ neural networks to classify entailment
                                             adopted a structured reasoning paradigm that       and contradiction. However, these models remain
                                             parses first-order logic (FOL) rules from nat-     opaque black boxes, lacking interpretability and
                                             ural language and delegates inference to au-       formal verifiability. To improve transparency and
                                             tomated solvers. With the rise of large lan-
                                                                                                explainability, recent research introduces a struc-
                                             guage models (LLMs), methods such as GCD
                                             and CODE4LOGIC leverage their reasoning
                                                                                                tured reasoning paradigm that first derives explicit
                                             and code generation capabilities to enhance        logical representations from text and then verifies
                                             logic parsing. However, these approaches suf-      claims through automated reasoning engines. This
                                             fer from (1) fragile syntax control, due to weak   transition improves inference transparency and au-
                                             enforcement of global grammar consistency,         ditability by explicitly representing intermediate
                                             and (2) low semantic faithfulness, as they lack    proof steps, rather than only final results.
                                             fine-grained clause-level semantic understand-        In recent years, Large Language Models (LLMs)
                                             ing. To address these challenges, we propose
                                                                                                have shown notable progress in logical reasoning,
                                             NL2L OGIC, a FOL translation framework that
                                             uses an AST as an intermediate layer, com-         particularly when guided by prompting strategies
                                             bining a recursive LLM-based semantic parser       such as few-shot examples and Chain-of-Thought
                                             with an AST-guided generator that determinis-      (CoT) prompting. Building on this progress, recent
                                             tically produces solver-ready code. On the FO-     research has developed LLM-powered approaches
                                             LIO, LogicNLI, and ProofWriter benchmarks,         for translating natural language (NL) into first-
                                             NL2L OGIC attains 99% syntactic accuracy and       order logic (FOL), leveraging the models’ strong
                                             improves semantic correctness by 30% over
                                                                                                natural language understanding and code gener-
                                             state-of-the-art baselines. Moreover, integrat-
                                             ing NL2L OGIC into Logic-LM yields near-
                                                                                                ation capabilities to enable automated reasoning
                                             perfect executability and improves downstream      with explicit semantics such as FOL.
                                             reasoning accuracy by 31% over Logic-LM’s             To improve NL-to-FOL translation performance,
                                             original few-shot unconstrained FOL transla-       several approaches have developed specialized
                                             tion module.                                       pipelines that enhance LLMs with additional struc-
                                                                                                tural guidance and symbolic control. A repre-
                                         1   Introduction
                                                                                                sentative work, Grammar-Constrained Decoding
                                         Natural language documents, especially in domains      (GCD) (Raspanti et al., 2025), enforces token-level
                                         such as law, policy, and governance, encode com-       syntactic correctness by encoding the target formal
                                         plex logical relations that must be interpreted pre-   language as a context-free grammar and constrain-
                                         cisely for downstream reasoning and compliance         ing the LLM’s decoding process to adhere to this
                                         checking. However, natural language is inherently      grammar. CODE4LOGIC (Liu, 2025) adopts a
                                         ambiguous and unstructured, making it difficult        complementary approach. It leverages the code un-
                                         for machines, and even humans, to ensure logical       derstanding capability of code generation models.
                                         consistency, detect contradictions, or verify claims   Rather than generating FOL formulas directly, it
                                         across documents. This gap has motivated research      uses few-shot prompting to produce Python code
                                         on automated reasoning over natural language,          that encodes the grammar tree, which, when exe-
cuted, generates the corresponding FOL rule.             scoped expressions following solver-specific gram-
  Despite their contributions, these methods face        mar. This design enforces strict syntactic validity
two key limitations:                                     while preserving semantic alignment, producing ex-
                                                         ecutable logical rules compatible with solvers such
• Fragile syntax control. GCD restricts genera-          as Z3 (De Moura and Bjørner, 2008) and SMT-LIB
  tion at the token level through context-free gram-     (Barrett et al., 2010).
  mars. While this enforces local syntactic correct-        We evaluate NL2L OGIC on three widely used
  ness, grammatically valid outputs do not neces-        natural language inference (NLI) datasets, FO-
  sarily constitute valid logical statements, such as    LIO (Han et al., 2024), ProofWriter (Tafjord et al.,
  those requiring variable or signature consistency.     2021), and LogicNLI (Tian et al., 2021), using the
  CODE4LOGIC uses in-context learning (ICL) to           Z3 reasoning engine for consistent formal verifica-
  generate a grammar tree and guides subsequent          tion. We also integrate NL2L OGIC into Logic-
  code generation with this structure. However,          LM (Pan et al., 2023), a representative neuro-
  despite leveraging ICL, the free-form generation       symbolic framework, demonstrating its practical
  process remains prone to hallucination, and any        value as a modular component.
  errors in the tree can propagate into the follow-
                                                            The evaluation addresses three research ques-
  ing code generation stage, leading to invalid or
                                                         tions: (RQ1) whether the generated formulas are
  inconsistent outputs.
                                                         syntactically valid; (RQ2) whether they preserve
• Limited semantic faithfulness. Existing ap-            the intended semantics for entailment prediction;
  proaches formulate NL–to–FOL translation as            (RQ3) whether the integration of NL2L OGIC im-
  a single-step text-to-text task, mapping entire        proves existing neuro-symbolic systems. Across
  paragraphs to complete logical programs and            twelve models ranging from 0.5B to 27B parame-
  forcing models to perform comprehension and            ters, NL2L OGIC achieves near-perfect syntax cor-
  translation simultaneously. Handling each clause       rectness, improves semantic accuracy by an av-
  iteratively is essential, as clauses often encode      erage of 30% over the strongest baseline (GCD),
  complex logical relations that can overwhelm           and improves the existing neuro-symbolic frame-
  the LLM if processed and translated all at once.       work by 31% on downstream reasoning task over
  Without this iterative decomposition, the LLM          Logic-LM’s original unconstrained FOL transla-
  tends to rely on shallow token prediction rather       tion module. These results demonstrate that our
  than genuine logical understanding, making hal-        decoupled, AST-based design provides stronger
  lucinations more likely when sentence structures       syntactic control and more faithful semantic align-
  become complex.                                        ment, advancing automated reasoning over natural
                                                         language through formal, interpretable symbolic
   To address these limitations, we propose              representations.
NL2L OGIC, a framework that translates natural              To facilitate future research, we release
language sentences into semantically faithful and        our implementation at: https://github.com/
syntactically correct logical rules. Rather than         peng-gao-lab/nl2logic.
adopting an imprecise, unconstrained, and single-
step approach, the semantic parser decomposes            2   Related Work
each sentence into clauses and iteratively extract-
ing first-order logic components (e.g., predicates,      Natural Language to Formal Logic Transla-
quantifiers, and logical connectives) to construct a     tion. Research on formal logic translation has
First-Order Logic Abstract Syntax Tree (FOLAST).         evolved across several paradigms. Early rule-based
Parsing each clause iteratively enables the model        methods (Bos and Markert, 2005; Zettlemoyer
to make controlled, grammar-guided decisions, en-        and Collins, 2012; Barker-Plummer et al., 2009;
suring clause-level accuracy that composes into a        Abzianidze, 2017) offer precise control but lack
globally coherent logical representation.                robustness to linguistic variation. Neural models
   Then, the AST-guided generator ensures syn-           later generated logical forms directly from text (Lu
tactic correctness by deterministically compiling        et al., 2022; Cao et al., 2019), improving gener-
the FOLAST through a two-pass algorithm: the             alization but struggling with rare operators and
first pass registers all constants, variables, and re-   complex syntax. More recently, neuro-symbolic
lation signatures, while the second pass assembles       systems commonly adopt unconstrained few-shot
LLM translation integrated with logic solvers (Pan         will be executed by automated reasoning engines.
et al., 2023; Olausson et al., 2023; Xu et al., 2024;      Reasoning Engines and Target Languages. Auto-
Sanyal et al., 2022; Quan et al., 2024, 2025). Struc-      mated reasoning engines such as Z3 (De Moura and
tured pipelines that add syntactic constraints (Ras-       Bjørner, 2008), Prover9 (McCune, 2005–2010),
panti et al., 2025; Liu, 2025) further improve per-        and SMT-LIB (Barrett et al., 2010) solvers evaluate
formance, yet the resulting formulas often remain          FOL statements for satisfiability, entailment, and
semantically unfaithful to the source text.                consistency. Each engine requires strict, engine-
LLMs for Logical Reasoning. The development                specific syntax, e.g., Z3’s Python API or SMT-
of logical reasoning capabilities in LLMs has seen         LIB’s symbolic format. However, these syntactic
significant progress through a range of approaches.        forms are rarely observed during LLM pretrain-
One line of work breaks down complex reasoning             ing. Hence, directly generating solver code in an
into intermediate steps, often referred to as chain-       end-to-end manner leads to high syntax errors and
of-thought prompting (Wei et al., 2022), while oth-        inconsistent logical structures. Our key insight is
ers show that simple step-by-step prompting can            to decouple logical parsing from code generation
yield similar benefits without explicit examples           by introducing an intermediate AST representation,
(Kojima et al., 2022). However, these approaches           which captures the logical structure in an engine-
lack the formal proof. To address this, some frame-        agnostic form and can then be deterministically
works combine LLMs with automated reasoning                compiled into the target reasoning language. This
tools to improve faithfulness (Creswell et al., 2022).     separation enforces syntactic correctness, facili-
Recent research has further explored integrating           tates multi-engine generalization, and avoids LLM
LLMs with symbolic solvers (Wang et al., 2023),            hallucinations tied to solver-specific syntax.
treating LLMs as logical parsers rather than inde-
pendent reasoners. In summary, prior work either           4     NL2L OGIC Design
lacks formal proof for logical reasoning or pro-
duces unfaithful logical forms due to overly simple,       NL2L OGIC adopts a parser-generator architecture
unconstrained translation methods.                         designed to ensure syntactic correctness and seman-
                                                           tic faithfulness in translating natural language into
3   Preliminary                                            formal logic. As illustrated in Fig. 1, the pipeline
                                                           consists of two stages: a semantic parser, which
First-Order Logic. First-Order Logic (FOL) is              converts natural language text into a structured first-
a formal system for expressing statements about            order logic abstract syntax tree (FOLAST), defined
entities, their properties, and relations (Enderton,       by the standard grammar in Fig. 2, and an AST-
2001). Its syntax comprises constants, variables,          guided generator, which compiles the FOLAST
functions, relations, quantifiers (e.g., ∀, ∃), and log-   into solver-executable code (e.g., Z3, SMT-LIB).
ical connectives (e.g., ∧, ∨, →, ¬). A well-formed         We next describe each component.
FOL formula such as ∀x. Human(x) → Mortal(x)
captures meaning in a precise, machine-verifiable          4.1    Preprocessing
form. Unlike natural language, FOL enforces strict         Documents are divided into well-defined sentences
grammar, enabling unambiguous interpretation and           leveraging prior work on sentence boundary de-
compatibility with automated reasoning systems.            tection, as directly feeding long paragraphs into
Abstract Syntax Tree. An Abstract Syntax Tree              the parser risks hallucination and error propa-
(AST) is a tree-based data structure, commonly             gation. Instead of rule-based splitting that re-
used in compilers and interpreters to represent            lies only on punctuation and heuristics, we adopt
the syntactic structure of a program (Alfred et al.,       SaT (Frohmann et al., 2024; Minixhofer et al.,
2007). Each node in an AST corresponds to a                2023), a learning-based model that predicts sen-
syntactic construct (e.g., operator, expression, dec-      tence boundaries using contextual and lexical cues.
laration), enabling structural analysis and system-        This ML-based approach distinguishes true sen-
atic code generation. We extend this concept to a          tence endings from punctuation used in abbrevi-
first-order logic AST (FOLAST) defined by the              ations (e.g., U.S., Prof.) or numeric expressions,
standard FOL grammar in Fig. 2, serving as a               thereby avoiding fragmentation errors. As a result,
backend-independent intermediate representation            each logical sentence is reliably isolated, providing
linking natural language to the generated code that        clean and accurate input to the semantic parser.
                                  ① PARSER                    LLM w/ In-                                                 GENERATOR                 ForAll




                                                                                                                                                                                   In specific target language (e.g., Z3,
                                                            Context Learning
                                                                                                                                                     x




                                                                                      Independent of reasoning engine
  "Everyone love John or Mary"




                                                                                                                                                                                      Prover9, PyProver, SMT-LIB)
  Natural Language Sentence.
                                                       recursively parse child node




                                                                                                                                                                                        Reasoning Engine's Code
                                  Parser Selector                                                                                                    Or

                                                                                                                                     Atom                 Atom
                                         Atomic Sentence Parser                                                                      Loves                Loves




                                                                                                   AST.
                                      Quantified Sentence Parser                                                               Var      Constant     Var     Constant
                                                                                                                                x         John        x       Mary
                                                                                                                          ② First pass:             ③ Second pass:
                                         Logical Sentence Parser
                                                                                                                        collect declaration        generate expression
                                 System Prompt Demonstration   Input   Result                                              Const: John, Mary
                                                                                                                                                      ForAll([x], ...)
                                       S
                                              ⊕
                                                   D
                                                             ⊕
                                                                 I
                                                                     =
                                                                         R                                                 Var: x
                                                                                                                           Function: Loves
                                                                                                                                               ⊕      Loves(Alice, John)




Figure 1: Overview of NL2L OGIC. The semantic parser ( 1 ) takes a natural language sentence and outputs a
first-order logic abstract syntax tree (FOLAST) through a recursive, top-down approach. The AST is then compiled
into the reasoning engine’s target language through a two-pass algorithm. The first pass ( 2 ) collects constant,
variable, and predicate signature declarations. The second pass ( 3 ) generates the concrete logical expression.


                                                                                                                           Rina is either a student who is unaware that caffeine is a
                     ⟨T erm⟩       ::=     ⟨V ariable⟩ | ⟨Constant⟩
                                                                                                                           drug, or she is not a student and is aware that caffeine is
             ⟨Atomic⟩              ::=     RelationName(⟨T erm⟩)
                                     |     RelationName(⟨T erm⟩, ⟨T erm⟩)                                                  a drug
                                     |     RelationName(⟨T erm⟩, ⟨T erm⟩, ⟨T erm⟩)
 ⟨Quantif ied⟩                     ::=     ∀⟨V ariable⟩. ⟨F ormula⟩                                                     (a) The parser decomposes a sentence containing a logical
                                     |     ∃⟨V ariable⟩. ⟨F ormula⟩                                                     operator into its operator and operand(s).
             ⟨Logical⟩             ::=     ¬⟨F ormula⟩
                                     |     ⟨F ormula⟩ ∧ ⟨F ormula⟩                                                         - Rina is a student who is unaware that caffeine is a drug
                                     |     ⟨F ormula⟩ ∨ ⟨F ormula⟩                                                        - Rina is not a student and is aware that caffeine is a drug
                                     |     ⟨F ormula⟩ → ⟨F ormula⟩
      ⟨F ormula⟩                   ::=     ⟨Atomic⟩                                                                     (b) The extracted operands are rewritten as standalone sen-
                                     |     ⟨Quantif ied⟩
                                     |     ⟨Logical⟩                                                                    tences. Since they are not necessarily atomic, each operand is
                                                                                                                        recursively fed back to the parser.

Figure 2: Formal notation of abstract syntax tree (AST)                                                                                                     Or

                                                                                                                                               And

4.2                Semantic Parser                                                                                                  Atom              Atom                 And
                                                                                                                                   Student            Aware
The semantic parser is the first and most critical
                                                                                                                                                     Not                     Not
stage of NL2L OGIC. It maps natural language                                                                                     Constant Constant
sentences into a first-order logic abstract syntax                                                                                 Rina     Rina    Atom                     Atom
tree (FOLAST; described in Section 3) that strictly                                                                                                Student                   Aware
enforces logical grammar. Without this stage, di-                                                                                                           Constant Constant
rectly prompting an LLM to generate FOL symbols                                                                                                               Rina     Rina
or solver-specific code (e.g., Z3, SMT-LIB) often                                                                       (c) The complete AST representation. The parser identifies
yields syntax errors, hallucinations, or undeclared                                                                     only the outermost structure , while the operands are recur-
variables. This is demonstrated in our evaluations                                                                      sively fed back to the parser.
(Section 5) and caused by such formats are rarely                                                                          (Student(Rina) ∧ Aware(Rina)) ∨ (¬Student(Rina) ∧
observed during pre-training. By isolating parsing                                                                                           ¬Aware(Rina))
as a dedicated component, we guarantee that natu-
                                                                                                                                   (d) The first-order logic rule representation
ral language is first converted into a syntactically
valid and semantically transparent representation.                                                                           Figure 3: LogicalSentenceParser example.
   Conventional NLP parsers (e.g., dependency or
constituency parsers) are inadequate for translating
NL into formal logic. Rule-based parsers (Woods,                                                                        tional ML-based parsers (Kitaev and Klein, 2018;
1970; Marcus, 1978) fail to capture the diversity                                                                       Kitaev et al., 2019) require large annotated corpora
and ambiguity of natural sentences, while conven-                                                                       of NL and FOL pairs. In contrast, large language
models (LLMs) can perform in-context learning               All people who regularly drink coffee are dependent on
(Brown et al., 2020), allowing them to follow               caffeine.
explicit grammar constraints and generate struc-
                                                         (a) The parser decomposes the sentence into its quantifier and
tured FOLAST outputs. Therefore, an LLM-based            scope.
parser is both necessary and practical: it combines
pretrained linguistic knowledge with these formal           x that regularly drink coffee are dependent on caffeine
grammar constraints to produce accurate and gen-         (b) The scope is rewritten such that the quantified subject is
eralizable logical representations.                      replaced by a variable. Since the scope is not necessarily
    Our parser operates recursively through special-     atomic, it is recursively fed back into the parser.
ized sub-modules, as shown in Fig. 1. The Parser
                                                                                    For All
Selector first classifies each sentence as atomic,                                    x
quantified, or logical. An atomic sentence ex-
                                                                                    Implies
presses a single relation, a quantified sentence in-
troduces a quantifier (e.g., ∀, ∃), and a logical sen-
                                                                           Atom              Atom
tence contains logical connectives (e.g., ∧, ∨, →,                         Drink           Dependent
¬). Then, the corresponding sub-parser is invoked:
                                                                            Var               Var
the Atomic Sentence Parser extracts predicates and                           x                 x
arguments; the Quantified Sentence Parser iden-
tifies quantifiers and variables, then recursively
                                                         (c) The complete AST representation. The parser identifies
parses the quantified scope; and the Logical Sen-        only the outermost structure , while the scope is recursively
tence Parser detects operators, splits the input into    fed back to the parser.
operands, and recursively processes each operand.
At each step, the parser focuses only on the out-                      ∀x (Drink(x) → Dependent(x))
ermost construct while delegating the remaining                  (d) The first-order logic rule representation.
sub-sentences to recursive parsing calls. This top-
down recursion incrementally builds the AST, mir-           Figure 4: QuantifiedSentenceParser example.
roring the hierarchical composition of FOL expres-
sions. This design limits error propagation, reduces     posing them into their outermost constructs and
the LLM’s cognitive load, and maintains semantic         deferring sub-sentences to recursive parsing.
faithfulness across sentences of varying complexity.
The complete system prompts for each parser are          4.3    AST-Guided Generator
provided in Section A.                                   The AST-guided generator converts the FOLAST
    To illustrate the recursive mechanism, Fig. 3        produced by the parser into solver-ready code (e.g.,
and Fig. 4 present two representative cases, com-        Z3 or SMT-LIB). The generator deterministically
pound and quantified sentences. Fig. 3 shows how         maps each AST node to target-language expres-
a disjunctive sentence is parsed by identifying the      sions, mimicking how source-to-source compilers
outermost operator (Or) and recursively decom-           work (e.g., Cython (Behnel et al., 2010)). Its work-
posing its operands, each containing internal con-       flow follows a two-pass algorithm: the first pass
junctions and negations. At each step, the parser        traverses the AST to collect all variable, constant,
enforces local correctness by validating the syntac-     and relation signature declarations, establishing a
tic and semantic consistency of each node before         consistent global context; the second pass revisits
integrating it into the higher-level tree. For ex-       each node to emit logical expressions that respect
ample, it ensures that every predicate has a valid       operator precedence, quantifier scope, and relation
argument (e.g., Student(Rina)) and that logical          arity. The generator produces executable code in
connectives such as And or Not combine clauses           the reasoning engine’s target language, preserving
rather than partial phrases. Fig. 4 then illustrates a   syntactic consistency and faithfully reflecting the
quantified structure, where the parser isolates the      logical structure defined by the FOLAST. We de-
quantifier (ForAll), abstracts the variable (x), and     scribe each pass below.
recursively parses its scoped clause into atomic            The first pass, Declaration Collection, constructs
predicates such as Drink(x) and Dependent(x).            the symbol table for the target language (Algo-
These two examples show how our parser consis-           rithm 1). Each node is visited in preorder: decla-
tently handles different logical forms by decom-         ration nodes (constants, variables, and relations)
Algorithm 1 First pass to collect declaration in an     Algorithm 2 Second pass to generate expression
AST                                                     in an AST
Require: N                  ▷ set of nodes in an AST       function G ENERATE E XPRESSION(r)
Ensure: D                        ▷ set of declaration         if r = atomic sentence then
  D←∅                                                              a←∅
  for n ∈ N do                                                     for x ∈ r.args do
      if n is a variable then                                          a          ←          a    ∪
          D ← D ∪ {D ECLARE VAR(n)}                                    G ENERATE E XPRESSION(x)
      else if n is a constant then                                 name ← r.name
          D ← D ∪ {D ECLARE C ONST(n)}                             return ATOMIC S ENTENCE(name, a)
      else if n is a relation then                            else if r = binary sentence then
          D ← D ∪ {D ECLARE R ELATION(n)}                          a ← r.lef t_operand
      else continue                                                a ← G ENERATE E XPRESSION(a)
                                                                   b ← r.right_operand
                                                                   b ← G ENERATE E XPRESSION(b)
record their signatures in a shared context, while                 op ← r.operator
expression nodes (e.g., And, Or, Not, Implies) are                 return B INARY S ENTENCE(a, op, b)
traversed only to process their children without              else if r = negation sentence then
generating expressions. Together, these recorded                   s ← r.sentence
entries form a declaration environment, a mapping                  n ← G ENERATE E XPRESSION(s)
that registers all identifiers to their declared type              return N EGATED S ENTENCE(n)
or signature. This environment ensures that every             else if r = quantified sentence then
symbol referenced in the subsequent expression                     q ← r.quantif ier
generation stage (e.g., variable names or predicate                s ← G ENERATE E XPRESSION(r.scope)
signatures) has been properly introduced.                          return Q UANTIFIED S ENTENCE(q, s)
   The second pass, Expression Generation, emits              else if r = variable or constant then
logical statements in the reasoning engine’s target                return r.name
language (Algorithm 2). Each AST node is revis-
ited to produce concrete code: constants and vari-
ables map to their declared identifiers, relational     implementation and follow the original evaluation
nodes expand into function calls with correct arity,    protocol.
and logical operators format operands according            The second baseline is Logic-LM (Pan et al.,
to the solver’s grammar. Quantified nodes intro-        2023), a representative neuro-symbolic framework
duce scoped variables and generate expressions          that translates natural language into first-order logic
with explicit bindings, ensuring variable names re-     using few-shot prompting, without explicit syn-
main unique and properly scoped. All generated          tactic or semantic constraints on the generated
expressions are then added to the solver’s assertion    formulas. To evaluate whether NL2L OGIC can
set (e.g., s.add(...) in Z3). This pass converts        strengthen existing neuro-symbolic systems, we
the FOLAST into final executable reasoning rules,       replace Logic-LM’s original NL-to-FOL transla-
grounding natural language in formal logic.             tion component with NL2L OGIC while keeping all
                                                        other components unchanged. For this comparison,
5     Evaluation                                        we report both executable rate (i.e., whether the
                                                        generated FOL formulas are syntactically valid and
5.1    Evaluation Setup                                 solver-executable) and downstream NLI accuracy.
Baseline. We compare NL2L OGIC against two                 For fairness, we evaluate using the same models
representative baselines. The first baseline is         (Gemma, Llama, Mistral, and Qwen) with sizes
Grammar-Constrained Decoding (GCD) (Raspanti            ranging from 0.5 to 27B parameters, as shown in
et al., 2025), a state-of-the-art approach that en-     Tables 1 and 3 to 5. For Logic-LM integration, we
forces syntactic correctness by encoding the target     maintain the original pipeline but substitute only
formal language as a context-free grammar and           the FOL translation component.
constraining the LLM’s decoding process accord-         Datasets. We use three natural language infer-
ingly. We run GCD using the authors’ released           ence (NLI) datasets, LogicNLI (Tian et al., 2021),
ProofWriter (Tafjord et al., 2021), and FOLIO (Han                               Pn
et al., 2024). These datasets are widely used for                                   i=1 1(yˆi = yi )
                                                                   Accuracy =                             (3)
NLI (Pan et al., 2023; Morishita et al., 2024) and                                       n
first-order logic (FOL) translation tasks (Liu, 2025;   • RQ3: Integration with neuro-symbolic sys-
Yang et al., 2024). In total, we use 3,000 premise-       tems. We evaluate whether NL2L OGIC ’s
hypothesis pairs. Each premise consists of a set of       AST-guided translation improves existing neuro-
sentences, with each sentence corresponding to one        symbolic frameworks that rely on unconstrained
logical rule. The hypothesis is a single sentence         zero-shot or few-shot prompting. Specifically,
expressible as one logical statement. The sentence        we integrate NL2L OGIC into the Logic-LM (Pan
structures are relatively simple, with minimal co-        et al., 2023) pipeline by replacing its original
reference and inter-sentence dependencies. Each           FOL translation module. Performance is as-
pair is labeled as entailment, contradiction, or          sessed using the same two key metrics, which
uncertain. To obtain the entailment prediction ŷ,        are syntactic and semantic accuracy.
NL2L OGIC parses the premises p and hypotheses
h to generate executable code for the automated         5.2   RQ1: Syntax Correctness
reasoning engine S OLVER, as defined in Eq. (1).
                                                        Result.
                                                           Table 1 shows that NL2L OGIC consistently
                  
                           p |= h ∧ p ̸|= ¬h,           outperforms the grammar-constrained decoding
                  Ent.,
                  
                                                        (GCD) baseline (Raspanti et al., 2025) across all
 S OLVER(p, h) =    Cont., p ̸|= h ∧ p |= ¬h,
                                                       model families and scales, achieving near-perfect
                    Unc., otherwise
                  
                                                        syntactic correctness (up to 0.99). The improve-
             ŷ = S OLVER(p, h)                         ment is most pronounced in smaller models (e.g.,
                                           (1)          Gemma-2-2B, Llama-3.2-1B), where syntax con-
RQs and Metrics. Our evaluations aim to answer          trol is typically fragile. This demonstrates that
two research questions.                                 NL2L OGIC ’s iterative parser effectively mitigates
                                                        syntax drift by incrementally constructing the ab-
• RQ1: Syntax correctness. We assess whether            stract syntax tree (AST), thus reducing the model’s
  NL2L OGIC generates rules that adhere to first-       cognitive burden. For larger models (e.g., Mistral-
  order logic syntax, as specified in Fig. 2. Syntax    22B, Qwen-2.5-14B), NL2L OGIC saturates near
  correctness is quantified using the correctness       0.99 accuracy, showing that once local node valid-
  rate defined in Eq. (2), where Ncorrect is the num-   ity is guaranteed, global syntactic integrity emerges
  ber of sentences with correct syntax and Ntotal is    naturally.
  the total number of sentences.
                                                                             FOLIO              LogicNLI
                                                                                 NL2                  NL2
                                                          Model           GCD                GCD
                                      Ncorrect                                  L OGIC               L OGIC
        Syntax Correctness Rate =                (2)      gemma-2-2b      0.56   0.92        0.25     0.94
                                      Ntotal              gemma-2-9b      0.77   0.98        0.91     0.99
                                                          gemma-2-27b     0.81   0.99        0.93     0.99
• RQ2: Semantic correctness. Following stan-              llama-3.2-1b    0.27   0.99        0.08     0.97
                                                          llama-3.2-3b    0.29   0.93        0.28     0.98
  dard practice in prior NL-to-FOL work (Ras-             llama-3.1-8b    0.13   0.96        0.68     0.98
  panti et al., 2025; Liu, 2025), we assess se-           ministral-8b    0.09   0.99        0.07     0.98
  mantic correctness through downstream natural           mistral-22b     0.29   0.99        0.46     0.98
                                                          qwen-2.5-0.5b   0.14   0.66        0.05     0.80
  language inference (NLI) accuracy. This indi-           qwen-2.5-1.5b   0.36   0.87        0.09     0.99
  rect evaluation is necessary because FOL expres-        qwen-2.5-3b     0.12   0.81        0.01     0.99
  sions admit many truth-equivalent variants (e.g.,       qwen-2.5-7b     0.01   0.94        0.01     0.99
                                                          qwen-2.5-14b    0.53   0.92        0.56     0.99
  ¬(P ∧ Q) ≡ ¬P ∨ ¬Q), making direct com-
  parison against a single canonical form imprac-       Table 1: Syntax correctness rate. NL2L OGIC consis-
  tical. Each NLI problem consists of premises          tently outperforms GCD and achieves near-perfect syn-
  and a hypothesis, and correctness is measured as      tax correctness.
  NL2L OGIC ’s accuracy (Eq. (3)), defined as the
  proportion of predictions (yˆi ) matching the gold    Error Analysis. However, errors may still occur
  labels (y).                                           when the LLM produces invalid nodes, rendering
   {"quantifier": {                                              decoding (GCD) baseline. This gain stems from
       "quantifier" : { ...                                      NL2L OGIC ’s parser, which incrementally con-
(a) In rare cases, the LLM produces incomplete JSON that         structs the abstract syntax tree (AST) instead of
exceeds the maximum token limit.                                 generating the entire logical rule in one step. The
                                                                 iterative design lowers the LLM’s cognitive load
   {"transitive_verb": "kind",
     "subject": "sophia",                                        when identifying entities, predicates, and logical
     "object": "" }                                              connectives, which is particularly advantageous for
                                                                 smaller models. NL2L OGIC achieves relatively
(b) The parser applies an incorrect JSON schema for the
sentence “Sophia is kind”, causing the LLM to leave the object   higher accuracy on LogicNLI than on FOLIO be-
empty. As a result, the generated node is invalid.               cause LogicNLI contains simpler sentence struc-
                                                                 tures with clearer connectives and clauses, mak-
Figure 5: Common errors that result in first-order logic
syntax violations.
                                                                 ing the top-down parsing approach more natural.
                                                                 In contrast, on FOLIO, some larger models with
                                                                 GCD surpass NL2L OGIC, suggesting that exces-
the accumulated AST incorrect. Two types of er-                  sive structural decomposition may not always be
rors are commonly observed in our experiments.                   beneficial, especially for sentences that are not nat-
The first type violates the given JSON output for-               urally parse-able in a top-down manner.
mat entirely, resulting in missing nodes, as illus-
trated in Fig. 5a. Although rare, the LLM may
hallucinate and produce incomplete or unparseable                                     FOLIO             LogicNLI
JSON. The second type conforms to the JSON                         Model           GCD
                                                                                          NL2
                                                                                                     GCD
                                                                                                              NL2
                                                                                         L OGIC              L OGIC
schema but leaves required fields empty, resulting
                                                                   gemma-2-2b      0.27   0.35       0.22     0.41
in invalid nodes, such as missing variable names                   gemma-2-9b      0.53   0.38       0.23     0.37
in Term nodes or relation names in Atom nodes, as                  gemma-2-27b     0.61   0.40       0.24     0.37
                                                                   llama-3.2-1b    0.17   0.38       0.11     0.33
shown in Fig. 5b. Together, these cases account                    llama-3.2-3b    0.18   0.36       0.15     0.37
for less than 5% of all sentences. Error statistics                llama-3.1-8b    0.12   0.37       0.17     0.37
are summarized in Table 2. We minimized these                      ministral-8b    0.16   0.37       0.04     0.38
                                                                   mistral-22b     0.23   0.38       0.14     0.34
errors by employing strong output-control tech-                    qwen-2.5-0.5b   0.17   0.26       0.12     0.36
niques, including the structured output feature in                 qwen-2.5-1.5b   0.19   0.34       0.03     0.41
vLLM (Kwon et al., 2023) and few-shot prompt-                      qwen-2.5-3b     0.08   0.32       0.01     0.35
                                                                   qwen-2.5-7b     0.01   0.37       0.01     0.34
ing (Section A) to guide the LLM in producing                      qwen-2.5-14b    0.34   0.37       0.27     0.35
structured JSON representations of AST nodes.
                                                                 Table 3: Semantic correctness measured by accuracy on
                       Missing     Invalid      Total            natural language inference (NLI) tasks.
      Model
                       Nodes        Nodes     Sentences
      gemma-2-2b         15          472
      gemma-2-9b          1          63
      gemma-2-27b         1          24
      llama-3.2-1b      127           5
      llama-3.2-3b      133          148                         Observation and Error Analysis. There are two
      llama-3.1-8b      107          97
      ministral-8b      100           9          7100
                                                                 common semantic errors. First, words with implicit
      mistral-22b       100          13                          negation (e.g., unable, unaware, inconsistent) often
      qwen-2.5-0.5b      13         1786                         confuse the parser. Despite careful prompt design,
      qwen-2.5-1.5b      31          392
      qwen-2.5-3b        18          530                         the parser sometimes misinterprets them and enters
      qwen-2.5-7b         0          173                         an infinite recursive parse. For instance, the sen-
      qwen-2.5-14b        5          224                         tence ’John is unable to walk’ is parsed back
Table 2: Error analysis on syntax correctness, account-          and forth to the sentence ’John is not unable
ing for less than 5% of all sentences.                           to walk’, as illustrated in Fig. 6a. Second, sen-
                                                                 tences with subtle operator ordering often lead to
                                                                 operator order errors. For example, the sentence
5.3    RQ2: Semantic Correctness
                                                                 Alice is not a student and does not like coffee is
Result. Table 3 shows that NL2L OGIC improves                    occasionally parsed with the Not operator preced-
performance on natural language inference tasks by               ing And, producing a semantically incorrect AST,
an average of 31% over the grammar-constrained                   as shown in Fig. 6b.
  Parsing ’John is unable to walk’                             on smaller models: on ProofWriter, gemma-2-2b
  Unary operator parser. Operator: ’Not’                       improves from 0.01 to 0.58, llama-3.2-3b from 0.03
  |— Parsing ’John is not unable to walk’
     Unary operator parser. Operator: ’Not’                    to 0.68, qwen-2.5-7b from 0.08 to 0.90, demonstrat-
         ...                                                   ing that NL2L OGIC’s structured decomposition re-
(a) Infinite recursion caused by parsing words with implicit
                                                               duces cognitive load by parsing natural language
negation.                                                      into FOL one clause at a time.
                           Not                                                      ProofWriter       FOLIO
                                                                                   Logic  NL2      Logic  NL2
                           And                                     Model
                                                                                    LM    Logic     LM    Logic
                                                                   gemma-2-2b      0.01    0.99    0.07   0.99
                Atom              Atom                             gemma-2-9b      0.90    0.99    0.65   0.99
               Student            Like                             gemma-2-27b     0.94    0.99    0.60   0.99
                                                                   llama-3.2-1b    0.72    0.99    0.83   0.99
              Constant Constant Constant                           llama-3.2-3b    0.25    0.99    0.38   0.99
               Alice    Alice    Coffee                            llama-3.1-8b    0.90    0.99    0.58   0.99
                                                                   ministral-8b    0.20    0.99    0.14   0.99
(b) Incorrect operator ordering when parsing sentences with        mistral-22b     0.85    0.99    0.65   0.99
complex compound sentences. The sentence is "Alice is              qwen-2.5-0.5b   0.01    0.99    0.01   0.99
not a student and does not like coffee", where And                 qwen-2.5-1.5b   0.01    0.99    0.05   0.99
operator should precede the Not operator.                          qwen-2.5-3b     0.45    0.99    0.52   0.99
                                                                   qwen-2.5-7b     0.15    0.99    0.55   0.99
          Figure 6: Common semantic errors.                        qwen-2.5-14b    0.38    0.99    0.72   0.99

5.4   RQ3: Integration with Neuro-Symbolic                     Table 4: Executable rate: Logic-LM original vs. with
                                                               NL2L OGIC integration.
      Systems
To demonstrate NL2L OGIC’s practical value as a
modular component, we integrated it into Logic-                                     ProofWriter       FOLIO
                                                                                   Logic  NL2      Logic  NL2
LM (Pan et al., 2023), a representative neuro-                     Model
                                                                                    LM    Logic     LM    Logic
symbolic framework combining LLMs with sym-                        gemma-2-2b      0.01    0.58    0.21   0.36
bolic solvers. Logic-LM originally uses few-shot                   gemma-2-9b      0.45    0.85    0.26   0.39
                                                                   gemma-2-27b     0.60    0.90    0.31   0.41
prompting for FOL translation without explicit syn-                llama-3.2-1b    0.25    0.47    0.18   0.38
tactic or semantic constraints. We replaced this                   llama-3.2-3b    0.03    0.68    0.14   0.36
module with NL2L OGIC while keeping all other                      llama-3.1-8b    0.40    0.91    0.22   0.38
                                                                   ministral-8b    0.18    0.75    0.04   0.39
pipeline components unchanged (Z3 solver, refine-                  mistral-22b     0.51    0.78    0.26   0.41
ment mechanisms, answer selection), isolating the                  qwen-2.5-0.5b   0.01    0.38    0.01   0.26
impact of our AST-guided translation on syntactic                  qwen-2.5-1.5b   0.01    0.48    0.02   0.34
                                                                   qwen-2.5-3b     0.17    0.37    0.14   0.32
validity and downstream reasoning accuracy.                        qwen-2.5-7b     0.08    0.90    0.22   0.37
   Table 4 presents executable rate comparison on                  qwen-2.5-14b    0.32    0.86    0.31   0.38
ProofWriter (Tafjord et al., 2021) and FOLIO (Han
                                                               Table 5: Accuracy on executable rules: Logic-LM origi-
et al., 2024). Logic-LM’s original few-shot trans-
                                                               nal vs. with NL2L OGIC integration.
lation produces highly variable executable rates
(0.01-0.94), with particularly poor performance on
smaller models (e.g., 0.01 for gemma-2-2b, qwen-
                                                               6   Conclusion
2.5-0.5b on ProofWriter). NL2L OGIC achieves
near-perfect executable rate (0.99) across all 13              This paper presents NL2L OGIC, an AST-guided
models and both datasets through iterative AST                 framework for translating natural language into
construction validating each logical construct in-             first-order logic using large language models
crementally.                                                   (LLMs). Unlike prior work that treats this task
   This syntactic validity improvement translates              as free-form text generation with limited con-
into better semantic correctness. Table 5 shows ac-            trol, NL2L OGIC incrementally constructs the AST
curacy on executable rules only, where predictions             in a top-down manner. This approach provides
originate from logic solver execution rather than              stronger control over the LLM output, achieving
backup strategies (random guessing or CoT fall-                near-perfect syntactic correctness, improving se-
back). NL2L OGIC improves Logic-LM’s accuracy                  mantic accuracy by 30% on LogicNLI, FOLIO,
by ∼31% on average. Gains are most pronounced                  and ProofWriter datasets, and improving existing
neuro-symbolic system Logic-LM by 31% on both           full context, however, the predicate father could
syntactic and downstream reasoning task accuracy.       instead be expressed as a conjunction of parent
                                                        and male.
Ethical Considerations                                  Reliance      on     Structured      Generations.
                                                        NL2L OGIC relies on structured output capa-
Datasets and Models. We rely solely on pub-
                                                        bilities available in both commercial APIs
licly available datasets and models, without in-
                                                        (e.g., OpenAI) and open-source LLM serving
volving human subjects or newly collected data.
                                                        frameworks (e.g., vLLM). It prompts the LLM to
No personal, private, or sensitive information is
                                                        generate JSON outputs following schemas specific
used. Therefore, this work poses no risks related
                                                        to each parser type. However, not all LLM serving
to privacy, consent, or data annotation ethics. All
                                                        frameworks support this feature natively. For
datasets and models are utilized in accordance with
                                                        instance, llama.cpp requires integration with the
their respective licenses.
                                                        lm-format-enforcer tool to enable structured
Potential Misleading Proof. We envision that            output.
rules generated by NL2L OGIC will be executed
using automated reasoning engines such as Z3,           Acknowledgments
PyProver, or SMT-LIB to verify a hypothesis
                                                        We would like to thank the anonymous reviewers
against a set of premises. Although the goal is to
                                                        for their constructive comments and suggestions.
obtain a formally provable answer, the proof must
                                                        This work is supported in part by the National Sci-
be interpreted carefully. Given a set of premises P
                                                        ence Foundation under grant CNS-2442171. Any
and a hypothesis Q, P |= Q does not necessarily
                                                        opinions, findings, and conclusions made in this pa-
imply that Q is proven. If P |= ¬Q also holds,
                                                        per are those of the authors and do not necessarily
the result is uncertain instead of entailment. If the
                                                        reflect the views of the funding agencies.
premises themselves are unsatisfiable (e.g., due to
semantic errors during translation), P may entail
any statement. Hence, one must examine all pos-         References
sible outcomes, which are P |= Q, P |= ¬Q, and
                                                        Lasha Abzianidze. 2017. Langpro: Natural language
even the satisfiability of P itself.
                                                          theorem prover. arXiv preprint arXiv:1708.09417.
Use of AI Assistants. We acknowledge the use of
AI assistants for grammar checking. The authors         V Aho Alfred, S Lam Monica, and D Ullman Jeffrey.
                                                          2007. Compilers principles, techniques & tools.
remain fully responsible for the scientific contribu-     pearson Education.
tions, experimental results, and all claims presented
in this paper.                                          Dave Barker-Plummer, Richard Cox, and Robert Dale.
                                                          2009. Dimensions of difficulty in translating natural
                                                          language into first order logic. International Working
Limitations                                               Group on Educational Data Mining.

Dependencies        on     Multiple      Sentences.     Clark Barrett, Aaron Stump, Cesare Tinelli, and 1 oth-
NL2L OGIC converts text into first-order logic,           ers. 2010. The smt-lib standard: Version 2.0. In
                                                          Proceedings of the 8th international workshop on
one sentence at a time. It ensures consistent
                                                          satisfiability modulo theories (Edinburgh, UK), vol-
predicate arity, constant’ names, and variable’           ume 13, page 14.
names across sentences by prompting the LLM to
use the base form of each word, such as the present     Stefan Behnel, Robert Bradshaw, Craig Citro, Lisandro
                                                           Dalcin, Dag Sverre Seljebotn, and Kurt Smith. 2010.
tense for verbs and objects without modifiers.             Cython: The best of both worlds. Computing in
However, certain sentences require contextual              Science & Engineering, 13(2):31–39.
information from adjacent sentences or the entire
text to generate accurate logical representations.      Johan Bos and Katja Markert. 2005. Recognising tex-
                                                          tual entailment with logical inference. In Proceed-
In such cases, NL2L OGIC does not yet handle              ings of Human Language Technology Conference
co-reference or implicit relational links across          and Conference on Empirical Methods in Natural
sentences. For instance, given the premise “John is       Language Processing, pages 628–635.
the father of Alice” and the hypothesis “John is the    Samuel R. Bowman, Christopher Potts, and Christo-
parent of Alice,” separate translation would yield        pher D. Manning. 2015. Recursive neural networks
two distinct relations: father and parent. With           can learn logical semantics. In Proceedings of the
  3rd Workshop on Continuous Vector Space Models            Computational Linguistics (Volume 1: Long Papers),
  and their Compositionality, pages 12–21, Beijing,         pages 2676–2686.
  China. Association for Computational Linguistics.
                                                          Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yu-
Tom Brown, Benjamin Mann, Nick Ryder, Melanie               taka Matsuo, and Yusuke Iwasawa. 2022. Large lan-
  Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind        guage models are zero-shot reasoners. Advances in
  Neelakantan, Pranav Shyam, Girish Sastry, Amanda          neural information processing systems, 35:22199–
  Askell, Sandhini Agarwal, Ariel Herbert-Voss,             22213.
  Gretchen Krueger, Tom Henighan, Rewon Child,
  Aditya Ramesh, Daniel Ziegler, Jeffrey Wu, Clemens      Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying
  Winter, and 12 others. 2020. Language models are         Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E.
  few-shot learners. In Advances in Neural Information     Gonzalez, Hao Zhang, and Ion Stoica. 2023. Effi-
  Processing Systems, volume 33, pages 1877–1901.          cient memory management for large language model
  Curran Associates, Inc.                                  serving with pagedattention. In Proceedings of the
                                                           ACM SIGOPS 29th Symposium on Operating Systems
Ruisheng Cao, Su Zhu, Chen Liu, Jieyu Li, and Kai Yu.      Principles.
  2019. Semantic parsing with dual learning. arXiv
  preprint arXiv:1907.05343.                              Junnan Liu. 2025. Few-shot natural language to first-
                                                            order logic translation via code generation. In Pro-
Antonia Creswell, Murray Shanahan, and Irina Higgins.       ceedings of the 2025 Conference of the Nations of
  2022. Selection-inference: Exploiting large language      the Americas Chapter of the Association for Compu-
  models for interpretable logical reasoning. Preprint,     tational Linguistics: Human Language Technologies
  arXiv:2205.09712.                                         (Volume 1: Long Papers), pages 10939–10960, Al-
                                                            buquerque, New Mexico. Association for Computa-
Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: an         tional Linguistics.
  efficient smt solver. In Proceedings of the Theory
  and Practice of Software, 14th International Con-       Xuantao Lu, Jingping Liu, Zhouhong Gu, Hanwen Tong,
  ference on Tools and Algorithms for the Construc-         Chenhao Xie, Junyang Huang, Yanghua Xiao, and
  tion and Analysis of Systems, TACAS’08/ETAPS’08,          Wenguang Wang. 2022. Parsing natural language
  page 337–340, Berlin, Heidelberg. Springer-Verlag.        into propositional and first-order logic with dual re-
                                                            inforcement learning. In Proceedings of the 29th
Herbert B Enderton. 2001. A mathematical introduction       International Conference on Computational Linguis-
  to logic. Elsevier.                                       tics, pages 5419–5431.
Richard Evans, David Saxton, David Amos, Pushmeet         Mitchell Philip Marcus. 1978. A theory of syntactic
  Kohli, and Edward Grefenstette. 2018. Can neural          recognition for natural language. Ph.D. thesis, Mas-
  networks understand logical entailment? In Interna-       sachusetts Institute of Technology.
  tional Conference on Learning Representations.
                                                          W. McCune. 2005–2010. Prover9 and mace4. http:
Markus Frohmann, Igor Sterner, Ivan Vulić, Benjamin        //www.cs.unm.edu/~mccune/prover9/.
 Minixhofer, and Markus Schedl. 2024. Segment any
 text: A universal approach for robust, efficient and     Benjamin Minixhofer, Jonas Pfeiffer, and Ivan Vulić.
 adaptable sentence segmentation. In Proceedings            2023. Where’s the point? self-supervised multilin-
 of the 2024 Conference on Empirical Methods in             gual punctuation-agnostic sentence segmentation. In
 Natural Language Processing, pages 11908–11941,            Proceedings of the 61st Annual Meeting of the As-
 Miami, Florida, USA. Association for Computational         sociation for Computational Linguistics (Volume 1:
 Linguistics.                                               Long Papers), pages 7215–7235, Toronto, Canada.
                                                            Association for Computational Linguistics.
Simeng Han, Hailey Schoelkopf, Yilun Zhao, Zhent-
  ing Qi, Martin Riddell, Wenfei Zhou, James Coady,       Terufumi Morishita, Gaku Morio, Atsuki Yamaguchi,
  David Peng, Yujie Qiao, Luke Benson, and 1 oth-           and Yasuhiro Sogawa. 2024. Enhancing reasoning
  ers. 2024. Folio: Natural language reasoning with         capabilities of llms via principled synthetic logic cor-
  first-order logic. In Proceedings of the 2024 Con-        pus. Advances in Neural Information Processing
  ference on Empirical Methods in Natural Language          Systems, 37:73572–73604.
  Processing, pages 22017–22031.
                                                          Theo Olausson, Alex Gu, Ben Lipkin, Cedegao Zhang,
Nikita Kitaev, Steven Cao, and Dan Klein. 2019. Multi-      Armando Solar-Lezama, Joshua Tenenbaum, and
  lingual constituency parsing with self-attention and      Roger Levy. 2023. LINC: A neurosymbolic approach
  pre-training. In Proceedings of the 57th Annual Meet-     for logical reasoning by combining language models
  ing of the Association for Computational Linguistics,     with first-order logic provers. In Proceedings of the
  pages 3499–3505, Florence, Italy. Association for         2023 Conference on Empirical Methods in Natural
  Computational Linguistics.                                Language Processing, pages 5153–5176, Singapore.
                                                            Association for Computational Linguistics.
Nikita Kitaev and Dan Klein. 2018. Constituency pars-
  ing with a self-attentive encoder. In Proceedings       Liangming Pan, Alon Albalak, Xinyi Wang, and
  of the 56th Annual Meeting of the Association for         William Wang. 2023. Logic-LM: Empowering large
  language models with symbolic solvers for faithful           and 1 others. 2022. Chain-of-thought prompting elic-
  logical reasoning. In Findings of the Association            its reasoning in large language models. Advances
  for Computational Linguistics: EMNLP 2023, pages             in neural information processing systems, 35:24824–
  3806–3824, Singapore. Association for Computa-               24837.
  tional Linguistics.
                                                             William A Woods. 1970. Transition network grammars
Xin Quan, Marco Valentino, Louise A. Dennis, and An-           for natural language analysis. Communications of
  dre Freitas. 2024. Verification and refinement of nat-       the ACM, 13(10):591–606.
  ural language explanations through LLM-symbolic
  theorem proving. In Proceedings of the 2024 Con-           Jundong Xu, Hao Fei, Liangming Pan, Qian Liu, Mong-
  ference on Empirical Methods in Natural Language             Li Lee, and Wynne Hsu. 2024. Faithful logical rea-
  Processing, pages 2933–2958, Miami, Florida, USA.            soning via symbolic chain-of-thought. In Proceed-
  Association for Computational Linguistics.                   ings of the 62nd Annual Meeting of the Association
                                                               for Computational Linguistics (Volume 1: Long Pa-
Xin Quan, Marco Valentino, Louise A. Dennis, and An-           pers), pages 13326–13365, Bangkok, Thailand. As-
  dre Freitas. 2025. Faithful and robust LLM-driven            sociation for Computational Linguistics.
  theorem proving for NLI explanations. In Proceed-
  ings of the 63rd Annual Meeting of the Association         Yuan Yang, Siheng Xiong, Ali Payani, Ehsan Shareghi,
  for Computational Linguistics (Volume 1: Long Pa-            and Faramarz Fekri. 2024. Harnessing the power of
  pers), pages 17734–17755, Vienna, Austria. Associa-          large language models for natural language to first-
  tion for Computational Linguistics.                          order logic translation. In Proceedings of the 62nd
                                                               Annual Meeting of the Association for Computational
Federico Raspanti, Tanir Ozcelebi, and Mike Holen-             Linguistics (Volume 1: Long Papers), pages 6942–
  derski. 2025. Grammar-constrained decoding makes             6959, Bangkok, Thailand. Association for Computa-
  large language models better logical parsers. In Pro-        tional Linguistics.
  ceedings of the 63rd Annual Meeting of the Associa-
  tion for Computational Linguistics (Volume 6: Indus-       Luke S Zettlemoyer and Michael Collins. 2012. Learn-
  try Track), pages 485–499.                                   ing to map sentences to logical form: Structured
                                                               classification with probabilistic categorial grammars.
Tim Rocktaschel, Edward Grefenstette, Karl Moritz              arXiv preprint arXiv:1207.1420.
  Hermann, Tomas Kocisky, and Phil Blunsom. 2016.
  Reasoning about entailment with neural attention. In
  International Conference on Learning Representa-
  tions (ICLR).

Soumya Sanyal, Harman Singh, and Xiang Ren. 2022.
  FaiRR: Faithful and robust deductive reasoning over
  natural language. In Proceedings of the 60th Annual
  Meeting of the Association for Computational Lin-
  guistics (Volume 1: Long Papers), pages 1075–1093,
  Dublin, Ireland. Association for Computational Lin-
  guistics.

Oyvind Tafjord, Bhavana Dalvi, and Peter Clark. 2021.
  ProofWriter: Generating implications, proofs, and
  abductive statements over natural language. In Find-
  ings of the Association for Computational Linguis-
  tics: ACL-IJCNLP 2021, pages 3621–3634, Online.
  Association for Computational Linguistics.

Jidong Tian, Yitian Li, Wenqing Chen, Liqiang Xiao,
   Hao He, and Yaohui Jin. 2021. Diagnosing the
   first-order logical reasoning ability through logicnli.
   In Proceedings of the 2021 Conference on Empiri-
   cal Methods in Natural Language Processing, pages
   3738–3747.

Bailin Wang, Zi Wang, Xuezhi Wang, Yuan Cao, Rif
  A Saurous, and Yoon Kim. 2023. Grammar prompt-
  ing for domain-specific language generation with
  large language models. Advances in Neural Informa-
  tion Processing Systems, 36:65030–65055.

Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
   Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou,
A    System Prompts
The parser, described in Section 4 and illus-
trated in Fig. 1, iteratively constructs the abstract
syntax tree (AST) by recursively analyzing each              QuantifiedSentenceParser System Prompt
sentence component through specialized submod-
ules: ParserSelector, AtomicSentenceParser,                  You identified the sentence as a quantified
QuantifiedSentenceParser, and LogicalSen                     logical statement.
tenceParser. The ParserSelector determines
the appropriate parser for a sentence, while the             Task:
remaining three parsers perform parsing and recur-           1. Select the correct quantifier:
                                                             - ForAll (e.g., all, every, each, no one) ->
sively invoke the ParserSelector for any child
nodes. The system prompt for ParserSelector                   the logical statement applies to ALL entities
                                                             - ThereExists (e.g., some, there is, at least
is shown in Fig. 7. While the system prompt                   one, a) -> the logical statement applies to
for the QuantifiedSentenceParser is shown
in Fig. 8. The LogicalSentenceParser involves                SOME entities
                                                             2. Identify the variable (and all reference)
multiple system prompts, as shown in Figs. 9                 being quantified (the noun phrase that follows
and 10. AtomicSentenceParser also involves
multiple system prompts, as shown in Figs. 11                the quantifier, e.g., "student", "person",
                                                             "dog") and replace it with a letter like x, y,
to 15.                                                       or z.

 ParserSelector System Prompt                                3. Rewrite the sentence WITHOUT the quantifier,
                                                             keeping the variable in place so the sentence
 You are an expert on classifying the sentence               is still natural and understandable. Preserve
 by its overall structure:
 A = An atomic logical statement.           (no              the exact wording and capitalization of all
 quantifiers, no logical connectives, no                     subject and object names. If there is multiple
 negation)                                                   quantifier, just remove the outermost.
 B = A quantified logical statement when the
 sentence talks about a general rule that                    4. If the sentence is ambiguous, you should
 covers many entities.                                       rephrase it so that the next parser will
 If the sentence only mentions specific proper               understand whether it is an atomic logical
 names, or an instances of variable (x,y,z), or
 if quantifiers appear only inside part of the               sentence, or logical sentence with connectives,
 sentence, then it should be classified as A,                or a quantified logical sentence.
 C, or D instead.
 C = A compound logical sentence, where each
 part is connected with logical connectives                  Examples:
 such as ’and’, ’or’, ’if...then’, or ’only
 if’.                                                        Input: "All students study hard."
 D = A statement that contains literal negation
 of another sentence (’not’, ’no’, ’dont’,                   Output: { "quantifier" : "ForAll", "variable"
 ’doesnt’). Only look for a literal negation.                : "x", "sentence_without_quantifier" : "x
                                                             study hard."}
 Example 1:
 Sentence: ’Alice sings.’
                                                             ...
 Answer: { "answer" : "A"}
 ...
 Now, it is your turn                                        Now, it is your turn
 Input: {input sentence}                                     Input: {input sentence}
 Answer:
                                                             Output:

Figure 7: The system prompt for selecting the appro-
priate parser. The first step in parsing a sentence is to   Figure 8: The system prompt for parsing a quantified
classify whether it is an atomic, quantified, compound,     logical sentence. It instructs the LLM to extract the
or negation logical sentence.                               quantifier, variable, and the scoped logical sentence.
 LogicalSentenceParser System Prompt

 You parse a sentence into its OUTERMOST                     LogicalSentenceParser System Prompt
 (top-level) logical operator and its two
 operands. Always choose the operator that
                                                             You parse a sentence whose top-level operator
 governs the entire sentence (outermost scope).              is unary negation.
 Do not parse nested or inner operators here.
 Each operand, left and right, are a standalone
                                                             Output JSON matching:
                                                             operator: always "Not"
 and complete sentence, not just a phrase,
                                                             operand : rewrite the sentence without the
 meaning it has at least subject and verb/to
 be. Output JSON matching:
                                                             outermost negation
 operator:    one of ["Not","And","Or","If",
                                                             Guidelines:
 "OnlyIf","IfAndOnlyIf"]
 left_operand: rewrite the left part as a clean,             - Always set operator = "Not".
                                                             - For the operand, remove only the **outermost**
 standalone clause. Preserve the exact wording                negation.
 and capitalization of all subject and object
 names. But, resolve co-reference such as she,               - If there are multiple negations, strip just
                                                              the outermost one and keep the inner ones.
 he, it, etc.                                                - Rewrite the operand as a natural, grammatical
 right_operand: rewrite the right part as a
 clean, standalone clause. Preserve the exact                 sentence.
                                                             - Do not add explanations or extra words.
 wording and capitalization of all subject and               - Return JSON only.
 object names. But, resolve co-reference such
 as she, he, it, etc.
                                                             Examples:
 Decide by the main structure of the whole
 sentence:                                                   Input: "It is not raining."
                                                             Output: {"operator": "Not", "operand": "It is
 - And: two clauses joined by and.                           raining"}
 - Or: two clauses joined by or / either ... or.
 - If: conditional “if . . .         then . . . ”
                                                             Input: "No student is absent."
 (antecedent = left, consequent = right).                    Output: {"operator": "Not", "operand":            "a
 - OnlyIf: “P only if Q” (left = P, right = Q;
  Q is required for P).                                      student is absent"}

 - IfAndOnlyIf: “iff / if and only if / exactly              Input:      "It   is   not   true   that   John   is
 when / just in case”.
                                                             not guilty." Output: {"operator":            "Not",
                                                             "operand": "John is not guilty"}
 Examples:

 Input:     "Alice sings and dances." Output:                Input: "Nobody loves me." Output: {"operator":
                                                             "Not", "operand": "Somebody loves me"}
 {"operator": "And", "left_operand": "Alice
 sings", "right_operand": "Alice dances"}
                                                             Now, it is your turn
 ...                                                         Input: {input sentence}
 Now, it is your turn
                                                             Answer:
 Input: {input sentence}
 Output:
                                                            Figure 10: The system prompt for parsing a sentence
                                                            involving a negation operator. It instructs the LLM to
Figure 9: The system prompt for parsing a sentence          extract the sentence excluding the negation.
involving a binary logical operator. It instructs the LLM
to extract the operator and its two operands.
                                                             AtomicSentenceParser System Prompt

                                                             You extract the object and its adjective
                                                             property from a simple atomic sentence.
                                                             Output JSON matching:

                                                             adjective: the describing word or phrase. use
                                                             the base form with no modifier
                                                             obj: the entity being described (keep wording
 AtomicSentenceParser System Prompt
                                                             and capitalization verbatim).          use the base
                                                             form with no modifier
 You classify an ATOMIC             natural-language
 predicate into one of:
 A = Adjective/property                                       Rules:
                                                             - Handle only atomic adjective/property
  B = Intransitive verb (takes no object)                     sentences (e.g., "Alice is tall", "The dog is
  C = Transitive verb (takes exactly one object)
  D = Ditransitive verb (takes two objects)                   happy").
                                                             - Subjects must be individual names or noun
  Examples:                                                   phrases without quantifiers ("all", "every",

                                                              "some", "no").
  Input: "Alice is tall."                                    - Adjective may be single word or short phrase
  Output: {"answer":"A"}                                     (e.g., "absent", "very tall").

                                                             - Do not paraphrase or change casing; copy
  Input: "Alice is a student."                                terms exactly.
  Output: {"answer":"A"}                                     - Ignore tense/negation; just extract subject

                                                             and adjective.
  Input: "Alice runs."
  Output: {"answer":"B"}                                     Examples:

  Input: "The baby sleeps."                                  Input: "Alice is tall."
  Output: {"answer":"B"}                                     Output: {"adjective": "tall", "obj": "Alice"}

                                                             Input: "student is awesome."
  ...                                                        Output:    {"adjective":   "awesome",           "obj":
  Now, it is your turn
                                                             "student"}
  Input: {input sentence}
  Output:                                                    Input: "Bob is very tired."

                                                             Output:     {"adjective":     "very tired", "obj":
                                                             "Bob"}
Figure 11: The system prompt for parsing an atomic
logical sentence. It first instructs the LLM to determine
whether the sentence involves an adjective, intransitive     Now, it is your turn
verb, transitive verb, or ditransitive verb predicate.
                                                             Input: {input sentence}
                                                             Answer:


                                                            Figure 12: The system prompt for parsing an atomic
                                                            logical sentence involving a subject and an adjective. It
                                                            instructs the LLM to extract the subject and the adjective
                                                            predicate.
                                                             AtomicSentenceParser System Prompt
 AtomicSentenceParser System Prompt
                                                             You extract the subject, the main transitive
 You extract the         subject and the main                verb, and its single object from a simple
 intransitive verb       from a simple atomic                atomic sentence.
 sentence.
                                                             Output JSON matching:
 Output JSON matching:                                       subject: the entity performing the action
 verb: the main intransitive verb (copy exactly
                                                             (copy wording and capitalization verbatim)
 as in the input). use the verb base form                    verb: the main transitive verb. use the verb
 subject: the entity performing the action                   base form
 (keep wording and capitalization verbatim)
                                                             obj: the object of the verb (copy wording and
                                                             capitalization verbatim). use the base form
  Rules:                                                     in infinitive form
 - Handle only atomic intransitive sentences (a

  subject + intransitive verb, with no object,
  no quantifier, no negation).                               Examples:
 - Subject is a proper name or noun phrase
                                                             Input: "Alice loves Bob."
 (e.g., "Alice", "The student").                             Output: {"subject": "Alice", "verb": "love",
 - Verb must appear exactly as written in the
  sentence (respect tense/aspect: "runs", "is                "obj": "Bob"}

  running", "slept").                                        Input: "The student reads a book."
 - Do not paraphrase or alter capitalization.
 - Sentences with objects, quantifiers, or                   Output: {"subject": "The student", "verb":
                                                             "read", "obj": "a book"}
 negation are out of scope.

 Examples:                                                   Input: "Bob is watching TV."
                                                             Output: {"subject": "Bob", "verb": "watch",
                                                             "obj": "TV"}
 Input: "Alice runs."
 Output: {"verb": "run", "subject": "Alice"}
                                                             Input: "Mary wrote a letter."
                                                             Output: {"subject": "Mary", "verb": "write",
 Input: "The student sleeps."
 Output: {"verb": "sleep", "subject":             "The       "obj": "a letter"}
 student"}                                                   Input: "John loves swimming."
 Input: "Bob is running."                                    Output: {"subject": "John", "verb": "love",
                                                             "obj": "to swim"}
 Output: {"verb": "run", "subject": "Bob"}

 Input: "Alice swam."                                        Input: "Doe likes to read a book"
                                                             Output: {"subject": "Doe", "verb":         "like",
 Output: {"verb": "swim", "subject": "Alice"}                "obj": "to read a book"}
 Now, it is your turn
                                                             Now, it is your turn
 Input: {input sentence}
 Answer:                                                     Input: {input sentence}
                                                             Answer:

Figure 13: The system prompt for parsing an atomic
logical sentence involving a simple subject and intransi-   Figure 14: The system prompt for parsing an atomic
tive verb structure. It instructs the LLM to extract the    logical sentence involving a subject and a transitive
subject and the verb predicate.                             verb. It instructs the LLM to extract the subject, the
                                                            verb predicate, and the object.
 AtomicSentenceParser System Prompt

 You extract the subject, the main ditransitive
 verb, its indirect object, and its direct
 object from a simple atomic sentence.

  Output JSON matching:
  subject: the entity performing the action

 (copy wording and capitalization verbatim)
 verb: the main ditransitive verb. use the base
 verb form

 indirect_obj: the recipient/beneficiary of
 the action (copy wording and capitalization
 verbatim). use the infinitive form if needed

  direct_obj:           the     thing    being
  given/sent/shown/etc.     (copy wording and
  capitalization verbatim). use the infinitive

  form if needed

  Examples:

  Input: "John gave Mary a book."
  Output: {"subject": "John", "verb": "give",

  "indirect_obj":      "Mary",     "direct_obj":      "a
  book"}


  Input: "Alice sent Bob a letter."
  Output: {"subject": "Alice", "verb": "send",
  "indirect_obj":   "Bob", "direct_obj":    "a

  letter"}
  Input:   "The     teacher    showed the students
  a picture."       Output:      {"subject":  "The

  teacher", "verb":     "show", "indirect_obj":
  "the students", "direct_obj": "a picture"}


  Input: "John gave a book to Mary."
  Output: {"subject": "John", "verb": "give",
  "indirect_obj":   "Mary", "direct_obj": "a

  book"}

  ...

  Now, it is your turn

  Input: {input sentence}

 Answer:


Figure 15: The system prompt for parsing an atomic
logical sentence involving a subject and a ditransitive
verb. It instructs the LLM to extract the subject, the verb
predicate, the direct object, and the indirect object.
