# An International Standard For Assessing Trustworthiness In **Media**

Publisher: IEEE Cite This  PDF
Deepayan Bhowmik ; Sabrina Caldwell ; Jaime Delgado ; Touradj Ebrahimi ; Nikolaos Fotos ; Xiaojun Gu All **Authors** 
209 Full Text Views Alerts Manage Content Alerts Add to Citation Alerts Abstract Document Sections 1. Introduction 2. Background 3. Jpeg Trust 4. Example Use Case 5. Conclusions and Future Plans Authors Figures References Keywords Metrics More Like This Footnotes Downl PDF
Abstract: The proliferation of synthetic media generation technologies, such as generative AI, has led to a surge of media content generation and consumption. While this progress o... **View more**

## **Metadata**

| Abstract:   |
|-------------|

The proliferation of synthetic media generation technologies, such as generative AI, has led to a surge of media content generation and consumption. While this progress opens new opportunities, especially in creative industries, it also causes challenges, including piracy, fake media distribution, and concerns about trust and privacy. In the creative sector, media modifications are often part of the production pipelines and in many application domains, creators need or want to declare the type of modifications that were performed on the media asset. The cryptographically signed association of provenance information with the media asset itself provides a trust link between the owner or editor of a media asset and its consumers. The absence of such assertions may reveal the lack of trustworthiness in media assets or worse, the intention to hide the existence of manipulations. This paper describes the JPEG Trust framework
(ISO/IEC 21617) that aims to establish trust in digital media creation, modification, annotation, distribution and consumption. The framework provides standardized protocols to extract indicators to assess trustworthiness, means to annotate media provenance, and securely link the assets and associated annotations together.

Published in: 2024 IEEE International Conference on Image Processing (ICIP)
Date of Conference: 27-30 October 2024 Date Added to IEEE *Xplore*: 27 September 2024
 **ISBN Information:**
 ISSN Information:
DOI: 10.1109/ICIP51287.2024.10647585 Publisher: IEEE Conference Location: Abu Dhabi, United Arab Emirates

## Section 1. Introduction

Media manipulation can be traced back over 150 years to 1860 when Abraham Lincoln's head was placed on John Calhoun's portrait [1]. While media manipulations are seen as malpractices, manipulations are commonplace in wider usage scenarios, starting from editing for entertainment and creative industries (legitimate) to gaining political advantages, spreading misinformation or harming others' reputations and finances [2]. Technological developments in software toolsets and recent advancements in Artificial Intelligence (AI), particularly generative AI, have created a disruptive inroad over the last few years permitting near-realistic synthetic content modification and generation with ease.

 Contents Media manipulation detection has been a subject of interest for many years in the signal processing/computer vision community, with a plethora of algorithms proposed in the recent past. Traditional algorithms include camera-based image forgery detection [3], identifying seam curving in JPEG re-compressed images [4], segmentation-based image copy-move forgery detection [5] or detection of object-based forgery [6]. In recent approaches, deep learning has been heavily used in detecting image re-colorization [7], deepfake detection through multi-attention models [8], analyzing convolutional traces [9], feature inconsistencies
[10] or region discrepancies [11], and general image manipulation detection using multimodal fusion [12].

While such algorithms offer crucial advancement in manipulation detection, they are not readily usable on their own in the absence of a larger framework for providing end-to-end content provenance information [13]. Additionally, media modifications are not always negative, as they are increasingly a normal and legal component of many production pipelines. However, in many application domains, creators need or want to declare the type of modifications that were performed on the media asset. A lack of such declarations in these situations may reveal the lack of trustworthiness of media assets or the intention to hide the existence of manipulations.

To address those challenges, the Joint Photographic Experts Group (JPEG) committee (ISO/IEC JTC 1/SC
29/WG 1) has initiated a new international standard, JPEG Trust (ISO/IEC 21617), which is expected to be published in 2024. The standard aims to ensure interoperability between a wide range of applications dealing with media asset creation and modification. To this end, JPEG Trust provides a comprehensive framework for individuals, organizations, and governing institutions interested in establishing an environment of trust for the media that they use and supporting trust in the media they share online. This framework addresses aspects of providing provenance information, extracting and evaluating trust indicators, and handling privacy and security concerns, and provides standardized protocols to extract indicators to assess trustworthiness and means to annotate media assets and securely link the assets and annotations together. This paper describes the JPEG Trust framework's Core Foundation and examples of usage scenarios that will benefit adopters of this standard, both technology developers and end users.

## Section 2. Background 2.1. Explorations Leading To Jpeg **Trust**

The inception of JPEG Trust can be traced back to deliberations within the JPEG standardization committee commencing in 2018. At this juncture, the committee began exploring innovative ways, best practices and potential standards at the intersection of imaging and blockchain technologies, aiming at solutions based on blockchain and distributed ledger technologies to address ownership, integrity, conditional access and other security concerns around digital images. Discussions within this period primarily revolved around organization of a number of workshops with invited expert speakers in media blockchains, along with analysis of solutions to embedding image metadata in conjunction with blockchain and distributed ledger technologies. Efforts were also undertaken to better understand and document use cases where blockchain can be used to resolve image-centric problems, identification of requirements arising from resolutions to these problems, understanding of defacto or international standardization efforts in blockchain and distributed ledger technologies, and attempting to identify areas of standardization where JPEG can play a role and potentially publish specifications with a view to securing interoperability [14].

With the proliferation of fake news relying on visual information becoming increasingly prevalent, from 2020, the activity was focused on the challenges of modifications of images or synthesis of photo-realistic images such as those in deepfakes and generative AI [2]. Efforts were devoted to a better understanding, identification and clustering requirements of use cases in modification and processing of visual content, not only from a malicious and fraudulent perspective but also exploring positive aspects and advantages of such technologies in support of creativity and modern visual storytelling approaches.

In response to the escalating urgency of the challenges in fake media, JPEG issued a formal call for proposals in 2022, inviting contributions from a wide array of stakeholders, including researchers, technologists and professionals, and encouraging submissions of solutions that best cope with both good faith and malicious intended applications relying on advanced content alterations and synthesis, notably thanks to a recent surge in the use of artificial intelligence for such purposes. A total of six proposals from industry and academia responded to the call and underwent rigorous evaluations, with criteria defined to precisely assess how well each submission addressed identified requirements. After deliberation, the JPEG committee selected the proposal from the Coalition for Content Provenance and Authenticity (C2PA) [15] as a starting point and undertook an effort to further extend it to effectively fulfil as many as possible use cases coping with as large as possible range of trust models in an interoperable way and under the auspices and governance of a well established international standardization committee, hence ensuring interoperability among different approaches adopted around the world for trustworthiness. To better reflect the scope of the standardization effort, establishing trust in our media assets, JPEG Fake Media was renamed to JPEG Trust.

2.2. The JPEG **Systems Framework**
JPEG Systems (ISO/IEC 19566) is a suite of specifications that extend JPEG coding standards with system aspects and extensions. It describes file formats, metadata tools and functionalities that are independent of the used image coding solution, including the commonly used JPEG 1, JPEG 2000 and JPEG XL. JPEG Trust leverages this systems architecture and in particular builds on the JPEG Universal Metadata Box Format
(JUMBF, ISO/IEC 19566-5) and JPEG Privacy and Security (ISO/IEC 19566-4) [14, 16].

The JPEG universal metadata box format (JUMBF) standard [17], first published in 2019, specifies a container format that enables embedding any type of metadata in media assets, including JPEG 1 and ISO
Base Media File Format (ISOBMFF) based formats [18]. The format also provides additional tools that enable means for interacting with the embedded data. These tools include a mechanism for data type identification as well as labels and identifiers for referencing and requesting metadata. Both C2PA and JPEG Trust adopt JUMBF as the container format to embed provenance information and other metadata.

JPEG Privacy and Security, published in 2020, introduces essential tools for protecting media and its associated metadata, with a specific focus on user privacy. The standard provides a signaling syntax that allows the protection of elements of a media asset from general access. For example, sensitive metadata such as a GPS location can be encrypted, or a specific region of interest depicting a person can be obfuscated. The standard allows for the specification of distinct access rights for each protected element independently.

Given that provenance information frequently contains potentially sensitive details about the stakeholders involved, the JPEG Trust standard builds upon the foundation laid by the JPEG Privacy and Security standard, with the objective to broaden the scope of the available tools for protecting authenticity and provenance information but also others such as authorship and ownership to mention some. By doing so, it can ensure that the privacy of all actors involved in the life cycle of a media asset can be appropriately preserved.

## 2.3. Reactive And Proactive Content **Authentication**

Two general methods can be distinguished to address challenges associated to generative media and are broadly referred to as reactive and proactive approaches. Reactive approaches rely on detection techniques that automatically or semi-automatically analyse media asset content e.g**., a picture, and provide confirmation**
of its authenticity. This information could be also provided with an associated degree of likelihood such as a probability of authenticity and eventually indications on the location of areas with high likelihood of alteration. Due to the diversity of different approaches to alter or synthesise content, it remains a challenge to develop universal and reliable detection methods. Such reactive approaches however are needed for legacy contents and for situations where it is not possible to verify authenticity of a content using alternative techniques.

Proactive approaches, as opposed to reactive, would require proactive provenance and tracing mechanisms.

Such approaches may leverage different technologies to securely annotate provenance and tracking information. While [19] uses distributed ledger technologies to enable the registration and certification of provenance information, [20] is based on public key infrastructure (PKI) technology to allow entities to express authentic provenance statements for a media asset. In addition, the International Press Telecommunications Council (IPTC) [21] extends existing IPTC metadata standards to support new properties for expressing trust signals. To unify the efforts around the immutable and secure annotation of provenance metadata in media, the C2PA has proposed a technical specification. It defines a data model for expressing provenance statements - called C2PA Manifests - in an integrity preserving manner, while also describing the processes to produce and verify their authenticity. The C2PA Manifest data model is compatible with JUMBF which allows the embedding of C2PA provenance information to many common media asset formats as well as the storage separately from the associated media asset.

## Section 3. Jpeg Trust

The scope of JPEG Trust is to provide a framework for establishing trust in media. This framework includes aspects of authenticity, provenance and integrity through secure and reliable annotation of the media assets throughout their life cycle [22]. The scope and the requirements of this framework are determined by a number of use cases collected from a wide range of stakeholders, including businesses, governmental and non-governmental organisations, academics and end users across the world over two years between 2020 and 2022 through a series of workshops, discussion forums and other form of communications . The use cases, grouped into A) Misinformation and disinformation, B) Forgery/Media forensics, C) Media creation and D)
Media modifications, led to three main categories of requirements:1)Media creation and modification descriptions, 2) Metadata embedding and referencing and 3) Authenticity, integrity, and trust model [23, 24].

1 Guided by the requirements outlined above, the fundamental structure of the JPEG Trust, called **Core** Foundation**, is proposed for standardisation in 2024 (subject to final ISO approval by its national member** bodies). This section provides a description of various components of the Core Foundation:1) JPEG Trust framework, 2) Media life cycle annotations, 3) Embedding and referencing, 4) Identification of actors, 5)
Media asset content binding and 6) Privacy and protection.

![3_image_0.png](3_image_0.png)

Fig. 1:

JPEG Trust framework indicating pathways to establish a trust report from the media asset by extracting trust credentials combined with a target trust profile.

## 3.1. Jpeg Trust **Framework**

The JPEG Trust framework establishes that a media asset consists of the media asset content, media asset metadata, and a *Trust Record*. The Trust Record is a tamper-evident unit consisting of one or more *Trust* Manifests. The Trust Manifests contain a series of statements, called *Assertions***, that cover areas such as asset**
creation, device details, authorship, edit actions, bindings to content and other information associated with the media asset. A set of *Trust Indicators* **can be derived from the Trust Record as well as from other**
metadata or the media asset content. These Trust Indicators are gathered together into a *Trust Credential*,
which can be used to assess the trustworthiness of a media asset in a given context through the use of a specified *Trust Profile***. The result of this evaluation is documented in a Trust Report. The framework and its** core components are illustrated in Fig. 1. The framework consists of the following components:
The Trust Record consists **of one or more Trust Manifests and is expressed in this standard through a**
JUMBF [17] superbox serialisation format composed of a series of other JUMBF boxes and superboxes, each identified by their own Universally Unique Identifier (UUID) and label in their JUMBF Description box.

The Trust Manifest **is the set of information about the media asset provenance, while a Trust Declaration is**
a special type of Trust Manifest with only mandatory assertions that always come first in the Trust Record. Each Trust Manifest may contain a Verifiable Credentials (VC) Store, Assertions, a Claim, and a Claim Signature.

A Trust Declaration **is a specific type of Trust Manifest that shall only be defined during the creation of a** media asset and shall only contain a specific set of mandatory assertions (e.g., file hash) as well as the Claim and Claim Signature.

Trust Indicator **are parameters that may be used to assess the trustworthiness of a media asset in a given**
context. Trust Indicators are derived from one or more of the following sources: media asset content, the trust record, and the media asset metadata. Each of these is represented as a separate *section* **of the Trust** Credential, along with any additional indicators that a given workflow may produce.

Trust Credential **consists of Trust Indicators extracted from the two portions of the media asset, namely** metadata (including both Trust Record and other metadata) and content.

A Trust Profile1 **enables the generation of a Trust Report from a Trust Credential. A Trust Profile contains a**
block of information about the Trust Profile and a set of statements that are evaluated against a Trust Credential. Each statement has an expression/formula that takes one or more trust indicators as input and produces a single output value. The Trust Profile is expressed in Ain't Markup Language (YAML), and the statement expressions/formulas are expressed as json-formula.

A Trust Report **results from combining a Trust Profile and a Trust Credential, thereby documenting the** result of evaluating the Trust Credential against the Trust Profile. The evaluation helps to indicate a level of trustworthiness **for a given media asset. A Trust Indicator presented in the Trust Credential (extracted from** the media asset) passes the evaluation if it satisfies the Trust Indicator requirement in the Trust Profile.

3.2. Media asset life cycle **annotations**
Media asset life cycle annotations facilitate the production, distribution, and consumption of media assets in a trustworthy manner. The use of these annotations is expected to improve trust in media consumption by expressing the provenance of a media asset throughout its lifecycle while ensuring media integrity and authenticity. Reliable association of the media lifecycle annotations with the corresponding media asset is essential for ensuring that no information is tampered with. This enables detection capabilities in the event of alteration of the media asset. This part of the standard specifies that interoperability is essential to achieving wide adoption of such an annotation ecosystem. In addition, it identifies that media assets consist of at least two parts - content and metadata. The overview of the media life cycle annotation is shown in Fig. 2.

![4_image_0.png](4_image_0.png)

Fig. 2:

Assertions relating to media life cycle annotation. Assertions provide necessary Trust Manifests leading to Trust Indicators, Credentials and, finally, a Trust Report.

In this framework, an annotation for representing information about the provenance of a media asset is called an *Assertion*. An assertion is labelled data representing a statement made by an *Actor* **about a media asset.**
Each of the actors in the system that creates or processes an asset should produce one or more assertions about when, where, and how the asset originated or was transformed. Actors may be human, thus adding human-generated information (i.e**., copyright) or machines (software/hardware) providing the information** they generated (i.e**., camera type or lens details). An assertion may also include information about the actors**
themselves. The assertions proposed in this standard are:
Intellectual Property Right (IPR) **information, which includes media asset type as defined by IPTC photo** and video metadata, information regarding training and data mining for AI media content generation, and other standard metadata such as Exif and IPTC.

Actions **record an array of steps that are carried out during the creation or subsequent modification of the** media asset. While the creation refers to the activity relating to the source of the media asset, a modification involves any type of change to the media asset, including the media asset content and metadata.

Assertion metadata **In various scenarios it is necessary or useful to provide additional information about**
an assertion, such as the actors, when (date and time) it was generated or other data that may help users to make informed decisions about the provenance or veracity of the assertion data.

Extent of Modification **This assertion is used to provide a means to signal the extent of modifications of** this asset compared to a reference version of the asset by providing one or more objective similarity metrics, e.g., PSNR, SSIM, etc.

## 3.3. Embedding And **Referencing**

In order to support many of the requirements of JPEG Trust, Trust Manifests need to be stored (serialized)
into a structured binary data store that enables some specific functionality, including the ability to 1) store multiple manifests in a single container, 2) refer to individual elements (both within and across manifests) via URIs, 3) clearly identify the parts of an element to be hashed, 4) store pre-defined data types (e.g., JSON and CBOR) and 5) store arbitrary data formats (e.g**., XML, JPEG, etc.).**
In supporting all of the requirements above, this standard has chosen the JUMBF container format [17], which is natively supported by the JPEG family of formats and is compatible with the box-based model (i.e., ISOBMFF) used by many common image and video file formats. Using JUMBF enables all the same benefits of other native box-based formats but with a few additional benefits, such as URI References, in addition to being able to work with the various JPEG standards as well as other formats.

### 3.4. Identification Of **Actors**

Actors, human or non-human (hardware or software) entities that are participating in the media ecosystem, are an integral part of the Trust Manifest. This standard proposes the identification of the actors through their W3C Verifiable Credentials [25] to the claim generator as part of establishing provenance for an asset. Actors may be individuals, groups or organizations. W3C Verifiable Credentials, as specified in its Data Model, are used in this standard to provide additional detail about the actors identified in assertions with more information, potentially providing additional trust signals.

## 3.5. Media Asset Content **Binding**

Content integrity plays a major role in establishing trust, and this standard proposes the use of a signed cryptographic hash, which is bound to the media asset for such trust manifest. Trust manifests are validated by a process that tests the validity of the associated claim signature as well as the time stamp and any included credential revocation information. A validator may also evaluate each of the assertions in the trust manifest, and those results become new trust indicators that are added to the full list of trust indicators (for a given asset) and compiled together into a trust credential. This trust credential may also then undergo evaluation and reporting in alignment with the requirements of a provided trust profile(s). Content binding in this standard is achieved through:

#### Cryptographic Binding To Content:

This is accomplished using standard cryptographic hashes, such as SHA2-256. These hashes also enable a validator to detect if the asset has been modified since the trust manifest was constructed.

#### Use Of Digital Signatures:

A trust manifest is signed by the claim generator of the manifest, using a certificate for a specific actor. This signature is used not only to ensure that the manifest has not been tampered with since it was created but also to clearly identify (and enable validation of) the actor that claims to have created it. This is accomplished through the use of standard digital signature algorithms and key types, such as RSA or ECDSA.

#### Validation:

The determination of whether the Trust Record for a given media asset is valid is accomplished through the use of a validation process. The process works by first determining if the claim signature of the active trust manifest is valid, including validation of an associated time stamp and credential revocation information. If there are no problems with the active trust manifest, then each of the assertions in the trust manifest is validated, including checking its associated hash provided in the claim. If any of the assertions are invalid, then the entire trust manifest is considered invalid. The results of each of these validations are expressed as trust indicators, followed by the generation of trust credentials and trust reports to verify the integrity of the content.

The need to ensure privacy and protection is crucial to establishing trust in media. Various parts of a media asset can disclose privacy-related information: the media asset content, the media asset metadata, and the trust record. In principle, an actor shall be able to control the level of privacy of a media asset. The standard specifies the mechanisms to anonymize a media asset and control access to sensitive information. It allows an actor to apply these privacy-enhancing capabilities in different places of a media asset. The standard defines two categories of privacy preservance mechanism:
Anonymization **The identity of an actor or a location can be signaled in various parts of the Trust Record.**
Based on the use case, anonymization of the privacy-related information are achieved either by a) W3C Verifiable Credentials or b) *Redaction*.

Obfuscation **Apart from anonymizing a media asset, it is also essential to enhance privacy by allowing an**
actor to control the access to sensitive information, either within the media asset content or outside of it. This specification is aligned with the JPEG family of standards ISO/IEC 19566-4:2020 to allow the protection of assertions **that contain privacy-related information and achieved by a) Protection of an Assertion and b)** Protecting the media asset content.

## Section 4. Example Use Case 4.1. Ai Generated **Content**

The production of AI Generated Content (AIGC) has surged over the last years, serving various creative and entertaining purposes. However, the surge has also given rise to instances where AIGC is utilized to spread misinformation. Consequently, numerous governing institutions are taking measures to enhance end-user awareness regarding how content has been generated and in particular regarding the involvement of AI. Meta and OpenAI, for example, comply to such regulations and claim to tag AI-generated images on their platforms.

![6_image_0.png](6_image_0.png)

Fig. 3: Media platform uses JPEG Trust framework to identify whether the media asset is generated by AI.

As introduced earlier, addressing this issue can take a reactive approach, by adopting detection algorithms, or a proactive one, mandating provenance signaling at the time of creation. Since the optimal strategy depends on the specific context, JPEG Trust has been designed to accommodate both approaches.

For the proactive approach, as the example shown in Fig. 3, a media platform can define a such Trust Profile, which contains a check on whether the content is generated by AI. When an AIGC was created, its digital source type in Trust Declaration is defined as "trainedAlgorithmicMedia". After receiving an AI-generated media asset contributed by the creator, the media platform extracts its digital source type and places it in a trust credential. A Trust Report is generated by validating the trust credential according to the Trust Profile as defined above. Since the digital source type in Trust Declaration is "trainedAlgorithmicMedia", the output of the Trust Report should be "Yes, the media is AIGC". Otherwise, "No, the media is not AIGC". Moreover, the media platform can further process the media content according to the Trust Report, such as label the media AIGC.

For the reactive approach, while JPEG Trust does not specify any detection algorithms itself, the results of such algorithms can be expressed as Trust Indicators and hence be used in a Trust Profile. To record the results of a detection algorithm, the algorithm provider registers a JSON-LD context in the Trust Credential and adds one or more Trust Indicators to signal the result of the detection algorithm. E.g. the algorithm may produce a probability of the likelihood that the asset is generated by AI expressed as a Trust Indicator named aigc_probability. Since this value is generated from the media asset content, this value is registered in the content section of the Trust Credential.

Subsequently, a Trust Profile can add rules to check this value and report it to the end user. The Trust Profile can be specified to simply communicate the value to the end user, or it can set a threshold and signal a binary compliance result. For example, a media asset can be considered compliant with the profile if the value of the aigc_probability is lower than 30 percent.

## 4.2. **Insurance**

In a typical scenario in the insurance industry, after a car accident, the insured needs to take a photo to record the accident and send this photo to the insurance company. Naturally, the insurance company is concerned about the authenticity of the photo to prevent malicious insured from obtaining more benefits by forging or modifying the accident photo.

In this scenario, when an accident occurs, the insured will declare to the insurance company and upload accident photo later. After recording the relevant information of the accident, the insurance company can generate corresponding Trust Profile, which may require that **a) the generation time of the accident photo** should be close to the insured's reporting time, b) the location where the accident photo is generated shall be the same as the location of the accident and c) the accident photo shall not be modified.

Later, when the insurance company receives the accident photo sent by the user, it will extract important Trust Indicators from the image assets such as time, location, and photo modification information. Then it generates the Trust Credential. Finally, the insurance company matches Trust credential with Trust Profile to generate the final Trust Report. According to this report, insurance companies will be able to conveniently evaluate the authenticity of accident photos uploaded by the insured.

## Section 5. Conclusions And Future Plans

Manipulation of images and the evolution of image generation technologies are continuously happening. At the same time, trust in digital media is of paramount importance in all the steps of the media asset life cycle, from its creation to its final consumption. Keeping track of the evolution of a media asset, including any modifications, annotations or distributions between its creation and consumption steps is key for assessing trust.

The JPEG committee is developing a globally interoperable solution to improve trust in digital media: JPEG
Trust. Its Core Foundation, expected to become an International Standard in 2024, specifies a framework addressing aspects of authenticity, provenance and integrity through secure and reliable annotation of media assets throughout their life cycle. Further development of the JPEG Trust standard, including new parts, will continue to be based on real-world use cases and requirements and the expertise of the global community.

#### 

Figures 

References 

Keywords 

Metrics 

Footnotes 

#### More Like This

An Efficient 3D Data Annotation and Object Detection Pipeline for Production Line 2024 IEEE International Conference on Omni-layer Intelligent Systems (COINS)
Published: 2024 An Empirical Study to Scrutinize the Interplay Between Safety and Sustainable Production Performance in the Context of Chemical Industry 2021 IEEE International Conference on Industrial Engineering and Engineering Management (IEEM) Published: 2021 Show More

### Ieee Account

» Change Username/Password
» Update Address Purchase Details
»Payment Options »Order History
»View Purchased Documents Profile Information
» Communications Preferences »Profession and Education »Technical Interests Need Help?

» **US & Canada:** +1 800 678 4333 »**Worldwide:** +1 732 981 0060 » Contact & Support About IEEE *Xplore* | Contact Us | Help | Accessibility | Terms of Use | Nondiscrimination Policy | Sitemap | Privacy & Opting Out of Cookies A not-for-profit organization, IEEE is the world's largest technical professional organization dedicated to advancing technology for the benefit of humanity. © Copyright 2024 IEEE - All rights reserved. Use of this web site signifies your agreement to the terms and conditions.