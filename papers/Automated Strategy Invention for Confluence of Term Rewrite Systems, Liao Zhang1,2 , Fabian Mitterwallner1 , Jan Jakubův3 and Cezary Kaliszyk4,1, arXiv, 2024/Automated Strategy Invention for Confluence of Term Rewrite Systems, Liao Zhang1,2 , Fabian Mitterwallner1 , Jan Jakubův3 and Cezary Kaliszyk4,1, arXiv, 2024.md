                                                 Automated Strategy Invention for Confluence of Term Rewrite Systems
                                                     Liao Zhang1,2 , Fabian Mitterwallner1 , Jan Jakubův3 and Cezary Kaliszyk4,1
                                                                                  1
                                                                                    University of Innsbruck
                                                                              2
                                                                                Shanghai Jiao Tong University
                                                                          3
                                                                            Czech Technical University in Prague
                                                                                 4
                                                                                   University of Melbourne
                                             zhangliao714@gmail.com, fabian.mitterwallner@uibk.ac.at, {jakubuv, cezarykaliszyk}@gmail.com

                                                                  Abstract                                 appropriate strategies automatically. In this paper, we fo-
arXiv:2411.06409v2 [cs.LO] 31 Jul 2025




                                                                                                           cus on confluence, an important property of term rewriting,
                                              Term rewriting plays a crucial role in software ver-         and discuss automated strategy invention for the state-of-the-
                                              ification and compiler optimization. With dozens             art confluence prover CSI [Nagele et al., 2017]. We mod-
                                              of highly parameterizable techniques developed to            ify Grackle [Hůla and Jakubův, 2022], an automatic tool to
                                              prove various system properties, automatic term              generate a strategy portfolio, encoding strategies that require
                                              rewriting tools work in an extensive parameter               transformations and complex schedules such as parallelism.
                                              space. This complexity exceeds human capacity                   Directly using a tool like Grackle to randomly generate
                                              for parameter selection, motivating an investigation         parameters for CSI may produce unsound results. This is
                                              into automated strategy invention. In this paper, we         a unique challenge compared to previous applications of
                                              focus on confluence of term rewrite systems, and             Grackle [Hůla and Jakubův, 2022; Aleksandrova et al., 2024].
                                              apply AI techniques to invent strategies for auto-           The solvers to which Grackle was previously applied always
                                              matic confluence proving. Moreover, we randomly              produce sound results, while CSI’s users need to carefully
                                              generate a large dataset to analyze confluence for           specify their strategies to ensure soundness.
                                              term rewrite systems. We improve the state-of-                  We also augment the human-built confluence problems
                                              the-art automatic confluence prover CSI: When                database (ARI-COPS)1 , a representative benchmark for the
                                              equipped with our invented strategies, it surpasses          annual confluence competition (CoCo)2 . Before 2024, CoCo
                                              its human-designed strategies both on the aug-               used the COPS database as the benchmark. An unpublished
                                              mented dataset and on the original human-created             duplicate checker is executed to remove duplicated problems
                                              benchmark dataset ARI-COPS, proving/disproving               in COPS, resulting in the ARI-COPS database, which is used
                                              the confluence of several term rewrite systems for           in CoCo 2024. As ARI-COPS has been created manually, it
                                              which no automated proofs were known before.                 includes only 566 TRSs. They are of high quality, but the
                                                                                                           relatively small number is still inadequate for data-driven AI
                                                                                                           techniques that require large amounts of training data. To
                                         1    Introduction                                                 handle this problem, we generate a large number of TRSs
                                         Term rewriting studies substituting subterms of a formula         randomly, but ensure that they are interesting enough to an-
                                         with other terms [Baader and Nipkow, 1998], playing               alyze. For this, we develop a procedure to confirm a relative
                                         an important role in automated reasoning [Bachmair and            balance in the number of TRSs most quickly solved by dif-
                                         Ganzinger, 1994], software verification [Meseguer, 2003],         ferent confluence analysis techniques within the dataset.
                                         and compiler optimization [Willsey et al., 2021]. Mathe-             We evaluate our strategy invention approach in ARI-COPS
                                         maticians have developed various techniques to analyze the        and the augmented dataset. On both of the datasets, the in-
                                         properties of term rewrite systems (TRSs). However, many          vented strategies surpass CSI’s competition strategy. In par-
                                         properties are undecidable [Baader and Nipkow, 1998], im-         ticular, we prove (non-)confluence for several TRSs that have
                                         plying that no technique can consistently prove a particular      not been proved by any automatic confluence provers in the
                                         property. To navigate this undecidability, modern term rewrit-    history of the CoCo competition.
                                         ing provers typically employ complicated strategies, incorpo-        As an example, our invented strategy is able to dis-
                                         rating wide arrays of rewriting analysis techniques, with the     prove confluence for the ARI-COPS problem 846.ari
                                         hope that one will be effective. Each technique often accom-      (991.trs in COPS), never proved by any participant in
                                         panies several flags to control its behavior. The diversity of    CoCo. The key is the application of the redundant rule
                                         techniques and their controlling flags result in a vast parame-   technique [Nagele et al., 2015] with non-standard argu-
                                         ter space for modern automated term rewriting provers.            ments. CSI’s competition strategy performs redundant
                                            Manually optimizing strategies for undecidable problems
                                                                                                              1
                                         is beyond human capacity given the extensive parameter                   https://ari-cops.uibk.ac.at/
                                                                                                              2
                                         space. This inspires us to apply AI techniques to search for             https://project-coco.uibk.ac.at/
-narrowfwd -narrowbwd -size 7 prior to perform-                    variables and function symbols. The set of variables occur-
ing non-confluence analysis. The flags narrowfwd and               ring in a term t is denoted by Var (t). A term rewrite sys-
narrowbwd determine the categories of redundant rules to           tem (TRS) consists of a set of rewrite rules l → r where
generate. Our tool automatically discovered that by changing       l, r ∈ terms, l ∈ / variables, and Var (r) ⊆ Var (l). We write
the original redundant rule transformation to redundant            t1 →∗ tn to denote t1 → t2 → ... → tn where n can be
-development 6 -size 7, we can prove this problem.                 one. A TRS is confluent if and only if ∀s, t, u ∈ terms(s →∗
A larger value for the flag development causes a larger            t ∧ s →∗ u ⇒ ∃v ∈ terms(t →∗ v ∧ u →∗ v)). Con-
number of development redundant rules to be added. We no-          sider the TRS of {f (g(x), h(x)) → a, g(b) → d, h(c) →
tice that the value six is crucial as small values below three     d} [Gramlich, 1996]. It is not confluent since f (d, h(b)) ←
are ineffective for 846.ari. This is only one of the several       f (g(b), h(b)) → a, and no rules are applicable to f (d, h(b))
TRSs which our new strategies can solve as discussed in the        and a. A rewrite rule l → r is called left-linear if no variable
later sections.                                                    occurs multiple times in l. A TRS is called left-linear if all
   The main reason why it is difficult to discover new proofs      its rules are left-linear. Left-linearity is crucial for confluence
in CoCo, is because CSI’s competition strategy developed           analysis since most existing confluence techniques only ap-
rewriting experts is very complicated, for which a compre-         ply to such systems. In this paper, a term is called complex if
hensive explanation is presented in the technical appendix.        it is neither a variable nor a constant.
For example the competition strategy includes the develop-
ment redundant rule technique [Nagele et al., 2015]. The           2.2   CSI
original evaluation of it shows no improvement over other          CSI is one of the state-of-the-art automatic confluence
redundant rule techniques in COPS at that time. Thus, CSI’s        provers that participates in CoCo. It ranked first in five
developers decided not to use it in the competition strategy.      categories of competitions in CoCo 2024. To show (non-
As COPS grows, it becomes helpful in some new TRSs such            )confluence of TRSs, CSI automatically executes a range of
as 846.ari. However, the default strategy has only slightly        techniques, scheduled by a complicated configuration docu-
changed over the past years, and the development redundant         ment written by experts in confluence analysis. Subsequently,
rule technique has never been tried. One reason for this could     CSI either outputs YES, NO, or MAYBE indicating confluence,
be that choosing sound parameters is challenging even for          non-confluence, or indetermination, respectively.
rewriting experts. Meanwhile, competition strategy is highly           CSI implements many techniques applicable to the analy-
complicated and has a prohibitively large configuration space      sis of TRSs (many of them parametrized or transforming the
both in the number of parameters and structures of the strat-      system into one that can be analyzed by other techniques)
egy itself. We leverage Grackle to do the tedious strategy         and utilizes a complicated strategy language to control them.
search. It can automatically optimize the strategies better than   In CSI, these techniques are called processors. They are de-
experts as the dataset grows. Other rewriting tools do not dis-    signed to prove the properties of TRSs, perform various trans-
cover the proof perhaps because they do not implement the          formations, and check the satisfiability of certain conditions.
essential techniques for solving the problems.                     The strategy language can flexibly combine the execution of
Contributions. First, to our best knowledge, our work is           processors such as specifying parallel or sequential applica-
the first application of AI techniques to automatic confluence     tions, disregarding unexpected results, assigning time lim-
provers. We automatically generate a lot of strategies for the     its, and designating repeated applications. The details of the
state-of-the-art confluence prover CSI and combine them as         strategy language are presented in the technical appendix.
a unified strategy. Second, we carefully design the parame-            Since the generated proofs are almost always large and dif-
ter search space for CSI to confirm the soundness of strategy      ficult to check manually, CSI relies on an external certifier
invention. Third, we build a large dataset for confluence anal-    CeTA [Thiemann and Sternagel, 2009] to verify its proofs. To
ysis, comprising randomly generated TRSs and problems in           utilize CeTA, CSI outputs a certificate of its proof in the cer-
the ARI-COPS dataset. Finally, empirical results show that         tification problem format [Sternagel and Thiemann, 2014a].
our strategy invention approach surpasses CSI’s competition        Given a certificate, CeTA will either answer CERTIFIED or
strategy both in ARI-COPS and the augmented datasets. No-          present a reason to reject it. Not all processors implemented
tably, we discover several proofs for (non-)confluence that        in CSI are verifiable because CSI cannot produce certificates
have never been discovered by any automatic confluence             for all processors, and CeTA does not implement the verifica-
provers in the annual confluence competition.                      tion procedures for all processors.

                                                                   2.3   Grackle
2     Background
                                                                      Grackle [Hůla and Jakubův, 2022] is a strategy optimiza-
2.1    Term Rewriting                                              tion system designed to automate the generation of various
We informally define some theoretical properties of term           effective strategies for a given solver based on benchmark
rewriting in this section, hoping to ease the understanding        problems. Such solvers receive a problem and decide the sat-
of the behavior underlining automatic confluence provers. A        isfiability of a particular property of the problem. It was origi-
formal description can be found in the technical appendix.         nally designed for automated reasoning tools and has been ap-
   We assume a disjoint set of variable symbols and a fi-          plied to various provers such as Prover9 [McCune, 2005] and
nite signature of function symbols. Constants are function         Lash [Brown and Kaliszyk, 2022]. We choose Grackle for
symbols with zero arity. The set of terms is built up from         our research, as it is highly adaptable and we are not aware of
Algorithm 1 GrackleLoop: an outline of the strategy portfo-        ated with a default value and several disjoint potential val-
lio invention loop.                                                ues. Grackle users need to input the potential values based on
Input: initial strategies S, benchmark problems P,                 their domain-specific experiences on the particular solvers.
        hyperparameters β                                          We refer to [Hůla and Jakubův, 2022] for a comprehensive
Output: a strategy portfolio Φ                                     explanation of Grackle.
  1: Φstrat ← S
  2: while termination criteria is not satisfied do                3     Strategy Invention and Combination
  3:   Evaluate(P, Φ, β)                                           To generate a better strategy for CSI, we first invent a large set
  4:   Φcur ← Reduce(P, Φ, β)                                      of complementary strategies, and then appropriately combine
  5:   s ← Select(P, Φ, β)                                         a subset of the invented strategies into a single strategy.
  6:   if s is None then return Φ
  7:   s0 ← Specialize(s, P, Φ, β)                                 3.1    Strategy Invention
  8:   Φstrat ← Φstrat ∪ s0
  9: end while                                                     To find new strategies for CSI, we first need to represent the
                                                                   parameter space in a meaningful way. The parameter space
                                                                   needs to be designed with precision to guarantee soundness.
any strategy invention program that would allow the kinds of          There are three reasons why CSI may produce unsound
strategies needed for automatic rewriting tools. Additionally,     results given an entirely random strategy. First, some pro-
Grackle has achieved good results with the solvers it was pre-     cessors are not intended for confluence analysis. They may
viously applied to. The strategy invention problem of Grackle      intend to prove other properties of TRSs, such as termina-
is formally defined below.                                         tion [Baader and Nipkow, 1998]. Second, even for the same
                                                                   processor, it may be designed to prove different properties of
Definition 1 (Strategy Invention Problem). Assume a set of
                                                                   TRSs with different flags. Third, some transformation pro-
initial strategies S. In the benchmark of examples P, the
                                                                   cessors may change the goal of CSI to prove another property
problem is to invent a bounded set of complementary strate-
                                                                   of TRSs, which is different from confluence such as relative
gies S ′ that can prove the largest number of problems in P.
                                                                   termination [Zantema, 2004].
Complementary strategies means that ∀s′i ∈ S ′ , s′i should
                                                                      We separate CSI’s competition strategy into 23 sub-
master a subset of problems Pi′ ⊆ P, such that ∀i ̸= j,
                                                                   strategies, which, along with CSI’s competition strategy, also
s′j ∈ S ′ cannot solve any problem in Pi′ quicker than s′i .
                                                                   serve as the initial strategies for Grackle. Among the 23 sub-
   Algorithm 1 outlines the strategy portfolio invention loop      strategies, nine are mainly used to show confluence, and 14
of Grackle, which invents strategies via a genetic algorithm       are used to show non-confluence. A comprehensive explana-
and parameter tuning with randomness. The variable Φ de-           tion of the division is shown in the technical appendix.
notes the current state, including information like all invented      We maintain the structure used in CSI’s competition strat-
strategies Φstrat , and the current generation of strategies       egy during the strategy invention because CSI relies on cer-
Φcur . The first phase is generation evaluation (evaluate). In     tain combinations of processors to (dis)prove confluence.
this phase, Grackle evaluates all strategies Φstrat in its port-   There are papers proving theorems for confluence analysis,
folio on the benchmark P. The evaluation results are stored        stating that if some properties of a TRS can be proved, then
in Φ to avoid duplicated execution.                                it is (non-)confluent. Such a theorem can be implemented
   Next, Grackle performs generation reduction (reduce). It        as a single processor, which checks whether the given TRS
assigns scores to every strategy in Φstrat based on the evalu-     satisfies the properties required by the theorem. However,
ation results in the previous phase. A configurable number of      not all such theorems are implemented as a processor. To
strategies with the highest scores becomes the current gener-      utilize such theorems, we need to combine CSI’s strategy
ation of strategies Φcur .                                         language and processors to perform transformations on the
   The third phase is strategy selection (select). It selects      original TRS and prove the necessary properties of the trans-
a strategy s from the current generation of strategies Φcur        formed problem. If we generate strategies randomly, it will be
based on certain criteria, which is then used to invent new        difficult to generate such useful structures and may produce
strategies. If no strategy can be selected, the algorithm termi-   unsound strategies due to inappropriate transformations.
nates.                                                                We search for three categories of parameters. First, we
   Finally, strategy specialization (specialize) invents a new     search for processor flags which do not violate the soundness
strategy s0 via specializing s over its best-performing prob-      guarantee. For instance, -development 6 in Section 1 is
lems Ps in P. Grackle then executes external parameter             a processor flag for the redundant processor. To ensure
tuning programs such as ParamILS [Hutter et al., 2009] or          soundness, we only search for flags of processors existing in
SMAC3 [Lindauer et al., 2022], tuning parameters for the se-       CSI’s competition strategy. Second, we include iteration pa-
lected strategy s with randomness. The goal is to invent a         rameters, such as time limits or repeated numbers of execu-
new strategy s0 such that it performs better than s ion Ps .       tion, to regulate the running of a certain sub-strategy. These
The new strategy s0 will be added to the portfolio Φ.              parameters are defined in CSI’s strategy language. More-
   Grackle employs the same approach to describe its pa-           over, we add a boolean execution-controlling parameter for
rameter search space as ParamILS. The space is described           some parallel or sequential executed sub-strategies, indicat-
by a set of available parameters, each of which is associ-         ing whether to run the particular sub-strategies in confluence
analysis. Assume a strategy A||B, where || denotes a par-              of function symbols. For each function symbol, an arity is
allel execution. The boolean parameters for A and B can rep-           randomly chosen between one and M
resent whether to run one, both, or neither of them.                      Another important parameter is the probability of generat-
   We need to construct a strategy for CSI using the parame-           ing a left-linear TRS L, which is associated with the likeli-
ters searched by Grackle. To achieve this, we start with CSI’s         hood of producing provably confluent TRSs. The majority of
competition strategy, replacing the processor flags and iter-          contemporary techniques for proving confluence are merely
ation parameters with relevant invented parameters. Then,              effective for left-linear TRSs. Without regulating the ratios
we disable sub-strategies according to the boolean execution-          of left-linearity, randomly generated TRSs rarely exhibit left-
controlling parameters.                                                linearity, making it theoretically difficult to show confluence
   The most challenging part of our work is the proper defi-           for them. We also notice that, in practice, CSI can merely
nition of the parameter space to confirm CSI’s soundness. As           prove confluence of very few generated TRSs if the ratios of
the exact definition is quite technical and verbose, we present        left-linearity are not controlled. By default, we force 60% of
the explanation of the parameter space and show an invented            generated TRSs to be left-linear.
strategy in the technical appendix.                                       Moreover, for a rule l → r, there is a parameter called
                                                                       CT related to the probability of generating l and r that are
3.2    Strategy Combination                                            complex terms. We need it because we prefer complex terms,
After inventing several complementary strategies, we want to           whereas constants and variables are quite simple.
combine them into a single strategy and compare it with the               Algorithm 2 presents the generation procedure of a single
competition strategy of CSI. The combination is performed              term. While choosing the root symbol, we first randomly
by choosing a few strategies from Grackle’s final portfolio            sample a value between zero and one and compare it with
and appropriately assigning a time limit to each of them.              comp to determine whether to only use funs as candidates
   To effectively divide the time, we split the whole one              for the root symbol. Here, comp is a value randomly cho-
minute into several time splits. Next, we greedily allocate            sen between zero and CT during the initialization stage of
a strategy to each time split in the sequence by order. Each           the generation of a TRS. If the comp is larger than one, we
newly chosen strategy aims at proving the largest number of            can only generate complex terms. Meanwhile, according to
remaining benchmark problems that have not been proved by              the definition of rewrite rules in Section A, the left term l in
the previously chosen strategies. We shuffle the sequence              l → r cannot be a variable. After choosing a root symbol for
100 times and greedily select strategies for each shuffled se-         the term t, we continuously choose new symbols for unde-
quence, resulting in strategy schedules comprising sequences           fined function arguments until all of them are defined. After
of pairs of strategies and time splits. To use a strategy sched-       selecting a new variable, we need to remove it from the set
ule, CSI executes each strategy in it by order for a duration of       of available variables if we are generating a left-linear TRS.
the relevant time split. We split the one-minute duration into         The size of the terms generated by us is at most 15, where the
many sequences and perform the greedy strategy selection for           size of a term is defined as the number of symbols in it. We
each. We finally choose the strategy schedule that maximizes           choose 15 as the maximum value because the sizes of most
the number of provable problems. The details of the strategy           terms in ARI-COPS are smaller than 15.
combination are explained in the technical appendix.                      To generate a rule l → r, we first execute Algorithm 2 to
                                                                       generate l and then execute it again to generate r. We extract
4     Dataset Augmentation                                             all used variables in l and mark them as available variables for
Although ARI-COPS is meticulously built by term rewriting              the generation of r, thereby Var (r ) ⊆ Var (l ), as required by
experts, it is unsuitable for AI techniques. First, it is relatively   the definition of rewrite rules in Section A.
small which is insufficient for contemporary AI techniques.               We repeatedly generate rewrite rules until they reach the
Second, there may be an imbalance in ARI-COPS because                  expected number and then return the newly generated TRS.
the problems come from rewriting literature. The examples
are often of theoretical interest and are constructed to illus-        4.2   Dataset Generation
trate specific confluence analysis techniques. However, TRSs
encountered in practical applications can contain redundant            We utilize the program explained in this section to construct
rules that are irrelevant to illustrating a certain property.          a large dataset, facilitating the application of AI techniques
                                                                       to confluence analysis. First, we randomly generate 100,000
4.1    TRS Generation Procedure                                        TRSs with the parameters of the maximum number of avail-
We develop a program to randomly generate a large dataset              able function symbols F = 12, constants C = 5, variables
of TRSs, receiving multiple parameters to control the overall          V = 8, and rules R = 15. Other parameters include the max-
generation procedure. First, the maximum number of avail-              imum arity of function symbols M = 8, the probability of
able function symbols F , constants C, variables V , and rules         generating left-linear TRSs L = 0.6, and the value related to
R establish the upper bound of the respective quantities of            the possibility of generating complex terms CT = 1.6.
symbols and rules. For each of F , C, and V , a value is ran-             However, the randomly generated dataset can be imbal-
domly selected between zero and the specified maximum, de-             anced. First, there may be significant differences in the
termining the actual number of available symbols. The actual           number of confluent, non-confluent, and indeterminate TRSs.
number of rules is randomly chosen between one and R. Sec-             Second, the number of TRSs mastered by different conflu-
ond, we define a parameter M , used during the initialization          ence analysis techniques may vary considerably.
Algorithm 2 Term Generation                                         300
Input: consts, vars, funs                                           250
        comp, the likelihood of making a complex term
        left, whether the term is on the rewrite rule’s left side   200
        linear, whether to construct a linear term
Output: a term t                                                    150
 1: if random(0, 1) < comp then                                     100
 2:    root symbols ← funs
 3: else if left then                                                50
 4:    root symbols ← funs + consts
 5: else                                                                0
                                                                            0 1 2 3 4 5 6 7 8 9 1011121314151617181920212223
 6:    root symbols ← funs + consts + vars
 7: end if                                                          Figure 1: The number of TRSs solved most quickly (y-axis) for each
 8: t ← random choose one(root symbols)                             labeling strategy (x-axis). Two labeling strategies that do not master
 9: undefs ← undefined function arguments in t                      any problems are ignored in the x-axis.
10: while undefs is not empty do
11:    for all undef ∈ undefs do                                    labeling, we will not be able to understand whether a TRS
12:       sym ← random choose one(funs + consts +                   is mastered by one of the two important confluence analy-
          vars)                                                     sis techniques. The details of the two new labeling strate-
13:       replace the undefined function argument corre-            gies are explained in the technical appendix. The time limit
          sponding to undef in t with sym                           for using CSI’s competition strategy as a labeling strategy is
14:       if linear and is var(sym) and left then                   one minute. The time limit for other labeling strategies is
15:          remove sym from vars                                   30 seconds, smaller than one minute because the execution
16:       end if                                                    of decomposed sub-strategies is more efficient. We calculate
17:    end for                                                      the number of problems most quickly solved by each label-
18:    undefs ← undefined function arguments of t                   ing strategy. The details of labeling strategies are presented
19: end while                                                       in the technical appendix. The randomly generated dataset
20: return t                                                        is quite imbalanced, four strategies master more than 1,000
                                                                    problems; however, 16 strategies master less than 250 prob-
                                                                    lems. To address the imbalance, we randomly choose at most
   We develop a multi-step procedure to build a relatively bal-
                                                                    300 problems for a strategy from its set of mastered problems.
anced dataset. First, we execute CSI’s competition strategy
                                                                    We also randomly add 1,200 problems that cannot be solved
on all generated TRSs for one minute using a single CPU. CSI
                                                                    by any labeling strategy to the dataset.
outputs NO, YES, and MAYBE for 69317, 25012, and 5671
                                                                       Finally, we obtain a dataset of 5,267 TRSs. Within this
TRSs, respectively.
                                                                    dataset, 1,647 TRSs are classified as confluent, 1,910 as non-
   Second, we randomly choose 5,000 problems from each
                                                                    confluent, and 1,710 as indeterminate when evaluated by CSI
set of problems classified as NO, YES, and MAYBE by CSI.
                                                                    using a single CPU within a one-minute time limit.
   Third, we execute the duplicate checker used in CoCo 2024           Figure 1 shows the final distribution of the number of prob-
to remove the duplications in the 15,000 chosen TRSs and            lems mastered by each labeling strategy. It is not perfectly
566 ARI-COPS TRSs. It checks the equivalence of syntac-             balanced; however, we consider it relatively balanced, given
tical structures between TRSs modulo renaming of variables          that certain strategies can only master problems that satisfy
and a special renaming on function symbols of their signa-          particular properties. Such properties can be uncommon in
tures. If TRSs of an equivalence class occur both in the            randomly generated TRSs and practical applications.
randomly generated dataset and ARI-COPS, we only remove                There are infinitely many strategies that can be chosen as
those randomly generated TRSs.                                      labeling strategies, such as strategies obtained by changing
   Fourth, we want to mitigate the imbalance in the number          processor flags. We do not choose other labeling strategies as
of problems mastered by different confluence techniques. We         we have already decomposed CSI’s competition strategy, en-
execute 26 strategies for all TRSs, aiming at labeling each         abling us to label problems with all categories of confluence
of them with the most effective strategy. The labeling strate-      analysis techniques implemented in CSI. Further decomposi-
gies contain all initial strategies for Grackle, which are ex-      tion or modification of processor flags may allocate problems
plained in Section 3.1. The other two that are used to prove        to different labeling strategies that only slightly differ.
confluence are extracted from two complicated initial strate-
gies, both consisting of many sub-strategies and integrated
with transformation techniques that potentially simplify the        5       Experiments
search for proofs. Specifically, the two complicated initial        We evaluate our strategy invention method on ARI-COPS
strategies parallelly execute two important confluence analy-       and a combination of the randomly generated TRSs and ARI-
sis techniques, development closedness [Van Oostrom, 1997]          COPS datasets. In both datasets, CSI with invented strategies
and decreasing diagrams [Van Oostrom, 1994], not used by            outperforms CSI with the competition strategy, the state-of-
the other initial sub-strategies. If we do not use them for         the-art approach in confluence analysis for TRSs.
                             ARI-COPS         augment                                  comp            total        combine
                                                                                                                                   CoCo
               CPU             1    4         1    4                        CPU       1    4         1       4      1     4
                 init        475 477         846 852                        yes      266 272        271 277        271 276          272
                total        479 484         873 871                         no      203 205        208 207        207 207          205
               confs          73   93        92 104                        solved    469 477        479 484        478 483          477
            both in final      6    2        22    12
                                                                         Table 2: Numbers of solved TRSs on ARI-COPS. The column comp
Table 1: Statistics of Grackle’s training procedure. The rows init and   represents CSI’s competition strategy, total shows the total number
total denote the number of problems solved by Grackle’s initial strat-   of problems proved by all invented strategies, and combine denotes
egy and the number of problems solved by strategies in Grackle’s         combining invented strategies as a single strategy. CoCo denotes the
final portfolio, respectively. The row confs denotes the number of       results obtained by CSI in CoCo 2024.
strategies that remains in Grackle’s final portfolio. The row both in
final represents the number of strategies in the final portfolio that                          never by CSI           never in CoCo
master both confluence and non-confluence of TRSs.                             CPU          yes no solved           yes no solved
                                                                                 1           2     3      5          1     3      4
5.1    Experimental Settings                                                     4           4     2      6          1     2      3
                                                                                1&4          6     3      9          2     3      5
The ARI-COPS 2024 dataset comprises a total of 1,613 prob-                    1-CeTA         0     3      3          0     3      3
lems of which 566 are TRS problems. We focus on evaluat-                      4-CeTA         1     0      1          0     0      0
ing our approach on TRS problems since they are standard                     1&4-CeTA        1     3      4          0     3      3
term rewriting problems for confluence analysis and repre-
sent the major category in ARI-COPS. Another evaluation                  Table 3: Numbers of TRSs solved by all strategies in Grackle’s final
dataset consists of data from both ARI-COPS and our ran-                 portfolio that have never been solved by all versions of CSI or any
domly generated datasets in Section 4.2. For training pur-               tool in CoCo. The suffix CeTA denotes the proofs can be certified
poses, we arbitrarily select 283 examples from ARI-COPS                  by CeTA. The notion 1&4 means the union of all strategies invented
and 800 examples from the randomly generated dataset. To                 by employing one CPU and four CPUs per strategy execution.
build the test dataset, we exclude the examples in the train-
ing dataset, subsequently randomly selecting 800 examples
from the randomly generated dataset and the remaining 283                some strategies that are only effective with enough computa-
examples from ARI-COPS.                                                  tion resources. The final augmented portfolios contain more
   The Grackle time limit for proving a TRS is 30 seconds,               strategies that master both confluence and non-confluence of
employed both in the evaluation and the strategy special-                TRSs. The likely reason is that a larger dataset makes train-
ization phases. During the specialization phase, Grackle                 ing slower, and it is more difficult for Grackle to find optimal
launches ParamILS for parameter tuning. The overall time                 strategies for particular theoretical properties of TRSs.
limit for one strategy specialization phase is 45 minutes. The              Table 2 compares the invented strategies with CSI’s com-
total execution time of Grackle is two days. Grackle performs            petition strategy. With a single CPU per each strategy evalua-
parallel execution in both the evaluation and specialization             tion, Grackle’s final portfolio proves ten more problems than
phases; thus, we also limit the number of CPUs it can use.               CSI’s competition strategy. With four CPUs, total proves
For each dataset, we perform two Grackle runs, configuring               seven more problems than comp.
the numbers of available CPUs for a single strategy run to be               The invented strategies additionally (dis)prove several
either one or four. When it is set to one and four, the total            TRSs that have never been proved by different versions of
number of available CPUs for Grackle is set to 52 and 66, re-            CSI or all CoCo’s participants, as depicted in Table 3. In to-
spectively. Here, a CPU denotes a core of the AMD EPYC                   tal, we show (non-)confluence for nine TRSs that could not
7513 32-core processor. Grackle’s portfolio stores at most               be solved by any versions of CSI. Five of the nine new proofs
200 of the best strategies.                                              have never been proven by all CoCo’s participants.
   The use of four CPUs has been selected to match the results              We combine the invented strategies as a single strategy to
of CSI’s competition strategy in CoCo 2024 on the competi-               compare it with CSI’s competition strategy. The number of
tion setup. Given exactly the same problems solved by CSI                time splits and the exact time assigned for each invented strat-
in our own setup described above with four CPUs and in the               egy are presented in the technical appendix. With single and
CoCo competition in their Starexec [Stump et al., 2014] setup            four CPUs, combine proves nine and six more problems than
we consider the further comparisons in the paper fair.                   the competition strategy, respectively.
                                                                            When using one CPU, we gain more improvements over
5.2    Experimental Results                                              CSI’s competition strategy compared to using four CPUs. A
Performance on ARI-COPS. Table 1 depicts the statis-                     likely reason is that our strategy invention approach is partic-
tics of Grackle’s training procedure. The value total shows              ularly good at generating efficient strategies. With four CPUs,
the number of solved TRSs after the training, while init is              CSI can run several processors in parallelly, effectively reduc-
the number solved by the initial strategies. When using four             ing the runtime.
CPUs, Grackle’s final portfolio contains more strategies than            Certification. First, we check whether the answers found
those in the final portfolio generated using one CPU. A prob-            by the invented strategies are consistent with the answers dis-
able reason is that executing with four CPUs can discover                covered in CoCo. Second, we execute CeTA to verify the
                          comp          combine                     and Toyama, 2012], is defined in CSI’s competition configu-
               CPU       1    4         1     4                     ration document. CSI’s competition strategy executes AT in
               yes      403 412        412 418                      parallel with many other sub-strategies, reducing the compu-
                no      399 442        450 449                      tational resources allocated to it and failing to find a proof.
              solved    802 854        862 867                         Another example is similar to that in Section 1, we dis-
                                                                    cover that if CSI employs redundant -development
Table 4: Numbers of solved TRSs on the testing examples of the      6 to generate redundant rules in the competition strategy, it
augmented dataset.
                                                                    can disprove confluence for 852.ari (997.trs in COPS),
                                                                    and the proof can be certified by CeTA.
proofs for the newly solved problems. Table 3 depicts the
number of newly solved problems certifiable by CeTA. If we
cannot certify the proofs due to the limitation of CeTA and
                                                                    7   Related Work
CSI as explained in Section 2.2, we analyze the related strate-     There have been several attempts to apply machine learning
gies. We aim to understand what changes they perform to the         to rewriting; however, none have been applied to automatic
original strategy lead to the proofs. From the analysis, we         confluence provers. While [Winkler and Moser, 2019] inves-
either slightly modify the sub-strategy defined in the compe-       tigate feature characterization of term rewrite systems, they
tition strategy or directly use some existing sub-strategies to     do not build any learning models based on the features. There
produce the same answers as the invented strategies. These          are works analyzing the termination of programs using neu-
modifications that lead to the answers are employed in the          ral networks to learn from the execution traces of the pro-
corresponding invented strategies, which are small and sound        gram [Giacobbe et al., 2022; Abate et al., 2021]. Neverthe-
according to our knowledge of term rewriting. We also check         less, they do not transform programs to term rewrite systems
the certification errors output by CeTA to figure out whether       and apply machine learning to guide automatic term rewriting
they are indeed errors or just caused by limitations of CSI and     tools in termination analysis. MCTS-GEB [He et al., 2023]
CeTA. Third, for each strategy in Grackle’s final portfolio, we     applies reinforcement learning to build equivalence graphs
run CSI on its mastered problems and apply CeTA to verify           for E-graph rewriting, but it focuses on optimization prob-
the proofs. Only 234 and 226 proofs can be verified when            lems, not on confluence.
one and four CPUs are employed for strategy invention, re-             There has been extensive research on parameter tuning and
spectively. We manually check the proofs that cannot be ver-        strategy portfolio optimization in automated reasoning. Hy-
ified by CeTA. The details of our certification procedures are      dra [Xu et al., 2010] employs a boosting algorithm [Fre-
shown in the technical appendix.                                    und and Schapire, 1997] to select complementary strategies
Performance on the augmented dataset. Table 1 also                  for SAT solvers. [Ramı́rez et al., 2016] propose an evolu-
summarizes Grackle’s training procedure in the augmented            tionary algorithm for strategy generation in the SMT solver
dataset. Compared to the training in ARI-COPS, Grackle’s            Z3 [De Moura and Bjørner, 2008]. A comprehensive review
final portfolios consist of more strategies. The likely reason is   of these approaches is provided by [Kerschke et al., 2019].
that the augmentation dataset comprises more examples, ne-
cessitating more diverse strategies to cover them. We notice
that with one CPU, the invented strategies prove more prob-         8   Conclusion and Future Work
lems than those invented with four CPUs. This is probably           We have proposed an approach to automatically invent strate-
caused by the randomness in the strategy invention.                 gies for the state-of-the-art confluence analysis prover CSI.
    The results of the evaluation in the test dataset are pre-      We have performed data augmentation by randomly gener-
sented in Table 4. With one and four CPUs, combine respec-          ating a large number of term rewrite systems and mixing
tively proves 60 and 13 more problems than comp. Notice             these with the human-built dataset ARI-COPS. We have eval-
that here the training examples are disjoint from the testing       uated the invented combined strategy both on the original
examples, whereas in the evaluation for ARI-COPS, they are          ARI-COPS dataset and the augmented dataset. The invented
the same. From this, we can conclude that our invented strate-      strategies discover significantly more proofs than CSI’s com-
gies generalize well to unseen data. With four CPUs, the uni-       petition strategy on both datasets. Notably, five of the human-
fied strategy proves more problems than using one CPU. The          written problems have never been proved by any automatic
likely reason is that the invented strategies with four CPUs        confluence provers in the annual confluence competitions.
can discover proofs more quickly, leading to a stronger uni-
                                                                       Future work includes applying machine learning to indi-
fied strategy within the one-minute time limit.
                                                                    vidual term-rewriting techniques, for example those that per-
                                                                    form search in a large space. Prioritizing the more promising
6   Examples                                                        parts of the search space could improve the individual tech-
Besides the example in Section 1, we present two more ex-           niques. Our strategy invention approach could also be ex-
amples of the invented strategies that (dis)prove problems un-      tended to other automatic term rewriting provers. It would
provable by any participant in CoCo.                                also be possible to apply neural networks to directly pre-
   The core structure of the first example is AT. It proves con-    dict appropriate strategies for automatic term rewriting tools,
fluence for 794.ari in ARI-COPS (939.trs in COPS).                  however, soundness of proofs generated using such an ap-
The sub-strategy AT, denoting Aoto-Toyama criteria [Aoto            proach remains a major challenge.
Acknowledgements
This research was supported by the ERC PoC project Formal-
Web3 no. 101156734, the University of Innsbruck doctoral
scholarship promotion of young talent, the National Natural
Science Foundation of China 92370201, and the Czech Sci-
ence Foundation project no. 24-12759S.
A     Term Rewriting                                                                   The TRS A = {f (x) → g(f (x)), g(y) → f (g(y))} is not
                                                                                    terminating, as it allows the infinite rewrite sequence f (x) →
We explain the essential concepts of term rewriting in this
                                                                                    g(f (x)) → f (g(f (x))) → · · · . This sequence is infinite
section.
                                                                                    because the term f (x) within g(f (x)) can be rewritten back
   Various types of rewrite systems exist based on the formal-
                                                                                    to g(f (x)), resulting in an infinite loop.
ization of objects, with the simplest being the abstract rewrite
system (ARS).                                                                       Definition 9 (confluence). A TRS R is confluent if and only
                                                                                    if ∀s, t, u ∈ T (F, V), s →∗R t ∧ s →∗R u ⇒ t ↓R u.
Definition 2. An ARS is a pair A = (A, →) of a set A and a
binary relation → on A.                                                                The TRS B = {f (x, x) → a, f (x, g(x)) → b, c → g(c)}
                                                                                    is not confluent, as it permits the following rewrite sequences:
  A (possibly infinite) rewrite sequence is a sequence a0 →                         a ← f (c, c) → f (c, g(c)) → b. Since no rules can be applied
a1 → · · · such that ai ∈ A. We write a →∗ b if there is a                          to a and b, convergence between them is not achievable.
rewrite sequence a → · · · → b.                                                        A term is called linear if no variable multiply occurs in it.
Definition 3. An ARS (A, →) is terminating if ∀a ∈ A, there                         A rewrite rule l → r is called left-linear if l is linear. A TRS is
are no infinite rewrite sequences starting from a.                                  called left-linear if all its rules are left-linear. Left-linearity is
                                                                                    crucial for confluence analysis since most existing confluence
  The notation a ↓ b denotes that a and b are joinable, mean-
                                                                                    analysis techniques depend on it to determine the confluence
ing that there exists an element c ∈ A such that a →∗ c and
                                                                                    of TRSs. In this paper, a term is called compositional if it is
b →∗ c.
                                                                                    neither a variable nor a constant.
Definition 4. An ARS (A, →) is confluent if ∀a, b, c ∈ A with                          We will also explain some rewriting concepts that are im-
b ←∗ a →∗ c, we have b ↓ c.                                                         portant for the understanding of the parameter space in Sec-
   Consider an abstract reduction system (ARS) E = (E, →),                          tion D. However, our parameter involves an extensive num-
where E = {a, b, c, d} and →= {(a, b), (b, d), (c, b), (d, c)}.                     ber of rewriting techniques. Explaining all basic rewriting
The ARS E is non-terminating as it admits an infinite rewrite                       concepts requires extremely large amount of work, which is
sequence: c → b → d → c → · · · .                                                   beyond the scope of our paper. Moreover, a lot of definitions
   Term rewrite systems (TRSs) extend ARS by incorporating                          or theorems rely on previous definitions and theorems. Pre-
first-order variables and employing first-order terms.                              senting all the dependent also necessiate too much work for
   We then define the notions of rewriting terms using con-                         us.
texts and holes.                                                                       We recommend readers to read some textbooks [Baader
                                                                                    and Nipkow, 1998; Bezem et al., 2003] for the concepts that
Definition 5. A hole is defined as a special symbol □ ∈                     / F,    they cannot understand.
and a context C is a term that contains exactly one hole. The                          You may skip the following definitons and theorems if you
notion C[t] denotes the application of the term t to the context                    can get a feeling of our parameter space.
C, which is defined as follows:
                                                                                          A.1 Basic Termination Techniques
           t                                      if C = □                                 To prove termination, many techniques try to discover a well-
C[t] =
           f (t1 , . . . , C ′ [t], . . . , tn ) if C = f (t1 , . . . , C ′ , . . . , tn ) founded monotone algebra that is compatible with the given
                                                                                           TRS. The crucial part is the discovery of interpretations. De-
Definition 6. The set of variables in a term t is defined as                               pending on their formats, there are integer interpretations,
                       
                           {t}                  if t is a variable                         polynomial interpretations, matrix interpretations, etc.
                       
                                                                                           Definition 10 (interpretation). Let F be a signature. An F-
                       
                       
        Var (t) = ∅n                            if t is a constant
                            S                                                              algebra    A is a set A equipped with operations fA : An → A
                        V ar(ti ) if t = f (t1 , . . . , tn )
                       
                                                                                          for every n-ary function symbol f ∈ F. The underlying set A
                           i=1
                                                                                           is called the carrier of A and fA is called the interpretation
Definition 7. A rewrite rule for terms l and r is written as                               of f .
l → r where l ∈      / V and V ar(r) ⊆ V ar(l). A term rewrite                             Definition 11. Let A be an arbitrary algebra. We inductively
system R consists of a set of rewrite rules. Consider the TRS                              define a mapping [·]A from the set of ground terms to A as fol-
R, we write the rewrite relation t →R u for terms t, u if                                  lows: [f (t1 , ..., tn )]A = fA ([t1 ]A , . . . , [tn ]A). In particular,
there exists a rewrite rule l → r ∈ R, a context C, and a                                  if t is a constant then [t]A = tA .
substitution σ such that t = C[lσ] and u = C[rσ].
                                                                                           Definition 12 (well-founed relation). Let R be a relation on
   We write →∗R to denote the transitive-reflexive closure of                              a set A. A relation R is called well-founded if there are no
→R . Similar to ARSs, we obtain the definitions of rewrite                                 infinite descending sequences a1 Ra2 Ra3 R · · · of elements of
sequences and ↓R for TRSs. We drop the subscript R for the                                 A.
relations on terms in the subsequent sections if it is contextu-                           Definition 13 (monotone algebra). A monotone F-algebra
ally inferrable.                                                                           (A, >) consists of a non-empty F-algebra A and a proper
Definition 8. A TRS R is terminating if ∀t ∈ T (F, V), there                               order > on the carrier A of A such that every algebra op-
is not any infinite rewrite sequence t → t1 → · · · starting                               eration is strictly monotone in all its coordinates, i.e., if
from t.                                                                                    f ∈ F has arity n ≥ 1 then fA (a1 , . . . , ai , . . . , an) >
fA (a1 , . . . , b, . . . , an ) for all a1 , . . . , an , b ∈ A and i ∈      PosV (t) denotes the positions of variables in the term t.
1, . . . , n with ai > b. We call a monotone F-algebra (A, >)              PosF (t) denotes the positions of function symbols in the
well-founded if > is well-founded.                                         term t.
Theorem 1. A TRS is terminating if and only if it is compat-               Definition 19 (Overlap). An overlap of a TRS (F, R) is a
ible with a well-founded monotone algebra.                                 triple ⟨l1 → r1 , p, l2 → r2 ⟩ satisfying the following proper-
Example 1. Consider the TRS R1 consisting of the single                    ties:
rewrite rule f (f (x, y), z) → f (x, f (y, z)) Let (A, >) =                  1. l1 → r1 and l2 → r2 are variants of rewrite rules of R
(N, >N ), the set of natural numbers equipped with the usual                     without common variables,
order, and define fA (x, y) = 2x + y + 1 for all x, y ∈ N.                   2. p ∈ PosF (l2 )
The operation fA is strictly monotone in both coordinates: if
x >N x′ and y >N y ′ then 2x+y+1 >N 2x′ +y+1 and 2x+                         3. l1 and l2 |p are unifiable,
y+1 >N 2x+y ′ +1. We have fA (fA (x, y), z) = 4x+2y+z+                       4. if p = ϵ then l1 → r1 and l2 → r2 are not variants.
3 > N2x + 2y + z + 2 = fA (x, fA (y, z)) for all x, y, z ∈ N.
                                                                           Definition 20 (Critical Pair). Suppose ⟨l1 → r1 , p, l2 → r2 ⟩
Hence [α]A (f (f (x, y), z)) >N [α]A (f (x, f (y, z))) for every
                                                                           is an overlap of a TRS R. Let σ be a most general unifier of l1
assignment α, yielding the termination of R1
                                                                           and l2 |p . The term l2 σ[l1 σ]p = l2 σ can be rewritten in two
                                                                                                         l →r                        l →r
A.2    Basic Confluence Techniques                                                                      1
                                                                           different ways: l2 σ[r1 σ]p ←−   1
                                                                                                          −−−                     2
                                                                                                              l2 σ[l1 σ]p = l2 σ −−   2
                                                                                                                                    −−→
                                                                                                            p                           ϵ
One typical way of proving confluence is first proving termi-              r2 σ We call the quadruple (l2 σ[r1 σ]p, p, l2 σ, r2 σ) a critical
nation and then proving local confluence.                                  peak and the equation l2 σ[r1 σ]p ≈ r2 σ a critical pair of R,
Definition 14 (local confluence). Let R be a TRS. An element               obtained from the overlap ⟨l1 → r1 , p, l2 → r2 ⟩.
a ∈ T is locally confluent if for all elements b, c ∈ T with               Example 2. Let the TRS R have two rules f (a, g(x)) →
b → a → c we have b ↓ c. The TRS T is locally confluent if                 f (x, x) and g(b) → c. We have an overlap ⟨g(b) →
all its elements are locally confluent.                                    c, 2, f (a, g(x)) → f (x, x)⟩. It gives rise to the critical
Theorem 2 (Newman’s Lemma). Every terminating and lo-                                       2             ε
                                                                           peak f (a, c) ← − f (a, g(b)) −→ f (b, b) and the critical pair
cally confluent TRS is confluent.                                          f (a, c) ≈ f (b, b).
A.3    Basic Non-confluence Techniques                                        To disprove confluence of a TRS R, we consider peaks of
We want to introduce critical pairs since they are crucial for             the form
non-confluence analysis.                                                                     t ←≤m t1 ← s → u1 →≤n u
                                                                           such that t1 = s[r1 σ]p ← s[t1 σ]p = s = s[t2 σ]q →
Definition 15 (substitution). A substitution is a mapping σ
                                                                           s[r2 σ]q = u1 with t1 → r1 , t2 → r2 ∈ R, q ≤ p, and
from V to T (F, V). The application of the substitution σ to
                                                                           p ∈ Pos(s[t2 ]q). The basic idea is to show non-joinability
the term t is defined as:
                                                                           of t and u. In order to test non-joinability of t and u we con-
                                                                           sider ground instances of t and u. Here, ground instances
              
                σ(t)                   if t ∈ V
        tσ =                                                               mean substituting all variables with constants. Let cx be a
                f (t1 σ, . . . , tn σ) if t = f (t1 , . . . , tn )
                                                                           fresh constant for every variable x and let t̂ denote the result
Definition 16 (unifiability). Two terms s and t are unifiable              of replacing every variable in a term t with the corresponding
if there exists a substitution σ such that σs = σt.                        constant. Since for terms s and w we have s →R w if and
                                                                           only if ŝ →R ŵ, it follows that terms t and u are joinable if
Definition 17 (variant). A variable substitution is a substitu-
                                                                           and only if t̂ and û are joinable. To test non-joinability of t̂
tion from V to V. A renaming is a bijective variable substi-
                                                                           and û we overapproximate the sets of reducts for t̂ and û and
tution. A term s is a variant of a term t if s = tσ for some
                                                                           check if the intersection of these sets is empty.
renaming σ.
Definition 18 (Position).                                                  B    CSI Strategy Language
                                                                           Besides the technical appendix, [Nagele et al., 2017] also ex-
             
             {ϵ} if t is a variable
  Pos(t) = {ϵ} ∪ {ip|1 ≤ i ≤ n and p ∈ P os(ti )}                          plains CSI’s strategy language.
                                                                           Overall Grammar A strategy is defined by the grammar
             
                 if t = f (t1 , . . . , tn )
                                                                           s ::= m | (s) | c | i | e
  Let p ∈ Pos(t). The subterm of t at position p is denoted                e ::= s% | s! | s[f] | {s}o
by t|p , i.e.,                                                             i ::= s? | s* | s+ | sn* | s[f]*
               
                 t if p = ϵ                                                c ::= s;s | s|s | s||s
         t|p =                                                                      | if p then s else s
                 ti |q if t = f (t1 , . . . , tn ) and p = iq
                                                                           where s expresses the possible strategies of CSI, m denotes
The symbol t(p) at position p in t is defined as t(p) =                    the name of any available processor, p denotes the name of
root(t|p ). We partition the set Pos(t) into PosV (t) = {p ∈               any available predicate, and c, i, and e define the available
Pos(t)|t|p ∈ V} and PosF (t) = Pos(t) \ P osV (t).                         combinators, iterators, and specifiers. Here combinators are
used to combine two strategies whereas iterators are used to            • s[f]: Tries to modify a given problem via s for at most
repeat a given strategy a designated number of times. In con-             f seconds. If s does not succeed or fail within f sec-
trast, specifiers are used to control the behavior of strategies.         onds, s[f] fails. Otherwise s[f] returns the resulting
A strategy works on a confluence problem. Whenever CSI                    problem. Hence it succeeds (fails) if s succeeds (fails).
executes a strategy, internally, a so-called proof object is con-       • {s}o: Applies s to the given problem. If s fails, {s}o
structed which represents the actual proof. Depending on the              fails. Otherwise, the modifier o is applied to the result-
shape of the resulting proof object after applying a strategy s,          ing problems.
we say that s succeeded or s failed. This should not be con-
fused with the possible answers of the prover: YES, NO, and         Configuration File Since strategies can get quite complex,
MAYBE. Here YES means that confluence could be proved,              CSI provides the possibility to specify a config file. A config
NO indicates a successful non-confluence proof, and MAYBE           file consists of a sequence of abbreviations of the form N =
refers to the case when confluence could neither be proved          s where N defines its name and s the strategy (in principle
nor disproved. On the success of a strategy s, it depends on        arbitrary text) it should expand to. The convention is to use
the internal proof object whether the final answer is YES or        all capital names for abbreviations. Each abbreviation has
NO. On failure, the answer is always MAYBE. Based on the            to be put on a separate line. You can spread a strategy over
two possibilities success or failure, the semantics of the strat-   several lines by terminating each line with a \. Last but not
egy operators is as follows.                                        least, you can add comments to config files by putting a # in
                                                                    front of each line.
Combinators
   • s;s’: First applies s to the given problem. If this fails,     C    Default Strategy
     then s;s’ fails. Otherwise s’ is applied to the resulting      This section explains the workflows of CSI’s default com-
     problems.                                                      petition strategy. In the CoCo competition, CSI’s execution
   • s|s’: Applies s to the given problem. If this succeeds,        command is roughly csi -C CR -s AUTO -c x.trs.
     its result is returned. Otherwise s’ is applied to the         Here, -C CR denotes to prove (non-)confluence for a TRS.
     given problem.                                                 CSI is based on the termination tool TTT2 [Korp et al., 2009]
   • s||s’: Runs s and s’ in parallel on the given prob-            since some confluence techniques need to first prove termi-
     lem. As soon as at least one of s and s’ succeeds, the         nation. There are also other flags for -C to prove different
     resulting problem is returned.                                 properties of TRSs. The flag -s AUTO means that CSI ex-
                                                                    ecutes the AUTO strategy below in the default configuration
   • if p then s else s’: Applies s to the given                    document. Finally, x.trs means to prove (non-)confluence
     problem if p is satisfied by the underlying problem. Oth-      for the TRS x. In ARI-COPS, the TRSs are represented by
     erwise s’ is applied.                                          the .ari format. However, CSI cannot receive .ari docu-
Iterators                                                           ments currently. We need to first execute a tool [James and
   • s?: Applies s to the given problem. On success, its            Fabian, 2023] to convert .ari documents to the correspond-
     result is returned. Otherwise, the original problem is re-     ing .trs documents.
     turned and unmodified.                                         AUTO = ( i f t r s t h e n ( \
   • s*: Applies s recursively to the given problem until it          s o r t e d − o r d e r * ; ( AUTO INNER \
     cannot be modified anymore. Note that s* is always                   | | (NOTCR | REDUNDANT FC ) 3 * ! ) \
     successful.                                                     ) else fail )
   • s+: Applies s recursively to the given problem until             AUTO works as below:
     it cannot be modified anymore. I.e., s+ is successful           1. Check whether the given problem is a TRS problem.
     if it can prove or disprove termination or confluence of           There are many different rewrite systems that can be in-
     the given problem. Otherwise, it fails. Note that s+ =             put to CSI like higher-order rewrite systems, etc. CSI
     s*;s but s+ is not equivalent to s;s*.                             fails if it is not a TRS problem.
  • sn*: Applies s recursively to the given problem until            2. If it is, the default strategy uses ordered sorted decom-
    it cannot be modified anymore or s has been applied n               position [Felgenhauer et al., 2015] to try to decompose
    times. Note that sn* is always successful.                          the given TRS problem to a set of sub-problems. The
  • s[f]*: Applies s recursively to the given problem until             original TRS is confluent if and only if all decomposed
    it cannot be modified anymore or f seconds are elapsed.             problems are confluent [Felgenhauer et al., 2015].
    Note that s[f]* is always successful.                            3. AUTO INNER and (NOTCR | REDUNDANT FC)3*!
Specifiers                                                              are parallelly executed. AUTO INNER mainly fo-
                                                                        cuses on proving confluence, while (NOTCR |
   • s%: Applies s to the given problem. If s fails, the com-           REDUNDANT FC)3*! focuses on disproving conflu-
     putation is aborted and s% fails. Otherwise, it succeeds.          ence. (NOTCR | REDUNDANT FC)3*! first uses
   • s!: Applies s to the given problem. If s proves or dis-            NOTCR to determine whether the given problem is non-
     proves termination or confluence of the given problem,             confluence, if it can be determined, the answer will
     s! is successful. Otherwise, it fails.                             be returned. Otherwise, it applies REDUNDANT FC
      which executes the redundant rule technique [Nagele                flag. If PRETRS matrix ib chooses the value 6, we
      et al., 2015] to transform the given TRS. (NOTCR                   may obtain matrix -ib 6.
      | REDUNDANT FC) is repeatedly applied for at most              • name time or name loop. It belongs to iteration param-
      three times to discover an answer. The specifier ! is cru-       eters. They are used to control the execution time or
      cial since the transformation of REDUNDANT FC may                the number of repeated application times of a strategy.
      be successful, but it does not discover a nonconfluence          They control the values of the specifiers. For instance,
      proof. According to the explanation in Section B, CSI            if PRETRS time is set to 2, we generate the strategy
      will return YES in this case if we do not use !. The             PRETRS = content of PRETRS[2].
      details of NOTCR and REDUNDANT FC are explained in
      Section D.                                                   D.2    Details of Patameters
AUTO INNER = \                                                     In this Section, we explain the strategies in CSI’s competition
    ( AUTO INNER0 [ 3 0 ] | CPCS [ 5 ] 2 * ) ! | \                 strategy document, following its structure sequentially from
    ( { AUTO INNER0 [ 3 0 ] } nono \                               the beginning to the end. The explanations of a flag and its
        | CPCS [ 5 ] 2 * ) 2 * !                                   soundness will be ignored if we have explained them in the
                                                                   previous strategy definitions. After searching for the parame-
   The definition of AUTO INNER is shown above. It                 ters, we convert the parameters into a configuration document
first tries to discover a proof using AUTO INNER0. If it           which is used by CSI. The structures of strategies generally
cannot discover a proof, the critical pair closing system          remain the same to confirm soundness, meaning that besides
(CPCS) [Oyamaguchi and Hirokawa, 2014] transformation is           the newly discovered parameters, we do not change the pro-
applied. Then AUTO INNER0 is executed again. Notice that           cessors and the order of their applications. We give examples
the second AUTO INNER0[30]nono uses nono to ignore                 to explain how to keep the structures in this section later via
the proof for nonconfluence produced by AUTO INNER0                examples.
because after the CPCS transformation, we cannot produce              We ignore the processor flags not searched by us since the
sound proofs for nonconfluence [Oyamaguchi and Hirokawa,           number of them is indeed intensive, and presenting all expla-
2014].                                                             nations is too verbose. We recommend executing CSI’s help
AUTO INNER0 = (GROUND | | KB | | AC | | \                          function to understand the details.
  (REDUNDANT DEL ? ; ( CLOSED | | DD \
                                                                   PRETRS = ( ( \
       | | SIMPLE | | KB | | AC \
                                                                    m a t r i x −dim   1 −ib    3 −ob    5 | \
       | | {GROUND} nono ) ) 3 * ! \
                                                                    m a t r i x −dim   2 −ib    2 −ob    3 | \
  | | ( ( ( CLOSED | | DD) \
                                                                    m a t r i x −dim   3 −ib    1 −ob    1 | \
     | REDUNDANT RHS) 3 * ! \
                                                                    m a t r i x −dim   3 −ib    1 −ob    3)[2]*)
  | | (CLOSED | | DD) \
     | REDUNDANT JS ) 3 * ! | | KH \                                  It preprocesses the TRS before trying to discover a termi-
  | | AT | | SIMPLE | | CPCS2 | | \                                nation proof. The preprocess tries to reduce the size of the
 fail )                                                            original TRS by removing some rules from it. The parameter
  The above code explains the details of AUTO INNER0. It           space for PRETRS is presented below.
parallelly executes various techniques. The details of all tech-     • PRETRS {yes, no}. PRETRS can be chosen as yes
niques are explained in Section D.                                     or no. When it is set as no, we replace its defini-
                                                                       tion with fail, i.e. PRETRS = fail. The proces-
D     Parameter Space                                                  sor fail means the processor simply fails. Replacing
                                                                       it with fail is sound since it is only used in SN. It is
D.1    Overall Patterns                                                (PRETRS;(...). According to the definition of ;,
The name of a parameter often follows one of the patterns:             replacing it with fail only makes the strategy for ter-
  • abbreviation such as PRETRS. It is a boolean-execution             mination fail immediately.
    controlling parameter. When it is set to no, we set              • PRETRS time {1, 2, 3, 4, 5}. It is used to control the
    PRETRS = fail in the generated configuration doc-                  execution time of PRETRS. The default execution time
    ument. The fail processor fails immediately. CSI will              is 2 seconds, controlled by [2] as in the definition. We
    not do any modification and discover any proof.                    set the execution time to be chosen from {1, 2, 3,
  • abbreviation processor such as PRETRS matrix. It is                4, 5} seconds.
    a boolean-execution controlling parameter. We use such           • PRETRS matrix dim {1, 2, 3, 4, 5, 6,
    names when a strategy contains several parallelly or se-           7, 8, 10, 12, 16}.          The matrix processor
    quentially executed processors. When it is set to no, we           means applying matrix interpretations [Endrullis et al.,
    ignore the corresponding processor in the strategy.                2008]. The parameter PRETRS matrix dim specifies
  • abbreviation processor flag.      It belongs to pro-               the dimension of the matrices. Each matrix processor
    cessor flags, e.g., PRETRS matrix ib.                  It          has several processor flags and associative values to
    chooses the flags for the processor. For instance,                 choose from as below. Since there are several matrix
    PRETRS matrix ib chooses the value for the ib                      processors in PRETRS, we actually associate each
    matrix processor with a set of parameters to search              m a t r i x −dim 3 − i b 3 −ob 3 | \
    from. For simplicity, we only show the parameter space           m a t r i x −dim 3 − i b 3 −ob 7 | \
    of a single matrix processor. The values {yes, no}               m a t r i x −dim 3 − i b 1 −ob 3 ) [ 4 ] * )
    indicate whether to use such flags. For instance, when
                                                                     Next, we explain the parameter space for DIRECTTRS.
    matrix real is set to yes, we add the real flag to
    matrix and obtain matrix -real. In comparison,                 DIRECTTRS = ( ( \
    when it is set to no, we do not append the real flag            kbo | | ( l p o | ( r e f ; l p o ) \
    and simply use matrix. The other flag values indicate           | | ( b o u n d s − r f c −qc ) ) * [ 7 ] ) !
    the values of the flags. For instance, when matrix ib
    is set to 3, we obtain a processor of matrix -ib 3.               • DIRECTTRS {yes, no}.                  DIRECTTRS and
  • PRETRS matrix ib {1, 2, 3, 4, 5, 6}. De-                            DIRECTTRS time works similar as PRETRS and
    fines the number of bits that can be used to represent the          PRETRS time. Hence, we ignore such explanations
    smallest number that appears in the intermediate results            here and for the following sub-strategy definitions. It
                                                                        is sound as DIRECTTRS is only parallelly with other
  • PRETRS matrix ob {1, 2, 3, 4, 5, 6, 7,                              strategies in SN. It makes one technique fail and does
    8, 9, 10, 12, max}. Defines the number of bits                      not affect other parallel executions.
    that can be used to represent the largest number that
    appears in the intermediate results. Actually max is not          • DIRECTTRS time {1, 3, 5, 7, 9, 11}
    a valid value to the ob flag. However, Grackle has the            • DIRECTTRS kbo {yes, no}. The kbo proces-
    mechanism to ignore a parameter if it equals the default            sor means the application of the Knuth-Bendix order
    value. We set max as PRETRS matrix ob’s default                     (KBO) [Baader and Nipkow, 1998].
    value. Moreover, by default, CSI uses the largest 64-bit          • DIRECTTRS kbo ep {yes, no}.                 Demands an
    integers for ob. Hence, max reasonably represents the               empty precedence (only for ‘-pbc’). According to the
    maximal value of ob.                                                function pbc aux in csi/src/processors/src/termination/
  • PRETRS matrix rat {1, 2, 3, 4}. Sets the                            orderings/kbo.ml, it is only used when the PBC prover
    denominator of integers. It makes integers become ra-               is invoked. As explained in Definition 1 in [Zankl et
    tional numbers. The soundness of non-negative ratio-                al., 2009], KBO has a set of precedences and a set of
    nal numbers for matrix interpretation is explained in               weight functions. An empty set of precedences makes
    in [Gebhardt et al., 2007; Zankl and Middeldorp, 2010].             KBO weaker in discovering termination proofs. Empty
    The matrix processor also has a flag neg, which is                  precedences have also been used in Example 3 in the
    set to false by default. Since we do not use neg in                 paper. Section 9 in [Zankl et al., 2009] shows empty
    our parameter space, the interpretations are always non-            precedences are sometimes useful for the PBC backend.
    negative and therefore sound.                                     • DIRECTTRS kbo ib {1, 2, 3, 4, 5, 6}. De-
  • PRETRS matrix db {1, 2, 3, 4, max}.                                 fines the number of bits that can be used to represent the
    Specifies the bits after the decimal point. The reason for          smallest number that appears in the intermediate results
    soundness is the same as PRETRS matrix rat                        • DIRECTTRS kbo minp {yes, no}. Minimizes the
  • PRETRS matrix real {yes, no}. The sound-                            precedence comparisons (only for ‘-pbc’). According
    ness of non-negative real numbers for matrix interpre-              to the function solve2 in csi/src/logic/src/solver.ml
    tation is explained in Lemma 23, Definition 24, and                 and the function context in csi/src/processors/src/
    Lemma 25 in [Zankl and Middeldorp, 2010]. Matrix in-                termination/orderings/kbo.ml, it is only used when the
    terpretation over real numbers is unsound because nega-             PBC prover is invoked. According to the function
    tive numbers break the monotone constraints [Endrullis              solve in csi/src/logic/src/miniSatP.ml, the usage of
    et al., 2008]. However, matrix also has a flag neg,                 -pbc is sound without -minp or -minw. According
    which is set to false by default. Since we do not use               to Section 9 in [Zankl et al., 2009], it is sound and is
    neg in our parameter space, the real number interpreta-             helpful for generating human-readable proofs. KBO has
    tions are always non-negative and therefore sound.                  a set of precedence and a set of weight functions. This
  • PRETRS matrix triangle {yes, no}. Use tri-                          flag tries to discover a termination proof with a small set
    angular matrices. It is sound since it only constrains the          of precedence.
    shape of the matrix. It is less expressive than the tradi-        • DIRECTTRS kbo minw {yes, no}. Minimize the
    tional matrix interpretation. Originally, it is invented for        sum of weights (only for ‘-pbc’). According to the func-
    complexity analysis [Moser et al., 2008].                           tion solve2 in csi/src/logic/src/solver.ml and the func-
   The structure of PRETRS is kept although we search for               tion context in csi/src/processors/src/termination/
other parameters. This means the matrix processors are                  orderings/kbo.ml, it is only used when the PBC prover
still connected by | instead of ||. We may generate some-               is invoked. According to the function solve in csi/
thing like the strategy below.                                          src/logic/src/miniSatP.ml, the usage of -pbc is sound
                                                                        without -minp or -minw. According to Section 9
PRETRS = ( ( \                                                          in [Zankl et al., 2009], it is sound and is helpful for
 m a t r i x −dim 1 − i b 4 −ob 5 | \                                   generating human-readable proofs. Small weights are
  more readable. KBO has a set of precedence and a set           • DIRECTTRS bounds rc {explicit,
  of weight functions. This flag tries to discover a termi-        implicit}. Defines the algorithm that is used
  nation proof with weight functions that map symbols to           to construct raise-consistent tree automata. Possible val-
  small weights.                                                   ues are explicit and implicit where. Per default
• DIRECTTRS kbo ob {1, 2, 3, 4, 5, 6, 7,                           implicit is used. Different values of the parameter
  8, 9, 10, 12, max}. Defines the number of bits                   are sound according to [Korp and Middeldorp, 2009].
  that can be used to represent the largest number that          • DIRECTTRS bounds rfc {yes, no}. Uses right-
  appears in the intermediate results.                             hand sides of forward closures. Different values of the
• DIRECTTRS kbo pbc {yes, no}.                  Uses PBC           parameter are sound according to [Korp and Middel-
  backend. PBC, SAT, or SMT are just solvers to search             dorp, 2009]. Moreover, it is used in DIRECTTRS.
  for interpretations. The choice does not affect the sound-     • DIRECTTRS bounds steps {-1, 1, 2, 3,
  ness.                                                            4, 5, 6, 7, 8, 10, 12, 16, 32}. Specifies
• DIRECTTRS kbo quasi {yes, no}.                     Allows        the maximum number of compatibility violations that
  quasi-precedences. It is sound according to Definition           should be solved. This guarantees that the proce-
  3.1 in [Sternagel and Thiemann, 2013].                           dure always terminates. Otherwise it might happen
                                                                   that the graph approximation does not terminate.
• DIRECTTRS kbo rat {1, 2, 3, 4}. Sets the                         The match-bound technique tries to build a tree
  denumerator (only in combination with ‘-sat’ or ‘-smt’).         automata using the tree automata completion tech-
• DIRECTTRS kbo sat {yes, no}. Uses SAT back-                      nique. The tree automata completion tries to solve
  end (default).                                                   all compatibility violations.       However, sometimes
• DIRECTTRS kbo smt {yes, no}.                  Uses SMT           there are infinite violations. Meanwhile solving all
  backend.                                                         violations may take too much time. According to
                                                                   csi/src/processors/src/termination/bounds/bounds.ml,
• DIRECTTRS lpo {yes, no}.                Applies Lexico-          CSI uses -1 by default, meaning to solve all violations.
  graphic Path Order [Baader and Nipkow, 1998]. There              Other values make the match-bound technique fail
  are two lpo processors in DIRECTTRS. We employ the               earlier. This flag only controls the size of the search
  same parameters for them to reduce the size of the pa-           space and therefore sound.
  rameter space. Since lpo are weak techniques for prov-
  ing termination, assigning different parameters to two
  lpo processors should only have little influence on the         ARCTICTRS = a r c t i c −dp − u r \
  performance of proving termination.                               −dim 2 − i b 2 −ob 2 [ 2 ]
• DIRECTTRS lpo direct {yes, no}. Try to fin-
  ish the termination proof. The lpo processor can each           ARCTICBZTRS = a r c t i c −bz −dp − u r \
  time prove the termination of a single rule of a TRS and          −dim 2 − i b 2 −ob 2 [ 2 ]
  remove the rule from the TRS. Afterwards, it can be re-
  peatedly applied to prove the termination of another rule
  in the smaller TRS. It shows the termination of the entire     Use arctic interpretation [Koprowski and Waldmann,
  TRS by proving the termination of all rules. Notice that     2008].     The parameter space for ARCTICTRS and
  *[7] in the definition means repeatedly applying lpo         ARCTICBZTRS is presented below.
  and lpo as much as possible in seven seconds. Using            • ARCTICTRS {yes, no}. Notice that ARCTICTRS
  direct, it tries to show termination for all rules; thus,        and ARCTICBZTRS use the flag ur because they are
  it only makes the searching difficult.                           employed in MAINTRS, which first applies the transfor-
• DIRECTTRS lpo quasi {yes, no}.                     Allows        mation using the ur processor. The ur processor re-
  quasi-precedences (currently not supported together              moves all rules of the given dependency pair (DP) prob-
  with -dp flag). The proofs of the soundness are pre-             lem which are not usable [Suzuki et al., 2011]. The -ur
  sented in Theorem 2.37 and Theorem 2.26 in Chapter 2             flag for arctic uses usable rules with respect to inter-
  Preliminaries in [Hirokawa, 2006].                               pretation. If we remove -ur here, we will produce un-
                                                                   soundness. Therefore, we always choose to use the -ur
• DIRECTTRS lpo sat {yes, no}.                                     flag for arcitc and only search for other parameters.
• DIRECTTRS lpo smt {yes, no}                                      It is sound as ARCTICTRS is only parallelly executed
• DIRECTTRS bounds {yes, no}. This processor                       with other strategies in MAINTRS. It makes one tech-
  proves termination of a given problem by using the               nique fail and does not affect other parallel executions.
  match-bound technique [Korp and Middeldorp, 2009].             • ARCTICTRS time {1, 2, 3, 4}
• DIRECTTRS bounds qc {yes, no}. Computes                        • ARCTICTRS arctic dim {1, 2, 3, 4, 5,
  quasi-compatible tree automata instead of compati-               6, 7, 8, 10, 12, 16}. The reasons for the
  ble tree automata. Different values of the parameter             soundness of dim, ib, ob, direct, rat,
  are sound according to [Korp and Middeldorp, 2009].              real have been explained for the previous strategy
  Moreover, it is used in DIRECTTRS.                               definitions.
• ARCTICTRS arctic ib {1, 2, 4, 8, 16}.                               -direct flag that proves a certain property for all
• ARCTICTRS arctic ob {1, 2, 4, 8, max}.                              rewrite rules at the same time. Moreover, both yes and
  Defines the number of bits that can be used to represent            no are used for bounds in BOUNDS.
  the largest number that appears in the intermediate              • BOUNDS bounds dp {yes, no}. Uses the enrich-
  results.                                                           ments match-DP and top-DP instead of match and
• ARCTICTRS arctic bz {yes, no}. Since both                          top if a DP problem is given. Make sure that as enrich-
  yes and no are empolyed in ARCTICTRS and                           ment either top or match has been chosen because the
  ARCTICBZTRS, and they are used in the same strat-                  soundness of roof-DP is unknown. The enrichments
  egy definition MAINTRS, we conclude either the choice              are determined by the flag -e. Since we do not search
  of yes or no is sound. Moreover, its soundness is ex-              for -e here, it uses the default value match and hence
  plained in Section 7 [Koprowski and Waldmann, 2008].               is sound.
• ARCTICTRS arctic direct {yes, no}                                • BOUNDS bounds qc {yes, no},
                                                                     BOUNDS bounds rc {explicit, implicit},
• ARCTICTRS arctic dp {yes, no}. Allows non-                         BOUNDS bounds rfc {yes, no},
  monotone interpretations, i.e., ‘0’ as a coefficient. In the       BOUNDS bounds steps {-1, 1, 2, 4, 8,
  original definition of ARCTICTRS, -dp is used; hence,              16, 32}. Their soundness has been explained for
  yes is sound. Choosing no merely makes the inter-                  DIRECTTRS
  pretation monotone. Basically, termination techniques
  require monotone interpretations. The -dp flag is an
  exception since it works in the dependency pair (DP)              MAINTRS = ( dp ; edg [ 0 . 5 ] ? ; ( s c c s | \
  frameworks [Giesl et al., 2005a]. The soundness of non-            ( sc | | s c t | | \
  monotone interpretations is explained in Section 6 [Ko-            { ur ? ; ( \
  prowski and Waldmann, 2008].                                         ( m a t r i x −dp − u r −dim 1 \
• ARCTICTRS arctic rat {1, 2, 3, 4}. Use                                  − i b 3 −ob 5 | \
  rational numbers for arctic interpretations. The sound-                m a t r i x −dp − u r −dim 2 \
  ness is explained in Section 5 [Sternagel and Thiemann,                 − i b 2 −ob 3 | \
  2014b].                                                                m a t r i x −dp − u r −dim 3 \
• ARCTICTRS arctic real {yes, no}. Use real                               − i b 1 −ob 1 | \
  numbers for arctic interpretations. The soundness is ex-               m a t r i x −dp − u r −dim 3 \
  plained in Section 6 [Sternagel and Thiemann, 2014b].                   − i b 1 −ob 3 ) | | \
                                                                       ( kbo − u r − a f | l p o − u r − a f ) | | \
• ARCTICBZTRS {yes, no}.                  The parameter               ARCTICTRS | | \
  space for ARCTICBZTRS is the same as that for                       ARCTICBZTRS ) \
  ARCTICTRS; hence, we ignore it here. It is sound as                }restore || \
  ARCTICBZTRS is only parallelly executed with other                 BOUNDS[ 1 ]
  strategies in MAINTRS. It makes one technique fail and             ))*[6])!
  does not affect other parallel executions.

                                                                    The MAINTRS is the main strategy for proving termina-
BOUNDS = ( b o u n d s −dp − r f c −qc \                         tion. It first transforms TRS problems into dependency pair
  | | b o u n d s −dp − a l l − r f c −qc \                      (DP) problems using the dp processor. Next, the edg pro-
  | | b o u n d s − r f c −qc )                                  cessor reduces the sizes of the DP problems. Afterwards, the
                                                                 sccs processors tries to decompose each DP problems into
                                                                 several smaller DP problems. Finally, many processors are
• BOUNDS {yes, no}. Prove termination of a given                 executed to solve the DP problems. In particular, the ur pro-
  problem by using the match-bound technique [Korp and           cessor removes all rules of the given DP Problem which are
  Middeldorp, 2009]. It is sound as ARCTICBZTRS                  not usable. Note that this processor is not sound if the given
  is only parallelly executed with other strategies in           DP problem is duplicating. To confirm the soundness, the
  MAINTRS. It makes one technique fail and does not af-          termination processors after the application of the transfor-
  fect other parallel executions.                                mation processor ur must use the flag -ur. The processor
• BOUNDS bounds {yes, no}.          There are three              restore remains unchanged to confirm soundness. It re-
  bounds, we only explain the parameter space for one            stores the original TRS within the given DP problem. In CSI,
  for simplicity.                                                TRS rules and DP rules are stored in different data structures.
• BOUNDS bounds all {yes, no}. This flag is only                 Each execution of processors like matrix in MAINTRS may
  effective if a DP, critical pair, or relative termination      remove TRS rules or DP rules, but the TRS rule will be re-
  problem is given. In that case, all rewrite rules are          stored afterward. The details of the parameter space are pre-
  proved to be finite (relative terminating) instead of a        sented below.
  single rewrite rule. It is sound since it works like the         • MAINTRS {yes, no}. The main technique to prove
  termination. It is sound as MAINTRS is only parallelly            is that we always use flags -ur and -dp for every
  executed with other strategies in SN. It makes one tech-          matrix processor here. The usage -ur is for sound-
  nique fail and does not affect other parallel executions.         ness, while the usage of -dp aims at making the matrix
• MAINTRS time {2, 4, 6, 8}                                         interpretation stronger in discovering termination.
• MAINTRS edg time {0.2, 0.5, 1}. The edg                        • MAINTRS kbo {yes, no}. Applies Knuth-Bendix
  processor [Giesl et al., 2005b] removes all edges from           order [Baader and Nipkow, 1998]. Always use the -ur
  the current dependency graph (DG) that are not con-              -af flags.
  tained in the EDG (approximation of DG based on re-            • MAINTRS kbo ib {1, 2, 3, 4, 5, 6}.                    De-
  cursive unification and symmetry). Here, the parameter           fines the number of bits that can be used to represent the
  controls its execution time.                                     smallest number that appears in the intermediate results
• MAINTRS edg gtcap {yes, no}. Use a general                     • MAINTRS kbo ob {1, 2, 3, 4, 5, 6, 7,
  tcap-like non-reachability analysis. Sound as explained          8, 9, 10, 12, max}. Defines the number of bits
  in Theorem 13 of [Giesl et al., 2005b].                          that can be used to represent the largest number that
• MAINTRS edg nl {yes, no}. Try to exploit non-                    appears in the intermediate results. Actually max is not
  linearity for -gtcap. Non-linear order is more expres-           a valid value to the ob flag. However, Grackle has the
  sive than linear order. The soundness is explained in            mechanism to ignore a parameter if it equals the default
  Section 3 in [Giesl et al., 2005b].                              value. We set max as MAINTRS kbo ob’s default
                                                                   value. Moreover, by default, CSI uses the largest 64-bit
• MAINTRS BOUNDS time {0.5, 1, 2, 3}
                                                                   integers for ob. Hence, max reasonably represents the
• MAINTRS sc {yes, no}. Applies the subterm cri-                   maximal value of ob.
  terion processor [Sternagel, 2016].
                                                                 • MAINTRS kbo quasi {yes, no}. Allow quasi-
• MAINTRS sc sat {yes, no}. Uses SAT backend                       precedences. It is sound as explained in [Sternagel and
  (default).                                                       Thiemann, 2013]
• MAINTRS sc smt {yes, no}. Uses Yices backend                   • MAINTRS lpo {yes, no}. The soundness has been
  (default).                                                       explained previously. Always use the -ur -af flags.
• MAINTRS sc rec {yes, no}.              Allow recursive
                                                                 • MAINTRS lpo sat {yes, no}.
  simple projections. It is sound because in [Sternagel,
  2016], it is explained below Definition 5 and is used in       • MAINTRS lpo smt {yes, no}.
  the proving termination as shown in Table 1.
                                                                 • MAINTRS lpo direct {yes, no}.
• MAINTRS sc mulex {yes, no}. Allow projec-
  tions to multisets of terms. It is sound because in [Ster-      The structures are also kept unchanged, meaning that we
  nagel, 2016], it is explained in Definition 5 and is used    first execute dp and then edg, etc. We may probably gen-
  in the proving termination as shown in Table 1.              erate a strategy like below. The flags to matrix processors
                                                               and the time limit of edg are changed. However, the over-
• MAINTRS sc defs {yes, no}. Allow projection                  all structure remains the same, and all termination processors
  of defined symbols (only relevant for -rec and               always employ the -ur and -dp flags.
  -mulex; default false). It is sound according to the
  explanation below Definition 5 in [Sternagel, 2016].
• MAINTRS sc mbits {1, 2, 3, 4, 5}.                    Bits       MAINTRS = ( dp ; edg [ 1 ] ? ; ( s c c s | \
  used for multiplicity of terms in multisets corresponding        ( sct || \
  to left- and right-hand sides (default 2). The soundness         { ur ? ; ( \
  is explained in Section 3 [Sternagel, 2016].                       ( m a t r i x −dp − u r −dim 2 \
                                                                        − i b 4 −ob 5 | \
• MAINTRS sc wbits {1, 2, 3, 4, 5}.                   Bits             m a t r i x −dp − u r −dim 2 \
  used for multiplicity (weight) of arguments in projec-                 − i b 2 −ob 3 | \
  tions (default 2). The soundness is explained in Section             m a t r i x −dp − u r −dim 4 \
  3 [Sternagel, 2016].                                                   − i b 2 −ob 2 | \
• MAINTRS sc nsteps {0, 1, 2, 3, 4}. Num-                              m a t r i x −dp − u r −dim 3 \
  ber of rewrite steps before checking for subterms (de-                 − i b 1 −ob 3 ) | | \
  fault 0). It only uses the rules to rewrite the TRS. The           ( kbo − u r − a f | l p o − u r − a f ) | | \
  properties of the original TRS remain the same.                   ARCTICTRS | | \
• MAINTRS sct {yes, no}. Applies the size-change                    ARCTICBZTRS ) \
  termination processor to a DP problem.                           }restore || \
                                                                   BOUNDS[ 2 ]
• MAINTRS matrix. The parameter space for the four                 ))*[8])!
  matrix processors is similar to that for PRETRS.
  Hence, we ignore its details here. The only difference
   We will subsequently explain the parameter space for SN.       the minimal weight that appears in the intermediate
It is a sub-strategy for proving termination, which is also       results.
called strong normalization.                                    • SNRELATIVE poly neg {yes, no}. Allow neg-
                                                                  ative numbers (only for non-linear interpretations) for
                                                                  some coefficients. It is sound for non-linear interpre-
   SN = ( PRETRS ; ( MAINTRS \                                    tation according to Corollary 3.9 in [Neurauter, 2012].
     | | DIRECTTRS | | \                                          The combination of neg flag and the default linear
     ( r e v ; ( MAINTRS | | DIRECTTRS ) ) ) )                    interpretation may cause unsoundenss. We avoid it
                                                                  by using Grackle’s forbidden mechanism that disallows
                                                                  the combination of the neg flag and the default lin-
   The only parameter is SN rev {yes, no}. If it is no,           ear interpretation as shown in Section D.3. The com-
(rev;(MAINTRS || DIRECTTRS)) is not used in SN.                   bination of neg, the nonlinear interpretation (nl or
Otherwise, it remains in SN. It is sound as SN rev is only        nl2), and the real number interpretation (real or
parallelly executed with other strategies in SN. It makes one     rat > 1) is also unsound. But CSI can detect it
technique fail and does not affect other parallel executions.     and forbade such combinations according to the func-
                                                                  tion context in csi/src/processors/src/termination/
                                                                  interpretations/polynomialInterpretation.ml.
   SNRELATIVE STEP = ( \
    lpo −quasi | | \                                            • SNRELATIVE poly ob {1, 2, 3, 4, 5, 6,
    ( m a t r i x −dim 1 − i b 3 −ob 4 | \                        7, 8, 9, 10, 12, max} Defines the number of
      m a t r i x −dim 2 − i b 2 −ob 2 | \                        bits that can be used to represent the largest number that
      m a t r i x −dim 3 − i b 1 −ob 2 | \                        appears in the intermediate results.
      a r c t i c −dim 2 − i b 2 −ob 2 ) | | \                  • SNRELATIVE poly rat {1, 2, 3, 4}. Sets the
    ( i f duplicating then f a i l else                           denumerators for rational numbers. The soundness is
        ( bounds − r t | | \                                      explained in Section 2.1.2 [Neurauter, 2012].
           b o u n d s − r t −qc ) ) [ 1 ] | | \                • SNRELATIVE poly real {yes, no}. Uses reals.
    p o l y − i b 2 −ob 4 − n l 2 − h e u r i s t i c 1 )         The soundness is explained in Section 2.1.2 [Neurauter,
                                                                  2012].
   SNRELATIVE = ( SNRELATIVE STEP [ 5 ] * )
                                                                • SNRELATIVE poly nl {yes, no}. Allow x2 +
                                                                  y 2 . By default, linear interpretation is used, which de-
  SNRELATIVE STEP tries to prove the relative ter-                notes the format of f (x1 , ..., xn ) = a0 + a1 x1 + · · · +
mination of a rule.        SNRELATIVE repeatedly apply            an xn where xi ≥ 0. The -nl flag enables the inter-
SNRELATIVE STEP in five seconds until all rules are               pretation in the format of f (x1 , ..., xn ) = a0 + a1 x1 +
proven to be relatively terminated.                               · · · + an xn + a′1 x21 + · · · + a′n x2n where xi ≥ 0 accord-
                                                                  ing to Section 3.2.2 in [Neurauter, 2012] and the func-
  • SNRELATIVE STEP time {1, 2, 3, 4,                             tion quadratic in csi/src/processors/src/termination/
    5, 6, 7, 8}.           Assign an execution time for           interpretations/polynomialInterpretation.ml. It is sound
    SNRELATIVE STEP. Notice that CSI’s default                    according to [Neurauter, 2012].
    strategy assigns five seconds.                              • SNRELATIVE poly nl2 {yes, no}. Allow x2 +
  • SNRELATIVE lpo {yes, no}. The parameters of                   x ∗ y + y 2 . The -nl2 flag enables the interpretation in
    lpo are the same as those of lpo in DIRECTTRS.                the format of
                                                                                                 n              n
  • SNRELATIVE matrix {yes, no}. The parame-                                                   X               X
                                                                      f (x1 , ..., xn ) = a0 +      aj xj +           ajk xj xk
    ters of matrix are the same as those of matrix in
                                                                                            j=1          1≤j≤k≤n
    PRETRS.
                                                                  where xi ≥ 0 according to Section 3.2.2 in [Neu-
  • SNRELATIVE arctic {yes, no}. The parame-                      rauter, 2012] and the function quadratic in
    ters of arctic are ib, ob, direct, rat, real.                 csi/src/processors/src/termination/interpretations/
    Their soundness have been explained for ARCTICTRS.            polynomialInterpretation.ml. It is sound according
  • SNRELATIVE poly {yes, no}. Applies polyno-                    to [Neurauter, 2012].
    mial interpretations.                                       • SNRELATIVE poly heuristic {-1, 0, 1,
  • SNRELATIVE poly dim {1, 2, 3, 4, 5, 6,                        2, 3, 4}. -1 → all symbols (default); 0 → no
    7, 8, 10, 12, 16}. Specifies the dimension of                 symbols ; 1 → symbols appearing at most once in
    the matrices.                                                 each left-hand side (lhs)/ right-hand side (rhs); 2 →
                                                                  symbols appearing at most twice in each lhs/rhs; 3 →
  • SNRELATIVE poly direct {yes, no}. Try to                      symbols appearing at parallel positions in each lhs/rhs;
    finish the termination proof.                                 4 → defined symbols. It decides which symbols should
  • SNRELATIVE poly ib {1, 2, 3, 4, 5, 6}.                        be interpreted by non-linear polynomials and is sound
    Defines the number of bits that can be used to represent      according to Section 5 in [Neurauter et al., 2010].
                                                                 it is only parallel executed with other confluence techniques.
   MATRIXSTAR= ( ( \
    m a t r i x −dim 1 − i b 2 \
      −ob 2 − s t r i c t e m p t y − l s t a r | \                 NOTCR = ( \
    m a t r i x −dim 2 − i b 2 −ob 2 \                               ( nonconfluence − steps 0 \
      −strict empty −lstar )[2])                                        − tcap −fun | \
                                                                       nonconfluence − steps 2 \
                                                                        − tcap −fun | \
  • MATRIXSTAR time {1, 2, 3, 4}                                       n o n c o n f l u e n c e − s t e p s 25 \
  • The parameter space for each matrix processor is                    −width 1 − tcap −fun | \
    the same as that for a matrix processor in PRETRS.                 nonconfluence − steps 2 \
    Notice that both processors matrix here employ the                  −idem − f u n ) | | \
    flags -strict empty -lstar. We fix the usage of                  ( nonconfluence − steps 2 \
    matrix -strict empty -lstar and search for                          −tcap −var | \
    the other parameters.                                              n o n c o n f l u e n c e − s t e p s 25 \
                                                                          −width 1 − tcap −var ) | | \
                                                                     ( nonconfluence − steps 0 \
   MATRIXREDEX= ( ( \                                                   − t r e e −fun | \
    m a t r i x −dim 1 − i b 2 −ob 2 \                                 nonconfluence − steps 0 \
    −strict empty −lredex )[2])                                           − t r e e −var | \
                                                                       nonconfluence − steps 1 \
                                                                          − t r e e −fun | \
  • MATRIXREDEX time {1, 2, 3, 4, 5}                                   nonconfluence − steps 1 \
                                                                          − t r e e −var | \
  • The parameter space for each matrix processor is the
                                                                       nonconfluence − steps 2 \
    same as that for a matrix processor in PRETRS. No-
                                                                          − t r e e −fun | \
    tice that both processors matrix here employ the flags
                                                                       nonconfluence − steps 2 \
    -strict empty -lredex. We fix the usage of
                                                                          − t r e e −var | \
    -strict empty -lredex and search for the other
                                                                       n o n c o n f l u e n c e − s t e p s 25 \
    parameters.
                                                                          −width 1 − t r e e −fun | \
                                                                       n o n c o n f l u e n c e − s t e p s 25 \
   LDH = ( s h i f t −dd ; SNRELATIVE ; \                                 −width 1 − t r e e −var ) \
      s h i f t −ldh − force )                                      )[10]
   LDHF = ( s h i f t −dd − f o r c e ; \
     SNRELATIVE ; s h i f t − l d h − f o r c e )
   SSTAR = ( c r M − s t a r ; MATRIXSTAR * ; \                     The NOTCR strategy is used to disprove confluence. It
      shift −sstar )                                             uses the || combinator to parallelly execute three groups
   DUP = ( c r M −dup ; SNRELATIVE ; \                           of nonconfluence techinuqes. Each group contains several
      shift −lstar )                                             nonconfluence processors employed with different pa-
   REDEX = ( c r M − r e d e x ; MATRIXREDEX * ; \               rameters. These parameters determine the search space of
      shift −lstar )                                             the nonconfluence processors. To improve the execution
                                                                 speed, the processors using smaller search spaces are invoked
                                                                 before those using larger search spaces in each group. We
    The strategies in the above code block are very compli-      only define the parameter space for one nonconfluence
cated, and we cannot understand them. Therefore, we keep         processor due to the following reasons. First, although the
them unchanged and do not search for the parameters. We          sorted decomposition technique may decompose a TRS to
only have a parameter REDEX {yes, no}. It is sound as            several sub-TRSs, we only need to disprove confluence for
it is only used in COR3 = (REDEX; ...)!, and COR3 is             a sub-TRS to disprove confluence for the original TRS [Fel-
parallelly executed with other techniques in DD. It only makes   genhauer et al., 2015]. CSI’s solution in CoCo for a non-
COR3 immediately fail.                                           confluence problem also shows that we only need to prove
                                                                 nonconfluence for a sub-TRS to disprove confluence for the
                                                                 original TRS. Second, we want to invent a set of complemen-
   GROUND = ( i f g r o u n d \                                  tary strategies and then combine them in the approach ex-
     then uncurry −curry ?; \                                    plained in Section Strategy Combination in our paper. CSI’s
     groundcr else f a i l )                                     default strategy combines sequential and parallel execution
                                                                 to try various nonconfluence techniques and increase the
                                                                 execution speed. In contrast, our goal of defining a pa-
  The decision procedure for ground systems [Felgenhauer,        rameter space is simply to invent a technique suitable for
2012]. We only have GROUND {yes, no}. It is sound as             a set of problems. The combination of invented strategies
will be considered later. Therefore, our parameter space                the nonconfluence techniques. It is explained in Lemma
will produce a strategy like NOTCR = nonconfluence                      1 of [Zankl et al., 2011].
-steps 0 -tcap -fun[10] where the execution time                      • nonconfluence tree {yes, no}. Show non-
of nonconfluence and its flags are decided by Grackle.                  confluence by tree automata (default off). It is sound as it
   • NOTCR {yes, no}. Disprove confluence. It is sound                  is one of the nonconfluence techniques used in NOTCR..
     because if we set it to fail, the strategy simply mainly           It is explained in Theorem 4 of [Zankl et al., 2011]
     tries to discover confluence proofs. It will not cause un-
                                                                      • nonconfluence idem {yes, no}. Show non-
     expected transformations.
                                                                        confluence by idem (default off). It is sound as it is
   • nonconfluence time {1, 2, 4, 6, 8,                                 one of the nonconfluence techniques. Meanwhile, ac-
     10, 12, 14, 16, 18, 20, 25, 30}                                    cording to the function idem in csi/src/processors/src/
   • nonconfluence steps {0, 1, 2, 3, 4,                                confluence/nonconfluence.ml, it simply checks the non-
     5, 6, 7, 8, 9, 10, 11, 12, 16, 25,                                 joinability of the reducts of the two terms in a critical
     32}. Number of rewrite steps that are performed from               pair. The nonjoinability is approximated via defined
     critical pairs to test terms nonconfluent [default: 2].            symbols. Moreover, it is used in the original NOTCR.
     Critical pairs are explained in Section A. It is sound as        • nonconfluence nf {yes, no}. Show no unique
     it only changes the size of the search space.                      normal forms exist by finding distinct normal forms (de-
   • nonconfluence width {-1, 1, 2, 3, 4,                               fault off). No unique normal forms imply nonconflu-
     5, 6, 7, 8, 9, 10, 11, 12, 16}. Width of                           ence [Baader and Nipkow, 1998]; hence, the flag is
     search tree for rewrite sequences; -1 means unbounded              sound.
     [default: -1]. It is sound as it only changes the size of
     the search space.
   • nonconfluence fun {yes, no}. Use overlaps at                     KB = ( c r −kb ; SN ) !
     function positions only. As explained in Section A, an           RL = ( r u l e l a b e l i n g \
     overlap roughly means that at a certain position, a sub-           | rule labeling −left )
     term can be applied with two rewrite rules [Baader and           DECPAR = ( ( s h i f t − p a r ; \
     Nipkow, 1998]. As explained in Section A, the basic                decreasing −par ) | \
     idea for disproving confluence is to discover an over-             ( s h i f t − p a r −m 2 ; d e c r e a s i n g − p a r ) )
     lap, discover a critical pair from the overlap, and check        DECWLL = ( ( r u l e l a b e l i n g − l e f t \
     the non-joinability of the pair. This flag only determines         − p e r s i s t ; d e c r e a s i n g ) | DECPAR)
     where to find such an overlap and thereby is sound.              DDLAB = (LDH ; ( d e c r e a s i n g | \
                                                                        RL ? ; d e c r e a s i n g ) ) !
   • nonconfluence var {yes, no}. Use overlaps at
     variable positions only. As explained in the last flag, this
     flag only determines where to find such an overlap and           • KB {yes, no}. Denote the Knuth-Bendix crite-
     thereby is sound.                                                  rion [Knuth and Bendix, 1983]. It is sound because it
   • nonconfluence iter {-1, 1, 2, 3, 4,                                is only a technique parallelly executed with other tech-
     5, 6, 7, 8, 9, 10, 11, 12, 16}. Specifies                          niques.
     the maximum number of compatibility violations that
                                                                      • DECPAR {yes, no}. One technique in decreasing
     should be solved. This guarantees that the procedure
                                                                        diagrams [Aoto et al., 2014]. We cannot entirely un-
     always terminates. Otherwise, it might happen that
                                                                        derstand it. Thus, there is only one boolean execution-
     non-confluence check does not terminate. It is only used
                                                                        controlling parameter. It is sound because DECPAR is
     for tree automata technique. According to Theorem 4
                                                                        simply used at the end of DECWLL. DECWLL is only
     in [Nagele et al., 2017], for a critical pair (s, t), it first
                                                                        used at the end of DD. DD is only a technique paral-
     tries to respectively construct compatible tree automates
                                                                        lelly executed with other techniques. Setting DECPAR
     A1 and A2 . Then, it checks the non-joinability of
                                                                        to fail only makes the strategy weaker in discovering
     term reachable from A1 and A2 . The flag uses the tree
                                                                        proofs.
     automata completion technique [Korp and Middeldorp,
     2009] to build tree automata, which solves compatibility         • DECPAR shift m {0, 1, 2, 4, 6}. Search for
     violations during the constructions. If it cannot solve all        (minimal+m)-length joins. It changes the value of -m
     compatibility violations, the flag fails and cannot dis-           of the second shift in DECPAR. If m < 0, it does
     prove confluence. According to the filter function                 not search for joins. Otherwise, it first searches for the
     in csi/src/processors/src/confluence/nonconfluence.ml,             minimal-length of joins. After that, according to the
     when -iter is -1, it tries to solve all compatibility              value of -m, it searches for joins of length minimal+m.
     violations. However, the construction process may not              It is sound as it only changes the size of the search space.
     terminate and fail. Other values only make the tree                Meanwhile, different values of -m are used in DECPAR.
     automate completion fails earlier.                               • DDLAB {yes, no}. One technique in decreasing di-
   • nonconfluence tcap {yes, no}. Show non-                            agrams. We cannot entirely understand it. Thus, there is
     confluence by tcap (default on). It is sound as it is one of       only one boolean execution-controlling parameter.
                                                             • CLOSED LEFT closed strongly {-1, 1, 3,
COR1 = (DUP ;DDLAB ) !                                         5, 7, 9, 11}. There are four closed processors
COR2 = ( SSTAR ;DDLAB ) !                                      with this flag in CLOSED LEFT, we only explain one.
COR3 = (REDEX ;LDH ; ( d e c r e a s i n g \
 | rule labeling ?; decreasing ))!
DDWLL = (LDHF ; RL ? ;DECWLL) !                              CR AUX = ( s o r t e d − o r d e r | \
DD = ( i f l e f t − l i n e a r t h e n \                       (KB | | ( ( ( ( CLOSED \
  ( COR1 | | COR2 | | COR3 | | \                                    | | DD) | add ) 2 * ) ! ) ) ) *
  ( c r − f o r c e ;DDWLL) ! ) e l s e f a i l ) !          KH = ( c r − r t ; SNRELATIVE ; \
                                                               kh −mace ; CR AUX ) !

• COR1 {yes, no}. One technique in decreasing dia-
  grams [Aoto et al., 2014]. We cannot entirely under-       • CR AUX loop {1, 2, 3, 4, 5}.              It determines
  stand it. Thus, there is only one boolean execution-         the times of the application of CR AUX.
  controlling parameter.
                                                             • KH {yes, no}. Perform the confluence test for asso-
• COR2 {yes, no}. One technique in decreasing dia-             ciative communicative (AC) problems by using the theo-
  grams [Aoto et al., 2014]. We cannot entirely under-         rem of Klein and Hirokawa [Klein and Hirokawa, 2012].
  stand it. Thus, there is only one boolean execution-
  controlling parameter.                                     • KH mace {yes, no}. Use mace4 theorem prover if
                                                               available. The yes value is sound since kh -mace
• COR3 {yes, no}. One technique in decreasing dia-
                                                               is used in the default configuration. According to
  grams [Aoto et al., 2014]. We cannot entirely under-
                                                               the csi/src/processors/src/confluence/kleinHirokawa.ml
  stand it. Thus, there is only one boolean execution-
                                                               in CSI’s source code, when it is set to no, no theorem
  controlling parameter.
                                                               prover will be invoked. According to the paper [Klein
• DD {yes, no}.         Techniques in decreasing dia-          and Hirokawa, 2012], when no theorem prover is in-
  grams [Aoto et al., 2014].                                   voked, the method merely becomes weaker in construct-
                                                               ing confluence proofs.

CLOSED LINEAR = ( i f l i n e a r \
   t h e n c r − c l o s e d − r e d u n d a n t −m −1; \    AT1 = ( a t − t h e o r e m 1 ; SN ) !
       ( closed −feeble \                                    AT2 = ( a t − t h e o r e m 2 ; SN ) !
          | closed − s t r o n g l y 7) \                    AT3 = ( a t − t h e o r e m 3 ; SN ) !
   else fail )                                               AT = ( AT2 | | AT3 )
CLOSED LEFT = ( i f l e f t − l i n e a r \
 t h e n ( ( c r − c l o s e d − r e d u n d a n t −m −1;\
       ( closed −feeble \                                    • AT {yes, no}. The confluence test for associative-
         | closed −development \                               communicative (AC) problems by using the theorems of
         | closed −upside \                                    Aoto and Toyama [2012].
         | closed −outside )) \
       | cr −okui ) e l s e f a i l )                        • AT2 {yes, no}
CLOSED = ( CLOSED LINEAR | | \
 CLOSED LEFT ) !                                             • AT2 theorem {1, 2, 3} Indicates which of the
                                                               three theorems is used. By default, theorem 3 will be
                                                               used. The three theorems are explained in [Aoto and
• CLOSED {yes, no}. Test whether the critical pairs            Toyama, 2012] and are all sound. The value 1, 2, and 3
  of a TRS are strongly or development closed [Huet,           respectively correspond to Theorem 3.8, Theorem 3.18,
  1980; Nagele and Middeldorp, 2016].                          and Theorem 3.28 in [Aoto and Toyama, 2012],
• CLOSED LINEAR {yes, no}                                    • AT2 bound {1, 2, 4, 8, 12, 14, 16,
                                                               24}. Indicates an upper bound for the number of
• CLOSED LINEAR strongly {-1, 1, 3, 5,                         rewrite rules. If the number of rewrite rules is >= b,
  7, 9, 11}. Check critical pairs strongly closed              then the processor ends and fails. By default, b = 12
  (in ≤ n steps). It is sound since it only changes the        will be used. It is sound as it only changes the size of
  number of rewrite steps before checking whether critical     the search space.
  pairs are strongly closed. It determines the value of
  -strongly 7 in CLOSED LINEAR.                              • AT3 {yes, no}
• CLOSED LEFT {yes, no}. Test whether the crit-              • AT3 theorem {1, 2, 3}
  ical pairs of a left-linear system are development
  closed [Van Oostrom, 1997].                                • AT3 bound {1, 2, 4, 8, 12, 14, 16, 24}
                                                                   • REDUNDANT DEL cr m {-1, 0, 1, 2, 3, 4,
   CPCS = ( c r − c p c s ; SNRELATIVE ; \                           5}
    shift −lstar )                                                 • REDUNDANT DEL redundant js {yes, no}.
   CPCS2 = ( c r − c p c s 2 ; SN ) !                                Add joining sequences of critical peaks as rules. It is
                                                                     sound as explained in Collary 6 and Section 5 in [Nagele
                                                                     et al., 2015].
  • CPCS {yes, no}. The processor cr -cpcs com-
    putes the critical pair closing system by Theorem 2.4          • REDUNDANT DEL redundant development
    in [Oyamaguchi and Hirokawa, 2014]. It is sound since            {-1, 1, 2, 3, 4, 5, 6}. Add rules to make
    if it is set to fail, it simply does not transform the prob-     critical peaks development closed. It is sound as
    lem in AUTO INNER.                                               explained in Collary 6 and Section 5 in [Nagele et al.,
                                                                     2015].
  • CPCS2 {yes, no}. The processor cr -cpcs2
    computes the critical pair closing system by Theorem           • REDUNDANT DEL redundant rhs {yes, no}.
    2.11 in [Oyamaguchi and Hirokawa, 2014]. It is sound             Add rules by rewriting right-hand sides 1 step. It
    since it is parallelly executed with other techniques in         is sound as explained in Collary 6 and Section 5 in
                                                                     [Nagele et al., 2015].
    AUTO INNER0.
                                                                   • REDUNDANT DEL redundant remove {-1, 1,
                                                                     2, 3, 4, 5, 6, 7, 8, 9, 10}. Remove rules
   REDUNDANT JS = ( ( \                                              whose left- and right-hand sides are joinable in n steps.
    cr −force −redundant ) ; \                                       By default, it is -1, meaning no limitations on the
    ( redundant ))                                                   number of rewrite steps. The parameter is sound as
   REDUNDANT RHS = ( \                                               other values are weaker than the default in removing
    ( c r −m −1 − f o r c e − r e d u n d a n t ) ; \                rules.
    ( redundant −rhs ))                                            • REDUNDANT DEL redundant reverse {-1,
   REDUNDANT DEL = ( ( c r −m −1 − f o r c e ) ; \                   1, 2, 3, 4, 5, 6}. Add reversible rules. It
    ( r e d u n d a n t −remove 4 ) )                                is sound as explained in Collary 6 and Section 5 in
                                                                     [Nagele et al., 2015].

   A group of redundant rule techniques. REDUNDANT FC              • REDUNDANT DEL redundant size {-1, 1,
is used in nonconfluence analysis, while the other three are         2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
mainly used for confluence analysis.                                 16, 32}

  • REDUNDANT JS cr m {-1, 0, 1, 2,
    3, 4, 5}.             Search for (minimal+m)-length            REDUNDANT FC = ( ( c r −m −1 − f o r c e ) ; \
    joins.     For a critical pair (s, t), According to              ( r e d u n d a n t −narrowfwd \
    csi/src/processors/src/transformation/redundant.ml and             −narrowbwd − s i z e 7 ) )
    csi/src/rewriting/src/rewrite.ml, When m = −1, only
    critical pairs are returned, and no joins will be found.
    When m = 0, it tries to discover the minimal number            • REDUNDANT FC {yes, no}. It is sound because if it
    M of rewrite steps, such that ∃u, s →M u ∧ t →M u.               is set to fail, it simply does not do the redundant rule
    Then joins reachable from M steps are returned. When             transformation for non-confluence analysis.
    m > 0, joins reachable from M + m steps are returned.
                                                                   • REDUNDANT FC cr m {-1, 0, 1, 2, 3, 4,
    Some redundant rule techniques use joins of critical
                                                                     5}. The soundness has been explained before.
    pairs to generate redundant rules [Nagele et al., 2015].
    This parameter is sound since it only controls the length      • REDUNDANT FC redundant js {yes, no}. The
    of joins to be generated.                                        soundness has been explained before.
  • REDUNDANT JS redundant size {-1, 1, 2,                         • REDUNDANT FC redundant development
    3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16,                             {-1, 1, 2, 3, 4, 5, 6}. The soundness has
    32}. Only add rules whose size is less than n (default:          been explained before.
    -1, i.e., unrestricted). It is sound since values other than   • REDUNDANT FC redundant rhs {yes, no}.
    the default merely limit the number of redundant rules           The soundness has been explained before.
    to generate.
                                                                   • REDUNDANT FC redundant narrowfwd {yes,
  • REDUNDANT RHS cr m {-1, 0, 1, 2, 3, 4,                           no}. Use narrowing forwards to generate new rules. It
    5}                                                               is sound since it is in the original REDUNDANT FC.
  • REDUNDANT RHS redundant size {-1, 1,                           • REDUNDANT FC redundant narrowbwd {yes,
    2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,                              no}. Use narrowing backwards to generate new rules.
    16, 32}                                                          It is sound since it is in the original REDUNDANT FC.
   • REDUNDANT FC redundant size {-1, 1, 2,                              • AC ackbo direct {yes, no}. Try to finish the
     3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 16,                                  termination proof.
     32}. The soundness has been explained before.
                                                                         • AC ackbo ib {1, 2, 3, 4, 5, 6}. Defines the
    SIMPLE = FULL ( \                                                      number of bits that can be used to represent the smallest
      ( if right − linear \                                                number that appears in the intermediate results.
        then i f l e f t − l i n e a r −ie \
          t h e n i f s t r o n g l y −non − o v e r l a p p i n g
              then succ −reason \                                        • AC ackbo kv2 {yes, no}. Use corrected Korovin
                ToyamaOyamaguchi95Cor22                                    and Voronkov’s ordering. The paper [Yamada et al.,
              else fail else fail else fail )|\                            2016] finds a bug in the original Korovin and Voronkov’s
      ( i f collapsing then f a i l else                                   ordering and has corrected it.
          i f s h a l l o w −ws t h e n
              i f s t r o n g l y −non − o v e r l a p p i n g t h e n
                                                                         • AC ackbo ob {1, 2, 3, 4, 5, 6, 7, 8,
                 succ −reason \
                                                                           9, 10, 12, max}. Defines the number of bits that
                  SakaiOyamaguchiOgawa14
                                                                           can be used to represent the largest number that appears
              else fail else fail ) | \
                                                                           in the intermediate results.
       fail )

                                                                         • AC ackbo q {yes, no}. Uses quasi-precedences.
   Simple criteria for proving confluence [Sakai et al., 2015;             According to the annotation of the function quasi adm
Toyama and Oyamaguchi, 1994]. The FULL keyword is a                        in csi/src/processors/src/termination/orderings/ackbo.ml
trick in the competition strategy for easily taking part in dif-           in CSI’s source code, here, quasi-precedences mean that
ferent categories of competitions in CoCo. For us, it means                AC-symbols never equal to non-AC symbols. Using
nothing and can be ignored. The only parameter is SIMPLE                   the flag only makes the order more strict and thereby is
{yes, no}.                                                                 sound. Moreover, the ackbo processors have both use
                                                                           and do not use -q in AC SN.
   AC SN = ( ( a c r p o \
     ||    a c k b o − i b 3 −ob 5 −q − n t − s c                        • AC ackbo sat {yes, no}. Uses SAT backend (de-
   \                                                                       fault).
     | | a c k b o − i b 3 −ob 5 −kv2 ) * [ 1 0 ] )
   AC = ( c r − a c ; AC SN ) !
                                                                         • AC ackbo sc {yes, no}. Uses subterm coeffi-
                                                                           cients. It is sound since ackbo both employs it and ig-
   • AC {yes, no}. Main techniques for proving conflu-                     nores it in AC SN. Moreover, its soundness is explained
     ence for AC problems.                                                 in Theorem 8.2 in [Yamada et al., 2016].
   • AC time {1, 2, 4, 6, 8, 10, 15}
   • AC acrpo {yes, no}. Applies AC-Recursive Path                       • AC ackbo smt {yes, no}. Uses SMT backend.
     Order [Yamada et al., 2016].
   • AC acrpo direct {yes, no}
                                                                         • AC ackbo st {yes, no}. Use Steinbach’s order-
   • AC acrpo sat {yes, no}                                                ing. Its soundness is explained in Theorem 3.3 in [Ya-
   • AC acrpo smt {yes, no}                                                mada et al., 2016].
   • AC ackbo {yes, no}. Apply standard, Korov-
     in/Voronkov’s, and Steinbachs AC-KBO [Yamada et al.,                • AC ackbo nt {yes, no}. Allow non-total prece-
     2016]. There are two ackbo processors in AC SN, we                    dences (not compatible with -kv). Precedences are de-
     only explain the parameter for one for simplification.                fined between function symbols or constants. It is essen-
     The flags -kv, kv2, and st respectively correspond to                 tial as explained in Example 5.11, sometimes we need
     Korovin &Voronkov, KV’, and Steinbach methods in Ta-                  to make two function symbols incomparable to obtain a
     ble 1 of [Yamada et al., 2016]. When none of -kv, kv2,                working order. We use Grackle’s forbidden mechanism
     and st is used, by default, ackbo uses the AC-KBO                     to forbidde both -kv and -nt are employed by ackbo.
     method in Table 1.                                                    According to AC SN, the combination of -nt and AC-
   • AC ackbo ac0 {yes, no}. In case of Steinbach’s                        KBO is sound. According to Definition 4.1 and Example
     order, give AC symbols weight 0. Its soundness is ex-                 5.11, the combination of -nt and kv2 is sound. Ac-
     plained in Theorem 3.3 [Yamada et al., 2016] and the                  cording to Definition 3.1, the combination of -nt and
     related footnote.                                                     st is sound.
                                                                   • AUTO INNER0 AT {yes, no}. Control whether to
   AUTO INNER0 DEL = (REDUNDANT DEL ? ; \                            execute AT in AUTO INNER0.
    (CLOSED | | DD | | SIMPLE | | KB \                             • AUTO INNER0 SIMPLE {yes, no}.             Control
     | | AC | | {GROUND} nono ) ) 3 * !                              whether to execute SIMPLE in AUTO INNER0.

   AUTO INNER0 CLOSED DD REDUNDANT =                               • AUTO INNER0 CPCS2 {yes, no}.             Control
    ( ( ( CLOSED | | DD) \                                           whether to execute CPCS2 in AUTO INNER0.
        | REDUNDANT RHS) 3 * ! | | \
      (CLOSED | | DD) \
                                                                    AUTO INNER = ( AUTO INNER0 [ 3 0 ] \
        | REDUNDANT JS ) 3 * !
                                                                      | CPCS [ 5 ] 2 * ) ! \
                                                                        | ( { AUTO INNER0 [ 3 0 ] } nono \
   AUTO INNER0 = (GROUND | | KB | | AC | | \
                                                                           | CPCS [ 5 ] 2 * ) 2 * !
    AUTO INNER0 DEL | | \
    AUTO INNER0 CLOSED DD REDUNDANT | | \
    KH | | AT | | SIMPLE | | CPCS2 )                               • AUTO INNER {yes, no}
                                                                   • AUTO INNER CPCS time1 {1, 2, 3, 4, 5,
   As explained in Section D, AUTO INNER0 paral-                     6, 7, 8, 9}. Control the running time of the first
lelly executes a set of techniques.            When search-          CPCS.
ing for parameters, we group some techniques                       • AUTO INNER CPCS time2 {1, 2, 3, 4, 5,
in AUTO INNER0 into AUTO INNER0 DEL and                              6, 7, 8, 9} Control the running time of the second
AUTO INNER0 CLOSED DD REDUNDANT. We perform                          CPCS.
this modification since techniques inside the two groups have
two common features that not exist in the other techniques         • AUTO INNER CPCS loop1 {1, 2, 3, 4, 5,
in AUTO INNER0. Grouping them is helpful for using a                 6, 7}. Control the number of repeated application
boolean execution-controlling flag to determine whether              times of the first CPCS.
to execute the two groups of techniques. The first distinct        • AUTO INNER CPCS loop2 {1, 2, 3, 4, 5,
feature is that both groups utilize redundant rule techniques.       6, 7}. Control the number of repeated application
Moreover, both groups consist of multiple techniques which           times of the second CPCS.
follow a specific invocation procedure.                            • AUTO INNER loop {1, 2, 3, 4, 5, 6, 7}.
  • AUTO INNER0 {yes, no}.                                           Control the number of repeated application times of
  • AUTO INNER0 time {2, 4, 6, 8, 12, 16,                            the compound processor (AUTO INNER0[30] |
    30, 60}. Control the running time of AUTO INNER0.                CPCS[5]2*)! | (AUTO INNER0[30]nono |
                                                                     CPCS[5]2*).
  • AUTO INNER0 DEL {yes, no}.
  • AUTO INNER0 DEL loop {1, 2, 3, 4, 5,
    6, 7}                                                           AUTO = ( i f t r s t h e n ( \
                                                                     s o r t e d − o r d e r * ; ( AUTO INNER \
  • AUTO INNER0 GROUND {yes, no}.             Control                | | (NOTCR | REDUNDANT FC ) 3 * ! ) \
    whether to execute GROUND in AUTO INNER0.                        ) else fail )
  • AUTO INNER0 KB {yes, no}. Control whether to
    execute KB in AUTO INNER0.
  • AUTO INNER0 AC {yes, no}. Control whether to                   • AUTO sorted order {yes, no}. Decompose a
    execute AC in AUTO INNER0.                                       problem due to sorted information [Felgenhauer et al.,
                                                                     2015]. The flag -order tries order-sorted decomposi-
  • AUTO INNER0 CLOSED DD REDUNDANT {yes,                            tion.
    no}
                                                                   • AUTO sorted ms {yes, no}. Try many-sorted de-
  • AUTO INNER0 CLOSED DD REDUNDANT loop                             composition. It is weaker than -order in decomposing
    {1, 2, 3, 4, 5, 6, 7}.           Control the re-                 TRSs [Felgenhauer et al., 2015].
    peated application times of ((CLOSED || DD) |
    REDUNDANT RHS)3*! || (CLOSED || DD)                            • NOTCR loop {1, 2, 3, 4, 5, 6, 7, 8,
    | REDUNDANT JS).                                                 9, 10}. Control the number of repeated applications
                                                                     of (NOTCR | REDUNDANT FC)3*!, default 3.
  • AUTO INNER0 CLOSED DD REDUNDANT inner
     loop {1, 2, 3, 4, 5, 6, 7}.          Control the            D.3   Forbidden Parameters
    repeated application times of (CLOSED || DD) |               Grackle can forbid the occurrence of certain parameters. We
    REDUNDANT RHS.                                               have listed the parameters we forbid below. We forbid them
  • AUTO INNER0 KH {yes, no}. Control whether to                 either to confirm soundness or to reduce the size of the pa-
    execute KH in AUTO INNER0.                                   rameter search space.
                                                                  • AUTO INNER0 = AC
    { A C a c k b o 1 n t = yes , AC ackbo1 kv = y e s }          • AUTO INNER0 = AUTO INNER0 DEL
    { A C a c k b o 2 n t = yes , AC ackbo2 kv = y e s }
    { MAINTRS edg nl= yes ,                                       • AUTO INNER0 = AUTO INNER0 CLOSED DD REDUNDANT
       MAINTRS edg gtcap=no }                                     • AUTO INNER0 = KH
    { AUTO INNER sorted order =no ,                               • AUTO INNER0 = AT
       AUTO INNER sorted ms=no }
    { DIRECTTRS kbo pbc=no ,                                      • AUTO INNER0 = SIMPLE
       DIRECTTRS kbo eq= y e s }                                  • AUTO INNER0 = CPCS2
    { DIRECTTRS kbo pbc=no ,                                       We also separate each strategy in the nonconfluence anal-
       DIRECTTRS kbo minp= y e s }                              ysis strategy NOTCR as an initial strategy. This means we
    { DIRECTTRS kbo pbc=no ,                                    use the default competition strategy except that we change
       DIRECTTRS kbo minw= y e s }                              AUTO INNER to fail using parameters defined in Sec-
    { DIRECTTRS kbo sat=no ,                                    tion D. Meanwhile, we respectively change the definition of
       DIRECTTRS kbo smt=no ,                                   NOTCR to one of the items below and obtain 14 initial strate-
       DIRECTTRS kbo rat =2}                                    gies.
    { DIRECTTRS kbo sat=no ,
       DIRECTTRS kbo smt=no ,                                     • NOTCR = nonconfluence -steps 0 -tcap
       DIRECTTRS kbo rat =3}                                        -fun[10]
    { DIRECTTRS kbo sat=no ,                                      • NOTCR = nonconfluence -steps 2 -tcap
       DIRECTTRS kbo smt=no ,                                       -fun[10]
       DIRECTTRS kbo rat =4}
    { MAINTRS kbo sat=no ,                                        • NOTCR = nonconfluence -steps 25
       MAINTRS kbo smt=no ,                                         -width 1 -tcap -fun[10]
       MAINTRS kbo rat =2}                                        • NOTCR = nonconfluence -steps 2 -idem
    { MAINTRS kbo sat=no ,                                          -fun[10]
       MAINTRS kbo smt=no ,                                       • NOTCR = nonconfluence -steps 2 -tcap
       MAINTRS kbo rat =3}                                          -var[10]
    { MAINTRS kbo sat=no ,
       MAINTRS kbo smt=no ,                                       • NOTCR = nonconfluence -steps 25
       MAINTRS kbo rat =4}                                          -width 1 -tcap -var[10]
    { SNRELATIVE poly neg= yes ,                                  • NOTCR = nonconfluence -steps 0 -tree
       SNRELATIVE poly nl=no ,                                      -fun[10]
       SNRELATIVE poly nl2=no }
                                                                  • NOTCR = nonconfluence -steps 0 -tree
                                                                    -var[10]
                                                                  • NOTCR = nonconfluence -steps 1 -tree
E    Examples of Invented Strategy                                  -fun[10]
Figure 2 presents the invented strategy csi-                      • NOTCR = nonconfluence -steps 1 -tree
0d232dbb588232c4fa2a8db3585ab8b2d0c28c44bdbcfb555-                  -var[10]
98ae901. It follows the basic structure of the original
competition strategy. Boolean-execution controlling flags         • NOTCR = nonconfluence -steps 2 -tree
disable some sub-strategies be replacing their definitions to       -fun[10]
fail. In SNRELATIVE STEP, the values of -ib, -ob,                 • NOTCR = nonconfluence -steps 2 -tree
and -dim are chosen by Grackle, which differs from those            -var[10]
in the original SNRELATIVE STEP in Seciton C.
                                                                  • NOTCR = nonconfluence -steps 25
                                                                    -width 1 -tree -fun[10]
F   Grackle’s Initial Strategies
                                                                  • NOTCR = nonconfluence -steps 25
As explained in Section C, AUTO INNER0 parallelly exe-              -width 1 -tree -var[10]
cutes a set of strategies mainly for confluence. We separate
each of them as an initial strategy. This means we use the        To generate the dataset, we further add two other strategies
default competition strategy except that we change NOTCR to     besides the initial strategies. This means we use the default
fail and REDUNDANT FC to fail via parameters defined            competition strategy except that we change NOTCR to fail
in Section D. Moreover, we respectively change the definition   and REDUNDANT FC to fail. Moreover, we respectively
of AUTO INNER0 to one of the items below and obtain nine        change the definition of AUTO INNER0 to one of the items
initial strategies.                                             below and obtain two strategies.
   • AUTO INNER0 = GROUND                                         • AUTO INNER0 = CLOSED
   • AUTO INNER0 = KB                                             • AUTO INNER0 = DD
                Figure 2: The invented strategy csi-0d232dbb588232c4fa2a8db3585ab8b2d0c28c44bdbcfb55598ae901

AUTO = ( i f t r s t h e n ( s o r t e d − o r d e r * ; \
  ( AUTO INNER | | (NOTCR | REDUNDANT FC ) 3 * ! ) ) e l s e f a i l )

AUTO INNER = ( AUTO INNER0 [ 3 0 ] | CPCS [ 5 ] 2 * ) ! \
  | ( { AUTO INNER0 [ 3 0 ] } nono | CPCS [ 5 ] 2 * ) 2 * !

AUTO INNER0 = ( AUTO INNER0 GROUND | | AUTO INNER0 KB | | AUTO INNER0 AC \
  | | AUTO INNER0 DEL | | AUTO INNER0 CLOSED DD REDUNDANT | | AUTO INNER0 KH \
  | | AUTO INNER0 AT | | AUTO INNER0 SIMPLE | | AUTO INNER0 CPCS2 | | f a i l )

AUTO INNER0 AC = f a i l

AUTO INNER0 AT = f a i l

AUTO INNER0 CLOSED DD REDUNDANT = f a i l

AUTO INNER0 CPCS2 = f a i l

AUTO INNER0 DEL = f a i l

AUTO INNER0 GROUND = f a i l

AUTO INNER0 KB = f a i l

AUTO INNER0 KH = f a i l

AUTO INNER0 SIMPLE = SIMPLE

CPCS = ( c r − c p c s ; SNRELATIVE ; s h i f t − l s t a r )

NOTCR = f a i l

REDUNDANT FC = f a i l

SIMPLE = FULL ( ( i f r i g h t − l i n e a r t h e n i f l e f t − l i n e a r − i e t h e n \
     i f s t r o n g l y −non − o v e r l a p p i n g t h e n s u c c − r e a s o n ToyamaOyamaguchi95Cor22 \
   else fail else fail else fail )
   | ( i f c o l l a p s i n g t h e n f a i l e l s e i f s h a l l o w −ws t h e n \
     i f s t r o n g l y −non − o v e r l a p p i n g t h e n s u c c − r e a s o n SakaiOyamaguchiOgawa14 \
     else fail else fail ) | fail )

SNRELATIVE = ( SNRELATIVE STEP [ 5 ] * )

SNRELATIVE STEP = ( l p o − q u a s i \
  | | ( m a t r i x − i b 6 −ob 6 | m a t r i x −dim 2 − i b 2 −ob 2 \
     | m a t r i x −dim 3 −ob 2 | a r c t i c −dim 2 − i b 2 −ob 8 ) \
  | | ( i f duplicating then f a i l else \
     ( b o u n d s − r t | | b o u n d s − r t −qc ) ) [ 1 ] \
  | | p o l y − h e u r i s t i c 1 − i b 2 − n l 2 −ob 4 )
We particularly extract them since CLOSED and DD are com-          • csi-ec0fb3f8ce9f2d586b23f5cd9c4a399845157f2854ef5-
bined with redundant rule techniques in AUTO INNER0 DEL               f8e2f9d3f3a, 6
and AUTO INNER0 CLOSED DD REDUNDANT among the                      • csi-af40c043b23e299af5c85347534fe62d2c963a8f7d6b0-
initial strategies.   Moreover, AUTO INNER0 DEL and                   dac873b8846, 7
AUTO INNER0 CLOSED DD REDUNDANT parallelly exe-
cute CLOSED and DD. If we do not use them for labeling,            • csi-3f5a5b338144451e2d7e22bcc184940e796a74510ec87-
we will not be able to understand whether a TRS is mastered           4966c88b93d, 8
only by CLOSED or DD.                                              • csi-fc9509efa9ad65cb01f89548200a9ae5480ef616e48df-
   In the augmented dataset, we notice eight initial strategies       fb3e0d790a2, 8
can only prove confluence, and 14 initial strategies can only     When using one CPU, the time splits are presented below
prove non-confluence. One can prove both.
                                                                   • csi-1789a05ac5304d685e89b710f75edd8a273fc474526-
                                                                      6a3c7faadba34, 0.5,
G Strategy Combination
                                                                   • csi-c3e1c6423a6b61ebf5d3b3c3999fca2d098d4461b23-
To combine several strategies, we first assign a time limit for       a4b50d77171b3, 0.5,
each using the method in Section 3.2. Each strategy is writ-       • csi-075d10c4a77649791eac301cda263f977e1a66186e7-
ten into a document. We use a Python program to invoke                20906f67a2c34, 0.5,
CSI with each strategy document within the assigned time
limit. The advantage of writing each strategy into a docu-         • csi-ddc25446660daf33870ef6991406ec360404a5af909-
ment is avoiding naming conflict since our strategy invention         928d5ea21794f, 0.5,
does not change the name of strategies. We only change the         • csi-6c8b5e7b4af3c2970275389b01434b25395a13d8f72-
parameters. Every strategy document is still invoked from the         4e4a8aba48e24, 0.5,
definition AUTO via Python.                                        • csi-b3ab9764cd4f0717a3037a5849e47d41c56af511e84-
   When we choose a strategy, we make sure this strategy can          d4a72659e0829, 0.5,
solve the largest number of problems in the training data un-
solvable by previously chosen strategies.                          • csi-0ccc287f955294ea83afdc800030b453a8e37b1ee37-
   When we run experiments on the ARI-COPS database and               157d83dcf04eb, 0.5,
use four CPUs for each CSI execution, the assigning time           • csi-224dc655e2c823145f6a545fa78601d91e647dcfeff-
limit for each strategy is presented below in the format of           b317d8f57b340, 0.5,
strategy, time by seconds.                                         • csi-a8f7d2a391815f9c401550acbb694bae346f443a43a-
   • csi-0ccc287f955294ea83afdc800030b453a8e37b1ee371-                098c5e072aae9, 0.5,
     57d83dcf04eb, 0.5                                             • csi-e2877b030e4118e870207e14ef1a44e240c33e16a0e-
   • csi-9f19c01a538808477a8980f80d3d2face7303ce6f058-                79c8f57adaacd, 0.5,
     f8b6170f9461, 0.5                                             • csi-ddc25446660daf33870ef6991406ec360404a5af909-
   • csi-224dc655e2c823145f6a545fa78601d91e647dcfeffb-                928d5ea21794f, 1,
     317d8f57b340 0.5                                              • csi-af40c043b23e299af5c85347534fe62d2c963a8f7d6-
   • csi-2ebf247f07a5706eaf7a7a399dcd47bb52bbb40694af-                b0dac873b8846, 4,
     808ec8624cf1, 0.5                                             •  csi-d56e502247dfc3854f0a5360649b5be5357e2b60693-
                                                                      fdfdc40dc5527, 8,
   • csi-5deb4704be2267c6724151a6417770ceb5ffc4799560-
     7bbf3a169c28, 1                                               • csi-0e7e3ba5c042fabdf8151556dc8b26717d98bcd49c2-
                                                                      3193ec7f29d33, 9,
   • csi-c3e1c6423a6b61ebf5d3b3c3999fca2d098d4461b23a4-
     b50d77171b3, 2                                                • csi-36920a8f429f37ae80839d40e3cd805ef096f1aafbb-
                                                                      2dd6d7b845531, 10,
   • csi-af40c043b23e299af5c85347534fe62d2c963a8f7d6b0-
     dac873b8846, 3                                                •  csi-5deb4704be2267c6724151a6417770ceb5ffc479956-
                                                                      07bbf3a169c28, 11,
   • csi-5deb4704be2267c6724151a6417770ceb5ffc47995607-
                                                                   • csi-33d868984681a7cc4455c15daaa16bf675ba3056c6f-
     bbf3a169c28, 3
                                                                      f1f186057216e, 12
   • csi-a4390ec528e4f6c2616765939087c14c1ca0bd47cf1dd-           When using one CPU for the augmented dataset, the time
     d3b6d055ba0, 3                                             splits are presented below
   • csi-112ecf2d9f970dad13f1bb4e09c25c2b51385f7324062-            • csi-04117237bacc588c78fade8bc184e29c2f22ce95f0f-
     deb49084b46, 5                                                   3d8fc051128e4, 0.5
   • csi-5c115df06bbafa913b50c0fd62a28f53e6739d1358646-            • csi-a4390ec528e4f6c2616765939087c14c1ca0bd47cf1-
     b7f3cea19bf, 6                                                   ddd3b6d055ba0, 0.5
   • csi-14c86024498e9a3ce1b4b79795e5ab8f6c49a19f5df8c-            • csi-379e7f8304b587a34081a91ae8a1624f0fb9a83ef83-
     924ce82f577, 6                                                   2090b72713d9f, 0.5
  • csi-931e7ced256711e95501f485d5b130953464871eebe-            • (csi-a8f7d2a391815f9c401550acbb694bae346f443a43-
    6e41dd72957e9, 0.5                                            a098c5e072aae9, 0.5),
  • csi-c3e1c6423a6b61ebf5d3b3c3999fca2d098d4461b23-            • (csi-4c4f985d3c24d4e988879b93a20ba27aef4d1b5e43-
    a4b50d77171b3, 0.5                                            1cff21ed9c304f, 0.5),
  • csi-af40c043b23e299af5c85347534fe62d2c963a8f7d6-            • (csi-007a111242d4e9cc17cbb487d338934ef25edfe677-
    b0dac873b8846, 0.5                                            bec379b08b5002, 0.5),
  • csi-224dc655e2c823145f6a545fa78601d91e647dcfeff-            • (csi-007a111242d4e9cc17cbb487d338934ef25edfe677-
    b317d8f57b340, 0.5                                            bec379b08b5002, 0.5),
  • csi-5d8720a14f25d32a3a4cecd80b5cc818cfafce6f753-            • (csi-042b74efcc92c96a15db35030eea542a97329bf422-
    b2acd33280292, 0.5                                            cced8e7fc07453, 1),
  • csi-aecfb984dbfbfe0cb3ba80326dcc23b15a9c2f0a01c-            • (csi-5704ae7a7f958a112c4ab6707b5b6708c839a7a23a-
    1e9620916c9e4, 0.5                                            8927ff774d5a38, 1),
  • csi-0ccc287f955294ea83afdc800030b453a8e37b1ee37-            • (csi-af40c043b23e299af5c85347534fe62d2c963a8f7d-
    157d83dcf04eb, 0.5                                            6b0dac873b8846, 4),
  • csi-f660fd4bbdf8ee1f7e501b27bc2a8223d96e0f47cda-            • (csi-535aa6a8940b19cbf86cda227104df4ff1f3c76e36-
    55d550d72973c, 0.5                                            eb17aa89585b91, 4),
  • csi-f660fd4bbdf8ee1f7e501b27bc2a8223d96e0f47cda-            • (csi-5deb4704be2267c6724151a6417770ceb5ffc47995-
    55d550d72973c, 0.5                                            607bbf3a169c28, 8),
  • csi-f660fd4bbdf8ee1f7e501b27bc2a8223d96e0f47cda-            • (csi-a4390ec528e4f6c2616765939087c14c1ca0bd47cf-
    55d550d72973c, 0.5                                            1ddd3b6d055ba0, 9),
                                                                • (csi-3f5a5b338144451e2d7e22bcc184940e796a74510e-
  • csi-f660fd4bbdf8ee1f7e501b27bc2a8223d96e0f47cda-
                                                                  c874966c88b93d, 12),
    55d550d72973c, 0.5
                                                                • (csi-953d891df68f6a2fd85d53da81602b86b0f04a395d-
  • csi-aa24b5e64bf83e78a707b01ad35bc3b6e22e06f9402-
                                                                  a9aa547b02a4a3, 16),
    a758631eee1bb, 1
  • csi-af40c043b23e299af5c85347534fe62d2c963a8f7d6-        H     Certification
    b0dac873b8846, 6
                                                            Besides carefully designing the parameter space of Grackle,
  • csi-f1d55b73677f250ea72db5a2658ffe0f92fc0197ea7-        we also perform various verification procedures to ensure the
    9717d372870d1, 7                                        soundness of the invented strategies.
  • csi-1bccc2cf890e2f92f021b591ec34371ebdd2a68741d-
    08de7fff0924e, 8                                        H.1    Proof Consistence Checking
                                                            One typical way to verify the correctness of proofs in CoCo
  • csi-5deb4704be2267c6724151a6417770ceb5ffc479956-        is to check whether the proofs of a prover are consistent
    07bbf3a169c28, 9                                        with other provers. Here, the consistency means that we
  • csi-a4390ec528e4f6c2616765939087c14c1ca0bd47cf1-        do not prove confluence (non-confluence) for a problem for
    ddd3b6d055ba0, 10                                       which other provers prove its non-confluence (confluence).
  • csi-36920a8f429f37ae80839d40e3cd805ef096f1aafbb-        We check whether the proofs found by invented strategies
    2dd6d7b845531, 12                                       are consistent with all provers in CoCo. The proofs found
                                                            by Grackle are depicted in the final portfolio grackle.flee.
  When using four CPU for the augmented dataset, the time   The check is done by stats/dif coco grackle.py, which com-
splits are presented below                                  pares the difference between results in grackle.flee and the
  • (csi-1f0dd05ed5c19b06c8c11b6dda27bd743c3b691c8f-        results obtained by CSI in CoCo2024. For proofs found
    f22150acb2c5e3, 0.5),                                   in grackle.flee but not by CSI in CoCo 2024, we manually
                                                            check the consistency between them and proofs of all provers
  • (csi-95e8deb6c1089354822fc19425ea6cab098fff49ea-
                                                            in the previous CoCo competitions. We also confirm that
    9ec5afb65da9da, 0.5),
                                                            the proofs obtained by the unified strategies are consistent
  • (csi-f660fd4bbdf8ee1f7e501b27bc2a8223d96e0f47cd-        with all provers in all CoCo competitions. This is done by
    a55d550d72973c, 0.5),                                   stats/consistency.py in our code.
  • (csi-36920a8f429f37ae80839d40e3cd805ef096f1aafb-
    b2dd6d7b845531, 0.5),
                                                            H.2    Certifying Newly Found Proofs
                                                            We run CeTA for each problem solved by invented strategies
  • (csi-042b74efcc92c96a15db35030eea542a97329bf422-        but not by CSI in CoCo. If it can be certified by CeTA, we
    cced8e7fc07453, 0.5),                                   trust the results. Otherwise, we manually look at the error
  • (csi-224dc655e2c823145f6a545fa78601d91e647dcfef-        information to see whether it is really an error and try to re-
    fb317d8f57b340, 0.5),                                   produce the proof and the certification error using the strategy
defined in CSI’s competition strategy. We aim to understand          however, they are used in CSI’s original competition
what changes they perform to the original strategy lead to the       strategy. From the invented strategy, we learn that it
proofs. From the analysis, we either slightly modify the sub-        can be proven with two modifications to the original
strategy defined in the competition strategy or directly use         competition strategy. First, increase the number of
some existing sub-strategies to produce the same answers as          repeated applications from two to five in AUTO INNER.
the invented strategies. These modifications that lead to the        It leads to AUTO INNER = (AUTO INNER0[30] |
answers are employed in the corresponding invented strate-           CPCS[5]2*)! | (AUTO INNER0[30]nono |
gies, which are small and sound according to our knowledge           CPCS[5]2*)5*!. Second, only run a subset of tech-
of term rewriting. We also check the certification errors out-       niques in AUTO INNER0. It leads to AUTO INNER0
put by CeTA to figure out whether they are indeed errors or          = (REDUNDANT DEL?;(CLOSED || DD ||
just caused by limitations of CSI and CeTA. The statistics of        SIMPLE || KB || AC || GROUNDnono))3*!
the certifications are shown in Table 2 of the paper.                If we only change AUTO INNER0 and AUTO INNER
   When we use four CPUs per CSI execution on ARI-COPS,              as mentioned above, CeTA can produce the same
we prove the following problems that are unprovable by CSI           certification error as the invented strategy.
in CoCo. We analyze each of them. The format is (strategy,         • (csi-b994d65167954d35cdd2b7a70646a4f8d550ec9e0de-
newly proved problems in ARI-COPS, corresponding prob-               bc650285a0d90, YES, 158.ari, 160.trs). Ackbo: no
lems in COPS). The results CERTIFIED means the proof is              XML output for SCFs.               CSI cannot output a
certified by CeTA.                                                   certificate for the ackbo processor with the flag -sc.
  • (csi-e5535657f8e54081f79c2291ebad9d81992f6e7248-                 The soundness of it has been explained in Section D.
    49f0fa92a83cc9, YES, 1499.ari, 1652.trs). The output             Moreover, CSI cannot produce a certificate for the
    is CERTIFIED.                                                    CPCS transformation. We can prove it by changing
                                                                     the definition of AUTO INNER0 to AUTO INNER0 =
  • (csi-9f19c01a538808477a8980f80d3d2face7303ce6f0-
                                                                     (REDUNDANT DEL?;(AC))3*!, which is used in
    58f8b6170f9461, YES, 879.ari, 1024.trs. The output
                                                                     the original AUTO INNER0. The new definition does
    is ./csi: XML output is not supported
                                                                     not parallelly execute all techniques in AUTO INNER0
    for this method. The reason why CeTA fails
                                                                     and makes the execution faster. Using AUTO INNER0
    to certify is CeTA does not support the certification
                                                                     = (REDUNDANT DEL?;(AC))3*!                   leads to the
    of Aoto-Toyama criteria. It can be proved by (at
                                                                     same certification error as the invented strategy. It is not
    -bound 16; SN)!. The strategy only changes the
                                                                     solved by CSI in CoCo 2024 but was solved by CSI in
    value of the -bound flag for AT3, which has been
                                                                     the previous CoCo competitions.
    used in the original competition strategy. Using (at
    -bound 16; SN)! leads to the same certification                • csi-b3ab9764cd4f0717a3037a5849e47d41c56af511e84-
    error as the invented strategy.                                  d4a72659e0829, YES, 1500.ari, 1653.trs. CPCS cannot
                                                                     be certified by CeTA. It can be proven by CPCS*.
  • (csi-9f6172de97a8148d22ba4b910ba8b16dccd0196c276-
                                                                     CPCS is defined in the competition strategy and the
    c568d9ab2c0b5, NO, 852.ari (997.trs), 846.ari
                                                                     soundness is guaranteed. Using CPCS* leads to the
    (991.trs)) CeTA cannot support the verification of
                                                                     same certification error as the invented strategy. It is not
    nonconfluence -idem.          However, the essen-
                                                                     solved by CSI in CoCo 2024 but was solved by CSI in
    tial for solving such two problems is the usage of
                                                                     the previous CoCo competitions.
    redundant -development 6, which is discov-
    ered by Grackle. Two problems can be solved if we               When we use one CPU per CSI execution on ARI-COPS,
    change redundant -narrowfwd -narrowbwd                       we prove the following problems that are unprovable by CSI
    -size 7 in REDUNDANT FC to redundant                         in CoCo.
    -development 6 -size 7. Moreover, they are                     • csi-0d382fd14a431f6befe533e561bbaf68c777bf48b92-
    certifiable.                                                     ccbbea5fd4346, NO, 449.ari, 540.trs, CERTIFIED.
  • csi-beb87b539aa3911f6c65d5e2a97ef40cb45898dfafc-               • csi-9e016d5ab9730720dcd426c5368545f09f0f5b9b464-
    7283f152a217a, YES, 794.ari, 939.trs, UNSUP-                     9cd6af41284ad, YES, 463.ari, 554.trs.       the
    PORTED. CeTA cannot certify AoTo-Toyama criteria.                critical pair g(h(f(f(b, b), b)))
    We can use AT defined in the competition strategy to             <- . -> g(h(h(f(f(h(k(k(b, b), b)),
    prove it. Using AT leads to the same certification error         h(k(k(b, b), b))), h(k(k(b, b),
    as the invented strategy.                                        b)))))) is not (almost) parallel
  • csi-ec0fb3f8ce9f2d586b23f5cd9c4a399845157f2854e-                 closed within None steps. hence
    f5f8e2f9d3f3a,      YES,      167.ari,     170.trs.              the following TRS is not (almost)
    UNSUPPORTED                     Fatal: parse                     parallel closed.           CeTA cannot certify
    error on <acRuleRemoval> at                                      the cr -okui technique.     We can prove it if
    [trsTerminationProof, wcrAndSN,                                  we change AUTO INNER0 to AUTO INNER0
    crProof, redundantRules, crProof,                                = (REDUNDANT DEL?;(CLOSED))3*! ||
    proof, certificationProblem].               CeTA                 ((CLOSED | REDUNDANT RHS)3*! ||
    does not support AC confluence proving techniques;               (CLOSED) | REDUNDANT JS)3*!,          which is
      used in the original definition of AUTO INNER0. The          statusPrecedence, pathOrder,
      modified definition causes the same certification error      redPair, orderingConstraintProof,
      as the invented strategy.                                    ruleRemoval, trsTerminationProof,
  • csi-0e7e3ba5c042fabdf8151556dc8b26717d98bcd49c2-               wcrAndSN, crProof, proof,
    3193ec7f29d33, YES, 166.ari, 169.trs.         ./csi:           certificationProblem]. CeTA cannot verify
    XML output is not supported for this                           AC processors.
    method. CSI cannot output certificates for Aoto-             • Fatal: parse error
    Toyama criteria. It can be proven by (at -bound                on <acRuleRemoval> at
    16 -theorem 2; SN)! where SN is defined in the                 [trsTerminationProof, wcrAndSN,
    original competition strategy. We only change -bound           crProof, redundantRules, crProof,
    16 to increase the search space as explained in Sec-           proof, certificationProblem]. CeTA does
    tion D. The strategy (at -bound 16 -theorem                    not support AC confluence proving techniques
    2; SN)! causes the same certification error as the
    invented strategy.                                           • Error in checking parallel closedness
                                                                   for the rewrite system ... The
  • csi-aabfb22bdd5b365b18568e462dd644b3a94146e63d2-               critical pair XXX is not (almost)
    c44ff35c98a2c, NO, 846.ari(991.trs), 852.ari(997.trs),         parallel closed within None steps.
    CERTIFIED.                                                     hence the following TRS is not
  • (csi-d42ec2e614b9f4287137c1772a4a13176783da5195-               (almost) parallel closed.                CSI outputs
    2c630b016bc7c4, YES, 158.ari, 160.trs). Ackbo:                 an empty certificate for the CPCS transformation
    no XML output for SCFs. CSI cannot output a                    and Church Rosser Transformation Processor (okui),
    certificate for the ackbo processor with the flag -sc.         confusing CeTA there are no proof steps.
    The soundness of it has been explained in Section D.         • Fatal: parse error on
    Moreover, CSI cannot produce a certificate for the             <unknownAssumption> at [proof,
    CPCS transformation. We can prove it by changing               certificationProblem]. CSI uses a theo-
    the definition of AUTO INNER0 to AUTO INNER0 =                 rem that is not supported by CeTA.
    (REDUNDANT DEL?;(AC))3*!, which is used in
    the original AUTO INNER0. The new definition does            • ./csi: order-sorted decomposition:
    not parallelly execute all techniques in AUTO INNER0           xml proof not supported.            CeTA does not
    and makes the execution faster. It is not solved by CSI        support order-sorted decomposition.
    in CoCo 2024 but was solved by CSI in the previous           • Fatal: parse error on text element
    CoCo competitions. The strategy AUTO INNER0 =                  "-1" at [stronglyClosed, crProof,
    (REDUNDANT DEL?;(AC))3*! causes the same                       redundantRules, crProof, proof,
    certification error as the invented strategy.                  certificationProblem].             CSI implements
  • csi-b3ab9764cd4f0717a3037a5849e47d41c56af511e84-               some development closedness techniques that cannot be
    d4a72659e0829, YES, 1500.ari, 1653.trs. CPCS cannot            verified by CeTA.
    be certified by CeTA. It can be proven by CPCS*.             • Fatal: parse error on <uncurry> at
    CPCS is defined in the competition strategy and the            [proof, certificationProblem]. Uncurry is
    soundness is guaranteed. It is not solved by CSI in            not supported by CeTA.
    CoCo 2024 but was solved by CSI in the previous CoCo
    competition. CPCS* causes the same certification error       • Could not infer that X and Y are
    as the invented strategy.                                      not joinable, could not ensure
                                                                   closure under rewriting for first
H.3    Certifying Strategies on Mastered Problems                  automaton, problem when ensuring
For every invented strategy in the ARI-COPS dataset, we run        (state-)compatibility of TRS with
it on the problems it matsered and try to certify the proofs.      TA. The processor nonconfluence -tree cannot
The problems mastered by each strategy is calculated by            be verified. Need to use nonconfluence -tree
Grackle. Since the outputs of CeTA on such problems are            -cert.
indeed lengthy, we do not present them in the technical ap-      • Fatal: parse error on <magic> at
pendix. The outputs exist in the attached code. We refer           [nonJoinableFork, crDisproof, proof,
readers to read such logs for details. As explained in the         certificationProblem].         The technique
main paper, CeTA may fail to certify the proofs due to several     nonconfluence -idem is not supported by CeTA.
reasons. We manually check whether the outputs indeed de-
                                                                 • Error when closing critical pairs of
note errors. We have not found any unsoundness. The typical
                                                                   rules, C not a subsystem of R, hence
reasons why CeTA’s rejection information does not indicate
                                                                   the following TRS is not critical
unsoundness are shown below.
                                                                   pair closing rewrite system. The tech-
  • Fatal: parse error on <ac>                                     nique cr -cpcs2 is not certifiable. It should be
    at [statusPrecedenceEntry,                                     changed to cr -cpcs2 -cpcscert for certi-
  fication. But cr -cpcs2 is used in the original
  competition strategy.
• Error below strong normalization +
  wcr; R is not empty in the following
  termination-problem. The usage of AC proces-
  sors makes CSI output an empty proof; thus, confusing
  CeTA.
• ./csi: MatrixInterpretation.fprintfx:
  XML output not supported expecting
  "<", but found: ’’ CPCS is not supported,
  and sometimes outputs entire empty certificates.
• ./csi: XML output is not supported
  for this method. CSI does not implement the
  functions to output the certificates for some processors.
• parser error : Excessive depth in
  document. The certificate is too large for CeTA to
  parse.
• Ackbo: no XML output for SCFs CSI can-
  not output a certificate for ackbo -sc. However it is
  used in the original competition strategy, and its sound-
  ness has been explained in Section D.
• ./csi: not an integer. CSI cannot generate a
  certificate if kbo uses rational weights. The soundness
  of rational weights is explained in Section D
• could not apply the reduction
  pair processor with the following
  polynomial interpretation over
  polynomial interpretation.                  CeTA can-
  not certify the flag -heuristic 1 for the poly
  processor. But poly -heuristic 1 is used in the
  original competition strategy, and its soundness has
  been explained in Section D. From the proofs, we know
  we can use DD to prove the problems, which are defined
  in the competition strategy. We can also reproduce the
  certification error if we only use DD and CeTA.
References                                                      [Freund and Schapire, 1997] Yoav Freund and Robert E
[Abate et al., 2021] Alessandro Abate, Mirco Giacobbe, and         Schapire. A decision-theoretic generalization of on-line
                                                                   learning and an application to boosting. Journal of com-
   Diptarko Roy. Learning probabilistic termination proofs.
                                                                   puter and system sciences, 55(1):119–139, 1997.
   In Computer Aided Verification: 33rd International Con-
   ference, CAV 2021, Virtual Event, July 20–23, 2021, Pro-     [Gebhardt et al., 2007] Andreas Gebhardt, Dieter Hofbauer,
   ceedings, Part II 33, pages 3–26. Springer, 2021.               and Johannes Waldmann. Matrix evolutions. In Proc.
[Aleksandrova et al., 2024] Kristina Aleksandrova, Jan             Workshop on Termination, Paris, 2007.
   Jakubuv, and Cezary Kaliszyk.           Prover9 unleashed:   [Giacobbe et al., 2022] Mirco Giacobbe, Daniel Kroening,
   Automated configuration for enhanced proof discovery. In        and Julian Parsert. Neural termination analysis. In Pro-
   Proceedings of 25th Conference on Logic for Pro, volume         ceedings of the 30th ACM Joint European Software Engi-
   100, pages 360–369, 2024.                                       neering Conference and Symposium on the Foundations of
[Aoto and Toyama, 2012] Takahito Aoto and Yoshihito                Software Engineering, pages 633–645, 2022.
   Toyama. A reduction-preserving completion for proving        [Giesl et al., 2005a] Jürgen Giesl, René Thiemann, and Peter
   confluence of non-terminating term rewriting systems.           Schneider-Kamp. The dependency pair framework: Com-
   Logical Methods in Computer Science, 8, 2012.                   bining techniques for automated termination proofs. In In-
                                                                   ternational Conference on Logic for Programming Artifi-
[Aoto et al., 2014] Takahito Aoto, Yoshihito Toyama, and
                                                                   cial Intelligence and Reasoning, pages 301–331. Springer,
   Kazumasa Uchida. Proving confluence of term rewrit-             2005.
   ing systems via persistency and decreasing diagrams. In
   Rewriting and Typed Lambda Calculi: Joint International      [Giesl et al., 2005b] Jürgen Giesl, René Thiemann, and Pe-
   Conference, RTA-TLCA 2014, Held as Part of the Vienna           ter Schneider-Kamp. Proving and disproving termination
   Summer of Logic, VSL 2014, Vienna, Austria, July 14-17,         of higher-order functions. In International Workshop on
   2014. Proceedings 25, pages 46–60. Springer, 2014.              Frontiers of Combining Systems, pages 216–231. Springer,
                                                                   2005.
[Baader and Nipkow, 1998] Franz Baader and Tobias Nip-
   kow. Term rewriting and all that. Cambridge university       [Gramlich, 1996] Bernhard Gramlich. Confluence without
   press, 1998.                                                    termination via parallel critical pairs. In Colloquium
                                                                   on Trees in Algebra and Programming, pages 211–225.
[Bachmair and Ganzinger, 1994] Leo Bachmair and Harald
                                                                   Springer, 1996.
   Ganzinger. Rewrite-based equational theorem proving
   with selection and simplification. Journal of Logic and      [He et al., 2023] Guoliang He, Zak Singh, and Eiko Yoneki.
   Computation, 4(3):217–247, 1994.                                Mcts-geb: Monte carlo tree search is a good e-graph
                                                                   builder. In Proceedings of the 3rd Workshop on Machine
[Bezem et al., 2003] Marc Bezem, Jan Willem Klop, and              Learning and Systems, pages 26–33, 2023.
   Roel de Vrijer. Term rewriting systems. Cambridge Uni-
   versity Press, 2003.                                         [Hirokawa, 2006] Nao Hirokawa. Automated termination
                                                                   analysis for term rewriting. Citeseer, 2006.
[Brown and Kaliszyk, 2022] Chad E Brown and Cezary
   Kaliszyk. Lash 1.0 (system description). In International    [Huet, 1980] Gérard Huet. Confluent reductions: Abstract
   Joint Conference on Automated Reasoning, pages 350–             properties and applications to term rewriting systems: Ab-
   358. Springer, 2022.                                            stract properties and applications to term rewriting sys-
                                                                   tems. Journal of the ACM (JACM), 27(4):797–821, 1980.
[De Moura and Bjørner, 2008] Leonardo De Moura and
   Nikolaj Bjørner. Z3: An efficient smt solver. In In-         [Hůla and Jakubův, 2022] Jan Hůla and Jakubův. Targeted
   ternational conference on Tools and Algorithms for the          configuration of an smt solver. In International Confer-
   Construction and Analysis of Systems, pages 337–340.            ence on Intelligent Computer Mathematics, pages 256–
   Springer, 2008.                                                 271. Springer, 2022.
[Endrullis et al., 2008] Jörg Endrullis, Johannes Waldmann,    [Hutter et al., 2009] Frank Hutter, Holger H Hoos, Kevin
   and Hans Zantema. Matrix interpretations for proving ter-       Leyton-Brown, and Thomas Stützle. Paramils: an auto-
   mination of term rewriting. Journal of Automated Reason-        matic algorithm configuration framework. Journal of arti-
   ing, 40:195–220, 2008.                                          ficial intelligence research, 36:267–306, 2009.
[Felgenhauer et al., 2015] Bertram Felgenhauer, Aart Mid-       [James and Fabian, 2023] Fox James and Mitterwallner
   deldorp, Harald Zankl, and Vincent Van Oostrom. Layer           Fabian, 2023.
   systems for proving confluence. ACM Transactions on          [Kerschke et al., 2019] Pascal Kerschke, Holger H Hoos,
   Computational Logic (TOCL), 16(2):1–32, 2015.                   Frank Neumann, and Heike Trautmann. Automated al-
[Felgenhauer, 2012] Bertram Felgenhauer. Deciding conflu-          gorithm selection: Survey and perspectives. Evolutionary
   ence of ground term rewrite systems in cubic time. In 23rd      computation, 27(1):3–45, 2019.
   International Conference on Rewriting Techniques and         [Klein and Hirokawa, 2012] Dominik Klein and Nao Hi-
   Applications (RTA’12)(2012). Schloss-Dagstuhl-Leibniz           rokawa. Confluence of non-left-linear trss via relative
   Zentrum für Informatik, 2012.                                  termination. In International Conference on Logic for
  Programming Artificial Intelligence and Reasoning, pages      [Neurauter et al., 2010] Friedrich Neurauter, Aart Middel-
  258–273. Springer, 2012.                                         dorp, and Harald Zankl. Monotonicity criteria for polyno-
                                                                   mial interpretations over the naturals. In Automated Rea-
[Knuth and Bendix, 1983] Donald E Knuth and Peter B
                                                                   soning: 5th International Joint Conference, IJCAR 2010,
  Bendix. Simple word problems in universal algebras. Au-          Edinburgh, UK, July 16-19, 2010. Proceedings 5, pages
  tomation of Reasoning: 2: Classical Papers on Computa-           502–517. Springer, 2010.
  tional Logic 1967–1970, pages 342–376, 1983.
                                                                [Neurauter, 2012] Friedrich Neurauter. Termination analysis
[Koprowski and Waldmann, 2008] Adam Koprowski and Jo-              of term rewriting by polynomial interpretations and matrix
  hannes Waldmann. Arctic termination... below zero. In In-        interpretations. na, 2012.
  ternational Conference on Rewriting Techniques and Ap-
  plications, pages 202–216. Springer, 2008.                    [Oyamaguchi and Hirokawa, 2014] Michio            Oyamaguchi
                                                                   and Nao Hirokawa. Confluence and critical-pair-closing
[Korp and Middeldorp, 2009] Martin Korp and Aart Middel-           systems. Proc. 3rd IWC, pages 29–33, 2014.
  dorp. Match-bounds revisited. Information and Computa-
                                                                [Ramı́rez et al., 2016] Nicolás Gálvez Ramı́rez, Youssef
  tion, 207(11):1259–1283, 2009.
                                                                   Hamadi, Eric Monfroy, and Frédéric Saubion. Evolving
[Korp et al., 2009] Martin Korp, Christian Sternagel, Harald       smt strategies. In 2016 IEEE 28th International Confer-
  Zankl, and Aart Middeldorp. Tyrolean termination tool 2.         ence on Tools with Artificial Intelligence, 2016.
  In Rewriting Techniques and Applications: 20th Interna-       [Sakai et al., 2015] Masahiko Sakai, Michio Oyamaguchi,
  tional Conference, RTA 2009 Brası́lia, Brazil, June 29-July
                                                                   and Mizuhito Ogawa. Non-e-overlapping, weakly shal-
  1, 2009 Proceedings 20, pages 295–304. Springer, 2009.
                                                                   low, and non-collapsing trss are confluent. In Automated
[Lindauer et al., 2022] Marius   Lindauer,       Katharina         Deduction-CADE-25: 25th International Conference on
   Eggensperger, Matthias Feurer, André Biedenkapp,               Automated Deduction, Berlin, Germany, August 1-7, 2015,
   Difan Deng, Carolin Benjamins, Tim Ruhkopf, René               Proceedings 25, pages 111–126. Springer, 2015.
   Sass, and Frank Hutter. Smac3: A versatile bayesian          [Sternagel and Thiemann, 2013] Christian Sternagel and
   optimization package for hyperparameter optimization.           René Thiemann. Formalizing knuth-bendix orders and
   Journal of Machine Learning Research, 23(54):1–9, 2022.         knuth-bendix completion. In 24th International Con-
[McCune, 2005] W. McCune. Prover9 and Mace4. http:                 ference on Rewriting Techniques and Applications (RTA
  //www.cs.unm.edu/∼mccune/prover9/, 2005. Accessed:               2013). Schloss-Dagstuhl-Leibniz Zentrum für Informatik,
  2025-05-21.                                                      2013.
[Meseguer, 2003] José Meseguer. Software specification and     [Sternagel and Thiemann, 2014a] Christian Sternagel and
  verification in rewriting logic. Nato Science Series Sub         René Thiemann. The certification problem format. arXiv
  Series III Computer and Systems Sciences, 191:133–194,           preprint arXiv:1410.8220, 2014.
  2003.                                                         [Sternagel and Thiemann, 2014b] Christian Sternagel and
[Moser et al., 2008] Georg Moser, Andreas Schnabl, and Jo-         René Thiemann. Formalizing monotone algebras for cer-
                                                                   tification of termination and complexity proofs. In Inter-
  hannes Waldmann. Complexity analysis of term rewrit-
                                                                   national Conference on Rewriting Techniques and Appli-
  ing based on matrix and context dependent interpreta-
                                                                   cations, pages 441–455. Springer, 2014.
  tions. In IARCS Annual Conference on Foundations of
  Software Technology and Theoretical Computer Science          [Sternagel, 2016] Christian Sternagel. The generalized sub-
  (2008). Schloss-Dagstuhl-Leibniz Zentrum für Informatik,        term criterion in ttt2. arXiv preprint arXiv:1609.03432,
  2008.                                                            2016.
[Nagele and Middeldorp, 2016] Julian Nagele and Aart Mid-       [Stump et al., 2014] Aaron Stump, Geoff Sutcliffe, and Ce-
  deldorp. Certification of classical confluence results for       sare Tinelli. Starexec: A cross-community infrastructure
  left-linear term rewrite systems. In International Con-          for logic solving. In International joint conference on au-
  ference on Interactive Theorem Proving, pages 290–306.           tomated reasoning, pages 367–373. Springer, 2014.
  Springer, 2016.                                               [Suzuki et al., 2011] Sho Suzuki, Keiichirou Kusakari, and
[Nagele et al., 2015] Julian Nagele, Bertram Felgenhauer,          Frédéric Blanqui. Argument filterings and usable rules in
  and Aart Middeldorp. Improving automatic confluence              higher-order rewrite systems. IPSJ Online Transactions,
  analysis of rewrite systems by redundant rules. In 26th In-      4:114–125, 2011.
  ternational Conference on Rewriting Techniques and Ap-        [Thiemann and Sternagel, 2009] René Thiemann and Chris-
  plications (RTA 2015). Schloss Dagstuhl-Leibniz-Zentrum          tian Sternagel. Certification of termination proofs using
  fuer Informatik, 2015.                                           ceta. In International Conference on Theorem Proving in
[Nagele et al., 2017] Julian Nagele, Bertram Felgenhauer,          Higher Order Logics, pages 452–468. Springer, 2009.
  and Aart Middeldorp. Csi: New evidence–a progress re-         [Toyama and Oyamaguchi, 1994] Yoshihito Toyama and
  port. In International Conference on Automated Deduc-            Michio Oyamaguchi. Church-rosser property and unique
  tion, pages 385–397. Springer, 2017.                             normal form property of non-duplicating term rewriting
   systems. In International Workshop on Conditional Term
   Rewriting Systems, pages 316–331. Springer, 1994.
[Van Oostrom, 1994] Vincent Van Oostrom. Confluence
   by decreasing diagrams. Theoretical computer science,
   126(2):259–280, 1994.
[Van Oostrom, 1997] Vincent Van Oostrom. Developing de-
   velopments. Theoretical Computer Science, 175(1):159–
   181, 1997.
[Willsey et al., 2021] Max Willsey, Chandrakana Nandi,
   Yisu Remy Wang, Oliver Flatt, Zachary Tatlock, and Pavel
   Panchekha. Egg: Fast and extensible equality saturation.
   Proceedings of the ACM on Programming Languages,
   5(POPL):1–29, 2021.
[Winkler and Moser, 2019] Sarah Winkler and Georg Moser.
   Smarter features, simpler learning? In Proceedings of the
   Second International Workshop on Automated Reasoning:
   Challenges, Applications, Directions, Exemplary Achieve-
   ments, 2019.
[Xu et al., 2010] Lin Xu, Holger Hoos, and Kevin Leyton-
   Brown. Hydra: Automatically configuring algorithms for
   portfolio-based selection. In Proceedings of the AAAI
   Conference on Artificial Intelligence, volume 24, pages
   210–216, 2010.
[Yamada et al., 2016] Akihisa Yamada, Sarah Winkler, Nao
   Hirokawa, and Aart Middeldorp. Ac-kbo revisited. The-
   ory and Practice of Logic Programming, 16(2):163–188,
   2016.
[Zankl and Middeldorp, 2010] Harald Zankl and Aart Mid-
   deldorp. Satisfiability of non-linear (ir) rational arith-
   metic. In Logic for Programming, Artificial Intelligence,
   and Reasoning: 16th International Conference, LPAR-16,
   Dakar, Senegal, April 25–May 1, 2010, Revised Selected
   Papers 16, pages 481–500. Springer, 2010.
[Zankl et al., 2009] Harald Zankl, Nao Hirokawa, and Aart
   Middeldorp. Kbo orientability. Journal of Automated Rea-
   soning, 43(2):173–201, 2009.
[Zankl et al., 2011] Harald Zankl, Bertram Felgenhauer, and
   Aart Middeldorp. Csi–a confluence tool. In Automated
   Deduction–CADE-23: 23rd International Conference on
   Automated Deduction, Wrocław, Poland, July 31-August
   5, 2011. Proceedings 23, pages 499–505. Springer, 2011.
[Zantema, 2004] Hans Zantema. Relative termination in
   term rewriting. In WST’04 7th International Workshop on
   Termination, page 51, 2004.
