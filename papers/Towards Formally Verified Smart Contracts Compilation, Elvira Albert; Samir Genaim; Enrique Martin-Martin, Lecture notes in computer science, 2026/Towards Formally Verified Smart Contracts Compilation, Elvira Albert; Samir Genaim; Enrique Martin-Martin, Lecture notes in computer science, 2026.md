              Towards Formally Verified Smart
                  Contracts Compilation

          Elvira Albert, Samir Genaim, and Enrique Martin-Martin(B)

                  Complutense University of Madrid, Madrid, Spain
                  elvira@fdi.ucm.es, {sgenaim,emartinm}@ucm.es



       Abstract. Many compilation stages of smart contracts on the Ethereum
       blockchain have been transitioned to the intermediate language YUL.
       Tasks such as smart contract optimization and bytecode generation are—
       or will soon be—performed directly at the YUL level in the compilers for
       the higher-level languages such as Solidity. In this paper, we develop
       a formal semantics of YUL programs in Rocq, suitable for veriﬁcation,
       which allows formal reasoning at the level of YUL code or generation
       tools processing YUL programs. Our semantics is expressive enough to
       be the basis for formal veriﬁcation tools, and simple enough to make
       the development of such tools feasible. In order to prove its adequacy
       for veriﬁcation, we develop in Rocq a checker (and associated soundness
       proofs), based on our semantics, able to verify the results of the live-
       ness analysis stage of the oﬃcial Solidity compiler solc, which opens the
       door towards formally veriﬁed Ethereum’s smart contracts compilation.
       Experiments on more than 1,500 smart contracts show that we are able
       to automatically verify solc’s liveness analysis results in negligible time.


1    Introduction

Smart Contracts. Ethereum [36] is a decentralized blockchain with smart con-
tract functionality. A smart contract is a self-executing program that auto-
mates the actions required in a blockchain transaction, eliminating the need for
a central authority or intermediary. Once transactions are done, they are trace-
able and cannot be undone. Because smart contracts execute agreements, they
can be used for many diﬀerent purposes: the smart contracts introduced by
Ethereum are considered a fundamental building block for decentralized ﬁnance
(DeFi) and non-fungible token (NFT) applications. On Ethereum, smart con-
tracts are written in Turing-complete programming languages—such as Solidity
[8], Vyper [18] or Fe [1]—and compiled into low-level bytecode to be executed
by the Ethereum Virtual Machine [36] (EVM). Even though smart contracts are
stored on secure blockchains like Ethereum, they are not immune to security
E. Martin-Martin, S. Genaim and E. Albert—Supported partially by Ethereum Foun-
dation (Grant ID AOC-2616), Spanish MCI, AEI, FEDER (EU) projects PID2021-
122830OB-C41, PID2024-157044OB-C31, TEC-2024/COM-235 and PR17/24-31926
Funded By Madrid(UCM Action-6th Framework.
 c The Author(s) 2026
A. Sampaio and M. Stoelinga (Eds.): FM 2026, LNCS 16557, pp. 255–274, 2026.
https://doi.org/10.1007/978-3-032-26220-2_13
256    E. Albert et al.

threats. Attackers can exploit code vulnerabilities to steal funds or manipulate
contract execution.

Towards Verified Compilation. Formal methods are playing a fundamental role
to guarantee security before deploying smart contracts (see [11,15, 17,19, 20,22,
31, 34] and their references), and thus ensure safe transactions. Our focus is on
the development of veriﬁed optimization and compilation tools which increase
the trustworthiness of the compiled bytecode. Many compilation stages of smart
contracts on the Ethereum blockchain have been transitioned to the intermediate
language YUL [9]. The motivation behind YUL is to have a common representa-
tion for the analysis and optimization stages that can beneﬁt all target platforms
equally. By means of the so-called dialect [9], YUL can be compiled to bytecode
for diﬀerent backends. Tasks such as smart contract optimization and EVM code
generation are—or will soon be—performed directly at the YUL level in the com-
pilers for the higher-level languages such as Solidity, Vyper or Fe compilers.

Formal Verification. As security requirements are critical today in many con-
texts, formal veriﬁcation has taken an essential role in the software engineer-
ing process to verify and/or certify formal speciﬁcations of the software behav-
ior. In order to formally verify the correctness of an analysis or optimization,
one can develop a formally veriﬁed tool using machine-assisted mathematical
proofs (such as done in the Compert certiﬁed compiler [25]), or follow the trans-
lation validation approach [35] in which each of the analysis or optimization
results are formally checked to be correct using a veriﬁed checker (as applied
e.g. in [12,16,27, 28,32, 33]). As EVM compilers—and their built-in analyses and
optimizers—are continuously evolving, translation validation is the most suit-
able approach until the languages and tools stabilize. The last years have wit-
nessed the development of powerful proof assistants such as Rocq (formerly
known as Coq) [14,21], Lean [29], and Isabelle/HOL [30] which provide a formal
language to write mathematical deﬁnitions, executable algorithms and theorems
together with environments for semi-interactive development of machine-checked
proofs.

Contributions. The goal of this paper is to develop a formal semantics of YUL in
Rocq and showcase its adequacy for veriﬁcation by applying it to verify the
soundness of the liveness analysis results of the most-widely used Solidity com-
piler, solc [3]. A liveness analysis aims at determining the lifetime of each vari-
able in the program, i.e., the points from which an execution can reach an instruc-
tion where each variable is used. It is a fundamental analysis in the development
of a compiler, as several compiler analyses need to know the lifetime of vari-
ables (e.g., deadcode elimination, register allocation, etc.). Our work is a ﬁrst
major step towards the long-term goal of the Ethereum community of having
all optimization and static analysis tools for YUL programs veriﬁed using a proof
assistant. The main contributions of the paper are:
                    Towards Formally Veriﬁed Smart Contracts Compilation        257

1. YUL formal semantics. We develop a formal semantics of YUL programs in
   Rocq that is suitable for veriﬁcation as it allows formal reasoning at the level
   of YUL code and of the analysis/optimization tools processing YUL programs.
2. Verification of liveness analysis results. We develop a checker based on our
   semantics to verify the results of the liveness static analysis phase in the solc
   compiler, which opens the door towards formally veriﬁed Ethereum’s smart
   contracts compilation.
3. Implementation and experimental evaluation. Our implementation, named
   FORYU [6,10], includes the semantics and checker, it is open-source and pub-
   licly available. Experimental evaluation on the large-scale set of 1,550 smart
   contracts utilized for regression testing by the solc development team [7]
   demonstrates the practicality of our approach: the veriﬁcation process for the
   liveness analysis results takes on average 3ms per smart contract.


2   An Overview of Verified Smart Contract Compilation
This section provides preliminary background on Ethereum smart contracts [36],
their intermediate YUL representation [3], and it overviews the general framework
for veriﬁed smart contracts compilation with the FORYU components.
YUL-IR as a Common Analysis/Optimization Target. A smart contract can be
seen as a collection of functions whose executions are invoked in the Ethereum
transactions. A so-called transaction can execute any public function of the con-
tract, and it may terminate successfully, but also in an error, or revert status
(the latter undoing the contract state changes). Regarding the implementation
of the functions, besides the regular types of instructions used by any high-
level programming language (e.g., assignments, conditionals, iterative constructs,
etc.), there are speciﬁc instructions that communicate to the blockchain (e.g.,
sstore that modiﬁes the contract storage that is replicated in the blockchain),
and instructions to invoke other contracts. There coexist several high-level lan-
guages to program Ethereum smart contracts: while Solidity is the most popular,
Vyper is also widely used, and Fe is being proposed as the next generation lan-
guage. In order to unify eﬀorts, YUL has been proposed as a common intermediate
language to carry out contract optimization and bytecode generation in the com-
pilers for the diverse higher-level languages. Figure 1 provides an overview of the
overall veriﬁcation framework, where we can see on the left (component 1 )
that smart contracts written in the diﬀerent languages are ﬁrst translated to the
YUL-IR. The core idea proposed by Ethereum is that the Analysis+Optimization
component 4 (that outputs in 5 Liveness, Constancy, Dependencies and any
other current or future analysis/optimization) is done at the intermediate lan-
guage YUL so that it can be shared by all high-level compilers and only the ﬁrst
translation stage Trans 1 needs to be speciﬁcally developed, as shown in the
ﬁgure.

The YUL-IR in CFG-SSA Form. The YUL-IR obtained from the source program
must be provided by the compilers in CFG (Control Flow Graph) and SSA
258     E. Albert et al.




       Fig. 1. An overview of veriﬁed compilation with the FORYU components.


(Single Static Assignment) form 2 , named CFG-SSA in what follows. Basically,
in such YUL-IR in CFG-SSA form, each function in the smart contract is repre-
sented by means of a CFG whose blocks contain a sequence of instructions in
SSA and a set of φ-functions to handle joint points in the CFG. As usual, there is
an entry block and we have conditional and unconditional jumps between blocks,
and terminal (or exit) blocks. It is widely known that SSA is a type of inter-
mediate representation (IR) where each variable is assigned exactly once, used
in most high-quality optimizing compilers for imperative languages, including
LLVM, and many commercial compilers. Converting ordinary code into SSA
form is done by replacing the target of each assignment with a new variable, and
replacing each use of a variable with the new version of the variable reaching
that point. A φ-function for a variable is not needed when only one version of
the variable is reaching a joint point in the CFG. When there is ambiguity, the
φ-function is used to combine the values from diﬀerent control ﬂow paths into
a single variable, using the incoming edge to determine which source value to
select. The usual notation to declare a φ-function is a0 = φ(B1 : a1 , . . . , Bn : an )
meaning that a0 takes the value of ai when the control ﬂows from block Bi with
i = 1, . . . , n.

Example 1. The left side of Fig. 2 shows a smart contract in the standard YUL-IR
given by the solc compiler. It includes a function cal, and the contract’s entry
code. This contract calculates the interest over a speciﬁc period given an initial
balance. We can see that the YUL code contains the high-level instructions for
the control ﬂow (for loops and if conditional) while it uses the EVM opcodes
for the operations (e.g., div, add, etc.) and for storage accesses (e.g., sstore).
On the right of the ﬁgure, we have the YUL-IR in CFG-SSA form for the function
cal exactly as generated by solc. In this form, the control ﬂow is explicit by
means of the CFG blocks (e.g., the inner loop is represented by blocks B5-B8,
and the outer loop by block B1-B4) that are connected to their continuations by
means of conditional jumps (e.g., the continuation from B1 depends on condition
                    Towards Formally Veriﬁed Smart Contracts Compilation        259

v8 in the outgoing labels) or unconditional (e.g., B8 to B3). Besides, an SSA-
transformation has been performed and φ-functions introduced at joint blocks
when needed (e.g., in B1 and B5). At the CFG level, variables v0–v3 are the
input parameters of cal, and in block B4 the value of variable v23 is returned.
    Our FORYU semantics 3 is deﬁned at the level of the CFGs (example on the
right of ﬁgure) instead of at the pure abstract syntax tree (AST) representation
of YUL programs (on the left), because optimizations and analysis are more
eﬃcient when developed at the CFG-SSA level and it is the current trend on the
ongoing Ethereum developments. While our semantics could be used for dynamic
execution by providing a concrete initial state, our focus is on its use within the
FORYU veriﬁer 6 . The veriﬁer takes the YUL-IR 2 and the analysis results 5 to
be veriﬁed (our current implementation works on the liveness analysis output,
future plans include all analyses) and it returns     if correctness is proven.




  Fig. 2. Left: YUL-IR for smart contract. Right: CFG-SSA form for function cal.



Dialects in the YUL-IR . To keep the language simple and ﬂexible, YUL does not
have any built-in operation, functions or types in its pure form. These are added
together with their semantics when specifying the so-called dialect of YUL, which
allows specializing YUL to the requirements of diﬀerent target platforms and
feature sets. Currently, there is only one oﬃcial dialect of YUL, which uses the EVM
opcodes as builtin functions and deﬁnes only the type u256, which is the native
256-bit type of the EVM (named EVM/prague in the ﬁgure). There are ongoing
projects though aiming at including other dialects (e.g., the EVM/shanghai that
is a speciﬁc version of the EVM to handle the Shanghai hard fork). It can be
observed in the ﬁgure on the right 7 that code generation backends can be
developed for speciﬁc target code. The YUL-IR of the example in Fig. 2 uses the
standard EVM dialect [36], e.g., the EVM opcode add is used in the YUL code for
addition, sstore for a write access in the blockchain storage, etc.
260      E. Albert et al.

3     The Rocq YUL-Semantics
This section deﬁnes a YUL-formal semantics that is expressive enough to be
the basis for formal veriﬁcation tools, and at the same time, simple enough
to make the development of such tools feasible. This is not simply a matter
of choosing a semantics from among the existing possibilities in the ﬁeld of
programming languages, such as small-step or big-step, but also has to do with
the fundamentals of how programs and states are represented and how the data
structures are used, as these aﬀect the feasibility of writing proofs for related
formal statements. We start by modeling the YUL syntax in Rocq and then we
present the essential parts of our semantics based on such YUL models.

3.1    Modeling YUL Syntax
Let us ﬁrst deﬁne the representation of YUL dialects and then model smart con-
tracts. The provided code snippets include only the essential details, with addi-
tional explanations integrated via comments. The next Rocq Module Type deﬁnes
the interface for a YUL dialect. It speciﬁes the parameters (data types, func-
tions, and propositions) that any concrete dialect implementation must provide.

Module Type DIALECT.
  Parameter value_t : Type. (* Type of basic values *)
  Parameter opcode_t : Type. (* Inductive data type of supported opcodes *)
  Parameter dialect_state : Type. (* The dialect state *)

    Parameter default_value : value_t. (* Value for initializing variables *)
    Parameter is_true_value: value_t → bool. (* Value representing true *)
    Parameter is_false_value: value_t → bool. (* Value representing false *)
    Parameter equal_values: value_t → value_t → bool. (* Equality check *)

  Parameter execute_op_code : (* Execute an opcode *)
      dialect_state → opcode_t → list (value_t) →
      (list value_t ∗ dialect_state ∗ Status.t).
  ...
End DIALECT.

    All dialect operations are deﬁned by the inductive type opcode_t and manip-
ulate data of type value_t. The dialect_state parameter deﬁnes the type for the
dialect-speciﬁc state, e.g., the diﬀerent types of storage that the EVM has (EVM
uses a heap and the replicated storage). The core functionality is provided by
the execute_op_code function. It takes the current dialect state, an opcode, and
a list of input values. It returns a new dialect state, a list of output values, and
an execution status. This status is deﬁned by the following Rocq module:

Module Status.
  Inductive t : Type :=
  | Running : t | Terminated : t     | Reverted : t   | Error : string → t.
End Status.
                      Towards Formally Veriﬁed Smart Contracts Compilation          261

    We have implemented the EVM dialect as a module called EVMDialect, and it
is based on the semantics deﬁned in [4,5].
    A smart contract is modeled using the following Rocq module,1 which is
parameterized over a speciﬁc dialect D.

Module SmartContract (D: DIALECT).
  Record t : Type := {
      name : string; (* Its name *)
      functions : list Function(D).t; (* List of functions *)
      main: FuncName.t; (* The name of the main function *)
  }.
  ...
  Definition valid_sc: t → Prop := ... (* validity of smart contracts*)
End SmartContract.

    The core type for a smart contract is SmartContract.t, deﬁned as a Record.
This record encapsulates the contract’s name, a list of its functions, and the
main function name (textttFuncName.t is deﬁned as a string). The valid sc
parameter enforces structural validity, requiring, among other conditions, that
all included functions are valid and that their names are unique. The functions
in the contract are modeled using the following Rocq module.

Module Function (D: DIALECT).
  Record t : Type := {
      name : FuncName.t; (* Its name *)
      arguments : list YULVariable.t; (* Input parameters *)
      blocks : list Block(D).t; (* List of blocks *)
      entry_block_id : BlockID.t; (* The ID of the entry block. *)
  }.
  ...
  Definition valid_f: t → Prop := ... (* validity of functions *)
End Function.

    The core type for a function is Function.t, and it includes its name, a list of
input parameters (where YULVariable.t is a unique nat identiﬁer modeling a
variable), and the identiﬁer of the initial block (BlockID.t is nat). The valid f
parameter enforces structural validity, requiring, among other conditions, that
all blocks have unique identiﬁers. A block in (the CFG of) a function is modeled
using the following Rocq module.

Module Block (D: DIALECT).
  Record t : Type := {
    bid : BlockID.t; (* The block’s identifier (nat) *)
    instructions : list (Instruction(D).t); (* Its list of instructions *)
    exit_info : ExitInfo(D).t; (* Its kind: branching, return, etc. *)
1
    For the sake of conciseness and clarity, we use expressions such as Function(D) to
    denote the instantiation of the Function module with parameter D, which is not valid
    Rocq syntax. The code available at [6] contains the actual (less compact) syntax.
262    E. Albert et al.

      phi_function : PhiInfo(D).t; (* Phi function used CFG-SSA *)
  }.
  ...
End Block.

    The core type for a block is Block.t, and it includes a block identiﬁer, a list
of instructions, information on how to exit the block, and a φ-function that is
used to model CFG-SSA’s. Instructions are modeled as follows.

Module SimpleExpr (D: DIALECT).
  Definition t : Type := YULVariable.t + D.value_t. (* Variable or value *)
End SimpleExpr.

Module Instruction (D: DIALECT).
  Inductive other_inst_t : Type := | ASSIGN.

  Record t : Type := {
     input : list SimpleExpr(D).t; (* Input expressions *)
     output : list YULVariable.t; (* Output variables *)
     op : FuncName.t + D.opcode_t + other_inst_t; (* Operation *)
  }.
End Instruction.

    The core type for an instruction is Instruction.t, and it includes a list of
input simple expressions, a list of output variables, and an opcode that can be
a function name, a dialect opcode or an assignment. The exit information of a
block is modeled using the following Rocq module.

Module ExitInfo (D: DIALECT).
  Inductive t : Type :=
  | CondJump (v : YULVariable.t) (bid_t bid_f: BlockID.t) (* Conditional jump *)
  | Jump (bid : BlockID.t) (* Jump to block bid *)
  | ReturnBlock (rs : list SimpleExpr(D).t) (* Return the values of rs *)
  | Terminated. (* Terminate the execution *)
End ExitInfo.

   The core type for exit information is ExitInfo.t, and it indicates how the
execution proceeds when reaching the end of a block, in particular, the next
block for the case of CondJump is decided depending on whether the value of
variable v is true or false. Finally, a φ-function is modeled using the following
Rocq module.

Module PhiInfo (D: DIALECT).
  Definition t := BlockID.t → list (YULVariable.t ∗ SimpleExpr(D).t).
End PhiInfo.

   The core type for a φ-function is PhiInfo.t, and it maps each incoming
block identiﬁer to a list of pairs (v,e) meaning that when the execution comes
from the corresponding block, variable v should be assigned the value of e.
                   Towards Formally Veriﬁed Smart Contracts Compilation       263

3.2   The Rocq Small-Step Semantics

We ﬁrst explain how the states are modeled using the following Rocq module,
which is parameterized over a speciﬁc dialect D.

Module State(D: DIALECT).
  Record t : Type := {
      call_stack : CallStack(D).t; (* The call stack for functions calls *)
      status : Status.t; (* The status of the execution *)
      dialect_state : D.dialect_state; (* The dialect state *)
  }.
  ...
End Module

    The core type for YUL states is State.t, and it encapsulates a call stack,
the status of the execution, and a dialect state that is entirely managed by the
dialect D. The variable mapping, stack frame, and call stack are core components
for tracking program execution and are modeled in Rocq as follows.

Module VarMap (D: DIALECT).
  Definition t := YULVariable.t → D.value_t. (* Maps variables to values *)
  ...
End VarMap

Module StackFrame(D: DIALECT).
  Record t : Type := {
      func_name: FuncName.t; (* The function owning the frame *)
      curr_bid: BlockID.t; (* The currently block executing *)
      pc : nat; (* Position of the next instructions in the current block *)
      vars_map : VarMap(D).t; (* Mapping variables to values *)
  }.
  ...
End StackFrame.

Module CallStack(D: DIALECT).
  Definition t := list StackFrame(D).t. (* Stack of frames *)
  ...
End CallStack.

    The call stack is modeled as a list of frames, acting as a stack. Each frame
contains the following execution context: the name of the function that owns
the frame (the function called when the frame was created), the identiﬁer of the
block currently executing, the pc (program counter) index of the next instruction
to execute, and a map assigning values to local variables.
    The small-step semantics is modeled using the following SmallStep module.
264     E. Albert et al.


Module SmallStep (D: DIALECT).
  ...
  (* Performs a single execution step *)
  Definition step (s: State(D).t) (p: SmartContract(D).t) : State(D).t :=
      match s.(State(D).status) with
      | Status.Running ⇒
        match get_next_instruction s p with
        | None ⇒ handle_block_finish s p
        | Some instruction ⇒ execute_instr instruction s p
        end
      | _ ⇒s
      end.

  (* Performs n execution steps *)
  Fixpoint eval (n: nat) (s: State(D).t) (p: SmartContract(D).t) : State(D).t := ...
End Module

    Function step performs a single execution step as follows. If the state’s sta-
tus is not Running, it returns the current state since no transition can be made
(we could prohibit this by deﬁnition as well, but keeping it this way simpli-
ﬁes the formalization). If the state status is Running and there is a next instruc-
tion to execute, we execute it using execute instr, and if there is no next
instruction it means that the execution is at the end of a block and we use
handle block finish to handle this case. Function eval simply executes step
in a loop n times.


4     Verified Liveness Analysis

Notation. A program point (pp) is identiﬁed by the triple (fname,bid,pc), and it
is typically associated with a speciﬁc stack frame to indicate the next instruc-
tion to be executed within that frame. The VarSet module implements a set of
YULVariable.t elements along with relevant set operations.


4.1    Formal Definition of Dead Variable in Rocq

A variable v is considered dead at a program point pp if its value does not
aﬀect any future execution outcome starting from pp. This concept is commonly
modeled as: If an execution starting from state st1 at program point pp (in the
top stack frame) reaches state st1’ in n steps, then starting from any state st2
that is identical to st1 except for the value of v, an execution of n steps will reach
state st2’ such that, (i) st1’ and st2’ are at the same program point (relative
to the top stack frame); and (ii) the values of all variables that will be accessed
in the immediate next step (including instruction inputs, conditional variables, or
return variables) are the same in st1’ and st2’. We now formalize this notion of
                    Towards Formally Veriﬁed Smart Contracts Compilation          265

dead variable.2 This requires deﬁning several propositions about the equivalence
of states up to the value of a variable v. The ﬁrst of such propositions3 deﬁnes the
conditions under which two stack frames, sf1 and sf2, are considered equivalent
up to the value of v at a given program point (fname,bid,pc). This requires that
all variables, except possibly v, hold the same values in both frames, and that
the program point of both frames is (fname,bid,pc).

Definition same_pp (fname: FuncName.t) (bid: BlockID.t) (pc: nat)
                           (sf1 sf2: StackFrame(D).t) :=
  sf1.func_name = fname ∧ sf2.func_name = fname ∧
  sf1.curr_bid = bid ∧ sf2.curr_bid = bid ∧ sf1.pc = pc ∧ sf2.pc = pc.

Definition equiv_frames_up_to_v (fname: FuncName.t) (bid: BlockID.t) (pc: nat)
  (v: YULVariable.t) (sf1 sf2: StackFrame(D).t) :=
  same_pp fname bid pc sf1 sf2 ∧
  ∀ v’, v’ = v → (* equality is required for variable different from v *)
     VarMap.get sf1.vars_map v’ = VarMap.get sf2.vars_map v’.

    The next proposition deﬁnes when two states, st1 and st2, are considered
equivalent up to the value of variable v at a given program point (fname,bid,pc).
This equivalence holds when the following conditions are met: the status and
underlying dialect states must be equivalent; the top stack frames must be equiv-
alent up to the value of v and at (fname,bid,pc); and all remaining (deeper) frames
in the call stack must be identical.

Definition equiv_states_up_to_v (fname: FuncName.t) (bid: BlockID.t) (pc: nat)
                                 (v: YULVariable.t) (st1 st2: State(D).t) :=
  (length st1.call_stack > 0) ∧
  st1.status = st2.status ∧ st1.dialect_state = st2.dialect_state ∧
  ∃ sf1 sf2 rsf,
     st1.call_stack = sf1::rsf ∧ st2.call_stack = sf2::rsf ∧
     equiv_frames_up_to_v fname bid pc v sf1 sf2.

   The next proposition formally deﬁnes a set of variables (s) that includes
precisely those variables which are immediately accessed in the next execution
step, given the block (b) and program counter (pc). This deﬁnition distinguishes
between two cases: when pc points to an instruction within the block, and when
pc points to the end of the block.

Definition accessed_vars (b: Block(D).t) (pc: nat) (s: VarSet.t) :=
  ( pc = (length b.instructions) ∧ (* end of block *)
    match b.exit_info with
    | ExitInfo(D).CondJump cv _ _ ⇒
2
   This is a simpliﬁed version (for the sake of clarity) of a more general property
  we have formally proven in [6]. In module fm26.v we prove that this version is an
  instance of the general property.
3
  For clarity, we will use the notation register.field name to denote access to a ﬁeld
  of a record, as in sf1.func name.
266      E. Albert et al.

         VarSet.Equal s (VarSet.add cv VarSet.empty) (* cv is accessed *)
      | ExitInfo(D).ReturnBlock rvs ⇒
         VarSet.Equal s (list_sexp_to_varset rvs) (* rs are accessed *)
      | _ ⇒ VarSet.Equal s VarSet.empty (* nothing is accessed *)
      end )
 ∨
 ( pc < (length b.instructions) ∧ (* within the block *)
   exists instr,                (* instr.input are accessed *)
     nth_error b.instructions pc = Some instr ∧
     (VarSet.Equal s (list_sexp_to_varset instr.input)) ).

   The next proposition states that the top stack frames of states st1 and st2
agree on the values of all variables that are immediately accessed.

Definition equiv_top_frame (p: SmartContract(D).t) (st1 st2: State(D).t) :=
  match st1.call_stack, st2.call_stack with
  | nil,nil ⇒ True (* both call stacks are empty *)
  | sf1:: _, sf2:: _ ⇒ (* top frames agree on values of accessed variables *)
       let fname := sf1.func_name in
       let bid := sf1.curr_bid in
       let pc := sf1.pc in
         same_pp fname bid pc sf1 sf2 ∧
         ∀ v s b,
             SmartContract(D).get_block p fname bid = Some b →
             accessed_vars b pc s →
             VarSet.In v s →
             VarMap.get sf1.vars_map v = VarMap.get sf2.vars_map v
  | _, _ ⇒ False (* one of the call stacks is empty *)
 end.

   Finally, the following proposition formally deﬁnes the conditions under which
a variable v is considered dead at a given program point (fname,bid,pc), it relies
on the eval function deﬁned in the semantics in Sect. 3.

Definition dead_variable (p: SmartContract(D).t) (fname: FuncName.t)
  (bid: BlockID.t) (pc: nat) (v: YULVariable.t) :=
    ∀ (st1 st2 st1’: State(D).t) (n: nat),
       equiv_states_up_to_v fname bid pc v st1 st2 →
       SmallStep(D).eval n st1 p = st1’ →
       ∃ st2’,
         SmallStep(D).eval n st2 p = st2’ ∧ equiv_top_frame p st1’ st2’.

    A variable that is not dead is called live. We typically compute an over-appro-
ximation of live variables and thus any variable not declared live by the analysis
is considered dead (i.e., we get an under-approximation for dead variables).
    Note that the above deﬁnition includes a universal quantiﬁcation on the
length of the trace, meaning that the variable is not accessed independently of
that length, and thus also covers non-terminating programs. The same reasoning
holds for non-deterministic programs; however, in the context of blockchain,
                        Towards Formally Veriﬁed Smart Contracts Compilation                 267

determinism is an essential requirement and hence non-determinism is left out
of our formalization.

4.2    Formally Verified Liveness Checker
Our goal is to check that the results of a liveness analysis are sound, i.e., if a
program point (fname,bid,pc) is associated with a set s of live variables, then any
variable not in s must satisfy the dead variable proposition.
    At the level of YUL-IR in CFG-SSA form, the liveness analysis infers sets of live
variables at the entry (IN) and exit (OUT) of each block (called live-in and live-
out sets), and as typical in any liveness analysis is based on solving the following
set of equations:

                            retvars(b)                b is a terminal block
             OUT(b) =
                            ∪i φ−1
                                bi (b, IN(bi ))       b has successor b1 , . . . , bn         (1)
               IN(b) = BKW(instrs(b), OUT(b) ∪ condvars(b))

The equations deﬁne the live-out set OUT of a block b based on whether it is a
terminal block: (i) If the block is terminal, its live-out set is simply the set of
returned variables (retvars(b)), if any exist; and (ii) If the block is non-terminal,
its live-out set is the union of the live-in IN sets of all its successor blocks after
appropriate variable renaming using the inverse of the corresponding φ-functions.
The live-in set of a block b is obtained by propagating backwards (BKW) the
live-out set of the block, after adding conditional jump variable (condvars(b)),
if any exists. The propagation is done instruction by instruction in the block
(instrs(b)), by removing the updated variables (denoted by def(i)) and adding
the accessed variables (denoted by used(i)) as follows:

          BKW(l, s) = if l = i :: l then BKW(l , (s \ def(i)) ∪ used(i)) else s

Note that we could also replace = by ⊇ in (1) to allow correct but less precise
over-approximations.

Example 2. The live-in and live-out sets for the blocks in the CFG of Fig. 2 are:
   live-in           live-out                live-in               live-out
B0 {v0,v1,v2,v3}     {v0,v1,v2,v3,v5}     B5 {v1,v2,v3,v7,v11,v15} {v1,v2,v3,v7,v11,v15}
B1 {v1,v2,v3,v7,v23} {v1,v2,v3,v7,v23}    B6 {v1,v2,v3,v7,v11,v15} {v1,v2,v3,v7,v11,v18}
                                                                                           Let us
B2 {v1,v2,v3,v7,v23} {v1,v2,v3,v7,v9,v23} B7 {v1,v2,v3,v7,v11,v18} {v1,v2,v3,v7,v18,v20}
B3 {v1,v2,v3,v7,v15} {v1,v2,v3,v15,v25} B8 {v1,v2,v3,v7,v15}       {v1,v2,v3,v7,v15}
B4 {v23}             {v23}

explain some of the blocks: (i) Block B4 is a return block, so its live-out set
includes only the return variable v23, and its live-in set is equal to its live-
out set since it does not have instructions. (ii) The live-out set of block B2
is obtained from the live-in of B5 after renaming v11 and v15 to v9 and v23
respectively (according to the φ-function). (iii) The live-in set of B6 is obtained
by propagating its live-out set backwards, which removes variable v18 since it
268     E. Albert et al.

is updated and adds v15 since it is accessed. (iii) The live-out set of B5 is the
union of the live-in sets of its successors B6 and B8.
    The equations in (1) can be modeled in Rocq using the following CoInductive
data-type (we do not show all cases).

CoInductive live_out (p: SmartContract(D).t) :
  FuncName.t → BlockID.t → VarSet.t → Prop :=
  (* Return block *)
  | lo_ret (fname: FuncName.t) (bid: BlockID.t) ... (sout: VarSet.t):
    SmartContract(D).get_block p fname bid = Some b → (* block exists *)
    Block(D).is_return_block b = Some rs → (* it is a return block *)
    VarSet.Equal sout (list_sexp_to_varset rs) →
    live_out p fname bid sout
  (* A block with a conditional jump *)
  | lout_cjump (fname: FuncName.t) (bid: BlockID.t) ... (sout: VarSet.t):
    SmartContract(D).get_block p fname bid = Some b →
    Block(D).is_cond_jump_block b = Some (cvar, bid_t, bid_f) →
    live_in p fname bid_t s1 →
    live_in p fname bid_f s2 →
    SmartContract(D).get_block p fname bid_t = Some b_t →
    SmartContract(D).get_block p fname bid_f = Some b_f →
    VarSet.Equal sout (VarSet.union (inv_phi b_t.phi_function bid) s1)
                                     (inv_phi b_f.phi_function bid) s2)) →
    live_out p fname bid sout
    ...
  with
  live_in (p: SmartContract(D).t): FuncName.t → BlockID.t → VarSet.t → Prop :=
  | lin (fname: FuncName.t) (bid: BlockID.t) ... (sout: VarSet.t):
    SmartContract(D).get_block p fname bid = Some b →
    live_out p fname bid s →
    VarSet.Equal sout (prop_bkw b.instructions (add_jump_var b s)) →
    live_in p fname bid sout.

    The ﬁrst case of the live out states that if a block is a return block with
rs as its return expressions, then the set of live-out variables is equivalent to
(list sexp to varset rs). This set precisely includes all variables in the list
rs. The second case of live out states that if the block is a conditional jump,
and s1 and s2 are the live-in sets for the next blocks, then the set of live-out
variables is equivalent to the union of s1 and s2 after applying the inverse
of the corresponding φ-functions. The case of live in states that if s is the
live-out set for the block, then the set of live-in variables is equivalent to propa-
gating s backwards after adding the condition variable if needed (in the case of
a block with conditional jump). The use of CoInductive instead of Inductive is
because some of the proofs rely on co-induction for the following reason: A direct
translation of the equations in (1) into a proof assistant like Rocq might initially
lean towards standard Inductive types. However, standard inductive deﬁnitions
construct strictly well-founded, ﬁnite derivation trees. To complete an induc-
tive proof for OUT(b) or IN(b), the derivation chain must physically terminate
                    Towards Formally Veriﬁed Smart Contracts Compilation        269

at a deﬁnitive base case, e.g., a terminal block where OUT(b) = retvars(b).
Because CFGs naturally contain cycles (loops), this well-foundedness require-
ment becomes a severe limitation. If block b has a successor bi , and bi contains
a back-edge leading to b, the evaluation of OUT(b) triggers an inﬁnite depen-
dency chain: OUT(b) → IN(bi ) → OUT(bi ) → · · · → OUT(b). To accommodate the
cyclic nature of CFGs, we model the equations using CoInductive types and use
co-indcution in the proofs.
    The following lemma guarantees that liveness information as deﬁned above is
sound. It states that the complement of live in is a safe under-approximation
of the set of dead variables for the corresponding program point. We could state
a similar statement for live out as well, but this is not needed since executions
that start at the beginning of a block pass through the end of the block (unless
there is a call to a non-terminating method or an error in a call to the dialect).


Lemma live_in_out_snd:
  ∀ p fname bid b s,
     SmartContract(D).get_block p fname bid = Some b →
     live_in p fname bid s →
     (∀ v, ¬ VarSet.In v s → dead_variable p fname bid 0 v).

    Now we move to verifying the correctness of a liveness analysis results, in
particular that they agree with the above live in and live out propositions.
We ﬁrst deﬁne two data types to represent the result of a liveness analysis. The
ﬁrst fun live info t is used for the liveness information of a function and it
maps blocks to their live-in and live-out sets. The second sc live info t is used
for a smart contract and it maps functions to their results.

Definition fun_live_info_t := BlockID.t → option (VarSet.t ∗ VarSet.t).
Definition sc_live_info_t := FuncName.t → option fun_live_info_t.

    The following proposition formally establishes when a given result of the
liveness analysis is sound. Essentially, the computed live-in and live-out sets must
be equal to those that satisfy the live in and live out propositions (although
requiring them to be a superset would be valid as well).

Definition liveness_info_snd (p: SmartContract(D).t) (r: sc_live_info_t) :=
  ∀ fname bid b f_r in_set out_set,
     SmartContract(D).get_block p fname bid = Some b →
     r fname = Some f_r →
     f_r bid = Some (in_set, out_set) →
     ( live_in p fname bid in_set ∧ live_out p fname bid out_set).

    Our liveness checker is a function liveness chk that takes a smart contract
and corresponding liveness analysis results, and returns true if the results are a
solution to the equation in (1). The lemma liveness chk snd cmp establishes
that this function is sound and complete, with the proof fully veriﬁed in Rocq:
270       E. Albert et al.


Definition liveness_chk (p: SmartContract(D).t) (r: sc_live_info_t) := ...

Lemma liveness_chk_snd_cmp:
∀ (p: SmartContract(D).t) (r: sc_live_info_t),
  SmartContract(D).valid p →
     ( liveness_info_snd p r ↔ liveness_chk p r = true).

    We note that our checker rejects liveness results that are not optimal, i.e.,
solutions to the equations in (1). As we have mentioned before, we could replace
= by ⊇ in (1) to allow correct but less precise over-approximations. This change
is straightforward both at the implementation level and in the corresponding
proofs.


5     Experimental Evaluation
The diﬀerent components of the FORYU veriﬁcation framework have been imple-
mented in the Rocq Prover (Coq v.8.20.1), as well as the complete proofs of
all the theoretical results (more than 100 proofs in around 9000 lines of Rocq
code). The source code, executables and benchmarks can be found at [6,10].
We have evaluated our implementation using the liveness analysis results pro-
duced by the oﬃcial Solidity compiler solc. To this end, we have fully auto-
mated the interaction between the compiler and the FORYU liveness veriﬁer by
applying the following four-step pipeline: (1) compile the smart contract with
the oﬃcial solc compiler to obtain its YUL-IR CFG-SSA representation as a
JSON ﬁle; (2) translate this JSON ﬁle into a Rocq ﬁle deﬁning a term of type
SmartContract(EVMDialect) (see Sect. 3.1); (3) compile the Rocq ﬁle together
with the liveness chk function and use Rocq’s facilities to produce a static
binary executable via OCaml (we make sure that the OCaml compiler does not
apply any inlining or partial evaluation of the contract); and (4) execute this
binary to obtain the output of the liveness checker. Following this pipeline, we
used as benchmarks the 1,550 smart contracts contained in the semantic test
suite of solc,4 and we successfully validated the liveness analysis results on all
of them. The size of these contracts ranges from 2 to 562 blocks (with an average
of 44.06 blocks). The total time required to run the compiled liveness checker—
step 4 of the pipeline—was 3.576 seconds: 78% of all contracts complete in 2 ms,
20% complete in 3 ms, and the remaining 2% take between 4 and 11 ms. All
experiments were conducted on a machine equipped with an Intel i7-4790 CPU
at 3.60 GHz and 16 GB of RAM.
    In the current setting, we compile the checker into a binary for each contract.
We adopted this approach because it easily allows us to measure the time (at
OCaml level, not Rocq) required to check each contract once its Rocq represen-
tation is generated—which is the key factor in evaluating the checker’s eﬃciency.
We plan to streamline the liveness-checking pipeline by generating a specialized
4
    The test suite is available at [7]. We omitted three contracts that rely on experimental
    features not yet supported by oﬃcial releases of solc.
                    Towards Formally Veriﬁed Smart Contracts Compilation        271

OCaml implementation of the checker (using Rocq’s extraction facilities) that
takes as input the Rocq representation of the smart contract and produces the
liveness-checking verdict. This specialized checker (combining steps 3 and 4 of
the current pipeline) will be compiled once, and the resulting static executable
will then be invoked directly, eliminating the dependency on the Rocq Prover
for end-users and improving the overall eﬃciency and usability of the tool.


6   Conclusions, Related and Future Work
There are other ongoing eﬀorts to facilitate formal veriﬁcation of YUL programs,
which also require formalization of the YUL semantics [2,23]. On one hand, in [23],
both a big- and a small-step YUL operational semantics are deﬁned together with
an interpreter in OCaml. Another important eﬀort is the Clear project [2] by
Nethermind Security, developed in Lean, that deﬁnes a YUL and an EVM seman-
tics that share the primitive operators. Using their YUL semantics, this work
proposes to generate veriﬁcation conditions that can be automatically veriﬁed
from knowledge in preconditions and other annotations. In both cases [2,23], the
semantics is deﬁned at the level of YUL abstract syntax tree, rather than at the
level of the CFG-SSA as our semantics. As our goal is to verify smart contracts
compilation, deﬁning the semantics at the level of the CFG is more adequate as
it facilitates reasoning about the compilation stages that are typically developed
on this CFG-SSA form. As regards the proof assistants, having a formalization in
diﬀerent proof assistants such as Rocq and Lean is not a weakness but a strength,
since it extends the community of formal methods in YUL to more research groups
with experience in the diﬀerent proof assistants. Moreover, the diﬀerent proof
assistants provide diﬀerent capabilities, e.g. in Rocq it is easy to export the Rocq
functional code to the functional programming language OCaml, thus obtain-
ing more eﬃcient binary programs without dependencies on Rocq, which can be
easily integrated into third-party tools.
    In summary, we have presented the ﬁrst steps towards developing a frame-
work for fully veriﬁed smart contract compilation in the context of the Ethereum
blockchain. Other compilers have already worked towards achieving this goal.
An inspiring case is the CompCert project [26], that has investigated the formal
veriﬁcation of realistic compilers usable for critical embedded software. Such
veriﬁed compilers come with a mathematical, machine-checked proof that the
generated executable code behaves exactly as prescribed by the semantics of
the source program. By ruling out the possibility of compiler-introduced bugs,
veriﬁed compilers strengthen the guarantees that can be obtained by applying
formal methods to source programs. The main result of the Compcert project is
the CompCert C veriﬁed compiler, a high-assurance compiler for almost all of
the C language (ISO C 2011), generating eﬃcient code for the ARM, PowerPC,
RISC-V and x86 processors. This includes the veriﬁcation of several types of
liveness analysis [13,24].
272     E. Albert et al.

    Our future work spawns along several directions. The most immediate plan
is to integrate the liveness checker within the solc compiler, as described at the
end of Sect. 5. We also aim at implementing veriﬁed checkers for other stages
of the solc compilation process with the goal of having the whole compilation
fully veriﬁed. Finally, let us note that, while our implementation focus has been
solc, the FORYU components are general and could be used to verify other smart
contracts compilers, as overviewed in Sect. 2.


References
 1. FE: The next generation smart contract language for Ethereum. https://fe-lang.
    org
 2. A formal veriﬁcation tool for Solidity smart contracts by Nethermind Security.
    https://github.com/NethermindEth/Clear. Accessed 27 Nov 2025
 3. The solc optimizer (2021). https://docs.soliditylang.org/en/v0.8.7/internals/
    optimizer.html
 4. FORVES: Formally Veriﬁed EVM Block-Optimizations (2024). https://github.
    com/costa-group/forves. Accessed 27 Nov 2025
 5. coq-of-solidity (2025). https://github.com/formal-land/coq-of-solidity. Accessed
    27 Nov 2025
 6. FORYU: A Formal Semantics for Yul in Coq (2025). https://github.com/costa-
    group/foryu. Accessed 27 Nov 2025
 7. Semantic tests of solidity (2025). https://github.com/argotorg/solidity/tree/
    develop/test/libsolidity/semanticTests. Accessed 27 Nov 2025
 8. Solidity documentation (2025). https://docs.soliditylang.org/en/latest/index.html
 9. Yul (2025). https://docs.soliditylang.org/en/latest/yul.html. Accessed 27 Nov
    2025
10. Albert, E., Genaim, S., Martin-Martin, E.: Towards Formally Veriﬁed Smart
    Contracts Compilation (FM’26 Artifact) (2026). https://doi.org/10.5281/zenodo.
    18612372. Accessed 13 Feb 2026
11. Amani, S., Bégel, M., Bortin, M., Staples, M.: Towards verifying Ethereum smart
    contract bytecode in Isabelle/HOL. In: CPP, pp. 66–77. ACM (2018)
12. Barrière, A., Blazy, S., Flückiger, O., Pichardie, D., Vitek, J.: Formally veriﬁed
    speculation and deoptimization in a JIT compiler. Proc. ACM Program. Lang.
    5(POPL), 1–26 (2021)
13. Barthe, G., Demange, D., Pichardie, D.: A formally veriﬁed SSA-Based Middle-
    End. In: Seidl, H. (ed.) ESOP 2012. LNCS, vol. 7211, pp. 47–66. Springer, Heidel-
    berg (2012). https://doi.org/10.1007/978-3-642-28869-2 3
14. Bertot, Y., Castéran, P.: Interactive theorem proving and program development -
    Coq’Art: the calculus of inductive constructions. Texts in Theoretical Computer
    Science. An EATCS Series. Springer (2004)
15. Cassez, F., Fuller, J., Asgaonkar, A.: Formal veriﬁcation of the ethereum 2.0 bea-
    con chain. In: Fisman, D., Rosu, G., (eds.) Tools and Algorithms for the Construc-
    tion and Analysis of Systems - 28th International Conference, TACAS 2022, Held
    as Part of the European Joint Conferences on Theory and Practice of Software,
    ETAPS 2022, Munich, Germany, April 2–7, 2022, Proceedings, Part I, vol. 13243
    of Lecture Notes in Computer Science, pp. 167–182. Springer (2022)
                     Towards Formally Veriﬁed Smart Contracts Compilation            273

16. Demange, D., Pichardie, D., Stefanesco, L.: Verifying fast and sparse SSA-based
    optimizations in Coq. In: Franke, B., (ed.), Compiler Construction - 24th Interna-
    tional Conference, CC 2015, Held as Part of the European Joint Conferences on
    Theory and Practice of Software, ETAPS 2015, London, UK, April 11-18, 2015.
    Proceedings, vol. 9031 of Lecture Notes in Computer Science, pp. 233–252. Springer
    (2015)
17. Dill, D.L., et al.: Fast and reliable formal veriﬁcation of smart contracts with
    the move prover. In: Fisman, D., Rosu, G., (eds.) Tools and Algorithms for the
    Construction and Analysis of Systems - 28th International Conference, TACAS
    2022, Held as Part of the European Joint Conferences on Theory and Practice of
    Software, ETAPS 2022, Munich, Germany, April 2-7, 2022, Proceedings, Part I,
    vol. 13243 of Lecture Notes in Computer Science, pp. 183–200. Springer (2022)
18. Ethereum. Vyper (2024). https://vyper.readthedocs.io. Accessed 27 Nov 2025
19. Grossman, S., et al.: Practical veriﬁcation of smart contracts using memory split-
    ting. Proc. ACM Program. Lang. 8(OOPSLA2), 2402–2433 (2024)
20. Hirai, Y.: Deﬁning the Ethereum virtual machine for interactive theorem provers.
    In: Brenner, M., et al., (eds.) Financial Cryptography and Data Security, pp. 520–
    535. Springer International Publishing, Cham (2017)
21. INRIA. The Rocq Reference Manual - Version 9.1.0 (2025). https://rocq-prover.
    org/doc/V9.1.0/refman/index.html
22. ivan71kmayshan27. Coq formalisation of the ethereum virtual machine (wip)
    (2020). https://github.com/ivan71kmayshan27/coq-evm. Accessed 23 June 2022
23. Koutavas, V., Lin, Y., Tzevelekos, N.: An operational semantics for YUL. In:
    Madeira, A., Knapp, A., (eds.) Software Engineering and Formal Methods - 22nd
    International Conference, SEFM 2024, Aveiro, Portugal, November 6-8, 2024, Pro-
    ceedings, vol. 15280 of Lecture Notes in Computer Science, pp. 328–346. Springer
    (2024)
24. Léchenet, J.-C., Blazy, S., Pichardie, D.: A fast veriﬁed liveness analysis in SSA
    form. In: Peltier, N., Sofronie-Stokkermans, V. (eds.) IJCAR 2020. LNCS (LNAI),
    vol. 12167, pp. 324–340. Springer, Cham (2020). https://doi.org/10.1007/978-3-
    030-51054-1 19
25. Leroy, X.: Formal veriﬁcation of a realistic compiler. Commun. ACM 52(7), 107–
    115 (2009)
26. Leroy, X.: Formal veriﬁcation of a realistic compiler. Commun. ACM 52(7), 107–
    115 (2009)
27. Monniaux, D.: Pragmatics of formally veriﬁed yet eﬃcient static analysis, in par-
    ticular, for formally veriﬁed compilers. Int. J. Softw. Tools Technol. Transf. 26(4),
    463–477 (2024)
28. Monniaux, D., Six, C.: Simple, light, yet formally veriﬁed, global common subex-
    pression elimination and loop-invariant code motion. In: Henkel, J., Liu, X., (eds.)
    LCTES ’21: 22nd ACM SIGPLAN/SIGBED International Conference on Lan-
    guages, Compilers, and Tools for Embedded Systems, Virtual Event, Canada, 22
    June, 2021, pp. 85–96. ACM (2021)
29. Moura, L., Ullrich, S.: The lean 4 theorem prover and programming language.
    In: Platzer, A., Sutcliﬀe, G. (eds.) CADE 2021. LNCS (LNAI), vol. 12699, pp.
    625–635. Springer, Cham (2021). https://doi.org/10.1007/978-3-030-79876-5 37
30. Nipkow, T., Wenzel, M., Paulson, L.C. (eds.): Isabelle/HOL. LNCS, vol. 2283.
    Springer, Heidelberg (2002). https://doi.org/10.1007/3-540-45949-9
31. Schneidewind, C., Grishchenko, I., Scherer, M., Maﬀei, M.: Ethor: practical and
    provably sound static analysis of Ethereum smart contracts. In: CCS ’20: 2020
274     E. Albert et al.

    ACM SIGSAC Conference on Computer and Communications Security, Virtual
    Event, USA, 9–13 November 2020, pp. 621–640. ACM (2020)
32. Six, C., Boulmé, S., Monniaux, D.: Certiﬁed and eﬃcient instruction schedul-
    ing: application to interlocked VLIW processors. Proc. ACM Program. Lang.
    4(OOPSLA), 129:1–129:29 (2020)
33. Six, C., et al.: Formally veriﬁed superblock scheduling. In: Popescu, A., Zdancewic,
    S., (eds.) CPP ’22: 11th ACM SIGPLAN International Conference on Certiﬁed
    Programs and Proofs, Philadelphia, PA, USA, January 17 – 18, 2022, pp. 40–54.
    ACM (2022)
34. Stegeman, L., Solitor: runtime veriﬁcation of smart contracts on the Ethereum
    network. Master’s thesis, University of Twente (2018)
35. Tristan, J., Leroy, X.: Formal veriﬁcation of translation validators: a case study
    on instruction scheduling optimizations. In: Necula, G.C. Wadler, P., (eds.) Pro-
    ceedings of the 35th ACM SIGPLAN-SIGACT Symposium on Principles of Pro-
    gramming Languages, POPL 2008, San Francisco, California, USA, January 7–12,
    2008, pp. 17–27. ACM (2008)
36. Wood, G.: Ethereum: a secure decentralised generalised transaction ledger (Berlin
    version 8fea825 – 2022-08-22) (2022)




Open Access This chapter is licensed under the terms of the Creative Commons
Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/),
which permits use, sharing, adaptation, distribution and reproduction in any medium
or format, as long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons license and indicate if changes were
made.
   The images or other third party material in this chapter are included in the
chapter’s Creative Commons license, unless indicated otherwise in a credit line to the
material. If material is not included in the chapter’s Creative Commons license and
your intended use is not permitted by statutory regulation or exceeds the permitted
use, you will need to obtain permission directly from the copyright holder.
