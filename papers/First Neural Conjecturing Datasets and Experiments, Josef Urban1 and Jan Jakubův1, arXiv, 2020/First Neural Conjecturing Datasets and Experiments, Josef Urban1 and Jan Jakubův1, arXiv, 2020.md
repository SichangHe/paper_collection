                                                              First Neural Conjecturing
                                                              Datasets and Experiments?

                                                                      Josef Urban1 and Jan Jakubův1

                                             Czech Institute of Informatics, Robotics and Cybernetics, Prague, Czech Republic
arXiv:2005.14664v1 [cs.AI] 29 May 2020




                                                  Abstract. We describe several datasets and first experiments with cre-
                                                  ating conjectures by neural methods. The datasets are based on the Mizar
                                                  Mathematical Library processed in several forms and the problems ex-
                                                  tracted from it by the MPTP system and proved by the E prover using
                                                  the ENIGMA guidance. The conjecturing experiments use the Trans-
                                                  former architecture and in particular its GPT-2 implementation.


                                         1      Introduction and Related Work
                                         Automated creation of suitable conjectures is one of the hard problems in au-
                                         tomated reasoning over large mathematical corpora. This includes tasks such
                                         as (i) conjecturing suitable intermediate lemmas (cuts) when proving a harder
                                         conjecture, and (ii) unrestricted creation of interesting conjectures based on the
                                         previous theory (i.e., theory exploration). Starting with Lenat’s AM [10], several
                                         systems such as the more specialized Graffitti by Fajtlowicz [4], and Colton’s
                                         HR [3] have been developed, typically using heuristics for theory exploration or
                                         limited brute-force enumeration, controlled e.g. by the type system [7].
                                             Our motivation is the work of Karpathy1 with recurrent neural networks
                                         (RNNs). One of his experiments used the Stacks project, generating LaTeX-
                                         style pseudo-mathematics that looked quite credible to non-experts. We have
                                         repeated these experiments over the Mizar library using Karpathy’s RNNs in
                                         2016, but the results did not seem convincing. The neural methods have however
                                         improved since, coming up with stronger methods and systems such as attention,
                                         transformer and GPT-2 [12]. The experiments described here started by testing
                                         GPT-2 on the Mizar library, gradually producing several more datasets.
                                             Related work includes research on the informal-to-formal grammar-based and
                                         neural translation [9,8,17,16]. There it was found that PCFGs and RNNs with at-
                                         tention work well on some informal-to-formal datasets, can learn analogies from
                                         the data, and can be used to produce multiple formal outputs of which some are
                                         new provable conjectures. In [16] we use this together with type checking to set
                                         up a data-augmentation loop between the neural learner and the type-checker.
                                         Such learning-reasoning loops are also planned for the datasets presented here.
                                         ?
                                             Funded by the AI4REASON ERC Consolidator grant nr. 649043 and by the Czech
                                             project AI&Reasoning CZ.02.1.01/0.0/0.0/15 003/0000466 and the European Re-
                                             gional Development Fund. We thank K. Chvalovský and T. Gauthier for discussions.
                                         1
                                             http://karpathy.github.io/2015/05/21/rnn-effectiveness/
2         Urban, Jakubův

Similar experiments are done in [6] and by Chvalovský2 . Gauthier has been
working on term synthesis using Monte-Carlo Tree Search and reinforcement
learning with semantic feedback [1,5].

2     Datasets
The datasets for neural conjecturing are available from our web page3 . We have
so far experimented with the following data:

1. All Mizar articles (MML version 1147), stripped of comments and concate-
   nated together4 . This is 78M of uncompressed text.
2. Text version of the HTML export [14] of the MML articles5 . This unpacks to
   156MB. It additionally contains disambiguation features such as full types
   of variables, full names of theorems and the thesis is printed after every
   natural deduction step. This seems useful for neural conjecturing because
   the context is repeated more often.
3. Tokenized TPTP proofs6 of 28271 Mizar theorems translated by the MPTP
   system [15]. The proofs are produced by the E prover [13] equipped with
   recent ENIGMA guidance [2]. This unpacks to 658MB.
4. A subselection of the used Mizar premises from the 28271 proofs printed
   in prefix notation7 . These files always start with the conjecture, and the
   premises are printed in the order in which E used them in its proof. This
   unpacks to 53MB.
Below we show short examples of the four kinds of data, all for the theorem
ZMODUL01:103:
theorem
  for W being strict Submodule of V holds W /\ W = W
  proof
    let W be strict Submodule of V;
    the carrier of W = (the carrier of W) /\ (the carrier of W);
    hence thesis by Def15;
  end;

theorem :: ZMODUL01:103
for V being Z_Module
for W being strict Submodule of V holds W /\ W = W
proof
let V be Z_Module; ::_thesis: for W being strict Submodule of V holds W /\ W = W
let W be strict Submodule of V; ::_thesis: W /\ W = W
2
    http://aitp-conference.org/2019/abstract/AITP_2019_paper_27.pdf,    http://aitp-conference.
    org/2020/abstract/paper_21.pdf
3
    http://grid01.ciirc.cvut.cz/~mptp/nn_conj20/
4
    http://grid01.ciirc.cvut.cz/~mptp/nn_conj20/datasets/mmlall.txt2
5
    http://grid01.ciirc.cvut.cz/~mptp/nn_conj20/datasets/html2.tar.gz
6
    http://grid01.ciirc.cvut.cz/~mptp/nn_conj20/datasets/prf2.tar.gz
7
    http://grid01.ciirc.cvut.cz/~mptp/nn_conj20/datasets/prf7.tar.gz
                            First Neural Conjecturing Datasets and Experiments               3

 the carrier of W = the carrier of W /\ the carrier of W ;
hence W /\ W = W by Def15; ::_thesis: verum
end;

fof ( d15_zmodul01 , axiom , ! [ X1 ] : ( ( ( ( ( ( ( ( ( ( ~ ( v2_struct_0 ...
fof ( idempotence_k3_xboole_0 , axiom , ! [ X1 , X2 ] : k3_xboole_0 ( ...
fof ( t103_zmodul01 , conjecture , ! [ X1 ] : ( ( ( ( ( ( ( ( ( ( ~ ( ...
fof ( c_0_3 , plain , ! [ X118 , X119 , X120 , X121 ] : ( ( X121 ! = ...
cnf ( c_0_6 , plain , ( X1 = k7_zmodul01 ( X4 , X2 , X3 ) | v2_struct_0 ...

c! b0     c=> c& c~ cv2_struct_0 b0 c& cv13_algstr_0 b0 c& cv2_rlvect_1 b0 c& ...
c! b0     c=> c& c~ cv2_struct_0 b0 c& cv13_algstr_0 b0 c& cv2_rlvect_1 b0 c& ...
c! b0      c! b1 c= ck3_xboole_0 b0 b0 b0


3     Experiments
The basic experiment for each dataset consists of training the smallest (117M
parameters) version of GPT-2 on a NVIDIA GeForce GTX 1080 GPU with
12GB RAM, producing random unconditioned samples during the training. The
produced samples and the most recent trained models are available from our
web page8 . The published models can be used for conditional and unconditional
generation of Mizar-like texts, proofs and premise completion. The samples con-
tain megabytes of examples of what can be generated and how the generated
texts improve during the training. The training on the third dataset was stopped
early. The large number of redundant tokens such as brackets and commas led
us to produce the fourth dataset that uses the punctuation-free prefix notation
and much shorter summary of the E proof (just the premises in their order).
The training for datasets 1, 2 and 4 has been running for several weeks, with
the performance still slowly improving. See Figure 1 in Appendix A for a sample
training and loss on dataset 2. There are many interesting conjectures generated
during the unconditioned sampling. The trained models can be directly used by
Mizar users for autocompletion of their texts. Some examples compared to real
theorems are shown below. More semantic evaluation on the textual datasets (1
and 2) could be done in various ways. We imagine that a proper Mizar environ-
ment will have to be guessed, some assumptions may be automatically added,
etc.

# real MML theorem
theorem :: YELLOW10:61
for S, T being non empty up-complete Poset
for X being Subset of S
for Y being Subset of T st X is property(S) & Y is property(S) holds
[:X,Y:] is property(S)

# generated similar "theorem"
theorem :: WAYBEL30:56
for R being complete Lattice
8
    http://grid01.ciirc.cvut.cz/~mptp/nn_conj20/samples/, http://grid01.ciirc.cvut.cz/~mptp/nn_
    conj20/models/
4         Urban, Jakubův

for X being Subset of [:R,R:] st X is upper & X is property(S) holds
[:X,X:] is property(S)

# real MML theorem
theorem :: SEQ_4:47
for X being non empty real-membered set
for Y being real-membered set st X c= Y & Y is bounded_below holds
lower_bound Y <= lower_bound X

# generated similar "theorem"
theorem Th33: :: SEQ_4:33
for X being real-membered set
for Y being real-membered set st Y is bounded_below & X c= Y holds
lower_bound Y <= lower_bound X

# generated "theorem" with "proof"
theorem Th23: :: STIRL2_1:23
for X, Y being finite set st not X is empty & X c= Y &
card X = card Y holds X = Y
proof
let X, Y be finite set ; ::_thesis: ( not X is empty & X c= Y &
card X = card Y implies X = Y )
assume that
A1: not X is empty and A2: X c= Y and A3: card X = card Y ; ::_thesis: X = Y
 card (Y \ X) = (card Y) - (card X) by A1, A3, CARD_2:44;
then A4: card (Y \ X) = ((card Y) - 1) - (card X) by CARD_1:30;
 X = Y \ X by A2, A3, Th22;
hence X = Y by A4, XBOOLE_0:def_10; ::_thesis: verum
end;


3.1     Conditioned completion
We have also done two initial experiments with proof and formula completion.
The data and results for them are available from our web page9 . In the first
experiment, we use a model trained on Dataset 4 (premises), and ask the model
to auto-complete 369 theorems from the CARD series of Mizar. For each conjec-
ture we produce 10 premise selections using beam search, and we use different
temperatures and beam search parameters. An interesting phenomenon is that
with low temperatures, practically all conjectured premises are known Mizar
theorems. I.e., the task reduces to standard premise selection. With higher tem-
peratures, GPT-2 starts producing premises (lemmas) that are not among the
existing Mizar theorems, but are still well-typed. Even higher temperatures lead
to non-well-typed or even unparsable lemmas. The next section provides a more
involved ATP evaluation done on a larger dataset.
    The second experiment was done over Dataset 2 and a set of 462 partial
formulas from the CARD articles. The model trained on Dataset 2 is then (again
9
    http://grid01.ciirc.cvut.cz/~mptp/nn_conj20/samples/premises/, http://grid01.ciirc.cvut.cz/
    ~mptp/nn_conj20/samples/html2/
                            First Neural Conjecturing Datasets and Experiments          5

using beam search) asked to auto-complete these formulas. Mizar users can also
play with such autocompletion via a web server10 using this model. For example,
for M, N being Cardinal holds
results in the following (selected) auto-completions (more are available online11 ):
( M = N iff M,N are_equipotent )
( M = N iff not 0 in M ) by ORDINAL3:8;
M *‘ N = N *‘ M
( M in N iff not M c= N )
the_rank_of M = the_rank_of N by Th77;
nextcard (Sum M) = M *‘ N

3.2      Initial ATP Evaluation
The first larger ATP (semantic) evaluation uses the fourth dataset following the
setting introduced for such evaluations in [6]. After training GPT-2 on the 28271
ENIGMA proofs, we produce (using beam search) 12 GPT-2 premise predictions
for a set of 31792 theorems of which 6639 are not among the training ones. This
yields 381432 predictions,12 deduplicated to 193320 unique predictions. The pre-
dictions are converted back to TPTP from the polish notation, creating ATP
problems. We distinguish between the premises that already exist as Mizar theo-
rems and definitions, and the new formulas (conjectures) introduced by GPT-2.
10856413 of the created problems contain no new conjectures, i.e., GPT-2 works
there as a standard premise selector similar to [11].
    Most (86899) of these ATP problems14 can be quickly shown to be coun-
tersatisfiable by E prover.15 This shows the first difference between syntactic
loss as used by the ML/NLP community and semantic usefulness. GPT-2’s loss
is geared towards mimicking the length of the original texts with a small num-
ber of syntactic mistakes. In premise selection, the underlying task is to generate
premises that have sufficient logical power. Overshooting is better than making a
mistake and observing the usual length of the text. 11866 of the problems can be
proved in 6 s, resulting in proofs of 8105 theorems. This is not yet an interesting
number, because GPT-2 does not observe the chronological order of premises.
E.g., 4350 of the proofs use only a single premise – typically GPT-2 suggested
the proved theorem itself as a premise. Still, some predictions are chronologically
correct and lead to correct new proofs. E.g. for theorem XXREAL 1:48,16 which
is not in the training set, the fifth GPT-2 sample proposed 7 premises17 of which
5 were used in a quickly found new E proof18 (see Appendix A for details).
10
     http://grid01.ciirc.cvut.cz:8000/
11
     http://grid01.ciirc.cvut.cz/~mptp/nn_conj20/samples/html2/00cardmizout1_t1
12
     http://grid01.ciirc.cvut.cz/~mptp/nn_conj20/results/preds3.tar.gz
13
     http://grid01.ciirc.cvut.cz/~mptp/nn_conj20/results/preds5.tar.gz
14
     http://grid01.ciirc.cvut.cz/~mptp/nn_conj20/results/preds6.tar.gz
15
     We used E with 6 s time limit and its auto-schedule mode for this initial check.
16
     http://grid01.ciirc.cvut.cz/~mptp/7.13.01_4.181.1147/html/xxreal_1.html#T48
17
     http://grid01.ciirc.cvut.cz/~mptp/nn_conj20/results/t48_xxreal_1___5
18
     http://grid01.ciirc.cvut.cz/~mptp/nn_conj20/results/t48_xxreal_1___5.out
6          Urban, Jakubův

    Next we evaluate19 the 44524 problems20 that do use at least one newly
proposed premise. We have not strictly enforced the chronology, but remove the
theorem itself from axioms if proposed. 34675 of the problems are then found
countersatisfiable by E in 1 s and for 1515 a proof is found. The conjectures may
be interesting, even though hard to prove automatically: E.g. for GROUPP -
1:T1021 a valid, though not quite trivial strengthening from finite to general
groups is proposed, see Appendix A for details.
    In total, GPT-2 proposed in this experiment 52515 new syntactically correct
formulas22 that deduplicate to 33100. Some are clearly false, yet quite natural
to ask: e.g. for dozens of theorems like SINCOS10:1723 – “sec is increasing
on [0, π/2)” – GPT-2 makes the conjecture that every differentiable function is
increasing.24 In this particular case we can likely disprove the conjecture since
there are counterexamples in the MML. Similarly, in FUNCTOR1:925 , to prove
that the composition of full functors is full, GPT-2 proposes to reduce fullness
to faithfulness, likely because a previous theorem26 says that faithfulness is pre-
served under composition. See Appendix A for details.
    Finally we use standard premise selection (although we could recurse and
use GPT-2) and E with the ENIGMA guidance to try to prove the 52515 new
formulas.27 This yields 9000-10000 proofs,28 depending on how we run premise
selection and E. While some proofs are long, it seems that we are not yet ca-
pable of proving the more interesting conjectures and we still need more ATP
strengths. E.g., the longest ATP proof shows that -infty is non empty, where
-infty is defined as [0,REAL]. A slightly more useful conjecture which is also
hard to prove29 is the strengthening of the symmetry of the are_homeomorphic
predicate30 from non-empty to arbitrary spaces.

References
 1. Chad E. Brown and Thibault Gauthier. Self-learned formula synthesis in set theory.
    CoRR, abs/1912.01525, 2019.
 2. Karel Chvalovský, Jan Jakubuv, Martin Suda, and Josef Urban. ENIGMA-NG:
    efficient neural and gradient-boosted inference guidance for E. In CADE 27, pages
    197–215, 2019.
 3. Simon Colton. Automated Theory Formation in Pure Mathematics. Distinguished
    Dissertations. Springer London, 2012.
19
     http://grid01.ciirc.cvut.cz/~mptp/nn_conj20/results/preddatagpt1.out.tar.gz
20
     http://grid01.ciirc.cvut.cz/~mptp/nn_conj20/results/preddatagpt1.tar.gz
21
     http://grid01.ciirc.cvut.cz/~mptp/7.13.01_4.181.1147/html/groupp_1.html#T10
22
     http://grid01.ciirc.cvut.cz/~mptp/nn_conj20/results/out4.tar.gz
23
     http://grid01.ciirc.cvut.cz/~mptp/7.13.01_4.181.1147/html/sincos10.html#T17
24
     http://grid01.ciirc.cvut.cz/~mptp/nn_conj20/results/t17_sincos10___1
25
     http://grid01.ciirc.cvut.cz/~mptp/7.13.01_4.181.1147/html/functor1.html#T9
26
     http://grid01.ciirc.cvut.cz/~mptp/7.13.01_4.181.1147/html/functor1.html#T7
27
     http://grid01.ciirc.cvut.cz/~mptp/nn_conj20/results/preddata128.tar.gz
28
     http://grid01.ciirc.cvut.cz/~mptp/nn_conj20/results/preddata128.out.tar.gz
29
     http://grid01.ciirc.cvut.cz/~mptp/nn_conj20/results/t20_borsuk_3___7__1
30
     http://grid01.ciirc.cvut.cz/~mptp/7.13.01_4.181.1147/html/borsuk_3.html#R2
                        First Neural Conjecturing Datasets and Experiments          7

 4. Siemion Fajtlowicz. On conjectures of Graffiti. Annals of Discrete Mathematics,
    72(1–3):113–118, 1988.
 5. Thibault Gauthier. Deep reinforcement learning in HOL4. CoRR, abs/1910.11797,
    2019.
 6. Thibault Gauthier, Cezary Kaliszyk, and Josef Urban. Initial experiments with
    statistical conjecturing over large formal corpora. In CICM’16 WiP Proceedings,
    pages 219–228, 2016.
 7. Moa Johansson, Dan Rosén, Nicholas Smallbone, and Koen Claessen. Hipster:
    Integrating theory exploration in a proof assistant. In CICM 2014, pages 108–122,
    2014.
 8. Cezary Kaliszyk, Josef Urban, and Jirı́ Vyskocil. Automating formalization by
    statistical and semantic parsing of mathematics. In ITP, pages 12–27, 2017.
 9. Cezary Kaliszyk, Josef Urban, and Jiřı́ Vyskočil. Learning to parse on aligned
    corpora (rough diamond). In ITP 2015, pages 227–233, 2015.
10. Douglas Bruce Lenat. AM: An Artificial Intelligence Approach to Discovery in
    Mathematics as Heuristic Search. PhD thesis, Stanford, 1976.
11. Bartosz Piotrowski and Josef Urban. Stateful premise selection by recurrent neural
    networks, 2020.
12. Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, and Ilya
    Sutskever. Language models are unsupervised multitask learners. OpenAI Blog,
    1(8):9, 2019.
13. Stephan Schulz. System description: E 1.8. In Kenneth L. McMillan, Aart Middel-
    dorp, and Andrei Voronkov, editors, LPAR, volume 8312 of LNCS, pages 735–743.
    Springer, 2013.
14. Josef Urban. XML-izing Mizar: Making semantic processing and presentation of
    MML easy. In Michael Kohlhase, editor, MKM, volume 3863 of LNCS, pages
    346–360. Springer, 2005.
15. Josef Urban. MPTP 0.2: Design, implementation, and initial experiments. J.
    Autom. Reasoning, 37(1-2):21–43, 2006.
16. Qingxiang Wang, Chad E. Brown, Cezary Kaliszyk, and Josef Urban. Exploration
    of neural machine translation in autoformalization of mathematics in mizar. In
    CPP, pages 85–98, 2020.
17. Qingxiang Wang, Cezary Kaliszyk, and Josef Urban. First experiments with neural
    translation of informal to formal mathematics. In CICM, pages 255–270, 2018.

A     Additional Data From the Experiments
A.1    XXREAL 1:48 and its GPT-2 predictions

theorem Th48 : : : XXREAL 1: 4 8
f o r p , r , s , q being ext−r e a l number s t p < r & s <= q holds
[ . r , s . [ c= ] . p , q . [

Following are the Mizar premises in the order proposed by GPT-2. The fifth and
sixth were not needed for the ATP proof.

theorem Th3 : : : XXREAL 1 : 3
f o r t , r , s being ext−r e a l number holds
t in [ . r , s . [ i f f r <= t & t < s
8       Urban, Jakubův




                          Fig. 1. Dataset 2 training and loss.



l e t X be ext−r e a l −membered s e t ; l e t Y be s e t ;
pred X c= Y means : Def8 : : : MEMBERED: def 8
f o r e being ext−r e a l number s t e i n X holds e i n Y;

l e t r , s be ext−r e a l number ;
c l u s t e r [ . r , s . [ → ext−r e a l −membered ;

theorem Th2 : : : XXREAL 0 : 2
f o r a , b , c being ext−r e a l number s t a <= b & b <= c holds a <= c

l e t X be ext−r e a l −membered s e t ;
c l u s t e r → ext−r e a l f o r Element of X;

theorem : : SUBSET: 1
f o r a , b being s e t s t a i n b holds a i s Element of b ;

theorem Th4 : : : XXREAL 1 : 4
f o r t , r , s being ext−r e a l number holds
t in ] . r , s . [ i f f r < t & t < s
A.2    GROUPP_1:10 and its generalization conjectured by GPT-2

theorem Th10 : : : GROUPP 1: 1 0
f o r G being f i n i t e Group f o r N being normal Subgroup of G s t
N i s Subgroup of c e n t e r G & G . / . N i s c y c l i c holds
G i s commutative
The generalization that avoids finiteness:
f o r G being Group f o r N being normal Subgroup of G s t
N i s Subgroup of c e n t e r G & G . / . N i s c y c l i c holds
G i s commutative
                            First Neural Conjecturing Datasets and Experiments      9

We don’t have an ATP proof of the generalization yet. We thank algebraists
Michael Kinyon and David Stanovský for confirming that this generalization
is provable. Based on this example Stanovský commented that related Mizar
theorems can be similarly generalized.
A.3     SINCOS10:17 and a false conjecture by GPT-2

theorem Th17 : : : SINCOS10 : 1 7
s e c | [ . 0 , ( PI / 2 ) . [ i s i n c r e a s i n g
GPT-2 generated the following conjecture, which is false. Along with another
GPT-2 conjecture about the differentiability of sec on the interval, this results
in an ATP proof of SINCOS10:17.
f o r X being s e t f o r f being Function of REAL, REAL holds
f i s d i f f e r e n t i a b l e o n X implies f | X i s i n c r e a s i n g

A.4     FUNCTOR1:9 and a GPT-2 conjecture reducing it to FUNCTOR1:7

theorem Th9 : : : FUNCTOR1: 9
f o r C1 being non empty AltGraph
f o r C2 , C3 being non empty r e f l e x i v e AltGraph
f o r F being f e a s i b l e F u n c t o r S t r over C1 , C2
f o r G being F u n c t o r S t r over C2 , C3
s t F i s f u l l & G i s f u l l holds G ∗ F i s f u l l

f o r C1 , C2 being AltGraph f o r F being F u n c t o r S t r over C1 , C2
holds F i s f u l l i f f F i s f a i t h f u l & F i s f e a s i b l e

theorem Th7 :        : : FUNCTOR1: 7

f o r C1 being non empty AltGraph
f o r C2 , C3 being non empty r e f l e x i v e AltGraph
f o r F being f e a s i b l e F u n c t o r S t r over C1 , C2
f o r G being F u n c t o r S t r over C2 , C3
s t F i s f a i t h f u l & G i s f a i t h f u l holds G ∗ F i s f a i t h f u l
