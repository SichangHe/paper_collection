# Pseudorandom Error-Correcting Codes

Miranda Christ<sup>∗</sup>

Columbia University

Sam Gunn<sup>∗</sup>† UC Berkeley

#### Abstract

We construct pseudorandom error-correcting codes (or simply pseudorandom codes), which are errorcorrecting codes with the property that any polynomial number of codewords are pseudorandom to any computationally-bounded adversary. Efficient decoding of corrupted codewords is possible with the help of a decoding key.

We build pseudorandom codes that are robust to substitution and deletion errors, where pseudorandomness rests on standard cryptographic assumptions. Specifically, pseudorandomness is based on either 2 O( <sup>√</sup>n) -hardness of LPN, or polynomial hardness of LPN and the planted XOR problem at low density.

As our primary application of pseudorandom codes, we present an undetectable watermarking scheme for outputs of language models that is robust to cropping and a constant rate of random substitutions and deletions. The watermark is undetectable in the sense that any number of samples of watermarked text are computationally indistinguishable from text output by the original model. This is the first undetectable watermarking scheme that can tolerate a constant rate of errors.

Our second application is to steganography, where a secret message is hidden in innocent-looking content. We present a constant-rate stateless steganography scheme with robustness to a constant rate of substitutions. Ours is the first stateless steganography scheme with provable steganographic security and any robustness to errors.

<sup>∗</sup>Equal contribution. Email addresses: mchrist@cs.columbia.edu, gunn@berkeley.edu †Supported by a Google PhD Fellowship.

## Contents

| 1 | Introduction                                                         | 3  |
|---|----------------------------------------------------------------------|----|
|   | 1.1<br>An approach to watermarking                                   | 3  |
|   | 1.2<br>Our contributions                                             | 5  |
|   | 1.3<br>Related work: short summary                                   | 7  |
|   | 1.4<br>Organization<br>.                                             | 8  |
|   | 1.5<br>Differences from a previous version                           | 8  |
|   |                                                                      |    |
| 2 | Technical overview                                                   | 10 |
|   | 2.1<br>Pseudorandom code basics                                      | 10 |
|   | 2.2<br>Pseudorandom LDPC codes                                       | 11 |
|   | 2.3<br>Pseudorandom codes for the deletion channel<br>.              | 14 |
|   | 2.4<br>Constant-rate pseudorandom codes                              | 16 |
|   | 2.5<br>Watermarks for language models<br>.                           | 16 |
|   | 2.6<br>Watermarks with public attribution<br>.                       | 18 |
|   | 2.7<br>Robust steganography<br>.                                     | 19 |
| 3 | Preliminaries                                                        | 21 |
|   | 3.1<br>Cryptography preliminaries<br>.                               | 21 |
|   | 3.2<br>Coding theory preliminaries                                   | 22 |
|   |                                                                      |    |
| 4 | Pseudorandom code basics                                             | 23 |
|   | 4.1<br>Definitions                                                   | 23 |
|   | 4.2<br>Heuristic construction from permuted codes                    | 24 |
|   |                                                                      |    |
|   |                                                                      |    |
| 5 | Constructing pseudorandom codes from cryptographic assumptions       | 26 |
|   | 5.1<br>The zero-bit construction<br>.                                | 26 |
|   | 5.2<br>Codeword detection (zero-bit decoding)<br>.                   | 27 |
|   | 5.3<br>Pseudorandomness from the planted XOR assumption and LPN<br>. | 29 |
|   | 5.4<br>Pseudorandomness from subexponential LPN                      | 31 |
|   |                                                                      |    |
| 6 | Boosting the rate and robustness of any pseudorandom code            | 38 |
|   | 6.1<br>Multi-bit pseudorandom codes<br>.                             | 38 |
|   | 6.2<br>Constant-rate pseudorandom codes                              | 40 |
|   | 6.3<br>Pseudorandom codes for the deletion channel<br>.              | 41 |
| 7 | Application: watermarking for language models                        | 46 |
|   | 7.1<br>Watermarking preliminaries                                    | 46 |
|   | 7.2<br>Robust watermarking from PRCs                                 | 49 |
|   | 7.3<br>Language model steganography                                  | 55 |
|   | 7.4<br>Watermarks with public attribution<br>.                       | 55 |
|   |                                                                      |    |
| 8 | Application: universal steganography                                 | 59 |
|   | 8.1<br>Steganography preliminaries                                   | 59 |
|   | 8.2<br>Robust stateless steganography                                | 60 |
|   | 8.3<br>Stateless steganography from weaker modeling assumptions<br>. | 61 |

### <span id="page-2-0"></span>1 Introduction

The proliferation of AI-generated content is one of the biggest issues facing the internet today. Recent breakthroughs in large language models have made it increasingly difficult to distinguish this influx of AIgenerated content from human-generated content.

A promising solution for detecting AI-generated content is watermarking, where a hidden signal is embedded in the content. Several major companies, including OpenAI and Google, have pledged to embed watermarks in content output by their models [\[BH23\]](#page-62-0). Despite this explosion of interest in watermarking, there are very few techniques for building watermarking schemes that do not noticeably alter the generated content. Existing schemes incur trade-offs between the quality of generated content, the robustness of the watermark, and the computational complexity of detection.

In this work, we take a new cryptographic approach to this problem that allows us to avoid some of these trade-offs. Our approach is based on a new cryptographic primitive that we call a pseudorandom errorcorrecting code, or simply a pseudorandom code (PRC). A PRC is an error-correcting code that is parameterized by a decoding key. The pseudorandomness property states that, without this decoding key, any polynomial number of codewords are pseudorandom.

We find that the problem of building robust, quality-preserving watermarks reduces to the problem of building PRCs. Essentially, the watermarking strategy is to replace some of the randomness used by the generative algorithm with outputs from a PRC.

Building PRCs is challenging: Error-correcting codes are typically highly structured, while pseudorandomness implies a lack of discernible structure. Indeed, a priori it is not clear that such objects should exist. Nonetheless, we construct PRCs from standard (subexponential) cryptographic assumptions. Our constructions are related to low-density parity-check codes, and we base pseudorandomness on the Learning Parity with Noise assumption. We construct PRCs with strong robustness properties, including robustness to any constant rate of substitution and deletion errors.

Applying these PRCs to watermarking for language models, we obtain the first quality-preserving language model watermarking schemes that are robust to cropping and any constant rate of substitution and deletion errors. That is, the watermark detector will work as long as it is provided any sufficiently-long sequence of text, even if that text is subjected to any constant (less than 1/2) rate of random substitutions and any constant (less than 1) rate of random deletions.

### <span id="page-2-1"></span>1.1 An approach to watermarking

In this subsection we present a simple, general template for watermarking AI-generated content. The template described here can in principle be used to watermark arbitrary media, but we only present concrete instantiations in certain contexts (Sections [7](#page-45-0) and [8\)](#page-58-0).

In all generative AI settings there is a generative algorithm, Generate, that defines the behavior of the AI. A user provides a prompt, and Generate outputs some randomly-generated content. A watermarking scheme modifies Generate so that the generated content contains a hidden pattern, called a watermark. There are two essential requirements that any watermarking scheme should satisfy:

- Quality: embedding the watermark should not reduce the quality of generative algorithm; and
- Robustness: the watermark should be detectable in generated content, even if this content is corrupted.

Achieving both of these properties simultaneously is the central challenge of watermarking. Quality means that the watermark should not significantly alter the generated content, while robustness seems to require the watermark to change the content a great deal.

In this work, we propose a new strategy for watermarking: replacing the randomness used by Generate with codewords from a pseudorandom error-correcting code. A pseudorandom error-correcting code, or simply pseudorandom code (PRC), is a new cryptographic primitive that we introduce in this work. A PRC is defined by algorithms Encode, Decode satisfying two properties:

- Pseudorandomness: Any efficient adversary, without knowledge of the decoding key, cannot distinguish between oracle access to Encode and an oracle that always outputs a fresh random string; and
- Error correction or robustness: For any message m, if x ← Encode(m) and x ′ is a "corrupted" version of x where the amount of corruption is bounded, then Decode(x ′ ) = m.

For watermarking the message can be simply m = 1, indicating the presence of a watermark.[1](#page-3-0)

In order to make detection possible, we specify Generate in such a way that the detector can approximate the randomness used to produce any given content. To test for the presence of a watermark, the detector computes this approximation and then applies Decode to the result. If the content is watermarked and the approximation is close enough to the true randomness, then robustness of the PRC ensures that Decode returns 1. This indicates to the detector that the watermark is present. Stronger robustness of the PRC translates to stronger robustness of the watermark.

Pseudorandomness of the PRC guarantees that, without the decoding key, watermarked content is indistinguishable from content produced by the original generative algorithm — even if one is allowed to see many outputs. In particular, the quality of the generative algorithm is not deteriorated by the watermark. In [\[CGZ23\]](#page-62-1), such a watermark is referred to as undetectable.

Therefore, the problem of building robust, quality-preserving watermarks reduces to building PRCs (and appropriately specifying Generate). Below, we describe the application of this template to watermarking for language models.

Watermarks for language models. A generative language model is a randomized algorithm that takes as input a prompt, and samples text constituting a response. This text consists of tokens. For simplicity, we assume here that tokens are binary and that the full response is of a fixed length n. Neither of these assumptions is important for our results, as discussed in Section [7.](#page-45-0)

Given any generative language model, it is not difficult to define an algorithm Generate that takes a prompt and a random seed x ∈ {0, 1} <sup>n</sup>, and samples a response t ∈ {0, 1} <sup>n</sup> such that

- if x is uniformly random, then t is distributed identically to the original model, and
- each bit of t is correlated with the corresponding bit of x.

See Section [2.5](#page-15-1) for an example of such an algorithm. Now it is easy to recover an approximation of the randomness x that was used to produce a given text: just use the text t itself.

One natural watermarking strategy is to use the same random seed x ∈ {0, 1} <sup>n</sup> for every call to Generate, storing x itself as the watermarking key. This is essentially the strategy used by [\[KTHL23\]](#page-64-0), and it yields a highly robust watermark because the detector can compute the edit distance between the given text and x. The resulting quality guarantee is that a single response from the watermarked model is distributed identically to a single response from the original model.

However, this strategy results in redundancy of responses because the i th token of every response is biased towards the i th bit of x. This is problematic as it limits the variability of text that the language model generates. For instance, it should not be the case that certain words are preferred as the first word of every response. One can mitigate this issue by storing a family of seeds x1, . . . , x<sup>ℓ</sup> ∈ {0, 1} <sup>n</sup> and randomly choosing one such seed for each response. Increasing ℓ improves the variability, but comes at the cost of a corresponding increase in both watermark key length and detector runtime. Now, the detector must

<span id="page-3-0"></span><sup>1</sup>By instead encoding a longer message in the PRC, this technique extends to steganography — where messages are secretly communicated in innocent-looking content — as well.

compute the edit distance for each seed, resulting in a runtime of O(n 2 ℓ). In particular, for any polynomialtime watermarking scheme using this approach, there exists a polynomial-time adversary that can distinguish watermarked content from un-watermarked content without needing the watermark detection key.

A PRC is exactly the object needed to avoid this tradeoff between response variability and efficiency. Our watermark detection key will be the decoding key for a PRC, and we will embed the watermark by sampling a fresh pseudorandom seed x ← Encode(1) for each query to Generate. This results in no observable correlations between responses, regardless of the number of queries — i.e., the watermark is undetectable. Since the same hidden structure is present in every sample from Encode(1), our detector can simply apply Decode to check for this structure. Now, the detector's runtime has no dependence on the response variability. Using PRCs that we construct in Sections [5](#page-25-0) and [6,](#page-37-0) we also find that our watermarking scheme can be made robust to a constant fraction of random substitution and deletion errors.

A note on undetectability. Undetectability is a strong quality guarantee for watermarking. Outputs of the watermarked model must be computationally indistinguishable from outputs of the original model, even to a user who is allowed to make many queries. While this is imperative for steganography, its necessity in watermarking is less clear, as some noticeable changes to the model may be permissible as long as the outputs remain "high-quality."

However, measuring the quality of watermarked content is often challenging or impossible — especially when the content is used in a wide range of applications. Computational indistinguishability is a strong quality guarantee that applies uniformly to every application: it implies that the watermark causes no observable loss in any efficiently-computable quality metric. Without such a guarantee, it is impossible to verify that a watermark is quality-preserving across all applications. We therefore focus on undetectability in this work.

### <span id="page-4-0"></span>1.2 Our contributions

Pseudorandom codes (Sections [4](#page-22-0) to [6\)](#page-37-0). Our first contribution is to identify PRCs as an interesting cryptographic primitive, with applications to robustly hiding messages in AI-generated content. Very roughly, the definition is as follows — for more details, see either the technical overview (Section [2.1\)](#page-9-1) or the formal definitions (Section [4.1\)](#page-22-1).

Definition (Definitions [1](#page-22-2) and [2\)](#page-22-3). A pseudorandom code (PRC) is an error-correcting code where codewords are pseudorandom to any computationally-bounded adversary who doesn't hold the decoding key.

We consider both public- and secret-key variants of PRCs. For a public-key PRC, the encoding algorithm can be made public without sacrificing pseudorandomness. When the message space consists of only a single message, we call it a zero-bit PRC. Zero-bit PRCs can also be viewed as robust backdoored (or trapdoor) pseudorandom generators [\[VV83,](#page-64-1) [DGG](#page-63-0)<sup>+</sup>15], and they are sufficient for our applications to watermarking.

We show how to build zero-bit public-key PRCs related to low-density parity-check (LDPC) codes, where pseudorandomness rests on standard (subexponential) cryptographic assumptions. All of the PRCs we construct are over a binary alphabet. Depending on the parameter choices, the pseudorandomness of these LDPC-related codes is based on either of two assumptions, which we state together as Assumption [1.](#page-28-1)

Assumption (Assumption [1\)](#page-28-1). Either

- LPN is hard for any 2<sup>O</sup>( √ n) -time adversary, or
- LPN and planted XOR are both hard for any polynomial-time adversary.

For descriptions of the LPN and planted XOR assumptions, see either Section [2.2](#page-10-0) or Section [5.](#page-25-0) Under Assumption [1,](#page-28-1) we prove that there exist PRCs with robustness to channels that introduce a bounded number of substitution errors. We say that any channel that introduces at most a p fraction of substitution errors (and no other types of errors) is p-bounded.

Theorem (Theorems [1](#page-30-1) and [2\)](#page-36-0). Let p ∈ (0, 1/2) be any constant. Under Assumption [1,](#page-28-1) there exists a zero-bit public-key PRC that is robust to every p-bounded channel.

For some applications it will be useful to have multi-bit PRCs. Any such construction should ideally have a high rate, which is the ratio of the number of message bits to the number of codeword bits. We prove that any zero-bit PRC can be combined with any error correcting code to give a multi-bit PRC.

Theorem (Theorem [3\)](#page-39-1). Suppose that there exists a zero-bit (public-key) PRC and a rate-R error-correcting code, that are both robust to every p-bounded channel. Then there exists a (public-key) PRC of rate R − o(1) that is robust to every (p − ε)-bounded channel, for every constant ε > 0.

Applying this theorem with our zero-bit LDPC-based PRCs and the binary error-correcting codes of [\[ABN](#page-62-2)+92, [NN93,](#page-64-2) [Ta-17\]](#page-64-3), we have the following corollary.

Corollary. Let p ∈ (0, 1/2) be any constant. Under Assumption [1,](#page-28-1) there exists a constant-rate PRC that is robust to every p-bounded channel.

None of the PRCs mentioned so far can handle deletions. Deletions are a particularly important type of edit for text watermarks, because an adversary may try to remove the watermark by simply deleting some of the words.

Deletions are notoriously difficult to handle in error correction, and standard techniques involve significant structure — thus violating pseudorandomness. Nonetheless, we show that if a PRC has sufficiently strong robustness to substitutions, then it can be converted to a PRC with robustness to deletions (at the cost of a decreased rate).

Let BSC<sup>p</sup> be the binary symmetric channel with error rate p, and BDC<sup>q</sup> be the binary deletion channel with deletion rate q. That is, BSC<sup>p</sup> randomly flips each bit with probability p and BDC<sup>q</sup> randomly deletes each bit with probability q.

Theorem (Theorem [4\)](#page-44-0). For any constants p ∈ (0, 1/2) and q ∈ (0, 1), there exists p ′ ∈ (0, 1/2) such that the following holds. If there exists a zero-bit (public-key) PRC with robustness to every p ′ -bounded channel, then there exists a zero-bit (public-key) PRC that is robust to the channel BSC<sup>p</sup> ◦ BDCq.

Together with our LDPC-based PRCs, we obtain the following result.

Corollary. Let p ∈ (0, 1/2) and q ∈ (0, 1) be any constants. Under Assumption [1,](#page-28-1) there exists a zero-bit public-key PRC that is robust to the channel BSC<sup>p</sup> ◦ BDCq.

Watermarking and steganography for language models (Section [7\)](#page-45-0). We apply our zero-bit PRCs to build the first undetectable watermarking scheme for language models with robustness to a constant rate of random substitutions and deletions. In this section, we assume that text output by the language model is represented as a bitstring. Arbitrary text can be mapped to a bitstring by either randomly assigning a single bit to each token, or by expanding the tokens into a binary representation.

Theorem (Theorem [5\)](#page-54-2). Let p ∈ (0, 1/2) be any constant. Under Assumption [1,](#page-28-1) there exists an undetectable watermarking scheme W such that the watermark appears in any sufficiently high-entropy text, even if the text is subjected to the channel BSCp.

Under an extra assumption about the generated text, which roughly corresponds to the text having few repeated words, we can strengthen this to handle deletions as well.

Theorem (Theorem [6\)](#page-54-3). Let p ∈ (0, 1/2) and q ∈ (0, 1) be any constants. Under Assumption [1,](#page-28-1) there exists an undetectable watermarking scheme W such that the watermark appears in any sufficiently high-entropy and "variable" text, even if the text is subjected to the channel BSC<sup>p</sup> ◦ BDCq.

In all of our theorems the text can be cropped, as long as the remaining text is sufficiently high-entropy.

We also construct undetectable watermarking schemes with unforgeable public attribution and the same robustness as W. Public attribution means that there is a public algorithm to identify which portion of a given text was output by the model. Unforgeability means that no efficient user can produce text that the attribution algorithm identifies as model-generated, but that was not output by the model. Interestingly, our schemes retain the standard robust secret-key detector in addition to this public attribution algorithm.

Theorem (Theorem [8\)](#page-57-0). Under Assumption [1,](#page-28-1) there exists a watermarking scheme Watt that retains all properties of W from Theorem [5](#page-54-2) or Theorem [6,](#page-54-3) and additionally satisfies unforgeable public attribution.

Finally, using PRCs with constant rate (Theorem [3\)](#page-39-1), we also obtain the first robust language model steganography scheme.[2](#page-6-1)

Theorem (Theorem [7\)](#page-54-4). Let p ∈ (0, 1/2) be any constant. Under Assumption [1,](#page-28-1) there exists a language model steganography scheme with constant information rate, such that the message can be recovered from any sufficiently high-entropy text, even if the text is subjected to the channel BSCp.

Universal steganography (Section [8\)](#page-58-0). In Section [8](#page-58-0) we show that PRCs can be used to solve a longstanding open question in steganography: A simple application of PRCs yields the first robust, stateless universal steganography scheme. Universal steganography can be used for language model steganography, but it is more general [\[vAH04\]](#page-64-4). We take the rate of the steganography scheme to be the ratio of the number of stegotext symbols to the number of bits in the message being encoded.

Theorem (Theorem [9\)](#page-59-1). Suppose there is a hash function that is unbiased over the covertext channel. If PRC is any PRC, then there exists a stateless, public-key universal steganography scheme with the same rate and robustness as PRC.

Finally, we show that this result can be extended to the setting where an unbiased hash function on the covertext channel is not known, with some loss in robustness.

Theorem (Theorem [10\)](#page-61-0). Suppose there is a hash function that has constant min-entropy over the covertext channel. Then under Assumption [1,](#page-28-1) for any p ∈ (0, 1/2), there exists a constant-rate public-key stateless steganography scheme that is robust to a p rate of random substitutions.

### <span id="page-6-0"></span>1.3 Related work: short summary

We briefly outline some of the related work here. See Appendix [A](#page-65-0) for a more complete discussion.

- Code-based cryptography: Our work bears some similarity to the field of code-based cryptography. However, code-based cryptography is generally focused on building existing primitives from new assumptions — whereas PRCs are a new primitive that we base on existing assumptions.
- Trapdoor pseudorandom generators: Our zero-bit PRCs can be equivalently viewed as robust trapdoor (or equivalently, backdoored) pseudorandom generators [\[VV83,](#page-64-1) [DGG](#page-63-0)<sup>+</sup>15]. That is, we require the additional property that the trapdoor (or secret key) can be used to detect even corrupted pseudorandom strings.
- Watermarking for language models: We build watermarking schemes for language models satisfying the strongest quality guarantee, undetectability. Undetectability was defined by [\[CGZ23\]](#page-62-1), where undetectable watermarks for language models were also constructed. In that work and in [\[Aar22,](#page-62-3) [KGW](#page-63-1)<sup>+</sup>23a], it is essential for watermark detection that many sufficiently-long contiguous substrings of the response remain unchanged. Therefore, these watermarks are easily removable by simple attacks (see the "robustness of our watermark" paragraph of Section [2.5\)](#page-15-1). The watermarks of [\[KTHL23\]](#page-64-0) are more robust — their robustness is more comparable to ours — but they sacrifice undetectability. Instead, their watermarks satisfy the weaker property of distortion-freeness, which is the single-query

<span id="page-6-1"></span><sup>2</sup>Since this scheme doesn't rely on the decoder having access to the prompt, it can also be seen as an undetectable "multi-bit watermarking scheme."

version of undetectability. [\[ZALW23\]](#page-65-1) obtain even stronger robustness, at the cost of even further reduced quality.

- Impossibility of strong watermarks: [\[ZEF](#page-65-2)+23] explore the possibility of watermarking for language models in the presence of motivated adversaries. They argue that sampling a random response is easier when one is provided any response. Since a random response cannot be watermarked (or else there would be a high false-positive rate), they use this to argue that any watermarked language model necessarily provides some assistance in generating un-watermarked text.
- Steganography: Steganography is the study of concealing secret messages in innocent-looking content. Whereas encryption is about hiding the message, steganography is about hiding the existence of the message. Ever since steganography was formalized by [\[HLVA02\]](#page-63-2), robust steganography schemes (that don't require a shared state) have remained elusive. We resolve this problem using PRCs.

### <span id="page-7-0"></span>1.4 Organization

In Section [2,](#page-9-0) we give a technical overview of the paper, which is self-contained and sufficient to understand the high-level ideas and results of each section. In Section [3,](#page-20-0) we state relevant preliminaries and notation. In Section [4,](#page-22-0) we formally define PRCs and provide a heuristic construction. In Section [5,](#page-25-0) we build PRCs from LDPC codes and prove their pseudorandomness from standard cryptographic assumptions. We then show in Section [6](#page-37-0) how to improve the rate and robustness of any PRC, resulting in our constant-rate multi-bit PRCs and PRCs for deletion channels. In Section [7,](#page-45-0) we present our language model watermarking schemes from PRCs, including both our standard watermarks and our watermarks with unforgeable public attribution. Finally, in Section [8,](#page-58-0) we show how PRCs can be used to construct robust universal steganography schemes.

Appendix [A](#page-65-0) gives a more comprehensive overview of related work.

### <span id="page-7-1"></span>1.5 Differences from a previous version

This version of the paper contains two significant technical updates relative to the previous version, as well as a few editorial updates. The two significant updates address subtle technical issues, but do not substantially change any of the ideas or messages of the paper.

The first significant update is to the choice of parameters for which we invoke the planted XOR assumption (Assumption [3\)](#page-28-2). The previous version of the paper invoked the assumption with m, the number of samples, set to Ω(n). However, as pointed out to us by an anonymous CRYPTO 2024 reviewer, Theorem 4.26 of [\[ASS](#page-62-4)<sup>+</sup>23] (which is itself an updated version of a paper that we had cited in the old version of this paper) shows this assumption to be false. Fortunately we had only set m = Ω(n) because it made notation more convenient, and by instead setting m = n <sup>1</sup>−Ω(1), we avoid the attack without sacrificing any of our results. We have updated all of the relevant theorem statements and proofs in this version. We emphasize that this issue did not affect our other main proof that our LDPC-based PRCs are pseudorandom, because that proof only relies on LPN.

The other significant update regards the completeness and robustness of our watermarking scheme in Section [7.](#page-45-0) To sample a long response, we repeatedly sample fresh PRC codewords to bias the text. However, in order to argue that the resulting text contains the watermark, we need to ensure that the channel applied to the text is p-bounded — which, according to our definition, means that the error channel is not allowed to depend on the PRC key. But if the response contains multiple PRC blocks, then the error channel on one block could depend on codewords embedded in the previous blocks, violating this condition. In the prior version we had missed this issue, making our completeness and robustness claims incorrect. In this updated version we apply a one-time pad to each PRC codeword before embedding it, to ensure that the error channel cannot depend on the PRC key — thus resolving the issue.

Acknowledgements. We thank Yael Kalai, Venkat Guruswami, Rainer B¨ohme, Or Zamir, Shyamal Patel, and Shivam Nadimpalli for helpful research conversations. We additionally thank Vinod Vaikuntanathan for pointing out the LDPC-based PRC variant that we use to present Lemma [9](#page-31-0) in the Technical Overview. We thank Mihalis Yannakakis and Fermi Ma for helpful suggestions about the write-up. We thank Omar Alrabiah for help in proving Lemma [9,](#page-31-0) as well as general assistance with coding theory. We thank an anonymous CRYPTO 2024 reviewer for helpful feedback, especially regarding our use of the planted XOR assumption (Assumption [3\)](#page-28-2).

### <span id="page-9-0"></span>2 Technical overview

### <span id="page-9-1"></span>2.1 Pseudorandom code basics

Pseudorandom codes (PRCs) can be viewed as a combination of two related primitives:

- Pseudorandom encryption, where ciphertexts are indistinguishable from random under a chosen plaintext attack [\[RBB03\]](#page-64-5). Secret-key pseudorandom encryption is easy to build using a pseudorandom function Fsk — just encrypt m by sampling a random r and outputting (r, m ⊕ Fsk(r)). Public-key pseudorandom encryption is also known from standard assumptions [\[vAH04\]](#page-64-4). However, none of these constructions have any nontrivial robustness.
- Robust encryption, where encryptions of messages are robust to errors. Robust encryption is easy to build by applying an error-correcting code to ciphertexts from any standard encryption scheme. Even if that encryption scheme is pseudorandom, the use of the error-correcting code will in general render the robust encryption scheme not pseudorandom.

A PRC is required to simultaneously satisfy both pseudorandomness and robustness — properties that are in direct tension with each other. Using the secret key, one should be able to discern the redundancy and structure that give ciphertexts their robustness. Without the secret key, ciphertexts must appear completely unstructured.

We define secret-key PRCs below. For public-key PRCs (Definition [2\)](#page-22-3), we further require that the encoding algorithm can be made public without sacrificing pseudorandomness.

Definition (Definition [1\)](#page-22-2). Let Σ be an alphabet and E : Σ<sup>∗</sup> → Σ <sup>∗</sup> be a channel. A secret-key PRC with robustness to E is described by algorithms Encodesk : Σ<sup>k</sup> → Σ <sup>n</sup> and Decodesk : Σ<sup>∗</sup> → Σ <sup>k</sup>∪{⊥}, parameterized by a secret key sk, satisfying the following criteria for every security parameter λ:

• (Error correction, or robustness) For any message m ∈ Σ k ,

$$\Pr\_{\mathsf{sk}}[\mathsf{Decode}\_{\mathsf{sk}}(\mathcal{E}(x)) = \mathsf{m} : x \leftarrow \mathsf{Encode}\_{\mathsf{sk}}(\mathsf{m})] \geq 1 - \mathsf{negl}(\lambda).$$

• (Soundness) For any fixed c ∈ Σ ∗ ,

$$\Pr\_{\mathsf{sk}}[\mathsf{Decode}\_{\mathsf{sk}}(c) = \bot] \ge 1 - \mathsf{negl}(\lambda).$$

• (Pseudorandomness) For any polynomial-time adversary A,

$$\left| \Pr\_{\mathsf{sk}}[\mathcal{A}^{\mathsf{Encode}\_{\mathsf{sk}}}(1^{\lambda}) = 1] - \Pr\_{\mathsf{tl}}[\mathcal{A}^{\mathsf{lt}}(1^{\lambda}) = 1] \right| \le \mathsf{negl}(\lambda),$$

where A<sup>U</sup> means that the adversary has access to an oracle that, on any (even previously queried) input, responds with a freshly drawn uniform value in Σ<sup>n</sup>.

If the scheme can only encode a singular message (i.e. k = 0), then we call it a zero-bit PRC. Soundness is a technical condition that we include only to ensure that zero-bit PRCs are non-trivial.

For a sufficiently weak channel E, it is not hard to construct a secret-key PRC with robustness to E where pseudorandomness rests on very mild assumptions. For instance, if Fsk : {0, 1} <sup>ℓ</sup> → {0, 1} is a pseudorandom function, we can build a zero-bit secret-key PRC with the following encoding algorithm:

- Encodesk(1):
- 1. Randomly sample x1, . . . , x<sup>ℓ</sup> ← {0, 1}.
- 2. For i = ℓ + 1, . . . , n, let x<sup>i</sup> = Fsk(xi−ℓ, . . . , xi−1).

3. Output x1, . . . , xn.

The decoding algorithm Decodesk simply checks whether much more than a 1/2 fraction of conditions x<sup>i</sup> = Fsk(xi−ℓ, . . . , xi−1) are satisfied. Pseudorandomness follows by taking ℓ to be the security parameter. It is immediate that this PRC is robust to any length-preserving channel that introduces at most a p fraction of errors, for p << 1/ℓ. We call any such channel p-bounded.

This secret-key PRC construction can be seen as implicit in prior hash-based watermarking schemes [\[Aar22,](#page-62-3) [KGW](#page-63-1)+23a, [CGZ23\]](#page-62-1), where essentially the same level of robustness to a 1/ℓ error rate is obtained. Unfortunately, it has an inherent trade-off between pseudorandomness and robustness: After roughly 2ℓ/<sup>2</sup> samples from Encodesk(1), there will be repeated prefixes and therefore correlations between the samples. In particular, if we want this PRC to be robust to a constant rate of errors, we have to set ℓ = O(1), in which case even a constant number of queries are enough to observe correlations. We therefore turn to alternative constructions.

### <span id="page-10-0"></span>2.2 Pseudorandom LDPC codes

Fortunately, one of the most prominent assumptions in theoretical cryptography is a statement about codes: Learning Parity with Noise (LPN). The LPN assumption states that noisy samples from the codespace of a random linear code are pseudorandom, even to an adversary who knows a generator matrix for the code. In more detail, let n, g be integers and G ← F n×g <sup>2</sup> be a random matrix. The LPN assumption (with noise rate η and secrets of size g) states that (G, Gs ⊕ e) ≈ (G, u),[3](#page-10-1) where s ← F g 2 , e ← Ber(n, η), and u ← F n 2 .

The LPN assumption suggests using noisy codewords from a random linear code as a PRC. That is, let G ← F n×g <sup>2</sup> be the secret key and Encode<sup>G</sup> be the following zero-bit secret-key PRC encoder:

• EncodeG(1): Sample s ← F g 2 and e ← Ber(n, η). Output Gs ⊕ e.

The LPN assumption immediately implies that an arbitrary polynomial number of samples from EncodeG(1) are pseudorandom. However, recall that the LPN assumption states that these samples are pseudorandom even given G — which means precisely that there does not exist an efficient zero-bit decoder DecodeG(x)!

While this random linear code construction does not work, it naturally suggests a strategy that does. If we find a sampling procedure that produces a random (or even pseudorandom) generator matrix G together with a trapdoor for efficient decoding, then we have a public-key PRC where the generator matrix is the public encoding key and the trapdoor is the secret decoding key. By the LPN assumption, EncodeG(1) produces pseudorandom vectors even to an adversary who knows G, so the construction will satisfy pseudorandomness.

It turns out that low-weight parity checks can serve as such a trapdoor. That is, instead of sampling G uniformly at random, we first sample a "parity-check matrix" P ∈ F r×n <sup>2</sup> with sparse rows (i.e., "low density"), and then sample G ∈ F n×g 2 subject to P G = 0. For appropriate choice of n, g, t, r, we will show that the resulting marginal distribution on G is random or pseudorandom. The low-density parity-check matrix P will allow for efficient detection of near-codewords.

Codes defined by Low-Density Parity-Check matrices are called LDPC codes. For n, g, t, r ∈ N, we define an (n, g, t, r) random LDPC code by the following distribution over parity-check and generator matrices:

- LDPC[n, g, t, r]:
- 1. Sample a random matrix P ∈ F r×n 2 subject to every row of P being t-sparse.
- 2. Sample a random matrix G ∈ F n×g 2 subject to P G = 0.
- 3. Output (P, G).

Zero-bit decoding works by counting the number of satisfied parity checks. For any fixed x ∈ F n 2 , with high probability over P ∈ F r×n <sup>2</sup> we expect that the number of unsatisfied parity checks, wt(P x), is roughly r/2.

<span id="page-10-1"></span><sup>3</sup>Throughout this work we use ≈ to refer to computational indistinguishability.

But if x is close to Im G ⊆ ker P in Hamming distance, then as long as the error and the sparsity t of the parity checks are not too high, we expect wt(P x) to be significantly smaller than r/2.

Therefore our zero-bit pseudorandom LDPC code uses the following zero-bit decoding algorithm:

• Decode<sup>P</sup> (x): If wt(P x) < (1/2 − r −1/4 ) · r, output 1; otherwise output ⊥. [4](#page-11-0)

Encoding is exactly the same Encode<sup>G</sup> algorithm as above — but now that G is sampled together with the trapdoor P, we have an efficient decoding algorithm. Observe that this is a zero-bit scheme, because the decoder only determines whether the input is related to the keys or not. Using belief propagation, it is possible to push this construction beyond a zero-bit PRC, although this results in lower robustness. We ultimately construct a constant-rate multi-bit PRC by other means, which we discuss in Section [6.2.](#page-39-0)

Let LDPC-PRC<sup>0</sup> be the zero-bit public-key PRC defined by (EncodeG, Decode<sup>P</sup> ) for (P, G) ← LDPC[n, g, t, r]. In a moment we will outline our proofs that LDPC-PRC<sup>0</sup> is a public-key PRC with very strong robustness. First, let us see some restrictions on the sparsity parameter t that provide important context for these proofs.

If random noise of rate 1/2−ε is applied to x ∈ Im G, then the probability of each parity check being satisfied for the noisy codeword is 1/2 − (2ε) <sup>t</sup>/2. So in order for Decode<sup>P</sup> (x) to output 1 with high probability, we need (2ε) <sup>t</sup>/2 > r−1/<sup>4</sup> , i.e., t < 1 + log r/4 log(1/2ε) = O(log r). We will always have r = n Ω(1), so this restriction says that t = O(log n) for appropriate choice of constant.

On the other hand, if we set t = O(1) then EncodeG(1) cannot be pseudorandom. This is because it is possible to brute-force search over all <sup>n</sup> t possible parity checks of weight t, and one can test whether Encode<sup>G</sup> is consistent with a given parity check s ∈ F n <sup>2</sup> by simply computing s · x for many samples x ← EncodeG(1).

Therefore, we will choose t = Θ(log n) in order to rely on the weakest possible cryptographic assumption for pseudorandomness, without sacrificing robustness to a constant noise rate.

Remark. The LDPC codes considered in this work differ from the traditional Gallager's LDPC ensemble in two important ways. First, our LDPC codes will have t = Θ(log n) sparsity as opposed to constant sparsity. Unfortunately, the usual belief propagation decoder does not work for noise rates beyond O(log t/t); this is the reason why we only perform the simple zero-bit decoding. The second difference is that we use independent parity checks, which results in an irregular Tanner graph.

Remark. There is a well-known public-key encryption scheme, due to Alekhnovich [\[Ale03,](#page-62-5) Cryptosystem 1], based on a low-noise variant of LPN. This scheme is similar to ours, but the decoder cannot tolerate any constant rate of errors.

Pseudorandom generator matrix (Lemma [8\)](#page-29-0). For appropriate choices of parameters, it turns out that the generator matrix of LDPC[n, g, t, r] is pseudorandom under the planted t-XOR assumption. The planted t-XOR problem (and its generalization, the planted t-SUM problem) is a natural and well-studied problem — see e.g. [\[ASS](#page-62-4)<sup>+</sup>23] for a more detailed discussion. Formally, the (n, m, t) planted XOR problem states that it is computationally hard to distinguish between

- D m 0 : a random m-dimensional linear subspace V ⊆ F n 2 , and
- D m 1 : a random m-dimensional linear subspace V<sup>s</sup> ⊆ F n 2 satisfying a random planted t-XOR relation s (i.e., s is a random t-sparse vector and s · v = 0 for all v ∈ Vs).

Throughout this overview, we consider linear subspaces to be described by a random basis. Recalling the definition of (P, G) ← LDPC[n, g, t, r], if r = 1 the (n, g, t) planted XOR assumption immediately implies that G is pseudorandom (by identifying V with Im G). But for the more interesting case that r > 1, we require a stronger version of the planted XOR assumption with many planted relations. That is, we need to assume that the following distribution is indistinguishable from D m 0 :

<span id="page-11-0"></span><sup>4</sup>Throughout this work, wt will refer to Hamming weight.

D m r : a random m-dimensional linear subspace Vs1,...,s<sup>r</sup> ⊆ F n 2 satisfying r random planted t-XOR relations s1, . . . , s<sup>r</sup> (i.e., s1, . . . , s<sup>r</sup> are random t-sparse vectors and s<sup>1</sup> · v = · · · = s<sup>r</sup> · v = 0 for all v ∈ Vs1,...,s<sup>r</sup> ).

We are not aware of any prior work on this assumption that D m <sup>0</sup> ≈ D<sup>m</sup> r , so it is not immediately clear how reliable it is. Fortunately, it is implied by the (n, m + r, t) planted XOR assumption.

We prove this with a hybrid argument. Suppose that an efficient adversary A distinguishes between D m 0 and D m <sup>r</sup> with advantage ε > 0. By a telescoping argument, A must distinguish between D m <sup>i</sup> and D m i+1 with advantage ε/r, for some i ∈ {0, . . . , r − 1}. For each i, the following efficient reduction Red<sup>i</sup> satisfies Redi(D m+r 0 ) ≡ D<sup>m</sup> <sup>i</sup> and Redi(D m+r 1 ) ≡ D<sup>m</sup> <sup>i</sup>+1, which implies that ε/r (and therefore ε) is negligible under the (n, m + r, t) planted XOR assumption.

Redi(W):

- 1. Sample i random t-sparse vectors s1, . . . , s<sup>i</sup> ∈ F n <sup>2</sup> and let S = {v ∈ F n 2 : v · s<sup>j</sup> = 0 ∀j ∈ [i]}.
- 2. Let U = W ∩ S. Notice that dim U ≥ dim W − i. Since dim W = m + r and i < r, this is at least m.
- 3. Output a random m-dimensional subspace of U.

It remains to see why Redi(D m+r 0 ) ≡ D<sup>m</sup> <sup>i</sup> and Redi(D m+r 1 ) ≡ D<sup>m</sup> <sup>i</sup>+1. In fact both of these statements are true even for fixed planted relations.

- Redi(D m+r 0 ) ≡ D<sup>m</sup> i . Fix s1, . . . , s<sup>i</sup> sampled in Red<sup>i</sup> and let S = {v ∈ F n 2 : v ·s<sup>j</sup> = 0 ∀j ∈ [i]}. Since W is a random subspace of F n 2 , conditioned on any d = dim(W ∩ S), U = W ∩ S is a random d-dimensional subspace of S. Therefore the output of Redi(D m+r 0 ) is a random m-dimensional subspace of S.
- Redi(D m+r 1 ) ≡ D<sup>m</sup> <sup>i</sup>+1. Fix s1, . . . , s<sup>i</sup> sampled in Red<sup>i</sup> and let S = {v ∈ F n 2 : v · s<sup>j</sup> = 0 ∀j ∈ [i]}, as above. Suppose that W ← Dm+<sup>r</sup> 1 is sampled with the planted relation s. Fix s and let S ′ = {v ∈ S : v · s = 0}. Again, conditioned on any d = dim(W ∩S), U = W ∩S = W ∩S ′ is a random d-dimensional subspace of S ′ . Therefore the output of Redi(D m+r 1 ) is a random m-dimensional subspace of S ′ .

Narrow, statistically random generator matrix (Lemma [9\)](#page-31-0). Since the planted XOR assumption is not a standard cryptographic assumption, we show in Lemma [9](#page-31-0) that the generator matrix of LDPC[n, c log<sup>2</sup> n, log n, 0.99n] is statistically random for some c > 0. This removes the need for the planted XOR assumption, but it comes at the cost of requiring a stronger version of the LPN assumption: When we invoke LPN to see that samples (G, Gs ⊕ e) are pseudorandom, the secrets s are now only of size c log<sup>2</sup> n. Therefore, for this PRC we will rely on a subexponential version of the LPN assumption which states that LPN is 2<sup>O</sup>( √ n) -hard.

For the purposes of this technical overview, we will show that the generator matrix of a closely related code is random. The proof for this version is significantly simpler, but the distribution is less natural and has worse error-correcting properties. The modified distribution on (P, G) is defined as follows:

.

- 1. Sample a uniformly random G<sup>0</sup> ← F 0.01n×g 2
- 2. For i ∈ [0.99n]:
	- (a) Sample a random (t − 1)-sparse s<sup>i</sup> ∈ F 0.01n 2
	- (b) Let G<sup>i</sup> be the matrix Gi−<sup>1</sup> with the extra row s T <sup>i</sup> G<sup>0</sup> appended to the bottom,

.

$$G\_i = \begin{bmatrix} G\_{i-1} \\ s\_i^T G\_0 \end{bmatrix}$$

.

- (c) Let s ′ <sup>i</sup> = [s T i , 0 i−1 , 1, 0 0.99n−i ].
- 3. Let P be the matrix whose rows are s ′ 1 , . . . , s′ <sup>0</sup>.99<sup>n</sup> and G = G0.99<sup>n</sup>. Output (P, G).

First observe that P G = 0, because s ′ <sup>i</sup>G = [s T i , 0 i−1 , 1, 0 0.99n−i ]G = s T <sup>i</sup> G<sup>0</sup> ⊕(s T <sup>i</sup> G0) = 0 for every i ∈ [0.99n].

The leftover hash lemma immediately implies that G is statistically random. Recall that the leftover hash lemma states that if A ← F g×ℓ 2 is a uniformly random matrix and s ∈ F ℓ <sup>2</sup> has min-entropy µ, then (A, As) is 2 −(µ−g)/2 -close to uniform in statistical distance. In our case, we use A = G<sup>T</sup> <sup>0</sup> and s = s<sup>i</sup> to see that s T <sup>i</sup> G<sup>0</sup> is 2−(log ( 0.01n <sup>t</sup> )−g)/<sup>2</sup> -close to uniform in statistical distance for each i ∈ [n − g]. If t = Ω(log n), then there is a choice of g = Ω(log<sup>2</sup> n) such that 2−(log ( 0.01n <sup>t</sup> )−g)/<sup>2</sup> = 2−Ω(log<sup>2</sup> <sup>n</sup>) = negl(n), completing the proof.

LDPC-PRC<sup>0</sup> is robust to any p-bounded channel (Lemma [4\)](#page-26-1). Recall that we say that any lengthpreserving channel that introduces at most a p fraction of bit-flip errors is p-bounded. To prove robustness, we need to show two things:

- 1. any fixed x ∈ F n <sup>2</sup> decodes to ⊥ with high probability, and
- 2. for any p-bounded channel E, samples from E(EncodeG(1)) decode to 1 with high probability.

Unfortunately, (1) does not quite hold for the scheme presented above. The issue is that, while most fixed strings will decode to ⊥, a small fraction of strings will decode to 1 regardless of P. For instance, 0 will always decode to 1 because wt(P · 0) = 0 for any P. Therefore we modify our scheme slightly by using a one-time pad z ∈ F n 2 , included in the public key. The modified EncodeG(1) outputs Gs ⊕ e ⊕ z, and Decode<sup>P</sup> (x) computes wt(P x ⊕ P z) instead of wt(P x); this is the actual scheme we describe in Section [5.](#page-25-0)

Now, for any fixed x ∈ F n 2 , wt(P x ⊕ P z) is distributed identically to wt(P z) because z is uniform. In Section [5.4](#page-30-0) we will see that P is full rank with high probability, so P z is uniformly random. By a Chernoff bound, wt(P z) ≥ (1/2−r −1/4 )·r with high probability and therefore Decode<sup>P</sup> (x) outputs ⊥. This concludes the proof of (1), so we turn to (2).

Suppose that we sample Gs ⊕ e ⊕ z ← EncodeG(1) and apply some p-bounded channel E. The one-time pad effectively converts E to a fixed error channel, independent of P, G, s, e: Suppose that E(x) = x⊕e(x), where e(x) is a random variable depending on x. Since E is p-bounded, wt(e(x)) ≤ p · n. Letting y = Gs ⊕ e ⊕ z, we have

$$\begin{aligned} \mathcal{E}(Gs \oplus e \oplus z) \oplus z &= (Gs \oplus e \oplus z) \oplus e(Gs \oplus e \oplus z) \oplus z \\ &=Gs \oplus e \oplus e(y) \end{aligned}$$

where y is uniformly random in F n 2 , independent of P, G, s, e because of z. Now it only remains to see that wt(P(Gs ⊕ e ⊕ e(y))) = wt(P(e ⊕ e(y))) < (1/2 − r −1/4 ) · r with high probability. Since e and e(y) are independent errors, each of weight (1/2 − Ω(1)) · n, the combined error e ⊕ e(y) also has weight (1/2 − Ω(1)) · n. Therefore, if the row sparsity t of P is c log n for sufficiently small constant c, then we will have wt(P(e ⊕ e(y))) < (1/2 − r −1/4 ) · r with high probability, completing the proof of (2).

### <span id="page-13-0"></span>2.3 Pseudorandom codes for the deletion channel

So far, we have only considered PRCs for substitution channels. For our applications to watermarking and steganography, it will be useful to have PRCs for the noisy deletion channel as well. The noisy deletion channel randomly introduces both deletions and substitutions.

Unfortunately, existing error-correcting codes for the deletion channel introduce a large amount of structure into codewords that precludes pseudorandomness. For instance, the popular techniques of synchronization symbols or concatenation with constant-sized inner codes are immediately seen to be incompatible with pseudorandomness. Even further limiting the techniques available to us, we want our PRCs for the noisy deletion channel to have a binary alphabet in order to be useful for watermarking.

We therefore turn to alternative techniques. Surprisingly, we find that the repetition code — perhaps the simplest and most-structured error-correcting code — is a useful starting point.

For odd integer T, the rate-(1/T) repetition code works by repeating each bit of the message T times. That is, for any message m = (m1|| · · · ||mk) ∈ {0, 1} k , the encoder RepEnc<sup>T</sup> is defined by RepEnc<sup>T</sup> (m) = (m1) T || · · · ||(mk) T , where (mi) <sup>T</sup> denotes bit m<sup>i</sup> repeated T times. For example, the rate-(1/3) repetition code encodes 010 as RepEnc<sup>T</sup> (010) = 000111000.

Now suppose that the encoding (m1) T || · · · ||(mk) T is subjected to the noisy deletion channel, resulting in a string z. A natural algorithm for decoding z is to partition z into k equal-length blocks z1, . . . , zk, and compute the majority of each block:

MajDec<sup>k</sup> (z):

- 1. Partition z into k equal-length blocks z = (z1|| · · · ||zk).
- 2. Output (Maj(z1)|| · · · || Maj(zk)).

As long as the deletions are sufficiently balanced across the different blocks, the z<sup>i</sup> will align well with the original blocks (mi) T . Provided further that there are not too many substitutions in any block, we should have MajDec<sup>k</sup> (z) = m. The issue is that RepEnc<sup>T</sup> (m) is not pseudorandom even for random m, because a random string is (extremely) unlikely to consist of T repeated bits.

On the other hand, a random string typically does have Θ(<sup>√</sup> T) bias towards 0 or 1.[5](#page-14-0) So if we change or delete a small O( √ T) number of bits of a random string, we expect the majority to stay the same. This observation brings us to the following encoder MajEnc<sup>T</sup> , which encodes each bit in the majority of a random string. We refer to the code defined by (MajEnc<sup>T</sup> , MajDec<sup>k</sup> ) as the majority code.

#### MajEnc<sup>T</sup> (m):

- 1. For i ∈ [k], let z<sup>i</sup> be a random sample from {0, 1} T conditioned on Maj(zi) = m<sup>i</sup> .
- 2. Output (z1|| · · · ||zk).

Now if m is random, then z = MajEnc<sup>T</sup> (m) is random as well. Furthermore, if we subject z to the noisy deletion channel to obtain z ′ , then the bits of m′ = MajDec<sup>k</sup> (z ′ ) are positively correlated with the bits of m. This is because the deletions are at random locations, and are therefore (roughly) evenly-distributed across the different blocks z<sup>i</sup> — meaning that MajDec<sup>k</sup> will mostly use the correct locations to decode each bit. Since the bit-flip errors are random, they merely dilute the Θ(<sup>√</sup> T) biases. If T >> k and the rates of deletions and bit-flip errors are constants below 1 and 1/2 respectively, then we show in Lemma [15](#page-41-0) that Pr[m<sup>i</sup> = m′ i ] is a constant greater than 1/2. Therefore, the majority code has the effect of converting the constant-rate noisy deletion channel into some p-bounded channel.

Of course, the majority code is not itself a PRC. The first problem is that codewords for the majority code are only random if the message is random, whereas a PRC needs to allow encoding of any particular message. The second problem is that, even if the message is random, the majority code recovers a string that is only correlated with it.

But these are exactly the problems solved by PRCs for bounded-weight error channels! That is, if PRC is any PRC with robustness to every p-bounded channel (e.g. the PRCs from Section [2.2\)](#page-10-0), then the combined code PRCdel = (MajEnc ◦ PRC.Encode, PRC.Decode ◦ MajDec) is a PRC with robustness to some constantrate noisy deletion channel.[6](#page-14-1) Pseudorandomness follows from the pseudorandomness of PRC.Encode: Since PRC.Encode(m) is pseudorandom for any message m, MajEnc(PRC.Encode(m)) is as well. Robustness follows from the fact that the majority code has the effect of converting the constant-rate noisy deletion channel into some p-bounded channel, which is handled by PRC.Decode.

<span id="page-14-0"></span><sup>5</sup>That is, a random string has Θ(<sup>√</sup> T) more 0's than 1's, or 1's than 0's. This can be seen as a consequence of the fact that a one-dimensional simple random walk of length <sup>T</sup> will usually terminate Θ(<sup>√</sup> T) away from the origin.

<span id="page-14-1"></span><sup>6</sup>As p approaches 1/2, the combined PRC tolerates a noisy deletion channel with rates of deletions and bit-flip errors approaching 1 and 1/2.

### <span id="page-15-0"></span>2.4 Constant-rate pseudorandom codes

So far we have only considered zero-bit PRCs, but for many applications it will be useful to have PRCs that can encode longer messages. There is a simple construction of a multi-bit PRC directly from any zero-bit PRC: Encode each bit of the message with either a zero-bit PRC codeword, or a uniformly random string. That is, if PRC is a zero-bit PRC, we encode a message m ∈ {0, 1} <sup>k</sup> as (x1|| · · · ||xk) where for each i ∈ [k], x<sup>i</sup> ← {0, 1} <sup>n</sup> if m<sup>i</sup> = 0 and x<sup>i</sup> ← PRC.Encode(1) if m<sup>i</sup> = 1.

Unfortunately this scheme has a very low rate. If the zero-bit PRC has block length n, then the resulting multi-bit PRC has rate 1/n. However, we show in Section [6.2](#page-39-0) that one can use any such low-rate PRC to make any error-correcting code pseudorandom, with no asymptotic loss in rate.

The idea is to encode a seed for a one-time pad in the simple low-rate PRC just described, and then use the one-time pad to hide an error-correcting encoding of the message. More formally, let (Enc, Dec) be any (standard) error-correcting code and PRC be a low-rate PRC. We do not require (Enc, Dec) to have any cryptographic properties. We encode a message m as[7](#page-15-2)

PRC.Encode(r), Enc(m) ⊕ PRG(r),

where PRG is any pseudorandom generator and r ← {0, 1} k is a fresh uniformly random string.

By pseudorandomness of PRC, PRC.Encode(r) is indistinguishable from a uniformly random string — even for a fixed choice of r. By security of PRG, the encoding is therefore indistinguishable from a totally random string.

Decoding works as long as PRC.Encode(r) is not too corrupted for PRC to recover r, and Enc(m) ⊕ PRG(r) is not too corrupted for Dec to recover m.

### <span id="page-15-1"></span>2.5 Watermarks for language models

In this work, a generative language model is formally described by an algorithm Model that takes as input a prompt prompt and a sequence of tokens output thus far t1, . . . ,ti−1, and produces a distribution over the next token. A full response is generated by iteratively sampling from these distributions, at each step providing Model with the partial response, and terminating once a special "done" token is sampled. For simplicity, we assume here that tokens are binary, which allows us to specify the distribution p<sup>i</sup> over the next token as a Bernoulli distribution Ber(pˆi) where pˆ<sup>i</sup> := E[p<sup>i</sup> ] ∈ [0, 1]. We also assume for the purposes of this technical overview that the model always generates a response of length n. In Section [7](#page-45-0) we explain why neither of these assumptions is important for our results.

As defined in [\[CGZ23\]](#page-62-1), a watermarking scheme for a language model consists of algorithms Wat and Detect, where Wat is the watermarked model and Detect is an algorithm used to detect the presence of the watermark. In this work we are interested in watermarks that are undetectable, sound, and robust, loosely defined as follows.

- Undetectability: Any polynomial number of responses from the watermarked model are computationally indistinguishable from those of the original model.
- Soundness: Text generated independently of the watermarked model is not falsely detected.
- Robustness: Sufficiently high-entropy text output by the model is detected as watermarked, even if it is altered.

We show that the watermarking strategy from Section [1,](#page-2-0) which replaces some of the model's randomness with PRC codewords, yields a scheme that satisfies all of the above properties.

<span id="page-15-2"></span><sup>7</sup> In order to obtain stronger robustness guarantee, we actually randomly permute the symbols of this encoding. For the purposes of this technical overview we omit this detail.

Defining Generate for language models. Recall that the approach from Section [1](#page-2-0) requires an algorithm Generate that takes as input a prompt and a random seed x ∈ {0, 1} <sup>n</sup>, and samples a response t ∈ {0, 1} n such that

- <span id="page-16-1"></span><span id="page-16-0"></span>(1) if x is uniformly random, then t is distributed identically to a response from Model, and
- (2) each bit of t is correlated with the corresponding bit of x.

We define Generate(prompt, x) to sample the i th bit t<sup>i</sup> of the response as follows. It first computes p<sup>i</sup> by querying Model with prompt and the response output thus far, then:

- If pˆ<sup>i</sup> ≤ 1/2, sample t<sup>i</sup> ← Ber(2xipˆi).
- If pˆ<sup>i</sup> > 1/2, sample t<sup>i</sup> ← Ber(1 − 2(1 − xi)(1 − pˆi)).

For any pˆ<sup>i</sup> ∈ [0, 1], one can easily see that t<sup>i</sup> is distributed as Ber(pˆi) since x<sup>i</sup> is a uniformly random bit. This means that Generate satisfies Condition [\(1\)](#page-16-0) above.

For Condition [\(2\),](#page-16-1) the bias toward the seed is stronger the closer pˆ<sup>i</sup> is to 1/2. It is strongest when pˆ<sup>i</sup> = 1/2 exactly, in which case t<sup>i</sup> is sampled from Ber(xi) and is therefore equal to x<sup>i</sup> . At the other extreme, if pˆ<sup>i</sup> = 0 or 1, there is no bias. In general the response is a noisy version of the seed, where the amount of noise on the i th token decays as the binary entropy of Ber(pˆi) grows.

Replacing seeds with PRC codewords. We use PRC samples x ← PRC.Encode(1), instead of random samples x ← {0, 1} <sup>n</sup>, as the seeds in Generate. That is, if PRC is a zero-bit PRC, we let our watermarking scheme W[PRC] be defined by

Wat(prompt): Sample x ← PRC.Encode(1) and output a sample from Generate(prompt, x).

Detect(t): Compute PRC.Decode(t) and output the result.

By Condition [\(1\)](#page-16-0) and the pseudorandomness property of PRC, the responses from Wat are computationally indistinguishable from those of the original model. By Condition [\(2\)](#page-16-1) and the robustness property of PRC, the watermark will be detectable as long as the PRC is sufficiently powerful.

Remark. Depending on the kind of robustness of the PRC, substituting the entire seed with a single PRC sample results in a watermark that may or may not be detectable from just a subsequence. This is easily fixed by using x = (x1|| · · · ||xm), where x<sup>i</sup> ← PRC.Encode(1) are independent PRC samples that are much shorter than the generated content. As long as the text contains at least one subsequence corresponding to a PRC sample xi, the watermark will be detected.

PRC error correction and watermark robustness. To understand how error correction of PRC translates to robustness of W[PRC], it is helpful to think of Generate's sampling process as a noisy embedding channel applied to the seed. That is, for a seed x ∈ {0, 1} <sup>n</sup>, let EEmb(x) = Generate(prompt, x) be the "embedding channel" describing the noise in x 7→ t. For detection, it is sufficient for PRC to correct against the channel EEmb, since watermarked responses are exactly samples from EEmb(x) for x ← PRC.Encode(1).

Robustness of W[PRC] is determined by PRC's ability to correct from additional errors on top of EEmb. Let Eadv be a channel modeling the changes an adversary introduces to a watermarked response, so the overall error applied to t follows Eadv ◦ EEmb. If PRC is robust to Eadv ◦ EEmb, the watermark is robust to this adversary's modifications.

In Section [7.2,](#page-48-0) we show that as long as the text has non-zero entropy, EEmb introduces errors at a rate of less than 1/2. Therefore, using any PRC with robustness to every p-bounded channel, we immediately obtain watermarks that are robust to a constant rate of random substitutions.

Robustness of our watermark. Hashing-based watermarking schemes — including all existing undetectable schemes — are removable by the simple "emoji attack" [\[Aar22,](#page-62-3) [KGW](#page-63-1)+23a]. In this attack, an adversary asks the model to respond to its prompt and insert an emoji between every word of its response. The adversary then deletes the emojis from the response. This attack removes any watermark that relies on the detector seeing contiguous sequences of watermarked text.

It turns out that hashing-based schemes [\[Aar22,](#page-62-3) [KGW](#page-63-1)+23a, [CGZ23\]](#page-62-1) can easily be made robust to this particular attack.[8](#page-17-1) However, if the adversary instead instructs the model to insert the emojis randomly, then we do not know how to make any hashing-based scheme robust. By constructing PRCs with robustness to random deletion channels, we give the first undetectable watermarking scheme that can resist this kind of attack.

In order to show this, we require a stronger assumption on the response: That EEmb behaves as the binary symmetric channel BSC<sup>q</sup> for some q ∈ (0, 1/2). The binary symmetric channel BSC<sup>q</sup> is the channel that flips each bit of its input independently with probability q, so BSCq(x) = x ⊕ Ber(q) for x ∈ {0, 1}. Essentially, this is equivalent to the assumption that the response has high entropy and does not repeat words too often.

Under this assumption, if Eadv = BDC<sup>p</sup> is the binary deletion channel for some p ∈ (0, 1), then we just need a PRC with robustness to Eadv ◦ EEmb = BDC<sup>p</sup> ◦ BSCq. The binary deletion channel BDC<sup>p</sup> is the channel that deletes each bit of its input independently with probability p. Indeed, we saw in Section [2.3](#page-13-0) that there exist PRCs with robustness to BDC<sup>p</sup> ◦ BSC<sup>q</sup> for any p ∈ (0, 1), q ∈ (0, 1/2).

### <span id="page-17-0"></span>2.6 Watermarks with public attribution

For the "standard" notions of watermarks considered so far, the goal is to determine whether a given text is a possibly-corrupted version of an output generated by a model. Standard watermarks are well-suited for applications such as detecting plagiarism, where one wishes to know if a model was used at all to produce a text, even if that text has been altered by the user.

A different use of watermarks is in attributing content to an LLM that generated it. For example, if harmful content generated by an LLM is found on social media, it would be useful to trace this content back to the model using the watermark. Ideally, anyone holding a public detection key should be able to trace the content. On the other hand, it should only be possible to embed the watermark by using a secret embedding key, in order to avoid falsely attributing text to any model.[9](#page-17-2) In other words, to an attacker who does not know the secret key, the watermark should be unforgeable.

In addition to unforgeability, watermarks with public attribution have subtly different detection properties than standard watermarks. Robustness of standard watermarks means that an LLM-generated text will be detected even if small modifications are made. If robust watermarks were used for attribution, an attacker could use a model to generate a benign watermark text, then change a few words to make it offensive. By robustness, the watermark would still be present in this now-offensive content. So whereas robustness is a useful feature for standard watermarking, in the context of attribution it is actually an issue.

We therefore define a watermark with public attribution to have a separate detection algorithm called AttrText, which is intentionally designed to not be robust. AttrText, given a text x and a public detection key, indicates whether the model output verbatim a significant part of that text, and outputs that portion of the text if so.

In order to preserve the benefits of robust watermarking for applications like detecting plagiarism, our publicly attributable watermarks also retain a Detect algorithm (in addition to the AttrText algorithm) with the robustness of our standard watermarking schemes. One can choose at detection time whether one wants to use Detect for standard detection, or AttrText for attribution.

<span id="page-17-2"></span><span id="page-17-1"></span><sup>8</sup>For instance, we could choose to only hash tokens whose index has the same parity as the token being sampled.

<sup>9</sup>Note that the roles of the public and secret keys are reversed here. For PRCs, a secret key is necessary for decoding, but anyone can encode with knowledge of a public key. Public-key PRCs are useful for public-key steganography.

Our watermarking scheme with public attribution, Watt[PRC], is a natural extension of our regular watermarking scheme W[PRC]. Recall that W[PRC] embeds a codeword of a zero-bit PRC into the model's response; the detector checks whether the given text is close to a codeword. Of course, if we use a PRC that encodes an arbitrary message (rather than only '1' as in a zero-bit PRC), then W[PRC] will embed arbitrary messages in the text. Watt[PRC] does exactly this, where the message that it encodes is a signature on the response output thus far. AttrText decodes the given text to obtain this signature, and checks using the public detection key that it is a valid signature of a portion of the response. If so, this signed portion must have been generated by the model.

Concurrent work [\[FGJ](#page-63-3)+23] also constructs a watermark with public detection, although this scheme is designed to have mild robustness (comparable to that of [\[CGZ23\]](#page-62-1)) and therefore is not appropriate for attribution as-is. Their scheme can easily be modified to satisfy our definition of unforgeable public attribution, but it would then lose all robustness guarantees for standard watermarking. Our scheme simultaneously functions as a highly robust standard watermark via Detect, while also satisfying unforgeable public attribution via AttrText.

### <span id="page-18-0"></span>2.7 Robust steganography

In steganography, the goal is to send a hidden message such that an observer cannot tell that a message is being sent at all. In the classic presentation, a prisoner wishes to secretly communicate with an outside party even though the warden is filtering their letters. If the warden detects any unusual language then the communication channel will be shut down, so the prisoner cannot simply encrypt the message: The warden should not only be unable to learn anything about the message, but should be unable to even detect that secret communication is occurring at all.

Steganography was formalized in [\[HLVA02\]](#page-63-2). In this presentation, there is some underlying steganographic channel, [10](#page-18-1) a distribution with which the sender wishes to conceal a message. The sender is given sample access to this steganographic channel and sends a stegotext to the receiver. Steganographic secrecy requires that the distribution of stegotexts is indistinguishable from the steganographic channel, except to the receiver who can recover the message with a secret key.

[\[HLVA02\]](#page-63-2) proves the security of a steganography scheme of [\[AP98\]](#page-62-6) that can be constructed using any encryption scheme (Encode, Decode) with pseudorandom ciphertexts. The key idea behind this scheme is to embed each bit x<sup>i</sup> of a pseudorandom encryption of the message by drawing a sample d<sup>i</sup> from the steganographic channel such that f(di) = x<sup>i</sup> for some hash function f:

Steg.Encode(sk, m) [\[AP98,](#page-62-6) [HLVA02\]](#page-63-2):

- 1. Let x = x1|| . . . ||x<sup>n</sup> ← Encode(sk, m)
- 2. For i ∈ [n], sample a random d<sup>i</sup> from the channel conditioned on f(di) = x<sup>i</sup>
- 3. Output d = d1|| . . . ||d<sup>n</sup>

The decoder Steg.Decode simply outputs Decode(sk, f(d1)|| . . . ||f(dn)) = Decode(sk, x) = m.

If x<sup>i</sup> is uniform over {0, 1}, and f is perfectly unbiased for the channel, then d<sup>i</sup> is sampled exactly from the channel distribution. Therefore, by pseudorandomness of the ciphertext, an observer cannot distinguish stegotexts from samples from the steganographic channel. The receiver, which knows the decoding key for the encryption scheme, can evaluate f on each block of the stegotext to obtain the ciphertext, then decrypt to recover the message.

However, this scheme is very brittle. If the stegotext is corrupted with any errors at all — even ones resulting from any small bias in the hash function f — the message cannot be recovered. A natural attempt

<span id="page-18-1"></span><sup>10</sup>In the steganography literature this is usually just called a "channel"; we call it a "steganographic channel" to differentiate it from the coding-theoretic channels we use in the context of robustness.

at achieving robustness is for the sender to apply an error-correcting code (Enc, Dec) to the ciphertext before embedding it. But this loses pseudorandomness and therefore steganographic secrecy! Consequently, the robust steganography schemes of prior work rely on stronger assumptions like the ability of the sender and receiver to share state. A shared state allows the sender to generate a fresh one-time pad r for each message it sends, making the task much easier: The sender embeds x = Enc(m)⊕r by choosing d such that f(di) = x<sup>i</sup> , and the receiver computes Dec(˜x ⊕ r), where (Enc, Dec) is any error-correcting code. However, if the sender and receiver become unsynchronized (as is likely in practice), the receiver can no longer decode the message.

We observe that PRCs are exactly the primitive needed for robust stateless steganography: Using a PRC as the pseudorandom encryption scheme in the above (Steg.Encode, Steg.Decode) construction immediately gives us a steganography scheme with the same robustness as the PRC. If we use a public-key PRC, the resulting steganography scheme is also public-key. Furthermore, the robustness of the PRC allows us to relax the assumption that f is perfectly unbiased on the steganographic channel.

Our main result of Section [8](#page-58-0) is the first stateless steganography scheme with nontrivial robustness to errors. In particular, using our LDPC-based PRCs, we construct stateless steganography schemes that are robust to p-bounded channels for any constant p, or any constant-rate random deletion channel.

### <span id="page-20-0"></span>3 Preliminaries

Let N := {1, 2, . . . } denote the set of positive integers. We will write [q] := {1, . . . , q}. For a set X, we define X<sup>∗</sup> := {(x1, . . . , xk) | x1, . . . , x<sup>k</sup> ∈ X ∧ k ∈ Z≥0} to be the set of all strings with alphabet X. For a binary string s ∈ X<sup>∗</sup> , we let s<sup>i</sup> denote the i th symbol of s and len s denote the length of s. For a string s ∈ X<sup>∗</sup> and positive integers a ≤ b ≤ len s, let s[a : b] denote the substring (sa, . . . , sb).

For a finite set X, we will use the notation x ← X to denote a uniformly random sample x from X. If X is a set of n-dimensional column vectors, we will write X<sup>m</sup> to refer to the set of n × m matrices whose columns take values in X. Unless otherwise specified, vectors are assumed to be column vectors. For matrices M ∈ F m×n 2 , let ker M and Im M denote the kernel and image of M over F2, respectively.

We use log(x) to denote the logarithm base 2 of x, and ln(x) to denote the natural logarithm of x.

Let Ber(p) be the Bernoulli distribution on {0, 1} with expectation p. Let Ber(n, p) be the distribution on n-bit strings where each bit is an i.i.d sample from Ber(p).

We let ◦ denote the composition of functions, algorithms, or channels; that is, f ◦ g denotes (the function/algorithm/channel) obtained by applying g, then f.

Let λ denote the security parameter. A function f of λ is negligible if f(λ) = O( 1 poly(λ) ) for every polynomial poly(·). We write f(λ) ≤ negl(λ) to mean that f is negligible. We let ≈ denote computational indistinguishability and ≡ denote statistical indistinguishability.

<span id="page-20-3"></span>Lemma 1 (Azuma's inequality). Let Z0, . . . , Z<sup>n</sup> be a martingale with respect to X0, . . . , Xn. If the differences |Z<sup>i</sup> − Zi−1| are all bounded by C with probability 1 − ε, then for all t > 0,

$$\Pr[|Z\_n - Z\_0| > t] \le \exp\left(\frac{-t^2}{2nC^2}\right) + \varepsilon.$$

Lemma 2 (Chernoff bounds). Let X1, . . . , X<sup>n</sup> ∈ [0, 1] be independent random variables. Let µ = E [ P<sup>n</sup> <sup>i</sup>=1 X<sup>i</sup> ]. Then for any δ ∈ (0, 1):

$$\begin{aligned} \Pr\left[\sum\_{i=1}^n X\_i \ge (1+\delta)\mu\right] &\le \exp\left(-\frac{\mu\delta^2}{3}\right) \text{ and }\\ \Pr\left[\sum\_{i=1}^n X\_i \le (1-\delta)\mu\right] &\le \exp\left(-\frac{\mu\delta^2}{2}\right). \end{aligned}$$

Let Hyp(N, K, n) denote the hypergeometric distribution with a population of size N, with K success elements, and n draws. That is, a random variable X ∼ Hyp(N, K, n) is the number of success elements contained in n uniform draws from the population without replacement.

<span id="page-20-2"></span>Lemma 3 (Hypergeometric tail bounds [\[Hoe94\]](#page-63-4)). Let X ∼ Hyp(N, K, n) and p = K/N. Then for any 0 < t < K/N,

$$\Pr\left[X \le (p-t)n\right] \le e^{-2t^2n}, \text{ and}$$

$$\Pr\left[X \ge (p+t)n\right] \le e^{-2t^2n}.$$

### <span id="page-20-1"></span>3.1 Cryptography preliminaries

Pseudorandom function (PRF). Let F = {Fsk : {0, 1} <sup>ℓ</sup>1(λ) → {0, 1} ℓ2(λ) | sk ∈ {0, 1} <sup>λ</sup>} be a family of functions. F is a PRF if Fsk is efficiently computable and for all polynomial-time distinguishers D,

$$\left| \Pr\_{\mathsf{sk} \leftarrow \{0, 1\}^{\lambda}} \left[ D^{F\_{\mathsf{sk}}(\cdot)}(1^{\lambda}) = 1 \right] - \Pr\_{f} \left[ D^{f(\cdot)}(1^{\lambda}) = 1 \right] \right| \leq \mathsf{negl}(\lambda) .$$

SigForge<sup>A</sup>,Π(λ) (pk,sk) ← Gen(1<sup>λ</sup> ) (m, σ) ← ASignsk(·) (pk) Let Q denote the set of queries made by A to Signsk(·). return Vrfypk(m, σ) ∧ m ∈ Q/

Figure 1: The signature forgery experiment SigForgeA,Π(λ)

<span id="page-21-1"></span>where f denotes a random function from {0, 1} ℓ1(λ) to {0, 1} ℓ2(λ) .

Digital signature scheme. We use the definition of a digital signature from [\[KL07\]](#page-64-6), with small modifications. A digital signature scheme is defined over a message space M and consists of polynomial-time algorithms (Gen, Sign, Vrfy) such that:

- Gen : takes as input a security parameter 1<sup>λ</sup> and outputs a public-private key pair (pk,sk).
- Sign : takes as input a private key sk and a message m ∈ M. It outputs a signature σ, which we write as σ ← Signsk(m).
- Vrfy : takes as input a public key pk, a message m, and a signature σ. It outputs 1 if the signature is valid and 0 otherwise. We write b := Vrfypk(m, σ).

It is required that except with negligible over (pk,sk) output by Gen(1<sup>λ</sup> ), it holds that Vrfypk(m, Signsk(m)) = 1 for every m ∈ M.

Definition (Security of a digital signature scheme.). A digital signature scheme Π = (Gen, Sign, Vrfy) is existentially unforgeable under an adaptive chosen-message attack, or just secure, if for all polynomial-time adversaries A,

Pr[SigForge<sup>A</sup>,Π(λ) = 1] ≤ negl(λ)

where the experiment SigForge<sup>A</sup>,Π(λ) is defined in Figure [1.](#page-21-1)

### <span id="page-21-0"></span>3.2 Coding theory preliminaries

A channel is a randomized map E : Σ<sup>∗</sup> → Σ ∗ . That is, for x ∈ Σ ∗ , E(x) is a random sample from Σ<sup>∗</sup> . We use channels to model errors introduced by the environment, or by an adversary attempting to e.g. remove a watermark. Two of the most important channels we consider are the binary symmetric channel BSC and the binary deletion channel BDC:

- BSC<sup>p</sup> : {0, 1} <sup>∗</sup> → {0, 1} ∗ is the binary symmetric channel with error rate p ∈ (0, 1). That is, BSCp(x) = x ⊕ e where e ← Ber(len x, p).
- BDC<sup>q</sup> : {0, 1} <sup>∗</sup> → {0, 1} ∗ is the binary deletion channel with deletion rate q ∈ (0, 1). That is, BDCp(x) randomly deletes each bit x<sup>i</sup> independently with probability q.

For the purposes of this work, an error-correcting code with robustness to the channel E is a pair of algorithms (Enc, Dec) where Enc, Dec : Σ<sup>∗</sup> → Σ ∗ . Error-correction (or robustness) for the channel E says that if x ← Enc(m), then Dec(E(x)) = m. The block length of an error correcting code is the number of symbols in a codeword required to encode a message of a particular length. We therefore write the block length n = n(k) as a function of the message length k. The rate of a code is the function k 7→ k/n(k), which may or may not depend on the message length k.

### <span id="page-22-0"></span>4 Pseudorandom code basics

### <span id="page-22-1"></span>4.1 Definitions

In this section we define pseudorandom codes (PRCs)[11](#page-22-4) and related terminology. A PRC can be viewed as a family[12](#page-22-5) of error-correcting codes indexed by encoding and decoding keys. For secret-key PRCs, the encoding and decoding keys are identical; for public-key PRCs, the encoding key is public and the decoding key is secret.

Formally, a PRC is specified by three algorithms. A key generation function samples the keys. An encoding function takes as input the encoding key and a message, and it outputs a codeword. A decoding function takes as input the decoding key and a perturbed codeword, and it outputs the message or ⊥.

Our error correction guarantee is defined in terms of a channel. A PRC is robust to a channel E if Decode can recover m from E(Encode(m)) with overwhelming probability. In addition to requiring that we can recover messages from noisy codewords, we also require that Decode outputs ⊥ given a string that is unrelated to the code. That is, for any string c, Decode(c) outputs ⊥ with overwhelming probability over the choice of the decoding key. This property is important for applications such as watermarking, where we want the ability to distinguish codewords from uniformly random strings.

Pseudorandomness of the PRC ensures that an adversary without knowledge of the secret key cannot distinguish between an oracle for the Encode algorithm of the scheme, or an oracle that outputs independently drawn uniform strings. If a PRC is viewed as an encryption scheme, pseudorandomness is equivalent to indistinguishability from random bits against a chosen plaintext attack (IND-\$CPA security) [\[RBB03\]](#page-64-5). For public-key PRCs, pseudorandomness holds even against adversaries holding the encryption key.

<span id="page-22-2"></span>Definition 1 (Secret-key PRC). Let Σ be a fixed alphabet. A secret-key pseudorandom error-correcting code (abbreviated as secret-key PRC) with robustness to a channel E : Σ<sup>∗</sup> → Σ ∗ is a triple of polynomial-time randomized algorithms (KeyGen, Encode, Decode) satisfying

- (Syntax) There exist functions ℓ, n, k : N → N such that for all λ ∈ N, KeyGen(1<sup>λ</sup> ) ∈ {0, 1} ℓ(λ) , Encode : {1 <sup>λ</sup>} × {0, 1} <sup>ℓ</sup>(λ) × Σ <sup>k</sup>(λ) → Σ n(λ) , and Decode : {1 <sup>λ</sup>} × {0, 1} <sup>ℓ</sup>(λ) × Σ <sup>∗</sup> → Σ <sup>k</sup>(λ) ∪ {⊥}.
- (Error correction, or robustness) For any λ ∈ N and any message m ∈ Σ k(λ) ,

$$\Pr\_{\mathsf{sk}\leftarrow\mathsf{KeqGen}(1^{\lambda})}[\mathsf{Decoder}(1^{\lambda},\mathsf{sk},\mathcal{E}(x))=\mathsf{m}:x\leftarrow\mathsf{Encode}(1^{\lambda},\mathsf{sk},\mathsf{m})] \geq 1-\mathsf{negl}(\lambda).$$

• (Soundness) For any fixed c ∈ Σ ∗ ,

$$\Pr\_{\mathsf{sk}\leftarrow\mathsf{KeyGen}(1^{\lambda})}[\mathsf{Decode}(1^{\lambda},\mathsf{sk},c)=\bot] \geq 1-\mathsf{negl}(\lambda).$$

• (Pseudorandomness) For any polynomial-time adversary A,

$$\left| \Pr\_{\mathsf{sk} \leftarrow \mathsf{KeyGen}(1^{\lambda})} [\mathcal{A}^{\mathsf{Encode}(1^{\lambda}, \mathsf{sk}, \cdot)}(1^{\lambda}) = 1] - \Pr\_{\mathsf{ll}} [\mathcal{A}^{\mathsf{ll}}(1^{\lambda}) = 1] \right| \leq \mathsf{negl}(\lambda),$$

where A<sup>U</sup> means that the adversary has access to an oracle that, on any (even previously queried) input, responds with a freshly drawn uniform value in Σ<sup>n</sup>(λ) .

<span id="page-22-3"></span>Definition 2 (Public-key PRC). Let Σ be a fixed alphabet. A public-key pseudorandom error-correcting code (abbreviated as public-key PRC) with robustness to a channel E : Σ<sup>∗</sup> → Σ ∗ is a triple of polynomial-time randomized algorithms (KeyGen, Encode, Decode) satisfying

<span id="page-22-4"></span><sup>11</sup>An unrelated notion of pseudorandom codes was defined by [\[KKRT16\]](#page-64-7). Their notion does not require efficient decoding or pseudorandomness of codewords; rather, they require only that codewords are far apart.

<span id="page-22-5"></span><sup>12</sup>We remark that if a PRC were a fixed code rather than a family of codes, pseudorandomness against non-uniform adversaries would be impossible since the adversary could have the decoding key hard-coded.

- (Syntax) There exist functions ℓDec, ℓEnc, n, k : N → N such that for all λ ∈ N, KeyGen(1<sup>λ</sup> ) ∈ {0, 1} <sup>ℓ</sup>Dec(λ)×{0, 1} ℓEnc(λ) , Encode : {1 <sup>λ</sup>}×{0, 1} <sup>ℓ</sup>Enc(λ)×Σ <sup>k</sup>(λ) → Σ n(λ) , and Decode : {1 <sup>λ</sup>}×{0, 1} <sup>ℓ</sup>Dec(λ)× Σ <sup>∗</sup> → Σ <sup>k</sup>(λ) ∪ {⊥}.
- (Error correction, or robustness) For any λ ∈ N and any message m ∈ Σ k(λ) ,

$$\Pr\_{\mathsf{F}(\mathsf{sk},\mathsf{pk}) \leftarrow \mathsf{KeyGen}(1^{\lambda})}[\mathsf{Decode}(1^{\lambda},\mathsf{sk},\mathcal{E}(x)) = \mathsf{m} : x \leftarrow \mathsf{Encode}(1^{\lambda},\mathsf{pk},\mathsf{m})] \geq 1 - \mathsf{negl}(\lambda).$$

• (Soundness) For any fixed c ∈ Σ ∗ ,

$$\Pr\_{\mathsf{(sk,pk)} \leftarrow \mathsf{KeyGen}(1^{\lambda})} \left[ \mathsf{Decode}(1^{\lambda}, \mathsf{sk}, c) = \bot \right] \geq 1 - \mathsf{negl}(\lambda).$$

• (Pseudorandomness) For any polynomial-time adversary A,

$$\left| \Pr\_{\left(\mathsf{sk},\mathsf{pk}\right) \leftarrow \mathsf{KeyGen}\left(1^{\lambda}\right)} \left[ \mathcal{A}^{\mathsf{Encoder}\left(1^{\lambda},\mathsf{pk},\cdot\right)} \left(1^{\lambda},\mathsf{pk}\right) = 1 \right] - \Pr\_{\left(\mathsf{sk},\mathsf{pk}\right) \leftarrow \mathsf{KeyGen}\left(1^{\lambda}\right)} \left[ \mathcal{A}^{\mathsf{M}} \left(1^{\lambda},\mathsf{pk}\right) = 1 \right] \right| \leq \mathsf{negl}(\lambda),$$

where A<sup>U</sup> means that the adversary has access to an oracle that, on any (even previously queried) input, responds with a freshly drawn uniform value in Σ<sup>n</sup>(λ) .

The block length of a (secret-key or public-key) PRC is n(λ) and the message length is k(λ). The rate is the function λ 7→ k(λ)/n(λ). We often drop the dependence on λ when it is clear from context.

For both secret-key and public-key PRCs, if there is only one possible message (i.e. k(λ) = 0), then we say that the scheme is a zero-bit PRC.

Remark. We present our constructions of PRCs for messages of fixed lengths. That is, for a given set of keys, the construction will only work for messages of a fixed length. However, we note that this can be easily remedied using a pseudorandom function (PRF) to select new keys for every message length. We do not include the PRF in our constructions in order to simplify presentation.

### <span id="page-23-0"></span>4.2 Heuristic construction from permuted codes

In this section we describe a natural heuristic transformation for building a candidate secret-key PRC from any error-correcting code. In Section [5](#page-25-0) we will give provably secure constructions of PRCs from standard (subexponential) cryptographic assumptions.

Our heuristic construction can be applied to any binary error-correcting code, such as the polar code [\[Ari09\]](#page-62-7). The secret key will be a random permutation of the indices of the codewords. To encode a message, we encode it using the error-correcting code, then apply the secret permutation, and finally add a small amount of random Bernoulli noise.

There are two drawbacks of this generic permuted code construction relative to our pseudorandom LDPC codes:

- In general the pseudorandomness of a permuted code is based on non-standard, ad-hoc conjectures. For certain codes, such as Gallager's LDPC ensemble [\[Gal62\]](#page-63-5), the permuted code construction is not pseudorandom.
- Permuted codes are inherently secret-key PRCs, whereas our pseudorandom LDPC codes are publickey.

For any error-correcting code (Enc, Dec) and parameter η > 0, we formally define the corresponding permuted code Permuted-PRCη[Enc, Dec] as follows. Let n = n(·) be the block length for (Enc, Dec), as a function of the message length. (Recall that the block length is the number of codeword symbols needed to encode a given message.) Permuted-PRCη[Enc, Dec] will encode messages of length k into codewords of length n = n(k + λ), where λ is a security parameter.

Construction 1 (Permuted-PRCη[Enc, Dec]).

- Let λ be a security parameter, let k be the length of messages we wish to encode, and let n = n(k +λ).
- KeyGen(1<sup>λ</sup> ): Sample a random permutation π : [n] → [n] and output sk = π.
- Encode(sk, m) for m ∈ Σ k :
	- 1. Sample a random string r ← Σ <sup>λ</sup> and a noise vector e ← Ber(n, η).
	- 2. Compute c = Enc(r||m) ⊕ e.
	- 3. Output (cπ(1)|| · · · ||cπ(n)).
- Decode(sk, x) for x ∈ Σ n:
	- 1. Compute c = (xπ−1(1)|| · · · ||xπ−1(n)).
	- 2. Compute m′ = Dec(c).
	- 3. Output the last k symbols of m′ .

A permuted code has the same robustness to substitutions, and nearly the same rate, as (Enc, Dec).

A natural choice of error-correcting codes to use in this permuted code construction is polar codes [\[Ari09\]](#page-62-7). Since polar codes have linear rate and tolerate a constant rate of adversarial errors, permuted polar codes are a candidate linear-rate secret-key PRC with robustness to a constant rate of adversarial errors. We do not know whether such codes satisfy pseudorandomness.

# <span id="page-25-0"></span>5 Constructing pseudorandom codes from cryptographic assumptions

In this section, we introduce a public-key PRC based on LDPC codes. We present the zero-bit version of our scheme, LDPC-PRC0, in Section [5.1;](#page-25-1) we will see in Section [6](#page-37-0) that this immediately implies a many-bit scheme with essentially the same robustness. In Section [5.2](#page-26-0) we show that LDPC-PRC<sup>0</sup> is robust to every error channel of bounded weight, as long as the parity checks have sufficiently low weight. Finally, we prove pseudorandomness of LDPC-PRC<sup>0</sup> in two different parameter regimes under different cryptographic assumptions: In Section [5.3,](#page-28-0) we prove pseudorandomness under LPN and a certain planted XOR assumption; in Section [5.4,](#page-30-0) we prove pseudorandomness under a subexponential-query variant of LPN.

### <span id="page-25-1"></span>5.1 The zero-bit construction

Let

$$\mathcal{S}\_{t,n} = \{ s \in \mathbb{F}\_2^n : \text{wt}(s) = t \}.$$

be the set of all t-sparse vectors in F n 2 , and

$$\mathcal{S}\_{t,r,n} = \{ P \in \mathbb{F}\_2^{r \times n} : \text{wt}(P\_{i,:}) = t \,\,\forall i \in [r] \}$$

be the set of all t-row-sparse matrices in F r×n 2 .

Our zero-bit pseudorandom LDPC codes are parameterized by a public generator matrix G ∈ F n×g 2 and a secret parity-check matrix P ∈ F r×n 2 . The sampling process for these matrices is described in Definition [3.](#page-25-2)

<span id="page-25-2"></span>Definition 3 (Random LDPC code, LDPC[n, g, t, r]). For n, g, t, r ∈ N, define the distribution LDPC[n, g, t, r] over F r×n <sup>2</sup> <sup>×</sup> <sup>F</sup> n×g 2 as follows:

- LDPC[n, g, t, r]:
- 1. Sample P ← St,r,n, i.e. P ∈ F r×n 2 is chosen to have i.i.d random t-sparse rows.
- 2. Sample G ← (ker P) g , i.e. G ∈ F n×g 2 is a random matrix subject to P G = 0.
- 3. Output (P, G).

An (n, g, t, r) random LDPC code is a pair of matrices (P, G) ← LDPC[n, g, t, r].

The focus of this section will be on the following zero-bit PRC. Recall that a zero-bit PRC is one whose message space is just {1}. We will see in Section [6.2](#page-39-0) that a constant-rate PRC can be generically constructed from any zero-bit PRC.

<span id="page-25-3"></span>Construction 2 (Zero-bit public-key pseudorandom LDPC code, LDPC-PRC0[n, g, t, r, η, ζ]). Let n, g, t, r : N → N and η, ζ : N → [0, 1/2) be efficiently-computable functions of the security parameter. We define LDPC-PRC0[n, g, t, r, η, ζ] by the following algorithms, where we leave the dependence of n, g, t, r, η, ζ on λ implicit:

- KeyGen(1<sup>λ</sup> ): Sample (P, G) ← LDPC[n, g, t, r] and z ← F n 2 . Output (sk = (P, z), pk = (G, z)).
- Encode(1<sup>λ</sup> ,(G, z)): Sample u ← F g 2 , e ← Ber(n, η). Output Gu ⊕ z ⊕ e.
- Decode(1<sup>λ</sup> ,(P, z), x): If wt(P x ⊕ P z) < 1 <sup>2</sup> − ζ · r, output 1; otherwise output ⊥.

For the remainder of this section, we will identify the security parameter λ with the dimension of the code n. We will therefore write g, t, r, η, ζ as functions of n, with the understanding that n(λ) = λ.

### <span id="page-26-0"></span>5.2 Codeword detection (zero-bit decoding)

We say that a length-preserving binary channel E : {0, 1} <sup>∗</sup> → {0, 1} ∗ is p-bounded if there exists a negligible function negl(·) such that for all n ∈ N, Prx←{0,1}<sup>n</sup> [wt(E(x) ⊕ x) > pn] ≤ negl(n).

<span id="page-26-1"></span>Lemma 4. For any p, η ∈ [0, 1/2) and ε ∈ (0, 1), there exits δ > 0 such that the following holds. For any t ≤ δ log n, g > 0, and n <sup>ε</sup> ≤ r ≤ 0.99n, LDPC-PRC0[n, g, t, r, η, r−1/<sup>4</sup> ] is robust to every p-bounded channel.

Proof. Lemma [6](#page-27-0) shows that any fixed string c ∈ F n <sup>2</sup> decodes to ⊥ with probability 1 − negl(n). It remains to show that codewords subject to any p-bounded channel decode to 1.

Let E be any p-bounded channel. We need to show that wt(P x ⊕ P z) < 1 <sup>2</sup> − r −1/4 r with probability 1 − negl(n) over (P, G) ← LDPC[n, g, t, r], u ← F g 2 , z ← F n 2 , e ← Ber(n, η), x ← E(Gu ⊕ z ⊕ e).

We will show that there exists a constant α ∈ (0, 1/2) such that wt(Gu⊕z ⊕x) ≤ 1 <sup>2</sup> − α n with probability 1 − negl(n). Then we can apply Lemma [5](#page-26-2) with y = Gu ⊕ z ⊕ x to see that wt(P y) = wt(P x ⊕ P z) < 1 <sup>2</sup> − r −1/4 r with probability 1 − negl(n) for appropriate choices of t, r.

Let c = Gu ⊕ z ⊕ e. Then

$$\begin{aligned} y &= Gu \oplus z \oplus x \\ &= Gu \oplus z \oplus \mathcal{E}(Gu \oplus z \oplus e) \\ &= e \oplus c \oplus \mathcal{E}(c), \end{aligned}$$

where c is uniformly distributed because of z. Let e ′ = c⊕ E(c), so that y = e⊕e ′ . Then since e ← Ber(n, η) is independent from e ′ , we have

$$\begin{aligned} \mathbb{E}[\text{wt}(y)] &= \mathbb{E}[\text{wt}(e \oplus e')] \\ &= (1 - \eta)\, \mathbb{E}[\text{wt}(e')] + \eta \, \mathbb{E}[n - \text{wt}(e')] \\ &\leq (1 - \eta)pn + \eta(1 - p)n + \text{negl}(n) \end{aligned}$$

where the inequality holds because E is p-bounded, so wt(e ′ ) ≤ pn with probability 1−negl(n). Conditioned on wt(e ′ ) ≤ pn, a Chernoff bound over the random choice of e implies that

$$\text{wt}(e \oplus e') \le \left[ \frac{(1 - \eta)p + \eta(1 - p)}{2} + \frac{1}{4} \right] \cdot n$$

with probability 1 − negl(n). Therefore we apply Lemma [5](#page-26-2) with α = h (1−η)p+η(1−p) <sup>2</sup> + 1 4 i .

<span id="page-26-2"></span>Lemma 5. Let α ∈ (0, 1/2) be some constant and suppose that r = n Ω(1) and t ≤ 1 5 log1/2<sup>α</sup> r. If y ∈ F n 2 satisfies wt(y) ≤ 1 <sup>2</sup> − α n, then

$$\Pr\_{P \leftarrow \mathcal{S}\_{t,r,n}} \left[ \text{wt}(Py) < \left( \frac{1}{2} - r^{-1/4} \right) r \right] \ge 1 - \text{negl}(n).$$

Proof. Let P<sup>i</sup> denote the i th row of P. We will show that

<span id="page-26-3"></span>
$$\Pr\_{P\_i \leftarrow \mathcal{S}\_{t,1,n}} \left[ P\_i y = 0 \right] \geq \frac{1}{2} + \frac{2}{r^{1/4}},\tag{1}$$

and the independence of the rows of P will imply the lemma by a Chernoff bound.

Let j1, . . . , j<sup>t</sup> ∈ [n], Y1, . . . , Y<sup>t</sup> ∈ {−1, 1} be random variables, defined as follows, for ℓ = 1, . . . , t:

1. Sample j<sup>ℓ</sup> ← [n] \ {j1, . . . , jℓ−1}.

2. Let Y<sup>ℓ</sup> = (−1)xjℓ .

Then the bit Piy is distributed as (1 − Y<sup>1</sup> · · · Yt)/2, so

$$\Pr\_{P\_i \leftarrow \mathcal{S}\_{t,1,n}}[P\_i y = 0] = \Pr[Y\_1 \cdots Y\_t = 1]$$

$$= \frac{1}{2} + \frac{1}{2} \mathbb{E}[Y\_1 \cdots Y\_t].$$

The remainder of the proof is devoted to showing that

<span id="page-27-1"></span>
$$\mathbb{E}[Y\_1 \cdots Y\_t] \ge (2\alpha)^t - 2t^2/n. \tag{2}$$

For large enough n, this will imply Equation [\(1\)](#page-26-3) by the assumption that t ≤ 1 5 log1/2<sup>α</sup> r.

Let α ′ = 1/2 − wt(y)/n, and note that α ′ ≥ α. To prove Equation [\(2\)](#page-27-1) we first show that for all m ∈ [t],

<span id="page-27-3"></span>
$$|\mathbb{E}[Y\_1 \cdots Y\_m] - 2\alpha' \mathbb{E}[Y\_1 \cdots Y\_{m-1}]| \le 2t/n. \tag{3}$$

By the tower property and linearity of expectation,

<span id="page-27-2"></span>
$$\left| \mathbb{E} [Y\_1 \cdots Y\_m] - 2\alpha' \mathbb{E} [Y\_1 \cdots Y\_{m-1}] \right| = \left| \mathbb{E} \left[ Y\_1 \cdots Y\_{m-1} \cdot \left( \mathbb{E} [Y\_m \mid Y\_{$$

For all possible assignments of Y<m,

$$\begin{aligned} \mathbb{E}[Y\_m \mid Y\_{$$

Recall that j<sup>m</sup> is chosen to be a uniformly random index from [n] \ {j<m}. Since m ≤ t, [n] \ {j<m} contains at least ( <sup>1</sup> <sup>2</sup> + α ′ )n − t and at most ( <sup>1</sup> <sup>2</sup> + α ′ )n indices for which the corresponding bit of y is 0. Therefore, 1 <sup>2</sup> + α ′ − t/n ≤ Pr<sup>j</sup>m[x<sup>j</sup><sup>m</sup> = 0 | Y<m] ≤ 1 <sup>2</sup> + α ′ + t/n.

We now have that |E[Y<sup>m</sup> | Y<m] − 2α ′ | ≤ 2t/n, and |Y<sup>1</sup> · · · Ym−1| = 1. Plugging these two facts into Equation [\(4\)](#page-27-2) gives us Equation [\(3\)](#page-27-3).

We complete the proof by showing by induction that E[Y<sup>1</sup> · · · Ym] ≥ (2α ′ ) <sup>m</sup> − 2mt/n. Observe first that E[Y1] = ( <sup>1</sup> <sup>2</sup> + α ′ ) − ( 1 <sup>2</sup> − α ′ ) > 2α ′ − 2t/n. Assume that the inequality holds for some m < t; we'll show that it holds for m + 1. We have E[Y<sup>1</sup> · · · Y<sup>m</sup>+1] ≥ 2α ′ E[Y<sup>1</sup> · · · Ym] − 2t/n. Therefore, since 2α ′ ≤ 1,

$$\begin{aligned} \mathbb{E}[Y\_1 \cdots Y\_{m+1}] &\geq 2\alpha' \left( (2\alpha')^m - \frac{2mt}{n} \right) - \frac{2t}{n} \\ &= (2\alpha')^{m+1} - \frac{2(m+1)t}{n} \end{aligned}$$

as desired.

<span id="page-27-0"></span>Lemma 6. If n Ω(1) ≤ r ≤ 0.99n, then for any fixed c ∈ F n 2 ,

$$\Pr\_{\begin{subarray}{c}P\leftarrow\mathcal{S}\_{t,r,n} \\ z\leftarrow\mathbb{F}\_{2}^{n}\end{subarray}}\left[\operatorname{wt}(Pc\oplus Pz)\geq\left(\frac{1}{2}-r^{-1/4}\right)r\right]\geq 1-\mathsf{negl}(n).$$

Proof. With probability 1 − negl(n), P ← St,r,n is full rank by Lemma [12](#page-33-0) (invoking the lemma with g = 0). For any such P, over the random choice of z ← F n 2 , the vector P(c ⊕ z) ∈ F r 2 is uniformly random. The lemma follows from a Chernoff bound.

### <span id="page-28-0"></span>5.3 Pseudorandomness from the planted XOR assumption and LPN

In this subsection we prove that the generator matrix (public key) of LDPC-PRC<sup>0</sup> is pseudorandom under the planted XOR assumption. This is Lemma [8.](#page-29-0) The number of columns of the generator matrix and the number of rows of the parity check matrix will depend on the particular planted XOR assumption one is willing to make. Then, since the generator matrix is pseudorandom, pseudorandomness of LDPC-PRC<sup>0</sup> (Theorem [1\)](#page-30-1) follows directly from the standard LPN assumption.

Cryptographic assumptions. The existence of our LDPC-based PRCs relies on either of two assumptions. We state the two assumptions together as Assumption [1.](#page-28-1)

<span id="page-28-1"></span>Assumption 1. At least one of the following two statements is true:

- There exists a constant η ∈ (0, 1/2) such that, for any function g(n) = Ω(log<sup>2</sup> n), the LPNg,η assumption (Assumption [2\)](#page-28-3) holds.
- There exist constants η ∈ (0, 1/2) and ε ∈ (0, 1) such that, for any function t(n) = Θ(log n), both the LPNnε,η assumption (Assumption [2\)](#page-28-3) and the XOR2nε,t assumption (Assumption [3\)](#page-28-2) hold.

We now define the LPNg,η and XORm,t assumptions. Let us first recall the LPN assumption. We only state the decisional, constant-noise version, since all of our results pertain to that variant. For η ∈ (0, 1/2) and g : N → N, the LPNg,η problem is to distinguish between (A, As ⊕ e) and (A, u), where A ← F n×g(n) 2 , s ← F g(n) 2 , e ← Ber(n, η), and u ← F n 2 .

<span id="page-28-3"></span>Assumption 2 (LPN assumption). For η ∈ (0, 1/2) and g : N → N, the LPNg,η assumption states that for every n ∈ N and every polynomial-time adversary A,

$$\left| \Pr\_{\begin{subarray}{c} A \leftarrow \mathbb{F}\_2^{n \times g(n)} \\ s \leftarrow \mathbb{F}\_2^{g(n)} \\ e \leftarrow \mathbb{F}\_2^{g(n)} \\ e \leftarrow \text{Ber}(n, \eta) \end{subarray}} [\mathcal{A}(A, As \oplus e) = 1] - \Pr\_{\begin{subarray}{c} A \leftarrow \mathbb{F}\_2^{n \times g(n)} \\ u \leftarrow \mathbb{F}\_2^n \end{subarray}} [\mathcal{A}(A, u) = 1] \right| \leq \mathsf{negl}(n).$$

By a standard hybrid argument, the LPNg,η assumption implies that any polynomial number of samples of the form (A, As ⊕ e) are indistinguishable from uniformly random samples.

The planted XOR assumption is lesser-known than LPN, but there is still precedent [\[ASS](#page-62-4)<sup>+</sup>23]. This assumption states that a random linear subspace over F<sup>2</sup> is indistinguishable from one containing a planted sparse vector. Formally, it says that the distributions D0(n, m) and D1(n, m, t) are computationally indistinguishable, where the "null" distribution D<sup>0</sup> is the uniform distribution over F n×m 2 , and the "planted" distribution D<sup>1</sup> is defined as follows.

D1(n, m, t):

- 1. Sample s ← St,n.
- 2. Sample a random matrix G ∈ F n×m 2 subject to s <sup>T</sup> G = 0.
- 3. Output G.

<span id="page-28-2"></span>Assumption 3 (Planted XOR assumption). For m, t : N → N, the XORm,t assumption states that for every n ∈ N and every polynomial-time adversary A,

$$\left| \Pr\_{G \leftarrow \mathcal{D}\_0(n, m(n))} [\mathcal{A}(G) = 1] - \Pr\_{G \leftarrow \mathcal{D}\_1(n, m(n), t(n))} [\mathcal{A}(G) = 1] \right| \le \mathsf{negl}(n).$$

Remark. A previous version of this paper made use of the planted XOR assumption with m = Ω(n). However, an anonymous CRYPTO 2024 reviewer pointed out to us that this assumption is false by Theorem 4.26 of [\[ASS](#page-62-4)+23]. All of our results are therefore updated in this version of the paper to use m = n Ω(1); none of our results significantly change with the new choice of parameters. See Theorem [1](#page-30-1) for the updated theorem statement. Note also that Theorem [2](#page-36-0) is not affected, as it does not make use of the planted XOR assumption.

Note that when m = n − O(log n), the XORm,t assumption is false because there will be only n <sup>O</sup>(1) vectors v ∈ F n 2 such that v <sup>T</sup> G = 0, and one can therefore brute force search for the planted relation s. On the other hand, Claim [7](#page-29-1) shows that when (for instance) t ∼ log n and m ∼ log<sup>2</sup> n the XORm,t assumption holds against even unbounded adversaries. This claim follows from Theorem 4.2 of [\[ASS](#page-62-4)+23].

<span id="page-29-1"></span>Claim 7. If t = O(log n) and m ≤ (1 − Ω(1))tlog n, then

$$SD(\mathcal{D}\_0(n,m), \mathcal{D}\_1(n,m,t)) = n^{-\Omega(t)}.$$

For larger values of m, D0(n, m) and D1(n, m, t) are no longer statistically close, but the planted XOR assumption says that they remain computationally indistinguishable.

<span id="page-29-0"></span>Lemma 8. Let m, t, r : N → N be such that m(n) + r(n) ≤ n − ω(log n). The XORm+r,t assumption (Assumption [3\)](#page-28-2) implies that the marginal distribution on G for (P, G) ← LDPC[n, m, t, r] is pseudorandom.

Proof. The proof closely mirrors that in the technical overview (Section [2.1\)](#page-9-1), with the main difference being that here we deal with generator matrices instead of the linear subspaces themselves. For i ∈ {0, . . . , r − 1} and m′ ∈ [m + r], let Di(n, m′ , t) be defined as follows.

- Di(n, m′ , t):
- 1. Sample s1, . . . , s<sup>i</sup> ← St,n.
- 2. Sample a random matrix G ∈ F n×m′ 2 subject to s T <sup>j</sup> G = 0 for all j ∈ [i].
- 3. Output G.

Observe that D0(n, m′ , t) = D0(n, m′ ), and D1(n, m′ , t) is consistent with the definition given earlier.

For each i ∈ {0, . . . , r − 1} and m′ ∈ [m + r], since m′ ≤ m + r ≤ n − ω(log n), the matrix G ← Di(n, m′ , t) has full rank with probability 1 − negl(n). Therefore, Di(n, m′ , t) is negl(n)-close in statistical distance to the following distribution:

- Dˆ <sup>i</sup>(n, m′ , t):
- 1. Sample s1, . . . , s<sup>i</sup> ← St,n.
- 2. Sample a random full-rank matrix G ∈ F n×m′ 2 subject to s T <sup>j</sup> G = 0 for all j ∈ [i].
- 3. Output G.

Since Dˆ <sup>0</sup>(n, m+r, t) (resp. Dˆ <sup>1</sup>(n, m+r, t)) is negl(n)-close to D0(n, m+r) (resp. D1(n, m+r, t)) in statistical distance, the (n, m + r, t) planted XOR assumption implies that Dˆ <sup>0</sup>(n, m + r, t), and Dˆ <sup>1</sup>(n, m + r, t) are computationally indistinguishable.

Now suppose that an efficient adversary A distinguishes between Dˆ <sup>0</sup>(n, m, t) and Dˆ <sup>r</sup>(n, m, t) with advantage ε > 0. By a telescoping argument, A must distinguish between Dˆ <sup>i</sup>(n, m, t) and Dˆ <sup>i</sup>+1(n, m, t) with advantage ε/r, for some i ∈ {0, . . . , r − 1}. For each i ∈ {0, . . . , r − 1}, the following efficient reduction Red<sup>i</sup> satisfies Redi(Dˆ <sup>0</sup>(n, m + r, t)) ≡ Dˆ <sup>i</sup>(n, m, t) and Redi(Dˆ <sup>1</sup>(n, m + r, t)) ≡ Dˆ <sup>i</sup>+1(n, m, t). Therefore, the (n, m + r, t) planted XOR assumption implies that ε/r = negl(n), which will complete the proof.

$$\operatorname{Red}\_i(W);$$

- 1. Sample i random t-sparse vectors s1, . . . , s<sup>i</sup> ∈ F n <sup>2</sup> and let S = {v ∈ F n 2 : v · s<sup>j</sup> = 0 ∀j ∈ [i]}.
- 2. Let U = Im(W) ∩ S. Since i < r and dim Im W = m + r, we have dim U > m.
- 3. Sample a random full-rank matrix G ∈ F n×m 2 such that Im(G) ⊆ U.
- 4. Output G.

It remains to see why Redi(Dˆ <sup>0</sup>(n, m + r, t)) ≡ Dˆ <sup>i</sup>(n, m, t) and Redi(Dˆ <sup>1</sup>(n, m + r, t)) ≡ Dˆ <sup>i</sup>+1(n, m, t). In fact both of these statements are true even for fixed planted relations.

Proof that Redi(Dˆ <sup>0</sup>(n, m+r, t)) ≡ Dˆ <sup>i</sup>(n, m, t). Suppose that W ← Dˆ <sup>0</sup>(n, m+r, t). Fix s1, . . . , s<sup>i</sup> sampled in Redi(W) and let S = {v ∈ F n 2 : v·s<sup>j</sup> = 0 ∀j ∈ [i]}. For any d ∈ {m+1, . . . , m+r}, consider the distribution of the subspace U = Im(W)∩S conditioned on the event that dim U = d. Before the conditioning Im W was a random subspace of F n 2 , so after the conditioning U is a random d-dimensional subspace of S. The output of Redi(W) is a random full-rank matrix G ∈ F n×m 2 such that Im(G) ⊆ U ⊆ S. But we have just seen that U is a uniformly random d > m dimensional subspace of S, so it follows that G is a random matrix subject to Im G ⊆ S — i.e., s T <sup>j</sup> G = 0 for all j ∈ [i].

Proof that Redi(Dˆ <sup>1</sup>(n, m + r, t)) ≡ Dˆ <sup>i</sup>+1(n, m, t). Suppose that W ← Dˆ <sup>1</sup>(n, m + r, t) is sampled with the planted relation s. Fix s and s1, . . . , s<sup>i</sup> sampled in Red<sup>i</sup> . Let S = {v ∈ F n 2 : v · s<sup>j</sup> = 0 ∀j ∈ [i]} and S ′ = {v ∈ F n 2 : v · s = 0}. Again, for each d ∈ {m+ 1, . . . , m+r}, consider the distribution of U = Im(W)∩S conditioned on the event that dim U = d. Before the conditioning Im W was a random subspace of S ′ , so after the conditioning U is a random d-dimensional subspace of S ∩ S ′ . The output of Redi(W) is a random full-rank matrix G ∈ F n×m 2 such that Im(G) ⊆ U ⊆ S ∩ S ′ . But we have just seen that U is a uniformly random d > m dimensional subspace of S ∩ S ′ , so it follows that G is a random matrix subject to Im G ⊆ S ∩ S ′ — i.e., s <sup>T</sup> G = 0 and s T <sup>j</sup> G = 0 for all j ∈ [i].

Claim [7](#page-29-1) and Lemma [8](#page-29-0) together imply that the generator matrix from LDPC[n, log<sup>2</sup> n, 4 log n, log<sup>2</sup> n] is statistically uniform. In Lemma [9](#page-31-0) we improve this to show that the generator matrix from LDPC[n, g, 4 log n, r] is statistically uniform for any r ≤ 0.99n (and some g = Ω(log<sup>2</sup> n)); this forms the basis of our PRC construction based only on LPN (Theorem [2\)](#page-36-0).

<span id="page-30-1"></span>Theorem 1. For any constants p, η ∈ (0, 1/2) and ε ∈ (0, 1), there exists a function t = Θ(log n) such that LDPC-PRC0[n, n<sup>ε</sup> , t, n<sup>ε</sup> , η, n<sup>−</sup>ε/<sup>4</sup> ] is a zero-bit public-key PRC (Definition [2\)](#page-22-3) that is robust to every pbounded channel, where pseudorandomness rests on the LPNnε,η assumption (Assumption [2\)](#page-28-3) and the XOR2nε,t assumption (Assumption [3\)](#page-28-2).

Proof. By Lemma [4,](#page-26-1) there exists t = Θ(log n) such that LDPC-PRC0[n, n<sup>ε</sup> , t, n<sup>ε</sup> , η, n<sup>−</sup>ε/<sup>4</sup> ] is robust to every p-bounded channel.

By Lemma [8,](#page-29-0) the XOR2nε,t assumption implies that for (P, G) ← LDPC[n, n<sup>ε</sup> , t, n<sup>ε</sup> ], the marginal distribution on G is pseudorandom. By the LPNnε,η assumption, it follows that LDPC-PRC0[n, n<sup>ε</sup> , t, n<sup>ε</sup> , η, n<sup>−</sup>ε/<sup>4</sup> ] is a public-key PRC.

### <span id="page-30-0"></span>5.4 Pseudorandomness from subexponential LPN

In Section [5.3,](#page-28-0) we showed that the generator matrix G ∈ F n×g 2 of LDPC-PRC<sup>0</sup> was pseudorandom under the planted XOR assumption. In Lemma [9](#page-31-0) of this section, we will show that G is statistically random if we set g to be sufficiently small. Therefore, the planted XOR assumption is no longer necessary; however, the number of columns will be only g = O(log<sup>2</sup> n), so we must rely on a stronger, sub-exponential variant of LPN than in Section [5.3.](#page-28-0)

Remark. Before we see Lemma [9,](#page-31-0) note that we use a different proof strategy here than the technical overview. The reason we use this more involved proof here is that the proof outlined in the technical overview results in a different ensemble of parity-check matrices P with a triangular restriction and non-independent rows. By proving Lemma [9,](#page-31-0) we are able to use the same ensemble as in Section [5.3](#page-28-0) — that is, the rows of P are still independent and uniform t-sparse vectors.

<span id="page-31-0"></span>Lemma 9. If r ≤ 0.99n and ω( √ log n) ≤ t ≤ O(log n), then there is a g = Ω(t 2 ) such that the marginal distribution on G for (P, G) ← LDPC[n, g, t, r] is negl(n)-close to uniform in statistical distance.

Proof. Recall the definitions of St,n and St,r,n from Section [5.1.](#page-25-1) Let D be the marginal distribution on G ∈ F n×g 2 for (P, G) ← LDPC[n, g, t, r].

We will show that D is negl(n)-close to the uniform distribution in statistical distance. For any G<sup>∗</sup> ∈ F n×g 2 ,

$$\begin{split} \Pr\_{G \leftarrow \mathcal{D}}[G = G^\*] &= \sum\_{\substack{P^\* \in \mathcal{S}\_{t,r,n} \\ P^\*G^\* = 0}} \Pr\_{P \leftarrow \mathcal{S}\_{t,r,n}}[P = P^\*] \cdot \Pr\_{G \leftarrow (\ker P^\*)^g}[G = G^\*] \\ &= \frac{1}{\binom{n}{t}^r} \sum\_{\substack{P^\* \in \mathcal{S}\_{t,r,n} \\ P^\*G^\* = 0}} \frac{1}{|\ker P^\*|^g} \\ &\leq \frac{1}{\binom{n}{t}^r} \sum\_{\substack{P^\* \in \mathcal{S}\_{t,r,n} \\ P^\*G^\* = 0}} \frac{1}{2^{(n-r)m}} \\ &= \frac{\eta(G^\*)^r}{\binom{n}{t}^r \cdot 2^{(n-r)m}} \end{split}$$

where η(G<sup>∗</sup> ) is the number of collections of t rows of G<sup>∗</sup> that sum to 0. Since valid rows of P ∗ correspond to collections of t rows of G<sup>∗</sup> that sum to 0, |{P <sup>∗</sup> ∈ F r×n 2 : P <sup>∗</sup>G<sup>∗</sup> = 0}| = η(G<sup>∗</sup> ) r , which gives us the last equality above.

Let F ⊂ F r×n <sup>2</sup> be the set of t-row-sparse matrices of full rank,

$$\mathcal{F} := \{ P \in \mathcal{S}\_{t,r,n} \mid \text{rank}(P) = r \} = \{ P \in \mathcal{S}\_{t,r,n} \mid \dim \ker(P) = n - r \}.$$

Then we also have

$$\begin{split} \Pr\_{G \leftarrow \mathcal{D}}[G = G^\*] &= \frac{1}{\binom{n}{t}^r} \sum\_{P^\* \in \mathcal{S}\_{t, r, n}} \frac{1}{|\ker P^\*|^g} \\ &\geq \frac{1}{\binom{n}{t}^r} \sum\_{P^\* \in \mathcal{F} \colon \\ &\qquad P^\* G^\* = 0 \end{split}$$

$$\begin{split} &= \frac{\eta(G^\*)^r}{\binom{n}{t}^r \cdot 2^{(n-r)g}} \cdot \Pr\_{P^\* \leftarrow \mathbb{F}\_2^{r \times n}}[P^\* \text{ has full rank } |P^\* G^\* = 0]. \end{split}$$

Let P(G<sup>∗</sup> ) = {P <sup>∗</sup> ∈ St,r,n | P <sup>∗</sup>G<sup>∗</sup> = 0}. The above two inequalities give us a point-wise approximation to the density of D,

<span id="page-31-1"></span>
$$\Pr\_{P^\* \leftarrow \mathcal{P}(G^\*)}[P^\* \text{ has full rank}] \cdot \frac{\eta(G^\*)^r}{\binom{n}{t}^r \cdot 2^{(n-r)g}} \le \Pr\_{G \leftarrow \mathcal{D}}[G = G^\*] \le \frac{\eta(G^\*)^r}{\binom{n}{t}^r \cdot 2^{(n-r)g}}.\tag{5}$$

We complete the proof with the following three facts:

• Lemma [10](#page-32-0) is a general statistical fact, which implies that if

$$\Pr\_{G^\* \leftarrow \mathbb{F}\_2^{n \times g}} \left[ \left| \Pr\_{G \leftarrow \mathcal{D}} [G = G^\*] - \frac{1}{2^{ng}} \right| \le \frac{\mathsf{negl}(n)}{2^{ng}} \right] \ge 1 - \mathsf{negl}(n),$$

then D is negl(n)-close to uniform in statistical distance. Crucially, Lemma [10](#page-32-0) and Equation [\(5\)](#page-31-1) reduce the problem to reasoning about the uniform distribution over G<sup>∗</sup> , rather than D.

• Lemma [11](#page-32-1) implies that

$$\Pr\_{G^\* \leftarrow \mathbb{P}\_2^{n \times g}} \left[ \left| \frac{\eta(G^\*)^r}{\binom{n}{t}^r \cdot 2^{(n-r)g}} - \frac{1}{2^{ng}} \right| \le \frac{\mathsf{negl}(n)}{2^{ng}} \right] \ge 1 - \mathsf{negl}(n).$$

The proof is a simple invocation of Chebyshev's inequality.

• Lemma [12](#page-33-0) implies that

$$\Pr\_{G^\* \leftarrow \mathbb{F}\_2^{n \times g}} \left[ \Pr\_{P^\* \leftarrow \mathcal{P}(G^\*)} [P^\* \text{ has full rank}] \ge 1 - \mathsf{negl}(n) \right] \ge 1 - \mathsf{negl}(n).$$

Using Lemmas [11](#page-32-1) and [12](#page-33-0) with Equation [\(5\)](#page-31-1), the condition of Lemma [10](#page-32-0) is satisfied. This completes the proof of the theorem.

<span id="page-32-0"></span>Lemma 10. Let p be a probability distribution on a finite set X . If

$$\Pr\_{x \leftarrow \mathcal{X}} \left[ \left| p(x) - \frac{1}{|\mathcal{X}|} \right| > \frac{\alpha}{|\mathcal{X}|} \right] \leq \beta, 1$$

then the statistical distance between p and the uniform distribution is at most α + β.

Proof. We just compute

$$\begin{aligned} &\sum\_{\substack{x\in\mathcal{X}:\\p(x)<\lfloor\frac{1}{|X|}\rfloor}} \left(\frac{1}{|X|} - p(x)\right) \\ &=\sum\_{\substack{x\in\mathcal{X}:\\\frac{1-\alpha}{|X|}\le p(x)<\lfloor\frac{1}{|X|}\rfloor}} \left(\frac{1}{|X|} - p(x)\right) + \sum\_{p(x)<\frac{1-\alpha}{|X|}} \left(\frac{1}{|X|} - p(x)\right) \\ &\le \alpha + \sum\_{\substack{p(x)<\frac{1-\alpha}{|X|}\\p(x)<\frac{1-\alpha}{|X|}}} \frac{1}{|X|} \\ &\le \alpha + \beta. \end{aligned}$$

<span id="page-32-1"></span>Lemma 11. For any ε > 0,

$$\Pr\_{G^\* \leftarrow \mathbb{F}\_2^{n \times g}} \left[ \left| \eta(G^\*) - \binom{n}{t} \cdot 2^{-g} \right| > \varepsilon \cdot \binom{n}{t} \cdot 2^{-g} \right] \leq \frac{2^g}{\binom{n}{t} \cdot \varepsilon^2}.$$

Proof. By linearity of expectation,

$$\mathop{\mathbb{E}}\_{G^\* \leftarrow \mathbb{F}\_2^{n \times g}} \eta(G^\*) = \sum\_{w \in \mathcal{S}\_{t,n}} \Pr\_{G^\* \leftarrow \mathbb{F}\_2^{n \times g}} [w^T G^\* = 0] = \binom{n}{t} \cdot 2^{-g} \cdot 1$$

Furthermore, {1[w <sup>T</sup> G<sup>∗</sup> = 0]}w∈St,n are pairwise independent random variables over G<sup>∗</sup> ← F n×g 2 , so the lemma follows from Chebyshev's inequality.

<span id="page-33-0"></span>Lemma 12. If r ≤ 0.99n and ω( √ log n) ≤ t ≤ O(log n), then there is a g˜ = Ω(t 2 ) such that for all g ≤ g˜, Pr G∗←F n×g Pr P <sup>∗</sup>←P(G∗) [P <sup>∗</sup> has full rank] ≥ 1 − negl(n) ≥ 1 − negl(n).

Proof. We say that a subset of rows S ⊆ [r] of P ∗ forms a "simple dependency" if those rows sum to 0, and no subset of them sums to 0. For a 1 − negl(n) fraction of G<sup>∗</sup> ← F n×g 2 , we will show that over P <sup>∗</sup> ← P(G<sup>∗</sup> ) the expected number of simple dependencies in P ∗ is negl(n).

Letting W<sup>i</sup> denote the ith row of the matrix W, we define

2

$$\mathsf{SD}\_{\ell} = \left\{ W \in \mathcal{S}\_{t,\ell,n} \; \middle| \; \bigoplus\_{i \in [\ell]} W\_i = 0 \text{ and } \forall T \subsetneq [\ell], \bigoplus\_{i \in T} W\_i \neq 0 \right\}$$

and

$$\mathsf{SD}\_{\ell}(G^\*) = \{ W \in \mathsf{SD}\_{\ell} \mid WG^\* = 0 \}.$$

For any G<sup>∗</sup> , over P <sup>∗</sup> ← P(G<sup>∗</sup> ) the expected number of simple dependencies in P ∗ is

$$\begin{split} \mathop{\mathbb{E}}\_{P^\* \leftarrow \mathcal{P}(G^\*)} \sum\_{\ell=1}^r \sum\_{S \in \binom{[r]}{\ell}} \mathbbm{1}[P\_S^\* \in \mathsf{SD}\_\ell] &= \sum\_{\ell=1}^r \sum\_{S \in \binom{[r]}{\ell}} \Pr\_{P^\* \leftarrow \mathcal{P}(G^\*)}[P\_S^\* \in \mathsf{SD}\_\ell] \\ &= \sum\_{\ell=1}^r \binom{r}{\ell} \frac{|\mathsf{SD}\_\ell(G^\*)|}{\eta(G^\*)^\ell} . \end{split} \tag{6}$$

Now since any ℓ − 1 of the rows of any simple dependency are linearly independent, we have

<span id="page-33-1"></span>
$$\Pr\_{G^\* \leftarrow \mathbb{F}\_2^{n \times g}}[WG^\* = 0] = \frac{1}{2^{(\ell - 1)g}}$$

for any W ∈ SDℓ. Therefore,

$$\begin{aligned} \mathop{\mathbb{E}}\_{G^\* \leftarrow \mathbb{F}\_2^{n \times g}} |\mathsf{SD}\_{\ell}(G^\*)| &= \sum\_{W \in \mathsf{SD}\_{\ell}} \Pr\_{G^\* \leftarrow \mathbb{F}\_2^{n \times g}} [WG^\* = 0] \\ &= \frac{|\mathsf{SD}\_{\ell}|}{2^{(\ell - 1)g}} . \end{aligned}$$

By Markov's inequality it follows that for any q > 0, with probability 1 − 1/q over G<sup>∗</sup> ← F n×g 2 ,

$$|\mathsf{SD}\_{\ell}(G^{\*})| \leq \frac{|\mathsf{SD}\_{\ell}|}{2^{(\ell-1)g}} \cdot q.$$

Together with Lemma [11,](#page-32-1) we have that for any q, ε > 0 the expected number of simple dependencies computed in Equation [\(6\)](#page-33-1) is at most

$$\begin{split} \sum\_{\ell=1}^{r} \binom{r}{\ell} \frac{|\mathsf{SD}\_{\ell}(G^{\*})|}{\eta(G^{\*})^{\ell}} &\leq q \sum\_{\ell=1}^{r} \binom{r}{\ell} \frac{|\mathsf{SD}\_{\ell}|}{\eta(G^{\*})^{\ell} \cdot 2^{(\ell-1)g}} \\ &\leq \frac{q}{(1-\varepsilon)^{n}} \sum\_{\ell=1}^{r} \binom{r}{\ell} \frac{2^{g\ell}|\mathsf{SD}\_{\ell}|}{\binom{n}{t}^{\ell} 2^{(\ell-1)g}} \\ &= \frac{q \cdot 2^{g}}{(1-\varepsilon)^{n}} \sum\_{\ell=1}^{r} \binom{r}{\ell} \frac{|\mathsf{SD}\_{\ell}|}{\binom{n}{t}^{\ell}} \end{split}$$

with probability 1 − 1 <sup>q</sup> − 2 g ( n <sup>t</sup> )·<sup>ε</sup> 2 over G<sup>∗</sup> . Since

$$\frac{|\mathsf{SD}\_{\ell}|}{\binom{n}{t}^{\ell}} \le \Pr\_{w\_1,\ldots,w\_{\ell}\leftarrow\mathsf{S}\_{t,n}}[w\_1 \oplus \cdots \oplus w\_{\ell} = 0],$$

the remainder of the proof is devoted to showing that

<span id="page-34-1"></span>
$$\sum\_{\ell=1}^{r} \binom{r}{\ell}\_{w\_1,\ldots,w\_\ell \leftarrow \mathcal{S}\_{t,n}} \text{Pr}\_{\ell,n} \left[ w\_1 \oplus \cdots \oplus w\_\ell = 0 \right] \le 2^{-ct^2}.\tag{7}$$

for some constant c > 0. Setting ˜g = ct2/4, q = 2ct2/<sup>4</sup> , and ε = 2−<sup>t</sup> log(n/t)/<sup>8</sup> will then complete the proof of Lemma [12.](#page-33-0)

Let A be the transition matrix for the random walk on F n <sup>2</sup> where, at each step, we sample a random w ← St,n and move x 7→ x⊕w. Observe that Prw1,...,wℓ←St,n [w<sup>1</sup> ⊕ · · · ⊕w<sup>ℓ</sup> = 0] is equal to the probability that ℓ steps of this walk form a (not necessarily simple) cycle, i.e.,

$$\Pr\_{w\_1,\ldots,w\_\ell \leftarrow \mathcal{S}\_{t,n}}[w\_1 \oplus \cdots \oplus w\_\ell = 0] = \frac{1}{2^n} \operatorname{Tr}(A^\ell).$$

Let H be the transition matrix for the random walk on the hypercube graph on F n 2 . In Claim [13,](#page-34-0) we bound the probability that ℓ steps of A form a cycle in terms of the probability that ℓt steps of H form a cycle.

<span id="page-34-0"></span>Claim 13. If ℓ = O(n) and t = o(n 1/3 ), then Tr(A<sup>ℓ</sup> ) ≤ O e t 2 ℓ/n · Tr(Hℓt) .

Proof. Let E<sup>H</sup> denote the event that ℓt steps of H form a cycle, and let E<sup>A</sup> denote the event that ℓ steps of A form a cycle. Observe that

$$\frac{1}{2^n}\operatorname{Tr}(A^\ell) = \Pr[\mathcal{E}\_A] = \Pr\left[\mathcal{E}\_H \mid \text{every } t\text{-block is distinct}\right]$$

where we consider the walk in H as consisting of ℓ consecutive blocks of t steps each, and we say a block is "distinct" if a different index is changed in each step.

Furthermore,

$$\frac{1}{2^n} \operatorname{Tr} (H^{\ell t}) = \operatorname{Pr} [\mathcal{E}\_H] \ge \operatorname{Pr} \left[ \mathcal{E}\_H \mid \text{every } t\text{-block is distinct} \right] \cdot \operatorname{Pr} [\text{every } t\text{-block is distinct}] \cdot \frac{1}{2^n}$$

So Pr[EA] ≤ Pr[EH] Pr[every <sup>t</sup>-block is distinct] . Thus, it suffices to see that

Pr[every t-block is distinct] = Pr[a given t-block is distinct]<sup>ℓ</sup>

$$\begin{aligned} &\geq (1 - t/n)^{t\ell} \\ &\geq \left( e^{-t} \left( 1 - \frac{t^2}{n} \right) \right)^{t\ell/n} \\ &\geq e^{-t^2\ell/n} \cdot (1 - t^3\ell/n^2) \\ &\geq \Omega(e^{-t^2\ell/n}). \end{aligned}$$

Applying Claim [13,](#page-34-0) we have reduced the problem of proving Equation [\(7\)](#page-34-1) to showing that

$$\sum\_{\ell=1}^{r} \binom{r}{\ell} \cdot \frac{e^{t^2 \ell/n}}{2^n} \operatorname{Tr}(H^{\ell t}) \le 2^{-\Omega(t^2)}.\tag{8}$$

Fortunately, the eigenvalues of H are simple to compute:

<span id="page-35-0"></span>
$$\frac{1}{2^n}\operatorname{Tr}(H^{\ell t}) = \underset{x \leftarrow \mathbb{F}\_2^n}{\mathbb{E}}\left[\left(1 - \frac{2\operatorname{wt}(x)}{n}\right)^{\ell t}\right] \tag{9}$$

where wt(x) denotes the Hamming weight of x ∈ F n 2 . We analyze this expression separately depending on how large ℓ is.

Small ℓ (ℓ ≤ (e − Ω(1)) · n/t). We can rewrite Equation [\(9\)](#page-35-0) as a moment of a simple random walk:

$$\mathbb{E}\_{x \leftarrow \mathbb{F}\_2^n} \left[ \left( 1 - \frac{2 \operatorname{wt}(x)}{n} \right)^{\ell t} \right] = n^{-\ell t} \underset{X\_1, \dots, X\_n \leftarrow \{1, -1\}}{\mathbb{E}} \left[ \left( \sum\_{i=1}^n X\_i \right)^{\ell t} \right] . \text{ }$$

Let X = P<sup>n</sup> <sup>i</sup>=1 X<sup>i</sup> where X1, . . . , X<sup>n</sup> ← {1, −1}. For small ℓ, the Gaussian approximation to these moments is good enough. For even p,

$$\begin{aligned} \mathbb{E}\left[X^p\right] &= \sum\_{i\_1,\ldots,i\_p \in [n]} \mathbb{E}[X\_{i\_1} \cdots X\_{i\_p}] \\ &= |\{(i\_1,\ldots,i\_p) \in [n]^p \mid \text{ each } i\_j \text{ appears an even number of times}\}| \\ &\leq n^{p/2} \cdot (p-1)!! \end{aligned}$$

For odd p, E[X<sup>p</sup> ] = 0. Therefore, for ℓ = O(n/t) we have

$$\begin{aligned} \left(\frac{r}{\ell}\right) \cdot \frac{e^{t^2 \ell/n}}{2^n} \operatorname{Tr}(H^{\ell t}) &\leq e^{O(t)} \left(\frac{n}{\ell}\right) \cdot \frac{(\ell t - 1)!!}{n^{\ell t/2}} \\ &\leq e^{O(t)} \left(\frac{en}{\ell}\right)^{\ell} \cdot \left(\frac{\ell t}{en}\right)^{\ell t/2} \cdot O(\sqrt{\ell t}) \\ &= e^{O(t)} \left(\frac{\ell}{en}\right)^{\ell(t/2 - 1)} \cdot t^{\ell t/2} \cdot O(\sqrt{\ell t}) \end{aligned}$$

If ℓ ≤ t, then this yields

$$\binom{r}{\ell} \cdot \frac{e^{t^2 \ell/n}}{2^n} \operatorname{Tr}(H^{\ell t}) \le e^{O(t)} \left(\frac{t^{t-1}}{(en)^{t/2-1}}\right)^{\ell} = n^{-\Omega(t)}$$

and if t < ℓ ≤ (e − Ω(1)) · n/t,

$$\binom{r}{\ell} \cdot \frac{e^{t^2 \ell/n}}{2^n} \operatorname{Tr}(H^{\ell t}) \le e^{O(t)} \left(\frac{e - \Omega(1)}{et}\right)^{\ell(t/2 - 1)} \cdot t^{\ell t/2} \cdot O(\sqrt{\ell t}) = 2^{-\Omega(t^2)} \cdot t$$

In either case we have a bound of 2<sup>−</sup>Ω(<sup>t</sup> 2 ) . Large ℓ (ℓ ≥ (e − o(1)) · n/t). Using the binomial theorem,

$$\begin{split} \frac{1}{2^n} \text{Tr}(H^{\ell t}) &= \mathop{\mathbb{E}}\_{x \leftarrow \mathbb{F}\_2^n} \left[ \left( 1 - \frac{2 \,\text{wt}(x)}{n} \right)^{\ell t} \right] \\ &= \frac{1}{2^n} \sum\_{s=0}^n \binom{n}{s} \cdot \left( 1 - \frac{2s}{n} \right)^{\ell t} \\ &\leq \frac{1}{2^n} \sum\_{s=0}^n \binom{n}{s} \cdot e^{-2s\ell t/n} \\ &= \left( \frac{1 + e^{-2\ell t/n}}{2} \right)^n. \end{split}$$

For ℓ ≥ (e − o(1)) · n/t, this is at most 1+e o(1)−2e 2 n . Since 1+e −2e 2 < 2 <sup>−</sup>0.99, we have for r ≤ 0.99n that

$$\sum\_{\ell=1}^r \binom{r}{\ell} \cdot \frac{e^{t^2 \ell/n}}{2^n} \text{Tr}(H^{\ell t}) \le 2^r \cdot e^{t^2} \cdot \left(\frac{1 + e^{o(1) - 2e}}{2}\right)^n = 2^{-\Omega(n)}.\tag{7}$$

<span id="page-36-0"></span>Theorem 2. For any p, η ∈ (0, 1/2), there exists g = Ω(log<sup>2</sup> n), t = Θ(log n) such that LDPC-PRC0[n, g, t, 0.99n, η,(0.99n) −1/4 ] is a zero-bit public-key PRC (Definition [2\)](#page-22-3) that is robust to every p-bounded channel, where pseudorandomness rests on the LPNg,η assumption (Assumption [2\)](#page-28-3).

Proof. By Lemma [4,](#page-26-1) there exists t = Θ(log n) such that for any g > 0, LDPC-PRC0[n, g, t, 0.99n, η,(0.99n) −1/4 ] is robust to every p-bounded channel.

By Lemma [9,](#page-31-0) there exists a function g = Ω(log<sup>2</sup> n) such that the generator matrix of this code — that is, G for (P, G) ← LDPC[n, g, t, 0.99n] — is negl(n)-close to uniformly random.

Since G has dimensions n × g, the LPNg,η assumption implies that LDPC-PRC0[n, g, t, 0.99n, η,(0.99n) −1/4 ] is a public-key PRC.

### <span id="page-37-0"></span>6 Boosting the rate and robustness of any pseudorandom code

### <span id="page-37-1"></span>6.1 Multi-bit pseudorandom codes

We show how to construct a multi-bit PRC from any zero-bit PRC. The high-level idea is to encode a given message bit-by-bit, where we use codewords from the zero-bit PRC to represent bits of the message that are 1, and uniformly random strings to represent bits of the message that are 0. We say this encoding consists of many blocks, where each block is either a codeword from the zero-bit PRC or a random string. Since our zero-bit PRC allows a decoder with the secret key to distinguish uniform strings from noisy codewords, we can use this decoder to recover each bit of the message from each block.

However, as described so far, there are two issues with this scheme. The first is that this scheme encodes the all-0 string as a uniformly random string, but the error correction property of a PRC requires that the decoder can distinguish encodings (of any message) from random strings. Thus, we modify the above scheme to append a codeword from the zero-bit PRC to the end of every encoding.

The other issue is that this scheme may lose the zero-bit PRC's robustness. In particular, consider a zero-bit PRC that is robust to all p-bounded channels; we would like for our multi-bit PRC to retain this robustness. However, consider the channel that flips each bit in only the first block of the encoding, independently with probability <sup>1</sup> 2 . The decoder will now be unable to recover the first bit of the message, and this channel is p-bounded since it changes only a sub-constant fraction of the bits. The issue here is that our p-bounded channel was not bounded at all on the first block; we'd like for the channel's effect on every block of the encoding to be p-bounded. We solve this issue by randomly permuting the encoding, which ensures that the errors introduced by the channel cannot be too concentrated in any block. The decoder now inverts the permutation before decoding block-by-block as before.

Although the constructions are essentially the same, we separately present multi-bit secret-key and public-key PRCs as they have slightly different syntax.

<span id="page-37-2"></span>Construction 3 (Multi-bit secret-key PRC). Let PRC<sup>0</sup> = (KeyGen<sup>0</sup> , Encode0, Decode0) be a zero-bit secretkey PRC with block length n. We define an ℓ-bit secret-key PRC, PRC<sup>ℓ</sup> = (KeyGen<sup>ℓ</sup> , Encodeℓ, Decodeℓ), as follows:

- KeyGen<sup>ℓ</sup> (1<sup>λ</sup> ): Sample sk<sup>0</sup> ← KeyGen<sup>0</sup> (1<sup>λ</sup> ). Sample a random permutation π : [n·(ℓ+ 1)] → [n·(ℓ+ 1)]. Output sk = (sk<sup>0</sup> , π).
- Encodeℓ(sk, m): Given as input a message m ∈ {0, 1} ℓ , for each i ∈ [ℓ + 1], let

$$c\_i = \begin{cases} c \leftarrow \{0, 1\}^n & \text{if } \mathfrak{m}\_i = 0 \text{ and } i \neq \ell + 1\\ c \leftarrow \mathsf{Encode}\_0(\mathsf{sk}\_0) & \text{if } \mathfrak{m}\_i = 1 \text{ and } i \neq \ell + 1\\ c \leftarrow \mathsf{Encode}\_0(\mathsf{sk}\_0) & \text{if } i = \ell + 1 \end{cases}$$

Let y = c1|| . . . ||c<sup>ℓ</sup>+1 ∈ {0, 1} <sup>n</sup>(ℓ+1). Output x = y<sup>π</sup>(1)|| . . . ||y<sup>π</sup>(n(ℓ+1)).

• Decodeℓ(sk, x1|| . . . ||x<sup>n</sup>(ℓ+1)): For each i ∈ [ℓ+1], let ˆy<sup>i</sup> = xπ−1(1+(i−1)n) ||xπ−1(2+(i−1)n) || . . . ||xπ−1(n+(i−1)n)

.

$$
\hat{x}\_i = \begin{cases} 1 & \text{if } \mathsf{Decode}\_0(\mathsf{sk}\_0, \hat{y}\_i) = 1 \\ 0 & \text{otherwise} \end{cases}
$$

If ˆx<sup>ℓ</sup>+1 ̸= 1, output ⊥. Otherwise, output mˆ = ˆxπ−1(1)|| . . . ||xˆπ−1(ℓ) .

<span id="page-37-3"></span>Construction 4 (Multi-bit public-key PRC). Let PRC<sup>0</sup> = (KeyGen<sup>0</sup> , Encode0, Decode0) be a zero-bit publickey PRC with block length n. We define a ℓ-bit public-key PRC, PRC<sup>ℓ</sup> = (KeyGen<sup>ℓ</sup> , Encodeℓ, Decodeℓ), as follows:

• KeyGen<sup>ℓ</sup> (1<sup>λ</sup> ): Sample (sk<sup>0</sup> , pk<sup>0</sup> ) ← KeyGen<sup>0</sup> (1<sup>λ</sup> ). Sample a random permutation π : [n · (ℓ + 1)] → [n · (ℓ + 1)]. Output sk = (sk<sup>0</sup> , π) and pk = (pk<sup>0</sup> , π).

• Encodeℓ(pk, m): Given as input a message m ∈ {0, 1} ℓ , for each i ∈ [ℓ + 1], let

$$c\_i = \begin{cases} c \leftarrow \{0, 1\}^n & \text{if } \mathfrak{m}\_i = 0 \text{ and } i \neq \ell + 1\\ c \leftarrow \mathsf{Encode}\_0(\mathsf{pk}\_0) & \text{if } \mathfrak{m}\_i = 1 \text{ and } i \neq \ell + 1\\ c \leftarrow \mathsf{Encode}\_0(\mathsf{pk}\_0) & \text{if } i = \ell + 1 \end{cases}$$

Let y = c1|| . . . ||cℓ+1 ∈ {0, 1} <sup>n</sup>(ℓ+1). Output x = yπ(1)|| . . . ||yπ(n(ℓ+1)).

• Decodeℓ(sk, x1|| . . . ||xn(ℓ+1)): For each i ∈ [ℓ+1], let ˆy<sup>i</sup> = xπ−1(1+(i−1)n) ||xπ−1(2+(i−1)n) || . . . ||xπ−1(n+(i−1)n) .

$$
\hat{x}\_i = \begin{cases} 1 & \text{if } \mathbf{Decode}\_0(\mathbf{sk}\_0, \hat{y}\_i) = 1 \\ 0 & \text{otherwise} \end{cases}
$$

If ˆxℓ+1 ̸= 1, output ⊥. Otherwise, output mˆ = ˆxπ−1(1)|| . . . ||xˆπ−1(ℓ) .

Claim 14. If PRC<sup>0</sup> = (KeyGen<sup>0</sup> , Encode0, Decode0) is a zero-bit secret-key (public-key) PRC robust to pbounded channels, PRC<sup>ℓ</sup> is a ℓ-bit secret-key (public-key) PRC robust to (p − ε)-bounded channels for any constant ε ∈ (0, p).

Proof. Error correction. We first show that with overwhelming probability, a (p − ε)-bounded channel applied to a codeword of Encode<sup>ℓ</sup> is p-bounded on each of its blocks. Since PRC<sup>0</sup> is robust against pbounded channels, this implies that each block will be correctly decoded by Decode0. First, by definition of p-boundedness, the entire codeword from PRC<sup>ℓ</sup> will have at most (p − ε)n(ℓ + 1) errors with overwhelming probability. Let α ≤ p−ε be the actual fraction of errors. Now, fix any n-length block of the codeword after the permutation has been inverted. Observe that over the randomness of the permutation, the number of errors in this block is a random variable X ∼ Hyp(n(ℓ + 1), αn(ℓ + 1), n). By Lemma [3,](#page-20-2)

$$\Pr\left[X \ge (\alpha + \varepsilon)n\right] \le e^{-2\varepsilon^2 n},$$

which is negligible in n. Since α ≤ p − ε, the probability that there are at least pn errors in our block is at most the probability that there are (α + ε)n errors, which we've just shown is negligible. By a union bound, the probability that any block has more than pn errors is negligible.

We now show the second property of error correction, that an unrelated string c decodes to ⊥ with overwhelming probability. Consider the last block ˆy<sup>ℓ</sup>+1 of c after the permutation has been inverted. By error correction of PRC0, the probability over sk<sup>0</sup> that Decode0(sk<sup>0</sup> , yˆ<sup>ℓ</sup>+1) = 1 is negligible. Therefore, with overwhelming probability, Decodeℓ(sk, c) = ⊥.

Pseudorandomness. We prove pseudorandomness of public-key PRCℓ. We observe that the same proof holds for secret-key PRCℓ, by omitting the public keys as input to the adversaries A and B, and instead giving them oracle access to Encode0(sk<sup>0</sup> , ·) and Encodeℓ(sk, ·) respectively.

Suppose that an adversary A given pk can distinguish between oracle access to Encodeℓ(pk, ·) and the uniform distribution. Then B given pk<sup>0</sup> can distinguish between oracle access to Encode<sup>0</sup> and the uniform distribution as follows. B samples a random permutation π : [n(ℓ + 1)] → [n(ℓ + 1)] and gives pk = (pk<sup>0</sup> , π) to A as input. Whenever A queries m to its oracle, B computes a response x by following Encodeℓ, but querying its own oracle when Encode<sup>ℓ</sup> requires a call to Encode0, and using π as the permutation. Observe that if B's oracle is the uniform distribution, the resulting x is permutation of a uniform string, so x is uniform. If B's oracle is Encode0, the resulting x is drawn from Encodeℓ(sk, m). Therefore, B's advantage is exactly A's advantage.

Remark. Unfortunately, Constructions [3](#page-37-2) and [4](#page-37-3) yield codes of rate roughly 1/n: If the underlying zero-bit PRC has block length n, then in order to encode a ℓ-bit message we need codewords of length n · (ℓ + 1). Ideally, we would like to have constant rate — i.e., to encode ℓ-bit messages into O(ℓ)-bit codewords. While typical LDPC codes have constant rate, and there is a simple modification of our pseudorandom LDPC codes that have constant rate, at densities of Ω(log n) it is not known how to decode from a constant rate of errors. Instead, we build constant-rate PRCs generically from any multi-bit PRC in Section [6.2.](#page-39-0)

### <span id="page-39-0"></span>6.2 Constant-rate pseudorandom codes

We now show how to build constant-rate PRCs from any multi-bit PRC (as in Section [6.1\)](#page-37-1) and any constantrate error-correcting code. We state the public-key version of the following construction only; as usual, the secret-key version is similar.

<span id="page-39-2"></span>Construction 5 (Constant-rate public-key PRC). Let λ be a security parameter and PRC<sup>λ</sup> be a λ-bit public-key PRC with block length n ′ . Let (Enc, Dec) be any error-correcting code with block length n > λ and messages of length k. Let PRG : {0, 1} <sup>λ</sup> → {0, 1} <sup>n</sup> be any pseudorandom generator. We define PRC[PRCλ,(Enc, Dec)] which is a k-bit public-key PRC as follows:

- PRC.KeyGen(1<sup>λ</sup> ): Sample (sk′ , pk′ ) ← PRCλ.KeyGen(1<sup>λ</sup> ). Sample a random permutation π : [n ′ +n] → [n ′ + n]. Let sk = (sk′ , π) and pk = (pk′ , π); output (sk, pk).
- PRC.Encode(pk, m): Given as input a message m ∈ {0, 1} k , let r ← {0, 1} λ , and let

x ← PRCλ.Encode(pk, r)||PRG(r) ⊕ Enc(m).

Let x1, . . . , xn′+<sup>n</sup> denote the bits of x. The output is x<sup>π</sup>(1)||x<sup>π</sup>(2)|| . . . ||x<sup>π</sup>(n′+n) .

• PRC.Decode(sk, c): Letting c1, . . . , cn′+<sup>n</sup> denote the bits of c, the decoder first computes

$$y = c\_{\pi^{-1}(1)} | | \cdot \ldots | | c\_{\pi^{-1}(n'+n)} \cdot |$$

The decoder then parses y as y1||y2, where |y1| = n ′ and |y2| = n. It computes r ← PRCλ.Decode(sk, y1) and outputs m = Dec(PRG(r) ⊕ y2).

The block length of the resulting PRC is n + n ′ , so the rate is k/(n + n ′ ). Since n ′ is only a function of the security parameter λ and does not depend on k, for large k the rate approaches the rate k/n of the underlying error-correcting code (Enc, Dec).

<span id="page-39-1"></span>Theorem 3. Let PRC<sup>λ</sup> be a λ-bit public-key PRC with block length n ′ , and let (Enc, Dec) be any errorcorrecting code with block length n > λ and messages of length k.

Then PRC = PRC[PRCλ,(Enc, Dec)] of Construction [5](#page-39-2) is a public-key PRC where

- the rate of PRC is k/(n + n ′ ); and
- for any constants p, ε ∈ (0, 1/2), if PRC<sup>λ</sup> and (Enc, Dec) are robust to channels that introduce at most a p fraction of errors at random locations, then PRC is robust to all (p − ε)-bounded channels.

Proof. Pseudorandomness. By pseudorandomness of PRCλ, no polynomial-time adversary can distinguish between PRC.Encode and a hybrid where x ← PRCλ.Encode(pk, r) is replaced by a uniformly random x ← {0, 1} n ′ . By pseudorandomness of the PRG, this is computationally indistinguishable from a hybrid where PRG(r) is replaced by a uniformly random s ← {0, 1} <sup>n</sup>, making (x||s ⊕ Enc(m)) uniform. Therefore, in this hybrid, which is indistinguishable from oracle access to PRC.Encode, each query to the oracle outputs an independently drawn uniform string in {0, 1} n+n ′ .

Robustness. We first show that for any p-bounded channel E, if the decoder receives c ← E(PRC.Encode(pk, m)), then the resulting y<sup>1</sup> and y<sup>2</sup> are equal to E1(Encode(r)) and E2(Enc(m))⊕PRG(r) respectively, where E<sup>1</sup> and E<sup>2</sup> are both p-bounded. Observe that the number of errors introduced by E<sup>1</sup> is distributed as a hypergoemetric random variable with a population of size n+n ′ , p(n+n ′ ) success elements (representing the errors), and n ′ draws. By Lemma [3,](#page-20-2) the probability that E<sup>1</sup> introduces at least (p − ε)n ′ errors is at most e −2ε <sup>2</sup>n ′ ,

which is negligible. Similarly, the number of errors introduced by E<sup>2</sup> is distributed as a hypergoemetric random variable with a population of size n + n ′ , p(n + n ′ ) success elements (representing the errors), and n draws. By Lemma [3,](#page-20-2) the probability that E<sup>2</sup> introduces at least (p − ε)n ′ errors is at most e −2ε <sup>2</sup>n, which is negligible as n > λ. By a union bound, with overwhelming probability both E<sup>1</sup> and E<sup>2</sup> introduce errors with at most a rate of (p − ε), and therefore they are (p − ε)-bounded.

Furthermore, because of the random permutation π, the locations of the errors on y<sup>2</sup> are random. Therefore by robustness of PRCλ, we have that Decode(sk, y1) = r with overwhelming probability; and by error correction of (Enc, Dec), Dec(PRG(r) ⊕ y2) = Dec(BSCp(Enc(m))) = m with overwhelming probability as well.

If we instantiate Construction [5](#page-39-2) with

- PRC<sup>λ</sup> from Construction [4,](#page-37-3) using the LDPC-based PRCs of Construction [2](#page-25-3) as PRC0; and
- the error-correcting codes (Enc, Dec) of [\[ABN](#page-62-2)+92, [NN93,](#page-64-2) [Ta-17\]](#page-64-3),

then we obtain constant-rate PRCs with robustness to every p-bounded channel for p ∈ (0, 1/2).

### <span id="page-40-0"></span>6.3 Pseudorandom codes for the deletion channel

In this section, our primary goal is to construct a PRC, PRCdel, that is robust against a constant-rate deletion channel. That is, the message can be recovered from an encoding under PRCdel when each of its bits is deleted independently with some constant probability p. The actual robustness guarantee we obtain is even stronger: we can recover the message even when this constant-rate deletion channel is composed with a constant-rate binary symmetric channel. Our construction makes black-box use of any PRC that is robust against p-bounded channels.

Our high-level idea is to take an encoding of this original PRC and make it redundant, while preserving pseudorandomness. Let x = x1, . . . , x<sup>n</sup> be a PRC encoding of some message. We could make x robust to the deletion channel by duplicating each bit x<sup>i</sup> some number of times m. However, the result would no longer be pseudorandom. Instead of duplicating x<sup>i</sup> , we sample a random y ∈ {0, 1} <sup>m</sup>, conditioned on the majority of the bits of y being x<sup>i</sup> . Observe that if x<sup>i</sup> is Ber 1 2 , y is uniform over {0, 1} <sup>m</sup>. Since x<sup>i</sup> is a bit of our PRC, it is pseudorandom, and y is indistinguishable from uniform. The resulting codeword is y1, . . . , yn, where each y<sup>i</sup> ∈ {0, 1} <sup>m</sup>. We call this the "majority code."

Observe that given y = y1, . . . , yn, one can recover x by computing the majority of each length-m block y<sup>i</sup> . If each bit of y is deleted independently with some probability p to yield y ′ , we can recover an approximate version of x as follows. We partition y ′ into equal-length blocks y ′ 1 , . . . , y′ n , and we compute the majority of each block. Intuitively, we expect most of the new blocks y ′ i to be subsets of the corresponding original blocks yi . Since the deletions are random, we expect them to preserve the majority for most blocks. Therefore, the message x ′ that we recover should be approximately x, with some bounded number of bits flipped. Recalling that x itself was a PRC codeword, and our PRC is robust to bounded-weight channels, we can recover the original message from x ′ .

It may be tempting to apply this majority code to other encoding schemes such as pseudorandom encryption, and the result would indeed be pseudorandom. However, it would not be robust against a constant-rate deletion channel. Since decoding from the deletion channel introduces bounded-weight errors, the message that the majority code is applied to must be error-correcting against bounded-weight channels. Therefore, our PRC is crucial to this approach.

We first introduce some notation. Let Maj(y) denote the majority function for bitstrings y, where ties are resolved by choosing a random bit. For a given positive odd integer m ∈ N, let MajEnc<sup>m</sup> : {0, 1} → {0, 1} <sup>k</sup> be a randomized function that takes an input bit b ∈ {0, 1} and outputs a random string y ∈ {0, 1} <sup>m</sup> conditioned on Maj(y) = b. For x ∈ {0, 1} <sup>n</sup>, we define MajEncm(x) := (MajEncm(x1), . . . , MajEncm(xn)) ∈ {0, 1} nm.

![](_page_41_Figure_0.jpeg)

Figure 2: Objects from the proof of Lemma [15:](#page-41-0) y ← MajEncm(x), z ← BSC<sup>q</sup> ◦ BDCp(y), the function f, and the partitions R, S for n = 3, m = 5. In this illustration x = (1, 1, 0) and MajDec<sup>3</sup> (z) = (0, 1, 0). There are deletions at locations D = {3, 11} (indicated by solid red), and there are errors from BSC<sup>q</sup> at locations 2 and 4 (indicated by hatched red). The arrows indicate the mapping f, i.e. an arrow points from an index in z to the index in y from which it originated.

The decoding algorithm MajDec<sup>n</sup> : {0, 1} <sup>∗</sup> → {0, 1} <sup>n</sup> evenly partitions the received string into n blocks and outputs a string of the blocks' majorities.

MajEncm(x):

- 1. For each i ∈ [len x], let y <sup>i</sup> = MajEncm(xi).
- 2. Output (y 1 || · · · ||y len x ) ∈ {0, 1} len <sup>x</sup>·<sup>m</sup>.

MajDecn(z):

- 1. Partition z into n blocks z = (z 1 || · · · ||z <sup>n</sup>) such that len(z i ) − len(z)/n <sup>≤</sup> 1 for all <sup>i</sup> <sup>∈</sup> [n].
- 2. Output (Maj(z 1 ), . . . , Maj(z <sup>n</sup>)).

In Lemma [15,](#page-41-0) we show that majority encoding a message allows us to recover an approximation of the message with bounded-weight error after a deletion channel is applied. This holds even if this deletion channel is composed with a binary symmetric channel.

<span id="page-41-0"></span>Lemma 15. Assume m = Ω(n log<sup>6</sup> n). For any constant deletion rate p ∈ (0, 1) and error rate q ∈ (0, 1/2), there exists a constant ε > 0 such that

$$\Pr\_{x \leftarrow \{0, 1\}^n} \left[ \text{wt} (x \oplus \text{MajDec}\_n \circ \text{BSC}\_q \circ \text{BDC}\_p \circ \text{MajEnc}\_m (x)) \le (1/2 - \varepsilon) \cdot n \right] \ge 1 - \text{negl}(n).$$

Proof. Let y ← MajEncm(x) and let z ← BSC<sup>q</sup> ◦ BDCp(y). Let D ⊆ [nm] be the set of indices deleted by BDCp; D is a random variable where each i ∈ [nm] is included in D independently with probability p. Let f : [nm − |D|] → [nm] be the function that maps indices of z to those of y, i.e., z<sup>j</sup> = BSCq(y<sup>f</sup>(j)).

Let R = R1, . . . , R<sup>n</sup> ⊆ [nm] be the partition of [nm] into n blocks of length m. Let S = S1, . . . , S<sup>n</sup> ⊆ [nm − |D|] be the partition of [nm − |D|] into almost-equal-sized blocks from the definition of MajDecn(z). R and S define partitions of y and z, respectively. All of

Let a, b ∈ [nm] be such that a ≤ b. Applying Hoeffding's inequality to |[a, b] \ D| = P<sup>b</sup> <sup>j</sup>=<sup>a</sup> <sup>1</sup>[<sup>j</sup> ̸∈ <sup>D</sup>] yields

$$\Pr\left[\left| (b-a+1)(1-p) - \left[ [a,b] \backslash D \right] \right| > \sqrt{nm} \log n \right] \le e^{-\Omega(\log^2 n)}.$$

By a union bound, with probability 1 − negl(n) we have that for every a, b ∈ [nm]

<span id="page-42-1"></span>
$$\left| (b - a + 1)(1 - p) - |[a, b] \backslash D| \right| \le \sqrt{nm} \log n. \tag{10}$$

That is, the number of deletions in every contiguous interval [a, b] of y concentrates and is roughly p(b−a)± √ nm log n.

We now argue in Claim [16](#page-42-0) that because of this concentration, each S<sup>i</sup> in the decoder's partition corresponds to a subset of the original message y that is largely contained in R<sup>i</sup> . That is, the symmetric set difference between f(Si) and (R<sup>i</sup> \ D) is small.

<span id="page-42-0"></span>Claim 16. If Equation [\(10\)](#page-42-1) holds for all a, b ∈ [nm], then for all i ∈ [n] we have |f(Si)△(R<sup>i</sup> \ D)| = O( √ nm log n) (where △ denotes the symmetric set difference).

Proof. Observe that |f(Si)△(R<sup>i</sup> \ D)| ≤ |(i − 1)m − min f(Si)| + |im − max f(Si)|. We will show that |(i − 1)m − min f(Si)| = O( √ nm log n). A nearly identical proof shows that |im − max f(Si)| = O( √ nm log n) as well, so this will complete the proof.

Setting [a, b] = [nm] to be all of <sup>y</sup> in Equation [\(10\)](#page-42-1), we have that <sup>|</sup>(1 <sup>−</sup> <sup>p</sup>)nm <sup>−</sup> len <sup>z</sup>| ≤ <sup>√</sup> nm log n. Therefore, |(1 − p)m − |S<sup>i</sup> || ≤ <sup>l</sup> <sup>√</sup> nm log n n m for every i ∈ [n]. It follows that for every i ∈ [n],

<span id="page-42-2"></span>
$$|(1-p)(i-1)m - \min S\_i| = O(\sqrt{nm}\log n). \tag{11}$$

For any j ∈ [nm−|D|], setting [a, b] = [f(j)] in Equation [\(10\)](#page-42-1) we have that |j − (1 − p)f(j)| = O( √ nm log n). Applying this fact to j = min S<sup>i</sup> for any i ∈ [n],

$$|\min S\_i - (1 - p)\min f(S\_i)| = O(\sqrt{nm}\log n).$$

Together with Equation [\(11\)](#page-42-2) and the fact that p ∈ (0, 1) is a constant, we have

$$|(i-1)m - \min f(S\_i)| = O(\sqrt{nm} \log n)$$

as desired.

So far, we've argued that each block z i in the decoder's partition consists mostly of bits from block y <sup>i</sup> of the encoding. We now argue that with high probability, the bits of y i that were excluded and the bits from other blocks that were erroneously included do not affect the majority of z i .

To do so, we define ∆<sup>i</sup> to be the difference of the erroneously excluded bits and the erroneously included bits, converted to values in {−1, 1} so we can later reason about this as a random walk. Let

$$\Delta\_i = \sum\_{j \in (R\_i \backslash D) \backslash f(S\_i)} (-1)^{y\_j} - \sum\_{j \in f(S\_i) \backslash (R\_i \backslash D)} (-1)^{y\_j} \cdot \square$$

Conditioned on Equation [\(10\)](#page-42-1) holding for all a, b ∈ [nm], Claim [16](#page-42-0) implies that ∆<sup>i</sup> is a sum of O( √ nm log n) random {1, −1} variables. Furthermore, these random variables are independent because y is uniform over {0, 1} nm. By Hoeffding's inequality,

<span id="page-42-4"></span>
$$\Pr[|\Delta\_i| \ge (nm)^{1/4} \log^{3/2} n] \le 2 \exp\left(\frac{-\sqrt{nm}\log^3 n}{O(\sqrt{nm}\log n)}\right) \le \text{negl}(n). \tag{12}$$

By a union bound, the probability that |∆<sup>i</sup> | ≤ (nm) 1/4 log<sup>3</sup>/<sup>2</sup> n for all i ∈ [n] is at least 1 − negl(n).

<span id="page-42-3"></span>We will complete the proof by applying Claim [17](#page-42-3) with N = |S<sup>i</sup> |, N′ = |R<sup>i</sup> ∩ D|, and ∆ = ∆<sup>i</sup> . The variables X<sup>j</sup> are the values of y<sup>j</sup> for j ∈ f(Si) ∪ (R<sup>i</sup> ∩ D) and Z<sup>j</sup> are the errors introduced by BSCq. Since the sets f(Si) ∪ (R<sup>i</sup> ∩ D) are disjoint for distinct i, the events that Maj(zi) = x<sup>i</sup> are independent once we condition on the values of y<sup>j</sup> for j ̸∈ S i∈[n] f(Si) ∪ (R<sup>i</sup> ∩ D); therefore the result will follow from a Chernoff bound.

Claim 17. Let N, N′ ∈ N and ∆ ∈ R be such that N′ = O(N) and ∆ = O( √ N). Let X1, . . . , X<sup>N</sup> , Y1, . . . , YN′ be independent, uniform {−1, 1} random variables and Z1, . . . , Z<sup>N</sup> be independent {−1, 1} random variables with expectation δ = Ω(1). Then for sufficiently large N,

$$\Pr\left[\text{sgn}\left(\sum\_{j\in[N]} X\_j \cdot Z\_j\right) = \text{sgn}\left(\sum\_{j\in[N]} X\_j + \sum\_{j\in[N']} Y\_j + \Delta\right)\right] = \frac{1}{2} + \Omega(1),$$

where we define sgn(0) to be a random value in {−1, 1}.

Proof. We can equivalently view Z<sup>j</sup> as a random variable which is 1 with probability δ, and a uniformly random {−1, 1} value with probability 1−δ. Let F be the set of indices j ∈ [N] where Z<sup>j</sup> is deterministically 1. By a Chernoff bound, |δN − |F|| ≤ δN/2 with probability 1 − negl(n); fix such an F. We can write

$$\begin{aligned} \sum\_{j \in [N]} X\_j \cdot Z\_j &= \sum\_{j \in F} X\_j + \sum\_{j \in [N] \backslash F} X\_j \cdot Z\_j \\ &=: \sum\_{j \in F} X\_j + \sum\_{j \in [N\_a]} X\_j^a \end{aligned}$$

where we have defined N<sup>a</sup> := N − |F| and {−1, 1} variables {X<sup>a</sup> j }j∈[Na] = {X<sup>j</sup> · Zj}j∈[N]\<sup>F</sup> . We also write

$$\begin{aligned} \sum\_{j \in [N]} X\_j + \sum\_{j \in [N']} Y\_j + \Delta &= \sum\_{j \in F} X\_j + \left( \sum\_{j \in [N] \backslash F} X\_j + \sum\_{j \in [N']} Y\_j \right) + \Delta \\ &=: \sum\_{j \in F} X\_j + \sum\_{j \in [N\_b]} X\_j^b + \Delta \end{aligned}$$

where we have defined N<sup>b</sup> := N − |F| + N′ and {−1, 1} variables {X<sup>b</sup> j }j∈[Nb] = {Xj}j∈[N]\<sup>F</sup> ∪ {Yj}j∈[N′ ] . Observe that {Xj}j∈<sup>F</sup> ∪ {X<sup>a</sup> j }j∈[Na] ∪ {X<sup>b</sup> j }j∈[Nb] are all independent, uniformly random {−1, 1} variables. We wish to show that

$$\Pr\left[\text{sgn}\left(\sum\_{j\in F} X\_j + \sum\_{j\in [N\_a]} X\_j^a\right) = \text{sgn}\left(\sum\_{j\in F} X\_j + \sum\_{j\in [N\_b]} X\_j^b + \Delta\right)\right] = \frac{1}{2} + \Omega(1).$$

Let X = P <sup>j</sup>∈<sup>F</sup> X<sup>j</sup> , A = P <sup>j</sup>∈[Na] X<sup>a</sup> j , and B = P <sup>j</sup>∈[Nb] X<sup>b</sup> j . The above equation we wish to show becomes

$$\Pr[\text{sgn}(X+A) = \text{sgn}(X+B+\Delta)] = \frac{1}{2} + \Omega(1).$$

If |X| > max{|A|, |B + ∆|}, then sgn(X + A) = sgn(X + B + ∆) = sgn(X). On the other hand,

$$\Pr\left[\text{sgn}(X+A) = \text{sgn}(X+B+\Delta) \mid |X| \le \max\{|A|, |B+\Delta|\}\right] = \frac{1}{2}.$$

Therefore, it suffices to show that Pr[|X| > max{|A|, |B + ∆|}] = Ω(1). We do this by bounding each of the three factors below separately:

$$\Pr\left[|X| > \max\{|A|, |B+\Delta|\}\right] \ge \Pr\left[|X| > \sqrt{|F|} + |\Delta|\right] \cdot \Pr\left[|A| \le \sqrt{|F|} + |\Delta|\right] \cdot \Pr\left[|B+\Delta| \le \sqrt{|F|} + |\Delta|\right] \cdot \Pr\left[|A| > \sqrt{|F|} + |\Delta|\right]$$

- Since p |F| + |∆| = O( p |F|), the central limit theorem implies that Pr h |X| > p |F| + |∆| i = Ω(1).
- Since <sup>N</sup><sup>a</sup> <sup>=</sup> <sup>O</sup>(|F|), Hoeffding's inequality implies that Pr <sup>h</sup> |A| ≤ p |F| + |∆| i ≥ Pr h |A| ≤ p |F| i = Ω(1).

• By the triangle inequality, Pr h |B + ∆| ≤ p |F| + |∆| i ≥ Pr h |B| ≤ p |F| i . Since N<sup>b</sup> = O(|F|), Hoeffding's inequality again implies that Pr h |B| ≤ p |F| i = Ω(1).

It only remains to show that the conditions of Claim [17](#page-42-3) are satisfied with probability 1 − negl(n). That is, for N = |S<sup>i</sup> |, we need to show that N′ = |R<sup>i</sup> ∩ D| = O(N) and ∆ = ∆<sup>i</sup> = O( √ N) with probability 1 − negl(n). Conditioned on Equation [\(10\)](#page-42-1) holding for all a, b ∈ [nm], we have that |pm − |R<sup>i</sup> ∩ D|| ≤ √ nm log n and |(1 − p)m − |S<sup>i</sup> || = O( √ nm log n) for all i ∈ [n]. Therefore |R<sup>i</sup> ∩ D| = Θ(m) and |S<sup>i</sup> | = Θ(m). By Equation [\(12\)](#page-42-4), |∆<sup>i</sup> | = O((nm) 1/4 log3/<sup>2</sup> n) for all i ∈ [n] with probability 1 − negl(n). Therefore, |∆<sup>i</sup> | = O( p |S<sup>i</sup> |) with probability 1 − negl(n) if m = Ω(n log<sup>6</sup> n).

We now show that we can compose this majority code with a PRC for bounded-weight channels to yield a PRC for the deletion channel.

Construction 6 (PRC for deletions). Let PRC = (KeyGen, Encode, Decode) be a PRC with block length n. PRCdel[m, PRC] = (KeyGendel, Encodedel, Decodedel) is defined as follows:

- KeyGendel(1<sup>λ</sup> ): Output sk ← KeyGen(1<sup>λ</sup> ).
- Encodedel(sk, m): Output MajEncm(Encode(sk, m)).
- Decodedel(sk, z): Output Decode(sk, MajDecn(z)).

<span id="page-44-0"></span>Theorem 4. For any constants p ∈ (0, 1) and q ∈ (0, 1/2), there exists ε > 0 such that the following holds. If PRC is a PRC for 1 <sup>2</sup> − ε -bounded channels with block length n, there exists an m ∈ N, where m = Ω(n log<sup>6</sup> n), such that PRCdel[m, PRC] is a PRC for the channel BSC<sup>q</sup> ◦ BDCp.

Proof. Error correction. Let m be any message, and let x = Encode(sk, m) for sk ← KeyGen(1<sup>λ</sup> ). By pseudorandomness of PRC, x is indistinguishable from a random string in {0, 1} <sup>n</sup>. By Lemma [15,](#page-41-0) there exists ε ∈ (0, 1/2) such that

$$\Pr\_{x \leftarrow \{0, 1\}^n} \left[ \text{wt} (x \oplus \textsf{MajDec}\_n \circ BSC\_q \circ BDC\_p \circ \textsf{MajEnc}\_m (x)) \le (1/2 - \varepsilon \cdot n) \right] \ge 1 - \textsf{negl}(n).$$

Let E ′ = MajDec<sup>n</sup> ◦ BSC<sup>q</sup> ◦ BDC<sup>p</sup> ◦ MajEnc<sup>m</sup> be a channel, and observe that the above implies that E ′ is (1/2 − ε)-bounded.

Since PRC is error-correcting against (1/2 − ε)-bounded channels,

$$\Pr\_{\mathsf{sk}\leftarrow\mathsf{KeyGen}(1^{\lambda})}[\mathsf{Decode}(\mathsf{sk},\mathcal{E}'(x)) = s: x \leftarrow \mathsf{Encode}(\mathsf{sk},\mathsf{m})] \geq 1 - \mathsf{negl}(\lambda).$$

Now, we rewrite this guarantee to be in terms of PRCdel. Observe that by definition, for all m, Decodedel(sk, BSCq◦ BDCp(Encodedel(sk, m))) is distributed identically to Decode(sk, E ′ (Encode(sk, m))). Therefore,

$$\Pr\_{\mathsf{sk}\leftarrow\mathsf{KeyGen}\_{\mathsf{sk}}(1^{\lambda})}\left[\mathsf{Decode}\_{\mathsf{sk}}(\mathsf{sk},\mathrm{BSC}\_{q}\circ\mathrm{BDC}\_{p}(x))=\mathsf{m}:x\leftarrow\mathsf{Encode}\_{\mathsf{sk}}(\mathsf{sk},s)\right]\geq 1-\mathsf{negl}(\lambda).$$

We finally show that unrelated strings c decode to ⊥ under PRCdel. Let c ′ = MajDecn(c). By the analogous property for PRC,

$$\Pr\_{\mathsf{sk}\leftarrow\mathsf{KeyGen}(1^{\lambda})}[\mathsf{Decode}(\mathsf{sk},c') = \bot] \ge 1 - \mathsf{negl}(\lambda)$$

as desired.

Pseudorandomness. By pseudorandomness of PRC, its codewords are indistinguishable from random strings from {0, 1} <sup>n</sup>. Thus, let x be drawn uniformly from {0, 1} <sup>n</sup>. The distribution MajEncm(x) is uniform over {0, 1} nm because for odd m ∈ N, |{y ∈ {0, 1} <sup>m</sup> : Maj(y) = 0}| = |{y ∈ {0, 1} <sup>m</sup> : Maj(y) = 1}| = 2<sup>m</sup>−<sup>1</sup> .

### <span id="page-45-0"></span>7 Application: watermarking for language models

In this section we show that PRCs can be used to build quality-preserving (undetectable) and robust watermarks. For an overview of our approach, see either the introduction or Section [2.5.](#page-15-1)

### <span id="page-45-1"></span>7.1 Watermarking preliminaries

We follow [\[CGZ23\]](#page-62-1) in our definition of a language model. We will often refer to language models simply as models.

Definition 4. A language model Model over token set T is a deterministic algorithm that takes as input a prompt prompt and tokens previously output by the model t = (t1, . . . ,ti−1), and outputs a probability distribution p<sup>i</sup> = Model(prompt,t) over T .

We write pi(t) to denote the probability that the model outputs a token t ∈ T as specified by the distribution pi . When p<sup>i</sup> is supported on {0, 1}, we write pˆ<sup>i</sup> := E[p<sup>i</sup> ] ∈ [0, 1].

A language model Model is used to generate text as a response to a prompt by iteratively sampling from the returned distribution until a special terminating token done ∈ T is drawn. We assume an upper bound L ∗ on the length of the token sequence comprising any response.

Definition 5. A language model's response to prompt is a random variable Model(prompt) ∈ T <sup>⋆</sup> that is defined algorithmically as follows. We begin with an empty list of tokens t = (). As long as the last token in t is not done, we draw a token t<sup>i</sup> from the distribution Model(prompt,t) and append it to t. Finally, we set Model(prompt) = t.

For a probability distribution D over elements of a finite set X, we define the Shannon entropy of D as

$$H(D) = \underset{x \sim D}{\mathbb{E}}\left[ -\log D(x) \right],$$

where D(x) is the probability of x in the distribution D. The empirical entropy (also known as Shannon information or surprisal) of x in D is simply − log D(x). The expected empirical entropy of x ∼ D is exactly H(D). Intuitively, the empirical entropy of x (with respect to D) is the number of random bits that were required to draw x out of the distribution D.

<span id="page-45-2"></span>Definition 6 (Empirical entropy). For a language model Model, a prompt prompt, and a possible response t ∈ T <sup>⋆</sup> , we define the empirical entropy of Model responding with t to prompt as

$$H\_e(\mathbf{Model}, \text{PROOPT}, \mathbf{t}) := -\log \text{Pr}\left[\overline{\mathbf{Model}} \, (\text{PROOPT}) = \mathbf{t}\right].$$

We next generalize the definition of empirical entropy from whole outputs to substrings of a model's output. This will quantify how much entropy was involved in the generation of a particular contiguous substring of the output.

Definition 7. For a language model Model, a prompt prompt, a possible response t ∈ T <sup>⋆</sup> , and indices i, j ∈ [len t] with i ≤ j we define the empirical entropy on substring [i, j] of Model responding with t to prompt as

$$\begin{aligned} H\_e^{[i,j]}(\mathsf{Model}, \mathsf{PROOPT}, \mathfrak{t}) &:= -\log \Pr\left[\overline{\mathsf{Model}}\,(\mathsf{PROOPT}) \,[i:j] = \mathfrak{t}[i:j] \\ &\Big|\,\overline{\mathsf{Model}}\,(\mathsf{PROOPT}) \,[1:(i-1)] = \mathfrak{t}[1:(i-1)] \,\Big|\,. \end{aligned}$$

For convenience, in settings where the model and prompt are clear we simply write H [i,j] <sup>e</sup> (t) to mean H [i,j] <sup>e</sup> (Model, prompt,t). We sometimes write H<sup>i</sup> e := H [i,i] <sup>e</sup> to denote the empirical entropy of a single token i.

We formally define a watermarking scheme as follows.

Definition 8 (Watermarking scheme). A watermarking scheme for a model Model over T is a tuple of polynomial-time algorithms W = (Setup, Wat, Detect) where:

- Setup(1<sup>λ</sup> ) → sk outputs a secret key, with respect to a security parameter λ.
- Watsk(prompt) is a randomized algorithm that takes as input a prompt prompt and generates a response in T ⋆ .
- Detectsk(t) → {true, false} is an algorithm that takes as input a sequence t ∈ T <sup>⋆</sup> outputs true or false.

Ideally, Detectsk(t) should output true if t is generated by Watsk(prompt), and should output false if t is generated independently of sk. The former property is called completeness and the latter soundness.

Definition 9 (Soundness). A watermarking scheme W is sound if for every security parameter λ and token sequence t ∈ T <sup>⋆</sup> of length poly(λ),

$$\Pr\_{\mathsf{sk}\leftarrow\mathsf{Setup}(1^{\lambda})}[\mathsf{Detect}\_{\mathsf{sk}}(\mathsf{t})=\mathsf{true}]\leq\mathsf{negl}(\lambda).$$

Definition 10 (Completeness). A watermarking scheme W is b(L)-complete if for every security parameter λ and prompt prompt of length poly(λ),

$$\Pr\_{\mathsf{sk}\leftarrow\mathsf{Setup}(1^{\lambda})}\left[\mathsf{Detect}\_{\mathsf{sk}}(\mathsf{t})=\mathsf{falsse}\text{ and }H\_{e}\left(\mathsf{Model},\mathsf{PROOPT},\mathsf{t}\right)\geq b\left(\mathsf{len}\,\mathsf{t}\right)\right]\leq\mathsf{negl}(\lambda).$$
 $\mathsf{sk}\leftarrow\mathsf{Setup}(1^{\lambda})$  $\forall\,\mathsf{sk}\leftarrow\mathsf{Mat}\_{\mathsf{sk}}\left(\mathsf{PROOPT}\right)$ 

Definition 11 (Substring completeness). A watermarking scheme W is b(L)-substring-complete if for every prompt prompt and security parameter λ,

$$\Pr\_{\begin{subarray}{c}\mathsf{sk}\leftarrow\mathsf{Setup}(1^{\lambda})\\ \mathsf{t}\leftarrow\mathsf{Wat}\_{\mathsf{sk}}(\mathsf{PRoutput})\end{subarray}}\left[\exists\ i,L\in[\mathsf{len}\ \mathsf{t}]\ \mathsf{such that\ \mathsf{Detect}\_{\mathsf{sk}}(\mathsf{t}[i:i+L])=\mathsf{f}\mathsf{slse}$$

$$\text{and }H\_{e}^{[i:i+L]}\left(\mathsf{Model},\mathsf{PROOPT},\mathsf{t}\right)\geq b(L)\right]\leq\mathsf{negl}(\lambda).$$

If the watermarked model is indistinguishable from the un-watermarked model (and therefore perfectly quality-preserving), we say that the watermarking scheme is undetectable.

Definition 12 (Undetectability). A watermarking scheme W = (Setup, Wat, Detect) is undetectable if for every security parameter λ and all polynomial-time distinguishers D,

$$\left| \Pr[D^{\mathsf{Moded}, \overline{\mathsf{Moded}}}(1^{\lambda}) \to 1] - \Pr\_{\mathsf{sk} \leftarrow \mathsf{Setup}(1^{\lambda})} [D^{\mathsf{Moded}, \mathsf{Mat}\_{\mathsf{sk}}}(1^{\lambda}) \to 1] \right| \leq \mathsf{negl}(\lambda), \lambda$$

where the notation D<sup>O</sup>1,O<sup>2</sup> means that D is allowed to adaptively query both O<sup>1</sup> and O<sup>2</sup> with arbitrary prompts.

We also define robustness for a watermarking scheme. For robustness, the detector should be able to identify the watermark even if the text has undergone corruption by some channel E. Substring robustness says that the watermark should be robust to both cropping as well as E.

Definition 13 (Substring robustness). A watermarking scheme W = (Setup, Wat, Detect) is b(L)-substringrobust against a channel E if for every security parameter λ and prompt prompt of length poly(λ),

$$\Pr\_{\begin{subarray}{c}\mathsf{sk}\leftarrow\mathsf{Setup}(1^{\lambda})\\ \mathsf{t}\leftarrow\mathsf{Wat}\_{\mathsf{sk}}(\mathsf{rows})\end{subarray}}\left[\exists\,i,L\in[\mathsf{len}\,\mathsf{t}]\text{ such that\ \mathsf{Detect}\_{\mathsf{sk}}(\mathcal{E}(\mathsf{t}[i:i+L]))=\mathsf{false}$$

$$\text{and }H\_{\epsilon}^{[:i:i+L]}\left(\mathsf{Model},\mathsf{PROOPT},\mathsf{t}\right)\geq b(L)\right]\leq\mathsf{negl}(\lambda).$$

e

Reducing to a binary alphabet. Recall that a language model operates over an arbitrary token alphabet T . In constructing our PRC-based watermarks, it will be convenient to take T to be {0, 1}, since our pseudorandom LDPC codes have binary codewords. Prior work [\[CGZ23\]](#page-62-1) suggests a black-box transformation from any model with an arbitrary-token alphabet to a model with a binary-token alphabet, by reinterpreting the probability vectors output by the model. Here, we describe that transformation in more detail.

Let Model be any model with token alphabet T . Model, when queried with a prompt and token sequence, outputs a probability vector p ∈ [0, 1]|T |. We construct a model Model′ that has token alphabet T ′ = {0, 1}; that is, Model′ outputs probability vectors p ′ ∈ [0, 1]<sup>2</sup> . This construction will make only black-box use of Model and will ensure that there is some decoding function <sup>f</sup> converting binary outputs of Model′ into sequences of tokens from T , such that the distributions of Model and f Model′ are identical.

Let Enc : T → {0, 1} <sup>∗</sup> be any prefix-free encoding function, and let Dec : {0, 1} <sup>∗</sup> → T <sup>∗</sup> ×{0, 1} <sup>∗</sup> be the corresponding decoding function such that for any t ∈ T , Dec(Enc(t)) = (t, ⊥). Furthermore, if Dec is given as input an encoded token Enc(t) concatenated with some binary string s ∈ {0, 1} ∗ such that no prefix of s is a valid codeword, Dec outputs the token and the string; that is, Dec(Enc(t)||s) = (t, s). We will construct Model′ such that the distribution of Dec Model′ is identical to that of Model. That is, Model′ will output a binary encoding of a token sequence in T . So Model′ will compute its distribution p ′ over the next binary token by querying Model for its distribution p over T , and computing (according to p) the distribution over the next bit of the binary encoding of the next token.

Suppose that Model′ is given as input a prompt prompt and a binary token sequence (t ′ 1 , . . . ,t ′ ℓ ) ∈ {0, 1} ℓ . Model′ must now output a probability distribution over the next (binary) token, which must match Model under the appropriate transformation. Let ((t1, . . . ,ti), s) ← Dec(t ′ 1 , . . . ,t ′ ℓ ), and let p = Model(prompt,(t1, . . . ,ti)), where p ∈ [0, 1]|T | . Model′ computes p ′ as

$$\begin{aligned} \mathfrak{p}'(0) &= \sum\_{\substack{t \in \mathcal{T} \\ \mathsf{Enc}(t)[1:\mathsf{len}\ s+1] = s||0}} \mathfrak{p}(t) \\ \mathfrak{p}'(1) &= 1 - \mathfrak{p}'(0) \end{aligned} $$

where Enc(t)[1 : len s + 1] denotes the first (len s + 1) bits of Enc(t). Observe that p ′ (0) is exactly the probability that the next bit of Enc(t) is 0, where t ← p from Model, conditioned on the event that the previous bits of Enc(t) match s. Therefore, the probability that t is drawn as the next token from Model is exactly the same as the probability that Enc(t) is drawn as the next sequence of binary tokens from Model′ .

This transformation exactly preserves the empirical entropy of the response, since the distribution of Dec Model′

is identical to that of Model. However, it does reduce the rate of entropy per token, since responses from Model′ are longer. This reduction will depend on the length of codewords, and using an efficient encoding such as a Huffman encoding can help mitigate this rate reduction.

For the remainder of this paper, we assume that the token alphabet of the underlying model is binary. In practice, we can embed the watermark in a model Model with an arbitrary token alphabet T by using this transformation to compute Model′ , generating a watermarked binary response from Model′ , and transforming this response back to tokens in T using the decoding function D. This transformation preserves the undetectability of our watermark. Recall that by undetectability, the distribution of watermarked (binary) responses from Model′ is indistinguishable from the original (binary) distribution of Model′ . Let Wat denote the distribution of watermarked responses from Model′ . Since our transformation guarantees that Dec Model′ ≡ Model, we have that Dec (Wat) ≈ Model, meaning that our watermarked responses after this transformation are indistinguishable from those of the original model.

Since Model′ outputs distributions p over {0, 1}, we often specify these distributions by their expectations pˆ := E[p] ∈ [0, 1].

Remark. In our robustness theorems, we assume that the bit-errors are random. Using the above transformation, this may not be realistic because bit-errors within the representation of a given token may be correlated. We note that an alternative transformation that avoids this issue simply uses the first bit of the above representation.

### <span id="page-48-0"></span>7.2 Robust watermarking from PRCs

Watermarking schemes for language models typically embed the watermark by sampling each token with some bias. In this section, we show that using a PRC to determine this bias yields a watermarking scheme that inherits robustness from the PRC. In more detail, our watermark generator first samples a PRC codeword x ∈ {0, 1} <sup>n</sup>. It then samples each token t<sup>i</sup> ∈ {0, 1} to be biased toward x<sup>i</sup> , yielding a response that is a noisy codeword. By pseudorandomness of PRCs, this biased sampling does not noticeably change the distribution of t<sup>i</sup> in expectation over x<sup>i</sup> . Yet the detector, which knows the PRC secret key, can check if the given text is a noisy codeword to detect the watermark. Furthermore, one can use our scheme to embed an arbitrary message m in the response, by choosing x to be Encode(pk, m) under a multi-bit PRC. This yields a language model steganography scheme, since steganographic secrecy is implied by undetectability.

Our watermarking scheme can tolerate additional changes to the response depending on the robustness of the PRC used. In particular, if the PRC is robust to deletions, our scheme evades the emoji attack which succeeds against all existing undetectable watermarking schemes. Here, the attacker asks the model to answer the prompt and randomly insert an emoji in between words, then deletes the emojis. This attack succeeds because the detectors in existing schemes must be given contiguous text from the watermarked model. However, modeling this attack as a random deletion channel, our codes from Section [6.3](#page-40-0) give rise to watermarking schemes that are robust to this attack.

Construction 7 (Watermark from PRCs). Let PRC be a PRC of block length n with security parameter λ. W[PRC] = (Setup, Wat, Detect) is the watermarking scheme whose algorithms are specified in Figure [3.](#page-49-0)

Remark. In Algorithm [3,](#page-49-1) we specify the detector to do a brute-force search over O(Ln) index pairs to find the start and end locations of the perturbed codeword, since deletions may change its length. If the perturbed codeword length is known, e.g., when one wants robustness only to substitutions, one can use a more efficient detector that searches only over O(L) indices to find the start location of the codeword.

Recall that we write pˆ for the expectation E[p] of a distribution p over {0, 1}.

Soundness and undetectability We first show that W[PRC] is sound and undetectable, which follows quickly from pseudorandomness and error correction of PRCs.

<span id="page-48-1"></span>Lemma 18 (Soundness). W[PRC] is sound.

Proof. Let t ∈ T <sup>∗</sup> be any token sequence of length (len t) ≤ poly(λ). Detectsk(t) iterates over all i ∈ [len t], j ∈ [i, min{i + n − 1, len t}], checks if PRC.Decode(PRC.sk,(t<sup>i</sup> , . . . ,t<sup>j</sup> ) ⊕ aℓ) = 1 for any i, j, ℓ, and outputs true if so. Recall that the error correction of PRC ensures that for any c ∈ Σ <sup>∗</sup> = T ∗ ,

$$\Pr\_{\mathsf{PRC.sh}\leftarrow\mathsf{PRC.KeyGen}(1^{\lambda})}[\mathsf{Decode}(\mathsf{PRC.sk}, c) \neq \bot] \leq \mathsf{negl}(\lambda).$$

Setting c<sup>i</sup> = (t<sup>i</sup> , . . . ,t<sup>j</sup> ) ⊕ a<sup>ℓ</sup> for each i, j, ℓ, the probability that Decode returns 1 for any c<sup>i</sup> is negligible by a union bound. Consequently, the probability over choice of sk that Detectsk outputs true is negligible.

<span id="page-48-2"></span>Lemma 19 (Undetectability). W[PRC] is undetectable.

Proof. We prove that if the output of Encode is replaced with uniform randomness, this watermark is undetectable. It then follows from pseudorandomness of the PRC that the actual watermark is undetectable.

<span id="page-49-0"></span>Algorithm 1: Watermark setup procedure Setup(1<sup>λ</sup> )

Input: A security parameter λ Result: A watermark key sk

<sup>1</sup> PRC.sk ← PRC.KeyGen(1<sup>λ</sup> );

<sup>2</sup> a1, . . . , a⌈ L∗ ⌉ ← {0, 1} n;

n

<sup>3</sup> return sk = PRC.sk,(a1, . . . , a⌈ L∗ n ⌉ ) 

#### Algorithm 2: Watermarked text generator Watsk

;

```
Input: A prompt (prompt) and a key sk
   Result: Watermarked text t1, . . . ,tL
 1 (PRC.sk, a) ← sk;
 2 x ← PRC.Encode(PRC.sk) ⊕ a1;
 3 i := 1;
 4 j := 1;
 5 while done ∈ { / t1, . . . ,ti−1} do
 6 pi
         := Model(prompt,t1, . . . ,ti−1);
 7 ti ← Ber(pˆi − (−1)xj
                           · min{pˆi
                                   , 1 − pˆi});
 8 i ← i + 1;
 9 j ← j + 1;
10 if j > n then
         // Re-sample from the PRC
11 x ← PRC.Encode(PRC.sk) ⊕ a⌈
                                        i
                                       n
                                         ⌉
                                          ;
12 j ← 1;
13 return t1, . . . ,tL;
```
#### Algorithm 3: Watermark detector Detectsk

<span id="page-49-1"></span>Input: Text t1, . . . ,t<sup>L</sup> and watermark key sk Result: true or false <sup>1</sup> (PRC.sk, a) ← sk; <sup>2</sup> for i ∈ [L], j ∈ [i, min{i + n − 1, L}], ℓ ∈ h ⌈ L ∗ n ⌉ i do <sup>3</sup> if PRC.Decode(PRC.sk,(t<sup>i</sup> , . . . ,t<sup>j</sup> ) ⊕ aℓ) ̸= ⊥ then <sup>4</sup> return true; <sup>5</sup> return false;

Figure 3: The algorithms (Setup, Wat, Detect) of W[PRC].

We begin by showing that if x<sup>j</sup> ← Ber( <sup>1</sup> 2 ), then Pr[t<sup>i</sup> = 1] = pˆ<sup>i</sup> , where t<sup>i</sup> ← Ber(pˆ<sup>i</sup> −(−1)x<sup>j</sup> ·min{pˆ<sup>i</sup> , 1−pˆi}). Suppose first that min{pˆ<sup>i</sup> , 1 − pˆi} = pˆ<sup>i</sup> . Then

$$
\left\{\hat{\mathfrak{p}}\_i - (-1)^{x\_j} \cdot \min\{\hat{\mathfrak{p}}\_i, 1 - \hat{\mathfrak{p}}\_i\} \right\} = \begin{cases} 0 & \text{if } x\_j = 0 \\ 2\hat{\mathfrak{p}}\_i & \text{if } x\_j = 1 \end{cases}
$$

so Prx<sup>j</sup> [t<sup>i</sup> = 1] = <sup>1</sup> 2 · 0 + <sup>1</sup> 2 · 2pˆ<sup>i</sup> = pˆ<sup>i</sup> . Now, suppose that min{pˆ<sup>i</sup> , 1 − pˆi} = 1 − pˆ<sup>i</sup> Then

$$\left\| \left\| \right\| - (-1)^{x\_j} \cdot \min \{ \left\| \right\|, 1 - \left\| \right\| \right\} = \begin{cases} 2\left\| \right\| - 1 & \text{if } x\_j = 0 \\ 1 & \text{if } x\_j = 1 \end{cases}$$

so Prx<sup>j</sup> [t<sup>i</sup> = 1] = <sup>1</sup> 2 · (2pˆ<sup>i</sup> − 1) + <sup>1</sup> 2 · 1 = pˆ<sup>i</sup> . Therefore, if the x<sup>j</sup> 's are independent Ber( <sup>1</sup> 2 ), the distribution of every t<sup>i</sup> under the watermark is identical to its distribution under the original model.

Suppose for the sake of contradiction that W is not undetectable; that is, there is a polynomial-time distinguisher D such that for some constant c > 0,

$$\left| \Pr[D^{\mathsf{Moded}, \overline{\mathsf{Moded}}}(1^{\lambda}) \to 1] - \Pr\_{\mathsf{sk} \leftarrow \mathsf{Setup}(1^{\lambda})} [D^{\mathsf{Moded}, \mathsf{Wat}\_{\mathsf{sk}}}(1^{\lambda}) \to 1] \right| \geq \frac{1}{\lambda^c}.$$

We'll construct an adversary A that uses D to break pseudorandomness of PRC. Recall that in the PRC pseudorandomness experiment, A has access to O, which is either an oracle for Encode(PRC.sk, ·) or the uniform distribution U, and its goal is to distinguish between these two cases. A interacts with D and simulates D's oracle O2, which is either Model or Watsk. When D queries a prompt prompt to O2, A returns a response according to Algorithm [2,](#page-49-2) with one key modification: It draws each x by querying its oracle O. If O is Encode(PRC.sk), the responses returned by A are exactly those of Watsk. By our earlier observation that if the x<sup>j</sup> 's are uniform, the t<sup>i</sup> 's distributions are unchanged, if O is U the responses returned by A are exactly those of Model. Therefore, if we set A to output 1 if and only if D outputs 1, we have that

$$\left| \Pr\_{\left( (\mathsf{PRC.sk}) \leftarrow \mathsf{KeyGen}(1^{\lambda}) \right)} \left[ \mathcal{A}^{\mathsf{Encode}(\mathsf{PRC.sk}, \cdot)}(1^{\lambda}) = 1 \right] - \Pr\_{\mathcal{U}} [\mathcal{A}^{\mathcal{U}}(1^{\lambda}) = 1] \right| \geq \frac{1}{\lambda^{c}},$$

contradicting pseudorandomness of the PRC.

Robustness of our scheme In the watermarked text generator (Algorithm [2\)](#page-49-2), we embed a PRC output r into the model's response to a prompt prompt by sampling t<sup>i</sup> from Ber(pˆ<sup>i</sup> − (−1)<sup>x</sup><sup>j</sup> · min{pˆ<sup>i</sup> , 1 − pˆi}). Observe that if pˆ<sup>i</sup> = 1 2 , this is equal to Ber(x<sup>j</sup> ), so t<sup>i</sup> will always equal x<sup>j</sup> . If pˆ<sup>i</sup> ̸= 1 2 , then t<sup>i</sup> is sampled with bias toward x<sup>j</sup> , but it sometimes will not equal x<sup>j</sup> . One can think of this embedding process as taking as input x, applying some random error, and returning the noisy response x as output.

We model this process as an embedding channel EEmb : {0, 1} <sup>n</sup> → {0, 1} <sup>n</sup>, where for x ← {0, 1} <sup>n</sup>, EEmb(x) ∼ Model(prompt)[i : i + n − 1] (i.e., the n bits of the watermarked model's response to prompt where x is embedded). For ease of notation, we write t ← EEmb(x), leaving prompt and the index i implicit. We will show that EEmb introduces a bounded number of errors when the text has non-zero entropy.

The relevant notion of entropy is the empirical entropy (Definition [6\)](#page-45-2). We will also make use of the truncated empirical entropy H¯ <sup>e</sup>, which is defined as follows. For a model output t (given some prompt that we leave implicit), H¯ <sup>e</sup>(t) = P <sup>i</sup>∈len <sup>t</sup> min{1, H<sup>i</sup> e (t)}. As with empirical entropy, we define truncated empirical entropy for partial responses: H¯ e [i,j] (t) = P<sup>j</sup> <sup>ℓ</sup>=<sup>i</sup> min{1, H<sup>ℓ</sup> e (t)}, and H¯ e i (t) = min{1, H<sup>i</sup> e (t)}.

<span id="page-50-0"></span>Lemma 20. For any c > 0 and any indices a, b ∈ N where a ≤ b,

$$\Pr\_{\mathbf{t}\leftarrow\mathsf{Model}}\left[H\_e^{[a,b]}(\mathbf{t}) > c \cdot (b-a) \text{ and } H\_e^{\ [a,b]}(\mathbf{t}) \le \frac{c^2}{2}(b-a)\right] \le \mathsf{negl}(b-a).$$

Proof. We will show that with probability 1 − negl(b − a) over t ← Model,

$$\sum\_{i=a}^{b} \left( \frac{H\_e^i(\mathbf{t})}{\bar{H}\_e^{\ i}(\mathbf{t})} \right)^2 \le 2(b-a).$$

By the Cauchy-Schwarz inequality, we have

X b i=a Hi e (t) ≤ vuutX b i=a H<sup>i</sup> e (t) H¯ e i (t) !2 · vuutX b i=a H¯ e i (t) 2.

Combining these two inequalities, it will follow that with probability 1−negl(b − a) if P<sup>b</sup> <sup>i</sup>=<sup>a</sup> H<sup>i</sup> e (t) ≥ c·(b−a) then

$$\begin{split} \sum\_{i=a}^{b} \left( \bar{H}\_e^{\ i} \mathbf{(t)} \right)^2 &\geq \left( \sum\_{i=a}^{b} H\_e^i \mathbf{(t)} \right)^2 \left( \sum\_{i=a}^{b} \left( \frac{H\_e^i \mathbf{(t)}}{\bar{H}\_e^{\ i} \mathbf{(t)}} \right)^2 \right)^{-1} \\ &\geq \frac{c^2 \cdot (b-a)^2}{2(b-a)} \\ &= \frac{c^2}{2} (b-a) . \end{split}$$

And since H¯ e i (t) ≤ 1 by definition, H¯ e i (t) ≥ H¯ e i (t) 2 for every i, and P<sup>b</sup> <sup>i</sup>=<sup>a</sup> <sup>H</sup>¯ e i (t) ≥ c 2 2 (b − a) as desired.

It remains to show that with overwhelming probability, P<sup>b</sup> i=a H<sup>i</sup> e (t) H¯<sup>e</sup> i (t) 2 ≤ 2(b − a). For i ∈ [a, b], let X<sup>i</sup> := (H<sup>i</sup> e (t)/H¯ e i (t))<sup>2</sup> and q<sup>i</sup> := min{pi(0), pi(1)}. If q<sup>i</sup> ≥ 1/e, X<sup>i</sup> = 1; if q<sup>i</sup> < 1/e then

$$X\_i = \begin{cases} 1 & \text{w.p. } 1 - \mathfrak{q}\_i \\ \ln^2 \mathfrak{q}\_i & \text{w.p. } \mathfrak{q}\_i \end{cases}$$

and E[X<sup>i</sup> | ta, . . . ,ti−1] = 1 − q<sup>i</sup> + q<sup>i</sup> ln<sup>2</sup> q<sup>i</sup> ≤ 3/2. For any fixed ta, . . . ,ti−1,

$$\Pr\_{\mathbf{t}\_i \leftarrow \mathbf{p}\_i}[X\_i \ge \ln^4(b-a)] = \mathbf{q}\_i \cdot \mathbb{1}[\mathbf{q}\_i \le e^{-\ln^2(b-a)}] \le e^{-\ln^2(b-a)}.$$

By a union bound, Pr[∃i ∈ [a, b] s.t. X<sup>i</sup> ≥ ln<sup>4</sup> (b − a)] = negl(b − a).

Let Za−<sup>1</sup> = 0 and for i ∈ [a, b] let Z<sup>i</sup> = Zi−<sup>1</sup> + X<sup>i</sup> − (1 − q<sup>i</sup> + q<sup>i</sup> ln<sup>2</sup> qi). Observe that Za, . . . , Z<sup>b</sup> is a martingale with respect to ta, . . . ,tb. Since the differences |Z<sup>i</sup> − Zi−1| are bounded by ln<sup>4</sup> (b − a) with probability 1 − negl(b − a), Azuma's inequality (Lemma [1\)](#page-20-3) implies that

$$\Pr[Z\_b > (b-a)/2] \le \exp\left(\frac{-(b-a)}{8\ln^8(b-a)}\right) + \text{negl}(b-a) \le \text{negl}(b-a).$$

Since Z<sup>b</sup> = P<sup>b</sup> i=a [X<sup>i</sup> − (1 − q<sup>i</sup> + q<sup>i</sup> ln<sup>2</sup> qi)] ≥ P<sup>b</sup> <sup>i</sup>=<sup>a</sup> X<sup>i</sup> − 3 2 (b − a), it follows that

$$\Pr\left[\sum\_{i=a}^{b} X\_i > 2(b-a)\right] \le \text{negl}(b-a). \tag{7}$$

<span id="page-51-0"></span>We show in the following lemma that the embedding channel introduces bounded-weight errors into any contiguous substring of a response with sufficient empirical entropy.

Lemma 21 (Entropy and EEmb). Let κ > 0 be any constant, and let a, b ∈ N be indices such that b = a + ⌈κn⌉ − 1. For the embedding channel EEmb of our watermarked model,

$$\Pr\_{\begin{subarray}{c}\mathsf{x}\leftarrow\{0,1\}^{\mathsf{len}}\rightarrow\mathsf{x}\end{subarray}}\left[\begin{array}{c}\mathsf{wt}(\mathsf{t}\ominus x)>\left(\frac{1}{2}-\frac{c^{2}}{16}\right)\cdot\mathsf{len}\ \mathsf{t}\ \mathit{and}\ \mathit{H}\_{\mathsf{e}}^{[a,b]}(\mathsf{t}')>\mathsf{c}\cdot\mathsf{len}\ \mathsf{t}\ \mathit{i}\ \mathsf{t}'\leftarrow\mathcal{E}\_{\mathsf{Emb}}(x)\\\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\mathrm{Im}(\begin{array}{c}\mathsf{x}\ \mathit{i}'\rightarrow\mathit{j}\ \mathit{x}\ \mathit{i}'\end{array})\right]$$

Proof. For ease of notation, in this proof we use pi(ˆti) to denote the probability that the model outputs a bit ˆt<sup>i</sup> ∈ {0, 1} as the next (a + i) th token given that it has output tokens t ′ [: a + i − 1] so far. We also let He(t) denote H [a,b] <sup>e</sup> (t ′ ) and H¯ <sup>e</sup>(t) denote H¯ e [a,b] (t ′ ).

For each i ∈ len t, recall that the watermark samples t<sup>i</sup> ← Ber(pˆi−(−1)x<sup>i</sup> ·min{pˆ<sup>i</sup> , 1−pˆi}), and for ˆt<sup>i</sup> ∈ {0, 1}, Prxi←{0,1}[t<sup>i</sup> = ˆt<sup>i</sup> ] = pi(ˆti).

For fixed ˆt<sup>i</sup> ∈ {0, 1}, we have

$$\begin{split} \frac{\Pr[\mathbf{t}\_{i} = \hat{\mathbf{t}}\_{i} \mid x\_{i} = \hat{\mathbf{t}}\_{i}]}{2} &= \Pr[x\_{i} = \hat{\mathbf{t}}\_{i} \text{ and } \mathbf{t}\_{i} = \hat{\mathbf{t}}\_{i}] \\ &= \Pr[\mathbf{t}\_{i} = \hat{\mathbf{t}}\_{i}] \cdot \Pr[x\_{i} = \hat{\mathbf{t}}\_{i} \mid \mathbf{t}\_{i} = \hat{\mathbf{t}}\_{i}] \\ &= \mathbf{p}\_{i}(\hat{\mathbf{t}}\_{i}) \cdot \Pr[x\_{i} = \hat{\mathbf{t}}\_{i} \mid \mathbf{t}\_{i} = \hat{\mathbf{t}}\_{i}]. \end{split}$$

]

Because t<sup>i</sup> is distributed as Ber(pˆ<sup>i</sup> − (−1)<sup>x</sup><sup>i</sup> · min{pˆ<sup>i</sup> , 1 − pˆi}) = Ber(pˆ<sup>i</sup> − (−1)<sup>x</sup><sup>i</sup> · min{pˆ<sup>i</sup> , 1 − pˆi}), we also have

$$\Pr[\mathbf{t}\_i = \hat{\mathbf{t}}\_i \mid x\_i = \hat{\mathbf{t}}\_i] = \mathfrak{p}\_i(\hat{\mathbf{t}}\_i) + \min\{\mathfrak{p}\_i(\hat{\mathbf{t}}\_i), 1 - \mathfrak{p}\_i(\hat{\mathbf{t}}\_i)\}.$$

Therefore,

$$\begin{aligned} \Pr[x\_i = \hat{\mathbf{t}}\_i \mid \mathbf{t}\_i = \hat{\mathbf{t}}\_i] &= \frac{1}{2} + \frac{1}{2} \min\left\{1, \frac{1}{\mathbf{p}\_i(\hat{\mathbf{t}}\_i)} - 1\right\} \\ &\geq \frac{1}{2} + \frac{1}{2} \min\left\{1, -\ln \mathbf{p}\_i(\hat{\mathbf{t}}\_i)\right\} \end{aligned}$$

where for the inequality we have used the fact that ln z ≥ 1 − 1/z for z > 0.

Let Y1, . . . , Ylen <sup>t</sup> be Bernoulli random variables where Y<sup>i</sup> = 1 if and only if x<sup>i</sup> = ˆt<sup>i</sup> . The expected number of correct bits given that t = ˆt is

$$\begin{split} \mathbb{E}\left[\sum\_{i=1}^{\text{len}} Y\_i \; \middle| \; \mathbf{t} = \hat{\mathbf{t}} \right] &= \sum\_{i=1}^{\text{len}} \Pr[Y\_i \; | \; \mathbf{t}\_i = \hat{\mathbf{t}}\_i] \\ &\geq \frac{\text{len} \; \mathbf{t}}{2} + \frac{1}{2} \sum\_{i=1}^{\text{len}} \min\{1, -\ln \mathsf{p}\_i(\hat{\mathbf{t}}\_i) \} \\ &\geq \frac{\text{len} \; \mathbf{t}}{2} + \frac{\ln 2}{2} \sum\_{i=1}^{\text{len}} \min\{1, -\log \mathsf{p}\_i(\hat{\mathbf{t}}\_i) \} \\ &\geq \frac{\text{len} \; \mathbf{t}}{2} + \frac{1}{4} H\_e(\mathbf{t}). \end{split}$$

By Lemma [20,](#page-50-0) if <sup>H</sup>e(t) > c · len <sup>t</sup>, this is at least 1 <sup>2</sup> + c 2 8 len t. Since the events x<sup>i</sup> = ˆt<sup>i</sup> are independent for fixed ˆt<sup>i</sup> , we can apply a Chernoff bound to see that wt(x⊕t) ≤ 1 <sup>2</sup> − c 2 16 ·len t with probability 1−negl(n).

In the following proofs of substring-completeness and substring-robustness, it will be useful to consider the model's response as consisting of blocks. A block is a contiguous substring of the response where a PRC codeword was embedded. More formally, recall that the generator Watsk first chooses a PRC codeword of length n that corresponds to the first n tokens of the response, (t1, . . . ,tn), and applies a one-time pad a1. It then chooses a new PRC codeword for the next n tokens of the response and applies a fresh one-time pad, continuing to do so until it terminates, having output the final response t1, . . . ,tcn+<sup>i</sup> for some c, i ∈ Z≥0. This response consists of (c − 1) full blocks (t1, . . . ,tn), . . . ,(t(c−1)n+1, . . . ,tcn). It also consists of a possibly incomplete block, (tcn+1, . . . ,tcn+i). The substring tn−1, . . . ,t2n+2 of this response consists of two incomplete blocks: (tn−1,tn) and (t2n+1,t2n+2), and one full block: (tn+1, . . . ,t2n).

<span id="page-53-0"></span>Lemma 22 (Substring completeness). Let ε > 0 be any constant. If PRC is a zero-bit PRC with block length <sup>n</sup> and robustness to every (1/2−ε)-bounded channel, then <sup>W</sup>[PRC] is (4<sup>√</sup> <sup>ε</sup> ·L+ 2<sup>√</sup> 2 ·n)-substring-complete.

Proof. Let t ← Watsk(prompt) be a watermarked response for some arbitrary prompt prompt, and let t ′ be a length-L contiguous substring of t, where He(t ′ ) ≥ 4 √ <sup>ε</sup> · <sup>L</sup> + 2<sup>√</sup> 2 · n.

The start and end of t ′ may be part of incomplete blocks, with some number of full blocks in between. Recall that the truncated empirical entropy of any single-bit distribution is at most 1, so each of these possibly-incomplete blocks contains at most n truncated empirical entropy. Consider padding these possiblyincomplete blocks, appending deterministic bits so they are each of length n but have the same truncated empirical entropy. It now follows from Lemma [20](#page-50-0) that with overwhelming probability in the length of these blocks (which is now n), they each have at most n √ 2 empirical entropy. The full blocks therefore contain at least 4<sup>√</sup> ε · L empirical entropy.

By an averaging argument, t ′ must contain some full block ˜t ⊆ t ′ with at least 4<sup>√</sup> ε · n empirical entropy. By Lemma [21,](#page-51-0) the embedding channel applied to this block is (1/2 − ε)-bounded. Furthermore, because of the one-time pads, these channels' errors do not depend on other codewords. Since the PRC used is robust against such bounded channels, the detector will see that PRC.Decode(PRC.sk,˜t ⊕ αℓ) ̸= ⊥ for some ℓ and output true.

<span id="page-53-2"></span>Lemma 23 (Substring-robustness against substitutions). Let ε, δ > 0 be any constants. If PRC is a zero-bit PRC with block length <sup>n</sup> and robustness to every (1/<sup>2</sup> <sup>−</sup> <sup>ε</sup> · <sup>δ</sup>)-bounded channel, then <sup>W</sup>[PRC] is (4<sup>√</sup> ε · L + 2 √ 2 · n)-substring-robust against BSC1/2−δ.

Proof. As in the proof of Lemma [22,](#page-53-0) the decoder receives the output of the composition of the error channel and embedding channel on the sufficiently high-entropy block. The embedding channel is again (1/2 − ε) bounded on this block by Lemma [21.](#page-51-0) Therefore, the composition of the error channel BSC1/2−<sup>δ</sup> with the embedding channel has expected error rate

$$(1/2 - \delta) \cdot (1/2 + \varepsilon) + (1/2 - \varepsilon) \cdot (1/2 + \delta) = \frac{1}{2} - 2\varepsilon \cdot \delta$$

and is in particular (1/2 − ε · δ)-bounded. Since PRC is robust to such channels, it follows that W[PRC] is (4√ <sup>ε</sup> · <sup>L</sup> + 2<sup>√</sup> 2 · n)-substring-robust against BSC1/2−δ.

We showed above that when a substring t ′ of a response has at least 4<sup>√</sup> ε·t ′ empirical entropy, the embedding channel EEmb applied to some block in that substring is 1 <sup>2</sup> − ε -bounded. For the following theorem, we need to assume something further about EEmb: restricted to that block in the substring, EEmb is equal to BSC<sup>α</sup>(ε) for some α(ε) ∈ 0, 1 <sup>2</sup> − ε .

<span id="page-53-1"></span>Assumption 4. There is a function α : [0, 1/2) → [0, 1/2) such that for any constant ε ∈ [0, 1/2), if a response substring of length <sup>L</sup> has at least (4<sup>√</sup> <sup>ε</sup> ·<sup>L</sup> + 2<sup>√</sup> 2 · n) empirical entropy, the embedding channel can be modeled as BSC<sup>α</sup>(ε) .

As noted in the remark at the end of Section [7.1,](#page-45-1) this assumption is not realistic if we use the standard transformation from tokens to bits because the bit-errors within the representation of a given token may be correlated. However, an alternative transformation that avoids this issue simply uses one bit for each token. In this case, Assumption [4](#page-53-1) roughly states that the entropy is spread throughout the substring, and that the substring does not repeat too many tokens.

<span id="page-54-5"></span>Lemma 24 (Substring-robustness against deletions). Suppose that Assumption [4](#page-53-1) holds with function α. Let ε > 0, q ∈ (0, 1/2), and p ∈ (0, 1) be any constants. If PRCdel is a zero-bit PRC with block length n and robustness to BDC<sup>p</sup> ◦ BSC<sup>q</sup> ◦ BSCα(ε) = BDC<sup>p</sup> ◦ BSCq+α(ε)−q·α(ε) , then <sup>W</sup>[PRCdel] is (4<sup>√</sup> <sup>ε</sup> · <sup>L</sup> + 2<sup>√</sup> 2 · n) substring-robust against BDC<sup>p</sup> ◦ BSCq.

Proof. Consider the block of the response over which EEmb is equivalent to BSCα(ε) . The decoder receives the output of the composition of the error channel BDC<sup>p</sup> ◦ BSC<sup>q</sup> and embedding channel BSCα(ε) applied to the codeword used in this block. The composition of these channels is BDC<sup>p</sup> ◦ BSC<sup>q</sup> ◦ BSCα(ε) , which PRCdel is robust to.

Therefore, the detector of W[PRCdel] will output true when it runs Decode on this block of the response.

<span id="page-54-2"></span>By applying the PRCs of Theorems [1](#page-30-1) and [2](#page-36-0) to Lemmas [23](#page-53-2) and [24,](#page-54-5) we obtain the following results.

Theorem 5. Let δ > 0 be any constant and n be a security parameter. Under Assumption [1,](#page-28-1) there exists a language model watermarking scheme that is O(L + n)-substring-robust against BSC1/2−δ.

<span id="page-54-3"></span>Theorem 6. Suppose that Assumption [4](#page-53-1) holds with function α, let q ∈ (0, 1/2) and p ∈ (0, 1) be any constants, and let n be a security parameter. Under Assumption [1,](#page-28-1) there exists a language model watermarking scheme that is O(L + n)-substring-robust against BDC<sup>p</sup> ◦ BSCq.

We remark that although we state our theorems for error rates in (0, 1/2) for convenience, one can easily extend these schemes to error rates for arbitrary constants in (0, 1) \ {1/2}.

### <span id="page-54-0"></span>7.3 Language model steganography

We have proven completeness, robustness, soundness, and undetectability of W, where the random strings x used in Watsk were computed as PRC.Encode(PRC.sk). These proofs relied only on our ability to distinguish PRC codewords from unrelated strings, so it sufficed to use a zero-bit PRC. Of course, one could obtain a multi-bit watermarking scheme by replacing PRC.Encode(PRC.sk) with PRC′ .Encode(PRC′ .sk, m) for any message m, using PRC′ which is multi-bit and has the same robustness as PRC. Lemmas [23](#page-53-2) and [24](#page-54-5) both apply identically in this case. This yields a robust language model steganography scheme, where steganographic secrecy is implied by undetectability of W[PRC′ ]. This steganography scheme has the same robustness as the watermarking scheme.

<span id="page-54-4"></span>Applying this observation and using the constant-rate PRCs of Section [6.2,](#page-39-0) we obtain the following result.

Theorem 7. Let δ > 0 be any constant and n be a security parameter. Under Assumption [1,](#page-28-1) there exists a language model steganography scheme that is O(L + n)-substring-robust against BSC1/2−δ.

In Section [7.4,](#page-54-1) we will see how this observation about encoding arbitrary messages can be used to build watermarks with public attribution. Since the proofs of security and robustness of the language model steganography scheme are completely identical to those for the watermarking scheme W[PRC], we do not formally prove them separately. However, in Section [8](#page-58-0) we show that PRCs can be used for universal steganography (which is more general than language model steganography).

### <span id="page-54-1"></span>7.4 Watermarks with public attribution

See Section [2.6](#page-17-0) for a description of publicly attributable watermarks.

We define public attribution in terms of a function called AttrText. Recall that we intentionally design this function to not be robust. AttrText, given a text t and a public detection key, outputs a pair (t ′ , b), where b ∈ {true, false} indicates whether t contains verbatim a significant prefix of text output by the model, and if so, t ′ is that prefix. Although AttrText is intentionally not robust, our scheme's Detect function retains all properties (undetectability, robustness, soundness) of our standard watermarks.

Algorithms [3](#page-49-1) to [6,](#page-56-0) given in Figure [4,](#page-56-1) comprise a watermarking scheme with unforgeable public attribution from any secret-key PRC and any digital signature scheme.

The watermarked text generator of Watt (Algorithm [5\)](#page-56-2) is exactly the same as that of W (Algorithm [2\)](#page-49-2), but x is now generated as the output of PRC.Encode on specific messages. In particular, the first x is sampled as PRC.Encode(sk), and every subsequent x is the encoding of a signature on the response output thus far.

Definition 14 (Unforgeable public attribution). A watermarking scheme Watt for a model Model has b(L) unforgeable public attribution if there is a function AttrTextpk(t) satisfying:

- (Syntax): AttrTextpk(t) → (t ′ , b) takes in a token sequence t and outputs a (token sequence, boolean) pair. b = true indicates that a prefix of t was output verbatim by the model; the corresponding t ′ that it outputs is this prefix. b = false indicates that no sufficiently long prefix of t was output verbatim by the model; in this case t ′ = ⊥.
- (b(L) public attribution): For every security parameter λ and prompt prompt of length poly(λ),

$$\Pr\_{\begin{subarray}{c}\mathsf{pk},\mathsf{sk}\leftarrow\mathsf{Setup}(1^{\lambda})\\ \mathsf{t}\leftarrow\mathsf{Wat}\_{\mathsf{sk}}(\mathsf{ROOPT})\end{subarray}}\left[\exists\,i,L\in[\mathsf{len}\,\mathsf{t}]\text{ such that }\mathsf{len}\,\mathsf{t}'
$$H\_{e}^{[i:i+L]}\left(\mathsf{Model},\mathsf{PROOPT},\mathsf{t}\right)\geq b\left(L\right)\mid\left(\mathsf{t}',\mathsf{b}\right)\leftarrow\mathsf{Attr}\mathsf{Text}\_{\mathsf{pk}}(\mathsf{t})\right]\leq\mathsf{negl}(\lambda).$$
$$

• (Unforgeability): For all polynomial-time adversaries A,

$$\Pr[\mathsf{AttrForge}\_{\mathcal{A},\mathcal{W}\_{\mathsf{att}}}(\lambda) = 1] \le \mathsf{negl}(\lambda),$$

where the AttrForge experiment is given in Figure [5.](#page-57-1)

Construction 8 (Watermark with public attribution). Let Sig be a digital signature scheme with signatures of length n, and let PRC be a PRC of block length n. Watt[PRC] is the watermarking scheme whose algorithms are specified in Figure [4.](#page-56-1) Its detector is the same as that of W[PRC].

<span id="page-55-0"></span>Lemma 25 (Unforgeability). Watt[PRC] is unforgeable if the underlying signature scheme is unforgeable.

Proof. Suppose there exists an adversary A that wins AttrForge<sup>A</sup>,Watt (λ) with non-negligible probability. We construct B that uses A to break unforgeability of the underlying signature scheme Sig. B acts as the challenger in AttrForge<sup>A</sup>,Watt (λ). It receives the signature public key Sig.pk used in Watt from its own challenger for SigForge<sup>B</sup>,Sig. B generates the other parameters for Watt (that is, the PRC parameters) itself. Let pk denote the resulting public key of the watermarking scheme; B passes A pk as input. When responding to A's queries to Watsk, B generates the necessary signature using its signing oracle in SigForge<sup>B</sup>,Sig. Notice that every query that B makes to its signing oracle is a contiguous substring of some response t ∈ Q, where Q is the set of responses returned to A by Watsk. At the end of AttrForge<sup>A</sup>,Watt (λ), A outputs t ∗ . B computes (m, b) ← AttrText(pk,t ∗ ); if b = true, B outputs the corresponding m and verifying signature σ.

Recall that if A wins, it outputs t ∗ such that (m, b) ← AttrText(pk,t ∗ ) where b = true and m is not a contiguous substring of any response in Q. Since every query made by B to its signing oracle was a substring of some response in Q, B did not query this m. However, B is able to output a verifying signature for m, so B wins SigForge<sup>B</sup>,Sig.

<span id="page-55-1"></span>Lemma 26 (Public attribution). Let ε > 0 be any constant. If PRC has block length n and is robust to 1 <sup>2</sup> − ε -bounded channels, then <sup>W</sup>att[PRC] satisfies (4<sup>√</sup> <sup>ε</sup> · <sup>L</sup> + 2<sup>√</sup> 2 · n) public attribution.

<span id="page-56-1"></span>Algorithm 4: Publicly attributable watermark setup procedure Setup(1<sup>λ</sup> )

Input: A security parameter λ. Result: A watermark public key pk and secret key sk <sup>1</sup> PRC.sk ← PRC.KeyGen(1<sup>λ</sup> ); <sup>2</sup> Sig.pk, Sig.sk ← Sig.KeyGen(1<sup>λ</sup> ); <sup>3</sup> a1, . . . , a⌈ L∗ n ⌉ ← {0, 1} n; <sup>4</sup> pk ← PRC.sk, Sig.pk,(a1, . . . , a⌈ L∗ n ⌉ ) ; <sup>5</sup> sk ← Sig.sk;

<sup>6</sup> return pk,sk;

Algorithm 5: Publicly attributable watermarked text generator Watsk

<span id="page-56-2"></span>Input: A prompt (prompt), a watermark public key pk = PRC.sk, Sig.pk,(a1, . . . , a⌈ L∗ n ⌉ ) , and a watermark secret key sk = Sig.sk. Result: Watermarked text t1, . . . ,t<sup>L</sup> <sup>1</sup> (PRC.sk, Sig.pk, a) ← pk; <sup>2</sup> x ← PRC.Encode(PRC.sk) ⊕ a1; <sup>3</sup> i := 1, j := 1; <sup>4</sup> while done ∈ { / t1, . . . ,ti−1} do // Embed the current message if first block, or signature otherwise <sup>5</sup> p<sup>i</sup> := Model(prompt,t1, . . . ,ti−1); <sup>6</sup> t<sup>i</sup> ← Ber(pˆ<sup>i</sup> − (−1)<sup>x</sup><sup>j</sup> · min{pˆ<sup>i</sup> , 1 − pˆi}); <sup>7</sup> i ← i + 1, j ← j + 1; // If done embedding the current codeword, generate a new signature <sup>8</sup> if j > n then <sup>9</sup> m ← t1, . . . ,t<sup>i</sup> ; <sup>10</sup> σ ← SignSig.sk(m); <sup>11</sup> x ← PRC.Encode(PRC.sk, σ) ⊕ a⌈ i n ⌉ ; <sup>12</sup> j ← 1; <sup>13</sup> return t1, . . . ,tL;

Algorithm 6: Publicly attributable watermarked text attributor AttrTextpk

<span id="page-56-0"></span>Input: Text t1, . . . ,t<sup>L</sup> and a watermark public key pk = PRC.sk, Sig.pk,(a1, . . . , a⌈ L∗ n ⌉ ) . Result: true or false <sup>1</sup> (PRC.sk, Sig.pk, a) ← pk; <sup>2</sup> for i ∈ [L − n + 1], ℓ ∈ h ⌈ L ∗ n ⌉ i do <sup>3</sup> m ← t1, . . . ,ti−1; <sup>4</sup> σ ← PRC.Decode(PRC.sk,(t<sup>i</sup> , . . . ,t<sup>i</sup>+n−1) ⊕ aℓ); <sup>5</sup> if VrfySig.pk(m, σ) then <sup>6</sup> return (m,true); <sup>7</sup> return (⊥, false);

Figure 4: Algorithms (Setup, Wat, AttrText) of Watt[PRC]. The detector Detect is the same as that of W[PRC], given in Algorithm [3.](#page-49-1) Here, we let n be a codeword length sufficient to encode signatures from Sig using PRC.

<span id="page-57-1"></span>AttrForge<sup>A</sup>,Watt (λ) pk,sk ← KeyGen(1<sup>λ</sup> ) t <sup>∗</sup> ← AModel,Watsk (1<sup>λ</sup> , pk) Let Q denote the set of responses returned to A by Watsk (m, b) ← AttrText(pk,t ∗ ) return (b = true) ∧ (∀t ∈ Q, m is not a contiguous substring of t)

Figure 5: The attribution forgery experiment AttrForgeA,Watt (λ)

Proof. Let t ← Watsk(prompt) be a response, and let i be such that H [i:i+L] <sup>e</sup> (t) ≥ 4 √ <sup>ε</sup> · <sup>L</sup> + 2<sup>√</sup> 2 · n.

By the exact same proof as in Lemma [22,](#page-53-0) the robustness of PRC implies that there is some block t ′ with starting index at least i, which is correctly decoded by PRC.Decode in Algorithm [6.](#page-56-0) That is, PRC.Decode yields a signature computed on the substring of the response up to the start of block t ′ . Since t ′ starts at index at least i, this signed portion has length at least i − 1.

<span id="page-57-0"></span>Theorem 8 (A watermark with unforgeable public attribution). Let ε > 0 be any constant. If the underlying signature scheme is unforgeable, and PRC is a PRC with block length n and robustness to every 1 <sup>2</sup> − ε bounded channel, <sup>W</sup>att[PRC] is unforgeable and (4<sup>√</sup> <sup>ε</sup> · <sup>L</sup> + 2<sup>√</sup> 2 · n)-publicly-attributable.

Furthermore, Watt[PRC] retains the same soundness, undetectability, substring-completeness, and substringrobustness properties as W[PRC]. That is, Lemmas [18,](#page-48-1) [19](#page-48-2) and [22](#page-53-0) to [24](#page-54-5) all apply to Watt[PRC].

Proof. Unforgeabile public attribution follows from Lemmas [25](#page-55-0) and [26.](#page-55-1)

As noted earlier, the proofs of Lemmas [18,](#page-48-1) [19](#page-48-2) and [22](#page-53-0) to [24](#page-54-5) all hold for any choice of message input to PRC.Encode. The only difference between W[PRC] and Watt[PRC] is the choice of message input to PRC.Encode. Therefore, those proofs hold for Watt[PRC].

Related public watermarking work. Concurrent work [\[FGJ](#page-63-3)<sup>+</sup>23] constructs a watermark that similarly can be detected with a public key but requires a secret key for generation. Their scheme, like Watt, embeds a digital signature in the response and includes the signature verification key in the public key. However, their scheme has two key differences from Watt:

- They assume that each token sequence of a fixed length ℓ has at least α min-entropy.
- Their scheme has a single detector, analogous to AttrText, which is robust only to cropping. In addition to AttrText, our scheme also has Detect, which is robust to deletions and/or the binary symmetric channel, depending on the underlying PRC.

[\[FGJ](#page-63-3)<sup>+</sup>23] also discuss using error-correcting codes to improve robustness. They suggest applying an errorcorrecting code to the message and signature before embedding them. However, this would make the scheme no longer undetectable or distortion-free.

### <span id="page-58-0"></span>8 Application: universal steganography

Our main result in this section is the construction of a robust stateless steganography scheme using PRCs. We first prove that robustness follows immediately from applying a PRC to a non-robust steganography scheme appearing in several prior works [\[AP98,](#page-62-6) [HLVA02,](#page-63-2) [vAH04\]](#page-64-4). We then show that the assumptions necessary for this scheme can be weakened, which sacrifices some robustness but still yields the most robust scheme in its regime.

### <span id="page-58-1"></span>8.1 Steganography preliminaries

Setting (from [\[HLVA02\]](#page-63-2)). A steganographic channel (or covertext distribution) C is a distribution on sequences of symbols from some alphabet Σ. These symbols d ∈ Σ are often called documents, and sequences of symbols are often called covertexts. It is often convenient to consider the conditional distribution over the next symbol, given some subsequence already output by C. More precisely, given a history h ∈ Σ ∗ , we use C<sup>h</sup> to denote the conditional distribution of the next symbol from C given that thus far C has output h. For the steganographic encoder, we assume existence of an efficient oracle M(·) that can sample C<sup>h</sup> for any h ∈ Σ <sup>∗</sup> of the encoder's choice. Our steganographic encoder makes use of a rejection sampling function denoted RSM,f : {0, 1} × N → Σ, which on input (x, κ), samples c ← M until f(c) = x, taking at most κ samples. If the sampler reaches the κ th sample cκ, it outputs c<sup>κ</sup> regardless of whether f(cκ) = x. We say a function f : Σ → R is an unbiased function on a steganographic channel C if for all r ∈ R and all histories h ∈ Σ ∗ , Prd←C<sup>h</sup> [f(d) = r] = <sup>1</sup> |R| .

We recall the definition of a symmetric steganography scheme as presented in [\[KJGR21\]](#page-63-6), which is equivalent to that of [\[HLVA02\]](#page-63-2).

Definition 15 (Symmetric steganography scheme [\[KJGR21\]](#page-63-6)). A symmetric steganography scheme Σ<sup>C</sup> is a triple of possibly probabilistic algorithms Π<sup>C</sup> = (KeyGen<sup>C</sup> , EncodeC, DecodeC) parameterized by a covertext channel distribution C.

- KeyGen<sup>C</sup> (1<sup>λ</sup> ) generates the key sk.
- EncodeC(sk, m, h) is a (possibly probabilistic) algorithm that takes the key sk and a plaintext message m, called a hiddentext. Additionally, the algorithm can optionally take in a message history h = {h0, h1, . . . , h<sup>|</sup>h|−1} ∈ Σ <sup>∗</sup> of covertext messages. It returns a symbol sequence c<sup>i</sup> ∈ Σ ∗ , called a stegotext.
- DecodeC(sk, c, h) is a (possibly probabilistic) algorithm that takes as input the key sk, a stegotext c, and optionally a history h ∈ Σ ∗ . It returns a plaintext message m on success or the empty string ε on failure.

The subscript C indicates that these algorithms have access to C via the oracle M(·); we often omit this subscript for convenience.

A scheme in which the decoding algorithm requires the history is stateful; a scheme where decoding is possible without knowledge of the history is stateless. This shared history in stateful schemes is very powerful, allowing the sender and receiver to maintain a shared counter of messages sent thus far, which they can use to generate a shared one-time pad for each message.

In a public-key steganography scheme, KeyGen outputs a public-secret key pair. Analogously to public-key encryption, the encoder takes as input the public key (and not the secret key), and the decoder still takes as input the secret key. We present formal definitions for secret-key steganography here, and refer the reader to [\[vAH04\]](#page-64-4) for formal definitions of public-key steganography.

A steganography scheme must satisfy correctness and security.

Definition 16 (Steganographic correctness). A steganography scheme Π<sup>C</sup> = (KeyGen<sup>C</sup> , EncodeC, DecodeC) is correct if for any history h ∈ Σ <sup>∗</sup> and any message m,

$$\Pr\_{\mathsf{sk}\leftarrow\mathsf{KeyGen}(1^{\lambda})}\left[\mathsf{Decode}\_{\mathcal{C}}(\mathsf{sk},\mathsf{Encode}\_{\mathcal{C}}(\mathsf{sk},\mathsf{m},h),h) = \mathsf{m}\right] \geq 1 - \mathsf{negl}(\lambda).$$

We note that some other works require this probability to be 1.

Security requires that an adversary cannot distinguish between oracle access to EncodeC(sk, ·, ·) or a sampling oracle OC(·, ·) for the channel distribution.

Definition 17 (Steganographic security against chosen hiddentext attacks). Π<sup>C</sup> is secure against chosen hiddentext attacks if for all polynomial-time adversaries A, for all sk ← KeyGen<sup>C</sup> (1<sup>λ</sup> ),

$$\left| \Pr\left[ \mathcal{A}^{\mathsf{Encode}\_{\mathcal{C}}(\mathsf{sk},\cdot,\cdot),M(\cdot)} = 1 \right] - \Pr\left[ \mathcal{A}^{O\_{\mathcal{C}}(\cdot,\cdot),M(\cdot)} = 1 \right] \right| \leq \mathsf{negl}(\lambda).$$

This definition can be modified for public-key steganography by giving the adversary the public key as input.

### <span id="page-59-0"></span>8.2 Robust stateless steganography

We first present Steg, a steganography scheme that appeared originally in [\[AP98\]](#page-62-6). Steg is parameterized by an encryption scheme (KeyGen, Enc, Dec) and a function f.

Construction 9 (Steg[(KeyGen, Enc, Dec), f, κ]). Let Steg.KeyGen = KeyGen. Let Steg.Encode and Steg.Decode be defined as in Figure [6.](#page-60-1)

<span id="page-59-2"></span>[\[HLVA02\]](#page-63-2) and [\[vAH04\]](#page-64-4) prove security of the secret- and public-key versions of Steg, respectively.

Claim 27 ([\[HLVA02,](#page-63-2) [vAH04\]](#page-64-4)). Let (KeyGen, Enc, Dec) be a (public-key) encryption scheme with ciphertexts indistinguishable from random bits under a chosen plaintext attack, and let f : Σ → {0, 1} be a function which is unbiased on C. Then Steg[(KeyGen, Enc, Dec), f, λ] is a secure (public-key) steganography scheme.

Our first application of PRCs to steganography will be in showing that Steg is robust to errors when a PRC is used as the encryption scheme. To our knowledge, this gives the first robust stateless steganography scheme.

Here, we define robustness of a steganography scheme against a channel E analogously to robustness of a PRC. In particular, E may be a deletion channel, rather than just making substitutions. Robustness requires that given the output of the error channel applied to a stegotext, the hiddentext can be recovered with overwhelming probability.

Definition 18 (Robustness to an error channel). Let C be a steganographic channel with symbol alphabet Σ, and let E : Σ<sup>∗</sup> → Σ <sup>∗</sup> be an error channel. A steganography scheme (KeyGen, Encode, Decode) for C is robust to E if for all messages m and all histories h,

$$\Pr\_{\mathsf{sk},\mathsf{pk}\leftarrow\mathsf{KeyGen}(1^{\lambda})}[\mathsf{Decode}(\mathsf{sk},\mathcal{E}(x),h) = \mathsf{m}: x \leftarrow \mathsf{Encode}(\mathsf{pk},\mathsf{m},h)] = 1 - \mathsf{negl}(\lambda).$$

This definition can be adapted for secret-key schemes by replacing pk with sk.

We say that the rate of a steganography scheme is the ratio of the number of message bits to the number of symbols of stegotext that are needed to decode the message.

<span id="page-59-1"></span>Theorem 9 (Robust stateless steganography). Let PRC = (KeyGen, Encode, Decode) be a (public-key) PRC that is robust to some binary channel E. Let f : Σ → {0, 1} be a public function which is unbiased on C. Then Steg[PRC, f, λ] is a (public-key) steganography scheme, with the same rate as PRC, that is robust to any E ′ such that f ◦ E′ = E ◦f.

<span id="page-60-1"></span>

| Algorithm 7: Steg.Encode             | Algorithm 8: Steg.Decode                                                   |
|--------------------------------------|----------------------------------------------------------------------------|
| Input: Key pk, message m, history h. | ′<br>Input: Key sk and stegotext c                                         |
| 1 Let x ← Enc(pk, m);                | ′ as<br>′<br>′<br>′<br>  c<br>     c<br>1 Parse c<br>c<br>;<br>1<br>2<br>n |
| 2 for i = 1, , n do                  | 2 for i = 1, , n do                                                        |
| ← RSM(h),f (xi<br>ci<br>, κ);<br>3   | ′<br>′<br>Set x<br>i = f(c<br>);<br>3<br>i                                 |
| Set h = h  ci<br>;<br>4              | ′ =<br>′<br>′<br>′<br>  x<br>     x<br>4 Set x<br>x<br>;<br>1<br>2<br>n    |
| 5 return c1  c2     cn               | 5 return Dec(sk, x′<br>)                                                   |
|                                      |                                                                            |

Figure 6: Encoding and decoding algorithms of Steg[(KeyGen, Enc, Dec), f, κ].

Remark. We use E ◦f to denote the channel where f is applied individually to each symbol of the input, and then E is applied to the resulting bitstring. Similarly, f ◦ E′ is the channel where E ′ is applied, and then f is applied individually to each symbol of the resulting Σ-string. The condition that f ◦ E′ = E ◦f means that E ′ acts as E in the binary representation. For instance, if E ′ is a deletion channel over Σ, then E is the corresponding deletion channel over {0, 1}; if E ′ is the channel that independently replaces each symbol with a random symbol with probability p, and f is a random function, then E is approximately BSCp/2.

Proof. Steganographic security follows immediately from Claim [27](#page-59-2) and the fact that a PRC is a pseudorandom encryption scheme.

For robustness, let m be an arbitrary message and h an arbitrary history, and let c = c1|| . . . ||c<sup>n</sup> ← Steg.Encode(pk, m, h). Recall that each c<sup>i</sup> is chosen as RS<sup>M</sup>(h),f (x<sup>i</sup> , λ), where x = x1|| . . . ||x<sup>n</sup> is the output of PRC.Encode. Since f is unbiased, each sample x ′ from RS satisfies f(x ′ ) = x<sup>i</sup> independently with probability 1/2, and therefore with overwhelming probability within λ draws the sampler will output c<sup>i</sup> such that f(ci) = x<sup>i</sup> .

Given c ′ = E ′ (c), decoder first computes x ′ = f(c ′ 1 )|| . . . ||f(c ′ n ). Observe that x ′ = f ◦ E′ (c), which by assumption is equal to E ◦f(c) = E(x), where x is the output of PRC.Encode. By robustness of the PRC, PRC.Decode(sk, x′ , h) = m.

Applying Theorem [9](#page-59-1) with our PRCs from Section [6.3,](#page-40-0) we obtain a stateless public-key steganography scheme that is robust to random deletions and substitutions.

### <span id="page-60-0"></span>8.3 Stateless steganography from weaker modeling assumptions

The assumption of the existence of an unbiased function f over C is quite strong. One way to relax this assumption is to assume instead that f(C) meets some min-entropy requirement. However, now f may be unbalanced; for example, it could be the case that Pr<sup>c</sup>i←C<sup>n</sup> h [f(ci) = 1] = 2/3 for all h. Now, the encoder in Figure [6](#page-60-1) would no longer be secure: Consider sampling each symbol c<sup>i</sup> in the stegotext to always satisfy f(ci) = x<sup>i</sup> . Then, since each x<sup>i</sup> is uniform in {0, 1}, half of the symbols c<sup>i</sup> in the stegotext would satisfy f(ci) = 1. Therefore, one could distinguish between stegotexts and samples from C using f.

A natural way (used by [\[HLVA02\]](#page-63-2)) to build a secure stateful steganography scheme under only this minentropy assumption, is to let c be an error-corrected version of the message and use in the encoder a rejection sampler that takes at most two samples, sometimes outputting f(ci) ̸= x<sup>i</sup> . This rejection sampler preserves the channel distribution as long as c<sup>i</sup> is random, which is not the case for generic error-correcting codes. Therefore, [\[HLVA02\]](#page-63-2) relies on shared state to let the sender and receiver generate a fresh one-time pad per stegotext, letting c be an error-corrected message with this one-time pad applied. This shared state significantly simplifies the problem and is a strong assumption of its own.

Relaxing the assumption of an unbiased function poses more challenges for stateless steganography, where this error-correction approach fails. Although [\[HvAL08\]](#page-63-7) does construct a stateless steganography scheme under only a min-entropy assumption, this scheme has poor robustness. The idea behind this scheme is that the encoder first samples a symbol sequence d that is long enough to have λ min-entropy, and includes this sequence in the stegotext. Since both the encoder and decoder know d, d can now act as their shared state, and the remainder of the stegotext is formed using a stateful scheme such as that of [\[HLVA02\]](#page-63-2). The min-entropy assumption ensures that the state will never be used twice.

<span id="page-61-0"></span>Theorem 10. Let C be a steganographic channel with alphabet Σ, and let f : Σ → {0, 1} be a function. Suppose that there exists some α > 0 such that for all histories h ∈ Σ ∗ , minb∈{0,1} Prc←C<sup>h</sup> [f(c) = b] ≥ α. Then for any p ∈ (0, 1/2), there exists q ∈ (0, 1/2) such that if PRC is any (public-key) PRC for every q-bounded channel, then Steg[PRC, f, 2] is a (public-key) stateless steganography scheme for C, with the same rate as PRC, that is robust to any channel E such that f ◦ E = BSC<sup>p</sup> ◦ f.

Proof. We begin by showing that Steg[PRC, f, 2] is steganographically secure. As in Figure [6,](#page-60-1) suppose that we wish to encode a message m, let x ← PRC.Encode(pk, m), and let c<sup>i</sup> ← RSM(h),f (x<sup>i</sup> , 2) be the i th symbol output by the steganography scheme. Let c 1 <sup>i</sup> denote the first sample from M(h) and let c 2 <sup>i</sup> denote the second sample (which is irrelevant in the event that f(c 1 i ) = xi).

By pseudorandomness of x ← PRC.Encode(pk, m), it suffices to show that for any i ∈ [n], h ∈ Σ i−1 , and c <sup>∗</sup> ∈ Σ,

$$\Pr\_{\begin{subarray}{c} x\_i \leftarrow \{0, 1\} \\ c\_i \leftarrow RS^{M(h), f}(x\_i, 2) \end{subarray}} [c\_i = c^\*] = \Pr\_{c \leftarrow M(h)}[c = c^\*].$$

Indeed,

$$\begin{split} \Pr\_{\begin{subarray}{c} x\_{i} \leftarrow \{0,1\}\\ c\_{i} \leftarrow RS^{M(h),f}(x\_{i},2) \end{subarray}} \left[c\_{i} = c^{\*}\right] &= \Pr\_{\begin{subarray}{c} x\_{i} \leftarrow \{0,1\}\\ c\_{i}^{1} \leftarrow M(h) \end{subarray}} \left[c\_{i}^{1} = c^{\*} \wedge f(c\_{i}^{1}) = x\_{i}\right] + \Pr\_{\begin{subarray}{c} x\_{i} \leftarrow \{0,1\}\\ c\_{i}^{1}, c\_{i}^{2} \leftarrow M(h) \end{subarray}} \left[c\_{i}^{2} = c^{\*} \wedge f(c\_{i}^{1}) \neq x\_{i}\right] \\ &= \frac{1}{2} \Pr\_{\begin{subarray}{c} x\_{i}^{1} \leftarrow M(h) \end{subarray}} \left[c\_{i}^{1} = c^{\*}\right] + \frac{1}{2} \Pr\_{c\_{i}^{2} \leftarrow M(h)} \left[c\_{i}^{2} = c^{\*}\right] \\ &= \Pr\_{c \leftarrow M(h)} \left[c = c^{\*}\right]. \end{split}$$

Now we turn to showing that Steg[PRC, f, 2] is robust to any channel E such that f ◦ E = BSC<sup>p</sup> ◦ f, provided that PRC is robust to every q-bounded channel for appropriate choice of q.

Again, pseudorandomness of x ← PRC.Encode(pk, m) allows us to assume x is random. Observe that the bits f(ci) are correlated with the bits x<sup>i</sup> :

$$\begin{split} \Pr\_{\begin{subarray}{c} x\_{i} \leftarrow \{0,1\}\\ c\_{i} \leftarrow RS^{M(h),f}(x\_{i},2) \end{subarray}} \left[ f(c\_{i}) = x\_{i} \right] &= \Pr\_{\begin{subarray}{c} x\_{i} \leftarrow \{0,1\}\\ c\_{i}^{1} \leftarrow M(h) \end{subarray}} \left[ f(c\_{i}^{2}) = x\_{i} \right] + \Pr\_{\begin{subarray}{c} x\_{i} \leftarrow \{0,1\}\\ c\_{i}^{1}, c\_{i}^{2} \leftarrow M(h) \end{subarray}} \left[ f(c\_{i}^{2}) = x\_{i} \wedge f(c\_{i}^{1}) \neq x\_{i} \right] \\ &= \frac{1}{2} + \frac{1}{2} \Pr\_{\begin{subarray}{c} x\_{i} \leftarrow \{0,1\}\\ c\_{i}^{1}, c\_{i}^{2} \leftarrow M(h) \end{subarray}} \left[ f(c\_{i}^{2}) = x\_{i} \mid f(c\_{i}^{1}) \neq x\_{i} \right] \\ &\geq \frac{1}{2} + \frac{1}{2} \alpha. \end{split}$$

For i ∈ [n] let ˆc be the content generated by Steg (before the error channel E is applied), defined by cˆ = ˆc1|| · · · ||cˆ<sup>n</sup> for ˆc<sup>i</sup> = f(ci). By Azuma's inequality (Lemma [1\)](#page-20-3), wt(ˆc⊕x) ≤ (1/2−α/4)·n with probability 1−negl(n). The decoder for the steganography scheme will compute (f ◦E)(c), which is distributed identically to (BSC<sup>p</sup> ◦ f)(c) = BSCp(ˆc) since f ◦ E = BSC<sup>p</sup> ◦ f. By a Chernoff bound and straightforward computation,

$$\operatorname{wt}(\operatorname{BSC}\_p(\hat{c}) \oplus x) \le \left(\frac{1}{2} - \frac{\alpha}{8}(1 - 2p)\right) \cdot n$$

with probability 1−negl(n). Therefore, if PRC is robust to any q-bounded channel for q = 1/2−(α/8)(1−2p), then Steg[PRC, f, 2] is robust to E.

### References

- <span id="page-62-3"></span>[Aar22] Scott Aaronson. My AI Safety Lecture for UT Effective Altruism. [https://scottaaronson.](https://scottaaronson.blog/?p=6823) [blog/?p=6823](https://scottaaronson.blog/?p=6823), November 2022. Accessed May 2023.
- <span id="page-62-2"></span>[ABN+92] Noga Alon, Jehoshua Bruck, Joseph Naor, Moni Naor, and Ron M. Roth. Construction of asymptotically good low-rate error-correcting codes through pseudo-random graphs. IEEE Trans. Inf. Theory, 38(2):509–516, 1992.
- <span id="page-62-10"></span>[ACI+20] Thomas Agrikola, Geoffroy Couteau, Yuval Ishai, Stanis law Jarecki, and Amit Sahai. On pseudorandom encodings. In Theory of Cryptography: 18th International Conference, TCC 2020, Durham, NC, USA, November 16–19, 2020, Proceedings, Part III 18, pages 639–669. Springer, 2020.
- <span id="page-62-9"></span>[ADI+17] Benny Applebaum, Ivan Damg˚ard, Yuval Ishai, Michael Nielsen, and Lior Zichron. Secure arithmetic computation with constant computational overhead. In Annual International Cryptology Conference, pages 223–254. Springer, 2017.
- <span id="page-62-5"></span>[Ale03] Michael Alekhnovich. More on average case vs approximation complexity. In 44th Symposium on Foundations of Computer Science (FOCS 2003), 11-14 October 2003, Cambridge, MA, USA, Proceedings, pages 298–307. IEEE Computer Society, 2003.
- <span id="page-62-6"></span>[AP98] Ross J Anderson and Fabien AP Petitcolas. On the limits of steganography. IEEE Journal on selected areas in communications, 16(4):474–481, 1998.
- <span id="page-62-11"></span>[ARC<sup>+</sup>01] Mikhail J Atallah, Victor Raskin, Michael Crogan, Christian Hempelmann, Florian Kerschbaum, Dina Mohamed, and Sanket Naik. Natural language watermarking: Design, analysis, and a proof-of-concept implementation. In Information Hiding: 4th International Workshop, IH 2001 Pittsburgh, PA, USA, April 25–27, 2001 Proceedings 4, pages 185–200. Springer, 2001.
- <span id="page-62-12"></span>[ARH<sup>+</sup>02] Mikhail J Atallah, Victor Raskin, Christian F Hempelmann, Mercan Karahan, Radu Sion, Umut Topkara, and Katrina E Triezenberg. Natural language watermarking and tamperproofing. In International workshop on information hiding, pages 196–212. Springer, 2002.
- <span id="page-62-7"></span>[Ari09] Erdal Arikan. Channel polarization: a method for constructing capacity-achieving codes for symmetric binary-input memoryless channels. IEEE Trans. Inf. Theory, 55(7):3051–3073, 2009.
- <span id="page-62-4"></span>[ASS<sup>+</sup>23] Shweta Agrawal, Sagnik Saha, Nikolaj Ignatieff Schwartzbach, Akhil Vanukuri, and Prashant Nalini Vasudevan. k-sum in the sparse regime. Cryptology ePrint Archive, Paper 2023/488, 2023. <https://eprint.iacr.org/2023/488>.
- <span id="page-62-14"></span>[BC05] Michael Backes and Christian Cachin. Public-key steganography with active attacks. In Theory of Cryptography Conference, pages 210–226. Springer, 2005.
- <span id="page-62-8"></span>[BCG<sup>+</sup>19] Elette Boyle, Geoffroy Couteau, Niv Gilboa, Yuval Ishai, Lisa Kohl, and Peter Scholl. Efficient pseudorandom correlation generators: Silent ot extension and more. In Advances in Cryptology– CRYPTO 2019: 39th Annual International Cryptology Conference, Santa Barbara, CA, USA, August 18–22, 2019, Proceedings, Part III 39, pages 489–518. Springer, 2019.
- <span id="page-62-0"></span>[BH23] Diane Bartz and Krystal Hu. OpenAI, Google, others pledge to watermark AI content for safety, White House says, July 2023. [https://www.reuters.com/technology/openai-google](https://www.reuters.com/technology/openai-google-others-pledge-watermark-ai-content-safety-white-house-2023-07-21)[others-pledge-watermark-ai-content-safety-white-house-2023-07-21.](https://www.reuters.com/technology/openai-google-others-pledge-watermark-ai-content-safety-white-house-2023-07-21)
- <span id="page-62-13"></span>[Cac98] Christian Cachin. An information-theoretic model for steganography. In International Workshop on Information Hiding, pages 306–318. Springer, 1998.
- <span id="page-62-1"></span>[CGZ23] Miranda Christ, Sam Gunn, and Or Zamir. Undetectable watermarks for language models. IACR Cryptol. ePrint Arch., page 763, 2023.
- <span id="page-63-13"></span>[Cra98] Scott Craver. On public-key steganography in the presence of an active warden. In International Workshop on Information Hiding, pages 355–368. Springer, 1998.
- <span id="page-63-0"></span>[DGG+15] Yevgeniy Dodis, Chaya Ganesh, Alexander Golovnev, Ari Juels, and Thomas Ristenpart. A formal treatment of backdoored pseudorandom generators. In Advances in Cryptology– EUROCRYPT 2015: 34th Annual International Conference on the Theory and Applications of Cryptographic Techniques, Sofia, Bulgaria, April 26-30, 2015, Proceedings, Part I 34, pages 101–126. Springer, 2015.
- <span id="page-63-12"></span>[DIRR09] Nenad Dedi´c, Gene Itkis, Leonid Reyzin, and Scott Russell. Upper and lower bounds on black-box steganography. Journal of Cryptology, 22:365–394, 2009.
- <span id="page-63-15"></span>[dWSK+22] Christian Schroeder de Witt, Samuel Sokota, J Zico Kolter, Jakob Foerster, and Martin Strohmeier. Perfectly secure steganography using minimum entropy coupling. arXiv preprint arXiv:2210.14889, 2022.
- <span id="page-63-3"></span>[FGJ+23] Jaiden Fairoze, Sanjam Garg, Somesh Jha, Saeed Mahloujifar, Mohammad Mahmoody, and Mingyuan Wang. Publicly detectable watermarking for language models. Cryptology ePrint Archive, 2023.
- <span id="page-63-14"></span>[Fri09] Jessica Fridrich. Steganography in digital media: principles, algorithms, and applications. Cambridge University Press, 2009.
- <span id="page-63-5"></span>[Gal62] Robert G. Gallager. Low-density parity-check codes. IRE Trans. Inf. Theory, 8(1):21–28, 1962.
- <span id="page-63-10"></span>[GKVZ22] Shafi Goldwasser, Michael P Kim, Vinod Vaikuntanathan, and Or Zamir. Planting undetectable backdoors in machine learning models. In 2022 IEEE 63rd Annual Symposium on Foundations of Computer Science (FOCS), pages 931–942. IEEE, 2022.
- <span id="page-63-2"></span>[HLVA02] Nicholas J Hopper, John Langford, and Luis Von Ahn. Provably secure steganography. In Advances in Cryptology—CRYPTO 2002: 22nd Annual International Cryptology Conference Santa Barbara, California, USA, August 18–22, 2002 Proceedings 22, pages 77–92. Springer, 2002.
- <span id="page-63-4"></span>[Hoe94] Wassily Hoeffding. Probability inequalities for sums of bounded random variables. The collected works of Wassily Hoeffding, pages 409–426, 1994.
- <span id="page-63-11"></span>[Hop05] Nicholas Hopper. On steganographic chosen covertext security. In International Colloquium on Automata, Languages, and Programming, pages 311–323. Springer, 2005.
- <span id="page-63-7"></span>[HvAL08] Nicholas Hopper, Luis von Ahn, and John Langford. Provably secure steganography. IEEE Transactions on Computers, 58(5):662–676, 2008.
- <span id="page-63-9"></span>[KAAL23] Jan Hendrik Kirchner, Lama Ahmad, Scott Aaronson, and Jan Leike. New ai classifier for indicating AI-written text. [https://openai.com/blog/](https://openai.com/blog/new-ai-classifier-for-indicating-ai-written-text) [new-ai-classifier-for-indicating-ai-written-text](https://openai.com/blog/new-ai-classifier-for-indicating-ai-written-text), January 2023. Accessed May 2023.
- <span id="page-63-1"></span>[KGW<sup>+</sup>23a] John Kirchenbauer, Jonas Geiping, Yuxin Wen, Jonathan Katz, Ian Miers, and Tom Goldstein. A watermark for large language models. arXiv preprint arXiv:2301.10226, 2023.
- <span id="page-63-8"></span>[KGW<sup>+</sup>23b] John Kirchenbauer, Jonas Geiping, Yuxin Wen, Manli Shu, Khalid Saifullah, Kezhi Kong, Kasun Fernando, Aniruddha Saha, Micah Goldblum, and Tom Goldstein. On the reliability of watermarks for large language models. arXiv preprint arXiv:2306.04634, 2023.
- <span id="page-63-6"></span>[KJGR21] Gabriel Kaptchuk, Tushar M. Jois, Matthew Green, and Aviel D. Rubin. Meteor: Cryptographically secure steganography for realistic distributions. In Yongdae Kim, Jong Kim, Giovanni Vigna, and Elaine Shi, editors, CCS '21: 2021 ACM SIGSAC Conference on Computer and

Communications Security, Virtual Event, Republic of Korea, November 15 - 19, 2021, pages 1529–1548. ACM, 2021.

- <span id="page-64-7"></span>[KKRT16] Vladimir Kolesnikov, Ranjit Kumaresan, Mike Rosulek, and Ni Trieu. Efficient batched oblivious prf with applications to private set intersection. In Proceedings of the 2016 ACM SIGSAC Conference on Computer and Communications Security, pages 818–829, 2016.
- <span id="page-64-6"></span>[KL07] Jonathan Katz and Yehuda Lindell. Introduction to modern cryptography: principles and protocols. Chapman and hall/CRC, 2007.
- <span id="page-64-0"></span>[KTHL23] Rohith Kuditipudi, John Thickstun, Tatsunori Hashimoto, and Percy Liang. Robust distortionfree watermarks for language models. arXiv preprint arXiv:2307.15593, 2023.
- <span id="page-64-11"></span>[MLK+23] Eric Mitchell, Yoonho Lee, Alexander Khazatsky, Christopher D. Manning, and Chelsea Finn. DetectGPT: Zero-shot machine-generated text detection using probability curvature. CoRR, abs/2301.11305, 2023.
- <span id="page-64-8"></span>[MTSB13] Rafael Misoczki, Jean-Pierre Tillich, Nicolas Sendrier, and Paulo SLM Barreto. MDPC-McEliece: New McEliece variants from moderate density parity-check codes. In 2013 IEEE international symposium on information theory, pages 2069–2073. IEEE, 2013.
- <span id="page-64-2"></span>[NN93] Joseph Naor and Moni Naor. Small-bias probability spaces: Efficient constructions and applications. SIAM J. Comput., 22(4):838–856, 1993.
- <span id="page-64-10"></span>[PSF<sup>+</sup>23] Julien Piet, Chawin Sitawarin, Vivian Fang, Norman Mu, and David Wagner. Mark my words: Analyzing and evaluating language model watermarks. arXiv preprint arXiv:2312.00273, 2023.
- <span id="page-64-5"></span>[RBB03] Phillip Rogaway, Mihir Bellare, and John Black. Ocb: A block-cipher mode of operation for efficient authenticated encryption. ACM Transactions on Information and System Security (TISSEC), 6(3):365–403, 2003.
- <span id="page-64-14"></span>[Sim84] Gustavus J Simmons. The prisoners' problem and the subliminal channel. In Advances in Cryptology: Proceedings of Crypto 83, pages 51–67. Springer, 1984.
- <span id="page-64-3"></span>[Ta-17] Amnon Ta-Shma. Explicit, almost optimal, epsilon-balanced codes. In Hamed Hatami, Pierre McKenzie, and Valerie King, editors, Proceedings of the 49th Annual ACM SIGACT Symposium on Theory of Computing, STOC 2017, Montreal, QC, Canada, June 19-23, 2017, pages 238– 251. ACM, 2017.
- <span id="page-64-13"></span>[TCH23] Ruixiang Tang, Yu-Neng Chuang, and Xia Hu. The science of detecting LLM-generated texts. arXiv preprint arXiv:2303.07205, 2023.
- <span id="page-64-12"></span>[Tia23] Edward Tian. GPTZero update V1. [https://gptzero.substack.com/p/](https://gptzero.substack.com/p/gptzero-update-v1) [gptzero-update-v1](https://gptzero.substack.com/p/gptzero-update-v1), January 2023. Accessed May 2023.
- <span id="page-64-9"></span>[TTDI05] Mercan Topkara, Cuneyt M Taskiran, and Edward J Delp III. Natural language watermarking. In Security, Steganography, and Watermarking of Multimedia Contents VII, volume 5681, pages 441–452. SPIE, 2005.
- <span id="page-64-4"></span>[vAH04] Luis von Ahn and Nicholas J. Hopper. Public-key steganography. In Christian Cachin and Jan Camenisch, editors, Advances in Cryptology - EUROCRYPT 2004, International Conference on the Theory and Applications of Cryptographic Techniques, Interlaken, Switzerland, May 2-6, 2004, Proceedings, volume 3027 of Lecture Notes in Computer Science, pages 323–341. Springer, 2004.
- <span id="page-64-1"></span>[VV83] Umesh V. Vazirani and Vijay V. Vazirani. Trapdoor pseudo-random number generators, with applications to protocol design. In 24th Annual Symposium on Foundations of Computer Science (sfcs 1983), pages 23–30, 1983.
- <span id="page-65-1"></span>[ZALW23] Xuandong Zhao, Prabhanjan Ananth, Lei Li, and Yu-Xiang Wang. Provable robust watermarking for AI-generated text. arXiv preprint arXiv:2306.17439, 2023.
- <span id="page-65-5"></span>[Zam24] Or Zamir. Excuse me, sir? your language model is leaking (information). arXiv preprint arXiv:2401.10360, 2024.
- <span id="page-65-4"></span>[ZDR19] Zachary M. Ziegler, Yuntian Deng, and Alexander M. Rush. Neural linguistic steganography. In Kentaro Inui, Jing Jiang, Vincent Ng, and Xiaojun Wan, editors, Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing, EMNLP-IJCNLP 2019, Hong Kong, China, November 3-7, 2019, pages 1210–1215. Association for Computational Linguistics, 2019.
- <span id="page-65-2"></span>[ZEF+23] Hanlin Zhang, Benjamin L Edelman, Danilo Francati, Daniele Venturi, Giuseppe Ateniese, and Boaz Barak. Watermarks in the sand: Impossibility of strong watermarking for generative models. arXiv preprint arXiv:2311.04378, 2023.
- <span id="page-65-3"></span>[ZHR+19] Rowan Zellers, Ari Holtzman, Hannah Rashkin, Yonatan Bisk, Ali Farhadi, Franziska Roesner, and Yejin Choi. Defending against neural fake news. Advances in neural information processing systems, 32, 2019.

### <span id="page-65-0"></span>A Related work

Comparison to code-based cryptography. Our approach to constructing pseudorandom codes is closely related to code-based cryptography, and in particular the McEliece cryptosystem. The McEliece cryptosystem is a public-key encryption scheme in which the public key is a generator matrix for a linear code and the secret key is a trapdoor for efficient decoding. In this sense, our constructions of pseudorandom codes can be viewed as instantiations of the McEliece cryptosystem. However, there are two key differences between our setting and that of code-based cryptography that render code-based cryptography results inapplicable for our purposes.

The first difference is in the source of the errors, or noise. PRCs are required to correct uncontrolled errors introduced by an adversarial channel; in McEliece, all of the errors are introduced by an honest user for the purpose of securely sending the message over a perfect channel. Therefore, the channel itself is specified as part of the cryptosystem and the code only needs to be robust to this channel. In pseudorandom codes, it is crucial that we can correct from an arbitrary constant rate p < 1/2 of additional errors introduced by a noisy channel on a binary alphabet. Existing code-based cryptosystems (such as binary Goppa codes, Reed-Solomon codes, Reed-Muller codes, or Algebraic Geometry codes) either do not enjoy such strong robustness or rely on a larger alphabet.

The second difference is that we require noisy codewords to be pseudorandom, rather than just hiding. If every (noisy) codeword satisfies some efficiently-computable property P, but a uniformly random string does not satisfy P, then the code cannot be a PRC. However, such a code might still define a secure encryption scheme, as long as P does not distinguish between codewords for different messages.

Our primary construction of PRCs is based on low-density parity-check (LDPC) codes, with somewhathigher Ω(log n) density than is typically considered. The work of [\[MTSB13\]](#page-64-8) consider "moderate-density parity-check" codes, with density Ω(<sup>√</sup> n log n). While their codes suffice for code-based cryptography, they do not enjoy as strong robustness as ours because of the higher density. In particular, they are not robust to any constant rate of substitutions.

PRC-like cryptographic tools. Error-correcting codes with some pseudorandomness properties have proven useful in cryptographic applications such as pseudorandom correlation generators [\[BCG](#page-62-8)<sup>+</sup>19] and oblivious linear evaluation (OLE) [\[ADI](#page-62-9)<sup>+</sup>17]. However, in all of these applications, decoding requires new side information for each message, such as the locations of the errors. The fundamental difficulty in constructing our pseudorandom codes is that the only extra information provided to the decoder is a single, unchanging secret key; without this key the messages must be pseudorandom.

Pseudorandom encodings, defined and studied in [\[ACI](#page-62-10)+20], are similar in name to PRCs but are very different objects. A pseudorandom encoding for a distribution X is a pair of unkeyed algorithms (Encode, Decode) such that Encode(x) is pseudorandom (i.e., appears uniform) for a random x ← X, and Decode(Encode(x)) = x with overwhelming probability. For pseudorandom encodings there is no robustness requirement. Furthermore, pseudorandomness for PRCs requires that Encode(x) is pseudorandom for any x of the adversary's choice.

Language watermarking schemes. Classical watermarking considers the problem of embedding a signal into a fixed object, such as a given text, in such a way that the watermark is hard to remove, and the quality of the original object is preserved. In that setting, studied specifically for natural language in [\[TTDI05,](#page-64-9) [ARC](#page-62-11)+01, [ARH](#page-62-12)+02], planting the watermark must alter the text, and the goal is to minimize some distance measure between the original text and the watermarked text. In contrast, since generative models are randomized, the quality goal of watermarks for generative models is to preserve certain properties of the distribution of the model's outputs. Due to this difference, new techniques have been developed for watermarking AI-generated content, particularly text output by language models, which is the focus of our watermarking work in this paper.

A language model takes as input a prompt and randomly samples a response using an iterative process. Given a prompt, it computes a probability distribution p<sup>1</sup> for the first token and samples a token t<sup>1</sup> from this distribution. At each subsequent step, it takes as input the token sequence t1, . . . ,ti−<sup>1</sup> output thus far, computes the distribution p<sup>i</sup> , and samples the i th token in the response t<sup>i</sup> from p<sup>i</sup> . It continues doing so until it samples a special "done" token, at which point it terminates and outputs the response. The randomness in this process is important for the usefulness of the model—a model should produce a wide variety of useful responses given the same prompt—and it is crucial for watermarking.

Recently, there have been several language model watermarking schemes proposed (e.g., [\[Aar22,](#page-62-3) [KGW](#page-63-1)<sup>+</sup>23a, [CGZ23,](#page-62-1) [ZALW23,](#page-65-1) [KTHL23,](#page-64-0) [FGJ](#page-63-3)<sup>+</sup>23]), which embed the watermark by changing the way that each t<sup>i</sup> is sampled from p<sup>i</sup> . At a very high level, these watermark embedders give preference to certain tokens in the sampling process. The corresponding detectors check for the presence of more preferred tokens than would be expected in independently generated text.

The simplest of these schemes, [\[ZALW23\]](#page-65-1), fixes a random partition of tokens into equal-sized green and red lists, and it embeds the watermark by increasing the probabilities of tokens on the green list when it samples its response. The detector computes the fraction of green tokens, which should be appreciably greater than 1 2 for watermarked text and roughly <sup>1</sup> 2 for all other text. This red-green partition is used for every sampled token across all responses, which results in a significant change to the model's distribution. For example, if "computer" is on the red list, the model now prefers not to talk about computers.

[\[Aar22,](#page-62-3) [KGW](#page-63-1)<sup>+</sup>23a] mitigate this distributional shift by generating the red-green partitions dynamically. Rather than using the same red-green partition for every token, [\[Aar22,](#page-62-3) [KGW](#page-63-1)<sup>+</sup>23a] select a partition for each token using a PRF evaluated at the previous k tokens. That is, these schemes use a PRF Fsk with secret key sk, and add weight to tokens t<sup>i</sup> such that Fsk(ti−k, . . . ,ti−1,ti) = 1. This effectively generates a new red-green partition for each token, assuming that no prefix ti−k, . . . ,ti−<sup>1</sup> ever appears twice. The detector computes the fraction of tokens on these green lists, which it can compute by evaluating the PRF, provided that the seeds are intact in the given text. The length k of the token sequence used as these seeds can be tuned to trade off between robustness and frequency of seed reuse. Longer seeds result in less frequent seed reuse but make the watermark easier to remove, since the adversary can destroy every seed and prevent the detector from computing the green lists by changing only 1/k tokens in a watermarked response.

Although [\[KGW](#page-63-1)<sup>+</sup>23a] and [\[Aar22\]](#page-62-3) both generate randomness using this seeded PRF, they use this randomness to sample from p<sup>i</sup> differently, achieving different quality guarantees as a result. The watermarking algorithm in [\[Aar22\]](#page-62-3) samples tokens such that, for each token of the response, the expected watermarked distribution (over the randomness of sk) is identical to the original model's distribution. However, while individual tokens' distributions are preserved, the watermark introduces correlations between tokens' distributions as seeds can be reused (even within the same response). For example, if the same prompt is queried multiple times, the watermark will result in the same bias for the first token of the response each time. [\[KGW](#page-63-1)+23a] achieves a weaker guarantee and changes the distribution of the model's outputs.

Distortion-freeness, a quality notion defined by [\[KTHL23\]](#page-64-0), is the property that the expected distribution of a single response from the watermarked model is identical to the distribution of a single response from the original model. [\[KTHL23\]](#page-64-0) constructs a distortion-free watermarking scheme with an interesting level of robustness. To generate each response, this watermarking scheme samples a string x ∗ from a fixed collection of seeds x1, . . . , xℓ. The i th token in the response is chosen to be correlated with the i th bit of x ∗ . The detector checks whether the given text is watermarked by computing its edit distance from each of the strings x1, . . . , xℓ, returning true if any of these distances is below some threshold.

This detection algorithm is quite slow in practice: It runs in time O(n 2 ℓ), where n is the length of the random strings. While using a smaller ℓ improves the detector's efficiency, it deteriorates the model's quality by reducing the response variability. Our watermark avoids this tradeoff between variability of the model and detector efficiency, while still offering robustness.

The strongest quality guarantee is undetectability, defined by [\[CGZ23\]](#page-62-1), which is the quality notion we focus on in this work. Undetectability requires that the watermarked model and original model are computationally indistinguishable to an adversary without knowledge of the detection key, even if the adversary can make an unbounded number of adaptive queries. In contrast, distortion-freeness of [\[KTHL23\]](#page-64-0) says nothing about multiple responses from the model. In particular, a watermark can be distortion-free but render the response to a given prompt entirely deterministic — even if the original model had a great deal of variability on the same prompt.

Like [\[KGW](#page-63-1)<sup>+</sup>23a, [Aar22\]](#page-62-3), the watermark in [\[CGZ23\]](#page-62-1) uses a PRF seeded with previously output tokens to generate the randomness used to bias the token sampler. A crucial observation used in [\[CGZ23\]](#page-62-1) to avoid the seed reuse issue of [\[KGW](#page-63-1)<sup>+</sup>23a, [Aar22\]](#page-62-3), is that if the tokens constituting the seed contain enough entropy, seed reuse becomes unlikely. Because the watermarking algorithm has access to the token distributions, it can compute the amount of entropy in a token sequence and use it as a seed only once this entropy has exceeded a certain threshold. This allows [\[CGZ23\]](#page-62-1) to achieve undetectability and a robustness guarantee they call substring-completeness, that any sufficiently high-entropy substring of a response will be detected as watermarked. This is essentially the same robustness guarantee as [\[KGW](#page-63-1)<sup>+</sup>23a, [Aar22\]](#page-62-3), but it is weaker than that of [\[KTHL23,](#page-64-0) [ZALW23\]](#page-65-1), since changing one token in every seed removes the watermark.

[\[FGJ](#page-63-3)<sup>+</sup>23] has similar quality to [\[CGZ23\]](#page-62-1), and embeds a digital signature in the response to make it detectable by anyone with a public detection key. A separate secret key is required to embed the watermark. Similarly to [\[CGZ23\]](#page-62-1), their watermark generates the initial portion of the response from the original model. It then uses this portion as a seed for a PRF and encodes each bit of a digital signature by sampling a block of tokens such that the PRF evaluated on that block is equal to that bit. Like [\[CGZ23\]](#page-62-1), changing any token in the seed removes the watermark.

We compare some of these watermarking schemes in Table [1.](#page-68-0) We refer the reader to [\[PSF](#page-64-10)<sup>+</sup>23] for a more detailed empirical comparison of some of these schemes, and to [\[KGW](#page-63-8)<sup>+</sup>23b] for an empirical study of the robustness of [\[KGW](#page-63-1)<sup>+</sup>23a].

On removing watermarks. [\[CGZ23\]](#page-62-1) describe an attack that removes any undetectable watermark and preserves response quality, but this attack is very impractical because it involves querying the model once for each token in the response. [\[ZEF](#page-65-2)<sup>+</sup>23] describe an attack that can remove any watermark in a way that preserves response quality, assuming that the attacker has access to a quality oracle and that random walks over the graph of responses mix sufficiently quickly. These assumptions are quite strong, and it is not

<span id="page-68-0"></span>

| Paper     | Single-query undetectable? | Undetectable? | Robust? |
|-----------|----------------------------|---------------|---------|
| [Aar22]   | ✓*                         | ✗             | ✗       |
| [KGW+23a] | ✗                          | ✗             | ✗       |
| [CGZ23]   | ✓                          | ✓             | ✗       |
| [ZALW23]  | ✗                          | ✗             | ✓       |
| [KTHL23]  | ✓                          | ✗             | ✓       |
| [FGJ+23]  | ✓                          | ✓             | ✗       |
| This work | ✓                          | ✓             | ✓       |

Table 1: Comparison between various watermarking schemes for language models. "Single-query undetectable" means that a single query to the watermarked model is computationally indistinguishable from one to the original model, and "undetectable" is the multi-query analogue as defined in [\[CGZ23\]](#page-62-1). In this table, "robust" means that the watermark is resilient to a constant rate of substitutions.

\* [\[Aar22\]](#page-62-3) is single-query undetectable provided that every short contiguous sequence of response tokens has high enough entropy.

clear whether there are fast, reliable quality oracles that don't already yield a full language model. Still, in light of these impossibility results, one cannot hope to have a watermarking scheme that is robust against all possible attacks — indeed, an adversary with sufficient knowledge of the language could always write a high-quality text without even consulting the watermarked model. Therefore, we instead define robustness against particular classes of adversaries, including those that delete and substitute tokens.

Other techniques for detecting machine-generated text. Another approach for detecting AI-generated text is to train a machine learning classifier to distinguish between AI-generated and natural text [\[ZHR](#page-65-3)<sup>+</sup>19, [MLK](#page-64-11)<sup>+</sup>23, [Tia23,](#page-64-12) [KAAL23\]](#page-63-9). However, these classifiers lack transparency, can be easily evaded, have high false-positive rates, and have unpredictable biases. OpenAI retracted its classifier-based detector due to these issues.

Instead of relying on existing idiosyncrasies of AI-generated text, watermarks embed patterns themselves, making detection more reliable and transparent. See, e.g., [\[TCH23,](#page-64-13) [PSF](#page-64-10)<sup>+</sup>23] for an overview of the various approaches to detecting AI-generated text.

Undetectable backdoors for models. [\[GKVZ22\]](#page-63-10) shows how to embed a hidden "backdoor" during training of a model. Using a secret key, one can "activate" the backdoor by slightly perturbing inputs to alter their classification under the backdoored model. These backdoors are undetectable in the sense that, without the secret key, one cannot distinguish between an honestly trained or a backdoored model. While not closely related to our work in technical content, [\[GKVZ22\]](#page-63-10) is similar in spirit as an application of cryptographic definitions and techniques to machine learning.

Universal steganography. Steganography was introduced by Simmons [\[Sim84\]](#page-64-14), who presented it as problem where two prisoners wish to communicate in the presence of a warden, hiding not only the content of their communication but also the fact that this communication is occurring. [\[HLVA02\]](#page-63-2) first formalized steganography in the computational setting. Here, there is some distribution of covertexts in which the sender wishes to conceal its message. In Section [8,](#page-58-0) we consider universal steganography, where the covertext distribution is an arbitrary distribution to which the sender has sample access. The sender uses this sample access and a secret key to construct a stegotext that encodes the message, which the receiver decodes using the secret key.

Loosely speaking, steganographic security requires that an outside observer cannot distinguish stegotexts from covertexts, and furthermore cannot learn anything about the message. There are several security

<span id="page-69-0"></span>

| Scheme                        | Stateless? | No unbiased function? | Public-key? | Robust? |
|-------------------------------|------------|-----------------------|-------------|---------|
| [HLVA02] Construction 2*      | ✓          | ✗                     | ✗           | ✗       |
| [HLVA02] Constructions 3,4    | ✗          | ✓                     | ✗           | ✓       |
| [HvAL08] NoState Construction | ✓          | ✗                     | ✗           | ✗       |
| [vAH04] Construction 2        | ✓          | ✗                     | ✓           | ✗       |
| This work                     | ✓          | ✓                     | ✓           | ✓       |

Table 2: Comparison of universal steganography schemes. "Stateless" means that the sender and receiver do not need to share a synchronized state. "No unbiased function" means that the scheme does not require a function that is unbiased over the covertext distribution; instead, schemes with a check mark in this column rely on an assumption about the entropy of the text. As in Table [1,](#page-68-0) "robust" means robustness to a constant rate of substitutions.

\* Although this scheme was also proposed by [\[AP98,](#page-62-6) [Cac98\]](#page-62-13), we refer to the construction from [\[HLVA02\]](#page-63-2), whose setting and terminology we follow.

variants in the literature, including information-theoretic security [\[Cac98\]](#page-62-13) and security against active attacks [\[BC05,](#page-62-14) [Hop05\]](#page-63-11). We focus on (computational) security against chosen message attacks (CMA) as defined in [\[HLVA02\]](#page-63-2), which is analogous to CPA security of encryption. There are several constructions of CMA-secure secret-key steganography schemes under certain assumptions, including [\[HLVA02,](#page-63-2) [HvAL08,](#page-63-7) [DIRR09\]](#page-63-12). We present a comparison of these schemes' properties in Table [2.](#page-69-0) All of these schemes either make the very strong assumption that there is a known hash function that is unbiased on the covertext distribution, or else rely on a synchronized shared state between the sender and receiver.

An additional desirable property of a stegosystem, and one that is challenging to achieve, is robustness: Even if the stegotext is corrupted by an adversary, the receiver should be able to recover the message. To the best of our knowledge, prior to this work there was no provably secure stateless secret-key stegosystem with nontrivial robustness.

Our robustness notion is different from that of [\[HLVA02\]](#page-63-2), called substitution-robustness. In substitutionrobustness, an adversary may make substitutions of some symbols of the stegotext before it is given to the receiver, which should still recover the message. The set of substitutions that their adversary is allowed to make is parameterized by a relation R. That is, the adversary can change any symbol s to a symbol s ′ provided that (s, s′ ) ∈ R. This definition breaks down when the alphabet is binary, since if R is nontrivial, containing without loss of generality (0, 1), the adversary can change all stegotexts to the all-one string. Furthermore, it does not capture an adversary that has a bound on the number of symbols it may change, but that can change each symbol to any other symbol. Our definition is thus incomparable to theirs, and our channel may introduce deletions rather than just substitutions.

While [\[HLVA02\]](#page-63-2) constructs a robust steganography scheme under this relation-based definition, they assume that the sender and receiver can share some state; in their scheme, this state is a synchronized counter N of the number of messages sent so far. See Section [2.7](#page-18-0) for a discussion on synchronized states in steganography.

As with encryption, steganography has a public-key analogue, which was defined formally by [\[vAH04\]](#page-64-4). That is, encoding is possible with a public key, and decoding requires a secret key. While [\[vAH04\]](#page-64-4) was the first to define and formally prove security of public-key steganography, public-key schemes existed in prior work [\[AP98,](#page-62-6) [Cra98\]](#page-63-13). The main steganography construction in this work is public-key as well.

While we focus on steganography with provable security in the models of [\[HLVA02,](#page-63-2) [vAH04\]](#page-64-4), we note that there is a large body of work that constructs steganography schemes with heuristic guarantees. We refer the interested reader to [\[Fri09\]](#page-63-14).

Language model steganography. The formal setting of steganography from [\[HLVA02\]](#page-63-2) assumes that the sender has sample access to the covertext distribution. It is unclear how to realize this assumption in practice: If the sender wishes to conceal its message in casual conversation, it must be able to sample a random casual conversation. One solution is to use a language model as this sampler for the covertext distribution, and there are several language model steganography schemes tailored to this setting where the sender interacts with a language model to craft its stegotexts [\[KJGR21,](#page-63-6) [dWSK](#page-63-15)+22, [ZDR19,](#page-65-4) [Zam24\]](#page-65-5). This is a relaxation of universal steganography, since these language model steganography schemes leverage the sender's explicit access to the covertext distribution via the model. Therefore, our universal steganography scheme in Section [8](#page-58-0) is incomparable to these schemes.

Language model steganography and undetectable watermarks for language models are closely related, as both are concerned with secretly embedding a signal in the output of a language model. Indeed, we note in Section [7.2](#page-48-0) that our watermarking scheme yields a language model steganography scheme, since undetectability implies steganographic secrecy. Our resulting steganography scheme has the strongest robustness of any existing scheme, and in particular is the only language model steganography scheme with robustness to a constant rate of random substitutions.

[\[Zam24\]](#page-65-5) presents a language model steganography scheme derived from the watermarking scheme of [\[CGZ23\]](#page-62-1). This scheme is also stateless and relies on a minimal entropy assumption about the text, but it is not publickey or robust.

In Meteor [\[KJGR21\]](#page-63-6), the sender and receiver share a generative language model, and they maintain a shared history of the prompt and all tokens output thus far by the model. To encode a message, the sender queries the model to obtain the distribution p<sup>i</sup> over the next token. It then samples the next token in a way that encodes some information about the message. Because the sender and receiver share the model description and the token history including the prompt, the receiver can compute p<sup>i</sup> . Meteor crucially uses the ability of the receiver to compute p<sup>i</sup> , in order to decode the message. Any change to the text history at all (even removing the prompt) can destroy the receiver's ability to compute p<sup>i</sup> , and therefore the receiver's ability to decode the message.

[\[dWSK](#page-63-15)<sup>+</sup>22] constructs a steganography scheme using minimum entropy couplings, in the information theoretic setting of [\[Cac98\]](#page-62-13). In their scheme, the decoder also must know the prompt used, as it requires access to an explicit description of the covertext distribution which is determined by the prompt. Furthermore, the adversary is not allowed to tamper with the stegotexts.

Backdoored/trapdoor PRGs. A trapdoor or backdoored PRG [\[VV83,](#page-64-1) [DGG](#page-63-0)<sup>+</sup>15] is a pseudorandom generator that outputs a sequence of bits that are pseudorandom to an observer, but where a party holding a secret key can distinguish this sequence from random. In the context of backdoored PRGs, the secret key is viewed as a potential vulnerability of the PRG. A PRC is in particular a trapdoor/backdoored PRG, since codewords appear uniformly random to an outside observer but can be detected with a secret key.

However, a PRC comes with the additional property of robustness. This is especially interesting in the context of backdoored PRGs, where an immunizer may be applied to the PRG output in an attempt to thwart the adversary holding the backdoor. For example, one might apply a hash to the PRG output; [\[DGG](#page-63-0)<sup>+</sup>15] show that this immunizer is effective for certain PRGs. In that work they consider three classes of immunizers: public immunizers where the adversary can construct the trapdoor PRG based on knowledge of the seed of the function to be applied, semi-private immunizers where the adversary does not know the seed when constructing the PRG but does know it at attack time, and private immunizers where the adversary does not know the seed at all. Our PRCs show a strong impossibility result for immunizers against an adversary distinguishing PRG outputs from uniform randomness. For any immunizers in the class of channels that the PRC is robust to, the adversary can distinguish a single immunized output from uniform randomness with overwhelming probability. This applies even to private immunizers, since the randomness of the channel is not known to the code detection algorithm.