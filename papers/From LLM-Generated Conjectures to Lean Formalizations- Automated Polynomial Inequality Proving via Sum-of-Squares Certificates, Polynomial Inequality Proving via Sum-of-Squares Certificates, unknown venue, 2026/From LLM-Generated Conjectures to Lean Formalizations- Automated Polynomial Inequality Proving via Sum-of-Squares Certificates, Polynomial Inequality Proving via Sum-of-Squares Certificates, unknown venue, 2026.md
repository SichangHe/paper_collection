                                               From LLM-Generated Conjectures to Lean Formalizations: Automated
                                                  Polynomial Inequality Proving via Sum-of-Squares Certificates


                                                            Ruobing Zuo 1 Hanrui Zhao 2 Gaolei He 1 Zhengfeng Yang 1 Jianlin Wang 3


                                                                   Abstract                                    automation of complex inequality proving has recently
                                                                                                               emerged as an important benchmark for evaluating the lim-
                                              Automated proving of polynomial inequalities                     its of AI in mathematical reasoning (Trinh et al., 2024;
arXiv:2605.15445v1 [cs.AI] 14 May 2026




                                              is a fundamental challenge in automated mathe-                   Wei et al., 2024; He et al., 2024; Li et al., 2025c). Recent
                                              matical reasoning, where rich algebraic structure                systems such as AlphaGeometry (Trinh et al., 2024; Cher-
                                              and a rapidly growing certificate search space hin-              vonyi et al., 2025) and Seed-Prover (Chen et al., 2025b;a)
                                              der scalability. Purely symbolic approaches pro-                 have demonstrated impressive performance on Olympiad-
                                              vide strong guarantees but often scale poorly as                 level problems, highlighting the potential of large language
                                              the number of variables or the degree increases,                 models (LLMs) for theorem proving. Nevertheless, auto-
                                              due to expensive algebraic manipulations and                     mated inequality proving remains highly challenging due
                                              rapidly growing intermediate expressions. In                     to the long reasoning chains, vast search spaces, and sub-
                                              parallel, LLM-guided methods have made no-                       stantial computational complexity involved, especially for
                                              table progress, particularly on competition-style                high-dimensional and multivariate cases.
                                              inequalities with a small number of variables.
                                              To address the remaining scalability challenges,                 Symbolic computation has long been a cornerstone for prov-
                                              we propose NSPI, a neuro-symbolic framework                      ing polynomial inequalities (Yang, 1999; Lasserre, 2002;
                                              that combines the complementary strengths of                     Uray, 2020; Yang et al., 2023). A widely used approach is
                                              LLMs and symbolic computation for polynomial-                    based on Sum-of-Squares (SOS) decomposition (Kaltofen
                                              inequality proving. Concretely, an LLM pro-                      et al., 2012), which transforms the nonnegativity of a poly-
                                              poses a conjecture in the form of an approximate                 nomial into a semidefinite programming (SDP) problem.
                                              polynomial Sum-Of-Squares (SOS) decomposi-                       Modern computer algebra systems further support such
                                              tion; we refine it via symbolic computation to                   pipelines with basic algebraic operations (Heck & Koepf,
                                              obtain an exact polynomial SOS representation,                   1993; De Moura & Bjørner, 2008; Meurer et al., 2017).
                                              which directly proves the target inequality, and                 However, purely symbolic approaches often suffer from
                                              we further certify the proof in Lean, yielding an                poor scalability due to combinatorial explosion and typi-
                                              end-to-end pipeline from heuristic discovery to                  cally fail to produce structured, human-readable proofs. In
                                              machine-checked proof. Experiments on chal-                      parallel, recent LLM-based methods have substantially ad-
                                              lenging benchmarks involving polynomials with                    vanced automated formal theorem proving (Lample et al.,
                                              up to 10 variables demonstrate the effectiveness                 2022; Xin et al., 2025; Ren et al., 2025; Lin et al., 2025a;
                                              and scalability of the proposed method.                          Wang et al., 2025; Lin et al., 2025b) integrated with proof
                                                                                                               assistants such as Lean (De Moura et al., 2015) and Is-
                                                                                                               abelle (Paulson, 1990). Nevertheless, their performance
                                         1. Introduction                                                       on complex algebraic inequalities remains limited by the
                                                                                                               scarcity formalized training data.
                                         Polynomial inequalities play a fundamental role in areas
                                                                                                               To address the above challenges, a promising approach is to
                                         such as optimization, control, and combinatorics (Kaltofen
                                                                                                               integrate neural and symbolic methods, thereby combining
                                         et al., 2012; Parrilo, 2000a; Maréchal et al., 2015). The
                                                                                                               the strengths of structured reasoning and symbolic preci-
                                             1
                                               School of Software Engineering, East China Normal Univer-       sion while mitigating dependence on large-scale formalized
                                         sity, Shanghai, China 2 College of Computer Science and Tech-         training data (Heule et al., 2016; Trinh et al., 2024; Wei
                                         nology, National University of Defense Technology, Changsha,          et al., 2024; Li et al., 2025a). However, existing approaches
                                         China 3 School of Computer and Information Engineering, Henan
                                         University, Kaifeng, China. Correspondence to: Zhengfeng Yang         (e.g., AIPS (Wei et al., 2024)) remain limited in two key
                                         <zfyang@sei.ecnu.edu.cn>.                                             aspects: they mainly target low-dimensional cases (e.g.,
                                                                                                               ternary or quaternary polynomials), and typically restrict
                                         Preprint. May 18, 2026.

                                                                                                           1
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

the role of LLMs to search guidance or strategy selection,         rapidly. Various approaches integrate LLMs with interactive
since directly using LLMs to generate symbolic conjectures         proof assistants such as Lean (De Moura et al., 2015) to pro-
remains difficult to control and certify. In this paper, we        duce machine-checkable formal proofs. One line of work
propose a new neuro-symbolic framework for polynomial              fine-tunes models on large-scale corpora of formal proofs
inequality proving that targets unconstrained polynomial in-       to generate proof strategies or local proof tactics (Polu
equality scenarios, high-dimensional multivariate problems         & Sutskever, 2020; Lample et al., 2022; Xin et al., 2025).
and elevates LLMs to primary conjecture generators. By for-        Another line explores end-to-end generation of complete
mulating inequality proving as SOS-based certification and         formal proofs (Ren et al., 2025; Lin et al., 2025a; Wang
tightly coupling LLM-driven hypothesis generation with             et al., 2025; Lin et al., 2025b), exemplified by Goedel-
symbolic refinement and formal verification, our approach          Prover (Lin et al., 2025a) ,Kimina Prover (Wang et al.,
establishes an end-to-end pipeline from heuristic discov-          2025) and DeepSeek-Prover-V2 (Ren et al., 2025). How-
ery to certified proof, significantly extending the scope of       ever, LLM-based methods are limited by the scarcity and
neuro-symbolic automated theorem proving.                          uneven quality of formal-proof data, and thus remain weak
                                                                   on high-dimensional inequalities.
The main contributions can be summarized as follows:
                                                                   Neuro-Symbolic Theorem Proving. To bridge the scala-
  • We propose a neuro-symbolic approach for auto-                 bility limitations of purely symbolic methods and the data
    mated polynomial inequality proving, which automati-           bottleneck of purely neural approaches, recent work has
    cally generates complete formal proofs of inequalities         explored neuro-symbolic integration for automated theorem
    through a pipeline of neural conjecture, symbolic cor-         proving (Trinh et al., 2024; Wei et al., 2024; Li et al., 2025a;
    rection, and Lean verification.                                Chervonyi et al., 2025). These methods typically combine
                                                                   neural models with symbolic solvers, using learning-based
  • We develop a principled reliability bridge that in-            components to guide or prioritize symbolic reasoning or
    tegrates LLM-based heuristic conjecture generation             derivation steps. Representative systems such as Alpha-
    with symbolic exact certification, transforming neu-           Geometry (Trinh et al., 2024), AIPS (Wei et al., 2024), and
    ral conjectures into machine-checkable proofs and en-          LIPS (Li et al., 2025a) demonstrate the effectiveness of
    abling automated inequality proving to scale to higher-        this paradigm in geometry and algebraic inequality prov-
    dimensional multivariate cases.                                ing. In contrast, while existing approaches mainly focus
  • Extensive experiments on 522 challenging inequal-              on learning-guided derivation or strategy selection, we treat
    ity problems demonstrate the effectiveness of the              LLMs as generators of symbolic conjectures and machine-
    proposed method, which outperforms both symbolic               checkable formal verification. Centered on verifiable SOS
    computation-based and LLM-assisted approaches, es-             certificates, our framework establishes an end-to-end neuro-
    pecially on problems with up to 10 variables.                  symbolic pipeline for tackling more complex multivariate
                                                                   polynomial inequalities.

2. Related Work
                                                                   3. Preliminaries
Symbolic Methods for Inequality Proving. Polynomial in-
equality proving has traditionally been approached through         Let R[x] := R[x1 , . . . , xn ] be the ring of polynomials in n
symbolic computation. A classical method is based on               variables with coefficients in the real field R. A polynomial
the SOS methodology (Kaltofen et al., 2012; Martin-Dorel           f (x) ∈ R[x] is said to be nonnegative or positive semidef-
& Roux, 2017), which reduces nonnegativity certification           inite (PSD) if f (x) ≥ 0 for all x ∈ Rn . In this work, we
to the existence of an SOS decomposition and further to            focus on automated proving of unconstrained polynomial
solving SDP problem. Meanwhile, computer algebra sys-              nonnegativity: given f ∈ R[x], our goal is to formally prove
tems such as Maple (Heck & Koepf, 1993), Z3 (De Moura
& Bjørner, 2008) and SymPy (Meurer et al., 2017) pro-                                 f (x) ≥ 0,    ∀x ∈ Rn .                  (1)
vide fundamental symbolic capabilities, which support alge-
braic preprocessing and manipulation in inequality-proving
pipelines. Nevertheless, purely symbolic approaches typi-          Beyond establishing (1) mathematically, automated theorem
cally struggle to produce human-readable reasoning steps           proving additionally requires certificates that are rigorous
and often suffer from combinatorial explosion as the prob-         and machine-checkable, rather than purely numerical or
lem dimension increases, particularly for multivariate and         heuristic validations.
algebraically intensive polynomial inequalities.
                                                                   A widely-used sufficient certificate for (1) is a sum-of-
LLM-based Formal Theorem Proving. In recent years,                 squares (SOS) decomposition. A polynomial f (x) is said
LLM-based automated theorem proving has advanced                   to be an SOS, if there exist polynomials f1 (x), . . . , fm (x)

                                                               2
        From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates


                    Neural Conjecture                                 Symbolic Correction                         Formal Verification

                  Computation-Driven                                                                          Exact SOS Representation
                                                                      SOS Conjecture No.
                   Structure-Driven
                               Data Construction
                                                                           Newton’s Method
                                                                                                                              Theorem Statement
                Polynomial-SOS Pairs

                          Model Training                                   Rational Recovery                                     SOS Expression




                                   SOS Conjectures
                                                                   Exact SOS Representation

            Conjecture & Ranking
                                           ...




                                                                                                                                 Proof Template



Figure 1. Overview of Neuro-Symbolic SOS-based Polynomial Inequality Proving (NSPI). (1) Neural Conjecture Module: Non-
negative polynomial-SOS representation pairs are constructed using computation-driven and structure-driven approaches. A Large
Language Model (LLM) is trained on the constructed data to function as an SOS structure conjecturer, which generates corresponding SOS
representations based on the non-negative polynomials and ranks them according to the magnitude of the errors. (2) Symbolic Correction
Module: An exact SOS representation is derived from the top-ranked SOS structure conjectures through a symbolic computation process
that involves Newton iteration and rational recovery. (3) Formal Verification Module: Based on the exact SOS representations and
predefined Lean proof templates, a complete Lean formal proof is automatically generated.


such that                                                                            4. Methodology
                                      m
                                      X                                              In this section, we introduce Neuro-Symbolic SOS-based
                         f (x) =                 fi (x)2 .                 (2)
                                                                                     Polynomial Inequality Proving (NSPI), a neuro-symbolic
                                       i=1
                                                                                     framework for automated proving of unconstrained poly-
It is immediate f (x) being SOS implies that is nonnegative                          nomial inequalities. NSPI is designed as a pipeline that
over Rn , hence an explicit SOS decomposition provides a                             integrates LLM-based conjecture with symbolic computa-
constructive certificate of (1). Notice that necessarily f (x)                       tion and formal verification. The overall architecture of
must be of even degree 2d. Let vd (x) be the vector                                  NSPI is illustrated in Fig. 1, which depicts the following
                                                                                     three main stages:
      vd (x) = [1, x1 , x2 , . . . , xn , x21 , x1 x2 , . . . , xdn ]T ,
                                                                                     [Neural Conjecture]. The LLM is employed as a structure
of all monomials in x and whose degrees are at most d,                              conjecturer for sum-of-squares (SOS) representations. By
which has dimension s(d) = n+d d . Then f (x) is SOS if
                                                                                     combining computation-driven and structure-driven strate-
and only if there exists a symmetric positive semidefinite                           gies, we construct a diverse dataset of nonnegative polyno-
matrix G ⪰ 0 such that                                                               mials and their corresponding SOS pair forms. The con-
                                                                                     jecturer is trained on synthetically generated data via a pro-
                        f (x) = v(x)T Gv(x).                               (3)       gressive two-stage training scheme, enabling the LLM to
                                                                                     more accurately predict plausible SOS structures for given
Equating coefficients in the identity (3) yields a system of
                                                                                     polynomials (see more details in Section 4.1).
linear equations that the entries of G must satisfy. Therefore,
determining whether f (x) is SOS can be formulated as a                              [Symbolic Correction]. Symbolic computation serves as
semidefinite feasibility problem:                                                    a precision bridge in SOS-based proving. At this point,
                               s(d)×s(d)
                                                                                     symbolic computation tools are employed to refine the ap-
              find G ∈ R
                                                                                    proximate SOS decomposition produced in the previous
                 s.t. G ⪰ 0, G = GT ,                       (4)                      stage. By combining Newton-type iterative refinement with
              
                                     T                                              rational recovery techniques, numerical solutions are sys-
                        f (x) = v(x) Gv(x).
                                                                                     tematically converted into exact rational representations,
However, SDP solvers typically return numerical solutions,                           yielding a precise SOS certificate of the target polynomial.
while formal verification requires exact certificates. This                          (see more details in Section 4.2).
motivates our focus on constructing exact SOS certificates                           [Formal Verification]. This module converts the precise
that can be directly checked in a proof assistant.

                                                                                 3
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

SOS decomposition into machine-checkable Lean proof                   obtained by either approach, the SOS polynomial f (x) is
templates, thereby ensuring that the entire proving process,          generated by instantiating a monomial basis v(x).
from conjecture to certificate, is fully verified by a trusted
                                                                      (1) Computation-Driven Methods. We first consider con-
formal kernel. (see more details in Section 4.3).
                                                                      structing the Gram matrix G  e through numerical procedures.
                                                                      The objective is to systematically control the magnitude and
4.1. Neural Conjecture: LLM-Guided SOS Generation                     precision of the coefficients while ensuring that the resulting
Given an input polynomial, the neural conjecture compo-               Ge remains positive semi-definite. The computation-driven
nent leverages the structural conjecturing capability of large        methods comprise two main approaches.
language models to propose candidate the sum-of-squares               [Explicit Algebraic Construction]. One direct way to
decomposition. The overall procedure is organized into two            obtain a PSD Gram matrix G   e is based on spectral shifting.
complementary parts as follows:                                       Specifically, we first generate a symmetric integer matrix
                                                                      G ∈ Sm and compute its smallest eigenvalue λmin . Setting
  i) Constructing SOS training data: we construct large-
     scale polynomial–SOS training pairs by generating                           e = G − kI ⪰ 0, where k = ⌊λmin ⌋
                                                                                 G                                               (5)
     SOS polynomials through Gram matrix synthesis,
     using both computation-driven and structure-driven                               e ⪰ 0, since its smallest eigenvalue satisfies
                                                                      yields a matrix G
     mechanisms to obtain PSD matrices with controlled                λmin − k ≥ 0.
     coefficient properties. (see Subsection 4.1.1)
                                                                      Alternatively, a PSD Gram matrix can also be constructed
 ii) Training the SOS structure conjecturer: we train an              in factored form. Let L ∈ Zm×k (k ≤ m) be a sparse integer
     SOS structure conjecturer via a progressive two-stage            matrix and let D ∈ Rk×k be a positive definite diagonal
     scheme, where supervised fine-tuning provides a cold             matrix, where k corresponds to the number of squared terms
     start on the synthetic corpus and curriculum-based re-           in the SOS decomposition. Then the matrix
     inforcement learning further improves conjecturing
     performance on harder multivariate instances. (see                                       e = LT DL
                                                                                              G                                  (6)
     Subsection 4.1.2)
                                                                      is symmetric positive semidefinite by construction.
4.1.1. SOS DATA C ONSTRUCTION M ETHOD                                 [Optimization-Based Approach]. Another computation-
                                                                      driven method constructs the Gram matrix G  e through Linear
Constructing nonnegative polynomials and and their corre-
                                                                      Matrix Inequality (LMI) optimization. This approach em-
sponding SOS representations in a systematic and numeri-
                                                                      ploys LMI optimization to compute an approximate SOS
cally well-behaved manner is a nontrivial task. A straightfor-
                                                                      representation, followed by controlled adjustment to obtain
ward approach is toPrandomly sample polynomials fi (x) and
                                                                      an exact integer-coefficient solution. Suppose f (x) ∈ Z[x]
construct f (x) = i fi (x)2 . However, this naive strategy
                                                                      is a randomly selected integer-coefficient polynomial. We
suffers from two major limitations: (1) the coefficients of the
                                                                      first solve the following semidefinite program:
generated fi (x) are typically non-integer, which makes the
resulting polynomial inconsistent with the typical symbolic                         
representations that require integer coefficients, and (2) the                      max λ
                                                                                    
expansion of randomly generated squared polynomials often                              s.t. f (x) = v(x)T Gv(x)                (7)
                                                                                                                T
                                                                                            G − λI ⪰ 0, G = G .
                                                                                    
leads to severe coefficient swelling, producing polynomials
with unreasonably large or unbalanced coefficients.
                                                                      Let (λ, G) be an optimal solution. Since G − λI ⪰ 0,
To address these issues, we develop a novel data construc-            for any integer k ≥ −λ we have G + kI ⪰ 0. Choosing
tion method grounded in the algebraic structure of SOS                k := ⌈−λ⌉ ∈ Z yields G + kI ⪰ 0, and therefore
decomposition. As reviewed in Section 3, a polynomial
f (x) is SOS if and only if there exists a positive semidefi-         f˜(x) := f (x) + v(x)T (kI)v(x) = v(x)T (G + kI)v(x)
nite (PSD) Gram matrix G  e such that f (x) = v(x)T Gv(x),
                                                      e
where v(x) denotes the vector of monomials. Consequently,             is SOS polynomial with integer coefficients. Then the Gram
the problem of generating suitable polynomial–SOS pairs               matrix is updated as G e = G + kI. Appendix B.1 pro-
reduces to the problem of constructing a PSD Gram matrix              vides the theoretical foundations for the aforementioned
Ge with controlled coefficient structure.                             computation-driven methods.
Based on this observation, we propose two families of SOS             (2) Structure-Driven Methods. This category constructs
data construction methods, namely computation-driven and              the Gram matrix G e by exploiting algebraic matrix struc-
structure-driven approaches. Once a Gram matrix G     e is            tures that guarantee positive semidefiniteness by design,

                                                                  4
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

                                                         Poly 1
                                                         Poly 2      Right
                                                                  conjectures
                                                         Poly 3                                     #vars (n)
                                                         Poly 4
                                                         Poly 5     Wrong              RL Dataset               Curriculum Data
                                                                  conjectures
       Base Model          Cold Start                    Poly 6
                            (SFT)




                                                                       ...
                                                            ...
                                                                                Progressive Reinforcement Learning
    Polynomial-SOS Pairs                                                                  (GRPO + CL)
                                                                                                                                  SOS Conjecturer


Figure 2. Two-stage training of the SOS conjecturer: (1) Cold Start: supervised fine-tuning (SFT) on large-scale synthetic polyno-
mial–SOS pairs; (2) Progressive reinforcement learning: curriculum-based GRPO on challenging training data.


most notably diagonally dominant (dd) matrices and scaled              notes a non-negative polynomial and S represents its corre-
diagonally dominant (sdd) matrices.                                    sponding SOS decomposition. This stage endows the base
                                                                       model with the foundational capability for SOS structural
Specifically, a matrix G ∈ Rm×m is defined as diag-
                                                                       reasoning, serving as a critical precursor to the subsequent
onally dominant      if it satisfies the following condition:
         P                                                             reinforcement learning phase. Further details regarding the
Gii ≥       j̸=i |Gij |, ∀i. By Gershgorin’s circle theorem            synthetic dataset are provided in Appendix D.2.
(Gerschgorin, 1931), any symmetric G that satisfies the di-
agonal dominance condition is guaranteed to be positive                Progressive Reinforcement Learning.We further optimize
semidefinite. In this case, G  e can be directly initialized as        the model’s SOS structural reasoning through progressive
a diagonally dominant matrix. Furthermore, we construct                reinforcement learning on challenging tasks. Specifically,
Ge in a structured diagonally dominant form by restricting             we curate the training instances that remain unsolved by
it to a non-negative combination of m rank-one generators              the cold-started model into an easy-to-hard curriculum and
inspired by (Barker & Carlson, 1975):                                  conduct curriculum-based Group Relative Policy Optimiza-
                                                                       tion (GRPO) (Shao et al., 2024). The reward function is
                                  2
                                m
                                X                                      designed with three critical components:
                           G
                           e=           ηi Ui ,             (8)
                                i=1                                    [Accuracy Reward]. The accuracy reward encourages SOS
                                                                       structure conjectures with smaller errors compared to the
where G e is an m × m symmetric matrix, ηi ≥ 0, and                    original polynomial. It measures the numerical fidelity of
Ui = ui u⊤ i , with ui ∈ R
                            m
                               having at most two non-zero             the conjecture and is computed as
components, each equal to ±1. This representation provides                                                            1
a convenient structural parameterization of PSD Gram matri-                           RAccuracy =                                     ,             (9)
ces, and naturally extends to the scaled diagonally dominant                                          1 + α∥f (x) − f̂ (x)∥2
case to introduce greater flexibility. Appendix B.2 provides           where f (x) represents the original polynomial, f̂ (x) denotes
the theoretical foundations and more details of structure-             the SOS structure conjecture generated by the model, and α
driven methods.                                                        is a scaling factor.
4.1.2. T RAINING THE SOS S TRUCTURE C ONJECTURER                       [Format Reward]. A binary indicator ensuring the output
                                                                       strictly adheres to the predefined SOS structural template
To obtain an LLM-based SOS structure conjecturer with                  and delimiters (e.g., <SOS Expression>).
strong structural reasoning capability, we design a progres-
sive two-stage training scheme. As illustrated in Fig. 2, the          [Algebraic Structure Penalty]. The algebraic structure
procedure consists of two phases. (1) Cold Start: endow                consistency penalty is designed to ensure that the set of
the model with the ability to conjecture SOS structures via            nonzero monomials in the SOS strucure conjecture closely
supervised fine-tuning (SFT) on the constructed polynomial-            matches that of the original polynomial, which comprises a
SOS pair data. (2) Progressive Reinforcement Learning:                 soft penalty and a hard penalty. Appendix D.3 details the
further enhance the model’s SOS-structure conjecturing                 specific computation procedure and provides further details
performance via curriculum-based reinforcement learning                on the progressive reinforcement learning procedure.
(RL) on challenging data.
                                                                       4.2. Symbolic Correction: Exact Rational Recovery
Cold Start.We perform SFT on the base model using over
one million synthetic data samples. These samples are gen-             In this part, the symbolic correction module serves as a
erated via the method described in Section 4.1.1, with each            precision bridge between model-generated SOS structure
instance formulated as a pair (f (x), S), where f (x) de-              conjecture and the exact representation required for formal

                                                                  5
        From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

verification, which encompasses two stages: Gauss–Newton                 and then rationalize the resulting matrix. (2) Boundary case:
refinement and rational recovery.                                        when the matrix is numerically rank-deficient, direct matrix
                                                                         rationalization is avoided. Instead, we perform a truncated
Gauss–Newton Refinement. After obtaining the SOS struc-
                                                                         LDL⊤ factorization followed by simultaneous Diophantine
tural conjecture fˆ(x) from the neural conjecture module,
                                                                         approximation to recover rational vectors while preserving
we perform Gauss–Newton refinement to enhance the nu-
                                                                         the rank structure. Appendix C provides further details of
merical precision of the SOS representation.
                                                                         Symbolic Correction module.
First, the corresponding monomial basis v(x) is extracted,
and an initial floating-point Gram matrix G is constructed               4.3. Formal Verification: Lean Proof Generation
such that fˆ(x) ≈ v(x)T Gv(x). To refine G using the
Gauss–Newton iteration, we compute the Cholesky decom-                   After obtaining the exact SOS certificates, the formal verifi-
position of G:                                                           cation module generates a complete Lean proof. By integrat-
                                                                         ing pre-defined proof templates with the neural conjecture
                                                  !2
                                Xk  X                                    and symbolic correction modules, we implement a callable
   fˆ(x) ≈ v(x) LL v(x) =
                  T    T
                                         ci,α x α
                                                     , (10)              Lean tactic, llm ineq. Given a target polynomial and its
                                  i=1     α                              exact SOS certificate, llm ineq automatically constructs a
                                                                         complete Lean proof by discharging two obligations:
where k is the rank of the matrix G, and LLT denotes the
Cholesky factorization of the Gram matrix G.                             Equality between polynomial and SOS certificate. Lean
                                                                         expands the polynomial and the SOS expression into
The Gauss–Newton iteration is applied to compute the coef-
                                                                         canonical forms and checks their equality via the lin-
ficient correction term ∆ci,α xα such that
                                                                         ear combination tactic. For example, the code below shows
                    k
                                               !2                        how Lean verifies the equality:
                  X     X
          ˆ
          f (x) =                 α
                            ci,α x + ∆ci,α x α
                                                  ,   (11)
                   i=1     α                                              have h_eq : p = (terms.map (fun (q, k) =>
                                                                               k * qˆ2)).sum := by
where ∆ci,α xα represents the perturbation to the poly-                     linear_combination
nomial coefficients, and the Gram matrix is updated as
G + ∆G. The optimization objective is to minimize the                    Nonnegativity of the SOS expansion. Lean provides sev-
backward error:                                                          eral built-in strategies for proving nonnegativity. The non-
                θ = ||fˆ(x) − v(x)T Gv(x)||.                 (12)        negativity of the SOS expression is proved by Lean’s posi-
                                                                         tivity tactic, which recursively applies standard rules (e.g.,
Gauss–Newton iteration terminates when θ falls below a                   sq nonneg, mul nonneg, add nonneg).
predefined tolerance threshold τ . This process is crucial
for the subsequent rational recovery process, ensuring that               have h_nn : 0 <= (terms.map (fun (q, k)
the obtained SOS representation achieves high precision.                      => k * qˆ2)).sum := by
Appendix C.1 provides further details of the procedure.                     positivity

Rational Recovery. The numerical Gram matrix GN ob-
tained from Gauss–Newton refinement contains inherent                    Further details on the proof templates and illustrative exam-
floating-point errors. Our objective is to transform the ma-             ples are provided in Appendix E.
trix into an exact rational PSD matrix that rigorously satis-
fies the polynomial identity without numerical uncertainty,              5. Experiments
thereby yielding an exact SOS representation.
                                                                         5.1. A Challenging Benchmark for Multivariate
According to a classical result on rational recovery (Peyrl                   Polynomial Inequalities
& Parrilo, 2008a),1 we distinguish two recovery regimes
depending on the numerical rank of the refined solution.                 Existing mathematical benchmarks for theorem proving
(1) Interior-point case: when the refined Gram matrix lies               do not encompass proofs of high-dimensional multivari-
strictly in the interior of the PSD cone, we project it orthogo-         ate polynomial inequalities. To fill this gap, we con-
nally onto the affine subspace defined by the SOS constraints            struct PolyIneqBench, a challenging benchmark for un-
   1
                                                                         constrained polynomial inequality proving. It contains 522
     If a polynomial admits a Gram matrix lying strictly in the          complex inequality problems with 3 to 10 variables, all trans-
interior of the PSD cone, then there exists a threshold δ > 0 such
that any numerical Gram matrix within δ of the exact solution            formed into the form of (1) and formalized in Lean. Among
can be converted into an exact rational PSD matrix by combining          them, 102 problems are collected from international mathe-
rational approximation with orthogonal projection                        matics competitions and other authoritative sources (Chen,

                                                                     6
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

Table 1. Comparative Performance on PolyIneqBench (n=3 to 10). Pass: success rate within 1 hour; t(s): mean execution time of
solved instances. DS-Prover-v2 denotes DeepSeek-Prover-v2. Best and second-best results are in bold and underlined, respectively.

                            n=3              n=4               n=5                n=6                             n=7                     n=8                n=9                      n=10
 Method Name
                         Pass t(s)        Pass t(s)         Pass t(s)          Pass t(s)                       Pass t(s)               Pass t(s)          Pass t(s)                 Pass t(s)
                                                                    Symbol-based Method
 Maple                   97.6% 24.6       39.0% 107.4 26.7% 451.2 8.2% 54.9 6.7% 821.5 6.67% 456.3 3.3% 3176.6 1.7% 1525.6
 Z3                      97.6% 0.6        32.5% 21.8 23.3% 101.9 19.7% 196.4 1.7% 65.0 1.7% 1598.6 0.0% NA 0.0% NA
                                                                      LLM-based Prover
 DS-Prover-v2            42.9% 19.8 2.6% 17.9 0.0% NA                          0.0% NA                         0.0% NA 0.0% NA                            0.0% NA 0.0% NA
 Goedel-Prover-v2        20.2% 189.6 5.2% 136.4 0.0% NA                        0.0% NA                         0.0% NA 0.0% NA                            0.0% NA 0.0% NA
 Kimina-Prover           36.9% 117.0 5.2% 111.7 0%   NA                        0.0% NA                         1.7% 120.6 0.0% NA                         1.7% 115.8 0.0% NA
                                                                   General-purpose LLM
 GPT-5.2                 26.2% 56.8 10.4% 86.7 1.7% 51.8 4.9% 154.4 3.3% 75.3 3.3% 55.9 3.3% 68.3 1.7% 49.2
 Gemini-3-Pro            22.6% 91.2 24.7% 102.4 36.7% 109.8 21.3% 138.9 15.0% 140.7 15.0% 126.7 13.3% 143.5 6.7% 116.7
 DeepSeek-V3.2           14.3% 368.4 6.5% 420.9 1.7% 526.8 1.6% 495.8 5.0% 393.8 5.0% 561.5 1.7% 358.0 3.3% 678.9
                                                                           Hybrid system
 LIPS                    71.4% 82.5       27.3% 131.0 13.3% 141.6 11.5% 195.7 8.3% 150.2 8.3% 153.1 1.7% 148.7 0.0% NA
 NSPI (ours)             44.1% 16.3       40.3% 14.4 36.7% 20.0 29.5% 21.4 26.7% 29.6 21.7% 63.9 15.0% 20.8 11.7% 58.3


                                                                                                      Deepseek-Prover-v2            GPT-5.2            LIPS                        Runtime (Synth)
                                                                                                      Godel-prover                  Gemini-3-pro       NSPI (ours)                 Fastest
                   6.9% 6.9%                                                                          Kimina-Prover                 deepseek-3.2       Runtime (Real)              2nd Fastest
                                               Literature Categories
          12.7%                                  (Chen, 2014)                                                                        67.65
                                                 (Tung, 2012)                                                                                                                            500
                                                 (Riasat, 2008)




                                                                                                                                                                                             Average Runtime (s)
                                                 (Manfrino et al., 2010)                              60
                                                                                   Success Rate (%)




       6.9%                            30.4%     (Mildorf, 2005)                                                                                                                         400
                                                 (Parvardi, 2011)                                                                        43.14
       2.9%                                      (Tung & Zhe, 2014)                                   40   37.25                                                                         300
                                                 (Lee, 2005)                                                       33.33
         6.9%                                    (Andreescu, 2019)                                                                                                            25.95 200
                                                 Competition Problems                                                  23.5321.57                               19.29
                                                 Classical Inequalities                               20       18.63
              5.9%              3.9%             Others                                                                        11.76                                        9.05         100
                  2.9%5.9% 7.8%                                                                                                                           0.714.05      3.81
                                                                                                                                                   NA 0.48
                                                                                                       0                                                                                 0
                                                                                                                   PolyIneq-Real                       PolyIneq-Synth
Figure 3. Distribution of sample counts across data source cate-                   Figure 4. Performance of different methods on PolyIneqBench
gories in PolyIneq-Real.                                                           (PolyIneq-Real and PolyIneq-Synth).



2014; Tung, 2012; Riasat, 2008; Manfrino et al., 2010; Mil-                        ina Prover (Wang et al., 2025). We also consider recent
dorf, 2005; Parvardi, 2011; Tung & Zhe, 2014; Lee, 2005;                           general-purpose LLMs, including GPT-5.2, Gemini-3-Pro,
Andreescu, 2019), forming PolyIneq-Real. Fig. 3 shows                              and DeepSeek-V3.2 (DeepSeek-AI, 2025), as well as the hy-
the distribution of data sources for PolyIneq-Real. Notably,                       brid system LIPS (Li et al., 2025a). We evaluate all methods
existing competition problems are largely concentrated in                          on PolyIneqBench using proof success rate and the average
the 3 or 4-variable setting. To extend the benchmark to                            runtime of successful proofs, and further examine perfor-
more challenging high-dimensional cases, we synthesize                             mance trends as the polynomial degree increases to assess
problems with 4 to 10 variables to build PolyIneq-Synth.                           scalability. Appendix G provides additional implementation
Appendix G.3 provides further details on PolyIneqBench.                            details and experimental configurations.

5.2. Experimental Setup                                                            5.3. Main Results
We compare our method NSPI with several state-of-the-                              Best performance under multivariate scenarios. Table 1
art inequality-proving approaches. Symbolic computa-                               presents the comparative performance of various baseline
tion–based baselines include Maple (Heck & Koepf, 1993)                            methods on the PolyIneqBench across different numbers
and Z3 (De Moura & Bjørner, 2008). State-of-the-art LLM-                           of variables n. As illustrated, a general downward trend
based provers include DeepSeek-Prover-V2 (Ren et al.,                              in pass rates is observed for all methods as the problem di-
2025), Goedel-Prover-V2 (Lin et al., 2025a), and Kim-                              mensionality increases. Overall, the proposed NSPI frame-

                                                                               7
           From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

             Success Rate Heatmap (3 10 vars)          100                                     Overall Success                                          Scalability Trend with Curriculum Groups
                                                                                                                   29.3%                           Curriculum: 3 5 vars Curriculum: 6 8 vars CL: 9 10 vars
Base 28.6% 20.8% 13.3% 11.5% 11.7% 16.7% 11.7% 6.7%                            30.0                        28.7%                              50
                                                                                                 27.6%                                                                               SFT
                                                       80                      27.525.3%
                                                                                                                                              40                                     RL Stage 1 (3 5 vars)
 SFT 40.5% 36.4% 31.7% 27.9% 20.0% 16.7% 11.7% 8.3%




                                                            Success Rate (%)
                                                            Success Rate (%)




                                                                                                                           Success Rate (%)
                                                                               25.0                                                                                                  RL Stage 2 (6 8 vars)
                                                       60                                                                                                                            RL Stage 3 (9 10 vars)
                                                                               22.5                                                           30
RL-1 44.0% 39.0% 36.7% 29.5% 21.7% 16.7% 13.3% 10.0%
                                                       40                      20.0                                                           20
RL-2 44.0% 40.3% 36.7% 29.5% 26.7% 18.3% 15.0% 10.0%                           17.5
                                                       20                             Base model (15.9%)                                      10
RL-3 44.0% 40.3% 36.7% 29.5% 26.7% 21.7% 15.0% 11.7%                           15.0 RL-1:  3 5 vars
                                                                                     RL-2: 6 8 vars
                                                                                     RL-3: 9 10 vars
                                                       0                       12.5                                                            0
       3     4     5     6     7     8     9    10                                  SFT           RL-1     RL-2    RL-3                            3      4       5      6       7       8        9           10
                        #Variables                                                                                                                                      #Variables

Figure 5. Performance on PolyIneqBench across different training stages. Left: Success rate heatmap showing capability boundary
migration. Middle: Overall performance gains from base model through RL stages. Right: Scalability trends across curriculum groups.


work outperforms symbol-based methods, pure LLM-based                                                 right panel of Fig. 5 highlights “jump-like” performance
approaches, and other hybrid systems, achieving best per-                                             improvements at the curriculum boundary points for differ-
formance. Notably, while baseline methods struggle as the                                             ent data groups. Moreover, training on specific curriculum
variable count scales to n = 10, NSPI maintains a consis-                                             groups yields cross-group generalization, partially enhanc-
tent pass rate of 11.7%. Our analysis further reveals several                                         ing performance on out-of-distribution instances. Overall,
key insights: (1) symbolic methods, though proficient in                                              large-scale supervised fine-tuning (SFT) in the cold-start
low-dimensional settings, suffer from exponential computa-                                            phase establishes a strong performance foundation (middle
tional complexity as dimensionality increases and lack the                                            panel), upon which progressive RL provides additional gains
ability to generate human-readable formal proofs; (2) state-                                          by extending generalization to more challenging, higher-
of-the-art (SOTA) LLM-based provers encounter significant                                             dimensional instances.
performance bottlenecks when tackling competition-level
polynomial inequalities exceeding 5 variables; and (3) al-                                            5.4. Ablation Studies
though general-purpose LLMs like Gemini-3-Pro exhibit
commendable scalability in certain cases, their overall per-                                          To validate the effectiveness of the individual components of
formance remains inferior to NSPI.                                                                    NSPI, we conduct ablation studies on PolyIneqBench under
                                                                                                      three settings: (1) removing the synthetic SOS cold start
                                                                                                      and applying RL directly to the base model; (2) removing
Challenging synthetic data (PolyIneq-Real vs. PolyIneq-
                                                                                                      progressive RL; and (3) disabling curriculum-based data
Synth). We compare the performance of various LLM-
                                                                                                      partitioning during RL. The results in Table 2 show that the
assisted methods on PolyIneq-Real and PolyIneq-Synth.
                                                                                                      cold-start stage trained on large-scale synthetic data is cru-
Fig. 4 shows a marked decrease in both pass rates and
                                                                                                      cial for SOS conjecturing performance, and that curriculum-
computational efficiency (running time) observed across
                                                                                                      based GRPO further improves the overall results.
all methods when tested on synthetic data, validating that
the synthesized high-dimensional instances represent more                                             Table 2. Ablation study of NSPI components. PI-Real and PI-
challenging reasoning scenarios. Under the more rigorous                                              Synth denote PolyIneq-Real and PolyIneq-Synth, respectively.
PolyIneq-Synth benchmark, NSPI achieves a 25.95% pass
rate while maintaining the minimum average execution time,                                                  SOS Data       GRPO                          CL           PI-Real        PI-Synth
thereby underscoring its superior efficacy and robustness.                                                  ✗                      ✓                       ✓          34.31%          14.76%
Notably, NSPI delivers a 2.87-fold improvement in pass                                                      ✓                      ✗                       ✗          40.20%          21.19%
rate over the hybrid LIPS system. In terms of computational                                                 ✓                      ✓                       ✗          42.16%          24.29%
throughput, NSPI consistently outperforms its counterparts                                                  ✓                      ✓                       ✓          43.14%          25.95%
by maintaining the lowest latency across both benchmarks,
yielding a remarkable speedup exceeding 10x compared to
several state-of-the-art LLM-based provers.
                                                                                                      6. Conclusion
Effectiveness of the progressive training process. Fig. 5                                             In this paper, we presented NSPI, a neuro-symbolic frame-
illustrates the performance of the SOS Structure Conjec-                                              work for automated polynomial-inequality proving that com-
turer across successive training stages on PolyIneqBench.                                             bines the complementary strengths of large language models
As illustrated by the color transitions in the left panel of                                          and symbolic computation to provide an end-to-end pipeline
Fig. 5, progressive reinforcement learning (RL) facilitates                                           from conjecture to certified proof. NSPI leverages an LLM
the migration of the model’s capability boundaries to-                                                to propose approximate Sum-Of-Squares (SOS) decomposi-
ward higher-dimensional polynomials. Furthermore, the                                                 tions, and refines them via symbolic computation into exact

                                                                                                 8
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

SOS representations that directly prove the target inequali-        Chen, L., Gu, J., Huang, L., Huang, W., Jiang, Z., Jie,
ties; we then machine-check these proofs in Lean. Extensive           A., Jin, X., Jin, X., Li, C., Ma, K., Ren, C., Shen, J.,
experiments on challenging benchmarks with polynomials                Shi, W., Sun, T., Sun, H., Wang, J., Wang, S., Wang,
of up to 10 variables show that NSPI consistently improves            Z., Wei, C., Wei, S., Wu, Y., Wu, Y., Xia, Y., Xin, H.,
the success rate and efficiency over competitive baseline             Yang, F., Ying, H., Yuan, H., Yuan, Z., Zhan, T., Zhang,
methods, substantially broadening the practical scope of              C., Zhang, Y., Zhang, G., Zhao, T., Zhao, J., Zhou, Y.,
automated polynomial-inequality proving.                              and Zhu, T. H. Seed-prover: Deep and broad reasoning
                                                                      for automated theorem proving, 2025b. URL https:
Acknowledgements                                                      //arxiv.org/abs/2507.23726.

This work was supported in part by the National Key Re-             Chervonyi, Y., Trinh, T. H., Olšák, M., Yang, X., Nguyen,
search and Development Program of China under Grant                   H. H., Menegali, M., Jung, J., Kim, J., Verma, V., Le,
2023YFA1009402, the Strategic Priority Research Program               Q. V., et al. Gold-medalist performance in solving
of Chinese Academy of Sciences under Grant XDA0480501,                olympiad geometry with alphageometry2. Journal of
and the Natural Science Foundation of Hunan Province un-              Machine Learning Research, 26(241):1–39, 2025.
der Grant 2026JJ70102.
                                                                    De Moura, L. and Bjørner, N. Z3: An efficient smt solver.
                                                                      In International conference on Tools and Algorithms for
Impact Statement                                                      the Construction and Analysis of Systems, pp. 337–340.
This paper presents work whose goal is to the field of Ma-            Springer, 2008.
chine Learning. The development of our approach holds
potential for significant impact within the domains of formal       De Moura, L., Kong, S., Avigad, J., Van Doorn, F., and von
verification and automated polynomial inequality proving.             Raumer, J. The lean theorem prover (system description).
While there are various potential societal consequences of            In International Conference on Automated Deduction, pp.
this work, none which we feel must be specifically high-              378–388. Springer, 2015.
lighted here.
                                                                    DeepSeek-AI. Deepseek-v3.2: Pushing the frontier of open
                                                                      large language models, 2025.
References
Ahmadi, A. A. and Majumdar, A. Dsos and sdsos opti-                 El Din, M. S. Computing the global optimum of a mul-
  mization: more tractable alternatives to sum of squares             tivariate polynomial over the reals. In Proceedings of
  and semidefinite optimization. SIAM Journal on Applied              the twenty-first international symposium on Symbolic and
 Algebra and Geometry, 3(2):193–230, 2019.                            algebraic computation, pp. 71–78, 2008.

Andreescu, T. 118 Inequalities for Mathematics Competi-             Gerschgorin, S. Uber die abgrenzung der eigenwerte einer
  tions. XYZ Press, Plano, TX, 2019.                                  matrix. Izvestija Akademii Nauk SSSR, Serija Matematika,
                                                                      7(3):749–754, 1931.
Azerbayev, Z., Piotrowski, B., Schoelkopf, H., Ayers, E. W.,
  Radev, D., and Avigad, J. Proofnet: Autoformalizing and           Golub, G. H. and Van Loan, C. F. Matrix computations.
  formally proving undergraduate-level mathematics, 2023.            JHU press, 2013.
Barker, G. and Carlson, D. Cones of diagonally dominant
                                                                    He, C., Luo, R., Bai, Y., Hu, S., Thai, Z., Shen, J., Hu, J.,
  matrices. Pacific Journal of Mathematics, 57(1):15–32,
                                                                      Han, X., Huang, Y., Zhang, Y., Liu, J., Qi, L., Liu, Z., and
  1975.
                                                                      Sun, M. OlympiadBench: A challenging benchmark for
Chen, E. A brief introduction to olympiad inequalities. URL:          promoting AGI with olympiad-level bilingual multimodal
  https://web.evanchen.cc/handouts/Ineq/en.pdf (accessed              scientific problems. In Ku, L.-W., Martins, A., and Sriku-
  20.03.2021), 2014.                                                  mar, V. (eds.), Proceedings of the 62nd Annual Meeting
                                                                      of the Association for Computational Linguistics (Volume
Chen, J., Chen, W., Du, J., Hu, J., Jiang, Z., Jie, A.,              1: Long Papers), pp. 3828–3850, Bangkok, Thailand,
  Jin, X., Jin, X., Li, C., Shi, W., Wang, Z., Wang, M.,              August 2024. Association for Computational Linguis-
  Wei, C., Wei, S., Xin, H., Yang, F., Gao, W., Yuan,                 tics. doi: 10.18653/v1/2024.acl-long.211. URL https:
  Z., Zhan, T., Zheng, Z., Zhou, T., and Zhu, T. H.                  //aclanthology.org/2024.acl-long.211/.
  Seed-prover 1.5: Mastering undergraduate-level theo-
  rem proving via learning from experience, 2025a. URL              Heck, A. and Koepf, W. Introduction to MAPLE, volume
  https://arxiv.org/abs/2512.17260.                                  1993. Springer, 1993.

                                                                9
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

Heule, M. J. H., Kullmann, O., and Marek, V. W. Solving                Lin, Y., Tang, S., Lyu, B., Wu, J., Lin, H., Yang, K., Li, J.,
  and verifying the boolean pythagorean triples problem                  Xia, M., Chen, D., Arora, S., et al. Goedel-prover: A fron-
  via cube-and-conquer. In Creignou, N. and Le Berre, D.                 tier model for open-source automated theorem proving.
  (eds.), Theory and Applications of Satisfiability Testing –            arXiv preprint arXiv:2502.07640, 2025a.
  SAT 2016, pp. 228–245, Cham, 2016. Springer Interna-
  tional Publishing. ISBN 978-3-319-40970-2.                           Lin, Y., Tang, S., Lyu, B., Yang, Z., Chung, J.-H., Zhao,
                                                                         H., Jiang, L., Geng, Y., Ge, J., Sun, J., et al. Goedel-
Kaltofen, E. L., Li, B., Yang, Z., and Zhi, L. Ex-                       prover-v2: Scaling formal theorem proving with scaf-
  act certification in global polynomial optimization                    folded data synthesis and self-correction. arXiv preprint
  via sums-of-squares of rational functions with                         arXiv:2508.03613, 2025b.
  rational coefficients.      Journal of Symbolic Com-
  putation, 47(1):1–15, 2012.           ISSN 0747-7171.                Magron, V., Din, M. S. E., and Vu, T.-H. Sum of squares
  doi:           https://doi.org/10.1016/j.jsc.2011.08.002.             decompositions of polynomials over their gradient ideals
  URL         https://www.sciencedirect.com/                            with rational coefficients. SIAM Journal on Optimization,
  science/article/pii/S0747717111001143.                                33(1):63–88, 2023.
                                                                       Manfrino, R. B., Ortega, J. A. G., and Delgado, R. V. In-
Lagarias, J. C. The computational complexity of simultane-
                                                                        equalities: a mathematical olympiad approach. Springer
  ous diophantine approximation problems. SIAM Journal
                                                                        Science & Business Media, 2010.
  on Computing, 14(1):196–209, 1985.
                                                                       Maréchal, A., Fouilhé, A., King, T., Monniaux, D., and
Lample, G., Lacroix, T., Lachaux, M.-A., Rodriguez, A.,
                                                                        Périn, M. Polyhedral approximation of multivariate poly-
  Hayat, A., Lavril, T., Ebner, G., and Martinet, X. Hyper-
                                                                        nomials using handelman’s theorem. In International
  tree proof search for neural theorem proving. Advances in
                                                                        Conference on Verification, Model Checking, and Ab-
  neural information processing systems, 35:26337–26349,
                                                                        stract Interpretation, pp. 166–184. Springer, 2015.
  2022.
                                                                       Martin-Dorel, É. and Roux, P. A reflexive tactic for polyno-
Langley, P. Crafting papers on machine learning. In Langley,
                                                                        mial positivity using numerical solvers and floating-point
  P. (ed.), Proceedings of the 17th International Conference
                                                                        computations. In Proceedings of the 6th ACM SIGPLAN
  on Machine Learning (ICML 2000), pp. 1207–1216, Stan-
                                                                        Conference on Certified Programs and Proofs, pp. 90–99,
  ford, CA, 2000. Morgan Kaufmann.
                                                                        2017.
Lasserre, J. B. Semidefinite programming vs. lp relaxations
                                                                       Meurer, A., Smith, C. P., Paprocki, M., Čertı́k, O., Kirpichev,
  for polynomial programming. Mathematics of operations
                                                                        S. B., Rocklin, M., Kumar, A., Ivanov, S., Moore, J. K.,
  research, 27(2):347–360, 2002.
                                                                        Singh, S., et al. Sympy: symbolic computing in python.
Le, H. and Van Barel, M. An algorithm for decomposing a                 PeerJ Computer Science, 3:e103, 2017.
  non-negative polynomial as a sum of squares of rational
                                                                       Mildorf, T. J.      Olympiad inequalities.   Preprint,
  functions. Numerical Algorithms, 69, 06 2014. doi:
                                                                        https://artofproblemsolving.   com/articles/files/Mil-
  10.1007/s11075-014-9903-3.
                                                                        dorfInequalities. pdf, 2005.
Lee, H. Topics in inequalities. Halen gelismekte olan kitabı
                                                                       Parrilo, P. Structured semidenite programs and semialge-
  bulmak için internetten arayınız, 2005.
                                                                         braic geometry methods in robustness and optimization.
Li, Z., Li, Z., Tang, W., Zhang, X., Yao, Y., Si, X., Yang, F.,          PhD thesis, 08 2000a.
  Yang, K., and Ma, X. Proving olympiad inequalities by
                                                                       Parrilo, P. A. Structured semidefinite programs and semial-
  synergizing LLMs and symbolic reasoning. In Interna-
                                                                         gebraic geometry methods in robustness and optimization.
  tional Conference on Learning Representations (ICLR),
                                                                         California Institute of Technology, 2000b.
  2025a.
                                                                       Parrilo, P. A. Semidefinite programming relaxations for
Li, Z., Liao, B., and Ye, Q. Ineqsearch: Hybrid reasoning for            semialgebraic problems. Mathematical programming, 96
   olympiad inequality proofs. In The Thirty-ninth Annual                (2):293–320, 2003.
  Conference on Neural Information Processing Systems,
   2025b.                                                              Parvardi, A. H. Problems proposed by vasc and arqady,
                                                                         2011.
Li, Z., Liao, B., and Ye, Q. Ineqsearch: Hybrid reasoning for
   olympiad inequality proofs. In The Thirty-ninth Annual              Paulson, L. C. Isabelle: The next 700 theorem provers. In
  Conference on Neural Information Processing Systems,                   Logic and computer science, volume 31, pp. 361–386,
   2025c.                                                                1990.

                                                                  10
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

Peyrl, H. and Parrilo, P. A. Computing sum of squares                Wang, H., Unsal, M., Lin, X., Baksys, M., Liu, J., Santos,
  decompositions with rational coefficients. Theoretical              M. D., Sung, F., Vinyes, M., Ying, Z., Zhu, Z., et al.
  Computer Science, 409(2):269–281, 2008a. ISSN 0304-                 Kimina-prover preview: Towards large formal reason-
  3975. doi: https://doi.org/10.1016/j.tcs.2008.09.025.               ing models with reinforcement learning. arXiv preprint
  URL        https://www.sciencedirect.com/                           arXiv:2504.11354, 2025.
  science/article/pii/S0304397508006452.
  Symbolic-Numerical Computations.                                   Wei, C., Sun, M., and Wang, W. Proving olympiad algebraic
                                                                      inequalities without human demonstrations. Advances
Peyrl, H. and Parrilo, P. A. Computing sum of squares                 in Neural Information Processing Systems, 37:82811–
  decompositions with rational coefficients. Theor. Com-              82822, 2024.
  put. Sci., 409:269–281, 2008b. URL https://api.
  semanticscholar.org/CorpusID:2370460.                              Xin, R., Xi, C., Yang, J., Chen, F., Wu, H., Xiao, X., Sun, Y.,
                                                                       Zheng, S., and Ding, M. Bfs-prover: Scalable best-first
Polu, S. and Sutskever, I. Generative language model-                  tree search for llm-based automatic theorem proving. In
  ing for automated theorem proving. arXiv preprint                    Proceedings of the 63rd Annual Meeting of the Associ-
  arXiv:2009.03393, 2020.                                              ation for Computational Linguistics (Volume 1: Long
Ren, Z., Shao, Z., Song, J., Xin, H., Wang, H., Zhao, W.,              Papers), pp. 32588–32599, 2025.
  Zhang, L., Fu, Z., Zhu, Q., Yang, D., et al. Deepseek-             Yang, L. Recent advances in automated theorem prov-
  prover-v2: Advancing formal mathematical reasoning via               ing on inequalities. J. Comput. Sci. Technol., 14(5):
  reinforcement learning for subgoal decomposition. arXiv              434–446, September 1999. ISSN 1000-9000. doi:
  preprint arXiv:2504.21801, 2025.                                     10.1007/BF02948785. URL https://doi.org/10.
Riasat, S. Basics of olympiad inequalities. Preprint, 20:              1007/BF02948785.
  80–90, 2008.                                                       Yang, Z., Zhao, H., and Zhi, L. Verifyrealroots: A matlab
Shao, Z., Wang, P., Zhu, Q., Xu, R., Song, J., Bi, X., Zhang,          package for computing verified real solutions of poly-
  H., Zhang, M., Li, Y., Wu, Y., et al. Deepseekmath: Push-            nomials systems of equations and inequalities. Jour-
  ing the limits of mathematical reasoning in open language            nal of Systems Science and Complexity, 02 2023. doi:
  models. arXiv preprint arXiv:2402.03300, 2024.                       10.1007/s11424-023-1406-7.

Team, Q. Qwen3 technical report, 2025. URL https:                    Zheng, K., Han, J. M., and Polu, S. Minif2f: a cross-system
  //arxiv.org/abs/2505.09388.                                          benchmark for formal olympiad-level mathematics. arXiv
                                                                       preprint arXiv:2109.00110, 2021.
Trinh, T. H., Wu, Y., Le, Q. V., He, H., and Luong, T. Solv-
  ing olympiad geometry without human demonstrations.
  Nature, 625(7995):476–482, 2024.
Tsoukalas, G., Lee, J., Jennings, J., Xin, J., Ding, M., Jen-
  nings, M., Thakur, A., and Chaudhuri, S. Putnambench:
  evaluating neural theorem-provers on the putnam math-
  ematical competition. In Proceedings of the 38th Inter-
  national Conference on Neural Information Processing
  Systems, NIPS ’24, Red Hook, NY, USA, 2024. Curran
  Associates Inc. ISBN 9798331314385.
Tung, N. D.    567 nice and hard inequality.
  https://phamtuankhai.wordpress.
  com/wp-content/uploads/2012/04/
  567-bat-dang-thuc-hay.pdf, 2012.
Tung, N. D. and Zhe, Z. Y. The interesting around technical
  analysis: Three variable inequalities, 2014.
Uray, M. On proving inequalities by cylindrical algebraic
  decomposition. Annales Universitatis Scientiarum Bu-
  dapestinensis de Rolando Eötvös Nominatae. Sectio com-
  putatorica, pp. 231–252, 01 2020. doi: 10.71352/ac.51.
  231.

                                                                11
        From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

A. Sum of Squares and Semidefinite Programming
We introduce the relationship between sum-of-squares (SOS) polynomials and semidefinite programming (SDP), which
provides the theoretical foundation for the methods employed in this study.
A polynomial f (x) ∈ R[x] is called a sum-of-squares (SOS) polynomial if it can be expressed as
                                               X
                                       f (x) =    fi (x)2 , where fi (x) ∈ R[x].                                          (13)
                                                        i

Example 1. Consider the  polynomial    f (x) = 2x41 + 2x31 x2 − x21 x22 + 5x42 , x = (x1 , x2 ) ∈ R2 . Define f1 (x) =
 1                                   1
√
  2
    2x1 − 3x2 + x1 x2 , f2 (x) = √2 x22 + 3x1 x2 . Then f (x) admits the SOS decomposition f (x) = f1 (x)2 + f2 (x)2 ,
       2      2

which implies that f (x) ≥ 0 for all x ∈ R2 .
Semidefinite programming (SDP) is a class of convex optimization problems, whose standard form can be expressed as

                                              minimize      ⟨C, G⟩
                                             subject to     ⟨Ai , G⟩ = bi ,   i = 1, . . . , m,                           (14)
                                                            G ⪰ 0,

where G is a symmetric matrix variable and G ⪰ 0 denotes that G is positive semidefinite. ⟨A, G⟩ = tr(A⊤ G) denotes the
matrix inner product.
Theorem A.1. (Parrilo, 2000b) A multivariate polynomial f (x) in n variables and of degree 2d is a sum of squares (SOS)
if and only if there exists a symmetric positive semidefinite (PSD) matrix G
                                                                           e such that

                                                          f (x) = v(x)⊤ Gv(x),
                                                                        e                                                 (15)

where v(x) = [1, x1 , x2 , ..., xn , x21 , x1 x2 , ..., xdn ] is the vector of monomials up to degree d.

The matrix Ge is referred to as a Gram matrix of f (x) with respect to the monomial basis v(x).
Remark A.2. The Gram matrix representation is generally not unique, as different choices of the monomial basis or
orthogonal transformations of the SOS components yield different PSD matrices G.
According to Theorem A.1, expanding the right-hand side of equation Equation (15) and matching the coefficients with those
of f (x) yields a system of linear equality constraints on the entries of the Gram matrix G. Consequently, the problem of
finding an SOS decomposition of the polynomial can be equivalently reformulated as the SDP problem given in Equation (4)
of Section 3.
Example 2. (Parrilo, 2003) Consider the bivariate quartic polynomial f (x) = 2x41 + 2x31 x2 − x21 x22 + 5x42 , x = (x1 , x2 ) ∈
R2 . Let the monomial basis vector be v(x) = [x21 , x22 , x1 x2 ]⊤ . Then f (x) can be written in Gram form as

                             f (x) = v(x)⊤ G v(x)
                                      2 ⊤                            2 
                                       x1      q11           q12   q13     x1
                                   =  x22  q12            q22   q23   x22 
                                      x1 x2    q13           q23   q33    x1 x2
                                     = q11 x41 + q22 x42 + (q33 + 2q12 )x21 x22 + 2q13 x31 x2 + 2q23 x1 x32 .             (16)

Matching coefficients with the target polynomial f (x) yields the following linear equalities:

                          q11 = 2,        q22 = 5,          q33 + 2q12 = −1,         2q13 = 2,       2q23 = 0.            (17)

A positive semidefinite matrix G ⪰ 0 satisfying (17) can be obtained, e.g., via semidefinite programming. One feasible
choice is                                       
                                       2 −3 1                                         
                                                                        1 2 −3 1
                               G = −3 5 0 = L⊤ L,              L= √                    .
                                       1    0 5                          2 0 1 3
                                                                                         2                2
Consequently, f (x) admits the explicit SOS decomposition f (x) = 12 2x21 − 3x22 + x1 x2 + 12 x22 + 3x1 x2 .

                                                                     12
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

B. Theoretical Foundations of SOS Data Construction
This part provides the formal theoretical guarantees for the data construction methods described in Section 4.1.1. We focus
on the spectral properties and decomposition theorems that ensure the generated Gram matrices G e are positive semidefinite.

                                                  construction

                                        Computation-Driven Methods
                                                                                   genaration
                                       Explicit Algebraic Construction


                                       Optimization-Based Approach
                                                                           Polynomial-SOS Pairs

                                          Structure-Driven Methods



Figure 6. Framework of SOS data construction methods in Section 4.1.1. The generation of polynomial-SOS pairs is based on the
quadratic form f (x) = v(x)T Gv(x),
                             e      where the Gram matrix G
                                                          e is synthesized through either computation-driven or structure-driven
approaches.



B.1. Spectral Foundations for Computation-Driven Methods
The computation-driven methods rely on the relationship between eigenvalues and the PSD property.
Lemma B.1 (Eigenvalue Shift). Let G ∈ Sm be a symmetric matrix with real entries. For any k ∈ R, the eigenvalues of
e = G − kI are given by λi (G)
G                           e = λi (G) − k. Consequently, selecting k ≤ λmin (G) is a sufficient condition to ensure
G ⪰ 0.
e

To generate Gram matrices with controlled sparsity and coefficient types, we employ a constructive approach based on
quadratic forms.
Lemma B.2. Let L ∈ Zk×m be an arbitrary matrix (representing the coefficients of k basis polynomials) and D =
diag(d1 , . . . , dk ) be a diagonal matrix with di > 0. The resulting matrix
                                                            e = L⊤ DL
                                                            G                                                              (18)
                                            e ⪰ 0).
is guaranteed to be positive semi-definite (G

B.2. Diagonally Dominant (dd) and Scaled Diagonally Dominant (sdd) Cones
Structure-driven methods restrict the search space to specific sub-cones of the PSD cone to simplify formal verification.
Definition B.3. (Ahmadi & Majumdar, 2019) A matrix G ∈ Rm×m is defined as diagonally dominant (dd) if it satisfies the
following condition:
                                                    X
                                             Gii ≥     |Gij |, ∀i.                                                (19)
                                                                 j̸=i

A symmetric matrix G is called scaled diagonally dominant (sdd) if there exists a diagonal matrix D with strictly positive
diagonal elements such that the matrix DGD is diagonally dominant.

According to Gershgorin’s circle theorem (Gerschgorin, 1931), any symmetric diagonally dominant matrix with non-negative
diagonal entries is positive semi-definite.
The following lemma provides the theoretical justification for the extreme ray decomposition used in our framework:
Lemma B.4. (Barker & Carlson, 1975)The cone of m × m symmetric dd matrices is the set of all matrices that can be
represented as:
                                               m2
                                               X
                                          G
                                          e=      ηi Ui , ηi ≥ 0                                             (20)
                                                            i=1

                                                                     13
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

where each Ui = ui u⊤                                  m
                      i is a rank-one matrix and ui ∈ R is a vector with at most two non-zero components, each belonging
to {±1}, that is, ui ∈ {±ek : k ∈ [m]} ∪ {±ek ± eℓ : 1 ≤ k < ℓ ≤ m}.

For the construction of scaled diagonally dominant (sdd) matrices, we utilize the properties of diagonal congruence
transformation:
Lemma B.5. A matrix G is sdd if there exists a positive definite diagonal matrix D ≻ 0 such that DGD is dd. By Sylvester’s
Law of Inertia, diagonal congruence transformations preserve the inertia of a matrix and, in particular, the signs of its
eigenvalues. Since DGD is dd, it follows that DGD ⪰ 0. Consequently, G = D−1 (DGD)D−1 ⪰ 0.
                                           Pm2                                                         e = D−1 GD−1
Since G is dd, it admits the decomposition i=1 ηi Ui . Applying the diagonal congruence transformation G
yields the sdd matrix G
                      e as a non-negative linear combination of scaled rank-one matrices:

                                                                 2
                                                              m
                                                              X
                                                       G
                                                       e=            ηi U
                                                                        bi ,                                            (21)
                                                              i=1

      bi := D−1 Ui D−1 = wi w⊤ and wi := D−1 ui . Each vector wi still has at most two nonzero components, whose
where U                         i
magnitudes are determined by the diagonal entries of D−1 .

C. Further Details of Symbolic Correction Module
This section presents the theoretical foundations of the symbolic correction module described in Section 4.2. The purpose
of this module is to convert the SOS structural conjecture obtained from the SOS conjecture stage into an exact rational
sum-of-squares certificate, ensuring suitability for formal verification.

C.1. Gauss-Newton Refinement for SOS
Suppose a polynomial f (x) ∈ R[x] of degree 2d is conjectured to admit a sum-of-squares (SOS) decomposition. Let v(x)
denote the monomial basis consisting of all monomials of degree at most d. The SOS condition is equivalently expressed in
Gram matrix form as f (x) = v(x)⊤ Gv(x), where G ⪰ 0 is a symmetric positive semidefinite Gram matrix. In practice,
numerical solvers only provide an approximate Gram matrix G, such that f (x) ≈ v(x)⊤ Gv(x).
To reduce numerical errors and improve stability prior to exact rational recovery, we apply a structure-preserving
Gauss–Newton refinement.

C.1.1. N UMERICAL N EWTON R EFINEMENT OF AN A PPROXIMATE G RAM M ATRIX
Factorization-based parameterization.       Assume G ⪰ 0 numerically and compute a factorization

                                                        G ≈ LL⊤ ,                                                       (22)

where L ∈ Rm×k and k = rank(G). Then
                                                     k
                                                     X                               X
                                   v(x)⊤ G v(x) ≈          ℓi (x)2 ,     ℓi (x) :=       ci,α xα .                      (23)
                                                     i=1                             α


                                                                                                              2
                                                                                                     P
We refine the coefficient vectors L:,i via a Gauss–Newton update so that the induced polynomial       i ℓi (x) matches f (x)
as accurately as possible.
Proposition C.1. By applying a Cholesky factorization G = LL⊤ or an LDL⊤ decomposition to the Gram matrix G, and
treating the coefficients of the SOS factors as optimization variables, the Gauss–Newton iteration exhibits rapid convergence
when applied to SOS problems. Provided that sufficient numerical precision is employed, the backward error θ can be
reduced to arbitrarily small values.

This yields a high-accuracy numerical approximation, which serves as a reliable foundation for the subsequent rational
recovery procedure.

                                                               14
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

Residual and stopping criterion.     Let coeff(·) denote the coefficient vector of a polynomial in the chosen monomial basis.
Define the residual
                                                 k
                                                                              !
                                                 X
                                                               2
                                 r(L) := coeff         ℓi (x) − f (x) ,                    θ := ∥r(L)∥2 .                (24)
                                                 i=1


Here, θ denotes the backward error of the numerical Gram matrix G. We apply the Gauss–Newton iteration to compute the
coefficient correction terms ∆ci,α so as to minimize θ, as described in Equation (11) of Section 4.2.
Simultaneously, the Gram matrix is updated according to G ← G + ∆G, where the correction term ∆G can be expressed as

                                         k
                                                                   !2
                                         X X
                                                     ∆ci,α x   α
                                                                        = v(x)⊤ ∆G v(x).
                                         i=1     α


The iteration terminates once θ < τ for a prescribed tolerance τ > 0.

C.2. Detailed Formulation of Exact Rational Recovery
The following proposition establishes the fundamental equivalence between the existence of a rational sum-of-squares (SOS)
decomposition and the existence of a Gram matrix with rational entries.
Proposition C.2. (Peyrl & Parrilo, 2008a) Let f (x) ∈ Q[x] be a polynomial, and let v(x) denote a fixed vector of
monomials. Then the following statements are equivalent:

 1. The polynomial f (x) admits a rational SOS decomposition, that is, there exist polynomials fi (x) ∈ Q[x] such that
                                                                        r
                                                                        X
                                                        f (x) =               fi (x)2 .
                                                                        i=1


 2. There exists a symmetric positive semidefinite Gram matrix G ∈ Sm ∩ Qm×m such that

                                               f (x) = v(x)⊤ G v(x),                      G ⪰ 0.

For the numerical solution GN obtained after the Gauss–Newton refinement, when the backward error θ is sufficiently small,
one can recover from GN an exact rational PSD matrix G,    e which satisfies the polynomial identity exactly, thereby yielding
a certified rational SOS certificate. Which satisfies the following identity:


                                          f (x) − v(x)⊤ Gv(x)
                                                        e     = 0,                        e ⪰ 0.
                                                                                          G                              (25)

The matrix G is projected onto the following affine hyperplane:

                                    X = G G⊤ = G, f (x) − v(x)⊤ G v(x) = 0
                                       
                                                                                                     .                   (26)

Suppose that the affine hyperplane defined by Equation (26) can be represented by a linear system Ay = b, where y consist
of the entries of G. If the matrix A has full row rank, then such a hyperplane is guaranteed to exist.
The recovery strategy depends on whether the refined Gram matrix lies in the interior of the PSD cone.
An exact solution satisfying Equation (25) can be obtained via the following two approaches:

  • Case 1: If the matrix GN is of full rank, the solution is recovered by applying an orthogonal projection method.

  • Case 2: Otherwise, a rational vector recovery method is employed.

                                                                   15
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

Case 1: Interior Point Solution (GN is full rank). The solution of Equation (25) lies in the intersection of the affine
hyperplane X and the positive semidefinite cone. To compute G,
                                                            e the corresponding orthogonal projection can be obtained
by solving the following least-squares problem.


                                       min ∥GN − G∥2F         s.t. f (x) = v(x)⊤ G v(x).                                      (27)
                                       G⪰0


Next, to verify whether the recovered rational solution G
                                                        e is a symmetric positive semidefinite matrix, we compute the exact
LDL⊤ decomposition of G.   e


                                         f (x) = v(x)⊤ Gv(x)
                                                       e     = v(x)⊤ LDL⊤ v(x)                                                (28)
Theorem C.3. Let GN be the refined numerical solution whose backward error satisfies θ < τ , and let Ay = b be the
linear system associated with the affine hyperplane defined by Equation (26). Suppose that G
                                                                                           e is the optimal rational solution
of the least-squares Equation (27), and that the matrix A has full row rank. If the minimal eigenvalue λ of Ge satisfies

                                                     λ > ∥GN ∥2F κ22 (A)τ 2 ,                                                 (29)

then G
     e is an exact solution of Equation (25).

             e is a solution of Problem (27), it clearly satisfies the polynomial identity f (x) = v(x)⊤ Gv(x).
Proof. Since G                                                                                           e      Let yN and ye
denote the vectors consisting of the entries of GN and G, respectively. From (26), and under the assumption that the matrix
                                                          e
A has full row rank, we have
                                             ∥AyN − b∥22 = θ < τ,          Aey = b.                                     (30)
According to the perturbation result (Golub & Van Loan, 2013) for full-row-rank underdetermined linear systems, the
following estimate holds:
                                       ∥yN − ye∥2 ≤ (κ2 (A)τ )∥yN ∥2 + O(τ 2 ).                                (31)
Under the assumption that λ > ∥GN ∥2F κ22 (A)τ 2 , it follows that
                                                      e 2F ≤ ∥yN − ye∥22 < λ
                                                ∥GN − G∥                                                                      (32)
where the inequality ∥yN − ye∥22 < λ holds because the higher-order term O(τ 2 ) is negligible when τ is sufficiently small.
Let λ
    e denote an eigenvalue of G.
                              e By the Wielandt–Hoffman theorem (Golub & Van Loan, 2013), we obtain

                                                 |λ              e 2 ≤ λ,
                                                  e − λ| ≤ ∥GN − G∥                                                           (33)
                                                                   F

which implies that all eigenvalues of G                                              e ⪰ 0.
                                      e are nonnegative. Therefore, we conclude that G

Case 2: Boundary Solution (GN is rank-deficient). When the numerical Gram matrix GN obtained via Gauss–Newton
refinement is rank-deficient or ill-conditioned (near-singular), the affine hyperplane X defined by the linear constraints is
typically tangent to the boundary of the positive semidefinite (PSD) cone. In such instances, GN does not reside within
the interior of the PSD cone; consequently, direct orthogonal projection may yield a rational matrix G    e that violates the
semi-definiteness requirement. We provides a rigorous discussion on the structural origins of such cases and presents a
theoretical framework for exact recovery based on rational vector reconstruction.

   • Redundant Monomials: In the construction of the SOS decomposition, a monomial basis that is not strictly necessary
     may be used. This situation can be avoided by exploring the sparse structure of the polynomial or by removing entire
     rows and columns of the Gram matrix GN that correspond to numerically small entries, i.e., eliminating the monomials
     that should not appear in the polynomial’s SOS representation.
   • Intrinsic Singularity: If the polynomial f (x) attains its global minimum at a nonzero real point (ξ1 , . . . , ξn ), then the
     monomial vector v(ξ) at this point is a zero vector in the Gram matrix GN , implying that GN is singular. When the
     global minimum is attained only at finitely many nonzero points, and the backward error θ is sufficiently small, the
     Gram matrix can be rendered full rank by performing Gauss–Newton refinement, after which an orthogonal projection
     can be applied. In contrast, when the global minimum is attained on some manifolds, we apply the Gauss–Newton
     iteration to a truncated triangular decomposition of GN . Once the residual is sufficiently small, a rational recovery of
     GN is carried out via a simultaneous Diophantine approximation algorithm (Lagarias, 1985).

                                                                16
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

D. Neural Conjectur Midule Configuration
D.1. Prompt Template
Here we present the prompt template employed by the SOS structure conjecture module in the neural conjecture module.
For a given nonnegative polynomial, the SOS structure conjecturer generates a candidate SOS structural conjecture based
on an expanded-form representation, with the objective that the proposed SOS structure matches the target polynomial as
closely as possible.

  Prompt Template for SOS Structure Conjecturer
  Task:
  You are given a polynomial that is the expanded form of a sum-of-squares (SOS) expression. Your task is to reconstruct
  a plausible SOS representation whose expanded form matches the given polynomial as closely as possible.
  Instructions:
  1. Analyze the input polynomial carefully, focusing on the coefficients and the combinations of variables involved.
  2. Infer possible linear or polynomial terms inside each square in the sum-of-squares expression.
  3. Construct a sum of square terms without expanding the squares. Keep the output compact and well-structured.
  4. Aim for the expanded form of your SOS expression to closely approximate the coefficients in the original polynomial.
  Minor numerical deviations are acceptable.
  5. If multiple valid SOS decompositions exist, prefer one that is simple, symmetric, and easy to interpret.
  6. Include variables and constants inside parentheses when appropriate to match constant terms in the input polynomial.


  Output format:
  Please provide your response in the following structure:
  <SOS Expression>: <sum of squares expression>
  Where <sum of squares expression> is a sum-of-squares term, expressed compactly.
  For example:
  (x1 + 1)ˆ2 + (2*x1 + 3*x2)ˆ2
  Key considerations:
  1. Do not simply rewrite the input polynomial or output expanded terms. The output must be a sum-of-squares
  expression.
  2. Constants inside square terms can be fractional or decimal, as needed, to best approximate the original polynomial.
  3. Avoid expanding the squares in the output; always keep terms inside parentheses squared.
  4. Aim for clear and interpretable variable groupings. Symmetry and simplicity are preferred if multiple answers fit.
  5. Your SOS expression should fully explain the input polynomial’s structure and coefficients to the best achievable
  extent.

  Example:
  Input polynomial:
  x1ˆ2 + 2*x1 + 1
  Output:
  (SOS Expression): (x1 + 1)ˆ2
  Explanation:
  The polynomial is a perfect square trinomial; the SOS reconstruction is exact.
  Input polynomial:
  5*x1ˆ2 + 12*x1*x2 + 6*x1 + 9*x2ˆ2 + 9
  Output:
  (SOS Expression): (x1 + 2.99)ˆ2 + (2*x1 + 3*x2)ˆ2
  Now, please provide the SOS reconstruction for the following polynomial:
  Original polynomial: {polynomial}

As illustrated by the prompt template above, it consists of a task description, multiple explicit instructions specifying the

                                                             17
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

required output format and content constraints for the large language model, and several illustrative examples provided to
guide the generation process.

D.2. Synthetic Dataset Statistics
During the data construction stage of the neural conjecture module, we generate more than 100w synthetic data instances
using the four data generation strategies proposed in Section 4.1.1, including both computation-driven and structure-
driven approaches. These synthetic datasets, covering problems with varying numbers of variables ranging from 3 to 10, are
used as the training corpus for the neural conjecturer.
Notably, we performed a manual quality inspection of the synthesized polynomial–SOS pair data via random sampling.
For each variable setting from 3 to 10, we randomly sampled 50 instances for review. The inspection results indicate that the
synthesized data contain no formatting errors and encompass polynomial SOS decomposition cases of varying difficulty,
including a substantial proportion of highly non-trivial instances that pose significant challenges to conventional symbolic
solvers. Additionally, we computed the degree and number of SOS terms of the synthesized data. The statistical results are
reported in Fig. 7 and Fig. 8.

                                                                 Polynomial Degree Distribution
                               400000

                               350000

                               300000
                   Frequency




                               250000

                               200000

                               150000

                               100000

                               50000

                                   0
                                            2      4       6      8      10        12    14     16      18     20      22
                                                                               Degree
                                        Figure 7. Statistical distribution of degrees for synthetic polynomial data.

As illustrated in Fig. 7 and Fig. 8, the synthetic dataset exhibits significant diversity in both algebraic complexity and
representation structure. Specifically, the degrees of the synthesized polynomials span a wide range from 2 to 22, ensuring
the model is exposed to problems of varying algebraic depths; this reflects that the synthetic data encompasses both relatively
simple low-degree polynomials and structurally sophisticated high-degree instances. Furthermore, the distribution of SOS
term counts covers a spectrum ranging from basic single-term squares to complex decomposition instances involving up to
15 terms. Such structural diversity indicates that our construction strategies effectively cover a broad difficulty spectrum,
preventing the model from over-fitting to specific sparse or low-degree patterns.

D.3. Additional Details of Progressive Reinforcement Learning Process
For the progressive two-stage training procedure of the SOS-structure conjecturer described in Section 4.1.2, in the second
stage we employ a curriculum-style GRPO reinforcement learning process. Here, we provide the theoretical foundations
and several implementation details.

Group Relative Policy Optimization (GRPO). Group Relative Policy Optimization (GRPO) (Shao et al., 2024) is a
reinforcement learning algorithm used for fine-tuning large language models (LLMs). Unlike the popular Proximal Policy
Optimization (PPO), GRPO enhances efficiency by eliminating the need for a separate value function. It estimates the
advantage by normalizing the rewards of a set of responses to the same prompt. Specifically, for each question q in a given
set Q, a set of responses {o1 , . . . , oG } is sampled from the old policy πold . The reward model then evaluates these responses,

                                                                              18
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

                                                                       Distribution of SOS Term Counts
                                140000

                                120000

                    Frequency   100000

                                80000

                                60000

                                40000

                                20000

                                    0
                                             1   2   3     4    5     6     7   8   9    10   11   12   13   14   15   16   17   18   19   20
                                                                                Number of SOS Terms
                                     Figure 8. Statistical distribution of SOS term counts in synthetic polynomials.


generating rewards {r1 , . . . , rG }, and the advantage is computed as follows:
                                                                            ri − mean(r1 , . . . , rG )
                                                                    Âi =                                                                        (34)
                                                                                std(r1 , . . . , rG )
The policy model πθ is then optimized by maximizing the following objective:

                                                            G        |oi |
                                                         1 X 1 X               h                                                   i
  JGRPO (θ) = Eq∼Q,{oi }i=1G ∼πold (O|q)                                   {min γi,t (θ)Âi,t , clip (γi,t (θ), 1 − ϵ, 1 + ϵ) Âi,t −βDKL (πθ ||πref )}
                                                         G i=1 |oi | t=1
                                                                                                                                                     (35)

                   π (o           |q,o   )
where γi,t (θ) = πoldθ (oi,t      i,<t
                          i,t |q,oi,<t )
                                         is the importance sampling ratio, πref represents the reference model, πold is the policy used
to sample the responses, and DKL (πθ ||πref ) introduces a KL divergence constraint to limit the deviation of the model from
the reference model.

Difficulty-Based Curriculum Data Partitioning. As discussed in Section 4.1.2, we partition the training data based
on the difficulty of polynomial SOS decomposition in the dataset, obtaining multiple groups of training data with varying
difficulty levels. Each group is then trained using a Graduated Reinforcement Policy Optimization (GRPO) approach,
progressing from easier to more challenging data. Specifically, we categorize the data into three tiers based on the ascending
number of polynomial variables: Polynomial-SOS pairs data with 3 to 5 variables are used in the first stage, data with 6 to
8 variables in the second stage, and the more challenging data with 9 to 10 variables in the third stage. GRPO training is
conducted sequentially across these three stages.

Reward Functions Design.                     As illstrated in Section 4.1.2, the reward function design includes three key components:

   • [accuracy reward] encourages SOS structure conjectures with smaller errors compared to the original polynomial.
   • [format reward] ensures that the model-generated conjectures adhere to the required SOS structure.
   • [algebraic structure penalty] penalizes the SOS structure hypothesis based on the degree of term matching with the
     original polynomial.

The total reward is defined as:
                                                               R = wacc Racc + wfmt Rfmt − Pstruct ,                                             (36)

                                                                                    19
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

where wacc + wfmt = 1, Racc ∈ [0, 1] denotes the accuracy reward based on the approximation error, Rfmt ∈ [0, 1] denotes
the format consistency reward, Pstruct denotes the algebraic structure penalty.

Computation of Algebraic Structure Penalty. The algebraic structure penalty consists of two components: a soft
penalty and a hard penalty. To accurately assess the algebraic structure, we express the original polynomial f and the
model-generated SOS conjecture fˆ in terms of a common monomial basis. A coefficient threshold τ (e.g., 10−5 ) is set, such
that a monomial is considered present in the polynomial (i.e., a nonzero term) only if the absolute value of its coefficient
exceeds τ .
We define Structural Deviation Rate (SDR) to quantify the discrepancy between the algebraic structure of the SOS
representation and that of the original polynomial:

                                                                                           Nmiss + Nspur
                                                                                SDR =                    ,                                                               (37)
                                                                                               Nreq

where Nreq denotes the number of nonzero monomials in the original polynomial, Nmiss is the number of monomials that
appear in the original polynomial but are absent in fˆ, and Nspur is the number of extraneous terms present in fˆ but not
belonging to the monomial set Vf .
The soft penalty is defined as

                                                                       Pstruct-soft = λ · min(SDR, ρmax ),                                                               (38)

where λ controls the strength of the penalty and ρmax caps the maximum penalty.
If the generated SOS structure exhibits severe algebraic inconsistencies (e.g., exceeding the degree of the original polynomial
or introducing variables not present in it), a hard penalty is imposed:
                                                  (
                                                    Chard , if a structural violation occurs
                                   Pstruct-hard =                                                                          (39)
                                                    0,      otherwise

The overall algebraic structure penalty is the sum of the soft and hard penalties:

                                                                         Pstruct = Pstruct-hard + Pstruct-soft .                                                         (40)


E. Further Details of Lean Verification Module

            Lean Proof
            Lean Proof Template
                       Template                                                            Example: [Schur’s Inequality (r=2)] For non-negative real numbers 𝑎,𝑏,𝑐, 𝑟,
            /--
            General template for SOS-based inequality proofs.
            `<Theorem_Name>` : customized theorem name.
            `<Polynomial>` : target polynomial expression.
            `<Exact SOS Expression>` : list of weighted square terms representing the
            SOS decomposition.
            -/
            theorem <Theorem_Name> (x₁ x₂ ... xₙ : ℝ) (h₁ : I = <Polynomial>) : I ≥ 0 :=       Lean tactic：LLM_Ineq “”
            by
              -- Step 1: Construct SOS term list
              let terms : List (ℝ × ℝ) :=                                                                                                           Lean infoview
                [ <Exact SOS Expression> ]
              -- Step 2: Prove equality between polynomial and its SOS expansion
              have : I = (terms.map (λ (p, k) => p * k^2)).sum := by
                unfold terms
                simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
                  one_mul, mul_one, zero_mul, add_zero, zero_add, neg_mul]
                linear_combination h₁
              -- Step 3: Substitute and simplify
              rw [this]
              unfold terms
              simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
                one_mul, mul_one, zero_mul, add_zero, zero_add, ge_iff_le]
              -- Step 4: Apply positivity tactic to conclude
              positivity                                                                                                 No Goals


Figure 9. Automated Lean Proof Generation Example. left: The pre-defined Lean Proof Template. right: An Example of automated
proof generation within Lean4, where the formal verification is completed using the integrated tactic “LLM Ineq”.


                                                                                            20
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

E.1. Lean Template of Proof
Here presents the Lean4 proof template referenced in section Section 4.3, which yields a verifiable formal proof based on
the exact sum-of-squares (SOS) representation of a non-negative polynomial.

  Lean Proof Template
  /--
  General template for SOS-based inequality proofs.
  ‘<Theorem_Name>‘ : customized theorem name.
  ‘<Polynomial>‘ : target polynomial expression.
  ‘<Exact SOS Expression>‘ : list of weighted square terms representing the SOS
       decomposition.
  -/
  theorem <Theorem_Name> (x1 x2 ... xn : Real)
     (h1 : I = <Polynomial>) :
     I >= 0 := by
     -- Step 1: Construct SOS term list
     let terms : List (Real × Real) :=
       [ <Exact SOS Expression> ]
     -- Step 2: Prove equality between polynomial and its SOS expansion
     have : I = (terms.map (fun (p, k) => p * kˆ2)).sum := by
       unfold terms
       simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
         one_mul, mul_one, zero_mul, add_zero, zero_add, neg_mul]
       linear_combination h1
     -- Step 3: Substitute and simplify
     rw [this]
     unfold terms
     simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil,
       one_mul, mul_one, zero_mul, add_zero, zero_add, ge_iff_le]
     -- Step 4: Apply positivity tactic to conclude
     positivity


                           Figure 10. Lean template for inequality proof based on SOS representation.

The template uses the following placeholders:

  • <Theorem Name>: the customized theorem name;
  • <Polynomial>: the target polynomial expression (often an expanded or normalized form equivalent to the original);
  • <Exact SOS Expression>: a list of exact square terms constituting the SOS certificate, encoded as a Lean list of pairs
    (e.g., (p, k)) representing a squared polynomial p together with its coefficient k, according to the chosen encoding.

The proof proceeds in four structured steps:

  • Step 1: Construct the SOS term list. The SOS representation is introduced as terms : List(R × R) = [...] containing
    all exact squared terms required for the proof.
  • Step 2: Prove the polynomial identity. A key lemma establishes that the target polynomial equals the sum of the ex-
    panded SOS terms. This step typically relies on simp to unfold list combinators List.map cons, List.sum cons, etc. and
    on linear combination to derive the exact identity from the provided equality hypothesis (e.g., h1 : I = <Polynomial>)
    together with auxiliary algebraic equalities.
  • Step 3: Substitute and normalize the goal. By rewriting with the established identity (rw [this]), the original goal is
    transformed into nonnegativity of a sum-of-squares, followed by additional simplifications to reach a form amenable to
    automation.
  • Step 4: Conclude via positivity automation. Finally, the positivity tactic is invoked to prove that a sum-of-squares is
    nonnegative, completing the formal verification of I(x) ≥ 0.

                                                              21
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

E.2. An Example of Automated Lean Proof Generation
Fig. 9 illustrates the structure of the proof template and an example of automated proof generation.

F. Algorithm
Here provides the overall pseudocode for the proposed NSPI method (Algorithm 1), along with the detailed pseudocodes for
the progressive two-stage training process of the neural conjecture module (Algorithm 2), the Newton iteration (Algorithm 3),
and the rational recovery process (Algorithm 4) within the symbolic correction module.

Algorithm 1 Overall Proof Generation Process of NSPI
Input: Target polynomial f (x); SOS structure conjecturer M ; candidate budget K.
Output: A verified Lean proof script Pf ormal , or FAILURE.
 1: Stage 1: Neural Conjecture
 2: Sapprox ← M (f (x), K)                                                     ▷ Generate K SOS-structure conjectures
 3: Rank Sapprox by θ(s) = ∥fˆs (x) − f (x)∥2
 4: Stage 2: Symbolic Correction
 5: for each structure s in Sapprox do
 6:    GN ← NewtonIteration(f (x), s)               ▷ Gauss–Newton refinement to obtain GN with small backward error
 7:    Srat ← RationalRecovery(GN )                                               ▷ Interior/boundary rational recovery
 8:    if I S E XACT SOS(f (x), Srat ) then
 9:       break                                                             ▷ An exact rational SOS certificate is found
10:    end if
11: end for
12: Stage 3: Formal Verification
13: if Srat is found then
14:    Pf ormal ← T EMPLATE F ILL(f (x), Srat )                                  ▷ Generate Lean script from templates
15:    if L EAN C HECK(Pf ormal ) then
16:       return Pf ormal
17:    end if
18: end if
19: return FAILURE.



Algorithm 2 Progressive Two-Stage Training of the SOS Structure Conjecturer
Input: Base language model M0 ; data construction methods D = {D1 , . . . , D4 }; curriculum schedule C; GRPO hyperpa-
    rameters.
Output: Trained SOS structure conjecturer M .
 1: Stage 1: Data Construction and Supervised Fine-TuningS4
 2: Construct synthetic polynomial–SOS pairs S ← j=1 Dj                                     ▷ Four construction methods
 3: Train M0 on S via teacher forcing to obtain MSFT                                            ▷ Supervised fine-tuning
 4: Stage 2: Curriculum Reinforcement Learning
 5: Evaluate MSFT on S and collect unsolved samples U
 6: Partition U into curriculum buckets {U1 , . . . , UL } by C                                    ▷ Increasing difficulty
 7: for ℓ = 1 to L do
 8:   for each mini-batch B ⊂ Uℓ do
 9:      Sample SOS conjectures {Si } from M for each (f, S ⋆ ) ∈ B                                      ▷ Policy rollout
10:      Compute reward R(Si ) ← Racc (Si ) + Rfmt (Si ) − Palg (Si )          ▷ Accuracy, format, and algebraic penalty
11:      Update M via GRPO to maximize E[R]                                                    ▷ Reinforcement learning
12:   end for
13: end for
14: return M                                                                         ▷ Trained SOS structure conjecturer


                                                             22
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

Algorithm 3 N EWTON I TERATION: Gauss–Newton Refinement for SOS Certificates
Input: Polynomial f (x); SOS structure s; tolerance τ ; max steps TN .
Output: Refined numerical Gram matrix GN (or ∅).
 1: Build monomial basis v(x) implied by s and initialize floating Gram matrix G(0) .
 2: for t = 0 to TN − 1 do
 3:   Compute backward error θ(t) = ∥f (x) − v(x)⊤ G(t) v(x)∥2 .
 4:   if θ(t) ≤ τ then
 5:      return GN ← G(t)
 6:   end if
 7:   Update G(t) by one Gauss–Newton step (via Cholesky parameterization).
 8: end for
 9: return ∅.

Algorithm 4 R ATIONAL R ECOVERY: Exact Rational SOS Certificate Recovery
Input: Polynomial f (x); SOS structure s; refined Gram matrix GN ; rank threshold ϵ; precision ρ.
Output: Exact rational SOS certificate Srat (or ∅).
 1: Form affine constraints from coefficient matching: f (x) = v(x)⊤ Gv(x).
 2: if N UM R ANK(GN , ϵ) is full then
 3:    Project GN onto the affine constraint and rationalize entries with precision ρ.
 4: else
 5:    Perform truncated LDL⊤ and LLL-based rational vector recovery to preserve rank.
 6: end if
 7: Construct Srat from the recovered rational Gram matrix and return Srat .



G. Experimental Details
G.1. Implementation Details
During the data construction phase of the neural conjecture module, over one million training instances were generated
based on the proposed construction methods. Qwen3-8B (Team, 2025) was employed as the base model for SOS structure
conjecturing. In the reinforcement learning phase, progressive multi-round training was conducted using curriculum data
organized by the increasing number of variables: Stage 1 (3–5 variables), Stage 2 (6–8 variables), and Stage 3 (9–10
variables). The reward function parameters were configured with α = 0.5, λ = 0.5, and Chard = 0.5, with the accuracy
weight wacc set to 0.9. Within the symbolic correction module, the tolerance threshold τ for Newton iteration was predefined
as 1e-15. During the inference phase, the computational budget k is set to 32, with a maximum time limit of 1 hour.

G.2. Baseline Setups
To ensure a fair comparison, we evaluate our method against several categories of approaches, including symbol-based
methods, LLM-based provers, general-purpose LLMs, and hybrid systems. Detailed configurations and specifications for
each category are provided below.

   • Symbol-based Method. We evaluate the symbolic computation tools Maple (Heck & Koepf, 1993) and Z3 (De Moura
     & Bjørner, 2008). For Maple, we perform symbolic decomposition and sampling of the semi-algebraic set via
     SamplePoints to check for the absence of negative values. For Z3, we employ its SMT solver to formulate the
     problem as a satisfiability task under real arithmetic.

   • LLM-based Prover. We consider state-of-the-art (SOTA) LLM-driven Lean automated theorem provers, including
     DeepSeek-Prover-V2-7B (Ren et al., 2025), Goedel-Prover-V2-8B (Lin et al., 2025b), and Kimina Prover (Wang et al.,
     2025). Each prover is tested using its respective default prompt templates. In our main experiments, we compare their
     performance under a computational budget of pass@32.

   • General-purpose LLM. This group encompasses the latest closed-source foundation models, including GPT-5.2,
     Gemini-3-Pro-Preview, and DeepSeek-V3.2 (DeepSeek-AI, 2025). We assess their ability to generate Lean proofs

                                                            23
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

     directly from Lean theorem statements.

   • Hybrid system. We compare against the recent hybrid inequality-proving system LIPS (Li et al., 2025a), using its
     default experimental configuration. It is worth noting that a comparison with several hybrid systems (Wei et al., 2024;
     Li et al., 2025b) was not feasible, as their source code is not publicly available for replication. Furthermore, these
     methods primarily focus on addressing problems with 3 or 4 variables, as evidenced by the datasets described in their
     respective papers.


G.3. Details of Benchmark
Here we provide additional details on PolyIneqBench, the challenging inequality proving benchmark constructed in this
work.
Specifically, PolyIneqBench consists of a total of 522 inequality problems, which primarily categorized into two subsets
based on their origin and complexity:


   • PolyIneq-Real: This subset contains 102 inequality problems sourced from real-world domains. It comprises two
     main components:

       – Classical benchmark inequalities, including the Schur inequality, Robinson polynomial, Delzell polynomial,
         Peyri–Parrilo polynomial, Lax polynomial, Nesbitt inequality, and Voronoi polynomial.
       – Problems derived from national and international mathematics competitions, as well as standard competition
         textbooks.

     Representative examples of PolyIneq-Real are presented in Table 4.

   • PolyIneq-Synth: To extend the benchmark to higher-dimensional settings, we constructed this synthetic subset
     containing 420 inequalities spanning four to ten variables (with 60 problems per variable count). Each generated
     problem was validated by domain experts through manual quality assessment on randomly sampled instances (see
     Section D.2), ensuring non-triviality and challenge. Representative examples are provided in Table 5.


Expanding to High-Dimensional Settings: As shown in Table 4, most problems in PolyIneq-Real involve only three or
four variables. PolyIneq-Synth was specifically designed to address this limitation by introducing systematically constructed
problems in higher-dimensional settings.
Table 3 presents the distribution of polynomial inequalities within the PolyIneqBench, categorized by the number of variables
(n) and their respective sample sizes.

                      Table 3. Distribution of Polynomial Inequalities by Variable Count in PolyIneqBench.

                                            Variable Count (n)       Sample Size
                                                      3                   84
                                                      4                   77
                                                      5                   60
                                                      6                   61
                                                      7                   60
                                                      8                   60
                                                      9                   60
                                                     10                   60


                                                              24
     From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

                                       Table 4. Part of PolyIneq-Real Benchmark

Source                       #Variables (n)   #Degree     #Terms      f (x)
(Chen, 2014)                       3              2           6       x21 − x1 x2 − x1 x3 + x22 − x2 x3 + x23
(Chen, 2014)                       3              6           6       x61 − x41 x22 − x21 x43 + x62 − x42 x23 + x63
(Tung, 2012)                       3              8           7       4x81 − 4x21 x22 − 4x21 x23 + 4x82 − 4x22 x23 + 4x83 + 3
(Tung, 2012)                       3              4           6       −2x41 + 2x21 x22 + 2x21 x23 + x42 − 4x22 x23 + x43
(Riasat, 2008)                     3              2           6       2x21 − 2x1 x2 − 2x1 x3 + 2x22 − 2x2 x3 + 2x23
IMO Short List 1998                3              8           7       4x81 + 4x61 + 4x82 + 4x62 + 4x83 + 4x63 − 3
(Manfrino et al., 2010)            3              8           6       x41 x42 − x41 x22 x23 + x41 x43 − x21 x42 x23 − x21 x22 x43 + x42 x43
Canada 2002                        3              8           6       x81 − x41 x22 x23 − x21 x42 x23 − x21 x22 x43 + x82 + x83
Spain 1996                         3              4           6       x41 − 4x21 x22 + 2x21 x23 + 4x42 − 4x22 x23 + x43
Schur’s Inequality (r = 2)         3              8           12      x81 − x61 x22 − x61 x23 + x41 x22 x23 − x21 x62 + x21 x42 x23 +
                                                                      x21 x22 x43 − x21 x63 + x82 − x62 x23 − x22 x63 + x83
                                                                      x63 − x42 x23 − x22 x43 + x62 − x21 x43 + 3x21 x22 x23 − x21 x42 −
Robinson Polynomial                3              6           10
                                                                      x41 x23 − x41 x22 + x61
(Mildorf, 2005)                    3              4           9      x41 − 3x31 x2 + 2x21 x22 + 2x21 x23 − 3x1 x33 + x42 − 3x32 x3 +
                                                                     2x22 x23 + x43
                                                                      x81 + 4x61 x22 − 4x61 x23 + 2x41 x42 + 2x41 x43 − 4x21 x62 +
(Parvardi, 2011)                   3              8           12
                                                                      4x21 x63 + x82 + 4x62 x23 + 2x42 x43 − 4x22 x63 + x83
                                                                      4x61 + 12x41 x22 − 15x41 x23 − 15x21 x42 − 3x21 x22 x23 +
(Tung & Zhe, 2014)                 3              6           10
                                                                      12x21 x43 + 4x62 + 12x42 x23 − 15x22 x43 + 4x63
                                                                      x21 x22 x23 − 2x21 x2 x3 + x21 − 2x1 x22 x3 − 2x1 x2 x23 +
(Lee, 2005)                        3              6           10
                                                                      2x1 x2 + 2x1 x3 + x22 + 2x2 x3 + x23
                                                                      x61 + 3x41 x22 + 3x21 x42 − 4x21 x22 − 4x21 x23 − 4x21 x24 + x62
(Andreescu, 2019)                  4              6           15      − 4x22 x23 − 4x22 x24 + x63 + 3x43 x24 + 3x23 x44
                                                                      − 4x23 x24 + x64 + 8
                                                                      1 − 8x23 x24 − 196608x35 x21 x24 x3 + 1536x5 x1 x44 x23 +
                                                                      21504x25 x1 x24 x3 − 4096x25 x1 x33 x24 − 384x5 x1 x24 +
                                                                      1024x25 x1 x3 + 16x43 x44 − 72x23 x44 + 1024x23 x25 +
(El Din, 2008)                     4              8           20
                                                                      36864x25 x21 x44 − 3456x5 x1 x44 + 262144x45 x21 x23 −
                                                                      32768x35 x1 x23 + 256x33 x24 x5 − 576x3 x5 x24 + 81x44
                                                                      + 64x3 x5 − 18x24
                                                                      x41 + x1 x32 + x42 − 3x21 x2 x3 − 4x1 x22 x3 + 2x21 x23 + x1 x33
(Magron et al., 2023)              3              4           9
                                                                      + x2 x33 + x43




                                                         25
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

                                            Table 5. Part of PolyIneq-Synth Benchmark

      #Variables (n)     #Degree    #Terms                                                f (x)
             4              12          7         6x12    6     3     6 2 4       2 6      2 6         5 4      4 8
                                                    1 − 2x1 x2 x3 − 4x1 x4 x3 + 5x2 x4 + 4x2 x3 − 2x2 x4 x3 + 3x4 x3

             5              12         10         8x12        6            6 2       2 10  2 6         2 2 2
                                                    1 + 2x1 x2 x3 x4 + 2x1 x5 + 8x2 x3 + 2x2 x3 x4 + 6x2 x3 x4 −
                                                             2     2 6         5     4
                                                  2x2 x3 x4 x5 + 7x4 x5 − 2x4 x5 + 8x5
             6              12         13         5x12     6 6      6 3 2      12    6 3 2      6 2 2 2       6
                                                    1 +2x1 x2 +2x1 x3 x4 +8x2 −2x2 x3 x4 +2x2 x3 x4 x5 +2x2 x4 x6 +
                                                                                                                   5
                                                    6 4      5 4 2        4 4 4      3 3 5       2 3 5 2        2 10
                                                  5x3 x4 + 2x3 x4 x5 + 5x3 x4 x5 − 2x3 x4 x6 − 2x3 x4 x6 x5 + 7x4 x6
             7              12         14         4x10    2       5 3 2 2          5     3             5   3 3          5
                                                    1 x2 + 4x1 x2 x3 x4 − 2x1 x2 x3 x5 − 6x1 x2 x6 x7 + 2x1 x2 x6 x4 x7 +
                                                                                                                                2 3

                                                  5x42 x43 x44 −10x22 x53 x5 x24 −2x22 x23 x36 x24 x37 +4x22 x23 x6 x44 x37 +9x63 x25 −
                                                  8x33 x5 x36 x37 − 4x33 x5 x6 x24 x37 + 8x66 x67 + 2x26 x44 x67
             8              16         23         9x12   2            10 2 2 2             6 2 2           2
                                                    1 x7 + 22x1 x3 x5 x8 + 16x1 x3 x5 x6 x7 x8 − 44x1 x3 x5 x8 +
                                                                                                                      6 2

                                                  4x1 x4 x5 + 6x1 x3 x5 x6 x8 + 8x1 x3 x5 x7 x8 − 8x1 x3 x4 x35 x6 x7 x8 +
                                                    6 2 4            5 2 2               5 2                 4

                                                  11x41 x24 x45 x28 −16x31 x3 x4 x35 x6 +8x31 x3 x4 x25 x7 +23x21 x23 x25 x26 x27 x28 −
                                                  32x21 x23 x5 x6 x7 x8 +28x21 x23 +32x1 x23 x25 x26 x7 x8 −8x1 x23 x5 x6 x27 x8 −
                                                  16x1 x23 x5 x6 − 8x1 x23 x7 + 2x42 x24 x25 x26 x27 x28 + 4x22 x3 x4 x5 x6 x27 x8 +
                                                  21x23 x25 x26 − 16x23 x5 x6 x7 + 8x23 x27
             9              18         34         14x12     2 2        12               12        8            2
                                                       1 x3 x9 − 2x1 x3 x9 + 13x1 + 2x1 x2 x3 x5 x9 − 2x1 x2 x5 x9 −
                                                                                                                        8

                                                  2x1 x2 x3 x4 x5 x6 − 4x1 x2 x3 x5 x6 x7 x8 x9 + 2x71 x25 x9 +
                                                     7 2 2           2            7       2 2

                                                  2x61 x33 x26 x9 + 2x61 x23 x5 x8 x9 + 2x61 x23 x26 + 4x61 x3 x4 x5 x8 x29 +
                                                  2x61 x3 x5 x8 − 2x61 x7 x8 x49 + 15x41 x22 x25 x29 + 2x31 x22 x3 x35 x6 x7 x8 x9 −
                                                  2x31 x2 x35 x29 + 11x21 x42 x43 x24 x25 x46 + 12x21 x22 x23 x45 x26 x27 x28 −
                                                  4x21 x2 x3 x25 x8 x9 − 2x21 x2 x4 x25 x8 x29 + 2x21 x2 x5 x7 x8 x59 +
                                                  13x21 x45 x29 − 2x1 x22 x33 x4 x25 x26 x8 − 2x1 x22 x23 x4 x5 x26 x7 x8 x49 −
                                                  2x1 x2 x23 x35 x6 x7 x28 + 2x1 x23 x25 x26 x9 + 2x1 x4 x35 x8 x29 + 16x43 x46 −
                                                  2x33 x5 x26 x8 +13x23 x25 x28 −2x3 x4 x25 x28 x9 +12x24 x25 x28 x29 +14x27 x28 x89
             10             18         42         10x10     6         7 3 3                 6       4
                                                       1 x4 + 2x1 x4 x7 x8 − 2x1 x3 x4 x5 x6 x7 − 4x1 x3 x4 x5 x9 −
                                                                                                                        6      3

                                                  2x1 x2 x4 x6 x7 − 2x1 x4 x5 x8 x9 + 10x1 x7 x8 + 2x1 x2 x3 x6 x57 x28 x9 +
                                                     5      3 6 2          5 3 2 3                   4 6 2          3

                                                  4x31 x3 x4 x5 x6 x47 x8 +14x21 x22 x23 x26 x47 x28 x29 −4x21 x2 x23 x5 x6 x27 x8 x29 −
                                                  2x21 x2 x3 x37 x8       −         2x21 x2 x66 x57 x8     +         2x21 x2 x37 x8     +
                                                       2 2 2 2 2 2
                                                  15x1 x3 x4 x5 x6 x7 − 4x1 x3 x4 x5 x6 x7 x9 + 16x21 x23 x25 x29 +
                                                                                      2 2        2

                                                  2x1 x10 x32 x23 x4 x6 x37 x28 x29       +        2x1 x10 x22 x23 x4 x5 x7 x8 x29      −
                                                  2x1 x2 x3 x6 x7 x8 x9 − 2x1 x2 x3 x6 x7 x8 x9 − 2x1 x22 x3 x6 x27 x8 x9 −
                                                        2 2       2                    2      7 4

                                                  2x1 x2 x23 x5 x9 − 4x1 x2 x3 x4 x5 x76 x37 + 2x1 x2 x3 x4 x5 x6 x7 −
                                                  4x1 x2 x3 x25 x6 x27 x48 x29 − 2x1 x2 x3 x5 x66 x27 x9 − 2x1 x2 x3 x5 x9 +
                                                  2x1 x3 x35 x38 x29 + 13x210 x42 x23 x24 x27 x28 x29 + 2x10 x32 x23 x4 x7 x8 x9 −
                                                  2x10 x32 x3 x4 x66 x37 x8 x9            +           2x10 x32 x3 x4 x7 x8 x9           −
                                                  2x10 x2 x3 x4 x5 x7 x8 x9 + 10x2 x3 − 2x22 x3 + 14x22 x12
                                                          2         2     4 2               2 2
                                                                                                                                 6 7 +
                                                                                                                                    x 4

                                                  2x22 x66 x27 + 15x22 + 2x2 x3 x25 x38 x9 − 4x2 x25 x38 x9 + 12x45 x68 x29




H. Case Study
Here we provide detailed case studies illustrating the complete proof process of NSPI on two representative examples drawn
from PolyIneqBench.
Case 1 is a classical inequality from the PolyIneq-Real subset, whereas Case 2 is a challenging competition-level synthetic
inequality from the PolyIneq-Synth subset, corresponding to a higher-dimensional and more difficult setting. Notably, for
Case 2, NSPI is the only method among all baselines that successfully completes the proof.

                                                                 26
        From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates


            Case 1: (Peyrl-Parrilo polynomial)



                                                                Conjecture


              LLM Conjecture:
            <SOS Expression>:




                                                               Newton Iteration


          Newton-refined Approximations




                                                                Rational Recovery


         Exact SOS Representation via Rational Recovery




Figure 11. Detailed workflow of the NSPI method applied to the Peyrl-Parrilo polynomial from PolyIneq-Real (Case 1).This
example illustrates the complete pipeline from initial conjecture to formal certification.



      Case 2: A polynomial with 10 variables from PolyIneq-Synth, where f(x) =




                                                                  Conjecture


           LLM Conjecture:
         <SOS Expression>:




                                                                  Newton Iteration

            Newton-refined Approximations




                                                                     Rational Recovery

            Exact SOS Representation via Rational Recovery




Figure 12. Case study of a challenging synthetic polynomial from PolyIneq-Synth. This 10-variable instance represents a significant
challenge in high-dimensional formal reasoning; notably, NSPI is the sole method among all evaluated baselines (Case 2) capable of
successfully generating a verified formal proof.



                                                                                         27
                             From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

      H.1. Case 1: Peyrl-Parrilo polynomial.
      Case 1 features a classic non-negative polynomial drawn from (Peyrl & Parrilo, 2008b; Le & Van Barel, 2014). Fig. 11
      presents an example of generating a complete proof using the NSPI method.

      H.2. Case 2: A challenging synthetic polynomial.
      We present a challenging 10-variable synthetic polynomial instance from the PolyIneq-Synth dataset. Notably, for this
      specific case, NSPI is the only method among all considered baselines that successfully generates a complete formal proof.

      I. More Experimental Results
      I.1. Results under Different Computational Budgets
      Here, we report the performance of various LLM-based provers and our NSPI method under different computational budgets.
      The results on PolyIneqBench are summarized in Table 6.

                                    Table 6. Comparative results of multiple methods on PolyIneqBench under different computational budgets

                                             Method Name               Computational Budget                                  PolyIneq-Real          PolyIneq-Synth
                                                                                pass@8                                                  28.43%              0.00%
                                             DeepSeek-Prover-V2                 pass@16                                                 32.35%              0.00%
                                                                                pass@32                                                 37.25%              0.00%
                                                                                pass@8                                                  15.69%              0.48%
                                             Goedel-Prover-V2                   pass@16                                                 16.67%              0.48%
                                                                                pass@32                                                 18.63%              0.48%
                                                                                pass@8                                                  27.45%              0.24%
                                             Kimina-Prover                      pass@16                                                 30.39%              0.24%
                                                                                pass@32                                                 33.33%              0.71%
                                                                                pass@8                                                  36.27%              23.57%
                                             NSPI (ours)                        pass@16                                                 40.20%              25.48%
                                                                                pass@32                                                 43.14%              25.95%


      I.2. Detailed Comparative Study on Benchmark Difficulty Metrics

                      16 (n=153)
                          14.67                                                                                                     11.44
                                                                                                                            12 (n=153)
                      14
                                                                                               Avg #Total Degree (solved)




                                     11.77                                                                                                     9.50    9.75    9.54
                                             11.42
                                    (n=107) (n=144)  11.27                                                                  10               (n=107) (n=144) (n=135)
Avg #Terms (solved)




                      12                            (n=135)
                                                               9.92
                                                              (n=37)                                                                                                     7.51
                      10                                                8.63      8.57                                       8                                          (n=37)    6.89      6.86
                                                                       (n=38)    (n=21)                                                                                          (n=38)    (n=21)
                       8                                                                                                     6
                       6
                                                                                                                             4
                       4
                       2                                                                                                     2
                       0                                                                                                     0
                            ours)    LIPS   Map
                                               le    Z3           r       2
                                                              rove rover-V rover-V
                                                                                   2                                                 rs)     LIPS   Map
                                                                                                                                                       le       Z3          r       2
                                                                                                                                                                        rove rover-V rover-V
                                                                                                                                                                                             2
                       SPI(                              na_p                                                                    I(ou                               na_p
                      N                                             -P
                                                     kimi epseek Goedel
                                                                            -P                                              NSP                                               -P
                                                                                                                                                                kimi epseek Goedel
                                                                                                                                                                                      -P
                                                          De                                                                                                         De
     (a) Average Number of Terms in Polynomials Solved by Different                                    (b) Average Total Degree of Terms in Polynomials Solved by
     Methods.                                                                                          Different Methods.
                      Figure 13. Comparative analysis of different polynomial solving methods: (a) average number of terms; (b) average total degree.


      Fig. 13 and Fig. 14 present a comparative analysis of different polynomial inequality solving methods in terms of average
      number of terms (Fig. 13 (a)), average total degree (Fig. 13 (b)), and average number of variables (Fig. 14) in successfully

                                                                                          28
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

                                                          6          5.36
                                                          5




                                Avg #Variables (solved)
                                                                             4.02     3.92
                                                          4                                   3.73
                                                                                                         3.38                 3.19
                                                                                                                    3.05
                                                          3
                                                          2
                                                          1
                                                          0
                                                                  rs)       LIPS    Map
                                                                                       le     Z3           over    r-V2      r-V2
                                                              I(ou                                     a_pr k-Prove el-Prove
                                                  NSP                                            m i n
                                                                                              ki            psee  Goe
                                                                                                                      d
                                                                                                        Dee
Figure 14. Average number of variables in polynomial inequalities successfully verified by each method. This metric illustrates the
scalability of various provers, where NSPI (ours) demonstrates a superior capability in handling higher-dimensional problems compared
to both symbolic baselines and LLM-based provers.



solved instances.
Fig. 13 shows that our NSPI outperforms other methods in terms of the average number of terms and total degree in the
polynomials it solves, suggesting its ability to handle more complex polynomials.
Fig. 14 highlights that NSPI also excels in handling higher-dimensional problems, as it successfully solves polynomials
with the largest average number of variables, outperforming symbolic and LLM-based provers. These metrics together
demonstrate NSPI’s superior scalability in solving complex and high-dimensional polynomial inequalities compared to both
symbolic and LLM-based approaches.

J. Extended Discussion
Neuro-symbolic reasoning systems represent a highly valuable and promising research direction. It is worth noting that the
neuro-symbolic approach to inequality proving proposed in this work differs fundamentally from existing neuro-symbolic
practices. In particular, we innovatively explore the feasibility of employing large language models (LLMs) as core symbolic
conjecture engines that directly provide end-to-end symbolic priors, thereby opening a promising new direction in which
LLMs function as the central component for symbolic conjecturing. Moreover, we extend formalized theorem proving for
polynomial inequalities to challenging high-dimensional cases with up to 10 variables, thereby extending the boundary of
automated proof generation for polynomial inequalities. To further contextualize the contributions of this work, we provide
a comparative discussion with existing neuro-symbolic reasoning approaches.

J.1. A New Paradigm: LLMs as Core Symbolic Conjecture Engines
In recent years, several neuro-symbolic hybrid reasoning approaches have demonstrated encouraging progress in automated
theorem proving. However, in most existing systems, neural modules primarily serve auxiliary roles that guide or accelerate
symbolic derivation processes by reducing the search space.
For example, AlphaGeometry (Trinh et al., 2024) uses an LLM to predict auxiliary constructions, while the proof is
completed by a symbolic solver that enumerates derivation rules. AIPS (Wei et al., 2024) employs a learned value network
to evaluate intermediate subgoals during symbolic proof search. LIPS (Li et al., 2025a) leverages an LLM to generate
candidate goal-rewriting steps and selects promising subgoals to prune the strategy space. Similarly, IneqSearch (Li et al.,
2025b) leverages LLMs to perform inequality transformations or to select appropriate transformation rules, integrating
an iterative learning mechanism. In these systems, neural components assist decision-making within a symbolic engine,
whereas the ability of neural models to directly provide symbolic reasoning content remains relatively underexplored.
In contrast, our work treats the LLM as a core symbolic conjecturing engine. The LLM directly produces the symbolic priors
required to complete a proof, in the form of SOS structure conjectures. These conjectures are subsequently refined through

                                                                                             29
       From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates

Newton-style numerical refinement and rational recovery (Section 4.2), and finally transformed into complete formal Lean
proofs (Section 4.3). This end-to-end pipeline demonstrates the feasibility of a new neuro-symbolic paradigm in which
LLMs provide high-level symbolic structure, while symbolic computation and formal verification ensure correctness.

J.2. Extending the Frontier of Formal Polynomial Inequality Proving
Automated formal proving of polynomial inequalities remains a challenging problem. Although automated theorem-
proving techniques have advanced rapidly, competition-level polynomial inequalities continue to pose significant difficulties,
especially in settings involving many variables or high-dimensional structures.
Learning-based approaches to formal inequality proving often face a bottleneck in the availability of high-quality formal data.
Widely used theorem-proving benchmarks, such as miniF2F (Zheng et al., 2021), ProofNet (Azerbayev et al., 2023) and
Putnum (Tsoukalas et al., 2024) contain very few polynomial inequality problems; this scarcity is particularly pronounced
for high-dimensional multivariate polynomials. Existing neuro-symbolic inequality proving methods also tend to focus on
low-dimensional cases with a small number of variables, and struggle to scale to more complex settings.
The neuro-symbolic approach proposed in this work extends Lean-based formal polynomial inequality proving to settings
involving up to ten variables, and further introduces a competition-level benchmark covering inequalities with three to
ten variables. As demonstrated by the results in Section 5, our method consistently outperforms all LLM-based and
symbolic baselines on this challenging benchmark, with particularly strong performance in cases involving a larger number
of variables. These results indicate that the proposed approach significantly expands the frontier of formal polynomial
inequality theorem proving.

K. More Examples
Here we provide additional examples that were successfully solved exclusively by our proposed NSPI method among all
baseline approaches.

  NSPI Achieves Solution While Baseline Methods Fail(1)
  Polynomial:
  8x61 x22 x23 x24 + 6x41 x25 x6 x2 x3 x4 + 8x31 x67 x2 x3 x4 + 8x31 x6 x32 x23 x4 + 6x31 x2 x3 x34 x28 x29 + 9x21 x45 x26 − 6x1 x67 x25 x6 −
  4x1 x25 x26 x22 x3 + 10x1 x25 x6 x24 x28 x29 + 9x12       6    2           6 2 2 2         2 4 2             2       2 2 2
                                                   7 + 2x7 x6 x2 x3 + 4x7 x4 x8 x9 + 9x6 x2 x3 − 8x6 x2 x3 x4 x8 x9 + 6x4 x8 x9
                                                                                                                                    4 4 4


  Lean Proof:
  import Mathlib
  theorem f1 (x1 x2 x3 x4 x5 x6 x7 x8 x9 I : Real) (h1 :I = 8*x1ˆ6*x2ˆ2*x3ˆ2*x4ˆ2 + 6*x1
      ˆ4*x2*x3*x4*x5ˆ2*x6 + 8*x1ˆ3*x2ˆ3*x3ˆ2*x4*x6 + 6*x1ˆ3*x2*x3*x4ˆ3*x8ˆ2*x9ˆ2 + 8*x1
      ˆ3*x2*x3*x4*x7ˆ6 + 9*x1ˆ2*x5ˆ4*x6ˆ2 - 4*x1*x2ˆ2*x3*x5ˆ2*x6ˆ2 + 10*x1*x4ˆ2*x5ˆ2*x6*
      x8ˆ2*x9ˆ2 - 6*x1*x5ˆ2*x6*x7ˆ6 + 9*x2ˆ4*x3ˆ2*x6ˆ2 - 8*x2ˆ2*x3*x4ˆ2*x6*x8ˆ2*x9ˆ2 + 2*
      x2ˆ2*x3*x6*x7ˆ6 + 6*x4ˆ4*x8ˆ4*x9ˆ4 + 4*x4ˆ2*x7ˆ6*x8ˆ2*x9ˆ2 + 9*x7ˆ12) : I >= 0 :=
      by
    let terms : List (Real × Real) := [ (0, 1), (0, x2ˆ2*x3), (9, x1ˆ3*x2*x3*x4/3 + x1*
         x5ˆ2*x6 - 2*x2ˆ2*x3*x6/9 + 5*x4ˆ2*x8ˆ2*x9ˆ2/9 - x7ˆ6/3), (77/9, 6*x1ˆ3*x2*x3*x4
         /11 + x2ˆ2*x3*x6 - 26*x4ˆ2*x8ˆ2*x9ˆ2/77 + 3*x7ˆ6/77), (173/77, 224*x1ˆ3*x2*x3*x4
         /173 + x4ˆ2*x8ˆ2*x9ˆ2 + 291*x7ˆ6/173), (282/173, -13*x1ˆ3*x2*x3*x4/282 + x7ˆ6),
         (0, x3ˆ2*x4ˆ4), (193/282, x1ˆ3*x2*x3*x4), (0, x4ˆ2*x6*x8ˆ2*x9ˆ2), (0, x6*x7ˆ6) ]
    have : I = (terms.map (fun (p, k) => p * kˆ2)).sum := by
      unfold terms
      simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil]
      linear_combination h1
    rw [this]
    unfold terms
    simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil]
    positivity




                                                                      30
     From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates




NSPI Achieves Solution While Baseline Methods Fail(2)
Polynomial:
7x21 x22 x23 x24 − 2x1 x25 x2 x3 x4 x6 x7 x8 − 4x1 x5 x2 x3 x4 x6 x49 − 6x1 x2 x3 x4 x56 x8 − 10x1 x2 x3 x4 x6 x37 x28 + 8x45 x26 x27 x28 −
4x25 x26 x47 x38 + 8x25 x26 x89 − 4x5 x66 x8 x49 − 2x5 x26 x37 x28 x49 + 5x10 2     6 3 3       2 6 4
                                                                           6 x8 + 6x6 x7 x8 + 6x6 x7 x8

Lean Proof:
import Mathlib
theorem f1 (x1 x2 x3 x4 x5 x6 x7 x8 x9 I : Real) (h1 :I = 7*x1ˆ2*x2ˆ2*x3ˆ2*x4ˆ2 - 2*x1
    *x2*x3*x4*x5ˆ2*x6*x7*x8 - 4*x1*x2*x3*x4*x5*x6*x9ˆ4 - 6*x1*x2*x3*x4*x6ˆ5*x8 - 10*x1*
    x2*x3*x4*x6*x7ˆ3*x8ˆ2 + 8*x5ˆ4*x6ˆ2*x7ˆ2*x8ˆ2 - 4*x5ˆ2*x6ˆ2*x7ˆ4*x8ˆ3 + 8*x5ˆ2*x6
    ˆ2*x9ˆ8 - 4*x5*x6ˆ6*x8*x9ˆ4 - 2*x5*x6ˆ2*x7ˆ3*x8ˆ2*x9ˆ4 + 5*x6ˆ10*x8ˆ2 + 6*x6ˆ6*x7
    ˆ3*x8ˆ3 + 6*x6ˆ2*x7ˆ6*x8ˆ4) : I >= 0 := by
  let terms : List (Real × Real) := [ (0, 1), (0, x3*x4ˆ2), (0, x4ˆ3*x6), (7, x1*x2*x3
      *x4 - x5ˆ2*x6*x7*x8/7 - 2*x5*x6*x9ˆ4/7 - 3*x6ˆ5*x8/7 - 5*x6*x7ˆ3*x8ˆ2/7), (55/7,
      x5ˆ2*x6*x7*x8 - 2*x5*x6*x9ˆ4/55 - 3*x6ˆ5*x8/55 - 19*x6*x7ˆ3*x8ˆ2/55), (0, x3ˆ2*x4
      *x6*x7), (408/55, x5*x6*x9ˆ4 - 79*x6ˆ5*x8/204 - 139*x6*x7ˆ3*x8ˆ2/408), (257/408,
      -110*x6ˆ5*x8/257 + x6*x7ˆ3*x8ˆ2), (633/257, x6ˆ5*x8), (0, x4*x6ˆ5), (0, x3ˆ4*x5*
      x6), (0, x5ˆ2*x6ˆ2*x7ˆ4*x8ˆ3), (0, x6ˆ6*x7ˆ3*x8ˆ3) ]
  have : I = (terms.map (fun (p, k) => p * kˆ2)).sum := by
    unfold terms
    simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil]
    linear_combination h1
  rw [this]
  unfold terms
  simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil]
  positivity




                                                                    31
      From LLM Conjectures to Lean Formalizations: Automated Inequality Proving via Sum-of-Squares Certificates




NSPI Achieves Solution While Baseline Methods Fail(3)
Polynomial:
11x41 x42 x23 − 4x31 x32 x3 − 12x31 x22 x33 x5 x6 − 6x31 x22 x23 x55 x7 + 2x21 x32 x33 x5 − 2x21 x32 x3 x4 − 8x21 x32 x3 x5 x7 − 2x21 x22 x3 x47 +
10x21 x22 + 4x21 x2 x23 x5 x6 + 4x21 x2 x3 x55 x7 + 12x21 x43 x25 x26 + 2x21 x33 x65 x6 x7 + 12x21 x23 x10   2            2 2
                                                                                                         5 x7 − 12x1 x2 x3 x5 − 4x1 x2 x4 −
                                                                                                                                           2

2x1 x2 x5 x7 −6x1 x2 x3 x5 x6 +2x1 x2 x3 x5 x7 +8x1 x2 x3 x4 x5 x6 +2x1 x2 x3 x5 x6 x7 +4x1 x2 x3 x4 x5 x7 −6x1 x2 x3 x65 x27 −
      2                    4 2                 3 6                  2                      2 2                          5

14x1 x2 x47 +10x1 x23 x5 x6 x47 +2x1 x3 x55 x57 +13x22 x43 x25 +4x22 x23 x4 x5 −12x22 x23 x25 x7 +10x22 x24 +14x22 x25 x27 +8x2 x23 x5 x47 +
2x2 x4 x47 + 4x2 x5 x57 + 12x87
Lean Proof:
import Mathlib
theorem f1 (x1 x2 x3 x4 x5 x6 x7 I : Real) (h1 :I = 11*x1ˆ4*x2ˆ4*x3ˆ2 - 4*x1ˆ3*x2ˆ3*x3
     - 12*x1ˆ3*x2ˆ2*x3ˆ3*x5*x6 - 6*x1ˆ3*x2ˆ2*x3ˆ2*x5ˆ5*x7 + 2*x1ˆ2*x2ˆ3*x3ˆ3*x5 - 2*x1
    ˆ2*x2ˆ3*x3*x4 - 8*x1ˆ2*x2ˆ3*x3*x5*x7 - 2*x1ˆ2*x2ˆ2*x3*x7ˆ4 + 10*x1ˆ2*x2ˆ2 + 4*x1ˆ2*
    x2*x3ˆ2*x5*x6 + 4*x1ˆ2*x2*x3*x5ˆ5*x7 + 12*x1ˆ2*x3ˆ4*x5ˆ2*x6ˆ2 + 2*x1ˆ2*x3ˆ3*x5ˆ6*x6
    *x7 + 12*x1ˆ2*x3ˆ2*x5ˆ10*x7ˆ2 - 12*x1*x2ˆ2*x3ˆ2*x5 - 4*x1*x2ˆ2*x4 - 2*x1*x2ˆ2*x5*x7
     - 6*x1*x2*x3ˆ4*x5ˆ2*x6 + 2*x1*x2*x3ˆ3*x5ˆ6*x7 + 8*x1*x2*x3ˆ2*x4*x5*x6 + 2*x1*x2*x3
    ˆ2*x5ˆ2*x6*x7 + 4*x1*x2*x3*x4*x5ˆ5*x7 - 6*x1*x2*x3*x5ˆ6*x7ˆ2 - 14*x1*x2*x7ˆ4 + 10*
    x1*x3ˆ2*x5*x6*x7ˆ4 + 2*x1*x3*x5ˆ5*x7ˆ5 + 13*x2ˆ2*x3ˆ4*x5ˆ2 + 4*x2ˆ2*x3ˆ2*x4*x5 -
    12*x2ˆ2*x3ˆ2*x5ˆ2*x7 + 10*x2ˆ2*x4ˆ2 + 14*x2ˆ2*x5ˆ2*x7ˆ2 + 8*x2*x3ˆ2*x5*x7ˆ4 + 2*x2*
    x4*x7ˆ4 + 4*x2*x5*x7ˆ5 + 12*x7ˆ8) : I >= 0 := by
  let terms : List (Real × Real) := [ (0, 1), (10, -x1ˆ2*x2ˆ2*x3/10 - x1*x2/5 + 2*x1*
      x3ˆ2*x5*x6/5 + x1*x3*x5ˆ5*x7/5 + x2*x3ˆ2*x5/5 + x2*x4 + x7ˆ4/10), (48/5, -11*x1
      ˆ2*x2ˆ2*x3/48 + x1*x2 + 7*x1*x3ˆ2*x5*x6/24 + x1*x3*x5ˆ5*x7/4 - 7*x2*x3ˆ2*x5/12 -
      5*x2*x5*x7/48 - 17*x7ˆ4/24), (667/48, -7*x1ˆ2*x2ˆ2*x3/23 + 62*x1*x3ˆ2*x5*x6/667 -
       132*x1*x3*x5ˆ5*x7/667 - 316*x2*x3ˆ2*x5/667 + x2*x5*x7 + 62*x7ˆ4/667), (0, x2*x3*
      x5), (9289/1334, -2755*x1ˆ2*x2ˆ2*x3/9289 + 8622*x1*x3ˆ2*x5*x6/9289 + 3676*x1*x3*
      x5ˆ5*x7/9289 + 594*x2*x3ˆ2*x5/9289 + x7ˆ4), (57461/9289, -18159*x1ˆ2*x2ˆ2*x3
      /57461 - 18281*x1*x3ˆ2*x5*x6/57461 + 4839*x1*x3*x5ˆ5*x7/57461 + x2*x3ˆ2*x5), (0,
      x3ˆ4), (163073/57461, -187911*x1ˆ2*x2ˆ2*x3/163073 + x1*x3ˆ2*x5*x6 - 151490*x1*x3*
      x5ˆ5*x7/163073), (670239/163073, x1ˆ2*x2ˆ2*x3 - 838684*x1*x3*x5ˆ5*x7/670239), (0,
       x1*x3*x5ˆ5), (292711/670239, x1*x3*x5ˆ5*x7) ]
  have : I = (terms.map (fun (p, k) => p * kˆ2)).sum := by
    unfold terms
    simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil]
    linear_combination h1
  rw [this]
  unfold terms
  simp only [List.map_cons, List.map_nil, List.sum_cons, List.sum_nil]
  positivity




                                                                       32
