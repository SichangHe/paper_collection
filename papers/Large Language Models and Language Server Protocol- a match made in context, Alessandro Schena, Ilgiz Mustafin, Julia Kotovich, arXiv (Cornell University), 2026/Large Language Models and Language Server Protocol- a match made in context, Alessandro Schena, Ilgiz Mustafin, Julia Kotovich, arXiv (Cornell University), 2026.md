                                            Large Language Models and Language Server
                                                 Protocol: a match made in context

                                                        Alessandro Schena1 [0009-0005-1793-9107] , Ilgiz
                                         Mustafin1 [0009-0007-0476-5966] , and Julia Kotovich1,2 [0000-0003-3739-6304]
                                                  1
                                                   Constructor Institute of Technology, Schaffhausen, Switzerland
                                            {Alessandro.Schena, Ilgiz.Mustafin, Julia.Kotovich}@constructor.org
arXiv:2609.03086v1 [cs.SE] 2 Sep 2026




                                                          2
                                                            Constructor University, Bremen, Germany



                                               Abstract. This article introduces Eiffel-tools, a language server pro-
                                               tocol (LSP) implementation for the Eiffel programming language that
                                               uses Large Language Models (LLMs) to aid the development of stati-
                                               cally verified software. The tool provides various interactive and non-
                                               interactive commands to produce code and specifications. It uses lan-
                                               guage and project specific knowledge to precisely direct the LLM and
                                               verifies the output using a static verifier. It crafts rich programmatic
                                               prompts for the input and corrects or rejects the output. Furthermore,
                                               it handles the retries until the program passes verification.
                                               The tool’s bug fixing capability is evaluated on 2 public datasets using
                                               3 models. The tool can fix 76% to 95% of bugs by combining LLMs and
                                               a formal verifier depending on the model and prompts used. The results
                                               show the trade-off between the number of fixing attempts and the success
                                               rate.

                                               Keywords: LLM · LSP · Software verification · Design by Contract ·
                                               Eiffel · AutoProof


                                        1    Introduction
                                        Specification-driven development (SDD) is getting more attention with the grow-
                                        ing use of Large Language Models (LLMs) for development [1]. In this approach,
                                        the development is done in a natural language by writing specifications while the
                                        program code is then generated automatically from the specifications.
                                            Expressing specifications using a formal language, even partially [2], opens
                                        the door for various analysis tools. For example, using Design by Contract [3]
                                        in Eiffel, the program’s state is checked against specifications during execution.
                                        This allows test runs of the program to show the presence of implementation
                                        errors.
                                            A more advanced analysis such as formal verification allows finding incon-
                                        sistencies between specifications and implementation statically, without running
                                        the code. This allows finding errors earlier and mathematically proving arbitrary
                                        functional properties. Still, errors in specifications can lead to invalid but correct
                                        programs.
2       Alessandro Schena, Ilgiz Mustafin, and Julia Kotovich

    Modern SDD relies heavily on LLMs. While LLMs code generation might
work well for programming languages that are well-represented in the train-
ing datasets, their ecosystem might not have formal verification tools available.
These are called high-resource languages [4].
    Eiffel is a low-resource language; it has a first-class support for specifications
and a static verifier AutoProof, but the low amount of public code makes LLM
code generation more challenging. Adapter tools could mitigate this issue. Any
such tool must structure and contextualize the code for the model and must keep
the user in the loop whenever a reasonable output is produced. To mitigate this
issue, special tools can be implemented which take the role of an adapter: on
the one hand, the tool must structure and contextualize the code for the model,
on the other hand, the tool must present model’s outputs to allow the user to
benefit more from the LLM.
    This paper introduces Eiffel-tools [5], as the aforementioned adapter. Eiffel-
tools implements the Language Server Protocol (LSP) to integrate conveniently
in the majority of code editors.
    In this paper we highlight the tool’s “fix feature body” command. The com-
mand tries to change the body of the procedure such that it will satisfy its
specifications. The tool presents the relevant parts of the code, while omitting
irrelevant parts of the project, to the LLM and sets up the interaction loop
between the LLM and the verifier.
    We present the evaluation of this command using two datasets of buggy pro-
grams with correct specifications and compare the performance of three LLMs.
One model is a small generalist model, second is a small coding model and
another is a bigger coding model.
    The remainder of this paper is structured as follows. Section 2 provides the
necessary background, introducing the core concepts related to the Eiffel pro-
gramming language, large language models, and LSP-based tooling in greater de-
tail. Section 3 reviews related work in automated program repair, LLM-assisted
development, and contract-driven methodologies. Section 4 presents the design
and implementation of our experimental setup, describing how contract-guided
repair is operationalized using LLMs. Section 5 outlines the evaluation method-
ology, followed by Section 6, which reports the experiment results and discusses
them. Section 7 addresses threats to validity and limitations of the study. Finally,
Section 8 outlines directions for future work.

2     Background
This section provides the background information about the Eiffel programming
language and the related technologies.

2.1   Eiffel and AutoProof
Eiffel [6] is an object-oriented programming language with first-class support for
Design by Contract [3], allowing developers to embed preconditions, postcon-
ditions, and class invariants directly in the source code. Thus, a typical Eiffel
                                   LLMs and LSP: a match made in context          3

project contains both the executable program and its formal specifications within
the same codebase. For this reason, we consider Eiffel to be natively suitable for
SDD.
    Eiffel’s contracts are used commonly for dynamic checking. When a program
is executed in testing or development environment, its contracts transformed in
equivalent runtime assertions. For example, when there is a procedure call, the
callee’s preconditions are asserted in the caller just before the call. These checks
are removed in the finalized version of the program.
    Another use of contracts is static verification via AutoProof [7]. AutoProof is
an auto-active verifier for the Eiffel programming language that can prove func-
tional correctness of Eiffel programs annotated with contracts. It works only with
model-based contracts. Model-based contracts refer to data structures which are
formalized by axioms in the lower-level verifier. They are not executable. They
are the bridge that connects Eiffel to Boogie [8], the underlying tool that gener-
ates proof obligations for some SMT solver. This allows proving correctness of
the program for all possible execution paths, in contrast with testing where it
might be impossible to test the program in all possible states.


2.2   Large language models for software development

The recent advancements in deep learning brought large language models into
industrial use for software development. LLMs need proper context to provide
useful information because despite their impressively coherent outputs, they are
not oracles and cannot infer user intentions that are not explicitly stated. This
paper shows that language servers are a natural place to condense language and
project specific information to guide the generation of large language models. We
expect the constructed context to compensate partially the scarcity of training
data for low resources languages and boost the quality of performance for all
other languages.


2.3   Language server protocol

The language server protocol (LSP) [9] is proposed to be used as a common
integration point between the code editor, the verifier and the LLM. It defines
a compatibility layer between source code editors and language specific func-
tionalities. To exemplify the widespread adoption of this protocol, let us note
that at the time of this writing there are 302 server side and 65 client side
implementations listed on the official website [9].
    When a programming editor implements the client side of the LSP, it auto-
matically provides “smart editing features” for any programming language sup-
ported by a protocol compliant server. Some of the language-specific features
which the LSP standardizes are code completion, marking of lints, warnings
and errors and editing routines. The latter can be refactoring routines, format-
ting routines, and custom operations with domain specific knowledge. Within
the protocol they are shown as code actions or commands; the former being
4       Alessandro Schena, Ilgiz Mustafin, and Julia Kotovich

parametrized only by the user’s cursor position and the latter which can be
called from anywhere with the right arguments.
    These custom operations may access the server state and use the project and
language specific knowledge to implement their custom logic. This is a perfect
environment for defining guidelines for LLMs: which information is useful in the
prompt, which outputs satisfy the syntax of the language and which identifiers
are valid in the place the custom command wants to write and more. In our
case, because Eiffel can define formal specifications and AutoProof can prove the
correctness of the code against those specifications, we can force any command
that generates code to produce only verified code.


3   Related work

The research area applying LLMs to software engineering is flourishing, with a
rapidly expanding body of work addressing a wide range of development and
analysis tasks. Authors of [10] provide a systematic taxonomy of generative
transformations and their compositional patterns in LLM-native applications,
primarily as an analytical framework. Another study [11] conducts a systematic
literature review of LLM applications in SE, with a particular focus on under-
standing how LLMs can be exploited to optimize processes and outcomes. Com-
plementary to these studies, the authors [12] systematically review recent ad-
vances in LLM applications for software engineering. They analyze applications
in requirements, testing, deployment, and operations, and identify key challenges
and future directions.
    The study [13] emphasizes on the investigation of the emerging area of LLMs
for SE and their applications, highlighting the importance of hybrid techniques,
such as traditional SE plus LLMs for the reliable and efficient software develop-
ment.
    LSP can be used to provide context during the LLM inference through mon-
itors [14]. This approach uses language servers externally, primarily leveraging
their completion engines, to dynamically mask the streaming output of large lan-
guage models, which further enhances fine-tuning and dynamic masking. With
the same philosophy, our work defines where and how the LLMs may find lan-
guage and project specific knowledge, which adds benefit to fine-tuning and
dynamic masking.
    CITADEL [15] and AutoInfer [16] automatically generate Eiffel specifica-
tions. Citadel is an Eiffel front end for Daikon [17]. AutoInfer [16] is another
tool that generates Eiffel contracts using data mining and contract templates.
However, these tools generate specifications for dynamic checks, not model-based
specifications for static verification.
    On the side of automatic repair of Eiffel programs there is AutoFix [18] and
Proof2Fix [19]. AutoFix uses random testing through AutoTest [20] to iden-
tify the faults. Proof2Fix identifies faults using AutoProof. They both propose
candidate fixes that may be the substitution of a template for code edits or
the strengthening of the preconditions or weakening of the postconditions for
                                  LLMs and LSP: a match made in context         5

contracts edits. However, these tools are limited to Eiffel and do not general-
ize to LLM-guided, project- and language-specific specification and verification
workflows, which is the focus of our approach.
    An experiment similar to the evaluation of this paper is presented in [21]
with the focus on generating specifications and fixing them. Similar prompting
techniques are discussed for JML and Frama-C.
    A close work in the field of LLM-assisted development and manual program
repair is the study [22] of developers producing verified fixes with and without
the assistance of an LLM chat.

4   Design and implementation
Eiffel-tools is an LSP language server which provides several novel commands
using LLMs and a static verifier to generate or repair Eiffel code and specifica-
tions.
    The language server avoids using a full-fledged Eiffel compiler to be perfor-
mant and provide support to projects in inconsistent states with compilation
errors and missing files. Eiffel-tools reads the project configuration file (ECF),
parses it, extracts the used libraries and recursively analyses them. All classes
used in the system are indexed (features, contracts, inheritance tree is stored)
and available through the usual LSP interfaces which allows code editors, for ex-
ample, to display and navigate between classes and features in the source code.
This information is also integrated into LLM prompts when relevant to give the
relevant context to the model.
    Eiffel source code in files and LLM responses is parsed using an external
parser [23] based on Tree-sitter [24]. This allows using Tree-sitter queries to
extract the relevant structures from the source code. For example, when LLM is
used to generate code, the parser is used to find valid features in the responses
and then to extract code or contracts of the found feature.
    The tool does not depend heavily on any specific LLM or an API. Currently
an OpenAI-like chat/completions API is supported. We are using the Open-
Router platform which provides access to several LLMs using the same API to
conduct the experiment.
    Eiffel-tools uses AutoProof to verify existing code or LLM-generated sugges-
tions. Because AutoProof may not terminate on some inputs, Eiffel-tools runs it
with timeouts: any verification exceeding a time limit is killed, and if the code
was LLM-generated, the tool reverts it to its previous stable state upon failure.
    For organizational clarity, Eiffel-tools commands are classified along two di-
mensions:
 – By interaction mode
    • Interactive, invoked as code actions by the LSP client
    • Non-interactive, invoked as standalone executables
 – By focus
    • specifications
    • code
    • specification and code
6         Alessandro Schena, Ilgiz Mustafin, and Julia Kotovich

4.1     Interactive commands
Interactive commands are invoked by the developer as code actions in the IDE,
typically when the cursor is inside the definition of a feature (routine). These
commands may create intermediate files or artifacts in the workspace, but they
do not modify the files currently open in the developer’s editor. This approach
minimizes disruption and reduces context switching.

Add model-based contracts This command tries to add model-based con-
tracts to a given feature. As its focus in only on specifications, it may only
extend the feature’s precondition and postcondition blocks. It prompts an LLM
following this schema, where the “*” before a placeholder means that it is kept
as a placeholder in the final prompt.
-- <TASK>
-- <MODEL CURRENT CLASS>
-- <MODEL ARGUMENT CLASSES>
-- <PRECONDITION AVAILABLE IDENTIFIERS>
-- <POSTCONDITION AVAILABLE IDENTIFIERS>
<FEATURE NAME> <PARAMETERS> <RETURN TYPE>
   <HEADER COMMENT>
   require
       <PREEXISTING PRECONDITIONS>
       ∗<ADD NEW PRECONDITIONS>
   do
       <ALREADY PRESENT BODY>
   ensure
       <PREEXISTING POSTCONDITIONS>
       ∗<ADD NEW POSTCONDITIONS>
   end

    The user can include additional hints in the feature’s header comment, which
are incorporated into the prompt. The LLM returns a set of candidate feature
definitions. Eiffel-tools parses each candidate to extract the suggested contracts
and then applies filtering to remove any unsuitable contracts. Specifically, we
remove contracts which:
    – Are redundant
    – Are not model-based, and thus unusable by AutoProof
    – Contain invalid top-level identifiers
    – Contain calls with the wrong number of arguments
   Finally, Eiffel-tools instructs the LSP client to insert the remaining valid
contracts into the feature, appending them after any existing contracts.
   An example is shown at Figure 1.

Fix feature body This command generates an implementation for a feature
that satisfies its model-based specifications. It modifies only the feature’s body,
never its specifications. Because AutoProof can verify only complete, compil-
able programs, Eiffel-tools handles intermediate results by creating a subclass of
                                    LLMs and LSP: a match made in context        7




min (x, y: INTEGER): INTEGER
    -- Header comment
    require
        True
    do
        Result := x
    ensure
        True                            -- <task>
    end                                 -- <model current class>
                                        -- <model argument classes>
                                        -- <precondition available ids>
Initial feature                         -- <postcondition available ids>
                                        min (x, y: INTEGER): INTEGER
                                            -- Header comment
                                            require
                                                True
                                                <ADD NEW PRECONDITIONS>
                                            do
                                                Result := x
                                            ensure
min (x, y: INTEGER): INTEGER                    True
    -- Header comment                           <ADD NEW POSTCONDITIONS>
    require                                 end
        True
        llm−candidate−pre1              Generated prompt
        llm−candidate−pre2
    do
        Result := x
    ensure
        True
        llm−candidate−post1
        llm−candidate−post2
    end
                                        new−preconditions:
Generated llm-candidate                   llm−candidate−pre1
                                          llm−candidate−pre2

                                        new−postconditions:
                                          llm−candidate−post1
                                          llm−candidate−post2
new−preconditions:
  llm−candidate−pre1                    Extracted contracts
new−postconditions:
  llm−candidate−post2

Filtered contracts                      min (x, y: INTEGER): INTEGER
                                            -- Header comment
                                            require
                                                True
                                            do
                                                Result := x
                                            ensure
                                                True
                                                res: (Result = x or Result
                                                      = y)
                                                     and Result ≤ x and
                                                          Result ≤ y
                                            end

                                        Feature after edits


        Fig. 1. Dataflow of a feature in the add model-based contracts command
8                  Alessandro Schena, Ilgiz Mustafin, and Julia Kotovich

the current class and overriding the target feature in it. The overriding feature
is initially given to AutoProof. If verification fails, Eiffel-tools enters a loop: it
prompts the LLM for a new candidate body, inserts the candidate into the over-
riding feature, and reruns AutoProof. If a candidate body passes verification,
Eiffel-tools copies that body into the original feature; otherwise, the loop con-
tinues until a candidate passes or a maximum number of attempts is reached.
Unless a candidate succeeds, no changes are applied to the original feature.
       An example is shown at Figure 2.



class
    EXAMPLE
feature
    min (x, y: INTEGER): INTEGER
        -- Header comment
        do
            Result := x
        ensure
            res: (Result = x or Result = y)      -- <task>
                 and Result ≤ x and Result ≤ y   -- <model current class>
        end                                      -- <model argument classes>
end                                              -- <precondition available ids>
                                                 -- <postcondition available ids>
                                                 min (x, y: INTEGER): INTEGER
Initial feature in class                             -- Header comment
                                                     do
                                                         <ADD BODY>
min (x, y: INTEGER): INTEGER                         ensure
    -- Header comment                                    res: (Result = x or Result = y)
    do                                                        and Result ≤ x and Result ≤ y
        if x <y then                                 end
             Result := x
        else
             Result := y                         Generated prompt
        end
    ensure
        res: (Result = x or Result = y)          if x <y then
             and Result ≤ x and Result ≤ y           Result := x
    end                                          else
                                                     Result := y
                                                 end
Generated llm-candidate
                                                 Extracted body
class
    LLM_INSTRUMENTED_EXAMPLE
inherit
    EXAMPLE redefine min end
feature
    min (x, y: INTEGER): INTEGER
        do
            if x <y then
                 Result := x
            else
                 Result := y
            end
        ensure
            res: (Result = x or Result = y)
                 and Result ≤ x and Result ≤ y
        end
end                                                               Verification output         Fails

Instrumented feature redefinition
                                                       Succeds
min (x, y: INTEGER): INTEGER
    -- Header comment
    require
        True
    do
        if x <y then
             Result := x
        else
             Result := y
        end
    ensure
        True
        res: (Result = x or Result = y)
             and Result ≤ x and Result ≤ y
    end

Feature after edits



                           Fig. 2. Dataflow of a feature in the fix feature body command
                                    LLMs and LSP: a match made in context             9

4.2   Non-interactive commands

Non-interactive commands run as standalone executables, enabling batch ex-
ecution and clear tracking of LLM-generated changes under version control.
These commands may modify the project code and specifications directly, writ-
ing changes in place. After each change, Eiffel-tools runs AutoProof: if AutoProof
fails to verify the modified code, the tool reverts to the last stable state.


Feature by feature body correction This command takes an Eiffel configu-
ration file and a list of classes or features in classes. It parses the entire project
and attempts to verify each feature in the specified classes or only the given
features. If a feature fails verification, the tool prompts the LLM to suggest a
correction. It may modify the code of the failing feature. The contracts cannot
be changed and assumed to be correct. The LLM prompt includes the task de-
scription, a list of available identifiers, the feature’s code, the class invariant, and
the AutoProof counterexample (or a compilation error).
    The prompt to the LLM consists of two messages. The first message is a
system message including the task instructions and a short Eiffel syntax guide.
The second message is a user message which includes the feature to be fixed and
the verification or compilation errors present in the current version of the code.
System:
-- <TASK>

User:
-- <AVAILABLE IDENTIFIERS>
<FEATURE CODE>
-- <CLASS INVARIANT>
-- <AUTOPROOF COUNTEREXAMPLE>

    From each LLM response, the parser extracts a candidate feature definition.
Eiffel-tools backs up the original feature, replaces it with the candidate, and
reruns AutoProof. If verification still fails, the original is restored and another
candidate is tried. This process repeats until a candidate verifies or a maximum
number of attempts is reached.
    An example is shown at Figure 3;


Class by class correction This command takes an Eiffel configuration file and
a list of classes. It verifies and repairs entire classes as a unit. It may modify both
the specifications and code of all features in a class. After parsing the project,
Eiffel-tools verifies each class as a whole. If a class fails verification, the LLM is
asked to generate a new candidate version of the entire class. Eiffel-tools first
backs up the original class. If the LLM’s candidate is syntactically correct, it
replaces the class, and AutoProof is run on it. If verification succeeds, Eiffel-
tools moves on to the next class. Otherwise, it reverts to the backup and retries
with another candidate (up to a fixed limit). This is the only command that
attempts to produce a large, consistent output (a whole class) in one step.
10                  Alessandro Schena, Ilgiz Mustafin, and Julia Kotovich



class
    EXAMPLE
feature
    min (x, y: INTEGER): INTEGER
        -- Header comment
        do
            Result := x
        ensure
            res: (Result = x or Result = y)
                 and Result ≤ x and Result ≤ y
        end

      max (x, y: INTEGER): INTEGER
          -- Header comment
          do
              Result := x
          ensure
              res: (Result = x or Result = y)      class
                   and Result ≥ x and Result ≥ y       EXAMPLE
          end                                      feature
end                                                    -- <task>
                                                       min (x, y: INTEGER): INTEGER
Initial feature in class                                   -- Header comment
                                                           do
                                                               Result := x
                                                           ensure
                                                               res: (Result = x or Result = y)
class                                                               and Result ≤ x and Result ≤ y
    EXAMPLE                                                end
feature                                                    -- AutoProof counterexample
    -- <task>
    min (x, y: INTEGER): INTEGER                         -- <task>
        -- Header comment                                max (x, y: INTEGER): INTEGER
        do                                                   -- Header comment
            if x <y then                                     do
                 Result := x                                     Result := x
            else                                             ensure
                 Result := y                                     res: (Result = x or Result = y)
            end                                                       and Result ≥ x and Result ≥ y
        ensure                                               end
            res: (Result = x or Result = y)                  -- AutoProof counterexample
                 and Result ≤ x and Result ≤ y     end
        end
        -- AutoProof counterexample                Generated prompt
      -- <task>
      max (x, y: INTEGER): INTEGER
          -- Header comment
          do
              if x <y then                                                                Reset failing features
                   Result := y
              else
                   Result := x
              end
          ensure
              res: (Result = x or Result = y)
                   and Result ≥ x and Result ≥ y
          end                                                                                      Some feature fails
          -- AutoProof counterexample                               Verification output
end

Generated llm-candidate



                                                          All features verify


class
    EXAMPLE
feature
    min (x, y: INTEGER): INTEGER
        -- Header comment
        do
            if x <y then
                 Result := x
            else
                 Result := y
            end
        ensure
            res: (Result = x or Result = y)
                 and Result ≤ x and Result ≤ y
        end

      max (x, y: INTEGER): INTEGER
          -- Header comment
          do
              if x <y then
                   Result := y
              else
                   Result := x
              end
          ensure
              res: (Result = x or Result = y)
                   and Result ≥ x and Result ≥ y
          end
end

Feature after edits




           Fig. 3. Dataflow of a feature in the feature by feature correction command
                                  LLMs and LSP: a match made in context         11

  Each feature in the class prompt is formatted with its associated counterex-
ample, as follows:
-- <TASK>
<FEATURE CODE>
-- <AUTOPROOF COUNTEREXAMPLE ABOUT FEATURE>



5     Evaluation

We evaluated the feature by feature body correction command, described in
Section 4.2, on the datasets buggy-java-jml-eiffel and maple-recursive-eiffel using
three LLMs, GPT-5 Nano, Claude Sonnet 4.6 and Poolside Laguna XS with 2
ablations (versions) of prompts used.
    For every bug fixing task, 10 attempts were made by Eiffel-tools to fix the
error. Each attempt included the initial verification, prompting the model with
the verification result, verifying the suggested fix. If the suggested fix does not
verify, it is kept and the next attempt starts with the previously suggeste fix,
enabling a feedback loop between LLM and the verifier.
    All evaluations are in Eiffel-tools repository within the corresponding folder
experiment-results [5].


5.1   Models

The experiment compares performance of several models in the bug fixing task.
All model were accessed through the OpenRouter API.
    The Claude Sonnet 4.6 model from Anthropic [25] was created especially for
coding and for for building complex agents. This model represents the “expensive
but powerful” option in the experiment.
    The GPT-5 Nano model from OpenAI [26] is a generalist model “great for
summarization and classification tasks”. Comparing with Sonnet 4.6, the nano
model provides lower latency and a cheaper cost, so it represents the “cheap but
fast” option in the experiment.
    The Poolside Laguna XS [27] model is a smaller model with open weights.
At the moment of writing, it was provided for free, so it represents the “free and
open-weights” option in the experiment.


5.2   Datasets

Performance of the bug fixing capability was measured on two publicly available
datasets of buggy programs with contracts (formal specifications).
    The buggy-java-jml-eiffel dataset is a translation of the BuggyJava+JML
dataset [28] from Java and JML [29] to Eiffel. The Eiffel translation is available
online at [30]. Examples in the dataset include simple algorithms (function to
return the absolute value of an integer), array algorithms (copying an array,
12                  Alessandro Schena, Ilgiz Mustafin, and Julia Kotovich



class
    EXAMPLE
feature
    min (x, y: INTEGER): INTEGER
        -- Header comment
        do
            Result := x
        ensure
            res: (Result = x or Result = y)
                 and Result ≤ x and Result ≤ y
        end

      max (x, y: INTEGER): INTEGER
          -- Header comment
          do
              Result := x
          ensure
              res: (Result = x or Result = y)      class
                   and Result ≥ x and Result ≥ y       EXAMPLE
          end                                      feature
end                                                    -- <task>
                                                       min (x, y: INTEGER): INTEGER
Initial feature in class                                   -- Header comment
                                                           do
                                                               Result := x
                                                           ensure
                                                               res: (Result = x or Result = y)
class                                                               and Result ≤ x and Result ≤ y
    EXAMPLE                                                end
feature                                                    -- AutoProof counterexample
    -- <task>
    min (x, y: INTEGER): INTEGER                         -- <task>
        -- Header comment                                max (x, y: INTEGER): INTEGER
        do                                                   -- Header comment
            if x <y then                                     do
                 Result := x                                     Result := x
            else                                             ensure
                 Result := y                                     res: (Result = x or Result = y)
            end                                                       and Result ≥ x and Result ≥ y
        ensure                                               end
            res: (Result = x or Result = y)                  -- AutoProof counterexample
                 and Result ≤ x and Result ≤ y     end
        end
        -- AutoProof counterexample                Generated prompt
      -- <task>
      max (x, y: INTEGER): INTEGER
          -- Header comment
          do
              if x <y then                                                                Reset failing features
                   Result := y
              else
                   Result := x
              end
          ensure
              res: (Result = x or Result = y)
                   and Result ≥ x and Result ≥ y
          end                                                                                      Some feature fails
          -- AutoProof counterexample                               Verification output
end

Generated llm-candidate



                                                          All features verify


class
    EXAMPLE
feature
    min (x, y: INTEGER): INTEGER
        -- Header comment
        do
            if x <y then
                 Result := x
            else
                 Result := y
            end
        ensure
            res: (Result = x or Result = y)
                 and Result ≤ x and Result ≤ y
        end

      max (x, y: INTEGER): INTEGER
          -- Header comment
          do
              if x <y then
                   Result := y
              else
                   Result := x
              end
          ensure
              res: (Result = x or Result = y)
                   and Result ≥ x and Result ≥ y
          end
end

Feature after edits




                            Fig. 4. Dataflow of the class by class correction command
                                   LLMs and LSP: a match made in context           13

binary search), data structures (stack, queue). In total, 513 examples were used
from the dataset.
    The maple-recursive-eiffel dataset is a translation of the Maple dataset [31]
from C to Eiffel. The translation was used as a part of the evaluation benchmark
in Proof2fix [19] and is available online at [32]. Examples in the dataset include
simple algorithms (absolute value, sum, min, max) and recursive functions (re-
cursive counter). In total the dataset contains 26 examples and all of them were
used in the evaluation.

5.3   Ablations
To measure the usefulness of Eiffel-tools in helping LLMs work with a low-
resource language like Eiffel, performance of models is compared using two
prompt ablations (versions).
    The “full” version includes all parts of the prompt described in Section 4.2.
System message explains the Eiffel syntax which makes the most problems to
LLMs, including the order clauses in the loop (from invariant until loop variant
 end), arithmetic operators (// \\ for div and mod respectively). Additionally,
system message provides the prefilled template (Figure 5) for the expected fixed
feature.
    User message in the “full” ablation lists the names and types of variables
available in pre- and post-conditions and includes the feature to be fixed and
the compilation or verification error from AutoProof.


Your response must be a single ‘‘‘eiffel code block. The block must begin
      verbatim with the feature header (signature, documentation comments,
      notes, and precondition − exactly as shown). Then add your corrected
      local declarations and body. End the block with the verbatim
      postcondition and closing ‘end‘ before the closing ‘‘‘.
Required structure:
‘‘‘eiffel
div (a_n, a_d: INTEGER): INTEGER
     note
       status: functional
     require
       non_zero_divisor: a_d /= 0
...(your corrected local declarations and body here) ...
     ensure
       res_mod: Result = a_n \\ a_d
     end
‘‘‘


  Fig. 5. Part of the “full” ablation system message specifying the feature template


   The “minimal” ablation omits almost all of the rich features extracted by the
tool. System message does not have the Eiffel syntax guide nor the verbatim
14                             Alessandro Schena, Ilgiz Mustafin, and Julia Kotovich

feature template. Instead, a natural text explanation is provided: “The first line
of your response must be “‘eiffel and the second line must be the feature
signature”.
    User message omits the list of available variables and the error itself. Model
is only told in the system message that there is a problem, but the exact problem
is not specified in the user message.


6                        Results and Discussion

In total, the experiment used 539 bugs to be fixed by 3 LLMs using 2 prompt
ablations. At most 10 attempts were allowed per feature.



                                                                   Full
                                    513/539
                         100         95.2% 486/539                 Minimal
                                            90.2%                                  458/539
                                                           443/539                  85.0%
                                                            82.2% 415/539
                                                                                              410/539
                          80                                       77.0%                       76.1%
    Features Fixed (%)




                          60


                          40


                          20


                           0
                                           6                     no                    a XS
                                      et 4.              -5 na                       n
                                 Sonn                 GPT                       Lagu


                                                   Fig. 6. Model success rate


   Figure 6 shows how many bugs were fixed by each model in every ablation.
   Sonnet 4.6 solved the most tasks in both ablations (95% full, 90% minimal).
Laguna XS was better than GPT-5 nano in “full” (85% vs. 82%) while GPT was
better than Lagune in “minimal” (77% GPT vs. 76% Laguna).
   Using “full” gives 6.4 pp improvement on average. Extended prompts helped
Laguna to improve the most (8.9 pp).
                                                   LLMs and LSP: a match made in context          15


                      100


                       90
 Features fixed (%)




                       80


                       70                                                Sonnet 4.6 (Full)
                                                                         Sonnet 4.6 (Minimal)
                                                                         Laguna XS (Full)
                       60                                                Laguna XS (Minimal)
                                                                         GPT-5 nano (Full)
                                                                         GPT-5 nano (Minimal)
                       50
                            1       2      3    4     5      6     7      8            9     10
                                           Max attempts allowed per feature


                                Fig. 7. Model success rate per attempts (only fixed)



    Figure 7 shows the cumulative success rate per the number of attempts used.
The majority of fixes happen on the first attempt (from 67.9% for Laguna “min-
imal” to 83.5% for Sonnet “minimal”). Every next attempt increases the success
rate less and less.
    The “full” ablation results in a higher success rate consistently starting from
the 2nd attempt.
    Figure 8 shows the mean time used per feature run, including both sucessfully
fixed and still unfixed features after all attempts are exhausted. The diagram
shows the time spent in the LLM (waiting for the model response) separately
from the time spent in other steps (verification, tool overhead).
    LLM time depends on the model itself and the provider’s API. While there
are several configurable settings in OpenRouter which can optimize throughput
and latency, the experiment used the default settings.
    Experiments using smaller models spent the majority of time waiting for
LLM while Sonnet’s LLM time was similar to verification + tool time.
    Using the “minimal” ablation increases the total time per feature which is
mainly connected with the increase in the number of attempts used.
    Figure 9 present the mean cost used per feature run, including both sucess-
fully fixed and unfixed features.
    Because Laguna was available for free at the time of writing and no pricing
information was known, only Sonnet 4.6 and GPT-5 nano are compared.
    While Sonnet’s usage per feature is more expensive than of GPT (5x in “full”
and 3.3x in “minimal”), Sonnet is faster (2x in “full”, 3.3x in “minimal”).
16                                            Alessandro Schena, Ilgiz Mustafin, and Julia Kotovich




                                                                                                 LLM
 Mean wall-clock time per feature (s)
                                                                                                 Verification + tool
                                        200                                           195s




                                        150
                                                                           128s                              127s
                                                                                      158s        107s
                                        100
                                                                                                             76s
                                                                           105s
                                                                                                  78s
                                                                50s
                                         50         35s         19s
                                                    18s                                                      50s
                                                                30s                    38s        29s
                                                    17s                    23s
                                          0
                                                 Sonnet 4.6 Sonnet 4.6 GPT-5 nano GPT-5 nano Laguna XS Laguna XS
                                                   (Full)   (Minimal)    (Full)    (Minimal)   (Full)  (Minimal)


                                                      Fig. 8. Mean time per feature (fixed and unfixed)




                                        0.04
 Mean cost per feature (USD)




                                                   $0.0307
                                        0.03
                                                              $0.0261


                                        0.02


                                        0.01                                         $0.0080
                                                                          $0.0061

                                                                                                  free       free
                                        0.00
                                                  Sonnet 4.6 Sonnet 4.6 GPT-5 nanoGPT-5 nano Laguna XS Laguna XS
                                                    (Full)   (Minimal)    (Full)   (Minimal)   (Full)  (Minimal)


                                                       Fig. 9. Mean cost per feature (fixed and unfixed)
                                                               LLMs and LSP: a match made in context           17

    Switching to the “minimal” ablation decreased the cost per feature when using
Sonnet but increased when using GPT. The difference can be attributed to the
increase in attempts needed and the increase in reasoning tokens (Figure 10).



                                  30                                                         Out (reasoning)
    Mean tokens (k) per feature




                                                                                             Out (output)
                                  25                                                         In (input)


                                  20
                                                                 12.9

                                  15                                                   7.9
                                                                            18.3
                                                                 1.2
                                  10                                                   1.0
                                                                                                     7.7
                                          1.1                    10.6
                                   5                                                   8.7
                                          4.9          1.4                  1.3                      1.3
                                                       1.6                  2.2                      2.3
                                   0
                                       Sonnet 4.6   Sonnet 4.6 GPT-5 nano GPT-5 nano Laguna XS Laguna XS
                                         (Full)     (Minimal)    (Full)    (Minimal)   (Full)  (Minimal)


     Fig. 10. Mean input, output and reasoning tokens per feature (fixed and unfixed)


    In the experiment Sonnet had reasoning disabled (default settings) but GPT
and Laguna have reasoning enabled. Reasoning tokens have the same cost as
output tokens and cost more (5x more expensive for Sonnet, 8x more expensive
for GPT). Minimal ablation triggers additional reasoning in GPT which increases
the cost.


7                                 Limitations and threats to validity
The benchmarks used in our evaluation, described in Section 5, are public and
available in multiple programming languages, either C and Eiffel or Java-JML
and Eiffel. It is possible that those benchmarks leaked in the training data of
some LLMs and the models could reproduce the solution they were trained on
instead of “fixing” the bug.


8                                 Conclusion and Future work
This paper presented an approach for using an LSP server as both the LLM
harness and the integration interface between the editor, verifier and LLM at the
same time. Implementation of several advanced code editing actions combining
LLMs and vormal verification is presented.
18       Alessandro Schena, Ilgiz Mustafin, and Julia Kotovich

    The experiment results discuss trade-offs and set a baseline for the possible
further improvements across several axes: fix success rate, time, and cost.
    Further analysis of prompt ablations is needed to identify optimal initial
prompt and the possible extension of the system with “tool calls” and presenting
an MCP (Model Context Protocol) interfaces for the compilar and verifier.
    Authors plan extending the implementation of Eiffel-tools and analysing per-
formance of new code actions.


References
 1. M. S. Patil, G. Ung, and M. Nyberg, “Towards specification-driven llm-based
    generation of embedded automotive software,” in Bridging the Gap Between AI and
    Reality: Second International Conference, AISoLA 2024, Crete, Greece, October
    30 – November 3, 2024, Proceedings. Berlin, Heidelberg: Springer-Verlag, 2025,
    p. 125–144. [Online]. Available: https://doi.org/10.1007/978-3-031-75434-0_9
 2. B. Meyer, Handbook of Requirements and Business Analysis. Springer, 2022, vol.
    277.
 3. ——, “Applying design by contract,” Computer, vol. 25, no. 10, pp. 40–51, 2002.
 4. S. Joel, J. J. Wu, and F. H. Fard, “A survey on llm-based code generation
    for low-resource and domain-specific programming languages,” 2025. [Online].
    Available: https://arxiv.org/abs/2410.03981
 5. A. Schena, “eiffel-tools,” 2025. [Online]. Available: https://github.com/alschena/
    eiffel-tools.git
 6. B. Meyer, “Eiffel: A language and environment for software engineering,” Journal
    of Systems and Software, vol. 8, no. 3, pp. 199–246, 1988.
 7. J. Tschannen, C. A. Furia, M. Nordio, and B. Meyer, “Automatic verification of
    advanced object-oriented features: The autoproof approach,” in Tools for Practical
    Software Verification - LASER 2011, International Summer School, ser. LNCS,
    vol. 7682. Springer, 2012, pp. 134–156.
 8. K. R. M. Leino, “This is boogie 2,” manuscript KRML, vol. 178, no. 131, p. 9, 2008.
 9. C. Microsoft, Red Hat, “Language server protocol,” 2016, accessed: 2025-08-11.
    [Online]. Available: https://github.com/microsoft/language-server-protocol.git
10. V. A. Braberman, F. Bonomo-Braberman, Y. Charalambous, J. G. Colonna,
    L. C. Cordeiro, and R. de Freitas, “Generative transformations and patterns in
    llm-native approaches for software verification and falsification,” 2025. [Online].
    Available: https://arxiv.org/abs/2404.09384
11. X. Hou, Y. Zhao, Y. Liu, Z. Yang, K. Wang, L. Li, X. Luo, D. Lo, J. Grundy, and
    H. Wang, “Large language models for software engineering: A systematic literature
    review,” ACM Transactions on Software Engineering and Methodology, vol. 33,
    no. 8, pp. 1–79, 2024.
12. Z. Zhang, C. Chen, B. Liu, C. Liao, Z. Gong, H. Yu, J. Li, and R. Wang,
    “Unifying the perspectives of nlp and software engineering: A survey on language
    models for code,” 2024. [Online]. Available: https://arxiv.org/abs/2311.07989
13. A. Fan, B. Gokkaya, M. Harman, M. Lyubarskiy, S. Sengupta, S. Yoo, and
    J. M. Zhang, “Large language models for software engineering: Survey and open
    problems,” 2023. [Online]. Available: https://arxiv.org/abs/2310.03533
14. L. A. Agrawal, A. Kanade, N. Goyal, S. K. Lahiri, and S. K. Rajamani, “Guid-
    ing language models of code with global context using monitors,” arXiv preprint
    arXiv:2306.10763, 2023.
                                     LLMs and LSP: a match made in context            19

15. N. Polikarpova, I. Ciupa, and B. Meyer, “A comparative study of programmer-
    written and automatically inferred contracts,” in Proceedings of the eighteenth in-
    ternational symposium on Software testing and analysis, 2009, pp. 93–104.
16. Y. Wei, C. A. Furia, N. Kazmin, and B. Meyer, “Inferring better contracts,” in
    Proceedings of the 33rd International Conference on Software Engineering, 2011,
    pp. 191–200.
17. M. D. Ernst, J. H. Perkins, P. J. Guo, S. McCamant, C. Pacheco, M. S. Tschantz,
    and C. Xiao, “The daikon system for dynamic detection of likely invariants,” Science
    of computer programming, vol. 69, no. 1-3, pp. 35–45, 2007.
18. Y. Pei, “Automatic fixing of programs with contracts,” Ph.D. dissertation, ETH
    Zurich, 2015.
19. L. Huang, B. Meyer, I. Mustafin, and M. Oriol, “Execution-free program repair,” in
    Companion Proceedings of the 32nd ACM International Conference on the Foun-
    dations of Software Engineering, 2024, pp. 517–521.
20. B. Meyer, I. Ciupa, A. Leitner, and L. L. Liu, “Automatic testing of object-oriented
    software,” in SOFSEM 2007: Theory and Practice of Computer Science: 33rd Con-
    ference on Current Trends in Theory and Practice of Computer Science, Harra-
    chov, Czech Republic, January 20-26, 2007. Proceedings 33. Springer, 2007, pp.
    114–129.
21. T. Le-Cong, B. Le, and T. Murray, “Can llms reason about program semantics?
    a comprehensive evaluation of llms on formal specification inference,” in Proceed-
    ings of the 63rd Annual Meeting of the Association for Computational Linguistics
    (Volume 1: Long Papers), 2025, pp. 21 991–22 014.
22. L. Huang, I. Mustafin, M. Piccioni, A. Schena, R. Weber, and B. Meyer,
    “Do ai models help produce verified bug fixes?” 2025. [Online]. Available:
    https://arxiv.org/abs/2507.15822
23. I. Mustafin, “tree-sitter-eiffel,” 2024, accessed: 2025-07-04. [Online]. Available:
    https://github.com/imustafin/tree-sitter-eiffel
24. M. Brunsfeld, “Tree-sitter,” 2018. [Online]. Available: https://github.com/
    tree-sitter/tree-sitter
25. Anthropic, “Introducing claude sonnet 4.6,” 2026, [accessed 04-Jun-2026]. [Online].
    Available: https://www.anthropic.com/news/claude-sonnet-4-6
26. OpenAI, “GPT-5 nano model,” 2026, [accessed 04-Jun-2026]. [Online]. Available:
    https://developers.openai.com/api/docs/models/gpt-5-nano
27. J. Abadji, M. Abdin, C. Adams, E. Alcaide, M. Altun, M. Artoni, J. Bao, U. Barar,
    V. Bekiaris, A. Bessonov et al., “Laguna m. 1/xs. 2 technical report,” arXiv preprint
    arXiv:2605.27605, 2026.
28. A. Nilizadeh, G. T. Leavens, X.-B. Le, C. S. Pasareanu, and D. Cok, “Exploring
    true test overfitting in dynamic automated program repair using formal methods
    (in press),” in 2021 14th IEEE Conference on Software Testing, Validation and
    Verification (ICST). IEEE, 2021.
29. G. T. Leavens, A. L. Baker, and C. Ruby, “Jml: A notation for detailed design,”
    Behavioral specifications of businesses and systems, pp. 175–188, 1999.
30. I. Mustafin, A. Schena, and R. Weber, “buggy-java-jml-eiffel,” Feb. 2024. [Online].
    Available: https://github.com/CI-CSE/buggy-java-jml-eiffel
31. T.-T. Nguyen, Q.-T. Ta, and W.-N. Chin, “Automatic program repair using formal
    verification and expression templates,” in International Conference on Verification,
    Model Checking, and Abstract Interpretation. Springer, 2019, pp. 70–91.
32. I. Mustafin, A. Schena, and R. Weber, “maple-recursive-eiffel,” Feb. 2024. [Online].
    Available: https://github.com/CI-CSE/maple-recursive-eiffel
