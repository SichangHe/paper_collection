                                                   ABSTRACT

                                                       Agentic porting of multiple open-source libraries into Rust, with human in the loop, has been per-
                                                   formed for construction of modules within the Open-source Unified TRAnsient Multi-Phase Advanced
                                                   Reactor simulation Kit (Outram Park). With this new methodology, verification and validation with
                                                   human expertise, rather than code generation has become the bottleneck in developing reliable simula-
                                                   tion codes. In this research log, we present the porting of OpenFOAM libraries into the Outram-Foam
                                                   Rust libraries, their preliminary verification and validation (V&V) efforts, and their subsequent use
                                                   in the development of open-source two-phase homogeneous-equilibrium (HEM) choked-flow solvers
                                                   for the Thermo-hydraulic AI Multi-Phase INtegrated Emulator System (TAMPINES) libraries within
arXiv:2608.17504v2 [physics.comp-ph] 17 Sep 2026




                                                   Outram Park such as tampines-steam-tables. V&V efforts of Outram-Foam show that the cavity and
                                                   Sod shock tube cases agree with literature values. For the lid-driven cavity at Re = 100, a three-mesh
                                                   grid-convergence study (20 × 20, 40 × 40, 80 × 80 at a constant refinement ratio of two) gives an ob-
                                                   served order of accuracy of 1.12, consistent with the first-order upwind convection the solver uses, and
                                                   Richardson extrapolation of that sequence recovers the benchmark centerline velocity of Ghia et al. to
                                                   within 0.64%. The port therefore converges at its formal rate and to the published reference value, rather
                                                   than merely agreeing to within a stated tolerance on one mesh. Moreover, the preliminary development
                                                   of tampines-steam-tables shows good agreement with Moody’s HEM charts. Thereafter, the 1D HEM
                                                   solver, developed agentically, is presented and preliminarily validated against the Edwards blowdown
                                                   case. Productivity increases were observed with the use of Claude Code, but domain expertise supplied
                                                   by human experts remains critically required to ensure the generated code can solve the problem effec-
                                                   tively. Further work remains to be done in V&V, but the agentic coding methodology described here
                                                   demonstrates considerable potential to speed up production and development of open-source libraries
                                                   such as Outram Park. These are presented as research notes rather than as a finished study: the results
                                                   are interim, the development history is recorded as it happened, and the contribution is principally one
                                                   of software engineering applied to computational reactor physics rather than one of new physics.


                                                                                                                              KEYWORDS
                                                                          Open Source, TAMPINES, TUAS, OUTRAM PARK, Agentic Coding, LLM, AI




                                                                                                       1
    Research Notes on Agentic Porting, Construction and Initial Verification
    and Validation of Libraries within the Open Source Unified TRAnsient
    Multi-Phase Advanced Reactor simulation Kit (Outram Park) Part I: A
              Software Engineering Log for Thermal Hydraulics
                              Theodore Kay Chen Ong, Sicong Xiao
                       Singapore Nuclear Research and Safety Institute (SNRSI)
                              16 Prince George’s Pk, Singapore 118415
                                        snrokct@nus.edu.sg




1    INTRODUCTION
Simulation of nuclear reactors is important for both research and education. In Singapore’s context,
where Prime Minister Lawrence Wong announced that Singapore would embark on the IAEA Inte-
grated Nuclear Infrastructure Review (INIR) [1], this is especially relevant to the nuclear safety and
human resource development aspects of the INIR. Reliable reactor simulations are also required for
regulators to independently assess the safety claims of vendors. However, simulation of such reactors
in a comprehensive manner often requires a suite of tools ranging from materials, to neutronics and
thermal hydraulics. Such codes are also not readily available due to export control, thus reducing the
reproducibility of research done using export controlled and proprietary codes [2]. Such barriers have
historically made it hard for these export controlled codes to be used in the arena of human resource de-
velopment, where export controlled and proprietary codes are off limits to most students who may want
to learn about nuclear power and nuclear safety. Moreover, such data is difficult to visualise and often
without a freely available integrated graphical user interface (GUI). Hence, its use was largely confined
to technically competent audiences.
     This lack of open-source capability was apparent to the author even before Singapore embarked on
the INIR, and the incompressible open-source system code TUAS [3], was developed in Rust along with
its GUIs also written in Rust, which could compile natively across Windows, Mac and Linux systems
[2], [4], [5]. TUAS was also used to build the CIET Educational Simulator which was validated against
forced and natural-circulation flows in CIET [5], [6]. Figure 1 details the GUI of the CIET Educational
Simulator, which shows its capability to display the temperature distribution during coupled natural-
circulation, thus enabling the user to intuitively grasp the temperature profile one should roughly observe
during natural-circulation:




                                                    2
                                Figure 1: CIET Educational Simulator

     Nevertheless, TUAS was limited in its capabilities as it used the Boussinesq approximation and
could only simulate single-phase, largely incompressible flow. Density changes were not considered
except where natural-circulation was computed. To serve the purposes of the INIR for Singapore, a
larger suite of simulation codes would be required. The author envisioned this suite as the Open-source
Unified TRAnsient Multi-Phase Advanced Reactor simulation Kit (OUTRAM PARK), named after the
Outram Park MRT station in Singapore much like TUAS was named after the TUAS industrial region in
Singapore. Outram Park would contain codes such as TUAS, in addition to a neutronics suite, thermal-
hydraulics simulation capabilities and fission-product transport. Such a scope for a simulator suite would
be vast and cost many man-years to develop. Nevertheless, Outram Park was envisioned as a long term
goal which could provide Singapore with tools required to serve its purposes, and as of July 2026 it
became more relevant because of the INIR announcement.
     Such capabilities were traditionally fulfilled by a fragmented open-source ecosystem, with open-
source frameworks and codes being written in various languages such as Python, C++, C and Fortran
with various compilation configurations. This made the multiphysics coupling required for reactor sim-
ulations difficult. Nevertheless, the open-source ecosystem was still rich, and one could in theory, com-
bine them to produce a coupled multiphysics simulation. These tools include Finite Volume codes such
as OpenFOAM [7] and GeN-Foam [8] helping fill thermal hydraulics, OpenMC [9] and NJOY [10]
fulfilling the part of nuclear data and Monte Carlo neutronics. System codes and simulators such as
OpenModelica [11] and DWSIM [12] were also used by researchers in evaluating system level phenom-
ena. MOOSE is also a notable contribution with its open-source Finite Element Method [13], and this
was used to construct Cardinal [14] which coupled the spectral element solvers with OpenMC. How-
ever, certain codes built on MOOSE such as BISON and SAM [15] were closed source and not easily
available to the general public, thus the results they produced were not easily reproducible by students
and researchers without the clearance for such codes.
     Within this open-source ecosystem, the main challenge was that integration was cumbersome. With
each C++, C and Fortran code requiring their own set of dependencies and build version, compiling them
to work together and integrate in order to run a nuclear simulation would be a challenge. OpenFOAM
has wmake while OpenMC and MOOSE use cmake. Integrating OpenFOAM and OpenMC directly
would therefore be a challenge. Even within MOOSE, an integrated system including a Python script
of 20,000 lines long was created just to handle dependencies, documentation and the ability to run the
same code across various compilers and operating systems [16]. Even MOOSE currently only runs on


                                                    3
Linux or macOS, and virtual machines (including WSL) are required to set it up.
     The ideal of Outram Park would be to have an open-source Rust alternative of MOOSE where Cargo
would be used as the single compiler across multiple platforms including, Windows, MacOS and Linux
(including Android). These would enable Outram Park to build user friendly, performant and reasonably
accurate graphical applications which run on all these platforms as tools for both education and research.
Such an effort, a reinvention of the wheel you might say, would be impractical, monumental and expen-
sive to do for a typical researcher in Singapore. However, with the advent of artificial intelligence and
agentic coding, this vision of Outram Park is now realisable within a reasonable timeframe.
     Agentic coding would allow the Singapore Nuclear Research and Safety Institute (SNRSI) to sub-
stantially improve its coding output and verification and Validation (V&V) efforts. This aligns closely
with the Singapore government’s AI agenda [17], where Prime Minister Lawrence Wong highlighted
the use of AI in the national budget. As part of this Agenda, there was a major push for the Infocomm
Media Development Authority to train 40,000 tech professionals to use automated AI coding systems
(agentic coding) by 2029 [18]. In alignment with this agenda, agentic coding was used to accelerate
the development of Outram Park and produce deliverables previously not possible. Of course, agentic
coding is strictly limited to open-source and non-export controlled code, where Outram Park lies.
     Readers proficient in nuclear engineering may express a healthy scepticism of the use of large lan-
guage models, and this is warranted given the hallucinations risk of AI [19]. In nuclear engineering,
where quality control and nuclear quality assurance standards (eg. NQA-1) are of utmost importance,
use of LLMs carry risks that must be mitigated [20] if they are ever used in nuclear engineering fields.
Despite these risks, the benefits of AI and LLMs are apparent and such that the Nuclear Regulatory
Commission has started considering its use [21]. Moreover, in established nuclear engineering coding
frameworks such as MOOSE, LLMs have also seen increased use such as in the MOOSE agent [22].
This is a testament to the usefulness of AI models in nuclear engineering. In fact, as of 15 Sep 2026,
OpenAI has also claimed the breakthrough solutions in the Navier–Stokes equations [23], albeit with
a fair amount of controversy generated in Sep 2026 [24]. This controversy cannot be glossed over as
it mentions that OpenAI could not rule out that de-identified product-usage data contributed to model
improvement [24]. This has given rise to concerns ” among mathematicians around how AI models
learn from interacting with their users — and whether the models, together with the developers and
researchers using them, are giving due credit to previous work.” [25]. This is a textbook case testifying
to both the rapidly evolving capabilities of AI, as well as risks pertaining to data provenance, privacy,
attribution, and academic integrity.
     The question now, is what to do with these 2026 software engineering practices and LLM tools at our
disposal given its risks and benefits. The answer is perhaps not to disregard use of AI completely, but use
it in a careful manner where AI-assisted scientific development must include a framework for structured
verification and validation (V&V), traceability and transparency, which is especially important in the
NQA-1 context [26]. Given these developments, and the overarching push to use AI models in Singapore
and the tech industry, it is therefore important to investigate the use of AI in software engineering for
nuclear engineering codes and perhaps attempt to use some of these frameworks for quality control.
     This research log details the agentic library porting and construction of various libraries in Rust,
as well as their initial V&V efforts for the Outram Park backend repository [27]. We also examine
the productivity increase from using AI agents. For this research log, we confine ourselves to thermal-
hydraulics; nuclear data and neutronics are left to a companion paper. Readers should note that this is
not meant to be a full blown thermal-hydraulics paper, its bent towards software engineering and quality
control is deliberately logged in hopes of it being useful to other software developers who may consider
using agentic LLMs.




                                                    4
2     METHODS
2.1   Origin of Discovery
The author began by purchasing his own subscription of Claude Code, initially for personal use and
paid for out of his own pocket, but with experimentation, he found that Claude Code (both via the Opus
and Sonnet) was able to translate codes from C to Rust with exceptional ease, provided there were
enough tokens. Specifically, the author is an avid guitarist and used lingot [28] for tuning his guitar.
Nevertheless, lingot development stalled, and it could not compile on Windows natively. Hence, there
was motivation to translate it to Rust. This would involve translation of Fast Fourier Transforms, signal
processing and front end GUI to Rust. The author was able to do so using Claude Code within one
weekend [29], [30] and test the tuning GUI app on real guitars. Given this exceptional capability of
Claude Code, even Sonnet, the author then had the idea to apply this methodology to Outram Park. If
agentic porting of signal processing, Fast Fourier transforms and GUI to Rust could be done in a single
weekend, this could then imply that the Rust translation required for Outram Park was actually possible.
Or at least more possible as compared to the daunting task of translation by hand. This hypothesis had to
be tested, and the results were shown in this research log. To check if such practices were documented
in literature, the author did literature searches and found similar efforts being done to translate legacy
Fortran to C++ [31]. Thus the practice of agentic ports for legacy codes was performed in peer reviewed
literature, and this gave the author additional confidence to use this in Outram Park. Once the utility of
the tool to Outram Park development had been demonstrated, the SNRSI CEO permitted the author to
claim the Claude Code subscription as a work expense. The subscription costs incurred thereafter were
therefore borne by SNRSI rather than by the author personally, though the initial exploratory period
described above was self-funded.

2.2   Outram-Foam, Rust Port of OpenFOAM
During the initial exploratory phase, the next target was the rather refractory and unwieldy OpenFOAM
library. This is because OpenFOAM could only be compiled on Linux systems with the use of a cus-
tomised bashrc file and wmake script. Such manual compilation and editing of OpenFOAM was cum-
bersome as compared to Rust, where the build systems were modernised using a simple ”cargo build
–release” command. and execution speeds were similar to C and Fortran [32]. Should the libraries be
portable, then it would avail the entire open-source solver library to Rust for use in Outram Park albeit
under the GNU GPLv3 license. This is, however, an advantage for education and research as the strongly
copyleft GPLv3 license forces code derivatives of OpenFOAM to be made open-source for students and
researchers alike. In the NQA-1 context, keeping source code open-source facilitates traceability, trans-
parency, reproducibility and auditability [33], [34], [35]. In fact, there is a philosophy that exists where
”given enough eyeballs, all bugs are shallow”. This is known as Linus’s law. It may not mean that
open-source code is completely secure, but in some cases, having more independent reviewers scruti-
nize code may lead to more bugs being discovered and patched [36]. This has helped in the context of
Linux kernel development [37], [38], where security vulnerabilities and other such defects are subject to
public scrutiny, review and correction.
    Porting OpenFOAM libraries to Rust was undertaken because the OpenFOAM library has many
useful matrix operations and finite volume method libraries which, could in theory, be used for two
phase flows, but they were impractical to humanly import over and translate to Rust. Claude Code
was then used to port and debug the open-source OpenFOAM libraries to Rust, including the many
matrix solvers, discretisation methods, fvMatrix and source files. It was proven for use in the coding
community [39] and proved to be extremely useful in porting the libraries over. In doing so, of course,
one has had to do unit testing to verify the code that was developed. For this, unit tests were imported
over from OpenFOAM as well to verify that the matrix solvers were ported over correctly. In following
naming convention of solvers based on OpenFOAM such as GeN-Foam [8] and HRMFoam [40], [41],
the Outram Park Rust fork of OpenFOAM is henceforth named Outram-Foam.


                                                     5
2.3   The role of AI in Tampines
The goal, however, was not simply to port CFD software to Rust. At the point of porting, the author had
conceived of a multi-phase version of TUAS, which was the Thermo-hydraulic Artificial-intelligence
Multi Phase INtegrated Emulator System (TAMPINES), named after the Tampines MRT station on the
east side of Singapore. TAMPINES was to simulate multi-phase flows using various models which firstly
included the Homogeneous Equilibrium Model (HEM), the simplest of multi-phase thermal hydraulics
modelling for water and steam. From thereon, there was intent to move on to drift flux modelling, and
eventually a six equation model if there was capacity. OpenFOAM solvers such as driftFluxFoam, rho-
CentralFoam and rhoPimpleFoam would have been ideal for such cases. While impractical to translate
to Rust quickly for a 1D solver, agentic porting now made this possible.
    Even with appropriate and accurate ports, this may not, in itself, be sufficient. The goal was to
use TAMPINES for real-time simulation such as in the case of the CIET Educational Simulator for
reactor modelling and secondary loop modelling for various reactors. Knowing that the equations may
not have been easy enough to solve in real-time, surrogate models and AI would have been part of the
solution. Hence, the name in TAMPINES includes A for AI. Serendipitously, it would now also imply
that TAMPINES was made with the help of agentic porting, an AI centric methodology.

2.4   Tampines Steam Tables and Critical Flow
Now, every OpenFOAM solver requires some form of thermophysical properties. Even for the HEM
model, multiphase compressible flow phenomena such as choked flow and critical heat flux models also
had to be ported. To break this problem down, thermodynamics was to be done first, and heat transfer
done later. Heat Transfer and Critical Heat Flux is the subject of future work, not in this research log.
    As for the first step, thermodynamics would have to be implemented first. The author initially hand
coded tampines-steam-tables from Wagner et al. [42] for the steam table thermodynamics. This initially
took a number of months. However, for any real two-phase thermodynamics package to be complete,
multi-phase choked flow would have to be tackled. However, multi-phase choked flow algorithms and
formulae were harder to find than for single phase. Such algorithms and problems were absent in stan-
dard thermodynamics textbooks such as Cengel [43] which only included single phase choked flow. To
the best of the author’s knowledge, no open-source library nuclear related numerical model for critical
choked flow for LOCA exists for porting. Even ThermoSysPro [44] within the OpenModelica ecosys-
tem and DWSIM were not found (with the help of Agentic AI scouring its source code) to have choked
flow correlations programmed into it. Such flow phenomena are extremely important for modelling loss
of coolant accidents and turbines. This reflects a lack of multi-phase critical choked flow code within the
open-source community. For this, tampines-steam-tables would start to fill a gap by providing the HEM
choked flow algorithms and contribute solvers to open-source code using agentic coding methodology.
For this, initial attempts were performed using human debugging, as even for a HEM model, there was a
discontinuity where the speed of sound dropped drastically between subcooled liquid and bubble point.
However, this debugging process was then accelerated and automated using Claude Opus.

2.5   Human in the Loop Agentic Porting methodology
Reduction of Bad Engineering and Hallucinated Debugging Cycles
Despite the benefits of agentic coding and porting, agentic porting of nuclear simulation software is not
a fully automated task. This is because software has to be well organised and structured to ensure re-use.
Moreover, AI agents, even the Opus models, were observed to apply the wrong method of automated
debugging and required explicit human intervention to prevent waste of time and AI tokens.
    One example is where a tampines-steam-tables function obtaining enthalpy from (p,T) for single
phase water or steam flows was called for a steam generator simulation for which multi-phase flow
was obviously expected. The function coded was specifically called ”h tp eqm single phase” which
signalled its use in single phase regions and would panic on two phase regions. Opus kept chasing these


                                                    6
crashes incorrectly, adding unnecessary guards, and exhausting the token limit. For the author who hand
coded these functions, the mistake was obvious, and he injected a prompt to ensure that Opus used (p,h)
flashes rather than (p,T) flashes because the former already contained quality data. With this correction,
Opus could then converge on the correct solution which prevented crashing.

Structuring Workflow with Claude Code and other AI tools
     Outram-Foam Translation Early experiments were conducted using the National University of
Singapore’s institutional AI platform, NUS AI Know. While suitable for conventional conversational
assistance, it proved insufficient for the requirements of large-scale software porting. At the time of
evaluation, the system accepted only limited file uploads and could not recursively inspect, modify,
execute, and iterate over a local software workspace. Consequently, repository-scale tasks required
extensive manual context management, resulting in high interaction overhead.
     In contrast, agentic coding systems such as Anthropic Claude Code were capable of operating across
an entire software repository, autonomously reading files, proposing modifications, executing tests, ob-
serving failures, and iterating on solutions. The potential of this workflow became apparent during an
early experimental project involving the translation of a guitar-tuner application into Rust. This ex-
ercise demonstrated that repository-scale translation and iterative debugging could be performed with
substantially less manual intervention than was possible using conversational interfaces alone.
     Rust was selected as the target implementation language for several practical reasons. The scien-
tific software ecosystems evaluated during this work, including OpenFOAM, OpenMC, NJOY, MOOSE,
and PFLOTRAN, employ heterogeneous build systems, compiler toolchains, dependency management
strategies, and language combinations. These include wmake, make, cmake, C++, C, and Fortran
toolchains. Reproducing legacy software environments frequently required substantial effort to resolve
compiler and dependency incompatibilities. In contrast, Rust provides a unified package-management
and build system through Cargo, reducing the operational complexity associated with multi-language
scientific software development [45]. Historically, the scientific-computing capabilities in Rust were
much less developed than in C++ or Fortran, but with today’s agentic coding capabilities, this gap can
be closed much more quickly than before.
     Experience accumulated during the project also revealed significant differences between model capa-
bilities. Claude Sonnet proved effective for localized translation tasks, individual modules, and relatively
well-bounded implementation requests. However, larger architectural tasks, complex physics models,
and new subsystem designs frequently required the more capable Claude Opus models. Claude Haiku
was generally reserved for smaller utility tasks and isolated functions. In practice, larger objectives were
typically scaffolded using Opus before being decomposed into smaller subtasks that could subsequently
be delegated to Sonnet.
     A key methodological principle was hierarchical decomposition. OpenFOAM, for example, consists
of multiple layers of abstraction, including fundamental matrix structures, fvMatrix, fvMesh, finite-
volume operators, turbulence models, thermophysical models, and application-level solvers. Rather than
attempting direct translation of entire applications, development proceeded from lower-level numerical
components toward higher-level physics modules. Matrix solvers, array libraries, ordinary differential
equation integrators, algebraic equation solvers, and polynomial root-finding utilities were translated
and verified first before more complex finite-volume infrastructure was constructed.
     Every translated component was accompanied by an explicit verification step. Following implemen-
tation, AI-generated code was subjected to a lightweight verification procedure referred to within Claude
Code as a “smoke test.” For example, when validating a linear-system solver, a matrix A and solution
vector x were chosen a priori and the right-hand-side vector computed according to

                                                 b = Ax.                                                (1)
   The translated solver was then required to recover x from A and b. Successful reconstruction within
acceptable numerical tolerances was treated as evidence that the translation was functionally correct and



                                                     7
free from obvious regressions [46]. When a translated implementation failed its smoke test, the agent
was instructed to iteratively diagnose and correct the defect until the verification case passed.
    Initial verification often employed small synthetic matrices generated during development, including
the classical 5 × 5 Hilbert matrix. However, such examples were regarded only as preliminary checks.
Final verification employed larger benchmark problems drawn from established scientific-computing
repositories. In particular, the Harwell–Boeing matrix nnc261, originating from nuclear-engineering
applications, was used as a representative sparse-matrix benchmark [47], [48]. Forward and backward
solution tests were performed using the same methodology described above. Successful recovery of the
original solution vector on both synthetic and application-derived benchmark problems was considered
a prerequisite for integrating translated numerical components into higher-level software modules.
    Within the Outram Park architecture, the OpenFOAM-derived functionality was decomposed into
multiple Rust crates. Fundamental numerical capabilities were implemented within the outram-foam-basic-lib
crate, which contained matrix structures, linear solvers, array utilities, and related numerical infras-
tructure. Turbulence modelling functionality was isolated within the outram-foam-turbulence-lib
crate, while application-level solver logic was implemented within the outram-foam-appbuilder-lib
crate. The latter contained translated solver implementations, including rhoPimpleFoam and other
application-specific finite-volume solvers.
    This decomposition strategy reduced the complexity of individual translation tasks and enabled each
layer of functionality to be verified before being used as a dependency by higher-level modules. As a
result, verification effort could be concentrated on well-defined software components prior to full solver
integration.

     Tampines Steam Tables Development of the tampines-steam-tables library began with the
implementation of the IAPWS-IF97 industrial formulation for water and steam properties [42]. The
Gibbs free-energy formulations for pressure–temperature calculations, together with the pressure–enthalpy
(ph), pressure–entropy (ps), and enthalpy–entropy (hs) formulations, were implemented directly from
the published standard. Much of the implementation work was performed manually using text-processing
workflows within Neovim. Large tabulated datasets from the standard were converted into intermediate
CSV-format representations before being translated into Rust data structures. Although repetitive, this
approach enabled the published tables to be incorporated with minimal transcription logic and preserved
traceability to the original source document.
     Verification proceeded in several stages. Initially, the implemented equations were checked against
the numerical examples provided in the IAPWS-IF97 reference documentation [42]. Subsequently,
steam-table values were transcribed and used to validate both forward and inverse thermodynamic-
property calculations. Particular attention was devoted to validating the hs formulation, whose domain
of applicability is more restricted than other regions of the standard. Saturation, superheated, and sub-
cooled steam tables were individually transcribed into Rust test fixtures and verified through automated
unit-test procedures. Verification was performed across entire tables rather than isolated points wherever
practical. Most of this work predated the adoption of Claude Code and was completed using conven-
tional manual development workflows.
     The implementation of the homogeneous-equilibrium-model (HEM) two-phase critical-flow capa-
bility presented a substantially greater challenge. Unlike the steam-table implementation, suitable open-
source reference implementations were not readily available. Existing open-source process-simulation
frameworks investigated during the project, including ThermoSysPro and other Modelica-based li-
braries, did not provide equivalent functionality suitable for direct reuse. Consequently, the imple-
mentation required both literature review and independent algorithm development.
     The original motivation for the work arose from turbine-simulation requirements within fluoride-
salt-cooled high-temperature reactor (FHR) studies. During this investigation it became apparent that
critical-flow phenomena play an important role in steam-turbine systems, particularly under high-pressure
conditions approaching sonic or supersonic flow. More importantly, two-phase critical flow is also a
fundamental phenomenon in nuclear-engineering safety analysis, particularly during loss-of-coolant ac-


                                                   8
cidents (LOCAs). As a result, the development of an open-source critical-flow capability was considered
an important prerequisite for future thermal-hydraulic modelling efforts.
     The initial development effort drew upon classical compressible-flow treatment from [43]. However,
these methods primarily address single-phase fluids and were insufficient for direct application to two-
phase steam-water systems. Validation was therefore performed against established critical-flow litera-
ture, particularly the critical-flow correlations of Moody [49] and the review of two-phase critical-flow
models by Saha [50]. Experimental and published benchmark data were digitized using GraphReader
[51] to enable quantitative comparison against the implementation.
     An important practical difficulty arose from the form in which benchmark data were reported. Pub-
lished studies generally provide stagnation properties and measured critical mass fluxes. Direct repro-
duction of these results required iterative determination of the critical pressure and critical-flow condi-
tions, creating a numerically challenging optimization problem. An alternative validation strategy was
therefore adopted. Critical mass-flux values and critical thermodynamic states were digitized directly
from published figures. Using the steam-table infrastructure already developed within TAMPINES, the
corresponding thermodynamic properties at the choke point were reconstructed. Given critical density
and mass flux, flow velocity could be calculated directly, allowing stagnation conditions to be recovered
through appropriate thermodynamic flash calculations. This substantially reduced the complexity of the
validation procedure by avoiding certain classes of nested iterative calculations.
     The forward problem remained more challenging. Starting from stagnation conditions, isentropic
pressure reduction was performed through a pressure–entropy flash calculation. At each candidate pres-
sure, local thermodynamic properties, density, and sonic velocity were determined, allowing a predicted
mass flux to be calculated. The critical mass flux was then identified through numerical maximiza-
tion. AI-assisted development tools proposed the use of golden-section search [52] to accelerate this
optimization process and reduce computational cost compared with exhaustive scanning.
     During development, significant numerical difficulties were encountered near saturation boundaries.
In particular, the sonic velocity exhibits strong discontinuities across the bubble point, transitioning from
liquid-phase values of the order of kilometres per second to substantially lower values in two-phase re-
gions. These discontinuities degraded the behaviour of the optimization algorithm and complicated
identification of the true maximum mass-flux condition. Extensive debugging was therefore required.
Diagnostic quantities, including pressure, density, sonic velocity, and predicted mass flux, were system-
atically recorded and analyzed. AI-assisted tooling proved particularly useful during this phase because
it automated generation of diagnostic output and accelerated investigation of numerical anomalies.
     Several alternative optimization strategies were subsequently explored. Separate optimization pro-
cedures were tested within and outside the two-phase dome, and the resulting predictions were compared
across a wide range of conditions. Development records and Git history indicate that much of this itera-
tive refinement occurred during the latter half of June 2026. Repeated testing and validation ultimately
yielded a stable implementation capable of reproducing the benchmark trends reported in the literature.
Quantitative validation results are presented in a later section.
     Integration studies followed, coupling the TAMPINES steam-table and critical-flow infrastructure
with the Rust implementation of rhoPimpleFoam and forming the basis of the emerging Outram-Foam
validation effort. The resulting integration tests were an important step toward applying the framework
to nuclear-engineering transient analysis.
     The principal contribution of the tampines-steam-tables project is therefore not merely the im-
plementation of steam-property calculations, but the creation of an open-source HEM-based critical-flow
capability suitable for nuclear-engineering applications. Although the HEM approximation is known to
have limitations relative to more advanced non-equilibrium models, it provides a foundation upon which
more sophisticated delayed-equilibrium, homogeneous-relaxation, and two-fluid approaches may sub-
sequently be constructed.

    Refactoring into a Rust Workspace and Monorepo As development progressed, it became de-
sirable to consolidate the previously independent software components into a single Rust workspace and


                                                     9
monorepo. Earlier versions of the software stack suffered from dependency-management challenges.
For example, different projects relied upon different versions of the uom (Units of Measurement) library,
requiring manual coordination whenever shared functionality was introduced. Such version mismatches
increased maintenance burden and complicated cross-project integration.
    AI-assisted development tools recommended migration to a Cargo workspace architecture. Under
this arrangement, multiple Rust crates share a common dependency graph, build configuration, and
version-management strategy. As a result, all workspace members automatically use consistent library
versions, substantially reducing dependency conflicts and simplifying maintenance.
    The workspace architecture also provided an opportunity to eliminate external numerical-library de-
pendencies that had previously complicated deployment. Earlier implementations relied upon OpenBLAS-
based linear algebra infrastructure, requiring platform-specific installation and configuration procedures.
This created practical difficulties on systems such as Android devices and other environments where
OpenBLAS was not readily available. Following the introduction of OpenFOAM-derived sparse and
iterative solver infrastructure, small-to-medium-sized numerical systems could instead be solved using
pure-Rust implementations.
    This capability enabled numerical infrastructure to be shared across multiple Outram Park projects.
The resulting solver implementations were used within TUAS, the TAMPINES steam-table and critical-
flow framework, and the TEH-O-PRKE reactor-kinetics package. Although the latter is outside the
scope of the present thermal-hydraulics paper, it forms part of the broader software ecosystem and is
discussed in the companion neutronics publication. The same numerical infrastructure also provides the
foundation for the rhoPimpleFoam-derived implementation used in the Edwards–O’Brien blowdown
integration studies.
    The workspace architecture significantly improved software portability. Because the resulting code-
base relied primarily upon Rust-native dependencies and Cargo-based build procedures, it could be
compiled and executed across a wide range of platforms without substantial reconfiguration. Successful
execution was demonstrated on desktop Linux systems as well as Android-based devices.
    AI-assisted development played a largely operational role during this refactoring process. Tasks such
as dependency alignment, version migration, workspace configuration, compiler-error diagnosis, and
crate integration were effectively automated. Compared with the algorithmic and physics-development
challenges described elsewhere in this work, workspace refactoring proved relatively straightforward.
The principal benefit of AI assistance was therefore a reduction in engineering effort associated with
software maintenance and ecosystem integration rather than the development of new numerical methods.

2.6   Use of AI to Track Provenance
Generative AI was also employed as a provenance-tracing and project archaeology tool. During the
development of Outram Park, a substantial amount of functionality was implemented over extended
periods of time across multiple repositories and software components. As development progressed, it
became increasingly difficult for the authors to recall the precise sequence of implementation decisions,
debugging efforts, verification activities, and feature additions solely from memory.
     AI-assisted repository analysis was therefore used to inspect Git commit histories, summarize de-
velopment timelines, identify relevant pull requests and implementation milestones, and recover histor-
ical design rationale recorded in commit messages and source-code comments. This capability proved
particularly useful when preparing the present manuscript, as it enabled previously forgotten implemen-
tation details, verification studies, and development decisions to be located rapidly and cross-referenced
against repository history.
     Rather than serving as a source of technical content, the AI acted as an interface to the project’s
historical record. Retrieved information was subsequently verified by the authors against the underlying
Git history, source code, commit metadata, benchmark results, and documentation before being incorpo-
rated into the manuscript. This workflow enabled specific implementation details, verification activities,
and development milestones to be documented with greater accuracy than would have been possible
using author recollection alone.

                                                   10
    The use of AI-assisted provenance tracing also reduced the cognitive burden associated with navi-
gating large software repositories. Instead of manually inspecting extensive commit histories and source
trees, the authors were able to query implementation history at a higher semantic level, allowing greater
effort to be directed toward scientific interpretation, verification activities, and manuscript preparation.

2.7     Reduction of Cognitive Load in Prose Writing and Prompt Engineering
A secondary use of generative AI within the project was the refinement of informal technical notes into
publication-ready academic prose. During development, the primary author frequently recorded imple-
mentation rationale, debugging observations, verification results, and design decisions in abbreviated
engineering prose rather than directly composing journal-style text. This approach was adopted to re-
duce the cognitive overhead associated with first-draft composition and to allow technical ideas to be
captured rapidly while attention remained focused on software development and scientific reasoning.
    For example, prose describing the translation and verification of OpenFOAM numerical infrastruc-
ture was initially recorded as informal Singlish (an English-based creole spoken in Singapore [53])
engineering text (in LATEX format) and subsequently transformed into structured academic prose using
AI-assisted language revision. The transformation was restricted to language, organization, and read-
ability. Technical content, verification procedures, numerical results, interpretations, and conclusions
remained author-generated. The refined text was then reviewed by the authors to ensure technical equiv-
alence with the original notes.
    This was the original text, which was then translated into proper journal language:

      Author’s original note (verbatim LaTeX source code, informal Singlish)

       OpenFOAM right, for example, got matrices, fvMatrix, fvmesh etc etc.
      The idea right is to break it down. First the basics, got matrix solvers,
      arrays, ODEs, algebraic solver, quadratic and cubic equation solver.
      Quite basic lah. Ask Claude translate and test first. And make sure right,
      every time translation comes, there should be some sanity check. Claude
      calls it a smoke test lah. So for example, for solving Ax=b matrix,
      we can determine A and x, then calculate b. Then we try to back calculate
      x using the solver. if can hor, then okay lah. swee liao, solver verified.
      \cite{higham2002accuracy}
      If not, ask claude keep debugging until swee swee.


      Ahh this one lah. nnc261 \cite{duff1989sparse}.

      https://math.nist.gov/MatrixMarket/data/Harwell-Boeing/nucl/nnc261.html

      Claude made smaller test like the hilbert 5x5 matrix. I mannaully do the
      nnc261. The forward backward test. Once that one done, ho seh liao.


    Typing this less verbose form out and having it translated into proper academic text was valuable in
reducing cognitive load for the author. This was because the author was more comfortable expressing
ideas in Singlish, his colloquial native tongue, than English.
    This workflow was particularly valuable during large-scale agentic porting activities, as well as prose
writing, where implementation progress frequently outpaced the ability to document design decisions
and prose in formal publication style. By separating technical idea capture from language refinement,
cognitive resources could be directed toward numerical verification, software architecture, and scientific
interpretation rather than grammatical editing and prose construction. Such practices used and described


                                                    11
in reputable literature [54] (Nature Biomedical engineering), were indeed valuable to the author’s inter-
action with AI and the writing of prose from LATEX based Singlish prose to English. This technique
should be useful for Singaporeans more accustomed to expressing ideas in colloquial language rather
than English, but could also be useful for those writing ideas in any colloquial language and converting
it to English suitable for a journal article.
     The use of AI for language refinement is consistent with contemporary publisher guidance permitting
generative AI tools to assist with organization, readability, and manuscript preparation, provided that
human authors retain responsibility for the scientific content, verify all outputs, and disclose their use
appropriately.
     Annals of Nuclear Energy states [55]:

      Annals of Nuclear Energy, Guide for Authors

      Authors preparing a manuscript for this journal may use AI tools to support them. However, these
      tools must never be used as a substitute for human critical thinking, expertise and evaluation. AI
      tools may only be applied with human oversight and control.
      Please read Elsevier’s detailed author policy on the use of AI tools, as stated in Elsevier’s gener-
      ative AI policies for journals.

      Elsevier explicitly states [56]:

      Elsevier, Generative AI Policies for Journals

      Increasingly, these tools, including AI agents and deep research tools, are helping researchers
      to synthesize complex literature, provide an overview of a field or research question, identify
      research gaps, generate ideas and provide tailored support for tasks such as content organization
      and improving language and readability. Authors preparing a manuscript for an Elsevier journal
      can use AI tools to support them in these tasks. However, these tools must never be used as a
      substitute for human critical thinking, expertise and evaluation.
      AI tools may be used to support the creation of data visualizations only when the visual output is
      directly derived from underlying data.

    The authors reviewed all AI-assisted revisions and retained full responsibility for the technical ac-
curacy and conclusions presented in the manuscript.

2.8     Verification and Validation (V&V)
Verification and validation are particularly important for AI-assisted software development. Large lan-
guage models are known to generate plausible but incorrect outputs, a phenomenon commonly referred
to as hallucination [57]. Consequently, code that compiles successfully cannot automatically be assumed
to be correct. The same principle applies to conventionally developed scientific software: implementa-
tion correctness and physical validity must be demonstrated through systematic testing before software
can be regarded as trustworthy [58]. Within the Outram Park ecosystem, all software components are
regarded as experimental until they have successfully passed an appropriate verification and validation
procedure.
    The V&V workflow employed throughout this work combined AI-assisted automation with manda-
tory human review. Benchmark data were first extracted from published figures using GraphReader
[51]. The resulting datasets were exported into CSV format for subsequent use within the verification
workflow.
    Verification tests were then implemented in Rust and executed using:

cargo test --release



                                                      12
    The generated output was manually inspected by the authors to determine whether the implemented
functionality behaved as expected. When anomalies were observed, additional diagnostics were added
and the tests were repeated until the behaviour of the implementation was understood.
    Verification outputs were written to CSV files within a Git-ignored verification-and-validation direc-
tory. These files could then be re-ingested into AI tools, including Claude Code, Microsoft Enterprise
Copilot, and NUS AI Know, for post-processing. Typical tasks included automatic generation of Python
matplotlib plotting scripts, LATEX pgfplotstable tables, and visualization code. The resulting figures
and tables were reviewed by the authors before being incorporated into the manuscript.
    This workflow substantially reduced the effort required to transform raw verification output into
publication-quality figures and tables while retaining human oversight of benchmark selection, numeri-
cal verification, result interpretation, and scientific conclusions.
    The workflow described above was intended primarily as a productivity mechanism rather than as a
complete substitute for conventional verification practice. In its current form, the workflow provides a
substantial level of confidence in implementation correctness by combining automated test generation,
benchmark comparisons, numerical inspection, and human review.
    For applications requiring a higher degree of assurance, authors may elect to independently derive
and implement verification tests without AI assistance. The resulting manually derived reference solu-
tions can then be compared against AI-generated implementations and against the CSV-based validation
workflow described above. Such independent cross-checking provides an additional layer of verifica-
tion by reducing the possibility that errors in AI-generated code and AI-generated test logic remain
undetected.
    Although this final verification step was not systematically applied to all case studies reported in
the present work, the workflow adopted here was generally sufficient to identify the majority of im-
plementation and translation errors encountered during development. The authors therefore regard the
AI-assisted workflow as an effective first-pass verification strategy, while recognising that independently
derived validation tests remain the preferred standard when the highest degree of confidence is required.

2.9   Use of Agents and Subagents in Claude Code Max
This work made extensive use of the multi-agent capabilities available within Claude Code Max [59].
The larger token allocation and extended usage limits permitted the simultaneous execution of multiple
agent and subagent workflows across different repositories and development tasks.
    A recurring pattern throughout the project was the decomposition of large software-porting objec-
tives into multiple parallel activities. Rather than translating a single repository sequentially, separate
agents were assigned to independent numerical, thermophysical, and software-engineering tasks. This
enabled concurrent development across multiple projects, including ports and reimplementations related
to OpenMC, NJOY, OpenFOAM-derived infrastructure, and associated Outram Park components.
    The multi-agent workflow proved particularly useful for repository-scale translation tasks. Individ-
ual agents could be assigned responsibility for understanding source-code structure, generating Rust
implementations, performing verification tests, resolving compiler errors, and preparing documentation.
Higher-level coordinating agents were then used to review and integrate the outputs of these subordinate
agents into a unified codebase.
    Practical experience revealed that model capabilities were not uniform. Large architectural and
repository-wide tasks generally benefited from more capable models, while localized refactoring and
implementation work could often be delegated to smaller models. As a result, agentic development
frequently adopted a hierarchical structure, in which a higher-level model generated implementation
plans and task decomposition strategies before dispatching narrower subtasks to subordinate agents.
    The principal advantage of this approach was increased throughput. Multiple repositories and soft-
ware components could be developed, reviewed, and validated concurrently rather than sequentially.
In practice, this significantly accelerated progress on projects spanning multiple physics domains and
software stacks.



                                                    13
     However, increased development throughput also introduced new human factors considerations. Al-
though agent fleets reduced the effort associated with implementation, they increased the monitoring
burden on the human developer. Simultaneous review of multiple streams of code generation, verifi-
cation output, debugging reports, and scientific results introduced substantial cognitive demands. Con-
sequently, the limiting factor in development frequently became human review capacity rather than
code-generation speed.
     The authors therefore regard multi-agent development as a powerful productivity mechanism when
combined with rigorous human oversight, verification, and validation. While agent fleets can substan-
tially increase software-development throughput, scientific responsibility remains with the human de-
veloper, who must review implementation choices, validate numerical results, and assess the physical
correctness of generated code.


3     Results
3.1   Speed Increase by Agentic Porting
One of the most striking observations arising from this work was the development velocity enabled by
agentic software-development workflows. The combination of repository-scale code understanding, au-
tomated compiler-error resolution, dependency management, code generation, testing, and iterative de-
bugging substantially reduced the engineering effort required to construct new scientific software com-
ponents. Tasks that would traditionally require extensive manual investigation and software-engineering
effort, particularly language-porting activities and dependency management across heterogeneous code
bases, could often be completed significantly more rapidly through AI-assisted workflows.
    Historically, software efforts of comparable breadth would often require multiple developers work-
ing over extended periods of time. In contrast, the Outram Park project demonstrated that a single
researcher (or two), supported by agentic development tools, could make meaningful progress across
multiple domains including computational fluid dynamics, thermophysical property modelling, reactor
kinetics, nuclear-data processing, Monte Carlo transport, process-system simulation, and digital-twin
infrastructure within a relatively short period.
    An additional observation was that development throughput increased further following adoption of
Claude Code Max in mid-July 2026. Larger context windows, increased token availability, and multi-
agent execution capabilities enabled multiple repositories and software components to be developed
concurrently rather than sequentially. Consequently, productivity became increasingly limited by human
review, verification, and scientific judgement rather than by code-generation capacity itself.
    The cumulative effect of these development activities is summarized in Table I. Over approximately
four weeks, substantial progress was achieved across the Outram Park ecosystem, ranging from finite-
volume infrastructure and thermophysical property libraries to nuclear-data processing, Monte Carlo
transport, reactor kinetics, and digital-twin foundations. Although only the thermal-hydraulics-related
developments are discussed in detail in the present paper, the timeline provides context for the broader
software ecosystem that emerged during the same development period.




                                                  14
Table I: Development milestones of Outram Park, 19 June – 16 July 2026. Roughly four weeks of
agentic-AI-assisted development (Claude Code) delivered substantial productivity gains over conven-
tional scientific software engineering workflows. All commit hashes and full messages are publicly
available in the project repository under the develop branch. Items marked in progress are not yet vali-
dated; see the per-crate verification and validation/ records for validation status.

 Date             Milestone                                                   Cumulative capability
 19 Jun           Active development begins                                   Baseline: prior tuas, teh-o-prke
 23–24 Jun        outram-foam-basic-lib v0.1.2–v0.1.5                         FV operators, thermophysics, matrix
                                                                              solvers
 25 Jun           outram-foam-appbuilder-lib scaffolded                       rhoCentralFoam, rhoPimpleFoam
                                                                              skeletons
 26 Jun           Ghia benchmark; MUSCL + k-ω SST added                       Ghia cavity 1.9% L∞a ; Sod L1 3.7%
 26 Jun           vanLeer MUSCL reconstruction                                rhoCentralFoam Sod L1 → 0.7%
 28 Jun           njoy-outram-park-fork scaffolded                            ENDF tape reader; RECONR Phase 1
 28 Jun           RECONR Phase 2b SLBW/MLBW                                   U-235 thermal cross sections validated
 2 Jul            WMP + fast MGXS baked (ENDF/B-VIII.0)                       Offline nuclear-data blob (4.7 MB)
 3 Jul            First end-to-end Godiva keff                                keff = 1.129 (+12852 pcm), coupled
                                                                              physics live
 3 Jul            Anisotropic elastic scatter (MF=4)                          Godiva HIGH keff = 0.996 (−373 pcm)
 3–4 Jul          MF=5 fission spectrum χ(E); HEATR H1–H7                     Full continuous-energy transport physics
 6 Jul            Sod shock tube validation documented                        LaTeX-ready V&V infrastructure
 7 Jul            U-238 capture wing pedestal fix                             RRR L1 vs OpenMC: 0.30 → 0.0007
                                                                              (400×)
 7 Jul            Godiva HIGH-fidelity V&V document                           keff = 1.00094 ± 0.00198 (+94 pcm)
 8 Jul            CoolProp fork: 137-fluid coverage                           Helmholtz EOS + transport + VLE
 10 Jul           CoolProp: HumidAir, incompressibles, mixtures               126 incompressibles + 840 binary pairs;
                  (codegen)                                                   V&V scaffold across 13 crates
 13 Jul           DWSIM balance-of-plant ports + tampines crate               Valve/HX/pump/expander, pipe
                                                                              correlations; digital-twin GUI scaffold
 13 Jul           Real IAPWS-IF97 (p, h) flash in correct                     Two-phase-safe array thermodynamics
                  thermo
 14 Jul           Nordheim–Fuchs prompt-excursion kinetics                    teh-o-prke → nee soon → digital twin;
                                                                              909 tests pass
 14 Jul           Two-phase boiling unblocked; OpenFOAM                       Boiling stable; V&V log + student
                  pressure bounding                                           teaching doc
 15 Jul           outram-mc Monte Carlo transport (CSG + surface              Thermal LWR pincell k∞ = 1.398
                  tracking)                                                   (OpenMC comparison in progress)
 15 Jul           TRISO random packing + delta-tracking;                      Doubly-heterogeneous k∞ ; burnup driver;
                  depletion (CRAM)                                            HexLattice
 15 Jul           GeN-Foam multiphysics port begun                            In progress: single-phase TH core
                  (SP3/SN /multiRegion)                                       pending
 16 Jul           First crates.io release prep                                coolprop 0.1.0 (GPL-3.0), tuas 0.1.4,
                                                                              tampines 0.2.2, outram-foam
 16 Jul           Current tip                                                 Multi-physics suite; validation ongoing

a This row records the cavity result as it stood on 26 June 2026, obtained on a single refined mesh. The three-mesh

grid-convergence study reported in Section 3.2.2 — which adds the 80 × 80 mesh and the observed order of accuracy,
Tables V and VI — was performed on 17 September 2026 and therefore postdates this table’s 19 June – 16 July window. It is
reported here because it re-measures work described in this table, not because it belongs to it. Note also that the MUSCL
reconstruction named in this row was added to rhoCentralFoam (next row) and is not used by the cavity case, whose
convection scheme is first-order upwind throughout.




                                                             15
     3.2     Outram-Foam Verification and Validation
     As discussed previously, Outram-Foam is a Rust implementation derived from the numerical meth-
     ods and software architecture of OpenFOAM. However, because Outram-Foam is a newly developed
     codebase, systematic verification and validation activities were necessary to establish confidence in the
     correctness of its implementation.
         The verification strategy adopted in this work proceeded in several stages. First, the underlying
     matrix and linear-algebra libraries were verified using established benchmark problems. Second, code-
     to-code verification was performed against OpenFOAM using the classical lid-driven cavity benchmark.
     Finally, validation against the published reference solution of Ghia et al.[60] was carried out, including
     a mesh-refinement study to assess discretization error and solution convergence.

     3.2.1    Matrix Libraries
     The first verification exercise focused on the matrix and linear-algebra infrastructure that forms the nu-
     merical foundation of Outram-Foam. For this purpose, the Harwell–Boeing benchmark matrix nnc261
     was obtained from the Matrix Market repository [47], [48]. A method of manufactured solutions was
     employed, in which a known reference solution vector was first prescribed and subsequently used to
     generate the corresponding right-hand-side vector. The solver was then required to recover the original
     solution vector from the resulting linear system.
         The resulting verification test is shown here:
 1   #[test]
 2   fn nnc261_lu_roundtrip() {
 3       let mtx_path = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
 4           .join("tests").join("nnc261.mtx");
 5       let contents = std::fs::read_to_string(&mtx_path)
 6           .expect("could not read tests/nnc261.mtx");
 7
 8         let a = load_matrix_market(&contents);
 9         assert_eq!(a.n(), 261, "expected a 261x261 matrix");
10
11         // Manufactured reference solution: x_ref[i] = i + 1 (1, 2, ..., 261)
12         let n = a.n();
13         let x_ref: Vec<f64> = (1..=n).map(|i| i as f64).collect();
14
15         // Forward pass: b = A * x_ref
16         let b = mat_vec(&a, &x_ref);
17
18         // Solve A * x = b
19         let x_solved = a.solve(&b).expect("NNC261 must be non-singular");
20
21         // Check 1 (primary): relative residual ||A*x - b||_inf / ||b||_inf < 1e-10
22         let ax = mat_vec(&a, &x_solved);
23         let residual: Vec<f64> = ax.iter().zip(b.iter())
24             .map(|(a, b)| a - b).collect();
25         let rel_residual = norm_inf(&residual) / norm_inf(&b);
26         assert!(rel_residual < 1e-10,
27             "relative residual {rel_residual:.3e} exceeds 1e-10");
28
29         // Check 2 (secondary): relative solution error
30         // ||x - x_ref||_inf / ||x_ref||_inf < 0.05
31         let err: Vec<f64> = x_solved.iter().zip(x_ref.iter())
32             .map(|(a, b)| a - b).collect();
33         let rel_err = norm_inf(&err) / norm_inf(&x_ref);
34         assert!(rel_err < 0.05,
35             "relative solution error {rel_err:.3e} exceeds 0.05");
36   }




                                                        16
Listing 1: Verification test for the dense LU solver (SquareMatrix::solve, Crout LU with scaled
partial pivoting) against the NNC261 Harwell–Boeing matrix, using the method of manufactured
solutions.

    Residuals for the iterative calculations were evaluated using two separate criteria.
    The first criterion was the relative residual, which measures the extent to which the computed so-
lution satisfies the original linear system. Using the infinity norm,1 the relative residual was calculated
as

                                                          ∥Ax − b∥∞
                                                 rrel =             .                                  (2)
                                                            ∥b∥∞
    This quantity represents the normalized discrepancy between the computed right-hand side Ax and
the prescribed vector b. A value close to zero indicates that the numerical solution satisfies the linear
system to high accuracy.
    The second criterion was the relative solution error. Unlike the residual, which measures how well
the equations are satisfied, the relative solution error directly compares the recovered solution vector
against a known reference solution,

                                                          ∥x − xref ∥∞
                                                 erel =                .                               (3)
                                                            ∥xref ∥∞
    For the nnc261 benchmark, the measured solution error was

                                                erel = 1.184 × 10−2 ,                                  (4)
     corresponding to approximately 1.18% relative error. Although this may initially appear large com-
pared with the residual, the benchmark matrix is highly ill-conditioned (κ ≈ 1013 ). The observed error
therefore remains consistent with expected numerical behaviour for such a challenging test problem and
lies comfortably within the prescribed acceptance criterion of 5%.
     Having demonstrated satisfactory performance on the initial benchmark problems, the author pro-
ceeded to more challenging verification and validation studies.

3.2.2   Cavity Case
The lid-driven cavity problem was selected as the next verification exercise. This benchmark is one of
the most widely used validation cases within the OpenFOAM community and is distributed as part of the
official OpenFOAM tutorial suite [61]. As a consequence, it provides a convenient and well-understood
baseline for assessing the correctness of finite-volume implementations.
    The reference cavity case was first executed using OpenFOAM. The resulting mesh (polyMesh),
boundary conditions, controlDict, and velocity-field data were retained as reference information.
The same case was subsequently executed using Outram-Foam’s pimpleFoam solver.
    To enable a direct comparison, Outram-Foam’s pimpleFoam solver was configured to operate in
a PISO-like mode equivalent to that of OpenFOAM’s icoFoam. Under these conditions, differences
between the two solutions can be attributed primarily to implementation details rather than differences
in solution methodology.
    Centerline velocity profiles were then compared between OpenFOAM icoFoam and Outram-Foam’s
pimpleFoam. Following this code-to-code verification step, comparison with the benchmark data of
Ghia et al.[60] was also performed. Benchmarking against peer-reviewed literature was considered
preferable to solely comparing against another software implementation, since agreement with published
benchmark data provides stronger evidence of correctness.
  1 The infinity norm is defined as the maximum absolute value among all components of a vector.




                                                           17
     The benchmark data reported by Ghia et al.[60] were manually reviewed and verified before use. Ini-
tial comparison suggested that further improvement might be obtained through mesh refinement. Con-
sequently, a mesh-refinement study was also conducted in order to assess the influence of discretization
error on the solution.
     The resulting comparison between OpenFOAM icoFoam and Outram-Foam’s pimpleFoam is shown
below. Excellent agreement was observed between the two solvers, indicating that the finite-volume op-
erators, pressure–velocity coupling procedures, and associated numerical infrastructure were translated
correctly. The detailed data are provided to facilitate independent reproduction of the verification exer-
cise.
     The agreement between OpenFOAM icoFoam and Outram-Foam’s pimpleFoam was excellent, as
evidenced by the small residual differences reported in Table II.

Table II: Comparison of dimensionless x-velocity ux along the vertical centerline (y/L) between the
Outram-Foam’s pimpleFoam and OpenFOAM’s icoFoam reference.

                             y/L         uRust
                                          x          uicoFoam
                                                      x             |∆ux |
                            0.0250    −0.017 70    −0.017 68     2.00 × 10−5
                            0.0750    −0.046 09    −0.046 09     0.00
                            0.1250    −0.070 24    −0.070 35     1.10 × 10−4
                            0.1750    −0.091 94    −0.092 22     2.80 × 10−4
                            0.2250    −0.112 22    −0.112 75     5.30 × 10−4
                            0.2750    −0.131 65    −0.132 50     8.50 × 10−4
                            0.3250    −0.150 33    −0.151 55     1.22 × 10−3
                            0.3750    −0.167 83    −0.169 47     1.64 × 10−3
                            0.4250    −0.183 17    −0.185 23     2.06 × 10−3
                            0.4750    −0.194 68    −0.197 13     2.45 × 10−3
                            0.5250    −0.199 91    −0.202 61     2.70 × 10−3
                            0.5750    −0.195 46    −0.198 18     2.72 × 10−3
                            0.6250    −0.176 89    −0.179 30     2.41 × 10−3
                            0.6750    −0.138 69    −0.140 35     1.66 × 10−3
                            0.7250    −0.074 39    −0.074 79     4.00 × 10−4
                            0.7750     0.023 03     0.024 42     1.39 × 10−3
                            0.8250     0.160 35     0.164 00     3.65 × 10−3
                            0.8750     0.343 40     0.348 92     5.52 × 10−3
                            0.9250     0.574 70     0.580 34     5.64 × 10−3
                            0.9750     0.849 23     0.852 02     2.79 × 10−3




                                                   18
                                          icoFoam from OpenFOAM
                        0.8
                                          pimpleFoam from Outram-Foam
                        0.6

                        0.4
    ux




                        0.2

                         0

                  −0.2
                                  ·10−3
                         2
           − uicoFoam




                         0
              x




                        −2
     uRust




                        −4
      x




                        −6
                              0       0.1      0.2   0.3   0.4    0.5   0.6   0.7   0.8   0.9   1
                                                                  y/L
     The agreement between Outram-Foam’s pimpleFoam and the benchmark data of Ghia et al. [60] is
also encouraging, as evidenced by the relatively small discrepancies reported in Table III.
     Following successful code-to-code verification against OpenFOAM, comparison against the bench-
mark data of Ghia et al. [60] was performed. This recommendation initially arose from the AI-assisted
workflow. The suggestion was accepted because comparison against peer-reviewed benchmark data
provides stronger validation than agreement with a single software implementation alone. While code-
to-code verification establishes consistency with OpenFOAM, agreement with benchmark data from the
literature provides additional confidence that the solver is correctly reproducing the underlying physics.
     The benchmark values were obtained from Table I of Ghia et al. [60] for the lid-driven cavity problem
at a Reynolds number of Re = 100. The benchmark data were manually reviewed against the original
publication prior to their use in the validation study.
     The resulting comparison between Ghia et al. and Outram-Foam’s pimpleFoam is presented in Ta-
ble III.




                                                                 19
Table III: Validation of the Rust port against the Ghia et al. (1982) lid-driven cavity benchmark: x-
velocity ux along the vertical centerline (y/L) at Re = 100.

                                y/L         uGhia
                                             x            uRust
                                                           x          |∆ux |
                               0.0000     0.000 00      0.000 00    0.000 00
                               0.0547    −0.037 17     −0.033 48    0.003 69
                               0.0625    −0.041 92     −0.037 75    0.004 17
                               0.0703    −0.047 75     −0.042 01    0.005 74
                               0.1016    −0.064 34     −0.056 78    0.007 56
                               0.1719    −0.101 50     −0.086 52    0.014 98
                               0.2813    −0.156 62     −0.125 66    0.030 96
                               0.4531    −0.210 90     −0.165 10    0.045 80
                               0.5000    −0.205 81     −0.165 20    0.040 61
                               0.6172    −0.136 41     −0.128 85    0.007 56
                               0.7344     0.003 32     −0.022 15    0.025 47
                               0.8516     0.231 51      0.192 53    0.038 98
                               0.9531     0.687 17      0.628 02    0.059 15
                               0.9609     0.737 22      0.676 34    0.060 88
                               0.9688     0.788 71      0.725 29    0.063 42
                               0.9766     0.841 23      0.778 83    0.062 40
                               1.0000     1.000 00      1.000 00    0.000 00
                                                      Max |∆ux |     0.063 42
                                                     Mean |∆ux |     0.027 73
                                                     RMS |∆ux |      0.036 30

     An initial comparison against the benchmark data of Ghia et al. [60] was performed using a relatively
coarse 20 × 20 computational mesh.
     At this stage, the observed discrepancies were not unexpected because the mesh resolution was
relatively low. The maximum pointwise error was approximately 6.3% of the lid velocity, with the
largest deviations occurring in regions of strong velocity gradients near the moving lid.
     It is important to state what discretization produced that figure, because it sets the accuracy that
can be expected. Convection in Outram-Foam’s pimpleFoam is assembled with first-order upwind
differencing (DivScheme::GaussUpwind, the solver default), while the Laplacian is second order. The
formal spatial order of the cavity solution is therefore one, not two, and the gap to Ghia et al. on a coarse
mesh is dominated by first-order numerical diffusion. Ghia et al. themselves used a 129 × 129 grid. A
6.3% maximum deviation is thus the expected behaviour of this scheme at this resolution rather than
an indication of an implementation defect — a proposition that the grid-convergence study below tests
directly.
     Following inspection of the validation results, a mesh-refinement study was undertaken to quantify
the effect of spatial resolution on solution accuracy. Two grids can only show that the error became
smaller; they cannot establish an observed order of accuracy. A third grid was therefore added, giving
the sequence 20 × 20, 40 × 40 and 80 × 80 at a constant refinement ratio r = 2.
     All three meshes are generated from the same blockMeshDict with only the cell count substituted,
so they are identical in geometry, patch naming and patch type, and all three have an even cell count so
that the centerline sampling is performed identically on each. This matters: the sampling line x = L/2
falls between two columns of cell centres on an even mesh and exactly on a column on an odd one, so a
sequence mixing the two would place a different sampling error on different members of it and corrupt
the measured order.
     The per-station results are given in Tables IV and V, and the convergence quantities derived from
them in Table VI.


                                                     20
Table IV: Validation of the Rust port against the Ghia et al. (1982) lid-driven cavity benchmark at
Re = 100 on the refined mesh: x-velocity ux along the vertical centerline (y/L).

                              y/L        uGhia
                                          x             uRust
                                                         x        |∆ux |
                             0.0000     0.000 00     0.000 00    0.000 00
                             0.0547    −0.037 17    −0.036 69    0.000 48
                             0.0625    −0.041 92    −0.041 42    0.000 50
                             0.0703    −0.047 75    −0.045 76    0.001 99
                             0.1016    −0.064 34    −0.062 65    0.001 69
                             0.1719    −0.101 50    −0.096 54    0.004 96
                             0.2813    −0.156 62    −0.143 59    0.013 03
                             0.4531    −0.210 90    −0.190 58    0.020 32
                             0.5000    −0.205 81    −0.188 83    0.016 98
                             0.6172    −0.136 41    −0.137 81    0.001 40
                             0.7344     0.003 32    −0.013 37    0.016 69
                             0.8516     0.231 51     0.214 28    0.017 23
                             0.9531     0.687 17     0.669 85    0.017 32
                             0.9609     0.737 22     0.719 30    0.017 92
                             0.9688     0.788 71     0.774 33    0.014 38
                             0.9766     0.841 23     0.829 90    0.011 33
                             1.0000     1.000 00     1.000 00    0.000 00
                                                   Max |∆ux |    0.020 32
                                                   RMS |∆ux |    0.011 97


Table V: Validation of the Rust port against the Ghia et al. (1982) lid-driven cavity benchmark at Re =
100 on the finest (80 × 80) mesh: x-velocity ux along the vertical centerline (y/L).

                              y/L        uGhia
                                          x             uRust
                                                         x        |∆ux |
                             0.0000     0.000 00     0.000 00    0.000 00
                             0.0547    −0.037 17    −0.037 30    0.000 13
                             0.0625    −0.041 92    −0.041 98    0.000 06
                             0.0703    −0.047 75    −0.046 59    0.001 16
                             0.1016    −0.064 34    −0.064 04    0.000 30
                             0.1719    −0.101 50    −0.099 73    0.001 77
                             0.2813    −0.156 62    −0.151 01    0.005 61
                             0.4531    −0.210 90    −0.202 29    0.008 61
                             0.5000    −0.205 81    −0.199 16    0.006 65
                             0.6172    −0.136 41    −0.139 10    0.002 69
                             0.7344     0.003 32    −0.005 36    0.008 68
                             0.8516     0.231 51     0.225 60    0.005 91
                             0.9531     0.687 17     0.681 85    0.005 32
                             0.9609     0.737 22     0.732 28    0.004 94
                             0.9688     0.788 71     0.784 55    0.004 16
                             0.9766     0.841 23     0.838 11    0.003 12
                             1.0000     1.000 00     1.000 00    0.000 00
                                                   Max |∆ux |    0.008 68
                                                   RMS |∆ux |    0.004 55




                                                   21
Table VI: Grid-convergence quantities for the lid-driven cavity at Re = 100, derived from the three
meshes above at a constant refinement ratio r = 2. The functional is ux /Ulid interpolated at the fixed
station y/L = 0.4531, Ghia’s tabulated point nearest the recirculation peak and the location of the largest
coarse-mesh error. The observed order is p = ln(| f1 − f2 |/| f2 − f3 |)/ ln r; Richardson extrapolation is
fh→0 = f3 + ( f3 − f2 )/(r p − 1); and GCI23 = Fs |( f3 − f2 )/ f3 |/(r p − 1) with Fs = 1.25.

                            Quantity                                                                   Value
                            f1 , 20 × 20 (∆x = 5.00 × 10−3 m)                                      −0.165103
                            f2 , 40 × 40 (∆x = 2.50 × 10−3 m)                                      −0.190580
                            f3 , 80 × 80 (∆x = 1.25 × 10−3 m)                                      −0.202290
                            Observed order of accuracy p                                                1.121
                            Richardson extrapolation fh→0                                           −0.21225
                            Ghia et al. (1982) at the same station                                  −0.21090
                            Difference, extrapolated vs. benchmark                                     0.64 %
                            GCI23 (Fs = 1.25)                                                          6.16 %
                            RMS |∆ux | vs. Ghia, 20 → 40 → 80                    0.03630 → 0.01197 → 0.00455
                            Trend in the benchmark error, log2 (ei /ei+1 )                       1.600, 1.396


    Each refinement reduces the maximum pointwise error: 6.3% of the lid velocity on 20 × 20, 2.0%
on 40 × 40 and 0.87% on 80 × 80. Increasing agreement is therefore achieved with the lid-driven cavity
flow of Ghia et al. [60], and the rate at which it is achieved is quantified below.

                    1              Ghia et al. (1982)
                                   Outram-Foam, 20 × 20
                                   Outram-Foam, 40 × 40
                                   Outram-Foam, 80 × 80
                  0.5
             ux




                    0



                 10−1
                                  20 × 20
                                  40 × 40
                 10−2
                                  80 × 80
        |∆ux |




                 10−3


                 10−4
                        0        0.1        0.2      0.3        0.4        0.5       0.6     0.7      0.8       0.9   1
                                                                           y/L

Figure 2: Grid convergence of the Rust port against the Ghia et al. (1982) lid-driven cavity benchmark
at Re = 100, on the three-mesh sequence 20 × 20, 40 × 40, 80 × 80 (r = 2). Top: ux profiles along the
vertical centerline; each refinement tracks the benchmark more closely, most visibly in the shear layer
near y/L ≈ 1 and at the recirculation peak near y/L ≈ 0.45. Bottom: pointwise absolute error (log scale).
RMS error over the 17 stations falls 0.0363 → 0.0120 → 0.0046.




                                                                      22
                                                  measured
                                     10−1.5       slope 1 (first order)
                                                  slope 2 (second order)


               RMS |∆ux | vs. Ghia
                                      10−2




                                     10−2.5


                                              10−2.9   10−2.8   10−2.7 10−2.6 10−2.5   10−2.4   10−2.3
                                                                   cell width ∆x [m]

Figure 3: Convergence of the centerline RMS error against cell width, with first- and second-order
reference slopes anchored at the coarsest mesh. The measured points sit between the two references,
which is the expected signature of a scheme combining first-order upwind convection with a second-
order Laplacian. The verification order obtained by Richardson extrapolation of the solution itself is
p = 1.121 (Table VI); the steeper apparent slope of the benchmark error — log2 (ei /ei+1 ) of 1.600 and
1.396 — includes Ghia’s own discretization error and is not an order of accuracy.

     Figure 2 shows that each refinement improves agreement with the benchmark solution of Ghia et
al. [60]. The maximum pointwise error falls from 6.3% of the lid velocity on the 20 × 20 mesh to 2.0%
on 40 × 40 and 0.87% on 80 × 80, and the centerline RMS error from 0.0363 to 0.0120 to 0.0046.
     That the error decreases is necessary but not sufficient: it shows only that the discretization is doing
something sensible, not that it is converging at the rate the scheme should deliver, nor that it is converging
to the right answer. The three-mesh sequence permits both to be measured, and Table VI reports them.
     The observed order of accuracy, obtained by Richardson extrapolation of the centerline velocity at
y/L = 0.4531, is p = 1.121. This is the verification result, and it sits essentially on the formal first
order of the upwind convection scheme in use. Richardson extrapolation of the same sequence gives
ux /Ulid = −0.21225 as ∆x → 0, against Ghia et al.’s tabulated −0.21090 at that station — a difference of
0.64%. The discretization therefore converges at its formal rate, and converges to the benchmark value
rather than merely to some grid-independent value of its own. The fine-grid convergence index on the
40 → 80 pair is GCI23 = 6.16%, which is the uncertainty that should be attached to the 80 × 80 result.
     One distinction is worth drawing explicitly, because conflating the two overstates the result. The
trend in the error against Ghia et al. is steeper than the order of accuracy: log2 (ei /ei+1 ) gives 1.600 for
20 → 40 and 1.396 for 40 → 80. Those figures include Ghia et al.’s own discretization error and the fact
that the benchmark error is not a clean power law, and they are reported here as a validation trend only.
The order of accuracy of this implementation is the 1.121 obtained from the solution sequence itself, not
the 1.4–1.6 obtained from the benchmark comparison.
     Taken together, these results are consistent with Outram-Foam’s pimpleFoam correctly reproduc-
ing the classical lid-driven cavity benchmark: it agrees with OpenFOAM icoFoam under matched PISO
settings, converges at its formal order, and extrapolates to the published reference value. Two limitations
should be stated alongside. First, the study is at Re = 100, the lowest of the seven Reynolds numbers
tabulated by Ghia et al., where the flow is diffusion-dominated and the convective discretization is cor-
respondingly lightly exercised; agreement here does not establish behaviour in convection-dominated
regimes. Second, reaching benchmark accuracy on a practical mesh is a question of scheme rather than
of implementation — a second-order or limited convection scheme would reach the same accuracy at
far lower cost — and that comparison has not been run. Both are left to future work, readers should note


                                                                     23
that this is an incomplete, initial verficiation effort.

3.2.3   Sod Shock Tube Case for rhoCentralFoam Port
The lid-driven cavity case is verified using literature data, but it only covers incompressible regimes.
However, real fluid simulation in reactors would need compressible flow. For that, we need to consider
classic use cases for compressible flow such as shock formation.
    OpenFOAM provides a Sod shock tube case, a classic benchmark [62], [63]. This case is commonly
used as a benchmark for finite-volume methods [64]. This OpenFOAM case used rhoCentralFoam; as
a compressible solver, rhoCentralFoam is suitable for transonic flows, and the Sod shock tube is well
established in the literature [62], [63] The Sod shock tube case was therefore adopted.
    As with the cavity case, OpenFOAM was used to construct the Sod shock tube geometry using its
meshing tools. Once the geometry was complete, it was provided to Claude Code. After asking Claude
Code to implement rhoCentralFoam, it was asked to produce a tutorial example for V&V, namely this
Sod shock tube case, and Claude Code compared it to the exact Riemann solution by generating its own
code.
    The exact Riemann solution Claude Code used for V&V was computed by implementing the solver
from Toro chapter 4 [62]. Results are here Fig. 4:




                Figure 4: Outram-Foam V&V against the exact Riemann solution [62]



                                                       24
   The residuals are acceptable, as seen in Fig 5 for exact solution:




                            Figure 5: Outram-Foam V&V Residuals [62]

    But how can one be sure it is correct? Claude Code generated both the coding results and the V&V
case, it effectively checked its own work. One must be meticulous and independently locate the V&V
data manually.
    For this, The port was compared against Sod’s Table II [63]. Matches decently except at the rarefac-
tion wave, as shown in Figure 6:




                                                   25
                       Figure 6: Outram-Foam V&V using Sod’s Table II [63]

    The station-by-station values behind Figure 6 are given in Table VII.

Table VII: Sod shock tube: station-by-station comparison against the coarse 9-point Sod (1978)
Table II. The Outram-Foam rhoCentralFoam port (100 cells) and the exact Riemann solution are the
quantitative references; the 9-point tabulated column (ρSod II etc.) is a coarse literature sanity check
only and is not treated as authoritative. Where the port departs from it (e.g. x/L = 0.4 and 0.7, in the
rarefaction fan and at the contact) it still tracks the exact solution — the 9-point table simply cannot
resolve those features. Densities are in kg/m3 , velocity in m/s and pressure in Pa

 x/L     ρport    ρSod II    ρexact    uport    uSod II   uexact       pport       pSod II       pexact
 0.10   0.9996    1.0000    1.0000     0.00      0.00      0.00 100,000.0 100,000.0 100,000.0
 0.20   0.9996    1.0000    1.0000     0.00      0.00      0.00 100,000.0 100,000.0 100,000.0
 0.30   0.8717    0.8690    0.8775     50.61    51.86     48.28 82,560.8 82,200.0 83,274.7
 0.40   0.6090    0.4260    0.6029    176.65    293.14    180.04 49,971.7 30,300.0 49,247.2
 0.50   0.4303    0.4260    0.4263    290.31    293.14    293.29 30,726.9 30,300.0 30,313.0
 0.60   0.4262    0.4260    0.4263    293.71    293.14    293.29 30,265.7 30,300.0 30,313.0
 0.70   0.2953    0.4260    0.2656    293.90    293.14    293.29 30,351.5 30,300.0 30,313.0
 0.80   0.2652    0.2660    0.2656    293.48    293.14    293.29 30,321.1 30,300.0 30,313.0
 0.90   0.1250    0.1250    0.1250     0.00      0.00      0.00  10,000.0 10,000.0 10,000.0

    This is a reasonable result for a first attempt. Sod Table II was used because it was readily available
as a first bound check. The tabulated data are provided for 9 grid points as mentioned in [63]. This is
a relatively coarse mesh solution, as typical solutions can have as many as 100 points [63]. It is never


                                                    26
as accurate as the exact solution, but still useful as a sanity check that Claude Code was not fabricating
results.
    Naturally, when a coarse mesh is compared to the Outram-Foam mesh of 100 cells, the coarseness
can explain the discrepancy. Is there anything more concrete? For this, one may examine Fig 4 of
Marzouk’s paper [64]. In his Fig 4 caption, Marzouk cites the Castro solver’s verification page [65].
That page also cites chapter 4 of Riemann solver [62], the same chapter that Claude Code implemented.
The method Claude Code used is therefore the standard one, not one it fabricated.
    More usefully, Marzouk solves the same Sod problem at the same dimensionless time τ = 0.2, and
compares it against the Castro solver, which is an entirely different code developed by a different group.
So if Outram-Foam also matches Marzouk, then it is not being self-validated anymore. Furthermore,
Marzouk states τ = 0.2 explicitly [64]. Sod’s paper [63] never actually gives the time, neither for Table
II nor for his figures. Marzouk is therefore the citable source for the comparison time.
    The manual check of the reference is valuable, but it is also worth doing a check that does not require
complicated programming. Marzouk’s Figure 4 was digitised approximately. Pressure, velocity and
density were read off using graphreader [51] at dimensionless time τ = 0.2 as mentioned by Marzouk
[64]:




                                                    27
Figure 7: Outram-Foam V&V using Marzouk’s Fig 4 Digitised using GraphReader (approx only)
[64]

                                           28
      A representative slice of the digitised pressure comparison is tabulated in Table VIII.

Table VIII: Sod shock tube pressure: Outram-Foam port vs. Marzouk (2020) Fig. 4, digitised. Ten
representative stations of the pressure channel at τ = 0.2, dimensionless (p/P0 ). Marzouk’s points are
read off a printed figure (approximate); the exact Riemann solution is the quantitative reference and
∆ = pMarzouk − pexact measures digitisation agreement, not solver error. The single large residual at
x/L ≈ 0.85 is one digitised point straddling the shock jump. The density and velocity channels agree
comparably over the full digitised sets (max|∆|: ρ 0.061, u 0.035; RMS 0.021 and 0.012).

                                  x/L     pMarzouk   pexact    pport   ∆ (M−E)
                                 0.0469   1.0057     1.0000   1.0000   0.0057
                                 0.1925   1.0057     1.0000   1.0000   0.0057
                                 0.2911   0.8854     0.8710   0.8602   0.0144
                                 0.3709   0.6045     0.5762   0.5812   0.0283
                                 0.4507   0.3981     0.3714   0.3823   0.0267
                                 0.5634   0.3064     0.3031   0.3024   0.0033
                                 0.7700   0.3064     0.3031   0.3030   0.0033
                                 0.8545   0.2720     0.1000   0.1788   0.1720
                                 0.8826   0.1000     0.1000   0.1000   0.0000
                                 0.9859   0.1000     0.1000   0.1000   0.0000


     The CSV file was obtained manually. Then Claude Code was asked to write a Python script to
produce the PNG. This became Figure 7.
     Overall, given how the Outram-Foam solver compares with the exact Riemann solution, the coarse
Sod Table II sanity check, and the independent Marzouk digitised data, the port is qualitatively validated
for the Sod shock tube, with pressure and density agreeing to within 5%, provided they are distanced
from the discontinuities. There, the errors can be as high as 20%. However, in the discontinuities, it is
difficult to have lower error anyhow. Taking all this into account, the Sod shock case can be considered
ported rather satisfactorily for something as difficult to solve as a shock front.

3.3     TAMPINES Steam Tables
3.3.1    Steam Tables Testing Summary
The tampines-steam-tables library took some time to develop. The commit history is long, so it was
summarised with AI assistance in Table IX which summarises the two development phases; the fuller
AI-generated summary history is in Table XXI in Appendix C.
    As seen in Table XXI and IX, Phase I concerned Tampines Steam tables as a standalone IAPWS-
IF97 library. This was meant for future development of Tampines and for the steam cycle simulation in
an FHR Educational Simulator.
    At that time, no known Rust library fully provided IAPWS-IF97 equations with (p,T), (p,s), (p,h)
and (h,s) flashes. So this was a first, unpublished work. At that time, all of the steam tables were copied
from [42]. Each flash was tested against the entire steam table. Only for (h,s) flash, there were parts in
the saturation dome that could not be tested due to the limitations of the (h,s) equations. Those regimes
were initially left as to-do items. But as of today, they fall back to an iterative (p,s) equation to solve the
parts where the (h,s) equation does not apply in the saturation dome. Table X summarises the per-flash
limitations found across the whole steam table.
    For those, the flash equations agree well with those values in the table for areas outside the saturation
dome. Of these, the (h,s) flash seems to be the most problematic around certain regions such as triple-
point and critical point. Some parts of V &V are left out for the high pressure regions, but these are not
particularly important for LWR-type scenarios or steam turbines, where maximum pressure is almost
150 bar for PWRs and 70-75 bar for BWRs. Hence, these are left out, as full coverage is not necessary
here. This can be addressed in future work. SCWR conditions, which involve pressures of around


                                                       29
Table IX: AI-generated Summary of tampines-steam-tables development. Phase I spans 947 com-
mits in the standalone repository (2025-01 to 2026-06); Phase II covers 74 commits on the migrated
crate within outram-park-backend (2026-06 to 2026-07). Full per-commit detail is given in Ta-
ble XXI, Appendix C.

         Period       Focus                      Key milestones
         Phase I — standalone IAPWS-IF97 property library
         2025-01      Forward equations       Regions 1–5 Gibbs/Helmholtz forward properties, B23
                                              boundary and saturation line; dimensioned with uom,
                                              verified vs. IST sets A–C
         2025-01/04 Backward flashes          (p, h), (p, T ), (p, s) and (h, s) inversions across the IF97
                                              surface
         2025-02      Transport properties    Dynamic viscosity (2008), thermal conductivity (2011),
                                              surface tension and dielectric constant
         2026-03/06 Choked-flow scaffolding Nozzle and converging–diverging solvers; Marviken
                                              blowdown harness; Moody and Zaloudek datasets digitised.
                                              In-dome solver passing but near-bubble-point artifact
                                              unresolved at migration; validation completed in Phase II
         Phase II — migrated into outram-park-backend
         2026-06      Migration               Vendored into the workspace; uom/ndarray/egui upgrades;
                                              BLAS decoupled
         2026-06      Choked-flow completion Near-bubble-point artifact resolved; unified HEM
                                              dispatcher; Moody isobars pass (v0.2.1)
         2026-07      Array solver            TampinesSteamArray 1-D PIMPLE pipe solver and
                                              tampines framework crate; steam-generator integration
         2026-07      Blowdown V&V            Edwards–O’Brien blowdown (v0.2.3); HybridAllMach
                                              solver stabilised (v0.2.4)



22 MPa and above [66], cannot yet be handled. Moreover, Singapore is not currently surveying SCWR
at the moment. This is of little concern.
     For completeness, TAMPINES eventually had to implement compressible-flow solvers. From basic
thermodynamics references such as Cengel [43], compressible-flow must include the critical flow phe-
nomena. Therefore, choked flow was added and there were plans to do blowdown tests with V&V using
Zaloudek, Moody and Marviken tests. However, without the critical-flow solver machinery, these were
only scaffolds/harnesses, not implemented at all.
     For critical flow, initial placeholder values were given for the speed of sound, compressibility, etc.,
so that it linearly interpolates against the saturated-liquid and saturated-vapour values. This was not
accurate, but it was deferred to future work. It will be addressed if necessary. Note that such values are
linearly interpolated unless otherwise stated.
     At this point, minimal AI was used, except to check the speed of sound, which was critical for choked
flow. NUS-AI initially suggested that the author’s linear interpolation was incorrect, and provided a
formula for Wood–Wallis speed of sound (frozen speed of sound).
     Of course, on further investigation, there were many kinds of speed of sound leading to different
levels of choked flow in the two-phase dome. This was very troublesome when surveying the NRC
literature.
     Moreover, no algorithm was found in the open-source domain to the best of the author’s knowledge.
Most of the codes which could do this were closed source. After initial debugging, the authors found
that two-phase choked flow was difficult.
     However with move to agentic coding, the debugging process was sped up, though it still needed
plenty of human intervention.
     With agentic coding, however, CoolProp was also translated to Rust (not covered in this article, for
length) which provided Helmholtz equations for both steam and helium.
     Of course, reproducing a steam table is not novel, and the distinction from CoolProp should be stated
carefully rather than overclaimed. CoolProp does accept an (h, s) input pair through its generic flash


                                                        30
Table X: AI-generated summary of the property-flash limitations found when each backward flash was
tested against the full IAPWS-IF97 steam table of [42] (triple point to 1000 bar, Regions 1–5). Choked-
flow / two-phase critical-flow limitations are excluded here and treated separately. This table was gener-
ated with AI assistance from a survey of the tampines-steam-tables test suite and source comments;
the author reviewed and verified its contents.

        Flash Region / condition       Limitation                                         Current handling
        (p, T ) Saturation dome        (p, T ) is non-unique inside the dome, so          Not attempted (expected
                (Region 4)             mixture h, s, c p , cv , v, w cannot be resolved   degeneracy)
                                       without a quality input
        (p, T ) Single phase,          High-pressure single-phase table not               Deferred to next major
                240–1000 bar           implemented                                        version
        (p, h) Single phase,           Flash goes out of bounds at 1000 bar               Accepted Caveat, near
                1000 bar                                                                  max pressure
        (p, s) Single phase,           High-pressure single-phase table not               Deferred to next major
                240–1000 bar           implemented                                        version
        (h, s) Triple-point pressure   (h, s) equations cannot resolve triple-point       Accepted Caveat
                (0.006112127 bar)      liquid/vapour accurately
        (h, s) Single phase,           Flash goes out of bounds at 1000 bar            Accepted Caveat, near
                1000 bar                                                               max pressure
        (h, s) Saturation dome         (h, s) backward equations invalid over parts of Falls back to iterative
                                       the dome                                        (p, s) solve
        (h, s)   Near critical point                     ◦
                                       T off by up to 5 C, v up to 10%, h f g up to 5% Accepted accuracy
                                                                                       caveat
        (h, s)   Low pressure          Pressure back-equation error ∼20% at            Accepted accuracy
                                       0.1–1 bar, falling to ∼2% by 10–20 bar; dew     caveat
                                       point can fail (e.g. at 8 bar)



routine, so what tampines-steam-tables adds there is a direct IAPWS-IF97 backward (h, s) formulation
rather than a capability CoolProp lacks outright.
     The substantive difference is critical flow. For nuclear applications, two-phase critical flow is impor-
tant, and to the best of the authors’ knowledge — based on a survey of CoolProp, ThermoSysPro and
DWSIM, assisted by agentic search of their source — no open-source thermophysical property library
ships a verified HEM critical-flow solver. That survey is not exhaustive, and the claim should be read
as such. Subject to it, tampines-steam-tables appears to be the first open-source steam-table library with
critical-flow thermodynamics and solvers embedded in it and verified against published charts.

3.3.2   Steady State homogeneous-equilibrium-model for Two Phase Choked Flow
Initially, to break up the problem, the authors required understanding of the flash equations and their
limitations, and to structure a plan towards obtaining a critical-flow solver. In doing so, the authors
would know how best to prompt Claude Code to solve the problem. Without this guidance, Claude
Code tended to go in circles, wasting tokens implementing the wrong solutions.
     In any critical flow, we go from stagnation (p,h) to arrive at choked flow (p,h) using an isentropic
process, wherein we normally use an iterative (p,s) flash to find the speed of sound. Now, due to the
kink in the speed of sound at the bubble point, a specialised dispatch algorithm is required in order to
find the choked flow as the mass flux was not unimodal and had two local maxima, usually one before
the bubble point and one after.
     It was important to know which local maxima to take.
     The best approach to break down this problem was to first solve the inverse problem. Given choked
flow conditions, what would the stagnation conditions be?
     A deliberate decision to scope down the choked flow to HEM. Additionally, we did not wish to
address the other formulations, as HEM is the most basic. The remaining cases can be handled later.


                                                             31
     This was the simpler problem to solve as it was not iterative. For this, it was convenient to use data
from Saha et al. [50] especially since it is from the NRC, a gold-standard source. Moreover, it had
graphs where data was in terms of choked flow conditions rather than stagnation conditions. This made
it ideal for the choked flow to stagnation condition graph. Results are shown in Figures 8:

                                          3,000
        Stagnation Enthalpy, h0 [kJ/kg]




                                          2,500


                                          2,000


                                          1,500


                                          1,000


                                           500


                                                  102                 103                    104                  105
                                                                 Critical Mass Flux, G [kg/(m2 ·s)]
                                                        Literature    TAMPINES         xt = 0.0001    xt = 0.05
                                                        xt = 0.10     xt = 0.15        xt = 0.20      xt = 0.25
                                                        xt = 0.30     xt = 0.35        xt = 0.40      xt = 0.45
                                                        xt = 0.50     xt = 0.55        xt = 0.60      xt = 0.65
                                                        xt = 0.70     xt = 0.75        xt = 0.80      xt = 0.85
                                                        xt = 0.90     xt = 0.95        xt = 1.00

Figure 8: Zaloudek critical-flow validation: stagnation enthalpy vs. critical mass flux (log scale) for each
quality curve.

    With that done, we then tackle the forward iteration problem since the backward function is solved.
    For this, Claude Code’s Opus models were better, though they consume more tokens. The reasoning
and debugging in Opus 4.8 were far superior to that of Sonnet 4.5 used during June-early July 2026.
This enabled it to be better at debugging.
    It was used to check the shape of the mass-flux curves before and after the bubble point. Claude Code
proposed and implemented the Golden Section algorithm which was then checked against literature [52]
and accepted.
    The idea was to apply golden-section search before and after the bubble point
    However, considerable debugging was required around the bubble point, because the kink is genuine
and throws numerical solvers off. Depending on how deeply subcooled the solvers were, slightly differ-
ing algorithms and adjustments were needed. Claude Opus helped to debug this by suggesting solutions
and performing iterative debugging.
    Claude Code was monitored from the author’s phone, observing what Opus was doing; for the most
part it was left to fix issues automatically. It is difficult to recall in detail which fixes Opus made and
which the author contributed.
    Nevertheless, Moody’s graphs were digitised into CSV, and Claude was asked to confirm that the
graph was reproduced to within reasonable bounds. This resulted in Figure 9:


                                                                            32
       Critical Mass Flux, G [kg/(m2 ·s)]   105




                                            104




                                            103




                                                  0          500        1,000           1,500      2,000     2,500       3,000
                                                                      Stagnation Enthalpy, h0 [kJ/kg]
                                                      Literature                        TAMPINES           pref = 0.25 MPa
                                                      pref = 0.50 MPa                   pref = 1.00 MPa    pref = 2.00 MPa
                                                      pref = 4.00 MPa                   pref = 6.00 MPa    pref = 8.00 MPa
                                                      pref = 10.00 MPa                  pref = 12.00 MPa   pref = 14.00 MPa
                                                      pref = 16.00 MPa                  pref = 20.00 MPa   pref = 30.00 MPa
                                                      Bubble-point locus (Moody)

Figure 9: Moody critical-flow validation: critical mass flux (log scale) vs. stagnation enthalpy for each
isobar pressure.

    The agreement is acceptable except for the kink region at the bubble point. This is difficult because
of the discontinuity.
    The errors are summarized in Table XI, XII, Figure 10, and Figure 11:




                                                                                   33
Table XI: Summary of the Zaloudek critical-flow validation dataset for the TAMPINES HEM dis-
patcher, benchmarked against the Zaloudek curves digitised from Fig. 2 of Saha [50]. The pres-
sure error ε p = |pcrit,solver − pcrit,lit |/ max(|pcrit,solver |, |pcrit,lit |) is the relative pressure difference as eval-
uated by the regression tests. The mass-flux columns report the absolute log-scale error εlog G =
| log10 Gsolver − log10 Glit | and its linear-scale equivalent εG = |Gsolver − Glit |/Glit = 1 − 10−εlog G ; εG is
a derived diagnostic and is not directly asserted. Note that the regression-test pass/fail gate for mass flux
is a relative tolerance on log10 G rather than the absolute εlog G tabulated here.

     xt          N       max ε p        mean ε p        max εlog G         mean εlog G         max εG         mean εG
  0.0001        17       0.0024          0.0012           0.0348              0.0187           0.0771          0.0430
  0.0500        17       0.0139          0.0051           0.0303              0.0113           0.0673          0.0255
  0.1000        17       0.0038          0.0017           0.0267              0.0092           0.0597          0.0208
  0.1500        17       0.0041          0.0014           0.0226              0.0088           0.0508          0.0201
  0.2000        17       0.0047          0.0009           0.0281              0.0121           0.0628          0.0274
  0.2500        17       0.0045          0.0006           0.0266              0.0104           0.0593          0.0235
  0.3000        17       0.0032          0.0006           0.0215              0.0084           0.0484          0.0192
  0.3500        17       0.0012          0.0004           0.0265              0.0091           0.0593          0.0208
  0.4000        17       0.0006          0.0002           0.0244              0.0083           0.0547          0.0189
  0.4500        17       0.0012          0.0004           0.0212              0.0074           0.0477          0.0171
  0.5000        17       0.0018          0.0003           0.0234              0.0078           0.0525          0.0180
  0.5500        17       0.0005          0.0003           0.0246              0.0079           0.0550          0.0180
  0.6000        17       0.0015          0.0003           0.0372              0.0102           0.0820          0.0231
  0.6500        17       0.0030          0.0003           0.0304              0.0104           0.0675          0.0234
  0.7000        17       0.0038          0.0003           0.0418              0.0151           0.0918          0.0340
  0.7500        17       0.0128          0.0008           0.0403              0.0173           0.0885          0.0388
  0.8000        17       0.0129          0.0008           0.0504              0.0254           0.1096          0.0566
  0.8500        17       0.0354          0.0021           0.0602              0.0283           0.1293          0.0626
  0.9000        17       0.0024          0.0002           0.0637              0.0366           0.1364          0.0805
  0.9500        17       0.0019          0.0002           0.0772              0.0421           0.1628          0.0918
  1.0000        17       0.0004          0.0001           0.0809              0.0331           0.1699          0.0718




                                                            34
                                                   357 validation points
                                                   one-to-one

           TAMPINES G (kg m−2 s−1 )
                                      104




                                      103




                                      102
                                            102                         103                           104
                                                                           Zaloudek G (kg m−2 s−1 )


                                  10−1             εp
                                                   εlog G
       maximum error




                                  10−2



                                  10−3



                                  10−4
                                         0        0.1       0.2   0.3         0.4     0.5      0.6    0.7   0.8   0.9   1
                                                                                Throat quality xt

Figure 10: Zaloudek critical-flow validation of the TAMPINES HEM dispatcher. Top: mass-flux parity
over all extracted points. Bottom: maximum pressure and mass-flux errors by throat quality.




                                                                                  35
Table XII: Summary of the Moody critical-flow validation dataset for the TAMPINES HEM stagnation
mass-flux routine, benchmarked against the Moody maximum-discharge curve [49]. The mass-flux
error is the absolute log-scale difference εlog G = | log10 Gsolver − log10 Glit |, which is the metric asserted
by the regression tests; εG = |Gsolver − Glit |/Glit = 1 − 10−εlog G is its linear-scale equivalent, reported as
a diagnostic. The “all” columns include diagnostic Region 1 and Region 3 points that are not asserted,
while the Region 4 columns isolate the in-dome two-phase points asserted at the standard Moody log-
scale tolerance (εlog G ≤ 0.06).

  p0 /pref    N     max εlog G , all   mean εlog G , all        max εlog G , R4   mean εlog G , R4   max εG , R4
  0.25       32         0.2554             0.0364                  0.0444             0.0074           0.1076
  0.50       24         0.4204             0.0310                  0.0127             0.0043           0.0297
  1.00       21         0.7212             0.0817                  0.0166             0.0062           0.0391
  2.00       18         0.6377             0.0751                  0.0174             0.0078           0.0408
  4.00       18         0.4712             0.0381                  0.0247             0.0182           0.0584
  6.00       26         0.5284             0.0451                  0.0239             0.0102           0.0566
  8.00       30         0.6105             0.0605                  0.0221             0.0091           0.0522
  10.00      23         0.5563             0.0641                  0.0194             0.0079           0.0457
  12.00      25         0.5798             0.0655                  0.0204             0.0155           0.0480
  14.00      25         0.6299             0.0684                  0.0249             0.0138           0.0590
  16.00      27         0.6345             0.0763                  0.0203             0.0112           0.0480
  20.00      28         0.6866             0.0894                  0.0154             0.0082           0.0360
  30.00      24         0.7011             0.0965                  0.0069             0.0044           0.0161




                                                           36
                                                     321 extracted points
                                      105            one-to-one

           TAMPINES G (kg m−2 s−1 )


                                      104




                                      103



                                                             103                            104                            105
                                                                            Moody G (kg m−2 s−1 )

                                       100
         maximum εlog G




                                      10−1



                                      10−2

                                                                                                                 all extracted points
                                                                                                                 Region 4 only
                                      10−3
                                             0   2     4     6     8   10    12    14      16     18   20   22     24    26      28   30
                                                                                       p0 /pref

Figure 11: Moody critical-flow validation of the TAMPINES HEM stagnation mass-flux routine. Top:
mass-flux parity over all extracted isobar points. Bottom: maximum log-scale mass-flux error by
stagnation-pressure isobar, comparing the full diagnostic dataset with the asserted in-dome Region 4
subset.

    From these, one can see that the data matches well. Error was quantified using log scale, because
digitisation was in log scale.
    Also, it is interesting to note that the HEM solver managed to reproduce the shape of the bubble
point curve due to the kink of Moody’s critical-flow diagram under Figure 1 of Saha [50]. This shows
that the trends produced match those in the literature. This is also shown in Figure 9 which shows that
the solver can roughly produce Moody’s bubble point locus at least for lower quality steam.
    Overall, the trend is broadly there. Although there are some points where the solver fails to produce
the critical mass flux, on the whole it appears acceptable for this attempt. Future refinements can be
made.
    The main issue now is whether this will impact critical flow in a benchmarked test. Hence, we
proceed to the Edwards pipe demonstration.

3.3.3   Transient Edwards Pipe Blowdown Test
Since we do not know if the steady-state errors are too large, it is best to test this in a transient case. This
is Edwards blowdown.

                                                                                  37
     Only preliminary solver results for the Edwards pipe blowdown test are presented here, based on
agentic coding. Rigorous derivation is reserved for future work, as it is out of scope for this research
log.
     The Edwards pipe is a good choice of test, as both RELAP and TRACE use it; the nodalisation and
initial-condition data used here are taken from the RELAP paper [67].
     Here there is both code-to-code verification and validation, so it can be determined whether the
behaviour at the bubble point causes serious numerical difficulty.

Summary of Debugging
The authors subsequently investigated whether the SIMPLE or PISO algorithms would be more appro-
priate for the present application, although using either approach would increase the computational cost.
Table XIII summarises the issues encountered and the corresponding stages of the investigation. Readers
should note that rhoCentralFoam falls under the Kurganov–Noelle–Petrova (KNP) classification, and
that the two names are sometimes used interchangeably in this prose.

Table XIII: AI-generated summary of the Edwards–O’Brien blowdown debugging timeline for the
TampinesSteamArray PIMPLE / HybridAllMach Rust solver. Reconstructed with AI assistance from
the case READMEs and the solver debugging notes; the authors reviewed and verified its contents.
RMSE values are gauge-station GS-1 pressure against the Edwards data [67].

   Stage               Issue encountered                              Fix and outcome
   Rust TampinesSteamArray PIMPLE solver (16 July 2026)
   16 Jul — Energy  Plateau collapses to 17.4 psia (vs. ∼350); the     Conservative ddt with continuity-consistent
   conservation (A) non-conservative ρ ∂ h/∂t form over-drains         ρcont and compressibility ψ = ∂ ρ/∂ p|h ;
                    enthalpy during the flash                          plateau recovers to 392.7 psia (RMSE 59.8), no
                                                                       clamps
   16 Jul — Shock      High-frequency ringing at the near-sonic        Mach-weighted KNP (rhoCentralFoam)
   capturing (B)       flashing front from the low-dissipation         dissipation in a HybridAllMach mode;
                       pressure solver                                 dissipate static enthalpy, gate on min(Ma);
                                                                       ringing −55.5%
   16 Jul — Tail       Hybrid crashes at t ≈ 0.18 s: a rarefied cell’s Rarefied-tail density taper (KNP off below 50,
   stability (C)       enthalpy diverges and trips the (p, h) 273.15 K full above 100 kg/m3 ); stable over the full
                       validity edge                                   600 ms (RMSE 30.6)


     The Edwards validation required sustained, human-led iterative development: the solver reached a
stable 600 ms run only after the three targeted fixes above, each of which depended on understanding the
underlying physics rather than on generating more code. Domain knowledge and practical experience
remain essential and are not replaced by AI models, including highly capable ones such as Opus, when
developing new numerical solvers.
     This table was AI-generated, and the author was initially unfamiliar with the details. Claude was
therefore asked to explain the concepts from the energy balance upward, so that the steps taken could
be checked for reasonableness against the literature, or at least against first principles. That checking
is the substantive point rather than an aside: an AI-generated summary that has not been independently
understood is not a result.
     What follows is an account of the fixes Claude Code made, presented as interim work. Fuller solver
derivation and quantification is reserved for a later paper, the scope being too large for this one.

Enthalpy Drain Fix
First, this is common sense energy balance:

                                                 Dh
                                                     =S
                                                      ρ
                                                 Dt
   S represents all the source and sink terms. This comes from the full conservative form:

                                                          38
                                            ∂ (ρh)
                                                   + ∇ · (ρuh) = S
                                              ∂t
   When taking product rule:                              
                                      Dh      ∂ρ
                                    ρ    +h      + ∇ · (ρu) = S
                                      Dt      ∂t
   Normally the mass conservation equations necessitate that:
                                              ∂ρ
                                                 + ∇ · (ρu) = 0
                                              ∂t
    Though in approximate form, discretisation and after we apply Gauss’s theorem and approximate
face fluxes as per normal finite volume method [68], [69]:

                                          ρ new − ρ old
                                  Vcell                 + ∑(ρu) f · A f = 0
                                               ∆t         f

   However, due to discretisation or other such errors, this term may not drop to zero. So, under
numerical solution:

                                      ρ new − ρ old
                                  Vcell             + ∑(ρu) f · A f ̸= 0
                                            ∆t        f
                                                            new    old
                                                                                    
   This caused the overcooling due to the spurious h Vcell ρ ∆t−ρ + ∑ f (ρu) f · A f term.
   So using the ρ new was not suitable. If we want the continuity to hold, we had to force the continuity
equation to zero.

                                          ρ cont − ρ old
                                  Vcell                  + ∑(ρu) f · A f = 0
                                                ∆t         f

   In doing so:

                                                      Dh
                                             ρ cont      + h (0) = S
                                                      Dt
                                                    Dh
                                                 ρ cont =S
                                                    Dt
    When ρ cont is used, the continuity error used for the energy balance equation is solved, preventing
the overdrain of enthalpy.
    The mass balance itself is not written in terms of pressure, whereas rhoPimpleFoam is essentially
based on the pimpleFoam algorithm which is a pressure based solver rather than a density based solver
like rhoCentralFoam.
    The mass balance itself needs to be written in terms of pressure.
    Starting with:
                                            ∂ρ
                                                + ∇ · (ρu) = 0
                                            ∂t
    In differential form, we can use thermodynamic calculus, for pure steam
                                                            
                                                ∂ρ             ∂ρ
                                 dρ(p, T ) =           dT +           dp
                                                ∂T p           ∂p T
   Or if one desires the use of enthalpy:
                                                                        
                                                      ∂ρ              ∂ρ
                                 dρ(p, h) =                      dh +          dp
                                                      ∂h       p      ∂p   h


                                                           39
     Now, in the saturation dome, then the ρ(p, T ) equation doesn’t quite apply, because in saturation,
under thermodynamic equilibrium, then T and p are not enough to describe the thermodynamic state of
the system. One needs to include quality. rhoPimpleFoam traditionally deals with single phase flows
as in for the Sod shock tube, but for two phase flashing, this algorithm (the closure part specifically)
fails without proper correction. Again, the PIMPLE algorithm still works, but one cannot use a rhoPim-
pleFoam translation in this case as it uses the wrong thermodynamics. With AI-assisted debugging, the
latter form was used instead.
     Now, under constant enthalpy (which translates to constant temperature in the single phase case for
ideal gas), the derivative is reduced to:
                                                      
                                                       ∂ρ
                                          dρ(p, h) =        dp
                                                       ∂p h

                                           dρ(p, h)|h = ψh d p
   Equivalently, the constant temperature version used in original rhoPimpleFoam is:

                                           dρ(p,t)|T = ψT d p
                                  
   From hereon, we define ψh ≡ ∂∂ ρp .
                                     h
   With discretisation, we obtain:

                                      ρ new = ρ old + ψh (p − pold )
    Now, ψT used for rhoPimpleFoam was wrong, so in agentic debugging, ψh was used instead. This
ensured that the plateau at 392.7 psia was recovered for the Edwards case, and that the solver was stable.
Moreover, using ψh would ensure that the solver can work in both single and two phase regimes. This
resulted in Figure 12:




                                                   40
                         Figure 12: Enthalpy Drain Fix Results with Ringing

   Nevertheless, there was noticeable ringing and oscillation through the system even with these fixes.

Shock Capturing Fix
To remove ringing and oscillation, it was initially decided to use rhoCentralFoam type solver to re-
duce the shocks. Unfortunately, these were quite futile as they reduced ringing, but re-introduced the
instability issues as seen in Figure 13:




                                                 41
          Figure 13: Ringing Fix with rhoCentralFoam introduced new numerical instability

   To remove the ringing and oscillation and maintain stability, the author then decided to use a rho-
CentralFoam like solver in the shock regime, and rhoPimpleFoam like solver in the subsonic regime.
This became known as the HybridAllMach mode in Table XIII. Hence, the TampinesSteamArray, the
Rust struct responsible for solving the Edwards Pipe, had two modes, a rhoPimpleFoam mode and a
HybridAllMach mode. This was user selectable.
   The Mach numbers used to switch the solver to a rhoCentralFoam like solver are based on the current
”owner” cell O and neighboughring cell N:

                                            |uO |                  |uN |
                                   MaO =          ,        MaN =
                                             cO                     cN
where c is the local speed of sound evaluated from the homogeneous-equilibrium steam tables at the cell


                                                      42
state (p, h). Inside the saturation dome this is the two-phase equilibrium sound speed, which is far lower
than that of either phase alone. The blending weight is then:
                                                       
                                    Ma f − Malo
                     β f = clamp                  , 0, 1 ,    Ma f = min (MaO , MaN )
                                    Mahi − Malo
    Mahi and Malo are set at 1.0 and 0.3 respectively. This makes sense because Mach 1 is sonic, and
Mach 0.3 is the lower bound where compressibility effects start to matter.
    Using this weighting allows us to switch on or off the rhoCentralFoam like KNP solver based on
Mach number.
    Nevertheless, introducing this solver also produced yet another bug. The solver again overdrains
enthalpy and some cells in the system went below freezing in the later part of the depressurisation. This
necessitated the final fix.

Tail Stability Fix
For the last fix, we know that rhoPimpleFoam is stable in all regimes, just produces ringing during
depressurisation. Since the enthalpy overdrains in the low pressure, low density regime where the system
is already significantly depressurised, it makes sense to turn off the rhoCentralFoam type solver and
restore the rhoPimpleFoam type. Intuitively, this makes sense.
    This is because rhoPimpleFoam is the more numerically stable of the solvers and prevents enthalpy
divergence. Having the KNP switch off at 50 kg/m3 , close to the density of steam, is an elegant way to
patch the solver to make it more stable all the way up to 600 ms. This is more of a stability patch than
anything else, but it worked!
    All in all, the compressibility and ρcont fixes are more grounded in thermodynamics, whereas the
KNP (rhoCentralFoam) type solver blending helps fix ringing and potential numerical instabilities asso-
ciated with it. These are more of stopgap measures and numerical improvements to an otherwise stable
solver with some ringing.
    This yields the figure shown in Figure 14:




                                                   43
                   Figure 14: Final performance of HybridAllMach after debugging

    Significant ringing was still observed, but it was damped compared to before. This is an acceptable
result for a first attempt, which was after all, a HEM solver with limitations. Instabilities notwithstand-
ing, it still performs adequately, the trend of pressure drop still follows experiment and RELAP code
somewhat well at a root mean square error of 30.6 psia. Though much remains to be desired of the void
fraction.

Workflow and future work
The workflow that emerged for the Edwards case was as follows. Claude Code proposed and imple-
mented the numerical fixes described above. Because the first author was not initially familiar with
the derivations behind them, he asked Claude Code to set out each one from first principles, and then
checked that derivation himself against the finite-volume literature [68], [69] and against the conserva-

                                                    44
tion arguments reproduced in this section, before accepting the fix.
    It is worth being explicit about what this does and does not establish, because the distinction is
the one this research log is arguing for. Asking a model to justify its own output is not verification:
a model that produced a wrong fix can produce a plausible derivation for it, and the two failures are
correlated. What made the step meaningful was that the derivation was checked by a human against
independent sources, and that it terminated in quantities — the continuity-consistent density ρ cont and
the compressibility ψh — that can be written down from the governing equations without reference to
the code. Where that check could not be closed independently, the result is reported here as interim
rather than verified.
    The GS-1 pressure comparison against the Edwards data is accordingly a validation of the solver’s
gross behaviour only. A full derivation, a mesh-convergence study of the kind performed for the cavity
in Section 3.2.2, and quantitative void-fraction validation are reserved for future work.


4     Discussion
4.1     Initial V&V Efforts of Outram-Foam and Outram-Foam Derived Solvers in Tampines
        Steam Tables
Using Claude Code, the path from draft code to V&V-ed case has been significantly shorter as the code
produced was able to match solutions in literature and experimental data to within reasonable bounds.
Moreover, the development of an initial draft of the HEM solver validated using the Edwards Pipe
Blowdown test using Claude Code demonstrates its effectiveness in producing new thermal-hydraulics
code quickly from existing libraries, provided there is some guidance from the human in the loop.
    This contribution is significant because prior to this, critical choked flow for two phase steam and
water was scarcely found in open-source repositories. From this agentic coding experience, the bot-
tleneck for code development now is the human V&V required to validate and certify that the drafts
produced by AI agents is useful and safe enough for educational and research uses.

4.2     Speed Increase and Productivity Gain
Both agentic development and validation efforts in this research log required human-in-the-loop devel-
opment, which should dispel the myth that AI is ready to replace human beings, at least in this field. In
this case, it was demonstrated that Agentic AI augmented capabilities of human beings to boost produc-
tivity.

4.2.1    Humans are Still Required
AI-assisted coding is effective, and much faster. From Table I, one month can produce code for thermo-
dynamics, PRKE, Monte Carlo, and NJOY translation.
     In the span of a few months, the Rust ports were done.
     as of July 23 2026 we have - Rust Translation and Refactoring of many codes - Verified CFD in
Outram-Foam - NJOY and Outram MC (not in this research log) - Work in Progress PFLOTRAN trans-
lation - Preliminarily Verified 1D Homogeneous Equilibrium Solver in TampinesSteamArray
     However, this speed increase is only possible with AI for someone with background knowledge of:
     - Rust Programming Language - CFD - Reactor Physics - Thermal Hydraulics - Some experience
with NJOY, OpenFOAM and OpenMC
     The author has had these experiences from PhD [2], and these proved to be extremely valuable in
guiding and prompting the AI, and doing V&V on the code afterwards, as was done in TUAS [5]. These
skills are indispensable, and it is still up to humans to verify and validate the codes generated. AI will
not replace human beings. Rather, it is a workforce enablement tool, as is the case here.
     This is in alignment with the government, as Dr Tan See Leng said



                                                   45
    ” While an AI-ready workforce offers significant potential to improve productivity, we must steer
AI adoption to enhance our workers’ potential, not displace or replace it.” [70] In this case, AI was used
to draft and generate code, but it is human input which then checked and validated to make sure it is of
use and correct enough for teaching and research. Even during development, as mentioned, the authors
needed to give AI constant guidance to ensure tokens were not wasted chasing the wrong solution, when
the implemented solution was obviously wrong.
    This use of Agentic Coding and translation in Outram Park is exactly a case study in AI.

4.2.2   Ballpark Productivity Gains when using Agentic Coding
Estimate using Boehm et al’s Method
With this combination however, it is possible to achieve significant savings. When estimating the value
of outram park, it is possible to use several estimation techniques. The upper bound is classical software
cost estimation where cost can be estimated by person months [71]:

                                  Person Months = 2.4 ∗ (KLOC)1.05                                     (5)
     For outram park backend in end july, the repository was in the order of 350,000 lines of code or 350
(kilo lines of code, KLOC). Using Boehm’s formula, we obtain about 1125 person months of productiv-
ity.
     Priced at SGD$10,000 per month, we would have a value of about SGD$11.26 million or about
USD$8.66 million depending on exchange rate. These are rough estimates that estimate a repository’s
value based on the number of lines of code, which may not reflect the value that this is open-source code.
Moreover, it does not reflect the use of modern tools such as language server protocol, autocompletes
and neovim which helped speed up development.

Estimate using pre-agentically written Rust Code as Baseline
To obtain a better estimate, consider the author’s pre-agentic repositories: TUAS [3], ,tampines-steam-
tables [72] and boon lay (still in development) [73] as an example. During his PhD the author spent
roughly two years learning Rust and developing it (2022-2023) formerly named ”thermal hydraulics
rs”[74], and another 2 years in SNRSI (2024-2025) where it evolved into TUAS [3]. This is 4 years
total just to get it out and validate it. Suppose verification and validation took about 1.5 years of that
effort. With TUAS, there were 96 KLOC including doc comments pre-AI. With tampines-steam-tables
there were about 55 KLOC in the same era by roughly end 2025, with a little bit of AI assitance from
NUS AI-know for root finding solvers. Boon Lay was another 15 KLOC roughly, partly generated with
NUS AI-know, but at a rate nowhere near the level of agentic coding Claude Code offered. A naive
computation gives three years to generate roughly 165 KLOC without validation, allowing that other
projects and work were ongoing throughout. This would be about 55 KLOC per year done at a more
sustainable pace. This is shown in detail, using AI summarised review of git logs in Table XIV for work
done before Agentic coding:




                                                   46
Table XIV: Pre-agentic repositories forming the productivity baseline, measured 2026-06-22. Code
lines exclude blank and comment-only lines; total lines include both, so Rust doc comments, which
carry executable doctests, appear only in the total. An active day is any calendar date carrying at least
one commit; the total is a union of distinct dates rather than a column sum, because these projects
overlapped in time. TUAS is reported net of the code it inherited from thermal hydraulics rs at
spin-out — specifically net of the tree TUAS imported wholesale at its second commit, c451c8e, rather
than net of the predecessor’s own full extent, so that what is removed is what actually came across.
At its head TUAS stands at 171 618 total and 96 507 code lines, the 96 KLOC quoted in the text. All
figures are measured on each repository’s develop branch, which is where the development history lives
— these repositories squash-merge into main, so measuring main would collapse years of work into a
handful of commits. thermal hydraulics rs is measured at commit 4d534af, the last before its code
was moved into TUAS on 2024-10-11 and the repository emptied. None of these repositories used an
agentic coding workflow. Every figure in this table is produced by kloc accounting.py, which walks
the repositories and their git histories directly; see Section A

            Repository                                 Period                      Total     Code    Active
                                                                                   lines     lines    days
            thermal hydraulics rs (predecessor         Jun 2023 – Oct 2024       111 437    59 808      144
            to TUAS)a [74]
            chem-eng-...-simulatora [75]               Oct 2023 – Apr 2024         8 848     4 802        9
            teh-o-prkea [76]                           Apr 2024 – Jun 2025        10 751     6 579       32
            tuas boussinesq solver (net-new)a          Oct 2024 – Jun 2026        76 672    44 453       69
            [3]
            tampines-steam-tablesb [72]                Jan 2025 – Jun 2026        79 990    56 082       98
            boon-layc [73]                             Jan 2026 – May 2026        15 765     9 574       30
            Baseline total                             2023 – 2026               303 463   181 298      367
a No AI assistance of any kind. b Minimal AI assistance, confined to root-finding solvers, via NUS AI-know. c Non-agentic

AI code generation for user interfaces and some Monte Carlo solvers, via NUS AI-know.


    Two repositories appear in Table XIV that were not named in the discussion above: teh-o-prke
[76], the point reactor kinetics package, and the chemical engineering real-time process control simulator
[75]. Both predate Outram Park and are vendored into it, so both belong in the baseline rather than in
the agentic tally. teh-o-prke is in turn the predecessor of the nee soon coupling layer. The process
control simulator dates from the author’s doctoral work and is the one baseline component carrying a
published verification and validation record, having been validated against Scilab in [2].
    The baseline reaches 181.3 KLOC of code by a different route to the running total in the text.
The text sums TUAS at its head (96 KLOC), tampines-steam-tables (56 KLOC) and boon-lay
(15 KLOC); the table separates thermal hydraulics rs from the TUAS work that followed it, counts
boon-lay at its 9.6 KLOC of code rather than its 15.8 KLOC total, and adds the two repositories above.
    Spread over 367 active days, the baseline works out at roughly 494 lines of code per working day.
This is the running average for code in Table XIV, with some help with NUS AI-know. Ranking the
repositories by that rate, as in Table XV, is more informative than the average alone: the pre-agentic
repositories span 206 to 572 lines per active day, a factor of roughly three, which is the ordinary variation
between projects of differing nature. That spread is the yardstick the agentic rate should be read against.




                                                           47
Table XV: Code lines per active day, each pre-agentic repository ranked fastest first, against the agentic
month. The spread among the pre-agentic repositories — roughly a factor of three, from 206 to 572 — is
the useful context for the agentic figure: it is the ordinary variation between projects of differing nature,
and it is far smaller than the gap to the agentic rate. The AI? column records only non-agentic assistance;
none of the pre-agentic repositories used an agentic workflow. Produced by kloc accounting.py; see
Section A

           Code lines    Repository                                     Non-agentic
        per active day                                                  AI assistance
                  644    tuas boussinesq solver (net-new)               none
                  572    tampines-steam-tables                          root-finding solvers only
                  534    chem-eng-...-simulator                         none
                  415    thermal hydraulics rs (predecessor to TUAS)    none
                  319    boon-lay                                       code generation
                  206    teh-o-prke                                     none
                  494    Pre-agentic baseline, all repositories         mixed
                6 069    outram-park-backend                            agentic


    Note also that the ranking does not line up with the amount of AI help received. The fastest reposi-
tory, tampines-steam-tables, had only root-finding solvers generated with NUS AI-know and noth-
ing more; the slowest, teh-o-prke, had none at all, and boon-lay, which had the most non-agentic
code generation of the three, sits second from the bottom. Whatever sets the pace of pre-agentic work,
chat-assisted code generation is not the dominant term.
    Now, if one were to consider the crates built with help from NUS-AI know via chat and code gener-
ation, the average is 525 lines of code per working day compared to 470 lines of code per working day
for the older crates. This is a 12% increase in productivity. Not all of it can be attributed to NUS-AI
know however, because the author has gotten more proficient in Rust programming via neovim and its
plugins in 2025-2026 as compared to 2023-2024. Hence, this is not a clean comparison. Moreover, the
nature of the crates differ. Therefore, not all lines of code are created equal. Hence, this should only be
treated as a ballpark figure.
    Hence, the pre-agentic ballpark for Rust based development was around 500 lines of code/active
day of coding. At that rate the agentically written portion of Outram Park, 175 997 lines, represents
about 352 engineer-days, and the full 181 298-line baseline about 362; the figure depends on which
body of code one takes as the thing being replaced. Assuming engineers are paid US$200 per day (a
conservative figure, as lower-bound estimates are about US$100,000/year [77], or about USD$273 per
day), the cost to replace Outram Park pre-agentically is in the range USD$70,000–73,000. This
range, rather than a single figure, is what the line counts support. Note also that this assumes all days
are used for coding. In reality, a software engineer or nuclear numerical simulation engineer would be
expected to regularly attend meetings and non coding related activites. Sometimes, rest is also required
to ensure coding is sustainable. This means that the figure cited here for human cost to replace is lower
than what it may be in real life.

Agentically Developed Source Code
The comparison becomes clearer in Table XVI, which gives the corresponding breakdown for outram-park-backend,
by crate, as of 2026-07-23. The repository holds 349 541 lines of Rust code across 26 crates; subtracting
the 173 544 lines of pre-agentic work vendored into it leaves 175 997 lines written agentically. That
subtracted figure is not an independent estimate: it is the baseline of Table XIV less the 7 754 code lines
that were written in thermal hydraulics rs and never carried across at spin-out. Those lines are
pre-agentic work and belong in the baseline, but they are not vendored into the backend and so cannot
be subtracted from it. The two tables otherwise partition the same body of code without overlap or omis-
sion, which is the arithmetic check on both. Classification follows each crate’s own declared provenance
in its Cargo.toml manifest.


                                                          48
Table XVI: Agentic lines of code in outram-park-backend by crate, 2026-06-19 – 2026-07-23. Code
lines exclude blank and comment-only lines. Translated crates are pure-Rust forks or ports of the named
upstream project and are independent works, not the official software. Extensions are the excess of a
vendored crate over its standalone pre-agentic original, and are credited here rather than to the baseline.
Every figure in this table is produced by kloc accounting.py from the repository pinned at commit
3130b38, because develop moves daily and a tip measurement could not be reproduced later; the
classification of each crate is the one editorial input, and is carried in the script beside each crate’s own
Cargo.toml description so it can be audited. See Section A.

             Crate                                                Upstream                    Code lines
             Translated or ported from an existing codebase
             njoy-outram-park-fork                                NJOY2016                         32 481
             outram-park-fork-coolprop                            CoolProp                         28 707
             outram-foam-appbuilder-lib                           OpenFOAM                         20 495
             outram-foam-basic-lib                                OpenFOAM                         15 691
             outram-mc-libs                                       OpenMC                           15 406
             outram-park-fork-pflotran                            PFLOTRAN                          7 939
             outram-foam-mesh                                     OpenFOAM                          6 218
             outram-blender                                       Blender                           4 769
             outram-park-fork-dwsim-libs                          DWSIM                             2 079
             outram-foam-turbulence-lib                           OpenFOAM                          1 717
             outram-foam-cli                                      OpenFOAM                            960
             Subtotal, translated                                                                136 462
             Originally written
             outram-park-digital-twin-engine                      —                                 8 651
             tampines                                             —                                 7 306
             kovan-tui                                            —                                 1 716
             kovan-cli                                            —                                 1 354
             njoy-tui (bin in njoy-outram-park-fork)              —                                 1 304
             kovan-codegen                                        —                                 1 267
             kovan-semantics                                      —                                 1 222
             outram-mc-tui (bin in outram-mc-libs)                —                                 1 202
             kovan-literature                                     —                                 1 114
             kovan-discovery                                      —                                   934
             kovan-common                                         —                                   617
             nee soon†                                            —                                   490
             Subtotal, original                                                                    27 177
             Agentic extensions to vendored pre-agentic crates
             tampines-steam-tables                                (own, pre-agentic)                7 150
             boon-lay                                             (own, pre-agentic)                3 680
             tuas boussinesq solver                               (own, pre-agentic)                  836
             teh-o-prke                                           (own, pre-agentic)                  692
             chem-eng-...-simulator                               (own, pre-agentic)                    0
             Subtotal, extensions                                                                  12 358
             Total agentic                                                                       175 997
† nee soon succeeds teh-o-prke in naming — the former Teh-O package — but its code is newly written; the point kinetics

module itself remains vendored as teh-o-prke.


    Three features of Table XVI bear on how the productivity figure should be read. First, 77 per cent
of the agentic output is translation rather than original design: porting an existing, already-debugged
numerical implementation into Rust is substantially faster per line than inventing one, and the headline
figure should not be read as 175 KLOC of novel engineering. Second, the 15 per cent that is original
is dominated by tooling and interface code, chiefly the KOVAN agent-facing utilities and the terminal
interfaces, rather than by new physics. Third, the agentic month produced 175 997 lines against a pre-
agentic baseline of 181 298 lines accumulated over roughly three years: as much code in one month as


                                                           49
in the preceding three years, which on a per-working-day basis is a factor of 12.3 — 6 069 code lines
per active day against 494. Both rates, and the composition underlying the first two points, are plotted
in Figure 15.




Figure 15: Rate and composition of code production. (a) Code lines per active day for each pre-agentic
repository, for the pre-agentic baseline as a whole, and for the agentic month. The aggregate is separated
by a rule because its denominator is the union of active dates across overlapping projects, not the sum of
the rows above it. (b) The agentic output split by provenance. Generated from the repositories and their
git histories by kloc accounting.py; the underlying figures are those of Tables XIV and XVI.

    Note also that the author is comparatively proficient with neovim and Rust, which if anything flatters
the pre-agentic baseline.
    Suppose one were to naively extrapolate this to Outram Park, where about 187 KLOC was written
within the span of one month. Note that this was not sustainable: the author fell ill repeatedly over
the course of the month. (please see health advisory) Suppose we took 2.5 months instead to produce
agentic code at a sustainable pace. Hence, the productivity with agentic coding is about 74.8 KLOC per
month. In other words, working agentically with Claude Code produced more KLOC than the author
would normally produce in a year. This would almost be 900 KLOC per year or a roughly 23 times
productivity gain as compared to manual + some AI chat bot assisted coding if one were to consider
Boon Lay.
    Whether we use the low bound of 12x or high bound of 23x, this reflects a one order of magnitude
productivity increase over pre-agentic AI coding.
    Hence, for agentic translation, the ballpark figure is about 6000 lines of code/active coding day.
Which means for human translation of codes (plus some new code generation), agentic AI via Claude
Code was about one order of magnitude faster than human coding. Assuming roughly the same amount
of 500 lines of code/active coding day for human translation, this is the same USD$70,000–73,000
replacement cost given above, arrived at from the translation side rather than from the line-count
baseline — not a further cost on top of it. This of course, assumes that there is a team with intimate


                                                   50
knowledge of Rust, C, C++ and Fortran which knows each of the nuclear science and engineering
domains enough to translate such codes and develop applications from it.

4.2.3   Ballpark Productivity Costs when using Agentic Coding
The work above was done under a flat-rate subscription (actually two, because both Claude Pro and
Claude Max were used). This totalled around USD$400 listed price, but Anthropic charged SGD$600
for both. There is worry that tokens will not always be cheap [78]. Hence, it is also of interest to see
whether the tokens used even when API is used, will outweigh the gains described in earlier sections.
    Table XVII shows the estimated token cost of Outram Park:

Table XVII: Token consumption and Anthropic API list-price cost of the agentic coding work on this
project, measured on one machine, as of 2026-07-23. The work was carried out under a flat-rate sub-
scription, so this is a counterfactual — what a reader reproducing it through the metered API would be
charged — and not an amount that was paid. Counts are taken from the Claude Code session transcripts,
which record the token usage the API itself reported for each call, deduplicated by message id; no figure
here is estimated. List prices were retrieved 2026-07-17. The total is a lower bound in two independent
ways. Transcripts are stored per machine with no synchronisation, so any machine not scanned is miss-
ing; and Claude Code prunes them on a rolling retention window (cleanupPeriodDays, thirty days
by default), so a later rerun returns a smaller total as old sessions expire. The transcripts counted span
2026-06-23 to 2026-07-23. Every cache write on record carries the 1-hour time-to-live and is there-
fore billed at 2.00× the input rate; none used the cheaper 1.25× five-minute tier. Produced by token
accounting.py, which reads the transcripts directly and emits this table; re-run it to update the num-
bers.

                Model                                         Billed         Billable    List-price
                                                            API calls         tokens    cost (USD)
                claude-opus-4-8                                3 778    1 396 968 434    $1 026.49
                claude-sonnet-5                                3 012    1 430 185 326     $512.10
                claude-sonnet-4-6                                813       84 970 645       $56.84
                claude-haiku-4-5-20251001                         54        2 810 324        $0.62
                Total                                          7 657    2 914 934 729    $1 596.05
                Same work, Sonnet 5 introductory pricing ($2/$10 per Mtok)               $1 425.35
                Same work, counterfactual with no prompt caching                        $11 670.78


   Two features of the bill also deserve comment, and are set out in Table XVIII.




                                                       51
Table XVIII: The same spend of Table XVII split by what was actually billed, measured on one machine,
as of 2026-07-23. Token volume and cost share disagree sharply, which is the characteristic shape of
a long agentic session: the context is re-read on nearly every turn, so cache reads dominate the token
count, and only the 0.10× read multiplier keeps them from dominating the bill by the same margin.
Generated output, a rounding error by volume, is a substantial fraction of the cost. Note that the five-
minute cache tier is unused — every write on record carries the 1-hour time-to-live and is billed at
2.00× the input rate rather than 1.25×. Prices are Anthropic API list, retrieved 2026-07-17; the work
itself was done under a flat-rate subscription, so these are counterfactual charges rather than money
paid, and they are a lower bound both across machines and in time — Claude Code prunes transcripts
on a thirty-day rolling window. The transcripts counted span 2026-06-23 to 2026-07-23. Produced by
token accounting.py; see Table XVII for the per-model totals.

          Billed as                   Priced at               Tokens        % of       Cost      % of
                                                                          tokens     (USD)       cost
          Cache read                  0.10× input        2 872 615 552    98.5%    $1 135.21    71.1%
          Cache write, 1 h TTL        2.00× input           33 044 451     1.1%     $284.26     17.8%
          Cache write, 5 min TTL      1.25× input                    0     0.0%        $0.00     0.0%
          Fresh input                 1.00× input            1 039 602     0.0%        $4.51     0.3%
          Output                      output rate            8 235 124     0.3%     $172.08     10.8%
          Total                                          2 914 934 729   100.0%    $1 596.05   100.0%


    Now, prior to 23 July, no proper token accounting was done. Therefore Table XVII would underes-
timate the cost of the tokens used to construct Outram Park agentically. However, taking the ballpark
figure of USD$1600 and adding a 10 times buffer, USD$16000, we would still be producing several
times the value with the code in Outram Park should it be constructed non-agentically. Comparing
USD$16,000 for approximate token cost to USD$70,000–73,000 for cost to replace, it would have
been far cheaper to use agentic coding to perform this task even at API costs. Therefore, Agentic Cod-
ing even with the higher API costs still has its value in longer term development of code bases and
open-source nuclear simulation frameworks such as Outram Park.
    Naturally, we must be judicious about the use of tokens in this manner. As the price of tokens
increase, one has to balance its costs against Manpower and the use of open source local AI models
available in ollama [79].

4.3     The Role of AI in Software Development
Many advocate for the use of AI, but how should AI be used? And how do humans still have relevance?
  Indeed, in the pre-AI era, we have:


                                   Human                           Code

Figure 16: Traditional software development workflow. The engineer directly develops, tests, and main-
tains the code.

      Whereas now, we have a newer code development model:




                                                    52
                                                                    Code
                               Human                                 +
                                                                Documentation



                                                 AI Agent

Figure 17: Modern human-in-the-loop development. AI agents assist implementation while humans
remain directly engaged with the code and documentation.

     With this new style of development, there have been arguments and questions raised on whether AI
will replace human beings [80], [81]. Moreover, there is great concern that even when humans use AI,
the result is cognitive atrophy [82]. We make the argument AI should augment human intelligence, not
replace it [83]. Herein, we describe the proper use of AI, where humans should not work in such a way
as to experience cognitive decline. This is the model used for developing Outram Park.
     Anecdotally, it was impossible for humans to just dump one prompt into Claude Code to result in
Outram Park. Outram Park was done with specific directions for AI, to translate open-source nuclear
codes from Fortran and C++ to Rust library by library. For each library, sufficient levels of domain
knowledge were required to guide the AI. This involvement increases where AI is asked to synthesise
new codes and solvers such as those seen in tampines-steam-tables. Without prior Thermodynamics
knowledge from the human prompter, AI would have wasted a good amount of tokens using the wrong
functions in classic hallucination [84]. Humans therefore are present and required to mitigate the hallu-
cination risks.
     It should also be noted that hallucination risks are lowered when there is a codebase of source
material. AI is after all a transformer at heart. It is able to hold onto large amounts of data and synthe-
sise something new based on the data. An interpolation or extrapolation perhaps, or as in literature a
stochastic parrot [85]. In today’s state of AI in 2024-2026, it is still doubtful whether Artificial General
Intelligence (AGI) exists [86]. For now, it is the author’s opinion to be sceptical of agentic AI capa-
bilities until otherwise proven. Therefore, we adopt the approach that AI is just (at least) a very good
stochastic parrot. Of course, a stochastic parrot is useful if one wants to do major refactoring of code,
where source code is verified correct, or to make GUIs of which plenty of working examples are already
available. However, when it comes to synthesising something new or novel, AI in today’s state may still
be a useful stochastic parrot, but still fall short of a human being. It is therefore up to the human being
to think creatively, innovatively and with a noble purpose in mind - to solve problems to make the life
of other human beings better.
     With this in mind, in Outram Park, all code is considered an incomplete draft unless humans validate
it and check it first. We do not adopt the practice that AI generated code is considered correct. This is
the wrong model:

                                                                                Code
                    Human                        AI Agent                        +
                                                                               Writing

Figure 18: Undesirable workflow in which the human delegates both implementation and understanding
to an AI system.

   Instead, for Outram Park, AI was used to speed up the drafting and code debugging stage. Thereafter,
humans would then manually check the validation stage with verified V&V data:




                                                    53
                                   Draft Stage (Large AI Speedup)

                                                                                Code
                    Human                       AI Agent                         +
                                                                               Writing



                      Verification Stage (Minimal AI Speedup)

                                                                Code

                    Human

                                                              Writing

Figure 19: Human-in-the-loop development model adopted by OUTRAM PARK. AI provides signifi-
cant acceleration during drafting and implementation, while verification and validation remain primarily
human responsibilities.

    Writing and coding were done with AI help, but the concepts were not from AI. As mentioned in
the Methods section, AI was used to adapt language but not come up with new scientific concepts [54].
Humans must verify code is correct and can be usable without AI help.
    In fact, the humans had to guide the AI throughout the agentic debugging of the TampinesSteamAr-
ray HEM solver. Reaching a stable solution took months spent reading about pressure-based solvers,
density-based solvers and choked flow; that background is what made it possible to direct the agent
effectively rather than merely to generate more code. For AI-assisted agentic development, the domain
knowledge and engineering experience of the human remain indispensable to obtaining effective and
accurate solutions.
    It is useful in the new model to think of AI, deterministic code and humans as performing three
complementary roles in this process:

    • Human: manager, responsible owner, and verifier of code and coding agents

    • Code: Does deterministic calculations based on human and agent input

    • AI Agent: Useful Stochastic Parrot able to draw from large libraries of data and codebases to draft
      templates and codes for human use

    AI Agents have limitations, due to their stochastic nature, and in essence they are stochastic parrots,
only able to regurgitate information with some degree of randomness. Humans are best at innovation
and creative thinking but are not able to hold libraries of information in short term memory. Codes are
accurate as far as they are programmed to be, but reproduce output deterministically much better than
human beings. Thus they have a capability to be more ”correct” in calculating a value than a human and
AI-LLM, and for potentially much lower computational cost for the desired accuracy.
    To use AI agents effectively, the human agentic engineer should delegate tasks to himself, the AI
agent or code based on these strengths. Codes can reproduce and calculate cross sections effectively, but
should not be asked to innovate or make value judgements. AI can create new versions of codes based
on older versions much better than a human, but may not innovate on new ideas outside their existing
database as well as a human. Humans should no longer do code refactoring by hand, AI can do better, or
do calculations by hand, as code is faster and more accurate. But determining which problem to solve,
how to innovate and what value and moral judgements should be exclusively within the domain and
responsibility of humans. As Einstein mentioned, ”formulation of a problem is far more essential than

                                                    54
its solution, which may be merely a matter of . . . skill. To raise new questions, new possibilities, to
regard old problems from a new angle, requires creative imagination and marks real advance.” [87]
     In essence, delegate work to the entity best suited to solve it, but let the human define the
problem well first.

4.4   Health Advisory
Agentic coding can be quite taxing, as seen in Figure 20:




Figure 20: Commit by hours of the day from 19 jun 2026 to 10 july 2026, the period before working
hour guardrails were adopted. Times are in GMT+8

    The author wished to maximise token usage, and consequently became anxious about drawing fully
on the quota so as to extract the full value of the Claude Code subscription. Sleep quality suffered as a
result. This is known in literature as technostress [88], [89]. With long period of poor sleep quality, long
hours of agentic coding due to hyperfocus [90], [91], it led to higher levels of cognitive fatigue [92],
[93] and decision fatigue [94]. Stresses also led to lower immunity [95], [96], [97] which would likely
have contributed to the author’s longer recovery periods from a sore throat.
    Of course, we do not suggest AI-assisted coding causes more illness, but the AI-assisted developer
should do well to ensure that health is taken care of so that coding is done sustainably. To ensure this,
outram-park-backend has instructions and warnings in its repository to ensure agentic coding is done
only during specified working hours as seen in Appendix D.


5     Future Work
5.1   Verification and Validation
The V&V efforts in this research log are quite preliminary. Claude has helped develop some of the cases
here for Outram Foam and the reduced order Tampines Steam Array HEM solver derived from Outram-
Foam rhoPimpleFoam and rhoCentralFoam. AI assisted debugging has resulted in a deterministic solver
which was able to reproduce these results with some reduced ringing.
    However, it remains to be seen if such fixes can work outside the domain of the Edwards test. If the
exact same HEM solver could work for the Marviken tests [98], as well as natural circulation tests [99],
then one can know that this solver works sufficiently well and did not just receive random AI fixes that


                                                    55
made it useful for Edwards but useless for other nuclear engineering use cases. One useful case is that
of Zhang and Brooks [100], [101] where nodalisation and results are given in the paper.
    Moreover, the void fraction validation is not yet complete as there is significant ringing even with
the HybridAllMach Solver. Complete resolution of this problem is reserved for future work, whether
using an improved HEM solver, or driftFlux or 6 equation model.

5.2   Thermal Hydraulics
The next milestone for 1D thermal-hydraulics is the drift-flux and six-equation model, which is the
natural next frontier of experimentation for the Edwards test.

5.3   Neutronics and Nuclear Data
As mentioned earlier, thermal-hydraulics is only part of Outram Park. Neutronics is covered in a com-
panion paper to follow shortly after the thermal-hydraulics paper is published. Much remains to be done
in the realm of neutronics. This includes the chord length sampling methods used in TRISO pebble beds
and methods suitable for liquid fuelled molten salt reactors. Depletion and burnup are also important as
OpenMC covers them. The port known as Outram MC will be discussed in future.

5.4   Materials
Outram Park as it stands in July 2026 is lacking much in fuel performance and materials simulation.
These are important for nuclear safety evaluations and construction of proper digital twins. Initial ports
of Offbeat, the foamForNuclear code built along with GeN-Foam [102], have been partially completed
but no validation has been done yet. Moreover, corium interaction studies, which have been done in
OpenFOAM [103] have yet to be ported, studied and validated yet.
    These are in the realm of future work and will require more manpower.

5.5   Source Term and Dispersion
For source term and dispersion studies, these are important for nuclear safety analysis. TRISO Atops
has already been ported into Outram Park, but there is little else in this arena as of July 2026.

5.6   Digital Twin Work
Initial FHR simulators have already been done in Outram Park prior to agentic coding.
     Figure 21 shows the pre-agentic UI of the simulator:




                                                   56
             Figure 21: FHR Educational Simulator v1/v2 (still undergoing development)

    The models in figure 21, rudimentary and require improvement. This is because the steam turbine
cycle is merely a steady state Rankine cycle loop without critical heat flux (CHF) or integration of the
transient TampinesSteamArray developed in this work. The aesthetics, User Interface and physics need
to be incorporated into these simulators to improve it. Moreover, LWR and HTGR simulators need to
be developed in order for Outram Park to be applicable to these reactors.


6    Conclusions
In this work, we present the use of Agentic AI in translating libraries, performing initial V&V and its role
in solver development. Cost considerations and value analysis of Agentic AI have also been discussed
in the context of Outram Park development in June-July 2026.
    AI-assisted Agentic Development has been greatly accelerated with the use of Claude Pro (1 year)
and Claude Max (1 month) subscriptions totalling SGD$600, and the value returned is roughly two or-
ders of magnitude that amount. Even when considering raw API costs, Agentic AI could potentially
return value approximately one order of magnitude cheaper compared to hiring a full software develop-
ment team with nuclear expertise.
    Agentic development workflows have been shown to greatly improve speed and productivity, but we
have shown in this research log, in the development of tampines-steam-tables and TampinesSteamArray
HEM solver, that human familiarity with the numerical solution and physics of the problem cannot
be 100% substituted by AI. However, AI-assisted agentic translation and debugging have served to
greatly enhance the speed and efficiency of iterative development workflows especially when the humans
operating the AI Agents have specific domain knowledge and coding knowledge of the systems at hand.
This is once again in line with what the Singapore government has been saying, that AI should not
replace human beings, but augment them [17], [70].
ACKNOWLEDGMENTS

This work was performed with funding support from the Singapore Nuclear Research and Safety Insti-
tute (SNRSI). NRF Funding number (A-8002968-00-00). The author also thanks colleagues at SNRSI
for introducing him to vibe coding fundamentals and Claude Code, as well as many useful constructive
conversations. These include, Goh Zhi Zheng, Darryl Foo, Than Yan Ren, Seow Chun Yong, Isaac Yap
and Vitesh. Thanks to ZheXi Guo for introducing Zhang and Brooks validation cases, which are now
part of future work. The author also thanks SNRSI Director Prof Chung Keng Yeow and SNRSI CEO

                                                    57
Low Xin Wei continued support of Outram Park’s various libraries and advocating the use of Artificial
Intelligence in general. The author further thanks SNRSI CEO Low Xin Wei for permitting the Claude
Code subscription, which the author had initially purchased at his own expense for personal use, to be
claimed as a work expense once its value to Outram Park development had been demonstrated.


7    CRediT Authorship Contribution Statement
Theodore Kay Chen Ong: Conceptualization; Methodology; Software; Validation; Formal analysis;
Investigation; Data curation; Visualization; Writing — original draft; Writing — review & editing;
Project administration. Sicong Xiao: Supervision; Writing — review & editing.


8    Declaration of Generative AI and AI-assisted Technologies in the Manuscript
     Preparation Process
During the preparation of this work, the authors used Anthropic Claude Code (Opus and Sonnet models
primarily, with Haiku models for lighter-weight tasks such as V&V memo drafting, LaTeX table gener-
ation, and case run orchestration) for agentic porting of OpenFOAM, NJOY, and CoolProp source code
into Rust under a strict provenance-tracking protocol, and for authoring Rust utility code that mechani-
cally generates figures and tables from author-verified numerical data. The authors also used Microsoft
Enterprise Copilot, Claude Code and ChatGPT as a sounding board for discussing methodology, for
literature search assistance, for cross-checking references, for assistance with LATEX table syntax and
matplotlib plotting code, and for critique and feedback on hand-written Singlish draft prose. All refer-
ences identified with AI assistance were independently verified by the authors against primary sources.
The National University of Singapore’s institutional AI assistant (NUS AI Know), which routes user
prompts to Anthropic Claude, OpenAI ChatGPT, and Google Gemini backends under institutional data-
governance controls, was evaluated but not adopted for this project: at the time of use it operated as a
conversational assistant only, without the ability to autonomously read, edit, run, and iterate on a multi-
file Rust workspace, which was required for the agentic porting scale of this work. AI tools were used
extensively in the preparation of the manuscript text: the authors drafted informal engineering notes
and technical brainstorming material, in part in Singlish (Singapore Colloquial English), and used AI
assistance to convert these into publication-ready academic prose. The underlying technical content,
analysis, interpretation, and conclusions are the authors’ own; AI assistance operated on the expression
of that material rather than its substance, and every AI-revised passage was reviewed and edited by the
authors. All AI-generated code was reviewed, tested, and integrated into the Outram Park repository
under GPLv3 provenance-tracking conventions. The authors reviewed all AI-assisted output and take
full responsibility for the content of the publication. Further detail on how AI tools were used, including
a verbatim example of the Singlish-to-academic-prose workflow, is given in the methods section.
     The productivity comparison reported in this work is drawn against a baseline of four earlier repos-
itories by the same author, whose AI-use status differs and is stated here for transparency. thermal
hydraulics rs (June 2023 to October 2024) and tuas boussinesq solver (October 2024 to June
2026) were developed without AI assistance of any kind. tampines-steam-tables (January 2025 to
June 2026) used minimal AI assistance, confined to root-finding solvers and similar numerical routines.
boon-lay (January to May 2026) used non-agentic AI code generation, for user interface code and
some Monte Carlo solvers, alongside conversational assistance. Three of boon-lay’s data dependen-
cies — openmc-endf-8-depletion-lib-a [104], -lib-b [105] and fission-yields-data [106]
— require separate comment. Their serialisation parsers were generated largely by OpenAI ChatGPT-5
(non-agentic, conversational) with author corrections. The bulk of each repository, however, is ENDF/B-
VIII.0 decay-chain and fission-yield data taken verbatim from the OpenMC project; the author separated
this data by nuclide and wrapped it into Rust functions by hand in Neovim. It is therefore neither au-


                                                    58
thored logic nor AI-generated code, but reorganised public reference data, and it is excluded from the
productivity accounting on that basis. None of these repositories employed an agentic coding workflow,
in which an AI tool autonomously reads, edits, runs, and iterates on a multi-file workspace. The com-
parison reported here is therefore between agentic development and non-agentic development, where
the latter comprises both unassisted manual programming and conversational AI assistance. It is not a
comparison between AI-assisted and AI-free development, and should not be read as one. This distinc-
tion is deliberate: it isolates the agentic workflow, rather than the availability of a language model, as
the variable under examination.


References
  [1]   Energy Market Authority, Singapore to undertake IAEA review by international experts to as-
        sess its ability to make informed decision on nuclear energy deployment, Joint Media Release,
        Ministry of Trade and Industry, Ministry of Sustainability and the Environment, Energy Mar-
        ket Authority, and National Environment Agency, Announced by Prime Minister Lawrence
        Wong at EMA’s 25th Anniversary Gala Dinner, May 2026. Accessed: Jul. 6, 2026. [Online].
        Available: https://www.ema.gov.sg/news- events/news/media- releases/2026/
        Singapore-to-Undertake-IAEA-Review-by-International-Experts-to-Assess-
        Its-Ability-to-Make-Informed-Decision-on-Nuclear-Energy-Deployment
  [2]   T. K. C. Ong, Digital Twins as Testbeds for Iterative Simulated Neutronics Feedback Controller
        Development. University of California, Berkeley, 2024.
  [3]   T. K. C. Ong, S. Xiao, and P. F. Peterson, Tuas boussinesq solver, https://github.com/
        theodoreOnzGit/tuas_boussinesq_solver, 2024.
  [4]   T. K. C. Ong, Development of an Isothermal-Flow Digital Twin for the Compact Integral Effects
        Test. University of California, Berkeley, 2023.
  [5]   T. K. C. Ong, S. Xiao, and P. F. Peterson, “An open-source thermo-hydraulic uniphase advection
        and convection solver for salt flows (tuas),” International Journal of Advanced Nuclear Reactor
        Design and Technology, vol. 6, no. 4, pp. 281–301, 2024.
  [6]   T. Ong, S. Xiao, and P. Peterson, “Validation of the open source tuas using coupled natural
        circulation data from ciet,” Aug. 2025.
  [7]   H. Jasak, “Openfoam: Open source cfd in research and industry,” International journal of naval
        architecture and ocean engineering, vol. 1, no. 2, pp. 89–94, 2009.
  [8]   C. Fiorina, I. Clifford, M. Aufiero, and K. Mikityuk, “Gen-foam: A novel openfoam® based
        multi-physics solver for 2d/3d transient analysis of nuclear reactors,” Nuclear Engineering and
        Design, vol. 294, pp. 24–37, 2015.
  [9]   P. K. Romano, N. E. Horelik, B. R. Herman, A. G. Nelson, B. Forget, and K. Smith, “Openmc:
        A state-of-the-art monte carlo code for research and development,” Annals of Nuclear Energy,
        vol. 82, pp. 90–97, 2015.
 [10]   R. E. MacFarlane, D. W. Muir, R. M. Boicourt, A. C. Kahler, and J. L. Conlin, “The NJOY
        Nuclear Data Processing System, Version 2016,” Los Alamos National Laboratory, Technical
        Report LA-UR-17-20093, 2017. [Online]. Available: https : / / www . osti . gov / biblio /
        1338791
 [11]   P. Fritzson et al., “The openmodelica integrated environment for modeling, simulation, and
        model-based development,” Modeling, Identification and Control, vol. 41, no. 4, pp. 241–295,
        2020.




                                                   59
[12]   K. Tangsriwong, P. Lapchit, T. Kittijungjit, T. Klamrassamee, Y. Sukjai, and Y. Laoonual, “Mod-
       eling of chemical processes using commercial and open-source software: A comparison between
       aspen plus and dwsim,” in IOP Conference Series: Earth and Environmental Science, IOP Pub-
       lishing, vol. 463, 2020, p. 012 057.
[13]   D. Gaston, C. Newman, G. Hansen, and D. Lebrun-Grandie, “Moose: A parallel computa-
       tional framework for coupled systems of nonlinear equations,” Nuclear Engineering and Design,
       vol. 239, no. 10, pp. 1768–1778, 2009.
[14]   A. Novak, P Shriwise, P. Romano, R Rahaman, E Merzari, and D Gaston, “Coupled monte carlo
       transport and conjugate heat transfer for wire-wrapped bundles within the moose framework,”
       Nuclear Science and Engineering, vol. 197, no. 10, pp. 2561–2584, 2023.
[15]   L. Zou, R. Hu, and A. Charpentier, “Sam code validation using the compact integral effects test
       (ciet) experimental data,” Argonne National Laboratory (ANL), Argonne, IL (United States).
       Advanced . . ., Tech. Rep., 2019.
[16]   A. E. Slaughter, D. R. Gaston, C. J. Permann, D. Andrš, J. A. Miller, and J. W. Peterson, “Code
       documentation, and automation for Nuclear Quality Assurance,” Nuclear Technology, vol. 207,
       no. sup1, S109–S116, 2021. DOI: 10.1080/00295450.2021.1873215 [Online]. Available:
       https://inldigitallibrary.inl.gov/sites/STI/STI/Sort_24568.pdf
[17]   L. Wong, Singapore Budget 2026 Statement, Section C: Harness AI as a Strategic Advantage,
       Official Budget Speech, Ministry of Finance, Presented by Prime Minister and Minister for
       Finance Lawrence Wong on February 12, 2026, Feb. 2026. [Online]. Available: https : / /
       singaporebudget.gov.sg
[18]   Infocomm Media Development Authority, Major push to upskill 40,000 tech professionals over
       the next three years and grow the next-generation of tech leaders as IMDA doubles down on
       AI readiness, Official Press Release, Infocomm Media Development Authority, Government of
       Singapore, May 2026. Accessed: Jul. 6, 2026. [Online]. Available: https://www.imda.gov.
       sg/resources/press-releases-factsheets-and-speeches/press-releases/2026/
       major-push-to-upskill-tech-professionals-and-grow-the-next-generation-
       of-tech-leaders
[19]   L. Huang et al., “A survey on hallucination in large language models: Principles, taxonomy,
       challenges, and open questions,” ACM transactions on information systems, vol. 43, no. 2, pp. 1–
       55, 2025.
[20]   X. Sun, D. Ståhl, K. Sandahl, and C. Kessler, “Quality assurance of llm-generated code: Ad-
       dressing non-functional quality characteristics,” Journal of Systems and Software, p. 112 885,
       2026.
[21]   U.S. Nuclear Regulatory Commission, “Advancing the use of artificial intelligence at the u.s.
       nuclear regulatory commission,” U.S. Nuclear Regulatory Commission, Tech. Rep. SECY-24-
       0035, Apr. 2024, ADAMS Accession No. ML24086A002. [Online]. Available: https://www.
       nrc.gov/docs/ML2408/ML24086A002.pdf
[22]   T. Zhang, Z. Liu, Y. Xin, and Y. Jiao, “MooseAgent: A LLM based multi-agent framework for
       automating MOOSE simulation,” arXiv preprint arXiv:2504.08621, 2025. DOI: 10 . 48550 /
       arXiv.2504.08621
[23]   S. Cao and Z. Chi, “Distribution of singular data generated by compact forced Navier–Stokes
       blowup,” arXiv preprint arXiv:2609.10262, 2026, Withdrawn. DOI: 10.48550/arXiv.2609.
       10262
[24]   C. Zhao and A. Cho, “How an AI math breakthrough ignited a controversy,” Science, Sep. 2026.
       [Online]. Available: https : / / www . science . org / content / article / how - ai - math -
       breakthrough-ignited-controversy


                                                 60
[25]   “AI companies must work with the research community to protect attribution,” Nature, vol. 657,
       p. 573, Sep. 2026. DOI: 10.1038/d41586-026-02886-7
[26]   C. Bhave et al., “Bridging the gap on ai-assisted scientific software development through trans-
       parency and traceability,” arXiv preprint arXiv:2605.17675, 2026.
[27]   T. K. C. Ong, Outram Park backend: Open-source TRAnsient Multi-Phase Advanced Reactor
       simulator Kit, https : / / github . com / theodoreOnzGit / outram - park - backend, Li-
       censed GPL-3.0. Repository created 2024-11-25; commit 66ae6ad on main, accessed 2026-07-
       23, 2026.
[28]   I. Cereijo and J. Chapela Martı́nez, LINGOT Is Not a Guitar-Only Tuner: A universal musical
       instrument tuner, Non-GNU project hosted at Savannah, GPL-2.0-or-later license, Original C
       source code available at https://git.savannah.nongnu.org/git/lingot.git. Version
       1.1.0 released May 2020, adding strobe display and experimental features., 2020. Accessed:
       Jul. 6, 2026. [Online]. Available: http://lingot.nongnu.org/
[29]   K. C. T. Ong, lingot tuner rust: A Rust rewrite of the LINGOT musical instrument tuner us-
       ing Claude Code, GitHub repository, GPL-3.0 license, Rust rewrite of the original C-based
       LINGOT tuner (Cereijo and Chapela). First agentic-porting demonstration preceding Outram
       Park; 38 passing unit tests, verified on real guitar hardware. Also available on crates.io as
       lingot-tuner., Jun. 2026. Accessed: Jul. 6, 2026. [Online]. Available: https://github.
       com/theodoreOnzGit/lingot_tuner_rust
[30]   K. C. T. Ong, Vibe coding: Rewriting LINGOT in Rust with Claude Code, Video series, Theo
       Ong Science and Engineering YouTube channel, Four-part video series documenting the end-to-
       end agentic Rust port of LINGOT: (1) initial layered implementation, (2) CLI tuner and guitar
       test, (3) GUI development and token exhaustion, (4) GUI touchups and testing. Approximately 2
       hours total recorded workflow evidence., Jun. 2026. Accessed: Jul. 6, 2026. [Online]. Available:
       https://www.youtube.com/watch?v=_CTuoYE0gEQ
[31]   S. Gupta, K. Kamalakkannan, M. Moraru, G. Shipman, and P. Diehl, “From legacy fortran to
       portable kokkos: An autonomous agentic ai workflow,” arXiv preprint arXiv:2509.12443, 2025.
[32]   S. Kailasa and T. Betcke, “Mostly painless scientific computing with rust,” in SC ACM Student
       Research Competition Posters. The International Conference for High Performance Computing,
       Networking, Storage, and Analysis, 2022.
[33]   S. Mangul et al., “Recommendations to enhance rigor and reproducibility in biomedical re-
       search,” GigaScience, vol. 9, no. 6, 2020. DOI: 10.1093/gigascience/giaa056
[34]   L. A. Barba, “Defining the role of open source software in research reproducibility,” arXiv
       preprint arXiv:2204.12564, 2022. DOI: 10.48550/arXiv.2204.12564
[35]   D. Spinellis et al., “Evaluating the quality of open source software,” Electronic Notes in Theo-
       retical Computer Science, vol. 233, pp. 5–28, 2009.
[36]   A. Meneely and L. Williams, “Secure open source collaboration: An empirical study of linus’
       law,” in Proceedings of the 16th ACM Conference on Computer and Communications Security,
       2009, pp. 453–462. DOI: 10.1145/1653662.1653717
[37]   Linux Kernel Developers, CVEs, The Linux Kernel Documentation, Accessed September 2026,
       2026. [Online]. Available: https://www.kernel.org/doc/html/latest/process/cve.
       html
[38]   Linux Kernel Developers, Security bugs, The Linux Kernel Documentation, Accessed Septem-
       ber 2026, 2026. [Online]. Available: https : / / www . kernel . org / doc / html / latest /
       process/security-bugs.html
[39]   J. Liu, X. Zhao, X. Shang, and Z. Shen, “Dive into claude code: The design space of today’s and
       future ai agent systems,” arXiv preprint arXiv:2604.14228, 2026.

                                                 61
[40]   D. P. Schmidt, S. Gopalakrishnan, and H. Jasak, “Multi-dimensional simulation of thermal non-
       equilibrium channel flow,” International Journal of Multiphase Flow, vol. 36, no. 4, pp. 284–
       292, 2010. DOI: 10.1016/j.ijmultiphaseflow.2009.11.012
[41]   D. P. Schmidt, HRMFoam: Homogeneous Relaxation Model solver for OpenFOAM, GitHub
       repository, GPL-3.0 license, OpenFOAM-based solver implementing the homogeneous relax-
       ation model for two-phase flow with thermal non-equilibrium. Accessed: Jul. 6, 2026. [Online].
       Available: https://github.com/davidpschmidt/HRMFoam
[42]   W. Wagner and H.-J. Kretzschmar, International steam tables: Properties of water and steam
       based on the industrial formulation IAPWS-IF97. Springer, 2008.
[43]   Y. A. Cengel and M. A. Boles, “Thermodynamics: An engineering approach,” Sea, vol. 1000,
       no. 8862, pp. 287–293, 2002.
[44]   B. El Hefni and D. Bouskela, Modeling and Simulation of Thermal Power Plants with Ther-
       moSysPro: A Theoretical Introduction and a Practical Guide. Springer International Publishing,
       2019, ISBN: 978-3-030-05104-4. DOI: 10.1007/978-3-030-05105-1
[45]   W. Veytsman, S. Zhai, C. Ding, and A. B. Sefkow, “Rewrite it in rust: A computational physics
       case study,” arXiv preprint arXiv:2410.19146, 2024.
[46]   N. J. Higham, Accuracy and Stability of Numerical Algorithms, 2nd. Philadelphia, PA: Society
       for Industrial and Applied Mathematics (SIAM), 2002, ISBN: 9780898715217.
[47]   I. S. Duff, R. G. Grimes, and J. G. Lewis, “Sparse matrix test problems,” ACM Transactions on
       Mathematical Software (TOMS), vol. 15, no. 1, pp. 1–14, 1989. DOI: 10.1145/58846.58847
[48]   Matrix Market, NNC261: Nuclear reactor neutron diffusion matrix, https : / / math . nist .
       gov/MatrixMarket/data/Harwell-Boeing/nucl/nnc261.html, Harwell–Boeing sparse
       matrix collection, National Institute of Standards and Technology (NIST). Accessed 2026-07-
       16, 1995.
[49]   F. J. Moody, “Maximum discharge rate of liquid-vapor mixtures from vessels,” General Elec-
       tric Co., San Jose, CA (United States). BWR Projects Dept., Tech. Rep. NEDO-21052, 1975.
       [Online]. Available: https://www.osti.gov/servlets/purl/7309475
[50]   P. Saha, “A review of two-phase steam-water critical flow models with emphasis on thermal
       nonequilibrium,” Brookhaven National Laboratory, Upton, NY, Tech. Rep. NUREG/CR-0417,
       BNL-NUREG-50907, 1978.
[51]   GraphReader, GraphReader: Online tool for extracting values from image-based graphs and
       plots, https://www.graphreader.com/, Used to digitise reference curves from published
       figures. Accessed 2026-07-16.
[52]   C. Price and B. Robertson, “Golden section search,” in Encyclopedia of Engineering Optimiza-
       tion and Heuristics, Springer, 2012, pp. 1–4.
[53]   N. S. Ningsih and F. Rahman, “Exploring the unique morphological and syntactic features of
       Singlish (Singapore English),” Journal of English in Academic and Professional Communica-
       tion, vol. 9, no. 2, pp. 72–80, 2023. DOI: 10.25047/jeapco.v9i2.3933
[54]   Z. Lin, “Techniques for supercharging academic writing with generative ai,” Nature Biomedical
       Engineering, vol. 9, pp. 426–431, 2025. DOI: 10.1038/s41551-024-01185-8
[55]   Elsevier, Annals of nuclear energy: Guide for authors, https://www.sciencedirect.com/
       journal / annals - of - nuclear - energy / publish / guide - for - authors, Elsevier. Ac-
       cessed 2026-07-16, 2026.
[56]   Elsevier, Generative AI policies for journals, https://www.elsevier.com/about/policies-
       and- standards/generative- ai- policies- for- journals, Policy updated June 2026.
       Accessed 2026-07-16, 2026.


                                                62
[57]   A. Alansari and H. Luqman, “Large language models hallucination: A comprehensive survey,”
       Computer Science Review, vol. 61, p. 100 970, 2026.
[58]   D. Hook and D. Kelly, “Testing for trustworthiness in scientific software,” in 2009 ICSE work-
       shop on software engineering for computational science and engineering, IEEE, 2009, pp. 59–
       64.
[59]   Anthropic, Claude pricing, https : / / claude . com / pricing, Claude Pro and Claude Max
       subscription tiers; Claude Code included. Accessed 2026-07-16, 2026.
[60]   U. Ghia, K. N. Ghia, and C. Shin, “High-re solutions for incompressible flow using the navier-
       stokes equations and a multigrid method,” Journal of computational physics, vol. 48, no. 3,
       pp. 387–411, 1982.
[61]   OpenCFD Ltd., 2.1 lid-driven cavity flow, https://www.openfoam.com/documentation/
       tutorial- guide/2- incompressible- flow/2.1- lid- driven- cavity- flow, Open-
       FOAM Tutorial Guide. Accessed 2026-07-16, 2026.
[62]   E. F. Toro, Riemann solvers and numerical methods for fluid dynamics: a practical introduction,
       3rd. Springer Science & Business Media, 2013.
[63]   G. A. Sod, “A survey of several finite difference methods for systems of nonlinear hyperbolic
       conservation laws,” Journal of Computational Physics, vol. 27, no. 1, pp. 1–31, 1978. DOI:
       10.1016/0021-9991(78)90023-2
[64]   O. A. Marzouk, “The Sod gasdynamics problem as a tool for benchmarking face flux construc-
       tion in the finite volume method,” Scientific African, vol. 10, e00573, 2020. DOI: 10.1016/j.
       sciaf.2020.e00573
[65]   Castro development team, Verification: Sod’s problem and other shock tube problems, https:
       //amrex-astro.github.io/Castro/docs/Verification.html#sods-problem-and-
       other-shock-tube-problems, Castro documentation. Accessed 2026-07-20, 2024.
[66]   P. Wu, Y. Ren, M. Feng, J. Shan, Y. Huang, and W. Yang, “A review of existing SuperCritical
       Water reactor concepts, safety analysis codes and safety characteristics,” Progress in Nuclear
       Energy, vol. 153, p. 104 409, 2022. DOI: 10.1016/j.pnucene.2022.104409
[67]   A. R. Edwards and T. P. O’Brien, “Studies of phenomena connected with the depressurization
       of water reactors,” Journal of the British Nuclear Energy Society, pp. 125–135, 1970.
[68]   C. J. Greenshields and H. G. Weller, Notes on Computational Fluid Dynamics: General Prin-
       ciples, First. CFD Direct Ltd, 2022, ISBN: 978-1-3999-2078-0. [Online]. Available: https :
       //doc.cfd.direct/notes/cfd-general-principles
[69]   H. Jasak, “Error analysis and estimation for the finite volume method with applications to fluid
       flows,” Department of Mechanical Engineering, Ph.D. dissertation, Imperial College of Science,
       Technology and Medicine, University of London, 1996.
[70]   S. L. Tan, Speech by Minister for Manpower Dr Tan See Leng at Ministry of Manpower Com-
       mittee of Supply 2026, Official Speech, Ministry of Manpower, Government of Singapore, Par-
       liament House, Delivered 3 March 2026; published on the MOM website 5 June 2026, Mar.
       2026. Accessed: Jul. 23, 2026. [Online]. Available: https://www.mom.gov.sg/newsroom/
       speeches/2026/0303-minister-speech-for-cos-2026
[71]   B. W. Boehm, Software Engineering Economics. Englewood Cliffs, NJ: Prentice-Hall, 1981,
       ISBN : 0-13-822122-7.




                                                 63
[72]   T. K. C. Ong, Tampines-steam-tables: In house steam tables for the Thermo-hydraulic Artificial
       intelligence Multi-Phase INtegrated Emulator System (TAMPINES) solver, https://github.
       com/theodoreOnzGit/tampines-steam-tables, Licensed GPL-3.0. Developed 2025-01-
       21 to 2026-06-15 with minimal AI assistance, confined to root-finding solvers and similar rou-
       tines, and without an agentic coding workflow; 941 commits over 96 active days, 56,318 lines
       of Rust. Commit 086167d (2026-06-15) is the final state of the manual development era, imme-
       diately preceding the addition of agentic tooling configuration. Accessed 2026-07-23, 2026.
[73]   T. K. C. Ong, Boon-lay: BOmbardment Open source Nuclide simulation Laboratory Algorithm
       for Yields (BOON LAY), https : / / github . com / theodoreOnzGit / boon - lay, Licensed
       GPL-3.0. Developed 2026-01-14 to 2026-05-12; 410 commits over 30 active days, 9,574 lines
       of Rust. Written with non-agentic AI assistance, including AI code generation for user interface
       code and some Monte Carlo solvers, but no agentic coding workflow; the repository carries no
       agentic-tooling configuration. Accessed 2026-07-23, 2026.
[74]   T. K. C. Ong, Thermal hydraulics rs: A thermal hydraulics library primarily for the Compact
       Integral Effects Test (CIET) and the Fluoride Salt Cooled High Temperature Reactor (FHR),
       https://github.com/theodoreOnzGit/thermal_hydraulics_rs, Licensed GPL-3.0.
       Predecessor of tuas boussinesq solver; developed 2023-06-27 to 2024-10-14 without AI
       assistance of any kind. Commit bf52af0 (2024-10-07) is the last state before the library was
       spun out into TUAS and this repository reduced to a stub. Accessed 2026-07-23, 2024.
[75]   T. K. C. Ong, Chem-eng-real-time-process-control-simulator: A real-time process control simu-
       lator library, https://github.com/theodoreOnzGit/chem-eng-real-time-process-
       control-simulator, Licensed Apache-2.0. Developed 2023-10-26 to 2024-04-29 during the
       author’s doctoral work, entirely by hand and without AI assistance of any kind; 9 active days,
       4,802 lines of Rust. Verified and validated against Scilab, as documented in the author’s dis-
       sertation. Vendored unchanged into Outram Park, with no agentic-era modification. Accessed
       2026-07-23, 2024.
[76]   T. K. C. Ong, Teh-o-prke: Point reactor kinetics equations module for the Teh-O package,
       https : / / github . com / theodoreOnzGit / teh - o - prke, Licensed GPL-3.0. Developed
       2024-04-12 to 2025-06-26 entirely by hand, without AI assistance of any kind; 32 active days,
       6,602 lines of Rust. Predecessor of the nee soon coupling layer in Outram Park. Accessed
       2026-07-23, 2025.
[77]   B. Veseli, F. Dalipi, F. Idrizi, S. Luma-Osmani, and G. Ajvazi, “Navigating career paths: Pre-
       dictive modelling of salary trends of data engineers,” in Pattern Recognition and Artificial In-
       telligence: Selected papers from the 6th Mediterranean Conference on Pattern Recognition and
       Artificial Intelligence (MedPRAI24), Springer, 2025, pp. 377–389.
[78]   The Infographics Show, The $15,000 AI Bill. Your $20 Subscription is a DELUSION, Video,
       The Infographics Show YouTube channel, Published 2026-06-09; duration 18 min 11 s. Popular-
       media video on the gap between flat-rate AI subscription pricing and metered API list prices.
       Title, channel and publication date verified against the YouTube oEmbed endpoint and page
       metadata on 2026-07-23; the video’s contents have not been independently verified. Accessed
       2026-07-23, Jun. 2026. Accessed: Jul. 23, 2026. [Online]. Available: https://www.youtube.
       com/watch?v=UfApUobqN8Y
[79]   F. S. Marcondes, A. Gala, R. Magalhães, F. Perez de Britto, D. Durães, and P. Novais, “Using
       Ollama,” in Natural Language Analytics with Generative Large-Language Models: A Practical
       Approach with Ollama and Open-Source LLMs, ser. SpringerBriefs in Computer Science, Cham:
       Springer Nature Switzerland, 2025, pp. 23–35, ISBN: 978-3-031-76630-5. DOI: 10.1007/978-
       3-031-76631-2_3
[80]   S. J. Andriole, “The big miss: Ai will replace just about everything,” Communications of the
       Association for Information Systems, vol. 55, no. 1, pp. 819–830, 2024.

                                                 64
[81]   P. H. Eng and R. L. Liu, “Will intelligent technologies replace humans in the future? an ex-
       ploratory study for likelihood of intelligent technologies to replace humans in the future,” in Cur-
       rent and Future Trends on Intelligent Technology Adoption: Volume 2, Springer, 2024, pp. 171–
       202.
[82]   D. Trajanov and L. Kocarev, “The cognitive obesity hypothesis: Ai and the risk of mental atro-
       phy,” 2026.
[83]   D. De Cremer and G. Kasparov, “Ai should augment human intelligence, not replace it,” Har-
       vard Business Review, vol. 18, no. 1, pp. 1–8, 2021.
[84]   V. Rawte, A. Sheth, and A. Das, “A survey of hallucination in large foundation models,” arXiv
       preprint arXiv:2309.05922, 2023.
[85]   E. M. Bender, T. Gebru, A. McMillan-Major, and S. Shmitchell, “On the dangers of stochastic
       parrots: Can language models be too big?” In Proceedings of the 2021 ACM conference on
       fairness, accountability, and transparency, 2021, pp. 610–623.
[86]   T. Feng et al., “How far are we from agi: Are llms all we need?” arXiv preprint arXiv:2405.10313,
       2024.
[87]   M. D. Murphy, “Problem definition,” in Landscape Architecture Theory: An Ecological Ap-
       proach, Springer, 2016, pp. 217–242.
[88]   M. Tarafdar, Q. Tu, B. S. Ragu-Nathan, and T. S. Ragu-Nathan, “The impact of technostress
       on role stress and productivity,” Journal of Management Information Systems, vol. 24, no. 1,
       pp. 301–328, 2007. DOI: 10.2753/MIS0742-1222240109
[89]   M. Tarafdar, C. L. Cooper, and J.-F. Stich, “The technostress trifecta — techno eustress, techno
       distress and design: Theoretical directions and an agenda for research,” Information Systems
       Journal, vol. 29, no. 1, pp. 6–42, 2019. DOI: 10.1111/isj.12169
[90]   P. Dwyer, Z. J. Williams, W. B. Lawson, and S. M. Rivera, “A trans-diagnostic investigation of
       attention, hyper-focus, and monotropism in autism, attention dysregulation hyperactivity devel-
       opment, and the general population,” Neurodiversity, vol. 2, p. 27 546 330 241 237 883, 2024.
       DOI : 10.1177/27546330241237883

[91]   A. Dupuis, P. Mudiyanselage, C. L. Burton, P. D. Arnold, J. Crosbie, and R. J. Schachar, “Hy-
       perfocus or flow? Attentional strengths in autism spectrum disorder,” Frontiers in Psychiatry,
       vol. 13, p. 886 692, 2022. DOI: 10.3389/fpsyt.2022.886692
[92]   M. Pessiglione, B. Blain, A. Wiehler, and S. Naik, “Origins and consequences of cognitive
       fatigue,” Trends in Cognitive Sciences, vol. 29, no. 8, pp. 730–749, 2025. DOI: 10.1016/j.
       tics.2025.02.005
[93]   G. Steward, V. Looi, and V. S. Chib, “The neurobiology of cognitive fatigue and its influence
       on effort-based choice,” The Journal of Neuroscience, vol. 45, no. 24, e1612242025, 2025. DOI:
       10.1523/JNEUROSCI.1612-24.2025
[94]   N. A. Choudhury and P. Saravanan, “An integrative review on unveiling the causes and effects
       of decision fatigue to develop a multi-domain conceptual framework,” Frontiers in Cognition,
       vol. 4, p. 1 719 312, 2026. DOI: 10.3389/fcogn.2025.1719312
[95]   S. Cohen, D. A. J. Tyrrell, and A. P. Smith, “Psychological stress and susceptibility to the
       common cold,” New England Journal of Medicine, vol. 325, no. 9, pp. 606–612, 1991. DOI:
       10.1056/NEJM199108293250903
[96]   S. Cohen, “Psychological stress and susceptibility to upper respiratory infections,” American
       Journal of Respiratory and Critical Care Medicine, vol. 152, no. 4 Pt 2, S53–S58, 1995. DOI:
       10.1164/ajrccm/152.4_Pt_2.S53



                                                   65
 [97]    S. Cohen, “Psychological stress, immunity, and upper respiratory infections,” Current Direc-
         tions in Psychological Science, vol. 5, no. 3, pp. 86–89, 1996. DOI: 10.1111/1467- 8721.
         ep10772808
 [98]    D. G. Hall and L. Ericson, “The marviken critical flow test—a description and early results,” in
         ENS/ANS international topical meeting on nuclear power reactor safety, Belgium, 1978.
 [99]    Z. Guo and S. Xiao, “Thermal hydraulic study of nuscale ipwr passive containment cooling
         behaviour during loss-of-coolant accident,” International Journal of Advanced Nuclear Reactor
         Design and Technology, vol. 7, no. 2, pp. 100–109, 2025.
[100]    T. Zhang and C. S. Brooks, “Linear stability analysis of flashing instability based on the homo-
         geneous equilibrium model,” Nuclear Engineering and Design, vol. 373, p. 110 994, 2021.
[101]    T. Zhang and C. S. Brooks, “Assessment of asyst and relap5 for predicting stability and limit
         cycles of a low-pressure natural circulation loop with flashing instability,” Applied Thermal
         Engineering, vol. 257, p. 124 427, 2024.
[102]    G. Nervi, T. Guilbaud, C. Fiorina, M. Hursin, and A. Scolaro, “Foamfornuclear: A unified open-
         foam multi-physics platform for nuclear applications,” Progress in Nuclear Energy, vol. 193,
         p. 106 250, 2026. DOI: 10.1016/j.pnucene.2026.106250
[103]    K. Mahboob, A. Alkaabi, and Y. Addad, “Simulating molten corium concrete interaction: A
         multiphase approach with openfoam,” Nuclear Engineering and Technology, p. 104 357, 2026.
[104]    T. K. C. Ong, Openmc-endf-8-depletion-lib-a: Rust parser for OpenMC ENDF/B-VIII.0 deple-
         tion chain data, part one, https : / / github . com / theodoreOnzGit / openmc - endf - 8 -
         depletion-lib-a, Licensed MIT. A boon-lay dependency, consumed by outram-mc-libs.
         The parser was generated largely by OpenAI ChatGPT-5 (non-agentic, conversational) with au-
         thor corrections; the bulk of the repository is ENDF/B-VIII.0 decay-chain data taken verbatim
         from the OpenMC depletion libraries, which the author separated by nuclide and wrapped into
         Rust functions by hand in Neovim — reorganised public reference data, not authored logic.
         Excluded from the productivity accounting for that reason. Accessed 2026-07-24, 2026.
[105]    T. K. C. Ong, Openmc-endf-8-depletion-lib-b: Rust parser for OpenMC ENDF/B-VIII.0 deple-
         tion chain data, part two, https : / / github . com / theodoreOnzGit / openmc - endf - 8 -
         depletion-lib-b, Licensed MIT. A boon-lay dependency, consumed by outram-mc-libs.
         Parser generated largely by OpenAI ChatGPT-5 (non-agentic, conversational) with author cor-
         rections; the remainder is ENDF/B-VIII.0 decay-chain data taken verbatim from the OpenMC
         depletion libraries and wrapped into Rust functions by hand in Neovim. Reorganised public
         reference data, excluded from the productivity accounting. Accessed 2026-07-24, 2026.
[106]    T. K. C. Ong, Fission-yields-data: Fission yields for various nuclides using ENDF and other
         library data, https : / / github . com / theodoreOnzGit / fission - yields - data, Li-
         censed GPL-3.0. Developed 2025-10-17 to 2026-01-19; a boon-lay dependency, consumed by
         outram-mc-libs. The serialisation parser (serde chatgpt 5) was generated largely by Ope-
         nAI ChatGPT-5 (non-agentic, conversational) with author corrections; the bulk is ENDF/B-
         VIII.0 parent-independent fission-yield data taken verbatim from public libraries and wrapped
         into Rust functions by hand in Neovim. Reorganised public reference data, excluded from the
         productivity accounting. Accessed 2026-07-24, 2026.


A       Reproducing the Line Counts
The productivity claims above rest entirely on line counts, and a line count is only as good as the rule
used to produce it. Tables XIV and XVI and Figure 15 are therefore not compiled by hand. They are
emitted by a single script, kloc accounting.py, which is distributed with this manuscript and which
takes its inputs directly from the repositories and their git histories. Anyone may re-derive every number
by running

                                                   66
                     python3 kloc accounting.py --from-github --check

which clones the public repositories, measures them, and prints a row-by-row comparison against the
figures printed here. It requires nothing on the machine beyond git, python3 and matplotlib.
    Four decisions in that script materially affect the result and are stated here rather than buried:

   1. Comment stripping is lexical, not regular. A code line is a line carrying at least one non-
      whitespace character once comments are removed. The remover is a scanner that tracks nested
      block comments, raw strings (r#"..."#), byte strings and character literals, so that a // inside a
      string literal is not mistaken for a comment and a lifetime ’a is not mistaken for a character. Doc
      comments, which in Rust carry executable doctests, are excluded from the code count and appear
      only in the total.

   2. Measurement is on develop, not main. These repositories squash-merge into main. Measur-
      ing main reports nine active days for thermal hydraulics rs where the development branch
      records 144, and would understate the pre-agentic baseline by more than a factor of two — which
      would inflate, not deflate, the productivity claim.

   3. An emptied repository is measured before it was emptied. thermal hydraulics rs was
      reduced from 260 Rust files to nine on 2024-10-11, when its code moved into TUAS. It is therefore
      counted at commit 4d534af, the last commit at full extent. Its branch tip would report 1.6 KLOC
      and would make the ”TUAS net of what it inherited” subtraction meaningless.

   4. TUAS is netted against what it imported, not against its predecessor’s size. TUAS was spun
      out of thermal hydraulics rs and imported it wholesale at its second commit, c451c8e,
      42 minutes after the initial commit. The subtrahend is that imported tree — 236 files, 52 054
      code lines — and not the predecessor’s own full extent of 260 files and 59 808 code lines. The
      difference, 7 754 code lines, is work written in the predecessor and abandoned rather than carried
      forward. Netting against the predecessor’s full size would delete that work from the baseline, and
      since the baseline is the denominator of the productivity ratio, doing so would inflate the headline
      figure from 12.3 to 12.8. The narrower reading of ”inherited” is the one that can be defended, and
      it is the one used here.

   5. Provenance classification is the one editorial input. Whether a crate counts as a translation, as
      original work, or as an extension of vendored pre-agentic code is a judgement, not a measurement.
      Those judgements are listed explicitly in the script, and each crate’s own Cargo.toml description
      is carried into the emitted CSV beside the classification so that a reader can disagree with any
      individual assignment and recompute the subtotals.

   6. Classification follows the code, not the package boundary. The two terminal interfaces, njoy-tui
      and outram-mc-tui, ceased to be workspace crates on 2026-07-23 and became feature-gated bi-
      naries inside the libraries they drive, so that a library consumer no longer sees them as separate
      packages. Their code is newly written, but it now sits inside crates that are ports of an existing
      upstream. The script therefore splits them out at the path boundary (src/bin/) and credits them
      to original work; folding them into their host crates would have moved 2.5 KLOC of interface
      code into the translated column and overstated the translated share.

    The script refuses to fail silently in the two ways that would matter. A crate present in the repository
but absent from the classification is reported and excluded rather than quietly folded into a subtotal, and
a classification with no corresponding crate in the checkout is reported as stale. Both checks earned their
place: the crate reorganisation described above was detected by the second of them rather than noticed
by hand.
    Finally, these counts measure volume, not worth. Lines of code are a poor proxy for engineering
value at the best of times, and they are a particularly poor one here, where 77 per cent of the agentic

                                                    67
output is translation of an existing and already-debugged implementation. The counts are reported
because they are reproducible, not because they are sufficient.


B    Token Consumption of an Agentic Crate
Token accounting was not performed properly during the early Rust translations of Outram-Foam and
Outram MC. Token accounting scripts and instructions for Claude Code were introduced later.
    This makes it easier to see how much an agentic porting costs in terms of tokens. This is useful for
management decisions, since management may want to know a realistic upper limit of API costs in the
long run as opposed to subscription costs.
    To check, we used Claude Code to translate Offbeat, which is the fuel performance sister code of
GeN-Foam[102] , into outram-park-fork-offbeat, one single active day sufficed (2026-07-29), got
ten commits totalling 13 863 lines of Rust code. This was done after the snapshot used in the main body
text. The reader should note that agentic development of Outram Park is an ongoing process. By the
time the papers come out, the figures here will already be outdated. This should be read as historical
snapshots, and the offbeat translation is an addendum to the work discussed in the prose. Do note also
that offbeat postdates any of the agentic coding work described in the prose.
    AI-generated scripts with Claude Code were used to insert token usage counts into git commit his-
tories. Then after that, Claude Code was asked to summarise token usage between commits for offbeat
from the Git histories. These were done in Tables XX and XIX:

Table XIX: API token consumption for outram-park-fork-offbeat, ten commits on 2026-07-29.
total = in + out + cache read + cache write.

                                     Category            Tokens        Share
                                     Input                 2 867    0.0 %
                                     Output              658 725    0.2 %
                                     Cache write       6 440 829    2.1 %
                                     Cache read      305 272 222   97.7 %
                                     Total           312 374 643   100 %



Table XX: Estimated API cost for outram-park-fork-offbeat at Claude Opus 4.8 list rates (input
$5.00, output $25.00, cache read $0.50, cache write $6.25 at the five-minute cache tier per million
tokens). The cache-write tier is not recorded in the trailers; the one-hour tier ($10.00 per million) gives
the upper figure.

                               Category               Rate ($/Mtok)       Cost ($)
                               Input                            5.00         0.01
                               Output                          25.00        16.47
                               Cache read                       0.50       152.64
                               Cache write (5 min)              6.25        40.26
                               Total (5 min cache)                         209.37
                               Total (1 h cache)                           233.53


    We can see that, assuming Opus costs (this is the upper limit), offbeat would have cost about
USD$210 for the entire code translation based on API costs. Compared to Claude Max subscription
for one month, which is USD$200, one offbeat library translation would have easily made up for the
sunk cost of Claude Max.
    Assuming a 500 lines/active coding day pre-agentic coding speed, offbeat would have taken 26
engineer-days to develop. Assuming USD$200 per working day, this would mean a cost of about
USD$5,200 to translate offbeat. In reality, it may have taken longer and cost more if such an engineer

                                                      68
did not have the domain knowledge of the numerical methods and engineering knowledge to translate
offbeat by hand. In the case of the author, the author’s main knowledge is thermal-hydraulics and dig-
ital twins [2], so fuel performance lies outside his expertise. However, translation of offbeat via AI
to produce such a draft demonstrates the use of AI to translate code outside the author’s main domain
knowledge within nuclear engineering. This illustrates the capability that agentic coding offers the user.
     Thus, even in this case, using the API costs, it would be more economical to translate offbeat using
Claude Code as compared to human translation.


C      Development of Tampines Steam Tables

Table XXI: Major development milestones of tampines-steam-tables, from the standalone reposi-
tory (v0.0.1–v0.1.8) through migration into the outram-park-backend workspace (v0.2.0–v0.2.4).

    Date               Milestone                            Implementation and verification                      Commit
    Phase I — Standalone repository: IAPWS-IF97 property library
    2025-01          Project bootstrap                  Physical constants, triple and boiling points,           3e266d5
                                                        region 1–5 coefficient tables
    2025-01          Region 1 forward equations         Gibbs energy and derivatives for subcooled liquid;       25d2a67
                     (v0.0.1)                           dimensioned with uom. Verified vs. IST Table 2.5
                                                        sets A–C
    2025-01          Region 2 and metastable vapour     Ideal-gas and residual γ terms, κ, α, κT ; separate      8ba86e5
                     (v0.0.2)                           metastable subregion. Verified vs. IST region 2
                                                        sets A–C
    2025-01          Region 3, B23 boundary,            Helmholtz φ derivatives; auxiliary B23 equation;         f9d18ec
                     saturation line (v0.0.3–4)         region 4 saturation p–T . Verified vs. IST region 3
                                                        sets A–C
    2025-01          Region 5 high-temperature steam    Forward equations above 800 ◦ C. Verified vs. IST        eb77b17
                     (v0.0.5)                           region 5 sets A–C
    2025-01          Backward (p, h) equations (v0.0.6) T (p, h) regions 1–2, subregion 2b–2c boundary,          4cf0793
                                                        v(p, h) and T (p, h) for 3a/3b. Verified vs. IST
                                                        Tables 2.38, 2.42
    2025-01/02       Region dispatch and (p, T ) flash  Functional interfaces/ API, validity-range               3663628
                                                        checks, boundary logic across all five regions and
                                                        the two-phase dome
    2025-01/02       Full (p, h) flash verification     v, T , s, x, c p , cv , w over the whole IF97 surface,   46fd78c
                                                        0.006 11 bar to 1000 bar, 0 ◦ C to 800 ◦ C; accuracy
                                                        loss documented near the critical point
    2025-02          Two-phase (p, T ) flash            Multiphase flash; revised κ/α in region 3 near           d9cc877
                                                        saturation; near-critical enthalpy fix
    2025-02          Dynamic viscosity (IAPWS 2008) ψ0 , ψ1 terms with (ρ, T ), (p, T ), (p, h) entry            3f60ab4
                                                        points; agreement within 2 %
    2025-02          Thermal conductivity (IAPWS        λ0 , λ1 , λ2 critical enhancement; larger uncertainty    6978dab
                     2011) (v0.0.7–8)                   documented at 160/220 bar and supercritical
    2025-02          Backward (p, s) equations and      T (p, s) regions 1, 2a–2c; v(p, s), T (p, s) for         e1208ba
                     flash (v0.0.9)                     3a/3b; B ps3 boundary. Verified 10 bar to 800 bar
    2025-02          Surface tension and dielectric     IAPWS surface-tension correlation and                    a483cfd
                     constant (v0.1.0)                  Harvey–Fernández-Prini dielectric constant
    2025-03/04       Backward (h, s) equations (v0.1.1) p(h, s) regions 1, 2a–2c, 3a/3b; Tsat (h, s) region 4;   3703731
                                                        B13 and TB23 boundaries. Partial: inaccurate
                                                        below 10 bar
    2025-03–2026-03 OpenFOAM algorithm ports            Rust translations of simpleFoam,                         fecd17d
                                                        rhoPimpleFoam, driftFluxFoam,
                                                        chtMultiRegionTwoPhaseEulerFoam with
                                                        LATEX derivations
    2025-06          FHR educational simulator v1       egui GUI; steam generator and Rankine loop               33bfa9b
                     (v0.1.2, tagged)                   coupled to salt loops via tuas boussinesq
                                                        solver and teh-o-prke
                                                                                                  continued on next page


                                                             69
Table XXI (continued)
Date               Milestone                           Implementation and verification                         Commit
2026-02/03         Object-oriented control-volume      TampinesSteamTableCV wrapper, transient                 df9edfc
                   API (v0.1.4)                        mass balance, serde support
2026-03            Steam turbine and generator         Euler/impulse turbine equations, velocity               e9a8824
                   models                              triangles, torque and EMF braking, discretised
                                                       three-phase generator (250 MWe )
2026-03            Isentropic nozzle solver            Force-balance residual, entropy iteration after         5c3043d
                                                       (h, s)/(p, s) disagreement, iterative (p, h)-based
                                                       (h, s) flash for low quality
2026-03/04         Choked-flow foundations             Critical pressure ratio, HEM sound speed,               01cc3e7
                                                       nozzle/diffuser dp–dA–dv relations, Rayleigh-line
                                                       balance. Verified vs. Çengel worked examples
2026-04/05         Converging–diverging nozzle         Bisection/secant solvers for subsonic,                  8b1c313
                   regimes (v0.1.6–7)                  perfectly-expanded and overexpanded branches;
                                                       Mach-number and Joule–Thomson tests
2026-05            Marviken critical-flow tests        Blowdown harness after the Marviken full-scale          8ad8819
                   (v0.1.7)                            vessel series (NUREG/CR-2671)
2026-05/06         Moody critical mass flux (HEM)      Critical mass flux from stagnation (p0 , h0 ); isobar   0b5c72f
                                                       verification vs. Moody (1975), NEDO-21052,
                                                       p0 /pref = 0.5–30
2026-06            Wood–Wallis and equilibrium         w ps eqm via finite-difference volume derivatives;      2329742
                   sound speed                         verified vs. Kieffer (1977) eq. 28, except
                                                       100/200 bar near saturation
2026-06            Zaloudek dataset and round-trip     Digitised critical-pressure curves for x = 0–0.75;      aaed718
                   validation                          forward and backward throat→stagnation tests;
                                                       bubble-point edge cases. Data per Saha (1978),
                                                       NUREG/CR-0417
2026-06            Choked-flow module split (v0.1.8)   Separate single-phase, in-dome and outside-dome         e7b5097
                                                       stagnation solvers; in-dome passing,
                                                       near-bubble-point artifact unresolved at migration
Phase II — Migrated into outram-park-backend: dependency refresh and new functionality
2026-06-19       Migration into workspace            Vendored with three sibling crates (813 files,            8a048d3
                                                     +291k lines); v0.1.8→v0.2.0; dependencies
                                                     centralised in [workspace.dependencies]
2026-06-22       Dependency upgrade                  uom 0.36→0.38, ndarray 0.15→0.17,                         0148c75
                                                     thiserror 1.0→2.0, egui 0.29→0.34;
                                                     breaking-change fixes across the crate
2026-06-24       BLAS decoupling                     ndarray-linalg and openblas-src demoted                   85ac0d8
                                                     then removed; library reduced to four
                                                     dependencies
2026-06-26       Near-bubble-point artifact resolved Root-caused as numerical, not physical; quality           06e33fb
                                                     discriminator x < 0.03 plus precomputed sonic
                                                     mass flux along the saturated-liquid line.
                                                     Zaloudek xt = 0–1.0 within ±0.04 in log10 G
2026-06-26       Superheated/supercritical HEM       get critical pressure and mass flux                       3dbbdd9
                 solver                              superheated vapour ph for stagnation states
                                                     outside the dome
2026-06-29       Unified HEM dispatcher              Routes (p0 , h0 ) by ph flash region to in-dome,          50632f0
                                                     subcooled and superheated solvers; handles
                                                     region-3 isentropes re-entering the dome. All 13
                                                     stagnation tests re-enabled; region 3 < 0.5 %,
                                                     region 1 < 1.4 %
2026-06-29       Transient mass and energy balance CvMassEnthalpyChanges ledger and advance                    0ffbe91
                 API                                 timestep(); regula-falsi (p, h) inversion on
                                                     target specific volume
2026-06-30       Moody isobars pass (v0.2.1)         Region-filtered tests across 13 isobars at 0.06           7173480
                                                     log10 G tolerance; subcooled Moody–Zaloudek
                                                     regime reconciliation documented
                                                                                               continued on next page




                                                       70
    Table XXI (continued)
    Date               Milestone                          Implementation and verification                    Commit
    2026-07-01         TampinesSteamArray scaffolded      One-dimensional compressible PIMPLE pipe           01bda7c
                                                          solver on an FvMesh; vendored OpenFOAM field,
                                                          FV-operator, LDU-matrix and thermophysics
                                                          sources
    2026-07-06         TUAS dependency dropped            Property core made fully standalone; tuas          18d7a6f
                                                          boussinesq solver removed as a library
                                                          dependency
    2026-07-13         tampines framework crate           Facade composing steam tables, CoolProp fork       5bca434
                                                          and DWSIM equipment models; balance-of-plant
                                                          and cooling-tower modules; hosts fhr sim v2
    2026-07-13         Real IF97 flash in correct         Placeholder EOS replaced by a genuine              356daff
                       thermo()                           two-phase (p, h) flash in the array solver
    2026-07-14         Steam-generator tube integration   Array wired into fhr sim v2; OpenFOAM-style        032e95f
                                                          pressure bounding; lambda ph eqm
                                                          critical-enhancement term made two-phase-safe
    2026-07-15         Android portability (v0.2.2)       (p, h) flash hardening for regions 4–5;            bbde28a
                                                          dev-dependencies gated off
                                                          aarch64-linux-android
    2026-07-16         Edwards–O’Brien blowdown           24-CV RELAP nodalisation, Hendrie (1973) axial     8380513
                       V&V (v0.2.3)                       IC, HEM break BC, 600 ms at ∆t = 1 × 10−4 s;
                                                          conservative energy derivative and two-phase
                                                          ψ = ∂ ρ/∂ p|h by finite difference. GS-1 RMSE
                                                          60 psia, down from 276
    2026-07-16         HybridAllMach solver stabilised    KNP central-upwind flux with Kieffer HEM           46b75a6
                       (v0.2.4)                           sound speed plus rarefied-tail blend taper. GS-1
                                                          RMSE 30.6 psia vs. 58.6 for PIMPLE; 920 library
                                                          tests pass



D      Developer Health Warning: Agentic Software Development
The following reproduces, near-verbatim, the project’s DEVELOPER HEALTH WARNING.md, authored by
the maintainer (agentically) after roughly one month of intensive agentic development. The prose is un-
changed; three presentational changes have been made for this manuscript. The in-text citations, written
in APA style in the original, are rendered here in the numeric style of this research log. The original doc-
ument’s separate reference list has been folded into the manuscript bibliography, where its ten sources
appear via the citations below. And the two flow sketches, drawn as ASCII art in the original, have been
redrawn as diagrams with their node text preserved — these are therefore not verbatim reproductions of
the original figures.

     Warning

     Outram Park was developed using highly agentic software engineering workflows involving
     Claude Code, Microsoft Copilot, ChatGPT, Gemini, and other AI-assisted development tools.
     While these tools can dramatically increase engineering productivity, they may also increase the
     risk of technostress, cognitive fatigue, decision fatigue, hyperfocus, insomnia, burnout, and pro-
     longed illness.
     Developers are encouraged to treat wellbeing, recovery, and sustainable working practices as
     first-class engineering requirements.


Why This Document Exists
This document was written after approximately one month of intensive agentic software development
on the Outram Park project.
    During this period, the maintainer experienced:


                                                          71
    • Persistent fatigue.

    • Decision fatigue.

    • Difficulty disengaging from development activities.

    • Hyperfocus lasting many consecutive hours.

    • Sleep disruption and insomnia.

    • Reduced awareness of accumulating exhaustion.

    • A prolonged sore throat lasting approximately one month.

    • Continued development activity despite recognized fatigue.

   These experiences motivated a review of:

    • Repository commit history.

    • Working-hour patterns.

    • Existing literature on technostress.

    • Existing literature on cognitive fatigue.

    • Existing literature on hyperfocus.

    • Existing literature on psychological stress and immune function.

   The goal of this document is to help future contributors avoid repeating the same mistakes.

1. Anecdotal Evidence from the Outram Park Project
Commit History Analysis
A review of repository history identified:

                                Metric                             Value
                                Total commits analysed               282
                                Commits inside working hours         201
                                Commits outside working hours          81
                                Percentage outside working hours   28.7%


   This means:

    • Nearly 29% of all commits occurred outside working hours.

    • Roughly 1 in every 3.5 commits was made outside the eventual safety window.

    • Almost one-third of repository activity occurred during periods later designated as recovery or
      off-work time.




                                                   72
Breakdown of Outside-Hours Activity


                             Category                                              Count
                             Weekday commits before 07:30 or after 20:00                52
                             Sunday commits outside permitted hours                     13
                             Saturday commits (full rest day)                           16
                             Total outside-hours commits                                81


Observed patterns included:
    • Late-night development sessions.
    • Activity extending beyond 22:00.
    • Occasional development after midnight.
    • Multiple weekend coding sessions.
    • Repeated Sunday evening work.
    • Several full Saturdays spent developing software.
    Importantly, the working-hours policy discussed later did not exist during most of this period. The
majority of these commits therefore do not represent policy violations; rather, they represent historical
behaviour that preceded the creation of project-level health safeguards.
    Nevertheless, the commit history provides an objective record of sustained after-hours development
activity.

The Productivity Trap
One particularly important observation was that excessive work was not primarily driven by project
deadlines.
   A major motivating factor was:
      Maximizing utilization of a Claude Pro subscription.
   The thought process often looked like:

                                               Available token budget


                                                 Unused AI capacity


                                        “I should use what I am paying for”


                                                 “One more feature”


                                               “One more benchmark”


                                                 “One more refactor”


                                          Several additional hours of work

      Redrawn as a diagram; the original document rendered this as an ASCII sketch, so this figure is not verbatim.


                                                          73
   This behaviour was reinforced by:

    • Immediate implementation availability.

    • Extremely short development feedback loops.

    • Rapid visible project progress.

    • The feeling that unused model capacity represented wasted value.

   In retrospect, this created a novel productivity trap:

      Because software development had become unusually inexpensive, there was increased
      pressure to continue generating more work.

   The AI model never became tired.
   The developer did.

The One-Month Illness
During the same period, the maintainer experienced:

    • Persistent fatigue.

    • Sleep disruption.

    • Decision fatigue.

    • A sore throat lasting approximately one month.

   This document does not claim that AI tools directly caused illness.
   However, these observations motivated a review of literature exploring the relationship between:

    • Technostress,

    • Hyperfocus,

    • Sleep disruption,

    • Cognitive fatigue,

    • Psychological stress,

    • Immune function.

2. Engineering Safety Controls
Working-Hour Restrictions
Following this period, formal safeguards were introduced into CLAUDE.md.
    Agentic development is restricted to:

                                Day                Working Hours
                                Monday–Friday      07:30–20:00
                                Saturday           No agentic development
                                Sunday             12:00–19:00


   Outside these periods:

                                                    74
    • Claude Code must not perform agentic development work.

    • Claude Code may assist only with planning activities.

    • Tasks should instead be recorded using Beads or TODO systems.

Purpose of the Policy
The purpose of this policy is not to reduce productivity.
   The purpose is to:

    • Protect sleep.

    • Protect weekends.

    • Protect long-term sustainability.

    • Reduce burnout risk.

    • Preserve engineering judgement.

    • Prevent recurrence of prolonged illness.

3. Literature Review
Technostress
Technostress refers to stress arising from technology use and technology-enabled work.
   Tarafdar, Tu, and Ragu-Nathan [88] introduced several major dimensions of technostress:

    • Techno-overload.

    • Techno-invasion.

    • Techno-complexity.

    • Techno-insecurity.

    • Techno-uncertainty.

Techno-Overload
Techno-overload occurs when technology increases the amount of work an individual can perform and
therefore increases expectations and workload [88].
    Agentic development workflows may amplify techno-overload because:

    • Code generation becomes dramatically faster.

    • Refactoring becomes inexpensive.

    • Architectural experimentation becomes easier.

   The bottleneck therefore shifts from implementation toward:

    • Review,

    • Verification,

    • Validation,

    • Decision making.

                                                   75
Techno-Invasion
Techno-invasion occurs when technology erodes the boundary between work and personal life [88].
   Examples include:

    • Evening coding sessions.

    • Weekend work.

    • Difficulty disengaging from projects.

    • The feeling that productive work remains continuously available.

    Tarafdar, Cooper, and Stich [89] note that technology can simultaneously generate benefits (“techno-
eustress”) and harms (“techno-distress”), highlighting the need for deliberate safeguards.

Hyperfocus
Hyperfocus refers to periods of unusually intense attentional engagement.
   Research has documented hyperfocus across autistic, ADHD, and general populations [90].
   Dwyer et al. [90] reported associations between hyperfocus and:

    • Reduced quality of life.

    • Repetitive thinking.

    • Greater anxiety symptoms.

    • Attentional regulation difficulties.

    At the same time, hyperfocus is not inherently negative.
    Dupuis et al. [91] found that intense attentional engagement may also function as a genuine cognitive
strength that contributes to productivity and deep work.
    Consequently:

      Hyperfocus may facilitate exceptional progress while simultaneously increasing the risk of
      overwork.

    Warning signs include:

    • Skipping meals.

    • Missing breaks.

    • Delaying sleep.

    • Losing awareness of time.

    • Continuing work despite obvious fatigue.

[90], [91]




                                                   76
Cognitive Fatigue
Cognitive fatigue emerges following prolonged periods of demanding mental effort.
   Pessiglione et al. [92] reviewed evidence suggesting that cognitive fatigue:

    • Accumulates over time.

    • Is often poorly recognized by the individual experiencing it.

    • Alters subsequent decision making.

    • Reduces willingness to engage in demanding cognitive tasks.

    Steward et al. [93] further demonstrated that repeated cognitive exertion alters subsequent effort-
based decision making.
    Their findings suggest that fatigue affects not only performance but also future willingness to exert
effort [93].
    In agentic development:

    • Coding effort decreases.

    • Review effort increases.

    • Validation effort increases.

    • Architectural decision making increases.

    Consequently, significant cognitive fatigue may develop despite reduced manual programming ef-
fort.

Decision Fatigue
Decision fatigue refers to deterioration in decision quality following prolonged decision making.
   Choudhury and Saravanan [94] identified several consequences:

    • Reduced efficiency.

    • Lower-quality decisions.

    • Increased cognitive burden.

    • Choice avoidance.

   Agentic systems frequently generate:

    • Multiple architectures.

    • Multiple valid implementations.

    • Multiple debugging approaches.

    • Multiple optimization strategies.

   The developer therefore becomes responsible for choosing among many plausible alternatives.
   AI systems may therefore reduce implementation effort while simultaneously increasing decision-
making effort.



                                                   77
Stress, Immunity, and Illness
The relationship between psychological stress and immune function is one of the strongest empirical
foundations relevant to this document.
    Cohen, Tyrrell, and Smith [95] conducted a landmark viral challenge study in which healthy volun-
teers were intentionally exposed to respiratory viruses.
    They observed a dose-dependent relationship between psychological stress and susceptibility to res-
piratory illness [95].
    Participants experiencing higher levels of psychological stress were more likely to:

    • Become infected.

    • Develop clinical cold symptoms.

[95]
    Subsequent reviews concluded that psychological stress is associated with measurable changes in
immune functioning and increased susceptibility to upper respiratory infections [96], [97].
    The literature therefore supports the plausibility of the following pathway:

                                                Agentic development


                                                     Technostress


                                                      Hyperfocus


                                              Extended working hours


                                                   Sleep disruption


                                            Chronic psychological stress


                                               Immune system effects


                                          Increased susceptibility to illness

      Redrawn as a diagram; the original document rendered this as an ASCII sketch, so this figure is not verbatim.

    Importantly, the literature does not demonstrate that AI tools directly cause illness.
    Instead, it demonstrates that prolonged stress, fatigue, poor recovery, and sleep disruption may con-
tribute to physiological states associated with increased illness susceptibility [95], [96], [97].

Key Takeaway
The current scientific literature does not yet contain extensive studies specifically examining long-
duration agentic coding workflows.
   However, converging evidence from:

    • Technostress research [88], [89],

    • Hyperfocus research [90], [91],


                                                          78
    • Cognitive fatigue research [92], [93],

    • Decision fatigue research [94], and

    • Stress-immunity research [95], [96], [97]

   suggests that highly productive AI-assisted development workflows should be treated as potential
occupational health risks when recovery, boundaries, and sustainable work practices are neglected.

4. Recommendations
Protect Sleep
Sleep is an engineering dependency.
    Treat insufficient sleep as seriously as:

    • Failing tests.

    • Broken builds.

    • Invalid validation results.

Record Decisions Instead of Continuing Work
When fatigued:

    • Write notes.

    • Create TODO items.

    • Create Beads tasks.

    Do not force major architectural decisions.

Respect Stopping Points
Establish explicit end-of-day criteria.
    Do not rely on:

      “Just one more task.”

Preserve Recovery Time
Protect:

    • Sleep.

    • Meals.

    • Exercise.

    • Weekends.

    • Annual leave.

    • Family time.




                                                  79
Remember the Human Bottleneck
      AI systems do not become tired.
      Developers do.

   A highly productive project that burns out its developers has failed one of its most important engi-
neering constraints.




                                                  80
