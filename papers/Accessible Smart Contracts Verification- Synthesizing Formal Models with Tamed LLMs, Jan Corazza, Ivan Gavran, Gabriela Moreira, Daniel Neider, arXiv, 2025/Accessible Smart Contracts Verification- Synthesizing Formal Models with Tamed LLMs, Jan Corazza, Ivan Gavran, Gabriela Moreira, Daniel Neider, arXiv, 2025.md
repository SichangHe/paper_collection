                                                Accessible Smart Contracts Verification:
                                             Synthesizing Formal Models with Tamed LLMs

                                         Jan Corazza1[0009−0000−1342−0117] , Ivan Gavran2[0000−0002−2049−6264] , Gabriela
                                             Moreira2[0000−0003−0275−5717] , and Daniel Neider1[0000−0001−9276−6342]
                                         1
                                             Research Center Trustworthy Data Science and Security, TU Dortmund University,
                                                                         Dortmund, Germany
arXiv:2501.12972v1 [cs.SE] 22 Jan 2025




                                                            {jan.corazza,daniel.neider}@tu-dortmund.de
                                                                         2
                                                                           Informal Systems
                                                                 {ivan,gabriela}@informal.systems



                                                 Abstract. When blockchain systems are said to be trustless, what this
                                                 really means is that all the trust is put into software. Thus, there are
                                                 strong incentives to ensure blockchain software is correct—vulnerabilities
                                                 here cost millions and break businesses. One of the most powerful ways of
                                                 establishing software correctness is by using formal methods. Approaches
                                                 based on formal methods, however, induce a significant overhead in terms
                                                 of time and expertise required to successfully employ them. Our work
                                                 addresses this critical disadvantage by automating the creation of a for-
                                                 mal model—a mathematical abstraction of the software system—which
                                                 is often a core task when employing formal methods. We perform model
                                                 synthesis in three phases: we first transpile the code into model stubs;
                                                 then we “fill in the blanks” using a large language model (LLM); finally,
                                                 we iteratively repair the generated model, on both syntactical and se-
                                                 mantical level. In this way, we significantly reduce the amount of time
                                                 necessary to create formal models and increase accessibility of valuable
                                                 software verification methods that rely on them. The practical context
                                                 of our work was reducing the time-to-value of using formal models for
                                                 correctness audits of smart contracts.

                                                 Keywords: Code Generation · Large Language Models · Formal Meth-
                                                 ods · Model Synthesis · Smart Contracts · Model-Based Techniques ·
                                                 Software Auditing.


                                         1     Introduction
                                         Modern blockchain platforms such as Ethereum and Cosmos extend the underly-
                                         ing consensus technology pioneered by Bitcoin towards a generalized computing
                                         platform. Rather than solely reaching consensus on transactions modifying the
                                         state of a ledger, these platforms also enable consensus on program executions.
                                         Roughly speaking, they are platforms for decentralized computing capable of
                                         executing stateful protocols—called smart contracts—in a trustless manner. For
                                         example, one may write a smart contract for holding an auction without having
                                         to put one’s trust into a centralized marketplace provider such as eBay.
2       J. Corazza et al.

    Currently, the smart contract ecosystem manages assets worth billions of
dollars. This substantial value makes smart contracts prime targets for cyberat-
tacks. A successful exploit can result in catastrophic financial losses, potentially
devastating businesses and the investments of numerous individuals.
    Due to these high stakes, companies launching blockchain-based products
have begun placing an increasingly high priority on carrying out thorough soft-
ware audits before the launch. Most auditors, however, base their work on man-
ual line-by-line code inspection, foregoing more powerful tools such as formal
methods.
    Formal methods are a potent tool in the software verification toolkit, par-
ticularly for high-stakes environments like blockchain-based systems. They rely
on rigorous logical reasoning to either automatically uncover vulnerabilities or
assert their absence, thereby mathematically guaranteeing that certain types of
bugs do not exist. Not everything is perfect, however: for large codebases and
expressive languages, formal methods scale poorly. One common way to address
the problem of scalability is to build a formal model of the system and rea-
son about that model instead of the full system implementation. We call the
techniques embracing this approach model-based techniques (MBT).
    A formal model is a mathematical abstraction of the software system—the art
of modeling is about abstracting away all unnecessary details while preserving
relevant aspects of the system. For example, in a banking application, a model
will capture how funds change owners. When verifying the model, we can ensure
that users cannot access funds that do not belong to them.
    We can reason about properties of the model, and establish the connection
of the model to the software using model-based testing [18] techniques. Thus,
model-based techniques provide an effective framework for verifying software.
However, because of the initial cost of writing a model and the need for special-
ized knowledge of the modeling language, model-based techniques did not yet
see widespread adoption.
    In this work, we reduce the effort for an auditor writing a model, with help of
large language models (LLMs). We tame LLMs’ propensity for hallucination by
setting a hard frame around it through mechanical model synthesis, and through
iterative repair of the generated model, until it conforms to the user’s (partial)
specification.


An auditor’s workflow (model-based techniques) Let us examine the
workflow of an auditor who attempts to use model-based techniques (we get into
more details of those techniques in Section 3.1). After understanding the logic
of the codebase, the auditor models it in a modeling language. Now the auditor
is able to reason about the model, but a connection to the implementation is
missing. Thus, the auditor writes some glue code (called an adapter ), which
translates model’s abstract traces into test cases.
    These two steps are already time-consuming for an auditor already experi-
enced in MBT. For auditors just starting with MBT, they can also be daunting.
Given that audits are typically time-constrained, the time that needs to be in-
                               Synthesizing Formal Models with Tamed LLMs             3

vested is often used as an argument against using (otherwise effective and useful)
model-based techniques.
    Therefore, the primary objective of our work is to significantly reduce the
time and effort needed to apply model-based techniques to smart contracts. To
this end, we propose an automated method that generates a formal model of a
smart contract, based on the contract itself and the auditor’s3 input.


Overview of the method Our method allows the auditor-user to automate
parts of the MBT workflow, or take over in the middle of the process. Impor-
tantly, at every step, the method provides a valuable artifact to the auditor.
    As a first step, we transpile the smart contract(s) into a stub of the model:
the stub captures interleavings of different actions, but does not capture the
actions’ semantics. As a part of the transpilation process, we are also generating
the stub of the adapter. At this point, the auditor can use both stubs to run
fuzzing tests against the contract.
    In the second step, we ask the user to provide a natural language (NL)
description of each action and a couple of input-output examples. (An action
is a transformation of the state, so the notion of I/O examples is well-defined.)
Our method then interacts with an LLM: each time the generated model is
not aligned with the user-provided examples, it generates the prompt pointing
out the inconsistency and requesting new generation. Throughout our work we
utilize OpenAI’s Chat Completions API for this purpose, specifically GPT-4o.
    The main insight on which we based the design of our tool is that the careful
separation of concerns between mechanical synthesis (transpilation) and sta-
tistical synthesis (LLM-based) is crucial. Relying on an LLM to generate the
whole model results in hallucinations (e.g., using non-existent helper functions)
or convincingly looking yet wrong models. Conversely, transpiling the full con-
tract into a model is hopeless: even if it worked, it would result in line-by-line
re-implementation of the contract, instead of a good abstraction. We suggest
taming as an appropriate metaphor: model stubs give a firm frame that con-
straints the wild creative power of LLMs.
    We focus on smart contracts implemented using CosmWasm [2], a smart-
contract platform of the Cosmos ecosystem. CosmWasm contracts are written
in Rust, and the models that our tool generates are written in Quint [10], an
executable modeling language based on TLA—temporal logic of actions [23]. Fig-
ure 1 provides a high-level overview of our method for transforming a CosmWasm
contract into a Quint model. The process involves three main steps.

1. Mechanical Generation: Transpile as much of the Rust source code into
   Quint, leaving placeholders (“stubs”) for parts that cannot be easily tran-
   spiled.
3
    We refer to an auditor as the main user of our method because our work was done
    in the context of a team performing correctness audits. The method is equally useful
    for developers aiming to employ formal methods in their work.
4      J. Corazza et al.

                                            fixed
                                    Done             Repair
                                                              not fixed

                           Mechanical   LLM-based
                           generation    synthesis
             CosmWasm                                Quint model
              contract

                                    1. NL descriptions
                                    2. I/O examples

Fig. 1. High-level illustration of the method for generating a Quint model from a
CosmWasm contract.


2. LLM-based Synthesis: Use a large language model (LLM) to complete
   the stubs based on user’s input, thereby finishing the Quint model.
3. Testing and Repair: Conduct a series of tests on the generated model and
   identify the LLM’s syntactic and semantic hallucinations. Then, provide the
   information about the problem to the LLM and ask for it to be fixed.

    In Sections 2 and 3, we discuss related work and provide the necessary back-
ground information, respectively. In Section 4, we elaborate the technical details
involved in each step of our method.
    To evaluate its effectiveness, we created a benchmark based on CosmWasm
CTF [3], a collection of publicly available CosmWasm smart contracts with in-
jected bugs. Along with the evaluation results on the CTF benchmark, we also
conducted two case studies of using our method as a part of an auditor’s work.
The evaluation results (described in Section 5) suggest the following conclusion:
our method successfully generates models for the benchmark contracts and is
useful for auditors. Using the method, we uncovered a bug in a real-world smart
contract.


2     Related Work

In this section, we provide an overview of existing research and technologies
related to formal methods for blockchain systems and LLM code generation,
and place our work within this broader context.


2.1   Formal Methods for Blockchain Systems

Software vulnerabilities in the blockchain world imply high financial and repu-
tational loss. Once on-chain, the software with a fix cannot be deployed quickly.
Therefore, there has been a lot of effort in ensuring blockchain systems are cor-
rect.
                             Synthesizing Formal Models with Tamed LLMs          5

    On the level of the underlying blockchain infrastructure, engaging software
verification experts to assess the correctness of the critical parts has become
a standard. The experts employ a variety of tools to conduct their analysis,
for instance: Jepsen [6] for fault tolerance, modeling with TLA+ [24] for prov-
ing properties of inter-blockchain communication [14], or providing a reference
implementation [11] in Dafny [25].
    Verifying individual smart contracts is (in principle, at least) a more attain-
able task than verifying the infrastructure, while the incentives remain equally
high. Thus, there is abundance of tools for smart contracts correctness assurance.
Examples include Certora [1], Slither [13], Mythril [8], Echidna [19], Quint [10],
to name but a few.
    One thing these tools all share is that only specialized experts can use them.
The problem is well recognized and there is a trend for tools to get closer to
users by integrating with commonly used frameworks. This approach is taken
by e.g., Kontrol [7] and Halmos [5].
    In this work, we take a different approach: we bring a modeling language
closer to the users with help of automated synthesis. Such an approach could be
applied to other formal verification tools as well.

2.2   LLM Code Generation and Verification
LLMs optimized for code generation showed stunning results [17,29]. One con-
cern when using LLMs for generating code is that they are inherently stochastic
and offer no assurance that the generated code will be error-free.
    Techniques such as PICARD [30] and Synchromesh [28] utilize parsers to
sequentially filter out undesirable tokens at inference time. Synchromesh addi-
tionally introduces Target Similarity Tuning (TST), a mechanism for selecting
few-shot demonstrations for in-context learning. While TST is highly relevant for
all techniques which rely on few-shot prompting, we did not incorporate it in our
approach due to the small number of few-shot demonstrations at our disposal
and generally satisfactory performance without it. We discuss our prompting
methodology and approach to LLM-based code synthesis in Section 4.2.
    At their core, these methods enforce syntactic and a limited number of
semantic rules by restricting the token set the LLM can sample from, based
on a provided syntax. However, the rules enforceable at the parser level are
limited and require an expert to encode them. Furthermore, while correct-by-
construction synthesis is a valuable ideal, we found that code generation capabil-
ities of advanced LLMs have progressed to a point where existing inference-time
approaches, especially those that rely on syntax level guarantees, are becoming
less relevant.
    Techniques like Clover [31] cross-verify multiple LLM-generated artifacts, in-
cluding code, documentation, and formal specifications. This bears similarity to
our approach, in which the LLM generator gets feedback from other generated
parts (discussed in more detail in Section 4.3). A radically different approach
is taken by Sun et al. [32], who experiment with changing a programming lan-
guage’s grammar to make it a better fit for LLM-based generation.
6       J. Corazza et al.

   There has been a lot of interesting work with promising results combining
aspects of formal methods and LLM code generation [26,16,35,21,27,33]. Our
work fits into that broad context.


3     Preliminaries

In this section, we cover the necessary background on model-based techniques,
the Quint modeling language, and CosmWasm smart contracts, which form the
primary focus of our work.


3.1   Model-based Techniques

In the context of this paper, a model is an abstract, formal representation of
a software system that can be automatically analyzed. Common examples in-
clude 1) writing models in the TLA+ [24] modeling language and analyzing them
either by an explicit model checker TLC [36] or by a symbolic model checker
Apalache [22]; and 2) writing models in the Alloy modeling language and an-
alyzing them with the Alloy analyzer [20]. In this paper, we focus on models
written in Quint (see Section 3.2 for a brief introduction to Quint).
    Models are in general the most useful when modeling a (distributed) proto-
col before the implementation. Then, verifying the model can point to protocol
problems early in the process (or assure us that the approach makes sense). In
our auditing practice, we most often come in once the software is already imple-
mented, and we focus on finding bugs. We can use models to help us find bugs
in two ways: by verifying the code-based model, or by generating tests from the
ideal-based model.
    In the code-based approach, we write our model to be as close as possible
to the implementation. Then, finding violations of invariants with respect to
the model will correspond to finding bugs in the code. Of course, the pending
question is how we can be sure that our model corresponds to the code: this is
ensured by running model-based tests. The model generates traces, which are
then executed against the implementation to verify conformance.
    A symmetrical situation occurs in the ideal-based approach. There, we write
a model to correspond to what we understand to be the correct functioning of
the software. From the model, we generate traces which are executed against
the implementation and after each step of the trace, the state of the model is
compared to the state of the implementation. If there is a mismatch, it suggests
there is a bug in the implementation. A similar validity question is pending here,
too: how can we be sure that our model is correct? We can be assured of the
model’s correctness by writing and verifying the invariants that are expected to
hold.
    These two approaches represent somewhat extreme cases. In reality, a model,
tests, and invariants may co-evolve as our understanding of the system improves.
Furthermore, as noted already by many practitioners, one less tangible value of
writing models is that it makes our thinking about the (audited) software much
                            Synthesizing Formal Models with Tamed LLMs          7

more precise. Thus, it is very common that bugs are recognized while writing
the model, before any automatic analysis is run.


3.2   Quint

Quint [10] is a modeling language based on TLA+ [24]. Quint’s main advantage
compared to TLA+ is being significantly more in line with standard development
practice.
   It was designed according to the following principles:

 – Whenever a language concept has a “standard” syntax in mainstream lan-
   guages, Quint adopts it. Conversely, when a concept is specific to modeling
   languages, Quint’s syntax makes it explicit. As examples: Quint expresses
   inequality with != (as opposed to # and /=, used in TLA+ ); when a value
   needs to be chosen nondeterministically, Quint demands a nondet modifier.
 – Users can specify types, and types are checked as soon as possible, identifying
   mistakes sooner rather than later.
 – Indentation is encouraged with IDE tools, but does not carry meaning.
 – There is a clear separation between functions that modify the model state,
   and those that do not.
 – One can interact with parts of the model (i.e., in a REPL), before the whole
   model is finished.
 – Models written in Quint remain compatible with TLA+ and transpilation is
   possible, so all existing tools for TLA+ can be used for Quint.

    While most of these points may seem straightforward, the accepted wisdom
among TLA+ users was that a modeling language does not need to follow modern
programming practices. Even more, that trying to stay sufficiently away from
programming languages’ mores is beneficial for modeling [24].
    In our experience, Quint’s principles add value by integrating modeling into
the development process. Quint’s intuitive language and support for integration
into standard, ergonomic tools have been essential for bringing modeling into
practice.


3.3   CosmWasm Smart Contracts

CosmWasm [2] (CW) is a smart contract platform of the Cosmos ecosystem. The
name comes from the fact that CW contracts are compiled into WebAssembly
(Wasm), enabling CW contracts to be written in multiple languages (the de
facto standard programming language for CW at this point is Rust).
    A CosmWasm smart contract consists of type definitions which define how
the contract’s data is stored on the blockchain, and entry-point implementations
that operate on that data based on the messages that the contract receives.
Multiple contracts can communicate by sending each other messages, which are
all delivered and processed as part of the same transaction as the initial user’s
message.
8       J. Corazza et al.

4     Model Generation

As stated in the introduction, our goal is to generate a Quint model for a given
smart contract in three steps. In the first step, which we call mechanical gener-
ation, we use the contract’s Rust source code to determine the overall structure
of Quint model. This enables us to generate data types, function signatures, and
parts of code that follow common CosmWasm patterns, such as receiving and
replying to messages and mutating the contract’s internal state. However, we
leave placeholders, which we refer to as stubs, in place of functions that encode
the contract’s main logic. Filling these placeholders mechanically would require
one to develop a complete Rust-to-Quint transpiler, including translation of side
effects and loops, which is an exceedingly difficult task. Additionally, mechan-
ical generation would necessarily follow the Rust code by the letter, failing to
sufficiently abstract away from it. (In Figure 3 in Appendix C, we provide an
example of a stub along with the original Rust code that induced it.)
    Instead, in the second step, we prompt the LLM to complete the missing
parts of the model. In order to help the LLM accurately complete this task, we
provide it with general information about Quint, user-provided NL descriptions,
and I/O specifications. We also include relevant parts of the contract’s Rust
implementation along with results of step 1 (primarily, stubs’ signatures that
the synthesized code must adhere to). Most importantly, we provide the LLM
with few-shot examples which demonstrate how to generate Quint code.
    Finally, in the third step, we conduct a series of tests on the generated model
to ensure its correctness, and again employ the LLM to repair any identified
errors based on the error details.


4.1    Mechanical Generation for Stubs

The mechanical generation phase analyzes a CosmWasm contract written in Rust
and produces a corresponding Quint model with the overall structure, without
attempting to generally translate Rust expressions. It introduces placeholders
for the core elements that it cannot translate. It also generates an adapter test
file in Rust, which reads traces produced by the generated model and replays
them against the implementation. The tool is called cosmwasm-to-quint and
the source code is available on GitHub4 .
     This section touches on the technical aspects of Rust tooling and their ap-
plication in the generation process. Readers unfamiliar with these details may
choose to skip it, or refer to the Rust documentation5 . Furthermore, it also
touches on the structure of Quint models. Appendix F provides a quick primer
on the basic structure of Quint models.
     There are several ways to work with Rust code, from building a new parser
to using existing translation libraries. After considering a few of those options,
we chose a tool called rustc_plugin [12] for that purpose. rustc_plugin is
4
    https://github.com/informalsystems/cosmwasm-to-quint
5
    https://doc.rust-lang.org/
                                 Synthesizing Formal Models with Tamed LLMs          9

    a framework that makes it easier to add callbacks to compilation phases of
    rustc (the Rust compiler), where all the information produced by the compiler
    is available.
        Since the compiler is capable of understanding the project’s configuration
    (Cargo.toml and related files), the tool can be run for the entire project (as
    opposed to individual Rust files), which is a great convenience as CosmWasm
    projects often involve multiple files. Some projects define more than one contract,
    each one in its own Rust crate. The generation tool will generate a different
    Quint file and Rust test for each crate. A significant constraint that affects the
    transpilation at this time is the lack of import resolution for external crates. A
    potential solution for this is to download the external crates and compile them
    as well, so the definitions are compiled and compilation callbacks are called for
    them. This is not currently automated by the tool, which means any definitions
    from external crates will be undefined in the Quint model (and therefore, name
    resolution for Quint will report errors).


    Finding the contract state CosmWasm contracts have a state, and it has
    to be translated into a Quint state variable in order to be persisted between
    different transitions. Listings 1.1 and 1.2 show the input and the output of this
    process. The most complex part is finding which definitions are related to the
    state definition, and expressing their types (as Quint state variables require a
    precise type annotation). To this end, the tool scans all Rust constants and
    selects them as state variables if they satisfy all of the following conditions:

     1. the body of the constant is a call to a type with a relative path that resolves
        into a definition;
     2. the resolved definition is from a crate called “cw_storage_plus”; and
     3. the resolved definition is either “Map::new” or “Item::new”.

        If “Map::new”, the tool looks for two generic arguments to determine the type
    of the keys and the values of the map, and produces a Quint type from them.
    If “Item::new”, the tool looks for a single generic argument, which is translated
    into the corresponding Quint type.
        After collecting all state-related variable names and types, the generator will
    produce a Quint type called ContractState, defined as a record where field
    names are the variable names, and field types are their corresponding types.
    This is more convenient than generating one state variable for each of the found
    variables because it is necessary to pass this to many functions, so having the
    information stored in a single value makes it easier. The tool will always produce
    a state variable definition called contract_state with this type, and also a value
    definition called init_contract_state with the default values with which to
    initialize the contract state.
1   pub const LAST_ID : Item < u64 > = Item :: new ( " lock_id " ) ;
2   pub const LOCKUPS : Map < u64 , Lockup > = Map :: new ( " lockups " ) ;
                     Listing 1.1. Original CosmWasm state definition
    10     J. Corazza et al.

1 type ContractState = {
2   last_id : int ,
3   lockups : int -> Lockup
4}

5 var contract_state : ContractState

             Listing 1.2. Generated Quint code for the contract state


    Finding actions Quint actions define the transitions of the model, and they are
    the only kind of definition where state variables can be modified. CosmWasm
    uses values of types Deps and DepsMut to pass the state around, the latter
    allowing for it to be updated. The tool looks for the presence of those values to
    determine if a Rust function should be translated into a Quint action or just a
    pure definition (which is the Quint version of a pure function).
        When the tool generates a Quint action, it will also generate a matching
    pure definition that takes the two parameters in addition to the Rust parameters
    for the function: state: ContractState and deps: Deps parameter. In Quint,
    there is no distinction between Deps and DepsMut since there is no mutability.
    The pure definition will return the updated value of the contract state. Since
    there is no translation of the body of Rust functions, this will be a stub like the
    one in Figure 3 in Appendix C.
        The generated action itself non-deterministically picks values for all of the
    Rust function’s parameters (except for Deps), builds an execution message with
    those parameters and calls execute_message with it. execute_message is a
    helper action that non-deterministically picks additional metadata (the sender
    address, funds denomination and funds amount) and calls the execute pure
    definition, which is a direct translation of the CosmWasm execute function,
    present in every contract. This is where each message will be processed by the
    pure definition generated for it (explained in the paragraph above). At each
    step of the model, execute_message is called, its result value is assigned to the
    contract state, and the bank is updated with the funds transfer according to the
    non-deterministic funds pick.
        The bank is a separate state variable that stores the balances for each ac-
    count. On top of the bank and the contract state, the model also has a variable
    to track time, and a variable to store the last result–the returned value from
    the last entry point that was executed which, like in CosmWasm, is either an
    error or a response object (containing arbitrary attributes and any number of
    messages).

    Messages Another core feature of CosmWasm’s execution environment is how
    messages are processed. A contract is not able to directly update the bank or
    call other contracts–it does that through messages. At this point, the mechanical
    generation tool is able to handle bank messages but not general inter-contract
    communication. That is an important improvement to be made.
        Handling bank messages in the Quint model means that, at every step, if
    there is a message in the last execution’s response, the step should consist of
                            Synthesizing Formal Models with Tamed LLMs        11

processing that message instead of another execution call. It then updates the
bank with the corresponding data inside the message and removes it from the
set of messages in the response state variable.
    The same concept can be applied for inter-contract communication, as that
interaction is also done by including a message in the response. There is ad-
ditional complexity in processing these messages because it involves other con-
tract’s state and types.

Generated adapter With the goal of bridging the gap between the Quint
model and the CosmWasm code, the generator tool produces an adapter file.
This is a Rust test that reads JSON traces produced by Quint tooling and
reproduces each step of the trace in the CosmWasm contract, using the testing
library cw_multi_test [4], which defines helpers to interact with the contract.
If the trace can be reproduced successfully, and the states after each execution
match, it is evidence that the set of behaviors defined by Quint model is also
defined in the implementation. This test can be run for an arbitrary number of
traces—the larger the number of traces we generate, the higher our confidence
is that the implementation conforms to the model.

4.2   LLM-based Synthesis for Contract Logic
In this phase of the generation, we instruct the LLM to complete the Quint stubs,
i.e., the partial model with placeholders in place of functions that implement
the contract logic. In addition to the stubs that resulted from the mechanical
generation phase, we assume that the following three types of inputs will be
made available by the user.

1. CosmWasm source code, which contains the data structures that the contract
   stores on the blockchain, Rust implementations of message handlers, and
   helper data structures such as possible error formats.
2. Natural-language descriptions of the functionality that each stub is supposed
   to encode, which will steer the LLM’s output towards Quint code that cor-
   rectly captures the contract logic.
3. Two input-output specifications for each placeholder, which will be used to
   steer generation, and repair the generated code in case of errors.

    The result of the mechanical generation phase is a Quint model with “stubs”
in place of implementations of pure Quint functions that capture the function-
ality of the smart contract message handlers. They correspond to CosmWasm
message handlers in the contract’s Rust source code (and any utility functions
that they may use). Stubs are pure Quint functions that are intended to capture
the main contract logic. Pure functions are defined solely by their input-output
behavior and have no side effects, i.e., they do not modify or read any external
state implicitly, nor perform any I/O operations. The core idea of our approach
is to factorize the complex task of generating an entire model into a set of more
tractable pure function synthesis tasks. Crucially, the LLM may complete each
12       J. Corazza et al.

stub independently of others. This also applies to testing and repairing the gen-
erated implementations.
    Relying on this factorization, we provide a pseudocode outline for our LLM-
based synthesis method in Algorithm 1. This pseudocode is run for each of the
stubs. In Section 4.2 (In-Context Learning) we explain how the LLM is prompted
to generate the code for a particular stub. We explain the final phase of testing
and repairing each generated implementation in Section 4.3. Throughout this
work, we sample the LLM using a temperature of 0.6 and a top-p value of 0.7.
Our implementation of LLM-based synthesis is available on GitHub.6


Algorithm 1 LLM-Based Synthesis and Repair (Single Stub)
Require: partialModel, cosmWasmSource, nlDescriptions, ioExamples, stubName,
   stubDescription
1: prompt     ←    GeneratePrompt(stubName,       stubDescription, ioExamples,
   cosmWasmSource, partialModel )
2: code ← CallLLM(prompt)
3: stub ← Extract(stubName, partialModel )
4: filledStub ← Replace(partialModel, stub, code)
5: return
   TestAndRepair(stubName, ioExamples, filledStub)




In-Context Learning It is well-understood that large language models are
capable of in-context learning [15], i.e., learning from examples prepended to
the main prompt. Instead of fine-tuning the LLM on a downstream task such as
code generation, which is a slow and data-hungry process, one may improve the
model’s performance by seeding the context window with a number of example
tasks, along with solutions that demonstrate the desired output.
    This format of providing few-shot examples which facilitate in-context learn-
ing is commonly accepted by LLM APIs natively in the form of a messaging
API. Each message in OpenAI’s Chat Completions API is tagged as either a
system message, which is used to provide general instructions or set the tone of
the conversation, user message which contains the user query in the form of a
question, or an assistant message, demonstrating the expected answer.
    The final message in the sequence is commonly a user message containing
the desired prompt that the LLM is supposed to answer in the style of preceding
messages. Figure 2 illustrates the structure of our in-context learning prompt
format when generating based on a stub called claim_rewards (a part of CTF-
09), demonstrating the sequence of system message, few-shot examples, and the
final user query.

6
     https://github.com/informalsystems/FuzzMo/
                               Synthesizing Formal Models with Tamed LLMs                            13

         System message
         Q1: “Generate CTF-01, instantiate”




                                                                           Few-shot demonstrations
         A1: code for CTF-01, instantiate
         Q2: “Generate CTF-01, deposit”
         A2: code for CTF-01, deposit
         Q3: “Generate CTF-01, withdraw”
         A3: code for CTF-01, withdraw
         Q_user: “Generate CTF-09, claim_rewards”


Fig. 2. Message format illustrating the use of few-shot examples for in-context learning.


    In our few-shot examples, each question emulates a user asking the model to
generate a particular Quint pure function that encapsulates the logic of a message
handler found in CTF-01 (instantiate, deposit, or withdraw). The answer,
emulating the LLM’s response, is the correct implementation taken from our
hand-crafted model for CTF-01. A partial template we use to create the question
prompts is provided in Listing 1.3 (see Appendix E.1 for the full version). We
use the same template to format the final user prompt, containing the query for
the target Quint function of the model we are currently generating.
    As shown by our experimental evaluation, presented in part in Table 1, this
prompting style resulted in highly successful initial generations, frequently elim-
inating the need for further repair steps. We hypothesize that this high success
rate is due to two key factors. First, the mechanical generation phase manages
a significant portion of the task, reducing the potential for errors that would
otherwise burden the LLM. Second, we enrich the LLM’s context window with
highly relevant information derived from analyzing generated stubs and the Rust
source code of the contract.
Please complete this stub for my ‘@@@NAME@@@‘ Quint function.
@@@DESCRIPTION@@@
‘‘‘
@@@STUB@@@
‘‘‘
Here is the contract state type and related types:
‘‘‘
@@@QUINT TYPE DEFINITIONS@@@
‘‘‘
<omitted>
The ‘@@@NAME@@@‘ Quint function models a CosmWasm Rust function for
processing smart contract messages.
@@@MESSAGE HANDLER@@@
Your Quint code must be functional.
All function arguments are immutable, and you can not use mutable
variables.
14     J. Corazza et al.

@@@IO EXAMPLES@@@
                    Listing 1.3. Partial user prompt template

    In the template from Listing 1.3, the @@@NAME@@@ macro expands to the stub
(pure function) name, such as withdraw, as demonstrated in the third few-shot
example for CTF-01 in Figure 2. The @@@DESCRIPTION@@@ macro expands to
the user-provided natural language description of the stub’s intended function-
ality, as illustrated in Listing 1.4 for the withdraw stub in CTF-01. We obtain
the expansion for @@@QUINT TYPE DEFINITIONS@@@ by analyzing the output of
the mechanical generation phase. Starting from the function signature of the
placeholder at hand, we recursively look up relevant type definitions in the stub
model’s Quint source code.
    Coupled with a Quint cheatsheet with a list of commonly used operations
that we always include in the system message, this provides the LLM with useful
and targeted knowledge to execute complex operations on data and implement
the desired functionality for a particular stub.
    In order to expand the @@@MESSAGE HANDLER@@@ macro, we search the con-
tract’s CosmWasm source code for a block of Rust code that is a function def-
inition beginning with pub fn <stub name>. Our mechanical generation tool
guarantees that this function (the message handler which induced the place-
holder) exists in the Rust source files.
    Finally, the @@@IO EXAMPLES@@@ macro expands to the input-output specifi-
cations provided by the user. (In our evaluation, we supply the LLM with two
input-output specifications.) The full version of this template can be seen in
Listing 1.19 in Appendix E.
"Enable users to withdraw from valid lockups, updating the state, or
return an error if validation fails."
        Listing 1.4. User-provided description for CTF-01, withdraw stub



Adapter Generation for Model-based Testing As explained in Section 3.1,
model-based testing involves executing traces, sequences of state transitions gen-
erated by the model, against the implementation. An adapter is a Rust test which
accomplishes this, but writing one manually is a time-consuming task. In order
to fully automate a model-based testing workflow, we generate an adapter by
following a procedure similar to the one outlined throughout Section 4: a base-
line test which executes the trace can be generated mechanically, but we use an
LLM to synthesize the state comparison function, a part of the adapter which
checks whether contract states correspond with state transitions in the model.
    While a trivial state comparison function can be mechanically generated
(e.g., one that always returns true), we leverage the LLM’s instruction-following
capabilities to generate a function that performs a more thorough inspection of
the smart contract’s state. If we detect errors in the generated adapter code,
we trigger a repair loop similar to the one we outline for model generation in
the next section. In Appendix A, we conduct a case study for the model-based
                             Synthesizing Formal Models with Tamed LLMs          15

testing workflow supported by adapter generation, and relegate the technical
details to Appendix D.


4.3   Testing and Repair Phase

In this section, we outline our strategy for addressing potential errors that arise
during generation. As highlighted in Section 4.2, we independently repair each
function in the model. Because we never generate code with side effects, it suffices
that the generated code correctly implements the intended behavior for all I/O
specifications. This stems from the fact that the model’s overall structure and
state management code have been generated deterministically. We divide errors
into three distinct categories, based on the earliest point at which they can be
detected, namely

 1. static errors (e.g., incorrect Quint syntax), which are detected before exe-
    cuting any tests;
 2. runtime errors (e.g., calling a nonexistent method), which are detected
    when the generated is executed; and
 3. semantic errors, which are detected once the generated pure function re-
    turns an output that is inconsistent with a user-provided input-output spec-
    ification.

    After the initial generation is completed, we analyze it for the presence of
either static, runtime, or semantic errors. If we detect them, our strategy is to
enter a loop of test-and-repair rounds, as shown in Figure 1. In each round, we
gather relevant information about the probable cause (such as error messages)
and construct a prompt asking the LLM to repair the code based on this context.
The LLM’s response then replaces the previous, erroneous fragment of code, and
we check the new version for correctness again.
    In order to prevent an unbounded number of LLM calls, we define a finite
repair round “budget” for each error category: the amount of times the system
may invoke an LLM to repair a particular type of error. In all of our experiments,
we use a budget of 3 repair rounds for each error category, leading to a maximum
of 9 additional LLM calls.
    Although this approach does not guarantee an error-free result, in practice we
have found it sufficiently capable of achieving our goal: reducing the developer
time necessary to utilize Quint models. As shown in our experimental evaluation,
in most runs we were able to successfully generate correct code for most target
functions and contracts in our benchmark, using fewer than 3 rounds of repair
on average. We outline the pseudocode for this phase (the TestAndRepair
function in Algorithm 1), in Algorithm 2 of Appendix B.1.
    In the following two sections, we further explain the static and semantic
repair rounds. When repairing runtime errors, we use a combination of methods
and prompts employed for static and semantic errors (details in Appendix B.2).
16      J. Corazza et al.

Static Errors To detect static errors, we utilize Quint’s type checking tool
(which will, naturally, also detect syntax errors). An example of this tool’s output
when detecting a syntax error is presented in Listing 1.5. This error occurred
during code generation for a stub named execute_add_strategy in our real-
world Neutron DAO case study.
    Quint being a new language means that commercial LLMs lack comprehen-
sive information on Quint-specifics. The error in Listing 1.5 arises from the new
and limited pattern matching syntax in Quint. The generated code attempts to
pattern-match on literal values, a valid pattern in many languages that support
this feature. However, as the error message points out, this is not yet supported
in Quint. (In this case, a parser-informed method such as PICARD [30] would
prove valuable.)
    Using our repair prompting methodology, the LLM is able to correctly reason
about the root cause of the error, and subsequently produces correct Quint code.
Although we lack a dataset of few-shot examples suitable for our repair phase, we
compensate by instructing the LLM to start the solution with reasoning about
the problem before writing any code [34]. For brevity, we omit the corrected
code, and instead showcase the LLM’s reasoning in Listing 1.6. The template we
use to generate static repair prompts can be found in Appendix E.2.

[...] quint / model_generated . qnt :86:20 - error : [ QNT000 ]
mismatched input ’ true ’ expecting { ’_ ’ , LOW_ID , CAP_ID }
86:     | Ok ( true ) = > ( Err (" Cannot remove last administrator ")
, state )
               ^^^^

[...] quint / model_generated . qnt :87:20 - error : [ QNT000 ]
mismatched input ’ false ’ expecting { ’_ ’ , LOW_ID , CAP_ID }
87:     | Ok ( false ) = > (
               ^^^^^

                     Listing 1.5. Static error in Neutron DAO

2. **Mismatched input ’true’ expecting {’_’, LOW_ID, CAP_ID}**: This
error indicates that the use of the boolean literals ‘true‘ and ‘false‘
directly in pattern matching is not allowed in Quint.
3. **Mismatched input ’false’ expecting {’_’, LOW_ID, CAP_ID}**: Similar
to the previous error, the use of the boolean literal ‘false‘ directly in
 pattern matching is not allowed.
                            Listing 1.6. LLM reasoning



Semantic Errors After embedding the synthesized function into the mechani-
cally generated stub file and confirming it passes type checking, we verify whether
it respects the user-provided I/O specifications.
    Let F denote the true Quint pure function that implements a particular part
of the contract’s logic in the model. In this setting, F is unknown, and we only
                             Synthesizing Formal Models with Tamed LLMs           17

assume access to K ∈ N user-provided I/O specifications (K ≥ 2), and F̃ , the
LLM’s completion for a stub of F . Mechanical generation guarantees that F and
F̃ share the same type signature (arguments and return type), and we require
that F̃ must pass type checking before semantic repair rounds are triggered.
Thus, we may call F̃ with arguments suitable for F , and if F̃ returns, the return
value will be comparable with the return value of F .
    Semantic repair rounds run only if there are no runtime errors. Each I/O
specification is represented as a pair (argsi , Ri ) (1 ≤ i ≤ K), where argsi denotes
the arguments applied to F or F̃ (the user-specified input), and Ri = F (argsi )
denotes the expected return value (the user-specified output). We identify a
semantic error if F̃ (argsi ) ̸= Ri for a given i. In that case, we start a semantic
repair round by preparing a specialized prompt, employing a template similar
to the one used for static errors.
    We provide to the LLM (1) argsi , the user-specified input data; (2) F̃ (argsi ),
the incorrect output of the current implementation; and (3) Ri , the user-specified
expected output. Of course, just as in a static repair round, the prompt also
contains other information such as the erroneous implementation (F̃ ). In this
way, we provide sufficient information to correct the function’s behavior at a
number of points in the input space, and we rely on the LLM’s generalization
capabilities to enhance the overall correctness.


5     Evaluation

In Section 5.1, we evaluate our Quint model generation technique on a bench-
mark consisting of 5 smart contracts from the CosmWasm Capture the Flag
repository and present summary results. In Appendix C, we present more com-
prehensive results for the entire benchmark, and perform a limited ablation study
investigating the effect of natural language descriptions on performance across
the CTF Benchmark.
   In Section 5.2, we present a case study applying our method to a real-world
audit scenario. An additional case study, capturing the full model-based testing
workflow, can be found in Appendix A.


5.1   Benchmark: CosmWasm Capture the Flag

The CosmWasm Capture the Flag (CTF) repository provides the source code for
10 smart contracts used in a capture-the-flag competition. Each smart contract
in the repository contains a critical bug, and the goal in a CTF competition is to
find the bug and craft an exploit around it. For example, in CTF-01, users may
deposit funds into a lockup, and withdraw funds from lockups by specifying a
lockup ID. The bug can be found in the withdraw message handler, which does
not check if the same lockup ID appears multiple times in the message, enabling
users to withdraw all funds from the same lockup twice, and thus steal funds
from the contract. We focused our benchmark on contracts from the CosmWasm
CTF repository where the vulnerability is caused by a bug in program logic
18      J. Corazza et al.

rather than by a technical or platform-dependent reason, making Quint models
useful for detecting the issue.
    Our benchmark consists of 23 target functions, drawn from our hand-crafted
reference Quint models for CTFs 02, 04, 05, 07, and 09. We used the CTF-
01 contract and its model for in-context learning, as described in Section 4.2:
we crafted a series of Question-Answer pairs, each pair demonstrating how to
fulfill the task of generating implementations (Answer) given Quint placeholders
(Question).
    Furthermore, we wrote a natural-language description of each target function,
along with 5 I/O examples. We use 2 I/O examples to emulate a user’s input,
and the remaining 3 as a partial specification for post-generation inspection.
(Each function was additionally manually inspected for correctness.)
    In this benchmark, our tool generated and repaired a Quint model for each
of the contracts. To manage stochasticity inherent in LLM outputs, we repeat
this experiment across 5 independent runs. We made a best-effort attempt to
maximize the reproducibility of our experiments. In addition to a frozen model
checkpoint, we provide timestamps, system fingerprints, and the seeds used for
all LLM API calls.
    We present the results of our benchmark for CTF-04 and 09 in Table 1,
showing that the final, post-repair, results generate a function that satisfies the
supplied I/O specification in almost all runs (indicated by the green checkmark
in the first column). Full results can be found in Appendix C, in Table 3.
    We supply the first two I/O examples as part of the initial generation request,
and to perform test-and-repair rounds. The column Avg. Repair indicates the
average number of repair rounds (static, runtime, and semantic) that were used
for generating each function. If the generated code contains no runtime errors,
we evaluate the functions on the remaining three I/O examples, that the LLM
did not have access to during generation, and report the results as the Pass
Rate.


Table 1. Average number of repair rounds used per function and pass rates for unseen
test cases, averaged across 5 independent runs for CTF-04 and CTF-09

                                     CTF-04
                      Function          Avg. Repair             Pass Rate
         ✓           instantiate            0.0                   100%
         ✓              mint                1.2                    90%
         ✓              burn                0.0                   100%
                                     CTF-09
                      Function           Avg. Repair            Pass Rate
       ✓               deposit               2.4                   73%
     ? (4/5)          withdraw               1.6                   73%
       ✓           increase_reward           0.2                  100%
     ? (4/5)        claim_rewards            1.8                   80%
                             Synthesizing Formal Models with Tamed LLMs         19

   To provide a clearer view of each contract’s difficulty, Table 2 details the
total number of repair rounds performed per contract, categorized by type of
repair.


               Table 2. Distribution of error repair rounds by type

                    Contract Static Runtime Semantic Σ
                     CTF-02     0      0       3      3
                    CTF-04      1      5       0     6
                     CTF-05     0      0       0      0
                     CTF-07     4      0       0      4
                    CTF-09     23      0       7     30



   More detailed results can be found in Appendix C. They follow the trends
described in this section and provide one additional insight: the quality of the
NL description degrades the performance only slightly, allowing the method to
work well even if the user fails to provide a precise description.

5.2   Case Study: Privileged subDAO Contract
In this case study, we applied the described approach to a project from one of
the audits that Informal performed recently. The scope of the audit was a new
functionality of Neutron’s [9] governance contracts. To provide sufficient context,
let us describe the basic concepts of on-chain governance.
    Most blockchains, including Neutron, typically do not have a single chain
owner. Instead, the chain is jointly owned and governed by all the token holders.
Any user may create a governance proposal, and the token holders vote for or
against it. If there is sufficient support for the proposal, it gets automatically
executed on the chain. We call such an organizational structure a decentralized
autonomous organization (DAO).
    The whole governance process, from proposal creation to its execution, takes
a non-negligible amount of time. Furthermore, some proposals may be very tech-
nically specialized (e.g., regular adjustment of particular chain parameters) and
thus not sufficiently interesting for members of the DAO. To address these issues,
the newly added functionality introduced the concept of a privileged subDAO:
a smaller set of users authorized to vote in and execute specific changes only
(before execution, the decision can still be overridden by members of the main
DAO).
    The functionality is implemented in the neutron-chain-manager contract.
Different subDAOs can either have an AllowAll authorization (typically, for the
main or security DAO, which can do anything) or an AllowOnly([Permission])
authorization, which specifies a set of permissions that a subDAO can exe-
cute. The relevant entry point functions of the contract are AddStrategy (which
gives an authorization to a subDAO), RemoveStrategy (which removes it), and
ExecuteMessages (which executes a message if it has authorization to do so).
20       J. Corazza et al.

Overall, the contract contains 16 functions that together implement the desired
functionality.
    The main property that needs to be preserved is the following: ExecuteMessages
that attempts to execute a message for which the sender subDAO does not have
permission will fail. Unfortunately, in the audited commit, the property was not
satisfied. The problem was identified through manual code analysis and fixed for
the release.

Identifying the bug using model generation We took the code at the audit
commit and wanted to see if we could find the same bug using model generation.
We first applied the mechanical generation step described in Section 4.1, and
then the model generation described in Section 4.2. The artifacts resulting from
this case study are available on GitHub.7
    Mechanical generation reliably produced stubs as expected. There was some
additional cleanup work needed: removing references to external libraries or un-
used types, and removing stubs for contracts that were out of scope. Further-
more, some adjustment was needed for handling message passing of the custom
NeutronMsg type. Overall, the effort to go from the generated version to a work-
ing model stub was neither trivial nor too big.
    Out of 16 functions that there were in the contract, we identified 6 of them
relevant for deciding on the correct authorization. For those 6 functions, we ran
the model generation process.
    Out of 6 functions, 4 were immediately generated correctly. The remaining
two functions were fixed with syntactic repair. The problem was that at the first
attempt, there were issues in calling functions within the generated code (once
the name was hallucinated, and once the order of parameters did not match the
signature).
    One interesting observation compared to the reference model (a model writ-
ten by the authors manually): at a couple of places we had to make sure that
a property holds for all elements of a list. Thus, we factored that functional-
ity out and wrote the helper function listforall (following the naming of the
equivalent function on sets, forall). The generated model, since it always gen-
erates only one function at a time (without the possibility of creating helper
functions), generated expressions that were more complicated compared to the
reference implementation.
    Finally, the generated Quint model sufficed to uncover the authorization bug
that existed in the contract. This presents the main takeaway of the case study:
the presented approach could indeed be used in a real-world audit.
    Beside the main takeaway, there are a couple of peculiarities worth comment-
ing on. First, we see that there was no need for semantic repair of generated
model functions. This is because the authorization mostly depends on getting
the types right, and the logic is fairly simple.
    Second, because our model stub ensures full generality handling CosmWasm
bank transfers, and the analyzed contracts did not include any, the whole model
7
     https://github.com/informalsystems/fuzzmo_use_case2/
                             Synthesizing Formal Models with Tamed LLMs          21

ended up less readable than a model an experienced Quint user would have
written by hand. The tradeoff is then between ease of modeling and ease of
reading. Because these models are used for bug finding, and not for protocol
documentation (which is another use case for Quint models), we find that making
modeling easier is the right choice for all but the most proficient Quint modelers.
Contrary to the full generality of mechanically generated stubs, we found the
LLM-generated parts of the models to be written in a very natural way.
   There are two caveats regarding the optimistic takeaways of this section.
First, our method presents the core around which an ergonomic, user-friendly
tool should be built. Second, generalizing the method to smart contract envi-
ronments other than CosmWasm would require separate design process for the
stub generation part.


6   Conclusion
In this paper, we reported on our effort to bridge the gap between model-based
techniques and software auditing practice. We did so by automatically gener-
ating both Quint models and model-based tests, taking a CosmWasm contract,
I/O examples, and a high-level description as input. We demonstrated how our
technique is able to generate correct models on a capture-the-flag benchmark,
and ran a successful case study on a past audit.
    Our experience shows that LLMs can be tamed by using mechanical gener-
ation for setting up a firm frame for statistical code generation. Iterated repair
attempts (syntactic, semantic, and runtime) were useful for correcting the LLM’s
occasional hallucinations. While the proposed method does not guarantee cor-
rectness, our evaluation shows that it works well in practice. Furthermore, at
every step of the generation process (model stubs, models, test stubs, tests), the
method provides useful artifacts for the users, which is very much appreciated
by practitioners.
    There are still aspects of our technique that need to be improved if we want
to make it fully practical. Currently, the input-output examples we expect from
users are encoded as Quint files with Quint syntax. Providing a better user
experience there would go a long way to bring our technique to a broader audi-
ence. Additionally, mechanical generation, while fully reliable, is still restricted
to CW contracts that do not send messages among themselves. This limits the
applicability of the technique to simpler contracts.
    The main practical benefit of our approach is easing auditors’ way into using
model-based techniques—a task with a very steep learning curve prior to having
our tool available.
22      J. Corazza et al.

References

 1. Certora prover, https://www.certora.com/prover
 2. Cosmwasm book, https://book.cosmwasm.com/
 3. Cosmwasm capture the flag competition tasks, https://github.com/
    oak-security/cosmwasm-ctf
 4. cw-multi-test cosmwasm testing framework, https://github.com/CosmWasm/
    cw-multi-test
 5. Halmos code repository, https://github.com/a16z/halmos
 6. Jepsen, https://jepsen.io
 7. Kontrol code repository, https://github.com/runtimeverification/kontrol
 8. Mythril code repository, https://github.com/Consensys/mythril
 9. Neutron github org, https://github.com/neutron-org
10. Quint, https://quint-lang.org/
11. Reference implementation of eth2.0 in dafny, https://github.com/ConsenSys/
    eth2.0-dafny
12. Rustc plugin, https://github.com/cognitive-engineering-lab/rustc_plugin
13. Slither code repository, https://github.com/crytic/slither
14. Tla+ ibc specifications, https://github.com/informalsystems/hermes/tree/
    master/docs/spec/tla
15. Brown, T.B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., Nee-
    lakantan, A., Shyam, P., Sastry, G., Askell, A., Agarwal, S., Herbert-Voss, A.,
    Krueger, G., Henighan, T., Child, R., Ramesh, A., Ziegler, D.M., Wu, J., Win-
    ter, C., Hesse, C., Chen, M., Sigler, E., Litwin, M., Gray, S., Chess, B., Clark,
    J., Berner, C., McCandlish, S., Radford, A., Sutskever, I., Amodei, D.: Language
    models are few-shot learners. CoRR abs/2005.14165 (2020), https://arxiv.
    org/abs/2005.14165
16. Charalambous, Y., Tihanyi, N., Jain, R., Sun, Y., Ferrag, M.A., Cordeiro, L.C.:
    A new era in software security: Towards self-healing software via large language
    models and formal verification. arXiv preprint arXiv:2305.14752 (2023)
17. Chen, M., Tworek, J., Jun, H., Yuan, Q., de Oliveira Pinto, H.P., Kaplan, J.,
    Edwards, H., Burda, Y., Joseph, N., Brockman, G., Ray, A., Puri, R., Krueger,
    G., Petrov, M., Khlaaf, H., Sastry, G., Mishkin, P., Chan, B., Gray, S., Ryder, N.,
    Pavlov, M., Power, A., Kaiser, L., Bavarian, M., Winter, C., Tillet, P., Such, F.P.,
    Cummings, D., Plappert, M., Chantzis, F., Barnes, E., Herbert-Voss, A., Guss,
    W.H., Nichol, A., Paino, A., Tezak, N., Tang, J., Babuschkin, I., Balaji, S., Jain,
    S., Saunders, W., Hesse, C., Carr, A.N., Leike, J., Achiam, J., Misra, V., Morikawa,
    E., Radford, A., Knight, M., Brundage, M., Murati, M., Mayer, K., Welinder, P.,
    McGrew, B., Amodei, D., McCandlish, S., Sutskever, I., Zaremba, W.: Evaluating
    large language models trained on code. CoRR abs/2107.03374 (2021)
18. Dias Neto, A.C., Subramanyan, R., Vieira, M., Travassos, G.H.: A survey on model-
    based testing approaches: a systematic review. In: Proceedings of the 1st ACM
    international workshop on Empirical assessment of software engineering languages
    and technologies: held in conjunction with the 22nd IEEE/ACM International
    Conference on Automated Software Engineering (ASE) 2007. pp. 31–36 (2007)
19. Groce, A., Grieco, G.: echidna-parade: A tool for diverse multicore smart contract
    fuzzing. In: Proceedings of the 30th ACM SIGSOFT International Symposium on
    Software Testing and Analysis. pp. 658–661 (2021)
20. Jackson, D.: Software Abstractions: logic, language, and analysis. MIT press (2012)
                               Synthesizing Formal Models with Tamed LLMs             23

21. Jain, N., Vaidyanath, S., Iyer, A.S., Natarajan, N., Parthasarathy, S., Rajamani,
    S.K., Sharma, R.: Jigsaw: Large language models meet program synthesis. In:
    ICSE. pp. 1219–1231. ACM (2022)
22. Konnov, I., Kukovec, J., Tran, T.: TLA+ model checking made symbolic. Proc.
    ACM Program. Lang. 3(OOPSLA), 123:1–123:30 (2019)
23. Lamport, L.: The temporal logic of actions. ACM Trans. Program. Lang. Syst.
    16(3), 872–923 (1994)
24. Lamport, L.: Specifying Systems, The TLA+ Language and Tools for Hardware
    and Software Engineers. Addison-Wesley (2002)
25. Leino, K.R.M.: Accessible software verification with dafny. IEEE Softw. 34(6),
    94–97 (2017), https://github.com/dafny-lang/dafny
26. Meng, R., Mirchev, M., Böhme, M., Roychoudhury, A.: Large language model
    guided protocol fuzzing. In: Proceedings of the 31st Annual Network and Dis-
    tributed System Security Symposium (NDSS) (2024)
27. Misu, M.R.H., Lopes, C.V., Ma, I., Noble, J.: Towards ai-assisted synthesis of
    verified dafny methods. arXiv preprint arXiv:2402.00247 (2024)
28. Poesia, G., Polozov, A., Le, V., Tiwari, A., Soares, G., Meek, C., Gulwani, S.:
    Synchromesh: Reliable code generation from pre-trained language models. In: In-
    ternational Conference on Learning Representations (2022), https://openreview.
    net/forum?id=KmtVD97J43e
29. Rozière, B., Gehring, J., Gloeckle, F., Sootla, S., Gat, I., Tan, X.E., Adi, Y., Liu,
    J., Remez, T., Rapin, J., Kozhevnikov, A., Evtimov, I., Bitton, J., Bhatt, M.,
    Canton-Ferrer, C., Grattafiori, A., Xiong, W., Défossez, A., Copet, J., Azhar, F.,
    Touvron, H., Martin, L., Usunier, N., Scialom, T., Synnaeve, G.: Code llama: Open
    foundation models for code. CoRR abs/2308.12950 (2023)
30. Scholak, T., Schucher, N., Bahdanau, D.: PICARD: parsing incrementally for con-
    strained auto-regressive decoding from language models. CoRR abs/2109.05093
    (2021), https://arxiv.org/abs/2109.05093
31. Sun, C., Sheng, Y., Padon, O., Barrett, C.: Clover: Closed-loop verifiable code
    generation (2024), https://openreview.net/forum?id=oSuVEv4X7w
32. Sun, Z., Du, X., Yang, Z., Li, L., Lo, D.: Ai coders are among us: Rethinking
    programming language grammar towards efficient code generation. In: Proceedings
    of the 33rd ACM SIGSOFT International Symposium on Software Testing and
    Analysis. pp. 1124–1136 (2024)
33. Wang, R., Zhang, J., Jia, Y., Pan, R., Diao, S., Pi, R., Zhang, T.: Theo-
    remllama: Transforming general-purpose llms into lean4 experts. arXiv preprint
    arXiv:2407.03203 (2024)
34. Wei, J., Wang, X., Schuurmans, D., Bosma, M., Chi, E.H., Le, Q., Zhou, D.:
    Chain of thought prompting elicits reasoning in large language models. CoRR
    abs/2201.11903 (2022), https://arxiv.org/abs/2201.11903
35. Ye, X., Chen, Q., Dillig, I., Durrett, G.: Optimal neural program synthesis from
    multimodal specifications. arXiv preprint arXiv:2010.01678 (2020)
36. Yu, Y., Manolios, P., Lamport, L.: Model checking tla+ specifications. In:
    CHARME. Lecture Notes in Computer Science, vol. 1703, pp. 54–66. Springer
    (1999)
24      J. Corazza et al.

A     Case Study: Model-based Testing Workflow
We conducted a case study of the model-based testing workflow—which includes
both model generation and adapter generation—on two smart contracts, CTF-
02 and 04. First, we simulated Quint models generated as part of the benchmark
from Section 5.1 to obtain traces. We then generated adapters that can execute
these traces, as discussed in Section 4.2. In Appendix D we provide further details
on the adapter generation process in this case study, including examples of state
comparison functions synthesized with our LLM-based method.
   Listing 1.7 shows the output produced by our synthesized adapter for CTF-
02 while processing a trace generated by our synthesized model of the contract.
As can be seen, the test compiles and successfully starts executing the trace,
but fails after two steps, uncovering a bug. The test fails due to a withdraw
message in the trace sent from an unrecognized address. The Quint model is
able to handle this situation gracefully, while the CosmWasm implementation
panics. This difference between the model and the implementation points to a
vulnerability in the code.
Step number : Some (0)
Result from trace : Ok ( Response { messages : [] , attributes : [
Attribute { key : " action " , value : FromStr (" instantiate ") }]
})
Initializing contract .
Message : InstantiateMsg
Sender : Addr (" admin ")
Funds : []
Contract balance ( Addr (" contract0 ") ) for uawesome : Uint128
(200) vs Uint128 (200)
clock is advancing for 1 seconds
-----------------------------------
Step number : Some (1)
Result from trace : Err (" Unauthorized ( Withdraw ) ")
Message : Withdraw { amount : Uint128 (32) }
Sender : Addr (" contract0 ")
Funds : [ Coin { 77 " d1 " }]
thread ’ tests :: model_test ’ panicked at src / contract . rs :68:66:
called ‘ Result :: unwrap () ‘ on an ‘Err ‘ value : NotFound { kind :
 " type : o a k s e c u r i t y _ c o s m w a s m _ c t f _ 0 2 :: state :: UserInfo ; key :
[00 , 0C , 76 , 6F , 74 , 69 , 6E , 67 , 5F , 70 , 6F , 77 , 65 , 72 , 63 ,
6F , 6E , 74 , 72 , 61 , 63 , 74 , 30]" }

                        Listing 1.7. Adapter output (CTF-02)

    Each CTF contract is designed to demonstrate only a specific exploit, and
they do not implement handling of various edge-cases such as this. Thus, this
was an easy catch for the model-based testing workflow we envisioned, which
replaces hours of careful code inspection. By iteratively fixing all the differences
between the code and model, we can eliminate all the bugs in the contract,
including the main vulnerability.
                            Synthesizing Formal Models with Tamed LLMs         25

    Another approach to achieving the same goal (uncovering the main vulnera-
bility) is to modify the adapter so as to catch the panics raised by the contract
under test, verify that they correspond to the errors predicted by the model,
and if so, ignore them and carry on with processing the trace. Although this
approach is less natural than correcting the model itself, we chose to follow it
so as to minimize changes to our dataset (the CTF benchmark). We cover this
process in the following section.


A.1   Uncovering the Main Vulnerability in CTF-02

The exploit in CTF-02 is triggered when an attacker attempts to unstake (re-
claim) more funds than they had originally staked. In a testing environment,
an overflow error will occur in this scenario, reverting the transaction. This may
give developers false confidence that the exploit will similarly be prevented when
executing on-chain. However, the core idea of the vulnerability is that overflow
checks will be disabled in the release version of the contract, making it easier
for developers (who primarily work within the testing environment) to overlook
this bug.
    In order to uncover this vulnerability, we needed to accommodate the gen-
erated adapter from the previous section to be more resilient against contract
panics, such as the one from Listing 1.7. Specifically, we modified the adapter
to unwind particular panics raised by CTF-02 (e.g., if an unrecognized token
denomination is received in a deposit message). In that case, we ensured that
corresponding transitions in the trace also report an error of the same kind in
the model (otherwise, we would not be alerted to a worrying mismatch between
the model and the implementation).
    These modifications allowed the adapter to progress further and process more
steps of the trace, up until discovering the main vulnerability. As can be seen in
Listing 1.8, the adapter processed 14 steps of the trace and eventually encoun-
tered an inconsistent state, thus uncovering the vulnerability.

Step number : Some (14)
Result from trace : Err (" Insufficient voting power ( Unstake ) ")
Message : Unstake { unlock_amount : 194 }
Sender : Addr (" sender3 ")
Funds : [ Coin { 29 " uawesome " }]
thread ’ tests :: model_test ’ panicked at tests /
c o n t r a c t _ m o d e l _ t e s t _ a d a p t e r _ s t u d y . rs :172:13:
Expected action to fail with error : Some (" Insufficient voting
  power ( Unstake ) ")

                      Listing 1.8. Adapter output (CTF-04)

    In order to generate this output, one needs to run cargo test using the
--release flag. The vulnerability is uncovered by our generated adapter, which
expects the unstake action to fail, while the contract’s CosmWasm implemen-
tation simply carries on with an overflow in its arithmetic (due to the release
26       J. Corazza et al.

flag). If one leaves out the release flag, our generated adapter will still discover
the bug, but the output will be slightly different: instead of complaining about
the action succeeding, when it should have failed, this time the implementation
itself will panic because the overflow checks are present, successfully alerting the
developer of the vulnerability.

A.2      Uncovering an Unexpected Vulnerability CTF-04
Similar to our end-to-end model-based testing case study for CTF-02, when
executing a trace from the Quint model for CTF-04, our generated adapter
panics and inadvertently uncovers a bug in CTF-04. The output of this test
run in shown in Listing 1.9. In this case, the problematic state transition in
the trace involves an unrecognized token denomination. The bug is found in the
mint function of CTF-04’s Rust implementation, where the CosmWasm utility
function must_pay is called without proper error handling, resulting in a panic. 8
Step number : Some (0)
Result from trace : Ok ( Response { messages : [] , attributes : []
 })
Initializing contract .
Message : InstantiateMsg { offset : 0 }
Sender : Addr (" admin ")
Funds : []
Contract balance ( Addr (" contract0 ") ) for uawesome : Uint128
(200) vs Uint128 (200)
Contract config total_supply : Uint128 (0) vs Uint128 (0)
clock is advancing for 1 seconds
-----------------------------------
Step number : Some (1)
Result from trace : Ok ( Response { messages : [] , attributes : []
 })
Message : Mint
Sender : Addr (" sender1 ")
Funds : [ Coin { 31 " d1 " }]
thread ’ tests :: model_test ’ panicked at src / contract . rs :45:41:
called ‘ Result :: unwrap () ‘ on an ‘Err ‘ value : MissingDenom ("
uawesome ")

                        Listing 1.9. Adapter output (CTF-04)


B      Testing and Repair Phase Details
In this section, we provide additional details on the testing and repair phase
of our method that were omitted from the main paper. The pseudocode for the
testing and repair phase can be found in the following Section B.1 as Algorithm 2.
In Section B.2 we describe runtime repair rounds.
8
     https://github.com/oak-security/cosmwasm-ctf/blob/
     c32fa94947f4199596d26696afeb3de0ab3d9cca/ctf-04/src/contract.rs#L45
                                  Synthesizing Formal Models with Tamed LLMs           27

     B.1    Full Repair Algorithm Pseudocode
     We assume that GeneratePrompt calls in Algorithm 2 have access to similar
     contextual information (such as the stub name, description, and CosmWasm
     source code) as in Algorithm 1, but for the sake of brevity we do not explicitly
     state them as arguments. The full template used by GeneratePrompt calls in
     this case can be found in Appendix E.2.

     B.2    Runtime Errors
     In this section we will use the same notation as in Section 4.3, where we explain
     semantic errors: F̃ denotes the LLM-synthesized function, and (argsi , Ri ) (1 ≤
     i ≤ K) denote the K user-provided I/O specifications (argsi and Ri are the
     user-specified input and output, respectively).
         Runtime errors occur when the synthesized function F̃ attempts to execute
     illegal Quint code which was not detected by the Quint type checker (such as
     attempting to call a nonexistent method), or when certain runtime invariants
     are broken, for example if attempting to access a list with an invalid index. We
     detect this by passing all the user-provided arguments argsi , one by one, to F̃ , as
     soon as it passes type checking. If the execution of this function crashes instead
     of returning a value, we trigger a runtime repair round.
         An example of a runtime error and the synthesized Quint function that caused
     it are provided in Listings 1.10 and 1.11, respectively. As can be seen, this run-
     time error was caused by map lookup with a missing key. Finally, we provide
     the LLM’s reasoning based on the error message from Listing 1.10, including the
     repaired function, in Listing 1.12.

     runtime error : error : [ QNT507 ] Called ’get ’ with a non -
     existing key
      val user_balance = state . balances . get ( info . sender ) . amount
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

              Listing 1.10. Runtime error when running CTF-04, burn function

1 pure def burn ( state : ContractState , deps : Deps , env : Env ,
      info : MessageInfo , shares : int ) : ( Result [ Response ,
      ContractError ] , ContractState ) = {
2     val contract_balance = deps . querier . bank . get (
      CONTRACT_ADDRESS ) . get ( DENOM )
3     val total_assets = contract_balance
4     val total_supply = state . config . total_supply
5

6          // Compute the amount of assets to return
7          val asset_to_return = shares * total_assets /
           total_supply
8

9          if ( asset_to_return == 0) {
10           ( Err ( " ZeroAmountNotAllowed " ) , state )
28     J. Corazza et al.




Algorithm 2 Testing and Repair Phase
Require: stubName, ioExamples, filledStub, staticRounds, runtimeRounds, semanti-
    cRounds
 1: done ← false
 2: while not done do
 3:    done ← true
 4:    if not TypeChecks(filledStub) and staticRounds > 0 then
 5:        done ← false
 6:        staticRounds ← staticRounds - 1
 7:        typeCheckOutput ← QuintTypeCheck(filledStub)
 8:        prompt ← GeneratePrompt(filledStub, typeCheckOutput)
 9:        code ← CallLLM(prompt)
10:        filledStub ← Replace(quintStubs, stub, code)
11:        continue
12:    end if
13:    if TypeChecks(filledStub) and Crashes(stubName, ioExamples, filledStub)
    and runtimeRounds > 0 then
14:        done ← false
15:        runtimeRounds ← runtimeRounds - 1
16:        runtimeOutput ← RuntimeCheck(stubName, ioExamples, filledStub)
17:        prompt ← GeneratePrompt(filledStub, runtimeOutput)
18:        code ← CallLLM(prompt)
19:        filledStub ← Replace(quintStubs, stub, code)
20:        continue
21:    end if
22:    if not Crashes(stubName, ioExamples, filledStub) then
23:        ioIncorrect ← {}
24:        for (args, expect) in ioExamples do
25:             output ← executeQuint(stubName, args, filledStub)
26:             if output != expect then
27:                  ioIncorrect[(args, expect)] ← output
28:             end if
29:        end for
30:        if size(ioIncorrect) > 0 and semanticRounds > 0 then
31:             done ← false
32:             semanticRounds ← semanticRounds - 1
33:             prompt ← GeneratePrompt(ioIncorrect)
34:             code ← CallLLM(prompt)
35:             filledStub ← Replace(quintStubs, stub, code)
36:        end if
37:    end if
38: end while
                                   Synthesizing Formal Models with Tamed LLMs       29

11         } else {
12            val user_balance = state . balances . get ( info . sender ) .
           amount
13

14             if ( user_balance < shares ) {
15               ( Err ( " unsigned int error " ) , state )
16             } else {
17               val updated_user_balance = user_balance - shares
18               val updated_total_supply = total_supply - shares
19

20              val updated_balances = state . balances . put ( info . sender
           , { amount : updated_user_balance })
21              val updated_state = { ... state , config : {
           total_supply : updated_total_supply } , balances :
           updated_balances }
22

23               val msg = CosmosMsg_Bank ( BankMsg_Send ({ to_address :
           info . sender , amount : [{ denom : DENOM , amount :
           asset_to_return }] }) )
24

25                 ( Ok ( Response_new
26                    . add_attribute ( " action " , FromStr ( " burn " ) )
27                    . add_attribute ( " user " , FromStr ( info . sender ) )
28                    . add_attribute ( " asset " , FromInt ( asset_to_return ) )
29                    . add_attribute ( " shares " , FromInt ( shares ) )
30                    . add_message ( msg ) ) , updated_state )
31             }
32         }
33     }
                            Listing 1.11. CTF-04, burn (erroneous)


     ### Explanation of Errors

     - **Non-existing key error**: The error ‘Called ’get’ with a non-existing
      key‘ indicates that the key ‘info.sender‘ does not exist in the ‘state.
     balances‘ map. This means that the code attempts to access a balance for
     a user that might not have an entry in the ‘balances‘ map.

     ### Repaired Function

     To fix this issue, we need to handle the case where ‘info.sender‘ does
     not have an existing balance entry. We can use the ‘getOrElse‘ function
     to provide a default balance of 0 if the user does not have an entry in
     the map.

     ‘‘‘quint
     pure def burn(state: ContractState, deps: Deps, env: Env, info:
     MessageInfo, shares: int): (Result[Response, ContractError],
     ContractState) = {
30            J. Corazza et al.

      val contract_balance = deps.querier.bank.get(CONTRACT_ADDRESS).get(
      DENOM)
      val total_assets = contract_balance
      val total_supply = state.config.total_supply

      // Compute the amount of assets to return
      val asset_to_return = shares * total_assets / total_supply

      if (asset_to_return == 0) {
        (Err("ZeroAmountNotAllowed"), state)
      } else {
        val user_balance = getOrElse(state.balances, info.sender, { amount:
        0 }).amount

          if (user_balance < shares) {
            (Err("unsigned int error"), state)
          } else {
            val updated_user_balance = user_balance - shares
            val updated_total_supply = total_supply - shares

              val updated_balances = state.balances.put(info.sender, { amount:
              updated_user_balance })
              val updated_state = { ...state, config: { total_supply:
              updated_total_supply }, balances: updated_balances }

              val msg = CosmosMsg_Bank(BankMsg_Send({ to_address: info.sender,
              amount: [{ denom: DENOM, amount: asset_to_return }] }))

              (Ok(Response_new
                .add_attribute("action", FromStr("burn"))
                .add_attribute("user", FromStr(info.sender))
                .add_attribute("asset", FromInt(asset_to_return))
                .add_attribute("shares", FromInt(shares))
                .add_message(msg)), updated_state)
          }
      }
  }
‘‘‘

### Changes Made

- Used ‘getOrElse‘ to safely retrieve the user’s balance, providing a
default balance of ‘{ amount: 0 }‘ if the user does not have an entry in
the ‘state.balances‘ map. This prevents the ‘Called ’get’ with a non-
existing key‘ error.

                Listing 1.12. LLM reasoning for runtime error in CTF-04, burn

   The overall runtime repair process resembles semantic repair, because it relies
on iterating over the user-provided I/O examples for detection. However, the
                             Synthesizing Formal Models with Tamed LLMs         31

content that we use to prompt the LLM—primarily, error messages obtained
by running Quint—is more akin to static repair rounds. The only difference
is that, when repairing static errors, we obtain error messages from the type
checker as explained in Section 4.3, and not by attempting to run the simulator
(REPL) as we do when obtaining runtime error messages. However, because of
the aforementioned similarity in content, we prepare runtime repair prompts by
reusing the static repair prompt template (shown in full in Listing 1.20).


C    Comprehensive model generation results
In Table 3, we present comprehensive results of our evaluation, including the
complete outcomes for the Capture the Flag benchmark (CTF-02, 04, 05, 07, and
09). These results include information about both the generation process (Avg.
Repair), and the testing that followed if the generated functions contained no
runtime errors and were able to execute the tests (Pass Rate).
    Interestingly, the results for CTF-09 are the least promising. For two of its
functions (withdraw and claim_rewards), the generation process was successful
in only 4 out of 5 runs. Moreover, this contract required the most rounds of repair
on average, and has the worst pass rates on unseen test cases. The reason for
this likely lies in the complex logic required for contract operations in CTF-09
(and, consequently, lengthy target Quint implementations).
    How do user-supplied natural language (NL) inputs, i.e., the English language
description of each Quint action, affect performance across our CTF Benchmark?
In order to answer this question, we also conducted an ablation study where
we left out the NL descriptions when asking the LLM to generate or repair a
function. We report the results of our ablation study in Table 4.
    As can be seen, our results show a low impact of NL user inputs on the
performance across our benchmark, suggesting that the necessary level of user
expertise and involvement is lower than originally anticipated for a task of this
level of complexity. When user NL inputs are withheld, CTF-04, 07, and 09
required a slightly higher average number of repair rounds, while performance
on CTF-02 and 05 was unaffected.
    Notably, performance was more negatively affected on CTF-09, which in-
cludes the most challenging Quint functions. Although firm conclusions are lim-
ited by the scope of this ablation study, these results suggest that custom NL
user inputs may play a more significant role in more demanding generation tasks.
    Finally, in Figure 3, we provide an illustrative example showcasing the pro-
gression from the original Rust code to the corresponding Quint stub and the
final LLM-generated Quint code, demonstrating the translation and generation
process for a function from the CTF-02 benchmark.


D    Adapter Generation and Repair
While mechanically generating a Quint model for a smart contract, we also gen-
erate an adapter stub, a Rust test file which can run traces induces by the Quint
     32      J. Corazza et al.

     model against the CosmWasm implementation of the smart contract. Afterwards,
     we use an LLM to improve the adapter by regenerating a core part of the test’s
     functionality: the state comparison function compare_state. In Listing 1.16, we
     present the stub for the compare_state function (the mechanically generated
     default with weak checks), and in Listings 1.17 and 1.18 we present example
     generations from our study in Appendix A for CTF-02 and 04, respectively.
1  fn compare_state ( test_state : & TestState , app : & App , state : &
       State ) {
 2           // compare contract balances
 3           let balance = app
 4               . wrap ()
 5               . query_balance (& test_state . contract_addr , DENOM )
 6               . unwrap ()
 7               . amount ;
 8           let trace_balance = state
 9               . bank
10               . get (& test_state . contract_addr . to_string () )
11               . and_then (| x | x . get ( DENOM ) )
12               . and_then (| x | x . to_u128 () )
13               . unwrap_or (0) ;
14           println !(
15               " Contract balance ({:?}) for { DENOM }: {:?} vs
       {:?} " ,
16               test_state . contract_addr ,
17               balance ,
18               Uint128 :: new ( trace_balance )
19           );
20           assert_eq !( balance , Uint128 :: new ( trace_balance ) ) ;
21

22            // TODO : Query the contract and compare the state as
          you wish
23        }
     Listing 1.16. Stub used for the state comparison functions during adapter generation


1  fn compare_state ( test_state : & TestState , app : & App , state : &
       State ) {
 2     // compare contract balances
 3     let balance = app
 4          . wrap ()
 5          . query_balance (& test_state . contract_addr , DENOM )
 6          . unwrap ()
 7          . amount ;
 8     let trace_balance = state
 9          . bank
10          . get (& test_state . contract_addr . to_string () )
11          . and_then (| x | x . get ( DENOM ) )
12          . and_then (| x | x . to_u128 () )
13          . unwrap_or (0) ;
                                Synthesizing Formal Models with Tamed LLMs                  33

14   println !(
15       " Contract balance ({:?}) for { DENOM }: {:?} vs {:?} " ,
16       test_state . contract_addr ,
17       balance ,
18       Uint128 :: new ( trace_balance )
19   );
20   assert_eq !( balance , Uint128 :: new ( trace_balance ) ) ;
21

22   // compare contract state
23    for ( user , trace_user_info ) in & state . contract_state .
     voting_power {
24        // Query user info
25         let msg = o a k s e c u r i t y _ c o s m w a s m _ c t f _ 0 2 :: msg :: QueryMsg
     :: GetUser {
26             user : user . clone () ,
27        };
28         let user_info : o a k s e c u r i t y _ c o s m w a s m _ c t f _ 0 2 :: state ::
     UserInfo = app
29             . wrap ()
30             . query_wasm_smart ( test_state . contract_addr .
     to_owned () , & msg )
31             . unwrap () ;
32

33        // Compare total tokens
34        let trace_total_tokens = Uint128 :: new ( trace_user_info
     . total_tokens . to_u128 () . unwrap () ) ;
35         assert_eq !( user_info . total_tokens , trace_total_tokens
     , " Mismatch in total tokens for user {} " , user ) ;
36

37         // Compare voting power
38         let trace_voting_power = trace_user_info . voting_power
     . to_u128 () . unwrap () ;
39         assert_eq !( user_info . voting_power , trace_voting_power
     , " Mismatch in voting power for user {} " , user ) ;
40

41          // Compare release time
42          let trace_released_time = trace_user_info .
     released_time . to_u64 () . unwrap () ;
43          assert_eq !( user_info . released_time . seconds () ,
     trace_released_time , " Mismatch in released time for user
     {} " , user ) ;
44

45        // Query voting power separately
46        let msg = o a k s e c u r i t y _ c o s m w a s m _ c t f _ 0 2 :: msg :: QueryMsg
     :: GetVotingPower {
47             user : user . clone () ,
48        };
49        let voting_power : u128 = app
50            . wrap ()
     34      J. Corazza et al.

51                 . query_wasm_smart ( test_state . contract_addr .
          to_owned () , & msg )
52                 . unwrap () ;
53

54             assert_eq !( voting_power , trace_voting_power , "
          Mismatch in voting power query for user {} " , user ) ;
55        }
56   }
                  Listing 1.17. CTF-02 generated state comparison example


1  fn compare_state ( test_state : & TestState , app : & App , state : &
       State ) {
 2     // compare contract balances
 3     let balance = app
 4          . wrap ()
 5          . query_balance (& test_state . contract_addr , DENOM )
 6          . unwrap ()
 7          . amount ;
 8     let trace_balance = state
 9          . bank
10          . get (& test_state . contract_addr . to_string () )
11          . and_then (| x | x . get ( DENOM ) )
12          . and_then (| x | x . to_u128 () )
13          . unwrap_or (0) ;
14     println !(
15          " Contract balance ({:?}) for { DENOM }: {:?} vs {:?} " ,
16          test_state . contract_addr ,
17          balance ,
18          Uint128 :: new ( trace_balance )
19     );
20     assert_eq !( balance , Uint128 :: new ( trace_balance ) ) ;
21

22         // Query the contract ’s config
23         let config_msg = o a k s e c u r i t y _ c o s m w a s m _ c t f _ 0 4 :: msg ::
          QueryMsg :: GetConfig {};
24         let contract_config : o a k s e c u r i t y _ c o s m w a s m _ c t f _ 0 4 :: state ::
          Config = app
25             . wrap ()
26             . query_wasm_smart ( test_state . contract_addr . to_owned ()
          , & config_msg )
27             . unwrap () ;
28         let trace_config = & state . contract_state . config ;
29         assert_eq !(
30             contract_config . total_supply ,
31             Uint128 :: new ( trace_config . total_supply . to_u128 () .
          unwrap () )
32         );
33

34        // Query the contract ’s user balances
                                      Synthesizing Formal Models with Tamed LLMs                35

35         for ( address , trace_balance ) in & state . contract_state .
           balances {
36              let balance_msg = o a k s e c u r i t y _ c o s m w a s m _ c t f _ 0 4 :: msg ::
           QueryMsg :: UserBalance {
37                    address : address . clone () ,
38              };
39              let contract_balance : o a k s e c u r i t y _ c o s m w a s m _ c t f _ 0 4 ::
           state :: Balance = app
40                    . wrap ()
41                    . query_wasm_smart ( test_state . contract_addr .
           to_owned () , & balance_msg )
42                    . unwrap () ;
43              assert_eq !(
44                    contract_balance . amount ,
45                    Uint128 :: new ( trace_balance . amount . to_u128 () .
           unwrap () )
46              );
47         }
48   }
                   Listing 1.18. CTF-04 generated state comparison example



     D.1     Adapter generation testing and repair results
     As part of our model-based testing case study from Appendix A, we evaluated of
     our adapter generation method on CTF-02 and 04. For each of the two adapters,
     we only use the LLM to generate one particular (Rust) function: compare_state.
     After (re-)generating this function, we attempt to run the whole test using the
     cargo test utility. Given that the LLM may also produce errors when generating
     Rust code, the resulting adapter can fail to compile and execute. Therefore,
     implementing a repair loop is necessary here as well. In Table 5 we summarize
     the full results of the generate-and-repair loop, obtained throughout our model-
     based testing case study.
         To summarize, our adapter generation method resulted in a working adapter
     test in all 5 runs, and we only required two rounds of repair in total. However,
     it must be noted that, in this case, mechanical generation carries an even larger
     portion of the responsibility: the LLM’s task is to simply expand the checks
     carried out by a single Rust function (a language which LLMs handle with
     higher proficiency than Quint).


     E     Prompt Templates
     In this section, we present an informative selection of prompt templates that we
     use to format the system’s LLM queries, and to create our few-shot demonstra-
     tions dataset. The full list of templates is available in the project’s repository on
     GitHub.9
     9
         https://github.com/informalsystems/FuzzMo/tree/main/data/prompts
36     J. Corazza et al.

E.1   Full model generation user prompt template

Please complete this stub for my ‘@@@NAME@@@‘ Quint function.

@@@DESCRIPTION@@@

‘‘‘
@@@STUB@@@
‘‘‘

Here is the contract state type and related types:

‘‘‘
@@@QUINT TYPE DEFINITIONS@@@
‘‘‘

The following constants are available to the function:

‘‘‘
@@@CONSTANTS@@@
‘‘‘
@@@DEC@@@

The following Quint imports are available:

‘‘‘
@@@QUINT IMPORTS@@@
‘‘‘

If a module is imported as ‘import Module.* from "./lib/module"‘, you
must use the identifiers from it directly without (so ‘name‘ instead of
‘Module.name‘).

The ‘@@@NAME@@@‘ Quint function models a CosmWasm Rust function for
processing smart contract messages.
@@@MESSAGE HANDLERS@@@

Your Quint code must be functional.
All function arguments are immutable, and you can not use mutable
variables.
@@@IO EXAMPLES@@@
                       Listing 1.19. User prompt template



E.2   Full repair user prompt template
Listing 1.20 presents the full prompt template we utilize for generating user mes-
sages during the static error repair phase. The macro @@@ORIGINAL IMPLEMENTATION@@@
expands to a stub implementation that is being repaired (i.e., the output of the
                           Synthesizing Formal Models with Tamed LLMs     37

initial code generation or a preceding repair round), and @@@QUINT ERRORS@@@
expands to the output of the Quint type checker (or, in the case of a runtime
repair round, the standard output of the Quint executable).


Please repair my ‘@@@NAME@@@‘ Quint function so that it no longer has
Quint errors.

@@@DESCRIPTION@@@

Here is the contract state type and related types:

‘‘‘
@@@QUINT TYPE DEFINITIONS@@@
‘‘‘

The following constants are available to the function:

‘‘‘
@@@CONSTANTS@@@
‘‘‘
@@@DEC@@@

@@@QUINT SHORT INSTRUCTIONS@@@

Here is the current implementation:

‘‘‘
@@@ORIGINAL IMPLEMENTATION@@@
‘‘‘

Here are the Quint errors that the current implementation has:

@@@QUINT ERRORS@@@

Ignore problems that do not concern this function.
Only respond with a function definition (‘pure def‘), and not type
definitions.

First explain what the problem is with a bullet-point list.
Do not make guesses about other problems.
Then respond with the repaired function that does not have those errors.
Minimize your changes to the original implementation, and please respect
Quint rules.
Do not introduce your own type definitions.

          Listing 1.20. Static and runtime repair user prompt template
     38       J. Corazza et al.

     F     Quint Model Structure

     In this section, we give a basic overview of how a Quint model looks like. This
     is far from a complete description, but it should give you enough detail to un-
     derstand the decisions made when generating Quint stubs. For a more detailed
     description, refer to the Quint documentation [10].
         Quint is a modelling language. It is like a very familiar pseudocode, that
     additionally enables us to encode state machines (the evolution of the system)
     and nondeterministic choices.
         The state of the Quint model is defined by a set of variables, for example the
     following:
1           var x : int
2           var y : bool
        The model’s evolution is described by its initial state and possible transitions
     from each state. In Quint, there is a special kind of function, called action, that
     can modify state variables. Thus, we use actions to define both the initial state
     and transitions.
        As an example, the initial state may be defined as follows:
1           action i n i t = a l l {
2               x’ = 0,
3               y ’ = false
4           }
          And transitions may be defined like this:
 1          action s t e p = any {
 2              nondet i n c r e a s e = oneOf ( 1 . to ( 1 0 ) )
 3              all {
 4                    x < 5,
 5                    y == f a l s e ,
 6                    x ’ = x + increase ,
 7                    y ’ = true
 8              },
 9              all {
10                    y ’ = true ,
11                    x’ = 0
12              }
13          }
         Let us explain the above two actions. The syntax x’ (read: x primed ) means
     “the value of x in the next state”. Thus, the action step defines two possible
     transitions:

      – either x < 5 and y == false, in which case increase x in the next state by
        a non-deterministically chosen number between 1 and 10, and set y to true,
      – or set y to true and x to 0.
                                Synthesizing Formal Models with Tamed LLMs         39

    The either-or choice is encoded by the any keyword. Furthermore, which one of
    them is chosen is non-deterministic, but the first option can only be selected if
    its conditions are satisfied.
        The action init is straightforward: it sets the initial values of x and y to 0
    and false, respectively.
        Beside actions, Quint has a concept of pure functions. Those are the functions
    that may not modify the state, but can be used to calculate values.
        The last point to mention is the concept of invariants. They are defined on
    state variables, and Quint’s simulator or model checker make sure that they hold
    at all states of the model evolution. As an example of an invariant, consider the
    following simple one:
1        val xAlwaysSmall = i n v a r i a n t x < 15
40     J. Corazza et al.




Table 3. Average number of repair rounds used per function and test pass rates for
unseen test cases, averaged across 5 independent runs (results for the whole CTF
benchmark)

                                    CTF-02
                      Function         Avg. Repair             Pass Rate
        ✓              deposit             0.0                   100%
        ✓             withdraw             0.0                   100%
        ✓               stake              0.0                   100%
        ✓              unstake             0.0                    50%
                                    CTF-04
                     Function          Avg. Repair             Pass Rate
        ✓           instantiate            0.0                   100%
        ✓              mint                1.2                    90%
        ✓              burn                0.0                   100%
                                    CTF-05
                     Function          Avg. Repair             Pass Rate
        ✓           instantiate            0.0                   100%
        ✓             deposit              0.0                   100%
        ✓            withdraw              0.0                   100%
        ✓          owner_action            0.0                   100%
        ✓          propose_owner           0.0                   100%
        ✓          accept_owner            0.0                   100%
        ✓           drop_owner             0.0                   100%
                                    CTF-07
                     Function          Avg. Repair             Pass Rate
        ✓           instantiate            0.0                   100%
        ✓             deposit              0.8                   100%
        ✓            withdraw              0.0                   100%
        ✓          owner_action            0.0                   100%
        ✓          update_config           0.0                   100%
                                    CTF-09
                     Function            Avg. Repair           Pass Rate
        ✓             deposit                2.4                  73%
      ? (4/5)        withdraw                1.6                  73%
        ✓         increase_reward            0.2                 100%
      ? (4/5)      claim_rewards             1.8                  80%
                            Synthesizing Formal Models with Tamed LLMs         41



       Table 4. Ablation study with natural language descriptions left out

                                    CTF-02
                      Function         Avg. Repair             Pass Rate
        ✓              deposit             0.0                   100%
        ✓             withdraw             0.0                   100%
        ✓               stake              0.0                   100%
        ✓              unstake             0.0                    50%
                                    CTF-04
                     Function          Avg. Repair             Pass Rate
        ✓           instantiate            0.0                   100%
        ✓              mint                2.0                   100%
        ✓              burn                0.0                   100%
                                    CTF-05
                     Function          Avg. Repair             Pass Rate
        ✓           instantiate            0.0                   100%
        ✓             deposit              0.0                   100%
        ✓            withdraw              0.0                   100%
        ✓          owner_action            0.0                   100%
        ✓          propose_owner           0.0                   100%
        ✓          accept_owner            0.0                   100%
        ✓           drop_owner             0.0                   100%
                                    CTF-07
                     Function          Avg. Repair             Pass Rate
        ✓           instantiate            0.0                   100%
        ✓             deposit              1.0                   100%
        ✓            withdraw              0.2                   100%
        ✓          owner_action            0.0                   100%
        ✓          update_config           0.0                   100%
                                    CTF-09
                     Function            Avg. Repair           Pass Rate
      ? (4/5)         deposit                2.0                  67%
      ? (2/5)        withdraw                2.4                  40%
        ✓         increase_reward            0.8                 100%
        ✓          claim_rewards             1.8                 100%




            CTF Adapter Function Avg. Repair Static Rounds
           CTF-02      compare_state          0.40           2
           CTF-04      compare_state          0.00           0
Table 5. Results for adapter generation for CTF-02 and CTF-04 across 5 independent
runs
     42     J. Corazza et al.


1 // / Entry point for user to stake tokens
2 pub fn deposit ( deps : DepsMut , info : MessageInfo ) -> Result <
       Response , ContractError > {
3      // validate denom
4      let amount = must_pay (& info , DENOM ) . unwrap () ;
5

6         // increase total stake
7         let mut user = VOTING_POWER
8              . load ( deps . storage , & info . sender )
9              . unwrap_or_default () ;
10        user . total_tokens += amount ;
11

12        VOTING_POWER
13            . save ( deps . storage , & info . sender , & user )
14            . unwrap () ;
15

16        Ok ( Response :: new ()
17              . add_attribute ( " action " , " deposit " )
18              . add_attribute ( " user " , info . sender )
19              . add_attribute ( " amount " , amount ) )
20   }
                                Listing 1.13. Original Rust code

1 pure def deposit ( state : ContractState , deps : Deps , info :
      MessageInfo ) : ( Result [ Response , ContractError ] ,
      ContractState ) = {
2     // TODO : Update body
3     ( Ok ( Response_new ) , state )
4}

                                   Listing 1.14. Quint stub

1 pure def deposit ( state : ContractState , info : MessageInfo ) : (
      Result [ Response , ContractError ] , ContractState ) = {
2     match must_pay ( info , DENOM ) {
3           | Err ( e ) = > ( Err ( e ) , state )
4           | Ok ( amount ) = > {
5           val user = getOrElse ( state . voting_power , info . sender ,
       { total_tokens : 0 , voting_power : 0 , released_time : 0 })
6           val updated_user = { ... user , total_tokens : user .
      total_tokens + amount }
7           val updated_voting_power = state . voting_power . put (
      info . sender , updated_user )
8           val new_state = { ... state , voting_power :
      updated_voting_pow er }
9

10            ( Ok ( Response_new
11                   . add_attribute ( " action " , FromStr ( " deposit " ) )
12                   . add_attribute ( " user " , FromStr ( info . sender ) )
13                   . add_attribute ( " amount " , FromInt ( amount ) ) ) ,
          new_state )
14            }
15        }
16        }
                          Listing 1.15. LLM-generated Quint code


     Fig. 3. Example of a stub along with the original Rust code that induced it and the
     final LLM-generated Quint code. Source: CTF-02.
