                                           A COMPLEX-ANALYTIC PROOF OF SQUARE-RESTRICTED STABLE
                                                      PHASE RETRIEVAL IN FOCK SPACE

                                                                 CYNTHIA BORTOLOTTO AND JOÃO P. G. RAMOS


                                                  Abstract. We give a short complex-analytic proof of a square-restricted form of local
                                                  stable phase retrieval at the Gaussian in one-dimensional Fock space. The main estimate
                                                  is a coercivity inequality for the map F 7→ F 2 :
arXiv:2608.26365v1 [math.CV] 26 Aug 2026




                                                                         ∥F 2 − F (0)2 ∥F 2 (C) ≲ inf ∥|F |2 − c∥F 2 (C) .
                                                                                                      c∈R

                                                  The proof uses a weighted derivative norm, two integrations by parts, and a weighted
                                                  Cauchy inequality. The proof has been completely verified in Lean with the aid of Large
                                                  Language Models.




                                                                                    1. Introduction
                                              Given a window function g ∈ L2 (R), we define the Short-time Fourier transform (STFT)
                                           of another f ∈ L2 (R) as
                                                                                  Z
                                                                    Vg f (x, ω) =   f (t)g(t − x)e−2πitω dt.
                                                                                          R
                                           This transform is important in several different contexts, from signal processing to x-ray
                                           imaging [10, 11, 16, 18], and it is the main object of study of this paper, as well as one of
                                           the cornerstone objects of modern time-frequency analysis. As one major mathematical
                                           property of such object, we highlight that it is an isometry up to the norm of the window,
                                                                          ∥Vg f ∥L2 (R2 ) = ∥g∥L2 (R) ∥f ∥L2 (R) ,
                                           which allows such operators to retain many of the metric properties of L2 (R), with the
                                           major advantage that one often gains regularity when applying it [11, Chapters 3 and 11].
                                              We shall be interested in the case of a specific window g, which perhaps best exemplifies
                                                                            2
                                           this: if we take g(t) = 21/4 e−πt to be the L2 -normalized Gaussian on R, the transform
                                           Vg f is called the Gabor transform, and it is intimately connected to the theory of entire
                                           functions on the plane. Indeed, one sees that the Gabor transform gives rise naturally to
                                           the so-called Bargmann transform
                                                                               Z
                                                                                                2 π 2
                                                                Bf (z) := 21/4
                                                                                  f (t) e2πtz−πt − 2 z dt,  z ∈ C,
                                                                                    R
                                           which satisfies the pointwise identity
                                                                                          π   2
                                                                  |Vg f (x, −ω)| = e− 2 |z| |Bf (z)|,             z = x + iω;
                                           see [6] and [11, Section 3.4], whose conventions we follow. This operator, as it turns out, is
                                           an isometric isomorphism between L2 (R) and the Bargmann-Fock space of entire functions
                                                                                                                  2
                                           on C, which is nothing but the space of entire F with C |F (z)|2 e−π|z| dm(z) < ∞, where
                                                                                                    R
                                                                                                  1
2                      CYNTHIA BORTOLOTTO AND JOÃO P. G. RAMOS


m denotes Lebesgue measure on C. Throughout this paper we work with the equivalent
normalization
                                                    Z
                      1 −|z|2
              dγ(z) := e      dm(z),   ∥H∥F 2 (C) := |H(z)|2 dγ(z),
                                           2
                      π                              C
F 2 (C)√denoting the space of entire functions of finite norm; the substitution H(w) :=
F (w/ π) is a unitary map from √   the space of the previous display onto F 2 (C). The
normalized   monomials en (z) = z / n! form an orthonormal basis of F 2 (C), so if H(z) =
                                 n
           n
P
   n≥0 an z , then                              X
                                  ∥H∥2F 2 (C) =   |an |2 n!.
                                               n≥0
We refer to [19] for a systematic treatment of Fock spaces.
   Such a window has, beyond its interesting analyticity properties, the practical advantage
of yielding a lot of spatial concentration, due to the rapid decay of the Gaussian. In
that regard, it is the perhaps most natural object in order to investigate one of the main
mathematical problems related to the applied theory of the Short-time Fourier transform,
which is that of phase retrieval. Phase retrieval asks whether an unknown function can be
recovered, up to a constant phase, from the modulus of its STFT; equivalently, the inverse
problem is to reconstruct f from the phaseless measurement |Vg f |, or from the intensity
|Vg f |2 . This problem is central in time–frequency analysis and also arises in ptychography,
where an unknown object is probed by translates of a window and only far-field intensities
are recorded.
   If stability is ignored, phase retrieval can often be understood through the ambiguity
function. With
                                   Af (x, ω) := eπixω Vf f (x, ω),
one has the fundamental identity
                             \
                            |V      2
                               g f | (ω, −x) = Af (x, ω)Ag(x, ω).

For a Gaussian window, Ag is a nonvanishing Gaussian, and this identity gives phase
retrieval. For Hermite windows, the ambiguity function is a Gaussian times a Laguerre
polynomial and therefore has zeros on finitely many circles. These zeros do not prevent
phase retrieval, but they do make quantitative stability more delicate, since a direct
inversion would require division by a function that degenerates along those circles. See
[12] for a systematic study of zeros of ambiguity functions and STFTs.
   On the complex-analytic side, the Hermite windows correspond to the scale of true
polyanalytic Fock spaces, of which F 2 (C) is the first member; see, for example, [1]. For
k ≥ 0, the kth space is generated by the true Hermite basis
                               min(k,n)      
                           1     X
                                           j k     n!
              Φk,n (z) = √             (−1)               z n−j z k−j , n ≥ 0.
                          k!n! j=0           j  (n −  j)!

The case k = 0 is exactly F 2 (C), whereas k ≥ 1 gives a genuinely polyanalytic space. The
companion stability theorem discussed below treats these Hermite settings at canonical
finite combinations of basis vectors. The present paper stays in the analytic case k = 0,
where the Cauchy–Riemann equations provide an additional identity that is unavailable in
the polyanalytic setting.
                     COMPLEX ANALYTIC PROOF OF SQUARE FOCK SPR                              3


   The fundamental stability question is whether the distance to the global-phase orbit can
be controlled by the distance between phaseless measurements. In the natural Hilbert-space
formulation, one seeks an estimate of the form
                      inf ∥f − λh∥L2 (R) ≤ C(f )∥|Vg f | − |Vg h|∥L2 (R2 ) .
                      |λ|=1

 More generally, if E is a closed subspace of some L2 (Ω, µ), one can ask whether the
modulus map is locally stable at f ∈ E:
                   inf ∥f − λh∥L2 (µ) ≤ C(f )∥|f | − |h|∥L2 (µ) ,       h ∈ E.          (1.1)
                  |λ|=1

This formulation serves as evidence as to why infinite-dimensional stability is subtle. Uni-
form Lipschitz bounds fail for phase retrieval by continuous frames in infinite-dimensional
spaces [8, 3], and even Gabor phase retrieval is severely ill-posed in its unrestricted form
[4]. More recently, it was shown that the local stability constant is infinite on a dense set
in broad classes of phase-retrieval spaces [5].
   These negative results, however, do not end the stability question, as they merely indicate
that one must identify the geometry of the instability and the points at which it can be
excluded. For Gaussian-window Gabor measurements, this led to quantitative estimates
in which the stability constant is governed by connectivity or Poincaré-type quantities of
the spectrogram [2, 13, 14, 17]. Such estimates make precise the principle that instability
is caused by separated components or by mass escaping to infinity. They generally use a
stronger first-order Sobolev measurement norm rather than the natural L2 norm. Thus
two basic issues remain visible: robustness under a change of window and stability in the
topology in which the forward STFT map is naturally bounded.
   In the Fock model the difficulty is purely metric: the modulus of an entire function
determines it up to a unimodular constant, so uniqueness is immediate and only the
quantitative question is left, and that question is genuinely infinite dimensional. The
preceding literature provides powerful conditional stability estimates, but it does not by
itself give local stability in the unmodified L2 measurement norm at a concrete nonzero
signal. The companion paper [7] is one of the first instances where a positive result which
makes use of the full geometry was shown. Indeed, it proves the global estimate
                   inf ∥F − λ∥F 2 (C) ≤ M ∥|F | − 1∥F 2 (C) ,       F ∈ F 2 (C),        (1.2)
                  |λ|=1

at the constant function. More generally, it establishes local stability for the canonical
Hermite windows at elements of the finite span of their basis vectors. Its proof proceeds
through an orthogonal reduction and a quantitative estimate for trigonometric polynomials
on circles, followed by frequency localization on annuli; see [7].
   The point of the present manuscript is to go a different way, providing a different
argument in a particular context. It is shorter and uses only complex analysis, but it
applies to a smaller, nonlinear but still infinite-dimensional class of competitors, namely
the class of squares
                          S := {F 2 : F is entire and F 2 ∈ F 2 (C)}.
Our main estimate is the following.
4                      CYNTHIA BORTOLOTTO AND JOÃO P. G. RAMOS


Theorem 1.1. There is an absolute constant C > 0 such that, for every polynomial F ,
                        ∥F 2 − F (0)2 ∥F 2 (C) ≤ C inf ∥|F |2 − c∥F 2 (C) .            (1.3)
                                                      c∈R

The same estimate holds for every entire F such that F 2 ∈ F 2 (C).
    The theorem immediately gives a square-restricted version of (1.2).
Corollary 1.2. There is an absolute constant C > 0 such that, for every entire F with
F 2 ∈ F 2 (C),
                       inf ∥F 2 − λ∥F 2 (C) ≤ C∥|F |2 − 1∥F 2 (C) .              (1.4)
                          |λ|=1

   The proof of Theorem 1.1 has three ingredients. First, on the subspace of Fock functions
vanishing at the origin, the Fock norm is equivalent to a weighted norm of the derivative,
enabling a direct replacement thereof. Second, the Cauchy–Riemann equations identify the
gradient of |F |2 with the derivative of F 2 . Finally, two integrations by parts reduce the
remaining expression to weighted L4 norms of F ′ and F ′′ ; a scale adapted Cauchy estimate
controls the latter by the former.
   The method is closely related in spirit to Gaussian energy methods. The classical
Gaussian logarithmic Sobolev inequality originates in work of Gross [15]; the complex-
analytic viewpoint particularly relevant here appears in Carlen’s work on Fisher information
and logarithmic Sobolev inequalities [9].
   Finally, the entire argument below has been formalized in Lean 4 and checked by its
kernel. Section 4 states what was verified, matches it step by step with the proof, and
records what the formalization required beyond the text.

LLM Usage. The ideas in this manuscript are completely devised by humans. A good part
of their writing was itself done by humans, but several large language models, such as GPT
5.5 and 5.6 Sol, as well as Claude Opus 4.8, 5 and Fable 5 have been used to punctually
expand computations, rewrite parts of sentences and proof check the manuscript.
   The main part where LLMs were instrumental was in the Lean formalization part.
Through extensive use of Claude Opus 4.8, 5, Fable 5, and GPT 5.5 and 5.6 Sol, the
manuscript has been thoroughly verified in Lean.
   In spite of the usage of LLMs, we have checked carefully all results in this manuscript,
including (and, as a matter of fact, most carefully of all) the Lean statements. We have
significantly changed parts where the LLMs edited the manuscript, and we have rewritten
several other parts to more closely match our intuition. We take full responsibility for the
contents of this paper.

                                      2. Main argument
    Throughout the proof, m denotes Lebesgue measure on C. For k ≥ 0, write
                                                        2
                                               1 e−|z|
                                  dγk (z) :=                  dm(z),
                                               π (1 + |z|2 )k
Thus dγ = dγ0 . We first prove that, when H(0) = 0, the Fock norm of H is equivalent to
a weighted L2 -norm of H ′ .
                     COMPLEX ANALYTIC PROOF OF SQUARE FOCK SPR                                     5


Lemma 2.1. There are absolute constants 0 < c ≤ C < ∞ such that, whenever H ∈ F 2 (C)
and H(0) = 0,
                                 Z
                   c∥H∥F 2 (C) ≤ |H ′ (z)|2 dγ1 (z) ≤ C∥H∥2F 2 (C) .
                        2
                                                                               (2.1)
                                         C
                                                                                            n . Note
                                                                             P
Proof. Since H(0) = 0, the Taylor expansion of H has the form H(z) =             n≥1 an z
that
                                          X
                            H ′ (reiθ ) =   nan rn−1 ei(n−1)θ .
                                                 n≥1

Changing to polar coordinates and using the orthogonality of θ 7→ eikθ in the angular
integral, we obtain
                                                                           2
                             1 ∞ 2π X                                  e−r
               Z               Z Z
                    ′ 2
                  |H | dγ1 =              |      nan rn−1 ei(n−1)θ |2        r dθ dr
                C            π 0      0                               1 + r2
                                            n≥1
                                             Z ∞ 2n−1 −r2
                              X
                                    2     2       r      e
                           =2     n |an |                     dr
                                               0     1 + r2
                              n≥1
                             X
                           =    n2 |an |2 κn ,
                              n≥1

where
                                               |z|2(n−1)
                                             Z
                                    κn :=              2
                                                         dγ(z).
                                             C 1 + |z|
Here the derivative series is uniformly convergent on each circle, and Tonelli’s theorem
justifies the interchange with the resulting nonnegative radial series. Observe that it suffices
to prove that
                                     n2 κn
                                             ∼ 1,     n ≥ 1.                               (2.2)
                                       n!
Indeed, if (2.2) holds, then, since ∥H∥2F 2 (C) = n≥1 |an |2 n!, the identity above can be
                                                     P

compared term by term, and summing over n gives
                                   Z
                                      |H ′ |2 dγ1 ∼ ∥H∥2F 2 (C) .
                                     C
                                                                                R ∞ −(1+|z|2 )s
  Therefore,  we only need to prove (2.2). To this end, using (1 + |z|2 )−1 =    0 e            ds
and C |z|2j dγ = j!, we obtain
   R

                                           Z ∞
                                 n 2 κn            e−s
                                        =n               ds.                                   (2.3)
                                   n!       0   (1 + s)n
For the lower bound in (2.2), we use (2.3) and restrict the integral to 0 ≤ s ≤ 1/n. On
this interval, we use that (1 + s)−n ≥ e−ns , and therefore
                           Z ∞
                                   e−s
                                                 Z 1/n
                         n              n
                                          ds ≥ n       e−2 ds = e−2 .
                            0   (1 + s)           0
6                       CYNTHIA BORTOLOTTO AND JOÃO P. G. RAMOS


For the upper bound, split the integral at s = 1. On 0 ≤ s ≤ 1 we use that log(1 + s) ≥ s/2,
and on s ≥ 1 we have (1 + s)−n ≤ 2−n . Hence
                     Z ∞                                         Z ∞
                            e−s
                                          Z 1
                                                −ns/2         −n
                  n               ds ≤ n      e       ds + n2        e−s ds
                      0  (1 + s)n          0                      1
                                             1
                                     ≤2+         < 3,
                                             2e
finishing the proof.                                                                      □
    We will also use the following elementary weighted Cauchy estimate.
Lemma 2.2. There is an absolute constant A such that every polynomial F satisfies
                             Z                     Z
                                   |F | dγ4 ≤ A |F ′ |4 dγ2 ,
                                      ′′ 4
                                                                                 (2.4)
                                C                   C
                        Z                          Z
                           |F ′ |2 |F ′′ |2 dγ3 ≤ A |F ′ |4 dγ2 .                (2.5)
                               C                             C
Proof. We first prove (2.4). The Cauchy integral formula applied to F ′ gives
                                            Z 2π
                                ′′       1
                            |F (z)| ≤            |F ′ (z + reiθ )| dθ,
                                       2πr 0
and Hölder’s inequality yields, for every r > 0,
                                            Z 2π
                             ′′          1
                          |F (z)| ≤4
                                                  |F ′ (z + reiθ )|4 dθ.             (2.6)
                                       2πr4 0
  To compute the integral in (2.4), we split the plane into the regions {z : |z| ≤ 2} and
{z : |z| > 2}.
  Note that if |z| ≤ 2, then
                                        2                           iθ 2
                                 e−|z|             e−|z+e |
                                           ≤ C1                     .
                              (1 + |z|2 )4      (1 + |z + eiθ |2 )2
Therefore, using (2.6) with r = 1, Tonelli’s theorem, and translation by eiθ , we obtain
                                                                                2
                                                                          e−|z|
       Z                               Z 2π Z
                  ′′   4           1                    ′        iθ 4
                |F (z)| dγ4 (z) ≤ 2                   |F (z + e )|                  dm(z) dθ
        {|z|≤2}                   2π 0       {|z|≤2}                   (1 + |z|2 )4
                                                                             2
                                                                        e−|ζ|
                                       Z 2π Z
                                  C1
                                ≤ 2                       |F ′ (ζ)|4              dm(ζ) dθ
                                  2π 0       {|ζ−eiθ |≤2}            (1 + |ζ|2 )2
                                     Z
                                ≤ C1 |F ′ |4 dγ2 .
                                            C
   We now consider {z : |z| > 2}. Here a fixed radius would not give a uniform comparison
of the Gaussian weights, so we choose rz = |z|−1 . For fixed θ, set
                                                            eiθ
                                            Φθ (z) := z +       .
                                                            |z|
Then (2.6) becomes
                                                  Z 2π
                               ′′      |z|4
                                    4
                             |F (z)| ≤                   |F ′ (Φθ (z))|4 dθ.
                                        2π         0
                       COMPLEX ANALYTIC PROOF OF SQUARE FOCK SPR                                      7


   Before integrating, we compare the weight at z with the weight at Φθ (z). The choice
rz = |z|−1 ensures that the difference between |Φθ (z)|2 and |z|2 is uniformly bounded. In
particular,
                                             9
                     |Φθ (z)|2 − |z|2 ≤ ,             1 + |Φθ (z)|2 ≤ 2(1 + |z|2 ),
                                             4
and therefore
                                           2                             2
                                |z|4 e−|z|           9/4      e−|Φθ (z)|
                                               ≤ 4e                            .
                               (1 + |z|2 )4               (1 + |Φθ (z)|2 )2
   Multiplying the pointwise estimate by the density of dγ4 , integrating, and using the
inequality above, we obtain
                                                                                       2
                                                                            |z|4 e−|z|
     Z                                 Z 2π Z
                ′′                 1
                     4
              |F (z)| dγ4 (z) ≤ 2                        |F ′ (Φθ (z))|4                 dm(z) dθ
      {|z|>2}                     2π 0          {|z|>2}                    (1 + |z|2 )4
                                                                                            2
                                  2e9/4 2π                                       e−|Φθ (z)|
                                         Z      Z
                                                               ′           4
                              ≤                            |F (Φθ (z))|                        dm(z) dθ.
                                   π2 0           {|z|>2}                    (1 + |Φθ (z)|2 )2
  To apply the change-of-variables formula to Φθ , we check that this map is one-to-one
and that its Jacobian determinant is bounded away from zero. The real differential of Φθ is
                                                          eiθ
                                   DΦθ (z)[h] = h −           Re(zh),
                                                         |z|3
and hence
                                                   Re(e−iθ z)     1  3
                          det DΦθ (z) = 1 −              3
                                                              ≥1− 2 ≥ .
                                                     |z|         |z| 4
Moreover, for |z| > 2 and |z ′ | > 2,
                                                                    1   1
                             |Φθ (z) − Φθ (z ′ )| ≥ |z − z ′ | −      − ′
                                                                   |z| |z |
                                                   3
                                                ≥ |z − z ′ |.
                                                   4
Thus Φθ is one-to-one on {z : |z| > 2}. Since det DΦθ (z) ≥ 3/4, the change-of-variables
formula gives
                                              2                                       2
                                   e−|Φθ (z)|                                    e−|ζ|
       Z                                                      Z
                   ′          4                             4       ′      4
                 |F (Φθ (z))|                     dm(z) ≤        |F   (ζ)|                dm(ζ)
         {|z|>2}                (1 + |Φθ (z)|2 )2           3 C              (1 + |ζ|2 )2
                                                                Z
                                                            4π
                                                        =          |F ′ |4 dγ2 .
                                                             3 C
Consequently,                Z                                 Z
                                          ′′   4
                                        |F (z)| dγ4 (z) ≤ C2           |F ′ |4 dγ2 ,
                              {|z|>2}                              C
and putting the two estimates together, we get
                   Z                Z
                      |F | dγ4 ≤ A4 |F ′ |4 dγ2 ,
                         ′′ 4
                                                                   A4 := C1 + C2 ,
                         C                     C
where A4 is an absolute constant. This proves (2.4).
8                           CYNTHIA BORTOLOTTO AND JOÃO P. G. RAMOS


    To prove (2.5), we just apply Cauchy-Schwarz and get
                                                             !                        !
            Z
                                1
                                   Z                −|z|2 /2                −|z|2 /2
                 ′ 2  ′′ 2                   ′ 2e                    ′′ 2 e
               |F | |F | dγ3 =            |F |                   |F |                   dm(z)
             C                  π C               1 + |z|2               (1 + |z|2 )2
                               Z                  1/2 Z                1/2
                                         ′ 4                      ′′ 4
                             ≤        |F | dγ2                 |F | dγ4
                                    C                        C
                                       Z
                                  1/2
                             ≤ A4          |F ′ |4 dγ2 .
                                 C
                      1/2
Taking A := max{A4 , A4 } proves both estimates.                                                  □
    We are now ready to prove Theorem 1.1.
Proof of Theorem 1.1. Let F be a polynomial and c ∈ R. The Cauchy–Riemann equations
give
                    ∂x |F |2 = 2 Re(F ′ F ), ∂y |F |2 = −2 Im(F ′ F ),
and consequently, we have the pointwise identity
                                 |∇(|F |2 )|2 = 4|F |2 |F ′ |2 = |(F 2 )′ |2 .                  (2.7)
Since F 2 − F (0)2 vanishes at the origin, applying Lemma 2.1 to F 2 − F (0)2 and then using
(2.7) gives                                        Z
                             ∥F 2 − F (0)2 ∥2F 2 (C) ≤ C         |∇(|F |2 )|2 dγ1 .
                                                             C
To bound the integral above, fix c ∈ R and let
                                                                 2
                                            1 e−|z|
                                          w1 (z) :=    .
                                            π 1 + |z|2
Subtracting c does not change the gradient, so
                  Z                    Z
                           2 2
                    |∇(|F | )| w1 dm =    ∇(|F |2 − c) · ∇(|F |2 )w1 dm.
                        C                          C
Integrating by parts once gives
                 Z                        Z
                    |∇(|F |2 )|2 w1 dm = − (|F |2 − c) ∆(|F |2 ) w1 dm
                  C
                                          ZC
                                         − (|F |2 − c) ∇(|F |2 ) · ∇w1 dm.
                                                    C
To treat the second integral, first note that
                                                1
                          (|F |2 − c)∇(|F |2 ) = ∇ (|F |2 − c)2 .
                                                                
                                                2
We use this identity to rewrite the integral as
             Z                                      Z
                    2            2                1
                                                       ∇ (|F |2 − c)2 · ∇w1 dm.
                                                                      
          − (|F | − c) ∇(|F | ) · ∇w1 dm = −
              C                                   2 C
We now integrate by parts to obtain
                   Z                                  Z
                 1             2     2              1
                                                        (|F |2 − c)2 ∆w1 dm.
                                       
               −      ∇ (|F | − c) · ∇w1 dm =
                 2 C                                2 C
                     COMPLEX ANALYTIC PROOF OF SQUARE FOCK SPR                                     9


Combining the two identities, we obtain
  Z                        Z                            Z
            2 2                  2         2          1
     |∇(|F | )| w1 dm = − (|F | − c) ∆(|F | ) w1 dm +     (|F |2 − c)2 ∆w1 dm.                  (2.8)
   C                        C                         2 C
The boundary terms vanish because F is a polynomial and w1 has Gaussian decay.
  The explicit form of w1 gives
                                                                        2
                                                         e−|z|
                                           |∆w1 (z)| ≤ C       ,
                                                           π
and therefore the last term in (2.8) is bounded by C∥|F |2 − c∥2F 2 (C) .
  For the first term on the right-hand side of (2.8), Cauchy–Schwarz yields
  Z                                                                       Z
         2           2                 2           1/2
                                                                                     2
    (|F | − c) ∆(|F | ) w1 dm ≤ ∥|F | − c∥F 2 (C) J ,      where J :=       ∆(|F |2 ) dγ2 .
   C                                                                                       C

Therefore, it remains to show that J ≲ ∥|F |2 − c∥2F 2 (C) to conclude the proof. Put
                                                                    2
                                                      1 e−|z|
                                       w2 (z) :=                     ,
                                                      π (1 + |z|2 )2
and observe that, since ∆(|F |2 − c) = ∆(|F |2 ), two further integrations by parts give
                            Z
                        J = (|F |2 − c) ∆ ∆(|F |2 )w2 dm
                                                        

                            ZC
                          = (|F |2 − c) ∆2 (|F |2 ) w2 dm
                             C
                                Z
                           + 2 (|F |2 − c) ∇ ∆(|F |2 ) · ∇w2 dm
                                                         

                              Z C
                           + (|F |2 − c) ∆(|F |2 ) ∆w2 dm.                              (2.9)
                                   C

Note that we can bound the derivatives of w2 by
                                              2                                        2
                                  e−|z|                                        e−|z|
                |∇w2 (z)| ≤ C                 ,                |∆w2 (z)| ≤ C              .
                              π(1 + |z|2 )3/2                                π(1 + |z|2 )
For any holomorphic function G, the Cauchy–Riemann equations give ∆(|G|2 ) = 4|G′ |2 .
Applying this identity first to G = F and then to G = F ′ gives
                  ∆(|F |2 ) = 4|F ′ |2 ,          ∆2 (|F |2 ) = 4∆(|F ′ |2 ) = 16|F ′′ |2 .    (2.10)
Moreover, applying the pointwise identity (2.7) with F ′ in place of F gives
                        |∇ ∆(|F |2 ) | = 4|∇|F ′ |2 | = 8|F ′ ||F ′′ |.
                                    

The first identity in (2.10) also shows that
                                                     Z
                                           J = 16          |F ′ |4 dγ2 .                       (2.11)
                                                       C
10                       CYNTHIA BORTOLOTTO AND JOÃO P. G. RAMOS


   We now estimate separately the three integrals on the right-hand side of (2.9). For the
first integral, we use the second identity in (2.10). Since w2 dm = dγ2 and the density of
dγ2 is the geometric mean of the densities of dγ and dγ4 , Cauchy–Schwarz gives
             Z                                                  Z          1/2
                     2      2     2                2                 ′′ 4
                (|F | − c) ∆ (|F | ) w2 dm ≤ C∥|F | − c∥F 2 (C)    |F | dγ4      .
                                                                            C

  For the second integral, we use the identity |∇(∆(|F |2 ))| = 8|F ′ ||F ′′ | together with the
bound for |∇w2 |. The density that occurs is the geometric mean of the densities of dγ and
dγ3 , so Cauchy–Schwarz gives
                                                                                  2
                                                                           e−|z|
       Z                                      Z
     2 (|F | − c) ∇ ∆(|F | ) · ∇w2 dm ≤ C ||F |2 − c| |F ′ ||F ′′ |
            2              2
                             
                                                                                         dm(z)
                                                C                   π(1 + |z|2 )3/2
                                                               Z                       1/2
                                         ≤ C∥|F |2 − c∥F 2 (C)     |F ′ |2 |F ′′ |2 dγ3      .
                                                                             C

   For the third integral, we use the first identity in (2.10) and the bound for |∆w2 |. This
time the density is the geometric mean of the densities of dγ and dγ2 , and hence
                                                                           2
                                                                     e−|z|
           Z                                    Z
             (|F | − c) ∆(|F | ) ∆w2 dm ≤ C ||F |2 − c| |F ′ |2
                  2           2
                                                                               dm(z)
                                                  C               π(1 + |z|2 )
                                                                Z            1/2
                                                     2                 ′ 4
                                           ≤ C∥|F | − c∥F 2 (C)      |F | dγ2      .
                                                                            C

  By (2.4) and (2.5), the last factors in the first two estimates are also bounded by a
                                   1/2
constant multiple of C |F ′ |4 dγ2
                     R
                                        . Summing the three estimates in (2.9), we obtain
                                                Z            1/2
                                      2                ′ 4
                        J ≤ C∥|F | − c∥F 2 (C)       |F | dγ2      .
                                                             C

                                ′ 4
                                         1/2
                                                = J 1/2 /4. Therefore,
                        R
Finally, (2.11) gives       C |F | dγ2

                                     J ≤ C∥|F |2 − c∥F 2 (C) J 1/2 .

If J = 0 there is nothing to prove; otherwise division by J 1/2 gives
                                          J ≤ C∥|F |2 − c∥2F 2 (C) .
Returning to (2.8) and using the estimates for its two terms, we obtain
               Z
                  |∇(|F |2 )|2 dγ1 ≤ C∥|F |2 − c∥2F 2 (C) + ∥|F |2 − c∥F 2 (C) J 1/2
                   C
                                         ≤ C∥|F |2 − c∥2F 2 (C) .
Combining this estimate with the initial application of Lemma 2.1 gives
                              ∥F 2 − F (0)2 ∥2F 2 (C) ≤ C∥|F |2 − c∥2F 2 (C) ,
for every polynomial F . Taking square roots and then the infimum over c ∈ R proves the
polynomial case of Theorem 1.1.
                       COMPLEX ANALYTIC PROOF OF SQUARE FOCK SPR                                    11

                                                                                                        n
                                                                                         P
  We finish the extension to the stated entire-function class. Write F (z) =                 n≥0 an z
and F 2 (z) = n≥0 bn z n . For 0 ≤ r < 1, set
             P
                                                         X
                       Fr (z) := F (rz),     Pr,N (z) :=   an r n z n .
                                                                  n<N
Since                                                    X
                                  Fr2 (z) = F 2 (rz) =         bn rn z n ,
                                                         n≥0
the coefficient formula for the Fock norm gives
                                                  X
                           ∥Fr2 − F 2 ∥2F 2 (C) =   |bn |2 (1 − rn )2 n!.
                                                  n≥0

Since n≥0 |bn |2 n! = ∥F 2 ∥2F 2 (C) < ∞ and (1 − rn )2 ≤ 1, dominated convergence shows
        P

that this expression tends to zero as r ↑ 1.
  We next fix 0 < r < 1 and prove that Pr,N → Fr in L4 (dγ). For each circle of radius
ρ ≥ 0, Parseval’s identity and Cauchy–Schwarz with respect to the normalized angular
measure give
                                      2
                                             Z 2π                    2
                        |an |2 ρ2n  = 1
                         X
                                                               iθ 2
                                                        |F (ρe )| dθ
                                              2π 0
                         n≥0
                                               Z 2π
                                             1
                                          ≤           |F (ρeiθ )|4 dθ
                                            2π 0
                                            X
                                          =    |bn |2 ρ2n .
                                                 n≥0

Therefore, applying Cauchy–Schwarz to the Taylor tail, we get
                                                2                  2
                                           X          X
                  |Pr,N (z) − Fr (z)|4 ≤    r2n       |an |2 |z|2n 
                                               n≥N                n≥N
                                                         2
                                                 X             X
                                          ≤           r2n         |bn |2 |z|2n .
                                               n≥N             n≥0

Integrating this inequality with respect to dγ and using C |z|2n dγ(z) = n!, we obtain
                                                           R
                                        2                       2
                                 X          X                X
          ∥Pr,N − Fr ∥4 4   ≤
                        L (dγ)       r2n      |bn |2 n! =    r2n  ∥F 2 ∥2 2 .     F (C)
                                    n≥N          n≥0                   n≥N

The geometric tail tends to zero as N → ∞, proving that Pr,N → Fr in L4 (dγ). Finally,
the factorization
                            2
                          Pr,N − Fr2 = (Pr,N − Fr )(Pr,N + Fr )
and Cauchy–Schwarz give
                 2
               ∥Pr,N − Fr2 ∥F 2 (C) ≤ ∥Pr,N − Fr ∥L4 (dγ) ∥Pr,N + Fr ∥L4 (dγ) −→ 0.
12                       CYNTHIA BORTOLOTTO AND JOÃO P. G. RAMOS


Here the second factor remains bounded because Pr,N → Fr in L4 (dγ).
  Now take rk = k/(k + 1) and choose Nk ≥ 1 so that
                                                              1
                                   ∥Pr2k ,Nk − Fr2k ∥F 2 (C) < .
                                                              k
Since Frk → F in F (C), the triangle inequality gives Pr2k ,Nk → F 2 in F 2 (C). Moreover,
          2      2      2

Prk ,Nk (0) = F (0) for every k. For any fixed c ∈ R, the polynomial estimate therefore gives
                       ∥Pr2k ,Nk − F (0)2 ∥F 2 (C) ≤ C∥|Prk ,Nk |2 − c∥F 2 (C) .
The pointwise inequality |Prk ,Nk |2 − |F |2 ≤ |Pr2k ,Nk − F 2 | shows that we may pass to the
limit and obtain
                        ∥F 2 − F (0)2 ∥F 2 (C) ≤ C∥|F |2 − c∥F 2 (C) .
Taking the infimum over c ∈ R proves the theorem.                                           □
2.1. Proof of the square-restricted stability statement.
Proof of Corollary 1.2. Theorem 1.1 with c = 1 gives
                            ∥F 2 − F (0)2 ∥F 2 (C) ≤ C∥|F |2 − 1∥F 2 (C) .
Since ||F |2 − |F (0)|2 | ≤ |F 2 − F (0)2 | pointwise and dγ is a probability measure,
     |F (0)|2 − 1 ≤ ∥|F |2 − |F (0)|2 ∥F 2 (C) + ∥|F |2 − 1∥F 2 (C) ≤ (C + 1)∥|F |2 − 1∥F 2 (C) .
If F (0) ̸= 0, choose λ = F (0)2 /|F (0)|2 ; if F (0) = 0, choose any unimodular λ. In both
cases,
                                |F (0)2 − λ| = |F (0)|2 − 1 .
Consequently,
      ∥F 2 − λ∥F 2 (C) ≤ ∥F 2 − F (0)2 ∥F 2 (C) + |F (0)2 − λ| ≤ (2C + 1)∥|F |2 − 1∥F 2 (C) ,
which proves Corollary 1.2.                                                                         □

                                          3. Comments
3.1. Comparison to [7]. The estimate in Corollary 1.2 has the same natural Fock-space
topology and the same global form as (1.2). Its scope is smaller: the competitor is required
to be a square. In particular, the argument does not prove stability for an arbitrary
G ∈ F 2 (C), and it does not address the higher Hermite windows or the true polyanalytic
Fock spaces considered in [7].
   The gain is conceptual and cosmetic, but useful. The proof is entirely complex analytic
after the Bargmann–Fock reduction. It uses no circle estimate for trigonometric polynomials,
no decomposition into frequency blocks, and no annular mass-concentration argument.
The price of this simplification is precisely the identity
                                       |∇|F |2 |2 = |(F 2 )′ |2 ,
which has no counterpart for a general competitor and is not stable under the passage to
polyanalytic functions.
   The two proof architectures can therefore be summarized as follows. The full theorem
first removes the phase direction by an abstract orthogonal reduction and then exploits
polar Fourier structure. The present argument removes the constant mode by the weighted
                     COMPLEX ANALYTIC PROOF OF SQUARE FOCK SPR                            13


derivative equivalence, converts the modulus defect into a gradient energy, and closes the
estimate by Cauchy integral bounds. The latter route is shorter, while the former route
has the substantially broader conclusion.
3.2. The Gaussian energy viewpoint and Carlen’s work. There is a natural connec-
tion with the Gaussian energy methods appearing in Carlen’s work on Fisher information
and logarithmic Sobolev inequalities [9]. Both arguments exploit the Gaussian measure,
an integration-by-parts identity, and the fact that complex analyticity turns derivatives of
a modulus into holomorphic derivatives. In the present proof, this mechanism appears in
the pair of identities
                         ∆|F |2 = 4|F ′ |2 ,   |∇|F |2 |2 = |(F 2 )′ |2 .
They play the role of a particularly rigid carré-du-champ structure for the density |F |2 .
   In spite of the similarities, Carlen’s arguments are designed around entropy, Fisher
information, and sharp Gaussian inequalities, whereas the present argument is a coercivity
estimate for the nonlinear squaring map. The auxiliary factor (1 + |z|2 )−1 is inserted to
make differentiation coercive away from the constant mode, and the weighted Cauchy
lemma is the genuinely complex-analytic step that closes the estimate.

                               4. The Lean verification
  Every result of this note has been formalized in Lean 4 and checked by its kernel
against Mathlib: Lemma 2.1, Lemma 2.2, Theorem 1.1 in both its polynomial and its
entire-function form, and Corollary 1.2. The library builds with Lean v4.30.0 against
Mathlib v4.30.0; it contains no sorry, no admit and no project axiom, and #print axioms
on each of the declarations listed below reports only propext, Classical.choice and
Quot.sound. The trusted base is therefore Lean’s kernel together with the pinned Mathlib;
nothing in this note is verified relative to an unproved assumption. All Lean statements
reproduced or cited in this section were also read and checked by a human against the
corresponding mathematical statements in the note. The code is available at https:
//github.com/cynthiabort/SPR-near-Gaussian.
4.1. The verified statement. A formalization is only as informative as the statement it
proves, so we reproduce the definitions and the two theorems that carry the mathematical
content. At the level of statements these depend on Mathlib alone, and reading them is
enough to check that what was verified is what was claimed.
   The measure is the normalized Gaussian dγ of the introduction, realized as a density
against planar Lebesgue measure:
def gaussianDensity (z : C) : R≥0∞ :=
  ENNReal.ofReal (Real.exp (-∥z∥ ^ 2) / Real.pi)

def gaussianMeasure : Measure C :=
  volume.withDensity gaussianDensity
The Fock norm is not introduced as a norm on an abstract space of entire functions,
but rather, in this context itPis interpreted as the Gaussian L2 norm, so that the coef-
ficient identity ∥H∥2F 2 (C) = n |an |2 n! used throughout Section 2 is a proved theorem
(fock norm sq eq coeff sum) and not a definition.
14                    CYNTHIA BORTOLOTTO AND JOÃO P. G. RAMOS


def functionFockNorm (f : C → C) : R :=
  lpNorm f 2 gaussianMeasure

def functionCenteredSquare (F : C → C) : C → C :=
  fun z 7→ F z ^ 2 - F 0 ^ 2

def functionDistanceToConstant (F : C → C) (c : R) : R :=
  lpNorm (fun z 7→ Complex.normSq (F z) - c) 2 gaussianMeasure

def functionDistanceToUnimodularConstants (G : C → C) : R :=
  sInf {d : R | ∃ phase : C, ∥phase∥ = 1 ∧
    d = functionFockNorm (fun z 7→ G z - phase)}
Here Complex.normSq (F z) is |F (z)|2 and lpNorm f 2 gaussianMeasure is ∥f ∥L2 (dγ) , so
functionDistanceToConstant F c is ∥|F |2 − c∥F 2 (C) . The last definition is the infimum
appearing in (1.4), taken literally as the infimum of a set of real numbers rather than
replaced by a chosen minimizing phase.
  Theorem 1.1 for entire F and Corollary 1.2 are then the following two statements.
theorem square_coercivity_for_entire :
    ∃ C : R, 0 < C ∧ ∀ (F : C → C), Differentiable C F →
      MemLp (fun z 7→ F z ^ 2) 2 gaussianMeasure →
      functionFockNorm
             d         (functionCenteredSquare F) ≤
        C * ( c : R, functionDistanceToConstant F c)

theorem stable_phase_retrieval_for_squares :
    ∃ C_square : R, 0 < C_square ∧
      ∀ (F : C → C), Differentiable C F →
        MemLp (fun z 7→ F z ^ 2) 2 gaussianMeasure →
        functionDistanceToUnimodularConstants (fun z 7→ F z ^ 2) ≤
          C_square * functionDistanceToConstant F 1
In these statements Differentiable C F says that F is entire, MemLp (fun z 7→ F z ^ 2)
2 gaussianMeasure says that F 2 ∈ F 2 (C), and
                                               d
                                                  c : R is the infimum over all real c.
The constant is quantified before F , hence absolute, and neither statement carries any
hypothesis beyond those of Theorem 1.1 and Corollary 1.2.
4.2. Correspondence with the proof. The table below records the statements from
Section 2 whose correspondence with one or more Lean declarations was checked by a
human. For every entry, the hypotheses, conclusion, constants, and cited Lean declaration
were compared directly with the mathematical statement in the note.

                                 Acknowledgements
  J. P. G. R. was supported by the FCT through project SHADE (project 2023.17881.ICDT,
DOI 10.54499 / 2023.17881.ICDT), by FAPERJ through the JCNE grant no. SEI-260003 /
020475/2025, and by Instituto Serrapilheira through grant Serra-R-2510-59765.
  We would furthermore like to express our gratitude towards Jaume de Dios Pont, Mitchell
Taylor, André Guerra, and Francisco Ganacim for several discussions on the strategy to
prove the theorem, the lean formalization and the overall structure of the manuscript.
                        COMPLEX ANALYTIC PROOF OF SQUARE FOCK SPR                                         15

 Result    in this note               Lean declaration
        2k
 R
   C
     |z|   dγ = k!                    complex gaussian monomial moment
 ∥H∥2F 2 (C) = n |an |2 n!
                 P
                                      fock norm sq eq coeff sum
 (2.2), (2.3)                         weighted derivative coefficient
                                      weighted derivative coefficient bounds
 Lemma 2.1                            entire weighted derivative equivalence integral
 (2.6)                                pointwise cauchy bound
 weight comparison under the two inner weight shift, outer weight shift
 shifts
 injectivity/diffeomorphism of Φθ outer shift diffeomorph
 Lemma 2.2                            weighted cauchy
 gradient identity in (2.7) and first gradient normSq polynomial
 identity in (2.10)                   laplacian normSq polynomial
 (2.8)                                weighted integration by parts
 bounds on ∆w1 , on ∇w2 and ∆w2 weight laplacian bound
                                      weight two derivative bounds
 J ≲ ∥|F |2 − c∥2F 2 (C)              laplacian energy bound
 Theorem 1.1, polynomial case         squaring against every constant, squaring
 construction of Pr,N                 entire fock square polynomial approximation
 Theorem 1.1, entire case             square coercivity for entire
 Corollary 1.2                        stable phase retrieval for squares



                                              References
 [1] L. D. Abreu and H. G. Feichtinger, Function spaces of polyanalytic functions, in Harmonic and complex
     analysis and its applications, Trends Math., Birkhäuser/Springer, Cham, 2014, pp. 1–38.
 [2] R. Alaifari, I. Daubechies, P. Grohs, and R. Yin, Stable phase retrieval in infinite dimensions, Found.
     Comput. Math. 19 (2019), no. 4, 869–900.
 [3] R. Alaifari and P. Grohs, Phase retrieval in the general setting of continuous frames for Banach spaces,
     SIAM J. Math. Anal. 49 (2017), no. 3, 1895–1911.
 [4] R. Alaifari and P. Grohs, Gabor phase retrieval is severely ill-posed, Appl. Comput. Harmon. Anal. 50
     (2021), 401–419.
 [5] W. Alharbi, S. Alshabhi, D. Freeman, and D. Ghoreishi, Locality and stability for phase retrieval,
     Sampl. Theory Signal Process. Data Anal. 22 (2024), Paper No. 10, 16 pp.
 [6] V. Bargmann, On a Hilbert space of analytic functions and an associated integral transform, Comm.
     Pure Appl. Math. 14 (1961), 187–214.
 [7] S. Bertolini, J. de Dios Pont, B. Pineau, J. P. G. Ramos, and M. A. Taylor, L2 -stability for STFT
     phase retrieval, manuscript, 2026.
 [8] J. Cahill, P. G. Casazza, and I. Daubechies, Phase retrieval in infinite-dimensional Hilbert spaces,
     Trans. Amer. Math. Soc. Ser. B 3 (2016), 63–76.
 [9] E. A. Carlen, Superadditivity of Fisher’s information and logarithmic Sobolev inequalities, J. Funct.
     Anal. 101 (1991), no. 1, 194–211.
[10] G. B. Folland, Harmonic analysis in phase space, Annals of Mathematics Studies 122, Princeton
     University Press, Princeton, NJ, 1989.
[11] K. Gröchenig, Foundations of time-frequency analysis, Applied and Numerical Harmonic Analysis,
     Birkhäuser, Boston, 2001.
[12] K. Gröchenig, P. Jaming, and E. Malinnikova, Zeros of the Wigner distribution and the short-time
     Fourier transform, Rev. Mat. Complut. 33 (2020), no. 3, 723–744.
[13] P. Grohs and M. Rathmair, Stable Gabor phase retrieval and spectral clustering, Comm. Pure Appl.
     Math. 72 (2019), no. 5, 981–1043.
16                        CYNTHIA BORTOLOTTO AND JOÃO P. G. RAMOS


[14] P. Grohs and M. Rathmair, Stable Gabor phase retrieval for multivariate functions, J. Eur. Math. Soc.
     (JEMS) 24 (2022), no. 5, 1593–1615.
[15] L. Gross, Logarithmic Sobolev inequalities, Amer. J. Math. 97 (1975), no. 4, 1061–1083.
[16] F. Pfeiffer, X-ray ptychography, Nature Photonics 12 (2018), 9–17.
[17] M. Rathmair, Stable STFT phase retrieval and Poincaré inequalities, Int. Math. Res. Not. IMRN
     (2024), no. 22, 14094–14114.
[18] J. M. Rodenburg, Ptychography and related diffractive imaging methods, Adv. Imaging Electron Phys.
     150 (2008), 87–184.
[19] K. Zhu, Analysis on Fock spaces, Graduate Texts in Mathematics 263, Springer, New York, 2012.
