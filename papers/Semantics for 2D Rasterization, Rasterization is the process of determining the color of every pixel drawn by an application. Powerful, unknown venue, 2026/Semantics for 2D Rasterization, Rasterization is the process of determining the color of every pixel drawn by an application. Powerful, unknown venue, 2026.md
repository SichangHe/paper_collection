                                         Semantics for 2D Rasterization
                                         BHARGAV K KULKARNI, University of Utah, USA
                                         HENRY WHITING, University of Utah, USA
                                         PAVEL PANCHEKHA, University of Utah, USA
                                         Rasterization is the process of determining the color of every pixel drawn by an application. Powerful
                                         rasterization libraries like Skia, CoreGraphics, and Direct2D put exceptional effort into drawing, blending,
                                         and rendering efficiently. Yet applications are still hindered by the inefficient sequences of instructions that
                                         they ask these libraries to perform. Even Google Chrome, a highly optimized web browser co-developed with
arXiv:2603.23696v1 [cs.PL] 24 Mar 2026




                                         the Skia rasterization library, still produces inefficient instruction sequences even on the top 100 most visited
                                         websites. The underlying reason for this inefficiency is that rasterization libraries have complex semantics
                                         and opaque and non-obvious execution models.
                                            To address this issue, we introduce 𝜇Skia, a formal semantics for the Skia 2D graphics library, and mechanize
                                         this semantics in Lean. 𝜇Skia covers language and graphics features like canvas state, the layer stack, blending,
                                         and color filters, and the semantics itself is split into three strata to separate concerns and enable extensibility.
                                         We then identify four patterns of sub-optimal Skia code produced by Google Chrome, and then write replace-
                                         ments for each pattern. 𝜇Skia allows us to verify that the replacements are correct, including identifying
                                         numerous tricky side conditions. We then develop a high-performance Skia optimizer that applies these
                                         patterns to speed up rasterization. On 99 Skia programs gathered from the top 100 websites, this optimizer
                                         yields a speedup of 18.7% over Skia’s most modern GPU backend, while taking just 32 µs for optimization.
                                         The speedups persist across a variety of websites, Skia backends, and GPUs. To provide true, end-to-end
                                         verification, optimization traces produced by the optimizer are loaded back into the 𝜇Skia semantics and
                                         translation validated in Lean.
                                         CCS Concepts: • Computing methodologies → Rasterization; • Software and its engineering → Visual
                                         languages; Semantics.
                                         Additional Key Words and Phrases: Visual Languages, Rasterization, Computer Graphics, Compilers, Semantics,
                                         Automated Verification, Interactive Theorem Proving, Web Browsers

                                         1   Introduction
                                         Every pixel you see on a computer screen was produced by a process called rasterization. Programs
                                         like desktop, mobile, and web applications send a series of instructions to a rasterization library;
                                         these instructions draw shapes, render text, and blend overlapping visual elements. Then, the
                                         rasterization library—which might be Skia, CoreGraphics, Direct2D, Cairo, or something else—
                                         executes the instructions, determining the color of every pixel on the screen. Rasterization must be
                                         done at interactive rates, ideally 60 to 120 frames per second, to ensure a smooth experience for
                                         users. Rasterization libraries are thus highly optimized. Skia, for example, targets a wide variety of
                                         CPU- and GPU-based backends using both legacy and modern graphics APIs like OpenGL, Vulkan,
                                         and Metal. In fact, between 2021 and 2025, the Skia team wrote an entirely new backend, Graphite,
                                         to improve rasterization times by about 15% [9] by leveraging new GPU APIs. It’s therefore no
                                         surprise that Skia is the rasterization library of choice for the Google Chrome, Firefox, and Ladybird
                                         browsers, the Android operating system, the Flutter mobile application framework, as well as for
                                         native applications like Sublime Text.
                                            Despite this extreme performance focus, rasterization is not a solved problem. Web browsers,
                                         for example, struggle to render modern web pages, with trendy effects like partial transparency,
                                         animations, and blurs, at a stable 60 frames per second, especially on lower-end mobile devices.
                                         Authors’ Contact Information: Bhargav K Kulkarni, University of Utah, Salt Lake City, UT, USA, bhargavk@utah.edu;
                                         Henry Whiting, University of Utah, Salt Lake City, UT, USA, u1598085@utah.edu; Pavel Panchekha, University of Utah,
                                         Salt Lake City, UT, USA, pavpan@cs.utah.edu.


                                                                                                          , Vol. 1, No. 1, Article . Publication date: March 2026.
The trend toward 120 Hz displays only raises the bar. The reason this is so hard is that while
rasterization libraries implement individual instructions efficiently, clients ask them to execute ineffi-
cient instruction sequences. For example, the authors have manually examined the instructions that
Chrome executes to raster the top 100 websites (by traffic) and identified numerous straightforward
performance problems. And Chrome is surely the most sophisticated Skia client: it is developed at
the same company, with engineers working in such close coordination that Chrome and Skia make
simultaneous releases. Other Skia clients are even worse off. Improving the quality of rasterization
programs would dramatically reduce rasterization time, but doing that is unnecessarily difficult
because rasterization libraries have strange, imperative semantics and an opaque, non-obvious
execution model.
   We address this problem with 𝜇Skia, a formal semantics for the Skia 2D rasterization library.
𝜇Skia captures key features of the Skia API like canvas state, the layer stack, clipping, and blending.
More generally, since these features appear in all rasterization libraries, drawing from their common
PostScript heritage, we see our formalization as providing a foundation for future language-driven
rasterization research. Our formalization is built in three strata—a command language, a functional
core, and an abstract model—that seperate concerns, simplify reasoning, and allow for extensibility.
The semantics is mechanized in Lean and enables automated reasoning and verification of 𝜇Skia
programs.
   To demonstrate the utility of 𝜇Skia, we identify four patterns of suboptimal Skia instructions
generated by Google Chrome on the top 100 websites by traffic. For each one, we provide a more
efficient instruction sequence and prove the two sequences equivalent in Lean. 𝜇Skia enables us
to identify non-trivial side conditions and ensure that the optimization is correct. We then build
an optimizer that applies these rewrite rules before rasterization, enabling significant speed-ups
to rasterization. This simple optimizer results in an average speedup of 18.7% over Skia’s most
modern Graphite backend on 99 Chrome-generated Skia programs from the top 100 websites. The
optimizer is also highly efficient, with optimization taking at most 32 µs, and the optimizer improves
rasterization time across Skia back-ends and GPUs. Moreover, the optimizer is able to generate
optimization traces that can be translation validated using 𝜇Skia, providing an end-to-end proof of
correctness for those programs.
In short, the contributions in this paper are:
   (1) A new formalization of the Skia API and rasterization more generally (Section 3)
   (2) A collection of focused optimizations proven valid using this formalization (Section 4)
   (3) A efficient and correct Skia optimizer that applies these optimizations (Section 5).

2     Skia
Skia was originally an independent company founded by veterans of MacOS QuickDraw. Google
acquired Skia in 2005 [18], open-sourced the library, and has maintained it since. As of March 2026,
its AUTHORS file lists 109 contributors, and it cuts stable milestone releases every four weeks.
   A Skia client creates a “surface” and then issues commands to that surface by calling methods of
an associated SkCanvas object. Then, when a flush method is called, the commands are executed
to raster an image to the surface.1 Commands can also be stored in an intermediate command
buffer for serialization or replay. We take this command language to be a stand-alone programming
language and introduce its basic operations.

2.1    Drawing and Painting
The drawRect command draws a rectangle:
1 The CPU backend does execute commands eagerly, but most clients use the GPU backend.



                                                        2
                                   SkPaint p;
                                   canvas->drawRect(rect1, p);



Here, the layout is meant to evoke a Hoare triple: the left square shows the (empty) state of
the canvas before the drawRect command, while the right square shows the state of the canvas
afterwards. The first argument to drawRect is the rectangle to be drawn, but the second argument,
an SkPaint object, is more interesting. An SkPaint describes how a shape is drawn, for example
how to fill the shape. The default fill for a SkPaint is the color black, but we can also change it to
another color.

                                   SkPaint p;
                                   p.setColor(SK_ColorRED);
                                   canvas->drawRect(rect1, p);


It’s also possible to specify a non-constant fill, like a gradient:

                                   SkPaint p;
                                   p.setShader(
                                     SkShaders::LinearGradient(...));
                                   canvas->drawRect(rect1, p);

Formally, filling is a stage of Skia’s drawing pipeline, which assigns a color to every pixel in the
shape. More complex fills include images and shaders.

2.2    Blending
Things get a little more interesting once there is more than one shape being drawn. Suppose we
draw a second, overlapping, blue square:


                                   p.setColor(SK_ColorBLUE);
                                   canvas->drawRect(rect2, p);



   Conceptually, drawing this second shape involves two stages. First, as before, every pixel in
rect2 is assigned a fill color, here a solid blue. But then, this assigned fill color is blended with
the existing color for that pixel. That second stage is a bit difficult to see here, because the default
blend mode, called SrcOver, just chooses the new color.2 A program can, however, select a different
blend mode instead. For example, the Multiply blend mode combines both colors being blended:

                                   p.setColor(SK_ColorBLUE);
                                   p.setBlendMode(
                                     SkBlendMode::kMultiply);
                                   canvas->drawRect(rect2, p);
2 In reality, SrcOver blending is more complicated and depends on the opacity or alpha of the new color, which can matter

even for opaque fills due to anti-aliasing, but in our examples all the colors are opaque and we ignore anti-aliasing as a
simplification.

                                                            3
  In the intersection of the two rectangles, the initial red color is blended with the newly-drawn
blue fill, which in the Multiply blend mode results in black. Formally, blending is a stage in the
Skia drawing pipeline that comes after filling and combines the fill color assigned to each pixel
with the pre-existing color of that pixel.

2.3 Clipping
So far, drawRect has been applying the fill to the entirety of the shape being drawn. But Skia also
provides a clipRect command to restrict or clip the drawing bounds:3


                                     canvas->clipRect(clip_rect);
                                     canvas->drawRect(rect1, redPaint);


Note that clipRect command is run first, before the drawRect command. In fact, clipRect does
not modify the image at all; instead, it modifies canvas state that influences later draw operations.
Formally, that influence happens in yet another stage of the Skia drawing pipeline that comes
before filling and modifies the shape being drawn.
  The canvas state is stored in the canvas object and can affect multiple drawing commands:

                                     canvas->clipRect(clip_rect);
                                     canvas->drawRect(rect1, redPaint);
                                     canvas->drawRect(rect2, bluePaint);


  Naturally, one might want to limit which drawing commands a clip command applies to. Luckily,
Skia maintains a stack of canvas states; clipRect affects the top of the stack, which is used by
drawing commands, while save and restore commands push and pop from the stack:

                                     canvas->save();
                                     canvas->clipRect(clip_rect);
                                     canvas->drawRect(rect1, redPaint);
                                     canvas->restore();
                                     canvas->drawRect(rect2, bluePaint);

In other words, save and restore act like brackets, restricting the effect of clipRect to the
enclosed commands:

2.4    Layers
Besides the stack of canvas states modified by save and restore, there is a stack of drawing surfaces
and saveLayer and restore commands that push and pop from it. Conceptually, saveLayer
allocates a new, empty drawing surface:



                                     canvas->saveLayer();


3 Skia allows clipping with arbitrary shapes, but rectangle and rounded-rectangle clips are especially fast, using scissor tests.



                                                               4
   All drawing commands until the corresponding restore draw to this new surface.



                                   canvas->drawRect(rect2, bluePaint);




  Then, when the restore command is reached, the whole resulting drawing surface is blended
back into the original drawing surface.



                                  restore();




  The saveLayer operation accepts an SkPaint argument that can change the blend used during
restore. For example, with Multiply blending, the previous example would look like so:



                                  restore(); // multiply blending




2.5    Masking
One prominent use for saveLayer is masking. This refers to clipping one image based on the
contents of another image, and it can be achieved using saveLayer with DstIn blending:

                                   SkPaint blend_p;
                                   blend_p.setBlendMode(
                                     SkBlendMode::kDstIn);
                                   canvas->saveLayer(blendPaint);


  Here the initial state is the image to be masked, while the new layer represents the mask. We
now draw the mask shape on the new layer.


                                   SkPaint p;
                                   canvas->drawRect(rect1, p);
                                   canvas->drawRect(rect2, p);


   Finally, on restore, the initial image and the mask are combined using DstIn blending. DstIn
is very simple: it simply keeps all pixels from the bottom layer that are colored in in the top layer.4
4 The behavior with opacity is slightly more complex, but the same basic idea remains.



                                                            5
                            restore();




  DstIn blending is far more powerful than clipRect because it also allows masking with arbitrary
Skia-drawable images. For example, here is the previous image, masked with a radial gradient.



                            restore();




2.6    Equivalences
Nonetheless, simple rectangular clips can be achieved using either clipRect or with a saveLayer
with DstIn blending:

                            canvas->clipRect(rect1);
                            canvas->drawImage(...);



                            canvas->drawImage(...);
                            SkPaint b;
                            b.setBlendMode(SkBlendMode::kDstIn);
                            canvas->saveLayer(b);
                            SkPaint p;
                            canvas->drawRect(rect1, p);
                            canvas->restore();


   However, the saveLayer-based program is far less efficient than the clipRect-based one. It has
to allocate a whole new layer, draw additional pixels to it, and blend the results together, while
the clipRect-based one uses a fast path. In fact, it is common for the same image to be achievable
with many different Skia programs, some of which are much more efficient than others. This
motivates the rest of the paper: Section 3 develops a semantics, which allows proving that two Skia
programs have identical results. Section 4 uses that semantics to verify several rewrite rules over
Skia programs. And Section 5 then uses those rewrites to build a general-purpose Skia optimizer.
Section 6 demonstrates that this optimizer results in dramatically faster rasterization of a wide
range of real-world Skia programs.

3     Semantics
Our Skia semantics consists of three strata. The bottom-most stratum is an abstract model of
images, shapes, blends, and filters defined in terms of abstract types Point and Color, which can be
instantiated to model as much of the actual Skia API as necessary. The middle stratum is functional
operations DrawShape and BlendLayer parameterized by a Paint object, all of which denote to our
abstract model. The top stratum is an imperative language, 𝜇Skia, whose operational semantics
provides a model of Skia.

                                                 6
          Image      : Point → Color                     e.g. Solid(𝑐 : Color), LinearGradient(. . .), . . .
          Shape      : Point → Bool                      e.g. Rect(. . .), RRect(. . .), Path(. . .), Text(. . .)
          Blend      : Color × Color → Color             e.g. SrcOut, DstIn, . . .
          Filter     : Color → Color                     e.g. Id, Luma, . . .

Fig. 1. Our abstract model of Images and Shapes is built from abstract types Points and Colors. We also
include the various instantiations of the types of the abstract model we use in our formalization.


3.1    Abstract Model
In traditional programming language semantics, the abstract model—objects like pairs, functions,
integers, and the like—is implicit and well understood. In the graphics domain, the core types are
not so well established, so the abstract model must be explicitly defined. The abstract model for
𝜇Skia it is based around two core abstract types, Point and Color. The Point and Color types are
then used to define additional types, as shown in Figure 1. A special Transparent color is also
assumed. An Image is defined as a Color for every Point and Shapes are defined as predicates
on Points. Equivalence of two Images is defined extensionally: the same Color for each Point.
Additionally, since a major focus of this semantics is reasoning about color blending and filtration,
Blends and Filters are defined as binary and unary operators on colors.
   An instantiation of the abstract model would then define specific Images (solid color fills,
gradients, image files), Shapes (rectangles, paths, text outlines), Blends (roughly two dozen), and
Filters (a few built-in, but extensible with shaders), along with equivalences between them. Figure 1
shows some of the objects of each type. This provides extensibility for 𝜇Skia: an instantiation of
the abstract model can define more or fewer of these objects, and provide more or fewer theorems
about them, allowing a trade-off between the accuracy and complexity of our formalism. Our Lean
mechanization, for example, treats most shapes as entirely symbolic, with only minimal support
for reasoning about subset relations between them, sufficient for the rewrites of Section 4 and the
optimizer of Section 5. Future work may expand the abstract model or more carefully model its
objects so as to provide more theorems about them.
   The abstract model also provides some flexibility for choosing either simpler or more accurate
models of Point and Color. The actual Skia implementation defines Point to be a pair of 32-bit
floats and Color to be a 32-bit unsigned integer interpreted as ARGB pre-multiplied byte-sized
color,5 and operations on points and colors thus reflect effects from anti-aliasing and rounding.
The exact anti-aliasing and rounding behavior is not guaranteed by Skia and is also exceptionally
complex, including hardware dependence in some back-ends. Our Lean formalization instead uses
an abstract model where points and colors are represented by real numbers, which in practice
means it assumes away up to anti-aliasing and rounding.

3.2    Skia as Layers
The execution model of Skia centers around layers, which store images and are modified by drawing
and blending. Figure 2 thus introduces Layer objects with DrawShape and BlendLayer operations.
DrawShape draws a single shape 𝑠 on a Layer ℓ yielding the new state of ℓ, while BlendLayer
blends the layer ℓtop into ℓbot , yielding the new state of ℓbot . Each operation is parameterized by a
5“ARGB” gives the in-memory byte order of the alpha, red, green, and blue components of a color. The interpretation of

these bytes as an unsigned 32-bit integer will depend on the endianness of the platform itself. The colors are premultiplied,
meaning that a color with an alpha value of 𝛼 will have its red, green, and blue components range from 0 to 𝛼; this form
makes blending computations somewhat more efficient.


                                                             7
 Layer ::=                                                        Command ::=
 | Empty()                                                        | Draw(𝑔 : Shape, 𝑝 : Paint)
 | DrawShape(ℓ : Layer, 𝑠 : Shape, 𝑝 : Paint)                     | Clip(𝑚 : Shape)
 | BlendLayer(ℓbot : Layer, ℓtop : Layer, 𝑝 : Paint)              | Save(); 𝑐; Restore()
 Paint ::=                                                        | SaveLayer(𝑝 : Paint); 𝑐; Restore()
 | Paint(fill : Image, filter : Filter, blend : Blend)            | 𝑐; 𝑐

Fig. 2. Layer objects store images and are modified          Fig. 3. The 𝜇Skia command language. Note that
by drawing and blending operations. Each drawing or          Save/Restore and SaveLayer/Restore pairs are
blending operation is parameterized by a Paint object.       defined as structured terms wrapping a subse-
Layer terms denote to the abstract model of Section 3.1.     quence of commands.



                        JEmpty()K(pt) = Transparent
       JBlendLayer(ℓbot, ℓbot, 𝑝)K(pt) = blendp Jℓbot K(pt), filter𝑝 Jℓtop K(pt)
                                                                                 

                                                                      fill𝑝 (pt)
                                                                                         
                                                                                    𝑠 (pt)
           JDrawShape(ℓ, 𝑠, 𝑝)K(pt) = blend𝑝 JℓK(pt), filter𝑝
                                                                      Transparent else



                               Fig. 4. Denotational semantics for Layer terms.



Paint object, which defines a blend mode, fill type, and color filter. The Paint object configures the
various phases of the Skia drawing pipeline. Because Layer has only these two constructors (plus
the special Empty layer), it is particularly easy to induct on them in proofs.
   The Layer constructors denote to the abstract model, as shown in Figure 4. Empty has a straight-
forward denotation to an all-Transparent image. BlendLayer is likewise straightforward, first
applying an image filter to the top layer and then blending it with the bottom layer, both pointwise
and with the filter and blend mode determined by the Paint object. DrawShape is the most complex.
Conceptually, it first computes which points are within the shape 𝑠; then computes the fill color for
each one; and finally blends the layer’s current color and computed color for each point. The blend
is performed even for points outside 𝑠; this is critical for, for example, DstIn blending.
   Layers are equivalent up to denotation, and permit substitution. That is, if JℓK = Jℓ ′ K, then
J𝑚K = J𝑚[ℓ/ℓ ′ ]K. This fact means that equivalences over Layer terms can be used as rewrite rules,
which we leverage in Section 4 to prove Skia optimizations correct.

3.3   𝜇Skia
𝜇Skia is a simplified version of the Skia API itself. A 𝜇Skia program consists of a sequence of
commands (see Figure 3). These commands include all the features described in Section 2, including
the Draw command for drawing, the Clip command for manipulating the clip state, and the Save,
SaveLayer, and Restore stack manipulation commands. 𝜇Skia diverges from the Skia API in two
main ways. First, the syntax definition is more regular to eliminate unimportant special cases:
Save, SaveLayer, and Restore must be properly bracketed, while the Draw and Clip commands
take arbitrary Shapes, Second, only a small fraction of the API is modeled. Our Lean formalization
extends the grammar in Figure 3 with several additional features, including opacity, styles, and
transforms, and we expect adding even more features to be straightforward.

                                                         8
   𝜇Skia programs manipulate a state Σ:
                                           Σ : List[Layer] × List[Shape]
The first list in Σ is the stack of layers manipulated by SaveLayer, while the second list is the stack
of canvas states manipulated by Save. In the minimal 𝜇Skia language of Figure 3, the the canvas
state is a single Shape because the only canvas state operation is Clip; our Lean formalization adds
additional fields. The initial state is ⟨[Empty()], [U]⟩, an Empty layer and the full clip state, each
as single-element stacks; we treat the head of the list as the top of the stack.
   A 𝜇Skia program then performs a sequence of steps 𝑐, Σ ↦−→ Σ′ . The simplest is the Draw
command, which modifies the top Layer:

                  Draw(𝑔, 𝑝), ⟨ℓ :: 𝐿, 𝑚 :: 𝐶⟩ ↦−→ ⟨DrawShape(ℓ, 𝑔 ∩ 𝑚, 𝑝) :: 𝐿, 𝑚 :: 𝐶⟩
Note that the DrawShape operation is passed the intersection of the shape 𝑔 being drawn and the
current clip mask 𝑚.
  The Clip command modifies the canvas state, intersecting it with the new clip geometry:

                                  Clip(𝑚 ′ ), ⟨𝐿, 𝑚 :: 𝐶⟩ ↦−→ ⟨𝐿, (𝑚 ∩ 𝑚 ′ ) :: 𝐶⟩
Note that the actual Skia clipRect command has an optional SkClipOp parameter that allows
instead taking the difference instead of intersecting the new mask with the clip state; this paper
does not show that (straightforward) extension but our Lean formalization does include it.
   The Save command duplicates the top canvas state, runs the bracketed commands, and then
discards the new canvas state when its matching Restore is reached:
                                     𝑐, ⟨𝐿, 𝑚 :: 𝑚 :: 𝐶⟩ ↦−→ ⟨𝐿 ′, 𝑚 ′ :: 𝑚 :: 𝐶⟩
                              (Save(); 𝑐; Restore()), ⟨𝐿, 𝑚 :: 𝐶⟩ ↦−→ ⟨𝐿 ′, 𝑚 :: 𝐶⟩
Note that Restore does not make any changes to the layer state.
  The SaveLayer command, meanwhile, allocates a new, Empty layer to push onto the layer stack
and, when the Restore command is reached, blends that new layer with the one below:
                       𝑐, ⟨Empty() :: ℓ :: 𝐿, 𝑚 :: 𝑚 :: 𝐶⟩ ↦−→ ⟨ℓ ′ :: ℓ :: 𝐿, 𝑚 ′ :: 𝑚 :: 𝐶⟩
          (SaveLayer(𝑝); 𝑐; Restore()), ⟨ℓ :: 𝐿, 𝑚 :: 𝐶⟩ ↦−→ ⟨BlendLayer(ℓ, ℓ ′, 𝑝) :: 𝐿, 𝑚 :: 𝐶⟩
The inference rule for sequential composition is straightforward and, along with various extensions
to 𝜇Skia, is given in our Lean formalization.
   The 𝜇Skia semantics is deterministic, and programs never get stuck.6 The final state consists of a
single layer, whose denotation is the program’s output.

3.4    Lean Formalization
We have mechanized all three strata of this formalization—the abstract model, Layer terms, and
𝜇Skia commands, and their respective denotational / operational semantics, in the Lean 4 interactive
theorem prover [20]. Our mechanization, which we intend to submit as an artifact, is 453 lines
of code in total. We also provide an instantiation of the abstract model, representing Point as a
2-tuple of reals and Color as a 4-tuple of real numbers representing premultiplied ARGB colors.
This means that the alpha channel 𝛼 is bounded between 0 and 1, while the three color channels
are bounded between 0 and 𝛼. By formalizing Point with reals, equivalences in this abstract model
are only up to anti-aliasing. By formalizing Color with reals, equivalences in this abstract model
6 Proving this requires proving that Skia programs only ever modify the top of the layer and canvas stack, and do not change

the stack size. This is proven by induction.


                                                             9
are also only up to rounding. We have discussed these choices with the Skia engineering team,
who confirmed that anti-aliasing and rounding behavior, while important, are acceptable to change
during optimization.
   Our formalization also includes a number of extensions not discussed in this section. We for-
malize “style”, like fill versus stroke, as a unary function on Shapes, and handle opacity accurately
during blending, which requires care with certain blend modes. We also extend the canvas state
with an affine transform, manipulated by translate, rotate, scale, and perspective operations, and
add SkClipOp-style clip operations. All these extensions involve new 𝜇Skia commands, or new
parameters to existing 𝜇Skia commands, but do not affect the Layer terms. This makes it easy to
write proofs that remain valid as the semantics are extended. More speculatively, we also expect that
Layer terms will be useful for formalizing rasterization libraries besides Skia, since most existing
rasterization libraries share a similar drawing pipeline due to a shared heritage from PostScript.
   There are still some parts of Skia’s API that our Lean mechanization does not cover, like mask
filters, blurs, and image filters, as well as even more obscure portions of the API like the SkSL
shading language or support for bitmap images. These have little effect on the rewrite rules of
Section 4, but we do expect that they could be added to 𝜇Skia if a need arose.

4     Rewrites in 𝜇Skia
𝜇Skia enables rigorous, verified reasoning about the equivalence of Skia programs. As a case study,
we collected Chrome-generated Skia programs from the top 100 websites, including pages like
the Amazon, Github, New York Times, and Tiktok home pages.7 A manual examination showed
that many included suboptimal patterns that used more SaveLayers than necessary, which means
rasterization allocated unnecessary GPU memory and performed unnecessary blends. We identified
four common patterns of suboptimal Skia instructions; some patterns were common across many
pages, while others were specific to particular, widely-used, web frameworks. For each one, we
wrote a more optimized pattern and verified each replacement using the 𝜇Skia semantics, including
identifying the necessary side conditions and proving the necessary equivalences for our real
abstract model.
  Formally, two 𝜇Skia programs are equal when they evaluate to the same Image in the 𝜇Skia
semantics. Because 𝜇Skia programs are imperative, however, equivalence does not generally allow
substitution. However, because 𝜇Skia commands only modify the top of the state or layer stack,
substitution directly inside SaveLayer is valid.8 The common patterns we identify are therefore
whole-program or whole-layer patterns.

4.1    SrcOver SaveLayers
SrcOver is by far the most common blend mode, corresponding to the normal intuitive meaning of
“drawing over” some other image, and SaveLayers with SrcOver blend mode are often unnecessary,
suggesting the following idealized equivalence:
                            ℓ1 . . .                        ℓ1 . . .
                            SaveLayer(𝑝 { SrcOver, Id });   Save();
                               ℓ2 . . .                   =    ℓ2 . . .
                            Restore();                      Restore();
                            ℓ3 . . .                        ℓ3 . . .
Here, the syntax ℓ . . . means any sequence of Skia commands, while the syntax 𝑝{SrcOver, Id}
means any Paint object 𝑝 with a SrcOver blend mode and Id color filter.
7 And many international pages like Bilibili, Mail.ru, and Yahoo.jp.
8We mechanize this theorem in Lean.



                                                             10
   We prove that this equivalence holds under the condition that all drawing commands in ℓ2 use
SrcOver blend mode and further that ℓ2 contains no SaveLayer commands.9 This restriction is
necessary to ensure that DstIn or other blends performed in ℓ2 are properly isolated from ℓ1 . In
the replacement pattern on the right hand side, the SaveLayer commands are replaced with Save.
This ensures that changes to canvas state in ℓ2 are properly isolated from ℓ3 , while still avoiding
the extra layer allocation and blend performed by SaveLayer.
   This equivalence is proven by induction over ℓ2 . It is convenient to assume that sequential
composition is left-associated; induction then proceeds by “peeling off” the last drawing command
in ℓ2 and case-splitting on it. After expanding out the 𝜇Skia semantics, the inductive step requires
proving the following equivalence of Layer terms:
   BlendLayer(ℓ1, DrawShape(ℓ2, 𝑔, 𝑝𝑑 {SrcOver}), 𝑝) = DrawShape(BlendLayer(ℓ1, ℓ2, 𝑝), 𝑔, 𝑝𝑑 )
Note that, per the restriction of ℓ2 , the Draw command uses a SrcOver blend. Applying this rewrite
once “peels” a single Draw command out of the inner SaveLayer, and applying it repeatedly results,
inductively, in the intended equivalence.
  The Layer equivalence, in turn, boils down to the following equivalence in our abstract model:
                            SrcOver(𝑎, SrcOver(𝑏, 𝑐)) = SrcOver(SrcOver(𝑎, 𝑏), 𝑐)
We prove this equivalence directly for our real-valued instantiation of the abstract model using the
standard definition of SrcOver blending.

4.2    Dstin to Clip
In a number of cases, Chrome uses DstIn for general-purpose masking, even though using a Clip
command would be equivalent and more efficient. This suggests the following idealized equivalence:
                             ℓ1 . . .
                             SaveLayer(𝑝 1 { DstIn });                    Clip(𝑔);
                                 ℓ2 . . .                               = ℓ2 . . .
                                 Draw(𝑔, 𝑝 2 { Solid(𝑐 2 ), SrcOver });   ℓ1 . . .
                             Restore()
    We prove that this equivalence holds under the condition that ℓ1 does not contain any SaveLayer
operations, that ℓ2 contains only Clip operations,10 and that the color 𝑐 2 is opaque after applying
𝑝 2 ’s and then 𝑝 1 ’s color filters.
    The challenge with verifying this rewrite is that Clip operations in ℓ2 do not apply to the
operations in ℓ1 on the left hand side, but do apply to operations in ℓ1 on the right hand side. The
equivalence holds because the ℓ2 Clips intersect with 𝑔, which then acts as a mask for the entire
image drawn by ℓ1 . The proof therefore proceeds by induction over ℓ1 , and we define a helper
function clipAll on Layer terms to aid the proof:
                           clipAll : Layer → Shape → Layer
                           clipAll(Empty(), 𝑚) = Empty()
                           clipAll(Draw(ℓ, 𝑔, 𝑝), 𝑚) = Draw(clipAll(ℓ, 𝑚), 𝑔 ∩ 𝑚, 𝑝)
Note that clipAll is not defined on BlendLayers, which is fine because we assume that ℓ1 does
not contain SaveLayers; in Lean, clipAll returns a dummy layer in that case. We then prove, by
induction, that commuting Clip over ℓ results in clipAll(ℓ).
9 Our Lean formalization also includes opacity, so additionally restricts the paint 𝑝 to be opaque.
10 Our Lean formalization also includes SkClipOp-style clip operations so further restricts ℓ Clip operations to only use the
                                                                                             2
intersection operator.


                                                             11
<svg width="80" height="30" viewBox="0 0 80 30">
  <defs>
    <radialGradient id="b" ...>...</radialGradient>
    ...
    <pattern id="x" ...>
       <rect width="100" height="100" fill="#7D2AE7"/>
       ...
    </pattern>
  </defs>
  <mask id="a" ...>
    <path fill="#fff" d="M79.444 18.096 ... 69.192 21.888z"/>
  </mask>
  <rect mask="url(#a)" width="100" height="100" fill="url(#x)"/>
</svg>

               Fig. 5. SVG snippet used in this subsection, shown alongside its rasterized result.


   With this induction proven, the core Layer equivalence becomes:
                         BlendLayer(ℓ1, Draw(Empty(), 𝑚, 𝑝 2 ), 𝑝 1 ) = clipAll(ℓ1, 𝑚)
This is then proven by induction over ℓ1 , using as a lemma that states as a fact that, since ℓ1 contains
no SaveLayer commands, its denotation will contain no BlendLayers. The base case, where ℓ1 is
Empty, is trivial, while the inductive case reduces to the following in the abstract model:
                                                                               
                             𝑐 1,             𝑥 ∈𝑔         𝑐 2,          𝑥 ∈𝑚
                    DstIn                              ,
                             Transparent, else             Transparent, else
                                                                  
                                       𝑐 1,              𝑥 ∈ 𝑔 ∩𝑚
                                  =
                                       Transparent, else
where 𝑐 2 is known to be opaque. This is proven by case analysis on 𝑥 ∈ 𝑔 and 𝑥 ∈ 𝑚.

4.3    Subsuming Filters
Figure 5 shows a snippet of SVG code; this snippet specifically is from the Canva website. SVG is a
declarative, XML-based language for vector graphics implemented by Google Chrome.11 In this
snippet, <rect> declares a rectangle, but that rectangle uses a custom fill (a <radialGradient>
defined in a <defs>) and a custom mask (defined by a <mask>). When drawn, the rectangle thus
actually looks like the Canva logo. Unfortunately, the Skia program Chrome generates for this code
is not straightforward.
   Chrome performs the fill-and-mask operation by drawing the mask on a SaveLayer and blend-
ing it on the fill using DstIn blending. However, while DstIn blending is based on mask layer
transparency, SVG masking (by default) is based on luminance, requiring an extra conversion step.
Chrome performs this conversion using a separate SaveLayer with a luminance color filter. This is
suboptimal:
   ℓ ...
   SaveLayer(𝑝 { DstIn });                         ℓ ...
      SaveLayer(𝑝 1 { Luma, SrcOver });            SaveLayer(𝑝);
                                                 =
         Draw(𝑚, 𝑝 2 { Solid(𝑐), SrcOver, Id });      Draw(𝑚, 𝑝 3 { Solid(Luma(𝑐)), SrcOver, Id });
      Restore()                                    Restore()
   Restore()
11 It is delightfully recursive that Canva is itself an online vector graphics tool, which was probably used to make this SVG

logo; SVG is itself a vector graphics language, which Chrome executes with Skia; and then Skia itself offers vector graphics
operations.


                                                             12
    We prove this equivalence unconditionally. The replacement pattern on the right removes the
luminance conversion SaveLayer and simply pre-computes the luminance of the mask fill color.
The remaining SaveLayer in the replacement pattern can be removed using the DstIn-Clip rewrite
of Section 4.2. However, this equivalence does not generalize to cases where the inner SaveLayer
contains multiple Draw commands due to the way multiple colors can interact with the Luma color
filter.
    Proving this rewrite in the 𝜇Skia semantics does not require induction. Instead, the proof abstracts
over the state Σ produced by ℓ and then evaluates the fixed sequence of three Skia commands in
the pattern. This reduces to the following equation in the abstract model:
                   Luma(SrcOver(Transparent, 𝑐)) = SrcOver(Transparent, Luma(𝑐))
The equation is trivially true because SrcOver(Transparent, 𝑐) = 𝑐. An analogous rewrite with two
or more Draw commands, by contrast, would require this more general equation and incorrect
equation:
                         Luma(SrcOver(𝑐 1, 𝑐 2 )) ≠ SrcOver(Luma(𝑐 1 ), Luma(𝑐 2 ))

4.4    Gradient Masks
Three Russian websites—mail.ru, dzen.ru, and yandex.ru12 —use a common web framework
which, for some reason, uses opaque gradients as masks. The gradients do not actually mask out
any content, because they are opaque, but they are expensive for Skia to raster. This suggests the
following idealized equivalence:
                       Draw(𝑠, 𝑝 1 { SrcOver });
                       SaveLayer({ DstIn });
                                                                    = Draw(𝑠, 𝑝 1 );
                         Draw(𝑠, 𝑝 2 { Gradient(𝑔), SrcOver, Id });
                       Restore();
Here the left hand side is a complete, four-instruction Skia program; this rewrite is performed
under SaveLayer on the target web pages.
   We prove this equivalence under the condition that every color stop in 𝑔 is opaque. In this case,
the DstIn blend does not affect the initial Draw and the mask is entirely superfluous. Again, no
induction is needed, since only a fixed number of 𝜇Skia commands are present. Converting to Layer
terms, the rewrite unfolds to:
                   BlendLayer(Draw(Empty(), 𝑠, 𝑝 1 ),
                        Draw(Empty(), 𝑠, 𝑝 2 ),         = Draw(Empty(), 𝑠, 𝑝 1 )
                        { DstIn })
This reduces to the following equation in the abstract model:
                      DstIn(SrcOver(Transparent, 𝑎), 𝑏) = SrcOver(Transparent, 𝑎)
where 𝑏 is known to be opaque because all color stops in the gradient 𝑔 were opaque.
   All four suboptimal patterns in this section require careful reasoning about colors, blends, and
filters in order to guarantee that the optimization is correct. While each high-level rewrite is
straightforward, we needed many attempts to write down valid replacement patterns and discover
critical assumptions like the lack of SaveLayer operations in certain command sequences or the
opacity of the colors involved. The 𝜇Skia semantics, and the rigorous proofs it enables, were
essential to surfacing assumptions and ensuring that each rewrite was correct.

12Which together received just over 5 billion visits/month in January 2026!



                                                           13
5     Compiler
To demonstrate the utility of the 𝜇Skia semantics for developing impactful Skia tooling, this section
discusses a Skia optimizer that applies rewrites discussed in Section 4. The optimizer is highly
efficient, processing thousands of Skia commands in microseconds, allowing Skia clients to meet
demanding refresh rate targets.

5.1    Rewriting


 template <typename MatchState>
 struct SkOptPass {                                        SaveLayer (p {¬SrcOver})                               SaveLayer (p {SrcOver})
                                                                                      Draw (s, p {¬SrcOver})
     struct Frame {
         MatchState match_state;
         int save_count;                                                        Ignore                    Matching               Draw (s, p {SrcOver})

     };
     STArray<8, Frame> frames;
     int save_count;                                                                                           Restore()


       void transform(SkRecord*);
                                                                                            Rewrite

       MatchState onSaveLayer(SkRecord*, int);
       void onSave(SkRecord*, int);
       void onRestoreLayer(SkRecord*, int);
       void onRestore(SkRecord*, int);
       void onDraw(SkRecord*, int);
       void onClip(SkRecord*, int);
       void onOther(SkRecord*, int);
 };

Fig. 6. Here we show both the definition of the abstract SkOptPass rewrite pass, and the corresponding
state machine implementing the SrcOver-SaveLayer rewrite. The state machine state is managed by the
MatchState struct. It tracks the state, and any metadata needed to complete the rewrite. In this case the
only extra metadata needed is the location of the SaveLayer to be removed. The state machine we show is the
state machine for only one layer for simplicity. The rewriter actually functions like a stack of state machines,
with each SaveLayer pushing the start of a new state machine onto a stack, and a Restore popping it off.
Some times the actions of the top most state machine can change the state of the ones below. We implement
this by allowing the rewriter to look beyond the top of the stack.

   When a Skia client calls a method on the SkCanvas object, Skia records this command as an
SkRecords object in an in-memory buffer called an SkRecord.13 The optimizer then searches the
SkRecord buffer for each rewrite rule from Section 4, replacing the matched commands with the
right-hand side of the rewrite rule. Each rewrite is implemented as a single optimization pass that
performs a single pass over the command buffer. A single pass can perform multiple matches.
   Each optimization pass implements the SkOptPass interface shown in Figure 6. Implementation
passes subclass from SkOptPass and implement the on* callback methods to handle different Skia
command types. The transform method is the main entry point, performing a single optimization
pass over an SkRecord command buffer by calling the relevant callback method for every Skia
command in the buffer. The onOther callback is called for all commands outside the 𝜇Skia semantics;
generally the onOther callback invalidates the current match. However, SkOptPass also handles a
13 Yes, the class name for the collection is singular while the class name for its elements is plural.



                                                               14
             fRecords:      ∗      ∗     ∗       ···


               fAlloc:     SkRecords::DrawRect         SkRecords::ClipRect   SkRecords::DrawRect    ···


Fig. 7. SkRecord stores an array of pointers (fRecords) into a contiguous chunk of record objects (fAlloc),
each of which represents a single Skia command.


key gap between the actual Skia language and the 𝜇Skia semantics of Section 3: matching Save and
SaveLayer to their corresponding Restore calls and thereby calling onRestore or onRestoreLayer.
   To do so, the SkOptPass class stores a save_count and a stack of Frame objects. Every Save
command increments the save_count field, while every SaveLayer command pushes a new Frame,
which in turn also saves the current save_count. When a Restore command is seen, the save_count
field is compared to the save_count of the top Frame to determine if a Save or SaveLayer is being
closed and to call the appropriate callback. Additionally, the 𝜇Skia language permits rewrites under
SaveLayer commands, so in principle a rewrite can apply to any SaveLayer/Restore pair. For this
reason, the Frame stack also stores a MatchState for each currently-open SaveLayer; the initial
MatchState for the layer is returned from onSaveLayer. The stack of frames is stored in a Skia
STArray, a container that stores its first eight entries on the stack. The stack depth corresponds
to the SaveLayer depth, and most Chrome-generated Skia programs we have seen have shallow
SaveLayer depths, so the frame stack is typically entirely stack-allocated.
   The MatchState type is instantiated by every individual optimization pass and implements a
finite state automaton that matches the rewrite rule. For example, the SrcOver-SaveLayer rewrite
uses two states, Matching and Ignore, shown in Figure 6. The initial MatchState is Matching
for SrcOver-SaveLayer commands14 and Ignore otherwise. The MatchState also stores the index
in the SkRecord of the SaveLayer command, for later rewriting. SrcOver-Draw commands stay
in the Matching state, while all other Draw commands and all SaveLayer commands transition
to the Ignore state. All other commands (Clip, Save, Restore) do not affect the match state. The
MatchState therefore indicates whether a given layer is a SrcOver-SaveLayer containing only
SrcOver-Draw commands—exactly the requirements of the SrcOver-SaveLayer rewrite in Sec-
tion 4. The other rewrites in Section 4 have similar, though more elaborate, state machines. In
onRestoreLayer, if the current state is matching, the actual rewriting is performed by changing
the SaveLayer command into a Save command using the saved index.

5.2   Memory Management
While the single-pass design does limit the computational complexity of our optimizer, effi-
ciently manipulating Skia programs in memory is also critical to hitting demanding latency
limits. Each SkRecords object has a tag and fields for all the arguments to that specific com-
mand. SkRecords::DrawRect, for example, has a DrawRect_Type tag, an SkRect for the rectangle
bounds, and an SkPaint for the paint parameters. The SkRecord buffer stores two fields: fRecords,
an array of pointers to SkRecords objects, and fAlloc, an arena allocator where the SkRecords
objects are stored. Figure 7 illustrates the memory layout. Importantly, this design means that the
compiler can mutate the SkRecord buffer without moving the actual SkRecords objects, simply by
adjusting the pointers in fRecords.

14 The optimizer also requires the SaveLayer command to be opaque; while Section 3 does not include opacity, our Lean

formalization does.


                                                            15
   Applying the rewrites from Section 4 requires changing, removing, or adding commands to the
SkRecord. Changing commands is easy: the optimizer allocates a new SkRecords object in the
arena and changes the fRecords buffer to point to this new object. Removal likewise changes a
command into a special SkRecords::NoOp command. When inserting new commands, however,
it would be expensive to move the fRecords elements, especially since multiple rewrites can
apply to the same SkRecord. We therefore store pending insertions into a separate insertion buffer,
and merge the original and insertion buffer in a single linear scan after the optimization pass is
complete. We learned of this technique from the WebKit browser engine’s B3 JIT, where it is called
an “InsertionSet” [27], though the general technique is well-known.
   Skia can serialize SkRecord objects to and from a binary format called a “Skia Picture” or skp.
All information in a SkRecord format required for drawing, including referenced external images,
are serialized into the skp.15 Google Chrome can dump generated Skia programs as skps with
the chrome.gpuBenchmarking.printToSkPicture debug method, available when Chrome is run
with –no-sandbox and –enable-gpu-benchmarking flags. It is important to note here that Chrome
generates multiple Skia programs, meaning multiple skps, for a single website. These multiple
programs represent different “layers” of the page, which are then composited in a later step;
this split into layers chosen by Chrome to optimize animations [25] and is unrelated to Skia’s
concept of layers. Our optimizer operates on individual SkRecord objects in memory for maximum
performance, but our evaluation does save and load these SkRecord objects from/to skp files to
minimize interference from Google Chrome during benchmarking, as discussed in more detail in
Section 6.

6     Evaluation
We evaluate the 𝜇Skia semantics, and the optimizer based on them, on a collection of real-world
Skia programs generated by Google Chrome on the Top 100 websites, focusing on four research
questions:
RQ1 Is the optimizer correct?
RQ2 Is the optimizer effective?
RQ3 Is the optimizer fast?
RQ4 Are the optimizations generic across Skia backends, hardware, and websites?

6.1    Methodology
We evaluate our optimizer on Skia programs generated by Google Chrome on the top 100 most-
visited websites in the world,16 using the list on Wikipedia [2], which in turn is based on data from
Similarweb and Semrush.17 Google Chrome, via the playwright Python library, is used to visit
the main page of each website, and skp files are dumped as described in Section 5. Each website
produces one or more skp files. Since our optimizer focuses on reducing the number of SaveLayer
commands, we focus on skp files that have SaveLayer commands. For our primary evaluation in
RQs 1–3, this leaves 99 benchmarks across 100 websites.
   The optimizer itself is based off of Skia commit f931a2e, on the main branch between milestones
143 and 144 [10]. For our primary evaluation in RQs 1–3, we build Skia with Clang version 17.0.0
with -O3 and -flto=thin and run it on an 8-core Apple M2 unified CPU/GPU with 16GB RAM
with Skia’s “Graphite” graphics backend and the Metal GPU API.

15 Though typefaces do not get serialized into the skp.
16 Excluding a few pornographic websites.
17 The famous “Alexa Top 100” is no longer produced.



                                                          16
                      theorem src_eq_opt1 : denote src = denote opt1 := by
                        unfold src
                        unfold opt1
                        grind (gen := 80) [GradientMask]

Fig. 8. Example of a translation validation lemma. src is the source 𝜇Skia term, and opt1 is the term after
one optimization pass. The relevant rewrite theorem, GradientMask, is passed to grind to search for a proof;
a number of general-purpose 𝜇Skia theorems are also included by @[grind] annotations. The gen argument
to grind increases its search fuel to enable proofs for larger 𝜇Skia terms.


6.2   RQ1: Is the Optimizer Correct?
This section aims to answer RQ1 by showing that the optimizer is correct, in two senses: that it
conforms with the 𝜇Skia semantics and that it also does not introduce visible distortions on the
evaluation websites.
6.2.1 Conformance with 𝜇Skia Semantics. To test whether the optimizer conforms with the 𝜇Skia
semantics, we extended it with a mode that outputs an skp after each individual rewrite pass,
forming an “optimization trace”. Each of these skp files is then converted into a readable JSON
format using skp_parser, a tool distributed with Skia, and then read and converted to 𝜇Skia
Lean terms using a short Python program. Not every skp can be converted, since 𝜇Skia does not
formalize some advanced Skia features like mask and image filters, but for 42 benchmarks all
steps in the optimization trace convert cleanly. The conversion program also performs some minor
simplifications, such as down-casting SkPath shapes to simpler shapes like SkRect when possible,
to invert a transformation done by Skia. If all skp files in the optimization trace can be converted
to a 𝜇Skia Lean term, a sequence of lemmas is asserted in Lean, claiming that each step in the trace
is equivalent, as a 𝜇Skia program, to the previous step.
   To prove this theorem, we rely on Lean’s grind tactic. The grind database is loaded with
theorems for the rewrite rules applied by the optimizer in this step as well as general theorems
about 𝜇Skia equivalence. Figure 8 shows an example proof. Translation validation succeeds for
34 benchmarks of 99 benchmarks, demonstrating that our optimizer conforms with the 𝜇Skia
semantics and providing a “foundational” certification of its correctness on these benchmarks.
Some of the successful translation validations are quite complex; for example, the main skp from
Pinterest contains a luminance filter nested in a DstIn mask nested in an opaque SaveLayer. Three
separate optimization passes fire on this benchmark, with each one exposing the next rewrite
opportunity; all three translation validate. The remaining 8 benchmarks do not translation validate
due to grind timeouts; as a general-purpose proof search engine, grind is slower than our optimizer
and times out on complex 𝜇Skia terms.
 6.2.2 Optimizations yield the same images. Conformance with the 𝜇Skia semantics, however, is
 only as good as the quality of the 𝜇Skia semantics themselves. We therefore compare the baseline
 and optimized skp by rasterizing both skp to PNG images and performing a pixel diff using
 ImageMagick compare. The 𝜇Skia rewrites of Section 4 are proven in a real-valued abstract model,
 so ignore effects from discretization and anti-aliasing, which are caused by the discrete pixel grid
 and finite color depth, so some differing pixels are expected; we therefore pass -metric AE and
-fuzz 1% to compare, asking it to report the number of pixels that differ by more than 1% in a
 color channel. Notably, we perform the pixel comparison to all benchmarks, and can thus test the
 optimizer’s correctness even for benchmarks that use features not formalized in 𝜇Skia.
    Across the 99 benchmarks, only 19 report significant pixel differences. We examine all such
 instances manually; Figure 9 shows one example, from TikTok. In all such instances, the differing

                                                     17
Fig. 9. On the left, a button drawn by the skp captured for Layer 5 on the TikTok website. In the middle, the
same button drawn by the optimized skp. On the right, the same button is drawn, lighter, with differing pixels
are drawn in red. The differing pixels are clearly placed along a curved shape edge, exactly where anti-aliasing
effects are expected.




                                                            Fig. 10. Raster-time speed-up CDF. The horizon-
                                                            tal axis shows a speedup value, with the red line
                                                            marking a 1× speedup meaning identical runtime
                                                            for the baseline and optimized skp. The vertical
                                                            axis shows the fraction of benchmarks that meet
                                                            or exceed that speed-up amount. We find a geo-
                                                            mean speedup of 18.7% across the benchmarks.
                                                            35 benchmarks are actually affected by the opti-
                                                            mizer, and these all see speed-ups, ranging from
                                                            1.035× to 3.584×.




pixels are clearly caused by anti-aliasing, as evident by the “spotted” nature of differences and
their location along curved shape edges. The authors could not tell the baseline and optimized
rasterizations apart by sight. Skia does not guarantee its anti-aliasing behavior, which can further
differ by monitor type or operating system, and we confirmed with a member of the Skia team that
anti-aliasing changes are acceptable.

6.3   RQ2: Is the Optimizer Effective?
This section aims to answer RQ2 by showing that the optimizer is effective at reducing the rasteri-
zation time of Skia programs.
   To measure raster time, we use nanobench, Skia’s standard, internal benchmarking tool. We
specifically use the playback benchmarking option, which rasters the same exact skp in a loop,
calibrating the number of loops so that the total GPU rasterization time is 5 milliseconds. This makes
timing overhead negligible. nanobench also performs warm-up iterations to avoid measuring shader
compilation time. To verify that the timing is reliable, we perform the nanobench measurement
100 times for each benchmark and consider the geometric mean.
   Figure 10 show our results. In this CDF, benchmarks are arranged vertically, and the dotted red
line corresponds to “no speedup”. Points to the right of the line get faster when optimized, with a
maximum speedup of 3.584×. The average geo-mean speedup across all 99 benchmarks is 18.7%.
The very largest speedups are seen on skps from a group of Russian websites that use the same
web framework; this framework, as discussed in Section 4, uses redundant gradient masks that
seem very expensive in Skia. Slowdowns are seen on 32.323% of benchmarks; however, all of the
skps that see slowdowns are not optimized suggesting that the slowdowns are noise. All of the

                                                       18
Fig. 11. Optimization time versus skp size on             Fig. 12. CDF with optimization time included.
Graphite/Metal. Runtime scales approximately lin-
early, and the all benchmarks optimizes in under 32 µs


significant speedups, by contrast, are on websites that are optimized, suggesting the speed-ups are
genuine. Specifically, out of 99 benchmarks, 67 see speedups, and of these, 35 are actually optimized
by the optimizer. The noise in measured speed-ups could be due to GPU load, scheduling, or other
concerns, or it could be due to the skp serialization and deserialization machinery; in any case,
the range of speed-ups for unoptimized benchmarks, 1.000× to 1.410×, is much smaller than the
range of speed-ups for optimized benchmarks, 1.035× to 3.584×, suggesting that the speed-ups are
genuine. In short, the optimizer is effective at significantly improving the rasterization time of
real-world Skia programs.

6.4   RQ3: Is the Optimizer Fast?
This section aims to answer RQ3 by showing that the optimizer is fast enough to “pay for itself” in
rasterization time reductions.
   Skia rasterization must be extremely fast: browser engines need rasterization to take hundreds
of microseconds for even large, complex websites to meet their frame budgets. We thus measure
the total optimization time using a similar measurement scheme as in RQ2. Figure 11 shows the
results. On the left, the scatter plot shows that the optimizer’s runtime is linear in the skp size, and
all skps optimize under 32 µs. The vast majority of skps are much smaller and thus much faster. On
the right, the CDF of Figure 10 is redrawn, but with the estimated optimization time added to the
estimated rasterization time. Slowdowns are now somewhat more common, since some skps see
no optimizations applied but still spend time in the optimizer. Still, the majority of skp continue to
show speed-ups, with the largest speed-ups still as large as 3.561×.

6.5   RQ4: Generalizability
This section attempts to answer RQ4 by showing that the optimizer is effective on a range of
back-ends, hardware, and websites. We focus on rasterization time, since optimization does not
invoke the back-end and thus cannot vary with the chosen back-end.
6.5.1 Backend generalizability. To test different Skia backends, we compare the speedups achieved
by the optimizer on the standard Graphite backend, which uses the Metal GPU API, and on the
legacy Ganesh backend, which uses the older OpenGL API. Figure 13 shows the results. The
optimizer is effective with both contexts, though the newer Graphite backend does see more

                                                     19
Fig. 13. Raster-time CDFs for the Graphite/Metal (left) and Ganesh/Apple (right) backends. The newer
Graphite backend achieves larger speed-ups and fewer slow-downs, but the optimizer is still effective on both.
Graphite/Metal sees a geo-mean speedup of 18.7% and Ganesh/Apple sees a geo-mean speedup of 13.2%.




Fig. 14. Raster-time CDFs for the Graphite/Vulkan (left) and Ganesh/Intel (right) backends on Machine #2.
The optimizer is still effective, with the exception of one benchmark, Canva, on the older Ganesh back-end,
which sees a dramatic but easily-avoided slow-down. Graphite/Vulkan sees a geo-mean speedup of 16.0%
and Ganesh/Intel sees a geo-mean speedup of 10.5%.


substantial speed-ups as well as fewer slow-downs. We suspect that the larger speed-ups result
from the generally-better performance of Graphite. The slowdowns with the Ganesh backend
are on benchmarks that are not optimized, so are indicative of greater noise, not lower optimizer
effectiveness. We were also able to reproduce Graphite’s claimed 15% speedup (we measured a
geo-mean of 18%) over Ganesh on fixed hardware. In fact, the speedup is almost the same as the
speedup of optimized over non-optimized programs, meaning that the older Ganesh backend with
optimized Skia programs is about as fast as the newer Graphite backend with Chrome-generated
Skia programs.
6.5.2 Hardware generalizability. To test the effect of different hardware, we repeated our evaluation
on a second machine, which runs Ubuntu 24.04.4 on an Intel i7-8700K CPU and an Intel CoffeeLake-
S GT2 GPU. This machine uses Clang version 18.1.3 and supports the Vulkan and OpenGL graphics

                                                     20
                                                                  Fig. 15. Raster-time CDF on Graphite/Metal with
                                                                  the new set of 100 websites.




APIs. Chrome’s generated Skia programs differ depending on the hardware used18 so the benchmark
set is re-captured on this machine, resulting in 83 benchmarks. The resulting skps are optimized
and measured with both the Graphite and Ganesh backends.
   Figure 14 shows the results. The optimizer is effective on the second machine too. The maximum
speed-up with the Graphite backend is somewhat smaller (2.285× instead of 3.584×) though in
this case the Russian websites are more clearly outliers. Slow-downs on Graphite continue to be
largely due to noise on benchmarks that aren’t optimized, while speed-ups are much larger than
any observed slow-downs.
   With the Ganesh backend, the same pattern persists (with an even lower maximum speed-up of
1.930×), except for one benchmark: Canva. The relevant part of the Canva benchmark is described
in more detail in Section 4; in short, it uses a number of SVG features that trigger a number of
separate optimization passes, resulting in a clipPath command with a complex clipping path.
We suspect that the complex clipping path somehow triggers bad behavior in the older Ganesh
backend. If support for Ganesh were important, the DstIn mask optimization pass could be disabled
for complex paths. In any case, this Canva benchmark is the only benchmark significantly slowed
down by the optimizer, suggesting that the optimizer generalizes well across different hardware
platforms.
6.5.3 Website generalizability. Finally, we ask whether the optimizer is effective on different
websites than the ones the authors examined. To test this, we froze the optimization passes and
their order and performed the same skp gathering process for the next 100 most-visited websites,
which yielded 180 new benchmarks. The authors have never examined the generated Skia programs
for these websites and have made no attempt to tune the optimizer to perform better on these
benchmarks.
   Figure 15 shows the results. Like in the old benchmarks set, we see significant speedups of up
to 2.543×, and, like before, websites actually rewritten by the optimizer show significantly larger
speed-ups than those that see slowdowns. All of the slowdowns are websites unaffected by the
optimizer, so the slowdowns are just noise. Considering the optimization passes individually, the
gradient mask optimization does not fire at all on the new set of benchmarks. This is expected,
18 Chrome will split the same web page into more or fewer layers depending on the available hardware. It will also use

different fonts. Plus, the evaluations were performed at different times and may capture different versions of the websites in
question.


                                                             21
because this optimization is targeted toward a specific web framework used on a number of popular
Russian websites; likely the new benchmark set does not have any websites using this framework.
The other optimization passes all see use on the new set of benchmarks.
  We expect that this new set of benchmarks has new, suboptimal patterns in its Chrome-generated
Skia programs, and that other Skia users have their own patterns of suboptimal Skia programs.
We expect the 𝜇Skia semantics and Lean formalization, plus the compiler architecture detailed in
Section 5, to prove useful in writing more optimal replacement patterns, proving them correct, and
enabling our optimizer to speed up rasterization for those clients as well.

7   Related Work
   2D graphics. Modern rasterization can be said to start with Warnock and Geschke’s Interpress
system at Xerox PARC [11]. Warnock and Geschke then founded Adobe [1], which introduced
PostScript [4], then PDF [3]. Color blending introduced by Porter and Duff [28]. Crow [6] introduced
a rudimentary rendering pipeline separating what is being drawn (objects and their spacial positions)
from how it is being drawn (rendering). The standard textbook on the topic is Computer Graphics:
Principles and Practice, especially the first edition [7]. A more recent thread of development in the
programming languages community is the Halide programming language [29]. In Halide, individual
graphical kernels, like those that implement drawing or blending operations, are described as a
combination of computation and schedule. Schedules can inline across operations, tile and vectorize
operations, and even split operations across multiple cores or accelerators without affecting the
computation itself. Further work [5, 21] introduced an auto-tuner to automatically generate high-
quality schedules. Work by Newcomb et al. [23], on automatically verifying optimizing rewrites in
the Halide compiler, is particularly relevant to this work. All that said, Halide and 𝜇Skia focus on
different aspects of rasterization: Halide focuses on the implementation of individual instructions,
while 𝜇Skia focuses on the semantics of the Skia command language itself.
   Web Browser Optimizations. Web browsers are prominent and demanding clients of rasterization
libraries, and have been a focus of recent research. Web browser JavaScript engines have seen
significant work, dating back to Gal et al. [8]’s initial JIT compiler for Firefox’s JavaScript engine.
Layout engines are also an area of active research, including Meyerovich and Bodik [19]’s parallel
layout algorithm, Liu et al. [17]’s synthesis algorithm for web browser layout algorithms, and
Kirisame et al. [14]’s algorithm for optimized layout invalidation. However, while web browsers are
important clients for rasterization libraries, rasterization is a later phase in the browser rendering
pipeline and does not directly interact with layout.
   Semantics for graphical domains. A number of papers have defined semantics for programming
languages in other graphical domains. Panchekha and Torlak [26] formalize a significant fraction of
the CSS specification, and later work from the same authors [24] uses that formalization to verify
geometric assertions about web page layouts, such as guaranteeing that two page components do not
overlap. Nandi et al. [22] introduces denotational semantics for the compilation of CAD programs
into 3D meshes, and He et al. [12] introduce a semantics for the lower level G-code instructions
used by 3D printing machines. The Marshall language [30] likewise defines a semantics for CAD,
with a focus on defining the semantics of continuous real operators. There is also a body of work
on semantics and decision procedures for knitting machines and knitting programs (Hurtig et al.
[13], Lin et al. [15, 16]). While there’s no direct relation with our work, these papers demonstrate
the significant interest in graphical computing in the programming languages community.

References
 [1] [n. d.]. About Adobe. https://www.adobe.com/about-adobe.html


                                                       22
 [2] 2026. List of most-visited websites. https://en.wikipedia.org/w/index.php?title=List_of_most-visited_websites&oldid=
     1342530547 Page Version ID: 1342530547.
 [3] 2026. PDF. Wikipedia (March 2026).
 [4] 2026. PostScript. Wikipedia (Feb. 2026).
 [5] Andrew Adams, Karima Ma, Luke Anderson, Riyadh Baghdadi, Tzu-Mao Li, Michaël Gharbi, Benoit Steiner, Steven
     Johnson, Kayvon Fatahalian, Frédo Durand, and Jonathan Ragan-Kelley. 2019. Learning to optimize halide with tree
     search and random programs. ACM Transactions on Graphics 38 (12 7 2019). Issue 4. doi:10.1145/3306346.3322967
 [6] F. C. Crow. 1982. A more flexible image generation environment. In SIGGRAPH ’82: Computer graphics and interactive
     techniques. doi:10.1145/800064.801253
 [7] J.D. Foley. 1996. Computer Graphics: Principles and Practice. Addison-Wesley.
 [8] Andreas Gal, Brendan Eich, Mike Shaver, David Anderson, David Mandelin, Mohammad R. Haghighat, Blake Kaplan,
     Graydon Hoare, Boris Zbarsky, Jason Orendorff, Jesse Ruderman, Edwin W. Smith, Rick Reitmaier, Michael Bebenita,
     Mason Chang, and Michael Franz. 2009. Trace-based just-in-time type specialization for dynamic languages. ACM
     SIGPLAN Notices 44 (28 5 2009). Issue 6. doi:10.1145/1543135.1542528
 [9] Google. [n. d.]. Introducing Skia Graphite: Chrome’s Rasterization Backend for the Future. https://blog.chromium.
     org/2025/07/introducing-skia-graphite-chromes.html
[10] Google. 2026. skia - Git at Google. https://skia.googlesource.com/skia/
[11] S. Harrington and R.R. Buckley. 1988. Interpress, the Source Book. Brady Book.
[12] Yumeng He, Chandrakana Nandi, and Sreepathi Pai. 2025. Formalizing Linear Motion G-Code for Invariant Checking
     and Differential Testing of Fabrication Tools. Proceedings of the ACM on Programming Languages 9 (9 10 2025). Issue
     OOPSLA2. doi:10.1145/3763106
[13] Nathan Hurtig, Jenny Han Lin, Thomas S. Price, Adriana Schulz, James McCann, and Gilbert Louis Bernstein. 2025.
     Polynomial-Time Program Equivalence for Machine Knitting. Proceedings of the ACM on Programming Languages 9 (5
     8 2025). Issue ICFP. doi:10.1145/3747517
[14] Marisa Kirisame, Tiezhi Wang, and Pavel Panchekha. 2025. Spineless Traversal for Layout Invalidation. Proceedings of
     the ACM on Programming Languages 9 (10 6 2025). Issue PLDI. doi:10.1145/3729322
[15] Jenny Lin, Vidya Narayanan, Yuka Ikarashi, Jonathan Ragan-Kelley, Gilbert Bernstein, and James Mccann. 2023.
     Semantics and Scheduling for Machine Knitting Compilers. ACM Transactions on Graphics 42 (26 7 2023). Issue 4.
     doi:10.1145/3592449
[16] Jenny Han Lin, Yuka Ikarashi, Gilbert Louis Bernstein, and James McCann. 2024. UFO Instruction Graphs Are Machine
     Knittable. ACM Transactions on Graphics 43 (19 11 2024). Issue 6. doi:10.1145/3687948
[17] Junrui Liu, Yanju Chen, Eric Atkinson, Yu Feng, and Rastislav Bodik. 2023. Conflict-Driven Synthesis for Layout
     Engines. Proceedings of the ACM on Programming Languages 7 (6 6 2023). Issue PLDI. doi:10.1145/3591246
[18] Mergr. 2026. Google Acquires Skia | Mergr. https://mergr.com/transaction/google-acquires-skia
[19] Leo A. Meyerovich and Rastislav Bodik. 2010. Fast and parallel webpage layout. In WWW ’10: The 19th International
     World Wide Web Conference. doi:10.1145/1772690.1772763
[20] Leonardo de Moura and Sebastian Ullrich. 2021. The Lean 4 Theorem Prover and Programming Language. Springer-
     Verlag, Berlin, Heidelberg. doi:10.1007/978-3-030-79876-5_37
[21] Ravi Teja Mullapudi, Andrew Adams, Dillon Sharlet, Jonathan Ragan-Kelley, and Kayvon Fatahalian. 2016. Au-
     tomatically scheduling halide image processing pipelines. ACM Transactions on Graphics 35 (11 7 2016). Issue 4.
     doi:10.1145/2897824.2925952
[22] Chandrakana Nandi, James R. Wilcox, Pavel Panchekha, Taylor Blau, Dan Grossman, and Zachary Tatlock. 2018. Func-
     tional programming for compiling and decompiling computer-aided design. Proceedings of the ACM on Programming
     Languages 2 (30 7 2018). Issue ICFP. doi:10.1145/3236794
[23] Julie L. Newcomb, Andrew Adams, Steven Johnson, Rastislav Bodik, and Shoaib Kamil. 2020. Verifying and improving
     Halide’s term rewriting system with program synthesis. Proceedings of the ACM on Programming Languages 4 (13 11
     2020). Issue OOPSLA. doi:10.1145/3428234
[24] Pavel Panchekha, Adam T. Geller, Michael D. Ernst, Zachary Tatlock, and Shoaib Kamil. 2018. Verifying that web
     pages have accessible layout. ACM SIGPLAN Notices 53 (11 6 2018). Issue 4. doi:10.1145/3296979.3192407
[25] Pavel Panchekha and Chris Harrelson. 2024. Web browser engineering. Oxford University Press.
[26] Pavel Panchekha and Emina Torlak. 2016. Automated reasoning for web page layout. In SPLASH ’16: Conference on
     Systems, Programming, Languages, and Applications: Software for Humanity. doi:10.1145/2983990.2984010
[27] Filip Pizlo. 2016. Introducing the B3 JIT Compiler. https://webkit.org/blog/5852/introducing-the-b3-jit-compiler/
[28] Thomas Porter and Tom Duff. 1984. Compositing digital images. ACM SIGGRAPH Computer Graphics 18 (1 1984).
     Issue 3. doi:10.1145/964965.808606
[29] Jonathan Ragan-Kelley, Connelly Barnes, Andrew Adams, Sylvain Paris, Frédo Durand, and Saman Amarasinghe. 2013.
     Halide. In PLDI ’13: ACM SIGPLAN Conference on Programming Language Design and Implementation. doi:10.1145/


                                                           23
     2491956.2462176
[30] Benjamin Sherman, Jesse Michel, and Michael Carbin. 2019. Sound and robust solid modeling via exact real arithmetic
     and continuity. Proc. ACM Program. Lang. 3, ICFP, Article 99 (July 2019), 29 pages. doi:10.1145/3341703




                                                           24
