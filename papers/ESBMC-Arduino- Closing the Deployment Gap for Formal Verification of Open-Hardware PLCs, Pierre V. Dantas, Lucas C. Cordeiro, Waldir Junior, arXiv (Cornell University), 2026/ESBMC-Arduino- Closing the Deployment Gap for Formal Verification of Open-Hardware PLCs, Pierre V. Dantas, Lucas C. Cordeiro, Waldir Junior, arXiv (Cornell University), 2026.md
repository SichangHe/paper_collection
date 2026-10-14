                                              ESBMC-A RDUINO : C LOSING THE D EPLOYMENT G AP FOR
                                                F ORMAL V ERIFICATION OF O PEN -H ARDWARE PLC S

                                                                                                P REPRINT


                                                                Pierre Dantas*                                        Lucas Cordeiro
                                                        Department of Computer Science                         Department of Computer Science
                                                          The University of Manchester                          The University of Manchester
                                                               Manchester, UK                                         Manchester, UK
                                                      pierre.dantas@manchester.ac.uk                        lucas.cordeiro@manchester.ac.uk

                                                                                            Waldir Junior
                                                                                         Electrical Engineering
                                                                                Federal University of Amazonas (UFAM)
                                                                                          Manaus, AM, Brazil
arXiv:2607.08550v1 [cs.PL] 9 Jul 2026




                                                                                       waldirjr@ufam.edu.br


                                                                                              July 10, 2026

                                                                                              A BSTRACT
                                                   OpenPLC, Arduino OPTA, CONTROLLINO, and Industrial Shields M-Duino – bring IEC 61131-3
                                                   programming to low-cost, microcontroller-class devices increasingly used in real automation and in
                                                   Industrial Control Systems (ICS) security research. Existing open-source verifiers for IEC 61131-3,
                                                   including the ESBMC-PLC line, prove safety over an abstract scan-cycle model with idealized
                                                   unbounded integers. The artifact that runs on the board, however, executes on a resource-constrained
                                                   Microcontroller Unit (MCU) with a 16-bit machine word (8-bit AVR Arduinos), and sensors are
                                                   read through a finite-resolution Analog-to-Digital Converter (ADC). We show that this deployment
                                                   gap makes naive width-aware verification unsound in practice: on 123 real third-party programs,
                                                   checking 16-bit arithmetic overflow without a hardware input model raises a 44 % false-alarm rate
                                                   (54/123) and finds zero genuine defects, because it explores sensor values no ADC can produce.
                                                   Because the gap sits exactly where computation meets the physical process – a bounded sensor
                                                   reading scaled by finite-width integer arithmetic into an actuation command – an overflow can
                                                   silently suppress a physical safety action such as a high-level alarm. At the same time, an unbounded
                                                   input model fabricates alarms that no environment can trigger. We present a method for hardware-
                                                   faithful verification of IEC 61131-3 on open hardware: a declarative Hardware Abstraction Layer
                                                   (HAL) descriptor (word width, ADC/Pulse-Width Modulation (PWM) resolution, I/O binding) and
                                                   a sound lowering that interprets arithmetic at the target word width and constrains each input to its
                                                   hardware-realizable range, transferring to the Programmable Logic Controller (PLC) domain the
                                                   target-model discipline established for safety-critical embedded C (Frama-C, Astrée). We instantiate
                                                   it for Arduino as ESBMC-Arduino, deriving HAL parameters from the official Arduino cores and
                                                   realizing the input-range model as a lightweight hook in the Efficient SMT-based Context-Bounded
                                                   Model Checker (ESBMC) Ladder Diagram (LD) frontend. On the 123-program corpus, the HAL
                                                   annotator eliminates all 54 false alarms (54→0) while preserving every robustness proof, and a
                                                   controlled corpus demonstrates the genuine – but rare – width-dependent defects the method detects
                                                   with physically realizable witnesses.

                                        Keywords deployment gap · hardware-faithful verification · HAL descriptor · machine word width · ADC input model ·
                                        PLC · IEC 61131-3 · open-hardware PLC · ESBMC · BMC · k-induction · formal verification · LD · PLCopen XML
                                          ∗
                                              Corresponding author.
                        ESBMC-Arduino: Closing the Deployment Gap for Open-Hardware PLCs                       A P REPRINT



1     Introduction

Programmable Logic Controllers (PLCs) govern safety-critical processes, but a new class of open-hardware PLCs
– OpenPLC [1, 2], Arduino OPTA [3, 4], CONTROLLINO [5], and Industrial Shields M-Duino [6] – now brings
International Electrotechnical Commission (IEC) 61131-3 programming to low-cost, microcontroller-class devices.
These platforms are widely used in education, small-scale automation, and – importantly for assurance – as the runtime
substrate for academic Industrial Control Systems (ICS) security testbeds; OpenPLC, in particular, was designed
explicitly for cybersecurity research [1].

1.1    The Deployment Gap

Open-source verifiers for IEC 61131-3 – the ESBMC-PLC in particular [7, 8, 9], and PLCverif [10, 11] – prove safety
properties over an abstract scan-cycle model of the Ladder Diagram (LD) or Structured Text (ST) logic, with idealized,
effectively unbounded integers and unconstrained inputs. The artifact that runs on an open-hardware PLC is different: it
executes on a resource-constrained Microcontroller Unit (MCU) where a machine word is only 16 bits on the 8-bit
AVR boards (Arduino Uno/Nano/Mega), and physical inputs arrive through an Analog-to-Digital Converter (ADC) of
finite resolution (a 10-bit ADC yields integer readings in [0, 1,023]). Arithmetic that is exact in the abstract model can
therefore overflow on the device, and a property proved on the logic model need not hold on the deployed binary. We
call this discrepancy the deployment gap.
The gap cuts both ways, and both directions matter for assurance. A program can be unsafe on the device yet pass
abstract verification (a missed defect); and – less obviously but, as we show, far more common – naively accounting for
the word width without modelling the hardware inputs makes verification unsound in practice: the verifier explores
sensor values no ADC can produce (e.g. IN = −32,764), reports overflows that can never occur, and buries any real
finding under false alarms. On 123 real third-party programs, we measured a 44 % false-alarm rate (54/123) with zero
genuine defects found this way (§8).

1.2    Contributions

This paper closes the gap with a method and its open-hardware instantiation. Our thesis is “what you verify must be
what runs on the device”, which requires modeling both the target word width and the hardware-realizable input ranges.

    1. Hardware-faithful verification of IEC 61131-3 (§5). A method that, given a program P and a declarative
       Hardware Abstraction Layer (HAL) descriptor H (word width, ADC/Pulse-Width Modulation (PWM) resolution,
       I/O binding), constructs a sound deployment model Mdev (P, H): arithmetic is interpreted at the target word
       width and every input is constrained to its hardware-realizable range. We give the construction, a soundness
       argument, and a gap-diagnosis procedure that flags hardware-induced defects with physically realizable witnesses.
       Methodologically, this transfers to the PLC domain the target-model discipline long established for safety-critical
       embedded C (Frama-C’s machine model [12], Astrée [13]), with the novelty that the HAL model is derived
       automatically from the program’s PLCopen I/O addresses.
    2. ESBMC-Arduino: an Arduino instantiation (§6). A HAL library whose parameters are sourced from the official
       Arduino cores [14], and a realization of the input-range model as a lightweight (≈40-line) hook in the Efficient
       SMT-based Context-Bounded Model Checker (ESBMC) LD frontend – the Satisfiability Modulo Theories (SMT)
       backend and k-induction engine are reused unchanged.
    3. Evaluation on real and controlled corpora (§8). On 123 real third-party IEC 61131-3 programs, naive 16-bit
       overflow checking yields a 44 % false-alarm rate and zero true findings; the HAL annotator eliminates all 54 false
       alarms (54→0) while preserving every robustness proof. A controlled corpus demonstrates the genuine width-
       dependent defects the method detects (with realizable witnesses) and precisely characterizes which arithmetic
       patterns are vulnerable, thereby establishing, honestly, that the gap is real but rare in the public corpora we could
       ingest.

1.3    Scope

We target the integer/Boolean fragment of IEC 61131-3, deployed via open-hardware toolchains, and evaluate at the
model level (no hardware-in-the-loop). Non-linear floating-point function blocks (e.g. Proportional-Integral-Derivative
(PID), transcendental sensor linearization) are outside the deployment-gap claim and are soundly over-approximated
(§5); we discuss this and other limitations in §10.


                                                              2
                      ESBMC-Arduino: Closing the Deployment Gap for Open-Hardware PLCs                        A P REPRINT



Why it Matters
Open-hardware PLCs are not toys: they run real water, lighting, and process-control logic, and they are the default
substrate for the academic ICS security testbeds on which much of the field’s empirical work depends. A safety or
security argument built on abstract verification of such a system is only as sound as the assumption that the abstract
model matches the device – an assumption this paper shows to be false in a precise, reproducible way, and then repairs.
The repair is cheap (a four-field descriptor and a 40-line hook) and reuses a mature verifier, so it is realistic to adopt
rather than a clean-slate proposal.

Roadmap
§2 reviews the scan cycle, the OpenPLC toolchain, the machine models of Arduino targets, and the verification
backend. §3 positions the work against PLC verification and target-faithful embedded-C analysis. §4 formalizes the
deployment gap; §5 presents the method (descriptor, lowering, soundness; Fig. 6); §6 gives the Arduino instantiation and
implementation; §7 walks through two end-to-end scenarios; and §8 reports the evaluation. §9–11 discuss implications,
threats, and future work.


2     Background

2.1   The PLC Scan Cycle

A PLC executes a deterministic scan cycle: it reads all inputs into a process image, executes the user program once
from first rung to last, writes the output image to the actuators, and repeats [9]. The ESBMC-PLC line encodes this as a
while(true) loop in which inputs are re-sampled each iteration (an open-world sensor model) nondeterministically,
output coils are persistent state, and safety properties are injected as assertions; k-induction then proves invariants for
all future scans. We reuse this encoding and add a faithful model of the hardware boundary that the scan cycle crosses
on a real device.

2.2   Open-Hardware PLCs and the OpenPLC Toolchain

Open-hardware PLCs run IEC 61131-3 programs on commodity microcontroller boards. OpenPLC [1, 2] is the domi-
nant open-source example: its editor exports PLCopen XML, and its runtime compiles the program (via MATIEC [15])
to C, which is then cross-compiled for Arduino-, ESP32-, or Raspberry Pi-class targets. Arduino OPTA [3] is
Arduino’s industrial micro-PLC, programmed in IEC 61131-3 via the Arduino PLC IDE [4]; CONTROLLINO [5] and
Industrial Shields M-Duino [6] are Arduino-compatible industrial PLCs commonly driven by OpenPLC. All reduce a
vendor-neutral program to C plus a hardware binding (the object we verify).

2.3   The Hardware Abstraction Layer (HAL): Word Width, Pin Binding, ADC, and PWM

The HAL connects logical IEC 61131-3 variables to physical peripherals. Each Boolean %IX/%QX address binds to a
General-Purpose Input/Output (GPIO) pin; analog inputs are read through an ADC of finite resolution (typically 10–14
bits) and scaled; analog outputs are produced by PWM. Two facts of this layer drive the deployment gap: (i) the MCU’s
native word width – 16-bit int on AVR-class boards – so computations exact in the abstract model can overflow; and
(ii) the bounded input domains – an n-bit ADC reading lies in [0, 2n − 1], a digital input in {0, 1} – which the abstract
model omits entirely (Fig. 1).

2.4   PLCopen XML

LD programs are exchanged as PLCopen XML in textual and graphical encodings, reconstructed into rungs by the
ESBMC-GraphPLC Depth-First Search (DFS) resolver [8]. Open-hardware editors export the graphical encoding;
crucially, the variable declarations carry explicit %IX/%IW addresses, which we exploit as the ground truth for HAL input
binding. The IEC 61131-3 direct-addressing scheme is itself the bridge between logic and hardware: a location prefix
names the memory area (I input, Q output, M internal) and a size prefix names the width (X bit, B byte, W word, D double
word). Thus %IX0.0 is a single digital input bit, while %IW0 is a 16-bit analog input word; on an open-hardware target,
the former is wired to a GPIO pin read by digitalRead and the latter to an ADC channel read by analogRead. The
address, therefore, encodes the information our method needs precisely – whether a variable is an input and, if analog,
the width of the channel feeding it – without any additional annotation by the Engineer.


                                                            3
                        ESBMC-Arduino: Closing the Deployment Gap for Open-Hardware PLCs                                           A P REPRINT



                               Abstract IEC 61131-3                                     Arduino-class MCU
                                 (unbounded int)    HAL descriptor                         (16-bit int)
                                        %IX0.0 :                                                GPIO
                                                                        bind
                                         BOOL                                                 digital in
                                                                                                           {0, 1}
                                                                                                ADC
                                       %IW0 : INT                      scale
                                                                                                n-bit
                                                                                                           [0, 2n −1]
                                                                                                PWM
                                       %QW0 : INT                      PWM
                                                                                                (duty)

                                        %QX0.0 :                                                GPIO
                                                                        bind
                                         BOOL                                                 digital out

Figure 1: The HAL binds logical IEC 61131-3 variables to physical peripherals: Boolean %IX/%QX addresses map to
GPIO pins, analog inputs are read through a finite-resolution ADC and scaled, analog outputs are produced by PWM.
Two facts about this layer drive the deployment gap: the MCU’s native 16-bit word width and the bounded input
domains that the abstract model omits.


2.5   From PLCopen XML to a Binary: the OpenPLC Toolchain

Understanding where the deployment gap enters requires following a program from the editor to the device. In the
dominant open-source flow, the OpenPLC Editor exports a PLCopen XML project; the OpenPLC runtime invokes
the MATIEC compiler [15] to translate the IEC 61131-3 Program Organization Unit (POU)s into portable C (one
function per POU, plus a generated config_run__ driver that executes one scan); this C is then cross-compiled by the
board’s standard toolchain (avr-gcc for AVR boards, arm-none-eabi-gcc for ARM boards) and linked against a board-
specific runtime that maps the located %I/%Q addresses onto the digitalRead/digitalWrite/analogRead/analogWrite
primitives of the Arduino core. Three observations follow. First, the semantics that finally execute are those of C
compiled for the target Application Binary Interface (ABI) – in particular, integer arithmetic is performed at the target’s
int width, not at the abstract model’s idealized width. Second, the inputs are not free: each is produced by a peripheral
with a fixed range. Third, none of this is visible at the PLCopen XML level that existing verifiers analyze, which is
exactly why the gap is missed today (Fig. 2).

                                                                              What actually executes (target ABI + peripherals)
      Analyzed by existing verifiers
                                             deployment gap




                                                              MATIEC → C            Board toolchain         Board runtime
                                                                                                                                   Device
      OpenPLC           PLCopen XML                            one fn / POU           avr-gcc /               %I/%Q →
                                                                                                                                  (executes
       Editor              project                                   +                arm-none-               digital/
                                                                                                                                  one scan)
                                                              config_run__            eabi-gcc               analogRead


Figure 2: Open-source PLC deployment: OpenPLC Editor → PLCopen XML → MATIEC C compilation ([15]) →
cross-compilation + runtime mapping %I/%Q to Arduino I/O primitives. Verifiers analyze the abstract model (left), but
real semantics (integer widths, bounded I/O) appear only post-compilation (right), creating the deployment gap between
them.

2.6   Machine Models of Arduino-Class Targets

The single most consequential difference between the abstract model and the deployed artifact is the machine word
width, fixed by the target ABI. On the 8-bit AVR architecture that powers the Arduino Uno, Nano, Mega, and the
Arduino-compatible CONTROLLINO Micro/Maxi and Industrial Shields M-Duino, the C int is 16 bits (range
[−32,768, 32,767]), following the avr-gcc ABI. On the 32-bit ARM Cortex-M cores that power the Arduino Due,
Zero, MKR, UNO R4, and the industrial OPTA, int is 32 bits. Table 2 (§6) summarizes the relevant parameters. The
consequence is stark and routinely surprising to engineers: the multiplication x*100 that is harmless on a Due overflows
on a Uno once x exceeds 327, because the result leaves the 16-bit range and wraps under two’s-complement semantics.
Analog peripherals compound this: the AVR ADC is 10-bit (readings 0 . . . 1,023) and analogWrite drives an 8-bit
PWM duty (0 . . . 255), whereas the UNO R4 offers a 14-bit ADC; the combination of a narrow word and a wide sensor
range is precisely the regime in which scaling arithmetic overflows. We take all of these parameters from the official


                                                                          4
                      ESBMC-Arduino: Closing the Deployment Gap for Open-Hardware PLCs                                   A P REPRINT



Arduino cores [14] rather than asserting them, so the machine model is auditable and exactly matches what ships on the
device.

2.7    Bounded Model Checking and k-Induction for PLCs

Our backend is ESBMC [16, 17], an SMT-based Bounded Model Checking (BMC) engine. BMC unrolls the scan loop
a bounded number of times k and encodes “does a property violation occur within k scans?” as an SMT formula whose
satisfying assignment, if any, is a concrete counterexample trace [17]. Because ESBMC models machine integers as
fixed-width bit-vectors, arithmetic overflow and two’s-complement wrap-around are reproduced bit-precisely – the
property of the solver we rely on to detect width-dependent defects, and the reason a faster word-agnostic abstraction
would be unsound here. Plain BMC is a falsifier: it finds bugs up to depth k but does not prove their absence.
To obtain unbounded proofs over the non-terminating scan loop, ESBMC uses k-induction [18, 17]: a base case checks
the first k scans, and an inductive step shows that if the property holds for k consecutive scans it holds for the next, with
internal state hacked. For a per-scan, state-independent property such as “the scaling arithmetic does not overflow,” the
inductive step typically closes at small k; for properties whose proof requires reasoning about loop-carried internal
state – as in function blocks with internal counters – the inductive step may fail to close, yielding an inconclusive
unknown verdict rather than safe. This distinction explains both why our method proves many programs robust and
why a residual set remains unknown (§8). Overflow itself is encoded as a verification condition: for a subtraction a-b
of signed type, ESBMC asserts !overflow("-", a, b), whose negation the solver tries to satisfy within the modeled
input ranges (Fig. 3).

                                                                                                                   per-scan, state-
                                                                                                                  independent (e.g.
                                                                                                                scaling: no overflow)
                          ESBMC: SMT-based                                        Inductive step:
                                                          Base case:                                                   safe
    Non-terminating        BMC + k-induction                              no     k scans ⇒ next?       closes
                                                       violation in the                                              unbounded
      scan loop        int = fixed-width bit-vector                               (internal state
                                                        first k scans?                                                 proof
                       (overflow / wrap bit-precise)                                havocked)
                                                               yes                       fails

                                                          unsafe                     unknown
                                                       counterexample              inconclusive

                                                                               loop-carried internal
                                                                                  state (function-
                                                                                  block counters)

Figure 3: Verification with ESBMC: BMC unrolls the scan loop k times and encodes violations as bit-vector SMT
formulas, capturing overflow and wrap-around exactly. k-induction closes state-independent properties at small k (safe)
but may leave loop-carried state open (unknown). Overflow itself is checked as a condition, e.g., !overflow("-", a,
b) for signed subtraction—with the solver seeking inputs within modeled ranges.


3     Related Work
We situate the work along three axes – verification of IEC 61131-3, target-faithful analysis of embedded software, and
code-generation correctness – and summarize the positioning in Table 1.

3.1    Verification of IEC 61131-3

The most mature open-source effort is PLCverif [10, 11], developed at Conseil Européen pour la Recherche Nucléaire
(CERN) and in production since 2019; it accepts Siemens Structured Control Language (SCL) and dispatches to
Bounded Model Checking for ANSI-C Programs (CBMC), nuXmv, or Theta, with engineer-facing requirement
patterns.
Earlier and complementary academic tools include:
         • Arcade.PLC [19], which provides counterexample-guided analysis and value-set abstraction over several
           IEC 61131-3 languages;
         • Model-checking frontends that translate Instruction List (IL) or ST into the input languages of NuS-
           MV/nuXmv [20].


                                                              5
                      ESBMC-Arduino: Closing the Deployment Gap for Open-Hardware PLCs                       A P REPRINT



A complementary and fast-growing line establishes precise formal semantics for IEC 61131-3 and analyzes richer
execution settings:
       • K-ST gives an executable semantics for ST [21];
       • Lee and Bae [22] formalize multitask ST with preemption;
       • Closest to our cyber-physical concern, Lee and Bae [23] formalize networked PLCs interacting with physical
         environments;
       • FRET-based monitor synthesis extends PLCverif with requirement formalization [24];
       • Cooperative verification orchestrates multiple backends via CoVeriTeam [25];
       • Ladder logic has been formalized for fault-tolerance analysis [26].
Industrial practice mirrors this – an SMT-based ladder-to-model-checker translation is patented for network anomaly
detection [27].
The ESBMC-PLC line targets the ESBMC backend specifically:
       • ESBMC-PLC [7] introduced a native textual PLCopen XML LD frontend with k-induction;
       • ESBMC-GraphPLC [8] added the graphical encoding via a DFS rung resolver;
       • ESBMC-PLC+ [9] added ST/SCL ingestion through MATIEC and scan-cycle-accurate semantics for timer,
         counter, and edge function blocks.
What unites all of these tools – commercial and academic alike – is that they verify an abstract model of the control
logic: integers are mathematical (or fixed at a host width chosen for convenience, typically 32 bits), and inputs are
unconstrained. None models the word width of the deployment target or the bounded domains of the physical inputs.
The deployment gap is therefore orthogonal to and composable with each of these efforts; our method could, in principle,
be layered onto PLCverif or Arcade.PLC as readily as onto ESBMC.

3.2   Target-Faithful Analysis of Embedded Software

The discipline we transfer to the PLC domain is well established for handwritten embedded C.
       • Frama-C [12] carries an explicit machine model selected with -machdep (e.g. avr fixes a 16-bit int), and its
         value analysis obtains input ranges from ACSL contracts written by the Engineer.
       • Astrée [13], the abstract interpreter used in avionics certification, reliably reports integer and floating-point
         overflow in the target’s arithmetic and derives input bounds from volatile-range and known_fact annotations.
       • Industrial static analyzers in the same lineage detect overflow under a configured target model.
All of these “deal with the gap” in exactly the manner we advocate – target machine model plus bounded inputs – which
is precisely why our approach is defensible rather than speculative.
Two differences distinguish our work.
      1. The object of analysis is IEC 61131-3, not C: the Engineer never sees or writes the generated C, so any
         hardware model must be expressed at, or recovered for, the PLC level.
      2. And centrally, those tools require the input ranges to be supplied manually (as contracts or annotations),
         whereas we derive them automatically from the IEC 61131-3 direct-addressing scheme: a %IW location is, by
         the standard, an analog input word, and the board descriptor fixes its ADC width. The Engineer writes nothing.

3.3   Code-Generation Correctness

A separate body of work establishes that a code generator preserves semantics from model to executable:
       • CompCert [28] for general-purpose C-to-assembly.
       • Qualified generators such as SCADE KCG in the model-based-design world.
These guarantees are real but orthogonal: even a perfectly verified translation does not prevent a program’s own
arithmetic from overflowing on a small target, because the overflow is a property of the source semantics under the
target word width, not of the translation. Our method is complementary – it checks the property that code-generation
correctness deliberately does not.


                                                            6
                       ESBMC-Arduino: Closing the Deployment Gap for Open-Hardware PLCs                              A P REPRINT


Table 1: Positioning: who models the deployment target. “Auto inputs” = hardware input ranges derived automatically
rather than supplied by hand

                Approach                         IEC 61131-3        Word width    Input ranges        Auto inputs
                PLCverif [10]                          ✓                 –             –                  –
                Arcade.PLC [19]                        ✓                 –           partial              –
                ESBMC-PLC+ [9]                         ✓                 –             –                  –
                CBMC [29]                              –                 ✓           manual               –
                Frama-C [12]                           –                 ✓          contracts             –
                Astrée [13]                            –                 ✓           annot.               –
                This work (ESBMC-Arduino)              ✓                 ✓             ✓                  ✓



4     The Deployment Gap, Formally

4.1     Physical Process and Fault Model

An open-hardware PLC is one element of a closed cyber-physical loop (Fig. 4). A physical process – a tank, a burner, a
conveyor – is observed by sensors whose continuous signals are digitized by the MCU’s ADC into integer codes; the
scan-cycle logic reads those codes, computes in the MCU’s finite-width integer arithmetic, and drives actuators through
digital pins and PWM, which in turn act on the process. A safety property is ultimately a property of this loop – “the
high-level alarm actuates before the tank overflows” – realized in software as an assertion over the program variables
that bind to the physical I/O. The cyber and the physical meet at exactly two surfaces: the ADC that turns a bounded
physical quantity into an integer (so each input has a hardware-realizable range, not the full machine word), and the
integer arithmetic that runs at the target’s word width (so a computed actuation command can wrap). These two surfaces
are the locus of the deployment gap.

                                               ADC              Scan logic
              Physical
                             Sensor           (10-bit:          (16-bit int       PWM / GPIO              Actuator
              process
                                            [0, 1,023])         arithmetic)
                                                                                 word-width surface
                                         input-range surface
                                                    actuation closes the loop


Figure 4: The cyber-physical loop of an open-hardware PLC. The deployment gap lies at the two interfaces where
computation meets physical I/O: the ADC bounds each input to a hardware-realizable range (10-bit, [0, 1,023]), and the
scan logic executes 16-bit integer arithmetic at the target word width. Properties verified against the abstract logic alone
ignore both, rendering the verification unsound with respect to the actual hardware.


4.1.1    Fault model
We do not assume a malicious adversary; the fault we target is a latent computational fault induced by legitimate
physical inputs. A program that is correct in the abstract model can, on a narrow-word target, compute the wrong
actuation for a perfectly ordinary sensor reading – an integer overflow in an ADC-to-engineering-unit conversion
silently inverts a comparison and suppresses a safety action. The fault is triggered by inputs the environment routinely
produces (within D(a), the bounded domain D of physically realizable values for analog input a), is invisible at the
PLC-logic level existing verifiers analyze, and manifests only once the logic is composed with a specific board’s HAL.
Dually, an unconstrained input model fabricates faults the environment can never trigger (inputs outside D(a)): these
are the phantom alarms of §8. A faithful model must therefore admit exactly the physically realizable inputs – no more,
no less.

4.1.2    Assumptions
We assume the standard PLC scan-cycle timing model (§5.1): inputs are sampled at the top of each scan and held
constant during rung evaluation, so we reason about values, not intra-scan transients, and we do not model continuous
plant dynamics, sensor noise, or actuator latency – the property is the per-scan logical assertion, and the environment
is the open-world set of realizable input vectors. Within this model, the gap is purely a function of the program, the
property, and the board HAL H, which is what makes it amenable to the bit-precise analysis that follows.


                                                               7
                        ESBMC-Arduino: Closing the Deployment Gap for Open-Hardware PLCs                          A P REPRINT



Let P be a program and φ a safety property. Existing tools check Mabs (P ) |= φ, where Mabs is the abstract scan-cycle
model (§5.1) with idealized arithmetic (word width w → ∞) and free inputs (D(i) = Z). What runs on the board is
Mdev (P, H): the same control logic composed with a board HAL H that (i) evaluates arithmetic in the MCU’s finite
word width w and (ii) constrains each input to its hardware-realizable domain D(i).
Definition 1 (Deployment gap). The deployment gap of (P, φ) on target H is the situation in which the two models
disagree on φ: either Mabs (P ) |= φ while Mdev (P, H) ̸|= φ (a missed defect: safe in the abstract, unsafe on the device),
or Mabs (P ) ̸|= φ under free inputs while Mdev (P, H) |= φ (a phantom: an abstract counterexample that no hardware
input can realize). The first direction motivates detection; the second, as RQ2 shows, dominates in practice and renders
naive width-checking unsound (Fig. 5).



                                   Mdev (P, H) |= φ                  Mdev (P, H) ̸|= φ
                                    safe on device                   unsafe on device

            Mabs (P ) |=
                                          agree:                        missed defect
                 φ                                                                               motivates
                                           safe                      safe in the abstract,       detection
              safe in
                                                                    unsafe on the device
             abstract

            Mabs (P ) ̸|=               phantom                            agree:
                 φ              abstract counterexample                genuine defect
            free inputs        no hardware input realizes

                                    dominates in practice
                                   (RQ2 §8) – makes naive
                                   width-checking unsound

Figure 5: Deployment gap as model agreement (diagonal) vs. disagreement (anti-diagonal) on φ. Missed defects (top-
right) are device-unsafe but abstract-safe – requiring detection. Phantoms (bottom-left) are abstract counterexamples
unreachable in hardware, hence device-safe. RQ2 (§8) shows phantoms dominate, making naive width-checking
unsound. Diagonal cells indicate genuine agreement.


Three mechanisms populate the gap.

        1. (M1) Binding errors: an %IX/%QX address mapped to the wrong physical pin, or two addresses aliased to one
           pin, so that an output write clobbers an unrelated signal – a fault in µ rather than in the logic, modeled by the
           io_map and detectable as a property over the bound variables.

        2. (M2) ADC quantization: a physical level maps to one of only 2badc discrete codes, so a threshold test such as
           “alarm exactly at 50.0 %” may straddle two representable codes and never hold with equality; we model a read
           as a nondeterministic representable value, a sound over-approximation of any rounding policy.

        3. (M3) Bounded-width arithmetic: an operation that is exact in Mabs exceeds [−2w−1 , 2w−1 ) and wraps under
           two’s-complement semantics in Mdev . Formally, an operation ⊙ on w-bit operands computes a ⊙ b mod 2w
           reinterpreted as signed, so a ⊙ b is faithful iff a ⊙ b ∈ [−2w−1 , 2w−1 ); outside that interval the device silently
           produces a different value. (M3) is the dominant cause of overflow defects and the focus of this paper;
           (M1) and (M2) are expressible in the same framework and are future work (§11).


4.1.3    Motivating example

Listing 1 shows an analog high-level alarm from the OpenPLC water/dimmer pattern: a 10-bit ADC read-
ing is scaled to a percentage, and an alarm fires at ≥ 80%. The property is “if the sensor is at/above
the high mark (adc ≥ 819) the alarm must be ON.” Under Mabs (32-bit) ESBMC proves it (k=2). Under
Mdev for an AVR board, where int is 16-bit, the product adc × 100 wraps for high readings; ESBMC re-
ports a violation with counterexample adc = 898 (tank ≈88%), where the alarm stays silent – a missed high-


                                                               8
                      ESBMC-Arduino: Closing the Deployment Gap for Open-Hardware PLCs                         A P REPRINT



level alarm caused purely by the word width.             The two models differ only in the HAL-injected arithmetic.
1        int adc = nondet_int ();           // HAL: 10- bit ADC
2        __ESBMC_assume (adc >= 0 && adc <= 1023);
3        int16_t prod     = adc * 100;      // HAL - faithful width on AVR
4        int16_t percent = prod / 1023;     // wraps for high adc
5        bool    Alarm    = ( percent >= 80);
6        if (adc >= 819) assert (Alarm);    // engineer ’s safety property
Listing 1: Deployment-gap motivating example. Abstract int (32-bit)⇒SAFE; deployed int16_t (AVR)⇒missed
alarm at adc = 898.


5     Hardware-Faithful Verification
Given a program P and a HAL descriptor H, the method constructs a deployment model Mdev (P, H). It verifies
the safety property φ against it, reusing the ESBMC backend and k-induction unchanged (Fig. 6). We first fix the
underlying execution model, then define H, the lowering, and its soundness.

                                                               HAL descriptor
                                                            H = ⟨w, badc , bpwm , µ⟩
                                                                                                                safe
                                                                                                          robustness proof
                               LD front-end /
                                                              Faithful lowering           ESBMC
    PLCopen XML                  MATIEC→                                                                        unsafe
                                                                width w; input           k-induction
      program                      GOTO                                                                   realizable witness
                                                              assume; FB abstr.         (bit-precise)
                      Intermediate Representation (IR)
                                                                                                             unknown
                                                                                                          (completeness)

Figure 6: ESBMC-Arduino pipeline. A PLCopen program is lowered to a GOTO IR; the faithful lowering (§5.3),
parameterized by the board’s HAL descriptor, fixes the word width and injects hardware input bounds before bit-precise
k-induction. Setting w wide yields the abstract reference Mabs ; the per-board w yields Mdev . The backend is reused
unchanged.


5.1    Scan-Cycle Execution Model

We model a PLC program as a transition system T = (S, s0 , R) over a state S that partitions variables into inputs
I, outputs O, and internal state V. One scan is the relation scan ⊆ S × S that (i) re-samples every input i ∈ I,
(ii) executes the program body once, updating O and V, and the system iterates scan indefinitely. A safety property φ is
an assertion required to hold after every scan. Two parameters of this model are left implicit by existing verifiers but
fixed on a real device: the interpretation of arithmetic operators (the word width w at which +, −, × are evaluated,
with two’s-complement wrap outside [−2w−1 , 2w−1 )) and the input domains (the set D(i) ⊆ Z from which each i ∈ I
may be sampled). The abstract model Mabs takes w large and D(i) = Z; the deployment model Mdev (P, H) takes both
from H (Fig. 7.

5.2    The Hardware Abstraction Layer (HAL) Descriptor

A HAL descriptor is a tuple H = ⟨w, badc , bpwm , µ⟩ where w is the machine word width (int_bits), badc and bpwm
are the ADC and PWM resolutions in bits, and µ (the io_map) assigns each IEC address class a role and domain (Eq. 1).
                    µ(%IX) = ⟨in, {0, 1}⟩,    µ(%IW) = ⟨in, [0, 2badc −1]⟩,       µ(%QX), µ(%QW) = out.                   (1)

H is small, declarative, and reusable across all programs for a given board; Table 2 lists the instances we use. Crucially,
H is independent of P : the per-program input bounds are obtained by composing H with the addresses already present
in P .

5.3    Faithful Lowering

The lowering P 7→ Mdev (P, H) is the identity on the control logic and modifies only the hardware boundary, via four
transformations (Algorithm 1):


                                                              9
                      ESBMC-Arduino: Closing the Deployment Gap for Open-Hardware PLCs                        A P REPRINT



                        next scan (scan ⊆ S × S)


                      init      Sample inputs              Execute body                 Check φ
                             ∀i ∈ I : i ← D(i)         update O, V at width w          (after scan)



                                    Fixed by H on the device:
                                    word width w (two’s-complement wrap outside [−2w−1 , 2w−1 ))
                                    input domain D(i) ⊆ Z
                                    Mabs : w large, D(i) = Z | Mdev (P, H): both from H

Figure 7: The scan-cycle execution model. Each scan resamples the inputs, executes the program body once, and
ensures that the safety property φ holds afterward; the system iterates scan indefinitely. Two parameters left implicit by
existing verifiers are fixed on a real target: the arithmetic word width w and the per-input domains D(i). The abstract
model Mabs leaves both unconstrained; the deployment model Mdev (P, H) takes both from the HAL descriptor H.


 1. Word width. All machine integers are interpreted as w-bit bit-vectors, so every arithmetic operator wraps exactly
    as on the target. In ESBMC, this is the word-width setting for the architecture; no program rewriting is required.
 2. Input-range annotation.
                             For each input i ∈ I with address a, immediately after i is re-sampled in scan we inject
    assume i ∈ D(a) with D(a) the domain from µ. Booleans receive {0, 1} (already implied by their type and
    thus a no-op); analog/integer inputs receive [0, 2badc − 1]. This single step is what restores soundness in practice.
 3. Quantization and saturation. An ADC read is modeled as a nondeterministic value within the representable set –
    a sound over-approximation that subsumes any rounding policy – and a PWM write is clamped to [0, 2bpwm − 1].
 4. Non-linear abstraction. A function block whose body uses floating-point or transcendental operations (e.g. PID,
    thermistor linearization) is replaced by a fresh nondeterministic output constrained to its declared range. This is a
    sound over-approximation that removes SMT-intractable arithmetic outside the integer deployment-gap claim.


Algorithm 1 Faithful lowering P, H 7→ Mdev
 1: set machine word width to H.w                                                                  ▷ bit-precise arithmetic
 2: for each input i with address a sampled in scan do
 3:     emit i ← nondet()                                                             ▷ open-world re-sample (existing)
 4:     if µ(a) is analog/integer then emit assume(0 ≤ i ≤ 2H.badc − 1)
 5:     end if
 6: end for
 7: for each analog output write o ← e do
 8:     emit o ← clamp(e, 0, 2H.bpwm − 1)
 9: end for
10: for each non-linear function-block instance f do
11:     replace body of f by outf ← nondet_in_range()
12: end for
13: return resulting model, to be checked with overflow VCs + k-induction



5.4   Soundness and Gap Diagnosis

Let Reachdev be the states reachable on the physical device (arithmetic at width w, inputs from their true hardware
ranges D(a)), and ReachMdev those of the constructed model. The soundness argument assumes the descriptor is
faithful: H.w equals the target’s int width and, for every input address a, D(a) contains the true hardware range of
that input (Fig. 8). Under this premise the lowering preserves all device behavior:
Theorem 1 (Soundness). For a HAL descriptor H that correctly captures the target’s word width and input domains,
Reachdev ⊆ ReachMdev (P,H) . Consequently, if Mdev (P, H) |= φ then the deployed program satisfies φ on the device
(modulo the non-linear abstraction). Every counterexample reported on Mdev (P, H) uses inputs in D(a) and is
therefore physically realizable.


                                                           10
                     ESBMC-Arduino: Closing the Deployment Gap for Open-Hardware PLCs                                   A P REPRINT



                 inputs unconstrained: D(i) = Z            inputs ∈
                                                                  / D(a): removed by assume (phantom alarms of Mabs )


                                              ReachMdev (P,H) (inputs ∈ D(a), width w)
                                                                                 non-linear over-approx.
                                                                                 (Lemma 1)
                                                      Reachdev
                                                   (physical device)              reported CEX:
                                                                                  inputs ∈ D(a) ⇒ realizable




Figure 8: Soundness as state-set containment (Theorem 1). Under a faithful descriptor H, the states reachable on the
physical device are contained in those of the model, Reachdev ⊆ ReachMdev (P,H) ; the only slack is the non-linear
over-approximation (Lemma 1). Hence Mdev (P, H) |= φ implies the device satisfies φ. Because the injected assumes
admit only inputs in D(a), every reported counterexample (orange star) is physically realizable; the hatched band of
states reachable only with inputs ∈
                                  / D(a) – the phantom alarms of the unconstrained Mabs – is excluded.


The argument is a containment: width-w arithmetic is reproduced exactly (not abstracted), each non-linear function
block is replaced by a nondeterministic over-approximation of its declared outputs, and the injected assumes remove
only inputs the device never produces. So no device behavior is excluded, and every counterexample is realizable. The
supporting lemma and full proof are deferred to Appendix A.
The dual – that the abstract model is unsound for the device – also follows: without the assumes, Mabs admits inputs
outside D(a), so an Mabs counterexample need not be realizable (Scenario 2, §7.2). Gap diagnosis compares the two
models on the same program and property with the same input bounds, so they differ only in w: a verdict that is safe
under Mabs but unsafe under Mdev isolates a defect attributable solely to the deployment word width, reported with
a realizable witness. Completeness is inherited from the backend and is partial: BMC falsifies up to depth k and
k-induction proves when the inductive step closes; for programs whose proof depends on loop-carried internal state the
step may not close, yielding unknown (§8) – an incompleteness of the prover, independent of the lowering.

6     ESBMC-Arduino: Arduino Instantiation and Implementation
6.1   Arduino Instantiation

We instantiate the method for Arduino. The HAL library fixes H per board with parameters taken from the official
Arduino cores [14]: AVR (ArduinoCore-avr) gives int_bits=16, adc_bits=10, pwm_bits=8; 32-bit references (Due,
UNO R4, OPTA) give int_bits=32 with 12–14-bit ADCs (Table 2). Our primary focus is the 16-bit AVR boards
(Uno/Nano/Mega), the dominant low-cost open-hardware PLCs. The pipeline ingests a PLCopen program through the
native LD frontend, applies the faithful lowering for the chosen board, and verifies with ESBMC at the target word
width; the reference run uses the abstract model (wide integers, same input bounds).

                    Table 2: Board HAL descriptors (parameters from the official Arduino cores)

                Board                                                  Core / MCU            int       ADC      PWM
                Uno/Nano/Mega, CONTROLLINO, M-Duino                    -avr (AVR)          16-bit          10      8
                Due                                                    -sam (ARM)          32-bit          12      8
                UNO R4                                                 -renesas (ARM)      32-bit          14      8
                OPTA                                                   -mbed (ARM)         32-bit          12      –



6.2   Implementation

A design goal of the method is to be minimally invasive: the deployment model should reuse a mature verifier rather
than reimplement one. We therefore realize the lowering inside the existing ESBMC LD frontend, changing only where
the model meets the hardware boundary.


                                                                11
                       ESBMC-Arduino: Closing the Deployment Gap for Open-Hardware PLCs                        A P REPRINT



6.2.1    Where the Hook Sits
The LD frontend builds a GOTO IR in which one scan is a loop body that first re-samples the inputs (the open-world
sensor model of §2.7) and then evaluates the rungs. Inputs are re-sampled at two sites: the program-level READ_INPUTS
step, which assigns each physical input a fresh nondeterministic value, and the function-block input-sampling step,
which does the same for an instantiated block’s formal inputs. The annotator attaches at exactly these two sites,
immediately after each nondeterministic assignment, so that the bound applies to the freshly sampled value on every
scan.

6.2.2    What the Hook Emits
For an input variable of integer type, the hook synthesizes a guard 0 ≤ v ≤ ADCMAX as a relational IR expression.
It wraps it in a assume node inserted into the scan body (Listing 2). The bound is taken from the board descriptor
(HAL_ADC_MAX, default 1,023 for the AVR 10-bit ADC); Boolean inputs already range over {0, 1} by type and need no
guard, and floating-point inputs are left unconstrained (they fall under the non-linear abstraction). Gating on the static
type keeps the transformation sound for mixed-type programs.
1   codet ld_converter :: hal_input_bound ( const symbol_exprt &in) const {
2       if ( getenv (" HAL_ANNOTATE ") == nullptr ) return code_skipt (); // baseline
3       if (! is_integer (in.type ()))              return code_skipt (); // BOOL/REAL
4       long adcmax = env_long (" HAL_ADC_MAX ", 1023) ;                  // board param
5       exprt lo = binary_relation_exprt (in , " >=", from_integer (0, in.type ()));
6       exprt hi = binary_relation_exprt (in , " <=", from_integer (adcmax , in.type ()));
7       return code_assumet ( and_exprt (lo , hi));                       // assume bound
8       }

           Listing 2: The annotator hook (abridged): after an input is re-sampled, bind it to the ADC domain.


6.2.3    Configurability and Engineering
The model is toggled by HAL_ANNOTATE and parameterized by HAL_ADC_MAX, so a single binary reproduces both the
naive baseline and hardware-faithful configuration – the basis for the controlled before/after in §8. Word width is set by
ESBMC’s –16/–32 flag, and overflow is governed by the standard verification condition; neither requires modification.
The hook is ≈40 lines, confined to the frontend, and adds no dependencies: the GOTO encoding, SMT backend,
k-induction engine, and solver are unchanged. This confinement lets Theorem 1 rest on the backend’s existing soundness
– we add assumptions and set a width, but do not alter the proof engine. The same hook bounds function-block inputs,
including IN1 in the worked example (§7.2).

7     The Approach in Practice
We walk through two end-to-end scenarios on real artifacts. Each is presented in two passes: an Engineer’s view (what
happens and what to do about it), followed by an under the hood paragraph with the formal detail. The two scenarios
cover the two faces of the deployment gap: detecting a genuine hardware-induced defect (§7.1), and not raising a false
alarm on correct code (§7.2) – the latter being, in practice, the more common and the reason the input model is essential.

7.1     Scenario 1: A Program that is Safe in the Editor but Unsafe on a Uno

7.1.1    Engineer’s View
Consider the analog high-level alarm of Listing 1: a tank level is read from a 10-bit ADC, scaled to a percentage, and an
alarm is asserted to fire at ≥ 80%. In the OpenPLC editor, and under any abstract verifier, the logic is correct – the alarm
always fires when the tank is high. Deployed to an Arduino Uno (an AVR board), however, the alarm silently fails at
high levels. ESBMC-Arduino reports the violation and, crucially, hands back the exact sensor reading that triggers it:
1       # AVR / Uno target (16 - bit), HAL input model enabled
2       $ HAL_ANNOTATE =1 esbmc alarm .ld --16 --overflow - check --k- induction
3         Counterexample : adc = 898
4         Violated property : arithmetic overflow on mul (adc * 100)
5         VERIFICATION FAILED
6       # 32- bit reference (e.g., OPTA), same input bounds
7       $ HAL_ANNOTATE =1 esbmc alarm .ld --32 --overflow - check --k- induction
8         VERIFICATION SUCCESSFUL

                  Listing 3: Running the deployment check; the counterexample is a real ADC reading.


                                                            12
                       ESBMC-Arduino: Closing the Deployment Gap for Open-Hardware PLCs                         A P REPRINT



The engineer reads this directly: at a tank reading of 898 (≈ 88%) the alarm does not fire on a 16-bit board. The
physical consequence closes the loop of Fig. 4: the high-level alarm that should trip the inflow never actuates, so the
tank keeps filling past the high mark – a safety action silently lost to a word-width overflow, not to any logic error the
Engineer could see in the editor. The fix is equally concrete – use a wider intermediate (DINT) for the scaling, or deploy
on a 32-bit board – and re-running confirms the repair.

7.1.2    Under the Hood
The two runs are the deployment model Mdev and the abstract reference Mabs of §5, differing only in the machine word
width. The HAL annotator has constrained the input with assume(adc >= 0 && adc <= 1,023), so the counterexample
is realizable: at the 16-bit width adc × 100 for adc = 898 equals 89,800, which exceeds INT16_MAX=32,767 and
wraps, collapsing percent to 23 and falsifying the alarm. ESBMC proves the abstract model by k-induction at k=2 and
refutes the deployment model at the base case, attributing the verdict change solely to the word width.

7.2     Scenario 2: Avoiding a False Alarm on Correct Code

7.2.1    Engineer’s View
Take a real program from our corpus, lassignment, whose valve handler contains the assignment in Listing 4 – an
ordinary offset of an integer input. If one naively asks a verifier to check 16-bit overflow, it reports this correct code as
unsafe (Listing 5):
1   real_value := IN1 - 5;    (* IN1 is an INT input *)

                           Listing 4: Real code from valves_handler (program lassignment).

1       $ esbmc lassignment .ld --16 --overflow - check        # NAIVE : no input model
2         Counterexample : IN1 = -32764
3         Violated property : arithmetic overflow on sub (IN1 - 5)
4         VERIFICATION FAILED

             Listing 5: Naive checking flags a phantom overflow; the witness is an impossible sensor value.

A practitioner would rightly distrust this: the “bug” requires IN1 = −32,764, a value no real sensor or ADC can ever
produce. Chasing it wastes effort, and a tool that produces dozens of such reports (we measured 54 across the corpus) is
ignored. Enabling the HAL model makes the report disappear—the code is accepted (Listing 6):
1       # HAL model enabled (ADC inputs bounded to [0 ,1023])
2       $ HAL_ANNOTATE =1 esbmc lassignment .ld --16 --overflow - check
3         no arithmetic overflow on sub (IN1 - 5)

                               Listing 6: With the HAL input model the phantom is gone.


7.2.2    Under the Hood
The annotator emits, immediately after IN1 is sampled, assume(IN1 >= 0 && IN1 <= 1023) (the AVR 10-bit ADC
domain from the board descriptor). The overflow verification condition !overflow("-", IN1, 5) is then discharged: un-
der the bound, IN1-5 lies in [−5, 1,018], which cannot underflow a 16-bit integer, so the counterexample at INT16_MIN
is no longer reachable. The witness in the naive run was an artifact of an unconstrained input, not a property of the
program – exactly the unsoundness-in-practice the method removes.

8     Evaluation
We answer:

    • RQ1. Is the deployment gap real, and which arithmetic patterns are vulnerable?
    • RQ2. On real programs, is naive width-aware verification (no input model) usable?
    • RQ3. Does the HAL annotator make it sound – eliminating false alarms while preserving proofs?
    • RQ4. What is the performance, and what are the method’s completeness limits?


                                                             13
                     ESBMC-Arduino: Closing the Deployment Gap for Open-Hardware PLCs                      A P REPRINT



8.1   Setup and Methodology

All experiments use ESBMC v8.3.0 with our annotator hook and the Z3 backend, on a commodity laptop. The HAL
model is toggled per run via HAL_ANNOTATE, so that the naive baseline and the hardware-faithful configuration are
produced by the same binary, thereby isolating the input model as the only independent variable. Word width is set by
–16/–32 and overflow by the standard signed/unsigned overflow property; HAL_ADC_MAX=1023 (AVR 10-bit).
We use two corpora (Table 3). The real corpus comprises 123 third-party PLCopen XML programs that the LD frontend
ingests natively, drawn from two public datasets at pinned commits and archived in the artifact: a water-treatment
Ladder-Logic dataset [30] (60 programs) and an IEC 61131-3 clone-detection benchmark [31] (63 of 65 programs
ingest).
The controlled corpus is a taxonomy of HAL-effect classes – analog scaling and accumulation, each in a deliberately
buggy and a correctly-coded (_ok) variant – crossed with the board descriptors, designed to exhibit the isolation gap,
free of the confounds of arbitrary third-party code. The real corpus answers prevalence, false-alarm, and robustness
questions; the controlled corpus isolates the mechanism and characterizes which patterns are vulnerable.

Table 3: Evaluation corpora. The real corpus is third-party and pinned; the controlled corpus is authored to isolate the
deployment gap

                      Corpus    Source                             #    Role
                      Real      Water-treatment LD [30]           60    prevalence, FP, robustness
                      Real      Clone-detection [31]              63    prevalence, FP, robustness
                      Ctrl.     HAL-effect taxonomy (this work)   20    isolate gap, pattern analysis


8.2   RQ1: The Gap Is Real but Rare

The Gap is Real (Controlled Corpus)
The same program and property flip from safe under Mabs to unsafe under Mdev on the 16-bit boards, each with a
realizable witness (Table 4); the correctly-coded _ok variants never flip, on any board, confirming that the flips track
a genuine hardware-induced overflow rather than a modelling artifact. On the 32-bit board, the buggy variants are
themselves safe, isolating the word width as the sole cause – the same program is correct on a Due and unsafe on a
Uno.

Which Patterns are Vulnerable
The flip condition is precise and instructive for practitioners. With an input bounded to a 10-bit ADC (v ≤ 1,023), a
16-bit overflow (> 32,767) requires the arithmetic to magnify v past the word range: multiply by a constant ≳ 33 (e.g.
percentage or milli-unit scaling, v × 100), accumulation of many readings, or squaring. Conversely, multiply-by-small-
constant (v × 2), additive offsets (v ± c), and comparisons all remain within range and are provably safe – which is why
the _ok variants, and the bulk of real code, do not flip.

The Gap is Rare in the Corpora We Surveyed
We surveyed the real corpus and a larger pool of public Structured-Text libraries for the vulnerable pattern. Within
these corpora, the pattern is essentially absent: across 341 ST programs in a verification benchmark library, none
contained a multiply-by-a-three-or-more-digit constant; the integer arithmetic that does occur is dominated by ×2,
offsets, clamping, and comparisons – operations that bounded inputs keep safe. The public PLC code we could ingest
is overwhelmingly Boolean and timer logic with small-magnitude integer arithmetic. We therefore report, honestly,
that in these corpora the deployment gap is genuine and sound to detect but infrequent; the analog-scaling regime in
which it bites (e.g. ADC-to-engineering-unit conversion on a narrow-word board) is real but not the common case
here. We caution that this prevalence finding is scoped to the integer/Boolean LD programs our frontend ingests (§10);
analog-heavy process-control corpora may exhibit it more often. This finding reframes the contribution: the value of
hardware-faithful verification lies less in bug count than in the soundness it restores (RQ2–RQ3).

8.3   RQ2: Naive Width-Aware Verification Is Unusable

A natural first attempt at hardware-faithful verification is to set the word width and check overflow, without modeling
the inputs. We ran exactly this on the 123 real programs at 16 bits (Table 5, “Naive”). 54/123 (44 %) report unsafe, and


                                                          14
                      ESBMC-Arduino: Closing the Deployment Gap for Open-Hardware PLCs                      A P REPRINT


Table 4: Verdict matrix: identical logic and properties, abstract model vs. per-board deployed model. Unsafe = ESBMC
found a counterexample

                    Class    Abstract    CTRL Micro        CTRL Maxi        M-Duino       Arduino OPTA
                                           16-bit            16-bit          16-bit           32-bit
                    A_bug    safe           unsafe          unsafe          unsafe            safe
                    A_ok     safe            safe            safe            safe             safe
                    B_bug    safe           unsafe          unsafe          unsafe            safe
                    B_ok     safe            safe            safe            safe             safe



inspection shows every one is a spurious overflow on an unphysical input. The reports are strikingly uniform: all are
overflow on a subtraction of the form IN − c for a small constant c, with counterexamples pinned at the boundary of the
signed range – e.g. IN=-32,764 ≈ INT16_MIN, so that IN-5 underflows. No 10-bit ADC, and indeed no physical input
wired through the standard Arduino core, can ever present such a value.
Two controls confirm the diagnosis. First, the same 54 programs fail identically at 16 and 32 bits: the trigger is the
unbounded input, not the word width (a width-dependent defect would, by definition, differ between the two). Second,
the remaining programs are split into 32 that verify safe and 37 that are unknown for reasons unrelated to inputs
(§ RQ4). Naive width-aware checking therefore exhibits a 44 % false-alarm rate while finding zero genuine defects – a
signal-to-noise ratio that makes it unusable for assurance, since an engineer cannot distinguish its phantom reports from
real ones without manually re-deriving each input’s physical range.

              Table 5: Real corpus (123 programs), 16-bit overflow checking: naive vs. HAL-annotated.

                                  Configuration             safe   unknown      unsafe
                                  Naive (no input model)     32        37            54
                                  HAL-annotated              32        91             0



8.4   RQ3: The HAL Annotator Restores Soundness

Enabling the HAL model – the same binary, the only change being the injected input bounds – transforms the picture
(Table 5, “HAL-annotated”). All 54 false alarms are eliminated: the unsafe count drops from 54 to 0, and every one
of the 32 robustness proofs is preserved. The mechanism is exactly as analyzed: bounding each integer input to its
realizable ADC range constrains, for instance, IN − 5 to [−5, 1,018], which cannot underflow a 16-bit integer, so the
boundary counterexample becomes unreachable. No genuine defect is suppressed in the process, because (RQ1) none
of the real programs contains the vulnerable high-magnitude arithmetic; were one present, the bound would leave its
overflow witness intact and realizable.
The 32 preserved safe verdicts are themselves a positive result: they are robustness certificates – proofs that those
programs do not overflow at 16 bits for any physically realizable input, the kind of evidence a deployment safety case
requires. This is the central finding of the paper: the HAL input model makes width-aware verification of open-hardware
PLCs sound in practice where naive checking is not, converting a 44 %-noise tool into one that issues only realizable
reports.

8.5   Cross-Tool Validation: the Gap Is Not Tool-Specific

A natural objection is that the phantom alarms are an ESBMC idiosyncrasy. They are not. We reproduced the two faces
of the gap on an independent, peer SMT-based bounded model checker, CBMC [29], run on C mirrors of the same
logic with its native machine-width flag (–16/–32) and signed-overflow checking (Table 6). Three findings stand out.
First, the phantom is cross-tool: on the unconstrained IN1-5 pattern CBMC reports the very same spurious overflow,
with the identical witness IN1=−32,764 that ESBMC produces – confirming the false alarm is a property of naive
width-aware checking, not of one engine. Second, it is input-driven, not width-driven: the phantom fails at both
16 and 32 bits, whereas the genuine alarm defect fails only at 16 bits (with the realizable witness adc = 819) and
verifies safe at 32 bits – the cross-tool analog of our RQ2 control. Third, and decisively for our contribution, CBMC
can use an input bound but cannot derive one: removing the phantom required us to insert the bound by hand as
__CPROVER_assume(0<=IN1<=1023), exactly the manual annotation that C-level analyzers (Frama-C’s ACSL contracts,
Astrée’s known_facts) also demand.


                                                           15
                      ESBMC-Arduino: Closing the Deployment Gap for Open-Hardware PLCs                      A P REPRINT



Our method automatically recovers the same bound from the PLCopen %IW address – the “Auto inputs” column of
Table 1 – which makes it deployable at corpus scale without per-program specification effort. We confirmed the same
three findings on a second, architecturally different analyzer: Frama-C’s EVA abstract interpreter [12] (v32.1, -machdep
avr_16) raises the identical signed-overflow alarm assert -32768 <= IN1-5 on the naive program; bounding the input
with a handwritten Frama_C_interval(0,1023) (Frama-C’s analogue of an ACSL contract, again supplied manually)
makes it disappear; and the genuine adc*100 defect alarms at avr_16 but is clean at x86_32. Astrée, in the same lineage,
detects overflow under a configured target model with annotation-supplied input bounds. Across three independent
engines, then, the phantom, its input-driven nature, and the manual-annotation requirement are invariant – only the
automatic derivation of the bound from the PLC address space is ours.

Table 6: External baseline on C mirrors of the deployment-gap cases (signed-overflow checking). Verdicts are identical
on CBMC 6.10.0 and Frama-C/EVA 32.1 (-machdep avr_16), and match ESBMC. The phantom is reproduced cross-
tool; only the genuine defect is width-dependent; the bound that clears the phantom must be supplied by hand in every
tool
                         Case                Input model        16-bit    32-bit    Diagnosis
                         IN1-5 (phantom)     none (naive)       fail      fail      input-driven
                         IN1-5 (phantom)     manual assume      safe      safe      bound by hand
                         adc*100 (alarm)     input bounded      fail      safe      width-dependent


8.5.1    Replication on the Real Corpus and the Actual Generated Code
The cases above are faithful but handwritten. To confirm the result on the real programs and the actual deployment C,
we took all 54 programs that ESBMC’s naive run flagged, reconstructed the ST function blocks holding the flagged
arithmetic from each PLCopen file, compiled them to C with MATIEC [15] – the same code generator the OpenPLC
toolchain uses – and ran CBMC at the AVR width with each integer function-block input made nondeterministic. The
outcome is unambiguous: CBMC independently reproduces the overflow on all 54/54 programs with no input model,
and the hand-supplied HAL bound eliminates it on all 54/54 – a cross-tool replication of the keystone 54→0 result on
the real MATIEC-generated code, not on mirrors. Two honest caveats: under the bound CBMC’s bounded check returns
overflow-safe (where ESBMC’s k-induction returns unknown on the same programs, §8, RQ4), so the tools agree on
the absence of the overflow but differ on proof strength; and the malicious_* dataset variants additionally contain a
non-terminating logic-bomb loop, an orthogonal non-termination property we do not treat here. This experiment is fully
scripted in the artifact.

8.6     RQ4: Performance and Completeness

Performance
Verification is fast (Table 7). On the controlled corpus, the median solve time is 168 ms (max 412 ms); on the real
corpus, runs complete well under a second per program. The HAL annotator adds only a pair of assume constraints per
input and leaves the SMT encoding otherwise unchanged, so its overhead is negligible – and, by shrinking each input’s
domain from the full word to a 10-bit range, it can make solving easier.

                  Table 7: Per-program solve time (ESBMC v8.3.0, Z3 backend, commodity laptop)

                                Corpus                               #     Median       Max
                                Controlled (HAL-effect taxonomy)    20     168 ms      412 ms
                                Real (third-party)                  123     < 1s        < 1s


Completeness
A genuine limit remains, and we state it plainly. The 54 eliminated false alarms become unknown rather than safe: the
spurious overflow is gone, but the prover does not prove those programs safe. The cause is k-induction incompleteness
on function-block-heavy programs. Tracing one such case, ESBMC unwinds an internal function-block loop to the
default bound, reports that “the forward condition is unable to prove the property,” and that the inductive step does not
close because it must havoc-loop-carry internal state.
This is a property of the prover, not of the input model: 37 of these programs are already unknown in the naive run, and
enabling the annotator neither helps nor harms their proof (it only removes the false unsafe). Interval analysis [32] and


                                                           16
                      ESBMC-Arduino: Closing the Deployment Gap for Open-Hardware PLCs                        A P REPRINT



bounded-proof configurations did not change the outcome. Closing these – via loop-invariant inference or compositional
k-induction – would raise the robustness-proof count above the current 32 and is the most valuable direction for future
work (§11). The headline soundness result (54→0 false alarms) is independent of this limit.


9    Discussion

The strongest contribution of this work is not a bug count but a soundness result: open-hardware PLC verification that
accounts for the word width but ignores the hardware input domains is unusable (44% false alarms, zero true findings),
and a small, automatically-derived HAL model restores usability (54→0 false alarms) while preserving every proof.
This mirrors how target-faithful embedded-C analysis is judged [13]: value lies in sound proofs and the absence of false
alarms, not in headline defect counts. An analyzer that cries wolf is switched off; one that issues only realizable reports
is trusted.
RQ1 lets us tell practitioners precisely when to worry. The deployment gap manifests when bounded-range sensor
data is magnified by integer arithmetic beyond the narrow machine word: ADC-to-engineering-unit scaling (raw *
span/range), running sums and integrators, and squared terms, all deployed on a 16-bit AVR board. Boolean interlocks,
timers, counters with small presets, and offset/threshold logic are safe by construction and need no special attention.
This is actionable guidance independent of our tool: an engineer porting a recipe or PID-like computation from a 32-bit
controller to a Uno-class board should widen intermediates to DINT or verify with a hardware-faithful model.
The embedded-C analyzers that pioneered target-faithful analysis require the Engineer to supply input ranges as
contracts or annotations. In the PLC setting, that burden would fall on an automation engineer unfamiliar with formal
specification, and – for a corpus of 123 programs – would dominate the effort. Recovering the bounds from the
IEC 61131-3 direct-addressing scheme removes the burden entirely: the %IW/%IX address is the specification of the
input’s nature, and the board descriptor supplies the width. The Engineer writes nothing, which is what makes the
method deployable at the corpus scale.
Although we instantiate for Arduino, neither the method nor the implementation is Arduino-specific. The HAL
descriptor is a four-field record; retargeting to another open-hardware family (e.g. an ESP32-based controller, or a
32-bit industrial soft-PLC) is a matter of supplying its word width and ADC/PWM resolutions. The same hook, applied
with a 32-bit width, reproduces the abstract behavior, so the method strictly generalizes existing abstract verification
rather than replacing it.


10    Threats to Validity

The naive baseline and the annotated runs are produced by the same binary, differing only by the HAL_ANNOTATE
toggle, so the measured 54→0 change is attributable to the input model alone and not to incidental differences in tool
configuration. Verdicts agree between –16 and –32 on all 54 naive failures, an independent check that those reports are
input-driven rather than width-driven.
Modelling an integer IEC input as a 10-bit ADC source is the AVR HAL assumption encoded in H. An input physically
wired to a wider ADC (e.g. a 14-bit UNO R4 channel), to a digital word, or to a network variable would carry a different
domain; the descriptor is configurable per address, and a mis-specified bound would be unsound in the same way a
wrong -machdep would be for Frama-C. In this study, every integer input is treated uniformly as a 10-bit analog source,
the conservative common case for the AVR boards; finer per-address domains are a straightforward extension once
richer I/O metadata is available.
91/123 programs are unknown owing to k-induction limits on loop-bearing function blocks (§8), bounding the robustness-
proof count to 32. We emphasize this is a backend limitation orthogonal to the contribution: it is present with and
without the input model, and the soundness result (no false alarms, no suppressed real defects) holds regardless. It does,
however, mean we cannot claim “123 programs proven robust,” only “54 false alarms removed and 32 robustness proofs
retained.”
The deployment gap is rare in the public corpora we could ingest, which are dominated by Boolean/timer logic. Analog
process-control corpora (e.g. ICS testbeds in REAL arithmetic) where high-magnitude scaling – and hence the gap –
may be more common fall outside our current frontend (REAL/non-linear support is partial) and are not represented;
our prevalence claim is therefore scoped to integer/Boolean LD programs. The two datasets are third-party and pinned,
but they are not the universe of PLC code.
The non-linear abstraction is sound but imprecise: a property that genuinely depends on a PID output cannot be proved
under it (it will be unknown or spuriously unsafe on the abstracted output). Hence, the method is most precise on the


                                                           17
                      ESBMC-Arduino: Closing the Deployment Gap for Open-Hardware PLCs                       A P REPRINT



integer fragment it targets. Finally, we validate at the model level; we do not execute the verified binaries on physical
boards, so the soundness guarantee is relative to the faithfulness of H and the frontend’s semantics rather than measured
against silicon. Hardware-in-the-loop confirmation is future work.


11    Future Work

Several directions follow directly from the limitations above.
The most valuable next step is to convert the 91 unknown verdicts into safe robustness proofs, by strengthening
k-induction over function-block internal state – loop-invariant inference, or compositional k-induction that verifies each
function block once and composes the results, avoiding the monolithic unwinding that currently fails to close.
The same framework expresses mechanisms (M1) and (M2): modeling ADC quantization precisely (representable-code
sets rather than intervals) would let the method find threshold-straddling defects, and modeling pin binding from the
io_map would catch aliasing faults; both are properties over the existing model rather than new machinery.
A fixed-point abstraction of non-linear blocks would be more faithful than the current nondet over-approximation –
and is itself how such computations are often realized on an MCU – enabling sound, precise verification of the analog
programs presently out of scope, and opening the ICS-testbed corpora where the gap may be more prevalent.
Per-address ADC widths and engineering-unit scaling recovered from the project file would replace the uniform 10-bit
assumption with exact per-input domains.
Finally, executing the verified programs on physical Uno/Due boards and confronting the synthesized witnesses (e.g.
adc = 898) with measured behavior would close the loop between the model-level guarantee and the device, and is the
natural validation of the soundness theorem.


12    Conclusion

We presented hardware-faithful verification of IEC 61131-3 on open hardware – a declarative HAL descriptor and
a sound lowering that models the target word width and hardware-realizable input ranges – as well as its Arduino
instantiation, ESBMC-Arduino. On 123 real programs, naive width-aware verification is unusable (44% false alarms,
zero true findings); the automatically derived HAL input model eliminates all false alarms while preserving every proof,
and a controlled corpus characterizes the genuine, if rare, width-dependent defects that the method soundly detects.


Artifact Availability

The corpus (pinned, with provenance), the annotator patch, and the scripts reproducing every table are archived
in an anonymized Zenodo deposit, https://doi.org/10.5281/zenodo.21014209 (concept DOI 10.5281/zen-
odo.21014209, resolving to the latest version); author identity and the paper DOI are withheld for double-anonymous
review and restored at camera-ready. The artifact is self-contained: two scripts (setup.sh, reproduce.sh) install the
pinned tools – CBMC 6.10.0, Frama-C 32.1, matiec, and our patched ESBMC (the HAL annotator, built from the bun-
dled source) – and regenerate every claim with a single command. The supported environment is x86_64 Ubuntu 22.04;
safe/unsafe verdicts are deterministic across hosts (only wall-clock times vary), and a claim-to-command-to-expected-
output map accompanies the scripts. An independent continuous-integration pipeline that rebuilds the entire toolchain
from source on a clean Ubuntu 22.04 image reproduces every verdict-based result in this paper identically; only the
performance figures (Table 7) are host-dependent.


Appendix

A    Soundness: Supporting Lemma and Proofs

This appendix supplies the lemma and full proof underlying the Soundness theorem (Theorem 1, §5.4). We first isolate
the only step of the lowering that is an abstraction rather than an exact match.
Lemma 1 (Non-linear over-approximation). Replacing the body of a non-linear function block by a fresh nondetermin-
istic value constrained to the block’s declared output range yields a transition relation whose reachable states form a
superset of those of the original block.


                                                           18
                     ESBMC-Arduino: Closing the Deployment Gap for Open-Hardware PLCs                       A P REPRINT



Proof. The block is type-correct, so every value its body can compute lies within the declared output range. Hence, for
each transition of the original block, there is a nondeterministic choice in the abstracted block that reaches the same
successor state; the abstraction additionally admits choices the body never makes. The abstracted relation, therefore,
contains the original one and adds behaviors.

Proof of Theorem 1. The lowering changes the device’s transition relation only by (a) fixing arithmetic at the true width
w – an exact match, not an abstraction – and (b) replacing each non-linear block body by a nondeterministic value
ranging over a superset of its actual outputs. Step (b) only adds behaviors by Lemma 1. The input-range assumes remove
behaviors, but only those with inputs outside D(a), which the device never exhibits; hence, no device behavior is
excluded. Therefore Reachdev ⊆ ReachMdev , giving the φ-preservation. Realisability is immediate: a counterexample
satisfies the injected assume(i ∈ D(a)) for every input, so its inputs are values the hardware can produce.

Acknowledgements
The authors would like to express their gratitude to the Department of Computer Science at the University of Manchester
and the Systems and Software Security (S3) Research Group for their invaluable support, collaborative environment,
and access to cutting-edge resources, which were instrumental in the success of this research. This work was conducted
with partial funding from the Engineering and Physical Sciences Research Council (EPSRC) grants EP/T026995/1,
EP/V000497/1, EP/X037290/1, and the Soteria project, awarded by UK Research and Innovation under the Digital
Security by Design (DSbD) Programme.

References
 [1] Thiago Alves and Thomas Morris. Openplc: An iec 61131-3 compliant open source industrial controller
     for cyber security research. Computers & Security, 78:364–379, September 2018. ISSN 0167-4048. doi:
     10.1016/j.cose.2018.07.007.
 [2] Thiago Rodrigues Alves, Mario Buratto, Flavio Mauricio de Souza, and Thelma Virginia Rodrigues. Openplc: An
     open source alternative to automation. In IEEE Global Humanitarian Technology Conference (GHTC 2014), page
     585–589, San Jose, CA, USA, October 2014. IEEE. doi: 10.1109/ghtc.2014.6970342.
 [3] Arduino.        Arduino OPTA: Micro PLC with industrial IoT.                   https://www.arduino.cc/pro/
     hardware-arduino-opta/, 2024. Accessed 2026-06-27.
 [4] Arduino. Arduino PLC IDE: IEC 61131-3 programming for arduino pro hardware. https://www.arduino.cc/
     pro/software-plc-ide/, 2024. Accessed 2026-06-27.
 [5] CONTROLLINO. CONTROLLINO: Arduino-compatible industrial PLC. https://www.controllino.com/,
     2024. Accessed 2026-06-27.
 [6] Industrial Shields. M-Duino arduino-based PLC family. https://www.industrialshields.com/, 2024.
     Accessed 2026-06-27.
 [7] Pierre Dantas, Lucas C. Cordeiro, and W. S. Silva Júnior. ESBMC-PLC: Formal verification of IEC 61131-3
     ladder diagram programs, 2026. TACAS 2027 artefact. Reproducible viabash conformance/run_all.sh.
 [8] Pierre Dantas, Lucas C. Cordeiro, and W. S. Silva Júnior. ESBMC-GraphPLC: Formal verification of graphical
     PLCopen XML ladder diagram programs using SMT-based model checking, 2026.
 [9] Pierre Dantas, Lucas C. Cordeiro, and W. S. Silva Júnior. ESBMC-PLC+: Unified IEC 61131-3 formal verification
     framework with ST frontend and graphical function block support (pull request #5427). GitHub Pull Request #5427,
     esbmc/esbmc, 2026. URL https://github.com/esbmc/esbmc/pull/5427. Source code and benchmark
     suite.
[10] Jean-Charles Tournier, Borja Fernández Adiego, and Ignacio D. Lopez-Miguel. PLCverif: Status of a formal verifi-
     cation tool for programmable logic controller. In Proceedings of the 18th International Conference on Accelerator
     and Large Experimental Physics Control Systems (ICALEPCS’21), page MOPV042, Shanghai, China, October
     2021. JACoW Publishing. ISBN 978-3-95450-221-9. doi: 10.18429/JACoW-ICALEPCS2021-MOPV042.
[11] Ignacio D. Lopez-Miguel, Borja Fernández Adiego, Matias Salinas, and Christine Betz. Formal Verification
     of PLCs as a Service: A CERN-GSI Safety-Critical Case Study, pages 227–235. Springer Nature Switzerland,
     Williamsburg, VA, USA, June 2025. ISBN 9783031937064. doi: 10.1007/978-3-031-93706-4_13.
[12] Florent Kirchner, Nikolai Kosmatov, Virgile Prevosto, Julien Signoles, and Boris Yakobowski. Frama-c: A
     software analysis perspective. Formal Aspects of Computing, 27(3):573–609, May 2015. ISSN 1433-299X. doi:
     10.1007/s00165-014-0326-7.


                                                           19
                     ESBMC-Arduino: Closing the Deployment Gap for Open-Hardware PLCs                    A P REPRINT



[13] Patrick Cousot, Radhia Cousot, Jêrome Feret, Laurent Mauborgne, Antoine Miné, David Monniaux, and Xavier
     Rival. The astreÉ analyzer. In Programming Languages and Systems, page 21–30, Edinburgh, UK, 2005. Springer
     Berlin Heidelberg. ISBN 9783540319870. doi: 10.1007/978-3-540-31987-0_3.
[14] Arduino. ArduinoCore-avr: the official arduino avr core. https://github.com/arduino/ArduinoCore-avr,
     2024. ADC 10-bit, analogWrite/PWM 8-bit; AVR-GCC int = 16-bit. Accessed 2026-06-28.
[15] Edouard Tisserant, Laurent Bessard, and Mario de Sousa. An open source iec 61131-3 integrated development
     environment, July 2007. ISSN 1935-4576.
[16] Lucas Cordeiro, Bernd Fischer, and Joao Marques-Silva. Smt-based bounded model checking for embedded
     ansi-c software. IEEE Transactions on Software Engineering, 38(4):957–974, July 2012. ISSN 0098-5589. doi:
     10.1109/tse.2011.59.
[17] Mikhail R. Gadelha, Rafael S. Menezes, and Lucas C. Cordeiro. ESBMC 6.1: Automated Test Case Generation
     Using Bounded Model Checking. International Journal on Software Tools for Technology Transfer, 23(6):857–861,
     May 2020. doi: 10.1007/s10009-020-00571-2.
[18] Mary Sheeran, Satnam Singh, and Gunnar Stålmarck. Checking safety properties using induction and a sat-solver.
     In Formal Methods in Computer-Aided Design, page 127–144, Berlin, 2000. Springer Berlin Heidelberg. ISBN
     9783540409229. doi: 10.1007/3-540-40922-x_8.
[19] Matthias Weis, Philipp Marks, Benjamin Maschler, Dustin White, Pascal Kesseli, and Michael Weyrich. Towards
     establishing formal verification and inductive code synthesis in the PLC domain. In 2021 IEEE 19th International
     Conference on Industrial Informatics (INDIN), pages 1–8, Palma de Mallorca, Spain, July 2021. IEEE. doi:
     10.1109/INDIN45523.2021.9557423.
[20] Roberto Cavada, Alessandro Cimatti, Marco Dorigatti, Alberto Griggio, Alessandro Mariotti, Andrea Micheli,
     Sergio Mover, Marco Roveri, and Stefano Tonetta. The nuXmv symbolic model checker. In Computer Aided
     Verification (CAV 2014), volume 8559 of Lecture Notes in Computer Science, pages 334–345, Vienna, Austria,
     2014. Springer. doi: 10.1007/978-3-319-08867-9_22.
[21] Kun Wang, Jingyi Wang, Christopher M. Poskitt, Xiangxiang Chen, Jun Sun, and Peng Cheng. K-st: A formal
     executable semantics of the structured text language for plcs. IEEE Transactions on Software Engineering, 49
     (10):4796–4813, October 2023. ISSN 2326-3881. doi: 10.1109/tse.2023.3315292.
[22] Jaeseo Lee and Kyungmin Bae. Formal Semantics and Analysis of Multitask PLC ST Programs with Preemption,
     pages 425–442. Springer Nature Switzerland, Milan, Italy, September 2024. ISBN 9783031711626. doi:
     10.1007/978-3-031-71162-6_22.
[23] Jaeseo Lee and Kyungmin Bae. Formal Analysis of Networked PLC Controllers Interacting with Physical
     Environments, pages 328–356. Springer Nature Switzerland, Singapore, Singapore, October 2025. ISBN
     9783032071064. doi: 10.1007/978-3-032-07106-4_14.
[24] Xaver Fink, Anastasia Mavridou, Andreas Katis, and Borja Fernández Adiego. Verifying PLC Programs via
     Monitors: Extending the Integration of FRET and PLCverif, page 427–435. Springer Nature Switzerland, Moffett
     Field, CA, USA, 2024. ISBN 9783031606984. doi: 10.1007/978-3-031-60698-4_26.
[25] Chibuzo Ukegbu and Hoda Mehrpouyan. Cooperative verification of PLC programs using CoVeriTeam: Towards
     a reliable and secure industrial control systems. In Proceedings of Cyber-Physical Systems and Internet of Things
     Week 2023, CPS-IoT Week ’23, pages 37–42, San Antonio, TX, USA, May 2023. ACM. doi: 10.1145/3576914.
     3587490.
[26] Ali Ebnenasir. Formalizing ladder logic programs and timing charts for fault impact analysis and
     verification of fault tolerance. Technical Report CS-TR-23-01, Michigan Technological University,
     Department of Computer Science, 2023. URL https://www.mtu.edu/cs/research/papers/pdfs/
     formalizing-ladder-logic-ali-ebnenasir-tech-rpt-010623-rev.pdf.
[27] Roberto Bruttomesso, Alessandro Di Pinto, Moreno Carullo, and Andrea Carcano. Method for automatic
     translation of ladder logic to a SMT-based model checker in a network. US Patent 11,906,943. Assignee: Nozomi
     Networks SAGL, 2024. Filed: 2021-08-12. Granted: 2024-02-20.
[28] Xavier Leroy. Formal verification of a realistic compiler. Communications of the ACM, 52(7):107–115, July 2009.
     ISSN 1557-7317. doi: 10.1145/1538788.1538814.
[29] Edmund Clarke, Daniel Kroening, and Flavio Lerda. A Tool for Checking ANSI-C Programs, page 168–176.
     Springer Berlin Heidelberg, Berlin, 2004. ISBN 9783540247302. doi: 10.1007/978-3-540-24730-2_15.
[30] Antonio Iacobelli, Lorenzo Rinieri, Andrea Melis, Amir Al Sadi, Marco Prandini, and Franco Callegati. Detection
     of ladder logic bombs in PLC control programs: An architecture based on formal verification. In 2024 IEEE 7th


                                                         20
                     ESBMC-Arduino: Closing the Deployment Gap for Open-Hardware PLCs                    A P REPRINT



     International Conference on Industrial Cyber-Physical Systems (ICPS), pages 1–7, St. Louis, MO, USA, May
     2024. IEEE. doi: 10.1109/ICPS59941.2024.10639995.
[31] Kamil Rosiak et al. IEC 61131-3 clone detection dataset (plcopen xml / structured text). https://github.com/
     KamilRosiak/IEC_61131_3_Clone_Detection, 2022. Accessed 2026-06-28.
[32] Rafael Sá Menezes, Mohannad Aldughaim, Bruno Farias, Xianzhiyu Li, Edoardo Manino, Fedor Shmarov, Kunjian
     Song, Franz Brauße, Mikhail R. Gadelha, Norbert Tihanyi, Konstantin Korovin, and Lucas C. Cordeiro. ESBMC
     v7.4: Harnessing the Power of Intervals: (Competition Contribution). In Tools and Algorithms for the Construction
     and Analysis of Systems (TACAS 2024), volume 14572 of Lecture Notes in Computer Science, pages 376–380,
     Luxembourg City, Luxembourg, 2024. Springer Nature Switzerland. doi: 10.1007/978-3-031-57256-2_24.




                                                         21
