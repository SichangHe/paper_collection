                                         A Calculus for Units of Measure with Conversion
                                         ERIC ALLEN, Two Sigma Investments, LP, USA
                                         Programs that compute with physical quantities often need to convert between units of measurement, and
                                         as the Mars Climate Orbiter showed, these conversions can be a rich source of errors. Meanwhile, typed
                                         unit calculi, our most rigorous formalisms for checking physical units in a program, have excluded unit
                                         conversions. Through this exclusion, they have established a powerful property: well-typed programs are
                                         invariant under rescaling (no program can depend on how big a meter is). But losing the ability to convert
                                         between units is a significant cost. In contrast, practical languages provide conversion but no invariance
arXiv:2609.38242v1 [cs.PL] 29 Sep 2026




                                         theorem. We present Λ𝑆 , a typed lambda calculus with conversion, quantification over units and dimensions,
                                         and vectors and linear maps with per-component units, and we determine exactly how much invariance
                                         survives conversion. For terms without unit constants we prove two abstraction theorems: (i) a convert-free
                                         term is invariant under every rescaling; (ii) a term with conversions is invariant under every rescaling that
                                         scales all units of one dimension by the same factor. The condition in (ii) cannot be weakened: under any
                                         other rescaling, some conversion of a nonzero value is not invariant.
                                            For first-order programs, a verified decision procedure returns one of three verdicts: it certifies that no error
                                         in the declared conversion factors can change the program’s answer, names the accumulated ratio through
                                         which such an error would scale it, or declines. A verified checker decides whether unit declarations are
                                         consistent and determine every conversion factor, and extracts each factor exactly. We also prove adequacy,
                                         erasure, and the 𝑛-variable Pi theorem of dimensional analysis with conversion. Every theorem is mechanized
                                         in Lean 4, and the evaluator compiles to a native binary.
                                         Additional Key Words and Phrases: units of measure, conversion, parametricity, coherence, dimensional anal-
                                         ysis, mechanized metatheory, Lean

                                         1 Introduction
                                         Programs that manipulate physical quantities must eventually convert between units, and con-
                                         version is where the errors occur. The loss of the Mars Climate Orbiter was traced to ground
                                         software that reported thruster impulse in pound-seconds where its interface specified newton-
                                         seconds [Mars Climate Orbiter Mishap Investigation Board 1999]; the enduring popularity of
                                         units-of-measure extensions, libraries, and checkers testifies that the problem is neither exotic
                                         nor solved [Danish et al. 2024, a preprint]. Nor is the disaster a relic: a lightweight detector found
                                         physical-unit inconsistencies in 11% of 213 open-source robotics systems [Ore et al. 2017], and a
                                         units checker applied to the Weather Research and Forecasting model found an equation convert-
                                         ing grams to micrograms by multiplying by 10−6 instead of 106 [Danish et al. 2024].
                                           At least superficially, the remedy looks like a type system, and an elegant theoretical literature
                                         has explored this approach. Moreover, the static analysis required has compiler applications be-
                                         yond just spotting errors. To rescale a unit is to multiply every quantity stored at it by a factor. A
                                         numerical kernel may choose to rescale measurements in order to keep the values it works with
                                         inside the range where floating point carries full precision, or move a whole computation into one
                                         system of units so that no operation has to convert. Both are choices of internal representation,
                                         invisible in the source, and both are rescalings.1
                                           An abstraction theorem says that well-typed programs respect rescalings: rescale a program’s
                                         inputs by their units’ factors and its output rescales by exactly the factor its result type prescribes.
                                         No program can depend on how big a meter is. Beginning with Kennedy [1997], typed calculi with
                                         units as a free abelian group enjoy abstraction theorems, non-definability results (e.g., no term
                                         1
                                          Binary powers are useful choices of factor. IEEE 754 [IEEE 2019] represents a binary number by a significand and an
                                         exponent, so rescaling by 2𝑘 is exact when the value remains in the normal range.

                                         Author’s Contact Information: Eric Allen, eric.allen@twosigma.com, Two Sigma Investments, LP, New York, USA.
2                                                                                           Eric Allen


of type ∀u. Q u2 → Q u computes square root), and the Pi theorem of dimensional analysis, all
as consequences of parametricity. The Pi theorem says that a dimensionally consistent relation
among 𝑛 quantities factors through their dimensionless combinations. But that literature rests on
a design property: nothing in those calculi can observe a unit. There is no conversion operator, and
there cannot be one. A term that converts meters to feet multiplies by a factor determined by the
magnitudes of the meter and the foot; rescale the meter and the correct factor changes, so the term
would no longer commute with rescaling, and the unconditional abstraction theorems would be
false.
   The practical literature has the opposite problem. Practical language designs and libraries make
conversion available: the object-oriented formulation of Allen et al. [2004], with its dynamic con-
version factors and scales; F#’s units [Kennedy 2010], where the programmer writes each factor
as a typed literal; and the metrology library of Foster and Wolff [2023]. The gap has persisted for
more than two decades: calculi with theorems have no conversion, and systems with conversion
have no invariance theorems. The gap is in the theory. In the deployed designs a conversion factor
is a number, whether derived from declared unit magnitudes or written by hand. What none of
them has is a theorem saying what the factor costs invariance.
   In this paper, we close that gap. We present Λ𝑆 , the simply typed lambda calculus extended with
quantity types indexed by units (Q meter is the type of lengths measured in meters), quantification
over units and over dimensions, dimensioned vectors and linear maps, and a typed conversion
primitive. The primitive convert 𝑒 𝑢 𝑣 takes a quantity at unit 𝑢 to the same quantity at unit 𝑣 ,
multiplying its magnitude by the appropriate factor; it is well-typed only when 𝑢 and 𝑣 share a
dimension. The question our paper answers is what survives of the parametric theory once this
term is in the language, and the answer has three parts.
   First, invariance survives, and conversion tells us exactly by how much. We call a term paramet-
ric when it names no unit constant 1𝑢 (the constant magnitude 1 at unit 𝑢 ), and a rescaling coherent
when it factors through dimension, so that it cannot separate units of one dimension: if it doubles
the meter, it must double the foot and the yard, all being lengths, which is to say it leaves the
declared factors where they are. A kernel that rescales one length unit while fixing others makes
an incoherent change, outside this guarantee. Section 6 gives a separate certificate for invariance
under independent unit rescalings. Every parametric term, conversions included, is invariant un-
der every coherent rescaling; every parametric convert-free term is invariant under every rescaling
whatsoever, Kennedy’s theorem in our setting. The pair brackets conversion exactly: a single con-
version of a nonzero argument is invariant under a rescaling if and only if that rescaling assigns
its source and target the same factor, which is what coherence demands of a same-dimension pair.
   Second, for first-order programs the theory becomes an algorithm. A program is first-order when
its inputs and result are scalars, vectors, or matrices rather than functions; internal abstraction
and application remain unrestricted. We begin with the scalar case. We abbreviate meter, foot, and
second as m, ft, and s. Writing 𝑒 in 𝑣 for the conversion of 𝑒 to 𝑣 , and taking 𝑥 of type Q m, the
round trip (𝑥 in ft) in m multiplies by a factor and its reciprocal and so cannot depend on how the
units are declared, while the one-way 𝑥 in ft can. We analyze a program’s accumulated conversion
ratio and prove that, when the analysis assigns a ratio, a first-order program with nonzero output
is invariant under all rescalings exactly when its ratio is trivial. Triviality is decidable because
ratios, like units, are exponent vectors over ℚ. The procedure returns one of three verdicts: it
certifies invariance, names the ratio responsible for a departure, or declines. A decline supplies
no invariance verdict; we call an assigned ratio the program’s drift. Drift-free does not require
conversion freedom, as the round trip shows: the certificate says the declarations cannot reach the
answer, not that the program avoided conversion.
A Calculus for Units of Measure with Conversion                                                                        3


   Third, conversion forces an account of where its factors come from. Declarations such as yard =
3 foot and foot = 0.3048 meter can conflict: a mistyped yard = 0.9 meter makes a direct conversion
and a conversion through feet disagree, a conversion-library bug. Following Karr and Loveman III
[1978], we give declaration sets a consistency criterion in exact rational arithmetic, necessary and
sufficient, and carry the surviving factor by a chain of theorems from the declaration through
the semantics to the multiplication the evaluator performs with real arithmetic: a yard evaluates
to 0.9144 meters by either route, as a theorem. An executable, verified declaration checker also
requires the factors to be determined for every same-dimension pair; consistency alone does not
ensure this. It extracts exact factors, including radicals,2 from the accepted declarations (Section 3).
   Every theorem in our paper is a theorem of a Lean 4 mechanization we call the artifact,3 and
the artifact, not this paper, is the source of truth (Section 10); our paper guides the reader to the
ideas. The artifact also runs: the evaluator the theorems are about, instantiated at floating point,
compiles through Lean’s C backend to a native binary whose vector and matrix operations call
BLAS (Accelerate’s cblas) on macOS and portable C loops elsewhere. That is possible because a
matrix’s units live in its type (Section 9), so its payload is an array of doubles with no per-entry
tags, which is exactly what BLAS expects. The binary runs the instrumented evaluator of Section 4,
so a scalar still carries its unit tag; the erasure theorem (Section 7) says it need not.
   Λ𝑆 has no recursion and no boolean type beyond a compare-and-branch on quantities, but does
have vectors and linear maps with per-component units, following Hart [1995]; we sought the
smallest calculus that captures the phenomena we study. Every term works at one fixed size, since
Λ𝑆 has neither recursion nor quantification over size, but at a fixed size it writes numerical kernels
directly: the artifact reads matrix entries and rows, builds transposes, computes the trace, deter-
minant, and inverse of a dimensioned endomorphism, and performs a 2 × 2 Jacobi rotation that
diagonalizes a symmetric matrix exactly (Section 9). Algorithms that iterate to convergence, such
as a general eigensolver or a singular value decomposition, are not expressible.
   Our paper follows the development in order: the calculus and its checker (Section 2), declarations
(Section 3), the evaluator (Section 4), the semantics and the price of conversion (Sections 5–6),
adequacy and erasure (Section 7), dimensional analysis and dimensioned linear algebra (Sections 8–
9), the mechanization (Section 10), related work, and the conclusion.

2 The Calculus
We present the syntax and statics of Λ𝑆 . We represent units and dimensions as exponent vectors
over ℚ, and every operation on them is linear algebra. The unit kg ⋅ m/s2 is the vector (kg ↦
1, m ↦ 1, s ↦ −2); multiplication is pointwise addition, the 𝑞 -th power is scalar multiplication
by 𝑞 , and equality is a comparison of finitely many rationals. There is nothing to normalize: u ⋅ v
and v ⋅ u are one vector, exactly as 2 + 2 and 4 are one number.
   Two aspects of this representation carry our paper. First, exponents are rational, not integral as in
Kennedy’s free abelian group [Kennedy 1997]. Rational exponents appear in Karr and Loveman III
[1978] and in the dimension-inference systems of Wand and O’Keefe [1991] and Goubault [1994],
where dimensions already form a vector space over ℚ. Kennedy’s argument for ℤ was that M1/2
makes no physical sense and would suggest revising the set of base dimensions [Kennedy 1996,
§1.3]. Any finite set of rational exponents can be made integral by rebasing at a common denomi-
nator. But a library fixes its basis before a client chooses the powers it needs; rational exponents

2
  Declared factors are rational, but because exponents are rational, a derived factor can be a radical. A one-dimensional
wavefunction amplitude carries m−1/2 ; with nm = 10−9 m declared, converting an amplitude from nm−1/2 to m−1/2 mul-
tiplies by 109/2 . The checker extracts every factor exactly, as a rational radicand and an integer root degree.
3
  https://github.com/ericeallen/lambda-s
4                                                                                                                Eric Allen


    units       𝑢, 𝑣 ∶∶= 1 ∣ 𝑏 ∣ u ∣ 𝑢 ⋅ 𝑣 ∣ 𝑢/𝑣 ∣ 𝑢 𝑞              𝑏 ∈ 𝐵; u a unit variable; 𝑞 ∈ ℚ
    dimensions      𝑑 ∶∶= 1 ∣ 𝑑0 ∣ 𝛿 ∣ 𝑑 ⋅ 𝑑 ∣ 𝑑/𝑑 ∣ 𝑑 𝑞            𝑑0 ∈ 𝐷; 𝛿 a dimension variable
    spaces     𝑢⃗, 𝑤⃗ ∶∶= [ ] ∣ 𝑢, 𝑢⃗                               per-component unit lists
    types             𝜏 ∶∶= Q 𝑢                                     quantity at unit 𝑢
                         ∣ 𝜏 →𝜏                                     function
                         ∣ Vec 𝑢⃗                                   vector with per-component units
                         ∣ Lin 𝑢⃗ 𝑤⃗                                linear map
                         ∣ ∀u∶𝑑. 𝜏                                  unit abstraction, bounded by a dimension
                         ∣ ∀𝛿. 𝜏                                    dimension abstraction
    terms             𝑒 ∶∶= 𝑥 ∣ 𝜆𝑥∶𝜏 . 𝑒 ∣ 𝑒 𝑒
                         ∣ 𝑞 ∣ 1𝑢                                   rational literal (at unit 1); unit constant
                         ∣ 𝑒 ⋅ 𝑒 ∣ 𝑒/𝑒 ∣ 𝑒 + 𝑒 ∣ 𝑒 𝑞                arithmetic; constant rational power
                         ∣ log 𝑒 ∣ exp 𝑒                            at unit 1 only
                         ∣ if 𝑒 ≤ 𝑒 then 𝑒 else 𝑒                   compare and branch
                         ∣ 𝑒.𝑖 ∣ row𝑖 𝑒                             component; row
                         ∣ 𝑒⊙𝑒 ∣𝑒∘𝑒                                 map application; composition
                         ∣ ⟨⟩ ∣ 𝑒 ∶∶ 𝑒                              vector literals: empty; cons
                         ∣ ⟨⟩𝑢⃗ ∣ 𝑒 ∶∶𝑤 𝑒                           matrix literals: rowless at 𝑢⃗; row cons at 𝑤
                         ∣ Λu∶𝑑. 𝑒 ∣ 𝑒 [𝑢]                          unit abstraction and application
                         ∣ Λ𝛿. 𝑒 ∣ 𝑒 {𝑑}                            dimension abstraction and application
                         ∣ convert 𝑒 𝑢 𝑣                            conversion

Fig. 1. Syntax of Λ𝑆 . Function application 𝑒 𝑒 and linear-map application 𝑒 ⊙ 𝑒 are distinct term forms, as in
the artifact.


admit those powers without changing the library. The group is then divisible, so √𝑒 ∶ Q m1/2
for 𝑒 ∶ Q m needs no change of basis, and in the proofs rank-nullity replaces Smith normal form
(Section 8). Quantities of genuinely fractional dimension, such as the m−1/2 of a one-dimensional
wavefunction amplitude in quantum mechanics, come for free.4 Second, units and dimensions are
related by a homomorphism. Let 𝐵 and 𝐷 be the sets of base units and base dimensions. A unit
system assigns each base unit a dimension, dim ∶ 𝐵 → ℚ𝐷 , total and fixed, extended linearly.
Nothing restricts a dimension to one unit, which is precisely the situation conversion exists to
serve and that systems tracking only dimensions cannot express. The two-level design follows the
object-oriented lineage [Allen et al. 2004].
    The types and terms of Λ𝑆 appear in Figure 1. A quantity type Q 𝑢 classifies scalars at unit
𝑢 ; Vec 𝑢⃗ and Lin 𝑢⃗ 𝑤⃗ classify vectors and linear maps with per-component units, following Hart
[1995]. Both carry introduction forms as well as eliminations: a vector is built by consing scalars
onto ⟨⟩, each cons extending the space, and a matrix by rows, where ⟨⟩𝑢⃗ carries its domain space
(so a rowless matrix has a well-defined width) and a row cons at output unit 𝑤 requires component
𝑖 at unit 𝑤/𝑢𝑖 . The two quantifiers are the calculus’s answer to what an unbounded unit variable
means: there is no such thing. Unit abstraction is always bounded by a dimension, and unbounded
quantification is recovered as ∀𝛿. ∀u∶𝛿. 𝜏 . The bound is what makes conversion usable in polymor-
phic code: under Λu∶Length the body may convert between u and meter, because the checker sees

4                                             −1
 A probability density on a line carries Length , so that its integral is dimensionless. The density is the squared modulus
                                                 −1/2
of the amplitude, so the amplitude carries Length     .
A Calculus for Units of Measure with Conversion                                                                             5


they share a dimension. In particular the generic caster Λ𝛿. Λu∶𝛿. Λv∶𝛿. 𝜆𝑥∶Q u. convert 𝑥 u v is
well-typed (caster), and the abstraction theorems of Section 5 explain what it costs.
   The arithmetic rules carry the unit discipline (Figure 2). Multiplication and division are to-
tal on units. Addition demands its operands at equal units, not merely interchangeable ones:
adding meters to feet is a type error, and convert is how the programmer says it was intended.5
Kennedy’s thesis proposes the opposite design as further work for a units-primary language: typ-
ing rules extended so that inference inserts the conversions automatically, after Thatte’s coer-
cive isomorphisms [Kennedy 1996, §8.1]. Powers at constant rational exponents are primitive,
(⋅)𝑞 ∶ Q 𝑢 → Q 𝑢 𝑞 with no side condition, and √   𝑛 𝑒 abbreviates 𝑒 1/𝑛 ; not every power is definable

from the field operations, which is the non-definability theorem of Section 8. Finally, log and exp
require arguments at unit 1. A dimensionless ratio such as m/ft must first be converted to that unit.
Conversion carries its source unit and its target, because the evaluator uses those units to look up
the factor in its supplied conversion function, without consulting a typing derivation; we support
a surface syntax such as 𝑒 in 𝑣 that leaves the source to the verified checker (elabConvert). Elabo-
ration succeeds exactly when the argument has some unit of 𝑣 ’s dimension (elabConvert_isSome).
   The statics borrow a practice from dependently typed programming [Chlipala 2013]: the checker
returns not a type but a derivation, an inhabitant of Σ𝜏 . HasTy Δ Γ 𝑒 𝜏 . Checker soundness (anything
it accepts is well-typed) is then a consequence of the type rather than a theorem: a checker that
cannot produce a type without the derivation justifying it cannot accept an ill-typed term. (Type
soundness, about the dynamics, is proved in Section 4.) What remains with content is completeness,
which the artifact proves in a strengthened form: the checker returns a derivation whenever one
exists, and derivations are unique, so we can define the semantics by recursion on them (check_eq,
which gives uniqueness as a corollary).
   The checker consumes fully annotated terms; it is not a principal-type inference algorithm.
Kennedy’s inference solves unit equations by abelian-group unification [Kennedy 1996]. Our mod-
ule LambdaS.Unify proves single-equation elimination, preservation of ground solution sets by
terminating triangularization (System.solves_triangulate_iff), and the terminal check that the
variable-free equations left after triangularization already hold. It does not construct a most gen-
eral symbolic substitution or generate constraints from unannotated terms. Conversion also con-
tributes dim 𝑢 = dim 𝑣 , which does not imply 𝑢 = 𝑣 . Whether decidable principal-type inference
extends to this two-level constraint system remains open in our development.

3 Unit Declarations
Conversion needs factors, and factors need a source and a soundness criterion. In Λ𝑆 they come
from declarations:
                        unit yard = 3 foot;    unit foot = 0.3048 meter.
Declarations can conflict: add a mistyped yard = 0.9 meter and the direct route disagrees with
the route through feet, since 3 × 0.3048 = 0.9144 ≠ 0.9.6 An implementation that chooses a
conversion route without first checking consistency can admit this conversion-library bug. Λ𝑆
chooses no route. A valuation 𝑉 assigns each base unit a positive real magnitude (an exchange-
rate table, not a measurement), extended homomorphically to all algebraically expressible units.
5
  The value of requiring exact unit matching was first made clear to the author by Guy L. Steele Jr., who argued that it helps
a programmer manage the imprecisions and finite bounds of floating-point computation.
6
  The yard has been exactly 0.9144 meters only since 1959, when the United States and five other English-speaking countries
adopted a common yard, the American one moving by two parts per million [Astin and Karo 1959]. The United States kept
its earlier foot for surveying; that redundant declaration, inconsistent with the new one in the seventh decimal place,
survived until its retirement, effective December 31, 2022, announced by a 2020 Federal Register notice [National Institute
of Standards and Technology and National Oceanic and Atmospheric Administration 2020].
6                                                                                                               Eric Allen


       T-VaR                   T-Lam                                   T-App
         Γ(𝑥) = 𝜏                     Δ; Γ, 𝑥∶𝜏 ⊢ 𝑒 ∶ 𝜎                Δ; Γ ⊢ 𝑒1 ∶ 𝜏 → 𝜎            Δ; Γ ⊢ 𝑒2 ∶ 𝜏
       Δ; Γ ⊢ 𝑥 ∶ 𝜏             Δ; Γ ⊢ 𝜆𝑥∶𝜏 . 𝑒 ∶ 𝜏 → 𝜎                            Δ; Γ ⊢ 𝑒1 𝑒2 ∶ 𝜎

                                                                      T-Mul
         T-Lit                         T-Con                          Δ; Γ ⊢ 𝑒1 ∶ Q 𝑢          Δ; Γ ⊢ 𝑒2 ∶ Q 𝑣
         Δ; Γ ⊢ 𝑞 ∶ Q 1                 Δ; Γ ⊢ 1𝑢 ∶ Q 𝑢                        Δ; Γ ⊢ 𝑒1 ⋅ 𝑒2 ∶ Q 𝑢 𝑣

             T-Div                                               T-Add
             Δ; Γ ⊢ 𝑒1 ∶ Q 𝑢          Δ; Γ ⊢ 𝑒2 ∶ Q 𝑣                Δ; Γ ⊢ 𝑒1 ∶ Q 𝑢         Δ; Γ ⊢ 𝑒2 ∶ Q 𝑢
                     Δ; Γ ⊢ 𝑒1 /𝑒2 ∶ Q 𝑢/𝑣                                    Δ; Γ ⊢ 𝑒1 + 𝑒2 ∶ Q 𝑢

    T-IfLe                                                                                         T-Pow
    Δ; Γ ⊢ 𝑒1 ∶ Q 𝑢          Δ; Γ ⊢ 𝑒2 ∶ Q 𝑢         Δ; Γ ⊢ 𝑒3 ∶ 𝜏           Δ; Γ ⊢ 𝑒4 ∶ 𝜏            Δ; Γ ⊢ 𝑒 ∶ Q 𝑢
                         Δ; Γ ⊢ if 𝑒1 ≤ 𝑒2 then 𝑒3 else 𝑒4 ∶ 𝜏                                     Δ; Γ ⊢ 𝑒 𝑞 ∶ Q 𝑢 𝑞

                                      T-VCons
     T-VNil                           Δ; Γ ⊢ 𝑒1 ∶ Q 𝑢        Δ; Γ ⊢ 𝑒2 ∶ Vec 𝑢⃗              T-MNil

      Δ; Γ ⊢ ⟨⟩ ∶ Vec [ ]                   Δ; Γ ⊢ 𝑒1 ∶∶ 𝑒2 ∶ Vec (𝑢, 𝑢⃗)                    Δ; Γ ⊢ ⟨⟩𝑢⃗ ∶ Lin 𝑢⃗ [ ]

         T-MCons                                                               T-Idx
             Δ; Γ ⊢ 𝑒1 ∶ Vec (𝑤/⃗𝑢)          Δ; Γ ⊢ 𝑒2 ∶ Lin 𝑢⃗ 𝑤⃗             Δ; Γ ⊢ 𝑒 ∶ Vec 𝑢⃗         𝑢⃗𝑖 = 𝑢
                     Δ; Γ ⊢ 𝑒1 ∶∶𝑤 𝑒2 ∶ Lin 𝑢⃗ (𝑤, 𝑤)
                                                   ⃗                                   Δ; Γ ⊢ 𝑒.𝑖 ∶ Q 𝑢

             T-MRow                                         T-Mapp
             Δ; Γ ⊢ 𝑒 ∶ Lin 𝑢⃗ 𝑤⃗        𝑤⃗𝑗 = 𝑤            Δ; Γ ⊢ 𝑒1 ∶ Lin 𝑢⃗ 𝑤⃗         Δ; Γ ⊢ 𝑒2 ∶ Vec 𝑢⃗
               Δ; Γ ⊢ row𝑗 𝑒 ∶ Vec (𝑤/⃗𝑢)                               Δ; Γ ⊢ 𝑒1 ⊙ 𝑒2 ∶ Vec 𝑤⃗

     T-Comp                                                     T-Log                           T-Exp
     Δ; Γ ⊢ 𝑒1 ∶ Lin 𝑣⃗ 𝑤⃗          Δ; Γ ⊢ 𝑒2 ∶ Lin 𝑢⃗ 𝑣⃗            Δ; Γ ⊢ 𝑒 ∶ Q 1               Δ; Γ ⊢ 𝑒 ∶ Q 1
                 Δ; Γ ⊢ 𝑒1 ∘ 𝑒2 ∶ Lin 𝑢⃗ 𝑤⃗                     Δ; Γ ⊢ log 𝑒 ∶ Q 1              Δ; Γ ⊢ exp 𝑒 ∶ Q 1

    T-ULam                                 T-UApp                                              T-DLam
        Δ, u∶𝑑; Γ ⊢ 𝑒 ∶ 𝜏                  Δ; Γ ⊢ 𝑒 ∶ ∀u∶𝑑. 𝜏          dimΔ (𝑤) = 𝑑                Δ, 𝛿; Γ ⊢ 𝑒 ∶ 𝜏
    Δ; Γ ⊢ Λu∶𝑑. 𝑒 ∶ ∀u∶𝑑. 𝜏                       Δ; Γ ⊢ 𝑒 [𝑤] ∶ 𝜏 [u ↦ 𝑤]                     Δ; Γ ⊢ Λ𝛿. 𝑒 ∶ ∀𝛿. 𝜏

                      T-DApp                                         T-Cvt
                          Δ; Γ ⊢ 𝑒 ∶ ∀𝛿. 𝜏                           Δ; Γ ⊢ 𝑒 ∶ Q 𝑢          𝑢 ∼Δ 𝑣
                      Δ; Γ ⊢ 𝑒 {𝑑} ∶ 𝜏 [𝛿 ↦ 𝑑]                       Δ; Γ ⊢ convert 𝑒 𝑢 𝑣 ∶ Q 𝑣

Fig. 2. Typing: the full rule set, transcribed from the artifact’s HasTy with named variables in place of its de
Bruijn indices. Δ; Γ ⊢ 𝑒 ∶ 𝜏 types 𝑒 under a context Δ of dimension variables and unit variables (each with
its dimension bound) and a term context Γ; dimΔ extends dim to unit variables by their bounds, and 𝑢 ∼Δ 𝑣
means dimΔ (𝑢) = dimΔ (𝑣). In T-ULam and T-DLam the bound variable is fresh for Δ, so it occurs nowhere in
Γ. In T-Idx and T-MRow, the premises 𝑢⃗𝑖 = 𝑢 and 𝑤⃗𝑗 = 𝑤 abbreviate successful bounds-checked lookups, as
in the artifact. In T-Con, 𝑢 ranges over all unit expressions, variables included. (𝑢, 𝑢⃗) prepends a component
to a space, and in T-MCons, 𝑤/⃗     𝑢 is the pointwise quotient, entry 𝑗 at 𝑤/𝑢𝑗 .
A Calculus for Units of Measure with Conversion                                                      7


Conversion factors are ratios of magnitudes, so path independence is a theorem, and a declaration
set is consistent when some valuation satisfies every declared equation.
   The other declaration forms need only scoping: a bare dimension Length supplies the param-
eter 𝐷 ; an abbreviation dimension Velocity = Length/Time expands at once, so cycles are un-
representable rather than detected (a cycle would need a second binding of Length, rejected for
rebinding a generator, dimCycle); and a primary unit declaration (the term is Allen et al.’s [2004],
the syntax Fortress’s [Allen et al. 2006]), unit meter ∶ Length, supplies 𝐵 and dim (elabPrimary).
Factor declarations, by contrast, carry semantic content, and cycles among them are just depen-
dencies: the benign foot = 13 yard is satisfiable (cycle_satisfiable); foot = yard forces 3 = 1 and
is rejected (cycle_conflict).
   Each factor declaration 𝑢 = 𝑞 𝑣 is a ratio 𝑟 = 𝑢/𝑣 in the unit group and a positive rational
factor 𝑞 , and a valuation satisfies it exactly when 𝑉 (𝑟) = 𝑞 . The mistyped set has 𝑟1 = yard/foot,
𝑟2 = foot/meter, 𝑟3 = yard/meter with 𝑞1 = 3, 𝑞2 = 0.3048, 𝑞3 = 0.9. Its ratios are dependent,
𝑟1 ⋅ 𝑟2 = 𝑟3 , that is, 𝑟1 + 𝑟2 − 𝑟3 = 0 as exponent vectors, so any valuation must have 𝑞1 𝑞2 /𝑞3 =
𝑉 (𝑟1 )𝑉 (𝑟2 )/𝑉 (𝑟3 ) = 𝑉 (1) = 1; but 3 × 0.3048/0.9 = 1.016, so none exists. With 𝑞3 = 0.9144 the
product is exactly 1. The three ratios have rank 2, so this is their only dependency, and 𝑉 (meter) =
1, 𝑉 (foot) = 0.3048, 𝑉 (yard) = 0.9144 satisfies all three declarations. The general statement is this
computation over every dependency.

   TheoRem 3.1 (Consistency; consistent_iff_dependencies_mul). A finite declaration set with
ratios 𝑟𝑖 and positive rational factors 𝑞𝑖 admits a satisfying valuation if and only if every ℚ-linear
                                                           𝑐
combination with ∑𝑖 𝑐𝑖 𝑟𝑖 = 0 in the unit group has ∏𝑖 𝑞𝑖 𝑖 = 1.

   In logarithmic coordinates each declaration is one linear equation, as Karr and Loveman III
[1978] observed. The artifact solves this system by executable Gaussian elimination and back-
substitution (DeclSolver.solve_isSome_iff). Coefficients are rational; the right-hand sides are
symbolic rational combinations of logarithms of positive rationals. For example, (log 2)/2 is stored
as the logarithm of the rational 2 divided by the integer 2, without evaluating it. Clearing denom-
inators expresses such a combination as (log 𝑞)/𝑁 , for positive rational 𝑞 and positive integer 𝑁 .
It is zero exactly when 𝑞 = 1, an exact rational test. Thus elimination never evaluates a real loga-
rithm or root, and a nonzero right-hand side on a zero row rejects an inconsistent set. Soundness
and completeness connect success to existence of a real satisfying valuation.
   Rational powers can require irrational magnitudes. A valuation satisfying nm = 10−9 m with
𝑉 (m) = 1 has 𝑉 (nm−1/2 ) = 109/2 . We therefore take valuations over the reals. For sufficiency
in Theorem 3.1, the unknowns log 𝑉 (𝑏) are real, yet checking only rational dependencies suffices
because ℝ is a vector space over ℚ. The compatible assignment of log-factors defines a ℚ-linear map
on the span of the ratio vectors; extending it to the whole unit space gives a satisfying valuation
(dependency_sufficient). The mistyped set is rejected outright: no valuation exists, so there is no
route to choose.
   Before execution, every conversion the program can perform must have a supplied numerical
factor. Consistency alone does not ensure this. Declaring meter and foot as primary units of length
makes 𝑥 in meter well-typed for 𝑥 ∶ Q foot, but supplies no numerical answer. The artifact’s
declaration checker rejects this incomplete system; adding foot = 0.3048 meter makes it pass.
   For a consistent set, 𝑉 (𝑢)/𝑉 (𝑣) is fixed across its satisfying valuations exactly when the ex-
ponent vector 𝑢/𝑣 lies in the ℚ-span of the declared ratios (Decl.determined_iff_coefficients).
On that span linearity fixes the log-factor; outside it a separating linear functional changes the
factor while preserving every declaration. The executable factor lookup solves for the span co-
efficients and succeeds exactly when the factor is determined (DeclSolver.conversion_isSome_
8                                                                                             Eric Allen


iff). To cover every pair of same-dimension units, the declared ratios must span the kernel of
dim. The global check decides this finite linear-algebra condition, with both directions proved
(DeclarationComplete.check_iff_all_conversions_determined).
  TheoRem 3.2 (Executable declaRation checKing; DeclSolver.check_isSome_iff). For a finite
unit system, the declaration checker accepts exactly when every declaration relates units of the same
dimension, a satisfying valuation exists, and every same-dimension conversion has the same factor in
every satisfying valuation.
   Acceptance returns a computed solution with proofs of these properties. Factor extraction then
succeeds for every same-dimension pair of concrete units (DeclSolver.Checked.conversionExact_
isSome). It returns a positive rational radicand and a positive integer root degree, and the factor
they represent is 𝑉 (𝑢)/𝑉 (𝑣) in every satisfying valuation (DeclSolver.conversionExact_correct).
For example, with nm = 10−9 m declared, converting a wavefunction amplitude from nm−1/2
to m−1/2 multiplies by 109/2 , returned as radicand 109 and degree 2 (Nanometer.exactAmplitude).
The solver may choose reference magnitudes for unconstrained directions, but it never uses that
choice to claim a missing factor is determined. Path independence holds within a valuation; the
determinacy criterion above gives agreement across satisfying valuations. Section 6’s certificate
of independence from every supplied factor is stronger (den_indep_of_driftFree), while the dec-
laration checker ensures that the conversions needed to execute the program have factors.

4 Dynamics
We now run the calculus, with a total conversion function supplied as an input. Section 3’s checker
and factor extractor establish that accepted declarations supply every same-dimension factor. We
write 𝐸 = (𝜌, 𝜂, 𝜃) for the term, unit, and dimension environments. The latter two assign a ground
unit or dimension to every variable in scope, because the only rule that brings one into scope,
E-UApp or E-DApp, grounds its argument in the caller’s environment before binding it, and evalu-
ation starts on a closed term with empty environments. Write 𝑢 𝐸 and 𝑑 𝐸 for their linear extensions
to unit and dimension expressions, and 𝑢⃗𝐸 for componentwise grounding; these are always closed,
and no run-time value carries a unit variable. Magnitudes range over a carrier 𝑅 with the artifact’s
Num operations. Values are scalars, vectors, matrices, or closures of three kinds, each capturing all
three environments (Figure 3).
   The evaluator is a definitional interpreter [Reynolds 1972] written as a total function. Lean re-
quires every function to terminate, and termination of evaluation is a theorem proved below rather
than a fact available at the definition, so the evaluator takes a natural number, its fuel, and returns
failure when the fuel runs out [Amin and Rompf 2017; Owens et al. 2016]. Intuitively, fuel is a finite
resource like stack space, supplied in whatever quantity a run needs: a run that completes within
the bound returns the same value under every larger bound (eval_mono), and a run that exhausts it
fails rather than diverging. The judgment 𝐸; 𝑛 ⊢ 𝑒 ⇓ 𝑣 means that eval, with conversion function
𝑐 and fuel 𝑛, returns 𝑣 . We hold 𝑐 fixed in the rules. The environment, fuel, and term are inputs;
the value is the output. Figures 3–5 give every successful case of the evaluator. A term with no
applicable rule returns failure, including every closure application at fuel zero. Failure thus rep-
resents either exhausted fuel or a failed dynamic check; the evaluator does not distinguish them.
Fuel bounds closure-entry depth, not a global count of steps: subterms receive the same fuel as
their parent, and only entering a closure body decreases it.
   The evaluator checks units wherever an operation is meaningful only at particular units, and
nowhere else. Addition, comparison, conversion, map application, and composition each check
that their two operands agree; logarithm and exponential check that their one operand is dimen-
sionless; multiplication, division, and powers compute their result unit and check nothing; and the
A Calculus for Units of Measure with Conversion                                                                            9


                             𝑣    ∶∶=      ⟨𝑎, 𝑢⟩ ∣ vec(⃗𝑎, 𝑈 ) ∣ mat(𝑀, 𝑈 , 𝑊 )
                                            ∣ clos(𝑥∶𝜏 , 𝑒, 𝐸) ∣ uclos(u∶𝑑, 𝑒, 𝐸) ∣ dclos(𝛿, 𝑒, 𝐸).
       E-VaR
         𝜌(𝑥) = 𝑣                 E-Lam                                           E-ULam

        𝐸; 𝑛 ⊢ 𝑥 ⇓ 𝑣              𝐸; 𝑛 ⊢ 𝜆𝑥∶𝜏 . 𝑒 ⇓ clos(𝑥∶𝜏 , 𝑒, 𝐸)              𝐸; 𝑛 ⊢ Λu∶𝑑. 𝑒 ⇓ uclos(u∶𝑑, 𝑒, 𝐸)

                                                 E-DLam

                                                 𝐸; 𝑛 ⊢ Λ𝛿. 𝑒 ⇓ dclos(𝛿, 𝑒, 𝐸)

         E-App
         𝐸; 𝑛 + 1 ⊢ 𝑓 ⇓ clos(𝑥∶𝜏 , 𝑒, (𝜌 ′ , 𝜂′ , 𝜃 ′ ))     𝐸; 𝑛 + 1 ⊢ 𝑎 ⇓ 𝑣        (𝜌 ′ [𝑥 ↦ 𝑣], 𝜂′ , 𝜃 ′ ); 𝑛 ⊢ 𝑒 ⇓ 𝑤
                                                       𝐸; 𝑛 + 1 ⊢ 𝑓 𝑎 ⇓ 𝑤

                    E-UApp
                    𝐸; 𝑛 + 1 ⊢ 𝑓 ⇓ uclos(u∶𝑑, 𝑒, (𝜌 ′ , 𝜂′ , 𝜃 ′ ))     (𝜌 ′ , 𝜂′ [u ↦ 𝑢 𝐸 ], 𝜃 ′ ); 𝑛 ⊢ 𝑒 ⇓ 𝑣
                                                      𝐸; 𝑛 + 1 ⊢ 𝑓 [𝑢] ⇓ 𝑣

                      E-DApp
                      𝐸; 𝑛 + 1 ⊢ 𝑓 ⇓ dclos(𝛿, 𝑒, (𝜌 ′ , 𝜂′ , 𝜃 ′ ))    (𝜌 ′ , 𝜂′ , 𝜃 ′ [𝛿 ↦ 𝑑 𝐸 ]); 𝑛 ⊢ 𝑒 ⇓ 𝑣
                                                      𝐸; 𝑛 + 1 ⊢ 𝑓 {𝑑} ⇓ 𝑣

Fig. 3. Instrumented dynamics: values, variables, and closures. A scalar carries its ground unit 𝑢 ; a vector
carries its space 𝑈 ; a matrix carries its domain 𝑈 , codomain 𝑊 , and magnitude rows 𝑀 . The notation 𝜌(𝑥) = 𝑣
denotes a successful lookup, and 𝜌[𝑥 ↦ 𝑣] extends an environment. Unit and dimension arguments are
grounded in the caller’s environment before extending the captured one. The stored type and dimension
annotations impose no dynamic check.


introduction forms record their annotations without inspecting their arguments. The checks are
redundant for well-typed terms, and that redundancy is Theorem 4.1 below: the stuck states are
unreachable. The one constructor where this matters is mcons, which records its annotated output
unit and discards the row’s units, since a matrix value stores bare magnitudes. An ill-typed row
would corrupt every later product undetected; the typing rule alone excludes it, and soundness
carries that guarantee to the eliminators.
   The soundness and normalization results are parameterized by the supplied conversion function.
The fuel is not assumed but produced: every closed well-typed term evaluates at some fuel, by a
reducibility argument in the style of Tait [1967]7 (eval_terminates). The calculus has no reduction
relation; what is proved is termination of the evaluator, which is the normalization the fuel needs.
Type soundness then has its usual two halves: preservation (eval_sound), and progress in the form
the fueled setting delivers, that enough fuel always exists (eval_total).
  TheoRem 4.1 (Unit soundness; unit_soundness_total). For every closed well-typed term 𝑒 ∶ Q 𝑢
there exists a fuel bound 𝑛 and a magnitude 𝑚 such that evaluation of 𝑒 at fuel 𝑛 yields exactly ⟨𝑚, 𝑢⟩.
   The unit in the conclusion is 𝑢 itself: the run-time tag provably agrees with the static type, which
is what makes the tag erasable (Section 7). Fuel is observable: in the artifact’s quantum system
example (LambdaS.QM), a scalar computation written as an open term over its inputs evaluates at
fuel zero, and, curried and reapplied, it fails there and needs fuel one (twoStateChecks).
7
 Quantification ranges over units and dimensions, first-order algebraic data, so there is no impredicativity and no need for
Girard’s candidates [Girard 1972].
10                                                                                                                       Eric Allen


                                                                               E-Mul
       E-Lit                             E-Con                                 𝐸; 𝑛 ⊢ 𝑒1 ⇓ ⟨𝑎, 𝑢⟩         𝐸; 𝑛 ⊢ 𝑒2 ⇓ ⟨𝑏, 𝑣⟩
                                                                   𝐸
        𝐸; 𝑛 ⊢ 𝑞 ⇓ ⟨rat(𝑞), 1⟩            𝐸; 𝑛 ⊢ 1𝑢 ⇓ ⟨rat(1), 𝑢 ⟩                    𝐸; 𝑛 ⊢ 𝑒1 ⋅ 𝑒2 ⇓ ⟨𝑎 ×𝑅 𝑏, 𝑢𝑣⟩

              E-Div                                                      E-Add
              𝐸; 𝑛 ⊢ 𝑒1 ⇓ ⟨𝑎, 𝑢⟩        𝐸; 𝑛 ⊢ 𝑒2 ⇓ ⟨𝑏, 𝑣⟩               𝐸; 𝑛 ⊢ 𝑒1 ⇓ ⟨𝑎, 𝑢⟩         𝐸; 𝑛 ⊢ 𝑒2 ⇓ ⟨𝑏, 𝑢⟩
                    𝐸; 𝑛 ⊢ 𝑒1 /𝑒2 ⇓ ⟨𝑎 ÷𝑅 𝑏, 𝑢/𝑣⟩                               𝐸; 𝑛 ⊢ 𝑒1 + 𝑒2 ⇓ ⟨𝑎 +𝑅 𝑏, 𝑢⟩

                    E-Pow                                              E-TRans
                         𝐸; 𝑛 ⊢ 𝑒 ⇓ ⟨𝑎, 𝑢⟩                             𝐸; 𝑛 ⊢ 𝑒 ⇓ ⟨𝑎, 1⟩       ℎ ∈ {log, exp}
                               𝑞                  𝑞
                     𝐸; 𝑛 ⊢ 𝑒 ⇓ ⟨pow𝑅 (𝑎, 𝑞), 𝑢 ⟩                             𝐸; 𝑛 ⊢ ℎ 𝑒 ⇓ ⟨ℎ𝑅 (𝑎), 1⟩

                      E-If
                      𝐸; 𝑛 ⊢ 𝑒1 ⇓ ⟨𝑎, 𝑢⟩        𝐸; 𝑛 ⊢ 𝑒2 ⇓ ⟨𝑏, 𝑢⟩         𝛽 = le(𝑎, 𝑏)       𝐸; 𝑛 ⊢ 𝑒𝛽 ⇓ 𝑣
                                           𝐸; 𝑛 ⊢ if 𝑒1 ≤ 𝑒2 then 𝑒true else 𝑒false ⇓ 𝑣

                                         E-Cvt
                                         𝐸; 𝑛 ⊢ 𝑒 ⇓ ⟨𝑎, 𝑢 𝐸 ⟩      dim(𝑢 𝐸 ) = dim(𝑣 𝐸 )
                                         𝐸; 𝑛 ⊢ convert 𝑒 𝑢 𝑣 ⇓ ⟨𝑎 ×𝑅 𝑐(𝑢 𝐸 , 𝑣 𝐸 ), 𝑣 𝐸 ⟩

Fig. 4. Instrumented dynamics: scalars and branching. The transcendental schema covers logarithm and ex-
ponential. All magnitude operations are those supplied by Num: rat, ×𝑅 , ÷𝑅 , +𝑅 , pow𝑅 (base first; the artifact’s
Num takes the exponent first), log𝑅 , exp𝑅 , and the Boolean comparison le. No positivity or nonzero-divisor
check is added. Only the selected branch is evaluated.

                                       E-VCons
     E-VNil                            𝐸; 𝑛 ⊢ 𝑒 ⇓ ⟨𝑎, 𝑢⟩        𝐸; 𝑛 ⊢ 𝑣 ⇓ vec(⃗𝑎, 𝑈 )         E-MNil

     𝐸; 𝑛 ⊢ ⟨⟩ ⇓ vec([ ], [ ])            𝐸; 𝑛 ⊢ 𝑒 ∶∶ 𝑣 ⇓ vec(𝑎 ∶∶ 𝑎⃗, 𝑢 ∶∶ 𝑈 )                𝐸; 𝑛 ⊢ ⟨⟩𝑢⃗ ⇓ mat([ ], 𝑢⃗𝐸 , [ ])

      E-MCons                                                              E-Idx
      𝐸; 𝑛 ⊢ 𝑟 ⇓ vec(⃗𝑎, 𝑍 )        𝐸; 𝑛 ⊢ 𝑚 ⇓ mat(𝑀, 𝑈 , 𝑊 )              𝐸; 𝑛 ⊢ 𝑒 ⇓ vec(⃗𝑎, 𝑈 )        𝑎⃗[𝑖] = 𝑎 𝑈 [𝑖] = 𝑢
                                                   𝐸
         𝐸; 𝑛 ⊢ 𝑟 ∶∶𝑤 𝑚 ⇓ mat(⃗𝑎 ∶∶ 𝑀, 𝑈 , 𝑤 ∶∶ 𝑊 )                                        𝐸; 𝑛 ⊢ 𝑒.𝑖 ⇓ ⟨𝑎, 𝑢⟩

E-Row                                                                  E-MApp
𝐸; 𝑛 ⊢ 𝑒 ⇓ mat(𝑀, 𝑈 , 𝑊 )             𝑀[𝑖] = 𝑎⃗ 𝑊 [𝑖] = 𝑤              𝐸; 𝑛 ⊢ 𝑓 ⇓ mat(𝑀, 𝑈 , 𝑊 )           𝐸; 𝑛 ⊢ 𝑥 ⇓ vec(⃗𝑎, 𝑈 )
                𝐸; 𝑛 ⊢ row𝑖 𝑒 ⇓ vec(⃗𝑎, 𝑤/𝑈 )                                 𝐸; 𝑛 ⊢ 𝑓 ⊙ 𝑥 ⇓ vec(matVec(𝑀, 𝑎⃗), 𝑊 )

                                   E-Comp
                                   𝐸; 𝑛 ⊢ 𝑓 ⇓ mat(𝑀, 𝑉 , 𝑊 )           𝐸; 𝑛 ⊢ 𝑔 ⇓ mat(𝑁 , 𝑈 , 𝑉 )
                                            𝐸; 𝑛 ⊢ 𝑓 ∘ 𝑔 ⇓ mat(𝑀 ⊙|𝑈 | 𝑁 , 𝑈 , 𝑊 )

Fig. 5. Instrumented dynamics: vectors and matrices. All indexed lookups must succeed. The space 𝑤/𝑈 has
component 𝑖 at 𝑤/𝑢𝑖 . The operation matVec is supplied by Num. For each row 𝑟 of 𝑀 , the product 𝑀 ⊙𝑝 𝑁
                                      𝑝−1
constructs the row [dot(𝑟, col𝑖 (𝑁 ))]𝑖=0 using the carrier’s dot; col𝑖 replaces a missing entry in a row by rat(0).
Matrix row construction ignores 𝑍 , the incoming row’s unit space. No rule checks payload lengths beyond
the explicit indexed lookups; typing and soundness establish the shapes for well-typed executions.
A Calculus for Units of Measure with Conversion                                                     11


5 The Price of Conversion
This section states what conversion costs. The semantics rests on one decision, and it is where
our development parts from prior formalizations: a unit abstraction denotes a family of meanings,
indexed by the magnitude the bound unit receives. A calculus that cannot observe units may in-
terpret the family as constant, which is why the mechanized semantics of Kennedy [2008] could
interpret an abstraction as just its body (“units ignored”); conversion is exactly what forces the
family to vary. A rescaling 𝜓 assigns each base unit and unit variable a positive factor, extended
homomorphically; it is coherent when it factors through dimension, so that units of one dimen-
sion move together. A coherent rescaling therefore leaves every same-dimension conversion fac-
tor fixed, and an incoherent one changes at least one such factor. We call a term parametric when
it contains no unit constant 1𝑢 .
   There are two independent actions. Rescaling inputs by 𝜓 multiplies an argument at Q 𝑢 by
𝜓 (𝑢). With the valuation fixed, doubling a meter input doubles 𝑥 in ft. Rescaling the valuation
by 𝜑 instead replaces 𝑉 (𝑏) by 𝑉 (𝑏)𝜑(𝑏). The valuation moves with the inputs, not against them:
a rescaling is a change of representation applied to the stored numerals and to the declared table
alike, not a change in the size of a physical unit, under which numerals and magnitudes would
move inversely and every conversion would be trivially invariant. With the input fixed, doubling
the meter’s valuation and fixing the foot’s doubles the conversion factor 𝑉 (m)/𝑉 (ft). Doing both
therefore multiplies the answer by four, although its type Q ft predicts no change. The abstraction
theorems below specialize these actions to 𝜑 = 𝜓 ; Section 6 states the law with the actions separate.
   Unit application also consults the valuation to select a member of a family; conversion uses it to
multiply a magnitude. Convert-free terms nevertheless have valuation-independent denotations
in independent environments, at every type, and at scalar type this is equality of the two numbers
(den_indep). This is a semantic independence property, not an absence of valuation lookups.
   The proofs use two logical relations, ℛ𝜓 (Rel) and ℛco     Δ,Φ,𝜓 (RelCo), where Δ assigns dimensions
to unit variables and Φ rescales dimensions. They agree at quantifier-free types. At Q 𝑢 both re-
late 𝑥 to 𝜓 (𝑢) ⋅ 𝑥 ; at an arrow they map related arguments to related results. Vectors are related
componentwise; entry (𝑗, 𝑖) of a linear map scales by 𝜓 (𝑤𝑗 )/𝜓 (𝑢𝑖 ), as in Hart’s rank-one factoring
(Section 9).
   The difference is at a unit quantifier ∀u∶𝑑. 𝜏 . Write 𝐹 (𝑟) and 𝐺(𝑟) for the values of two families
when the bound unit has log-magnitude 𝑟 , and 𝜓 [u ↦ 𝑒 𝑠 ] for extending a rescaling. The convert-
free relation requires
                                 ∀𝑟, 𝑠 ∈ ℝ. ℛ𝜏𝜓 [u↦𝑒 𝑠 ] (𝐹 (𝑟), 𝐺(𝑟 + 𝑠)).
The coherent relation instead requires
                                     ,𝜏
                          ∀𝑟 ∈ ℝ. ℛco
                                   Δ,u∶𝑑,Φ,𝜓 [u↦Φ(𝑑)]
                                                      (𝐹 (𝑟), 𝐺(𝑟 + log Φ(𝑑))).
The family’s index remains quantified, but the bound unit’s factor is determined by its dimension.
Quantifying that factor independently would let a bound length rescale differently from the meter,
invalidating conversion to meters under the binder. At a dimension quantifier, ℛ uses the body’s
relation unchanged, whereas ℛco quantifies over every positive factor for the new dimension,
extending Φ accordingly. Theorem 5.1 below is therefore not the special case of Theorem 5.2 at a
coherent 𝜓 : at a unit binder it asks for relatedness at every factor for the bound unit, where the
coherent relation fixes one.
   Conversion convert 𝑥 𝑢 𝑣 multiplies by conv𝑉 (𝑢, 𝑣) = 𝑉 (𝑢)/𝑉 (𝑣), so relatedness at a nonzero
argument requires 𝜓 (𝑢) = 𝜓 (𝑣). The fundamental lemmas prove relatedness of denotations at 𝑉
and 𝑉 𝜓 , in related environments: with ℛ for convert-free terms, and with ℛco when 𝜓 factors
through Φ.
12                                                                                                              Eric Allen


   TheoRem 5.1 (AbstRaction, conveRt-fRee; fundamental_free). Every parametric, convert-free
term preserves ℛ𝜓 -related environments under every rescaling 𝜓 : its denotations at 𝑉 and 𝑉 𝜓 are
ℛ𝜓 -related at its result type.
   TheoRem 5.2 (AbstRaction, coheRent; fundamental). Every parametric term, conversions in-
cluded, preserves ℛco
                    Δ,Φ,𝜓 -related environments whenever 𝜓 factors through Φ: its denotations at 𝑉
and 𝑉 𝜓 are related by ℛcoΔ,Φ,𝜓 at its result type.
    Theorem 5.1 is Kennedy’s theorem [1997], here with vectors, linear maps, both quantifiers,
and rational powers; we call its equation a term’s scaling law. His scalings [Kennedy 1996, §6.4]
run over dimensions, so they are exactly our coherent ones by the following characterization
(coherent_iff_factors): a rescaling assigns equal factors to every same-dimension pair if and only
if it factors through a dimension rescaling. With independent base dimensions and one base unit
for each, every unit rescaling in closed unit scope is coherent (Scaling.coherent_of_dim_equiv).
Unit constants are excluded because 1𝑢 denotes the number 1 (a value at Q 𝑢 is a numeral at 𝑢 ,
and one 𝑢 is the numeral 1), and self-relatedness would demand 1 = 𝜓 (𝑢): a term that can name a
unit can detect a rescaling. Three term forms depend on a unit, at three different costs: 1𝑢 names
one and leaves the theory, conversion reads the declared magnitudes and costs coherence, and
a comparison sees only within a single unit and costs nothing, both sides moving by the same
positive factor. Zero alone is scale-invariant,8 the standing zero exception: it is why the theorem
below assumes a nonzero value. Powers need no positivity: for positive 𝑘 , (𝑘 ⋅ 𝑥)𝑞 = 𝑘 𝑞 ⋅ 𝑥 𝑞 at ev-
ery real 𝑥 (mul_rpow_of_pos_left), so signed quantities, which Kennedy’s Coq development [2008]
excludes by taking every value positive, keep their scaling law. For negative inputs, the artifact’s
non-integer power operation uses the real part of the principal complex power, rather than a real-
root convention. Theorem 5.1 certifies covariance of that total operation; it does not assert that
such a value is a root (Section 10).
  TheoRem 5.3 (Single-conveRsion invaRiance; cvt_rel_iff_coherent). For convert 𝑥 𝑢 𝑣 with
𝑥 given any nonzero value: invariance holds at a rescaling 𝜓 if and only if 𝜓 (𝑢) = 𝜓 (𝑣), the equation
every coherent rescaling satisfies at a same-dimension pair.
   Consequently, coherent rescalings are exactly those preserving every parametric term. Suffi-
ciency is Theorem 5.2. For necessity, a non-coherent rescaling separates some same-dimension pair
𝑢, 𝑣 ; the parametric term convert 𝑥 𝑢 𝑣 at a nonzero input then fails invariance by Theorem 5.3. The
artifact states the biconditional for the conversions themselves: a rescaling is coherent if and only if
every single conversion of a nonzero argument is invariant under it (coherent_iff_cvt_invariant).
   Theorem 5.3 says the bound the abstraction theorems place on the cost of conversion (coherence
suffices) is tight, per term and per rescaling, and that coherence is forced by the term rather than
chosen by the proof. Note that multiplication cannot substitute for the primitive, although con-
version’s semantics is multiplication by conv𝑉 (𝑢, 𝑣): a literal denotes the number the programmer
wrote and 1𝑢 denotes the number 1. A convert-free scalar term denotes the same number un-
der different valuations in independent environments (den_indep), and no parametric convert-free
term converts between distinct base units (convert_not_definable). The artifact runs the instance
that makes the point: 1yard /1foot evaluates to 1yard/foot at the declared table (ydPerFt), and by
den_indep its denotation is the same under every table. Converted to the dimensionless unit one
8
  Whether there is one zero or many is the subject of Russell’s Chapter XXII [Russell 1903, §§172–178]: he canvasses a
limit construction that makes zero single and “not one among the magnitudes whose zero it is” (§176), then concludes that
each kind of magnitude has its own zero (§177). Λ𝑆 takes both sides, and the seam is exactly the one between types and
semantics: 0 ⋅ 1m ∶ Q m and 0 ⋅ 1s ∶ Q s are distinct terms at distinct types denoting the one real number every rescaling
fixes.
A Calculus for Units of Measure with Conversion                                                                          13


(written in one), it is the declared 3, fetched by the only construct allowed to (ydPerFtIn1). The
route through feet, (1yard in foot)/1foot , is the same 3, dimensionless outright (ydPerFtViaFt).9

6 Accumulated Ratios, and a Decidable Diagnostic
With the abstraction theorems in hand, we ask what many conversions accumulate to, and turn the
answer into a decision procedure. The procedure is not a typing rule: every program it examines
is already well-typed and runs once its conversion factors are supplied (Section 3). For a first-
order program it delivers one of three verdicts: the program is certified invariant under every
rescaling; its departure from invariance is named by one accumulated conversion ratio, an element
of the group of units, which we call the program’s drift; or the analysis declines. In declaration
terms, the first verdict says that no error in the declaration set can change the program’s answer
(den_indep_of_driftFree), and the second says by how much one would (den_comp_of_drift). For
a drift-free program, a compiler may rescale units independently; for any analyzed program, a
rescaling that sends its drift to 1 is licensed, and at a nonzero output no other rescaling is.
   The ratio records how a value moves under a rescaling beyond the factor its type predicts. A
conversion convert 𝑒 𝑢 𝑣 leaves its value moving with 𝑢 where its type Q 𝑣 predicts 𝑣 : it contributes
𝑢/𝑣 . A product multiplies ratios. A sum requires its summands to agree, since unequal excess
factors do not in general give the sum a single factor; a conditional requires the same of its two
branches and of the two quantities compared, so that a wrong declaration cannot change which
branch runs. log and exp accept drift-free arguments and decline drifting ones, because log turns
an excess factor into an excess summand and exp into an excess exponent, and neither is a ratio.
The unit constant 1𝑢 is declined unconditionally: Theorem 5.1 places it outside the invariance
theory, and declining it keeps a reported drift meaning one thing. So the meter-to-feet round trip
(𝑥 in ft) in m gets the trivial ratio 1, the one-way 𝑥 in ft gets m/ft, and triviality is decidable
because ratios, like units, are exponent vectors over ℚ (Tw.nfOne_eq_one_iff).
   TheoRem 6.1 (DRift decides invaRiance; Twist.invariant_iff). A first-order program over
scalars, with result type Q 𝑢 and nonzero denotation, to which the analysis assigns a ratio is invariant
under all rescalings, that is, its denotation at 𝑉 𝜓 on inputs rescaled by 𝜓 is 𝜓 (𝑢) times its denotation
at 𝑉 for every 𝜓 , exactly when that ratio evaluates to 1 under every rescaling.
   The analysis computes the ratio (unitDrift_spec) and decides the condition. The sum rule is
where a decline is most likely to surprise. Both summands of (𝑥 in ft) + 𝑦 , for 𝑥 a meter input
and 𝑦 a foot input, have type Q ft, yet the analysis declines the sum (addMixed), and rightly: at
𝑥 = 𝑦 = 1 with 𝑉 (m) = 𝑉 (ft) = 1 the sum is 2; doubling the meter doubles 𝑥 and 𝑉 (m) while 𝑦
and 𝑉 (ft) stay put, and the sum becomes 2 ⋅ 2/1 + 1 = 5, where the type Q ft promised 2. Over
two meter inputs, (𝑥 in ft) + (𝑦 in ft) is accepted at drift m/ft (addTwoVars): both summands
move together. Declines are conservative, not complete: 0 ⋅ (𝑥 in ft) + 𝑦 is declined because its
summands’ ratios disagree, yet it denotes 𝑦 and is invariant. Exactness concerns assigned ratios,
whose triviality is decided exactly.
   Inputs are measurements and rescale with their units, so every input receives the trivial ratio,
whether it is a context variable or a leading 𝜆. A 𝜆 inside the term is different: its argument may
arrive with a drift of its own, so its bound variable receives a ratio variable standing for that un-
known drift. Comparison of ratios is exact, without reduction fuel, whenever the context holds
only scalar, vector, or matrix variables (Tw.normEq_firstOrder_iff); internal higher-order applica-
tions and unit binders are unrestricted. Contexts containing unknown functions or unit-indexed
families fall back to a bounded comparison that is sound but not proved complete.
9
 one is the SI’s name: quantities of dimension one carry “the unit one, symbol 1” [Bureau International des Poids et Mesures
2019]; here it is the empty exponent vector, whose dimension the object-oriented design [Allen et al. 2004] named Unity.
14                                                                                                Eric Allen


   The artifact’s ballistics kernel (Ballistics) computes a velocity squared, an energy per unit
mass, from a distance in feet and a time in seconds, and reports it four ways: back in its input
                                                2
units, certified drift-free; in metric, drift ft /m2 ; two routes summed, accepted at the shared drift;
and through a square root, drift ft/m, the exponent halved with the unit’s. The generic caster of
Section 2 has the drift u/v, a ratio containing unit variables, and the round trip through the caster,
out to v and back to u, is certified drift-free without instantiation (casterRound).
   Section 5 separated the two actions of a rescaling, on the values and on the valuation; the drift
keeps them apart. With its inputs held fixed, a program of drift 𝑤 is multiplied by 𝜑(𝑤) when the
valuation is rescaled by 𝜑 (den_comp_of_drift), so a drift-free program denotes the same number
under every valuation (den_indep_of_driftFree), and by adequacy (Section 7) so does the real-
arithmetic evaluator for a closed dimensionless one (evalC_indep_of_driftFree). With the valua-
tion held fixed instead, a drift-free program obeys Theorem 5.1’s scaling law although it converts
(scaleLaw_of_driftFree); this is the hypothesis Section 8 uses. Both specialize one law in which
the values are rescaled by 𝜓 and the valuation by 𝜑 at once: the factor is 𝜓 (𝑢) ⋅ 𝜑(𝑤) ⋅ 𝜓 (𝑤) for a
program of drift 𝑤 at result unit 𝑢 (unitDrift_law). The diagnostic extends to first-order programs
at vector and matrix types, with a drift per entry (unitDriftGen, scaleLaw_lin_of_driftFree_gen):
the Jacobi sweep of Section 9 converts nowhere, and every entry receives the trivial drift.

7 Adequacy and Erasure
Two theorems connect the semantics to the machine. They relate Section 4’s evaluator, which
carries a unit on every value and performs the dynamic checks (we call it instrumented), to an
erased evaluator that carries neither; both are developed in the artifact (modules LambdaS.Adequacy
and LambdaS.Erasure).
   TheoRem 7.1 (FactoRs Reach the machine; evalC_convert_declared). Let 𝑉 satisfy the decla-
ration 𝑢 = 𝑞 𝑣 , with 𝑢 a base unit and 𝑣 a unit of its dimension, and let 𝑒 be a closed term of type Q 𝑢 .
Instantiate the evaluator with real arithmetic and the conversion function that 𝑉 determines. Then
convert 𝑒 𝑢 𝑣 evaluates to the denotation of 𝑒 multiplied by exactly 𝑞 , at unit 𝑣 .
   A chain thus runs from the declaration, through the semantics, to the evaluator’s multiplica-
tion. The link from semantics to evaluator is adequacy (evalC_eq_den): with the conversion factors
the valuation determines, the evaluator instantiated with real arithmetic computes the denotation.
With the yard declared at 3 feet, the foot at 0.3048 meters, and, redundantly, the yard at 0.9144 me-
ters, one yard evaluates to 0.9144 meters through feet or directly, and the routes are provably equal
(one_yard_in_meters, one_yard_in_meters_via_feet, yard_routes_agree). Separately, the compiled
Float binary prints 91.44 for one hundred yards by either route; this executed example is not a real-
to-Float theorem.
  TheoRem 7.2 (ERasuRe; erasure_correct). For any numeric carrier, using the same arithmetic
and conversion function in both evaluators, every closed well-typed term of scalar type has a fuel
bound at which the instrumented evaluator returns a magnitude carrying exactly the unit its type
predicts and the erased evaluator returns exactly that magnitude.
   Units can thus be stripped from run-time values, together with every dynamic check, without
moving the numbers. Without conversion this is Kennedy’s dimension-erasure theorem [1996,
Theorem 5.4]. Kennedy [2010, §4.1] states the requirement: programs with and without unit anno-
tations behave the same. Conversion reads units, so it is where that requirement is at risk. Behind
the theorem is a simulation (eeval_erase). For any term, under any number of enclosing unit and
dimension binders and any environment, if the instrumented evaluator succeeds at fuel 𝑛 then the
erased evaluator succeeds at the same fuel and returns the erased value. The simulation needs no
A Calculus for Units of Measure with Conversion                                                      15


typing hypothesis; the instrumented run’s success already witnesses that every check the erased
run skips would have passed. With adequacy, the erased evaluator instantiated with real arith-
metic computes the denotation (eeval_den). Two things deliberately survive erasure, and neither
is a unit tag on a value. Array extents survive, because a matrix with zero rows has no entries from
which to recover its width. And the unit and dimension environments survive, because a polymor-
phic conversion takes its factor from a unit supplied at run time: data the size of the scope, not of
the payload, passed in dictionary-passing style [Wadler and Blott 1989]. Units are static except at
the finitely many scope entries that polymorphic conversion consults.

8 Dimensional Analysis
Two results remain: a non-definability theorem, which justifies a constructor of Λ𝑆 , and the Pi
theorem of dimensional analysis, the classical consequence of the abstraction theorem. The first is
the non-definability result of Kennedy [1997] in our setting. For 𝑢 ≠ 1, no term built from variables,
rational literals, and the field operations computes square root at Q 𝑢 2 → Q 𝑢 (sqrt_not_definable;
at the term level, sqrt_not_definable_tm), so the powers of Section 2 must be primitive. Kennedy’s
proof is semantic. Ours is linear algebra over the syntax, which the absence of recursion permits:
from an argument at 𝑢 2 and dimensionless literals, the field operations reach exactly the ℤ-span of
𝑢 2 , while 𝑢 = (𝑢 2 )1/2 needs the ℚ-span. Newton’s Method, 𝑥𝑛+1 = (𝑥𝑛 + 𝑎/𝑥𝑛 )/2, does not escape
it. Without the primitive, no term built from the field operations manufactures the seed 𝑥0 ∶ Q 𝑢
from 𝑎 ∶ Q 𝑢 2 (no_newton_seed_tm); with 1𝑢 as seed a finite unrolling is writable, but it denotes
a rational function of 𝑎, and no rational function is a square root. The seed fixes a scale, and the
iterates show it: from 1𝑢 on 4 m2 , one step gives 2.5 m in meters and 200.005 m in centimeters
(LambdaS.NonDefinability). The theorem is about exactness, not approximation; a primitive root
is what a units calculus needs to denote √ℓ/𝑔 , and it is parametric where a seeded iteration is not.
    The second result we illustrate with a common example. What determines the period 𝑇 of a
pendulum? Suppose we have decided that it could depend on the mass 𝑚 of the bob, the length ℓ
of the arm, the gravitational acceleration 𝑔 , and the release amplitude 𝜃 : 𝑇 = 𝑓 (𝑚, ℓ, 𝑔, 𝜃) for some
unknown 𝑓 . Record the exponents of each argument’s unit over the base units of mass, length,
and time as the columns of a matrix: 𝑔 is an acceleration, L/T2 , and the amplitude is an angle,
dimensionless, so its column is zero. This example uses one base unit per independent dimension,
so the unit rows and the dimension rows coincide:

                                                𝑚    ℓ 𝑔       𝜃
                                             M 1     0 0       0
                                         𝐴 = L (0    1 1       0)
                                             T  0    0 −2      0

A power product 𝑚𝑐1 ℓ𝑐2 𝑔 𝑐3 𝜃 𝑐4 of the arguments is dimensionless exactly when 𝐴𝑐 = 0, so the
dimensionless combinations are the kernel of 𝐴. Here 𝐴 has rank 3, the kernel has dimension
4 − 3 = 1, and solving 𝐴𝑐 = 0 forces 𝑐1 = 𝑐2 = 𝑐3 = 0: the amplitude is the only dimension-
less combination. The output 𝑇 has exponent vector 𝑏 = (0, 0, 1), and 𝐴𝑋 = 𝑏 has the solution
𝑋 = (0, 12 , − 12 , 0), the power product ℓ1/2 𝑔 −1/2 = √ℓ/𝑔 . The Pi theorem says that these two
computations determine 𝑓 up to one unknown function of one variable, 𝑇 = √ℓ/𝑔 ⋅ 𝐺(𝜃), and
mechanics contributes only 𝐺 , with 𝐺(𝜃) → 2𝜋 at small amplitude. Note what the mass row has
already decided: mass occurs in one argument and not in the output, so every solution and ev-
ery kernel vector has zero in the mass coordinate. The period’s independence from the bob’s mass,
which mechanics derives from the equation of motion, is read off the type (pendulum_mass_absent).
16                                                                                             Eric Allen


    This computation is the Pi theorem as Buckingham [1914] stated it: a physically meaningful
equation among 𝑛 quantities whose units involve 𝑟 independent base dimensions can be rewritten
as an equation among 𝑛 − 𝑟 dimensionless products of those quantities. The kernel of 𝐴 supplies
the products, and there are 𝑛 − 𝑟 of them because 𝐴 has rank 𝑟 . Kennedy [1997] showed that the
theorem is a consequence of parametricity: a well-typed program cannot depend on the choice
of units, and a function that cannot depend on the choice of units is a function of dimensionless
products. His calculus has no conversion. The question for ours is whether the theorem survives
it, and it does.

   TheoRem 8.1 (Pi, foR pRogRams with conveRsion; den_pi_coherent_dichotomy). Let a para-
metric first-order program take 𝑛 scalar arguments to a scalar result, in closed unit and dimension
scope; it may convert, and may bind units and dimensions internally. Let column 𝑖 of 𝐴dim hold the
dimension exponents of argument 𝑖, and 𝑏 those of the result. Then one of two cases holds. Either some
power product of the arguments has the result’s dimension, that is, 𝐴dim 𝑋 = 𝑏 is solvable, and on
positive arguments the program is that power product times a function of 𝑛 − rank 𝐴dim dimensionless
products of its arguments; or no power product does, and the program denotes zero on every argument.

   The pendulum is in the first case, with one dimensionless product, 𝜃 . The second case is a non-
definability theorem in disguise. Take a program that computes a period from a mass alone. Dou-
bling the unit of time while fixing the kilogram is a coherent rescaling. It leaves the argument
unchanged, and so the program’s output, while the scaling law demands that the output double;
so the output is zero. No power of a kilogram is a unit of time, and a program that respects rescaling
cannot manufacture one. The zero case needs no positivity of the arguments; only the factorization
does.
   The theorem holds with conversion because Theorem 5.2 does. A coherent rescaling preserves
every same-dimension conversion factor, and the evaluator consults only those factors (eval_
congr_sameDim), so the program computes the same number at 𝑉 and at 𝑉 𝜓 ; by normalization and
adequacy its denotation obeys the dimension-level scaling law (den_mulScaleLaw_coherent), even
where the drift analysis declines it (addMixed_coherent is the instance for Section 6’s declined sum).
The scope is closed because the proof runs through the evaluator, whose termination theorem is for
closed terms; a direct semantic proof would lift the restriction. From the scaling law the two cases
                                                                           𝑗
are linear algebra (mulScaleLaw_dichotomy): the 𝑛 − 𝑟 coordinates ∑𝑖 𝑐𝑖 log 𝑥𝑖 , for a rational basis
 1       𝑛−𝑟
𝑐 , … , 𝑐 of the kernel, are constant on rescaling orbits and separate them, so a function invariant
under rescaling is a function of them (invariant_descends, mulScaleLaw_factorization_reduced),
and with ℚ exponents rank-nullity gives the count (pi_count) where Kennedy’s ℤ-exponent proof
needs Smith normal form. Every step is mechanized, with the equivalence between functions obey-
ing a scaling law and scale-invariant functions proved in both directions (piEquiv, piEquivSigned);
Section 11 compares the statement with Kennedy’s.
   A stronger law is available to programs the drift analysis certifies. Independent unit rescalings,
which move the meter without the foot, form a larger group than dimension rescalings, and a
drift-free program respects all of them (den_mulScaleLaw_driftFree), as does every parametric
convert-free one (den_mulScaleLaw); neither needs the closed scope the coherent version does. For
these programs the matrix may have a row for each base unit and each unit variable rather than
for each dimension, and the two cases hold over that matrix too. The constraint is stronger: a meter
argument divided by a foot argument is dimensionless but has unit m/ft, so the unit-level theorem
does not let the program depend on it, where the dimension-level theorem does; and a program
from a meter argument to a foot result, dimensionally consistent as it is, falls in the zero case, since
no power of a meter is a foot.
A Calculus for Units of Measure with Conversion                                                     17


9 Dimensioned Linear Algebra
Dimensioned linear algebra is where units matter most in numerical code, and it is where the
invariance theory of Sections 5–6 meets code a numerical analyst would write. This section shows
that the type discipline those theorems assume for vectors and linear maps is Hart’s [1995], that
it costs nothing at run time, and that on a real kernel the theorems say two things untyped code
cannot.
   A vector of dimensioned entries poses no problem: each component carries its own unit, and a
state of position and momentum lives in the space [m, kg ⋅ m/s]. A matrix does. Hart observed that
a matrix of dimensioned entries cannot carry arbitrary units: for 𝑥 in Vec 𝑢⃗ and 𝐴𝑥 in Vec 𝑤⃗ , each
summand 𝐴𝑗𝑖 𝑥𝑖 of (𝐴𝑥)𝑗 = ∑𝑖 𝐴𝑗𝑖 𝑥𝑖 must carry the unit 𝑤𝑗 of the result component, so entry (𝑗, 𝑖)
carries 𝑤𝑗 /𝑢𝑖 , and the whole array of entry units is determined by two vectors of units, one for the
domain and one for the codomain. We say the array of entry units has rank one; this says nothing
about the numerical rank of the matrix. In Λ𝑆 , as in the type systems of Griffioen [2015, 2019] and
of McBride and Nordvall Forsberg [2022], the invariant is representational: a type Lin 𝑢⃗ 𝑤⃗ carries
its two spaces and nothing per entry, and the introduction rule T-MCons (Figure 2) accepts a row
only at the space 𝑤/⃗  𝑢 , so no term constructs a matrix outside Hart’s form. Type soundness carries
the two spaces, over an array of bare magnitudes, to the evaluator (lin_soundness_total); since
the two spaces determine every entry unit, the array loses nothing, and the compiled evaluator
passes vectors and matrices unboxed to a BLAS-shaped kernel [Lawson et al. 1979] (Section 10).
The eliminator row𝑗 returns a row at the type T-MCons demanded, so entries and transposes are
writable (fromTimeT).
   Hart went on to classify dimensioned matrices by the operations their units permit, and in Λ𝑆
each class is an identity of unit assignments, proved in a model of dimensioned matrices (module
LambdaS.Map) in which the unit of entry (𝑗, 𝑖) is defined as 𝑤𝑗 /𝑢𝑖 (entry), the unit T-MCons assigns
(HasTy.mcons_entry). A composite’s summand 𝐴𝑘𝑗 𝐵𝑗𝑖 carries (𝑤𝑘 /𝑣𝑗 )(𝑣𝑗 /𝑢𝑖 ) = 𝑤𝑘 /𝑢𝑖 , so Hart’s
“multipliable” condition is not a condition to check but the only composition writable (entry_comp).
On an endomorphism Lin 𝑢⃗ 𝑢⃗ every diagonal entry carries 𝑢𝑖 /𝑢𝑖 = 1, and so does every prod-
uct ∏𝑖 𝐴𝜎(𝑖) 𝑖 over a permutation 𝜎 , so trace and determinant are plain numbers (entry_id_diag,
                                                                             1   s/kg
entry_perm_prod): on the position-momentum space the entry units are ( kg/s 1 ), and written as
terms the trace and determinant typecheck at unit 1 and the 2 × 2 cofactor inverse as an endomor-
phism of the same space (traceTm, detTm, invTm), with the compiled binary checking that 𝐴−1 ∘ 𝐴
evaluates to the identity. A space is uniform when every component carries one unit, as [m, m]
does; between uniform spaces every entry carries the same unit (svd_entry_const), which is what
sorting singular values requires, and a space equals its dual, the space of componentwise reciprocal
units, exactly when it is dimensionless (transpose_comp_direct_iff), which is what composing a
Cholesky factor with its transpose requires (cholesky_factor_dimensionless). These are identities
of unit assignments; they do not implement a decomposition. The kernel below supplies a concrete
typing test.
   A 2 × 2 Jacobi step (sweep) rotates a symmetric matrix toward diagonal form to compute its
eigenvalues. A symmetric matrix is the matrix of a quadratic form, taking a vector 𝑥 to the covector
𝑦 ↦ 𝑦 T 𝐴 𝑥 , so on the uniform space 𝑈2 = [m, m] its type is Lin 𝑈2 𝑈2−1 with 𝑈2−1 = [1/m, 1/m]
its dual, and every entry carries m−2 . The step computes 𝜏 = (𝐴22 − 𝐴11 )/(2𝐴12 ), chooses the
corresponding cosine 𝑐 and sine 𝑠 , and forms 𝑅T 𝐴𝑅 with 𝑅 = ( −𝑠  𝑐 𝑠 ), which zeroes the off-diagonal
                                                                     𝑐
pair in exact arithmetic; the compiled numerical checks exercise both signs of the off-diagonal and
equal, unequal, and already-diagonal inputs within a floating-point tolerance. Two things about
this kernel are invisible in untyped code.
18                                                                                                                Eric Allen


   First, 𝜏 is a ratio of entries at one unit and so is dimensionless, and cosine and sine follow: the
rotation is a matrix of plain numbers whatever the space’s unit. On a non-uniform space the kernel
does not typecheck at all: its two diagonal entries carry different units, so the numerator of 𝜏 is an
addition at unequal units (Γ𝑁 in Examples.lean). Hart’s uniformity condition is not a hypothesis
a programmer must carry; it is the condition under which the code can be written.
   Second, a stopping test compares |𝐴12 | against a tolerance carrying the entries’ unit, and the
invariance theory distinguishes how that tolerance is supplied. A relative test, 𝜀 max(|𝐴11 |, |𝐴22 |)
for dimensionless 𝜀 , scales a quantity already in hand, names no unit constant, and stays inside the
parametric fragment, so Theorem 5.1 applies to the kernel. A fixed absolute tolerance written as a
literal times 1𝑢 names a unit and leaves that fragment (stopAbsolute); both forms typecheck, and
both run. An absolute tolerance supplied as an input rescales with its unit and remains parametric,
so what the theory forbids is not absolute tolerances but tolerances that fix a scale in the program
text. The drift analysis of Section 6 certifies the sweep itself drift-free, entry by entry. The kernel
examples test one stopping decision; iteration is outside a calculus without recursion.

10    Mechanization
The modules cited throughout develop each result in full, with rendered documentation. The devel-
opment is 10,900 lines of Lean 4 [de Moura and Ullrich 2021] definitions and proofs and 6,300 lines
of documentation (the artifact’s count_lines script counts LambdaS/*.lean), building with no ad-
mitted proofs (Lean’s sorry) and no axioms beyond the three of Lean’s standard library.10 It stays
that small because units are exponent vectors (Section 2), as in Kennedy’s Coq development [2008]
(over ℤ there): substitution is a linear map, and where Kennedy’s substitution lemma, over types
interpreted as Coq types, needs equality coercions he calls awkward, ours keeps types syntactic
and reorders a finite sum.
   Two things beyond the theorems. First, a defect the mechanization caught that every test missed:
a variable-capture bug in substitution, invisible to the weaken-then-substitute tests, where it can-
celed itself, exposed only when the composition law of substitutions was proved. The artifact repre-
sents variables as de Bruijn indices [de Bruijn 1972], with types and terms indexed by the number
of enclosing unit and dimension binders; the named variables of Figures 1 and 2 are a presenta-
tion choice. Scope indices rule out dangling unit and dimension variables, but not selection of the
wrong variable within a scope. The defect illustrates why substitution needs identity and compo-
sition laws in addition to examples.
   Second, the trusted base. A reader who believes a theorem trusts Lean’s kernel and its three
axioms. Concrete checker and diagnostic outcomes in Examples.lean, including the caster, Jacobi
sweep, its non-uniform rejection, and the reported drift tables, are mostly #guard assertions, ex-
ecuted by Lean’s compiler rather than checked by its kernel. Their execution adds the compiler
to the trusted base. Numerical regression checks, including the Jacobi residual and stopping deci-
sions, run in the native binary with Float. Kernel-checked typing derivations and parametricity
proofs are separate from these executed checks. A reader who believes the number the compiled
binary prints trusts, in addition, Lean’s code generator, the Float carrier, and three C functions
behind a BLAS-shaped interface: a dot product, a matrix-vector product, and a query naming the
backend. The denotational theorems use real arithmetic; they do not prove that floating-point eval-
uation equals it. Rounding affects defined operations. The carriers also totalize partial operations


10
  Propositional extensionality, choice, and quotient soundness. The kernel, Lean’s proof checker, checks every proof as part
of the build; that no theorem our paper cites depends on a further axiom is audited by a script in the artifact’s continuous
integration.
A Calculus for Units of Measure with Conversion                                                     19


differently: real division by zero and log 0 yield 0, while the binary follows its floating-point oper-
ations. Non-integer powers of negative values likewise use different conventions (Section 5); no
real-to-floating-point correspondence is claimed at these points. We claim no IEEE conformance;
the standard [IEEE 2019] itself requires correctly rounded field operations and square root, while
the transcendental functions are recommended operations, correctly rounded only when provided.

11   Related Work
In this section, we situate Λ𝑆 among the calculi it descends from, the practical systems that moti-
vated it, and the proof methods it borrows.
  Kennedy. Kennedy [1997] is the direct ancestor: a typed lambda calculus with units as a free
abelian group, unit polymorphism, the abstraction theorem, non-definability of square root, and
the Pi theorem as a type isomorphism derived from parametricity. Kennedy established several
surprising properties of unit systems, and nearly every design decision in Λ𝑆 inherits from it or
answers it. The differences are the ones our paper is about: Kennedy’s calculus has no conversion
operator (nothing in it can observe a unit), no dimensions distinct from units, and ℤ rather than
ℚ exponents. The later mechanization [Kennedy 2008] interprets types shallowly into Coq (“units
ignored”) over a base domain restricted to positive values. It has no terms yet, only semantic re-
sults over total Coq functions, so neither the bottom element that domain theory forced nor the
question of totality arises; his 2008 work-in-progress list includes formalizing the Pi theorem and
non-definability. His Pi theorem (Theorem 3) states the solvable case for 𝑛 arguments over ℤ expo-
nents, by Smith normal form, as a type isomorphism for positive values, and his Section 5.2 shows
every term of unsolvable signature trivial. Ours (Section 8) states both cases as one dichotomy
with outputs of either sign, has ℚ exponents, covers base units and unit variables jointly, and
mechanizes the equivalence with both round trips proved.
   Atkey, Johann, and Kennedy. Atkey et al. [2013] generalize the theory to types indexed by arbi-
trary algebraic structures, with an abstraction theorem over arbitrary index theories and a general
non-definability criterion for first-order types that subsumes Kennedy’s square-root result and
ours. Our development is narrower and deeper on one axis: in their units instance the index is a
group and no term reads it, which is why their abstraction theorem is unconditional on the term
language, where Λ𝑆 has an operator that does read it. In that configuration coherence becomes a
theorem rather than a vacuous condition. Their scaling law is a type isomorphism that splits off the
zero argument as one factor of a product, the same exception our nonzero hypotheses mark. From
it their paper derives a one-variable instance of the Pi theorem, ∀𝑠. real⟨𝑠⟩ → real⟨𝑠 2 ⟩ ≅ real⟨1⟩,
the area of a circle. Their Coq development contains the scalings, non-inhabitation, and the square
and cube root results, and proves the zero-argument isomorphism (the only polymorphic scalar
is zero); the instance ∀𝑠. real⟨𝑠⟩ → real⟨𝑠⟩ ≅ real⟨1⟩ is stated there in a comment with its proof
unfinished.
   Dimensions as a grading and several units per dimension are already McBride and Nordvall
Forsberg’s [2022]: their semiring is graded over the group of dimensions, so that a length in feet
and a length in meters already inhabit one graded component, and a unit system is a choice of one
unit per dimension used to render a quantity numerically. What is new here is a term former that
reads the choice, and the coherence condition reading it forces.
   Practical systems. Allen et al. [2004] formulate dimensions and units as classes with statically
typed metaclasses (given a core calculus by Tobin-Hochstadt and Allen [2005]), dynamic conver-
sion factors, nonlinear scales, and several units per dimension: the practical feature set Λ𝑆 gives a
theory to, minus the scales. The design entered the Fortress specification [Allen et al. 2006, §2.10],
20                                                                                          Eric Allen


whose in converts a measurement to another unit of the same dimension: Λ𝑆 takes both its nota-
tion and its side condition from that operator. The core calculus covered the metaclass mechanism
rather than conversion, and no invariance theorem was proved for either. F#’s units [Kennedy
2010] erase completely and convert by multiplication the programmer writes herself; the type sys-
tem checks the unit annotation on the literal factor but nothing ties the number 3.28084 to feet
and meters, and Theorem 7.1 is that tie. Gundry [2015] implements unit inference in GHC with
a typechecker plugin solving free-abelian-group constraints. That design indexes by units alone
and leaves separate dimensions and inferred conversions as further work. Our rational elimination
lemmas address unit equations; they do not settle the two-level inference question of Section 2. Os-
prey [Jiang and Su 2006] checks the factors C programmers write against magnitudes carried in its
units, and caught a mile-to-meter factor typed as 1682 in an annotated test program; it has no in-
variance theory. Karr and Loveman III [1978] proposed declared factors checked by row reduction
of their logarithms, over rational exponents, with the compiler inserting the conversion factor
the declarations determine; the Pascal proposals that followed reached the same problem from
the language side, and House [1983] was alone among them in seeing that units need polymor-
phism [Kennedy 1996, §1.3]. Trancón y Widemann and Lepper [2025] give declared conversions
an algebraic theory. Their Theorem 4.38 establishes consistency for well-defining conversions, and
Remark 4.40 conjectures residual finiteness as a route to deciding convertibility of closed conver-
sions. In our rational-exponent model, Theorem 3.1 characterizes consistency of finite declarations
with positive rational factors; the verified checker decides this without an acyclicity hypothesis.
Foster and Wolff [2023] build the ISQ (the International System of Quantities) in Isabelle/HOL
with the same exponent-vector representation of dimensions we use, ℤ exponents, and conver-
sion between unit systems. The unit system, not the unit, is their type-level grading: yard and foot
differ only at the value level, a distinction our types draw and theirs do not. Their formalization
has no language calculus and no invariance theory; it is a metrology library with proof automa-
tion, and a good one. Botta and Jansson [2026] formalize unit systems, the covariance principle,
and the statement of the Pi theorem in Idris, with ℤ exponents, and observe that its proofs, be-
ing non-constructive, are not implementable there, the obstacle being the excluded middle. Ours
use classical logic, as Lean’s real analysis does; they are proofs, not programs that compute the
factorization. Danish et al. [2024] report on incremental units verification for Fortran at scale,
in a preprint; their checker found the wrong conversion factor cited in our introduction. A recent
preprint [Haynes 2026] keeps dimension information through compilation so that value ranges can
drive numeric representation choices, an approach compatible with our erasure theorem, which
says the semantics ignores dimensions, not that a compiler must discard them.


    Methods. Fuel-based definitional interpreters and soundness-as-preservation over them are stan-
dard [Amin and Rompf 2017; Owens et al. 2016; Reynolds 1972], as are intrinsically typed inter-
preters [Poulsen et al. 2018] and the discharge of the fuel by a normalization theorem; we follow
all three. The accumulated-ratio analysis of Section 6 is in the family of graded and coeffect sys-
tems [Gaboardi et al. 2016; Orchard et al. 2019; Petricek et al. 2014]: each judgment carries an
element of an algebra recording how a term uses its context, here the net conversion. We know
of no prior grading by conversion. The nearest operation is the constant-multiplication primitive
of Atkey et al.’s [2013] distance-indexed instance (their §7), which records the factor in its index;
it is assumed in an operation context over a distance bound, not written as a term former over a
dimension grading. Among language operators, the nearest is Fortress’s in, which no calculus has
graded. Per-component units for linear algebra are due to Hart [1995]; Griffioen [2015, 2019] types
them with inference, and McBride and Nordvall Forsberg [2022] with dependent types graded by
A Calculus for Units of Measure with Conversion                                                    21


dimension. Typed index sets for array programs, as in Dex [Paszke et al. 2021], are the natural
neighbors of our Vec/Lin types.

12   Conclusion
We have presented a calculus in which conversion coexists with the theory that makes unit types
worth having. Every parametric term is invariant under coherent rescalings. For a first-order pro-
gram with nonzero output to which the analysis assigns a ratio, invariance under all rescalings is
equivalent to a trivial ratio; the ratio records dependence on declared magnitudes, and triviality
is decidable. The treatment extends to dimensioned vectors and linear maps (Section 9), and the
declared factors reach the real-arithmetic evaluator’s multiplication by theorem. Executable decla-
ration checking decides consistency and whether every same-dimension factor is determined, and
extracts those factors exactly. The artifact is complete from the checker to the compiled binary, and
small enough to read, because units are exponent vectors and their metatheory is linear algebra.
   Many extensions would be necessary for Λ𝑆 to become a usable language in practice. A first
tier adds let, fixpoints, a boolean type and its conditional, and size polymorphism for the vector
types. Their typing rules can retain the same unit equalities; extending the metatheory requires
separate proofs. Fixpoints would remove the normalization guarantee of Section 4, and extending
the diagnostic to recursive calls requires an account of equations for their accumulated ratios. One
of the most important extensions is a module system in which unit declarations are interfaces, so
that consistency and the availability of required conversion factors (Section 3), already checked
for a finite unit system, become linking-time obligations.
   A second line is completeness of the diagnostic under binders. Comparison is exact for ratios
with scalar, vector, or matrix inputs, including internal higher-order applications, without a fuel
bound. Unknown function and unit-family inputs retain a conservative comparison; proving suf-
ficient reduction fuel or replacing that fallback with a terminating normalizer remains open. Sep-
arately, distinct argument drifts are independent unless a call site establishes their agreement.
Exploiting that agreement needs ratio families defined only where their argument drifts agree.
   Finally, scales and defined zeros [Allen et al. 2004] require structure beyond the multiplicative
theory: affine offsets for temperature scales and timestamps, and logarithmic coordinates for deci-
bel levels. Extending the declaration discipline, coherence theorem, and drift analysis to these cases
remains open.

Acknowledgments
This paper and its artifact were developed in sustained collaboration with Claude Fable 5 (An-
thropic). Claude drafted and revised the prose under the author’s direction, engineered much of
the Lean mechanization, and strengthened the artifact each time review exposed a gap between
what the text claimed and what the proofs delivered; the author set the design, questioned the
claims, and made the calls, including the ones Claude got wrong first. Codex Astra (OpenAI) sub-
sequently revised the paper in response to human and AI reviews and extended the Pi mechaniza-
tion. Authorship policies rightly reserve authorship for those who can be accountable for the work;
the author reviewed every theorem and every sentence and bears sole responsibility. The author
thanks Scott Kilpatrick for comments on an earlier version of this paper.

Disclaimer
This document is being distributed for informational and educational purposes only and is not an
offer to sell or the solicitation of an offer to buy any securities or other instruments. The informa-
tion contained herein is not intended to provide, and should not be relied upon for, investment
advice. The views expressed herein are not necessarily the views of Two Sigma Investments, LP
22                                                                                                              Eric Allen


or any of its affiliates (collectively, “Two Sigma”). Such views reflect the assumptions of the au-
thor(s) of the document and are subject to change without notice. The document may employ data
derived from third-party sources. No representation is made by Two Sigma as to the accuracy of
such information and the use of such information in no way implies an endorsement of the source
of such information or its validity.
   The copyrights and/or trademarks in some of the images, logos or other material used herein
may be owned by entities other than Two Sigma. If so, such copyrights and/or trademarks are
most likely owned by the entity that created the material and are used purely for identification
and comment as fair use under international copyright and/or trademark laws. Use of such image,
copyright or trademark does not imply any association with such organization (or endorsement
of such organization) by Two Sigma, nor vice versa.

References
Eric Allen, David Chase, Joe Hallett, Victor Luchangco, Jan-Willem Maessen, Sukyoung Ryu, Guy L. Steele Jr., and Sam
   Tobin-Hochstadt. 2006. The Fortress Language Specification, Version 1.0𝛼 . Technical Report. Sun Microsystems.
Eric Allen, David Chase, Victor Luchangco, Jan-Willem Maessen, and Guy L. Steele Jr. 2004. Object-Oriented Units of
   Measurement. In Proceedings of the 19th ACM SIGPLAN Conference on Object-Oriented Programming, Systems, Languages,
   and Applications (OOPSLA ’04). ACM, 384–403. doi:10.1145/1028976.1029008
Nada Amin and Tiark Rompf. 2017. Type Soundness Proofs with Definitional Interpreters. In Proceedings of the 44th ACM
   SIGPLAN Symposium on Principles of Programming Languages (POPL ’17). ACM, 666–679. doi:10.1145/3009837.3009866
Allen V. Astin and H. Arnold Karo. 1959. Refinement of Values for the Yard and the Pound. Federal Register 24, 128 (1959),
   5348. FR Doc. 59-5442, July 1, 1959; approved June 25, 1959 by F. H. Mueller, Secretary of Commerce.
Robert Atkey, Patricia Johann, and Andrew J. Kennedy. 2013. Abstraction and Invariance for Algebraically Indexed Types.
   In Proceedings of the 40th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL ’13). ACM,
   87–100. doi:10.1145/2429069.2429082
Nicola Botta and Patrik Jansson. 2026. Types, Equations, Dimensions and the Pi Theorem. Journal of Functional Program-
   ming 36, Article 3 (2026), 43 pages. doi:10.46298/jfp.17762
Edgar Buckingham. 1914. On Physically Similar Systems; Illustrations of the Use of Dimensional Equations. Physical
   Review 4, 4 (1914), 345–376. doi:10.1103/PhysRev.4.345
Bureau International des Poids et Mesures. 2019. The International System of Units (SI). 9th edition. doi:10.59161/AUEZ1291
Adam Chlipala. 2013. Certified Programming with Dependent Types: A Pragmatic Introduction to the Coq Proof Assistant.
   MIT Press. doi:10.7551/mitpress/9153.001.0001
Matthew Danish, Dominic Orchard, and Andrew Rice. 2024. Incremental Units-of-Measure Verification. arXiv:2406.02174.
   Written in 2018 and archived in 2024.
Nicolaas G. de Bruijn. 1972. Lambda Calculus Notation with Nameless Dummies, a Tool for Automatic Formula Manipu-
   lation, with Application to the Church-Rosser Theorem. Indagationes Mathematicae (Proceedings) 75, 5 (1972), 381–392.
   doi:10.1016/1385-7258(72)90034-0
Leonardo de Moura and Sebastian Ullrich. 2021. The Lean 4 Theorem Prover and Programming Language. In Automated
   Deduction (CADE 28) (LNCS, Vol. 12699). Springer, 625–635. doi:10.1007/978-3-030-79876-5_37
Simon Foster and Burkhart Wolff. 2023. Automated Reasoning for Physical Quantities, Units, and Measurements in Is-
   abelle/HOL. In 27th International Conference on Engineering of Complex Computer Systems (ICECCS 2023). IEEE, 136–141.
   doi:10.1109/ICECCS59891.2023.00025
Marco Gaboardi, Shin-ya Katsumata, Dominic Orchard, Flavien Breuvart, and Tarmo Uustalu. 2016. Combining Effects
   and Coeffects via Grading. In Proceedings of the 21st ACM SIGPLAN International Conference on Functional Programming
   (ICFP ’16). ACM, 476–489. doi:10.1145/2951913.2951939
Jean-Yves Girard. 1972. Interprétation fonctionnelle et élimination des coupures de l’arithmétique d’ordre supérieur. Thèse
   d’État. Université Paris VII.
Jean Goubault. 1994. Inférence d’unités physiques en ML. In Journées Francophones des Langages Applicatifs (Collection
   didactique), P. Cointe, C. Queinnec, and B. Serpette (Eds.). INRIA, Noirmoutier, 3–20.
P. R. Griffioen. 2015. Type Inference for Array Programming with Dimensioned Vector Spaces. In Proceedings of the 27th
   Symposium on the Implementation and Application of Functional Programming Languages (IFL ’15). ACM, 4:1–4:12. doi:10.
   1145/2897336.2897341
P. R. Griffioen. 2019. A Unit-Aware Matrix Language and its Application in Control and Auditing. Ph. D. Dissertation.
   Universiteit van Amsterdam. https://pure.uva.nl/ws/files/42206706/Thesis.pdf
A Calculus for Units of Measure with Conversion                                                                         23


Adam Gundry. 2015. A Typechecker Plugin for Units of Measure: Domain-Specific Constraint Solving in GHC Haskell. In
   Proceedings of the 2015 ACM SIGPLAN Symposium on Haskell (Haskell ’15). ACM, 11–22. doi:10.1145/2804302.2804305
George W. Hart. 1995. Multidimensional Analysis: Algebras and Systems for Science and Engineering. Springer, New York.
   doi:10.1007/978-1-4612-4208-6
Houston Haynes. 2026. Dimensional Type Systems and Deterministic Memory Management: Design-Time Semantic Preser-
   vation in Native Compilation. arXiv:2603.16437.
R. T. House. 1983. A Proposal for an Extended Form of Type Checking of Expressions. Comput. J. 26, 4 (1983), 366–374.
   doi:10.1093/comjnl/26.4.366
IEEE. 2019. IEEE Standard for Floating-Point Arithmetic. IEEE Std 754-2019. doi:10.1109/IEEESTD.2019.8766229
Lingxiao Jiang and Zhendong Su. 2006. Osprey: A Practical Type System for Validating Dimensional Unit Correctness
   of C Programs. In Proceedings of the 28th International Conference on Software Engineering (ICSE ’06). ACM, 262–271.
   doi:10.1145/1134285.1134323
Michael Karr and David B. Loveman III. 1978. Incorporation of Units into Programming Languages. Commun. ACM 21, 5
   (1978), 385–391. doi:10.1145/359488.359501
Andrew J. Kennedy. 1996. Programming Languages and Dimensions. Technical Report UCAM-CL-TR-391. University of
   Cambridge, Computer Laboratory. doi:10.48456/tr-391 PhD thesis, submitted November 1995.
Andrew J. Kennedy. 1997. Relational Parametricity and Units of Measure. In Proceedings of the 24th ACM SIGPLAN-SIGACT
   Symposium on Principles of Programming Languages (POPL ’97). ACM, 442–455. doi:10.1145/263699.263761
Andrew J. Kennedy. 2008. Formalizing an Extensional Semantics for Units-of-Measure. Talk, 3rd Informal ACM SIGPLAN
   Workshop on Mechanizing Metatheory (WMM ’08). https://www.cis.upenn.edu/~sweirich/wmm/wmm08/kennedy.pdf
   Slides; they describe the accompanying Coq development.
Andrew J. Kennedy. 2010. Types for Units-of-Measure: Theory and Practice. In Central European Functional Programming
   School (CEFP 2009). LNCS, Vol. 6299. Springer, 268–305. doi:10.1007/978-3-642-17685-2_8
Charles L. Lawson, Richard J. Hanson, David R. Kincaid, and Fred T. Krogh. 1979. Basic Linear Algebra Subprograms for
   Fortran Usage. ACM Trans. Math. Software 5, 3 (1979), 308–323. doi:10.1145/355841.355847
Mars Climate Orbiter Mishap Investigation Board. 1999. Mars Climate Orbiter Mishap Investigation Board: Phase I Report.
   Technical Report. NASA. https://llis.nasa.gov/llis_lib/pdf/1009464main1_0641-mr.pdf November 10, 1999; chaired by
   Arthur G. Stephenson.
Conor McBride and Fredrik Nordvall Forsberg. 2022. Type Systems for Programs Respecting Dimensions. In Advanced
   Mathematical and Computational Tools in Metrology and Testing XII, F. Pavese, A. B. Forbes, N. F. Zhang, and A. G.
   Chunovkina (Eds.). Series on Advances in Mathematics for Applied Sciences, Vol. 90. World Scientific, 331–345. doi:10.
   1142/9789811242380_0020
National Institute of Standards and Technology and National Oceanic and Atmospheric Administration. 2020. Deprecation
   of the United States (U.S.) Survey Foot. Federal Register 85, 193 (2020), 62698–62708. FR Doc. 2020-21902, October 5,
   2020; deprecation effective December 31, 2022.
Dominic Orchard, Vilem-Benjamin Liepelt, and Harley Eades III. 2019. Quantitative Program Reasoning with Graded Modal
   Types. Proceedings of the ACM on Programming Languages 3, ICFP (2019), 110:1–110:30. doi:10.1145/3341714
John-Paul Ore, Carrick Detweiler, and Sebastian Elbaum. 2017. Lightweight Detection of Physical Unit Inconsistencies
   without Program Annotations. In Proceedings of the 26th ACM SIGSOFT International Symposium on Software Testing
   and Analysis (ISSTA ’17). ACM, 341–351. doi:10.1145/3092703.3092722
Scott Owens, Magnus O. Myreen, Ramana Kumar, and Yong Kiam Tan. 2016. Functional Big-Step Semantics. In Program-
   ming Languages and Systems (ESOP 2016) (LNCS, Vol. 9632). Springer, 589–615. doi:10.1007/978-3-662-49498-1_23
Adam Paszke, Daniel D. Johnson, David Duvenaud, Dimitrios Vytiniotis, Alexey Radul, Matthew J. Johnson, Jonathan
   Ragan-Kelley, and Dougal Maclaurin. 2021. Getting to the Point: Index Sets and Parallelism-Preserving Autodiff for
   Pointful Array Programming. Proceedings of the ACM on Programming Languages 5, ICFP (2021), 88:1–88:29. doi:10.
   1145/3473593
Tomas Petricek, Dominic Orchard, and Alan Mycroft. 2014. Coeffects: A Calculus of Context-Dependent Computation. In
   Proceedings of the 19th ACM SIGPLAN International Conference on Functional Programming (ICFP ’14). ACM, 123–135.
   doi:10.1145/2628136.2628160
Casper Bach Poulsen, Arjen Rouvoet, Andrew Tolmach, Robbert Krebbers, and Eelco Visser. 2018. Intrinsically-Typed
   Definitional Interpreters for Imperative Languages. Proceedings of the ACM on Programming Languages 2, POPL (2018),
   16:1–16:34. doi:10.1145/3158104
John C. Reynolds. 1972. Definitional Interpreters for Higher-Order Programming Languages. In Proceedings of the ACM
   Annual Conference, Volume 2. ACM, 717–740. doi:10.1145/800194.805852
Bertrand Russell. 1903. The Principles of Mathematics. Cambridge University Press, Cambridge.
William W. Tait. 1967. Intensional Interpretations of Functionals of Finite Type I. Journal of Symbolic Logic 32, 2 (1967),
   198–212. doi:10.2307/2271658
24                                                                                                         Eric Allen


Sam Tobin-Hochstadt and Eric Allen. 2005. A Core Calculus of Metaclasses. In Foundations of Object-Oriented Languages
   (FOOL ’05). https://homepages.inf.ed.ac.uk/wadler/fool/program/final/7/7_Paper.pdf
Baltasar Trancón y Widemann and Markus Lepper. 2025. A Theory of Conversion Relations for Prefixed Units of Measure.
   Fundamenta Informaticae 195, 1–4, Article 11 (2025), 45 pages. doi:10.46298/fi.12436
Philip Wadler and Stephen Blott. 1989. How to Make Ad-Hoc Polymorphism Less Ad Hoc. In Proceedings of the 16th ACM
   SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL ’89). ACM, 60–76. doi:10.1145/75277.75283
Mitchell Wand and Patrick M. O’Keefe. 1991. Automatic Dimensional Inference. In Computational Logic: Essays in Honor
   of Alan Robinson, Jean-Louis Lassez and Gordon Plotkin (Eds.). MIT Press, 479–486.
