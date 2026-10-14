                                         SolutionsX: supergravity theories/solutions as code

                                         with an agentic workflow for machine-verifiable physics


                                         Vasil Dimitrova
                                         a
                                             INRNE, Bulgarian Academy of Sciences, Tsarigradsko Chaussee 72, 1784 Sofia, Bulgaria

                                             E-mail: vasildimi@gmail.com

                                         Abstract: A supergravity solution in the literature is an artifact that cannot be verified
                                         without re-deriving it: conventions might not be clearly stated, papers have typos, algebra
arXiv:2609.07826v1 [hep-th] 7 Sep 2026




                                         is tedious. SolutionsX is a Mathematica package that turns an xAct environment, whatever
                                         physics it may describe, into a stored, machine-verifiable record: code that replays in a fresh
                                         kernel, carries its own verification, and can later be fetched for re-use or extension. The
                                         shipped examples are supergravity theories and their solutions, but the scope is anything
                                         xAct reaches: abstract tensors, differential forms, spinors in any dimension. We follow
                                         one published solution through the entire workflow, benchmark the package’s component
                                         engine against xAct’s, and report on three blind runs of an agentic workflow in which an
                                         AI coding agent, given the package and a small toolkit, correctly codified a recent paper
                                         in under three hours. A database of such records is useful to researchers today and gives
                                         agents worked examples to learn from. The package acts as an internal verifier during the
                                         thought process of an agent: a claim is checked in the kernel before it is made.

                                         Program summary:
                                                Program title:              SolutionsX
                                                Version:                    2.1.0
                                                Programming language:       Mathematica (version 13.3 or later)
                                                Dependencies:               xAct
                                                Obtainable from:            github.com/waskou/SolutionsX
                                                                            or the Wolfram Paclet Repository
                                                License:                    AGPL-3.0-or-later (code)
                                                                            CC BY 4.0 (bundled data)
                                                Mascot:
Contents

1 Introduction                                                                             1

2 Installation                                                                             4

3 The life of a solution                                                                   6
  3.1 Fetching the parent theory                                                           6
  3.2 Inputting the solution                                                               8
  3.3 Computing the tensor components of the solution                                     13
  3.4 Verifying the solution                                                              16
  3.5 The solution can now play with its friends                                          18

4 Benchmarking: SolutionsX vs xCoba                                                       23
  4.1 Flexibility                                                                         24
  4.2 Need for speed and quality                                                          24

5 SolutionsX and agents                                                                   26
  5.1 The agent toolkit                                                                   27
  5.2 Example blind runs                                                                  29

6 Discussion                                                                              32

A Mathematica notation                                                                    36

B Public symbols of SolutionsX                                                            39

C Configuring the agent toolkit                                                           47




1    Introduction

There is a plethora of computer algebra systems (CAS) that can handle differential geom-
etry, tensor calculus and explicit-coordinates-calculations. A person working with super-
symmetry, or more generally one who wants to couple fermions to gravity — dynamical
or as a fixed background — requires a CAS that can also handle spinors, gamma matri-
ces, generalized connections, . . . , preferably in arbitrary dimensions. We are aware of the
following pieces of software that achieve that in various capacity:

    • xAct [1]: a free suite of packages for abstract tensor calculus (xTensor), component
      calculus (xCoba), exterior calculus (xTerior), spinors and fermions (FieldsX [2]), and
      more, running on top of the commercial Mathematica.




                                            –1–
   • Cadabra2 [3]: a free standalone CAS designed specifically for field-theory problems.

   • SageManifolds [4]: differential geometry and tensor calculus within the free, Python-
     based SageMath system.

   • DifferentialGeometry [5]: tensor calculus and Newman–Penrose/spinor formalisms
     within the commercial Maple.

SolutionsX builds upon xAct. It is a combination of three key functionalities

  (i) Ability to work with spinors and fermionic fields in arbitrary dimension — already
      present in xAct, most importantly through FieldsX

 (ii) An open database of theories and their solutions, whose entries are verifiable, re-
      usable and subject to human/agent contributions

(iii) Fast and flexible computations of tensor components — for any type of tensor, car-
      rying indices in any vector bundle — with ability to parallelize1

Essentially, SolutionsX is a “wrapper” over an existing xAct environment2 , such that the
environment can be stored and re-played at will in a new kernel. As such it automatically
ports the capabilities of xAct and its associated sub-packages — and it is deliberately
agnostic about what the environment describes. In practice a stored record is one of two
kinds. A theory is an abstract environment: a manifold, a metric with no chart attached,
the field content, and the distinguished expressions that define the physics — equations of
motion, supersymmetry variations, Killing-spinor conditions, the latter built on FieldsX.
A solution is the same environment specialized to explicit coordinates — charts, component
metrics, fluxes, Killing spinors — together with the replayed computations that verify it.
Neither notion is tied to supergravity: a QFT with fermions, supersymmetric or not, on
a fixed curved background is the same kind of environment with the metric simply non-
dynamical, and is covered automatically. The examples throughout the paper are drawn
from supergravity and holography, since that is the expertise of the author, not because
the system cannot handle more general setups. Of course SolutionsX, like xAct, lives on
the geometric side of such a problem — backgrounds, spinors, variations — and does not
attempt loop calculations. In all cases the user computes once and stores for the future.
     Before the broader vision, the pragmatic question: what does a user gain the day they
install SolutionsX? Fetching a stored theory replaces re-deriving it: conventions, field
content and defining equations arrive as code that loads in seconds. A finished calculation
becomes an entry that replays on a fresh kernel, so it can be re-checked, extended, or handed
over years later. Stored entries work together: in Section 3 one black hole is obtained as a
limit of another, and a holographic computation is spread across five cooperating entries.
Finally, the package is what turns an AI agent into a useful collaborator on such problems,
which is the subject of Section 5.
  1
   The words “fast” and “flexible” will be quantified in Section 4
  2
   By that we mean all the symbols that the user defines using xAct, together with any computations
done in a given kernel session




                                              –2–
     Now for the broader vision, with more users and more worked out examples the aim
is to have:

     A database of theories and solutions which are verifiable code, not merely arXiv
     prose

The idea behind this is clear and mathematics is already demonstrating the utility. Once
statements live in a form a machine can check, correctness stops being a matter of trust (or
time spent verifying) and collaboration scales up: Lean’s library mathlib now counts over
280 000 verified theorems from nearly 800 contributors, and the Liquid Tensor Experiment
formalized a central theorem of condensed mathematics within eighteen months of Scholze’s
challenge. The same substrate admits machines as contributors: AlphaProof [6], searching
over Lean proofs, reached silver-medal standard at the 2024 International Mathematical
Olympiad — possible precisely because every candidate proof could be verified. In 2026
the pace of progress is on a different level: working through a curated database of nearly a
thousand Erdős problems, agents delivered the first fully autonomous resolution of one [7]
(#728, January 2026, proof in Lean), and by mid-2026 the community tracker recorded AI
contributions to over a hundred more — genuinely new proofs, including a disproof of the
unit-distance conjecture posed in 1946 [8], next to many rediscoveries of results buried in
the literature. We aim at a hep-th analogue currently restricted to supergravity and QFT
on a fixed background: a stored theory or solution is code that re-runs, so a contribution
— from a colleague or from an agent — is machine verifiable. This removes a familiar
bottleneck of chasing conventions/typos in papers and allows one to build upon a trusted
source. The long-term goal is that a reliable database of theories and solutions will not
only be useful to human researchers, but will allow agents to “learn from the existing code”
and contribute meaningfully to novel research. The division of labour deserves to be stated
plainly: there is no AI inside the package. SolutionsX is deterministic computer algebra;
the AI enters as a user of it, reading the corpus for worked examples, authoring new entries,
and consulting the kernel as an independent verifier.
     In addition to xAct’s built in functionality, SolutionsX defines a handful of functions
that the author deemed important in their own workflow which extend xAct’s capabil-
ities. These additions are mainly concerned with converting between differential forms
representation and tensor representation of geometric objects, see MakeArray, MakeMetric,
MakeForm, ExpandForms, WedgeCoeff, ComputeDiffs.
     The paper is organized as follows. Section 2 contains the installation instructions.
Section 3 follows a single record through its life: how a theory and a solution are entered,
computed, verified, stored and reused. Section 4 benchmarks the component engine against
xCoba’s native one on two five-dimensional black-hole records. Section 5 presents the agent
toolkit and three blind runs in which an agent re-works three published physics problems.
Section 6 classifies types of problems that the author deemed amenable to codification.
Section A collects the Mathematica notation the paper’s cells rely on, Section B lists every
public symbol with its usage message, and Section C documents the configuration of the
agent toolkit.




                                           –3–
2       Installation

Installation is in three steps: the prerequisites, the package itself, and a first-session wizard.
Steps 1 and 3 are identical for everyone. Step 2 comes in two routes, and the choice depends
on whether you want the package alone or the whole repository around it.

Step 1: prerequisites (both routes) SolutionsX runs in Mathematica, version 13.3
or newer, and builds on two packages that have to be installed first. Both are installed
by placing files in a specific folder, and Mathematica itself tells you where that folder is:
evaluate in a notebook
                                                                                          In[1]:=
    FileNameJoin[{$UserBaseDirectory, "Applications"}]

and the printed path is the folder3 , called Applications below. Three items go into it:

    • xAct. Download the bundle from its download page and unzip it; the result is a folder
      named xAct. Move that folder into Applications.
    • FieldsX [2]. On its repository page press the Code button and choose Download
      ZIP; unzip the download.       From the resulting folder copy the single file
      FieldsX.m into the xAct folder of the previous item, so that now it is located
      at Applications/xAct/FieldsX.m.
    • Multisets.m. FieldsX relies on this one further file, downloaded from the Wolfram
      Library Archive and placed directly in Applications, beside the xAct folder, at
      Applications/Multisets.m.

IMPORTANT: FieldsX.m should sit inside the xAct folder, which is inside the
Applications folder; Multisets.m should sit beside the xAct folder, directly in the
Applications folder.

Step 2, route A: the paclet The package, its documentation and the curated example
entries ship together, and installing them is one line, evaluated in any notebook
                                                                                          In[2]:=
    PacletInstall["VasilDimitrov/SolutionsX"]

which fetches the package from the Wolfram Paclet Repository.
IMPORTANT: The install line above needs wolframcloud.com to be reachable. At the
time of writing the Wolfram Cloud is undergoing an internal update. Until that update is
complete, use route B.

Step 2, route B: the repository Take this route if you want more than the package:
the data directory with the published corpus (including the agent-authored entries of Sec-
tion 5), the agent toolkit agent/, and the package source. It is also the starting point for
contributing entries of your own. The repository lives at github.com/waskou/SolutionsX,
    3
    Typically ~/Library/Mathematica/Applications on macOS and ~/.Mathematica/Applications on
Linux; newer installations say Wolfram in place of Mathematica.




                                              –4–
and installing it means getting a copy of that folder onto your computer, then running its
setup script. Getting the copy, with or without git:

   • With git (recommended). Open a terminal and run

            git clone https://github.com/waskou/SolutionsX.git

        The folder SolutionsX appears; a later git pull inside it fetches updates, and con-
        tributing back runs through git as well.
   • Without git.       Open the page in a browser, press the Code button, and choose
        Download ZIP. Unzip the downloaded file; the result is the same folder, named
        SolutionsX-main4 . Move it wherever you want to keep it. Beware that the ZIP
        is a plain snapshot with no update mechanism: to update you download a fresh copy
        and move your own Data alias folder into it by hand, which is why we recommend
        the git route.

Now run the setup script from inside that folder: open a terminal, type cd followed by a
space and the folder’s path, press enter, and then run
       wolframscript -file setup.wls
The wolframscript executable ships with Mathematica. The script builds the paclet from
the repository, installs it, and points your SolutionsX configuration at the repository’s
Data directory.
IMPORTANT: The repository folder itself stays where you put it: unlike the prerequisites
of step 1, nothing is copied or moved into Applications.

Step 3: the first session (both routes)              Load the package with
                                                                                                  In[3]:=
  Needs["VasilDimitrov`SolutionsX`"]

and run the welcome wizard once
                                                                                                  In[4]:=
  Welcome[]

The wizard sets up your local storage: where the data lives (on route B this is already
the repository’s Data directory), the alias under which your own entries will be saved, and
which curated entries to copy under it. The answers are remembered, so every later session
starts directly with Needs["VasilDimitrov`SolutionsX`"]. With the package loaded, one
of the shipped solutions is fetched and loaded with
                                                                                                  In[5]:=
  sol = GetData["Curated/Sol__4dL__Black-hole__Global"];
  Load@sol

and if the wizard copied the curated entries under your own alias, the bare name suffices

   4
    The -main suffix is GitHub’s naming and is harmless; if you prefer to rename or move the folder, do it
before running the setup script, which records the folder’s location.




                                                  –5–
                                                                                      In[6]:=
    sol = GetData["Sol__4dL__Black-hole__Global"];

Authoring a new solution starts with
                                                                                      In[7]:=
    NewData[]

which opens a new notebook with the initialization cell already in place. The available
entries are browsed interactively with
                                                                                      In[8]:=
    ShowData[]

and the in-package documentation opens with
                                                                                      In[9]:=
    SolutionsXHelp[]

The usage message of a symbol prints directly with
                                                                                     In[10]:=
    ?Compute

and the ⃝ i icon in the message opens the symbol’s documentation page, exactly as for the
built-in Mathematica symbols.

3     The life of a solution

In this section we exemplify how a solution gets created, what information about it is stored
and where, how computations are done, and how the solution relates to other theories
and solutions. The presentation favours narrative structure, so not everything needed to
reproduce the example in a Mathematica kernel is explicitly shown. Section A collects
the Mathematica idioms the cells below rely on. The section mainly follows the example
entries:

    • Curated/Thr__5dL__Minimal-gauged

    • Curated/Sol__5dL__CCLP-susy__Orthotoric

3.1    Fetching the parent theory
What counts as a theory (Thr) and what counts as a solution (Sol) is determined by the
rudimentary question: Does the xAct environment define a local chart? If no, it is a theory;
if yes, a solution. Otherwise the distinction is merely semantics.
     We begin by fetching the already stored theory. In this case this is 5d minimal super-
gravity whose Lorentzian bosonic action is
                            Z "                                            #
                      1              12            C2          C3
                                          
                 S=                R− 2       ⋆ 1 − x F ∧ ⋆F − √x A ∧ F ∧ F ,           (3.1)
                    16πG5            ℓ5             2         3 3
where G5 is Newton’s constant, ℓ5 is the AdS5 scale and Cx is the placeholder for a possibly
different normalization of the gauge field. We fetch and load it with




                                                –6–
                                                                                                          In[11]:=
  sol = GetData["Curated/Thr__5dL__Minimal-gauged"];
  Load@sol

                                                                                                          Out[11]=
  Loaded:
  M, TM, m , n , o , p , q , r , s , t , u , v , w , x , y , z , PerturbationParametergg, gg, cd, epsilongg,
  Torsioncd, Christoffelcd, Riemanncd, Riccicd, RicciScalarcd, Einsteincd, Weylcd, TFRiccicd,
  Kretschmanncd, SymRiemanncd, Schoutencd, SchoutenCCcd, EinsteinCCcd, Detgg, Perturbationgg,
  Koszulcd, CovDcd, ηη , FM, ee, Detee, epsilonηη , a, b, c, d, e, f, g, h, i, j, k, l, SM,
  AChristoffelcd, FRiemanncd, Gammagg1, Gammaηη 1, Gammagg0, Gammaηη 0, Gammagg2, Gammaηη 2, Gammagg3,
  Gammaηη 3, Gammagg4, Gammaηη 4, Gammagg5, Gammaηη 5, A, B, C, D, E, F, G, H, I, J, K, L, ωω ,
  Riemannωω , Ricciωω , RicciScalarωω , PDflat, flat, TorsionPDflat, ChristoffelPDflat, RiemannPDflat,
  RicciPDflat, AChristoffelPDflat, FRiemannPDflat, etaUpflat, etaDownflat, flat0, flat1, flat2,
  flat3, flat4, KoszulPDflat, CovDPDflat, PDspin, spin, TorsionPDspin, ChristoffelPDspin,
  RiemannPDspin, RicciPDspin, AChristoffelPDspin, FRiemannPDspin, etaUpspin, etaDownspin, spin1,
  spin2, spin3, spin4, KoszulPDspin, CovDPDspin, TA, A, TF, F, ϵϵ, barϵϵ, G5, l5, Cx
  Info[...]



The output is a live panel: clicking on a symbol shows its Information panel, and clicking
again closes it. Only a small part of what is listed was fed in by hand when Curated/Thr_
_5dL__Minimal-gauged was authored:

   • $manifold — the spacetime M: five-dimensional, with abstract indices m, n, . . . , z
     on its (automatically created) tangent bundle TangentM, printed TM, and the Name
         "Minimal-gauged"

   • $metric — the metric gg, declared with Signature → -1 and no chart, and its Levi-
     Civita connection cd
   • $frame — the vielbein ee[−m, a] and the flat metric ηη [−a, −b], where a, b, . . . , l
     are the indices on the automatically created vector bundle FrameM, printed FM.
   • $spinStructure — over gg with spinor indices A, B, . . . , L for the vector bundle
     SpinM, printed SM5

   • $spinConnection — ωω[−m, −a, −b] associated to the Levi-Civita connection cd.
   • $basis — the two bases: flat on the frame bundle FM, colored , numbered 0 . . . 4;
     and spin on the spin bundle SM, colored , numbered 1 . . . 46
   • $form — the gauge potential A[] (differential form of degree one) and its field strength
     F[] (differential form of degree two). Each one arrives with a tensor partner, TA[−m ]
     and TF[−m, −n ], automatically created by SolutionsX7
   • $spinor — the Dirac spinor ϵϵ[−A], and with it its bar.
   5
       Now a curved γ-matrix is called as, eg. Gammagg2[−m, −n, −A, B] and a flat γ-matrix is called as
Gammaηη 2[−a, −b, −A, B]; the trailing digit is the rank, and the heads run Gammagg0 to Gammagg5 in five
dimensions
   6
     ToBases    now converts Gammaηη 2[−a, −b, −A, B] into Gammaηη 2[{−a, −flat}, {−b, −flat},
{−A, −spin}, {B, spin}] and it prints as γ[ηη]abAB , each index wearing its basis colour
   7
     Notice the [] after the form symbols; this is xTerior’s way to denote forms that carry no indices. For
an example with tensor-valued forms consult Curated/Thr__5dL__STU-gauged.




                                                      –7–
  • $constant — G5 , ℓ5 and Cx , the constants of the action above.

The rest is everything xAct automatically defines. The entry’s own name is “deduced”:
no chart makes it a Thr, Dimension → 5 with Signature → -1 makes it 5dL, and
sol[$manifold, M, Name] is appended to that. Aside from that Curated/Thr__5dL__
Minimal-gauged calls IncludeTo[sol[$set]] to store the equations of motion

                                                                                          In[12]:=
  E gg[-m , -n ]

                                                                                          Out[12]=
                      4 ggmn                 Cx2      o         Cx2                  op
                               + R[∇]mn −          TFm TFno +         ggmn TFop TF
                         l52                  2                  12

                                                                                          In[13]:=
  E TA[-m ]

                                                                                          Out[13]=
                                      Cx ϵggmnopq TFno TFpq              n
                                  −            √              + ∇n TFm
                                              4 3

which were previously derived from the Lagrangian using xAct’s built-in functions; and the
Killing spinor equation
                                                                                          In[14]:=
  δψψ [-m , -A]

                                                                                          Out[14]=
                      √
                     i 3 Cx TAm ϵϵA γ[gg]mAB ϵϵB i Cx γ[gg]n AB TFmn ϵϵB
                   −               −            +           √
                          2 l5          2 l5              2 3
                         i Cx γ[gg]monA B TFon ϵϵB 1
                     −              √             + γ[ηη]baAB ϵϵB ωωmba + ∂m ϵϵA
                                   8 3             4

which one can in principle derive from scratch using FieldsX, once the fermionic terms
are supplied to (3.1). What is useful about this setup is that Load loaded that entire xAct
environment. The theory and its defining expressions are derived once, then called upon
whenever needed. For a more involved pre-built theory, one carrying vector multiplets, see
Curated/Thr__5dL__STU-gauged.

3.2   Inputting the solution
Having loaded the theory, we “append” to it the data that specifies a concrete solution. In
the example below we build up towards a known solution; one can also build up an ansatz
and solve for it afterwards.
    We exemplify that step with the supersymmetric limit of the CCLP black hole, see
[9–11]. In the orthotoric coordinates {y, x, ρ, Φ, Ψ} it is the field configuration

                          ds2 = − (e0 )2 + (e1 )2 + (e2 )2 + (e3 )2 + (e4 )2 ,
                                  √ 
                                    3 0 ℓ5
                                                                                            (3.2)
                           A= −          e + P − f0 dy + dλ ,
                                  Cx           3




                                                   –8–
where f0 is a constant gauge shift, λ(x, Φ, Ψ) a gauge shift function, and the frame is

                               e0 = f (dy + ϖ) ,
                                         s
                                             x−ρ
                               e1 = ℓ5           dρ ,
                                              fF
                                         s
                                2                F
                               e = ℓ5                  (dΦ + x dΨ) ,
                                             f (x − ρ)                                       (3.3)
                                             s
                                                 x−ρ
                               e3 = − ℓ5             dx ,
                                                  fG
                                         s
                                4                G
                               e = ℓ5                  (dΦ + ρ dΨ) .
                                             f (x − ρ)

Above f = f (ρ, x), F = F (ρ) and G = G(x), while ϖ and P are the one-forms
   ℓ5 (F ′′′ + G ′′′ )                 1        1
                                                                                           
ϖ=                 2
                           F + (x − ρ) F ′ − F ′′′ (ρ − m1 )2         (dΦ + x dΨ) + G(dΦ + ρ dΨ)
    48(x − ρ)                          2        4
       ℓ5 F G′′′ ′′′
   −                 ((x + ρ) dΦ + xρ dΨ) + dχ ,
          288
            1
                      F ′ (dΦ + x dΨ) + G ′ (dΦ + ρ dΨ) ,
                                                       
P= −
       2(x − ρ)
                                                                                             (3.4)

with χ(x, Φ, Ψ) a second gauge shift function. Supersymmetry fixes f in terms of F and G
                                                 24(x − ρ)
                                         f=                  .                               (3.5)
                                                 F ′′ + G ′′
Furthermore F and G satisfy a complicated 6th order PDE. A known solution of it has
both functions cubic

              G(x) = g0 (x2 − 1)(x − g1 ) ,          F (ρ) = −G(ρ) + m0 (ρ − m1 )3 ,         (3.6)

     Having recalled the physics background, we begin by including the needed definitions
into sol
                                                                                          In[15]:=
  IncludeTo[sol[$chart], {
    <|Symbol → curved, Manifold → M,
     CNumbersOf → {0, 1, 2, 3, 4},
     ScalarsOfChart → {y[], x[], ρ[], Φ[], Ψ[]},
     ChartColor → Red|>
    }]
  IncludeTo[sol[$form], {
    <|Symbol → ϖ [], Manifold → M, Deg → 1, Symmetry → None|>,
    <|Symbol → P [], Manifold → M, Deg → 1, Symmetry → None|>
    }]
  IncludeTo[sol[$function], (<|Symbol → #|> & /@ {f[ρ[], x[]], G [x[]],
     F [ρ[]], λ[x[], Φ[], Ψ[]], χ[x[], Φ[], Ψ[]]})]




                                                 –9–
                                                                                               In[15]:=
  IncludeTo[sol[$constant], (<|Symbol → #|> & /@ {g0, g1, m0, m1, f0})]
  IncludeTo[sol[$assumption], <|Symbol → asymp, Expression → {
       l5 > 0,
       F [ρ[]] > 0, G [x[]] > 0, f[ρ[], x[]] > 0,
       Derivative[4][F ][ρ[]] == 0, Derivative[4][G ][x[]] == 0,
       -1 < x[] < 1, x[] > ρ[]
      }|>]

                                                                                               Out[15]=
  Loaded:
  PDcurved, curved, y, x, ρ, Φ, Ψ, dicurved, dcurved, TorsionPDcurved, ChristoffelPDcurved,
  RiemannPDcurved, RicciPDcurved, etaUpcurved, etaDowncurved, curved0, curved1, curved2, curved3,
  curved4, icurved, KoszulPDcurved, CovDPDcurved
  Info[...]



                                                                                               Out[16]=
  Loaded:
  Tϖ , ϖ , TP , P
  Info[...]



                                                                                               Out[17]=
  Loaded:
  f, G , F , λ, χ
  Info[...]



                                                                                               Out[18]=
  Loaded:
  g0, g1, m0, m1, f0
  Info[...]



                                                                                               Out[19]=
  Loaded:
  $Assumptions
  Info[...]



Notice the [] brackets next to the coordinate symbols; this is xAct’s convention and signifies
that the coordinates are really scalar functions of the chart curved. sol[$assumption]
is a special key: whatever Expression we include under it, and we may IncludeTo it as
many times as we like, becomes part of the kernel’s $Assumptions. For example, with
the above, Sqrt[F []2 ] Simplify-es to F []. sol[$function] also deserves a closer look.
Its Symbol key carries more than a name. What is declared is the head together with its
arguments: f[ρ[], x[]]. The head becomes the xAct scalar function, defined through
DefScalarFunction; the argument list becomes an abbreviation, so that from now on
f[] evaluates to f[ρ[], x[]] and Derivative[1, 0][f][] evaluates to Derivative[1,
0][f][ρ[], x[]]8 . We supply the three functions with their expressions

  8
    That abbreviation is why the frame and the metric below can be typed with bare f[], F [] and G []
and still carry the right dependence




                                                   – 10 –
                                                                                         In[20]:=
  sol[$function, G , Expression] = g0 x[]2 − 1
                                                                               
                                                                     x[] − g1
                                                                                    3
  sol[$function, F , Expression] = −G [ρ[]] + m0 ρ[] − m1
                                                                      
                                                     24 x[] − ρ[]
  sol[$function, f, Expression] =
                                                   F ”[ρ[]] + G ”[x[]]
Stored like that these expressions are inert: they are data in the record, not definitions in
the kernel. Gen9 is what turns them into genuine Function rules, for example
                                                                                         In[21]:=
  Gen@sol[$function, f]

                                                                                         Out[21]=
                                           h             24 (−xxx1 + xxx2) i
                             f → Function {xxx1, xxx2},
                                                        F ′′ [xxx1] + G ′′ [xxx2]

From here the solution data is typed almost verbatim as in the formulas above: the frame
(3.3)
                                              (                                          In[22]:=

  sol[$frame, ee, Expression] =

                                               
       f[ρ[], x[]] Diff[y[]] + ϖ [] ,
            s
                x[] − ρ[]
       l5                     Diff[ρ[]],
                f[] F []
            s
                      F []                                                
       l5                           Diff[Φ[]] + x[] × Diff[Ψ[]] ,
                f[] x[] − ρ[]
                s
                    x[] − ρ[]
        − l5                     Diff[x[]],
                    f[] G []
            s
                      G []                                                
       l5                           Diff[Φ[]] + ρ[] × Diff[Ψ[]]
                f[] x[] − ρ[]
  )



and the metric (3.2)

  9
      Shortened from “Generate”, as it is typed very often in a standard workflow.




                                                        – 11 –
                                                                                              In[23]:=
  sol[$metric, gg, Expression] =
                                                             
       − f[]2 Diff[y[]] + ϖ [] ⊗ Diff[y[]] + ϖ [] +

                      x[] − ρ[]
       l52 f[]−1                  Diff[ρ[]] ⊗ Diff[ρ[]]
                        F []
              F []                                                                   
        +                 Diff[Φ[]] + x[] × Diff[Ψ[]] ⊗ Diff[Φ[]] + x[] × Diff[Ψ[]]
            x[] − ρ[]
              x[] − ρ[]
          +               Diff[x[]] ⊗ Diff[x[]]
                G []
                                                                                          !
               G []                                                                  
        +                 Diff[Φ[]] + ρ[] × Diff[Ψ[]] ⊗ Diff[Φ[]] + ρ[] × Diff[Ψ[]]
            x[] − ρ[]


Note that SolutionsX registers the symbol CircleTimes (⊗) as a graded product, within
xAct’s framework of products10 , to represent the symmetric product of forms. The remain-
ing input, ϖ and P of (3.4) followed by A of (3.2) and F = dA, is typed the same way and
we do not reproduce it here. Once the metric and all the forms are populated we register
three rules that will be convenient during the Compute phase
                                                                                              In[24]:=
  IncludeTo[sol[$rule], <|Symbol → func, Expression →
       FoldedRule[Gen@sol[$function, #] & /@ {f},
        Gen@sol[$function, #] & /@ {F },
        Gen@sol[$function, #] & /@ {G }]|>]
  IncludeTo[sol[$rule], <|Symbol → der3, Expression →
       ((Derivative[3][#][] → (Derivative[3][#][] /. Gen@sol[$rule, func])) & /@
         {F , G })|>]
  IncludeTo[sol[$rule], <|Symbol → $form, Expression → FoldedRule[
         Gen[sol[$form, #]] & /@ {F},
         Gen[sol[$form, #]] & /@ {A},
         Gen[sol[$form, #]] & /@ {ϖ , P }
         ]|>]

Notice that some of them are layered, making use of xAct’s FoldedRule11 . der3 collapses
the third derivatives of the two cubics, which are constants and therefore cheap in the
upcoming computations. Thus far these rules are inertly stored. Gen is overloaded on
$rule’s to call the actual replacement rules

                                                                                              In[25]:=
  Gen@sol[$rule, func]
  Gen@sol[$rule, der3]
  Gen@sol[$rule, $form]


 10
      See Wedge (∧) in xTerior and CenterDot (·) in FieldsX
 11
      FoldedRule belongs to xCore; see the xCoreDoc notebook shipped with xAct




                                                    – 12 –
                                                                                                 Out[25]=

                        h                                   24 (−xxx1 + xxx2) 
         FoldedRule          f → Function {xxx1, xxx2},                                ,
                                                             F ′′ [xxx1] + G ′′ [xxx2]
                             F → Function {xxx1}, m0 (−m1 + xxx1)3 − G[xxx1] ,
                                                                                    

                                                                                            i
                             G → Function {xxx1}, g0 (−g1 + xxx1) (−1 + xxx12 )
                                          


                                                                                                 Out[26]=
                               (3)
                               F [ρ] → −6 g0 + 6 m0, G (3) [x] → 6 g0

                                                                                                 Out[27]=
             h
  FoldedRule    F → d[A] ,
                        √ 
               n         3
                  A→−          − f0 d[y] + l53P + f[ρ,x] (d[y] + ϖ)
                        Cx
                                                                                                     o
                     + d[Ψ] λ(0,0,1) [x, Φ, Ψ] + d[Φ] λ(0,1,0) [x, Φ, Ψ] + d[x] λ(1,0,0) [x, Φ, Ψ]        ,
                                                     
               n    l5 d[Ψ] x ρ + d[Φ] (x + ρ) F (3) [ρ] G (3) [x]
                ϖ→−
                                            288
                   l5 F (3) [ρ] + G (3) [x] 
                 +                            G[x] (d[Φ] + d[Ψ] ρ)
                        48 (x − ρ)2
                                                              ′                             
                     + (d[Φ] + d[Ψ] x) F[ρ] + (x − ρ) F 2[ρ] − 14 (−m1 + ρ)2 F (3) [ρ]
                     + d[Ψ] χ(0,0,1) [x, Φ, Ψ] + d[Φ] χ(0,1,0) [x, Φ, Ψ] + d[x] χ(1,0,0) [x, Φ, Ψ],
                       (d[Φ] + d[Ψ] x) F ′ [ρ] + (d[Φ] + d[Ψ] ρ) G ′ [x] oi
                   P→−
                                             2 (x − ρ)

Notice that the gauge functions λ and χ have been kept arbitrary. In Section 3.5 that
freedom will be spent to match the present solution with the supersymmetric limit of
Curated/Sol__5dL__CCLP__Boyer-Lindquist.

3.3   Computing the tensor components of the solution
So far nothing has been computed: what the record holds is a chart, a handful of functions
and forms, and the expressions (3.2)–(3.6) written in them. Next we Compute the tensor
components out of these definitions.

The chain Every entry that Compute can produce is reached through a Chain: an ordered
list saying where the components come from. A chain entry has one of two shapes. An
array entry: HoldForm[expr ] → {slots }, holds an expression that ReleaseHold-s into an
explicit array, which is then stored into the named index placement. A slot entry: {from }
→ {to}, will compute the left-hand side by raising or lowering the right-hand side with the
metrics of the bundles involved. For example, the set of computation instructions for the
metric, which we call Routine, is
                                                                                                 In[28]:=
  sol[$metric, gg, $auto, gg, Routine, Chain] = {




                                               – 13 –
                                                                                             In[28]:=
       HoldForm[MakeArray[$self[$metric, gg, Expression] /. Gen@$self[$rule, $
           form]]] → {{-1, -1}},
       HoldForm[Inverse@ToArray@gg[-m , -n ]] → {{1, 1}}
       }

$self is SolutionsX’s way to emulate Python’s self. It refers to the parent association,
whatever that association happens to be called. For longer chains there is the short-
hand syntax RulesToChain which expands an arrow sequence into the successive pairs; e.g.
RulesToChain[a → b → c] gives {a → b, b → c}. Using it, the Christoffel symbols of the
Levi-Civita connection have the Chain
                                                                                             In[29]:=
  sol[$metric, gg, $auto, Christoffelcd, Routine, Chain] = RulesToChain @@ {
           HoldForm[ToArray@ChristoffelToGradMetric@Christoffelcd[-m , -n , -o ]] →
               Permutations[{-1, -1, -1}] → Permutations[{1, -1, -1}]
           }

a.k.a. build the all-lower placement from ∂g, then raise one index. The vielbein, which
lives in two bundles at once, is a three-step chain
                                                                                             In[30]:=
  sol[$frame, ee, $auto, ee, Routine, Chain] = RulesToChain @@ {
           HoldForm[Transpose[MakeArray[#] & /@ ($self[$frame, ee, Expression] /.
           Gen@$self[$rule, $form])]] →
               {{-1, 1}} → {{1, 1}, {-1, -1}} → {{1, -1}}
           }

The spin connection is a single array entry, written straight from its definition in terms of
the Christoffel symbols and the vielbein
                                                                                             In[31]:=
  sol[$spinConnection, ωω , $auto, ωω , Routine, Chain] = {
       HoldForm[ToArray@(Christoffelcd[o , -n , -m ] ee[n , -c] ee[-o , -b]
               - ee[p , -c] PD[-m ][ee[-p , -b]])] → {{-1, -1, -1}}
       }

It is worth being plain about what a slot specification buys, because it is easy to write more
of them than one needs. A list of ±1 says where each index sits: {-1, -1, -1} is “all three
downstairs”, {1, -1, -1} is “the first one upstairs”. Getting from the first to the second
costs a contraction with the metric. That is real work, and it is why it is a rung of its own.
Getting from {1, -1, -1} to {-1, 1, -1} might cost less depending on the symmetries
of the tensor. Compute fills all such rearrangements together, so the three placements that
Permutations[{1, -1, -1}] lists above are one rung of the ladder and not three. The rule
of thumb: a different number of raised indices needs its own chain entry, a different order
of the same indices does not. Within a placement the same economy applies. Compute
evaluates only the components the tensor’s symmetries leave independent, and fills the rest
from those, signs included12 .
  12
   The all-lower Christoffel symbols below are symmetric in their last two indices, so 75 of their 125
components are evaluated and the other 50 are read off.




                                                – 14 –
What is done to each component Every value Compute produces is passed through
the functions of the Apply option, whose default is the global $Apply: a list keyed by Map
and ParallelMap, applied in that order: the first serially, the second distributed over the
subkernels. For this record we set
                                                                                              In[32]:=
  $Apply = {
       Map → (# /. Gen@sol[$rule, der3] &),
       ParallelMap → (Simplify[Together[#]] &)
       }

so that the third derivatives of the cubics collapse to constants before anything expensive
happens, and the simplification runs in parallel. The split is not a matter of taste. A
function handed to ParallelMap must be built from System‘ symbols alone13 ; Gen and
sol are not, which is why that substitution sits in the Map slot. Simplify[Together[#]]
& qualifies, and the assumptions of sol[$assumption] are shipped with it, which is what
lets Simplify combine the radicals of the frame.

Computing           With the chains stored and $Apply set, we are finally ready to Compute
                                                                                              In[33]:=
  Compute@sol[$metric, gg, $auto, #] & /@ {gg, Detgg, Christoffelcd, Riccicd,
           RicciScalarcd};


  » Applied #1 /.          Gen[sol[$rule, der3]] & and Simplify[Together[#1]] & to
           ggmn = MakeArray[$self[$metric, gg, Expression] /.                 Gen[$self[$rule,
           $form]]] in 0min 11s
                            −1 in 0min 2s
  » Applied ... to ggmn = ggmn
                          ∼
                          ∼               
  » Applied ... to gg = Det ggmn in 0min 0s
  » Applied ... to Γ[∇]mno = 12 −∂m ggno + ∂n ggom + ∂o ggnm
                                                                       
                                                                           in 0min 14s
  » Applied ... to Γ[∇]m no , Γ[∇]m n o , Γ[∇]mn o obtained from Γ[∇]mno using metrics
     TM → gg in 1min 44s
  » Applied ... to
                                   p                   p
           R[∇]mn = −Γ[∇]o mp Γ[∇] on + Γ[∇]o mn Γ[∇] po − ∂m Γ[∇]o on + ∂o Γ[∇]o mn in 3min 33s
  » Applied ... to R[∇]m n , R[∇]m n obtained from R[∇]mn using metrics TM → gg
           in 2min 12s
  » Applied ... to R[∇] = Tr R[∇]m n in 0min 2s
                                              


SolutionsX echoes each step in the chain: how it was computed and how long it took.
The frame goes the same way. Its flat metric is entered as a literal and inverted; the
vielbein is built from the frame expression (3.3) and then walked through its three remaining
placements, with the flat and curved indices being raised and lowered with ηη and gg
respectively
                                                                                              In[34]:=
  Compute@sol[$frame, ee, $auto, #] & /@ {ηη , ee};


 13
      This is a present Mathematica limitation to which we have not yet found a workaround.




                                                   – 15 –
  » Applied ... to ηηab = DiagonalMatrix[{-1, 1, 1, 1, 1}] in 0min 0s
                             −1
  » Applied ... to ηη ab = ηηab in 0min 0s
  » Applied ... to eem b = ((MakeArray[#1] &) /@ ($self[$frame, ee,
      Expression] /.       Gen[$self[$rule, $form]]))T in 0min 0s
  » Applied ... to eemb , eemb obtained from eem b using metrics
      TM → gg, FM → ηη in 0min 1s
  » Applied ... to eem b obtained from eemb , eemb using metrics
      TM → gg, FM → ηη in 0min 0s

The spin connection is one entry and one echo:
                                                                                       In[35]:=
  Compute@sol[$spinConnection, ωω , $auto, #] & /@ {ωω };

                                                         p
  » Applied ... to ωωmbc = Γ[∇]o nm een c eeob − ee c ∂m eepb in 0min 24s

Every index in an echo wears the colour of the basis it sits in:    for the chart curved,
   for flat, for spin. Thus, one can read at a glance that ωω has one curved leg and
two frame legs. The remaining sectors are computed analogously: Compute@sol[$tensor,
#, $auto, #] & /@ {TA, TF} builds the tensor partners of the gauge potential and its
field strength from sol[$form, A, Expression] and sol[$form, F, Expression], and
Compute@sol[$spinStructure, gg, $auto, #] & /@ {...} does the same for the rank-
one, -two and -three γ-matrices in both the flat and the curved bases.

3.4   Verifying the solution
Having computed all the desired tensor values it is now time to check if the equations of
motion and the Killing spinor equation hold. Since the solution is built on top of its parent
theory (which stored these equations) we simply call them, act with ToArray to convert
them to arrays and then Simplify
                                                                                       In[36]:=
  E gg[-m , -n ]
  (ToArray[%] // Flatten // DeleteCases[0] // DeleteDuplicates) /. Gen@sol[$rule,
      func];
  AbsoluteTiming[ParallelMap[Simplify, %]]

                                                                                       Out[36]=
                    4 ggmn                Cx2      o         Cx2                  op
                             + R[∇]mn −         TFm TFno +         ggmn TFop TF
                     l52                   2                 12

                                                                                       Out[38]=
  {53.878, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}}


The first line only recalls the stored equation. ToArray takes it to bases, traces the dum-
mies and inserts the component values computed in the previous subsection; Flatten,
DeleteCases and DeleteDuplicates reduce the resulting 5 × 5 array to its 16 distinct
nonzero components. The func rule expands f , F and G. That produces a set of long
expressions, omitted here, each of which simplifies to 0.




                                                – 16 –
      The Maxwell equation goes the same way, but it needs one more line:
                                                                                                                                  In[39]:=
  E TA[-m ]
  % /. epsilonToetaDown[gg, curved] // CovDToChristoffel
  (ToArray[%] // Flatten // DeleteCases[0] // DeleteDuplicates) /. Gen@sol[$rule,
         func];
  AbsoluteTiming[ParallelMap[Simplify, %] // PowerExpand // Simplify]

                                                                                                                                  Out[39]=
                                                Cx ϵggmnopq TFno TFpq                        n
                                           −                 √                    + ∇n TFm
                                                            4 3

                                                                         q                                                        Out[40]=
                                                                              ∼
                                                                              ∼
                                                                  Cx         −gg ηmnopq TFno TFpq
                  Γ[∇]n no TFm o − Γ[∇]o nm TFo n −                              ∼
                                                                                   √              + ∂n TFm n
                                                                                 4 3

                                                                                                                                  Out[42]=
  {15.1216, {0, 0, 0, 0, 0}}


The extra line trades the two objects whose components we have not actually computed.
                                   q rewrites the Levi-Civita tensor ϵgg as the etaDown
xCoba’s epsilonToetaDown[gg, curved]
                                                            ∼
                                                            ∼
tensor of the chart curved14 times −gg. The tildes are xCoba’s way of signifying that
the object in question is a tensor density15 . xTensor’s CovDToChristoffel rewrites ∇
as the chart’s partial derivative plus Christoffel tensors. PowerExpand, which behaves as
√       √ √
  ab = a b, is safe to use in this case because at the very beginning we arranged positive
factors under the square roots with sol[$assumption].
     The Killing spinor equation is checked the same way, once the spinor is in the record.
It is not derived but posed, and it enters through Compute like any other component value:
             h                                                                                                                    In[43]:=
  Compute sol[$spinor, ϵϵ, $auto, ϵϵ],
                    n                h     3i
                                                                                                 i                   o
          Chain →       HoldForm e 2 l5 (f0 y[]−λ[]) f[]1/2 {1, 1, −1, −1} → {{−1}} ,
                                                   i
          Apply → {Map → Identity}



                                                       n 3i(f0 y−λ[x,Φ,Ψ]) p                         3i(f0 y−λ[x,Φ,Ψ])   p
        » Applied Identity to ϵϵA =                     e         2 l5             f[ρ,x], e                2 l5             f[ρ,x],

                       3i(f0 y−λ[x,Φ,Ψ])   p                    3i(f0 y−λ[x,Φ,Ψ])   p                o
                  −e          2 l5              f[ρ,x], −e             2 l5           f[ρ,x]             in 0min 0s


Nothing is really computed here: the array is simply hooked to the TensorValues of the
spinor ϵϵ, so that it can be recalled with ToArray. After this preparation we are ready to
check the Killing spinor equation

 14
      the antisymmetric symbol of the basis covectors, a density of weight −1 with components 0 and ±1
 15
      See the xCobaDoc notebook shipped with xAct




                                                                – 17 –
                                                                                          In[44]:=
  δψψ [-m , -A]
  AbsoluteTiming[(ToArray[%] // Flatten // PowerExpand // Simplify //
       PowerExpand) /. Gen@sol[$rule, func] // Simplify]

                                                                                          Out[44]=
                     √
                    i 3 Cx TAm ϵϵA γ[gg]mAB ϵϵB i Cx γ[gg]n AB TFmn ϵϵB
                  −               −            +           √
                         2 l5          2 l5              2 3
                        i Cx γ[gg]monA B TFon ϵϵB 1
                    −              √             + γ[ηη]baAB ϵϵB ωωmba + ∂m ϵϵA
                                  8 3             4

                                                                                          Out[45]=
  {74.2331, {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}}


With that, the solution is verified against the equations of motion and the Killing spinor
equation of its parent theory.

3.5    The solution can now play with its friends
A verified record is worth keeping. SaveData writes it, together with the notebook it was
built in, into $DataDirectory/$Alias/name /. The $DataDirectory and the $Alias are
configured through the Welcome[] wizard, or later with SetDataDirectory and SetAlias,
and are recorded in the user configuration file, so they persist across sessions. name is
determined from the association itself
                                                                                          In[46]:=
  sol[$manifold, M, Name] = "CCLP-susy";
  sol[$chart, curved, Name] = "Orthotoric";
  SaveData@sol

SaveData echoes where it put the entry: Saved alias /name under directory. What lands
on disk is a folder named Sol__5dL__CCLP-susy__Orthotoric, containing two files that
carry that same name: name .nb, the notebook from which we last called SaveData, and
name .m, a compressed record of the entire association. From now on the solution can be
recalled with GetData and Load, which rebuilds the whole xAct environment together with
every component computed in Section 3.3. SolutionsX makes one simplifying assumption:
one record is to be loaded at a time16 . Thus, there is a single xAct environment in a kernel,
and it belongs to whoever called Load. Any number of further records may be fetched. A
fetched record is an ordinary association: its stored expressions can be read out and used,
but its own symbols are inert. Below we give three physically relevant examples of how a
stored solution can “interact with its neighbours”.

The supersymmetric black hole is a limit of the non-supersymmetric black hole
The corpus already contains the general, non-supersymmetric CCLP black hole in Boyer–
Lindquist coordinates, Curated/Sol__5dL__CCLP__Boyer-Lindquist, built on top of the
same parent theory. In a fresh kernel we fetch our record, load it, and fetch that one
  16
    We have not yet stumbled on a convincing argument for extending this to multiple entries loaded
simultaneously.




                                              – 18 –
                                                                                                     In[47]:=
  sol = GetData["Curated/Sol__5dL__CCLP-susy__Orthotoric"];
  Load@sol
  cclp = GetData["Curated/Sol__5dL__CCLP__Boyer-Lindquist"];

The supersymmetric solution should be the limit of the general one, and the statement
has two parts: a change of coordinates, and a restriction of parameters. The change of
coordinates is entered as an ordinary list of rules
         (                                                                                           In[48]:=

  ct =


      t[] → y[],
               r
                   1 − x[]
      θ [] →                    ,
                       2
               s
                   1                                1                            1
      r[] →            a2 − b2 mt ρ[] +                (a + b) mt + a + b + a b g + (a + b)2 mt,
                   2                                 g                             2
                                      1 − a 2 g2          
      ϕ1[] → g y[] − 4               2    2
                                            
                                               2
                                                 Φ[] − Ψ[] ,
                                    a − b g mt
                                        1 − b 2 g2                       
      ϕ2[] → g y[] − 4                                      Φ[] + Ψ[]
                                    a2 − b2    g2 mt
  )



The parameter map is then obtained by matching polynomials. The change of variables
above and the identifications below are those of [11], and the two cells that follow are the
elementary algebra that pins the four constants of (3.6) onto parameters of Curated/Sol_
_5dL__CCLP__Boyer-Lindquist:

                                                                                                     In[49]:=
  G [] /.      Gen@sol[$rule, func];
               4                                                                     
                                1 − x[]2          1 − a2 g2 1 + x[] + 1 − b2 g2 1 − x[] ;
                                                                             
  −                
       a2 − b2 g2 mt
  CoefficientArrays[%% - %, x[]] // Normal // Flatten // Simplify;
  g01 = Solve[% == 0, {g0, g1}] // First

                                                                                                     Out[52]=
                                         n              2 − a2 g2 − b2 g2 o
                                                         4
                                          g0 → − , g1 →
                                                mt        a2 g2 − b2 g2

and, in the same way:
                                                                                                     In[53]:=
  F [] /.      Gen@sol[$rule, func];
                                                             !3
                       1 + mt             2 + ag + bg
  − G [ρ[]] − 4                                        + ρ[]    /.          Gen@sol[$rule, func];
                           mt                a−b g

  CoefficientArrays[%% - %, ρ[]] // Normal // Flatten // Simplify;
  m01 = Solve[% == 0, {m0, m1}] // First




                                                               – 19 –
                                                                                                 Out[56]=
                            n            4 (1 + mt)          −2 − a g − b g o
                                m0 → −                , m1 →                  .
                                            mt                 ag − bg

Everything is now in place to compare the two metrics. The fetched record’s expression is
pulled through the coordinate map and its own stored rules17 ; ours is expanded with its
form rule; the difference is turned into an array:
                                                                                                 In[57]:=
  cclp[$metric, gg, Expression] /.               ct /.   Gen@cclp[$rule, func]
           /.    Gen@cclp[$rule, const];
  sol[$metric, gg, Expression] /.             Gen@sol[$rule, $form];
  (MakeArray[%% - %] /.          Gen@sol[$rule, func]
          // DeleteDuplicates // DeleteCases[0]);
                            h             2Ψi
      % /.      χ → Function {x, Φ, Ψ}, −
                                               g mt
                            m
           /.    q→                  /.    g01 /.      m01 /.
                      1 + ag + bg
                                      mg
          mt →                                                      −1
                  (a + b) (1 + a g) (1 + b g) (1 + a g + b g)
                         !
                       1
           /.    l5 →       // Simplify
                       g

                                                                                                 Out[60]=
  {{0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}}


which simplifies to 0 upon taking the parameter q to its supersymmetric value and relating
the extremality parameter mt to the mass parameter m. To obtain perfect agreement the
gauge freedom χ is used up. The gauge field goes the same way and comparing fixes the
second gauge function, λ, together with the gauge shift constant f0 .

The supersymmetric black hole is a U(1) fiber over a Kähler base The second
kind of interplay is structural rather than a limit. Every supersymmetric solution of five-
dimensional minimal gauged supergravity whose Killing-spinor bilinear is timelike is a
fibration over a four-dimensional Kähler base [12],

                                  ds25 = − f 2 (dy + ϖ)2 + f −1 ds2B ,                               (3.7)

and the function f that (3.5) produced out of thin air is nothing but the inverse of the
curvature of that base
                                                          24
                                              f= −              ,                                    (3.8)
                                                         ℓ25 RB

with RB its Ricci scalar. The base is a geometry in its own right and deserves its own entry.
Curated/Thr__4dE__Kahler-base is the theory: a four-dimensional Euclidean manifold
carrying, besides its metric and frame, an SU(2) bundle whose sections are a triplet of
 17
      Note that the potent combination of Diff and ⊗ does most of the heavy lifting automatically.




                                                    – 20 –
two-forms X i , together with a one-form P and the two-form R = dP. Its $set entries are
the conditions that make such a manifold Kähler, each stored as a named expression that
any solution built on the theory can call:
                                                     1
      X i X j = − δ ij 1 + η ijl Xl ,               − X i ∧ X i = ⋆B , ⋆B X i = − X i ,
                                                    2                                              (3.9)
           1
      dX = 0 ,                          (∇m + iPm ) X 2 + iX 3 = 0 ,    Rmn = 21 Rmnpq X 1 pq ,

together with the equation that determines the fibration one-form,

                                                 ℓ3 RB    1
                                                                        
                                      dϖ + ⋆ dϖ = 5    R − RB X 1 .                                (3.10)
                                                   24     4

The first row of (3.9) says that the X i are an anti-self-dual quaternionic triple, normalised
against the volume form. The second row is where the gauging shows: only X 1 is closed,
so it alone is a Kähler form, P is the connection on the canonical bundle whose curvature
R is the Ricci form, and X 2 + iX 3 is the holomorphic (2, 0)-form, covariantly constant with
respect to P.
     Curated/Sol__4dE__Kahler-base__Orthotoric is an explicit geometry that satisfies
the above conditions
                    x−ρ 2    F                 x−ρ 2    G
                                                                                           
  ds2B = ℓ25           dρ +     (dΦ + x dΨ)2 +    dx +     (dΦ + ρ dΨ)2 ,                          (3.11)
                     F      x−ρ                 G      x−ρ

with the same P and ϖ of (3.4). Its notebook computes X i from the frame and checks
(3.9) and (3.10). Along the way it stores the base Ricci scalar,

                                                        F ′′ + G ′′
                                              RB = −                ,                              (3.12)
                                                        ℓ25 (x − ρ)

which is (3.5) and (3.8) in one line.
    To see this explicitly we call both solutions and verify that our algebra checks out:
                                                                                                  In[61]:=
  sol = GetData["Curated/Sol__5dL__CCLP-susy__Orthotoric"];
  Load@sol
  base = GetData["Curated/Sol__4dE__Kahler-base__Orthotoric"];


                                                                                                  In[62]:=
  sol[$metric, gg, Expression];
  − f[]2 Diff[y[]] + ϖ [] ⊗ Diff[y[]] + ϖ [] + f[]−1 base[$metric, gg, Expression];
                                                       

  %% - % // Simplify

                                                                                                  Out[64]=
  0


The above shows that we have correctly built up the 5d metric.




                                                     – 21 –
                                                                                     In[65]:=
  Last@First@base[$metric, gg, $auto, RicciScalarcd, Value]
                  24
  f[] +                         /.   Gen@sol[$function, f] /.   %
          l52 RicciScalarcd[]

                                                                                     Out[66]=
  0


The first line above is a plain lookup into the fetched association: $auto entries are stored
under their Value. The second line substitutes it into (3.8) together with the definition of
f.
    Nothing here was re-computed. Both records were built once, saved once, and the two
checks are two substitutions. That is the whole argument of this paper in miniature: a
solution stored as code can be used, not merely cited.

A more involved interplay of entries: holographic renormalization in 4d The
Curated corpus also carries a larger set of “interacting entries”, in which a holographic
computation is spread across five of them:

  • Curated/Thr__4dL__Minimal-gauged — the bulk theory, four-dimensional minimal
    gauged supergravity.
  • Curated/Sol__4dL__Black-hole__Global — the dyonic black hole in global coordi-
    nates: it solves the equations of motion, then computes its thermodynamic potentials,
    its electric and magnetic charges, its entropy, and its divergent bulk on-shell action.
  • Curated/Sol__4dL__Black-hole__FG — the same solution again, fetched from the
    previous entry and rewritten in Fefferman–Graham coordinates.
  • Curated/Thr__3dL__Boundary-minimal-gauged — the three-dimensional boundary
    theory, an entry of its own because the boundary is a different manifold with a
    different metric.
  • Curated/Sol__3dL__Induced-black-hole__FG — the induced boundary solution,
    built from the Fefferman–Graham record. Its last section is the holographic renor-
    malisation proper: it adds the Gibbons–Hawking term and the counterterms to the
    divergent bulk action to obtain the renormalised one, and varies the same combina-
    tion to obtain the boundary stress tensor and hence the energy.

Read these example notebooks in the above order to see the details of the calculation.
The final section of Curated/Sol__4dL__Black-hole__Global fetches the boundary record,
imports the renormalised action and the energy from it, and verifies the quantum statistical
relation.

Browsing the available entries ShowData[] is a simple interactive browser, allowing
a bird’s-eye view of the available entries:
                                                                                     In[67]:=
  ShowData[]




                                            – 22 –
                                                                                                         Out[67]=

         ✎ Vasko | Curated | Vasko-bot              search all aliases

         Curated/Sol__3dL__Induced-black-hole__FG   OpenData   CopyName   CopyData   DeleteData   CurateData


         Curated/Sol__4dE__Kahler-base__Orthotoric OpenData    CopyName   CopyData   DeleteData   CurateData


         Curated/Sol__4dL__Black-hole__FG           OpenData   CopyName   CopyData   DeleteData   CurateData


         Curated/Sol__4dL__Black-hole__Global       OpenData   CopyName   CopyData   DeleteData   CurateData


         Curated/Sol__5dL__CCLP__Boyer-Lindquist    OpenData   CopyName   CopyData   DeleteData   CurateData


         Curated/Sol__5dL__CCLP-susy__Orthotoric    OpenData   CopyName   CopyData   DeleteData   CurateData


         Curated/Thr__3dL__Boundary-minimal-gauged OpenData    CopyName   CopyData   DeleteData   CurateData


         Curated/Thr__4dE__Kahler-base              OpenData   CopyName   CopyData   DeleteData   CurateData


         Curated/Thr__4dL__Minimal-gauged           OpenData   CopyName   CopyData   DeleteData   CurateData


         Curated/Thr__5dL__Minimal-gauged           OpenData   CopyName   CopyData   DeleteData   CurateData


         Curated/Thr__5dL__STU-gauged               OpenData   CopyName   CopyData   DeleteData   CurateData




The three names at the top of the panel are aliases 18 . An alias is a folder of entries with
somebody’s name on it. Each user chooses their alias once, when they first run Welcome[],
and from then on everything they save lands under it. Reading is unrestricted: any alias
present in the data directory can be fetched. Writing, by design, is restricted: one writes
only under one’s own alias. In the example panel above Vasko is the current user, signified
by the pencil; Curated is a special alias where all the curated entries (think of them as
“official”) are stored; and Vasko-bot is a second alias, belonging to the same author, where
Vasko’s agents store their entries. Depending on their permissions, a user can OpenData
(open the corresponding notebook), CopyName (copy the name of the entry), CopyData
(copy someone else’s entry under their own alias), DeleteData (delete a data entry) and
CurateData (copy one of their own entries into the curated corpus).


4        Benchmarking: SolutionsX vs xCoba

Any new package owes the reader a comparison with what already exists. For Compute
the nearest thing to compare against is xCoba’s MetricCompute, which builds the tensor
components of a chart out of a component metric. This section reports a head-to-head
between the two on two five-dimensional records, one of them the solution of Section 319 .
    18
     Next to the alias tabs sits the search field. The query is split into words, and an entry stays listed
when every word occurs, case-insensitively, in its alias/name. The double-underscore names make this
plain substring matching effectively structural: 5dL CCLP finds exactly the CCLP records.
  19
     The benchmark harness is not part of the package; it is available upon request.




                                                      – 23 –
4.1   Flexibility
MetricCompute produces a fixed set of objects: the metric in both index placements and
its determinant, the Christoffel symbols all-lower and once-raised, the Riemann tensor all-
lower and once-raised, the Ricci tensor and the Ricci scalar. Which of them are actually
built is decided by a dependency table inside xCoba, and the first and second derivatives
of the metric are built on the way whether or not anybody wanted them. Simplification
is a single function, handed over through the CVSimplify option and applied to every
component, with a boolean deciding whether it runs in parallel.
     Compute has no such menu. It computes whatever the record’s Chain names, in
whichever bundle the indices live, along whichever route the author wrote down, and it
passes every component through the two sieves of $Apply, one serial and one parallel. Sec-
tion 3.3 used all of that: the vielbein carries a chart index and a frame index at once; the
spin connection is written straight from its definition; the γ-matrices are computed in two
bases; and the serial sieve carries a substitution that the distributed one cannot express.
     This says nothing about what xAct can or cannot do, in principle. xCoba exposes the
primitives, so every array Compute produces can be re-created by hand-written code using
vanilla xAct. Our contribution is devising a unified syntax to achieve that with ease.

4.2   Need for speed and quality
Both engines make clever use of tensor symmetries and allow the user to run calculations in
parallel. In order to compare them, we focus on where they overlap: namely, on computing
the metric-associated tensors. All timings in this paper come from the same laptop, an
Apple M1 Pro with 8 cores and 32 GB of RAM, with nothing else running on it; the runs
of this section use Wolfram 15.0.1 with eight parallel subkernels.
     To ensure a fair benchmark both engines are given the same input, allowed the same
means, and asked for the same output. The input is the array of the metric components
with both indices down: ggmn . The output is nine arrays:
                      ∼
                      ∼                                           p
        ggmn , ggmn , gg, Γ[∇]mno , Γ[∇]m no , R[∇]mnop , R[∇]mno , R[∇]mn , R[∇] .

Both simplify with Simplify[Together[#]] &, applied once per independent component,
in parallel, with no serial pre-pass on either side. Both declare the same constants and
functions to xAct beforehand, which matters because a declaration is what lets Simplify
treat a symbol as a quantity an assumption can be about. Importantly, both engines agree
on every tensor component, up to Simplify. Agreement in value is not by itself enough, be-
cause an engine can be fast by simplifying less. The control is LeafCount, which counts the
atoms of an expression, so the same quantity simplified further has fewer of them. Across
all runs the summed leaf counts agree to within 0.015%, practically the same. One thing
the two engines do not share is the environment their simplifier runs in. SolutionsX ships
the record’s assumptions into the subkernels, together with the definitions of the declared
symbols. xCoba’s parallel simplification is hard-wired to ship neither, and its interface of-
fers no way to ask for it, so the assumption-bearing runs of MetricCompute were produced




                                           – 24 –
by supplying both from outside the package. In a way we have given MetricCompute a
custom-designed “crutch” to allow it to work with $Assumptions.
     The comparison is presented in Table 1, on Sol__5dL__CCLP__Boyer-Lindquist and
Sol__5dL__CCLP-susy__Orthotoric. Besides the engine, the table varies two things. One
is the assumptions. SolutionsX always ships them to the simplifier and xCoba never does,
so neither setting is neutral ground, and both are measured for both engines. The other
is the route. In the middle block Compute is driven the way xCoba drives itself, with the
derivatives of the metric built as explicit arrays and every tensor assembled out of them,
the whole recipe written as an ordinary Chain. That block separates the cost of the route
from the cost of the engine.

                     Sol__5dL__CCLP__Boyer-Lindquist         Sol__5dL__CCLP-susy__Orthotoric

                     no assumptions         assumptions      no assumptions           assumptions
 Compute, the record’s own chains
   wall clock (s)               65.81               92.87              982.69              2398.16
   leaf count                  727 000             727 000            2 662 078            2 662 078

 Compute, mimicking xCoba
   wall clock (s)               87.32              114.51             1013.65              2386.76
   leaf count                  727 012             727 012            2 662 080            2 662 080

 MetricCompute
   wall clock (s)               41.28              85.78†              635.87             2905.69†
   leaf count                  726 891             727 028            2 662 150            2 662 138

Table 1. Nine tensor arrays, computed from the same metric with the same simplification function,
on Sol__5dL__CCLP__Boyer-Lindquist and Sol__5dL__CCLP-susy__Orthotoric. Wall clock in
seconds, and under it the summed LeafCount of all nine arrays. Every run reproduces the stored
record exactly. In each column the faster of Compute on the record’s own chains and MetricCompute
is set in green, the slower in red. The mimicking block is reported as an aside and does not
participate in the race. The † signifies that MetricCompute has no way of sending assumptions to
its subkernels, so those two runs were given them from outside the package.

Without assumptions Compute loses to MetricCompute by a factor of 1.59 on Sol__5dL_
_CCLP__Boyer-Lindquist and by 1.55 on Sol__5dL__CCLP-susy__Orthotoric. With as-
sumptions the picture turns: Compute is practically level on the first record and ahead by
1.21 on the second. What the engines do differently, underneath, is choose which com-
ponents the simplifier sees. Compute hands over only the components that the record’s
symmetries leave independent. MetricCompute hands over nearly twice as many20 , but the
extra ones are the easy ones, so its average component is cheaper. Each engine thus holds
one advantage: Compute simplifies fewer components, MetricCompute pays less per com-
ponent. Without assumptions the per-component advantage is the larger of the two, and
MetricCompute wins. Shipping the assumptions makes every component dearer on both
  20
    977 against Compute’s 502, over the nine arrays. The excess is components that its own symmetries
already fix, plus the derivatives of the metric that its route builds on the way.




                                               – 25 –
sides by a comparable amount, which shrinks the per-component advantage; the shorter
list then pulls Compute level on the first record and ahead on the second. The middle
block makes two points. xCoba’s particular recipe is one concrete Chain one can choose for
Compute. Driving that Chain, instead of the “native” one, moves the clocks only modestly.
Thus, the route is not what separates the engines; the simplification is.
     We want to disclose that for the particular experiments in Table 1 carrying the as-
sumptions is “dead weight”: the final LeafCount is practically the same with or without
assumptions. That is because in the present examples the metrics see no radicals. Using
assumptions really pays off only when radicals are present. In the Sol__5dL__CCLP-susy_
_Orthotoric example that is: the frame, the spin connection, and the γ-matrices. Said
differently: if there were a MetricCompute analogue for those tensors it would not simplify
nearly as well as Compute. The tests above are a proxy for this behaviour, based on what
xCoba currently provides. Note that the desire to properly distribute assumptions across
kernels is not cosmetic. If we specified no assumptions whatsoever we would finish com-
puting the tensor components faster, but then, when we pass those answers to the Killing
spinor equation of Section 3.4, Mathematica would struggle to make a dent in Simplify-ing
it for a very long time, rendering the results not practically useful.
     In summary: on the nine metric-related tensors without assumptions MetricCompute
is faster. In the regime where SolutionsX actually runs — with assumptions on, Compute
comes out ahead. The real benefit of that is visible beyond the metric sector. Both engines
leave room for improvements. To spell out a few possible directions:

    • MetricCompute could handle assumptions better:     the setting that keeps
      $Assumptions and the declared symbols out of its subkernels is currently not
      configurable.

    • Both engines could make explicit use of the isometry group of the ansatz; neither
      consults it today.

    • Compute could let the user decline the assumptions where they are dead weight; at
      present they are always shipped.

    • MetricCompute could simplify fewer components: part of its run goes to components
      its own symmetry declarations already fix, and to intermediates the user never asked
      to see.

    • Both engines parallelise one simplifier call per component, so a run ends waiting on
      its few largest components; splitting this across subkernels is an open problem.

5    SolutionsX and agents

A record that replays on a fresh kernel, a corpus of finished examples, and a documentation
whose every example is executed were all designed with a human user in mind. That turns
out to be what an AI agent needs even more urgently than a human does: a template that
shows what finished work looks like, and a kernel that says whether a claim is true before




                                          – 26 –
the claim is made. This section reports what happened when we asked an agent to use
SolutionsX by itself. We wrote a small toolkit that clears the obstacles standing between
an agent and the package, described in Section 5.1, and then gave an agent three tasks to
work through with it, reported in Section 5.2. We close with what we expect agents to be
able to do in the future. Everything below assumes route B of the installation instructions
of Section 2: the repository, not the paclet alone. The repository carries the notebooks
that the agents “learned from”, together with the notebooks they produced. The directory
agent/ is the toolkit of this section, self-documented in its own README and maintained
with the package.
     A fair question before any toolkit discussion: why not paste the problem into a chat
with a state-of-the-art model and ask it to check the algebra carefully, step by step? Because
what comes back is a transcript: plausible algebra that has to be re-derived to be trusted,
which is the artifact this paper set out to replace. Scale compounds the problem: verifying
the solutions of Section 4 means handling expressions whose combined size runs to millions
of leaves, arithmetic that no model performs reliably. In contrast, the kernel performs
exact verifiable algebraic manipulations. The workflow below therefore splits the work: the
model chooses what to try, the kernel decides what is true, and what the agent hands back
is a replayable entry rather than prose. We provide no controlled chat-versus-SolutionsX
measurement. Instead, we report that without the toolkit an agent tasked with what
became runs 1 and 2 ran some twelve hours and did not reach the goal. With the toolkit
the same scope was completed, correctly, in under three hours.
     The toolkit assumes a shell (macOS or Linux, bash) and an agent that can run shell
commands and read files. An agent confined to a notebook evaluator is not supported, for
a reason worth spelling out. When an xAct session goes wrong (a symbol defined twice,
packages loaded in the wrong order) the accumulated definitions cannot be reliably undone
from within the session; the one dependable recovery is to quit the kernel and start over.
From the shell that is a two-second command. An agent that lives inside a single kernel
has no way to issue it.

5.1     The agent toolkit
The toolkit’s mission fits in one sentence: read the existing corpus for methods and for
how your user writes, read a paper, and author entries your user could have written. Three
obstacles stand between an agent and that mission. First, a full xAct stack load costs the
better part of a minute, so the kernel must survive between calls. Second, the corpus is
notebooks and the deliverable is a notebook, while an agent reads and writes plain text.
Third, a human squints at a suspicious output and re-checks; an agent records it as truth.
So failures have to be made loud, and claims have to come with the evidence to audit them.
Each item below addresses one of the three.

  • sxk21 drives one long-lived kernel from the shell, and it simulates “using notebook
    cells”: each submission is one cell, evaluated in that kernel, with the output returned
    as text. sxk try runs a submission under a time budget; on expiry the submission is
 21
      The name abbreviates SolutionsX kernel.




                                                – 27 –
   cut off and the kernel, with all its state, survives. sxk again is the recovery verb: it
   restarts the kernel and re-runs a startup file the agent maintains (load the package,
   set the identity, reload the entry), so a session that has gone wrong is abandoned
   without losing its footing. The channel runs both ways: the user can interrupt
   the agent’s loop at any moment by typing sxk tell "<message>" in a terminal,
   and every subsequent sxk command shows the message to the agent until the agent
   acknowledges it.

• nb2txt and nb-author exist because the corpus is notebooks and the deliverable is
  a notebook, while an agent reads and writes text. nb2txt extracts from a notebook
  exactly what its human author typed (input and text cells), and nothing the kernel
  generated (output cells). nb-author is the way back: from the agent’s typed session
  it builds a notebook of input cells only, which the user then runs top to bottom
  themselves, watching every output appear on screen.

• reporter exists because a result produced in the long-lived sxk kernel may silently
  depend on everything that kernel evaluated before it. Its job, in plain terms: run a
  given script on a brand-new kernel that has seen nothing else, and hand back the full
  transcript, with every line that looks like an error or warning pulled out. It renders
  no verdicts; judging the transcript is the agent’s job. The idea behind this is that:
  “it worked in my temporary kernel” is a weak statement that is easily corrupted. In
  contrast: “it works on a fresh kernel, here is the transcript attached” is a claim the
  user can audit.

• WorkAs is the identity verb, and the one piece that lives in the package rather than
  the toolkit. The first thing an agent runs is WorkAs["Vasko-bot"]: it switches to
  the agent’s own alias, drops the curator flag, leaves the user’s configuration file un-
  touched, and verifies that the switch took. That is to ensure that the agent does not
  accidentally write in under the user alias.

• Compute gains a progress channel: it writes one line per finished component into a log
  file, and sxk displays the latest line together with how long ago it was written. This
  is the shell’s substitute for the progress monitor a notebook shows, and it doubles
  as the stall detector: a kernel that is busy while its latest line keeps getting older is
  stuck on one component. This gets flagged and the agent is forced to reconsider the
  computation approach.

• METHODS.md and TRAPS.md are hint files, keyed by symptoms the agents experienced
  during real runs — “the hard-won lessons”. METHODS.md holds approach hints, each
  with the cost record that earned it. TRAPS.md holds the silent failures: the cases
  where the kernel or the package returns a wrong or empty answer with no error.
  Together they are a rudimentary continuous-learning protocol: a setback in one run
  is written down as a hint, and every later run reads the hints before hitting the same
  wall. Section 5.2 contains one full turn of that cycle.




                                        – 28 –
  • LADDER.md is policy. It defines what counts as a structurally different attempt on
    an obstacle, what counts as a verified fact, and how many failed attempts and how
    much kernel time one obstacle is worth. Past those thresholds the agent must stop
    working on the obstacle and write a report for the user, whose most important line
    is the single question whose answer would unblock it.

The working contract, in one line: cheap attempts, loud failures, auditable claims.
      The budgets and thresholds are configuration, not doctrine, and the user controls
them. They live in one flat text file, agent/kit.conf, which the user edits like any other
file; a single value can also be overridden for one session from the terminal, with sxk set,
and sxk config prints every effective value and where it came from. The full list is in
Section C. The budget levers are enforced by sxk itself; the stall thresholds are advisory,
because nothing can force an agent to comply. What the toolkit cannot enforce, it makes
visible.

5.2      Example blind runs
With the toolkit written down, we gave an agent three tasks. Each run saw the cloned
repository, the toolkit, and its task, and none of our earlier attempts22 . Run 0 exercises
the from-scratch path; runs 1 and 2 take on a published paper, the accelerating and su-
persymmetric AdS4 black holes of [13], starting from its arXiv source. Table 2 lists the
three tasks, as the runs’ journals record them, and under each task the entries the run
produced: seven in total, five authored and two theories recycled from the human’s corpus
with CopyData.
     Every authored entry was replayed on a fresh, isolated kernel, and the paper-facing
ones were checked against the published equations one by one, with the AdS radius kept
general where the paper sets ℓ = 1. Run 2’s record is the deepest: the boundary metric
and gauge field at the cutoff, the cancellation of both divergent orders of the counterterm
bracket in an ADM slicing with shift (no template for this existed in the corpus), a traceless
boundary stress tensor with its Ward identities, all four charges, the renormalised on-shell
action, the quantum statistical relation, the Smarr formula, and the first law with all eight
residuals vanishing identically.
     Table 3 is the campaign’s ledger. Its sharpest reading is that the kernel time is the
cheap part; the expensive part is deciding what to ask the kernel. Productive tensor algebra
took twelve minutes against three hours and sixteen minutes of wall clock, and starting
kernels cost more than every Ricci tensor, variation and simplification combined; for most
of the clock no kernel was busy at all, the agent being occupied with reading the corpus,
choosing an approach, authoring notebooks and verifying. The table also shows the kernel
spending as much time on attempts that timed out as on attempts that worked, and that
is expenditure, not waste: a budgeted attempt costs its budget, leaves the kernel alive, and
returns a verdict, and those verdicts are what located each obstacle precisely enough for
the method that dissolved it to be found.
 22
      The runs’ journals, reports and resource ledgers are available on request, like the harness of Section 4.




                                                    – 29 –
  run 0: Build the theory of three-dimensional Einstein gravity with a negative cosmological
  constant from nothing, and show that the BTZ black hole solves its equations of motion.
    Vasko-bot/Thr__3dL__Einstein-AdS
    Vasko-bot/Sol__3dL__BTZ__Global

  run 1: Recreate sections 2.1 and 2.2 of [13], the accelerating black hole of minimal gauged
  supergravity and the regularity analysis of its spindle horizon, starting from the paper’s arXiv
  source.
    Vasko-bot/Sol__4dL__Accelerating-black-hole__PD
    the theory Thr__4dL__Minimal-gauged, recycled from the human’s corpus
  run 2: Recreate the same paper’s section 3, the holographic thermodynamics, per a written
  brief: the solution induced on the cutoff slice, the conformal boundary solution, and the ther-
  modynamic sections appended to run 1’s entry.
    Vasko-bot/Sol__3dL__Induced-accelerating-black-hole__ADM
    Vasko-bot/Sol__3dL__Boundary-accelerating-black-hole__Conformal
    four sections appended to run 1’s entry
    the theory Thr__3dL__Boundary-minimal-gauged, recycled from the human’s corpus

Table 2. The three tasks, as the runs’ journals record them, lightly trimmed, and under each task
the entries the run produced under the agent’s alias. Recycled means copied unmodified from the
human’s corpus with CopyData.

                                                      run 0             run 1          run 2
         wall clock                               ≈ 35 min          40 min       2 h 01 min
         productive kernel time                    ≈ 1 min         ≈ 2 min       9 min 10 s
         kernel time in budgeted timeouts              ≈0      ≈ 5 min 30 s      9 min 10 s
         full xAct-stack kernel loads                    9                3              14
         sxk submissions                                57              95              393
         front-end utility launches                     12                7              17
         context-counter tokens                     ≈ 310k         80–100k           ≈ 308k
         entries authored (recycled)                     2          1 (+1)           2 (+1)
         setbacks, all recovered                         4                5               6

Table 3. Time and resources of the three runs, transcribed from their records: times from file
modification times and in-kernel timings, counts from the session logs. The token counter is the
agent harness’s context counter, read by the agent at the time: its exact semantics are opaque to us
and it is not billed API volume, so it is useful for the relative weight of the runs, not for cost; run
1’s figure is an estimate cross-checked against the other two. Run 0’s wall clock spans its two turns
and excludes a ten-minute orientation turn in which the agent read the toolkit’s documentation.


    Where the runs struggled is more instructive than where they cruised. Run 0 produced
the one failure that no guard caught. The agent had copied a cell out of a corpus notebook,
and the front end had long ago hard-wrapped that cell’s longest product at the width of
the screen. Read back as plain text, the inserted line break split the product into two
syntactically complete expressions, the variational derivative acted on the constant first




                                                – 30 –
half, returned zero, and a zero equation of motion was stored with no message anywhere.
It surfaced minutes later, as a solver complaining about a degenerate system. The repair
took four minutes, and the incident is now both a TRAPS.md entry and a warning wired
into the authoring tool: one run’s setback, become the next run’s hint.
      In run 1, Einstein’s equations verified in sixteen seconds and Maxwell’s would not.
Three structurally different attempts were made, each hit the 110-second budget. The
first exit is the one the ladder prescribes at the threshold: stop grinding and ask what the
computation is a check of. For this ansatz Maxwell’s equations hold with the structure
functions kept arbitrary: they are satisfied by the shape of the metric and gauge field
alone, before any particular solution is chosen. Substituting the explicit quartic structure
functions had therefore been gratuitous work; kept symbolic, the check ran in seconds
and proves that stronger, ansatz-level statement. The one human intervention during the
campaign attacked the same obstacle. It was a prompt suggesting to remove the dependence
on trigonometric functions by exchanging the polar coordinate θ for x as cos θ = −x, which
makes every metric function rational. Rebuilt in that chart, the obstacle disappeared: the
check that had timed out three times ran in a tenth of a second23 .
      Run 2’s hardest obstacle was solved by the agent alone. The boundary stress tensor
is assembled out of ingredients that are each small, a couple of hundred leaves apiece.
Combining them, with the exact data of the cutoff slice substituted, produces one rational
expression in seven parameters that is too large to bring to a common denominator in any
reasonable time: three structurally different attempts at simplifying it hit their budgets
and were cut off. The method that worked never forms that expression. First expand
formally: write each function on the cutoff slice as a series in the cutoff with undetermined
coefficients, so that each order of the counterterm bracket becomes a compact formula in
those coefficients, and the divergent orders cancel identically at the level of the formulas.
Then substitute: compute one inexpensive series per slice function and feed its coefficients
into the per-order formulas. Each step fit comfortably inside the budget that the direct
route had blown three times.
      The human’s hand in the campaign is three prompts and two interruptions, and nothing
else:

   • the three prompts of Table 2;
   • between run 0’s two turns: an input-formatting fix, and a request to extend the entry;
   • during run 1: the mid-run interruption hinting to change coordinates.

The stall ladder never fired; every obstacle was overcome before the thresholds compelled
a report. Silent failures did occur, seven of them, wrong or empty answers with no error.
Six were caught by discipline the hint files had already written down; the seventh, the
stored zero above, is why it is written down now. For calibration: an earlier attempt at
the same paper, made before the toolkit and its hint files existed, ran some twelve hours
  23
    Every slow step sped up with it, by roughly three orders of magnitude. This was the largest single
speed-up of the campaign, and it came from the human, not from the agent’s next attempt. It is why sxk
keeps the two-way channel open at all times.




                                               – 31 –
and was abandoned with nothing meaningful to show. The same paper, the same package,
the same kind of agent; what changed in between is the toolkit.
     None of this is a mature workflow. The toolkit is some seven hundred lines of shell and
three text files; the corpus the agent read holds under twenty records. What we expect
is that two effects will compound to significantly better results and a better user/agent
experience: every codified paper enlarges the set of worked examples the next agent reads,
and every setback sharpens the hint files, so later runs should need less time and less
supervision than the earlier ones. The direction this points in is: agents that contribute
rather than merely “codify papers”. SolutionsX plays a crucial part in that as it is the
verifier: an agent’s ideas, like anybody’s, are mostly wrong, and SolutionsX is the machine
that tells it so before it tells you.

6    Discussion

In this paper we have introduced SolutionsX, a new Mathematica package based on xAct.
The main motivation behind creating this package is the desire to turn existing papers and
novel calculations into verifiable, re-usable code. SolutionsX provides two main contribu-
tions on top of xAct: a unified database of xAct environments, together with a workflow to
call, load and operate with them; and a flexible way to compute the components of tensors
living on multiple vector bundles simultaneously. The package automatically ports xAct’s
abilities to work with:

    • abstract tensors (xTensor): tensor symmetries, generalized connections/covariant
      derivatives, tensor rules, tensor densities, Lie derivatives, variational derivatives

    • explicit coordinate charts (xCoba): coordinate transformations of tensors

    • differential forms (xTerior): forms, exterior derivative, Cartan structure equations,
      Lie derivatives, inner contractions, variational derivatives of forms

    • spinors in arbitrary dimensions (FieldsX): inner bundles with metric, spin struc-
      ture, spin connection, gamma matrices, spinors, Fiertz identities, BRST operators,
      cohomology

All of this functionality allows one to work with SolutionsX on a large class of geometry/-
supergravity/QFT problems. The examples which ship with the package focus on explicit
supergravity solutions, but that is just a sliver of what one can achieve with xAct. We
would like to categorize the class of problems amenable to SolutionsX-codification in three
categories: (A) working today, (B) can be made to work with minimal extension to xAct,
(C) need major extension to xAct.




                                           – 32 –
Class A: working today

Working with Lagrangian          Equations of motion, checking closure under
theories                         supersymmetry variations, Killing spinor equations.
                                 Within SolutionsX such problems will fall into the Thr
                                 category as no explicit chart will be defined
Working with higher              This should really be bundled together with the
derivative Lagrangian theories   previous class of problems as it requires no new
                                 functionality, but we want to explicitly emphasize it,
                                 especially because the algebra gets progressively more
                                 involved, which is where a CAS starts to shine
Working with explicit            Within SolutionsX such problems are usually extending
solutions of supergravity or     a Thr entry with a local chart, thus making it a Sol
devising fixed curved
backgrounds on which one can
place a QFT/SQFT/SCFT
Holographic renormalization:     Within SolutionsX this is a chain of related entries: the
Fefferman–Graham                 bulk Sol, its Fefferman–Graham chart as a second Sol,
expansions and induced           and the induced boundary solution as a third. The
boundary data                    boundary stress tensor of the agent runs in Section 5.2
                                 was assembled this way



Class B: minimal extension to xAct

Supersymmetric localization à    In such a problem SolutionsX can already handle: the
la Pestun [14]                   rigid background, the off-shell closure of the algebra, the
                                 QV deformation. What it cannot yet do is one-loop
                                 determinants and instantons, see class C.
Equivariant localization in      The needed technical extension is to introduce
supergravity [15, 16]            polyforms and the equivariant exterior derivative of the
                                 Cartan model dX = d − ιX , nilpotent on X-invariant
                                 forms since d2X = −LX
Dimensional reductions &         Take for example reducing 11d supergravity on S 4 [17].
consistent truncations in        This can be achieved by a simple interplay between
supergravity                     three SolutionsX entries: one for the 11d space, one for
                                 the S 4 and one for the 7d space together with its vectors
                                 and scalars. The required functionality to make this
                                 actually pleasant to codify is a rudimentary list of rules
                                 that automatically generates the field content of the 7d
                                 theory, see class C




                                          – 33 –
Class B: minimal extension to xAct (continued)

Verifying explicit instanton     Solving the ADHM constraints is finite matrix algebra
gauge fields obtained from the   and needs only Mathematica itself. The resulting gauge
ADHM construction [18]           field on an R4 chart is then a Sol like any other:
                                 self-duality, the Yang–Mills equations and the
                                 topological charge density are component checks. On
                                 paper this needs no extension at all; it sits in class B
                                 because a nonabelian gauge field through a FieldsX
                                 inner bundle has not been exercised in SolutionsX. The
                                 general-k proof of self-duality and the integration over
                                 the instanton moduli space are not claimed; for the
                                 latter see class C



Class C: major extension to xAct

Dimensional reductions &         That would require teaching xAct group theory and Lie
consistent truncations - done    algebras. A possible route will be integration with
properly                         LieART [19].

Exceptional geometry             Exceptional field theory organizes the supergravity fields
                                 into representations of Ed(d) , with a generalized Lie
                                 derivative in place of the ordinary one [20]. The calculus
                                 is finite but it is representation theory throughout, so
                                 this entry stands or falls with the group-theory layer of
                                 the previous one.
Supersymmetric localization -    On a general rigid background the class B algebra ends
done properly                    at the BPS locus; what follows is an equivariant index
                                 engine, in two programmable halves. The geometric half
                                 is tensor algebra: the zeros of the supercharge’s Killing
                                 vector, and the linearized field content around the locus
                                 (xPert territory). The index half needs no xAct: the
                                 weights of the isometry action at each fixed point are
                                 finite linear-algebra data, and the Atiyah–Bott formula
                                 turns them into the index and hence the one-loop
                                 determinant [14, 21]; instanton blocks glue over the
                                 same fixed points [22]. A long shot, but every step is
                                 finite, and the input is what an entry already stores.




                                         – 34 –
Class C: major extension to xAct (continued)

Spectra and perturbations               xAct already covers the algebraic part: xPert builds
                                        metric perturbation theory to any order [23]. The
                                        reduction to master equations [24] and the spectral step
                                        of solving them are the missing layers; for the latter
                                        numerical tools exist outside xAct [25].


The tables above make it clear that xAct + SolutionsX are already powerful tools in the
quest of codifying calculations on a large array of problems. They also make it clear that
there is a long list of homework in extending the tools to capture a larger set of problems
and research programs24 .
     We would like to use this paper as an opportunity to call out to “programmatically
inclined” physicists to help develop some of these extensions: if that is in your ballpark,
email me at vasildimi@gmail.com.
     The second message of this paper is that once problems are codified in a verifiable
fashion, agents suddenly become far more useful compared to “ordinary chat”. We ex-
perimented with giving Claude Code the task of recreating a paper [13] and it managed
to codify it correctly in under three hours, see Section 5.2. In order to aid its work we
developed a simple agent toolkit, which ships with the GitHub version of SolutionsX. The
promise here is worth emphasising. An agent who is given access to a good database and
an independent verifier performs well on re-creating existing literature. More importantly,
this might be a pathway to allow agents to operate on complex open problems in hep-th
by separating the task in two: the thinking, ideating part (agents are already pretty good
at that), and the continuous testing, fidgeting and verifying of their claims with standard
code. SolutionsX provides the framework for the second part when it comes to supergrav-
ity/QFT related problems. Still, the agent toolkit that we have provided is in a somewhat
rudimentary, experimental stage.
     We would like to use this paper as an opportunity to call out to “physically inclined”
developers to help streamline the database, make SolutionsX smoother to use and develop
a more sophisticated agent toolkit: if that is in your ballpark, email me at vasildimi@
gmail.com.
     Finally, the current Curated list of examples will continue growing, so keep an eye on
the GitHub repository. On that note, if you start using SolutionsX and you have a set of
data entries that you deem valuable, email me at vasildimi@gmail.com and I will consider
making you a curator, so that your entries can enter the “official” library.

Use of AI

The first prototype of SolutionsX was developed by hand in 2022, for the calculations
of [26], and the core of the package is the author’s: the simulation of objects with
 24
      The extension suggestions are limited by the author’s own understanding; feel free to email me yours.




                                                   – 35 –
Association’s and the core logic of Compute.            Claude Code, running the Opus 5 and
Fable 5 models, wrote the symbol reference pages of the in-system documentation;
while the tech notes were written by the author. It also rebuilt the component engine
behind Compute towards speed-up, carried out smaller Kernel tasks and maintenance, and
templated the LATEX machinery of the present paper. The agent toolkit was developed
by Claude Code after extensive discussions on its architecture. Throughout, Claude Code
was treated as a collaborator: in particular, it wrote almost all of “its own section”:
Section 5, reporting there how its previous instances drove SolutionsX.

A     Mathematica notation

The cells of this paper use a handful of Mathematica idioms that a reader coming from
another CAS may not have met. This appendix collects them. It does not replace the
Mathematica documentation; it is just enough to keep reading.

Special characters The indices and the products of the paper are single glyphs, each
carrying a long name:


 glyph        long name                          role
m, n, . . .   \[ScriptM], \[ScriptN], . . .      abstract indices on a tangent bundle
a, b, . . .   \[GothicA], \[GothicB], . . .      frame-bundle indices
A, B, . . .   \[DoubleStruckCapitalA], . . .     spinor indices
I, J, . . .   \[GothicCapitalI], . . .           indices on further inner bundles
 M, N         \[ScriptCapitalM], . . .           manifolds
    ⊗         \[CircleTimes]                     the symmetric product of forms (Section 3.2)
    ∧         \[Wedge]                           the exterior product (xTerior)
     ·        \[CenterDot]                       FieldsX’s product of Grassmann-odd objects
   7→         \[RightTeeArrow]                   xTensor’s infix IndexRule
    ⌞⌟        \[UnderBracket]                    an ordinary name character, see below

The role column is a convention, not a constraint: nothing in SolutionsX ties a glyph to a
role, and the assignments above are simply what the author found visually appealing. Any
symbol works in any position. Typing the long name in a notebook produces the glyph
the moment the name is complete; most characters also carry a short alias between two
presses of Esc, listed in the documentation. The last row exists because the underscore
itself is not available in names: _ is Wolfram syntax for a pattern, so the corpus notebooks
use ⌞⌟ where a human would write _. The last two rows appear in the corpus notebooks
rather than in the cells of this paper.

Applying functions A function of one argument can be applied in three equivalent
ways: bracketed, postfix with //, and prefix with @




                                               – 36 –
                                                                                     In[68]:=
  Simplify[Sin[x]^2 + Cos[x]^2]
  Sin[x]^2 + Cos[x]^2 // Simplify
  Simplify@(Sin[x]^2 + Cos[x]^2)

                                                                                     Out[68]=
  1


                                                                                     Out[69]=
  1


                                                                                     Out[70]=
  1


The paper’s cells use all three, favouring // for pipelines and @ for single wrappers.

Pure functions Simplify[#] & is a function without a name: # marks where the ar-
gument goes and the trailing & closes the definition. It applies in the same three ways

                                                                                     In[71]:=
  (Simplify[#] &)[Sin[x]^2 + Cos[x]^2]
  Sin[x]^2 + Cos[x]^2 // (Simplify[#] &)
  (Simplify[#] &)@(Sin[x]^2 + Cos[x]^2)

                                                                                     Out[71]=
  1


                                                                                     Out[72]=
  1


                                                                                     Out[73]=
  1


and /@ maps it over a list
                                                                                     In[74]:=
  Simplify[#] & /@ {Sin[x]^2 + Cos[x]^2, Cosh[x]^2 - Sinh[x]^2}

                                                                                     Out[74]=
  {1, 1}


The slot may sit anywhere in the body, so a function of two arguments becomes a pure
function of one of them by fixing the other
                                                                                     In[75]:=
  D[#, x] & /@ {x^2, Sin[x]}

                                                                                     Out[75]=
  {2 x, Cos[x]}


Most of the $Apply entries of Section 3.3 are pure functions of exactly this kind.

A list as an argument sequence @@ feeds a list to a function as separate arguments,
so the following are the same expression




                                           – 37 –
                                                                                   In[76]:=
  f[a, b, c]
  f @@ {a, b, c}

                                                                                   Out[76]=
  f[a, b, c]


                                                                                   Out[77]=
  f[a, b, c]


The paper meets it as RulesToChain @@ {...} in Section 3.3.

Previous outputs Within a cell, % is the last output and %% the one before it; a trailing
; suppresses the display of a result without suppressing the result

                                                                                   In[78]:=
  Sin[x]^2 + Cos[x]^2 // Simplify;
  5;
  %% + %

                                                                                   Out[80]=
  6


This is what lets the verification cells of Section 3.4 read as short pipelines.

Rules, and rules with Function A rule lhs -> rhs rewrites, via the operator /.,
exactly the pattern it names and nothing else
                                                                                   In[81]:=
  rule = {f[x] → Sin[x] + Cos[x]};
  f[x] + 5 /. rule
  f'[x] + 5 /. rule

                                                                                   Out[82]=
  5 + Cos[x] + Sin[x]


                                                                                   Out[83]=
  5 + f'[x]


The second line is untouched: the rule knows what f[x] becomes but not what f is, so
the derivative has nothing to act on. The cure is a rule for the head itself, with Function
carrying the body
                                                                                   In[84]:=
  frule = {f → Function[x, Sin[x] + Cos[x]]};
  f[x] + 5 /. frule
  f'[x] + 5 /. frule

                                                                                   Out[85]=
  5 + Cos[x] + Sin[x]


                                                                                   Out[86]=
  5 + Cos[x] - Sin[x]




                                            – 38 –
Now the substitution commutes with differentiation. This is why Gen returns rules of
exactly this shape (Section 3.2).

Associations An association is Wolfram’s dictionary, written <|key -> value|>. Values
nest, and a nested value is looked up by giving the keys in sequence
                                                                                             In[87]:=
    assoc = <|"a" → 1, "b" → <|"c" → 2|>|>;
    assoc["b", "c"]

                                                                                             Out[88]=
    2


Assigning into a sequence of keys creates the entry. A record sol in this paper is one associa-
tion, which is why every address in its cells has the shape sol[$metric, gg, Expression],
and why a solution is built by assigning into such addresses (Section 3.2).

B       Public symbols of SolutionsX

Every public symbol of SolutionsX, with its usage message as displayed by the in-system
documentation. Names in teal link within this appendix; built-ins link to the Wolfram
Language reference. This appendix is generated from the package documentation sources
and is not edited by hand.

Configuration and identity

$DefaultDataDirectory

    $DefaultDataDirectory
        is the path used for data and notebooks when no other is set: the SolutionsX folder under
        $LocalBase.


$DataDirectory

    $DataDirectory
        is the path under which data and notebooks are stored and retrieved.
        Entries live in $DataDirectory/$Alias/name/. Set it with SetDataDirectory.

$Alias

    $Alias
        is the sub-directory of $DataDirectory holding the current user’s entries: their identity.
        SaveData and DeleteData act only under it; GetData and OpenData default to it but read any
        alias via "alias/name" or the Alias option. Set it once with SetAlias; it persists in the user
        configuration file.




                                                 – 39 –
Alias

 Alias
   is an option for GetData and OpenData that selects the alias to read from, equivalent to the
   "alias/name" form.

$Curator

 $Curator
   is True when this user curates the published Curated corpus: it unlocks working under the
   Curated alias and CurateData. Set it with SetCurator; it persists in the user configuration
   file.

SetAlias

 SetAlias["alias"]
   sets $Alias, refreshes the argument completions, and records the alias in the user configuration
   file so later sessions restore it.
 SetAlias["alias", Permanent->False]
   sets it for this session only.

SetDataDirectory

 SetDataDirectory["path"]
   sets $DataDirectory, refreshes the argument completions, and records the path in the user
   configuration file so later sessions restore it.
 SetDataDirectory["path", Permanent->False]
   sets it for this session only.

SetCurator

 SetCurator[True]
   marks this user as the curator of the Curated corpus and records it in the user configuration
   file; SetCurator[False] removes the mark.
 SetCurator[flag, Permanent->False]
   sets it for this session only.

WorkAs

 WorkAs
   ["owner-bot"] switches this session to an agent identity: $Alias is set to the given agent alias
   and the curator flag is dropped. The user configuration file is never written, so the switch ends
   with the kernel.
   Only aliases of the shape "<owner>-bot" are accepted — one agent alias per human, e.g.
   "Vasko-bot"; your own identity is set with SetAlias. A refused alias, or a switch that does not
   take, aborts the evaluation. Experimental, part of the agent kit.




                                             – 40 –
LocateData

 LocateData[]
      points $DataDirectory at the data tree containing the current notebook, for this session only,
      then displays the package load panel and the Data status.
 LocateData[dir]
      does the same for an explicit entry directory path.
      It relocates only when the notebook sits inside a Data entry directory (. . . /Data/alias/name/)
      or at a SolutionsX repository root; anywhere else it leaves the configured values untouched
      and just displays them. It is the display line of NewData’s initialization cell.

Welcome

 Welcome[]
      guides a first session: it asks where your data should live and what your alias is, records both
      in the user configuration, and offers the curated entries — individually selectable — to copy
      under your alias.
      Without a front end it prints the same steps as commands. Welcome[] never touches the
      curator flag and can be re-run at any time.

SolutionsXHelp

 SolutionsXHelp[]
      opens the SolutionsX guide page in the Documentation Center.

Objects and their keys

Gen

 Gen[sol[$function,key]]
      gives the rule sending the scalar function key to its stored Expression, for use with /.
 Gen[sol[$form,key]]
      gives the rule sending the form’s Symbol to its stored Expression.
 Gen[sol[$rule,key]]
      gives the stored Expression of the rule entry key.
      Gen gives {} when the entry is absent, so it is safe to apply unconditionally.


Dimension

 Dimension
      is a key of $manifold and $bundle objects: the dimension, a positive integer.

Index

 Index
      is a key of $manifold, $frame, $spinStructure and $bundle objects: the abstract indices to
      register, as a list of symbols.




                                                – 41 –
Name

 Name
   is a key of $manifold and $chart objects: a string from which SaveData composes the entry
   name.

$auto

 $auto
   is a key of most objects: slots for the symbols xAct creates alongside the definition, each
   carrying a Routine (the Chain recipe Compute follows) and its computed Value.

ValidateObject

 ValidateObject[object,expr,types]
   checks the association expr against the template of object, and returns it unchanged if it passes.
 ValidateObject[$solution,sol,types]
   checks a whole solution, object type by object type.
   types is a list of key selectors, normally {PropKeysOf, OptKeysOf}. Failure issues a message
   and throws object.

IncludeTo

 IncludeTo[sol[object],assoc]
   validates assoc, stores it under object, and makes the corresponding xAct definition.
 IncludeTo[sol[object],{assoc..}]
   does the same for several entries in order.
   The keys of assoc are those of Options[object]; missing keys take their default. Any entry
   already under the same key is unloaded first.

DropFrom

 DropFrom[sol[object],key]
   undefines the entry and removes it from sol; a list of keys is also accepted.
   Unlike Unload, DropFrom forgets the stored association as well.

MergeWith

 MergeWith[sol,assoc]
   includes and loads every entry of the solution association assoc into sol.
   It refuses, with a message, if the two share any symbol or any key.

Instantiate

 Instantiate[sol]
   clears sol and makes it an empty solution: an association over $Objects, carrying the UpValues
   of Load, Unload, IncludeTo, DropFrom and MergeWith.
 Instantiate[sol,assoc]
   does the same and then merges assoc into it.




                                             – 42 –
Building expressions

MakeArray

 MakeArray[expr]
   gives the component array of expr, which may be a line element written with CircleTimes or
   a differential form written with Wedge.
   The chart is deduced from the Diff’s appearing in expr. It is the inverse of MakeMetric and
   MakeForm.


MakeMetric

 MakeMetric[chart][array]
   gives the line element of the symmetric matrix array in chart, as a sum of CircleTimes of
   coordinate differentials.

MakeForm

 MakeForm[chart][array]
   gives the differential form of the totally antisymmetric array in chart, as a sum of Wedge of
   coordinate differentials.

RulesToChain

 RulesToChain[a -> b -> c]
   gives {a -> b, b -> c}, the form Compute expects for a raising or lowering ladder.

ExpandForms

 ExpandForms[sol][expr]
   rewrites every differential form of sol appearing in expr as its companion tensor contracted with
   a wedge of coordinate differentials, and expands the exterior derivative of every degree-zero
   expression in the same sweep.

WedgeCoeff

 WedgeCoeff[sol][expr]
   extracts the antisymmetric component tensor of a form written in wedges of coordinate dif-
   ferentials, as the lowest-rank equivalent: a form of degree p above half the dimension d is
   Hodge-dualized and expanded first, and the extraction runs on the dual, giving the compo-
   nent tensor of the Hodge dual with d-p free indices.
   For p at most d/2 the result is the plain component tensor, so WedgeCoeff inverts ExpandForms:
   the companion tensor comes back exactly.
   Reconstructing a dualized form from its result costs the double-dual sign (-1)ˆ(p(d-p)) sign(det
   g) — in Lorentzian signature the volume form extracts to minus its coefficient. That sign is
   mathematics, not a convention.
   The result is presented in the order of the manifold’s Index list: the frees introduced by the
   extraction take the first names not already free in expr, and ScreenDollarIndices renames the




                                             – 43 –
   dummies to the following unused ones. If the registered list is exhausted mid-extraction, new
   indices are generated and registered, so the extraction always succeeds.
   Only ContractMetric is applied to the result; simplification is left to the caller.

ComputeDiffs

 ComputeDiffs[chart]
   installs the rules that canonicalise, and annihilate repeated, wedge products of the coordinate
   differentials of chart.

BasisOfVBundle

 BasisOfVBundle[bundle]
   gives the first basis or chart defined over bundle, or None if there is none.
   It issues a message and throws $Failed if bundle is not a vector bundle.

ToBases

 ToBases[expr]
   rewrites every abstract index of expr in the basis belonging to its vector bundle.
   The option Not -> {basis..} leaves those bases untouched.

ToArray

 ToArray[expr]
   gives the explicit component array of expr, by taking it to bases, tracing dummies and resolving
   component values.
   The option Not -> {basis..} leaves those bases untouched.

Computing

Compute

 Compute[sol[object,key,$auto,autoKey]]
   computes the components of autoKey by walking its stored Chain, and stores them under
   Value.
 Compute[sol[object,key]]
   does this for every automatic tensor of the entry.
   A Chain entry HoldForm[expr] -> {slots} takes the components from expr; an entry {slots}
   -> {slots} raises or lowers indices with the metric. Nothing is computed if the Chain is unset.
   Options are Chain, which overrides and stores the recipe, Using, which chooses the metric of
   each bundle, and Apply, which defaults to $Apply.
   Compute checks the Chain’s slot specification against the object, reports an Apply key that is
   neither Map nor ParallelMap, and refuses to raise a slot whose vector bundle has no metric.




                                             – 44 –
$Apply

 $Apply
   is the default value of the Apply option of Compute.
   It is a list of rules whose keys are Map or ParallelMap and whose values are applied to computed
   components; the default is {Map -> Together, ParallelMap -> Simplify}.

Loading and unloading

Load

 Load[sol]
   installs the UpValues of sol, then makes the xAct definitions of every entry it holds.
 Load[sol[object],key]
   loads a single entry; a list of keys is also accepted.
   Load is the step that turns an association returned by GetData into live xAct definitions.


Unload

 Unload[sol]
   undefines every xAct object of sol, in reverse order of construction, keeping the stored associ-
   ation.
 Unload[sol[object],key]
   undefines a single entry; a list of keys is also accepted.
   Unload does not delete the entry: use DropFrom for that.


Resurrect

 Resurrect[symbol]
   rebinds any symbol removed by an xAct Undef, by round-tripping symbol through Compress
   and replacing Removed[name] by Symbol[name].

Revive

 Revive[sol]
   applies Resurrect throughout sol, to every symbol in the Global‘ context and to $Assumptions.
   It is called after each unload.

ResumeAs

 ResumeAs[sol]
   restores the current notebook’s entry into sol (GetData[] followed by Load) when nothing has
   been loaded in this kernel yet, and rebuilds the Load banner of everything loaded so far
   otherwise.
   Put it at the top of a notebook section: after a kernel quit it resumes from disk; in a full top-
   to-bottom run it only re-shows the banner, so the same notebook supports both workflows.




                                             – 45 –
Storing and retrieving

NewData

 NewData[]
   creates a notebook holding the initialization cell that loads SolutionsX.
   The cell carries no user identity and no absolute paths: LocateData[] finds the data root
   relative to the notebook’s own position; $Alias always comes from the user configuration.

SaveData

 SaveData[sol]
   writes sol and the evaluation notebook into $DataDirectory/$Alias/name/, and echoes the
   destination.
   The name is built from the first manifold’s Name and Dimension, the first metric’s Signature
   and the first chart’s Name: an entry with a chart is a Sol, one without is a Thr.
   Every save stamps sol[$info]: SolutionsX version, the saving alias (LastEdit), date, and the
   Wolfram and xAct versions. The stamp is machine-written and invisible to validation.

Overwrite

 Overwrite
   is an option for CopyData and CurateData: Automatic (default) asks per existing entry in a
   front end and skips headless; True replaces silently; False always skips.

GetData

 GetData[name]
   gives the stored solution association of the entry name under the user’s own alias, validated
   but not loaded.
 GetData["alias/name"]
   (or the option Alias->"alias") reads the entry of another alias.
 GetData[]
   takes the alias and name from the directory containing the current notebook.
   Follow GetData with Load to make the definitions.

OpenData

 OpenData[name]
   opens the notebook of the entry name under the user’s own alias.
 OpenData["alias/name"]
   (or the option Alias->"alias") opens another alias’s entry.

ShowData

 ShowData[]
   displays an interactive browser of the data tree: one button per alias — your own first, marked
   with a pencil — and the entries of the chosen alias with their OpenData, CopyName, CopyData




                                            – 46 –
     and DeleteData actions.
     Every entry shows the name GetData takes, and CopyName copies it as a quoted string, ready
     to paste. The search field filters across every alias as you type. Without a front end ShowData[]
     prints the same tree as text.

CopyData

    CopyData["alias/name"]
     copies the entry name of another alias into your own alias, notebook and all; the source is
     never touched.
    CopyData["alias"]
     copies every entry of that alias into yours, one by one.

CurateData

    CurateData["name"]
     publishes the entry name of your own alias into the Curated corpus. Curator-only; enable
     with SetCurator.

DeleteData

    DeleteData[name]
     permanently deletes the entry directory name and all of its contents.
     DeleteData acts only under the user’s own alias; entries of other aliases cannot be deleted.


C     Configuring the agent toolkit

The toolkit of Section 5.1 is configured by one flat file, agent/kit.conf: KEY=VALUE lines,
integers only. The file is parsed, never sourced, so a malformed line is ignored (and warned
about) rather than executed. Four layers override each other, highest first: sxk set KEY
value, which lives for one session and is surfaced to the agent like a user note until ac-
knowledged; the environment variable SXK_KEY, for scripted runs; the file itself, holding the
owner’s standing preferences; and the built-in defaults. sxk config prints every effective
value together with the layer it came from.
     Each lever is one of two kinds. An enforced lever is acted on by sxk itself: changing
it changes behaviour. An advisory lever is only displayed by sxk; LADDER.md instructs the
agent to act on it, and nothing can force compliance, by design.




                                               – 47 –
lever               kind       default   governs
TRY_SECONDS         enforced      120    the time budget of sxk try when none is given
DO_TIMEOUT          enforced      600    how long sxk do blocks before returning control
WATCH_INTERVAL      enforced        5    the polling interval of sxk watch
WATCH_MAX           enforced      600    total watch time before sxk watch gives up waiting
WAIT_MAX            enforced     3600    the timeout of sxk wait
STALL_SHAPES        advisory        3    failed shapes on one obstacle before the agent must stop
STALL_MINUTES       advisory       30    minutes without a new verified fact before the same

Table 7. The seven levers of agent/kit.conf. Defaults in seconds where the name says so. Three
behaviours are worth spelling out. A try that expires cuts off the expression but the kernel, with
all its state, survives: a wrong-shaped attempt costs TRY_SECONDS, not a silent half-hour. A do
that times out returns the prompt to the agent while the submission keeps running, and a watch
that ends is a decision point, not an abort. STALL_MINUTES is also the one advisory lever with an
enforced display: a busy kernel whose compute pulse is older than it is flagged as stale by sxk
status and sxk watch, as a report, not a verdict.


References

 [1] J. M. Martín-García, xPerm: Fast index canonicalization for tensor computer algebra,
     Computer Physics Communications 179 (2008), no. 8 597–603, [arXiv:0803.0862].
 [2] M. Fröb, FieldsX – An extension package for the xAct tensor computer algebra suite to
     include fermions, gauge fields and BRST cohomology, arXiv:2008.12422 [gr-qc,
     physics:hep-th] (May, 2021) [arXiv:2008.12422].
 [3] K. Peeters, Cadabra2: Computer algebra for field theory revisited, Journal of Open Source
     Software 3 (2018), no. 32 1118.
 [4] E. Gourgoulhon, M. Bejger, and M. Mancini, Tensor calculus with open-source software: The
     SageManifolds project, Journal of Physics: Conference Series 600 (2015), no. 1 012002,
     [arXiv:1412.4765].
 [5] I. M. Anderson and C. G. Torre, New symbolic tools for differential geometry, gravitation,
     and field theory, Journal of Mathematical Physics 53 (2012) 013511, [arXiv:1103.1608].
 [6] T. Hubert, R. Mehta, L. Sartran, et al., Olympiad-level formal mathematical reasoning with
     reinforcement learning, Nature 651 (2025) 607–613.
 [7] N. Sothanaphan, Resolution of Erdős Problem #728: A writeup of Aristotle’s Lean proof,
     arXiv:2601.07421 (2026) [arXiv:2601.07421].
 [8] N. Alon, T. F. Bloom, W. T. Gowers, D. Litt, W. Sawin, A. Shankar, J. Tsimerman,
     V. Wang, and M. M. Wood, Remarks on the disproof of the unit distance conjecture,
     arXiv:2605.20695 (2026) [arXiv:2605.20695].
 [9] ZW. Chong, M. Cvetic, H. Lu, and C. Pope, General Non-Extremal Rotating Black Holes in
     Minimal Five-Dimensional Gauged Supergravity, Physical Review Letters 95 (October, 2005)
     161301, [hep-th/0506029].
[10] J. Gutowski and H. Reall, Supersymmetric AdS5 black holes, Journal of High Energy Physics
     2004 (February, 2004) 006–006, [hep-th/0401042].




                                             – 48 –
[11] D. Cassani, J. Lorenzen, and D. Martelli, Comments on supersymmetric solutions of minimal
     gauged supergravity in five dimensions, Classical and Quantum Gravity 33 (June, 2016)
     115013, [arXiv:1510.01380].
[12] J. P. Gauntlett and J. B. Gutowski, All supersymmetric solutions of minimal gauged
     supergravity in five dimensions, Physical Review D 70 (October, 2004) 089901,
     [hep-th/0304064].
[13] D. Cassani, J. P. Gauntlett, D. Martelli, and J. Sparks, Thermodynamics of accelerating and
     supersymmetric AdS4 black holes, Physical Review D (October, 2021) 086005,
     [arXiv:2106.05571].
[14] V. Pestun, Localization of gauge theory on a four-sphere and supersymmetric Wilson loops,
     Communications in Mathematical Physics 313 (July, 2012) 71–129, [arXiv:0712.2824].
[15] P. B. Genolini, J. P. Gauntlett, and J. Sparks, Equivariant localization in supergravity,
     arXiv:2306.03868.

[16] D. Martelli and A. Zaffaroni, Equivariant localization and holography, Letters in
     Mathematical Physics 114 (January, 2024) 15, [arXiv:2306.03891].
[17] H. Nastase, D. Vaman, and P. van Nieuwenhuizen, Consistent nonlinear KK reduction of 11d
     supergravity on AdS7 × s4 and self-duality in odd dimensions, Physics Letters B 469 (1999)
     96–102, [hep-th/9905075].
[18] M. F. Atiyah, N. J. Hitchin, V. G. Drinfeld, and Y. I. Manin, Construction of instantons,
     Physics Letters A 65 (1978) 185–187.
[19] R. Feger, T. W. Kephart, and R. J. Saskowski, LieART 2.0 – A Mathematica application for
     Lie algebras and representation theory, Computer Physics Communications 257 (2020)
     107490, [arXiv:1912.10969].
[20] D. S. Berman and C. D. A. Blair, The geometry, branes and applications of exceptional field
     theory, International Journal of Modern Physics A 35 (2020), no. 30 2030014,
     [arXiv:2006.09777].
[21] V. Pestun, M. Zabzine, et al., Localization techniques in quantum field theories, Journal of
     Physics A 50 (2017), no. 44 440301, [arXiv:1608.02952].
[22] N. A. Nekrasov, Seiberg-Witten prepotential from instanton counting, Advances in
     Theoretical and Mathematical Physics 7 (2003), no. 5 831–864, [hep-th/0206161].
[23] D. Brizuela, J. M. Martin-Garcia, and G. A. Mena Marugan, xPert: Computer algebra for
     metric perturbation theory, General Relativity and Gravitation 41 (2009) 2415–2431,
     [arXiv:0807.0824].
[24] A. Jansen, A. Rostworowski, and M. Rutkowski, Master equations and stability of
     Einstein-Maxwell-scalar black holes, Journal of High Energy Physics 2019 (December, 2019)
     36, [arXiv:1909.04049].
[25] A. Jansen, Overdamped modes in Schwarzschild-de Sitter and a Mathematica package for the
     numerical computation of quasinormal modes, European Physical Journal Plus 132 (2017),
     no. 12 546, [arXiv:1709.09178].
[26] N. Bobev, V. Dimitrov, V. Reys, and A. Vekemans, Higher-Derivative Corrections and AdS5
     Black Holes, Physical Review D 106 (December, 2022) L121903, [arXiv:2207.10671].




                                              – 49 –
