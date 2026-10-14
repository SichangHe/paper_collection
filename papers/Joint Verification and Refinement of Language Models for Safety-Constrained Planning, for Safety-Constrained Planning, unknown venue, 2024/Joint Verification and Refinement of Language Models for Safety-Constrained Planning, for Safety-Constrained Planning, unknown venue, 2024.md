                                        Joint Verification and Refinement of Language Models
                                        for Safety-Constrained Planning

                                        Yunhao Yang                                                                        yunhaoyang234@utexas.edu
                                        University of Texas at Austin

                                        Neel P. Bhatt                                                                              npbhatt@utexas.edu
                                        University of Texas at Austin

                                        William Ward                                                                           wsw568@my.utexas.edu
                                        University of Texas at Austin
arXiv:2410.14865v2 [cs.AI] 6 Nov 2025




                                        Zichao Hu                                                                                   zichao@utexas.edu
                                        University of Texas at Austin

                                        Joydeep Biswas                                                                         joydeepb@cs.utexas.edu
                                        University of Texas at Austin

                                        Ufuk Topcu                                                                                 utopcu@utexas.edu
                                        University of Texas at Austin



                                                                                         Abstract

                                                Large language models possess impressive capabilities in generating programs (e.g., Python)
                                                from natural language descriptions to execute robotic tasks. However, these generated pro-
                                                grams often contain errors that violate externally given task specifications. Without an
                                                effective method to verify their correctness, the reliable deployment of language models in
                                                real-world systems is practically infeasible. We develop a method that converts generated
                                                robot programs into an automaton-based representation and verifies them against task-
                                                relevant safety specifications. We establish a theorem that any arbitrary combination of the
                                                verified programs will also satisfy the safety specifications. Hence, the method eliminates
                                                the need to verify complex programs composed of multiple simpler ones, reducing compu-
                                                tation complexity. We then introduce an automated fine-tuning procedure that leverages
                                                verification outcomes for supervision. By applying the theorem, this procedure only requires
                                                training the model to generate safe sub-components, thereby improving training efficiency.
                                                Empirical results on robot applications show a 30 percent increase in the probability of gen-
                                                erating specification-compliant programs, with training time reduced by half compared to
                                                fine-tuning on generating full programs. Code available: https://tinyurl.com/safe-codegen.


                                        1   Introduction

                                        As large language models (LLMs) have demonstrated significant potential in generating programs for solving
                                        robot tasks Wang et al. (2023); et al. (2022; 2021); Hu et al. (2024b), the generated programs often fail to
                                        meet the externally provided task specifications, which may lead to severe consequences in safety-critical
                                        contexts. Existing approaches Hu et al. (2024b); Liu et al. (2023b); Du et al. (2024) verify the programs by
                                        empirically collecting and checking execution traces. Such empirical verification may miss corner cases that
                                        violate the specifications. Therefore, guaranteeing that the generated programs satisfy task specifications
                                        remains challenging.
                                        Formal verification provides guarantees of compliance with specifications Baier & Katoen (2008); Mac-
                                        Conville & Monahan (2024); Shu et al. (2019); Sun et al. (2024), but applying it to LLM-generated programs


                                                                                             1
presents unique challenges. Unlike programs written with well-defined patterns, LLM-generated programs
exhibit flexible structures and inconsistent variable naming. These factors increase the difficulty of program
abstraction—a key component of verification that expresses a program in a finite-state machine. Moreover,
the size of such programs increases the state space, making verification computationally expensive.
We develop a program verification method that (1) verifies the high-level behaviors of LLM-generated
programs against externally provided specifications, and (2) alleviates the computational complexity of
verifying complex, long-horizon programs. Given a set of logical specifications (e.g., safety constraints) and
an LLM-generated program (e.g., in Python), the method converts the program into an automaton that is
amenable to formal verification tools, such as model checking. It enables verification of programs with flexible
structures and varied lengths. To address scalability, we establish a compositional verification theorem:
if individual program components each satisfy the safety specification, then any arbitrary composition of
these components also satisfies it. This theorem (illustrated in fig. 1) modularizes the verification process,
reduces the need for exhaustive, system-wide verification while maintaining safety guarantees.
                                                                                                         ¬ pedestrian
In addition, we introduce an automated fine-
tuning procedure that leverages verification                            ¬ stop sign
                                                                                                                      ¬ pedestria
                                                                                                                                    n
outcomes to improve the LLM’s ability to gen-                                               of    road
                                                                                      ¬ end                  PV
erate specification-compliant programs with-                                                               (u-turn)
                                                                                                                                        stop
out requiring human annotations. The pro-                                  PV
                                                       start                                                         pedestrian
cedure treats programs that pass formal ver-                            (forward)
                                                                                                   f r oad
ification as positive training examples and                                                   end o
                                                                                                         ¬ pedestrian
updates the model parameters in a super-                                  stop sign

vised manner. Importantly, the compositional                                                                          ¬ pedestrian
                                                                                       Tr
                                                           pedestrian




                                                                                                                                               pedestrian
verification theorem enhances fine-tuning effi-                                           u   e              PV
                                                                            stop                                                        stop
ciency: Instead of training the LLM to gen-                                           ¬ pedestrian         (right)
erate entire programs, we only need to fine-                                                                           pedestrian
tune it to generate sub-components that meet
safety specifications. Through this process, we   Figure 1: A composed program of three subprograms. The
achieve a 30 percent probability of generat-      states of each subprogram are connected in black transi-
ing specification-satisfying programs with only   tions. The orange dashed transitions connect the subpro-
20 minutes of training—halving the time re-       grams. We establish a theorem that any combination of
quired compared to training for full program      individually verified subprograms also satisfies the safety
generation.                                       specifications.
In summary, the contributions of this work are
twofold:

     • Verification: Develop a method to verify the safety of the LLM-generated programs, along with
       a theorem that ensures the safety of complex, long-horizon programs.
     • Learning: Propose a fine-tuning procedure that improves specification compliance without human
       labels, achieving better performance with reduced training time by leveraging the compositional
       verification theorem.

2   Related Work

Many existing works develop methods to generate executable programs (e.g., C++ or Python) via language
models Svyatkovskiy et al. (2020); Fried et al. (2022); Rozière & et al. (2023); et al. (2023); Nijkamp et al.
(2023); Wang et al. (2023); et al. (2022; 2021); Ahmad et al. (2021); Singh et al. (2022). However, these
works lack verification of their generated programs and directly execute them, which is risky in safety-critical
applications. The works Hu et al. (2024b;a); et al. (2022; 2021); Liu et al. (2023b); Hendrycks et al. (2021);
Austin et al. (2021); Du et al. (2024); Nguyen & Nadi (2022); Ni et al. (2023) empirically verify generated
programs against externally provided specifications. However, such empirical tests may miss edge cases,
which still pose a safety risk. In contrast, our proposed method provides formal guarantees, ensuring the
program satisfies given specifications in all possible scenarios, including all the edge cases.


                                                       2
Traditional program verification methods can verify program behaviors via model checking Nelson (1980);
Hoare (1969); Pnueli (1977); Clarke et al. (2018); Vardi & Wolper (1986); Kurshan (2000); Farias et al. (2024)
or transform programs into formal languages to constrain the values of variables or check runtime errors, e.g.,
dividing by 0 MacConville & Monahan (2024); Shu et al. (2019); Sun et al. (2024). Meanwhile, recent work has
made progress in verifying high-level plans expressed in natural language Liu et al. (2023a); Yang et al. (2024);
Yang & et al. (2024). However, these methods are incapable of verifying LLM-generated programs with
unconventional constructs, inconsistent naming, or non-modular logic, and are computationally expensive
when verifying long-horizon programs.

3   Problem Formulation
Consider a system S = (S, E, APS , APE , Φ) provided by a system designer, where

     • S is a set of subscribing functions (API calls) receiving and extracting environment or system in-
       formation. Each subscribing function fs ∈ S takes inputs from text space T (a set of all possible
       texts) and returns a Boolean value, i.e., fs : T → {0, 1}.
     • E is a set of execution functions that publish actions for the system to execute.
     • APS is a set of atomic propositions corresponding to S. Each function fs ∈ S corresponds to a
       proposition in APS .
     • APE is a set of atomic propositions corresponding to functions in E.
     • FC : S ∪ E → APS ∪ APE maps a function (with its input and output) to a corresponding atomic
       proposition.
     • Φ is a set of safety specifications over APS and APE .

A safety specification is a temporal logic formula Rescher & Urquhart (2012) asserts that “bad things” never
happen during a system’s execution.
Let P be a language model-generated program formally defined as:
Definition 1. A program P is a computer program describing a set of function sequences. Each sequence
f1 f2 ... consists of functions fi ∈ S ∪ E for i = 1, 2, ....

We show some generated programs in Section 5.1. Then, we can formulate our problem.
Problem 1: Given a system S = (S, E, APS , APE , FC , Φ) and a program P , formally verify whether P
satisfies the safety specifications Φ.
Once we can verify a single program against safety specifications, we want to prove that any combination
of verified programs will still satisfy the safety specifications. Let {Pi }m
                                                                            i=1 be a set of m programs. We can
combine these programs to solve complex tasks.
Definition 2. A composed program Cp of {Pi }m                                             C C C            C
                                                        i=1 is a sequence of programs P1 P2 P3 ..., ∀j∈N Pj ∈
     m
{Pi }i=1 .

We show an example of a composed program Cp in Fig. 1.
A composed program Cp describes a set of function sequences, where each sequence is a concatenation of
sequences described by programs in P1C P2C P3C .... For example, if f1 f2 and fa fb fc are sequences described
by P1C and P2C , respectively, then f1 fa f2 fb ... is in Cp . Note that a composed program does not need to
complete P1C and then transit to the beginning of P2C . Instead, it can halt P1C at any point and transit to
any point at P2C .
Problem 2: Given a system S = (S, E, APS , APE , FC , Φ), let Cp be a composed program of {Pi }m
                                                                                               i=1 , prove
the following statement:

     If every program in {Pi }m                                                     m
                              i=1 satisfies Φ, then the composed program Cp of {Pi }i=1 also satisfies Φ.


                                                       3
                                                                Phase 1: Training Data Collection

                                       velocity_publisher ( )          publish velocity,
                                         car_observed ( )                    car,              G( car 𝒢 ¬ publish velocity )
                                      stop_sign_observed ( )              stop sign                stop sign 𝒢 F sleep
                                          sleep ( ), exit ( )            sleep, exit
                                         Functions in S Φ E         Props APS Φ APE               Safety Specifications ∪
       Autonomous System

                                                     1                                             Task: Turn left safely.
                                                                                                                                                     3
                                                               Program P
                                                                                                                                                                                       Safety-Constrained
                                                                                                                                           Model
                                                                                                                             q1→ q2→ q2: observe traffic & Wait   q2→ q3: turn left
                                                                                                                                                                                            Programs
       Turn left 90 degrees                                                                                                               Checking                                    go_straight ( ), stop ( ),
                                                                                           2                                                                         Add P
        Task Description                                                                                                                                                                       ……
                              Language Model M                                                  Automaton →                  q1→ q2→ q2: observe traffic & Wait   q2→ q3: turn left




                                                               Change Random Seed and Re-query


                                                                         Phase 2: LLM Training
                                                         Task prompt
                              Task Bank
                                                                              Training Data                                   4
                         Safety-Constrained                              { Input: Task prompt ,
                                                                          Output: Program}             Supervised Fine-tuning
                              Programs
                        go_straight ( ), stop ( ),
                                                          Program                                                                                       Language Model M
                                 ……



Figure 2: In this pipeline, we verify each LLM-generated program and add the specification-compliant
programs to a set of safety-constrained programs, which will be used for fine-tuning the LLM.
4     Methodology

We present a method for verifying and improving LLM-generated robot programs to satisfy externally pro-
vided safety specifications. The method consists of three key components: (1) converting the generated
program into an automaton-based representation suitable for formal verification, (2) applying a composi-
tional verification theorem to scale verification across program components, and (3) fine-tuning the language
model using verified subprograms to improve specification compliance.

4.1   Program Verification Against Safety Specifications

Since a program is not formally verifiable directly, we transform it into a verifiable form and then verify the
transformed program against logic-based safety specifications in Φ.
First, we construct a transition system T S = (Qs , Ts , Ls ) representing the task environment.
Definition 3. A transition system T S = (Qs , Ts , Ls ) is a tuple of a set of states Qs , a set of transitions
Ts = {(qi , qj ) | qi , qj ∈ Qs }, i.e., (qi , qj ) means a transition from state qi to qj , and a label function
Ls : Qs → 2AP .

AP is a set of atomic propositions. Each atomic proposition has a truth value—true or false—but does
not contain any logical connectives like "and," "or," "not," etc. This system builds transitions between every
conjunction of the truth values of propositions in APS .
Next, we construct an automaton that represents each program.
Definition 4. A finite-state automaton (FSA) A = (Qa , p0 , Ta , La ) is a tuple consisting of a set of
states Qa , an initial state p0 , a set of transitions Ta = {(pi , σ, pj ) | pi , pj ∈ Qa , σ ∈ 2AP }, and a label
function La : Qa → 2AP .

Consider a system S, a program Pi , and a transition system T S. We construct an FSA A such that: For
every function sequence f1 f2 , ... described by Pi , there is a corresponding sequence FC (f1 )FC (f2 )... described
by A.
To build the FSA, we follow the three steps below:


                                                                                     4
Algorithm 1: AST to Finite state automaton (FSA)
 1: procedure Tree2FSA(root, keywords, keyword_processor)              ▷ keywords is a set of predefined words,
    keyword_processor is a function
 2:    Qa , Ta , La = [], [], []
 3:    create an initial state p0 , Qa .add(p0 ), La (p0 ) = ∅
 4:    pcurrent = p0                                                          ▷ keep track of the current state
 5:    for node in root.children do
 6:        if (every node in node.children is leaf) | (node.children[0] in keywords) then
 7:             Q̃, p̃0 , T̃ , L̃ = keyword_processor(node)
 8:        else
 9:             Q̃, p̃0 , T̃ , L̃ = Tree2FSA(node, keywords, keyword_processor)           ▷ Preorder Traversal
10:        end if
11:        Qa + = Q̃, Ta + = T̃ , La + = L̃                                        ▷ merge the sub-automaton
12:        Ta .add((pcurrent , T rue, p̃0 ))
13:        pcurrent = p̃0
14:    end for
15:    return Qa , p0 , Ta , La
16: end procedure



1) Parse Pi into an abstract syntax tree (AST).
2) Define a keyword processor that maps an AST with predefined keywords and specified structures to an
FSA, as presented in Table 1.
3) Follow Algorithm 1 to build an FSA. Note that the algorithm takes the root of AST and the keyword
processor as inputs and returns an FSA A = (Qa , p0 , Ta , La ).
Once the FSA A is constructed, we formulate a product automaton by implementing the FSA in the transition
system T S, denoted as P = A ⊗ T S.
Definition 5. Given an FSA A and a transition system T S, a product automaton P of A and T S,
denoted P = A ⊗ T S, is a tuple (Q, Q0 , T, L), where
Q = {(p, q) | p ∈ Qa , q ∈ Qs }, Q0 = {p0 } × Qs , T = {((p, q), (p′ , q ′ )) | p ∈ Qa , q ∈ Qs , (p, Ls (q), p′ ) ∈
Ta , (q, q ′ ) ∈ Ts }, and L((p, q)) = La (p) ∪ Ls (q), where p ∈ Qa , q ∈ Qs .

In the product automaton P = (Q, Q0 , T, L),

      • a prefix is a finite sequence of states starting from (p0 , q0 ) ∈ Q0 , e.g., (p0 , q0 )(p1 , q1 )(p2 , q2 )...(pk , qk ),
        k is the prefix length,

      • a trace ϕ is a sequence of labels L((p0 , q0 ))L((p1 , q1 )) . . . , where Traces(P) denotes the set of all
        traces from P. In words, Traces(P) captures all possible behaviors of A in the task environment
        represented by T S.

Finally, we use a model checker Cimatti et al. (2002) to verify whether the product P satisfies all the
specifications Φ. If a program’s automaton satisfies all the specifications, we add this program to a set of
safety-constrained programs. We present an illustration of this procedure in fig. 2 Phase 1.

4.2   Safety of Composed Program

As verifying long-horizon programs directly can be computationally expensive, we propose a compositional
verification theorem that allows the safety of complex programs to be inferred from their components.
Specifically, if each subprogram satisfies the safety specification in isolation, then their composition also
satisfies the specification under mild assumptions. An example of a composed program is in fig. 1.


                                                                5
   AST                               FSA                                       Note
   start        root




                                                              ¬σ
                                     start            ∅                        σ = FC (fs ), ω = FC (fe ), fs ∈ S, fe ∈
                                                                               E. “For loop” can be expressed by




                                                     ¬σ
                                                          σ
                while
                                                                               “while loop.”
                                                      ω




                                                              σ
       fs               fe

   start        root




                                                              ¬σ
                                     start            ∅




                                             T rue
                                                                               σ, ω = FC (fs ), FC (fe ), fs ∈ S, fe ∈ E.




                                                          σ
                 if

       fs               fe                            ω


   start         root                start            ∅
                                                                               σ, ω1 , ω2 = FC (fs ), FC (fe1 ), FC (fe2 ).
                                          e
                                                          T ru
                                                          ¬σ
                                         σ
                                      T ru



           if           else                                                   For “if-elif-else,” we duplicate the “if”
                                                               e

                                                                               node and replace it with “elif.”
    fs fe1              fe2             ω1                  ω2

Table 1: A subset of rules to convert abstract syntax trees to FSA-based representations. We present the
complete rules in the Appendix.


To establish and prove the theorem, we first need to define the terminology safety. Let ϕ ∈ Φ be a temporal
logic formula. We call ϕ a safety specification if it describes a safety property Baier & Katoen (2008) as
defined in definition 6.
Definition 6. A safety property Psafe is a set of traces in (2AP )ω (ω means infinite repetitions) such that
for all traces ψ ∈ (2AP )ω \Psafe , there is a finite-length prefix ψ̂ such that

                                     Psafe ∩ {ψ ∈ (2AP )ω | ψ̂ is a prefix of ψ} = ∅.

ψ̂ is a bad prefix, and BadPref(Psafe ) denotes the set of all bad prefixes.

From the definition of safety property, we derive the proposition below.
Proposition 1. Let ϕ describe safety property Psafe , an automaton P satisfies ϕ (denoted as P |= ϕ) if and
only if Traces(P) ⊆ Psafe .
                                                                                               ¬σ1
From section 4.1, we obtain a set of safety-constrained
programs where each program satisfies the safety spec-                           start         ω1
                                                                                                             ¬σ2
ifications. To proceed with our theorem establishment,
we introduce a terminology joint automaton as defined in                                                     ω3    True   ω4
                                                                                          σ1




Definition 7.                                                                                        Tru
                                                                                                         e         σ2
                                                                                   True




                                                                                               ω2
Definition 7. Let P1 = (Q1 , Q01 , T1 , L1 ) and P2 =
(Q2 , Q02 , T2 , L2 ) be two automata over the same set of
                                                                       Figure 3: An example of a joint automaton P ∗ =
atomic propositions. Consider a new set of transitions
                                                                       (Q1 ∪ Q2 , Q01 , T1 ∪ T2 ∪ T ∗ , L1 ∪ L2 ) of P1 and
T ∗ : {(q, q ′ ) | q ∈ Q1 , q ′ ∈ Q02 } that transit from a subset
                                                                       P2 . We mark P1 and P2 in blue and purple, and
of P1 ’s states to a subset of P2 ’s initial states. We define
                                                                       mark the transition in T ∗ in orange.
P ∗ = (Q1 ∪ Q2 , Q01 , T1 ∪ T2 ∪ T ∗ , L1 ∪ L2 ) as a joint
automaton of P1 and P2 .

Figure 3 is a joint automaton of two automata.
Note that we can “connect" a joint automaton of P1 and P2 with P3 to obtain a new joint automaton of the
three automata. By repeating this procedure, we can get the joint automaton of any number of automata.
Such a joint automaton is the representation of the composed program:


                                                                   6
Remark 1. Let {Pi }m                                                   m
                     i=1 be a set of safety-constrained programs, {Pi }i=1 be the product automata corre-
sponding to the programs. Let Cp be a composed program of the programs in {Pi }m    i=1 , then there exist a
joint automaton P ∗ captures the behaviors of Cp .
Theorem 1. [Compositional Verification Theorem] Given a safety property Psafe , two automata P1 =
(Q1 , Q01 , T1 , L1 ) and P2 = (Q2 , Q02 , T2 , L2 ), let P ∗ = (Q1 ∪ Q2 , Q01 , T1 ∪ T2 ∪ T ∗ , L1 ∪ L2 ) be a joint
automaton of P1 and P2 , assume
1) P1 and P2 satisfy Psafe ,
                     / BadPref(Psafe ), for any (q, q ′ ) ∈ T ∗ ,
2) for any prefix ψ̂ ∈

                                             ψ̂L1 (q)L2 (q ′ ) ∈
                                                               / BadPref(Psafe ),                                  (1)

then P ∗ satisfies Psafe .

Proof. Assume P ∗ does not satisfy Psafe , there exists a trace ψ from P ∗ such that ψ has a prefix ψ̂ ∈
BadPref(Psafe ).
Let ψ = ψ1 L1 (q)L2 (q ′ )ψ2 be a trace with the bad prefix, where ψi ∈ Traces(Pi ), i ∈ [1, 2] and (q, q ′ ) ∈ T ∗ .
Since P1 satisfies Psafe , ψ1 does not contain any bad prefix. Then, by the assumption of eq. (1), ψ1 L1 (q)L2 (q ′ )
does not contain any bad prefix. Similarly, ψ2 does not contain bad prefix because P2 satisfies Psafe .
Therefore, ψ does not have a bad prefix, which leads to a contradiction. Hence, we have proved that P ∗
satisfies Psafe .

Proposition 2. Given a safety property Psafe , let P ∗ be a joint automaton of {Pi }m
                                                                                    i=1 such that


      • all Pi , i ∈ [1, ..., m] satisfy Psafe ,

                          / BadPref(Psafe ), for any (q, q ′ ) such that q ∈ Qx , q ′ ∈ Q0y , x ̸= y,
      • for any prefix ψ̂ ∈                                                                             eq. (1) holds,

then, P ∗ satisfies Psafe .

Proof. We prove proposition 2 by induction.
Base case: the joint automaton of two automata satisfies Psafe , by theorem 1.
Inductive step: assume the joint automaton P ∗ of m automata {Pi }m  i=1 satisfies Psafe . Consider a new joint
automaton P ∗∗ of P ∗ and Pm+1 , where Pm+1 also satisfies Psafe , by theorem 1, P ∗∗ satisfies Psafe .
By the theory of induction, we have proved proposition 2.

For any complex task that can be broken down into
simpler sub-components, it is unnecessary to con-
struct and verify an automaton for the overall pro-
gram. Instead, the safety of the complex task
can be asserted if the simpler components
from which it is composed are themselves
safe. This conclusion significantly reduces verifi-
cation complexity.

4.3   Verification-Guided Refinement
                                                    Figure 4: By Theorem 1, we can safely execute the
To improve the quality of LLM-generated programs, composed program to solve complex tasks without fur-
we introduce an automated fine-tuning procedure ther verification.
that uses verification outcomes as feedback. Unlike


                                                              7
Figure 5: The three robots we used in the experiments. From left to right, we name them Jackal outdoor
robot, Jackal indoor robot, and Spot robot dog.




                              pedestrian=False                pedestrian=True                 pedestrian=True
                         publish velocity (turn right)   publish velocity (turn right)   publish velocity (turn right)




                              pedestrian=True                 pedestrian=False                pedestrian=True
                                    stop                 publish velocity (turn right)              stop


Figure 6: A failure example of executing the first program “turn_right_90_degrees_1” (top row) and
a success example of executing the second program “turn_right_90_degrees_2”(bottom row). The first
program publishes velocity even if a pedestrian is observed, which violates the safety specification.




traditional supervised learning, which requires man-
ually labeled data, our method relies entirely on formal verification results to supervise the training process.
This enables the LLM to iteratively improve its ability to generate specification-compliant programs without
human intervention.
The fine-tuning procedure works as follows:
(1) Given a set {t1 , t2 , ...} of task descriptions, query the language model M to generate executable program
{P1 , P2 , ...}. We can get multiple programs with each task description by varying the random seeds.
(2) For each program Pi , construct an FSA Ai and verify it against the specifications Φ.
(3) If Ai satisfies all the specifications, we add Pi to the set of safety-constrained programs and formulate a
(ti , Pi ) pair that consists of the program and its corresponding task description.
(4) Repeat 2 and 3 to obtain a set of {(ti , Pi )}ni=1 pairs, which we considered as the training dataset with n
samples.
(5) Use the set of pairs as supervised training data to fine-tune the language model, as presented in fig. 2
Phase 2. We consider task descriptions ti as inputs and safety-constraint programs Pi as labels.
Due to the compositional verification theorem, we only need to verify and fine-tune on subprogram
generation (each safety-constrained program is a subprogram for a composed program), rather than
training for generating complete, long-horizon programs. This reduces the computational cost of
both verification and model training.


                                                                      8
                                           True        backpack=True, person=False   backpack=True, person=True
                                       go to lounge              sleep                          ask


           Figure 7: Execution of the program “bring_backpack_2,” which passes the safety specification.


    5     Demonstration

    We first present two robot demonstrations to iterate the steps of verifying the language model-generated
    programs against safety specifications in Section 5.1 and 5.2. In the experiments, we use GPT-4o-mini as
    the language model. We also demonstrate the necessity of these verification steps through two examples.

    5.1    Outdoor Driving Task

    We first present a demonstration of a Jackal outdoor robot (on the left of Figure 5) over a driving task. We
    formally define the system for this robot as follows:
        S = {pedestrian_observed()}, E = velocity_publisher(), stop(),
        APS = {pedestrian}, APE = {publish velocity, stop},
        FC (pedestrian_observed()) = pedestrian, FC (stop()) = stop, FC (velocity_publisher()) = publish velocity,
    and we verify the generated programs against the specification

                                               ϕ = G( pedestrian → X ¬ publish velocity ),

    meaning that the system should never publish velocity when seeing a pedestrian ahead.
    We send the sets of subscribing functions S and execution functions E (i.e., robot APIs) along with their
    textual descriptions to a language model. Then, query for a task “turn right at a 90-degree intersection.”
    By varying the random seeds of the language model, we obtain the following two responses:


1   def t u r n _ r i g h t _ 9 0 _ d e g r e e s _ 1 () :
2       ......
3       if p e d e s t r i a n _ o b s e r v e d () :
4               stop ()
5       v e l o c i t y _ p u b l i s h e r ( linear , angular )
1   def t u r n _ r i g h t _ 9 0 _ d e g r e e s _ 2 () :
2       ......
3       while True :
4           if p e d e s t r i a n _ o b s e r v e d () :
5               stop ()
6           else :
7               v e l o c i t y _ p u b l i s h e r ( linear , angular )

    Then, we follow the method in Section 4.1 to construct an automaton-based representation for each of the
    executable programs and present them in Figure 8. For brevity, the automata we present correspond to the
    blue parts in the programs. The rest are variable assignments, which are irrelevant to our specification.
    Next, we verify the two automata against our safety specification ϕ. The verification results indicate that
    the first program fails the specification. The counterexample shows a scenario where another pedestrian is
    coming after the action “stop.” There is no double check on pedestrians before publishing velocity. Hence,


                                                                                9
                                                                                      True
      start                 ∅                         start                ∅                     PV
                                         Tr                                                                           ¬ backpack                                                           ¬ (backpack ∧ person)
                                            u



                                  True
                                             e                                    ¬ pedestrian
                                                                                                                                                                                                                      True




                                                              pedestrian
                                                                                                       start                     ∅                                                         start           ∅




                                                                               True
                                                                                                                                                                                                                                      ask
                            ∅                        PV




                                                                                                                      backpack
              pedestrian



                                  ¬ pedestrian                                                                                                                                                                 backpack ∧ person




                                                                                                           ¬ person
                                                 e                                                                                      True
                                               u                                                                                 ∅                                                              ask
                           stop             Tr                        stop                                                             person


Figure 8:   We show the constructed automaton-based representations of the executable pro-
grams   “turn_right_90_degrees_1,”       “turn_right_90_degrees_2,”        “bring_backpack_1,” and
“bring_backpack_2”(from left to right). PV stands for publishing velocity.


this program fails the specification and may lead to safety risks during execution. We present an example
of such a safety violation in Figure 6. In contrast, the second program satisfies the specification and leads
to a safe execution, as presented in Figure 6.
This example indicates the necessity of our proposed method. The formal verification provides mathematical
guarantees for the programs. Hence, we can catch all the edge cases that may violate safety specifications
without an empirical study.


5.2   CodeBotler

The second demonstration uses the Jackal indoor robot (the middle robot in Figure 5). The robot system is
  S = {is_in_room(), get_current_location()}, E = {ask(), go_to()},
  APS = {person, backpack}, APE = {ask, go},
  FC (is_in_room(“person”)) = person, FC (is_in_room(“backpack”)) = backpack, FC (ask(...)) = ask,
FC (go_to(...)) = go.
We generate programs using CodeBotler Hu et al. (2024b)—a few-shot program generator using language
models—and verify the generated programs against the specification

                                                          ϕ = G(¬( person ∧ backpack ) → ¬ ask ).

We require the robot to only ask for help when the backpack and the person exist.
We query the language model to generate a program for the task “bring my backpack back from the lounge”
given the APIs in S ∪ E. We show two of the generated programs in the Appendix.
We construct automaton-based representations for the two pro-
grams and present them in Figure 8. Then, we formally verify
                                                                                                                                            Probability of Satisfying the Specification




the two automata against the specification ϕ. The first au-                                                                                                                                1

tomaton violates the specification with a counterexample “¬
                                                                                                                                                                                          0.8
backpack ∧ ask.” This counterexample captures an edge case:
A person takes the backpack and responds “no,” the robot will
                                                                                                                                                                                          0.6
ask the next person to put the backpack without checking if the
backpack still exists. We argue that this edge case is hard to                                                                                                                            0.4
catch by empirical experiments, but it will lead to a specifica-
tion violation. We use this example to highlight the necessity of                                                                                                                         0.2
our proposed method. In contrast, the second automaton sat-                                                                                                                                           Φ1         Φ2          Φ3
                                                                                                                                                                                                            Specifications
isfies the specification. We successfully execute the program                                                                          Before Refinement                                              Checkpoint 1 Checkpoint 2   Final   In-Context
and show the execution in Figure 7.
                                                                                                                                     Figure 9: Probability of each specification
                                                                                                                                     being satisfied before and after fine-tuning
                                                                                                      10
                                                                                                                                     the language model. Checkpoints 1, 2, and
                                                                                                                                     Final refer to the language model after 130,
                                                                                                                                     230, and 350 epochs of fine-tuning. “In-
6     Quantitative Analysis

We have demonstrated the proposed method in the previous
section and indicated its necessity. In this section, we conduct
quantitative studies to show the probability of the language
model generating safety-constrained programs. Then, we fine-
tune the language model and show how much the fine-tuning
procedure can improve such probability.

6.1   Automated Refinement

We first follow the steps in Section 4.3 to automatically collect fine-tuning data and use it to fine-tune the
parameters of the language model. Recall that we consider the programs that pass all the specifications as the
ground truth during fine-tuning. We use the system described in Section 5.1 and the following specifications
to fine-tune the language model:
ϕ1 = G( pedestrian → X ¬ publish velocity ),
ϕ2 = G(¬( pedestrian ∨ ¬ stop sign ) → X ¬ stop ),
ϕ3 = G( car → X ¬ publish velocity ).
We employ the default supervised fine-tuning algorithm with negative log-likelihood loss and early stopping
(at convergence) Dodge et al. (2020), as proposed by OpenAI Liu et al. (2023c). We collect 100 training
samples and set the maximum number of epochs to 400. Each training sample is a (prompt, program) pair,
where the prompt is a random driving task, e.g., go straight 10 meters, make a 60-degree left turn, etc.
Then, we select three checkpoints, test them over a separate set of driving tasks, and show the probability of
each checkpoint generating safety-constrained programs in Figure 9. We observe a consistent improvement
in the probability of satisfying each specification during fine-tuning. The final fine-tuned model increases
such probability by over 50 percent compared with the initial model. On the other hand, our fine-
tuned model also outperforms in-context learning, in which we provide between 1 and 5 manually generated
in-context examples in the input prompt.
                                                                      Probability of Satisfying the Specification




In conclusion, even in the absence of task or system knowl-                                                          1
edge, i.e., unable to provide in-context examples, our fine-
tuning procedure can improve the probability of the lan-                                                            0.8
guage model generating safety-constrained programs to
nearly 100 percent. In addition, this fine-tuning proce-
                                                                                                                    0.6
dure only consumes 100 samples and less than 5 min-
utes of training on a single Nvidia A100 GPU.
                                                                                                                    0.4
By leveraging the compositional verification theorem,
which ensures that any combination of verified sub-                    0.2
programs preserves safety, we shift the focus to fine-                          ϕ4       ϕ5         ϕ6      ϕ7
                                                                                         Specifications
tuning on smaller, verifiably safe components. This mod-                   Before Refinement Final (After Refinement)
ular approach reduces training time by 50 percent while
maintaining the likelihood of generating safety-compliant Figure 10: Out-of-domain test: We fine-tune the
programs.                                                   language model over the ground robot to meet
                                                            ϕ1 , ..., ϕ4 and then test it over a different robot
6.2 Out-of-Domain Validation                                (robot dog) against specifications ϕ5 , ..., ϕ7 . Over
                                                            the new robot, there is an improvement in the
Next, we validate our fine-tuned language model over probability of each specification being satisfied
some out-of-domain autonomous systems and tasks. We after the fine-tuning process.
validate the model via the Jackal indoor robot and Spot
robot dog (see Figure 5). We have defined the system for
the Jackal indoor robot in Section 5.2, and the specification is


                                                         11
ϕ4 = G(¬( person ∧ backpack ) → ¬ ask ).
The system for the robot dog is
    S = {person_observed(), target_observed()},
    E = {navigate(), stop(), signal()},
    APS = {person, target},
    APE = {navigate, stop, signal},
    FC (person_observed()) = person, FC (stop()) = stop,
    FC (target_observed()) = target, FC (navigate()) = navigate, FC (signal()) = signal.
The specifications for the robot dog are:
ϕ5 = G( person → X ¬ navigate ),
ϕ6 = G(¬ person ∧ target → X ¬ navigate ),
ϕ7 = G(¬ target → X ¬ signal ).
We query the language model to generate 20 programs per task. The task for the indoor robot is “bringing
my backpack back from the lounge,” and the task for the robot dog is “finding the target and sending a
signal.” We compare the probability of the generated programs satisfying the specifications before and after
fine-tuning. The results in Figure 10 indicate that our fine-tuned model improves such probability by
an average of 30 percent over the out-of-domain tasks. Hence, our fine-tuning procedure is not
restricted to the system it is fine-tuned for, and it also increases the chance of satisfying safety specifications
for tasks in any robot system.
                                                        Probability of Satisfying the Specification




6.3    Additional Baseline Comparison                                                                  1

We evaluate our fine-tuned GPT-4o-mini
                                                                                                      0.8
model against several strong pretrained
baselines, including GPT-4.1, GPT-4o,
GPT-4o-mini (pre-trained), and DS-R1-                                                                 0.6

Qwen-7B. Despite being fine-tuned on
only 100 verified programs and trained                                                                0.4
for less than one hour, our model outper-
forms all baselines — achieving the high-                                                             0.2
est specification-satisfaction rate — while                                                                 Φ1   Φ2   Φ3    Φ4      Φ5   Φ6      Φ7
also surpassing large pre-trained models                                                                              Specifications

with 20 times the parameter size.
                                                GPT-4o-mini                                             DS-R1-Qwen-7B      GPT-4o      GPT-4.1    GPT-4o-mini (refined)
In addition to the satisfaction rate, our
fine-tuned model exhibits significantly Figure 11: We compare our fine-tuned GPT-4o-mini with other
lower latency. The average response time pre-trained models. With only 100 training samples and less than
for generating a single program is approx- an hour of training, our fine-tuned model outperforms baseline
imately half that of larger models such models with 20x parameter size.
as GPT-4o and GPT-4.1, demonstrating
the practicality of our approach for real-time applications. We present detailed results in the Appendix.


7     Conclusion

This work addresses a critical limitation in deploying large language models for robotic programming by
introducing a verification framework that ensures compliance with safety specifications. By representing
generated programs as automata and verifying them at the sub-component level, the method guarantees
the correctness of both individual and composed programs. A central contribution is the compositional


                                                        12
verification theorem, which guarantees that any combination of individually verified sub-programs will also
satisfy the overall safety specifications. This theorem removes the need to verify complex programs in their
entirety, significantly reducing computational overhead.
We then propose an automated fine-tuning procedure that uses verification outcomes as supervision. Due
to the composition theorem, the model only needs to learn to generate safe sub-components, enabling more
efficient and modular training. Empirical results validate the effectiveness of this approach, showing a
30% increase in the generation of specification-compliant programs and a 50% reduction in training time.
Together, these contributions pave the way for safer and more scalable deployment of language models in
real-world robotic systems.
As a future direction, we can 1) incorporate multimodal inputs, such as visual or sensory data, into the
planning process to create richer, more context-aware plans, and 2) develop systems that allow for humans-
AI collaboration in program generation, where human feedback can dynamically influence the planning
process to ensure compliance with nuanced or unstructured task specifications.

Broader Impact Statement

This work enables safer and more efficient use of language models in robot program generation by developing
a method to verify generated programs against task-specific safety specifications. This work guarantees that
any combination of verified sub-programs also satisfies the specifications, eliminating the need to verify
complex compositions and improving computational efficiency. An automated LLM fine-tuning procedure
results in a 30% increase in specification-conformant programs while reducing training time by half.

References
Wasi Uddin Ahmad, Saikat Chakraborty, Baishakhi Ray, and Kai-Wei Chang. Unified pre-training for
 program understanding and generation. In Conference of the North American Chapter of the Association
 for Computational Linguistics: Human Language Technologies, pp. 2655–2668, Online, 2021. Association
 for Computational Linguistics.
Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk Michalewski, David Dohan, Ellen
  Jiang, Carrie Cai, Michael Terry, Quoc Le, et al. Program synthesis with large language models. arXiv
  preprint arXiv:2108.07732, 2021.
Christel Baier and Joost-Pieter Katoen. Principles of model checking. MIT press, MA, USA, 2008.
Alessandro Cimatti, Edmund Clarke, Enrico Giunchiglia, Fausto Giunchiglia, Marco Pistore, Marco Roveri,
  Roberto Sebastiani, and Armando Tacchella. Nusmv 2: An opensource tool for symbolic model checking.
  In International conference on computer aided verification, pp. 359–364. Springer, 2002.
Edmund M. Clarke, Orna Grumberg, Daniel Kroening, Doron A. Peled, and Helmut Veith. Model checking,
  2nd Edition. MIT Press, Cambridge, Massachusetts, USA, 2018.
Jesse Dodge, Gabriel Ilharco, Roy Schwartz, Ali Farhadi, Hannaneh Hajishirzi, and Noah Smith. Fine-
  tuning pretrained language models: Weight initializations, data orders, and early stopping. arXiv preprint
  arXiv:2002.06305, 2020.
Xueying Du, Mingwei Liu, Kaixin Wang, Hanlin Wang, Junwei Liu, Yixuan Chen, Jiayi Feng, Chaofeng Sha,
 Xin Peng, and Yiling Lou. Evaluating large language models in class-level code generation. In Proceedings
 of the 46th IEEE/ACM International Conference on Software Engineering, ICSE 2024, pp. 81:1–81:13,
 Lisbon, Portugal, 2024. ACM.
Erik Nijkamp et al. Codegen: An open large language model for code with multi-turn program synthesis.
  In International Conference on Learning Representations, Kigali, Rwanda, 2023. OpenReview.net.
Mark Chen et al. Evaluating large language models trained on code, 2021.
Yujia Li et al. Competition-level code generation with alphacode. Science, 378(6624):1092–1097, 2022.


                                                    13
Bruno Farias, Rafael Menezes, Eddie B. de Lima Filho, Youcheng Sun, and Lucas C. Cordeiro. Esbmc-
  python: A bounded model checker for python programs. In International Symposium on Software Testing
  and Analysis, pp. 1836–1840, Vienna, Austria, 2024. ACM.

Daniel Fried, Armen Aghajanyan, Jessy Lin, Sida Wang, Eric Wallace, Freda Shi, Ruiqi Zhong, Wen-tau
 Yih, Luke Zettlemoyer, and Mike Lewis. Incoder: A generative model for code infilling and synthesis.
 arXiv preprint arXiv:2204.05999, 2022.

Dan Hendrycks, Steven Basart, Saurav Kadavath, Mantas Mazeika, Akul Arora, Ethan Guo, Collin Burns,
 Samir Puranik, Horace He, Dawn Song, et al. Measuring coding challenge competence with apps. arXiv
 preprint arXiv:2105.09938, 2021.

C. A. R. Hoare. An axiomatic basis for computer programming. Commun. ACM, 12(10):576–580, 1969.

Zichao Hu, Junyi Jessy Li, Arjun Guha, and Joydeep Biswas. Robo-instruct: Simulator-augmented instruc-
  tion alignment for finetuning codellms, 2024a. URL https://arxiv.org/abs/2405.20179.

Zichao Hu, Francesca Lucchetti, Claire Schlesinger, Yash Saxena, Anders Freeman, Sadanand Modak, Arjun
  Guha, and Joydeep Biswas. Deploying and evaluating llms to program service mobile robots. IEEE
  Robotics Autom. Lett., 9(3):2853–2860, 2024b.

Robert P Kurshan. Program verification. Notices of the AMS, 47(5):534–545, 2000.

Jason Xinyu Liu, Ziyi Yang, Ifrah Idrees, Sam Liang, Benjamin Schornstein, Stefanie Tellex, and Ankit
  Shah. Grounding complex natural language commands for temporal tasks in unseen environments. In
  Conference on Robot Learning, volume 229 of Proceedings of Machine Learning Research, pp. 1084–1110,
  Atlanta, GA, USA, 2023a. PMLR.

Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang. Is your code generated by chatgpt
  really correct? rigorous evaluation of large language models for code generation. In Advances in Neural
  Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023,
  NeurIPS 2023, New Orleans, LA, USA, 2023b.

Xiao Liu, Yanan Zheng, Zhengxiao Du, Ming Ding, Yujie Qian, Zhilin Yang, and Jie Tang. Gpt understands,
  too. AI Open, 1:0–11, 2023c.

Dara MacConville and Rosemary Monahan. Towards a model checker for python: pymodcheck. In Interna-
 tional Workshop on Formal Techniques for Java-like Programs, pp. 1–4, Austria, 2024. ACM.

Charles Gregory Nelson. Techniques for program verification. PhD thesis, Stanford University, Stanford,
  CA, USA, 1980.

Nhan Nguyen and Sarah Nadi. An empirical evaluation of github copilot’s code suggestions. In IEEE/ACM
 International Conference on Mining Software Repositories, pp. 1–5, Pittsburgh, PA, USA, 2022. ACM.

Ansong Ni, Srini Iyer, Dragomir Radev, Veselin Stoyanov, Wen-Tau Yih, Sida I. Wang, and Xi Victoria Lin.
 LEVER: learning to verify language-to-code generation with execution. In International Conference on
 Machine Learning, volume 202, pp. 26106–26128, Honolulu, Hawaii, USA, 2023. PMLR.

Erik Nijkamp, Hiroaki Hayashi, Caiming Xiong, Silvio Savarese, and Yingbo Zhou. Codegen2: Lessons for
  training llms on programming and natural languages, 2023.

Amir Pnueli. The temporal logic of programs. In 18th Annual Symposium on Foundations of Computer
 Science, 1977, pp. 46–57, Providence, Rhode Island, USA, 1977. IEEE Computer Society.

Nicholas Rescher and Alasdair Urquhart. Temporal logic, volume 3. Springer Science & Business Media,
  Germany, 2012.

Baptiste Rozière and Jonas Gehring et al. Code llama: Open foundation models for code, 2023.


                                                   14
Xinfeng Shu, Fengyun Gao, Weiran Gao, Lili Zhang, Xiaobing Wang, and Liang Zhao. Model checking python
  programs with MSVL. In Structured Object-Oriented Formal Language and Method - 9th International
  Workshop, volume 12028 of Lecture Notes in Computer Science, pp. 205–224, Shenzhen, China, 2019.
  Springer.
Ishika Singh, Valts Blukis, Arsalan Mousavian, Ankit Goyal, Danfei Xu, Jonathan Tremblay, Dieter Fox,
  Jesse Thomason, and Animesh Garg. Progprompt: Generating situated robot task plans using large
  language models. arXiv preprint arXiv:2209.11302, 2022.
Chuyue Sun, Ying Sheng, Oded Padon, and Clark W. Barrett. Clover: Closed-loop verifiable code generation.
  In AI Verification - First International Symposium, volume 14846 of Lecture Notes in Computer Science,
  pp. 134–155, Montreal, QC, Canada, 2024. Springer.
Alexey Svyatkovskiy, Shao Kun Deng, Shengyu Fu, and Neel Sundaresan. Intellicode compose: code gen-
  eration using transformer. In Joint European Software Engineering Conference and Symposium on the
  Foundations of Software Engineering, pp. 1433–1443, Virtual, 2020. ACM.
Moshe Y. Vardi and Pierre Wolper. An automata-theoretic approach to automatic program verification
 (preliminary report). In Proceedings of the Symposium on Logic in Computer Science (LICS ’86), pp.
 332–344, Cambridge, Massachusetts, USA, 1986. IEEE Computer Society.

Yue Wang, Hung Le, Akhilesh Gotmare, Nghi D. Q. Bui, Junnan Li, and Steven C. H. Hoi. Codet5+:
  Open code large language models for code understanding and generation. In Conference on Empirical
  Methods in Natural Language Processing, pp. 1069–1088, Singapore, 2023. Association for Computational
  Linguistics.

Yunhao Yang and Neel P. Bhatt et al. Fine-tuning language models using formal methods feedback: A use
  case in autonomous systems. In Conference on Machine Learning and Systems, CA, USA, 2024. mlsys.org.
Yunhao Yang, Cyrus Neary, and Ufuk Topcu. Multimodal pretrained models for verifiable sequential decision-
  making: Planning, grounding, and perception. In International Conference on Autonomous Agents and
  Multiagent Systems, pp. 2011–2019, New Zealand, 2024. ACM.




                                                   15
A      Details of Program-Automaton Conversion

Executable Program to Abstract Syntax Tree Recall that an executable program is a program that
consists of a set of predefined keywords and grammar associated with the keywords. Given a program, we
first parse it into an AST. We use an existing parsing method with built-in rules for translating programs
into ASTs. We present some sample ASTs in table 2.

    AST                                     finite state automaton (FSA)        Note
    start        root




                                                                      ¬σ
                                            start             ∅                 σ = FC (fs ), ω = FC (fe ), fs ∈ S, fe ∈
                                                                                E. “For loop” can be expressed by

                                                             ¬σ
                                                                  σ
                 while
                                                                                “while loop.”
                                                              ω



                                                                      σ
        fs               fe

    start        root
                                            start             ∅       ¬σ
                                                     T rue




                                                                                σ, ω = FC (fs ), FC (fe ), fs ∈ S, fe ∈ E.
                                                                  σ


                  if

        fs               fe                                   ω


    start         root                      start             ∅
                                                                                σ, ω1 , ω2 = FC (fs ), FC (fe1 ), FC (fe2 ).
                                                  e
                                                                  T ru
                                                                  ¬σ
                                                σ
                                             T ru




            if           else                                                   For “if-elif-else,” we duplicate the “if”
                                                                      e




                                                                                node and replace it with “elif.”
     fs fe1              fe2                   ω1                  ω2


    start        root                        start            ∅                 Running a set of functions sequen-
                                                    ue

                                                                  Tr




                                                                                tially without keywords. ωi = FC (fei )
                                               Tr


                                                                   ue




                                                                                for i ∈ [1, 2, 3]. We can extend it to
       fe2 fe1 fe3                           ω1     ω2    ω3
                                                                                any number of leaf nodes.
                                               T rue T rue
                           Table 2: Rules to convert abstract syntax trees to FSA-based representations.

An AST has a set of tree nodes and a set of direct transitions between the tree nodes. Each tree node
corresponds to a keyword or a function f ∈ S ∪ E. A tree node has at most one incoming transition and
a set of outgoing transitions connecting to a set of children tree nodes. Root is a tree node that does not
belong to the children of any node, and leaf is a tree node whose children are empty.

Keyword Processor The keyword processor is a function mapping an AST with predefined keywords and
specified structures to an FSA. It has a set of built-in rules for mapping an AST to an FSA, and we present
some sample rules in table 1. The keyword processor cannot handle AST structures beyond the domain of
built-in rules.

Tree to FSA So far, we have the AST for the program and the keyword processor, so we can run
algorithm 1 to construct an FSA representing the program. First, the algorithm initializes the states,
transitions, and labels of an FSA (lines 2-4). Next, it follows a preorder traversal to go through all the tree
nodes in the AST (line 9), and it uses the keyword processor to build sub-automata based on the keywords
(lines 7). Then, it merges the sub-automata and returns the merged automaton as the final output (lines
11-15).




                                                                           16
     B   Additional Experimental Details

     We present the programs generated by the language model for the task “bring my backpack back from the
     lounge” below.

1    def br ing_back pack () _1 :
2        start_loc = g e t _ c u r r e n t _ l o c a t i o n ()
3        go_to (" lounge ")
4        if is_in_room (" backpack ") :
5             while True :
6                  if is_in_room (" person ") :
7                       response = ask (" Could you put my backpack in the basket ?")
8                       if response == " Yes ":
9                            break
10                 time . sleep (1)
11       go_to ( start_loc )
1    def b r i n g _ b a c k p a c k _ 2 () :
2        start_loc = g e t _ c u r r e n t _ l o c a t i o n ()
3        go_to (" lounge ")
4        while True :
5                if is_in_room (" backpack ") and is_in_room (" person ") :
6                        response = ask (...)
7                        if response == " Yes ":
8                                go_to ( start_loc )
9                                return
10               if not is_in_room (" backpack ") :
11                       go_to ( start_loc )
12                       return
13               time . sleep (1)

     We record the average time for generating a program using each baseline models in table 3. The response
     (program generation) time for GPT-4o-mini and DeepSeek-R1-Qwen-7B is half of the two large models
     (GPT-4.1 and GPT-4o).

                     Model                GPT-4.1     GPT-4o     GPT-4o-mini   DeepSeek-R1-Qwen-7B
             Response Time (seconds)       11.7        12.1         7.4                 5.6

     Table 3: The average time for each model to generate a complete response (program). Note that we query
     the online models, hence the recorded time includes internet latency. Given that the internet latency is
     constant, the total response time of GPT-4o-mini and DeepSeek-R1-Qwen-7B is significantly shorter than
     that of the former two large models.




                                                          17
                               Go straight        Turn right 90 degrees   Go straight




                           Turn left 90 degrees       Go straight         Left U-turn



Figure 12: Execution of a composed program that consists of multiple sub-programs. Each sub-program
(e.g., go straight, turn left 90 degrees) is formally verified and satisfies the specifications.


C    Composed Program Execution

Consider we obtain a set of safety-constrained programs for the Jackal outdoor robot by repeating the steps
in Section 5.2. The programs include basic driving behaviors such as going straight to approach the stop
sign (left of Figure 1), turning left/right (bottom right of Figure 1), U-turn (top right of Figure 1), etc. We
compose them into a complex, long-horizon driving task:

                          “Always turn right at the stop sign and then go straight,
                            and make a U-turn if you reach the end of the road.”

In Section 4.2, we prove that the composed program from multiple safety-constrained programs also satisfies
the safety specifications. We empirically test the composed programs using the outdoor robot. It satisfies
the safety specifications during the entire execution.
Theorem 1 allows users or planners to guarantee the composed program satisfies the safety specifications
without additional verification to the overall composed program. As the state space of the composed program
can be large compared to each individual sub-program, avoiding verifying the overall program significantly
reduces the computational complexity.




                                                          18
