                                                 Autoformalization of Game Descriptions using Large Language Models

                                                                  Agnieszka Mensfelt1 , Kostas Stathis1 , Vince Trencsenyi1 ,
                                                             1
                                                               Department of Computer Science, Royal Holloway, University of London
                                                                 {agnieszka.mensfelt, kostas.stathis, vince.trencsenyi}@rhul.ac.uk
arXiv:2409.12300v1 [cs.AI] 18 Sep 2024




                                                                     Abstract                                   To the best of our knowledge, this work is the first to lever-
                                                                                                             age LLMs for autoformalization within the domain of game
                                           Game theory is a powerful framework for reasoning about           theory. The results pave the way for more easily accessi-
                                           strategic interactions, with applications in domains ranging
                                                                                                             ble applications of game theory, bridging the gap between
                                           from day-to-day life to international politics. However, ap-
                                           plying formal reasoning tools in such contexts is challenging,    natural language and formal reasoning in strategic interac-
                                           as these scenarios are often expressed in natural language. To    tive scenarios. The main contributions of this paper are as
                                           address this, we introduce a framework for the autoformaliza-     follows:
                                           tion of game-theoretic scenarios, which translates natural lan-
                                                                                                             • Dataset creation. We developed a dataset consisting of
                                           guage descriptions into formal logic representations suitable
                                           for formal solvers. Our approach utilizes one-shot prompting        105 natural language descriptions of scenarios that can be
                                           and a solver that provides feedback on syntactic correctness        modelled using game theory. This dataset includes both
                                           to allow LLMs to refine the code. We evaluate the framework         standard and non-standard descriptions, with and without
                                           using GPT-4o and a dataset of natural language problem de-          numerical payoffs, to vary the translation difficulty level.
                                           scriptions, achieving 98% syntactic correctness and 88% se-       • Autoformalization framework development. We pro-
                                           mantic correctness. These results show the potential of LLMs
                                           to bridge the gap between real-life strategic interactions and
                                                                                                               pose a novel framework for translating natural language
                                           formal reasoning.                                                   descriptions into formal representations, enabling formal
                                                                                                               reasoning in real-world game-theoretic scenarios.
                                                                                                             • Evaluation. We evaluate the performance of GPT-4o
                                                              1    Introduction                                within our framework by assessing its ability to trans-
                                         Game theory (von Neumann and Morgenstern 1944) is                     late natural language descriptions of strategic interac-
                                         a mathematical framework that facilitates the analysis of             tions into formal representations. Our evaluation includes
                                         competitive and cooperative interactions among rational               both zero-shot and one-shot prompting and examines the
                                         decision-makers. It can be applied to a wide range of sce-            model’s capacity to generate formal specifications for
                                         narios, from family decision-making to business strategies            games that differ structurally from provided examples.
                                         to nuclear conflict. However, these scenarios are typically
                                                                                                                The remainder of this paper is organized as follows. Sec-
                                         expressed in natural language, making it challenging to ap-
                                                                                                             tion 2 provides a background overview, including LLMs,
                                         ply formal reasoning tools directly. Moreover, the inherent
                                                                                                             game theory, and general game playing. Section 3 details the
                                         ambiguities and complexities of natural language compli-
                                                                                                             formal solver, the proposed framework, experimental setup,
                                         cate the task of automatically converting problem descrip-
                                                                                                             and the dataset of game descriptions. Section 4 presents the
                                         tions into formal representations suitable for solvers.
                                                                                                             evaluation results on the dataset. Section 5 reviews related
                                            Recent advancements in Large Language Models (LLMs)
                                                                                                             work. Finally, Section 6 provides the conclusions and out-
                                         offer a solution to this challenge. LLMs exhibit remarkable
                                                                                                             lines future work.
                                         abilities in handling the nuances of natural language in the
                                         context of translation. They have proved to be successful in
                                         converting natural language into formal representations, in-                             2    Background
                                         cluding mathematical (Wu et al. 2022; He-Yueya et al. 2023;         Large Language Models Multi-layered LSTMs are se-
                                         Jiang et al. 2022) and logical expressions (Cosler et al. 2023;     quential models that perform well on complex sequential
                                         Pan et al. 2023; Feng et al. 2023; Yang, Ishay, and Lee 2023;       tasks such as language translation (Sutskever, Vinyals, and
                                         Chen et al. 2023), which is known as autoformalization (Wu          Le 2014). Following the emergence of transformers and the
                                         et al. 2022). This paper explores the novel application of          success of pre-trained models (Qiu et al. 2020), such archi-
                                         LLMs in the context of game theory, specifically focusing on        tectures had become the go-to solution for state-of-the-art
                                         translating natural language descriptions of game-theoretic         Large Language Models (LLMs). LLM performance de-
                                         scenarios into formal representations that enable formal rea-       pends on billions of parameters and huge training data sets
                                         soning in real-world situations.                                    (Zhao et al. 2023). While LLMs generalize well over a wide
Table 1: A general game in matrix form, with the row and column   • T: the Temptation to defect, resulting from the opponent
players payoffs recorded as a tuple: (πrow , πcolumn )               choosing D against the player’s C;
               P1/P2          Cooperate   Defect                  • R: the Reward for mutual cooperation;
            Cooperate          (R, R)     (S, T)                  • P: the Punishment for mutual defection;
               Defect           (T, S)    (P, P)                  • S: the Sucker’s Payoff, resulting from the player cooperat-
                                                                     ing while the opponent chooses to defect.
                                                                  The relation of these four outcomes can be used to classify
variety of tasks, fine-tuning can be used to optimize their       strategic interaction into different games (Rasmusen 2006).
performance for specific tasks (Ziegler et al. 2020).
GPT-4o OpenAI’s GPT-4o (OpenAI 2024) is a current                 Prisoner’s Dilemma The Prisoner’s Dilemma is a sym-
state-of-the-art LLM. Its multi-modal architecture supports       metric game defined by a payoff structure that values the
text, image and audio inputs and outputs. GPT-4o super-           temptation to defect over mutual cooperation: T > R >
sedes GPT-4 (Achiam et al. 2023) and is estimated to have         P > S. An example payoff matrix is (-1,-1) for mutual co-
175B parameters. It has been shown to perform exception-          operation, (0,-10) for the temptation to defect, (-10,0) for the
ally well in reasoning tasks (Wang and Zhao 2024).                sucker’s payoff, and (5,5) for mutual defection. The negative
                                                                  payoffs represent years spent in prison.
Game Theory Game theory provides a mathematical
framework to reason about strategic interactions and              Hawk-Dove The Hawk-Dove game describes a situation
decision-making analytically (Osborne 2004). Following            where T is associated with the highest reward, but the pun-
the formalization by (Osborne and Rubinstein 1994), we de-        ishment for mutual defection yields the lowest utility. The
fine a game theoretic encounter – a game – by its players,        definitive relation T > R > S > P is demonstrated by
the available strategies and payoffs.                             the following payoff assignments: R:(0,0), S:(-1,1), T:(1,-
                                                                  1), P:(-10,-10).
Players Game theory assumes a simple definition of ratio-
nality to hold for all of its actors – the players – and that     Matching Pennies Matching Pennies is a zero-sum game.
each actor is aware that all others are also rational in the      In our generalised version of the game, if both players
same sense. Such players are expected to act intelligently        choose the same action, the row player gets higher pay-
and voluntarily, with a full understanding of the game and to     off while the opponent gets lower payoff. If the player
be acting to optimize their own utility score (Myerson 1984).     choices are in disagreement, the yields are the reverse re-
                                                                  sulting in the asymmetric outcome relations: R, P > T, S
                                                                  and T, S > R, P .
Strategies A player’s strategy maps the state of the game
to an available action, also considering the accumulated his-
tory (Osborne and Rubinstein 1994).                               Stag Hunt The Stag Hunt involves a payoff structure
                                                                  which values mutual cooperation over the temptation to de-
                                                                  fect. For instance, mutual cooperation gives both players
Payoff A payoff is a numerical value associated with a            a payoff of 3, the temptation to defect yields 2 while the
specific outcome of strategic interaction; it is the reward       sucker gets 0, and mutual defection will result in a reward
each player receives as a result of a combination of their        of 1 utility for both – resulting in the outcome relation
actions (Gibbons 1992).                                           R > T > P > S.

Game Based on the outlines of (Osborne and Rubinstein             Battle of the Sexes In this asymmetric coordination game,
1994) and (Rasmusen 2006), our games are formally defined         both players have a preferred action, while disagreement is
in the following way:                                             the least preferred outcome for both (Osborne 2004). For
• N : the set of n players;                                       instance, mutual cooperation yields (2, 1), mutual defection
                                                                  gives (1, 2), and distinct player choices result in 0 for both.
• Ai : ∀i ∈ N , a non-empty set of actions available to the
                                                                  From the row player’s perspective, the situation is charac-
  player;
                                                                  terised by the relation R > P > T, S, and P > R > T, S
• ui : a utility function mapping Ai → R, ∀i ∈ N , produc-        for the column player.
  ing πi .
   In the context of our experiments, we refer to non-            General Game Playing The idea behind general game
cooperative games in normal form (Rasmusen 2006). A gen-          playing (Genesereth, Love, and Pell 2005) is about how to
eral example is shown in Table 1. Our five games are char-        construct intelligent systems that can process the rules of
acterised by such 2 × 2 payoff matrices, having two players       arbitrary new games and learn to play these games with-
and two actions – Cooperate and Defect. Taking the row            out human intervention. Key to this idea is the notion of
player’s perspective, these actions lead to four possible out-    a Game Description Language (GDL), proposed as a for-
comes:                                                            mal and machine-processable language for describing the
rules of arbitrary games (Love et al. 2006). Initially, GDL         histories of moves starting in an initial situation denoted by
focused on information games only, but its extended ver-            a constant (e.g. s0). The special binary function do(M,
sion GDL-II covers both n-player games with incomplete              S) represents the situation resulting from the execution of
information (Thielscher 2010)) and games in extensive nor-          move M in situation S, as in the Situation Calculus.
mal form (Thielscher 2011). GDL-II is based on the stan-
                                                                    Game-independent part We specify legal transitions of
dard syntax and semantics of logic programming and char-
                                                                    an extended form game from an initial situation S to a final
acterised by special keywords about the role of players, what
                                                                    situation F as:
holds in the initial, intermediate, and final states of the game,
and other useful predicates about legal moves, and the utility      game(F,F):-
players once a goal state is achieved.                                  final(F).
   A challenge with GDL systems is learning without hu-             game(S,F):-
man guidance. To address this challenge players must be                 \+ final(S),
                                                                        legal(M,S),
able to reason about the possible actions of others, essen-             game(do(M,S),F).
tially evaluating hypothetical game situations before taking
action. Action languages like the classical Situation Cal-          The final situation F is returned when reached. In a non-final
culus (McCarthy and Hayes 1981) have been developed for             situation S, the game accepts a legal move M, and the game
precisely this purpose. Formal schemes and inference meth-          continues in the next do(M,S) situation, until the final situ-
ods are readily available for Situation Calculus (Giacomo,          ation F is reached. To reason about what holds in a situation,
Lespérance, and Pearce 2010; Lesperance et al. 2024), while        we use Situation Calculus:
their deployment in general game-playing presupposes a              holds(F, S):-
translation from GDL into existing, suitably expressive for-            initially(F, S).
malisms. One such scheme (Schiffel and Thielscher 2011)             holds(F, do(M, S)):-
shows how to fully embed GDL-II into a version of the                   effect(F, M, S).
Situation Calculus based on knowledge fluents (Scherl and           holds(F, do(M, S)):-
Levesque 2003). Inspired by these works, we present a gen-              holds(F, S),
eral game solver in section 3.1, that reasons with GDL spec-            \+ abnormal(F, M, S).
ifications, and show how the way the solver is represented             A fluent F holds in the initial situation, a new fluent F is
can guide an LLM to generate the game-specific parts of             initiated by the effects of a move M executed in a situation S,
different games after having seen example.                          and a fluent F persists after a move is made, provided it is not
                                                                    abnormal; abnormal fluents are terminated (do not persist).
                       3    Methods                                 Rules of the form:
Our methods rely on a logic programming solver that pro-            finally(F, S):- Conditions.
vides a game game-independent formulation of an initial
state, a set of legal moves, the effects of these moves on the      return derived fluents F describing the result of the game,
state, and a description of the final states of a game. This for-   when the Conditions hold in the final situation S.
mulation can generate or test all possible evolutions of a spe-     Game-dependent part For a specific game, we de-
cific game, given we provide it with the domain-dependent           fine game-dependent predicates for the initial state
part describing the specifics of that game. If we then feed the     initial/1, the legal moves legal/2, what holds in the
solver a logic programming description of a specific game           initial game situation via initially/2, the effects of a
and a textual description of that game to an LLM, we can            move on a situation via effect/3, what stops persisting in
then prompt the LLM to generate the formulations of dif-            a situation after the execution of a move via abnormal/3,
ferent games from textual descriptions. We then devise an           the final situation final/1, and the result of the game via
algorithm that allows us to do just that, viz., automatically       finally/2 definitions. To exemplify a game definition,
formalise logic programs of new games systematically from           we show how to describe a PD game with initial situation
textual descriptions of these games.                                s0, defined as:
                                                                    initial(s0).
3.1   Solver
                                                                    What holds in s0 we specify as:
Our solver consists of a game-independent part specifying
the rules of any game in extensive form, a game-dependent           initially(player(p1), s0).
part expressing the rules of a specific game, and a set of          initially(player(p2), s0).
auxiliary predicates used on top of these representations to        initially(role(p1,row), s0).
support processing a game. We represent all parts in Prolog:        initially(role(p2,col), s0).
                                                                    initially(control(p1), s0).
variables are denoted by uppercase letters, predicates and
                                                                    initially(control(p2), s0).
function symbols by lowercase letters. The symbol :- is
read as if, and \+ is read as not (negation by failure).            Player names are represented by unique identifiers (p1 and
An underscore ’ ’ is used to denote a variable whose value          p2), their roles (p1 is the row player, while p2 is the
is unused within a specific definition. In this setting, the        column player), and then the fact that initially any of them
state of a game is represented as a situation understood by         can play next (we use a control/1 fluent to indicate that,
as in GDL). What holds in the initial situation changes as a      ?- game(s0, F), finally(goal(p1, 100), F).
result of the move being made in the game. We represent           based on the game’s payoff matrix, our solver provides the
moves as terms of the form choice(P, M), where P is a             following two solutions:
player, and M is a move. As it is possible for any player in a
Prisoner’s Dilemma game to choose defect (’D’) or coop-           F=do(choice(p2,’C’),do(choice(p1,’D’),s0)) ;
                                                                  F=do(choice(p1,’D’),do(choice(p2,’C’),s0)) ;
erate (’C’), we write this as:
                                                                  false.
possible(choice(P,’D’), S):-
    holds(player(P), S).                                          In the first answer for F where p1 acted first and p2 second,
possible(choice(P,’C’), S):-                                      while in the second answer, the order is reversed. This is
    holds(player(P), S).                                          not unexpected, as the way we have defined the game both
                                                                  players have control in the initial state, and the answers show
It is then legal for a player to choose a possible move if they   both combinations.
have the control to execute it in the current situation:
legal(choice(P,M), S):-                                           3.2   Framework
    possible(choice(P,M), S),
    holds(control(P), S).                                         Algorithm 1 Generating game-specific predicates from
When a legal move M is made by a player P, the effect that        natural language descriptions. PD stands for Prisoner’s
this move is actually made is recorded in the next situation:     Dilemma.
                                                                   1: Input:
effect(did(P, M), choice(P, M), S).                                   Γ: game-independent predicates,
Once a legal move is executed, the player loses control,              N LP D : natural language description of PD,
which we specify in our framework as:                                 ξP D : game-specific predicates of PD,
                                                                      N LN G : natural language description of a new game.
abnormal(control(P), choice(P, M), S).                             2: Output:
I.e., after a choice made by a player, that player loses con-         ξN G : game-specific predicates for the new game.
trol and cannot play a move again from that situation on-          3: Parameter:
                                                                      max attempts: maximum correction attempts.
wards. Moves made in this way bring about the final situa-
                                                                   4: attempts ← 0
tion, which we specify as a situation term with two choices        5: trace ← ∅
made from the initial situation, one for each player.              6: while attempts < max attempts do
final(S):-                                                         7:     ξN G ← LLM.translate(Γ, N LP D , ξP D , N LN G )
    ground(S),                                                     8:     is valid ← solver.check predicates(ξN G )
    S=do(choice(_,_), do(choice(_,_), I)),                         9:     if is valid then
    initial(I).                                                   10:         return ξN G
                                                                  11:     else
Assuming the payoff matrix of Table 1 defined as:                 12:         trace ← solver.get trace()
payoff(’D’, ’D’, 35, 35).                                         13:         ξN G ← LLM.self correct(ξN G , trace)
payoff(’C’, ’D’, 10, 100).                                        14:     end if
payoff(’D’, ’C’, 100, 10).                                        15:     attempts ← attempts + 1
payoff(’C’, ’C’, 65, 65).                                         16: end while
                                                                  17: return Unable to generate valid predicates
the outcome of the game holds information about the actual            within maximum attempts.
moves made by the players and their payoffs.
finally(outcome(P1,M1,U1,P2,M2,U2), S):-                             To generate a formal game specification for a given game,
    final(S),
                                                                  we use the one-shot prompting approach. The prompt con-
    holds(role(P1, row), S),
    holds(did(P1, M1), S),                                        sists of game-independent predicates (Γ), an example: a nat-
    holds(role(P2, col), S),                                      ural language description of Prisoner’s Dilemma (N LP D )
    holds(did(P2, M2), S),                                        and game-specific predicates for PD (ξP D ), and a natural
    payoff(M1, M2, U1, U2).                                       language description of a game to be translated (N LN G ).
                                                                  An LLM is prompted iteratively. Once the game-specific
We can extract outcome information, e.g. the utility for a
                                                                  predicates (ξN G ) are generated, they are validated for syn-
player, through a goal/2 fluent (as in GDL) e.g.:
                                                                  tactic correctness using a Prolog solver. If the generated
finally(goal(P1, U1), S):-                                        predicates contain syntax errors, the LLM is re-prompted
    finally(outcome(P1,_,U1,_,_,_), S).                           with the solver’s error trace and additional instructions for
finally(goal(P2, U2), S):-                                        correcting the Prolog code. This correction process is re-
    finally(outcome(_,_,_,P2,_,U2), S).                           peated up to max attempts. An overview of the algo-
This completes the definition of a PD game and allows us          rithm is provided in Listing 1.
to use the above game description to reason about the game.
For instance, if player p1 wanted to reason about the game        3.3   Game descriptions
and determine the actions required to achieve a utility of 100,   To evaluate the ability of GPT-4o to translate natural lan-
expressed as the query:                                           guage game descriptions into their formal specification, we
       Payoffs/Description      Standard      Non-standard                      4    Results and Discussion
           Numerical                5              50
                                                                   Our experimental results include both zero-shot and one-
         Non-numerical              5              50
                                                                   shot prompting, as well as testing the model’s capability to
Table 2: Number of natural language game descriptions for each     generate formal specifications for games that differ struc-
variant. Standard refers to example employing a typical metaphor   turally from the provided examples. Although the out-
for a given game. Conversely, non-standard is a newly invented     comes from zero-shot prompting demonstrate the weak-
example of a situation that can be modelled by a given game. Nu-   nesses of LLMs to produce formal description for our game-
merical refers to descriptions containing numerical payoffs, and   independent part, one-shot prompting with an example is
non-numerical to descriptions without numerical payoffs.           able to provide results that adapt successfully the two-player
                                                                   game formulations for different game instances.

used standard examples of five classic 2-player simultane-         4.1   Zero-shot prompting
ous one-shot games from game theory: Battle of the Sexes,          We started by performing zero-shot prompting, including
Hawk-Dove, Matching Pennies, Prisoner’s Dilemma, and               only the predicates for the game-independent part in the
Stag Hunt. Additionally, we investigated the GPT-4o’s ca-          prompt. The goal was to generate the game-dependent part
pability to formalize a description of a real-world conflict or    from a textual description without an example. For PD, the
cooperation situation that can be modelled by one of the five      following code sequence was generated as an answer. The
games but differs from the typically used metaphor.                first part of the answer contained the representation of the
   The real-world dilemma descriptions were synthetically          players and the legal moves:
generated. For each game, a real-life scenario was devel-
oped that avoided the standard metaphor (e.g., avoiding two        suspect(suspect1).
prisoners for the Prisoner’s Dilemma). Then, GPT-4o was            suspect(suspect2).
prompted to create further dilemmas from various domains
such as social life, business, politics, and warfare, using the    legal(confess(S), _):- suspect(S).
                                                                   legal(silent(S), _):- suspect(S).
initial scenario as a template. To increase the difficulty, some
natural language descriptions were generated without nu-           Although players represented as suspects is acceptable,
merical payoffs. Table 2 summarizes the number of game             players’ moves being legal in any state is not; the under-
descriptions for each variant, resulting in 110 descriptions       score (’ ’) indicates that state is unnecessary when check-
of simultaneous move games.                                        ing whether a move is legal. This is obviously undesired, as
   In a separate experiment, we evaluated the performance of       it is illegal to make two consecutive moves, but the formu-
GPT-4o using a zero-shot prompting approach. In this case,         lation allows it. The generated answer also contains what
only the game-independent predicates (Γ) were provided in          holds initially:
the prompt, without the inclusion of any example game-
specific predicates, such as ξP D . This experiment aimed          initially(state(0, 0), s0).
to assess the model’s ability to formalize a game without          Here clearly the generated code is problematic as the term
prior examples. Additionally, to analyse the LLM’s capac-          state(0,0) has unclear parameters, including their 0
ity to generalize from examples, we conducted an autofor-          value. Also, problematic is the code generated subsequently,
malization of two differently structured games: a sequen-          for when a state is final:
tial version of the Prisoner’s Dilemma, where players take
turns making decisions, and the Rock-Paper-Scissors game,          final(state(_, _)).
which provides more than two choices per player and lacks          This implies that any state term of the form state( , ) is
specified numerical payoffs.                                       final. So already the solution so far is unusable. The situa-
                                                                   tion deteriorates with the effects of moves. We show below
3.4      Experimental parameters                                   an effect rule, specified as:
                                                                   effect(state(Y1, Y2), silent(suspect1),
          LLM                                     GPT-4o               state(NY1, NY2)) :-
          temperature                             1                    holds(state(Y1, Y2), s0),
          maximum output tokens                   1024                 ( % If suspect2 also silent
          maximum attempts number                 5                        holds(state(_, _), do(silent(
                                                                               suspect2), s0))
                  Table 3: Experimental parameters.                    -> NY1 is Y1 + 1, NY2 is Y2 + 1
                                                                       ; % If suspect2 confesses
                                                                         NY1 is Y1, NY2 is 10
   To perform autoformalization we employed state-of-the-              ).
art model GPT-4o. The experimental parameters used in the
evaluation are shown in Table 3. The source code and the           The above effect rule has the state as the first and third argu-
logs generated in the experiment are publicly available1 .         ments, but the state is not in situation calculus format. As a
                                                                   result, only what happens at the initial state will be inferred
   1
       https://github.com/dicelab-rhul/game-formaliser             correctly. Also, the first argument is intended as a fluent in
      Payoffs/Desc.        Standard        Non-standard                                              Semantic Accuracy by Game
                         synt sem          synt sem                                 100                      Correctness
        Numerical         1.00   1.00       1.00   0.90                                                          correct
      Non-numerical       1.00   1.00       0.96   0.83                                                          incorrect
                                                                                    80
Table 4: Syntactic and semantic accuracy of generated game-




                                                                    Frequency [%]
specific predicates. Synt denotes syntactic accuracy, sem denotes                   60
semantic accuracy.
                                                                                    40

the game-independent part of our formulation, but the gener-                        20
ated answer does not reflect this. Moreover, from the above,
we can now see that the two parameters of the state are used                         0
for storing the players’ utility, originally set to zero, updated                             BS     HD         MP           PD   SH
                                                                                                               Game
wrongly, and missing all other useful state information that
is required. Finally, this kind of formulation for effects re-
                                                                    Figure 1: Semantic accuracy of generated predicates for each of
quires that nothing can be abnormal in the generated answer:
                                                                    the games. “BS”, “HD”, “MP”, “PD”, and “SH” stand for Battle
abnormal(_, _, _) :- false.                                         of the Sexes, Hawk-Dove, Matching Pennies, Prisoner’s Dilemma,
                                                                    and Stag-Hunt, respectively.
All the above show that there is no deep understanding of
how the situation calculus really works.
                                                                    was 90% for the numerical variants and 83% for the non-
4.2    2-player simultaneous move games                             numerical ones. Fig. 1 shows the semantic accuracy for each
In the one-shot prompting method, we provided game-                 of the considered games. Interestingly, even though the Pris-
specific axioms for prisoner’s dilemma, ξP D , as an example.       oner’s Dilemma was provided as an example in the prompt,
This resulted in the generation of game-specific predicates         some translations of real-world situations modeled by PD
for the natural language description variants presented in Ta-      were incorrect. In contrast, all translations for Hawk-Dove
ble 2, analogous to those defined for PD (see Sect. 3.1). The       and Stag Hunt were semantically accurate, despite no spe-
main difference was the definition of the payoff matrix. Ta-        cific examples being provided in the prompt for these games.
ble 4 summarizes the syntactic and semantic accuracy of the         It may suggest that the Prisoner’s Dilemma is more chal-
generated predicates. Syntactic accuracy refers to the per-         lenging, however, the number of errors was not significantly
centage of syntactically correct Prolog programs produced           high. Most of the semantic errors involved incorrect payoff
on the first translation attempt, before any revisions were         assignment in the predicates specifying the payoff matrix.
made. The semantic correctness of the generated predicates          In one case, one, instead of two constants was used in pred-
(e.g. the relationships between payoffs in the payoff ma-           icates describing the payoff matrix:
trix) was reviewed manually. During the inspection of non-          payoffRD(’Holiday Holiday’, -1, 3)
standard natural language descriptions, some instances were
found to be incomplete or ambiguous. As a result, semantic            Overall, the translation showed high syntactic and lower
accuracy was calculated based on 48 samples for the numer-          semantic correctness. It is worth noting that the real-world
ical variants and 47 samples for the non-numerical variants.        examples were translated in most cases correctly, even in the
   The generated code was syntactically correct in 108 out of       absence of numerical payoffs.
110 cases (98%). In one of the incorrect cases, the error in-
volved the use of a comment delimiter (’//’), not valid in Pro-     4.3                   Towards Generalisation
log. In the second case, the code triggered a warning about         Sequential PD In order to explore whether the LLM can
singleton variables. Notably, despite receiving feedback            generalise over different aspects of a game, we also run our
from the Prolog solver, GPT-4o was unable to fix the syntac-        system to see what is generated in the case of the sequential
tic errors. This contrasts with our previous work, where the        PD. This is a turn-based two-player game in which there is
model was able to correct reasoning errors in game-theoretic        a first-mover that chooses to cooperate or defect, and after
scenarios based on solver feedback (Mensfelt, Stathis, and          observing this choice, the second-mover responds with an
Trencsenyi 2024). A potential explanation could be that             action of the same set. In terms of the game specification,
the feedback prompt, which included the solver trace and            the LLM should produce the same specification as the game-
debugging guidelines, may not have been specific enough.            dependent part of Section 3.1, with the only differences (a)
However, when the model was re-prompted in a separate               a revised payoff matrix and (b) the way the initial state is
call, syntactically correct code was generated on the first at-     specified, to allow only for one player to play first, and not
tempt. For analyzing semantic correctness, the syntactically        both, i.e. it should contain only one player having the control
incorrect codes were replaced with corrected versions.              of the game at state s0. Indeed, as shown below, the system
   Regarding semantic correctness, the standard examples            generated in the initial state two players a and b, the role of
were translated into their formal specification with 100%           a is to play first, and of b second, and the control is given to
accuracy. For the non-standard examples, the accuracy               only to a:
initially(player(a), s0).                                         occurred in some cases. Pan et al. (Pan et al. 2023) com-
initially(player(b), s0).                                         bined in-context learning with self-refinement based on the
initially(role(a, first), s0).                                    evaluation from the solver. This improved the performance
initially(role(b, second), s0).                                   over standard LLM and chain-of-thought prompting on log-
initially(control(a), s0).                                        ical reasoning benchmarks. This approach was also not free
Rock-Paper-Scissors We also explored whether the LLM              from translation errors. To address this problem in the con-
can generalise over the number of moves of the game and           text of translation to temporal logics, Cosler et al. (Cosler et
the specification of the possible moves. For this purpose, we     al. 2023) introduced an interactive approach in which the
gave it the textual description of the Rock-Paper-Scissors        user can edit sub-translations. Fine-tuning of LLMs was
game, a simultaneous zero-sum game that has three pos-            demonstrated to be another successful method for increas-
sible outcomes: a draw, a win, or a loss. A player who            ing translation accuracy in both temporal logics (Chen et al.
decides to play rock will beat another player who chooses         2023) and deductive datasets (Feng et al. 2023).
scissors (“rock crushes scissors”), but will lose to one who         The aforementioned works considered standard logical
has played paper (“paper covers rock”); a play of paper will      reasoning tasks and benchmarks. To the best of our knowl-
lose to a play of scissors (“scissors cuts paper”). If both       edge, this work is the first to perform autoformalization in
players choose the same shape, the game is tied and is usu-       the context of game theory.
ally replayed to break the tie. Again, our system produced
the same specification as the game-dependent part of Sec-
tion 3.1, with the only differences (a) a revised payoff matrix
and (b) the way possible moves were specified, to allow for
                                                                          6    Conclusions and Future Work
three moves instead of two, as shown below:
                                                                  To evaluate the ability of our framework and GPT-4o to per-
possible(choice(P, ’rock’), S) :-
                                                                  form autoformalization in the domain of logical represen-
    holds(player(P), S).
possible(choice(P, ’paper’), S) :-                                tation of game-theoretic scenarios, we developed a dataset
    holds(player(P), S).                                          of natural-language descriptions. The descriptions involved
possible(choice(P, ’scissors’), S) :-                             scenarios ranging from family decision-making to business
    holds(player(P), S).                                          to warfare, possible to model by 2-players simultaneous-
                                                                  move games. The descriptions were developed in two ver-
This demonstrates that our original formulation of a domain-      sions, including and lacking numerical payoffs.
specific game allowed our system to generalise well to dif-
ferent aspects of a new game.                                        The preliminary assessment demonstrated that with zero-
                                                                  shot prompting GPT-4o was not able to autoformalize the
                   5    Related Work                              standard description of the Prisoner’s Dilemma. One-shot
                                                                  prompting, however, showed high syntactic and semantic
LLMs have gained significant interest as potential build-         accuracy. Interestingly, even in the case of real-world ex-
ing blocks for agents in game-theoretical simulations (Akata      amples with no numeric payoffs, the LLM was mostly able
et al. 2023; Fan et al. 2023; Guo 2023; Lorè and Heydari         to infer an appropriate payoff matrix. To evaluate the abil-
2023). Despite their promise, a major obstacle is the in-         ity of generalization within the proposed framework, we
herent challenge that reasoning tasks pose for LLMs (Rae          used the natural-language descriptions of sequential Pris-
et al. 2022), (Nye et al. 2021). While techniques such as         oner’s Dilemma and Rock-Paper-Scissors. The formal rep-
Chain-of-Thought (Wei et al. 2023) can enhance perfor-            resentation of both games, differing in structure from non-
mance in some of the tasks, even state-of-the-art models are      sequential PD provided as an example in the prompt, were
not free from logical and arithmetic errors (Imani, Du, and       syntactically and semantically correct.
Shrivastava 2023). An alternative approach to leveraging
LLMs for reasoning in game-theoretic scenarios is to utilise         We acknowledge several limitations of this work. The se-
them for translating natural language into formal representa-     mantic correctness was investigated manually, which limits
tions, followed by employing a formal solver for the actual       the scalability of the evaluation. We plan to address this in
reasoning process. This method, known as autoformaliza-           future work by not only generating the predicates for the
tion (Wu et al. 2022), has been successful in translating nat-    game description but also executing the code to find payoffs
ural language into mathematical formalisms (Wu et al. 2022;       for specific actions, which will allow us to automatize the
He-Yueya et al. 2023; Jiang et al. 2022), providing a method      evaluation. The class of games that we considered was lim-
to integrate LLMs with formal tools to solve reasoning tasks.     ited to 2-players simultaneous-move games and two games
   The autoformalization approach was also successfully ap-       that differ only in the sequential nature of decision-making
plied to creating logical representations of natural language     and the number of possible actions. We will expand the set
descriptions. Yang et al. (Yang, Ishay, and Lee 2023) used        of considered games to include games from outside this class
GPT-3 and few-shot prompting to translate natural lan-            and outside game theory.
guage sentences into their formal representation, passed as          Overall, the results show the promise of using LLMs as a
an input to answer set programs. GPT-3 autoformalization          bridge between real-life strategic interactions and the game
coupled with ASP achieved high accuracy on NLP bench-             theory framework, facilitating the use of formal tools in find-
marks, however, errors in translation from natural language       ing an optimal action in such scenarios.
                   Acknowledgments                                 Lorè, N., and Heydari, B. 2023. Strategic behavior of large
This work was supported by a Leverhulme Trust Interna-             language models: Game structure vs. contextual framing.
tional Professorship Grant (LIP-2022-001).                         arXiv preprint arXiv:2309.05898.
                                                                   Love, N.; Hinrichs, T.; Haley, D.; Schkufza, E.; and Gene-
                        References                                 sereth, M. 2006. General Game Playing: Game Description
                                                                   Language Specification. Technical Report LG–2006–01,
Achiam, J.; Adler, S.; Agarwal, S.; et al. 2023. GPT-4
                                                                   Stanford University.
technical report. arXiv preprint arXiv:2303.08774.
Akata, E.; Schulz, L.; Coda-Forno, J.; et al. 2023. Playing        McCarthy, J., and Hayes, P. 1981. Some philosophical prob-
repeated games with large language models. arXiv preprint          lems from the standpoint of artificial intelligence. In Web-
arXiv:2305.16867.                                                  ber, B. L., and Nilsson, N. J., eds., Readings in Artificial
                                                                   Intelligence. Morgan Kaufmann. 431–450.
Chen, Y.; Gandhi, R.; Zhang, Y.; and Fan, C. 2023. Nl2tl:
Transforming natural languages to temporal logics using            Mensfelt, A.; Stathis, K.; and Trencsenyi, V. 2024. Logic-
large language models. In Proceedings of the 2023 Confer-          enhanced language model agents for trustworthy social sim-
ence on Empirical Methods in Natural Language Process-             ulations. arXiv preprint arXiv:2408.16081.
ing, 15880–15903.                                                  Myerson, R. B. 1984. An introduction to game theory.
Cosler, M.; Hahn, C.; Mendoza, D.; Schmitt, F.; and Trippel,       Discussion Papers 623, Northwestern University, Center for
C. 2023. nl2spec: interactively translating unstructured nat-      Mathematical Studies in Economics and Management Sci-
ural language to temporal logics with large language mod-          ence.
els. In International Conference on Computer Aided Verifi-         Nye, M.; Tessler, M. H.; Tenenbaum, J. B.; and Lake, B. M.
cation, 383–396. Springer.                                         2021. Improving coherence and consistency in neural se-
Fan, C.; Chen, J.; Jin, Y.; and He, H. 2023. Can large             quence models with dual-system, neuro-symbolic reason-
language models serve as rational players in game theory? a        ing. arXiv preprint arXiv:2107.02794.
systematic analysis. arXiv preprint arXiv:2312.05488.              OpenAI.      2024.      GPT-4o.       https://openai.com/index/
Feng, J.; Xu, R.; Hao, J.; Sharma, H.; Shen, Y.; Zhao, D.;         hello-gpt-4o/. Accessed: 25/07/2024.
and Chen, W. 2023. Language models can be logical solvers.         Osborne, M., and Rubinstein, A. 1994. A Course in Game
arXiv preprint arXiv:2311.06158.                                   Theory. The MIT Press.
Genesereth, M. R.; Love, N.; and Pell, B. 2005. General            Osborne, M. 2004. Introduction to Game Theory. Oxford
game playing: Overview of the AAAI competition. AI Mag.            University Press USA.
26(2):62–72.
                                                                   Pan, L.; Albalak, A.; Wang, X.; and Wang, W. 2023.
Giacomo, G. D.; Lespérance, Y.; and Pearce, A. R. 2010.           Logic-lm: Empowering large language models with sym-
Situation calculus based programs for representing and rea-        bolic solvers for faithful logical reasoning. In Findings of the
soning about game structures. In Lin, F.; Sattler, U.; and         Association for Computational Linguistics: EMNLP 2023,
Truszczynski, M., eds., Principles of Knowledge Represen-          3806–3824.
tation and Reasoning: Proceedings of the Twelfth Inter-
national Conference, KR 2010, Toronto, Ontario, Canada,            Qiu, X.; Sun, T.; Xu, Y.; Shao, Y.; Dai, N.; and Huang, X.
May 9-13, 2010. AAAI Press.                                        2020. Pre-trained models for natural language processing:
                                                                   A survey. Science China Technological Sciences 63:1872–
Gibbons, R. 1992. A Primer in Game Theory. Harlow,                 1897.
Essex, United Kingdom: Pearson Education Limited.
                                                                   Rae, J. W.; Borgeaud, S.; Cai, T.; et al. 2022. Scaling lan-
Guo, F. 2023. GPT agents in game theory experiments.               guage models: Methods, analysis & insights from training
arXiv preprint arXiv:2305.05516.                                   gopher. arXiv preprint arXiv:2112.11446.
He-Yueya, J.; Poesia, G.; Wang, R. E.; and Goodman,
                                                                   Rasmusen, E. 2006. Games and information an introduction
N. D. 2023. Solving math word problems by combin-
                                                                   to game theory. Blackwell.
ing language models with symbolic solvers. arXiv preprint
arXiv:2304.09102.                                                  Scherl, R. B., and Levesque, H. J. 2003. Knowledge, action,
Imani, S.; Du, L.; and Shrivastava, H. 2023. Mathprompter:         and the frame problem. Artif. Intell. 144(1-2):1–39.
Mathematical reasoning using large language models. arXiv          Schiffel, S., and Thielscher, M. 2011. Reasoning about
preprint arXiv:2303.05398.                                         general games described in gdl-ii. Proceedings of the AAAI
Jiang, A. Q.; Welleck, S.; Zhou, J. P.; Li, W.; Liu, J.; Jamnik,   Conference on Artificial Intelligence 25(1):846–851.
M.; Lacroix, T.; Wu, Y.; and Lample, G. 2022. Draft, sketch,       Sutskever, I.; Vinyals, O.; and Le, Q. V. 2014. Sequence to
and prove: Guiding formal theorem provers with informal            sequence learning with neural networks. In Ghahramani, Z.;
proofs. arXiv preprint arXiv:2210.12283.                           Welling, M.; Cortes, C.; Lawrence, N.; and Weinberger, K.,
Lesperance, Y.; De Giacomo, G.; Rostamigiv, M.; and Khan,          eds., Advances in Neural Information Processing Systems,
S. M. 2024. Abstraction of situation calculus concurrent           volume 27. Curran Associates, Inc.
game structures. Proceedings of the AAAI Conference on             Thielscher, M. 2010. A general game description language
Artificial Intelligence 38(9):10624–10634.                         for incomplete information games. In Proceedings of the
Twenty-Fourth AAAI Conference on Artificial Intelligence,
AAAI’10, 994–999. AAAI Press.
Thielscher, M. 2011. The general game playing descrip-
tion language is universal. In Walsh, T., ed., IJCAI 2011,
Proceedings of the 22nd International Joint Conference on
Artificial Intelligence, Barcelona, Catalonia, Spain, July 16-
22, 2011, 1107–1112. IJCAI/AAAI.
von Neumann, J., and Morgenstern, O. 1944. Theory of
Games and Economic Behavior (60th Anniversary Com-
memorative Edition). Princeton University Press.
Wang, Y., and Zhao, Y. 2024. Rupbench: Benchmarking
reasoning under perturbations for robustness evaluation in
large language models. arXiv preprint arXiv:2406.11020.
Wei, J.; Wang, X.; Schuurmans, D.; et al. 2023. Chain-of-
thought prompting elicits reasoning in large language mod-
els. arXiv preprint arXiv:2201.11903.
Wu, Y.; Jiang, A. Q.; Li, W.; Rabe, M.; Staats, C.; Jamnik,
M.; and Szegedy, C. 2022. Autoformalization with large
language models. Advances in Neural Information Process-
ing Systems 35:32353–32368.
Yang, Z.; Ishay, A.; and Lee, J. 2023. Coupling large lan-
guage models with logic programming for robust and gen-
eral reasoning from text. arXiv preprint arXiv:2307.07696.
Zhao, W. X.; Zhou, K.; Li, J.; et al. 2023. A survey of large
language models. arXiv preprint arXiv:2303.18223.
Ziegler, D. M.; Stiennon, N.; Wu, J.; Brown, T. B.; et al.
2020. Fine-tuning language models from human prefer-
ences. arXiv preprint arXiv:1909.08593.
