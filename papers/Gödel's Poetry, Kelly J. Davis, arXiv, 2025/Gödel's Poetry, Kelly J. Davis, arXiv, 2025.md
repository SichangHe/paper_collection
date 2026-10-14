                                                                                    G ÖDEL’ S P OETRY


                                                                                            Kelly J. Davis
                                                                                             Unaffiliated
                                                                                        kdavis@alum.mit.edu
arXiv:2512.14252v1 [cs.AI] 16 Dec 2025




                                                                                              A BSTRACT
                                                  Formal, automated theorem proving has long been viewed as a challenge to artificial intelligence. We
                                                  introduce here a new approach to computer theorem proving, one that employs specialized language
                                                  models for Lean4 proof generation combined with recursive decomposition of difficult theorems into
                                                  simpler entailing propositions. These models are coordinated through a multi-agent architecture that
                                                  orchestrates autoformalization (if required), proof generation, decomposition of difficult theorems
                                                  into simpler entailing propositions, and recursive proof (and/or decomposition) of these proposi-
                                                  tions. Without decomposition, we achieve a 90.4% pass rate on miniF2F. With decomposition, this
                                                  is significantly improved. A key technical contribution lies in our extension of the Kimina Lean
                                                  Server with abstract syntax tree (AST) parsing capabilities to facilitate automated, recursive proof
                                                  decomposition. The system is made available on PyPI as goedels-poetry, and the open-source
                                                  implementation at https://github.com/KellyJDavis/goedels-poetry facilitates both adap-
                                                  tation to alternative language models and extension with custom functionality.




                                         1   Introduction


                                         Formal, automated theorem proving represents a fundamental challenge to artificial intelligence. The task requires au-
                                         tomated generation of formal proofs that may be verified by computer systems [11]. Recent advances in large language
                                         models [12–15] have demonstrated remarkable capabilities in mathematical reasoning [2, 4–8, 17, 18]. However, the
                                         generation of formally verified proofs remains a difficult undertaking due to the strict syntactic and logical require-
                                         ments imposed by proof assistants such as Lean [1], Isabelle [23], and Coq [24].
                                         We introduce here Gödel’s Poetry, a system combining automated theorem proving, decomposition of difficult the-
                                         orems into entailing propositions, RAG based retrieval of propositions useful for decomposition, and specialized
                                         language models. Our approach builds upon three recent advances: the verifier-guided self-correction approach of
                                         Goedel-Prover-V2 [2], the recursive proof strategy of POETRY [3], and the RAG based propositions retrieval of
                                         Hilbert [4]. The system coordinates specialized agents through LangGraph [9] and LangChain [25] for the purposes of
                                         autoformalization, autoformalization verification, proof generation, proof verification, and recursive decomposition.
                                         A key technical contribution of this work lies in our extension of the Kimina Lean Server [10] to support abstract syntax
                                         tree (AST) extraction from Lean 4 code. This extension enables programmatic analysis of decompositions, automatic
                                         identification of unproven subgoals, and extraction of subgoal proposition statements—operations that prove essential
                                         for recursive decomposition as adapted to Lean’s tactic-based proof system.
                                         The system provides three principal capabilities: (1) multi-stage proof generation proceeding through an optional
                                         autoformalization phase (autoformalization, autoformalization syntactic validation, and autoformalization semantic
                                         validation), a proof generation phase , and a proof verification phase; (2) recursive decomposition of complex theorems
                                         into entailing propositions using proof sketches with sorry placeholders; (3) proof reconstruction integrating verified
                                         proposition proofs through AST-based substitution. The modular architecture permits the substitution of alternative
                                         language models, thereby facilitating experimentation with different proof strategies.
Gödel’s Poetry


2     Related Work

2.1   Neural Theorem Proving

Neural theorem proving, which combines deep learning with formal verification, has emerged as a productive area of
research [16]. Its modern era arguably began with Polu and Sutskever’s work [41] applying transformer-based [39]
language models to automated theorem proving. Formulating tactic prediction as language modeling, this inspired
much follow-on research [29–36].
More recently, the work of DeepSeek-Prover [42] demonstrated that language models, when fine-tuned on mathe-
matical corpora, are capable of generating Lean 4 proofs with significant success rates. This motivated follow-on
work, DeepSeek-Prover-V1.5 [38] and DeepSeek-Prover-V2 [17]. Subsequent to DeepSeek-Prover, AlphaProof [43]
achieved silver-medal performance on the International Mathematical Olympiad employing reinforcement learning
with formal verification. Even more recently there has been a flood of papers from Apple [4], ByteDance [5–7],
Harmonic [8], Kimina [18], and many others.
Progress in this domain has been driven by benchmarks including miniF2F [44], MathLib-Bench [45], and Putnam-
Bench [46], which provide standardized evaluation on undergraduate mathematics, Mathlib [47] theorems, and Putnam
competition problems.

2.2   Goedel-Prover-V2

The work of Goedel-Prover-V2 [2] introduced three key innovations: (1) scaffolded data synthesis, which generates
training examples of increasing difficulty; (2) verifier-guided self-correction, which enables iterative proof refinement
using compiler feedback; and (3) model averaging, which serves to mitigate diversity loss during training. Their 8B
model achieved 84.6% pass@32 on miniF2F, thereby outperforming DeepSeek-Prover-V2-671B despite being 80×
smaller. Their 32B model reached 88.1% on miniF2F at pass@32 in standard mode and 90.4% at pass@32 with
verifier-guided self-correction. On PutnamBench, the model solved 86 problems at pass@184, at the time securing
first place among open-source models.
Our system employs Goedel-Prover-V2 models that use verifier-guided self-correction as specialized agents for direct
proof generation. This is then extended through the addition of RAG-guided, hierarchical decomposition for cases in
which a direct proof fails.

2.3   POETRY: Proving Theorems Recursively

The work of POETRY [3] introduced recursive, level-by-level proof generation for Isabelle [23]. Rather than generat-
ing proofs in a step-by-step fashion, POETRY creates verifiable sketches, i.e. decompositions, at each level, employing
sorry placeholders for intermediate propositions. The system focuses upon solving the theorem at the current level,
thereby deferring detailed proofs to subsequent levels. This approach has been found to discover substantially longer
proofs—increasing the maximum proof length from 10 to 26 steps—and achieved a 5.1% improvement on miniF2F.
We adapt this recursive strategy, implementing proof decompositions wherein difficult theorems are decomposed into
entailing propositions with explicit named hypotheses (expressed as have statements). These have statements are
then directly proven. If direct proof is too difficult, then they too are sketched and decomposed into subgoals with
explicit named hypotheses. This entire process is applied recursively.

2.4   Hilbert: Retrieving Relevant Theorems

Concurrently with our work, the Hilbert system [4] demonstrated that recursive decomposition was aided by retrieving
previously proven theorems that could aid in decomposition. When tasked with decomposing a theorem, an LLM in
the Hilbert system [4] system generates a number descriptions of theorems it thinks would be of use in decomposition.
These descriptions are then used to query a vector database to retrieve relevant theorems. These theorems are then, if
appropriate, employed in decomposition. This framework yields substantial improvements on formal theorem proving
benchmarks, achieving 99.2% on miniF2F and 70.0% on PutnamBench. While Hilbert was developed independently,
the convergence upon these recursive decomposition strategies serves to validate this architectural approach.
We adopt this RAG-bsed theorem retrieval. Gödel’s Poetry adds an agent that generates a number of descriptions of
theorems it thinks would be of use in decomposition. It then queries a vector database, we employ a LeanExplore
variant [56], to retrieve relevant theorems that are, if appropriate, then used in decomposition.


                                                           2
Gödel’s Poetry


2.5   Kimina Lean Server

The Kimina Lean Server [10] provides high-performance parallel verification of Lean 4 proofs through a FastAPI [48]
service that wraps the Lean REPL. It supports batch proof checking with configurable parallelism, REPL reuse for
improved throughput, and structured error reporting.
We extend the Kimina server with AST extraction capabilities (the details of which appear in Appendix A), thereby
enabling programmatic analysis of proof structures essential for recursive decomposition.

2.6   Multi-Agent Systems

Multi-agent architectures have been applied with success to a variety of AI tasks [51]. In the domain of theorem prov-
ing, HyperTree Proof Search [52] employs a MCTS-inspired search algorithm. The work of Draft-Sketch-Prove [53]
uses separate models for drafting informal proofs, sketching formal structure, and completing details. Hilbert [4] in-
troduces four agents: an informal LLM that excels at mathematical reasoning, a specialized prover LLM optimized
for Lean 4 tactics, a formal verifier, and a semantic theorem retriever.
Our system employs specialized agents for distinct stages of the proof process (e.g. formalization, proving, decompo-
sition), with orchestration through LangGraph [9] enabling flexible workflow management.

3     Methods

3.1   System Architecture

Our system employs a multi-agent architecture (Figure 1) that is coordinated by a supervisor agent, elided in (Figure 1).
The supervisor analyzes the current proof state and dispatches work to specialized agents, shown in (Figure 1), which in
turn handle formalization and validation of formalized theorems, proof generation, proof validation, query generation,
theorem lookup, proof sketch/decomposition, and extraction of subgoals.
The system maintains a tree-structured proof state, wherein each node represents either a leaf node (containing the
formal theorem, proof attempt, verification status, and proof history) or an internal node (containing the formal the-
orem, proof decomposition, child subgoals, and decomposition history). This structure enables both the tracking of
complete proof provenance and the systematic reconstruction of verified proofs.

3.2   Formalization Pipeline

For informal theorems expressed in natural language, the system executes a three-stage pipeline, which we now de-
scribe.
Stage 1: Formalization. The formalizer agent employs a swappable LLM, which by default is Goedel-Formalizer-
V2, to translate a natural language statement into a Lean 4 theorem (the prompt it employs is provided in full in
Appendix B.1). The model was fine-tuned upon pairs of informal mathematical statements and their formal Lean 4
counterparts.
Stage 2: Syntax Validation. The syntax agent submits the formalization to the Kimina Lean Server [10] for parsing.
The Lean compiler reports any syntax errors, type mismatches, unknown identifiers, or inconsistencies. Invalid for-
malizations are returned to Stage 1, and this process continues until validation succeeds or the maximum number of
retries is exhausted (default: 10 attempts).
Stage 3: Semantic Checking. A semantic validation agent employs a swappable LLM, which is by default Qwen 3
30GB [27], to verify that the formalization preserves the meaning of the informal statement (the prompt it employs is
provided in full in Appendix B.9). The agent receives both the original informal statement and the formalized version,
and determines whether the formalization accurately captures the meaning of the informal statement. This serves to
prevent syntactically valid but semantically incorrect translations. The semantic checker possesses veto power: if it
determines that the formalization is incorrect, the theorem is returned to Stage 1.

3.3   Direct Proof Generation

The prover agent employs a swappable LLM, which is by default the Goedel-Prover-V2 [2] model, and uses verifier-
guided self-correction to generate complete proofs (the prompts it employs are provided in full in Appendices B.2
and B.3).


                                                           3
Gödel’s Poetry




                                                                                         Target Theorem
                                                                                       fermats_last_theorem



                                                                                          Formalization
                                                                                          & Validation



                                                                                        Proof Generation
                                                                                       (Goedel-Prover-V2)



                                                                                           Verification
                                                                                       (Kimina Lean Server)




                                                                                            Verified?
                                                                             No
                                                                                                              Yes
                                                      Query Generation
                                                       (Search Agent)                                                Complete
                                                                                                                    Verified Proof


                                                      Theorem Lookup
                                                     (Vector DB Agent)



                                                        Proof Sketch
                                                      & Decomposition



                                                      Extract Subgoals
                                                       (AST Parser)



                       Recurse
                                          Subgoal 1                      Subgoal 2
                                                                                                    Extracted Subgoals
                                 taniyama_shimura_conjecture         epsilon_conjecture




                                           Prove                             Prove



                                           Verify                            Verify



                                         Decompose                       Decompose


                                              ..                                  ..
                                               .                                   .
                                           recurse                           recurse


Figure 1: The Gödel’s Poetry recursive decomposition architecture. Flow proceeds top-to-bottom: a target theorem
undergoes (if required) formalization, proof generation with Goedel-Prover-V2 using verifier-guided self-correction,
and verification with Kimina Lean Server. Upon verification failure, the system queries a vector database, obtaining
theorems of use when generating a proof sketch. Using these theorems it generates a proof sketch with sorry place-
holders, extracts subgoals via AST parsing, and recursively proves each (shown in dashed boxes with colored stages:
orange=theorem, blue=prove, teal=verify, red=decompose). The red dashed arrow shows recursion back to the prover
for subgoal solving.




                                                                         4
Gödel’s Poetry


The agent receives the formal theorem statement along with appropriate import declarations and Mathlib [47] de-
pendencies. The model then generates a proof intended to close all goals. The system validates the proof through the
Kimina server.
When verification fails, a corrector agent analyzes the error messages and generates a correction prompt that includes
the original theorem statement, the failed proof attempt, and specific error messages from Lean. This self-correction
loop continues until verification succeeds or the self-correction limits are reached (default: 2 attempts per pass, up to
32 passes).
For verified proofs, a parser agent requests the proof’s AST from the Kimina server in order to, if required, use the
AST in the reconstruction of an enclosing proof of which this proof may only be a part.

3.4   Recursive Decomposition

When direct proof generation fails, the system activates recursive decomposition, motivated by the POETRY algo-
rithm [3] and the Hilbert [4] system.
Step 1: Theorem Retrieval. The query generation agent employs a swappable LLM, which is by default Qwen 3
30GB [27], to generate a number of natural language descriptions of theorems it thinks would be useful in the proof
sketching task. (The prompts it employs are provided in full in Appendices B.4 and B.5). Using these natural language
descriptions the theorem lookup agent then queries a vector database, we employ a LeanExplore variant [56], to obtain
a number of theorems that may be of use in the proof sketching task.
Step 2: Proof Sketching. The proof sketcher agent employs a swappable frontier LLM, which is by default GPT-
5 [13], along with the theorems retrieved in the previous step to generate a proof sketch that outlines the high-level
structure using named hypotheses and placeholder proofs (the prompts it employs are provided in full in Appen-
dices B.6, B.7, and B.8):

  import Mathlib
  import Aesop

  set_option maxHeartbeats 0

  open BigOperators Real Nat Topology Rat

  variable (P Q R : Nat → Prop)

  theorem complex_theorem (n : Nat) : P n := by
    have lemma1 : Q n := by sorry
    have lemma2 : Q n → P n := by sorry
    apply lemma2
    exact lemma1


The sketch provides the overall proof strategy while deferring subgoal proofs to sorry tactics. The model is prompted
to create sketches that are logically sound (in that the combination of assumed lemmas implies the theorem), self-
contained (in that each lemma is independently provable), and appropriately granular (in that the lemmas are simpler
than the original theorem but not trivial).
Step 3: Sketch Validation. The sketch checker submits the proof sketch to the Kimina server for validation. Lean
verifies that the sketch is syntactically correct, that the types of all have statements are well-formed, and that the
combination of assumed subgoals (with sorry proofs) logically implies the theorem statement.
When validation fails, a corrector agent analyzes the error messages and requests a sketch revision. Common errors
include type mismatches in hypotheses and the have statements not entailing the main theorem. When repeated
correction attempts fail (default: 6 attempts), a “backtrack” occurs and an ancestor is decomposed in a different
manner, one that emphasizes alternative proof approaches.
Step 4: AST-Based Extraction. The parser agent requests the AST of the proof sketch from the Kimina server using
the /api/ast_code endpoint (the details of which appear in Appendix A). The decomposition agent then traverses
the AST in order to identify all unproven subgoals—that is, have statements followed by by sorry. For each subgoal,
the system extracts the subgoal name, proof “type” (e.g. sorry), the complete theorem statement with appropriate
context, and type information from the sorries metadata.


                                                           5
Gödel’s Poetry


The AST traversal algorithm recursively walks the syntax tree, thereby identifying proof nodes and extracting subgoal
information. A sketch of this algorithm takes the form:

  function ExtractSubgoals(ast):
      subgoals := []
      TraverseNode(ast, subgoals)
      return subgoals

  function TraverseNode(node, subgoals):
      if node.type = "have" and node.proof.type = "sorry":
          subgoal := {name: node.name, type: node.type_expr}
          subgoals.append(subgoal)
      for each child in node.children:
          TraverseNode(child, subgoals)



Step 5: Recursive Proving. Each extracted subgoal becomes a new formal theorem at depth d + 1 in the proof
tree. The system then recursively applies the complete proving pipeline (that is, direct proof generation with fallback
to decomposition) to each subgoal. This creates a tree of proof obligations, wherein each node tracks its parent
decomposition, sibling nodes represent independent subgoals, and depth limits serve to prevent infinite decomposition
(default: 20 levels).
The recursive proving proceeds in breadth-first fashion: all subgoals at a given depth are processed before proceeding
to deeper levels. When a subgoal exceeds the maximum depth limit (max_depth, default: 20), the system attempts
to backtrack to a backtrackable grandparent or higher ancestor in the proof tree. This ancestor is then re-decomposed
with an alternative strategy, potentially yielding a shallower proof structure. Backtracking occurs only if the ancestor
has not exhausted its self-correction attempts, thereby enabling the exploration of alternative decomposition strategies.
If no backtrackable ancestor exists, the proof terminates with an appropriate error message. This mechanism serves to
prevent premature termination when a shallower decomposition strategy might succeed, while still maintaining depth
limits to prevent unbounded exploration.
Step 6: Proof Reconstruction. Once all subgoals verify successfully, the reconstruction algorithm (recursively)
replaces each sorry placeholder in the parent sketch with the verified sub-proof body, producing a complete verified
proof. A sketch of this algorithm takes the form:

  function ReconstructProof(node):
      if node is leaf:
          return node.formal_proof
      sketch := node.proof_sketch
      for each child in node.children:
          child_proof := ReconstructProof(child)
          proof_body := ExtractProofBody(child_proof)
          sketch := ReplaceSubgoal(sketch, child.name, proof_body)
      return sketch

  function ExtractProofBody(proof):
      // Extract tactics after "by", excluding theorem declaration
      pattern := r"by\s+(.+)"
      return regex.match(pattern, proof).group(1)

  function ReplaceSubgoal(sketch, name, proof_body):
      // Replace "have name : ... := by sorry" with complete proof
      pattern := f"have {name} : .* := by sorry"
      replacement := f"have {name} : ... := by {proof_body}"
      return regex.sub(pattern, replacement, sketch)



The reconstruction maintains proper indentation and formatting.


                                                           6
Gödel’s Poetry


3.5   State Management

The supervisor agent implements a state machine that determines the next action based upon the current proof state.
The implementation employs LangGraph [9], which provides a framework for stateful, multi-agent applications with
cyclic workflows.
The state manager tracks several categories of information: theorems awaiting formalization, validation, or semantic
checking; theorems awaiting proof generation or verification; theorems requiring decomposition or sketch validation;
the complete proof tree with parent-child relationships; verification status and error messages for all nodes; and the
action history for debugging purposes. The state manager also implements depth-based backtracking: when children
exceed the maximum depth, the system identifies backtrackable ancestors (at grandparent level or higher) and queues
them for re-decomposition, rather than immediately terminating the proof attempt.
The supervisor queries the state manager in order to identify pending work, employing the following priority rules:
formalize informal theorems (highest priority), validate formal theorems syntactically, check semantic equivalence,
attempt direct proof generation, verify generated proofs, parse successful proofs into ASTs, query for useful theorems,
decompose failed proofs, and recursively prove subgoals.

4     Example
To demonstrate the capabilities of the system, we consider the task of proving that the sum of two even numbers is
even.
Informal Input: “Prove that for any natural numbers m and n, if m is even and n is even, then m + n is even.”
Formalization. The Goedel-Formalizer-V2 model produces the following (examples include the system’s standard
Lean preamble):

    theorem theorem_b2f45cfb951a : ∀ m n : N, Even m → Even n → Even (m + n) := by
      sorry


Syntax Validation. The Kimina server [10] confirms that the formalization is syntactically valid and type-correct.
Semantic Checking. qwen3:30b [27] verifies that the formalization preserves the meaning of the informal statement.
Direct Proof Attempt. Goedel-Prover-V2 [2] using verifier-guided self-correction suggests the following proof:

    import Mathlib
    import Aesop

    set_option maxHeartbeats 0

    open BigOperators Real Nat Topology Rat

    theorem theorem_b2f45cfb951a : ∀ m n : N, Even m → Even n → Even (m + n) := by
      intro m n hm hn
      have h_main : Even (m + n) := by
        -- Extract the witnesses for m and n being even
        cases' hm with a ha
        cases' hn with b hb
        -- Rewrite m and n as 2a and 2b respectively
        rw
        -- Factor out the 2 from the sum 2a + 2b
        use a + b
        <;> ring
        <;> simp
        <;> ring
      -- The main result follows directly from the above steps
      exact h_main


Verification. The Kimina server verifies that the proof succeeds.


                                                          7
Gödel’s Poetry


For a more complex example that requires decomposition, we consider the task of proving the infinitude of primes.
When direct proof generation fails after exhausting the configured self-correction loop (default: 2 attempts per pass,
up to 32 passes), the system activates decomposition. The GPT-5 model generates the following:
    import Mathlib
    import Aesop

    set_option maxHeartbeats 0

    open BigOperators Real Nat Topology Rat

    theorem infinitude_of_primes : ∀ n : Nat, ∃ p, p > n ∧ Prime p := by
      -- Step 1: Define product of all primes ≤ n
      have prod_primes_def
                        Q :
          ∀ n, ∃ P, P =    p in Finset.filter Prime (Finset.range (n + 1)), p := by
        sorry

      -- Step 2: For given n, take P = product of all primes ≤ n
      have choose_P : Q
          ∀ n, ∃ P, P =    p in Finset.filter Prime (Finset.range (n + 1)), p := by
        sorry

      -- Step 3: Show that P + 1 has a prime divisor
      have prime_divisor_exists  :
          ∀ n P, P =    p in Finset.filter Prime (Finset.range (n + 1)), p →
                     Q
            ∃ q, Prime q ∧ q | (P + 1) := by
        sorry

      -- Step 4: Show that such a prime divisor q is greater than n
      have divisor_gt_n :
          ∀ n P q,Q
              P =    p in Finset.filter Prime (Finset.range (n + 1)), p →
                Prime q → q | (P + 1) → q > n := by
        sorry

      -- Step 5: Combine to conclude existence of a prime > n
      have conclusion : ∀ n, ∃ p, p > n ∧ Prime p := by
        sorry

      exact conclusion


The AST parser identifies five subgoals: prod_primes_def, choose_P, prime_divisor_exists, divisor_gt_n,
and conclusion. Each subgoal is then independently proved (or, if necessary, further decomposed). Once all subgoals
have been proven, the reconstruction algorithm substitutes their proofs into the sketch, thereby producing a complete
verified proof.

5     Implementation
5.1    Installation and Deployment

The system is distributed through PyPI as goedels-poetry, thereby enabling straightforward installation with pip
install goedels-poetry. The package installs the Python dependencies used by the framework (for example,
LangGraph, LangChain, Kimina AST client, LeanExplore client, Rich, Typer) and a command-line interface acces-
sible via goedels_poetry. It does not install any model backends; callers supply their own OpenAI-compatible
endpoints (e.g., OpenAI, Ollama, vLLM, or LM Studio) and run the required external services.
The system requires the Kimina Lean Server for verification. A packaged distribution, kimina-ast-server on PyPI,
installs Lean 4, mathlib4, the AST exporter, and a FastAPI front end; running kimina-ast-server setup fol-
lowed by kimina-ast-server starts the verifier (default: http://localhost:8000). The system also depends


                                                          8
Gödel’s Poetry


on the LeanExplore server (lean-xplore on PyPI) to provide semantic search over Mathlib declarations; start-
ing leanexplore http serve –backend local (default: http://localhost:8001/api/v1) enables vector-
database retrieval for the search and sketching agents. With both services running and an LLM backend configured,
users may immediately begin proving theorems through either the CLI or the Python API.
For purposes of development and extension, the source code is available at https://github.com/KellyJDavis/
goedels-poetry under the Apache 2.0 license. The modular architecture enables researchers to add custom agents,
implement alternative decomposition strategies, or integrate additional LLM providers, all without modifying the core
framework code.

5.2   Architecture and Components

The system is implemented in Python 3.10+ using LangGraph [9] for multi-agent orchestration and LangChain [25] for
LLM interaction. The codebase consists of approximately 5,000 lines organized into modular components: the Agents
component (goedels_poetry/agents/) implements 18 agent types spanning formalization, semantics checking,
search-query generation, vector-database lookup, proving, verification, sketching, backtracking, and supervision; State
Management (goedels_poetry/state.py) provides tree-structured state representation and proof reconstruction
logic (800 lines); AST Parsing (goedels_poetry/parsers/) provides AST traversal and subgoal extraction utilities
(now enriched with type binders recovered from Lean “sorries”); Configuration (goedels_poetry/config/) man-
ages LLM selection and Kimina server connections. The decomposer uses an OpenAI backend (default: GPT-5) while
the remaining agents default to a local Ollama endpoint; vLLM or LM Studio may be selected through configuration
overrides.
The system supports flexible LLM configuration through a declarative INI file and environment variable overrides.
Researchers may specify different models for each agent role, thereby enabling experimentation with various model
combinations.
Any OpenAI model compatible with the langchain_openai.ChatOpenAI class is supported for theorem decompo-
sition. Similarly, any model compatible with the langchain_openai.ChatOpenAI class may be used for formal-
ization, proving, semantic checking, and search-query generation. Vector retrieval is delegated to LeanExplore and is
controlled via explicit configuration.
As an example, the default configuration (goedels_poetry/data/config.ini) is:

  [FORMALIZER_AGENT_LLM]
  model = kdavis/goedel-formalizer-v2:32b
  provider = ollama
  url = http://localhost:11434/v1
  api_key = ollama
  max_tokens = 50000
  num_ctx = 40960
  max_retries = 10
  max_remote_retries = 5

  [PROVER_AGENT_LLM]
  model = kdavis/Goedel-Prover-V2:32b
  provider = ollama
  url = http://localhost:11434/v1
  api_key = ollama
  max_tokens = 50000
  num_ctx = 40960
  max_self_correction_attempts = 2
  max_depth = 20
  max_pass = 32
  max_remote_retries = 5

  [SEMANTICS_AGENT_LLM]
  model = qwen3:30b
  provider = ollama
  url = http://localhost:11434/v1
  api_key = ollama


                                                          9
Gödel’s Poetry


  max_tokens = 50000
  num_ctx = 262144
  max_remote_retries = 5

  [SEARCH_QUERY_AGENT_LLM]
  model = qwen3:30b
  provider = ollama
  url = http://localhost:11434/v1
  api_key = ollama
  max_tokens = 50000
  num_ctx = 262144
  max_remote_retries = 5

  [DECOMPOSER_AGENT_LLM]
  model = gpt-5-2025-08-07
  max_completion_tokens = 50000
  max_remote_retries = 5
  max_self_correction_attempts = 6

  [KIMINA_LEAN_SERVER]
  url = http://0.0.0.0:8000
  max_retries = 5

  [LEAN_EXPLORE_SERVER]
  url = http://localhost:8001/api/v1
  package_filters = Mathlib,Batteries,Std,Init,Lean


This configuration specifies that formalization and proving employ locally hosted 32B models via Ollama, that seman-
tic checking and search-query generation use qwen3:30b, that decomposition relies on an OpenAI GPT-5 endpoint,
that verification is handled by the Kimina server, and that vector retrieval uses a local LeanExplore server filtered to
Mathlib, Batteries, Std, Init, and Lean declarations. Providers may be switched to vLLM or LM Studio via environ-
ment variable overrides.

5.3   Environment Variable Configuration

All configuration parameters may be overridden through environment variables, thereby enabling deployment-specific
customization without the need to modify configuration files or code. Environment variables employ the format
SECTION__OPTION (with double underscore separator, uppercase). For example:

  # Override prover model
  export PROVER_AGENT_LLM__MODEL="custom-model:latest"

  # Use different Kimina server
  export KIMINA_LEAN_SERVER__URL="http://production-server:8000"

  # Adjust context window
  export PROVER_AGENT_LLM__NUM_CTX="8192"


This mechanism supports multiple deployment scenarios: development environments employing smaller models for
faster iteration, continuous integration environments with dedicated verification servers, and production deployments
with frontier models and distributed infrastructure. Environment variables take precedence over config.ini values,
thereby enabling flexible configuration management without the need for reinstallation.

5.4   Performance

Without decomposition and using the default configuration, the system achieves a 90.4% pass rate on miniF2F, as
this is no more than the Goedel-Prover-V2 system using verifier-guided self-correction at pass@32. With RAG and
recursive decomposition, this is significantly improved but has yet to be fully benchmarked.


                                                          10
Gödel’s Poetry


The system’s other performance characteristics are determined by several factors, with LLM inference forming the
primary bottleneck. For informal theorems, formalization latency depends upon the model size and the complexity of
the mathematical statement. Semantic checking with frontier models represents an additional overhead incurred per
formalization attempt.
Direct proof generation with specialized models such as Goedel-Prover-V2 exhibits higher latency for complex theo-
rems that require extensive context. Verification through the Kimina Lean Server is comparatively fast, as it involves
deterministic type checking rather than generation. The system’s retry mechanism serves to amplify latency when
theorems fail direct proving, as multiple generation-verification cycles occur prior to decomposition.
Proof sketching with frontier models introduces additional latency that scales with both the theorem complexity and
the number of decomposition strategies attempted. AST parsing latency depends primarily upon the complexity of
import structures in the generated code, rather than upon the proof length.
The current implementation enforces consistent Lean preambles across all formal artifacts. Any incoming Lean the-
orem is first split into preamble and body components; the preamble is normalized, augmented with mandatory di-
rectives such as set_option maxHeartbeats 0, and persisted with the proof state. Reconstruction routines sub-
sequently recombine the stored preamble with regenerated proof bodies, ensuring that proof outputs carry the exact
header required for downstream verification. The command-line interface mirrors this logic: it rejects formal inputs
that omit a Lean header and emits diagnostic files explaining the requirement. This end-to-end normalization prevents
subtle failures when default imports evolve and guarantees that proofs produced by the system are always accompanied
by the proper Lean context.
Memory consumption is dominated by the proof tree structure, which retains all intermediate proofs, LLM conver-
sation histories, and verification results. For deeply nested recursive decompositions, memory usage scales linearly
with both tree depth and breadth. The configuration parameter max_depth provides a safety limit intended to prevent
unbounded memory growth.
The architecture naturally supports parallelization at the subgoal level, as sibling subgoals are independent and may be
proved concurrently. The current implementation processes subgoals in parallel using LangGraph’s Send API. This
approach yields substantial speedups for theorems that decompose into many independent subgoals, with speedup
limited primarily by the available computational resources and LLM API rate limits.


5.5   Kimina Server Extensions

As detailed in Appendix A, we have extended the Kimina Lean Server with two AST endpoints: POST /api/ast,
which exports ASTs for existing Lean modules (e.g., Mathlib.Data.List.Basic), and POST /api/ast_code,
which exports ASTs for dynamically provided Lean code snippets.
The /api/ast_code endpoint proved essential for recursive decomposition. It accepts arbitrary Lean code, creates
a temporary module, configures the correct import paths for Mathlib and the Lean standard library, invokes the AST
exporter, and returns a structured AST representation. This enables real-time analysis of proof sketches generated by
language models, all without the need for manual file management.


6     Discussion

6.1   Comparison with POETRY

While inspired by the work of POETRY [3], our approach exhibits several notable differences. POETRY targets
Isabelle [23], which employs a proof language and tactic system distinct from that of Lean 4. Lean’s tactic mode
encourages a more compositional style with explicit have statements, thereby simplifying subgoal extraction.
POETRY relies upon Isabelle’s proof levels. In contrast, we employ explicit have statements with sorry placeholders,
thereby making subgoals clearly identifiable within the AST. This explicitness serves to improve interpretability: proof
sketches function as documentation of the proof strategy.
POETRY employs a single model for all tasks. We, in contrast, employ specialized models: Goedel-Prover-V2 for
direct proving, and frontier LLMs for decomposition and semantic validation. This specialization serves to improve
performance on each subtask. POETRY assumes that theorems are already formalized in Isabelle. We handle informal
theorems through a dedicated formalization pipeline with semantic validation, thereby broadening the applicability of
the approach.


                                                          11
Gödel’s Poetry


6.2   Concurrent Work: Hilbert

During the development of our system, the Hilbert system [4] independently arrived at similar conclusions regarding
the utility of recursive decomposition for formal theorem proving. Both systems combine informal reasoning with
formal verification, and both employ recursive strategies for complex theorems. Hilbert achieves impressive results:
99.2% on miniF2F and 70.0% on PutnamBench, thereby demonstrating the effectiveness of this approach.
Key architectural similarities include the recursive decomposition of complex problems, coordination between infor-
mal reasoning and formal verification, and the use of multi-component systems with specialized roles. In addition, like
our work Hilbert employs a semantic theorem retriever for the purpose of finding theorems that assist in decomposition.
Hilbert’s implementation details and model configurations are not publicly available, whereas our system emphasizes
open-source extensibility with straightforward model substitution. This convergence upon recursive decomposition
and semantic theorem retrieval strategies from independent research efforts serves to validate this architectural direc-
tion for automated theorem proving.

6.3   Limitations

The system inherits the limitations of its constituent models. The default Goedel-Prover-V2 model excels on
undergraduate-level mathematics but tends to struggle with specialized domains. Decomposition quality depends
upon the default GPT-5 model’s ability to identify productive proof strategies. For highly specialized domains (such
as category theory or abstract algebra), the model may generate decompositions that prove unhelpful. That being said,
all models may be swapped for more capable models. So these limitations may be exceeded.
The maximum recursion depth (default: 20) serves to prevent infinite decomposition. When subgoals exceed this
depth, the system attempts to backtrack to earlier decomposition points and explore alternative strategies, thereby
mitigating premature termination. However, theorems requiring very deep hierarchical reasoning may still fail if all
backtrackable ancestors have exhausted their correction attempts or if no suitable alternative decomposition strategy
exists. The system currently explores one decomposition path at a time.
Deep decomposition of complex theorems may require hundreds of API calls to frontier LLMs, thereby incurring
significant cost. Techniques such as proof caching, early termination heuristics, and model distillation could serve to
reduce these costs.

6.4   Extensibility and Open Source Architecture

The system is released as open source under the Apache 2.0 license, thereby enabling permissive use, modification,
and extension. The codebase (https://github.com/KellyJDavis/goedels-poetry) has been designed for ex-
tensibility at multiple levels.
Model Configuration. The configuration system enables straightforward comparison of different LLMs for each
agent role, all without the need for code modification. Researchers may evaluate whether larger models improve
formalization accuracy, whether specialized models excel at specific proving tasks, or whether mixture-of-experts
approaches outperform single-model strategies. The environment variable override mechanism supports A/B testing
across different deployment configurations.
Agent Extension. The agent-based architecture supports experimentation with alternative reasoning strategies. New
agents may be added through their implementation in LangChain and their registration with the system. This enables
researchers to experiment with other strategies, combine multiple techniques, or use domain-specific proving tactics.
The modular design ensures that new agents integrate seamlessly with the existing orchestration logic.
Search Strategy Customization. The tree structure enables alternative search strategies. The LangGraph framework
can naturally support beam search (wherein multiple decomposition alternatives are maintained simultaneously), best-
first search (wherein promising branches are prioritized based upon estimated difficulty), and adaptive backtracking
(wherein unproductive branches are abandoned intelligently). Researchers may implement custom search heuristics
without the need to modify too much of the core state management code.
Training Data Generation. Successful proof attempts can generate aligned (informal statement, formal theorem,
verified proof) triples that prove suitable for fine-tuning. The hierarchical proofs provide additional training signal
for the learning of decomposition strategies. The complete proof provenance enables synthetic data generation for the
training of specialized formalization and proving models.
Community Extensions. The package distribution via PyPI, comprehensive documentation, and permissive license
serve to facilitate community contributions. Researchers may publish custom agents, alternative decomposition strate-


                                                          12
Gödel’s Poetry


gies, or domain-specific configurations as separate packages that extend the core system. The modular architecture
ensures that extensions remain compatible across version updates.

7   Conclusion
We have presented here a new approach to automated theorem proving, one that combines specialized language models
with recursive decomposition. Through our extension of the Kimina Lean Server with AST parsing capabilities and
our implementation of a multi-agent architecture that supports recursive proof strategies, we provide a practical system
that serves to bridge informal mathematical reasoning with rigorous formal verification in Lean 4.
The key contributions of the system include a multi-stage formalization pipeline with semantic validation, AST-based
subgoal extraction that enables systematic decomposition, a proof reconstruction algorithm that assembles verified
sub-proofs into complete proofs, and a flexible configuration system that supports model substitution via INI files and
environment variables.
The system is made available on PyPI as goedels-poetry, thereby enabling installation with pip install
goedels-poetry. The open-source implementation (released under the Apache 2.0 license) at https://github.
com/KellyJDavis/goedels-poetry facilitates experimentation with alternative models, decomposition strategies,
and proof search algorithms. The modular architecture, built upon LangGraph and LangChain, serves to decouple or-
chestration logic from agent implementations, thereby enabling researchers to extend the system in diverse directions
without the need to modify core functionality. Community contributions are encouraged through both the permissive
licensing and the extensible architecture.
Possible future work includes the incorporation of alternative tree search techniques for exploring multiple decomposi-
tion paths, the integration of proof repair techniques [54] for fixing near-correct proofs, the learning of decomposition
strategies through reinforcement learning, and the extension of the system to collaborative theorem proving, wherein
human experts guide decomposition strategies interactively.

Acknowledgments
We gratefully acknowledge Project Numina for their development of the Kimina Lean Server, Justin Asher for his
development of LeanExplore, the Lean community for their creation of the Lean 4 proof assistant and Mathlib library,
and the developers of Goedel-Prover-V2, whose models power the core proving capabilities of this system. We also
extend our thanks to the developers of LangGraph and LangChain for providing the infrastructure that enables this
multi-agent architecture.

References
 [1] Leonardo de Moura and Sebastian Ullrich. The Lean 4 Theorem Prover and Programming Language. In Interna-
     tional Conference on Automated Deduction (CADE), 2021.
 [2] Yong Lin, Shange Tang, Bohan Lyu, et al. Goedel-Prover-V2: Scaling Formal Theorem Proving with Scaffolded
     Data Synthesis and Self-Correction. arXiv preprint arXiv:2508.03613, 2025.
 [3] Haiming Wang, Huajian Xin, Zhengying Liu, et al. Proving Theorems Recursively. arXiv preprint
     arXiv:2405.14414, 2024.
 [4] Sumanth Varambally, Thomas Voice, Yanchao Sun, et al. Hilbert: Recursively Building Formal Proofs with
     Informal Reasoning. arXiv preprint arXiv:2509.22819, 2025.
 [5] Luoxin Chen, Jinming Gu, et al. Seed-Prover: Deep and Broad Reasoning for Automated Theorem Proving.
     arXiv preprint arXiv:2507.23726, 2025.
 [6] Yichi Zhou, Jianqiu Zhao, et al. Solving Formal Math Problems by Decomposition and Iterative Reflection. arXiv
     preprint arXiv:2507.15225, 2025.
 [7] Ran Xin, Zeyu Zheng, et al. Scaling up Multi-Turn Off-Policy RL and Multi-Agent Tree Search for LLM Step-
     Provers. arXiv preprint arXiv:2509.06493, 2025.
 [8] Tudor Achim, Alex Best, et al. Aristotle:           IMO-level Automated Theorem Proving. arXiv preprint
     arXiv:2510.01346, 2025.
 [9] LangChain AI. LangGraph: Build resilient language agent applications. https://langchain-ai.github.
     io/langgraph/, 2024.


                                                           13
Gödel’s Poetry


[10] Marco Dos Santos, Haiming Wang, Hugues de Saxcé, et al. Kimina Lean Server: Technical Report. arXiv
     preprint arXiv:2504.21230, 2025.
[11] John Harrison, Josef Urban, and Freek Wiedijk. History of Interactive Theorem Proving. Handbook of the History
     of Logic, 2014.
[12] X AI. Grock 4. https://x.ai/news/grok-4, 2025.
[13] OpenAI. Introducing GPT-5. https://openai.com/index/introducing-gpt-5/, 2025.
[14] Anthropic. Introducing Claude Sonnet 4.5. https://www.anthropic.com/news/claude-sonnet-4-5,
     2025.
[15] Anthropic. Introducing Claude Haiku 4.5. https://www.anthropic.com/news/claude-haiku-4-5, 2025.
[16] Zhaoyu Li and Jialiang Sun, et al. A Survey on Deep Learning for Theorem Proving. arXiv preprint
     arXiv:2404.09939, 2024.
[17] Z. Z. Ren, Zhihong Shao, et al. DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Rein-
     forcement Learning for Subgoal Decomposition. arXiv preprint arXiv:2504.21801, 2025.
[18] Haiming Wang, Mert Unsal, et al. Kimina-Prover Preview: Towards Large Formal Reasoning Models with
     Reinforcement Learning. arXiv preprint arXiv:2504.11354, 2025.
[19] OpenAI. GPT-4 Technical Report. arXiv preprint arXiv:2303.08774, 2023.
[20] Abhimanyu Dubey, Abhinav Jauhri, et al. The Llama 3 Herd of Models. arXiv preprint arXiv:2407.21783, 2024.
[21] Hunter Lightman, Vineet Kosaraju, et al. Let’s Verify Step by Step. arXiv preprint arXiv:2305.20050, 2023.
[22] Zhangir Azerbayev, Hailey Schoelkopf, et al. Llemma: An Open Language Model For Mathematics. arXiv
     preprint arXiv:2310.10631, 2023.
[23] Tobias Nipkow, Markus Wenzel, and Lawrence C. Paulson. Isabelle/HOL: A Proof Assistant for Higher-Order
     Logic. Springer, 2002.
[24] The Coq Development Team. The Coq Proof Assistant. https://coq.inria.fr/, 2024.
[25] Harrison Chase. LangChain: Building applications with LLMs through composability. https://github.com/
     langchain-ai/langchain, 2024.
[26] Anthropic. Claude 3.5 Sonnet. https://www.anthropic.com/, 2024.
[27] Qwen.       Qwen3:               Think      Deeper,        Act      Faster.     https://qwen.ai/blog?id=
     1e3fa5c2d4662af2855586055ad037ed9e555125&from=research.research-list, 2025.
[28] Cezary Kaliszyk, Josef Urban, et al. Reinforcement Learning of Theorem Proving. In NeurIPS, 2018.
[29] Stanislas Polu, Jesse Michael Han, et al. Formal Mathematics Statement Curriculum Learning. In ICLR, 2023.
[30] Jesse Michael Han, Jason Rute, et al. Proof Artifact Co-Training for Theorem Proving with Language Models.
     In ICLR, 2022.
[31] Albert Q Jiang, Wenda Li, et al. LISA: Language Models of Isabelle Proofs. In ICLR, 2021.
[32] Liao Zhang, Lasse Blaauwbroek, et al. Learning Proof Transformations and Its Applications in Interactive The-
     orem Proving. In FroCoS, 2023.
[33] Eric Yeh, Briland Hitaj, et al. CoProver: A Recommender System for Proof Construction. In CICM, 2023.
[34] Jing Xiong, Jianhao Shen, et al. TRIGO: Benchmarking Formal Mathematical Proof Reduction for Generative
     Language Models. In EMNLP, 2023.
[35] Sean Welleck, Jiacheng Liu, et al. NaturalProofs: Mathematical Theorem Proving in Natural Language. In
     NeurIPS, 2021.
[36] Rahul Vishwakarma and Subhankar Mishra. Enhancing Neural Theorem Proving through Data Augmentation
     and Dynamic Sampling Method. arXiv preprint arXiv:2312.14188, 2023.
[37] Xin Huajian, Z. Z. Ren, et al. DeepSeek-Prover-V1.5: Harnessing Proof Assistant Feedback for Reinforcement
     Learning and Monte-Carlo Tree Search. arXiv preprint arXiv:2408.08152, 2024.
[38] Xin Huajian, Z. Z. Ren, et al. DeepSeek-Prover-V1.5: Harnessing Proof Assistant Feedback for Reinforcement
     Learning and Monte-Carlo Tree Search. arXiv preprint arXiv:2408.08152, 2024.
[39] Ashish Vaswani, Noam Shazeer, et al. Attention Is All You Need. arXiv preprint arXiv:1706.03762, 2017.
[40] Kshitij Bansal, Sarah M. Loos, et al. HOList: An Environment for Machine Learning of Higher-Order Logic
     Theorem Proving. In ICML, 2019.


                                                        14
Gödel’s Poetry


[41] Stanislas Polu and Ilya Sutskever. Generative Language Modeling for Automated Theorem Proving. arXiv
     preprint arXiv:2009.03393, 2020.
[42] Huajian Xin, Daya Guo, et al. DeepSeek-Prover: Advancing Theorem Proving in LLMs through Large-Scale
     Synthetic Data. arXiv preprint arXiv:2405.14333, 2024.
[43] Trieu H. Trinh, Yuhuai Wu, et al. Solving Olympiad Geometry without Human Demonstrations. Nature, 2024.
[44] Kunhao Zheng, Jesse Michael Han, et al. miniF2F: A Cross-System Benchmark for Formal Olympiad-Level
     Mathematics. In ICLR, 2022.
[45] Zhangir Azerbayev, Bartosz Piotrowski, et al. ProofNet: Autoformalizing and Formally Proving Undergraduate-
     Level Mathematics. arXiv preprint arXiv:2302.12433, 2023.
[46] George Tsoukalas, Jasper Lee, et al. PutnamBench: Evaluating Neural Theorem-Provers on the Putnam Mathe-
     matical Competition. arXiv preprint arXiv:2407.11214, 2024.
[47] The mathlib Community. The Lean Mathematical Library. In CPP, 2020.
[48] Sebastián Ramírez. FastAPI: Modern, fast web framework for building APIs with Python. https://fastapi.
     tiangolo.com/, 2024.
[49] Wenda Li, Lei Yu, et al. IsarStep: A Benchmark for High-level Mathematical Reasoning. In ICLR, 2021.
[50] Kaiyu Yang and Jia Deng. Learning to Prove Theorems via Interacting with Proof Assistants. In ICML, 2019.
[51] Renjun Xu and Jingwen Peng. A Comprehensive Survey of Deep Research: Systems, Methodologies, and Ap-
     plications. arXiv preprint arXiv:2506.12594, 2025.
[52] Guillaume Lample, Timothée Lacroix, et al. HyperTree Proof Search for Neural Theorem Proving. In NeurIPS,
     2022.
[53] Albert Q. Jiang, Sean Welleck, et al. Draft, Sketch, and Prove: Guiding Formal Theorem Provers with Informal
     Proofs. In ICLR, 2023.
[54] Emily First, Markus N. Rabe, Talia Ringer, and Yuriy Brun. Baldur: Whole-Proof Generation and Repair with
     Large Language Models. In FSE, 2023.
[55] Norman Megill and David A. Wheeler. Metamath: A Computer Language for Mathematical Proofs. Lulu Press,
     2019.
[56] Justin Asher. LeanExplore: A search engine for Lean 4 declarations. arXiv preprint arXiv:2506.11085, 2025.




                                                       15
Gödel’s Poetry


A     Kimina Lean Server AST Extensions

This appendix describes AST export functionality that was added to the Kimina Lean Server for the purpose of recur-
sive decomposition.

A.1     Motivation

Recursive proof decomposition requires the programmatic extraction of unproven subgoals from proof sketches. While
Lean’s compiler identifies syntactic structure, the extraction of specific theorem statements with complete context and
type information requires parsing of the abstract syntax tree. The Lean community’s ast-export tool provides this
capability, but the original Kimina server lacked an API endpoint through which to access it.

A.2     AST Export Tool

The ast-export tool (available at https://github.com/KellyJDavis/ast_export) exports Lean module defi-
nitions as structured JSON. For a given module, it produces a nested representation containing all theorem declarations
(with their types and proof terms), hypothesis bindings within proofs (such as have statements), tactic invocations and
their subgoals, and placeholders (sorry) that indicate unproven statements. The tool operates as a standalone Lake
executable that is built against the same Lean version as the Kimina server.

A.3     Implementation

We added a router module server/routers/ast.py that implements two endpoints.

A.3.1    Module AST Endpoint
The POST /api/ast endpoint accepts a request that specifies modules, whether to export only the specified module
(the one flag), and a timeout value. For each specified module, the endpoint invokes lake exe ast-export with
the –one flag (which exports only the specified module, not its dependencies). The exporter writes JSON output to
.lake/build/lib/<module_path>.out.json. The endpoint then reads this file and returns structured results that
include the module name, the AST, execution time, and diagnostics.
The endpoint employs a semaphore (manager.ast_semaphore) to limit concurrent AST exports, thereby preventing
resource exhaustion during batch processing.

A.3.2    Code AST Endpoint
The POST /api/ast_code endpoint proved essential for the analysis of dynamically generated proof sketches. It
accepts arbitrary Lean code, a module name, and a timeout value.
The endpoint creates a temporary directory with a src/ subdirectory, and writes the provided code to
src/User/Code.lean. It constructs LEAN_SRC_PATH to include the temporary src/ directory, the mathlib4 project
directory, and the .lake/packages directory. It constructs LEAN_PATH to include compiled libraries (the .olean
files), such that imported notations and macros are available during parsing. The endpoint then invokes lake exe
ast-export –one User.Code, reads the generated .lake/build/lib/User/Code.out.json, returns the parsed
AST, and performs cleanup.
The critical insight lay in the correct configuration of Lean source and library paths. Initially, the endpoint failed to
resolve import Mathlib statements. The solution involved setting LEAN_SRC_PATH to include both the temporary
source and the local mathlib4 checkout, setting LEAN_PATH to include the compiled libraries, and running the exporter
via lake within the AST exporter project directory. This configuration enables the AST exporter to process arbitrary
Lean code with full Mathlib support.

A.4     Error Handling

Both endpoints implement robust error handling: asynchronous subprocess execution with timeout enforcement serves
to prevent hanging on malformed input; Lean compilation errors are captured from stderr and returned in the error field;
module names are validated against a regex in order to prevent directory traversal attacks; all AST export operations
are logged with timing information; and responses include both execution time and AST size metrics.


                                                           16
Gödel’s Poetry


A.5    Integration

The parser agents invoke the /api/ast_code endpoint with proof sketches that have been generated by the decompo-
sition agent. The returned AST is wrapped within an AST class (goedels_poetry/parsers/ast.py) that provides
methods for get_unproven_subgoal_names() (which traverses the AST in order to identify all sorry placeholders
and extract the names of associated hypotheses), get_named_subgoal_code(name) (which retrieves complete Lean
code for a specific subgoal, including context and type information from the sorries metadata), and get_ast()
(which returns the raw AST for custom analysis).
This abstraction serves to decouple decomposition logic from AST structure details, thereby enabling the maintenance
of extraction logic independently of changes to the Lean AST format.

A.6    Code Availability

The AST endpoint implementation and AST exporter tool integration are available at
https://github.com/KellyJDavis/kimina-lean-server
in the main branch.

B     Agent Prompts
This appendix provides the complete prompts used by each agent in the Gödel’s Poetry system.

B.1    Formalizer Agent Prompt

The formalizer agent uses the following prompt to translate informal mathematical statements into Lean 4:

    Please autoformalize the following natural language problem statement in Lean 4. Use the
        following theorem name: {{ formal_statement_name }}

    The natural language statement is:

    {{ informal_statement }}

    Think before you provide the lean statement.



B.2    Prover Agent Initial Prompt

The prover agent uses the following initial prompt for direct proof generation:

    Complete the following Lean 4 code:

    ```lean4
    {{ formal_statement }}```

    Before producing the Lean 4 code to formally prove the given theorem, provide a detailed proof
        plan outlining the main proof steps and strategies.
    The plan should highlight key ideas, intermediate lemmas, and proof structures that will guide
        the construction of the final formal proof.

    IMPORTANT: When you've completed your planning you should output your proof of the Lean 4 code
        within a ```lean4...``` code block.

    IMPORTANT: Your proof should actually prove the theorem or lemma using Lean 4 code. It should
        not contain sorry, admit, or any other Lean 4 tactics that indicate an incomplete proof.

    IMPORTANT: Your completion should contain ONLY the theorem/def and its proof. Do NOT include
        any import statements or preamble (like `import Mathlib`, `open`, `set_option`, `


                                                          17
Gödel’s Poetry


       noncomputable section`, etc.) as these are already provided in the code above. Start
       directly with your theorem/definition/lemma declaration.


B.3   Prover Agent Subsequent Prompt

When proof attempts fail, the prover agent uses this correction prompt:

  The proof (Round {{ prev_round_num }}) is not correct. Following is the compilation error
      message, where we use <error></error> to signal the position of the error.

  {{ error_message_for_prev_round }}

  Before producing the Lean 4 code to formally prove the given theorem, provide a detailed
      analysis of the error message.

  IMPORTANT: When you've completed your detailed analysis of the error message you should output
      your proof in Lean 4 code within a ```lean4...``` code block.

  IMPORTANT: Your proof should actually prove the theorem or lemma using Lean 4 code. It should
      not contain sorry, admit, or any other Lean 4 tactics that indicate an incomplete proof.

  IMPORTANT: Your corrected proof should contain ONLY the theorem/def and its proof. Do NOT
      include any import statements or preamble (like `import Mathlib`, `open`, `set_option`, `
      noncomputable section`, etc.). Start directly with your theorem/definition/lemma
      declaration.


B.4   Query Agent Initial Prompt

The query agent initially uses the following prompt to generate natural language descriptions of potentially useful
theorems:

  You are a search query generation assistant for a mathematical theorem proving system. Your
      task is to generate diverse search queries that will help find relevant theorems, lemmas,
      and tactics from a mathematical library (like Mathlib) that could be useful for proving the
       given formal theorem.

  Given a Lean 4 formal theorem statement, generate 3-5 diverse search queries that cover
      different aspects:
  - Key mathematical concepts and structures mentioned in the theorem
  - Related lemmas or theorems that might be useful
  - Specific tactics or proof techniques that could apply
  - Important properties or relationships

  Each query should be concise and focused on a specific aspect that could help in proving the
      theorem.

  Here is the formal theorem statement:

  ```lean4
  {{ formal_theorem }}
  ```

  Generate your search queries below, each enclosed in <search> tags:

  <search>your first search query here</search>
  <search>your second search query here</search>
  <search>your third search query here</search>


                                                         18
Gödel’s Poetry


B.5   Query Agent Backtrack Prompt

The query agent when backtracking uses the following prompt to generate natural language descriptions of potentially
useful theorems:

  You are a search query generation assistant for a mathematical theorem proving system. Your
      task is to generate diverse search queries that will help find relevant theorems, lemmas,
      and tactics from a mathematical library (like Mathlib) that could be useful for proving the
       given formal theorem.

  **IMPORTANT**: A previous attempt to prove this theorem failed. The previous decomposition
      strategy was syntactically valid but the decomposed subgoals could not be proven after
      multiple attempts. This suggests the previous approach may not have been the right strategy
      .

  Given the formal theorem statement and the conversation history about the previous failed
      attempt, generate 3-5 NEW and DIFFERENT search queries that:
  - Explore alternative mathematical concepts or structures
  - Consider different proof techniques or approaches
  - Focus on different aspects of the problem than the previous attempt
  - May lead to a simpler or more direct proof path

  Each query should be concise and focused on a specific aspect that could help in proving the
      theorem using a different strategy.

  Here is the formal theorem statement:

  ```lean4
  {{ formal_theorem }}
  ```

  The conversation history above contains information about the previous failed attempt. Use that
       context to generate different search queries.

  Generate your search queries below, each enclosed in <search> tags. Make sure they are
      different from what might have been used in the previous attempt:

  <search>your first search query here</search>
  <search>your second search query here</search>
  <search>your third search query here</search>



B.6   Decomposer Agent Initial Prompt

The decomposer agent uses the following prompt for initial proof decomposition:

  You are a Lean 4 formal theorem prover assistant. Your task is to take a Lean theorem statement
       and:

  1. Think and provide a natural-language proof sketch that explains the reasoning strategy.
  2. Decompose the proof into smaller formal Lean 4 have statements (subgoals) subordinate to the
       main Lean 4 theorem statement, i.e. contained within the by block of the main Lean 4
      theorem.
  3. When decomposing the proof, use existing proven theorems from the list below if warranted to
       help establish subgoals or simplify the decomposition.
  4. Output Lean 4 code where each subgoal is expressed as a have statement ending with sorry, so
       that another prover can attempt to solve them recursively.
  5. Ensure that the top-level Lean 4 theorem does not contain a sorry that is directly
      subordinate to it.


                                                        19
Gödel’s Poetry


  6. Ensure that the top-level Lean 4 theorem is entailed by the smaller formal Lean 4 have
      statements (subgoals) along, possibly, with other Lean 4 code within the by block of the
      main Lean 4 theorem.
  7. Ensure that later subgoals may assume earlier ones as premises if helpful.
  8. Do not attempt to fully solve the subgoals -- only set up the structured decomposition.
  9. Do not introduce auxiliary lemmas or any other statements not subordinate to the main Lean 4
       theorem.
  10. In particular do not introduce an unexpected identifier or unexpected command such as "
      Complex" before the main Lean 4 theorem statement.

  When decomposing the proof, you may find it helpful to use existing proven theorems from the
      list below. For example:
  - You might use an existing theorem like `Nat.add_comm` to simplify expressions involving
      addition
  - You might apply a theorem about inequalities to establish relationships between terms
  - You might use a theorem about properties of functions to transform the goal into a more
      manageable form
  - You might combine multiple existing theorems to build up to the desired conclusion

  Consider how these existing theorems might be incorporated into your proof sketch, either
      directly in the decomposition or as intermediate steps that help establish the subgoals.

  {{ theorem_hints_section }}

  Example input theorem:

  ```lean4
  theorem induction_ineq_nsqlefactn (n : N) (h : 4 ≤ n) : n ^ 2 ≤ n ! := by
    sorry```

  Expected output format:

  * Natural language reasoning: high-level strategy (e.g., induction).
  * Formal Lean code: theorem restated, followed by subgoal decomposition.

  Example output (sketch):

  Natural language proof sketch:
  We prove by induction on n. Base case: verify for n = 4. Inductive step: assume k^2 ≤ k! for
      some k ≥ 4, then show (k+1)^2 ≤ (k+1)!.

  Lean code with subgoals:
  ```lean4
  theorem induction_ineq_nsqlefactn (n : N) (h : 4 ≤ n) : n ^ 2 ≤ n ! := by
    -- Base case
    have base_case : 4 ^ 2 ≤ 4 ! := by
      sorry

   -- Inductive step
   have inductive_step : ∀ k ≥ 4, k ^ 2 ≤ k ! → (k + 1) ^ 2 ≤ (k + 1) ! := by
     sorry

    -- Combine base case and inductive step
    have final_proof : ∀ n ≥ 4, n ^ 2 ≤ n ! := by
      sorry
  ```

  Here is the Lean 4 formal theorem to decompose:



                                                20
Gödel’s Poetry


  ```lean4
  {{ formal_theorem }}```



B.7   Decomposer Agent Subsequent Prompt

When sketch validation fails, the decomposer agent uses this correction prompt:

  The proof sketch (Round {{ prev_round_num }}) is not correct. Following is the compilation
      error message, where we use <error></error> to signal the position of the error.

  {{ error_message_for_prev_round }}

  Before producing the Lean 4 code to sketch a proof to the given theorem, provide a detailed
      analysis of the error message.



B.8   Decomposer Agent Backtrack Prompt

When decomposition strategies fail repeatedly, the decomposer agent uses this backtrack prompt:

  The previous proof sketch (Round {{ prev_round_num }}) was syntactically valid, but the
      decomposed subgoals could not be proven after multiple attempts. This suggests that the
      decomposition strategy itself may not be the right approach for this theorem.

  Please try a COMPLETELY DIFFERENT decomposition strategy. Consider:
  - A different proof technique (e.g., if the previous attempt used induction, try direct proof,
      contradiction, or case analysis)
  - A different way to break down the problem into subgoals
  - Different intermediate lemmas that might be easier to prove
  - A simpler or more direct path to the conclusion
  - Utilizing, if warranted, the possibly new theorems listed below in pursuit of your goal

  Before producing the new Lean 4 code to sketch a proof, provide:
  1. A brief analysis of why the previous decomposition might have been too difficult
  2. A description of the new strategy you will try
  3. An explanation of how this new approach differs from the previous one

  Note that the theorems listed below may differ from those presented in previous attempts, as a
      new search strategy was used to find potentially useful theorems for this different
      decomposition approach. These theorems may or may not be new compared to previous attempts,
       but they represent theorems identified specifically for trying this alternative strategy.
      Consider how these theorems might be useful in your new decomposition approach.

  {{ theorem_hints_section }}



B.9   Semantic Checker Agent Prompt

The semantic checker agent uses the following prompt to validate formalization accuracy:

  You will receive a math problem consisting of its natural language statement along with its
      formal statement in LEAN 4.

  Please evaluate whether the formal LEAN statement appropriately translates the natural language
       statement based on the following criteria:

  1. Key Elements: The problem's essential components are correctly represented in LEAN code.
  2. Mathematical Accuracy: The translation preserves the accuracy of the mathematical content.


                                                        21
Gödel’s Poetry


  3. Structural Fidelity: The translation aligns closely with the original problem, maintaining
      its structure and purpose.
  4. Comprehensiveness: All assumptions, conditions, and goals present in the natural language
      statement are included in the LEAN translation.

  Your answer should be in the following format:

  Thought: [Your Answer]

  Judgement: [Your Answer, one of {Appropriate, Inappropriate}]

  ---

  Following are the example problems label for the reasonability of their translation.

  # Example 1:

  ## Original natural language statement of the problem:

  For the graph of a certain quadratic y = ax2 + bx + c, the vertex of the parabola is (2, 10), and
      one of the x-intercepts is (1, 0). What is the x-coordinate of the other x-intercept?

  ## Translated formal statement:
  ```lean
  theorem quadratic_other_intercept
      (f : R → R)
      (a b c : R)
      (h_quad : ∀ x, f x = a * x^2 + b * x + c)
      (h_vertex : f 2 = 10 ∧ ∀ x, f x ≤ f 2) -- vertex at (2,10)
      (h_intercept1 : f 1 = 0) : -- x-intercept at (1,0)
      f 3 = 0 := by -- other x-intercept at (3,0)
  ```

  Thought: The Lean translation of the problem is appropriate because it accurately captures the
      intent and reasoning of the original problem. The problem's key elements, such as the
      vertex, axis of symmetry, and x-intercepts of the quadratic function, are correctly
      translated into Lean code. The logical flow of the proof mirrors the original reasoning,
      starting with the symmetry property of the quadratic function and using it to determine the
       second x-intercept. The mathematical accuracy is preserved, as the proof correctly applies
       the vertex property and symmetry to arrive at the solution. Furthermore, the translation
      aligns well with the original problem in natural language, maintaining fidelity to its
      structure and purpose. Overall, the translation is both faithful and complete, making it an
       appropriate representation of the original problem.

  Judgement: Appropriate

  # Example 2:

  ## Original natural language statement of the problem:

  Draw a tangent line from the point (4, 3) to the circle (x − 2)2 + (y − 1)2 = 1. What is the
      equation of the line that passes through the two tangent points?

  ## Translated formal statement:
  ```lean
  theorem tangent_line_equation (x y : R) :
    let P : R × R := (4, 3) -- Point P
    let C : R × R := (2, 1) -- Center of first circle
    let r : R := 1 -- Radius of first circle


                                                   22
Gödel’s Poetry


    -- Points (x,y) satisfying both circle equations
    let on_first_circle := (x - 2)^2 + (y - 1)^2 = 1
    let on_second_circle := (x - 3)^2 + (y - 2)^2 = 2
    -- If point is on both circles
    on_first_circle ∧ on_second_circle →
    -- Then it lies on the line 2x + 2y - 7 = 0
    2*x + 2*y - 7 = 0 := by
  ```

  Thought: The Lean translation of the problem is inappropriate because it fundamentally changes
      the intent of the original problem. The original problem asks to derive the equation of the
       tangent line passing through the intersection points of two circles, but the translation
      assumes the equation (2x + 2y - 7 = 0) is already given and instead asks to prove that the
      intersection points lie on this line. This shifts the problem from a construction task to a
       verification task, losing the original problem's focus on deriving the result through
      geometric and algebraic reasoning. Additionally, the translation omits the key reasoning
      step of subtracting the circle equations to derive the line equation, which is central to
      the original problem. As a result, the translation fails to accurately represent the
      problem's intent and educational value, making it an incomplete and inappropriate
      representation.

  Judgement: Inappropriate


  Example3:

  ## Original natural language statement of the problem:

  If a, b, c, d > 0 and abcd = 1 , prove that

     1         1         1         1       1     1     1     1
  a+b+c+1
          + b+c+d+1 + c+d+a+1 + d+a+b+1 ≤ a+3 + b+3 + c+3 + d+3

  ## Translated formal statement:
  ```lean4
  theorem lean_workbook_49553 (a b c d : R) (habc : a * b * c * d = 1) : (1 / (a + b + c + 1) + 1
       / (b + c + d + 1) + 1 / (c + d + a + 1) + 1 / (d + a + b + 1)) ≤ (1 / (a + 3) + 1 / (b +
      3) + 1 / (c + 3) + 1 / (d + 3)) := by sorry
  ```

  Thought: The Lean translation of the problem is inappropriate because the condition a, b, c, d > 0
      is ignored in the formal statement.

  Judgement: Inappropriate



  Example4:

  ## Original natural language statement of the problem:

                               (a−1)2
  If a = b = c = 2 so                   = 21 . We'll prove that 12 is the answer.
                        P
                         cyc    a2 +2


  ## Translated formal statement:
  ```lean4
  theorem lean_workbook_plus_1478 (a b c : R) (ha : a = 2) (hb : b = 2) (hc : c = 2) : (a - 1) ^
      2 / (a ^ 2 + 2) + (b - 1) ^ 2 / (b ^ 2 + 2) + (c - 1) ^ 2 / (c ^ 2 + 2) = 1 / 2 := by sorry
  ```




                                                          23
Gödel’s Poetry


  Thought: The Lean translation of the problem is appropriate because it accurately captures the
      assumptions and the goal in the natural language statement.

  Judgement: Appropriate

  ## Original natural language statement of the problem:

  {{ informal_statement }}

  ## Translated formal statement:
  ```lean4
  {{ formal_statement }}
  ```




                                                24
