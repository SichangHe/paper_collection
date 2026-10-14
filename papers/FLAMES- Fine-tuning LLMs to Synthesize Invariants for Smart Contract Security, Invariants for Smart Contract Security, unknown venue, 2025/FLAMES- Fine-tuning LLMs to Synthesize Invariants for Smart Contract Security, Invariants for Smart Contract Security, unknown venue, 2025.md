                                                      F LAMES: Fine-tuning LLMs to Synthesize
                                                         Invariants for Smart Contract Security
                                                  Mojtaba Eshghie 1 , Gabriele Morello2 , Matteo Lauretano2 , Alexandre Bartel1 , Martin Monperrus2
                                                                                             1
                                                                                                 Umeå University, Umeå, Sweden

                                                                                2
                                                                                    KTH Royal Institute of Technology, Stockholm, Sweden



                                            Abstract—Smart contract vulnerabilities cost billions of dollars
arXiv:2510.21401v1 [cs.CR] 24 Oct 2025




                                                                                                                                   DISL Dataset       Contract       Evaluation               Results
                                         annually, yet existing automated analysis tools fail to generate
                                         deployable defenses. We present FLAMES, a novel automated                                                                Compilability of           4835/5000
                                                                                                                                                                  hardended contracts        compilable
                                         approach that synthesizes executable runtime guards as Solidity                                     AST Creation
                                                                                                                                                                  via invariants




                                                                                                                   Code Analysis
                                         require statements to harden smart contracts against exploits.
                                                                                                                                       Method Identification
                                         Unlike prior work that relies on vulnerability labels, symbolic                                                          Semantic similarity
                                                                                                                                                                  to human-written           2226/5000
                                         analysis, or natural language specifications, FLAMES employs                                  Context Abstraction                                   equivalent
                                                                                                                                                                  invariants
                                         domain-adapted large language models trained through fill-in-
                                         the-middle supervised fine-tuning on real-world invariants ex-                                   Token Infilling
                                                                                                                                                                  Exploit reverting            22/108
                                         tracted from 514,506 verified contracts. Our extensive evaluation                                                        capability of invariant-    exploits
                                         across three dimensions demonstrates FLAMES’s effectiveness:                              Fine-Tuning        Inference   based hardening             reverted
                                         (1) Compilation: FLAMES achieves 96.7% compilability for
                                         synthesized invariant (2) Semantic Quality: on a curated test             Fig. 1: F LAMES architecture, evaluation, and results overview.
                                         set of 5,000 challenging invariants, FLAMES produces exact
                                         or semantically equivalent matches to ground truth in 44.5%
                                         of cases; (3) Exploit Mitigation: FLAMES prevents 22 out of               mining from on-chain transaction traces can surface likely
                                         108 real exploits (20.4%) while preserving contract functionality,        properties [9], but are noisy and miss important security
                                         and (4) FLAMES successfully blocks the real-world APEMAGA                 aspects [8].
                                         incident by synthesizing a pre-condition that mitigates the
                                         attack. FLAMES establishes that domain-adapted LLMs can
                                                                                                                      Our core insight is to use Large Language Models (LLM)
                                         automatically generate production-ready security defenses for             to synthesize invariants. Yet, off-the-shelf code LLMs are not
                                         smart contracts without requiring vulnerability detection, formal         good at handling Solidity smart contracts without domain
                                         specifications, or human intervention. We release our code,               adaptation [10]–[12]. We propose F LAMES1 , a novel training
                                         model weights, datasets, and evaluation infrastructure to enable          and inference pipeline to synthesize high-quality invariants
                                         reproducible research in this critical domain.
                                            Index Terms—Smart Contracts, Invariant Synthesis, Program
                                                                                                                   as Solidity pre-/post-conditions. F LAMES (i) analyzes the
                                         Hardening, Large Language Models, Blockchain Security                     contract to extract a contract context to be given as input
                                                                                                                   to the LLM; (ii) F LAMES uses fill-in-the-middle supervised
                                                                 I. I NTRODUCTION                                  fine-tuning (SFT) over real-world require(<invariant>) state-
                                            Smart contracts underpin blockchain applications for man-              ments to train the model to reconstruct missing invariants;
                                         aging digital assets. Despite the progress in automated smart             and (iii) at inference, F LAMES synthesizes require invariant
                                         contract analysis, billions of dollars are lost every year due            statements at function entry (pre-conditions) and exit (post-
                                         to exploits abusing smart contract vulnerabilities [1], [2].              conditions) locations. Crucially, F LAMES does not require vul-
                                         Most smart contract vulnerability detectors produce unreliable            nerability labels, vulnerability detectors, or natural-language
                                         verdicts and do not generate deployable defenses [3]–[5]. As              description, it does fully automated invariant synthesis for
                                         a result, there is strong demand for practical techniques to              contract hardening.
                                         generate concrete security mitigations.                                      Prior work have mined invariants from transaction traces [8],
                                            A promising solution is invariant-based defense: pre-/post-            [9], used symbolic analysis to infer invariants [13], or
                                         conditions that revert dangerous executions at runtime [6].               prompted LLMs with vulnerability labels to propose invari-
                                         This is implemented in the widely used require statement in               ants [14]–[16]. In contrast, F LAMES generates concrete exe-
                                         the Solidity language for smart contracts [7]. Recent work                cutable invariants as Solidity require statements; with no need
                                         further confirms that attacks are preventable by invariants [8].          for specifications or vulnerability labels or hints.
                                         However, automatically obtaining useful invariants for real                  Three research questions guide our extensive experimental
                                         contracts is a hard open research problem. Dynamic invariant              evaluations:
                                           Emails:             {mojtabae,           alexandre.bartel}@cs.umu.se;
                                         gabriele.morello.123@gmail.com, matteola@kth.se, monperrus@kth.se.               1 https://github.com/ASSERT-KTH/FLAMES
• RQ1 (Compilation). What percentage of invariants synthe-
                                                                                       DISL-20k sample         DISL-100k sample
  sized by F LAMES compile when injected into real contracts?
  Answer: up to 96.7% synthesized invariants compile (vs.
                                                                                                     Code Analysis
  62.6% for the non–domain-adapted baseline).
                                                                                            Infilled contracts batch size 32
• RQ2 (Semantic Quality). How close are the synthesized
  invariants to human-written ones? Answer: on a 5k hard-                              Base   Model's      LoRA Trainable V K
  invariant set, F LAMES attains 44.5% exact-or-equivalent                               Weights              Adapters       Q O
  matches to ground truth (vs. 23.5% baseline).




                                                                                      Optimizer
                                                                                                  AdamW            LR: 3 × 10-4
• RQ3 (Exploit Mitigation). To what extent do injected in-
                                                                                              Grad Clipping        Weight Decay
  variants prevent exploits while preserving functionality? An-
  swer: the best configuration prevents 22/108 exploits with-
  out negatively affecting contract’s functionality (vs 16/108
  baseline).                                                                            Flames-20k               Flames-100k
• RQ4 (Real Incident Hardening). How effective is F LAMES
  at synthesizing a deployable invariant in blocking a suc- Fig. 2: The supervised fine-tuning pipeline yields to F LAMES
  cessful attack? Answer: In a reproduction of the real-world models, specialized for Solidity.
  APEMAGA incident, F LAMES-100k synthesizes a pre-condition
                                                                    1 function batchTransfer ( address [] _rec , uint256 _value )
  semantically equivalent to the ground-truth patch, reverting              public whenNotPaused returns ( bool ) {
  the attack transaction.                                           2 require( rec.length == 0|| value <= type(uint256).max/ rec.length);
                                                                    3 uint cnt = _rec . length ;
   To sum up, our contributions are:                                4 uint256 amount = uint256 ( cnt ) * _value ;
                                                                    5 require ( cnt > 0 && cnt <= 20) ;
• We introduce F LAMES , a novel pipeline for invariant- 6 require ( _value > 0 && balances [ msg . sender ] >= amount );
   based smart contract hardening, based on LLM fine-tuning. 7 balances [ msg . sender ] = balances [ msg . sender ]. sub ( amount );
                                                                    8 for ( uint i = 0; i < cnt ; i ++) {
   F LAMES generates valuable pre-/post-conditions using only 9            balances [ _rec [ i ]] = balances [ _rec [ i ]]. add ( _value );
   source code as input.                                           10      Transfer ( msg . sender , _rec [ i ] , _value ) ;
                                                                   11 }
• We curate D ISL , a dataset of 514 506 unique, verified 12 return true ;
   Solidity files and a 5k D ISL -H ARD I NV test set for rigorous 13 }
   evaluation.                                                        Fig. 3: Preventing the BeautyChain attack with a pre-condition
• We deliver a comprehensive evaluation demonstrating the
                                                                      invariant.
   high compilability, semantic quality , and exploit mitigation
   effectiveness of F LAMES invariants.                               require statetement is evaluated as false, transaction execution
                                           2
• We release our code, model weights , and evaluation har-            reverts, preventing any state changes with guarantees.
   nesses for reproducibility and future research in this area.          In April 2018, the BeautyChain contract suffered a attack
   Section II describes the design of F LAMES, Section III ex- abusing an overflow vulnerability in its code [17]. As Figure 3
pands the details of the collection, deduplication, and contents shows, BeautyChain implemented a batchTransfer that com-
of our D ISL dataset, Section IV describes the experimental puted amount = _value * _rec.length before any overflow
protocol to answer RQ1–RQ4, Section V provide our results to check. The attacker exploited this publicly callable vulnerable
the RQs, Section VII provides an account of the most relevant function by sending a transaction with a very large _value
scientific papers, Section VI discusses the threats to validity, resulting in an overflow and wrap around letting attackers
and Section VIII concludes the paper.                                 mint gigantic balances. The one-line pre-condition invariant
                                                                      in Section II-A would have blocked the attack transaction.
                     II. F LAMES A RCHITECTURE
                                                                      Invariants at the right point can stop exploits mid-flight.
   We propose F LAMES, a novel smart contract hardening                  Figure 1 shows our proposed solution, called F LAMES.
pipeline via specialized LLMs. F LAMES follows a multi- It follows a three-stage pipeline to harden smart contracts
stage process: a code analysis stage (Section II-B), a one-time without any prior vulnerability information: (i) code analysis
supervised fine-tuning stage (Section II-C), and an inference (§II-B), (ii) supervised fine-tuning (§II-C), and (iii) invariant
stage (Section II-D) to synthesize missing invariants in smart synthesis (§II-D). Given a contract, the code-analysis stage
contracts.                                                            parses the source into an AST, determines the invariant syn-
A. Overview                                                           thesis location, builds a compact version of the contract and
                                                                      then, the extracted data is used to fine-tune the LLM or to
   The core idea of F LAMES is to inject invariants to harden
                                                                      synthesize the invariants.
smart contracts. Invariants are boolean conditions that must
                                                                         Fine-tuning. During the fine-tuning stage, we mine real-
hold at specific program points, such as pre-conditions at func-
                                                                      world invariants of the form of require(...) statements and
tion entry and post-conditions at function exit. In Solidity, they
                                                                      conduct supervised fine-tuning to obtain a model specialized
are written with require(<invariant>) statements. When a
                                                                      for generating smart-contract invariants.
  2 https://huggingface.co/ASSERT-KTH/FLAMES-100k-2406                   Inference. At inference time (Figure 4), a user specifies one
 pragma solidity ^0.8.0;                                                 Abstract Syntax Tree (AST). The AST representation helps
 contract MinimalERC20 {                                                 manipulate the code programmatically [18].
      mapping(address => uint) public balanceOf;
                                                                            A key challenge with using LLMs both during the fine-
     uint public totalSupply;
     event Transfer(address indexed from, address to, uint value);       tuning and inference stage is their limited context window.
      constructor(uint initialSupply) {                                  Indeed, many real-world smart-contracts do not fit into this
        totalSupply = initialSupply;
                                                                         context, which is a blocker for both fine-tuning and inference.
         balanceOf[msg.sender] = initialSupply;
     }                                                                   As the token length distribution of the sources in D ISL in
      function transfer(address rec, uint amt) public returns (bool) {   Figure 5 shows, more than 31% of the dataset overflows
        uint senderBalance = balanceOf[msg.sender];
                                                                         4096 which is the maximum token length of many base
         balanceOf[msg.sender] = senderBalance - amt;
         balanceOf[rec] += amt;
                                                                         LLM models. This is a major problem for both training and
         emit Transfer(sender, recipient, amount);                       inference This token length typically represents ≈300 lines of
         return true;                                                    code for Solidity smart contracts. To handle contracts more
 }}
                                                                         than 4096 tokens, we employ a context abstraction technique
                                     AST Creation                        adapted from prior work [19]. It consists of only keeping the
                                                                         most important parts of the code relevant to the task at hand.
                            Method Identification                        F LAMES abstracts the smart contract as follows: 1) it retains
                                                                         the full body of the function containing the current invariant
                            Context Abstraction                          (to be learned or to be synthesized at training and inference
pragma solidity ^0.8.0;                                                  time respectively); 2) it retains all function definitions that
contract MinimalERC20 {                                                  call the target function, 3) it keeps modifier definitions applied
  mapping(address => uint) public balanceOf;
                                                                         on the mentioned functions 4) it only keeps signature of the
  uint public totalSupply;
  constructor(uint initialSupply);
                                                                         other functions. 5) it keeps state variable declarations, and 6)
  function transfer(address rec, uint amt) public returns (bool) {       it removes event definition. All this is done precisely based
    uint senderBalance = balanceOf[msg.sender];                          on AST manipulation.
         balanceOf[msg.sender] = senderBalance - amt;
         balanceOf[rec] += amt; return true;
                                                                            Analysis at training time. F LAMES conducts contract anal-
}}                                                                       ysis to prepare the code for the fine-tuning pipeline. It first
                                                                         extracts the require statements to be fine-tuned on. Given the
                                  Token Infilling
                                                                         require statements, it determines their enclosing function and
  function transfer(address rec, uint amt) public returns (bool) {
                                                                         prepares the abstract contract context based on the identified
 1 require(<FILL_ME>);
         uint senderBalance = balanceOf[msg.sender];                     function. The rest of the procedure is described in subsec-
         require(<FILL_ME>);                                             tion II-C.
         balanceOf[msg.sender] = senderBalance - amt;
                                                                            Analysis at inference time. Figure 4 shows an instance
         balanceOf[rec] += amt;
 2 require(<FILL_ME>);
                                                                         of this code analysis abstraction during the inference stage.
         return true;                                                    F LAMES only keeps the state variable declarations balancedOf
     }                                                                   and totalSupply, preserves the signature of the constructor,
                                                                         and the full definition of the transfer function which is target
                                    Inference
                                                                         of invariant synthesis.
     function transfer(address rec, uint amt) public returns (bool) {
         require(rec != address(0));                                     C. Supervised Fine-Tuning Stage
         uint senderBalance = balanceOf[msg.sender];
         require(<FILL_ME>);                                                F LAMES specializes a base LLM for invariant generation
         balanceOf[msg.sender] = senderBalance - amt;                    via supervised fine-tuning. Each training sample is built from
         balanceOf[rec] += amt;
         require(balanceOf[rec] >= amt);
                                                                         a real require(<invariant>) taken from the training dataset
         return true;                                                    (see §IV-A). The training sample is generated as follows (i)
     }                                                                   we use the abstract context of the contract (§II-B); (ii) we
                                                                         replace the invariant with the placeholder token <FILL_ME> and
Fig. 4: F LAMES synthesis stage illustrated with an example.
                                                                         keep the surrounding code intact. This is the fill-in-the-middle
or more synthesis locations and asks the model to generates              (FIM) training objective [20]. Each invariant inside a require
the missing invariant(s). The synthesized invariants are then            statement in the training dataset is meant to be recreated at
injected into the full source in order to permanently harden             the FIM location, based and the surrounding contract.
the contract.                                                            D. Invariant Synthesis Stage
                                                                           During the inference stage (Figure 4), a user provides
B. Code Analysis Stage
                                                                         a full smart contract and specifies a target function for
   In F LAMES, the same code analysis is applied at training             smart-contract synthesis. F LAMES extracts this function, then
time, to prepare the data, and at inference time, to synthesize          prepares the abstracted version of the contract keeping the
new invariants. F LAMES first parses the smart contract into an          identified function with its full implementation. It then infills
                                                                                    TABLE I: Training parameters of supervised fine-tuning for
                               1.0
                                                                                    F LAMES

         Cumulative fraction
                               0.8              >4096: 31.3%                                                         Hardware and Runtime

                               0.6                                                      Train GPUs         4× Nvidia A100 (80 GB each)
                                                                                        Precision          4-bit quantized load (nf4) with mixed precision (fp16) for training
                               0.4
                                                                                        Optimizer          AdamW
                                                                                        Batch size         32 (per-device batch: 2; gradient accumulation: 16)
                                                                                        Epochs             1 (for both F LAMES-20k and F LAMES-100k)
                               0.2
                                                                                        Learning rate      3 × 10−4
                                                                       Decomposed
                               0.0                                                                              Model and PEFT Configuration
                                     0   2000 4000 6000 8000 10000120001400016000       Base model         CodeLlama2-7B
                                                    Tokenized length                    LoRA               rank r=8, α=16; injected in attention Q/V projections
                                                                                        Context length     4096 tokens
                                                                                        Infilling mode     Fill-in-the-Middle (FIM) with <FILL ME>
Fig. 5: Cumulative distribution of the token length of D ISL
contracts.                                                                                               III. DISL: F INE -T UNING DATASET
the function by require(<FILL_ME>) statement at the desired                            A major challenge in applying machine learning to smart
invariant locations, one location to be inferred at a time. The                     contract security is the lack of unique large datasets of real-
F LAMES model then generates the boolean predicate to fill                          world contracts. Recent studies indicate that synthetic, small,
the mask. Finally, F LAMES replaces the placeholder with the                        or non-diverse datasets are not satisfactory [3], [24].
synthesized invariant and reconstructs the full, hardened smart                        To address this gap, we create D ISL, the largest dataset of
contract code. Then, it compiles and returns the hardened                           unique Solidity smart contracts that serves as the foundation
contract to the user.                                                               for training and evaluating F LAMES. D ISL is designed to be
   1) Invariant Synthesis Locations: F LAMES considers two                          diverse, recent, and suitable for AI tasks. It focuses exclusively
places for synthesis, where invariants can revert harmful                           on real-world contract with verified source code.
transactions: pre-condition (function entry point) and post-                        A. Data Collection
condition (function exit point), F LAMES supports synthesizing
                                                                                        To ensure clarity, we define the following terms:
invariants at the mentioned locations.
                                                                                    •  Deployed contract: A smart contract address on the
   2) Inference Strategies: Single-turn: When injecting multi-
                                                                                       Ethereum mainnet associated with executable bytecode.
ple invariants in the contract, on can prompt the model each
                                                                                    • Raw contract: The complete, concatenated source code re-
time with the original version of the contract.
                                                                                       trieved from Etherscan for a single deployed contract, which
   Multi-turn: When generating multiple invariants (e.g., pre-
                                                                                       may include multiple files.
and post-condition in the same contract or function), syn-
                                                                                    • Solidity file: A single “.sol” source file, which may itself
thesized invariants are kept in the context for subsequent
                                                                                       contain multiple contract or library definitions.
generations. In other words, if the synthesis task consists
of generating multiple pre-/post-conditation, the model will                            Our collection process was executed in two phases:
be prompted multiple times, and at each turn, it is given                                  a) Initial Seeding and Expansion: We began with the
the contract containing the newly synthesized invariants from                       Storhaug et al.’s dataset [25], [26], which contains 2 217 692
previous turns [21], [22].                                                          raw contract records up to April 1, 2022. To capture more
                                                                                    recent contracts, we queried the Google BigQuery Ethereum
                                                                                    database for all contracts deployed between April 1, 2022,
E. Implementation
                                                                                    and January 15, 2024, that had at least one on-chain transac-
   We implement our fine-tuning stage using the Parameter-                          tion [27]. This query yields 2 709 030 contract addresses.
Efficient Fine-Tuning (PEFT) library of Huggingface [23]. We                               b) Source Code Retrieval: Using the Etherscan API, we
use C ODE L LAMA 2-7B as base model, in 4-bit quantization.                         fetched the verified source code for these addresses. A contract
We employ the QLoRA technique and LoRA adapters for                                 is “verified” if its uploaded source compiles to the exact byte-
fine-tuning. This parameter-efficient fine tuning (i) reduces the                   code on the blockchain, ensuring authenticity. After filtering
training memory footprint enabling us to use larger training                        out unverified contracts, this step yielded 1 080 579 new raw
corpora on commodity multi-GPU machines; (ii) constrains                            contract records. Merging these with the seed dataset resulted
parameter updates to a low-rank subspace while preserving                           in a total raw collection of 3 298 271 deployed contracts.
the base model’s capabilities. We use AdamW optimizer with                              After this curation, we obtain the final, unique D ISL dataset.
a learning rate of 3 × 10−4 and a batch size of 32 (with two                        D ISL consists of two collections: i) decomposed set containing
batches per device), and gradient clipping for stability. Table I                   12 931 943 Solidity files which is the result of splitting each
details the system setup for the fine-tuning stage. The training                    raw contract record into its individual Solidity files. This pro-
runs for one epoch on the selected subset of the D ISL dataset                      cess expanded our collection to a total of 12 931 943 Solidity
(see §IV). We fine-tune two versions of F LAMES, one with                           files. and ii) the decomposed and duduplicated (unique) set
20 000 samples (F LAMES-20k), another with 100 000 samples                          consisting of 514 506 Solidity files: to eliminate redundant
(F LAMES-100k).                                                                     code, we used the Jaccard similarity index with a 90%
TABLE II: The other smart contract datasets. D ISL is founda-      not picked from the fine-tuning corpus. We publish D ISL -
tional for future learning-based approaches on smart contracts.    H ARD I NV on our repository3 .
  Dataset                                Year             Size        3) Benchmark for RQ3: To evaluate real-world effective-
  Storhaug (deduplicated) [25]           2022         186 397      ness, we use 108 vulnerable contracts from the SB-Heist
  Fiesta1 (deduplicated) [29]            2023         149 386      benchmark [35], which are written in Solidity and come with
  Sanctuary [30]                         2022         144 857      ground-truth exploits. We chose this benchmark since it pro-
  SmartBugs-Wild [31], [32]              2020          47 587
  Ren et al. [24], [33]                  2021          46 186
                                                                   vides read-to-use proof-of-concept exploits and functionality
  DAppSCAN [34]                          2023          39 904      tests that would capture if hardening has changed the nominal
  D ISL (decomposed)                                12 931 943
                                                                   behavior of the contract.
  D ISL (decomposed & deduplicated)                    514 506
                                                                   B. Protocol for RQ1
 1. Uses exact match for deduplication
                                                                      We evaluate the compilability of the synthesized invariants
threshold to compare the sets of tokens in each file [28].         on D ISL -H ARD I NV dataset (see §IV-A). Then, we replace all
This way, we identify and remove near-duplicates and preserve      invariants in D ISL -H ARD I NV with <FILL_ME> token, and infer
unique implementations. This step was critical as it revealed      the missing invariant. We use C ODE L LAMA (as baseline),
that over 96% of the decomposed files were duplicates.             F LAMES-20k, and F LAMES-100k to recreate the invariant.
   Each entry of D ISL is enriched with valuable metadata (see     We then compile the contract, using its original compiler
repository), which is crucial for tasks requiring compilation      configuration. To prevent data leakage, these contracts are
and metadata analysis, as we do in F LAMES. As Table II            distinct from the fine-tuning dataset presented in Section IV-A.
shows, D ISL is the largest Solidity smart contract dataset           We report the number of successful compilations for each
to date based on number of files, recency, uniqueness, and         model. A build succeeds if, under the contract’s original
diversity.                                                         compiler configuration (pragma/version), solc compiler exits
   Our analysis shows the deduplicated subset of D ISL con-        without errors and produces artifacts. A high compilation
tains 5 276 315 require statements. We use these require           success post-hardening indicates that the model’s synthesized
statements for both the supervised fine-tuning and evaluation      predicates are syntactically valid and are consistent with
of F LAMES (RQ1 and RQ2), with seggegration to avoid data          the surrounding context from a typing, naming and scoping
leakage.                                                           perspective. A high compilation rate is a necessary condition
                                                                   for deployable hardening but not a guarantee of semantic
                 IV. E XPERIMENTAL E VALUATION
                                                                   correctness or security: those are evaluated separately in RQ2
   We design a comprehensive set of experiments to evaluate        (semantic relation to human invariants) and RQ3 (exploit
F LAMES, addressing the following research questions:              prevention).
• RQ1 Compilation: To what extent do invariants synthesized
  by F LAMES real smart contracts compile when injected back       C. Protocol for RQ2
  in the code?                                                        To assess how well the generated invariants match the
• RQ2 Semantic Quality: How semantically close are the             human-written ones, we use the D ISL -H ARD I NV dataset (see
  F LAMES invariants compared to human-written ones?               §IV-A). For each sample, we prompt the models to generate
• RQ3 Mitigation: To what extent do F LAMES invariants             the missing invariant. We then compare the synthesized in-
  prevent exploits while preserving functionality?                 variant with the ground-truth using S INDI [36], a semantic
• RQ4 (Real Incident Hardening). How effective is F LAMES          equivalence checker tool for Solidity. S INDI uses a combi-
  at synthesizing a deployable invariant to block a real-world     nation of SMT-solving and rewrite rules to determine the
  incident?                                                        semantic relationship of two given invariants. Using S INDI,
   This section details the datasets (Section IV-A) and the        we classify the relationship of the invariant and its ground
experimental protocols for RQ1–RQ3 (Sections IV-B to IV-D).        truth into five categories: exact match, semantically equiva-
                                                                   lent, synthesized or ground truth stronger, inconclusive. For
A. Datasets Used for Experiments
                                                                   each ⟨synthesized, ground truth⟩ pair, we assign one of five
   1) Fine Tuning Datasets: We train F LAMES-20k and               verdicts.
F LAMES-100k on 20 000 and 100 000 samples, respectively,          Exact Match. We first compare the invariants in textual form
from the D ISL deduplicated set. Each sample is a full contract    after stripping whitespaces. If they are equal, they are classified
file from D ISL with one of its invariants randomly selected for   as an exact match, otherwise, we move to using S INDI for the
the supervised fine-tuning stage.                                  semantic comparison.
   2) Benchmark for RQ1 & RQ2: To rigorously code genera-          Semantically equivalent. S INDI proves semantic equivalence
tion quality, we create a challenging test set by filtering DISL   through mutual logical implication (when syn: synthesized
and selecting 5000 unique, non-trivial invariants. We do so        invariant and gt: ground truth then syn ⇒ gt and gt ⇒ syn):
by removing the ones that contain only variable identifiers,       __msgSender() == owner ≡ msg.sender == owner.
simple comparisons, negations, straightforward function calls,
or hardcoded addresses. To prevent data leakage, they are            3 https://github.com/ASSERT-KTH/FLAMES/tree/master/Disl-hardinv
Synthesized / ground truth stronger. S INDI proves syn ⇒ gt
                                                                              CodeLlama                   3130 (62.6%)
but not the inverse; this means one of the invariants accepts a
smaller set of states:                                                       FLAMES-20k                    3348 (67.0%)
paidCount * mintPrice == msg.value         ⇒      msg.value >=
paidCount * mintPrice.                                                      FLAMES-100k                             4835 (96.7%)
Inconclusive. Neither implication is provable within S INDI’s
logic or given the solver time budget, or the invariants are over     Fig. 6: RQ1: Compilation success rate of synthesized invari-
unrelated variables so that no implication holds:                     ants for different models.
IERC20(token).balanceOf(msg.sender)>= amount                  vs.
whitelist[msg.sender].
                                                                        We use F LAMES to synthesize the invariant and put it
D. Protocol for RQ3                                                   back in the contract. We compile the hardened contract. After
   We use a dataset of vulnerable smart contracts and their           hardening, we evaluate the hardening effectiveness by running
exploit to measure security effectiveness of the synthesized          the exploit PoC on the hardened version with the real state
invariants [5], [37]. Each one of the 108 contracts in this           of the blockchain pre-incident. To do this, we fork Ethereum
benchmark contains one or more vulnerabilities in one or more         mainnet at block prior the attack transaction, replace the
lines in the source code.                                             token’s runtime at the APEMAGA address, preserving its storage.
   For each of these vulnerability locations, we synthesize in-       Then, we run the exploit script to check the effectiveness of
variants with three different injection strategies: pre-condition,    the invariant against the attack.
post-condition, and both pre and post for the same contract.
For each injection strategy and inference strategy (single- and
multi-turn), we synthesize the missing invariants, and inject
them at their determined location.
   For each candidate hardened version, we then execute:
1) The contract’s functional tests to check if the invariant                          V. E XPERIMENTAL R ESULTS
    introduces any regression.
2) We run the ground-truth exploit on the hardened contract
    to determine whether the F LAMES invariant mitigates the
    exploit.
   If the hardened contract compiles, passes all functional           A. RQ1: Well-formedness of Synthesized Invariants
tests, and successfully stops the exploit, the hardening task
is considered successful.
   We benchmark our models against C ODE L LAMA [38]. We
evaluate C ODE L LAMA and F LAMES using the exact same                   We measure whether the F LAMES synthesized invariants are
harness. This gives an insight about F LAMES’s performance            correct per the syntactic and semantic checks of the compiler.
against a non–domain-adapted model on the hardening task.             Figure 6 shows the compilability results of 5000 synthesized
The Python notebooks used in our experiments are publicly             invariants for the D ISL -H ARD I NV dataset. The bars show
available4 .                                                          from top to bottom number of contracts compiled without any
                                                                      modification, the number of them compiled after a random
E. Protocol for RQ4                                                   require statement is replaced by its synthesized version, and
   In this RQ, we check whether F LAMES is able to prevent a          the two bottom bars pertain to F LAMES models.
real-world smart contract incident. We choose an attack based
                                                                         As Figure 6 shows, our best model F LAMES-100k, gen-
on two criteria: i) the concrete exploit proof-of-concept is
                                                                      erates require statements that compile at least 4835/5000
available to reproduce the incident ii) it is in nature preventable
                                                                      of the times with showing significant improvement over
using an invariant. After careful review of multiple incidents,
                                                                      both the baseline and the less fine-tuned variant (F LAMES-
we select the APEMAGA protocol incident that happened in June,
                                                                      20k). C ODE L LAMA performs poorly with 3130/5000 compiled
2024 leading to a ∼9.4 ETH loss. The manual review of
                                                                      cases post-hardening, demonstrating the effectiveness of the
the public attack transaction5 and the exploit reproduction
                                                                      training loop.
script 6 reveals the flow of the attack, and the function(s)
where the synthesis of a precise invariant would deter the               Figure 7a presents one failed synthesis result where
attack transaction. The patch of the attack is also published         C ODE L LAMA continues to generate a function declaration
and gives us the location of the missing invariant.                   within another function body leading to a parser error dur-
  4 https://github.com/ASSERT-KTH/FLAMES/blob/master/
                                                                      ing compilation. C ODE L LAMA is not able to output a stop
raw-validation-results/sb-heists/
                                                                      token appropriately. Compared to C ODE L LAMA, F LAMES-
  5 APEMAGA attack transaction.                                       100k does not generate such multi-line generation errors due
  6 DeFiHackLabs Exploit PoC.                                         to incorrect end of generation.
 1 contract Vault {                                                                   3500
 2 mapping ( address = > uint256 ) public balances ; // ...                                                                                  CodeLlama
 3 function withdraw ( uint256 amount ) external {
                                                                                      3000                                                   FLAMES-20k
 4     require(balances[msg.sender] >= amount);                                                                                              FLAMES-100k
 5     function safeSub(uint256 a, uint256 b) internal pure returns
 6         (uint256) { return a - b; }                                                2500
 7     balances [ msg . sender ] -= amount ;
 8     ( bool ok , ) = msg . sender . call { value : amount }( " " ) ;                2000




                                                                              Count
 9     require ( ok ); } // ...
10 }
                                                                                      1500
  (a) Invariant synthesized by C ODE L LAMA failing compilation. After
  infilling the require, C ODE L LAMA appends a function inside the                   1000
  body of another function, making the contract uncompilable (line
  breaks added for clarity).                                                           500

 1 contract Vault {                                                                      0
                                                                                                   ve             tch     ally         zed          uth
                                                                                               lusi           t Ma antiicvalent nthesrionger und Trronger
 2 mapping ( address = > uint256 ) public balances ; // ...
                                                                                             nc             c
                                                                                        Inco               a
 3 function withdraw ( uint256 amount ) external {
 4     require(amount <= balances[msg.sender]);                                                         Ex         SemEqu Sy St Gro St
 5     // same as (a)
 6}                                                                           Fig. 8: Semantic Similarity of F LAMES invariants .
  (b) F LAMES returns a single well-formed compilable invariant at
  the mask location.                                                        The number of cases where the invariants are
                                                                         stronger/weaker are balanced for the two categories for
 Fig. 7: Synthesized invariants (a) failure by C ODE L LAMA; (b)
                                                                         all models (e.g., out of 446 such cases for F LAMES-100k, in
 success by F LAMES (compiles).
                                                                         209 cases the synthesized invariants are stronger and 237 vice
                                                                         versa). Table III presents five synthesized invariants (right)
                  RQ1 Answer: Compilability                              from each of the four semantic categories and their ground
  Invariants synthesized by F LAMES compile in 96.7 of cases,            truth (left).
  versus 62.6% for the baseline. This indicates that domain-                Equivalent Invariants. Equivalences arise from alge-
  specific fine-tuning with F LAMES yields invariants that are           braic normalization, commutativity, and popular library alias
  of much higher usability. Fine-tuning enables the model                substitutions. In Table III, ID 1 swaps sides of equality
  to capture the syntactic (e.g., scoping) and semantic (e.g.,           (_msgSender()== ownerOf(..) ≡ ownerOf(..)== msg.sender)
  typing) constraints of invariants in the considered smart              while also replacing the _msgSender() with the equivalent
  contract language, Solidity.                                           msg.sender. ID 3 replaces a SafeMath idiom a.add(b)>= a
                                                                         with its native form a + b >= a. ID 4 distributes constants
                                                                         and rewrites >= cost * (_mintAmount - 1) as >= (cost *
 B. RQ2: Comparison Against Human-Generated Invariants
                                                                         _mintAmount)- (cost * 1). ID 5 flips both inequalities while
    Next, we compare the 5000 synthesized invariants for D ISL -         preserving the same closed interval. ID 2 shows an aliasing
 H ARD I NV against the original one written by a developer.             pattern (token().transfer vs. _token.transfer) which resolve
 Figure 8 shows our results for the five categories of seman-            to the same callee. As these examples show, supervised fine-
 tic relationship between the synthesized invariants and their           tuning helps the model learn semantics-preserving rewrites,
 ground truths for D ISL -H ARD I NV. F LAMES monotonically              yielding invariants that are functionally equivalent.
 improves semantic alignment of synthesized invariants with                 F LAMES Strengthening. Several pairs in Table III
 human-written ones. Moving from the base model to F LAMES               demonstrate semantic strengthening by narrowing admissi-
 trained on 20k and 100k samples monotonically raises exact              ble states. In ID 6, the model tightens a payment invari-
 matches (from 959 to 1328 to 1840). We observe the same                 ant from msg.value>=mintPrice*paidCount to paidCount *
 improvement via fine-tuning when generating invariants that             mintPrice == msg.value, which reverts transactions where
 are textually different but semantically equivalent (from 217           the human-written one would allow. ID 7 removes the
 to 362 to 386).                                                         self-call: msg.sender==ctrl || msg.sender==gov making it
    Fine-tuning also increases the number of cases where the             strictly stronger than the developer’s require(gov || ctrl ||
 invariant does not semantically or textually equal to the ground        address(this)). The stronger one is useful when re-entry be-
 truth but still has a semantic relationship (stronger/weaker bars       tween contract’s own functions is undesired. ID 10 collapses a
 in Figure 8) with its ground truth (157 such cases for C ODE L-         disjunction of “time still within cancel window or already can-
 LAMA to 168 for F LAMES-20k to 446 cases for F LAMES-                   celled” to only a.cancel. Finally, ID 8 illustrates an strength-
 100k). Generating invariants that have semantic relationship            ening via units: multiplying _amount by 1e18 (>= _amount
 with their ground truth counts as partial success as stronger           * 1e18) silently assumes base units and can overconstrain
 synthesized invariants could subsume the allowed behavior of            transfers if _amount is already in wei. Overall, strengthening
 their ground truth and synthesis of multiple weaker invariants          can emerge from equalities replacing inequalities, removing
 (compared to their ground truth) can resolve some security              disjunctive invariants, or hard-coding units. While these may
 issues.                                                                 block attacks, they may also induce false positives if the
     TABLE III: RQ2. Comparison of Ground Truth and Synthesized Invariants, categorized by their logical relationship.
ID Ground Truth                                                                       Synthesized
                                                                  Equivalent
 1     msgSender()==hashesToken.ownerOf( hashesTokenId)                               hashesToken.ownerOf( hashesTokenId)==msg.sender
 2   token().transfer(beneficiary,tokensToUnlock)                                       token.transfer(beneficiary,tokensToUnlock)
 3   balanceOf[ to].add( value)>=balanceOf[ to]                                       balanceOf[ to]+ value>=balanceOf[ to]
 4   msg.value>=(cost*( mintAmount-1))                                                msg.value>=((cost* mintAmount)-(cost*1))
 5   getBlockTimestamp()>= payload.valid from &&                                        payload.valid from<=getBlockTimestamp() &&
     getBlockTimestamp()<= payload.valid to                                            payload.valid to>=getBlockTimestamp()
                                                            Synthesized is stronger
6    msg.value>=mintPrice*paidCount                                                   paidCount*mintPrice==msg.value
7    msg.sender==gov || msg.sender==ctrl || msg.sender==address(this)                 msg.sender==ctrl || msg.sender==gov
8    coinMap[ c].cContract.balanceOf(msg.sender)>= amount                             coinMap[ c].cContract.balanceOf(msg.sender)>= amount*1e18
9    offer.offeredTo==address(0x0)||offer.offeredTo==msg.sender                       offer.offeredTo==msg.sender
10   block.timestamp<a.allocTime+CANCEL PERIOD||a.cancel                              a.cancel
                                                            Synthesized is weaker
11   userMinted[block.number]<Num() && userForFree[tx.origin]<maxFreePerTx              userForFree[tx.origin]<maxFreePerTx
12 isEndStage && enterEndTime>0 && now-enterEndTime>END STAGE DURATION                isEndStage
13 (amount>0) && (GAMintCounter+amount) <= GASupply                                   amount>0
14 block.timestamp>partyTime && hodlers[msg.sender]>0                                 now>=partyTime
15   redisFeeOnBuy+ redisFeeOnSell+ taxFeeOnBuy+ taxFeeOnSell<=25                       redisFeeOnBuy+ redisFeeOnSell +
                                                                                       taxFeeOnBuy+ taxFeeOnSell<=50
                                                                 Inconclusive
16 (from==owner)||(crowdSalesCompleted>0)                                             tokens<=allowed[from][msg.sender]
17   tx.deadline==0 || tx.deadline>block.timestamp                                      tx.to!=address(0)
18   raffle.end==0 || block.timestamp> raffle.end                                       raffle.isClosed
19   maxTransactionAmountBuy>=(totalSupply() / (10**decimals()))/1 000 &&             maxTransactionLimitEnabled
    maxTransactionAmountSell>=(totalSupply() / (10**decimals()))/1 000
20 payable(teamWallet).send(bal*4/10)&&payable(msg.sender).send(bal*2/10) &&          payable(developmentWallet).send(bal)
   payable(developmentWallet).send(bal*4/10)




human-written invariant intentionally permitted the broader                      the fine-tuning data size improves the model to synthesize
state.                                                                           invariants that exactly match with their human-written coun-
   F LAMES Weakening. Weakening typically results from                           terparts ( 1328 in baseline → 1840 F LAMES-100k). The
dropping parts of conjunctive invariants, relaxing thresholds,                   same improvement is observed in generating invariants that
or replacing compound progress conditions with a single flag.                    are semantically equivalent to the human-written ones (217
In ID 11, the model only synthesize the free-mint quota                          → 386).
_userForFree[tx.origin] < maxFreePerTx and omits the per-
block mint cap, admitting transactions the ground truth would                   C. RQ3: Vulnerability Mitigation via Hardening
forbid. ID 13 retains amount > 0 but omits the supply bound,                       We assess exploit mitigation entry (pre), exit (post), and
risking overflow. ID 14 replaces a conjunction over time and                    their combination (pre+post) with two multi-turn and single-
balance with a pure time check; ID 12 reduces a three-part                      turn inference strategies. Table IV shows the results of these
end-stage condition to a bare isEndStage; and ID 15 doubles                     experiments. Here, the colored headers show the exact type
the allowed aggregate fee cap from <= 25 to <= 50. These                        of synthesis (pre, post, or pre+post) on contracts containing a
weakenings preserve compilability but affect security.                          specific type of vulnerability (first column). Recall that no
   Inconclusive IDs 16–20 illustrate predicates over orthog-                    label is given as input to Flames, corresponding to a true
onal state dimensions where neither implication is expected                     hardening technique when one does not know the vulnerability.
(e.g., authorization/timing vs. allowance/limit toggles). For                   The numbers in the inner cells show the cases where the
instance, ID 16 (from == owner || crowdSalesCompleted>0)                        synthesized invariants 1) prevent the vulnerability and 2)
and tokens <= allowed[from][msg.sender] constrain unre-                         pass all functionality tests for the multi-turn inference. For
lated facets (authority/progress vs. approval), and ID 20’s                     conciseness, we only present the total numbers for the single-
human guard enforces a three-way split of bal, while the                        turn strategy at the bottom of the table below the total for the
synthesized check covers only one leg. In such cases, S INDI                    multi-turn strategy.
conservatively reports “inconclusive”. Here, inconclusive may                      Under the multi-turn setting, F LAMES-20k prevents 16/108,
not mean “wrong” as it flags non-comparable properties.                         20/108, and 22/108 exploits for pre, post, and pre+post re-
These cases may require multi-turn prompting or composition                     spectively, while F LAMES-100k prevents 21/108, 22/108, and
when multiple orthogonal properties (e.g., authorization and                    20/108. The non–domain-adapted baseline (C ODE L LAMA -
accounting invariants together) must jointly hold.                              7B) reaches 16/108, 10/108, and 13/108. This means that
              RQ2 Answer: Semantic Quality                                      domain-adapted fine-tuning clearly allows end-to-end exploit
                                                                                mitigation. F LAMES-20k needs multi-turn pre+post to reach
F LAMES increases the semantic quality of synthesized in-
                                                                                its maximum potential and F LAMES-100k attains the same
variants. F LAMES invariants are significantly more semanti-
                                                                                performance with a single post-condition invariant (22/108).
cally accurate than those of the baseline model. Increasing
                                                                                This is significant because it shows that specialization, rather
TABLE IV: Effectiveness of the F LAMES invariants to harden          1 function CashOut ( uint _am ) public payable {
smart contracts and mitigate the actual, reproducible exploit.       2 require( am > 0);
                                                                     3 if ( _am <= balances [ msg . sender ]) {
The numbers represent cases where both the exploit trans-            4     if ( msg . sender . call . value ( _am ) () ) {
action is reverted and the functional tests are successful. The      5       balances [ msg . sender ] -= _am ;
                                                                     6       TransferLog . AddMessage ( msg . sender , _am , " CashOut ");
colored headers represent condition combinations, where a dot        7     }
signifies presence: • pre-condition • post-condition.                8 }
                                                                     9 require(balances[msg.sender] >= MinDeposit);
                            CodeLlama-7B F LAMES-20k   F LAMES-100k 10 }

Vulnerability                •        •   •       •     •        •   Fig. 9: A functionality-preserving synthesized invariant that
                                  •   •       •   •         •    •   fails to deter the exploit.
Access control (16)           4   3   3   5   5   6     7   7    7
Arithmetic (20)               6   1   4   4   7   5     3   7    condition (balances[msg.sender] >= MinDeposit) for the func-
                                                                 6
Bad randomness (8)            0   1   1   2   3   4     1   1    1
                                                                 tion CashOut [39]. The invariants do not affect the normal
Denial of service (4)         1   0   1   1   0   0     2   0    1
Front running (6)             0   0   0   0   0   0     0   0    functionality, yet they are orthogonal to the exploit path as
                                                                 0
Other (2)                     0   0   0   0   0   0     0   0    during reentrancy the state update balances[msg.sender]-=_am
                                                                 0
Reentrancy (26)               1   0   0   1   4   7     7   2    3
                                                                 happens after the external call, so repeated callbacks can ex-
Time manipulation (4)         0   1   0   0   1   0     1   2    2
Unchecked Low Level Call (22) 4   4   4   0   0   0     0   0
                                                                 tract value while the post-condition only constrains to remain
                                                                 0
                                                                 above a threshold after the external call. If the attacker selects
Total of 108 (single-turn)  16 10 12 16 20 17 21 22 21
                                                                 a small-enough _am, the post-condition still holds even though
Total of 108 (multi-turn)   16 10 13 16 20 22 21 22 20
                                                                 multiple value transfers may have already been performed;
                                                                 hence the exploit is not prevented, while ordinary withdrawals
than sheer model size drives exploit mitigation. It also shows are unaffected.
that a post-condition is often the most effective placement in
practice.                                                                   RQ3 Answer: Hardening Effectiveness
   Effectiveness varies by vulnerability class. For access con-    F LAMES generates vulnerability-mitigating invariants with-
trol, F LAMES-100k consistently reaches 7 across all invariant    out any prior knowledge of the vulnerabilities. To our
locations, indicating robustness to whether the guard sits        knowledge, we are the first to show that LLM-synthesized
at entry, exit, or both. Arithmetic benefits most from post       invariants both maintain functionality and mitigate actual
conditions (F LAMES-100k: 7 vs. 3 and 6). Reentrancy shows        end-to-end executable smart contract exploits. F LAMES is
the opposite pattern: pre is strongest for F LAMES-100k (7 vs.    the only technique in the literature to not require any
2 and 3). Time manipulation remains modest but still F LAMES      vulnerability label or hint.
could prevent 2/4 of exploits. For unchecked low-level calls,
entry/exit guards are largely ineffective (all zeros across pre, D. RQ4: Hardening Against a Real-World Attack
post, pre+post for both F LAMES variants). Front running and        The Attack. At its core, the APEMAGA incident was due
the others class remain at zero for all models and placements to a flaw that allowed the attacker to burn all tokens via
which indicates the limitation of purely pre-/post-condition the contract’s publicly callable method family(address). The
based hardening for this vulnerability type.                     vulnerable contract contains an external family function which
   Multi-turn synthesis helps when composing multiple invari- calls to an internal _approve_ method (Figure 10a) that burns
ant placements. For F LAMES-20k, pre+post improves from nearly all of the account’s balance. There is no authorization
17/108 (single-turn) to 22/108 (multi-turn), indicating that implemented in the family function.
carrying earlier guards into the next generation improves pro-      To attack, the attacker first acquires a small APEMAGA token
tection. For F LAMES-100k, totals are essentially flat between which seeds the inventory for a later dump. Then, to deflate the
single- and multi-turn (pre: 21/21, post: 22/22, pre+post: 21 token pair balance, the attacker calls family(address(PAIR))
vs. 20), suggesting the larger fine-tuned model maintains repeatedly. Each call burns ∼ 99.9% of the pair’s APEMAGA
coherence even without the stacking the previous generations. balance (by design of the _approve_ method in Figure 10a).
   Our protocol includes running regression tests. Now we Three calls to this function are sufficient to reduce it to near-
measure the proportion of invariants which break some func- zero. Next, the attacker invokes pair.sync() to synchronize
tionality. We observe that 41.3% (134/324) of invariants reserves. The Uniswap pair now records a near-zero APEMAGA
generated by the baseline preserve the functionality of the reserve, while the WETH reserve is unchanged, causing the on-
contracts. In comparison, this number for F LAMES-20k and chain ratio to appear extremely high. Then, the attacker sells at
F LAMES-100k is 64.5% (209/324) and 67.9% (220/324), re- a skewed price by executing APEMAGA → WETH swap. Because
spectively. This demonstrates that F LAMES generates invari- the pool believes APEMAGA is very scarce, the trade pays out
ants that do not negatively affect the contract’s functionality. disproportionate WETH for the attacker’s tokens.
A significant portion of these are benign with respect to the       Hardening Using F LAMES Following the RQ1–RQ3 setup,
contract’s functionality but are also incapable of stopping the we construct an abstract context (that keeps the full implemen-
exploit. Figure 9 shows a contract vulnerable to reentrancy. tation of thefamily function, relevant state and signatures) and
F LAMES-100k’s synthesized pre-condition (_am > 0) and post- insert a single masked require as a pre-condition (Figure 10c).
 1 function _approve_ ( address owner , address spender ,             less of the state and require(true) has no other effect except
        uint256 amount ) internal virtual {
 2 require ( owner != address (0) , " Burn from the 0 address " ) ;   consuming gas. C ODE L LAMA, F LAMES-20k, and F LAMES-
 3 require ( owner == spender , " Burn to the owner address " ) ;     100k each generate 24, 20, and 20 cases of require(false).
 4 uint256 accountBalance = ( _balances [ owner ] + trading () )
          * 999 / 1000;                                               Fine-tuning further from F LAMES-20k to F LAMES-100k does
 5 _beforeTokenTransfer ( owner , address (0) , accountBalance ) ;    not reduce the synthesis of require(false) but eliminates
 6 require ( accountBalance >= amount , " Amt exceeds balance " ) ;
 7 _balances [ owner ] -= accountBalance ;                            require(true). Out of the 20 cases where C ODE L LAMA
 8 _totalSupply -= accountBalance ;                                   generates require(true), 14 of them are false negatives
 9 _afterTokenTransfer ( owner , address (0) , accountBalance ) ;
10 }                                                                  (the code requires an invariant, but C ODE L LAMA generates
                                                                      require(true) with no effect on the vulnerable control flow).
          (a) Vulnerable internal burn used by family( ).
                                                                      Furthermore, in both F LAMES models, for all cases of gen-
 1 contract ERC20 is Context , IERC20 { ... }                         erating trivial require(false), they generate them as post-
 2 contract Tonken_patch is ERC20 {
 3 constructor (                                                      conditions.
 4     string memory name_ ,
 5     string memory symbol_ ,                                                            VII. R ELATED W ORK
 6     uint8 decimals_ ,
 7     uint256 totalSupply_                                             We review the prior works on generating invariants using
 8 ) ERC20 ( name_ , symbol_ , decimals_ , totalSupply_ ) {}
 9 receive () external payable {}                                     LLMs (§VII-B), smart contract invariant generation (§VII-C),
10 function family ( address account ) external {                     and using invariants for smart contract security (§VII-A).
11     require(msg.sender==account, "caller != token owner");
12     super . _approve_ ( account , account ,0) ;
13 }                                                                  A. Usage of Invariants for Smart Contract Security
14 }
                                                                         Li et al. inject executable checks into smart contracts to
        (b) Ground-truth pre-condition guarding family( ).            prevent known exploits at runtime [41]. The main difference is
1 function family ( address account ) external {                      that F LAMES automatically synthesizes the invariants whereas
2 require(account== msgSender());
3 super . _approve_ ( account , account ,0) ;                         they rely on user-written ones.
4}                                                                       PROMFUZZ [42] uses six hand-crafted invariant templates
          (c) Pre-condition synthesized by F LAMES-100k.              as analysis oracles to detect functional bugs. These templates
                                                                      could be backed by a F LAMES-style invariant generator, re-
Fig. 10: APEMAGA hardening with F LAMES: (a) vulnerable               moving static templates that limit the scope of their analysis
internal burn; (b) ground-truth fix; (c) F LAMES-generated            while retaining the bug-oriented placement and their validation
invariant.                                                            loop. Fuzzers like Echidna [43] and ItyFuzz [44] use user-
                                                                      provided invariants as falsification oracles to guide vulnera-
Using F LAMES-100k, the model synthesizes account ==
                                                                      bility analysis. Provers such as Certora Prover [45] and solc-
_msgSender() (Section V-D) which is semantically equivalent
                                                                      verify [46] relies on provided pre-/post-conditions for property
to the ground-truth patch invariant presented in Figure 10b.
                                                                      verification. HighGuard [47] uses business-logic invariants
The hardened contract compiles under the original settings.
                                                                      to monitor contracts and catch exploits. XploGen [48] uses
The synthesized F LAMES invariant reverts the exploit’s call,
                                                                      invariants as oracles to synthesize exploits. Contrary to them,
rendering the attack unsuccessful.
                                                                      F LAMES generate invariants and do not expect engineer to
  RQ4 Answer: Hardening against a Real-World Attack                   write them. F LAMES can feed consumers of invariants such
                                                                      as fuzzers and provers.
 F LAMES-100k is capable of generating an invariant that pro-
 tects against the real-world APEMAGA attack. The synthesized         B. Generating Invariants Using LLMs
 invariant is fully validated by reverting the proof-of-concept
                                                                         Pei et al. synthesize invariants using fine-tuned LLMs
 exploit of the attack. The F LAMES invariant is semantically
                                                                      for Java programs [49]. They use Daikon-mined templates
 equivalent to the ground truth APEMAGA mitigating invariant.
                                                                      as supervision labels. Unlike this work, which evaluates
                                                                      agreement with Daikon and does not produce deployable
                  VI. T HREATS TO VALIDITY
                                                                      code, F LAMES targets executable Solidity defenses by infilling
   Although we use context abstraction (Section II-B), very           concrete require statements, enforcing compilability. Further-
large contracts can still exceed the model’s token limit, leading     more, we measure downstream security impact (regression
to truncated context and potentially incorrect invariants.            tests, exploit replays, and a real incident case study). The
   Some generated invariants may over-/under-constrain a con-         supervision also differs as Pei et al. train against Daikon [50]
tract (stronger/weaker cases in §III). To mitigate that, another      templates, whereas F LAMES learns from actual human-written
method of validation (e.g., replaying transaction history in case     invariants extracted at scale from D ISL dataset.
of invariant-based hardening for upgraded contracts [40]) is a           Here, we review the research on LLM-based invariant gen-
valid solution.                                                       eration for general programming languages. ClassInvGen [51]
   All three models in all strategies occasionally gener-             couples GPT models with testing to synthesize executable
ate two instances of trivial invariants: require(false) and           invariants, outperforming both a pure LLM baseline and
require(true). require(false) reverts the transaction regard-         dynamic invariant mining with Daikon [50].
   Translating informal intent into formal specifications is                                  VIII. C ONCLUSION
also beneficial. Previous work has demonstrated that LLM-              We have presented F LAMES, a fne-tuning approach for
generated invariants can catch real defects [52]. There has         synthesizing Solidity invariants for defensive hardening of
also been work on fine-tuning LLMs for Java/JML [53].               smart contracts. Across three axes, we have demonstrated
SpecGen [54] employs a two-phase LLM generation and                 F LAMES’s capabilities. First, it produces usable invariants
verification: conversational specification drafting is followed     compiling in real-world smart contracts : F LAMES gener-
by solver-based filtering which outperforms vanilla prompting       ates 96.7% compilable invariants. Second, fine-tuning largely
and classical invariant mining. In contrast to prior LLM-based      improves semantic similarity to human-written ground truth
invariant generators, F LAMES targets the different domain of       (2226/5000 equivalent) over the baseline model (1176/5000).
smart contract hardening. F LAMES fine-tunes a code model           Third, in end-to-end exploit prevention on 108 vulnerable
to produce require(...) statements at pre-/post-conditions.         contracts, F LAMES has been shown to produce invariants that
F LAMES does not assume any natural-language specification          prevent exploits while preserving functionality. Lastly, our case
or vulnerability labels.                                            study of using F LAMES on a real DeFi incident demonstrates
                                                                    its capability in reverting the actual attack’s transaction.
                                                                       Our study shows that placement matters. A potential future
C. Smart Contract Invariant Generation                              direction is to learn the invariant synthesis location itself.
                                                                    This requires learning objectives about where to synthesize the
   Prior research as used the contract’s transaction history to     invariants. To foster future research, we release the F LAMES
mine likely invariants for smart contracts. InvCon [55] adapts      model weights, fine-tuning, and evaluation pipelines.
Daikon-style mining to smart contract traces and mines ERC20
invariants. InvCon+ [9] filters the mined candidate invariants                                     R EFERENCES
to eliminate false positives. Reinforcement learning policies        [1] H. Rezaei, M. Eshghie, K. Anderesson, and F. Palmieri, “Sok:
trained against verifiers can suggest arithmetic-safety invari-          Root cause of $1 billion loss in smart contract real-world attacks
ants for smart conrtacts [56]. VeriSmart [13] uses symbolic              via a systematic literature review of vulnerabilities,” 2025. [Online].
                                                                         Available: https://arxiv.org/abs/2507.20175
analysis to discover arithmetic invariants. Instead of proving       [2] L. Zhou, X. Xiong, J. Ernstberger, S. Chaliasos, Z. Wang, Y. Wang,
absence of arithmetic faults, F LAMES synthesizes concrete               K. Qin, R. Wattenhofer, D. Song, and A. Gervais, “SoK: Decentralized
invariants to prevent them, and it is evaluated across vulner-           Finance (DeFi) Attacks,” in 2023 IEEE Symposium on Security and
                                                                         Privacy (SP), May 2023, pp. 2444–2461.
ability classes beyond arithmetic. PropertyGPT [15] retrieves        [3] A. Ghaleb and K. Pattabiraman, “How effective are smart contract
known specifications for LLM-based Solidity auditing and re-             analysis tools? evaluating smart contract static analysis tools using bug
fines the auditing results with analyzer feedback. SmartInv [14]         injection,” in Proceedings of the 29th ACM SIGSOFT International
                                                                         Symposium on Software Testing and Analysis, ser. ISSTA 2020. New
targets detection of business logic flaws, by prompting LLMs             York, NY, USA: Association for Computing Machinery, Jul. 2020, pp.
with Solidity code enhanced with protocol documentation and              415–427.
a Tier-of-Thought strategy. SmartOracle [57] mines likely            [4] S. Chaliasos, M. A. Charalambous, L. Zhou, R. Galanopoulou,
                                                                         A. Gervais, D. Mitropoulos, and B. Livshits, “Smart contract and
invariants from contract transaction history and uses them               defi security tools: Do they meet the needs of practitioners?”
as analysis oracles to flag violations in new transactions.              in Proceedings of the IEEE/ACM 46th International Conference
Assuming that future behavior should subsume the transaction             on Software Engineering, ser. ICSE ’24. New York, NY, USA:
                                                                         Association for Computing Machinery, 2024. [Online]. Available:
history, SmartOracle can act as a runtime monitor. Com-                  https://doi.org/10.1145/3597503.3623302
pared to SmartOracle [57], F LAMES hardens the contracts             [5] S. Bobadilla, M. Jin, and M. Monperrus, “Do automated fixes
even when there is no or limited transaction history (pre-               truly mitigate smart contract exploits?” 2025. [Online]. Available:
                                                                         https://arxiv.org/abs/2501.04600
deployment) or the future transaction history subsumption            [6] B. Meyer, “Applying ’design by contract’,” Computer, vol. 25, no. 10,
assumption is invalid for the contract. TrustLLM [16] fine-              pp. 40–51, Oct. 1992.
tune a detector LLM to label functions as vulnerable and then        [7] “Ethereum Yellow Paper,” Dec. 2022. [Online]. Available: https:
                                                                         //github.com/ethereum/yellowpaper
use agentic critics to produce natural-language justifications.      [8] Z. Chen, Y. Liu, S. M. Beillahi, Y. Li, and F. Long, “Demystifying
LLM-based detectors that fine-tune on smart contract audit               invariant effectiveness for securing smart contracts,” Proc. ACM
reports show promising detection and explanation results es-             Softw. Eng., vol. 1, no. FSE, Jul. 2024. [Online]. Available:
                                                                         https://doi.org/10.1145/3660786
pecially on functional bugs (aka business logic flaws) which         [9] Y. Liu, C. Zhang, and Y. Li, “Automated invariant generation for
are often overlooked by classic runtime/static analysis but they         solidity smart contracts,” IEEE Transactions on Dependable and Secure
stop at detection and do not generate deployable defenses                Computing, pp. 1–17, 2025.
                                                                    [10] Z. Chen, H. Qin, N. Chen, X. Zhao, L. Xue, X. Luo, and X.-M.
or validate exploit mitigation end-to-end [14], [58], [59]. In           Wu, “Solbench: A dataset and benchmark for evaluating functional
comparison, F LAMES conducts defensive code synthesis given              correctness in solidity code completion and repair,” 2025. [Online].
only source code, it synthesize tthe missing Solidity invariants         Available: https://arxiv.org/abs/2503.01098
                                                                    [11] Z. Peng, X. Yin, R. Qian, P. Lin, Y. Liu, H. Zhang, C. Ying,
at strategic placements without relying on prior vulnerability           and Y. Luo, “Soleval: Benchmarking large language models for
knowledge, label or documentation. We note that F LAMES and              repository-level solidity code generation,” 2025. [Online]. Available:
TrustLLM [16] are complementary as TrustLLM can prioritize               https://arxiv.org/abs/2502.18793
                                                                    [12] A. Dinaburg, “Evaluating solidity support in ai coding assistants,” Trail
functions for hardening and prepare the ground for F LAMES to            of Bits Blog, November 2024. [Online]. Available: https://blog.trailofbits.
synthesize invariants specific locations (pre vs. post vs. both).        com/2024/11/19/evaluating-solidity-support-in-ai-coding-assistants/
[13] S. So, M. Lee, J. Park, H. Lee, and H. Oh, “Verismart: A highly precise      [30] M. Ortner and S. Eskandari, “Smart contract sanctuary.” [Online].
     safety verifier for ethereum smart contracts,” in 2020 IEEE Symposium             Available: https://github.com/tintinweb/smart-contract-sanctuary
     on Security and Privacy (SP), 2020, pp. 1678–1694.                           [31] “Smartbugs/smartbugs-wild,”                  https://github.com/smartbugs/
[14] S. J. Wang, K. Pei, and J. Yang, “SMARTINV: Multimodal                            smartbugs-wild, Feb. 2024.
     Learning for Smart Contract Invariant Inference.” IEEE Computer              [32] T. Durieux, J. F. Ferreira, R. Abreu, and P. Cruz, “Empirical review
     Society, Feb. 2024, pp. 125–125, iSSN: 2375-1207. [Online].                       of automated analysis tools on 47,587 Ethereum smart contracts,”
     Available: https://www.computer.org/csdl/proceedings-article/sp/2024/             in Proceedings of the ACM/IEEE 42nd International Conference on
     313000a126/1Ub23GNTAeQ                                                            Software Engineering, ser. ICSE ’20. New York, NY, USA: Association
[15] Y. Liu, Y. Xue, D. Wu, Y. Sun, Y. Li, M. Shi, and Y. Liu, “PropertyGPT:           for Computing Machinery, Oct. 2020, pp. 530–541.
     LLM-driven Formal Verification of Smart Contracts through Retrieval-         [33] “Renardbebe/Smart-Contract-Benchmark-Suites: A unified smart
     Augmented Property Generation,” in Proceedings of the 2025 Network                contract      standard     data    set.”    https://github.com/renardbebe/
     and Distributed System Security Symposium (NDSS). Internet Society,               Smart-Contract-Benchmark-Suites/tree/master.
     2025.                                                                        [34] “InPlusLab/DAppSCAN: DAppSCAN: Building Large-Scale Datasets
[16] W. Ma, D. Wu, Y. Sun, T. Wang, S. Liu, J. Zhang, Y. Xue, and Y. Liu,              for Smart Contract Weaknesses in DApp Projects.” https://github.com/
     “Combining fine-tuning and llm-based agents for intuitive smart contract          InPlusLab/DAppSCAN.
     auditing with justifications,” in Proceedings of the 47th International      [35] S. Bobadilla, M. Jin, and M. Monperrus, “Do automated fixes
     Conference on Software Engineering (ICSE 2025), 2025.                             truly mitigate smart contract exploits?” 2025. [Online]. Available:
[17] S. Team. A disastrous vulnerability found in smart contracts                      https://arxiv.org/abs/2501.04600
     of beautychain (bec). Accessed: 2025-10-03. [Online]. Available:             [36] M. Eshghie, “Sindi: Semantic invariant differencing for solidity
     https://medium.com/secbit-media/dbf24ddbc30e                                      smart contracts,” accessed: 2025-10-02. [Online]. Available: https:
[18] M. Eshghie, V. Åryd, C. Artho, and M. Monperrus, “Solidiffy: Ast                 //github.com/mojtaba-eshghie/Sindi
     differencing for solidity smart contracts,” 2025. [Online]. Available:       [37] S. Bobadilla, M. Jin, and M. Monperrus, “sb-heists: A scientific
     https://arxiv.org/abs/2411.07718                                                  dataset of smart contract exploits.” [Online]. Available: https:
[19] Z. Chen, S. Kommrusch, M. Tufano, L.-N. Pouchet, D. Poshyvanyk, and               //github.com/ASSERT-KTH/sb-heists
     M. Monperrus, “SequenceR: Sequence-to-Sequence Learning for End-             [38] B. Rozière, J. Gehring, F. Gloeckle, S. Sootla, I. Gat, X. E. Tan,
     to-End Program Repair,” IEEE Transactions on Software Engineering,                Y. Adi, J. Liu, R. Sauvestre, T. Remez, J. Rapin, A. Kozhevnikov,
     vol. 47, no. 9, pp. 1943–1959, 2021.                                              I. Evtimov, J. Bitton, M. Bhatt, C. C. Ferrer, A. Grattafiori, W. Xiong,
[20] M. Bavarian, H. Jun, N. Tezak, J. Schulman, C. McLeavey, J. Tworek,               A. Défossez, J. Copet, F. Azhar, H. Touvron, L. Martin, N. Usunier,
     and M. Chen, “Efficient training of language models to fill in the                T. Scialom, and G. Synnaeve, “Code llama: Open foundation models
     middle,” 2022. [Online]. Available: https://arxiv.org/abs/2207.14255              for code,” 2024. [Online]. Available: https://arxiv.org/abs/2308.12950
[21] A. Madaan, N. Tandon, P. Gupta, S. Hallinan, L. Gao, S. Wiegreffe,           [39] M. Eshghie, W. Ahrendt, C. Artho, T. T. Hildebrandt, and G. Schneider,
     U. Alon, N. Dziri, S. Prabhumoye, Y. Yang, S. Gupta, B. P.                        “Capturing Smart Contract Design with DCR Graphs,” in Software
     Majumder, K. Hermann, S. Welleck, A. Yazdanbakhsh, and                            Engineering and Formal Methods, C. Ferreira and T. A. C. Willemse,
     P. Clark, “Self-Refine: Iterative Refinement with Self-Feedback,”                 Eds. Cham: Springer Nature Switzerland, 2023, pp. 106–125.
     in Advances in Neural Information Processing Systems, A. Oh,                 [40] M. Eshghie, W. Ahrendt, C. Artho, T. Troels Hildebrandt, and G. Schnei-
     T. Naumann, A. Globerson, K. Saenko, M. Hardt, and S. Levine,                     der, “Formalizing Smart Contract Design Patterns with DCR Graphs,”
     Eds., vol. 36. Curran Associates, Inc., 2023, pp. 46 534–46 594.                  2025.
     [Online]. Available: https://proceedings.neurips.cc/paper files/paper/       [41] A. Li, J. A. Choi, and F. Long, “Securing smart contract with runtime
     2023/file/91edff07232fb1b55a505a9e9f6c0ff3-Paper-Conference.pdf                   validation,” in Proceedings of the 41st ACM SIGPLAN Conference on
[22] E. Nijkamp, B. Pang, H. Hayashi, L. Tu, H. Wang, Y. Zhou,                         Programming Language Design and Implementation, ser. PLDI 2020.
     S. Savarese, and C. Xiong, “Codegen: An open large language model                 New York, NY, USA: Association for Computing Machinery, 2020, p.
     for code with multi-turn program synthesis,” 2023. [Online]. Available:           438–453. [Online]. Available: https://doi.org/10.1145/3385412.3385982
     https://arxiv.org/abs/2203.13474                                             [42] X. Lin, Q. Xie, B. Zhao, Y. Tian, S. Zonouz, N. Ruan, J. Li, R. Beyah,
[23] N. Houlsby, A. Giurgiu, S. Jastrzebski, B. Morrone, Q. De Laroussilhe,            and S. Ji, “Promfuzz: Leveraging llm-driven and bug-oriented composite
     A. Gesmundo, M. Attariyan, and S. Gelly, “Parameter-efficient                     analysis for detecting functional bugs in smart contracts,” in Proceedings
     transfer learning for NLP,” in Proceedings of the 36th International              of the 40th IEEE/ACM International Conference on Automated Software
     Conference on Machine Learning, ser. Proceedings of Machine                       Engineering (ASE 2025), Research Papers Track. Seoul, South Korea:
     Learning Research, K. Chaudhuri and R. Salakhutdinov, Eds.,                       IEEE/ACM, Nov. 2025, to appear.
     vol. 97. PMLR, 09–15 Jun 2019, pp. 2790–2799. [Online]. Available:           [43] G. Grieco, W. Song, A. Cygan, J. Feist, and A. Groce, “Echidna:
     https://proceedings.mlr.press/v97/houlsby19a.html                                 effective, usable, and fast fuzzing for smart contracts,” in Proceedings of
[24] M. Ren, Z. Yin, F. Ma, Z. Xu, Y. Jiang, C. Sun, H. Li, and Y. Cai,                the 29th ACM SIGSOFT International Symposium on Software Testing
     “Empirical evaluation of smart contract testing: What is the best choice?”        and Analysis, ser. ISSTA 2020. New York, NY, USA: Association
     in Proceedings of the 30th ACM SIGSOFT International Symposium on                 for Computing Machinery, Jul. 2020, pp. 557–560. [Online]. Available:
     Software Testing and Analysis. Virtual Denmark: ACM, Jul. 2021, pp.               https://dl.acm.org/doi/10.1145/3395363.3404366
     566–579.                                                                     [44] C. Shou, S. Tan, and K. Sen, “ItyFuzz: Snapshot-Based Fuzzer for Smart
[25] André       Storhaug,       “smart contracts    (revision     448b3e9),”         Contract,” Jun. 2023.
     https://huggingface.co/datasets/andstor/smart contracts, 2023.               [45] “The Certora Verification Language — Certora Prover Documentation,”
[26] A. Storhaug, J. Li, and T. Hu, “ Efficient Avoidance of Vulnerabilities in        accessed: 2025-04-11. [Online]. Available: https://docs.certora.com/en/
     Auto-completed Smart Contract Code Using Vulnerability-constrained                latest/docs/cvl/index.html
     Decoding ,” in 2023 IEEE 34th International Symposium on Software            [46] Á. Hajdu and D. Jovanović, “solc-verify: A modular verifier for solidity
     Reliability Engineering (ISSRE). Los Alamitos, CA, USA: IEEE                      smart contracts,” in Verified Software. Theories, Tools, and Experiments,
     Computer Society, Oct. 2023, pp. 683–693. [Online]. Available:                    S. Chakraborty and J. A. Navas, Eds. Cham: Springer International
     https://doi.ieeecomputersociety.org/10.1109/ISSRE59848.2023.00035                 Publishing, 2020, pp. 161–179.
[27] “Ethereum in BigQuery: A Public Dataset for smart contract                   [47] M. Eshghie, C. Artho, H. Stammler, W. Ahrendt, T. Hildebrandt, and
     analytics,”         https://cloud.google.com/blog/products/data-analytics/        G. Schneider, “Highguard: Cross-chain business logic monitoring of
     ethereum-bigquery-public-dataset-smart-contract-analytics.                        smart contracts,” in Proceedings of the 39th IEEE/ACM International
[28] M. Allamanis, “The adverse effects of code duplication in machine                 Conference on Automated Software Engineering, 2024, pp. 2378–2381.
     learning models of code,” in Proceedings of the 2019 ACM SIGPLAN             [48] M. Eshghie and C. Artho, “Oracle-guided vulnerability diversity and
     International Symposium on New Ideas, New Paradigms, and Reflections              exploit synthesis of smart contracts using llms,” in Proceedings of
     on Programming and Software, ser. Onward! 2019. New York, NY,                     the 39th IEEE/ACM International Conference on Automated Software
     USA: Association for Computing Machinery, Oct. 2019, pp. 143–153.                 Engineering, 2024, pp. 2240–2248.
[29] “Zellic/smart-contract-fiesta · Datasets at Hugging Face,” https://          [49] K. Pei, D. Bieber, K. Shi, C. Sutton, and P. Yin, “Can large language
     huggingface.co/datasets/Zellic/smart-contract-fiesta.                             models reason about program invariants?” in Proceedings of the 40th In-
     ternational Conference on Machine Learning, ser. ICML’23. JMLR.org,
     2023.
[50] M. D. Ernst, J. H. Perkins, P. J. Guo, S. McCamant, C. Pacheco,
     M. S. Tschantz, and C. Xiao, “The Daikon System for Dynamic
     Detection of Likely Invariants,” Science of Computer Programming,
     vol. 69, no. 1, pp. 35–45, Dec. 2007. [Online]. Available: https:
     //www.sciencedirect.com/science/article/pii/S016764230700161X
[51] C. Sun, V. Agashe, S. Chakraborty, J. Taneja, C. Barrett, D. Dill,
     X. Qiu, and S. K. Lahiri, “Classinvgen: Class invariant synthesis
     using large language models,” 2025. [Online]. Available: https:
     //arxiv.org/abs/2502.18917
[52] M. Endres, S. Fakhoury, S. Chakraborty, and S. K. Lahiri, “Can large
     language models transform natural language intent into formal method
     postconditions?” Proc. ACM Softw. Eng., vol. 1, no. FSE, Jul. 2024.
     [Online]. Available: https://doi.org/10.1145/3660791
[53] S. Greiner, N. Bühlmann, M. Ohrndorf, C. Tsigkanos, O. Nierstrasz,
     and T. Kehrer, “Automated generation of code contracts: Generative
     ai to the rescue?” in Proceedings of the 23rd ACM SIGPLAN
     International Conference on Generative Programming: Concepts and
     Experiences, ser. GPCE ’24. New York, NY, USA: Association
     for Computing Machinery, 2024, p. 1–14. [Online]. Available:
     https://doi.org/10.1145/3689484.3690738
[54] L. Ma, S. Liu, Y. Li, X. Xie, and L. Bu, “Specgen: Automated
     generation of formal program specifications via large language models,”
     2025. [Online]. Available: https://arxiv.org/abs/2401.08807
[55] Y. Liu and Y. Li, “InvCon: A Dynamic Invariant Detector for Ethereum
     Smart Contracts,” in Proceedings of the 37th IEEE/ACM International
     Conference on Automated Software Engineering, ser. ASE ’22. New
     York, NY, USA: Association for Computing Machinery, Jan. 2023, pp.
     1–4. [Online]. Available: https://doi.org/10.1145/3551349.3559539
[56] J. Liu, Y. Chen, B. Tan, I. Dillig, and Y. Feng, “Learning Contract
     Invariants Using Reinforcement Learning,” in Proceedings of the
     37th IEEE/ACM International Conference on Automated Software
     Engineering, ser. ASE ’22. New York, NY, USA: Association for
     Computing Machinery, Jan. 2023, pp. 1–11. [Online]. Available:
     https://dl.acm.org/doi/10.1145/3551349.3556962
[57] J. Su, J. Chen, Z. Fang, X. Lin, Y. Tang, and Z. Zheng, “SmartOracle:
     Generating Smart Contract Oracle via Fine-Grained Invariant Detection,”
     IEEE Transactions on Software Engineering, pp. 1–13, 2025.
[58] J. Bu, W. Li, Z. Li, Z. Zhang, and X. Li, “Enhancing smart contract
     vulnerability detection in dapps leveraging fine-tuned llm,” 2025.
     [Online]. Available: https://arxiv.org/abs/2504.05006
[59] L. Yu, Z. Huang, H. Yuan, S. Cheng, L. Yang, F. Zhang, C. Shen,
     J. Ma, J. Zhang, J. Lu, and C. Zuo, “Smart-llama-dpo: Reinforced large
     language model for explainable smart contract vulnerability detection,”
     Proc. ACM Softw. Eng., vol. 2, no. ISSTA, Jun. 2025. [Online].
     Available: https://doi.org/10.1145/3728878
