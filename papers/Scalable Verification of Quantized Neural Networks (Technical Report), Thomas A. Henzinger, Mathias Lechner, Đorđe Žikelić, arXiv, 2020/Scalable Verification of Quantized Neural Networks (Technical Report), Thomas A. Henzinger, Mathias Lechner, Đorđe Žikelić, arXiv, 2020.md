                                                 Scalable Verification of Quantized Neural Networks (Technical Report)

                                                                        Thomas A. Henzinger, Mathias Lechner, Ðord̄e Žikelić
                                                                                                        IST Austria
                                                                                                  Klosterneuburg, Austria
                                                                                             {tah,mlechner, dzikelic}@ist.ac.at
arXiv:2012.08185v2 [cs.AI] 5 Apr 2022




                                                                    Abstract                                       The verification problem for neural networks consists of
                                                                                                                checking validity of some input-output relation. More pre-
                                          Formal verification of neural networks is an active topic of re-
                                          search, and recent advances have significantly increased the          cisely, given two conditions over inputs and outputs of the
                                          size of the networks that verification tools can handle. How-         network, the goal is to check if for every input sample
                                          ever, most methods are designed for verification of an ideal-         which satisfies the input condition, the corresponding out-
                                          ized model of the actual network which works over real arith-         put of the neural network satisfies the output condition. Ver-
                                          metic and ignores rounding imprecisions. This idealization is         ification of neural networks has many important practical
                                          in stark contrast to network quantization, which is a technique       applications such as checking robustness to adversarial at-
                                          that trades numerical precision for computational efficiency          tacks (Szegedy et al. 2013; Tjeng, Xiao, and Tedrake 2019),
                                          and is, therefore, often applied in practice. Neglecting round-       proving safety in safety-critical applications (Huang et al.
                                          ing errors of such low-bit quantized neural networks has been         2017; Lechner et al. 2021a,b) or output range analy-
                                          shown to lead to wrong conclusions about the network’s cor-
                                                                                                                sis (Dutta, Chen, and Sankaranarayanan 2019), to name
                                          rectness. Thus, the desired approach for verifying quantized
                                          neural networks would be one that takes these rounding errors         a few. There are many efficient methods for ver-
                                          into account. In this paper, we show that verifying the bit-          ification of neural networks (e.g. (Katz et al. 2017;
                                          exact implementation of quantized neural networks with bit-           Tjeng, Xiao, and Tedrake 2019; Bunel et al. 2018)), how-
                                          vector specifications is PSPACE-hard, even though verifying           ever most of them ignore rounding errors in computa-
                                          idealized real-valued networks and satisfiability of bit-vector       tions. The few approaches that can handle the seman-
                                          specifications alone are each in NP. Furthermore, we explore          tics of rounding operations are overapproximation-based
                                          several practical heuristics toward closing the complexity gap        methods, i.e., incomplete verification (Singh et al. 2018,
                                          between idealized and bit-exact verification. In particular, we       2019). The imprecision introduced by quantization stands
                                          propose three techniques for making SMT-based verification            in stark contrast with the idealization made by verifica-
                                          of quantized neural networks more scalable. Our experiments
                                                                                                                tion methods for standard neural networks, which disre-
                                          demonstrate that our proposed methods allow a speedup of
                                          up to three orders of magnitude over existing approaches.             gards rounding errors that appear due to the network’s se-
                                                                                                                mantics. Consequently, verification methods developed for
                                                                                                                standard networks are not sound for and cannot be applied
                                                                Introduction                                    to quantized neural networks. Indeed, recently it has been
                                        Deep neural networks for image classification typically con-            shown that specifications that hold for a floating-point rep-
                                        sist of a large number of sequentially composed layers.                 resentation of a network need not necessarily hold after
                                        Computing the output of such a network for a single input               quantizing the network (Giacobbe, Henzinger, and Lechner
                                        sample may require more than a billion floating-point opera-            2020). As a result, specialized verification methods that
                                        tions (Tan and Le 2019). Consequently, deploying a trained              take quantization into account need to be developed, due
                                        deep neural network imposes demanding requirements on                   to more complex semantics of quantized neural networks.
                                        the computational resources available at the computing de-              Groundwork on such methods demonstrated that special
                                        vice that runs the network. Quantization of neural networks             encodings of networks in terms of Satisfiability Mod-
                                        is a technique that reduces the computational cost of run-              ulo Theories (SMT) (Clark and Cesare 2018) with bit-
                                        ning a neural network by reducing the arithmetic precision              vector (Giacobbe, Henzinger, and Lechner 2020) or fixed-
                                        of computations inside the network (Jacob et al. 2018). As              point (Baranowski et al. 2020) theories present a promis-
                                        a result, quantization has been widely adapted in industry              ing approach towards the verification of quantized networks.
                                        for deploying neural networks in a resource-friendly way.               However, the size of networks that these tools can handle
                                        For instance, Tesla’s Autopilot Hardware 3.0 is designed                and runtimes of these approaches do not match the effi-
                                        for running 8-bit quantized neural networks (wikichip.org               ciency of advanced verification methods developed for stan-
                                        (accessed December 14, 2020)).                                          dard networks like Reluplex(Katz et al. 2017) and Neurify
                                                                                                                (Wang et al. 2018a).
                                        Copyright © 2021, Association for the Advancement of Artificial
                                        Intelligence (www.aaai.org). All rights reserved.                          In this paper, we provide first evidence that the verifica-
tion problem for quantized neural networks is harder com-          where D ⊂ Rn is the admissible input domain. For in-
pared to verification of their idealized counterparts, thus ex-    stance, we denote by Jf KR : f 7→ f the idealized real-valued
plaining the scalability-gap between existing methods for          abstraction of a network f , whereas Jf Kfloat32 denotes its
standard and quantized network verification. In particular,        floating-point implementation, i.e. the realization of f us-
we show that verifying quantized neural networks with bit-         ing 32-bit IEEE floating-point (Kahan 1996) instead of real
vector specifications is PSPACE-hard, despite the satisfia-        arithmetic. Evaluating f , even under floating-point interpre-
bility problem of formulas in the given specification logic        tation, can be costly in terms of computations and memory
being in NP. As verification of neural networks without            resources. In order to reduce these resource requirements,
quantization is known to be NP-complete (Katz et al. 2017),        networks are usually quantized before being deployed to end
this implies that the verification of quantized neural net-        devices (Jacob et al. 2018).
works is a harder problem.                                            Formally, quantization is an interpretation Jf Kint-k that
   We then address the scalability limitation of SMT-based         evaluates a network f which uses k-bit fixed-point arith-
methods for verification of quantized neural networks, and         metic (Smith et al. 1997), e.g. 4 to 8 bits. Let [Z]k = {0, 1}k
propose three techniques for their more efficient SMT en-          denote the set of all bit-vectors of bit-width k. For each layer
coding. First, we introduce a technique for identifying those      l : [Z]nk i → [Z]nk 0 in Jf Kint-k , we define its semantics by
variables and constraints whose value can be determined            defining l(x1 , . . . , xni ) = (y1 , . . . , yn0 ) as follows:
in advance, thus decreasing the size of SMT-encodings of
                                                                                    ni
networks. Second, we show how to encode variables as                                X
bit-vectors of minimal necessary bit-width. This signifi-                   x′i =         wij xj + bi ,                         (3)
cantly reduces the size of bit-vector encoding of networks                          j=1

in (Giacobbe, Henzinger, and Lechner 2020). Third, we pro-                 x′′i = round(x′i , ki ) = ⌊x′i · 2−ki ⌋,    and      (4)
pose a redundancy elimination heuristic which exploits bit-
level redundancies occurring in the semantics of the net-                   yi = max{0, min{2Ni − 1, x′′i }},                   (5)
work.                                                              Here, wi,j and bi for each 1 ≤ j ≤ ni and 1 ≤ i ≤ n0
   Finally, we propose a new method for the analysis of the        denote the learned weights and biases of f , and ki and Ni
quantized network’s reachable value range, which is based          denote the bit-shift and the cut-off value associated to each
on abstract interpretation and assists our new techniques for      variable yi , respectively. Eq. (3) multiplies the inputs xj with
SMT-encoding of quantized networks. We evaluate our ap-            the weight values wij and adds the bias bi , eq. (4) rounds the
proach on two well-studied adversarial robustness verifica-        result to the nearest valid k-bit fixed-point value, and eq. (5)
tion benchmarks. Our evaluation demonstrates that the com-         is a non-linear ReLU-N activation function 1 .
bined effect of our techniques is a speed-up of over three            An illustration of how the computations inside a network
orders of magnitude compared to the existing tools.                differ based on the used interpretation is shown in Fig. 1.
   The rest of this work is organized as follows: First, we
provide background and discuss related works on the veri-          Verification of neural networks
fication of neural networks and quantized neural networks.
We then start with our contribution by showing that the ver-       The verification problem for a neural network and its given
ification problem for quantized neural networks with bit-          interpretation consists of verifying some input-output rela-
vector specifications is PSPACE-hard. In the following sec-        tion. More formally, given a neural network f , its interpre-
tion, we propose several improvements to the existing SMT-         tation Jf K and two predicates ϕ and ψ over the input domain
encodings of quantized neural networks. Finally, we present        D and output domain Rm of Jf K, we want to check valid-
our experimental evaluation to assess the performance im-          ity of the following formula (i.e. whether it holds for each
pacts of our techniques.                                           x ∈ D)
                                                                                   ϕ(x) ∧ Jf K(x) = y =⇒ ψ(y).               (6)
          Background and Related work                              We refer to the formula in eq. (6) as the formal specifica-
A neural network is a function f : Rn → Rm that consists           tion that needs to be proved. In order to formally verify a
of several layers f = l1 ◦ l2 ◦ · · · ◦ lk that are sequentially   neural network, it is insufficient to just specify the network
composed, with each layer parameterized by learned weight          without also providing a particular interpretation. A prop-
values. Commonly found types of layers are linear                  erty that holds with respect to one interpretation need not
                                                                   necessarily remain true if we consider a different interpreta-
          l(x) = W x + b, W ∈ Rno ×ni , b ∈ Rno ,           (1)
                                                                   tion. For example, robustness of the real-valued abstraction
ReLU l(x) = max{x, 0}, and convolutional layers                    does not imply robustness of the floating-point implementa-
(LeCun et al. 1998).                                               tion of a network (Giacobbe, Henzinger, and Lechner 2020;
   In practice, the function f is implemented by floating-         Jia and Rinard 2020).
point arithmetic instead of real-valued computations. To dis-         Ideally, we would like to verify neural networks under
tinguish a neural network from its approximation, we define        the exact semantics that are used for running networks on
an interpretation Jf K as a map which assigns a new function          1
to each network, i.e.                                                   Note that for quanitzed neural networks, the double-side
                                                                   bounded ReLU-N activation is preferred over the standard ReLU
              JK : (Rn → Rm ) → (D → Rm ),                  (2)    activation function (Jacob et al. 2018)
A) Idealized real-valued network Jf KR                                a) y                          b) y

  0.94374 . . .             1.75
                                     +        2.57799431 . . .
                                                                                            x                             x
 1.382723 . . .             0.67

                                                                        y = JReLU(x)KR             y = JReLU-N(x)Kint-k
B) Floating-point network Jf Kfloat32
                                                                  Figure 2: Illustration of a) the ReLU activation function un-
      0.94374               1.75                                  der real-valued semantics, and b) ReLU-N activation under
                                              J2.577954Kfloat32
                                     +                            fixed-point semantics (right).
                                               = 2.5780
        1.3827              0.67
                                                                  Verification of quantized neural networks
C) Quantized (fixed-point) network Jf Kint-8
                                                                  The low numerical precision of few-bit fixed-point
                                                                  arithmetic implies that Jf Kint-k 6= Jf KR . Indeed,
          0.94              1.75                                  (Giacobbe, Henzinger, and Lechner 2020) constructed a
                                              J2.5696Kint-8
                                     +                            prototypical network that either satisfies or violates a formal
                                               = 2.57             specification, depending on the numerical precision used to
          1.38              0.67
                                                                  evaluate the network. Moreover, they observed such dis-
Figure 1: Illustration of how different interpretations of the    crepancy in networks found in practice. Thus, no formal
same network run with different numerical precision. A)           guarantee on Jf Kint-k can be obtained by verifying Jf KR or
Jf KR assumes infinite precision. B) Jf Kfloat32 rounds the       Jf Kfloat32 . In order to verify fixed-point implementations
mantissa according on the IEEE 754 standard. C) Jf Kint-8         of (i.e. quantized) neural networks, new approaches are re-
rounds to a fixed number of digits before and after the           quired.
comma. (Note that this figure serves as a hypothetical ex-           Fig. 2 depicts the ReLU activation function for ideal-
ample in decimal format, the actual computations run with         ized real-valued ReLU networks and for quantized ReLU
the base-2 representation.)                                       networks, respectively. The activation function under fixed-
                                                                  point semantics consists of an exponential number of piece-
the end device, i.e., Jf Kfloat32 most of the time. How-          wise constant intervals thus making the LP-based tech-
ever, as verification methods for IEEE floating-point arith-      niques, which otherwise work well for real-valued networks,
metic are extremely inefficient, research has focused on          extremely inefficient. So the approaches developed for ide-
verifying the idealized real-valued abstraction Jf KR of f .      alized real-valued ReLU networks cannot be efficiently ap-
In particular, efficient methods have been developed for a        plied to quantized networks. Existing verification meth-
popular type or networks that only consist of linear and          ods for quantized neural networks are based on bit-exact
ReLU operations (Figure 2 a) (Katz et al. 2017; Ehlers            Boolean Satisfiability (SAT) and SMT encodings. For 1-bit
2017; Tjeng, Xiao, and Tedrake 2019; Bunel et al. 2018).          networks, i.e., binarized neural networks, Narodytska et al.
The piecewise linearity of such ReLU networks allows the          (Narodytska et al.) and (Cheng et al. 2018) proposed to en-
use of Linear Programming (LP) techniques, which make             code the network semantics and the formal specification into
the verification methods more efficient. The underlying ver-      an SAT formula, which is then checked by an off-the-shelf
ification problem of ReLU networks with linear inequality         SAT solver. While their approach could handle networks of
specifications was shown to be NP-complete in the number          decent size, the use of SAT-solving is limited to binarized
of ReLU operations (Katz et al. 2017), however advanced           networks, which are not very common in practice.
tools scale beyond toy networks.
   Although these methods can handle networks of large               (Giacobbe, Henzinger, and Lechner 2020) proposed to
size, they are building on the assumption that                    verify many-bit quantized neural network by encoding their
                                                                  semantics and specifications into quantifier-free bit-vector
                    Jf Kfloat32 ≈ Jf KR ,                 (7)     SMT (QF_BV) formulas. The authors showed that, by re-
i.e. that the rounding errors introduced by the IEEE floating-    ordering linear summations inside the network, such mono-
point arithmetic of both the network and the verification al-     lithic bit-vector SMT encodings could scale to the verifica-
gorithm can be neglected. It has been recently shown that         tion of small but interestingly sized networks.
this need not always be true. For example, Jia and Ri-               (Baranowski et al. 2020) introduced an SMT theory for
nard (Jia and Rinard 2020) crafted adversarial counterexam-       fixed-point arithmetic and showed that the semantics of
ples to the floating-point implementation of a neural net-        quantized neural networks could be encoded in this theory
work whose idealized interpretation was verified to be robust     very naturally. However, as the authors only proposed pro-
against such attacks, by exploiting subtle numerical differ-      totype solvers for reference purposes, the size of the verified
ences between Jf Kfloat32 and Jf KR .                             networks was limited.
Limitations of neural network verification                        with respect to the fragment QF_BV2bw of the fixed-size
The existing techniques for verification of idealized             bit-vector logic QF_BV2 (Kovásznai, Fröhlich, and Biere
real-valued abstractions of neural networks have signif-          2016). The fragment QF_BV2 bw allows bit-wise logi-
icantly increased the size of networks that can be ver-           cal operations (such as bit-wise conjunction, disjunction
ified (Ehlers 2017; Katz et al. 2017; Bunel et al. 2018;          and negation) and the equality operator. The index 2 in
Tjeng, Xiao, and Tedrake 2019). However, scalability re-          QF_BV2bw is used to denote that the constants and bit-
mains the key challenge hindering formal verification             widths are given in binary representation. It was shown
of neural networks in practice. For instance, even                in (Kovásznai, Fröhlich, and Biere 2016) that the satisfiabil-
the largest networks verified by the existing meth-               ity problem for formulas in QF_BV2 bw is NP-complete.
ods (Ruan, Huang, and Kwiatkowska 2018) are tiny com-                Even though QF_BV2bw itself allows only bit-vector op-
pared to the network architectures used for object detection      erations and not linear integer arithmetic, we show that by
and image classification (He et al. 2016).                        introducing dummy output variables in Jf Kint-k we may still
   Regarding the verification of quantized neural networks,       encode formal specifications on outputs that are boolean
no advanced techniques aiming at performance improve-             combinations of linear inequalities over network’s outputs.
ments have been studied so far. In this paper, we address the     Thus, this specification logic is sufficiently expressive to en-
scalability of quantized neural network verification methods      code formal specifications most often seen in practice. Let
that rely on SMT-solving.                                         y1 , . . . , ym denote output variables of Jf Kint-k . In order to
                                                                  encode an inequality of the form a1 y1 + · · ·+ am ym + b ≥ 0
 Hardness of Verification of Quantized Neural                     into the output specification, we do the following:
                   Networks                                        • Introduce an additional output neuron ỹ and a directed
                                                                     edge from each output neuron yi to ỹ. Let ai be the weight
The size of quantized neural networks that existing veri-            of an edge from yi to ỹ, b be the bias term of ỹ, k − 1 be
fication methods can handle is significantly smaller com-            the bit-shift value of ỹ, and N = k be the number of bits
pared to the real arithmetic networks that can be ver-
                                                                     defining the cut-off value of ỹ. Then
ified by the state-of-the-art tools like (Katz et al. 2017;
Tjeng, Xiao, and Tedrake 2019; Bunel et al. 2018). Thus, a           ỹ = ReLU-N(round(2−(k−1) (a1 y1 + · · · + am ym + b))).
natural question is whether this gap in scalability is only be-
cause existing methods for quantized neural networks are             Thus, as we work with bit-vectors of bit-width k, ỹ is just
less efficient, or if the verification problem for quantized         the sign bit of a1 y1 + · · · + as ys + b preceded by zeros.
neural networks is computationally harder.                         • As a1 y1 + · · · + as ys + b ≥ 0 holds if and only if the
   In this section, we study the computational complexity of         sign bit of a1 y1 + · · · + as ys + b is 0, in order to en-
the verification problem for quantized neural networks. For          code the inequality into the output specification it suffices
idealized real arithmetic interpretation of neural networks, it      to encode that ỹ = 0, which is a formula expressible in
was shown in (Katz et al. 2017) that, if predicates on inputs        QF_BV2bw .
and outputs are given as conjunctions of linear inequalities,     By doing this for each linear inequality in the specification
then the problem is NP-complete. The fact that the prob-          and since the logical operations are allowed by QF_BV2bw ,
lem is NP-hard is established by reduction from 3-SAT, and        it follows that we may use QF_BV2bw to encode boolean
the same argument can be used to show that the verification       combinations of linear inequalities over outputs as formal
problem for quantized neural networks is also NP-hard. In         specifications that are to be verified.
this work, we argue that the verification problem for quan-          Our main result in this section is that, if ψ in eq. (8) is
tized neural networks with bit-vector specifications is in fact   assumed to be a formula in QF_BV2bw , then the verifi-
PSPACE-hard, and thus harder then verifying real arithmetic       cation problem for quantized neural networks is PSPACE-
neural networks. Moreover, we show that this holds even for       hard. Since checking satisfiability of ψ can be done in non-
the special case when there are no constraints on the inputs      deterministic polynomial time, this means that the additional
of the network, i.e. when the predicate on inputs is assumed      hardness really comes from the quantized neural networks.
to be a tautology. The verification problem for a quantized
neural network f that we consider consists of checking va-        Theorem 1 (Complexity of verification of QNNs). If
lidity of a given input-output relation formula                   the predicate on outputs is assumed to be a formula in
                                                                  QF_BV2bw , the verification problem for quantized neural
                 Jf Kint-k (x) = y =⇒ ψ(y).                       networks is PSPACE-hard.
Here, Jf Kint-k is the k-bit fixed point arithmetic interpreta-   Proof sketch. Here we summarize the key ideas of our
tion of f , and ψ is a predicate in some specification logic      proof. For the complete proof, see the appendix.
over the outputs of Jf Kint-k . Equivalently, we may also            To prove PSPACE-hardness, we exhibit a reduc-
check satisfiability of the dual formula                          tion from TQBF which is known to be PSPACE-
                 Jf Kint-k (x) = y ∧ ¬ψ(y).                (8)    complete (Arora and Barak 2009). TQBF is the problem of
                                                                  deciding whether a quantified boolean formula (QBF) of
  In order to study complexity of the verification prob-          the form Q1 x1 . Q2 x2 . . . . Qn xn . φ(x1 , x2 , . . . , xn ) is true,
lem, we also need to specify the specification logic to           where each Qi ∈ {∃, ∀} and φ is a quantifier-free formula
which formula ψ belongs. In this work, we study hardness          in propositional logic over the variables x1 , . . . , xn . A QBF
formula is true if it admits a truth table for each existentially         linear integer inequalities, which is the most common form
quantified variable xi , where the truth table for xi specifies a         of formal specifications seen in practice. This is because
value in {0, 1} for each valuation of those universally quan-             QF_BV2bw also allows logical operations over bit vectors,
tified variables xj on which xi depends (i.e. xj with j < i).             and not just over single bits. Nevertheless, our result presents
Thus, the size of each truth table is at most 2k , where k is             the first step towards understanding computational hardness
the total number of universally quantified variables in the               of the quantized neural network verification problem.
formula.
    In our reduction, given an instance of the TQBF problem                 Improvements to bit-vector SMT-encodings
Q1 x1 . Q2 x2 . . . . Qn xn . φ(x1 , x2 , . . . , xn ) we map it to the
corresponding verification problem as follows. The interpre-              In this section, we study efficient SMT-encodings of
tation Jf Kint-k of the neural network f consists of n + 1 dis-           quantized neural networks that would improve scal-
joint gadgets f1 , . . . , fn , g, each having a single input and a       ability of verification methods for them. In particu-
single output neuron of bit-width 2k . Note that bit-widths are           lar, we propose three simplifications to the monolithic
given in binary representation, thus this is still polynomial in          SMT encoding of eq. (3), (4), and (5) introduced in
the size of the problem. We use these gadgets to encode all               (Giacobbe, Henzinger, and Lechner 2020), which encodes
possible inputs to the QBF formula, whereas the postcondi-                quantized neural networks and formal specifications as for-
tion in the verification problem encodes the quantifier-free              mulas in the QF_BV2 logic : I) Remove dead branches of the
formula itself. For a universally quantified variable xi , the            If-Then-Else encoding of the activation function in eq. (5),
output of fi is always a constant vector encoding the values              i.e., branches that are guaranteed to never be taken; II) Allo-
of xi in each of the 2k valuations of universally quantified              cate only the minimal number of bits for each bit-vector vari-
variables (for a fixed ordering of the valuations). For existen-          able in the formula; and III) Eliminate sub-expressions from
tially quantified xi , we use fi and its input neuron to encode           the summation in eq. (3). To obtain the information needed
2k possible choices for the value of xi , one for each valua-             by the techniques I and II we further propose an abstract in-
tion of universally quantified variables, and thus to encode              terpretation framework for quantized neural networks.
the truth table for xi . Finally, the gadget g is used to return a
constant bit-vector 1 of bit-width 2k on any possible input.              Abstract interpretation analysis
The predicate ψ on the outputs is then defined as                         Abstract interpretation (Cousot and Cousot 1977) is a tech-
                  ψ := (φbw (y1 , . . . , yn ) = 1),                      nique for constructing over-approximations to the behavior
                                                                          of a system. Initially developed for software verification, the
where φbw is the quantifier-free formula in QF_BV2 bw
                                                                          method has recently been adapted to robustness verification
identical to φ, with only difference being that the inputs
                                                                          of neural networks and is used to over-approximate the out-
of φbw are bit-vectors of bit-width 2k instead of boolean
                                                                          put range of variables in the network. Instead of consider-
variables, and logical operations are also defined over bit-
                                                                          ing all possible subsets of real numbers, it only considers an
vectors (again, since bit-widths are encoded in binary rep-
                                                                          abstract domain which consists of subsets of suitable form
resentation, this is of polynomial size). The output of φbw
                                                                          (e.g. intervals, boxes or polyhedra). This allows modeling
is thus tested if it equals 1 for each valuation of universally
                                                                          each operation in the network in terms of operations over the
quantified variables and the corresponding values of exis-
                                                                          elements of the abstract domain, thus over-approximating
tentially quantified variables defined by the truth tables. Our
                                                                          the semantics of the network. While it leads to some im-
construction ensures that any satisfying input for the neural
                                                                          preision, abstract interpretation allows more efficient output
networks induces satisfying truth tables for the TQBF in-
                                                                          range analysis for variables. Due to its over-approximating
stance and vice-versa, which completes the reduction.
                                                                          nature, it remains sound for verifying neural networks.
   Theorem 1 is to our best knowledge the first theoretical                  Interval (Wang et al. 2018b; Tjeng, Xiao, and Tedrake
result which indicates that the verification problem for quan-            2019), zonotope (Mirman, Gehr, and Vechev 2018;
tized neural networks is harder than verifying their idealized            Singh et al. 2018), and convex polytope (Katz et al.
real arithmetic counterparts. It sheds some light on the scal-            2017; Ehlers 2017; Bunel et al. 2018; Wang et al. 2018a)
ability gap of existing SMT-based methods for their veri-                 abstractions have emerged in literature as efficient and yet
fication, and shows that this gap is not solely due to prac-              precise choices for the abstract domains of real-valued
tical inefficiency of existing methods for quantized neural               neural networks. The obtained abstract domains have been
networks, but also due to the fact that the problem is com-               used for output range analysis (Wang et al. 2018b), as well
putationally harder. While Theorem 1 gives a lower bound                  as removing decision points from the search process of
on the hardness of verifying quantized neural networks, it is             complete verification algorithms (Tjeng, Xiao, and Tedrake
easy to see that an upper bound on the complexity of this                 2019; Katz et al. 2017). One important difference between
problem is NEXP since the inputs to the verification prob-                standard and quantized networks is the use of double-sided
lem are of size that is exponential in the size of the problem.           bounded activation functions in quantized neural networks,
Closing the gap and identifying tight complexity bounds is                i.e., ReLU-N instead of ReLU (Jacob et al. 2018). This
an interesting direction of future work.                                  additional non-linear transition, on one hand, renders
   Note though that the specification logic QF_BV2bw used                 linear abstractions less effective, while on the other hand it
to encode predicates over outputs is strictly more expres-                provides hard upper bounds to each neuron, which bounds
sive than what we need to express boolean combinations of                 the over-approximation error. Consequently, we adopt
interval abstractions (IA) on the quantized interpretation         Redundant multiplication elimination
of a network to obtain reachability sets for each neuron           Another difference between quantized and standard neural
in the network. As discussed in (Tjeng, Xiao, and Tedrake          networks is the rounding of the weight values to the near-
2019), using a tighter abstract interpretation poses a tradeoff    est representable value of the employed fixed-point format.
between verification and pre-processing complexity.                Consequently, there is a considerable chance that two con-
                                                                   nections outgoing from the same source neuron will have
Dead branch removal                                                the same weight value. For instance, assuming an 8-bit net-
Suppose that through our abstract interpretation we obtained       work and a uniform weight distribution, the chance of two
an interval [lb, ub] for the input x of a ReLU-N operation         connections having the same weight value is around 0.4%
y = ReLU-N(x). Then, we can substitute the formulation             compared to the much lower 4 · 10−8% of the same scenario
of the ReLU-N by                                                   happening in a floating-point network.
                                                                      Moreover, many weight values express some subtle form
                                  if ub ≤ 0
 
 
  0,                                                              of redundancy on a bit-level. For instance, both multiplica-
   2 N
       − 1,                       if lb ≥ 2N − 1
 
                                                                   tion by 2 and multiplication by 6 contain a shift operations
 
 
 
                                  if ub ≥ 0 and lb ≤ 2N − 1        by 1 digit in their binary representation. Thus, computations
 
   x,
 
 max{0, x},                      if 0 < ub ≤ 2N − 1.
                                                                               y1 = 3 · x1             y2 = 6 · x1          (11)
         N
                                  if 0 ≤ lb < 2N − 1.
 
 
  min{2 − 1, x},
                                                                   can be rewritten as
 
   max{0, min{2 − 1, x}}, otherwise,
 
                  N


which reduces the number of decision points in the SMT                        y1 = 3 · x1             y2 = y1 << 1,          (12)
formula.                                                           where << is a binary shift to the left by 1 digit. As a result,
                                                                   a multiplication by 6 is replaced by a much simpler shift op-
Minimum bit allocation                                             eration. Based on this motivation, we propose a redundancy
A k-bit quantized neural network represents each neuron            elimination heuristic to remove redundant and partially re-
and weight variable by a k-bit integer. However, when com-         dundant multiplications from the SMT formula. Our heuris-
puting the values of certain types of layers, such as the lin-     tic first orders all outgoing weights of a neuron in ascending
ear layer in eq. (1), a wider register is necessary. The binary    order and then sequentially applies a rule-matching for each
multiplication of a k-bit weight and a k-bit neuron value re-      weight value. The rules try to find a simpler way to com-
sults in a number that is represented by 2k-bits. Furthermore,     pute the multiplication of the weight and the neuron value
summing up n such 2k-bit integer requires                          by using already performed multiplications. The algorithm
                                                                   and the rules in full are provided in the appendix.
                  bnaive = 2k + log2 (n) + 1                (9)
                                                                      Note that a similar idea was introduced by (Cheng et al.
bits to be safely represented without resulting in an overflow.    2018) in the form of a neuron factoring algorithm for the en-
   Thus, linear combinations are in practice usually com-          coding of binarized (1-bit) neural networks into SAT formu-
puted on 32-bit integer registers. Application of fixed-point      las. However, the heuristic of (Cheng et al. 2018) removes
rounding and the activation function then reduces the neuron       redundant additions, whereas we consider bit-level redun-
values back to a k-bit representation (Jacob et al. 2018).         dancies in multiplications. For many-bit quantization, the
   QF_BV2        reasons    over    fixed-size      bit-vectors,   probability of two neurons sharing more than one incom-
i.e. the bit width of each variable must be fixed                  ing weight is negligible, thus making such neuron factoring
in the formula regardless of the variable’s value.                 proposed in (Cheng et al. 2018) less effective.
(Giacobbe, Henzinger, and Lechner 2020) showed that
the number of bits used for all weight and neuron variables                      Experimental Evaluation
in the formal affects the runtime of the SMT-solver signif-        We create an experimental setup to evaluate how much the
icantly. For example, omitting the least significant bit of        proposed techniques affect the runtime and efficiency of
each variable cuts the runtime on average by half. However,        the SMT-solver. Our reference baseline is the approach of
the SMT encoding of (Giacobbe, Henzinger, and Lechner              (Giacobbe, Henzinger, and Lechner 2020), which consists
2020) allocates bnaive bits according to eq. (9) for each          of a monolithic and "balanced" bit-vector formulation for the
accumulation variable of a linear layer.                           Boolector SMT-solver. We implement our techniques on top
   Our approach uses the interval [lb, ub] obtained for each       of this baseline. We limited our evaluation to Boolector, as
variable by abstract interpretation to compute the minimal         other SMT-solvers supporting bit-vector theories, such as Z3
number of bits necessary to express any value in the inter-        (De Moura and Bjørner 2008), CVC4 (Barrett et al. 2011),
val. As the signed bit-vector variables are represented in the     and Yices (Dutertre 2014), performed much worse in the
two’s complement format, we can compute the bit width b            evaluation of (Giacobbe, Henzinger, and Lechner 2020).
of variable x with computed interval [lb, ub] by                      Our evaluation comprises of two benchmarks. Our first
         bminimal = 1 + log2 (max{|lb|, |ub|} + 1).        (10)    evaluation considers the adversarial robustness verifica-
                                                                   tion of image classifier trained on the MNIST dataset
Trivially, one can show that bminimal < bnaive , as |ub|≤ 22k n    (LeCun et al. 1998). In particular, we check the l∞ robust-
and |lb|≤ 22k n.                                                   ness of networks against adversarial attacks (Szegedy et al.
  Attack       Baseline         Baseline           Ours               Attack      Baseline         Baseline          Ours
  radius     (+ Lingeling)    (+ CaDiCal)                             radius    (+ Lingeling)    (+ CaDiCal)
  ε=1         63 (63.6%)       92 (92.9%)      99 (100.0%)            ε=1         2 (2.3%)        44 (50.6%)      76 (87.4%)
  ε=2          0 (0.0%)        20 (20.2%)       94 (94.9%)            ε=2         0 (0.0%)         7 (7.8%)       73 (81.1%)
  ε=3          0 (0.0%)         2 (2.1%)        71 (74.0%)            ε=3         0 (0.0%)         1 (2.3%)       27 (62.8%)
  ε=4          0 (0.0%)         1 (1.0%)        54 (55.7%)            ε=4         0 (0.0%)         0 (0.0%)       18 (40.9%)

Table 1: Number of solved instances of adversarial robust-         Table 3: Number of solved instances of adversarial robust-
ness verification on the MNIST dataset. Absolute numbers           ness verification on the Fashion-MNIST dataset. Absolute
and in percentages of checked instances in parenthesis.            numbers and in percentages of checked instances in paren-
                                                                   thesis. Best method in bold.
      Dataset           Baseline          Baseline        Ours
                      (+ Lingeling)     (+ CaDiCal)                 Method                            Total solved   Cumulative
     MNIST             8803 |8789        2798 |3931       5 |90                                          instances     runtime
 Fashion-MNIST         6927 |6927        3105 |3474       4 |49     No redundancy eliminiation       316 (80.8%)          7.7 h
                                                                    No minimum bitwidth              315 (80.6%)          5.1 h
Table 2: Median |mean runtime of adversarial robustness             No ReLU simplify                   88 (22.5%)        83.2 h
verification process per sample. The reported values only ac-       No Abstract interpretation       107 (27.4%)        126.0 h
count for non-timed-out samples.                                    All enabled                      318 (81.3%)          7.9 h

2013). Other norms, such as l1 and l2 , can be expressed           Table 4: Results of our ablation analysis on the MNIST
in bit-vector SMT constraints as well, although with poten-        dataset. The cumulative runtime only accounts for non-
tially negative effects on the solver runtime. In the second       timed-out samples.
evaluation, we repeat the experiment on the slightly more
complex Fashion-MNIST dataset (Xiao, Rasul, and Vollgraf           gains. Due to time and computational limitations we focus
2017) .                                                            our ablation experiments to MNIST exclusively.
   All experiments are run on a 14-core Intel W-2175                  The results in Table 4 show the highest number of solved
CPU with 64GB of memory. We used the boolector                     instances were achieved when all our techniques were en-
(Niemetz, Preiner, and Biere 2015) with the SAT-solvers            abled. Nonetheless, Table 4 demonstrate these gains are not
Lingeling(Biere 2017) (only baseline) and CaDiCal (Biere           equally distributed across the three techniques. In particular,
2019) (baseline + our improvements) as SAT-backend.                the ReLU simplification has a much higher contribution for
   Adversarial robustness specification can be expressed as        explaining the gains compared to the redundancy elimina-
                                                                   tion and minimum bitwidth methods. The limited benefits
    |x − xi |∞ ≤ ε ∧ y = Jf Kint-k (x) =⇒ y = yi ,          (13)   observed for these two techniques may be explain by the in-
                                                                   ner workings of the Boolector SMT-solver.
where (xi , yi ) is a human labeled test sample and ε is a fixed      The Boolector SMT-solver (Niemetz, Preiner, and Biere
attack radius. As shown in eq. (13), the space of possible at-     2015) is based on a portfolio approach which se-
tacks increases with ε. Consequently, we evaluate with dif-        quentially applies several different heuristics to
ferent attack radii ε and study the runtimes individually. In      find a satisfying assignment of the input formula
particular, for MNIST we check the first 100 test samples          (Wintersteiger, Hamadi, and De Moura 2009). In par-
with an attack radius of ε = 1, the next 100 test samples          ticular, Boolector starts with fast but incomplete local
with ε = 2, and the next 200 test samples with ε = 3 and           search heuristics and falls back to slower but complete
ε = 4 respectively. For our Fashion-MNIST evaluation, we           bit-blasting (Clark and Cesare 2018) in case the incom-
reduce the number of samples to 50 per attack radius value         plete search is unsuccessful (Niemetz, Preiner, and Biere
for ε > 2 due to time and compute limitations.                     2019). Although our redundancy elimination and minimum
   The network studied in our benchmark consists of four           bitwidth techniques simplify the bit-blasted representation
fully-connected layers (784,64,32,10), resulting in 52,650         of the encoding, it introduces additional dependencies
parameters in total. It was trained using a quantization-aware     between different bit-vector variables. As a result, we
training scheme with a 6-bit quantization.                         believe these extra dependencies make the local search
   The results for the MNIST evaluation in terms of solved         heuristics of Boolector less effective and thus enabling only
instances and median solver runtime are shown in Table 1           limited performance improvements.
and Table 2 respectively. Table 3 and Table 2 show the re-
sults for the Fashion-MNIST benchmark.                                                    Conclusion
                                                                   We show that the problem of verifying quantized neural net-
Ablation analysis                                                  works with bit-vector specifications on the inputs and out-
We perform an ablation analysis where we re-run our ro-            puts of the network is PSPACE-hard. We tackle this chal-
bustness evaluation with one of our proposed techniques dis-       lenging problem by proposing three techniques to make the
abled. The objective of our ablation analysis is to understand     SMT-based verification of quantized networks more effi-
how the individual techniques affect the observed efficiency       cient. Our experiments show that our method outperforms
existing tools by several orders of magnitude on adversar-       SIGPLAN symposium on Principles of programming lan-
ial robustness verification instances. Future work is neces-     guages (POPL).
sary to explore quantized neural network verification’s com-
                                                                 De Moura, L.; and Bjørner, N. 2008. Z3: An efficient
plexity with respect to different specification logics. On the
                                                                 SMT solver. In International conference on Tools and Algo-
practical side, our methods point to limitations of mono-
                                                                 rithms for the Construction and Analysis of Systems, 337–
lithic SMT-encodings for quantized neural network verifica-
                                                                 340. Springer.
tion and suggest that future improvements may be obtained
by integrating the encoding and the solver steps more tightly.   Dutertre, B. 2014. Yices 2.2. In International Conference
                                                                 on Computer Aided Verification, 737–744. Springer.
                   Acknowledgments                               Dutta, S.; Chen, X.; and Sankaranarayanan, S. 2019. Reach-
This research was supported in part by the Austrian Sci-         ability analysis for neural feedback systems using regressive
ence Fund (FWF) under grant Z211-N23 (Wittgenstein               polynomial rule inference. In International Conference on
Award), ERC CoG 863818 (FoRM-SMArt), and the Euro-               Hybrid Systems: Computation and Control (HSCC).
pean Union’s Horizon 2020 research and innovation pro-
                                                                 Ehlers, R. 2017. Formal verification of piece-wise lin-
gramme under the Marie Skłodowska-Curie Grant Agree-
                                                                 ear feed-forward neural networks. In International Sympo-
ment No. 665385.
                                                                 sium on Automated Technology for Verification and Analysis
                                                                 (ATVA).
                       References
Arora, S.; and Barak, B. 2009. Computational Com-            Giacobbe, M.; Henzinger, T. A.; and Lechner, M. 2020. How
plexity - A Modern Approach.              Cambridge Uni-     Many Bits Does it Take to Quantize Your Neural Network?
versity Press.       ISBN 978-0-521-42426-4.           URL   In International Conference on Tools and Algorithms for the
                                                             Construction and Analysis of Systems (TACAS).
http://www.cambridge.org/catalogue/catalogue.asp?isbn=9780521424264.
Baranowski, M.; He, S.; Lechner, M.; Nguyen, T. S.; and      He, K.; Zhang, X.; Ren, S.; and Sun, J. 2016. Deep resid-
Rakamaric, Z. 2020. An SMT Theory of Fixed-Point Arith-      ual learning for image recognition. In IEEE Conference on
metic .                                                      Computer Vision and Pattern Recognition (CVPR).
Barrett, C.; Conway, C. L.; Deters, M.; Hadarean, L.; Jo-    Huang, X.; Kwiatkowska, M.; Wang, S.; and Wu, M. 2017.
vanović, D.; King, T.; Reynolds, A.; and Tinelli, C. 2011.  Safety verification of deep neural networks. In International
CVC4. In International Conference on Computer Aided Ver-     Conference on Computer Aided Verification, 3–29. Springer.
ification, 171–177. Springer.                                Jacob, B.; Kligys, S.; Chen, B.; Zhu, M.; Tang, M.; Howard,
Biere, A. 2017. CaDiCaL, Lingeling, Plingeling, Treen-       A.; Adam, H.; and Kalenichenko, D. 2018. Quantization and
geling, YalSAT Entering the SAT Competition 2017. In         training of neural networks for efficient integer-arithmetic-
Balyo, T.; Heule, M.; and Järvisalo, M., eds., Proc. of SAT  only inference. In IEEE Conference on Computer Vision
Competition 2017 – Solver and Benchmark Descriptions,        and Pattern Recognition (CVPR).
volume B-2017-1 of Department of Computer Science Se-        Jia, K.; and Rinard, M. 2020. Exploiting Verified Neural
ries of Publications B, 14–15. University of Helsinki.       Networks via Floating Point Numerical Error. arXiv preprint
Biere, A. 2019. CaDiCaL at the SAT Race 2019. In Heule,          arXiv:2003.03021 .
M.; Järvisalo, M.; and Suda, M., eds., Proc. of SAT Race
                                                                 Kahan, W. 1996. IEEE standard 754 for binary floating-
2019 – Solver and Benchmark Descriptions, volume B-
                                                                 point arithmetic. Lecture Notes on the Status of IEEE
2019-1 of Department of Computer Science Series of Publi-
                                                                 754(94720-1776): 11.
cations B, 8–9. University of Helsinki.
Bunel, R. R.; Turkaslan, I.; Torr, P.; Kohli, P.; and            Katz, G.; Barrett, C.; Dill, D. L.; Julian, K.; and Kochender-
Mudigonda, P. K. 2018. A unified view of piecewise lin-          fer, M. J. 2017. Reluplex: An efficient SMT solver for veri-
ear neural network verification. In Conference on Neural         fying deep neural networks. In International Conference on
Information Processing Systems (NeurIPS).                        Computer Aided Verification (CAV).
Cheng, C.-H.; Nührenberg, G.; Huang, C.-H.; and Ruess, H.        Kovásznai, G.; Fröhlich, A.; and Biere, A. 2016. Complexity
2018. Verification of Binarized Neural Networks via Inter-       of fixed-size bit-vector logics. Theory of Computing Systems
Neuron Factoring. In Working Conference on Verified Soft-        59(2): 323–376.
ware: Theories, Tools, and Experiments (VSTTE).                  Lechner, M.; Žikelić, Ð.; Chatterjee, K.; and Henzinger,
Clark, B.; and Cesare, T. 2018. Satisfiability Modulo The-       T. A. 2021a. Infinite Time Horizon Safety of Bayesian Neu-
ories. In Clarke, E. M.; Henzinger, T. A.; Veith, H.; and        ral Networks. In Conference on Neural Information Pro-
Bloem, R., eds., Handbook of model checking, volume 10,          cessing Systems (NeurIPS).
chapter 11. Springer.                                            Lechner, M.; Žikelić, Ð.; Chatterjee, K.; and Henzinger,
Cousot, P.; and Cousot, R. 1977. Abstract interpretation: a      T. A. 2021b. Stability Verification in Stochastic Control Sys-
unified lattice model for static analysis of programs by con-    tems via Neural Network Supermartingales. arXiv preprint
struction or approximation of fixpoints. In ACM SIGACT-          arXiv:2112.09495 .
LeCun, Y.; Bottou, L.; Bengio, Y.; and Haffner, P. 1998.
Gradient-based learning applied to document recognition.
Proceedings of the IEEE 86(11): 2278–2324.
Mirman, M.; Gehr, T.; and Vechev, M. 2018. Differentiable
abstract interpretation for provably robust neural networks .
Narodytska, N.; Kasiviswanathan, S.; Ryzhyk, L.; Sagiv, M.;
and Walsh, T. ???? Verifying properties of binarized deep
neural networks. In AAAI Conference on Artificial Intelli-
gence (AAAI).
Niemetz, A.; Preiner, M.; and Biere, A. 2015. Boolector
2.0 system description. Journal on Satisfiability, Boolean
Modeling and Computation 9: 53–58.
Niemetz, A.; Preiner, M.; and Biere, A. 2019. Boolector
at the SMT Competition 2019. Technical report, Stanford
University and JKU Linz.
Ruan, W.; Huang, X.; and Kwiatkowska, M. 2018. Reacha-
bility analysis of deep neural networks with provable guar-
antees. In International Joint Conference on Artificial Intel-
ligence (IJCAI).
Singh, G.; Gehr, T.; Mirman, M.; Püschel, M.; and Vechev,
M. 2018. Fast and effective robustness certification .
Singh, G.; Gehr, T.; Püschel, M.; and Vechev, M. 2019. An
abstract domain for certifying neural networks. Proceedings
of the ACM on Programming Languages 3(POPL): 1–30.
Smith, S. W.; et al. 1997. The scientist and engineer’s guide
to digital signal processing .
Szegedy, C.; Zaremba, W.; Sutskever, I.; Bruna, J.; Erhan,
D.; Goodfellow, I.; and Fergus, R. 2013. Intriguing prop-
erties of neural networks. arXiv preprint arXiv:1312.6199
.
Tan, M.; and Le, Q. V. 2019. Efficientnet: Rethinking model
scaling for convolutional neural networks .
Tjeng, V.; Xiao, K. Y.; and Tedrake, R. 2019. Evaluating
robustness of neural networks with mixed integer program-
ming. In International Conference on Learning Representa-
tions (ICLR).
Wang, S.; Pei, K.; Whitehouse, J.; Yang, J.; and Jana, S.
2018a. Efficient formal safety analysis of neural networks
.
Wang, S.; Pei, K.; Whitehouse, J.; Yang, J.; and Jana, S.
2018b. Formal security analysis of neural networks using
symbolic intervals. In 27th {USENIX} Security Symposium
({USENIX} Security 18), 1599–1614.
wikichip.org.         (accessed        December        14,
2020).           FSD Chip - Tesla.                   URL
https://en.wikichip.org/wiki/tesla_(car_company)/fsd_chip.
Wintersteiger, C. M.; Hamadi, Y.; and De Moura, L. 2009.
A concurrent portfolio approach to SMT solving. In Inter-
national Conference on Computer Aided Verification, 715–
720. Springer.
Xiao, H.; Rasul, K.; and Vollgraf, R. 2017. Fashion-MNIST:
a Novel Image Dataset for Benchmarking Machine Learning
Algorithms.
                            Appendix                                       Ordering of variable valuations. Let U denote the ordered
                                                                           set of all universally quantified variables in the QBF for-
         Redundancy elimination algorithm                                  mula, where variables are ordered according to their indices.
The algorithm aiming to remove bit-level redundancies is                   A valuation of U is an assignment in {0, 1}k of each vari-
shown in Algorithm 1. The rules for matching a weight value                able in U . As a truth table for each existentially quantified
to the set of existing computations V of a layer is Table 5.               variable xi is defined with respect to all variable valuations
                                                                           of universally quantified variables on which xi depends, it
                                                                           will be convenient to fix an ordering ⊑ of all 2k valua-
 Algorithm 1: Multiplication redundancy elimina-                           tions of U . For two valuations (y1 , . . . , yk ) and (y1′ , . . . , yk′ )
 tion                                                                      in {0, 1}k , we say that (y1 , . . . , yk ) ⊑ (y1′ , . . . , yk′ ) if ei-
   Input: Outgoing weights W = {wi |i = 1, . . . n} of                     ther they are equal or there exists an index 1 ≤ i ≤ k
           neuron x, with n neurons in the next layers                     such that yi < yi′ and yj = yj′ for j > i. Equivalently,
   Output: Outgoing values wi · x of neuron x                              (y1 , . . . , yk ) ⊑ (y1′ , . . . , yk′ ) if and only if
   Sort W in ascending order by absolute value;
   V ← {}, Y ← {};                                                                               k                   k
   foreach wi ∈ W do
                                                                                                 X                   X
                                                                                                        yi · 2 i ≤         yi′ · 2i
       Find rule for wi according to Table 1 given V ;                                            i=1                i=1
       if rule found then
            Y ← Y ∪ {rule(wi , V )};                                       Thus this is the lexicographic ordering on "reflected" valu-
       else                                                                ations, i.e. the largest index having the highest priority. For
            y ← wi · x;                                                    brevity, we will still refer to it as the lexicographic ordering.
            V ← V ∪ {wi }, Y ← Y ∪ {y};                                    For an existentially quantified variable xi , its truth table can
                                                                           therefore also be defined by specifying a value in {0, 1} for
       end
                                                                           each of the first 2u(i) valuations of U in the lexicographic
   end
                                                                           ordering, since these are the orderings in which we consider
   return Y ;
                                                                           all possible valuations of the first u(i) universally quantified
                                                                           variables in U with setting the remaining universally quan-
                                                                           tified variables to equal 0.
                    Proof of Theorem 1                                      Reduction. We now proceed to the construction of our reduc-
In order to prove that the verification problem for quan-                   tion. Given Φ = Q1 x1 . Q2 x2 . . . . Qn xn . φ(x1 , x2 , . . . , xn )
tized neural networks is PSPACE-hard, we exhibit a re-                      a QBF formula, we need to construct
duction from TQBF which is known to be PSPACE-                             1. a quantized neural network f Φ , and
complete (Arora and Barak 2009) to the QNN verification
problem. TQBF is the problem of deciding whether a                         2. a predicate ψ Φ over the outputs of the neural network,
quantified boolean formula (QBF) in propositional logic of                  each of polynomial size in the size of Φ, such that Φ is true
the form Q1 x1 . Q2 x2 . . . . Qn xn . φ(x1 , x2 , . . . , xn ) is true,    if and only if the neural networks admits inputs that satisfy
where each Qi ∈ {∃, ∀} and φ is a quantifier-free formula                   the verification problem.
in propositional logic over the variables x1 , . . . , xn .
                                                                           1. Construction of the quantized neural network. We con-
TQBF. Given Φ = Q1 x1 . Q2 x2 . . . . Qn xn . φ(x1 , x2 , . . . , xn )         struct f Φ to consist of n+1 gadgets f1Φ , . . . , fnΦ , g Φ . Each
a QBF formula, for each variable xi let u(i) be the number                     gadget can be viewed as a sub-neural network, and all
of universally quantified variables xj with j < i. Then, Φ is                  nodes in gadgets are of the bit-width 2k each. Since bit-
true if it admits a truth table for each existentially quantified              widths in quantized neural networks are given in binary
variable xi , where the truth table for xi specifies a value                   representation, specifying bit-width is still of polynomial
in {0, 1} for each valuation of u(i) universally quantified                    size. Each gadget fiΦ is associated to the variable xi in the
variables that xi depends on. Hence, the size of the truth                     QBF formula. The purpose of each gadget is to produce
table for xi is 2u(i) . In particular, if k is the total number of             the output of the following form:
universally quantified variables, then to show that Φ is true                   • If xi is universally quantified in Φ, then fiΦ will return
it suffices to find n − k truth tables with each of size at most                  the single output neuron whose value is the constant
2k .                                                                                                        k
                                                                                  bit-vector ci ∈ {0, 1}2 whenever the predicate ψ Φ is
                                                                                  satisfied. For each 1 ≤ j ≤ 2k , the component ci [j]
             Condition                  Action                                    will be equal to 1 if and only if the value of xi in the
             wi = 0                     yi = 0                                    j-th valuation of U (w.r.t. the lexicographic ordering)
             wi = 1                     yi = x                                    is equal to 1. Thus, ci will encode values of xi in each
             ∃wj : wi = wj              yi = yj                                   valuation of U when ordered lexicographically.
             ∃wj : wi = −wj             yi = −yj                                • If xi is existentially quantified in Φ, then fiΦ will return
             ∃wj : wi = wj · 2k         yi = yj << k                              a single output neuron which will encode a truth table
                                                                                  for xi . Recall, xi depends only on the first u(i) univer-
Table 5: Rules used for the multiplication redundancy elim-                       sally quantified variables in Φ, thus its truth table is of
ination heuristic
  size 2u(i) . As the values of xi should remain invariant          gadget fiΦ will thus consist of two sequentially com-
  if the values remaining universally quantified variables          posed parts. The first part fi,1 Φ
                                                                                                         takes any bit-vector of
  are changed, we will encode the truth table for xi by             bit-width 2 as an input, and outputs a bit-vector of the
                                                                                 k
  first extracting the first 2u(i) bits from the input neuron       same bit-width which starts with the block Bi followed
  to encode the truth table itself, and then copying this           by zeros. The second part fi,2   Φ
                                                                                                         takes the output of the
  block of bits 2k−u(i) times in order to obtain an output          first part as an input, and outputs ci .
  bit-vector of bit-width 2k .                                        Φ
                                                                    fi,1 consists of 3 layers: the input layer L0 with the sin-
• The gadget g Φ will return the constant bit-vector 1 con-         gle input neuron, layer L1 with two neurons, and output
  sisting of all 1’s (thus written in bold) whenever the            layer L2 with a single output neuron. The input neuron
  predicate ψ Φ is satisfied. Note, the constant bit-vector         in L0 is set to coincide with the output neuron of g Φ and
  whose each bit is 1 is exponential in k and thus expo-            thus equals 1. The cut-off value of each neuron in fi,1       Φ
  nential in the size of the TQBF problem. Hence, as we             is N = 2k . The weights of edges from the input neu-
  will later need to encode 1 into the predicate ψ Φ over           ron in L0 to neurons in L1 are set to w01     ′
                                                                                                                     = w01 ′′
                                                                                                                                = 1,
  outputs of the quantized neural network, we cannot do
                                                                    the biases b′1 = b′′1 = 0 and the bit-shifts F01  ′
                                                                                                                           = 2u(i)
  it directly but use the quantized neural network to con-
  struct 1.                                                         and F01 ′′
                                                                               = 22u(i) . Hence, the output values of two neu-
                                                                    rons in L1 will be the bit-vectors of bit-width 2k that
We now describe the architecture of the gadgets that can            start with 2u(i) (resp. 22u(i) ) zeros, followed by ones.
perform the tasks described above:                                  Finally, the weights of edges from neurons in L1 to the
• The gadget g Φ consists only of the input and the out-            output neuron in L2 are set to w12    ′
                                                                                                            = 1 and w12 ′′
                                                                                                                              = −1,
  put layer. The input layer consists of the single neuron          the bias b2 = 0 and the bit-shifts F12      ′
                                                                                                                    = F12 ′′
                                                                                                                                = 0.
  xg , and three output neurons yg , yg′ and yg′′ . Each edge       The output value of the neuron in L2 will thus be a bit-
  between the layers has weight 1, bias 0 and the cut-off           vector of bit-width 2k which starts with the block of
  value 2k . The bit-shifts of the edges from xg to yg , yg′        bits Bi and followed by zeros, as desired.
                                                                      Φ
  and yg′′ are 0, 2k − 1 and 1, respectively. The gadget g Φ        fi,2  consists of 2(k − u(i) − 1) + 1 layers, where the
  is accompanied by the predicate ψgΦ which is satisfied            input layer coincides with the output layer of fi,1  Φ
                                                                                                                              . Then
  if and only if xg = yg = 1. Formally, we define ψgΦ via           for each 1 ≤ j ≤ k−u(i)−1, the 2j-th layer consists of
                                                                    two neurons and the (2j+1)-st layer consists of a single
             ψgΦ := ((yg′ = 1) ∧ (¬(yg′′ ) ∨ yg )).                 neuron. The cut-off value of each neuron is N = 2k .
                                                                    The weights of each edge in fi,2     Φ
                                                                                                            is 1 and the bias of
  To prove this, suppose first that ψgΦ is true so we need          each neuron is 0, thus we only need to specify the bit-
  to show that xg = yg = 1. Clearly, by our definition              shifts. For two edges from the neuron in the (2j − 1)-st
  of the gadget we have xg = yg . Furthermore, yg′ = 1              layer to neurons in the (2j)-th layer we set bit-shifts to
  implies that the first bit of xg = yg is equal to 1. Finally,     be F2j−1,2j
                                                                          ′
                                                                                   = 0 and F2j−1,2j
                                                                                              ′′
                                                                                                       = u(i) + j, respectively.
  observe that                                                      For two edges from neurons in the 2j-th layer to the
                                                                    neuron in the (2j +1)-st layer both bit-shits are set to 0.
        (¬(yg′′ ) ∨ yg ) ≡ (yg′′ → yg )                             Given that the input fi,2Φ
                                                                                                 is a bit-vector of bit-width 2k
                             k
                            2^ −1                                   which starts with the block Bi of length 22u(i) followed
         ≡ (0 → yg [1]) ∧          (yg [j] → yg [j + 1]),           by zeros, by simple induction one can show that the
                             j=1                                    output of the neuron in the (2j + 1)-st layer is a bit-
                                                                    vector of bit-width 2k which starts with 2j copies of Bi
  where the last inequality follows from the fact that yg′′         which are followed by zeros. Hence, the value of the
  is obtained by shifting yg by 1 bit. Here we use yg [j] to        output neuron of fi,2 Φ
                                                                                            will be ci , as desired.
  denote the j-th bit in yg for each 1 ≤ j ≤ 2k , with yg [1]
  denoting the most significant bit in yg . Then, since we        • For fiΦ corresponding to existentially quantified vari-
  already showed that the first bit of xg = yg is equal to          able xi , the neural network fiΦ will also consist of two
  1, a simple induction on j shows that all bits of xg = yg         sequentially composed parts. The first part fi,1 Φ
                                                                                                                        takes
  are equal to 1, i.e. xg = yg = 1.                                 any bit-vector of bit-width 2 as an input, and outputs a
                                                                                                 k

  Conversely, suppose that xg = yg = 1 so we need to                bit-vector of the same bit-width which starts with the
  show that ψgΦ is true. The formula ¬(yg′′ )∨yg is trivially       same 2u(i) bits as the input bit-vector but which are
  true as yg = 1 and yg′ = 1 follows since yg′ is obtained          then followed by zeros. The second part fi,2 Φ
                                                                                                                    takes the
                                                                    output of the first part as an input, and outputs a bit-
  by shifting yg = 1 by 2k − 1 bits. This concludes the
                                                                    vector obtained by copying 2k−u(i) times the block of
  proof that ψgΦ is true if and only if xg = yg = 1.
                                                                    the first 2u(i) bits.
• For fiΦ corresponding to universally quantified variable            Φ
                                                                    fi,1 consists only of the input and the output layer. The
  xi , let Bi be the block of bits starting with 2u(i) zeros        input layer consists of two neurons, one of which coin-
  followed by 2u(i) ones. The bit-vector ci should then             cides with the input neuron xg of the gadget g Φ . We de-
  consist of 2k−u(i)−1 repetitions of the block Bi . The            note the other input neuron by zi . The output layer con-
      sists of two neurons hi and hg . The weights of edges                Hence, the size of the instance of the quantized neural
      from zi to hi and from xg to hg are set to 1, and weights            network verification problem to which we reduced Φ is
      of edges from zi to hg and from xg to hi are set to 0.               O(n3 + n · |φ|), which is polynomial in the size of Φ.
      Biases and cut-off values of all edges between the lay-              Correctness of reduction. It remains to prove correctness of
      ers are set to 0 and 2k , respectively. All bit-shifts are           our reduction, i.e. that Φ is true if and only if the correspond-
      also set to 0, with the exception of the edge from xg to             ing quantized neural network verification problem is satisfi-
      hg whose bit-shift is set to 2u(i) . These choices ensure            able.
      that hi = zi and that hg is a bit-vector that starts with               Suppose first that Φ is true, i.e. that for each existentially
      2u(i) 0-bits followed by 2k − 2u(i) 1-bits. The gadget               quantified variable xi in Φ there exists a truth table ti of
        Φ
      fi,1 is accompanied by the predicate ψiΦ defined via                 size 2u(i) , such that any valuation of universally quantified
                                                                           variables U together with the corresponding values of exis-
                      ψiΦ := (hi = (hi ∧ ¬(hg )).
                                                                           tentially quantified variables defined by truth tables form a
      This choice of ψiΦ together with the design of fi,1         Φ
                                                                     en-   satisfying assignment for the quantifier-free formula φ in Φ.
                        Φ    Φ
      force that ψi ∧ ψg is satisfied if and only if xi = zi               Consider the following set of inputs z1 , . . . , zn , xg to gad-
      and the last 2k − 2u(i) bits of xi = zi are equal to 0.              gets f1Φ , . . . , fnΦ , g Φ :
      Since the goal of the second part is to just copy 2k−u(i)             • If xi is universally quantified, then zi = 0.
      times the block of the first 2u(i) bits of the output hi of           • If xi is existentially quantified, consider ti as a bit-vector
         Φ
      fi,1                      Φ
             , the second part fi,2 is constructed analogously as             of bit-width 2u(i) with elements ordered in such a way that
      in the case of neural networks corresponding to univer-                 corresponding valuations of universally quantified vari-
      sally quantified variables above.                                       ables on which xi depends in Φ are ordered lexicograph-
   Recall, constant bit-vectors, bit-widths of bit-vectors as                 ically. Then zi starts with a block of bits identical to ti ,
   well as the number of bits used for rounding (i.e. bit-                    followed by zeros.
   shifts) are encoded in binary representation. Thus, each                 • zg = 0.
   of the values used in the construction of gadgets fiΦ and               From our construction of neural networks and the predicate
   g Φ is encoded using at most k bits, and is polynomial in               ψ Φ we know that:
   the size of Φ. On the other hand, from our construction                  • g Φ (zg ) = 1.
   one can check that each gadget consists of at most 2k + 4
   neurons. Therefore, as there are n + 1 gadgets the size of               • If xi is universally quantified, then fiΦ (zi ) is equal to the
   all networks combined is O(k·(2k+4)·(n+1)) = O(n3 ).                       bit-vector ci whose j-th component is equal to 1 if and
                                                                              only if the value of xi in the j-th valuation of U in the
2. Construction of the output predicate ψ Φ . Denote by                       lexicographic ordering is equal to 1, where 1 ≤ j ≤ 2k .
   y1 , . . . , yn , yg the outputs of f1Φ , . . . , fnΦ , g Φ , respec-
   tively. We define ψ Φ as                                                 • If xi is existentially quantified, then fiΦ (zi ) is the bit-
                                                                              vector obtained by copying the block ti 2k−u(i) times.
         ψ Φ := (φbw (y1 , . . . , yn ) = yg ) ∧ ψauxiliary
                                                  Φ
                                                            ,     (14)        Thus, the j-th component of fiΦ (zi ) is equal to the value
   where φbw is the quantifier-free formula in QF_BV2 bw                      in the truth table ti corresponding to the j-th valuation of
   identical to φ, with only difference being that the inputs                 U in the lexicographic ordering, where 1 ≤ j ≤ 2k .
   of φbw are bit-vectors of bit-width 2k instead of boolean               Finally, as ψ Φ is obtained by considering a bit-vector ver-
   variables and logical operations are also defined over bit-             sion of formula φ and then checking if each component of
                              Φ
   vectors. The formula ψauxiliary  collects the auxiliary logi-           the output is equal to 1, it follows that the output of ψ Φ on
   cal predicates that were introduced by our construction of              inputs f1Φ (z1 ), . . . , fnΦ (zn ) is equal to 1, thus showing that
   each gadget above, i.e.                                                 the quantized neural network verification problem is satisfi-
                                  n                                        able.
                                                                              Conversely, suppose that z1 , . . . , zn , zg is a set of satisfy-
                                  ^
                     Φ
                    ψauxiliary :=    ψiΦ ∧ ψgΦ .
                                    i=1
                                                                           ing inputs to the quantized neural network verification prob-
                                                                           lems. Then for each existentially quantified variable xi , we
   As yg = 1 if and only if ΨΦ
                             g is satisfied, the formula ψ
                                                           Φ
                                                                           construct a truth table ti as follows. Again, consider ti as
   is true if and only if the equality φbw (y1 , . . . , yn ) = yg         a bit-vector of bit-width 2u(i) , where elements are ordered
   holds for each component. Intuitively, ψ Φ performs bit-                in such a way that the corresponding valuations of univer-
   wise evaluation of the formula φ on each component of                   sally quantified variables on which xi depends are ordered
   bit-vector inputs, and then checks if each output is equal              lexicographically. Then we set ti to be equal to the block of
   to 1. The size of ψ Φ is thus O(|φbw |) = O(|φ|·k + 3 · n +             first 2u(i) bits in zi . From our construction of the quantized
   3) = O(|φ|·n), where the additional factor k comes from                 neural network and ψ Φ , and the fact that z1 , . . . , zn , zg is
   the fact that inputs of φbw are bit-vectors of bit-width 2k ,           a satisfying inputs to the quantized neural network verifica-
   and bit-widths are encoded in binary representation.                    tion problem, it follows that for any valuation of U the cor-
   Note that the above expression for ψ Φ differs from that                responding values of existentially quantified variables de-
   in the sketch proof of Theorem 1, where we omitted the                  fined by these turth tables yield a satisfying assignment for
               Φ
   formula ψauxiliary to simplify the presentation.                        φ. Hence, the QBF formula Φ is true, as desired.
