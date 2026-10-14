                                             Towards Logically Sound Natural Language Reasoning
                                                with Logic-Enhanced Language Model Agents
                                                                           Agnieszka Mensfelta , Kostas Stathisa and Vince Trencsenyia
                                                                             a Royal Holloway, University of London, Egham, Surrey, UK
                                                    ORCID (Agnieszka Mensfelt): https://orcid.org/0000-0002-2385-2017, ORCID (Kostas Stathis):
                                             https://orcid.org/0000-0002-9946-4037, ORCID (Vince Trencsenyi): https://orcid.org/0009-0009-4560-7571


                                         Abstract. Large language models (LLMs) are increasingly ex-                   tion optimality – whether models select payoff-maximizing strate-
                                         plored as general-purpose reasoners, particularly in agentic contexts.        gies [2, 11, 17, 24]. However, optimality alone may result from well-
                                         However, their outputs remain prone to mathematical and logical er-           represented game-theoretic examples in the training data, and thus
arXiv:2408.16081v2 [cs.AI] 29 May 2025




                                         rors. This is especially challenging in open-ended tasks, where un-           does not guarantee robustness when the model encounters novel or
                                         structured outputs lack explicit ground truth and may contain subtle          out-of-distribution scenarios.
                                         inconsistencies. To address this issue, we propose Logic-Enhanced                In this work, we shift the focus from action outcomes to reasoning
                                         Language Model Agents (LELMA), a framework that integrates                    processes. We introduce Logic-Enhanced Language Model Agents
                                         LLMs with formal logic to enable validation and refinement of nat-            (LELMA), a framework that integrates LLMs with formal logic to
                                         ural language reasoning. LELMA comprises three components: an                 validate and refine natural language reasoning. LELMA employs
                                         LLM-Reasoner, an LLM-Translator, and a Solver, and employs auto-              a modular architecture consisting of three components: an LLM-
                                         formalization to translate reasoning into logic representations, which        Reasoner, an LLM-Translator, and a formal Solver. Through a pro-
                                         are then used to assess logical validity. Using game-theoretic scenar-        cess of autoformalization [39, 18, 20, 40, 29, 8, 6, 12], the system
                                         ios such as the Prisoner’s Dilemma as testbeds, we highlight the limi-        translates natural language reasoning into formal logic queries, en-
                                         tations of both less capable (Gemini 1.0 Pro) and advanced (GPT-4o)           abling logical validity checks. Detected errors trigger feedback, al-
                                         models in generating logically sound reasoning. LELMA achieves                lowing the LLM to iteratively improve its reasoning through self-
                                         high accuracy in error detection and improves reasoning correctness           refinement.
                                         via self-refinement, particularly in GPT-4o. The study also highlights           Using classic game-theoretic scenarios such as the Prisoner’s
                                         challenges in autoformalization accuracy and in evaluation of inher-          Dilemma as evaluation tasks, we investigate reasoning quality in
                                         ently ambiguous open-ended reasoning tasks.                                   both advanced (GPT-4o) and less capable (Gemini 1.0 Pro) mod-
                                                                                                                       els. Our results show that LELMA effectively improves reasoning
                                                                                                                       correctness – particularly for GPT-4o. Still, challenges remain in
                                         1   Introduction                                                              translation accuracy and evaluation of open-ended, ambiguous rea-
                                                                                                                       soning. This highlights the need for more robust methods to ensure
                                         Large language models (LLMs) are capable of generating sophis-                that LLMs, when deployed as agents in interactive settings, reason
                                         ticated natural language explanations and decisions across a wide             logically soundly.
                                         range of tasks. Their ability to process and produce human-like text             This paper makes the following contributions:
                                         makes them attractive candidates for use in agentic AI systems,
                                         where autonomous agents interact with both humans and other agents
                                         through natural language communication. This vision includes sce-             (i) We introduce, a neurosymbolic framework that integrates LLM-
                                         narios ranging from collaborative multi-agent systems to negotiation,             generated reasoning with formal logic to validate and refine natu-
                                         coordination, and human-agent teaming [30, 10].                                   ral language outputs.
                                            However, despite their extensive capabilities, LLMs remain funda-         (ii) We conduct extensive experiments with GPT-4o and Gemini 1.0
                                         mentally unreliable reasoners. Their outputs often suffer from math-              Pro, showing improvements in reasoning correctness, especially
                                         ematical, logical, and factual errors, as well as hallucinations [19, 1].         for advanced models.
                                         Furthermore, although significant research effort has been devoted to       (iii) We identify key challenges, including limitations in autoformal-
                                         improving single-agent safety and alignment, ensuring that a model                ization and evaluation of open-ended reasoning.
                                         produces safe and accurate outputs in isolation does not automati-
                                         cally guarantee safe and reliable behavior in multi-agent settings [4].          The remainder of this paper is organized as follows. Section 2
                                            In this context, game theory [28] offers a particularly suit-              presents the preliminaries, covering large language models, game
                                         able testbed. As a formal model of strategic interaction, it allows           theory, and general game playing. Section 3 introduces the LELMA
                                         controlled evaluation of reasoning in multi-agent scenarios where             framework, followed by the detailed methodology in Section 4. Sec-
                                         choices must be justified based on payoffs, incentives, and antic-            tion 5 presents the experimental evaluation and key findings. We dis-
                                         ipated actions of others. Recent works have explored LLMs as                  cuss these results in depth in Section 6, and finally, Section 7 sum-
                                         agents in game-theoretic environments, primarily focusing on ac-              marizes the work and outlines directions for future research.
2     Preliminaries                                                             We experiment with symmetric non-cooperative games presented in
                                                                                normal form, usually a matrix showing the players, strategies, and
2.1     Large Language Models                                                   payoffs [31]. Table 2a demonstrates a general game matrix, where
The term Large Language Model typically refers to a model based on              the row player’s actions are denoted by U and D, and the column
the transformer architecture with billions of parameters. In this work,         player’s actions are marked by L and R. The four possible outcomes
GPT-4o and Gemini 1.0 Pro were used to compare a state-of-the-art               W,X,Y,Z denote the players’ payoff πi for the given action pairs as
(SOTA) model with a less capable counterpart.                                   the tuple (πrow , πcol ).
                                                                                  All games in our experiment can be mapped over the general game
GPT-4o OpenAI’s GPT-4o [27]—based on and successor of GPT-                      matrix. We classify actions U and L as “Defect” denoted by D and
4 [1]—a current SOTA LLM. Its multi-modal architecture supports                 actions D and R as “Cooperate” denoted by C. This allows us to use
text, image and audio inputs and outputs. It was pre-trained with               the well-known terminology from Axelrod’s tournaments to define
publicly accessible data and third-party resources, and fine-tuned              these games in terms of the four outcomes:
with human feedback. GPT-4o demonstrates enhanced performance
in reasoning tasks compared to its predecessor and is reported to have          T (Temptation to defect): (D, C)
increased factuality. However, GPT-4o still faces challenges with re-           R (Reward for mutual cooperation): (C, C)
liability due to hallucinations.                                                P (Punishment for mutual defection): (D, D)
 Gemini 1.0 Pro Gemini 1.0 Pro is Google’s previous largest                     S (Sucker’s payoff): (C, D)
model, with good general performance [32]. The Gemini model fam-
ily supports various forms of textual, visual and audio inputs and can             The Prisoner’s Dilemma (PD) is a classical concept in game the-
produce interleaved textual and visual outputs. Gemini models are               ory involving two players. Each player can decide to cooperate for
pre-trained on publicly available resources for each modality. They             mutual benefit or betray their partner (defect) for individual reward,
support external tool use and web search, increasing their perfor-              characterised by the matrix in Table 2b. The Stag Hunt (SH) is a
mance in reasoning tasks.                                                       coordination game, where the players have two options: be selfish
                                                                                and hunt Hare (D), or be cooperative and hunt Stag (C). The SH has
                                                                                a payoff structure that favours mutual cooperation the most, instead
2.2     Game Theory                                                             of the temptation to defect as in the PD—Table 2c. Our third game,
Game theory provides the mathematical tools to analyse the strate-              Hawk Dove (HD), involves the defective action Hawk, and coopera-
gic interaction between decision-makers [28]. Its applications range            tive action Dove. As demonstrated by the game matrix in Table 2d,
from analysing day-to-day social situations to complex political or             HD is described by having the temptation to defect as the most re-
economic problems.                                                              warding outcome, but the mutual defection yields the least amount
                                                                                of payoff.

2.2.1      Games in our experiments
                                                                                2.3    General game playing
Table 1.    General payoff matrix and specific payoff matrices for considered   General game playing ([15]) aims at creating intelligent systems
                                   games.                                       that understand the rules of arbitrary new games and learns to play
                                                                                them without human intervention. The Game Description Language
                                                                                (GDL) has been proposed as a formal, machine-processable language
                row/col             L                 R                         for describing the rules of arbitrary games ([25]). GDL focused on in-
                      U       (Wrow , Wcol )    (Xrow , Xcol )                  formation games only, so it was extended in GDL-II ([35]) to cover
                      D        (Yrow , Ycol )   (Zrow , Zcol )                  n-player games with incomplete information and games in extensive
              (a) A general game in matrix form.                                normal form ([36]). GDL-II is based on the standard syntax and se-
                                                                                mantics of logic programming and characterised by the special key-
                                                                                words shown in Table 2.
                    row/col       Defect (D)       Coop. (C)
                                                                                Table 2.   Subset of GDL-II (uppercase letters denote variables, lowercase
                 Defect (D)         (1, 1)          (5, 0)                                     letters denote predicates/function symbols)
                 Coop. (C)          (0, 5)          (3, 3)
              (b) Prisoner’s Dilemma: T > R > P > S.                             role(R)               R is a player
                                                                                 init(F)               F holds in the initial position
                                                                                 true(F)               F holds in the current position
                  row/col         Hare (D)         Stag (C)                      legal(R, M)           R can do move M in the current position
                                                                                 does(R, M)            player R does move M
                Hare (D)           (1, 1)           (3, 0)                       next(F)               F holds in the next position
                Stag (C)           (0, 3)           (5, 5)                       terminal              the current position is terminal
              (c) Stag Hunt: R > T > P > S.                                      goal(R, N)            R gets N points in the current position


                                                                                   A difficulty with GDL systems is that learning without human
                   row/col        Hawk (D)         Dove (C)
                                                                                guidance poses a reasoning challenge. Players must infer the pos-
                Hawk (D)            (0, 0)           (5, 1)                     sible actions of others, essentially evaluating hypothetical game situ-
                 Dove (C)           (1, 5)           (3, 3)
                                                                                ations before taking action. Action formalisms like the classical Sit-
              (d) Hawk-Dove: T > R > S > P .                                    uation Calculus [26] have been developed for precisely this purpose.
Formal schemes and inference methods are readily available for Sit-                Algorithm 1 LELMA reasoning loop
uation Calculus [16, 23], while their deployment in general game                   Input: Payoff matrix, instruction prompt
playing presupposes a translation from GDL into existing, suitably                 Output: Strategic reasoning
expressive action languages. One such scheme [34] shows how to                      1: attempts ← 0
fully embed GDL-II into a version of the Situation Calculus based                   2: while attempts < max_attempts do
                                                                                    3:     reasoning ← Reasoner(instruction)
on knowledge fluents [33]. Our game solver, presented later in sec-                 4:     queries ← Translator(reasoning)
tion 3.2, is inspired by these previous works, to support light GDL                 5:     if queries is ∅ then
specifications that can be readily combined with LLM APIs to vali-                  6:         return reasoning                     ▷ No queries found
date their reasoning.                                                               7:     else
                                                                                    8:         failed ← Solver(queries)
                                                                                    9:         if failed is ∅ then
                                                                                   10:              return reasoning                  ▷ All queries true
3        Logic-Enhanced Language Model Agents                                      11:          else
3.1          Framework Overview                                                    12:              instruction ← feedback(failed)
                                                                                   13:          end if
                                                                                   14:     end if
                                                                                   15:     attempts ← attempts +1           ▷ Reevaluate using feedback
Natural language      NEURAL COMPONENT                                             16: end while
     input:

    “Your task is                            Natural language                      17: return reasoning                         ▷ Max attempts reached
       to...”
                       LLM-Reasoner             reasoning         LLM-Translator


                                                                                   a specific game using the predicates of the game-independent part,
                          Natural language
                                                                                   and a set of auxiliary predicates built on top of these representations
                                                                    Queries: Q
                             feedback                                              to evaluate LLM reasoning for that specific game. We adhere to the
Natural language                   No
                                                                                   usual conventions for representing a game as an implementable logic
     output:                                                                       program: variables are denoted by uppercase letters and predicates
   “Let’s think     Yes        ∀ q∈Q         Logical value
 step-by-step...”               True              (Q)
                                                                     Solver        and function symbols by lowercase letters. An underscore (_) de-
                                 ?
                                                                                   notes a variable whose value is unused within a definition. The state
                                                           SYMBOLIC COMPONENT      of a game is represented by a situation, initially defined as a constant
                                             LELMA                                 (e.g., s0). The special binary function do(M, S) represents the sit-
                                                                                   uation resulting from the execution of move M in situation S, as in the
                                                                                   Situation Calculus. In the logical rules that follow, the symbols if,
 Figure 1. Overview of the LELMA framework. The relevant statements                and, and not correspond to their logical equivalents.
 generated by the Reasoner are translated into a set of queries Q, which are
evaluated by the Solver. If any of the queries fail, the Reasoner is prompted
 to refine its reasoning in light of the facts derived from the failed queries.    3.2.1   Game-independent part
                                                                                   We recursively specify as a logic program all legal transitions of an
  The Logic-Enhanced Language Model Agents (LELMA) frame-                          extended form game from an initial situation S to a final situation F
work is implemented in Python and Prolog [38]. Owing to the frame-                 as follows:
work’s modularity, the Prolog solver can be easily replaced with an-
                                                                                   game(F, F) if
other type of formal solver. The system (Fig. 1) comprises the fol-                    final(F).
lowing components:                                                                 game(S, F) if
                                                                                       not final(S) and
Reasoner: An LLM agent responsible for generating natural lan-                         legal(M, S) and
  guage reasoning.                                                                     game(do(M, S), F).
Translator: An LLM agent that maps statements from the Rea-                        The first two lines return the final game situation F, when it is
  soner’s output to logical queries sent to the Solver.                            reached. Otherwise, in a non-final situation S, the game accepts a
Solver: A standard logic program implemented in Prolog that eval-                  legal move M, and the game continues in the next do(M,S) situa-
  uates the queries.                                                               tion, until the final situation F is reached. To reason about what holds
Feedback loop: A mechanism for providing natural language feed-                    in individual legal situations, we use Situation Calculus represented
  back to the Reasoner when a query evaluation fails.                              as:
 The source code of the framework and the results of the experi-                   holds(F, S) if
                                                                                       initially(F, S).
mental evaluation are publicly available.1                                         holds(F, do(M, S)) if
                                                                                       effect(F, M, S).
                                                                                   holds(F, do(M, S)) if
3.2          Solver                                                                    holds(F, S) and
                                                                                       not abnormal(F, M, S).
We specify the solver module as a logic program implemented in
Prolog ([22], [38]), a declarative programming language well-suited                   A fluent F holds in the initial situation, a new fluent F is initiated
for high-level problem definitions. Logic programs enhance the reli-               by the effects of a move M executed in a situation S, and a fluent F
ability of stochastic LLM outputs by providing a robust framework                  persists after a move is made, provided it is not abnormal; abnormal
for logical rule-based reasoning. Our solver consists of three main                fluents are terminated (do not persist). We also use rules of the form:
components: a game-independent part representing the rules of any                  finally(F, S) if Conditions.
game in normal form, a game-dependent part defining the rules of
                                                                                   to return derived fluents F describing the result of the game, when
1 https://github.com/dicelab-rhul/LELMA
                                                                                   the Conditions hold in the final situation S.
3.2.2   Game-dependent part                                                finally(outcome(P1,M1,U1,P2,M2,U2), S) if
                                                                               final(S) and
To represent a specific game we need to define game-dependent pred-            holds(role(P1, row), S) and
icates for the initial state initial/1, the legal moves legal/2,               holds(did(P1, M1), S) and
                                                                               holds(role(P2, col), S) and
what holds in the initial game situation via initially/2, the ef-              holds(did(P2, M2), S) and
fects of a move on a situation via effect/3, what stops persisting             payoff(M1, M2, U1, U2).
in a situation after the execution of a move via abnormal/3, the fi-
                                                                           We can then extract specific outcome information, e.g. the player’s
nal situation final/1, and the result of the game via finally/2
                                                                           utility, through a goal/2 fluent (as in GDL) e.g.:
definitions. To exemplify these definitions, we show how to describe
a PD game to our solver. The initial situation s0 is defined as:           finally(goal(P1, U1), S) if
                                                                               finally(outcome(P1, _, U1, _, _, _), S).
initial(s0).                                                               finally(goal(P2, U2), S) if
                                                                               finally(outcome(_, _, _, P2, _, U2), S).
What holds in this initial situation we specify it as:
                                                                           This completes the definition of a PD game, and allows us to use the
initially(player(p1), s0).
initially(player(p2), s0).                                                 above game description to reason about the game. If, in the speci-
initially(role(p1,row), s0).                                               fications above, we substitute the symbol if with ‘:-’, the sym-
initially(role(p2,col), s0).                                               bol and with ‘,’, and the symbol not with ‘\+’ (representing
initially(control(p1), s0).                                                negation by failure), we obtain an executable Prolog program that a
initially(control(p2), s0).
                                                                           player can query to perform reasoning within the game. For exam-
These assertions define first the player names represented by unique       ple, if player p1 wanted to reason about the game and determine the
identifiers (p1 and p2), their roles (p1 is the row player, while p2 is    actions needed to achieve a utility of 5, they could express this as the
the column player), and then the fact that initially either of them can    query shown below (queries are initiated with the symbol ‘?-’):
the game next (via the control/1 fluent,as in GDL). What holds                ?- game(s0,F), finally(goal(p1,5),F).
in the initial situation changes as a result of move being made in the        based on the game’s payoff matrix, our solver provides the follow-
game. We represent moves as terms of the form choice(P, M),                ing answers for F:
where P is a player, and M is a move. As it is possible for any player        1 do(choice(p2,’C’),do(choice(p1,’D’),s0));
in a Prisoner’s Dilemma game to choose defect (’D’) or cooperate           2 do(choice(p1,’D’),do(choice(p2,’C’),s0)); 3
(’C’), we write this as:                                                   false.
possible(choice(P, ’D’), S) if                                                In the first answer, p1 acted first and p2 second, while in the sec-
    holds(player(P), S).                                                   ond answer, the order is reversed. This is not unexpected, as in our
possible(choice(P, ’C’), S) if                                             game definition both players have control initially, so the answers
    holds(player(P), S).
                                                                           show both combinations.
It is then legal for a player to choose a possible move if they have the
control to execute it in the current situation:                            3.3    Translator
legal(choice(P, M), S) if
    possible(choice(P, M), S) and                                          Table 3. A set of queries corresponding to natural language statements and
    holds(control(P), S).                                                    their explanation, as provided to the Translator. For each predicate that
                                                                             determines the higher/highest payoff of a given type, except for ∗ , there
When a legal move M is made by a player P, the effect that this move          exists a corresponding predicate determining the lower/lowest payoff.
is actually made is recorded in the next situation:
effect(did(P, M), choice(P, M), S).                                         finally(outcome(you,B,1,them,R,$ _),S)
                                                                            ‘you’ corresponds to the reasoner, ‘them’ to their opponent, 10 to payoff,
Once a legal move is executed, the player loses control, which we           and ‘B’, ‘R’ to choices assumed to give this payoff to the reasoner
specify in our framework as:                                                higher(1, 3)
abnormal(control(P), choice(P, M), S).                                      1 and 3 correspond to numerical payoffs, 1 is assumed to be higher than 3
                                                                            highest_possible_individual_payoff(1)
In other words, after a choice is made by a player, the player loses        1 corresponds to the assumed highest possible payoff for the reasoner
control and therefore cannot play a move again from that situation          highest_individual_payoff_for_choice(1,B)
onwards.                                                                    1 corresponds to the assumed highest individual payoff for a given choice,
   Moves made in this way bring about the final situation, which we         e.g. ‘B’
specify as a situation term with two choices made from the initial          highest_guaranteed_payoff_choice(B)∗
situation, one for each player.                                             ‘B’ corresponds to the choice assumed to give the highest guaranteed
                                                                            (worst-case) individual payoff
final(S) if                                                                 higher_guaranteed_payoff(B,R)
    ground(S) and
                                                                            ‘B’ and ‘R’ correspond to choices, and ‘B’ is assumed to give the higher
    S = do(choice(_, _), do(choice(_, _), I)) and
                                                                            guaranteed payoff
    initial(I).
                                                                            highest_mutual_payoff(R,R)
Assuming the payoff matrix of Table 2b defined as:                          ‘R’ and ‘R’ correspond to choices, assumed to give the highest mutual
                                                                            payoff
payoff(’D’, ’D’, 1, 1).
payoff(’C’, ’D’, 0, 5).
payoff(’D’, ’C’, 5, 0).                                                       The Solver is extended with predicates derived from a preliminary
payoff(’C’, ’C’, 3, 3).
                                                                           analysis of common LLM reasoning errors in the evaluation task.
the outcome of the game holds information about the actual moves           Translation employs one-shot learning, using a prompt that lists pred-
made by the players, and their payoffs.                                    icates with sample arguments and their natural language descriptions
(Table 3). For failed predicates, the Solver identifies correct variable   4.2     Settings
values; the queries are then translated back into natural language and
incorporated into feedback for the Reasoner. Queries that are syntac-      In the experiments, we used two LLMs as LLM-Reasoner agents:
tically invalid or do not match expected forms are discarded. Con-         GPT-4o and Gemini 1.0 Pro. In both setups, GPT-4o was used as
stants outside the allowable set are replaced with variables.              the LLM-Translator. The experimental parameters are summarized
                                                                           in Table 4.
3.4    Feedback loop
The feedback loop logic is shown in Listing 1. The max attempts            4.3     Correctness criteria and evaluation
parameter limits the number of reasoning iterations. If all attempts
fail (i.e., each contains some failed queries), the final attempt is re-   In evaluating correctness, we assume that both actions in the con-
turned as the most refined. The feedback prompt is dynamically pop-        sidered games are valid and can be justified by factors such as
ulated with natural language corrections for each failed query. For        risk aversion or cooperativeness (e.g., a cooperatively minded agent
example, if the original reasoning includes “I choose B because it         may choose “Cooperate” even if it does not yield the highest util-
gives me payoff 3 which is higher than 5,” the corresponding query         ity). A reasoning sample is marked as incorrect only if it con-
higher(3, 5). fails and is translated as “payoff 3 is lower than           tains logical or mathematical errors related to payoff assignment
payoff 5.” The prompt instructs the agent to reconsider its reasoning      or inference—errors that human participants typically do not make
in light of these corrections, but also allows reaffirming the original    (e.g., “payoff 3 is higher than payoff 5”). Misuse of game-theoretic
reasoning. This accounts for possible false positives—that is, queries     terminology (e.g., incorrect application of Nash equilibrium) does
that were incorrectly translated. While the Solver guarantees the cor-     not count against correctness. Accordingly, the evaluation focuses
rectness of the generated feedback, some feedback—–such as that            strictly on the logical accuracy of reasoning about payoffs, indepen-
suggesting a particular choice yields a higher guaranteed payof—           dent of theoretical knowledge.
may potentially bias the agent’s reasoning toward that option.                To assess the framework’s accuracy in detecting such errors, we
                                                                           conducted a manual evaluation of all reasoning samples generated in
                                                                           the experiments. To ensure objectivity and reproducibility, we devel-
4     Methods                                                              oped an evaluation protocol and accompanying scoring sheet (avail-
4.1    Task                                                                able in the repository). Three independent evaluators reviewed each
                                                                           sample to reduce the impact of individual oversight. Due to the task’s
To evaluate the effectiveness of the LELMA framework in detecting          cognitive demands, some errors may have been missed, and false
and correcting natural language reasoning errors, we conducted ex-         negatives (missed errors) are more likely than false positives. Thus,
periments using the games introduced in Section 2.2. The rules and         we adopted a conservative aggregation method, labeling a sample as
payoff structures of each game were presented in a natural language        correct only if all evaluators agreed on its correctness.
instruction prompt, following the style commonly used in human-               Additionally, to assess the utility of the LLM-as-a-judge [41] ap-
subject game-theoretic studies. The expected output was an action          proach, we evaluated the same reasoning samples using two LLMs:
choice accompanied by natural language reasoning, consistent with          GPT-4o (gpt-4o-2024-08-06 version) and Claude 3.7 Son-
the Chain-of-Thought [37] approach. Correctness was defined as the         net [3], a state-of-the-art model not involved in generation. Each
absence of logical errors in the reasoning about payoffs.                  model was given a simplified version of the evaluation protocol used
   To evaluate both the robustness of the approach and the baseline        by human judges. Their ratings were then compared against human
performance of LLMs, we deliberately obfuscated the task—that is,          evaluations.
we modified its presentation to differ from formats likely present in
the training data. Prior work has shown that LLM performance can
degrade when familiar tasks are presented in unfamiliar ways [21].         5     Results
In our setup, the standard game-theoretic action labels were replaced
with abstract symbols ‘B’ and ‘R’. Furthermore, preliminary experi-        5.1     Experiments
ments indicated improved performance from GPT-4o when the pay-
off matrix followed a specific layout—particularly when the Cooper-        5.1.1    Attempts distribution
ate/Cooperate outcome appeared in the top-left corner. Consequently,
we inverted the matrix order in the experimental instructions.
                                                                               Table 5.   Distribution of reasoning for GPT-4o and Gemini 1.0 Pro.
        Table 4. Experimental parameters. ∗ gpt-4o-2024-05-13.
                                                                                          Attempts           1     2      3    4    5
                                             Hawk-Dove
      Games                                  Prisoner’s Dilemma                           GPT-4o             24    46    10    6     4
                                                                                          Gemini 1.0 Pro     26    20    11    9    24
                                             Stag Hunt
                                             GPT-4o∗
      LLM-Reasoner Agents                                                     Table 5 presents the distribution of reasoning attempts for GPT-
                                             Gemini 1.0 Pro
      Temperature                            1                             4o and Gemini 1.0 Pro. For GPT-4o, 78% of samples required only
                                                                           one or two attempts, with the maximum number of attempts (five)
      Maximum output tokens                  1024
                                                                           reached in just four cases. In all four instances, the final attempt was
      Maximum attempts number                5                             correct. In contrast, Gemini 1.0 Pro performed worse: 27% of its
      Repetitions                            30                            samples reached the five-attempt limit, and in 83% of those cases,
                                                                           the final attempt remained incorrect.
   Table 6.    Choice ‘B’ distribution for initial and final reasoning (%).     Table 8. Confusion matrices for initial reasoning for Gemini 1.0 Pro.
                                                                                Rows: actual correctness, columns: predicted correctness, 1: correct, 0:
                          GPT-4o                  Gemini 1.0 Pro                                       incorrect, A: accuracy.

        Game     Initial (%)    Final (%)     Initial (%)    Final (%)           Total (A=86%)          HD (A=81%)             PD (A=86%)               SH (A=90%)
        HD         100.00        100.00          66.67         70.00                    1   0               1   0                  1   0                    1   0
        PD          96.67         23.33          36.67         30.00                1    15    2         1     8     6         1      4      3             1       3    2
        SH         100.00         33.33          80.00         60.00                0    11   62         0     0     17        0      1     21             0       1   24

                                                                              Table 9. Confusion matrices for initial reasoning of GPT-4o. Rows: actual
Table 7. Percentage of correct reasoning samples in the original and final
                                                                                correctness, columns: predicted correctness, 1: correct, 0: incorrect, A:
                                attempt.
                                                                                                              accuracy.

                          GPT-4o                  Gemini 1.0 Pro                 Total (A=84%)          HD (A=73%)             PD (A=93%)                SH (A=87%)
        Game     Initial (%)    Final (%)     Initial (%)    Final (%)                  1   0               1   0                  1   0                     1   0

        HD          46.67          73.33        25.81         35.48                 1    15   5         1      12     6         1     0      1              1      3   2
        PD           3.33          70.00        17.24         34.48                 0     9   61        0       2     10        0     1     28              0      2   23
        SH          16.67          90.00        13.33         40.00
                                                                              5.2       Evaluation
5.1.2    Choices distribution                                                 5.2.1      Confusion matrices and accuracy
                                                                              Confusion matrices were computed by comparing manual evalua-
                                                                              tions (representing ground-truth correctness) with the presence or
Table 6 shows the frequency of choosing action ‘B’ in both the initial        absence of failed predicates (representing predicted correctness). Ta-
and final reasoning attempts for GPT-4o and Gemini 1.0 Pro. When              bles 8 and 9 show the confusion matrices for the initial reasoning
no feedback was provided, the initial choice remained unchanged.              attempts of both LLMs. Overall, error recognition was high, with ac-
The action ‘B’ corresponds to ‘Dove’ in Hawk-Dove, ‘Cooperate’ in             curacy rates of 84% for GPT-4o and 86% for Gemini 1.0 Pro. The
the Prisoner’s Dilemma, and ‘Stag’ in Stag Hunt.                              lowest detection accuracy was observed in the Hawk-Dove game—
   Overall, risk-averse choices became more frequent in final at-             73% for GPT-4o and 81% for Gemini 1.0 Pro. Among the detection
tempts. The Hawk-Dove game showed the highest consistency, with               errors, false positives were more common than false negatives.
‘Dove’ being the dominant action for both models: GPT-4o selected                False positives undermine trustworthiness, as they indicate correct
it in 100% of initial and final attempts, while Gemini 1.0 Pro in-            reasoning being incorrectly flagged as erroneous. In contrast, false
creased from 66.67% initially to 70% in the final attempt. This re-           negatives primarily increase computational cost without compromis-
flects a preference for avoiding the worst possible payoff (0), even at       ing correctness. Since the feedback generated by the solver is always
the expense of forgoing the highest payoff.                                   factually accurate, false negatives are unlikely to cause an agent to
   In contrast, the Prisoner’s Dilemma exhibited the most pronounced          revise correct reasoning into incorrect reasoning.
shift. For GPT-4o, the frequency of choosing ‘Cooperate’ dropped
from 96.67% to 23.33% after feedback, indicating that initial coop-
erative choices were often based on incorrect reasoning. In the Stag          5.2.2      Inter-rater agreement
Hunt, feedback similarly led to reduced selection of the less risk-
averse ‘Stag’: for GPT-4o, from 100% to 33%, and for Gemini 1.0
Pro, from 80% to 60%.                                                                              Pairwise Cohen's Kappa GPT-4o
                                                                                                                                                 1.0
                                                                                              Rater 1    0.39 0.34 0.10 0.30
                                                                                                                                                 0.8
                                                                                                                                                   Cohen's Kappa




5.1.3    Correctness                                                                          Rater 2               0.28 0.11 0.46               0.6

                                                                                              Rater 3                      -0.00 0.24            0.4
Table 7 presents the percentage of correct reasoning samples in the
                                                                                                                                                 0.2
initial and final attempts for both models. Initially, both LLMs ex-                           GPT4                                  0.08
hibited low correctness: GPT-4o achieved an average of 22.22%,                                                                                   0.0
while Gemini 1.0 Pro achieved 18.79%. After receiving corrective
                                                                                                        r2

                                                                                                               r3

                                                                                                                          T4

                                                                                                                                   e
                                                                                                                                ud
                                                                                                                      GP
                                                                                                      te

                                                                                                                te



                                                                                                                               Cla
                                                                                                   Ra

                                                                                                             Ra




feedback, GPT-4o demonstrated significant improvement, reaching
an average correctness of 77.78%, whereas Gemini 1.0 Pro showed
lower gain, reaching 36.65%.                                                              Figure 2. Pairwise inter-rater agreement for GPT-4o.
   A detailed analysis of the reasoning samples revealed that GPT-4o
was often able to incorporate feedback effectively, correcting prior             To assess inter-rater agreement among the three human evaluators,
errors—sometimes resulting in a change of action. This effect was             Fleiss’ Kappa [13] was computed. For GPT-4o, the Kappa value was
particularly notable in the Prisoner’s Dilemma and Stag Hunt scenar-          κ = 0.31, indicating fair agreement, while for Gemini 1.0 Pro, it was
ios (see Table 6). In contrast, Gemini 1.0 Pro’s reasoning frequently         κ = 0.59, indicating moderate agreement. These results underscore
reiterated previous justifications, either repeating the same errors or       the inherent challenges of the evaluation task. The higher agreement
introducing new ones. This pattern is consistent with the number of           for Gemini 1.0 Pro likely reflects the presence of more apparent and
required attempts reported in Table 5.                                        easier-to-detect errors compared to those found in GPT-4o.
                                                                          LLM Performance in Social Dilemmas LLMs have attracted in-
                Pairwise Cohen's Kappa Gemini 1.0 Pro                     creasing interest as potential agents in game-theoretic contexts [2,
                                                        1.0
                                                                          11, 17, 24]. This study evaluated the correctness of strategic rea-
               Rater 1    0.61 0.63 0.02 0.50                             soning produced by GPT-4o and Gemini 1.0 Pro across three one-
                                                        0.8
                                                                          shot games. Initial correctness, prior to any feedback, was generally




                                                          Cohen's Kappa
               Rater 2            0.54 -0.00 0.44       0.6               low, ranging from 3.33% to 46.67%. These results highlight the lim-
                                                                          itations of existing automated benchmarks (e.g., [9]), which tend to
               Rater 3                 0.08 0.62        0.4
                                                                          emphasize outcome optimality rather than the validity of reasoning.
                                                        0.2               Furthermore, the findings underscore the challenges of employing
                 GPT4                            0.13                     LLMs as agents in social simulations.
                                                        0.0                  Despite the high overall accuracy in detecting incorrect reason-
                         r2

                                r3

                                      T4

                                               e
                                                                          ing, the process was not entirely error-free. Detection performance
                                            ud
                                      GP
                      te

                                 te



                                           Cla
                   Ra

                              Ra




                                                                          depended on the accuracy of translating natural language into for-
                                                                          mal predicates, a task handled by a separate LLM instance. Although
        Figure 3. Pairwise inter-rater agreement for Gemini 1.0 Pro.      translating atomic statements into formal representations is generally
                                                                          simpler than generating coherent reasoning, it remains a nontrivial
   To explore LLM-as-a-judge as a scalable alternative to human
                                                                          challenge with room for improvement. One potential avenue for en-
evaluation, we measured agreement using Cohen’s Kappa [7] be-
                                                                          hancing translation — and thus improving error detection — is to
tween each LLM and the aggregated human judgment, as well as
                                                                          fine-tune the LLM responsible for the translation task.
pairwise agreement among all raters (human and LLMs). Figures 2
and 3 display the pairwise Cohen’s Kappa values for reasoning gen-        LELMA Evaluation The moderate and fair inter-rater agreement
erated by Gemini 1.0 Pro and GPT-4o, respectively.                        values indicate that this evaluation task is challenging even for hu-
   GPT-4o, when acting as a judge, showed low agreement with              man judges. The lower agreement observed for the more advanced
both human raters and Claude 3.7 Sonnet. In contrast, Claude              model suggests that in open-ended tasks such as this, more sophis-
3.7 Sonnet exhibited substantially higher agreement with human            ticated outputs demand greater cognitive effort to assess, making er-
raters—comparable to inter-human agreement.                               rors harder to detect. Although manual evaluation remains essential
   For reasoning generated by Gemini 1.0 Pro, the agreement be-           at this stage, it is not a scalable solution. Potential alternatives include
tween GPT-4o as a judge and the aggregated human judgment was             automated and semi-automated methods, such as LLM-derived met-
low, with Cohen’s Kappa κ = 0.044. In contrast, Claude 3.7 Sonnet         rics, prompting LLMs, human-LLM collaborative evaluation, and
showed substantially higher agreement with the aggregated human           fine-tuning approaches [14].
ratings, achieving κ = 0.555. For reasoning generated by GPT-4o,             We assessed the LLM-as-a-judge approach using an adapted ver-
the agreement between GPT-4o as a judge and the aggregated human          sion of our evaluation protocol. Among the two tested models,
judgment was similarly low, with κ = 0.159. Claude 3.7 Sonnet             Claude 3.7 Sonnet achieved inter-rater agreement levels compara-
again showed better alignment, with κ = 0.301.                            ble to those between human judges. However, in the more challeng-
                                                                          ing case of reasoning generated by GPT-4o, the agreement between
5.2.3     Computational cost                                              Claude and aggregated human evaluations was low, indicating fre-
                                                                          quent omission of errors. Thus, it cannot yet be considered a reliable
In experiments with GPT-4o, an average of 1269.77 tokens were used        alternative to human judgment in this context. Among the remaining
per attempt in the instruction prompt, and the model generated an av-     options, fine-tuning appears particularly promising, provided that a
erage of 1224.38 tokens in response. The average duration of a single     sufficiently large and representative training dataset can be gathered.
reasoning attempt was 16.53 seconds for GPT-4o and 34.66 seconds
for Gemini 1.0 Pro. The total runtime for all experiments was ap-         Limitations This study has several limitations. First, the need for
proximately 53 minutes for GPT-4o and 173 minutes for Gemini.             manual assessment of reasoning correctness constrained the size of
                                                                          the evaluation sample. Second, the accuracy of translating natural
6   Discussion                                                            language into formal representations directly impacts the effective-
                                                                          ness of reasoning error detection. Imperfect translation may lead
LELMA Accuracy The framework achieved 84% accuracy in de-                 to false negatives, which undermine trustworthiness, and false posi-
tecting reasoning correctness for GPT-4o and 86% for Gemini 1.0           tives, which increase computational cost and may inadvertently bias
Pro. Although error detection accuracy was high for both models,          the model toward specific choices. Therefore, further improvement
the improvement resulting from corrective feedback was consider-          in translation accuracy is needed.
ably greater for GPT-4o (ranging from 27 to 73 percentage points)
compared to Gemini 1.0 Pro (10 to 27 percentage points). Notably,
after receiving validation-based feedback, GPT-4o’s cooperation rate      7    Conclusions and Future Work
in the Prisoner’s Dilemma (PD) aligned more closely with rates ob-
served in human participant experiments [5]. GPT-4o more effec-           This work introduces LELMA, a framework for validating the logi-
tively incorporated feedback to refine its reasoning. By contrast,        cal soundness of natural language reasoning generated by large lan-
while Gemini 1.0 Pro was often less successful at correcting errors, it   guage models. The initial evaluation of GPT-4o and Gemini 1.0 Pro
occasionally produced errors related to incorrect calculations of ex-     in game-theoretic scenarios revealed frequent reasoning errors, par-
pected payoffs—issues not covered by the existing set of predicates.      ticularly in payoff attribution and comparison. Experimental results
This suggests that predicate design should be preceded by systematic      demonstrated that reasoning correctness improved for both mod-
error sampling to ensure adequate coverage of model-specific error        els—especially for GPT-4o—when integrated within the LELMA
types.                                                                    framework. The evaluation also highlighted the need to improve
translation accuracy and underscored the challenges of assessing am-             [20] A. Q. Jiang, S. Welleck, J. P. Zhou, W. Li, J. Liu, M. Jamnik, T. Lacroix,
biguous, open-ended tasks.                                                            Y. Wu, and G. Lample. Draft, sketch, and prove: Guiding formal the-
                                                                                      orem provers with informal proofs. arXiv preprint arXiv:2210.12283,
   Future work will focus on enhancing the accuracy of natural lan-                   2022.
guage to query translation, potentially through fine-tuning. We also             [21] S. Kambhampati, K. Valmeekam, L. Guan, M. Verma, K. Stechly,
plan to validate the framework across a wider range of language mod-                  S. Bhambri, L. Saldyt, and A. Murthy. Llms can’t plan, but can help
                                                                                      planning in llm-modulo frameworks. arXiv preprint arXiv:2402.01817,
els. Given LELMA’s modular design, which enables the flexible sub-
                                                                                      2024.
stitution of LLM agents, query sets, and solvers, we aim to extend its           [22] P. Körner, M. Leuschel, J. Barbosa, V. S. Costa, V. Dahl, M. V.
application to additional domains beyond game theory.                                 Hermenegildo, J. F. Morales, J. Wielemaker, D. Diaz, S. Abreu, and
                                                                                      G. Ciatto. Fifty Years of Prolog and Beyond. Theory and Prac-
                                                                                      tice of Logic Programming, 22(6):776–858, 2022. doi: 10.1017/
Acknowledgements                                                                      S1471068422000102.
                                                                                 [23] Y. Lesperance, G. De Giacomo, M. Rostamigiv, and S. M. Khan. Ab-
This work was supported by a Leverhulme Trust International Pro-                      straction of situation calculus concurrent game structures. Proceedings
fessorship Grant (LIP-2022-001). We also thank Heartwin Haveluck                      of the AAAI Conference on Artificial Intelligence, 38(9):10624–10634,
                                                                                      Mar. 2024. doi: 10.1609/aaai.v38i9.28933. URL https://ojs.aaai.org/
for his assistance in the evaluation.                                                 index.php/AAAI/article/view/28933.
                                                                                 [24] N. Lorè and B. Heydari. Strategic behavior of large language
                                                                                      models: Game structure vs. contextual framing.             arXiv preprint
References                                                                            arXiv:2309.05898, 2023.
 [1] J. Achiam, S. Adler, S. Agarwal, et al. Gpt-4 technical report. arXiv       [25] N. Love, T. Hinrichs, D. Haley, E. Schkufza, and M. Genesereth. Gen-
     preprint arXiv:2303.08774, 2023.                                                 eral Game Playing: Game Description Language Specification. Techni-
 [2] E. Akata, L. Schulz, J. Coda-Forno, et al. Playing repeated games with           cal Report LG–2006–01, Stanford University, 2006.
     large language models. arXiv preprint arXiv:2305.16867, 2023.               [26] J. McCarthy and P. Hayes. Some philosophical problems from the
 [3] Anthropic. Claude 3.7 sonnet. https://www.anthropic.com/claude,                  standpoint of artificial intelligence. In B. L. Webber and N. J. Nils-
     2025. Large language model.                                                      son, editors, Readings in Artificial Intelligence, pages 431–450. Morgan
 [4] U. Anwar, A. Saparov, J. Rando, D. Paleka, M. Turpin, P. Hase, E. S.             Kaufmann, 1981.
     Lubana, E. Jenner, S. Casper, O. Sourbut, et al. Foundational chal-         [27] OpenAI. GPT-4o. https://openai.com/index/hello-gpt-4o/, 2024. URL
     lenges in assuring alignment and safety of large language models. arXiv          https://openai.com/index/hello-gpt-4o/. Accessed: 25/07/2024.
     preprint arXiv:2404.09932, 2024.                                            [28] M. Osborne. Introduction to Game Theory. Oxford University Press
 [5] P. D. Bó. Cooperation under the shadow of the future: experimental               USA, 2004.
     evidence from infinitely repeated games. American economic review,          [29] L. Pan, A. Albalak, X. Wang, and W. Wang. Logic-lm: Empowering
     95(5):1591–1604, 2005.                                                           large language models with symbolic solvers for faithful logical rea-
 [6] Y. Chen, R. Gandhi, Y. Zhang, and C. Fan. Nl2tl: Transforming natural            soning. In Findings of the Association for Computational Linguistics:
     languages to temporal logics using large language models. In Proceed-            EMNLP 2023, pages 3806–3824, 2023.
     ings of the 2023 Conference on Empirical Methods in Natural Language        [30] J. S. Park, J. O’Brien, C. J. Cai, M. R. Morris, P. Liang, and M. S.
     Processing, pages 15880–15903, 2023.                                             Bernstein. Generative agents: Interactive simulacra of human behavior.
 [7] J. Cohen. A coefficient of agreement for nominal scales. Educational             In Proceedings of the 36th annual acm symposium on user interface
     and psychological measurement, 20(1):37–46, 1960.                                software and technology, pages 1–22, 2023.
 [8] M. Cosler, C. Hahn, D. Mendoza, F. Schmitt, and C. Trippel. nl2spec:        [31] E. Rasmusen. Games and information an introduction to game theory.
     interactively translating unstructured natural language to temporal log-         Blackwell, 2006.
     ics with large language models. In International Conference on Com-         [32] J.-B. A. Rohan Anil, Sebastian Borgeaud et al. Gemini: A family of
     puter Aided Verification, pages 383–396. Springer, 2023.                         highly capable multimodal models. arXiv preprint arXiv:2312.11805,
 [9] J. Duan, R. Zhang, J. Diffenderfer, B. Kailkhura, L. Sun, E. Stengel-            2024.
     Eskin, M. Bansal, T. Chen, and K. Xu. Gtbench: Uncovering the strate-       [33] R. B. Scherl and H. J. Levesque.                Knowledge, action, and
     gic reasoning limitations of llms via game-theoretic evaluations. arXiv          the frame problem.         Artif. Intell., 144(1-2):1–39, 2003.       doi:
     preprint arXiv:2402.12348, 2024.                                                 10.1016/S0004-3702(02)00365-X.              URL https://doi.org/10.1016/
[10] Z. Durante, Q. Huang, N. Wake, R. Gong, J. S. Park, B. Sarkar, R. Taori,         S0004-3702(02)00365-X.
     Y. Noda, D. Terzopoulos, Y. Choi, et al. Agent ai: Surveying the hori-      [34] S. Schiffel and M. Thielscher. Reasoning about general games de-
     zons of multimodal interaction. arXiv preprint arXiv:2401.03568, 2024.           scribed in gdl-ii. Proceedings of the AAAI Conference on Artificial
[11] C. Fan, J. Chen, Y. Jin, and H. He. Can large language models serve              Intelligence, 25(1):846–851, Aug. 2011. doi: 10.1609/aaai.v25i1.7944.
     as rational players in game theory? a systematic analysis. In Proceed-      [35] M. Thielscher. A general game description language for incomplete
     ings of the AAAI Conference on Artificial Intelligence, volume 38, pages         information games. In Proceedings of the Twenty-Fourth AAAI Confer-
     17960–17967, 2024.                                                               ence on Artificial Intelligence, AAAI’10, page 994–999. AAAI Press,
[12] J. Feng, R. Xu, J. Hao, H. Sharma, Y. Shen, D. Zhao, and W. Chen. Lan-           2010.
     guage models can be logical solvers. arXiv preprint arXiv:2311.06158,       [36] M. Thielscher. The general game playing description language is uni-
     2023.                                                                            versal. In T. Walsh, editor, IJCAI 2011, Proceedings of the 22nd Inter-
[13] J. L. Fleiss. Measuring nominal scale agreement among many raters.               national Joint Conference on Artificial Intelligence, Barcelona, Catalo-
     Psychological bulletin, 76(5):378, 1971.                                         nia, Spain, July 16-22, 2011, pages 1107–1112. IJCAI/AAAI, 2011.
[14] M. Gao, X. Hu, J. Ruan, X. Pu, and X. Wan. LLM-based nlg evaluation:        [37] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le,
     Current status and challenges. arXiv preprint arXiv:2402.01383, 2024.            D. Zhou, et al. Chain-of-thought prompting elicits reasoning in large
[15] M. R. Genesereth, N. Love, and B. Pell. General game playing:                    language models. Advances in neural information processing systems,
     Overview of the AAAI competition. AI Mag., 26(2):62–72, 2005.                    35:24824–24837, 2022.
[16] G. D. Giacomo, Y. Lespérance, and A. R. Pearce. Situation calculus          [38] J. Wielemaker, T. Schrijvers, M. Triska, and T. Lager. Swi-prolog. The-
     based programs for representing and reasoning about game structures.             ory and Practice of Logic Programming, 12(1-2):67–96, 2012.
     In F. Lin, U. Sattler, and M. Truszczynski, editors, Principles of Knowl-   [39] Y. Wu, A. Q. Jiang, W. Li, M. Rabe, C. Staats, M. Jamnik, and
     edge Representation and Reasoning: Proceedings of the Twelfth Inter-             C. Szegedy. Autoformalization with large language models. Advances
     national Conference, KR 2010, Toronto, Ontario, Canada, May 9-13,                in Neural Information Processing Systems, 35:32353–32368, 2022.
     2010. AAAI Press, 2010.                                                     [40] Z. Yang, A. Ishay, and J. Lee. Coupling large language models with
[17] F. Guo. GPT agents in game theory experiments. arXiv preprint                    logic programming for robust and general reasoning from text. arXiv
     arXiv:2305.05516, 2023.                                                          preprint arXiv:2307.07696, 2023.
[18] J. He-Yueya, G. Poesia, R. E. Wang, and N. D. Goodman. Solving math         [41] L. Zheng, W.-L. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin,
     word problems by combining language models with symbolic solvers.                Z. Li, D. Li, E. Xing, et al. Judging llm-as-a-judge with mt-bench and
     arXiv preprint arXiv:2304.09102, 2023.                                           chatbot arena. Advances in Neural Information Processing Systems, 36:
[19] S. Imani, L. Du, and H. Shrivastava. Mathprompter: Mathematical rea-             46595–46623, 2023.
     soning using large language models. arXiv preprint arXiv:2303.05398,
     2023.
