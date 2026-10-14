                 A Formal Semantics for P-Code

 Nico Naus1(B) , Freek Verbeek1,2 , Dale Walker1 , and Binoy Ravindran1
                           1
                           Virginia Tech, Blacksburg, USA
                   {niconaus,freek,dalewalker,binoy}@vt.edu
           2
             Open University of The Netherlands, Heerlen, The Netherlands



        Abstract. Decompilation is currently a widely used tool in reverse
        engineering and exploit detection in binaries. Ghidra, developed by the
        National Security Agency, is one of the most popular decompilers. It
        decompiles binaries to high P-Code, from which the ﬁnal decompila-
        tion output in C code is generated. Ghidra allows users to work with
        P-Code, so users can analyze the intermediate representation directly.
        Several projects make use of this to build tools that perform veriﬁca-
        tion, decompilation, taint analysis and emulation, to name a few. P-
        Code lacks a formal semantics, and its documentation is limited. It has
        a notoriously subtle semantics, which makes it hard to do any sort of
        analysis on P-Code. We show that P-Code, as-is, cannot be given an
        executable semantics. In this paper, we augment P-Code and deﬁne a
        complete, executable, formal semantics for it. This is done by looking at
        the documentation and the decompilation results of binaries with known
        source code. The development of a formal P-Code semantics uncovered
        several issues in Ghidra, P-Code, and the documentation. We show that
        these issues aﬀect projects that rely on Ghidra and P-Code. We evaluate
        the executability of our semantics by building a P-Code interpreter that
        directly uses our semantics. Our work uncovered several issues in Ghidra
        and allows Ghidra users to better leverage P-Code.


        Keywords: Decompilation · P-Code · Formal semantics


1     Introduction
After more than 60 years of research, the ﬁeld of decompilation is currently
very mature. A plethora of open source and commercial decompilation tools
exist [1,7,11–13]. They are widely used to recover source code from binaries and
to detect software vulnerabilities.
    Ghidra1 is one of those tools, developed by the National Security Agency
(NSA), and made public and open source a few years ago. Recent comparative
studies show that it ranks among the top performing decompilers [5]. At the
heart of Ghidra lies P-Code, an intermediate representation that exists at two
levels of abstraction. The ﬁrst is a direct one-to-many translation of the disas-
sembled assembly instructions, called low P-Code. The second is high P-Code,
1
    https://ghidra-sre.org/.
c The Author(s) 2023
A. Lal and S. Tonetta (Eds.): VSTTE 2022, LNCS 13800, pp. 111–128, 2023.
https://doi.org/10.1007/978-3-031-25803-9_7
112    N. Naus et al.

which is the result of various transformations on the low P-Code from Ghidra’s
decompiler. Since we focus our work on high P-Code, we will simply refer to it
as P-Code from now on.
    From the P-Code, Ghidra constructs C code, which is the ﬁnal decompilation
result. Users can deﬁne their own analyses over high P-Code, customizing the
decompilation process or extracting information from it. We have come across
several projects that perform a wide range of analyses on P-Code. Veriﬁcation [6],
decompilation [14] and taint analysis [2], to name a few. However, the P-Code
documentation is very limited and P-Code lacks any form of formal semantics.
On top of that, P-Code has a notoriously subtle semantics, as will become clear
in the rest of this paper. This limits the usability of P-Code for formal analysis,
since there is no way to know if the analysis that is being performed is correct
with respect to the language semantics.
    In this paper, we develop a formal semantics for high P-Code. We base our
work on Ghidra 10.1.4 released May 2022, which comes with P-Code documen-
tation last updated September 5th, 2019 [9]. Ghidra does come with a P-Code
interpreter, but only for low P-Code. This means that there is no ground-truth
that we can base our high P-Code semantics on. We therefore start our inves-
tigation by looking at the P-Code documentation. Since this is rather limited,
we additionally run experiments for P-Code instructions that are unclear. These
experiments consist of compiling several C programs to binary, decompiling them
using Ghidra, and comparing the high P-Code and decompiled C code to the
original source code. During the development of a formal P-Code semantics, we
uncover several issues in Ghidra, P-Code and the P-Code documentation. These
issues all stem from inconsistencies in documentation, Ghidra’s output via UI or
API, and in some cases the inability to formulate executable P-Code semantics.
As-is, P-Code cannot be given an executable semantics. To overcome the short-
comings of P-Code, we extend the language with additional information. For
the extended P-Code semantics, we deﬁne a formal operational semantics. We
argue that projects relying on P-Code are directly aﬀected by these issues, and
could beneﬁt from a formal P-Code semantics. Since there is no interpreter for
high P-Code available, we are only able to validate our semantics by writing an
interpreter for high P-Code to show that our semantics are executable. We have
shared our results with the NSA prior to publication, and they acknowledge all
issues identiﬁed in this paper.
    More speciﬁcally, we make the following contributions:
– An extended P-Code language.
– A formal syntax and semantics for extended P-Code.
– A P-Code interpreter written in Haskell.
– An overview of several bugs, issues and inconsistencies in Ghidra, P-Code
  and documentation.
    The P-Code interpreter written in Haskell and the accompanying Ghidra
script written in Java are publicly available2 .
2
  https://github.com/niconaus/pcode-interpreter
https://github.com/niconaus/PCode-Dump.
                                             A Formal Semantics for P-Code     113

   Section 2 ﬁrst gives an introduction to Ghidra, its assembly translator
SLEIGH and low & high P-Code. Section 3 describes and motivates our design
choices. Section 4 describes the P-Code syntax and Sect. 5 gives its semantics.
We list an overview of the bugs, issues and inconsistencies we have found, and a
response from the NSA on these, in Sect. 6. Section 7 presents related work and
Sect. 8 concludes.


2   Ghidra, SLEIGH and P-Code
Ghidra is an open-source reverse engineering tool, developed by the National
Security Agency. It is capable of decompiling binaries of a wide variety of archi-
tectures. To do so, it ﬁrst disassembles the binary using its custom disassembler
SLEIGH, and performs several analysis steps. The end result is high-level C code,
as well as detailed control ﬂow information. A recent study compared other well
known decompilers like IDA-pro [7] and Angr [13] to Ghidra, by evaluating 1760
binaries, using the correctly identiﬁed function starts (CFS) metric [5]. They
found that Ghidra performs above average.




        Fig. 1. First few instructions in the decompilation of nearest prime


    To illustrate the Ghidra decompilation pipeline, we take a look at the ﬁrst
few instructions of an x86-64 binary. Figure 1 lists the decompilation result for
the ﬁrst few addresses of our example binary. For readability’s sake, we have har-
monized notation, and simpliﬁed in- and output notation. Address 0x100000e70
is the entry point of a function. Ghidra’s machine code translator SLEIGH takes
the x86-64 assembly instructions as listed in the second column in Intel syn-
tax, and translates them to low P-Code, listed in the third column. The exact
meaning of the P-Code instructions will be left for the coming sections, and is
not essential to understand at this point. As for notation, the $U preﬁx indi-
cates local variables. Registers are identiﬁed by their name, and are assumed
to have a ﬁxed size. Addresses are given in a hexadecimal format, preﬁxed by
114     N. Naus et al.

0x. Constants are given either as a decimal or hexadecimal preﬁxed by 0x. Both
addresses and constants have a size indicated by the number after the colon.
    P-Code is considered low before decompilation, and is merely a one-to-many
translation from assembly instructions to P-Code. The instruction set of P-Code
is much smaller than x86, and SLEIGH basically breaks up a complicated assem-
bly instruction into simple P-Code ones. For example, the x86 compare instruc-
tion at address 0x100000e77 breaks down into 13 separate P-Code instructions.
To break down the instructions, P-Code uses local variables. The x86 push rbp
instruction at address 0x100000e70 for example, is broken down into three sim-
ple assignments, using the variable $Uea00:8 to hold the original value of RBP
temporarily, until it has been stored in memory.
    After disassembly and translation, Ghidra performs several decompilation
analyses. This results in high P-Code, listed in the third column, which uses an
instruction set almost identical to low P-Code. The analyses Ghidra performs,
remove all instructions that have no eﬀect on execution, resolves the stack and
constructs a control ﬂow graph, among other things. A more detailed description
of Ghidra’s decompilation analyses can be found in other literature [4]. From the
high P-Code, Ghidra constructs the ﬁnal decompilation result in C code.
    By example, we have shown how the basic Ghidra pipeline operates. Users can
inspect the ﬁnal decompilation result, but there also exists a plethora of scripts
that can be run to further analyse the ﬁnal or intermediate P-Code result. It
is also possible to deﬁne custom scripts, through Ghidra’s extensive API [10].
Since these analyses can target high P-Code directly, it is important to have a
correct semantics for it.


3     Design Choices

As mentioned in Sect. 1, P-Code documentation is limited. On top of that, P-
Code as-is cannot be given a formal semantics, because crucial information is
not included. To arrive at an executable P-Code semantics, we had to make the
following design choices.

Conditional Branches. We observed that the P-Code generated for condi-
  tional branches is often incorrect. Three diﬀerent situations occur. One, the
  conditional branch is correct. Two, the conditional branch incorrectly jumps
  to the fall-through address in the True case. Three, the conditional branch
  should jump to a diﬀerent address than the fall-through in the False case.
  The control ﬂow API always returned the correct out addresses in our exper-
  iments. We use this fact later on when we build our interpreter.
Phi-nodes. P-Code has a MULTIEQUAL instruction, which is better known as
  a phi-node in literature [3]. A phi-node’s value depends on the address of the
  previous block that was executed. In other SSA languages using phi-nodes,
  like LLVM IR [8], every alternative value is guarded by an address, which is
  compared to the address of the previous block. You compare the address to
  the alternatives in the phi-node, to know which value will be selected. This is
                                            A Formal Semantics for P-Code      115

  not the case in P-Code. Here, only the alternative values are listed. Looking at
  the documentation, no additional information is provided about the ordering
  of the alternatives.
  To determine which alternative belongs to which control ﬂow, we have ran
  several experiments. From these experiments, we know that the order of the
  alternatives coincides with the inbound edge ordering when requesting these
  though Ghidra’s control ﬂow API.
Varnodes. Inputs and outputs are encoded by the so called varnodes. They
  represent the arguments and destination of the instructions. The P-Code
  manual states that varnodes are either a register or a memory location, and
  that they consist of three components: address space, oﬀset and size.
  We use a slightly diﬀerent view of varnodes, and regard the “address space”
  as a varnode type. We have come across six diﬀerent types, and they consist
  of two components: a value and a size. Of those six, we can bring it down to
  four essential types of varnodes.
   (R r, l) register, identiﬁed by a register address r and size l.
   (A a, l) memory, with a the starting address and l the size of the memory
       region.
   (C c, l) constant value, with c the value and l the size.
   (v, l) local variable, with v the identiﬁer and l its size.
  In the case where P-Code models a Harvard architecture binary instead of
  the more common von Neumann architecture, the memory varnode is split
  up into a data varnode and a code varnode, to model the dedicated addresses
  in this architecture.

   (AC a, l) memory containing code, with a the starting address and l the size
       of the memory region.
   (AD a, l) memory containing data, with a the starting address and l the size
       of the memory region.
  The register notation diﬀers from the previous P-Code example, as listed
  in Fig. 1. Instead of listing register names, an address in the register space is
  used, together with a size. Using register addresses and sizes has the advantage
  that we do not explicitly have to take care of register aliasing.
Call & Return. For the CALL instruction, P-Code documentation lists:
  “This instruction is semantically equivalent to the BRANCH instruction. (...)
  The P-Code instruction does not implement the full semantics of the call
  itself; it only implements the ﬁnal branch.”
  Looking at P-Code programs, it is immediately clear that this cannot be
  true. A function can have arguments and return a value, and this behavior is
  certainly not captured by a basic BRANCH instruction. What is more, not
  all varnode address spaces will be in scope when dispatching a function call.
  Local variables are cleared when a new function context is entered. Arguments
  are passed through the registers, and these registers are cleaned up when P-
  Code returns from a call. How this is done exactly depends on the calling
  convention that the original binary relies on, more on this later.
116    N. Naus et al.

  For the indirect call and return, documentation lists a similar description.
  They are both said to be equivalent to BRANCHIND. For indirect call, this
  is false, for the reasons described above. For return, we see that this cannot
  hold for two reasons. One, in high P-Code, a return instruction can hold a
  return value that is to be the result of calling the function. Furthermore, no
  address to return to is included in the instruction; we do not have a branch
  destination.
Fall-through. The P-Code outputted by Ghidra performs fall-through in a non-
  uniform way. Looking at the P-Code output for several decompiled binaries,
  there is no pattern to be found in the way fall-through is performed. The
  most natural way to perform fall-through is to let control ﬂow jump to the
  next block listed in the output, but this is not always true. It can occur that
  control ﬂow jumps to a later or earlier block instead. The addresses of those
  blocks are not logical either. In some cases, the address of the fall-through
  block is higher than the current block, in some cases it is lower. We therefore
  do away with fall-through all-together, instead requiring that every block ends
  in a branching instruction.
User defined instructions. P-Code allows the use of the so called “USERDE-
  FINED” instruction. The goal of this instruction is to capture very compli-
  cated behavior that cannot be described in terms of existing P-Code instruc-
  tions. Since the semantics are user-provided, we consider this instruction to
  be out of scope for this paper.
Indirect instruction. One ﬁnal tricky aspect of P-Code is the use of the indirect
  instruction. We will denote an indirect instruction as out = in0 ← in1 . The
  intuition of this instruction is that the value of in0 should be assigned to
  out, but may be inﬂuenced indirectly by an instruction elsewhere, which is
  described by in1 . If there was an indirect inﬂuence, this means that potentially
  any value may be assigned to out. This can happen for example when calling
  external functions, so there is no way of knowing what the value will be.


4     P-Code Syntax
This section lists the syntax of P-Code programs. We base the syntax on the
notation used in the P-Code documentation. P-Code features some instructions
that do not have a deﬁned syntax. For those instructions, we have taken the
liberty of choosing an appropriate representation ourselves. On top of that, there
are several minor changes that we needed to make, in accordance with the design
choices from Sect. 3.
    Figures 2 and 3 lists our P-Code syntax and P-Code operators. We model a
program as a mapping from addresses a to code blocks b.
    Inputs and outputs are modeled by four diﬀerent varnodes. Registers, mem-
ory, constants and variables. For registers, addresses are used instead of names.
To give an example, (0x18,8), (0x18,4) and (0x19,1) refer to RBX, EBX and BH
respectively.
                                              A Formal Semantics for P-Code         117




                      Fig. 2. P-Code language syntax deﬁnition


    A P-Code block must be non-empty, can have zero or more instructions i, and
must end in a terminator instruction t. This does not adhere to documentation
or Ghidra produced P-Code, but is required to correct the fall-through issues
that occur, as mentioned in Sect. 3. We distinguish between regular instructions
and terminator instructions, to make it easier to construct a semantics later on.
    Instructions i are either basic operations on data, that are assigned to an
output, or a function call that may or may not return some value. The instruction
out = (o | s) represents basic operations o that are assigned to the output out, or
a function call s with a return value. In some cases, the data operation depends
on the size of the output, like sign-extend. These instructions are added at this
level for that reason.
    A function call is denoted by call [in0 ] in1 . . . inn , where in0 is either a con-
stant, for direct calls, or a register, memory location or variable, which indicates
that this is an indirect function call. This notation is identical to the P-Code doc-
umentation, but diﬀers from the P-Code that Ghidra produces. Instead, Ghidra
explicitly diﬀerentiates between direct and indirect function calls using diﬀerent
instructions, and uses a memory-varnode in the case of a direct function call,
instead of a constant value.
118    N. Naus et al.




                Fig. 3. P-Code language operator syntax deﬁnition


    Basic operations o are all data operations that are independent of the output.
Most of them are straight forward binary or unary operations. We will discuss
two non-standard operations.
    The P-Code documentation does not list a syntax for the phi-node, so we
have chosen one ourselves. We enhance the phi-node to include the address that
guards the value alternative.
    Indirect (in0 ← in1 ) is the second non-standard operation. This instruction
indicates that either the value of in0 will be returned, or the value is unknown,
because an instruction pointed to by in1 has altered it. A typical use case of this
is when an external function is called with a pointer.
    Finally, we have terminator instructions. These instructions are not singled
out by the P-Code documentation, but as mentioned, by separating them, con-
structing a semantics becomes easier.
    The conditional branch is an interesting case. We have seen that Ghidra does
not produces consistent P-Code for this instruction. To work around this issue,
we replaced the conditional branch instruction with our own, so we can later use
the Ghidra API to get a hold of the correct addresses, and explicitly state both
the true and false branch. This works since conditional branches are terminators
and can thus only appear at the end of a block.
    Lastly, the return instruction. This instruction includes an oﬀset, and may
hold a value to be returned. Looking at large pieces of P-Code, we found that the
oﬀset is not actually used in performing the return. For completeness sake we
include this parameter in the syntax, but we will not give it any semantics. The
same is true for the cast and new unary operators, these are merely placeholders
to indicate that a value has been cast or new memory has been allocated. This
information can then be used by subsequent analyses.
    For space reasons, we omit a description of all basic operations, as well as
unary and binary operators.
                                             A Formal Semantics for P-Code       119

5   P-Code Semantics
This section presents a big-step semantics for P-Code. As described in the previ-
ous sections, deﬁning a semantics for P-Code is not trivial. Based on our exper-
iments and observations so far, we assume that the following holds for programs
written in P-Code.
Local variables do not overlap. We assume that local variables do not overlap
  in the local variable address space. In other words, local variables occupy
  separate memory locations. This property of P-Code has been veriﬁed by
  decompiling large binaries and checking that no variables overlap.
No global variables. We assume that all declared variables are local. Strictly
  speaking, the P-Code documentation does not prohibit an address space
  that serves as global variables, but after running several experiments, this
  behaviour has not been observed. Programs can and do have global variables,
  but they are conﬁned to memory and registers.
Call and Branch on constant. We assume that direct calls and direct branches
  are encoded by having a constant varnode as an argument. In all other cases,
  the call and branch will be interpreted as indirect.
Terminators only at block’s end. We assume that terminator instructions
  like branch and return only occur at the end of a block. This assumption
  already shows up in the syntax listed in the previous section, but for com-
  pleteness sake, we reiterate this fact here.




                             Fig. 4. Semantic objects


    Figure 4 lists the semantic objects needed for evaluation; state, memory, reg-
isters and variable mapping. The memory mapping M takes an address a and
size l and returns a constant varnode (Cc, l). The register mapping R takes a
register address r and a size l and returns a constant varnode (Cc, l). Just a regis-
ter identiﬁer is not suﬃcient, since registers can alias. Three special registers are
used to keep track of function return value, the address of the previous block and
the address of the current block. These registers are denoted by “Ret”, “Prev”
and “Cur”, assuming that a varnode representation that is separate from regis-
ters used by the program exists. Variable mapping V takes a variable identiﬁer
v and returns a constant varnode (Cc, l). Figures 7 through 11 list the rules for
the diﬀerent semantic judgements we use. These rules use two auxiliary judge-
ments, namely the evaluation of varnodes and state update, listed in Fig. 5 and
6 respectively.
120     N. Naus et al.




                         Fig. 5. Evaluation of varnodes to values




                             Fig. 6. State update semantics


      Varnodes are evaluated by judgements of the form σ, in ↓ val, taking a state
σ and varnode in, and returning the resulting value val, as listed in Fig. 5. The
resulting value is again a varnode, of the form (Cc, l), where c is a constant and
l the size. Depending on the type of the varnode, this value is retrieved from
memory, register mapping or variable mapping.
      Updates to memory are handled by judgements of the form σ, out, in ↑ σ  ,
taking a state σ, destination out and source in, returning the updated state σ  ,
as listed in Fig. 6. The type of the destination is used to select the correct rule,
and ultimately which part of the state to update. In general, P-Code always
requires that destination and source size is equal. This is ensured by the update
semantics.
      At the top-level, we evaluate a block using the judgement p, σ, b −→b σ  ,
which takes a program p, state σ and entry block b and returns a new state
σ  , which is the result of completely executing the program. Figure 7 lists the
semantic rules for block evaluation.

B-Seq ﬁrst evaluates the instruction i, and uses the resulting state to evaluate
  the remainder of the block, b.
B-Term evaluates a block ending in a terminator, using the terminator seman-
  tics.

    The terminator semantics is given in Fig. 8. It uses judgements of the form
p, σ, t −→t σ  , taking a program p, state σ and terminator t as input and pro-
ducing a resulting state σ  .
    The terminator semantics is pretty straight forward. T-Branch evaluates its
varnode in and looks up the next block in p, and then use the block semantics
to evaluate it. These rules make use of the varnode evaluation semantics ↓ listed
in Fig. 5. In the case of a conditional branch, in0 is evaluated. If the condition
returns decimal 1, of any size, we go to the true-branch. All other return values
are regarded as false. Branching instructions also perform some bookkeeping on
what the current and previous block addresses are.
                                            A Formal Semantics for P-Code     121




                        Fig. 7. Block evaluation semantics




                     Fig. 8. Terminator evaluation semantics


    T-Return handles a return statement. To pass the return value to the caller,
we use the Ret register. Updating the state as such is taken care of by the memory
update function ↑.
    Figure 9 lists the partial instruction semantics. Judgements have the form
p, σ, i −→i σ  , taking a program p, state σ and instruction i, and returning the
resulting state σ  . For space reasons, we only list I-Assign, I-AssCall, I-Store
and I-Load here.

I-Assign uses the operation semantics to evaluate o, which returns the value
   that should be assigned to out. The output out is updated by ↑, depending
   on the type of varnode that out is; memory, register or variable.
I-AssCall relies on the call semantics to perform the call, and the resulting
   value is again used to update out, and the ﬁnal state is returned.
I-Store evaluates the destination, converts it to a varnode of type address,
   and updates accordingly.
I-Load evaluates the input and then treats it as a memory address, and looks
   up the ﬁnal value in memory. The number of bytes to be retrieved from
   memory is dictated by the output varnode.

   The calling semantics is one of the more perculiar aspects of P-Code. All
arguments that are passed though registers in the original binary, are now passed
122     N. Naus et al.




                  Fig. 9. Partial instruction evaluation semantics




                Fig. 10. Example of a function call evaluation rule


as function arguments in the call instruction. However, the called function does
still retrieve them from registers. How this is done precicely depends on the
original calling convention. Figure 10 lists an example of a call rule for a binary
that uses the AMD64-ABI calling convention.
     Judgements are of the form p, σ, s −→s σ  , val, taking a program p, state σ,
call statement s and returning the resulting state σ  and value val. In this case, a
call can have at most six arguments, adhering to the speciﬁc calling convention.
     The semantics completely deviates from the P-Code documentation.
Section 3 discusses this issue, here we stick to a description of the semantics.
     The Call-rule ﬁrst resolves the address of the function to be called. As men-
tioned in Sect. 4, if in is a constant, we have a direct call. In all other cases, we
have an indirect call, and the varnode evaluation semantics takes care of resolv-
ing the address. We evaluate all arguments to the call, which are then assigned
to the appropriate registers. To execute the called function, the block seman-
tics is used. We look up the block, and evaluate it under the current memory,
the registers containing the arguments, and an empty local variable mapping ∅.
Returning from the call, the local variable mapping is disregarded, registers are
cleaned up, and the return value is retrieved from the registers. This value, along
with the new state are then returned.
     Figure 11 lists a few of the operation evaluation rules. Judgements are of the
form σ, o −→o val, taking a state σ and operation o, returning the resulting value
                                             A Formal Semantics for P-Code   123




                   Fig. 11. Partial operation evaluation semantics


val. For space reasons, we omit all basic operations, as well as unary and binary
operations. These operations are all straight-forward and standard.
O-Copy evaluates the varnode and return its value.
O-phi evaluates the phi-node by ﬁnding the address ai that is equal to the
  address of the last block. The selected input is evaluated and its value
  returned.
O-Indirect-val and -ND rules handle the indirect instruction. Here, we
  basically have two options. Either the value is unaﬀected, and we can return
  it, or the instruction pointed to by the second argument has altered the ﬁrst
  in some way, in which case any value of any size can be returned.
   The above syntax and semantics assume that the P-Code models the von
Neumann architecture. Extending them to deal with Harvard architecture that
has dedicated code and data memory sections is straight-forward, but omitted
from the description here for space reasons.

5.1    P-Code Interpreter
To validate that the semantics above are executable, we have built a P-Code
interpreter in Haskell. The source code is publicly available, and consists of a
parser, type deﬁnitions and the interpreter itself3 . Ghidra does not come with
a script to dump P-Code, so we have created a script with that functionality4 .
The interpreter is intended to be used in combination with this Ghidra script,
since it corrects the P-Code output of Ghidra with respect to the conditional
branch, fall-through and phi-nodes.
    We encountered several interesting issues in order to get to a working inter-
preter. First of all, we had to bridge the gap between what we think the syntax
and semantics of P-Code should be, ideally, and what Ghidra actually produces
for us. We assumed that both call and indirect call use the same instruction,
and we merged the branch and indirect branch instruction. In the P-Code pro-
duced by Ghidra, these are all separate instructions. The direct call and direct
branch use a memory varnode where we prefer to use a constant. For the MULTI-
EQUAL (phi-node), conditional branch instruction and the fall-through mech-
anism, Ghidra’s output does not contain enough information to come to an
executable semantics, as described above. We augment the P-Code dumping
3
    https://github.com/niconaus/pcode-interpreter.
4
    https://github.com/niconaus/PCode-Dump.
124    N. Naus et al.

script to include the additional information required. Second, we assumed sev-
eral properties to hold for P-Code programs, as outlined in the beginning of this
section.
    Finally, it is important to note that although the semantics is executable,
it is not practical to do so. Any realistic program will produce many INDI-
RECT instructions, which introduces non-determinism into the program. Execu-
tion of P-Code containing these instructions will therefore return many diﬀerent
alternative outcomes, and may be propagating unknown values, not returning
a meaningful result. The point of the P-Code interpreter is merely to validate
the property of our semantics that it is in fact executable. In our interpreter, we
have chosen to regard INDIRECT instructions as deterministic, assuming that
their value has not been changed by the indicated side-eﬀect.


6     Changes to Ghidra and P-Code
Based on our ﬁndings, we recommend the following changes to be made to
Ghidra, P-Code and its documentation.


6.1   P-Code

Currently, the phi-node, or MULTIEQUAL as P-Code calls it, is incomplete.
It only contains a list of alternative values, but not the control ﬂow address
that guards it. We suggest to adopt the deﬁnition introduced in Sect. 4, which
includes both the address of the previous block and the value associated.


6.2   Ghidra/SLEIGH
We recommend the following changes to be made to Ghidra and its machine
code translator SLEIGH.

CBRANCH Our experiments show that Ghidra can return erroneous desti-
  nations for the CBRANCH instruction. It does have the correct information
  available, as we have validated by requesting the true-branch and false-branch
  destination via the Ghidra API instead of P-Code. It is clear that there is a
  bug in the way Ghidra produces P-Code. As mentioned before, one of three
  situations occur. The conditional branch is correct, and so is the fall-through.
  The conditional branch is incorrect, either the true-address or the fall-through
  branches to the wrong address.
Fall-through The P-Code outputted by Ghidra performs fall-through in a
  non-standard way in certain cases. For assembly languages, the fall-through
  address is the next instruction listed, or in our case, the next block listed.
  The P-Code that Ghidra returns sometimes breaks with this standard, and
  fall-through goes to the next block listed, which might have a completely
  diﬀerent address, or in some rare cases, to a completely diﬀerent block all
  together.
                                           A Formal Semantics for P-Code     125

P-Code rendering The P-Code displayed in Ghidra’s GUI uses a diﬀerent
  syntax than the one given in the P-Code documentation. The low P-Code in
  the listing view uses the capital letters notation, where tools like the graph
  AST do use the regular syntax. Readability would be greatly improved if the
  same, preferably the regular, syntax is used.

6.3   Documentation
The P-Code documentation included with Ghidra has not been updated for
several years. We suggest to make the following changes to greatly improve the
quality of the documentation, both in correctness and completeness.
High and Low P-Code The P-Code Reference Manual attempts to cover
  both low and high P-Code with one description for each instruction, and
  then tagging on extra information for the high P-Code case. We recommend
  splitting up documentation in high and low P-Code.
Varnodes In documentation, varnodes are described as containing three ele-
  ments: address space, address and size. From our experiments, we see that
  this view does not work in practice. Constants are also encoded as varnodes,
  where the address is used as a constant value instead. When performing a
  call (also see below), some address spaces are preserved, some are reset for
  the scope of the call. In this paper we have used the address space ﬁeld as the
  type of the varnode, and this seems to be a better ﬁt. We suggest one of two
  things to be done. One, this view is adopted by documentation, including a
  list of the diﬀerent types of varnodes and how they behave in for example a
  function call. Or two, the CALL and RETURN instructions are updated to
  include address space scoping.
CALL, CALLIND, RETURN As mentioned in Sect. 3, documentation
  states that CALL, CALLIND and RETURN are equivalent to BRANCH,
  BRANCHIND and BRANCHIND respectively. From our experimental
  results, we see that this is not the case. Function arguments are transferred
  via registers, local variables are reset, a value can be returned, and after
  a call, register cleanup is performed and local variables restored. We don’t
  see an issue with these instructions themselves, more with the way they are
  explained. This also ties in with the ﬁrst point made on the diﬀerence between
  low and high P-Code. Call, indirect call and return behave completely diﬀer-
  ent in low and high P-Code, and deserve a better documentation.
Small inconsistencies The documentation contains many small inconsistencies
  which should be cleared up. For example, the syntax reference introduces two
  diﬀerent notations for SUBPIECE that are not in the P-Code Operation
  reference, and that we have not found in our experiments.

6.4   Response from Ghidra Developers
We have reached out to the Ghidra development team at NSA with our ﬁndings
and the above recommendations. They have conﬁrmed our ﬁndings and acknowl-
edged all issues we found. As for the conditional branch, they refer to a GitHub
126      N. Naus et al.

issue where this problem is also identiﬁed5 . Their stance is that although it is
semantically incorrect, they do not consider this to be a bug. The destination
of the conditional jump is preserved from low to high P-Code, which they deem
more important than the correctness of the instruction itself.


7     Related Work

Research that makes use of Ghidra’s results is scarce, due to the fact that Ghidra
has only been publicly available for a few years. Below is a survey of several
interesting projects that use Ghidra and P-Code to perform program analysis.
    GhiHorn is an SMT based path analysis tool that uses Ghidra and P-Code [6].
Their goal is to determine if a path exists to a certain program point, and
how the program should be instantiated to reach this point. Their approach
relies on Ghidra’s control ﬂow API to construct ﬂow from block to block. For
the individual blocks, they use a custom made transformer from P-Code to Z3
expressions. The documentation provided is limited, and GhiHorn does not seem
to deal with the more intricate details of P-Code, such as phi-nodes, indirect and
the call/return mechanism. It would be interesting to see where this approach
leads in the future, when the tool matures further.
    A recent master thesis describes work on decompiling binaries into LLVM IR
using Ghidra [14]. The binary is loaded into Ghidra, and the decompiled P-Code
is then translated to LLVM IR. Although this work does not provide a semantics
for P-Code, it does relate LLVM IR’s semantics to that of P-Code. We’ve looked
though the source code for this project, and compared the relational semantics
to our P-Code semantics. In most cases, translation to LLVM IR seems to be
a more straight-forward aﬀair, since issues like the call/return mechanism carry
over directly. One big limitation of this work is again that more diﬃcult P-Code
concepts like phi-nodes, the nondeterministic indirect instruction, ﬂoating point
operations and pointer calculations are not supported. Looking at the translation
for conditional branches, we see that this work is susceptible to the error that
we discovered in Ghidra.
    Ghidra has also been used to develop a static taint analysis [2]. The author
uses external lists containing sources and sinks, and uses a taint policy that
deﬁnes how a taint is introduced and propagated. Unfortunately, source code for
this project is no longer available. The group is working on a new version and
has pulled the code in the mean time. It would have been very interesting to see
what P-Code semantics they employ.
    A caveat of all of these approaches is the fact that none of them do any kind of
veriﬁcation or have any formal theory on their approaches. As we have seen from
our experiments, the P-Code semantics is not straight-forward. Having a formal
semantics has the potential to improve these and future eﬀorts on decompilation
and binary analysis.


5
    https://github.com/NationalSecurityAgency/ghidra/issues/2736.
                                                A Formal Semantics for P-Code          127

8    Conclusion
We have presented a formal semantics for Ghidra’s P-Code. By developing this
semantics, we have uncovered several undocumented properties of P-Code, as
well as some inconsistencies and one serious bug in the way that Ghidra builds
the conditional branch instruction. To arrive at an executable P-Code semantics,
we have made several extensions to the language. We have validated that our
semantics is executable by building an interpreter for P-Code in Haskell. The
semantics and issues described have been acknowledged by the NSA. We have
performed a survey of binary analysis projects that leverage Ghidra and P-Code,
and have seen several that are directly aﬀected by the issues we uncovered.

Acknowledgements. We would like to thank the anonymous reviewers for their
insightful comments and suggestions, which helped to greatly improve the paper.
    This material is based upon work supported by the Defense Advanced Research
Projects Agency (DARPA) and Naval Information Warfare Center Paciﬁc (NIWC
Paciﬁc) under contract N6600121C4028 and Agreement No. HR.00112090028, and the
US Oﬃce of Naval Research (ONR) under grant N00014-17-1-2297.
    Any opinions, ﬁndings and conclusions or recommendations expressed in this mate-
rial are those of the author(s) and do not necessarily reﬂect the views of DARPA or
NIWC Paciﬁc, or ONR.


References
 1. Brumley, D., Jager, I., Avgerinos, T., Schwartz, E.J.: BAP: a binary analysis plat-
    form. In: Computer Aided Veriﬁcation–23rd International Conference, CAV 2011,
    Snowbird, UT, USA, 14–20 July 2011. Proceedings, pp. 463–469 (2011)
 2. Cole, E.: Static taint analysis of binary executables using architecture-neutral inter-
    mediate representation (2019)
 3. Cytron, R., Ferrante, J., Rosen, B.K., Wegman, M.N., Zadeck, F.K.: Eﬃciently
    computing static single assignment form and the control dependence graph. ACM
    Trans. Program. Lang. Syst. 13(4), 451–490 (1991)
 4. Eagle, C., Nance, K.: The Ghidra Book: The Deﬁnitive Guide. No Starch Press,
    California (2020)
 5. Shaila, S., Darki, A., Faloutsos, M., Abu-Ghazaleh, N., Sridharan, M.: Disco: com-
    bining disassemblers for improved performance. In: RAID 2021: 24th International
    Symposium on Research in Attacks, Intrusions and Defenses, San Sebastian, Spain,
    6–8 October 2021, pp. 148–161 (2021)
 6. Gennari, J.: Ghihorn: Path analysis in Ghidra using smt solvers. Carnegie Mellon
    University’s Software Engineering Institute Blog, 18 October 2021. http://insights.
    sei.cmu.edu/blog/ghihorn-path-analysis-in-ghidra-using-smt-solvers/
 7. Hex-Rays, S.: Ida pro disassembler (2022)
 8. Lattner, C., Adve, V.S.: LLVM: a compilation framework for lifelong program
    analysis & transformation. In: 2nd IEEE/ACM International Symposium on Code
    Generation and Optimization (CGO 2004), 20–24 March 2004, San Jose, CA, USA,
    pp. 75–88 (2004)
 9. National Security Agency: P-Code Reference Manual, September 2019
10. National Security Agency: Ghidra API help (2021)
128     N. Naus et al.

11. PNF Software: Jeb decompiler (2022). https://www.pnfsoftware.com
12. Radare org: Radare2 (2022). https://github.com/radareorg/radare2
13. Shoshitaishvili, Y., et al.: SOK: (state of) the art of war: oﬀensive techniques in
    binary analysis. In: IEEE Symposium on Security and Privacy, SP 2016, San Jose,
    CA, USA, 22–26 May 2016, pp. 138–157. IEEE Computer Society (2016)
14. Toor, T.: Decompilation of Binaries into LLVM IR for Automated Analysis. Mas-
    ter’s thesis, University of Waterloo (2022)




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
